# -*- coding: utf-8 -*-
"""what-is-an-akiya の新規記事（2026-11-21 執筆部）。構成案とリサーチメモ: tools/okaeri/briefs/what-is-an-akiya.md（リサーチメモ 2026-11-21 まで）。
空き家テーマの柱（親）記事。事実はリサーチ部が開いて確かめた公的な出典（総務省統計局・e-Gov・国交省・静岡市・上市町・財務省・衆議院）と、
既存記事で確かめた出典（moj_nationality）だけを使う。相続登記の義務化は e-Gov の不動産登記法の範囲（3年以内）だけで、開始日・経過措置の期限は書かない（編集長の判断）。
書かないもの: 検索数、取引価格の実例、英語で検索できるか、新築を好む傾向、「6か月以上」の定義、空家法の英語の正式名、空き家バンクの利用者側の条件（伊豆の町）。
自社の体験は docs/brand/experience.md 3-2（人が確認済み）の改修 約410万円・家具など 約240万円・準備 約7か月だけ。「借りた部屋で、買った空き家ではない」と断る。
content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "stat_housing2023_terms": ("https://www.stat.go.jp/english/data/jyutaku/pdf/05terms.pdf", "Statistics Bureau of Japan (terms)", "総務省統計局（用語の解説・英語）",
                               "Statistics Bureau of Japan: Explanation of Terms of the 2023 Housing and Land Survey"),
    "egov_akiya_act": ("https://laws.e-gov.go.jp/law/426AC1000000127", "Vacant Houses Act", "空家等対策の推進に関する特別措置法（e-Gov法令検索）",
                       "Act on Special Measures concerning the Promotion of Measures for Vacant Houses, Act No. 127 of 2014 (e-Gov, version in force from 3 September 2026)"),
    "mlit_akiya_guideline": ("https://www.mlit.go.jp/jutakukentiku/house/content/002020062.pdf", "MLIT (basic guideline)", "国土交通省（空家等の基本指針）",
                             "MLIT and MIC: Basic guideline on measures for vacant houses (revised 3 September 2026)"),
    "mlit_akiya_act2023": ("https://www.mlit.go.jp/jutakukentiku/house/content/001621960.pdf", "MLIT, 2023", "国土交通省（改正空家法の概要）",
                           "MLIT: Outline of the 2023 amendment to the Vacant Houses Act (in force 13 December 2023)"),
    "mlit_owner_survey2024": ("https://www.mlit.go.jp/jutakukentiku/house/content/001907473.pdf", "MLIT, 2025", "国土交通省（令和6年空き家所有者実態調査・結果のポイント）",
                              "MLIT: 2024 Survey of Vacant House Owners, key results (August 2025)"),
    "mlit_owner_survey2024_report": ("https://www.mlit.go.jp/jutakukentiku/house/content/001907478.pdf", "MLIT, 2025 (report)", "国土交通省（令和6年空き家所有者実態調査・報告書）",
                                     "MLIT: 2024 Survey of Vacant House Owners, full report (August 2025)"),
    "egov_registration_act": ("https://laws.e-gov.go.jp/law/416AC0000000123", "Real Property Registration Act", "不動産登記法（e-Gov法令検索）",
                              "Real Property Registration Act, Act No. 123 of 2004, Article 76-2 (e-Gov)"),
    "mlit_seismic": ("https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_fr_000043.html", "MLIT (seismic retrofit)", "国土交通省（住宅・建築物の耐震化）",
                     "MLIT: Making homes and buildings earthquake-resistant"),
    "mlit_seismic_1981": ("https://www.mlit.go.jp/common/001184897.pdf", "MLIT (1981 standard)", "国土交通省（新耐震基準の木造住宅の耐震性能検証法）",
                          "MLIT: Verification method for wooden houses built to the post-June 1981 seismic standard"),
    "mlit_akiya_bank": ("https://www.mlit.go.jp/totikensangyo/const/sosei_const_tk3_000131.html", "MLIT (akiya bank)", "国土交通省（空き家・空き地バンク総合情報ページ）",
                        "MLIT: National akiya bank information page (figures as of end of October 2026)"),
    "mlit_akiya_bank_outline": ("https://www.mlit.go.jp/totikensangyo/const/content/002045626.pdf", "MLIT (akiya bank outline)", "国土交通省（全国版空き家・空き地バンクについて）",
                                "MLIT: About the national akiya bank (as of 31 October 2026)"),
    "shizuoka_akiya_bank": ("https://www.city.shizuoka.lg.jp/s7345/s000893.html", "Shizuoka City (akiya bank)", "静岡市（空き家情報バンク）",
                            "Shizuoka City: Shizuoka City akiya bank (checked November 2026)"),
    "kamiichi_zero_yen": ("https://www.town.kamiichi.toyama.jp/page/1934.html", "Kamiichi Town", "上市町（0円空家バンク）",
                          "Kamiichi Town, Toyama: Zero-yen akiya bank (updated 18 November 2026)"),
    "kamiichi_zero_yen_flow": ("https://www.town.kamiichi.toyama.jp/uploaded/attachment/3448.pdf", "Kamiichi Town (process)", "上市町（0円空家バンクの流れ）",
                               "Kamiichi Town, Toyama: How the zero-yen akiya bank works"),
    "mlit_brokerage_fee2024": ("https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/const/content/001749923.pdf", "MLIT, 2024", "国土交通省（空き家等に係る媒介報酬規制の見直し）",
                               "MLIT: Revised brokerage fee rules for low-priced and long-vacant properties (in force 1 July 2024)"),
}

# 見出し写真（エンジニア部へ）: Unsplash の候補。この環境から画像を開けず、執筆部は中身を目で確かめていない。
# PHOTO_PLAN.md の記載（軽トラ・トタンの小屋・古い家と緑の山）から仮の alt を書いた。組み込む前に画像を見て、
# ①古い木造の家が写っているか ②車のナンバー・表札・看板・人の顔が読み取れないか を確かめ、合わなければ別の写真にして alt・説明文を直す。
# download_asset でダウンロードを記録し、content.py の PHOTO_CREDITS に次の1行を足す。
PHOTO_CREDIT_NEW = {
    "rural-old-house": ("Loris Boulinguez", "https://unsplash.com/@lorisboulinguez", "https://unsplash.com/photos/Kjbhq8BJZTE", "Kjbhq8BJZTE"),  # 撮影者ページの URL は要確認
}

ARTICLE = {
 "id": "what-is-akiya", "slug": "what-is-an-akiya", "topic": "own", "place": None, "also": [],
 "photo": ("rural-old-house", "An old house and a tin-roofed shed below green hills", "An older house in the countryside."),
 "published": "2026-11-21", "updated": "2026-11-21",
 "kicker": "Own a home",
 "h1": "What is an akiya? Japan’s empty houses, and what buying one really means",
 "seo_title": "What Is an Akiya? Japan’s Empty Houses and Who Can Buy One",
 "description": "An akiya is simply an empty house. Japan had about 9 million in 2023, but most aren’t abandoned, and with a cheap one the price is only part of the cost.",
 "dek": "An akiya is just a house nobody lives in. Japan counted about 9 million in 2023, and fewer than half are the abandoned kind the headlines mean.",
 "card": "An akiya is simply a house nobody lives in. Japan counted about 9 million in 2023, but just over half were waiting for a tenant or buyer. Cheap ones are real, often on town-run akiya banks, yet repairs, fees and taxes come on top of the price.",
 "keywords": [("akiya", "3,600", "0"), ("akiya japan", "1,300", "—"), ("akiya houses", "1,300", "—"), ("abandoned houses in japan", "1,000", "3")],
 "intent": "Know（知りたい）",
 "points": [
   "Japan had about 9 million empty homes in 2023, a record 13.8% of all housing.",
   "Just over half were waiting for a tenant or buyer; about 3.9 million were simply left unused.",
   "You can buy one from abroad, and town-run akiya banks list many, but repairs and fees come on top.",
 ],
 "body": """
