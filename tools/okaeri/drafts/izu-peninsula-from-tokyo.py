# -*- coding: utf-8 -*-
"""izu-from-tokyo の書き直し（2026-11-16、手離れ）。content.py の ARTICLES の1件と同じ形。
黄色い枠をすべてなくし、確かめられないこと（パスの範囲と値段、改定後の JR だけの運賃、最終バス、Wi-Fi の実測）は書かない。
運賃は伊豆急行と伊豆箱根鉄道の公式の運賃表、バスは東海バスの公式、時刻は JR東日本の時刻表（2026年11月）と伊豆箱根鉄道の時刻表による。
出典はすべて 2026-11-16 に開いて確かめた（jre_tt_tokyo と shimoda_beach2026_city・shimoda_ohama は 2026-11-15 に編集長・品質保証部が確認）。"""

SOURCES_NEW = {
    "jre_tt_tokyo": ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetables", "JR東日本の時刻表",
                     "JR East timetables from Tokyo Station: Tokaido Shinkansen and Tokaido, Ito and Izukyu lines (November 2026)"),
    "izukyu_fares": ("https://www.izukyu.co.jp/fares/index.php", "Izukyu", "伊豆急行（各駅運賃表）",
                     "Izu Kyuko Railway: Fares between stations (revised 14 March 2026)"),
    "izukyu_express": ("https://www.izukyu.co.jp/fares/express.php", "Izukyu (express charges)", "伊豆急行（特急・新幹線料金）",
                       "Izu Kyuko Railway: Limited express, Green Car and Shinkansen charges (checked November 2026)"),
    "izuhakone_fares": ("https://www.izuhakone.co.jp/sunzudaiyu/zunzu_sub_nav/schedule/p010102.html", "Izuhakone Railway (fares)",
                        "伊豆箱根鉄道（運賃表）", "Izuhakone Railway: Fare table for the Sunzu Line (checked November 2026)"),
    "izuhakone_tt": ("https://www.izuhakone.co.jp/sunzudaiyu/sunzu-recommendation-article/p010438.html", "Izuhakone Railway (timetable)",
                     "伊豆箱根鉄道（駿豆線の時刻表）", "Izuhakone Railway: Sunzu Line timetable (revised 15 March 2025, checked November 2026)"),
    "izuhakone_fare2026": ("https://www.izuhakone.co.jp/izu-group/izu-news/p010993.html", "Izuhakone Railway (fare application)",
                           "伊豆箱根鉄道（運賃の改定申請）", "Izuhakone Railway: Application to revise fares (15 October 2026)"),
    "tokaibus_highway": ("https://www.tokaibus.jp/kousoku/", "Tokai Bus (highway buses)", "東海バス（高速バス）",
                         "Tokai Bus: Highway bus routes (checked November 2026)"),
    "tokaibus_freepass": ("https://www.tokaibus.jp/rosen/freekippu_shimoda_minamiizu.html", "Tokai Bus (bus passes)",
                          "東海バス（下田・南伊豆のフリーきっぷ）", "Tokai Bus: Shimoda and Minami-Izu two-day bus passes (checked November 2026)"),
    "izu_tokko": ("https://kanko.city.izu.shizuoka.jp/sightseeing/tokkonoyu/", "Izu City", "伊豆市", "Izu City tourism: Tokko-no-yu"),
    "shimoda_ohama": ("https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html", "Shimoda City", "下田市",
                      "Shimoda City: Shirahama Ohama Beach"),
    "shimoda_beach2026_city": ("https://city.shimoda.shizuoka.jp/file/広報しもだ令和8年8月号2-3頁.pdf", "Shimoda City newsletter, August 2026",
                               "広報しもだ 2026年8月号", "Shimoda City newsletter, August 2026: beaches open in Shimoda"),
    "node_access": ("https://nodeshimoda.com/access", "NODE Shimoda (access)", "NODE Shimoda 公式サイト（アクセス）",
                    "NODE Shimoda official site: access (checked November 2026)"),
}

