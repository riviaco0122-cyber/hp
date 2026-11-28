// 中央揃えの行の、行末の句読点による見た目のずれの点検（人の指摘 2026-11-28：アキヤドのトップの大見出し
// 「売る。活かす。」が、行末の「。」のせいで左に寄って見えた）。
// 全角の「。」「、」は点が字の左下にあり、右半分が空く。中央揃え（右揃え）の行の最後がこの字だと、行の見た目の中心が左にずれる。
// 全ページを開き、中央揃えの要素の行ごとに「左の空き」と「右の空き（行末が句読点なら、点の右の空きも足す）」を比べ、
// 差が文字の大きさの 0.3 倍を超える行を数える（0件にする。直し方は design-guide 3章：行末の句読点を .pe で半分の幅に詰める）。
// あわせて、句読点だけが1行に取り残されている所（p-e の中に display: block が効いている）も数える。
// 使い方: node tools/check/punct_center.js [--widths 390,1280] [--only media,index]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const root = path.resolve(__dirname, '..', '..');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const widths = arg('--widths', '390,1280').split(',').map(Number);
const only = (arg('--only', '') || '').split(',').filter(Boolean);
const T = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.avif': 'image/avif' };
const list = d => fs.readdirSync(path.join(root, d)).filter(f => f.endsWith('.html')).map(f => d + '/' + f);
let pages = list('pages').concat(list('pages/media'));
if (only.length) pages = pages.filter(p => only.some(o => p.endsWith('/' + o + '.html') || p.endsWith('/' + o)));
(async () => {
  const b = await chromium.launch(); let total = 0; const out = [];
  for (const w of widths) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.route('http://site.local/**', r => {
      const f = path.join(root, decodeURIComponent(new URL(r.request().url()).pathname));
      if (fs.existsSync(f) && fs.statSync(f).isFile()) return r.fulfill({ body: fs.readFileSync(f), contentType: T[path.extname(f)] || 'application/octet-stream' });
      return r.fulfill({ status: 404, body: '' });
    });
    for (const pg of pages) {
      await p.goto('http://site.local/' + pg, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
      const found = await p.evaluate(() => {
        const res = [];
        // 文字を直接もつ、中央揃え・右揃えの要素（見えているもの）
        const els = [...document.querySelectorAll('body *')].filter(el => {
          const s = getComputedStyle(el);
          if (!/center|right|end/.test(s.textAlign) || /inline/.test(s.display) || s.visibility === 'hidden') return false;
          const r = el.getBoundingClientRect(); if (!r.width || !r.height) return false;
          return [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || [...el.children].some(c => getComputedStyle(c).display === 'inline' || getComputedStyle(c).display === 'inline-block');
        });
        for (const el of els) {
          if (el.closest('[aria-hidden="true"], svg, button, .btn, [class*="btn"], input, select, textarea')) continue;
          const s = getComputedStyle(el); const fs = parseFloat(s.fontSize);
          const box = el.getBoundingClientRect(); const L0 = box.left + parseFloat(s.paddingLeft), R0 = box.right - parseFloat(s.paddingRight);
          // 1文字ずつの位置を取り、行（上端）ごとにまとめる
          const chars = []; const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
          for (let n = walker.nextNode(); n; n = walker.nextNode()) {
            // 中央揃えの子要素（別のかたまり）の文字は、その子要素で数える
            let a = n.parentElement, own = true; while (a && a !== el) { const d = getComputedStyle(a).display; if (!/inline/.test(d)) { own = false; break; } a = a.parentElement; }
            if (!own) continue;
            const t = n.textContent; const rg = document.createRange();
            for (let i = 0; i < t.length; i++) { if (/\s/.test(t[i])) continue; rg.setStart(n, i); rg.setEnd(n, i + 1); const rr = rg.getClientRects()[0]; if (rr && rr.width) chars.push({ c: t[i], l: rr.left, r: rr.right, t: Math.round(rr.top + rr.height / 2), fs: parseFloat(getComputedStyle(n.parentElement).fontSize) }); }
          }
          if (!chars.length) continue;
          const lines = []; for (const ch of chars) { const ln = lines.find(x => Math.abs(x.t - ch.t) < fs * 0.5); if (ln) ln.cs.push(ch); else lines.push({ t: ch.t, cs: [ch] }); }
          if (lines.length < 1) continue;
          for (const ln of lines) {
            ln.cs.sort((a, b) => a.l - b.l); const first = ln.cs[0], last = ln.cs[ln.cs.length - 1];
            if (!/[。、，．]/.test(last.c)) continue;
            // 句読点の点は字の左 0.4 の幅に入っている。点の右の空き＝字の右端 − (字の左端 + 0.4em)
            const inkR = Math.min(last.r, last.l + last.fs * 0.4);
            const left = first.l - L0, right = R0 - inkR;
            const isCenter = /center/.test(s.textAlign);
            const diff = isCenter ? (right - left) : (R0 - inkR);
            if (diff > last.fs * 0.3) {
              const name = (el.className && String(el.className).split(' ')[0]) || el.tagName.toLowerCase();
              res.push(`${isCenter ? '中央' : '右'}揃えの行末の「${last.c}」で ${Math.round(diff)}px 左にずれる ${name}「${ln.cs.map(x => x.c).join('').slice(-16)}」`);
            }
          }
        }
        // 句読点だけが1行に取り残されていないか（詰める部品 p-e の中の span に、ほかのルールの display: block が効くと起きる。人の指摘 2026-11-28）
        for (const pe of document.querySelectorAll('p-e, .pe')) {
          if (pe.closest('[aria-hidden="true"]') && !pe.getClientRects().length) continue;
          const sp = pe.querySelector(':scope > span'); if (!sp || !sp.getClientRects().length) continue;
          if (!/inline/.test(getComputedStyle(sp).display) || !/inline/.test(getComputedStyle(pe).display)) res.push(`句読点が1行に取り残される（p-e の中が ${getComputedStyle(sp).display}）「${(pe.parentElement.textContent || '').trim().slice(0, 16)}」`);
        }
        return res;
      });
      const uniq = [...new Set(found)];
      if (uniq.length) { out.push(`## ${pg}（${w}px）`, ...uniq.slice(0, 15).map(x => '- ' + x)); total += uniq.length; }
    }
    await p.close();
  }
  await b.close();
  console.log(out.join('\n'));
  console.log(`中央揃えの行末の句読点のずれ（幅 ${widths.join('・')}px）: ${total}件`);
})();
