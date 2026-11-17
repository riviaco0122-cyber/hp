# -*- coding: utf-8 -*-
"""izu-from-tokyo の書き直し（2026-11-16 手離れ、2026-11-17 品質保証部〔86点〕の指摘での2回目の直し）。content.py の ARTICLES の1件と同じ形。
黄色い枠はなし。確かめられないこと（JR東日本のワイド・パスなどほかのきっぷ、改定後の JR だけの運賃、最終バス、Wi-Fi の実測）は書かない。
運賃は伊豆急行と伊豆箱根鉄道の公式の運賃表、パスは JAPAN RAIL PASS の公式、バスは東海バスの公式、時刻は JR東日本の時刻表（2026年11月）と伊豆箱根鉄道の時刻表による。
jre_tt_tokyo・node_room・node_access は content.py の SOURCES にあるので、ここには書かない。"""

SOURCES_NEW = {
    "izukyu_fares": ("https://www.izukyu.co.jp/fares/index.php", "Izukyu", "伊豆急行（各駅運賃表）",
                     "Izu Kyuko Railway: Fares between stations (revised 14 March 2026)"),
    "izukyu_express": ("https://www.izukyu.co.jp/fares/express.php", "Izukyu (express charges)", "伊豆急行（特急・新幹線料金）",
                       "Izu Kyuko Railway: Limited express, Green Car and Shinkansen charges (for journeys from 1 February 2025, checked November 2026)"),
    "izuhakone_fares": ("https://www.izuhakone.co.jp/sunzudaiyu/zunzu_sub_nav/schedule/p010102.html", "Izuhakone Railway (fares)",
                        "伊豆箱根鉄道（運賃表）", "Izuhakone Railway: Fare table for the Sunzu Line (checked November 2026)"),
    "izuhakone_tt": ("https://www.izuhakone.co.jp/sunzudaiyu/sunzu-recommendation-article/p010438.html", "Izuhakone Railway (timetable)",
                     "伊豆箱根鉄道（駿豆線の時刻表）", "Izuhakone Railway: Sunzu Line timetable (revised 15 March 2025, checked November 2026)"),
    "izuhakone_fare2026": ("https://www.izuhakone.co.jp/izu-group/izu-news/p010993.html", "Izuhakone Railway (fare application)",
                           "伊豆箱根鉄道（運賃の改定申請）", "Izuhakone Railway: Application to revise fares (15 October 2026)"),
    "jrp_route": ("https://japanrailpass.net/en/about_jrp/route/", "JAPAN RAIL PASS (scope of validity)", "JAPAN RAIL PASS 公式（使える範囲）",
                  "JAPAN RAIL PASS official site: Scope of validity, including JR trains running through non-JR lines (checked November 2026)"),
    "jrp_conditions": ("https://japanrailpass.net/en/use/conditions-for-use/", "JAPAN RAIL PASS (conditions of use)", "JAPAN RAIL PASS 公式（利用条件）",
                       "JAPAN RAIL PASS official site: Conditions for use (current as of April 2026)"),
    "jrp_vehicle": ("https://japanrailpass.net/en/about_jrp/vehicle/", "JAPAN RAIL PASS (trains and cars)", "JAPAN RAIL PASS 公式（使える列車と車両）",
                    "JAPAN RAIL PASS official site: Trains and cars you can use (checked November 2026)"),
    "jrp_price": ("https://japanrailpass.net/en/purchase/price/", "JAPAN RAIL PASS (prices)", "JAPAN RAIL PASS 公式（値段）",
                  "JAPAN RAIL PASS official site: Prices (checked November 2026)"),
    "jrp_eligibility": ("https://japanrailpass.net/en/about_jrp/riyou/", "JAPAN RAIL PASS (who can use it)", "JAPAN RAIL PASS 公式（使える人）",
                        "JAPAN RAIL PASS official site: Eligibility (checked November 2026)"),
    "tokaibus_highway": ("https://www.tokaibus.jp/kousoku/", "Tokai Bus (highway buses)", "東海バス（高速バス）",
                         "Tokai Bus: Highway bus routes (checked November 2026)"),
    "tokaibus_freepass": ("https://www.tokaibus.jp/rosen/freekippu_shimoda_minamiizu.html", "Tokai Bus (bus passes)",
                          "東海バス（下田・南伊豆のフリーきっぷ）", "Tokai Bus: Shimoda and Minami-Izu two-day bus passes (checked November 2026)"),
    "izu_tokko": ("https://kanko.city.izu.shizuoka.jp/sightseeing/tokkonoyu/", "Izu City", "伊豆市", "Izu City tourism: Tokko-no-yu"),
    "shimoda_ohama": ("https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html", "Shimoda City", "下田市",
                      "Shimoda City: Shirahama Ohama Beach"),
    "shimoda_beach2026_city": ("https://city.shimoda.shizuoka.jp/file/広報しもだ令和8年8月号2-3頁.pdf", "Shimoda City newsletter, August 2026",
                               "広報しもだ 2026年8月号", "Shimoda City newsletter, August 2026: beaches open in Shimoda"),
}

