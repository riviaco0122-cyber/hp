# -*- coding: utf-8 -*-
"""japan-countryside の新規記事（2026-11-21 執筆部）。構成案とリサーチメモ: tools/okaeri/briefs/japan-countryside.md。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "soumu_kaso_r6": ("https://www.soumu.go.jp/main_content/001065428.pdf", "MIC: depopulated areas, FY2024", "総務省「令和6年度版 過疎対策の現況（概要版）」",
                      "Ministry of Internal Affairs and Communications, Current State of Measures for Depopulated Areas, FY2024 edition (summary), March 2026"),
    "jta_lodging_2025": ("https://www.mlit.go.jp/kankocho/content/002026763.pdf", "JTA: lodging statistics 2025", "観光庁「宿泊旅行統計調査（2025年・年間値（確定値））」",
                         "Japan Tourism Agency, Overnight Travel Statistics Survey, 2025 annual (final), July 2026"),
    "jnto_buses": ("https://www.japan.travel/en/plan/getting-around/buses/", "JNTO: Buses in Japan", "JNTO「Buses in Japan」",
                   "Japan National Tourism Organization, Buses in Japan (checked November 2026)"),
    "mlit_transport_wp2026": ("https://www.mlit.go.jp/sogoseisaku/transport/content/002018763.pdf", "MLIT: Transport white paper 2026", "国土交通省「令和8年版交通政策白書について」",
                              "Ministry of Land, Infrastructure, Transport and Tourism, White Paper on Transport Policy 2026 (summary), July 2026"),
    "mlit_pri_demand": ("https://www.mlit.go.jp/pri/houkoku/gaiyou/pdf/kkk147.pdf", "MLIT PRI: local transport services", "国土交通政策研究所「多様な地域公共交通サービスの導入状況に関する調査研究」",
                        "MLIT Policy Research Institute, Study on Diverse Local Public Transport Services, June 2018"),
    "mpd_idp_en": ("https://www.keishicho.metro.tokyo.lg.jp/multilingual/english/traffic_safety/drivers_licenses/index.files/kokusaimenkyo_english.pdf", "Tokyo police: IDP", "警視庁「Valid International Driving Permit in Japan」",
                   "Tokyo Metropolitan Police Department, Valid International Driving Permit in Japan (checked November 2026)"),
    "mpd_foreign_licence_en": ("https://www.keishicho.metro.tokyo.lg.jp/multilingual/english/traffic_safety/drivers_licenses/index.files/gaikokumenkyo_english.pdf", "Tokyo police: foreign licences", "警視庁「Valid Foreign Driving License in Japan」",
                               "Tokyo Metropolitan Police Department, Valid Foreign Driving License in Japan, June 2026"),
    "kyoto_police_driving": ("https://www.pref.kyoto.jp/fukei/foreign/s_men1/gaimen/unten.html", "Kyoto police: driving in Japan", "京都府警察「To drive legally in Japan」",
                             "Kyoto Prefectural Police, To Drive Legally in Japan, September 2024"),
    "egov_waste_act": ("https://laws.e-gov.go.jp/law/345AC0000000137", "Waste Management Act", "廃棄物の処理及び清掃に関する法律",
                       "Act on Waste Management and Public Cleaning (Act No. 137 of 1970), Articles 6 and 6-2"),
    "jnto_homestay": ("https://www.japan.travel/en/guide/homestay-farmstay/", "JNTO: homestays and farmstays", "JNTO「Homestays, Farmstays and WWOOFing in Japan」",
                      "Japan National Tourism Organization, Homestays, Farmstays and WWOOFing in Japan (checked November 2026)"),
    "fdma_ambulance_en": ("https://www.fdma.go.jp/publication/portal/items/portal001_pamphiet_english.pdf", "FDMA: ambulance guide", "総務省消防庁「救急車利用ガイド（英語版）」",
                          "Fire and Disaster Management Agency, Ambulance Usage Guide for Visitors (English)"),
    "iwate_emergency_en": ("https://www.pref.iwate.jp/kyouikubunka/kokusai/1006971/1006994/1006997/1006999.html", "Iwate: emergency medical care", "岩手県「Emergency Medical Care」",
                           "Iwate Prefecture, Emergency Medical Care (checked November 2026)"),
    "ibaraki_ambulance_fee": ("https://www.pref.ibaraki.jp/hokenfukushi/iryo/iryo/isei/sentei_ryoyohi.html", "Ibaraki: non-urgent ambulance fee", "茨城県「救急搬送における選定療養費の徴収について」",
                              "Ibaraki Prefecture, Fees for Non-urgent Ambulance Transport, updated October 2026"),
    "fdma_7119": ("https://www.fdma.go.jp/mission/enrichment/appropriate/appropriate007.html", "FDMA: #7119", "総務省消防庁「救急安心センター事業（♯7119）ってナニ？」",
                  "Fire and Disaster Management Agency, Emergency Medical Telephone Consultation (#7119) (checked November 2026)"),
    "jnto_hotline": ("https://www.japan.travel/en/plan/hotline/", "JNTO: Japan Visitor Hotline", "JNTO「Japan Visitor Hotline」",
                     "Japan National Tourism Organization, Japan Visitor Hotline (checked November 2026)"),
    "jma_baiu": ("https://www.data.jma.go.jp/cpd/baiu/index.html", "JMA: rainy season dates", "気象庁「過去の梅雨入りと梅雨明け」",
                 "Japan Meteorological Agency, Start and End of the Rainy Season (normals 1991–2020)"),
    "jma_baiu_faq": ("https://www.jma.go.jp/jma/kishou/know/faq/faq33.html", "JMA: about the rainy season", "気象庁「梅雨について」",
                     "Japan Meteorological Agency, FAQ: The Rainy Season"),
    "jma_typhoon_normals": ("https://www.data.jma.go.jp/yoho/typhoon/statistics/average/average.html", "JMA: typhoon normals", "気象庁「台風の平年値」",
                            "Japan Meteorological Agency, Typhoon Normals (1991–2020)"),
    "mlit_snow_areas": ("https://www.mlit.go.jp/kokudoseisaku/chisei/content/001881217.pdf", "MLIT: heavy-snow areas", "国土交通省「豪雪地帯及び特別豪雪地帯の指定について（概要）」",
                        "Ministry of Land, Infrastructure, Transport and Tourism, Designated Heavy-snow Areas (as of April 2026)"),
    "maff_nouhaku_status": ("https://www.maff.go.jp/j/nousin/kouryu/nouhakusuishin/attach/pdf/nouhaku_top-141.pdf", "MAFF: nouhaku status 2026", "農林水産省「農泊をめぐる状況について」",
                            "Ministry of Agriculture, Forestry and Fisheries, The State of Nouhaku (as of 20 November 2026)"),
    "jnto_minshuku": ("https://www.japan.travel/en/guide/guesthouse-budget-accommodation/", "JNTO: minshuku and guesthouses", "JNTO「Minshuku and Guesthouses in Japan」",
                      "Japan National Tourism Organization, Minshuku and Guesthouses in Japan (checked November 2026)"),
    "jnto_ryokan": ("https://www.japan.travel/en/guide/japanese-ryokan/", "JNTO: ryokan guide", "JNTO「Japanese Ryokan Guide」",
                    "Japan National Tourism Organization, Japanese Ryokan Guide (checked November 2026)"),
    "jnto_tic": ("https://www.japan.travel/en/tic/", "JNTO: tourist information centres", "JNTO「Tourist Information Center」",
                 "Japan National Tourism Organization, Tourist Information Center (checked November 2026)"),
    "jnto_tic_cert": ("https://www.japan.travel/en/plan/tic-certification/", "JNTO: TIC certification", "JNTO「TIC Certification Program」",
                      "Japan National Tourism Organization, TIC Certification Program (checked November 2026)"),
    "jta_visitor_survey_2025": ("https://www.mlit.go.jp/kankocho/news08_00039.html", "JTA: visitor survey FY2025", "観光庁「訪日外国人旅行者の受入環境に関する調査」（令和7年度）",
                                "Japan Tourism Agency, Survey on the Visitor Environment for International Travellers, FY2025 (April 2026)"),
    "mlit_michinoeki_2026": ("https://www.mlit.go.jp/report/press/road01_hh_002138.html", "MLIT: michi-no-eki count", "国土交通省「『道の駅』の第65回登録について」",
                             "Ministry of Land, Infrastructure, Transport and Tourism, 65th Registration of Michi-no-Eki, September 2026"),
    "jnto_michinoeki": ("https://www.japan.travel/en/guide/michi-no-eki/", "JNTO: michi-no-eki", "JNTO「Michi-no-Eki — Japan's roadside stations」",
                        "Japan National Tourism Organization, Michi-no-Eki: Japan’s Roadside Stations (checked November 2026)"),
}

# 見出し写真（エンジニア部へ）: 執筆部の環境には Unsplash のコネクタがなく、候補を選べていない。
# 構成案 7章の絵（山あいか海沿いの小さな集落を、田んぼや道越しに見た、人の少ない静かな風景。人の顔・看板・ナンバーなし）で
# Unsplash から選び、download_asset で記録し、名前・alt・説明文を写っているものに合わせて直す（地名は書かない）。
# 下の "rural-village-fields" は仮の名前と仮の alt。選んだら PHOTO_CREDIT_NEW に (撮影者, 撮影者ページ, 写真ページ, ID) を入れる。
PHOTO_CREDIT_NEW = {}

ARTICLE = {
 "id": "japan-countryside", "slug": "japan-countryside", "topic": "stay", "place": None, "also": ["live"],
 "photo": ("rural-village-fields", "Low houses beyond green rice fields, with wooded hills behind", "A quiet village in the countryside."),
 "published": "2026-11-21", "updated": "2026-11-21",
 "kicker": "Stay longer",
 "h1": "The Japanese countryside for a longer stay: choosing a base, getting around and daily life",
 "seo_title": "Japan Countryside: Spending a Week or More in Rural Japan",
 "description": "The Japanese countryside suits a longer stay when your base has a station, a shop you can walk to and buses that run. Then a car becomes optional.",
 "dek": "You can spend weeks in rural Japan without a car or much Japanese. What matters most is your base: a station, a shop on foot and a bus that runs.",
 "card": "A longer stay in rural Japan works best from the right base: a town with a station, a shop you can walk to and buses you can check. Pick that first, then the region. Rubbish rules, shop hours and the season differ by town, so ask on day one.",
 "keywords": [("japan countryside", "9,900", "6"), ("rural japan", "6,600", "12"), ("small towns in japan", "1,900", "7")],
 "intent": "Know → Do（どんなところか → どこを拠点に、どう暮らすか）",
 "points": [
   "Choose your base before your region: a station, a supermarket on foot and buses you can check.",
   "Rural buses can be few and may not take IC cards, so plan your day around the last bus.",
   "Rubbish rules, shop hours and the snow or typhoon season differ by town, so ask on your first day.",
 ],
 "body": """
