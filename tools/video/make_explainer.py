#!/usr/bin/env python3
"""アキヤドの、見た人が相談したくなる解説アニメ（約76秒・1920×1080・字幕・BGM・効果音つき）を作る。

- 流れ: 悩みのつかみ → 放置の負担 → 宿に変わる → あなたはどれ？ → 無料相談で比べられること
  → 借り上げのしくみ → 開業・運営の分担と手数料 → 運営実績 → 不安を消す → 問い合わせフォーム。
- 絵はすべて SVG を JS で組み、時刻 t ごとに描く（フラットなイラスト。人物は肩・ひじで曲がる腕、表情・まばたきつき）。
- 背景は場面ごとの色の町並み（山・家並み・木）を重ね、ゆっくり横に流す。場面の切り替えは丸く広がるワイプ。
- 各フレームを Playwright で画像にして ffmpeg でつなぐ。BGM と効果音は tools/video/pop_audio.py で合成する。
- 文言・数字は、サイトに載っているサービスの説明・実績・フォームの項目だけ。数字を作らない。
使い方: python3 tools/video/make_explainer.py [出力.mp4] [--preview 秒 ...]   # --preview は、その秒の静止画だけ書き出す
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FPS = 24
SC = [(0, 5), (5, 12), (12, 19), (19, 26), (26, 35), (35, 45), (45, 56), (56, 62), (62, 69), (69, 76)]
DUR = float(SC[-1][1])

# 効果音: (場面の番号, 場面の中の秒, 種類)。アニメの動き（JS の seg の開始）に合わせる
SFX = [
    (0, .1, "whoosh"), (0, .6, "pop"), (0, .9, "pop"), (0, 1.2, "pop"),
    (1, .2, "pop"), (1, 1.2, "whoosh"), (1, 1.8, "rise"), (1, 2.2, "pop"), (1, 2.9, "pop"), (1, 3.6, "pop"),
    (2, .2, "pop"), (2, 1.0, "chime"), (2, 2.6, "whoosh"), (2, 3.6, "pop"), (2, 4.5, "coin"), (2, 4.8, "pop"),
    (3, .1, "pop"), (3, .5, "pop"), (3, 1.2, "whoosh"), (3, 1.6, "pop"), (3, 2.0, "whoosh"), (3, 2.4, "pop"), (3, 2.8, "whoosh"), (3, 3.2, "pop"),
    (4, .2, "pop"), (4, .8, "pop"), (4, 1.2, "pop"), (4, 1.6, "pop"),
    *[(4, 2.4 + k * .25 + j * .3, "tick") for k in range(3) for j in range(3)], (4, 5.4, "ding"),
    (5, .2, "pop"), (5, .6, "pop"), (5, .9, "pop"), (5, 1.2, "pop"), (5, 1.6, "whoosh"), (5, 2.6, "whoosh"),
    (5, 3.6, "whoosh"), (5, 4.4, "coin"), (5, 4.6, "whoosh"), (5, 5.4, "coin"), (5, 6.4, "pop"), (5, 7.1, "pop"),
    (6, .2, "pop"), (6, .6, "pop"), *[(6, 1.8 + k * .35, "tick") for k in range(5)], (6, 6.2, "whoosh"),
    (6, 6.7, "rise"), (6, 7.8, "coin"), (6, 8.3, "coin"),
    (7, .2, "pop"), (7, .5, "whoosh"), (7, 1.0, "ding"), *[(7, 1.4 + k * .18, "pop") for k in range(6)],
    (8, .2, "pop"), (8, .8, "ding"), (8, 1.4, "ding"), (8, 2.0, "ding"),
    (9, .2, "pop"), (9, .5, "whoosh"), *[(9, 1.0 + k * .07, "tick") for k in range(60) if (1.0 + k * .07) < 5.0 and k % 2 == 0],
    (9, 5.6, "click"), (9, 5.9, "chime"), (9, 6.1, "pop"),
] + [(i, 0.0, "whoosh") for i in range(1, len(SC))]

HTML = r"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
@import url("https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&display=block");
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#cfeedd;font-family:"Zen Maru Gothic",sans-serif}
svg{display:block}
text{font-family:"Zen Maru Gothic","Zen Kaku Gothic New",sans-serif}
</style></head><body><svg id="s" width="1920" height="1080" viewBox="0 0 1920 1080"></svg>
<script>
const G='#2e6b47',DG='#1f3a2b',T='#c95a35',Y='#f0b35a',GROUND=860;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const eo=x=>1-Math.pow(1-clamp(x),3);
const bk=x=>{x=clamp(x);const c=1.70158,c3=c+1;return 1+c3*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const mix=(a,b,k)=>{const p=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));const A=p(a),B=p(b);return '#'+A.map((v,i)=>Math.round(v+(B[i]-v)*k).toString(16).padStart(2,'0')).join('')};
const seg=(t,a,b)=>clamp((t-a)/(b-a));
const rnd=(i)=>{const x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)};
// ---------- 人物（肩・ひじで曲がる腕。表情・まばたき・髪型・服の陰影） ----------
const CAST={
  owner:{skin:'#f1c7a1',hair:'#3b302a',style:'side',top:'#2e6b47',top2:'#24573a',collar:'#f4efe6',pants:'#3b4a5a',shoes:'#2a2a30'},
  staff:{skin:'#f3cba8',hair:'#2b2422',style:'bob',top:'#c95a35',top2:'#a94a2a',inner:'#ffffff',jacket:true,pants:'#2f3b4a',shoes:'#2a2a30',tag:true},
  guest1:{skin:'#e3b089',hair:'#1f1f24',style:'short',top:'#3d6a8a',top2:'#30566f',inner:'#f4efe6',jacket:true,pants:'#c9bfae',shoes:'#5a4636'},
  guest2:{skin:'#f6d2b4',hair:'#7a4a2a',style:'pony',top:'#f0b35a',top2:'#d89a3e',collar:'#ffffff',pants:'#2f3b4a',shoes:'#c95a35'},
};
function ik(sx,sy,hx,hy,side,L1=98,L2=92){
  let dx=hx-sx,dy=hy-sy,d=Math.hypot(dx,dy);const md=L1+L2-2;if(d>md){hx=sx+dx/d*md;hy=sy+dy/d*md;dx=hx-sx;dy=hy-sy;d=md}
  const a=Math.acos(clamp((L1*L1+d*d-L2*L2)/(2*L1*d),-1,1)),b=Math.atan2(dy,dx);
  const c1=[sx+Math.cos(b+a)*L1,sy+Math.sin(b+a)*L1],c2=[sx+Math.cos(b-a)*L1,sy+Math.sin(b-a)*L1];
  const sc=e=>e[1]+0.6*e[0]*side;const e=sc(c1)>sc(c2)?c1:c2;return [e,[hx,hy]];
}
function arm(c,side,hx,hy){
  const sx=side*54,sy=-432,[[ex,ey],[x,y]]=ik(sx,sy,hx,hy,side),sl=c.jacket?c.top:c.top;
  return `<path d="M${sx} ${sy} L${ex} ${ey}" stroke="${sl}" stroke-width="38" stroke-linecap="round"/><path d="M${ex} ${ey} L${x} ${y}" stroke="${sl}" stroke-width="33" stroke-linecap="round"/><path d="M${ex} ${ey} L${x} ${y}" stroke="${c.top2}" stroke-width="10" stroke-linecap="round" opacity=".45" transform="translate(${side*6},0)"/><circle cx="${x}" cy="${y}" r="13" fill="${c.inner||c.collar||'#fff'}"/><ellipse cx="${x+(x-ex)*.12}" cy="${y+(y-ey)*.12}" rx="17" ry="18" fill="${c.skin}"/>`;
}
const POSES={
  stand:(t)=>[[-82,-262],[82,-262]],
  hips:(t)=>[[-92,-300],[92,-300]],
  think:(t)=>[[34,-322],[20,-492]],
  cheer:(t)=>{const w=Math.sin(t*7)*14;return [[-128,-640+w],[128,-640-w]]},
  wave:(t)=>[[-82,-262],[150+Math.sin(t*8)*18,-610]],
  point:(t)=>[[-82,-262],[232,-470]],
  open:(t)=>[[-136,-296+Math.sin(t*4)*6],[136,-296-Math.sin(t*4)*6]],
  walk:(t)=>[[-70+Math.sin(t*9)*26,-262],[70-Math.sin(t*9)*26,-262]],
};
function head(c,mood,t,seed){
  const blink=((t*0.8+seed)%3.1)<0.1;
  const hb={short:`M-47 -536 Q-50 -594 0 -596 Q50 -594 47 -536 Q42 -562 22 -566 Q-6 -556 -30 -568 Q-44 -558 -47 -536Z`,
    side:`M-49 -530 Q-54 -598 4 -598 Q54 -596 49 -534 Q44 -568 24 -572 Q-4 -548 -38 -562 Q-48 -552 -49 -530Z`,
    bob:`M-50 -528 Q-52 -600 0 -600 Q52 -600 50 -528 Q34 -570 0 -568 Q-34 -570 -50 -528Z`,
    pony:`M-48 -532 Q-50 -598 0 -598 Q50 -598 48 -532 Q38 -566 6 -568 Q-30 -566 -48 -532Z`};
  let back='';
  if(c.style==='bob')back=`<path d="M-58 -540 Q-60 -606 0 -608 Q60 -606 58 -540 L60 -470 Q44 -462 36 -484 L-36 -484 Q-44 -462 -60 -470Z" fill="${c.hair}"/>`;
  if(c.style==='pony')back=`<ellipse cx="52" cy="-540" rx="20" ry="40" fill="${c.hair}" transform="rotate(${18+Math.sin(t*5)*6} 46 -570)"/><circle cx="44" cy="-572" r="9" fill="${T}"/>`;
  const eyeRy=blink?1:6.5;
  const brow=mood==='worry'?`<path d="M-26 -546 l15 -6 M26 -546 l-15 -6" stroke="${c.hair}" stroke-width="5" stroke-linecap="round"/>`:`<path d="M-26 -547 q9 -6 18 -1 M26 -547 q-9 -6 -18 -1" stroke="${c.hair}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  const mouth=mood==='worry'?`<path d="M-11 -496 q11 -7 22 0" stroke="#7a3b2e" stroke-width="4.5" fill="none" stroke-linecap="round"/>`
    :mood==='happy'?`<path d="M-15 -503 q15 0 30 0 q-2 17 -15 17 q-13 0 -15 -17z" fill="#8a3a2e"/><path d="M-9 -490 q9 5 18 0" stroke="#e97a6a" stroke-width="5" stroke-linecap="round"/>`
    :`<path d="M-13 -501 q13 11 26 0" stroke="#7a3b2e" stroke-width="4.5" fill="none" stroke-linecap="round"/>`;
  const glasses=c.glasses?`<g fill="none" stroke="#2b2b33" stroke-width="3.5"><rect x="-31" y="-534" width="25" height="20" rx="7"/><rect x="6" y="-534" width="25" height="20" rx="7"/><path d="M-6 -526 h12"/></g>`:'';
  return `${back}<rect x="-13" y="-486" width="26" height="40" rx="10" fill="${c.skin}"/><rect x="-13" y="-486" width="26" height="16" fill="#000" opacity=".08"/>
  <circle cx="-45" cy="-524" r="10" fill="${c.skin}"/><circle cx="45" cy="-524" r="10" fill="${c.skin}"/>
  <ellipse cx="0" cy="-530" rx="45" ry="54" fill="${c.skin}"/><path d="M20 -578 Q46 -560 44 -520 Q40 -488 14 -478 Q36 -510 20 -578Z" fill="#000" opacity=".05"/>
  <path d="${hb[c.style]}" fill="${c.hair}"/>
  ${brow}<ellipse cx="-17" cy="-524" rx="5" ry="${eyeRy}" fill="#2b2b33"/><ellipse cx="17" cy="-524" rx="5" ry="${eyeRy}" fill="#2b2b33"/>
  <circle cx="-27" cy="-507" r="8" fill="#ef8b78" opacity=".28"/><circle cx="27" cy="-507" r="8" fill="#ef8b78" opacity=".28"/>
  <path d="M0 -518 q-5 11 3 13" stroke="${mix(c.skin,'#7a4a33',.45)}" stroke-width="3.5" fill="none" stroke-linecap="round"/>${mouth}${glasses}`;
}
function person(x,y,s,o){
  const c=CAST[o.c||'owner'],t=o.t||0,pose=o.pose||'stand',mood=o.mood||'smile';
  const walk=pose==='walk',bob=walk?-Math.abs(Math.sin(t*9))*10:Math.sin(t*3)*2.5;
  const lg=walk?Math.sin(t*9)*16:0;
  const leg=(side,ang)=>`<g transform="rotate(${ang} ${side*20} -250)"><path d="M${side*4} -252 L${side*40} -252 L${side*36} -22 L${side*12} -22Z" fill="${c.pants}"/><path d="M${side*24} -252 L${side*40} -252 L${side*36} -22 L${side*28} -22Z" fill="#000" opacity="${side>0?.1:0}"/><path d="M${side*8} -26 h${side*34} q${side*20} 0 ${side*20} 18 v8 h${side*-54}z" fill="${c.shoes}"/></g>`;
  const [Lh,Rh]=POSES[pose](t);
  let torso;
  if(c.jacket){
    torso=`<path d="M-34 -460 L34 -460 L30 -258 L-30 -258Z" fill="${c.inner}"/>
    <path d="M-66 -456 Q-78 -452 -78 -430 L-66 -250 L-6 -250 L-6 -330 L-30 -462Z" fill="${c.top}"/><path d="M66 -456 Q78 -452 78 -430 L66 -250 L6 -250 L6 -330 L30 -462Z" fill="${c.top2}"/>
    <path d="M-30 -462 L-6 -330 L-22 -400 L-42 -430Z" fill="${c.top2}" opacity=".7"/><path d="M30 -462 L6 -330 L22 -400 L42 -430Z" fill="#000" opacity=".12"/>
    <path d="M-20 -466 L0 -440 L20 -466 L12 -472 L0 -456 L-12 -472Z" fill="${c.inner}"/>`;
  }else{
    torso=`<path d="M-62 -458 Q-76 -454 -76 -432 L-64 -250 L64 -250 L76 -432 Q76 -454 62 -458Z" fill="${c.top}"/><path d="M4 -458 L62 -458 Q76 -454 76 -432 L64 -250 L4 -250Z" fill="${c.top2}" opacity=".55"/>
    <path d="M-64 -270 h128 v20 h-128z" fill="#000" opacity=".1"/><path d="M-24 -464 L0 -436 L24 -464 L14 -472 L0 -452 L-14 -472Z" fill="${c.collar}"/>`;
  }
  const tag=c.tag||o.tag?`<g transform="translate(-58,-404)"><rect width="52" height="22" rx="5" fill="#fff"/><text x="26" y="16" text-anchor="middle" font-size="13" font-weight="900" fill="${DG}">アキヤド</text></g>`:'';
  return `<g transform="translate(${x},${y+bob*s}) scale(${o.flip?-s:s},${s})">
  <ellipse cx="0" cy="${-bob+4}" rx="92" ry="14" fill="#000" opacity=".13"/>
  ${leg(-1,lg)}${leg(1,-lg)}
  <rect x="-62" y="-272" width="124" height="26" rx="8" fill="${c.pants}"/>
  ${torso}${tag}
  ${head(c,mood,t,o.seed||0)}
  ${arm(c,-1,Lh[0],Lh[1])}${arm(c,1,Rh[0],Rh[1])}</g>`;
}
// ---------- 建物・小物 ----------
function house(x,y,s,k){ // k:0=古い空き家 1=再生した宿
  const wall=mix('#b9a58f','#fbf1dc',k),wall2=mix('#a6927d','#efe2c6',k),roof=mix('#6d625a',T,k),roof2=mix('#5e544d','#a94a2a',k),door=mix('#6a5646',G,k),win=mix('#8d99a0',Y,k);
  const cracks=k<.99?`<g opacity="${1-k}" stroke="#4d4136" stroke-width="5" fill="none"><path d="M-110 -250 l22 36 l-18 30 l24 40"/><path d="M70 -300 l-16 30 l20 24"/></g>`:'';
  const boards=k<.99?`<g opacity="${1-k}"><rect x="-128" y="-228" width="76" height="14" fill="#7a6a58" transform="rotate(-12 -90 -220)"/><rect x="-128" y="-196" width="76" height="14" fill="#7a6a58" transform="rotate(10 -90 -190)"/></g>`:'';
  const grass=k<.99?`<g opacity="${1-k}" fill="#7d9a5f"><path d="M-200 0 l10 -50 l10 50z M-170 0 l14 -64 l12 64z M140 0 l10 -48 l10 48z M180 0 l12 -60 l12 60z"/></g>`:'';
  const glow=k>.01?`<circle cx="-90" cy="-202" r="${70*k}" fill="${Y}" opacity="${.25*k}"/>`:'';
  const flag=k>.6?`<g opacity="${(k-.6)/.4}"><rect x="108" y="-470" width="6" height="90" fill="${DG}"/><path d="M114 -470 h70 l-16 22 l16 22 h-70z" fill="${T}"/></g>`:'';
  const plants=k>.5?`<g opacity="${(k-.5)/.5}"><rect x="-74" y="-40" width="30" height="40" rx="6" fill="#8a5a3c"/><circle cx="-59" cy="-52" r="22" fill="#4f9a66"/><rect x="44" y="-40" width="30" height="40" rx="6" fill="#8a5a3c"/><circle cx="59" cy="-52" r="22" fill="#4f9a66"/><path d="M-40 -0 h80 v-10 h-80z" fill="#d9cbb0"/></g>`:'';
  return `<g transform="translate(${x},${y}) scale(${s})">
  <ellipse cx="0" cy="10" rx="260" ry="20" fill="#000" opacity=".12"/>
  <rect x="-190" y="-300" width="380" height="300" rx="10" fill="${wall}"/><rect x="40" y="-300" width="150" height="300" fill="${wall2}"/>
  <path d="M-230 -296 L0 -470 L230 -296z" fill="${roof}"/><path d="M0 -470 L230 -296 L150 -296 Z" fill="${roof2}"/><rect x="-236" y="-306" width="472" height="18" rx="8" fill="${roof2}"/>
  <rect x="-128" y="-240" width="76" height="76" rx="8" fill="${win}"/><rect x="52" y="-240" width="76" height="76" rx="8" fill="${win}"/>
  <path d="M-90 -240 v76 M-128 -202 h76 M90 -240 v76 M52 -202 h76" stroke="${wall}" stroke-width="5"/>
  <rect x="-34" y="-190" width="68" height="190" rx="10" fill="${door}"/><circle cx="18" cy="-98" r="6" fill="#f0e2c6"/>
  ${glow}${cracks}${boards}${grass}${flag}${plants}</g>`;
}
const coin=(x,y,r=34)=>`<g transform="translate(${x},${y})"><circle r="${r}" fill="#e8b950"/><circle r="${r}" fill="none" stroke="#d09a2f" stroke-width="${r*.12}"/><circle r="${r*.72}" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/><text y="${r*.36}" text-anchor="middle" font-size="${r*1.05}" font-weight="900" fill="#fff">¥</text></g>`;
const q=(x,y,s,t,ph)=>`<text x="${x}" y="${y+Math.sin(t*4+ph)*10}" font-size="${s}" font-weight="900" fill="${T}" text-anchor="middle" stroke="#fff" stroke-width="8" paint-order="stroke" transform="rotate(${Math.sin(t*3+ph)*8} ${x} ${y})">？</text>`;
const sparkle=(x,y,s,t,ph)=>{const a=.5+.5*Math.sin(t*5+ph);return `<path transform="translate(${x},${y}) scale(${s*(.6+.4*a)})" d="M0 -30 L8 -8 L30 0 L8 8 L0 30 L-8 8 L-30 0 L-8 -8z" fill="#fff6c9" stroke="${Y}" stroke-width="4" opacity="${.5+.5*a}"/>`};
const LOGO=(x,y,s)=>`<g transform="translate(${x},${y}) scale(${s})"><rect width="64" height="64" rx="18" fill="${G}"/><path d="M15 31 L32 17 L49 31 V48 a2.6 2.6 0 0 1 -2.6 2.6 H37 V39 H27 V50.6 H17.6 A2.6 2.6 0 0 1 15 48z" fill="#fff"/><text x="84" y="46" font-size="46" font-weight="900" fill="${DG}" letter-spacing="6">アキヤド</text></g>`;
const MARK=(x,y,s)=>`<g transform="translate(${x},${y}) scale(${s}) translate(-32,-32)"><rect width="64" height="64" rx="18" fill="${G}"/><path d="M15 31 L32 17 L49 31 V48 a2.6 2.6 0 0 1 -2.6 2.6 H37 V39 H27 V50.6 H17.6 A2.6 2.6 0 0 1 15 48z" fill="#fff"/></g>`;
// ---------- 背景（場面ごとの色の町並み。山・家並み・木を重ねて、ゆっくり流す） ----------
const THEMES={
  dusk:{sky:'#e4e1ef',sun:'#f6dccb',far:'#d2cce3',mid:'#c3bbd9',win:'#ece8f5',near:'#ab9fcb',gr:'#c0b6da',gr2:'#b1a5d0'},
  yellow:{sky:'#f6c45c',sun:'#fde6ad',far:'#f3bb52',mid:'#f8d27f',win:'#fbe3b0',near:'#e7a23a',gr:'#eeb04a',gr2:'#e5a23b'},
  mint:{sky:'#cdeedb',sun:'#f5fad6',far:'#b4e1c6',mid:'#a2d8b8',win:'#dcf3e5',near:'#82c59d',gr:'#9bd2b0',gr2:'#8bc8a3'},
  sky:{sky:'#cde5f6',sun:'#fff3cc',far:'#b6d5ee',mid:'#a3c8e6',win:'#e0eef9',near:'#7fb1d9',gr:'#a6cbe6',gr2:'#95bfdf'},
  peach:{sky:'#f8d4c4',sun:'#fff1dc',far:'#f3c1ad',mid:'#ecad94',win:'#fce3d8',near:'#df937a',gr:'#eaa992',gr2:'#e29a83'},
};
const TOWN=(()=>{let x=0,i=0,a=[];while(x<2400){const r=rnd(i++),w=r<.6?150+rnd(i++)*90:120+rnd(i++)*70,h=r<.6?110+rnd(i++)*80:230+rnd(i++)*150;a.push([x,w,h,r<.6?'house':'bldg']);x+=w+10+rnd(i++)*40}return a})();
const TREES=(()=>{let x=40,i=99,a=[];while(x<2400){a.push([x,60+rnd(i++)*50,0.8+rnd(i++)*0.5]);x+=170+rnd(i++)*240}return a})();
function bg(t,th){
  const c=THEMES[th];let s=`<rect width="1920" height="1080" fill="${c.sky}"/><circle cx="1520" cy="250" r="150" fill="${c.sun}" opacity=".9"/>`;
  const cl=(x,y,sc,sp)=>`<g transform="translate(${((x+t*sp)%2400)-240},${y}) scale(${sc})" fill="#fff" opacity=".75"><ellipse cx="0" cy="0" rx="90" ry="30"/><ellipse cx="55" cy="-18" rx="60" ry="32"/><ellipse cx="-50" cy="-10" rx="50" ry="26"/></g>`;
  s+=cl(200,220,1.2,14)+cl(980,150,.9,9)+cl(1650,320,1.4,12);
  s+=`<path d="M0 640 Q220 470 470 600 Q700 420 980 590 Q1240 450 1500 580 Q1720 470 1920 560 V900 H0Z" fill="${c.far}"/>`;
  const off=-(t*10)%2400;let town='';
  [0,2400].forEach(o=>TOWN.forEach(([x,w,h,k])=>{const X=x+o+off;if(X>1940||X+w<-20)return;const top=GROUND-h;
    if(k==='house'){town+=`<rect x="${X}" y="${top}" width="${w}" height="${h}" fill="${c.mid}"/><path d="M${X-14} ${top+4} L${X+w/2} ${top-w*.38} L${X+w+14} ${top+4}Z" fill="${c.mid}"/>`;
      for(let j=0;j<2;j++)town+=`<rect x="${X+w*.18+j*w*.42}" y="${top+h*.28}" width="${w*.22}" height="${Math.min(40,h*.26)}" rx="4" fill="${c.win}"/>`;}
    else{town+=`<rect x="${X}" y="${top}" width="${w}" height="${h}" rx="6" fill="${c.mid}"/>`;
      for(let r=0;r<Math.floor((h-40)/52);r++)for(let q2=0;q2<Math.floor((w-24)/40);q2++)town+=`<rect x="${X+20+q2*40}" y="${top+26+r*52}" width="22" height="28" rx="3" fill="${c.win}"/>`;}
  }));
  s+=town;
  const off2=-(t*22)%2400;let tr='';
  [0,2400].forEach(o=>TREES.forEach(([x,h,sc])=>{const X=x+o+off2;if(X>1980||X<-80)return;
    tr+=`<g transform="translate(${X},${GROUND}) scale(${sc})"><rect x="-7" y="${-h-20}" width="14" height="${h+20}" rx="5" fill="${mix(c.near,'#000000',.25)}"/><circle cx="0" cy="${-h-40}" r="44" fill="${c.near}"/><circle cx="-30" cy="${-h-14}" r="32" fill="${c.near}"/><circle cx="30" cy="${-h-18}" r="34" fill="${c.near}"/><circle cx="-12" cy="${-h-58}" r="18" fill="#fff" opacity=".12"/></g>`;}));
  s+=tr;
  s+=`<rect y="${GROUND}" width="1920" height="${1080-GROUND}" fill="${c.gr}"/><rect y="${GROUND}" width="1920" height="12" fill="${c.gr2}"/>`;
  for(let j=0;j<8;j++){const X=((j*300-t*40)%2400+2400)%2400-200;s+=`<rect x="${X}" y="${GROUND+60}" width="120" height="10" rx="5" fill="${c.gr2}"/>`}
  return s;
}
// ---------- 図解の部品 ----------
const pop=(cx,cy,p,inner)=>{const o=clamp(p*3);if(o<=0)return '';const s=bk(p);return `<g opacity="${o}" transform="translate(${cx},${cy}) scale(${s}) translate(${-cx},${-cy})">${inner}</g>`};
const fade=(p,inner,dy=30)=>{const o=eo(p);if(o<=0)return '';return `<g opacity="${o}" transform="translate(0,${(1-o)*dy})">${inner}</g>`};
const TX=(x,y,s,fs,c=DG,w=900,a='middle')=>`<text x="${x}" y="${y}" text-anchor="${a}" font-size="${fs}" font-weight="${w}" fill="${c}">${s}</text>`;
const box=(x,y,w,h,rx=24,fill='#fff')=>`<rect x="${x}" y="${y+8}" width="${w}" height="${h}" rx="${rx}" fill="#000" opacity=".1"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}"/>`;
function arrow(x1,y1,x2,y2,p,c=T,w=10){
  if(p<=0)return '';const k=clamp(p),x=x1+(x2-x1)*k,y=y1+(y2-y1)*k,a=Math.atan2(y2-y1,x2-x1)*180/Math.PI;
  return `<path d="M${x1} ${y1} L${x} ${y}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`+(k>.85?`<path transform="translate(${x},${y}) rotate(${a})" d="M-24 -17 L2 0 L-24 17" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="${(k-.85)/.15}"/>`:'');
}
const ICON={
  chat:c=>`<path d="M-34 -28 h68 a10 10 0 0 1 10 10 v34 a10 10 0 0 1 -10 10 h-34 l-20 18 v-18 h-14 a10 10 0 0 1 -10 -10 v-34 a10 10 0 0 1 10 -10z" fill="${c}"/><circle cx="-16" cy="-1" r="5" fill="#fff"/><circle cx="0" cy="-1" r="5" fill="#fff"/><circle cx="16" cy="-1" r="5" fill="#fff"/>`,
  search:c=>`<circle cx="-8" cy="-8" r="22" fill="none" stroke="${c}" stroke-width="10"/><path d="M9 9 L30 30" stroke="${c}" stroke-width="12" stroke-linecap="round"/>`,
  key:c=>`<circle cx="-18" cy="0" r="16" fill="none" stroke="${c}" stroke-width="9"/><path d="M-2 0 h38 M24 0 v14 M35 0 v10" stroke="${c}" stroke-width="9" stroke-linecap="round"/>`,
  doc:c=>`<rect x="-26" y="-34" width="52" height="66" rx="6" fill="${c}"/><path d="M-14 -16 h28 M-14 -1 h28 M-14 14 h18" stroke="#fff" stroke-width="6" stroke-linecap="round"/>`,
  yen:c=>`<circle r="32" fill="${c}"/><text y="14" text-anchor="middle" font-size="40" font-weight="900" fill="${c==='#fff'?G:'#fff'}">¥</text>`,
  check:c=>`<path d="M-26 0 l16 16 l34 -36" stroke="${c}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
  chart:c=>`<path d="M-34 30 H34" stroke="${c}" stroke-width="7" stroke-linecap="round"/><rect x="-28" y="4" width="14" height="22" rx="3" fill="${c}"/><rect x="-7" y="-10" width="14" height="36" rx="3" fill="${c}"/><rect x="14" y="-28" width="14" height="54" rx="3" fill="${c}"/>`,
  hammer:c=>`<path d="M-4 -6 L-34 30" stroke="${c}" stroke-width="12" stroke-linecap="round"/><path d="M-8 -36 L24 -4 L34 -14 L2 -46Z" fill="${c}"/>`,
  home:c=>`<path d="M-34 -2 L0 -32 L34 -2 V32 H-34Z" fill="${c}"/><rect x="-10" y="8" width="20" height="24" fill="#fff"/>`,
};
const icon=(x,y,r,name,bgc,fc='#fff',s=1)=>`<g transform="translate(${x},${y})"><circle r="${r}" fill="${bgc}"/><g transform="scale(${s})">${ICON[name](fc)}</g></g>`;
function node(id,x,y,r,inner,label,p,ring,labelY){
  const ly=labelY??(y+r+22);
  return pop(x,y,p,`<circle cx="${x}" cy="${y+8}" r="${r+8}" fill="#000" opacity=".1"/><circle cx="${x}" cy="${y}" r="${r+8}" fill="${ring}"/><clipPath id="${id}"><circle cx="${x}" cy="${y}" r="${r}"/></clipPath><circle cx="${x}" cy="${y}" r="${r}" fill="#fff"/><g clip-path="url(#${id})">${inner}</g>${box(x-label.length*21-30,ly,label.length*42+60,62,31)}${TX(x,ly+45,label,40)}`);
}
const face=(id,x,y,r,c,ring,mood='smile',t=0)=>`<circle cx="${x}" cy="${y}" r="${r+7}" fill="${ring}"/><clipPath id="${id}"><circle cx="${x}" cy="${y}" r="${r}"/></clipPath><circle cx="${x}" cy="${y}" r="${r}" fill="#fff"/><g clip-path="url(#${id})">${person(x,y-r*.12+525*r/88,r/88,{c,mood,t})}</g>`;
const chip=(x,y,s,fs,bgc,fc,p)=>{const w=s.length*fs+fs*1.2,h=fs*1.8;return pop(x,y,p,`<rect x="${x-w/2}" y="${y-h/2+5}" width="${w}" height="${h}" rx="${h/2}" fill="#000" opacity=".1"/><rect x="${x-w/2}" y="${y-h/2}" width="${w}" height="${h}" rx="${h/2}" fill="${bgc}"/>${TX(x,y+fs*.36,s,fs,fc)}`)};
const pill=(txt,p,w)=>pop(960,253,p,`<rect x="${960-w/2}" y="218" width="${w}" height="76" rx="38" fill="${T}"/><text x="960" y="272" text-anchor="middle" font-size="46" font-weight="900" fill="#fff" letter-spacing="3">${txt}</text>`);
function caption(txt,p,y=56,fs=72){ // 上の見出し（白い丸みのある帯）
  const w=txt.length*fs*1.0+120,h=fs*1.7,x=960-w/2;
  return pop(960,y+h/2,p,`<rect x="${x}" y="${y+9}" width="${w}" height="${h}" rx="${h/2}" fill="#000" opacity=".13"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h/2}" fill="#fff"/><text x="960" y="${y+h/2+fs*.35}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="#14202a" letter-spacing="2">${txt}</text>`);
}
function sub(lines,p){ // 下の字幕
  const o=clamp(p*3),n=lines.length,fs=44,h=n*fs*1.5+34,w=1500;
  return `<g opacity="${o}" transform="translate(0,${(1-eo(p))*30})"><rect x="${960-w/2}" y="${1045-h}" width="${w}" height="${h}" rx="22" fill="${DG}" opacity=".93"/>${lines.map((l,i)=>`<text x="960" y="${1045-h+17+fs*1.2+i*fs*1.5}" text-anchor="middle" font-size="${fs}" font-weight="700" fill="#fff" letter-spacing="1.5">${l}</text>`).join('')}</g>`;
}
const AV=[1,2,3,6,4,5];
const SC=__SC__;
const THEME=['dusk','dusk','yellow','mint','sky','yellow','mint','peach','sky','yellow'];
// ---------- 場面 ----------
function scene(i,t,lt){
  let s='';
  if(i===0){ // つかみ：見る人の悩み
    s+=house(1260,GROUND,1.05,0);
    s+=person(600,GROUND,.92,{c:'owner',pose:'think',mood:'worry',t:lt});
    s+=[[440,430,90,0],[760,380,70,1.5],[1010,330,80,3]].map(([x,y,z,ph],k)=>pop(x,y-30,seg(lt,.6+k*.3,1.2+k*.3),q(x,y,z,lt,ph))).join('');
    s+=caption('その空き家、このままで大丈夫？',seg(lt,.1,.7));
    s+=sub(['相続した実家、遠くて通えない。','売るか、貸すか、決められないまま…。'],seg(lt,1.4,2.1));
  }
  if(i===1){ // 放置するほど負担が増える
    s+=house(700,GROUND,.78,0);
    s+=person(290,GROUND,.86,{c:'owner',pose:'think',mood:'worry',t:lt});
    const pp=seg(lt,.2,.8);
    let g=`${box(1060,250,780,560,28)}${TX(1450,320,'空き家を放置すると…',42)}
      <path d="M1140 750 H1780 M1140 750 V380" stroke="#9fb5a8" stroke-width="6" stroke-linecap="round"/>${TX(1780,792,'年数 →',28,'#5d7366',700,'end')}${TX(1124,392,'負担',28,'#5d7366',700,'end')}`;
    const k=eo(seg(lt,1.2,3.4)),N=40;let d='';
    for(let j=0;j<=N;j++){const u=j/N*k;d+=(j?'L':'M')+(1150+600*u)+' '+(735-300*u*u)+' '}
    g+=`<path d="${d} L${1150+600*k} 750 L1150 750Z" fill="${T}" opacity=".12"/><path d="${d}" stroke="${T}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
    g+=[[.3,'固定資産税'],[.6,'草刈り・管理'],[.9,'建物の傷み']].map(([u,l],j)=>chip(1150+600*u,735-300*u*u-62,l,30,T,'#fff',seg(lt,2.2+j*.7,2.8+j*.7))).join('');
    s+=pop(1450,530,pp,g);
    s+=caption('放置するほど、負担は増える',seg(lt,.1,.7));
    s+=sub(['固定資産税、草刈り、建物の傷み。','使っていない間も、費用と手間はかかり続けます。'],seg(lt,2.4,3.1));
  }
  if(i===2){ // 見方を変える：古い家が宿に
    const k=eo(seg(lt,1,2.8));
    s+=house(880,GROUND,1.0,k);
    s+=[[700,420,1.2,0],[1080,380,1.4,1],[1000,560,.9,2]].map(([x,y,z,ph])=>`<g opacity="${k}">${sparkle(x,y,z,lt,ph)}</g>`).join('');
    const w=eo(seg(lt,2.6,4.4)),walking=lt>2.6&&lt<4.4;
    s+=person(1820-w*330,GROUND,.84,{c:'guest1',pose:walking?'walk':'wave',t:lt,flip:true,seed:1});
    s+=person(1660-w*290,GROUND,.78,{c:'guest2',pose:walking?'walk':'stand',t:lt+.3,flip:true,mood:'happy',seed:2});
    s+=chip(1440,300,'旅行者が泊まりに来る',34,'#3d6a8a','#fff',seg(lt,3.6,4.2));
    s+=person(300,GROUND,.9,{c:'owner',pose:lt>4.5?'cheer':'stand',mood:lt>4.5?'happy':'smile',t:lt});
    s+=arrow(650,560,450,560,eo(seg(lt,4.4,5)),T,10)+`<g opacity="${eo(seg(lt,4.5,5.1))}">${coin(550,500-Math.abs(Math.sin(lt*4))*14,30)}</g>`;
    s+=chip(330,215,'家が、収入を生む',34,T,'#fff',seg(lt,4.8,5.4));
    s+=caption('古い空き家が、宿に変わる',seg(lt,.1,.7));
    s+=sub(['観光地でなくても、収益物件になり得ます。'],seg(lt,1.6,2.3));
  }
  if(i===3){ // 自分ごとにする
    s+=person(250,GROUND,.84,{c:'owner',pose:'think',mood:'smile',t:lt});
    const rows=[[300,'売りたい','アキヤド買取プラン','宿の目線で、家を買い取る'],[530,'活かしたい','アキヤド借り上げプラン','家は持ったまま、毎月の家賃に'],[760,'宿をはじめたい','アキヤド開業・運営プラン','開業準備から運営まで伴走']];
    s+=pop(410,330,seg(lt,.5,1.1),`<circle cx="410" cy="330" r="16" fill="#fff"/><circle cx="440" cy="290" r="10" fill="#fff"/>`);
    rows.forEach(([y,a,b,c],k)=>{
      const st=1.2+k*.8;
      s+=arrow(470,520,600,y,eo(seg(lt,st,st+.5)),G,9);
      s+=chip(780,y,a,40,'#fff',DG,seg(lt,st+.4,st+1));
      s+=arrow(965,y,1030,y,eo(seg(lt,st+.7,st+1)),T,9);
      s+=fade(seg(lt,st+.9,st+1.5),`${box(1050,y-78,780,156,24)}<rect x="1050" y="${y-78}" width="18" height="156" rx="9" fill="${T}"/>${TX(1096,y-8,b,48,DG,900,'start')}${TX(1096,y+46,c,32,'#4a5a52',700,'start')}`,0);
    });
    s+=caption('あなたは、どれですか？',seg(lt,.1,.7));
  }
  if(i===4){ // 無料相談で比べられる
    const cols=[['hammer','解体する'],['yen','売る'],['key','活かす']];
    cols.forEach(([ic,n],k)=>{const x=480+k*480,p=seg(lt,.8+k*.4,1.4+k*.4);
      let g=`${box(x-210,250,420,480,30)}${icon(x,340,56,ic,G,'#fff',.85)}${TX(x,452,n,50)}`;
      ['かかる費用','入るお金','手間'].forEach((r,j)=>{const y=520+j*64,c=seg(lt,2.4+k*.25+j*.3,2.8+k*.25+j*.3);
        g+=`<rect x="${x-140}" y="${y-26}" width="280" height="52" rx="26" fill="${mix('#f1f4f2','#e3f1e8',c)}"/>`;
        g+=`<g opacity="${1-clamp(c*3)}">${TX(x-104,y+13,'？',34,T,900,'middle')}</g>${pop(x-104,y,c,icon(x-104,y,17,'check',G,'#fff',.38))}`;
        g+=TX(x-72,y+11,r,30,'#2c3a33',900,'start');});
      s+=pop(x,490,p,g);
    });
    s+=pop(960,800,seg(lt,5.4,6),`<rect x="430" y="768" width="1060" height="84" rx="42" fill="#000" opacity=".12"/><rect x="430" y="760" width="1060" height="84" rx="42" fill="${T}"/>${TX(960,816,'負担がいちばん小さい方法を、ご提案',44,'#fff')}`);
    s+=caption('無料相談で、比べられます',seg(lt,.1,.7));
    s+=sub(['現地と周辺の宿を調べ、改修費と見込める収入を試算します。'],seg(lt,1.8,2.5));
  }
  if(i===5){ // 借り上げのしくみ
    const A=[640,410],O=[250,740],Gu=[1030,740],R=74;
    const par=(P,Q,off,sh)=>{const dx=Q[0]-P[0],dy=Q[1]-P[1],L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L,nx=-uy*off,ny=ux*off;return [P[0]+ux*sh+nx,P[1]+uy*sh+ny,Q[0]-ux*sh+nx,Q[1]-uy*sh+ny]};
    const e1=par(O,A,-20,R+22),e4=par(A,O,-20,R+22),e2=par(A,Gu,-20,R+22),e3=par(Gu,A,-20,R+22);
    s+=box(110,250,1060,640,36,'rgba(255,255,255,.55)');
    s+=arrow(...e1,eo(seg(lt,1.6,2.4)),G,9)+arrow(...e2,eo(seg(lt,2.6,3.4)),G,9)+arrow(...e3,eo(seg(lt,3.6,4.4)),T,9)+arrow(...e4,eo(seg(lt,4.6,5.4)),T,9);
    s+=chip(330,520,'① 家を貸す',32,G,'#fff',seg(lt,2,2.5))+chip(960,520,'② 宿として運営',32,G,'#fff',seg(lt,3,3.5))+chip(820,700,'③ 宿泊料金',32,T,'#fff',seg(lt,4,4.5))+chip(460,700,'④ 毎月の家賃',32,T,'#fff',seg(lt,5,5.5));
    const coinOn=(E,st)=>{let o='';for(let c=0;c<3;c++){const p=((lt-st)/1.6+c/3)%1;if(lt>st)o+=`<g opacity="${Math.sin(p*Math.PI)}">${coin(E[0]+(E[2]-E[0])*p,E[1]+(E[3]-E[1])*p,22)}</g>`}return o};
    s+=coinOn(e3,4.4)+coinOn(e4,5.4);
    s+=node('nA',A[0],A[1],R,MARK(A[0],A[1],1.6),'アキヤド',seg(lt,.6,1.2),T,A[1]-R-82);
    s+=pop(O[0],O[1],seg(lt,.9,1.5),face('nO',O[0],O[1],R,'owner',G,'happy',lt))+fade(seg(lt,.9,1.5),box(O[0]-115,O[1]+R+20,230,62,31)+TX(O[0],O[1]+R+65,'オーナー様',40),0);
    s+=pop(Gu[0],Gu[1],seg(lt,1.2,1.8),face('nG',Gu[0],Gu[1],R,'guest1','#3d6a8a','smile',lt))+fade(seg(lt,1.2,1.8),box(Gu[0]-90,Gu[1]+R+20,180,62,31)+TX(Gu[0],Gu[1]+R+65,'ゲスト',40),0);
    s+=fade(seg(lt,5.6,6.2),TX(640,800,'家はオーナー様のまま',34,DG,900),10);
    const card=(y,name,l1,l2,p,rec)=>pop(1500,y+115,p,`${box(1200,y,640,230,26)}${rec?`<rect x="1200" y="${y}" width="640" height="12" rx="6" fill="${T}"/>`:''}${TX(1236,y+72,name,44,DG,900,'start')}${icon(1256,y+128,22,'check',G,'#fff',.5)}${TX(1292,y+139,l1,29,'#2c3a33',700,'start')}${icon(1256,y+186,22,'check',G,'#fff',.5)}${TX(1292,y+197,l2,29,'#2c3a33',700,'start')}`);
    s+=card(290,'アキヤドおまかせプラン','改修・家具の費用はアキヤドがほぼ負担','毎月、決まった額の家賃',seg(lt,6.4,7),true);
    s+=card(560,'アキヤド売上シェアプラン','補修・内装をアキヤドと共同出資','家賃＋売上に応じた上乗せ',seg(lt,7.1,7.7),false);
    s+=caption('家は持ったまま、毎月の収入に',seg(lt,.1,.7));
    s+=sub(['アキヤドが借り上げ、改修から宿の運営まで行います。'],seg(lt,1.8,2.5));
  }
  if(i===6){ // 開業・運営：分担表 → 手数料の例
    const ph=clamp((lt-6.2)/.5),gA=1-ph;
    if(gA>0){
      const cols=[['伴走コース','手数料：売上の10%'],['運営代行コース','手数料：売上の20%'],['共同出資コース','利益を出資の割合で分配']];
      const rows=['物件取得','改修・家具の費用','開業準備・許認可','集客・価格の調整','ゲスト対応・清掃'];
      const split=[['owner','owner','rivia','rivia','owner'],['owner','owner','rivia','rivia','rivia'],['share','share','rivia','rivia','rivia']];
      const CX=[850,1230,1610],CW=360,Y0=432,RH=74;
      let g=box(160,310,1640,560,30,'rgba(255,255,255,.7)');
      cols.forEach(([n,f],c)=>{g+=pop(CX[c],368,seg(lt,.6+c*.25,1.1+c*.25),`<rect x="${CX[c]-CW/2+6}" y="322" width="${CW-12}" height="96" rx="18" fill="${DG}"/>${TX(CX[c],362,n,36,'#fff')}${TX(CX[c],400,f,24,'#ffe2b8',700)}`)});
      rows.forEach((r,k)=>{const y=Y0+k*(RH+8);g+=fade(seg(lt,1.6+k*.35,2.1+k*.35),`<rect x="186" y="${y}" width="470" height="${RH}" rx="14" fill="#fff"/>${TX(210,y+49,r,34,DG,900,'start')}`,0);
        split.forEach((sp,c)=>{const w=sp[k],p=seg(lt,1.8+k*.35+c*.12,2.3+k*.35+c*.12);const bgc=w==='rivia'?G:w==='share'?Y:'#fff',fc=w==='rivia'?'#fff':DG,l=w==='rivia'?'アキヤド':w==='share'?'共同出資':'オーナー様';
          g+=pop(CX[c],y+RH/2,p,`<rect x="${CX[c]-CW/2+10}" y="${y}" width="${CW-20}" height="${RH}" rx="14" fill="${bgc}" ${w==='owner'?`stroke="#b9cfc1" stroke-width="3"`:''}/>${TX(CX[c],y+RH/2+12,l,32,fc)}`)})});
      s+=`<g opacity="${gA}">${g}</g>`;
    }
    if(ph>0){
      let g=box(260,330,1400,520,30)+TX(960,400,'例：売上が30万円のとき',46);
      [['伴走コース',.1,'27万円','3万円'],['運営代行コース',.2,'24万円','6万円']].forEach(([n,f,own,fee],k)=>{const y=450+k*170,X0=600,W=860,gp=eo(seg(lt,6.7+k*.5,7.5+k*.5)),sp=eo(seg(lt,7.8+k*.5,8.5+k*.5));
        g+=TX(X0-24,y+70,n,34,DG,900,'end');
        g+=`<rect x="${X0}" y="${y}" width="${W*gp}" height="110" rx="16" fill="${mix('#a9c4b2',G,sp)}"/>`;
        if(sp>0)g+=`<rect x="${X0+W*(1-f*sp)}" y="${y}" width="${W*f*sp}" height="110" rx="16" fill="${T}"/>`;
        g+=`<g opacity="${clamp(gp*2-1)*(1-sp)}">${TX(X0+W/2,y+70,'売上 30万円',40,'#fff')}</g>`;
        g+=`<g opacity="${sp}">${TX(X0+W*(1-f)/2,y+70,'手取り '+own,40,'#fff')}${TX(X0+W+20,y+46,'手数料',26,T,900,'start')}${TX(X0+W+20,y+88,fee,38,T,900,'start')}</g>`;
      });
      g+=fade(seg(lt,9.3,9.9),TX(960,810,'※ 金額はイメージです。清掃費などの実費は別途かかります。',28,'#4a5a52',700),0);
      s+=`<g opacity="${ph}">${g}</g>`;
    }
    s+=caption('副業で、宿をはじめたい方も',seg(lt,.1,.7),40,64);
    s+=pill('アキヤド開業・運営プラン',seg(lt,.4,1.0),700);
    s+=sub(['実際に宿を運営しているアキヤドが、','任せたい範囲に合わせて支えます。'],seg(lt,2,2.7));
  }
  if(i===7){ // 実績
    s+=person(1790,GROUND,.66,{c:'staff',pose:'point',t:lt,flip:true});
    s+=pop(530,560,seg(lt,.5,1.1),`${box(150,280,760,560,28)}<clipPath id="ph"><rect x="174" y="304" width="712" height="300" rx="18"/></clipPath><image href="file://__ROOT__/images/photos/node-shimoda.avif" x="174" y="304" width="712" height="300" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph)"/><rect x="194" y="322" width="200" height="44" rx="22" fill="${DG}"/>${TX(294,352,'運営施設の一例',24,'#fff')}${TX(196,664,'NODE Shimoda',44,DG,900,'start')}${TX(196,708,'静岡県下田市・空き家を改修した一棟貸しの宿',28,'#4a5a52',700,'start')}${TX(196,790,'★ 4.88',52,'#d9952c',900,'start')}${TX(400,788,'Airbnb評価（51件）',32,DG,700,'start')}`);
    s+=AV.map((n,k)=>{const p=bk(seg(lt,1.4+k*.18,2+k*.18)),x=1100+(k%3)*215,y=400+Math.floor(k/3)*215;return `<g transform="translate(${x},${y}) scale(${p})"><circle r="96" fill="#fff"/><clipPath id="c${k}"><circle r="86"/></clipPath><image href="file://__ROOT__/images/portraits/circle/user_0${n}.png" x="-86" y="-86" width="172" height="172" clip-path="url(#c${k})"/><circle r="86" fill="none" stroke="${T}" stroke-width="6"/></g>`}).join('');
    s+=chip(1315,790,'取材した6人のオーナーの事例も公開',30,'#fff',DG,seg(lt,2.6,3.2));
    s+=caption('宿を運営している、当事者です',seg(lt,.1,.7));
    s+=sub(['自ら宿を運営し、現場で確かめたノウハウでお手伝いします。'],seg(lt,2,2.7));
  }
  if(i===8){ // 不安を消す
    s+=person(270,GROUND,.86,{c:'staff',pose:'open',t:lt,mood:'happy'});
    const items=[['chat','相談・査定は無料','費用はかかりません'],['search','2営業日以内にご連絡','フォームは24時間受付'],['check','ご納得いただけた場合のみ契約','比べてから決められます']];
    items.forEach(([ic,a,b],k)=>{const y=350+k*160,p=seg(lt,.8+k*.6,1.4+k*.6);
      s+=pop(1140,y,p,`${box(560,y-64,1260,128,64)}${icon(640,y,48,ic,k===2?T:G,'#fff',.75)}${TX(716,y+15,a,44,DG,900,'start')}${TX(1780,y+12,b,28,'#4a5a52',700,'end')}`);
    });
    s+=caption('まだ決めていなくても、大丈夫',seg(lt,.1,.7));
    s+=sub(['売る・貸す・活かす、どれにするかは相談してから。'],seg(lt,2.6,3.3));
  }
  if(i===9){ // 最初の一歩：問い合わせフォーム
    const fields=[['お名前','山田 太郎',1.0,1.7],['電話番号','090-1234-5678',1.8,2.6],['メールアドレス','your@email.com',2.7,3.6],['お問い合わせ内容','相続した実家の活かし方を相談したい',3.7,5.0]];
    let f=`${box(110,230,820,680,30)}<rect x="110" y="230" width="820" height="80" rx="30" fill="${G}"/><rect x="110" y="270" width="820" height="40" fill="${G}"/>${TX(520,284,'お問い合わせ（無料）',36,'#fff')}`;
    const typed=(str,a,b)=>str.slice(0,Math.round(str.length*clamp((lt-a)/(b-a))));
    fields.forEach(([l,v,a,b],k)=>{const y=360+k*118,act=lt>=a&&lt<b+.2;
      f+=`${TX(160,y,l,28,DG,900,'start')}<rect x="${160+l.length*28+14}" y="${y-24}" width="52" height="30" rx="8" fill="${T}"/>${TX(160+l.length*28+40,y-2,'必須',18,'#fff')}<rect x="160" y="${y+16}" width="720" height="64" rx="14" fill="#f2f6f3" stroke="${act?G:'#b9cfc1'}" stroke-width="${act?5:3}"/>${TX(184,y+59,typed(v,a,b)+(act&&Math.floor(lt*3)%2?'｜':''),30,'#2c3a33',700,'start')}`});
    const press=lt>5.55&&lt<5.8?.94:1;
    f+=`<g transform="translate(520,860) scale(${press}) translate(-520,-860)"><rect x="350" y="822" width="340" height="76" rx="38" fill="${T}"/>${TX(520,872,'送信する',38,'#fff')}</g>`;
    const mv=eo(seg(lt,5.0,5.5)),cx=880-340*mv,cy=930-60*mv;
    f+=`<path transform="translate(${cx},${cy})" d="M0 0 L0 46 L12 34 L22 56 L32 51 L22 30 L38 30z" fill="#fff" stroke="${DG}" stroke-width="4" stroke-linejoin="round"/>`;
    if(lt>5.6)f+=pop(520,860,seg(lt,5.6,5.9),`<circle cx="520" cy="860" r="${40+(lt-5.6)*120}" fill="none" stroke="${Y}" stroke-width="6" opacity="${clamp(1-(lt-5.6)*1.5)}"/>`);
    s+=fade(seg(lt,.3,.9),f,30);
    s+=pop(1360,470,seg(lt,1.2,1.9),`${TX(1360,400,'まずは、無料でご相談ください',44)}<rect x="1060" y="448" width="600" height="110" rx="55" fill="#000" opacity=".12"/><rect x="1060" y="440" width="600" height="110" rx="55" fill="${T}"/><text x="1360" y="516" text-anchor="middle" font-size="60" font-weight="900" fill="#fff" letter-spacing="4">rivia-co.com</text>`);
    s+=`<g opacity="${eo(seg(lt,1.8,2.4))}">${LOGO(1180,610,1.2)}</g>`;
    s+=person(1790,GROUND,.62,{c:'staff',pose:lt>5.8?'cheer':'wave',mood:'happy',t:lt,flip:true});
    s+=caption('フォームから、無料でご相談',seg(lt,.1,.7));
    s+=sub(['まだ考えがまとまっていない段階でも構いません。'],seg(lt,2.2,2.9));
  }
  return s;
}
window.draw=function(t){
  let i=SC.findIndex(([a,b])=>t>=a&&t<b);if(i<0)i=SC.length-1;
  const a=SC[i][0],TR=.6;
  let out=`${bg(t,THEME[i])}${scene(i,t,t-a)}`;
  if(i>0&&t-a<TR){const k=eo((t-a)/TR),r=k*1150,pa=SC[i-1][0];
    out=`${bg(t,THEME[i-1])}${scene(i-1,t,t-pa)}<clipPath id="iris"><circle cx="960" cy="540" r="${r}"/></clipPath><g clip-path="url(#iris)">${out}</g><circle cx="960" cy="540" r="${r}" fill="none" stroke="#fff" stroke-width="${26*(1-k)}" opacity="${1-k}"/>`;}
  document.getElementById('s').innerHTML=out.replaceAll('__ROOT__',window.ROOT);
};
</script></body></html>""".replace("__SC__", json.dumps([list(x) for x in SC]))

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
            od = os.path.join(tempfile.gettempdir(), "explainer_preview"); os.makedirs(od, exist_ok=True)
            subprocess.run(["node", js, h, od, "preview", json.dumps(prev)], check=True, env=env); print("preview", od); return
        fr = os.path.join(tmp, "fr"); os.makedirs(fr)
        n = int(DUR * FPS)
        subprocess.run(["node", js, h, fr, "video", str(n)], check=True, env=env)
        import pop_audio
        events = [(SC[i][0] + dt, kind) for i, dt, kind in SFX]
        wav = os.path.join(tmp, "audio.wav"); pop_audio.write(wav, DUR, events)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%05d.jpg"), "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, DUR, "秒")


if __name__ == "__main__":
    main()
