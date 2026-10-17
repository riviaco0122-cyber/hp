#!/usr/bin/env python3
"""アキヤドの解説動画 第1回「民泊を資産に入れる5つの理由」（約8分・1920×1080）を作る。

- 話し手はアニメの民泊戦略家「アキ」。聞き手にユウタ（アキヤド劇場と同じキャラ）。型は docs/youtube/manual.md 1-2章。
- 数字の出どころ（説明欄にも書く）:
  訪日客 2024年3,687万人・2025年4,268万人（JNTO「訪日外客統計」）、2030年目標6,000万人と外国人宿泊の地方部33.7%（観光庁「観光立国推進基本計画（第5次）」「宿泊旅行統計調査 2025年確定値」）、
  空き家約900万戸・空き家率13.8%（総務省「令和5年住宅・土地統計調査」）、住宅宿泊事業の所得は原則雑所得（国税庁「住宅宿泊事業により生じる所得の課税関係等について（情報）」）、
  管理不全空家等の勧告で住宅用地特例が外れる（国土交通省・総務省）、営業日数は年180日以内（住宅宿泊事業法）。
  宿の数字は記事「不動産投資として見る小さな宿・民泊」と同じ、創業メンバーが運営する下田の宿の実績（試運転3か月。docs/brand/experience.md の確認済みの節）。
- 部品・書き出しは make_explainer.py / make_scam_ep1.py と共通。声は VOICEVOX（クレジットは最後の画面と説明欄）。
使い方: python3 tools/video/make_strategy_ep1.py [出力.mp4] [--hq] [--preview 秒 ...] [--no-check]
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
VOICES = {
    "A": dict(name="戦略家 アキ", style=83, speed=1.12, intonation=1.2, pitch=0.0),   # 青山龍星（喜び）。明るく、テンポよく
    "K": dict(name="ジングル", style=1, speed=1.0, intonation=1.6, pitch=0.04),         # ずんだもん（あまあま）。オープニングの呼び込み
    "Y": dict(name="ユウタ", style=11, speed=1.08, intonation=1.15, pitch=0.0),        # 玄野武宏
}
MODELS = [0, 4, 15]
CREDIT = "VOICEVOX:青山龍星　VOICEVOX:玄野武宏　VOICEVOX:ずんだもん"
NOTE = "※ 情報提供を目的とした動画で、特定の投資を勧めるものではありません。数字は公表資料と、運営する宿の実績（一例）です。"

SCENES = [
    # 0 つかみ：結論 → 今日の話 → 自己紹介
    ("dark", 0.8, [
        ("A", "結論から言います。民泊は、株や預金とはちがう動きをする「第3の資産」になります。", dict(sfx=[(0.2, "pop"), (1.6, "pop"), (3.2, "bling")])),
        ("A", "ただし、入れ方をまちがえると、ただの重荷です。", dict(sfx=[(1.4, "boing")])),
        ("A", "今日は、民泊を資産に入れる5つの理由と、始める前に確かめること。そして最後に、失敗しない入れ方を1つだけお話しします。", dict(sfx=[(0.6, "pop"), (1.0, "pop"), (1.4, "pop"), (1.8, "pop"), (2.2, "pop"), (4.6, "pop"), (6.4, "chime")])),
        ("A", "アキヤドの民泊戦略家、アキです。自分たちで宿を運営しながら、空き家と民泊の情報を発信しています。専門的な話も、できるだけわかりやすくお話しします。", dict(pre=4.6, call=(-3.75, "K", "アキヤド、みんぱくスクール！"), sfx=[(-4.5, "whoosh"), (-4.1, "pop"), (-3.4, "rise"), (-2.6, "bling"), (-1.6, "chime"), (-0.5, "whoosh")])),
    ]),
    # 1 理由① 分散
    ("light", 0.8, [
        ("A", "理由その1。資産の「分散」です。", dict(sfx=[(0, "chime")])),
        ("Y", "分散って、いろんな株を買うことじゃないんですか？", dict(sfx=[(0, "pop")])),
        ("A", "それも分散です。でも株は、同じ日に、そろって下がることがあります。", dict(sfx=[(2.4, "boing")])),
        ("A", "宿の売上は、株価ではなく、旅行者の数で動きます。動く理由がちがう資産を持つのが、本当の分散です。", dict(sfx=[(0.4, "pop"), (2.0, "pop")])),
        ("Y", "でも、旅行者が減ったら、宿もダメになりませんか？", dict(sfx=[(0, "pop")])),
        ("A", "そのとおり。だから、全部を宿にはしません。そして宿には、株にはない強みがあります。自分で、打ち手を打てることです。", dict(sfx=[(4.6, "ding")])),
        ("A", "料金を変える。長く泊まるお客さんを増やす。予約の窓口を増やす。動かせるレバーが、自分の手の中にあるんです。", dict(sfx=[(0.3, "pop"), (1.6, "pop"), (3.6, "pop")])),
        ("A", "しかも宿は、料金を日ごとに決められる「実物の資産」。物価が上がる時代にも、合わせやすいんです。", dict(sfx=[(1.2, "ding")])),
    ]),
    # 2 理由② 賃貸とくらべた稼ぎ方
    ("light", 0.8, [
        ("A", "理由その2。賃貸とくらべた「稼ぎ方」のちがいです。", dict(sfx=[(0, "chime")])),
        ("A", "賃貸は、家賃が毎月ほぼ同じ。宿は「稼働率かける1泊の料金」で、上にも下にも動きます。", dict(sfx=[(0.4, "pop"), (2.4, "pop")])),
        ("A", "たとえば、1泊1万5千円で、月に15泊うまれば、売上は22万5千円。料金か泊数、どちらかを動かせば、売上が変わります。", dict(say="たとえば、一泊一万五千円で、月に十五泊うまれば、売上は二十二万五千円。料金か泊数、どちらかを動かせば、売上が変わります。", sfx=[(0.6, "pop"), (2.6, "pop"), (4.6, "coin")])),
        ("A", "実際の例です。私たちが下田で借りている一軒家の家賃は、月5万円。", dict(say="実際の例です。私たちが下田で借りている一軒家の家賃は、月五万円。", sfx=[(2.8, "coin")])),
        ("A", "その家を宿にしたら、試運転の3か月で、売上は約100万円。運営費を引いた営業利益は、約45万円でした。", dict(say="その家を宿にしたら、試運転の三か月で、売上は約百万円。運営費を引いた営業利益は、約四十五万円でした。", sfx=[(2.6, "pop"), (4.6, "pop"), (6.4, "coin")])),
        ("A", "運営費は、月に約18万円。家賃5万円、清掃2万円、予約サイトの手数料など8万円、光熱費や消耗品が3万円です。", dict(say="運営費は、月に約十八万円。家賃五万円、清掃二万円、予約サイトの手数料など八万円、光熱費や消耗品が三万円です。", sfx=[(1.6, "pop"), (2.6, "pop"), (3.6, "pop"), (5.6, "pop")])),
        ("A", "月にならすと、家賃を払ったうえで約15万円。家賃の約3倍が、手元に残った計算です。", dict(say="月にならすと、家賃を払ったうえで約十五万円。家賃の約三倍が、手元に残った計算です。", sfx=[(0.6, "rise"), (3.0, "bling")])),
        ("A", "ただし、ここには私たちの手間と、改修や家具の初期投資、約650万円は入っていません。", dict(say="ただし、ここには私たちの手間と、改修や家具の初期投資、約六百五十万円は入っていません。", sfx=[(0.3, "alert")])),
        ("A", "では、運営の腕で、何が変わるのか。同じ宿の、1年目と2年目をくらべます。", dict(say="では、運営の腕で、何が変わるのか。同じ宿の、一年目と二年目をくらべます。", sfx=[(0.3, "whoosh")])),
        ("A", "2年目の上半期は、混む時期に料金を上げて、1泊の平均単価が約1.4倍に。1部屋あたりの売上は、約1.74倍になりました。", dict(say="二年目の上半期は、混む時期に料金を上げて、一泊の平均単価が約一点四倍に。一部屋あたりの売上は、約一点七四倍になりました。", sfx=[(2.6, "rise"), (6.0, "bling")])),
        ("A", "売上が伸びたことで、家賃が売上に占める割合は、約30%から、約12%まで下がっています。", dict(say="売上が伸びたことで、家賃が売上に占める割合は、約三十パーセントから、約十二パーセントまで下がっています。", sfx=[(3.0, "pop")])),
        ("A", "一方で、季節の波もあります。1年目の稼働率は、12月が71%、11月は33%。平均すると、約53%でした。", dict(say="一方で、季節の波もあります。一年目の稼働率は、十二月が七十一パーセント、十一月は三十三パーセント。平均すると、約五十三パーセントでした。", sfx=[(0.4, "pop")])),
        ("A", "ちなみに、全国の簡易宿所の稼働率は、2025年の平均で29.6%。同じ宿でも、運営しだいで、数字は大きく変わります。", dict(say="ちなみに、全国の簡易宿所の稼働率は、二千二十五年の平均で二十九点六パーセント。同じ宿でも、運営しだいで、数字は大きく変わります。", sfx=[(0.4, "pop"), (4.0, "pop")])),
        ("A", "つまり宿は、運営の腕で、稼ぎを伸ばせる資産。ここが、賃貸との一番のちがいです。", dict(sfx=[(0.2, "ding")])),
    ]),
    # 3 理由③ 世界の観光需要（途中にクイズ）
    ("light", 0.8, [
        ("A", "理由その3。世界の観光需要を、自分の資産に取り込めることです。", dict(sfx=[(0, "chime")])),
        ("A", "日本に来た外国人旅行者は、2025年に4,268万人。過去最多を更新しました。", dict(say="日本に来た外国人旅行者は、二千二十五年に四千二百六十八万人。過去最多を更新しました。", sfx=[(0.4, "pop"), (2.2, "rise")])),
        ("A", "2024年の3,687万人から、1年で約16%も増えています。", dict(say="二千二十四年の三千六百八十七万人から、一年で約十六パーセントも増えています。", sfx=[(3.0, "pop")])),
        ("A", "そして国は、2030年に6,000万人を目標にしています。", dict(say="そして国は、二千三十年に六千万人を目標にしています。", sfx=[(0.4, "pop")])),
        ("A", "ここでクイズです。外国人が日本で泊まった数のうち、地方の割合はどれくらいでしょう？ A、1割。B、3割。C、5割。", dict(say="ここでクイズです。外国人が日本で泊まった数のうち、地方の割合はどれくらいでしょう？ エー、一割。ビー、三割。シー、五割。", sfx=[(0, "chime")])),
        ("A", "正解は、B。約3割、33.7%です。残りの約3分の2は、東京・大阪・名古屋などの大都市圏に集中しています。", dict(pre=3.2, say="正解は、ビー。約三割、三十三点七パーセントです。残りの約三分の二は、東京、大阪、名古屋などの大都市圏に集中しています。", sfx=[(-3.2, "tick"), (-2.2, "tick"), (-1.2, "tick"), (0, "ding")])),
        ("Y", "地方には、まだ伸びる余地があるってことか…！", dict(sfx=[(0, "pop")])),
        ("A", "そうなんです。私たちの宿も、欧米からの長期滞在のお客さんが中心。海外の需要は、地方の一軒家にも届きます。", dict(sfx=[(0.4, "bling")])),
    ]),
    # 4 理由④ 税金
    ("light", 0.8, [
        ("A", "理由その4。税金です。ここは誤解が多いので、正確にいきます。", dict(sfx=[(0, "chime")])),
        ("A", "宿の売上からは、清掃や手数料などの経費を差し引けます。家具や改修の費用は、何年かに分けて経費にする「減価償却」ができます。", dict(sfx=[(0.6, "pop"), (4.2, "pop")])),
        ("A", "ただし、民泊新法の宿の所得は、原則「雑所得」。赤字が出ても、給料と相殺して税金を減らす使い方はできない、と考えておきましょう。", dict(sfx=[(2.6, "pop"), (5.6, "boing")])),
        ("A", "むしろ注目は、空き家の固定資産税。放置して自治体から勧告を受けると、土地の税を軽くする特例が外れ、計算のもとが最大6倍になります。", dict(say="むしろ注目は、空き家の固定資産税。放置して自治体から勧告を受けると、土地の税を軽くする特例が外れ、計算のもとが最大六倍になります。", sfx=[(0.4, "pop"), (6.4, "boing")])),
        ("A", "たとえば、土地の評価額が1,200万円なら、税額は年2万8千円から、16万8千円に。", dict(say="たとえば、土地の評価額が千二百万円なら、税額は年二万八千円から、十六万八千円に。", sfx=[(1.6, "pop"), (3.6, "boing")])),
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
    # 6 大事な前提：民泊の始め方は3つ
    ("light", 0.8, [
        ("A", "ここで、大事な前提を1つ。民泊の始め方は、大きく3つあります。", dict(say="ここで、大事な前提をひとつ。民泊の始め方は、大きく三つあります。", sfx=[(0, "chime")])),
        ("A", "1つめ、民泊新法の届出。手続きは比較的かんたんですが、営業できるのは年180日までです。", dict(say="ひとつめ、民泊新法の届出。手続きは比較的かんたんですが、営業できるのは年百八十日までです。", sfx=[(0, "pop")])),
        ("A", "2つめ、旅館業法の許可。簡易宿所などの許可を取れば、日数の上限なく営業できます。そのかわり、建物の基準や、地域のルールを満たす必要があります。", dict(say="ふたつめ、旅館業法の許可。簡易宿所などの許可を取れば、日数の上限なく営業できます。そのかわり、建物の基準や、地域のルールを満たす必要があります。", sfx=[(0, "pop")])),
        ("A", "3つめ、特区民泊。国家戦略特区の、一部の地域だけで使える仕組みです。", dict(say="みっつめ、特区民泊。国家戦略特区の、一部の地域だけで使える仕組みです。", sfx=[(0, "pop")])),
        ("A", "私たちの宿は、2つめの、旅館業法の許可を取りました。年180日の上限なく、1年中営業するためです。", dict(say="私たちの宿は、ふたつめの、旅館業法の許可を取りました。年百八十日の上限なく、一年中営業するためです。", sfx=[(0.4, "ding")])),
        ("A", "資産として考えるなら、何日営業できるかで、売上の天井が変わります。ここは、最初に確かめてください。", dict(sfx=[(0.4, "pop")])),
    ]),
    # 6 リスク
    ("light", 0.8, [
        ("A", "もちろん、リスクもあります。大きく3つ。", dict(say="もちろん、リスクもあります。大きく三つ。", sfx=[(0, "alert")])),
        ("A", "1つめ、需要の波。季節や景気、感染症で、旅行者は大きく減ることがあります。", dict(say="ひとつめ、需要の波。季節や景気、感染症で、旅行者は大きく減ることがあります。", sfx=[(0, "pop")])),
        ("A", "2つめ、ルール。民泊新法では、営業は年180日まで。地域の条例で、さらに短くなることもあります。", dict(say="ふたつめ、ルール。民泊新法では、営業は年百八十日まで。地域の条例で、さらに短くなることもあります。", sfx=[(0, "pop")])),
        ("A", "3つめ、手間。清掃やゲスト対応は毎日続きます。自分でやるか、任せるかで、手元に残るお金が変わります。", dict(say="みっつめ、手間。清掃やゲスト対応は毎日続きます。自分でやるか、任せるかで、手元に残るお金が変わります。", sfx=[(0, "pop")])),
        ("A", "それから、「誰でも簡単に月100万円」という話は、まず疑ってください。うまい話ほど、裏があります。", dict(say="それから、誰でも簡単に月百万円、という話は、まず疑ってください。うまい話ほど、裏があります。", sfx=[(0.4, "boing")])),
    ]),
    # 7 始める前に：くらべる3つの数字・確かめる4つのこと
    ("light", 0.8, [
        ("A", "では、実際に始める前に、何を確かめればいいのか。まず、くらべる数字は3つです。", dict(say="では、実際に始める前に、何を確かめればいいのか。まず、くらべる数字は三つです。", sfx=[(0, "chime")])),
        ("A", "1つめ、その家を賃貸に出した場合の家賃。2つめ、宿の営業利益から、自分の手間を引いた額。3つめ、初期投資を、何年で回収できるか。", dict(say="ひとつめ、その家を賃貸に出した場合の家賃。ふたつめ、宿の営業利益から、自分の手間を引いた額。みっつめ、初期投資を、何年で回収できるか。", sfx=[(0, "pop"), (3.2, "pop"), (7.0, "pop")])),
        ("A", "私たちの宿は、約14か月で、初期投資の約98%を回収しました。ただし、これは1つの例です。", dict(say="私たちの宿は、約十四か月で、初期投資の約九十八パーセントを回収しました。ただし、これはひとつの例です。", sfx=[(0.4, "rise"), (4.0, "bling")])),
        ("A", "そして、確かめることは4つ。法律や条例で、営業できるか。まわりの需要と、競合の宿。建物の状態と、改修費。そして、運営の体制です。", dict(say="そして、確かめることは四つ。法律や条例で、営業できるか。まわりの需要と、競合の宿。建物の状態と、改修費。そして、運営の体制です。", sfx=[(1.6, "pop"), (4.0, "pop"), (6.4, "pop"), (8.8, "pop")])),
        ("Y", "数字と、チェックの両方が大事なんですね。", dict(sfx=[(0, "pop")])),
    ]),
    # 8 失敗しない入れ方 → まとめ → 無料相談
    ("dark", 4.6, [
        ("A", "では最後に、失敗しない入れ方を、1つだけ。", dict(say="では最後に、失敗しない入れ方を、ひとつだけ。", sfx=[(0, "rise")])),
        ("A", "それは、全部を民泊にしないこと。預金や株を土台にして、資産の一部として、小さく組み込むことです。", dict(sfx=[(0.4, "bling"), (3.6, "pop")])),
        ("A", "私たちも、家を買わずに借りて始めました。準備には、約7か月かかりました。", dict(say="私たちも、家を買わずに借りて始めました。準備には、約七か月かかりました。", sfx=[(0.4, "pop")])),
        ("A", "まとめると、分散、稼ぎ方、観光需要、税金、社会課題。5つの理由で、民泊は資産に入れる価値があります。リスクを知って、一部として、小さく。", dict(say="まとめると、分散、稼ぎ方、観光需要、税金、社会課題。五つの理由で、民泊は資産に入れる価値があります。リスクを知って、一部として、小さく。", sfx=[(0.6, "pop"), (1.2, "pop"), (1.8, "pop"), (2.6, "pop"), (3.2, "pop")])),
        ("A", "あなたなら、資産のどれくらいを民泊にしますか？ ぜひ、コメントで教えてください。", dict(sfx=[(0.4, "pop")])),
        ("A", "あなたの家や地域で、民泊が成り立つか知りたい方は、アキヤドの無料相談へ。概要欄のリンクからどうぞ。", dict(sfx=[(0.4, "chime")])),
    ]),
]
LEAD, GAP = 0.5, 0.32

SCENE_JS = r"""
CAST.aki={skin:'#f1c7a1',hair:'#2b2422',style:'short',top:'#23395b',top2:'#1a2c47',inner:'#ffffff',jacket:true,pants:'#2a3140',shoes:'#3a2a20',glasses:true,tie:'#c95a35'};
const VNAME={A:'戦略家 アキ',Y:'ユウタ'},VCOL={A:T,Y:G};
const NAVY='#23395b',RED='#e53935';
const talking=(s,t)=>LINES.some(l=>l[2]===s&&t>=l[0]&&t<l[1]);
function subtitle(l,t){
  const lines=l[3],fs=42,h=lines.length*fs*1.45+40,w=1560,y=1048-h,o=clamp((t-l[0]+.05)/.2)*clamp((l[1]+.3-t)/.2);
  const name=`<rect x="${960-w/2+28}" y="${y-26}" width="${VNAME[l[2]].length*30+44}" height="52" rx="26" fill="${VCOL[l[2]]}"/><text x="${960-w/2+50}" y="${y+9}" font-size="30" font-weight="900" fill="#fff">${VNAME[l[2]]}</text>`;
  return `<g opacity="${o}"><rect x="${960-w/2}" y="${y}" width="${w}" height="${h}" rx="24" fill="${DG}" opacity=".93"/>${name}${lines.map((s,i)=>`<text x="960" y="${y+28+fs*1.08+i*fs*1.45}" text-anchor="middle" font-size="${fs}" font-weight="700" fill="#fff" letter-spacing="1">${s}</text>`).join('')}</g>`;
}
const P=(x,y,s,o,t)=>person(x,y,s,Object.assign({t},o,{talk:o.who?talking(o.who,t):false}));
function studio(t,dark){ // 解説のスタジオ（明るい／暗い）
  if(dark){let s=`<rect width="1920" height="1080" fill="#173a29"/><path d="M700 0 L420 1080 L1640 1080 L1360 0Z" fill="#fff" opacity=".05"/>`;
    for(let k=0;k<30;k++)s+=`<circle cx="${rnd(k)*1920}" cy="${rnd(k+40)*700}" r="${1.5+rnd(k+80)*2}" fill="#fff" opacity="${.15+.25*Math.abs(Math.sin(t*1.5+k))}"/>`;
    return s+`<rect y="${GROUND}" width="1920" height="${1080-GROUND}" fill="#10291d"/>`;}
  let s=`<rect width="1920" height="1080" fill="#f4f6f1"/>`;
  for(let x=0;x<1920;x+=60)s+=`<path d="M${x} 0 V1080" stroke="#e3e9e2" stroke-width="2"/>`;
  for(let y=0;y<1080;y+=60)s+=`<path d="M0 ${y} H1920" stroke="#e3e9e2" stroke-width="2"/>`;
  return s+`<rect y="${GROUND}" width="1920" height="${1080-GROUND}" fill="#e1e9e0"/>`;
}
function hdr(no,title,p,c=T){ // 「理由 ①」の見出し
  return fade(p,`<rect x="540" y="70" width="${no?190:0}" height="64" rx="32" fill="${c}"/>${no?`<text x="635" y="114" text-anchor="middle" font-size="34" font-weight="900" fill="#fff">理由 ${no}</text>`:''}<text x="${no?750:540}" y="118" font-size="54" font-weight="900" fill="${DG}">${title}</text>`,0);
}
const card=(x,y,w,h,inner,p)=>pop(x+w/2,y+h/2,p,box(x,y,w,h,28)+inner);
function qbubble(id,txt,p,t){ // ユウタの質問
  return pop(1500,215,p,`${face(id,1790,215,62,'owner',G,'worry',t,talking('Y',t))}<rect x="${1700-txt.length*30-60}" y="172" width="${txt.length*30+60}" height="86" rx="30" fill="#fff" stroke="${G}" stroke-width="4"/><text x="${1700-30-txt.length*15}" y="227" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">${txt}</text>`);
}
function stampX(x,y,txt,p,c=RED,fs=72,rot=-8){return pop(x,y,p,`<g transform="rotate(${rot} ${x} ${y})"><rect x="${x-txt.length*fs*.5-34}" y="${y-fs*.8}" width="${txt.length*fs+68}" height="${fs*1.45}" rx="14" fill="#fff" fill-opacity=".92" stroke="${c}" stroke-width="10"/><text x="${x}" y="${y+fs*.33}" text-anchor="middle" font-size="${fs}" font-weight="900" fill="${c}">${txt}</text></g>`)}
const REASONS=[['1','分散',G],['2','稼ぎ方',T],['3','観光需要','#3d8a6a'],['4','税金','#b8862f'],['5','社会課題',DG]];
function scene(i,t,lt){
  const K=.89,L=SL[i],E=SE[i],at=(k,d=.5,o=0)=>seg(lt,L[k]+o*K,L[k]+o*K+d)  /* K: 話す速さを上げたぶん、絵の出るタイミングも詰める */,on=k=>lt>=L[k],win=(k,j)=>clamp(seg(lt,L[k],L[k]+.4))*(j==null?1:1-seg(lt,L[j]-.1,L[j]+.3));
  let s='';
  const aki=(pose,mood='happy',x=250)=>P(x,GROUND,.92,{c:'aki',who:'A',pose,mood},t);
  const tag=(x,y,txt,p,c=Y,fc=DG)=>pop(x,y,p,`<rect x="${x-txt.length*17-24}" y="${y-30}" width="${txt.length*34+48}" height="60" rx="30" fill="${c}"/><text x="${x}" y="${y+12}" text-anchor="middle" font-size="34" font-weight="900" fill="${fc}">${txt}</text>`);
  const reasonGrid=(k0,base)=>{let g='';REASONS.forEach(([n,w,c],k)=>{const x=640+(k%3)*420,y=k<3?300:470;g+=pop(x+180,y,at(k0,.35,base+k*.4),`${box(x,y-62,360,124,30)}<circle cx="${x+66}" cy="${y}" r="42" fill="${c}"/><text x="${x+66}" y="${y+16}" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">${n}</text><text x="${x+128}" y="${y+17}" font-size="46" font-weight="900" fill="${DG}">${w}</text>`)});return g};
  if(i===0){
    s+=aki(on(1)&&!on(2)?'open':(on(3)?'wave':'present'));
    if(!on(1)){[['預金','yen','#8a8f98'],['株','chart','#3d6a8a'],['民泊','home',T]].forEach(([w,ic,c],k)=>{const x=760+k*430,p=at(0,.4,.2+k*1.4);
      s+=pop(x,470,p,`${box(x-170,300,340,340,30)}${icon(x,430,78,ic,c,'#fff',1.1)}<text x="${x}" y="590" text-anchor="middle" font-size="52" font-weight="900" fill="${DG}">${w}</text>`)});
      s+=pop(1620,720,at(0,.4,3.2),`<rect x="1450" y="680" width="340" height="80" rx="40" fill="${Y}"/><text x="1620" y="735" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">第3の資産</text>`);
      s+=fade(at(0,.4,3.2),`<rect x="1442" y="292" width="356" height="356" rx="36" fill="none" stroke="${Y}" stroke-width="10"/>`,0);}
    if(on(1)&&!on(2)){s+=pop(1190,480,at(1,.4),`${icon(1190,480,150,'home',T,'#fff',2)}<rect x="1100" y="250" width="180" height="110" rx="14" fill="#3a3e46"/><text x="1190" y="322" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">重い</text>`)+stampX(1190,720,'ただの重荷',at(1,.3,1.3));}
    if(on(2)&&!on(3)&&lt<E[2]+.3){s+=reasonGrid(2,.6);
      s+=pop(1000,660,at(2,.4,4.6),`<rect x="660" y="620" width="680" height="84" rx="42" fill="#fff"/><text x="1000" y="676" text-anchor="middle" font-size="40" font-weight="900" fill="${G}">始める前に、確かめること</text>`);
      s+=pop(1560,660,at(2,.4,6.4),`<rect x="1370" y="620" width="380" height="84" rx="42" fill="${Y}"/><text x="1560" y="676" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">最後に：入れ方</text>`);}
    // オープニング（約4秒）：緑の幕 → ロゴ → シリーズ名 → 今回のタイトル → はける
    {const q=lt-(E[2]+.15),D=L[3]-.35-(E[2]+.15);if(q>0&&q<D){
      const out=seg(q,D-.5,D),wipe=eo(seg(q,0,.45));
      let o=`<g opacity="${1-out}"><rect width="${1920*wipe}" height="1080" fill="${G}"/>`;
      for(let k=0;k<12;k++){const x=((k*220+q*260)%2600)-400;o+=`<path d="M${x} 1080 L${x+500} 0" stroke="#fff" stroke-width="40" opacity="${.06*wipe}"/>`}
      o+=`<rect x="0" y="0" width="${1920*eo(seg(q,.15,.6))}" height="22" fill="${T}"/><rect x="${1920*(1-eo(seg(q,.15,.6)))}" y="1058" width="1920" height="22" fill="${Y}"/>`;
      o+=pop(960,250,seg(q,.35,.85),`<circle cx="960" cy="250" r="96" fill="#fff"/>${MARK(960,250,2.1)}`);
      o+=pop(960,425,seg(q,1.05,1.45),`<g transform="rotate(-3 960 425)"><rect x="560" y="370" width="800" height="110" rx="55" fill="#fff"/><text x="960" y="448" text-anchor="middle" font-size="62" font-weight="900" fill="${G}" letter-spacing="2">アキヤド <tspan fill="${T}">民泊school</tspan></text></g>`);
      o+=pop(960,610,seg(q,2.0,2.4),`<text x="960" y="590" text-anchor="middle" font-size="84" font-weight="900" fill="#fff">民泊を資産に入れる</text><text x="960" y="730" text-anchor="middle" font-size="120" font-weight="900" fill="${Y}">5つの理由</text>`);
      o+=fade(seg(q,2.4,2.8),`<text x="960" y="850" text-anchor="middle" font-size="26" font-weight="700" fill="#dfe9e3">${NOTE}</text>`,0);
      [[220,180],[1700,200],[160,560],[1760,600],[300,920],[1620,940]].forEach(([x,y],k)=>{o+=`<g opacity="${wipe}">${sparkle(x,y,1,lt,k)}</g>`});
      s+=o+`</g>`;}}
    if(on(3)){s+=pop(1150,430,at(3,.5),`${box(620,250,1060,360,36)}<rect x="660" y="290" width="380" height="64" rx="32" fill="${G}"/><text x="850" y="334" text-anchor="middle" font-size="32" font-weight="900" fill="#fff">アキヤドの民泊戦略家</text><text x="680" y="460" font-size="110" font-weight="900" fill="${DG}">アキ</text>`);
      [['宿を運営',G],['空き家と民泊を発信',T],['わかりやすく解説',Y]].forEach(([w,c],k)=>{s+=tag(1400,330+k*90,w,at(3,.4,2+k*1.2),c,k===2?DG:'#fff')});}
  }
  if(i===1){ // 分散
    s+=aki(on(2)&&!on(3)?'open':(on(6)?'point':'present'));
    s+=hdr('①','分散：動く理由がちがう資産を持つ',at(0,.4),G);
    if(on(1)&&!on(2))s+=qbubble('q1','いろんな株を買えば分散？',at(1,.4),t);
    if(on(1)&&!on(3)){const dn=on(2)?eo(at(2,1.2,.8)):0;[['株A','#3d6a8a'],['株B','#5a86a8'],['株C','#7a9fbf']].forEach(([w,c],k)=>{const x=700+k*360;let path='';for(let q=0;q<=10;q++){const yy=560-Math.sin(q*.9+k)*40-q*6+(q>6?dn*(q-6)*55:0);path+=(q?'L':'M')+(x+q*28)+' '+yy}
      s+=card(x-40,290,360,440,`<text x="${x+140}" y="350" text-anchor="middle" font-size="40" font-weight="900" fill="${c}">${w}</text><path d="${path}" stroke="${c}" stroke-width="10" fill="none" stroke-linejoin="round"/>`,at(1,.4,.3+k*.3))});
      if(on(2))s+=stampX(1240,790,'同じ日に、そろって下がる',at(2,.3,2.2),RED,48,-4);}
    if(on(3)&&!on(5)){s+=card(560,280,600,480,`<text x="860" y="350" text-anchor="middle" font-size="44" font-weight="900" fill="#3d6a8a">株の値段</text>${icon(860,500,90,'chart','#3d6a8a','#fff',1.3)}<text x="860" y="670" text-anchor="middle" font-size="34" font-weight="900" fill="#4a5a52">景気・金利で動く</text>`,at(3,.4))+card(1240,280,600,480,`<text x="1540" y="350" text-anchor="middle" font-size="44" font-weight="900" fill="${T}">宿の売上</text>${icon(1540,500,90,'home',T,'#fff',1.3)}<text x="1540" y="670" text-anchor="middle" font-size="34" font-weight="900" fill="#4a5a52">旅行者の数・季節で動く</text>`,at(3,.4,1.6));
      if(!on(4))s+=pop(1200,810,at(3,.4,3.6),`<rect x="830" y="770" width="740" height="80" rx="40" fill="${G}"/><text x="1200" y="823" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">動く理由がちがう＝本当の分散</text>`);
      if(on(4))s+=qbubble('q1b','旅行者が減ったら？',at(4,.4),t);}
    if(on(5)&&!on(6)){s+=card(560,250,600,500,`<text x="860" y="330" text-anchor="middle" font-size="44" font-weight="900" fill="#3d6a8a">株</text><text x="860" y="470" text-anchor="middle" font-size="120" font-weight="900" fill="#b9c3cc">✕</text><text x="860" y="640" text-anchor="middle" font-size="36" font-weight="900" fill="#4a5a52">自分では動かせない</text>`,at(5,.4,1.8))+card(1240,250,600,500,`<text x="1540" y="330" text-anchor="middle" font-size="44" font-weight="900" fill="${T}">宿</text><text x="1540" y="470" text-anchor="middle" font-size="120" font-weight="900" fill="${G}">◎</text><text x="1540" y="640" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">自分で打ち手を打てる</text>`,at(5,.4,4.4));}
    if(on(6)&&!on(7))[['料金を変える','yen',T],['長く泊まる客を増やす','home',G],['予約の窓口を増やす','search','#3d6a8a']].forEach(([w,ic,c],k)=>{const x=760+k*420;s+=pop(x,480,at(6,.4,[.3,1.6,3.6][k]),`${box(x-190,290,380,400,30)}${icon(x,420,80,ic,c,'#fff',1.1)}<path d="M${x-60} 560 h120" stroke="${c}" stroke-width="14" stroke-linecap="round"/><circle cx="${x+40*Math.sin(lt*2+k)}" cy="560" r="20" fill="${c}"/><text x="${x}" y="640" text-anchor="middle" font-size="${w.length>8?32:36}" font-weight="900" fill="${DG}">${w}</text>`)});
    if(on(7)){const pr=Math.round(12000+3000*eo(at(7,1.4,1.2)));s+=card(600,250,1200,520,`<text x="1200" y="320" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">宿の料金は、日ごとに決められる</text>${['月','火','水','木','金','土','日'].map((d,k)=>`<rect x="${660+k*155}" y="370" width="140" height="220" rx="14" fill="${k>=5?'#fdecea':'#eef3ee'}"/><text x="${730+k*155}" y="420" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">${d}</text><text x="${730+k*155}" y="520" text-anchor="middle" font-size="${k>=5?34:30}" font-weight="900" fill="${k>=5?RED:'#4a5a52'}">¥${(k>=5?pr:12000).toLocaleString()}</text>`).join('')}<text x="1200" y="700" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">「実物の資産」＝物価に合わせやすい</text>`,at(7,.4));}
  }
  if(i===2){ // 稼ぎ方
    s+=aki(on(7)&&!on(8)?'think':(on(6)||on(9)||on(12)?'point':'present'),on(7)&&!on(8)?'worry':'happy');
    s+=hdr('②','賃貸とくらべた「稼ぎ方」',at(0,.4),T);
    if(on(1)&&!on(2)){const bars=(x,vals,c,lab)=>`<text x="${x+250}" y="340" text-anchor="middle" font-size="42" font-weight="900" fill="${c}">${lab}</text><path d="M${x} 680 H${x+500}" stroke="#9fb5a8" stroke-width="5"/>`+vals.map((v,k)=>`<rect x="${x+20+k*80}" y="${680-v*eo(at(1,1,.4+k*.08))}" width="56" height="${v*eo(at(1,1,.4+k*.08))}" rx="6" fill="${c}"/>`).join('');
      s+=card(560,280,600,480,bars(610,[200,200,200,200,200,200],'#8a8f98','賃貸：毎月ほぼ同じ'),at(1,.4))+card(1240,280,600,480,bars(1290,[120,250,190,300,90,260],T,'宿：上にも下にも'),at(1,.4,1.8));
      s+=pop(1540,810,at(1,.4,3.2),`<rect x="1250" y="770" width="580" height="80" rx="40" fill="${T}"/><text x="1540" y="824" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">稼働率 × 1泊の料金</text>`);}
    if(on(2)&&!on(3)){const it=[['1泊の料金','¥15,000',G,.6],['×','',DG,2.0],['月の泊数','15泊',G,2.6],['=','',DG,4.2],['月の売上','¥225,000',T,4.6]];
      s+=card(560,260,1280,480,`<rect x="600" y="290" width="90" height="50" rx="10" fill="${Y}"/><text x="645" y="326" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">例</text>`+it.map(([a,b,c,o],k)=>{const x=[740,950,1110,1330,1560][k];const p=at(2,.3,o);if(p<=0)return '';return b?`<g opacity="${p}"><text x="${x}" y="450" text-anchor="middle" font-size="36" font-weight="900" fill="#4a5a52">${a}</text><text x="${x}" y="560" text-anchor="middle" font-size="${b.length>7?64:72}" font-weight="900" fill="${c}">${b}</text></g>`:`<text x="${x}" y="560" text-anchor="middle" font-size="80" font-weight="900" fill="${c}" opacity="${p}">${a}</text>`}).join('')+`<text x="1200" y="680" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">料金か泊数を動かせば、売上が変わる</text>`,at(2,.4));}
    if(on(3)&&!on(4))s+=card(760,260,900,500,`${house(1210,640,.7,1)}<rect x="1010" y="300" width="400" height="90" rx="45" fill="${G}"/><text x="1210" y="360" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">家賃 月5万円</text><text x="1210" y="720" text-anchor="middle" font-size="30" font-weight="700" fill="#4a5a52">下田の一軒家（借りている物件）</text>`,at(3,.4));
    if(on(4)&&!on(5)){const g=k=>eo(at(4,.8,[2.4,4.4,6.2][k]));const base=700,sc=3.0;
      s+=card(600,250,1200,560,`<text x="1200" y="310" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">試運転の3か月（2025年）</text><path d="M680 ${base} H1720" stroke="#9fb5a8" stroke-width="5"/>
        <rect x="740" y="${base-100*sc*g(0)}" width="220" height="${100*sc*g(0)}" rx="8" fill="${G}"/><text x="850" y="${base+50}" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">売上</text>${g(0)>.9?`<text x="850" y="${base-100*sc-20}" text-anchor="middle" font-size="40" font-weight="900" fill="${G}">約100万円</text>`:''}
        <rect x="1090" y="${base-100*sc}" width="220" height="${55*sc*g(1)}" rx="8" fill="#b9c3cc"/><text x="1200" y="${base+50}" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">運営費</text>${g(1)>.9?`<text x="1200" y="${base-100*sc+55*sc/2+14}" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">約55万円</text>`:''}
        <rect x="1440" y="${base-45*sc*g(2)}" width="220" height="${45*sc*g(2)}" rx="8" fill="${T}"/><text x="1550" y="${base+50}" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">営業利益</text>${g(2)>.9?`<text x="1550" y="${base-45*sc-20}" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">約45万円</text>`:''}`,at(4,.4));}
    if(on(5)&&!on(6)){const parts=[['家賃',5,G,1.6],['清掃',2,'#7fb894',2.6],['予約サイトの手数料など',8,T,3.6],['光熱費・消耗品',3,Y,5.6]];let x0=640,sv='';
      parts.forEach(([w,v,c,o],k)=>{const wd=v*61,p=eo(at(5,.4,o));sv+=`<rect x="${x0}" y="420" width="${wd*p}" height="130" fill="${c}"/>`+(p>.9?`<text x="${x0+wd/2}" y="500" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">${v}万</text><text x="${x0+wd/2}" y="${k%2?640:610}" text-anchor="middle" font-size="${w.length>8?26:30}" font-weight="900" fill="${DG}">${w}</text>`:'');x0+=wd});
      s+=card(600,260,1200,480,`<text x="1200" y="340" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">運営費 月 約18万円の中身</text>${sv}`,at(5,.4));}
    if(on(6)&&!on(7)){const g=eo(at(6,1,.4));s+=card(700,250,1000,560,`<text x="1200" y="310" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">1か月あたり</text><path d="M780 710 H1620" stroke="#9fb5a8" stroke-width="5"/>
      <rect x="860" y="${710-5*24*g}" width="220" height="${5*24*g}" rx="8" fill="#8a8f98"/><text x="970" y="${710-5*24*g-20}" text-anchor="middle" font-size="40" font-weight="900" fill="#5a6068">5万円</text><text x="970" y="760" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">家賃（大家さん）</text>
      <rect x="1320" y="${710-15*24*g}" width="220" height="${15*24*g}" rx="8" fill="${T}"/><text x="1430" y="${710-15*24*g-20}" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">約15万円</text><text x="1430" y="760" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">宿の営業利益</text>`,at(6,.4))+stampX(1660,470,'約3倍',at(6,.3,3.0),RED,64,8);}
    if(on(7)&&!on(8))s+=card(640,260,1120,500,`<text x="1200" y="330" text-anchor="middle" font-size="44" font-weight="900" fill="${RED}">ここに入っていないもの</text>${[['自分たちの手間（人件費）',''],['改修・家具の初期投資','約650万円']].map(([a,b],k)=>`<rect x="700" y="${400+k*150}" width="1000" height="120" rx="20" fill="#fdecea"/><text x="740" y="${474+k*150}" font-size="42" font-weight="900" fill="${DG}">${a}</text><text x="1660" y="${474+k*150}" text-anchor="end" font-size="42" font-weight="900" fill="${RED}">${b}</text>`).join('')}`,at(7,.4));
    if(on(8)&&!on(9))s+=card(640,280,520,420,`<text x="900" y="400" text-anchor="middle" font-size="60" font-weight="900" fill="#8a8f98">1年目</text>${house(900,640,.45,.8)}`,at(8,.4))+card(1240,280,520,420,`<text x="1500" y="400" text-anchor="middle" font-size="60" font-weight="900" fill="${T}">2年目</text>${house(1500,640,.45,1)}${sparkle(1640,480,1,lt,1)}`,at(8,.4,1.2))+pop(1200,490,at(8,.4,1.8),`<circle cx="1200" cy="490" r="50" fill="${Y}"/><text x="1200" y="508" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">→</text>`);
    if(on(9)&&!on(10)){const g=k=>eo(at(9,.9,[2.6,6.0][k]));const grp=(x,lab,v,o)=>`<text x="${x+170}" y="320" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">${lab}</text><path d="M${x} 700 H${x+340}" stroke="#9fb5a8" stroke-width="5"/><rect x="${x+20}" y="${700-170}" width="130" height="170" rx="8" fill="#b9c3cc"/><text x="${x+85}" y="745" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">1年目</text><rect x="${x+190}" y="${700-170*v*g(o)}" width="130" height="${170*v*g(o)}" rx="8" fill="${T}"/><text x="${x+255}" y="745" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">2年目</text>${g(o)>.9?`<text x="${x+255}" y="${700-170*v-18}" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">約${v}倍</text>`:''}`;
      s+=card(600,260,1200,540,grp(680,'1泊の平均単価',1.4,0)+grp(1160,'1部屋あたりの売上',1.74,1)+`<text x="1200" y="790" text-anchor="middle" font-size="26" font-weight="700" fill="#888">2年目は上半期（4〜9月）の数字</text>`,at(9,.4));}
    if(on(10)&&!on(11)){const g=eo(at(10,1.2,1.6));const pie=(cx,f,c,lab,val)=>{const a=2*Math.PI*f,R=130;return `<circle cx="${cx}" cy="510" r="${R}" fill="#eef3ee"/><path d="M${cx} 510 L${cx} ${510-R} A${R} ${R} 0 ${a>Math.PI?1:0} 1 ${cx+R*Math.sin(a)} ${510-R*Math.cos(a)}Z" fill="${c}"/><circle cx="${cx}" cy="510" r="${R*.55}" fill="#fff"/><text x="${cx}" y="525" text-anchor="middle" font-size="44" font-weight="900" fill="${c}">${val}</text><text x="${cx}" y="710" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">${lab}</text>`};
      s+=card(600,260,1200,520,`<text x="1200" y="330" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">売上に占める、家賃の割合</text>${pie(900,.3,'#8a8f98','1年目','約30%')}${g>0?pie(1500,.3-.18*g,G,'2年目の上半期','約'+Math.round(30-18*g)+'%'):''}<text x="1200" y="525" text-anchor="middle" font-size="70" font-weight="900" fill="${DG}">→</text>`,at(10,.4));}
    if(on(11)&&!on(12)){const M=[['8月',58],['9月',60],['10月',52],['11月',33],['12月',71],['1月',39],['2月',57],['3月',61]];
      s+=card(580,250,1240,560,`<text x="1200" y="315" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">1年目の月別の稼働率</text><path d="M660 720 H1760" stroke="#9fb5a8" stroke-width="5"/><path d="M660 ${720-53*4.6} H1760" stroke="${T}" stroke-width="4" stroke-dasharray="14 10"/><rect x="1600" y="262" width="190" height="46" rx="23" fill="${T}"/><text x="1695" y="295" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">平均 約53%</text>`+M.map(([m,v],k)=>{const g=eo(at(11,.6,.3+k*.12)),x=690+k*132,hi=v===71||v===33;return `<rect x="${x}" y="${720-v*4.6*g}" width="96" height="${v*4.6*g}" rx="6" fill="${hi?(v===71?G:RED):'#b9d3c2'}"/><text x="${x+48}" y="765" text-anchor="middle" font-size="28" font-weight="900" fill="${DG}">${m}</text>${hi&&g>.9?`<text x="${x+48}" y="${720-v*4.6-16}" text-anchor="middle" font-size="34" font-weight="900" fill="${v===71?G:RED}">${v}%</text>`:''}`}).join(''),at(11,.4));}
    if(on(12)&&!on(13)){const g=eo(at(12,1,.8)),g2=eo(at(12,1,4.2));s+=card(640,250,1120,560,`<text x="1200" y="315" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">稼働率をくらべる</text><path d="M760 720 H1640" stroke="#9fb5a8" stroke-width="5"/>
      <rect x="840" y="${720-29.6*6*g}" width="240" height="${29.6*6*g}" rx="8" fill="#b9c3cc"/><text x="960" y="${720-29.6*6*g-20}" text-anchor="middle" font-size="42" font-weight="900" fill="#5a6068">29.6%</text><text x="960" y="765" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">全国の簡易宿所（2025年）</text>
      <rect x="1320" y="${720-53*6*g2}" width="240" height="${53*6*g2}" rx="8" fill="${G}"/>${g2>0?`<text x="1440" y="${720-53*6*g2-20}" text-anchor="middle" font-size="42" font-weight="900" fill="${G}">約53%</text>`:''}<text x="1440" y="765" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">私たちの宿（1年目）</text>`,at(12,.4));}
    if(on(13))s+=pop(1200,500,at(13,.4),`<rect x="640" y="380" width="1120" height="240" rx="120" fill="${T}"/><text x="1200" y="480" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">運営の腕で、</text><text x="1200" y="570" text-anchor="middle" font-size="56" font-weight="900" fill="#fff">稼ぎを伸ばせる資産</text>`);
  }
  if(i===3){ // 観光需要
    s+=aki(on(5)?'point':(on(4)&&!on(5)?'think':'present'));
    s+=hdr('③','世界の観光需要を取り込む',at(0,.4),'#3d8a6a');
    if(on(1)&&!on(4)){const data=[['2024年',3687,'#9fc7b0'],['2025年',4268,'#3d8a6a'],['2030年 目標',6000,'#fff']];const sc=.07;
      s+=card(600,250,1200,580,`<text x="1200" y="310" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">日本に来た外国人旅行者</text><path d="M700 760 H1700" stroke="#9fb5a8" stroke-width="5"/>`+data.map(([y,v,c],k)=>{const p=k<2?eo(at(1,.9,.4+k*.9)):(on(3)?eo(at(3,.9,.4)):0);if(p<=0)return '';const h=v*sc*p;return `<rect x="${780+k*320}" y="${760-h}" width="220" height="${h}" rx="8" fill="${c}" ${k===2?`stroke="#3d8a6a" stroke-width="6" stroke-dasharray="16 10"`:''}/><text x="${890+k*320}" y="${740-h}" text-anchor="middle" font-size="40" font-weight="900" fill="#2f6e55">${v.toLocaleString()}万人</text><text x="${890+k*320}" y="808" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">${y}</text>`}).join(''),at(1,.4));
      if(lt>L[1]+2.7)s+=stampX(1010,380,'過去最多',at(1,.3,3.4),RED,52,-6);
      if(on(2))s+=pop(1050,560,at(2,.4,2.6),`<rect x="960" y="520" width="190" height="70" rx="35" fill="${T}"/><text x="1055" y="567" text-anchor="middle" font-size="36" font-weight="900" fill="#fff">+約16%</text>`);}
    if(on(4)&&!on(5)){s+=card(560,250,1280,560,`<rect x="600" y="280" width="200" height="64" rx="32" fill="${Y}"/><text x="700" y="324" text-anchor="middle" font-size="36" font-weight="900" fill="${DG}">クイズ</text><text x="1200" y="410" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">外国人の宿泊のうち、地方の割合は？</text>`+[['A','1割'],['B','3割'],['C','5割']].map(([k2,w],k)=>{const x=760+k*440;return `<g opacity="${at(4,.3,[4.4,5.6,6.6][k])}"><rect x="${x-170}" y="500" width="340" height="220" rx="30" fill="#eef3ee"/><circle cx="${x}" cy="560" r="40" fill="${[G,T,'#3d8a6a'][k]}"/><text x="${x}" y="576" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">${k2}</text><text x="${x}" y="680" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">${w}</text></g>`}).join(''),at(4,.4));}
    const cd=lt-(L[5]-3.2);if(cd>0&&cd<3.2)s+=pop(1200,880,clamp((cd%1)*4),`<circle cx="1200" cy="880" r="60" fill="${Y}"/><text x="1200" y="905" text-anchor="middle" font-size="72" font-weight="900" fill="${DG}">${Math.max(1,3-Math.floor(cd))}</text>`);
    if(on(5)&&!on(7)){const p=eo(at(5,1.4,.6)),a=2*Math.PI*.663*p,R=200,cx=980,cy=540;const x2=cx+R*Math.sin(a),y2=cy-R*Math.cos(a);
      s+=card(600,250,1200,560,`<text x="1200" y="310" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">外国人の延べ宿泊者数（2025年）</text><circle cx="${cx}" cy="${cy}" r="${R}" fill="#f6d9b0"/><path d="M${cx} ${cy} L${cx} ${cy-R} A${R} ${R} 0 ${a>Math.PI?1:0} 1 ${x2} ${y2}Z" fill="#3d8a6a"/><circle cx="${cx}" cy="${cy}" r="${R*.55}" fill="#fff"/><text x="${cx}" y="${cy+16}" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">B 正解</text>
        <rect x="1240" y="420" width="40" height="40" rx="8" fill="#3d8a6a"/><text x="1300" y="453" font-size="36" font-weight="900" fill="${DG}">三大都市圏 約3分の2</text><rect x="1240" y="520" width="40" height="40" rx="8" fill="#f6d9b0"/><text x="1300" y="553" font-size="40" font-weight="900" fill="${T}">地方部 33.7%</text>`,at(5,.4));
      if(on(6))s+=qbubble('q3','地方には伸びる余地！',at(6,.4),t);}
    if(on(7)){s+=card(700,280,1000,520,`${house(1200,700,.7,1)}${sparkle(950,420,1.2,lt,0)}<rect x="900" y="310" width="600" height="80" rx="40" fill="${G}"/><text x="1200" y="364" text-anchor="middle" font-size="36" font-weight="900" fill="#fff">欧米からの長期滞在が中心</text>`,at(7,.4));
      s+=`<g transform="translate(${1500+60*Math.sin(lt)},${470}) rotate(-12)"><path d="M-70 0 L60 -8 Q86 -8 86 0 Q86 8 60 8 L-70 0Z" fill="#3d8a6a"/><path d="M-10 -4 L-50 -50 L-26 -50 L20 -4Z M-10 4 L-50 50 L-26 50 L20 4Z" fill="#3d8a6a"/></g>`;}
  }
  if(i===4){ // 税金
    s+=aki(on(2)&&!on(3)?'think':'present',on(2)&&!on(3)?'worry':'happy');
    s+=hdr('④','税金：正しく知る',at(0,.4),'#b8862f');
    if(on(1)&&!on(2)){s+=card(560,250,1280,560,`<rect x="620" y="300" width="300" height="140" rx="20" fill="${G}"/><text x="770" y="385" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">売上</text><text x="980" y="390" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">−</text><rect x="1040" y="300" width="300" height="140" rx="20" fill="#b9c3cc"/><text x="1190" y="385" text-anchor="middle" font-size="48" font-weight="900" fill="${DG}">経費</text><text x="1400" y="390" text-anchor="middle" font-size="64" font-weight="900" fill="${DG}">=</text><rect x="1460" y="300" width="320" height="140" rx="20" fill="#b8862f"/><text x="1620" y="385" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">所得</text>
        <text x="1190" y="490" text-anchor="middle" font-size="30" font-weight="900" fill="#4a5a52">清掃・手数料・光熱費など</text>`,at(1,.4));
      const dp=at(1,.4,4.2);if(dp>0)s+=fade(dp,`<text x="700" y="600" font-size="34" font-weight="900" fill="#b8862f">減価償却：家具・改修の費用を、何年かに分けて経費に</text>${[0,1,2,3,4].map(k=>`<rect x="${700+k*210}" y="640" width="180" height="${100*eo(seg(lt,L[1]+4.1+k*.22,L[1]+4.5+k*.22))}" rx="10" fill="#ecd6a8"/><text x="${790+k*210}" y="775" text-anchor="middle" font-size="26" font-weight="900" fill="#4a5a52">${k+1}年目</text>`).join('')}`,0);}
    if(on(2)&&!on(3)){s+=card(620,260,1160,520,`<text x="1200" y="330" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">民泊新法の宿の所得は、原則</text><rect x="980" y="360" width="440" height="110" rx="55" fill="#b8862f"/><text x="1200" y="435" text-anchor="middle" font-size="54" font-weight="900" fill="#fff">雑所得</text>
        <rect x="700" y="530" width="360" height="120" rx="20" fill="#fbf1de"/><text x="880" y="605" text-anchor="middle" font-size="40" font-weight="900" fill="#b8862f">宿の赤字</text><rect x="1340" y="530" width="360" height="120" rx="20" fill="#eef3ee"/><text x="1520" y="605" text-anchor="middle" font-size="40" font-weight="900" fill="${G}">給料</text><path d="M1080 590 H1320" stroke="#9fb5a8" stroke-width="8" stroke-dasharray="14 10"/>`,at(2,.4));
      s+=stampX(1200,590,'相殺できない',at(2,.3,5.4),RED,48,-6);}
    if(on(3)&&!on(4)){const g=eo(at(3,1,6.2));s+=card(620,250,1160,580,`<text x="1200" y="315" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">空き家の土地の固定資産税（200㎡以下の部分）</text><path d="M760 740 H1640" stroke="#9fb5a8" stroke-width="5"/>
        <rect x="840" y="680" width="240" height="60" rx="8" fill="#9fc7a8"/><text x="960" y="660" text-anchor="middle" font-size="36" font-weight="900" fill="${G}">特例あり 1/6</text><text x="960" y="790" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">住宅が建つ土地</text>
        <rect x="1320" y="${740-300*g}" width="240" height="${300*g}" rx="8" fill="${RED}"/>${g>.9?`<text x="1440" y="420" text-anchor="middle" font-size="40" font-weight="900" fill="${RED}">最大6倍</text>`:''}<text x="1440" y="790" text-anchor="middle" font-size="32" font-weight="900" fill="${DG}">勧告を受けると</text>`,at(3,.4));}
    if(on(4)&&!on(5)){s+=card(620,260,1160,520,`<rect x="660" y="290" width="90" height="50" rx="10" fill="${Y}"/><text x="705" y="326" text-anchor="middle" font-size="30" font-weight="900" fill="${DG}">例</text><text x="1200" y="360" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">土地の評価額 1,200万円（200㎡以下）の場合</text>
        <text x="900" y="470" text-anchor="middle" font-size="34" font-weight="900" fill="#4a5a52">特例あり</text><text x="900" y="580" text-anchor="middle" font-size="76" font-weight="900" fill="${G}">年2.8万円</text><text x="1200" y="570" text-anchor="middle" font-size="70" font-weight="900" fill="${DG}">→</text>
        ${at(4,.3,3.6)>0?`<g opacity="${at(4,.3,3.6)}"><text x="1500" y="470" text-anchor="middle" font-size="34" font-weight="900" fill="#4a5a52">勧告を受けると</text><text x="1500" y="580" text-anchor="middle" font-size="76" font-weight="900" fill="${RED}">年16.8万円</text></g>`:''}<text x="1200" y="700" text-anchor="middle" font-size="26" font-weight="700" fill="#888">税率1.4%で計算。実際の税額は、地域や調整のしくみで変わります</text>`,at(4,.4));}
    if(on(5)&&!on(6))s+=card(760,270,880,500,`${house(1200,700,.7,1)}${sparkle(980,390,1.2,lt,0)}${sparkle(1420,370,1,lt,2)}<rect x="960" y="300" width="480" height="80" rx="40" fill="${G}"/><text x="1200" y="354" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">手入れを続ける家</text>`,at(5,.4));
    if(on(6))s+=pop(1200,500,at(6,.4),`<rect x="700" y="400" width="1000" height="200" rx="100" fill="#b8862f"/><text x="1200" y="482" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">税金は条件で変わる</text><text x="1200" y="555" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">始める前に、税理士さんに確認</text>`);
  }
  if(i===5){ // 社会課題
    s+=aki(on(3)?'cheer':'present');
    s+=hdr('⑤','社会の課題を、ビジネスで解決',at(0,.4),DG);
    if(on(1)){const lit=on(2)?eo(at(2,1,.4)):0;
      s+=card(560,250,1280,580,`<text x="1200" y="320" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">空き家 約900万戸（住宅の約7軒に1軒）</text>${[0,1,2,3,4,5,6].map(k=>`<g opacity="${eo(at(1,.3,.3+k*.2))}">${house(700+k*167,660,.32,k===3?lit:1)}</g>`).join('')}${on(2)?'':`<text x="1201" y="720" text-anchor="middle" font-size="34" font-weight="900" fill="${RED}">空き家</text>`}`,at(1,.4));
      if(on(2)){[['カフェ',1000],['お店',1400]].forEach(([w,x],k)=>{s+=pop(x,780,at(2,.4,2+k*.6),`<rect x="${x-110}" y="745" width="220" height="70" rx="35" fill="${Y}"/><text x="${x}" y="792" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">${w}</text>`)});
        for(let c=0;c<3;c++){const f=((lt*.7+c/3)%1);if(lt>L[2]+1.8)s+=`<g opacity="${Math.sin(f*Math.PI)}">${coin(1201+(c%2?200:-200)*f,580+180*f,22)}</g>`}}
      if(on(3))s+=pop(1200,430,at(3,.4),`<rect x="760" y="370" width="880" height="120" rx="60" fill="${G}"/><text x="1200" y="448" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">増やしながら、町の役に立つ</text>`);}
  }
  if(i===6){ // 始め方は3つ
    s+=aki(on(4)?'point':'present');
    s+=hdr('','大事な前提：民泊の始め方は3つ',at(0,.4),G);
    const W=[['民泊新法','届出','年180日まで',G],['旅館業法','許可（簡易宿所など）','日数の上限なし',T],['特区民泊','一部の地域だけ','国家戦略特区',DG]];
    if(!on(5))W.forEach(([a,b,c,col],k)=>{const x=760+k*420,hi=on(4)&&k===1;s+=pop(x,500,on(1+k)?at(1+k,.4):0,`<g transform="translate(${x},500) scale(${hi?1.06:1}) translate(${-x},-500)" opacity="${on(4)&&k!==1?.4:1}">${box(x-190,260,380,480,30)}<rect x="${x-190}" y="260" width="380" height="110" rx="30" fill="${col}"/><text x="${x}" y="330" text-anchor="middle" font-size="44" font-weight="900" fill="#fff">${a}</text><text x="${x}" y="450" text-anchor="middle" font-size="${b.length>8?30:36}" font-weight="900" fill="${DG}">${b}</text><text x="${x}" y="560" text-anchor="middle" font-size="40" font-weight="900" fill="${col}">${c}</text></g>`)});
    if(on(4)&&!on(5))s+=pop(1180,800,at(4,.4,.6),`<rect x="920" y="760" width="520" height="80" rx="40" fill="${Y}"/><text x="1180" y="813" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">私たちの宿は、これ</text>`);
    if(on(5)){const g=eo(at(5,1.2,.4));s+=card(640,260,1120,520,`<text x="1200" y="330" text-anchor="middle" font-size="40" font-weight="900" fill="${DG}">営業できる日数＝売上の天井</text>${[['年180日まで',180,G],['日数の上限なし',365,T]].map(([w,v,c],k)=>`<text x="700" y="${450+k*150}" font-size="34" font-weight="900" fill="${DG}">${w}</text><rect x="980" y="${410+k*150}" width="${700*v/365*g}" height="60" rx="12" fill="${c}"/>`).join('')}`,at(5,.4));}
  }
  if(i===7){ // リスク
    s+=aki(on(1)?'point':'think','happy');
    s+=hdr('','リスクも、大きく3つ',at(0,.4));
    [['1','需要の波','季節・景気・感染症で、旅行者が大きく減ることも'],['2','ルール','民泊新法は年180日まで。条例でさらに短いことも'],['3','手間','清掃・ゲスト対応が続く。自分か、任せるか']].forEach(([n,a,b],k)=>{
      s+=checkRow2(560,300+k*170,1280,n,a,b,at(1+k)*(1-at(4,.3)))});
    if(on(4))s+=pop(1200,480,at(4,.4),`${box(660,300,1080,360,36)}<text x="1200" y="440" text-anchor="middle" font-size="58" font-weight="900" fill="${DG}">「誰でも簡単に</text><text x="1200" y="530" text-anchor="middle" font-size="58" font-weight="900" fill="${DG}">月100万円」</text>`)+stampX(1200,610,'まず疑う',at(4,.3,2.4),RED,60,-6);
  }
  if(i===8){ // 始める前に
    s+=aki(on(4)?'present':'point');
    s+=hdr('','始める前に：くらべる数字と、確かめること',at(0,.4),G);
    if(on(0)&&!on(3)){[['1','賃貸に出した場合の家賃'],['2','宿の営業利益 − 自分の手間'],['3','初期投資の回収期間']].forEach(([n,w],k)=>{const x=760+k*420,o=[0,3.2,7.0][k];s+=pop(x,430,on(1)?at(1,.4,o):0,`${box(x-190,250,380,330,30)}<circle cx="${x}" cy="330" r="46" fill="${T}"/><text x="${x}" y="348" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">${n}</text><text x="${x}" y="${w.length>10?450:470}" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">${w.length>10?w.slice(0,8):w}</text>${w.length>10?`<text x="${x}" y="500" text-anchor="middle" font-size="34" font-weight="900" fill="${DG}">${w.slice(8)}</text>`:''}`)});
      if(on(2)){const g=eo(at(2,1.6,.6));s+=pop(1180,710,at(2,.4),`${box(620,630,1120,170,30)}<text x="660" y="690" font-size="32" font-weight="900" fill="${DG}">私たちの宿：約14か月で、初期投資の</text><rect x="660" y="720" width="900" height="44" rx="22" fill="#eef3ee"/><rect x="660" y="720" width="${900*.98*g}" height="44" rx="22" fill="${G}"/><text x="1600" y="755" font-size="40" font-weight="900" fill="${G}">${Math.round(98*g)}%</text>`)+stampX(1640,620,'1つの例',at(2,.3,4.2),T,36,6);}}
    if(on(3)){[['営業できるか（法律・条例）','doc'],['まわりの需要と競合','search'],['建物の状態と改修費','hammer'],['運営の体制','chat']].forEach(([w,ic],k)=>{const x=k%2?1260:620,y=k<2?280:520;s+=pop(x+280,y+100,at(3,.4,[1.6,4.0,6.4,8.8][k]),`${box(x,y,560,200,30)}${icon(x+90,y+100,56,ic,G,'#fff',.85)}<text x="${x+160}" y="${y+112}" font-size="${w.length>10?28:34}" font-weight="900" fill="${DG}">${w}</text><path d="M${x+500} ${y+40} l14 18 l28 -34" stroke="${T}" stroke-width="10" fill="none" stroke-linecap="round" opacity="${at(3,.3,[1.6,4.0,6.4,8.8][k]+1)}"/>`)});
      if(on(4))s+=qbubble('q7','数字とチェック、両方！',at(4,.4),t);}
  }
  if(i===9){ // 失敗しない入れ方
    s+=aki(on(3)?'present':(on(1)?'point':'present'));
    if(!on(1))s+=pop(1200,460,at(0,.5),`<rect x="800" y="300" width="800" height="320" rx="40" fill="${Y}"/><text x="1200" y="420" text-anchor="middle" font-size="46" font-weight="900" fill="${DG}">失敗しない入れ方</text><text x="1200" y="560" text-anchor="middle" font-size="120" font-weight="900" fill="${DG}">？</text>`);
    if(on(1)&&!on(2)){const p=eo(at(1,1.2,.6)),R=210,cx=960,cy=500;const parts=[['預金',.4,'#8a8f98'],['株・投資信託',.45,'#3d6a8a'],['民泊',.15,T]];let a0=0,sv='';
      parts.forEach(([w,f,c])=>{const a1=a0+2*Math.PI*f*p,x1=cx+R*Math.sin(a0),y1=cy-R*Math.cos(a0),x2=cx+R*Math.sin(a1),y2=cy-R*Math.cos(a1);sv+=`<path d="M${cx} ${cy} L${x1} ${y1} A${R} ${R} 0 ${a1-a0>Math.PI?1:0} 1 ${x2} ${y2}Z" fill="${c}" stroke="#fff" stroke-width="6"/>`;a0=a1});
      s+=pop(1200,500,at(1,.4),`${box(580,230,1240,560,30)}${sv}${parts.map(([w,f,c],k)=>`<rect x="1260" y="${360+k*100}" width="40" height="40" rx="8" fill="${c}"/><text x="1320" y="${393+k*100}" font-size="40" font-weight="900" fill="${DG}">${w}</text>`).join('')}<text x="1200" y="760" text-anchor="middle" font-size="26" font-weight="700" fill="#888">割合はイメージです</text>`);
      s+=pop(1560,710,at(1,.4,3.6),`<rect x="1330" y="660" width="460" height="100" rx="50" fill="${T}"/><text x="1560" y="725" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">一部として、小さく</text>`);}
    if(on(2)&&!on(3))s+=card(760,240,880,540,`${house(1200,680,.75,1)}<rect x="1000" y="280" width="400" height="84" rx="42" fill="${G}"/><text x="1200" y="337" text-anchor="middle" font-size="42" font-weight="900" fill="#fff">買わずに借りた家</text>`,at(2,.4))+stampX(1560,700,'準備 約7か月',at(2,.3,2.6),T,44,-6);
    if(on(3)&&!on(4)){s+=reasonGrid(3,.5);
      s+=pop(1200,660,at(3,.4,7),`<rect x="800" y="610" width="800" height="100" rx="50" fill="${Y}"/><text x="1200" y="676" text-anchor="middle" font-size="42" font-weight="900" fill="${DG}">リスクを知って、一部として、小さく</text>`);}
    if(on(4)&&!on(5))s+=pop(1200,470,at(4,.4),`${box(700,300,1000,340,36)}${icon(1200,420,70,'chat',G,'#fff',1)}<text x="1200" y="560" text-anchor="middle" font-size="44" font-weight="900" fill="${DG}">あなたなら、資産のどれくらい？</text><text x="1200" y="615" text-anchor="middle" font-size="34" font-weight="900" fill="${T}">コメントで教えてください</text>`);
    if(on(5))s+=pop(1200,470,at(5,.5),`${box(620,250,1160,420,36)}${LOGO(890,290,1.3)}<rect x="760" y="420" width="880" height="100" rx="50" fill="${T}"/><text x="1200" y="487" text-anchor="middle" font-size="48" font-weight="900" fill="#fff">民泊が成り立つか、無料で相談</text><text x="1200" y="610" text-anchor="middle" font-size="38" font-weight="900" fill="${DG}">概要欄のリンクから</text>`);
    s+=fade(seg(lt,E[5]+.5,E[5]+1.2),`<rect width="1920" height="1080" fill="#16301f"/><text x="960" y="380" text-anchor="middle" font-size="60" font-weight="900" fill="#fff">最後まで見てくれて、ありがとうございます</text><text x="960" y="480" text-anchor="middle" font-size="30" font-weight="700" fill="#dfe9e3">${NOTE}</text><text x="960" y="530" text-anchor="middle" font-size="30" font-weight="700" fill="#dfe9e3">出典は概要欄に記載しています。</text><text x="960" y="630" text-anchor="middle" font-size="30" font-weight="700" fill="#b8c9bf">${CREDIT}</text><rect x="780" y="700" width="360" height="100" rx="50" fill="#fff"/>${LOGO(810,715,1.1)}`,0);
  }
  const TT={1:['理由 ①','分散',G],2:['理由 ②','稼ぎ方',T],3:['理由 ③','観光需要','#3d8a6a'],4:['理由 ④','税金','#b8862f'],5:['理由 ⑤','社会課題',DG],6:['大事な前提','始め方は3つ',G],7:['知っておく','リスク',RED],8:['始める前に','くらべる・確かめる',G]};
  if(TT[i]&&L.length>1&&lt<L[1]){const [a,b,c]=TT[i],p=at(0,.4,.1)*(1-seg(lt,L[1]-.35,L[1]-.05));s+=pop(1180,480,p,`${box(700,300,960,360,40)}<rect x="${1180-130}" y="270" width="260" height="76" rx="38" fill="${c}"/><text x="1180" y="322" text-anchor="middle" font-size="40" font-weight="900" fill="#fff">${a}</text><text x="1180" y="${b.length>6?540:560}" text-anchor="middle" font-size="${b.length>6?88:120}" font-weight="900" fill="${c}">${b}</text>`);}
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
            f"const THEME={json.dumps([s[0] for s in SCENES])};const CREDIT={json.dumps(CREDIT, ensure_ascii=False)};const NOTE={json.dumps(NOTE, ensure_ascii=False)};")
    return h[:a] + head + SCENE_JS + h[b:]


def main():
    args = sys.argv[1:]
    hq = "--hq" in args; args = [x for x in args if x != "--hq"]
    prev = None
    if "--preview" in args:
        k = args.index("--preview"); prev = [float(x) for x in args[k + 1:]]; args = args[:k]
    nocheck = "--no-check" in args; args = [x for x in args if x != "--no-check"]
    out = args[0] if args else os.path.join(tempfile.gettempdir(), "akiyado-strategy-ep1.mp4")
    if prev is None and not nocheck:  # 書き出しの前に、文字の重なり・はみ出しを自動点検（layout_check.py）
        r = subprocess.run([sys.executable, os.path.join(HERE, "layout_check.py"), "make_strategy_ep1", "--step", "0.5"])
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