<p>Most guides to rural Japan are lists of pretty villages, written for a night or two. Once you’re staying a week or longer, the question changes. It’s less “where’s beautiful?” and more “where can I actually live for a while?” We think it’s the question that matters most, so it’s the one we’ll answer here.</p>

<h2>What is a longer stay in rural Japan really like?</h2>
<p>It’s slower and more ordinary than a tour, and we think that’s the point. You unpack once, find a supermarket, learn when the bus comes and go back to the same beach or bakery until people start to nod at you.</p>
<p>There’s a lot of quiet to choose from. About 60% of Japan’s land is officially classed as depopulated, yet fewer than one in ten people live there [[s:soumu_kaso_r6]]. Most visitors don’t get that far: in 2025, about two in three foreign guest nights were spent in and around the big cities [[s:jta_lodging_2025]].</p>
<p>Most of the guests we host come from Europe and North America, and they tend to stay a while. Some work remotely, and some come for the surf. For a stay like that, the town you pick matters far more than any single sight. How long you can stay depends on your passport, and our guide to [[l:how-long-stay|how long you can stay in Japan]] explains the limits. If you’d like to work from here for months, there’s also [[l:digital-nomad|Japan’s digital nomad visa]].</p>

<h2>How do you choose a base in the Japanese countryside?</h2>
<p>Choose it for how daily life works, not for the view. A lovely valley with no shop you can walk to gets hard by day four, while a plain little town with a station can feel easy for weeks.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What to check</th><th>Why it matters on a longer stay</th><th>Where to check</th></tr></thead>
<tbody>
<tr><td><strong>A railway station</strong></td><td>Day trips and the journey home don’t depend on a car</td><td>The railway company’s timetable</td></tr>
<tr><td><strong>A supermarket or convenience store on foot</strong></td><td>You’ll shop and cook most days</td><td>A map, then your host</td></tr>
<tr><td><strong>Buses, and the last one back</strong></td><td>It decides how late you can stay out</td><td>The bus company’s timetable, or a tourist information centre [[s:jnto_tic]]</td></tr>
<tr><td><strong>A place you can rent by the week or month</strong></td><td>A kitchen and a washing machine matter more than a view</td><td>Listings, then a message to the host</td></tr>
<tr><td><strong>A clinic or hospital nearby</strong></td><td>Peace of mind, especially with children</td><td>JNTO’s medical institution search [[s:jnto_medical]]</td></tr>
<tr><td><strong>The season</strong></td><td>Snow, typhoons and the rainy season change what you can do</td><td>The season table further down</td></tr>
</tbody></table></div>
<p>Once those basics are covered, the kind of place is a matter of taste. Seaside towns suit people who want to swim, surf or walk by the water every day. Hot-spring towns suit a slower winter stay, though in our view you’ll find more inns than places with kitchens. Mountain and farming areas are the quietest, and we think they’re easiest if you’re happy to drive.</p>
<p>If you’d like a concrete example, the seaside towns of [[l:izu|the Izu Peninsula]] are about two and a half hours from Tokyo by direct train [[s:jre_tt_tokyo]]. Our [[l:shimoda-guide|Shimoda guide]] shows what daily life in one of those towns looks like.</p>

