# -*- coding: utf-8 -*-
"""akiya-try-first の書き直し（2026-11-15 品質保証部の指摘とリサーチメモにもとづく）。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
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
    "cas_land_teigen": ("https://www.cas.go.jp/jp/seisaku/symbiotic_society/gaikokujin_tochishutoku/kaisai-jokyo/dai5/teigen.pdf",
                        "Cabinet Secretariat", "内閣官房", "Cabinet Secretariat: Expert panel recommendations on land acquisition rules (October 2026)"),
    "minamialps_trial": ("https://www.city.minami-alps.yamanashi.jp/docs/12876.html", "Minami-Alps City", "南アルプス市",
                         "Minami-Alps City: Trial homes for people considering a move"),
    "shizuoka_long_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000158.html", "Shizuoka City", "静岡市",
                            "Shizuoka City: Long-term trial homes for people moving to the city"),
    "jreast_odoriko": ("https://www.jreast.co.jp/en/multi/traininformation/odoriko/index.html", "JR East", "JR東日本",
                       "JR East: Odoriko (E257 series)"),
    "shizuoka_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000050.html", "Shizuoka City", "静岡市",
                       "Shizuoka City: Trial homes for people considering a move"),
    "okushizuoka_trial": ("https://www.city.shizuoka.lg.jp/s8937/okushizuoka/s000018.html", "Shizuoka City", "静岡市",
                          "Shizuoka City: Okushizuoka trial homes"),
}

ARTICLE = {
 "id": "akiya-try-first", "slug": "akiya-try-before-you-buy", "topic": "own", "place": None, "also": ["live"],
 "photo": ("yaizu-engawa", "Old wooden house with a long veranda and an overgrown garden", "An older house in Iwashigashima, Yaizu, before renovation."),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Own a home",
 "h1": "Buying an akiya in Japan? Live in one for a month first",
 "seo_title": "Buying an Akiya in Japan? Live in One for a Month First",
 "description": "Japan has about nine million empty homes, and foreigners aren’t banned from buying them. Spend a month in the town first: it tells you more than any listing.",
 "dek": "Japan has about nine million empty homes, and as of November 2026 foreigners aren’t banned from buying one. But the house is the easy part. The town is what you’re really signing up for, and a month there tells you more than any listing.",
 "card": "Japan has about nine million vacant homes, and foreigners can buy them. The town matters more than the house: how long you can stay, where to stay, and what a month shows you.",
 "keywords": [("buying an akiya in japan", "—", "—"), ("akiya", "3,600", "0")],
 "intent": "Do（比べたい・やり方）",
 "points": [
   "An akiya is an empty house. Japan had about 9.0 million of them on 1 October 2023, a record 13.8% of all homes.",
   "As of November 2026, foreigners aren’t banned from buying a home, but there’s more paperwork than before, and owning a house won’t get you a visa.",
   "A month in the town shows you what a listing can’t: the winter cold, whether you need a car, where you’ll shop and how the neighbours are.",
   "Most visa-exempt visitors can stay up to 90 days. Remote workers from certain countries can apply for a six-month digital nomad status.",
   "For somewhere to stay, you can look at a town’s trial home, a monthly rental or a guesthouse with monthly rates.",
 ],
 "body": """
<p>An akiya (空き家) is simply a house that nobody lives in. Japan’s 2023 Housing and Land Survey counted 9.0 million of them on 1 October 2023, a record 13.8% of the country’s homes [[s:stat_housing2023]]. About 3.86 million weren’t for rent or sale and weren’t anyone’s second home either, up by 369,000 since 2018 [[s:stat_housing2023]]. That’s the group people usually mean when they talk about Japan’s abandoned houses.</p>

