# -*- coding: utf-8 -*-
"""izu-from-tokyo の書き直し（2026-11-15 品質保証部の3回目の採点、リサーチメモ 3、編集長の時刻表の確認にもとづく）。content.py の ARTICLES の1件と同じ形。
運賃表は content.py の TRAIN_TABLE_EN/JA を使わず、本文に直接書く（運賃の数字は一次で確かめられていないので、黄色い枠で人に回す）。"""

SOURCES_NEW = {
    "jre_odoriko": ("https://www.jreast.co.jp/en/multi/traininformation/odoriko/", "JR East", "JR東日本", "JR East: Limited Express Odoriko"),
    "jre_tt_tokyo": ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetables", "JR東日本の時刻表",
                     "JR East timetables from Tokyo Station: Tokaido Shinkansen and Tokaido, Ito and Izukyu lines (November 2026)"),
    "jre_fare2026": ("https://www.jreast.co.jp/es/2026unchin-kaitei/", "JR East", "JR東日本", "JR East: Fare revision of 14 March 2026"),
    "jre_widepass": ("https://www.jreast.co.jp/en/multi/pass/tokyowidepass.html", "JR East", "JR東日本", "JR East: JR TOKYO Wide Pass"),
    "jrp_price": ("https://japanrailpass.net/en/purchase/price/", "Japan Rail Pass (JR Group)", "JRグループ", "JR Group: Japan Rail Pass types and prices"),
    "izu_tokko": ("https://kanko.city.izu.shizuoka.jp/sightseeing/tokkonoyu/", "Izu City", "伊豆市", "Izu City tourism: Tokko-no-yu"),
    "shimoda_ohama": ("https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html", "Shimoda City", "下田市",
                      "Shimoda City: Shirahama Ohama Beach"),
    "shimoda_beach2026_city": ("https://city.shimoda.shizuoka.jp/file/広報しもだ令和8年8月号2-3頁.pdf", "Shimoda City newsletter, August 2026",
                               "広報しもだ 2026年8月号", "Shimoda City newsletter, August 2026: beaches open in Shimoda"),
    "ekitan_saphir": ("https://ekitan.com/en/article/saphir-odoriko", "Ekitan", "駅探",
                      "Ekitan: Saphir Odoriko — all-Green-Car limited express to Izu, and what rail-pass holders need to pay"),
    "mlit_izuhakone2026": ("https://wwwtb.mlit.go.jp/chubu/press/pdf/tethudo20261016.pdf", "Chubu District Transport Bureau (MLIT)",
                           "国土交通省中部運輸局", "Chubu District Transport Bureau: Izuhakone Railway fare-ceiling application (16 October 2026)"),
    "mlit_izuhakone2022": ("https://wwwtb.mlit.go.jp/kanto/content/000284727.pdf", "Chubu District Transport Bureau (MLIT)",
                           "国土交通省中部運輸局", "Chubu District Transport Bureau: Approval of Izuhakone Railway fare revision (26 December 2022)"),
}