<h2>Do you need a car in rural Japan?</h2>
<p>Not if you choose your base well, but a car does widen what you can reach. Without one, you’ll live by the bus timetable, and that’s fine once you know how it works.</p>
<p>Local buses are under pressure. About 15,800 km of local bus routes were cut across Japan over nine years up to 2024, largely because of driver shortages and shrinking towns [[s:mlit_transport_wp2026]]. On a quiet route, the last bus can shape your evening more than any restaurant does.</p>
<p>Outside the main cities, some buses charge by distance, and the routine is simple once you’ve done it once [[s:jnto_buses]]:</p>
<ol>
<li>Get on by the centre door and take a small numbered ticket.</li>
<li>Watch the screen at the front, which shows the fare for your ticket number.</li>
<li>When you reach your stop, put the exact fare in the box by the driver and get off at the front.</li>
</ol>
<p>Your IC card may not work on these buses, so it’s worth carrying some cash [[s:jnto_buses]]. Buses are also where visitors to regional areas most often have trouble getting around, mostly with finding the right route and stop [[s:jta_visitor_survey_2025]]. We’d ask your host to show you the stop on your first day.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Getting around</th><th>Good for</th><th>Worth knowing</th></tr></thead>
<tbody>
<tr><td><strong>Local bus</strong></td><td>Station, town centre and beach</td><td>Some routes run rarely, and IC cards may not work [[s:jnto_buses]]</td></tr>
<tr><td><strong>Community bus or on-demand shared taxi</strong></td><td>Places the regular buses don’t reach</td><td>On-demand ones run when someone books, not to a timetable [[s:mlit_pri_demand]]</td></tr>
<tr><td><strong>Taxi</strong></td><td>Late evenings and heavy shopping</td><td>It’s handy to save a local number</td></tr>
<tr><td><strong>Bicycle</strong></td><td>Daily shopping and short trips</td><td>Hills, rain and summer heat</td></tr>
<tr><td><strong>Hire car</strong></td><td>Farms, mountains and day trips</td><td>You’ll need the right permit (below)</td></tr>
</tbody></table></div>
<p>Some towns run a community bus or an on-demand shared taxi (<em>demand kōtsū</em>) to fill gaps in the network [[s:mlit_pri_demand]]. Some are aimed at residents, so it’s worth asking at the town office or tourist information centre whether you can ride.</p>
<p>If you’d like to drive, Japan only accepts an international driving permit issued under the 1949 Geneva Convention, not the 1968 Vienna one [[s:mpd_idp_en]]. You can drive on it for up to a year from the day you arrive, or until it expires, whichever comes first [[s:kyoto_police_driving]]. A few places, including France, Germany and Switzerland, use a different route: your own licence plus an approved Japanese translation [[s:mpd_foreign_licence_en]]. For Izu in particular, our guide to [[l:izu-from-tokyo|getting to Izu from Tokyo]] covers the trains and how far you’ll get without a car.</p>

<h2>Where can you stay in the countryside for a week or more?</h2>
<p>For a week or more, a whole flat or house with a kitchen and a washing machine is usually the easiest choice. In the countryside, that often means a holiday rental (<em>minpaku</em>).</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Where to stay</th><th>Suits</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Holiday rental</strong> (<em>minpaku</em>)</td><td>A week to a month</td><td>A room or a whole house, sometimes an old traditional one (<em>kominka</em>) [[s:jnto_homestay]]</td></tr>
<tr><td><strong>Farm stay</strong> (<em>nouhaku</em>)</td><td>A few nights, to see rural life</td><td>A rural stay with farming, forestry or fishing [[s:jnto_homestay]]; about 700 areas take part [[s:maff_nouhaku_status]]</td></tr>
<tr><td><strong>Ryokan</strong> (traditional inn)</td><td>A few nights, as a treat</td><td>Dinner and breakfast are usually included [[s:jnto_ryokan]]</td></tr>
<tr><td><strong>Minshuku</strong> (family-run inn)</td><td>A few nights</td><td>B&amp;B-style rooms in the owner’s home, often with a shared bathroom [[s:jnto_minshuku]]</td></tr>
<tr><td><strong>Monthly apartment</strong></td><td>A month or more</td><td>A furnished flat on a short lease, and we find fewer in small towns</td></tr>
<tr><td><strong>Town trial home</strong> (<em>otameshi jutaku</em>)</td><td>People thinking of moving</td><td>Usually for would-be residents, not holidaymakers [[s:shizuoka_trial]]</td></tr>
</tbody></table></div>
<p>We think inns are lovely for a few nights but get expensive over a long stay, and you can’t cook for yourself. Town trial homes are another thing you’ll read about. Shizuoka City’s, for example, are for people living outside the prefecture who are thinking of moving and have spoken to its relocation advisers first [[s:shizuoka_trial]]. We look at them in [[l:akiya-try-first|trying out a town before you buy]].</p>
<p>To check that a rental is legal and know what to ask before you book a month, see our guide to [[l:monthly-rental|renting a place by the month]]. Here’s the checklist applied to our own place. <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a> is a renovated flat of about 40 m² in Shimoda’s old town, eight minutes’ walk from the station [[s:node_room,node_access]]. There’s a convenience store two minutes away and a supermarket three [[s:node_access]], plus a kitchen, a washing machine and a gas dryer [[s:node_room]].</p>

