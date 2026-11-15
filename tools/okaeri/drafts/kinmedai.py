# -*- coding: utf-8 -*-
"""kinmedai の書き直し（2026-11-15 品質保証部の3回目の採点、リサーチメモ 3、編集長の時刻表の確認にもとづく）。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "jfa_kinme_2021": ("https://www.pref.kanagawa.jp/documents/83073/siryou4-1.pdf", "Fisheries Agency, 2021", "水産庁 2021年",
                       "Fisheries Agency: Pacific splendid alfonsino — FY2021 stock assessment and wide-area management (committee papers, November 2021)"),
    "chiba_kinme_r6": ("https://www.pref.chiba.lg.jp/gyoshigen/sigenhyoka/documents/01-r6kinme.pdf", "Chiba Prefecture, 2025", "千葉県 2025年",
                       "Chiba Prefecture: Coastal fisheries resource assessment FY2024 — splendid alfonsino"),
    "shizuoka_kinme_fat": ("https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/025/667/06kinme.pdf", "Shizuoka Prefecture",
                           "静岡県", "Shizuoka Prefecture: A new season for kinmedai based on fat content"),
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
    "jre_tt_tokyo": ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetable, Tokyo Station", "JR東日本 東京駅の時刻表",
                     "JR East, Tokyo Station timetable (November 2026)"),
}

ARTICLE = {
 "id": "kinmedai", "slug": "kinmedai", "topic": "stay", "place": "izu", "also": [],
 "photo": ("grilled-red-fish", "A whole grilled red fish with rice, soup and small side dishes on a wooden table", ""),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Food and port towns",
 "h1": "Kinmedai: Japan’s golden-eye snapper and where to eat it",
 "seo_title": "Kinmedai: Japan’s Golden-Eye Snapper and Where to Eat It",
 "description": "Kinmedai is a red, golden-eyed deep-sea fish, often simmered as nitsuke. It’s fattiest around June, and the port of Shimoda in Izu is a good place to try it.",
 "dek": "Kinmedai is the red, golden-eyed fish you’ll find on sushi counters and ryokan tables all over Japan. It’s a deep-sea fish that’s often simmered in soy and sugar, and the port of Shimoda, which calls itself Japan’s top kinmedai port, is a good place to try it.",
 "card": "What kinmedai is, how it differs from nodoguro, how Japan cooks it, its seasons, and why Shimoda, which calls itself Japan’s top kinmedai port, is worth a night.",
 "keywords": [("kinmedai", "4,400", "0")],
 "intent": "Know（知りたい）",
 "points": [
   "Kinmedai is a red deep-sea fish with big golden eyes, sold in English as splendid alfonsino or golden-eye snapper. Despite the name, it isn’t a sea bream or a snapper, and it isn’t the same fish as nodoguro, which belongs to a different family and lives in shallower water.",
   "The flesh is white and carries fat all year. You’ll see it simmered as <em>nitsuke</em> (in soy sauce and sugar), raw as sashimi and lightly seared. We’d start with nitsuke.",
   "Catches off Tokyo, Chiba, Kanagawa and Shizuoka fell from just under 7,000 tonnes a year in 2005–2009 to 3,797 tonnes in 2020. A later national assessment found the breeding stock in 2023 at a healthy level and rising. We think deep-water fishing and smaller catches are why it isn’t cheap.",
   "Shimoda, at the southern tip of the Izu Peninsula, describes itself as Japan’s top kinmedai port. Even the first train from Tokyo gets you there too late for the early-morning landings, so it’s worth staying the night before.",
 ],
 "body": """
<h2>What is kinmedai?</h2>
<p>Kinmedai is a deep-sea fish with red skin and big golden eyes, known in English as splendid alfonsino (<em>Beryx splendens</em>) or golden-eye snapper. It usually lives deeper than 200 metres, on continental slopes and around underwater mountains [[s:fra_kinme,chiba_kinme_r6]]. Shimoda’s city newsletter talks about eyes that shine gold and skin that turns red all over about 40 minutes after the fish is landed [[s:shimoda_news]].</p>
<p>The name is written 金目鯛, which literally means “golden-eye sea bream”, but it belongs to its own family, the alfonsinos (Berycidae), not the sea bream or snapper families [[s:tokyo_kinme_tag]].</p>

