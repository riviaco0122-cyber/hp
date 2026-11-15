# -*- coding: utf-8 -*-
"""kinmedai の書き直し（2026-11-15 品質保証部の指摘とリサーチメモにもとづく）。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "shimoda_kanko_kinme": ("https://www.shimoda-city.info/kinem", "Shimoda Tourism Association", "伊豆下田観光協会",
                            "Shimoda Tourism Association: Shimoda kinmedai"),
    "shimoda_kanko_kinme2": ("https://www.shimoda-city.info/shimoda/kinme.html", "Shimoda Tourism Association", "伊豆下田観光協会",
                             "Shimoda Tourism Association: Kinmedai, Shimoda’s local fish"),
    "shimoda_kanko_fes": ("https://www.shimoda-city.info/event/kinme.html", "Shimoda Tourism Association", "伊豆下田観光協会",
                          "Shimoda Tourism Association: Kinme Matsuri"),
    "jfa_kinme": ("https://www.jfa.maff.go.jp/j/suisin/s_kouiki/taiheiyo/attach/pdf/index-100.pdf", "Fisheries Agency", "水産庁",
                  "Fisheries Agency: Splendid alfonsino, Pacific stock assessment (FY2019)"),
    "jfa_kinme_mgmt": ("https://www.jfa.maff.go.jp/j/council/seisaku/kanri/syuhou/attach/pdf/221220-10.pdf", "Fisheries Agency", "水産庁",
                       "Fisheries Agency: Management of the Pacific splendid alfonsino stock (2022)"),
    "fra_kinme": ("https://fra.repo.nii.ac.jp/record/2009184/files/kamisu_s_2018_13.pdf", "Japan Fisheries Research and Education Agency",
                  "水産研究・教育機構", "Japan Fisheries Research and Education Agency: research report on splendid alfonsino (2018)"),
    "kyoto_akamutsu": ("https://www.pref.kyoto.jp/kaiyo/documents/akamutu.pdf", "Kyoto Prefecture", "京都府",
                       "Kyoto Prefecture: Akamutsu (blackthroat seaperch)"),
    "ibaraki_akamutsu": ("https://www.pref.ibaraki.jp/nourinsuisan/suishi/teichaku/documents/r7akamutu.pdf", "Ibaraki Prefecture", "茨城県",
                         "Ibaraki Prefectural Fisheries Experimental Station: Akamutsu"),
    "mhlw_mercury": ("https://www.mhlw.go.jp/topics/bukyoku/iyaku/syoku-anzen/suigin/dl/050812-1.pdf", "Ministry of Health, Labour and Welfare",
                     "厚生労働省", "MHLW: Advice for pregnant women on fish and mercury (2005 revision)"),
    "osaka_mercury": ("https://www.pref.osaka.lg.jp/o100110/shokuhin/kosodate/hg.html", "Osaka Prefecture", "大阪府",
                      "Osaka Prefecture: Fish and mercury advice for pregnant women"),
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
   "Kinmedai is a red deep-sea fish with big golden eyes, sold in English as splendid alfonsino or golden-eye snapper. It isn’t a snapper, and it isn’t the same fish as nodoguro.",
   "The classic dish is <em>nitsuke</em>, fish simmered in soy sauce and sugar. Sashimi and lightly seared slices are common too.",
   "It lives more than 200 metres down, it’s caught on longlines rather than in nets, and Pacific catches have fallen since 2010. We think that’s a big part of why it isn’t cheap.",
   "Shimoda, at the southern tip of the Izu Peninsula, describes itself as Japan’s top kinmedai port. Winter is the peak season, and early summer brings the fattiest fish. The town has also held a kinmedai festival in June.",
 ],
 "body": """
<h2>What is kinmedai?</h2>
<p>Kinmedai is a deep-sea fish with red skin and big golden eyes, known in English as splendid alfonsino (<em>Beryx splendens</em>) or golden-eye snapper. It usually lives deeper than 200 metres, on continental slopes and around underwater mountains [[s:fra_kinme,jfa_kinme]]. Shimoda’s city newsletter talks about eyes that shine gold and skin that turns red all over about 40 minutes after the fish is landed [[s:shimoda_news]].</p>
<p>The name is written 金目鯛, which literally means “golden-eye sea bream”, but despite the name it isn’t a sea bream or a snapper. The flesh is white, and the same 2016 newsletter says it carries plenty of fat all year round [[s:shimoda_news]].</p>

