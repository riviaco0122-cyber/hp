#!/usr/bin/env python3
"""解説動画 第2回「民泊は届出か許可か」のサムネイル（1280×720 PNG）を作る。型は docs/youtube/manual.md 5章（シリーズの型）。
第1回より作り込む: 本編の絵（宿・カレンダー・石だたみ・遠景）の部品をそのまま使う。
案A（カード「同じ民泊なのに日数が半分？」。タイトルの問いとことばを重ねない）: 宿ふたつ＋365マスのカレンダー（180日で止まる／365日）。 案B: 小さな木戸と大きな門＋大きな日数の札。
使い方: python3 tools/video/thumb_strategy_ep2.py 出力A.png [出力B.png]（要 Playwright。NODE_PATH は Playwright のある場所）
"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_strategy_ep2 as e2

COMMON_HEAD = r"""(()=>{
let s=studio(.5,%J%);
const big=(x,y,w,txt,c)=>`<rect x="${x-w/2}" y="${y+8}" width="${w}" height="104" rx="52" fill="#000" opacity=".22"/><rect x="${x-w/2}" y="${y}" width="${w}" height="104" rx="52" fill="${c}" stroke="#fff" stroke-width="6"/><rect x="${x-w/2+20}" y="${y+8}" width="${w-40}" height="28" rx="14" fill="#fff" opacity=".22"/><text x="${x}" y="${y+78}" text-anchor="middle" font-size="76" font-weight="900" fill="#fff" stroke="#000" stroke-opacity=".25" stroke-width="2" paint-order="stroke">${txt}</text>`;
"""
FRAME = r"""
s+=`<rect x="40" y="44" width="180" height="84" rx="42" fill="#000" opacity=".14" transform="translate(0 6)"/><rect x="40" y="44" width="180" height="84" rx="42" fill="#2e6b47"/><rect x="52" y="50" width="156" height="24" rx="12" fill="#fff" opacity=".2"/><text x="130" y="106" text-anchor="middle" font-size="54" font-weight="900" fill="#fff">第2回</text>`;
s+=`<rect x="522" y="84" width="900" height="270" rx="10" fill="#000" opacity=".14"/><rect x="510" y="66" width="900" height="270" rx="10" fill="#fff"/><rect x="510" y="66" width="900" height="14" rx="7" fill="#2e6b47"/>`;
%CARD%
document.getElementById('s').innerHTML=s;})()"""

CARD_A = r"""s+=`<text x="960" y="170" text-anchor="middle" font-size="80" font-weight="900" fill="#1f3a2b">同じ民泊なのに</text><text x="960" y="298" text-anchor="middle" font-size="124" font-weight="900" fill="#1f3a2b">日数が<tspan fill="#c95a35">半分</tspan>？</text>`;"""
CARD_B = r"""s+=`<text x="960" y="180" text-anchor="middle" font-size="84" font-weight="900" fill="#1f3a2b">あなたの家は</text><text x="960" y="298" text-anchor="middle" font-size="104" font-weight="900" fill="#1f3a2b"><tspan fill="#c95a35">届出</tspan>か<tspan fill="#2e6b47">許可</tspan>か？</text>`;"""

SCENE_A = r"""
s+=inn(500,790,.78,{sign:'届出',roof:'#b5603a',noren:G,t:.4,lit:.7,case:1});
s+=inn(1090,790,.82,{sign:'許可',roof:'#2e6b47',noren:T,t:.9,lit:.9,post:1,bike:1,chim:1});
const bd=(x,y,w,h)=>`<rect x="${x-6}" y="${y-6}" width="${w+12}" height="${h+12}" rx="14" fill="#000" opacity=".2" transform="translate(0 6)"/><rect x="${x-6}" y="${y-6}" width="${w+12}" height="${h+12}" rx="14" fill="#fff"/>`;
s+=bd(278,832,444,120)+ybar(290,860,420,64,180,180,T,{});
s+=bd(868,832,444,120)+ybar(880,860,420,64,365,0,G,{});
s+=big(500,972,480,'年180日まで','#c95a35')+big(1090,972,590,'許可は上限なし','#2e6b47');
s+=`<g transform="translate(730 470) rotate(-8)"><circle r="78" fill="#fff" opacity=".96" stroke="#c95a35" stroke-width="8"/><text y="-8" text-anchor="middle" font-size="40" font-weight="900" fill="#c95a35">上限</text><text y="46" text-anchor="middle" font-size="58" font-weight="900" fill="#c95a35">49%</text></g>`;
s+=`<ellipse cx="1690" cy="${GROUND+16}" rx="130" ry="19" fill="#000" opacity=".26"/>`+person(1690,GROUND,1.12,{c:'aki',pose:'point',mood:'happy',t:.3,flip:true});
"""
SCENE_B = r"""
s+=`<g transform="translate(0 0)">${gateSmall(470,860,0)}${gateBig(1090,860,0)}</g>`;
const orb=(x,y,r,top,txt,c)=>`<circle cx="${x}" cy="${y+10}" r="${r}" fill="#000" opacity=".22"/><circle cx="${x}" cy="${y}" r="${r}" fill="${c}" stroke="#fff" stroke-width="9"/><ellipse cx="${x-r*.25}" cy="${y-r*.55}" rx="${r*.5}" ry="${r*.22}" fill="#fff" opacity=".25"/><text x="${x}" y="${y-r*.18}" text-anchor="middle" font-size="${r*.36}" font-weight="900" fill="#fff">${top}</text><text x="${x}" y="${y+r*.5}" text-anchor="middle" font-size="${r*.62}" font-weight="900" fill="#fff" stroke="#000" stroke-opacity=".25" stroke-width="2" paint-order="stroke">${txt}</text>`;
s+=orb(470,480,104,'年','180日','#c95a35')+orb(1090,480,112,'日数の上限','なし','#2e6b47');
s+=big(470,905,300,'届出','#c95a35')+big(1090,905,300,'許可','#2e6b47');
s+=`<ellipse cx="1690" cy="${GROUND+16}" rx="130" ry="19" fill="#000" opacity=".26"/>`+person(1690,GROUND,1.12,{c:'aki',pose:'point',mood:'happy',t:.3,flip:true});
"""
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
def render(out, scene, card, j):
    html = e2.build_html([[0, 10]] * 7, [])
    code = (COMMON_HEAD.replace("%J%", str(j)) + scene + FRAME.replace("%CARD%", card))
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(html)
        js = os.path.join(tmp, "r.js"); open(js, "w").write(JS)
        png = os.path.join(tmp, "t.png")
        subprocess.run(["node", js, h, png, code], check=True, env=dict(os.environ, NODE_PATH="/opt/node-tools/node_modules"))
        from PIL import Image, ImageFilter
        im = Image.open(png).convert("RGB").resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
        im.save(out, optimize=True)
    print(out)

if __name__ == "__main__":
    render(sys.argv[1], SCENE_A, CARD_A, 1)
    if len(sys.argv) > 2:
        render(sys.argv[2], SCENE_B, CARD_B, 3)