<h2>What does kinmedai taste like, and how is it eaten?</h2>
<p>It’s a white fish with plenty of fat. Shimoda City says it keeps that fat all year because it lives in deep water, which is why it works in almost any dish [[s:shimoda_news]]. Shizuoka’s fisheries researchers also found that bigger fish carry more fat [[s:shizuoka_kinme_fat]]. If you only try it once, we’d go for <em>nitsuke</em>, fish simmered in soy sauce and sugar, though in our view it’s just as good raw or lightly seared.</p>
<div class="tablewrap"><table>
<thead><tr><th>Dish</th><th>What it is</th></tr></thead>
<tbody>
<tr><td><strong>Nitsuke</strong></td><td>A whole fish or a thick cut, simmered until the sauce turns glossy. Our pick for a first try.</td></tr>
<tr><td><strong>Sashimi and aburi</strong></td><td>Raw slices, or slices with the skin lightly seared.</td></tr>
<tr><td><strong>Shabu-shabu</strong></td><td>Thin slices swished through hot broth at the table.</td></tr>
<tr><td><strong>Everything else</strong></td><td>The Japanese travel magazine Tabi-mag also lists kinmedai ramen, burgers and croquettes [[s:tabimag]].</td></tr>
</tbody></table></div>
<p>If you’re buying a whole fish, the same newsletter says a fresh one has clear golden eyes and bright red skin, and both turn whitish as it ages [[s:shimoda_news]].</p>

<h2>Why is kinmedai expensive?</h2>
<p>We think it comes down to how it’s caught and how much is caught. Off the Kanto coast and the Izu Islands, kinmedai are caught mainly on hook-and-line gear, mostly vertical longlines (<em>tatenawa</em>) and bottom-set longlines (<em>soko-tate-haenawa</em>) lowered into deep water [[s:jfa_kinme_2021,chiba_kinme_r6]]. Catches off Tokyo, Chiba, Kanagawa and Shizuoka held at just under 7,000 tonnes a year in 2005–2009, then fell to 3,797 tonnes in 2020 [[s:jfa_kinme_2021]].</p>
<p>The two assessments we found tell slightly different stories, so here they are with their years. The Fisheries Agency’s 2021 assessment rated the stock low in 2020, with the breeding (spawning) stock flat over the previous five years [[s:jfa_kinme_2021]]. Chiba Prefecture later reported that the national assessment found the 2023 spawning stock above its target level and increasing [[s:chiba_kinme_r6]].</p>
<p>That target is the level that should allow the largest catch year after year without shrinking the stock. For you, it means kinmedai isn’t a fish to avoid, but it isn’t plentiful either. Chiba’s own landings were 1,467 tonnes in 2023, against 2,263 tonnes in 2007 [[s:chiba_kinme_r6]].</p>

<h2>How is kinmedai different from nodoguro?</h2>
<p>Nodoguro is a different fish altogether: it’s the market name for <em>akamutsu</em>, or blackthroat seaperch, named for the black lining inside its mouth [[s:kyoto_akamutsu]]. The two are easy to mix up, since both are red and both are prized. Nodoguro belongs to a different family (Acropomatidae) and even a different order [[s:tokushima_akamutsu,tokyo_kinme_tag]], and it lives much shallower, at around 80 to 150 metres [[s:ibaraki_akamutsu]]. If a menu offers both, you’re choosing between two different fish.</p>

<h2>Is kinmedai safe to eat when you’re pregnant?</h2>
<p>Because of mercury, Japan’s health ministry advises pregnant women to limit some fish to about one 80 g serving a week. Kinmedai is on that list, along with swordfish, bluefin tuna and bigeye tuna [[s:mhlw_mercury2010]]. The same advice puts one piece of sushi or sashimi at about 15 g, so 80 g is roughly five pieces. It’s meant to protect the unborn baby, not children or other adults [[s:mhlw_mercury2010]]. It’s general public guidance rather than medical advice, so if you’re pregnant, your own doctor or midwife is the person to ask.</p>

