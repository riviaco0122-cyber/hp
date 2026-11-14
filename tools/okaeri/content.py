# -*- coding: utf-8 -*-
"""Okaeri Japan の記事・ページのデータ。HTML は直接書き換えず、ここを直して build.py を実行する。

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
# テーマ別の一覧ページ（/okaeri/akiya.html など）は、公開記事が3本以上になったテーマだけ自動で作る（薄い一覧を作らないため）
# 読み手の入口は「どこまで日本に深く関わるか」の1本の軸で分ける（重ならず、漏れない）:
#   stay = 旅行者として1週間〜1か月滞在する ／ live = 一年の一部を暮らす（数か月・毎年・仕事をしながら）／ own = 家を持つ（空き家を買う・直す・運営する）
# 記事は必ずこの3つのどれか1つ（"topic"）に入れる。ほかの段階の読み手にも役立つ記事は "also" に足す（一覧の「こちらも役立つ」に出る）。
# 場所（places）は別の軸。記事に "place" があれば場所の一覧にも出る。
TOPICS = {
    "stay": {"kind": "plan", "name": "Stay longer", "ja": "長めに旅する", "photo": "window-room",
             "photo_alt": "Two low chairs and a small table by a window with paper screens, looking out over water",
             "path_label": "A longer trip", "path_desc": "A week to a month as a visitor: towns, food, getting there.",
             "path_ja": "長めの旅（旅行者として1週間〜1か月）",
             "seo_title": "Slow Travel in Small-Town Japan: Week- and Month-Long Trips",
             "description": "Guides for travellers who want a week or a month in one small Japanese town instead of a different city every night: access, seasons, food and where to stay.",
             "intro": "For a week or a month as a visitor. One town instead of a different hotel every night: how to get there, when to go, what to eat and how a house changes the trip.",
             "coming": ["Shimoda for a week or longer", "The Japanese countryside for a longer stay"]},
    "live": {"kind": "plan", "name": "Live part-time", "ja": "一年の一部を暮らす", "photo": "town-lane",
             "photo_alt": "Quiet paved lane between hedges and low houses, with green hills behind",
             "path_label": "Living here part of the year", "path_desc": "Months at a time, or every year: remote work, visas, monthly homes.",
             "path_ja": "一年の一部を暮らす（数か月・毎年・仕事をしながら）",
             "seo_title": "Living in Japan Part-Time: Long Stays, Visas, Remote Work",
             "description": "How to live in small-town Japan for months at a time or every year: how long you can stay, Japan’s digital nomad visa, monthly homes and working remotely.",
             "intro": "For months at a time, or a season every year. How long you can stay, Japan’s digital nomad visa, renting a home by the month and working remotely from a small town.",
             "coming": ["Renting a house in Japan for a month", "Japan’s digital nomad visa, and where to base yourself", "How long can you stay in Japan?"]},
    "own": {"kind": "plan", "name": "Own a home", "ja": "家を持つ", "photo": "empty-tatami-room",
            "photo_alt": "Empty tatami room in an old wooden house, with sliding windows open to a garden",
            "path_label": "Owning a home here", "path_desc": "Buying, restoring or running an akiya.",
            "path_ja": "家を持つ（空き家を買う・直す・運営する）",
            "seo_title": "Akiya in Japan: Buying, Restoring and Owning an Old House",
            "description": "Plain guides to owning an akiya, one of Japan’s vacant houses: who can buy one, what it really costs, restoring it and testing the town before you commit.",
            "intro": "Japan has about nine million empty homes, and foreigners can buy them. The listings are the easy part. These guides cover what an akiya really costs, what owning one does and does not give you, and how to try a town before you sign.",
            "coming": ["Can foreigners buy property in Japan?", "What is an akiya?", "Cheap and free houses in Japan: the real cost", "Akiya banks explained"]},
    "places": {"kind": "place", "name": "Places", "ja": "場所", "photo": "rocky-coast",
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
 "published": "2026-11-14", "updated": "2026-11-14",
 "kicker": "Food and port towns",
 "h1": "Kinmedai: Japan’s golden-eye snapper and where to eat it",
 "seo_title": "Kinmedai: Japan’s Golden-Eye Snapper and Where to Eat It",
 "description": "Kinmedai is a red, golden-eyed deep-sea fish eaten simmered, seared or raw. What it is and why Shimoda, Japan’s top landing port, is the place to try it.",
 "dek": "Kinmedai is the red, golden-eyed fish on sushi counters and ryokan tables across Japan. Here is what it is, how it is eaten and why the port of Shimoda is the place to try it.",
 "card": "What kinmedai is, how Japan cooks it and why Shimoda, the port that lands more of it than any other, is worth staying the night for.",
 "keywords": [("kinmedai", "4,400", "0"), ("shimoda japan", "5,400", "21")],
 "intent": "Know（知りたい）",
 "points": [
  "Kinmedai is a deep-sea fish with red skin and large golden eyes. In English it is sold as splendid alfonsino or golden-eye snapper.",
  "Shimoda, at the southern tip of the Izu Peninsula, is Japan’s top landing port for it, according to the city and Shizuoka Prefecture.",
  "The classic dish is nitsuke, a whole fish simmered in sweet soy. A canteen inside the fish market opens at 7:00.",
  "June is festival month. Winter is the other season locals name.",
 ],
 "body": """
