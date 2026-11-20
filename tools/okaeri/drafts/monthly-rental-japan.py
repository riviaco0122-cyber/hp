# -*- coding: utf-8 -*-
"""monthly-rental-japan の新規記事（2026-11-16 執筆部）。構成案とリサーチメモ: tools/okaeri/briefs/monthly-rental-japan.md。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "jta_minpaku_overview": ("https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/index_en.html", "Japan Tourism Agency", "観光庁（民泊制度ポータル）",
                             "Japan Tourism Agency, Minpaku portal: What is private lodging? (checked November 2026)"),
    "jta_minpaku_act": ("https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/law1_en.html", "Japan Tourism Agency (Private Lodging Business Act)", "観光庁（住宅宿泊事業法とは）",
                        "Japan Tourism Agency, Minpaku portal: About the Private Lodging Business Act (checked November 2026)"),
    "jta_minpaku_users": ("https://www.mlit.go.jp/kankocho/minpaku/environment_en.html", "Japan Tourism Agency (for guests)", "観光庁（安心できる民泊環境）",
                          "Japan Tourism Agency, Minpaku portal: Safety-assured private lodging (checked November 2026)"),
    "jta_minpaku_illegal": ("https://www.mlit.go.jp/kankocho/minpaku/announcement.html", "Japan Tourism Agency (illegal minpaku)", "観光庁（違法民泊の利用はやめましょう）",
                            "Japan Tourism Agency: To guests — please don’t use illegal minpaku (checked November 2026)"),
    "jta_listing_rules": ("https://www.mlit.go.jp/kankocho/content/001218228.pdf", "Japan Tourism Agency, 2018", "観光庁 2018年（違法物件の掲載防止）",
                          "Japan Tourism Agency: Main points of the measures to prevent illegal properties on booking sites (2018)"),
    "jta_listing_page": ("https://www.mlit.go.jp/kankocho/minpaku/business/mediation/prevention.html", "Japan Tourism Agency (booking sites)", "観光庁（違法物件の掲載の防止について）",
                         "Japan Tourism Agency: Preventing illegal listings on booking sites (checked November 2026)"),
    "jta_cancel_2018": ("https://www.mlit.go.jp/kankocho/content/001244950.pdf", "Japan Tourism Agency, June 2018", "観光庁 2018年6月",
                        "Japan Tourism Agency: Handling of reservations at illegal properties after the Private Lodging Business Act took effect (1 June 2018)"),
    "jta_short_lease_2018": ("https://www.mlit.go.jp/kankocho/content/001260338.pdf", "Japan Tourism Agency and MHLW, 2018", "観光庁・厚生労働省 2018年",
                             "Japan Tourism Agency and Ministry of Health, Labour and Welfare: Handling of short-term rental properties by booking sites (6 November 2018)"),
    "mhlw_passport": ("https://www.mhlw.go.jp/content/000659685.pdf", "Ministry of Health, Labour and Welfare, 2020", "厚生労働省 2020年",
                      "MHLW: Published reply on storing passport copies with the guest register (April 2020)"),
    "mlit_foreign_rental": ("https://www.mlit.go.jp/common/001265432.pdf", "Ministry of Land, Infrastructure, Transport and Tourism", "国土交通省（外国人の民間賃貸住宅入居円滑化ガイドライン）",
                            "MLIT: Guideline for facilitating rental housing for foreign nationals, chapter 2 (Q&A)"),
    "mlit_fixed_term": ("https://www.mlit.go.jp/jutakukentiku/house/teishaku/111215-4.htm", "MLIT (fixed-term leases)", "国土交通省（定期借家権Q&A）",
                        "MLIT: Q&A on fixed-term building leases"),
    "jnto_visa": ("https://www.japan.travel/en/plan/visa-info/visa-immigration/", "JNTO", "日本政府観光局（入国とビザ）",
                  "JNTO: Entry into Japan and visa information (checked November 2026)"),
    "estat_rent_2025": ("https://www.e-stat.go.jp/dbview?sid=0003420453", "Statistics Bureau of Japan, 2025", "総務省統計局 小売物価統計調査 2025年",
                        "Statistics Bureau of Japan: Retail Price Survey, annual average prices 2025 — private rent"),
    "stat_rent_note": ("https://www.stat.go.jp/data/kouri/doukou/2024np/pdf/riyou2024.pdf", "Statistics Bureau of Japan (survey notes)", "総務省統計局（小売物価統計調査 利用上の注意）",
                       "Statistics Bureau of Japan: Retail Price Survey, notes for users 2024"),
    "shimoda_gomi": ("https://www.city.shimoda.shizuoka.jp/category/020100gomi_recycle/110876.html", "Shimoda City", "下田市（家庭ごみの分け方・出し方）",
                     "Shimoda City: How to sort and put out household rubbish (in Japanese)"),
}

ARTICLE = {
 "id": "monthly-rental", "slug": "monthly-rental-japan", "topic": "live", "place": None, "also": ["stay"],
 "photo": ("studio-apartment", "A small furnished studio with a compact kitchen, a dining table and a long wooden floor", ""),
 "published": "2026-11-16", "updated": "2026-11-16",
 "kicker": "Live part-time",
 "h1": "Monthly rentals in Japan: how to rent a place for a month",
 "seo_title": "Monthly Rental in Japan: How to Rent a Place for a Month",
 "description": "A month in Japan usually means a monthly apartment or a licensed holiday rental, not an ordinary lease. What’s included, and what to ask first.",
 "dek": "An ordinary Japanese lease usually isn’t an option for a visitor. For a month, you’re looking at a monthly apartment or a licensed holiday rental with monthly rates.",
 "card": "Ordinary leases in Japan run for years and need a guarantee, so a month means a monthly apartment or a licensed holiday rental. Compare the total cost, check the listing’s licence number, and ask about the things you’ll live with every day.",
 "keywords": [("monthly rental in japan", "—", "—"), ("monthly rental japan", "170", "16"), ("rent a house in japan", "1,300", "41"),
              ("long term stay japan / one month in japan", "50〜90", "0〜18")],
 "intent": "Do（やり方・何を選ぶか）",
 "points": [
   "Ordinary leases usually run for two years and need a rent guarantee, so they rarely suit a one-month stay.",
   "Monthly apartments and licensed holiday rentals with monthly rates are the realistic choices for a visitor.",
   "Registered booking sites show a legal rental’s licence or notification number, and you’ll be asked for your passport.",
 ],
 "body": """
