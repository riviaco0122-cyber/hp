# -*- coding: utf-8 -*-
"""kinmedai の書き直し（2026-11-15 品質保証部の2回目の採点とリサーチメモ 2 にもとづく）。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "shimoda_kanko_fes": ("https://www.shimoda-city.info/event/kinme.html", "Shimoda Tourism Association", "伊豆下田観光協会",
                          "Shimoda Tourism Association: Kinme Matsuri"),
    "jfa_kinme_2021": ("https://www.pref.kanagawa.jp/documents/83073/siryou4-1.pdf", "Fisheries Agency, 2021", "水産庁 2021年",
                       "Fisheries Agency: Pacific splendid alfonsino — FY2021 stock assessment and wide-area management (committee papers, November 2021)"),
    "chiba_kinme_r6": ("https://www.pref.chiba.lg.jp/gyoshigen/sigenhyoka/documents/01-r6kinme.pdf", "Chiba Prefecture, 2025", "千葉県 2025年",
                       "Chiba Prefecture: Coastal fisheries resource assessment FY2024 — splendid alfonsino"),
    "shizuoka_kinme_fat": ("https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/025/667/06kinme.pdf", "Shizuoka Prefecture",
                           "静岡県", "Shizuoka Prefecture: A new season for kinmedai based on fat content"),
    "jfa_kinme_mgmt": ("https://www.jfa.maff.go.jp/j/council/seisaku/kanri/syuhou/attach/pdf/221220-10.pdf", "Fisheries Agency", "水産庁",
                       "Fisheries Agency: Management of the Pacific splendid alfonsino stock (2022)"),
    "fra_kinme": ("https://fra.repo.nii.ac.jp/record/2009184/files/kamisu_s_2018_13.pdf", "Japan Fisheries Research and Education Agency",
                  "水産研究・教育機構", "Japan Fisheries Research and Education Agency: research report on splendid alfonsino (2018)"),
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
    "jre_izu": ("https://www.jreast.co.jp/en/multi/destinations/izu.html", "JR East", "JR東日本", "JR East: Izu"),
}

ARTICLE = {
 "id": "kinmedai", "slug": "kinmedai", "topic": "stay", "place": "izu", "also": [],
 "photo": ("grilled-red-fish", "A whole grilled red fish with rice, soup and small side dishes on a wooden table", ""),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Food and port towns",
 "h1": "Kinmedai: Japan’s golden-eye snapper and where to eat it",
 "seo_title": "Kinmedai: Japan’s Golden-Eye Snapper and Where to Eat It",
 "description": "Kinmedai is a red, golden-eyed deep-sea fish, best known simmered as nitsuke. It’s best in winter and early summer, and Shimoda is the port to try it.",
 "dek": "Kinmedai is the red, golden-eyed fish you’ll find on sushi counters and ryokan tables all over Japan. It’s a deep-sea fish, best known simmered in soy and sugar, and the port of Shimoda, which calls itself Japan’s top kinmedai port, is a good place to try it.",
 "card": "What kinmedai is, how it differs from nodoguro, how Japan cooks it, its seasons, and why Shimoda, which calls itself Japan’s top kinmedai port, is worth a night.",
 "keywords": [("kinmedai", "4,400", "0")],
 "intent": "Know（知りたい）",
 "points": [
   "Kinmedai is a red deep-sea fish with big golden eyes, sold in English as splendid alfonsino or golden-eye snapper. Despite the name, it isn’t a sea bream or a snapper, and it isn’t the same fish as nodoguro.",
   "The flesh is white and carries fat all year. The classic dish is <em>nitsuke</em>, fish simmered in soy sauce and sugar, and sashimi and lightly seared slices are common too.",
   "Catches off Tokyo, Chiba, Kanagawa and Shizuoka fell from about 7,000 tonnes a year in 2005–2009 to 3,797 tonnes in 2020. The stock has been recovering since, and we think deep-water longline fishing and smaller catches are why it isn’t cheap.",
   "Shimoda, at the southern tip of the Izu Peninsula, describes itself as Japan’s top kinmedai port. Winter is the traditional season, and the fish are fattiest around June, when the town has also held a kinmedai festival.",
 ],
 "body": """
