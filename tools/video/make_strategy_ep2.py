#!/usr/bin/env python3
"""アキヤドの解説動画 第2回「民泊は届出か許可か」（約9分・1920×1080）を作る。

- 話し手はアニメの民泊戦略家「アキ」。聞き手にユウタ。型は docs/youtube/manual.md 1-2章、骨組みは docs/youtube/ep2-plan.md。
- 第1回からの改善（2026-10-23）: 冒頭30秒に自己紹介を入れない（名乗りは章2の終わりに一言だけ）／イラストを作り込む
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
    "A": dict(name="戦略家 アキ", style=83, speed=1.12, intonation=1.2, pitch=0.0),   # 青山龍星（喜び）。明るく、テンポよく
    "K": dict(name="ジングル", style=1, speed=1.0, intonation=1.6, pitch=0.04),         # ずんだもん（あまあま）。オープニングの呼び込み
    "Y": dict(name="ユウタ", style=11, speed=1.08, intonation=1.15, pitch=0.0),        # 玄野武宏
}
MODELS = [0, 4, 15]
CREDIT = "VOICEVOX:青山龍星　VOICEVOX:玄野武宏　VOICEVOX:ずんだもん"
EP_TITLE = "民泊の手続き2つの違い"  # オープニングのあと、左上に出す今回のタイトル
NOTE = "※ 情報提供が目的で、特定の選択を勧めるものではありません。ルールは変わり、自治体で違います。"

SCENES = [
    ("sunset", 0.8, [
        ('A', '空き家で宿を始めたい人へ。まず、結論です。', dict(pre=3.4, call=(-3.0, 'K', 'アキヤド、みんぱくスクール！'), sfx=[(-3.9, 'whoosh'), (-3.55, 'pop'), (-2.9, 'bling'), (-0.4, 'whoosh'), (0.2, 'pop'), (1.6, 'pop')])),
        ('A', '旅館業の許可なら、1年に365日、泊められます。でも、民泊新法の届出だと、180日までです。', dict(say='旅館業の許可なら、いちねんに、さんびゃくろくじゅうごにち、泊められます。でも、民泊新法の届出だと、ひゃくはちじゅうにちまでです。', sfx=[(0.4, 'pop')])),
        ('A', '民泊戦略家の、アキです。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'ここで、ひとつ疑問です。許可のほうが、得に見えますよね。それなのに、なぜ届出で始める人がいるのでしょう？', dict(sfx=[(0.4, 'pop')])),
        ('A', 'その答えを、この動画で説明します。', dict(sfx=[(0.4, 'pop')])),
        ('A', '話は3つです。1つめは、泊められる日数。2つめは、許可の条件。3つめは、どちらを選ぶかの決め手です。', dict(say='話は、みっつです。ひとつめは、泊められる日数。ふたつめは、許可の条件。みっつめは、どちらを選ぶかの決め手です。', sfx=[(0.4, 'pop')])),
        ('A', '民泊が初めての人にも、分かるように話します。まず、民泊とは何か、からいきましょう。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("morning", 0.8, [
        ('A', '民泊とは、空き家や自宅に、旅行者を泊めて、お金をもらうことです。', dict(sfx=[(0, 'chime')])),
        ('A', 'お金をもらって人を泊めるには、国のルールに沿った手続きが要ります。少し貸すだけでも、同じです。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'その手続きの入口は、2つあります。届出と、許可です。', dict(say='その手続きの入口は、ふたつあります。届出と、許可です。', sfx=[(0.4, 'pop')])),
        ('A', '届出とは、民泊新法にしたがって、役所に「民泊をやります」と知らせる方法です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '民泊新法の正式な名前は、住宅宿泊事業法です。2018年6月に始まりました。', dict(say='民泊新法の正式な名前は、住宅宿泊事業法です。二千十八ねん、ろくがつに始まりました。', sfx=[(0.4, 'pop')])),
        ('A', '許可とは、旅館業法にしたがって、保健所の許可をもらう方法です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '小さな宿向けの許可は、簡易宿所と呼ばれます。', dict(sfx=[(0.4, 'pop')])),
        ('A', 'ほかに、特区民泊もあります。でも今日は、届出と許可の2つだけを話します。', dict(say='ほかに、特区民泊もあります。でも今日は、届出と許可のふたつだけを話します。', sfx=[(0.4, 'pop')])),
        ('Y', 'へえ、どっちも民泊なんですよね？ 何が違うんですか？', dict(sfx=[(0.4, 'pop')])),
        ('A', 'はい、どちらも民泊です。でも、1年に泊められる日数が違います。まず、そこから見ましょう。', dict(say='はい、どちらも民泊です。でも、いちねんに泊められる日数が違います。まず、そこから見ましょう。', sfx=[(0.4, 'pop')])),
    ]),
    ("noon", 0.8, [
        ('A', 'ここまでで、入口が2つあると分かりました。次は、泊められる日数の違いです。', dict(say='ここまでで、入口がふたつあると分かりました。次は、泊められる日数の違いです。', sfx=[(0, 'chime')])),
        ('A', '届出で始めると、泊められるのは、1年に180日までです。', dict(say='届出で始めると、泊められるのは、いちねんに、ひゃくはちじゅうにちまでです。', sfx=[(0.4, 'pop')])),
        ('A', '許可なら、日数の制限はありません。', dict(sfx=[(0.4, 'pop')])),
        ('A', '180日は、1年のおよそ半分。割合にすると、約49%です。', dict(say='ひゃくはちじゅうにちは、いちねんの、およそ半分。割合にすると、やく よんじゅうきゅうパーセントです。', sfx=[(0.4, 'pop')])),
        ('A', '地域のルールで、180日より短くなることもあります。', dict(say='地域のルールで、ひゃくはちじゅうにちより短くなることもあります。', sfx=[(0.4, 'pop')])),
        ('A', 'ここで、言葉をひとつ覚えましょう。稼働率です。1年のうち、お客さんが泊まった日の割合のことです。', dict(say='ここで、言葉をひとつ覚えましょう。稼働率です。いちねんのうち、お客さんが泊まった日の割合のことです。', sfx=[(0.4, 'pop')])),
        ('A', 'たとえば、稼働率が49%なら、1年に約180日、泊まることになります。', dict(say='たとえば、稼働率が、よんじゅうきゅうパーセントなら、いちねんに、やく ひゃくはちじゅうにち、泊まることになります。', sfx=[(0.4, 'pop')])),
        ('A', 'つまり、お客さんが多い宿ほど、届出の180日に、先に届いてしまいます。', dict(say='つまり、お客さんが多い宿ほど、届出の、ひゃくはちじゅうにちに、先に届いてしまいます。', sfx=[(0.4, 'pop')])),
        ('A', '私たちの宿の例を話します。開業から約8.5か月で、稼働率は約53%でした。', dict(say='私たちの宿の例を話します。開業から、やく はってんご かげつで、稼働率は、やく ごじゅうさんパーセントでした。', sfx=[(0.4, 'pop')])),
        ('A', 'この調子で1年続くと、泊まる日は約193日になります。180日を超えますね。ただし、これは一例です。', dict(say='この調子で、いちねん続くと、泊まる日は、やく ひゃくきゅうじゅうさんにちになります。ひゃくはちじゅうにちを超えますね。ただし、これは一例です。', sfx=[(0.4, 'pop')])),
        ('A', 'だから私たちは、日数の制限がない、旅館業の簡易宿所の許可を選びました。', dict(sfx=[(0.4, 'pop')])),
        ('A', '一方、ときどき使う家や、まず試したい家なら、180日でも困りません。', dict(say='一方、ときどき使う家や、まず試したい家なら、ひゃくはちじゅうにちでも困りません。', sfx=[(0.4, 'pop')])),
        ('Y', 'お客さんが少なければ、届出でも、いいんですか？', dict(sfx=[(0.4, 'pop')])),
        ('A', 'はい、そういう場合もあります。大事なのは、自分の家で、何日泊めたいかです。', dict(say='はい、そういう場合もあります。大事なのは、自分の家で、なんにち泊めたいかです。', sfx=[(0.4, 'pop')])),
        ('A', '日数だけ見れば、許可が有利です。それなのに、なぜ届出を選ぶ人がいるのか。次は、許可の条件を見ます。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("golden", 0.8, [
        ('A', 'ここまでで、許可は日数で有利と分かりました。次は、許可の条件です。', dict(sfx=[(0, 'chime')])),
        ('A', 'まず、手続きの窓口です。届出は、都道府県などの役所。許可は、保健所です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '建物はどうでしょう。届出なら、今の住まいのままで大丈夫です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '台所、浴室、トイレ、洗面。この4つがあれば、使えます。', dict(say='台所、浴室、トイレ、洗面。このよっつがあれば、使えます。', sfx=[(0.4, 'pop')])),
        ('A', '許可には、宿としての基準があります。', dict(sfx=[(0.4, 'pop')])),
        ('A', '建物の図面を出して、火災報知器や誘導灯などの消防設備を付けます。そのうえで、保健所の確認を受けます。', dict(sfx=[(0.4, 'pop')])),
        ('A', '広さにも目安があります。10人未満なら、1人あたり3.3平方メートルです。', dict(say='広さにも目安があります。じゅうにん未満なら、ひとりあたり、さんてんさん へいほうメートルです。', sfx=[(0.4, 'pop')])),
        ('A', 'たとえば、4人なら13.2平方メートル。10人以上なら、33平方メートル以上です。', dict(say='たとえば、よにんなら、じゅうさんてんに へいほうメートル。じゅうにん以上なら、さんじゅうさん へいほうメートル以上です。', sfx=[(0.4, 'pop')])),
        ('A', '届出でも、1人あたり3.3平方メートル以上は、必要です。', dict(say='届出でも、ひとりあたり、さんてんさん へいほうメートル以上は、必要です。', sfx=[(0.4, 'pop')])),
        ('A', '場所の条件もあります。住居専用地域とは、住宅だけを建てる地域のことです。', dict(sfx=[(0.4, 'pop')])),
        ('Y', 'もし、うちの空き家がそこにあったら、許可は取れないんですか？', dict(sfx=[(0.4, 'pop')])),
        ('A', '原則、取れません。届出なら、できますが、地域のルールで制限があります。', dict(sfx=[(0.4, 'pop')])),
        ('A', '管理の仕方も違います。家主が不在なら、届出では、管理業者に任せる決まりです。', dict(sfx=[(0.4, 'pop')])),
        ('A', '許可では、持ち主が自分で、管理の体制を整えます。', dict(sfx=[(0.4, 'pop')])),
        ('A', '宿に使う部分が200平方メートルを超えると、用途変更も要ります。建物の使い道を変える手続きです。', dict(say='宿に使う部分が、にひゃく へいほうメートルを超えると、用途変更も要ります。建物の使い道を変える手続きです。', sfx=[(0.4, 'pop')])),
        ('A', '私たちは、許可を取るとき、開業の2か月前に、保健所と消防署に相談しました。', dict(say='私たちは、許可を取るとき、開業のにかげつ前に、保健所と消防署に相談しました。', sfx=[(0.4, 'pop')])),
        ('A', '手続きは自分でやって、許可が出るまで、1〜2か月。許可番号がないと、Airbnbで予約を受けられません。', dict(say='手続きは自分でやって、許可が出るまで、いっかげつから、にかげつ。許可番号がないと、エアビーアンドビーで予約を受けられません。', sfx=[(0.4, 'pop')])),
        ('A', 'ただし、これは下田の1件の経験です。どこでも同じとは限りません。必ず、地元の窓口で確かめてください。', dict(say='ただし、これは下田の、いっけんの経験です。どこでも同じとは限りません。必ず、地元の窓口で確かめてください。', sfx=[(0.4, 'pop')])),
    ]),
    ("evening", 0.8, [
        ('A', 'ここまでで、疑問の答えが分かりました。許可は日数が強く、届出は始めやすい。次は、どちらが向くかです。', dict(sfx=[(0, 'chime')])),
        ('A', '届出が向くのは、小さく試したい人。ときどき使う家。そして、住居専用地域の家です。', dict(sfx=[(0.4, 'pop')])),
        ('A', '許可が向くのは、1年中、事業としてやりたい人です。', dict(say='許可が向くのは、いちねんじゅう、事業としてやりたい人です。', sfx=[(0.4, 'pop')])),
        ('A', '泊まった日数で、お金を回収したい人。家を1棟まるごと貸す、本格的な宿にも向きます。', dict(say='泊まった日数で、お金を回収したい人。家をいっとうまるごと貸す、本格的な宿にも向きます。', sfx=[(0.4, 'pop')])),
        ('A', 'ここで、考えてみてください。できるだけ多く泊めたい家が、住居専用地域にあります。どうしますか？', dict(sfx=[(0.4, 'pop')])),
        ('A', 'A、届出で、180日まで泊める。B、許可を取りに行く。C、別の場所の家を探す。迷いますよね。', dict(say='エー、届出で、ひゃくはちじゅうにちまで泊める。ビー、許可を取りに行く。シー、別の場所の家を探す。迷いますよね。', sfx=[(0, 'chime')])),
        ('A', '答えは、AかCです。住居専用地域では、許可は原則取れません。多く泊めたいなら、C。今の家で始めるなら、A。分かれ目は、家の場所です。', dict(pre=3.2, say='答えは、エーか、シーです。住居専用地域では、許可は原則取れません。多く泊めたいなら、シー。今の家で始めるなら、エー。分かれ目は、家の場所です。', sfx=[(-3.2, 'tick'), (-2.2, 'tick'), (-1.2, 'tick'), (0, 'ding'), (1.2, 'bling')])),
        ('Y', '届出で試して、あとから許可に変えられますか？', dict(sfx=[(0.4, 'pop')])),
        ('A', 'ここは、自治体と家によって違います。言い切れないので、窓口で確かめてください。', dict(sfx=[(0.4, 'pop')])),
        ('A', '決め手は、2つです。1年に何日泊めたいか。そして、その家で許可が取れるか。', dict(say='決め手は、ふたつです。いちねんに、なんにち泊めたいか。そして、その家で許可が取れるか。', sfx=[(0.4, 'pop')])),
    ]),
    ("twilight", 0.8, [
        ('A', 'ここからは、失敗しやすい点を4つ。決め方が分かったので、次は、決めたあとの注意です。', dict(say='ここからは、失敗しやすい点をよっつ。きめかたが分かったので、次は、決めたあとの注意です。', sfx=[(0, 'chime')])),
        ('A', '失敗しやすいのは、家を買ったあとに気づくことです。買ったあとでは、選べる道が、かぎられます。', dict(sfx=[(0.4, 'pop')])),
        ('A', '1つめ。買ってから、許可が取れないと知る。もう遅いんです。', dict(say='ひとつめ。買ってから、許可が取れないと知る。もう遅いんです。', sfx=[(0.4, 'pop')])),
        ('A', '2つめ。消防設備の費用の見落とし。会社員のオーナーさんの例では、想定の約40万円が、約60万円になりました。約1.5倍です。', dict(say='ふたつめ。消防設備の費用の見落とし。会社員のオーナーさんの例では、想定の、やく よんじゅうまんえんが、やく ろくじゅうまんえんになりました。やく いってんごばいです。', sfx=[(0.4, 'pop')])),
        ('A', 'これは、1人の事例です。どの家でもそうなる、という話ではありません。', dict(say='これは、ひとりの事例です。どの家でもそうなる、という話ではありません。', sfx=[(0.4, 'pop')])),
        ('A', '3つめ。地域のルールで、営業が制限されること。届出でも許可でも、できることが変わります。', dict(say='みっつめ。地域のルールで、営業が制限されること。届出でも許可でも、できることが変わります。', sfx=[(0.4, 'pop')])),
        ('A', '4つめ。近隣への説明不足。私たちも、Wi-Fi工事の車の駐車で、近所から指摘を受けました。', dict(say='よっつめ。近隣への説明不足。私たちも、ワイファイ工事の車の駐車で、近所から指摘を受けました。', sfx=[(0.4, 'pop')])),
        ('A', '「許可なんて簡単」とか、「届出だけで1年中OK」と言われたら、まず疑ってください。', dict(say='「許可なんて簡単」とか、「届出だけで、いちねんじゅうオーケー」と言われたら、まず疑ってください。', sfx=[(0.4, 'pop')])),
        ('A', '家を買う前に、役所へ相談する。これが、いちばんの対策です。', dict(sfx=[(0.4, 'pop')])),
    ]),
    ("night", 4.6, [
        ('A', '最後に、あなたの家はどちらか、確かめましょう。3つの質問に、答えてください。', dict(say='最後に、あなたの家はどちらか、確かめましょう。みっつの質問に、答えてください。', sfx=[(0, 'chime')])),
        ('A', '質問1。1年に、何日泊めたいですか？ 180日で足りるなら、届出も候補です。足りないなら、許可です。', dict(say='質問そのいち。いちねんに、なんにち泊めたいですか？ ひゃくはちじゅうにちで足りるなら、届出も候補です。足りないなら、許可です。', sfx=[(0.4, 'pop')])),
        ('A', '質問2。その家で、許可は取れそうですか？ 住居専用地域なら、原則むずかしい。広さが足りないなら、窓口に相談です。', dict(say='質問そのに。その家で、許可は取れそうですか？ 住居専用地域なら、原則むずかしい。広さが足りないなら、窓口に相談です。', sfx=[(0.4, 'pop')])),
        ('A', '質問3。誰が運営しますか？ 家主が不在なら、届出では、管理業者に任せます。許可は、自分たちで管理します。', dict(say='質問そのさん。誰が運営しますか？ 家主が不在なら、届出では、管理業者に任せます。許可は、自分たちで管理します。', sfx=[(0.4, 'pop')])),
        ('A', 'まとめです。泊めたい日数と、その家で許可が取れるか。この2つで、決まります。', dict(say='まとめです。泊めたい日数と、その家で許可が取れるか。このふたつで、決まります。', sfx=[(0.4, 'pop')])),
        ('A', '手続きの比較表は、概要欄の記事に。許可の取り方の記事と、無料相談も、概要欄のリンクからどうぞ。', dict(say='手続きの比較表は、概要欄の記事に。許可のとりかたの記事と、無料相談も、概要欄のリンクからどうぞ。', sfx=[(0.4, 'pop')])),
        ('A', '次は、第1回「民泊は第3の資産」がおすすめです。日数の上限を知ったうえで見ると、宿を資産に入れる意味が、よく分かります。', dict(say='次は、だいいっかい、「民泊は、だいさんの資産」がおすすめです。日数の上限を知ったうえで見ると、宿を資産に入れる意味が、よく分かります。', sfx=[(0.4, 'pop')])),
        ('A', 'あなたの家は、届出と許可の、どちらに向きそうですか？ コメントで、教えてください。', dict(sfx=[(0.4, 'pop')])),
    ]),
]
LEAD, GAP = 0.5, 0.32
# 読みまちがえやすい言葉は、音声を作る前にひらがなに置きかえる（字幕はそのまま）
READ_FIX = [("知りたい方", "知りたいかた"), ("入れ方", "入れかた"), ("稼ぎ方", "稼ぎかた"), ("使い方", "使いかた"), ("始め方", "始めかた"),
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
  const w=title.length*54+(no?250:80);
  return fade(p,`<rect x="540" y="72" width="${w}" height="86" rx="43" fill="#000" opacity=".13"/><rect x="540" y="66" width="${w}" height="86" rx="43" fill="#fff" opacity=".96"/>${no?`<rect x="552" y="77" width="190" height="64" rx="32" fill="${c}"/><text x="647" y="121" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">${no}</text>`:''}<text x="${no?764:584}" y="123" font-size="54" font-weight="900" fill="${DG}">${title}</text>`,0);
}
const tag=(x,y,txt,p,c=Y,fc=DG,fs=34)=>pop(x,y,p,`<rect x="${x-txt.length*fs*.5-24}" y="${y-fs*.88+5}" width="${txt.length*fs+48}" height="${fs*1.76}" rx="${fs*.88}" fill="#000" opacity=".13"/><rect x="${x-txt.length*fs*.5-24}" y="${y-fs*.88}" width="${txt.length*fs+48}" height="${fs*1.76}" rx="${fs*.88}" fill="${c}"/><rect x="${x-txt.length*fs*.5-10}" y="${y-fs*.88+4}" width="${txt.length*fs+20}" height="${fs*.5}" rx="${fs*.25}" fill="#fff" opacity=".2"/><text x="${x}" y="${y+fs*.36}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${fc}">${txt}</text>`);
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
  if(o.sign){const fs=34,w=o.sign.length*fs+36;h+=`<rect x="${-w/2}" y="-262" width="${w}" height="50" rx="8" fill="#000" opacity=".16" transform="translate(0 5)"/><rect x="${-w/2}" y="-262" width="${w}" height="50" rx="8" fill="${o.signc||'#4a3324'}"/><rect x="${-w/2}" y="-262" width="${w}" height="50" fill="url(#pWood)"/><rect x="${-w/2+4}" y="-258" width="${w-8}" height="6" rx="3" fill="#fff" opacity=".2"/><text x="0" y="-226" text-anchor="middle" font-size="${fs}" font-weight="900" fill="#fff">${o.sign}</text>`}
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
const cmpCard=(p,head)=>card(600,250,1240,540,`<text x="1220" y="324" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">${head}</text>`+cmp(660,'民泊新法の届出',G,[['泊められる日数','年180日まで','#d99a2b','△'],['条件・手間','軽い（始めやすい）',G,'○']])+cmp(1240,'旅館業の許可',T,[['泊められる日数','制限なし',G,'○'],['条件・手間','重い',RED,'△']]),p);
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
  if(i===0){ // つかみ
    const pose=on(4)?'present':on(3)?'point':on(2)?'present':on(1)?'think':'present';
    if(lt>L[0]-.6)s+=aki(pose,on(1)&&!on(2)?'worry':'happy');
    if(lt>L[0]-.5&&!on(1)){
      const A=900,B=1480,by=585,d=Math.floor(365*seg(lt,L[0]+1.0,L[0]+7.2)),dA=Math.min(d,180);
      s+=pop(A,by-100,at(0,.5,.1),inn(A,by,.6,{sign:'民泊届出',roof:'#b5603a',noren:G,t,lit:.55,case:1}));
      s+=pop(B,by-100,at(0,.5,.4),inn(B,by,.68,{sign:'旅館業許可',roof:'#2e6b47',noren:T,t,lit:.85,post:1,bike:1,signc:'#2f2a22'}));
      s+=card(620,618,560,196,`<text x="900" y="652" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">民泊新法の届出：年180日まで</text>${cal(641,664,14,dA,180)}${shutter(641,664,14,180,seg(lt,L[0]+4.1,L[0]+4.6),'',0)}`,at(0,.4,.5));
      s+=card(1200,618,560,196,`<text x="1480" y="652" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">旅館業の許可：日数の上限なし</text>${cal(1221,664,14,d,0)}`,at(0,.4,.8));
    }
    if(on(1)&&!on(2)){
      s+=pop(250,205,at(1,.4),`<rect x="68" y="168" width="364" height="76" rx="38" fill="#000" opacity=".14"/><rect x="68" y="160" width="364" height="76" rx="38" fill="url(#gG)"/><text x="250" y="212" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">民泊戦略家 アキ</text>`);
      s+=card(600,250,1240,540,`<text x="1220" y="340" text-anchor="middle" font-size="50" font-weight="900" fill="${DG}">許可なら、1年に365日、泊められる</text><text x="1220" y="410" text-anchor="middle" font-size="50" font-weight="900" fill="${T}">それなのに、なぜ届出で始める人がいる？</text>${q(1220,690,190,t,0)}`,at(1,.4));}
    if(on(2)&&!on(3))s+=cmpCard(at(2,.4),'答え：日数は許可、始めやすさは届出が強い');
    if(on(3)&&!on(4)){const it=[['1','1年に泊められる日数の違い',G],['2','許可を取る条件と手間',T],['3','届出か許可かの決め手と注意点','#3d8a6a']];
      s+=card(640,270,1160,470,`<text x="1220" y="350" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">今日わかること</text>`,at(3,.4));
      it.forEach(([n,w,c],k)=>{const y=450+k*110;s+=pop(1220,y,at(3,.4,[1.4,4.4,8][k]),`<rect x="720" y="${y-44}" width="1000" height="92" rx="46" fill="${c}"/><rect x="740" y="${y-38}" width="960" height="24" rx="12" fill="#fff" opacity=".18"/><circle cx="776" cy="${y}" r="34" fill="#fff"/><text x="776" y="${y+14}" text-anchor="middle" font-size="42" font-weight="900" fill="${c}">${n}</text><text x="840" y="${y+15}" font-size="${w.length>12?40:44}" font-weight="900" fill="#fff">${w}</text>`)});}
    if(on(4)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(4,.4));
      s+=tag(1220,330,'まず、民泊とは何か',at(4,.4,.3),Y,DG,46);
      s+=pop(1380,560,at(4,.5,.8),inn(1380,728,.72,{sign:'宿',t,lit:.7,case:1,post:1}));
      s+=pop(840,600,at(4,.5,1.4),`<g transform="translate(840,590)"><ellipse cx="0" cy="130" rx="90" ry="12" fill="#000" opacity=".15"/>${coin(-30,100,52)}${coin(40,60,44)}${coin(-4,20,40)}</g>`);}
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
    s+=aki(on(8)&&!on(9)?'think':(on(4)&&!on(5)?'point':'present'),on(8)&&!on(9)?'worry':'happy');
    const gatesScene=p=>{let g=cardGround(580,250,1260,570,708,'#cfe0c8',p);
      g+=pop(900,640,at(2,.5,.3),gateSmall(900,720,t))+pop(1450,640,at(2,.5,1.4),gateBig(1450,720,t));
      g+=tag(900,780,'届出  民泊新法',at(2,.4,2.6),G,'#fff',34)+tag(1450,780,'許可  旅館業',at(2,.4,4.2),T,'#fff',34);
      g+=plant(680,735,.9,t)+plant(1790,735,.9,t+1);
      return g};
    if(on(0)&&!on(2)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(0,.4));
      s+=fade(at(0,.5,.3),`<text x="1210" y="336" text-anchor="middle" font-size="48" font-weight="900" fill="${DG}">お金をもらって、人を泊める</text>`);
      s+=pop(1380,520,at(0,.5,.6),inn(1380,728,.72,{sign:'宿',t,lit:.7,case:1,post:1,bike:1}));
      s+=pop(780,560,at(0,.5,1.4),`<g transform="translate(780,560)"><ellipse cx="0" cy="130" rx="90" ry="12" fill="#000" opacity=".15"/>${coin(-30,100,52)}${coin(40,60,44)}${coin(-4,20,40)}${coin(46,128,38)}</g>`);
      s+=fade(at(0,.4,2.6),`<path d="M880 560 H1060" stroke="${T}" stroke-width="14" stroke-linecap="round" stroke-dasharray="26 16" stroke-dashoffset="${-t*40}"/><path d="M1060 530 L1110 560 L1060 590Z" fill="${T}"/>`);
      s+=stampX(1000,410,'手続きが要る',at(0,.3,5.2),RED,52,-5);
      for(let c=0;c<3;c++){const f=((t*.5+c/3)%1);s+=`<g opacity="${Math.sin(f*Math.PI)}">${sparkle(1000+c*120,470-f*60,.7,t,c)}</g>`}
    }
    if(on(2)&&!on(4))s+=gatesScene(1);
    if(on(4)&&!on(5)){const f=seg(lt,L[4]+1.4,L[4]+2.1),oldp=f<.5,sc=oldp?1-2*f:(f-.5)*2,page=(m)=>`<rect x="-160" y="6" width="320" height="350" rx="20" fill="#000" opacity=".14"/><rect x="-160" y="0" width="320" height="350" rx="20" fill="#fff" stroke="#dfe6dd" stroke-width="3"/><path d="M-160 20 a20 20 0 0 1 20 -20 h280 a20 20 0 0 1 20 20 v84 h-320z" fill="${T}"/><circle cx="-100" cy="-2" r="10" fill="#fff" stroke="#999"/><circle cx="100" cy="-2" r="10" fill="#fff" stroke="#999"/><text x="0" y="72" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">2018年</text><text x="0" y="250" text-anchor="middle" font-size="150" font-weight="900" fill="${DG}">${m}</text>`;
      s+=card(600,250,1240,540,`<text x="1220" y="330" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">民泊新法 ＝ 住宅宿泊事業法</text>`,at(4,.4));
      s+=pop(840,570,at(4,.5,.4),`<g transform="translate(840,560)">${box(-170,-130,340,260,26)}<path d="M-110 -70 h220 M-110 -30 h220 M-110 10 h150" stroke="#9fb5a8" stroke-width="10" stroke-linecap="round"/>${icon(90,70,44,'doc',G,'#fff',1)}</g>`);
      s+=`<g transform="translate(1400,350) scale(1,${Math.max(.02,sc)})">${page(oldp?'5月':'6月')}</g>`;
      s+=tag(1400,740,'2018年6月 施行',at(4,.4,2.4),G,'#fff',36);
      if(f>=1)s+=sparkle(1560,380,1.1,t,0)+sparkle(1240,420,.8,t,2);}
    if(on(5)&&!on(7)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(5,.4));
      s+=fade(at(5,.5,.2),`<text x="1210" y="336" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">旅館業法の許可（小さな宿向けは簡易宿所）</text>`);
      s+=pop(880,560,at(5,.5,.5),inn(880,728,.62,{sign:'簡易宿所',t,lit:.7,case:1}));
      s+=pop(1450,560,at(5,.5,2.4),office(1450,728,.78,'保健所',G));
      s+=fade(at(5,.4,3.4),`<path d="M1130 560 H1210" stroke="${T}" stroke-width="12" stroke-linecap="round" stroke-dasharray="22 14" stroke-dashoffset="${-t*40}"/>`);
      s+=hanko(1120,470,'許可',seg(lt,L[5]+(5.4*K),L[5]+(5.4*K)+.35));}
    if(on(7)&&!on(8)){
      s+=card(600,250,1240,540,`<text x="1220" y="330" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">特区民泊 ＝ 国が決めた区域だけ</text><path d="M720 640 Q660 560 720 500 Q780 430 860 450 Q920 360 1020 380 Q1080 330 1160 380 Q1240 360 1280 430 Q1360 450 1340 530 Q1420 560 1380 640 Q1260 700 1120 680 Q980 720 860 690 Q780 700 720 640Z" fill="#cfe5cf" stroke="#9fc4a8" stroke-width="6"/><path d="M780 600 Q860 560 940 610 M1100 470 Q1180 440 1260 500" stroke="#b6d4b8" stroke-width="10" fill="none" stroke-linecap="round"/>`,at(7,.4));
      s+=pop(1000,545,at(7,.5,.8),`<ellipse cx="1000" cy="545" rx="120" ry="84" fill="url(#pHatch)" stroke="${G}" stroke-width="7" stroke-dasharray="16 10"/><g transform="translate(1000,505)"><path d="M0 0 C-30 -30 -36 -66 0 -78 C36 -66 30 -30 0 0Z" fill="${T}"/><circle cx="0" cy="-48" r="11" fill="#fff"/></g>`);
      s+=tag(1580,520,'今日は扱いません',at(7,.4,2.8),'#9aa59d','#fff',34);
      s+=tag(1580,420,'特区民泊',at(7,.4,.4),G,'#fff',40);}
    if(on(8)&&!on(9))s+=gatesScene(1);
    if(on(8)&&!on(9))s+=qbubble('q1','どっちも民泊でしょ？',at(8,.4),t);
    if(on(9)){
      [['1','泊められる日数',G],['2','許可の条件','#3d8a6a'],['3','選ぶ決め手',T]].forEach(([n,w,c],k)=>{const x=640+k*400;s+=card(x,380,360,300,`<circle cx="${x+180}" cy="470" r="52" fill="${c}"/><text x="${x+180}" y="490" text-anchor="middle" font-size="58" font-weight="900" fill="#fff">${n}</text><text x="${x+180}" y="600" text-anchor="middle" font-size="${w.length>6?36:42}" font-weight="900" fill="${DG}">${w}</text>`,at(9,.4,[2.8,3.7,4.6][k]))});
      s+=tag(1200,330,'違いは、3つ',at(9,.4,2.4),Y,DG,44);}
  }
  if(i===2){ // 違い① 泊められる日数
    s+=aki(on(12)&&!on(13)?'think':(on(5)&&!on(6)?'point':'present'),on(12)&&!on(13)?'worry':'happy');
    if(on(1)&&!on(3)){
      const rows=[['届出',180,G,'年180日まで','#b5603a'],['許可',365,T,'日数の上限なし','#2e6b47']];
      s+=card(600,250,1240,560,'',at(1,.4));
      rows.forEach(([w,v,c,l,rc],k)=>{const y=470+k*190,g=eo(at(1,1.1,.4+k*1.2));
        s+=`<g opacity="${at(1,.3,.3+k*1.2)}">${inn(720,y+60,.34,{sign:'',roof:rc,noren:c,t,lit:.6,chim:0})}<text x="885" y="${y-2}" text-anchor="middle" font-size="32" font-weight="900" fill="${c}">${k?'旅館業':'民泊新法'}</text><text x="885" y="${y+34}" text-anchor="middle" font-size="30" font-weight="900" fill="${c}">（${w}）</text><rect x="960" y="${y-34}" width="800" height="68" rx="34" fill="#e3ebe3"/><rect x="960" y="${y-34}" width="${800*v/365*g}" height="68" rx="34" fill="${k?'url(#gO)':'url(#gG)'}"/><rect x="976" y="${y-26}" width="${Math.max(0,800*v/365*g-32)}" height="12" rx="6" fill="#fff" opacity=".26"/>${g>.9?`<text x="${960+800*v/365-30}" y="${y+14}" text-anchor="end" font-size="38" font-weight="900" fill="#fff">${l}</text>`:''}</g>`});}
    if(on(3)&&!on(5)){
      const show=Math.floor(365*seg(lt,L[3]+.3*K,L[3]+3.6*K)),dd=Math.min(show,365);
      s+=card(600,250,1240,545,`<text x="1220" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">1年 ＝ 365日（1マス ＝ 1日）</text>${cal(684,348,28,dd,180)}${shutter(684,348,28,180,seg(lt,L[3]+2.2,L[3]+2.8),'ここから先は営業できない',34)}`,at(3,.4));
      s+=fade(at(3,.4,3.6),`<rect x="660" y="672" width="780" height="92" rx="46" fill="url(#gO)"/><text x="1050" y="737" text-anchor="middle" font-size="50" font-weight="900" fill="#fff">180日 ÷ 365日 ＝ 約49%</text>`);
      s+=tag(1680,715,'地域で短いことも',at(3,.4,5.6),Y,DG,28);
      if(show<365&&show>0&&show<=180)s+=`<g transform="translate(${684+((show-1)%37)*28+14},${348+Math.floor((show-1)/37)*28-10})"><path d="M0 0 l-14 -26 h28z" fill="${T}"/></g>`;}
    if(on(5)&&!on(6)){
      const nights=[1,2,3,8,9,10,15,16,17,22,23,24,29,30];
      s+=card(600,250,1240,545,`<text x="1220" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">稼働率 ＝ 泊まった日 ÷ 全部の日</text>`,at(5,.4));
      s+=pop(880,560,at(5,.5,.5),`<g transform="translate(740,400)">${box(0,0,300,300,24)}<rect x="0" y="0" width="300" height="52" rx="24" fill="${T}"/><text x="150" y="38" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">ある月</text>${Array.from({length:35},(_,d)=>{const c=d%7,r=Math.floor(d/7),on1=nights.includes(d+1)&&d<30,x=16+c*38,y=70+r*44;return `<rect x="${x}" y="${y}" width="32" height="36" rx="7" fill="${on1?(at(5,.3,1+ (d%7)*.3)>0?T:'#e4ece4'):'#e4ece4'}"/>`}).join('')}</g>`);
      s+=fade(at(5,.5,2.2),`<text x="1180" y="510" font-size="46" font-weight="900" fill="${T}">泊まった日（オレンジ）</text><text x="1180" y="582" font-size="46" font-weight="900" fill="${DG}">÷ その月の日数</text><text x="1180" y="654" font-size="46" font-weight="900" fill="${G}">＝ 稼働率</text>`);}
    if(on(6)&&!on(7)){
      s+=card(600,250,1240,540,`<text x="1220" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">たとえば、稼働率が49%の宿は</text>`,at(6,.4));
      s+=pop(900,470,at(6,.4,.8),formulaChip(700,420,400,'365日',G,'#fff',44));
      s+=fade(at(6,.3,1.4),`<text x="1180" y="490" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">×</text>`);
      s+=pop(1420,470,at(6,.4,1.8),formulaChip(1260,420,320,'49%',T,'#fff',44));
      s+=pop(1220,650,at(6,.5,3.4),`<rect x="760" y="590" width="920" height="110" rx="55" fill="url(#gO)"/><text x="1220" y="665" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">＝ 約180日（届出の天井）</text>`);
      s+=sparkle(1640,430,1,t,0);}
    if(on(7)&&!on(8)){
      const months=['1','2','3','4','5','6','7','8','9','10','11','12'];
      const rowsM=[['ゆっくりの宿',0.5,G],['混む宿・1年中の宿',1.0,T]];
      s+=card(600,250,1240,560,`<text x="1220" y="312" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">使った日数が、180日に近づくスピード</text>`,at(7,.4));
      rowsM.forEach(([w,sp,c],k)=>{const y=420+k*190,g=seg(lt,L[7]+(1+k*.4)*K,L[7]+(5+k*.4)*K);const limitM=sp>.9?8.2:12;const fillM=Math.min(g*12,limitM),done=sp>.9&&fillM>=limitM;
        let r=`<text x="680" y="${y-46}" font-size="34" font-weight="900" fill="${DG}">${w}</text>`;
        months.forEach((m,mi)=>{const x=680+mi*90,f=(sp>.9?1:.5)*clamp(fillM-mi),cut=mi+1>limitM&&done;r+=`<rect x="${x}" y="${y-30}" width="82" height="72" rx="10" fill="${cut?'#2a2f2c':'#e4ece4'}"/>${f>0&&!cut?`<rect x="${x}" y="${y-30+72*(1-f)}" width="82" height="${72*f}" rx="10" fill="${c}"/>`:''}${cut?`<rect x="${x}" y="${y-30}" width="82" height="72" rx="10" fill="url(#pSlat)"/>`:''}<text x="${x+41}" y="${y+78}" text-anchor="middle" font-size="26" font-weight="900" fill="#4a5a52">${m}月</text>`});
        s+=r;
        if(k===1&&done)s+=pop(1220,y+120,seg(lt,L[7]+5.8*K,L[7]+6.3*K),`<rect x="900" y="${y+96}" width="640" height="56" rx="28" fill="${RED}"/><text x="1220" y="${y+136}" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">180日に着いたら、そこで終わり</text>`)});
      s+=stampX(1690,720,'イメージ',at(7,.3,.6),'#8a8f98',34,6);}
    if(on(8)&&!on(10)){const g=eo(at(8,1.6,.9));
      s+=card(600,250,1240,540,`<text x="1220" y="335" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">私たちの宿：開業から約8.5か月の平均</text>${gauge(700,480,1040,g)}`,at(8,.4));
      s+=stampX(1700,330,'一例',at(9,.3,3),T,44,6);
      if(g>.99)s+=sparkle(1320,500,1.1,t,0)+sparkle(1500,470,.8,t,3);
      s+=fade(at(9,.5,.6),`<text x="1220" y="760" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">この水準が1年続くと：365日 × 0.53 ＝ 約193日</text>`);}
    if(on(10)&&!on(11)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(10,.4));
      s+=pop(1000,560,at(10,.5,.4),inn(1000,728,.74,{sign:'許可',roof:'#2e6b47',noren:T,t,lit:.85,case:1,post:1,signc:'#2f2a22'}));
      const rot=-40+Math.min(1,seg(lt,L[10]+2.6*K,L[10]+3.4*K))*90;
      s+=pop(1560,520,at(10,.5,1.6),`<g transform="translate(1560,520)"><circle r="104" fill="#000" opacity=".1" transform="translate(5,8)"/><circle r="104" fill="url(#gD)"/><circle r="84" fill="#e8ece6"/><circle r="84" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/><circle r="22" fill="#2a2f2c"/><rect x="-6" y="0" width="12" height="40" rx="5" fill="#2a2f2c"/>${keyp(0,0,.85,rot)}</g>`);
      s+=tag(1560,690,'1年中、営業',at(10,.4,4.2),G,'#fff',38);
      s+=tag(1200,330,'簡易宿所の許可を選んだ',at(10,.4,6),Y,DG,40);}
    if(on(11)&&!on(12)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(11,.4));
      s+=pop(880,560,at(11,.5,.3),inn(880,728,.66,{sign:'届出',t,lit:.65,case:1}));
      s+=fade(at(11,.5,.8),`<text x="1420" y="400" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">ときどき使う家</text><text x="1420" y="470" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">まず小さく試す</text>`);
      s+=pop(1420,590,at(11,.5,3.2),`<rect x="1150" y="540" width="540" height="100" rx="50" fill="url(#gG)"/><text x="1420" y="606" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">上限は気にならない</text>`);
      s+=sparkle(1600,420,1,t,0);}
    if(on(12)&&!on(14)){
      s+=cardGround(600,250,1240,560,728,'#cfe0c8',at(12,.4));
      s+=pop(860,560,at(12,.5,.3),inn(860,728,.6,{sign:'届出',t,lit:.65,case:1}));
      s+=pop(1440,560,at(12,.5,.8),inn(1440,728,.68,{sign:'許可',t,lit:.85,roof:'#2e6b47',noren:T,post:1,signc:'#2f2a22'}));
      s+=q(1150,540,130,t,0);
      s+=tag(1150,330,'自分の宿は、どっち？',at(12,.4,1.6),Y,DG,44);}
    if(on(12)&&!on(13))s+=qbubble('q6','届出でもいいの？',at(12,.4),t);
    if(on(14))s+=pop(1200,500,at(14,.4),`<rect x="640" y="388" width="1120" height="240" rx="120" fill="#000" opacity=".14"/><rect x="640" y="380" width="1120" height="240" rx="120" fill="url(#gO)"/><rect x="700" y="394" width="1000" height="50" rx="25" fill="#fff" opacity=".18"/><text x="1200" y="480" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">日数だけなら、許可が有利</text><text x="1200" y="570" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">でも、許可には重い条件がある</text>`)+sparkle(700,380,1,t,0)+sparkle(1720,620,1.1,t,2);
  }
  if(i===3){ // 違い② 手続きと建物
    s+=aki(on(10)&&!on(11)?'point':(on(7)&&!on(8)?'think':(on(3)?'point':'present')),on(7)&&!on(8)?'worry':'happy');
    s+=hdr('違い ②','許可の条件と手間',at(0,.4),'#3d8a6a');
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
    if(on(1)&&!on(2)){
      s+=cardGround(580,250,1260,570,708,'#cfe0c8',at(1,.4));
      s+=pop(900,560,at(1,.5,.3),office(900,728,.78,'都道府県',G))+pop(1450,560,at(1,.5,2.2),office(1450,728,.78,'保健所',T));
      s+=tag(900,780,'届出の窓口',at(1,.4,.8),G,'#fff',32)+tag(1450,780,'許可の窓口',at(1,.4,2.6),T,'#fff',32);
      const f=((t*.5)%1);s+=`<g opacity="${Math.sin(f*Math.PI)}" transform="translate(${700+f*200},${470-Math.sin(f*Math.PI)*40})">${icon(0,0,34,'doc',Y,DG,.8)}</g>`;
      s+=fade(at(1,.4,3),`<g transform="translate(${1250+((t*.5+.5)%1)*200},470)" opacity="${Math.sin(((t*.5+.5)%1)*Math.PI)}">${icon(0,0,34,'doc',T,'#fff',.8)}</g>`,0);}
    if(on(2)&&!on(3)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(2,.4));
      s+=pop(830,560,at(2,.5,.3),inn(830,728,.7,{sign:'住宅',t,lit:.7,case:1,bike:1}));
      [['台所','kitchen'],['浴室','bath'],['トイレ','toilet'],['洗面','sink']].forEach(([w,pc],k)=>{const x=1130+(k%2)*350,y=330+Math.floor(k/2)*220,o=[2.6,3.8,5,6.2][k];
        s+=tileP(x,y,320,190,at(2,.4,o*.9),PIC[pc](x+160,y+70),w,at(2,.3,o*.9+.5))});}
    if(on(3)&&!on(4)){
      s+=cardGround(580,250,1260,570,728,'#cfe0c8',at(3,.4));
      s+=pop(830,560,at(3,.5,.3),inn(830,728,.7,{sign:'簡易宿所',t,lit:.8,roof:'#2e6b47',noren:T,signc:'#2f2a22'}));
      [['図面','plan'],['火災報知器','alarm'],['誘導灯','exit'],['保健所の確認','stampP']].forEach(([w,pc],k)=>{const x=1130+(k%2)*350,y=330+Math.floor(k/2)*220,o=[2.2,3.4,5,7.2][k];
        s+=tileP(x,y,320,190,at(3,.4,o*.9),PIC[pc](x+160,y+66),w,0)});}
    if(on(4)&&!on(6)){
      s+=card(600,250,1240,550,`<text x="1000" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">広さの目安（1人あたり）</text>`,at(4,.4));
      [0,1,2,3].forEach(k=>{const x=700+k*150;s+=pop(x+68,470,at(4,.4,.8+k*.5),`<rect x="${x}" y="400" width="136" height="136" rx="10" fill="#cfe3a8"/><rect x="${x}" y="400" width="136" height="136" rx="10" fill="url(#pTatami)"/><rect x="${x}" y="400" width="136" height="136" rx="10" fill="none" stroke="#6f8a3c" stroke-width="5"/>${person2(x+68,532,.8,[G,T,'#3d6a8a','#b8862f'][k],'#2b2422')}<text x="${x+68}" y="430" text-anchor="middle" font-size="28" font-weight="900" fill="${DG}">3.3㎡</text>`)});
      s+=fade(at(4,.5,4.6),`<path d="M700 566 v14 h586 v-14" stroke="${T}" stroke-width="7" fill="none" stroke-linecap="round"/><text x="993" y="650" text-anchor="middle" font-size="62" font-weight="900" fill="${T}">4人 ＝ 13.2㎡</text>`);
      s+=pop(1560,440,at(4,.4,.4),formulaChip(1340,390,440,'10人未満：1人 3.3㎡',G,'#fff',30));
      s+=pop(1560,560,at(4,.4,9.4*.9),formulaChip(1340,510,440,'10人以上：33㎡以上',T,'#fff',30));
      if(on(5))s+=tag(1200,744,'届出の宿も、1人 3.3㎡以上',at(5,.4,.4),Y,DG,34);}
    if(on(6)&&!on(8)){
      s+=card(600,250,1240,550,`<rect x="660" y="320" width="520" height="420" rx="22" fill="#e9efe4"/><rect x="660" y="320" width="270" height="420" rx="22" fill="url(#pHatch)"/><rect x="660" y="320" width="270" height="420" rx="22" fill="none" stroke="${G}" stroke-width="5" stroke-dasharray="14 9"/><path d="M930 320 V740 M660 530 H1180" stroke="#cfd8cb" stroke-width="22"/>${[[960,350],[1040,350],[1110,350],[960,570],[1040,570],[1110,570],[960,650],[1110,650]].map(([bx0,by0],k)=>`<rect x="${bx0}" y="${by0}" width="52" height="${k<3?70:60}" rx="6" fill="${['#e7b36a','#d98a6a','#9fc4d8'][k%3]}"/>`).join('')}<rect x="690" y="340" width="210" height="46" rx="23" fill="${G}"/><text x="795" y="373" text-anchor="middle" font-size="26" font-weight="900" fill="#fff">住居専用地域</text><g transform="translate(795,520)"><path d="M-44 0 L0 -40 L44 0 V40 H-44Z" fill="${T}"/><rect x="-12" y="8" width="24" height="32" fill="#fff"/></g>`,at(6,.4));
      const rowP=(y,name,c,sym,sc,txt,o)=>pop(1510,y,at(6,.4,o),`<rect x="1220" y="${y-52}" width="560" height="120" rx="30" fill="#f3f7f1" stroke="#dfe8dc" stroke-width="3"/><rect x="1236" y="${y-36}" width="170" height="52" rx="26" fill="${c}"/><text x="1321" y="${y}" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">${name}</text><circle cx="1700" cy="${y+8}" r="42" fill="${sc}"/><text x="1700" y="${y+30}" text-anchor="middle" font-size="64" font-weight="900" fill="#fff">${sym}</text><text x="1300" y="${y+50}" font-size="28" font-weight="900" fill="${DG}">${txt}</text>`);
      s+=rowP(420,'届出',G,'△','#d99a2b','地域のルールで制限あり',2.4)+rowP(610,'許可',T,'×',RED,'原則、営業できない',5.8);
      if(on(7))s+=qbubble('q3','許可は難しいのか…',at(7,.4),t);}
    if(on(8)&&!on(10)){
      s+=card(600,250,1240,550,'',at(8,.4));
      [[420,'届出','家主が不在 → 管理業者へ委託',G,0],[620,'許可','自分たちで管理体制',T,1]].forEach(([y,w,txt,c,k])=>{const o=[1.4,5.4][k];
        s+=pop(740,y,at(8,.4,o),`<g>${inn(740,y+78,.3,{sign:w,roof:k?'#2e6b47':'#b5603a',noren:c,t,lit:.6,chim:0})}</g>`);
        s+=fade(at(8,.4,o+.6),`<path d="M880 ${y} H1010" stroke="${c}" stroke-width="10" stroke-linecap="round" stroke-dasharray="20 12" stroke-dashoffset="${-t*40}"/><path d="M1010 ${y-22} L1048 ${y} L1010 ${y+22}Z" fill="${c}"/>`,0);
        s+=pop(1130,y,at(8,.4,o+.8),k?`${person2(1100,y+50,.9,G,'#2b2422')}${person2(1170,y+50,.9,T,'#4a3324')}`:`${icon(1130,y-6,50,'key',c,'#fff',1)}<text x="1130" y="${y+82}" text-anchor="middle" font-size="28" font-weight="900" fill="${DG}">管理業者</text>`);
        s+=fade(at(8,.4,o+1.2),`<text x="1260" y="${y+14}" font-size="36" font-weight="900" fill="${c}">${txt}</text>`)});
      if(on(9))s+=tag(1220,755,'住んでいない人ほど、管理の形を先に決める',at(9,.4,.4),Y,DG,32);}
    if(on(10)&&!on(11)){
      s+=cardGround(600,250,1240,560,720,'#cfe0c8',at(10,.4));
      s+=pop(800,540,at(10,.5,.3),inn(800,720,.66,{sign:'宿',t,lit:.7,case:1}));
      const g=eo(at(10,1,.8));
      s+=`<g opacity="${g}"><rect x="1100" y="360" width="520" height="${340*g}" rx="14" fill="#e6eee0" stroke="${G}" stroke-width="6"/><rect x="1100" y="360" width="520" height="${340*g}" rx="14" fill="url(#pTatami)"/><path d="M1100 740 H1620 M1100 725 v30 M1620 725 v30" stroke="${T}" stroke-width="6"/><text x="1360" y="545" text-anchor="middle" font-size="82" font-weight="900" fill="${DG}">200㎡</text></g>`;
      s+=stampX(1360,310,'超えると',at(10,.3,3),RED,44,-4);
      s+=tag(1220,780,'用途変更の確認申請',at(10,.4,3.8),T,'#fff',34);}
    if(on(11)&&!on(12)){
      s+=card(600,250,1240,550,`<path d="M740 430 H1670" stroke="#cfd8cb" stroke-width="12" stroke-linecap="round"/><path d="M740 430 H${740+930*eo(at(11,6,.6))}" stroke="${G}" stroke-width="12" stroke-linecap="round"/>`,at(11,.4));
      [['開業の2か月前','保健所・消防署に相談'],['自分で申請','書類をそろえる'],['1〜2か月','申請から許可まで'],['許可番号','予約を受けられる']].forEach(([a,b],k)=>{const x=740+k*310,o=[.8,3.4,6.0,9.0][k];
        s+=pop(x,430,at(11,.4,o),`<circle cx="${x}" cy="436" r="34" fill="#000" opacity=".12"/><circle cx="${x}" cy="430" r="34" fill="${[G,'#3d8a6a',Y,T][k]}"/><text x="${x}" y="445" text-anchor="middle" font-size="40" font-weight="900" fill="${k==2?DG:'#fff'}">${k+1}</text><text x="${x}" y="510" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">${a}</text><text x="${x}" y="552" text-anchor="middle" font-size="26" font-weight="700" fill="#4a5a52">${b}</text>`)});
      s+=pop(1250,670,at(11,.5,9.4),`<rect x="840" y="590" width="820" height="170" rx="26" fill="#000" opacity=".08" transform="translate(0 6)"/><rect x="840" y="590" width="820" height="170" rx="26" fill="#fff" stroke="#e1e8df" stroke-width="3"/><text x="880" y="640" font-size="36" font-weight="900" fill="#ff5a5f">Airbnb</text><rect x="880" y="660" width="420" height="60" rx="12" fill="#eef3ee"/><text x="900" y="702" font-size="30" font-weight="700" fill="#4a5a52">許可番号：●●●●●●</text><g transform="translate(1330,690)"><circle r="22" fill="${G}"/><path d="M-10 0 l8 9 l14 -18" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g><rect x="1410" y="650" width="210" height="64" rx="32" fill="url(#gO)"/><text x="1515" y="692" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">予約OK</text>`);}
    if(on(12)){
      s+=card(640,270,1160,500,`${icon(900,470,110,'search',G,'#fff',2.2)}<text x="1360" y="450" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">下田の1件の経験</text><text x="1360" y="520" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">どこでも同じとは限らない</text><rect x="760" y="620" width="880" height="96" rx="48" fill="url(#gO)"/><text x="1200" y="685" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">必ず、地元の窓口で確認</text>`,at(12,.4));
      s+=sparkle(1500,350,1,t,1);}
  }
  if(i===4){ // 違い③ 向く人は誰か
    s+=aki(on(5)?'present':(on(3)&&!on(4)?'think':'point'),on(3)&&!on(4)?'worry':'happy');
    s+=hdr('違い ③','届出か許可かの決め手',at(0,.4),T);
    if(on(1)&&!on(4)){
      const hl=on(2)?2:1,x0=580,y0=250,w=1280,h=570,sway=Math.sin(t*1.2)*3;
      let g=pop(1220,535,at(1,.5),`${bx(x0,y0,w,h)}<defs><linearGradient id="fkS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe3f3"/><stop offset=".6" stop-color="#fdf1d6"/></linearGradient></defs><clipPath id="fk"><rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="28"/></clipPath><g clip-path="url(#fk)"><rect x="${x0}" y="${y0}" width="${w}" height="${h}" fill="url(#fkS)"/>
        <circle cx="1560" cy="340" r="52" fill="#fff6c9" opacity=".95"/><path d="M${x0} 560 Q760 440 980 540 Q1160 460 1340 540 Q1560 450 1860 540 V820 H${x0}Z" fill="#b9dcc0"/><path d="M${x0} 620 Q800 540 1000 610 Q1200 540 1400 610 Q1640 540 1860 600 V820 H${x0}Z" fill="#a6d0a8"/><rect x="${x0}" y="640" width="${w}" height="180" fill="#9ac79a"/>
        <g opacity=".75" transform="translate(${((t*8)%1500)+600},300)" fill="#fff"><ellipse rx="80" ry="22"/><ellipse cx="46" cy="-14" rx="52" ry="26"/></g>
        <path d="M1110 820 L1280 820 L1520 590 L1440 590 L1195 760 L930 590 L860 590Z" fill="#d8c7a0"/><path d="M1110 820 L1280 820 L1195 735Z" fill="#d8c7a0"/><path d="M1125 820 L1195 756 L1265 820" stroke="#fff" stroke-width="5" fill="none" opacity=".6"/>
        <path d="M1195 740 L900 600 M1195 740 L1480 600" stroke="#fff" stroke-width="5" stroke-dasharray="20 18" stroke-dashoffset="${-t*30}" opacity=".7"/>
        <g transform="translate(790,560)"><ellipse cx="0" cy="12" rx="70" ry="10" fill="#000" opacity=".16"/><rect x="-6" y="-70" width="12" height="80" rx="4" fill="#7a5a3c"/><circle cx="${sway}" cy="-100" r="46" fill="#f4b6c9"/><circle cx="${-30+sway}" cy="-76" r="32" fill="#f7c8d6"/><circle cx="${30+sway}" cy="-80" r="34" fill="#f09ab5"/>${[0,1,2,3].map(k=>`<circle cx="${((k*57+t*30)%120)-60}" cy="${((k*41+t*40)%100)-20}" r="4" fill="#f9d3df" opacity=".8"/>`).join('')}</g>
        <g transform="translate(1590,560)"><ellipse cx="0" cy="12" rx="70" ry="10" fill="#000" opacity=".16"/><rect x="-6" y="-70" width="12" height="80" rx="4" fill="#7a5a3c"/><circle cx="${sway}" cy="-100" r="46" fill="#e0693a"/><circle cx="${-30+sway}" cy="-76" r="32" fill="#e9893f"/><circle cx="${30+sway}" cy="-80" r="34" fill="#cf4b2f"/></g>
        ${inn(880,600,.2,{sign:'',t,lit:.6,chim:0,roof:'#b5603a',noren:G})}${inn(1510,600,.26,{sign:'',t,lit:.9,roof:'#2e6b47',noren:T})}
        <g transform="translate(1195,740)"><ellipse cx="0" cy="8" rx="46" ry="8" fill="#000" opacity=".2"/><rect x="-7" y="-150" width="14" height="156" rx="4" fill="#7a5a3c"/><rect x="-7" y="-150" width="14" height="156" fill="url(#pWood)"/><path d="M-12 -142 h-130 l-26 28 l26 28 h130z" fill="${G}"/><path d="M12 -92 h130 l26 28 l-26 28 h-130z" fill="${T}"/><text x="-80" y="-102" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">届出</text><text x="80" y="-52" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">許可</text></g>
        <rect x="${x0}" y="${y0}" width="${hl==1?640:0}" height="${h}" fill="none"/>${hl==2?`<rect x="${x0}" y="${y0}" width="630" height="${h}" fill="#fff" opacity=".5"/>`:`<rect x="1190" y="${y0}" width="670" height="${h}" fill="#fff" opacity=".5"/>`}</g>`);
      s+=g;
      const L1=[['ときどき使う家',.4],['まず試す',2.2],['住居専用地域',4]],R1=[['通年',.4],['稼働日数で回収',2.4],['一棟貸しを本格運営',4.4]];
      L1.forEach(([w,o],k)=>{if(on(1))s+=tag(735,636+k*58,w,at(1,.4,o),G,'#fff',30)});
      R1.forEach(([w,o],k)=>{if(on(2))s+=tag(1675,636+k*58,w,at(2,.4,o),T,'#fff',30)});}
    if(on(3)&&!on(4))s+=qbubble('q4','あとで変えられる？',at(3,.4),t);
    if(on(4)&&!on(5)){
      s+=cardGround(600,250,1240,560,730,'#cfe0c8',at(4,.4));
      s+=pop(1180,540,at(4,.5,.3),`<g transform="translate(1180,730)"><ellipse cx="0" cy="8" rx="320" ry="16" fill="#000" opacity=".16"/><rect x="-300" y="-170" width="600" height="170" rx="10" fill="#b5835a"/><rect x="-300" y="-170" width="600" height="170" fill="url(#pWood)"/><rect x="-316" y="-190" width="632" height="30" rx="8" fill="#8a5a3c"/><rect x="-250" y="-330" width="500" height="150" rx="10" fill="#bfe0ef" opacity=".7"/><rect x="-250" y="-330" width="500" height="150" rx="10" fill="none" stroke="#fff" stroke-width="6"/><path d="M-250 -330 l140 0 l-90 150 l-50 0z" fill="#fff" opacity=".35"/><g transform="translate(-130,-186)">${person2(0,0,1.15,G,'#2b2422')}</g><g transform="translate(150,-186)">${person2(0,0,1.15,'#3d6a8a','#4a3324')}</g><rect x="-170" y="-384" width="340" height="56" rx="28" fill="${G}"/><text x="0" y="-345" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">窓口</text></g>`);
      s+=tag(1200,298,'自治体と物件によって違う',at(4,.4,.6),Y,DG,40);
      s+=stampX(1500,480,'窓口で確認',at(4,.3,3.4),RED,48,6);}
    if(on(5)&&!on(6)){
      s+=card(600,250,1240,550,'',at(5,.4));
      s+=pop(900,470,at(5,.5,.3),`<rect x="660" y="390" width="480" height="200" rx="30" fill="#f3f7f1"/><text x="900" y="470" text-anchor="middle" font-size="42" font-weight="900" fill="#8a8f98">どちらが儲かる？</text>${coin(900,540,34)}<path d="M700 410 L1100 580 M1100 410 L700 580" stroke="${RED}" stroke-width="12" stroke-linecap="round"/>`);
      s+=pop(1500,470,at(5,.5,2.4),`<rect x="1260" y="390" width="480" height="200" rx="30" fill="#e8f3ea" stroke="${G}" stroke-width="5"/><text x="1500" y="470" text-anchor="middle" font-size="42" font-weight="900" fill="${G}">自分の目的に合う？</text><g transform="translate(1500,540)"><circle r="34" fill="${G}"/><path d="M-14 0 l10 12 l20 -24" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`);
      s+=sparkle(1700,420,1,t,0);}
    if(on(6)&&!on(7)){
      s+=pop(900,480,at(6,.5,.2),`${bx(640,300,480,380,30)}<rect x="640" y="300" width="480" height="96" rx="30" fill="${G}"/><text x="880" y="365" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">届出</text><text x="880" y="500" text-anchor="middle" font-size="64" font-weight="900" fill="${G}">お試し向き</text>${plant(800,640,.8,t)}${suitcase(960,640,.8)}`);
      s+=pop(1500,480,at(6,.5,2.2),`${bx(1260,300,480,380,30)}<rect x="1260" y="300" width="480" height="96" rx="30" fill="${T}"/><text x="1500" y="365" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">許可</text><text x="1500" y="500" text-anchor="middle" font-size="64" font-weight="900" fill="${T}">本業向き</text>${keyp(1500,600,.7,-20)}`);
      s+=sparkle(1700,330,1,t,2)+sparkle(1090,340,.8,t,0);}
    if(on(7)){
      const rows=[['日数','年180日まで','日数の上限なし'],['建物','住宅のまま','宿の基準が厳しい'],['向く人','試す・ときどき','通年・本格運営']];
      s+=card(620,250,1200,540,`<rect x="920" y="290" width="400" height="64" rx="32" fill="${G}"/><text x="1120" y="335" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">届出</text><rect x="1360" y="290" width="400" height="64" rx="32" fill="${T}"/><text x="1560" y="335" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">許可</text>`,at(7,.4));
      rows.forEach(([a,b,c],k)=>{const y=400+k*125;s+=pop(1190,y+50,at(7,.4,[2,3.8,7.2][k]),`<rect x="650" y="${y}" width="1130" height="104" rx="26" fill="#f3f7f1"/><rect x="662" y="${y+12}" width="210" height="80" rx="22" fill="${DG}"/><text x="767" y="${y+66}" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">${a}</text><text x="1120" y="${y+66}" text-anchor="middle" font-size="36" font-weight="900" fill="${G}">${b}</text><text x="1560" y="${y+66}" text-anchor="middle" font-size="36" font-weight="900" fill="${T}">${c}</text>`)});}
  }
  if(i===5){ // 落とし穴 4つ
    s+=aki(on(7)?'point':(on(3)&&!on(5)?'think':'present'),on(3)&&!on(5)?'worry':'happy');
    s+=hdr('','失敗しやすい点 4つ',at(0,.4),RED);
    const drop=(p,inner,cx,cy)=>{if(p<=0)return '';const dy=-(1-bk(p))*560,imp=seg(p,.78,1);return `<g opacity="${clamp(p*5)}" transform="translate(0,${dy})">${inner}</g>${p>.9&&p<1?'':''}`};
    const slots=[[590,260],[1230,260],[590,530],[1230,530]];
    const ICONS=[
      (x,y)=>`<g transform="translate(${x+110},${y+130})"><ellipse cx="0" cy="62" rx="76" ry="10" fill="#000" opacity=".16"/>${inn(0,64,.2,{sign:'',t,lit:.4,chim:0,roof:'#9a8a7a',wall:'#d8cdb8'})}<circle cx="42" cy="-24" r="36" fill="${RED}"/><path d="M28 -38 L56 -10 M56 -38 L28 -10" stroke="#fff" stroke-width="9" stroke-linecap="round"/></g>`,
      (x,y)=>`<g transform="translate(${x+110},${y+130})"><ellipse cx="0" cy="66" rx="40" ry="8" fill="#000" opacity=".16"/><rect x="-26" y="-30" width="52" height="94" rx="18" fill="#d9342b"/><rect x="-26" y="-30" width="14" height="94" rx="8" fill="#fff" opacity=".24"/><rect x="-12" y="-52" width="24" height="26" rx="4" fill="#2a2f2c"/><path d="M12 -44 q40 -4 44 30 q2 30 -14 40" stroke="#2a2f2c" stroke-width="7" fill="none"/><rect x="-22" y="0" width="44" height="34" rx="4" fill="#fff" opacity=".9"/></g>`,
      (x,y)=>`<g transform="translate(${x+110},${y+130})"><ellipse cx="0" cy="66" rx="70" ry="8" fill="#000" opacity=".14"/><rect x="-60" y="-56" width="120" height="116" rx="10" fill="#f1e2bb"/><rect x="-70" y="-70" width="140" height="24" rx="12" fill="#c9a266"/><rect x="-70" y="44" width="140" height="24" rx="12" fill="#c9a266"/><path d="M-36 -22 h72 M-36 0 h72 M-36 22 h46" stroke="#a88a58" stroke-width="7" stroke-linecap="round"/><circle cx="38" cy="30" r="17" fill="#d9342b"/></g>`,
      (x,y)=>`<g transform="translate(${x+110},${y+130})"><ellipse cx="0" cy="66" rx="80" ry="9" fill="#000" opacity=".14"/>${inn(-48,64,.14,{sign:'',t,lit:.6,chim:0})}${inn(52,64,.14,{sign:'',t,lit:.3,chim:0,roof:'#7a8a9a'})}<g transform="translate(2,-38)"><path d="M-44 -30 h88 a14 14 0 0 1 14 14 v22 a14 14 0 0 1 -14 14 h-40 l-20 20 v-20 h-28 a14 14 0 0 1 -14 -14 v-22 a14 14 0 0 1 14 -14z" fill="#fff" stroke="${RED}" stroke-width="6"/><text y="14" text-anchor="middle" font-size="44" font-weight="900" fill="${RED}">!</text></g></g>`
    ];
    const cardsT=[['買ってから','許可が取れない'],['消防設備の','費用の見落とし'],['条例による','営業の制限'],['近隣への','説明不足']];
    const startL=[2,3,5,6];
    cardsT.forEach(([a,b],k)=>{const [x,y]=slots[k],p=at(startL[k],.9,.0);if(on(startL[k])&&!on(7)){
      const extra=k===1&&on(3)?`<text x="${x+210}" y="${y+170}" font-size="32" font-weight="900" fill="${DG}">想定 約40万円</text><text x="${x+210}" y="${y+212}" font-size="36" font-weight="900" fill="${RED}">→ 約60万円（約1.5倍）</text>`:'';
      s+=drop(p,`${bx(x,y,600,250,28)}<rect x="${x}" y="${y}" width="14" height="250" rx="7" fill="${RED}"/>${ICONS[k](x,y)}<text x="${x+210}" y="${y+80}" font-size="40" font-weight="900" fill="${DG}">${a}</text><text x="${x+210}" y="${y+128}" font-size="40" font-weight="900" fill="${DG}">${b}</text>${extra}<circle cx="${x+560}" cy="${y+36}" r="26" fill="${RED}"/><text x="${x+560}" y="${y+48}" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">${k+1}</text>`);
      if(p>.82&&p<1)s+=`<g opacity="${1-seg(p,.82,1)}"><ellipse cx="${x+300}" cy="${y+256}" rx="${200+80*seg(p,.82,1)}" ry="10" fill="#fff" opacity=".6"/></g>`}});
    if(on(4)&&!on(7))s+=pop(1340,490,at(4,.3),`<g transform="rotate(-5 1340 490)"><rect x="1245" y="464" width="190" height="52" rx="26" fill="${Y}"/><text x="1340" y="500" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">個人の事例</text></g>`);
    if(on(7)){
      s+=card(600,250,1240,560,'',at(7,.4));
      s+=pop(900,420,at(7,.4,.4),`${bx(640,330,520,160,40,'#f3f7f1')}<text x="900" y="425" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">「許可なんて簡単」</text>`);
      s+=pop(1500,420,at(7,.4,2.4),`${bx(1240,330,560,160,40,'#f3f7f1')}<text x="1520" y="425" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">「届出だけで通年OK」</text>`);
      s+=stampX(1210,610,'まず疑う',at(7,.3,4.6),RED,70,-5);
      s+=tag(1210,760,'家を買う前に、役所へ相談',at(7,.4,7.4),G,'#fff',38);}
  }
  if(i===6){ // あなたの家はどっち？
    s+=aki(on(7)?'cheer':(on(4)&&!on(5)?'present':'point'));
    if(on(1)&&!on(4)){
      const cols=[
        ['1','何日泊めたいか','年180日（約49%）で足りる？',[['足りるなら','届出も候補',G],['足りないなら','許可',T]]],
        ['2','立地と広さ','住居専用地域？ 広さは？',[['住居専用地域なら','許可は原則むずかしい',RED],['基準を超える広さなら','窓口に相談',T]]],
        ['3','誰が運営するか','家主は不在になる？',[['不在になるなら','届出は管理業者へ委託',G],['許可の場合','自前の管理体制',T]]]];
      cols.forEach(([n,a,b,ans],k)=>{const x=590+k*430,dim=on(k+1)&&!on(k+2)?1:.55;
        s+=`<g opacity="${on(k+1)?1:0}">`+card(x,260,400,540,`<circle cx="${x+66}" cy="338" r="40" fill="${[G,T,'#3d8a6a'][k]}"/><text x="${x+66}" y="354" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">${n}</text><text x="${x+120}" y="352" font-size="36" font-weight="900" fill="${DG}">${a}</text><text x="${x+200}" y="440" text-anchor="middle" font-size="30" font-weight="700" fill="#4a5a52">${b}</text>`+ans.map(([w,r,c],j)=>`<rect x="${x+24}" y="${480+j*150}" width="352" height="128" rx="24" fill="${c}"/><rect x="${x+36}" y="${488+j*150}" width="328" height="26" rx="13" fill="#fff" opacity=".18"/><text x="${x+200}" y="${526+j*150}" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">${w}</text><text x="${x+200}" y="${580+j*150}" text-anchor="middle" font-size="${r.length>8?30:36}" font-weight="900" fill="#fff">${r}</text>`).join(''),at(k+1,.4))+(dim<1?`<rect x="${x}" y="260" width="400" height="540" rx="28" fill="#1f3a2b" opacity=".42"/>`:'')+`</g>`});
    }
    if(on(4)&&!on(5)){
      s+=pop(1200,520,at(4,.5),inn(1200,770,.95,{sign:'あなたの家',t,lit:1,roof:'#2e6b47',noren:T,case:1,post:1,bike:1,signc:'#2f2a22'}));
      [['日数',860,G],['立地',1200,'#3d8a6a'],['運営',1540,T]].forEach(([w,x,c],k)=>{s+=tag(x,290,w,at(4,.4,[.4,1.2,2][k]),c,'#fff',44)});
      s+=tag(1200,835,'迷ったら、家を買う前に、窓口へ',at(4,.4,5.2),Y,DG,34);}
    if(on(5)&&!on(6)){
      [['手続きの比較表（記事）','doc',G],['旅館業の許可の取り方（記事）','key',T],['無料相談','chat','#3d8a6a']].forEach(([w,ic,c],k)=>{const y=330+k*150;
        s+=pop(1200,y,at(5,.4,[.4,2.6,5][k]),`${bx(640,y-60,1120,124,36)}${icon(740,y+2,44,ic,c,'#fff',.95)}<text x="830" y="${y+16}" font-size="46" font-weight="900" fill="${DG}">${w}</text><text x="1720" y="${y+14}" text-anchor="end" font-size="34" font-weight="900" fill="${c}">概要欄へ ▶</text>`)});}
    if(on(6)&&!on(7)){
      s+=pop(900,480,at(6,.5,.3),`<rect x="640" y="326" width="520" height="300" rx="26" fill="#000" opacity=".14" transform="translate(0 8)"/><rect x="640" y="326" width="520" height="300" rx="26" fill="url(#gD)"/><rect x="660" y="346" width="480" height="260" rx="16" fill="#cfe9d4"/>${inn(880,530,.36,{sign:'',t,lit:.7,chim:1})}${coin(1050,420,34)}${coin(1090,480,28)}<rect x="660" y="548" width="480" height="58" rx="12" fill="#fff" opacity=".94"/><text x="900" y="589" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">民泊は「第3の資産」</text><rect x="660" y="346" width="150" height="48" rx="24" fill="${T}"/><text x="735" y="380" text-anchor="middle" font-size="30" font-weight="900" fill="#fff">第1回</text><g transform="translate(730,470)"><circle r="42" fill="#fff" opacity=".92"/><path d="M-14 -22 L28 0 L-14 22Z" fill="${T}"/></g>`);
      s+=card(1200,330,640,300,`<text x="1240" y="410" font-size="40" font-weight="900" fill="${DG}">年180日の上限を知ったうえで</text><text x="1240" y="480" font-size="40" font-weight="900" fill="${DG}">宿を資産に入れる理由を見る</text><text x="1240" y="550" font-size="40" font-weight="900" fill="${T}">手続き選びの意味がわかる</text>`,at(6,.5,2.2));}
    if(on(7)){
      s+=pop(1200,470,at(7,.5),`${bx(660,270,1080,380,40)}${icon(940,380,70,'chat',G,'#fff',1.3)}<text x="1280" y="400" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">あなたの家は、どちら？</text>${formulaChip(900,480,300,'届出',G,'#fff',46)}${formulaChip(1260,480,300,'許可',T,'#fff',46)}<text x="1200" y="620" text-anchor="middle" font-size="34" font-weight="900" fill="${T}">コメントで教えてください</text>`);}
    s+=fade(seg(lt,E[7]+.5,E[7]+1.2),`<rect width="1920" height="1080" fill="#16301f"/><circle cx="960" cy="200" r="260" fill="url(#glow)" opacity=".25"/><text x="960" y="380" text-anchor="middle" font-size="60" font-weight="900" fill="#fff">最後まで見てくれて、ありがとうございます</text><text x="960" y="480" text-anchor="middle" font-size="30" font-weight="700" fill="#dfe9e3">${NOTE}</text><text x="960" y="530" text-anchor="middle" font-size="30" font-weight="700" fill="#dfe9e3">宿の稼働率は、開業から約8.5か月の平均で、一例です。出典は概要欄に記載しています。</text><text x="960" y="630" text-anchor="middle" font-size="30" font-weight="700" fill="#b8c9bf">${CREDIT}</text><rect x="780" y="700" width="360" height="100" rx="50" fill="#fff"/>${LOGO(810,715,1.1)}`,0);
  }
  const TT={2:['違い ①','1年に泊められる日数',G],3:['違い ②','許可の条件と手間','#3d8a6a'],4:['違い ③','届出か許可かの決め手',T],5:['注意','失敗しやすい点 4つ',RED],6:['さいごに','あなたの家は、届出？ 許可？',DG]};
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