<p>A month is too long for a hotel to feel like home, and far too short for a normal Japanese lease. Japan has a few legal ways to fill that gap, and they aren’t the same thing in law. That difference decides who cleans, what you pay and what happens if a listing turns out to be illegal.</p>

<h2>Can a visitor rent a place in Japan for a month?</h2>
<p>Yes, but usually not with an ordinary lease. You’ll want a place that’s set up to be let by the month.</p>
<p>An ordinary Japanese lease usually runs for two years, and landlords normally want a guarantee for the rent, either from a rent-guarantee company or by a joint guarantor [[s:mlit_foreign_rental]]. The government’s guideline for landlords tells them to check a foreign applicant’s status of residence first. It also notes that if your permission to stay ends before the lease does, the contract can end early [[s:mlit_foreign_rental]].</p>
<p>Then there’s the money up front. Key money (<em>reikin</em>) of one to two months’ rent is common in the Kanto region and isn’t refunded, and a deposit of about the same is returned after deductions [[s:mlit_foreign_rental]]. In our view, that rules out an ordinary lease for most people coming for a month. The good news is that Japan has places built for exactly this kind of stay.</p>

<h2>Monthly apartment, holiday rental or share house: which suits a month?</h2>
<p>For most visitors, it comes down to a monthly apartment or a licensed holiday rental. The difference is mostly legal, but it changes who cleans, what’s included and how you book.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Type</th><th>What it is in law</th><th>Shortest stay</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Monthly apartment</strong> (“monthly mansion”)</td><td>A short-term lease: a rental, not lodging [[s:jta_short_lease_2018]]</td><td>Usually a month [[s:jta_short_lease_2018]]</td><td>A furnished flat let by the month. You sign a rental contract, so read what the rent covers.</td></tr>
<tr><td><strong>Licensed holiday rental</strong> (<em>minpaku</em>)</td><td>A home notified to the authorities under the Private Lodging Business Act [[s:jta_minpaku_overview]]</td><td>Set by the host</td><td>It can host guests on no more than 180 nights a year, and local rules can cut that further [[s:jta_minpaku_act]].</td></tr>
<tr><td><strong>Guesthouse or holiday home</strong> with a lodging licence</td><td>Licensed under the Hotel Business Act, for example as simple lodging [[s:jta_minpaku_overview]]</td><td>Set by the host</td><td>There’s no yearly limit on operating days, so it can take guests all year [[s:jta_minpaku_overview]].</td></tr>
<tr><td><strong>Share house</strong></td><td>Usually a rental, on terms set by each operator</td><td>Set by the operator</td><td>Your own bedroom, with the kitchen and bathroom shared. Terms vary a lot, so it helps to get them in writing.</td></tr>
</tbody></table></div>
<p>Why does a monthly apartment usually ask for at least a month? Japan’s tourism and health authorities treat a stay of under a month as, in principle, lodging. Their guidance for booking sites is that a short-term lease should normally require at least a month and say clearly that it’s a rental, though a local authority can use a different yardstick [[s:jta_short_lease_2018]]. The same notice says monthly apartments shouldn’t be listed next to short-stay holiday rentals on the same site, so you’ll often find them in different places [[s:jta_short_lease_2018]].</p>
<p>The two give you different things, too. With lodging, keeping the room clean is the operator’s job, and you’re a guest rather than someone who lives there. With a lease, the place is your home for the length of the contract [[s:jta_short_lease_2018]]. Whichever you choose, it’s worth asking who cleans, and how often.</p>
<p>You may also see the term fixed-term lease (<em>teiki shakuya</em>). It’s a type of Japanese lease, not another name for a monthly apartment, and what it means for you is that you can’t count on extending. It ends on the date in the contract and isn’t renewed, though you and the landlord can agree a new one. It has to be in writing, and the landlord must explain in a separate document that it won’t be renewed [[s:mlit_fixed_term]].</p>