<h2>How is kinmedai eaten?</h2>
<p>Most people come for <em>nitsuke</em>, fish simmered in soy sauce and sugar, but kinmedai is just as good raw or lightly seared.</p>
<div class="tablewrap"><table>
<thead><tr><th>Dish</th><th>What it is</th></tr></thead>
<tbody>
<tr><td><strong>Nitsuke</strong></td><td>A whole fish or a thick cut, simmered until the sauce turns glossy. This is the one most people come for.</td></tr>
<tr><td><strong>Sashimi and aburi</strong></td><td>Raw slices, or slices with the skin lightly seared.</td></tr>
<tr><td><strong>Shabu-shabu</strong></td><td>Thin slices swished through hot broth at the table.</td></tr>
<tr><td><strong>Everything else</strong></td><td>The Japanese travel magazine Tabi-mag also lists kinmedai ramen, burgers and croquettes [[s:tabimag]].</td></tr>
</tbody></table></div>

<h2>Why is kinmedai expensive, and how is it different from nodoguro?</h2>
<p>We haven’t found an official explanation of the price, but the Fisheries Agency’s figures go a long way. Off the Pacific coast, kinmedai are caught with longlines dropped into deep water, not with nets [[s:jfa_kinme_mgmt]]. The Pacific catch was 5,302 tonnes in 2018 and had been falling since 2010, and the agency’s FY2019 assessment judged the stock to be low [[s:jfa_kinme]].</p>
<p>Nodoguro is easy to mix up with kinmedai, since both are red and both are prized. It’s the market name for <em>akamutsu</em>, or blackthroat seaperch, which belongs to a different family and is known for the black lining inside its mouth [[s:kyoto_akamutsu]]. It also lives much shallower, at around 80 to 150 metres [[s:ibaraki_akamutsu]]. If a menu offers both, you’re choosing between two different fish.</p>

<h2>Is kinmedai safe to eat when you’re pregnant?</h2>
<p>Japan’s health ministry puts kinmedai among the fish that pregnant women are advised to limit to about one 80 g serving a week, because of mercury [[s:mhlw_mercury,osaka_mercury]]. It’s in the same group as swordfish and bluefin tuna. That’s general public guidance rather than medical advice, so if you’re pregnant, your own doctor or midwife is the person to ask.</p>
[[ed:Open the current MHLW page on fish and mercury for pregnant women (2010 revision) and confirm kinmedai’s category, then swap in its URL if it differs.]]

<h2>Why is Shimoda the place to eat kinmedai?</h2>
<p>Shimoda, at the southern tip of the [[l:izu|Izu Peninsula]], describes itself as Japan’s top landing port for kinmedai. The city said so in its June 2016 newsletter, and Shizuoka Prefecture and the local tourism association describe the port the same way [[s:shimoda_news,pref,shimoda_kanko_kinme]]. The association says more than 1,000 tonnes are landed a year and that about 80% of the fish landed there are kinmedai, though it doesn’t give a year for those figures [[s:shimoda_kanko_kinme]]. We couldn’t find a recent national ranking of ports to check them against.</p>
<p>You may hear two local names. A 2014 TV Tokyo programme on Shimoda explained that <em>jikinme</em> are caught in nearby waters between Oshima and Kozushima, while <em>oki-kinme</em> come from grounds further out [[s:tvtokyo]].</p>
<p>The easiest place to start is Ichiba no Shokudo Kinmetei, a canteen inside the Shimoda fish market about ten minutes on foot from Izukyu-Shimoda Station. Shizuoka Prefecture lists its hours as 7:00 to 9:30 for the morning set and 11:00 to 15:00 for lunch, closed on Tuesdays ([[a:pref]], page updated March 2025). Hours do change, so it’s worth checking before you walk over.</p>
[[ed:Add the two or three places we actually send guests, with walking time from the house and what we order there.]]

