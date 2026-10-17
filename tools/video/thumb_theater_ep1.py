#!/usr/bin/env python3
"""アキヤド劇場 第1話「民泊副業詐欺の仕組み」のサムネイル（解説と同じシリーズの型）（1280×720 PNG）を作る。型は docs/youtube/manual.md 5章。
使い方: python3 tools/video/thumb_theater_ep1.py 出力.png（要 Playwright。NODE_PATH は Playwright のある場所）
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_explainer as m
OUT = sys.argv[1]
html = m.HTML.replace("__SC__", "[[0,1]]").replace("__SUBS__", "[]")
CODE = r"""(()=>{
// 劇場の舞台（夜のセミナー会場）
let s=`<rect width="1920" height="1080" fill="#2c2140"/><rect y="960" width="1920" height="120" fill="#221a33"/>`;
s+=`<path d="M560 0 L260 960 L1660 960 L1360 0Z" fill="#fff6c9" opacity=".16"/>`;
s+=`<path d="M0 0 H280 Q240 460 280 960 H0Z" fill="#a23b3b"/><path d="M1920 0 H1640 Q1680 460 1640 960 H1920Z" fill="#a23b3b"/><path d="M60 0 v960 M140 0 v960 M210 0 v960 M1710 0 v960 M1780 0 v960 M1860 0 v960" stroke="#8a2f2f" stroke-width="12"/>`;
s+=`<rect x="280" y="900" width="1360" height="64" rx="10" fill="#6b4a8a"/><rect x="280" y="892" width="1360" height="18" rx="8" fill="#8a66ad"/>`;
for(let k=0;k<9;k++)s+=`<circle cx="${420+k*135}" cy="${380+(k%2)*14}" r="9" fill="#fff6c9" opacity="${.5+.4*(k%3)/2}"/>`;
// 生徒さん3人（月100万円！）。正体は伏せる
[['umaiA',590,610],['umaiB',960,590],['umaiC',1330,610]].forEach(([c,x,y],k)=>{
  s+=face('f'+k,x,y,170,c,'#e8b950','happy',.3);
  s+=`<g transform="rotate(${[-5,4,-3][k]} ${x} ${y+190})"><rect x="${x-140}" y="${y+168}" width="280" height="76" rx="38" fill="#fff"/><text x="${x}" y="${y+220}" text-anchor="middle" font-size="40" font-weight="900" fill="#e53935">月100万円！</text></g>`;
  s+=`<text x="${x+130}" y="${y-126}" font-size="86" font-weight="900" fill="${Y}" stroke="#2c2140" stroke-width="8" paint-order="stroke">?</text>`;
});
for(let k=0;k<6;k++)s+=sparkle([380,1540,400,1520,720,1210][k],[360,380,820,810,370,360][k],1,k,k);
// シリーズの枠：アキヤド劇場 第1話＋問いのカード（中央）
s+=`<rect x="40" y="44" width="400" height="84" rx="42" fill="#2e6b47"/><text x="240" y="102" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">アキヤド劇場 第1話</text>`;
s+=`<rect x="472" y="74" width="1000" height="250" rx="10" fill="#000" opacity=".25"/><rect x="460" y="60" width="1000" height="250" rx="10" fill="#fff"/><rect x="460" y="60" width="1000" height="14" rx="7" fill="#2e6b47"/>`;
s+=`<text x="960" y="168" text-anchor="middle" font-size="76" font-weight="900" fill="#1f3a2b">民泊副業<tspan fill="#c95a35">詐欺</tspan>の仕組み</text><text x="960" y="272" text-anchor="middle" font-size="64" font-weight="900" fill="#1f3a2b">この3人の正体、わかる？</text>`;
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