<h2>What does a month cost, and what’s included?</h2>
<p>A month costs the rent plus cleaning, utilities, internet, any deposit and booking fees, so the total is what to compare. Prices vary too much from place to place for one figure to help, but the parts of the bill are much the same everywhere.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What you pay for</th><th>Why it matters</th><th>What to ask</th></tr></thead>
<tbody>
<tr><td>Rent or nightly rate</td><td>The figure you see first, and the one that’s easiest to compare</td><td>Is there a weekly or monthly discount, and is it already in this price?</td></tr>
<tr><td>Cleaning</td><td>It can be a one-off fee, regular cleans during the stay, or nothing at all</td><td>Is cleaning included during the stay, and how often?</td></tr>
<tr><td>Electricity, gas and water</td><td>They can be included, capped or charged by what you use</td><td>Is there a cap, and what happens if you go over it?</td></tr>
<tr><td>Internet</td><td>A slow line is hard to live with for a month if you work</td><td>Is it fixed broadband or a mobile router?</td></tr>
<tr><td>Deposit</td><td>Money you’ll want back at the end</td><td>Is there one, and when and how is it returned?</td></tr>
<tr><td>Booking site fees</td><td>The price you first see may not be the final total</td><td>Does the total include the booking site’s service fee?</td></tr>
<tr><td>Leaving early</td><td>Plans change over a month</td><td>If you leave early, are any unused nights refunded?</td></tr>
</tbody></table></div>
<p>Monthly rates exist for a reason. From the host’s side, a longer stay means fewer cleans between guests. That’s why, when we opened our first place to stay, we added weekly and monthly discounts. If a listing doesn’t show one, there’s no harm in asking.</p>

<h2>How can you tell a holiday rental is legal?</h2>
<p>Look for a notification or licence number on the listing. Since June 2018, anyone offering paid stays in a home in Japan has needed one of three things: a Hotel Business Act licence, special-zone certification, or a notification under the Private Lodging Business Act [[s:jta_minpaku_overview]].</p>
<p>Booking sites registered as minpaku agents have to show each listing’s notification number or similar licence details [[s:jta_listing_rules]]. The Japan Tourism Agency suggests checking that the registration number and the property’s address can be confirmed on the site [[s:jta_minpaku_users]]. A place with a lodging licence shows a licence number rather than a notification number, so the format won’t always look the same. We know this from the host’s side: until our licence came through, we couldn’t take bookings on Airbnb.</p>
<p>For a month-long stay, this matters because an illegal listing can vanish. Registered sites report their listings to the agency every six months and must promptly remove illegal ones when asked [[s:jta_listing_page]]. When the law took effect in June 2018, booking sites had to cancel future reservations at unregistered properties or move guests to legal ones [[s:jta_cancel_2018]]. The agency’s advice is to book minpaku only through registered sites or travel agencies [[s:jta_minpaku_illegal]].</p>
<p>The 180-night limit on a minpaku is the host’s limit, not yours. It’s counted per property, in a year that starts at noon on 1 April [[s:jta_minpaku_act]], so it only means that kind of home can’t be let all year.</p>
<p>Why does the host want your passport? Because the law asks them to. Under the Private Lodging Business Act, foreign guests without an address in Japan give their nationality and passport number. The host then keeps a copy of the passport [[s:jta_minpaku_users]]. Places with a lodging licence work the same way: the guest register includes those details, and the health ministry asks operators to see the passport and keep a copy [[s:mhlw_passport]]. At three homes our team helps run, questions about the guest register were among the most common we got, so you’re not alone in wondering.</p>

<h2>What should you ask before booking a whole month?</h2>
<p>The things you’ll live with every day, not just what’s in the photos. These are the questions we’d want answered, in the order we’d ask them.</p>
<ol>
<li><strong>Internet.</strong> Is it fixed broadband, and where’s the router if it needs restarting? If you’ll be on video calls, a proper desk matters as much as the speed.</li>
<li><strong>Electricity.</strong> How much can you run at once? In our first flat, the old two-wire wiring couldn’t run the air conditioner, fridge and microwave together, so knowing where the breaker box is helps too.</li>
<li><strong>Heating and cooling.</strong> Is there an air conditioner in the room you’ll sleep in, and is the electricity for it included?</li>
<li><strong>Washing.</strong> Is there a washing machine, and a dryer? Our guests have praised both in their reviews, and a month of rainy-season laundry explains why.</li>
<li><strong>Rubbish.</strong> How does it work on a long stay? Each town has its own sorting rules and collection days. In Shimoda, for example, the city’s guide is in Japanese [[s:shimoda_gomi]]. At the three homes our team helps run, a small number of reviews from long stays mentioned smells from the bin area.</li>
<li><strong>Cleaning and bedding.</strong> Is there a clean or a change of sheets during the stay, or is it all on you?</li>
<li><strong>Stairs and bathroom.</strong> Which floor is it on, is there a lift, and is there a bath or only a shower? At one of the homes our team helps run, explaining the steep stairs before people booked went down well.</li>
<li><strong>Getting around.</strong> Is there parking, or a bus stop and a supermarket within walking distance?</li>
<li><strong>Leaving early.</strong> If your plans change, what happens to the nights you don’t use?</li>
</ol>
<p>To show what useful answers look like, here’s how we’d answer for our own flat, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>. It’s a whole flat of about 40 m², up about 13 steps, with a shower but no bathtub [[s:node_room]]. There’s a work desk, fast Wi-Fi, and a free washing machine and gas dryer [[s:node_room]]. The electrical supply is small, so we ask guests to switch the air conditioner off for a moment while they use the microwave, vacuum cleaner or hairdryer [[s:node_room]]. Burnable rubbish goes in the bin, rinsed cans and bottles stay in the kitchen, and long-stay guests get in touch with us about the rest [[s:node_room]].</p>