ARTICLE = {
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, passes and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Passes and Where to Stay",
 "description": "Five direct Odoriko trains a day run from Tokyo to Shimoda in about 2½ hours. The JR Tokyo Wide Pass covers four; the Saphir Odoriko needs a Green Car ticket.",
 "dek": "The south of the Izu Peninsula is too far for a comfortable day trip and just right for a week. Five direct Odoriko trains a day take you from Tokyo to Shimoda in about two and a half hours. The JR Tokyo Wide Pass gets you on four of them, while the all-Green-Car Saphir Odoriko costs extra.",
 "card": "Five direct Odoriko trains a day reach Shimoda from Tokyo in about 2½ hours, and the JR Tokyo Wide Pass covers four of them. The south of Izu is a long way for a day, but just right for a week. As of November 2026.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—")],
 "intent": "Do（やり方を知りたい）",
 "points": [
   "Five direct Odoriko trains a day leave Tokyo between 9:00 and 13:00 and reach Shimoda in about 2 hours 30 minutes to 2 hours 45 minutes (JR East timetable, November 2026). A day trip there means about five hours on the train.",
   "For Shuzenji, you can take the Shinkansen to Mishima, about 50 to 53 minutes on a Kodama, and then the Izuhakone Railway, about 35 minutes. Two direct trains a day also run, at 9:00 and 12:00.",
   "The JR Tokyo Wide Pass (¥16,000 for three days, foreign passports only) covers four of the five daily direct trains in ordinary cars. The 11:00 Saphir Odoriko is all Green Car, so you’ll need an extra Green Car ticket for it. The Japan Rail Pass doesn’t cover the line south of Ito.",
   "In 2026, Shimoda’s nine official beaches opened on 18 July. Most closed on 23 August, Shirahama Chuo on 30 August, and Shirahama Ohama and Kujukihama on 31 August. Lifeguards are only there in the season.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The simplest way is the Odoriko limited express, which runs from Tokyo down the east coast of the [[l:izu|Izu Peninsula]] to Shimoda without a change. In JR East’s November 2026 timetable, five run every day, leaving Tokyo on the hour from 9:00 to 13:00. They take about 1 hour 40 minutes to Ito and about 2 hours 30 minutes to 2 hours 45 minutes to Izukyu-Shimoda [[s:jre_tt_tokyo]]. If you’re heading to Shuzenji, there are a couple of other routes that can suit you better.</p>
<div class="tablewrap"><table>
<thead><tr><th>Route</th><th>Changes</th><th>Time</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Direct Odoriko</strong> to Ito and Izukyu-Shimoda</td><td>None</td><td>About 1 h 40 min to Ito, about 2 h 30 min to 2 h 45 min to Shimoda [[s:jre_tt_tokyo]]</td><td>Five a day, leaving Tokyo at 9:00, 10:00, 11:00, 12:00 and 13:00. The 11:00 is the all-Green-Car Saphir Odoriko, which needs a Green Car ticket even if you have a rail pass [[s:ekitan_saphir]]. Extra trains run on set days [[s:jre_tt_tokyo]].</td></tr>
<tr><td><strong>Shinkansen to Atami</strong>, then a local train to Shimoda</td><td>One, at Atami</td><td>About 43 to 45 min to Atami by Kodama, then about 1 h 29 min to 1 h 49 min to Shimoda [[s:jre_tt_tokyo]]</td><td>With a good connection it can beat the direct train. The 6:30 Kodama and the 7:23 local from Atami get you to Shimoda at 8:52, in 2 h 22 min [[s:jre_tt_tokyo]]. It also helps when the direct times don’t suit you.</td></tr>
<tr><td><strong>Shinkansen to Mishima</strong>, then the Izuhakone Railway to Shuzenji</td><td>One, at Mishima</td><td>About 50 to 53 min to Mishima by Kodama [[s:jre_tt_tokyo]], then about 35 min to Shuzenji [[s:jg6311]]</td><td>We’d expect this to suit most days, since only two direct trains run to Shuzenji.</td></tr>
<tr><td><strong>Direct Odoriko</strong> to Shuzenji</td><td>None</td><td>About 2 h 6 min to 2 h 8 min [[s:jre_tt_tokyo]]</td><td>Two a day, leaving Tokyo at 9:00 and 12:00. A third, at 10:30, runs only on set days [[s:jre_tt_tokyo]].</td></tr>
</tbody></table></div>
<p class="fine">Train times are from JR East’s Tokyo Station timetables for November 2026. Timetables change with the seasons, so do check the times for your travel date.</p>
[[ed:Confirm the December 2026 Odoriko times and operating days, and the Saphir Odoriko Green Car charge for pass holders on JR East’s own pages.]]
<p>As for the fare, the one-way fare and limited-express charge depend on the date and seat, so the easiest way to see yours is JR East’s Ekinet booking site. JR East also revised its fares on 14 March 2026 [[s:jre_fare2026]], which means older fare tables online may be out of date.</p>
[[ed:On Ekinet, check the one-way adult fare with a reserved seat, as of November 2026, from Tokyo to Atami, Ito, Shuzenji and Izukyu-Shimoda. Secondary sites give ¥3,670, ¥4,000, ¥4,750 and ¥6,660. Add them to the table only if they match, with the date checked.]]
<p>What about the bus? For Shimoda and Shuzenji, we think the train is the practical way in.</p>
[[ed:Confirm whether any direct highway bus runs from Tokyo or Shinjuku to Shimoda or Shuzenji. Also decide whether to mention the Mishima Express highway bus (Busta Shinjuku–Mishima, Tokai Bus); its times and fare are only on secondary sites so far, so confirm them on Tokai Bus’s own page first.]]

<h2>Can you use the Japan Rail Pass or the JR Tokyo Wide Pass to get to Izu?</h2>
<p>Yes, but they don’t reach the same places, so it depends on where you’re going.</p>
<div class="tablewrap"><table>
<thead><tr><th>Pass</th><th>Price and length</th><th>What it covers in Izu</th></tr></thead>
<tbody>
<tr><td><strong>JR Tokyo Wide Pass</strong></td><td>¥16,000 for adults, three days in a row, foreign passport holders only, from 14 March 2026 [[s:jre_widepass]]</td><td>JR East lines in its area, including limited expresses on the Izu Kyuko line to Shimoda [[s:jre_widepass]]. That means four of the five daily direct trains in ordinary cars. The Saphir Odoriko is all Green Car, so it needs a separate Green Car reserved-seat ticket [[s:ekitan_saphir]].</td></tr>
<tr><td><strong>Japan Rail Pass</strong></td><td>¥50,000 for seven days when bought online in yen, ¥53,000 through overseas agents (JR Group notice, 9 April 2026) [[s:jrp_price]]</td><td>The JR sections. You pay extra on the Izu Kyuko line south of Ito [[s:jg6305]].</td></tr>
</tbody></table></div>
<p>The Izuhakone Railway from Mishima to Shuzenji isn’t a JR line, so on the Japan Rail Pass you pay that fare separately. It’s ¥550 as of November 2026, the fare since April 2023 [[s:jg6305,mlit_izuhakone2022]]. The railway applied in October 2026 to raise its fares, with the change on this line planned for spring 2027 if it’s approved [[s:mlit_izuhakone2026]].</p>
[[ed:Confirm on JR East’s Tokyo Wide Pass page whether the Tokaido Shinkansen and the Izuhakone Railway are excluded. Confirm in the Chubu District Transport Bureau papers (16 October 2026) that the Mishima–Shuzenji change is planned for spring 2027.]]

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is, but the south really isn’t. Even on the direct train, Shimoda is about two and a half hours from Tokyo [[s:jre_tt_tokyo]], so a return trip means about five hours on the train for a few hours on the beach. Atami and Ito are closer to Tokyo and work fine as day trips. We think the south coast and the inland hot-spring towns are far better if you stay.</p>

<h2>Which Izu town suits you?</h2>
<p>It mostly comes down to how far you want to go and how long you can stay.</p>
<div class="tablewrap"><table>
<thead><tr><th>Town</th><th>From Tokyo</th><th>What it’s like</th><th>Day trip or stay?</th></tr></thead>
<tbody>
<tr><td><strong>Atami and Ito</strong></td><td>Atami about 43–45 min by Shinkansen; Ito about 1 h 40 min direct</td><td>The two towns nearest Tokyo, on the east coast. We think they’re the ones that work as a day out, since you can see the sea and soak in a hot spring and still be home for dinner.</td><td>A day trip works</td></tr>
<tr><td><strong>Shuzenji</strong></td><td>About 50–53 min to Mishima, then about 35 min; or about 2 h 6 min direct</td><td>An inland hot-spring town along a river [[s:uncharted]]. Its best-known spring, Tokko-no-yu, is for looking at only [[s:izu_tokko]], though there’s a foot bath nearby. We think it suits a quiet night or two more than a rushed visit.</td><td>Better to stay</td></tr>
<tr><td><strong>Shimoda</strong></td><td>About 2 h 30 min to 2 h 45 min direct</td><td>A port town at the southern tip, with nine official swimming beaches in 2026 [[s:shimoda_beach2026_city]]. JNTO puts Shirahama Beach about 15 minutes by bus from the station [[s:jnto]], and the prefecture describes the harbour as Japan’s top landing port for [[l:kinmedai|kinmedai]] [[s:pref]]. In our view, it’s the town that suits a week best.</td><td>Better to stay</td></tr>
</tbody></table></div>
<p class="fine">Times are from the route table above.</p>
[[ed:On Izu City’s tourism site, confirm that there’s a foot bath near Tokko-no-yu that visitors can use, with its name, hours and fee (Sugi-no-yu or Kawara-yu?). If not, remove “though there’s a foot bath nearby”.]]

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>For swimming, it’s mid-July to late August. For a quieter stay, we’d pick the months either side.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Swimming season (in 2026, from 18 July to between 23 and 31 August, depending on the beach)</td><td>All nine of Shimoda’s official beaches opened on 18 July 2026, mostly from 8:00 to 16:00. Shirahama Ohama and Kujukihama stayed open until 31 August and Shirahama Chuo until 30 August, but the other six closed on 23 August [[s:shimoda_beach2026_city]]. Outside the season and those hours, there are no lifeguards [[s:shimoda_ohama]].</td></tr>
<tr><td>Late May to September</td><td>In good weather the sea is pleasant [[s:jg6304]]. Outside the school holidays, we’d expect fewer people around.</td></tr>
<tr><td>The rest of the year</td><td>The towns get much quieter. In our view, it’s the easiest time for hot springs and long walks.</td></tr>
</tbody></table></div>
<p class="fine">The city sets the beach dates each year, so if you’re planning a late-August trip, check which beaches will still be open. Dates for 2027 hadn’t been announced in November 2026.</p>

<h2>What changes when you rent a house in Izu?</h2>
<p>A house turns a short visit into an ordinary week. A hotel room is built around one or two nights and a set dinner time, while a house gives you a kitchen, a washing machine and a table to work at. A typical day ends up as work in the morning, the beach or a hot spring in the afternoon, and dinner at home when you don’t feel like going out.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, about ten minutes on foot from Izukyu-Shimoda Station.]]
<p>If you’d like to try that in Shimoda, our home there, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, has a work desk, a washing machine and dryer, a properly equipped kitchen and self check-in with a smart lock. It’s about ten minutes on foot from Izukyu-Shimoda Station, with restaurants, a convenience store and a supermarket close by.</p>
<p>If a week in Izu gets you thinking about a longer stay, or even a house of your own, here’s why we suggest [[l:akiya-try-first|living in a town for a month before buying a house]].</p>
[[ed:Add the measured Wi-Fi speed and the time of the last bus from the beaches.]]

