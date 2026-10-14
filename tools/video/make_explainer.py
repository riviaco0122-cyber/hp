#!/usr/bin/env python3
"""アキヤドのサービス紹介の解説アニメ（約44秒・1920×1080・字幕つき・合成BGMつき）を作る。

- 絵はすべて、SVG の部品（人・家・お金・パソコンなど）を JS で組み、時刻 t ごとに描く（フラットなイラスト）。
- 各フレームを Playwright で画像にして、ffmpeg でつなぐ。BGM は tools/video/make_intro.py の合成を使う。
- 文言は、サイトに載っているサービスの説明と、取材事例の件数だけ。数字を作らない。
使い方: python3 tools/video/make_explainer.py [出力.mp4] [--preview 秒 ...]   # --preview は、その秒の静止画だけ書き出す
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FPS = 24
DUR = 44.0

HTML = r"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
@import url("https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&display=block");
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#dff1e6;font-family:"Zen Maru Gothic",sans-serif}
svg{display:block}
text{font-family:"Zen Maru Gothic","Zen Kaku Gothic New",sans-serif}
</style></head><body><svg id="s" width="1920" height="1080" viewBox="0 0 1920 1080"></svg>
<script>
const G='#2e6b47',DG='#1f3a2b',T='#c95a35',Y='#f0b35a',NV='#1f3a52',SKIN='#f2c9a5';
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const eo=x=>1-Math.pow(1-clamp(x),3);
const bk=x=>{x=clamp(x);const c=1.70158,c3=c+1;return 1+c3*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const mix=(a,b,k)=>{const p=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));const A=p(a),B=p(b);return '#'+A.map((v,i)=>Math.round(v+(B[i]-v)*k).toString(16).padStart(2,'0')).join('')};
const seg=(t,a,b)=>clamp((t-a)/(b-a));
// ---------- 部品 ----------
function person(x,y,s,o){ // o:{shirt,hair,pose,t,flip,tag}
  const sh=o.shirt||G,hair=o.hair||'#2b2b33',pants=o.pants||'#3b4a5a',t=o.t||0,pose=o.pose||'stand';
  const bob=Math.sin(t*3)*3;
  let arms='';
  const arm=(x1,y1,x2,y2,c=sh)=>`<path d="M${x1} ${y1} L${x2} ${y2}" stroke="${c}" stroke-width="30" stroke-linecap="round"/><circle cx="${x2}" cy="${y2}" r="17" fill="${SKIN}"/>`;
  if(pose==='think'){arms=arm(-34,-190,-70,-110)+arm(34,-190,18,-290-bob*0)}
  else if(pose==='cheer'){const w=Math.sin(t*6)*12;arms=arm(-34,-190,-95,-290+w)+arm(34,-190,95,-290-w)}
  else if(pose==='point'){arms=arm(-34,-190,-62,-110)+arm(34,-190,140,-250)}
  else if(pose==='type'){arms=arm(-34,-190,-20,-130)+arm(34,-190,40,-130)}
  else {arms=arm(-34,-190,-62,-110)+arm(34,-190,62,-110)}
  const mouth=(o.mood==='worry')?`<path d="M-14 -317 q14 -10 28 0" stroke="#7a3b2e" stroke-width="5" fill="none" stroke-linecap="round"/>`:`<path d="M-16 -322 q16 16 32 0" stroke="#7a3b2e" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  const brow=(o.mood==='worry')?`<path d="M-30 -352 l16 -7M30 -352 l-16 -7" stroke="${hair}" stroke-width="5" stroke-linecap="round"/>`:'';
  const tag=o.tag?`<g transform="translate(0,-170)"><rect x="-58" y="0" width="116" height="40" rx="10" fill="#fff" opacity=".95"/><text x="0" y="29" text-anchor="middle" font-size="26" font-weight="900" fill="${DG}">${o.tag}</text></g>`:'';
  return `<g transform="translate(${x},${y+bob}) scale(${o.flip?-s:s},${s})">
  <ellipse cx="0" cy="8" rx="95" ry="16" fill="#000" opacity=".12"/>
  <rect x="-38" y="-130" width="30" height="125" rx="14" fill="${pants}"/><rect x="8" y="-130" width="30" height="125" rx="14" fill="${pants}"/>
  <rect x="-48" y="-235" width="96" height="125" rx="34" fill="${sh}"/>
  ${arms}
  <rect x="-13" y="-262" width="26" height="30" rx="10" fill="${SKIN}"/>
  <circle cx="0" cy="-328" r="52" fill="${SKIN}"/>
  <path d="M-54 -332 q4 -62 54 -62 q54 0 54 62 q-18 -34 -56 -36 q-38 0 -52 36z" fill="${hair}"/>
  <circle cx="-19" cy="-332" r="5.5" fill="#2b2b33"/><circle cx="19" cy="-332" r="5.5" fill="#2b2b33"/>${brow}${mouth}
  ${o.tag?`</g><g transform="translate(${x},${y+bob}) scale(${s})">${tag}`:''}</g>`;
}
function house(x,y,s,k,o={}){ // k:0=古い空き家 1=再生した宿
  const wall=mix('#b9a58f','#fbf1dc',k),roof=mix('#6d625a',T,k),door=mix('#6a5646',G,k),win=mix('#8d99a0',Y,k);
  const cracks=k<.99?`<g opacity="${1-k}" stroke="#4d4136" stroke-width="5" fill="none"><path d="M-110 -250 l22 36 l-18 30 l24 40"/><path d="M70 -300 l-16 30 l20 24"/></g>`:'';
  const boards=k<.99?`<g opacity="${1-k}"><rect x="-128" y="-228" width="76" height="14" fill="#7a6a58" transform="rotate(-12 -90 -220)"/><rect x="-128" y="-196" width="76" height="14" fill="#7a6a58" transform="rotate(10 -90 -190)"/></g>`:'';
  const grass=k<.99?`<g opacity="${1-k}" fill="#7d9a5f"><path d="M-200 0 l10 -50 l10 50z M-170 0 l14 -64 l12 64z M140 0 l10 -48 l10 48z M180 0 l12 -60 l12 60z"/></g>`:'';
  const glow=k>.01?`<circle cx="-90" cy="-210" r="${70*k}" fill="${Y}" opacity="${.25*k}"/>`:'';
  const flag=k>.6?`<g opacity="${(k-.6)/.4}"><rect x="108" y="-470" width="6" height="90" fill="${DG}"/><path d="M114 -470 h70 l-16 22 l16 22 h-70z" fill="${T}"/></g>`:'';
  return `<g transform="translate(${x},${y}) scale(${s})">
  <ellipse cx="0" cy="10" rx="260" ry="20" fill="#000" opacity=".12"/>
  <rect x="-190" y="-300" width="380" height="300" rx="10" fill="${wall}"/>
  <path d="M-230 -296 L0 -470 L230 -296z" fill="${roof}"/>
  <rect x="-128" y="-240" width="76" height="76" rx="8" fill="${win}"/><rect x="52" y="-240" width="76" height="76" rx="8" fill="${win}"/>
  <rect x="-34" y="-190" width="68" height="190" rx="10" fill="${door}"/><circle cx="18" cy="-98" r="6" fill="#f0e2c6"/>
  ${glow}${cracks}${boards}${grass}${flag}</g>`;
}
const money=(x,y,s,p=1)=>`<g transform="translate(${x},${y}) scale(${s})" opacity="${p}"><path d="M-60 0 q-26 -70 26 -96 h68 q52 26 26 96z" fill="#e8b950"/><rect x="-30" y="-110" width="60" height="26" rx="10" fill="#d09a2f"/><text x="0" y="-26" text-anchor="middle" font-size="76" font-weight="900" fill="#fff">¥</text></g>`;
const coin=(x,y,r=34)=>`<g transform="translate(${x},${y})"><circle r="${r}" fill="#e8b950"/><circle r="${r*.72}" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/><text y="${r*.36}" text-anchor="middle" font-size="${r*1.05}" font-weight="900" fill="#fff">¥</text></g>`;
const laptop=(x,y,s)=>`<g transform="translate(${x},${y}) scale(${s})"><rect x="-150" y="-190" width="300" height="190" rx="14" fill="#2b3a35"/><rect x="-134" y="-174" width="268" height="158" rx="6" fill="#dff1e6"/><rect x="-120" y="-156" width="120" height="14" rx="7" fill="${G}"/><rect x="-120" y="-128" width="200" height="10" rx="5" fill="#a9c4b2"/><rect x="-120" y="-106" width="170" height="10" rx="5" fill="#a9c4b2"/><rect x="-120" y="-84" width="110" height="34" rx="10" fill="${T}"/><path d="M-190 0 h380 l-20 24 h-340z" fill="#c9d6cf"/></g>`;
const bubble=(x,y,w,h,txt,fs,p)=>`<g transform="translate(${x},${y}) scale(${p})"><path d="M${-w/2} ${-h/2} h${w} a30 30 0 0 1 30 30 v${h-60} a30 30 0 0 1 -30 30 h${-w/2+30} l-34 40 l4 -40 h${-w/2-30} a30 30 0 0 1 -30 -30 v${-(h-60)} a30 30 0 0 1 30 -30z" fill="#fff" stroke="${G}" stroke-width="6"/><text x="0" y="${fs*.35}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${DG}">${txt}</text></g>`;
const q=(x,y,s,t,ph)=>`<text x="${x}" y="${y+Math.sin(t*4+ph)*10}" font-size="${s}" font-weight="900" fill="${T}" text-anchor="middle" transform="rotate(${Math.sin(t*3+ph)*8} ${x} ${y})">？</text>`;
const sparkle=(x,y,s,t,ph)=>{const a=.5+.5*Math.sin(t*5+ph);return `<path transform="translate(${x},${y}) scale(${s*(.6+.4*a)})" d="M0 -30 L8 -8 L30 0 L8 8 L0 30 L-8 8 L-30 0 L-8 -8z" fill="${Y}" opacity="${.4+.6*a}"/>`};
function caption(txt,p,y=70,fs=84){ // 上の字幕パネル（四隅の紺の点つき）
  const w=Math.max(560,txt.length*fs*.98+120),h=fs*1.55,x=960-w/2;
  const s=bk(p),o=clamp(p*3);
  return `<g opacity="${o}" transform="translate(960,${y+h/2}) scale(${s}) translate(-960,${-(y+h/2)})"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="#fff" opacity=".93"/>
  <circle cx="${x+10}" cy="${y+10}" r="11" fill="${NV}"/><circle cx="${x+w-10}" cy="${y+10}" r="11" fill="${NV}"/><circle cx="${x+10}" cy="${y+h-10}" r="11" fill="${NV}"/><circle cx="${x+w-10}" cy="${y+h-10}" r="11" fill="${NV}"/>
  <text x="960" y="${y+h/2+fs*.34}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="#14202a" letter-spacing="2">${txt}</text></g>`;
}
function sub(lines,p){ // 下の小さな字幕
  const o=clamp(p*3),n=lines.length,fs=46,h=n*fs*1.5+36,w=1500;
  return `<g opacity="${o}" transform="translate(0,${(1-eo(p))*30})"><rect x="${960-w/2}" y="${1040-h}" width="${w}" height="${h}" rx="22" fill="${DG}" opacity=".92"/>${lines.map((l,i)=>`<text x="960" y="${1040-h+18+fs*1.2+i*fs*1.5}" text-anchor="middle" font-size="${fs}" font-weight="700" fill="#fff" letter-spacing="1.5">${l}</text>`).join('')}</g>`;
}
function bg(t){
  const cl=(x,y,s,sp)=>`<g transform="translate(${((x+t*sp)%2400)-240},${y}) scale(${s})" fill="#fff" opacity=".7"><ellipse cx="0" cy="0" rx="90" ry="34"/><ellipse cx="60" cy="-16" rx="64" ry="30"/><ellipse cx="-56" cy="-8" rx="56" ry="26"/></g>`;
  return `<rect width="1920" height="1080" fill="#dff1e6"/>${cl(200,250,1.3,14)}${cl(900,180,1,9)}${cl(1500,300,1.5,12)}
  <path d="M0 640 q240 -150 520 -40 q300 -130 640 -30 q330 -120 760 -10 V1080 H0z" fill="#c4e3cf"/><rect y="800" width="1920" height="280" fill="#a9d4b8"/><rect y="800" width="1920" height="10" fill="#8fc2a1"/>`;
}
const LOGO=(x,y,s)=>`<g transform="translate(${x},${y}) scale(${s})"><rect width="64" height="64" rx="18" fill="${G}"/><path d="M15 31 L32 17 L49 31 V48 a2.6 2.6 0 0 1 -2.6 2.6 H37 V39 H27 V50.6 H17.6 A2.6 2.6 0 0 1 15 48z" fill="#fff"/><text x="84" y="46" font-size="46" font-weight="900" fill="${DG}" letter-spacing="6">アキヤド</text></g>`;
const AV=[1,2,3,6,4,5];
// ---------- 場面 ----------
const SC=[[0,7],[7,13],[13,20],[20,27],[27,34],[34,39],[39,44]];
function scene(i,t,lt){
  let s='';
  if(i===0){ // 悩み
    s+=house(1300,810,1.05,0,{});
    s+=person(520,800,1.25,{pose:'think',mood:'worry',t:lt,shirt:G});
    s+=[[430,520,90,0],[610,470,70,1.5],[1000,380,80,3]].map(([x,y,z,ph],k)=>`<g opacity="${eo(seg(lt,.8+k*.35,1.4+k*.35))}">${q(x,y,z,lt,ph)}</g>`).join('');
    s+=caption('空き家、どうしよう？',seg(lt,.2,.9));
    s+=sub(['相続した実家、遠くて管理できない…。','そんな悩みを、お持ちではありませんか。'],seg(lt,2.2,2.9));
  }
  if(i===1){ // アキヤドが答える
    const k=eo(seg(lt,1.2,3.2));
    s+=house(1300,810,1.05,k,{});
    s+=person(520,800,1.25,{pose:'cheer',t:lt,shirt:G});
    s+=person(800,800,1.25,{pose:'point',t:lt+1,shirt:T,hair:'#4a3328',tag:'アキヤド'});
    s+=[[1050,430,1.2,0],[1450,380,1.4,1],[1380,560,.9,2],[620,430,1.1,3]].map(([x,y,z,ph])=>sparkle(x,y,z,lt,ph)).join('');
    s+=caption('悩みの順に、お答えします',seg(lt,.2,.9),70,76);
    s+=`<g opacity="${eo(seg(lt,2.4,3.2))}">${LOGO(790,200,1.1)}</g>`;
    s+=sub(['空き家と民泊のメディア「アキヤド」'],seg(lt,3,3.6));
  }
  if(i===2){ // 買取
    const mv=eo(seg(lt,2.2,3.6));
    s+=house(1180,810,1.0,0,{});
    s+=person(520,800,1.25,{pose:'stand',t:lt,shirt:G});
    s+=`<g opacity="${eo(seg(lt,2.2,3))}">${money(1620,800-eo(seg(lt,2.2,3.4))*60,1.5)}</g>`;
    s+=`<g opacity="${eo(seg(lt,2.4,3.2))}"><path d="M1420 600 h60" stroke="${T}" stroke-width="10" stroke-linecap="round"/><path d="M1470 580 l30 20 l-30 20" stroke="${T}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;
    s+=caption('① 空き家を売りたい方へ',seg(lt,.2,.9),70,78);
    s+=`<g opacity="${eo(seg(lt,.8,1.5))}"><rect x="600" y="210" width="720" height="86" rx="43" fill="${T}"/><text x="960" y="270" text-anchor="middle" font-size="52" font-weight="900" fill="#fff" letter-spacing="3">アキヤド買取プラン</text></g>`;
    s+=sub(['「宿として再生できるか」という目で、物件を見ます。','一般の仲介では値段がつきにくい家も、ご相談ください。'],seg(lt,1.6,2.3));
  }
  if(i===3){ // 借り上げ
    const k=eo(seg(lt,1.4,3));
    s+=house(1300,810,1.05,k,{});
    s+=person(560,800,1.25,{pose:'point',t:lt,shirt:G});
    for(let c=0;c<5;c++){const p=seg(lt,3+c*.35,4.4+c*.35);if(p>0&&p<1.02)s+=`<g opacity="${Math.sin(clamp(p)*Math.PI)}">${coin(1180-p*520, 560-Math.sin(p*Math.PI)*110+p*40, 34)}</g>`.replace('translate(','translate(')}
    s+=caption('② 空き家を活かしたい方へ',seg(lt,.2,.9),70,78);
    s+=`<g opacity="${eo(seg(lt,.8,1.5))}"><rect x="560" y="210" width="800" height="86" rx="43" fill="${T}"/><text x="960" y="270" text-anchor="middle" font-size="52" font-weight="900" fill="#fff" letter-spacing="3">アキヤド借り上げプラン</text></g>`;
    s+=sub(['アキヤドが借り上げ、改修から宿の運営まで行います。','運営の手間をかけず、家賃を受け取れます。'],seg(lt,1.6,2.3));
  }
  if(i===4){ // 開業・運営
    s+=person(520,800,1.25,{pose:'type',t:lt,shirt:G});
    s+=laptop(800,800,1.0);
    const items=['物件選び','許可・届出','集客'];
    s+=items.map((x,i)=>{const p=eo(seg(lt,2+i*.7,2.7+i*.7));return `<g opacity="${p}" transform="translate(0,${(1-p)*30})"><rect x="1180" y="${330+i*120}" width="520" height="92" rx="20" fill="#fff"/><circle cx="1236" cy="${376+i*120}" r="26" fill="${G}"/><path d="M1224 ${376+i*120} l9 10 l17 -20" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><text x="1288" y="${390+i*120}" font-size="48" font-weight="900" fill="${DG}">${x}</text></g>`}).join('');
    s+=person(1120,800,1.05,{pose:'stand',t:lt+1,shirt:T,hair:'#4a3328',tag:'アキヤド'}).replace('rx="95"','rx="95"');
    s+=caption('③ 副業で宿をはじめたい方へ',seg(lt,.2,.9),70,74);
    s+=`<g opacity="${eo(seg(lt,.8,1.5))}"><rect x="560" y="210" width="800" height="86" rx="43" fill="${T}"/><text x="960" y="270" text-anchor="middle" font-size="52" font-weight="900" fill="#fff" letter-spacing="3">アキヤド開業・運営プラン</text></g>`;
    s+=sub(['実際に宿を運営しているアキヤドが、','任せたい範囲に合わせて支えます。'],seg(lt,1.6,2.3));
  }
  if(i===5){ // 事例
    s+=caption('取材した、6人のオーナーの事例',seg(lt,.2,.9),90,76);
    s+=AV.map((n,k)=>{const p=bk(seg(lt,.9+k*.25,1.5+k*.25));const x=330+k*252;return `<g transform="translate(${x},520) scale(${p})"><circle r="110" fill="#fff"/><clipPath id="c${k}"><circle r="100"/></clipPath><image href="file://__ROOT__/images/portraits/circle/user_0${n}.png" x="-100" y="-100" width="200" height="200" clip-path="url(#c${k})"/><circle r="100" fill="none" stroke="${T}" stroke-width="6"/></g>`}).join('');
    s+=sub(['初期費用・月商・純利益を、オーナーの申告の数字で。','事例も公開しています。'],seg(lt,2.4,3.1));
  }
  if(i===6){ // CTA
    s+=person(300,800,1.3,{pose:'cheer',t:lt,shirt:G});
    s+=person(1620,800,1.3,{pose:'cheer',t:lt+1,shirt:T,hair:'#4a3328',tag:'アキヤド'});
    s+=bubble(960,400,980,230,'まずは、無料でご相談ください',68,bk(seg(lt,.3,1.1)));
    s+=`<g opacity="${eo(seg(lt,1.3,2))}"><rect x="700" y="560" width="520" height="100" rx="50" fill="${T}"/><text x="960" y="630" text-anchor="middle" font-size="56" font-weight="900" fill="#fff" letter-spacing="4">rivia-co.com</text></g>`;
    s+=sub(['相談・お見積りは無料、全国対応です。'],seg(lt,2,2.7));
    s+=`<g opacity="${eo(seg(lt,2.4,3.2))}">${LOGO(780,700,1.2)}</g>`;
  }
  return s;
}
window.draw=function(t){
  const X=0.5; let out=bg(t);
  SC.forEach(([a,b],i)=>{
    const op=Math.min(clamp((t-a)/X+0.0001),clamp((b+X-t)/X));
    if(t>=a&&t<b+X){const o=(i===0&&t<X)?1:Math.min(clamp((t-a)/X),1)*1; const out2=(i===SC.length-1)?1:clamp((b+X-t)/X); out+=`<g opacity="${Math.min(i===0?1:o,out2)}">${scene(i,t,t-a)}</g>`}
  });
  document.getElementById('s').innerHTML=out.replaceAll('__ROOT__',window.ROOT);
};
</script></body></html>"""

