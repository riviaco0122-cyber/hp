#!/usr/bin/env node
/*
 * 改行の見本の点検（回帰テスト）。人が「この改行で良い」と確かめた文が、あとの改修で崩れていないかを確かめる。
 *
 * 見本は tools/check/linebreak_samples.json に書く（ページ・要素・幅ごとの「各行の文字」）。
 *   status: "approved" … 人が見て良いと言った形（お手本・指摘を直して人が確認した所）。崩れたら NG（直すまでマージしない）
 *           "baseline" … 指摘を受けて直した所の、いまの形（人の確認待ち）。変わったら「変化」として出す（意図した変化か、人に見せる）
 *
 * 使い方:
 *   node tools/check/linebreak_samples.js                 # 全見本を点検（NG があれば終了コード 1）
 *   node tools/check/linebreak_samples.js --only top      # id に top を含む見本だけ
 *   node tools/check/linebreak_samples.js --shots <フォルダ>  # 見本の要素のスクリーンショットも撮る（人に見せる用。deviceScaleFactor 2）
 *   node tools/check/linebreak_samples.js --update <id>   # その見本の期待値を、いまの形で書き換える（人が「これで良い」と言ったときだけ）
 *   見本を足すときは、json に expect の幅を空の配列（"390": []）で書いて実行すると、いまの形が記録される
 *   node tools/check/linebreak_samples.js --add <ページ> <CSSセレクタ> [<含む文字>]  # いまの形を表示する（見本に足す前の確認用）
 *
 * 実際の見た目に合わせるため、Google Fonts（Noto Sans JP など）を読み込み、document.fonts.ready を待ってから測る。
 * フォントが読み込めなかったときは、改行位置が実際と違うので、結果を信用しない（「フォント未読込」と出す）。
 */
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const fs = require('fs'), path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const FILE = path.join(__dirname, 'linebreak_samples.json');
const argv = process.argv.slice(2);
const opt = k => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : null; };

function pageFile(page) { // 公開URL風の名前（index.html・media/xxx.html）→ pages/ のファイル
  return path.join(ROOT, 'pages', page);
}

// 要素の中の文字を、表示されている行ごとに分ける（<br> の前後も別の行）
async function measure(p, sel, contains) {
  return p.evaluate(([sel, contains]) => {
    const els = [...document.querySelectorAll(sel)].filter(el => {
      const cs = getComputedStyle(el);
      return el.offsetParent !== null && cs.display !== 'none' && cs.visibility !== 'hidden' && (!contains || el.textContent.replace(/\s+/g, '').includes(contains));
    });
    if (!els.length) return { error: '要素が見つからない' };
    const el = els[0], r = document.createRange(), lines = [];
    const fs = parseFloat(getComputedStyle(el).fontSize);
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    let t;
    while ((t = tw.nextNode())) {
      for (let i = 0; i < t.length; i++) {
        const c = t.data[i];
        if (/\s/.test(c)) { if (lines.length) lines[lines.length - 1].sp = true; continue; } // 英単語の間の空白（「NODE Shimoda」）は1つにまとめて残す
        r.setStart(t, i); r.setEnd(t, i + 1);
        const rc = r.getClientRects()[0]; if (!rc || !rc.width) continue;
        const last = lines[lines.length - 1];
        if (!last || rc.top > last.top + fs * 0.6) lines.push({ top: rc.top, s: c });
        else { last.s += (last.sp ? ' ' : '') + c; }
        lines[lines.length - 1].sp = false;
      }
    }
    return { lines: lines.map(l => l.s), font: getComputedStyle(el).fontFamily.split(',')[0].replace(/"/g, '') };
  }, [sel, contains || '']);
}

async function open(browser, width, page) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: argv.includes('--shots') ? 2 : 1 });
  const p = await ctx.newPage();
  await p.goto('file://' + pageFile(page) + '?preview=1');
  await p.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important;transition:none!important}' });
  const fontsOk = await p.evaluate(async () => {
    await document.fonts.ready;
    return [...document.fonts].some(f => /Noto (Sans|Serif) JP/.test(f.family) && f.status === 'loaded');
  });
  await p.waitForTimeout(400); // js/main.js の改行の調整（fonts.ready のあと）を待つ
  return { ctx, p, fontsOk };
}

(async () => {
  const data = JSON.parse(fs.readFileSync(FILE, 'utf8'));
  const browser = await chromium.launch();

  if (argv[0] === '--add') {
    const [, page, sel, contains] = argv;
    for (const w of [375, 390, 430]) {
      const { ctx, p, fontsOk } = await open(browser, w, page);
      const m = await measure(p, sel, contains);
      console.log(`${w}px${fontsOk ? '' : '（フォント未読込）'}: ` + (m.error || JSON.stringify(m.lines)));
      await ctx.close();
    }
    return browser.close();
  }

  const only = opt('--only'), update = opt('--update'), shots = opt('--shots');
  if (shots) fs.mkdirSync(shots, { recursive: true });
  let ng = 0, changed = 0, nofont = 0, wrote = false;
  const out = [];
  for (const s of data.samples) {
    if (only && !s.id.includes(only)) continue;
    if (update && s.id !== update) continue;
    for (const [w, expect] of Object.entries(s.expect)) {
      const { ctx, p, fontsOk } = await open(browser, +w, s.page);
      const m = await measure(p, s.selector, s.contains);
      if (shots && !m.error) {
        const el = await p.$$(s.selector);
        for (const h of el) {
          if (s.contains && !(await h.textContent()).replace(/\s+/g, '').includes(s.contains)) continue;
          if (!(await h.isVisible())) continue;
          await h.screenshot({ path: path.join(shots, `${s.id}-${w}.png`) });
          break;
        }
      }
      await ctx.close();
      if (!fontsOk) nofont++;
      const got = m.lines || [];
      if (update || (!expect.length && !m.error)) { // 期待値が空の見本は、いまの形を記録する（足したばかりの見本）
        s.expect[w] = got; wrote = true; out.push(`${update ? '更新' : '新規'} ${s.id} ${w}px: ${got.join(' ／ ')}`); continue;
      }
      const same = !m.error && JSON.stringify(got) === JSON.stringify(expect);
      if (same) { out.push(`OK   ${s.id} ${w}px`); continue; }
      const label = s.status === 'approved' ? 'NG  ' : '変化';
      if (s.status === 'approved') ng++; else changed++;
      out.push(`${label} ${s.id} ${w}px${fontsOk ? '' : '（フォント未読込。結果は参考）'}  ${s.note || ''}\n     期待: ${expect.join(' ／ ')}\n     実際: ${m.error || got.join(' ／ ')}`);
    }
  }
  await browser.close();
  if (wrote) fs.writeFileSync(FILE, JSON.stringify(data, null, 2) + '\n');
  console.log(out.join('\n'));
  console.log(`\n改行の見本: NG ${ng}（人が確認済みの形が崩れた）・変化 ${changed}（確認待ちの形が変わった）` + (nofont ? `・フォント未読込 ${nofont}` : ''));
  process.exit(ng ? 1 : 0);
})();