ARTICLE = {
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-16",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, fares and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Fares and Where to Stay",
 "description": "Direct trains reach Shimoda from Tokyo in about 2½ hours, for ¥4,280 plus a ¥2,380 seat charge. Routes to Shuzenji, buses without a car and the best season.",
 "dek": "Southern Izu is too far for a day trip but just right for a week. Direct trains reach Shimoda from Tokyo in 2 hours 29 to 44 minutes (November 2026).",
 "card": "Direct trains reach Shimoda from Tokyo in about 2½ hours, for about ¥6,660 one way with a reserved seat. The south of Izu is a long way for a day, but just right for a week.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—")],
 "intent": "Do（やり方を知りたい）",
 "points": [
   "Shuzenji is about two hours direct, or about 50 minutes by Shinkansen to Mishima plus a 35-minute local line.",
   "In 2026, the swimming season ran from 18 July to late August, the only time lifeguards were on duty.",
   "Without a car, Tokai Bus’s two-day Shimoda pass (¥1,350) covers the town, Shirahama and Tsumekizaki.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The easiest way is the Odoriko limited express, which runs from Tokyo down the east coast of the [[l:izu|Izu Peninsula]] to Shimoda without a change. In JR East’s November 2026 timetable, five leave Tokyo every day, on the hour from 9:00 to 13:00. They take 1 hour 36 to 45 minutes to Ito and 2 hours 29 to 44 minutes to Izukyu-Shimoda [[s:jre_tt_tokyo]]. If you’re heading inland to Shuzenji, the Shinkansen and a short local line often suit you better.</p>
<div class="tablewrap"><table>
<thead><tr><th>Route</th><th>Changes</th><th>Time</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Direct Odoriko</strong> to Ito and Izukyu-Shimoda</td><td>None</td><td>About 1 h 40 min to Ito, 2 h 29 min to 2 h 44 min to Shimoda [[s:jre_tt_tokyo]]</td><td>Five a day, leaving Tokyo at 9:00, 10:00, 11:00, 12:00 and 13:00, with extra trains on set days [[s:jre_tt_tokyo]]. The 11:00 is the Saphir Odoriko, which only has Green Car and premium seats [[s:izukyu_express]].</td></tr>
<tr><td><strong>Shinkansen to Atami</strong>, then a local train to Shimoda</td><td>One, at Atami</td><td>43 to 45 min to Atami by Kodama, then 1 h 29 min to 1 h 49 min to Shimoda [[s:jre_tt_tokyo]]</td><td>With a good connection, it can beat the direct train. The 6:30 Kodama and the 7:23 local from Atami get you to Shimoda at 8:52, in 2 h 22 min [[s:jre_tt_tokyo]].</td></tr>
<tr><td><strong>Shinkansen to Mishima</strong>, then the Izuhakone Railway to Shuzenji</td><td>One, at Mishima</td><td>50 to 53 min to Mishima by Kodama [[s:jre_tt_tokyo]], then about 35 min to Shuzenji [[s:izuhakone_tt]]</td><td>Local trains to Shuzenji run about three times an hour for most of the day [[s:izuhakone_tt]], so we’d expect this to suit most days.</td></tr>
<tr><td><strong>Direct Odoriko</strong> to Shuzenji</td><td>None</td><td>2 h 6 min to 2 h 8 min [[s:jre_tt_tokyo]]</td><td>Two a day, leaving Tokyo at 9:00 and 12:00. A third, at 10:30, runs only on set days [[s:jre_tt_tokyo]].</td></tr>
</tbody></table></div>
<p class="fine">Times are from JR East’s Tokyo Station timetables for November 2026 and the Izuhakone Railway’s Sunzu Line timetable. Timetables change with the seasons, so it’s a good idea to look up the times for your travel date.</p>
<p>What about the bus? Tokai Bus, the main bus company on the peninsula, doesn’t run a highway bus from Tokyo to Shimoda or Shuzenji. Its Mishima Express goes from Shinjuku to Mishima, from ¥2,300 one way [[s:tokaibus_highway]], and from Mishima the Izuhakone Railway takes you on to Shuzenji [[s:izuhakone_tt]]. For Shimoda, we think the train is the simplest way to go.</p>

<h2>How much does the train from Tokyo to Izu cost?</h2>
<p>To Shimoda on the direct Odoriko, you’ll pay about ¥6,660 one way with a reserved seat. That’s the ¥4,280 fare plus a ¥2,380 seat charge bought before you board, using Izukyu’s fare tables after the 14 March 2026 revision [[s:izukyu_fares,izukyu_express]].</p>
<div class="tablewrap"><table>
<thead><tr><th>What you pay</th><th>One way, adult</th></tr></thead>
<tbody>
<tr><td>Fare, Tokyo to Izukyu-Shimoda</td><td>¥4,280 (¥4,276 with an IC card) [[s:izukyu_fares]]</td></tr>
<tr><td>Odoriko seat charge, Tokyo to Shimoda</td><td>¥2,380 bought before boarding, ¥2,640 on the train [[s:izukyu_express]]</td></tr>
<tr><td>Saphir Odoriko Green Car charge, Tokyo to Shimoda</td><td>¥6,260 in the normal season, up to ¥400 more at the busiest times and ¥200 less in quiet ones [[s:izukyu_express]]</td></tr>
<tr><td>Shinkansen charge, Tokyo to Atami</td><td>¥2,290 reserved, ¥1,760 unreserved, in the normal season, on top of the fare [[s:izukyu_express]]</td></tr>
<tr><td>Local train, Atami to Shimoda</td><td>¥2,210 [[s:izukyu_fares]]</td></tr>
<tr><td>Izu Kyuko line, Ito to Shimoda</td><td>¥1,860 (¥1,856 with an IC card) [[s:izukyu_fares]]</td></tr>
<tr><td>Izuhakone Railway, Mishima to Shuzenji</td><td>¥550 [[s:izuhakone_fares]]</td></tr>
</tbody></table></div>
<p class="fine">Fares as of November 2026. The Izuhakone Railway applied in October 2026 to raise its fares, with the change on the Mishima–Shuzenji line planned for spring 2027 [[s:izuhakone_fare2026]].</p>
<p>The line south of Ito belongs to Izukyu, and the line to Shuzenji to the Izuhakone Railway, not JR. So if you’re travelling on a rail pass, look up what it covers on these two lines before you go, rather than finding out at the gate.</p>

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is, but the south really isn’t. Even on the direct train, Shimoda is about two and a half hours from Tokyo [[s:jre_tt_tokyo]], so a return trip means about five hours on the train for a few hours on the beach. Atami is about 45 minutes away by Shinkansen and Ito about 1 hour 40 minutes on the direct train, so we think both work as day trips. The south coast and the inland hot-spring towns, in our view, are far better if you stay.</p>

<h2>Which Izu town suits you?</h2>
<p>It mostly comes down to how far you want to go and how long you can stay.</p>
<div class="tablewrap"><table>
<thead><tr><th>Town</th><th>From Tokyo</th><th>What it’s like</th><th>Day trip or stay?</th></tr></thead>
<tbody>
<tr><td><strong>Atami and Ito</strong></td><td>Atami 43–45 min by Shinkansen; Ito about 1 h 40 min direct</td><td>The two towns nearest Tokyo, on the east coast. In our view, they’re the ones that work as a day out, since you can spend a few hours by the sea and still be back in Tokyo for dinner.</td><td>A day trip works</td></tr>
<tr><td><strong>Shuzenji</strong></td><td>50–53 min to Mishima, then about 35 min; or about 2 h direct</td><td>An inland hot-spring town, said to be the oldest in Izu. You can look at the Tokko-no-yu spring but not bathe in it, and there are two foot baths nearby, Kawara-yu and Sugi-no-yu [[s:izu_tokko]]. We think it suits a quiet night or two more than a rushed visit.</td><td>Better to stay</td></tr>
<tr><td><strong>Shimoda</strong></td><td>2 h 29 min to 2 h 44 min direct</td><td>A port town at the southern tip, with nine official swimming beaches in 2026 [[s:shimoda_beach2026_city]]. The prefecture describes its fish market as Japan’s top landing port for [[l:kinmedai|kinmedai]] [[s:pref]]. In our view, it’s the town that suits a week best.</td><td>Better to stay</td></tr>
</tbody></table></div>

<h2>Can you get around southern Izu without a car?</h2>
<p>Yes, for the town and the nearby beaches. Shirahama Beach is about 15 minutes by bus from Izukyu-Shimoda Station, on a bus bound for Itadoichiki [[s:jnto]]. Tokai Bus sells two-day passes that cover most of what you’d want to see, valid on the day you buy them and the next [[s:tokaibus_freepass]].</p>
<div class="tablewrap"><table>
<thead><tr><th>Pass</th><th>Adult price</th><th>Where it takes you</th></tr></thead>
<tbody>
<tr><td><strong>Shimoda 2-day pass</strong></td><td>¥1,350</td><td>Shimoda town, Ryugu cave, Tsumekizaki and Shirahama [[s:tokaibus_freepass]]</td></tr>
<tr><td><strong>Irozaki–Shimoda 2-day pass</strong></td><td>¥2,850</td><td>All of the above, plus Cape Irozaki, Yumigahama, Shimokamo, Kawazu and Inatori [[s:tokaibus_freepass]]</td></tr>
</tbody></table></div>
<p>You buy them at Tokai Bus’s office by Shimoda Station, open every day from 8:45 to 12:30 and 13:30 to 17:00 [[s:tokaibus_freepass]]. Buses to the outer beaches don’t run often, so we’d look up the return times before heading out. If you want to hop between several beaches in one day, we think an e-bike or a rental car makes life much easier.</p>

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>For swimming, it’s mid-July to late August. For a quieter stay, we’d pick the months either side.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Swimming season (in 2026, from 18 July to between 23 and 31 August, depending on the beach)</td><td>All nine of Shimoda’s official beaches opened on 18 July 2026, mostly from 8:00 to 16:00. Shirahama Ohama and Kujukihama stayed open until 31 August and Shirahama Chuo until 30 August, but the other six closed on 23 August [[s:shimoda_beach2026_city]]. Outside the season and those hours, there are no lifeguards [[s:shimoda_ohama]].</td></tr>
<tr><td>Either side of the season</td><td>We’d expect fewer people around, outside the school holidays and long weekends.</td></tr>
<tr><td>The rest of the year</td><td>The towns get much quieter. In our view, it’s the easiest time for hot springs and long walks.</td></tr>
</tbody></table></div>
<p class="fine">The city sets the beach dates each year, so if you’re planning a late-August trip, it’s a good idea to see which beaches will still be open.</p>

<h2>Why stay a week in Izu rather than a night?</h2>
<p>A week turns a trip into ordinary life, and that’s when the slow pace of the south starts to make sense. A hotel room is built around one or two nights and a set dinner time. A place with a kitchen and a washing machine lets you work in the morning, head to the beach or a hot spring in the afternoon, and eat in when you don’t feel like going out.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, eight minutes on foot from Izukyu-Shimoda Station.]]
<p>If you’d like to try that in Shimoda, our apartment in the old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is set up for that kind of week. It’s about 40 m² on the first floor, with a work desk, a washing machine and gas dryer, and a kitchen with cookware [[s:node_room]]. It’s eight minutes’ walk on the flat from Izukyu-Shimoda Station, with a convenience store two minutes away and a supermarket three [[s:node_access]].</p>
<p>If a week in Izu gets you thinking about a longer stay, or even a house of your own, here’s why we suggest [[l:akiya-try-first|living in a town for a month before buying a house]].</p>
""",
 "faq": [
   ("How long does it take to get from Tokyo to Shimoda?",
    "2 hours 29 to 44 minutes on the direct Odoriko limited express. Five run a day, leaving Tokyo between 9:00 and 13:00 (JR East timetable, November 2026) [[s:jre_tt_tokyo]]."),
   ("How much is the train from Tokyo to Shimoda?",
    "About ¥6,660 one way on the Odoriko with a reserved seat: the ¥4,280 fare plus a ¥2,380 seat charge bought before boarding (Izukyu’s fare tables, November 2026) [[s:izukyu_fares,izukyu_express]]."),
   ("What’s the best way to get to Shuzenji?",
    "You can take the Shinkansen to Mishima, 50 to 53 minutes on a Kodama [[s:jre_tt_tokyo]], and then the Izuhakone Railway, about 35 minutes for ¥550 [[s:izuhakone_tt,izuhakone_fares]]. Two direct Odoriko trains also run every day, at 9:00 and 12:00, taking about two hours [[s:jre_tt_tokyo]]."),
   ("Is there a bus from Tokyo to Shimoda?",
    "Tokai Bus doesn’t run one. Its highway buses go to Mishima, including the Mishima Express from Shinjuku from ¥2,300 [[s:tokaibus_highway]]. For Shimoda, we think the train is the simplest way to go."),
   ("Do I need a car on the Izu Peninsula?",
    "Not for Shimoda town and the nearby beaches. Shirahama is about 15 minutes by bus from the station [[s:jnto]], and Tokai Bus’s two-day Shimoda pass costs ¥1,350 [[s:tokaibus_freepass]]. In our view, a car only really helps when you want to hop between beaches."),
 ],
 "sources": ["jre_tt_tokyo", "izukyu_fares", "izukyu_express", "izuhakone_tt", "izuhakone_fares", "izuhakone_fare2026",
             "tokaibus_highway", "tokaibus_freepass", "jnto", "izu_tokko", "shimoda_beach2026_city", "shimoda_ohama", "pref",
             "node_room", "node_access"],
 "related": ["kinmedai", "izu", "akiya-try-first"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・運賃と、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りには遠く、1週間ならちょうどいい距離です。下田へは、東京から直通の特急で2時間29〜44分です（2026年11月）。",
  "review": [
   "【2026-11-16 手離れでの書き直し（事実・出典の変更あり）】変えた点: ①黄色い枠を4つともなくしました ②ジャパン・レール・パスと JR東京ワイド・パスの範囲・値段を書くのをやめました（公式のページが開けず確かめられないため）。パスの節をなくし、「伊東より南は伊豆急行、修善寺へは伊豆箱根鉄道で、JR ではないので、パスで旅する人は、この2つの路線で何が使えるかを行く前に調べて」の一言だけにしました。出典 jre_widepass・jrp_price・ekitan_saphir・jre_odoriko・jre_fare2026 を外しました ③運賃の節を新しく作りました。伊豆急行の公式の運賃表（2026年3月14日改定）で、東京〜伊豆急下田 4,280円＋踊り子の指定席の特急料金 2,380円（乗る前に買う場合。車内は2,640円）＝約6,660円。サフィール踊り子のグリーンは通常期6,260円（最繁忙期は400円まで高く、閑散期は200円安い）、東京〜熱海の新幹線の特急料金（通常期・指定席2,290円・自由席1,760円）、熱海〜下田の普通 2,210円、伊東〜下田 1,860円。japan-guide の2025年12月の目安（約6,500円など）はやめました ④伊豆箱根鉄道の三島〜修善寺は、公式の運賃表で550円、時刻表（2025年3月改正）で約35分・昼間は1時間に3本ほど。出典を japan-guide から公式に替えました。値上げは、伊豆箱根鉄道の公式のお知らせ（2026年10月15日申請、駿豆線は2027年春の予定）に替えました ⑤直行バスは「東海バスには東京から下田・修善寺への高速バスがない。高速バスは三島行き」までにし、「どの会社にもない」と読める書き方をやめました ⑥車なしで回る節を新しく作りました。白浜海岸まで駅から板戸一色行きのバスで約15分（JNTO。前の「10〜15分」を直しました）、東海バスの「下田2日券」1,350円・「石廊崎・下田2日券」2,850円（買った日と翌日、下田駅前案内所で 8:45〜12:30・13:30〜17:00、年中無休）。浜からの最終バスの時刻は書いていません ⑦修善寺: 公式の伊豆市観光のページで「独鈷の湯は見るだけで入浴も足湯もできない。近くに河原湯、対岸に杉の湯の足湯がある」「伊豆最古の温泉街と言われる」を確かめ、名前を入れました。出典の uncharted を外しました ⑧修善寺の所要時間: 「直通でも新幹線経由でも約2時間」は、新幹線経由のほうが乗っている時間が短い（こだま50〜53分＋約35分）ので、In short を「直通で約2時間、または新幹線で三島まで約50分と35分のローカル線」に直しました ⑨東京〜下田の時間を、dek・本文・表・FAQ とも JR東日本の時刻表（2026年11月）の毎日の直通「2時間29〜44分」にそろえました（前の dek は Ekitan の2時間35分） ⑩NODE Shimoda: 「家（house）」をやめ「アパートの一室」に。公式サイトどおり約40㎡・2階・ワークデスク・洗濯機とガス乾燥機・調理器具のあるキッチン・駅から平坦な道で徒歩8分（前は約10分）・コンビニ2分・スーパー3分。「スマートロック」は公式が「テンキー錠」なので消しました。Wi-Fi の実測は書いていません。触れるのは最後の節の1回だけです ⑪節を組み替えました（運賃の節・車なしの節を足し、パスの節と弱点の節をなくしました）。h2 は7つです ⑫季節の表の「5月下旬〜9月」（japan-guide）を外し、「シーズンの前後は人が少なめだと思う」という私たちの見方にしました ⑬dek・In short は content.py の 2026-11-16 の短い版をもとに、数字と出典を直しました。関連記事に akiya-try-first を足しました",
   "【人に確かめてほしい点】①運賃・料金は2026年11月16日に伊豆急行・伊豆箱根鉄道の公式のページで見た値です（変わりやすい数字）。約6,660円は 4,280円＋2,380円の足し算です ②東京〜熱海の新幹線の運賃（特急料金を除く分）は公式で取れなかったので書いていません ③NODE Shimoda の「2階（英語では first floor と書いています）」「約40㎡」「徒歩8分」は公式サイトの記載です。experience.md の「徒歩10分ほど」と違うので、サイトの他のページ（NODE_FACTS など）もそろえるかを決めてください ④伊豆箱根鉄道の「昼間は1時間に3本ほど」は、時刻表（2025年3月15日改正）から数えた私たちのまとめです",
  ],
  "points": [
    "修善寺は直通で約2時間。または新幹線で三島まで約50分、そこからローカル線で35分です。",
    "2026年の海水浴の期間は7月18日から8月下旬までで、監視員がいたのもこの期間だけでした。",
    "車がなくても、東海バスの「下田2日券」（1,350円）で、下田の町・白浜・爪木崎を回れます。",
  ],
  "body": """
