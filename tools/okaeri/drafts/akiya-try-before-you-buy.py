# -*- coding: utf-8 -*-
"""akiya-try-first の書き直し（2026-11-16 手離れ: 黄色い枠をなくし、リサーチメモ（2026-11-16）の公式の出典で仕上げた）。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "stat_housing2023": ("https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf", "Statistics Bureau of Japan", "総務省統計局",
                         "Statistics Bureau of Japan: 2023 Housing and Land Survey, final basic tabulation (2024)"),
    "isa_nomad_en": ("https://www.moj.go.jp/isa/applications/status/designatedactivities53_00001.html", "Immigration Services Agency",
                     "出入国在留管理庁", "Immigration Services Agency: Designated Activities (Digital Nomad)"),
    "isa_nomad_list": ("https://www.moj.go.jp/isa/content/001416932.pdf", "Immigration Services Agency (country list)", "出入国在留管理庁（対象の国・地域）",
                       "Immigration Services Agency: Eligible countries and regions for the digital nomad status"),
    "mof_fefta2026": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/recent_revised/gaitamehou_20260220.html",
                      "Ministry of Finance", "財務省", "Ministry of Finance: Revision of reporting rules under the Foreign Exchange Act (20 February 2026)"),
    "mof_realprop_faq": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/real_property/FAQ_J.pdf", "Ministry of Finance (FAQ)",
                         "財務省（FAQ）", "Ministry of Finance: FAQ on reports of real property acquisition (June 2026)"),
    "moj_nationality": ("https://www.moj.go.jp/content/001470076.pdf", "Ministry of Justice", "法務省",
                        "Ministry of Justice: Notice on recording nationality in property registration (4 September 2026)"),
    "cao_land_bill": ("https://www.cao.go.jp/houan/222/index.html", "Cabinet Office", "内閣府", "Cabinet Office: Bills submitted to the 222nd Diet session"),
    "cao_land_bill_outline": ("https://www.cao.go.jp/houan/pdf/222/222_1gaiyou.pdf", "Cabinet Office (bill outline)", "内閣府（法案の概要）",
                              "Cabinet Office: Outline of the bill to amend the Act on the Review and Regulation of the Use of Real Estate around Important Facilities and on Remote Territorial Islands (2026)"),
    "minamialps_trial": ("https://www.city.minami-alps.yamanashi.jp/docs/12876.html", "Minami-Alps City", "南アルプス市",
                         "Minami-Alps City: Trial homes for people considering a move"),
    "shizuoka_long_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000158.html", "Shizuoka City (long-term)", "静岡市（長期）",
                            "Shizuoka City: Long-term trial homes for people moving to the city"),
    "jre_tt_tokyo": ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetables", "JR東日本の時刻表",
                     "JR East timetables from Tokyo Station: Tokaido Shinkansen and Tokaido, Ito and Izukyu lines (November 2026)"),
    "shizuoka_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000050.html", "Shizuoka City", "静岡市",
                       "Shizuoka City: Trial homes for people considering a move"),
    "shugiin_bill18": ("https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/keika/1DE36CA.htm", "House of Representatives", "衆議院（議案審議経過情報）",
                       "House of Representatives: Progress of cabinet bill no. 18, 222nd Diet session (checked 16 November 2026)"),
    "jnto_visa": ("https://www.japan.travel/en/plan/visa-info/visa-immigration/", "JNTO", "日本政府観光局（入国とビザ）",
                  "JNTO: Entry into Japan and visa information (checked November 2026)"),
    "shimoda_stay_subsidy": ("https://city.shimoda.shizuoka.jp/file/下田市移住希望者滞在費補助金交付要綱.pdf", "Shimoda City", "下田市（移住希望者滞在費補助金交付要綱）",
                             "Shimoda City: Rules for the stay subsidy for people considering a move (amended March 2026)"),
    "node_access": ("https://nodeshimoda.com/access", "NODE Shimoda (access)", "NODE Shimoda 公式サイト（アクセス）",
                    "NODE Shimoda official site: access (checked November 2026)"),
}

ARTICLE = {
 "id": "akiya-try-first", "slug": "akiya-try-before-you-buy", "topic": "own", "place": None, "also": ["live"],
 "photo": ("yaizu-engawa", "Old wooden house with a long veranda and an overgrown garden", "An older house in Iwashigashima, Yaizu, before renovation."),
 "published": "2026-11-14", "updated": "2026-11-16",
 "kicker": "Own a home",
 "h1": "Buying an akiya in Japan? Live in one for a month first",
 "seo_title": "Buying an Akiya in Japan? Live in One for a Month First",
 "description": "Japan has nine million empty homes. Non-residents can buy one, reporting it to the Ministry of Finance since April 2026. A month in the town tells you more.",
 "dek": "In 2023, Japan had about nine million empty homes, and non-residents can buy one. But you’re buying into the town, and a month there tells you more than any listing.",
 "card": "You can buy one of Japan’s nine million empty homes, but the town matters more than the house. A month there shows you what heating or cooling really costs, whether you need a car and how the neighbours are, and a monthly rental or guesthouse is the realistic way to do it from abroad.",
 "keywords": [("buying an akiya in japan", "—", "—"), ("akiya", "3,600", "0")],
 "intent": "Do（比べたい・やり方）",
 "points": [
   "Since April 2026, non-residents who buy a home have had to report it to the Ministry of Finance.",
   "A month shows you whether you need a car, how the neighbours are and what heating or cooling really costs.",
   "From abroad, a monthly rental or a guesthouse with monthly rates is usually more realistic than a town’s trial home.",
 ],
 "body": """
<p>An akiya (空き家) is simply a house that nobody lives in. Japan’s 2023 Housing and Land Survey counted 9.0 million of them on 1 October 2023, a record 13.8% of the country’s homes [[s:stat_housing2023]]. About 3.86 million weren’t for rent or sale and weren’t anyone’s second home either, up by 369,000 since 2018 [[s:stat_housing2023]]. In our experience, that’s usually the group people mean when they talk about Japan’s abandoned houses.</p>