<h2>How do shops, cash and rubbish work in a small town?</h2>
<p>Whether you can walk to the shops depends on the town, which is why a shop on foot is near the top of the base checklist. Once you’ve found one, the rest of daily life gets much easier.</p>
<p>Roadside stations (<em>michi-no-eki</em>) are worth knowing about. Japan had 1,234 of them as of September 2026 [[s:mlit_michinoeki_2026]], and they’re good places to buy fresh local produce [[s:jnto_michinoeki]]. We think many are easiest to reach by car, so we’d check for a bus stop before setting out without one.</p>
<p>Bring a card, but don’t rely on it alone. In a government survey of departing visitors in 2025, about one in ten had trouble paying by card, most often in restaurants [[s:jta_visitor_survey_2025]]. We’d keep some cash for small shops and the bus.</p>
<p>Rubbish is the part that surprises people. Each town sets its own sorting rules and collection days, so what you learn in one place won’t quite match the next [[s:egov_waste_act]]. Many holiday rentals are in residential streets, which is why JNTO asks guests to sort rubbish properly and keep the noise down [[s:jnto_homestay]]. Where we host, guests gather their rubbish indoors and our cleaning partner does the sorting, so it’s worth asking whether your host has a system like that.</p>
<p>When you arrive, it’s worth asking your host four things:</p>
<ol>
<li>How the rubbish is sorted, and which day each kind goes out.</li>
<li>Where the nearest supermarket and convenience store are, and when they close.</li>
<li>Where the bus stop is, and when the last bus leaves.</li>
<li>Where the nearest clinic and pharmacy are.</li>
</ol>

<h2>What if you get sick or need help in English?</h2>
<p>Help is only a phone call away, even in a small town. You can dial 119 for an ambulance, and there’s a 24-hour helpline in English for visitors.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>If you need</th><th>Who to contact</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>An ambulance or fire service</strong></td><td>119 [[s:fdma_ambulance_en]]</td><td>They’ll ask where you are and what’s wrong</td></tr>
<tr><td><strong>The police</strong></td><td>110 [[s:jnto_hotline]]</td><td>For crimes and accidents</td></tr>
<tr><td><strong>Help in English, day or night</strong></td><td>Japan Visitor Hotline: 050-3816-2787 [[s:jnto_hotline]]</td><td>Open all year, in English, Chinese and Korean</td></tr>
<tr><td><strong>Advice on whether to call an ambulance</strong></td><td>#7119 [[s:fdma_7119]]</td><td>Available in many areas, but not everywhere</td></tr>
<tr><td><strong>A doctor who speaks your language</strong></td><td>JNTO’s medical institution search [[s:jnto_medical]]</td><td>Filter by area and language, then confirm with the clinic</td></tr>
<tr><td><strong>Earthquake and weather alerts</strong></td><td>The Safety tips app [[s:jta_safety_tips]]</td><td>Free, with alerts in English</td></tr>
</tbody></table></div>
<p>The ambulance ride itself is free, but hospital treatment isn’t [[s:iwate_emergency_en]]. In a few places, such as Ibaraki Prefecture, some large hospitals add a fee if the case turns out not to be urgent [[s:ibaraki_ambulance_fee]]. We’d travel with insurance that covers medical costs, which takes most of the worry out of this.</p>
<p>How much English you’ll hear depends on the town, and in a small one it may not be much. Certified tourist information centres can help, and they’re graded by how much language support they offer [[s:jnto_tic,jnto_tic_cert]]. In our view, a translation app on your phone and a bit of patience go a long way.</p>