ARTICLE = {
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-17",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, fares and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Fares and Where to Stay",
 "description": "Direct trains reach Shimoda from Tokyo in about 2½ hours, for about ¥6,660 with a reserved seat. The Japan Rail Pass covers JR to Ito; beyond, you pay Izukyu.",
 "dek": "Southern Izu is too far for a day trip but just right for a week. Direct trains reach Shimoda from Tokyo in 2 hours 29 to 44 minutes (November 2026).",
 "card": "Direct trains reach Shimoda from Tokyo in about 2½ hours, for about ¥6,660 one way with a reserved seat. The south of Izu is a long way for a day, but just right for a week.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—")],
 "intent": "Do（やり方を知りたい）",
 "points": [
   "Shimoda is about 2½ hours on the direct Odoriko, about ¥6,660 with a reserved seat (November 2026).",
   "Shuzenji is about two hours direct, or about 50 minutes by Shinkansen to Mishima plus a 35-minute local line.",
   "The Japan Rail Pass covers JR to Ito and Mishima; beyond them, you pay the Izukyu or Izuhakone fare.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The easiest way is the Odoriko limited express, which runs from Tokyo down the east coast of the [[l:izu|Izu Peninsula]] to Shimoda without a change. In JR East’s November 2026 timetable, five leave Tokyo every day, on the hour from 9:00 to 13:00. They take 1 hour 36 to 45 minutes to Ito and 2 hours 29 to 44 minutes to Izukyu-Shimoda [[s:jre_tt_tokyo]]. If you’re heading inland to Shuzenji, the Shinkansen and a short local line often suit you better.</p>
<div class="tablewrap"><table>
<thead><tr><th>Route</th><th>Changes</th><th>Time</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Direct Odoriko</strong> to Ito and Izukyu-Shimoda</td><td>None</td><td>About 1 h 40 min to Ito, 2 h 29 min to 2 h 44 min to Shimoda [[s:jre_tt_tokyo]]</td><td>Five a day, leaving Tokyo at 9:00, 10:00, 11:00, 12:00 and 13:00, with extra trains on set days [[s:jre_tt_tokyo]]. The 11:00 is the Saphir Odoriko, which only has Green Car and premium seats [[s:izukyu_express]].</td></tr>
<tr><td><strong>Shinkansen to Atami</strong>, then a local train to Shimoda</td><td>One, at Atami</td><td>43 to 45 min to Atami by Kodama, then 1 h 29 min to 1 h 49 min to Shimoda [[s:jre_tt_tokyo]]</td><td>With a good connection, it can beat the direct train. The 6:30 Kodama and the 7:23 local from Atami get you to Shimoda at 8:52, in 2 h 22 min [[s:jre_tt_tokyo]].</td></tr>
<tr><td><strong>Shinkansen to Mishima</strong>, then the Izuhakone Railway to Shuzenji</td><td>One, at Mishima</td><td>50 to 53 min to Mishima by Kodama [[s:jre_tt_tokyo]], then about 35 min to Shuzenji [[s:izuhakone_tt]]</td><td>Local trains to Shuzenji run about three times an hour for most of the day [[s:izuhakone_tt]], so the change at Mishima is easy to fit in.</td></tr>
<tr><td><strong>Direct Odoriko</strong> to Shuzenji</td><td>None</td><td>2 h 6 min to 2 h 8 min [[s:jre_tt_tokyo]]</td><td>Two a day, leaving Tokyo at 9:00 and 12:00. A third, at 10:30, runs only on set days [[s:jre_tt_tokyo]].</td></tr>
</tbody></table></div>
<p class="fine">Times are from JR East’s Tokyo Station timetables for November 2026 and the Izuhakone Railway’s Sunzu Line timetable. Timetables change with the seasons, so it’s a good idea to look up the times for your travel date.</p>
<p>What about the bus? Tokai Bus doesn’t run a highway bus from Tokyo to Shimoda or Shuzenji. Its Mishima Express goes from Shinjuku to Mishima, from ¥2,300 one way [[s:tokaibus_highway]], and from Mishima the Izuhakone Railway takes you on to Shuzenji [[s:izuhakone_tt]]. For Shimoda, the train is the simple answer.</p>

<h2>How much does the train from Tokyo to Izu cost?</h2>
<p>To Shimoda on the direct Odoriko, you’ll pay about ¥6,660 one way with a reserved seat. That’s the ¥4,280 fare, from Izukyu’s tables revised on 14 March 2026, plus a ¥2,380 seat charge bought before you board, from its charge table for journeys since 1 February 2025 [[s:izukyu_fares,izukyu_express]].</p>
<div class="tablewrap"><table>
<thead><tr><th>What you pay</th><th>One way, adult</th></tr></thead>
<tbody>
<tr><td>Fare, Tokyo to Izukyu-Shimoda</td><td>¥4,280 (¥4,276 with an IC card) [[s:izukyu_fares]]</td></tr>
<tr><td>Fare, Tokyo to Ito</td><td>¥2,420, plus a seat charge on the Odoriko [[s:izukyu_fares]]</td></tr>
<tr><td>Odoriko seat charge, Tokyo to Shimoda</td><td>¥2,380 bought before boarding, ¥2,640 on the train [[s:izukyu_express]]</td></tr>
<tr><td>Saphir Odoriko Green Car charge, Tokyo to Shimoda</td><td>¥6,260 in the normal season, up to ¥400 more at the busiest times and ¥200 less in quiet ones [[s:izukyu_express]]</td></tr>
<tr><td>Shinkansen charge, Tokyo to Atami</td><td>¥2,290 reserved, ¥1,760 unreserved, in the normal season, on top of the fare [[s:izukyu_express]]</td></tr>
<tr><td>Local train, Atami to Shimoda</td><td>¥2,210 [[s:izukyu_fares]]</td></tr>
<tr><td>Izu Kyuko line, Ito to Shimoda</td><td>¥1,860 (¥1,856 with an IC card) [[s:izukyu_fares]]</td></tr>
<tr><td>Izuhakone Railway, Mishima to Shuzenji</td><td>¥550 [[s:izuhakone_fares]]</td></tr>
</tbody></table></div>
<p class="fine">Fares and charges as of November 2026. The Izuhakone Railway applied in October 2026 to raise its fares, with the change on the Mishima–Shuzenji line planned for spring 2027 [[s:izuhakone_fare2026]].</p>

<h2>Can you use the Japan Rail Pass to get to Izu?</h2>
<p>Yes, as far as Ito and Mishima. The pass covers ordinary cars on JR lines, including Kodama Shinkansen trains and limited expresses like the Odoriko [[s:jrp_conditions,jrp_vehicle]]. South of Ito, the line belongs to Izukyu, and from Mishima to Shuzenji it’s the Izuhakone Railway. On those stretches you pay the fare and charges yourself, even if you stay on the same Odoriko [[s:jrp_route]].</p>
<p>So on an ordinary pass to Shimoda, you’ll pay Izukyu for the last leg: ¥1,860 from Ito, and Izukyu’s limited express charge is ¥800 for any distance on its line [[s:izukyu_fares,izukyu_express]]. To Shuzenji, it’s ¥550 from Mishima [[s:izuhakone_fares]]. If you sit in a Green Car on an ordinary pass, you pay the Green Car charge and the limited express charge too [[s:jrp_conditions]]. That matters for the Saphir Odoriko, which has no ordinary seats [[s:izukyu_express]].</p>
<p>As of November 2026, the official site lists a 7-day ordinary pass at ¥50,000 for adults bought online, or ¥53,000 through an overseas agent [[s:jrp_price]]. It’s only for visitors who enter Japan as a “Temporary Visitor” [[s:jrp_eligibility]]. With a Tokyo–Shimoda trip at about ¥6,660 each way, we think the pass only pays off when Izu is one stop on a longer journey around Japan.</p>

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is, but the south really isn’t. Even on the direct train, Shimoda is about two and a half hours from Tokyo [[s:jre_tt_tokyo]], so a return trip means about five hours on the train for a few hours on the beach. Atami is about 45 minutes away by Shinkansen and Ito about 1 hour 40 minutes on the direct train, so both work as day trips. The south coast and the inland hot-spring towns are far better if you stay.</p>

<h2>Which Izu town suits you?</h2>
<p>It mostly comes down to how far you want to go and how long you can stay.</p>
<div class="tablewrap"><table>
<thead><tr><th>Town</th><th>From Tokyo</th><th>What it’s like</th><th>Day trip or stay?</th></tr></thead>
<tbody>
<tr><td><strong>Atami and Ito</strong></td><td>Atami 43–45 min by Shinkansen; Ito about 1 h 40 min direct</td><td>The two towns nearest Tokyo, on the east coast.</td><td>A day trip works</td></tr>
<tr><td><strong>Shuzenji</strong></td><td>50–53 min to Mishima, then about 35 min; or about 2 h direct</td><td>An inland hot-spring town, said to be the oldest in Izu. You can look at the Tokko-no-yu spring but not bathe in it, and there are two foot baths nearby, Kawara-yu and Sugi-no-yu [[s:izu_tokko]]. It suits a quiet night or two more than a rushed visit.</td><td>Better to stay</td></tr>
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
<p>You buy them at Tokai Bus’s office by Shimoda Station, open every day from 8:45 to 12:30 and 13:30 to 17:00 [[s:tokaibus_freepass]]. Buses to the outer beaches don’t run often, so look up the return times before you head out. If you want to hop between several beaches in one day, an e-bike or a rental car makes life much easier.</p>

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>For swimming in Shimoda, the 2026 season ran from mid-July to late August. For a quieter stay, we’d pick the months either side.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Swimming season in Shimoda (in 2026, from 18 July to between 23 and 31 August, depending on the beach)</td><td>All nine of Shimoda’s official beaches opened on 18 July 2026, mostly from 8:00 to 16:00. Shirahama Ohama and Kujukihama stayed open until 31 August and Shirahama Chuo until 30 August, but the other six closed on 23 August [[s:shimoda_beach2026_city]]. Outside the season and those hours, there are no lifeguards [[s:shimoda_ohama]].</td></tr>
<tr><td>The rest of the year</td><td>The towns get much quieter, and it’s the easiest time for hot springs and long walks.</td></tr>
</tbody></table></div>
<p class="fine">The city sets the beach dates each year, so if you’re planning a late-August trip, it’s a good idea to see which beaches will still be open.</p>

<h2>Why stay a week in Izu rather than a night?</h2>
<p>A week turns a trip into ordinary life, and that’s when the slow pace of the south starts to make sense. A hotel room is built around one or two nights and a set dinner time. A place with a kitchen and a washing machine lets you work in the morning, head to the beach or a hot spring in the afternoon, and eat in when you don’t feel like going out.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, eight minutes on foot from Izukyu-Shimoda Station.]]
<p>If you’d like to try that in Shimoda, our apartment in the old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is set up for that kind of week. It’s about 40 m² on the first floor, with a work desk, a washing machine and gas dryer, and a kitchen with cookware [[s:node_room]]. It’s eight minutes’ walk on the flat from Izukyu-Shimoda Station, with a convenience store two minutes away and a supermarket three [[s:node_access]]. Most of our guests come from abroad, some to work remotely and some to surf, and in summer more of them stay longer.</p>
<p>If a week in Izu gets you thinking about a longer stay, or even a house of your own, here’s why we suggest [[l:akiya-try-first|living in a town for a month before buying a house]].</p>
""",
 "faq": [
   ("How long does it take to get from Tokyo to Shimoda?",
    "2 hours 29 to 44 minutes on the direct Odoriko limited express. Five run a day, leaving Tokyo between 9:00 and 13:00 (JR East timetable, November 2026) [[s:jre_tt_tokyo]]."),
   ("How much is the train from Tokyo to Shimoda?",
    "About ¥6,660 one way on the Odoriko with a reserved seat: the ¥4,280 fare (revised 14 March 2026) plus a ¥2,380 seat charge bought before boarding (as of November 2026) [[s:izukyu_fares,izukyu_express]]."),
   ("Can I use the Japan Rail Pass to get to Izu?",
    "Yes, on JR as far as Ito and Mishima. From Ito to Izukyu-Shimoda and from Mishima to Shuzenji, you pay the fare and charges separately, even on the Odoriko [[s:jrp_route]]. A 7-day ordinary pass was ¥50,000 online in November 2026 [[s:jrp_price]]."),
   ("What’s the best way to get to Shuzenji?",
    "You can take the Shinkansen to Mishima, 50 to 53 minutes on a Kodama [[s:jre_tt_tokyo]], and then the Izuhakone Railway, about 35 minutes for ¥550 [[s:izuhakone_tt,izuhakone_fares]]. Two direct Odoriko trains also run every day, at 9:00 and 12:00, taking about two hours [[s:jre_tt_tokyo]]."),
   ("Is there a bus from Tokyo to Shimoda?",
    "Tokai Bus doesn’t run one. Its highway buses go to Mishima, including the Mishima Express from Shinjuku from ¥2,300 [[s:tokaibus_highway]]. For Shimoda, the train is the simple answer."),
   ("Do I need a car on the Izu Peninsula?",
    "Not for Shimoda town and the nearby beaches. Shirahama is about 15 minutes by bus from the station [[s:jnto]], and Tokai Bus’s two-day Shimoda pass costs ¥1,350 [[s:tokaibus_freepass]]. A car only really helps when you want to hop between beaches."),
 ],
 "sources": ["jre_tt_tokyo", "izukyu_fares", "izukyu_express", "izuhakone_tt", "izuhakone_fares", "izuhakone_fare2026",
             "jrp_route", "jrp_conditions", "jrp_vehicle", "jrp_price", "jrp_eligibility",
             "tokaibus_highway", "tokaibus_freepass", "jnto", "izu_tokko", "shimoda_beach2026_city", "shimoda_ohama", "pref",
             "node_room", "node_access"],
 "related": ["kinmedai", "izu", "akiya-try-first"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・運賃と、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りには遠く、1週間ならちょうどいい距離です。下田へは、東京から直通の特急で2時間29〜44分です（2026年11月）。",
  "review": [
   "【2026-11-17 品質保証部（86点）の指摘での2回目の直し】変えた点: ①ジャパン・レール・パスの節を新しく作りました（JAPAN RAIL PASS の公式で確認）。JR の普通車（こだまや踊り子などの特急を含む）にパスで乗れる＝伊東・三島まで。伊東〜伊豆急下田（伊豆急行）と三島〜修善寺（伊豆箱根鉄道）は、同じ踊り子に乗ったままでも運賃・料金を別に払う。下田まで行くなら伊東〜下田の1,860円と、伊豆急行線内の特急料金800円（区間にかかわらず同じ）。修善寺へは三島から550円。普通車用のパスでグリーン車に乗るとグリーン料金と特急料金が要り、サフィール踊り子は普通車がない。値段は2026年11月に公式サイトで見た値（7日間の普通車、オンラインで大人50,000円、海外の代理店で53,000円）。使えるのは「短期滞在（Temporary Visitor）」で入国した人だけ。「東京〜下田が片道約6,660円なので、伊豆だけならパスは元が取れず、日本を長く回る旅の途中なら」という私たちの見方を1文。FAQ にも1問足しました。ワイド・パスなどほかのきっぷは書いていません ②運賃の表に、伊豆急行の同じ運賃表にある東京〜伊東 2,420円を足しました（踊り子の特急料金は別）。熱海・三島までの JR の運賃は公式の表で取れないので書いていません ③冒頭で値段に答えるよう、In short を「下田は直通の踊り子で約2時間半、指定席で約6,660円（2026年11月）」「修善寺」「ジャパン・レール・パスは伊東・三島まで、その先は伊豆急行・伊豆箱根鉄道の運賃」の3つにしました（海水浴と路線バスの項目は本文に） ④正確性: 運賃（2026年3月14日改定）と特急料金（2025年2月1日以降の乗車分の料金表）の時点を分けて書きました。「半島のおもなバス会社」を消し「東海バスは東京から下田・修善寺への高速バスを走らせていない」に。海水浴の期間は「下田で、2026年は7月中旬〜8月下旬」と場所と年を付けました（季節の表の見出しも） ⑤独自性: 町の表の熱海・伊東の行を短くしました。experience.md の確認済みの節（ゲストの層: 訪日客が中心、ワーケーションやサーフィンの人もいる、夏は長期滞在が多め）を NODE Shimoda の段落に1文入れました ⑥トーン: description の後半を目次から答え（パスは伊東まで、その先は伊豆急行に払う）に。「私たちは思う／見ている」を減らし（見解の形は、パスの元が取れるか・下田が1週間に合う・季節の選び方など4か所に）、「〜だろうと見ています」の推測文（三島で乗り換える人が多いだろう・シーズン前後は人が少ないだろう）をなくしました。季節の表の「シーズンの前後」の行は外しました ⑦出典: jre_tt_tokyo と node_access は content.py にあるので SOURCES_NEW から外しました。JAPAN RAIL PASS の公式（jrp_route・jrp_conditions・jrp_vehicle・jrp_price・jrp_eligibility）を足しました。updated を 2026-11-17 に",
   "【2026-11-16 手離れでの書き直し（事実・出典の変更あり）】変えた点: 黄色い枠を4つともなくしました。運賃を伊豆急行・伊豆箱根鉄道の公式の運賃表に（japan-guide の改定前の目安をやめた）。三島〜修善寺は公式の時刻表で約35分、値上げは2027年春の予定（公式の申請のお知らせ）。直行バスは「東海バスにはない」まで。車なしで回る節（白浜までバスで約15分、下田2日券1,350円・石廊崎・下田2日券2,850円）を新しく作りました。修善寺の足湯（河原湯・杉の湯）は伊豆市の公式で確認。修善寺の所要時間を「直通で約2時間、または新幹線で三島まで約50分＋35分」に直しました。東京〜下田は JR東日本の時刻表（2026年11月）の2時間29〜44分にそろえました。NODE Shimoda は公式サイトどおり「アパートの一室」・約40㎡・2階・徒歩8分に。浜からの最終バスと Wi-Fi の実測は書いていません",
   "【人に確かめてほしい点】①変わりやすい数字: 運賃・特急料金（伊豆急行・伊豆箱根鉄道、2026-11-16 確認）、ジャパン・レール・パスの値段と利用条件（公式、2026-11-17 確認。利用条件は2026年4月時点の記載）、時刻（JR東日本 2026年11月・伊豆箱根鉄道 2025年3月改正）、東海バスのきっぷと三島エクスプレスの値段（2026-11-16 確認）、2026年の下田の海水浴場の期間",
  ],
  "points": [
    "下田へは直通の踊り子で約2時間半、指定席で約6,660円です（2026年11月）。",
    "修善寺は直通で約2時間。または新幹線で三島まで約50分、そこからローカル線で35分です。",
    "ジャパン・レール・パスは伊東と三島までの JR で使えます。その先は、伊豆急行か伊豆箱根鉄道の運賃を払います。",
  ],
  "body": """