<h2>Can foreigners buy an akiya?</h2>
<p>Yes. Non-residents can buy, and the Ministry of Finance’s rules spell out what they need to do. Since April 2026, a non-resident who buys property in Japan has to report the purchase to the ministry under the Foreign Exchange Act, even a home they plan to live in [[s:mof_fefta2026,mof_realprop_faq]]. Real Estate Japan, a property site for foreign buyers, makes the same point: you don’t need to live in Japan to buy [[s:rej]]. Since 5 October 2026, every buyer, Japanese or not, gives their nationality when the purchase is registered [[s:moj_nationality]].</p>
<p>The rules are still moving. A bill before the Diet would create new zones within about 1 km of some defence and coast guard sites, and on uninhabited border islands [[s:cao_land_bill,cao_land_bill_outline]]. Every transfer of land ownership in those zones would need the government’s approval in advance, and the changes would take effect within 18 months of the act being promulgated [[s:cao_land_bill_outline]]. As of mid-November 2026, the bill was still before the House of Representatives, so it isn’t law yet [[s:shugiin_bill18]].</p>
<p>We’d also treat a house and a visa as two separate questions. If you’re hoping that owning a home will help you stay in Japan longer, ask an administrative scrivener (<em>gyoseishoshi</em>) who handles visas before you count on it. With the rules changing this fast, we think it’s sensible to have a lawyer or judicial scrivener (<em>shiho shoshi</em>) look at your own case before you sign.</p>

<h2>Why live in the town before you buy?</h2>
<p>Buying the house is the easy part. What you’re really committing to is the town, and a listing can only tell you so much: the price, the floor plan, a few photos. The things that decide whether you’ll be happy there only show up once you’ve lived there for a while.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What you want to know</th><th>How a month shows you</th></tr></thead>
<tbody>
<tr><td>How cold an old wooden house gets in January, and what heating costs</td><td>You’ll feel it on the first cold night and see it on the electricity bill.</td></tr>
<tr><td>Whether daily life works without a car</td><td>A week of shopping and errands on foot, by bus or by bike makes it obvious, especially if you try the trips that aren’t on your doorstep, too.</td></tr>
<tr><td>Where you’ll buy food, and when the shops close</td><td>Cooking most of your own meals soon shows you what’s easy to find and what isn’t.</td></tr>
<tr><td>How rubbish sorting works on that street</td><td>You’ll be following the local collection calendar like everyone else. If there’s an English version, it’s worth asking city hall for it.</td></tr>
<tr><td>Whether the internet holds up for a working day</td><td>Normal working hours, video calls included, are the real test.</td></tr>
<tr><td>What humid months and typhoons do to the building</td><td>Neighbours and local builders know what tends to fail first in houses like it.</td></tr>
<tr><td>How the neighbourhood treats a newcomer</td><td>Saying hello, joining a clean-up day if there is one, and asking how other newcomers settled in will tell you a lot. Neighbours notice small things, too. When our broadband was being installed in Shimoda, we heard from neighbours about where the engineer’s van was parked.</td></tr>
</tbody></table></div>
<p>None of this comes up in a viewing.</p>

<h2>What only shows up once you live in an old house?</h2>
<p>The wiring and the internet, in our experience. We learnt this when one of our founding members rented an older flat in Shimoda from its owner and turned it into a guesthouse. We rented rather than bought, but we think a buyer would run into the same things.</p>
<p>The old two-wire electrics couldn’t run the air conditioner, the fridge and the microwave all at once, so we had to ask guests not to use them together. Upgrading the wiring costs real money, so it’s something to find out before you budget, not after. Getting broadband put in took more than two months because it was the busy season, and we got by on a plug-in home router until then.</p>
<p>The wiring and the wait for broadband are small examples of a bigger point. With a cheap old house, the asking price is only part of what you’ll pay. Renovation, taxes, insurance and upkeep come on top, and they vary so much from one building to the next that only written quotes will tell you the real figure.</p>

<h2>Which way of staying lets you spend a trial month in a town?</h2>
<p>For most people, either of two ways works without a work or residence visa, and both give you long enough for a proper trial. The rules below are as of November 2026.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Way to stay</th><th>How long</th><th>Who it’s for</th></tr></thead>
<tbody>
<tr><td><strong>Short-term visitor</strong>, visa-exempt</td><td>Up to 90 days for most visa-exempt nationalities, though some are given 15, 30 or 180 days [[s:jnto_visa]].</td><td>Anyone from a visa-exempt country or region. You can’t do paid work on this status, and the rule for your own passport is the one that counts [[s:jnto_visa]].</td></tr>
<tr><td><strong>Digital nomad</strong> status</td><td>Six months, and it can’t be renewed. You can apply for it again six months after you leave Japan [[s:isa_nomad_en]].</td><td>Nationals of countries and regions that are both visa-exempt and have a tax treaty with Japan [[s:isa_nomad_list]]. You need an annual income of at least ¥10 million and private medical insurance with at least ¥10 million of treatment cover, and you can’t work for a Japanese employer [[s:isa_nomad_en]].</td></tr>
</tbody></table></div>
<p>If the digital nomad route fits you, our [[l:digital-nomad|guide to Japan’s digital nomad visa]] has more on who qualifies and how it works.</p>
<p>For extensions, longer statuses and what happens if you leave and come back, see our guide to [[l:how-long-stay|how long you can stay in Japan]].</p>
<p class="fine">This is general information, not immigration advice. The list of eligible countries for the digital nomad status changes, so check it for your own passport.</p>

