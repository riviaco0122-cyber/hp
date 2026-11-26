// Figma から書き出したイラストの SVG を、記事用に整える（playbook 15-4）。
// 使い方: node tools/illust_fit.js <書き出した.svg> images/illust/<名前>.svg
// ・全体を覆う背景の四角（白・灰）を消す（図の淡い地に、白い箱が浮かないように）
// ・id 属性を消す（同じページに複数のイラストを置いても、id がぶつからないように）
// ・絵の範囲を実際に測って viewBox を詰め、width/height を外す（幅に合わせて伸び縮みするように）
const { chromium } = require('playwright'); const fs = require('fs');
const [src, out] = process.argv.slice(2);
if (!src || !out) { console.error('使い方: node tools/illust_fit.js <in.svg> <out.svg>'); process.exit(1); }
let svg = fs.readFileSync(src, 'utf8');
if (/<script|<foreignObject|\son\w+=/i.test(svg)) { console.error('スクリプトを含む SVG は取り込まない'); process.exit(1); }
const m = svg.match(/viewBox="0 0 (\d+) (\d+)"/); const [W, H] = m ? [m[1], m[2]] : [0, 0];
svg = svg.replace(new RegExp(`<(rect|path)[^>]*?(width="${W}" height="${H}"|d="M${W} 0H0V${H}H${W}V0Z")[^>]*/>\\s*`, 'g'), (t, tag, a, i) => (i < 600 ? '' : t))
  .replace(/\sid="[^"]*"/g, '').replace(/\sclip-path="url\([^)]*\)"/g, '').replace(/<defs>[\s\S]*?<\/defs>\s*/g, '');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.setContent(`<!doctype html><body style="margin:0">${svg}</body>`);
  const box = await p.evaluate(() => { const s = document.querySelector('svg'); const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    while (s.firstChild) g.appendChild(s.firstChild); s.appendChild(g); const r = g.getBBox(); return { x: r.x, y: r.y, width: r.width, height: r.height }; });
  await b.close();
  const pad = 12, vb = [box.x - pad, box.y - pad, box.width + pad * 2, box.height + pad * 2].map(v => Math.round(v));
  svg = svg.replace(/<svg[^>]*>/, `<svg viewBox="${vb.join(' ')}" fill="none" xmlns="http://www.w3.org/2000/svg">`);
  fs.writeFileSync(out, svg);
  console.log(out, `viewBox ${vb.join(' ')}`, `${(svg.length / 1024).toFixed(1)}KB`, `比率 ${vb[2]} / ${vb[3]}`);
})();