<h2>Is it harder to rent for a month outside Tokyo?</h2>
<p>There’s less to choose from, but it’s very doable if you start early. We think you’ll find fewer monthly apartments in a small town, and more guesthouses and holiday homes that offer monthly rates.</p>
<p>Housing does get cheaper away from the capital. In 2025, private rent averaged ¥9,803 per 3.3 m² a month in Tokyo’s 23 wards and ¥4,621 in Shizuoka City [[s:estat_rent_2025]]. That’s ordinary-lease rent across surveyed homes, not the price of a monthly apartment [[s:stat_rent_note]], but it gives you a sense of the gap.</p>
<p>Getting around matters more, too. Buses can be few, so a place within walking distance of a supermarket makes daily life much easier without a car. Seaside towns also fill up in summer. In Shimoda, where we host, summer brings people for the beaches and surfing, so a month in July or August needs booking well ahead.</p>
<p>If you want a small town that’s still easy to reach, the Izu Peninsula is one option. As of November 2026, the daily direct trains from Tokyo Station reach Shimoda in 2 hours 29 to 44 minutes [[s:jre_tt_tokyo]]. Our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] has the routes.</p>
<p>You may also read about towns’ trial homes (<em>otameshi jutaku</em>). They’re mostly for people planning to move. Shizuoka City’s, for example, are for people living outside Shizuoka Prefecture who are thinking of moving there and have talked to its relocation advisers first [[s:shizuoka_trial]]. We look at them in [[l:akiya-try-first|living in a town for a month before you buy]].</p>

