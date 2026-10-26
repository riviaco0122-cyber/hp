#!/usr/bin/env python3
"""アキヤドの解説動画 第2回「民泊の手続き2つの違い」（約8分・1920×1080）を作る。

- 話し手はアニメの民泊戦略家「アキ」。聞き手にユウタ。型は docs/youtube/manual.md 1-2章、骨組みは docs/youtube/ep2-plan.md。
- 第1回からの改善（2026-10-23）: 冒頭30秒に自己紹介を入れない（名乗りは約束の直後に一言だけ）／イラストを作り込む
  （背景の奥行き・質感と影・小物・色の深み・動き。ep2-plan.md 3章）。
- 数字の出どころ（説明欄にも書く）:
  営業日数は年180日以内・民泊新法の正式名称と施行（2018年6月）（住宅宿泊事業法）、
  旅館業の許可・簡易宿所の広さ（10人未満は1人3.3㎡、10人以上は33㎡以上）（旅館業法・同施行令）、
  宿に使う部分が200㎡を超えると用途変更の確認申請（建築基準法）、
  （簡易宿所の全国平均の稼働率は一次出典を照合できなかったため、使っていない）、180÷365＝約49%（計算）、
  開業から約8.5か月の平均の稼働率 約53%（創業メンバーが運営する下田の宿。運営事例の記事。experience.md 3-2）。この水準が1年続くと 0.53×365＝約193日（計算）、
  消防設備 約40万円→約60万円（取材事例の記事。2025年12月・本人申告。個人の事例）。
- 部品・書き出しは make_explainer.py / make_scam_ep1.py と共通。声は VOICEVOX（クレジットは最後の画面と説明欄）。
使い方: python3 tools/video/make_strategy_ep2.py [出力.mp4] [--hq] [--preview 秒 ...] [--no-check]
分けて書き出す: --work <フォルダ> --part 1 / --part 2 … を「残り 0 区切り」まで → 最後に --work <フォルダ>（--part なし）で mp4 にする（--hq は全部の回で付ける）
書き出しの前に layout_check.py の自動点検が走り、問題があれば止まる。
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import make_explainer as base
from make_scam_ep1 import wrap
from voicevox_tts import tts

FPS = 24
PART_FRAMES = 1200  # 分けて書き出すときの1区切りのコマ数（高画質でも1区切り8分ほど）
VOICES = {
    "A": dict(name="戦略家 アキ", style=83, speed=1.03, intonation=1.2, pitch=0.0),   # 青山龍星（喜び）。明るく、テンポよく
    "K": dict(name="ジングル", style=1, speed=1.0, intonation=1.6, pitch=0.04),         # ずんだもん（あまあま）。オープニングの呼び込み
    "Y": dict(name="ユウタ", style=11, speed=1.08, intonation=1.15, pitch=0.0),        # 玄野武宏
}
MODELS = [0, 4, 15]
CREDIT = "VOICEVOX:青山龍星　VOICEVOX:玄野武宏　VOICEVOX:ずんだもん"
EP_TITLE = "民泊の手続き2つの違い"  # オープニングのあと、左上に出す今回のタイトル
NOTE = "※ 情報提供が目的で、特定の選択を勧めるものではありません。ルールは変わり、自治体で違います。"

SCENES = [
    ("sunset", 2.0, [
        ('A', '民泊戦略家の、アキです。', dict(pre=3.4, call=(-3.0, 'K', 'アキヤド、みんぱくスクール！'), sfx=[(-3.9, 'whoosh'), (-3.55, 'pop'), (-2.9, 'bling'), (-0.4, 'whoosh'), (0.2, 'pop'), (1.6, 'pop')])),
        ('A', '空き家で民泊を始めたい人へ。まず、結論から話します。', dict(sfx=[(0.4, 'pop')])),
        ('A', '国のルールに沿った手続きは、2つあります。', dict(say='国のルールに沿った手続きは、ふたつあります。', sfx=[(0.4, 'pop')])),
        ('A', '1つは、泊められるのが、1年の半分ほどまでの方法です。', dict(say='ひとつは、泊められるのが、いちねんの半分ほどまでの方法です。', sfx=[(0.4, 'pop')])),
        ('A', 'もう1つは、1年中、泊められる方法です。', dict(say='もうひとつは、いちねんじゅう、泊められる方法です。', sfx=[(0.4, 'pop')])),
        ('A', '半分までの方法を「届出」、1年中の方法を「許可」と呼びます。', dict(say='半分までの方法を、とどけで、いちねんじゅうの方法を、きょか、と呼びます。', sfx=[(0.4, 'pop')])),
        ('A', '許可のほうが、お得に見えますよね。でも、実は、そう単純ではありません。', dict(sfx=[(0.4, 'pop')])),
        ('A', '許可には、届出にない条件があるからです。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'この動画で、順に説明します。最後には、あなたの家はどちらか、自分で判断できるようになります。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'では、あなたの家は、届出でしょうか。許可でしょうか。', dict(sfx=[(0.4, 'pop')])),
        ('A', '決めるのは、この3つです。1つめは、1年に何日、泊めたいか。', dict(say='決めるのは、このみっつです。ひとつめは、いちねんに、なんにち、泊めたいか。', sfx=[(0.4, 'pop')])),
        ('A', '2つめは、家のある場所。3つめは、建物の条件です。', dict(say='ふたつめは、家のある場所。みっつめは、建物の条件です。', sfx=[(0.4, 'pop')])),
        ('A', '民泊が初めての人にも、分かるように話します。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'まず、民泊とは何かからです。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("morning", 2.0, [
        ('A', '最初の問いは、民泊の手続きには、何があるのか、です。', dict(sfx=[(0, 'chime')])),
        ('A', '民泊とは、空き家や自宅に、旅行者を泊めて、お金をもらうことです。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'お金をもらって泊めるなら、国のルールに沿った手続きが必要です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '届出は、民泊新法という法律に沿って、役所に「民泊をやります」と知らせる方法です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '許可は、旅館業法という法律に沿って、保健所の許可をもらう方法です。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'この2つの違いで、いちばん大きいのは、泊められる日数です。次は、その日数を詳しく見ます。', dict(say='このふたつの違いで、いちばん大きいのは、泊められる日数です。次は、その日数を詳しく見ます。', sfx=[(0.4, 'pop')])),
    ]),
    ("noon", 2.0, [
        ('A', 'では、その違いから。まず、何日、泊められるのか、です。', dict(sfx=[(0, 'chime')])),
        ('A', '届出で泊められるのは、1年に180日まで。1年の約半分です。', dict(say='届出で泊められるのは、いちねんに、ひゃくはちじゅうにちまで。いちねんの約半分です。', sfx=[(0.4, 'pop')])),
        ('A', '許可なら、日数の制限がありません。1年中、泊められます。', dict(say='許可なら、日数の制限がありません。いちねんじゅう、泊められます。', sfx=[(0.4, 'pop')])),
        ('A', 'ただし、地域のルールで、届出の180日が、さらに短くなることもあります。', dict(say='ただし、地域のルールで、届出の、ひゃくはちじゅうにちが、さらに短くなることもあります。', sfx=[(0.4, 'pop')])),
        ('A', '180日は、多いのか、少ないのか。それは、お客さんの入り方で決まります。', dict(say='ひゃくはちじゅうにちは、多いのか、少ないのか。それは、お客さんの入り方で決まります。', sfx=[(0.4, 'pop')])),
        ('A', '入り方を表す数字が、稼働率です。1年のうち、お客さんが泊まった日の割合です。', dict(say='入り方を表す数字が、稼働率です。いちねんのうち、お客さんが泊まった日の割合です。', sfx=[(0.4, 'pop')])),
        ('A', '人気の宿ほど稼働率が高く、届出の180日に、早く上限に近づきます。', dict(say='人気の宿ほど稼働率が高く、届出の、ひゃくはちじゅうにちに、早く上限に近づきます。', sfx=[(0.4, 'pop')])),
        ('A', '私たちは、静岡県の下田で、宿を運営しています。開業から約8.5か月の平均で、稼働率は約53%でした。', dict(say='私たちは、静岡県の下田で、宿を運営しています。開業から、やく はってんご かげつの平均で、稼働率は、やく ごじゅうさんパーセントでした。', sfx=[(0.4, 'pop')])),
        ('A', 'このペースで1年続くと、泊まる日は約193日。届出の180日を、超えます。', dict(say='このペースで、いちねん続くと、泊まる日は、やく ひゃくきゅうじゅうさんにち。届出の、ひゃくはちじゅうにちを、超えます。', sfx=[(0.4, 'pop')])),
        ('A', 'これは一例で、手間や初期投資は含みません。どの宿でも同じではありません。', dict(sfx=[(0.4, 'pop')])),
        ('A', '私たちは、最初から1年中営業するつもりで、許可を選びました。', dict(say='私たちは、最初から、いちねんじゅう営業するつもりで、許可を選びました。', sfx=[(0.4, 'pop')])),
        ('Y', 'あまりお客さんが来ない家だと、どうなんですか？', dict(sfx=[(0.4, 'pop')])),
        ('A', 'ときどき使う家なら、180日でも足ります。その場合は、届出でも困りません。', dict(say='ときどき使う家なら、ひゃくはちじゅうにちでも足ります。その場合は、届出でも困りません。', sfx=[(0.4, 'pop')])),
        ('A', 'つまり、日数だけで見れば、許可が有利です。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("golden", 2.0, [
        ('A', 'さて、それでも届出を選ぶ人がいるのは、なぜでしょう。理由は、許可の条件にあります。', dict(sfx=[(0, 'chime')])),
        ('A', '1つめの条件は、場所です。住居専用地域とは、住宅だけを建てる地域のことです。', dict(say='ひとつめの条件は、場所です。住居専用地域とは、住宅だけを建てる地域のことです。', sfx=[(0.4, 'pop')])),
        ('Y', 'もし、うちの空き家がそこにあったら、許可は取れませんか？', dict(sfx=[(0.4, 'pop')])),
        ('A', '原則、取れません。届出なら、できます。', dict(sfx=[(0.4, 'pop')])),
        ('A', '2つめの条件は、建物です。許可には、宿としての基準があります。', dict(say='ふたつめの条件は、建物です。許可には、宿としての基準があります。', sfx=[(0.4, 'pop')])),
        ('A', '建物の図面を出して、消防の設備を付けます。保健所の確認も受けます。', dict(sfx=[(0.4, 'pop')])),
        ('A', '広さにも、目安があります。数字は、画面と概要欄にまとめました。', dict(sfx=[(0.4, 'pop')])),
        ('A', '許可が出るまでには、時間もかかります。私たちは、開業の2か月前に、保健所と消防署に相談しました。', dict(say='許可が出るまでには、時間もかかります。私たちは、開業のにかげつ前に、保健所と消防署に相談しました。', sfx=[(0.4, 'pop')])),
        ('A', '許可が出るまで、1〜2か月かかりました。許可番号がないと、予約サイトのAirbnbで、予約を受けられません。', dict(say='許可が出るまで、いっかげつから、にかげつかかりました。許可番号がないと、予約サイトの、エアビーアンドビーで、予約を受けられません。', sfx=[(0.4, 'pop')])),
        ('A', '一方、届出の条件は、軽いです。台所、浴室、トイレ、洗面がそろう家が、対象になります。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'つまり、許可は日数が強いぶん、場所と建物の条件が重いのです。それが、届出を選ぶ人がいる理由です。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("evening", 2.0, [
        ('A', 'いよいよ最後の問いです。あなたの家は、どちらでしょうか。まず、向く人から見ましょう。', dict(sfx=[(0, 'chime')])),
        ('A', '届出が向くのは、小さく試したい人、ときどき使う人、住居専用地域に家がある人です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '許可が向くのは、1年中、事業として運営したい人です。泊まる日数が多いほど、収入が増える宿だからです。', dict(say='許可が向くのは、いちねんじゅう、事業として運営したい人です。泊まる日数が多いほど、収入が増える宿だからです。', sfx=[(0.4, 'pop')])),
        ('A', 'ここで、考えてみてください。3人の空き家オーナーがいます。届出と許可の、どちらが向くでしょう。', dict(say='ここで、考えてみてください。さんにんの空き家オーナーがいます。届出と許可の、どちらが向くでしょう。', sfx=[(0.4, 'pop')])),
        ('A', '1人目は、週末だけ貸したい人。2人目は、1年中貸して、収入にしたい人。3人目は、家が住居専用地域にある人です。', dict(say='ひとりめは、週末だけ貸したい人。ふたりめは、いちねんじゅう貸して、収入にしたい人。さんにんめは、家が住居専用地域にある人です。', sfx=[(0, 'chime')])),
        ('A', '答えは、1人目が届出、2人目が許可、3人目が届出です。', dict(pre=3.2, say='答えは、ひとりめが届出、ふたりめが許可、さんにんめが届出です。', sfx=[(-3.2, 'tick'), (-2.2, 'tick'), (-1.2, 'tick'), (0, 'ding'), (1.2, 'bling')])),
        ('A', '1人目は、日数が少なくてよいので、届出。2人目は、日数が多く要るので、許可です。', dict(say='ひとりめは、日数が少なくてよいので、届出。ふたりめは、日数が多く要るので、許可です。', sfx=[(0.4, 'pop')])),
        ('A', '3人目は、住居専用地域だと、許可が原則取れないので、届出です。', dict(say='さんにんめは、住居専用地域だと、許可が原則取れないので、届出です。', sfx=[(0.4, 'pop')])),
        ('Y', '届出で始めて、あとから許可に変えられますか？', dict(sfx=[(0.4, 'pop')])),
        ('A', '許可は、新しく申請します。取れるかは、場所と建物の条件しだいです。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("twilight", 2.0, [
        ('A', 'ここからは、失敗しやすい点を、3つ話します。どれも、始める前に知っておけば防げます。', dict(say='ここからは、失敗しやすい点を、みっつ話します。どれも、始める前に知っておけば防げます。', sfx=[(0, 'chime')])),
        ('A', '1つめは、消防の設備の費用です。ある会社員オーナーさんは、想定の約40万円が、約60万円になりました。', dict(say='ひとつめは、消防の設備の費用です。ある会社員オーナーさんは、想定の、やく よんじゅうまんえんが、やく ろくじゅうまんえんになりました。', sfx=[(0.4, 'pop')])),
        ('A', '2つめは、近隣への説明不足です。私たちも、Wi-Fi工事の車の駐車で、近所から指摘を受けました。', dict(say='ふたつめは、近隣への説明不足です。私たちも、ワイファイ工事の車の駐車で、近所から指摘を受けました。', sfx=[(0.4, 'pop')])),
        ('A', '3つめは、うまい話をそのまま信じることです。「許可は簡単」「届出だけで1年中OK」と言われたら、疑ってください。', dict(say='みっつめは、うまい話をそのまま信じることです。「許可は簡単」「届出だけで、いちねんじゅうオーケー」と言われたら、疑ってください。', sfx=[(0.4, 'pop')])),
        ('A', '空き家を持っている人は、始める前に、市役所や保健所の相談窓口で、確かめてください。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("night", 6.0, [
        ('A', '最後に、あなたの家で確かめましょう。決める3つは、日数、場所、建物です。', dict(say='最後に、あなたの家で確かめましょう。決めるみっつは、日数、場所、建物です。', sfx=[(0, 'chime')])),
        ('A', '1つめは、日数です。1年に何日、泊めたいか。180日で足りるなら、届出も候補です。足りないなら、許可です。', dict(say='ひとつめは、日数です。いちねんに、なんにち、泊めたいか。ひゃくはちじゅうにちで足りるなら、届出も候補です。足りないなら、許可です。', sfx=[(0.4, 'pop')])),
        ('A', '2つめは、場所です。家は住居専用地域か。そうなら、許可は原則取れません。', dict(say='ふたつめは、場所です。家は住居専用地域か。そうなら、許可は原則取れません。', sfx=[(0.4, 'pop')])),
        ('A', '3つめは、建物です。広さや消防の設備が、許可の基準に合うか。足りないなら、整える費用がかかります。', dict(say='みっつめは、建物です。広さや消防の設備が、許可の基準に合うか。足りないなら、整える費用がかかります。', sfx=[(0.4, 'pop')])),
        ('A', '日数が多く必要で、場所も建物も条件に合うなら、許可。どれかが難しければ、届出です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '手続きの比較表は、概要欄の記事に。許可の取り方の記事と、無料相談も、概要欄のリンクからどうぞ。', dict(say='手続きの比較表は、概要欄の記事に。許可のとりかたの記事と、無料相談も、概要欄のリンクからどうぞ。', sfx=[(0.4, 'pop')])),
        ('A', '次は、第1回「民泊は第3の資産」がおすすめです。宿を、お金を生む資産として見る話です。日数の上限を知ったうえで見ると、よく分かります。', dict(say='次は、だいいっかい、「民泊は、だいさんの資産」がおすすめです。宿を、お金を生む資産として見る話です。日数の上限を知ったうえで見ると、よく分かります。', sfx=[(0.4, 'pop')])),
        ('A', 'あなたの家は、届出と許可の、どちらに向きそうですか？ コメントで教えてください。', dict(sfx=[(0.4, 'pop')])),
    ]),
]
LEAD, GAP = 0.5, 0.65
# 読みまちがえやすい言葉は、音声を作る前にひらがなに置きかえる（字幕はそのまま）
READ_FIX = [("届出", "とどけで"), ("知りたい方", "知りたいかた"), ("入れ方", "入れかた"), ("稼ぎ方", "稼ぎかた"), ("使い方", "使いかた"), ("始め方", "始めかた"),
            ("選び方", "選びかた"), ("取り方", "とりかた"), ("決め方", "決めかた"), ("見分け方", "見分けかた"), ("分け方", "分けかた"), ("一棟貸し", "いっとうがし")]

SCENE_JS = r"""
CAST.aki={skin:'#f1c7a1',hair:'#2b2422',style:'short',top:'#23395b',top2:'#1a2c47',inner:'#ffffff',jacket:true,pants:'#2a3140',shoes:'#3a2a20',glasses:true,tie:'#c95a35'};
const VNAME={A:'戦略家 アキ',Y:'ユウタ'},VCOL={A:T,Y:G};
const NAVY='#23395b',RED='#e53935';
const talking=(s,t)=>LINES.some(l=>l[2]===s&&t>=l[0]&&t<l[1]);
function subtitle(l,t){
  const lines=l[3],fs=42,h=lines.length*fs*1.45+40,w=1560,y=1048-h,o=clamp((t-l[0]+.05)/.2)*clamp((l[1]+.3-t)/.2);
  const nw=VNAME[l[2]].length*30+56,name=`<rect x="${960-w/2+28}" y="${y-26}" width="${nw}" height="52" rx="26" fill="${VCOL[l[2]]}"/><text x="${960-w/2+28+nw/2}" y="${y+10}" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">${VNAME[l[2]]}</text>`;
  return `<g opacity="${o}"><rect x="${960-w/2}" y="${y+6}" width="${w}" height="${h}" rx="24" fill="#000" opacity=".18"/><rect x="${960-w/2}" y="${y}" width="${w}" height="${h}" rx="24" fill="${DG}" opacity=".93"/>${name}${lines.map((s,i)=>`<text x="960" y="${y+28+fs*1.08+i*fs*1.45}" text-anchor="middle" font-size="${fs}" font-weight="700" fill="#fff" letter-spacing="1">${s}</text>`).join('')}</g>`;
}
const P=(x,y,s,o,t)=>person(x,y,s,Object.assign({t},o,{talk:o.who?talking(o.who,t):false}));