<h2>When is kinmedai in season?</h2>
<p>Kinmedai is landed all year, but there are two times locals point to, and June is the month to plan around if you’d like to see the boats come in.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Winter (December to February)</td><td>The peak season, when the flesh is at its firmest [[s:shimoda_news,shimoda_kanko_kinme,shimoda_kanko_kinme2]].</td></tr>
<tr><td>Early summer (June and July)</td><td>The fish are at their fattiest before spawning [[s:shimoda_news,shimoda_kanko_kinme,shimoda_kanko_kinme2]].</td></tr>
<tr><td>Kinme Matsuri, held in June</td><td>During the festival you can watch kinmedai being landed at the Shimoda fish market from about 7:30 to 9:00. There are no landings on Tuesdays and Saturdays, when the boats don’t go out, and times can change [[s:shimoda_kanko_fes]].</td></tr>
</tbody></table></div>
<p class="fine">Festival details are from the tourism association’s festival page, checked in November 2026. The page doesn’t give a year, and dates for 2027 hadn’t been announced.</p>
[[ed:Confirm with the Shimoda Tourism Association whether the Kinme Matsuri ran in June 2026, and the dates and viewing times for 2027.]]

<h2>Why stay overnight instead of visiting for the day?</h2>
<p>Because the harbour does its business early. JR East gives the Odoriko limited express from Tokyo to Izukyu-Shimoda as 2 hours 49 minutes (as of November 2026) [[s:jre_izu]], so catching the 7:30 landings on a day trip would mean setting off at around half past four. Stay in town and you can wander down to the market in the morning and be at the canteen when it opens. Routes are in our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]].</p>
<p>Our home in Shimoda’s old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is about ten minutes on foot from the station. It has a properly equipped kitchen and a supermarket within walking distance, so you can cook whatever you find.</p>
[[ed:Name where guests can buy kinmedai to cook at home.]]
""",
 "faq": [
   ("Is kinmedai the same as red snapper?",
    "No. Kinmedai is an alfonsino, not a snapper or a sea bream. “Golden-eye snapper” is just a market name."),
   ("Is kinmedai the same as nodoguro?",
    "No. Nodoguro is the market name for akamutsu, or blackthroat seaperch, a red fish from a different family that lives in shallower water [[s:kyoto_akamutsu,ibaraki_akamutsu]]."),
   ("Why is kinmedai so expensive?",
    "There’s no single official answer, but it lives deeper than 200 metres, it’s caught on longlines rather than in nets, and Pacific catches have been falling since 2010 [[s:jfa_kinme,jfa_kinme_mgmt]]."),
   ("Can I eat kinmedai when I’m pregnant?",
    "Japan’s health ministry advises pregnant women to keep kinmedai to about one 80 g serving a week because of mercury [[s:mhlw_mercury,osaka_mercury]]. Your doctor or midwife can tell you what applies to you."),
   ("When is kinmedai in season?",
    "It’s landed all year. Winter is the peak season, and early summer brings the fattiest fish [[s:shimoda_kanko_kinme,shimoda_kanko_kinme2]]."),
   ("How do you say kinmedai?",
    "Roughly “kin-meh-dye”. Locals often shorten it to <em>kinme</em>."),
 ],
 "sources": ["shimoda_news", "pref", "shimoda_kanko_kinme", "shimoda_kanko_kinme2", "shimoda_kanko_fes", "fra_kinme", "jfa_kinme",
             "jfa_kinme_mgmt", "kyoto_akamutsu", "ibaraki_akamutsu", "mhlw_mercury", "osaka_mercury", "tvtokyo", "tabimag", "jre_izu"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "金目鯛とは：日本の「ゴールデンアイ・スナッパー」と、食べられる場所",
  "dek": "金目鯛は、日本中の寿司屋や旅館で出会う、赤い皮と金色の目の魚です。深い海の魚で、醤油と砂糖で煮る煮付けが定番。金目鯛の水揚げ日本一を名乗る下田の港は、食べに行くのにちょうどいい場所です。",
  "review": [
   "【2026-11-15 品質保証部の指摘を受けた書き直し】変えた点: ①東京からの所要時間を、駅探の「約2時間35分」から JR東日本の公式の「2時間49分（2026年11月時点）」に直しました ②地金目・沖金目は「2014年のテレビ東京の番組の説明」として書き、出典にない「メニューで2つの名前を見る」「並べて頼む」を消しました ③「冬が旬」「一年中脂が多い」に、市の広報（2016年）と観光協会のページの出典の印を付けました。旬の表は「冬（12〜2月）＝身が締まる」「初夏（6〜7月）＝いちばん脂が乗る」に ④祭りの出典を旅マガジンから観光協会の公式ページに替え、「2026年11月に確認・ページに年の記載なし・2027年は未発表」と添えました ⑤生息する深さを「数百メートル」から「200メートルより深い」（水産研究・教育機構・水産庁）に ⑥新しい節「なぜ高いのか、のどぐろとの違い」を足しました。値段の数字は書かず、水産庁の事実（深海で、網ではなく延縄で釣る／太平洋の漁獲量は2018年に5,302トンで2010年から減少、2019年度の評価で資源は低位）を並べ、「だから高い」とは言い切らずに「私たちの見方」として書きました。のどぐろは京都府・茨城県の資料で「別の科の魚（アカムツ）、口の中が黒い、80〜150メートルと浅い所にすむ」と書きました ⑦水銀の節を足しました（厚労省: 妊婦は週1回・約80gまで。医療の助言ではないので、医師や助産師に相談を、という書き方） ⑧「describe / say」の重複と、煮付けの意味の言い直しを直しました ⑨FAQ を6問に（のどぐろ・値段・妊娠中・旬を足しました）",
   "【人に確かめてほしい点】①厚労省のいまの注意事項（2010年改訂）のページでキンメダイの区分を開いて確かめ、URL を差し替える（黄色い枠。今回は2005年の厚労省の資料と、いまの注意事項を載せた大阪府のページを出典にしています） ②きんめ祭りが2026年6月に開かれたか、2027年の日程と見学時間（黄色い枠） ③観光協会の「年間1,000トン以上・水揚げの約8割が金目鯛」は年の記載がありません。書いてよいか ④「なぜ高いか」を、水産庁の事実を並べたうえで「私たちの見方」として書いています。この言い方でよいか ⑤紹介している店（市場の食堂 金目亭）を載せてよいか、ほかに案内している店（黄色い枠） ⑥ゲストが金目鯛を買える店（黄色い枠） ⑦見出しの写真は「焼いた赤い魚」で、定番の煮付けとずれます。煮付けか水揚げの自社撮影の写真があると、ずっと良くなります ⑧出典はリサーチ部が検索で確認したもので、本文のページは開けていません。公開前にページを開いて照合してください",
   "【入れられなかったこと】値段の目安（市場価格・店の価格帯）は一次の出典が見つからず、書いていません。港別の全国順位の最新の統計も見つからなかったので、「下田市・県・観光協会がそう説明している」の形にとどめています",
  ],
  "points": [
    "金目鯛は、赤い皮と大きな金色の目をした深海魚。英語では splendid alfonsino や golden-eye snapper の名前で売られています。スナッパー（フエダイ）ではなく、のどぐろとも別の魚です。",
    "定番は、醤油と砂糖で煮る「煮付け」。刺身や、皮目をさっと炙ったものもよく食べられます。",
    "水深200メートルより深い所にすみ、網ではなく延縄で釣ります。太平洋の漁獲量は2010年から減っていて、これが安くない理由の一つだと私たちは見ています。",
    "伊豆半島の南端の下田は、金目鯛の水揚げ日本一の港だと説明しています。旬は冬で、初夏はいちばん脂が乗ります。町では6月に金目鯛の祭りも開かれてきました。",
  ],
  "body": """