<h2>Why is Shimoda the place to eat kinmedai?</h2>
<p>Shimoda, at the southern tip of the [[l:izu|Izu Peninsula]], describes itself as Japan’s top landing port for kinmedai. The city said so in its June 2016 newsletter, and Shizuoka Prefecture still describes the Shimoda fish market that way on a page updated in March 2025 [[s:shimoda_news,pref]].</p>
<p>You may hear two local names. A 2014 TV Tokyo programme on Shimoda explained that <em>jikinme</em> are caught in nearby waters between Oshima and Kozushima, while <em>oki-kinme</em> come from grounds further out [[s:tvtokyo]].</p>
<p>The easiest place to start is Ichiba no Shokudo Kinmetei, a canteen inside the Shimoda fish market about ten minutes on foot from Izukyu-Shimoda Station. Its menu includes a kinmedai rice bowl served three ways and a whole simmered kinmedai set. Shizuoka Prefecture lists its hours as 7:00 to 9:30 for the morning set and 11:00 to 15:00 for lunch, closed on Tuesdays ([[a:pref]], page updated March 2025). Hours do change, so a quick check before you walk over saves a wasted trip.</p>
[[ed:Add the two or three places we actually send guests, with walking time from the house and what we order there.]]

<h2>When is kinmedai in season?</h2>
<p>Kinmedai is landed all year, but locals point to two times: winter, and around June, when the fish are fattiest.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Winter</td><td>The traditional season, when kinmedai goes into hot pots [[s:shimoda_news,shizuoka_kinme_fat]].</td></tr>
<tr><td>Around June</td><td>Before spawning, when the fish carry the most fat. Shizuoka’s researchers measured the fat peaking in June [[s:shimoda_news,shizuoka_kinme_fat]].</td></tr>
<tr><td>Kinme Matsuri (all of June in 2016)</td><td>In 2016, the festival included a spot outside the fish market where you could watch the landings [[s:shimoda_news]].</td></tr>
</tbody></table></div>
<p>To give you an idea of what the festival looks like, here’s the 2016 example. The city’s June 2016 newsletter announced the Shimoda Kinme Matsuri for 1 to 30 June, with a viewing spot outside the fish market from about 7:30 to 9:00 a.m. There was no viewing on Tuesdays or Saturdays, and times could change or the viewing be cancelled in bad weather [[s:shimoda_news]]. We haven’t found an official notice for this year, so it’s best to check that it’s running before you plan a trip around it.</p>
[[ed:Confirm with the Shimoda Tourism Association whether the Kinme Matsuri ran in June 2026, and the dates and viewing times for 2027.]]