<h2>What is kinmedai?</h2>
<p>Kinmedai is a deep-sea fish with red skin and big golden eyes, known in English as splendid alfonsino (<em>Beryx splendens</em>) or golden-eye snapper. It usually lives deeper than 200 metres, on continental slopes and around underwater mountains [[s:fra_kinme,chiba_kinme_r6]]. Shimoda’s city newsletter talks about eyes that shine gold and skin that turns red all over about 40 minutes after the fish is landed [[s:shimoda_news]].</p>
<p>The name is written 金目鯛, which literally means “golden-eye sea bream”, but it belongs to its own family, the alfonsinos (Berycidae), not the sea bream or snapper families [[s:tokyo_kinme_tag]].</p>

<h2>What does kinmedai taste like, and how is it eaten?</h2>
<p>It’s a white fish with plenty of fat. Shimoda City says it keeps that fat all year because it lives in deep water, which is why it works in almost any dish [[s:shimoda_news]]. Shizuoka’s fisheries researchers also found that bigger fish carry more fat [[s:shizuoka_kinme_fat]]. Most people come for <em>nitsuke</em>, fish simmered in soy sauce and sugar, but it’s just as good raw or lightly seared.</p>
<div class="tablewrap"><table>
<thead><tr><th>Dish</th><th>What it is</th></tr></thead>
<tbody>
<tr><td><strong>Nitsuke</strong></td><td>A whole fish or a thick cut, simmered until the sauce turns glossy. This is the one most people come for.</td></tr>
<tr><td><strong>Sashimi and aburi</strong></td><td>Raw slices, or slices with the skin lightly seared.</td></tr>
<tr><td><strong>Shabu-shabu</strong></td><td>Thin slices swished through hot broth at the table.</td></tr>
<tr><td><strong>Everything else</strong></td><td>The Japanese travel magazine Tabi-mag also lists kinmedai ramen, burgers and croquettes [[s:tabimag]].</td></tr>
</tbody></table></div>
<p>If you’re buying a whole fish, the same newsletter says a fresh one has clear golden eyes and bright red skin, and both turn whitish as it ages [[s:shimoda_news]].</p>

<h2>Why is kinmedai expensive, and how is it different from nodoguro?</h2>
<p>We think it comes down to how it’s caught and how much is caught. Off the Pacific coast, kinmedai are fished with longlines dropped into deep water, not with nets [[s:jfa_kinme_mgmt]]. Catches off Tokyo, Chiba, Kanagawa and Shizuoka held at just under 7,000 tonnes a year in 2005–2009, then fell to 3,797 tonnes in 2020. A 2021 Fisheries Agency paper rated the stock low [[s:jfa_kinme_2021]].</p>
<p>The news since then is better. Chiba Prefecture reports that the national assessment found the 2023 spawning stock off the Kanto coast and Izu Islands above the level that supports the maximum sustainable yield, and rising. Chiba’s own landings were still 1,467 tonnes in 2023, against 2,263 tonnes in 2007 [[s:chiba_kinme_r6]].</p>
<p>Nodoguro is easy to mix up with kinmedai, since both are red and both are prized. It’s the market name for <em>akamutsu</em>, or blackthroat seaperch, named for the black lining inside its mouth [[s:kyoto_akamutsu]]. It belongs to a different family (Acropomatidae) and even a different order [[s:tokushima_akamutsu,tokyo_kinme_tag]], and it lives much shallower, at around 80 to 150 metres [[s:ibaraki_akamutsu]]. If a menu offers both, you’re choosing between two different fish.</p>

<h2>Is kinmedai safe to eat when you’re pregnant?</h2>
<p>Because of mercury, Japan’s health ministry advises pregnant women to limit some fish to about one 80 g serving a week. Kinmedai is on that list, along with swordfish, bluefin tuna and bigeye tuna [[s:mhlw_mercury2010]]. The same advice puts one piece of sushi or sashimi at about 15 g, so 80 g is roughly five pieces. It’s meant to protect the unborn baby, not children or other adults [[s:mhlw_mercury2010]]. It’s general public guidance rather than medical advice, so if you’re pregnant, your own doctor or midwife is the person to ask.</p>

