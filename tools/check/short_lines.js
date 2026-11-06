// 最後の行が短い（「ます。」だけなど）文を探す。スマホの主な幅で各ページを開き、段落・リスト・見出し・ラベルの最後の行の文字数を数える。
// 使い方: node tools/check/short_lines.js [--max 4] [--widths 375,390] [--only ページ名の一部,...] [--out ファイル]
const { chromium } = require(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const MAX = +arg('--max', 4), WIDTHS = arg('--widths', '375,390').split(',').map(Number);
const ONLY = (arg('--only', '') || '').split(',').filter(Boolean), OUT = arg('--out', '');
const root = path.resolve(__dirname, '../../pages');
let files = fs.readdirSync(root).filter(f => f.endsWith('.html')).map(f => f);
files = files.concat(fs.readdirSync(path.join(root, 'media')).filter(f => f.endsWith('.html')).map(f => 'media/' + f));
if (ONLY.length) files = files.filter(f => ONLY.some(o => f.includes(o)));
(async () => {
  const b = await chromium.launch(); const rows = [];
  for (const w of WIDTHS) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    for (const f of files) {
      await p.goto('file://' + path.join(root, f) + '?preview=1');
      await p.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important}' });
      await p.waitForTimeout(150);
      const found = await p.evaluate((MAX) => {
        const out = [];
        const blocks = document.querySelectorAll('main p, main li, main dd, main dt, main h1, main h2, main h3, main h4, main figcaption, main blockquote, main [class*="__lead"], main [class*="__text"], main [class*="__desc"], main [class*="__sub"]');
        for (const el of blocks) {
          if (el.closest('nav, header, footer, .toc, [hidden]')) continue;
          const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          if (el.querySelector('p, li, dd, div, ul, ol, table')) continue; // 中に段落を含む入れ物は除く
          if (/flex|grid/.test(cs.display) || cs.writingMode.indexOf('vertical') === 0) continue; // 横並びの部品（数字カードなど）は除く
          const text = el.innerText.trim(); if (text.length < 8 || !/[ぁ-んァ-ン一-龯]/.test(text)) continue;
          const lastPara = text.split('\n').pop(); // <br> で区切った最後の段だけを見る
          const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const r = document.createRange();
          const lines = []; let n;
          while ((n = walker.nextNode())) {
            const pe = n.parentElement; if (!pe || pe.offsetParent === null) continue;
            for (let i = 0; i < n.length; i++) {
              const c = n.data[i]; if (/\s/.test(c)) continue;
              r.setStart(n, i); r.setEnd(n, i + 1); const rc = r.getClientRects()[0]; if (!rc || !rc.width) continue;
              const last = lines[lines.length - 1];
              if (!last || rc.top > last.top + rc.height * 0.6) lines.push({ top: rc.top, s: c }); else last.s += c;
            }
          }
          if (lines.length < 2) continue;
          const tail = lines[lines.length - 1].s;
          if (lastPara.replace(/\s/g, '').length <= tail.length) continue; // <br> の後ろが元から短い（意図した改行）
          if (tail.length <= MAX) out.push({ tail, prev: lines[lines.length - 2].s.slice(-14), text: text.replace(/\s+/g, ' ').slice(0, 70), cls: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : '') });
        }
        return out;
      }, MAX);
      for (const x of found) rows.push({ w, f, ...x });
    }
    await p.close();
  }
  await b.close();
  const lines = rows.map(r => `${r.w}\t${r.f}\t${r.cls}\t…${r.prev}／${r.tail}\t${r.text}`);
  const head = `最後の行が${MAX}文字以下: ${rows.length}件（幅 ${WIDTHS.join('・')}px）`;
  if (OUT) fs.writeFileSync(OUT, head + '\n' + lines.join('\n') + '\n');
  console.log(head);
})();