<h2>When is the best season for a longer countryside stay?</h2>
<p>We think spring and autumn are the easiest for most people, but the right season depends on what you want to do. The rainy season, typhoons and snow are the things that change daily life on a longer stay.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Season</th><th>What happens</th><th>What it means for a longer stay</th></tr></thead>
<tbody>
<tr><td><strong>Rainy season</strong></td><td>Usually early June to late July from Kyushu to Tohoku; May to June in Okinawa; Hokkaido has no official rainy season [[s:jma_baiu,jma_baiu_faq]]</td><td>Washing dries slowly, so a dryer is a real help</td></tr>
<tr><td><strong>Summer</strong></td><td>Beach season in seaside towns</td><td>Where we host, longer stays are more common in summer, so book early</td></tr>
<tr><td><strong>Typhoon season</strong></td><td>About 12 typhoons a year come close to Japan, most in August and September [[s:jma_typhoon_normals]]</td><td>Leave a little slack in your plans for a day or two indoors</td></tr>
<tr><td><strong>Winter</strong></td><td>About half of Japan’s land is officially heavy-snow country [[s:mlit_snow_areas]]</td><td>Snow can make a car essential, so check winter bus services and heating</td></tr>
</tbody></table></div>
<p>If you’d like warm sea and long days, summer by the coast is hard to beat, as long as you book ahead. If you’d like snow, pick a town with a station and shops on foot, so the weather doesn’t trap you. And if you just want a calm, comfortable few weeks, spring or autumn is the safest bet.</p>
""",
 "faq": [
   ("Can you visit the Japanese countryside without a car?",
    "Yes, if you pick a base with a station, shops on foot and a bus service. Some rural buses charge by distance and may not take IC cards, so carry some cash [[s:jnto_buses]]. A car widens what you can reach, but you’ll need a 1949 Geneva Convention permit or an approved licence translation [[s:mpd_idp_en,mpd_foreign_licence_en]]."),
   ("Where should you stay in rural Japan for a week?",
    "We’d choose a whole flat or house with a kitchen and a washing machine, often a holiday rental (minpaku). Ryokan and minshuku suit a few nights better, and town trial homes are usually for people planning to move [[s:shizuoka_trial]]."),
   ("Do people speak English in rural Japan?",
    "It depends on the town, and in small ones it may not be much. The Japan Visitor Hotline helps in English 24 hours a day [[s:jnto_hotline]], and certified tourist information centres are graded by their language support [[s:jnto_tic_cert]]. A translation app helps too."),
   ("How does rubbish sorting work in rural Japan?",
    "Each town sets its own sorting rules and collection days [[s:egov_waste_act]], so ask your host on the first day. Some hosts gather and sort the rubbish for you."),
   ("What is the best time of year to visit the Japanese countryside?",
    "We think spring and autumn are the easiest. The rainy season runs from about early June to late July in most of Japan [[s:jma_baiu]], typhoons peak in August and September [[s:jma_typhoon_normals]], and about half the country gets heavy snow [[s:mlit_snow_areas]]."),
 ],
 "sources": ["soumu_kaso_r6", "jta_lodging_2025", "jnto_tic", "jnto_medical", "jre_tt_tokyo", "mlit_transport_wp2026", "jnto_buses", "jta_visitor_survey_2025",
             "mlit_pri_demand", "mpd_idp_en", "kyoto_police_driving", "mpd_foreign_licence_en", "jnto_homestay", "maff_nouhaku_status", "jnto_ryokan",
             "jnto_minshuku", "shizuoka_trial", "node_room", "node_access", "mlit_michinoeki_2026", "jnto_michinoeki", "egov_waste_act",
             "fdma_ambulance_en", "jnto_hotline", "fdma_7119", "jta_safety_tips", "iwate_emergency_en", "ibaraki_ambulance_fee", "jnto_tic_cert",
             "jma_baiu", "jma_baiu_faq", "jma_typhoon_normals", "mlit_snow_areas"],
 "related": ["shimoda-guide", "monthly-rental", "izu-from-tokyo"],
 "ja": {
  "h1": "日本の田舎に長く滞在する：拠点の選び方、移動、毎日の暮らし",
  "dek": "車がなくても、日本語があまりできなくても、日本の田舎で何週間も過ごせます。いちばん大事なのは拠点です。駅があり、歩いて行ける店があり、走っているバスがある町を選びます。",
  "review": [
   "【2026-11-21 新規（執筆部）】書いた点: ①1記事1主張は「田舎で長く過ごせるかは、地域の景色より拠点の選び方で決まる。駅・歩いて行ける店・時刻を確かめられるバスがある町なら、車がなくても日本語ができなくても数日〜数週間を暮らすように過ごせる」 ②h2 は構成案どおり7つ（長い滞在はどんなものか／拠点の選び方の表／車は要るか（バスの乗り方の番号つきリスト・移動手段の表・国際運転免許）／泊まる場所の表／店・現金・ごみ（着いた日に聞く4つ）／病気・英語（連絡先の表）／季節の表）、FAQ 5問 ③事実はリサーチメモで「開いた」と確認した公的な出典だけで書きました。名所の並べ立てにはせず、場所の性格（海沿い・温泉町・山や農村）は「どんな人に合うか」だけを1段落で書きました ④3-1 の6に合わせ、統計の数字は1段落に2つまで、気象の数字は季節の表に入れました。窓口は普通の言葉が先で、正式名（Japan Visitor Hotline など）は表の中だけにしました",
   "【書かなかったこと（リサーチメモ・編集長の指示どおり）】キャッシュレスの割合、VoiceTra などのアプリ名、乗合タクシーを走らせる市町村の全国の数、検索数、運転免許のエストニア、#7119 が英語で使えるか。救急車は「完全に無料」とは書かず「救急車で運ばれること自体は無料、病院の治療は有料。茨城県など、緊急でなかったときに一部の大病院が費用を取る地域がある」と書きました。「旅館・民宿は長くいると割高」は「私たちは思う」の見解にしています。お試し住宅の出典は shizuoka_trial だけです（minamialps_trial は使っていません）",
   "【既存記事との分け方】伊豆の運賃・時刻・JR Pass、下田の店・浜・津波、合法な民泊の見分け方と1か月の契約、お試し住宅の条件の詳細、ビザ・回線の数字は書かず、how-long-stay・digital-nomad・izu・shimoda-guide・izu-from-tokyo・monthly-rental・akiya-try-first へリンクで送りました。伊豆の例は「東京から直通の電車で約2時間半」の1文だけです（既存の出典 jre_tt_tokyo、2026年11月の時刻表）",
   "【自社の体験（experience.md の人が確認済みの節だけ）】①ゲストは欧米からの長期滞在が中心、リモートワークやサーフィン目的の人も（2026-10-11 回答・3-2） ②ごみは室内にまとめてもらい、清掃パートナーが分別（3-2） ③夏は長期滞在が多め（2026-10-11 回答）。ゲストから聞かれる質問の多さなど、体験にない言い方はしていません",
   "【NODE Shimoda に触れるのは泊まる場所の節の最後の1回】公式サイトの客室・アクセスのページ（2026-11-21 に確認）の事実だけ: 旧町内のアパートの一室を改装した約40㎡・駅から徒歩8分・コンビニ徒歩2分・スーパー徒歩3分・キッチン・洗濯機・ガス乾燥機。“house” とは呼ばず “flat” です。料金・割引・最低泊数は書いていません",
   "【人に確かめてほしい点】①冒頭の「ゲストのほとんどが欧米から来て、しばらく滞在する」は experience.md の「欧米からの長期滞在が中心」の言い換えです ②見出し写真が未定です（執筆部の環境に Unsplash がなく、仮の名前 rural-village-fields と仮の alt。エンジニア部が構成案7章の絵で選び、PHOTO_CREDIT_NEW と alt を直します） ③変わりやすい数字（playbook 6章）: 道の駅 1,234（2026年9月）、農泊の地域 約700（2025年度）、Japan Visitor Hotline の番号、#7119、バス路線の廃止 約15,800km（2016〜2024年度）、外国人の宿泊の3分の2が大都市圏（2025年） ④法律・制度の記述: 国際運転免許（1949年ジュネーブ条約・入国から1年まで・6つの国と地域は翻訳文）、ごみの分別は市町村が決める（廃棄物処理法6条）、救急車の費用 ⑤リサーチメモでは過疎地域の面積が 63.1% と 63.2% で1点違うため「約60%」と丸めました"
  ],
  "points": [
    "地域より先に拠点を選びます。駅があり、歩いて行けるスーパーがあり、時刻を確かめられるバスがある町です。",
    "田舎のバスは本数が少ないことがあり、IC カードが使えないこともあるので、最終バスに合わせて1日を組みます。",
    "ごみの決まり、店の閉まる時間、雪や台風の季節は町ごとに違うので、着いた日に聞いておきます。",
  ],
  "body": """