<p>If you’ve seen headlines about Japan giving houses away, the real picture is less dramatic and a lot more useful. An akiya (空き家, literally “empty house”) is simply a house that nobody lives in. Most of them aren’t ruins, and we think a low asking price tells you less than you’d hope about what you’d end up paying.</p>

<h2>What does “akiya” actually mean?</h2>
<p>In everyday Japanese, it just means a house where nobody lives. The catch is that Japan counts akiya in two different ways, and the news nearly always uses the wider one.</p>
<p>The wider one comes from a national housing survey held every five years (the Housing and Land Survey). It counts homes where no household usually lives on the survey day [[s:stat_housing2023_terms]]. So flats between tenants, houses on the market and holiday homes all count. So do homes left empty after someone moved into hospital, and homes that are about to be pulled down [[s:stat_housing2023_terms]].</p>
<p>The narrower one comes from a law on empty houses, often called the Vacant Houses Act. It covers buildings that normally aren’t lived in or used, along with their land [[s:egov_akiya_act]]. The government’s guideline treats about a year with no sign of use as one yardstick [[s:mlit_akiya_guideline]]. That law is what lets a town step in when an empty house starts to fall apart. So when you see a huge akiya number in the news, it’s the survey’s count, and plenty of those homes are simply waiting for the next tenant.</p>

