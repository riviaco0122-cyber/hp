const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
const R=require('path').join(__dirname,'..','..','pages','en')+'/';
(async () => { const b = await chromium.launch();
for (const w of [1440,375]) { const p = await b.newPage({viewport:{width:w,height:900}});
for (const f of fs.readdirSync(R)) {
 await p.goto('file://'+R+f);
 const r = await p.evaluate(async () => { const imgs=[...document.images]; imgs.forEach(i=>i.loading='eager'); await Promise.all(imgs.map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r}))); 
   const ja=[...document.body.querySelectorAll('*')].filter(e=>e.children.length===0 && /[ぁ-んァ-ン一-龥]/.test(e.textContent) && e.offsetParent).map(e=>e.textContent.trim().slice(0,30));
   return {broken: imgs.filter(i=>!i.naturalWidth).length, ov: document.documentElement.scrollWidth>innerWidth, ja: ja.slice(0,5), links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))}; });
 const bad=r.links.filter(h=>!/^(https?:|mailto:|tel:|#)/.test(h)).filter(h=>{const t=path.resolve(R,h.split('#')[0].split('?')[0]); return h.split('#')[0] && !fs.existsSync(t);});
 if (r.broken||r.ov||r.ja.length||bad.length) console.log(w,f,JSON.stringify({broken:r.broken,ov:r.ov,ja:r.ja,bad:bad.slice(0,3)}));
}
await p.close(); }
console.log('done'); await b.close(); })();