<h2>What are the downsides of staying in Izu?</h2>
<p>Getting around takes a bit of planning. The daily direct trains from Tokyo all leave between 9:00 and 13:00 [[s:jre_tt_tokyo]], so your travel day is easier if you build it around them. If none of them fits, you can take the Shinkansen to Atami and change there, and an early start that way can even get you in sooner. Once you’re in Izu, beaches and villages outside the main towns are reached by local bus, and buses aren’t frequent, so a look at the timetable before you set out saves a long wait. If you want to hop between beaches, we think an e-bike or a rental car makes life much easier.</p>
""",
 "faq": [
   ("How long does it take to get from Tokyo to Shimoda?",
    "About 2 hours 30 minutes to 2 hours 45 minutes on the direct Odoriko limited express. Five run a day, leaving Tokyo between 9:00 and 13:00 (JR East timetable, November 2026) [[s:jre_tt_tokyo]]."),
   ("Can I use the Japan Rail Pass to get to Izu?",
    "Partly. It covers the JR sections, but you pay extra on the Izu Kyuko line south of Ito, and the Izuhakone Railway to Shuzenji is a separate fare [[s:jg6305]]. The JR Tokyo Wide Pass does cover the Izu Kyuko line’s limited expresses [[s:jre_widepass]], though the all-Green-Car Saphir Odoriko needs an extra Green Car ticket [[s:ekitan_saphir]]."),
   ("What’s the best way to get to Shuzenji?",
    "You can take the Shinkansen to Mishima, about 50 to 53 minutes on a Kodama [[s:jre_tt_tokyo]], and then the Izuhakone Railway, about 35 minutes [[s:jg6311]]. Two direct Odoriko trains also run every day, at 9:00 and 12:00, with a third on set days [[s:jre_tt_tokyo]]."),
   ("Is there a bus from Tokyo to Shimoda?",
    "For Shimoda and Shuzenji, we think the train is the practical way in. Five direct trains a day reach Shimoda in about two and a half hours [[s:jre_tt_tokyo]]."),
   ("Do I need a car on the Izu Peninsula?",
    "Not to get to Shimoda or Shuzenji. You’ll only really miss one when you want to move between beaches."),
 ],
 "sources": ["jre_tt_tokyo", "ekitan_saphir", "jre_fare2026", "jre_widepass", "jrp_price", "jg6305", "jg6311",
             "jg6304", "jnto", "uncharted", "izu_tokko", "shimoda_ohama", "shimoda_beach2026_city", "mlit_izuhakone2022",
             "mlit_izuhakone2026", "pref"],
 "related": ["kinmedai", "izu"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・パスと、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りにはつらく、1週間ならちょうどいい距離です。東京から下田までは、直通の特急「踊り子」が1日5本、2時間半ほどで走ります。JR東京ワイド・パスなら、そのうち4本にパスだけで乗れます。全車グリーン車の「サフィール踊り子」は別料金です。",
  "review": [
   "【2026-11-15 品質保証部（HTML）の指摘での書き直し】変えた点: ①ワイド・パス: 全車グリーン車のサフィール踊り子（11:00発）は、パスがあっても別にグリーン車の指定席券が要ることを、description・dek・In short の3点目・行き方の表・パスの表・FAQ に入れました（「毎日5本のうち4本は普通車でパスだけで乗れる、サフィールは別料金」）。出典に駅探の英語のサフィール踊り子の記事（ekitan_saphir）を足しました ②「熱海乗り換えは直通より速くない」を直し、「乗り継ぎがよければ直通より速いこともある。こだま6:30発→熱海7:23発の普通→下田8:52着（2時間22分）」にしました。弱点の節の一言も合わせました ③時刻の出典を東京駅の時刻表の入口（jre_tt_tokyo）にまとめ、jre_tt_kodama・jre_tt_local を外しました。数字は品質保証部が11月の時刻表で確かめた値（こだま 東京→熱海43〜45分・東京→三島50〜53分、熱海→下田の普通1時間29〜49分）に。こだまの下りの所要時間の黄色い枠は外しました ④「多くの人は三島へ新幹線で」「学校の休み以外は人が少ない」を、私たちの見方（〜と見ています）に直しました ⑤高速バス: 「見つけられなかった」をやめ、「電車がいちばん現実的な行き方だと私たちは思う」と答え、直行便の有無は黄色い枠に（本文・FAQ） ⑥修善寺の足湯は「近くに足湯があります」だけにし、旅行者が使えるか・名前・時間・料金を黄色い枠で確かめる形に ⑦日本語版の伊豆半島のリンクを日本語版の記事（ja-izu）に ⑧一覧のカード（card）を、目次の読み上げから答え（毎日5本・約2時間半・パスは4本・南は1週間向き）に替えました",
   "【今回、人に確かめてほしい点】①サフィール踊り子のグリーン料金（パスを持つ人がいくら払うか）は書いていません。JR東日本の公式で確かめて、入れるか（黄色い枠） ②出典の駅探は民間のサイトです。JR東日本のワイド・パスのページで同じことが確かめられれば、そちらに替えたいです ③修善寺の足湯（黄色い枠） ④東京・新宿から下田・修善寺への直行の高速バスの有無（黄色い枠）",
   "【2026-11-15 3回目の書き直し（事実の変更あり）】変えた点: ①直通の本数・時間を、JR東日本の東京駅の時刻表（2026年11月、編集長が開いて確認。出典 jre_tt_tokyo を新しく追加）に合わせました。前の「下田まで2時間49分」（JR東日本の英語の案内ページ）をやめ、「毎日の直通は東京を9:00〜13:00に毎時ちょうど出る5本、下田まで約2時間30分〜2時間45分（11:00発は全車グリーン車のサフィール踊り子）、ほかに決まった日だけの列車もある」にしました。dek・description・In short・FAQ・日帰りの節・弱点の節も同じです ②修善寺への直通を「1日3本」から「毎日2本（9:00・12:00発、約2時間6〜8分）、10:30発は決まった日だけ」に直しました（前回のゲートの原因） ③伊東は時刻表の数字で「約1時間40分」（1時間36〜45分）。出典を jre_tt_tokyo に替えました ④こだまの東京→熱海を「約47分」から「約45分」に（JR東日本で確かめたのは上り〔熱海→東京 約47分〕だけなので、下りの確認を黄色い枠に）。東京→三島も「約50〜55分」に丸めました ⑤熱海→下田の普通は「約1時間30分〜1時間50分」に ⑥「時刻表は季節で変わるので、乗る日の時刻を確かめて」と一言添えました ⑦運賃: 「片道の運賃・特急料金は日付と席で変わるので、えきねっとで見るのがいちばん簡単」と本文で答え、金額の確認は黄色い枠のまま ⑧高速バス: 「東京・新宿から下田・修善寺への直行の高速バスは見つけられなかったので、電車が現実的」と本文と FAQ（新しく1問）で答えました。三島エクスプレスに触れるかは黄色い枠で編集長の判断に回しています ⑨修善寺の「無料の足湯 杉の湯」を消し、「近くに足を入れられる小さな足湯がある」にとどめました（名前・料金の確認は黄色い枠） ⑩「JR East gives the journey as」を言い換え、「it’s worth」を4回から0回に減らしました ⑪出典から jre_izu と jre_izu_tt（2026年10〜11月の PDF）を外しました",
   "【人に確かめてほしい点】①えきねっとで、東京→熱海・伊東・修善寺・伊豆急下田の片道（大人・普通車指定席、2026年11月時点）を確認し、表に入れるか（黄色い枠） ②2026年12月の踊り子の時刻・運転日（黄色い枠。こだまの下りの時間は品質保証部が11月の時刻表で確認済み） ③高速バス（三島エクスプレス）に触れるか（黄色い枠。時刻・運賃は二次の情報だけ） ④修善寺の足湯（杉の湯・河原湯）の名前・時間・料金（黄色い枠） ⑤ワイド・パスで東海道新幹線・伊豆箱根鉄道が対象外か、伊豆箱根鉄道の値上げが三島〜修善寺で2027年春の予定か（黄色い枠） ⑥回線速度の実測値と、浜からの最終バスの時刻（黄色い枠） ⑦白浜までバスで約15分は JNTO の記載で、2026年のダイヤでは確かめていません ⑧町の表の「私たちの見方」（熱海・伊東は日帰り向き、修善寺は1〜2泊、下田は1週間）が、運営者の感覚と合っているか",
   "【入れられなかったこと】運賃の数字（一次で未確認）。三島エクスプレスの時刻・運賃（二次の情報だけ）。伊豆箱根鉄道の値上げ後の額（二次の情報だけ）。2026年12月の時刻（未確認）",
  ],
  "points": [
    "東京から下田へは、毎日5本の直通の特急「踊り子」が東京を9時〜13時に出て、約2時間30分〜2時間45分で着きます（JR東日本の時刻表、2026年11月）。日帰りだと、電車に5時間ほど乗ることになります。",
    "修善寺へは、新幹線（こだまで東京〜三島 約50〜53分）で三島へ出て、伊豆箱根鉄道で約35分です。直通も毎日2本（9:00・12:00発）あります。",
    "JR東京ワイド・パス（16,000円・3日間・外国のパスポートの人だけ）なら、毎日5本の直通のうち4本に普通車で乗れます。11:00発の「サフィール踊り子」は全車グリーン車なので、別にグリーン券が要ります。ジャパン・レール・パスは、伊東より南の区間には使えません。",
    "2026年、下田の9つの海水浴場は7月18日に開きました。多くは8月23日に閉じ、白浜中央は8月30日、白浜大浜と九十浜は8月31日まで。監視員がいるのは期間中だけです。",
  ],
  "body": """
