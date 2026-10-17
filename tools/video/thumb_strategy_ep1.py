#!/usr/bin/env python3
"""解説動画 第1回「民泊を資産に入れる5つの理由」のサムネイル（1280×720 PNG）を作る。型は docs/youtube/manual.md 5章。
使い方: python3 tools/video/thumb_theater_ep1.py 出力.png（要 Playwright。NODE_PATH は Playwright のある場所）
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_explainer as m
OUT = sys.argv[1]
html = m.HTML.replace("__SC__", "[[0,1]]").replace("__SUBS__", "[]")
CODE = r"""(()=>{
CAST.aki={skin:'#f1c7a1',hair:'#2b2422',style:'short',top:'#23395b',top2:'#1a2c47',inner:'#ffffff',jacket:true,pants:'#2a3140',shoes:'#3a2a20',glasses:true,tie:'#c95a35'};
const big=(x,y,s,fs,c,sx=.92)=>`<g transform="translate(${x},${y}) scale(${sx},1)"><text x="0" y="0" font-size="${fs}" font-weight="900" fill="#fff" stroke="#fff" stroke-width="${fs*.30}" stroke-linejoin="round">${s}</text><text x="0" y="0" font-size="${fs}" font-weight="900" fill="${c}" stroke="#111" stroke-width="${fs*.13}" stroke-linejoin="round" paint-order="stroke">${s}</text></g>`;
let s=`<rect width="1920" height="1080" fill="#16233a"/><path d="M1080 0 L1920 0 L1920 1080 L760 1080Z" fill="#ffd84d"/>`;
for(let k=0;k<14;k++)s+=`<path d="M${1100+k*70} 1080 L${1300+k*70} 0" stroke="#ffc61a" stroke-width="18" opacity=".7"/>`;
s+=person(1500,2050,2.9,{c:'aki',pose:'point',mood:'happy',t:.3});
s+=`<rect x="50" y="46" width="560" height="96" rx="20" fill="#e53935"/><text x="330" y="116" text-anchor="middle" font-size="62" font-weight="900" fill="#fff">民泊戦略家が解説</text>`;
s+=big(60,370,'民泊は',190,'#fff');
s+=big(60,640,'第3の資産',230,'#ffd400');
s+=big(60,920,'5つの理由',200,'#ff3b30');
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
