#!/usr/bin/env python3
"""アキヤドの解説動画 第1回「民泊を資産に入れる5つの理由」（約8分・1920×1080）を作る。

- 話し手はアニメの民泊戦略家「アキ」。聞き手にユウタ（アキヤド劇場と同じキャラ）。型は docs/youtube/manual.md 1-2章。
- 数字の出どころ（説明欄にも書く）:
  訪日客 2024年3,687万人・2025年4,268万人（JNTO「訪日外客統計」）、2030年目標6,000万人と外国人宿泊の地方部33.7%（観光庁「観光立国推進基本計画（第5次）」「宿泊旅行統計調査 2025年確定値」）、
  空き家約900万戸・空き家率13.8%（総務省「令和5年住宅・土地統計調査」）、住宅宿泊事業の所得は原則雑所得（国税庁「住宅宿泊事業により生じる所得の課税関係等について（情報）」）、
  管理不全空家等の勧告で住宅用地特例が外れる（国土交通省・総務省）、営業日数は年180日以内（住宅宿泊事業法）。
  宿の数字は記事「不動産投資として見る小さな宿・民泊」と同じ、創業メンバーが運営する下田の宿の実績（試運転3か月。docs/brand/experience.md の確認済みの節）。
- 部品・書き出しは make_explainer.py / make_scam_ep1.py と共通。声は VOICEVOX（クレジットは最後の画面と説明欄）。
使い方: python3 tools/video/make_strategy_ep1.py [出力.mp4] [--hq] [--preview 秒 ...]
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import make_explainer as base
from make_scam_ep1 import wrap
from voicevox_tts import tts

FPS = 24
VOICES = {
    "A": dict(name="戦略家 アキ", style=13, speed=1.12, intonation=1.15, pitch=0.0),   # 青山龍星（ノーマル）
    "Y": dict(name="ユウタ", style=11, speed=1.08, intonation=1.15, pitch=0.0),        # 玄野武宏
}
MODELS = [4, 15]
CREDIT = "VOICEVOX:青山龍星　VOICEVOX:玄野武宏"
NOTE = "※ 情報提供を目的とした動画で、特定の投資を勧めるものではありません。数字は公表資料と、運営する宿の実績（一例）です。"

SCENES = [
    # 0 つかみ：結論 → 今日の5つ → 最後に1つ
    ("dark", 3.6, [
        ("A", "結論から言います。民泊は、株や預金とはちがう動きをする「第3の資産」になります。", dict(sfx=[(0.2, "pop"), (1.6, "pop"), (3.2, "bling")])),
        ("A", "ただし、入れ方をまちがえると、ただの重荷です。", dict(sfx=[(1.4, "boing")])),
        ("A", "今日は、民泊を資産に入れる5つの理由と、最後に、失敗しない入れ方を1つだけお話しします。", dict(sfx=[(0.6, "pop"), (1.0, "pop"), (1.4, "pop"), (1.8, "pop"), (2.2, "pop"), (4.4, "chime")])),
    ]),
    # 1 理由① 分散
    ("light", 0.8, [
        ("A", "理由その1。資産の「分散」です。", dict(sfx=[(0, "chime")])),
        ("Y", "分散って、いろんな株を買うことじゃないんですか？", dict(sfx=[(0, "pop")])),
        ("A", "それも分散です。でも株は、同じ日に、そろって下がることがあります。", dict(sfx=[(2.4, "boing")])),
        ("A", "宿の売上は、株価ではなく、旅行者の数で動きます。動く理由がちがう資産を持つのが、本当の分散です。", dict(sfx=[(0.4, "pop"), (2.0, "pop")])),
        ("A", "しかも宿は、料金を日ごとに決められる「実物の資産」。物価が上がる時代にも、合わせやすいんです。", dict(sfx=[(1.2, "ding")])),
    ]),
    # 2 理由② 賃貸とくらべた稼ぎ方
    ("light", 0.8, [
        ("A", "理由その2。賃貸とくらべた「稼ぎ方」のちがいです。", dict(sfx=[(0, "chime")])),
        ("A", "賃貸は、家賃が毎月ほぼ同じ。宿は「稼働率かける1泊の料金」で、上にも下にも動きます。", dict(sfx=[(0.4, "pop"), (2.4, "pop")])),
        ("A", "実際の例です。私たちが下田で借りている一軒家の家賃は、月5万円。", dict(say="実際の例です。私たちが下田で借りている一軒家の家賃は、月五万円。", sfx=[(2.8, "coin")])),
        ("A", "その家を宿にしたら、試運転の3か月で、売上は約100万円。運営費を引いた営業利益は、約45万円でした。", dict(say="その家を宿にしたら、試運転の三か月で、売上は約百万円。運営費を引いた営業利益は、約四十五万円でした。", sfx=[(2.6, "pop"), (4.6, "pop"), (6.4, "coin")])),
        ("A", "月にならすと、家賃を払ったうえで約15万円。家賃の約3倍が、手元に残った計算です。", dict(say="月にならすと、家賃を払ったうえで約十五万円。家賃の約三倍が、手元に残った計算です。", sfx=[(0.6, "rise"), (3.0, "bling")])),
        ("A", "ただし、ここには私たちの手間と、改修や家具の初期投資、約650万円は入っていません。稼働率が33%の月もありました。", dict(say="ただし、ここには私たちの手間と、改修や家具の初期投資、約六百五十万円は入っていません。稼働率が三十三パーセントの月もありました。", sfx=[(0.3, "alert")])),
        ("A", "つまり宿は、運営の腕で、稼ぎを伸ばせる資産。ここが、賃貸との一番のちがいです。", dict(sfx=[(0.2, "ding")])),
    ]),
    # 3 理由③ 世界の観光需要
    ("light", 0.8, [
        ("A", "理由その3。世界の観光需要を、自分の資産に取り込めることです。", dict(sfx=[(0, "chime")])),
        ("A", "日本に来た外国人旅行者は、2025年に4,268万人。過去最多を更新しました。", dict(say="日本に来た外国人旅行者は、二千二十五年に四千二百六十八万人。過去最多を更新しました。", sfx=[(0.4, "pop"), (2.2, "rise")])),
        ("A", "国は、2030年に6,000万人を目標にしています。", dict(say="国は、二千三十年に六千万人を目標にしています。", sfx=[(0.4, "pop")])),
        ("A", "しかも、外国人の宿泊の約3分の2は、東京・大阪・名古屋などの大都市圏。地方には、まだ伸びる余地があります。", dict(say="しかも、外国人の宿泊の約三分の二は、東京、大阪、名古屋などの大都市圏。地方には、まだ伸びる余地があります。", sfx=[(0.4, "pop"), (4.4, "ding")])),
        ("Y", "地方の空き家にも、チャンスがあるってことか…！", dict(sfx=[(0, "pop")])),
    ]),
    # 4 理由④ 税金
    ("light", 0.8, [
        ("A", "理由その4。税金です。ここは誤解が多いので、正確にいきます。", dict(sfx=[(0, "chime")])),
        ("A", "宿の売上からは、清掃や手数料などの経費を差し引けます。家具や改修の費用は、何年かに分けて経費にする「減価償却」ができます。", dict(sfx=[(0.6, "pop"), (4.2, "pop")])),
        ("A", "ただし、民泊新法の宿の所得は、原則「雑所得」。赤字が出ても、給料と相殺して税金を減らす使い方はできない、と考えておきましょう。", dict(sfx=[(2.6, "pop"), (5.6, "boing")])),
        ("A", "むしろ注目は、空き家の固定資産税。放置して自治体から勧告を受けると、土地の税を軽くする特例が外れ、計算のもとが最大6倍になります。", dict(say="むしろ注目は、空き家の固定資産税。放置して自治体から勧告を受けると、土地の税を軽くする特例が外れ、計算のもとが最大六倍になります。", sfx=[(0.4, "pop"), (6.4, "boing")])),
        ("A", "宿として手入れを続けることは、この負担を避けることにもつながります。", dict(sfx=[(0.6, "ding")])),
        ("A", "税金は条件で変わるので、始める前に、税理士さんに確認してください。", dict(sfx=[(0.4, "pop")])),
    ]),
    # 5 理由⑤ 社会課題
    ("light", 0.8, [
        ("A", "理由その5。社会の課題を、ビジネスで解決できることです。", dict(sfx=[(0, "chime")])),
        ("A", "日本の空き家は、約900万戸。住宅の、約7軒に1軒です。", dict(say="日本の空き家は、約九百万戸。住宅の、約七軒に一軒です。", sfx=[(2.2, "pop")])),
        ("A", "その家に旅行者を呼べば、家は生き返り、地域のお店にも、お金が落ちます。", dict(sfx=[(0.6, "bling"), (2.4, "coin"), (3.0, "coin")])),
        ("A", "お金を増やしながら、町の役にも立つ。だから、長く続けやすい投資なんです。", dict(sfx=[(0.4, "ding")])),
    ]),
    # 6 リスク
    ("light", 0.8, [
        ("A", "もちろん、リスクもあります。大きく3つ。", dict(say="もちろん、リスクもあります。大きく三つ。", sfx=[(0, "alert")])),
        ("A", "1つめ、需要の波。季節や景気、感染症で、旅行者は大きく減ることがあります。", dict(say="ひとつめ、需要の波。季節や景気、感染症で、旅行者は大きく減ることがあります。", sfx=[(0, "pop")])),
        ("A", "2つめ、ルール。民泊新法では、営業は年180日まで。地域の条例で、さらに短くなることもあります。", dict(say="ふたつめ、ルール。民泊新法では、営業は年百八十日まで。地域の条例で、さらに短くなることもあります。", sfx=[(0, "pop")])),
        ("A", "3つめ、手間。清掃やゲスト対応は毎日続きます。自分でやるか、任せるかで、手元に残るお金が変わります。", dict(say="みっつめ、手間。清掃やゲスト対応は毎日続きます。自分でやるか、任せるかで、手元に残るお金が変わります。", sfx=[(0, "pop")])),
    ]),
    # 7 失敗しない入れ方 → まとめ → 無料相談
    ("dark", 4.6, [
        ("A", "では最後に、失敗しない入れ方を、1つだけ。", dict(say="では最後に、失敗しない入れ方を、ひとつだけ。", sfx=[(0, "rise")])),
        ("A", "それは、全部を民泊にしないこと。預金や株を土台にして、資産の一部として、小さく組み込むことです。", dict(sfx=[(0.4, "bling"), (3.6, "pop")])),
        ("A", "私たちも、家を買わずに借りて始めました。準備には、約7か月かかりました。", dict(say="私たちも、家を買わずに借りて始めました。準備には、約七か月かかりました。", sfx=[(0.4, "pop")])),
        ("A", "まとめると、分散、稼ぎ方、観光需要、税金、社会課題。5つの理由で、民泊は資産に入れる価値があります。リスクを知って、一部として、小さく。", dict(say="まとめると、分散、稼ぎ方、観光需要、税金、社会課題。五つの理由で、民泊は資産に入れる価値があります。リスクを知って、一部として、小さく。", sfx=[(0.6, "pop"), (1.2, "pop"), (1.8, "pop"), (2.6, "pop"), (3.2, "pop")])),
        ("A", "あなたの家や地域で、民泊が成り立つか知りたい方は、アキヤドの無料相談へ。概要欄のリンクからどうぞ。", dict(sfx=[(0.4, "chime")])),
    ]),
]
LEAD, GAP = 0.6, 0.3

SCENE_JS = r"""
CAST.aki={skin:'#f1c7a1',hair:'#2b2422',style:'short',top:'#23395b',top2:'#1a2c47',inner:'#ffffff',jacket:true,pants:'#2a3140',shoes:'#3a2a20',glasses:true,tie:'#c95a35'};
const VNAME={A:'戦略家 アキ',Y:'ユウタ'},VCOL={A:'#23395b',Y:G};
const NAVY='#23395b',RED='#e53935';
const talking=(s,t)=>LINES.some(l=>l[2]===s&&t>=l[0]&&t<l[1]);
function subtitle(l,t){
  const lines=l[3],fs=42,h=lines.length*fs*1.45+40,w=1560,y=1048-h,o=clamp((t-l[0]+.05)/.2)*clamp((l[1]+.3-t)/.2);
  const name=`<rect x="${960-w/2+28}" y="${y-26}" width="${VNAME[l[2]].length*30+44}" height="52" rx="26" fill="${VCOL[l[2]]}"/><text x="${960-w/2+50}" y="${y+9}" font-size="30" font-weight="900" fill="#fff">${VNAME[l[2]]}</text>`;
  return `<g opacity="${o}"><rect x="${960-w/2}" y="${y}" width="${w}" height="${h}" rx="24" fill="#16233a" opacity=".93"/>${name}${lines.map((s,i)=>`<text x="960" y="${y+28+fs*1.08+i*fs*1.45}" text-anchor="middle" font-size="${fs}" font-weight="700" fill="#fff" letter-spacing="1">${s}</text>`).join('')}</g>`;
}
const P=(x,y,s,o,t)=>person(x,y,s,Object.assign({t},o,{talk:o.who?talking(o.who,t):false}));
function studio(t,dark){ // 解説のスタジオ（明るい／暗い）
  if(dark){let s=`<rect width="1920" height="1080" fill="#16233a"/><path d="M700 0 L420 1080 L1640 1080 L1360 0Z" fill="#fff" opacity=".05"/>`;
    for(let k=0;k<30;k++)s+=`<circle cx="${rnd(k)*1920}" cy="${rnd(k+40)*700}" r="${1.5+rnd(k+80)*2}" fill="#fff" opacity="${.15+.25*Math.abs(Math.sin(t*1.5+k))}"/>`;
    return s+`<rect y="${GROUND}" width="1920" height="${1080-GROUND}" fill="#0f1a2c"/>`;}
  let s=`<rect width="1920" height="1080" fill="#f5f1e8"/>`;
  for(let x=0;x<1920;x+=60)s+=`<path d="M${x} 0 V1080" stroke="#e9e3d5" stroke-width="2"/>`;
  for(let y=0;y<1080;y+=60)s+=`<path d="M0 ${y} H1920" stroke="#e9e3d5" stroke-width="2"/>`;
  return s+`<rect y="${GROUND}" width="1920" height="${1080-GROUND}" fill="#e6dfcf"/>`;
}
function hdr(no,title,p,c=T){ // 「理由 ①」の見出し
  return fade(p,`<rect x="540" y="70" width="${no?190:0}" height="64" rx="32" fill="${c}"/>${no?`<text x="635" y="114" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">理由 ${no}</text>`:''}<text x="${no?750:540}" y="118" font-size="54" font-weight="900" fill="${DG}">${title}</text>`,0);
}
const card=(x,y,w,h,inner,p)=>pop(x+w/2,y+h/2,p,box(x,y,w,h,28)+inner);
function qbubble(id,txt,p,t){ // ユウタの質問
  return pop(1500,215,p,`${face(id,1790,215,62,'owner',G,'worry',t,talking('Y',t))}<rect x="${1700-txt.length*30-60}" y="172" width="${txt.length*30+60}" height="86" rx="30" fill="#fff" stroke="${G}" stroke-width="4"/><text x="${1700-30-txt.length*15}" y="227" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">${txt}</text>`);
}
function stampX(x,y,txt,p,c=RED,fs=72,rot=-8){return pop(x,y,p,`<g transform="rotate(${rot} ${x} ${y})"><rect x="${x-txt.length*fs*.5-34}" y="${y-fs*.8}" width="${txt.length*fs+68}" height="${fs*1.45}" rx="14" fill="#fff" fill-opacity=".92" stroke="${c}" stroke-width="10"/><text x="${x}" y="${y+fs*.33}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${c}">${txt}</text></g>`)}
const REASONS=[['1','分散',NAVY],['2','稼ぎ方',T],['3','観光需要','#2a7fa8'],['4','税金','#7a4a9a'],['5','社会課題',G]];
function scene(i,t,lt){
  const L=SL[i],E=SE[i],at=(k,d=.5,o=0)=>seg(lt,L[k]+o,L[k]+o+d),on=k=>lt>=L[k],win=(k,j)=>clamp(seg(lt,L[k],L[k]+.4))*(j==null?1:1-seg(lt,L[j]-.1,L[j]+.3));
  let s='';
  const aki=(pose,mood='happy',x=250)=>P(x,GROUND,.92,{c:'aki',who:'A',pose,mood},t);
  if(i===0){
    s+=aki(on(1)&&!on(2)?'open':'present');
    if(!on(1)){[['預金','yen','#8a8f98'],['株','chart','#3d6a8a'],['民泊','home',T]].forEach(([w,ic,c],k)=>{const x=760+k*430,p=at(0,.4,.2+k*1.4);
      s+=pop(x,470,p,`${box(x-170,300,340,340,30)}${icon(x,430,78,ic,c,'#fff',1.1)}<text x="${x}" y="590" text-anchor="middle" font-size="52" font-weight="900" fill="${DG}">${w}</text>`)});
      s+=pop(1620,720,at(0,.4,3.2),`<rect x="1450" y="680" width="340" height="80" rx="40" fill="${Y}"/><text x="1620" y="735" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">第3の資産</text>`);
      s+=fade(at(0,.4,3.2),`<rect x="1442" y="292" width="356" height="356" rx="36" fill="none" stroke="${Y}" stroke-width="10"/>`,0);}
    if(on(1)&&!on(2)){s+=pop(1190,480,at(1,.4),`${icon(1190,480,150,'home',T,'#fff',2)}<rect x="1100" y="250" width="180" height="110" rx="14" fill="#3a3e46"/><text x="1190" y="322" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">重い</text>`)+stampX(1190,720,'ただの重荷',at(1,.3,1.3));}
    if(on(2)){REASONS.forEach(([n,w,c],k)=>{const x=640+(k%3)*420,y=k<3?330:520;s+=pop(x+180,y,at(2,.35,.6+k*.4),`${box(x,y-70,360,140,30)}<circle cx="${x+70}" cy="${y}" r="44" fill="${c}"/><text x="${x+70}" y="${y+16}" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">${n}</text><text x="${x+135}" y="${y+18}" font-size="48" font-weight="900" fill="${DG}">${w}</text>`)});
      s+=pop(1660,520,at(2,.4,4.4),`<rect x="1480" y="450" width="360" height="140" rx="30" fill="${Y}"/><text x="1660" y="505" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">最後に</text><text x="1660" y="560" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">失敗しない入れ方</text>`);}
    const tp=seg(lt,E[2]+.3,E[2]+1.0);
    s+=pop(960,440,tp,`<rect width="1920" height="1080" fill="#000" opacity=".45"/><rect x="240" y="250" width="1440" height="400" rx="40" fill="#fff"/><rect x="700" y="212" width="520" height="76" rx="38" fill="${NAVY}"/><text x="960" y="264" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">アキヤドの民泊戦略</text><text x="960" y="420" text-anchor="middle" font-size="84" font-weight="900" fill="${DG}">民泊を資産に入れる</text><text x="960" y="560" text-anchor="middle" font-size="110" font-weight="900" fill="${T}">5つの理由</text><text x="960" y="720" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">${NOTE}</text>`);
  }
  if(i===1){ // 分散
    s+=aki(on(2)&&!on(3)?'open':(on(4)?'point':'present'));
    s+=hdr('①','分散：動く理由がちがう資産を持つ',at(0,.4),NAVY);
    if(on(1)&&!on(2))s+=qbubble('q1','いろんな株を買えば分散？',at(1,.4),t);
    if(on(1)&&!on(3)){const dn=on(2)?eo(at(2,1.2,.8)):0;[['株A','#3d6a8a'],['株B','#5a86a8'],['株C','#7a9fbf']].forEach(([w,c],k)=>{const x=700+k*360;let path='';for(let q=0;q<=10;q++){const yy=560-Math.sin(q*.9+k)*40-q*6+(q>6?dn*(q-6)*55:0);path+=(q?'L':'M')+(x+q*28)+' '+yy}
      s+=card(x-40,290,360,440,`<text x="${x+140}" y="350" text-anchor="middle" font-size="40" font-weight="900" fill="${c}">${w}</text><path d="${path}" stroke="${c}" stroke-width="10" fill="none" stroke-linejoin="round"/>`,at(1,.4,.3+k*.3))});
      if(on(2))s+=stampX(1240,790,'同じ日に、そろって下がる',at(2,.3,2.2),RED,48,-4);}
    if(on(3)&&!on(4)){s+=card(560,250,600,500,`<text x="860" y="320" text-anchor="middle" font-size="44" font-weight="900" fill="#3d6a8a">株の値段</text>${icon(860,470,90,'chart','#3d6a8a','#fff',1.3)}<text x="860" y="640" text-anchor="middle" font-size="34" font-weight="900" fill="#4a5a52">景気・金利で動く</text>`,at(3,.4))+card(1240,250,600,500,`<text x="1540" y="320" text-anchor="middle" font-size="44" font-weight="900" fill="${T}">宿の売上</text>${icon(1540,470,90,'home',T,'#fff',1.3)}<text x="1540" y="640" text-anchor="middle" font-size="34" font-weight="900" fill="#4a5a52">旅行者の数・季節で動く</text>`,at(3,.4,1.6));
      s+=pop(1200,800,at(3,.4,3.6),`<rect x="830" y="760" width="740" height="84" rx="42" fill="${NAVY}"/><text x="1200" y="815" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">動く理由がちがう＝本当の分散</text>`);}
    if(on(4)){const pr=Math.round(12000+3000*eo(at(4,1.4,1.2)));s+=card(600,250,1200,520,`<text x="1200" y="320" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">宿の料金は、日ごとに決められる</text>${['月','火','水','木','金','土','日'].map((d,k)=>`<rect x="${660+k*155}" y="370" width="140" height="220" rx="14" fill="${k>=5?'#fdecea':'#eef3f8'}"/><text x="${730+k*155}" y="420" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">${d}</text><text x="${730+k*155}" y="520" text-anchor="middle" font-size="${k>=5?34:30}" font-weight="900" fill="${k>=5?RED:'#4a5a52'}">¥${(k>=5?pr:12000).toLocaleString()}</text>`).join('')}<text x="1200" y="700" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">「実物の資産」＝物価に合わせやすい</text>`,at(4,.4));}
  }
  if(i===2){ // 稼ぎ方
    s+=aki(on(5)&&!on(6)?'think':(on(4)?'point':'present'),on(5)&&!on(6)?'worry':'happy');
    s+=hdr('②','賃貸とくらべた「稼ぎ方」',at(0,.4),T);
    if(on(1)&&!on(2)){const bars=(x,vals,c,lab)=>`<text x="${x+250}" y="320" text-anchor="middle" font-size="44" font-weight="900" fill="${c}">${lab}</text><path d="M${x} 650 H${x+500}" stroke="#9fb5a8" stroke-width="5"/>`+vals.map((v,k)=>`<rect x="${x+20+k*80}" y="${650-v*eo(at(1,1,.4+k*.08))}" width="56" height="${v*eo(at(1,1,.4+k*.08))}" rx="6" fill="${c}"/>`).join('');
      s+=card(560,250,600,500,bars(610,[200,200,200,200,200,200],'#8a8f98','賃貸：毎月ほぼ同じ'),at(1,.4))+card(1240,250,600,500,bars(1290,[120,250,190,300,90,260],T,'宿：上にも下にも'),at(1,.4,1.8));
      s+=pop(1540,800,at(1,.4,3.2),`<rect x="1250" y="760" width="580" height="80" rx="40" fill="${T}"/><text x="1540" y="814" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">稼働率 × 1泊の料金</text>`);}
    if(on(2)&&!on(3))s+=card(760,260,900,500,`${house(1210,640,.7,1)}<rect x="1010" y="300" width="400" height="90" rx="45" fill="${NAVY}"/><text x="1210" y="360" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">家賃 月5万円</text><text x="1210" y="720" text-anchor="middle" font-size="30" font-weight="700" fill="#4a5a52">下田の一軒家（借りている物件）</text>`,at(2,.4));
    if(on(3)&&!on(4)){const g=k=>eo(at(3,.8,[2.4,4.4,6.2][k]));const base=680,sc=3.0;
      s+=card(600,240,1200,560,`<text x="1200" y="300" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">試運転の3か月（2025年）</text><path d="M680 ${base} H1720" stroke="#9fb5a8" stroke-width="5"/>
        <rect x="740" y="${base-100*sc*g(0)}" width="220" height="${100*sc*g(0)}" rx="8" fill="${NAVY}"/><text x="850" y="${base+50}" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">売上</text>${g(0)>.9?`<text x="850" y="${base-100*sc-20}" text-anchor="middle" font-size="40" font-weight="900" fill="${NAVY}">約100万円</text>`:''}
        <rect x="1090" y="${base-100*sc}" width="220" height="${55*sc*g(1)}" rx="8" fill="#b9c3cc"/><text x="1200" y="${base+50}" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">運営費</text>${g(1)>.9?`<text x="1200" y="${base-100*sc+55*sc/2+14}" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">約55万円</text>`:''}
        <rect x="1440" y="${base-45*sc*g(2)}" width="220" height="${45*sc*g(2)}" rx="8" fill="${T}"/><text x="1550" y="${base+50}" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">営業利益</text>${g(2)>.9?`<text x="1550" y="${base-45*sc-20}" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">約45万円</text>`:''}`,at(3,.4));}
    if(on(4)&&!on(5)){const g=eo(at(4,1,.4));s+=card(700,240,1000,560,`<text x="1200" y="300" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">1か月あたり</text><path d="M780 700 H1620" stroke="#9fb5a8" stroke-width="5"/>
      <rect x="860" y="${700-5*24*g}" width="220" height="${5*24*g}" rx="8" fill="#8a8f98"/><text x="970" y="${700-5*24*g-20}" text-anchor="middle" font-size="40" font-weight="900" fill="#5a6068">5万円</text><text x="970" y="750" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">家賃（大家さん）</text>
      <rect x="1320" y="${700-15*24*g}" width="220" height="${15*24*g}" rx="8" fill="${T}"/><text x="1430" y="${700-15*24*g-20}" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">約15万円</text><text x="1430" y="750" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">宿の営業利益</text>`,at(4,.4))+stampX(1660,460,'約3倍',at(4,.3,3.0),RED,64,8);}
    if(on(5)&&!on(6))s+=card(640,240,1120,560,`<text x="1200" y="310" text-anchor="middle" font-size="44" font-weight="900" fill="${RED}">ここに入っていないもの</text>${[['自分たちの手間（人件費）',''],['改修・家具の初期投資','約650万円'],['悪い月','稼働率33%の月も']].map(([a,b],k)=>`<rect x="700" y="${370+k*130}" width="1000" height="104" rx="20" fill="#fdecea"/><text x="740" y="${435+k*130}" font-size="40" font-weight="900" fill="${DG}">${a}</text><text x="1660" y="${435+k*130}" text-anchor="end" font-size="40" font-weight="900" fill="${RED}">${b}</text>`).join('')}`,at(5,.4));
    if(on(6))s+=pop(1200,500,at(6,.4),`<rect x="640" y="380" width="1120" height="240" rx="120" fill="${T}"/><text x="1200" y="480" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">運営の腕で、</text><text x="1200" y="570" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">稼ぎを伸ばせる資産</text>`);
  }
  if(i===3){ // 観光需要
    s+=aki(on(3)?'point':'present');
    s+=hdr('③','世界の観光需要を取り込む',at(0,.4),'#2a7fa8');
    if(on(1)&&!on(3)){const data=[['2024年',3687,'#7fb3cf'],['2025年',4268,'#2a7fa8'],['2030年 目標',6000,'#fff']];const sc=.07;
      s+=card(600,220,1200,600,`<text x="1200" y="285" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">日本に来た外国人旅行者</text><path d="M700 740 H1700" stroke="#9fb5a8" stroke-width="5"/>`+data.map(([y,v,c],k)=>{const p=k<2?eo(at(1,.9,.4+k*.9)):(on(2)?eo(at(2,.9,.4)):0);if(p<=0)return '';const h=v*sc*p;return `<rect x="${780+k*320}" y="${740-h}" width="220" height="${h}" rx="8" fill="${c}" ${k===2?`stroke="#2a7fa8" stroke-width="6" stroke-dasharray="16 10"`:''}/><text x="${890+k*320}" y="${720-h}" text-anchor="middle" font-size="40" font-weight="900" fill="#2a7fa8">${v.toLocaleString()}万人</text><text x="${890+k*320}" y="790" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">${y}</text>`}).join(''),at(1,.4));
      if(lt>L[1]+3)s+=stampX(1010,350,'過去最多',at(1,.3,3.4),RED,52,-6);}
    if(on(3)&&!on(4)){const p=eo(at(3,1.4,.6)),a=2*Math.PI*.663*p,R=200,cx=980,cy=520;const x2=cx+R*Math.sin(a),y2=cy-R*Math.cos(a);
      s+=card(600,220,1200,600,`<text x="1200" y="285" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">外国人の延べ宿泊者数（2025年）</text><circle cx="${cx}" cy="${cy}" r="${R}" fill="#cfe3ee"/><path d="M${cx} ${cy} L${cx} ${cy-R} A${R} ${R} 0 ${a>Math.PI?1:0} 1 ${x2} ${y2}Z" fill="#2a7fa8"/><circle cx="${cx}" cy="${cy}" r="${R*.55}" fill="#fff"/>
        <rect x="1240" y="400" width="40" height="40" rx="8" fill="#2a7fa8"/><text x="1300" y="433" font-size="36" font-weight="900" fill="${DG}">三大都市圏 約3分の2</text><rect x="1240" y="500" width="40" height="40" rx="8" fill="#cfe3ee"/><text x="1300" y="533" font-size="36" font-weight="900" fill="${DG}">地方部 33.7%</text>`,at(3,.4));
      s+=pop(1480,690,at(3,.4,4.6),`<rect x="1250" y="650" width="460" height="80" rx="40" fill="${Y}"/><text x="1480" y="704" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">地方は、伸びる余地</text>`);}
    if(on(4)){s+=qbubble('q3','地方の空き家にもチャンス！？',at(4,.4),t);s+=card(700,300,1000,460,`${house(1200,680,.7,1)}${sparkle(950,420,1.2,lt,0)}${sparkle(1450,400,1,lt,2)}`,at(4,.4,.2));}
  }
  if(i===4){ // 税金
    s+=aki(on(2)&&!on(3)?'think':'present',on(2)&&!on(3)?'worry':'happy');
    s+=hdr('④','税金：正しく知る',at(0,.4),'#7a4a9a');
    if(on(1)&&!on(2)){s+=card(560,230,1280,560,`<rect x="620" y="300" width="300" height="140" rx="20" fill="${NAVY}"/><text x="770" y="385" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">売上</text><text x="980" y="390" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">−</text><rect x="1040" y="300" width="300" height="140" rx="20" fill="#b9c3cc"/><text x="1190" y="385" text-anchor="middle" font-size="48" font-weight="900" fill="${DG}">経費</text><text x="1400" y="390" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">=</text><rect x="1460" y="300" width="320" height="140" rx="20" fill="#7a4a9a"/><text x="1620" y="385" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">所得</text>
        <text x="1190" y="490" text-anchor="middle" font-size="30" font-weight="900" fill="#4a5a52">清掃・手数料・光熱費など</text>`,at(1,.4));
      const dp=at(1,.4,4.2);if(dp>0)s+=fade(dp,`<text x="700" y="590" font-size="34" font-weight="900" fill="#7a4a9a">減価償却：家具・改修の費用を、何年かに分けて経費に</text>${[0,1,2,3,4].map(k=>`<rect x="${700+k*210}" y="630" width="180" height="${110*eo(seg(lt,L[1]+4.6+k*.25,L[1]+5+k*.25))}" rx="10" fill="#c9b6e0"/><text x="${790+k*210}" y="770" text-anchor="middle" font-size="26" font-weight="900" fill="#4a5a52">${k+1}年目</text>`).join('')}`,0);}
    if(on(2)&&!on(3)){s+=card(620,250,1160,520,`<text x="1200" y="320" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">民泊新法の宿の所得は、原則</text><rect x="980" y="350" width="440" height="110" rx="55" fill="#7a4a9a"/><text x="1200" y="425" text-anchor="middle" font-size="54" font-weight="900" fill="#fff">雑所得</text>
        <rect x="700" y="520" width="360" height="120" rx="20" fill="#f3eef8"/><text x="880" y="595" text-anchor="middle" font-size="40" font-weight="900" fill="#7a4a9a">宿の赤字</text><rect x="1340" y="520" width="360" height="120" rx="20" fill="#eef3f8"/><text x="1520" y="595" text-anchor="middle" font-size="40" font-weight="900" fill="${NAVY}">給料</text><path d="M1080 580 H1320" stroke="#9fb5a8" stroke-width="8" stroke-dasharray="14 10"/>`,at(2,.4));
      s+=stampX(1200,580,'相殺できない',at(2,.3,5.4),RED,48,-6);}
    if(on(3)&&!on(4)){const g=eo(at(3,1,6.2));s+=card(620,230,1160,580,`<text x="1200" y="295" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">空き家の土地の固定資産税（200㎡以下の部分）</text><path d="M760 720 H1640" stroke="#9fb5a8" stroke-width="5"/>
        <rect x="840" y="${720-60}" width="240" height="60" rx="8" fill="#9fc7a8"/><text x="960" y="640" text-anchor="middle" font-size="36" font-weight="900" fill="${G}">特例あり 1/6</text><text x="960" y="770" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">住宅が建つ土地</text>
        <rect x="1320" y="${720-300*g}" width="240" height="${300*g}" rx="8" fill="${RED}"/>${g>.9?`<text x="1440" y="400" text-anchor="middle" font-size="40" font-weight="900" fill="${RED}">最大6倍</text>`:''}<text x="1440" y="770" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">勧告を受けると</text>`,at(3,.4));}
    if(on(4)&&!on(5))s+=card(760,260,880,500,`${house(1200,690,.7,1)}${sparkle(980,380,1.2,lt,0)}${sparkle(1420,360,1,lt,2)}<rect x="960" y="290" width="480" height="80" rx="40" fill="${G}"/><text x="1200" y="344" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">手入れを続ける家</text>`,at(4,.4));
    if(on(5))s+=pop(1200,500,at(5,.4),`<rect x="700" y="400" width="1000" height="200" rx="100" fill="#7a4a9a"/><text x="1200" y="482" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">税金は条件で変わる</text><text x="1200" y="555" text-anchor="middle" font-size="40" font-weight="900" fill="${Y}">始める前に、税理士さんに確認</text>`);
  }
  if(i===5){ // 社会課題
    s+=aki(on(3)?'cheer':'present');
    s+=hdr('⑤','社会の課題を、ビジネスで解決',at(0,.4),G);
    if(on(1)){const lit=on(2)?eo(at(2,1,.4)):0;
      s+=card(560,220,1280,600,`<text x="1200" y="290" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">空き家 約900万戸（住宅の約7軒に1軒）</text>${[0,1,2,3,4,5,6].map(k=>`<g opacity="${eo(at(1,.3,.3+k*.2))}">${house(700+k*167,640,.32,k===3?lit:1)}</g>`).join('')}${on(2)?'':`<text x="1201" y="700" text-anchor="middle" font-size="34" font-weight="900" fill="${RED}">空き家</text>`}`,at(1,.4));
      if(on(2)){[['カフェ',1000],['お店',1400]].forEach(([w,x],k)=>{s+=pop(x,760,at(2,.4,2+k*.6),`<rect x="${x-110}" y="725" width="220" height="70" rx="35" fill="${Y}"/><text x="${x}" y="772" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">${w}</text>`)});
        for(let c=0;c<3;c++){const f=((lt*.7+c/3)%1);if(lt>L[2]+2)s+=`<g opacity="${Math.sin(f*Math.PI)}">${coin(1201+(c%2?200:-200)*f,560+180*f,22)}</g>`}}
      if(on(3))s+=pop(1200,420,at(3,.4),`<rect x="760" y="360" width="880" height="120" rx="60" fill="${G}"/><text x="1200" y="438" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">増やしながら、町の役に立つ</text>`);}
  }
  if(i===6){ // リスク
    s+=aki(on(1)?'point':'think','happy');
    s+=hdr('','リスクも、大きく3つ',at(0,.4));
    [['1','需要の波','季節・景気・感染症で、旅行者が大きく減ることも'],['2','ルール','民泊新法は年180日まで。条例でさらに短いことも'],['3','手間','清掃・ゲスト対応が続く。自分か、任せるか']].forEach(([n,a,b],k)=>{
      s+=checkRow2(560,320+k*170,1280,n,a,b,at(1+k))});
  }
  if(i===7){ // 失敗しない入れ方
    s+=aki(on(3)?'present':(on(1)?'point':'present'));
    if(!on(1))s+=pop(1200,460,at(0,.5),`<rect x="800" y="300" width="800" height="320" rx="40" fill="${Y}"/><text x="1200" y="420" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">失敗しない入れ方</text><text x="1200" y="560" text-anchor="middle" font-size="120" font-weight="900" fill="${DG}">？</text>`);
    if(on(1)&&!on(2)){const p=eo(at(1,1.2,.6)),R=210,cx=960,cy=500;const parts=[['預金',.4,'#8a8f98'],['株・投資信託',.45,'#3d6a8a'],['民泊',.15,T]];let a0=0,sv='';
      parts.forEach(([w,f,c])=>{const a1=a0+2*Math.PI*f*p,x1=cx+R*Math.sin(a0),y1=cy-R*Math.cos(a0),x2=cx+R*Math.sin(a1),y2=cy-R*Math.cos(a1);sv+=`<path d="M${cx} ${cy} L${x1} ${y1} A${R} ${R} 0 ${a1-a0>Math.PI?1:0} 1 ${x2} ${y2}Z" fill="${c}" stroke="#fff" stroke-width="6"/>`;a0=a1});
      s+=pop(1200,500,at(1,.4),`${box(580,230,1240,560,30)}${sv}${parts.map(([w,f,c],k)=>`<rect x="1260" y="${360+k*100}" width="40" height="40" rx="8" fill="${c}"/><text x="1320" y="${393+k*100}" font-size="40" font-weight="900" fill="${DG}">${w}</text>`).join('')}<text x="1200" y="760" text-anchor="middle" font-size="26" font-weight="700" fill="#888">割合はイメージです</text>`);
      s+=pop(1560,710,at(1,.4,3.6),`<rect x="1330" y="660" width="460" height="100" rx="50" fill="${T}"/><text x="1560" y="725" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">一部として、小さく</text>`);}
    if(on(2)&&!on(3))s+=card(760,240,880,540,`${house(1200,680,.75,1)}<rect x="1000" y="280" width="400" height="84" rx="42" fill="${G}"/><text x="1200" y="337" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">買わずに借りた家</text><rect x="1500" y="420" width="120" height="0"/>`,at(2,.4))+stampX(1560,700,'準備 約7か月',at(2,.3,2.6),T,44,-6);
    if(on(3)&&!on(4)){REASONS.forEach(([n,w,c],k)=>{const x=640+(k%3)*420,y=k<3?330:520;s+=pop(x+180,y,at(3,.3,.5+k*.6),`${box(x,y-70,360,140,30)}<circle cx="${x+70}" cy="${y}" r="44" fill="${c}"/><text x="${x+70}" y="${y+16}" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">${n}</text><text x="${x+135}" y="${y+18}" font-size="48" font-weight="900" fill="${DG}">${w}</text>`)});
      s+=pop(1660,520,at(3,.4,7),`<rect x="1480" y="450" width="360" height="140" rx="30" fill="${Y}"/><text x="1660" y="505" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">リスクを知って</text><text x="1660" y="560" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">一部として、小さく</text>`);}
    if(on(4))s+=pop(1200,470,at(4,.5),`${box(620,250,1160,420,36)}${LOGO(890,290,1.3)}<rect x="760" y="420" width="880" height="100" rx="50" fill="${T}"/><text x="1200" y="487" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">民泊が成り立つか、無料で相談</text><text x="1200" y="610" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">概要欄のリンクから</text>`);
    s+=fade(seg(lt,E[4]+.5,E[4]+1.2),`<rect width="1920" height="1080" fill="#16233a"/><text x="960" y="380" text-anchor="middle" font-size="60" font-weight="900" fill="#fff">最後まで見てくれて、ありがとうございます</text><text x="960" y="480" text-anchor="middle" font-size="30" font-weight="700" fill="#dfe6ee">${NOTE}</text><text x="960" y="530" text-anchor="middle" font-size="30" font-weight="700" fill="#dfe6ee">出典は概要欄に記載しています。</text><text x="960" y="630" text-anchor="middle" font-size="30" font-weight="700" fill="#b8c4d2">${CREDIT}</text><rect x="780" y="700" width="360" height="100" rx="50" fill="#fff"/>${LOGO(810,715,1.1)}`,0);
  }
  return s;
}
function checkRow2(x,y,w,no,title,note,p){return fade(p,`${box(x,y-70,w,140,70)}<circle cx="${x+80}" cy="${y}" r="48" fill="${RED}"/><text x="${x+80}" y="${y+17}" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">${no}</text><text x="${x+160}" y="${y-8}" font-size="50" font-weight="900" fill="${DG}">${title}</text><text x="${x+160}" y="${y+44}" font-size="32" font-weight="700" fill="#4a5a52">${note}</text>`,0)}
window.draw=function(t){
  let i=SC.findIndex(([a,b])=>t>=a&&t<b);if(i<0)i=SC.length-1;
  const a=SC[i][0],TR=.6;
  const B=j=>studio(t,THEME[j]==='dark');
  let out=`${B(i)}${scene(i,t,t-a)}`;
  if(i>0&&t-a<TR){const k=eo((t-a)/TR),r=k*1150,pa=SC[i-1][0];
    out=`${B(i-1)}${scene(i-1,t,t-pa)}<clipPath id="iris"><circle cx="960" cy="540" r="${r}"/></clipPath><g clip-path="url(#iris)">${out}</g><circle cx="960" cy="540" r="${r}" fill="none" stroke="#fff" stroke-width="${26*(1-k)}" opacity="${1-k}"/>`;}
  const cur=LINES.find(l=>t>=l[0]-.05&&t<l[1]+.3);
  if(cur)out+=subtitle(cur,t);
  document.getElementById('s').innerHTML=out.replaceAll('__ROOT__',window.ROOT);
};
"""


def timeline(cache):
    sc, lines, voices, sfx, t0 = [], [], [], [], 0.0
    for i, (theme, tail, ls) in enumerate(SCENES):
        t = t0 + LEAD
        if i > 0:
            sfx.append((t0, "whoosh"))
        for k, (spk, disp, opt) in enumerate(ls):
            v = VOICES[spk]
            t += opt.get("pre", 0)
            f, d = tts(opt.get("say", disp), v["style"], MODELS, cache, v["speed"], v["pitch"], v["intonation"])
            voices.append((t, f)); lines.append([round(t, 3), round(t + d, 3), spk, wrap(disp), i, k])
            for off, kind in opt.get("sfx", []):
                sfx.append((t + off, kind))
            t += d + GAP
        end = t - GAP + tail
        sc.append([round(t0, 3), round(end, 3)]); t0 = end
    return sc, lines, voices, sfx


def build_html(sc, lines):
    h = base.HTML
    a = h.index("const AV=[1,2,3,6,4,5];")
    b = h.index("</script></body></html>")
    sl = [[round(l[0] - sc[l[4]][0], 3) for l in lines if l[4] == i] for i in range(len(sc))]
    se = [[round(l[1] - sc[l[4]][0], 3) for l in lines if l[4] == i] for i in range(len(sc))]
    head = (f"const SC={json.dumps(sc)};const LINES={json.dumps(lines, ensure_ascii=False)};const SL={json.dumps(sl)};const SE={json.dumps(se)};"
            f"const THEME={json.dumps([s[0] for s in SCENES])};const CREDIT={json.dumps(CREDIT, ensure_ascii=False)};const NOTE={json.dumps(NOTE, ensure_ascii=False)};")
    return h[:a] + head + SCENE_JS + h[b:]


def main():
    args = sys.argv[1:]
    hq = "--hq" in args; args = [x for x in args if x != "--hq"]
    prev = None
    if "--preview" in args:
        k = args.index("--preview"); prev = [float(x) for x in args[k + 1:]]; args = args[:k]
    out = args[0] if args else os.path.join(tempfile.gettempdir(), "akiyado-strategy-ep1.mp4")
    sc, lines, voices, sfx = timeline(os.path.join(tempfile.gettempdir(), "akiyado_vv"))
    dur = sc[-1][1]
    html = build_html(sc, lines)
    env = dict(os.environ); env["ROOT_DIR"] = ROOT
    env["NODE_PATH"] = os.pathsep.join(p for p in ["/opt/node-tools/node_modules", os.path.join(ROOT, "tools", "check", "node_modules"), env.get("NODE_PATH", "")] if p)
    if hq:
        env["SCALE"] = str(4 / 3); env["JPEG_Q"] = "97"
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(html)
        js = os.path.join(tmp, "r.js"); open(js, "w").write(base.RENDER_JS)
        if prev is not None:
            od = os.path.join(tempfile.gettempdir(), "strategy_preview"); os.makedirs(od, exist_ok=True)
            subprocess.run(["node", js, h, od, "preview", json.dumps(prev)], check=True, env=env)
            print("preview", od, "長さ", round(dur, 1), "秒", [round(a, 1) for a, _ in sc]); return
        fr = os.path.join(tmp, "fr"); os.makedirs(fr)
        subprocess.run(["node", js, h, fr, "video", str(int(dur * FPS))], check=True, env=env)
        import pop_audio
        wav = os.path.join(tmp, "audio.wav"); pop_audio.write(wav, dur, sfx, bgm_gain=0.22, voices=voices, duck=0.3)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%05d.jpg"), "-i", wav, "-c:v", "libx264",
                        "-preset", "slow" if hq else "veryfast", "-crf", "14" if hq else "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k" if hq else "192k",
                        "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, round(dur, 1), "秒")


if __name__ == "__main__":
    main()
