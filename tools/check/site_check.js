#!/usr/bin/env node
/*
 * サイト全体のバグ点検（表示・動作）。記事を足したり build.py を直したりしたあとに、HP 全体が壊れていないかを確かめる。
 *
 * 使い方:
 *   node tools/check/site_check.js                  # 全ページの点検＋見た目の回帰テスト（本番ブランチと比較）
 *   node tools/check/site_check.js --no-visual      # 見た目の比較を省く（早い）
 *   node tools/check/site_check.js --visual-only    # 見た目の比較だけ
 *   node tools/check/site_check.js --out report.md  # 結果の Markdown をファイルにも書く
 *   オプション: --root <フォルダ>（点検するサイトの直下。既定はこのリポジトリ）  --only <URLの一部>  --widths 390,1280  --date YYYY-MM-DD（予約公開の判定に使う「今日」。既定は日本時間の今日）
 *              --tmp <一時フォルダ>（スクリーンショット・差分画像・本番ブランチの作業フォルダ。既定は OS の一時フォルダ）
 *              --base <ブランチ名>（比較の基準。既定は GitHub のデフォルトブランチ＝本番ブランチ）
 *              --diff-threshold 0.01（これより差分の割合が大きいページを一覧にする）  --concurrency 4  --allow-external  --json
 *
 * やること:
 *   - vercel.json の redirects・rewrites を再現するローカルサーバーを立て、公開と同じ URL で開く
 *     （/ → pages/index.html、/xxx.html → pages/xxx.html、/media/xxx.html → pages/media/xxx.html、/robots.txt 等 → seo/、
 *       それ以外はリポジトリ直下のファイル、見つからなければ 404.html を 404 で返す）
 *   - sitemap.xml の全 URL と pages/ 以下の全 HTML（noindex も）、存在しない URL（404 ページ）を、幅 390px と 1280px で開く
 *   - 重大: JS のエラー（pageerror・console.error）、内部のリソースの読み込み失敗（4xx/5xx）、内部リンク切れ、
 *           表示されない画像（naturalWidth 0）、横はみ出し（scrollWidth > 画面幅）、ヘッダー・フッター・h1 がない、ページ自体が開けない
 *   - 警告: 予約公開の記事が公開日前に一覧・ガイド・よくある悩みなどに見えている、公開日前の記事ページが一覧へ戻らない、
 *           ページ内リンク（#）の飛び先がない、転送（リダイレクト）される URL へのリンク、スマホのメニューが開かない、
 *           フェードイン（.reveal）が表示されないまま、読み込みが遅い、スマホで画像が重い、
 *           見た目の崩れ（スマホ幅のみ。図・カード・囲み枠の中身が左端／右端から 10px/6px 未満でくっついている、文字が枠や画面からはみ出している、
 *           図の中の要素の重なり）。警告が出たら css/style.css・tools/figures.py・記事データを直して 0 にする（機械では見つからない崩れは、スクリーンショットを自分の目で見る）
 *   - 参考: 外部ドメイン（Google Fonts・計測タグなど）への通信。ネットワーク制限で失敗しうるので重大に数えない（既定では遮断して速くする）
 *   - 見た目の回帰テスト: 本番ブランチを git worktree で一時フォルダに出し、主要ページのスクリーンショットを両方で撮って
 *     tools/check/img_diff.py（Pillow）で比べ、差分の割合が大きいページを一覧にする（意図した変更かを人と品質管理部が確認する）
 *
 * 終了コード: 重大な問題が 1 件でもあれば 1、なければ 0（警告・見た目の差分だけなら 0）。
 * 予約公開: 公開日前の記事ページは、その記事の公開日の時計にして中身を点検し、別に「今日」の時計で一覧へ戻ることを確かめる。
 */
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const os = require('os');
const { execFileSync, spawnSync } = require('child_process');

let playwright;
try { playwright = require('playwright'); } catch (e) { playwright = require('/opt/node22/lib/node_modules/playwright'); }

const REPO = path.resolve(__dirname, '..', '..');
const SITE = 'https://rivia-co.com';

// ---------------------------------------------------------------- オプション
function parseArgs(argv) {
  const o = { root: REPO, widths: [390, 1280], only: '', out: '', date: '', visual: true, tmp: '', base: '', diffThreshold: 0.01,
              concurrency: 4, allowExternal: false, json: false, slowMs: 5000, heavyMobileKB: 3000 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i], v = () => argv[++i];
    if (a === '--root') o.root = path.resolve(v());
    else if (a === '--widths') o.widths = v().split(',').map(Number);
    else if (a === '--only') o.only = v();
    else if (a === '--out') o.out = v();
    else if (a === '--date') o.date = v();
    else if (a === '--no-visual') o.visual = false;
    else if (a === '--visual-only') o.visualOnly = true;
    else if (a === '--tmp') o.tmp = v();
    else if (a === '--base') o.base = v();
    else if (a === '--diff-threshold') o.diffThreshold = Number(v());
    else if (a === '--concurrency') o.concurrency = Number(v());
    else if (a === '--allow-external') o.allowExternal = true;
    else if (a === '--json') o.json = true;
    else if (a === '-h' || a === '--help') { console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0]); process.exit(0); }
    else { console.error('不明なオプション: ' + a); process.exit(2); }
  }
  return o;
}

function todayJST() { return new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10); }

// ---------------------------------------------------------------- vercel.json を再現するローカルサーバー
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2', '.pdf': 'application/pdf', '.mp4': 'video/mp4' };

