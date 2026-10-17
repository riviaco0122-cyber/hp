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
THEMES.teal={sky:'#86d6d8',sun:'#c9f1f0',far:'#72c8cb',mid:'#62bdc1',win:'#b2e6e7',near:'#4aa9ae',gr:'#5cb7bb',gr2:'#4fadb1'};
let s=bg(3,'teal');
// 宿と、積み上がるコイン・伸びるグラフ・飛行機（旅行者）
s+=house(470,GROUND,1.0,1);
const stack=(x,n)=>{let g='';for(let k=0;k<n;k++)g+=`<ellipse cx="${x}" cy="${GROUND-10-k*22}" rx="54" ry="16" fill="#d09a2f"/><ellipse cx="${x}" cy="${GROUND-16-k*22}" rx="54" ry="16" fill="#f2c14e"/>`;return g};
s+=stack(770,5)+stack(880,8)+stack(160,3);
s+=coin(880,GROUND-215,40);
[[1050,0,60],[1130,0,110],[1210,0,170],[1290,0,240]].forEach(([x,y,h],k)=>{s+=`<rect x="${x}" y="${GROUND-h}" width="56" height="${h}" rx="6" fill="#fff" opacity=".85"/>`});
s+=`<path d="M1040 ${GROUND-90} L1140 ${GROUND-150} L1220 ${GROUND-200} L1340 ${GROUND-300}" stroke="#e53935" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M1340 ${GROUND-300} l-46 6 l30 34z" fill="#e53935"/>`;
s+=`<g transform="translate(330,420) rotate(-14)"><path d="M-70 0 L60 -8 Q86 -8 86 0 Q86 8 60 8 L-70 0Z" fill="#fff"/><path d="M-10 -4 L-50 -50 L-26 -50 L20 -4Z M-10 4 L-50 50 L-26 50 L20 4Z" fill="#fff"/><path d="M-66 -2 L-86 -26 L-74 -26 L-56 -2Z" fill="#fff"/></g>`;
s+=`<path d="M110 510 Q200 470 270 450" stroke="#fff" stroke-width="5" stroke-dasharray="12 12" fill="none" opacity=".8"/>`;
s+=person(1640,GROUND,1.05,{c:'aki',pose:'point',mood:'happy',t:.3,flip:true});
// シリーズの枠：第1回＋問いのカード
s+=`<text x="64" y="104" font-size="60" font-weight="900" fill="#1f2a33">第1回</text>`;
s+=`<rect x="522" y="80" width="900" height="250" rx="10" fill="#000" opacity=".12"/><rect x="510" y="66" width="900" height="250" rx="10" fill="#fff"/>`;
s+=`<text x="960" y="172" text-anchor="middle" font-size="78" font-weight="900" fill="#1f2a33">民泊はなぜ</text><text x="960" y="278" text-anchor="middle" font-size="78" font-weight="900" fill="#1f2a33">「<tspan fill="#c95a35">第3の資産</tspan>」なのか？</text>`;
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