<h2>Can foreigners buy an akiya?</h2>
<p>As of November 2026, Japan doesn’t ban foreigners or non-residents from buying a home, and you don’t need a visa to buy [[s:rej,mof_realprop_faq]]. There is more paperwork than before, though. Since April 2026, non-residents who buy property have to report it under the Foreign Exchange Act, even a home they plan to live in [[s:mof_fefta2026,mof_realprop_faq]]. Since 5 October 2026, every buyer, Japanese or not, gives their nationality when the purchase is registered [[s:moj_nationality]].</p>
<p>The rules are still moving. A bill sent to the Diet on 23 October 2026 would require government permission to buy land near key defence sites and on border islands, whatever your nationality [[s:cao_land_bill,cas_land_teigen]]. Buying a home also doesn’t come with a residence visa [[s:rej]]. Because all this is changing, it’s worth checking your own case with a lawyer or a judicial scrivener (<em>shiho shoshi</em>) before you sign.</p>
[[ed:Confirm the Diet status of the land bill as of the publishing date, and have someone check the wording of this section (legal content).]]

<h2>Why live in the town before you buy?</h2>
<p>The house is the cheap part. What you’re really committing to is the town, and a listing can only tell you so much: the price, the floor plan, a few photos. The things that decide whether you’ll be happy there only show up once you’ve lived there for a while.</p>
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

<h2>What only shows up once you live in an old house?</h2>
<p>The wiring and the internet, in our experience. We learnt this when one of our founding members rented an old house in Shimoda from its owner and turned it into a guesthouse. We rented rather than bought, but we think a buyer would run into the same things.</p>
<p>The old two-wire electrics couldn’t run the air conditioner, the fridge and the microwave all at once, so we had to ask guests not to use them together. Upgrading the wiring costs real money, so it’s something to find out before you budget, not after. Getting broadband put in took more than two months because it was the busy season, and we got by on a plug-in home router until then.</p>

<h2>How long can you stay in Japan to test a town?</h2>
<p>Long enough for a proper trial, for most people. There are two main ways to do it without a work or residence visa, and the rules below are as of November 2026.</p>
<div class="tablewrap"><table>
<thead><tr><th>Way to stay</th><th>How long</th><th>Who it’s for</th></tr></thead>
<tbody>
<tr><td><strong>Short-term visitor</strong>, visa-exempt</td><td>Up to 90 days for most visa-exempt nationalities. Some get 15 or 30 days, and some passports come with extra conditions [[s:mofa]].</td><td>Anyone from a visa-exempt country or region. It’s worth checking the rule for your own passport.</td></tr>
<tr><td><strong>Digital nomad</strong> status</td><td>Six months, and it can’t be renewed. Once six months have passed after you leave Japan, you can come back under it again [[s:isa_nomad_en]].</td><td>Nationals of countries and regions that are both visa-exempt and have a tax treaty with Japan [[s:isa_nomad_list]]. You need an annual income of at least ¥10 million and private medical insurance with at least ¥10 million of treatment cover, and you can’t work for a Japanese employer [[s:isa_nomad_en]].</td></tr>
</tbody></table></div>
<p class="fine">This is general information, not immigration advice. The list of eligible countries for the digital nomad status changes, so check it for your own passport.</p>
[[ed:Open MOFA’s visa exemption page and confirm the 90-day rule and the exceptions; open the Immigration Services Agency’s digital nomad page and list of eligible countries, and confirm each condition as of the publishing date.]]