<h2>東京から伊豆半島へは、どう行くか</h2>
<p>いちばん簡単なのは、特急「踊り子」です。東京から[[l:ja-izu|伊豆半島]]の東海岸を下田まで、乗り換えなしで走ります。JR東日本の2026年11月の時刻表では、毎日5本が、9時から13時まで毎時ちょうどに東京を出ます。伊東まで1時間36〜45分、伊豆急下田まで2時間29〜44分です[[s:jre_tt_tokyo]]。内陸の修善寺へ行くなら、新幹線と短いローカル線のほうが合うことが多いです。</p>
<div class="tablewrap"><table>
<thead><tr><th>行き方</th><th>乗り換え</th><th>所要時間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>直通の「踊り子」</strong>で伊東・伊豆急下田へ</td><td>なし</td><td>伊東まで約1時間40分、下田まで2時間29分〜2時間44分[[s:jre_tt_tokyo]]</td><td>毎日5本で、東京を9:00・10:00・11:00・12:00・13:00に出ます。決まった日だけ走る列車もあります[[s:jre_tt_tokyo]]。11:00発は「サフィール踊り子」で、グリーン車とその上の席だけの列車です[[s:izukyu_express]]。</td></tr>
<tr><td><strong>新幹線で熱海</strong>へ出て、普通列車で下田へ</td><td>1回（熱海）</td><td>こだまで熱海まで43〜45分、熱海から下田まで1時間29分〜1時間49分[[s:jre_tt_tokyo]]</td><td>乗り継ぎがよければ、直通より速く着くこともあります。こだま6:30発、熱海7:23発の普通に乗り継ぐと、下田に8:52に着きます（2時間22分）[[s:jre_tt_tokyo]]。</td></tr>
<tr><td><strong>新幹線で三島</strong>へ出て、伊豆箱根鉄道で修善寺へ</td><td>1回（三島）</td><td>こだまで三島まで50〜53分[[s:jre_tt_tokyo]]、三島から修善寺まで約35分[[s:izuhakone_tt]]</td><td>修善寺行きの普通は、昼間はだいたい1時間に3本あるので[[s:izuhakone_tt]]、たいていの日はこちらが合うと私たちは見ています。</td></tr>
<tr><td><strong>直通の「踊り子」</strong>で修善寺へ</td><td>なし</td><td>2時間6分〜2時間8分[[s:jre_tt_tokyo]]</td><td>毎日2本で、東京を9:00と12:00に出ます。10:30発の3本目は、決まった日だけです[[s:jre_tt_tokyo]]。</td></tr>
</tbody></table></div>
<p class="fine">時刻は、JR東日本の東京駅の時刻表（2026年11月）と、伊豆箱根鉄道の駿豆線の時刻表によります。時刻表は季節で変わるので、乗る日の時刻を調べておくと安心です。</p>
<p>バスはどうか。半島のおもなバス会社の東海バスは、東京から下田や修善寺への高速バスを走らせていません。高速バス「三島エクスプレス」は新宿から三島までで、片道2,300円からです[[s:tokaibus_highway]]。三島からは伊豆箱根鉄道で修善寺へ行けます[[s:izuhakone_tt]]。下田へは、電車がいちばん簡単だと私たちは思います。</p>