<h2>Why stay overnight instead of visiting for the day?</h2>
<p>Because the harbour does its business early, and you can’t get there in time from Tokyo on the day. The first Tokaido Line train leaves Tokyo at 5:20 and reaches Atami at 7:08, and the local train from Atami to Izukyu-Shimoda takes about another hour and a half (JR East timetable, November 2026) [[s:jre_tt_tokyo]]. That puts you in Shimoda well after the 7:30 start the city gave for the 2016 viewing, so plan to stay the night before. You can then wander down to the market in the morning and be at the canteen when it opens. Routes are in our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]].</p>
<p>Our home in Shimoda’s old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is about ten minutes on foot from the station. It has a properly equipped kitchen and a supermarket within walking distance, so you can cook whatever you find.</p>
[[ed:Name where guests can buy kinmedai to cook at home.]]
""",
 "faq": [
   ("Is kinmedai the same as red snapper?",
    "No. Kinmedai belongs to the alfonsino family (Berycidae), not the snapper or sea bream families [[s:tokyo_kinme_tag]]. “Golden-eye snapper” is just a market name."),
   ("Why is kinmedai so expensive?",
    "We think it’s mainly how it’s caught and how much. It lives deeper than 200 metres and is caught on hook-and-line gear, mostly vertical longlines [[s:fra_kinme,jfa_kinme_2021]]. Catches off Tokyo, Chiba, Kanagawa and Shizuoka fell from just under 7,000 tonnes a year in 2005–2009 to 3,797 tonnes in 2020 [[s:jfa_kinme_2021]]. A later national assessment found the 2023 breeding stock above its target level and rising [[s:chiba_kinme_r6]]."),
   ("Is kinmedai the same as nodoguro?",
    "No. Nodoguro is the market name for akamutsu, or blackthroat seaperch, a red fish from a different family (Acropomatidae) that lives in shallower water [[s:tokushima_akamutsu,ibaraki_akamutsu]]."),
   ("Can I eat kinmedai when I’m pregnant?",
    "Japan’s health ministry advises pregnant women to keep kinmedai to about one 80 g serving a week because of mercury, which is roughly five pieces of sushi [[s:mhlw_mercury2010]]. Your doctor or midwife can tell you what applies to you."),
   ("When is kinmedai in season?",
    "It’s landed all year. Winter is the traditional season, and the fish are fattiest around June [[s:shimoda_news,shizuoka_kinme_fat]]."),
   ("Can I see the kinmedai landings on a day trip from Tokyo?",
    "Not really. The first train from Tokyo reaches Atami at 7:08, and Shimoda is about an hour and a half further on [[s:jre_tt_tokyo]], so you’d arrive after the early-morning landings. Staying the night before is the easy way."),
   ("How do you say kinmedai?",
    "Roughly “kin-meh-dye”. Locals often shorten it to <em>kinme</em>."),
 ],
 "sources": ["shimoda_news", "pref", "shizuoka_kinme_fat", "fra_kinme", "chiba_kinme_r6", "jfa_kinme_2021",
             "tokyo_kinme_tag", "tokushima_akamutsu", "kyoto_akamutsu", "ibaraki_akamutsu", "mhlw_mercury2010",
             "tvtokyo", "tabimag", "jre_tt_tokyo"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "金目鯛とは：日本の「ゴールデンアイ・スナッパー」と、食べられる場所",
  "dek": "金目鯛は、日本中の寿司屋や旅館で出会う、赤い皮と金色の目の魚です。深い海の魚で、醤油と砂糖で煮る煮付けでよく食べられます。金目鯛の水揚げ日本一を名乗る下田の港は、食べに行くのにちょうどいい場所です。",
  "review": [
   "【2026-11-15 3回目の書き直し（事実の変更あり）】変えた点: ①日帰りの話: 「朝4時半ごろ出発」（根拠のない逆算）を消し、JR東日本の東京駅の時刻表（2026年11月、編集長が開いて確認）の事実に替えました。東京の始発の東海道線は5:20発・熱海7:08着、熱海から伊豆急下田は普通で約1時間半なので、日帰りでは朝の水揚げに間に合わない→前の晩に下田に泊まる、と書いています。出典は新しく jre_tt_tokyo。前の出典 jre_izu（2時間49分）は外しました。同じ内容の FAQ「東京から日帰りで水揚げを見られるか」を1問足しました ②見解を事実の形で書いていた所を直しました: 「多くの人は煮付けが目当て」「多くの人のお目当て」→「1回だけなら私たちは煮付けをすすめる」「私たちのおすすめ」、「生でも炙っても同じくらいおいしい」→「私たちの見方では」。In short・dek・description の「煮付けで知られる」も「よく煮付けにされる」に弱めました ③資源: 「その後、回復してきている（since）」をやめ、2つの評価を年を付けて別々に書きました。水産庁 2021年の評価＝2020年は「低位」、親魚量はそれまで5年ほど横ばい／千葉県が紹介する国の評価＝2023年の親魚量は目標の水準（MSY）を上回り増加。MSY は「資源を減らさずに、毎年いちばん多くとり続けられる水準」と平たく説明し、「避ける魚ではないが、たくさんいるわけでもない」と旅行者にとっての意味を1文で添えました ④祭り・見学: 出典を観光協会のページ（開けない）から下田市の広報 2016年6月号（shimoda_news、リサーチ部が開いて確認）に替え、「2016年の例では、6月1〜30日、市場の外の見学場所で朝7時半〜9時ごろ、火・土は休み、天候で変更・中止あり」と年を付けました。「今年の開催は公式の告知を見つけられていないので、確かめてから」と書いています。表の行も「きんめ祭り（2016年は6月いっぱい）」に。前の「火・土は漁が休みなので水揚げがない」は広報に理由が書かれていないので、「見学は休み」に直しました。旬の節の冒頭の「船を見たいなら6月がおすすめ」も消しました ⑤漁法: 「網ではなく延縄」（出典 jfa_kinme_mgmt は本文未確認）を、「関東の沖と伊豆諸島では、主に釣り（立縄・底立延縄）で、深い海に下ろす」に替えました。出典は jfa_kinme_2021・chiba_kinme_r6（どちらも開いて確認）。「網ではない」とは書いていません（同じ系群でも底刺し網などで獲る海域があるため）。jfa_kinme_mgmt は出典から外しました ⑥「なぜ高いか」と「のどぐろとの違い」の h2 を分けました（h2 は8個）。のどぐろの節は「のどぐろはまったく別の魚」から始めています。FAQ も「なぜ高いか」の次に「のどぐろと同じか」の順にしました",
   "【人に確かめてほしい点】①きんめ祭りが2026年6月に開かれたか、2027年の日程と見学の時間（黄色い枠。観光協会のページは開けていません） ②「なぜ高いか」は、事実を並べたうえで「私たちの見方」として書いています。この言い方でよいか ③「避ける魚ではないが、たくさんいるわけでもない」という読み手への一言が、資源の書き方として強すぎ・弱すぎでないか ④紹介している店（市場の食堂 金目亭。営業時間は静岡県の2025年3月更新のページ）を載せてよいか、ほかに案内している店（黄色い枠） ⑤ゲストが金目鯛を買える店（黄色い枠） ⑥深さ200メートルより深いこと（水産研究・教育機構）は前回の検索での確認のままです。公開前に照合してください ⑦見出しの写真は「焼いた赤い魚」で、本文のおすすめ（煮付け）とずれます。煮付けか水揚げの自社撮影の写真があると良くなります（手持ちの写真では替えられませんでした） ⑧「煮付けをすすめる」のは私たちの見方として書いています。運営者の感覚と合うか",
   "【入れられなかったこと】値段の目安（一次の出典なし）。2025年の資源の最新の数字（水産庁 2026年9月の資料は本文を開けていないため）。下田駅から魚市場の見学場所までの歩く時間（確認できず）",
  ],
  "points": [
    "金目鯛は、赤い皮と大きな金色の目をした深海魚。英語では splendid alfonsino や golden-eye snapper の名前で売られています。名前に「鯛」が付きますが、鯛やフエダイの仲間ではありません。のどぐろとも別の魚で、科が違い、すむ深さもずっと浅い魚です。",
    "身は一年中脂ののった白身。醤油と砂糖で煮る「煮付け」、刺身、さっと炙ったものなどで出てきます。私たちなら、まず煮付けを選びます。",
    "東京・千葉・神奈川・静岡の漁獲量は、2005〜09年の年7,000トン弱から、2020年には3,797トンに減りました。その後の国の評価では、2023年の親魚の量は目標の水準を上回り、増えています。深い海で釣ることと、とれる量が減ったことが、安くない理由だと私たちは見ています。",
    "伊豆半島の南端の下田は、金目鯛の水揚げ日本一の港だと説明しています。東京の始発で出ても朝の水揚げには間に合わないので、前の晩に泊まるのがおすすめです。",
  ],
  "body": """