<h2>Why is Shimoda the place to eat kinmedai?</h2>
<p>Shimoda, at the southern tip of the [[l:izu|Izu Peninsula]], describes itself as Japan’s top landing port for kinmedai. The city said so in its June 2016 newsletter, and Shizuoka Prefecture still describes the Shimoda fish market that way on a page updated in March 2025 [[s:shimoda_news,pref]].</p>
<p>You may hear two local names. A 2014 TV Tokyo programme on Shimoda explained that <em>jikinme</em> are caught in nearby waters between Oshima and Kozushima, while <em>oki-kinme</em> come from grounds further out [[s:tvtokyo]].</p>
<p>The easiest place to start is Ichiba no Shokudo Kinmetei, a canteen inside the Shimoda fish market about ten minutes on foot from Izukyu-Shimoda Station. Its menu includes a kinmedai rice bowl served three ways and a whole simmered kinmedai set. Shizuoka Prefecture lists its hours as 7:00 to 9:30 for the morning set and 11:00 to 15:00 for lunch, closed on Tuesdays ([[a:pref]], page updated March 2025). Hours do change, so it’s worth checking before you walk over.</p>
[[ed:Add the two or three places we actually send guests, with walking time from the house and what we order there.]]

<h2>When is kinmedai in season?</h2>
<p>Kinmedai is landed all year, but there are two times locals point to, and June is the month to plan around if you’d like to see the boats come in.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Winter</td><td>The traditional season, when kinmedai goes into hot pots [[s:shimoda_news,shizuoka_kinme_fat]].</td></tr>
<tr><td>Around June</td><td>Before spawning, when the fish carry the most fat. Shizuoka’s researchers measured the fat peaking in June [[s:shimoda_news,shizuoka_kinme_fat]].</td></tr>
<tr><td>Kinme Matsuri, held in June</td><td>During the festival you can watch kinmedai being landed at the Shimoda fish market from about 7:30 to 9:00. There are no landings on Tuesdays and Saturdays, when the boats don’t go out, and times can change [[s:shimoda_kanko_fes]].</td></tr>
</tbody></table></div>
<p class="fine">Festival details are from the tourism association’s festival page (November 2026). Dates for 2027 hadn’t been announced.</p>
[[ed:Confirm with the Shimoda Tourism Association whether the Kinme Matsuri ran in June 2026, and the dates and viewing times for 2027.]]