<h2>東京から伊豆半島への行き方</h2>
<p>いちばん簡単なのは、特急「踊り子」です。東京から[[l:ja-izu|伊豆半島]]の東海岸を下田まで、乗り換えなしで走ります。JR東日本の2026年11月の時刻表では、毎日5本が、9時から13時まで毎時ちょうどに東京を出ます。伊東まで約1時間40分、伊豆急下田まで約2時間30分〜2時間45分です[[s:jre_tt_tokyo]]。修善寺へ行くなら、ほかの行き方のほうが合うこともあります。</p>
<div class="tablewrap"><table>
<thead><tr><th>行き方</th><th>乗り換え</th><th>所要時間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>直通の「踊り子」</strong>で伊東・伊豆急下田へ</td><td>なし</td><td>伊東まで約1時間40分、下田まで約2時間30分〜2時間45分[[s:jre_tt_tokyo]]</td><td>毎日5本で、東京を9:00・10:00・11:00・12:00・13:00に出ます。11:00発は全車グリーン車の「サフィール踊り子」で、レールパスがあってもグリーン券が要ります[[s:ekitan_saphir]]。ほかに、決まった日だけ走る列車もあります[[s:jre_tt_tokyo]]。</td></tr>
<tr><td><strong>新幹線で熱海</strong>へ出て、普通列車で下田へ</td><td>1回（熱海）</td><td>こだまで熱海まで約43〜45分、熱海から下田まで約1時間29〜49分[[s:jre_tt_tokyo]]</td><td>乗り継ぎがよければ、直通より速く着くこともあります。こだま6:30発、熱海7:23発の普通に乗り継ぐと、下田に8:52に着きます（2時間22分）[[s:jre_tt_tokyo]]。直通の時間が合わないときにも便利です。</td></tr>
<tr><td><strong>新幹線で三島</strong>へ出て、伊豆箱根鉄道で修善寺へ</td><td>1回（三島）</td><td>こだまで三島まで約50〜53分[[s:jre_tt_tokyo]]、三島から修善寺まで約35分[[s:jg6311]]</td><td>修善寺への直通は2本だけなので、たいていの日はこちらが合うと私たちは見ています。</td></tr>
<tr><td><strong>直通の「踊り子」</strong>で修善寺へ</td><td>なし</td><td>約2時間6〜8分[[s:jre_tt_tokyo]]</td><td>毎日2本で、東京を9:00と12:00に出ます。10:30発の3本目は、決まった日だけです[[s:jre_tt_tokyo]]。</td></tr>
</tbody></table></div>
<p class="fine">電車の時刻は、JR東日本の東京駅の時刻表（2026年11月）によります。時刻表は季節で変わるので、乗る日の時刻を確かめてください。</p>
[[ed:2026年12月の踊り子の時刻・運転日と、パスを持つ人がサフィール踊り子に乗るときのグリーン料金を、JR東日本の公式のページで確かめてください。]]
<p>運賃については、片道の運賃と特急料金は日付や席で変わるので、JR東日本の予約サイト「えきねっと」で見るのがいちばん簡単です。JR東日本は2026年3月14日に運賃を改定したので[[s:jre_fare2026]]、ネットにある古い運賃表は当てにならないことがあります。</p>
[[ed:えきねっとで、2026年11月時点の東京→熱海・伊東・修善寺・伊豆急下田の片道（大人・普通車指定席）の運賃を確認してください。二次のサイトでは 3,670円・4,000円・4,750円・6,660円。一致したら、確認した日を添えて表に入れてください。]]
<p>バスはどうか。下田や修善寺へは、電車がいちばん現実的な行き方だと私たちは思います。</p>
[[ed:東京・新宿から下田・修善寺への直行の高速バスがあるかを確かめてください。あわせて、高速バス「三島エクスプレス」（バスタ新宿〜三島、東海バス）に触れるかを決めてください。時刻と運賃は、いまのところ二次のサイトにしかないので、触れるなら先に東海バスの公式で確かめてください。]]

