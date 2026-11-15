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
    "mlit": ("https://www.mlit.go.jp/common/001036700.pdf", "Ministry of Land, Infrastructure, Transport and Tourism",
             "国土交通省", "MLIT, citing the 2023 Housing and Land Survey"),
    "datamax": ("https://data-max.co.jp/article/70863", "Data Max", "データ・マックス", "Data Max: vacant homes reach 9 million"),
    "housingjapan": ("https://housingjapan.com/?p=60122", "Housing Japan", "Housing Japan",
                     "Housing Japan: Can foreigners buy property in Japan?"),
    "rej": ("https://resources.realestate.co.jp/buy/what-restrictions-are-there-on-foreigners-buying-a-home-in-japan-compared-to-other-countries/",
            "Real Estate Japan", "Real Estate Japan", "Real Estate Japan: restrictions on foreign buyers"),
    "mofa": ("https://www.mofa.go.jp/j_info/visit/visa/short/novisa.html", "Ministry of Foreign Affairs of Japan", "外務省", "Ministry of Foreign Affairs of Japan: Exemption of Visa (Short-Term Stay)"),
    "isa": ("https://www.moj.go.jp/isa/applications/status/designatedactivities10_00001.html",
            "Immigration Services Agency", "出入国在留管理庁", "Immigration Services Agency: Digital Nomad status"),
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
 "description": "Japan has about nine million empty homes, and foreigners can buy them. Before you do, spend a month in the town. Here’s what it shows you that a listing can’t.",
 "dek": "Japan has about nine million empty homes, and nothing stops a foreigner from buying one. But the house is the easy part. The town is what you’re really signing up for, and a month there tells you more than any listing.",
 "card": "Japan has about nine million vacant homes and no rule against foreigners buying them. The town matters more than the house, and a month is enough to find out.",
 "keywords": [("buying an akiya in japan", "—", "—"), ("akiya", "3,600", "0")],
 "intent": "Do（比べたい・やり方）",
 "points": [
   "An akiya is an empty house. Japan had about 9.0 million of them on 1 October 2023, 13.8% of all homes.",
   "Foreigners can buy property in Japan without living here, but owning a house won’t get you a visa.",
   "A month in the town shows you what a listing can’t: the winter cold, whether you need a car, where you’ll shop and how the neighbours are.",
   "Renting a renovated older house by the week or month lets you try all of this before you sign anything.",
 ],
 "body": """
<p>An akiya (空き家) is simply a house that nobody lives in. Japan’s 2023 Housing and Land Survey counted about 9.0 million of them on 1 October 2023, or 13.8% of the country’s homes [[s:mlit]]. Around 3.85 million weren’t for rent or sale and weren’t anyone’s holiday home either. That’s the group people usually mean when they talk about Japan’s abandoned houses [[s:datamax]].</p>

<h2>Can foreigners buy an akiya?</h2>
<p>Yes. Japan doesn’t restrict property purchases by nationality or residency [[s:housingjapan]]. The catch is on the immigration side: buying a home doesn’t come with a residence visa [[s:rej]]. You can own the house and still only be allowed to stay as long as your passport permits.</p>

<h2>Why live in the town before you buy?</h2>
<p>The house is the cheap part. What you’re really committing to is the town, and a listing can only tell you so much: the price, the floor plan, a few photos. The things that decide whether you’ll be happy there only show up once you’ve lived in it for a while.</p>
<div class="tablewrap"><table>
<thead><tr><th>What you want to know</th><th>How a month shows you</th></tr></thead>
<tbody>
<tr><td>How cold an old wooden house gets in January, and what heating costs</td><td>You’ll feel it on the first cold night and see it on the electricity bill.</td></tr>
<tr><td>Whether daily life works without a car</td><td>A week of shopping and errands on foot, by bus or by bike makes it obvious.</td></tr>
<tr><td>Where you’ll buy food, and when the shops close</td><td>Cooking most of your own meals soon shows you what’s easy to find and what isn’t.</td></tr>
<tr><td>How rubbish sorting works on that street</td><td>You’ll be following the local collection calendar like everyone else. If city hall has an English version, it’s worth asking for.</td></tr>
<tr><td>Whether the internet holds up for a working day</td><td>Normal working hours, video calls included, are the real test.</td></tr>
<tr><td>What humid months and typhoons do to the building</td><td>Neighbours and local builders know what tends to fail first in houses like it.</td></tr>
<tr><td>How the neighbourhood treats a newcomer</td><td>Saying hello, joining a clean-up day if there is one, and asking how other newcomers settled in will tell you a lot.</td></tr>
</tbody></table></div>
<p>None of this comes up in a viewing.</p>

<h2>How long can you stay in Japan to test a town?</h2>
<p>Long enough for a proper trial. Most visa-exempt nationalities can stay up to 90 days as short-term visitors, though a few get 15 or 30 days and some passports come with extra conditions [[s:mofa]]. It’s worth checking the rule for your own passport before you plan.</p>
<p>If you work remotely, there’s a second option. Japan’s Digital Nomad status lets you stay for six months. It can’t be renewed, and you’ll need an annual income of at least 10 million yen and private medical insurance [[s:isa]].</p>

<h2>What does a trial month look like?</h2>
<ol>
<li><strong>Week one: settle in.</strong> This is the week for finding the supermarket, the clinic and the bus stop, and for working out the rubbish calendar.</li>
<li><strong>Week two: live normally.</strong> Work your usual hours, cook, and notice what starts to bother you.</li>
<li><strong>Week three: ask around.</strong> It’s a good time to visit the city hall desk that handles empty houses, talk to a local agent and ask the neighbours what they’d fix first.</li>
<li><strong>Week four: decide.</strong> By now you’ll know what would need to change, both about the house and about the way you live.</li>
</ol>

<h2>Can you stay in a renovated older house before buying one?</h2>
<p>Yes, and it’s the most direct way to find out what living in one is really like, without signing anything. Towns within reach of Tokyo are the easiest to test. The Izu Peninsula, for example, is two to three hours away, as our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] explains.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, our home in Shimoda’s old town.]]
<p>Our home, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is in the old town of Shimoda, on the [[l:izu|Izu Peninsula]]. It’s an older house renovated for long stays, and it’s licensed under Japan’s Hotel Business Act, so it can take guests all year round. Longer stays get weekly and monthly discounts. Most of our guests so far have come from Europe and North America, and many of them work remotely.</p>
[[ed:Confirm before publishing: the monthly rate, whether stays of 30 nights or more can always be accepted, and whether we may call the Shimoda house a restored akiya. Add Shuzenji and Yaizu once their status is fixed.]]
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
   ("Is a cheap house in Japan really cheap?",
    "Not always. The purchase price is only one part of the bill. Renovation, taxes, insurance and upkeep come on top, and they vary a lot from one building to the next, so it’s worth getting written quotes before you commit."),
   ("Does owning a house in Japan help me get a visa?",
    "No. In Japan, owning property and immigration status are completely separate [[s:rej]]."),
   ("How many akiya are there in Japan?",
    "About 9.0 million homes were empty on 1 October 2023, which is 13.8% of all housing, according to Japan’s 2023 Housing and Land Survey [[s:mlit]]."),
 ],
 "sources": ["mlit", "datamax", "housingjapan", "rej", "isa", "mofa"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "日本で空き家を買う前に、まず1か月住んでみる",
  "dek": "日本には約900万戸の空き家があり、外国人が買うのを止める決まりもありません。でも、家を買うのは簡単なほうです。本当に引き受けるのは町のほうで、そこで1か月暮らすと、物件情報よりずっと多くのことが分かります。",
  "review": [
   "【2026-11-15 トーンの書き直し】説明書のような命令文の連続をやめ、現地に住む友人が話すような文にしました（英語は短縮形と you / we を使う形に）。日本語版も、硬い言い回しをやめて自然な話し言葉寄りにしました。数字・出典・主張は変えていません",
   "【2026-11-15 の見直しで変えた点（見せ方）】「akiya とは」の見出しをなくし、最初の段落にまとめました（これから書く「akiya とは」の記事と役割が重ならないように）。7つの確かめることを「何を確かめるか／1か月でどう確かめるか」の表にしました。自社の家の節の見出しを、読み手の疑問の形（「買う前に、改修した古い家に泊まれるか」）にして、東京からの行き方の記事へのリンクを足しました。狙う検索語の先頭を「buying an akiya in japan」に変えました",
   "【変えた点（言い方を確認済みの範囲にした・出典を足した）】①「静岡の小さな町で家を管理している」→ NODE Shimoda だけを書く形に（ほかの施設は公開しない決まりのため）②「家の売買や仲介はしていません」を消しました（RIVIA は空き家の買取にも対応しているので、言い切ってよいか分からないため）③焼津の写真の説明「私たちの家の1つ」→「焼津・鰯ヶ島の古い家（リフォーム前）」④ビザ免除の短期滞在を、外務省のページどおり「多くは90日、15日や30日の国もある」に直し、外務省を出典に足しました",
   "【人に確かめてほしい点】①「買う前に1か月暮らす」という切り口が、実際のゲストの動機と合っているか ②「家の売買や仲介はしない」と書きたいか（書く場合は事実か） ③月額料金、30泊以上を常に受けられるか、「再生した空き家」と呼んでよいか（黄色い枠） ④デジタルノマドの条件（年収・保険・6か月・更新不可）が、出入国在留管理庁の最新の条件と合っているか（ビザの記述は公開前に人の確認が必要）",
   "【まだ入れていないこと（確認待ち）】1か月泊まれる場所の比べ方（自治体のお試し住宅など）、空き家の数の出典を総務省統計局の確報に差し替えること、下田の宿を開いたときの体験（古い配線・回線工事の待ち）を書く節。確認できてから足します",
  ],
  "points": [
    "akiya（空き家）は、人が住んでいない家のこと。2023年10月1日時点で約900万戸、住宅全体の13.8%ありました。",
    "外国人は、日本に住んでいなくても家を買えます。ただ、家を持ってもビザはもらえません。",
    "町で1か月暮らすと、物件情報では分からないことが見えてきます。冬の寒さ、車が要るか、どこで買い物するか、近所の人のこと。",
    "改修した古い家を週単位・月単位で借りれば、何も契約しないうちに、全部試せます。",
  ],
  "body": """