<h2>Where can you stay for a month to test a town?</h2>
<p>You’ve got three main choices: a town’s trial home, a monthly rental, or a guesthouse with monthly rates. Which one works depends on the town, and on where you’re coming from.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Option</th><th>How long</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>A town’s trial home</strong> (<em>otameshi jutaku</em>)</td><td>From a day or two up to a few months, and in one city for up to just under two years [[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>Each town sets its own rules, mostly for people planning to move. Minami-Alps City rents its trial home for one to three months at ¥21,000 a month (February 2026) [[s:minamialps_trial]].</td></tr>
<tr><td><strong>A monthly rental</strong></td><td>A month or more</td><td>A furnished room or flat let by the month. In a small town there may be few to choose from, so it helps to search early.</td></tr>
<tr><td><strong>A guesthouse or holiday home with monthly rates</strong></td><td>A week to a month or more</td><td>Often the easiest to book from abroad, and you can try daily life in the town without committing to anything.</td></tr>
</tbody></table></div>
<p>Trial homes sound ideal, but there’s a catch: they’re built for people who are moving, not for people testing a town from abroad. Minami-Alps City’s home is for people registered as living outside Yamanashi who intend to move to the city and have signed up for a relocation consultation [[s:minamialps_trial]]. Nationality isn’t one of the listed conditions, so if you live overseas, the city’s relocation desk can tell you whether you’d qualify.</p>
<p>Some cities spell it out. Shizuoka City’s long-term trial flats are city-run apartments you can rent for six months to under two years, but only if you live outside Shizuoka Prefecture and have decided, or are preparing, to move to the city. Foreign nationals qualify only as permanent residents, long-term residents, special permanent residents, or the spouse or child of a Japanese national (page updated August 2026) [[s:shizuoka_long_trial]]. So a tourist or digital nomad stay won’t qualify there. In our view, if you’re coming from abroad, a monthly rental or a guesthouse is usually the realistic choice, and our [[l:monthly-rental|guide to monthly rentals in Japan]] has more on how they work. If you’ve set your heart on a trial home, the town’s relocation office is the first call to make.</p>
<p>Shimoda City takes another route. Under rules in force since April 2026, it pays half the rate at designated hotels for people thinking of moving there, up to ¥4,000 a night for stays of up to 10 nights [[s:shimoda_stay_subsidy]]. But you need to be registered as living in Japan outside Shizuoka Prefecture, so it won’t help if you’re coming from abroad [[s:shimoda_stay_subsidy]].</p>
<p>Towns within reach of Tokyo are the easiest to test. As of November 2026, the daily direct trains from Tokyo Station reach Shimoda, on the [[l:izu|Izu Peninsula]], in 2 hours 29 to 44 minutes [[s:jre_tt_tokyo]]. Our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] has the details.</p>
<p>If Shimoda is on your list, we run a small place there called <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, which can be a base while you get a feel for the town. It’s a renovated flat of about 40 m² in an apartment building in the old town, 8 minutes’ walk from Izukyu-Shimoda Station [[s:node_room,node_access]]. Our site describes it as handy for medium and long stays [[s:node_site]], and it’s licensed under Japan’s Hotel Business Act. Most of our guests so far have come from Europe and North America, and some come to work remotely.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, our flat in Shimoda’s old town.]]