<h2>東京から伊豆半島へは、どう行くか</h2>
<p>いちばん簡単なのは、特急「踊り子」です。東京から[[l:ja-izu|伊豆半島]]の東海岸を下田まで、乗り換えなしで走ります。JR東日本の2026年11月の時刻表では、毎日5本が、9時から13時まで毎時ちょうどに東京を出ます。伊東まで1時間36〜45分、伊豆急下田まで2時間29〜44分です[[s:jre_tt_tokyo]]。内陸の修善寺へ行くなら、新幹線と短いローカル線のほうが合うことが多いです。</p>
<div class="tablewrap"><table>
<thead><tr><th>行き方</th><th>乗り換え</th><th>所要時間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>直通の「踊り子」</strong>で伊東・伊豆急下田へ</td><td>なし</td><td>伊東まで約1時間40分、下田まで2時間29分〜2時間44分[[s:jre_tt_tokyo]]</td><td>毎日5本で、東京を9:00・10:00・11:00・12:00・13:00に出ます。決まった日だけ走る列車もあります[[s:jre_tt_tokyo]]。11:00発は「サフィール踊り子」で、グリーン車とその上の席だけの列車です[[s:izukyu_express]]。</td></tr>
<tr><td><strong>新幹線で熱海</strong>へ出て、普通列車で下田へ</td><td>1回（熱海）</td><td>こだまで熱海まで43〜45分、熱海から下田まで1時間29分〜1時間49分[[s:jre_tt_tokyo]]</td><td>乗り継ぎがよければ、直通より速く着くこともあります。こだま6:30発、熱海7:23発の普通に乗り継ぐと、下田に8:52に着きます（2時間22分）[[s:jre_tt_tokyo]]。</td></tr>
<tr><td><strong>新幹線で三島</strong>へ出て、伊豆箱根鉄道で修善寺へ</td><td>1回（三島）</td><td>こだまで三島まで50〜53分[[s:jre_tt_tokyo]]、三島から修善寺まで約35分[[s:izuhakone_tt]]</td><td>修善寺行きの普通は、昼間はだいたい1時間に3本あるので[[s:izuhakone_tt]]、三島での乗り換えは組みやすいです。</td></tr>
<tr><td><strong>直通の「踊り子」</strong>で修善寺へ</td><td>なし</td><td>2時間6分〜2時間8分[[s:jre_tt_tokyo]]</td><td>毎日2本で、東京を9:00と12:00に出ます。10:30発の3本目は、決まった日だけです[[s:jre_tt_tokyo]]。</td></tr>
</tbody></table></div>
<p class="fine">時刻は、JR東日本の東京駅の時刻表（2026年11月）と、伊豆箱根鉄道の駿豆線の時刻表によります。時刻表は季節で変わるので、乗る日の時刻を調べておくと安心です。</p>
<p>バスはどうか。東海バスは、東京から下田や修善寺への高速バスを走らせていません。高速バス「三島エクスプレス」は新宿から三島までで、片道2,300円からです[[s:tokaibus_highway]]。三島からは伊豆箱根鉄道で修善寺へ行けます[[s:izuhakone_tt]]。下田へは、電車がいちばん簡単です。</p>