<h2>Do you need a visa to stay for a month?</h2>
<p>For many visitors, no. As of November 2026, passport holders of many countries and regions can visit Japan for tourism without a visa, most for up to 90 days. Some nationalities are given 15, 30 or 180 days instead [[s:jnto_visa]].</p>
<p>On that kind of stay you can’t do paid work, and the rule for your own passport is the one that counts [[s:jnto_visa]]. If you’d like to work remotely from Japan for longer, [[l:digital-nomad|Japan’s digital nomad visa]] allows a stay of up to six months for some nationalities [[s:isa_nomad_en]]. Our guide to [[l:how-long-stay|how long you can stay in Japan]] covers the other options, from extensions to longer statuses.</p>
<p class="fine">This is general information, not legal or immigration advice. Rules can change, so check the official pages for your own case.</p>
""",
 "faq": [
   ("Can I rent an apartment in Japan on a tourist visa?",
    "An ordinary lease usually isn’t realistic. It typically runs for two years, needs a rent guarantee, and the landlord checks your status of residence first [[s:mlit_foreign_rental]]. For a month, a monthly apartment or a licensed holiday rental with monthly rates is the usual choice."),
   ("Is it legal to rent an Airbnb in Japan for a month?",
    "Yes, if the place is licensed or notified. Registered booking sites have to show the listing’s notification number or licence details [[s:jta_listing_rules]]. A minpaku can host guests on up to 180 nights a year, while a place with a lodging licence has no yearly limit [[s:jta_minpaku_overview]]."),
   ("Why does a Japanese host need a copy of my passport?",
    "Because the law asks them to. If you’re a foreign national without an address in Japan, hosts record your nationality and passport number and keep a copy of your passport, both in minpaku and in licensed lodging [[s:jta_minpaku_users,mhlw_passport]]."),
   ("Are utilities and Wi-Fi included in a monthly rental?",
    "It depends on the place. Some include them, some set a cap and some charge for what you use, so it’s best to ask before you book and to compare the total rather than the monthly rate."),
   ("Is it easy to find a monthly rental outside Tokyo?",
    "There’s less choice, so start early. We think guesthouses and holiday homes with monthly rates make up much of what’s on offer in small towns, and seaside towns fill up in summer."),
 ],
 "sources": ["mlit_foreign_rental", "jta_short_lease_2018", "mlit_fixed_term", "jta_minpaku_overview", "jta_minpaku_act", "jta_listing_rules", "jta_minpaku_users",
             "jta_listing_page", "jta_cancel_2018", "jta_minpaku_illegal", "mhlw_passport", "shimoda_gomi", "node_room", "estat_rent_2025", "stat_rent_note",
             "jre_tt_tokyo", "shizuoka_trial", "jnto_visa", "isa_nomad_en"],
 "related": ["digital-nomad", "akiya-try-first", "izu-from-tokyo"],
 "ja": {
  "h1": "日本で1か月、部屋を借りるには",
  "dek": "日本のふつうの賃貸は、旅行で来る人にはたいてい選べません。1か月なら、マンスリーの部屋か、月割のある許可・届出済みの貸し部屋（民泊など）を探すことになります。",
  "review": [
   "【2026-11-17 品質保証部（原稿 89点・ゲート1）の指摘での書き直し】変えた点: ①【ゲート】ごみ: 「下田市の案内は日本語だけ」→「日本語で書かれている」（確かめた範囲だけ。英語版の有無は書いていません） ②【言い方の変更】2018年11月の通知は「原則1か月が望ましい・自治体に別の目安があればそれで判断」までなので、「決まって1か月以上」→「たいてい1か月以上」、表の最短を「たいてい1か月」にし、「自治体が別の目安を使うこともある」を足しました ③ビザの節に「2026年11月時点」 ④宿泊と賃貸の違いの文を「宿泊では掃除は運営者の仕事で、あなたは住む人ではなく泊まる客。賃貸では契約の期間そこがあなたの住まい」に書き直しました ⑤定期借家の段落に「日本の賃貸契約の種類の1つで、マンスリーの別名ではない」「借りる側にとっては延長をあてにできない」を足しました ⑥費用の節の最初の文を、内訳（家賃・清掃・光熱費・ネット・保証金・手数料）を挙げて「比べるのは合計」と言い切る形に ⑦3物件のごみ置き場のにおいを「長期滞在のレビューの一部」に ⑧In short の3項目めを「登録した予約サイトでは、掲載に許可番号か届出番号が出る」と、予約サイトの掲載の話と分かる形に ⑨人に確かめてほしい点から、写真（編集長が studio-apartment を入れ済み）と、ノマドの記事へのリンクの扱い（同時に公開する前提）を消しました",
   "【2026-11-16 新規（執筆部）】書いた点: ①1記事1主張は「1か月なら、ふつうの賃貸ではなく“1か月から借りられる合法の部屋”を選び、合計の費用と暮らしの設備を予約の前に確かめる」 ②h2 は構成案どおり7つ（借りられるか／種類の比較表／費用の内訳表／合法かの見分け方とパスポート／予約前に聞くことの番号つきリスト／東京の外／ビザ）、FAQ 5問 ③事実はリサーチメモの公的な出典だけで書きました（国交省の外国人の賃貸ガイドライン・定期借家Q&A、観光庁の民泊ポータルと2018年の通知、厚労省の回答、日本政府観光局のビザのページ、総務省の小売物価統計、下田市のごみのページ、NODE Shimoda の公式サイト）。リサーチメモで「書かない」と決めた10件（マンスリー＝定期借家と言い切る、在留カード必須と言い切る、法律で2年、JESTA、査証免除の国名、伊豆の町のお試し住宅、下田市のごみの英語版、マンスリーの相場、NODE Shimoda のいまの週割・月割、2018年の削除件数）は書いていません ④黄色い枠はありません",
   "【自社の体験の使い方（experience.md の人が確認済みの節だけ）】3-2: 開業時に週割・月割を付けた（過去形。「最初の宿」とだけ書き、いまの割引・月額・30泊以上は書いていません）／許可番号が出るまで Airbnb で予約を受けられなかった／古い2芯の配線でエアコン・冷蔵庫・電子レンジを同時に使えなかった／洗濯機と乾燥機がレビューで評価された／夏は海水浴・サーフィンの客が来る。9章: 「私たちのチームが関わる3つの家」として、名簿の質問が多い種類の1つだった・長期滞在のゴミ置き場のにおいの指摘が少しあった・急な階段を予約前に説明したことが好評だった（エリア・件数・自社運営か支援かは書いていません）",
   "【NODE Shimoda に触れるのは節5の最後の1回】公式サイトの客室のページの事実だけ: 約40㎡の一室・階段約13段・シャワーのみでバスタブなし・ワークデスク・高速 Wi-Fi・無料の洗濯機とガス乾燥機・電気の容量が小さいので電子レンジ・掃除機・ドライヤーの間はエアコンを一時止めてもらう・燃えるごみは袋へ、缶やびんはすすいで台所へ、長期滞在はごみについて連絡してもらう。“house” とは呼ばず “flat” にしています。英国英語の “second floor” は日本の3階の意味になるので、階数は書かず「階段約13段」にしました",
   "【検索語】構成案の主な語は “monthly rental japan” ですが、題の “Monthly Rental in Japan” にそのまま入らないため、keywords の先頭を同じ検索の自然な形 “monthly rental in japan” にし、“monthly rental japan”（170・KD16）を2番目に残しました（akiya-try-first の “buying an akiya in japan” と同じ扱い）",
   "【人に確かめてほしい点】①出典 jnto_visa は akiya-try-first の下書きと同じ定義（URL も同じ）にしてあります。リサーチメモでは転送先の /visa-info/ を挙げていますが、同じページです ②法律・制度の記述（playbook 6章）: 賃貸のガイドライン、定期借家、民泊の180日・届出番号の表示・2018年の取り消し、1か月未満は宿泊として扱う通知（2018年11月）、パスポートの写しの保存、ビザなしの滞在日数。どれも 2026-11-16 にリサーチ部が公式ページで確かめたものです ③変わりやすい数字: 下田までの直通 2時間29〜44分（2026年11月の時刻表）、2025年の民営家賃（東京都区部 3.3㎡あたり月9,803円・静岡市 4,621円）",
  ],
  "points": [
    "ふつうの賃貸は2年契約が多く、家賃の保証も求められるので、1か月の滞在にはまず向きません。",
    "旅行で来る人に現実的なのは、マンスリーの部屋か、月割のある許可・届出済みの貸し部屋です。",
    "登録した予約サイトでは、合法の貸し部屋の掲載に許可番号か届出番号が出ていて、泊まるときはパスポートを求められます。",
  ],
  "body": """
