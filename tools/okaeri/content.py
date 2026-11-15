# -*- coding: utf-8 -*-
"""Noki の記事・ページのデータ。HTML は直接書き換えず、ここを直して build.py を実行する。

本文で使える記法:
  [[s:キー,キー]]   出典を（リンク; リンク）の形で入れる
  [[a:キー]]        出典を文中リンクとして入れる（かっこなし）
  [[l:ページID|文字]] サイト内リンク（本番は実URL、試作は #ページID に変わる）
  [[img:名前|代替テキスト|説明]] 写真（photos/ の <名前>-1200.webp と -640.webp）
  [[ed:文章]]       公開前に運営者の一次情報で埋める箇所（残っていると seo_check が公開不可にする）
"""

# ---------------------------------------------------------------- 出典
# key: (URL, 英語の短い名前, 日本語の短い名前, 出典一覧に出す名前)
SOURCES = {
    "shimoda_news": ("https://www.city.shimoda.shizuoka.jp/file/広報しもだ平成28年6月号16頁.pdf",
                     "Shimoda City newsletter, June 2016", "広報しもだ 2016年6月号", "Shimoda City newsletter, June 2016"),
    "pref": ("https://www.pref.shizuoka.jp/sangyoshigoto/suisan/suisangyo/uocching/1003397/1043925/1028101.html",
             "Shizuoka Prefecture", "静岡県", "Shizuoka Prefecture: Ichiba no Shokudo Kinmetei"),
    "tabimag": ("https://tabi-mag.jp/kinmefes/", "Tabi-mag", "旅マガジン", "Tabi-mag: Shimoda Kinme Matsuri"),
    "tvtokyo": ("https://www.tv-tokyo.co.jp/adomachi/backnumber/20140315/100043.html",
                "TV Tokyo, 2014", "テレビ東京 2014年", "TV Tokyo, Ado-machi: Izu Shimoda (2014)"),
    "ekitan": ("https://ekitan.com/en/article/odoriko", "Ekitan", "駅探", "Ekitan: Limited Express Odoriko"),
    "rej": ("https://resources.realestate.co.jp/buy/what-restrictions-are-there-on-foreigners-buying-a-home-in-japan-compared-to-other-countries/",
            "Real Estate Japan", "Real Estate Japan", "Real Estate Japan: restrictions on foreign buyers"),
    "mofa": ("https://www.mofa.go.jp/j_info/visit/visa/short/novisa.html", "Ministry of Foreign Affairs of Japan", "外務省", "Ministry of Foreign Affairs of Japan: Exemption of Visa (Short-Term Stay)"),
    "jg6305": ("https://japan-guide.com/e/e6305.html", "japan-guide.com", "japan-guide.com", "japan-guide.com: Getting to Izu Peninsula"),
    "jg6311": ("https://japan-guide.com/e/e6311.html", "japan-guide.com", "japan-guide.com", "japan-guide.com: Shuzenji access"),
    "jg6322": ("https://japan-guide.com/e/e6322.html", "japan-guide.com", "japan-guide.com", "japan-guide.com: Izu beaches"),
    "jg6304": ("https://www.japan-guide.com/e/e6304.html", "japan-guide.com", "japan-guide.com", "japan-guide.com: Shirahama Beach"),
    "jnto": ("https://www.japan.travel/en/spot/1273/", "JNTO", "日本政府観光局", "JNTO: Shirahama Chuo Beach"),
    "funjapan": ("https://www.fun-japan.jp/en/articles/10632", "FUN! JAPAN", "FUN! JAPAN", "FUN! JAPAN: Shirahama Beach"),
    "uncharted": ("https://japanuncharted.com/shizuoka/onsen-town", "Japan Uncharted", "Japan Uncharted",
                  "Japan Uncharted: Shizuoka onsen towns"),
    "tdn": ("https://www.thedigitalnomad.asia/travel-tips/shimoda-for-digital-nomads/", "The Digital Nomad Asia",
            "The Digital Nomad Asia", "The Digital Nomad Asia: Shimoda for Digital Nomads"),
    "stat_housing2023": ("https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf", "Statistics Bureau of Japan", "総務省統計局",
                         "Statistics Bureau of Japan: 2023 Housing and Land Survey, final basic tabulation (2024)"),
    "isa_nomad_en": ("https://www.moj.go.jp/isa/applications/status/designatedactivities53_00001.html", "Immigration Services Agency",
                     "出入国在留管理庁", "Immigration Services Agency: Designated Activities (Digital Nomad)"),
    "isa_nomad_list": ("https://www.moj.go.jp/isa/content/001416932.pdf", "Immigration Services Agency", "出入国在留管理庁",
                       "Immigration Services Agency: Eligible countries and regions for the digital nomad status"),
    "mof_fefta2026": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/recent_revised/gaitamehou_20260220.html",
                      "Ministry of Finance", "財務省", "Ministry of Finance: Revision of reporting rules under the Foreign Exchange Act (20 February 2026)"),
    "mof_realprop_faq": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/real_property/FAQ_J.pdf", "Ministry of Finance",
                         "財務省", "Ministry of Finance: FAQ on reports of real property acquisition (June 2026)"),
    "moj_nationality": ("https://www.moj.go.jp/content/001470076.pdf", "Ministry of Justice", "法務省",
                        "Ministry of Justice: Notice on recording nationality in property registration (4 September 2026)"),
    "cao_land_bill": ("https://www.cao.go.jp/houan/222/index.html", "Cabinet Office", "内閣府", "Cabinet Office: Bills submitted to the 222nd Diet session"),
    "minamialps_trial": ("https://www.city.minami-alps.yamanashi.jp/docs/12876.html", "Minami-Alps City", "南アルプス市",
                         "Minami-Alps City: Trial homes for people considering a move"),
    "shizuoka_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000050.html", "Shizuoka City", "静岡市",
                       "Shizuoka City: Trial homes for people considering a move"),
    "cao_land_bill_outline": ("https://www.cao.go.jp/houan/pdf/222/222_1gaiyou.pdf", "Cabinet Office (bill outline)", "内閣府（法案の概要）",
                              "Cabinet Office: Outline of the bill to amend the Act on the Review and Regulation of the Use of Real Estate around Important Facilities and on Remote Territorial Islands (2026)"),
    "shizuoka_long_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000158.html", "Shizuoka City (long-term)", "静岡市（長期）",
                            "Shizuoka City: Long-term trial homes for people moving to the city"),
    "jre_tt_tokyo": ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetable, Tokyo Station", "JR東日本 東京駅の時刻表",
                     "JR East, Tokyo Station timetable (November 2026)"),
}

# ---------------------------------------------------------------- 記事のテーマ
# テーマ別の一覧ページ（/noki/akiya.html など）は、公開記事が3本以上になったテーマだけ自動で作る（薄い一覧を作らないため）
# 読み手の入口は「どこまで日本に深く関わるか」の1本の軸で分ける（重ならず、漏れない）:
#   stay = 旅行者として1週間〜1か月滞在する ／ live = 一年の一部を暮らす（数か月・毎年・仕事をしながら）／ own = 家を持つ（空き家を買う・直す・運営する）
# 記事は必ずこの3つのどれか1つ（"topic"）に入れる。ほかの段階の読み手にも役立つ記事は "also" に足す（一覧の「こちらも役立つ」に出る）。
# kanji は入口の印（漢字一文字）。季節の色は site.css の .t-<キー>（春=旅・夏=暮らし・秋=家・冬=場所）。
# 場所（places）は別の軸。記事に "place" があれば場所の一覧にも出る。
TOPICS = {
    "stay": {"kind": "plan", "name": "Stay longer", "ja": "長めに旅する", "kanji": "旅", "photo": "window-room",
             "photo_alt": "Two low chairs and a small table by a window with paper screens, looking out over water",
             "path_label": "A longer trip", "path_desc": "A week to a month as a visitor: towns, food, getting there.",
             "path_ja": "長めの旅（旅行者として1週間〜1か月）",
             "seo_title": "Slow Travel in Small-Town Japan: Week- and Month-Long Trips",
             "description": "Guides for travellers who want a week or a month in one small Japanese town instead of a different city every night: access, seasons, food and where to stay.",
             "intro": "For a week or a month as a visitor. One town instead of a different hotel every night: how to get there, when to go, what to eat and how a house changes the trip.",
             "coming": ["Shimoda for a week or longer", "The Japanese countryside for a longer stay"]},
    "live": {"kind": "plan", "name": "Live part-time", "ja": "一年の一部を暮らす", "kanji": "暮", "photo": "town-lane",
             "photo_alt": "Quiet paved lane between hedges and low houses, with green hills behind",
             "path_label": "Living here part of the year", "path_desc": "Months at a time, or every year: remote work, visas, monthly homes.",
             "path_ja": "一年の一部を暮らす（数か月・毎年・仕事をしながら）",
             "seo_title": "Living in Japan Part-Time: Long Stays, Visas, Remote Work",
             "description": "How to live in small-town Japan for months at a time or every year: how long you can stay, Japan’s digital nomad visa, monthly homes and working remotely.",
             "intro": "For months at a time, or a season every year. How long you can stay, Japan’s digital nomad visa, renting a home by the month and working remotely from a small town.",
             "coming": ["Renting a house in Japan for a month", "Japan’s digital nomad visa, and where to base yourself", "How long can you stay in Japan?"]},
    "own": {"kind": "plan", "name": "Own a home", "ja": "家を持つ", "kanji": "家", "photo": "empty-tatami-room",
            "photo_alt": "Empty tatami room in an old wooden house, with sliding windows open to a garden",
            "path_label": "Owning a home here", "path_desc": "Buying, restoring or running an akiya.",
            "path_ja": "家を持つ（空き家を買う・直す・運営する）",
            "seo_title": "Akiya in Japan: Buying, Restoring and Owning an Old House",
            "description": "Plain guides to owning an akiya, one of Japan’s vacant houses: who can buy one, what it really costs, restoring it and testing the town before you commit.",
            "intro": "Japan has about nine million empty homes, and foreigners can buy them. The listings are the easy part. These guides cover what an akiya really costs, what owning one does and does not give you, and how to try a town before you sign.",
            "coming": ["Can foreigners buy property in Japan?", "What is an akiya?", "Cheap and free houses in Japan: the real cost", "Akiya banks explained"]},
    "places": {"kind": "place", "name": "Places", "ja": "場所", "kanji": "地", "photo": "rocky-coast",
               "photo_alt": "Waves breaking against dark volcanic cliffs on a rocky coastline",
               "seo_title": "Small-Town Japan: Place Guides for Longer Stays",
               "description": "Guides to the towns where we run homes and the regions around them, starting with the Izu Peninsula, written for people staying a week or longer.",
               "intro": "We write about the places where we run homes, starting with the Izu Peninsula south-west of Tokyo.",
               "coming": []},
}
PLANS = [k for k, v in TOPICS.items() if v["kind"] == "plan"]