<h2>Where can you stay for a month to test a town?</h2>
<p>You’ve got three main choices, and which one works depends on the town.</p>
<div class="tablewrap"><table>
<thead><tr><th>Option</th><th>How long</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>A town’s trial home</strong> (<em>otameshi jutaku</em>)</td><td>From a day or two up to a few months, and in one city up to two years [[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>Each town runs its own, with its own rules, and they’re mostly meant for people who plan to move there. Minami-Alps City in Yamanashi, for example, lets its Ashiyasu home for one to three months at ¥21,000 a month (page dated February 2026) [[s:minamialps_trial]]. Shizuoka City’s Okushizuoka homes take stays of three nights to two weeks, free of charge plus a ¥300 daily fee per group (page updated March 2025) [[s:okushizuoka_trial]].</td></tr>
<tr><td><strong>A monthly rental</strong></td><td>A month or more</td><td>A furnished room or flat let by the month. In a small town there may be few to choose from, so it helps to search early.</td></tr>
<tr><td><strong>A guesthouse or holiday home with monthly rates</strong></td><td>A week to a month or more</td><td>Often the easiest to book from abroad, and you can try living in an older house without committing to anything.</td></tr>
</tbody></table></div>
<p>Trial homes sound ideal, but there’s a catch: they’re built for people who are moving, not for people testing a town from abroad. Minami-Alps City’s home is for people registered as living outside Yamanashi who intend to move to the city and have signed up for a relocation consultation [[s:minamialps_trial]]. Its page doesn’t mention nationality, and we couldn’t find out whether someone living overseas counts.</p>
<p>Some cities spell it out. Shizuoka City’s long-term trial flats are city-run apartments you can rent for six months to under two years, but only if you live outside Shizuoka Prefecture and have decided to move to the city. Foreign nationals qualify only as permanent residents, long-term residents, special permanent residents or spouses of Japanese nationals (page updated August 2026) [[s:shizuoka_long_trial]]. So a tourist or digital nomad stay won’t qualify there. In our view, if you’re coming from abroad, a monthly rental or a guesthouse is usually the realistic choice, and it’s worth asking a town’s relocation office before you plan around a trial home.</p>
[[ed:Ask the Izu towns (Shimoda, Minamiizu, Izu City) whether they have trial homes of a month or more, what they cost, and whether foreign nationals or people living overseas can use them.]]
<p>Towns within reach of Tokyo are the easiest to test. Shimoda, on the [[l:izu|Izu Peninsula]], is under three hours away by direct train [[s:jreast_odoriko]], as our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] explains. If it’s on your list, our home there, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is one option among the ones above. It’s an older house in the old town, renovated for long stays and licensed under Japan’s Hotel Business Act, so it can take guests all year, with weekly and monthly discounts. Most of our guests so far have come from Europe and North America, and some come to work remotely.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, our home in Shimoda’s old town.]]
[[ed:Confirm before publishing: the monthly rate, whether stays of 30 nights or more can always be accepted, and whether we may call the Shimoda house a restored akiya.]]