function compileRule(src) {
  const names = [];
  const re = '^' + src.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/:(\w+)/g, (_, n) => { names.push(n); return '([^/]+)'; }) + '$';
  return { re: new RegExp(re), names };
}
function applyRule(rule, dest, p) {
  const m = rule.re.exec(p);
  if (!m) return null;
  const vals = {};
  rule.names.forEach((n, i) => { vals[n] = m[i + 1]; });
  return dest.replace(/:(\w+)/g, (_, n) => (n in vals ? vals[n] : ':' + n));
}

function makeRouter(root) {
  let conf = {};
  try { conf = JSON.parse(fs.readFileSync(path.join(root, 'vercel.json'), 'utf8')); } catch (e) { /* vercel.json がなければ素のファイル配信 */ }
  const redirects = (conf.redirects || []).map(r => ({ rule: compileRule(r.source), dest: r.destination, code: r.permanent === false ? 307 : 308 }));
  const rewrites = (conf.rewrites || []).map(r => ({ rule: compileRule(r.source), dest: r.destination }));
  const fileAt = p => {
    const f = path.join(root, decodeURIComponent(p));
    if (!f.startsWith(root)) return null;
    try { return fs.statSync(f).isFile() ? f : null; } catch (e) { return null; }
  };
  // 公開URLのパス → { redirect } または { file } または { notFound }
  return function route(p) {
    for (const r of redirects) {
      const d = applyRule(r.rule, r.dest, p);
      if (d !== null) return { redirect: d, code: r.code };
    }
    const direct = fileAt(p);
    if (direct) return { file: direct };
    for (const r of rewrites) {
      const d = applyRule(r.rule, r.dest, p);
      if (d !== null) {
        const f = fileAt(d);
        return f ? { file: f } : { notFound: true };
      }
    }
    return { notFound: true };
  };
}

function startServer(root) {
  const route = makeRouter(root);
  const server = http.createServer((req, res) => {
    const u = new URL(req.url, 'http://x');
    const r = route(u.pathname);
    if (r.redirect) {
      res.writeHead(r.code, { Location: r.redirect + (u.search || '') });
      return res.end();
    }
    let file = r.file, status = 200;
    if (!file) { file = path.join(root, '404.html'); status = 404; if (!fs.existsSync(file)) { res.writeHead(404); return res.end('not found'); } }
    const body = fs.readFileSync(file);
    res.writeHead(status, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream', 'Content-Length': body.length,
      'Cache-Control': 'no-store' });
    res.end(req.method === 'HEAD' ? undefined : body);
  });
  return new Promise(resolve => server.listen(0, '127.0.0.1', () => {
    resolve({ server, route, origin: `http://127.0.0.1:${server.address().port}`, root });
  }));
}

function fetchRaw(url) {
  return new Promise(resolve => {
    http.get(url, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, location: res.headers.location, body: Buffer.concat(chunks).toString('utf8'),
        type: res.headers['content-type'] || '' }));
    }).on('error', e => resolve({ status: 0, error: e.message, body: '' }));
  });
}
// 転送をたどって最終的な状態を返す
async function fetchFollow(url) {
  let cur = url, redirected = null;
  for (let i = 0; i < 6; i++) {
    const r = await fetchRaw(cur);
    if (r.status >= 300 && r.status < 400 && r.location) {
      redirected = redirected || new URL(r.location, cur).pathname;
      cur = new URL(r.location, cur).href;
      continue;
    }
    return Object.assign(r, { redirected, final: cur });
  }
  return { status: 0, error: '転送が多すぎる', redirected, final: cur, body: '' };
}

// ---------------------------------------------------------------- 点検するページ
function pageList(root, only) {
  const set = new Set();
  const sm = path.join(root, 'seo', 'sitemap.xml');
  if (fs.existsSync(sm)) {
    for (const m of fs.readFileSync(sm, 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)) set.add(new URL(m[1].trim()).pathname);
  }
  const walk = d => fs.readdirSync(d, { withFileTypes: true }).forEach(e => {
    const f = path.join(d, e.name);
    if (e.isDirectory()) walk(f);
    else if (e.name.endsWith('.html')) {
      const rel = path.relative(path.join(root, 'pages'), f).split(path.sep).join('/');
      set.add(rel === 'index.html' ? '/' : '/' + rel);
    }
  });
  if (fs.existsSync(path.join(root, 'pages'))) walk(path.join(root, 'pages'));
  set.add('/__site_check_no_such_page__.html'); // 404 ページの表示
  if (set.has('/media/search.html')) set.add('/media/search.html?q=' + encodeURIComponent('民泊')); // 記事検索の結果
  return [...set].filter(p => !only || p.includes(only)).sort();
}

function publishDateOf(router, p) {
  const r = router(p.split('?')[0].split('#')[0]);
  if (!r.file || !r.file.endsWith('.html')) return null;
  const m = /<article[^>]*data-publish="(\d{4}-\d{2}-\d{2})"/.exec(fs.readFileSync(r.file, 'utf8'));
  return m ? m[1] : null;
}