TRAIN_TABLE_EN = """
<div class="tablewrap"><table>
<thead><tr><th>From Tokyo to</th><th>Route</th><th>Time</th><th>One-way fare</th></tr></thead>
<tbody>
<tr><td>Atami</td><td>Odoriko limited express</td><td>about 80 min</td><td>about ¥3,500</td></tr>
<tr><td>Ito</td><td>Odoriko limited express</td><td>about 100 min</td><td>about ¥4,000</td></tr>
<tr><td>Shimoda</td><td>Odoriko limited express, direct</td><td>about 2 h 35 min</td><td>¥6,660 reserved seat</td></tr>
<tr><td>Shuzenji</td><td>Odoriko limited express, direct</td><td>about 2 h</td><td>about ¥4,500</td></tr>
</tbody></table></div>
"""
TRAIN_TABLE_JA = """
<div class="tablewrap"><table>
<thead><tr><th>東京から</th><th>行き方</th><th>所要時間</th><th>片道運賃</th></tr></thead>
<tbody>
<tr><td>熱海</td><td>特急「踊り子」</td><td>約80分</td><td>約3,500円</td></tr>
<tr><td>伊東</td><td>特急「踊り子」</td><td>約100分</td><td>約4,000円</td></tr>
<tr><td>下田</td><td>特急「踊り子」直通</td><td>約2時間35分</td><td>6,660円（指定席）</td></tr>
<tr><td>修善寺</td><td>特急「踊り子」直通</td><td>約2時間</td><td>約4,500円</td></tr>
</tbody></table></div>
"""

