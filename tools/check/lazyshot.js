const { chromium } = require('playwright');
// 画像の遅延読み込みを解除し、全画像の読み込み完了を待ってからフルページを撮る
(async () => { const b = await chromium.launch(); const [pg, w, out] = process.argv.slice(2); const date = process.argv[5] || '2026-11-10T09:00:00';
const ctx = await b.newContext({ viewport: { width: +w, height: 900 } }); const p = await ctx.newPage(); await p.clock.setFixedTime(new Date(date));
await p.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => { const s = document.createElement('style'); s.textContent = '*{transition:none!important;scroll-behavior:auto!important}'; document.head.appendChild(s); document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); }); });
await p.goto('file://' + require('path').join(__dirname, '..', '..', 'pages') + '/' + pg, { waitUntil: 'load' });
await p.evaluate(async () => { document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-visible')); const imgs = [...document.images]; await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); await Promise.all(imgs.map(i => i.decode ? i.decode().catch(()=>0) : 0)); });
await p.waitForTimeout(500); await p.screenshot({ path: out, fullPage: true }); await b.close(); })();