<h2>金目鯛とはどんな魚か</h2>
<p>金目鯛は、赤い皮と大きな金色の目をした深海魚です。英語では splendid alfonsino（学名 <em>Beryx splendens</em>）や golden-eye snapper と呼ばれます。ふだんは水深200メートルより深い、大陸斜面や海の中の山のまわりにすんでいます[[s:fra_kinme,jfa_kinme]]。下田市の広報によると、目は金色に輝き、水揚げから40分ほどで全身が赤くなるそうです[[s:shimoda_news]]。</p>
<p>「金目鯛」と書きますが、名前とは違って、鯛の仲間でもスナッパー（フエダイ）の仲間でもありません。身は白身で、同じ2016年の広報には、一年中脂がのっているとあります[[s:shimoda_news]]。</p>

<h2>金目鯛はどうやって食べるのか</h2>
<p>お目当ては、醤油と砂糖で煮る「煮付け」という人が多いですが、生でも、さっと炙っても同じくらいおいしい魚です。</p>
<div class="tablewrap"><table>
<thead><tr><th>料理</th><th>どんなものか</th></tr></thead>
<tbody>
<tr><td><strong>煮付け</strong></td><td>丸ごと、または厚い切り身を、たれに照りが出るまで煮たもの。多くの人のお目当てです。</td></tr>
<tr><td><strong>刺身と炙り</strong></td><td>生の切り身や、皮目をさっと炙った切り身です。</td></tr>
<tr><td><strong>しゃぶしゃぶ</strong></td><td>薄切りを、卓上の熱い出汁にくぐらせて食べます。</td></tr>
<tr><td><strong>そのほか</strong></td><td>旅のメディア「旅マガジン」は、金目鯛のラーメン、バーガー、コロッケも紹介しています[[s:tabimag]]。</td></tr>
</tbody></table></div>