# ---------------------------------------------------------------- 記事
ARTICLES = [
# ============================================================ 金目鯛
{
 "id": "kinmedai", "slug": "kinmedai", "topic": "stay", "place": "izu", "also": [],
 "photo": ("grilled-red-fish", "A whole grilled red fish with rice, soup and small side dishes on a wooden table", ""),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Food and port towns",
 "h1": "Kinmedai: Japan’s golden-eye snapper and where to eat it",
 "seo_title": "Kinmedai: Japan’s Golden-Eye Snapper and Where to Eat It",
 "description": "Kinmedai is a red, golden-eyed deep-sea fish eaten simmered, seared or raw. What it is, when to eat it and why Shimoda is the port to try it in.",
 "dek": "Kinmedai is the red, golden-eyed fish you’ll find on sushi counters and ryokan tables all over Japan. Here’s what it is, how it’s eaten, and why the port of Shimoda is the place to try it.",
 "card": "What kinmedai is, how Japan cooks it, its two seasons and why Shimoda, which calls itself Japan’s top kinmedai port, is worth a night.",
 "keywords": [("kinmedai", "4,400", "0")],
 "intent": "Know（知りたい）",
 "points": [
   "Kinmedai is a deep-sea fish with red skin and big golden eyes. In English it’s sold as splendid alfonsino or golden-eye snapper.",
   "Shimoda, at the southern tip of the Izu Peninsula, is Japan’s top landing port for it, according to a 2016 city newsletter and Shizuoka Prefecture.",
   "The classic dish is nitsuke, fish simmered in soy sauce and sugar, and there’s a canteen inside the fish market that opens at 7:00.",
   "It has two seasons: winter, and June, when it’s said to be at its fattiest and the town holds its kinmedai festival.",
 ],
 "body": """
<h2>What is kinmedai?</h2>
<p>Kinmedai is a deep-sea fish with red skin and big golden eyes, known in English as splendid alfonsino (<em>Beryx splendens</em>) or golden-eye snapper. It lives in deep water, several hundred metres down [[s:tabimag]]. Shimoda’s city newsletter describes eyes that shine gold and skin that turns red all over about 40 minutes after the fish is landed [[s:shimoda_news]].</p>
<p>The name is written 金目鯛, which literally means “golden-eye sea bream”, but it isn’t a sea bream or a snapper. The flesh is white and stays rich with fat all year, which is why it works so well simmered, raw or seared.</p>

<h2>Why is Shimoda the place to eat kinmedai?</h2>
<p>Shimoda, at the southern tip of the [[l:izu|Izu Peninsula]], describes itself as Japan’s top landing port for kinmedai. The city said so in its June 2016 newsletter, and Shizuoka Prefecture describes the port the same way [[s:shimoda_news,pref]].</p>
<p>You’ll often see two names on menus in town. <em>Jikinme</em> is caught in nearby waters, between Oshima and Kozushima, while <em>oki-kinme</em> comes from fishing grounds further out [[s:tvtokyo]]. Ordering both side by side is the quickest way to taste the difference.</p>

<h2>How is kinmedai eaten?</h2>
<p>Most people come for nitsuke, but it’s worth trying it more than one way.</p>
<div class="tablewrap"><table>
<thead><tr><th>Dish</th><th>What it is</th></tr></thead>
<tbody>
<tr><td><strong>Nitsuke</strong></td><td>A whole fish or a thick cut simmered in soy sauce and sugar. This is the one most people come for.</td></tr>
<tr><td><strong>Sashimi and aburi</strong></td><td>Raw slices, or slices with the skin lightly seared.</td></tr>
<tr><td><strong>Shabu-shabu</strong></td><td>Thin slices swished through hot broth at the table.</td></tr>
<tr><td><strong>Everything else</strong></td><td>Ramen, burgers and croquettes, listed by the Japanese travel magazine Tabi-mag [[s:tabimag]].</td></tr>
</tbody></table></div>

<h2>Where can you try kinmedai by the harbour?</h2>
<p>Ichiba no Shokudo Kinmetei is a canteen inside the Shimoda fish market, about ten minutes on foot from Izukyu-Shimoda Station. Shizuoka Prefecture lists its hours as 7:00 to 9:30 for the morning set and 11:00 to 15:00 for lunch, closed on Tuesdays ([[a:pref]], page updated March 2025). Hours do change, so it’s worth checking before you walk over.</p>
[[ed:Add the two or three places we actually send guests, with walking time from the house and what we order there.]]

<h2>When is the best time to eat kinmedai?</h2>
<p>There are two answers, and if you’d like to see the boats come in, June is the month to plan around.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Winter</td><td>Often named as the kinmedai season.</td></tr>
<tr><td>June</td><td>Just before spawning, when the fish is said to be at its fattiest [[s:shimoda_news]].</td></tr>
<tr><td>June festival</td><td>Tabi-mag lists the Shimoda Kinme Matsuri as running from 1 to 30 June, with landings visible from a viewing area beside the market from about 7:30 to 9:00. Boats don’t go out on Tuesdays or Saturdays, or after rough seas [[s:tabimag]].</td></tr>
</tbody></table></div>
<p>Festival dates and viewing times are set each year, so check them for the year you travel.</p>

<h2>Why stay overnight instead of visiting for the day?</h2>
<p>The market does its business early, and the direct Odoriko limited express from Tokyo takes about 2 hours 35 minutes [[s:ekitan]]. Come for the day and you’ll arrive after the boats have unloaded. Stay in town and you can watch the morning landings at the harbour and be at the canteen when it opens. Routes and fares are in our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]].</p>
<p>Our home in Shimoda’s old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is about ten minutes on foot from the station. It has a properly equipped kitchen and a supermarket within walking distance, so you can cook whatever you find.</p>
[[ed:Name where guests can buy kinmedai to cook at home.]]
""",
 "faq": [
   ("Is kinmedai the same as red snapper?",
    "No. Kinmedai is an alfonsino, a different family from the snappers. “Golden-eye snapper” is just a market name."),
   ("What does kinmedai taste like?",
    "It has white flesh that stays rich with fat all year, so it’s good simmered, seared or raw. The classic way to eat it is nitsuke, simmered in soy sauce and sugar."),
   ("Where is kinmedai caught?",
    "Shimoda, on the Izu Peninsula in Shizuoka Prefecture, is described by the city and the prefecture as Japan’s top landing port for kinmedai. The fish sold there as jikinme is caught in nearby waters between Oshima and Kozushima."),
   ("How do you say kinmedai?",
    "Roughly “kin-meh-dye”. Locals often shorten it to <em>kinme</em>."),
 ],
 "sources": ["shimoda_news", "pref", "tabimag", "tvtokyo", "ekitan"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "金目鯛とは：日本の「ゴールデンアイ・スナッパー」と、食べられる場所",
  "dek": "金目鯛は、日本中の寿司屋や旅館で出会う、赤い皮と金色の目の魚です。どんな魚か、どう食べるか、そしてなぜ下田の港で食べるのがいいのかをまとめました。",
  "review": [
   "【2026-11-15 トーンの書き直し】現地に住む友人が話すような文にしました（英語は短縮形と you を使い、表の前に一言添える形に）。日本語版も自然な話し言葉寄りにしました。数字・出典・主張は変えていません",
   "【2026-11-15 の見直しで変えた点（見せ方）】食べ方と旬を表にしました。本文から伊豆半島のページへのリンクを1本足しました。狙う検索語から「shimoda japan」を外しました（これから書く下田ガイドの記事と重ならないように）。「In short」の4点目を「旬は冬と6月の2つ」と答えが分かる形にしました",
   "【変えた点（言い方を出典の範囲に弱めた。事実は足していない）】「下田は水揚げが日本一の港」→「下田市（2016年の広報）と静岡県が、日本一の水揚げ港と説明している」。最新の全国統計で確かめられていないためです。生息する深さ「500メートル前後」→「数百メートル」。「観光協会が挙げている」→出典の実際の名前（旅のメディア「旅マガジン」）に。祭りの期間・見学時間は「旅マガジンの記載で、年ごとに決まる」と添えました",
   "【人に確かめてほしい点】①金目鯛の説明や食べ方に、地元の感覚とずれている点がないか ②紹介している店（市場の食堂 金目亭）を載せてよいか。ほかに必ず案内している店があるか（黄色い枠） ③ゲストが金目鯛を買える店（黄色い枠） ④見出しの写真は「焼いた赤い魚」で、定番の煮付けとずれます。煮付けか水揚げの自社撮影の写真があると、ずっと良くなります",
   "【まだ入れていないこと（出典の確認待ち）】値段の目安と高い理由、のどぐろとの違い、妊娠中の魚の食べ方の公的な目安（厚生労働省）、東京からの所要時間の2026年3月改定後の値。リサーチ部が確かめてから足します",
  ],
  "points": [
    "金目鯛は、赤い皮と大きな金色の目をした深海魚。英語では splendid alfonsino や golden-eye snapper の名前で売られています。",
    "伊豆半島の南端にある下田は、金目鯛の水揚げが日本一の港です（2016年の下田市の広報と静岡県の説明による）。",
    "定番は、醤油と砂糖で煮る煮付け。魚市場の中には、朝7時に開く食堂があります。",
    "旬は2つ。冬と、いちばん脂が乗るとされ、町で金目鯛の祭りが開かれる6月です。",
  ],
  "body": """
<h2>金目鯛とはどんな魚か</h2>
<p>金目鯛は、赤い皮と大きな金色の目をした深海魚です。英語では splendid alfonsino（学名 <em>Beryx splendens</em>）や golden-eye snapper と呼ばれます。水深数百メートルの深い海にすんでいます[[s:tabimag]]。下田市の広報によると、目は金色に輝き、水揚げから40分ほどで全身が赤くなるそうです[[s:shimoda_news]]。</p>
<p>「金目鯛」と書きますが、実は鯛の仲間でもスナッパー（フエダイ）の仲間でもありません。身は白身で、一年中脂がのっているので、煮ても、生でも、炙ってもおいしく食べられます。</p>

<h2>なぜ下田で食べるのがいいのか</h2>
<p>[[l:izu|伊豆半島]]の南端にある下田は、金目鯛の水揚げ日本一の港だと説明しています。下田市が2016年6月号の広報でそう書いていて、静岡県も同じように紹介しています[[s:shimoda_news,pref]]。</p>
<p>町のメニューでは、2つの名前をよく見かけます。「地金目」は大島から神津島にかけての近海でとれたもの、「沖金目」は遠くの漁場でとれたものです[[s:tvtokyo]]。両方を並べて頼むと、違いがすぐに分かります。</p>

<h2>金目鯛はどうやって食べるのか</h2>
<p>お目当ては煮付けという人が多いですが、いくつかの食べ方を試してみるのがおすすめです。</p>
<div class="tablewrap"><table>
<thead><tr><th>料理</th><th>どんなものか</th></tr></thead>
<tbody>
<tr><td><strong>煮付け</strong></td><td>丸ごと、または厚い切り身を醤油と砂糖で煮たもの。多くの人のお目当てです。</td></tr>
<tr><td><strong>刺身と炙り</strong></td><td>生の切り身や、皮目をさっと炙った切り身です。</td></tr>
<tr><td><strong>しゃぶしゃぶ</strong></td><td>薄切りを、卓上の熱い出汁にくぐらせて食べます。</td></tr>
<tr><td><strong>そのほか</strong></td><td>旅のメディア「旅マガジン」は、金目鯛のラーメン、バーガー、コロッケも紹介しています[[s:tabimag]]。</td></tr>
</tbody></table></div>

<h2>港の近くで食べられる店</h2>
<p>「市場の食堂 金目亭」は、下田市魚市場の中にある食堂で、伊豆急下田駅から歩いて約10分です。静岡県のページによると、朝定食が7時〜9時30分、昼が11時〜15時で、火曜が定休日です（[[a:pref]]、2025年3月更新）。営業時間は変わることがあるので、出かける前に確かめておくと安心です。</p>
[[ed:実際にゲストへ案内している店を2〜3軒、家からの徒歩時間と、そこで頼むものを添えて入れてください。]]

<h2>いつ食べに行くのがいいか</h2>
<p>答えは2つあります。船が港に入ってくるところを見たいなら、6月に合わせるのがおすすめです。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>理由</th></tr></thead>
<tbody>
<tr><td>冬</td><td>金目鯛の旬として、よく挙げられます。</td></tr>
<tr><td>6月</td><td>産卵前で、いちばん脂が乗る時期とも言われます[[s:shimoda_news]]。</td></tr>
<tr><td>6月の祭り</td><td>旅マガジンによると、「下田きんめ祭り」は6月1日から30日まで。市場の横の見学エリアから、7時30分から9時ごろまで水揚げを見られます。火曜と土曜、しけの後は漁が休みです[[s:tabimag]]。</td></tr>
</tbody></table></div>
<p>祭りの期間や見学の時間は年ごとに決まるので、行く年の情報を確かめてください。</p>

<h2>日帰りではなく、泊まったほうがいい理由</h2>
<p>市場は朝早くに動きます。東京からの直通特急「踊り子」でも約2時間35分かかるので[[s:ekitan]]、日帰りだと、着くころには水揚げが終わっています。町に泊まれば、朝の水揚げを港で見て、開店と同時に食堂に入れます。行き方と運賃は、[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田の旧町内にある私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、駅から歩いて約10分。調理器具のそろったキッチンがあり、スーパーも歩いて行けるので、見つけた魚を自分で料理できます。</p>
[[ed:ゲストが金目鯛を買える店の名前を入れてください。]]
""",
  "faq": [
    ("金目鯛は、レッドスナッパー（鯛の仲間）と同じですか",
     "違います。金目鯛はキンメダイ科の魚で、フエダイ（スナッパー）の仲間ではありません。「golden-eye snapper」は流通で使われる呼び名です。"),
    ("金目鯛はどんな味ですか",
     "一年中脂がのった白身で、煮ても、炙っても、生でもおいしく食べられます。定番は、醤油と砂糖で煮る煮付けです。"),
    ("金目鯛はどこでとれますか",
     "静岡県の伊豆半島にある下田は、下田市と静岡県が金目鯛の水揚げ日本一の港と説明しています。「地金目」として売られる魚は、大島から神津島にかけての近海でとれたものです。"),
    ("kinmedai はどう発音しますか",
     "英語を話す人には “kin-meh-dye” が近い音です。地元では「キンメ」と略すこともよくあります。"),
  ],
 },
},
# ============================================================ 空き家
{
 "id": "akiya-try-first", "slug": "akiya-try-before-you-buy", "topic": "own", "place": None, "also": ["live"],
 "photo": ("yaizu-engawa", "Old wooden house with a long veranda and an overgrown garden", "An older house in Iwashigashima, Yaizu, before renovation."),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Own a home",
 "h1": "Buying an akiya in Japan? Live in one for a month first",
 "seo_title": "Buying an Akiya in Japan? Live in One for a Month First",
 "description": "Japan has about nine million empty homes, and as of November 2026 foreigners aren’t banned from buying one. A month in the town tells you more than a listing.",
 "dek": "Japan has about nine million empty homes, and as of November 2026 foreigners aren’t banned from buying one. But the house is the easy part. The town is what you’re really signing up for, and a month there tells you more than any listing.",
 "card": "Japan has about nine million vacant homes, and as of November 2026 foreigners can buy them. The town matters more than the house: how long you can stay, where to stay, and what a month shows you.",
 "keywords": [("buying an akiya in japan", "—", "—"), ("akiya", "3,600", "0")],
 "intent": "Do（比べたい・やり方）",
 "points": [
   "An akiya is an empty house. Japan had about 9.0 million of them on 1 October 2023, a record 13.8% of all homes.",
   "As of November 2026, foreigners aren’t banned from buying a home, but there’s more paperwork than before. We wouldn’t count on a house to help with a visa.",
   "A month in the town shows you what a listing can’t: the winter cold, whether you need a car, where you’ll shop and how the neighbours are.",
   "As of November 2026, most visa-exempt visitors can stay up to 90 days, and remote workers from certain countries can apply for a six-month digital nomad status.",
   "For somewhere to stay, you’ve got a town’s trial home, a monthly rental or a guesthouse with monthly rates. From abroad, the last two are usually more realistic.",
 ],
 "body": """
<p>An akiya (空き家) is simply a house that nobody lives in. Japan’s 2023 Housing and Land Survey counted 9.0 million of them on 1 October 2023, a record 13.8% of the country’s homes [[s:stat_housing2023]]. About 3.86 million weren’t for rent or sale and weren’t anyone’s second home either, up by 369,000 since 2018 [[s:stat_housing2023]]. That’s the group people usually mean when they talk about Japan’s abandoned houses.</p>

<h2>Can foreigners buy an akiya?</h2>
<p>Yes. As of November 2026, Japan doesn’t ban foreigners or non-residents from buying a home [[s:rej,mof_realprop_faq]]. There’s more paperwork than before, though. Since April 2026, non-residents who buy property have to report it under the Foreign Exchange Act, even a home they plan to live in [[s:mof_fefta2026,mof_realprop_faq]]. Since 5 October 2026, every buyer, Japanese or not, gives their nationality when the purchase is registered [[s:moj_nationality]].</p>
<p>The rules are still moving. As of November 2026, a bill before the Diet would create new zones within about 1 km of some defence and coast guard sites, and on uninhabited border islands [[s:cao_land_bill,cao_land_bill_outline]]. Every transfer of land ownership in those zones would need the government’s approval in advance, and the law would take effect within 18 months of being promulgated [[s:cao_land_bill_outline]].</p>
[[ed:Check the bill’s progress in the House of Representatives (222nd Diet, cabinet bill no. 18): has it passed, when was it promulgated, and when does it take effect?]]
<p>We’d also treat a house and a visa as two separate questions. If you’re hoping that owning a home will help you stay in Japan longer, ask an administrative scrivener (<em>gyoseishoshi</em>) who handles visas before you count on it. With the rules changing this fast, we think it’s sensible to have a lawyer or judicial scrivener (<em>shiho shoshi</em>) look at your own case before you sign.</p>
[[ed:Confirm with a gyoseishoshi or the Immigration Services Agency how owning property relates to residence status. No official source has been found for this yet.]]

<h2>Why live in the town before you buy?</h2>
<p>Buying the house is the easy part. What you’re really committing to is the town, and a listing can only tell you so much: the price, the floor plan, a few photos. The things that decide whether you’ll be happy there only show up once you’ve lived there for a while.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What you want to know</th><th>How a month shows you</th></tr></thead>
<tbody>
<tr><td>How cold an old wooden house gets in January, and what heating costs</td><td>You’ll feel it on the first cold night and see it on the electricity bill.</td></tr>
<tr><td>Whether daily life works without a car</td><td>A week of shopping and errands on foot, by bus or by bike makes it obvious. Our house in Shimoda is about ten minutes’ walk from the station, with a supermarket, a convenience store and places to eat nearby, and that kind of spot is easy to test.</td></tr>
<tr><td>Where you’ll buy food, and when the shops close</td><td>Cooking most of your own meals soon shows you what’s easy to find and what isn’t.</td></tr>
<tr><td>How rubbish sorting works on that street</td><td>You’ll be following the local collection calendar like everyone else. If there’s an English version, it’s worth asking city hall for it.</td></tr>
<tr><td>Whether the internet holds up for a working day</td><td>Normal working hours, video calls included, are the real test.</td></tr>
<tr><td>What humid months and typhoons do to the building</td><td>Neighbours and local builders know what tends to fail first in houses like it.</td></tr>
<tr><td>How the neighbourhood treats a newcomer</td><td>Saying hello, joining a clean-up day if there is one, and asking how other newcomers settled in will tell you a lot. Neighbours notice small things, too. When our broadband was being installed in Shimoda, we heard from neighbours about where the engineer’s van was parked.</td></tr>
</tbody></table></div>
<p>None of this comes up in a viewing.</p>

<h2>What only shows up once you live in an old house?</h2>
<p>The wiring and the internet, in our experience. We learnt this when one of our founding members rented an old house in Shimoda from its owner and turned it into a guesthouse. We rented rather than bought, but we think a buyer would run into the same things.</p>
<p>The old two-wire electrics couldn’t run the air conditioner, the fridge and the microwave all at once, so we had to ask guests not to use them together. Upgrading the wiring costs real money, so it’s something to find out before you budget, not after. Getting broadband put in took more than two months because it was the busy season, and we got by on a plug-in home router until then.</p>
<p>That’s true of cheap houses in general. The asking price is only part of the bill: renovation, taxes, insurance and upkeep come on top, and they vary so much from one building to the next that only written quotes will tell you the real figure.</p>

<h2>How long can you stay in Japan to test a town?</h2>
<p>Long enough for a proper trial, for most people. There are two main ways to do it without a work or residence visa, and the rules below are as of November 2026.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Way to stay</th><th>How long</th><th>Who it’s for</th></tr></thead>
<tbody>
<tr><td><strong>Short-term visitor</strong>, visa-exempt</td><td>Up to 90 days for most visa-exempt nationalities. Some get 15 or 30 days, and some passports come with extra conditions [[s:mofa]].</td><td>Anyone from a visa-exempt country or region. The rule for your own passport is the one that counts.</td></tr>
<tr><td><strong>Digital nomad</strong> status</td><td>Six months, and it can’t be renewed. Once six months have passed after you leave Japan, you can come back under it again [[s:isa_nomad_en]].</td><td>Nationals of countries and regions that are both visa-exempt and have a tax treaty with Japan [[s:isa_nomad_list]]. You need an annual income of at least ¥10 million and private medical insurance with at least ¥10 million of treatment cover, and you can’t work for a Japanese employer [[s:isa_nomad_en]].</td></tr>
</tbody></table></div>
<p class="fine">This is general information, not immigration advice. The list of eligible countries for the digital nomad status changes, so check it for your own passport.</p>
[[ed:Open MOFA’s visa exemption page and confirm the 90-day rule and the exceptions; open the Immigration Services Agency’s digital nomad page and list of eligible countries, and confirm each condition as of the publishing date.]]

<h2>Where can you stay for a month to test a town?</h2>
<p>You’ve got three main choices: a town’s trial home, a monthly rental, or a guesthouse with monthly rates. Which one works depends on the town, and on where you’re coming from.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Option</th><th>How long</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>A town’s trial home</strong> (<em>otameshi jutaku</em>)</td><td>From a day or two up to a few months, and in one city up to two years [[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>Each town sets its own rules, mostly for people planning to move. Minami-Alps City lets one for one to three months at ¥21,000 a month (February 2026) [[s:minamialps_trial]].</td></tr>
<tr><td><strong>A monthly rental</strong></td><td>A month or more</td><td>A furnished room or flat let by the month. In a small town there may be few to choose from, so it helps to search early.</td></tr>
<tr><td><strong>A guesthouse or holiday home with monthly rates</strong></td><td>A week to a month or more</td><td>Often the easiest to book from abroad, and you can try living in an older house without committing to anything.</td></tr>
</tbody></table></div>
<p>Trial homes sound ideal, but there’s a catch: they’re built for people who are moving, not for people testing a town from abroad. Minami-Alps City’s home is for people registered as living outside Yamanashi who intend to move to the city and have signed up for a relocation consultation [[s:minamialps_trial]]. Nationality isn’t one of the listed conditions, so if you live overseas, the city’s relocation desk can tell you whether you’d qualify.</p>
<p>Some cities spell it out. Shizuoka City’s long-term trial flats are city-run apartments you can rent for six months to under two years, but only if you live outside Shizuoka Prefecture and have decided to move to the city. Foreign nationals qualify only as permanent residents, long-term residents, special permanent residents or spouses of Japanese nationals (page updated August 2026) [[s:shizuoka_long_trial]]. So a tourist or digital nomad stay won’t qualify there. In our view, if you’re coming from abroad, a monthly rental or a guesthouse is usually the realistic choice. If you’ve set your heart on a trial home, the town’s relocation office is the first call to make.</p>
[[ed:Ask the Izu towns (Shimoda, Minamiizu, Izu City) whether they have trial homes of a month or more, what they cost, and whether foreign nationals or people living overseas can use them.]]
<p>Towns within reach of Tokyo are the easiest to test. As of November 2026, the daily direct trains from Tokyo Station reach Shimoda, on the [[l:izu|Izu Peninsula]], in 2 hours 29 to 44 minutes [[s:jre_tt_tokyo]]. Our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] has the details.</p>
<p>If Shimoda is on your list, our own home there, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is one of the guesthouse options above. It’s an older house in the old town, renovated for long stays and licensed under Japan’s Hotel Business Act. Most of our guests so far have come from Europe and North America, and some come to work remotely.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, our home in Shimoda’s old town.]]
[[ed:Confirm before publishing: whether stays of 30 nights or more can always be accepted, and whether we may call the Shimoda house an older house.]]

<h2>What does a trial month look like?</h2>
<p>Mostly, it looks like ordinary life, with a few deliberate tests built in. Here’s roughly how we’d spend it, based on what caught us out in Shimoda.</p>
<p>The first week goes on settling in: the supermarket, the clinic, the bus stop and the rubbish calendar. If you’re staying in an older house, ask your host what amperage the electricity contract allows and where the breaker box is. Our own old wiring couldn’t run the air conditioner, fridge and microwave together, and those two answers give you a feel for what an old house can handle.</p>
<p>By the second week you’re working your usual hours and cooking at home. That’s when you find out whether the connection survives a day of video calls, and you’ll see what heating or cooling really costs. It’s also a good moment to ask a local provider how long a new line takes there, since ours took more than two months.</p>
<p>The third week is for asking around. You might visit the city hall desk that handles empty houses, talk to a local agent, or ask a builder roughly what rewiring an old house costs. Neighbours are often the best people to tell you what humid summers and typhoons do to houses like theirs.</p>
<p>By the fourth week you’ll have a fair idea of what would need to change, about the house and about the way you live. Writing those costs and doubts down while they’re fresh makes it much easier to compare towns, or to walk away.</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
   ("Can foreigners buy property in Japan?",
    "As of November 2026 there’s no ban, but non-residents must report a purchase under the Foreign Exchange Act, and every buyer gives their nationality at registration [[s:mof_fefta2026,moj_nationality]]. The rules are changing, so a lawyer or judicial scrivener can check your own case."),
   ("Will owning a house in Japan help me get a visa?",
    "We wouldn’t count on it. We treat a house and a visa as separate questions, so if staying longer is part of your plan, ask an administrative scrivener (<em>gyoseishoshi</em>) who handles visas before you buy."),
   ("Is a cheap house in Japan really cheap?",
    "Not always. The purchase price is only one part of the bill. Renovation, taxes, insurance and upkeep come on top, and they vary a lot from one building to the next, so written quotes are the only way to know before you commit."),
   ("Can I use a town’s trial home as a foreigner?",
    "It depends on the town. Trial homes are mostly for people who plan to move there, and some spell out who qualifies. As of August 2026, Shizuoka City’s long-term trial flats took foreign nationals only with permanent, long-term or special permanent residence, or as the spouse of a Japanese national [[s:shizuoka_long_trial]]. The town’s relocation office will know the current rules."),
   ("How many akiya are there in Japan?",
    "About 9.0 million homes were empty on 1 October 2023, 13.8% of all housing, according to the 2023 Housing and Land Survey [[s:stat_housing2023]]."),
 ],
 "sources": ["stat_housing2023", "rej", "mof_fefta2026", "mof_realprop_faq", "moj_nationality", "cao_land_bill", "cao_land_bill_outline", "mofa",
             "isa_nomad_en", "isa_nomad_list", "minamialps_trial", "shizuoka_trial", "shizuoka_long_trial", "jre_tt_tokyo"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "空き家を買う前に、まず1か月住んでみる",
  "dek": "日本には約900万戸の空き家があり、2026年11月時点で、外国人が買うことは禁止されていません。でも、家を買うのは簡単なほうです。本当に引き受けるのは町のほうで、そこで1か月暮らすと、物件情報よりずっと多くのことが分かります。",
  "review": [
   "【2026-11-15 組み込み前の仕上げ（品質保証部 90点・合格のあとの編集長の指摘8点）】変えた点: ①「家は安いほうの買い物」→「家を買うこと自体は簡単なほう」（リードと FAQ に合わせました）。配線の節の後に、改修・税金・保険・維持費が上乗せされ、本当の金額は書面の見積もりで分かる、の2文を足しました ②FAQ のお試し住宅の答えに特別永住者を足しました ③行政書士を英語で「在留資格（ビザ）の手続きを扱う行政書士（administrative scrivener）」と資格の名前で書きました（本文・FAQ） ④【事実の変更】「下田まで直通で3時間かからない」→「2026年11月時点で、東京駅から毎日走る直通で2時間29〜44分」。出典を編集長が確かめた JR東日本の東京駅の時刻表（jre_tt_tokyo）に替え、踊り子のページ（jreast_odoriko）は外しました ⑤南アルプス市の条件を「国籍は条件に挙げられていない」と制度の側から書きました ⑥NODE Shimoda の段落を3文にし、「一年中泊まれ、週割・月割がある」を削りました（黄色い枠から月額料金も外しました） ⑦「なぜ町で暮らすのか」の表の2行を、確認済みの体験（experience.md 3-2）につなげました。車の行に「下田の家は駅から徒歩10分ほどで、スーパー・コンビニ・飲食店が近い」、近所の行に「回線工事の車の停め方で近所から声をかけられた」 ⑧お試し1週目の「エアコン・冷蔵庫・電子レンジを同時に使ってみる」を、「泊まり先の人に契約のアンペア数とブレーカーの場所を聞く」に替えました。人に確かめてほしい点: 近所の行の書き方（experience.md では「工事の車両の駐車で近隣から指摘を受けた」）が、やわらげすぎ・強すぎになっていないか",
   "【2026-11-15 3回目の書き直し（品質保証部 84点・ゲート違反1、リサーチメモ 3）】変えた点: ①【事実の変更】土地の法案を、内閣府の法案の概要どおりに直しました。「重要な防衛施設の周りや国境の離島、国籍を問わず許可」→「一部の防衛関係施設と海上保安庁の施設の周り（おおむね1km）と無人の国境離島に区域をつくり、区域内の土地の所有権の移転はすべて事前許可。公布から1年6か月以内に施行」。審議の状況は「2026年11月時点で国会にかかっている」だけにし、10月23日の日付と内閣官房の提言の出典（cas_land_teigen）は外しました。新しい出典 cao_land_bill_outline を足しました ②【主張の変更】「家を買っても在留資格は付かない」「買うのにビザは要らない」は公的な出典が見つからなかったので、断定をやめました。本文・In short・FAQ とも「家とビザは別々の問題として考える、あてにする前に行政書士に聞く」という私たちの見方にし、黄色い枠を足しました ③description・card・In short の4項目目に「2026年11月時点」、FAQ のお試し住宅に「2026年8月時点」を入れました ④「海外に住む人が対象か確かめられなかった」という調べた側の言い方をやめ、「市の移住の窓口に聞けば分かる」にしました ⑤「it’s worth …」を7回から1回に減らし、締めの言い方を変えました（日本語版の「〜しておくと安心です」も同じように減らしました） ⑥「泊まれる場所」の節の最初の文で3つの選択肢の名前を言い、表のお試し住宅の欄を短くしました（静岡市オクシズの例と出典 okushizuoka_trial は外しました） ⑦「お試しの1か月」の節を、下田での体験（配線・回線工事の待ち）と表の項目につなげ、週ごとに試すこと（家電の同時使用、ビデオ会議と冷暖房費、回線工事にかかる期間を業者に聞く、配線のやり直しの費用を工務店に聞く、湿気・台風のことを近所に聞く、費用と迷いを書きとめる）を具体的にしました。新しい事実は足していません ⑧日本語版の伊豆半島への内部リンクを、日本語版の記事（ja-izu）に向くよう直しました ⑨In short の5項目目に「海外からならマンスリーか宿が現実的」を足しました（本文の見方と同じ）",
   "【2026-11-15 2回目の書き直し（リサーチメモ 2・組み込み後の採点の指摘）】変えた点: ①【事実の変更】京丹後市のお試し住宅は2026年9月末で市営の住宅が閉鎖されたため（市の閉鎖のお知らせ）、京丹後市を例から外し、出典 kyotango_trial も消しました。京丹後市にもとづいていた「1日から2か月ほどまで」は、「1〜2日から数か月まで、2年まで住める市もある」に直しました（静岡市 中心部・南アルプス市 1〜3か月・静岡市 長期 半年〜2年） ②お試し住宅の例を、リサーチ部が公式ページを開いて確かめた2つにしました。南アルプス市（芦安、1〜3か月・月21,000円、山梨県外に住民登録があり移住するつもりで移住相談に登録した人。国籍の記載なし）と、静岡市の長期お試し住宅（市営住宅に半年以上2年未満、静岡県外に住み移住を決めた人、外国籍は永住者・定住者・特別永住者・日本人の配偶者等に限る） ③お試し住宅は「移住する人のための仕組み」で、観光やデジタルノマドの滞在では使えない市があることを正直に書き、海外から来るならマンスリーか宿のほうが現実的だという見方を「私たちの考え」として添えました。FAQ の「外国人でも使えるか」も静岡市の例で答え直しました ④前の「たいてい町の外に住民登録がある人」という言い方（実際は県外が多い）をやめ、市ごとの条件をそのまま書きました ⑤「下田まで直通で3時間以内」に JR東日本（踊り子）の出典を付けました。数字は出していません ⑥「お試しの1か月」の節を、「1週目：…」のラベルの箇条書きから、ふつうの文章の段落に直しました ⑦伊豆の市町の黄色い枠を「1か月以上泊まれるか・料金・外国籍や海外在住の人が使えるか」に広げました",
   "【2026-11-15 品質保証部の指摘を受けた書き直し】変えた点: ①「購入に国籍・在留の制限はない」の断定をやめ、「2026年11月時点で禁止はないが、手続きは増えた（2026年4月から非居住者は外為法の報告、10月5日から登記で国籍の届出）。重要な区域の土地の許可制の法案が10月23日に国会に出ている」の形にし、専門家（弁護士・司法書士）に確かめるよう添えました（財務省・法務省・内閣府・内閣官房の出典） ②デジタルノマドを、出入国在留管理庁の条件どおりに直しました（対象はビザ免除かつ租税条約のある国・地域の人、年収1,000万円以上、治療費1,000万円以上の民間医療保険、日本の会社には雇われない、6か月で更新不可、出国から6か月たてば再び可）。時点は2026年11月 ③滞在の手段（観光の短期滞在・デジタルノマド）を表にしました ④空き家の数の出典を、総務省統計局の確報（2024年9月公表）1つにしました（900万戸・13.8%・過去最高、使い道のない空き家 約386万戸・2018年から36.9万戸増） ⑤「1か月泊まれる場所」の節を新しく書き、自治体のお試し住宅（自治体ごと、条件は町の外に住民登録があって移住を考えている人など。例は静岡市オクシズの3泊〜2週間・1組1日300円）、マンスリー、宿を表で並べました。NODE Shimoda はその中の1つとして紹介しています ⑥創業メンバーが下田で借りた古い家を宿に改修したときの体験を2点入れました（古い2芯の配線でエアコン・冷蔵庫・電子レンジを同時に使えなかった／繁忙期で回線工事に2か月以上かかり、置き型のルーターでしのいだ）。「買った」とは書かず「持ち主から借りた」と明記しています ⑦ゲストを「リモートで働く人がたくさん」→「リモートで働きに来る人もいる」に ⑧前の最後の節の「いちばんの近道」という押しの強い言い方をやめ、最後は1か月の過ごし方の節にしました。4週目も「決める」→「振り返る」に ⑨FAQ に「外国人は買えるか」「お試し住宅は外国人も使えるか」を足して5問にしました",
   "【人に確かめてほしい点】⓪【今回】(a) 土地の法案が成立したか、いつ公布・施行か（黄色い枠。審議入りの報道は政党の機関紙でしか確認できず、記事には「国会にかかっている」とだけ書いています） (b)「外国人が家を買うことは禁止されていない」の出典の1つ rej（Real Estate Japan）は民間の不動産サイトです。もう1つは財務省の FAQ ですが、在留資格と不動産の関係は公的な出典が見つからず、行政書士か入管で確かめてほしい点として黄色い枠を置きました (c) NODE Shimoda を英語で「older house」（古い家）と呼んでよいか（experience.md では「旧町内の空き家を改修した」とあり、築年数は未確認） (d)「お試しの1か月」の節の「私たちならこう過ごす」は私たちの見方として書いています。言い方に違和感がないか ①法務・在留の記述（不動産購入の手続き、法案の審議状況、デジタルノマドの条件、90日と例外の国）は、公開の直前に一次のページを開いて確かめてください（黄色い枠4か所） ②創業メンバーの体験（配線・回線）の書き方が、事実と合っているか。「私たち（we）」の体験として書いています ③伊豆の市町（下田市・南伊豆町・伊豆市）に1か月以上泊まれるお試し住宅があるか、料金、外国籍・海外在住の人が使えるか（黄色い枠） ④月額料金、30泊以上を常に受けられるか、「再生した空き家」と呼んでよいか（黄色い枠） ⑤法務・在留の出典はリサーチ部が検索で確認したもので、本文のページは開けていません ⑥「下田まで直通の電車で3時間かからない」の出典の JR東日本の踊り子のページ（東京〜伊豆急下田 2時間49分）は、この環境から開けず検索でしか確かめていません。公開前にページを開いて確かめてください（ほかの記事は駅探の約2時間35分を使っているので、数字は出していません） ⑦南アルプス市・静岡市のお試し住宅の条件と料金（2026年11月15日にリサーチ部がページを開いて確認）が、公開の時点でも変わっていないか ⑧京丹後市を外したことでよいか（市営のお試し住宅は2026年9月末で閉鎖。民間・地域のお試し住宅は案内されていますが、例には使っていません）",
   "【入れられなかったこと】外為法の不動産取得の報告の細かい範囲（財務省の制度の概要のページを本文で確認できていないため）、在留資格と不動産の所有の関係を書いた公的な出典、海外に住む人が南アルプス市などのお試し住宅の対象に入るか（ページに記載がなく、町に聞くように書きました）、伊豆の市町のお試し住宅の有無、新耐震基準（1981年）など建物の点検の項目（公的な出典を未確認）、マンスリーの部屋の相場（出典なし）。焼津・修善寺の家は、状況が決まるまで書いていません",
  ],
  "points": [
    "akiya（空き家）は、人が住んでいない家のこと。2023年10月1日時点で約900万戸、住宅全体の13.8%で、過去最高でした。",
    "2026年11月時点で、外国人が家を買うことは禁止されていません。ただ、手続きは前より増えました。家を持てばビザに有利になる、とは考えないほうがいいと私たちは思います。",
    "町で1か月暮らすと、物件情報では分からないことが見えてきます。冬の寒さ、車が要るか、どこで買い物するか、近所の人のこと。",
    "2026年11月時点で、ビザ免除の国の人の多くは90日まで滞在でき、特定の国のリモートワーカーなら6か月の「デジタルノマド」の在留資格もあります。",
    "泊まる場所は、自治体のお試し住宅、マンスリーの部屋、月割のある宿の3つ。海外から来るなら、たいていは後の2つが現実的です。",
  ],
  "body": """
<p>akiya（空き家）は、ひとことで言えば、誰も住んでいない家のことです。2023年の住宅・土地統計調査では、2023年10月1日時点で900万戸、日本の住宅の13.8%が空き家で、割合は過去最高でした[[s:stat_housing2023]]。そのうち約386万戸は、貸すためでも売るためでもなく、別荘でもない家で、2018年から36万9千戸増えました[[s:stat_housing2023]]。「日本の放置された家」と言うとき、たいていはこの家のことを指しています。</p>

<h2>外国人は空き家を買えるのか</h2>
<p>買えます。2026年11月時点で、外国人や日本に住んでいない人が家を買うことは禁止されていません[[s:rej,mof_realprop_faq]]。ただ、手続きは前より増えました。2026年4月から、日本に住んでいない人が不動産を買うと、住むための家でも外為法にもとづく報告が要ります[[s:mof_fefta2026,mof_realprop_faq]]。2026年10月5日からは、日本人も含めて、買った人はみな登記のときに国籍を届け出ます[[s:moj_nationality]]。</p>
<p>決まりは、まだ動いています。2026年11月時点で国会にかかっている法案は、一部の防衛関係施設と海上保安庁の施設の周り（おおむね1km）と、無人の国境離島に、新しい区域をつくる内容です[[s:cao_land_bill,cao_land_bill_outline]]。その区域で土地の所有権を移すときは、すべて事前に国の許可が要り、法律は公布から1年6か月以内に施行されます[[s:cao_land_bill_outline]]。</p>
[[ed:衆議院の議案審議経過（第222回国会 閣法18号）で、成立したか、いつ公布・施行かを確かめてください。]]
<p>家とビザは、別々の問題として考えたほうがいいと私たちは思います。家を持つことで日本に長くいられるようになると期待しているなら、あてにする前に、在留資格（ビザ）の手続きを扱う行政書士に聞いてみてください。決まりがこれだけ速く変わっているので、契約の前に、自分の場合を弁護士や司法書士に見てもらうのが賢明だと思います。</p>
[[ed:不動産を持つことと在留資格の関係を、行政書士か出入国在留管理庁に確かめてください。いまのところ公的な出典は見つかっていません。]]

<h2>なぜ、買う前にその町で暮らすのか</h2>
<p>家を買うこと自体は、簡単なほうです。本当に引き受けるのは町のほうで、物件情報から分かるのは、価格と間取りと何枚かの写真くらい。そこで楽しく暮らせるかを決めることは、しばらく住んでみて初めて見えてきます。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>知りたいこと</th><th>1か月暮らすと、こう分かる</th></tr></thead>
<tbody>
<tr><td>古い木造の家が1月にどれくらい寒いか、暖房にいくらかかるか</td><td>最初の寒い夜に体で分かり、電気代の請求で数字でも分かります。</td></tr>
<tr><td>車なしで毎日の暮らしが回るか</td><td>1週間、買い物や用事を徒歩・バス・自転車で済ませてみると、はっきりします。下田の私たちの家は駅から歩いて10分ほどで、スーパー、コンビニ、飲食店が近くにあり、こういう場所なら試しやすいです。</td></tr>
<tr><td>どこで食料を買うか、店は何時に閉まるか</td><td>食事をほとんど自炊していると、手に入りやすいものとそうでないものが、すぐに分かります。</td></tr>
<tr><td>その通りのごみの分別の仕組み</td><td>地域の収集カレンダーに合わせて、みんなと同じように出すことになります。英語版があれば、役所でもらっておくと便利です。</td></tr>
<tr><td>一日仕事をしても回線がもつか</td><td>ビデオ会議も含めて、いつもどおりに働いてみるのが一番の確かめ方です。</td></tr>
<tr><td>湿気の多い時期や台風で、建物がどうなるか</td><td>同じような家でどこから傷みやすいかは、近所の人や地元の工務店がよく知っています。</td></tr>
<tr><td>新しく来た人を、近所がどう迎えるか</td><td>あいさつをしたり、清掃の日があれば参加したり、先に移ってきた人にどうなじんだかを聞いたりすると、よく分かります。近所の人は小さなことにも気づきます。下田で回線の工事をしたとき、工事の車をどこに停めたかについて、近所の方から声をかけられました。</td></tr>
</tbody></table></div>
<p>どれも、内見では出てこないことばかりです。</p>

<h2>古い家で、住んでみて初めて分かることは何か</h2>
<p>私たちの経験では、配線と回線です。創業メンバーの1人が、下田の古い家を持ち主から借りて、宿に改修したときに知りました。買ったのではなく借りた家ですが、買った人も同じことにぶつかると私たちは思います。</p>
<p>古い2芯の配線では、エアコンと冷蔵庫と電子レンジを同時に使えず、ゲストに同時に使わないようお願いすることになりました。配線をやり直すにはそれなりの費用がかかるので、予算を組む前に知っておきたいことです。インターネットの回線工事は、繁忙期だったこともあって申し込みから2か月以上かかり、それまでは置き型のホームルーターでしのぎました。</p>
<p>これは、安い家すべてに言えることです。売り出し価格は、かかるお金の一部にすぎません。改修、税金、保険、維持費が上乗せされ、建物ごとに大きく変わるので、本当の金額は書面の見積もりを取って初めて分かります。</p>

<h2>町を試すために、日本にどれくらいいられるのか</h2>
<p>多くの人にとって、しっかり試せるくらいの長さはあります。就労や居住のビザなしで滞在する方法はおもに2つで、下の条件は2026年11月時点のものです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>滞在のしかた</th><th>期間</th><th>対象</th></tr></thead>
<tbody>
<tr><td><strong>短期滞在</strong>（ビザ免除）</td><td>ビザ免除の国・地域の多くは90日まで。15日や30日の国もあり、パスポートに条件が付く場合もあります[[s:mofa]]。</td><td>ビザ免除の国・地域の人。大事なのは、自分のパスポートの条件です。</td></tr>
<tr><td><strong>デジタルノマド</strong>の在留資格</td><td>6か月で、更新はできません。日本を出てから6か月たてば、同じ資格でまた来られます[[s:isa_nomad_en]]。</td><td>ビザ免除で、かつ日本と租税条約のある国・地域の人[[s:isa_nomad_list]]。年収1,000万円以上と、治療費1,000万円以上を補償する民間の医療保険が必要で、日本の会社に雇われて働くことはできません[[s:isa_nomad_en]]。</td></tr>
</tbody></table></div>
<p class="fine">これは一般的な情報で、在留手続きの助言ではありません。デジタルノマドの対象の国は変わるので、自分のパスポートで確かめてください。</p>
[[ed:外務省の査証免除のページで90日と例外の国を、出入国在留管理庁のデジタルノマドのページと対象国の一覧で各条件を、公開の時点で開いて確かめてください。]]

<h2>町を試すために1か月泊まれる場所はどこか</h2>
<p>おもな選択肢は、自治体のお試し住宅、マンスリーの部屋、月割のある宿の3つです。どれが合うかは、町と、どこから来るかによります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>選択肢</th><th>期間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>自治体のお試し住宅</strong></td><td>町によって、1〜2日から数か月まで。2年まで住める市もあります[[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>決まりは町ごとで、多くは移住するつもりの人向け。南アルプス市は1〜3か月、月21,000円で貸しています（2026年2月）[[s:minamialps_trial]]。</td></tr>
<tr><td><strong>マンスリーの部屋</strong></td><td>1か月以上</td><td>家具付きの部屋を月単位で借ります。小さな町では選べる数が少ないこともあるので、早めに探すと安心です。</td></tr>
<tr><td><strong>月割のある宿・貸別荘</strong></td><td>1週間〜1か月以上</td><td>海外からいちばん予約しやすいことが多く、何も契約せずに古い家での暮らしを試せます。</td></tr>
</tbody></table></div>
<p>お試し住宅はよさそうに見えますが、落とし穴があります。移住する人のための仕組みで、海外から町を試しに来る人向けではないのです。南アルプス市のお試し住宅は、山梨県の外に住民登録があり、市に移住するつもりで、移住の相談に登録した人が対象です[[s:minamialps_trial]]。国籍は条件に挙げられていないので、海外に住んでいるなら、対象に入るかは市の移住の窓口に聞けば分かります。</p>
<p>はっきり書いている市もあります。静岡市の「長期お試し住宅」は、市営住宅に半年以上2年未満住めるものですが、静岡県の外に住んでいて、市への移住を決めた人が対象です。外国籍の人は、永住者・定住者・特別永住者・日本人の配偶者等の在留資格がある場合に限られます（2026年8月更新のページ）[[s:shizuoka_long_trial]]。つまり、観光やデジタルノマドの滞在では使えません。私たちの考えでは、海外から来るなら、マンスリーの部屋か宿のほうが現実的です。どうしてもお試し住宅を使いたいなら、まず町の移住の窓口に連絡してみてください。</p>
[[ed:伊豆の市町（下田市・南伊豆町・伊豆市）に1か月以上泊まれるお試し住宅があるか、料金、外国籍・海外在住の人が使えるかを問い合わせてください。]]
<p>東京から行きやすい町のほうが試しやすいです。2026年11月時点で、東京駅から毎日走る直通の電車なら、[[l:ja-izu|伊豆半島]]の下田まで2時間29〜44分です[[s:jre_tt_tokyo]]。くわしくは[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田が候補に入っているなら、下田の私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」も、上の宿の選択肢の1つです。旧町内の古い家を長期滞在向けに改修したもので、旅館業法の許可を受けています。これまでのゲストは欧米の人が中心で、リモートで働きに来る人もいます。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|下田の旧町内にある私たちの家「NODE Shimoda」のリビング。]]
[[ed:公開前に要確認：30泊以上を常に受けられるか、下田の家を英語で「older house（古い家）」と呼んでよいか。]]

<h2>お試しの1か月は、どんなふうに過ぎるか</h2>
<p>ほとんどは、ふだんの暮らしそのものです。そこに、いくつか意識して試すことを入れます。下田で私たちがつまずいたことをもとに、私たちならこう過ごす、という例です。</p>
<p>最初の1週間は、落ち着くための時間です。スーパー、診療所、バス停、ごみの収集日を覚えます。古い家に泊まっているなら、泊まり先の人に、電気の契約のアンペア数とブレーカーの場所を聞いておきましょう。私たちの家の古い配線では、エアコンと冷蔵庫と電子レンジを同時に使えませんでした。この2つが分かると、古い家の電気でどこまでできるかの感覚がつかめます。</p>
<p>2週目には、いつもの時間に働き、家で料理をするようになります。ビデオ会議の続く一日に回線がもつか、冷暖房に実際いくらかかるかが分かるのはこの頃です。地元の回線業者に、そこで新しく回線を引くとどれくらいかかるかを聞いておくのもいい時期です。私たちのときは2か月以上かかりました。</p>
<p>3週目は、聞いてまわる週です。役所の空き家の窓口に行ったり、地元の不動産屋と話したり、工務店に古い家の配線のやり直しがおおよそいくらかを聞いたりできます。湿気の多い夏や台風で家がどうなるかは、近所の人がいちばんよく知っています。</p>
<p>4週目には、家について、そして自分の暮らし方について、何を変える必要がありそうか、だいたい見えています。費用や迷いを忘れないうちに書きとめておくと、町どうしを比べるときにも、見送ると決めるときにも、ずっと楽になります。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
    ("外国人は日本の不動産を買えますか",
     "2026年11月時点で禁止はありませんが、日本に住んでいない人は外為法にもとづく報告が要り、買った人はみな登記のときに国籍を届け出ます[[s:mof_fefta2026,moj_nationality]]。決まりが変わりつつあるので、自分の場合は弁護士や司法書士に見てもらえます。"),
    ("日本で家を持つと、ビザを取りやすくなりますか",
     "あてにしないほうがいいと私たちは思います。家とビザは別々の問題として考えているので、長く住むことも計画に入っているなら、買う前に、在留資格（ビザ）の手続きを扱う行政書士に聞いてみてください。"),
    ("日本の安い家は、本当に安いのですか",
     "そうとは限りません。購入価格は、かかるお金の一部です。改修、税金、保険、維持費が上乗せされ、金額は建物によって大きく変わるので、決める前に知るには、書面の見積もりを取るしかありません。"),
    ("外国人でも、自治体のお試し住宅を使えますか",
     "町しだいです。お試し住宅は、多くが移住するつもりの人向けで、対象をはっきり書いている町もあります。たとえば静岡市の長期お試し住宅は、2026年8月時点で、外国籍の人なら、永住者・定住者・特別永住者の在留資格か、日本人の配偶者である場合に限られていました[[s:shizuoka_long_trial]]。いまの決まりは、町の移住の窓口が知っています。"),
    ("日本に空き家は何戸ありますか",
     "2023年の住宅・土地統計調査によると、2023年10月1日時点で約900万戸、住宅全体の13.8%が空き家でした[[s:stat_housing2023]]。"),
  ],
 },
},
# ============================================================ 伊豆
{
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, fares and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Fares and Where to Stay",
 "description": "How to get from Tokyo to the Izu Peninsula by train, with times and fares to Atami, Ito, Shimoda and Shuzenji, the best season and why a house beats a day trip.",
 "dek": "The south of the Izu Peninsula is too far for a day trip and just right for a week. Here’s how to get there, when to go, and the downsides nobody mentions.",
 "card": "Train routes, times and fares from Tokyo to Atami, Ito, Shimoda and Shuzenji, plus the seasons and the drawbacks nobody mentions.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—")],
 "intent": "Do（やり方を知りたい）",
 "points": [
   "Shimoda is about 2 hours 35 minutes from Tokyo on the direct limited express, so a day trip means more than five hours on the train.",
   "Shuzenji is about two hours away, either direct or by Shinkansen to Mishima and a 35-minute local line.",
   "The official swimming season runs from mid-July to late August, and that’s the only time lifeguards are on duty.",
   "Buses are few and many shops close early outside summer, which is why a house with a kitchen makes such a difference.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The easiest way is the Odoriko limited express, which runs direct from Tokyo down the east coast of the [[l:izu|Izu Peninsula]] to Shimoda. A second branch heads inland to Shuzenji. Here are the times and one-way fares to the four main stops.</p>
""" + TRAIN_TABLE_EN + """
<p class="fine">Times and fares for Atami, Ito and Shuzenji are from [[a:jg6305]]. The Shimoda time and fare are from [[a:ekitan]]. Fares change, so check before you book.</p>
<p>For Shuzenji there’s also a route with far more trains: the Shinkansen to Mishima, then 35 minutes on the Izuhakone Railway [[s:jg6311]]. If you’re travelling on a Japan Rail Pass, it won’t cover the private line between Ito and Shimoda, and the Mishima to Shuzenji section carries a ¥550 supplement [[s:jg6305]].</p>

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is, but the south really isn’t. The direct Odoriko takes about 2 hours 35 minutes from Tokyo to Izukyu-Shimoda [[s:ekitan]], so going there and back means more than five hours on a train for a few hours on the beach. Atami and Ito, closer to Tokyo, work fine as day trips. The south coast and the inland hot-spring towns are far better if you stay.</p>

<h2>Which Izu town suits you?</h2>
<p>It mostly comes down to how far you want to go and how long you can stay.</p>
<div class="tablewrap"><table>
<thead><tr><th>Town</th><th>From Tokyo</th><th>What it’s like</th><th>Day trip or stay?</th></tr></thead>
<tbody>
<tr><td><strong>Atami and Ito</strong></td><td>About 80 to 100 min</td><td>The closest to Tokyo and the busiest, with the most hotels.</td><td>A day trip works</td></tr>
<tr><td><strong>Shuzenji</strong></td><td>About 2 h</td><td>A hot-spring town inland, along a river, with a bamboo grove, a temple and a free public foot bath [[s:uncharted]].</td><td>Better to stay</td></tr>
<tr><td><strong>Shimoda</strong></td><td>About 2 h 35 min</td><td>A port town with white-sand beaches. Shirahama Beach is about 15 minutes by bus from the station [[s:jnto]]. The city and the prefecture describe its harbour as Japan’s top landing port for [[l:kinmedai|kinmedai]] [[s:pref]].</td><td>Better to stay</td></tr>
</tbody></table></div>
<p class="fine">Times are from the train table above.</p>

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>For swimming, it’s mid-July to late August. For a quieter stay, the months either side are hard to beat.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Mid-July to late August</td><td>The official swimming season at Izu beaches [[s:jg6322]], and the only time lifeguards are on duty [[s:funjapan]].</td></tr>
<tr><td>Late May to September</td><td>In good weather the sea is pleasant [[s:jg6304]], and outside the school holidays there are fewer people around.</td></tr>
<tr><td>The rest of the year</td><td>The towns get much quieter, and plenty of restaurants and shops close early [[s:tdn]].</td></tr>
</tbody></table></div>

<h2>What changes when you rent a house in Izu?</h2>
<p>A hotel room is built around one or two nights and a set dinner time. A house gives you a kitchen, a washing machine and a table to work at, and that’s what makes four nights or a week easy. A typical day ends up looking like this: work in the morning, the beach or a hot spring in the afternoon, and dinner at home once the restaurants have closed.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, about ten minutes on foot from Izukyu-Shimoda Station.]]
<p>Our home in Shimoda, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, was set up for exactly this kind of stay. It has a work desk, a washing machine and dryer, a properly equipped kitchen and self check-in with a smart lock. It’s about ten minutes on foot from Izukyu-Shimoda Station, with restaurants, a convenience store and a supermarket close by.</p>
<p>If a week in Izu gets you thinking about a longer stay, or even a house of your own, here’s why we suggest [[l:akiya-try-first|living in a town for a month before buying a house]].</p>
[[ed:Add the measured Wi-Fi speed and the time of the last bus from the beaches.]]