<h2>What does a trial month look like?</h2>
<p>Mostly, it looks like ordinary life, and that’s the point. You’ll find your own rhythm, but the month tends to go something like this.</p>
<p>The first week goes on settling in. You find the supermarket, the clinic and the bus stop, and you work out the rubbish calendar. By the second week you’re working your usual hours and cooking at home, and you start to notice the small things that bother you.</p>
<p>The third week is a good time to ask around. You might visit the city hall desk that handles empty houses, talk to a local agent, or ask the neighbours what they’d fix first in a house like yours. By the fourth week you’ll have a fair idea of what would need to change, both about the house and about the way you live.</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
   ("Can foreigners buy property in Japan?",
    "As of November 2026 there’s no ban, but non-residents must report a purchase under the Foreign Exchange Act, and every buyer gives their nationality at registration [[s:mof_fefta2026,moj_nationality]]. The rules are changing, so it’s worth checking with a lawyer or judicial scrivener."),
   ("Does owning a house in Japan help me get a visa?",
    "No. In Japan, owning property and immigration status are separate [[s:rej]]."),
   ("Is a cheap house in Japan really cheap?",
    "Not always. The purchase price is only one part of the bill. Renovation, taxes, insurance and upkeep come on top, and they vary a lot from one building to the next, so it’s worth getting written quotes before you commit."),
   ("Can I use a town’s trial home as a foreigner?",
    "It depends on the town. Trial homes are mostly for people who plan to move there, and some spell out who qualifies. Shizuoka City’s long-term trial flats, for example, take foreign nationals only with permanent or long-term residence, or as the spouse of a Japanese national [[s:shizuoka_long_trial]]. It’s worth asking the town’s relocation office first."),
   ("How many akiya are there in Japan?",
    "About 9.0 million homes were empty on 1 October 2023, 13.8% of all housing, according to the 2023 Housing and Land Survey [[s:stat_housing2023]]."),
 ],
 "sources": ["stat_housing2023", "rej", "mof_fefta2026", "mof_realprop_faq", "moj_nationality", "cao_land_bill", "cas_land_teigen", "mofa",
             "isa_nomad_en", "isa_nomad_list", "minamialps_trial", "shizuoka_trial", "okushizuoka_trial", "shizuoka_long_trial", "jreast_odoriko"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "日本で空き家を買う前に、まず1か月住んでみる",
  "dek": "日本には約900万戸の空き家があり、2026年11月時点で、外国人が買うことは禁止されていません。でも、家を買うのは簡単なほうです。本当に引き受けるのは町のほうで、そこで1か月暮らすと、物件情報よりずっと多くのことが分かります。",
  "review": [
   "【2026-11-15 2回目の書き直し（リサーチメモ 2・組み込み後の採点の指摘）】変えた点: ①【事実の変更】京丹後市のお試し住宅は2026年9月末で市営の住宅が閉鎖されたため（市の閉鎖のお知らせ）、京丹後市を例から外し、出典 kyotango_trial も消しました。京丹後市にもとづいていた「1日から2か月ほどまで」は、「1〜2日から数か月まで、2年まで住める市もある」に直しました（静岡市 中心部・南アルプス市 1〜3か月・静岡市 長期 半年〜2年） ②お試し住宅の例を、リサーチ部が公式ページを開いて確かめた2つにしました。南アルプス市（芦安、1〜3か月・月21,000円、山梨県外に住民登録があり移住するつもりで移住相談に登録した人。国籍の記載なし）と、静岡市の長期お試し住宅（市営住宅に半年以上2年未満、静岡県外に住み移住を決めた人、外国籍は永住者・定住者・特別永住者・日本人の配偶者等に限る） ③お試し住宅は「移住する人のための仕組み」で、観光やデジタルノマドの滞在では使えない市があることを正直に書き、海外から来るならマンスリーか宿のほうが現実的だという見方を「私たちの考え」として添えました。FAQ の「外国人でも使えるか」も静岡市の例で答え直しました ④前の「たいてい町の外に住民登録がある人」という言い方（実際は県外が多い）をやめ、市ごとの条件をそのまま書きました ⑤「下田まで直通で3時間以内」に JR東日本（踊り子）の出典を付けました。数字は出していません ⑥「お試しの1か月」の節を、「1週目：…」のラベルの箇条書きから、ふつうの文章の段落に直しました ⑦伊豆の市町の黄色い枠を「1か月以上泊まれるか・料金・外国籍や海外在住の人が使えるか」に広げました",
   "【2026-11-15 品質保証部の指摘を受けた書き直し】変えた点: ①「購入に国籍・在留の制限はない」の断定をやめ、「2026年11月時点で禁止はないが、手続きは増えた（2026年4月から非居住者は外為法の報告、10月5日から登記で国籍の届出）。重要な区域の土地の許可制の法案が10月23日に国会に出ている」の形にし、専門家（弁護士・司法書士）に確かめるよう添えました（財務省・法務省・内閣府・内閣官房の出典） ②デジタルノマドを、出入国在留管理庁の条件どおりに直しました（対象はビザ免除かつ租税条約のある国・地域の人、年収1,000万円以上、治療費1,000万円以上の民間医療保険、日本の会社には雇われない、6か月で更新不可、出国から6か月たてば再び可）。時点は2026年11月 ③滞在の手段（観光の短期滞在・デジタルノマド）を表にしました ④空き家の数の出典を、総務省統計局の確報（2024年9月公表）1つにしました（900万戸・13.8%・過去最高、使い道のない空き家 約386万戸・2018年から36.9万戸増） ⑤「1か月泊まれる場所」の節を新しく書き、自治体のお試し住宅（自治体ごと、条件は町の外に住民登録があって移住を考えている人など。例は静岡市オクシズの3泊〜2週間・1組1日300円）、マンスリー、宿を表で並べました。NODE Shimoda はその中の1つとして紹介しています ⑥創業メンバーが下田で借りた古い家を宿に改修したときの体験を2点入れました（古い2芯の配線でエアコン・冷蔵庫・電子レンジを同時に使えなかった／繁忙期で回線工事に2か月以上かかり、置き型のルーターでしのいだ）。「買った」とは書かず「持ち主から借りた」と明記しています ⑦ゲストを「リモートで働く人がたくさん」→「リモートで働きに来る人もいる」に ⑧前の最後の節の「いちばんの近道」という押しの強い言い方をやめ、最後は1か月の過ごし方の節にしました。4週目も「決める」→「振り返る」に ⑨FAQ に「外国人は買えるか」「お試し住宅は外国人も使えるか」を足して5問にしました",
   "【人に確かめてほしい点】①法務・在留の記述（不動産購入の手続き、法案の審議状況、デジタルノマドの条件、90日と例外の国）は、公開の直前に一次のページを開いて確かめてください（黄色い枠2か所） ②創業メンバーの体験（配線・回線）の書き方が、事実と合っているか。「私たち（we）」の体験として書いています ③伊豆の市町（下田市・南伊豆町・伊豆市）に1か月以上泊まれるお試し住宅があるか、料金、外国籍・海外在住の人が使えるか（黄色い枠） ④月額料金、30泊以上を常に受けられるか、「再生した空き家」と呼んでよいか（黄色い枠） ⑤法務・在留の出典はリサーチ部が検索で確認したもので、本文のページは開けていません ⑥「下田まで直通の電車で3時間かからない」の出典の JR東日本の踊り子のページ（東京〜伊豆急下田 2時間49分）は、この環境から開けず検索でしか確かめていません。公開前にページを開いて確かめてください（ほかの記事は駅探の約2時間35分を使っているので、数字は出していません） ⑦南アルプス市・静岡市のお試し住宅の条件と料金（2026年11月15日にリサーチ部がページを開いて確認）が、公開の時点でも変わっていないか ⑧京丹後市を外したことでよいか（市営のお試し住宅は2026年9月末で閉鎖。民間・地域のお試し住宅は案内されていますが、例には使っていません）",
   "【入れられなかったこと】海外に住む人が南アルプス市などのお試し住宅の対象に入るか（ページに記載がなく、町に聞くように書きました）、伊豆の市町のお試し住宅の有無、新耐震基準（1981年）など建物の点検の項目（公的な出典を未確認）、マンスリーの部屋の相場（出典なし）。焼津・修善寺の家は、状況が決まるまで書いていません",
  ],
  "points": [
    "akiya（空き家）は、人が住んでいない家のこと。2023年10月1日時点で約900万戸、住宅全体の13.8%で、過去最高でした。",
    "2026年11月時点で、外国人が家を買うことは禁止されていません。ただ、手続きは前より増えていて、家を持ってもビザはもらえません。",
    "町で1か月暮らすと、物件情報では分からないことが見えてきます。冬の寒さ、車が要るか、どこで買い物するか、近所の人のこと。",
    "ビザ免除の国の人の多くは、90日まで滞在できます。特定の国のリモートワーカーなら、6か月の「デジタルノマド」の在留資格もあります。",
    "泊まる場所は、自治体のお試し住宅、マンスリーの部屋、月割のある宿の3つから考えられます。",
  ],
  "body": """
<p>akiya（空き家）は、ひとことで言えば、誰も住んでいない家のことです。2023年の住宅・土地統計調査では、2023年10月1日時点で900万戸、日本の住宅の13.8%が空き家で、割合は過去最高でした[[s:stat_housing2023]]。そのうち約386万戸は、貸すためでも売るためでもなく、別荘でもない家で、2018年から36万9千戸増えました[[s:stat_housing2023]]。「日本の放置された家」と言うとき、たいていはこの家のことを指しています。</p>

<h2>外国人は空き家を買えるのか</h2>
<p>2026年11月時点で、外国人や日本に住んでいない人が家を買うことは禁止されておらず、買うのにビザも要りません[[s:rej,mof_realprop_faq]]。ただ、手続きは前より増えました。2026年4月から、日本に住んでいない人が不動産を買うと、住むための家でも外為法にもとづく報告が要ります[[s:mof_fefta2026,mof_realprop_faq]]。2026年10月5日からは、日本人も含めて、買った人はみな登記のときに国籍を届け出ます[[s:moj_nationality]]。</p>
<p>決まりは、まだ動いています。2026年10月23日に国会に出された法案は、重要な防衛施設の周りや国境の離島の土地を買うのに、国籍を問わず政府の許可を求める内容です[[s:cao_land_bill,cas_land_teigen]]。また、家を買っても在留資格は付いてきません[[s:rej]]。こうした変化の途中なので、契約の前に、自分の場合を弁護士や司法書士に確かめておくと安心です。</p>
[[ed:公開の時点での法案の審議状況を確かめ、この節の言い方を人が確認してください（法務に関わる記述）。]]

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

<h2>古い家で、住んでみて初めて分かることは何か</h2>
<p>私たちの経験では、配線と回線です。創業メンバーの1人が、下田の古い家を持ち主から借りて、宿に改修したときに知りました。買ったのではなく借りた家ですが、買った人も同じことにぶつかると私たちは思います。</p>
<p>古い2芯の配線では、エアコンと冷蔵庫と電子レンジを同時に使えず、ゲストに同時に使わないようお願いすることになりました。配線をやり直すにはそれなりの費用がかかるので、予算を組む前に知っておきたいことです。インターネットの回線工事は、繁忙期だったこともあって申し込みから2か月以上かかり、それまでは置き型のホームルーターでしのぎました。</p>

<h2>町を試すために、日本にどれくらいいられるのか</h2>
<p>多くの人にとって、しっかり試せるくらいの長さはあります。就労や居住のビザなしで滞在する方法はおもに2つで、下の条件は2026年11月時点のものです。</p>
<div class="tablewrap"><table>
<thead><tr><th>滞在のしかた</th><th>期間</th><th>対象</th></tr></thead>
<tbody>
<tr><td><strong>短期滞在</strong>（ビザ免除）</td><td>ビザ免除の国・地域の多くは90日まで。15日や30日の国もあり、パスポートに条件が付く場合もあります[[s:mofa]]。</td><td>ビザ免除の国・地域の人。自分のパスポートの条件を確かめておくと安心です。</td></tr>
<tr><td><strong>デジタルノマド</strong>の在留資格</td><td>6か月で、更新はできません。日本を出てから6か月たてば、同じ資格でまた来られます[[s:isa_nomad_en]]。</td><td>ビザ免除で、かつ日本と租税条約のある国・地域の人[[s:isa_nomad_list]]。年収1,000万円以上と、治療費1,000万円以上を補償する民間の医療保険が必要で、日本の会社に雇われて働くことはできません[[s:isa_nomad_en]]。</td></tr>
</tbody></table></div>
<p class="fine">これは一般的な情報で、在留手続きの助言ではありません。デジタルノマドの対象の国は変わるので、自分のパスポートで確かめてください。</p>
[[ed:外務省の査証免除のページで90日と例外の国を、出入国在留管理庁のデジタルノマドのページと対象国の一覧で各条件を、公開の時点で開いて確かめてください。]]

<h2>町を試すために1か月泊まれる場所はどこか</h2>
<p>おもな選択肢は3つで、どれが合うかは町しだいです。</p>
<div class="tablewrap"><table>
<thead><tr><th>選択肢</th><th>期間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>自治体のお試し住宅</strong></td><td>町によって、1〜2日から数か月まで。2年まで住める市もあります[[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>町ごとに運営していて、決まりもそれぞれで、多くは移住するつもりの人に向けたものです。たとえば山梨県の南アルプス市は、芦安のお試し住宅を1〜3か月、月21,000円で貸しています（2026年2月掲載のページ）[[s:minamialps_trial]]。静岡市の「オクシズ」のお試し住宅は、3泊4日〜2週間、宿泊は無料で、体験料が1組1日300円です（2025年3月更新のページ）[[s:okushizuoka_trial]]。</td></tr>
<tr><td><strong>マンスリーの部屋</strong></td><td>1か月以上</td><td>家具付きの部屋を月単位で借ります。小さな町では選べる数が少ないこともあるので、早めに探すと安心です。</td></tr>
<tr><td><strong>月割のある宿・貸別荘</strong></td><td>1週間〜1か月以上</td><td>海外からいちばん予約しやすいことが多く、何も契約せずに古い家での暮らしを試せます。</td></tr>
</tbody></table></div>
<p>お試し住宅はよさそうに見えますが、落とし穴があります。移住する人のための仕組みで、海外から町を試しに来る人向けではないのです。南アルプス市のお試し住宅は、山梨県の外に住民登録があり、市に移住するつもりで、移住の相談に登録した人が対象です[[s:minamialps_trial]]。ページに国籍の条件は書かれておらず、海外に住む人が対象に入るかは確かめられませんでした。</p>
<p>はっきり書いている市もあります。静岡市の「長期お試し住宅」は、市営住宅に半年以上2年未満住めるものですが、静岡県の外に住んでいて、市への移住を決めた人が対象です。外国籍の人は、永住者・定住者・特別永住者・日本人の配偶者等の在留資格がある場合に限られます（2026年8月更新のページ）[[s:shizuoka_long_trial]]。つまり、観光やデジタルノマドの滞在では使えません。私たちの考えでは、海外から来るなら、マンスリーの部屋か宿のほうが現実的です。お試し住宅をあてにする前に、町の移住の担当窓口に聞いておくと安心です。</p>
[[ed:伊豆の市町（下田市・南伊豆町・伊豆市）に1か月以上泊まれるお試し住宅があるか、料金、外国籍・海外在住の人が使えるかを問い合わせてください。]]
<p>東京から行きやすい町のほうが試しやすく、[[l:izu|伊豆半島]]の下田なら直通の電車で3時間かかりません[[s:jreast_odoriko]]（[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]）。候補に入っているなら、下田の私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」も、上の選択肢の1つです。旧町内の古い家を長期滞在向けに改修したもので、旅館業法の許可を受けているので一年中泊まれ、週割・月割があります。これまでのゲストは欧米の人が中心で、リモートで働きに来る人もいます。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|下田の旧町内にある私たちの家「NODE Shimoda」のリビング。]]
[[ed:公開前に要確認：月額料金、30泊以上を常に受けられるか、下田の家を「再生した空き家」と呼んでよいか。]]

<h2>お試しの1か月は、どんなふうに過ぎるか</h2>
<p>ほとんどは、ふだんの暮らしそのものです。そこに意味があります。ペースは人それぞれですが、だいたい次のように過ぎていきます。</p>
<p>最初の1週間は、落ち着くための時間です。スーパーや診療所、バス停を見つけて、ごみの収集日を覚えます。2週目になると、いつもの時間に働いて家で料理をするようになり、小さな気になることが見えてきます。</p>
<p>3週目は、聞いてまわるのにちょうどいい頃です。役所の空き家の窓口に行ったり、地元の不動産屋と話したり、近所の人に「こういう家なら、最初にどこを直すか」を聞いたりできます。4週目には、家について、そして自分の暮らし方について、何を変える必要がありそうか、だいたい見えています。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
    ("外国人は日本の不動産を買えますか",
     "2026年11月時点で禁止はありませんが、日本に住んでいない人は外為法にもとづく報告が要り、買った人はみな登記のときに国籍を届け出ます[[s:mof_fefta2026,moj_nationality]]。決まりが変わりつつあるので、弁護士や司法書士に確かめておくと安心です。"),
    ("日本で家を持つと、ビザを取りやすくなりますか",
     "なりません。日本では、不動産を持つことと在留資格は別の話です[[s:rej]]。"),
    ("日本の安い家は、本当に安いのですか",
     "そうとは限りません。購入価格は、かかるお金の一部です。改修、税金、保険、維持費が上乗せされ、金額は建物によって大きく変わるので、決める前に書面で見積もりを取っておくと安心です。"),
    ("外国人でも、自治体のお試し住宅を使えますか",
     "町しだいです。お試し住宅は、多くが移住するつもりの人向けで、対象をはっきり書いている町もあります。たとえば静岡市の長期お試し住宅は、外国籍の人なら、永住者・定住者などの在留資格か、日本人の配偶者である場合に限られます[[s:shizuoka_long_trial]]。まず町の移住の担当窓口に聞いておくと安心です。"),
    ("日本に空き家は何戸ありますか",
     "2023年の住宅・土地統計調査によると、2023年10月1日時点で約900万戸、住宅全体の13.8%が空き家でした[[s:stat_housing2023]]。"),
  ],
 },
}