// ===== 共通の定義（質感のパターン・光・カードのグラデーション） =====
const DEFS=`<defs>
<pattern id="pTile" width="28" height="20" patternUnits="userSpaceOnUse"><path d="M0 20 Q14 4 28 20" fill="none" stroke="#000" stroke-opacity=".24" stroke-width="2.4"/><path d="M-14 10 Q0 -6 14 10 M14 10 Q28 -6 42 10" fill="none" stroke="#000" stroke-opacity=".16" stroke-width="2.4"/></pattern>
<pattern id="pWood" width="44" height="30" patternUnits="userSpaceOnUse"><path d="M0 8 H44 M0 23 H44" stroke="#000" stroke-opacity=".13" stroke-width="2"/><path d="M8 0 Q14 8 8 15 M30 15 Q36 23 30 30" stroke="#000" stroke-opacity=".09" stroke-width="2" fill="none"/></pattern>
<pattern id="pShoji" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M0 0 H28 M0 0 V28" stroke="#7a5a3c" stroke-width="3" opacity=".55"/></pattern>
<pattern id="pStone" width="128" height="52" patternUnits="userSpaceOnUse"><rect x="3" y="3" width="58" height="22" rx="7" fill="#fff" opacity=".13"/><rect x="67" y="3" width="58" height="22" rx="7" fill="#fff" opacity=".09"/><rect x="35" y="29" width="58" height="20" rx="7" fill="#fff" opacity=".12"/><rect x="99" y="29" width="26" height="20" rx="7" fill="#fff" opacity=".08"/><rect x="3" y="29" width="26" height="20" rx="7" fill="#fff" opacity=".08"/></pattern>
<pattern id="pHatch" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0 V18" stroke="#2e6b47" stroke-width="6" opacity=".55"/></pattern>
<pattern id="pTatami" width="70" height="36" patternUnits="userSpaceOnUse"><path d="M0 6 H70 M0 18 H70 M0 30 H70" stroke="#6f8a3c" stroke-opacity=".28" stroke-width="2"/></pattern>
<pattern id="pSlat" width="20" height="14" patternUnits="userSpaceOnUse"><rect width="20" height="2.6" y="11" fill="#fff" opacity=".16"/></pattern>
<radialGradient id="glow"><stop offset="0" stop-color="#ffd27a" stop-opacity=".9"/><stop offset=".5" stop-color="#ffb347" stop-opacity=".35"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<linearGradient id="cardG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#eef4ec"/></linearGradient>
<linearGradient id="gG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#58a377"/><stop offset="1" stop-color="#2e6b47"/></linearGradient>
<linearGradient id="gO" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e98557"/><stop offset="1" stop-color="#c95a35"/></linearGradient>
<linearGradient id="gY" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8cf85"/><stop offset="1" stop-color="#e8a23e"/></linearGradient>
<linearGradient id="gD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f5a42"/><stop offset="1" stop-color="#1f3a2b"/></linearGradient>
</defs>`;

// ===== 背景：空・遠くの山・海・町並み・木・地面の5層。場面ごとに時間帯を変える =====
const TH={
 sunset:{sk:['#ffd9a0','#f7a56b','#d9708a','#7a5aa0'],sun:'#fff3c8',sx:1480,sy:610,far:'#9a78a8',mid:'#7d6699',sea:['#f8b184','#d97a7a'],town:'#5b4a78',win:'#ffe3a0',tree:'#4b4a6f',gr:['#7a6a8c','#4e4363'],cl:'#ffd7c4',lit:.7},
 morning:{sk:['#bfe6f2','#e6f5ee','#fff6dc'],sun:'#fffbe0',sx:1560,sy:300,far:'#a8d3c6',mid:'#86bda8',sea:['#9fd8e6','#62b4cf'],town:'#6f9a86',win:'#f4fbf2',tree:'#4f8f6a',gr:['#d3e5d0','#a9c8b0'],cl:'#ffffff',lit:0},
 noon:{sk:['#6ec1ea','#a9dcf3','#e3f5fb'],sun:'#ffffff',sx:1000,sy:140,far:'#9cc8e4',mid:'#6fa9cc',sea:['#6cc3e8','#2f95c2'],town:'#5e8fae',win:'#e9f6fc',tree:'#3f8d5c',gr:['#d7e6d3','#b4cdb0'],cl:'#ffffff',lit:0},
 golden:{sk:['#f6c26b','#fbdca0','#fff0cf'],sun:'#fff4d0',sx:1560,sy:380,far:'#e9b97b',mid:'#d49a62',sea:['#f7cf8f','#e39a5b'],town:'#a8714e',win:'#fff0c2',tree:'#6f8d46',gr:['#e6d3a8','#c9b184'],cl:'#fff2d6',lit:.2},
 evening:{sk:['#f08a5d','#f6b17a','#fbd9a4'],sun:'#fff0c0',sx:1500,sy:660,far:'#c9708a',mid:'#a45a7e',sea:['#f3a37a','#c9647a'],town:'#6d3f5c',win:'#ffd27a',tree:'#5a3f5a',gr:['#9a6a76','#5f3f55'],cl:'#ffc9a0',lit:.8},
 twilight:{sk:['#2e3a6e','#6a5b97','#d78a8f'],sun:'#fdeab0',sx:1400,sy:700,far:'#52507f',mid:'#3f4170',sea:['#6a6a9c','#2f3866'],town:'#2e3258',win:'#ffd36e',tree:'#2d3558',gr:['#4a4e72','#2a2d4c'],cl:'#8f87b8',lit:1},
 night:{sk:['#0f1b38','#1d2e57','#34457a'],sun:'#f5f0c8',sx:1450,sy:230,far:'#26365f',mid:'#1d2b50',sea:['#2a3d6e','#16254a'],town:'#161f3d',win:'#ffd46e',tree:'#18294a',gr:['#33446a','#18233f'],cl:'#43557f',lit:1,stars:1},
};
function studio(t,j){
  const th=THEME[j],c=TH[th],id='b'+j;
  let s=`<defs><linearGradient id="${id}s" x1="0" y1="0" x2="0" y2="1">${c.sk.map((h,k)=>`<stop offset="${k/(c.sk.length-1)}" stop-color="${h}"/>`).join('')}</linearGradient>
  <radialGradient id="${id}r"><stop offset="0" stop-color="${c.sun}" stop-opacity=".95"/><stop offset=".3" stop-color="${c.sun}" stop-opacity=".4"/><stop offset="1" stop-color="${c.sun}" stop-opacity="0"/></radialGradient>
  <linearGradient id="${id}e" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.sea[0]}"/><stop offset="1" stop-color="${c.sea[1]}"/></linearGradient>
  <linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.gr[0]}"/><stop offset="1" stop-color="${c.gr[1]}"/></linearGradient>
  <linearGradient id="${id}h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient></defs>`;
  s+=`<rect width="1920" height="1080" fill="url(#${id}s)"/>`;
  if(c.stars)for(let k=0;k<54;k++)s+=`<circle cx="${rnd(k)*1920}" cy="${rnd(k+60)*520}" r="${1.2+rnd(k+120)*2.2}" fill="#fff" opacity="${.3+.6*Math.abs(Math.sin(t*1.3+k*1.7))}"/>`;
  const sx=c.sx-t*.8,sy=c.sy;
  if(c.lit<1||th==='sunset')s+=`<path d="M${sx} ${sy} L${sx-760} 1080 L${sx-260} 1080Z" fill="${c.sun}" opacity=".07"/><path d="M${sx} ${sy} L${sx-300} 1080 L${sx+120} 1080Z" fill="${c.sun}" opacity=".05"/>`;
  s+=`<circle cx="${sx}" cy="${sy}" r="470" fill="url(#${id}r)"/><circle cx="${sx}" cy="${sy}" r="${th==='night'?48:80}" fill="${c.sun}" opacity=".96"/>`;
  if(th==='night')s+=`<circle cx="${sx-14}" cy="${sy-10}" r="9" fill="#d9d4a8" opacity=".6"/><circle cx="${sx+16}" cy="${sy+14}" r="6" fill="#d9d4a8" opacity=".5"/>`;
  const cl=(x,y,sc,sp,op)=>`<g transform="translate(${((x+t*sp)%2500)-300},${y}) scale(${sc})" fill="${c.cl}" opacity="${op}"><ellipse cx="0" cy="8" rx="110" ry="26"/><ellipse cx="60" cy="-12" rx="70" ry="34"/><ellipse cx="-52" cy="-6" rx="56" ry="28"/><ellipse cx="10" cy="-26" rx="46" ry="26"/></g>`;
  s+=cl(300,200,1.3,11,.55)+cl(1100,130,.9,7,.5)+cl(1750,300,1.5,16,.45)+cl(700,360,.8,20,.35);
  const mt=(base,amp,ph,f1,col,op)=>{let d=`M-20 1080 L-20 ${base}`;for(let x=-20;x<=1960;x+=30){const y=base-amp*(Math.sin(x*f1+ph)+.55*Math.sin(x*f1*2.7+ph*1.7+1)+.3*Math.sin(x*f1*5+ph*.6));d+=` L${x} ${y.toFixed(1)}`}return `<path d="${d} L1960 1080Z" fill="${col}" opacity="${op}"/>`};
  s+=mt(610,80,t*.012+j,.0032,mix(c.far,c.sk[c.sk.length-1],.45),.85)+mt(670,64,t*.02+j*2+2,.0046,c.far,1)+mt(720,40,t*.03+j*3+4,.0075,c.mid,1);
  // 海（水平線・光のきらめき）
  s+=`<rect y="712" width="1920" height="${GROUND-712}" fill="url(#${id}e)"/><rect y="712" width="1920" height="10" fill="#fff" opacity=".28"/>`;
  for(let k=0;k<16;k++){const x=(k*151+t*(14+(k%4)*5))%2200-140,y=734+(k%6)*20,w=50+(k%4)*34;s+=`<rect x="${x}" y="${y}" width="${w}" height="4" rx="2" fill="${c.sun}" opacity="${.18+.16*Math.sin(t*2.4+k)}"/>`}
  // 町並み（瓦の屋根と灯り窓）
  const off=-(t*3)%2400,dark=mix(c.town,'#000000',.22);let town='';
  [0,2400].forEach(o=>TOWN.forEach(([x,w,h,k],ti)=>{const X=x+o+off;if(X>1940||X+w<-20)return;const top=GROUND+4-h;
    if(k==='house'){town+=`<rect x="${X}" y="${top}" width="${w}" height="${h}" fill="${c.town}"/><path d="M${X-16} ${top+6} L${X+w*.5} ${top-w*.4} L${X+w+16} ${top+6}Z" fill="${dark}"/><path d="M${X-16} ${top+6} L${X+w*.5} ${top-w*.4} L${X+w+16} ${top+6}Z" fill="url(#pTile)" opacity=".8"/>`;
      for(let q=0;q<2;q++){const lit=c.lit>0&&rnd(ti*7+q)<.35+c.lit*.5;town+=`<rect x="${X+w*.16+q*w*.44}" y="${top+h*.3}" width="${w*.22}" height="${Math.min(40,h*.28)}" rx="4" fill="${c.win}" opacity="${lit?.95:.55}"/>`}}
    else{town+=`<rect x="${X}" y="${top}" width="${w}" height="${h}" rx="6" fill="${c.town}"/><rect x="${X}" y="${top}" width="${w}" height="8" rx="4" fill="${dark}"/>`;
      for(let r=0;r<Math.floor((h-40)/52);r++)for(let q2=0;q2<Math.floor((w-24)/40);q2++){const lit=c.lit>0&&rnd(ti*31+r*7+q2)<.2+c.lit*.55;town+=`<rect x="${X+20+q2*40}" y="${top+26+r*52}" width="22" height="28" rx="3" fill="${c.win}" opacity="${lit?.95:.5}"/>`}}
  }));
  s+=town+`<rect y="${GROUND-60}" width="1920" height="60" fill="url(#${id}h)"/>`;
  // 木（ふたつの濃さ）
  const off2=-(t*9)%2400;let tr='';
  [0,2400].forEach(o=>TREES.forEach(([x,h,sc])=>{const X=x+o+off2;if(X>1980||X<-80)return;const sw=Math.sin(t*1.1+x)*2.5;
    tr+=`<g transform="translate(${X},${GROUND+6}) scale(${sc})"><ellipse cx="0" cy="2" rx="52" ry="9" fill="#000" opacity=".16"/><rect x="-7" y="${-h-20}" width="14" height="${h+20}" rx="5" fill="${mix(c.tree,'#000000',.35)}"/><circle cx="${sw}" cy="${-h-40}" r="46" fill="${mix(c.tree,'#000000',.12)}"/><circle cx="${-30+sw}" cy="${-h-14}" r="33" fill="${c.tree}"/><circle cx="${30+sw}" cy="${-h-18}" r="35" fill="${c.tree}"/><circle cx="${-12+sw}" cy="${-h-56}" r="20" fill="${mix(c.tree,'#ffffff',.2)}" opacity=".7"/></g>`}));
  s+=tr;
  // 地面（石だたみ・手前の影・ふち）
  s+=`<rect y="${GROUND}" width="1920" height="${1080-GROUND}" fill="url(#${id}g)"/><rect y="${GROUND}" width="1920" height="${1080-GROUND}" fill="url(#pStone)"/><rect y="${GROUND}" width="1920" height="9" fill="${mix(c.gr[0],'#ffffff',.4)}" opacity=".8"/><rect y="${GROUND+9}" width="1920" height="16" fill="#000" opacity=".1"/>`;
  [60,130,220].forEach((d,k)=>{s+=`<path d="M0 ${GROUND+d} H1920" stroke="#000" stroke-opacity="${.07-k*.01}" stroke-width="2"/>`});
  // ただよう光のつぶ
  for(let k=0;k<18;k++){const x=(rnd(k)*1920+Math.sin(t*.5+k)*36+1920)%1920,y=((rnd(k+50)*1100-t*(10+(k%5)*4))%1100+1100)%1100;s+=`<circle cx="${x}" cy="${y}" r="${2+rnd(k+90)*3.6}" fill="${c.sun}" opacity="${.22+.2*Math.sin(t*1.6+k)}"/>`}
  // 手前：街灯・植え込み・花
  const bush=(x,sc)=>`<g transform="translate(${x},${GROUND+54}) scale(${sc})"><ellipse cx="0" cy="8" rx="84" ry="12" fill="#000" opacity=".18"/><circle cx="-34" cy="-14" r="34" fill="${mix(c.tree,'#000000',.1)}"/><circle cx="14" cy="-26" r="42" fill="${c.tree}"/><circle cx="52" cy="-8" r="30" fill="${mix(c.tree,'#000000',.12)}"/><circle cx="4" cy="-40" r="20" fill="${mix(c.tree,'#ffffff',.22)}" opacity=".7"/>${[[-30,-30,T],[30,-12,Y],[0,-50,'#fff'],[56,-24,T]].map(([fx,fy,fc])=>`<circle cx="${fx}" cy="${fy}" r="6.5" fill="${fc}"/>`).join('')}</g>`;
  s+=bush(110,.9)+bush(760,.8)+bush(1250,.85)+bush(1760,.9);
  s+=lamp(470,GROUND+36,1,t,c);
  return s;
}
function lamp(x,y,s,t,c){const fl=.8+.2*Math.sin(t*7+x),on=c.lit>0?.4+c.lit*.6:.25;
  return `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="4" rx="34" ry="8" fill="#000" opacity=".22"/><rect x="-6" y="-250" width="12" height="250" rx="4" fill="#3a2a20"/><rect x="-6" y="-250" width="4" height="250" fill="#fff" opacity=".12"/><path d="M0 -246 Q30 -262 58 -246" stroke="#3a2a20" stroke-width="8" fill="none"/><circle cx="58" cy="-196" r="${90*on*fl+30}" fill="url(#glow)" opacity="${on}"/>${lantern(58,-246,1,t,x)}</g>`}