<h2>What are the downsides of staying in Izu?</h2>
<p>Getting around takes a bit of planning. Buses don’t run often, ride-hailing is nothing like a big city, and the direct trains from Tokyo run mainly in the morning and early afternoon [[s:tdn]]. It helps to plan the day around the timetable and get your shopping done before evening. If you want to hop between beaches, an e-bike or a rental car makes life much easier.</p>
""",
 "faq": [
   ("Can I use the Japan Rail Pass to get to Izu?",
    "Partly. It covers the JR sections, but not the Izukyu line between Ito and Shimoda, and Mishima to Shuzenji needs a ¥550 supplement [[s:jg6305]]."),
   ("Do I need a car on the Izu Peninsula?",
    "Not to get to Shimoda or Shuzenji. You’ll only really miss one when you want to move between beaches."),
   ("How long does it take to get from Tokyo to Shimoda?",
    "About 2 hours 35 minutes on the direct Odoriko limited express from Tokyo to Izukyu-Shimoda Station [[s:ekitan]]."),
 ],
 "sources": ["ekitan", "jg6305", "jg6311", "jg6322", "jg6304", "jnto", "funjapan", "uncharted", "tdn", "pref"],
 "related": ["kinmedai", "izu"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・運賃と、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りには遠く、1週間ならちょうどいい距離です。行き方、いつ行くか、そしてあまり語られない弱点をまとめました。",
  "review": [
   "【2026-11-15 トーンの書き直し】ぶつ切りの短い文や硬い言い方をやめ、現地に住む友人が話すような文にしました（英語は短縮形と you / we を使う形に）。日本語版も自然な話し言葉寄りにしました。数字・出典・主張は変えていません",
   "【2026-11-15 の見直しで変えた点（見せ方）】「どの町が合うか」を、東京からの時間・町の様子・日帰りか泊まりかの表にしました。季節も表にしました。本文から伊豆半島のページと、空き家の記事（買う前に1か月住む）へのリンクを足しました。狙う検索語から「izu peninsula」を外しました（伊豆半島のページと重ならないように）",
   "【変えた点（言い方を出典の範囲に弱めた）】「港の金目鯛の水揚げは日本一」→「下田市と静岡県が、水揚げ日本一の港と説明している」（出典に静岡県のページを足しました）",
   "【人に確かめてほしい点】①所要時間と運賃が、いまの感覚と合っているか。JR の運賃は2026年に改定されたとの情報があり、表の数字が古い可能性があります（リサーチ部が公式の値で取り直す予定） ②回線速度の実測値と、浜からの最終バスの時刻（黄色い枠） ③「バスが少ない」「店が早く閉まる」という弱点の書き方が、地元として違和感がないか",
   "【まだ入れていないこと（出典の確認待ち）】新幹線で熱海へ出て乗り換える行き方と高速バスの比較、ジャパン・レール・パスと JR東京ワイド・パスの違い、直通の踊り子の本数。公式の値を確かめてから足します",
  ],
  "points": [
    "下田は、東京から直通の特急で約2時間35分。日帰りだと、電車に5時間以上乗ることになります。",
    "修善寺は約2時間。直通の特急か、新幹線で三島へ出てローカル線で35分です。",
    "正式な海水浴シーズンは7月中旬から8月下旬で、ライフガードがいるのもこの期間だけです。",
    "夏以外はバスが少なく、早く閉まる店も多いので、キッチンのある家だと過ごしやすさがまるで違います。",
  ],
  "body": """