<h2>What is kinmedai?</h2>
<p>Kinmedai is a deep-sea fish with red skin and large golden eyes, known in English as splendid alfonsino (<em>Beryx splendens</em>) or golden-eye snapper. It lives around 500 metres down [[s:tabimag]]. Shimoda’s city newsletter describes eyes that shine gold and skin that turns red all over about 40 minutes after the fish is landed [[s:shimoda_news]].</p>
<p>The name is written 金目鯛, literally “golden-eye sea bream”, but kinmedai is neither a sea bream nor a snapper. The flesh is white and carries fat all year, which is why it works simmered, raw or seared.</p>

<h2>Why is Shimoda the place to eat kinmedai?</h2>
<p>Shimoda lands more kinmedai than any other port in Japan. Both the city and Shizuoka Prefecture describe it that way [[s:shimoda_news,pref]].</p>
<p>Menus in town often name one of two kinds. <em>Jikinme</em> is caught in nearby waters, between Oshima and Kozushima. <em>Oki-kinme</em> comes from fishing grounds further out [[s:tvtokyo]]. Ordering both side by side is the quickest way to taste the difference.</p>

<h2>How is kinmedai eaten?</h2>
<ul>
<li><strong>Nitsuke.</strong> A whole fish or a thick cut simmered in soy sauce and sugar. This is the dish most people come for.</li>
<li><strong>Sashimi and aburi.</strong> Raw slices, or slices with the skin seared.</li>
<li><strong>Shabu-shabu.</strong> Thin slices swished through hot broth at the table.</li>
<li><strong>Everything else.</strong> The local tourism association also lists kinmedai ramen, burgers and croquettes [[s:tabimag]].</li>
</ul>

<h2>Where can you try kinmedai by the harbour?</h2>
<p>Ichiba no Shokudo Kinmetei is a canteen inside the Shimoda fish market, about ten minutes on foot from Izukyu-Shimoda Station. Shizuoka Prefecture lists its hours as 7:00 to 9:30 for the morning set and 11:00 to 15:00 for lunch, closed on Tuesdays ([[a:pref]], page updated March 2025). Hours change, so check before you walk over.</p>
[[ed:Add the two or three places we actually send guests, with walking time from the house and what we order there.]]

<h2>When is the best time to eat kinmedai?</h2>
<p>There are two answers. Winter is often called the season. The city newsletter adds that June, just before spawning, is said to be when the fish is fattiest [[s:shimoda_news]].</p>
<p>June is also the Shimoda Kinme Matsuri, which runs from 1 to 30 June every year. During the festival you can watch the landings from a viewing area beside the market, roughly 7:30 to 9:00. Boats do not go out on Tuesdays or Saturdays, or after rough seas [[s:tabimag]].</p>

<h2>Why stay overnight instead of visiting for the day?</h2>
<p>The market does its business early, and the direct Odoriko limited express from Tokyo takes about 2 hours 35 minutes [[s:ekitan]]. A day trip arrives after the boats have unloaded. Staying in town puts you at the harbour for the morning landings and at the canteen when it opens. Routes and fares are in our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]].</p>
<p>Our home in Shimoda’s old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is about ten minutes on foot from the station. It has a kitchen with proper cooking equipment and a supermarket within walking distance, so you can cook what you find.</p>
[[ed:Name where guests can buy kinmedai to cook at home.]]
""",
 "faq": [
  ("Is kinmedai the same as red snapper?",
   "No. Kinmedai is an alfonsino, a different family of fish from the snappers. The English name golden-eye snapper is a market name."),
  ("What does kinmedai taste like?",
   "Kinmedai has white flesh that carries fat all year, so it stays rich whether it is simmered, seared or eaten raw. The classic preparation is nitsuke, simmered in soy sauce and sugar."),
  ("Where is kinmedai caught?",
   "Shimoda, on the Izu Peninsula in Shizuoka Prefecture, lands more kinmedai than any other port in Japan. The fish sold there as jikinme is caught in nearby waters between Oshima and Kozushima."),
  ("How do you say kinmedai?",
   "Roughly “kin-meh-dye”. Locals shorten it to <em>kinme</em>."),
 ],
 "sources": ["shimoda_news", "pref", "tabimag", "tvtokyo", "ekitan"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "金目鯛とは：日本の「ゴールデンアイ・スナッパー」と、食べられる場所",
  "dek": "金目鯛は、日本中の寿司屋や旅館で出てくる、赤い皮と金色の目の魚です。どんな魚か、どう食べるか、なぜ下田の港で食べるのがよいかをまとめます。",
  "review": [
   "題名を「下田の金目鯛」から「金目鯛とは」に広げました。検索する人の多くは「kinmedai とは何か」を知りたい人で、下田を知らないためです。下田の話は本文の主役のままです",
   "金目鯛の説明や食べ方に、地元の感覚とずれている点がないか",
   "紹介している店（市場の食堂 金目亭）を載せてよいか。ほかに必ず案内している店があるか",
   "金目鯛の写真がまだありません。料理か水揚げの自社撮影の写真があると、この記事はずっと強くなります",
  ],
  "points": [
   "金目鯛は、赤い皮と大きな金色の目を持つ深海魚です。英語では splendid alfonsino または golden-eye snapper の名前で売られています。",
   "伊豆半島の南端にある下田は、金目鯛の水揚げが日本一の港です（下田市と静岡県の説明による）。",
   "定番は煮付けです。魚市場の中の食堂は朝7時に開きます。",
   "6月は祭りの月です。地元では冬も旬とされています。",
  ],
  "body": """