<h2>金目鯛とはどんな魚か</h2>
<p>金目鯛は、赤い皮と大きな金色の目をした深海魚です。英語では splendid alfonsino（学名 <em>Beryx splendens</em>）や golden-eye snapper と呼ばれます。ふだんは水深200メートルより深い、大陸斜面や海の中の山のまわりにすんでいます[[s:fra_kinme,chiba_kinme_r6]]。下田市の広報によると、目は金色に輝き、水揚げから40分ほどで全身が赤くなるそうです[[s:shimoda_news]]。</p>
<p>漢字では「金目鯛」と書きますが、鯛の仲間でもフエダイ（スナッパー）の仲間でもなく、キンメダイ科という独自の科の魚です[[s:tokyo_kinme_tag]]。</p>

<h2>金目鯛はどんな味で、どうやって食べるのか</h2>
<p>脂のたっぷりのった白身です。下田市によると、深い海にすむので一年中脂がのっていて、だからどんな料理にも合うそうです[[s:shimoda_news]]。静岡県の水産の研究では、大きい魚ほど脂が多いことも分かっています[[s:shizuoka_kinme_fat]]。1回だけ食べるなら、私たちは醤油と砂糖で煮る「煮付け」をすすめます。ただ、生でも、さっと炙っても同じくらいおいしいと私たちは思います。</p>
<div class="tablewrap"><table>
<thead><tr><th>料理</th><th>どんなものか</th></tr></thead>
<tbody>
<tr><td><strong>煮付け</strong></td><td>丸ごと、または厚い切り身を、たれに照りが出るまで煮たもの。最初の1回に、私たちがすすめる食べ方です。</td></tr>
<tr><td><strong>刺身と炙り</strong></td><td>生の切り身や、皮目をさっと炙った切り身です。</td></tr>
<tr><td><strong>しゃぶしゃぶ</strong></td><td>薄切りを、卓上の熱い出汁にくぐらせて食べます。</td></tr>
<tr><td><strong>そのほか</strong></td><td>旅のメディア「旅マガジン」は、金目鯛のラーメン、バーガー、コロッケも紹介しています[[s:tabimag]]。</td></tr>
</tbody></table></div>
<p>丸ごと買うなら、同じ広報によると、新鮮なものは目が澄んだ金色で、皮が鮮やかな赤。古くなるとどちらも白っぽくなります[[s:shimoda_news]]。</p>