RENDER_JS = """
const { chromium } = require('playwright');
(async () => {
  const [html, outdir, mode, arg] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + html);
  await p.evaluate(async () => { await document.fonts.ready; });
  await p.evaluate((r) => { window.ROOT = r; }, process.env.ROOT_DIR);
  if (mode === 'preview') {
    for (const t of JSON.parse(arg)) { await p.evaluate((t) => window.draw(t), t); await p.waitForTimeout(80); await p.screenshot({ path: outdir + '/p_' + t + '.png' }); }
  } else {
    const n = parseInt(arg);
    for (let i = 0; i < n; i++) { await p.evaluate((t) => window.draw(t), i / %FPS%); await p.screenshot({ path: outdir + '/f' + String(i).padStart(5, '0') + '.jpg', type: 'jpeg', quality: 90 }); }
  }
  await b.close();
})();
""".replace("%FPS%", str(FPS))


def main():
    args = sys.argv[1:]
    prev = None
    if "--preview" in args:
        k = args.index("--preview"); prev = [float(x) for x in args[k + 1:]]; args = args[:k]
    out = args[0] if args else os.path.join(ROOT, "docs", "media", "akiyado-service-intro-anime.mp4")
    env = dict(os.environ); env["ROOT_DIR"] = ROOT
    env["NODE_PATH"] = os.pathsep.join(p for p in ["/opt/node-tools/node_modules", os.path.join(ROOT, "tools", "check", "node_modules"), env.get("NODE_PATH", "")] if p)
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(HTML)
        js = os.path.join(tmp, "r.js"); open(js, "w").write(RENDER_JS)
        if prev is not None:
            od = "/tmp/claude-0/vid2"; os.makedirs(od, exist_ok=True)
            subprocess.run(["node", js, h, od, "preview", json.dumps(prev)], check=True, env=env); print("preview", od); return
        fr = os.path.join(tmp, "fr"); os.makedirs(fr)
        n = int(DUR * FPS)
        subprocess.run(["node", js, h, fr, "video", str(n)], check=True, env=env)
        from make_intro import synth_bgm
        wav = os.path.join(tmp, "bgm.wav"); synth_bgm(wav, DUR)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%05d.jpg"), "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, DUR, "秒")


if __name__ == "__main__":
    main()