<p>日本の田舎のガイドの多くは、きれいな村の一覧で、1〜2泊の旅のために書かれています。1週間以上いるとなると、問いが変わります。「どこがきれいか」より、「どこならしばらく暮らせるか」です。私たちはそれがいちばん大事な問いだと思うので、ここではそれに答えます。</p>

<h2>田舎に長くいるのは、実際どんな感じか</h2>
<p>ツアーよりゆっくりで、ふつうの毎日です。私たちは、そこがいいところだと思っています。荷ほどきは1回だけ。スーパーを見つけ、バスの来る時間を覚え、同じ浜やパン屋に何度も通ううちに、町の人が会釈してくれるようになります。</p>
<p>静かな場所は、たくさんあります。日本の国土の約60%は、国の決まりで「過疎地域」とされていますが、そこに住む人は10人に1人もいません[[s:soumu_kaso_r6]]。そして、そこまで足を延ばす旅行者は多くありません。2025年、外国人の宿泊のおよそ3分の2は、大都市とその周りでした[[s:jta_lodging_2025]]。</p>
<p>私たちが迎えるゲストの多くは欧米から来た人で、しばらく滞在していきます。リモートで仕事をする人もいれば、サーフィンをしに来る人もいます。そういう滞在では、どの名所よりも、どの町を選ぶかのほうがずっと大事です。何日いられるかはパスポートによるので、[[l:ja-how-long-stay|日本に何日いられるかのガイド]]で確かめてください。何か月も日本から仕事をしたいなら、[[l:ja-digital-nomad|日本のデジタルノマドビザ]]もあります。</p>

<h2>田舎の拠点は、どう選べばいいか</h2>
<p>景色ではなく、毎日の暮らしが回るかで選びます。歩いて行ける店のないきれいな谷は4日目にはきつくなり、駅のある地味な小さな町のほうが、何週間でも楽に過ごせたりします。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>確かめること</th><th>長くいると、なぜ大事か</th><th>どこで確かめるか</th></tr></thead>
<tbody>
<tr><td><strong>駅があるか</strong></td><td>日帰りの遠出も帰りの移動も、車に頼らずにすむ</td><td>鉄道会社の時刻表</td></tr>
<tr><td><strong>歩いて行けるスーパーかコンビニ</strong></td><td>ほとんど毎日、買い物と料理をする</td><td>地図で見て、ホストに聞く</td></tr>
<tr><td><strong>バスと、帰りの最終便</strong></td><td>夜、何時まで出かけていられるかが決まる</td><td>バス会社の時刻表か、観光案内所[[s:jnto_tic]]</td></tr>
<tr><td><strong>週・月単位で借りられる部屋</strong></td><td>景色より、台所と洗濯機のほうが大事になる</td><td>予約サイトの掲載を見て、ホストに聞く</td></tr>
<tr><td><strong>近くの診療所・病院</strong></td><td>とくに子ども連れなら安心につながる</td><td>日本政府観光局の医療機関の検索[[s:jnto_medical]]</td></tr>
<tr><td><strong>季節</strong></td><td>雪・台風・梅雨で、できることが変わる</td><td>このページの下の季節の表</td></tr>
</tbody></table></div>
<p>この基本がそろえば、どんな場所にするかは好みです。海沿いの町は、毎日泳ぎたい、サーフィンしたい、海辺を歩きたい人に向きます。温泉町はゆっくりした冬の滞在に向きますが、私たちの見方では、台所のある所より宿のほうが多くなります。山あいや農村はいちばん静かで、運転をいとわない人のほうが過ごしやすいと私たちは思います。</p>
<p>具体的な例を1つ挙げると、[[l:ja-izu|伊豆半島]]の海沿いの町は、東京から直通の電車で約2時間半です[[s:jre_tt_tokyo]]。そうした町の1つでの毎日がどんなものかは、[[l:ja-shimoda-guide|下田のガイド]]にまとめています。</p>