<h2>東京から伊豆までの電車代は、いくらか</h2>
<p>直通の「踊り子」で下田まで、指定席で片道約6,660円です。2026年3月14日に改定された伊豆急行の運賃表の運賃4,280円に、2025年2月1日以降の乗車分の料金表の特急料金2,380円（乗る前に買う場合）を足した額です[[s:izukyu_fares,izukyu_express]]。</p>
<div class="tablewrap"><table>
<thead><tr><th>払うもの</th><th>片道・大人</th></tr></thead>
<tbody>
<tr><td>運賃（東京〜伊豆急下田）</td><td>4,280円（IC カードは4,276円）[[s:izukyu_fares]]</td></tr>
<tr><td>運賃（東京〜伊東）</td><td>2,420円。踊り子に乗るなら特急料金が別に要ります[[s:izukyu_fares]]</td></tr>
<tr><td>踊り子の特急料金（東京〜下田）</td><td>乗る前に買うと2,380円、車内で買うと2,640円[[s:izukyu_express]]</td></tr>
<tr><td>サフィール踊り子のグリーン（東京〜下田）</td><td>通常期6,260円。いちばん混む時期は最大400円高く、すいている時期は200円安くなります[[s:izukyu_express]]</td></tr>
<tr><td>新幹線の特急料金（東京〜熱海）</td><td>通常期で指定席2,290円、自由席1,760円。運賃は別です[[s:izukyu_express]]</td></tr>
<tr><td>普通列車（熱海〜下田）</td><td>2,210円[[s:izukyu_fares]]</td></tr>
<tr><td>伊豆急行線（伊東〜下田）</td><td>1,860円（IC カードは1,856円）[[s:izukyu_fares]]</td></tr>
<tr><td>伊豆箱根鉄道（三島〜修善寺）</td><td>550円[[s:izuhakone_fares]]</td></tr>
</tbody></table></div>
<p class="fine">2026年11月時点の運賃・料金です。伊豆箱根鉄道は2026年10月に運賃の値上げを申請していて、三島〜修善寺の線は2027年春に変わる予定です[[s:izuhakone_fare2026]]。</p>

