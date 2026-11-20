# -*- coding: utf-8 -*-
"""kinmedai の書き直し（2026-11-16 品質保証部の HTML 84点の指摘と、黄色い枠をなくす決まり〔playbook 3-2〕、リサーチメモ「2026-11-16 手離れ」にもとづく）。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "jfa_kinme_2021": ("https://www.pref.kanagawa.jp/documents/83073/siryou4-1.pdf", "Fisheries Agency, 2021", "水産庁 2021年",
                       "Fisheries Agency: Pacific splendid alfonsino — FY2021 stock assessment and wide-area management (committee papers, November 2021)"),
    "chiba_kinme_r6": ("https://www.pref.chiba.lg.jp/gyoshigen/sigenhyoka/documents/01-r6kinme.pdf", "Chiba Prefecture, 2025", "千葉県 2025年",
                       "Chiba Prefecture: Coastal fisheries resource assessment FY2024 — splendid alfonsino"),
    "shizuoka_kinme_fat": ("https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/025/667/06kinme.pdf", "Shizuoka Prefecture (fisheries research)",
                           "静岡県（水産技術研究所）", "Shizuoka Prefecture: A new season for kinmedai based on fat content"),
    "tokyo_kinme_tag": ("https://www.ifarc.metro.tokyo.lg.jp/watch/uploads/e1b51dd9a8029f8a3c05613d0c07008c.pdf", "Tokyo Metropolitan Government",
                        "東京都", "Tokyo Metropolitan Islands Area Research and Development Center: Tagged kinmedai report No. 217 (2019)"),
    "tokushima_akamutsu": ("https://www.pref.tokushima.lg.jp/file/attachment/175834.pdf", "Tokushima Prefecture", "徳島県",
                           "Tokushima Prefecture: Akamutsu (nodoguro) catch and stock status (2015)"),
    "kyoto_akamutsu": ("https://www.pref.kyoto.jp/kaiyo/documents/akamutu.pdf", "Kyoto Prefecture", "京都府",
                       "Kyoto Prefecture: Akamutsu (blackthroat seaperch)"),
    "ibaraki_akamutsu": ("https://www.pref.ibaraki.jp/nourinsuisan/suishi/teichaku/documents/r7akamutu.pdf", "Ibaraki Prefecture", "茨城県",
                         "Ibaraki Prefectural Fisheries Experimental Station: Akamutsu, habitat depth (2026)"),
    "mhlw_mercury2010": ("https://www.mhlw.go.jp/topics/bukyoku/iyaku/syoku-anzen/suigin/dl/index-a.pdf", "Ministry of Health, Labour and Welfare",
                         "厚生労働省", "MHLW: Advice for pregnant women on fish and mercury (revised June 2010)"),
    "jre_tt_tokyo": ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetables", "JR東日本の時刻表",
                     "JR East timetables from Tokyo Station: Tokaido Shinkansen and Tokaido, Ito and Izukyu lines (November 2026)"),
    "fishbase_beryx": ("https://www.fishbase.se/summary/1320", "FishBase", "FishBase",
                       "FishBase: Beryx splendens, splendid alfonsino"),
    "fishbase_nodoguro": ("https://fishbase.se/summary/4599", "FishBase", "FishBase",
                          "FishBase: Doederleinia berycoides, blackthroat seaperch"),
    "shimoda_kanko_event": ("https://www.shimoda-city.info/event", "Shimoda Tourism Association (events)", "下田市観光協会（イベント）",
                            "Shimoda Tourism Association: Events calendar (checked November 2026)"),
    "shimoda_kanko_gift": ("https://www.shimoda-city.info/gift", "Shimoda Tourism Association (shopping)", "下田市観光協会（買う・おみやげ）",
                           "Shimoda Tourism Association: Shopping and souvenirs (checked November 2026)"),
    "pref_izu_gyokyo_shop": ("https://www.pref.shizuoka.jp/sangyoshigoto/suisan/suisangyo/uocching/1003392/1043930/1028021.html", "Shizuoka Prefecture (fish shop)",
                             "静岡県（伊豆漁協ベイステージ直売所）", "Shizuoka Prefecture: Izu Fisheries Cooperative Bay Stage shop (updated April 2025)"),
    "node_access": ("https://nodeshimoda.com/access", "NODE Shimoda (access)", "NODE Shimoda 公式サイト（アクセス）",
                    "NODE Shimoda official site: access (checked November 2026)"),
}

ARTICLE = {
 "id": "kinmedai", "slug": "kinmedai", "topic": "stay", "place": "izu", "also": [],
 "photo": ("grilled-red-fish", "A whole grilled red fish with rice, soup and small side dishes on a wooden table", ""),
 "published": "2026-11-14", "updated": "2026-11-16",
 "kicker": "Food and port towns",
 "h1": "Kinmedai: Japan’s golden-eye snapper and where to eat it",
 "seo_title": "Kinmedai: Japan’s Golden-Eye Snapper and Where to Eat It",
 "description": "Kinmedai is a red, golden-eyed deep-sea fish, often simmered as nitsuke. It’s fattiest around June, and the port of Shimoda in Izu is a good place to try it.",
 "dek": "Kinmedai is a red, golden-eyed deep-sea fish, often simmered in soy and sugar. Shimoda, said to be Japan’s top kinmedai port, is a good place to try it.",
 "card": "Kinmedai is a fatty, red deep-sea fish, often simmered in soy and sugar. It’s fattiest around June, and Shimoda, said to be Japan’s top kinmedai port, is a good place to try it.",
 "keywords": [("kinmedai", "4,400", "0")],
 "intent": "Know（知りたい）",
 "points": [
   "Its English name is splendid alfonsino, and whatever a menu calls it, it isn’t a sea bream, snapper or nodoguro.",
   "The white flesh carries fat all year, and we’d start with <em>nitsuke</em>, though raw or lightly seared works too.",
   "We’d spend a night in Shimoda: kinmedai for dinner, then breakfast at the fish-market canteen next morning.",
 ],
 "body": """