// ---------------------------------------------------------------- ページの準備（遅延読み込みの解除・フェードイン・スクロール）
async function prepare(page, { reveal = false } = {}) {
  await page.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}' });
  await page.evaluate(async (reveal) => {
    document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; });
    if (reveal) document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-visible'));
    const step = Math.max(400, Math.floor(innerHeight * 0.9));
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 40));
    }
    window.scrollTo(0, document.documentElement.scrollHeight);
    await new Promise(r => setTimeout(r, 120));
    window.scrollTo(0, 0);
    const imgs = [...document.images];
    await Promise.race([
      Promise.all(imgs.map(i => (i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))),
      new Promise(r => setTimeout(r, 10000)),
    ]);
    await Promise.all(imgs.map(i => (i.decode ? i.decode().catch(() => 0) : 0)));
  }, reveal);
  if (reveal) {
    // スクリーンショット用: main.js の行末の調整（letter-spacing・文末の n-b）は、フォントの準備ができた時点と画面幅が変わった時点で
    // やり直され、画面に近づいた段落から順に行われる。走るタイミングで結果が変わるため、表示を確定させてから
    // 画面幅を1px変えて戻し（調整のやり直し）、もう一度ゆっくりスクロールして全段落を調整させる
    const vp = page.viewportSize();
    await page.setViewportSize({ width: vp.width + 1, height: vp.height });
    await page.waitForTimeout(250);
    await page.setViewportSize(vp);
    await page.waitForTimeout(250);
    await page.evaluate(async () => {
      const step = Math.max(300, Math.floor(innerHeight * 0.6));
      for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 50));
      }
      window.scrollTo(0, 0);
    });
  }
  // DOM の変化（main.js の行末の調整など）が 400ms 止まるまで待つ（最大 5 秒）
  await page.evaluate(() => new Promise(resolve => {
    let t = setTimeout(done, 400);
    const mo = new MutationObserver(() => { clearTimeout(t); t = setTimeout(done, 400); });
    const cap = setTimeout(done, 5000);
    function done() { mo.disconnect(); clearTimeout(cap); resolve(); }
    mo.observe(document.body, { subtree: true, childList: true, attributes: true, characterData: true });
  }));
  await page.waitForTimeout(100);
}

// ページの中で調べる（document の状態）
function inspectInPage() {
  const W = window.innerWidth;
  const now = new Date();
  const today = now.getFullYear() + '-' + ('0' + (now.getMonth() + 1)).slice(-2) + '-' + ('0' + now.getDate()).slice(-2);
  const visible = e => {
    if (!e || e.closest('[hidden]')) return false;
    const s = getComputedStyle(e);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    return e.offsetParent !== null || s.position === 'fixed';
  };
  const desc = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const sw = document.documentElement.scrollWidth;
  const offenders = [];
  if (sw > W) {
    const clipped = e => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const ox = getComputedStyle(p).overflowX; if (ox !== 'visible') return true; } return false; };
    const over = new Set();
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > W + 1 && !clipped(el)) over.add(el);
    }
    for (const el of over) { if (!over.has(el.parentElement)) offenders.push(desc(el) + `（右端 ${Math.round(el.getBoundingClientRect().right)}px）`); if (offenders.length >= 5) break; }
  }
  const imgs = [...document.images].filter(i => (i.currentSrc || i.src) && !(i.currentSrc || i.src).startsWith('data:'));
  const broken = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc || i.src);
  const pending = imgs.filter(i => !i.complete).map(i => i.currentSrc || i.src);
  const ids = [...document.querySelectorAll('[id]')].map(e => e.id).concat([...document.querySelectorAll('a[name]')].map(e => e.getAttribute('name')));
  const links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
  const sel = '.media-card[data-date], .mq li[data-date], .lchap__list li[data-date], .guide-box__list li[data-date]';
  const futureVisible = [...document.querySelectorAll(sel)].filter(e => e.getAttribute('data-date') > today && visible(e))
    .map(e => (e.getAttribute('href') || (e.querySelector('a') && e.querySelector('a').getAttribute('href')) || desc(e)) + `（公開日 ${e.getAttribute('data-date')}）`);
  const guideFutureLinked = [...document.querySelectorAll('.guide-step[data-date]')].filter(li => li.getAttribute('data-date') > today && li.querySelector('a'))
    .map(li => li.querySelector('a').getAttribute('href'));
  const unrevealed = [...document.querySelectorAll('.reveal')].filter(e => !e.classList.contains('is-visible') && visible(e)).map(desc);
  const mediaList = document.querySelector('#media-list');
  // 一覧・関連記事・ガイド・よくある悩み・体系的に学ぶ・検索結果に見えている記事へのリンク（公開日はページの外で確かめる）
  const listSel = '.media-card, .mq li a, .lchap__list li a, .guide-box__list li a, .guide-step a, .msearch-weak__item';
  const listed = [...new Set([...document.querySelectorAll(listSel)].filter(visible).map(e => e.getAttribute('href')).filter(Boolean))];
  const sr = document.getElementById('search-results');
  return {
    title: document.title, listed, searchResults: sr ? sr.children.length : null, W, sw, offenders, broken, pending, ids, links, futureVisible, guideFutureLinked, unrevealed: unrevealed.slice(0, 3), unrevealedCount: unrevealed.length,
    header: !!document.querySelector('header.header'), footer: !!document.querySelector('footer.footer, footer.mfooter'),
    h1: [...document.querySelectorAll('h1')].length, h1Visible: [...document.querySelectorAll('h1')].some(visible),
    mediaListVisible: mediaList ? [...mediaList.querySelectorAll('.media-card')].filter(visible).length : null,
    menuBtn: (() => { const b = document.querySelector('.menu-btn, .mmenu-btn'); return b && visible(b) ? (b.classList.contains('menu-btn') ? '.menu-btn' : '.mmenu-btn') : null; })(),
    today,
  };
}