<h2>伊豆へ行くのに、ジャパン・レール・パスは使えるか</h2>
<p>使えます。ただし伊東と三島までです。パスでは、こだまの新幹線や踊り子のような特急を含め、JR の線の普通車に乗れます[[s:jrp_conditions,jrp_vehicle]]。伊東より南は伊豆急行の線、三島から修善寺までは伊豆箱根鉄道の線で、この区間は、同じ踊り子に乗ったままでも、運賃と料金を自分で払います[[s:jrp_route]]。</p>
<p>なので、普通車用のパスで下田へ行くなら、最後の区間は伊豆急行に払います。伊東から1,860円で、伊豆急行線内の特急料金は、区間にかかわらず800円です[[s:izukyu_fares,izukyu_express]]。修善寺へは、三島から550円です[[s:izuhakone_fares]]。普通車用のパスでグリーン車に座ると、グリーン料金と特急料金も要ります[[s:jrp_conditions]]。普通車のないサフィール踊り子では、ここが効いてきます[[s:izukyu_express]]。</p>
<p>2026年11月時点で、公式サイトの値段は、7日間の普通車用がオンラインで大人50,000円、海外の代理店で53,000円です[[s:jrp_price]]。使えるのは、「短期滞在（Temporary Visitor）」で入国した人だけです[[s:jrp_eligibility]]。東京〜下田が片道約6,660円なので、パスの元が取れるのは、伊豆が日本を長く回る旅の途中のひとつのときだけだと私たちは思います。</p>