<p>akiya（空き家）は、ひとことで言えば、誰も住んでいない家のことです。2023年の住宅・土地統計調査では、2023年10月1日時点で約900万戸、日本の住宅の13.8%が空き家でした[[s:mlit]]。そのうち約385万戸は、貸すためでも売るためでもなく、別荘でもない家です。「日本の放置された家」と言うとき、たいていはこの家のことを指しています[[s:datamax]]。</p>

<h2>外国人は空き家を買えるのか</h2>
<p>買えます。日本では、国籍や在留資格によって不動産の購入が制限されることはありません[[s:housingjapan]]。気をつけたいのは在留のほうで、家を買っても在留資格は付いてきません[[s:rej]]。家を持っていても、いられる期間はパスポートで決まる範囲のままです。</p>

<h2>なぜ、買う前にその町で暮らすのか</h2>
<p>家は、安いほうの買い物です。本当に引き受けるのは町のほうで、物件情報から分かるのは、価格と間取りと何枚かの写真くらい。そこで楽しく暮らせるかを決めることは、しばらく住んでみて初めて見えてきます。</p>
<div class="tablewrap"><table>
<thead><tr><th>知りたいこと</th><th>1か月暮らすと、こう分かる</th></tr></thead>
<tbody>
<tr><td>古い木造の家が1月にどれくらい寒いか、暖房にいくらかかるか</td><td>最初の寒い夜に体で分かり、電気代の請求で数字でも分かります。</td></tr>
<tr><td>車なしで毎日の暮らしが回るか</td><td>1週間、買い物や用事を徒歩・バス・自転車で済ませてみると、はっきりします。</td></tr>
<tr><td>どこで食料を買うか、店は何時に閉まるか</td><td>食事をほとんど自炊していると、手に入りやすいものとそうでないものが、すぐに分かります。</td></tr>
<tr><td>その通りのごみの分別の仕組み</td><td>地域の収集カレンダーに合わせて、みんなと同じように出すことになります。役所に英語版があれば、もらっておくと便利です。</td></tr>
<tr><td>一日仕事をしても回線がもつか</td><td>ビデオ会議も含めて、いつもどおりに働いてみるのが一番の確かめ方です。</td></tr>
<tr><td>湿気の多い時期や台風で、建物がどうなるか</td><td>同じような家でどこから傷みやすいかは、近所の人や地元の工務店がよく知っています。</td></tr>
<tr><td>新しく来た人を、近所がどう迎えるか</td><td>あいさつをしたり、清掃の日があれば参加したり、先に移ってきた人にどうなじんだかを聞いたりすると、よく分かります。</td></tr>
</tbody></table></div>
<p>どれも、内見では出てこないことばかりです。</p>