<h2>田舎で車は要るか</h2>
<p>拠点をうまく選べば要りません。ただ、車があれば行ける範囲は広がります。車がなければバスの時刻表に合わせて暮らすことになりますが、仕組みが分かれば大丈夫です。</p>
<p>地方のバスは厳しい状況にあります。2024年度までの9年間で、全国で約15,800kmの路線バスが廃止されました。おもな理由は運転手の不足と人口の減少です[[s:mlit_transport_wp2026]]。本数の少ない路線では、どのレストランよりも、最終バスのほうが夜の過ごし方を決めます。</p>
<p>大きな都市の外では、乗った距離で運賃が決まるバスがあり、1回乗れば流れはかんたんです[[s:jnto_buses]]。</p>
<ol>
<li>真ん中のドアから乗り、番号の書かれた小さな券（整理券）を取ります。</li>
<li>前の画面を見ます。自分の券の番号の運賃が出ています。</li>
<li>降りるバス停で、運転席の横の箱にちょうどの運賃を入れ、前のドアから降ります。</li>
</ol>
<p>こうしたバスでは IC カードが使えないことがあるので、現金を少し持っておくと安心です[[s:jnto_buses]]。地方を訪れた旅行者が移動で困った場面で、いちばん多いのもバスで、おもに路線やバス停を見つけることでした[[s:jta_visitor_survey_2025]]。着いた日に、ホストにバス停を教えてもらうといいと思います。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>移動の手段</th><th>向く使い方</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>路線バス</strong></td><td>駅・町の中心・浜のあいだ</td><td>本数の少ない路線があり、IC カードが使えないこともある[[s:jnto_buses]]</td></tr>
<tr><td><strong>コミュニティバス・予約制の乗合タクシー</strong></td><td>ふつうのバスが行かない所</td><td>予約制のものは、時刻表ではなく予約があったときに走る[[s:mlit_pri_demand]]</td></tr>
<tr><td><strong>タクシー</strong></td><td>夜遅い時間や、買い物の荷物が多いとき</td><td>地元のタクシー会社の番号を登録しておくと便利</td></tr>
<tr><td><strong>自転車</strong></td><td>毎日の買い物や近場</td><td>坂・雨・夏の暑さ</td></tr>
<tr><td><strong>レンタカー</strong></td><td>農村・山・日帰りの遠出</td><td>決まった免許証が要る（下に）</td></tr>
</tbody></table></div>
<p>路線の足りないところを埋めるために、、コミュニティバスや予約制の乗合タクシー（デマンド交通）を走らせている町もあります[[s:mlit_pri_demand]]。住民向けのものもあるので、乗れるかどうかは、役場か観光案内所に聞いてみてください。</p>
<p>運転するなら、日本で使える国際運転免許証は、1949年のジュネーブ条約にもとづくものだけで、1968年のウィーン条約のものは使えません[[s:mpd_idp_en]]。運転できるのは、日本に着いた日から1年まで、または免許証の期限まで、どちらか早いほうです[[s:kyoto_police_driving]]。フランス・ドイツ・スイスなど、いくつかの国と地域は別の方法で、自分の免許証と、認められた日本語の翻訳文で運転します[[s:mpd_foreign_licence_en]]。伊豆については、[[l:ja-izu-from-tokyo|東京から伊豆への行き方のガイド]]で、電車と、車なしでどこまで行けるかをまとめています。</p>

<h2>田舎で1週間以上泊まるなら、どこがいいか</h2>
<p>1週間以上なら、台所と洗濯機のある部屋や家をまるごと借りるのが、たいていいちばん楽です。田舎では、それは民泊（貸し部屋・貸家）であることが多くなります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>泊まり方</th><th>向く長さ</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>民泊</strong></td><td>1週間〜1か月</td><td>部屋か家をまるごと。古い日本家屋（古民家）のこともある[[s:jnto_homestay]]</td></tr>
<tr><td><strong>農泊</strong></td><td>数泊。田舎の暮らしを見たいとき</td><td>農業・林業・漁業にふれながら田舎に泊まる[[s:jnto_homestay]]。取り組む地域は約700[[s:maff_nouhaku_status]]</td></tr>
<tr><td><strong>旅館</strong></td><td>数泊。ごほうびに</td><td>夕食と朝食が付くのがふつう[[s:jnto_ryokan]]</td></tr>
<tr><td><strong>民宿</strong>（家族で営む宿）</td><td>数泊</td><td>宿の人の家の一部に泊まる、朝食付きの宿のような形。浴室は共用のことが多い[[s:jnto_minshuku]]</td></tr>
<tr><td><strong>マンスリーの部屋</strong></td><td>1か月以上</td><td>家具付きの部屋を短期の賃貸で借りる。小さな町では少ないと私たちは感じている</td></tr>
<tr><td><strong>自治体のお試し住宅</strong></td><td>移住を考えている人</td><td>たいていは移住を考える人向けで、旅行者向けではない[[s:shizuoka_trial]]</td></tr>
</tbody></table></div>
<p>旅館は数泊ならすてきですが、長くいると割高になり、自分で料理もできない、と私たちは思います。自治体のお試し住宅のことを目にすることもあるでしょう。たとえば静岡市のお試し住宅は、静岡県の外に住んでいて、移住を考えていて、先に市の移住の相談員と話した人が対象です[[s:shizuoka_trial]]。くわしくは[[l:ja-akiya-try-first|買う前にその町で暮らしてみる記事]]で取り上げています。</p>
<p>合法な貸し部屋かの見分け方と、1か月予約する前に聞くことは、[[l:ja-monthly-rental|1か月部屋を借りるガイド]]にまとめました。このチェックリストを、私たちの宿に当てはめてみます。「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、下田の旧町内にあるアパートの一室（約40㎡）を改装したもので、駅から歩いて8分です[[s:node_room,node_access]]。コンビニまで2分、スーパーまで3分で[[s:node_access]]、台所・洗濯機・ガス乾燥機があります[[s:node_room]]。</p>

<h2>小さな町の店・現金・ごみは、どうなっているか</h2>
<p>店まで歩いて行けるかどうかは町しだいなので、歩いて行ける店は、拠点のチェックリストの上のほうに入れています。1軒見つかれば、毎日の暮らしはずっと楽になります。</p>
<p>道の駅は知っておくと便利です。2026年9月の時点で全国に1,234あり[[s:mlit_michinoeki_2026]]、地元の新鮮な農産物などを買うのにいい場所です[[s:jnto_michinoeki]]。車で行きやすい所が多いと思うので、車なしで出かけるなら、私たちなら先にバス停があるかを確かめます。</p>
<p>カードは持っていきつつ、カードだけに頼らないほうがいいです。2025年に日本を出国する旅行者に国が聞いた調査では、約10人に1人がカードの支払いで困っていて、いちばん多い場所は飲食店でした[[s:jta_visitor_survey_2025]]。小さな店やバスのために、現金も少し持っておくと思います。</p>
<p>みんなが驚くのが、ごみです。分け方と収集日は町ごとに決めているので、ある町で覚えたやり方は、次の町ではそのまま通じません[[s:egov_waste_act]]。民泊の多くは住宅街にあるので、日本政府観光局も、ごみを正しく分けて出すこと、静かにすることを呼びかけています[[s:jnto_homestay]]。私たちの宿では、ゲストにごみを部屋の中にまとめてもらい、清掃のパートナーが分別しています。ホストにそういう仕組みがあるか、聞いてみるといいと思います。</p>
<p>着いたら、ホストに次の4つを聞いておくといいと思います。</p>
<ol>
<li>ごみの分け方と、それぞれ何曜日に出すか。</li>
<li>いちばん近いスーパーとコンビニの場所と、閉まる時間。</li>
<li>バス停の場所と、最終バスの時間。</li>
<li>いちばん近い診療所と薬局の場所。</li>
</ol>