function lantern(x,y,s,t,ph=0){const sw=Math.sin(t*1.8+ph)*4,fl=.78+.22*Math.sin(t*7+ph*3);
  return `<g transform="translate(${x},${y}) scale(${s}) rotate(${sw})"><circle cx="0" cy="38" r="84" fill="url(#glow)" opacity="${.75*fl}"/><path d="M0 0 V8" stroke="#3a2a20" stroke-width="4"/><rect x="-14" y="6" width="28" height="9" rx="3" fill="#3a2a20"/><ellipse cx="0" cy="38" rx="25" ry="31" fill="#d9442f"/><ellipse cx="0" cy="38" rx="25" ry="31" fill="none" stroke="#a52f20" stroke-width="3"/><path d="M-22 28 Q0 20 22 28 M-24 40 Q0 32 24 40 M-22 52 Q0 44 22 52" stroke="#a52f20" stroke-width="2.5" fill="none"/><ellipse cx="-9" cy="26" rx="5" ry="12" fill="#fff" opacity=".3"/><rect x="-14" y="64" width="28" height="9" rx="3" fill="#3a2a20"/></g>`}

// ===== 小物 =====
const plant=(x,y,s,t=0)=>`<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="4" rx="36" ry="8" fill="#000" opacity=".18"/><path d="M-26 -44 H26 L20 0 H-20Z" fill="#a8683f"/><path d="M-26 -44 H26 L24 -34 H-24Z" fill="#c9875e"/><path d="M-20 -30 L-16 0 H-8 L-12 -30Z" fill="#fff" opacity=".12"/>${[-1,0,1].map(k=>`<path d="M${k*10} -44 Q${k*42+Math.sin(t*1.5+k)*4} -92 ${k*24} -122 Q${k*8} -86 ${k*10} -44Z" fill="${k?'#4f9a66':'#3a8558'}"/>`).join('')}</g>`;
const suitcase=(x,y,s,c='#c95a35')=>`<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="2" rx="46" ry="8" fill="#000" opacity=".2"/><path d="M-16 -64 v-14 h32 v14" stroke="#444" stroke-width="6" fill="none"/><rect x="-36" y="-64" width="72" height="56" rx="10" fill="${c}"/><rect x="-36" y="-64" width="72" height="12" rx="8" fill="#fff" opacity=".22"/><path d="M-14 -56 v44 M14 -56 v44" stroke="#000" stroke-opacity=".16" stroke-width="5"/><rect x="-6" y="-40" width="12" height="9" rx="2" fill="#f0c36a"/><circle cx="-24" cy="-6" r="6" fill="#333"/><circle cx="24" cy="-6" r="6" fill="#333"/></g>`;
const postbox=(x,y,s)=>`<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="3" rx="30" ry="7" fill="#000" opacity=".2"/><rect x="-8" y="-34" width="16" height="34" fill="#555"/><rect x="-26" y="-104" width="52" height="76" rx="14" fill="#d9442f"/><rect x="-26" y="-104" width="14" height="76" rx="8" fill="#fff" opacity=".2"/><rect x="-16" y="-86" width="32" height="7" rx="3" fill="#6f1d12"/><circle cx="0" cy="-58" r="7" fill="#f0c36a"/></g>`;
const bike=(x,y,s)=>`<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="2" rx="86" ry="8" fill="#000" opacity=".18"/><circle cx="-48" cy="-34" r="33" fill="none" stroke="#2d3a34" stroke-width="6"/><circle cx="48" cy="-34" r="33" fill="none" stroke="#2d3a34" stroke-width="6"/><circle cx="-48" cy="-34" r="4" fill="#2d3a34"/><circle cx="48" cy="-34" r="4" fill="#2d3a34"/><path d="M-48 -34 L-12 -72 L30 -72 L48 -34 M-12 -72 L6 -34 L-48 -34 M30 -72 L22 -92 M10 -92 H36 M-18 -80 H4" stroke="${T}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 -86 h26 l-4 22 h-20z" fill="#b9874f"/></g>`;
const keyp=(x,y,s,rot)=>`<g transform="translate(${x},${y}) scale(${s}) rotate(${rot})"><circle cx="-40" cy="0" r="28" fill="none" stroke="#e0a93a" stroke-width="13"/><circle cx="-40" cy="0" r="28" fill="none" stroke="#fff" stroke-width="3" opacity=".4" transform="translate(-3 -3)"/><rect x="-14" y="-7" width="96" height="14" rx="5" fill="#e0a93a"/><rect x="48" y="7" width="12" height="22" fill="#e0a93a"/><rect x="68" y="7" width="12" height="16" fill="#e0a93a"/></g>`;
const person2=(x,y,s,c1,c2)=>`<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="4" rx="26" ry="6" fill="#000" opacity=".18"/><path d="M-22 0 V-40 Q-22 -62 0 -62 Q22 -62 22 -40 V0Z" fill="${c1}"/><circle cx="0" cy="-84" r="20" fill="#f1c7a1"/><path d="M-20 -88 Q0 -112 20 -88 Q8 -98 -20 -88Z" fill="${c2}"/></g>`;

