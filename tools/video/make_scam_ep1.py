#!/usr/bin/env python3
"""アキヤド劇場 第1話「民泊をはじめたい会社員を待ち受ける3つの落とし穴」（約6〜9分・1920×1080）を作る。

- 絵の部品（人物・家・背景・図解）は tools/video/make_explainer.py と共通。セリフは VOICEVOX（tools/video/voicevox_tts.py）。
- 場面の長さはセリフの長さから決める。アニメは「何番目のセリフが始まったか」に合わせて動く。
- 話している人物は口が動き、字幕には話している人の名前を色つきで出す。
- 手口と見抜くポイントは、国民生活センター・観光庁の公表内容の範囲。人物・会社は架空（冒頭と最後に表示）。
使い方: python3 tools/video/make_scam_ep1.py [出力.mp4] [--hq] [--preview 秒 ...]
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import make_explainer as base
from voicevox_tts import tts

FPS = 24
# 声（VOICEVOX のスタイルID）。クレジットは最後の画面と説明欄に書く
VOICES = {
    "N": dict(name="ナレーション", style=84, speed=1.0, intonation=1.0, pitch=0.0),   # 青山龍星（しっとり）
    "Y": dict(name="ユウタ", style=11, speed=1.08, intonation=1.15, pitch=0.0),       # 玄野武宏
    "M": dict(name="ミナ", style=29, speed=1.08, intonation=1.15, pitch=0.0),         # No.7
    "U": dict(name="ウマイ先生", style=21, speed=1.12, intonation=1.6, pitch=0.02),    # 剣崎雌雄
}
MODELS = [4, 6, 15]
CREDIT = "VOICEVOX:青山龍星　VOICEVOX:玄野武宏　VOICEVOX:No.7　VOICEVOX:剣崎雌雄"

# 場面: (背景のテーマ, 場面の最後に足す秒, セリフの並び)。セリフ: (話す人, 字幕, {say: 読み, pre: 前の間, sfx: [(秒, 種類)]})
SCENES = [
    ("night", 3.2, [
        ("N", "会社員のユウタ、32歳。", dict(say="会社員のユウタ、三十二歳。")),
        ("Y", "はぁ…給料、上がらないなぁ。何か副業でもしようかな。", {}),
        ("Y", "民泊…？ 家を旅行者に貸して、収入になるのか。これ、いいかも！", dict(sfx=[(0, "alert")])),
        ("N", "こうして、ユウタの民泊への挑戦が始まった。", {}),
        ("N", "でもこの先、3つの落とし穴が待っていたのです…。", dict(say="でもこの先、みっつの落とし穴が待っていたのです。", sfx=[(0.2, "boing")])),
    ]),
    ("mint", 0.9, [
        ("M", "こんにちは、アキヤドのミナです！ まずは「民泊」をざっくり説明しますね。", dict(sfx=[(0, "pop")])),
        ("M", "民泊は、家やお部屋を、旅行に来た人に貸して、お金をいただくこと。ホテルの小さい版みたいなものです。", dict(sfx=[(0.3, "pop"), (2.4, "coin")])),
        ("M", "ただし、始めるには、役所への届け出が必要です。", dict(sfx=[(0.4, "pop")])),
        ("M", "それから、どんな家でもできるわけではありません。ここ、あとで大事になりますよ！", dict(sfx=[(0.4, "pop")])),
        ("Y", "ふむふむ。でも、なんだか難しそう…。", dict(sfx=[(0, "pop")])),
    ]),
    ("hall", 1.0, [
        ("N", "落とし穴その1。「誰でも簡単に稼げる」。", dict(say="落とし穴、その一。誰でも簡単に稼げる。", sfx=[(0, "boing")])),
        ("Y", "おっ、無料セミナーだって！ 行ってみよう。", dict(sfx=[(0, "alert")])),
        ("U", "民泊はねぇ、誰でも、簡単に、すぐ稼げるんですよ〜！", dict(sfx=[(0, "bling")])),
        ("U", "私のサポートを受ければ、もう安心！", {}),
        ("U", "ほら見て！ 成功した人たちの声です！", dict(sfx=[(0.3, "bling")])),
        ("Y", "月収アップ…！？ みんな、稼いでる…！", {}),
        ("Y", "すごい！ でも、僕、何も知らないんですけど…。", {}),
        ("U", "だいじょ〜ぶ！ 全部教えます。サポート代は少しかかりますが、すぐに元が取れますから！", {}),
        ("Y", "い、いくらなんですか？", {}),
        ("U", "こちらです！", dict(sfx=[(0.3, "boing")])),
        ("Y", "た、高い…！ そんなお金、ないです…。", {}),
        ("U", "お金がなくても大丈夫！ 借りればいいんです。稼いだ分から返せますから。", {}),
        ("U", "それに、この値段は、今日だけですよ〜。", dict(sfx=[(0.6, "bling")])),
        ("Y", "きょ、今日だけ…！？", {}),
        ("M", "ちょっと待ったー！！", dict(pre=0.7, sfx=[(-0.7, "freeze"), (0, "whoosh")])),
        ("Y", "うわっ、ミナさん！？", {}),
        ("M", "ユウタさん、それ、よくある落とし穴です！", {}),
    ]),
    ("sky", 0.9, [
        ("M", "こんな言葉が出てきたら、立ち止まってください。", {}),
        ("M", "1つめ。「誰でも簡単に、すぐ稼げる」。本当に簡単なら、高いお金を払って教わる必要はありませんよね。", dict(say="ひとつめ。誰でも簡単に、すぐ稼げる。本当に簡単なら、高いお金を払って教わる必要はありませんよね。", sfx=[(0, "pop")])),
        ("M", "2つめ。「お金がなければ、借りればいい」。借金をしてまで契約するのは、やめましょう。", dict(say="ふたつめ。お金がなければ、借りればいい。借金をしてまで契約するのは、やめましょう。", sfx=[(0, "pop")])),
        ("M", "3つめ。「今日だけ」「今すぐ決めて」。急がせるのは、考える時間をなくすため。その場では、契約しないことです。", dict(say="みっつめ。今日だけ、今すぐ決めて。急がせるのは、考える時間をなくすため。その場では、契約しないことです。", sfx=[(0, "pop")])),
        ("M", "それから、広告やSNSの「成功した人の声」も、本当かどうか分かりません。うのみにしないでくださいね。", dict(say="それから、広告やエスエヌエスの、成功した人の声も、本当かどうか分かりません。うのみにしないでくださいね。", sfx=[(0, "pop")])),
        ("M", "実際に、「すぐ元が取れる」と言われて契約したのに稼げず、やめたいと言っても応じてもらえない、という相談が寄せられています。", {}),
        ("Y", "あ、危なかった…！", {}),
        ("M", "困ったときは、消費者ホットライン「188（いやや）」に電話すれば、近くの相談窓口につながりますよ。", dict(say="困ったときは、消費者ホットライン、いち、はち、はち、いややに電話すれば、近くの相談窓口につながりますよ。", sfx=[(0.5, "ding")])),
    ]),
    ("mint", 0.9, [
        ("M", "ここでクイズです！", dict(sfx=[(0, "chime")])),
        ("M", "ウマイ先生のセリフで、危ない言葉はどれでしょう？", {}),
        ("M", "A、「すぐに元が取れる」。B、「借りればいい」。C、「今日だけ」。", dict(say="エー、すぐに元が取れる。ビー、借りればいい。シー、今日だけ。", sfx=[(0.1, "pop"), (2.0, "pop"), (3.6, "pop")])),
        ("M", "正解は…、ぜんぶです！", dict(pre=3.4, sfx=[(-3.4, "tick"), (-2.4, "tick"), (-1.4, "tick"), (0.9, "ding")])),
        ("Y", "ぜ、ぜんぶ…！？", dict(sfx=[(0, "boing")])),
        ("M", "どれか1つでも出てきたら、要注意。その場では決めないでくださいね。", dict(say="どれかひとつでも出てきたら、要注意。その場では決めないでくださいね。")),
    ]),
    ("peach", 0.9, [
        ("N", "落とし穴その2。「この物件、民泊できますよ」。", dict(say="落とし穴、その二。この物件、民泊できますよ。", sfx=[(0, "boing")])),
        ("N", "気を取り直して、自分で物件を探し始めたユウタ。", {}),
        ("U", "お客さ〜ん、いい物件ありますよ。駅近、きれい、民泊できます！", dict(say="お客さ〜ん、いい物件ありますよ。えきちか、きれい、民泊できます！", sfx=[(0, "bling")])),
        ("Y", "本当ですか！？ じゃあ、すぐ買い…", {}),
        ("M", "ストーップ！！ ユウタさん、その「民泊できます」、確かめました？", dict(sfx=[(0, "whoosh")])),
        ("Y", "え、だって、できるって…。", {}),
        ("M", "実は、こんなことがあるんです。", dict(sfx=[(0.3, "pop")])),
        ("M", "マンションのルールで、民泊が禁止されていることがあります。", dict(sfx=[(0, "pop")])),
        ("M", "地域によっては、民泊ができない場所や、できない時期があります。", dict(sfx=[(0, "pop")])),
        ("M", "火事に備えた設備などが必要で、思わぬ費用がかかることもあります。", dict(sfx=[(0, "pop")])),
        ("M", "買ってから「やっぱりできない」と分かっても、取り返しがつきません。", {}),
        ("Y", "ひぇ〜…。", dict(say="ひええ〜。", sfx=[(0, "boing")])),
    ]),
    ("sky", 0.9, [
        ("M", "買う前・借りる前に、この2つを確かめましょう。", dict(say="買う前、借りる前に、このふたつを確かめましょう。")),
        ("M", "1つめ。役所に「この場所で民泊できますか？」と聞く。", dict(say="ひとつめ。役所に、この場所で民泊できますか？と聞く。", sfx=[(0, "pop")])),
        ("M", "2つめ。マンションなら、管理規約、つまりマンションのルールで、民泊が禁止されていないか見る。", dict(say="ふたつめ。マンションなら、管理規約、つまりマンションのルールで、民泊が禁止されていないか見る。", sfx=[(0, "pop")])),
        ("M", "「できます」と言われても、自分の目で確かめるのがいちばんです！", {}),
    ]),
    ("yellow", 0.9, [
        ("N", "落とし穴その3。開業したのに…。", dict(say="落とし穴、その三。開業したのに。", sfx=[(0, "boing")])),
        ("N", "そして、ついに、ユウタの宿がオープン！", dict(sfx=[(0.3, "chime")])),
        ("Y", "やった〜！ 予約も入ってきたぞ！", {}),
        ("Y", "ん？ なんだろう。", dict(pre=0.4, sfx=[(-0.4, "alert")])),
        ("Y", "えっ、キャンセル！？ 大変だ、すぐ確認しないと！", {}),
        ("M", "待って待って！ そのリンク、押しちゃダメです！", dict(sfx=[(0, "whoosh")])),
        ("M", "これは、予約サイトのふりをした、偽のメッセージかもしれません。リンクの先で、クレジットカードの番号を入力させようとするんです。", dict(sfx=[(0.5, "pop")])),
        ("Y", "本物そっくりなんだけど…！", {}),
        ("M", "そう、見分けにくいのがこわいところ。実際に、宿や予約した人を狙った偽のメッセージに、国も注意を呼びかけています。", {}),
    ]),
    ("sky", 0.9, [
        ("M", "こう覚えておいてください。", {}),
        ("M", "1つめ。「急いで！」と言うメッセージのリンクは、押さない。", dict(say="ひとつめ。急いで！と言うメッセージのリンクは、押さない。", sfx=[(0, "pop")])),
        ("M", "2つめ。予約の確認は、いつも使っている公式のアプリやサイトから。", dict(say="ふたつめ。予約の確認は、いつも使っている公式のアプリやサイトから。", sfx=[(0, "pop")])),
        ("M", "3つめ。メッセージでカード番号を聞かれたら、入力しない。", dict(say="みっつめ。メッセージでカード番号を聞かれたら、入力しない。", sfx=[(0, "pop")])),
    ]),
    ("mint", 0.9, [
        ("M", "最後に、ふりかえりの〇✕クイズです！", dict(say="最後に、ふりかえりの、マルバツクイズです！", sfx=[(0, "chime")])),
        ("M", "第1問。「今日だけ」と言われたら、すぐ契約したほうがお得。〇か、✕か？", dict(say="第一問。今日だけと言われたら、すぐ契約したほうがお得。マルか、バツか？")),
        ("M", "正解は✕！ 急がせるのは、考える時間をなくすためでしたね。", dict(say="正解はバツ！ 急がせるのは、考える時間をなくすためでしたね。", pre=3.0, sfx=[(-3.0, "tick"), (-2.0, "tick"), (-1.0, "tick"), (0, "ding")])),
        ("M", "第2問。「民泊できます」と言われた物件は、役所とマンションのルールで確かめる。〇か、✕か？", dict(say="第二問。民泊できますと言われた物件は、役所とマンションのルールで確かめる。マルか、バツか？")),
        ("M", "正解は〇！ 自分の目で確かめるのがいちばんです。", dict(say="正解はマル！ 自分の目で確かめるのがいちばんです。", pre=3.0, sfx=[(-3.0, "tick"), (-2.0, "tick"), (-1.0, "tick"), (0, "ding")])),
        ("M", "第3問。「24時間以内に確認を」というメッセージが来たら、リンクからすぐ確認する。〇か、✕か？", dict(say="第三問。二十四時間以内に確認を、というメッセージが来たら、リンクからすぐ確認する。マルか、バツか？")),
        ("M", "正解は✕！ 確認は、いつも使っている公式のアプリやサイトからでしたね。", dict(say="正解はバツ！ 確認は、いつも使っている公式のアプリやサイトからでしたね。", pre=3.0, sfx=[(-3.0, "tick"), (-2.0, "tick"), (-1.0, "tick"), (0, "ding")])),
        ("Y", "ぜんぶ正解！ もう、だまされないぞ！", dict(sfx=[(0, "chime")])),
    ]),
    ("yellow", 5.0, [
        ("Y", "ミナさんのおかげで、3つの落とし穴、ぜんぶ避けられました！", dict(say="ミナさんのおかげで、みっつの落とし穴、ぜんぶ避けられました！")),
        ("M", "よかったです！ 民泊は、正しく始めれば、旅行者にも地域にも喜ばれる、すてきな仕事です。", {}),
        ("M", "怪しい話に出会ったら、ひとりで決めずに、まず誰かに相談してくださいね。", {}),
        ("N", "落とし穴は、知っていれば避けられる。", dict(sfx=[(0, "chime")])),
        ("M", "民泊の始め方は、アキヤドの記事でも紹介しています。ご相談も無料ですよ！", dict(sfx=[(0.4, "pop")])),
    ]),
]
LEAD, GAP = 0.6, 0.35


def wrap(s, n=31):
    """字幕の改行。行数を決めてから、各行がほぼ同じ長さになるよう句読点の後で分ける"""
    import math
    lines = []
    while len(s) > n:
        k = math.ceil(len(s) / n); target = len(s) / k
        best, cut = None, -1
        for i in range(max(1, int(target * 0.55)), min(n, len(s) - 1)):
            if s[i] in "。、！？…":
                sc = abs(i + 1 - target)
                if best is None or sc < best:
                    best, cut = sc, i
        if cut < 0:
            cut = min(n, round(target)) - 1
        while cut + 1 < len(s) and s[cut + 1] in "」』）！？…":
            cut += 1
        lines.append(s[:cut + 1].strip()); s = s[cut + 1:].strip()
    if s:
        lines.append(s)
    return lines


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


SCENE_JS = r"""
const VNAME={N:'ナレーション',Y:'ユウタ',M:'ミナ',U:'ウマイ先生'},VCOL={N:'#5d6b64',Y:G,M:T,U:'#6b3fa0'};
const talking=(s,t)=>LINES.some(l=>l[2]===s&&t>=l[0]&&t<l[1]);
function subtitle(l,t){
  const lines=l[3],fs=42,h=lines.length*fs*1.45+40,w=1560,y=1048-h,o=clamp((t-l[0]+.05)/.2)*clamp((l[1]+.3-t)/.2);
  const name=l[2]==='N'?'':`<rect x="${960-w/2+28}" y="${y-26}" width="${VNAME[l[2]].length*30+44}" height="52" rx="26" fill="${VCOL[l[2]]}"/><text x="${960-w/2+50}" y="${y+9}" font-size="30" font-weight="900" fill="#fff">${VNAME[l[2]]}</text>`;
  return `<g opacity="${o}"><rect x="${960-w/2}" y="${y}" width="${w}" height="${h}" rx="24" fill="${DG}" opacity=".93"/>${name}${lines.map((s,i)=>`<text x="960" y="${y+28+fs*1.08+i*fs*1.45}" text-anchor="middle" font-size="${fs}" font-weight="700" fill="${l[2]==='N'?'#e9f1ec':'#fff'}" letter-spacing="1">${s}</text>`).join('')}</g>`;
}
const P=(x,y,s,o,t)=>person(x,y,s,Object.assign({t},o,{talk:o.who?talking(o.who,t):false}));
function chapter(no,title,p){ // 「落とし穴①」の章の見出し
  if(p<=0||p>=1)return '';const a=clamp(p*6)*clamp((1-p)*5),s=bk(clamp(p*4));
  return `<g opacity="${a}"><rect width="1920" height="1080" fill="#1f2a24" opacity=".55"/><g transform="translate(960,470) scale(${s}) translate(-960,-470)"><rect x="420" y="330" width="1080" height="290" rx="36" fill="#fff"/><rect x="760" y="300" width="400" height="76" rx="38" fill="${T}"/><text x="960" y="352" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">落とし穴 ${no}</text><text x="960" y="520" text-anchor="middle" font-size="84" font-weight="900" fill="${DG}">${title}</text></g></g>`;
}
function phoneUI(x,y,s,inner,p=1){return pop(x,y,p,`<g transform="translate(${x},${y}) scale(${s})"><rect x="-190" y="-340" width="380" height="680" rx="48" fill="#22252b"/><rect x="-172" y="-300" width="344" height="610" rx="20" fill="#fff"/><rect x="-50" y="-326" width="100" height="14" rx="7" fill="#3a3e46"/>${inner}</g>`)}
function checkRow(x,y,w,no,title,note,p,c=G){return fade(p,`${box(x,y-62,w,124,62)}<circle cx="${x+66}" cy="${y}" r="42" fill="${c}"/><text x="${x+66}" y="${y+16}" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">${no}</text><text x="${x+130}" y="${y+(note?-4:15)}" font-size="${title.length>16?38:44}" font-weight="900" fill="${DG}">${title}</text>${note?`<text x="${x+130}" y="${y+40}" font-size="28" font-weight="700" fill="#4a5a52">${note}</text>`:''}`,0)}
function speedLines(x,y,a){let s='';for(let k=0;k<9;k++){const yy=y-260+k*58,len=160+rnd(k)*220;s+=`<rect x="${x+60+rnd(k+9)*80}" y="${yy}" width="${len}" height="8" rx="4" fill="#fff" opacity="${.8*a}"/>`}return s}
function hall(t){ // セミナー会場
  let s=`<rect width="1920" height="1080" fill="#3a2a4f"/><rect y="760" width="1920" height="320" fill="#2a1e3a"/>`;
  s+=`<path d="M760 0 L560 860 L1500 860 L1300 0Z" fill="#fff6c9" opacity="${.12+.04*Math.sin(t*3)}"/>`;
  s+=`<rect x="420" y="700" width="1380" height="70" rx="10" fill="#6b4a8a"/><rect x="420" y="690" width="1380" height="18" rx="8" fill="#8a66ad"/>`;
  s+=`<path d="M0 0 H300 Q260 400 300 860 H0Z" fill="#a23b3b"/><path d="M1920 0 H1620 Q1660 400 1620 860 H1920Z" fill="#a23b3b"/><path d="M60 0 v860 M140 0 v860 M220 0 v860 M1700 0 v860 M1780 0 v860 M1860 0 v860" stroke="#8a2f2f" stroke-width="10"/>`;
  s+=`<rect x="560" y="120" width="1000" height="96" rx="14" fill="#e8b950"/><text x="1060" y="186" text-anchor="middle" font-size="56" font-weight="900" fill="#3a2a4f">民泊で稼ぐ！特別セミナー</text>`;
  for(let k=0;k<7;k++){const x=520+k*190;s+=`<circle cx="${x}" cy="${120+Math.sin(t*4+k)*6}" r="10" fill="#fff6c9" opacity="${.5+.5*Math.sin(t*6+k)}"/>`}
  return s;
}
function roomNight(t){ // 夜の部屋
  let s=bg(t,'night');
  for(let k=0;k<40;k++){const x=rnd(k)*1920,y=rnd(k+50)*380;s+=`<circle cx="${x}" cy="${y}" r="${1.5+rnd(k+90)*2.5}" fill="#fff" opacity="${.4+.5*Math.abs(Math.sin(t*2+k))}"/>`}
  return s;
}
function scene(i,t,lt){
  const L=SL[i],E=SE[i],at=(k,d=.5,o=0)=>seg(lt,L[k]+o,L[k]+o+d),on=k=>lt>=L[k];
  let s='';
  if(i===0){
    s+=house(1380,GROUND,.9,0);
    s+=P(560,GROUND,.92,{c:'owner',who:'Y',pose:on(2)?'phone':'think',mood:lt>L[2]+1.6?'happy':'worry'},t);
    s+=phoneUI(960,470,.78,`<rect x="-172" y="-300" width="344" height="70" fill="${G}"/><text x="0" y="-252" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">検索</text><text x="0" y="-150" text-anchor="middle" font-size="60" font-weight="900" fill="${DG}">民泊</text><text x="0" y="-90" text-anchor="middle" font-size="26" font-weight="700" fill="#4a5a52">家を旅行者に貸して収入に</text>${house(0,150,.42,1)}`,at(2,.5)*(1-seg(lt,L[3],L[3]+.4)));
    [[880,760],[1120,800],[1360,760]].forEach(([x,y],k)=>{s+=pop(x,y,seg(lt,L[4]+.6+k*.35,L[4]+1+k*.35),`<ellipse cx="${x}" cy="${y}" rx="110" ry="36" fill="#141a2b"/><text x="${x}" y="${y-50}" text-anchor="middle" font-size="70" font-weight="900" fill="${Y}" stroke="#141a2b" stroke-width="10" paint-order="stroke">？</text>`)});
    const tp=seg(lt,E[4]+.3,E[4]+1);
    s+=pop(960,470,tp,`<rect width="1920" height="1080" fill="#000" opacity=".35"/><rect x="330" y="300" width="1260" height="330" rx="40" fill="#fff"/><rect x="700" y="262" width="520" height="76" rx="38" fill="${G}"/><text x="960" y="314" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">アキヤド劇場　第1話</text><text x="960" y="470" text-anchor="middle" font-size="96" font-weight="900" fill="${DG}">それ、民泊の</text><text x="960" y="590" text-anchor="middle" font-size="96" font-weight="900" fill="${T}">落とし穴です</text>`);
    s+=fade(seg(lt,.2,.6)*(1-seg(lt,5,5.5)),`<rect x="40" y="40" width="760" height="56" rx="28" fill="#000" opacity=".4"/><text x="70" y="78" font-size="26" font-weight="700" fill="#fff">※ 相談例をもとにしたフィクションです。人物・会社は架空です</text>`,0);
  }
  if(i===1){
    const wx=1560+360*(1-eo(seg(lt,0,.9)));
    s+=P(wx,GROUND,.86,{c:'staff',who:'M',pose:lt<.9?'walk':'present',mood:'happy',flip:true},t);
    s+=fade(at(1),`${box(150,250,1180,420,30,'rgba(255,255,255,.88)')}`,0);
    s+=pop(360,520,at(1,.5,.2),house(360,600,.55,1));
    s+=arrow(560,470,760,470,eo(at(1,.6,.9)),G,10);
    s+=pop(900,500,at(1,.5,1.2),`<g transform="translate(900,560)">${person(0,0,.42,{c:'guest1',t:lt,mood:'happy',flip:true}).replace('translate(0,','translate(0,')}</g>`);
    s+=arrow(1000,470,1180,470,eo(at(1,.6,2)),T,10)+pop(1240,470,at(1,.5,2.4),coin(1240,470,46));
    s+=TX(360,640,'家・お部屋',30,DG,900)+'';
    s+=fade(at(1,.5,.4),TX(900,640,'旅行者が泊まる',30,DG,900),0)+fade(at(1,.5,2.4),TX(1240,640,'お金が入る',30,DG,900),0);
    s+=pop(560,790,at(2),`${box(260,730,600,120,60)}${icon(330,790,40,'doc',G,'#fff',.6)}<text x="390" y="805" font-size="40" font-weight="900" fill="${DG}">役所への届け出が必要</text>`);
    s+=pop(1060,790,at(3),`${box(900,730,520,120,60)}${icon(970,790,40,'home',T,'#fff',.6)}<text x="1030" y="805" font-size="40" font-weight="900" fill="${DG}">どんな家でもOK…？</text>`);
    s+=P(180-200*(1-eo(at(4,.6))),GROUND+40,.62,{c:'owner',who:'Y',pose:'think',mood:'worry'},t);
  }
  if(i===2){
    const inHall=on(2);
    if(!inHall){s+=bg(t,'night');s+=P(520,GROUND,.92,{c:'owner',who:'Y',pose:'phone',mood:'happy'},t);
      s+=phoneUI(1150,480,.92,`<rect x="-172" y="-300" width="344" height="610" fill="#fff4d6"/><text x="0" y="-200" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">民泊で月収アップ！</text><text x="0" y="-130" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">初心者でも簡単！</text>${coin(-80,0,50)}${coin(70,-20,40)}${coin(10,80,34)}<rect x="-140" y="180" width="280" height="80" rx="40" fill="${T}"/><text x="0" y="234" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">無料セミナー</text>`,at(1,.5));}
    else{
      const fr=lt>=L[14]-.7,fz=clamp((lt-(L[14]-.7))/.25);
      let g=hall(fr?L[14]-.7:lt);
      const tu=fr?L[14]-.7:lt;
      g+=P(1180,750,.9,{c:'umai',who:'U',pose:on(9)?'point':(on(11)?'open':'cheer'),mood:'happy'},tu);
      [[900,320],[1460,300],[1300,520],[980,560]].forEach(([x,y],k)=>{g+=sparkle(x,y,1.2,tu,k)});
      g+=P(330,GROUND+80,.9,{c:'owner',who:'Y',pose:on(13)?'shake':(on(10)?'think':'stand'),mood:on(10)?'worry':'happy'},tu);
      g+=pop(1500,420,at(9,.5,.2),`<g transform="rotate(${-6+Math.sin(tu*3)*2} 1500 420)">${box(1310,250,380,340,16)}<text x="1500" y="320" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">サポート代</text><text x="1500" y="440" text-anchor="middle" font-size="88" font-weight="900" fill="${T}">数十万円</text><text x="1500" y="520" text-anchor="middle" font-size="28" font-weight="700" fill="#4a5a52">※今日だけの特別価格</text></g>`);
      g+=pop(760,380,at(4,.5,.2)*(1-seg(lt,L[6],L[6]+.4)),`<g transform="rotate(-4 760 380)">${box(500,200,520,380,18)}<text x="760" y="262" text-anchor="middle" font-size="36" font-weight="900" fill="#6b3fa0">成功者の声</text>${[['月収アップ！','Aさん'],['副業で大成功！','Bさん'],['人生が変わりました','Cさん']].map(([a,b],k)=>`<circle cx="560" cy="${325+k*85}" r="28" fill="#d9cbe6"/><text x="600" y="${336+k*85}" font-size="32" font-weight="900" fill="${DG}">「${a}」</text><text x="990" y="${336+k*85}" text-anchor="end" font-size="24" font-weight="700" fill="#777">${b}</text>`).join('')}<text x="760" y="560" text-anchor="middle" font-size="22" font-weight="700" fill="#999">※個人の感想です（？）</text></g>`);
      g+=pop(800,300,at(12,.4,.5),`<g transform="rotate(-10 800 300)"><rect x="620" y="240" width="360" height="120" rx="20" fill="#e53935"/><text x="800" y="322" text-anchor="middle" font-size="64" font-weight="900" fill="#fff">今日だけ！</text></g>`);
      if(on(11))g+=fade(at(11,.5,.5),chip(740,580,'借りればいい',40,'#6b3fa0','#fff',1),0);
      s+=fr?`<g filter="url(#gray)">${g}</g><rect width="1920" height="1080" fill="#000" opacity="${.25*fz}"/>`:g;
      if(fr){s+=pop(960,170,fz,`<g opacity=".9"><rect x="880" y="110" width="50" height="120" rx="10" fill="#fff"/><rect x="990" y="110" width="50" height="120" rx="10" fill="#fff"/></g>`);
        const mx=760+900*(1-eo(at(14,.45)));s+=speedLines(mx,700,1-at(14,.8,.5))+P(mx,GROUND+60,.95,{c:'staff',who:'M',pose:'point',mood:'happy',flip:true},t);}
    }
    s+=chapter('①','「誰でも簡単に稼げる」',seg(lt,L[0]-.2,E[0]+.4));
  }
  if(i===3){
    s+=P(240,GROUND,.84,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    const fadeRows=1-seg(lt,L[7],L[7]+.4);
    let g=fade(at(0),`<text x="1180" y="250" text-anchor="middle" font-size="50" font-weight="900" fill="${DG}">こんな言葉が出たら、立ち止まる</text>`,0);
    g+=checkRow(520,380,1340,'1','「誰でも簡単に、すぐ稼げる」','本当に簡単なら、高いお金を払って教わる必要はない',at(1),T);
    g+=checkRow(520,540,1340,'2','「お金がなければ、借りればいい」','借金をしてまで契約しない',at(2),T);
    g+=checkRow(520,700,1340,'3','「今日だけ」「今すぐ決めて」','急がせるのは、考える時間をなくすため',at(3),T);
    g+=pop(1190,830,at(4,.5),`<rect x="560" y="790" width="1260" height="76" rx="38" fill="#6b3fa0"/><text x="1190" y="840" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">＋ 広告やSNSの「成功した人の声」も、うのみにしない</text>`);
    s+=`<g opacity="${fadeRows}">${g}</g>`;
    s+=pop(1660,170,at(6,.4),`${face('yf',1660,170,64,'owner',G,'worry',lt)}`)+(on(5)?'':'');
    s+=pop(1180,520,at(7,.5),`${box(640,330,1080,380,40)}<text x="1180" y="420" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">困ったときは</text><text x="1180" y="550" text-anchor="middle" font-size="120" font-weight="900" fill="${T}">188</text><text x="1180" y="640" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">消費者ホットライン（いやや）</text>`);
  }
  if(i===5){
    const umaiIn=at(2,.6),umaiOut=seg(lt,L[10],L[10]+1.2),diag=at(6,.5)*(1-seg(lt,L[11]-.2,L[11]+.3));
    s+=house(1260,GROUND,.95,.35);
    s+=pop(1520,500,at(1,.5),`<rect x="1490" y="440" width="10" height="420" fill="#6a5646"/><rect x="1430" y="440" width="230" height="110" rx="12" fill="#fff"/><text x="1545" y="512" text-anchor="middle" font-size="46" font-weight="900" fill="${T}">売り物件</text>`);
    s+=P(330+200*eo(at(1,1.4)),GROUND,.9,{c:'owner',who:'Y',pose:lt<L[1]+1.4&&on(1)?'walk':(on(11)?'think':'stand'),mood:on(5)?'worry':'happy'},t);
    if(umaiIn>0)s+=P(1660+500*umaiOut,GROUND,.86*eo(umaiIn)+.001,{c:'umai',who:'U',pose:umaiOut>0?'walk':'open',mood:'happy',disguise:true,flip:true},t);
    if(on(4))s+=P(1040+700*(1-eo(at(4,.45))),GROUND+40,.84,{c:'staff',who:'M',pose:on(6)?'present':'point',mood:'happy',flip:true},t)+speedLines(1040+700*(1-eo(at(4,.45))),700,1-at(4,.8,.3));
    if(diag>0){let g=`<rect width="1920" height="1080" fill="#fff" opacity="${.5*diag}"/>`+box(240,230,1440,600,36);
      g+=`<text x="960" y="310" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">「民泊できます」でも、こんなことが…</text>`;
      [['🏢','マンションのルールで','禁止されていることも'],['🗺️','地域によって','できない場所・時期も'],['🧯','火事に備えた設備など','思わぬ費用も']].forEach(([e,a,b],k)=>{const x=480+k*480,p=at(7+k,.5);
        g+=pop(x,560,p,`<circle cx="${x}" cy="480" r="96" fill="${k===2?T:G}"/>${k===0?`<g transform="translate(${x},480)"><rect x="-40" y="-56" width="80" height="112" rx="6" fill="#fff"/><path d="M-26 -36 h16 M10 -36 h16 M-26 -6 h16 M10 -6 h16 M-26 24 h16 M10 24 h16" stroke="${G}" stroke-width="10"/></g>`:k===1?`<g transform="translate(${x},470)"><path d="M0 50 C-50 -10 -50 -60 0 -60 C50 -60 50 -10 0 50Z" fill="#fff"/><circle cy="-22" r="18" fill="${G}"/></g>`:`<g transform="translate(${x},480)"><rect x="-26" y="-40" width="52" height="96" rx="14" fill="#fff"/><rect x="-14" y="-62" width="28" height="22" fill="#fff"/><path d="M14 -56 h34" stroke="#fff" stroke-width="10" stroke-linecap="round"/></g>`}<text x="${x}" y="645" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">${a}</text><text x="${x}" y="700" text-anchor="middle" font-size="34" font-weight="700" fill="#4a5a52">${b}</text>`)});
      g+=fade(at(10,.4),`<rect x="560" y="740" width="800" height="70" rx="35" fill="${T}"/><text x="960" y="788" text-anchor="middle" font-size="36" font-weight="900" fill="#fff">買ってからでは、取り返しがつかない</text>`,0);
      s+=`<g opacity="${diag}">${g}</g>`;}
    s+=chapter('②','「この物件、民泊できますよ」',seg(lt,L[0]-.2,E[0]+.4));
  }
  if(i===6||i===8){
    s+=P(240,GROUND,.84,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    if(i===6){s+=fade(at(0),`<text x="1180" y="270" text-anchor="middle" font-size="50" font-weight="900" fill="${DG}">買う前・借りる前に、確かめる</text>`,0);
      s+=checkRow(520,420,1340,'1','役所に聞く','「この場所で民泊できますか？」',at(1));
      s+=checkRow(520,600,1340,'2','マンションのルールを見る','管理規約で、民泊が禁止されていないか',at(2));
      s+=pop(1180,770,at(3,.5),`<rect x="760" y="730" width="840" height="80" rx="40" fill="${T}"/><text x="1180" y="784" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">「できます」でも、自分の目で確かめる</text>`);}
    else{s+=fade(at(0),`<text x="1180" y="250" text-anchor="middle" font-size="50" font-weight="900" fill="${DG}">偽のメッセージから身を守る</text>`,0);
      s+=checkRow(520,380,1340,'1','「急いで！」のリンクは押さない','',at(1));
      s+=checkRow(520,540,1340,'2','確認は、いつもの公式アプリ・サイトから','',at(2));
      s+=checkRow(520,700,1340,'3','カード番号を聞かれたら、入力しない','',at(3),T);}
  }
  if(i===7){
    const k=eo(at(1,1.6,.3)),showPhone=at(3,.4,-.4)*(1-at(5,.4,.3)),fake=at(6,.5,.4)*(1-seg(lt,E[8]-.2,E[8]+.3));
    s+=house(1180,GROUND,1.0,k);
    s+=[[1000,360],[1380,330],[1300,520]].map(([x,y],j)=>`<g opacity="${k}">${sparkle(x,y,1.3,lt,j)}</g>`).join('');
    const gw=eo(at(1,1.6,1));s+=P(1820-gw*260,GROUND,.8,{c:'guest1',pose:gw<1&&on(1)?'walk':'wave',flip:true},t)+P(1700-gw*240,GROUND,.74,{c:'guest2',pose:gw<1&&on(1)?'walk':'stand',mood:'happy',flip:true,seed:2},t);
    s+=P(420,GROUND,.92,{c:'owner',who:'Y',pose:on(5)?'think':(on(3)?'phone':(on(2)?'cheer':'stand')),mood:on(4)?'worry':'happy'},t);
    if(on(5))s+=P(760+600*(1-eo(at(5,.4))),GROUND+40,.84,{c:'staff',who:'M',pose:on(6)?'present':'point',mood:'happy',flip:true},t)+speedLines(760+600*(1-eo(at(5,.4))),700,1-at(5,.8,.3));
    const shake=on(4)&&!on(5)?Math.sin(lt*40)*6:0;
    s+=phoneUI(1000+shake,480,1.02,`<rect x="-172" y="-300" width="344" height="80" fill="#fdecea"/><text x="0" y="-248" text-anchor="middle" font-size="30" font-weight="900" fill="#d32f2f">【重要】</text><text x="0" y="-150" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">予約の確認が必要です</text><text x="0" y="-80" text-anchor="middle" font-size="26" font-weight="700" fill="#2c3a33">24時間以内に確認しないと</text><text x="0" y="-40" text-anchor="middle" font-size="26" font-weight="700" fill="#2c3a33">予約はキャンセルされます</text><rect x="-130" y="40" width="260" height="76" rx="38" fill="#d32f2f"/><text x="0" y="90" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">今すぐ確認</text>${on(5)?`<g opacity="${at(5,.3)}"><path d="M-120 20 L120 140 M120 20 L-120 140" stroke="#d32f2f" stroke-width="18" stroke-linecap="round"/></g>`:''}`,showPhone);
    if(on(4)&&!on(5)){const fp=at(4,1.2,.4);s+=`<path transform="translate(${1250-200*fp},${760-160*fp})" d="M0 0 L0 46 L12 34 L22 56 L32 51 L22 30 L38 30z" fill="#fff" stroke="${DG}" stroke-width="4" stroke-linejoin="round"/>`;}
    if(fake>0)s+=`<g opacity="${fake}">${phoneUI(1000,480,1.02,`<rect x="-172" y="-300" width="344" height="70" fill="#e9eef5"/><text x="0" y="-254" text-anchor="middle" font-size="26" font-weight="900" fill="#2c3a33">予約サイト（？）</text><text x="-140" y="-170" font-size="26" font-weight="900" fill="${DG}">カード番号</text><rect x="-140" y="-150" width="280" height="56" rx="10" fill="#f2f6f3" stroke="#b9cfc1" stroke-width="3"/><text x="-140" y="-50" font-size="26" font-weight="900" fill="${DG}">有効期限・セキュリティコード</text><rect x="-140" y="-30" width="280" height="56" rx="10" fill="#f2f6f3" stroke="#b9cfc1" stroke-width="3"/>`,1)}${pop(1000,470,at(6,.4,1.6),`<g transform="rotate(-14 1000 470)"><circle cx="1000" cy="470" r="120" fill="none" stroke="#d32f2f" stroke-width="16"/><text x="1000" y="510" text-anchor="middle" font-size="120" font-weight="900" fill="#d32f2f">偽</text></g>`)}</g>`;
    s+=chapter('③','開業したのに…',seg(lt,L[0]-.2,E[0]+.4));
  }
  if(i===4){ // クイズ①
    s+=P(250,GROUND,.84,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    s+=P(1800,GROUND+60,.62,{c:'owner',who:'Y',pose:on(4)?'cheer':'think',mood:on(4)?'worry':'smile',flip:true},t);
    s+=pop(1120,180,at(0,.5),`<rect x="920" y="130" width="400" height="96" rx="48" fill="${T}"/><text x="1120" y="196" text-anchor="middle" font-size="54" font-weight="900" fill="#fff">クイズ</text>`);
    s+=fade(at(1,.5),`<text x="1120" y="320" text-anchor="middle" font-size="48" font-weight="900" fill="${DG}">ウマイ先生のセリフ、危ない言葉はどれ？</text>`,0);
    [['A','すぐに元が取れる'],['B','借りればいい'],['C','今日だけ']].forEach(([k2,w],k)=>{const x=620+k*440,y=540,p=at(2,.5,[0.1,2.0,3.6][k]);
      s+=pop(x,y,p,`${box(x-200,y-130,400,260,30)}<circle cx="${x}" cy="${y-60}" r="44" fill="${G}"/><text x="${x}" y="${y-44}" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">${k2}</text><text x="${x}" y="${y+60}" text-anchor="middle" font-size="${w.length>6?38:44}" font-weight="900" fill="${DG}">「${w}」</text>${pop(x,y,seg(lt,L[3]+.9+k*.15,L[3]+1.3+k*.15),`<circle cx="${x}" cy="${y}" r="150" fill="none" stroke="#e53935" stroke-width="16"/>`)}`)});
    const cd=lt-(L[3]-3.4);if(cd>0&&cd<3.4){const n=3-Math.floor(cd);s+=pop(1120,800,clamp((cd%1)*4),`<circle cx="1120" cy="800" r="70" fill="${Y}"/><text x="1120" y="830" text-anchor="middle" font-size="84" font-weight="900" fill="${DG}">${Math.max(1,n)}</text>`)}
    s+=pop(1060,810,at(3,.4,.8),`<rect x="780" y="760" width="560" height="100" rx="50" fill="#e53935"/><text x="1060" y="828" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">ぜんぶ危ない！</text>`);
  }
  if(i===9){ // ふりかえり〇✕クイズ
    s+=P(250,GROUND,.84,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    s+=P(1800,GROUND+60,.62,{c:'owner',who:'Y',pose:on(7)?'cheer':'think',mood:'happy',flip:true},t);
    s+=pop(1120,170,at(0,.5),`<rect x="830" y="120" width="580" height="96" rx="48" fill="${T}"/><text x="1120" y="186" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">〇✕クイズ</text>`);
    const QS=[['今日だけと言われたら、','すぐ契約したほうがお得','✕'],['「民泊できます」の物件は、','役所とマンションのルールで確かめる','〇'],['「24時間以内に確認を」が来たら、','リンクからすぐ確認する','✕']];
    QS.forEach(([a,b,ans],k)=>{const qi=1+k*2,ai=qi+1;if(!on(qi)||on(qi+2))return;
      const p=at(qi,.5);
      let g=`${box(560,280,1120,400,36)}<text x="1120" y="360" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">第${k+1}問</text><text x="1120" y="450" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">${a}</text><text x="1120" y="520" text-anchor="middle" font-size="${b.length>14?40:48}" font-weight="900" fill="${DG}">${b}</text>`;
      const rev=on(ai),okO=ans==='〇';
      g+=`<g opacity="${rev&&!okO?.3:1}"><circle cx="900" cy="610" r="0"/></g>`;
      ['〇','✕'].forEach((m2,j)=>{const x=920+j*400,hit=rev&&m2===ans;g+=`<g opacity="${rev&&!hit?.25:1}" transform="translate(${x},770) scale(${hit?1+.08*Math.sin(lt*8):1}) translate(${-x},-770)"><circle cx="${x}" cy="770" r="80" fill="${m2==='〇'?'#e53935':'#1e6fd9'}"/><text x="${x}" y="800" text-anchor="middle" font-size="84" font-weight="900" fill="#fff">${m2}</text></g>`});
      const cd=lt-(L[ai]-3.0);if(cd>0&&cd<3.0)g+=pop(1120,770,clamp((cd%1)*4),`<circle cx="1120" cy="770" r="56" fill="${Y}"/><text x="1120" y="796" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">${3-Math.floor(cd)}</text>`);
      s+=fade(p,g,20);});
    s+=pop(1120,480,at(7,.5),`${box(700,360,840,220,40)}<text x="1120" y="500" text-anchor="middle" font-size="64" font-weight="900" fill="${T}">ぜんぶ正解！</text>`);
  }
  if(i===10){
    s+=house(1000,GROUND,.95,1)+sparkle(800,330,1.3,lt,0)+sparkle(1220,300,1.1,lt,2);
    s+=P(400,GROUND,.9,{c:'owner',who:'Y',pose:'cheer',mood:'happy'},t)+P(1560,GROUND,.86,{c:'staff',who:'M',pose:on(4)?'present':'wave',mood:'happy',flip:true},t);
    s+=P(1790,GROUND,.66,{c:'guest2',pose:'wave',mood:'happy',flip:true,seed:2},t);
    s+=pop(960,470,at(3,.5)*(1-seg(lt,L[4],L[4]+.4)),`${box(330,230,1260,480,36)}<text x="960" y="310" text-anchor="middle" font-size="48" font-weight="900" fill="${DG}">落とし穴は、知っていれば避けられる</text>${[['1','「簡単に稼げる」「借りればいい」「今日だけ」は、立ち止まる'],['2','「民泊できます」は、役所とマンションのルールで確かめる'],['3','「急いで！」のメッセージのリンクは押さない']].map(([n,s2],k)=>`<circle cx="420" cy="${410+k*100}" r="32" fill="${k===2?T:G}"/><text x="420" y="${422+k*100}" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">${n}</text><text x="470" y="${422+k*100}" font-size="${s2.length>26?30:33}" font-weight="900" fill="#2c3a33">${s2}</text>`).join('')}`);
    s+=pop(960,420,at(4,.5),`${box(500,250,920,330,36)}${LOGO(760,290,1.2)}<rect x="620" y="400" width="680" height="92" rx="46" fill="${T}"/><text x="960" y="460" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">民泊の始め方・無料相談</text><text x="960" y="545" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">rivia-co.com/media.html</text>`);
    s+=fade(seg(lt,E[4]+.5,E[4]+1.2),`<rect width="1920" height="1080" fill="#1f2a24"/><text x="960" y="380" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">困ったときは 消費者ホットライン「188」</text><text x="960" y="480" text-anchor="middle" font-size="34" font-weight="700" fill="#dfe9e3">この動画は、国民生活センターなどに寄せられた相談例をもとにしたフィクションです。</text><text x="960" y="530" text-anchor="middle" font-size="34" font-weight="700" fill="#dfe9e3">登場する人物・会社は架空のものです。</text><text x="960" y="650" text-anchor="middle" font-size="30" font-weight="700" fill="#b8c9bf">${CREDIT}</text>${LOGO(810,730,1.1)}`,0);
  }
  return s;
}
window.draw=function(t){
  let i=SC.findIndex(([a,b])=>t>=a&&t<b);if(i<0)i=SC.length-1;
  const a=SC[i][0],TR=.6;
  const B=(j)=>THEME[j]==='hall'?'':(j===0?roomNight(t):bg(t,THEME[j]));
  let out=`${B(i)}${scene(i,t,t-a)}`;
  if(i>0&&t-a<TR){const k=eo((t-a)/TR),r=k*1150,pa=SC[i-1][0];
    out=`${B(i-1)}${scene(i-1,t,t-pa)}<clipPath id="iris"><circle cx="960" cy="540" r="${r}"/></clipPath><g clip-path="url(#iris)">${out}</g><circle cx="960" cy="540" r="${r}" fill="none" stroke="#fff" stroke-width="${26*(1-k)}" opacity="${1-k}"/>`;}
  const cur=LINES.find(l=>t>=l[0]-.05&&t<l[1]+.3);
  if(cur)out+=subtitle(cur,t);
  document.getElementById('s').innerHTML=`<defs><filter id="gray"><feColorMatrix type="saturate" values="0"/></filter></defs>`+out.replaceAll('__ROOT__',window.ROOT);
};
"""


def build_html(sc, lines):
    h = base.HTML
    a = h.index("const AV=[1,2,3,6,4,5];")
    b = h.index("</script></body></html>")
    sl = [[round(l[0] - sc[l[4]][0], 3) for l in lines if l[4] == i] for i in range(len(sc))]
    se = [[round(l[1] - sc[l[4]][0], 3) for l in lines if l[4] == i] for i in range(len(sc))]
    head = (f"const SC={json.dumps(sc)};const LINES={json.dumps(lines, ensure_ascii=False)};const SL={json.dumps(sl)};const SE={json.dumps(se)};"
            f"const THEME={json.dumps([s[0] for s in SCENES])};const CREDIT={json.dumps(CREDIT, ensure_ascii=False)};")
    return h[:a] + head + SCENE_JS + h[b:]


def main():
    args = sys.argv[1:]
    hq = "--hq" in args; args = [x for x in args if x != "--hq"]
    prev = None
    if "--preview" in args:
        k = args.index("--preview"); prev = [float(x) for x in args[k + 1:]]; args = args[:k]
    out = args[0] if args else os.path.join(ROOT, "docs", "media", "akiyado-theater-ep1.mp4")
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
            od = os.path.join(tempfile.gettempdir(), "theater_preview"); os.makedirs(od, exist_ok=True)
            subprocess.run(["node", js, h, od, "preview", json.dumps(prev)], check=True, env=env)
            print("preview", od, "長さ", round(dur, 1), "秒", [round(a, 1) for a, _ in sc]); return
        fr = os.path.join(tmp, "fr"); os.makedirs(fr)
        subprocess.run(["node", js, h, fr, "video", str(int(dur * FPS))], check=True, env=env)
        import pop_audio
        wav = os.path.join(tmp, "audio.wav"); pop_audio.write(wav, dur, sfx, bgm_gain=0.45, voices=voices, duck=0.35)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%05d.jpg"), "-i", wav, "-c:v", "libx264",
                        "-preset", "slow" if hq else "veryfast", "-crf", "14" if hq else "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k" if hq else "192k",
                        "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, round(dur, 1), "秒")


if __name__ == "__main__":
    main()