<h2>伊豆半島は、東京から日帰りできるか</h2>
<p>北のほうはできますが、南はあまり向きません。直通の電車でも下田まで2時間半ほどかかるので[[s:jre_tt_tokyo]]、往復すると、浜で過ごす数時間のために5時間ほど電車に乗ることになります。熱海は新幹線で45分ほど、伊東は直通で1時間40分ほどなので、どちらも日帰りで楽しめます。南の海岸と内陸の温泉町は、泊まったほうがずっと楽しめます。</p>

<h2>伊豆のどの町が合うか</h2>
<p>決め手は、どこまで行きたいかと、どれくらいいられるかです。</p>
<div class="tablewrap"><table>
<thead><tr><th>町</th><th>東京から</th><th>どんな町か</th><th>日帰りか、泊まりか</th></tr></thead>
<tbody>
<tr><td><strong>熱海と伊東</strong></td><td>熱海まで新幹線で43〜45分、伊東まで直通で約1時間40分</td><td>東海岸の、東京にいちばん近い2つの町です。</td><td>日帰りでも楽しめる</td></tr>
<tr><td><strong>修善寺</strong></td><td>三島まで50〜53分、そこから約35分。または直通で約2時間</td><td>伊豆でいちばん古いと言われる、内陸の温泉町です。「独鈷の湯」は見るだけで入れませんが、近くに「河原湯」と「杉の湯」の2つの足湯があります[[s:izu_tokko]]。慌ただしく立ち寄るより、1〜2泊して静かに過ごすのが合う町です。</td><td>泊まるのがおすすめ</td></tr>
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
<p>きっぷは、下田駅前の東海バスの案内所で買えます。毎日、8:45〜12:30と13:30〜17:00に開いています[[s:tokaibus_freepass]]。外れの浜へのバスは本数が多くないので、出かける前に帰りの時刻を調べておきましょう。1日にいくつもの浜を回りたいなら、電動自転車かレンタカーがあると、ぐっと動きやすくなります。</p>