// ===== カード・見出し・ラベル =====
const bx=(x,y,w,h,rx=28,fill='url(#cardG)')=>`<rect x="${x+2}" y="${y+16}" width="${w}" height="${h}" rx="${rx}" fill="#000" opacity=".06"/><rect x="${x}" y="${y+9}" width="${w}" height="${h}" rx="${rx}" fill="#000" opacity=".09"/><rect x="${x}" y="${y+3}" width="${w}" height="${h}" rx="${rx}" fill="#000" opacity=".1"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="#fff" stroke-width="3"/><path d="M${x+rx} ${y+5} H${x+w-rx}" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".9"/>`;
const card=(x,y,w,h,inner,p)=>pop(x+w/2,y+h/2,p,bx(x,y,w,h)+inner);
function hdr(no,title,p,c=T){
  const bw=no.length>5?270:190,w=title.length*54+(no?bw+60:80);
  return fade(p,`<rect x="540" y="72" width="${w}" height="86" rx="43" fill="#000" opacity=".13"/><rect x="540" y="66" width="${w}" height="86" rx="43" fill="#fff" opacity=".96"/>${no?`<rect x="552" y="77" width="${bw}" height="64" rx="32" fill="${c}"/><text x="${552+bw/2}" y="121" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">${no}</text>`:''}<text x="${no?552+bw+22:584}" y="123" font-size="54" font-weight="900" fill="${DG}">${title}</text>`,0);
}
const tag=(x,y,txt,p,c=Y,fc=DG,fs=34)=>pop(x,y,p,`<rect x="${x-txt.length*fs*.5-24}" y="${y-fs*.88+5}" width="${txt.length*fs+48}" height="${fs*1.76}" rx="${fs*.88}" fill="#000" opacity=".13"/><rect x="${x-txt.length*fs*.5-24}" y="${y-fs*.88}" width="${txt.length*fs+48}" height="${fs*1.76}" rx="${fs*.88}" fill="${c}"/><rect x="${x-txt.length*fs*.5-10}" y="${y-fs*.88+4}" width="${txt.length*fs+20}" height="${fs*.5}" rx="${fs*.25}" fill="#fff" opacity=".2"/><text x="${x}" y="${y+fs*.36}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${fc}">${txt}</text>`);
const noteB=(txt,p)=>{const w=txt.length*28+64;return fade(p,`<rect x="${1200-w/2}" y="812" width="${w}" height="46" rx="23" fill="#1f3a2b" opacity=".85"/><text x="1200" y="845" text-anchor="middle" font-size="28" font-weight="700" fill="#fff">${txt}</text>`,0)};
function qbubble(id,txt,p,t){
  return pop(1500,215,p,`${face(id,1790,215,62,'owner',G,'worry',t,talking('Y',t))}<rect x="${1700-txt.length*30-60}" y="178" width="${txt.length*30+60}" height="86" rx="30" fill="#000" opacity=".12"/><rect x="${1700-txt.length*30-60}" y="172" width="${txt.length*30+60}" height="86" rx="30" fill="#fff" stroke="${G}" stroke-width="4"/><text x="${1700-30-txt.length*15}" y="227" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">${txt}</text>`);
}
function stampX(x,y,txt,p,c=RED,fs=72,rot=-8){return pop(x,y,p,`<g transform="rotate(${rot} ${x} ${y})"><rect x="${x-txt.length*fs*.5-34}" y="${y-fs*.8+7}" width="${txt.length*fs+68}" height="${fs*1.45}" rx="14" fill="#000" opacity=".14"/><rect x="${x-txt.length*fs*.5-34}" y="${y-fs*.8}" width="${txt.length*fs+68}" height="${fs*1.45}" rx="14" fill="#fff" fill-opacity=".94" stroke="${c}" stroke-width="10"/><text x="${x}" y="${y+fs*.33}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${c}">${txt}</text></g>`)}

// ===== 宿（木の壁・瓦の屋根・障子の灯り・暖簾・提灯・煙・看板・小物） =====
function inn(x,y,s,o){
  o=o||{};const t=o.t||0,wall=o.wall||'#f3e4c4',roof=o.roof||'#b5603a',nor=o.noren||G,lit=o.lit==null?.6:o.lit,sw=Math.sin(t*1.7)*3.5;
  const rd=mix(roof,'#000000',.28),wd=mix(wall,'#000000',.26),base=mix(wall,'#3a2a20',.58),win=mix('#e9e3cf','#ffe08a',lit);
  let h=`<g transform="translate(${x},${y}) scale(${s})">`;
  h+=`<ellipse cx="30" cy="14" rx="310" ry="26" fill="#000" opacity=".14"/><ellipse cx="10" cy="8" rx="250" ry="14" fill="#000" opacity=".14"/>`;
  h+=`<path d="M190 -290 L264 -320 L264 -26 L190 0Z" fill="${wd}"/><path d="M190 -290 L264 -320 L264 -26 L190 0Z" fill="url(#pWood)"/>`;
  h+=`<rect x="-190" y="-290" width="380" height="290" fill="${wall}"/><rect x="-190" y="-290" width="380" height="290" fill="url(#pWood)"/><rect x="-190" y="-72" width="380" height="72" fill="${base}"/><rect x="-190" y="-72" width="380" height="72" fill="url(#pWood)"/><rect x="-190" y="-76" width="380" height="6" fill="#fff" opacity=".18"/>`;
  [[-178,-212],[100,-212]].forEach(([wx,wy],k)=>{h+=(lit>.45?`<circle cx="${wx+40}" cy="${wy+44}" r="96" fill="url(#glow)" opacity="${.55*lit}"/>`:'')+`<rect x="${wx-6}" y="${wy-6}" width="92" height="98" rx="6" fill="#6b4a32"/><rect x="${wx}" y="${wy}" width="80" height="86" rx="3" fill="${win}"/><rect x="${wx}" y="${wy}" width="80" height="86" fill="url(#pShoji)"/><rect x="${wx}" y="${wy}" width="80" height="14" fill="#fff" opacity=".22"/>`});
  h+=`<rect x="-64" y="-214" width="128" height="214" rx="6" fill="#6b4a32"/><rect x="-58" y="-208" width="116" height="208" rx="3" fill="${mix('#efe6d0','#ffe08a',lit)}"/><rect x="-58" y="-208" width="116" height="208" fill="url(#pShoji)"/><path d="M0 -208 V0" stroke="#6b4a32" stroke-width="5"/>`;
  h+=`<path d="M-232 -284 L-130 -414 L130 -414 L232 -284Z" fill="${roof}"/><path d="M-232 -284 L-130 -414 L130 -414 L232 -284Z" fill="url(#pTile)"/><path d="M-130 -414 L130 -414 L146 -396 L-146 -396Z" fill="#fff" opacity=".22"/><path d="M130 -414 L206 -432 L264 -320 L232 -284Z" fill="${rd}"/><path d="M130 -414 L206 -432 L264 -320 L232 -284Z" fill="url(#pTile)" opacity=".8"/><rect x="-244" y="-292" width="488" height="16" rx="7" fill="${rd}"/><rect x="-244" y="-292" width="488" height="5" rx="3" fill="#fff" opacity=".2"/><rect x="-190" y="-276" width="380" height="20" fill="#000" opacity=".14"/>`;
  if(o.chim!==0){h+=`<rect x="64" y="-474" width="36" height="66" fill="#8a4a38"/><rect x="58" y="-482" width="48" height="12" rx="3" fill="#6f382a"/>`;for(let k=0;k<4;k++){const a=((t*.45+k/4)%1);h+=`<circle cx="${82+a*34+Math.sin(t+k)*6}" cy="${-492-a*130}" r="${12+a*26}" fill="#fff" opacity="${.55*(1-a)}"/>`}}
  // 暖簾（ゆれる）
  [[-58,-30],[-28,0],[2,30],[32,58]].forEach(([a,b],k)=>{h+=`<path d="M${a} -214 H${b} L${b+sw*(1+k*.1)} -128 H${a+sw*(1+k*.1)}Z" fill="${nor}"/><path d="M${a} -214 H${b} L${b+sw*.4} -190 H${a+sw*.4}Z" fill="#000" opacity=".16"/>`});
  h+=`<circle cx="${sw*.7}" cy="-172" r="17" fill="#fff" opacity=".92"/><path d="M${-8+sw*.7} -172 L${sw*.7} -182 L${8+sw*.7} -172 V-164 H${-8+sw*.7}Z" fill="${nor}"/>`;
  h+=lantern(-104,-286,.9,t,x*.01)+lantern(104,-286,.9,t,x*.01+2);
  if(o.sign){const fs=46,w=o.sign.length*fs+40;h+=`<rect x="${-w/2}" y="-274" width="${w}" height="60" rx="8" fill="#000" opacity=".16" transform="translate(0 5)"/><rect x="${-w/2}" y="-274" width="${w}" height="60" rx="8" fill="${o.signc||'#4a3324'}"/><rect x="${-w/2}" y="-274" width="${w}" height="60" fill="url(#pWood)"/><rect x="${-w/2+4}" y="-270" width="${w-8}" height="6" rx="3" fill="#fff" opacity=".2"/><text x="0" y="-228" text-anchor="middle" font-size="${fs}" font-weight="900" fill="#fff">${o.sign}</text>`}
  h+=plant(-210,6,.9,t)+plant(214,6,.9,t+1);
  if(o.case)h+=suitcase(-130,6,.85);
  if(o.post)h+=postbox(270,8,.85);
  if(o.bike)h+=bike(-330,8,.9);
  return h+`</g>`;
}

// ===== カレンダー（365マスを1日ずつ塗る）・シャッター・稼働率のものさし =====
const COLS=37;
function cal(x,y,cell,show,limit){
  let s='';
  for(let d=0;d<365;d++){const c=d%COLS,r=Math.floor(d/COLS),X=x+c*cell,Y=y+r*cell,cut=limit&&d>=limit;let f;
    if(d<show){f=cut?'#aab4ac':(Math.floor(d/30.42)%2?'#3d8a6a':'#2e6b47')}else f=cut?'#dfe5df':'#e4ece4';
    if(d===show-1&&show<365&&!cut)f=T;
    s+=`<rect x="${X+1.5}" y="${Y+1.5}" width="${cell-3}" height="${cell-3}" rx="${cell*.2}" fill="${f}"/>`}
  return s;
}
function shutter(x,y,cell,limit,p,label,fs){
  if(p<=0)return '';
  const r0=Math.floor(limit/COLS),c0=limit%COLS,rows=Math.ceil(365/COLS),W=COLS*cell,H=rows*cell,x0=x+c0*cell,yr=y+r0*cell;
  const d=`M${x0} ${yr} H${x+W} V${y+H} H${x} V${yr+cell} H${x0}Z`;
  return `<g opacity="${clamp(p*2)}" transform="translate(0,${-(1-eo(p))*70})"><path d="${d}" fill="#2a2f2c" opacity=".84"/><path d="${d}" fill="url(#pSlat)"/><path d="M${x0} ${yr} V${yr+cell}" stroke="${T}" stroke-width="6"/>${label?`<text x="${x+W/2}" y="${yr+cell+(H-r0*cell-cell)/2+fs*.3}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="#fff">${label}</text>`:''}</g>`;
}
const MST=[0,31,59,90,120,151,181,212,243,273,304,334,365];
function ybar(x,y,W,H,days,limit,col,o){ // 1年を1本の横棒で。limit 以降は灰色。o.months で12か月のブロックに分ける
  const px=d=>x+W*d/365,cap=limit?(o.months&&limit===180?181:limit):365;let s='';
  if(o.months){
    for(let m=0;m<12;m++){const a=MST[m],b=MST[m+1],x0=px(a)+2,w=px(b)-px(a)-4,cut=limit&&a>=cap,f=cut?0:clamp((Math.min(days,cap)-a)/(b-a));
      s+=`<rect x="${x0}" y="${y+5}" width="${w}" height="${H}" rx="12" fill="#000" opacity=".1"/><rect x="${x0}" y="${y}" width="${w}" height="${H}" rx="12" fill="${cut?'#c4ccc6':'#e6ede6'}"/>`+(f>0?`<rect x="${x0}" y="${y}" width="${w*f}" height="${H}" rx="12" fill="${col}"/><rect x="${x0+4}" y="${y+5}" width="${Math.max(0,w*f-8)}" height="${H*.22}" rx="8" fill="#fff" opacity=".22"/>`:'')+`<text x="${x0+w/2}" y="${y+H/2+o.fs*.36}" text-anchor="middle" font-size="${o.fs}" font-weight="900" fill="${f>.5?'#fff':(cut?'#66706a':DG)}">${m+1}月</text>`}
    return s}
  const r=H/2;
  s+=`<rect x="${x}" y="${y+5}" width="${W}" height="${H}" rx="${r}" fill="#000" opacity=".1"/><rect x="${x}" y="${y}" width="${W}" height="${H}" rx="${r}" fill="#e6ede6"/>`;
  if(limit)s+=`<path d="M${px(limit)} ${y} H${x+W-r} A${r} ${r} 0 0 1 ${x+W-r} ${y+H} H${px(limit)}Z" fill="#c4ccc6"/>`;
  const fw=W*Math.min(days,cap)/365;
  if(fw>0)s+=`<rect x="${x}" y="${y}" width="${fw}" height="${H}" rx="${r}" fill="${col}"/><rect x="${x+12}" y="${y+6}" width="${Math.max(0,fw-24)}" height="${H*.2}" rx="${H*.1}" fill="#fff" opacity=".22"/>`;
  return s;
}
function gauge(x,y,W,prog){ // 0〜100%のものさし。天井（約49%）と、私たちの宿（約53%）
  const f=53*prog,cx=x+W*.49;let s=`<rect x="${x}" y="${y+6}" width="${W}" height="64" rx="32" fill="#000" opacity=".08"/><rect x="${x}" y="${y}" width="${W}" height="64" rx="32" fill="#dfe8df"/>`;
  s+=`<rect x="${x}" y="${y}" width="${Math.max(0,Math.min(W*.49,W*f/100))}" height="64" rx="32" fill="url(#gG)"/>`;
  if(f>49)s+=`<rect x="${cx}" y="${y}" width="${W*(f-49)/100}" height="64" fill="url(#gO)"/>`;
  s+=`<rect x="${x+16}" y="${y+8}" width="${Math.max(0,W*f/100-32)}" height="10" rx="5" fill="#fff" opacity=".25"/>`;
  s+=`<path d="M${cx} ${y-52} V${y+92}" stroke="${RED}" stroke-width="6" stroke-dasharray="14 9"/>`;
  [[0,'0%'],[50,'50%'],[100,'100%']].forEach(([v,l])=>{s+=`<text x="${x+W*v/100}" y="${y+112}" text-anchor="middle" font-size="28" font-weight="900" fill="#4a5a52">${l}</text>`});
  s+=`<rect x="${cx-190}" y="${y-110}" width="380" height="56" rx="28" fill="${RED}"/><text x="${cx}" y="${y-72}" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">届出の上限 約49%</text>`;
  if(prog>.99){const fx=x+W*.53;s+=`<path d="M${fx} ${y+64} V${y+150}" stroke="${DG}" stroke-width="6"/><path d="M${fx} ${y+150} h500 l-26 26 l26 26 h-500z" fill="${G}"/><text x="${fx+255}" y="${y+190}" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">開業から約8.5か月の平均 約53%</text>`}
  return s;
}
const cmp=(x0,title,c,rows)=>`<rect x="${x0}" y="370" width="540" height="64" rx="32" fill="${c}"/><text x="${x0+270}" y="414" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">${title}</text>`+rows.map(([a,b,col,sym],k)=>{const y=460+k*150;return `<rect x="${x0}" y="${y}" width="540" height="124" rx="26" fill="#f3f7f1" stroke="#dfe8dc" stroke-width="3"/><text x="${x0+24}" y="${y+40}" font-size="28" font-weight="700" fill="#4a5a52">${a}</text><text x="${x0+24}" y="${y+92}" font-size="40" font-weight="900" fill="${DG}">${b}</text><circle cx="${x0+470}" cy="${y+62}" r="38" fill="${col}"/><text x="${x0+470}" y="${y+80}" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">${sym}</text>`}).join('');
const cmpCard=(p,head)=>card(600,250,1240,540,`<text x="1220" y="324" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">${head}</text>`+cmp(660,'民泊新法の届出',T,[['泊められる日数','年180日まで','#d99a2b','△'],['条件・手間','軽い（始めやすい）',G,'○']])+cmp(1240,'旅館業の許可',G,[['泊められる日数','制限なし',G,'○'],['条件・手間','重い',RED,'△']]),p);
function formulaChip(x,y,w,txt,c,fc,fs=40){return `<rect x="${x}" y="${y+6}" width="${w}" height="${fs*1.9}" rx="${fs*.95}" fill="#000" opacity=".12"/><rect x="${x}" y="${y}" width="${w}" height="${fs*1.9}" rx="${fs*.95}" fill="${c}"/><text x="${x+w/2}" y="${y+fs*1.3}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${fc}">${txt}</text>`}

// ===== 場面 =====
const cardGround=(x,y,w,h,gy,col,p)=>pop(x+w/2,y+h/2,p,`${bx(x,y,w,h)}<clipPath id="cp${x}_${y}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="28"/></clipPath><g clip-path="url(#cp${x}_${y})"><rect x="${x}" y="${gy}" width="${w}" height="${y+h-gy}" fill="${col}"/><rect x="${x}" y="${gy}" width="${w}" height="${y+h-gy}" fill="url(#pStone)"/><rect x="${x}" y="${gy}" width="${w}" height="8" fill="#000" opacity=".1"/></g>`);
const gateSmall=(x,y,t)=>`<g transform="translate(${x},${y})"><ellipse cx="0" cy="8" rx="140" ry="14" fill="#000" opacity=".18"/>${[-92,66].map(px=>`<rect x="${px}" y="-190" width="26" height="190" rx="5" fill="#8a5a3c"/><rect x="${px}" y="-190" width="26" height="190" fill="url(#pWood)"/><rect x="${px}" y="-190" width="8" height="190" fill="#fff" opacity=".14"/>`).join('')}<rect x="-112" y="-212" width="224" height="30" rx="7" fill="#6b4a32"/><rect x="-112" y="-212" width="224" height="30" fill="url(#pWood)"/><path d="M-134 -206 L0 -270 L134 -206Z" fill="#b5603a"/><path d="M-134 -206 L0 -270 L134 -206Z" fill="url(#pTile)"/><path d="M-40 -252 L0 -270 L40 -252 L40 -244 L-40 -244Z" fill="#fff" opacity=".2"/><path d="M-66 -180 H66 V0 H-66Z" fill="#c9a77c"/><path d="M-66 -180 H-2 V0 H-66Z" fill="#a8825a"/><path d="M-66 -180 H-2 V0 H-66Z" fill="url(#pWood)"/><path d="M2 -180 H66 V0 H2Z" fill="url(#pWood)"/><path d="M-66 -120 H66 M-66 -60 H66" stroke="#6b4a32" stroke-width="4"/>${lantern(-124,-206,.7,t,1)}</g>`;
const gateBig=(x,y,t)=>`<g transform="translate(${x},${y})"><ellipse cx="0" cy="8" rx="250" ry="18" fill="#000" opacity=".18"/><path d="M-230 0 L-210 -22 H210 L230 0Z" fill="#cfc6b4"/><path d="M-200 -22 L-184 -44 H184 L200 -22Z" fill="#e0d8c6"/><rect x="-196" y="-340" width="40" height="296" rx="6" fill="#8a3f2c"/><rect x="156" y="-340" width="40" height="296" rx="6" fill="#8a3f2c"/><rect x="-196" y="-340" width="12" height="296" fill="#fff" opacity=".16"/><rect x="156" y="-340" width="12" height="296" fill="#fff" opacity=".16"/><rect x="-156" y="-320" width="312" height="276" fill="#f3e6c4"/><rect x="-156" y="-320" width="312" height="276" fill="url(#pShoji)"/><rect x="-156" y="-320" width="312" height="276" fill="#ffd27a" opacity=".22"/><path d="M0 -320 V-44" stroke="#6b4a32" stroke-width="7"/><path d="M-270 -330 L-170 -430 H170 L270 -330Z" fill="#2e6b47"/><path d="M-270 -330 L-170 -430 H170 L270 -330Z" fill="url(#pTile)"/><path d="M-170 -430 H170 L186 -412 H-186Z" fill="#fff" opacity=".22"/><rect x="-284" y="-342" width="568" height="20" rx="8" fill="#1f4a32"/><rect x="-100" y="-306" width="200" height="50" rx="8" fill="#2f2a22"/><text x="0" y="-270" text-anchor="middle" font-size="34" font-weight="900" fill="#f0b35a">旅館業</text>${lantern(-226,-322,.9,t,3)}${lantern(226,-322,.9,t,5)}</g>`;
const office=(x,y,s,label,c)=>`<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="8" rx="230" ry="16" fill="#000" opacity=".18"/><rect x="-190" y="-300" width="380" height="300" fill="#f4f1e6"/><rect x="-190" y="-300" width="380" height="300" fill="url(#pStone)" opacity=".5"/><rect x="190" y="-300" width="40" height="300" fill="#d8d3c2"/><rect x="-210" y="-336" width="440" height="42" rx="8" fill="${c}"/><rect x="-210" y="-336" width="440" height="10" rx="5" fill="#fff" opacity=".25"/><rect x="-110" y="-282" width="220" height="62" rx="10" fill="${c}"/><text x="0" y="-236" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">${label}</text>${[-140,-60,60,140].map(wx=>`<rect x="${wx-24}" y="-190" width="48" height="60" rx="5" fill="#bfe0ef"/><path d="M${wx-24} -190 l22 0 l-22 30z" fill="#fff" opacity=".4"/>`).join('')}<rect x="-34" y="-110" width="68" height="110" rx="6" fill="#7a5a3c"/><rect x="-30" y="-106" width="28" height="106" fill="#bfe0ef"/><rect x="2" y="-106" width="28" height="106" fill="#bfe0ef"/><rect x="-196" y="-400" width="5" height="70" fill="#555"/><path d="M-191 -400 h60 l-12 14 l12 14 h-60z" fill="${T}"/></g>`;
const hanko=(x,y,txt,p,rot=-10,c='#d9342b')=>{if(p<=0)return '';const k=1+(1-eo(p))*.6;return `<g opacity="${clamp(p*3)}" transform="translate(${x},${y}) rotate(${rot}) scale(${k})"><circle r="62" fill="none" stroke="${c}" stroke-width="9"/><circle r="50" fill="none" stroke="${c}" stroke-width="3"/><text y="16" text-anchor="middle" font-size="46" font-weight="900" fill="${c}">${txt}</text></g>`};
const REASONS=[];
function scene(i,t,lt){
  const K=.89,L=SL[i],E=SE[i],at=(k,d=.5,o=0)=>seg(lt,L[k]+o*K,L[k]+o*K+d),on=k=>lt>=L[k];
  let s='';
  const aki=(pose,mood='happy',x=250)=>`<ellipse cx="${x+10}" cy="${GROUND+12}" rx="112" ry="17" fill="#000" opacity=".24"/>`+P(x,GROUND,.92,{c:'aki',who:'A',pose,mood},t);
  if(i===0){ // つかみ（1文ごとに画面を切り替える。「届出」「許可」は、名前を付ける文（5つめ）まで画面にも出さない）
    const pose=on(12)?'present':on(9)&&!on(10)?'think':on(8)?'point':'present';
    if(lt>L[0]-.6)s+=aki(pose,on(9)&&!on(10)?'worry':'happy');
    if(on(0)&&!on(2))s+=pop(250,205,at(0,.4),`<rect x="68" y="168" width="364" height="76" rx="38" fill="#000" opacity=".14"/><rect x="68" y="160" width="364" height="76" rx="38" fill="url(#gG)"/><text x="250" y="212" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">民泊戦略家 アキ</text>`);
    // 1 空き家と、困る人の絵
    if(on(1)&&!on(2)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(1,.4));
      s+=pop(1220,560,at(1,.5,.5),inn(1220,728,.82,{sign:'空き家',roof:'#8a8f98',noren:'#9aa59d',t,lit:.25,chim:0,case:1}));
      s+=tag(1220,330,'空き家で、宿を始めたい',at(1,.4,.9),Y,DG,46);}
    // 1 国の手続きは2つ（まだ中身は分からない）
    if(on(2)&&!on(3)){
      s+=card(640,300,1160,400,`<text x="1220" y="392" text-anchor="middle" font-size="54" font-weight="900" fill="${DG}">宿を始める、国の手続き</text><text x="1220" y="460" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">その数は…</text>`,at(2,.4));
      [[1020,'#6b756e'],[1420,'#6b756e']].forEach(([x,c],k)=>{s+=pop(x,590,at(2,.5,.9+k*.7),`<circle cx="${x}" cy="598" r="78" fill="#000" opacity=".12"/><circle cx="${x}" cy="590" r="78" fill="${c}"/><text x="${x}" y="622" text-anchor="middle" font-size="88" font-weight="900" fill="#fff">？</text>`)});}
    // 2・3 手続きの1つめ・2つめ（意味のラベルだけ。名前はまだ出さない）
    if(on(3)&&!on(6)){
      const W5=510,d2=Math.round(180*seg(lt,L[3]+.4,L[3]+3)),d3=Math.round(365*seg(lt,L[4]+.4,L[4]+3));
      const named=(k)=>fade(at(5,.4,k*.9),`<rect x="${[895,1525][k]-110}" y="318" width="220" height="62" rx="31" fill="${[T,G][k]}"/><text x="${[895,1525][k]}" y="364" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">${['届出','許可'][k]}</text>`,0);
      s+=card(600,290,590,400,`<text x="895" y="450" text-anchor="middle" font-size="54" font-weight="900" fill="${T}">半年ほどまで</text>${ybar(640,490,W5,80,d2,180,T,{})}${d2>=150?`<text x="${640+W5*180/365/2}" y="542" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">泊められる</text>`:''}<text x="${640+W5*(180+365)/2/365}" y="542" text-anchor="middle" font-size="30" font-weight="900" fill="#4a5a52">泊められない</text><text x="640" y="622" font-size="26" font-weight="900" fill="${DG}">1月</text><text x="${640+W5}" y="622" text-anchor="end" font-size="26" font-weight="900" fill="${DG}">12月</text>${named(0)}`,at(3,.4));
      s+=card(1230,290,590,400,`<text x="1525" y="450" text-anchor="middle" font-size="54" font-weight="900" fill="${G}">1年中</text>${ybar(1270,490,W5,80,d3,0,G,{})}${d3>=300?`<text x="1525" y="542" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">ずっと泊められる</text>`:''}<text x="1270" y="622" font-size="26" font-weight="900" fill="${DG}">1月</text><text x="${1270+W5}" y="622" text-anchor="end" font-size="26" font-weight="900" fill="${DG}">12月</text>${named(1)}`,at(4,.4));}
    if(on(2)&&!on(5)){
      s+=pop(1430,215,at(2,.4,.6),`${face('qa',1790,215,62,'owner',G,'worry',t,false)}<rect x="1210" y="178" width="440" height="86" rx="30" fill="#000" opacity=".12"/><rect x="1210" y="172" width="440" height="86" rx="30" fill="#fff" stroke="${G}" stroke-width="4"/><text x="1430" y="226" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">手続きが難しそう…</text>`);}
    if(on(4)&&!on(6)){
      s+=pop(935,215,at(4,.4,.3),`<rect x="640" y="178" width="470" height="86" rx="30" fill="#000" opacity=".12"/><rect x="640" y="172" width="470" height="86" rx="30" fill="#fff" stroke="${T}" stroke-width="4"/><text x="875" y="226" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">何日、泊められるの？</text>`);}
    // 5〜7 名前が付いた2つの宿。始め方・売上 → 決まる3つ → 日数のちがい
    if(on(6)&&!on(9)){
      const A=900,B=1480,by=585,d=Math.floor(365*seg(lt,L[8]+.5,L[8]+6.0)),dA=Math.min(d,180);
      s+=pop(A,by-100,at(6,.5,.1),inn(A,by,.6,{sign:'届出',roof:'#b5603a',noren:T,t,lit:.55,case:1}));
      s+=pop(B,by-100,at(6,.5,.4),inn(B,by,.68,{sign:'許可',roof:'#2e6b47',noren:G,t,lit:.85,post:1,bike:1,signc:'#2f2a22'}));
      if(on(6)&&!on(8)){s+=tag(1190,225,'許可のほうが、お得に見える？',at(6,.4,.8),Y,DG,44);if(on(7))s+=tag(1190,345,'許可には、届出にない条件がある',at(7,.4,.3),T,'#fff',40);}
      if(on(8)){
        const W0=500,endL=(x)=>fade(at(8,.4,.9),`<text x="${x}" y="800" font-size="26" font-weight="900" fill="${DG}">1月</text><text x="${x+W0}" y="800" text-anchor="end" font-size="26" font-weight="900" fill="${DG}">12月</text>`);
        s+=card(620,618,560,222,`<text x="900" y="654" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">届出：年180日まで</text>${ybar(641,690,W0,64,dA,180,T,{})}${dA>=150?`<text x="${641+W0*180/365/2}" y="732" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">180日まで</text>`:''}<g opacity="${seg(lt,L[8]+.8,L[8]+1.3)}"><text x="${641+W0*(180+365)/2/365}" y="732" text-anchor="middle" font-size="30" font-weight="900" fill="#4a5a52">営業できない</text></g>${endL(641)}`,at(8,.4,.2));
        s+=card(1200,618,560,222,`<text x="1480" y="654" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">許可：日数の上限なし</text>${ybar(1221,690,W0,64,d,0,G,{})}${d>=300?`<text x="1471" y="732" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">365日 ずっと営業できる</text>`:''}${endL(1221)}`,at(8,.4,.5));}}
    // 8 なぜ届出を選ぶのか
    if(on(9)&&!on(10)){
      s+=card(600,250,1240,540,`<text x="1220" y="330" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">あなたの空き家は、</text><text x="1220" y="400" text-anchor="middle" font-size="50" font-weight="900" fill="${T}">届出？ 許可？</text>${q(1220,600,150,t,0)}`,at(9,.4));
    }
    // 9〜10 今日話す3つ（1つずつ出す）
    if(on(10)&&!on(12)){const it=[['1','1年に何日、泊めたい？',NAVY,10,2.0],['2','家のある場所は？',NAVY,11,.3],['3','建物の条件は？',NAVY,11,1.2]];
      s+=card(640,270,1160,470,`<text x="1220" y="350" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">届出か許可か、決める3つのこと</text>`,at(10,.4));
      it.forEach(([n,w,c,li,o],k)=>{const y=440+k*120;s+=pop(1220,y,at(li,.4,o),`<rect x="720" y="${y-44}" width="1000" height="92" rx="46" fill="${c}"/><rect x="740" y="${y-38}" width="960" height="24" rx="12" fill="#fff" opacity=".18"/><circle cx="776" cy="${y}" r="34" fill="#fff"/><text x="776" y="${y+14}" text-anchor="middle" font-size="42" font-weight="900" fill="${c}">${n}</text><text x="840" y="${y+14}" font-size="40" font-weight="900" fill="#fff">${w}</text>`)});}
    // 11 はじめての人にも
    if(on(12)&&!on(13)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(12,.4));
      s+=tag(1220,330,'はじめてでも、大丈夫',at(12,.4,.3),G,'#fff',46);
      s+=pop(1220,560,at(12,.5,.8),`<g transform="translate(1220,728)">${inn(0,0,.74,{sign:'宿',t,lit:.7,case:1,post:1,chim:0})}</g>`);
      s+=sparkle(900,470,1.2,t,0)+sparkle(1540,450,1,t,2);}
    // 13 まず、民泊とは
    if(on(13)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(13,.4));
      s+=tag(1220,330,'まず、民泊とは何か',at(13,.4,.3),Y,DG,46);
      s+=pop(1380,560,at(13,.5,.8),inn(1380,728,.72,{sign:'宿',t,lit:.7,case:1,post:1}));
      s+=pop(840,600,at(13,.5,1.4),`<g transform="translate(840,590)"><ellipse cx="0" cy="130" rx="90" ry="12" fill="#000" opacity=".15"/>${coin(-30,100,52)}${coin(40,60,44)}${coin(-4,20,40)}</g>`);}
    // オープニング（動画の頭の約3.5秒）：緑の幕が入る → ロゴ → 「アキヤド 民泊school」（呼び込みの声）→ はける
    {const q0=lt,D=L[0]-.3;if(q0<D){
      const out=seg(q0,D-.45,D),wipe=eo(seg(q0,0,.45));
      let o=`<g opacity="${1-out}"><rect width="${1920*wipe}" height="1080" fill="${G}"/>`;
      for(let k=0;k<12;k++){const x=((k*220+q0*260)%2600)-400;o+=`<path d="M${x} 1080 L${x+500} 0" stroke="#fff" stroke-width="40" opacity="${.06*wipe}"/>`}
      o+=`<rect x="0" y="0" width="${1920*eo(seg(q0,.15,.6))}" height="22" fill="${T}"/><rect x="${1920*(1-eo(seg(q0,.15,.6)))}" y="1058" width="1920" height="22" fill="${Y}"/>`;
      o+=pop(960,400,seg(q0,.35,.85),`<circle cx="960" cy="400" r="120" fill="#fff"/>${MARK(960,400,2.6)}`);
      o+=pop(960,640,seg(q0,.9,1.3),`<g transform="rotate(-3 960 640)"><rect x="500" y="575" width="920" height="130" rx="65" fill="#fff"/><text x="960" y="665" text-anchor="middle" font-size="74" font-weight="900" fill="${G}" letter-spacing="2">アキヤド <tspan fill="${T}">民泊school</tspan></text></g>`);
      [[220,180],[1700,200],[160,560],[1760,600],[300,920],[1620,940]].forEach(([x,y],k)=>{o+=`<g opacity="${wipe}">${sparkle(x,y,1,lt,k)}</g>`});
      s+=o+`</g>`;}}
  }
  if(i===1){ // 手続きの入口
    s+=aki(on(9)&&!on(10)?'think':(on(5)&&!on(6)?'point':'present'),on(9)&&!on(10)?'worry':'happy');
    const gatesScene=p=>{let g=cardGround(580,250,1260,570,708,'#cfe0c8',p);
      const rf=1-.65*seg(lt,L[3]+3,L[3]+3.6)*(1-seg(lt,L[5],L[5]+.3));
      g+=pop(900,640,at(3,.5,.3),gateSmall(900,720,t))+tag(900,780,'届出  民泊新法',at(3,.4,.9),T,'#fff',34);
      g+=`<g opacity="${rf}">`+pop(1450,640,at(3,.5,.5),gateBig(1450,720,t))+tag(1450,780,'許可  旅館業',at(3,.4,1.5),G,'#fff',34)+`</g>`;
      if(on(3)&&!on(5)&&lt<L[5]-.2&&on(3)&&!on(8))g+=tag(900,330,'役所に知らせる',at(3,.4,2.6),NAVY,'#fff',44);
      g+=plant(680,735,.9,t)+plant(1790,735,.9,t+1);
      return g};
    if(on(0)&&!on(3)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(0,.4));
      s+=fade(at(0,.5,.3),`<text x="1210" y="336" text-anchor="middle" font-size="48" font-weight="900" fill="${DG}">お金をもらって、人を泊める</text>`);
      s+=pop(1380,520,at(0,.5,.6),inn(1380,728,.72,{sign:'宿',t,lit:.7,case:1,post:1,bike:1}));
      s+=pop(780,560,at(1,.5,.3),`<g transform="translate(780,560)"><ellipse cx="0" cy="130" rx="90" ry="12" fill="#000" opacity=".15"/>${coin(-30,100,52)}${coin(40,60,44)}${coin(-4,20,40)}${coin(46,128,38)}</g>`);
      s+=fade(at(1,.4,1.5),`<path d="M880 560 H1060" stroke="${T}" stroke-width="14" stroke-linecap="round" stroke-dasharray="26 16" stroke-dashoffset="${-t*40}"/><path d="M1060 530 L1110 560 L1060 590Z" fill="${T}"/>`);
      s+=stampX(1000,410,'お金をもらうなら、手続きが必要',at(2,.3,.4),RED,40,-5);
      for(let c=0;c<3;c++){const f=((t*.5+c/3)%1);s+=`<g opacity="${Math.sin(f*Math.PI)}">${sparkle(1000+c*120,470-f*60,.7,t,c)}</g>`}
    }
    if(on(3)&&!on(4))s+=gatesScene(1);
    if(on(4)&&!on(5)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(4,.4));
      s+=fade(at(4,.5,.2),`<text x="1210" y="336" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">旅館業法の許可：保健所の許可をもらう</text>`);
      s+=pop(880,560,at(4,.5,.5),inn(880,728,.62,{sign:'許可',t,lit:.7,case:1}));
      s+=pop(1450,560,at(4,.5,2.4),office(1450,728,.78,'保健所',G));
      s+=fade(at(4,.4,3.4),`<path d="M1130 560 H1210" stroke="${T}" stroke-width="12" stroke-linecap="round" stroke-dasharray="22 14" stroke-dashoffset="${-t*40}"/>`);
      s+=hanko(1120,470,'許可',seg(lt,L[4]+(5.4*K),L[4]+(5.4*K)+.35));}
    if(on(5))s+=gatesScene(1);
    if(on(5))s+=tag(1220,330,'大きな違いは、泊められる日数',at(5,.4,.4),Y,DG,44);
  }
  if(i===2){ // 違い① 泊められる日数
    s+=aki(on(11)&&!on(12)?'think':(on(5)&&!on(6)?'point':'present'),on(11)&&!on(12)?'worry':'happy');
    s+=hdr('決める3つ','泊められる日数',at(0,.4),NAVY);
    if(on(2)&&!on(5)){
      const rows=[['届出',180,T,'年180日まで','#b5603a'],['許可',365,G,'日数の上限なし','#2e6b47']];
      s+=card(600,250,1240,560,'',at(2,.4));
      rows.forEach(([w,v,c,l,rc],k)=>{const y=470+k*190,g=eo(at(2,1.1,.4+k*1.2));
        s+=`<g opacity="${at(2,.3,.3+k*1.2)}">${inn(720,y+60,.34,{sign:'',roof:rc,noren:c,t,lit:.6,chim:0})}<text x="885" y="${y-2}" text-anchor="middle" font-size="32" font-weight="900" fill="${c}">${k?'旅館業':'民泊新法'}</text><text x="885" y="${y+34}" text-anchor="middle" font-size="30" font-weight="900" fill="${c}">（${w}）</text><rect x="960" y="${y-34}" width="800" height="68" rx="34" fill="#e3ebe3"/><rect x="960" y="${y-34}" width="${800*v/365*g}" height="68" rx="34" fill="${k?'url(#gG)':'url(#gO)'}"/><rect x="976" y="${y-26}" width="${Math.max(0,800*v/365*g-32)}" height="12" rx="6" fill="#fff" opacity=".26"/>${g>.9?`<text x="${960+800*v/365-30}" y="${y+14}" text-anchor="end" font-size="38" font-weight="900" fill="#fff">${l}</text>`:''}</g>`});}
    if(on(1)&&!on(2)){
      const days=Math.round(180*seg(lt,L[1]+.3*K,L[1]+3.6*K)),X0=670,W2=1100,BY=450,BH=110,lx=X0+W2*181/365;
      s+=card(600,250,1240,545,`<text x="1220" y="320" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">1年（12か月）</text>${ybar(X0,BY,W2,BH,days,180,T,{months:1,fs:28})}`,at(1,.4));
      s+=fade(at(1,.4,3.3),`<path d="M${lx} 395 V${BY}" stroke="${T}" stroke-width="6"/><rect x="${lx-75}" y="345" width="150" height="54" rx="27" fill="${T}"/><text x="${lx}" y="384" text-anchor="middle" font-size="36" font-weight="900" fill="#fff">180日</text>`);
      s+=fade(at(1,.4,3.6),`<rect x="${X0+W2*181/365/2-290}" y="585" width="580" height="62" rx="31" fill="${T}"/><text x="${X0+W2*181/365/2}" y="629" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">泊められる 180日（約半分）</text><rect x="${(lx+X0+W2)/2-235}" y="585" width="470" height="62" rx="31" fill="#6b756e"/><text x="${(lx+X0+W2)/2}" y="629" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">ここから先は営業できない</text>`);
      s+=fade(at(1,.4,4.6),`<rect x="620" y="672" width="720" height="84" rx="42" fill="url(#gO)"/><text x="980" y="730" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">180日 ÷ 365日 ＝ 約49%</text>`);
      s+=tag(1600,714,'1年の約半分',at(1,.4,5.2),Y,DG,40);
      s+=noteB('※地域のルールで、さらに短いこともあります',at(1,.4,6));}
    if(on(3)&&!on(4))s+=tag(1220,300,'地域のルールで、さらに短いことも',at(3,.4,.3),'#8a5a3c','#fff',36);
    if(on(4)&&!on(5))s+=tag(1220,300,'多い？ 少ない？ → お客さんの入り方で決まる',at(4,.4,.3),NAVY,'#fff',34);
    if(on(5)&&!on(6)){
      const nights=[1,2,3,8,9,10,15,16,17,22,23,24,29,30];
      s+=card(600,250,1240,545,`<text x="1220" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">稼働率 ＝ 泊まった日 ÷ 全部の日</text>`,at(5,.4));
      s+=pop(880,560,at(5,.5,.5),`<g transform="translate(740,400)">${box(0,0,300,300,24)}<rect x="0" y="0" width="300" height="52" rx="24" fill="${T}"/><text x="150" y="38" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">ある月</text>${Array.from({length:35},(_,d)=>{const c=d%7,r=Math.floor(d/7),on1=nights.includes(d+1)&&d<30,x=16+c*38,y=70+r*44;return `<rect x="${x}" y="${y}" width="32" height="36" rx="7" fill="${on1?(at(5,.3,1+ (d%7)*.3)>0?T:'#e4ece4'):'#e4ece4'}"/>`}).join('')}</g>`);
      s+=fade(at(5,.5,2.2),`<text x="1180" y="510" font-size="46" font-weight="900" fill="${T}">泊まった日（オレンジ）</text><text x="1180" y="582" font-size="46" font-weight="900" fill="${DG}">÷ その月の日数</text><text x="1180" y="654" font-size="46" font-weight="900" fill="${G}">＝ 稼働率</text>`);}
    if(on(6)&&!on(7)){
      const months=['1','2','3','4','5','6','7','8','9','10','11','12'];
      const rowsM=[['ゆっくりの宿',0.5,G],['混む宿・1年中の宿',1.0,T]];
      s+=card(600,250,1240,560,`<text x="1220" y="312" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">使った日数が、180日に近づくスピード</text>`,at(6,.4));
      rowsM.forEach(([w,sp,c],k)=>{const y=420+k*190,g=seg(lt,L[6]+(1+k*.4)*K,L[6]+(5+k*.4)*K);const limitM=sp>.9?8.2:12;const fillM=Math.min(g*12,limitM),done=sp>.9&&fillM>=limitM;
        let r=`<text x="680" y="${y-46}" font-size="34" font-weight="900" fill="${DG}">${w}</text>`;
        months.forEach((m,mi)=>{const x=680+mi*90,f=(sp>.9?1:.5)*clamp(fillM-mi),cut=mi+1>limitM&&done;r+=`<rect x="${x}" y="${y-30}" width="82" height="72" rx="10" fill="${cut?'#c4ccc6':'#e4ece4'}"/>${f>0&&!cut?`<rect x="${x}" y="${y-30+72*(1-f)}" width="82" height="${72*f}" rx="10" fill="${c}"/>`:''}<text x="${x+41}" y="${y+78}" text-anchor="middle" font-size="26" font-weight="900" fill="#4a5a52">${m}月</text>`});
        s+=r;
        if(k===1&&done)s+=pop(1220,y+120,seg(lt,L[6]+5.8*K,L[6]+6.3*K),`<rect x="900" y="${y+96}" width="640" height="56" rx="28" fill="${RED}"/><text x="1220" y="${y+136}" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">180日に着いたら、そこで終わり</text>`)});
      s+=stampX(1690,775,'イメージ',at(6,.3,.6),'#8a8f98',34,6);}
    if(on(7)&&!on(8)){const g=eo(at(7,6,.9));
      s+=card(600,250,1240,540,`<text x="1220" y="335" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">私たちの宿：開業から約8.5か月の平均</text>${gauge(700,480,1040,g)}`,at(7,.4));
      s+=tag(930,740,'静岡県 下田の宿',at(7,.4,.5),NAVY,'#fff',40);s+=tag(1480,740,'稼働率は 約53%',at(7,.4,8.2),Y,DG,40);
      if(g>.99)s+=sparkle(1320,500,1.1,t,0)+sparkle(1500,470,.8,t,3);}
    if(on(8)&&!on(9)){
      s+=card(600,250,1240,540,`<text x="1220" y="330" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">このペースで1年続くと</text><text x="1220" y="470" text-anchor="middle" font-size="76" font-weight="900" fill="${DG}">365日 × 0.53</text><text x="1220" y="590" text-anchor="middle" font-size="110" font-weight="900" fill="${T}">＝ 約193日</text>`,at(8,.4));
      s+=pop(1220,700,at(8,.5,3.6),`<rect x="800" y="652" width="840" height="84" rx="42" fill="${RED}"/><text x="1220" y="710" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">届出の上限 180日を、超える</text>`);}
    if(on(9)&&!on(10)){
      s+=card(600,250,1240,540,`<text x="1220" y="335" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">稼働率 約53%は、開業から約8.5か月の平均</text><text x="1220" y="470" text-anchor="middle" font-size="84" font-weight="900" fill="${T}">これは、一例</text><text x="1220" y="600" text-anchor="middle" font-size="58" font-weight="900" fill="${DG}">手間と初期投資は含まない</text>`,at(9,.4));
      s+=stampX(1560,705,'一例',at(9,.3,.6),T,44,6);}
    if(on(10)&&!on(11)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(10,.4));
      s+=pop(1000,560,at(10,.5,.4),inn(1000,728,.74,{sign:'許可',roof:'#2e6b47',noren:G,t,lit:.85,case:1,post:1,signc:'#2f2a22'}));
      const rot=-40+Math.min(1,seg(lt,L[10]+2.6*K,L[10]+3.4*K))*90;
      s+=pop(1560,520,at(10,.5,1.6),`<g transform="translate(1560,520)"><circle r="104" fill="#000" opacity=".1" transform="translate(5,8)"/><circle r="104" fill="url(#gD)"/><circle r="84" fill="#e8ece6"/><circle r="84" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/><circle r="22" fill="#2a2f2c"/><rect x="-6" y="0" width="12" height="40" rx="5" fill="#2a2f2c"/>${keyp(0,0,.85,rot)}</g>`);
      s+=tag(1560,690,'1年中、営業',at(10,.4,4.2),G,'#fff',38);
      s+=tag(1200,330,'最初から通年営業のつもりで、許可を選んだ',at(10,.4,6),Y,DG,40);}
    if(on(12)&&!on(13)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(12,.4));
      s+=pop(880,560,at(12,.5,.3),inn(880,728,.66,{sign:'届出',noren:T,t,lit:.65,case:1}));
      s+=fade(at(12,.5,.8),`<text x="1420" y="400" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">ときどき使う家</text><text x="1420" y="470" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">まず小さく試す</text>`);
      s+=pop(1420,590,at(12,.5,3.2),`<rect x="1150" y="540" width="540" height="100" rx="50" fill="url(#gG)"/><text x="1420" y="606" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">上限は気にならない</text>`);
      s+=sparkle(1600,420,1,t,0);}
    if(on(11)&&!on(12)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(11,.4));
      s+=pop(860,560,at(11,.5,.3),inn(860,728,.6,{sign:'届出',noren:T,t,lit:.65,case:1}));
      s+=pop(1440,560,at(11,.5,.8),inn(1440,728,.68,{sign:'許可',t,lit:.85,roof:'#2e6b47',noren:G,post:1,signc:'#2f2a22'}));
      s+=q(1150,540,130,t,0);
      s+=tag(1150,330,'自分の宿は、どっち？',at(11,.4,1.6),Y,DG,44);}
    if(on(11)&&!on(12))s+=qbubble('q6','届出でもいいの？',at(11,.4),t);
    if(on(13)){
      s+=card(620,250,1200,540,`<text x="1220" y="322" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">日数だけなら、許可が有利</text>`,at(13,.4));
      s+=pop(1220,470,at(13,.5,.5),`<rect x="720" y="400" width="1000" height="110" rx="55" fill="url(#gG)"/><text x="1220" y="474" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">許可：1年中 ／ 届出：180日まで</text>`);
      s+=pop(1220,600,at(13,.5,3.6),`<rect x="720" y="545" width="1000" height="110" rx="55" fill="${RED}"/><text x="1220" y="619" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">届出は、180日まで</text>`);
      s+=pop(1220,720,at(13,.5,6.6),`<rect x="720" y="680" width="1000" height="90" rx="45" fill="${NAVY}"/><text x="1220" y="742" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">日数が多いほど、許可が向く</text>`);}
  }
  if(i===3){ // 違い② 手続きと建物
    s+=aki(on(2)&&!on(3)?'think':(on(4)?'point':'present'),on(2)&&!on(3)?'worry':'happy');
    s+=hdr('決める3つ','場所と建物',at(0,.4),NAVY);
    const tileP=(x,y,w,h,p,inner,label,ck)=>pop(x+w/2,y+h/2,p,`${bx(x,y,w,h,22)}${inner}<text x="${x+w/2}" y="${y+h-24}" text-anchor="middle" font-size="${label.length>5?30:34}" font-weight="900" fill="${DG}">${label}</text>${ck>0?`<g transform="translate(${x+w-34},${y+34}) scale(${.5+.5*eo(ck)})"><circle r="26" fill="${G}"/><path d="M-12 0 l9 10 l17 -20" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`:''}`);
    const PIC={
      kitchen:(cx,cy)=>`<g transform="translate(${cx},${cy})"><rect x="-36" y="-6" width="72" height="42" rx="9" fill="#8a8f98"/><rect x="-42" y="-12" width="84" height="11" rx="5" fill="#b3b9c1"/><path d="M-46 10 h-14 M46 10 h14" stroke="#8a8f98" stroke-width="8" stroke-linecap="round"/>${[-14,0,14].map((o,k)=>`<path d="M${o} -24 q-9 -14 0 -28" stroke="#9aa59d" stroke-width="5" fill="none" stroke-linecap="round" opacity="${.5+.4*Math.sin(t*3+k)}"/>`).join('')}</g>`,
      bath:(cx,cy)=>`<g transform="translate(${cx},${cy})"><rect x="-52" y="-4" width="104" height="44" rx="16" fill="#bfe0ef"/><rect x="-52" y="-4" width="104" height="12" rx="6" fill="#fff" opacity=".5"/><path d="M-32 22 q8 -8 16 0 t16 0 t16 0 t16 0" stroke="#7fb8d6" stroke-width="5" fill="none"/>${[[-20,-22],[10,-34],[30,-18]].map(([bx0,by0],k)=>`<circle cx="${bx0}" cy="${by0-((t*20+k*10)%16)}" r="${6+k}" fill="#fff" stroke="#bfe0ef" stroke-width="3"/>`).join('')}</g>`,
      toilet:(cx,cy)=>`<g transform="translate(${cx},${cy})"><rect x="-18" y="-40" width="36" height="32" rx="8" fill="#fff" stroke="#c4cbc6" stroke-width="3"/><ellipse cx="0" cy="14" rx="34" ry="20" fill="#fff" stroke="#c4cbc6" stroke-width="3"/><ellipse cx="0" cy="12" rx="20" ry="9" fill="#dfe8ee"/><rect x="-12" y="30" width="24" height="12" rx="4" fill="#e6ebe8"/></g>`,
      sink:(cx,cy)=>`<g transform="translate(${cx},${cy})"><path d="M-44 0 h88 q0 36 -44 36 q-44 0 -44 -36z" fill="#fff" stroke="#c4cbc6" stroke-width="3"/><path d="M0 -4 v-30 h22 v10" stroke="#9aa59d" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="22" cy="-8" r="${3+((t*8)%6)}" fill="#8fd0f0" opacity=".8"/></g>`,
      plan:(cx,cy)=>`<g transform="translate(${cx},${cy}) rotate(-4)"><rect x="-48" y="-40" width="96" height="76" rx="6" fill="#3d6a8a"/><path d="M-36 -26 h40 v26 h-40z M4 -26 h32 M-36 20 h72 M10 -4 v24" stroke="#fff" stroke-width="3" fill="none" opacity=".85"/><rect x="-48" y="-40" width="96" height="14" fill="#fff" opacity=".15"/></g>`,
      alarm:(cx,cy)=>`<g transform="translate(${cx},${cy})"><circle r="40" fill="#f2f2ee" stroke="#c9c9c2" stroke-width="4"/><circle r="26" fill="#e4e4de"/><circle r="9" fill="#bbb"/><circle cx="0" cy="-26" r="6" fill="#e53935" opacity="${.35+.65*Math.abs(Math.sin(t*4))}"/>${[0,1,2,3].map(k=>`<path d="M${Math.cos(k*1.57+.8)*14} ${Math.sin(k*1.57+.8)*14} L${Math.cos(k*1.57+.8)*24} ${Math.sin(k*1.57+.8)*24}" stroke="#aaa" stroke-width="4"/>`).join('')}</g>`,
      exit:(cx,cy)=>`<g transform="translate(${cx},${cy})"><rect x="-52" y="-34" width="104" height="68" rx="9" fill="#2f9a5a"/><rect x="-52" y="-34" width="104" height="14" rx="7" fill="#fff" opacity=".22"/><circle cx="-8" cy="-14" r="8" fill="#fff"/><path d="M-8 -4 l-16 22 M-8 -4 l14 12 l16 -6 M-4 8 l-4 22 M-4 8 l18 18" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M30 -2 h14 m-6 -8 l8 8 l-8 8" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/></g>`,
      stampP:(cx,cy)=>hanko(cx,cy,'確認',1,-8,'#d9342b'),
    };
    if(on(9)&&!on(10)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(9,.4));
      s+=pop(830,560,at(9,.5,.3),inn(850,728,.7,{sign:'住宅',t,lit:.7,case:1}));
      [['台所','kitchen'],['浴室','bath'],['トイレ','toilet'],['洗面','sink']].forEach(([w,pc],k)=>{const x=1130+(k%2)*350,y=330+Math.floor(k/2)*220,o=[2.6,3.8,5,6.2][k];
        s+=tileP(x,y,320,190,at(9,.4,o*.9),PIC[pc](x+160,y+70),w,at(9,.3,o*.9+.5))});
      }
    if(on(4)&&!on(6)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(4,.4));
      s+=pop(830,560,at(4,.5,.3),inn(830,728,.7,{sign:'許可',t,lit:.8,roof:'#2e6b47',noren:G,signc:'#2f2a22'}));
      [['図面','plan'],['火災報知器','alarm'],['誘導灯','exit'],['保健所の確認','stampP']].forEach(([w,pc],k)=>{const x=1130+(k%2)*350,y=330+Math.floor(k/2)*220,o=[2.2,3.4,5,7.2][k];
        s+=tileP(x,y,320,190,at(4,.4,o*.9),PIC[pc](x+160,y+66),w,0)});}
    if(on(6)&&!on(7)){
      s+=card(600,250,1240,550,`<text x="1000" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">広さの目安（1人あたり）</text>`,at(6,.4));
      [0,1,2,3].forEach(k=>{const x=700+k*150;s+=pop(x+68,470,at(6,.4,.8+k*.5),`<rect x="${x}" y="400" width="136" height="136" rx="10" fill="#cfe3a8"/><rect x="${x}" y="400" width="136" height="136" rx="10" fill="url(#pTatami)"/><rect x="${x}" y="400" width="136" height="136" rx="10" fill="none" stroke="#6f8a3c" stroke-width="5"/>${person2(x+68,532,.8,[G,T,'#3d6a8a','#b8862f'][k],'#2b2422')}<text x="${x+68}" y="430" text-anchor="middle" font-size="28" font-weight="900" fill="${DG}">3.3㎡</text>`)});
      s+=fade(at(6,.5,4.6),`<path d="M700 566 v14 h586 v-14" stroke="${T}" stroke-width="7" fill="none" stroke-linecap="round"/><text x="993" y="650" text-anchor="middle" font-size="62" font-weight="900" fill="${T}">4人 ＝ 13.2㎡</text>`);
      s+=pop(1560,440,at(6,.4,.4),formulaChip(1340,390,440,'10人未満：1人 3.3㎡',G,'#fff',30));
      s+=pop(1560,560,at(6,.4,2.2),formulaChip(1340,510,440,'10人以上：33㎡以上',T,'#fff',30));
      }
    if(on(1)&&!on(4)){
      const rowP=(y,name,c,sym,sc,txt,o)=>pop(1510,y,at(1,.4,o<3?.9:1.3),`<rect x="1220" y="${y-52}" width="560" height="120" rx="30" fill="#f3f7f1" stroke="#dfe8dc" stroke-width="3"/><rect x="1236" y="${y-36}" width="170" height="52" rx="26" fill="${c}"/><text x="1321" y="${y}" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">${name}</text>`)+fade(at(1,.4,o),`<circle cx="1700" cy="${y+8}" r="42" fill="${sc}"/><text x="1700" y="${y+30}" text-anchor="middle" font-size="64" font-weight="900" fill="#fff">${sym}</text><text x="1300" y="${y+50}" font-size="28" font-weight="900" fill="${DG}">${txt}</text>`,0);
      s+=card(600,250,1240,550,`<rect x="660" y="320" width="520" height="420" rx="22" fill="#e9efe4"/><rect x="660" y="320" width="270" height="420" rx="22" fill="url(#pHatch)"/><rect x="660" y="320" width="270" height="420" rx="22" fill="none" stroke="${G}" stroke-width="5" stroke-dasharray="14 9"/><path d="M930 320 V740 M660 530 H1180" stroke="#cfd8cb" stroke-width="22"/>${[[960,350],[1040,350],[1110,350],[960,570],[1040,570],[1110,570],[960,650],[1110,650]].map(([bx0,by0],k)=>`<rect x="${bx0}" y="${by0}" width="52" height="${k<3?70:60}" rx="6" fill="${['#e7b36a','#d98a6a','#9fc4d8'][k%3]}"/>`).join('')}<rect x="690" y="340" width="210" height="46" rx="23" fill="${G}"/><text x="795" y="373" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">住居専用地域</text><g transform="translate(795,520)"><path d="M-44 0 L0 -40 L44 0 V40 H-44Z" fill="${T}"/><rect x="-12" y="8" width="24" height="32" fill="#fff"/></g>${rowP(420,'届出',T,'△','#d99a2b','制限つきで可能',2.4)}${rowP(610,'許可',G,'×',RED,'原則、営業できない',5.8)}`,at(1,.4));
      if(on(2)&&!on(3))s+=tag(1220,286,'空き家が、そこにあったら？',at(2,.4,.3),NAVY,'#fff',38);
      if(on(3))s+=tag(1220,286,'許可は、原則、取れない',at(3,.4,.3),RED,'#fff',38);
      if(on(2))s+=qbubble('q3','許可は難しいのか…',at(2,.4),t);}
    if(on(7)&&!on(9)){
      s+=card(600,250,1240,550,`<path d="M740 430 H1670" stroke="#cfd8cb" stroke-width="12" stroke-linecap="round"/><path d="M740 430 H${740+930*eo(at(7,6,.6))}" stroke="${G}" stroke-width="12" stroke-linecap="round"/>`,at(7,.4));
      [['開業の2か月前','保健所・消防署に相談'],['自分で申請','書類をそろえる'],['1〜2か月','申請から許可まで'],['許可番号','予約を受けられる']].forEach(([a,b],k)=>{const x=740+k*310,o=[.8,3.4,6.0,9.0][k];
        s+=pop(x,430,at(7,.4,o),`<circle cx="${x}" cy="436" r="34" fill="#000" opacity=".12"/><circle cx="${x}" cy="430" r="34" fill="${[G,'#3d8a6a',Y,T][k]}"/><circle cx="${x}" cy="430" r="11" fill="${k==2?DG:'#fff'}"/><text x="${x}" y="510" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">${a}</text><text x="${x}" y="552" text-anchor="middle" font-size="26" font-weight="700" fill="#4a5a52">${b}</text>`)});
      s+=pop(1250,670,at(7,.5,9.4),`<rect x="840" y="590" width="820" height="170" rx="26" fill="#000" opacity=".08" transform="translate(0 6)"/><rect x="840" y="590" width="820" height="170" rx="26" fill="#fff" stroke="#e1e8df" stroke-width="3"/><text x="880" y="640" font-size="36" font-weight="900" fill="#ff5a5f">Airbnb</text><rect x="880" y="660" width="420" height="60" rx="12" fill="#eef3ee"/><text x="900" y="702" font-size="30" font-weight="700" fill="#4a5a52">許可番号：●●●●●●</text><g transform="translate(1330,690)"><circle r="22" fill="${G}"/><path d="M-10 0 l8 9 l14 -18" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g><rect x="1410" y="650" width="210" height="64" rx="32" fill="url(#gO)"/><text x="1515" y="692" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">予約OK</text>`);
      s+=noteB('※許可番号の件は、私たちの1件の経験です',at(8,.4,.5));}
    if(on(10)){
      s+=card(600,250,1240,550,`<text x="1220" y="336" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">許可は、日数に強い。でも、条件が重い</text>`,at(10,.4));
      s+=pop(1220,480,at(10,.5,.8),`<rect x="760" y="410" width="920" height="100" rx="50" fill="url(#gG)"/><text x="1220" y="478" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">日数：1年中、泊められる</text>`);
      s+=pop(1220,620,at(10,.5,2.6),`<rect x="760" y="550" width="920" height="100" rx="50" fill="${RED}"/><text x="1220" y="618" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">場所と建物：条件が重い</text>`);
    }
  }
  if(i===4){ // 違い③ 向く人は誰か
    s+=aki(on(12)?'present':(on(7)&&!on(8)?'think':'point'),on(7)&&!on(8)?'worry':'happy');
    s+=hdr('','自分は、どちら？',at(0,.4),NAVY);
    if(on(1)&&!on(3)){
      const hl=on(2)?2:1,x0=580,y0=250,w=1280,h=570,sway=Math.sin(t*1.2)*3;
      let g=pop(1220,535,at(1,.5),`${bx(x0,y0,w,h)}<defs><linearGradient id="fkS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe3f3"/><stop offset=".6" stop-color="#fdf1d6"/></linearGradient></defs><clipPath id="fk"><rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="28"/></clipPath><g clip-path="url(#fk)"><rect x="${x0}" y="${y0}" width="${w}" height="${h}" fill="url(#fkS)"/>
        <circle cx="1560" cy="340" r="52" fill="#fff6c9" opacity=".95"/><path d="M${x0} 560 Q760 440 980 540 Q1160 460 1340 540 Q1560 450 1860 540 V820 H${x0}Z" fill="#b9dcc0"/><path d="M${x0} 620 Q800 540 1000 610 Q1200 540 1400 610 Q1640 540 1860 600 V820 H${x0}Z" fill="#a6d0a8"/><rect x="${x0}" y="640" width="${w}" height="180" fill="#9ac79a"/>
        <g opacity=".75" transform="translate(${((t*8)%1500)+600},300)" fill="#fff"><ellipse rx="80" ry="22"/><ellipse cx="46" cy="-14" rx="52" ry="26"/></g>
        <path d="M1110 820 L1280 820 L1520 590 L1440 590 L1195 760 L930 590 L860 590Z" fill="#d8c7a0"/><path d="M1110 820 L1280 820 L1195 735Z" fill="#d8c7a0"/><path d="M1125 820 L1195 756 L1265 820" stroke="#fff" stroke-width="5" fill="none" opacity=".6"/>
        <path d="M1195 815 V785 L1120 755 L895 590 M1195 785 L1270 755 L1480 590" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="20 18" stroke-dashoffset="${-t*30}" opacity=".7"/>
        <g transform="translate(790,560)"><ellipse cx="0" cy="12" rx="70" ry="10" fill="#000" opacity=".16"/><rect x="-6" y="-70" width="12" height="80" rx="4" fill="#7a5a3c"/><circle cx="${sway}" cy="-100" r="46" fill="#f4b6c9"/><circle cx="${-30+sway}" cy="-76" r="32" fill="#f7c8d6"/><circle cx="${30+sway}" cy="-80" r="34" fill="#f09ab5"/>${[0,1,2,3].map(k=>`<circle cx="${((k*57+t*30)%120)-60}" cy="${((k*41+t*40)%100)-20}" r="4" fill="#f9d3df" opacity=".8"/>`).join('')}</g>
        <g transform="translate(1590,560)"><ellipse cx="0" cy="12" rx="70" ry="10" fill="#000" opacity=".16"/><rect x="-6" y="-70" width="12" height="80" rx="4" fill="#7a5a3c"/><circle cx="${sway}" cy="-100" r="46" fill="#e0693a"/><circle cx="${-30+sway}" cy="-76" r="32" fill="#e9893f"/><circle cx="${30+sway}" cy="-80" r="34" fill="#cf4b2f"/></g>
        ${inn(880,600,.2,{sign:'',t,lit:.6,chim:0,roof:'#b5603a',noren:T})}${inn(1510,600,.26,{sign:'',t,lit:.9,roof:'#2e6b47',noren:G})}
        <g transform="translate(1195,740)"><ellipse cx="0" cy="8" rx="46" ry="8" fill="#000" opacity=".2"/><rect x="-7" y="-150" width="14" height="156" rx="4" fill="#7a5a3c"/><rect x="-7" y="-150" width="14" height="156" fill="url(#pWood)"/><path d="M-12 -142 h-130 l-26 28 l26 28 h130z" fill="${T}"/><path d="M12 -92 h130 l26 28 l-26 28 h-130z" fill="${G}"/><text x="-80" y="-102" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">届出</text><text x="80" y="-52" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">許可</text></g>
        <rect x="${x0}" y="${y0}" width="${hl==1?640:0}" height="${h}" fill="none"/>${hl==2?`<rect x="${x0}" y="${y0}" width="630" height="${h}" fill="#fff" opacity=".5"/>`:`<rect x="1190" y="${y0}" width="670" height="${h}" fill="#fff" opacity=".5"/>`}</g>`);
      s+=g;
      const L1=[['ときどき使う家',.4],['まず試す',2.2],['許可が取れない地域',4]],R1=[['通年',.4],['泊まった日数で回収',2.4],['一棟貸しを本格運営',4.4]];
      L1.forEach(([w,o],k)=>{if(on(1))s+=tag(760,604+k*80,w,at(1,.4,o),T,'#fff',30)});
      R1.forEach(([w,o],k)=>{if(on(2))s+=tag(1675,604+k*80,w,at(2,.4,o),G,'#fff',30)});}
    if(on(3)&&!on(5)){
      s+=card(560,250,1280,560,`<rect x="1080" y="280" width="240" height="64" rx="32" fill="${Y}"/><text x="1200" y="324" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">考えてみよう</text><text x="1200" y="395" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">3人の空き家オーナー。届出と許可、どちらが向く？</text>`,at(3,.4));
      [['1人目','週末だけ、貸したい'],['2人目','1年中貸して、収入にしたい'],['3人目','家が、住居専用地域にある']].forEach(([a1,b1],k)=>{const x=760+k*440;s+=pop(x,600,at(3,.4,1.2),`<rect x="${x-190}" y="450" width="380" height="270" rx="30" fill="#eef3f8" stroke="${NAVY}" stroke-width="4"/><circle cx="${x}" cy="520" r="40" fill="${NAVY}"/><text x="${x}" y="533" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">${k+1}</text><text x="${x}" y="610" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">${a1}</text>`)+fade(at(4,.4,.3),`<text x="${x}" y="672" text-anchor="middle" font-size="${b1.length>10?28:34}" font-weight="900" fill="${NAVY}">${b1}</text>`,0);const h0=[.3,3.3,6.8][k],h1=[3.3,6.8,99][k];if(on(4)&&at(4,.1,h0)>0&&at(4,.1,h1)<1)s+=`<rect x="${x-190}" y="450" width="380" height="270" rx="30" fill="${Y}" fill-opacity=".16" stroke="${Y}" stroke-width="10"/><circle cx="${x}" cy="520" r="${48+10*Math.abs(Math.sin(lt*4))}" fill="none" stroke="${NAVY}" stroke-width="5"/>`+pop(x+150,455,at(4,.4,h0),`<circle cx="${x+150}" cy="455" r="34" fill="${Y}"/><text x="${x+150}" y="474" text-anchor="middle" font-size="52" font-weight="900" fill="${DG}">?</text>`)});}
    const cd=lt-(L[5]-3.2);if(cd>0&&cd<3.2&&!on(5))s+=pop(1200,880,clamp((cd%1)*4),`<circle cx="1200" cy="886" r="60" fill="#000" opacity=".15"/><circle cx="1200" cy="880" r="60" fill="${Y}"/><text x="1200" y="905" text-anchor="middle" font-size="72" font-weight="900" fill="${DG}">${Math.max(1,3-Math.floor(cd))}</text>`);
    if(on(5)&&!on(8)){
      s+=card(560,250,1280,560,`<text x="1200" y="324" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">答え</text>`,at(5,.4));
      [['1人目','週末だけ、貸したい','届出',T,'日数が少なくてよい',6,.4],['2人目','1年中貸して、収入にしたい','許可',G,'日数が多く要る',6,3.2],['3人目','家が、住居専用地域にある','届出',T,'許可は原則取れない',7,.4]].forEach(([a1,b1,an,c,why,li,o],k)=>{const x=760+k*440;
        s+=fade(at(5,.4,.2),`<rect x="${x-190}" y="380" width="380" height="330" rx="30" fill="#eef3f8" stroke="${NAVY}" stroke-width="4"/><text x="${x}" y="432" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">${a1}</text><text x="${x}" y="478" text-anchor="middle" font-size="${b1.length>10?26:30}" font-weight="700" fill="#4a5a52">${b1}</text>`,0);
        s+=pop(x,560,at(5,.4,[1.2,2.4,3.6][k]),`<rect x="${x-120}" y="515" width="240" height="84" rx="42" fill="${c}"/><text x="${x}" y="573" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">${an}</text>`);
        s+=fade(at(li,.4,o),`<text x="${x}" y="655" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">${why}</text>`,0)});
      s+=fade(at(6,.4,3.8),`<text x="1200" y="760" text-anchor="middle" font-size="28" font-weight="700" fill="#4a5a52">※2人目は、場所と建物の条件に合う家なら</text>`,0);}
    if(on(8)&&!on(9))s+=qbubble('q4','あとで変えられる？',at(8,.4),t);
    if(on(8)&&!on(10)){
      s+=cardGround(600,250,1240,560,730,'#cfe0c8',at(8,.4));
      s+=tag(1220,330,'許可は、新しく申請する',at(8,.4,.6),G,'#fff',44);
      s+=pop(1220,520,at(9,.5,.4),`<rect x="720" y="440" width="1000" height="110" rx="55" fill="url(#gD)"/><text x="1220" y="513" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">取れるか ＝ 場所と建物の条件しだい</text>`);
      s+=pop(1220,690,at(9,.5,2.6),`<rect x="720" y="630" width="1000" height="100" rx="50" fill="#eef3f8" stroke="${NAVY}" stroke-width="4"/><text x="1220" y="696" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">住居専用地域は、原則、許可が取れない</text>`);}
  }
  if(i===5){ // 失敗しやすい点 3つ
    s+=aki(on(4)?'point':(on(3)?'think':'present'),on(3)&&!on(4)?'worry':'happy');
    s+=hdr('','失敗しやすい点 3つ',at(0,.4),RED);
    const drop=(p,inner)=>{if(p<=0)return '';const dy=-(1-bk(p))*560;return `<g opacity="${clamp(p*5)}" transform="translate(0,${dy})">${inner}</g>`};
    const slots=[[590,270],[1230,270],[900,540]];
    const ICONS=[
      (x,y)=>`<g transform="translate(${x+110},${y+130})"><ellipse cx="0" cy="66" rx="40" ry="8" fill="#000" opacity=".16"/><rect x="-26" y="-30" width="52" height="94" rx="18" fill="#d9342b"/><rect x="-26" y="-30" width="14" height="94" rx="8" fill="#fff" opacity=".24"/><rect x="-12" y="-52" width="24" height="26" rx="4" fill="#2a2f2c"/><path d="M12 -44 q40 -4 44 30 q2 30 -14 40" stroke="#2a2f2c" stroke-width="7" fill="none"/><rect x="-22" y="0" width="44" height="34" rx="4" fill="#fff" opacity=".9"/></g>`,
      (x,y)=>`<g transform="translate(${x+110},${y+130})"><ellipse cx="0" cy="66" rx="80" ry="9" fill="#000" opacity=".14"/>${inn(-48,64,.14,{sign:'',t,lit:.6,chim:0})}${inn(52,64,.14,{sign:'',t,lit:.3,chim:0,roof:'#7a8a9a'})}<g transform="translate(2,-38)"><path d="M-44 -30 h88 a14 14 0 0 1 14 14 v22 a14 14 0 0 1 -14 14 h-40 l-20 20 v-20 h-28 a14 14 0 0 1 -14 -14 v-22 a14 14 0 0 1 14 -14z" fill="#fff" stroke="${RED}" stroke-width="6"/><text y="14" text-anchor="middle" font-size="44" font-weight="900" fill="${RED}">!</text></g></g>`,
      (x,y)=>`<g transform="translate(${x+110},${y+130})"><ellipse cx="0" cy="66" rx="70" ry="8" fill="#000" opacity=".14"/><rect x="-60" y="-56" width="120" height="116" rx="10" fill="#f1e2bb"/><rect x="-70" y="-70" width="140" height="24" rx="12" fill="#c9a266"/><rect x="-70" y="44" width="140" height="24" rx="12" fill="#c9a266"/><path d="M-36 -22 h72 M-36 0 h72 M-36 22 h46" stroke="#a88a58" stroke-width="7" stroke-linecap="round"/><circle cx="38" cy="30" r="17" fill="#d9342b"/></g>`];
    const cardsT=[['消防設備の','費用の見落とし'],['近隣への','説明不足'],['うまい話を','そのまま信じる']];
    const startL=[1,2,3];
    cardsT.forEach(([a1,b1],k)=>{const [x,y]=slots[k],p=at(startL[k],.9,.0);if(on(startL[k])){
      const cx=x+385,extra=k===0&&on(1)?`<text x="${cx}" y="${y+170}" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">想定 約40万円</text><text x="${cx}" y="${y+212}" text-anchor="middle" font-size="32" font-weight="900" fill="${RED}">→ 約60万円（約1.5倍）</text>`:(k===1?`<text x="${cx}" y="${y+170}" text-anchor="middle" font-size="28" font-weight="900" fill="${DG}">Wi-Fi工事の車の駐車で</text><text x="${cx}" y="${y+212}" text-anchor="middle" font-size="28" font-weight="900" fill="${DG}">近所から指摘を受けた</text>`:(k===2?`<text x="${cx}" y="${y+170}" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">「許可なんて簡単」</text><text x="${cx}" y="${y+212}" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">「届出だけで1年中OK」</text>`:''));
      s+=drop(p,`${bx(x,y,600,250,28)}${ICONS[k](x,y)}<text x="${cx}" y="${y+80}" text-anchor="middle" font-size="${[40,38,36][k]}" font-weight="900" fill="${DG}">${a1}</text><text x="${cx}" y="${y+128}" text-anchor="middle" font-size="${[40,38,36][k]}" font-weight="900" fill="${DG}">${b1}</text>${extra}<circle cx="${x+36}" cy="${y+36}" r="26" fill="${RED}"/><text x="${x+36}" y="${y+48}" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">${k+1}</text>`);
      if(p>.82&&p<1)s+=`<g opacity="${1-seg(p,.82,1)}"><ellipse cx="${x+300}" cy="${y+256}" rx="${200+80*seg(p,.82,1)}" ry="10" fill="#fff" opacity=".6"/></g>`}});
    if(on(1)&&!on(3))s+=noteB('※消防設備の費用は1人の事例で、どの家でもそうなるとは限りません',at(1,.3));
    if(on(4))s+=tag(1220,845,'始める前に、窓口で確かめる',at(4,.4,.3),G,'#fff',34);
  }
  if(i===6){ // あなたの家はどっち？
    s+=aki(on(7)?'cheer':'present');
    if(on(0)&&!on(1)){
      s+=`<defs><radialGradient id="spD" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#0a1428" stop-opacity=".1"/><stop offset=".45" stop-color="#0a1428" stop-opacity=".72"/><stop offset="1" stop-color="#0a1428" stop-opacity="0"/></radialGradient><radialGradient id="spW" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6d0" stop-opacity=".55"/><stop offset=".6" stop-color="#fff6d0" stop-opacity=".18"/><stop offset="1" stop-color="#fff6d0" stop-opacity="0"/></radialGradient></defs><g opacity="${at(0,.5)}"><rect x="500" y="0" width="1420" height="1080" fill="url(#spD)"/><ellipse cx="1200" cy="600" rx="420" ry="400" fill="url(#spW)"/></g>`;
      s+=pop(1200,520,at(0,.5),inn(1200,790,1.0,{sign:'あなたの家',t,lit:1,roof:'#2e6b47',noren:T,signc:'#2f2a22'}));
      [['日数',860],['場所',1200],['建物',1540]].forEach(([w,x],k)=>{s+=tag(x,290,w,at(0,.4,[.4,1.2,2][k]),NAVY,'#fff',44)});
      s+=tag(1200,775,'日数・場所・建物が、決める3つ',at(0,.4,5.2),Y,DG,34);}
    if(on(1)&&!on(4)){
      const cols=[
        ['1','日数','1年に何日、泊めたい？',[['180日で足りる','届出も候補',T],['足りない','許可が向く',G]]],
        ['2','場所','家は住居専用地域？',[['住居専用地域','許可は原則取れない',RED],['それ以外','許可も候補',G]]],
        ['3','建物','広さ・消防設備は足りる？',[['足りている','許可も候補',G],['足りない','費用がかかる',RED]]]];
      cols.forEach(([n,a,b,ans],k)=>{const x=590+k*430,dim=on(k+1)&&!on(k+2)?1:.55;
        s+=`<g opacity="${on(k+1)?1:0}">`+card(x,260,400,540,`<circle cx="${x+66}" cy="338" r="40" fill="${[G,T,'#3d8a6a'][k]}"/><text x="${x+66}" y="354" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">${n}</text><text x="${x+120}" y="352" font-size="36" font-weight="900" fill="${DG}">${a}</text><text x="${x+200}" y="440" text-anchor="middle" font-size="30" font-weight="700" fill="#4a5a52">${b}</text>`+ans.map(([w,r,c],j)=>(j===1&&lt<L[k+1]+3.5*K)?'':`<rect x="${x+24}" y="${480+j*150}" width="352" height="128" rx="24" fill="${c}"/><rect x="${x+36}" y="${488+j*150}" width="328" height="26" rx="13" fill="#fff" opacity=".18"/><text x="${x+200}" y="${526+j*150}" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">${w}</text><text x="${x+200}" y="${580+j*150}" text-anchor="middle" font-size="${r.length>8?30:36}" font-weight="900" fill="#fff">${r}</text>`).join(''),at(k+1,.4))+(dim<1?`<rect x="${x}" y="260" width="400" height="540" rx="28" fill="#1f3a2b" opacity=".42"/>`:'')+`</g>`});
    }
    if(on(4)&&!on(5)){
      s+=pop(1200,470,at(4,.5),`${bx(640,250,1120,430,40)}<text x="1200" y="340" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">決める3つ</text>`+
        `<rect x="680" y="370" width="1040" height="130" rx="30" fill="${G}"/><text x="1200" y="420" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">日数が多く必要・場所も建物もOK</text><text x="1200" y="474" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">→ 許可</text>`+
        `<rect x="680" y="525" width="1040" height="130" rx="30" fill="${T}"/><text x="1200" y="575" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">どれかが難しい</text><text x="1200" y="629" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">→ 届出</text>`);}
    if(on(5)&&!on(6)){
      [['手続きの比較表（記事）','doc',G],['旅館業の許可の取り方（記事）','key',T],['無料相談','chat','#3d8a6a']].forEach(([w,ic,c],k)=>{const y=330+k*150;
        s+=pop(1200,y,at(5,.4,[.4,2.0,3.6][k]),`${bx(640,y-60,1120,124,36)}${icon(740,y+2,44,ic,c,'#fff',.95)}<text x="830" y="${y+16}" font-size="46" font-weight="900" fill="${DG}">${w}</text><text x="1720" y="${y+14}" text-anchor="end" font-size="34" font-weight="900" fill="${c}">概要欄へ ▶</text>`)});}
    if(on(6)&&!on(7)){
      s+=pop(900,480,at(6,.5,.3),`<rect x="640" y="326" width="520" height="300" rx="26" fill="#000" opacity=".14" transform="translate(0 8)"/><rect x="640" y="326" width="520" height="300" rx="26" fill="url(#gD)"/><rect x="660" y="346" width="480" height="260" rx="16" fill="#cfe9d4"/>${inn(880,530,.36,{sign:'',t,lit:.7,chim:1})}${coin(1050,420,34)}${coin(1090,480,28)}<rect x="660" y="548" width="480" height="58" rx="12" fill="#fff" opacity=".94"/><text x="900" y="589" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">民泊は「第3の資産」</text><rect x="660" y="346" width="150" height="48" rx="24" fill="${T}"/><text x="735" y="380" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">第1回</text><g transform="translate(730,470)"><circle r="42" fill="#fff" opacity=".92"/><path d="M-14 -22 L28 0 L-14 22Z" fill="${T}"/></g>`);
      s+=card(1200,330,640,300,`<text x="1240" y="410" font-size="40" font-weight="900" fill="${DG}">年180日の上限を知ったうえで</text><text x="1240" y="480" font-size="40" font-weight="900" fill="${DG}">宿を資産に入れる理由を見る</text><text x="1240" y="550" font-size="40" font-weight="900" fill="${T}">手続き選びの意味がわかる</text>`,at(6,.5,2.2));}
    if(on(7)){
      s+=pop(1200,470,at(7,.5),`${bx(660,270,1080,380,40)}${icon(940,380,70,'chat',G,'#fff',1.3)}<text x="1280" y="400" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">あなたの家は、どちら？</text>${formulaChip(900,480,300,'届出',T,'#fff',46)}${formulaChip(1260,480,300,'許可',G,'#fff',46)}<text x="1200" y="620" text-anchor="middle" font-size="34" font-weight="900" fill="${T}">コメントで教えてください</text>`);}
    s+=fade(seg(lt,E[7]+.5,E[7]+1.2),`<rect width="1920" height="1080" fill="#16301f"/><circle cx="960" cy="200" r="260" fill="url(#glow)" opacity=".25"/><text x="960" y="380" text-anchor="middle" font-size="60" font-weight="900" fill="#fff">最後まで見てくれて、ありがとうございます</text><text x="960" y="460" text-anchor="middle" font-size="37" font-weight="700" fill="#dfe9e3">${NOTE}</text><text x="960" y="524" text-anchor="middle" font-size="37" font-weight="700" fill="#dfe9e3">宿の稼働率は、開業から約8.5か月の平均の一例です。</text><text x="960" y="584" text-anchor="middle" font-size="37" font-weight="700" fill="#dfe9e3">手間と初期投資は含みません。出典は概要欄に記載しています。</text><text x="960" y="662" text-anchor="middle" font-size="34" font-weight="700" fill="#b8c9bf">${CREDIT}</text><rect x="780" y="730" width="360" height="100" rx="50" fill="#fff"/>${LOGO(810,745,1.1)}`,0);
  }
  const TT={2:['決める3つ ①','何日、泊められる？',NAVY],3:['決める3つ ②③','許可の条件は？',NAVY],4:['最後の問い','自分は、どちら？',NAVY],5:['注意','失敗しやすい点 3つ',RED]};
  if(TT[i]&&L.length>1&&lt<L[1]){const [a,b,c]=TT[i],p=at(0,.4,.1)*(1-seg(lt,L[1]-.35,L[1]-.05)),fs=b.length>8?72:b.length>6?88:120;s+=pop(1180,480,p,`${bx(640,300,1080,360,40)}<rect x="${1180-140}" y="270" width="280" height="76" rx="38" fill="${c}"/><text x="1180" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">${a}</text><text x="1180" y="${fs>100?560:540}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${c}">${b}</text>${sparkle(760,380,1,t,1)}${sparkle(1620,560,.9,t,3)}`);}
  return s;
}
window.draw=function(t){
  let i=SC.findIndex(([a,b])=>t>=a&&t<b);if(i<0)i=SC.length-1;
  const a=SC[i][0],TR=.6;
  let out=`${DEFS}${studio(t,i)}${scene(i,t,t-a)}`;
  if(i>0&&t-a<TR){const k=eo((t-a)/TR),r=k*1150,pa=SC[i-1][0];
    out=`${DEFS}${studio(t,i-1)}${scene(i-1,t,t-pa)}<clipPath id="iris"><circle cx="960" cy="540" r="${r}"/></clipPath><g clip-path="url(#iris)">${out}</g><circle cx="960" cy="540" r="${r}" fill="none" stroke="#fff" stroke-width="${26*(1-k)}" opacity="${1-k}"/>`;}
  { // オープニングのあと、左上に今回の動画のタイトル（ずっと出しておく）
    const t0=SL[0][0]-.3,p=seg(t,t0,t0+.5),e=1-seg(t,SC[SC.length-1][1]-6,SC[SC.length-1][1]-5.4);
    if(p>0)out+=`<g opacity="${p*e}"><rect x="24" y="26" width="${EP_TITLE.length*30+92}" height="56" rx="28" fill="#000" opacity=".14"/><rect x="24" y="20" width="${EP_TITLE.length*30+92}" height="56" rx="28" fill="#fff" opacity=".94"/><circle cx="52" cy="48" r="16" fill="${G}"/>${MARK(52,48,.42)}<text x="78" y="58" font-size="28" font-weight="900" fill="${DG}">${EP_TITLE}</text></g>`;
  }
  { // 画面の隅の「いま3つのうち何番め」（章2〜）
    const act={2:[0],3:[1,2]}[i];
    if(act!=null){const items=[['① 日数',130],['② 場所',130],['③ 建物',130]];let x=1400,g='';
      items.forEach(([w,wd],k)=>{const on1=act.includes(k);g+=`<rect x="${x}" y="22" width="${wd}" height="50" rx="25" fill="${on1?NAVY:'#fff'}" opacity="${on1?1:.8}" stroke="${NAVY}" stroke-width="3"/><text x="${x+wd/2}" y="55" text-anchor="middle" font-size="26" font-weight="900" fill="${on1?'#fff':NAVY}">${w}</text>`;x+=wd+26});
      const pp=seg(t,SC[2][0]+.6,SC[2][0]+1.2);out+=`<g opacity="${pp*(1-seg(t,SC[SC.length-1][1]-6,SC[SC.length-1][1]-5.4))}"><text x="1366" y="55" text-anchor="end" font-size="26" font-weight="900" fill="${NAVY}">決める3つ</text>${g}</g>`;}
  }
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
            say = opt.get("say", disp)
            for a_, b_ in READ_FIX:
                say = say.replace(a_, b_)
            f, d = tts(say, v["style"], MODELS, cache, v["speed"], v["pitch"], v["intonation"])
            voices.append((t, f)); lines.append([round(t, 3), round(t + d, 3), spk, wrap(disp), i, k])
            if "call" in opt:  # 字幕を出さない呼び込みの声（オープニングなど）
                off, cs, ctext = opt["call"]; cv = VOICES[cs]
                cf, _ = tts(ctext, cv["style"], MODELS, cache, cv["speed"], cv["pitch"], cv["intonation"])
                voices.append((t + off, cf))
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
            f"const THEME={json.dumps([s[0] for s in SCENES])};const CREDIT={json.dumps(CREDIT, ensure_ascii=False)};const NOTE={json.dumps(NOTE, ensure_ascii=False)};const EP_TITLE={json.dumps(EP_TITLE, ensure_ascii=False)};")
    return h[:a] + head + SCENE_JS + h[b:]