<h2>金目鯛はなぜ高いのか</h2>
<p>私たちは、とり方と、とれる量が大きいと見ています。関東の沖と伊豆諸島では、金目鯛は主に釣りでとります。おもに「立縄」と「底立延縄」で、深い海まで仕掛けを下ろします[[s:jfa_kinme_2021,chiba_kinme_r6]]。東京・千葉・神奈川・静岡の漁獲量は、2005〜09年は年7,000トン弱で安定していましたが、2020年には3,797トンに減りました[[s:jfa_kinme_2021]]。</p>
<p>資源の評価は、年によって少し違う内容なので、年を付けて分けて書きます。水産庁の2021年の評価では、2020年の資源は「低位」で、親魚の量はそれまでの5年ほど横ばいでした[[s:jfa_kinme_2021]]。その後、千葉県によると、国の評価では2023年の親魚の量が目標の水準を上回り、増えていると判断されました[[s:chiba_kinme_r6]]。</p>
<p>この目標の水準（MSY）は、資源を減らさずに、毎年いちばん多くとり続けられる量の目安です。旅行者にとっては、避けるべき魚ではないけれど、たくさんいるわけでもない、ということです。千葉県の水揚げは2023年に1,467トンで、2007年の2,263トンには届いていません[[s:chiba_kinme_r6]]。</p>

<h2>金目鯛とのどぐろは、どう違うのか</h2>
<p>のどぐろは、まったく別の魚です。「アカムツ」の呼び名で、口の中が黒いのが名前の由来です[[s:kyoto_akamutsu]]。どちらも赤くて高級なので、混同されがちです。のどぐろはホタルジャコ科という別の科で、目（もく）も違います[[s:tokushima_akamutsu,tokyo_kinme_tag]]。すむ深さも80〜150メートルほどと、ずっと浅い所です[[s:ibaraki_akamutsu]]。メニューに両方あれば、2つの違う魚から選んでいることになります。</p>

<h2>妊娠中に金目鯛を食べてもいいか</h2>
<p>厚生労働省は、水銀のために、妊婦が食べる量を「週1回・1回約80gまで」とする魚に、メカジキ、クロマグロ、メバチと並んで金目鯛を入れています[[s:mhlw_mercury2010]]。同じ注意事項では、寿司や刺身1貫は約15gなので、80gは寿司でだいたい5貫です。これはおなかの赤ちゃんを守るための目安で、子どもやほかの大人向けではありません[[s:mhlw_mercury2010]]。一般向けの目安で、医療の助言ではないので、妊娠中なら、かかりつけの医師や助産師に聞くのがいちばんです。</p>

<h2>なぜ下田で食べるのがいいのか</h2>
<p>[[l:izu|伊豆半島]]の南端にある下田は、金目鯛の水揚げ日本一の港だと説明しています。下田市が2016年6月号の広報でそう書いていて、静岡県も2025年3月更新のページで、下田市魚市場を同じように紹介しています[[s:shimoda_news,pref]]。</p>
<p>地元では、2つの呼び名を耳にするかもしれません。2014年のテレビ東京の下田の番組では、「地金目」は大島から神津島にかけての近海でとれたもの、「沖金目」はもっと遠くの漁場でとれたもの、と説明していました[[s:tvtokyo]]。</p>
<p>手始めにいちばん行きやすいのは、下田市魚市場の中にある食堂「市場の食堂 金目亭」で、伊豆急下田駅から歩いて約10分です。金目鯛を3通りで味わう丼や、丸ごとの煮付けの定食があります。静岡県のページによると、朝定食が7時〜9時30分、昼が11時〜15時で、火曜が定休日です（[[a:pref]]、2025年3月更新）。営業時間は変わることがあるので、出かける前にさっと確かめておくと、無駄足になりません。</p>
[[ed:実際にゲストへ案内している店を2〜3軒、家からの徒歩時間と、そこで頼むものを添えて入れてください。]]