<h2>伊豆半島はいつ行くのがいいか</h2>
<p>下田で泳ぐなら、2026年の期間は7月中旬から8月下旬でした。静かに過ごしたいなら、私たちはその前後の月を選びます。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>どんな感じか</th></tr></thead>
<tbody>
<tr><td>下田の海水浴の期間（2026年は7月18日から、浜によって8月23〜31日まで）</td><td>2026年は、下田の9つの海水浴場がすべて7月18日に開き、多くは8時〜16時でした。白浜大浜と九十浜は8月31日まで、白浜中央は8月30日まで開いていましたが、ほかの6つは8月23日に閉じました[[s:shimoda_beach2026_city]]。期間外と時間外は、監視員がいません[[s:shimoda_ohama]]。</td></tr>
<tr><td>それ以外</td><td>町はぐっと静かになり、温泉や長い散歩にはいちばん過ごしやすい時期です。</td></tr>
</tbody></table></div>
<p class="fine">海水浴場の期間は、市が毎年決めます。8月の終わりに行くなら、どの浜がまだ開いているかを見ておくと安心です。</p>

<h2>伊豆では、なぜ1泊より1週間なのか</h2>
<p>1週間いると、旅がふだんの暮らしに変わり、南伊豆のゆっくりした時間の流れがしっくりきはじめます。ホテルの部屋は1〜2泊と決まった夕食の時間が前提です。キッチンと洗濯機のある部屋なら、午前は仕事、午後は浜か温泉、出かける気分でない夜は部屋で夕食、という過ごし方ができます。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて8分の「NODE Shimoda」のリビング。]]
<p>下田で試してみたいなら、旧町内にある私たちのアパートの一室「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、そんな1週間に向くように整えています。約40㎡の2階の部屋で、ワークデスク、洗濯機とガス乾燥機、調理器具のそろったキッチンがあります[[s:node_room]]。伊豆急下田駅から平坦な道を歩いて8分で、コンビニまで2分、スーパーまで3分です[[s:node_access]]。泊まる方の多くは海外からで、リモートで仕事をする人もサーフィンに来る人もいて、夏は長く泊まる人が増えます。</p>
<p>伊豆で1週間過ごして、もっと長く住むことや、自分の家を持つことが気になり始めたら、[[l:ja-akiya-try-first|家を買う前に1か月その町に住む]]ことをすすめる理由も読んでみてください。</p>
""",
  "faq": [
    ("東京から下田まで、何時間かかりますか",
     "直通の特急「踊り子」で2時間29〜44分です。毎日5本が、東京を9時〜13時に出ます（JR東日本の時刻表、2026年11月）[[s:jre_tt_tokyo]]。"),
    ("東京から下田までの電車代はいくらですか",
     "踊り子の指定席で片道約6,660円です。運賃4,280円（2026年3月14日改定）に、乗る前に買う特急料金2,380円を足した額です（2026年11月時点）[[s:izukyu_fares,izukyu_express]]。"),
    ("伊豆へ行くのに、ジャパン・レール・パスは使えますか",
     "伊東と三島までの JR で使えます。伊東〜伊豆急下田と三島〜修善寺は、踊り子に乗ったままでも運賃と料金を別に払います[[s:jrp_route]]。7日間の普通車用は、2026年11月にオンラインで50,000円でした[[s:jrp_price]]。"),
    ("修善寺へは、どう行くのがいいですか",
     "新幹線で三島へ出て（こだまで50〜53分）[[s:jre_tt_tokyo]]、伊豆箱根鉄道で約35分、550円です[[s:izuhakone_tt,izuhakone_fares]]。直通の「踊り子」も毎日2本（9:00・12:00発）あり、約2時間です[[s:jre_tt_tokyo]]。"),
    ("東京から下田へのバスはありますか",
     "東海バスは走らせていません。東海バスの高速バスは三島行きで、新宿からの「三島エクスプレス」は2,300円からです[[s:tokaibus_highway]]。下田へは、電車がいちばん簡単です。"),
    ("伊豆半島で車は必要ですか",
     "下田の町と近くの浜なら要りません。白浜へは駅からバスで約15分で[[s:jnto]]、東海バスの「下田2日券」は1,350円です[[s:tokaibus_freepass]]。車があると助かるのは、浜から浜へ動きたいときくらいです。"),
  ],
 },
}
