// 文字の左右の余白の点検（人の指摘 2026-11-27：スマホの最初の画面で文字が左に寄りすぎていた）。
// スマホ幅で全ページ（または --only のページ）を開き、文字のかたまり（段落・見出し・ボタン・入力欄）について
//   ①画面の端からの余白が、決まりの最小値（既定 16px）より狭い
//   ②左右の余白が大きく違う（中央揃えの文や、横幅いっぱいのボタン・入力欄で、差が 6px を超える）
// を数える。横にスクロールする並び（カルーセル）の中や、見えない要素は数えない。
// 使い方: node tools/check/gutters.js [--widths 375,390] [--only media,index] [--min 16]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const root = path.resolve(__dirname, '..', '..');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const widths = arg('--widths', '375,390').split(',').map(Number);
const only = (arg('--only', '') || '').split(',').filter(Boolean);
const MIN = +arg('--min', '16');
const T = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.avif': 'image/avif' };
const list = d => fs.readdirSync(path.join(root, d)).filter(f => f.endsWith('.html')).map(f => d + '/' + f);
let pages = list('pages').concat(list('pages/media'));
if (only.length) pages = pages.filter(p => only.some(o => p.endsWith('/' + o + '.html') || p.endsWith('/' + o)));
(async () => {
  const b = await chromium.launch(); let total = 0; const out = [];
  for (const w of widths) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.route('http://site.local/**', r => {
      let u = decodeURIComponent(new URL(r.request().url()).pathname);
      const f = path.join(root, u);
      if (fs.existsSync(f) && fs.statSync(f).isFile()) return r.fulfill({ body: fs.readFileSync(f), contentType: T[path.extname(f)] || 'application/octet-stream' });
      return r.fulfill({ status: 404, body: '' });
    });
    for (const pg of pages) {
      await p.goto('http://site.local/' + pg, { waitUntil: 'load' }); await p.waitForTimeout(300);
      const found = await p.evaluate(({ MIN }) => {
        const W = document.documentElement.clientWidth, res = [];
        const inScroller = el => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { const s = getComputedStyle(a); if (/(auto|scroll)/.test(s.overflowX) && a.scrollWidth > a.clientWidth + 2) return true; if (a.matches('header, footer, nav, .fixed-cta, dialog, [aria-hidden="true"]')) return true; } return false; };
        document.querySelectorAll('main :is(p, h1, h2, h3, h4, li, dt, dd, .btn, a[class*="btn"], input, button, label)').forEach(el => {
          const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
          if (!r.width || !r.height || s.visibility === 'hidden' || r.bottom < 0 || r.right <= 0 || r.left >= W || inScroller(el)) return; // 画面の外（迷惑投稿よけの欄など）は数えない
          if (!el.textContent.trim() && !/INPUT|BUTTON/.test(el.tagName)) return;
          const L = Math.round(r.left), R = Math.round(W - r.right);
          const name = (el.className && String(el.className).split(' ')[0]) || el.tagName.toLowerCase();
          const txt = (el.textContent || el.placeholder || '').trim().slice(0, 18);
          if (L < MIN - 0.5 || R < MIN - 0.5) res.push(`余白が狭い 左${L}px・右${R}px ${name}「${txt}」`);
          else if (((s.textAlign === 'center' && r.width > W * 0.6) || r.width > W * 0.8) && Math.abs(L - R) > 6) res.push(`左右がそろっていない 左${L}px・右${R}px ${name}「${txt}」`);
        });
        return res;
      }, { MIN });
      const uniq = [...new Set(found)];
      if (uniq.length) { out.push(`## ${pg}（${w}px）`, ...uniq.slice(0, 12).map(x => '- ' + x)); total += uniq.length; }
    }
    await p.close();
  }
  await b.close();
  console.log(out.join('\n'));
  console.log(`文字の左右の余白（幅 ${widths.join('・')}px、最小 ${MIN}px）: ${total}件`);
})();