// スマホ幅の見た目の崩れ（図・カード・表の左端へのくっつき、枠からのはみ出し、要素の重なり）をページの中で機械的に探す
function layoutProbe() {
  const out = [];
  const W = window.innerWidth;
  const desc = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const shown = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && !e.closest('[hidden]'); };
  const alpha = c => { const m = /rgba?\(([^)]+)\)/.exec(c); if (!m) return 0; const v = m[1].split(',').map(Number); return v.length > 3 ? v[3] : 1; };
  const isCard = e => {
    const s = getComputedStyle(e);
    const pb = e.parentElement ? getComputedStyle(e.parentElement).backgroundColor : '';
    return (alpha(s.backgroundColor) > 0.05 && s.backgroundColor !== pb) || ['Left', 'Right'].some(k => parseFloat(s['border' + k + 'Width']) > 0 && s['border' + k + 'Style'] !== 'none') || (s.boxShadow && s.boxShadow !== 'none');
  };
  // 要素の中身（子孫の文字・画像）が実際に占める範囲
  const contentBox = e => {
    let l = Infinity, r = -Infinity, any = false;
    const add = b => { if (b.width > 0 && b.height > 0) { l = Math.min(l, b.left); r = Math.max(r, b.right); any = true; } };
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      if (!n.textContent.trim() || !n.parentElement || getComputedStyle(n.parentElement).position === 'absolute') continue;
      const rg = document.createRange(); rg.selectNodeContents(n); for (const b of rg.getClientRects()) add(b);
    }
    for (const im of e.querySelectorAll('img')) add(im.getBoundingClientRect());
    return any ? { l, r } : null;
  };
  const inScroller = e => { for (let p = e; p && p !== document.body; p = p.parentElement) { const ox = getComputedStyle(p).overflowX; if ((ox === 'auto' || ox === 'scroll') && p.scrollWidth > p.clientWidth) return true; } return false; };
  const area = document.querySelector('.article__body') || document.querySelector('main') || document.body;
  const seen = new Set();
  const push = (kind, e, msg) => { const k = kind + desc(e) + msg; if (!seen.has(k) && out.length < 12) { seen.add(k); out.push(`${kind}: ${desc(e)} ${msg}`); } };
  // 1) 枠・背景のある要素の中身が、左端（または右端）に 10px 未満でくっついている／枠からはみ出している
  for (const e of area.querySelectorAll('*')) {
    if (!shown(e) || e.closest('svg, figure.photo, .media-card, .toc, nav, summary, button, .btn')) continue;
    if (['IMG', 'SVG', 'PATH', 'A', 'SPAN', 'STRONG', 'B', 'EM', 'BR', 'TD', 'TH', 'TR'].includes(e.tagName)) continue;
    const r = e.getBoundingClientRect();
    if (r.width < 60 || r.height < 24 || r.width >= W - 2 || !isCard(e)) continue;
    const s = getComputedStyle(e);
    if (s.display === 'inline' || s.overflow !== 'visible') continue;
    const c = contentBox(e);
    if (!c) continue;
    const left = c.l - r.left, right = r.right - c.r;
    if (s.textAlign !== 'center' && left < 10) push('左端にくっつき', e, `中身が左端から ${left.toFixed(0)}px`);
    if (s.textAlign !== 'center' && right < 6 && c.r - c.l > r.width * 0.9 && (alpha(s.backgroundColor) > 0.05 || parseFloat(s.borderRightWidth) > 0 || (s.boxShadow && s.boxShadow !== 'none'))) push('右端にくっつき', e, `中身が右端から ${right.toFixed(0)}px`);
    if (c.r > r.right + 1 || c.l < r.left - 1) push('枠からはみ出し', e, `中身 ${Math.round(c.l)}〜${Math.round(c.r)}px が枠 ${Math.round(r.left)}〜${Math.round(r.right)}px の外`);
  }
  // 2) 文字が画面の外に出ている
  for (const e of area.querySelectorAll('p, li, h2, h3, h4, dt, dd, td, th, .fig *')) {
    if (!shown(e) || e.closest('svg, [hidden]') || inScroller(e)) continue;
    for (const n of e.childNodes) {
      if (n.nodeType !== 3 || !n.textContent.trim()) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      const b = rg.getBoundingClientRect();
      if (b.width > 0 && (b.right > W + 1 || b.left < -1)) { push('文字が画面外', e, `${Math.round(b.left)}〜${Math.round(b.right)}px（画面 ${W}px）`); break; }
    }
  }
  // 3) 図の中の兄弟要素どうしの重なり
  for (const par of area.querySelectorAll('.fig *')) {
    if (par.closest('svg')) continue;
    const kids = [...par.children].filter(k => shown(k) && !['absolute', 'fixed'].includes(getComputedStyle(k).position) && !/^(svg|br)$/i.test(k.tagName));
    for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) {
      const a = kids[i].getBoundingClientRect(), b = kids[j].getBoundingClientRect();
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 4 && oy > 4) push('重なり', par, `${desc(kids[i])} と ${desc(kids[j])}（${Math.round(ox)}×${Math.round(oy)}px）`);
    }
  }
  // 表の1列目が細く、文字が縦に長く伸びていないか（人の方針 2026-10-12。build.py の auto_stack_tables で自動でカード化されるが、漏れを拾う）
  for (const t of document.querySelectorAll('body.is-media .article__section table.table:not(.table--stack)')) {
    if (!shown(t)) continue;
    const rows = [...t.querySelectorAll('tbody tr')];
    if (!rows.length) continue;
    for (const tr of rows) {
      const c = tr.children[0];
      if (!c) continue;
      const r = c.getBoundingClientRect();
      const len = (c.textContent || '').trim().length;
      if (len > 10 && r.width < 110 && r.height > 120) { out.push(`表の1列目が細く縦に伸びている（${Math.round(r.width)}px・${Math.round(r.height)}px・「${(c.textContent || '').trim().slice(0, 14)}…」）。table--stack にして、スマホでカード表示にする`); break; }
    }
  }
  return out;
}