<h2>Why stay overnight instead of visiting for the day?</h2>
<p>Because the harbour does its business early. JR East gives the Odoriko limited express from Tokyo to Izukyu-Shimoda as 2 hours 49 minutes (as of November 2026) [[s:jre_izu]], so catching the 7:30 landings on a day trip would mean setting off at around half past four. Stay in town and you can wander down to the market in the morning and be at the canteen when it opens. Routes are in our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]].</p>
<p>Our home in Shimoda’s old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is about ten minutes on foot from the station. It has a properly equipped kitchen and a supermarket within walking distance, so you can cook whatever you find.</p>
[[ed:Name where guests can buy kinmedai to cook at home.]]
""",
 "faq": [
   ("Is kinmedai the same as red snapper?",
    "No. Kinmedai belongs to the alfonsino family (Berycidae), not the snapper or sea bream families [[s:tokyo_kinme_tag]]. “Golden-eye snapper” is just a market name."),
   ("Is kinmedai the same as nodoguro?",
    "No. Nodoguro is the market name for akamutsu, or blackthroat seaperch, a red fish from a different family (Acropomatidae) that lives in shallower water [[s:tokushima_akamutsu,ibaraki_akamutsu]]."),
   ("Why is kinmedai so expensive?",
    "We think it’s mainly how it’s caught and how much. It lives deeper than 200 metres and is caught on longlines rather than in nets [[s:jfa_kinme_mgmt]]. Catches off Tokyo, Chiba, Kanagawa and Shizuoka fell from just under 7,000 tonnes a year in 2005–2009 to 3,797 tonnes in 2020 [[s:jfa_kinme_2021]]. The stock has been recovering since, with the 2023 spawning stock above the sustainable-yield level [[s:chiba_kinme_r6]]."),
   ("Can I eat kinmedai when I’m pregnant?",
    "Japan’s health ministry advises pregnant women to keep kinmedai to about one 80 g serving a week because of mercury, which is roughly five pieces of sushi [[s:mhlw_mercury2010]]. Your doctor or midwife can tell you what applies to you."),
   ("When is kinmedai in season?",
    "It’s landed all year. Winter is the traditional season, and the fish are fattiest around June [[s:shimoda_news,shizuoka_kinme_fat]]."),
   ("How do you say kinmedai?",
    "Roughly “kin-meh-dye”. Locals often shorten it to <em>kinme</em>."),
 ],
 "sources": ["shimoda_news", "pref", "shizuoka_kinme_fat", "shimoda_kanko_fes", "fra_kinme", "chiba_kinme_r6", "jfa_kinme_2021",
             "jfa_kinme_mgmt", "tokyo_kinme_tag", "tokushima_akamutsu", "kyoto_akamutsu", "ibaraki_akamutsu", "mhlw_mercury2010",
             "tvtokyo", "tabimag", "jre_izu"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "金目鯛とは：日本の「ゴールデンアイ・スナッパー」と、食べられる場所",
  "dek": "金目鯛は、日本中の寿司屋や旅館で出会う、赤い皮と金色の目の魚です。深い海の魚で、醤油と砂糖で煮る煮付けが定番。金目鯛の水揚げ日本一を名乗る下田の港は、食べに行くのにちょうどいい場所です。",
  "review": [
   "【2026-11-15 2回目の書き直し】変えた点: ①資源・漁獲: 「2010年から減少」を、時点つきで過去と最近の両方に書き直しました。過去＝一都三県の漁獲量は2005〜09年に年7,000トン弱、2020年に3,797トン、資源は「低位」（水産庁 2021年11月の資料。神奈川県のサイトに載った会議資料）。最近＝国の評価で2023年の親魚量は MSY（最大持続生産量）の水準を上回り増加。ただ千葉県の水揚げは2023年1,467トンで、2007年の2,263トンを下回る（千葉県 令和6年度の資料）。In short・FAQ・日本語版も同じにしました。2018年の5,302トン（本文未確認の資料）は消しました ②観光協会の「年1,000トン以上・水揚げの約8割」を消しました。「日本一」は下田市（2016年の広報）と静岡県（2025年3月更新のページ）の説明として書いています ③「別の科」に出典を付けました。キンメダイ科＝東京都の資料、アカムツはホタルジャコ科（スズキ目）＝徳島県の資料。茨城県の資料は「80〜150メートル」の根拠としてだけ使っています ④水銀の出典を厚労省の注意事項 PDF（index-a.pdf、平成22年改訂）に差し替え、大阪府の出典と黄色い枠を外しました。同じ資料の「寿司・刺身1貫は約15g」から「80gは寿司で約5貫」と、「胎児を守るための目安で、子どもやほかの大人向けではない」を足しました ⑤味の説明を足しました（下田市の広報: 深い海にすむので一年中脂がのった白身で、どんな料理にも合う／静岡県の研究: 大きい魚ほど脂が多い）。新鮮な魚の見分け方（目が澄んだ金色、皮が鮮やかな赤。古くなると白っぽくなる）も市の広報から。金目亭のメニュー（三色の丼・丸ごとの煮付けの定食）は静岡県のページから ⑥旬の表を、市の広報と静岡県の研究で書き直しました（冬＝鍋の季節で昔からの旬、6月ごろ＝脂がいちばん多い。研究で6月に脂が最も多いと測定）。観光協会の旬のページ（開けていない）の出典は外しました ⑦日本語版 FAQ1 の「レッドスナッパー（鯛の仲間）」を直し、「名前に『鯛』が付くだけで、鯛の仲間でもフエダイの仲間でもない（キンメダイ科）」にしました ⑧「公式な説明は見つからなかった」「全国順位は見つけられなかった」など、調べた過程の話を消しました",
   "【人に確かめてほしい点】①「なぜ高いか」は、水産庁・千葉県の事実を並べたうえで「私たちの見方」として書いています。この言い方でよいか ②きんめ祭りが2026年6月に開かれたか、2027年の日程と見学の時間（黄色い枠。観光協会のページは今回も開けていません） ③紹介している店（市場の食堂 金目亭）を載せてよいか、ほかに案内している店（黄色い枠） ④ゲストが金目鯛を買える店（黄色い枠） ⑤延縄で釣ること（水産庁 2022年）、深さ200メートルより深いこと（水産研究・教育機構）は、前回の検索での確認のままです。公開前に開ける環境で照合してください（ほかの出典は、リサーチ部が今回 PDF を開いて確かめています） ⑥見出しの写真は「焼いた赤い魚」で、定番の煮付けとずれます。煮付けか水揚げの自社撮影の写真があると、ずっと良くなります",
   "【入れられなかったこと】値段の目安（一次の出典なし）。2025年の漁獲量・資源量の最新の数字（水産庁 2026年9月の資料は本文を開けていないため、千葉県の資料が伝える2023年の評価までにしました）。味そのもの（甘み・食感）の形容は公的な出典にないので、「脂ののった白身」にとどめています",
  ],
  "points": [
    "金目鯛は、赤い皮と大きな金色の目をした深海魚。英語では splendid alfonsino や golden-eye snapper の名前で売られています。名前に「鯛」が付きますが、鯛やフエダイの仲間ではなく、のどぐろとも別の魚です。",
    "身は一年中脂ののった白身。定番は、醤油と砂糖で煮る「煮付け」で、刺身や、皮目をさっと炙ったものもよく食べられます。",
    "東京・千葉・神奈川・静岡の漁獲量は、2005〜09年の年7,000トンほどから、2020年には3,797トンに減りました。その後、資源は回復してきています。深い海で延縄で釣ることと、漁獲が減ったことが、安くない理由だと私たちは見ています。",
    "伊豆半島の南端の下田は、金目鯛の水揚げ日本一の港だと説明しています。昔からの旬は冬で、脂がいちばん乗るのは6月ごろ。町ではその6月に金目鯛の祭りも開かれてきました。",
  ],
  "body": """