<h2>金目鯛はなぜ高いのか、のどぐろとはどう違うのか</h2>
<p>値段について公式な説明は見つかりませんでしたが、水産庁の数字を見ると、だいたい見当がつきます。太平洋側では、金目鯛は網ではなく、深い海に下ろす延縄で釣ります[[s:jfa_kinme_mgmt]]。太平洋の漁獲量は2018年に5,302トンで、2010年から減り続けていて、2019年度の評価では資源は「低位」とされました[[s:jfa_kinme]]。</p>
<p>のどぐろは、どちらも赤くて高級なので、金目鯛と混同されがちです。のどぐろは「アカムツ」の呼び名で、金目鯛とは別の科の魚。口の中が黒いのが特徴です[[s:kyoto_akamutsu]]。すむ深さも80〜150メートルほどと、ずっと浅い所です[[s:ibaraki_akamutsu]]。メニューに両方あれば、2つの違う魚から選んでいることになります。</p>

<h2>妊娠中に金目鯛を食べてもいいか</h2>
<p>厚生労働省は、水銀のために、妊婦が食べる量を「週1回・1回約80gまで」とする魚の中に、金目鯛を入れています[[s:mhlw_mercury,osaka_mercury]]。メカジキやクロマグロと同じ区分です。これは一般向けの目安で、医療の助言ではありません。妊娠中なら、かかりつけの医師や助産師に聞くのがいちばんです。</p>
[[ed:厚生労働省のいまの注意事項（2010年改訂）のページを開いてキンメダイの区分を確かめ、違っていれば URL を差し替えてください。]]

<h2>なぜ下田で食べるのがいいのか</h2>
<p>[[l:izu|伊豆半島]]の南端にある下田は、金目鯛の水揚げ日本一の港だと説明しています。下田市が2016年6月号の広報でそう書いていて、静岡県と地元の観光協会も同じように紹介しています[[s:shimoda_news,pref,shimoda_kanko_kinme]]。観光協会によると、水揚げは年間1,000トン以上で、港に揚がる魚の約8割が金目鯛です。ただ、何年の数字かは書かれていません[[s:shimoda_kanko_kinme]]。比べられる最新の港別の全国順位は、私たちには見つけられませんでした。</p>
<p>地元では、2つの呼び名を耳にするかもしれません。2014年のテレビ東京の下田の番組では、「地金目」は大島から神津島にかけての近海でとれたもの、「沖金目」はもっと遠くの漁場でとれたもの、と説明していました[[s:tvtokyo]]。</p>
<p>手始めにいちばん行きやすいのは、下田市魚市場の中にある食堂「市場の食堂 金目亭」で、伊豆急下田駅から歩いて約10分です。静岡県のページによると、朝定食が7時〜9時30分、昼が11時〜15時で、火曜が定休日です（[[a:pref]]、2025年3月更新）。営業時間は変わることがあるので、出かける前に確かめておくと安心です。</p>
[[ed:実際にゲストへ案内している店を2〜3軒、家からの徒歩時間と、そこで頼むものを添えて入れてください。]]