// ---------------------------------------------------------------- 1ページ×1画面幅の点検
async function checkPage(browser, srv, p, width, opts, report) {
  const isNotFound = p === '/__site_check_no_such_page__.html';
  const pub = publishDateOf(srv.route, p);
  const future = pub && pub > opts.today;
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, timezoneId: 'Asia/Tokyo', locale: 'ja-JP' });
  const page = await ctx.newPage();
  // 予約公開の記事は、その記事の公開日の時計で中身を点検する（今日の時計だと一覧へ戻るため）。ほかは --date の日付
  const clockDate = future ? pub : opts.date;
  if (clockDate) await page.clock.setFixedTime(new Date(clockDate + 'T10:00:00+09:00'));
  const host = new URL(srv.origin).host;
  let closing = false;
  const crit = (kind, msg) => report.add('crit', p, width, kind, msg);
  const warn = (kind, msg) => report.add('warn', p, width, kind, msg);
  await ctx.route('**/*', r => {
    const u = new URL(r.request().url());
    if (u.host === host || u.protocol === 'data:') return r.continue();
    report.external(u.host, opts.allowExternal ? 'allowed' : 'blocked');
    return opts.allowExternal ? r.continue() : r.abort('blockedbyclient');
  });
  page.on('pageerror', e => crit('JSエラー', String(e.message || e).split('\n')[0]));
  page.on('console', m => {
    if (m.type() !== 'error') return;
    const t = m.text();
    if (/Failed to load resource|ERR_BLOCKED_BY_CLIENT/.test(t)) return; // 読み込み失敗は response / requestfailed で数える
    crit('console.error', t.split('\n')[0].slice(0, 200));
  });
  let imageBytes = 0;
  page.on('response', async r => {
    const u = new URL(r.url());
    const internal = u.host === host;
    if (!internal) { if (r.status() >= 400) report.external(u.host, 'http ' + r.status()); return; }
    const isDoc = r.request().resourceType() === 'document' && r.request().frame() === page.mainFrame();
    if (r.status() >= 400 && !(isDoc && isNotFound && r.status() === 404) && !isDoc) crit('読み込み失敗', `${r.status()} ${r.request().resourceType()} ${u.pathname}`);
    if (r.request().resourceType() === 'image') { const len = Number(r.headers()['content-length'] || 0); imageBytes += len; }
  });
  page.on('requestfailed', r => {
    if (closing) return;
    const u = new URL(r.url());
    if (u.host !== host) return;
    // net::ERR_ABORTED はブラウザが自分で取りやめたもの（srcset の候補の切り替え・移動など）。本当の失敗は 4xx/5xx の応答で数える
    if (r.failure() && /ERR_ABORTED/.test(r.failure().errorText)) return;
    crit('読み込み失敗', `${r.failure() ? r.failure().errorText : 'failed'} ${r.resourceType()} ${u.pathname}`);
  });

  const t0 = Date.now();
  let resp;
  try {
    resp = await page.goto(srv.origin + p, { waitUntil: 'load', timeout: 30000 });
  } catch (e) {
    crit('開けない', String(e.message).split('\n')[0]);
    closing = true; await ctx.close(); return null;
  }
  const loadMs = Date.now() - t0;
  const status = resp ? resp.status() : 0;
  if (isNotFound ? status !== 404 : status !== 200) crit('開けない', `HTTP ${status}（想定 ${isNotFound ? 404 : 200}）`);
  if (loadMs > opts.slowMs) warn('遅い', `読み込みに ${(loadMs / 1000).toFixed(1)} 秒`);
  if (!isNotFound && new URL(page.url()).pathname !== p.split('?')[0]) warn('転送', `開くと ${new URL(page.url()).pathname} に移動した`);

  await prepare(page);
  const info = await page.evaluate(inspectInPage);
  if (width < 600) for (const m of await page.evaluate(layoutProbe)) warn('見た目の崩れ', m);
  if (info.sw > info.W) crit('横はみ出し', `ページの幅 ${info.sw}px > 画面 ${info.W}px` + (info.offenders.length ? '。はみ出している要素: ' + info.offenders.join('、') : ''));
  for (const s of info.broken) {
    const u = new URL(s, srv.origin);
    if (u.host === host) crit('画像が表示されない', u.pathname);
    else report.external(u.host, 'image');
  }
  for (const s of info.pending) { const u = new URL(s, srv.origin); if (u.host === host) warn('画像の読み込みが終わらない', u.pathname); }
  if (!info.header) crit('ヘッダーがない', 'header.header が見つからない');
  if (!info.footer) crit('フッターがない', 'footer.footer / footer.mfooter が見つからない');
  if (info.h1 === 0) crit('h1がない', 'h1 が見つからない');
  else if (!info.h1Visible) crit('h1がない', 'h1 が画面に表示されていない');
  for (const f of info.futureVisible) warn('予約公開', `公開日前（今日 ${info.today}）の記事が見えている: ${f}`);
  for (const f of info.guideFutureLinked) warn('予約公開', `ガイドの公開日前の記事がリンクのまま: ${f}`);
  for (const href of info.listed) {
    const u = new URL(href, srv.origin + p);
    if (u.host !== host) continue;
    const d = publishDateOf(srv.route, u.pathname);
    if (d && d > info.today) warn('予約公開', `公開日前（今日 ${info.today}）の記事へのリンクが一覧などに見えている: ${u.pathname}（公開日 ${d}）`);
  }
  if (info.searchResults === 0 && p.includes('?q=')) warn('検索', `記事検索の結果が0件（${decodeURIComponent(p.split('?q=')[1])}）`);
  if (info.mediaListVisible === 0) warn('予約公開', '「すべての記事」（#media-list）に公開済みの記事が1本も表示されていない');
  if (info.unrevealedCount) warn('フェードイン', `.reveal が表示されないまま ${info.unrevealedCount} 個（例: ${info.unrevealed.join('、')}）`);
  if (width < 600 && imageBytes / 1024 > opts.heavyMobileKB) warn('画像が重い', `スマホ幅で画像 ${(imageBytes / 1024 / 1024).toFixed(1)}MB を読み込んでいる`);

  // スマホのメニュー（ボタンを押すと開く）
  if (width < 900 && info.menuBtn) {
    try {
      await page.click(info.menuBtn, { timeout: 3000 });
      await page.waitForTimeout(250);
      const ok = await page.evaluate(sel => {
        const b = document.querySelector(sel);
        const nav = document.getElementById(b.getAttribute('aria-controls'));
        if (b.getAttribute('aria-expanded') !== 'true' || !nav) return false;
        const r = nav.getBoundingClientRect(), s = getComputedStyle(nav);
        return r.height > 0 && r.width > 0 && s.visibility !== 'hidden' && s.display !== 'none' && Number(s.opacity) > 0;
      }, info.menuBtn);
      if (!ok) warn('メニュー', `${info.menuBtn} を押してもメニューが開かない`);
    } catch (e) { warn('メニュー', `${info.menuBtn} を押せない: ${String(e.message).split('\n')[0]}`); }
  }
  closing = true;
  await ctx.close();
  return { p, width, info, loadMs };
}