<h2>伊豆へ行くのに、ジャパン・レール・パスや JR東京ワイド・パスは使えるか</h2>
<p>使えます。ただ、使える範囲がそれぞれ違うので、行き先しだいです。</p>
<div class="tablewrap"><table>
<thead><tr><th>パス</th><th>値段と日数</th><th>伊豆で使える範囲</th></tr></thead>
<tbody>
<tr><td><strong>JR東京ワイド・パス</strong></td><td>大人16,000円、連続3日間、外国のパスポートを持つ人だけ（2026年3月14日から）[[s:jre_widepass]]</td><td>エリア内の JR東日本の路線と、下田までの伊豆急行線の特急[[s:jre_widepass]]。毎日5本の直通のうち4本に、普通車で乗れます。サフィール踊り子は全車グリーン車なので、別にグリーン車の指定席券が要ります[[s:ekitan_saphir]]。</td></tr>
<tr><td><strong>ジャパン・レール・パス</strong></td><td>7日間で、オンラインで円で買うと50,000円、海外の代理店では53,000円（2026年4月9日の JR グループのお知らせ）[[s:jrp_price]]</td><td>JR の区間。伊東より南の伊豆急行線は別料金です[[s:jg6305]]。</td></tr>
</tbody></table></div>
<p>三島から修善寺までの伊豆箱根鉄道は JR ではないので、ジャパン・レール・パスでは別に運賃を払います。2026年11月時点で550円で、2023年4月からこの運賃です[[s:jg6305,mlit_izuhakone2022]]。鉄道会社は2026年10月に運賃の値上げを申請していて、認められれば、この区間は2027年春に変わる予定です[[s:mlit_izuhakone2026]]。</p>
[[ed:JR東日本のワイド・パスのページで、東海道新幹線と伊豆箱根鉄道が対象外と明記されているかを確かめてください。中部運輸局の資料（2026年10月16日）で、三島〜修善寺の値上げが2027年春の予定かも確かめてください。]]