<h2>金目鯛とはどんな魚か</h2>
<p>金目鯛は、赤い皮と大きな金色の目をした深海魚です。英語では splendid alfonsino（学名 <em>Beryx splendens</em>）や golden-eye snapper と呼ばれます。ふだんは水深200メートルより深い、大陸斜面や海の中の山のまわりにすんでいます[[s:fra_kinme,chiba_kinme_r6]]。下田市の広報によると、目は金色に輝き、水揚げから40分ほどで全身が赤くなるそうです[[s:shimoda_news]]。</p>
<p>漢字では「金目鯛」と書きますが、鯛の仲間でもフエダイ（スナッパー）の仲間でもなく、キンメダイ科という独自の科の魚です[[s:tokyo_kinme_tag]]。</p>

<h2>金目鯛はどんな味で、どうやって食べるのか</h2>
<p>脂のたっぷりのった白身です。下田市によると、深い海にすむので一年中脂がのっていて、だからどんな料理にも合うそうです[[s:shimoda_news]]。静岡県の水産の研究では、大きい魚ほど脂が多いことも分かっています[[s:shizuoka_kinme_fat]]。お目当ては、醤油と砂糖で煮る「煮付け」という人が多いですが、生でも、さっと炙っても同じくらいおいしい魚です。</p>
<div class="tablewrap"><table>
<thead><tr><th>料理</th><th>どんなものか</th></tr></thead>
<tbody>
<tr><td><strong>煮付け</strong></td><td>丸ごと、または厚い切り身を、たれに照りが出るまで煮たもの。多くの人のお目当てです。</td></tr>
<tr><td><strong>刺身と炙り</strong></td><td>生の切り身や、皮目をさっと炙った切り身です。</td></tr>
<tr><td><strong>しゃぶしゃぶ</strong></td><td>薄切りを、卓上の熱い出汁にくぐらせて食べます。</td></tr>
<tr><td><strong>そのほか</strong></td><td>旅のメディア「旅マガジン」は、金目鯛のラーメン、バーガー、コロッケも紹介しています[[s:tabimag]]。</td></tr>
</tbody></table></div>
<p>丸ごと買うなら、同じ広報によると、新鮮なものは目が澄んだ金色で、皮が鮮やかな赤。古くなるとどちらも白っぽくなります[[s:shimoda_news]]。</p>