// 公開日前の記事ページを「今日」の時計で開くと、一覧（media.html）へ戻ること（main.js の動作）
async function checkScheduledRedirect(browser, srv, p, opts, report) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 900 }, timezoneId: 'Asia/Tokyo', locale: 'ja-JP' });
  const page = await ctx.newPage();
  await page.clock.setFixedTime(new Date(opts.today + 'T10:00:00+09:00'));
  await ctx.route('**/*', r => (new URL(r.request().url()).host === new URL(srv.origin).host ? r.continue() : r.abort('blockedbyclient')));
  try {
    await page.goto(srv.origin + p, { waitUntil: 'load', timeout: 30000 });
    await page.waitForURL(u => new URL(u).pathname === '/media.html', { timeout: 5000 });
  } catch (e) {
    report.add('warn', p, 390, '予約公開', `公開日前（今日 ${opts.today}）に記事ページを開いても一覧へ戻らない（main.js）`);
  }
  await ctx.close();
}

// ---------------------------------------------------------------- 結果の集計
function makeReport() {
  const items = new Map();
  const ext = new Map();
  return {
    add(level, p, width, kind, msg) {
      const k = [level, p, kind, msg].join('\u0000');
      if (!items.has(k)) items.set(k, { level, page: p, kind, msg, widths: new Set() });
      items.get(k).widths.add(width);
    },
    external(host, how) {
      const k = host + ' ' + how;
      ext.set(k, (ext.get(k) || 0) + 1);
    },
    items: () => [...items.values()].map(i => Object.assign({}, i, { widths: [...i.widths].sort((a, b) => a - b) })),
    ext: () => [...ext.entries()].sort((a, b) => b[1] - a[1]),
  };
}