<h2>How many akiya are there, and how many are really abandoned?</h2>
<p>About 9 million, a record. The ones people mean by “abandoned” are about 3.9 million of those [[s:stat_housing2023]]. The rest all have a purpose: just over half are for rent or for sale, and a small share are second homes.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Type of empty home</th><th>Number in 2023</th><th>Change since 2018</th></tr></thead>
<tbody>
<tr><td>For rent</td><td>4.44 million</td><td>+109,000</td></tr>
<tr><td>For sale</td><td>326,000</td><td>+33,000</td></tr>
<tr><td>Second homes</td><td>384,000</td><td>+3,000</td></tr>
<tr><td>Left unused (none of the above)</td><td>3.86 million</td><td>+369,000</td></tr>
<tr><td><strong>All empty homes</strong></td><td><strong>9.00 million</strong> (13.8% of all homes)</td><td>+513,000</td></tr>
</tbody></table></div>
<p class="fine">Counted on 1 October 2023 [[s:stat_housing2023]].</p>
<p>The left-unused group is the one that keeps growing, and it’s mostly detached houses. About four in five empty detached houses fall into it [[s:stat_housing2023]]. So only a thin slice of Japan’s empty homes were actually for sale when the survey was taken.</p>

<h2>Why are so many houses left empty?</h2>
<p>Mostly because they were inherited, and leaving a house as it is can feel easier than deciding what to do with it. About 58% of the empty homes in a 2024 government survey of owners had been inherited [[s:mlit_owner_survey2024]]. Many of them became empty when the person living there died [[s:mlit_owner_survey2024]].</p>
<p>It isn’t usually that the owners live far away, either. About eight in ten empty homes are within an hour of the owner’s own home [[s:mlit_owner_survey2024_report]]. When owners who plan to keep a house empty were asked why, the most common answers were these [[s:mlit_owner_survey2024_report]]:</p>
<ul>
<li>they use it to store things</li>
<li>they don’t want to pay for demolition</li>
<li>the house is too old</li>
<li>there’d be no use for the land even if the house came down</li>
</ul>
<p>Some also worry that pulling the house down would raise their property tax [[s:mlit_owner_survey2024_report]]. The law is nudging things along, though. Under the current law, heirs must register an inherited property within three years of learning about it [[s:egov_registration_act]]. We think that should make it easier to find out who owns an empty house. The upshot for you is that plenty of akiya owners aren’t trying to sell. They’re waiting, and a house that isn’t listed anywhere may still have an owner who’d talk.</p>

<h2>Are akiya only in the countryside?</h2>
<p>No. Tokyo has more empty homes than any other prefecture, but only about 214,000 of them are the left-unused kind (2.6% of homes) [[s:stat_housing2023]]. The share of homes standing empty is highest in rural prefectures.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Prefecture</th><th>Share of homes empty (2023)</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td>Tokushima</td><td>21.3%</td><td>Highest in Japan</td></tr>
<tr><td>Wakayama</td><td>21.2%</td><td></td></tr>
<tr><td>Kagoshima</td><td>20.5%</td><td></td></tr>
<tr><td>Shizuoka</td><td>16.7%</td><td>Home to the Izu Peninsula; 296,000 empty homes</td></tr>
<tr><td>Tokyo</td><td>10.9%</td><td>897,000 empty homes, the most of any prefecture</td></tr>
<tr><td>Kanagawa</td><td>9.8%</td><td></td></tr>
<tr><td>Okinawa</td><td>9.4%</td><td></td></tr>
<tr><td>Saitama</td><td>9.3%</td><td>Lowest in Japan</td></tr>
</tbody></table></div>
<p class="fine">Statistics Bureau of Japan, 2023 Housing and Land Survey [[s:stat_housing2023]].</p>
<p>The difference shows up in the left-unused group. In Wakayama and Tokushima, those homes make up over 12% of all housing [[s:stat_housing2023]]. So the forgotten houses that end up cheap are mostly in the countryside, even if the biggest raw numbers are in the cities.</p>