<h2>金目鯛はなぜ高いのか、のどぐろとはどう違うのか</h2>
<p>私たちは、釣り方と、とれる量が大きいと見ています。太平洋側では、金目鯛は網ではなく、深い海に下ろす延縄で釣ります[[s:jfa_kinme_mgmt]]。東京・千葉・神奈川・静岡の漁獲量は、2005〜09年は年7,000トン弱で安定していましたが、2020年には3,797トンに減り、2021年の水産庁の資料では資源は「低位」とされました[[s:jfa_kinme_2021]]。</p>
<p>その後は、いい知らせもあります。千葉県によると、国の評価では、関東の沖と伊豆諸島の2023年の親魚の量は、最大の漁獲を続けられる水準（MSY）を上回り、増えています。それでも千葉県の水揚げは2023年に1,467トンで、2007年の2,263トンには届いていません[[s:chiba_kinme_r6]]。</p>
<p>のどぐろは、どちらも赤くて高級なので、金目鯛と混同されがちです。のどぐろは「アカムツ」の呼び名で、口の中が黒いのが名前の由来です[[s:kyoto_akamutsu]]。ホタルジャコ科という別の科で、目（もく）も違います[[s:tokushima_akamutsu,tokyo_kinme_tag]]。すむ深さも80〜150メートルほどと、ずっと浅い所です[[s:ibaraki_akamutsu]]。メニューに両方あれば、2つの違う魚から選んでいることになります。</p>

<h2>妊娠中に金目鯛を食べてもいいか</h2>
<p>厚生労働省は、水銀のために、妊婦が食べる量を「週1回・1回約80gまで」とする魚に、メカジキ、クロマグロ、メバチと並んで金目鯛を入れています[[s:mhlw_mercury2010]]。同じ注意事項では、寿司や刺身1貫は約15gなので、80gは寿司でだいたい5貫です。これはおなかの赤ちゃんを守るための目安で、子どもやほかの大人向けではありません[[s:mhlw_mercury2010]]。一般向けの目安で、医療の助言ではないので、妊娠中なら、かかりつけの医師や助産師に聞くのがいちばんです。</p>

<h2>なぜ下田で食べるのがいいのか</h2>
<p>[[l:izu|伊豆半島]]の南端にある下田は、金目鯛の水揚げ日本一の港だと説明しています。下田市が2016年6月号の広報でそう書いていて、静岡県も2025年3月更新のページで、下田市魚市場を同じように紹介しています[[s:shimoda_news,pref]]。</p>
<p>地元では、2つの呼び名を耳にするかもしれません。2014年のテレビ東京の下田の番組では、「地金目」は大島から神津島にかけての近海でとれたもの、「沖金目」はもっと遠くの漁場でとれたもの、と説明していました[[s:tvtokyo]]。</p>
<p>手始めにいちばん行きやすいのは、下田市魚市場の中にある食堂「市場の食堂 金目亭」で、伊豆急下田駅から歩いて約10分です。金目鯛を3通りで味わう丼や、丸ごとの煮付けの定食があります。静岡県のページによると、朝定食が7時〜9時30分、昼が11時〜15時で、火曜が定休日です（[[a:pref]]、2025年3月更新）。営業時間は変わることがあるので、出かける前に確かめておくと安心です。</p>
[[ed:実際にゲストへ案内している店を2〜3軒、家からの徒歩時間と、そこで頼むものを添えて入れてください。]]