<h2>What does a trial month look like?</h2>
<p>Mostly, it looks like ordinary life, with a few deliberate tests built in. Based on what caught us out in Shimoda, we’d plan it roughly week by week.</p>
<p>The first week goes on settling in: the supermarket, the clinic, the bus stop and the rubbish calendar. If you’re staying in an older building, ask your host what amperage the electricity contract allows and where the breaker box is. The old wiring in our Shimoda flat couldn’t run the air conditioner, fridge and microwave at the same time. The amperage tells you roughly how much you can run at once, and knowing where the breaker box is turns a tripped switch into a quick fix.</p>
<p>By the second week you’re working your usual hours and cooking at home. That’s when you find out whether the connection survives a day of video calls, and you’ll see what heating or cooling really costs. It’s also a good moment to ask a local provider how long a new line takes there, since ours took more than two months.</p>
<p>The third week is for asking around. You might visit the city hall desk that handles empty houses, talk to a local agent, or ask a builder roughly what rewiring an old house costs. Neighbours are often the best people to tell you what humid summers and typhoons do to houses like theirs.</p>
<p>By the fourth week you’ll have a fair idea of what would need to change, about the house and about the way you live. Writing those costs and doubts down while they’re fresh makes it much easier to compare towns, or to walk away.</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
   ("Can foreigners buy property in Japan?",
    "Yes. Non-residents can buy, and since April 2026 they’ve had to report the purchase to the Ministry of Finance under the Foreign Exchange Act. Every buyer also gives their nationality at registration [[s:mof_fefta2026,moj_nationality]]. The rules are changing, so a lawyer or judicial scrivener can check your own case."),
   ("Will owning a house in Japan help me get a visa?",
    "We wouldn’t count on it. We treat a house and a visa as separate questions, so if staying longer is part of your plan, ask an administrative scrivener (<em>gyoseishoshi</em>) who handles visas before you buy."),
   ("Is a cheap house in Japan really cheap?",
    "Not always. The purchase price is only one part of the bill. Renovation, taxes, insurance and upkeep come on top, and they vary a lot from one building to the next, so written quotes are the only way to know before you commit."),
   ("Can I use a town’s trial home as a foreigner?",
    "It depends on the town. Trial homes are mostly for people who plan to move there, and some spell out who qualifies. As of August 2026, Shizuoka City’s long-term trial flats took foreign nationals only with permanent, long-term or special permanent residence, or as the spouse or child of a Japanese national [[s:shizuoka_long_trial]]. The town’s relocation office will know the current rules."),
   ("How many akiya are there in Japan?",
    "About 9.0 million homes were empty on 1 October 2023, 13.8% of all housing, according to the 2023 Housing and Land Survey [[s:stat_housing2023]]."),
 ],
 "sources": ["stat_housing2023", "rej", "mof_fefta2026", "mof_realprop_faq", "moj_nationality", "cao_land_bill", "cao_land_bill_outline", "shugiin_bill18", "jnto_visa",
             "isa_nomad_en", "isa_nomad_list", "minamialps_trial", "shizuoka_trial", "shizuoka_long_trial", "shimoda_stay_subsidy", "jre_tt_tokyo",
             "node_site", "node_room", "node_access"],
 "related": ["monthly-rental", "izu-from-tokyo", "izu"],
 "ja": {
  "h1": "空き家を買う前に、まず1か月住んでみる",
  "dek": "2023年時点で、日本には約900万戸の空き家があり、日本に住んでいない人も買うことができます。でも本当に引き受けるのは町のほうで、そこで1か月暮らすと、物件情報よりずっと多くのことが分かります。",
  "review": [
   "【2026-11-19 公開前の導線の直し】①「1か月泊まれる場所」の節にマンスリーの部屋の記事へのリンク、ビザの表の下にデジタルノマドビザの記事へのリンクを1本ずつ足しました ②関連記事の先頭にマンスリーの部屋の記事を入れました（3本） ③一覧のカードの「冬の寒さ」を「冷暖房に実際いくらかかるか」に替え、本文・In short とそろえました。事実・出典は変えていません",
   "【2026-11-16 品質保証部（91点・ゲート違反1）の指摘での直し】変えた点: ①【ゲート】NODE Shimoda の段落の「上の宿の選択肢の1つ」をやめ、表の「月割のある宿（1か月以上）」の行とつながらないようにしました。「町の様子をつかむあいだの拠点にしてもらえる」「公式サイトでは中長期の滞在にも便利な宿として紹介」までにし、月割や1か月以上泊まれるとは書いていません ②下田市の補助に「2026年4月施行の要綱」と時点を足し、1〜2文に短くしました（1泊4,000円までと、海外からは使えないことだけ。11〜30泊の80,000円は本文から外しました） ③法案の施行を「公布から18か月以内（within 18 months of the act being promulgated）」にそろえ、law の重なりをなくしました ④法案の段落の時点を「2026年11月中旬」の1回だけにしました（冒頭の「2026年11月時点で」を削除）",
   "【2026-11-16 手離れ（黄色い枠をすべてなくした。playbook 3-2）】変えた点: ①【事実の追加】土地の法案: 衆議院の議案審議経過で「2026年11月中旬の時点で、まだ衆議院で審議中。法律になっていない」と書きました（出典 shugiin_bill18。10月23日受理・11月10日に内閣委員会に付託、成立・公布はまだ）。施行は「公布から18か月（1年6か月）以内」に英語版・日本語版ともそろえました ②【事実の変更】ビザなしの短期滞在: 出典を外務省（この環境から開けない mofa）から日本政府観光局の入国・ビザのページ（jnto_visa）に替え、「15日や30日の国もある」→「15日・30日・180日の国もある」に。「パスポートに条件が付く場合もある」は出典にないので削り、「この滞在では報酬を得る仕事はできない」を足しました ③デジタルノマドは編集長が出入国在留管理庁のページで確かめた内容と一致しているので、本文はそのままで枠だけ外しました ④家と在留資格の関係は公的な出典が見つからないため、断定は書かず、「家とビザは別の問題として考え、あてにする前に行政書士に聞く」という私たちの見方だけを残しました ⑤【事実の追加】伊豆の町のお試し住宅（伊豆市・南伊豆町）は公式ページで確かめられなかったので書いていません。代わりに、下田市の移住希望者の滞在費補助（市が指定する宿の宿泊料の半分、10泊まで1泊4,000円まで、11〜30泊続けてなら80,000円まで）を書き、対象が「静岡県外ですでに日本に住民登録があり、移住相談に登録した人」なので、海外から来る人は使えないと分かるようにしました（出典 shimoda_stay_subsidy。2026年3月改正の要綱） ⑥【事実の変更】NODE Shimoda を「古い家（older house）」→「旧町内のアパートの一室（約40㎡）を改装したもの、伊豆急下田駅から徒歩8分」に（公式サイトの客室・アクセスのページ）。「長めの滞在にも向く」は公式サイトの「中長期の滞在にも便利」にもとづき、30泊以上を受けるとは書いていません。写真の説明も「私たちの部屋」に ⑦体験の節の「下田の古い家を借りた」→「下田の古い部屋（older flat）を借りた」、1週目の「私たちの家の古い配線」→「下田の私たちの部屋の古い配線」に（experience.md 3-2 で NODE Shimoda と同じ施設と確認済み）。一軒家と読める言い方をなくしました ⑧宿の行の「古い家での暮らしを試せる」→「その町での暮らしを試せる」、1週目の「古い家に泊まっているなら」→「古い建物に泊まっているなら」 ⑨出典: shugiin_bill18・jnto_visa・shimoda_stay_subsidy・node_access を新しく（SOURCES_NEW）、node_site・node_room を使い、mofa を外しました",
   "【今回、人に確かめてほしい点】なし（黄色い枠はありません）。参考までに: 下田市の補助の対象の宿の一覧は確かめていないので、NODE Shimoda が対象かは書いていません。デジタルノマドの条件は、出入国在留管理庁のページがこの環境から開けず、編集長が2026-11-16に確かめた内容を使っています",
   "【2026-11-16 冒頭を短く（playbook 2章の1）】dek を2文・30語以内、In short を3項目・各20語以内にしました。空き家の数に「2023年時点」を付け、In short の「冬の寒さ」（冬の1か月でないと成り立たない）を、本文にある「冷暖房に実際いくらかかるか」に替えました。外した情報（空き家の割合13.8%、家とビザは別の話、2026年11月時点の90日の滞在・デジタルノマド、冬の寒さ）は本文にそのまま残っています。",
   "【2026-11-15 品質保証部（HTML）の指摘での書き直し】変えた点: ①デジタルノマド: 入管庁の英語のページに合わせ「出国後6か月たてば、もう一度申請できる（apply for it again six months after you leave）」に ②【言い方の変更】購入: 「日本は外国人の購入を禁止していない」をやめ、財務省の制度を主語に「日本に住んでいない人も買える。2026年4月からは、住むための家でも外為法にもとづいて財務省に報告する」にしました。民間サイト Real Estate Japan（rej）は「買うのに日本に住んでいる必要はない」という補足の1文だけに使っています。description・dek・card・In short・FAQ もそろえました ③静岡市の長期お試し住宅: 「移住を決めた、または準備している人」「日本人の配偶者等（配偶者や子）」に（本文・FAQ） ④「これは安い家すべてに言えること」を、「配線と回線工事の待ちは、もっと大きな話の小さな例。安い古い家では、売り出し価格はかかるお金の一部にすぎない」と、下田の体験から一般論へつなぐ形に ⑤1週目の「この2つが分かると…」を2文に分け、アンペア数＝一度にどれくらい使えるか、ブレーカーの場所＝落ちてもすぐ戻せる、と何を指すかをはっきりさせました ⑥「なぜ町で暮らすのか」の表の車の行から自社の家への言及を外しました（自社の家に触れるのは NODE Shimoda の段落の1回だけ） ⑦一覧のカード（card）を、目次の読み上げから答え（買えるが町のほうが大事、1か月で冬の寒さ・車・近所が分かる、海外からはマンスリーか宿）に替えました ⑧お試しの1か月の節の冒頭の「私たちならこう過ごす、という例です」というページの予告を、「週ごとにおおよそこう組み立てると思います」に",
   "【2026-11-15 時点の確認事項（2026-11-16 にすべて解決）】①NODE Shimoda を英語で「house（一軒家）」と呼んでよいか、さらに「older house（古い家）」と呼んでよいか、1週目の「私たちの家の古い配線」がこの家を指してよいか（黄色い枠） ②「買うのに日本に住んでいる必要はない」は Real Estate Japan（民間）の記載として書いています。ページの記載と合っているか ③購入の手続き（財務省への報告）は法務・制度の記述なので、公開前に財務省のページを開いて確かめてください",
   "【2026-11-15 組み込み前の仕上げ（品質保証部 90点・合格のあとの編集長の指摘8点）】変えた点: ①「家は安いほうの買い物」→「家を買うこと自体は簡単なほう」（リードと FAQ に合わせました）。配線の節の後に、改修・税金・保険・維持費が上乗せされ、本当の金額は書面の見積もりで分かる、の2文を足しました ②FAQ のお試し住宅の答えに特別永住者を足しました ③行政書士を英語で「在留資格（ビザ）の手続きを扱う行政書士（administrative scrivener）」と資格の名前で書きました（本文・FAQ） ④【事実の変更】「下田まで直通で3時間かからない」→「2026年11月時点で、東京駅から毎日走る直通で2時間29〜44分」。出典を編集長が確かめた JR東日本の東京駅の時刻表（jre_tt_tokyo）に替え、踊り子のページ（jreast_odoriko）は外しました ⑤南アルプス市の条件を「国籍は条件に挙げられていない」と制度の側から書きました ⑥NODE Shimoda の段落を3文にし、「一年中泊まれ、週割・月割がある」を削りました（黄色い枠から月額料金も外しました） ⑦「なぜ町で暮らすのか」の表の2行を、確認済みの体験（experience.md 3-2）につなげました。車の行に「下田の家は駅から徒歩10分ほどで、スーパー・コンビニ・飲食店が近い」、近所の行に「回線工事の車の停め方で近所から声をかけられた」 ⑧お試し1週目の「エアコン・冷蔵庫・電子レンジを同時に使ってみる」を、「泊まり先の人に契約のアンペア数とブレーカーの場所を聞く」に替えました。人に確かめてほしい点: 近所の行の書き方（experience.md では「工事の車両の駐車で近隣から指摘を受けた」）が、やわらげすぎ・強すぎになっていないか",
   "【2026-11-15 3回目の書き直し（品質保証部 84点・ゲート違反1、リサーチメモ 3）】変えた点: ①【事実の変更】土地の法案を、内閣府の法案の概要どおりに直しました。「重要な防衛施設の周りや国境の離島、国籍を問わず許可」→「一部の防衛関係施設と海上保安庁の施設の周り（おおむね1km）と無人の国境離島に区域をつくり、区域内の土地の所有権の移転はすべて事前許可。公布から1年6か月以内に施行」。審議の状況は「2026年11月時点で国会にかかっている」だけにし、10月23日の日付と内閣官房の提言の出典（cas_land_teigen）は外しました。新しい出典 cao_land_bill_outline を足しました ②【主張の変更】「家を買っても在留資格は付かない」「買うのにビザは要らない」は公的な出典が見つからなかったので、断定をやめました。本文・In short・FAQ とも「家とビザは別々の問題として考える、あてにする前に行政書士に聞く」という私たちの見方にし、黄色い枠を足しました ③description・card・In short の4項目目に「2026年11月時点」、FAQ のお試し住宅に「2026年8月時点」を入れました ④「海外に住む人が対象か確かめられなかった」という調べた側の言い方をやめ、「市の移住の窓口に聞けば分かる」にしました ⑤「it’s worth …」を7回から1回に減らし、締めの言い方を変えました（日本語版の「〜しておくと安心です」も同じように減らしました） ⑥「泊まれる場所」の節の最初の文で3つの選択肢の名前を言い、表のお試し住宅の欄を短くしました（静岡市オクシズの例と出典 okushizuoka_trial は外しました） ⑦「お試しの1か月」の節を、下田での体験（配線・回線工事の待ち）と表の項目につなげ、週ごとに試すこと（家電の同時使用、ビデオ会議と冷暖房費、回線工事にかかる期間を業者に聞く、配線のやり直しの費用を工務店に聞く、湿気・台風のことを近所に聞く、費用と迷いを書きとめる）を具体的にしました。新しい事実は足していません ⑧日本語版の伊豆半島への内部リンクを、日本語版の記事（ja-izu）に向くよう直しました ⑨In short の5項目目に「海外からならマンスリーか宿が現実的」を足しました（本文の見方と同じ）",
   "【2026-11-15 2回目の書き直し（リサーチメモ 2・組み込み後の採点の指摘）】変えた点: ①【事実の変更】京丹後市のお試し住宅は2026年9月末で市営の住宅が閉鎖されたため（市の閉鎖のお知らせ）、京丹後市を例から外し、出典 kyotango_trial も消しました。京丹後市にもとづいていた「1日から2か月ほどまで」は、「1〜2日から数か月まで、2年まで住める市もある」に直しました（静岡市 中心部・南アルプス市 1〜3か月・静岡市 長期 半年〜2年） ②お試し住宅の例を、リサーチ部が公式ページを開いて確かめた2つにしました。南アルプス市（芦安、1〜3か月・月21,000円、山梨県外に住民登録があり移住するつもりで移住相談に登録した人。国籍の記載なし）と、静岡市の長期お試し住宅（市営住宅に半年以上2年未満、静岡県外に住み移住を決めた人、外国籍は永住者・定住者・特別永住者・日本人の配偶者等に限る） ③お試し住宅は「移住する人のための仕組み」で、観光やデジタルノマドの滞在では使えない市があることを正直に書き、海外から来るならマンスリーか宿のほうが現実的だという見方を「私たちの考え」として添えました。FAQ の「外国人でも使えるか」も静岡市の例で答え直しました ④前の「たいてい町の外に住民登録がある人」という言い方（実際は県外が多い）をやめ、市ごとの条件をそのまま書きました ⑤「下田まで直通で3時間以内」に JR東日本（踊り子）の出典を付けました。数字は出していません ⑥「お試しの1か月」の節を、「1週目：…」のラベルの箇条書きから、ふつうの文章の段落に直しました ⑦伊豆の市町の黄色い枠を「1か月以上泊まれるか・料金・外国籍や海外在住の人が使えるか」に広げました",
   "【2026-11-15 品質保証部の指摘を受けた書き直し】変えた点: ①「購入に国籍・在留の制限はない」の断定をやめ、「2026年11月時点で禁止はないが、手続きは増えた（2026年4月から非居住者は外為法の報告、10月5日から登記で国籍の届出）。重要な区域の土地の許可制の法案が10月23日に国会に出ている」の形にし、専門家（弁護士・司法書士）に確かめるよう添えました（財務省・法務省・内閣府・内閣官房の出典） ②デジタルノマドを、出入国在留管理庁の条件どおりに直しました（対象はビザ免除かつ租税条約のある国・地域の人、年収1,000万円以上、治療費1,000万円以上の民間医療保険、日本の会社には雇われない、6か月で更新不可、出国から6か月たてば再び可）。時点は2026年11月 ③滞在の手段（観光の短期滞在・デジタルノマド）を表にしました ④空き家の数の出典を、総務省統計局の確報（2024年9月公表）1つにしました（900万戸・13.8%・過去最高、使い道のない空き家 約386万戸・2018年から36.9万戸増） ⑤「1か月泊まれる場所」の節を新しく書き、自治体のお試し住宅（自治体ごと、条件は町の外に住民登録があって移住を考えている人など。例は静岡市オクシズの3泊〜2週間・1組1日300円）、マンスリー、宿を表で並べました。NODE Shimoda はその中の1つとして紹介しています ⑥創業メンバーが下田で借りた古い家を宿に改修したときの体験を2点入れました（古い2芯の配線でエアコン・冷蔵庫・電子レンジを同時に使えなかった／繁忙期で回線工事に2か月以上かかり、置き型のルーターでしのいだ）。「買った」とは書かず「持ち主から借りた」と明記しています ⑦ゲストを「リモートで働く人がたくさん」→「リモートで働きに来る人もいる」に ⑧前の最後の節の「いちばんの近道」という押しの強い言い方をやめ、最後は1か月の過ごし方の節にしました。4週目も「決める」→「振り返る」に ⑨FAQ に「外国人は買えるか」「お試し住宅は外国人も使えるか」を足して5問にしました",
   "【以前の確認事項（2026-11-16 の手離れで解決・または書かないことにした）】⓪(a) 土地の法案が成立したか、いつ公布・施行か（黄色い枠。審議入りの報道は政党の機関紙でしか確認できず、記事には「国会にかかっている」とだけ書いています） (b)「外国人が家を買うことは禁止されていない」の出典の1つ rej（Real Estate Japan）は民間の不動産サイトです。もう1つは財務省の FAQ ですが、在留資格と不動産の関係は公的な出典が見つからず、行政書士か入管で確かめてほしい点として黄色い枠を置きました (c) NODE Shimoda を英語で「older house」（古い家）と呼んでよいか（experience.md では「旧町内の空き家を改修した」とあり、築年数は未確認） (d)「お試しの1か月」の節の「私たちならこう過ごす」は私たちの見方として書いています。言い方に違和感がないか ①法務・在留の記述（不動産購入の手続き、法案の審議状況、デジタルノマドの条件、90日と例外の国）は、公開の直前に一次のページを開いて確かめてください（黄色い枠4か所） ②創業メンバーの体験（配線・回線）の書き方が、事実と合っているか。「私たち（we）」の体験として書いています ③伊豆の市町（下田市・南伊豆町・伊豆市）に1か月以上泊まれるお試し住宅があるか、料金、外国籍・海外在住の人が使えるか（黄色い枠） ④月額料金、30泊以上を常に受けられるか、「再生した空き家」と呼んでよいか（黄色い枠） ⑤法務・在留の出典はリサーチ部が検索で確認したもので、本文のページは開けていません ⑥「下田まで直通の電車で3時間かからない」の出典の JR東日本の踊り子のページ（東京〜伊豆急下田 2時間49分）は、この環境から開けず検索でしか確かめていません。公開前にページを開いて確かめてください（ほかの記事は駅探の約2時間35分を使っているので、数字は出していません） ⑦南アルプス市・静岡市のお試し住宅の条件と料金（2026年11月15日にリサーチ部がページを開いて確認）が、公開の時点でも変わっていないか ⑧京丹後市を外したことでよいか（市営のお試し住宅は2026年9月末で閉鎖。民間・地域のお試し住宅は案内されていますが、例には使っていません）",
   "【入れられなかったこと】外為法の不動産取得の報告の細かい範囲（財務省の制度の概要のページを本文で確認できていないため）、在留資格と不動産の所有の関係を書いた公的な出典、海外に住む人が南アルプス市などのお試し住宅の対象に入るか（ページに記載がなく、町に聞くように書きました）、伊豆の市町のお試し住宅の有無、新耐震基準（1981年）など建物の点検の項目（公的な出典を未確認）、マンスリーの部屋の相場（出典なし）。焼津・修善寺の家は、状況が決まるまで書いていません",
  ],
  "points": [
    "2026年4月からは、日本に住んでいない人が家を買ったら、財務省への報告が要ります。",
    "1か月暮らすと、車が要るか、近所の人のこと、冷暖房に実際いくらかかるかが分かります。",
    "海外から来るなら、自治体のお試し住宅より、マンスリーの部屋か月割のある宿のほうが、たいてい現実的です。",
  ],
  "body": """
<p>akiya（空き家）は、ひとことで言えば、誰も住んでいない家のことです。2023年の住宅・土地統計調査では、2023年10月1日時点で900万戸、日本の住宅の13.8%が空き家で、割合は過去最高でした[[s:stat_housing2023]]。そのうち約386万戸は、貸すためでも売るためでもなく、別荘でもない家で、2018年から36万9千戸増えました[[s:stat_housing2023]]。私たちの感覚では、「日本の放置された家」と言うとき、たいていはこの家のことを指しています。</p>

<h2>外国人は空き家を買えるのか</h2>
<p>買えます。日本に住んでいない人も買うことができ、何をすればいいかは財務省の決まりに書かれています。2026年4月から、日本に住んでいない人が日本の不動産を買うと、住むための家でも、外為法にもとづいて財務省に報告することになりました[[s:mof_fefta2026,mof_realprop_faq]]。外国からの買い手向けの不動産サイト Real Estate Japan も、買うのに日本に住んでいる必要はないと書いています[[s:rej]]。2026年10月5日からは、日本人も含めて、買った人はみな登記のときに国籍を届け出ます[[s:moj_nationality]]。</p>
<p>決まりは、まだ動いています。国会に出ている法案は、一部の防衛関係施設と海上保安庁の施設の周り（おおむね1km）と、無人の国境離島に、新しい区域をつくる内容です[[s:cao_land_bill,cao_land_bill_outline]]。その区域で土地の所有権を移すときは、すべて事前に国の許可が要り、法律は公布から1年6か月以内に施行されます[[s:cao_land_bill_outline]]。2026年11月中旬の時点で、法案はまだ衆議院で審議中で、法律にはなっていません[[s:shugiin_bill18]]。</p>
<p>家とビザは、別々の問題として考えたほうがいいと私たちは思います。家を持つことで日本に長くいられるようになると期待しているなら、あてにする前に、在留資格（ビザ）の手続きを扱う行政書士に聞いてみてください。決まりがこれだけ速く変わっているので、契約の前に、自分の場合を弁護士や司法書士に見てもらうのが賢明だと思います。</p>

<h2>なぜ、買う前にその町で暮らすのか</h2>
<p>家を買うこと自体は、簡単なほうです。本当に引き受けるのは町のほうで、物件情報から分かるのは、価格と間取りと何枚かの写真くらい。そこで楽しく暮らせるかを決めることは、しばらく住んでみて初めて見えてきます。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>知りたいこと</th><th>1か月暮らすと、こう分かる</th></tr></thead>
<tbody>
<tr><td>古い木造の家が1月にどれくらい寒いか、暖房にいくらかかるか</td><td>最初の寒い夜に体で分かり、電気代の請求で数字でも分かります。</td></tr>
<tr><td>車なしで毎日の暮らしが回るか</td><td>1週間、買い物や用事を徒歩・バス・自転車で済ませてみると、はっきりします。家のすぐ近くでは済まない用事も、あわせて試してみてください。</td></tr>
<tr><td>どこで食料を買うか、店は何時に閉まるか</td><td>食事をほとんど自炊していると、手に入りやすいものとそうでないものが、すぐに分かります。</td></tr>
<tr><td>その通りのごみの分別の仕組み</td><td>地域の収集カレンダーに合わせて、みんなと同じように出すことになります。英語版があれば、役所でもらっておくと便利です。</td></tr>
<tr><td>一日仕事をしても回線がもつか</td><td>ビデオ会議も含めて、いつもどおりに働いてみるのが一番の確かめ方です。</td></tr>
<tr><td>湿気の多い時期や台風で、建物がどうなるか</td><td>同じような家でどこから傷みやすいかは、近所の人や地元の工務店がよく知っています。</td></tr>
<tr><td>新しく来た人を、近所がどう迎えるか</td><td>あいさつをしたり、清掃の日があれば参加したり、先に移ってきた人にどうなじんだかを聞いたりすると、よく分かります。近所の人は小さなことにも気づきます。下田で回線の工事をしたとき、工事の車をどこに停めたかについて、近所の方から声をかけられました。</td></tr>
</tbody></table></div>
<p>どれも、内見では出てこないことばかりです。</p>

<h2>古い家で、住んでみて初めて分かることは何か</h2>
<p>私たちの経験では、配線と回線です。創業メンバーの1人が、下田の古い部屋を持ち主から借りて、宿に改修したときに知りました。買ったのではなく借りた部屋ですが、買った人も同じことにぶつかると私たちは思います。</p>
<p>古い2芯の配線では、エアコンと冷蔵庫と電子レンジを同時に使えず、ゲストに同時に使わないようお願いすることになりました。配線をやり直すにはそれなりの費用がかかるので、予算を組む前に知っておきたいことです。インターネットの回線工事は、繁忙期だったこともあって申し込みから2か月以上かかり、それまでは置き型のホームルーターでしのぎました。</p>
<p>配線と回線工事の待ちは、もっと大きな話の小さな例です。安い古い家では、売り出し価格は、かかるお金の一部にすぎません。改修、税金、保険、維持費が上乗せされ、建物ごとに大きく変わるので、本当の金額は書面の見積もりを取って初めて分かります。</p>

<h2>町で1か月を試すには、どの在留資格が合うか</h2>
<p>多くの人は、就労や居住のビザなしで、しっかり試せるくらいの期間いられます。方法はおもに2つで、下の条件は2026年11月時点のものです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>滞在のしかた</th><th>期間</th><th>対象</th></tr></thead>
<tbody>
<tr><td><strong>短期滞在</strong>（ビザ免除）</td><td>ビザ免除の国・地域の多くは90日まで。15日・30日・180日の国もあります[[s:jnto_visa]]。</td><td>ビザ免除の国・地域の人。この滞在では報酬を得る仕事はできません。大事なのは、自分のパスポートの条件です[[s:jnto_visa]]。</td></tr>
<tr><td><strong>デジタルノマド</strong>の在留資格</td><td>6か月で、更新はできません。出国後6か月たてば、もう一度申請できます[[s:isa_nomad_en]]。</td><td>ビザ免除で、かつ日本と租税条約のある国・地域の人[[s:isa_nomad_list]]。年収1,000万円以上と、治療費1,000万円以上を補償する民間の医療保険が必要で、日本の会社に雇われて働くことはできません[[s:isa_nomad_en]]。</td></tr>
</tbody></table></div>
<p>デジタルノマドの在留資格が合いそうなら、[[l:ja-digital-nomad|日本のデジタルノマドビザの記事]]に、対象になる人と仕組みをくわしくまとめています。</p>
<p>延長、もっと長い在留資格、いったん出国してまた来る場合のことは、[[l:ja-how-long-stay|日本に何日いられるかのガイド]]にまとめました。</p>
<p class="fine">これは一般的な情報で、在留手続きの助言ではありません。デジタルノマドの対象の国は変わるので、自分のパスポートで確かめてください。</p>

<h2>町を試すために1か月泊まれる場所はどこか</h2>
<p>おもな選択肢は、自治体のお試し住宅、マンスリーの部屋、月割のある宿の3つです。どれが合うかは、町と、どこから来るかによります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>選択肢</th><th>期間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>自治体のお試し住宅</strong></td><td>町によって、1〜2日から数か月まで。2年近く住める市もあります[[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>決まりは町ごとで、多くは移住するつもりの人向け。南アルプス市は1〜3か月、月21,000円で貸しています（2026年2月）[[s:minamialps_trial]]。</td></tr>
<tr><td><strong>マンスリーの部屋</strong></td><td>1か月以上</td><td>家具付きの部屋を月単位で借ります。小さな町では選べる数が少ないこともあるので、早めに探すと安心です。</td></tr>
<tr><td><strong>月割のある宿・貸別荘</strong></td><td>1週間〜1か月以上</td><td>海外からいちばん予約しやすいことが多く、何も契約せずにその町での暮らしを試せます。</td></tr>
</tbody></table></div>
<p>お試し住宅はよさそうに見えますが、落とし穴があります。移住する人のための仕組みで、海外から町を試しに来る人向けではないのです。南アルプス市のお試し住宅は、山梨県の外に住民登録があり、市に移住するつもりで、移住の相談に登録した人が対象です[[s:minamialps_trial]]。国籍は条件に挙げられていないので、海外に住んでいるなら、対象に入るかは市の移住の窓口に聞けば分かります。</p>
<p>はっきり書いている市もあります。静岡市の「長期お試し住宅」は、市営住宅に半年以上2年未満住めるものですが、静岡県の外に住んでいて、市への移住を決めた、または準備している人が対象です。外国籍の人は、永住者・定住者・特別永住者・日本人の配偶者等（日本人の配偶者や子）の在留資格がある場合に限られます（2026年8月更新のページ）[[s:shizuoka_long_trial]]。つまり、観光やデジタルノマドの滞在では使えません。私たちの考えでは、海外から来るなら、マンスリーの部屋か宿のほうが現実的です。マンスリーの仕組みは、[[l:ja-monthly-rental|日本のマンスリーの部屋の記事]]にくわしく書いています。どうしてもお試し住宅を使いたいなら、まず町の移住の窓口に連絡してみてください。</p>
<p>下田市は別の形をとっています。2026年4月施行の要綱で、移住を考えている人が市の指定する宿に泊まると、10泊までなら宿泊料の半分（1泊4,000円まで）を補助しています[[s:shimoda_stay_subsidy]]。ただし静岡県の外で日本に住民登録がある人が対象なので、海外から来る場合は使えません[[s:shimoda_stay_subsidy]]。</p>
<p>東京から行きやすい町のほうが試しやすいです。2026年11月時点で、東京駅から毎日走る直通の電車なら、[[l:ja-izu|伊豆半島]]の下田まで2時間29〜44分です[[s:jre_tt_tokyo]]。くわしくは[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田が候補に入っているなら、私たちが下田で営んでいる小さな宿「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」を、町の様子をつかむあいだの拠点にしてもらえます。旧町内のアパートの一室（約40㎡）を改装したもので、伊豆急下田駅から歩いて8分です[[s:node_room,node_access]]。公式サイトでは中長期の滞在にも便利な宿として紹介していて[[s:node_site]]、旅館業法の許可を受けています。これまでのゲストは欧米の人が中心で、リモートで働きに来る人もいます。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|下田の旧町内にある私たちの部屋「NODE Shimoda」のリビング。]]

<h2>お試しの1か月は、どんなふうに過ぎるか</h2>
<p>ほとんどは、ふだんの暮らしそのものです。そこに、いくつか意識して試すことを入れます。下田で私たちがつまずいたことをもとに、週ごとにおおよそこう組み立てると思います。</p>
<p>最初の1週間は、落ち着くための時間です。スーパー、診療所、バス停、ごみの収集日を覚えます。古い建物に泊まっているなら、泊まり先の人に、電気の契約のアンペア数とブレーカーの場所を聞いておきましょう。下田の私たちの部屋の古い配線では、エアコンと冷蔵庫と電子レンジを同時に使えませんでした。アンペア数が分かれば、一度にどれくらい使えるかの見当がつきます。ブレーカーの場所を知っていれば、落ちてもすぐに戻せます。</p>
<p>2週目には、いつもの時間に働き、家で料理をするようになります。ビデオ会議の続く一日に回線がもつか、冷暖房に実際いくらかかるかが分かるのはこの頃です。地元の回線業者に、そこで新しく回線を引くとどれくらいかかるかを聞いておくのもいい時期です。私たちのときは2か月以上かかりました。</p>
<p>3週目は、聞いてまわる週です。役所の空き家の窓口に行ったり、地元の不動産屋と話したり、工務店に古い家の配線のやり直しがおおよそいくらかを聞いたりできます。湿気の多い夏や台風で家がどうなるかは、近所の人がいちばんよく知っています。</p>
<p>4週目には、家について、そして自分の暮らし方について、何を変える必要がありそうか、だいたい見えています。費用や迷いを忘れないうちに書きとめておくと、町どうしを比べるときにも、見送ると決めるときにも、ずっと楽になります。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
    ("外国人は日本の不動産を買えますか",
     "買えます。日本に住んでいない人も買うことができ、2026年4月からは、外為法にもとづいて財務省に報告することになりました。買った人はみな、登記のときに国籍も届け出ます[[s:mof_fefta2026,moj_nationality]]。決まりが変わりつつあるので、自分の場合は弁護士や司法書士に見てもらえます。"),
    ("日本で家を持つと、ビザを取りやすくなりますか",
     "あてにしないほうがいいと私たちは思います。家とビザは別々の問題として考えているので、長く住むことも計画に入っているなら、買う前に、在留資格（ビザ）の手続きを扱う行政書士に聞いてみてください。"),
    ("日本の安い家は、本当に安いのですか",
     "そうとは限りません。購入価格は、かかるお金の一部です。改修、税金、保険、維持費が上乗せされ、金額は建物によって大きく変わるので、決める前に知るには、書面の見積もりを取るしかありません。"),
    ("外国人でも、自治体のお試し住宅を使えますか",
     "町しだいです。お試し住宅は、多くが移住するつもりの人向けで、対象をはっきり書いている町もあります。たとえば静岡市の長期お試し住宅は、2026年8月時点で、外国籍の人なら、永住者・定住者・特別永住者の在留資格か、日本人の配偶者や子である場合に限られていました[[s:shizuoka_long_trial]]。いまの決まりは、町の移住の窓口が知っています。"),
    ("日本に空き家は何戸ありますか",
     "2023年の住宅・土地統計調査によると、2023年10月1日時点で約900万戸、住宅全体の13.8%が空き家でした[[s:stat_housing2023]]。"),
  ],
 },
}
