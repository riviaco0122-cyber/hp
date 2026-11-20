# -*- coding: utf-8 -*-
"""shimoda-guide の新規の下書き（2026-11-20 執筆部）。content.py の ARTICLES の1件と同じ形。
構成案とリサーチメモ: tools/okaeri/briefs/shimoda-guide.md。黄色い枠はなし。
書かないと決めたこと（リサーチメモの12件）: ロープウェイの運賃・所要・運行時間、月別の平年値、津波の到達時間、
入田浜の水質の「認証」、サーフィン区域の線引き、東海バスの系統名・時刻、道の駅全体の営業時間、スーパーの店名、
英語のごみ分別表、共同浴場。水族館の営業時間・料金も書かない。
共食いの線引き: 行き方・運賃・フリーきっぷ・2026年の海水浴の期間は izu-from-tokyo、店で食べる金目鯛は kinmedai、
部屋の借り方は monthly-rental へリンクで送る。
既存の出典（content.py の SOURCES）: shimoda_ohama・shimoda_gomi・pref_izu_gyokyo_shop・shimoda_kanko_gift・
shimoda_kanko_event・node_room・node_access。ここには新しいものだけを書く。
見出し写真は編集長が Unsplash で用意する（"TODO-PHOTO"）。"""

SOURCES_NEW = {
    "shimoda_population": ("https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/155431.html", "Shimoda City (population)",
                           "下田市（男女別人口・世帯数）", "Shimoda City: Population and households from the resident register (1 November 2026)"),
    "shimoda_profile": ("https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/110963.html", "Shimoda City (about the city)",
                        "下田市（下田市の紹介）", "Shimoda City: About Shimoda"),
    "shimoda_hist_perry": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110778.html", "Shimoda City (Perry and the opening of Japan)",
                           "下田市（ペリー黒船艦隊来航と日本開国）", "Shimoda City: Perry’s Black Ships and the opening of Japan"),
    "shimoda_hist_harris": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110776.html", "Shimoda City (Townsend Harris)",
                            "下田市（日本における初代米国総領事ハリス）", "Shimoda City: Townsend Harris, the first US Consul General in Japan"),
    "shimoda_hist_ansei": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110777.html", "Shimoda City (the Ansei tsunami)",
                           "下田市（ディアナ号来航と安政の大津波）", "Shimoda City: Putyatin, the Diana and the Ansei tsunami"),
    "shimoda_perryroad": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110766.html", "Shimoda City (Perry Road)",
                          "下田市（ペリーロード）", "Shimoda City: Perry Road"),
    "shimoda_ryosenji": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110768.html", "Shimoda City (Ryosenji)",
                         "下田市（了仙寺）", "Shimoda City: Ryosenji temple"),
    "shimoda_gyokusenji": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110756.html", "Shimoda City (Gyokusenji)",
                           "下田市（玉泉寺）", "Shimoda City: Gyokusenji temple"),
    "shimoda_nesugata": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110764.html", "Shimoda City (Mt Nesugata)",
                         "下田市（寝姿山）", "Shimoda City: Mt Nesugata"),
    "shimoda_park": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110769.html", "Shimoda City (Shimoda Park)",
                     "下田市（下田公園）", "Shimoda City: Shimoda Park"),
    "shimoda_michinoeki": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110763.html", "Shimoda City (Michi-no-Eki)",
                           "下田市（道の駅開国下田みなと）", "Shimoda City: Michi-no-Eki Kaikoku Shimoda Minato"),
    "shimoda_beaches_city": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/155720.html", "Shimoda City (beaches)",
                             "下田市（海水浴場）", "Shimoda City: Swimming beaches (2026 season, checked November 2026)"),
    "shimoda_kanko_umi": ("https://www.shimoda-city.info/umi", "Shimoda Tourism Association (beaches)", "下田市観光協会（下田の海）",
                          "Shimoda Tourism Association: Shimoda’s nine beaches and beach rules (checked November 2026)"),
    "shimoda_kanko_beach_shirahamachuo": ("https://www.shimoda-city.info/shirahama-chuo", "Shimoda Tourism Association (Shirahama Chuo)",
                                          "下田市観光協会（白浜中央海水浴場）", "Shimoda Tourism Association: Shirahama Chuo (Nagatahama) Beach (2026)"),
    "shimoda_kanko_beach_shirahama": ("https://www.shimoda-city.info/shirahama-ohama", "Shimoda Tourism Association (Shirahama Ohama)",
                                      "下田市観光協会（白浜大浜海水浴場）", "Shimoda Tourism Association: Shirahama Ohama Beach (2026)"),
    "shimoda_kanko_beach_sotoura": ("https://www.shimoda-city.info/sotoura", "Shimoda Tourism Association (Sotoura)",
                                    "下田市観光協会（外浦海水浴場）", "Shimoda Tourism Association: Sotoura Beach (2026)"),
    "shimoda_kanko_beach_kujuppama": ("https://www.shimoda-city.info/kujupama", "Shimoda Tourism Association (Kujuppama)",
                                      "下田市観光協会（九十浜海水浴場）", "Shimoda Tourism Association: Kujuppama Beach (2026)"),
    "shimoda_kanko_beach_nabeta": ("https://www.shimoda-city.info/nabeta", "Shimoda Tourism Association (Nabetahama)",
                                   "下田市観光協会（鍋田浜海水浴場）", "Shimoda Tourism Association: Nabetahama Beach (2026)"),
    "shimoda_kanko_beach_tatado": ("https://www.shimoda-city.info/tatado", "Shimoda Tourism Association (Tatadohama)",
                                   "下田市観光協会（多々戸浜海水浴場）", "Shimoda Tourism Association: Tatadohama Beach (2026)"),
    "shimoda_kanko_beach_irita": ("https://www.shimoda-city.info/irita", "Shimoda Tourism Association (Iritahama)",
                                  "下田市観光協会（入田浜海水浴場）", "Shimoda Tourism Association: Iritahama Beach (2026)"),
    "shimoda_kanko_beach_kisami": ("https://www.shimoda-city.info/kisami", "Shimoda Tourism Association (Kisami Ohama)",
                                   "下田市観光協会（吉佐美大浜海水浴場）", "Shimoda Tourism Association: Kisami Ohama Beach (2026)"),
    "shimoda_kanko_beach_toji": ("https://www.shimoda-city.info/toji", "Shimoda Tourism Association (Toji)",
                                 "下田市観光協会（田牛海水浴場）", "Shimoda Tourism Association: Toji Beach (2026)"),
    "pref_beach_water_2026": ("https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/050/681/r8kaisuiyokujoitiran.pdf",
                              "Shizuoka Prefecture, 2026", "静岡県（令和8年度 海水浴場水質調査結果一覧）",
                              "Shizuoka Prefecture: Beach water quality survey results, FY2026"),
    "shimoda_kanko_suisen": ("https://www.shimoda-city.info/suisen", "Shimoda Tourism Association (daffodil festival)", "下田市観光協会（水仙まつり）",
                             "Shimoda Tourism Association: Daffodil festival at Tsumekizaki (2026–27 season)"),
    "shimoda_kanko_kurofune": ("https://www.shimoda-city.info/kurofune", "Shimoda Tourism Association (Black Ship Festival)", "下田市観光協会（黒船祭）",
                               "Shimoda Tourism Association: Black Ship Festival (2026 edition)"),
    "shimoda_kanko_ajisai": ("https://www.shimoda-city.info/ajisai", "Shimoda Tourism Association (hydrangea festival)", "下田市観光協会（あじさい祭）",
                             "Shimoda Tourism Association: Hydrangea festival in Shimoda Park (2026)"),
    "shimoda_kanko_onsen": ("https://www.shimoda-city.info/onsen", "Shimoda Tourism Association (hot springs)", "下田市観光協会（下田の温泉）",
                            "Shimoda Tourism Association: Day hot springs and footbaths (checked November 2026)"),
    "shimoda_kanko_bicycle": ("https://www.shimoda-city.info/access-bicycle", "Shimoda Tourism Association (bike rental)", "下田市観光協会（レンタサイクル）",
                              "Shimoda Tourism Association: Bike rental (checked November 2026)"),
    "shimoda_kanko_promenade": ("https://www.shimoda-city.info/promenade", "Shimoda Tourism Association (walks)", "下田市観光協会（遊歩道）",
                                "Shimoda Tourism Association: Walking paths (checked November 2026)"),
    "shimoda_kanko_about": ("https://www.shimoda-city.info/about", "Shimoda Tourism Association (information centres)", "下田市観光協会（観光協会について）",
                            "Shimoda Tourism Association: Information centres and opening hours (checked November 2026)"),
    "shimoda_tsunami_map": ("https://www.city.shimoda.shizuoka.jp/category/010300tiiki_bousai/120138.html", "Shimoda City (tsunami hazard maps)",
                            "下田市（津波ハザードマップ・津波避難計画地図）", "Shimoda City: Tsunami hazard maps and evacuation maps (in Japanese)"),
    "shimoda_tsunami_bldg": ("https://www.city.shimoda.shizuoka.jp/category/010400hinan_basyo/111108.html", "Shimoda City (tsunami evacuation buildings)",
                             "下田市（津波避難ビル）", "Shimoda City: Tsunami evacuation buildings"),
    "shimoda_elevation_map": ("https://www.city.shimoda.shizuoka.jp/category/010500bousai_tishiki/159625.html", "Shimoda City (height above sea level map)",
                              "下田市（ここは海抜何メートル）", "Shimoda City: Online map of height above sea level"),
    "shimoda_news_2013_08": ("https://city.shimoda.shizuoka.jp/file/平成25年8月号2頁3頁.pdf", "Shimoda City newsletter, August 2013",
                             "広報しもだ 2013年8月号", "Shimoda City newsletter, August 2013: Shizuoka’s 4th earthquake damage estimate for Shimoda"),
    "jma_tsunami_warnings": ("https://www.jma.go.jp/jma/kishou/know/jishin/joho/tsunamiinfo.html", "Japan Meteorological Agency",
                             "気象庁（津波警報・注意報、津波情報、津波予報について）",
                             "Japan Meteorological Agency: Tsunami warnings, advisories and information (in Japanese, checked November 2026)"),
    "jta_safety_tips": ("https://www.jnto.go.jp/safety-tips/eng/app.html", "Japan Tourism Agency (Safety tips)", "観光庁（Safety tips アプリ）",
                        "Japan Tourism Agency: The app “Safety tips” (checked November 2026)"),
}