<h2>東京から伊豆までの電車代は、いくらか</h2>
<p>直通の「踊り子」で下田まで、指定席で片道約6,660円です。運賃4,280円に、乗る前に買う特急料金2,380円を足した額で、2026年3月14日の改定後の伊豆急行の運賃表によります[[s:izukyu_fares,izukyu_express]]。</p>
<div class="tablewrap"><table>
<thead><tr><th>払うもの</th><th>片道・大人</th></tr></thead>
<tbody>
<tr><td>運賃（東京〜伊豆急下田）</td><td>4,280円（IC カードは4,276円）[[s:izukyu_fares]]</td></tr>
<tr><td>踊り子の特急料金（東京〜下田）</td><td>乗る前に買うと2,380円、車内で買うと2,640円[[s:izukyu_express]]</td></tr>
<tr><td>サフィール踊り子のグリーン（東京〜下田）</td><td>通常期6,260円。いちばん混む時期は最大400円高く、すいている時期は200円安くなります[[s:izukyu_express]]</td></tr>
<tr><td>新幹線の特急料金（東京〜熱海）</td><td>通常期で指定席2,290円、自由席1,760円。運賃は別です[[s:izukyu_express]]</td></tr>
<tr><td>普通列車（熱海〜下田）</td><td>2,210円[[s:izukyu_fares]]</td></tr>
<tr><td>伊豆急行線（伊東〜下田）</td><td>1,860円（IC カードは1,856円）[[s:izukyu_fares]]</td></tr>
<tr><td>伊豆箱根鉄道（三島〜修善寺）</td><td>550円[[s:izuhakone_fares]]</td></tr>
</tbody></table></div>
<p class="fine">2026年11月時点の値段です。伊豆箱根鉄道は2026年10月に運賃の値上げを申請していて、三島〜修善寺の線は2027年春に変わる予定です[[s:izuhakone_fare2026]]。</p>
<p>伊東より南の線は伊豆急行、修善寺への線は伊豆箱根鉄道のもので、JR ではありません。なので、レールパスで旅するなら、この2つの線でパスが何に使えるかを、改札で知るより前に調べておくのがおすすめです。</p>