<h2>伊豆半島は、東京から日帰りできるか</h2>
<p>北のほうはできますが、南はあまり向きません。直通の電車でも下田まで2時間半ほどかかるので[[s:jre_tt_tokyo]]、往復すると、浜で過ごす数時間のために5時間ほど電車に乗ることになります。東京に近い熱海や伊東なら、日帰りでも十分楽しめます。南の海岸と内陸の温泉町は、泊まったほうがずっと楽しめると私たちは思います。</p>

<h2>伊豆のどの町が合うか</h2>
<p>決め手は、どこまで行きたいかと、どれくらいいられるかです。</p>
<div class="tablewrap"><table>
<thead><tr><th>町</th><th>東京から</th><th>どんな町か</th><th>日帰りか、泊まりか</th></tr></thead>
<tbody>
<tr><td><strong>熱海と伊東</strong></td><td>熱海まで新幹線で約43〜45分、伊東まで直通で約1時間40分</td><td>東海岸の、東京にいちばん近い2つの町。海を眺めて温泉に入り、夕食には帰れるので、日帰りに向いているのはこの2つだと私たちは思います。</td><td>日帰りでも楽しめる</td></tr>
<tr><td><strong>修善寺</strong></td><td>三島まで約50〜53分、そこから約35分。または直通で約2時間6分</td><td>川沿いの内陸の温泉町です[[s:uncharted]]。いちばん有名な「独鈷の湯」は見るだけの湯ですが[[s:izu_tokko]]、近くに足湯があります。慌ただしく立ち寄るより、1〜2泊して静かに過ごすのが合う町だと私たちは思います。</td><td>泊まるのがおすすめ</td></tr>
<tr><td><strong>下田</strong></td><td>直通で約2時間30分〜2時間45分</td><td>半島の南端の港町で、2026年は正式な海水浴場が9つありました[[s:shimoda_beach2026_city]]。JNTO によると、白浜海岸は駅からバスで約15分で[[s:jnto]]、静岡県は、この港を[[l:ja-kinmedai|金目鯛]]の水揚げ日本一の港と説明しています[[s:pref]]。1週間過ごすのにいちばん合う町だと、私たちは思います。</td><td>泊まるのがおすすめ</td></tr>
</tbody></table></div>
<p class="fine">時間は上の行き方の表によります。</p>
[[ed:伊豆市の観光サイトで、独鈷の湯の近くに旅行者が使える足湯があるか、名前・時間・料金（杉の湯か河原湯か）を確かめてください。なければ「近くに足湯があります」を消します。]]