ARTICLE = {
 "id": "shimoda-guide", "slug": "shimoda-guide", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("stony-shore-waves", "Waves breaking on a stony beach under a clear blue sky, with one person walking at the water’s edge", ""),
 "published": "2026-11-20", "updated": "2026-11-20",
 "kicker": "Izu Peninsula",
 "h1": "Shimoda, Japan: a guide for a week or longer",
 "seo_title": "Shimoda, Japan: Beaches, Old Town and a Week-Long Stay",
 "description": "Shimoda is a small port town at the tip of Izu with nine official beaches. A week lets you pick beaches by mood, walk the old town and cook local fish.",
 "dek": "Shimoda is a small port town at the southern tip of the Izu Peninsula. In a week, you can pick beaches by mood, cook local fish and settle in.",
 "card": "Shimoda is a port town at the southern tip of Izu, with nine official beaches and an old town you can walk. A week gives you time to pick beaches by mood, shop for fish and cook, and see the town outside the summer rush.",
 "keywords": [("shimoda", "5,400", "21"), ("shimoda japan", "5,400", "21"), ("shimoda beaches", "210", "—")],
 "intent": "Know → Do（どんな町か → 1週間をどう過ごすか）",
 "points": [
   "Pick a beach by what you want: calm coves for children, surf beaches, or a quieter stretch of sand.",
   "The old town is easy on foot: the ropeway, port and Perry Road are within 15 minutes of the station.",
   "Outside summer it’s quieter, with daffodils in winter, the Black Ship Festival in May and hydrangeas in June.",
 ],
 "body": """
<h2>Is Shimoda worth a week?</h2>
<p>We think so, if you want more than one beach and a quick look at the station area. A night is enough to swim once and eat well. A week lets you try different beaches, find a café you like and fall into the town’s slower rhythm.</p>
<p>Shimoda sits at the southern tip of the [[l:izu|Izu Peninsula]]. It’s a small place, with about 18,400 people on the register in November 2026 [[s:shimoda_population]], and around 47 kilometres of coastline [[s:shimoda_profile]]. It also has a big place in history: the 1854 Treaty of Kanagawa made Shimoda one of the country’s first two open ports [[s:shimoda_hist_perry]].</p>
<p>The train ride from Tokyo is long enough that you’ll want to stay put once you’re here. We’ve covered trains, fares and bus passes in [[l:izu-from-tokyo|our guide to getting to Izu from Tokyo]]. If you have more than a week, we’d spend most of it in Shimoda and add a night or two elsewhere on the peninsula.</p>

<h2>Which Shimoda beach suits you?</h2>
<p>It depends on what you want from the day, because Shimoda’s nine official beaches are surprisingly different. Some are sheltered coves where small children can paddle, and others are known for surfing.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Beach</th><th>What it’s like</th><th>Good for</th><th>From Izukyu-Shimoda Station</th></tr></thead>
<tbody>
<tr><td><strong>Nabetahama</strong> (130 m)</td><td>The beach closest to town, in an inlet with hardly any waves. There’s no car park or shower [[s:shimoda_kanko_beach_nabeta]].</td><td>A quick swim, small children</td><td>Bus from stand 3 or 4, about 7 min, then 5 min on foot [[s:shimoda_kanko_beach_nabeta]]</td></tr>
<tr><td><strong>Sotoura</strong> (470 m)</td><td>A cove with shallow, calm water, popular with families. People sea-kayak further out. No surfing area [[s:shimoda_kanko_beach_sotoura]].</td><td>Children, calm swimming</td><td>Bus from stand 9, about 10 min, then 3 min on foot [[s:shimoda_kanko_beach_sotoura]]</td></tr>
<tr><td><strong>Shirahama Chuo</strong> (720 m)</td><td>The quiet north end of the Shirahama coast, with rock pools. It’s the only beach in Shimoda where you can barbecue [[s:shimoda_kanko_beach_shirahamachuo]].</td><td>Families, rock pools</td><td>Bus from stand 9, about 18 min, then 1 min on foot [[s:shimoda_kanko_beach_shirahamachuo]]</td></tr>
<tr><td><strong>Shirahama Ohama</strong> (about 700 m)</td><td>One of the largest beaches in Izu, by the main coast road and busy with surfers and young people [[s:shimoda_beaches_city,shimoda_kanko_beach_shirahama]].</td><td>A lively day, surfing</td><td>Bus from stand 9, about 15 min [[s:shimoda_kanko_beach_shirahama]]</td></tr>
<tr><td><strong>Tatadohama</strong> (450 m)</td><td>Well known for surfing and bodyboarding, with national contests. It has warm showers you can use all year [[s:shimoda_kanko_beach_tatado]].</td><td>Surfing</td><td>Bus from stand 3 or 4, about 7 min, then 3 min on foot [[s:shimoda_kanko_beach_tatado]]</td></tr>
<tr><td><strong>Kisami Ohama</strong> (770 m)</td><td>A big beach away from the main road, so it feels quieter. Surfers and families share it, and there are cafés nearby [[s:shimoda_kanko_beach_kisami]].</td><td>A long, quieter day</td><td>Bus from stand 3 or 4, about 10 min, then 8 min on foot [[s:shimoda_kanko_beach_kisami]]</td></tr>
</tbody></table></div>
<p class="fine">Beach lengths are the tourism association’s figures; for Shirahama Ohama, the city’s list. The “stand” is the numbered bus stop outside the station.</p>
<p>The other three are smaller. Iritahama is a calm beach lined with cycad trees, and surfers use it too [[s:shimoda_kanko_beach_irita]]. Kujuppama is a 50-metre cove next to the Suzaki Imperial Villa, with rock pools on both sides and no large tents allowed [[s:shimoda_kanko_beach_kujuppama]]. Toji is rarely crowded and close to the Ryugu sea cave, but only four or five buses a day go there [[s:shimoda_kanko_beach_toji]].</p>
<p>The water is clean, too. In Shizuoka Prefecture’s 2026 survey, all nine beaches got the top AA grade [[s:pref_beach_water_2026]]. Six of them are also certified for safety by the Japan Lifesaving Association: Shirahama Chuo, Shirahama Ohama, Sotoura, Tatadohama, Iritahama and Kisami Ohama [[s:shimoda_beaches_city]].</p>
<p>Lifeguards only work during the official season, which the city sets each year [[s:shimoda_ohama]]. Our [[l:izu-from-tokyo|Izu travel guide]] has this year’s dates. In season, the beaches ban tents (sunshades are fine), open fires and barbecues outside part of Shirahama Chuo, fireworks, overnight camping and, since 2025, amplified speakers [[s:shimoda_kanko_umi]].</p>

<h2>What can you do in Shimoda besides the beach?</h2>
<p>Quite a lot, and most of it is within a short walk of the station. On a day off the sand, we’d start high up, wander the old town and finish in a hot bath.</p>
<p>The Shimoda Ropeway station is a one-minute walk from Izukyu-Shimoda Station. From the top of Mt Nesugata you can see the town, the port, the Izu Islands and the Amagi mountains [[s:shimoda_nesugata]]. Back down, the port and the Michi-no-Eki, a roadside market building, are about 10 minutes away on foot [[s:shimoda_michinoeki]].</p>
<p>Perry Road and Ryosenji temple are about 15 minutes from the station [[s:shimoda_perryroad,shimoda_ryosenji]]. Later in 1854, the follow-up Shimoda Treaty was signed in Ryosenji’s main hall. Perry Road is named after the route Perry’s men marched to the temple, and its stone paving runs for about 500 metres along a small stream [[s:shimoda_hist_perry,shimoda_perryroad]]. Further out, Gyokusenji temple housed Japan’s first US consulate, opened by Townsend Harris in 1856 [[s:shimoda_hist_harris,shimoda_gyokusenji]].</p>
<p>For a bath, the tourism association lists eight hotels and inns that take day visitors. As of November 2026 they charge ¥600 to ¥1,500 for adults, mostly from mid-afternoon, and they may turn you away when they’re busy [[s:shimoda_kanko_onsen]]. There’s also a free footbath, Kaikoku-no-yu, in front of the station, open from 9:00 to 17:00 [[s:shimoda_kanko_onsen]].</p>
<p>Rain doesn’t have to ruin the day. The Michi-no-Eki has a harbour museum about the town’s history on its fourth floor [[s:shimoda_michinoeki]], and Ryosenji has a treasure hall [[s:shimoda_ryosenji]]. On drier days, the Wakanoura promenade is a 1.2-kilometre, 15-minute coastal walk, and the paths round Shimoda Park take about an hour and a half [[s:shimoda_kanko_promenade]].</p>

<h2>Is Shimoda worth visiting outside summer?</h2>
<p>Yes. The beaches are quiet, but there’s something on in most seasons, and the city puts the average annual temperature at about 17°C [[s:shimoda_profile]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>When</th><th>What’s on</th></tr></thead>
<tbody>
<tr><td>20 December to 31 January</td><td>The daffodil festival at Tsumekizaki, with up to about 3 million flowers, usually at their best in January. Bus no. 10 from the station takes about 20 minutes [[s:shimoda_kanko_suisen]].</td></tr>
<tr><td>Winter into early spring</td><td>Camellias in Shimoda Park, with about 160 garden varieties [[s:shimoda_park]]. Cherry blossoms follow from mid-March to early April [[s:shimoda_kanko_event]].</td></tr>
<tr><td>May</td><td>The Black Ship Festival, held since 1934. In 2026 it ran from 15 to 17 May, with fireworks over the port, a US–Japan parade and a re-enactment of the Shimoda Treaty at Ryosenji [[s:shimoda_kanko_kurofune]].</td></tr>
<tr><td>June</td><td>The hydrangea festival in Shimoda Park, with about 3 million blooms of over 100 varieties (1 to 30 June in 2026). The park is hilly, and carts are on hand for people who find walking hard [[s:shimoda_kanko_ajisai]].</td></tr>
<tr><td>July and August</td><td>Beach season. In 2026 there were fireworks at Shirahama on 25 July, and the old town’s Taiko Matsuri drum festival is held on 14 and 15 August [[s:shimoda_kanko_event]].</td></tr>
<tr><td>Autumn</td><td>Hand-held <em>te-zutsu</em> fireworks (10 October in 2026), the Shirahama shrine festival in late October, and the start of the spiny lobster (<em>ise-ebi</em>) season, which runs to early May [[s:shimoda_kanko_event]].</td></tr>
</tbody></table></div>
<p>Summer is when the town fills up, and in our experience it’s also when more of our guests stay for longer. If you’d rather walk, soak and eat well than swim, we’d pick the cooler months.</p>

<h2>How do you shop and cook for a week in Shimoda?</h2>
<p>Buy your fish at the port and cook it yourself. The Izu Fisheries Cooperative shop is on the ground floor of the Michi-no-Eki Kaikoku Shimoda Minato. It sells kinmedai, live spiny lobster, turban shells and other seafood, and the prefecture lists it as open from 8:00 to 16:30 with no fixed closing day [[s:pref_izu_gyokyo_shop,shimoda_kanko_gift]]. The JA farmers’ shop in the same building has local vegetables, wasabi and products made from New Summer oranges [[s:shimoda_kanko_gift]].</p>
<p>If you’d rather have someone else cook the town’s famous red fish, our [[l:kinmedai|guide to kinmedai]] covers where to eat it. For everyday shopping, there are supermarkets and convenience stores in town, so a kitchen makes a week much cheaper and more relaxed.</p>
<p>Rubbish takes a little learning. Shimoda collects burnable rubbish twice a week in city bags, and cans, bottles, PET bottles and paper twice a month, each sorted separately [[s:shimoda_gomi]]. Where you stay will have its own system, so it’s easiest to ask your host on the first day. On your first day, we’d also do this:</p>
<ol>
<li>Find the nearest supermarket and the fish shop at the Michi-no-Eki.</li>
<li>Ask your host how to sort rubbish and where it goes.</li>
<li>Pick up a map at the tourism information centre near the station, open from 9:00 to 16:45 [[s:shimoda_kanko_about]].</li>
<li>Look up the bus times for the beaches you want, since some routes run only a few times a day.</li>
<li>Find the nearest high ground from where you’re staying (see the next section).</li>
</ol>

<h2>What should you know about tsunamis in Shimoda?</h2>
<p>If you feel a strong earthquake near the coast, go to high ground straight away, without waiting for a warning [[s:jma_tsunami_warnings]]. Shimoda faces the open sea, and in 1854 the Ansei tsunami swept Shimoda Bay and destroyed most of the town’s houses [[s:shimoda_hist_ansei]].</p>
<p>We don’t say that to scare you. Shizuoka Prefecture’s 2013 estimate put the highest possible tsunami in Shimoda, in the worst case, at 33 metres [[s:shimoda_news_2013_08]]. It’s a worst case rather than a forecast, but it’s why the advice is to get up high, fast. Japan’s weather agency, JMA, aims to issue alerts about three minutes after an earthquake [[s:jma_tsunami_warnings]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Alert</th><th>Expected wave</th><th>What to do</th></tr></thead>
<tbody>
<tr><td><strong>Tsunami advisory</strong></td><td>0.2 to 1 m</td><td>Get out of the water and away from the shore [[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>Tsunami warning</strong></td><td>1 to 3 m</td><td>Move to high ground or an evacuation building at once [[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>Major tsunami warning</strong></td><td>Over 3 m</td><td>Move to high ground or an evacuation building at once [[s:jma_tsunami_warnings]]</td></tr>
</tbody></table></div>
<p>Tsunamis come in several waves, so JMA advises staying put until the alert is lifted [[s:jma_tsunami_warnings]]. The city publishes hazard and evacuation maps, though only in Japanese [[s:shimoda_tsunami_map]]. It has also named a few tsunami evacuation buildings [[s:shimoda_tsunami_bldg]], and it runs an online map that shows the height above sea level of any spot you tap [[s:shimoda_elevation_map]].</p>
<p>The Japan Tourism Agency’s free app, Safety tips, sends earthquake, tsunami and weather warnings in English and other languages [[s:jta_safety_tips]]. We’d install it before you arrive. During the tsunami alerts in late July 2025, we sent our overseas guests messages as things changed, explaining what was happening and that they needed to evacuate. In our experience, a clear message in English makes a big difference.</p>

<h2>Where should you stay in Shimoda for a week?</h2>
<p>Without a car, we’d stay in the old town near the station. Shops, the port and every bus route are close by. If the beach is the whole point of your trip, staying near it saves you the bus rides.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Area</th><th>Suits you if…</th><th>Keep in mind</th></tr></thead>
<tbody>
<tr><td><strong>Old town, near the station</strong></td><td>You want to walk to shops, the port and Perry Road, and reach any beach by bus.</td><td>You’ll need a bus or a bike for most beaches.</td></tr>
<tr><td><strong>Shirahama</strong></td><td>You want the big beaches on your doorstep.</td><td>It’s about 15 minutes by bus from town [[s:shimoda_kanko_beach_shirahama]], so evenings out mean a ride back.</td></tr>
<tr><td><strong>Southern beaches</strong> (Tatado, Irita, Kisami)</td><td>You’re here to surf or want a quieter beach.</td><td>They’re 7 to 10 minutes by bus from the station [[s:shimoda_kanko_beach_tatado,shimoda_kanko_beach_kisami]], plus a short walk.</td></tr>
</tbody></table></div>
<p>Bikes help a lot. The tourism association rents bikes and e-bikes at the Michi-no-Eki from ¥500 for an hour or ¥2,000 for a day, from 9:00 to 17:00. You don’t need to book, but you’ll need ID such as a passport [[s:shimoda_kanko_bicycle]].</p>
<p>We run <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, an apartment of about 40 m² in the old town for up to four guests. It has a kitchen, a washing machine and gas dryer, and a work desk. It’s on the first floor, up about 13 steps, with a shower but no bath [[s:node_room]]. It’s eight minutes’ walk on the flat from the station, with a supermarket three minutes away and Perry Road five [[s:node_access]]. One guest who stayed in January wrote that the sea was close enough to watch the year’s first sunrise, and the supermarket was handy.</p>
<p>If a week turns into thoughts of a month or more, our guide to [[l:monthly-rental|renting a place by the month in Japan]] explains how that works.</p>
""",
 "faq": [
   ("Is Shimoda worth visiting?",
    "Yes, especially for a week. It’s a small port town at the tip of Izu with nine official beaches, a walkable old town and seasonal festivals [[s:shimoda_population,shimoda_kanko_umi,shimoda_kanko_event]]. A week lets you try several beaches and live at the town’s pace."),
   ("What is the best beach in Shimoda?",
    "It depends on what you want. Sotoura and Nabetahama are calm coves that suit children [[s:shimoda_kanko_beach_sotoura,shimoda_kanko_beach_nabeta]]. Tatadohama is the best-known surf beach [[s:shimoda_kanko_beach_tatado]], and Kisami Ohama is big and quieter [[s:shimoda_kanko_beach_kisami]]."),
   ("Can you swim in Shimoda outside summer?",
    "Lifeguards only work during the official season, which the city sets each year, so outside it you swim without them [[s:shimoda_ohama]]. Tatadohama has warm showers you can use all year [[s:shimoda_kanko_beach_tatado]]."),
   ("What is there to do in Shimoda in winter?",
    "The daffodil festival at Tsumekizaki runs from 20 December to 31 January [[s:shimoda_kanko_suisen]], and camellias bloom in Shimoda Park [[s:shimoda_park]]. Day hot springs, the ropeway and coastal walks fill the rest of the week [[s:shimoda_kanko_onsen,shimoda_nesugata,shimoda_kanko_promenade]]."),
   ("What should I do if there’s a tsunami warning in Shimoda?",
    "Move to high ground or an evacuation building at once, and stay until the warning is lifted. If you feel strong shaking near the coast, go without waiting for a warning [[s:jma_tsunami_warnings]]. The free Safety tips app sends alerts in English [[s:jta_safety_tips]]."),
 ],
 "sources": ["shimoda_population", "shimoda_profile", "shimoda_hist_perry", "shimoda_hist_harris", "shimoda_hist_ansei",
             "shimoda_perryroad", "shimoda_ryosenji", "shimoda_gyokusenji", "shimoda_nesugata", "shimoda_park", "shimoda_michinoeki",
             "shimoda_beaches_city", "shimoda_kanko_umi", "shimoda_kanko_beach_nabeta", "shimoda_kanko_beach_sotoura",
             "shimoda_kanko_beach_shirahamachuo", "shimoda_kanko_beach_shirahama", "shimoda_kanko_beach_tatado",
             "shimoda_kanko_beach_kisami", "shimoda_kanko_beach_irita", "shimoda_kanko_beach_kujuppama", "shimoda_kanko_beach_toji",
             "pref_beach_water_2026", "shimoda_ohama", "shimoda_kanko_onsen", "shimoda_kanko_promenade", "shimoda_kanko_suisen",
             "shimoda_kanko_event", "shimoda_kanko_kurofune", "shimoda_kanko_ajisai", "pref_izu_gyokyo_shop", "shimoda_kanko_gift",
             "shimoda_gomi", "shimoda_kanko_about", "jma_tsunami_warnings", "shimoda_news_2013_08", "shimoda_tsunami_map",
             "shimoda_tsunami_bldg", "shimoda_elevation_map", "jta_safety_tips", "shimoda_kanko_bicycle", "node_room", "node_access"],
 "related": ["izu-from-tokyo", "kinmedai", "monthly-rental"],
 "ja": {
  "h1": "下田（日本）：1週間以上いる人のためのガイド",
  "dek": "下田は、伊豆半島の南端にある小さな港町です。1週間いれば、その日の気分で浜を選び、地元の魚を料理して、町の暮らしになじめます。",
  "review": [
   "【2026-11-20 新規の下書き（執筆部）】書いた点: ①7つの節（1週間いる価値／浜の選び方／浜以外の過ごし方／夏以外の季節／買い物と料理・ごみ／津波／どこに泊まるか）。事実はすべて、リサーチメモで開いて確かめた市・県・観光協会・気象庁・観光庁のページによります ②浜の表は6つ（鍋田浜・外浦・白浜中央・白浜大浜・多々戸浜・吉佐美大浜）、残りの3つ（入田浜・九十浜・田牛）は文章で。白浜大浜の長さは市の一覧の「約700m」、ほかの長さは観光協会の値です ③人口は「約18,400人（2026年11月の住民基本台帳）」。日米和親条約は「1854年に下田を最初に開いた2つの港の1つにした」とだけ書き、調印の場所は書いていません。了仙寺は付録の「下田条約」の場として書きました（和暦の月日は西暦に直さず、年だけ） ④津波の体験は、種類（警報・注意報）を書かず「2025年7月末の津波の警報のとき（tsunami alerts）」とし、中身は「外国人ゲストに状況と避難の必要性を、状況が変わるたびにメッセージで伝えた」だけにしました（キャンセル・返金の話は入れていません） ⑤静岡県の2013年の想定（下田の最大の津波の高さ33m）を「最悪の場合の想定で、予報ではない」と添えて1文入れました。到達時間は書いていません ⑥NODE Shimoda は最後の節で1回だけ（アパートの一室・約40㎡・最大4名・2階で階段約13段・シャワーのみ・駅から平坦な道で徒歩8分・スーパー3分・ペリーロード5分）。料金・週割・泊数の上限は書いていません。写真は本文に入れていません ⑦ゲストの声（2026年1月）は「初日の出が見えるほど海が近かった」と要約して1回だけ使いました（引用符・名前なし） ⑧共食いを避けるため、行き方・運賃・フリーきっぷ・2026年の海水浴の期間は書かず、izu-from-tokyo へリンクで送りました（本文から2回）。店で食べる金目鯛は kinmedai、1か月以上の部屋は monthly-rental へ ⑨書かないと決めたこと（ロープウェイの運賃・時間、月別の平年値、津波の到達時間、水質の「認証」、サーフィン区域の線引き、バスの系統名・時刻、道の駅全体の営業時間、スーパーの店名、英語のごみ分別表、共同浴場、水族館の営業時間・料金）は書いていません ⑩見出し写真は TODO-PHOTO（編集長が Unsplash で人の少ない白い砂浜を用意）。alt は地名なしの案です",
   "【人に確かめてほしい点】①津波の体験の書き方: experience.md は「津波注意報」ですが、気象庁の記録では静岡県は最初「津波警報」で、のちに注意報に下がりました。記事では種類を書かず “tsunami alerts” としています。この書き方でよいか ②変わりやすい数字（2026年11月に確認）: 日帰り入浴の料金（600〜1,500円）、レンタサイクルの料金と時間、観光案内所の時間、漁協の直売所の時間（県のページは2025年4月更新）、行事の日付（黒船祭・あじさい祭・花火は2026年の日付、水仙まつりは毎年12月20日〜1月31日） ③33mの想定を入れるか（怖がらせない書き方にしたつもりです。外してもよい） ④NODE Shimoda の「2階で階段約13段・シャワーのみ」を正直に書きました（公式サイトの記載どおり）。長く泊まる人の判断に役立つと考えています ⑤IZU のページの keywords から「shimoda japan」を外してこの記事に移すこと、IZU・izu-from-tokyo・kinmedai からこの記事へのリンクを足すことは、エンジニア部の作業です（構成案の依頼）",
  ],
  "points": [
    "浜は、目的で選びます。子ども連れには穏やかな入り江、サーフィンならサーフィンの浜、静かに過ごすなら広い浜です。",
    "旧町内は歩いて回れます。ロープウェイ、港、ペリーロードは、どれも駅から15分以内です。",
    "夏以外は静かで、冬は水仙、5月は黒船祭、6月はあじさいがあります。",
  ],
  "body": """
<h2>下田に1週間いる価値はあるか</h2>
<p>浜を1つ見て駅前を少し歩くだけでは物足りないなら、あると私たちは思います。1泊なら、1回泳いでおいしいものを食べれば終わりです。1週間あれば、いろいろな浜を試し、気に入ったカフェを見つけ、町のゆっくりした調子に体がなじんでいきます。</p>
<p>下田は[[l:ja-izu|伊豆半島]]の南端にあります。住民基本台帳の人口は2026年11月で約18,400人の小さな町で[[s:shimoda_population]]、海岸線は約47kmあります[[s:shimoda_profile]]。日本が外に開いた最初の町のひとつでもあり、1854年の日米和親条約で、下田は日本で最初に開かれた2つの港の1つになりました[[s:shimoda_hist_perry]]。</p>
<p>東京からの電車はそれなりに長いので、着いたら腰を落ち着けたくなるはずです。電車・運賃・バスのきっぷは、[[l:ja-izu-from-tokyo|東京から伊豆への行き方の記事]]にまとめています。1週間より長くいられるなら、私たちならほとんどを下田で過ごし、半島のほかの町に1〜2泊足します。</p>

<h2>下田のどの浜が合うか</h2>
<p>その日に何をしたいかで決まります。下田の9つの海水浴場は、思った以上に性格が違うからです。小さな子どもが水遊びできる穏やかな入り江もあれば、サーフィンで知られる浜もあります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>浜</th><th>どんな浜か</th><th>向いていること</th><th>伊豆急下田駅から</th></tr></thead>
<tbody>
<tr><td><strong>鍋田浜</strong>（130m）</td><td>町にいちばん近い浜で、入り江のためほとんど波がありません。駐車場とシャワーはありません[[s:shimoda_kanko_beach_nabeta]]。</td><td>ちょっと泳ぐ、小さな子ども</td><td>3番か4番乗り場のバスで約7分、そこから徒歩5分[[s:shimoda_kanko_beach_nabeta]]</td></tr>
<tr><td><strong>外浦</strong>（470m）</td><td>遠浅で波の穏やかな入り江で、家族連れに人気です。沖ではシーカヤックをする人もいます。サーフィンの区域はありません[[s:shimoda_kanko_beach_sotoura]]。</td><td>子ども連れ、穏やかに泳ぐ</td><td>9番乗り場のバスで約10分、そこから徒歩3分[[s:shimoda_kanko_beach_sotoura]]</td></tr>
<tr><td><strong>白浜中央</strong>（720m）</td><td>白浜海岸の北の端の静かな浜で、磯遊びができます。下田で唯一バーベキューができる浜です[[s:shimoda_kanko_beach_shirahamachuo]]。</td><td>家族連れ、磯遊び</td><td>9番乗り場のバスで約18分、そこから徒歩1分[[s:shimoda_kanko_beach_shirahamachuo]]</td></tr>
<tr><td><strong>白浜大浜</strong>（約700m）</td><td>伊豆でも最大級の浜で、国道沿いにあり、サーファーや若い人でにぎわいます[[s:shimoda_beaches_city,shimoda_kanko_beach_shirahama]]。</td><td>にぎやかな1日、サーフィン</td><td>9番乗り場のバスで約15分[[s:shimoda_kanko_beach_shirahama]]</td></tr>
<tr><td><strong>多々戸浜</strong>（450m）</td><td>サーフィンとボディボードで知られ、全国大会も開かれます。一年中使える温水シャワーがあります[[s:shimoda_kanko_beach_tatado]]。</td><td>サーフィン</td><td>3番か4番乗り場のバスで約7分、そこから徒歩3分[[s:shimoda_kanko_beach_tatado]]</td></tr>
<tr><td><strong>吉佐美大浜</strong>（770m）</td><td>国道から離れた大きな浜で、静かに感じます。サーファーと家族連れが一緒に使い、近くにカフェもあります[[s:shimoda_kanko_beach_kisami]]。</td><td>長く、静かに過ごす1日</td><td>3番か4番乗り場のバスで約10分、そこから徒歩8分[[s:shimoda_kanko_beach_kisami]]</td></tr>
</tbody></table></div>
<p class="fine">浜の長さは観光協会の値です（白浜大浜は市の一覧の値）。「乗り場」は、駅前のバス乗り場の番号です。</p>
<p>残りの3つは小さめです。入田浜はソテツの並ぶ落ち着いた浜で、サーファーも使います[[s:shimoda_kanko_beach_irita]]。九十浜は須崎御用邸の隣の50mの入り江で、両側の岩場で磯遊びができ、大きなテントは使えません[[s:shimoda_kanko_beach_kujuppama]]。田牛は混みにくく龍宮窟にも近いのですが、バスは1日4〜5本だけです[[s:shimoda_kanko_beach_toji]]。</p>
<p>水もきれいです。静岡県の2026年度の調査で、9つの浜はすべていちばん上の「AA」でした[[s:pref_beach_water_2026]]。そのうち白浜中央・白浜大浜・外浦・多々戸浜・入田浜・吉佐美大浜の6つは、日本ライフセービング協会の安全の認定も受けています[[s:shimoda_beaches_city]]。</p>
<p>監視員がいるのは、市が毎年決める海水浴の期間だけです[[s:shimoda_ohama]]。今年の期間は[[l:ja-izu-from-tokyo|伊豆の旅の記事]]に載せています。期間中の浜では、テント（日よけのパラソルはよい）、直火とバーベキュー（白浜中央の一部を除く）、花火、泊まりがけのキャンプ、そして2025年からは音を大きくするスピーカーが禁止されています[[s:shimoda_kanko_umi]]。</p>

<h2>下田で、浜のほかに何ができるか</h2>
<p>けっこうたくさんあり、ほとんどが駅から歩いて行けます。浜に行かない日なら、私たちは高い所から始めて、旧町内を歩き、最後に温泉に入ります。</p>
<p>下田ロープウェイの乗り場は、伊豆急下田駅から歩いて1分です。寝姿山の山頂からは、町、港、伊豆諸島、天城の山々が見えます[[s:shimoda_nesugata]]。下りたら、港と道の駅（道路沿いの市場のような建物）までは歩いて約10分です[[s:shimoda_michinoeki]]。</p>
<p>ペリーロードと了仙寺は、駅から約15分です[[s:shimoda_perryroad,shimoda_ryosenji]]。同じ1854年の後半に、日米和親条約の付録の「下田条約」が了仙寺の本堂で結ばれました。ペリーロードの名前は、ペリーの一行が了仙寺まで行進した道に由来し、石畳が小さな川に沿って約500m続きます[[s:shimoda_hist_perry,shimoda_perryroad]]。少し離れた玉泉寺には、1856年にハリスが開いた日本で最初の米国総領事館が置かれました[[s:shimoda_hist_harris,shimoda_gyokusenji]]。</p>
<p>温泉なら、観光協会が日帰り入浴のできるホテル・旅館を8軒載せています。2026年11月時点で大人600〜1,500円、多くは午後の半ばからで、混んでいるときは断られることもあります[[s:shimoda_kanko_onsen]]。駅前には、無料の足湯「開国の湯」もあり、9時〜17時に使えます[[s:shimoda_kanko_onsen]]。</p>
<p>雨の日も、楽しみ方はあります。道の駅の4階には町の歴史を伝えるハーバーミュージアムがあり[[s:shimoda_michinoeki]]、了仙寺には宝物館があります[[s:shimoda_ryosenji]]。晴れた日なら、和歌の浦遊歩道は海沿いを1.2km・約15分で歩け、下田公園の遊歩道はひと回り約1時間半です[[s:shimoda_kanko_promenade]]。</p>

<h2>夏以外の下田は、行く価値があるか</h2>
<p>あります。浜は静かですが、たいていの季節に何かしらの行事があり、市は年の平均気温を約17℃としています[[s:shimoda_profile]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>時期</th><th>行事・見どころ</th></tr></thead>
<tbody>
<tr><td>12月20日〜1月31日</td><td>爪木崎の水仙まつり。最大で約300万本の水仙が咲き、見ごろはたいてい1月です。駅から10番乗り場のバスで約20分です[[s:shimoda_kanko_suisen]]。</td></tr>
<tr><td>冬から早春</td><td>下田公園の椿。園芸品種は約160種あります[[s:shimoda_park]]。3月中旬〜4月上旬は桜です[[s:shimoda_kanko_event]]。</td></tr>
<tr><td>5月</td><td>1934年から続く黒船祭。2026年は5月15〜17日で、港の花火、日米のパレード、了仙寺での下田条約の再現がありました[[s:shimoda_kanko_kurofune]]。</td></tr>
<tr><td>6月</td><td>下田公園のあじさい祭。100種以上・約300万輪が咲きます（2026年は6月1〜30日）。公園は坂が多く、歩くのがつらい人のためのカートがあります[[s:shimoda_kanko_ajisai]]。</td></tr>
<tr><td>7月・8月</td><td>海水浴の季節。2026年は7月25日に白浜で花火があり、旧町内の太鼓祭りは8月14・15日です[[s:shimoda_kanko_event]]。</td></tr>
<tr><td>秋</td><td>手筒花火（2026年は10月10日）、10月下旬の白浜神社の例大祭、そして5月上旬まで続く伊勢海老の季節の始まりです[[s:shimoda_kanko_event]]。</td></tr>
</tbody></table></div>
<p>町がいちばんにぎわうのは夏で、私たちの宿でも、夏は長く泊まる人が増えます。泳ぐより、歩いて、温泉に入って、おいしいものを食べたいなら、私たちは涼しい季節を選びます。</p>

<h2>下田で1週間、どう買い物して料理するか</h2>
<p>魚は港で買って、自分で料理するのがおすすめです。伊豆漁協の直売所は、道の駅「開国下田みなと」の1階にあります。金目鯛、生きた伊勢海老、サザエなどの魚介を売っていて、静岡県のページでは8時〜16時30分・定休日なしです[[s:pref_izu_gyokyo_shop,shimoda_kanko_gift]]。同じ建物の JA の直売所には、地元の野菜、わさび、ニューサマーオレンジを使った品があります[[s:shimoda_kanko_gift]]。</p>
<p>町の名物の赤い魚を誰かに料理してもらいたいなら、[[l:ja-kinmedai|金目鯛の記事]]に食べられる所をまとめています。日々の買い物には町なかにスーパーやコンビニがあるので、キッチンがあれば、1週間がずっと安く、気楽になります。</p>
<p>ごみの出し方は、少し慣れが要ります。下田市は、燃えるごみを週2回、市の指定袋で集め、缶・びん・ペットボトル・紙などは月2回、それぞれ分けて集めます[[s:shimoda_gomi]]。泊まる所ごとにやり方があるので、初日に宿の人に聞くのがいちばん簡単です。初日には、私たちならこんなこともします。</p>
<ol>
<li>いちばん近いスーパーと、道の駅の魚の直売所の場所を確かめる。</li>
<li>ごみの分け方と出す場所を、宿の人に聞く。</li>
<li>駅の近くの観光案内所（9時〜16時45分）で地図をもらう[[s:shimoda_kanko_about]]。</li>
<li>行きたい浜のバスの時刻を調べる。1日に数本しかない路線もあります。</li>
<li>泊まる所から、いちばん近い高い場所を確かめる（次の節）。</li>
</ol>

<h2>下田の津波について、何を知っておくべきか</h2>
<p>海の近くで強い揺れを感じたら、警報を待たずに、すぐ高い所へ逃げてください[[s:jma_tsunami_warnings]]。下田は外洋に面していて、1854年には安政の大津波が下田湾を襲い、町の家のほとんどが流されたり壊れたりしました[[s:shimoda_hist_ansei]]。</p>
<p>怖がらせたいのではありません。静岡県の2013年の想定では、最悪の場合、下田の最大の津波の高さは33mでした[[s:shimoda_news_2013_08]]。予報ではなく最悪の場合の想定ですが、「とにかく早く高い所へ」と言われるのはそのためです。気象庁は、地震からおよそ3分で津波の警報・注意報を出すことを目指しています[[s:jma_tsunami_warnings]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>発表</th><th>予想される高さ</th><th>すること</th></tr></thead>
<tbody>
<tr><td><strong>津波注意報</strong></td><td>0.2〜1m</td><td>海から上がり、海岸から離れる[[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>津波警報</strong></td><td>1〜3m</td><td>すぐに高台か避難ビルへ[[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>大津波警報</strong></td><td>3mを超える</td><td>すぐに高台か避難ビルへ[[s:jma_tsunami_warnings]]</td></tr>
</tbody></table></div>
<p>津波は何度も来るので、気象庁は、警報・注意報が解除されるまで避難を続けるよう呼びかけています[[s:jma_tsunami_warnings]]。市は津波ハザードマップと避難の地図を出していますが、日本語だけです[[s:shimoda_tsunami_map]]。津波避難ビルもいくつか指定していて[[s:shimoda_tsunami_bldg]]、地図の上でたたいた場所の海抜が分かる、オンラインの地図もあります[[s:shimoda_elevation_map]]。</p>
<p>観光庁の無料のアプリ「Safety tips」は、地震・津波・気象の警報を英語などで知らせてくれます[[s:jta_safety_tips]]。着く前に入れておくのがおすすめです。2025年7月末の津波の警報のとき、私たちは海外からのゲストに、状況が変わるたびにメッセージを送り、何が起きているかと、避難が必要なことを伝えました。英語ではっきり伝えることが大きな違いになる、というのが私たちの実感です。</p>

<h2>下田で1週間、どこに泊まるか</h2>
<p>車がないなら、私たちは駅に近い旧町内に泊まります。店も港も、どのバスの路線もすぐ近くです。浜が旅のいちばんの目的なら、浜の近くに泊まればバスに乗らずに済みます。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>地区</th><th>こんな人に合う</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>旧町内（駅の周り）</strong></td><td>店・港・ペリーロードに歩いて行き、浜へはバスで行きたい人。</td><td>たいていの浜へは、バスか自転車が要ります。</td></tr>
<tr><td><strong>白浜</strong></td><td>大きな浜をすぐ目の前にしたい人。</td><td>町からバスで約15分なので[[s:shimoda_kanko_beach_shirahama]]、夜に町へ出ると帰りもバスです。</td></tr>
<tr><td><strong>南の浜</strong>（多々戸・入田・吉佐美）</td><td>サーフィンが目的の人、静かな浜がいい人。</td><td>駅からバスで7〜10分[[s:shimoda_kanko_beach_tatado,shimoda_kanko_beach_kisami]]、そこから少し歩きます。</td></tr>
</tbody></table></div>
<p>自転車があると、ぐっと楽になります。観光協会が道の駅で、自転車と電動自転車を1時間500円から、1日2,000円で貸していて、時間は9時〜17時です。予約は要りませんが、パスポートなどの身分証が要ります[[s:shimoda_kanko_bicycle]]。</p>
<p>私たちは、旧町内で「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」を運営しています。約40㎡のアパートの一室で、最大4名まで泊まれます。キッチン、洗濯機とガス乾燥機、ワークデスクがあります。2階で階段は約13段、浴室はシャワーだけで浴槽はありません[[s:node_room]]。駅から平坦な道を歩いて8分で、スーパーまで3分、ペリーロードまで5分です[[s:node_access]]。1月に泊まったゲストは、初日の出が見えるほど海が近く、スーパーも近くて便利だったとレビューに書いてくれました。</p>
<p>1週間が、1か月以上いたい気持ちに変わったら、[[l:ja-monthly-rental|日本で1か月単位で部屋を借りる記事]]に仕組みをまとめています。</p>
""",
  "faq": [
    ("下田は行く価値がありますか",
     "あります。特に1週間いるなら。伊豆の南端の小さな港町で、9つの海水浴場、歩いて回れる旧町内、季節の行事があります[[s:shimoda_population,shimoda_kanko_umi,shimoda_kanko_event]]。1週間あれば、いくつもの浜を試し、町の調子で暮らせます。"),
    ("下田でいちばんいい浜はどこですか",
     "何をしたいかによります。外浦と鍋田浜は穏やかな入り江で、子ども連れに合います[[s:shimoda_kanko_beach_sotoura,shimoda_kanko_beach_nabeta]]。多々戸浜はいちばん知られたサーフィンの浜で[[s:shimoda_kanko_beach_tatado]]、吉佐美大浜は大きくて静かめです[[s:shimoda_kanko_beach_kisami]]。"),
    ("夏以外でも、下田で泳げますか",
     "監視員がいるのは市が毎年決める海水浴の期間だけなので、期間外は監視員なしで泳ぐことになります[[s:shimoda_ohama]]。多々戸浜には一年中使える温水シャワーがあります[[s:shimoda_kanko_beach_tatado]]。"),
    ("冬の下田では、何ができますか",
     "爪木崎の水仙まつりが12月20日〜1月31日にあり[[s:shimoda_kanko_suisen]]、下田公園では椿が咲きます[[s:shimoda_park]]。日帰り温泉、ロープウェイ、海沿いの散歩で、1週間はすぐに埋まります[[s:shimoda_kanko_onsen,shimoda_nesugata,shimoda_kanko_promenade]]。"),
    ("下田で津波警報が出たら、どうすればいいですか",
     "すぐに高台か避難ビルへ移り、警報が解除されるまでとどまります。海の近くで強い揺れを感じたら、警報を待たずに逃げます[[s:jma_tsunami_warnings]]。無料のアプリ「Safety tips」が英語で知らせてくれます[[s:jta_safety_tips]]。"),
  ],
 },
}