<p>1か月は、ホテルでは落ち着かないほど長く、日本のふつうの賃貸を借りるには短すぎます。そのすき間を埋める合法の方法はいくつかありますが、法律の上では同じものではありません。その違いで、掃除を誰がするか、何にお金を払うか、掲載が違法だったときにどうなるかが変わります。</p>

<h2>旅行で来た人が、日本で1か月部屋を借りられるか</h2>
<p>借りられます。ただ、ふつうの賃貸ではなく、1か月単位で貸す前提の部屋を探すことになります。</p>
<p>日本のふつうの賃貸は、たいてい2年契約で、家賃の保証を求められるのがふつうです。保証会社を使うか、連帯保証人を立てます[[s:mlit_foreign_rental]]。国の大家さん向けのガイドラインでは、外国人の申し込みでは、まず在留資格を確かめるよう書かれています。在留期間が契約期間より先に切れると、契約が途中で終わることがある、とも書かれています[[s:mlit_foreign_rental]]。</p>
<p>最初に払うお金もあります。関東では家賃の1〜2か月分の礼金がよくあり、戻ってきません。同じくらいの敷金は、差し引きのあとで戻ります[[s:mlit_foreign_rental]]。私たちの見方では、1か月だけ来る人の多くにとって、ふつうの賃貸は選択肢に入りません。うれしいことに、日本にはちょうどこういう滞在のための部屋があります。</p>

<h2>マンスリー、民泊、シェアハウス：1か月に向くのはどれか</h2>
<p>多くの人は、マンスリーの部屋か、許可・届出済みの貸し部屋かのどちらかになります。違いはおもに法律の上のものですが、掃除を誰がするか、何が含まれるか、どう予約するかが変わります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>種類</th><th>法律の上では</th><th>最短の日数</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>マンスリーの部屋</strong>（マンスリーマンション）</td><td>短期の賃貸借。宿泊ではなく賃貸です[[s:jta_short_lease_2018]]</td><td>たいてい1か月[[s:jta_short_lease_2018]]</td><td>家具付きの部屋を月単位で借ります。賃貸の契約を結ぶので、家賃に何が含まれるかを読んでおきます。</td></tr>
<tr><td><strong>民泊</strong>（届出済みの貸し部屋）</td><td>住宅宿泊事業法にもとづいて届け出た住宅[[s:jta_minpaku_overview]]</td><td>ホストが決める</td><td>ゲストを泊められるのは年180日までで、自治体の条例でさらに制限されることもあります[[s:jta_minpaku_act]]。</td></tr>
<tr><td><strong>宿・貸別荘</strong>（旅館業の許可あり）</td><td>旅館業法の許可を受けたもの。たとえば簡易宿所[[s:jta_minpaku_overview]]</td><td>ホストが決める</td><td>営業日数の上限がないので、一年中泊められます[[s:jta_minpaku_overview]]。</td></tr>
<tr><td><strong>シェアハウス</strong></td><td>たいていは賃貸で、条件は運営会社ごと</td><td>運営会社が決める</td><td>寝室は自分だけ、台所と浴室は共用です。条件の差が大きいので、書面でもらっておくと安心です。</td></tr>
</tbody></table></div>
<p>マンスリーの部屋が、なぜたいてい1か月以上なのか。観光庁と厚生労働省は、1か月に満たない滞在を、原則として宿泊として扱っています。予約サイト向けの考え方では、短期の賃貸は原則1か月以上の滞在を条件にし、宿泊ではなく賃貸だとはっきり書くこととされています。ただし、自治体が別の目安を使うこともあります[[s:jta_short_lease_2018]]。同じ通知には、マンスリーを短期の民泊と同じサイトに並べて載せないこととも書かれているので、探す場所が分かれていることがよくあります[[s:jta_short_lease_2018]]。</p>
<p>受けられるものも違います。宿泊では、部屋を清潔に保つのは運営者の仕事で、あなたはそこに住む人ではなく、泊まる客です。賃貸では、契約の期間、そこがあなたの住まいになります[[s:jta_short_lease_2018]]。どちらを選ぶにしても、掃除を誰がどれくらいの頻度でするかは、聞いておくといいと思います。</p>
<p>「定期借家」という言葉を目にすることもあるかもしれません。これは日本の賃貸契約の種類の1つで、マンスリーの部屋の別名ではありません。借りる側にとっての意味は、延長をあてにできないことです。契約に書いた日で終わり、更新はありません。ただし、貸す人と借りる人が合意すれば、新しく契約を結べます。書面で契約し、更新がないことを、貸す人が別の書面で説明しなければなりません[[s:mlit_fixed_term]]。</p>