<h2>具合が悪くなったら、英語で助けがほしいときは</h2>
<p>小さな町でも、電話1本で助けを呼べます。救急車は119、そして旅行者向けの、英語で24時間話せる電話窓口があります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>困ったこと</th><th>連絡先</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>救急車・火事</strong></td><td>119[[s:fdma_ambulance_en]]</td><td>場所と、どうしたかを聞かれる</td></tr>
<tr><td><strong>警察</strong></td><td>110[[s:jnto_hotline]]</td><td>事件や事故のとき</td></tr>
<tr><td><strong>英語で助けがほしい（昼も夜も）</strong></td><td>Japan Visitor Hotline：050-3816-2787[[s:jnto_hotline]]</td><td>一年中。英語・中国語・韓国語</td></tr>
<tr><td><strong>救急車を呼ぶべきか迷うとき</strong></td><td>#7119[[s:fdma_7119]]</td><td>多くの地域にあるが、全国どこでもではない</td></tr>
<tr><td><strong>自分の言葉が通じる医師</strong></td><td>日本政府観光局の医療機関の検索[[s:jnto_medical]]</td><td>地域と言語で絞り、病院にも確かめる</td></tr>
<tr><td><strong>地震や天気の警報</strong></td><td>Safety tips アプリ[[s:jta_safety_tips]]</td><td>無料。英語で警報が届く</td></tr>
</tbody></table></div>
<p>救急車で運ばれること自体は無料ですが、病院の治療にはお金がかかります[[s:iwate_emergency_en]]。茨城県など一部の地域では、緊急でなかったと判断されると、大きな病院の一部が費用を取ることがあります[[s:ibaraki_ambulance_fee]]。私たちなら医療費を補う旅行保険に入っておきます。そうすれば、この心配はほとんどなくなります。</p>
<p>英語がどれくらい通じるかは町しだいで、小さな町ではあまり通じないかもしれません。認定された観光案内所なら手伝ってもらえます。案内所は、外国語にどのくらい対応できるかで区分されています[[s:jnto_tic,jnto_tic_cert]]。私たちの見方では、スマホの翻訳アプリと、少しの気長さがあれば、たいていなんとかなります。</p>

<h2>田舎に長くいるなら、いつがいいか</h2>
<p>多くの人にとっていちばん楽なのは春と秋だと思いますが、何をしたいかで変わります。長くいるときの毎日を変えるのは、梅雨・台風・雪です。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>季節</th><th>何が起きるか</th><th>長くいると、どう変わるか</th></tr></thead>
<tbody>
<tr><td><strong>梅雨</strong></td><td>九州〜東北は、だいたい6月上旬〜7月下旬。沖縄は5〜6月。北海道には正式な梅雨がない[[s:jma_baiu,jma_baiu_faq]]</td><td>洗濯物が乾きにくいので、乾燥機があると本当に助かる</td></tr>
<tr><td><strong>夏</strong></td><td>海沿いの町は海水浴の季節</td><td>私たちの宿では、夏に長期滞在が多くなるので、早めの予約を</td></tr>
<tr><td><strong>台風の季節</strong></td><td>日本に近づく台風は年に約12個で、8月と9月がいちばん多い[[s:jma_typhoon_normals]]</td><td>1〜2日、家の中で過ごす日があってもいいよう、予定に余裕を</td></tr>
<tr><td><strong>冬</strong></td><td>日本の国土の約半分が、国の決まりで「豪雪地帯」[[s:mlit_snow_areas]]</td><td>雪で車が欠かせなくなることもあるので、冬のバスと暖房を確かめる</td></tr>
</tbody></table></div>
<p>温かい海と長い日が好きなら、早めに予約さえすれば、夏の海沿いはなかなかのものです。雪が好きなら、天気で身動きが取れなくならないよう、駅と歩いて行ける店のある町を選びます。とにかく穏やかに、快適に数週間を過ごしたいなら、春か秋がいちばん無難です。</p>
""",
  "faq": [
    ("日本の田舎には、車なしで行けますか",
     "行けます。駅があり、歩いて行ける店があり、バスが走っている拠点を選べば大丈夫です。乗った距離で運賃が決まる田舎のバスがあり、IC カードが使えないこともあるので、現金を持っておきます[[s:jnto_buses]]。車があれば行ける範囲は広がりますが、1949年のジュネーブ条約の国際運転免許証か、認められた翻訳文が要ります[[s:mpd_idp_en,mpd_foreign_licence_en]]。"),
    ("田舎で1週間泊まるなら、どこがいいですか",
     "私たちなら、台所と洗濯機のある部屋か家をまるごと借ります。多くは民泊です。旅館や民宿は数泊のほうが向き、自治体のお試し住宅は、たいてい移住を考える人向けです[[s:shizuoka_trial]]。"),
    ("日本の田舎で、英語は通じますか",
     "町によります。小さな町ではあまり通じないかもしれません。Japan Visitor Hotline なら24時間英語で相談でき[[s:jnto_hotline]]、認定された観光案内所は外国語の対応の程度で区分されています[[s:jnto_tic_cert]]。翻訳アプリも役に立ちます。"),
    ("田舎のごみの分け方は、どうなっていますか",
     "分け方と収集日は町ごとに決めているので[[s:egov_waste_act]]、着いた日にホストに聞きます。ホストがまとめて分別してくれるところもあります。"),
    ("日本の田舎に行くなら、いつがいいですか",
     "いちばん楽なのは春と秋だと思います。梅雨は日本の多くの地域でだいたい6月上旬〜7月下旬[[s:jma_baiu]]、台風は8月と9月が多く[[s:jma_typhoon_normals]]、国土の約半分は雪の多い地域です[[s:mlit_snow_areas]]。"),
  ],
 },
}