// 内部リンク・ページ内アンカーの確認（ページの DOM から集めたリンクを、ローカルサーバーで確かめる）
async function checkLinks(srv, results, report) {
  const host = new URL(srv.origin).host;
  const idsByPath = new Map();
  const linkSources = new Map(); // "path#hash" → Set(source page)
  for (const r of results) {
    if (!r) continue;
    if (!idsByPath.has(r.p)) idsByPath.set(r.p, new Set(r.info.ids));
    for (const href of r.info.links) {
      if (!href || /^(mailto:|tel:|javascript:|data:)/i.test(href)) continue;
      let u;
      try { u = new URL(href, srv.origin + r.p); } catch (e) { report.add('crit', r.p, r.width, 'リンク切れ', `URL として読めない: ${href}`); continue; }
      if (u.host !== host) continue;
      const key = u.pathname + (u.hash.length > 1 ? u.hash : '');
      if (!linkSources.has(key)) linkSources.set(key, new Set());
      linkSources.get(key).add(r.p);
    }
  }
  const status = new Map();
  for (const key of linkSources.keys()) {
    const pth = key.split('#')[0];
    if (!status.has(pth)) status.set(pth, await fetchFollow(srv.origin + pth));
  }
  for (const [key, srcs] of linkSources) {
    const [pth, hash] = key.split('#');
    const st = status.get(pth);
    const from = [...srcs];
    const where = from.slice(0, 3).join('、') + (from.length > 3 ? ` ほか${from.length - 3}ページ` : '');
    if (st.status !== 200) { for (const s of from) report.add('crit', s, 0, 'リンク切れ', `${pth}（HTTP ${st.status}）`); continue; }
    if (st.redirected) report.add('warn', from[0], 0, '転送されるリンク', `${pth} → ${st.redirected}（リンク元: ${where}）`);
    if (hash) {
      const target = st.redirected || pth;
      let ids = idsByPath.get(target);
      if (!ids) ids = new Set([...st.body.matchAll(/\s(?:id|name)="([^"]+)"/g)].map(m => m[1]));
      const id = decodeURIComponent(hash);
      if (!ids.has(id)) report.add('warn', from[0], 0, 'アンカー切れ', `${pth}#${hash} の飛び先（id="${id}"）がない（リンク元: ${where}）`);
    }
  }
}

// ---------------------------------------------------------------- 見た目の回帰テスト
const VISUAL_PAGES = ['/', '/media.html', '/service-operation.html', '/service-management.html', '/service-marketing.html',
  '/service-recruit.html', '/service-partnership.html', '/media/plans.html', '/media/service-kaitori.html', '/media/service-kariage.html',
  '/media/service-kaigyo.html', '/media/guide-sell.html', '/media/guide-use.html', '/media/guide-side.html', '/media/learn.html',
  '/media/category-house.html', '/media/category-operate.html', '/media/akiya-inherited-house-to-inn.html',
  '/media/minpaku-vs-rental-income.html', '/media/case-rental-house-inn-first-year.html'];

async function screenshots(browser, srv, pages, widths, date, dir, concurrency) {
  fs.mkdirSync(dir, { recursive: true });
  const host = new URL(srv.origin).host;
  const tasks = [];
  for (const p of pages) {
    const r = srv.route(p);
    if (!r.file) continue; // 本番ブランチにまだないページ
    const pub = publishDateOf(srv.route, p);
    for (const w of widths) tasks.push(async () => {
      const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, timezoneId: 'Asia/Tokyo', locale: 'ja-JP' });
      await ctx.route('**/*', rt => (new URL(rt.request().url()).host === host ? rt.continue() : rt.abort('blockedbyclient')));
      const page = await ctx.newPage();
      // 予約公開の記事は公開日の時計で撮る（どちらのブランチでも同じ時計にする）
      await page.clock.setFixedTime(new Date(((pub && pub > date) ? pub : date) + 'T10:00:00+09:00'));
      let name = null;
      try {
        await page.goto(srv.origin + p, { waitUntil: 'load', timeout: 30000 });
        await prepare(page, { reveal: true });
        name = (p === '/' ? 'index' : p.slice(1).replace(/\//g, '__').replace(/\.html$/, '')) + `@${w}.png`;
        await page.screenshot({ path: path.join(dir, name), fullPage: true });
      } catch (e) { name = null; /* 撮れなかったページは比較から外す */ }
      await ctx.close();
      return name;
    });
  }
  return (await pool(tasks, concurrency)).filter(Boolean);
}

function git(args, opts = {}) { return execFileSync('git', args, Object.assign({ cwd: REPO, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }, opts)).trim(); }

async function visualRegression(browser, cur, opts, notes) {
  let branch = opts.base;
  if (!branch) {
    try {
      const m = /ref: refs\/heads\/(\S+)\s+HEAD/.exec(git(['ls-remote', '--symref', 'origin', 'HEAD']));
      branch = m && m[1];
    } catch (e) { notes.push('本番ブランチを調べられなかった（git ls-remote --symref origin HEAD が失敗）: ' + String(e.message).split('\n')[0]); }
  }
  if (!branch) { notes.push('見た目の比較を省いた（本番ブランチが分からない。--base で指定できる）'); return null; }
  try { git(['fetch', '-q', 'origin', branch]); } catch (e) { notes.push(`git fetch origin ${branch} が失敗したため、手元の origin/${branch} で比べた`); }
  let ref = `origin/${branch}`;
  try { git(['rev-parse', '--verify', '-q', ref]); } catch (e) { ref = branch; }
  const work = path.join(opts.tmp, 'visual');
  const baseDir = path.join(work, 'base-worktree');
  fs.rmSync(work, { recursive: true, force: true });
  fs.mkdirSync(work, { recursive: true });
  try { git(['worktree', 'prune']); } catch (e) { /* なくてよい */ }
  try {
    git(['worktree', 'add', '-q', '--detach', baseDir, ref]);
  } catch (e) { notes.push('git worktree add が失敗したため、見た目の比較を省いた: ' + String(e.stderr || e.message).split('\n')[0]); return null; }
  const commit = git(['rev-parse', '--short', 'HEAD'], { cwd: baseDir });
  let base;
  try {
    base = await startServer(fs.realpathSync(baseDir));
    const shotsBase = path.join(work, 'base'), shotsCur = path.join(work, 'current'), diffs = path.join(work, 'diff');
    await screenshots(browser, base, VISUAL_PAGES, opts.widths, opts.date || opts.today, shotsBase, opts.concurrency);
    await screenshots(browser, cur, VISUAL_PAGES, opts.widths, opts.date || opts.today, shotsCur, opts.concurrency);
    const py = spawnSync('python3', [path.join(__dirname, 'img_diff.py'), shotsBase, shotsCur, diffs], { encoding: 'utf8' });
    if (py.status !== 0) { notes.push('img_diff.py が失敗した（pip install pillow が必要）: ' + (py.stderr || '').split('\n').slice(-2).join(' ')); return null; }
    return { branch, ref, commit, dir: work, rows: JSON.parse(py.stdout) };
  } finally {
    if (base) base.server.close();
    try { git(['worktree', 'remove', '--force', baseDir]); } catch (e) { notes.push('一時的な worktree を消せなかった: ' + baseDir); }
  }
}

// ---------------------------------------------------------------- 実行
async function pool(tasks, n) {
  const out = new Array(tasks.length);
  let i = 0;
  await Promise.all(Array.from({ length: Math.max(1, n) }, async () => {
    while (i < tasks.length) { const k = i++; out[k] = await tasks[k](); }
  }));
  return out;
}

function toMarkdown(o, pages, rep, visual, notes, secs) {
  const items = rep.items();
  const crit = items.filter(i => i.level === 'crit'), warn = items.filter(i => i.level === 'warn');
  const L = [];
  L.push('# サイト全体の点検結果（tools/check/site_check.js）', '');
  L.push(`- 対象: ${pages.length} ページ（sitemap.xml の全 URL と pages/ の全 HTML、404 ページ）× 画面幅 ${o.widths.join('px・')}px`);
  L.push(`- 予約公開の判定に使った「今日」: ${o.date || o.today}（日本時間）`);
  L.push(`- 所要時間: ${secs.toFixed(0)} 秒`);
  L.push('', `**重大 ${crit.length} 件 ／ 警告 ${warn.length} 件**`, '');
  const fmt = i => `- \`${i.page}\` ${i.widths.filter(Boolean).length ? '[' + i.widths.filter(Boolean).join('/') + ']' : ''} **${i.kind}**: ${i.msg}`;
  const sortI = a => a.sort((x, y) => (x.kind + x.page).localeCompare(y.kind + y.page));
  if (crit.length) { L.push('## 重大（直す。HTML ではなく tools/build.py・記事データ・css/js の元を直して作り直す）', ''); sortI(crit).forEach(i => L.push(fmt(i))); L.push(''); }
  if (warn.length) { L.push('## 警告（確認する）', ''); sortI(warn).forEach(i => L.push(fmt(i))); L.push(''); }
  const ext = rep.ext();
  if (ext.length) {
    L.push('## 参考: 外部ドメインへの通信（重大に数えない）', '');
    L.push(o.allowExternal ? '外部への通信を許可して点検した。' : '点検を速く安定させるため、外部への通信は遮断した（Google Fonts・GA4・Clarity など。本番では読み込まれる）。');
    ext.forEach(([k, n]) => L.push(`- ${k}: ${n} 回`));
    L.push('');
  }
  if (visual) {
    const rows = visual.rows.filter(r => r.ratio !== null).sort((a, b) => b.ratio - a.ratio);
    const big = rows.filter(r => r.ratio > o.diffThreshold);
    L.push(`## 見た目の変化（本番ブランチ ${visual.branch}・${visual.commit} との比較）`, '');
    L.push(`差分の割合が ${(o.diffThreshold * 100).toFixed(1)}% を超えたページ: ${big.length} / ${rows.length} 枚。意図した変更かを、人と品質管理部が差分画像で確認する（差分画像は赤が変わった部分。コミットしない）。`, '');
    L.push(`スクリーンショットと差分画像: \`${visual.dir}\`（base＝本番、current＝作業ブランチ、diff＝差分）`, '');
    if (big.length) {
      L.push('| ページ（@画面幅） | 差分の割合 | 高さ（本番→作業） | 差分画像 |', '|---|---|---|---|');
      big.forEach(r => L.push(`| ${r.name.replace(/\.png$/, '')} | ${(r.ratio * 100).toFixed(1)}% | ${r.base_h}→${r.cur_h}px | \`${r.diff}\` |`));
      L.push('');
    }
    const missing = visual.rows.filter(r => r.ratio === null);
    if (missing.length) L.push('本番ブランチにないページ（新しいページ）: ' + missing.map(r => r.name).join('、'), '');
  }
  if (notes.length) { L.push('## メモ', ''); notes.forEach(n => L.push('- ' + n)); L.push(''); }
  return L.join('\n');
}

(async () => {
  const o = parseArgs(process.argv.slice(2));
  o.today = o.date || todayJST();
  o.tmp = o.tmp || path.join(os.tmpdir(), 'akiyado-site-check');
  fs.mkdirSync(o.tmp, { recursive: true });
  const t0 = Date.now();
  const notes = [];
  const srv = await startServer(o.root);
  const browser = await playwright.chromium.launch();
  const rep = makeReport();
  let visual = null;
  let pages = [];
  try {
    pages = o.visualOnly ? [] : pageList(o.root, o.only);
    const tasks = [];
    for (const w of o.widths) for (const p of pages) tasks.push(() => checkPage(browser, srv, p, w, o, rep).catch(e => { rep.add('crit', p, w, '点検の失敗', String(e.message).split('\n')[0]); return null; }));
    const results = await pool(tasks, o.concurrency);
    await checkLinks(srv, results, rep);
    const future = pages.filter(p => { const d = publishDateOf(srv.route, p); return d && d > o.today; });
    await pool(future.map(p => () => checkScheduledRedirect(browser, srv, p, o, rep)), o.concurrency);
    if (o.visual) visual = await visualRegression(browser, srv, o, notes);
  } finally {
    await browser.close();
    srv.server.close();
  }
  const secs = (Date.now() - t0) / 1000;
  const md = toMarkdown(o, pages, rep, visual, notes, secs);
  if (o.json) console.log(JSON.stringify({ items: rep.items(), external: rep.ext(), visual, notes, seconds: secs }, null, 1));
  else console.log(md);
  if (o.out) fs.writeFileSync(o.out, md + '\n');
  process.exit(rep.items().some(i => i.level === 'crit') ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
