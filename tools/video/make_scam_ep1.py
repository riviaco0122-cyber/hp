#!/usr/bin/env python3
"""アキヤド劇場 第1話「その民泊副業、本当に“簡単”？」（約5分・1920×1080）を作る。1話完結・冒頭で「3人の正体」を問い、最後にどんでん返しともうひとつのオチ。

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
    # 生徒さん（じつはウマイ先生の変装。声は別の人に聞こえるように変えている）
    "A": dict(name="生徒Aさん", style=79, speed=1.05, intonation=1.2, pitch=0.0),    # もち子さん（喜び）
    "B": dict(name="生徒Bさん", style=46, speed=1.05, intonation=1.2, pitch=0.0),    # 小夜/SAYO
    "C": dict(name="生徒Cさん", style=53, speed=1.0, intonation=1.1, pitch=0.0),     # 麒ヶ島宗麟
}
MODELS = [4, 6, 12, 15]
CREDIT = "VOICEVOX:青山龍星　VOICEVOX:玄野武宏　VOICEVOX:No.7　VOICEVOX:剣崎雌雄　VOICEVOX:もち子(cv 明日葉よもぎ)　VOICEVOX:小夜/SAYO　VOICEVOX:麒ヶ島宗麟"

# 場面: (背景のテーマ, 場面の最後に足す秒, セリフの並び)。セリフ: (話す人, 字幕, {say: 読み, pre: 前の間, sfx: [(秒, 種類)]})
SCENES = [
    # 0 冒頭：契約ボタンを押してしまう瞬間＋「3人の正体」の謎かけ
    ("night", 3.4, [
        ("N", "会社員のユウタ。ある夜、パソコンの前で…。", {}),
        ("U", "では、こちらの「契約する」ボタンを、ポチッと！", dict(say="では、こちらの、契約するボタンを、ポチッと！")),
        ("U", "はい、ご契約、おめでとうございま〜す！", dict(pre=0.5, sfx=[(-0.45, "click"), (0.1, "bling")])),
        ("Y", "やった！ これで僕も、民泊でお金持ちだ…！", {}),
        ("N", "このあとユウタは、とんでもないことになる。", dict(sfx=[(0.2, "boing")])),
        ("N", "ところで、月100万円稼いだという、この3人の生徒さん。実は、とんでもない正体がある。", dict(say="ところで、月百万円稼いだという、この三人の生徒さん。実は、とんでもない正体がある。", sfx=[(0.2, "whoosh")])),
        ("N", "ヒントは、ずっと画面の中に。最後まで見て、見抜けるかな？", dict(sfx=[(0.2, "chime")])),
        ("N", "時間を少し、戻してみよう。", dict(sfx=[(0.6, "rewind")])),
    ]),
    # 1 SNS 広告 → メッセージアプリ
    ("night", 0.9, [
        ("N", "1週間前。", dict(say="一週間前。")),
        ("Y", "はぁ…給料、上がらないなぁ。", {}),
        ("Y", "ん？ 「旅しながら、民泊で月100万円」…？", dict(say="ん？ 旅しながら、民泊で月百万円…？", sfx=[(0, "alert")])),
        ("Y", "スマホだけで、物件がなくてもOK！？ 無料なら、登録してみよう。", dict(say="スマホだけで、物件がなくてもオーケー！？ 無料なら、登録してみよう。", sfx=[(3.2, "click")])),
        ("N", "メッセージアプリに登録すると、次々にメッセージが届いた。", dict(sfx=[(0.4, "alert"), (1.6, "alert"), (2.8, "alert"), (4.0, "alert")])),
        ("Y", "個別相談も無料！？ でも、その前に…。", {}),
    ]),
    # 2 ウマイ先生の旅動画 → お試しマニュアル
    ("night", 0.9, [
        ("N", "まずは、ウマイ先生のYouTubeをチェック。", dict(say="まずは、ウマイ先生のユーチューブをチェック。", sfx=[(0.6, "pop"), (1.4, "pop"), (2.2, "pop")])),
        ("Y", "うわぁ…。今日は南の島、昨日は温泉、その前は夜景の街。毎日、旅してる！", {}),
        ("Y", "コメント欄も「月100万円いきました！」ばっかり…。僕も、こうなりたい！", dict(say="コメント欄も、月百万円いきました、ばっかり…。僕も、こうなりたい！")),
        ("N", "そこで、おすすめされた「民泊スタートマニュアル」を、2,980円で買ってみた。", dict(say="そこで、おすすめされた、民泊スタートマニュアルを、二千九百八十円で買ってみた。", sfx=[(3.0, "coin")])),
        ("Y", "どれどれ…。「まずは、物件を探しましょう」…。えっ、それだけ！？", dict(sfx=[(3.4, "boing")])),
        ("N", "中身は、ネットで調べれば分かることばかり。", {}),
        ("Y", "うーん…。でも、「続きは個別相談で」って書いてある。申し込んでみよう！", dict(sfx=[(0.3, "alert")])),
    ]),
    # 3 オンライン個別相談（生徒さんの顔＝伏線）
    ("night", 1.0, [
        ("N", "そして、オンラインの個別相談の日。", dict(sfx=[(0.2, "alert")])),
        ("U", "こんばんは〜、ウマイです！ 今日は、南の島から失礼しま〜す。民泊なら、物件がなくてもOK。スマホだけで、すぐ始められて、いつでも好きなところに行けますよ〜！", dict(say="こんばんは〜、ウマイです！ 今日は、南の島から失礼しま〜す。民泊なら、物件がなくてもオーケー。スマホだけで、すぐ始められて、いつでも好きなところに行けますよ〜！", sfx=[(0, "bling")])),
        ("Y", "本当ですか！？", {}),
        ("U", "うちの生徒さんたちのインタビュー動画、見てください！", dict(sfx=[(0.3, "chime")])),
        ("A", "会社員だったけど、半年で月100万円！ 今は、南の島で暮らしてます♪", dict(say="会社員だったけど、半年で月百万円！ 今は、南の島で暮らしてます。", sfx=[(0, "pop")])),
        ("B", "子育てしながら、スマホだけで月100万円。昨日は、温泉宿にいました〜！", dict(say="子育てしながら、スマホだけで月百万円。昨日は、温泉宿にいました〜！", sfx=[(0, "pop")])),
        ("C", "定年後に始めて、月100万円。今は、海外を旅してます！", dict(say="定年後に始めて、月百万円。今は、海外を旅してます！", sfx=[(0, "pop")])),
        ("Y", "すごい…！ 3人とも、旅しながら月100万円…！", dict(say="すっごーい！ さんにんとも、旅しながら月百万円…！")),
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
    # 7 確かめてみる（ウマイ先生の言葉を、ひとつずつ）
    ("peach", 0.9, [
        ("M", "ウマイ先生の話、本当かどうか、ひとつずつ確かめてみましょう。", dict(sfx=[(0.2, "chime")])),
        ("M", "まず、「物件がなくてもOK」。家を借りて民泊を始めること自体は、できます。私たちも、借りた家で宿を始めました。", dict(say="まず、物件がなくてもオーケー。家を借りて民泊を始めること自体は、できます。私たちも、借りた家で宿を始めました。", sfx=[(0.4, "pop")])),
        ("M", "でも、大家さんの許可、役所への届け出、家具の準備…。私たちは、準備に約7か月かかりました。", dict(say="でも、大家さんの許可、役所への届け出、家具の準備…。私たちは、準備に約七か月かかりました。", sfx=[(0.6, "pop"), (1.8, "pop"), (3.0, "pop")])),
        ("Y", "7か月！？ 「スマホだけで、すぐ」…じゃないんだ。", dict(say="ななかげつ！？ スマホだけで、すぐ…じゃないんだ。", sfx=[(0, "boing")])),
        ("M", "「借りれば、すぐに返せます」も、あやしい。うまくいかなくても、借りたお金は、毎月返さなきゃいけません。", dict(say="借りれば、すぐに返せます、も、あやしい。うまくいかなくても、借りたお金は、毎月返さなきゃいけません。", sfx=[(0.2, "pop"), (1.6, "boing")])),
        ("M", "それに、ウマイ先生が本当に稼いでいるのは、民泊じゃなくて、みんなが払う「サポート代」かもしれません。", dict(sfx=[(1.0, "rise"), (3.0, "coin")])),
        ("Y", "そんな…。でも、生徒さんたちは、本当に稼いでるんですよね？", {}),
        ("M", "ふふ。じゃあ、最後の秘密を見せましょう。", dict(sfx=[(0.3, "chime")])),
    ]),
    # 8 どんでん返し：生徒さんは全員…
    ("hall", 1.4, [
        ("N", "さあ、最初の問題。生徒のAさん、Bさん、Cさん。3人の正体、わかったかな？", dict(say="さあ、最初の問題。生徒のエーさん、ビーさん、シーさん。三人の正体、わかったかな？")),
        ("M", "ヒントは、首元と、ほっぺた。", dict(pre=3.2, sfx=[(-3.2, "tick"), (-2.2, "tick"), (-1.2, "tick"), (0.2, "ding")])),
        ("Y", "あれ…？ 3人とも、同じ貝殻のネックレスに、同じほくろ…？", dict(say="あれ…？ さんにんとも、同じ貝殻のネックレスに、同じほくろ…？")),
        ("M", "そう。実は…。", dict(sfx=[(0.6, "whoosh")])),
        ("N", "生徒さんは全員、ウマイ先生がAIで顔と声を変えて作った、ニセモノだったのだ！", dict(pre=0.2, say="生徒さんは全員、ウマイ先生が、エーアイで顔と声を変えて作った、ニセモノだったのだ！", sfx=[(0, "boing"), (0.3, "bling")])),
        ("U", "バ、バレちゃった〜！ AIって、便利なんだもん〜！", dict(say="バ、バレちゃった〜！ エーアイって、便利なんだもん〜！")),
        ("Y", "ぜ、全員…！？ あのインタビューも、ぜんぶAI…！？", dict(say="ぜ、全員…！？ あのインタビューも、ぜんぶエーアイ…！？")),
        ("M", "顔や声は変えられても、ほくろとネックレスは、消し忘れたみたいですね。", {}),
    ]),
    # 9 エンディング（覚えておきたい3つ → お知らせ → ウマイ先生が逃げる）
    ("yellow", 0.9, [
        ("Y", "危なかった…。ミナさん、ありがとう！", {}),
        ("M", "今は、AIで、成功者の顔も声も作れる時代。うますぎる話は、まず疑う。", dict(say="今は、エーアイで、成功者の顔も声も作れる時代。うますぎる話は、まず疑う。", sfx=[(0.2, "pop")])),
        ("M", "お金を借りさせる話や、画面の共有は、そこでストップ。", dict(sfx=[(0, "pop")])),
        ("M", "そして、その場で決めずに、家族や友達に相談！", dict(sfx=[(0, "pop")])),
        ("M", "民泊は、手間はかかるけど、旅行者にも地域にも喜ばれる、すてきな仕事。正しく始めましょうね！", dict(sfx=[(0.2, "chime")])),
        ("M", "民泊の始め方は、アキヤドの記事でも紹介しています。ご相談も無料ですよ！", dict(sfx=[(0.4, "pop")])),
        ("U", "くっ…覚えてなさ〜い！", dict(sfx=[(0, "whoosh")])),
    ]),
    # 10 最後のオチ：ウマイ先生にも「先生」がいた
    ("night", 4.6, [
        ("N", "その夜…。", {}),
        ("N", "ちなみに、ウマイ先生の「南の島」も、AIで作った背景画像だった。", dict(say="ちなみに、ウマイ先生の南の島も、エーアイで作った背景画像だった。", sfx=[(0.3, "boing")])),
        ("N", "そこへ、1通の広告が…。", dict(say="そこへ、いっつうの広告が…。", sfx=[(0.6, "alert")])),
        ("U", "ん？ 「あなたも先生になって、月1000万円」…？ 今日だけ！？", dict(say="ん？ あなたも先生になって、月一千万円…？ 今日だけ！？")),
        ("U", "申し込みま〜す！", dict(sfx=[(0.1, "click"), (0.4, "bling")])),
        ("N", "ウマイ先生もまた、だれかの「生徒さん」だったのだ…。", dict(pre=0.4, sfx=[(0, "boing")])),
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
CAST.sugoi=Object.assign({},CAST.umai,{hair:'#e8d9a8',top:'#e8b950',top2:'#d09a2f',print:'#fff'});
const VNAME={N:'ナレーション',Y:'ユウタ',M:'ミナ',U:'ウマイ先生',A:'生徒Aさん',B:'生徒Bさん',C:'生徒Cさん'},VCOL={N:'#5d6b64',Y:G,M:T,U:'#6b3fa0',A:'#3d8a6a',B:'#c0782f',C:'#3d6a8a'};
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
function beach(x,y,w,h,t){ // ウマイ先生の「南の島」（じつは背景画像）
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#8fd3f0"/><circle cx="${x+w*.78}" cy="${y+h*.2}" r="${h*.1}" fill="#fff3b0"/><rect x="${x}" y="${y+h*.5}" width="${w}" height="${h*.22}" fill="#3aa6c8"/><path d="M${x} ${y+h*.56} h${w}" stroke="#fff" stroke-width="3" opacity=".5"/><rect x="${x}" y="${y+h*.72}" width="${w}" height="${h*.28}" fill="#f0d8a0"/>
  <path d="M${x+w*.86} ${y+h} Q${x+w*.8} ${y+h*.6} ${x+w*.9} ${y+h*.25}" stroke="#8a5a3c" stroke-width="${w*.03}" fill="none"/>${[-60,-20,20,60,100].map(a=>`<ellipse cx="${x+w*.9}" cy="${y+h*.25}" rx="${w*.1}" ry="${w*.025}" fill="#3f9a5a" transform="rotate(${a} ${x+w*.9} ${y+h*.25}) translate(${w*.08},0)"/>`).join('')}`;
}
function place(k,x,y,w,h,t){ // 旅先の景色 0:南の島 1:温泉 2:夜景の街
  if(k===0)return beach(x,y,w,h,t);
  if(k===1)return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#cfe3f0"/><path d="M${x} ${y+h*.7} L${x+w*.35} ${y+h*.25} L${x+w*.6} ${y+h*.55} L${x+w*.8} ${y+h*.35} L${x+w} ${y+h*.7}z" fill="#8fb39a"/><rect x="${x}" y="${y+h*.7}" width="${w}" height="${h*.3}" fill="#7ab8d6"/>${[0,1,2].map(q=>`<path d="M${x+w*(.3+q*.19)} ${y+h*.68} q${-w*.06} ${-h*.11} 0 ${-h*.22} q${w*.06} ${-h*.11} 0 ${-h*.22}" stroke="#fff" stroke-width="${Math.max(3,w*.03)}" fill="none" opacity=".8"/>`).join('')}`;
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#26304a"/>${[0,1,2,3,4].map(q=>`<rect x="${x+w*(.06+q*.19)}" y="${y+h*(.35-(q%2)*.16)}" width="${w*.14}" height="${h}" fill="#3a4766"/>`).join('')}${[0,1,2,3,4,5,6,7].map(q=>`<rect x="${x+w*(.09+q*.107)}" y="${y+h*(.5+(q%3)*.11)}" width="${w*.04}" height="${w*.04}" fill="${Y}"/>`).join('')}`;
}
function laptop(x,y,s,inner){return `<g transform="translate(${x},${y}) scale(${s})"><rect x="-470" y="-300" width="940" height="600" rx="26" fill="#22252b"/><rect x="-446" y="-276" width="892" height="552" rx="10" fill="#e9eef5"/>${inner}<path d="M-560 300 h1120 l-50 40 h-1020z" fill="#c9d1d9"/></g>`}
function callUI(t,umaiTalk,umaiMood,yuMood,extra=''){ // オンライン相談の画面
  return `<rect x="-446" y="-276" width="892" height="52" fill="#2f3b4a"/><circle cx="-410" cy="-250" r="9" fill="#e53935"/><text x="-390" y="-240" font-size="26" font-weight="700" fill="#fff">オンライン個別相談（無料）</text>
  <clipPath id="cuv"><rect x="-430" y="-210" width="600" height="420" rx="12"/></clipPath><g clip-path="url(#cuv)">${beach(-430,-210,600,420,t)}${person(-130,-40+525*170/88,170/88,{c:'umai',mood:umaiMood,t,talk:umaiTalk})}</g>
  <rect x="190" y="70" width="240" height="140" rx="10" fill="#cfe3d6"/>${face('cy',310,140,58,'owner',G,yuMood,t)}${extra}`;
}
function chatBubble(x,y,txt,p,ic){return fade(p,`${ic||`<circle cx="${x-130}" cy="${y}" r="22" fill="#7a4a9a"/><text x="${x-130}" y="${y+9}" text-anchor="middle" font-size="24" font-weight="900" fill="#fff">ウ</text>`}<rect x="${x-100}" y="${y-30}" width="${txt.length*24+36}" height="60" rx="20" fill="#fff" stroke="#d6dbe2" stroke-width="2"/><text x="${x-82}" y="${y+9}" font-size="24" font-weight="700" fill="${DG}">${txt}</text>`,10)}
function stamp(x,y,txt,p,c='#e53935',fs=96,rot=-10){return pop(x,y,p,`<g transform="rotate(${rot} ${x} ${y})"><rect x="${x-txt.length*fs*.5-40}" y="${y-fs*.8}" width="${txt.length*fs+80}" height="${fs*1.5}" rx="16" fill="#fff" fill-opacity=".92" stroke="${c}" stroke-width="12"/><text x="${x}" y="${y+fs*.35}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${c}">${txt}</text></g>`)}
function rewindFX(p){if(p<=0||p>=1)return '';const a=Math.sin(p*Math.PI);let s=`<rect width="1920" height="1080" fill="#0b1020" opacity="${.45*a}"/>`;
  for(let k=0;k<14;k++){const y=((k*83+p*2600)%1080);s+=`<rect x="0" y="${y}" width="1920" height="${6+k%3*4}" fill="#fff" opacity="${.18*a}"/>`}
  return s+`<g opacity="${a}"><path d="M860 470 l-80 50 l80 50z M960 470 l-80 50 l80 50z" fill="#fff"/><text x="1000" y="540" font-size="60" font-weight="900" fill="#fff">巻き戻し</text></g>`;}
function scene(i,t,lt){
  const L=SL[i],E=SE[i],at=(k,d=.5,o=0)=>seg(lt,L[k]+o,L[k]+o+d),on=k=>lt>=L[k],win=(k,j)=>clamp(seg(lt,L[k],L[k]+.4))*(j==null?1:1-seg(lt,L[j]-.1,L[j]+.3));
  let s='';
  if(i===0){
    s+=`<rect x="760" y="${GROUND-40}" width="840" height="40" rx="8" fill="#6a5646"/>`;
    const bad=at(4,.3),ck=L[2]-.45,done=lt>=ck,press=1-.12*Math.sin(Math.PI*seg(lt,ck,ck+.18));
    const btn=`<g transform="translate(310,-95) scale(${press}) translate(-310,95)"><rect x="190" y="-130" width="240" height="70" rx="35" fill="${done?'#7a4a9a':T}"/><text x="310" y="-82" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">${done?'契約完了！':'契約する'}</text></g>`+(done&&lt<ck+.5?`<circle cx="310" cy="-95" r="${30+90*seg(lt,ck,ck+.5)}" fill="none" stroke="#fff" stroke-width="6" opacity="${1-seg(lt,ck,ck+.5)}"/>`:'');
    s+=laptop(1180,520,.8,callUI(t,talking('U',t),'happy','happy')+`<g opacity="${1-bad}">${btn}</g>`+(bad>0?`<g opacity="${bad}"><rect x="-446" y="-276" width="892" height="552" fill="#b71c1c" opacity=".55"/><path d="M-200 -276 L-120 -60 L-220 60 L-80 276 M120 -276 L60 -100 L180 40 L90 276" stroke="#fff" stroke-width="8" fill="none"/></g>`:''));
    if(on(1)&&lt<ck+.9){const fp=eo(at(1,1.8,.3)),cs=1-.15*Math.sin(Math.PI*seg(lt,ck-.05,ck+.15));s+=`<path transform="translate(${1640-225*fp},${880-424*fp}) scale(${cs})" d="M0 0 L0 46 L12 34 L22 56 L32 51 L22 30 L38 30z" fill="#fff" stroke="${DG}" stroke-width="4" stroke-linejoin="round"/>`}
    s+=P(430,GROUND,.92,{c:'owner',who:'Y',pose:on(3)&&!on(4)?'cheer':(on(4)?'think':'stand'),mood:on(4)?'worry':'happy'},t);
    if(on(5)){const q=win(5,7);s+=fade(q,`<rect width="1920" height="1080" fill="#120c1c" opacity=".72"/>`,0)+pop(960,500,q,`${box(330,170,1260,660,40)}<text x="960" y="265" text-anchor="middle" font-size="58" font-weight="900" fill="${DG}">この3人の正体は？</text>${['umaiA','umaiB','umaiC'].map((c2,k)=>{const x=560+k*400;return `${face('q'+k,x,470,120,c2,'#7a4a9a','happy',t)}<text x="${x}" y="660" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">生徒${'ABC'[k]}さん</text><text x="${x}" y="712" text-anchor="middle" font-size="34" font-weight="900" fill="${T}">月100万円！</text>`}).join('')}`)+pop(960,800,at(6,.4)*q,`<rect x="610" y="760" width="700" height="84" rx="42" fill="${Y}"/><text x="960" y="816" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">ヒントは、画面のどこかに…</text>`);}
    s+=rewindFX(seg(lt,L[7]+.5,E[7]+.4));
    const tp=seg(lt,E[7]+.4,E[7]+1.1);
    s+=pop(960,470,tp,`<rect width="1920" height="1080" fill="#000" opacity=".4"/><rect x="290" y="300" width="1340" height="330" rx="40" fill="#fff"/><rect x="760" y="262" width="400" height="76" rx="38" fill="${G}"/><text x="960" y="314" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">アキヤド劇場</text><text x="960" y="470" text-anchor="middle" font-size="92" font-weight="900" fill="${DG}">その民泊副業、</text><text x="960" y="590" text-anchor="middle" font-size="92" font-weight="900" fill="${T}">本当に「簡単」？</text>`);
    s+=fade(seg(lt,.2,.6)*(1-seg(lt,5,5.5)),`<rect x="40" y="40" width="760" height="56" rx="28" fill="#000" opacity=".4"/><text x="70" y="78" font-size="26" font-weight="700" fill="#fff">※ この物語はフィクションです。人物・団体は架空です</text>`,0);
  }
  if(i===1){
    s+=pop(740,190,win(0,1),`<rect x="540" y="135" width="400" height="110" rx="55" fill="#fff"/><text x="740" y="213" text-anchor="middle" font-size="60" font-weight="900" fill="${DG}">1週間前</text>`);
    s+=P(420,GROUND,.92,{c:'owner',who:'Y',pose:on(1)?'phone':'stand',mood:on(5)||(on(3)&&!on(4))?'happy':'smile'},t);
    const chat=on(4);
    let ui;
    if(!chat){ui=`<rect x="-172" y="-300" width="344" height="60" fill="#fff"/><text x="0" y="-260" text-anchor="middle" font-size="26" font-weight="900" fill="#2c3a33">SNS</text>${[0,1].map(k=>`<rect x="-150" y="${-220+k*90}" width="300" height="70" rx="10" fill="#eef1f4"/>`).join('')}`+
      (on(2)?`<g opacity="${at(2,.4)}"><rect x="-160" y="-50" width="320" height="330" rx="16" fill="#fff4d6" stroke="${Y}" stroke-width="4"/><text x="-140" y="-18" font-size="18" font-weight="700" fill="#999">広告</text><text x="0" y="40" text-anchor="middle" font-size="34" font-weight="900" fill="${T}">旅しながら！</text><text x="0" y="90" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">民泊で月100万円</text><text x="0" y="140" text-anchor="middle" font-size="24" font-weight="900" fill="#6b3fa0">スマホだけ・物件なしOK</text><rect x="-120" y="180" width="240" height="64" rx="32" fill="${G}" stroke="#fff" stroke-width="${on(3)&&lt>L[3]+2.4?8:0}"/><text x="0" y="222" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">無料で登録</text></g>`:'');}
    else{ui=`<rect x="-172" y="-300" width="344" height="610" fill="#dfe8ef"/><rect x="-172" y="-300" width="344" height="60" fill="#7a4a9a"/><text x="0" y="-260" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">ウマイ先生（公式）</text>`+
      [['ご登録ありがとうございます！',.4],['無料動画をプレゼント！',1.6],['今なら個別相談も無料！',2.8],['私も月100万円♪',4.0]].map(([m2,o],k)=>chatBubble(-10,-200+k*100,m2,at(4,.3,o),k===3?face('cbB',-140,-200+k*100,24,'umaiB','#7a4a9a','happy',t):'')).join('').replace(/font-size="24"/g,'font-size="21"');}
    s+=phoneUI(1180,500,1.0,ui,1);
  }
  if(i===2){ // ウマイ先生の旅動画 → お試しマニュアル
    s+=P(400,GROUND,.92,{c:'owner',who:'Y',pose:'phone',mood:on(4)&&lt>L[4]+3.2?'worry':(on(6)?'smile':'happy')},t);
    if(!on(3)){
      const th=(k,x,y)=>{const w=130,h=88;let g=`<clipPath id="yt${k}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8"/></clipPath><g clip-path="url(#yt${k})">`;
        g+=place(k,x,y,w,h,t);
        g+=`</g><circle cx="${x+w-26}" cy="${y+h-24}" r="20" fill="#fff"/>`+`<g transform="translate(${x+w-26},${y+h-24})">${face('ytf'+k,0,0,18,'umai','#2f9aa0','happy',t)}</g>`;
        return g};
      const items=[['今日は南の島から！','12万回'],['温泉で、のんびり','9.8万回'],['夜景の街で乾杯','15万回']];
      let ui=`<rect x="-172" y="-300" width="344" height="610" fill="#fff"/><rect x="-172" y="-300" width="344" height="60" fill="#e53935"/><text x="0" y="-260" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">ウマイの旅チャンネル</text>`;
      items.forEach(([ti,vw],k)=>{const y=-225+k*112;ui+=fade(at(0,.3,[.6,1.4,2.2][k]),`${th(k,-160,y)}<text x="-20" y="${y+34}" font-size="21" font-weight="900" fill="${DG}">${ti}</text><text x="-20" y="${y+66}" font-size="19" font-weight="700" fill="#888">${vw} 再生</text>`,0)});
      ui+=fade(at(2,.3),`<rect x="-160" y="118" width="320" height="2" fill="#e5e5e5"/><text x="-150" y="150" font-size="19" font-weight="900" fill="#888">コメント</text>${[['umaiC','月100万円いきました！'],['umaiA','先生のおかげです♪']].map(([c2,m2],k)=>`${face('ytc'+k,-135,190+k*64,22,c2,'#ccc','happy',t)}<text x="-102" y="${197+k*64}" font-size="21" font-weight="700" fill="${DG}">${m2}</text>`).join('')}`,0);
      s+=phoneUI(1180,500,1.0,ui,at(0,.4));
      if(on(2))s+=pop(1600,760,at(2,.4,2.4),`<g transform="rotate(-6 1600 760)"><rect x="1420" y="700" width="360" height="110" rx="55" fill="${Y}"/><text x="1600" y="775" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">あこがれる…！</text></g>`);
    }
    if(on(3)){
    s+=pop(1180,470,at(3,.5),`${box(900,200,560,600,20)}<rect x="900" y="200" width="560" height="130" rx="20" fill="${T}"/><text x="1180" y="262" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">民泊スタート</text><text x="1180" y="310" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">マニュアル</text>`+(on(4)?`<text x="1180" y="440" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">第1章</text><text x="1180" y="520" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">まずは、物件を</text><text x="1180" y="580" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">探しましょう。</text>`:`<text x="1180" y="560" text-anchor="middle" font-size="72" font-weight="900" fill="${T}">2,980円</text>`)+(on(4)?`<text x="1180" y="720" text-anchor="middle" font-size="28" font-weight="700" fill="#999">（以上）</text>`:''));
    s+=stamp(1560,150,'うすっ！',at(4,.4,3.4),'#6b3fa0',70,-12);
    if(on(6))s+=pop(1180,820,at(6,.4,.4),`<rect x="900" y="770" width="560" height="90" rx="45" fill="#7a4a9a"/><text x="1180" y="828" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">続きは個別相談で！</text>`);
    }
  }

  if(i===3){
    s+=P(260,GROUND,.86,{c:'owner',who:'Y',pose:on(12)?'shake':(on(9)?'think':'stand'),mood:on(9)?'worry':'happy'},t);
    let extra='';
    // 生徒さんのインタビュー動画（ひとりずつ、通話画面いっぱいに）
    [4,5,6].forEach((ln,k)=>{if(on(ln)&&!on(ln+1)){const c2=['umaiA','umaiB','umaiC'][k],p=at(ln,.35);
      extra+=`<g opacity="${p}"><clipPath id="iv${k}"><rect x="-430" y="-210" width="600" height="420" rx="12"/></clipPath><g clip-path="url(#iv${k})">${place(k,-430,-210,600,420,t)}${person(-130,-40+525*170/88,170/88,{c:c2,mood:'happy',t,talk:talking('ABC'[k],t)})}</g>
      <rect x="-418" y="-198" width="170" height="44" rx="8" fill="#e53935"/><text x="-333" y="-166" text-anchor="middle" font-size="24" font-weight="900" fill="#fff">インタビュー</text>
      <rect x="-418" y="120" width="300" height="78" rx="12" fill="#fff" opacity=".95"/><text x="-400" y="152" font-size="24" font-weight="900" fill="${DG}">生徒${'ABC'[k]}さん（${['元・会社員','子育て中','定年後'][k]}）</text><text x="-400" y="186" font-size="26" font-weight="900" fill="${T}">月100万円！</text></g>`;}});
    if(on(7))extra+=`<g opacity="${win(7,8)}"><rect x="-430" y="-210" width="600" height="420" rx="12" fill="#1f2a24" opacity=".85"/><text x="-130" y="-170" text-anchor="middle" font-size="28" font-weight="900" fill="${Y}">生徒さんの声</text>${['umaiA','umaiB','umaiC'].map((c2,k)=>{const cx=-320+k*190;return `<rect x="${cx-88}" y="-145" width="176" height="340" rx="16" fill="#fff"/>${face('st'+k,cx,-60,62,c2,'#7a4a9a','happy',t)}<text x="${cx}" y="40" text-anchor="middle" font-size="24" font-weight="900" fill="${DG}">生徒${'ABC'[k]}さん</text><text x="${cx}" y="80" text-anchor="middle" font-size="20" font-weight="700" fill="#4a5a52">${['南の島から','温泉宿から','海外から'][k]}</text><text x="${cx}" y="130" text-anchor="middle" font-size="27" font-weight="900" fill="${T}">月100万円！</text>`}).join('')}</g>`;
    if(on(8))extra+=pop(310,-120,at(8,.4,.35)*(1-seg(lt,L[10]-.1,L[10]+.3)),`<g transform="rotate(4 310 -120)"><rect x="180" y="-200" width="260" height="160" rx="14" fill="#fff" stroke="${T}" stroke-width="6"/><text x="310" y="-150" text-anchor="middle" font-size="26" font-weight="900" fill="${DG}">フルサポート</text><text x="310" y="-80" text-anchor="middle" font-size="56" font-weight="900" fill="${T}">80万円</text></g>`);
    if(on(10))extra+=pop(310,-120,at(10,.4,.35)*(1-seg(lt,L[11]-.1,L[11]+.3)),`<rect x="180" y="-210" width="260" height="70" rx="35" fill="#6b3fa0"/><text x="310" y="-164" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">カードローン</text><rect x="180" y="-120" width="260" height="70" rx="35" fill="#2f3b4a"/><text x="310" y="-74" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">画面を共有</text>`);
    if(on(11))extra+=pop(310,-120,at(11,.4,1.4),`<g transform="rotate(-8 310 -120)"><rect x="170" y="-180" width="280" height="110" rx="18" fill="#e53935"/><text x="310" y="-108" text-anchor="middle" font-size="54" font-weight="900" fill="#fff">今日だけ！</text></g>`);
    s+=pop(1180,470,at(0,.5),laptop(1180,470,1.08,callUI(t,talking('U',t),'happy',on(9)?'worry':'happy',extra)));
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
    if(!on(1))s+=pop(1180,520,at(0,.5,.3),`${box(720,300,920,460,30)}<text x="1180" y="370" text-anchor="middle" font-size="36" font-weight="900" fill="#4a5a52">ウマイ先生の言葉</text>${['物件がなくてもOK','スマホだけで、すぐ','借りれば、すぐに返せます'].map((w,k)=>`<rect x="780" y="${405+k*110}" width="800" height="90" rx="45" fill="#f3eef8"/><text x="1180" y="${463+k*110}" text-anchor="middle" font-size="42" font-weight="900" fill="#6b3fa0">「${w}」</text>`).join('')}`);
    if(on(1)&&!on(2))s+=fade(at(1,.4),`${house(1180,840,.75,1)}<rect x="1400" y="430" width="10" height="410" fill="#6a5646"/><rect x="1340" y="430" width="240" height="96" rx="12" fill="#fff"/><text x="1460" y="492" text-anchor="middle" font-size="40" font-weight="900" fill="${G}">借りた家</text>${stamp(830,420,'OK',at(1,.4,3.2),G,80,-6)}`,0);
    if(on(2)&&!on(3)){s+=[['大家さんの許可','key'],['役所への届け出','doc'],['家具の準備','home']].map(([w,ic],k)=>{const x=720+k*430;return pop(x,480,at(2,.4,[0.6,1.8,3.0][k]),`${box(x-190,340,380,280,24)}${icon(x,430,56,ic,G,'#fff',.8)}<text x="${x}" y="560" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">${w}</text>`)}).join('');
      s+=pop(1150,760,at(2,.5,4.2),`<rect x="890" y="710" width="520" height="100" rx="50" fill="${T}"/><text x="1150" y="778" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">準備に約7か月</text>`);}
    const claim=(k,w,note)=>pop(1150,480,at(k,.4),`${box(720,330,860,300,30)}<text x="1150" y="510" text-anchor="middle" font-size="${w.length>8?60:72}" font-weight="900" fill="${DG}">「${w}」</text><path d="M760 360 L1540 600 M1540 360 L760 600" stroke="#e53935" stroke-width="20" stroke-linecap="round" opacity="${at(k,.3,1.4)}"/>`)+(note?pop(1150,740,at(k,.4,2.4),`<rect x="770" y="690" width="760" height="96" rx="48" fill="#e53935"/><text x="1150" y="754" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">${note}</text>`):'');
    if(on(3)&&!on(4))s+=claim(3,'スマホだけで、すぐ','')+pop(1760,200,at(3,.4),face('yf7',1760,200,80,'owner',G,'worry',t,talking('Y',t)));
    if(on(4)&&!on(5))s+=claim(4,'借りれば、すぐ返せる','返済は、毎月やってくる');
    if(on(5)&&!on(7)){const g=eo(at(5,1.6,1));s+=fade(at(5,.4),`${box(640,290,1080,520,30)}<text x="1180" y="360" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">ウマイ先生のお金の出どころ（イメージ）</text><path d="M760 740 H1600" stroke="#9fb5a8" stroke-width="6"/>
      <rect x="840" y="${740-60*g}" width="200" height="${60*g}" rx="8" fill="#9fb5a8"/><text x="940" y="790" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">民泊</text>
      <rect x="1300" y="${740-330*g}" width="200" height="${330*g}" rx="8" fill="${T}"/><text x="1400" y="790" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">サポート代</text>${g>.95?coin(1560,430,40):''}`,0);
      if(on(6))s+=pop(1760,200,at(6,.4),face('yf8',1760,200,80,'owner',G,'worry',t,talking('Y',t)));}
    if(on(7))s+=pop(1180,500,at(7,.5),`<rect x="760" y="420" width="840" height="160" rx="80" fill="#1f1530"/><text x="1180" y="525" text-anchor="middle" font-size="64" font-weight="900" fill="${Y}">最後の秘密…</text>`);
  }
  if(i===8){ // どんでん返し：生徒さんは全員…
    s+=hall(lt,true)+`<rect width="1920" height="1080" fill="#000" opacity="${.25*at(3,.4)}"/>`;
    s+=P(150,GROUND+40,.72,{c:'staff',who:'M',pose:'present',mood:'happy'},t);
    const rev=at(4,.5,-.1),X=[600,1010,1420],Rr=150,Y0=430;
    X.forEach((x,k)=>{const c2=['umaiA','umaiB','umaiC'][k],p=at(0,.4,.6+k*.4);
      let g=`<g opacity="${1-rev}">${face('tw'+k,x,Y0,Rr,c2,'#7a4a9a','happy',t)}</g>`;
      if(rev>0)g+=`<g opacity="${rev}">${face('tu'+k,x,Y0,Rr,'umai','#7a4a9a',on(5)?'happy':'worry',t,talking('U',t))}</g>`;
      const gl=Math.sin(Math.PI*clamp(rev*1.15))*(rev<1?1:0)+(on(3)&&!on(4)?.35*Math.max(0,Math.sin(lt*23+k*2)):0);
      if(gl>0.02)for(let q=0;q<7;q++){const yy=Y0-Rr+rnd(q*7+k+Math.floor(lt*12))*Rr*2,hh=6+rnd(q+k*3+Math.floor(lt*12))*18,dx=(rnd(q*3+Math.floor(lt*15))-.5)*60*gl;g+=`<rect x="${x-Rr+dx}" y="${yy}" width="${Rr*2}" height="${hh}" fill="${q%2?'#00e5ff':'#ff2d95'}" opacity="${.55*gl}"/>`}
      if(rev>.6)g+=pop(x+Rr*.72,Y0-Rr*.72,clamp((rev-.6)*2.5),`<circle cx="${x+Rr*.72}" cy="${Y0-Rr*.72}" r="40" fill="#111"/><text x="${x+Rr*.72}" y="${Y0-Rr*.72+15}" text-anchor="middle" font-size="40" font-weight="900" fill="#00e5ff">AI</text>`);
      g+=`<rect x="${x-130}" y="${Y0+Rr+20}" width="260" height="${rev>0?70:110}" rx="20" fill="#fff"/>`+(rev>0?`<text x="${x}" y="${Y0+Rr+68}" text-anchor="middle" font-size="36" font-weight="900" fill="#6b3fa0">ウマイ先生</text>`:`<text x="${x}" y="${Y0+Rr+62}" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">生徒${'ABC'[k]}さん</text><text x="${x}" y="${Y0+Rr+104}" text-anchor="middle" font-size="30" font-weight="900" fill="${T}">月100万円！</text>`);
      if(on(1)&&!on(4)){const pu=.6+.4*Math.abs(Math.sin(lt*5));g+=`<circle cx="${x}" cy="${Y0+Rr*.86}" r="${Rr*.3}" fill="none" stroke="${Y}" stroke-width="8" opacity="${pu*at(1,.3,.2)}"/><circle cx="${x+Rr*.27}" cy="${Y0+Rr*.1}" r="${Rr*.14}" fill="none" stroke="${Y}" stroke-width="7" opacity="${pu*at(1,.3,.5)}"/>`}
      s+=pop(x,Y0,p,g);});
    const cd=lt-(L[1]-3.2);if(cd>0&&cd<3.2)s+=pop(1010,170,clamp((cd%1)*4),`<circle cx="1010" cy="170" r="66" fill="${Y}"/><text x="1010" y="198" text-anchor="middle" font-size="80" font-weight="900" fill="${DG}">${Math.max(1,3-Math.floor(cd))}</text>`);
    if(lt<L[1]-3.3)s+=fade(at(0,.4),`<text x="1010" y="200" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">3人の正体は？</text>`,0);
    if(on(4))s+=pop(1010,180,at(4,.4,.3),`<g transform="rotate(-4 1010 180)"><rect x="560" y="110" width="900" height="130" rx="30" fill="#e53935"/><text x="1010" y="200" text-anchor="middle" font-size="64" font-weight="900" fill="#fff">全員、AIのウマイ先生！</text></g>`);
    if(on(2)&&!on(4))s+=pop(1780,180,at(2,.4),face('yt',1780,180,80,'owner',G,'worry',t,talking('Y',t)));
    if(on(6))s+=pop(1780,180,at(6,.3),face('yt2',1780,180,80,'owner',G,'worry',t,talking('Y',t)));
  }
  if(i===9){ // エンディング
    s+=house(1000,GROUND,.95,1)+sparkle(800,330,1.3,lt,0)+sparkle(1220,300,1.1,lt,2);
    s+=P(330,GROUND,.9,{c:'owner',who:'Y',pose:'cheer',mood:'happy'},t)+P(1620,GROUND,.86,{c:'staff',who:'M',pose:on(5)?'present':(on(1)&&!on(4)?'present':'wave'),mood:'happy',flip:true},t);
    const off=1-at(4,.3);
    if(on(1)&&!on(5))[['1','うますぎる話は、まず疑う'],['2','借金・画面共有は、ストップ'],['3','その場で決めず、相談する']].forEach(([no,w],k)=>{s+=checkRow(520,290+k*150,900,no,w,'',at(1+k)*off,T)});
    s+=pop(960,420,at(5,.5),`${box(500,250,920,330,36)}${LOGO(760,290,1.2)}<rect x="620" y="400" width="680" height="92" rx="46" fill="${T}"/><text x="960" y="460" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">民泊の始め方・無料相談</text><text x="960" y="545" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">rivia-co.com/media.html</text>`);
    if(on(6)){const rx=-200+2400*at(6,2.4);s+=speedLines(rx-460,820,1)+P(rx,GROUND+110,.62,{c:'umai',who:'U',pose:'walk',mood:'worry',disguise:true},t*2);}
  }
  if(i===10){ // 最後のオチ
    s+=`<rect width="1920" height="1080" fill="#4a4458"/><rect y="${GROUND-10}" width="1920" height="${1090-GROUND}" fill="#5e4a3c"/><rect x="1500" y="140" width="300" height="220" rx="10" fill="#2a2638"/><path d="M1650 140 v220 M1500 250 h300" stroke="#4a4458" stroke-width="10"/>${[0,1,2].map(k=>`<circle cx="${1560+k*90}" cy="${190+rnd(k)*30}" r="2.5" fill="#fff" opacity=".8"/>`).join('')}`;
    s+=`<rect x="140" y="140" width="660" height="470" fill="#ddd"/><clipPath id="bclip"><rect x="150" y="150" width="640" height="450"/></clipPath><g clip-path="url(#bclip)">${beach(150,150,640,450,t)}</g><rect x="465" y="610" width="10" height="${GROUND-610}" fill="#888"/><rect x="380" y="${GROUND-20}" width="180" height="16" rx="8" fill="#777"/>`;
    s+=pop(470,200,at(1,.4,.3),`<g transform="rotate(-6 470 200)"><rect x="250" y="150" width="440" height="96" rx="20" fill="#e53935"/><text x="470" y="216" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">AIで作った背景</text></g>`);
    s+=`<rect x="860" y="${GROUND-150}" width="260" height="150" fill="#8a6a4c"/><rect x="850" y="${GROUND-165}" width="280" height="20" rx="6" fill="#a2805c"/><path d="M930 ${GROUND-165} l8 -70 h64 l8 70z" fill="#fff"/><rect x="936" y="${GROUND-222}" width="68" height="20" fill="#e53935"/>`;
    s+=P(560,GROUND,.92,{c:'umai',who:'U',pose:on(4)&&!on(5)?'cheer':(on(2)?'phone':'stand'),mood:on(1)&&!on(2)?'worry':'happy'},t);
    const ad=`<rect x="-172" y="-300" width="344" height="60" fill="#fff"/><text x="0" y="-260" text-anchor="middle" font-size="26" font-weight="900" fill="#2c3a33">SNS</text><rect x="-160" y="-230" width="320" height="520" rx="16" fill="#fff4d6" stroke="${Y}" stroke-width="4"/><text x="-140" y="-200" font-size="18" font-weight="700" fill="#999">広告</text>${face('sg0',0,-120,62,'sugoi','#c9a227','happy',t)}<text x="0" y="-22" text-anchor="middle" font-size="22" font-weight="900" fill="#4a5a52">スゴイ先生</text><text x="0" y="30" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">あなたも先生に！</text><text x="0" y="90" text-anchor="middle" font-size="44" font-weight="900" fill="${T}">月1000万円</text><rect x="-110" y="120" width="220" height="50" rx="12" fill="#e53935"/><text x="0" y="155" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">今日だけ！</text><g transform="translate(0,225) scale(${1-.12*Math.sin(Math.PI*seg(lt,L[4],L[4]+.2))})"><rect x="-110" y="-32" width="220" height="64" rx="32" fill="${on(4)?'#7a4a9a':G}"/><text x="0" y="10" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">${on(4)?'申し込み完了':'申し込む'}</text></g>`;
    if(on(2))s+=phoneUI(1350,490,.95,ad,at(2,.4)*(1-at(5,.4)));
    if(on(5)){const q=at(5,.5);
      s+=pop(1220,480,q,`${box(800,150,840,700,36)}<text x="840" y="205" font-size="30" font-weight="900" fill="#4a5a52">お金の流れ（イメージ）</text>
      ${face('sg1',1220,330,80,'sugoi','#c9a227','happy',t)}<rect x="1100" y="420" width="240" height="44" rx="22" fill="#c9a227"/><text x="1220" y="452" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">スゴイ先生</text>
      ${face('um1',1220,580,64,'umai','#7a4a9a','worry',t)}<rect x="1100" y="652" width="240" height="44" rx="22" fill="#7a4a9a"/><text x="1220" y="684" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">ウマイ先生</text>
      ${['guest1','owner','guest2'].map((c2,k)=>face('gs'+k,1010+k*210,770,40,c2,G,'worry',t)).join('')}<text x="1220" y="838" text-anchor="middle" font-size="24" font-weight="900" fill="${DG}">生徒さんたち</text>
      ${[0,1].map(k=>{const y0=[730,500][k],y1=[650,420][k],f=((lt*1.2+k*.5)%1);return `<path d="M1390 ${y0} L1390 ${y1}" stroke="#c9a227" stroke-width="6" stroke-dasharray="10 8"/>${coin(1390,y0-(y0-y1)*f,20)}`}).join('')}`);
      s+=pop(1400,300,at(5,.4,1.2),`<circle cx="1420" cy="290" r="44" fill="${Y}"/><text x="1420" y="312" text-anchor="middle" font-size="60" font-weight="900" fill="${DG}">？</text>`);}
    s+=fade(seg(lt,E[5]+.6,E[5]+1.3),`<rect width="1920" height="1080" fill="#1f2a24"/><text x="960" y="400" text-anchor="middle" font-size="60" font-weight="900" fill="#fff">最後まで見てくれて、ありがとう！</text><text x="960" y="510" text-anchor="middle" font-size="34" font-weight="700" fill="#dfe9e3">この物語はフィクションです。登場する人物・団体は架空のものです。</text>${[CREDIT.split('　').slice(0,4),CREDIT.split('　').slice(4)].map((r,k)=>`<text x="960" y="${620+k*42}" text-anchor="middle" font-size="28" font-weight="700" fill="#b8c9bf">${r.join('　')}</text>`).join('')}<rect x="780" y="715" width="360" height="100" rx="50" fill="#fff"/>${LOGO(810,730,1.1)}`,0);
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
