// 記事ページをスマホ幅(390px)で開き、「文章だけが続く高さ」（図・表・カード・注意枠・折りたたみなどで区切られない連続）を測る。
// 使い方: node tools/check/text_runs.js [--min 1400] [--out ファイル]   （約 3 分）
// 文章だけが 1400px（スマホ約 2 画面）以上続く節は、図解・表・カードで区切る（playbook 2-1）。
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const root = path.resolve(__dirname, '..', '..');
const args = process.argv.slice(2);
const mi = args.indexOf('--min');
const min = mi >= 0 ? Number(args[mi + 1]) : 1400;
const outIdx = args.indexOf('--out');
(async () => {
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await (await b.newContext({ viewport: { width: 390, height: 900 } })).newPage();
  const dir = path.join(root, 'pages', 'media');
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  const rows = [];
  for (const f of files) {
    await p.goto('file://' + path.join(dir, f) + '?preview=1');
    await p.waitForTimeout(250);
    const r = await p.evaluate(() => {
      const body = document.querySelector('.article__body');
      if (!body) return null;
      const isBreak = el => el.matches('figure,table,.table-scroll,.callout,.carousel,.compare,.stats,details,blockquote,h2,.fig,.keypoints,.article-cta,.faq,ol.steps,.calc,.table-note') || el.querySelector(':scope > figure, :scope > .table-scroll, :scope > .carousel');
      let run = 0, best = 0, bestAt = '', cur = '';
      const kids = [...body.querySelectorAll('.article__section > *')];
      for (const el of kids) {
        const h = el.getBoundingClientRect().height;
        if (el.tagName === 'H2') { cur = el.textContent.trim().slice(0, 24); run = 0; continue; }
        if (isBreak(el)) { run = 0; continue; }
        run += h;
        if (run > best) { best = run; bestAt = cur; }
      }
      return { best: Math.round(best), at: bestAt };
    });
    if (r) rows.push({ slug: f.replace('.html', ''), ...r });
  }
  await b.close();
  rows.sort((a, b) => b.best - a.best);
  const hit = rows.filter(r => r.best >= min);
  const lines = ['# 文章だけが続く高さ（スマホ390px）', '', `基準: ${min}px 以上を要対応（${hit.length} / ${rows.length} 本）`, '', '| 記事 | 連続の高さ(px) | 節の見出し |', '|---|---|---|', ...rows.map(r => `| ${r.slug} | ${r.best}${r.best >= min ? ' ⚠' : ''} | ${r.at} |`)];
  const text = lines.join('\n');
  if (outIdx >= 0) fs.writeFileSync(args[outIdx + 1], text + '\n'); else console.log(text);
})();