<h2>伊豆半島は、東京から日帰りできるか</h2>
<p>北のほうはできますが、南はあまり向きません。直通の電車でも下田まで2時間半ほどかかるので[[s:jre_tt_tokyo]]、往復すると、浜で過ごす数時間のために5時間ほど電車に乗ることになります。熱海は新幹線で45分ほど、伊東は直通で1時間40分ほどなので、どちらも日帰りで楽しめると私たちは思います。南の海岸と内陸の温泉町は、泊まったほうがずっと楽しめるというのが私たちの考えです。</p>

<h2>伊豆のどの町が合うか</h2>
<p>決め手は、どこまで行きたいかと、どれくらいいられるかです。</p>
<div class="tablewrap"><table>
<thead><tr><th>町</th><th>東京から</th><th>どんな町か</th><th>日帰りか、泊まりか</th></tr></thead>
<tbody>
<tr><td><strong>熱海と伊東</strong></td><td>熱海まで新幹線で43〜45分、伊東まで直通で約1時間40分</td><td>東海岸の、東京にいちばん近い2つの町。海辺で数時間過ごしても東京で夕食に間に合うので、日帰りに向いているのはこの2つだと私たちは思います。</td><td>日帰りでも楽しめる</td></tr>
<tr><td><strong>修善寺</strong></td><td>三島まで50〜53分、そこから約35分。または直通で約2時間</td><td>伊豆でいちばん古いと言われる、内陸の温泉町です。「独鈷の湯」は見るだけで入れませんが、近くに「河原湯」と「杉の湯」の2つの足湯があります[[s:izu_tokko]]。慌ただしく立ち寄るより、1〜2泊して静かに過ごすのが合う町だと私たちは思います。</td><td>泊まるのがおすすめ</td></tr>
<tr><td><strong>下田</strong></td><td>直通で2時間29分〜2時間44分</td><td>半島の南端の港町で、2026年は正式な海水浴場が9つありました[[s:shimoda_beach2026_city]]。静岡県は、下田の魚市場を[[l:ja-kinmedai|金目鯛]]の水揚げ日本一と紹介しています[[s:pref]]。1週間過ごすのにいちばん合う町だと、私たちは思います。</td><td>泊まるのがおすすめ</td></tr>
</tbody></table></div>

