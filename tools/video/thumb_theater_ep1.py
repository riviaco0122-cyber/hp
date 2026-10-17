#!/usr/bin/env python3
"""アキヤド劇場 第1話のサムネイル（1280×720 PNG）を作る。型は docs/youtube/manual.md 5章。
使い方: python3 tools/video/thumb_theater_ep1.py 出力.png（要 Playwright。NODE_PATH は Playwright のある場所）
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_explainer as m
OUT = sys.argv[1]
html = m.HTML.replace("__SC__", "[[0,1]]").replace("__SUBS__", "[]")
CODE = r"""(()=>{
const big=(x,y,s,fs,c,a='start')=>`<text x="${x}" y="${y}" text-anchor="${a}" font-size="${fs}" font-weight="900" fill="${c}" stroke="#fff" stroke-width="${fs*.17}" stroke-linejoin="round" paint-order="stroke">${s}</text>`;
let s=`<rect width="1920" height="1080" fill="#3a2a4f"/><path d="M760 0 L460 1080 L1760 1080 L1460 0Z" fill="#fff6c9" opacity=".14"/>`;
for(let k=0;k<10;k++){s+=sparkle(200+rnd(k)*1600,80+rnd(k+20)*900,1.1,k,k)}
s+=`<g transform="translate(60,50)"><rect width="430" height="80" rx="40" fill="${G}"/>${MARK(46,40,.9)}<text x="96" y="56" font-size="40" font-weight="900" fill="#fff">アキヤド劇場</text></g>`;
s+=`<g transform="rotate(-3 300 215)"><rect x="60" y="175" width="480" height="84" rx="16" fill="${Y}"/><text x="300" y="235" text-anchor="middle" font-size="54" font-weight="900" fill="#3a2a4f">アニメでわかる</text></g>`;
s+=big(60,440,'民泊副業',145,DG);
s+=big(60,680,'詐欺',200,'#e53935');
s+=big(480,680,'の',110,DG);
s+=big(60,900,'仕組み',145,DG);
[['umaiA',1170,290],['umaiB',1650,450],['umaiC',1230,770]].forEach(([c,x,y],k)=>{s+=face('f'+k,x,y,195,c,'#e8b950','happy',.3);s+=`<g transform="rotate(${[-6,5,-4][k]} ${x} ${y+230})"><rect x="${x-170}" y="${y+190}" width="340" height="86" rx="43" fill="#fff"/><text x="${x}" y="${y+250}" text-anchor="middle" font-size="50" font-weight="900" fill="#e53935">月100万円！</text></g>`});
document.getElementById('s').innerHTML=s;})()"""
JS = """
const { chromium } = require('playwright');
(async () => {
  const [html, out, code] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 4/3 });
  await p.goto('file://' + html);
  await p.evaluate(async () => { await document.fonts.ready; });
  await p.evaluate(code); await p.waitForTimeout(150);
  await p.screenshot({ path: out, type: 'png' });
  await b.close();
})();
"""
with tempfile.TemporaryDirectory() as tmp:
    h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(html)
    js = os.path.join(tmp, "r.js"); open(js, "w").write(JS)
    png = os.path.join(tmp, "t.png")
    subprocess.run(["node", js, h, png, CODE], check=True, env=dict(os.environ, NODE_PATH="/opt/node-tools/node_modules"))
    from PIL import Image, ImageFilter
    im = Image.open(png).convert("RGB").resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
    im.save(OUT, optimize=True)
print(OUT)