<h2>1か月いくらかかり、何が含まれるか</h2>
<p>1か月の費用は、家賃に、清掃・光熱費・インターネット・保証金・予約サイトの手数料が加わったもので、比べるべきは合計です。値段は場所によって違いすぎて、1つの数字では役に立ちませんが、費用の内訳はどこでもだいたい同じです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>何に払うか</th><th>なぜ大事か</th><th>聞くこと</th></tr></thead>
<tbody>
<tr><td>家賃・1泊の料金</td><td>最初に目に入る数字で、いちばん比べやすい</td><td>週割・月割はあるか。この料金にもう入っているか</td></tr>
<tr><td>清掃</td><td>1回分の料金のことも、滞在中の定期的な清掃のことも、まったくないこともある</td><td>滞在中の清掃は含まれるか。どれくらいの頻度か</td></tr>
<tr><td>電気・ガス・水道</td><td>込みのことも、上限つきのことも、使った分だけ払うこともある</td><td>上限はあるか。超えたらどうなるか</td></tr>
<tr><td>インターネット</td><td>仕事をするなら、遅い回線で1か月は厳しい</td><td>固定回線か、モバイルルーターか</td></tr>
<tr><td>保証金</td><td>最後に返してほしいお金</td><td>あるか。いつ、どうやって戻るか</td></tr>
<tr><td>予約サイトの手数料</td><td>最初に見た料金が、最後の合計とは限らない</td><td>合計に予約サイトのサービス料は入っているか</td></tr>
<tr><td>途中で帰る場合</td><td>1か月のあいだには予定が変わることもある</td><td>早く帰ったら、使わなかった分は返金されるか</td></tr>
</tbody></table></div>
<p>月割があるのには理由があります。貸す側から見ると、長く泊まってもらえれば、ゲストの入れ替えの清掃が減ります。だから私たちも、最初の宿を開いたとき、週割と月割を付けました。掲載に割引が出ていなくても、聞いてみて損はありません。</p>

<h2>民泊が合法かどうか、どう見分けるか</h2>
<p>掲載に届出番号か許可番号が出ているかを見ます。2018年6月から、日本で住宅に有料で人を泊めるには、旅館業法の許可、特区民泊の認定、住宅宿泊事業法の届出のどれかが必要になりました[[s:jta_minpaku_overview]]。</p>
<p>住宅宿泊仲介業者として登録した予約サイトは、掲載ごとに届出番号などを表示しなければなりません[[s:jta_listing_rules]]。観光庁は、予約サイトで届出番号と物件の住所が確かめられるかを見るよう勧めています[[s:jta_minpaku_users]]。旅館業の許可の宿は、届出番号ではなく許可番号を出すので、表示の形はいつも同じとは限りません。私たちも貸す側としてこれを知っています。許可が下りるまで、Airbnb で予約を受けられませんでした。</p>
<p>1か月の滞在でこれが大事なのは、違法な掲載は消えることがあるからです。登録した予約サイトは、半年ごとに掲載している物件を観光庁に報告し、違法と分かった掲載は、求められたらすぐに削除しなければなりません[[s:jta_listing_page]]。法律が始まった2018年6月には、予約サイトは届出のない物件の先の予約を取り消すか、合法の物件に移すよう求められました[[s:jta_cancel_2018]]。観光庁は、民泊は登録した予約サイトか旅行会社を通して予約するよう呼びかけています[[s:jta_minpaku_illegal]]。</p>
<p>民泊の年180日の上限は、ホストの側の上限で、泊まる人の上限ではありません。物件ごとに、4月1日の正午から始まる1年で数えます[[s:jta_minpaku_act]]。つまり、そういう住宅は一年中は貸せない、というだけのことです。</p>
<p>ホストはなぜパスポートを求めるのか。法律でそう決まっているからです。住宅宿泊事業法では、日本に住所のない外国籍の宿泊者は、国籍と旅券番号を伝え、ホストは旅券の写しを保存します[[s:jta_minpaku_users]]。旅館業の許可の宿でも同じで、宿泊者名簿に国籍と旅券番号を書き、厚生労働省は、旅券を確かめて写しを名簿と一緒に保存するよう求めています[[s:mhlw_passport]]。私たちのチームが関わる3つの家でも、宿泊者名簿についての質問は、とくに多いものの1つでした。気になるのはあなただけではありません。</p>

<h2>1か月まるごと予約する前に、何を聞くか</h2>
<p>写真に写っていることより、毎日付き合うことを聞きます。私たちなら、次の順に聞きます。</p>
<ol>
<li><strong>インターネット</strong>　固定回線か。調子が悪いとき、ルーターはどこにあって、どう再起動するか。ビデオ会議があるなら、速さと同じくらい、ちゃんとした机が大事です。</li>
<li><strong>電気</strong>　一度にどれくらい使えるか。私たちの最初の部屋では、古い2芯の配線で、エアコンと冷蔵庫と電子レンジを同時に使えませんでした。ブレーカーの場所を知っておくのも役に立ちます。</li>
<li><strong>冷暖房</strong>　寝る部屋にエアコンがあるか。その電気代は含まれているか。</li>
<li><strong>洗濯</strong>　洗濯機と乾燥機はあるか。私たちのゲストもレビューで両方をほめてくれました。梅雨の1か月の洗濯を考えれば、理由は分かると思います。</li>
<li><strong>ごみ</strong>　長期の滞在ではどうするか。分け方と収集日は町ごとに違い、たとえば下田市の案内は日本語で書かれています[[s:shimoda_gomi]]。私たちのチームが関わる3つの家では、長期滞在のレビューの一部に、ごみ置き場のにおいの指摘がありました。</li>
<li><strong>清掃と寝具</strong>　滞在中に清掃やシーツの交換はあるか。それとも全部自分でするのか。</li>
<li><strong>階段と浴室</strong>　何階か、エレベーターはあるか、浴槽はあるかシャワーだけか。私たちのチームが関わる家の1つでは、急な階段のことを予約の前に説明しておいたのが好評でした。</li>
<li><strong>移動</strong>　駐車場はあるか。バス停やスーパーは歩いて行けるか。</li>
<li><strong>途中で帰る場合</strong>　予定が変わったら、使わなかった日の分はどうなるか。</li>
</ol>
<p>役に立つ答えがどんなものか、私たちの部屋「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」で答えてみます。約40㎡の部屋をまるごと貸していて、階段を約13段上がり、シャワーはありますが浴槽はありません[[s:node_room]]。ワークデスク、速い Wi-Fi、無料の洗濯機とガス乾燥機があります[[s:node_room]]。電気の容量が小さいので、電子レンジ・掃除機・ドライヤーを使うあいだは、エアコンを少しだけ止めてもらっています[[s:node_room]]。燃えるごみはごみ箱へ、すすいだ缶やびんは台所に置いてもらい、長く泊まる方には、ほかのことは連絡してもらうようにしています[[s:node_room]]。</p>