<h2>金目鯛の旬はいつか</h2>
<p>金目鯛は一年中揚がりますが、地元で挙がる時期は2つあります。冬と、脂がいちばん乗る6月ごろです。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>理由</th></tr></thead>
<tbody>
<tr><td>冬</td><td>鍋の季節で、昔からの旬とされる時期です[[s:shimoda_news,shizuoka_kinme_fat]]。</td></tr>
<tr><td>6月ごろ</td><td>産卵の前で、脂がいちばん多い時期。静岡県の研究では、脂が最も多いのは6月でした[[s:shimoda_news,shizuoka_kinme_fat]]。</td></tr>
<tr><td>きんめ祭り（2016年は6月いっぱい）</td><td>2016年の祭りでは、魚市場の外に水揚げを見られる場所がありました[[s:shimoda_news]]。</td></tr>
</tbody></table></div>
<p>祭りの様子の目安として、2016年の例を挙げます。下田市の2016年6月号の広報は、6月1日から30日まで「下田きんめ祭り」を開くと知らせていて、魚市場の外の見学場所で、朝7時半から9時ごろまで水揚げを見られました。火曜と土曜は見学が休みで、天候で時間が変わったり、中止になったりすることもありました[[s:shimoda_news]]。今年の公式の告知は見つけられていないので、祭りに合わせて旅を組むなら、開かれるかを先に確かめておくのがおすすめです。</p>
[[ed:きんめ祭りが2026年6月に開かれたか、2027年の日程と見学の時間を、伊豆下田観光協会に確かめてください。]]

<h2>日帰りではなく、泊まったほうがいい理由</h2>
<p>港は朝早くに動くのに、東京からはその日のうちに間に合わないからです。東京の始発の東海道線は5:20発で熱海に7:08に着き、熱海から伊豆急下田までは普通列車でさらに1時間半ほどかかります（JR東日本の時刻表、2026年11月）[[s:jre_tt_tokyo]]。これだと、2016年の見学で市が示した朝7時半の始まりにはとても間に合わないので、前の晩に下田に泊まるのがおすすめです。そうすれば、朝のんびり市場まで歩いて行って、開店と同時に食堂に入れます。行き方は、[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田の旧町内にある私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、駅から歩いて約10分。調理器具のそろったキッチンがあり、スーパーも歩いて行けるので、見つけた魚を自分で料理できます。</p>
[[ed:ゲストが金目鯛を買える店の名前を入れてください。]]
""",
  "faq": [
    ("金目鯛は、レッドスナッパーと同じですか",
     "違います。金目鯛はキンメダイ科の魚で、名前に「鯛」が付くだけです。鯛の仲間でも、スナッパー（フエダイ）の仲間でもありません[[s:tokyo_kinme_tag]]。「golden-eye snapper」は流通で使われる呼び名です。"),
    ("金目鯛はなぜ高いのですか",
     "とり方と、とれる量が大きいと私たちは見ています。水深200メートルより深い所にすみ、主に釣り（おもに立縄）でとります[[s:fra_kinme,jfa_kinme_2021]]。東京・千葉・神奈川・静岡の漁獲量は、2005〜09年の年7,000トン弱から2020年には3,797トンに減りました[[s:jfa_kinme_2021]]。その後の国の評価では、2023年の親魚の量は目標の水準を上回り、増えています[[s:chiba_kinme_r6]]。"),
    ("金目鯛とのどぐろは同じ魚ですか",
     "違います。のどぐろは「アカムツ」の呼び名で、ホタルジャコ科という別の科の赤い魚です。金目鯛より浅い所にすんでいます[[s:tokushima_akamutsu,ibaraki_akamutsu]]。"),
    ("妊娠中に金目鯛を食べてもいいですか",
     "厚生労働省は、水銀のために、妊婦は金目鯛を「週1回・1回約80gまで」にするよう勧めています。寿司ならだいたい5貫です[[s:mhlw_mercury2010]]。自分の場合どうかは、医師や助産師に聞いてください。"),
    ("金目鯛の旬はいつですか",
     "一年中揚がります。昔からの旬は冬で、脂がいちばん乗るのは6月ごろです[[s:shimoda_news,shizuoka_kinme_fat]]。"),
    ("東京から日帰りで、金目鯛の水揚げを見られますか",
     "あまり現実的ではありません。東京の始発でも熱海に着くのは7:08で、下田はそこから1時間半ほど先です[[s:jre_tt_tokyo]]。朝早い水揚げには間に合わないので、前の晩に泊まるのが楽です。"),
    ("kinmedai はどう発音しますか",
     "英語を話す人には “kin-meh-dye” が近い音です。地元では「キンメ」と略すこともよくあります。"),
  ],
 },
}
