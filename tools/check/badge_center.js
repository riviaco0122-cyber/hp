// 丸い印（円の中の数字・文字。「Q」「1」「R」など）の中で、文字が真ん中にあるかの点検（人の指摘 2026-11-07。docs/design-guide.md）
// 円（border-radius 50% の小さな箱。::before／::after の印も含む）の中の文字のインクの位置を、画面を撮って実際に測る。
// 使い方: node tools/check/badge_center.js [--widths 390,1280] [--only ページ名の一部,...] [--tol 1]
//   ずれ（文字の中心と円の中心の差）が tol px（既定 1px）を超えた印を出す。終了コード: 1件でもあれば 1
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const WIDTHS = arg('--widths', '390,1280').split(',').map(Number), TOL = +arg('--tol', '1');
const ONLY = (arg('--only', '') || '').split(',').filter(Boolean);
const ROOT = path.resolve(__dirname, '..', '..');
const files = [
  ...fs.readdirSync(path.join(ROOT, 'pages')).filter(f => f.endsWith('.html')).map(f => 'pages/' + f),
  ...fs.readdirSync(path.join(ROOT, 'pages/media')).filter(f => f.endsWith('.html')).map(f => 'pages/media/' + f),
].filter(f => !ONLY.length || ONLY.some(o => f.includes(o)));

(async () => {
  const browser = await chromium.launch();
  const seen = new Map(); let bad = 0;
  for (const w of WIDTHS) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: 2 });
    for (const f of files) {
      await page.goto('file://' + path.join(ROOT, f));
      await page.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important}' });
      await page.waitForTimeout(250);
      // 円の印を集める（要素そのもの、または ::before／::after）。同じ見た目（クラス＋擬似要素）は1ページ1つだけ測る
      const badges = await page.evaluate(() => {
        const out = [], keys = new Set();
        const isCircle = cs => cs.display !== 'none' && cs.visibility !== 'hidden' && /50%|9999px|999px/.test(cs.borderRadius) &&
          Math.abs(parseFloat(cs.width) - parseFloat(cs.height)) < 1 && parseFloat(cs.width) >= 14 && parseFloat(cs.width) <= 64;
        document.querySelectorAll('main *, header *').forEach((el, i) => {
          for (const pe of ['', '::before', '::after']) {
            const cs = getComputedStyle(el, pe || null);
            if (!isCircle(cs)) continue;
            const txt = pe ? (cs.content || '').replace(/^["']|["']$/g, '') : el.textContent.trim();
            if (!txt || txt === 'none' || txt.length > 3 || /^\s*$/.test(txt)) continue;
            if (!pe && el.children.length) continue;
            const key = el.className + pe;
            if (keys.has(key)) continue;
            const r = pe ? null : el.getBoundingClientRect();
            if (!pe && (!r.width || r.bottom < 0)) continue;
            keys.add(key); el.setAttribute('data-badge', i); out.push({ i, pe, key, txt });
          }
        });
        return out;
      });
      for (const b of badges) {
        const handle = await page.$(`[data-badge="${b.i}"]`); if (!handle) continue;
        // 要素ごと撮り、円の色（背景色）の範囲と、その中の文字色の範囲から、ずれを求める（::before の印も同じ）
        const info = await handle.evaluate((el, pe) => {
          el.scrollIntoView({ block: 'center' });
          const cs = getComputedStyle(el, pe || null);
          return { bg: cs.backgroundColor, color: cs.color, w: parseFloat(cs.width) };
        }, b.pe);
        await page.waitForTimeout(50);
        const box = await handle.boundingBox(); if (!box || box.width < 8 || box.height < 8) continue;
        let shot; try { shot = await handle.screenshot(); } catch (e) { continue; }
        // 画像を解析：円の色（背景色）の範囲＝円、文字の色の範囲＝インク
        const res = await page.evaluate(async ({ png, bg, color }) => {
          const img = new Image(); img.src = 'data:image/png;base64,' + png; await img.decode();
          const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const x = c.getContext('2d'); x.drawImage(img, 0, 0);
          const d = x.getImageData(0, 0, c.width, c.height).data;
          const rgb = s => (s.match(/\d+/g) || []).slice(0, 3).map(Number);
          const B = rgb(bg), C = rgb(color);
          const near = (p, q, t) => Math.abs(p[0] - q[0]) + Math.abs(p[1] - q[1]) + Math.abs(p[2] - q[2]) < t;
          let cb = [1e9, 1e9, -1, -1], ci = [1e9, 1e9, -1, -1];
          // 円の範囲：背景色の画素。インク：円の範囲の中で、文字色に近い画素
          for (let yy = 0; yy < c.height; yy++) for (let xx = 0; xx < c.width; xx++) {
            const k = (yy * c.width + xx) * 4, p = [d[k], d[k + 1], d[k + 2]];
            if (B.length === 3 && near(p, B, 30)) { cb[0] = Math.min(cb[0], xx); cb[1] = Math.min(cb[1], yy); cb[2] = Math.max(cb[2], xx); cb[3] = Math.max(cb[3], yy); }
          }
          if (cb[2] < 0) return null;
          const cx = (cb[0] + cb[2]) / 2, cy = (cb[1] + cb[3]) / 2, rad = (cb[2] - cb[0]) / 2 * 0.82;
          for (let yy = cb[1]; yy <= cb[3]; yy++) for (let xx = cb[0]; xx <= cb[2]; xx++) {
            if ((xx - cx) ** 2 + (yy - cy) ** 2 > rad * rad) continue; // 円の内側だけ（円の外の背景を文字と取り違えない）
            const k = (yy * c.width + xx) * 4, p = [d[k], d[k + 1], d[k + 2]];
            if (C.length === 3 && near(p, C, 120) && !near(p, B, 60)) { ci[0] = Math.min(ci[0], xx); ci[1] = Math.min(ci[1], yy); ci[2] = Math.max(ci[2], xx); ci[3] = Math.max(ci[3], yy); }
          }
          if (ci[2] < 0) return null;
          const dx = ((ci[0] + ci[2]) - (cb[0] + cb[2])) / 4, dy = ((ci[1] + ci[3]) - (cb[1] + cb[3])) / 4; // 2倍で撮っているので÷2（さらに中心で÷2）
          return { dx, dy, size: (cb[2] - cb[0]) / 2 };
        }, { png: shot.toString('base64'), bg: info.bg, color: info.color });
        if (process.env.DEBUG) console.log(f, b.key, b.txt, JSON.stringify(res));
        if (!res || res.size < 10) continue;
        const off = Math.max(Math.abs(res.dx), /[Qgjpqy]/.test(b.txt) ? 0 : Math.abs(res.dy)); // 下に尾のある字（Q）は横だけ見る（尾の分だけ下に見えるのが正しい）
        const k = `${b.key}|${b.txt}`;
        if (off > TOL && !seen.has(k)) { seen.set(k, `${w}\t${f.replace('pages/', '')}\t${b.key}\t「${b.txt}」\tずれ 横${res.dx.toFixed(1)}px 縦${res.dy.toFixed(1)}px（円${res.size.toFixed(0)}px）`); bad++; }
      }
    }
    await page.close();
  }
  await browser.close();
  console.log(`丸い印の文字のずれ（${TOL}px 超）: ${bad}件`);
  for (const v of seen.values()) console.log(v);
  process.exit(bad ? 1 : 0);
})();
