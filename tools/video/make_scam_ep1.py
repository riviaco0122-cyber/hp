#!/usr/bin/env python3
"""アキヤド劇場 第1話「その民泊副業、本当に“簡単”？」（約5分・1920×1080）を作る。1話完結・最後にどんでん返し。

- 絵の部品（人物・家・背景・図解）は tools/video/make_explainer.py と共通。セリフは VOICEVOX（tools/video/voicevox_tts.py）。
- 場面の長さはセリフの長さから決める。アニメは「何番目のセリフが始まったか」に合わせて動く。
- 話している人物は口が動き、字幕には話している人の名前を色つきで出す。
- 手口は公的機関が公表している相談例の範囲（動画の中では機関名を出さない）。人物・団体は架空（冒頭と最後に表示）。
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
    # 0 冒頭：契約してしまう瞬間＋「最後に秘密が…」の予告
    ("night", 3.4, [
        ("N", "会社員のユウタ。ある夜、パソコンの前で…。", {}),
        ("U", "では、こちらのボタンを押して…はい、ご契約、おめでとうございま〜す！", dict(sfx=[(0.3, "bling")])),
        ("Y", "やった！ これで僕も、民泊でお金持ちだ…！", {}),
        ("N", "このあとユウタは、とんでもないことになる。", dict(sfx=[(0.2, "boing")])),
        ("N", "そしてこの話には、最後に、もうひとつ驚きの秘密が隠されている…。", dict(sfx=[(0.3, "chime")])),
        ("N", "時間を少し、戻してみよう。", dict(sfx=[(0.6, "rewind")])),
    ]),
    # 1 SNS 広告 → メッセージアプリ
    ("night", 0.9, [
        ("N", "1週間前。", dict(say="一週間前。")),
        ("Y", "はぁ…給料、上がらないなぁ。", {}),
        ("Y", "ん？ 「スマホだけで、民泊で月30万円」…？", dict(say="ん？ スマホだけで、民泊で月三十万円…？", sfx=[(0, "alert")])),
        ("Y", "物件がなくてもいいのか！ 無料なら、登録してみよう。", dict(sfx=[(2.6, "click")])),
        ("N", "メッセージアプリに登録すると、次々にメッセージが届いた。", dict(sfx=[(0.4, "alert"), (1.6, "alert"), (2.8, "alert")])),
        ("Y", "個別相談も無料！？ でも、その前に…。", {}),
    ]),
    # 2 お試しマニュアル
    ("night", 0.9, [
        ("N", "まずは、おすすめされた「民泊スタートマニュアル」を、2,980円で買ってみた。", dict(say="まずは、おすすめされた、民泊スタートマニュアルを、二千九百八十円で買ってみた。", sfx=[(3.0, "coin")])),
        ("Y", "どれどれ…。「まずは、物件を探しましょう」…。えっ、それだけ！？", dict(sfx=[(3.4, "boing")])),
        ("N", "中身は、ネットで調べれば分かることばかり。", {}),
        ("Y", "うーん…。でも、「続きは個別相談で」って書いてある。申し込んでみよう！", dict(sfx=[(0.3, "alert")])),
    ]),
    # 3 オンライン個別相談（生徒さんの顔＝伏線）
    ("night", 1.0, [
        ("N", "そして、オンラインの個別相談の日。", dict(sfx=[(0.2, "alert")])),
        ("U", "こんばんは〜、ウマイです！ 民泊はね、物件がなくても、スマホひとつで始められるんですよ〜！", dict(sfx=[(0, "bling")])),
        ("Y", "本当ですか！？", {}),
        ("U", "ほら、うちの生徒さんたち。Aさん、Bさん、Cさん。みんな、月30万円、稼いでます！", dict(say="ほら、うちの生徒さんたち。エーさん、ビーさん、シーさん。みんな、月三十万円、稼いでます！", sfx=[(1.2, "pop"), (1.9, "pop"), (2.6, "pop")])),
        ("Y", "すごい…！", dict(say="すっごーい！")),
        ("U", "ただし、ノウハウを全部教えるサポートは、80万円。", dict(say="ただし、ノウハウを全部教えるサポートは、八十万円。", sfx=[(2.2, "boing")])),
        ("Y", "は、80万円！？ そんなお金、ないです…。", dict(say="は、八十万円！？ そんなお金、ないです…。")),
        ("U", "大丈夫！ カードローンで借りれば、すぐに返せますから。申し込みも、画面を共有してくれれば、私が手伝いますよ。", {}),
        ("U", "それに、今日決めてくれたら、特典つき！ 今日だけですよ〜。", dict(sfx=[(1.6, "bling")])),
        ("Y", "きょ、今日だけ…！", {}),
    ]),
    # 4 選択肢
    ("mint", 0.6, [
        ("N", "さて、あなたがユウタなら、どうする？", dict(sfx=[(0, "chime")])),
        ("N", "A、その場で契約する。B、「考えます」と言って、いったん切る。", dict(say="エー、その場で契約する。ビー、考えますと言って、いったん切る。", sfx=[(0.1, "pop"), (2.6, "pop")])),
        ("N", "まずは、Aを選んだ場合を見てみよう…。", dict(pre=3.2, say="まずは、エーを選んだ場合を見てみよう。", sfx=[(-3.2, "tick"), (-2.2, "tick"), (-1.2, "tick"), (0, "click")])),
    ]),
    # 5 A のバッドエンド
    ("dusk", 1.4, [
        ("N", "言われるまま画面を共有して、カードローンを申し込んだユウタ。", {}),
        ("N", "ところが、届いたサポートは、どこかで見たような動画だけ。", {}),
        ("Y", "あれ？ 質問しても、返事が来ない…。", dict(sfx=[(0.2, "alert")])),
        ("Y", "解約したいんですけど…！ もしもし！？ もしもーし！？", {}),
        ("N", "毎月の返済に追われ、家族にも言えない日々…。", {}),
        ("N", "残ったのは、借金だけ。", dict(sfx=[(0.4, "boing")])),
    ]),
    # 6 時間を戻して B
    ("night", 0.9, [
        ("N", "時間を戻して…。もし、Bを選んでいたら？", dict(say="時間を戻して…。もし、ビーを選んでいたら？", sfx=[(0, "rewind")])),
        ("Y", "ちょっと、考えます！ 失礼します！", dict(sfx=[(2.2, "click")])),
        ("U", "えっ、今日だけですよ！？ ちょ、ちょっと〜！", {}),
        ("Y", "ふぅ…。宿をやってる友達の、ミナさんに聞いてみよう。", dict(sfx=[(2.6, "alert")])),
        ("M", "ユウタさん、それ、あやしいですよ！ 一緒に、ウマイ先生の話を確かめてみましょう。", dict(sfx=[(0, "pop")])),
    ]),
    # 7 確かめてみる
    ("peach", 0.9, [
        ("M", "まず、「物件がなくてもOK」。家を借りて民泊を始めること自体は、できます。私たちも、借りた家で宿を始めました。", dict(say="まず、物件がなくてもオーケー。家を借りて民泊を始めること自体は、できます。私たちも、借りた家で宿を始めました。", sfx=[(0.4, "pop")])),
        ("M", "でも、大家さんの許可、役所への届け出、家具の準備…。私たちは、準備に約7か月かかりました。", dict(say="でも、大家さんの許可、役所への届け出、家具の準備…。私たちは、準備に約七か月かかりました。", sfx=[(0.6, "pop"), (1.8, "pop"), (3.0, "pop")])),
        ("Y", "7か月！？ スマホだけで、すぐ…じゃないんだ。", dict(say="ななかげつ！？ スマホだけで、すぐ…じゃないんだ。", sfx=[(0, "boing")])),
        ("M", "それに、ウマイ先生が本当に稼いでいるのは、民泊じゃなくて、みんなが払う「サポート代」かもしれません。", dict(sfx=[(1.0, "rise"), (3.0, "coin")])),
        ("Y", "そんな…。でも、生徒さんたちは、本当に稼いでるんですよね？", {}),
        ("M", "ふふ。じゃあ、最後の秘密を見せましょう。", dict(sfx=[(0.3, "chime")])),
    ]),
    # 8 どんでん返し：生徒さんは全員…
    ("hall", 1.4, [
        ("M", "生徒のAさん、Bさん、Cさん。よーく見てください。何か、気づきませんか？", dict(say="生徒のエーさん、ビーさん、シーさん。よーく見てください。何か、気づきませんか？")),
        ("M", "ヒントは、首元と、ほっぺた。", dict(pre=3.2, sfx=[(-3.2, "tick"), (-2.2, "tick"), (-1.2, "tick"), (0.2, "ding")])),
        ("Y", "あれ…？ 3人とも、同じ金のネックレスに、同じほくろ…？", dict(say="あれ…？ さんにんとも、同じ金のネックレスに、同じほくろ…？")),
        ("M", "そう。実は…。", dict(sfx=[(0.6, "whoosh")])),
        ("N", "生徒さんは、全員、カツラをかぶったウマイ先生だったのだ！", dict(pre=0.2, sfx=[(0, "boing"), (0.3, "bling")])),
        ("U", "バ、バレちゃった〜！", {}),
        ("Y", "ぜ、全員…！？", {}),
    ]),
    # 9 あやしい言葉、いくつ見つけた？
    ("mint", 0.9, [
        ("M", "ここで、ふりかえり。ウマイ先生のあやしい言葉、いくつ見つけられましたか？", dict(sfx=[(0, "chime")])),
        ("M", "1つめ、「スマホだけで月30万円」。", dict(say="ひとつめ、スマホだけで月三十万円。", sfx=[(0, "pop")])),
        ("M", "2つめ、「物件がなくてもOK」。", dict(say="ふたつめ、物件がなくてもオーケー。", sfx=[(0, "pop")])),
        ("M", "3つめ、「みんな稼いでます」という、成功者の声。", dict(say="みっつめ、みんな稼いでます、という、成功者の声。", sfx=[(0, "pop")])),
        ("M", "4つめ、「借りれば、すぐに返せます」。", dict(say="よっつめ、借りれば、すぐに返せます。", sfx=[(0, "pop")])),
        ("M", "5つめ、「今日だけですよ」。", dict(say="いつつめ、今日だけですよ。", sfx=[(0, "pop")])),
        ("Y", "5つも…！ ぜんぜん気づかなかった…。", dict(say="いつつも…！ ぜんぜん気づかなかった…。", sfx=[(0, "boing")])),
    ]),
    # 10 覚えておきたいこと
    ("sky", 0.9, [
        ("M", "こんな話に出会ったら、思い出してください。", {}),
        ("M", "1つめ。「誰でも・簡単に・すぐ」稼げる話は、まず疑う。", dict(say="ひとつめ。誰でも、簡単に、すぐ稼げる話は、まず疑う。", sfx=[(0, "pop")])),
        ("M", "2つめ。お金を借りさせる話は、そこでストップ。画面を共有して、人にスマホやパソコンを操作させないこと。", dict(say="ふたつめ。お金を借りさせる話は、そこでストップ。画面を共有して、人にスマホやパソコンを操作させないこと。", sfx=[(0, "pop")])),
        ("M", "3つめ。その場で決めない。家族や友達に、ひとこと相談してから。", dict(say="みっつめ。その場で決めない。家族や友達に、ひとこと相談してから。", sfx=[(0, "pop")])),
    ]),
    # 11 エンディング
    ("yellow", 4.2, [
        ("Y", "危なかった…。ミナさん、ありがとう！", {}),
        ("M", "民泊は、時間も手間もかかるけど、そのぶん、旅行者にも地域にも喜ばれる、すてきな仕事です。正しく始めましょうね。", {}),
        ("U", "くっ…覚えてなさ〜い！", dict(sfx=[(0, "whoosh")])),
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
        while cut + 1 < len(s) and s[cut + 1] in "」』）！？…。、":
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
function hall(t,noBanner){ // セミナー会場
  let s=`<rect width="1920" height="1080" fill="#3a2a4f"/><rect y="760" width="1920" height="320" fill="#2a1e3a"/>`;
  s+=`<path d="M760 0 L560 860 L1500 860 L1300 0Z" fill="#fff6c9" opacity="${.12+.04*Math.sin(t*3)}"/>`;
  s+=`<rect x="420" y="700" width="1380" height="70" rx="10" fill="#6b4a8a"/><rect x="420" y="690" width="1380" height="18" rx="8" fill="#8a66ad"/>`;
  s+=`<path d="M0 0 H300 Q260 400 300 860 H0Z" fill="#a23b3b"/><path d="M1920 0 H1620 Q1660 400 1620 860 H1920Z" fill="#a23b3b"/><path d="M60 0 v860 M140 0 v860 M220 0 v860 M1700 0 v860 M1780 0 v860 M1860 0 v860" stroke="#8a2f2f" stroke-width="10"/>`;
  if(!noBanner)s+=`<rect x="560" y="120" width="1000" height="96" rx="14" fill="#e8b950"/><text x="1060" y="186" text-anchor="middle" font-size="56" font-weight="900" fill="#3a2a4f">民泊で稼ぐ！特別セミナー</text>`;
  for(let k=0;k<7;k++){const x=520+k*190;s+=`<circle cx="${x}" cy="${120+Math.sin(t*4+k)*6}" r="10" fill="#fff6c9" opacity="${.5+.5*Math.sin(t*6+k)}"/>`}
  return s;
}
function roomNight(t){ // 夜の部屋
  let s=bg(t,'night');
  for(let k=0;k<40;k++){const x=rnd(k)*1920,y=rnd(k+50)*380;s+=`<circle cx="${x}" cy="${y}" r="${1.5+rnd(k+90)*2.5}" fill="#fff" opacity="${.4+.5*Math.abs(Math.sin(t*2+k))}"/>`}
  return s;
}
function laptop(x,y,s,inner){return `<g transform="translate(${x},${y}) scale(${s})"><rect x="-470" y="-300" width="940" height="600" rx="26" fill="#22252b"/><rect x="-446" y="-276" width="892" height="552" rx="10" fill="#e9eef5"/>${inner}<path d="M-560 300 h1120 l-50 40 h-1020z" fill="#c9d1d9"/></g>`}
function callUI(t,umaiTalk,umaiMood,yuMood,extra=''){ // オンライン相談の画面
  return `<rect x="-446" y="-276" width="892" height="52" fill="#2f3b4a"/><circle cx="-410" cy="-250" r="9" fill="#e53935"/><text x="-390" y="-240" font-size="26" font-weight="700" fill="#fff">オンライン個別相談（無料）</text>
  <rect x="-430" y="-210" width="600" height="420" rx="12" fill="#c8b6dc"/>${face('cu',-130,-10,170,'umai','#7a4a9a',umaiMood,t,umaiTalk)}
  <rect x="190" y="70" width="240" height="140" rx="10" fill="#cfe3d6"/>${face('cy',310,140,58,'owner',G,yuMood,t)}${extra}`;
}
function chatBubble(x,y,txt,p){return fade(p,`<circle cx="${x-130}" cy="${y}" r="22" fill="#7a4a9a"/><text x="${x-130}" y="${y+9}" text-anchor="middle" font-size="24" font-weight="900" fill="#fff">ウ</text><rect x="${x-100}" y="${y-30}" width="${txt.length*24+36}" height="60" rx="20" fill="#fff" stroke="#d6dbe2" stroke-width="2"/><text x="${x-82}" y="${y+9}" font-size="24" font-weight="700" fill="${DG}">${txt}</text>`,10)}
function stamp(x,y,txt,p,c='#e53935',fs=96,rot=-10){return pop(x,y,p,`<g transform="rotate(${rot} ${x} ${y})"><rect x="${x-txt.length*fs*.5-40}" y="${y-fs*.8}" width="${txt.length*fs+80}" height="${fs*1.5}" rx="16" fill="none" stroke="${c}" stroke-width="12"/><text x="${x}" y="${y+fs*.35}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${c}">${txt}</text></g>`)}
function rewindFX(p){if(p<=0||p>=1)return '';const a=Math.sin(p*Math.PI);let s=`<rect width="1920" height="1080" fill="#0b1020" opacity="${.45*a}"/>`;
  for(let k=0;k<14;k++){const y=((k*83+p*2600)%1080);s+=`<rect x="0" y="${y}" width="1920" height="${6+k%3*4}" fill="#fff" opacity="${.18*a}"/>`}
  return s+`<g opacity="${a}"><path d="M860 470 l-80 50 l80 50z M960 470 l-80 50 l80 50z" fill="#fff"/><text x="1000" y="540" font-size="60" font-weight="900" fill="#fff">巻き戻し</text></g>`;}
function scene(i,t,lt){
  const L=SL[i],E=SE[i],at=(k,d=.5,o=0)=>seg(lt,L[k]+o,L[k]+o+d),on=k=>lt>=L[k],win=(k,j)=>clamp(seg(lt,L[k],L[k]+.4))*(j==null?1:1-seg(lt,L[j]-.1,L[j]+.3));
  let s='';
  if(i===0){
    s+=`<rect x="760" y="${GROUND-40}" width="840" height="40" rx="8" fill="#6a5646"/>`;
    const bad=at(3,.3);
    s+=laptop(1180,520,.8,callUI(t,talking('U',t),'happy','happy',`<rect x="-150" y="230" width="300" height="0"/>`)+`<g opacity="${1-bad}"><rect x="-120" y="150" width="240" height="70" rx="35" fill="${T}"/><text x="0" y="198" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">契約する</text></g>`+(bad>0?`<g opacity="${bad}"><rect x="-446" y="-276" width="892" height="552" fill="#b71c1c" opacity=".55"/><path d="M-200 -276 L-120 -60 L-220 60 L-80 276 M120 -276 L60 -100 L180 40 L90 276" stroke="#fff" stroke-width="8" fill="none"/></g>`:''));
    if(on(1)&&!on(2)){const fp=at(1,1.2,1.2);s+=`<path transform="translate(${1500-260*fp},${830-150*fp})" d="M0 0 L0 46 L12 34 L22 56 L32 51 L22 30 L38 30z" fill="#fff" stroke="${DG}" stroke-width="4" stroke-linejoin="round"/>`}
    s+=P(430,GROUND,.92,{c:'owner',who:'Y',pose:on(2)&&!on(3)?'cheer':(on(3)?'think':'stand'),mood:on(3)?'worry':'happy'},t);
    s+=pop(960,200,win(4,5),`<rect x="560" y="140" width="800" height="110" rx="55" fill="#1f1530" opacity=".85"/><text x="960" y="212" text-anchor="middle" font-size="48" font-weight="900" fill="${Y}">最後に、驚きの秘密が…？</text>`);
    s+=rewindFX(seg(lt,L[5]+.5,E[5]+.4));
    const tp=seg(lt,E[5]+.4,E[5]+1.1);
    s+=pop(960,470,tp,`<rect width="1920" height="1080" fill="#000" opacity=".4"/><rect x="290" y="300" width="1340" height="330" rx="40" fill="#fff"/><rect x="760" y="262" width="400" height="76" rx="38" fill="${G}"/><text x="960" y="314" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">アキヤド劇場</text><text x="960" y="470" text-anchor="middle" font-size="92" font-weight="900" fill="${DG}">その民泊副業、</text><text x="960" y="590" text-anchor="middle" font-size="92" font-weight="900" fill="${T}">本当に「簡単」？</text>`);
    s+=fade(seg(lt,.2,.6)*(1-seg(lt,5,5.5)),`<rect x="40" y="40" width="760" height="56" rx="28" fill="#000" opacity=".4"/><text x="70" y="78" font-size="26" font-weight="700" fill="#fff">※ この物語はフィクションです。人物・団体は架空です</text>`,0);
  }
  if(i===1){
    s+=pop(960,300,win(0,1),`<rect x="760" y="240" width="400" height="110" rx="55" fill="#fff"/><text x="960" y="318" text-anchor="middle" font-size="60" font-weight="900" fill="${DG}">1週間前</text>`);
    s+=P(420,GROUND,.92,{c:'owner',who:'Y',pose:on(1)?'phone':'stand',mood:on(5)||(on(3)&&!on(4))?'happy':'smile'},t);
    const chat=on(4);
    let ui;
    if(!chat){ui=`<rect x="-172" y="-300" width="344" height="60" fill="#fff"/><text x="0" y="-260" text-anchor="middle" font-size="26" font-weight="900" fill="#2c3a33">SNS</text>${[0,1].map(k=>`<rect x="-150" y="${-220+k*90}" width="300" height="70" rx="10" fill="#eef1f4"/>`).join('')}`+
      (on(2)?`<g opacity="${at(2,.4)}"><rect x="-160" y="-50" width="320" height="330" rx="16" fill="#fff4d6" stroke="${Y}" stroke-width="4"/><text x="-140" y="-18" font-size="18" font-weight="700" fill="#999">広告</text><text x="0" y="40" text-anchor="middle" font-size="34" font-weight="900" fill="${T}">スマホだけ！</text><text x="0" y="90" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">民泊で月30万円</text><text x="0" y="140" text-anchor="middle" font-size="26" font-weight="900" fill="#6b3fa0">物件がなくてもOK</text><rect x="-120" y="180" width="240" height="64" rx="32" fill="${G}" stroke="#fff" stroke-width="${on(3)&&lt>L[3]+2.4?8:0}"/><text x="0" y="222" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">無料で登録</text></g>`:'');}
    else{ui=`<rect x="-172" y="-300" width="344" height="610" fill="#dfe8ef"/><rect x="-172" y="-300" width="344" height="60" fill="#7a4a9a"/><text x="0" y="-260" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">ウマイ先生（公式）</text>`+
      [['ご登録ありがとうございます！',.4],['無料動画をプレゼント！',1.6],['今なら個別相談も無料！',2.8]].map(([m2,o],k)=>chatBubble(-10,-180+k*110,m2,at(4,.3,o))).join('').replace(/font-size="24"/g,'font-size="21"');}
    s+=phoneUI(1180,500,1.0,ui,1);
  }
  if(i===2){ // お試しマニュアル
    s+=P(400,GROUND,.92,{c:'owner',who:'Y',pose:'phone',mood:on(1)&&lt>L[1]+3.2?'worry':(on(3)?'smile':'happy')},t);
    s+=pop(1180,470,at(0,.5),`${box(900,200,560,600,20)}<rect x="900" y="200" width="560" height="130" rx="20" fill="${T}"/><text x="1180" y="262" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">民泊スタート</text><text x="1180" y="310" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">マニュアル</text>`+(on(1)?`<text x="1180" y="440" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">第1章</text><text x="1180" y="520" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">まずは、物件を</text><text x="1180" y="580" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">探しましょう。</text>`:`<text x="1180" y="560" text-anchor="middle" font-size="72" font-weight="900" fill="${T}">2,980円</text>`)+(on(1)?`<text x="1180" y="720" text-anchor="middle" font-size="28" font-weight="700" fill="#999">（以上）</text>`:''));
    s+=stamp(1180,640,'うすっ！',at(1,.4,3.4),'#6b3fa0',70,-12);
    if(on(3))s+=pop(1180,820,at(3,.4,.4),`<rect x="900" y="770" width="560" height="90" rx="45" fill="#7a4a9a"/><text x="1180" y="828" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">続きは個別相談で！</text>`);
  }
  if(i===9){ // あやしい言葉、いくつ見つけた？
    s+=P(190,GROUND,.84,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    if(on(6))s+=pop(1760,200,at(6,.4),face('yf2',1760,200,80,'owner',G,'worry',t,talking('Y',t)));
    s+=fade(at(0,.5),`<text x="1060" y="230" text-anchor="middle" font-size="50" font-weight="900" fill="${DG}">ウマイ先生のあやしい言葉、いくつ見つけた？</text>`,0);
    const W=['スマホだけで月30万円','物件がなくてもOK','みんな稼いでます','借りれば、すぐに返せます','今日だけですよ'];
    W.forEach((w,k)=>{const x=k<3?660+k*505:912+(k-3)*505,y=k<3?400:590;s+=pop(x,y,at(1+k,.4),`${box(x-245,y-70,490,140,26)}<circle cx="${x-200}" cy="${y}" r="34" fill="#e53935"/><text x="${x-200}" y="${y+13}" text-anchor="middle" font-size="36" font-weight="900" fill="#fff">${k+1}</text><text x="${x-150}" y="${y+11}" font-size="${w.length>10?28:33}" font-weight="900" fill="${DG}">「${w}」</text>`)});
    let n=0;for(let k=1;k<=5;k++)if(on(k))n=k;
    if(n)s+=pop(1060,800,at(6,.4),`<rect x="840" y="745" width="440" height="110" rx="55" fill="#e53935"/><text x="1060" y="820" text-anchor="middle" font-size="60" font-weight="900" fill="#fff">ぜんぶで ${n}つ！</text>`);
  }
  if(i===3){
    s+=P(260,GROUND,.86,{c:'owner',who:'Y',pose:on(9)?'shake':(on(6)?'think':'stand'),mood:on(6)?'worry':'happy'},t);
    let extra='';
    if(on(3))extra+=`<g opacity="${win(3,5)}">${['umaiA','umaiB','umaiC'].map((c2,k)=>{const cy=-180+k*92,p=seg(lt,L[3]+1.2+k*.7,L[3]+1.6+k*.7);return p>0?`<g opacity="${p}"><rect x="186" y="${cy-42}" width="244" height="84" rx="12" fill="#fff"/>${face('st'+k,232,cy,36,c2,'#7a4a9a','happy',t)}<text x="278" y="${cy-6}" font-size="20" font-weight="900" fill="${DG}">生徒${'ABC'[k]}さん</text><text x="278" y="${cy+24}" font-size="24" font-weight="900" fill="${T}">月30万円！</text></g>`:''}).join('')}</g>`;
    if(on(5))extra+=pop(310,-120,win(5,7),`<g transform="rotate(4 310 -120)"><rect x="180" y="-200" width="260" height="160" rx="14" fill="#fff" stroke="${T}" stroke-width="6"/><text x="310" y="-150" text-anchor="middle" font-size="26" font-weight="900" fill="${DG}">フルサポート</text><text x="310" y="-80" text-anchor="middle" font-size="56" font-weight="900" fill="${T}">80万円</text></g>`);
    if(on(7))extra+=pop(310,-120,win(7,8),`<rect x="180" y="-210" width="260" height="70" rx="35" fill="#6b3fa0"/><text x="310" y="-164" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">カードローン</text><rect x="180" y="-120" width="260" height="70" rx="35" fill="#2f3b4a"/><text x="310" y="-74" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">画面を共有</text>`);
    if(on(8))extra+=pop(310,-120,at(8,.4,1.4),`<g transform="rotate(-8 310 -120)"><rect x="170" y="-180" width="280" height="110" rx="18" fill="#e53935"/><text x="310" y="-108" text-anchor="middle" font-size="54" font-weight="900" fill="#fff">今日だけ！</text></g>`);
    s+=pop(1180,470,at(0,.5),laptop(1180,470,1.08,callUI(t,talking('U',t),'happy',on(6)?'worry':'happy',extra)));
  }
  if(i===4){
    s+=fade(at(0,.5),`<text x="960" y="230" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">あなたなら、どうする？</text>`,0);
    [['A','その場で契約する',T],['B','「考えます」と言って、いったん切る',G]].forEach(([k2,w,c],k)=>{const x=560+k*800,p=at(1,.5,[0.1,2.6][k]),hit=on(2)&&k===0;
      s+=pop(x,520,p,`<g transform="translate(${x},520) scale(${hit?1.06:1}) translate(${-x},-520)" opacity="${on(2)&&k===1?.35:1}">${box(x-340,380,680,280,30)}<circle cx="${x}" cy="450" r="50" fill="${c}"/><text x="${x}" y="470" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">${k2}</text><text x="${x}" y="590" text-anchor="middle" font-size="${w.length>12?38:46}" font-weight="900" fill="${DG}">${w}</text></g>`)});
    const cd=lt-(L[2]-3.2);if(cd>0&&cd<3.2)s+=pop(960,780,clamp((cd%1)*4),`<circle cx="960" cy="780" r="70" fill="${Y}"/><text x="960" y="810" text-anchor="middle" font-size="84" font-weight="900" fill="${DG}">${Math.max(1,3-Math.floor(cd))}</text>`);
  }
  if(i===5){
    s+=P(330,GROUND,.9,{c:'owner',who:'Y',pose:on(3)?'phone':'think',mood:'worry'},t);
    s+=fade(at(0,.4),`<rect x="40" y="40" width="380" height="64" rx="32" fill="#e53935"/><text x="230" y="84" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">Aを選んだ場合…</text>`,0);
    if(on(0)&&!on(1))s+=phoneUI(1150,480,.95,`<rect x="-172" y="-300" width="344" height="610" fill="#fff"/><text x="0" y="-220" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">カードローン</text><text x="0" y="-120" text-anchor="middle" font-size="26" font-weight="700" fill="#4a5a52">画面共有中…</text><rect x="-130" y="-40" width="260" height="80" rx="14" fill="#e3f1e8"/><text x="0" y="12" text-anchor="middle" font-size="30" font-weight="900" fill="${G}">お借り入れ完了</text><circle cx="120" cy="-250" r="14" fill="#e53935" opacity="${.5+.5*Math.sin(lt*6)}"/>`,at(0,.4));
    if(on(1)&&!on(2))s+=pop(1150,470,at(1,.4),laptop(1150,470,.8,`<rect x="-446" y="-276" width="892" height="552" fill="#111"/><circle r="70" fill="#fff" opacity=".85"/><path d="M-22 -36 L40 0 L-22 36z" fill="#111"/><text x="0" y="200" text-anchor="middle" font-size="34" font-weight="900" fill="#ccc">サポート動画 #1（どこかで見たような…）</text>`));
    if(on(2)&&!on(3))s+=phoneUI(1150,480,.95,`<rect x="-172" y="-300" width="344" height="610" fill="#dfe8ef"/><rect x="-172" y="-300" width="344" height="60" fill="#7a4a9a"/><text x="0" y="-260" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">ウマイ先生（公式）</text>${[0,1,2].map(k=>`<rect x="-10" y="${-200+k*100}" width="170" height="60" rx="20" fill="#9fe3a6"/><text x="75" y="${-162+k*100}" text-anchor="middle" font-size="22" font-weight="900" fill="${DG}">質問です…</text>`).join('')}<text x="0" y="200" text-anchor="middle" font-size="26" font-weight="900" fill="#e53935">返事がない…</text>`,at(2,.4));
    if(on(4)&&!on(5))s+=pop(1150,450,at(4,.4),`${box(880,250,540,420,20)}<text x="1150" y="320" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">カレンダー</text>${[0,1,2,3,4,5].map(k=>`<rect x="${910+(k%3)*160}" y="${360+Math.floor(k/3)*140}" width="140" height="120" rx="10" fill="#fdecea"/><text x="${980+(k%3)*160}" y="${432+Math.floor(k/3)*140}" text-anchor="middle" font-size="30" font-weight="900" fill="#e53935">返済日</text>`).join('')}`);
    if(on(3)&&!on(4))s+=phoneUI(1150,480,.95,`<rect x="-172" y="-300" width="344" height="610" fill="#2f3b4a"/><text x="0" y="-160" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">ウマイ先生</text><text x="0" y="-100" text-anchor="middle" font-size="26" font-weight="700" fill="#ffcdd2">つながりません</text><circle cx="0" cy="180" r="56" fill="#e53935"/>`,at(3,.4));
    if(on(5)){s+=pop(1150,450,at(5,.5),`${box(880,250,540,400,20)}<text x="1150" y="320" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">ご返済のお知らせ</text><path d="M920 360 h460 M920 420 h460 M920 480 h300" stroke="#cfd8dc" stroke-width="10"/><text x="1150" y="600" text-anchor="middle" font-size="44" font-weight="900" fill="#e53935">借金だけが残った</text>`);
      s+=stamp(1150,800,'BAD END',at(5,.4,.6),'#e53935',100,-8);}
  }
  if(i===6){
    s+=P(330,GROUND,.92,{c:'owner',who:'Y',pose:on(3)?'phone':'stand',mood:on(3)?'smile':'worry'},t);
    const ended=lt>L[1]+2.2;
    if(!on(3)){s+=laptop(1180,470,1.0,ended&&lt>E[2]?`<rect x="-446" y="-276" width="892" height="552" fill="#2f3b4a"/><text x="0" y="10" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">通話を終了しました</text>`:callUI(t,talking('U',t),on(2)?'worry':'happy','smile',ended?`<rect x="-446" y="-276" width="892" height="552" fill="#000" opacity=".25"/>`:''));
      if(on(1)&&!ended){const fp=at(1,1.6,.4);s+=`<path transform="translate(${1560-120*fp},${900-120*fp})" d="M0 0 L0 46 L12 34 L22 56 L32 51 L22 30 L38 30z" fill="#fff" stroke="${DG}" stroke-width="4" stroke-linejoin="round"/>`;}}
    else s+=phoneUI(1080,480,.9,`<rect x="-172" y="-300" width="344" height="610" fill="#fdf6ec"/><text x="0" y="-150" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">ミナさん</text><text x="0" y="-100" text-anchor="middle" font-size="24" font-weight="700" fill="#4a5a52">（宿を運営している友達）</text>${face('mp',0,40,90,'staff',T,'smile',t)}`,at(3,.4)*(1-at(4,.4)));
    if(on(4))s+=P(1500+400*(1-eo(at(4,.5))),GROUND,.9,{c:'staff',who:'M',pose:'present',mood:'happy',flip:true},t);
    s+=rewindFX(seg(lt,0,1.2));
  }
  if(i===7){ // 確かめてみる
    s+=P(240,GROUND,.84,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    s+=pop(1180,170,at(0,.5),`<rect x="900" y="120" width="560" height="96" rx="48" fill="#6b3fa0"/><text x="1180" y="186" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">本当か、確かめてみよう</text>`);
    if(!on(1))s+=fade(at(0,.4),`${house(1180,840,.75,1)}<rect x="1400" y="430" width="10" height="410" fill="#6a5646"/><rect x="1340" y="430" width="240" height="96" rx="12" fill="#fff"/><text x="1460" y="492" text-anchor="middle" font-size="40" font-weight="900" fill="${G}">借りた家</text>${stamp(830,420,'OK',at(0,.4,3.2),G,80,-6)}`,0);
    if(on(1)&&!on(2)){s+=[['大家さんの許可','key'],['役所への届け出','doc'],['家具の準備','home']].map(([w,ic],k)=>{const x=720+k*430;return pop(x,480,at(1,.4,[0.6,1.8,3.0][k]),`${box(x-190,340,380,280,24)}${icon(x,430,56,ic,G,'#fff',.8)}<text x="${x}" y="560" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">${w}</text>`)}).join('');
      s+=pop(1150,760,at(1,.5,4.2),`<rect x="890" y="710" width="520" height="100" rx="50" fill="${T}"/><text x="1150" y="778" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">準備に約7か月</text>`);}
    if(on(2)&&!on(3))s+=pop(1150,480,at(2,.4),`${box(720,330,860,300,30)}<text x="1150" y="510" text-anchor="middle" font-size="72" font-weight="900" fill="${DG}">「スマホだけで、すぐ」</text><path d="M760 360 L1540 600 M1540 360 L760 600" stroke="#e53935" stroke-width="20" stroke-linecap="round" opacity="${at(2,.3,.6)}"/>`)+pop(1760,200,at(2,.4),face('yf7',1760,200,80,'owner',G,'worry',t,talking('Y',t)));
    if(on(3)&&!on(5)){const g=eo(at(3,1.6,1));s+=fade(at(3,.4),`${box(640,290,1080,520,30)}<text x="1180" y="360" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">ウマイ先生のお金の出どころ（イメージ）</text><path d="M760 740 H1600" stroke="#9fb5a8" stroke-width="6"/>
      <rect x="840" y="${740-60*g}" width="200" height="${60*g}" rx="8" fill="#9fb5a8"/><text x="940" y="790" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">民泊</text>
      <rect x="1300" y="${740-330*g}" width="200" height="${330*g}" rx="8" fill="${T}"/><text x="1400" y="790" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">サポート代</text>${g>.95?coin(1560,430,40):''}`,0);
      if(on(4))s+=pop(1760,200,at(4,.4),face('yf8',1760,200,80,'owner',G,'worry',t,talking('Y',t)));}
    if(on(5))s+=pop(1180,500,at(5,.5),`<rect x="760" y="420" width="840" height="160" rx="80" fill="#1f1530"/><text x="1180" y="525" text-anchor="middle" font-size="64" font-weight="900" fill="${Y}">最後の秘密…</text>`);
  }
  if(i===8){ // どんでん返し：生徒さんは全員…
    s+=hall(lt,true)+`<rect width="1920" height="1080" fill="#000" opacity="${.25*at(3,.4)}"/>`;
    s+=P(150,GROUND+40,.72,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    const rev=at(4,.5,-.1),X=[600,1010,1420],Rr=150,Y0=430;
    X.forEach((x,k)=>{const c2=['umaiA','umaiB','umaiC'][k],p=at(0,.4,.6+k*.4);
      let g=`<g opacity="${1-rev}">${face('tw'+k,x,Y0,Rr,c2,'#7a4a9a','happy',t)}</g>`;
      if(rev>0)g+=`<g opacity="${rev}">${face('tu'+k,x,Y0,Rr,'umai','#7a4a9a',on(5)?'happy':'worry',t,talking('U',t))}</g>`;
      if(rev>0&&rev<1){const hc=['#8a5a3c','#2b2422','#6d6d6d'][k];g+=`<g transform="translate(${x+(k-1)*120*rev},${Y0-130-420*rev}) rotate(${(k-1)*160*rev+40*rev})" opacity="${1-rev}"><ellipse rx="110" ry="60" fill="${hc}"/></g>`}
      g+=`<rect x="${x-130}" y="${Y0+Rr+20}" width="260" height="${rev>0?70:110}" rx="20" fill="#fff"/>`+(rev>0?`<text x="${x}" y="${Y0+Rr+68}" text-anchor="middle" font-size="36" font-weight="900" fill="#6b3fa0">ウマイ先生</text>`:`<text x="${x}" y="${Y0+Rr+62}" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">生徒${'ABC'[k]}さん</text><text x="${x}" y="${Y0+Rr+104}" text-anchor="middle" font-size="30" font-weight="900" fill="${T}">月30万円！</text>`);
      if(on(1)&&!on(4)){const pu=.6+.4*Math.abs(Math.sin(lt*5));g+=`<circle cx="${x}" cy="${Y0+Rr*.86}" r="${Rr*.3}" fill="none" stroke="${Y}" stroke-width="8" opacity="${pu*at(1,.3,.2)}"/><circle cx="${x+Rr*.27}" cy="${Y0+Rr*.1}" r="${Rr*.14}" fill="none" stroke="${Y}" stroke-width="7" opacity="${pu*at(1,.3,.5)}"/>`}
      s+=pop(x,Y0,p,g);});
    const cd=lt-(L[1]-3.2);if(cd>0&&cd<3.2)s+=pop(1010,170,clamp((cd%1)*4),`<circle cx="1010" cy="170" r="66" fill="${Y}"/><text x="1010" y="198" text-anchor="middle" font-size="80" font-weight="900" fill="${DG}">${Math.max(1,3-Math.floor(cd))}</text>`);
    if(!on(1))s+=fade(at(0,.4),`<text x="1010" y="200" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">何か、気づきませんか？</text>`,0);
    if(on(4))s+=pop(1010,180,at(4,.4,.3),`<g transform="rotate(-4 1010 180)"><rect x="560" y="110" width="900" height="130" rx="30" fill="#e53935"/><text x="1010" y="200" text-anchor="middle" font-size="72" font-weight="900" fill="#fff">全員、ウマイ先生！</text></g>`);
    if(on(2)&&!on(4))s+=pop(1780,180,at(2,.4),face('yt',1780,180,80,'owner',G,'worry',t,talking('Y',t)));
    if(on(6))s+=pop(1780,180,at(6,.3),face('yt2',1780,180,80,'owner',G,'worry',t,talking('Y',t)));
  }
  if(i===10){
    s+=P(240,GROUND,.84,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    s+=fade(at(0),`<text x="1180" y="250" text-anchor="middle" font-size="50" font-weight="900" fill="${DG}">こんな話に出会ったら</text>`,0);
    s+=checkRow(520,380,1340,'1','「誰でも・簡単に・すぐ」は、まず疑う','',at(1),T);
    s+=checkRow(520,540,1340,'2','お金を借りさせる話は、ストップ','画面を共有して、人に操作させない',at(2),T);
    s+=checkRow(520,700,1340,'3','その場で決めない','家族や友達に、ひとこと相談してから',at(3),T);
  }
  if(i===11){
    s+=house(1000,GROUND,.95,1)+sparkle(800,330,1.3,lt,0)+sparkle(1220,300,1.1,lt,2);
    s+=P(400,GROUND,.9,{c:'owner',who:'Y',pose:'cheer',mood:'happy'},t)+P(1560,GROUND,.86,{c:'staff',who:'M',pose:on(3)?'present':'wave',mood:'happy',flip:true},t);
    if(on(2)&&!on(3)){const rx=-200+2400*at(2,2.4);s+=speedLines(rx-500,700,1)+P(rx,GROUND+80,.8,{c:'umai',who:'U',pose:'walk',mood:'worry',disguise:true},t*2);}
    s+=pop(960,420,at(3,.5),`${box(500,250,920,330,36)}${LOGO(760,290,1.2)}<rect x="620" y="400" width="680" height="92" rx="46" fill="${T}"/><text x="960" y="460" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">民泊の始め方・無料相談</text><text x="960" y="545" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">rivia-co.com/media.html</text>`);
    s+=fade(seg(lt,E[3]+.5,E[3]+1.2),`<rect width="1920" height="1080" fill="#1f2a24"/><text x="960" y="400" text-anchor="middle" font-size="60" font-weight="900" fill="#fff">最後まで見てくれて、ありがとう！</text><text x="960" y="510" text-anchor="middle" font-size="34" font-weight="700" fill="#dfe9e3">この物語はフィクションです。登場する人物・団体は架空のものです。</text><text x="960" y="650" text-anchor="middle" font-size="30" font-weight="700" fill="#b8c9bf">${CREDIT}</text><rect x="780" y="715" width="360" height="100" rx="50" fill="#fff"/>${LOGO(810,730,1.1)}`,0);
  }
  return s;
}
window.draw=function(t){
  let i=SC.findIndex(([a,b])=>t>=a&&t<b);if(i<0)i=SC.length-1;
  const a=SC[i][0],TR=.6;
  const B=(j)=>THEME[j]==='night'?roomNight(t):(THEME[j]==='hall'?hall(t,true):bg(t,THEME[j]));
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