def main():
    args = sys.argv[1:]
    hq = "--hq" in args; args = [x for x in args if x != "--hq"]
    prev = None
    if "--preview" in args:
        k = args.index("--preview"); prev = [float(x) for x in args[k + 1:]]; args = args[:k]
    nocheck = "--no-check" in args; args = [x for x in args if x != "--no-check"]
    # 分けて書き出す（定期実行では1回の命令が10分までなので）:
    #   --work <フォルダ> --part k  … 全コマのうち k 番目の区切り（PART_FRAMES コマずつ）だけを、フォルダに描く。残りの数を表示する
    #   --work <フォルダ>（--part なし）… フォルダのコマと音声から mp4 を作る（全部そろっていないと止まる）
    work = None; part = None
    if "--work" in args:
        k = args.index("--work"); work = args[k + 1]; del args[k:k + 2]
    if "--part" in args:
        k = args.index("--part"); part = int(args[k + 1]); del args[k:k + 2]
    out = args[0] if args else os.path.join(tempfile.gettempdir(), "akiyado-strategy-ep2.mp4")
    if prev is None and not nocheck and not (work and part and part > 1) and not (work and part is None):  # 書き出しの前に、文字の重なり・はみ出しを自動点検（layout_check.py）
        r = subprocess.run([sys.executable, os.path.join(HERE, "layout_check.py"), "make_strategy_ep2", "--step", "0.5"])
        if r.returncode:
            sys.exit("自動点検で問題が見つかったため、書き出しを止めました（直してから再実行。点検を飛ばすなら --no-check）")
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
        total = int(dur * FPS)
        if work:
            fr = os.path.join(work, "fr"); os.makedirs(fr, exist_ok=True)
            if part is not None:
                n = (total + PART_FRAMES - 1) // PART_FRAMES
                a0, a1 = (part - 1) * PART_FRAMES, min(total, part * PART_FRAMES)
                if a0 >= total:
                    print(f"区切り {part} はありません（全 {n} 区切り）"); return
                js2 = js + ".part.js"
                open(js2, "w").write(base.RENDER_JS.replace("for (let i = 0; i < n; i++)", f"for (let i = {a0}; i < Math.min(n, {a1}); i++)"))
                subprocess.run(["node", js2, h, fr, "video", str(total)], check=True, env=env)
                print(f"区切り {part}/{n} を描きました（コマ {a0}〜{a1 - 1}）。残り {n - part} 区切り"); return
            miss = [i for i in range(total) if not os.path.exists(os.path.join(fr, f"f{i:05d}.jpg"))]
            if miss:
                sys.exit(f"まだ描いていないコマがあります（{len(miss)} コマ。最初は {miss[0]}）。--part で描いてから、もう一度実行してください")
        else:
            fr = os.path.join(tmp, "fr"); os.makedirs(fr)
            subprocess.run(["node", js, h, fr, "video", str(total)], check=True, env=env)
        import pop_audio
        wav = os.path.join(tmp, "audio.wav"); pop_audio.write(wav, dur, sfx, bgm_gain=0.22, voices=voices, duck=0.3)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%05d.jpg"), "-i", wav, "-c:v", "libx264",
                        "-preset", "slow" if hq else "veryfast", "-crf", "14" if hq else "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k" if hq else "192k",
                        "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, round(dur, 1), "秒")


if __name__ == "__main__":
    main()
