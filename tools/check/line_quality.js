// 改行の質の点検：全ページをスマホ幅で開き、次を数える（人の指摘 2026-11-07。docs/design-guide.md 3章）
//   はみ出し       … 文字が、その文字が並ぶ枠（段落・項目・見出し）の右端より外に出ている
//   語の途中の改行 … 見出し・カード・項目など、言葉の切れ目で折る文（n-w.h / n-w.c / .wrap-fill）で、
//                    漢字どうし（「魅／力」）・ひらがなどうし（「か／ら」）・カタカナどうし（「ス／カウト」）・英数字どうし・
//                    漢字と送り仮名（「働／く」）の間で折れている（ふつうの本文の段落は、どこで折れてもよいので数えない）
//   開きかっこ     … 「「」『（ などが行末に残っている
// 使い方: node tools/check/line_quality.js [--widths 360,375,390,414] [--only ページ名の一部,...] [--out ファイル]
// 終了コード: はみ出し・開きかっこが1件でもあれば 1（語の途中の改行は件数を出すだけ）
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
  const cls = c => c === '・' ? 'P' : /[一-鿿㐀-䶿々〆ヵヶ]/.test(c) ? 'K' : /[ぁ-ゟ]/.test(c) ? 'H' : /[゠-ヿ]/.test(c) ? 'T' : /[A-Za-z0-9]/.test(c) ? 'L' : 'P';
  const PARTICLE = /^(?:から|まで|より|など|への|での|との|には|では|とは|を|が|は|へ|の|で|と|も|や|に)/;
  const blockOf = el => { while (el.parentElement && getComputedStyle(el).display === 'inline') el = el.parentElement; return el; };
  const hidden = el => !!el.closest('.visually-hidden, [aria-hidden="true"], svg, script, style, noscript'); // 飾り・読み上げ用の文字は対象外
  const out = { over: [], mid: [], open: [] };
  const tw = document.createTreeWalker(document.querySelector('main') || document.body, NodeFilter.SHOW_TEXT);
  const items = []; let t;
  const rng = document.createRange();
  while ((t = tw.nextNode())) {
    const pe = t.parentElement; if (!pe || hidden(pe)) continue;
    const blk = blockOf(pe);
    if (blk.clientWidth <= 2 || getComputedStyle(blk).writingMode.startsWith('vertical') || getComputedStyle(blk).textOverflow === 'ellipsis') continue; // 見えない（1px に切り抜いた）文字・縦書き
    for (let i = 0; i < t.data.length; i++) {
      const c = t.data[i]; if (/\s/.test(c)) { if (items.length) items[items.length - 1].sp = true; continue; }
      rng.setStart(t, i); rng.setEnd(t, i + 1);
      const r = rng.getClientRects()[0]; if (!r || !r.width) continue;
      items.push({ c, r, blk, managed: !!(pe.closest('n-w.h, n-w.c') || blk.classList.contains('wrap-fill')), node: t, i });
    }
  }
  const planned = (x, y) => { // x と y の文字の間に <wbr> がある（文節の切れ目として折った）
    const r = document.createRange(); r.setStart(x.node, x.i + 1); r.setEnd(y.node, y.i);
    return !!r.cloneContents().querySelector('wbr, br');
  };
  const desc = el => el.tagName.toLowerCase() + (el.classList.length ? '.' + [...el.classList].join('.') : '');
  const ctx = k => items.slice(Math.max(0, k - 8), k + 8).map(x => x.c).join('') + '\t' + desc(items[k].blk);
  const seenOver = new Set();
  items.forEach((it, k) => {
    // はみ出し：枠（の内側）の右端より外。横にスクロールする枠の中は、枠の見えている範囲ではなく枠の中身の幅で見る
    const bs = getComputedStyle(it.blk), br = it.blk.getBoundingClientRect();
    const right = br.left + it.blk.clientWidth + parseFloat(bs.borderLeftWidth) - parseFloat(bs.paddingRight);
    if (it.r.right > right + 2 && !seenOver.has(it.blk) && bs.textOverflow !== 'ellipsis') { seenOver.add(it.blk); out.over.push(ctx(k)); }
    const nx = items[k + 1];
    if (!nx || nx.blk !== it.blk || nx.r.top < it.r.bottom - 2) return; // 同じ枠の次の行の頭だけを見る
    if (/[「『（(【〈《［]/.test(it.c)) out.open.push(ctx(k));
    if (!it.managed || !nx.managed) return;
    const a = cls(it.c), b = cls(nx.c);
    const prev2 = (items[k - 1] ? items[k - 1].c : '') + it.c;
    let bad = a !== 'P' && a === b && !(a === 'H' && (/[をがは]/.test(it.c) || /^(?:たり|ので|から|けど|ても|って|まで|より|など|には|では|とは)$/.test(prev2) || (/[ごお]/.test(nx.c) && items[k + 2] && cls(items[k + 2].c) === 'K'))); // 「状態を／つくります」「したり／しまったり」は良い
    if (a === 'K' && b === 'H') { // 漢字のあとのひらがな：助詞（「職種／を」）なら、2文字以上の漢字の語のあとだけ良い
      let n = 0, j = k; for (; j >= 0 && cls(items[j].c) === 'K'; j--) n++;
      bad = !(PARTICLE.test(nx.c + (items[k + 2] ? items[k + 2].c : '')) && (n >= 2 || (j >= 0 && /[0-9]/.test(items[j].c))));
    }
    if ((a === 'T' || a === 'L') && b === 'H') bad = !PARTICLE.test(nx.c + (items[k + 2] ? items[k + 2].c : ''));
    if (bad && a !== 'L' && planned(it, nx)) bad = false; // 文節の切れ目（<wbr>）での「お願いする／ことは」「24時間／体制」は良い（BudouX の誤りは build の _NO_SPLIT へ）
    if (it.sp) bad = false; // 空白のところ（「Grand Maison」）
    if (bad) out.mid.push(ctx(k).replace(/(.{9})/, '$1／'));
  });
  return out;
}

(async () => {
  const browser = await chromium.launch();
  const rows = [], sum = { over: 0, mid: 0, open: 0 };
  for (const w of WIDTHS) {
    const page = await browser.newPage({ viewport: { width: w, height: 800 } });
    for (const f of files) {
      await page.goto('file://' + path.join(ROOT, f));
      await page.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important}' });
      await page.waitForTimeout(300);
      const r = await page.evaluate(inspect);
      for (const k of Object.keys(sum)) { sum[k] += r[k].length; r[k].forEach(x => rows.push(`${w}\t${k}\t${f.replace('pages/', '')}\t${x}`)); }
    }
    await page.close();
  }
  await browser.close();
  const head = `改行の質（幅 ${WIDTHS.join('・')}px）: はみ出し ${sum.over}件 ／ 開きかっこが行末 ${sum.open}件 ／ 語の途中の改行 ${sum.mid}件`;
  const text = [head, ...rows].join('\n') + '\n';
  if (OUT) { fs.writeFileSync(OUT, text); console.log(head); } else process.stdout.write(text);
  process.exit(sum.over || sum.open ? 1 : 0);
})();