<h2>東京から伊豆半島への行き方</h2>
<p>いちばん楽なのは、特急「踊り子」です。東京から[[l:izu|伊豆半島]]の東海岸を下田まで、乗り換えなしで走ります。もう一方は内陸の修善寺へ向かいます。主な4駅までの時間と片道の運賃は、次のとおりです。</p>
""" + TRAIN_TABLE_JA + """
<p class="fine">熱海・伊東・修善寺の時間と運賃は[[a:jg6305]]、下田の時間と運賃は[[a:ekitan]]によります。運賃は変わるので、予約の前に確かめてください。</p>
<p>修善寺へは、本数がずっと多い行き方もあります。新幹線で三島へ行き、伊豆箱根鉄道に35分乗るルートです[[s:jg6311]]。ジャパン・レール・パスで旅しているなら、伊東〜下田の私鉄区間には使えず、三島〜修善寺は550円の追加料金がかかります[[s:jg6305]]。</p>

<h2>伊豆半島は、東京から日帰りできるか</h2>
<p>北のほうはできますが、南はあまり向きません。直通の「踊り子」でも東京から伊豆急下田まで約2時間35分かかるので[[s:ekitan]]、往復すると、浜で過ごす数時間のために5時間以上電車に乗ることになります。東京に近い熱海や伊東なら、日帰りでも十分楽しめます。南の海岸と内陸の温泉町は、泊まったほうがずっと楽しめます。</p>

