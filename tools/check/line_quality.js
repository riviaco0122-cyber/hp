// 改行の質の点検：全ページをスマホ幅で開き、次を数える（人の方針 2026-11-13。docs/design-guide.md 3章）
//   はみ出し       … 文字が、その文字が並ぶ枠（段落・項目・見出し）の右端より外に出ている
//   開きかっこ     … 「「」『（ などが行末に残っている
//   （短い最後の行が続けて起きていないかは、tools/check/short_lines.js が数える。js/main.js と同じ決め方にするため、ここでは数えない）
// 改行は全部ブラウザに任せて右まで詰める方針なので、語の途中の改行は数えない。
// 使い方: node tools/check/line_quality.js [--widths 360,375,390,414] [--only ページ名の一部,...] [--out ファイル]
// 終了コード: どれか1件でもあれば 1
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const WIDTHS = arg('--widths', '360,375,390,414').split(',').map(Number);
const ONLY = (arg('--only', '') || '').split(',').filter(Boolean), OUT = arg('--out', '');
const ROOT = path.resolve(__dirname, '..', '..');
const files = [
  ...fs.readdirSync(path.join(ROOT, 'pages')).filter(f => f.endsWith('.html')).map(f => 'pages/' + f),
  ...fs.readdirSync(path.join(ROOT, 'pages/media')).filter(f => f.endsWith('.html')).map(f => 'pages/media/' + f),
].filter(f => !ONLY.length || ONLY.some(o => f.includes(o)));

function inspect() {
  const blockOf = el => { while (el.parentElement && getComputedStyle(el).display === 'inline') el = el.parentElement; return el; };
  const hidden = el => !!el.closest('.visually-hidden, [aria-hidden="true"], svg, script, style, noscript'); // 飾り・読み上げ用の文字は対象外
  const out = { over: [], open: [] };
  const tw = document.createTreeWalker(document.querySelector('main') || document.body, NodeFilter.SHOW_TEXT);
  const items = []; let t;
  const rng = document.createRange();
  while ((t = tw.nextNode())) {
    const pe = t.parentElement; if (!pe || hidden(pe)) continue;
    const blk = blockOf(pe);
    const bcs = getComputedStyle(blk);
    if (blk.clientWidth <= 2 || bcs.writingMode.startsWith('vertical') || bcs.textOverflow === 'ellipsis') continue; // 見えない（1px に切り抜いた）文字・縦書き・省略表示
    for (let i = 0; i < t.data.length; i++) {
      const c = t.data[i]; if (/\s/.test(c)) continue;
      rng.setStart(t, i); rng.setEnd(t, i + 1);
      const r = rng.getClientRects()[0]; if (!r || !r.width) continue;
      items.push({ c, r, blk });
    }
  }
  const desc = el => el.tagName.toLowerCase() + (el.classList.length ? '.' + [...el.classList].join('.') : '');
  const ctx = k => items.slice(Math.max(0, k - 8), k + 8).map(x => x.c).join('') + '\t' + desc(items[k].blk);
  const seenOver = new Set(), lines = new Map(); // 枠 → [行ごとの文字数]
  items.forEach((it, k) => {
    // はみ出し：枠（の内側）の右端より外
    const bs = getComputedStyle(it.blk), br = it.blk.getBoundingClientRect();
    const right = br.left + it.blk.clientWidth + parseFloat(bs.borderLeftWidth) - parseFloat(bs.paddingRight);
    if (it.r.right > right + 2 && !seenOver.has(it.blk)) { seenOver.add(it.blk); out.over.push(ctx(k)); }
    const ls = lines.get(it.blk) || []; lines.set(it.blk, ls);
    const pv = items[k - 1];
    if (!pv || pv.blk !== it.blk || it.r.top >= pv.r.bottom - 2) ls.push(0);
    ls[ls.length - 1]++;
    const nx = items[k + 1];
    if (nx && nx.blk === it.blk && nx.r.top >= it.r.bottom - 2 && /[「『（(【〈《［]/.test(it.c)) out.open.push(ctx(k));
  });
  return out;
}

(async () => {
  const browser = await chromium.launch();
  const rows = [], sum = { over: 0, open: 0 };
  for (const w of WIDTHS) {
    const page = await browser.newPage({ viewport: { width: w, height: 800 } });
    for (const f of files) {
      await page.goto('file://' + path.join(ROOT, f));
      await page.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important}' });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(300);
      const r = await page.evaluate(inspect);
      for (const k of Object.keys(sum)) { sum[k] += r[k].length; r[k].forEach(x => rows.push(`${w}\t${k}\t${f.replace('pages/', '')}\t${x}`)); }
    }
    await page.close();
  }
  await browser.close();
  const head = `改行の質（幅 ${WIDTHS.join('・')}px）: はみ出し ${sum.over}件 ／ 開きかっこが行末 ${sum.open}件`;
  const text = [head, ...rows].join('\n') + '\n';
  if (OUT) { fs.writeFileSync(OUT, text); console.log(head); } else process.stdout.write(text);
  process.exit(sum.over || sum.open ? 1 : 0);
})();