<h2>東京の外で1か月借りるのは、むずかしいか</h2>
<p>選べる数は少なくなりますが、早めに探せば十分できます。小さな町では、マンスリーの部屋は少なく、月割のある宿や貸別荘のほうが多いと私たちは思います。</p>
<p>住まいの値段は、東京を離れると下がります。2025年の民営家賃の平均は、3.3㎡あたり月に、東京都区部で9,803円、静岡市で4,621円でした[[s:estat_rent_2025]]。これは調べた住宅のふつうの賃貸の家賃で、マンスリーの値段ではありませんが[[s:stat_rent_note]]、差の大きさの目安になります。</p>
<p>移動の手段も大事になります。バスが少ないこともあるので、スーパーまで歩いて行ける部屋なら、車がなくても毎日がずっと楽です。海の町は夏に混みます。私たちが宿をしている下田でも、夏は海水浴やサーフィンの人が来るので、7月や8月の1か月は、かなり早めに予約したほうがいいです。</p>
<p>小さな町で、それでも行きやすいところなら、伊豆半島は1つの候補です。2026年11月時点で、東京駅から毎日走る直通の電車で、下田まで2時間29〜44分です[[s:jre_tt_tokyo]]。くわしい行き方は[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>自治体の「お試し住宅」を目にすることもあると思います。多くは移住するつもりの人向けで、たとえば静岡市のお試し住宅は、静岡県の外に住んでいて、市への移住を考えていて、先に市の移住の相談員と話した人が対象です[[s:shizuoka_trial]]。お試し住宅のことは、[[l:ja-akiya-try-first|買う前にその町で1か月暮らす記事]]で取り上げています。</p>

<h2>1か月いるのに、ビザは要るか</h2>
<p>多くの人は要りません。2026年11月時点で、多くの国・地域のパスポートを持つ人は、観光ならビザなしで日本に来られ、ほとんどは90日までです。ただし、国籍によっては15日・30日・180日のこともあります[[s:jnto_visa]]。</p>
<p>この滞在では、報酬を得る仕事はできません。大事なのは、自分のパスポートの条件です[[s:jnto_visa]]。もっと長く、日本からリモートで働きたいなら、[[l:ja-digital-nomad|日本のデジタルノマドビザ]]で、一部の国籍の人は最長6か月滞在できます[[s:isa_nomad_en]]。延長やもっと長い在留資格など、ほかの方法は[[l:ja-how-long-stay|日本に何日いられるかのガイド]]にまとめました。</p>
<p class="fine">これは一般的な情報で、法律や在留手続きの助言ではありません。決まりは変わることがあるので、自分の場合は公式のページで確かめてください。</p>
""",
  "faq": [
    ("観光ビザで、日本のアパートを借りられますか",
     "ふつうの賃貸は、たいてい現実的ではありません。多くは2年契約で、家賃の保証が要り、大家さんはまず在留資格を確かめます[[s:mlit_foreign_rental]]。1か月なら、マンスリーの部屋か、月割のある許可・届出済みの貸し部屋を選ぶのがふつうです。"),
    ("日本で Airbnb を1か月借りるのは合法ですか",
     "許可か届出のある部屋なら合法です。登録した予約サイトは、掲載に届出番号などを出さなければなりません[[s:jta_listing_rules]]。民泊がゲストを泊められるのは年180日までで、旅館業の許可の宿には年の上限がありません[[s:jta_minpaku_overview]]。"),
    ("日本のホストは、なぜパスポートの写しが要るのですか",
     "法律でそう決まっているからです。日本に住所のない外国籍の人なら、民泊でも旅館業の宿でも、ホストは国籍と旅券番号を記録し、パスポートの写しを保存します[[s:jta_minpaku_users,mhlw_passport]]。"),
    ("マンスリーの部屋に、光熱費や Wi-Fi は含まれていますか",
     "部屋によります。込みのところも、上限つきのところも、使った分だけ払うところもあるので、予約の前に聞いて、月の料金ではなく合計で比べるのがいちばんです。"),
    ("東京の外で、マンスリーの部屋は見つかりやすいですか",
     "選べる数は少ないので、早めに探してください。小さな町では、月割のある宿や貸別荘が選択肢の多くを占めると私たちは思います。海の町は夏に混みます。"),
  ],
 },
}