<h2>南伊豆は、車なしで回れるか</h2>
<p>町と近くの浜なら、回れます。白浜海岸へは、伊豆急下田駅から板戸一色行きのバスで約15分です[[s:jnto]]。東海バスが、見たい所の多くを回れる2日間のフリーきっぷを出していて、買った日と次の日に使えます[[s:tokaibus_freepass]]。</p>
<div class="tablewrap"><table>
<thead><tr><th>きっぷ</th><th>大人の値段</th><th>行ける所</th></tr></thead>
<tbody>
<tr><td><strong>下田2日券</strong></td><td>1,350円</td><td>下田の町、龍宮窟、爪木崎、白浜[[s:tokaibus_freepass]]</td></tr>
<tr><td><strong>石廊崎・下田2日券</strong></td><td>2,850円</td><td>上の範囲に加えて、石廊崎、弓ヶ浜、下賀茂、河津、稲取[[s:tokaibus_freepass]]</td></tr>
</tbody></table></div>
<p>きっぷは、下田駅前の東海バスの案内所で買えます。毎日、8:45〜12:30と13:30〜17:00に開いています[[s:tokaibus_freepass]]。外れの浜へのバスは本数が多くないので、私たちなら出かける前に帰りの時刻を調べておきます。1日にいくつもの浜を回りたいなら、電動自転車かレンタカーがあると、ぐっと動きやすくなると思います。</p>