<h2>金目鯛の旬はいつか</h2>
<p>金目鯛は一年中揚がりますが、地元で挙がる時期は2つあります。船が港に入ってくるところを見たいなら、6月に合わせるのがおすすめです。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>理由</th></tr></thead>
<tbody>
<tr><td>冬</td><td>鍋の季節で、昔からの旬とされる時期です[[s:shimoda_news,shizuoka_kinme_fat]]。</td></tr>
<tr><td>6月ごろ</td><td>産卵の前で、脂がいちばん多い時期。静岡県の研究では、脂が最も多いのは6月でした[[s:shimoda_news,shizuoka_kinme_fat]]。</td></tr>
<tr><td>6月の「きんめ祭り」</td><td>祭りの間は、下田市魚市場で7時30分〜9時ごろ、金目鯛の水揚げを見られます。漁が休みの火曜と土曜は水揚げがなく、時間が変わることもあります[[s:shimoda_kanko_fes]]。</td></tr>
</tbody></table></div>
<p class="fine">祭りの情報は、観光協会の祭りのページ（2026年11月）によります。2027年の日程はまだ発表されていませんでした。</p>
[[ed:きんめ祭りが2026年6月に開かれたか、2027年の日程と見学の時間を、伊豆下田観光協会に確かめてください。]]

<h2>日帰りではなく、泊まったほうがいい理由</h2>
<p>港は朝早くに動くからです。JR東日本によると、東京から伊豆急下田までは特急「踊り子」で2時間49分（2026年11月時点）[[s:jre_izu]]。日帰りで7時30分の水揚げに間に合わせるには、朝4時半ごろに出ることになります。町に泊まれば、朝のんびり市場まで歩いて行って、開店と同時に食堂に入れます。行き方は、[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田の旧町内にある私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、駅から歩いて約10分。調理器具のそろったキッチンがあり、スーパーも歩いて行けるので、見つけた魚を自分で料理できます。</p>
[[ed:ゲストが金目鯛を買える店の名前を入れてください。]]
""",
  "faq": [
    ("金目鯛は、レッドスナッパーと同じですか",
     "違います。金目鯛はキンメダイ科の魚で、名前に「鯛」が付くだけです。鯛の仲間でも、スナッパー（フエダイ）の仲間でもありません[[s:tokyo_kinme_tag]]。「golden-eye snapper」は流通で使われる呼び名です。"),
    ("金目鯛とのどぐろは同じ魚ですか",
     "違います。のどぐろは「アカムツ」の呼び名で、ホタルジャコ科という別の科の赤い魚です。金目鯛より浅い所にすんでいます[[s:tokushima_akamutsu,ibaraki_akamutsu]]。"),
    ("金目鯛はなぜ高いのですか",
     "釣り方と、とれる量が大きいと私たちは見ています。水深200メートルより深い所にすみ、網ではなく延縄で釣ります[[s:jfa_kinme_mgmt]]。東京・千葉・神奈川・静岡の漁獲量は、2005〜09年の年7,000トン弱から2020年には3,797トンに減りました[[s:jfa_kinme_2021]]。その後は資源が回復してきていて、2023年の親魚の量は MSY の水準を上回っています[[s:chiba_kinme_r6]]。"),
    ("妊娠中に金目鯛を食べてもいいですか",
     "厚生労働省は、水銀のために、妊婦は金目鯛を「週1回・1回約80gまで」にするよう勧めています。寿司ならだいたい5貫です[[s:mhlw_mercury2010]]。自分の場合どうかは、医師や助産師に聞いてください。"),
    ("金目鯛の旬はいつですか",
     "一年中揚がります。昔からの旬は冬で、脂がいちばん乗るのは6月ごろです[[s:shimoda_news,shizuoka_kinme_fat]]。"),
    ("kinmedai はどう発音しますか",
     "英語を話す人には “kin-meh-dye” が近い音です。地元では「キンメ」と略すこともよくあります。"),
  ],
 },
}