<h2>Is an akiya really cheap?</h2>
<p>The asking price can be very low, but in our view the total rarely is. Repairs, safety checks, fees and taxes all come on top, and they vary so much from one house to the next that only written quotes tell you the real figure.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What comes on top</th><th>Why it matters</th><th>When</th></tr></thead>
<tbody>
<tr><td><strong>Repairs and renovation</strong></td><td>Old wiring, plumbing, roofs and damp differ from house to house. Written quotes are the only way to know.</td><td>Before you move in</td></tr>
<tr><td><strong>An earthquake check</strong></td><td>Houses built to the standard used before June 1981 often aren’t strong enough, and the government urges owners to get them assessed. National and local governments help pay for assessments and strengthening work [[s:mlit_seismic,mlit_seismic_1981]].</td><td>Before you buy</td></tr>
<tr><td><strong>The agent’s fee</strong></td><td>On a home priced at ¥8 million or less, an agent can charge up to ¥300,000 plus tax, which they have to explain and agree with you in advance [[s:mlit_brokerage_fee2024]]. On a very cheap house, that can be a big share of the price.</td><td>When you buy</td></tr>
<tr><td><strong>Registration and taxes on the purchase</strong></td><td>Even a free house has them. One town’s zero-yen scheme leaves the registration costs and the taxes on acquiring the property to the new owner [[s:kamiichi_zero_yen_flow]].</td><td>Around the purchase</td></tr>
<tr><td><strong>Property tax and upkeep</strong></td><td>You pay these every year. If the town formally warns that a house is badly kept, the land can lose its property tax reduction [[s:mlit_akiya_act2023]].</td><td>Every year</td></tr>
</tbody></table></div>
<p>We think that last row also gives some owners a reason to sell. Since an amendment in December 2023, a house left to decay can cost its owner more in tax once the town steps in [[s:mlit_akiya_act2023]].</p>
<p>We haven’t bought an akiya ourselves, so we can only give you a sense of scale. One of our founding members rented an older flat in Shimoda from its owner and turned it into a guesthouse. The building work alone came to about ¥4.1 million, and that was a rented flat, not a house we bought.</p>
<p>Furniture, appliances and supplies added roughly ¥2.4 million, and getting it all ready took about seven months. A whole house would usually be a bigger job, so we’d get quotes before treating any asking price as the real cost. If you’re seriously thinking about it, we’d suggest [[l:akiya-try-first|living in the town for a month before you buy]].</p>

<h2>Where do you find an akiya for sale?</h2>
<p>Mostly through akiya banks, lists of empty homes that towns and cities put together, though ordinary estate agents sell them too. The government has a national akiya bank, run by two property companies, LIFULL and At Home, where you can search many towns’ listings in one place [[s:mlit_akiya_bank]].</p>
<p>It doesn’t cover everywhere, though. As of October 2026, more than 1,100 towns and cities take part [[s:mlit_akiya_bank_outline]], so if a town you like isn’t on it, its own website is worth a look. Each bank also sets its own rules. Shizuoka City’s, for example, only covers homes in the city’s designated urban area, and only estate agents can list properties on it [[s:shizuoka_akiya_bank]].</p>
<p>A few towns go further. Kamiichi, a town in Toyama, runs a zero-yen akiya bank where owners give away the house and land for free [[s:kamiichi_zero_yen]]. The town only passes on the information, though. You deal with the owner directly and pay for the registration, repairs, moving and taxes yourself [[s:kamiichi_zero_yen_flow]].</p>
<p>If you want to start looking, this is the order we’d go in:</p>
<ol>
<li>Search the national akiya bank and narrow it down by region.</li>
<li>Look up the akiya bank page of any town you like, since it may list homes the national site doesn’t.</li>
<li>Read who can use that bank, because the rules change from town to town.</li>
<li>Contact the town office about the houses that interest you.</li>
<li>Go and see the house, and the town, in person.</li>
</ol>
<p>For that last step, [[l:monthly-rental|renting a place by the month]] gives you time to see more than one house without rushing.</p>

