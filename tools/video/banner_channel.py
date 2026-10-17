#!/usr/bin/env python3
"""YouTube チャンネルのバナー（2560×1440 PNG）を作る。
スマホでも切れない真ん中（1546×423）に番組名と説明を入れ、PC・テレビで見える左右に宿と戦略家アキを置く。
使い方: python3 tools/video/banner_channel.py 出力.png [--guide]（--guide は切れない範囲の枠を描いた確認用）
"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_explainer as m
OUT = sys.argv[1]
GUIDE = "--guide" in sys.argv
html = m.HTML.replace("__SC__", "[[0,1]]").replace("__SUBS__", "[]")
# 座標は 1920×1080（書き出しで 4/3 倍）。スマホで見える範囲 = x 380〜1540・y 382〜699、PC で見える範囲 = 横いっぱい・y 382〜699
CODE = r"""(()=>{
CAST.aki={skin:'#f1c7a1',hair:'#2b2422',style:'short',top:'#23395b',top2:'#1a2c47',inner:'#ffffff',jacket:true,pants:'#2a3140',shoes:'#3a2a20',glasses:true,tie:'#c95a35'};
THEMES.teal={sky:'#cfe6d6',sun:'#fbe6c4',far:'#b7d9c2',mid:'#a3ceb2',win:'#e3f1e7',near:'#7fb894',gr:'#9fcaae',gr2:'#8fbf9f'};
let s=bg(3,'teal');
const B=692;
s+=`<rect x="0" y="${B}" width="1920" height="${1080-B}" fill="#8fbf9f"/>`;
const stack=(x,n)=>{let g='';for(let k=0;k<n;k++)g+=`<ellipse cx="${x}" cy="${B-6-k*13}" rx="32" ry="10" fill="#d09a2f"/><ellipse cx="${x}" cy="${B-10-k*13}" rx="32" ry="10" fill="#f2c14e"/>`;return g};
s+=house(150,B,.55,1)+stack(300,4)+stack(345,7);
s+=house(1800,B,.55,1)+stack(1640,5);
s+=person(1690,B,.45,{c:'aki',pose:'point',mood:'happy',t:.3,flip:true});
// 真ん中のカード（番組名と説明）
s+=`<rect x="432" y="412" width="1080" height="262" rx="28" fill="#000" opacity=".10"/><rect x="420" y="398" width="1080" height="262" rx="28" fill="#fff"/>`;
s+=`<g id="ttl">${MARK(52,-32,1.6)}<text x="128" y="0" font-size="92" font-weight="900" fill="${G}">アキヤド <tspan fill="${T}">民泊school</tspan></text></g>`;
s+=`<rect x="470" y="584" width="980" height="4" rx="2" fill="${G}" opacity=".18"/>`;
s+=`<text x="960" y="636" text-anchor="middle" font-size="38" font-weight="800" fill="${DG}">民泊戦略家が、空き家と民泊の専門知識を<tspan fill="${T}">わかりやすく</tspan>解説</text>`;
if(GUIDE)s+=`<rect x="380" y="382" width="1160" height="317" fill="none" stroke="red" stroke-width="3"/><rect x="0" y="382" width="1920" height="317" fill="none" stroke="blue" stroke-width="3"/>`;
document.getElementById('s').innerHTML=s;
const g=document.getElementById('ttl'),bb=g.getBBox();g.setAttribute('transform',`translate(${960-bb.x-bb.width/2},545)`);})()""".replace("GUIDE", "true" if GUIDE else "false")
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
    subprocess.run(["node", js, h, OUT, CODE], check=True, env=dict(os.environ, NODE_PATH="/opt/node-tools/node_modules"))
print(OUT)