<h2>金目鯛とはどんな魚か</h2>
<p>金目鯛は、赤い皮と大きな金色の目を持つ深海魚です。英語では splendid alfonsino（学名 <em>Beryx splendens</em>）または golden-eye snapper と呼ばれます。水深500メートル前後にすんでいます[[s:tabimag]]。下田市の広報は、目が金色に輝き、水揚げから40分ほどで全身が赤くなると説明しています[[s:shimoda_news]]。</p>
<p>名前は「金目鯛」と書きますが、鯛の仲間でもスナッパー（フエダイ）の仲間でもありません。身は白身で一年を通して脂があるため、煮ても、生でも、炙ってもおいしく食べられます。</p>

<h2>なぜ下田で食べるのがよいのか</h2>
<p>下田は金目鯛の水揚げが日本で最も多い港です。下田市と静岡県の両方がそう説明しています[[s:shimoda_news,pref]]。</p>
<p>町のメニューには2つの呼び名がよく出てきます。「地金目」は大島から神津島にかけての近海でとれたもの、「沖金目」は遠くの漁場でとれたものです[[s:tvtokyo]]。両方を並べて頼むと、違いがすぐ分かります。</p>

<h2>金目鯛はどう食べるのか</h2>
<ul>
<li><strong>煮付け。</strong>丸ごと、または厚い切り身を醤油と砂糖で煮ます。多くの人がこれを目当てに来ます。</li>
<li><strong>刺身と炙り。</strong>生の切り身、または皮目を炙った切り身です。</li>
<li><strong>しゃぶしゃぶ。</strong>薄切りを卓上の出汁にくぐらせます。</li>
<li><strong>そのほか。</strong>観光協会は、金目鯛のラーメン、バーガー、コロッケも挙げています[[s:tabimag]]。</li>
</ul>

<h2>港の近くで食べられる店</h2>
<p>「市場の食堂 金目亭」は下田市魚市場の中にある食堂で、伊豆急下田駅から歩いて約10分です。静岡県のページでは、営業時間は朝定食が7時〜9時30分、昼が11時〜15時、火曜定休となっています（[[a:pref]]、2025年3月更新）。営業時間は変わることがあるので、行く前に確認してください。</p>
[[ed:実際にゲストへ案内している店を2〜3軒、家からの徒歩時間と、そこで頼むものを添えて入れてください。]]

<h2>いつ食べに行くのがよいか</h2>
<p>答えは2つあります。旬は冬と言われることが多いです。下田市の広報は、産卵前の6月ごろが最も脂が乗る時期とも言われる、と書いています[[s:shimoda_news]]。</p>
<p>6月は「下田きんめ祭り」の月でもあり、毎年6月1日から30日まで開かれます。期間中は、市場の横の見学エリアから水揚げを見られます。時間は7時30分から9時ごろです。火曜と土曜、しけの後は漁が休みです[[s:tabimag]]。</p>