<h2>伊豆半島はいつ行くのがいいか</h2>
<p>泳ぐなら7月中旬から8月下旬。静かに過ごしたいなら、私たちはその前後の月を選びます。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>どんな感じか</th></tr></thead>
<tbody>
<tr><td>海水浴の期間（2026年は7月18日から、浜によって8月23〜31日まで）</td><td>2026年は、下田の9つの海水浴場がすべて7月18日に開き、多くは8時〜16時でした。白浜大浜と九十浜は8月31日まで、白浜中央は8月30日まで開いていましたが、ほかの6つは8月23日に閉じました[[s:shimoda_beach2026_city]]。期間外と時間外は、監視員がいません[[s:shimoda_ohama]]。</td></tr>
<tr><td>5月下旬〜9月</td><td>天気がよければ海は気持ちよく[[s:jg6304]]、学校の休み以外は人も少なめだろうと私たちは見ています。</td></tr>
<tr><td>それ以外</td><td>町はぐっと静かになります。温泉や長い散歩には、いちばん過ごしやすい時期だと私たちは思います。</td></tr>
</tbody></table></div>
<p class="fine">海水浴場の期間は、市が毎年決めます。8月の終わりに行くなら、どの浜がまだ開いているか確かめてください。2027年の期間は、2026年11月の時点ではまだ発表されていませんでした。</p>