<h2>伊豆のどの町が合うか</h2>
<p>決め手は、どこまで行きたいかと、どれくらいいられるかです。</p>
<div class="tablewrap"><table>
<thead><tr><th>町</th><th>東京から</th><th>どんな町か</th><th>日帰りか、泊まりか</th></tr></thead>
<tbody>
<tr><td><strong>熱海と伊東</strong></td><td>約80〜100分</td><td>東京に最も近く、いちばんにぎやか。ホテルも最も多い町です。</td><td>日帰りでも楽しめる</td></tr>
<tr><td><strong>修善寺</strong></td><td>約2時間</td><td>川沿いに広がる内陸の温泉町。竹林や寺、無料の足湯があります[[s:uncharted]]。</td><td>泊まるのがおすすめ</td></tr>
<tr><td><strong>下田</strong></td><td>約2時間35分</td><td>白い砂浜のある港町。白浜海岸は駅からバスで約15分です[[s:jnto]]。下田市と静岡県は、[[l:ja-kinmedai|金目鯛]]の水揚げ日本一の港と説明しています[[s:pref]]。</td><td>泊まるのがおすすめ</td></tr>
</tbody></table></div>
<p class="fine">時間は上の電車の表によります。</p>

<h2>伊豆半島はいつ行くのがいいか</h2>
<p>泳ぐなら7月中旬から8月下旬。静かに過ごしたいなら、その前後の月がいちばんです。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>どんな感じか</th></tr></thead>
<tbody>
<tr><td>7月中旬〜8月下旬</td><td>伊豆の浜の正式な海水浴シーズンで[[s:jg6322]]、ライフガードがいるのもこの期間だけです[[s:funjapan]]。</td></tr>
<tr><td>5月下旬〜9月</td><td>天気がよければ海は気持ちよく[[s:jg6304]]、学校の休み以外は人も少なめです。</td></tr>
<tr><td>それ以外</td><td>町はぐっと静かになり、早く閉まる飲食店や商店も多くなります[[s:tdn]]。</td></tr>
</tbody></table></div>