<h2>Can you buy one if you live outside Japan?</h2>
<p>Yes. Living abroad doesn’t stop you buying, though there’s a little more paperwork than there used to be. Since April 2026, non-residents who buy property in Japan, even a home to live in, have had to report it to the Ministry of Finance afterwards [[s:mof_fefta2026,mof_realprop_faq]]. And since October 2026, every buyer, Japanese or not, gives their nationality when the purchase is registered [[s:moj_nationality]].</p>
<p>The rules are still moving. A land bill before the Diet would add new limits in some areas, but it hadn’t passed as of November 2026 [[s:shugiin_bill18]]. We’d also treat a house and a visa as separate questions, so our guide to [[l:how-long-stay|how long you can stay in Japan]] is worth reading alongside this. Our guide to [[l:akiya-try-first|living in the town before you buy]] goes into the buying rules in more detail.</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal, tax or property advice.</p>',
 "faq": [
   ("Is an akiya the same as an abandoned house?",
    "No. In Japan’s housing survey, “akiya” also covers homes for rent or sale and second homes. The ones closest to abandoned are the homes left unused, about 3.9 million of the 9 million counted [[s:stat_housing2023]]."),
   ("Why don’t owners just sell or knock them down?",
    "Many inherited the house and haven’t decided what to do with it. Owners who plan to keep one empty most often say they use it for storage, don’t want to pay for demolition, think it’s too old, or see no use for the land if it were cleared. Some also worry that pulling it down would raise their property tax [[s:mlit_owner_survey2024_report]]."),
   ("Are there free akiya in Japan?",
    "Yes, a few. Kamiichi in Toyama, for example, runs a zero-yen akiya bank where owners give houses away [[s:kamiichi_zero_yen]]. You still pay for registration, repairs, moving and taxes yourself [[s:kamiichi_zero_yen_flow]]."),
   ("Is an old akiya safe in an earthquake?",
    "It depends on the house. Homes built to the standard used before June 1981 often aren’t strong enough, so it’s sensible to get one assessed before you buy. National and local governments help pay for assessments and strengthening work [[s:mlit_seismic,mlit_seismic_1981]]."),
 ],
 "sources": ["stat_housing2023", "stat_housing2023_terms", "egov_akiya_act", "mlit_akiya_guideline", "mlit_owner_survey2024", "mlit_owner_survey2024_report",
             "egov_registration_act", "mlit_seismic", "mlit_seismic_1981", "mlit_brokerage_fee2024", "kamiichi_zero_yen", "kamiichi_zero_yen_flow", "mlit_akiya_act2023",
             "mlit_akiya_bank", "mlit_akiya_bank_outline", "shizuoka_akiya_bank", "mof_fefta2026", "mof_realprop_faq", "moj_nationality", "shugiin_bill18"],
 "related": ["akiya-try-first", "how-long-stay", "monthly-rental"],
 "ja": {
  "h1": "akiya（空き家）って何？ 日本の空き家と、買うことの本当の意味",
  "dek": "akiya は、ひとことで言えば誰も住んでいない家のこと。2023年に日本では約900万戸と数えられましたが、ニュースが言う「放置された家」は、その半分に届きません。",
  "points": [
    "2023年、日本の空き家は約900万戸で、住宅全体の13.8%。どちらも過去最多・最高です。",
    "半分強は借り手や買い手を待っている家で、ただ使われずに置かれているのは約390万戸です。",
    "海外に住んでいても買え、自治体の空き家バンクに多く載っています。ただし修繕や手数料が上乗せされます。",
  ],
  "body": """
<p>「日本では家がタダ同然でもらえる」という見出しを見たことがあるなら、実際の姿はもっと地味で、そのぶん役に立つ話です。akiya（空き家）は、ひとことで言えば、誰も住んでいない家のこと。ほとんどは廃墟ではありませんし、売り出し価格が安くても、最終的にいくら払うことになるかは、思うほど分からないと私たちは考えています。</p>

<h2>akiya って、そもそもどういう意味？</h2>
<p>ふだんの日本語では、ただ「人が住んでいない家」のことです。ややこしいのは、日本では空き家の数え方が2通りあって、ニュースはたいてい広いほうを使っていることです。</p>
<p>広いほうは、5年に1度の国の住宅の調査（住宅・土地統計調査）の数え方です。調査の日に、ふだん住んでいる世帯がいない住宅を数えます[[s:stat_housing2023_terms]]。つまり、次の借り手を待っている部屋も、売りに出ている家も、別荘も入ります。住んでいた人が入院して空いた家や、取り壊す予定の家も入ります[[s:stat_housing2023_terms]]。</p>
<p>狭いほうは、空き家の対策の法律（空家等対策の推進に関する特別措置法、いわゆる空家法）の考え方です。ふだん住んだり使ったりしていない建物と、その土地が対象です[[s:egov_akiya_act]]。国の指針では、1年ほど使われた様子がないことが、目安の1つになっています[[s:mlit_akiya_guideline]]。空き家が傷みはじめたとき、町が手を打てるのは、この法律があるからです。ですから、ニュースで大きな空き家の数を見たら、それは調査の数で、その中には、次の借り手を待っているだけの家もたくさん入っています。</p>

<h2>空き家はいくつあって、本当に放置されているのはどれくらい？</h2>
<p>約900万戸で、過去最多です。「放置された家」と言うときに指しているのは、そのうち約390万戸です[[s:stat_housing2023]]。残りには、どれも使い道があります。半分強は貸すためか売るための家で、少しは別荘です。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>空き家の種類</th><th>2023年の戸数</th><th>2018年からの増減</th></tr></thead>
<tbody>
<tr><td>賃貸用</td><td>443.6万戸</td><td>+10.9万戸</td></tr>
<tr><td>売却用</td><td>32.6万戸</td><td>+3.3万戸</td></tr>
<tr><td>別荘など（二次的住宅）</td><td>38.4万戸</td><td>+0.3万戸</td></tr>
<tr><td>使われずに置かれている（上のどれでもない）</td><td>385.6万戸</td><td>+36.9万戸</td></tr>
<tr><td><strong>空き家の合計</strong></td><td><strong>900.2万戸</strong>（住宅全体の13.8%）</td><td>+51.3万戸</td></tr>
</tbody></table></div>
<p class="fine">2023年10月1日時点[[s:stat_housing2023]]。</p>
<p>増え続けているのは、使われずに置かれている家で、その多くは一戸建てです。空いている一戸建ての、およそ5軒に4軒がここに入ります[[s:stat_housing2023]]。つまり、調査の時点で本当に売りに出ていた空き家は、ほんの一部です。</p>

<h2>なぜ、こんなに多くの家が空いたままなのか</h2>
<p>おもな理由は相続です。家をそのままにしておくほうが、どうするか決めるより楽に感じられるのです。2024年の国の持ち主の調査では、空き家の約58%が相続で手に入れたものでした[[s:mlit_owner_survey2024]]。その多くは、住んでいた人が亡くなったときに空き家になっています[[s:mlit_owner_survey2024]]。</p>
<p>持ち主が遠くに住んでいるから、というわけでもありません。空き家の約8割は、持ち主の家から1時間以内のところにあります[[s:mlit_owner_survey2024_report]]。空き家のままにしておくつもりの持ち主に理由を聞くと、多かった答えは次のとおりです[[s:mlit_owner_survey2024_report]]。</p>
<ul>
<li>物置として使っている</li>
<li>解体の費用を払いたくない</li>
<li>家が古すぎる</li>
<li>家を壊してさら地にしても、土地の使い道がない</li>
</ul>
<p>取り壊すと固定資産税が上がることを気にする人もいます[[s:mlit_owner_survey2024_report]]。それでも、法律は少しずつ背中を押しています。いまの法律では、相続人は、相続した不動産を、相続を知ってから3年以内に登記しなければなりません[[s:egov_registration_act]]。空き家の持ち主を調べやすくなるはずだと私たちは考えています。つまり、空き家の持ち主の多くは、売ろうとしているわけではありません。様子を見ているだけで、どこにも載っていない家でも、話を聞いてくれる持ち主がいるかもしれません。</p>

<h2>空き家があるのは田舎だけ？</h2>
<p>いいえ。空き家の数がいちばん多いのは東京都ですが、使われずに置かれている家は約21.4万戸（住宅全体の2.6%）だけです[[s:stat_housing2023]]。空き家の割合が高いのは、地方の県です。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>都道府県</th><th>空き家の割合（2023年）</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td>徳島県</td><td>21.3%</td><td>全国で最も高い</td></tr>
<tr><td>和歌山県</td><td>21.2%</td><td></td></tr>
<tr><td>鹿児島県</td><td>20.5%</td><td></td></tr>
<tr><td>静岡県</td><td>16.7%</td><td>伊豆半島がある県。空き家は29.6万戸</td></tr>
<tr><td>東京都</td><td>10.9%</td><td>空き家は89.7万戸で、都道府県で最も多い</td></tr>
<tr><td>神奈川県</td><td>9.8%</td><td></td></tr>
<tr><td>沖縄県</td><td>9.4%</td><td></td></tr>
<tr><td>埼玉県</td><td>9.3%</td><td>全国で最も低い</td></tr>
</tbody></table></div>
<p class="fine">総務省統計局「令和5年住宅・土地統計調査」[[s:stat_housing2023]]。</p>
<p>違いがはっきり出るのは、使われずに置かれている家です。和歌山県と徳島県では、住宅全体の12%を超えています[[s:stat_housing2023]]。つまり、数がいちばん多いのは都会でも、忘れられて安くなる家は、おもに地方にあります。</p>

<h2>空き家は本当に安い？</h2>
<p>売り出し価格はとても安いことがありますが、私たちの見方では、総額が安く済むことはあまりありません。修繕、安全の確認、手数料、税金が上乗せされ、家ごとに大きく違うので、本当の金額は書面の見積もりを取って初めて分かります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>上乗せされるもの</th><th>なぜ大事か</th><th>いつ</th></tr></thead>
<tbody>
<tr><td><strong>修繕・改修</strong></td><td>古い配線、水回り、屋根、湿気の傷みは家ごとに違います。書面の見積もりでしか分かりません。</td><td>住みはじめる前</td></tr>
<tr><td><strong>耐震の確認</strong></td><td>1981年6月より前の基準で建てられた家は、強さが足りないことが多く、国は持ち主に耐震診断を勧めています。診断や補強の工事には、国と自治体の補助があります[[s:mlit_seismic,mlit_seismic_1981]]。</td><td>買う前</td></tr>
<tr><td><strong>仲介手数料</strong></td><td>800万円以下の家では、不動産会社は最大30万円＋税を受け取れます。事前に説明し、合意することになっています[[s:mlit_brokerage_fee2024]]。とても安い家だと、価格に対して大きな割合になります。</td><td>買うとき</td></tr>
<tr><td><strong>登記と、買ったときの税金</strong></td><td>タダの家でもかかります。ある町の0円の空き家バンクでは、登記の費用と、不動産を手に入れたときの税金は、新しい持ち主が払います[[s:kamiichi_zero_yen_flow]]。</td><td>買うころ</td></tr>
<tr><td><strong>固定資産税と維持費</strong></td><td>毎年払います。手入れが悪いと町から正式に勧告されると、土地の固定資産税の軽減がなくなることがあります[[s:mlit_akiya_act2023]]。</td><td>毎年</td></tr>
</tbody></table></div>
<p>この最後の行も、持ち主が売ろうと考える理由の1つになっていると私たちは思います。2023年12月の法律の改正から、傷むまま放っておいた家は、町が動くと、持ち主の税金が増えることがあるのです[[s:mlit_akiya_act2023]]。</p>
<p>私たち自身は空き家を買ったことがないので、規模の感じをお伝えすることしかできません。創業メンバーの1人が、下田の古い部屋を持ち主から借りて、宿に改修しました。工事だけで約410万円かかりました。しかもこれは借りた部屋で、買った家ではありません。</p>
<p>家具・家電・備品でさらに約240万円かかり、準備には全部で約7か月かかりました。一軒家まるごとなら、たいていもっと大きな工事になるので、どんな売り出し価格も、見積もりを取るまでは本当の費用だと考えないようにしています。本気で考えているなら、[[l:ja-akiya-try-first|買う前に、その町で1か月暮らしてみる]]ことをおすすめします。</p>

<h2>売りに出ている空き家は、どこで探す？</h2>
<p>おもに空き家バンクです。市町村がまとめている空き家の一覧で、ふつうの不動産会社が売っている空き家もあります。国が用意した全国版の空き家バンクは、不動産会社2社（LIFULL とアットホーム）が運営していて、たくさんの町の物件を1か所で探せます[[s:mlit_akiya_bank]]。</p>
<p>ただし、すべての町が載っているわけではありません。2026年10月時点で、参加している市町村は1,100を超えます[[s:mlit_akiya_bank_outline]]。気になる町が載っていなければ、町のサイトも見てみる価値があります。決まりも空き家バンクごとに違います。たとえば静岡市の空き家バンクは、市街化区域の中の家だけが対象で、物件を載せられるのは不動産会社だけです[[s:shizuoka_akiya_bank]]。</p>
<p>もっと踏み込んだ町もあります。富山県の上市町は「0円空家バンク」を運営していて、持ち主が土地と家をタダで譲ります[[s:kamiichi_zero_yen]]。ただし、町は情報を紹介するだけです。持ち主と直接やりとりし、登記、修繕、引っ越し、税金は自分で払います[[s:kamiichi_zero_yen_flow]]。</p>
<p>探しはじめるなら、私たちならこの順番で進めます。</p>
<ol>
<li>全国版の空き家バンクで、地域を絞って探す。</li>
<li>気になる町の空き家バンクのページも見る。全国版にない家が載っていることがあります。</li>
<li>その空き家バンクを誰が使えるかを読む。決まりは町ごとに違います。</li>
<li>気になる家について、町の窓口に問い合わせる。</li>
<li>家と町を、自分の目で見に行く。</li>
</ol>
<p>最後の段階では、[[l:ja-monthly-rental|月単位で部屋を借りる]]と、あわてずに何軒も見られます。</p>

<h2>海外に住んでいても買える？</h2>
<p>買えます。海外に住んでいても買えますが、手続きは前より少し増えました。2026年4月から、日本に住んでいない人が日本の不動産を買うと、住むための家でも、買ったあとに財務省に報告することになっています[[s:mof_fefta2026,mof_realprop_faq]]。また2026年10月からは、日本人も含めて、買った人はみな登記のときに国籍を届け出ます[[s:moj_nationality]]。</p>
<p>決まりは、まだ動いています。国会に出ている土地の法案は、一部の区域に新しい制限を加える内容ですが、2026年11月時点では成立していません[[s:shugiin_bill18]]。家とビザは別々の問題として考えたほうがいいと私たちは思うので、[[l:ja-how-long-stay|日本に何日いられるかのガイド]]もあわせて読んでみてください。買うときの決まりは、[[l:ja-akiya-try-first|買う前にその町で暮らしてみる記事]]でくわしく書いています。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律・税金・不動産の助言ではありません。</p>',
  "faq": [
    ("akiya は、放置された家と同じですか",
     "違います。日本の住宅の調査でいう「空き家」には、貸すための家、売るための家、別荘も入ります。放置に近いのは、使われずに置かれている家で、数えられた約900万戸のうち約390万戸です[[s:stat_housing2023]]。"),
    ("持ち主は、なぜ売ったり取り壊したりしないのですか",
     "多くは相続した家で、どうするかまだ決めていません。空き家のままにするつもりの持ち主に多い理由は、物置に使っている、解体の費用を払いたくない、古すぎる、さら地にしても土地の使い道がない、です。取り壊すと固定資産税が上がることを気にする人もいます[[s:mlit_owner_survey2024_report]]。"),
    ("日本に、タダの空き家はありますか",
     "少しはあります。たとえば富山県の上市町は、持ち主が家を譲る「0円空家バンク」を運営しています[[s:kamiichi_zero_yen]]。それでも登記、修繕、引っ越し、税金は自分で払います[[s:kamiichi_zero_yen_flow]]。"),
    ("古い空き家は、地震のとき安全ですか",
     "家によります。1981年6月より前の基準で建てられた家は強さが足りないことが多いので、買う前に耐震診断を受けると安心です。診断や補強の工事には、国と自治体の補助があります[[s:mlit_seismic,mlit_seismic_1981]]。"),
  ],
  "review": [
   "【2026-11-21 品質保証部の1回目（83点・ゲート違反1）を受けた直し】①【ゲート】東京都の「多くは借り手の入れ替わりを待つ部屋」は出典に内訳がないので、「使われずに置かれている家は約21.4万戸（住宅全体の2.6%）だけ」に替えました（あとの段落の東京2.6%は重なるので外しました） ②「この最後の行は持ち主が手放したがる理由」を「私たちはそう思う」という見方に ③相続登記を「いまの法律では、相続を知ってから3年以内に登記しなければならない」に（開始日は書いていません） ④空き家バンクの参加数に「2026年10月時点」を足しました ⑤耐震の行と FAQ に出典 mlit_seismic_1981 を足しました ⑥空けておく理由を調査の上位4つ（物置・解体費・古すぎる・さら地にしても使い道がない）にし、固定資産税は別の文「気にする人もいる」にしました（FAQ も同じ） ⑦統計の説明を「人が住んでいない住宅を数える」に。英語の仕上げとして、数え方・空き家バンクの説明・「読み手にとっての意味」の言い方を自然にし、最後の節の akiya-try-first にリンクを付け、改修費の2段落を1段落にまとめました",
   "【2026-11-21 新規執筆】空き家テーマの柱になる記事です。構成案（briefs/what-is-an-akiya.md）の7つの見出しどおりに書き、細かい話は「買う前に1か月暮らす」記事・日本に何日いられるかの記事・マンスリーの記事にリンクでつないでいます",
   "書いた中身: ①akiya の意味を、統計の数え方（調査の日に人が住んでいない住宅すべて）と法律の考え方（ふだん使われていない建物、1年ほどが目安）の2つに分けました ②約900万戸のうち「放置」に近いのは約390万戸で、半分強は貸す用・売る用（52.9%）だと、表で4区分と2018年からの増減を見せました ③空き家が多い理由は国交省の2024年の持ち主の調査（約58%が相続、約8割は持ち主の家から1時間以内、空けておく理由の上位）。構成案の「離れて暮らす子が相続」は調査と逆なので書いていません ④都道府県の割合の表（高い3県・低い3県・東京・静岡） ⑤安いのかの節で、上乗せされるもの（修繕・耐震・仲介手数料の特例・登記と税・固定資産税と2023年の法改正）を表に ⑥空き家バンクの探し方（全国版・参加は1,100市町村超・静岡市の例・上市町の0円空家バンク）と、探す順番の番号つきリスト ⑦海外に住む人も買えること（財務省への報告・登記の国籍・未成立の法案）は短くし、くわしくは既存記事へ",
   "自社の体験: 下田の部屋の改修 約410万円・家具など 約240万円・準備 約7か月（experience.md 3-2、人が確認済み）を、「買った空き家ではなく、借りた部屋」と断って1回だけ使いました。合計額は書いていません。NODE Shimoda の名前・宣伝は入れていません",
   "書かなかったこと（確かめられない、または編集長の指示）: 相続登記の義務化の開始日（2024年4月1日）と、それより前の相続の期限（法務省のページが開けず検索でしか確かめていないため。不動産登記法の「知ってから3年以内」だけにしました）、空き家バンクを英語で探せるか（全国版のサイトが開けない）、取引価格の実例、新築を好む傾向、「6か月以上空いている家」という定義、空家法の英語の正式名（“often called the Vacant Houses Act” と説明で書いています）",
   "【人に確かめてほしい点】①見出し写真は Unsplash の候補（Kjbhq8BJZTE、Loris Boulinguez）ですが、この環境から画像を開けず、執筆部は中身を見ていません。エンジニア部が画像を見て、古い家が写っているか・車のナンバーなどが読めないかを確かめ、合わなければ差し替えて説明文を直します（ファイル内の PHOTO_CREDIT_NEW にクレジットのメモ） ②下田の改修費を「規模の感じ」として出す書き方（借りた部屋だと断っています）でよいか ③「登記の国籍の届け出（2026年10月から）」は、法務省のページが今回も開けず、既存記事で確かめた内容をそのまま使っています",
   "【編集長・エンジニア部への依頼（構成案のとおり）】公開と同時に、akiya-try-first の keywords から \"akiya\" を外す（共食いの整理）。TOPICS[\"own\"][\"coming\"] から \"What is an akiya?\" を外す",
  ],
 },
}