<h2>伊豆で家を借りると、何が変わるか</h2>
<p>家を借りると、短い旅が、ふだんの1週間に変わります。ホテルの部屋は1〜2泊と決まった夕食の時間が前提ですが、家ならキッチン、洗濯機、仕事ができる机があります。午前は仕事、午後は浜か温泉、出かける気分でない夜は家で夕食。だいたいそんな一日になります。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて約10分の「NODE Shimoda」のリビング。]]
<p>下田で試してみたいなら、私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」には、ワークデスク、洗濯機と乾燥機、調理器具のそろったキッチンがあり、スマートロックでセルフチェックインできます。伊豆急下田駅から歩いて約10分で、飲食店、コンビニ、スーパーもすぐ近くです。</p>
<p>伊豆で1週間過ごして、もっと長く住むことや、自分の家を持つことが気になり始めたら、[[l:ja-akiya-try-first|家を買う前に1か月その町に住む]]ことをすすめる理由も読んでみてください。</p>
[[ed:回線速度の実測値と、浜からの最終バスの時刻を入れてください。]]

<h2>伊豆に泊まる弱点は何か</h2>
<p>移動には、少し計画が要ります。東京から毎日走る直通列車は、どれも9時〜13時に出るので[[s:jre_tt_tokyo]]、移動の日はこの列車に合わせて組み立てると楽です。どれも合わなければ、新幹線で熱海まで行って乗り換える手もあり、朝早く出ればそのほうが早く着くこともあります。着いてからも、大きな町の外の浜や集落へは路線バスで行くことになり、本数も多くないので、出かける前に時刻表を見ておくと待ちぼうけを防げます。浜から浜へ移動したいなら、電動自転車かレンタカーがあると、ぐっと動きやすくなると私たちは思います。</p>
""",
  "faq": [
    ("東京から下田まで、何時間かかりますか",
     "直通の特急「踊り子」で約2時間30分〜2時間45分です。毎日5本が、東京を9時〜13時に出ます（JR東日本の時刻表、2026年11月）[[s:jre_tt_tokyo]]。"),
    ("伊豆へ行くのに、ジャパン・レール・パスは使えますか",
     "一部で使えます。JR の区間は対象ですが、伊東より南の伊豆急行線は別料金で、修善寺までの伊豆箱根鉄道も別の運賃です[[s:jg6305]]。JR東京ワイド・パスなら、伊豆急行線の特急にも乗れます[[s:jre_widepass]]。ただし、全車グリーン車のサフィール踊り子は、別にグリーン券が要ります[[s:ekitan_saphir]]。"),
    ("修善寺へは、どう行くのがいいですか",
     "新幹線で三島へ出て（こだまで約50〜53分）[[s:jre_tt_tokyo]]、伊豆箱根鉄道で約35分です[[s:jg6311]]。直通の「踊り子」も毎日2本（9:00・12:00発）あり、決まった日にはもう1本走ります[[s:jre_tt_tokyo]]。"),
    ("東京から下田へのバスはありますか",
     "下田や修善寺へは、電車がいちばん現実的な行き方だと私たちは思います。直通の電車が毎日5本、下田まで2時間半ほどで走っています[[s:jre_tt_tokyo]]。"),
    ("伊豆半島で車は必要ですか",
     "下田や修善寺へ行くだけなら要りません。車がほしくなるのは、浜から浜へ移動したいときくらいです。"),
  ],
 },
}