<h2>日帰りではなく泊まる理由</h2>
<p>市場は朝早くに動きます。東京からの直通特急「踊り子」は約2時間35分かかります[[s:ekitan]]。日帰りでは、着くころには水揚げが終わっています。町に泊まれば、朝の水揚げを港で見て、開店と同時に食堂に入れます。行き方と運賃は[[l:izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田の旧町内にある私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、駅から歩いて約10分です。調理器具のそろったキッチンがあり、スーパーも徒歩圏なので、買った魚を自分で料理できます。</p>
[[ed:ゲストが金目鯛を買える店の名前を入れてください。]]
""",
  "faq": [
   ("金目鯛はレッドスナッパー（鯛の仲間）と同じですか", "違います。金目鯛はキンメダイ科の魚で、フエダイ（スナッパー）の仲間ではありません。golden-eye snapper は流通上の呼び名です。"),
   ("金目鯛はどんな味ですか", "一年を通して脂のある白身で、煮ても、炙っても、生でも濃い味わいがあります。定番は、醤油と砂糖で煮る煮付けです。"),
   ("金目鯛はどこでとれますか", "静岡県の伊豆半島にある下田は、金目鯛の水揚げが日本一の港です。「地金目」として売られる魚は、大島から神津島にかけての近海でとれたものです。"),
   ("kinmedai はどう発音しますか", "英語話者には “kin-meh-dye” が近い音です。地元では「キンメ」と略します。"),
  ],
 },
},
# ============================================================ 空き家
{
 "id": "akiya-try-first", "slug": "akiya-try-before-you-buy", "topic": "own", "place": None, "also": ["live"],
 "photo": ("yaizu-engawa", "Old wooden house with a long veranda and an overgrown garden", "One of our houses, in Iwashigashima, Yaizu, before renovation."),
 "published": "2026-11-14", "updated": "2026-11-14",
 "kicker": "Own a home",
 "h1": "Buying an akiya in Japan? Live in one for a month first",
 "seo_title": "Buying an Akiya in Japan? Live in One for a Month First",
 "description": "Japan has about nine million vacant homes and foreigners can buy them. Before you do, spend a month in the town. What a trial stay shows that a listing cannot.",
 "dek": "Japan has about nine million vacant homes and no rule against foreigners buying them. The town matters more than the house, and a month is enough to find out.",
 "card": "Japan has about nine million vacant homes and no rule against foreigners buying them. The town matters more than the house, and a month is enough to find out.",
 "keywords": [("akiya", "3,600", "0"), ("cheap houses in japan", "1,900", "4"), ("akiya japan", "1,300", "7")],
 "intent": "Do（比べたい・やり方）",
 "points": [
  "An akiya is a vacant house in Japan. There were about 9.0 million of them, 13.8% of all homes, on 1 October 2023.",
  "Foreigners can buy property in Japan without residency. Owning a house does not give you a visa.",
  "A month in a town shows what a listing cannot: winter cold, driving, shopping and neighbours.",
  "We run homes you can stay in by the week or month. We do not sell houses.",
 ],
 "body": """
<h2>What is an akiya?</h2>
<p>An akiya (空き家) is a house in Japan that nobody lives in. Japan’s 2023 Housing and Land Survey counted about 9.0 million vacant homes on 1 October 2023, or 13.8% of the housing stock [[s:mlit]]. About 3.85 million of those were neither for rent or sale nor used as second homes, which is the group people usually mean when they talk about abandoned houses [[s:datamax]].</p>

<h2>Can foreigners buy an akiya?</h2>
<p>Yes. Japan places no nationality or residency requirement on buying property [[s:housingjapan]]. The catch is on the immigration side: buying a home does not entitle you to a residence visa [[s:rej]]. You can own the house and still be limited to the stay your passport allows.</p>

<h2>Why live in the town before buying an akiya?</h2>
<p>The house is the cheap part. The commitment is the town. A listing tells you the price and the floor plan. It does not tell you any of these:</p>
<ul>
<li>How cold an old wooden house is in January, and what heating it costs you.</li>
<li>Whether daily life works without a car.</li>
<li>Where you buy food, and what time the shops close.</li>
<li>How rubbish sorting and collection days work on that street.</li>
<li>Whether your internet connection holds up for a working day.</li>
<li>What the humid months and typhoon season do to the building.</li>
<li>How the neighbours and the neighbourhood association treat a newcomer.</li>
</ul>
<p>You can learn all seven in a month. You cannot learn any of them in a viewing.</p>

<h2>How long can you stay in Japan to test a town?</h2>
<p>Visitors from visa-exempt countries can generally stay up to 90 days as short-term visitors. Check the rule for your own passport with Japan’s Ministry of Foreign Affairs before you plan.</p>
<p>Remote workers have a second route. Japan’s Digital Nomad status allows a stay of six months. It cannot be renewed, and it requires annual income of at least 10 million yen and private medical insurance [[s:isa]].</p>

<h2>What does a trial month in an akiya town look like?</h2>
<ol>
<li><strong>Week one: settle.</strong> Find the supermarket, the clinic, the bus stop. Work out the rubbish calendar.</li>
<li><strong>Week two: live normally.</strong> Work your usual hours. Cook. Notice what annoys you.</li>
<li><strong>Week three: ask.</strong> Visit the city hall desk that handles vacant houses. Talk to a local agent. Ask neighbours what they would fix first.</li>
<li><strong>Week four: decide.</strong> Write down what you would need to change about the house and about your own habits.</li>
</ol>

<h2>Where does Okaeri Japan come in?</h2>
<p>We look after homes in small towns in Shizuoka and open them to guests for a week, a month or longer. Staying in one is a way to test a town without signing anything. We do not sell houses or act as agents.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, our home in Shimoda’s old town.]]
<p>The first, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is in the old town of Shimoda, on the [[l:izu|Izu Peninsula]]: an older house renovated for long stays and licensed as a lodging under Japan’s Hotel Business Act, so it can take guests all year. Longer stays get weekly and monthly discounts. Most guests so far have come from Europe and North America, many of them working remotely.</p>
[[ed:Confirm before publishing: the monthly rate, whether stays of 30 nights or more can always be accepted, and whether we may call the Shimoda house a restored akiya. Add Shuzenji and Yaizu once their status is fixed.]]
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
  ("Is a cheap house in Japan really cheap?",
   "The purchase price is one line of the bill. Renovation, taxes, insurance and upkeep are the others, and they vary with the building. Get written quotes before you commit."),
  ("Does owning a house in Japan help me get a visa?",
   "No. Property ownership and immigration status are separate in Japan [[s:rej]]."),
  ("How many akiya are there in Japan?",
   "About 9.0 million homes were vacant on 1 October 2023, which is 13.8% of all housing, according to Japan’s 2023 Housing and Land Survey [[s:mlit]]."),
 ],
 "sources": ["mlit", "datamax", "housingjapan", "rej", "isa"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "日本で空き家を買う前に、まず1か月住んでみる",
  "dek": "日本には約900万戸の空き家があり、外国人の購入を禁じる決まりもありません。大事なのは家より町で、1か月あれば確かめられます。",
  "review": [
   "「買う前に1か月暮らす」という切り口が、実際のゲストの動機と合っているか",
   "「売買や仲介はしない」と書いてよいか",
   "月額料金、30泊以上を常に受けられるか、「再生した空き家」と呼んでよいかは未確認です",
   "ビザ免除の短期滞在90日の説明は、公開前に外務省の最新情報で確認が必要",
  ],
  "points": [
   "akiya（空き家）は、日本で人が住んでいない家のことです。2023年10月1日時点で約900万戸、住宅全体の13.8%ありました。",
   "外国人は、在留資格がなくても日本の不動産を買えます。ただし、家を持ってもビザは得られません。",
   "町に1か月住むと、物件情報では分からないことが分かります。冬の寒さ、車の要否、買い物、近所づきあいです。",
   "私たちは週単位・月単位で滞在できる家を運営しています。家の売買はしていません。",
  ],
  "body": """
<h2>akiya とは何か</h2>
<p>akiya（空き家）は、日本で誰も住んでいない家のことです。2023年の住宅・土地統計調査では、2023年10月1日時点の空き家は約900万戸で、住宅全体の13.8%でした[[s:mlit]]。そのうち約385万戸は、賃貸用・売却用でも別荘でもない家です。「放置された家」と言うとき、多くの人が指しているのはこの部分です[[s:datamax]]。</p>

<h2>外国人は空き家を買えるのか</h2>
<p>買えます。日本では、不動産の購入に国籍や在留資格の条件はありません[[s:housingjapan]]。注意が要るのは在留の側です。家を買っても、在留資格は得られません[[s:rej]]。家を所有していても、滞在できる期間はパスポートで決まる範囲のままです。</p>

<h2>なぜ空き家を買う前にその町に住むのか</h2>
<p>安いのは家の方です。本当に引き受けるのは町の方です。物件情報で分かるのは価格と間取りで、次のことは分かりません。</p>
<ul>
<li>古い木造の家が1月にどれくらい寒いか、暖房にいくらかかるか。</li>
<li>車なしで毎日の暮らしが回るか。</li>
<li>食料をどこで買うか、店は何時に閉まるか。</li>
<li>その通りのごみの分別と収集日がどうなっているか。</li>
<li>一日仕事をしても回線が安定しているか。</li>
<li>湿気の多い時期と台風の季節に、建物がどうなるか。</li>
<li>近所の人と町内会が、新しく来た人をどう迎えるか。</li>
</ul>
<p>この7つは、1か月あれば全部分かります。内見では1つも分かりません。</p>

<h2>町を試すために、日本にどれくらい滞在できるか</h2>
<p>ビザ免除の対象国からの訪問者は、短期滞在として原則90日まで滞在できます。計画の前に、自分のパスポートの条件を日本の外務省の情報で確認してください。</p>
<p>リモートワーカーにはもう一つ方法があります。日本の「デジタルノマド」の在留資格は6か月の滞在を認めています。更新はできず、年収1,000万円以上と民間の医療保険が条件です[[s:isa]]。</p>

<h2>空き家のある町でのお試しの1か月はどう進むか</h2>
<ol>
<li><strong>1週目：落ち着く。</strong>スーパー、診療所、バス停を見つけます。ごみの収集日を把握します。</li>
<li><strong>2週目：普段どおりに暮らす。</strong>いつもの時間に働き、料理をします。不便に感じたことを書き留めます。</li>
<li><strong>3週目：聞く。</strong>市役所の空き家担当の窓口へ行きます。地元の不動産業者と話します。近所の人に、最初に直すならどこかを聞きます。</li>
<li><strong>4週目：決める。</strong>家について変える必要があること、自分の習慣について変える必要があることを書き出します。</li>
</ol>

<h2>Okaeri Japan ができること</h2>
<p>私たちは静岡の小さな町で家を管理し、1週間、1か月、またはそれ以上の滞在に開いています。そこに泊まることは、何も契約せずに町を試す方法になります。家の売買や仲介はしていません。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|下田の旧町内にある私たちの家「NODE Shimoda」のリビング。]]
<p>1軒目の「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、[[l:izu|伊豆半島]]の下田の旧町内にあります。長期滞在向けに改修した古い家で、旅館業法の許可を受けているため、一年を通して泊まれます。長く泊まるほど、週割・月割が付きます。これまでのゲストは欧米からの人が中心で、リモートワークをしている人が多くいます。</p>
[[ed:公開前に要確認：月額料金、30泊以上を常に受けられるか、下田の家を「再生した空き家」と呼んでよいか。修善寺と焼津は、状況が決まってから足してください。]]
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
   ("日本の安い家は、本当に安いのですか", "購入価格は費用の一部です。改修、税金、保険、維持費が別にかかり、金額は建物によって変わります。決める前に、書面で見積もりを取ってください。"),
   ("日本で家を持つとビザを取りやすくなりますか", "なりません。日本では、不動産の所有と在留資格は別の制度です[[s:rej]]。"),
   ("日本に空き家は何戸ありますか", "2023年の住宅・土地統計調査によると、2023年10月1日時点で約900万戸、住宅全体の13.8%が空き家でした[[s:mlit]]。"),
  ],
 },
},
# ============================================================ 伊豆
{
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-14",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, fares and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Fares and Where to Stay",
 "description": "How to get from Tokyo to the Izu Peninsula by train, with times and fares to Atami, Ito, Shimoda and Shuzenji, the best season and why a house beats a day trip.",
 "dek": "The south of the Izu Peninsula is too far for a day and just right for a week. Routes, fares, seasons and the drawbacks nobody mentions.",
 "card": "Train routes, times and fares from Tokyo to Atami, Ito, Shimoda and Shuzenji, plus the seasons and the drawbacks nobody mentions.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—"), ("izu peninsula", "12,100", "7")],
 "intent": "Do（やり方を知りたい）",
 "points": [
  "Shimoda is about 2 hours 35 minutes from Tokyo by direct limited express. That is more than five hours of train for a day trip.",
  "Shuzenji is about two hours away, by direct limited express or by Shinkansen to Mishima and a 35-minute local line.",
  "The official swimming season runs from mid-July to the end of August. Lifeguards work only in that window.",
  "Buses are infrequent and many shops close early outside summer. A house with a kitchen solves most of that.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The direct Odoriko limited express runs from Tokyo down the east coast of the Izu Peninsula to Shimoda, and a second branch runs inland to Shuzenji. These are the times and one-way fares to the four main stops.</p>
""" + TRAIN_TABLE_EN + """
<p class="fine">Times and fares for Atami, Ito and Shuzenji are from [[a:jg6305]]. The Shimoda time and fare are from [[a:ekitan]]. Fares change, so check before you book.</p>
<p>Shuzenji has a second route that runs far more often: take the Shinkansen to Mishima, then the Izuhakone Railway for 35 minutes [[s:jg6311]]. The Japan Rail Pass does not cover the private line between Ito and Shimoda, and the Mishima to Shuzenji section carries a ¥550 supplement [[s:jg6305]].</p>

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is. The south is not. The direct Odoriko limited express takes about 2 hours 35 minutes from Tokyo to Izukyu-Shimoda [[s:ekitan]]. Out and back is more than five hours on a train, for a few hours on a beach. The closer towns of Atami and Ito work as day trips. The south coast and the inland onsen towns reward people who stay.</p>

<h2>Which Izu town suits you?</h2>
<ul>
<li><strong>Shimoda</strong> is a port town with white-sand beaches. Shirahama Beach is about 15 minutes by bus from the station [[s:jnto]]. The harbour lands more [[l:kinmedai|kinmedai]] than anywhere in Japan.</li>
<li><strong>Shuzenji</strong> is an inland hot-spring town built along a river, with a bamboo grove, a temple and a free public foot bath [[s:uncharted]].</li>
<li><strong>Atami and Ito</strong> are the closest to Tokyo and have the most hotels. They are the busiest too.</li>
</ul>

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>The official swimming season at Izu beaches runs from around mid-July to late August [[s:jg6322]]. In good weather the sea is pleasant from late May through September [[s:jg6304]], but lifeguards are on duty only during the official season [[s:funjapan]]. Outside summer the towns are much quieter, and many restaurants and shops close early [[s:tdn]].</p>

<h2>What changes when you rent a house in Izu?</h2>
<p>A hotel room gives you one or two nights and a dinner time. A house gives you a kitchen, a washing machine and a table to work at, which is what makes four nights or a week practical. The usual rhythm is work in the morning, beach or bath in the afternoon, and dinner at home when the restaurants have closed.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, about ten minutes on foot from Izukyu-Shimoda Station.]]
<p>Our home in Shimoda, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, was set up for exactly this. It has a work desk, a washing machine and dryer, a kitchen with proper cooking equipment and self check-in with a smart lock. It is about ten minutes on foot from Izukyu-Shimoda Station, with restaurants, a convenience store and a supermarket within walking distance.</p>
[[ed:Add the measured Wi-Fi speed and the time of the last bus from the beaches.]]

<h2>What are the drawbacks of staying in Izu?</h2>
<p>Public transport is limited. Buses run infrequently, ride-hailing is not comparable to a big city, and the direct trains from Tokyo run mainly in the morning and early afternoon [[s:tdn]]. Plan the day around the timetable, shop before the evening, and consider an e-bike or a rental car if you want to move between beaches.</p>
""",
 "faq": [
  ("Can I use the Japan Rail Pass to get to Izu?",
   "Partly. It covers the JR sections, but not the Izukyu line between Ito and Shimoda. Mishima to Shuzenji needs a ¥550 supplement [[s:jg6305]]."),
  ("Do I need a car on the Izu Peninsula?",
   "Not to reach Shimoda or Shuzenji. Getting between beaches is slower without one."),
  ("How long does it take to get from Tokyo to Shimoda?",
   "About 2 hours 35 minutes by the direct Odoriko limited express from Tokyo to Izukyu-Shimoda Station [[s:ekitan]]."),
 ],
 "sources": ["ekitan", "jg6305", "jg6311", "jg6322", "jg6304", "jnto", "funjapan", "uncharted", "tdn"],
 "related": ["kinmedai", "izu"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・運賃と、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りには遠く、1週間にはちょうどよい距離です。行き方、運賃、季節、あまり語られない弱点をまとめます。",
  "review": [
   "題名と最初の節を「東京からの行き方」に変えました。「izu peninsula from tokyo」「tokyo to izu peninsula」で探す人が、最初に答えを見つけられるようにするためです",
   "所要時間と運賃が、いまの感覚と合っているか（出典は記事末にあります）",
   "回線速度の実測値と、浜からの最終バスの時刻は未記入です",
   "「バスが少ない」「店が早く閉まる」という弱点の書き方が、地元として違和感がないか",
  ],
  "points": [
   "下田は東京から直通特急で約2時間35分です。日帰りだと、電車に5時間以上乗ることになります。",
   "修善寺は約2時間です。直通特急か、新幹線で三島へ行き、ローカル線で35分です。",
   "正式な海水浴シーズンは7月中旬から8月末です。ライフガードがいるのはこの期間だけです。",
   "バスは本数が少なく、夏以外は早く閉まる店が多いです。キッチンのある家なら、その大半は解決します。",
  ],
  "body": """
<h2>東京から伊豆半島への行き方</h2>
<p>直通の特急「踊り子」は、東京から伊豆半島の東海岸を下田まで走ります。もう一方の編成は、内陸の修善寺へ向かいます。主な4駅までの所要時間と片道運賃は次のとおりです。</p>
""" + TRAIN_TABLE_JA + """
<p class="fine">熱海・伊東・修善寺の時間と運賃は[[a:jg6305]]、下田の時間と運賃は[[a:ekitan]]によります。運賃は変わるので、予約前に確認してください。</p>
<p>修善寺には、本数がずっと多い別の行き方があります。新幹線で三島へ行き、伊豆箱根鉄道に35分乗ります[[s:jg6311]]。ジャパン・レール・パスは伊東〜下田の私鉄区間では使えず、三島〜修善寺は550円の追加料金がかかります[[s:jg6305]]。</p>

<h2>伊豆半島は東京から日帰りできるか</h2>
<p>北側はできます。南側は向きません。直通の特急「踊り子」は、東京から伊豆急下田まで約2時間35分かかります[[s:ekitan]]。往復で5時間以上を電車で過ごし、浜にいられるのは数時間です。東京に近い熱海や伊東は日帰りでも成り立ちます。南の海岸と内陸の温泉町は、泊まる人の方が楽しめます。</p>

<h2>伊豆のどの町が合うか</h2>
<ul>
<li><strong>下田</strong>は、白い砂浜のある港町です。白浜海岸は駅からバスで約15分です[[s:jnto]]。港の[[l:ja-kinmedai|金目鯛]]の水揚げは日本一です。</li>
<li><strong>修善寺</strong>は、川沿いに広がる内陸の温泉町です。竹林、寺、無料の足湯があります[[s:uncharted]]。</li>
<li><strong>熱海と伊東</strong>は東京に最も近く、ホテルも最も多い町です。そのぶん一番にぎやかです。</li>
</ul>

<h2>伊豆半島はいつ行くのがよいか</h2>
<p>伊豆の浜の正式な海水浴シーズンは、7月中旬ごろから8月下旬です[[s:jg6322]]。天気がよければ5月下旬から9月まで海は快適ですが[[s:jg6304]]、ライフガードがいるのは正式なシーズン中だけです[[s:funjapan]]。夏以外の町はずっと静かで、早く閉まる飲食店や商店が多くなります[[s:tdn]]。</p>

<h2>伊豆で家を借りると何が変わるか</h2>
<p>ホテルの部屋は、1〜2泊と決まった夕食時間を前提にしています。家にはキッチン、洗濯機、仕事ができる机があり、4泊や1週間の滞在が現実的になります。午前は仕事、午後は浜か温泉、店が閉まった後は家で夕食、というのがよくある過ごし方です。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて約10分の「NODE Shimoda」のリビング。]]
<p>下田の私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、まさにこの過ごし方のために整えました。ワークデスク、洗濯機と乾燥機、調理器具のそろったキッチンがあり、スマートロックでセルフチェックインできます。伊豆急下田駅から歩いて約10分で、飲食店、コンビニ、スーパーが徒歩圏にあります。</p>
[[ed:回線速度の実測値と、浜からの最終バスの時刻を入れてください。]]

<h2>伊豆に泊まる弱点は何か</h2>
<p>公共交通は限られています。バスは本数が少なく、配車アプリは大都市のようには使えず、東京からの直通列車は午前から昼過ぎが中心です[[s:tdn]]。時刻表に合わせて一日を組み、買い物は夕方までに済ませます。浜から浜へ移動したい場合は、電動自転車かレンタカーを考えてください。</p>
""",
  "faq": [
   ("伊豆へ行くのにジャパン・レール・パスは使えますか", "一部で使えます。JRの区間は対象ですが、伊東〜下田の伊豆急行線は対象外です。三島〜修善寺は550円の追加料金が必要です[[s:jg6305]]。"),
   ("伊豆半島で車は必要ですか", "下田や修善寺に行くだけなら不要です。浜から浜への移動は、車がないと時間がかかります。"),
   ("東京から下田まで何時間かかりますか", "東京から伊豆急下田駅まで、直通の特急「踊り子」で約2時間35分です[[s:ekitan]]。"),
  ],
 },
},
]