<h2>町を試すために、日本にどれくらいいられるのか</h2>
<p>しっかり試せるくらいの長さはあります。ビザ免除の国・地域の多くは、短期滞在として90日までいられます。ただ、15日や30日の国もあり、パスポートに条件が付く場合もあります[[s:mofa]]。計画する前に、自分のパスポートの条件を確かめておくと安心です。</p>
<p>リモートで働いているなら、もう一つ方法があります。日本の「デジタルノマド」の在留資格なら、6か月滞在できます。更新はできず、年収1,000万円以上と民間の医療保険が必要です[[s:isa]]。</p>

<h2>お試しの1か月は、どんなふうに過ぎるか</h2>
<ol>
<li><strong>1週目：落ち着く。</strong>スーパー、診療所、バス停を見つけて、ごみの収集日を覚える週です。</li>
<li><strong>2週目：いつもどおりに暮らす。</strong>いつもの時間に働いて、料理をして、気になり始めたことに目を向けます。</li>
<li><strong>3週目：聞いてまわる。</strong>役所の空き家の窓口に行ったり、地元の不動産屋と話したり、近所の人に「最初に直すならどこか」を聞いたりするのに、ちょうどいい頃です。</li>
<li><strong>4週目：決める。</strong>この頃には、家について、そして自分の暮らし方について、何を変える必要があるかが分かっています。</li>
</ol>

