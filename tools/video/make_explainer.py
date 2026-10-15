#!/usr/bin/env python3
"""アキヤドの、見た人が相談したくなる解説アニメ（約76秒・1920×1080・字幕つき・合成BGMつき）を作る。

- 絵はすべて、SVG の部品（人・家・お金・パソコンなど）を JS で組み、時刻 t ごとに描く（フラットなイラスト）。
- 各フレームを Playwright で画像にして、ffmpeg でつなぐ。BGM は tools/video/make_intro.py の合成を使う。
- 文言は、サイトに載っているサービスの説明と、取材事例の件数だけ。数字を作らない。
使い方: python3 tools/video/make_explainer.py [出力.mp4] [--preview 秒 ...]   # --preview は、その秒の静止画だけ書き出す
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FPS = 24
DUR = 76.0

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
  if(pose==='think'){arms=arm(-34,-200,-70,-110)+arm(34,-200,26,-238)}
  else if(pose==='cheer'){const w=Math.sin(t*6)*12;arms=arm(-34,-205,-95,-300+w)+arm(34,-205,95,-300-w)}
  else if(pose==='point'){arms=arm(-34,-200,-62,-110)+arm(34,-200,140,-250)}
  else if(pose==='type'){arms=arm(-34,-200,-20,-130)+arm(34,-200,40,-130)}
  else {arms=arm(-34,-200,-62,-110)+arm(34,-200,62,-110)}
  const mouth=(o.mood==='worry')?`<path d="M-14 -289 q14 -10 28 0" stroke="#7a3b2e" stroke-width="5" fill="none" stroke-linecap="round"/>`:`<path d="M-16 -294 q16 16 32 0" stroke="#7a3b2e" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  const brow=(o.mood==='worry')?`<path d="M-30 -324 l16 -7M30 -324 l-16 -7" stroke="${hair}" stroke-width="5" stroke-linecap="round"/>`:'';
  const tag=o.tag?`<g transform="translate(0,-170)"><rect x="-58" y="0" width="116" height="40" rx="10" fill="#fff" opacity=".95"/><text x="0" y="29" text-anchor="middle" font-size="26" font-weight="900" fill="${DG}">${o.tag}</text></g>`:'';
  return `<g transform="translate(${x},${y+bob}) scale(${o.flip?-s:s},${s})">
  <ellipse cx="0" cy="8" rx="95" ry="16" fill="#000" opacity=".12"/>
  <rect x="-38" y="-130" width="30" height="125" rx="14" fill="${pants}"/><rect x="8" y="-130" width="30" height="125" rx="14" fill="${pants}"/>
  <rect x="-13" y="-258" width="26" height="30" rx="10" fill="${SKIN}"/>
  <rect x="-48" y="-238" width="96" height="128" rx="34" fill="${sh}"/>
  <circle cx="0" cy="-300" r="52" fill="${SKIN}"/>
  <path d="M-54 -304 q4 -62 54 -62 q54 0 54 62 q-18 -34 -56 -36 q-38 0 -52 36z" fill="${hair}"/>
  <circle cx="-19" cy="-304" r="5.5" fill="#2b2b33"/><circle cx="19" cy="-304" r="5.5" fill="#2b2b33"/>${brow}${mouth}
  ${arms}
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
// ---------- 図解の部品 ----------
const pop=(cx,cy,p,inner)=>{const o=clamp(p*3);if(o<=0)return '';const s=bk(p);return `<g opacity="${o}" transform="translate(${cx},${cy}) scale(${s}) translate(${-cx},${-cy})">${inner}</g>`};
const fade=(p,inner,dy=30)=>{const o=eo(p);if(o<=0)return '';return `<g opacity="${o}" transform="translate(0,${(1-o)*dy})">${inner}</g>`};
const TX=(x,y,s,fs,c=DG,w=900,a='middle')=>`<text x="${x}" y="${y}" text-anchor="${a}" font-size="${fs}" font-weight="${w}" fill="${c}">${s}</text>`;
function arrow(x1,y1,x2,y2,p,c=T,w=10){
  if(p<=0)return '';const k=clamp(p),x=x1+(x2-x1)*k,y=y1+(y2-y1)*k,a=Math.atan2(y2-y1,x2-x1)*180/Math.PI;
  return `<path d="M${x1} ${y1} L${x} ${y}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`+(k>.85?`<path transform="translate(${x},${y}) rotate(${a})" d="M-24 -17 L2 0 L-24 17" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="${(k-.85)/.15}"/>`:'');
}
const ICON={
  chat:c=>`<path d="M-34 -28 h68 a10 10 0 0 1 10 10 v34 a10 10 0 0 1 -10 10 h-34 l-20 18 v-18 h-14 a10 10 0 0 1 -10 -10 v-34 a10 10 0 0 1 10 -10z" fill="${c}"/><circle cx="-16" cy="-1" r="5" fill="#fff"/><circle cx="0" cy="-1" r="5" fill="#fff"/><circle cx="16" cy="-1" r="5" fill="#fff"/>`,
  search:c=>`<circle cx="-8" cy="-8" r="22" fill="none" stroke="${c}" stroke-width="10"/><path d="M9 9 L30 30" stroke="${c}" stroke-width="12" stroke-linecap="round"/>`,
  scale:c=>`<path d="M0 -30 V30 M-24 32 h48 M-38 -22 h76" stroke="${c}" stroke-width="8" stroke-linecap="round" fill="none"/><path d="M-38 -22 l-15 30 h30z M38 -22 l-15 30 h30z" fill="${c}"/>`,
  key:c=>`<circle cx="-18" cy="0" r="16" fill="none" stroke="${c}" stroke-width="9"/><path d="M-2 0 h38 M24 0 v14 M35 0 v10" stroke="${c}" stroke-width="9" stroke-linecap="round"/>`,
  doc:c=>`<rect x="-26" y="-34" width="52" height="66" rx="6" fill="${c}"/><path d="M-14 -16 h28 M-14 -1 h28 M-14 14 h18" stroke="#fff" stroke-width="6" stroke-linecap="round"/>`,
  yen:c=>`<circle r="32" fill="${c}"/><text y="14" text-anchor="middle" font-size="40" font-weight="900" fill="${c==='#fff'?G:'#fff'}">¥</text>`,
  check:c=>`<path d="M-26 0 l16 16 l34 -36" stroke="${c}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
  chart:c=>`<path d="M-34 30 H34" stroke="${c}" stroke-width="7" stroke-linecap="round"/><rect x="-28" y="4" width="14" height="22" rx="3" fill="${c}"/><rect x="-7" y="-10" width="14" height="36" rx="3" fill="${c}"/><rect x="14" y="-28" width="14" height="54" rx="3" fill="${c}"/>`,
};
const icon=(x,y,r,name,bgc,fc='#fff',s=1)=>`<g transform="translate(${x},${y})"><circle r="${r}" fill="${bgc}"/><g transform="scale(${s})">${ICON[name](fc)}</g></g>`;
const bust=(x,y,s,sh,hair)=>`<g transform="translate(${x},${y}) scale(${s})"><path d="M-48 64 q0 -58 48 -58 q48 0 48 58z" fill="${sh}"/><circle cy="-22" r="30" fill="${SKIN}"/><path d="M-31 -24 q2 -36 31 -36 q31 0 31 36 q-10 -20 -32 -21 q-22 0 -30 21z" fill="${hair}"/><circle cx="-10" cy="-21" r="3.5" fill="#2b2b33"/><circle cx="10" cy="-21" r="3.5" fill="#2b2b33"/><path d="M-9 -9 q9 9 18 0" stroke="#7a3b2e" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>`;
const MARK=(x,y,s)=>`<g transform="translate(${x},${y}) scale(${s}) translate(-32,-32)"><rect width="64" height="64" rx="18" fill="${G}"/><path d="M15 31 L32 17 L49 31 V48 a2.6 2.6 0 0 1 -2.6 2.6 H37 V39 H27 V50.6 H17.6 A2.6 2.6 0 0 1 15 48z" fill="#fff"/></g>`;
function node(id,x,y,r,inner,label,p,ring,labelY){
  const ly=labelY??(y+r+22);
  return pop(x,y,p,`<circle cx="${x}" cy="${y}" r="${r+8}" fill="${ring}"/><clipPath id="${id}"><circle cx="${x}" cy="${y}" r="${r}"/></clipPath><circle cx="${x}" cy="${y}" r="${r}" fill="#fff"/><g clip-path="url(#${id})">${inner}</g><rect x="${x-label.length*21-30}" y="${ly}" width="${label.length*42+60}" height="62" rx="31" fill="#fff"/>${TX(x,ly+45,label,40)}`);
}
const chip=(x,y,s,fs,bgc,fc,p)=>{const w=s.length*fs+fs*1.2,h=fs*1.8;return pop(x,y,p,`<rect x="${x-w/2}" y="${y-h/2}" width="${w}" height="${h}" rx="${h/2}" fill="${bgc}"/>${TX(x,y+fs*.36,s,fs,fc)}`)};
const pill=(txt,p,w)=>`<g opacity="${eo(p)}"><rect x="${960-w/2}" y="210" width="${w}" height="86" rx="43" fill="${T}"/><text x="960" y="270" text-anchor="middle" font-size="52" font-weight="900" fill="#fff" letter-spacing="3">${txt}</text></g>`;
// ---------- 場面（見る人の悩み → 放置の負担 → 見方を変える → 自分ごと → 相談で分かること → しくみ → 実績 → 不安を消す → 最初の一歩） ----------
const SC=[[0,5],[5,12],[12,19],[19,26],[26,35],[35,45],[45,56],[56,62],[62,69],[69,76]];
function scene(i,t,lt){
  let s='';
  if(i===0){ // つかみ：見る人の悩み
    s+=house(1250,810,1.05,0,{});
    s+=person(560,800,1.25,{pose:'think',mood:'worry',t:lt,shirt:G});
    s+=[[430,500,90,0],[700,440,70,1.5],[960,380,80,3]].map(([x,y,z,ph],k)=>`<g opacity="${eo(seg(lt,.6+k*.3,1.2+k*.3))}">${q(x,y,z,lt,ph)}</g>`).join('');
    s+=caption('その空き家、このままで大丈夫？',seg(lt,.1,.7),70,80);
    s+=sub(['相続した実家、遠くて通えない。','売るか、貸すか、決められないまま…。'],seg(lt,1.4,2.1));
  }
  if(i===1){ // 放置するほど負担が増える
    s+=house(770,810,0.8,0,{});
    s+=person(330,800,1.15,{pose:'think',mood:'worry',t:lt,shirt:G});
    s+=[[200,470,80,0],[480,430,64,1.5]].map(([x,y,z,ph],k)=>`<g opacity="${eo(seg(lt,.6+k*.35,1.2+k*.35))}">${q(x,y,z,lt,ph)}</g>`).join('');
    const pp=eo(seg(lt,1.2,1.9));
    if(pp>0){
      s+=`<g opacity="${pp}" transform="translate(${(1-pp)*40},0)"><rect x="1090" y="290" width="740" height="520" rx="28" fill="#fff" opacity=".96"/>${TX(1460,362,'空き家を放置すると…',42)}
      <path d="M1170 750 H1770 M1170 750 V420" stroke="#9fb5a8" stroke-width="6" stroke-linecap="round"/>${TX(1770,792,'年数 →',28,'#5d7366',700,'end')}${TX(1150,430,'負担',28,'#5d7366',700,'end')}`;
      const k=eo(seg(lt,1.8,4.2)),N=40;let d='';
      for(let j=0;j<=N;j++){const u=j/N*k;d+=(j?'L':'M')+(1180+560*u)+' '+(735-280*u*u)+' '}
      s+=`<path d="${d}" stroke="${T}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      s+=[[.3,'固定資産税'],[.6,'草刈り・管理'],[.9,'建物の傷み']].map(([u,l],j)=>chip(1180+560*u,735-280*u*u-62,l,30,T,'#fff',seg(lt,2.2+j*.7,2.8+j*.7))).join('');
      s+='</g>';
    }
    s+=caption('放置するほど、負担は増える',seg(lt,.2,.9),70,80);
    s+=sub(['固定資産税、草刈り、建物の傷み。','使っていない間も、費用と手間はかかり続けます。'],seg(lt,2.4,3.1));
  }
  if(i===2){ // 見方を変える：古い家が宿に
    const k=eo(seg(lt,1,2.8));
    s+=house(860,810,1.0,k,{});
    s+=[[700,420,1.2,0],[1060,380,1.4,1],[980,560,.9,2]].map(([x,y,z,ph])=>`<g opacity="${k}">${sparkle(x,y,z,lt,ph)}</g>`).join('');
    const w=eo(seg(lt,2.6,4.2));
    s+=person(1780-w*360,800,1.0,{pose:'stand',t:lt,shirt:'#3d6a8a',hair:'#6b4a2e'})+person(1640-w*300,800,0.9,{pose:'stand',t:lt+.7,shirt:Y,hair:'#2b2b33'});
    s+=chip(1460,330,'旅行者が泊まりに来る',34,'#3d6a8a','#fff',seg(lt,3.6,4.2));
    s+=person(300,800,1.15,{pose:lt>4.4?'cheer':'stand',t:lt,shirt:G});
    s+=arrow(640,560,420,560,eo(seg(lt,4.4,5)),T,10)+`<g opacity="${eo(seg(lt,4.6,5.2))}">${coin(530,500,30)}</g>`;
    s+=chip(300,300,'家が、収入を生む',34,T,'#fff',seg(lt,4.8,5.4));
    s+=caption('古い空き家が、宿に変わる',seg(lt,.2,.9),70,80);
    s+=sub(['観光地でなくても、収益物件になり得ます。'],seg(lt,1.6,2.3));
  }
  if(i===3){ // 自分ごとにする
    s+=node('rt',300,560,110,bust(300,585,1.9,G,'#2b2b33'),'あなたの状況は？',seg(lt,.5,1.2),G);
    const rows=[[320,'売りたい','アキヤド買取プラン','宿の目線で、家を買い取る'],[560,'活かしたい','アキヤド借り上げプラン','家は持ったまま、毎月の家賃に'],[800,'宿をはじめたい','アキヤド開業・運営プラン','開業準備から運営まで伴走']];
    rows.forEach(([y,a,b,c],k)=>{
      const st=1.2+k*.8;
      s+=arrow(420,560,585,y,eo(seg(lt,st,st+.5)),G,9);
      s+=chip(770,y,a,40,'#fff',DG,seg(lt,st+.4,st+1));
      s+=arrow(950,y,1015,y,eo(seg(lt,st+.7,st+1)),T,9);
      s+=fade(seg(lt,st+.9,st+1.5),`<rect x="1040" y="${y-78}" width="760" height="156" rx="24" fill="#fff"/><rect x="1040" y="${y-78}" width="16" height="156" rx="8" fill="${T}"/>${TX(1086,y-8,b,48,DG,900,'start')}${TX(1086,y+46,c,32,'#4a5a52',700,'start')}`,0);
    });
    s+=caption('あなたは、どれですか？',seg(lt,.1,.8),70,76);
  }
  if(i===4){ // 無料相談で分かること：3つの道を比べる
    const cols=[['doc','解体する'],['yen','売る'],['key','活かす']];
    cols.forEach(([ic,n],k)=>{const x=480+k*480,p=seg(lt,.8+k*.4,1.4+k*.4);
      let g=`<rect x="${x-200}" y="300" width="400" height="430" rx="28" fill="#fff"/>${icon(x,390,58,ic,G,'#fff',.85)}${TX(x,500,n,48)}`;
      ['かかる費用','入るお金','手間'].forEach((r,j)=>{const y=560+j*54,c=seg(lt,2.4+k*.25+j*.3,2.8+k*.25+j*.3);
        g+=`${TX(x-150,y+12,r,30,'#2c3a33',700,'start')}<g opacity="${1-c}">${TX(x+150,y+12,'？',34,T,900,'end')}</g>${pop(x+132,y,c,icon(x+132,y,20,'check',G,'#fff',.45))}`});
      s+=fade(p,g,30);
    });
    const hl=seg(lt,5.4,6);
    s+=pop(960,800,hl,`<rect x="420" y="760" width="1080" height="84" rx="42" fill="${T}"/>${TX(960,816,'負担がいちばん小さい方法を、ご提案',44,'#fff')}`);
    s+=caption('無料相談で、比べられます',seg(lt,.2,.9),70,80);
    s+=sub(['現地と周辺の宿を調べ、改修費と見込める収入を試算します。'],seg(lt,1.8,2.5));
  }
  if(i===5){ // 借り上げ：しくみ図＋2つのプラン
    const A=[640,410],O=[250,740],Gu=[1030,740],R=74;
    const par=(P,Q,off,sh)=>{const dx=Q[0]-P[0],dy=Q[1]-P[1],L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L,nx=-uy*off,ny=ux*off;return [P[0]+ux*sh+nx,P[1]+uy*sh+ny,Q[0]-ux*sh+nx,Q[1]-uy*sh+ny]};
    const e1=par(O,A,-20,R+22),e4=par(A,O,-20,R+22),e2=par(A,Gu,-20,R+22),e3=par(Gu,A,-20,R+22);
    const a1=eo(seg(lt,1.6,2.4)),a2=eo(seg(lt,2.6,3.4)),a3=eo(seg(lt,3.6,4.4)),a4=eo(seg(lt,4.6,5.4));
    s+=arrow(...e1,a1,G,9)+arrow(...e2,a2,G,9)+arrow(...e3,a3,T,9)+arrow(...e4,a4,T,9);
    const lab=(x,y,l,c,p)=>chip(x,y,l,32,c,'#fff',p);
    s+=lab(330,520,'① 家を貸す',G,seg(lt,2,2.5))+lab(960,520,'② 宿として運営',G,seg(lt,3,3.5))+lab(820,700,'③ 宿泊料金',T,seg(lt,4,4.5))+lab(460,700,'④ 毎月の家賃',T,seg(lt,5,5.5));
    const coinOn=(E,st)=>{let o='';for(let c=0;c<3;c++){const p=((lt-st)/1.6+c/3)%1;if(lt>st)o+=`<g opacity="${Math.sin(p*Math.PI)}">${coin(E[0]+(E[2]-E[0])*p,E[1]+(E[3]-E[1])*p,22)}</g>`}return o};
    s+=coinOn(e3,4.4)+coinOn(e4,5.4);
    s+=node('nA',A[0],A[1],R,MARK(A[0],A[1],1.6),'アキヤド',seg(lt,.6,1.2),T,A[1]-R-82);
    s+=node('nO',O[0],O[1],R,bust(O[0],O[1]+18,1.25,G,'#2b2b33'),'オーナー様',seg(lt,.9,1.5),G);
    s+=node('nG',Gu[0],Gu[1],R,bust(Gu[0],Gu[1]+18,1.25,'#3d6a8a','#6b4a2e'),'ゲスト',seg(lt,1.2,1.8),'#3d6a8a');
    s+=fade(seg(lt,5.6,6.2),TX(640,800,'家はオーナー様のまま',34,DG,900),10);
    const card=(y,name,l1,l2,p,rec)=>fade(p,`<rect x="1170" y="${y}" width="660" height="230" rx="24" fill="#fff"/>${rec?`<rect x="1170" y="${y}" width="660" height="10" rx="5" fill="${T}"/>`:''}${TX(1205,y+70,name,44,DG,900,'start')}${icon(1225,y+125,22,'check',G,'#fff',.5)}${TX(1262,y+136,l1,29,'#2c3a33',700,'start')}${icon(1225,y+185,22,'check',G,'#fff',.5)}${TX(1262,y+196,l2,29,'#2c3a33',700,'start')}`,30);
    s+=card(300,'アキヤドおまかせプラン','改修・家具の費用はアキヤドがほぼ負担','毎月、決まった額の家賃',seg(lt,6.4,7),true);
    s+=card(570,'アキヤド売上シェアプラン','補修・内装をアキヤドと共同出資','家賃＋売上に応じた上乗せ',seg(lt,7.1,7.7),false);
    s+=caption('家は持ったまま、毎月の収入に',seg(lt,.2,.9),70,74);
    s+=sub(['アキヤドが借り上げ、改修から宿の運営まで行います。'],seg(lt,1.8,2.5));
  }
  if(i===6){ // 開業・運営：分担表 → 手数料の例
    const ph=clamp((lt-6.2)/.5),gA=1-ph;
    if(gA>0){
      const cols=[['伴走コース','手数料：売上の10%'],['運営代行コース','手数料：売上の20%'],['共同出資コース','利益を出資の割合で分配']];
      const rows=['物件取得','改修・家具の費用','開業準備・許認可','集客・価格の調整','ゲスト対応・清掃'];
      const split=[['owner','owner','rivia','rivia','owner'],['owner','owner','rivia','rivia','rivia'],['share','share','rivia','rivia','rivia']];
      const CX=[850,1230,1610],CW=360,Y0=432,RH=78;
      let g='';
      cols.forEach(([n,f],c)=>{g+=fade(seg(lt,.9+c*.25,1.4+c*.25),`<rect x="${CX[c]-CW/2}" y="318" width="${CW}" height="100" rx="18" fill="${DG}"/>${TX(CX[c],360,n,36,'#fff')}${TX(CX[c],400,f,24,'#ffe2b8',700)}`,10)});
      rows.forEach((r,k)=>{const y=Y0+k*(RH+8);g+=fade(seg(lt,1.6+k*.35,2.1+k*.35),`<rect x="190" y="${y}" width="460" height="${RH}" rx="14" fill="#fff" opacity=".7"/>${TX(214,y+51,r,34,DG,900,'start')}`,0);
        split.forEach((sp,c)=>{const w=sp[k],p=seg(lt,1.8+k*.35+c*.12,2.3+k*.35+c*.12);const bg=w==='rivia'?G:w==='share'?Y:'#fff',fc=w==='rivia'?'#fff':DG,l=w==='rivia'?'アキヤド':w==='share'?'共同出資':'オーナー様';
          g+=pop(CX[c],y+RH/2,p,`<rect x="${CX[c]-CW/2+8}" y="${y}" width="${CW-16}" height="${RH}" rx="14" fill="${bg}" ${w==='owner'?`stroke="#b9cfc1" stroke-width="3"`:''}/>${TX(CX[c],y+RH/2+12,l,32,fc)}`)})});
      s+=`<g opacity="${gA}">${g}</g>`;
    }
    if(ph>0){
      let g=TX(960,390,'例：売上が30万円のとき',46);
      const bars=[['伴走コース',.1,'27万円','3万円'],['運営代行コース',.2,'24万円','6万円']];
      bars.forEach(([n,f,own,fee],k)=>{const y=450+k*170,X0=560,W=1000,gp=eo(seg(lt,6.7+k*.5,7.5+k*.5)),sp=eo(seg(lt,7.8+k*.5,8.5+k*.5));
        g+=TX(X0-24,y+70,n,36,DG,900,'end');
        g+=`<rect x="${X0}" y="${y}" width="${W*gp}" height="110" rx="16" fill="${mix('#a9c4b2',G,sp)}"/>`;
        if(sp>0)g+=`<rect x="${X0+W*(1-f*sp)}" y="${y}" width="${W*f*sp}" height="110" rx="16" fill="${T}"/>`;
        g+=`<g opacity="${clamp(gp*2-1)*(1-sp)}">${TX(X0+W/2,y+70,'売上 30万円',40,'#fff')}</g>`;
        g+=`<g opacity="${sp}">${TX(X0+W*(1-f)/2,y+70,'手取り '+own,40,'#fff')}${TX(X0+W+24,y+48,'手数料',28,T,900,'start')}${TX(X0+W+24,y+90,fee,40,T,900,'start')}</g>`;
      });
      g+=fade(seg(lt,9.3,9.9),TX(960,820,'※ 金額はイメージです。清掃費などの実費は別途かかります。',30,'#4a5a52',700),0);
      s+=`<g opacity="${ph}">${g}</g>`;
    }
    s+=caption('副業で、宿をはじめたい方も',seg(lt,.2,.9),70,74);
    s+=pill('アキヤド開業・運営プラン',seg(lt,.6,1.2),800);
    s+=sub(['実際に宿を運営しているアキヤドが、','任せたい範囲に合わせて支えます。'],seg(lt,2,2.7));
  }
  if(i===7){ // 実績：自ら宿を運営する当事者
    s+=fade(seg(lt,.5,1.1),`<rect x="150" y="290" width="760" height="540" rx="28" fill="#fff"/><clipPath id="ph"><rect x="174" y="314" width="712" height="300" rx="18"/></clipPath><image href="file://__ROOT__/images/photos/node-shimoda.avif" x="174" y="314" width="712" height="300" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph)"/><rect x="194" y="332" width="200" height="44" rx="22" fill="${DG}"/>${TX(294,362,'運営施設の一例',24,'#fff')}${TX(196,674,'NODE Shimoda',44,DG,900,'start')}${TX(196,718,'静岡県下田市・空き家を改修した一棟貸しの宿',28,'#4a5a52',700,'start')}${TX(196,790,'★ 4.88',52,'#d9952c',900,'start')}${TX(400,788,'Airbnb評価（51件）',32,DG,700,'start')}`,30);
    s+=AV.map((n,k)=>{const p=bk(seg(lt,1.4+k*.18,2+k*.18)),x=1130+(k%3)*230,y=400+Math.floor(k/3)*230;return `<g transform="translate(${x},${y}) scale(${p})"><circle r="98" fill="#fff"/><clipPath id="c${k}"><circle r="88"/></clipPath><image href="file://__ROOT__/images/portraits/circle/user_0${n}.png" x="-88" y="-88" width="176" height="176" clip-path="url(#c${k})"/><circle r="88" fill="none" stroke="${T}" stroke-width="6"/></g>`}).join('');
    s+=fade(seg(lt,2.6,3.2),TX(1360,800,'取材した6人のオーナーの事例も公開',36),10);
    s+=caption('宿を運営している、当事者です',seg(lt,.2,.9),70,78);
    s+=sub(['自ら宿を運営し、現場で確かめたノウハウでお手伝いします。'],seg(lt,2,2.7));
  }
  if(i===8){ // 不安を消す
    const items=[['chat','相談・査定は無料','費用はかかりません'],['search','2営業日以内にご連絡','フォームは24時間受付'],['check','ご納得いただけた場合のみ契約','比べてから決められます']];
    items.forEach(([ic,a,b],k)=>{const y=350+k*160,p=seg(lt,.8+k*.6,1.4+k*.6);
      s+=fade(p,`<rect x="360" y="${y-62}" width="1200" height="128" rx="64" fill="#fff"/>${icon(440,y+2,48,ic,k===2?T:G,'#fff',.75)}${TX(520,y+16,a,44,DG,900,'start')}${TX(1520,y+14,b,30,'#4a5a52',700,'end')}`,0);
    });
    s+=caption('まだ決めていなくても、大丈夫',seg(lt,.2,.9),70,78);
    s+=sub(['売る・貸す・活かす、どれにするかは相談してから。'],seg(lt,2.6,3.3));
  }
  if(i===9){ // 最初の一歩：送るのは物件の場所と状況だけ
    const fp=seg(lt,.5,1.1);
    let f=`<rect x="150" y="270" width="780" height="580" rx="28" fill="#fff"/><rect x="150" y="270" width="780" height="76" rx="28" fill="${G}"/><rect x="150" y="310" width="780" height="36" fill="${G}"/>${TX(540,322,'お問い合わせ（無料）',36,'#fff')}`;
    const typed=(str,a,b)=>str.slice(0,Math.round(str.length*clamp((lt-a)/(b-a))));
    [['物件の場所','○○県○○市',1.3,2.2],['いまの状況','相続した実家。いまは空き家',2.4,3.6]].forEach(([l,v,a,b],k)=>{const y=400+k*150;
      f+=`${TX(200,y,l,32,DG,900,'start')}<rect x="200" y="${y+20}" width="680" height="78" rx="14" fill="#f2f6f3" stroke="#b9cfc1" stroke-width="3"/>${TX(226,y+72,typed(v,a,b),32,'#2c3a33',700,'start')}`});
    const press=lt>4.2&&lt<4.5?.94:1;
    f+=`<g transform="translate(540,770) scale(${press}) translate(-540,-770)"><rect x="360" y="728" width="360" height="84" rx="42" fill="${T}"/>${TX(540,784,'送信する',40,'#fff')}</g>`;
    const cx=lt<3.8?900:900-(360*eo(seg(lt,3.8,4.2))),cy=lt<3.8?860:860-(90*eo(seg(lt,3.8,4.2)));
    f+=`<path transform="translate(${cx},${cy})" d="M0 0 L0 46 L12 34 L22 56 L32 51 L22 30 L38 30z" fill="#fff" stroke="${DG}" stroke-width="4" stroke-linejoin="round"/>`;
    s+=fade(fp,f,30);
    s+=pop(1430,470,seg(lt,4.6,5.3),`${TX(1430,400,'まずは、無料でご相談ください',46)}<rect x="1130" y="440" width="600" height="110" rx="55" fill="${T}"/><text x="1430" y="516" text-anchor="middle" font-size="60" font-weight="900" fill="#fff" letter-spacing="4">rivia-co.com</text>`);
    s+=`<g opacity="${eo(seg(lt,5.2,5.8))}">${LOGO(1250,620,1.2)}</g>`;
    s+=caption('送るのは、物件の場所と状況だけ',seg(lt,.2,.9),70,78);
    s+=sub(['相談・お見積りは無料、全国対応です。'],seg(lt,2,2.7));
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