<h2>What is kinmedai?</h2>
<p>Kinmedai is a deep-sea fish with red skin and big golden eyes, known in English as splendid alfonsino (<em>Beryx splendens</em>) [[s:fishbase_beryx]]. It lives on continental slopes and on the sides and tops of underwater mountains, at around 200 to 800 metres off Chiba [[s:jfa_kinme_2021,chiba_kinme_r6]]. Shimoda’s city newsletter talks about eyes that shine gold and skin that turns red all over about 40 minutes after the fish is landed [[s:shimoda_news]].</p>
<p>The name is written 金目鯛, which literally means “golden-eye sea bream”. If you’ve seen it called golden-eye snapper on an English menu, it’s the same fish. Despite the name, it isn’t a sea bream [[s:shimoda_kanko_kinme]], and it isn’t a snapper either: it belongs to the alfonsino family, Berycidae [[s:tokyo_kinme_tag]].</p>

<h2>What does kinmedai taste like, and how is it eaten?</h2>
<p>Kinmedai is a rich white fish that carries plenty of fat, and it stays that way all year. Shimoda City puts that down to its life in deep water, and says it works in lots of different dishes [[s:shimoda_news]]. If you only try it once, we’d go for <em>nitsuke</em>, fish simmered in soy sauce and sugar, though in our view it’s just as good raw or lightly seared.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Dish</th><th>What it is</th></tr></thead>
<tbody>
<tr><td><strong>Nitsuke</strong></td><td>A whole fish or a thick cut, simmered until the sauce turns glossy. Our pick for a first try, and we think a big fish is worth the extra: Shizuoka’s researchers, measuring kinmedai landed at Inatori in Izu (a 2007–2011 study), found that bigger fish carry more fat [[s:shizuoka_kinme_fat]].</td></tr>
<tr><td><strong>Sashimi and aburi</strong></td><td>Raw slices, or slices with the skin lightly seared.</td></tr>
<tr><td><strong>Shabu-shabu</strong></td><td>Thin slices swished through hot broth at the table. If you see it on a menu, we’d give it a try.</td></tr>
<tr><td><strong>Everything else</strong></td><td>The Japanese travel magazine Tabi-mag also lists kinmedai ramen, burgers and croquettes [[s:tabimag]].</td></tr>
</tbody></table></div>
<p>If you’re buying a whole fish, the same newsletter says a fresh one has clear golden eyes and bright red skin, and both turn whitish as it ages [[s:shimoda_news]].</p>

<h2>Why is kinmedai expensive?</h2>
<p>We think it comes down to how it’s caught and how much is caught. Off the Kanto coast and the Izu Islands, kinmedai are caught mainly on hook-and-line gear, mostly vertical longlines (<em>tatenawa</em>) and bottom-set longlines (<em>soko-tate-haenawa</em>) lowered into deep water [[s:jfa_kinme_2021,chiba_kinme_r6]]. Catches off Tokyo, Chiba, Kanagawa and Shizuoka held at just under 7,000 tonnes a year in 2005–2009, then fell to 3,797 tonnes in 2020 [[s:jfa_kinme_2021]].</p>
<p>The official picture of the stock has shifted over the past few years. The Fisheries Agency’s 2021 assessment rated the stock low in 2020, with the breeding (spawning) stock flat over the previous five years [[s:jfa_kinme_2021]]. Chiba Prefecture later reported that the national assessment found the 2023 spawning stock above its target level and increasing [[s:chiba_kinme_r6]].</p>
<p>That target is the level that should allow the largest catch year after year without shrinking the stock. For you, it means kinmedai isn’t a fish to avoid, but it isn’t plentiful either. Chiba’s own landings were 1,467 tonnes in 2023, against 2,263 tonnes in 2007 [[s:chiba_kinme_r6]].</p>