<h2>伊豆で家を借りると、何が変わるか</h2>
<p>ホテルの部屋は、1〜2泊と決まった夕食の時間を前提にしています。家ならキッチン、洗濯機、仕事ができる机があるので、4泊や1週間でも無理なく過ごせます。午前は仕事、午後は浜か温泉、店が閉まったら家で夕食。だいたいそんな一日になります。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて約10分の「NODE Shimoda」のリビング。]]
<p>下田の私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、まさにこういう滞在のために整えました。ワークデスク、洗濯機と乾燥機、調理器具のそろったキッチンがあり、スマートロックでセルフチェックインできます。伊豆急下田駅から歩いて約10分で、飲食店、コンビニ、スーパーもすぐ近くです。</p>
<p>伊豆で1週間過ごして、もっと長く住むことや、自分の家を持つことが気になり始めたら、[[l:ja-akiya-try-first|家を買う前に1か月その町に住む]]ことをすすめる理由も読んでみてください。</p>
[[ed:回線速度の実測値と、浜からの最終バスの時刻を入れてください。]]

<h2>伊豆に泊まる弱点は何か</h2>
<p>移動には、少し計画が要ります。バスは本数が少なく、配車アプリは大都市のようには使えず、東京からの直通列車は午前から昼過ぎが中心です[[s:tdn]]。一日の予定は時刻表に合わせて組み、買い物は夕方までに済ませておくと楽です。浜から浜へ移動したいなら、電動自転車かレンタカーがあると、ぐっと動きやすくなります。</p>
""",
  "faq": [
    ("伊豆へ行くのに、ジャパン・レール・パスは使えますか",
     "一部で使えます。JR の区間は対象ですが、伊東〜下田の伊豆急行線は対象外で、三島〜修善寺は550円の追加料金がかかります[[s:jg6305]]。"),
    ("伊豆半島で車は必要ですか",
     "下田や修善寺へ行くだけなら要りません。車がほしくなるのは、浜から浜へ移動したいときくらいです。"),
    ("東京から下田まで、何時間かかりますか",
     "東京から伊豆急下田駅まで、直通の特急「踊り子」で約2時間35分です[[s:ekitan]]。"),
  ],
 },
},
]

# ---------------------------------------------------------------- 固定ページの文言
HOME = {
 "seo_title": "Noki | Long Stays in Small-Town Japan",
 "description": "Homes for a week, a month or a season in small-town Japan, and plain guides to akiya, remote work and life outside the big cities from the people who run them.",
}
GUIDES = {
 "h1": "Guides to long stays and akiya in Japan",
 "seo_title": "Guides to Long Stays and Akiya in Japan",
 "description": "Guides for people who want more than a holiday in Japan: akiya and old houses, month-long stays, remote work and the small towns where we run homes.",
 "dek": "For people who want more than a holiday in Japan: old houses, month-long stays, remote work and the small towns where we run homes.",
}
IZU = {
 "h1": "Izu Peninsula",
 "seo_title": "Izu Peninsula Guide: Towns, Access and Long Stays",
 "description": "The Izu Peninsula is a mountainous peninsula south-west of Tokyo with beaches on the coast and onsen towns inland. Where to base yourself and how to get there.",
 "dek": "The Izu Peninsula is a mountainous peninsula south-west of Tokyo with beaches on the coast and hot-spring towns inland. Our first homes are in Shimoda and Shuzenji.",
 "keywords": [("izu peninsula", "12,100", "7"), ("shimoda japan", "5,400", "21"), ("shuzenji", "1,000", "0")],
}
ABOUT = {
 "h1": "About Noki",
 "seo_title": "About Noki: Who Runs It and How We Write",
 "description": "Noki is written by the team behind NODE Shimoda, a home for long stays on the Izu Peninsula, for people who want more than a few nights in small-town Japan.",
 "dek": "We run NODE Shimoda, a home for long stays on the Izu Peninsula, and we write the guides we wish our guests could read before they arrive.",
}

# ---------------------------------------------------------------- 写真・施設
# 写真は photos/<名前>-<幅>.webp（大きさは build.py がファイルから読む）。
# node-shimoda と yaizu-* は自社の写真（アキヤドの images/photos から）。ほかは Unsplash の写真（PHOTO_CREDITS）。
# Unsplash の写真は場所を特定しない雰囲気の写真として使い、alt・説明文に地名を書かない（撮影地が分かっても、自社の記事の主役の場所としては使わない）。
# yaizu-* は「リフォーム前」と明記する（docs/brand/experience.md の確認済みの条件）。
NODE_URL = "https://nodeshimoda.com/"

# Unsplash の写真の出典（写真の名前 → 撮影者・撮影者ページ・写真ページ・写真ID）。2026-11-14 に download_asset でダウンロードを記録して取得。
# ページ下の「Photo credits」に、そのページで使った写真の分だけ「Photo by 撮影者 on Unsplash」を出す（build.py の footer）。
UNSPLASH_UTM = "?utm_source=noki&utm_medium=referral"
PHOTO_CREDITS = {
    "coastal-village": ("PJH", "https://unsplash.com/@dokae", "https://unsplash.com/photos/jb0SsX_Bz_E", "jb0SsX_Bz_E"),
    "window-room": ("ZENG YILI", "https://unsplash.com/@zengyili", "https://unsplash.com/photos/fta5pzyM0T8", "fta5pzyM0T8"),
    "town-lane": ("PJH", "https://unsplash.com/@dokae", "https://unsplash.com/photos/stvwZJNN6Qo", "stvwZJNN6Qo"),
    "empty-tatami-room": ("ayumi kubo", "https://unsplash.com/@ayumikubo", "https://unsplash.com/photos/IAgczbi1B-M", "IAgczbi1B-M"),
    "rocky-coast": ("Lucius Hunter", "https://unsplash.com/@lucius_x14", "https://unsplash.com/photos/a3e4znCn-0o", "a3e4znCn-0o"),
    "grilled-red-fish": ("kazuend", "https://unsplash.com/@kazuend", "https://unsplash.com/photos/lFG7xubInhE", "lFG7xubInhE"),
    "train-window-sea": ("realfish", "https://unsplash.com/@realfish", "https://unsplash.com/photos/E401NBqwIGg", "E401NBqwIGg"),
}
NODE_FACTS = [
    "About 10 minutes on foot from Izukyu-Shimoda Station",
    "Work desk, washing machine and dryer",
    "Kitchen with proper cooking equipment",
    "Self check-in with a smart lock",
    "Weekly and monthly discounts",
    "Licensed under Japan’s Hotel Business Act, open all year",
]

# 場所（"place" のキー → 名前とページ）
PLACES = {"izu": {"name": "Izu Peninsula", "page": "izu"}}
for _a in ARTICLES:
    _a["topics"] = [_a["topic"]] + (["places"] if _a.get("place") else [])