<h2>金目鯛の旬はいつか</h2>
<p>金目鯛は一年中揚がりますが、地元で挙がる時期は2つあります。船が港に入ってくるところを見たいなら、6月に合わせるのがおすすめです。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>理由</th></tr></thead>
<tbody>
<tr><td>冬（12〜2月）</td><td>旬。身がいちばん締まる時期です[[s:shimoda_news,shimoda_kanko_kinme,shimoda_kanko_kinme2]]。</td></tr>
<tr><td>初夏（6〜7月）</td><td>産卵前で、いちばん脂が乗る時期です[[s:shimoda_news,shimoda_kanko_kinme,shimoda_kanko_kinme2]]。</td></tr>
<tr><td>6月の「きんめ祭り」</td><td>祭りの間は、下田市魚市場で7時30分〜9時ごろ、金目鯛の水揚げを見られます。漁が休みの火曜と土曜は水揚げがなく、時間が変わることもあります[[s:shimoda_kanko_fes]]。</td></tr>
</tbody></table></div>
<p class="fine">祭りの情報は、観光協会の祭りのページ（2026年11月に確認）によります。ページに年の記載はなく、2027年の日程はまだ発表されていませんでした。</p>
[[ed:きんめ祭りが2026年6月に開かれたか、2027年の日程と見学の時間を、伊豆下田観光協会に確かめてください。]]

<h2>日帰りではなく、泊まったほうがいい理由</h2>
<p>港は朝早くに動くからです。JR東日本によると、東京から伊豆急下田までは特急「踊り子」で2時間49分（2026年11月時点）[[s:jre_izu]]。日帰りで7時30分の水揚げに間に合わせるには、朝4時半ごろに出ることになります。町に泊まれば、朝のんびり市場まで歩いて行って、開店と同時に食堂に入れます。行き方は、[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田の旧町内にある私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、駅から歩いて約10分。調理器具のそろったキッチンがあり、スーパーも歩いて行けるので、見つけた魚を自分で料理できます。</p>
[[ed:ゲストが金目鯛を買える店の名前を入れてください。]]
""",
  "faq": [
    ("金目鯛は、レッドスナッパー（鯛の仲間）と同じですか",
     "違います。金目鯛はキンメダイの仲間で、スナッパー（フエダイ）でも鯛でもありません。「golden-eye snapper」は流通で使われる呼び名です。"),
    ("金目鯛とのどぐろは同じ魚ですか",
     "違います。のどぐろは「アカムツ」の呼び名で、別の科の赤い魚です。金目鯛より浅い所にすんでいます[[s:kyoto_akamutsu,ibaraki_akamutsu]]。"),
    ("金目鯛はなぜ高いのですか",
     "公式な答えは1つではありませんが、水深200メートルより深い所にすみ、網ではなく延縄で釣り、太平洋の漁獲量は2010年から減っています[[s:jfa_kinme,jfa_kinme_mgmt]]。"),
    ("妊娠中に金目鯛を食べてもいいですか",
     "厚生労働省は、水銀のために、妊婦は金目鯛を「週1回・1回約80gまで」にするよう勧めています[[s:mhlw_mercury,osaka_mercury]]。自分の場合どうかは、医師や助産師に聞いてください。"),
    ("金目鯛の旬はいつですか",
     "一年中揚がります。冬が旬で、初夏はいちばん脂が乗ります[[s:shimoda_kanko_kinme,shimoda_kanko_kinme2]]。"),
    ("kinmedai はどう発音しますか",
     "英語を話す人には “kin-meh-dye” が近い音です。地元では「キンメ」と略すこともよくあります。"),
  ],
 },
}