<h2>How is kinmedai different from nodoguro?</h2>
<p>Nodoguro is a different fish altogether: it’s the market name for <em>akamutsu</em>, known in English as blackthroat seaperch [[s:kyoto_akamutsu,fishbase_nodoguro]]. The two are easy to mix up, since both are red and both are prized. But they sit in different families and different orders, and nodoguro lives much shallower. If a menu offers both, you’re choosing between two different fish.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>Kinmedai</th><th>Nodoguro</th></tr></thead>
<tbody>
<tr><td><strong>Order</strong></td><td>Beryciformes, the alfonsino order [[s:tokyo_kinme_tag]]</td><td>Perciformes, the perch-like fishes [[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>Family</strong></td><td>Alfonsinos (Berycidae) [[s:tokyo_kinme_tag]]</td><td>Acropomatidae [[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>Depth</strong></td><td>About 200–800 m off Chiba [[s:chiba_kinme_r6]]</td><td>About 80–150 m in the south-western Sea of Japan [[s:ibaraki_akamutsu]], about 100–200 m in Tokushima’s account [[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>Name</strong></td><td>金目鯛, “golden-eye sea bream”</td><td>“Black throat”, for the black lining inside its mouth [[s:kyoto_akamutsu]]</td></tr>
</tbody></table></div>
<p>The order and family here are as given by Tokyo and Tokushima’s fisheries reports. Fish classification gets revised now and then, so other books may file them a little differently.</p>

<h2>Is kinmedai safe to eat when you’re pregnant?</h2>
<p>Because of mercury, Japan’s health ministry advises pregnant women to limit some fish to about one 80 g serving a week. Kinmedai is on that list, along with swordfish, bluefin tuna and bigeye tuna [[s:mhlw_mercury2010]]. The same advice puts one piece of sushi or sashimi at about 15 g, so 80 g is roughly five pieces. It’s meant to protect the unborn baby, not children or other adults [[s:mhlw_mercury2010]]. It’s general public guidance rather than medical advice, so if you’re pregnant, your own doctor or midwife is the person to ask.</p>

<h2>Where can you eat kinmedai in Shimoda?</h2>
<p>Plenty of places in town serve it, and the local tourism association keeps a list to start from. As of November 2026, it names 19 restaurants and 34 hotels and inns that serve kinmedai dishes, with a note that some may be off the menu depending on the catch [[s:shimoda_kanko_kinme]].</p>
<p>Shimoda sits at the southern tip of the [[l:izu|Izu Peninsula]]. According to the tourism association, it’s said to be Japan’s top kinmedai port. As of November 2026, its page puts landings at over 1,000 tonnes a year, about 80% of all the fish landed there [[s:shimoda_kanko_kinme]]. You may also hear two local names. A 2014 TV Tokyo programme on Shimoda explained that <em>jikinme</em> are caught in nearby waters between Oshima and Kozushima, while <em>oki-kinme</em> come from grounds further out [[s:tvtokyo]].</p>
<p>The easiest place to start is Ichiba no Shokudo Kinmetei, a canteen inside the Shimoda fish market about ten minutes on foot from Izukyu-Shimoda Station. Its menu includes a kinmedai rice bowl served three ways and a whole simmered kinmedai set. Shizuoka Prefecture’s page, updated in March 2025, lists the hours as 7:00 to 9:30 for the morning set and 11:00 to 15:00 for lunch, closed on Tuesdays [[s:pref]]. Hours do change, so a quick check before you walk over saves a wasted trip.</p>

<h2>When is kinmedai in season?</h2>
<p>Kinmedai is a deep-sea fish, so it’s landed all year, and the tourism association says it’s in season all year too [[s:shimoda_kanko_kinme]]. Locals still point to two high points: winter, and early summer around June, when the fish are fattiest.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>When</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Winter</td><td>The traditional season, when kinmedai goes into hot pots [[s:shimoda_news,shizuoka_kinme_fat]] and the flesh is at its firmest [[s:shimoda_kanko_kinme]].</td></tr>
<tr><td>Around June</td><td>Before spawning, when the fish carry the most fat. In Shizuoka’s year of measuring fish from Inatori (part of a 2007–2011 study), the fat peaked in June at about 10% [[s:shimoda_news,shizuoka_kinme_fat]].</td></tr>
<tr><td>Kinme Matsuri (all of June in 2016)</td><td>In 2016 there was a viewing spot outside the fish market, open from about 7:30 to 9:00 a.m. except on Tuesdays and Saturdays, and bad weather could cancel it [[s:shimoda_news]].</td></tr>
</tbody></table></div>
<p>In 2016, then, the festival gave visitors a place to watch the morning landings in June. For this year’s events, the tourism association’s events calendar is the place to look [[s:shimoda_kanko_event]], and the association can help if you’d like to plan a trip around one.</p>

<h2>Why stay overnight instead of visiting for the day?</h2>
<p>In our view, a night in town is what makes a kinmedai trip relaxed. You get kinmedai for dinner, then an unhurried morning: a walk down to the harbour, breakfast at the market canteen from 7:00, where the morning set changes daily with the catch [[s:pref]], and no train to rush back for. If you can stay longer, our [[l:shimoda-guide|guide to a week in Shimoda]] covers the beaches and the rest of the town.</p>
<p>A day trip is possible, but the mornings are tight. The first Tokaido Line train from Tokyo Station leaves at 5:20 and doesn’t reach Atami until 7:08. The one earlier option is a 4:35 local from Shinagawa, which connects at Atami. On JR East’s November 2026 timetable, it reaches Izukyu-Shimoda at 7:59 [[s:jre_tt_tokyo]]. If a festival viewing kept the 2016 hours of about 7:30 to 9:00 [[s:shimoda_news]], you’d still have most of an hour after the ten-minute walk to the market. Routes are in our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]].</p>
<p>If you’d like to cook a fish yourself, the Izu Fisheries Cooperative runs a shop on the ground floor of the Kaikoku Shimoda Minato roadside station that sells Shimoda kinmedai [[s:shimoda_kanko_gift]]. Shizuoka Prefecture lists it as open 8:00 to 16:30 with no regular closing day, about ten minutes on foot from the station (page updated April 2025) [[s:pref_izu_gyokyo_shop]]. Our apartment in the old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, has a kitchen with a gas hob, fridge, rice cooker and cookware [[s:node_room]], and it’s eight minutes’ walk from the station [[s:node_access]].</p>
""",
 "faq": [
   ("Is kinmedai the same as red snapper?",
    "No. Kinmedai belongs to the alfonsino family (Berycidae), not the snapper or sea bream families [[s:tokyo_kinme_tag]]. Whatever an English menu calls it, it isn’t a snapper."),
   ("Why is kinmedai so expensive?",
    "We think it’s mainly how it’s caught and how much. It lives deep, at around 200 to 800 metres off Chiba, and is caught on hook-and-line gear, mostly vertical longlines [[s:jfa_kinme_2021,chiba_kinme_r6]]. Catches off Tokyo, Chiba, Kanagawa and Shizuoka fell from just under 7,000 tonnes a year in 2005–2009 to 3,797 tonnes in 2020 [[s:jfa_kinme_2021]]. A later national assessment found the 2023 breeding stock above its target level and rising [[s:chiba_kinme_r6]]."),
   ("Is kinmedai the same as nodoguro?",
    "No. Nodoguro is the market name for akamutsu, or blackthroat seaperch [[s:fishbase_nodoguro]], a red fish from a different order and family (Perciformes, Acropomatidae). It lives in shallower water, at around 80 to 200 metres depending on the area [[s:tokushima_akamutsu,ibaraki_akamutsu]]."),
   ("Can I eat kinmedai when I’m pregnant?",
    "Japan’s health ministry advises pregnant women to keep kinmedai to about one 80 g serving a week because of mercury, which is roughly five pieces of sushi [[s:mhlw_mercury2010]]. Your doctor or midwife can tell you what applies to you."),
   ("When is kinmedai in season?",
    "It’s landed all year, and Shimoda’s tourism association calls it in season all year [[s:shimoda_kanko_kinme]]. Winter is the traditional season, and the fish are fattiest around June [[s:shimoda_news,shizuoka_kinme_fat]]."),
   ("Can I see the kinmedai landings on a day trip from Tokyo?",
    "In 2016, visitors could watch the landings during the June festival, from about 7:30 to 9:00 [[s:shimoda_news]]. This year’s events are on the tourism association’s events calendar [[s:shimoda_kanko_event]]. Trains are tight too: a 4:35 local from Shinagawa reaches Shimoda at 7:59 [[s:jre_tt_tokyo]]. We’d stay the night before and have breakfast at the market canteen."),
   ("How do you say kinmedai?",
    "Roughly “kin-meh-dye”. Locals often shorten it to <em>kinme</em>."),
 ],
 "sources": ["shimoda_kanko_kinme", "shimoda_news", "pref", "shizuoka_kinme_fat", "chiba_kinme_r6", "jfa_kinme_2021",
             "tokyo_kinme_tag", "tokushima_akamutsu", "kyoto_akamutsu", "ibaraki_akamutsu", "mhlw_mercury2010",
             "tvtokyo", "tabimag", "jre_tt_tokyo", "shimoda_kanko_event", "shimoda_kanko_gift", "pref_izu_gyokyo_shop",
             "node_room", "node_access", "fishbase_beryx", "fishbase_nodoguro"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "金目鯛とは：日本の「ゴールデンアイ・スナッパー」と、食べられる場所",
  "dek": "金目鯛は、赤い皮と金色の目をした深海魚で、醤油と砂糖で煮る煮付けでよく食べられます。金目鯛の水揚げ日本一と言われる下田は、食べに行くのにちょうどいい場所です。",
  "review": [
   "【2026-11-16 書き直し（品質保証部の HTML 84点・原稿 85点の指摘と、黄色い枠をなくす決まり〔playbook 3-2〕）】変えた点: ①黄色い枠をすべてなくしました。公式のページで確かめられたことだけで書き、確かめられないこと（いまの祭りの開催、祭り以外の日の見学、私たちが案内している店）は書いていません ②下田の水揚げは「日本一の港と言われ、年1,000トン以上・下田で揚がる魚の約8割」と観光協会の言い方のまま書き、時点（観光協会のページ、2026年11月時点）を付けました。dek・card も「日本一と言われる」に ③「一年中揚がる・1年中が旬」「冬は身が引き締まる」に観光協会の出典を付けました ④きんめ祭りは2016年の記録（6月、市場の外で7時半〜9時ごろ、火・土は休み、天候で中止あり）として表に残し、「いまの行事は観光協会の行事のページで。行事に合わせるなら観光協会に」としました。調べた過程（「確かめられなかった」など）は書いていません ⑤日帰り: 「間に合っても終わりのほうだけ」を「2016年と同じ時間なら、駅から約10分歩いても1時間近く残る」に直しました ⑥In short の3つ目を「1泊して、夕食に金目鯛、翌朝は市場の食堂で朝ごはん」に（朝も金目鯛が出るとは書いていません。金目亭の朝は日替わり定食のみで、その日の水揚げで変わるため。本文にもそう書きました） ⑦のどぐろとの表の「目」の行に キンメダイ目／スズキ目 を入れ、「東京都と徳島県の水産の資料での分け方。分類は見直されることがある」と添えました。「独自の科」はやめ、キンメダイ科（Berycidae）と書きました ⑧出典名の二重かっこをやめ、出典は番号だけにしました ⑨食べられる店は、観光協会の一覧（飲食店19軒・宿34軒）へのリンクにしました。店名は県の出典がある金目亭だけです ⑩自炊用に買える所として、道の駅 開国下田みなと1階の伊豆漁協の直売所（観光協会と県のページ。住所・電話が同じ同じ店）を足しました ⑪NODE Shimoda は「旧町内のアパートの一室」とし、キッチンの設備は公式サイトの記載（ガスコンロ・冷蔵庫・炊飯器・調理器具）、駅から徒歩8分（公式のアクセス）で書きました。触れるのは本文で1回です ⑫新しい出典: shimoda_kanko_event・shimoda_kanko_gift・pref_izu_gyokyo_shop・node_access（SOURCES_NEW）",
   "【変わりやすい数字（確認した日）】観光協会の一覧の店の数（飲食店19軒・宿34軒、2026-11-16）、年1,000トン以上・約8割（観光協会のページ、2026-11-16）、金目亭の営業時間（静岡県のページ 2025年3月更新）、伊豆漁協の直売所の営業時間（静岡県のページ 2025年4月更新）、品川4:35発→伊豆急下田7:59着（JR東日本の時刻表 2026年11月）、NODE Shimoda の徒歩8分と設備（公式サイト、2026-11-16）",
  ],
  "points": [
    "英語の名前は splendid alfonsino。メニューで何と呼ばれていても、鯛でもフエダイ（スナッパー）でもなく、のどぐろとも別の魚です。",
    "白身には一年中脂がのっています。私たちならまず煮付けを選びますが、刺身やさっと炙ったものもおいしいです。",
    "私たちなら下田に1泊します。夕食に金目鯛を食べて、翌朝は魚市場の食堂で朝ごはんです。",
  ],
  "body": """
<h2>金目鯛とはどんな魚か</h2>
<p>金目鯛は、赤い皮と大きな金色の目をした深海魚です。英語では splendid alfonsino（学名 <em>Beryx splendens</em>）と呼ばれます[[s:fishbase_beryx]]。大陸斜面や、海の中の山の斜面・頂上にすんでいて、千葉の沖では水深200〜800メートルほどの所です[[s:jfa_kinme_2021,chiba_kinme_r6]]。下田市の広報によると、目は金色に輝き、水揚げから40分ほどで全身が赤くなるそうです[[s:shimoda_news]]。</p>
<p>漢字では「金目鯛」と書きます。英語のメニューで golden-eye snapper と見かけたなら同じ魚です。名前に「鯛」がついていますが鯛の仲間ではなく[[s:shimoda_kanko_kinme]]、フエダイ（スナッパー）の仲間でもありません。キンメダイ科（Berycidae）の魚です[[s:tokyo_kinme_tag]]。</p>

<h2>金目鯛はどんな味で、どうやって食べるのか</h2>
<p>金目鯛は、脂のたっぷりのった、こくのある白身で、それが一年中変わりません。下田市は、深い海にすむからだと説明していて、いろいろな料理に向くそうです[[s:shimoda_news]]。1回だけ食べるなら、私たちは醤油と砂糖で煮る「煮付け」をすすめます。ただ、生でも、さっと炙っても同じくらいおいしいと私たちは思います。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>料理</th><th>どんなものか</th></tr></thead>
<tbody>
<tr><td><strong>煮付け</strong></td><td>丸ごと、または厚い切り身を、たれに照りが出るまで煮たもの。最初の1回に、私たちがすすめる食べ方です。大きめの魚を選ぶ価値があると思います。静岡県の研究者が伊豆の稲取に揚がった金目鯛を測ったところ（2007〜2011年度の調査）、大きい魚ほど脂が多かったからです[[s:shizuoka_kinme_fat]]。</td></tr>
<tr><td><strong>刺身と炙り</strong></td><td>生の切り身や、皮目をさっと炙った切り身です。</td></tr>
<tr><td><strong>しゃぶしゃぶ</strong></td><td>薄切りを、卓上の熱い出汁にくぐらせて食べます。メニューで見かけたら、私たちなら試してみます。</td></tr>
<tr><td><strong>そのほか</strong></td><td>旅のメディア「旅マガジン」は、金目鯛のラーメン、バーガー、コロッケも紹介しています[[s:tabimag]]。</td></tr>
</tbody></table></div>
<p>丸ごと買うなら、同じ広報によると、新鮮なものは目が澄んだ金色で、皮が鮮やかな赤。古くなるとどちらも白っぽくなります[[s:shimoda_news]]。</p>

<h2>金目鯛はなぜ高いのか</h2>
<p>私たちは、とり方と、とれる量が大きいと見ています。関東の沖と伊豆諸島では、金目鯛は主に釣りでとります。おもに「立縄」と「底立延縄」で、深い海まで仕掛けを下ろします[[s:jfa_kinme_2021,chiba_kinme_r6]]。東京・千葉・神奈川・静岡の漁獲量は、2005〜09年は年7,000トン弱で安定していましたが、2020年には3,797トンに減りました[[s:jfa_kinme_2021]]。</p>
<p>資源についての公的な評価は、ここ数年で変わってきています。水産庁の2021年の評価では、2020年の資源は「低位」で、親魚の量はそれまでの5年ほど横ばいでした[[s:jfa_kinme_2021]]。その後、千葉県によると、国の評価では2023年の親魚の量が目標の水準を上回り、増えていると判断されました[[s:chiba_kinme_r6]]。</p>
<p>この目標の水準（MSY）は、資源を減らさずに、毎年いちばん多くとり続けられる量の目安です。旅行者にとっては、避けるべき魚ではないけれど、たくさんいるわけでもない、ということです。千葉県の水揚げは2023年に1,467トンで、2007年の2,263トンには届いていません[[s:chiba_kinme_r6]]。</p>

<h2>金目鯛とのどぐろは、どう違うのか</h2>
<p>のどぐろは、まったく別の魚です。「アカムツ」の市場での呼び名で、英語では blackthroat seaperch と呼ばれます[[s:kyoto_akamutsu,fishbase_nodoguro]]。どちらも赤くて高級なので混同されがちです。でも、科も目（もく）も違い、のどぐろのほうがずっと浅い所にすんでいます。メニューに両方あれば、2つの違う魚から選んでいることになります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>金目鯛</th><th>のどぐろ</th></tr></thead>
<tbody>
<tr><td><strong>目（もく）</strong></td><td>キンメダイ目[[s:tokyo_kinme_tag]]</td><td>スズキ目[[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>科</strong></td><td>キンメダイ科[[s:tokyo_kinme_tag]]</td><td>ホタルジャコ科[[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>すむ深さ</strong></td><td>千葉の沖で200〜800メートルほど[[s:chiba_kinme_r6]]</td><td>日本海の南西の海域で80〜150メートルほど[[s:ibaraki_akamutsu]]、徳島県の資料では100〜200メートルほど[[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>名前の由来</strong></td><td>漢字で「金目鯛」（金色の目の鯛）</td><td>口の中（のど）が黒いこと[[s:kyoto_akamutsu]]</td></tr>
</tbody></table></div>
<p>目と科は、東京都と徳島県の水産の資料での分け方です。魚の分類はときどき見直されるので、本によっては少し違う分け方をしていることがあります。</p>

<h2>妊娠中に金目鯛を食べてもいいか</h2>
<p>厚生労働省は、水銀のために、妊婦が食べる量を「週1回・1回約80gまで」とする魚に、メカジキ、クロマグロ、メバチと並んで金目鯛を入れています[[s:mhlw_mercury2010]]。同じ注意事項では、寿司や刺身1貫は約15gなので、80gは寿司でだいたい5貫です。これはおなかの赤ちゃんを守るための目安で、子どもやほかの大人向けではありません[[s:mhlw_mercury2010]]。一般向けの目安で、医療の助言ではないので、妊娠中なら、かかりつけの医師や助産師に聞くのがいちばんです。</p>

<h2>下田のどこで金目鯛を食べられるか</h2>
<p>町には金目鯛を出す店がたくさんあります。手始めには、観光協会の一覧が便利です。2026年11月の時点で、金目鯛の料理を出す飲食店19軒と、ホテル・旅館34軒が載っていて、水揚げによっては出せない日もある、と添えてありました[[s:shimoda_kanko_kinme]]。</p>
<p>下田は[[l:ja-izu|伊豆半島]]の南端にあります。観光協会によると、下田港は金目鯛の水揚げ量日本一の港と言われ、年1,000トン以上（観光協会のページ、2026年11月時点）、下田で揚がる魚の約8割を金目鯛が占めるそうです[[s:shimoda_kanko_kinme]]。地元では、2つの呼び名を耳にするかもしれません。2014年のテレビ東京の下田の番組では、「地金目」は大島から神津島にかけての近海でとれたもの、「沖金目」はもっと遠くの漁場でとれたもの、と説明していました[[s:tvtokyo]]。</p>
<p>手始めにいちばん行きやすいのは、下田市魚市場の中にある食堂「市場の食堂 金目亭」で、伊豆急下田駅から歩いて約10分です。金目鯛を3通りで味わう丼や、丸ごとの煮付けの定食があります。静岡県のページ（2025年3月更新）によると、朝定食が7時〜9時30分、昼が11時〜15時で、火曜が定休日です[[s:pref]]。営業時間は変わることがあるので、出かける前にさっと確かめておくと、無駄足になりません。</p>

<h2>金目鯛の旬はいつか</h2>
<p>金目鯛は深海魚なので一年中揚がり、観光協会は「1年中が旬」と言っています[[s:shimoda_kanko_kinme]]。それでも地元で挙がる時期は2つあります。冬と、脂がいちばん乗る初夏の6月ごろです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>時期</th><th>理由</th></tr></thead>
<tbody>
<tr><td>冬</td><td>鍋の季節で、昔からの旬とされる時期です[[s:shimoda_news,shizuoka_kinme_fat]]。身がいちばん引き締まります[[s:shimoda_kanko_kinme]]。</td></tr>
<tr><td>6月ごろ</td><td>産卵の前で、脂がいちばん多い時期。静岡県が稲取の魚を1年間測ったところ（2007〜2011年度の調査）、脂は6月に最も多く、約10%でした[[s:shimoda_news,shizuoka_kinme_fat]]。</td></tr>
<tr><td>きんめ祭り（2016年は6月いっぱい）</td><td>2016年は、魚市場の外に見学場所があり、朝7時半〜9時ごろに水揚げを見られました（火曜・土曜は休み、天候で中止もあり）[[s:shimoda_news]]。</td></tr>
</tbody></table></div>
<p>2016年は、6月の祭りの期間に、朝の水揚げを見られる場所がありました。いまの行事は、観光協会の行事のページで見られます[[s:shimoda_kanko_event]]。行事に合わせて旅を組みたいなら、観光協会に聞くのが確実です。</p>

<h2>日帰りではなく、泊まったほうがいい理由</h2>
<p>私たちは、町に1泊すると金目鯛の旅がずっとゆったりすると思っています。夕食に金目鯛を食べて、朝は港までのんびり歩き、市場の食堂で7時からの朝ごはん（朝はその日の水揚げで変わる日替わりの定食です）[[s:pref]]。帰りの電車に追われることもありません。もっと長くいられるなら、浜や町の過ごし方を[[l:ja-shimoda-guide|下田で1週間過ごすためのガイド]]にまとめました。</p>
<p>日帰りもできますが、朝はかなり慌ただしくなります。東京駅の始発の東海道線は5:20発で、熱海に着くのは7:08です。それより早い行き方は1つで、品川4:35発の普通に乗って熱海で乗り継ぐと、JR東日本の2026年11月の時刻表で伊豆急下田に7:59に着きます[[s:jre_tt_tokyo]]。祭りの見学が2016年と同じ朝7時半〜9時ごろなら[[s:shimoda_news]]、駅から市場まで約10分歩いても、1時間近く残ります。行き方は、[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>魚を自分で料理してみたいなら、道の駅「開国下田みなと」の1階で、伊豆漁協が下田の金目鯛などを売る店を開いています[[s:shimoda_kanko_gift]]。静岡県のページ（2025年4月更新）では、8時〜16時30分・定休日なしで、駅から歩いて約10分です[[s:pref_izu_gyokyo_shop]]。旧町内にある私たちのアパートの一室「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」には、ガスコンロ・冷蔵庫・炊飯器・調理器具のそろったキッチンがあり[[s:node_room]]、駅から歩いて8分です[[s:node_access]]。</p>
""",
  "faq": [
    ("金目鯛は、レッドスナッパーと同じですか",
     "違います。金目鯛はキンメダイ科の魚で、名前に「鯛」が付くだけです。鯛の仲間でも、スナッパー（フエダイ）の仲間でもありません[[s:tokyo_kinme_tag]]。英語のメニューに何と書いてあっても、スナッパーではありません。"),
    ("金目鯛はなぜ高いのですか",
     "とり方と、とれる量が大きいと私たちは見ています。千葉の沖では水深200〜800メートルほどの深い所にすみ、主に釣り（おもに立縄）でとります[[s:jfa_kinme_2021,chiba_kinme_r6]]。東京・千葉・神奈川・静岡の漁獲量は、2005〜09年の年7,000トン弱から2020年には3,797トンに減りました[[s:jfa_kinme_2021]]。その後の国の評価では、2023年の親魚の量は目標の水準を上回り、増えています[[s:chiba_kinme_r6]]。"),
    ("金目鯛とのどぐろは同じ魚ですか",
     "違います。のどぐろは「アカムツ」の呼び名で[[s:fishbase_nodoguro]]、スズキ目ホタルジャコ科という、目も科も違う赤い魚です。すむ深さは、海域によって80〜200メートルほどと、金目鯛より浅い所です[[s:tokushima_akamutsu,ibaraki_akamutsu]]。"),
    ("妊娠中に金目鯛を食べてもいいですか",
     "厚生労働省は、水銀のために、妊婦は金目鯛を「週1回・1回約80gまで」にするよう勧めています。寿司ならだいたい5貫です[[s:mhlw_mercury2010]]。自分の場合どうかは、医師や助産師に聞いてください。"),
    ("金目鯛の旬はいつですか",
     "一年中揚がり、下田の観光協会は「1年中が旬」と言っています[[s:shimoda_kanko_kinme]]。昔からの旬は冬で、脂がいちばん乗るのは6月ごろです[[s:shimoda_news,shizuoka_kinme_fat]]。"),
    ("東京から日帰りで、金目鯛の水揚げを見られますか",
     "2016年は、6月のきんめ祭りの期間に、朝7時半〜9時ごろ水揚げを見学できました[[s:shimoda_news]]。いまの行事は、観光協会の行事のページで見られます[[s:shimoda_kanko_event]]。電車も慌ただしく、品川4:35発の普通で下田に7:59着です[[s:jre_tt_tokyo]]。私たちなら前の晩に泊まって、市場の食堂で朝ごはんにします。"),
    ("kinmedai はどう発音しますか",
     "英語を話す人には “kin-meh-dye” が近い音です。地元では「キンメ」と略すこともよくあります。"),
  ],
 },
}