# ---------------------------------------------------------------- 固定ページの文言
HOME = {
 "seo_title": "Okaeri Japan | Long Stays in Small-Town Japan",
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
 "h1": "About Okaeri Japan",
 "seo_title": "About Okaeri Japan: Who Runs It and How We Write",
 "description": "Okaeri Japan is run by the team that operates small homes for long stays in Shizuoka, Japan. Who we are, how our guides are sourced and how to reach us.",
 "dek": "Okaeri Japan is written by the team that runs the homes. This page says who we are, how the guides are put together and how to tell us we got something wrong.",
}

# ---------------------------------------------------------------- 写真・施設
# 写真は photos/<名前>-<幅>.webp（大きさは build.py がファイルから読む）。
# node-shimoda と yaizu-* は自社の写真（アキヤドの images/photos から）。ほかは Unsplash の写真（PHOTO_CREDITS）。
# Unsplash の写真は場所を特定しない雰囲気の写真として使い、alt・説明文に地名を書かない（撮影地が分かっても、自社の記事の主役の場所としては使わない）。
# yaizu-* は「リフォーム前」と明記する（docs/brand/experience.md の確認済みの条件）。
NODE_URL = "https://nodeshimoda.com/"

# Unsplash の写真の出典（写真の名前 → 撮影者・撮影者ページ・写真ページ・写真ID）。2026-11-14 に download_asset でダウンロードを記録して取得。
# ページ下の「Photo credits」に、そのページで使った写真の分だけ「Photo by 撮影者 on Unsplash」を出す（build.py の footer）。
UNSPLASH_UTM = "?utm_source=okaeri_japan&utm_medium=referral"
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