<h2>買う前に、改修した古い家に泊まれるか</h2>
<p>泊まれます。古い家での暮らしが本当はどんなものかを、何も契約せずに確かめる、いちばんの近道です。東京から行きやすい町のほうが試しやすく、たとえば伊豆半島なら2〜3時間で行けます（[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]）。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|下田の旧町内にある私たちの家「NODE Shimoda」のリビング。]]
<p>私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、[[l:izu|伊豆半島]]の下田の旧町内にあります。長期滞在向けに改修した古い家で、旅館業法の許可を受けているので、一年中泊まれます。長く泊まるほど、週割・月割が付きます。これまでのゲストは欧米の人が中心で、リモートで働いている人がたくさんいます。</p>
[[ed:公開前に要確認：月額料金、30泊以上を常に受けられるか、下田の家を「再生した空き家」と呼んでよいか。修善寺と焼津は、状況が決まってから足してください。]]
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
    ("日本の安い家は、本当に安いのですか",
     "そうとは限りません。購入価格は、かかるお金の一部です。改修、税金、保険、維持費が上乗せされ、金額は建物によって大きく変わるので、決める前に書面で見積もりを取っておくと安心です。"),
    ("日本で家を持つと、ビザを取りやすくなりますか",
     "なりません。日本では、不動産を持つことと在留資格は、まったく別の話です[[s:rej]]。"),
    ("日本に空き家は何戸ありますか",
     "2023年の住宅・土地統計調査によると、2023年10月1日時点で約900万戸、住宅全体の13.8%が空き家でした[[s:mlit]]。"),
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
 "description": "Noki is run by the team that operates small homes for long stays in Shizuoka, Japan. Who we are, how our guides are sourced and how to reach us.",
 "dek": "Noki is written by the team that runs the homes. This page says who we are, how the guides are put together and how to tell us we got something wrong.",
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