<h2>伊豆半島はいつ行くのがいいか</h2>
<p>泳ぐなら7月中旬から8月下旬。静かに過ごしたいなら、私たちはその前後の月を選びます。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>どんな感じか</th></tr></thead>
<tbody>
<tr><td>海水浴の期間（2026年は7月18日から、浜によって8月23〜31日まで）</td><td>2026年は、下田の9つの海水浴場がすべて7月18日に開き、多くは8時〜16時でした。白浜大浜と九十浜は8月31日まで、白浜中央は8月30日まで開いていましたが、ほかの6つは8月23日に閉じました[[s:shimoda_beach2026_city]]。期間外と時間外は、監視員がいません[[s:shimoda_ohama]]。</td></tr>
<tr><td>シーズンの前後</td><td>学校の休みと連休を外せば、人は少なめだろうと私たちは見ています。</td></tr>
<tr><td>それ以外</td><td>町はぐっと静かになります。温泉や長い散歩には、いちばん過ごしやすい時期だと私たちは思います。</td></tr>
</tbody></table></div>
<p class="fine">海水浴場の期間は、市が毎年決めます。8月の終わりに行くなら、どの浜がまだ開いているかを見ておくと安心です。</p>

<h2>伊豆では、なぜ1泊より1週間なのか</h2>
<p>1週間いると、旅がふだんの暮らしに変わり、南伊豆のゆっくりした時間の流れがしっくりきはじめます。ホテルの部屋は1〜2泊と決まった夕食の時間が前提です。キッチンと洗濯機のある部屋なら、午前は仕事、午後は浜か温泉、出かける気分でない夜は部屋で夕食、という過ごし方ができます。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて8分の「NODE Shimoda」のリビング。]]
<p>下田で試してみたいなら、旧町内にある私たちのアパートの一室「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、そんな1週間に向くように整えています。約40㎡の2階の部屋で、ワークデスク、洗濯機とガス乾燥機、調理器具のそろったキッチンがあります[[s:node_room]]。伊豆急下田駅から平坦な道を歩いて8分で、コンビニまで2分、スーパーまで3分です[[s:node_access]]。</p>
<p>伊豆で1週間過ごして、もっと長く住むことや、自分の家を持つことが気になり始めたら、[[l:ja-akiya-try-first|家を買う前に1か月その町に住む]]ことをすすめる理由も読んでみてください。</p>
""",
  "faq": [
    ("東京から下田まで、何時間かかりますか",
     "直通の特急「踊り子」で2時間29〜44分です。毎日5本が、東京を9時〜13時に出ます（JR東日本の時刻表、2026年11月）[[s:jre_tt_tokyo]]。"),
    ("東京から下田までの電車代はいくらですか",
     "踊り子の指定席で片道約6,660円です。運賃4,280円に、乗る前に買う特急料金2,380円を足した額です（伊豆急行の運賃表、2026年11月）[[s:izukyu_fares,izukyu_express]]。"),
    ("修善寺へは、どう行くのがいいですか",
     "新幹線で三島へ出て（こだまで50〜53分）[[s:jre_tt_tokyo]]、伊豆箱根鉄道で約35分、550円です[[s:izuhakone_tt,izuhakone_fares]]。直通の「踊り子」も毎日2本（9:00・12:00発）あり、約2時間です[[s:jre_tt_tokyo]]。"),
    ("東京から下田へのバスはありますか",
     "東海バスは走らせていません。東海バスの高速バスは三島行きで、新宿からの「三島エクスプレス」は2,300円からです[[s:tokaibus_highway]]。下田へは、電車がいちばん簡単だと私たちは思います。"),
    ("伊豆半島で車は必要ですか",
     "下田の町と近くの浜なら要りません。白浜へは駅からバスで約15分で[[s:jnto]]、東海バスの「下田2日券」は1,350円です[[s:tokaibus_freepass]]。車があると助かるのは、浜から浜へ動きたいときくらいだと私たちは思います。"),
  ],
 },
}
