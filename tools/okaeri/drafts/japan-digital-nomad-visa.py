# -*- coding: utf-8 -*-
"""digital-nomad の新規記事（2026-11-16 執筆部）。構成案とリサーチメモ: tools/okaeri/briefs/japan-digital-nomad-visa.md。
制度の事実は、編集長が 2026-11-16 に出入国在留管理庁のページで確かめた内容（launch-open-items.md）と、開いて確かめた出典（JNTO・e-Gov の条文・総務省・国交省・国税庁）だけを使う。
content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    "jnto_nomad": ("https://www.japan.travel/en/plan/digital-nomad-visa/", "JNTO", "日本政府観光局（デジタルノマドビザ）",
                   "JNTO: Digital Nomad Visa (checked November 2026)"),
    "jnto_visa": ("https://www.japan.travel/en/plan/visa-info/visa-immigration/", "JNTO", "日本政府観光局（入国とビザ）",
                  "JNTO: Entry into Japan and visa information (checked November 2026)"),
    "egov_immig_act": ("https://laws.e-gov.go.jp/law/326CO0000000319", "Immigration Control Act", "出入国管理及び難民認定法（e-Gov法令検索）",
                       "Immigration Control and Refugee Recognition Act, Articles 19-3 and 20 (e-Gov, version in force 1 October 2026)"),
    "egov_immig_rules": ("https://laws.e-gov.go.jp/law/356M50000010054", "Immigration Control Act ordinance", "出入国管理及び難民認定法施行規則（e-Gov法令検索）",
                         "Ordinance for Enforcement of the Immigration Control and Refugee Recognition Act, Article 19-5 (e-Gov, version in force 1 October 2026)"),
    "soumu_juki": ("https://www.soumu.go.jp/main_sosiki/jichi_gyousei/c-gyousei/zairyu/english/index.html", "Ministry of Internal Affairs and Communications",
                   "総務省（外国人住民の住民基本台帳制度）", "Ministry of Internal Affairs and Communications: Basic Resident Registration System for foreign residents"),
    "egov_nhi_rules": ("https://laws.e-gov.go.jp/law/333M50000100053", "National Health Insurance Act ordinance", "国民健康保険法施行規則（e-Gov法令検索）",
                       "Ordinance for Enforcement of the National Health Insurance Act, Article 1 (e-Gov, version in force 1 October 2026)"),
    "mlit_foreign_rental": ("https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000017.html", "Ministry of Land, Infrastructure, Transport and Tourism",
                            "国土交通省（外国人の民間賃貸住宅入居円滑化ガイドライン）",
                            "MLIT: Guideline for Facilitating Looking for and Moving in Rental Housing for Foreign Nationals"),
    "nta_2875": ("https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2875.htm", "National Tax Agency", "国税庁（タックスアンサー No.2875）",
                 "National Tax Agency: Tax Answer No.2875, residents and non-residents (law as of 1 April 2026)"),
    "nta_nonresident": ("https://www.nta.go.jp/english/taxes/individual/12006.htm", "National Tax Agency", "国税庁（非居住者の課税）",
                        "National Tax Agency: No.12006 Tax on the income of a non-resident"),
    "soumu_ftth_2025": ("https://www.soumu.go.jp/main_content/001088979.xlsx", "MIC, 2025", "総務省（令和6年度末 FTTH世帯カバー率）",
                        "Ministry of Internal Affairs and Communications: Fibre household coverage by prefecture and municipality, end of March 2025"),
    "jnto_medical": ("https://www.jnto.go.jp/emergency/eng/mi_guide.html", "JNTO", "日本政府観光局（医療機関の検索）",
                     "JNTO: Guide for when you are feeling ill (medical institution search)"),
}

ARTICLE = {
 "id": "digital-nomad", "slug": "japan-digital-nomad-visa", "topic": "live", "place": None, "also": [],
 "photo": ("laptop-plants-desk", "A laptop open on a wooden desk among potted plants, with a notebook and pen", ""),
 "published": "2026-11-16", "updated": "2026-11-16",
 "kicker": "Live part-time",
 "h1": "Japan’s digital nomad visa, and where to base yourself",
 "seo_title": "Japan Digital Nomad Visa: Who Qualifies and Where to Live",
 "description": "Japan’s digital nomad visa gives remote workers earning ¥10 million a year up to six months, with no extension or residence card, so where you live matters.",
 "dek": "Japan’s digital nomad status gives eligible remote workers up to six months. You’ll need ¥10 million a year in income, and it doesn’t come with a residence card.",
 "card": "Six months, no extension, ¥10 million a year in income and ¥10 million of medical cover. With no residence card, the real question is where you’ll live and work for those six months, and Tokyo isn’t the only sensible answer.",
 "keywords": [("japan digital nomad visa", "880", "2"), ("digital nomad visa japan", "720", "—")],
 "intent": "Know（条件・期間・家族・申請）→ Do（6か月をどこで暮らすか）",
 "points": [
   "You get up to six months with no extension, and you can apply again after six months away.",
   "You need ¥10 million a year in income, ¥10 million of medical cover and a passport from a listed country.",
   "There’s no residence card, so we think a furnished monthly place beats an ordinary lease.",
 ],
 "body": """
<p>Blogs disagree about almost everything on this visa: whether you can renew it, whether your family can come, whether you get a residence card. The rules themselves are short, and they sit on one page from Japan’s Immigration Services Agency [[s:isa_nomad_en]]. Once you’ve checked them, the bigger question is where you’ll spend six months without a residence card.</p>

<h2>What is Japan’s digital nomad visa?</h2>
<p>It’s a stay of up to six months for people who work online for someone outside Japan. Its official name is Designated Activities (Digital Nomad), and there’s a family version called Designated Activities (Spouse or Child of Digital Nomad) [[s:jnto_nomad]].</p>
<p>The rules cover two kinds of work done online from Japan. One is working under an employment contract with a foreign organisation, on its business abroad. The other is providing paid services, or selling goods, to people outside Japan [[s:isa_nomad_en,egov_immig_rules]]. So freelancers with clients abroad fit, not only employees.</p>
<p>What it isn’t is a way into a job in Japan. The agency’s page says you can’t work on this status under an employment contract with a Japanese public or private organisation [[s:isa_nomad_en]]. If that’s what you’re after, you’re looking at a different status.</p>

<h2>Who qualifies?</h2>
<p>You need three things: a passport from a listed country, a high income and private medical insurance. Here’s how the Immigration Services Agency set them out as of November 2026 [[s:isa_nomad_en]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Condition</th><th>What it means</th></tr></thead>
<tbody>
<tr><td>Nationality</td><td>A passport from a country or region on the agency’s list. The list is built from places that have both a visa exemption and a tax treaty with Japan [[s:isa_nomad_en,isa_nomad_list]].</td></tr>
<tr><td>Income</td><td>¥10 million or more a year, counted as the applicant’s own income [[s:isa_nomad_en,jnto_nomad]].</td></tr>
<tr><td>Insurance</td><td>Private insurance covering death, injury and illness during your stay, with at least ¥10 million of cover for medical treatment [[s:isa_nomad_en]].</td></tr>
<tr><td>Your work</td><td>Online work from Japan for a foreign organisation that employs you, or paid work for clients and customers outside Japan. Work under an employment contract with a Japanese organisation isn’t allowed [[s:isa_nomad_en,egov_immig_rules]].</td></tr>
</tbody></table></div>
<p>The list is a PDF, and it’s the only place to check your own passport [[s:isa_nomad_list]]. Counts on other sites go out of date, so the current version is the one to trust. The income test is about the applicant, so it’s safer not to count on adding a partner’s earnings.</p>

<h2>How long can you stay, and can you renew it?</h2>
<p>Six months at most, and it can’t be extended [[s:isa_nomad_en,jnto_nomad]]. You can come back on the same status once six months have passed since you left Japan [[s:isa_nomad_en]]. So the rhythm is six months in Japan, then six months somewhere else.</p>
<p>Some sites still say you get one extension. The agency’s own page says you don’t, and that’s the version to plan around. Here’s how it compares with an ordinary visa-free visit.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>Short-term visitor (visa-exempt)</th><th>Digital nomad</th></tr></thead>
<tbody>
<tr><td>How long</td><td>Usually up to 90 days, though some nationalities get 15, 30 or 180 days [[s:jnto_visa]]</td><td>Up to six months, no extension [[s:isa_nomad_en]]</td></tr>
<tr><td>Work</td><td>No paid work [[s:jnto_visa]]</td><td>Online work for a foreign employer or paid work for clients abroad, but not for a Japanese employer [[s:isa_nomad_en]]</td></tr>
<tr><td>Residence card</td><td>No [[s:egov_immig_act]]</td><td>No [[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>

<h2>Can your partner and children come too?</h2>
<p>Yes. A spouse or child you support can come on the family version of the status, which covers their everyday life as your dependants [[s:isa_nomad_en,jnto_nomad]]. Like you, they won’t get a residence card [[s:egov_immig_rules]].</p>
<p>Their conditions are a little different from yours. Family members need a passport from a visa-exempt country or region, and the tax treaty test applies only to you [[s:isa_nomad_en]]. Each of them also needs the same insurance as you: cover for death, injury and illness during the stay, with at least ¥10 million for medical treatment [[s:isa_nomad_en]]. The status is written for a spouse or a child, so if you and your partner aren’t married, it’s worth asking the agency before you plan around it.</p>

<h2>How do you apply?</h2>
<p>Two official pages cover it. Visas are issued by the Ministry of Foreign Affairs, and JNTO points you to its page for the documents you’ll need [[s:jnto_nomad]]. The Immigration Services Agency’s page also explains how to apply for a Certificate of Eligibility if you want to enter Japan on this status for the first time [[s:isa_nomad_en]].</p>
<ol>
<li>Find your passport’s country or region on the agency’s list [[s:isa_nomad_list]].</li>
<li>Gather proof of your income and an insurance policy that meets the conditions [[s:isa_nomad_en]].</li>
<li>Read the Ministry of Foreign Affairs page that JNTO links to for the current visa documents [[s:jnto_nomad]].</li>
<li>Read the agency’s guidance on the Certificate of Eligibility for a first entry on this status [[s:isa_nomad_en]].</li>
<li>Plan your exit date, since the stay ends at six months [[s:isa_nomad_en]].</li>
</ol>
<p>For anything those pages don’t answer, the Ministry of Foreign Affairs or the agency is the place to ask. Switching inside Japan is harder than many people hope. The Immigration Control Act only lets a short-term visitor change status in Japan when there are “unavoidable special circumstances” [[s:egov_immig_act]]. So it makes sense to sort out the status before you fly, rather than arrive as a tourist and try to switch.</p>

<h2>What doesn’t the visa give you?</h2>
<p>A residence card, and quite a lot follows from that. Japan’s immigration law doesn’t treat digital nomads and their families as mid- to long-term residents, so no card is issued [[s:egov_immig_act,egov_immig_rules]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>With a residence card</th><th>On the digital nomad status</th></tr></thead>
<tbody>
<tr><td>Resident register (<em>juminhyo</em>)</td><td>Foreign residents with a card are registered where they live [[s:soumu_juki]]</td><td>You won’t be on it</td></tr>
<tr><td>National Health Insurance</td><td>Open to registered foreign residents [[s:egov_nhi_rules]]</td><td>You can’t join it [[s:egov_nhi_rules]]. Separately, the status requires private insurance [[s:isa_nomad_en]]</td></tr>
<tr><td>An ordinary lease</td><td>The government’s guideline for landlords gives the card as one example of ID [[s:mlit_foreign_rental]]</td><td>Harder, in our view. A furnished monthly place is usually simpler</td></tr>
</tbody></table></div>
<p>Renting is where you’ll feel it most. The government’s guideline for landlords lists a passport and a residence card as examples of ID, and leaves what to ask for to the landlord and tenant [[s:mlit_foreign_rental]]. It also says landlords should ask whether you have a Japanese bank account and a phone that works in Japan [[s:mlit_foreign_rental]]. Without a card or a local account, we think a furnished place rented by the month is the easier route.</p>
<p>Tax is the other thing people get wrong. For Japanese income tax, you’re a resident if you have a domicile here, or have lived here continuously for a year or more [[s:nta_2875]]. Non-residents are taxed only on Japan-source income, and pay for work done in Japan counts as Japan-source income [[s:nta_nonresident]]. Tax treaties can change that [[s:nta_2875]], so “six months means no tax” is too simple. A tax adviser who knows your home country’s treaty with Japan is the person to ask.</p>
<p>Everything here describes the rules as of November 2026. For your own case, the Ministry of Foreign Affairs, the Immigration Services Agency or an administrative scrivener (<em>gyoseishoshi</em>) who handles visas is the place to check.</p>

<h2>Where should you base yourself for six months?</h2>
<p>We think five things matter most: an internet connection you can trust through your working hours, trains to Tokyo and an airport, a furnished place you can rent by the month, a clinic you can use, and the season. Tokyo wins on some of these, but not all, and here’s how we see the trade-offs.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>Tokyo</th><th>A regional city</th><th>A small town 2–3 hours from Tokyo</th></tr></thead>
<tbody>
<tr><td>Furnished monthly places</td><td>The most choice</td><td>Some choice</td><td>Few, so you book further ahead</td></tr>
<tr><td>Getting to an airport</td><td>Easy</td><td>Usually easy</td><td>A longer trip, so it takes planning</td></tr>
<tr><td>Daily life in English</td><td>Easiest</td><td>Patchier</td><td>Patchy, and a translation app helps</td></tr>
<tr><td>What you trade</td><td>Space and quiet</td><td>A little of everything</td><td>Choice and convenience, for space, quiet and a slower week</td></tr>
</tbody></table></div>
<p>Fibre is less of a worry than people expect: by the end of March 2025, an estimated 96.3% of households in Tokyo could get it, and about 93.8% in Shimoda [[s:soumu_ftth_2025]]. That figure is about whether a line reaches the building, not its speed, and installing one can take time. When we opened our place in Shimoda, broadband took more than two months in the busy season, so we got by on a plug-in home router. A place that already has a working line saves you that wait.</p>
<p>JNTO has an English search for medical institutions by prefecture, language and department, and suggests checking each one before you go [[s:jnto_medical]]. It’s easier to find your nearest clinic on day one than on the day you need it.</p>
<p>Shimoda, on the [[l:izu|Izu Peninsula]], is one example of a small town in reach. As of November 2026, the direct trains from Tokyo Station take 2 hours 29 to 44 minutes [[s:jre_tt_tokyo]], and our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] has the routes. Our own place there, NODE Shimoda, is an apartment of about 40 m² eight minutes’ walk from Izukyu-Shimoda Station, with a work desk, Wi-Fi, a kitchen, a washing machine and a gas dryer [[s:node_site,node_room]]. We set it up with long-staying remote workers in mind, so if you’re planning something longer, just ask us. If a season goes well and you start looking at houses, read our piece on [[l:akiya-try-first|living in a town before you buy an akiya]].</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal, immigration or tax advice.</p>',
 "faq": [
   ("How long is Japan’s digital nomad visa?",
    "Up to six months. As of November 2026, the Immigration Services Agency says the stay can’t be extended [[s:isa_nomad_en]]."),
   ("Can I extend Japan’s digital nomad visa?",
    "No. You can come back on the same status once six months have passed since you left Japan [[s:isa_nomad_en]], so the pattern is six months in, six months away."),
   ("Do I get a residence card on the digital nomad visa?",
    "No. Digital nomads and their families aren’t treated as mid- to long-term residents, so no card is issued [[s:egov_immig_act,egov_immig_rules]]. That also means you won’t be on the resident register or in National Health Insurance [[s:soumu_juki,egov_nhi_rules]]."),
   ("Can I bring my family on Japan’s digital nomad visa?",
    "A spouse or child you support can come on the family version of the status [[s:jnto_nomad,isa_nomad_en]]. They need a passport from a visa-exempt country or region and the same insurance as you [[s:isa_nomad_en]]. If you aren’t married, ask the agency first."),
   ("Can I work for a Japanese company on it?",
    "No. The Immigration Services Agency says you can’t work on this status under an employment contract with a Japanese public or private organisation [[s:isa_nomad_en]]. It covers online work for a foreign organisation that employs you, or paid work for clients outside Japan."),
 ],
 "sources": ["isa_nomad_en", "isa_nomad_list", "jnto_nomad", "jnto_visa", "egov_immig_act", "egov_immig_rules", "soumu_juki", "egov_nhi_rules",
             "mlit_foreign_rental", "nta_2875", "nta_nonresident", "soumu_ftth_2025", "jnto_medical", "jre_tt_tokyo", "node_site", "node_room"],
 "related": ["izu-from-tokyo", "akiya-try-first"],
 "ja": {
  "h1": "日本のデジタルノマドビザと、どこを拠点にするか",
  "dek": "日本のデジタルノマドの在留資格では、条件を満たすリモートワーカーが最長6か月滞在できます。年収1,000万円以上が必要で、在留カードは出ません。",
  "review": [
   "【2026-11-16 品質保証部の採点（89点・ゲート違反2）を受けた書き直し】変えた点: ①【事実の変更】申請: 「大使館・総領事館で申請する」（本文と手順の2か所）をやめ、「ビザは外務省が出し、必要な書類は外務省のページにある（JNTO）」と「入管庁のページに、この在留資格で新しく入国する人の在留資格認定証明書の交付申請の案内がある」だけで書きました。手数料・期間・どちらを先にするかは書いていません。手順の番号つきリストもこれに合わせました。②「私たちの経験では、6か月暮らしたい人は小さな町のほうがうまくいく」を消しました（確認済みの体験にないため）。比較表の前の文を「私たちの見方をまとめると」にして、表が見解だと分かるようにしています。③国民健康保険: 「入れない。だから民間の保険が条件」の理由づけをやめ、「入れない」と「それとは別に、民間の保険が条件」を並べました。④【言い切りに変更】仕事の範囲: 入管庁のページの原文（外国の組織との雇用契約で外国の業務をする／外国にいる人に有償で役務・物品を提供する、日本の公私の機関との雇用契約などにもとづいて働くことはできない）を出典に、「フリーランスも当てはまる」「日本の会社では働けない」を本文・表・FAQ で言い切りました。⑤【事実の追加】家族: 本人に扶養される配偶者・子として日常の活動をする資格であること、家族の国籍の条件は査証免除の国・地域（租税条約の条件は本人だけ）、家族の保険の条件は本人と同じ、を足しました。家族が働けるかは書いていません。⑥【事実の追加】保険の条件に「滞在中の死亡・けが・病気を補償」を足しました。⑦“we’d”（私たちなら）を減らし、description の末尾を文にしました。⑧光回線の段落を4文にし（静岡県の96.7%は外しました）、最後の節の表のあとの段落を5つから3つにしました（空き家の記事への案内は下田の段落にまとめました）。",
   "【2026-11-16 新規（執筆部）】書いた点: 条件・期間・延長・再申請・在留カード・家族は、編集長が 2026-11-16 に出入国在留管理庁のページで確かめた内容と JNTO の英語のページだけで書き、すべて「2026年11月時点」と書いています。在留カードが出ないこと、日本の中での在留資格の変更（やむを得ない特別の事情があるときだけ）は e-Gov の条文で裏付けました。在留カードがないことの影響（住民登録・国民健康保険・普通の賃貸）は総務省・国保法施行規則・国交省のガイドラインで書き、賃貸は「借りられない」とは書かず見解にしています。税は国税庁の居住者・非居住者の定義と国内源泉所得までで、自分の場合は税理士に、で止めました。拠点選びは、光回線の世帯カバー率（総務省、2025年3月末の推計）、JNTO の医療機関の検索、東京駅から下田の直通の所要時間（JR東日本の時刻表、2026年11月）、確認済みの体験（開業時に Wi-Fi の工事に2か月以上かかり、ホームルーターでしのいだ）で書きました。NODE Shimoda に触れるのは最後の節の1回で、公式サイトの事実だけです（30泊以上・6か月の受け入れ、料金、回線の実測値は書いていません）。",
   "【写真】編集長が入れた laptop-plants-desk（観葉植物のある木の机に開いたノートPC）をそのまま使っています。",
   "【書かなかったこと（確かめられなかったため）】制度が始まった日、対象の国・地域の数と、米英などが入っているか（一覧の PDF で確かめるよう案内しています）、家族が働けるか、手数料・審査の期間・ビザと在留資格認定証明書のどちらを先にするか、必要書類の細目、発給件数、在留カードなしで携帯・銀行口座を作れるか。月単位の部屋の記事（monthly-rental）はまだないので、内部リンクは伊豆・伊豆への行き方・空き家の記事に送っています。",
  ],
  "points": [
    "滞在は最長6か月で延長はできず、日本を出て6か月たてば、また申請できます。",
    "年収1,000万円以上、治療費1,000万円以上の医療保険、対象の国・地域のパスポートが要ります。",
    "在留カードが出ないので、普通の賃貸より家具付きの月単位の部屋のほうがいい、と私たちは考えています。",
  ],
  "body": """
<p>このビザについては、ブログによって言うことがほとんどばらばらです。更新できるのか、家族は来られるのか、在留カードはもらえるのか。でも決まりそのものは短く、出入国在留管理庁の1つのページにまとまっています[[s:isa_nomad_en]]。それを確かめたら、もっと大きな問題は、在留カードのない6か月をどこで過ごすかです。</p>

<h2>日本のデジタルノマドビザとは</h2>
<p>日本の外の誰かのためにオンラインで働く人が、最長6か月いられる在留資格です。正式な名前は「特定活動（デジタルノマド）」で、家族のための「特定活動（デジタルノマドの配偶者又は子）」もあります[[s:jnto_nomad]]。</p>
<p>対象になるのは、日本からオンラインでする2種類の仕事です。1つは、外国の組織との雇用契約にもとづいて、その組織の外国での業務をすること。もう1つは、日本の外にいる人に、有償でサービスを提供したり、物を売ったりすることです[[s:isa_nomad_en,egov_immig_rules]]。なので、会社員だけでなく、海外に取引先のあるフリーランスも当てはまります。</p>
<p>一方で、日本で仕事に就くための資格ではありません。入管庁のページには、この在留資格では、日本の公私の機関との雇用契約などにもとづいて働くことはできない、とあります[[s:isa_nomad_en]]。それが目的なら、別の在留資格を考えることになります。</p>

<h2>誰が対象になるのか</h2>
<p>必要なのは、対象の国・地域のパスポート、高い収入、民間の医療保険の3つです。2026年11月時点で、出入国在留管理庁は次のように決めています[[s:isa_nomad_en]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>条件</th><th>中身</th></tr></thead>
<tbody>
<tr><td>国籍</td><td>入管庁の一覧にある国・地域のパスポート。一覧は、日本との間で査証免除と租税条約の両方がある国・地域から作られています[[s:isa_nomad_en,isa_nomad_list]]。</td></tr>
<tr><td>収入</td><td>申請する本人の年収が1,000万円以上[[s:isa_nomad_en,jnto_nomad]]。</td></tr>
<tr><td>保険</td><td>滞在中の死亡・けが・病気を補償し、治療費1,000万円以上をカバーする民間の保険[[s:isa_nomad_en]]。</td></tr>
<tr><td>仕事</td><td>日本からのオンラインの仕事で、雇われている外国の組織のための仕事か、日本の外の取引先・お客さんへの有償の仕事。日本の組織との雇用契約にもとづいて働くことはできない[[s:isa_nomad_en,egov_immig_rules]]。</td></tr>
</tbody></table></div>
<p>一覧は PDF で、自分のパスポートが対象かを確かめられるのはそこだけです[[s:isa_nomad_list]]。ほかのサイトに載っている国の数は古くなるので、信頼できるのはいまの版です。収入の条件は申請する本人のものなので、パートナーの収入を足して届かせることはあてにしないほうが安全です。</p>

<h2>どれくらいいられて、更新はできるのか</h2>
<p>最長6か月で、延長はできません[[s:isa_nomad_en,jnto_nomad]]。日本を出てから6か月たてば、同じ在留資格でまた来られます[[s:isa_nomad_en]]。つまり、日本で6か月、ほかの場所で6か月というリズムになります。</p>
<p>いまでも「1回だけ延長できる」と書いているサイトがあります。入管庁のページには延長できないとあり、計画はそちらに合わせるのがいいと思います。ふつうのビザなしの滞在と比べると、次のとおりです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>短期滞在（査証免除）</th><th>デジタルノマド</th></tr></thead>
<tbody>
<tr><td>期間</td><td>たいてい最長90日。国籍によっては15日・30日・180日[[s:jnto_visa]]</td><td>最長6か月、延長なし[[s:isa_nomad_en]]</td></tr>
<tr><td>仕事</td><td>報酬を受ける仕事はできない[[s:jnto_visa]]</td><td>外国の雇用主や海外の取引先のためのオンラインの仕事。日本の雇用主のためには働けない[[s:isa_nomad_en]]</td></tr>
<tr><td>在留カード</td><td>出ない[[s:egov_immig_act]]</td><td>出ない[[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>

<h2>パートナーや子どもも一緒に来られるのか</h2>
<p>来られます。本人に扶養される配偶者と子どもは、家族のための在留資格で来られ、対象は扶養を受ける家族としての日常の活動です[[s:isa_nomad_en,jnto_nomad]]。本人と同じく、家族にも在留カードは出ません[[s:egov_immig_rules]]。</p>
<p>家族の条件は、本人と少し違います。家族は査証免除の国・地域のパスポートが要りますが、租税条約の条件は本人だけのものです[[s:isa_nomad_en]]。保険は本人と同じで、滞在中の死亡・けが・病気を補償し、治療費1,000万円以上をカバーするものが一人ひとりに要ります[[s:isa_nomad_en]]。この在留資格は配偶者か子どものためのものなので、パートナーと結婚していないなら、計画を立てる前に入管庁に聞いてみるといいと思います。</p>

<h2>どうやって申請するのか</h2>
<p>案内は2つの公式のページにあります。ビザは外務省が出し、必要な書類は外務省のページにあると JNTO が案内しています[[s:jnto_nomad]]。入管庁のページには、この在留資格で新しく日本に入国したい人のための、在留資格認定証明書の交付申請の案内もあります[[s:isa_nomad_en]]。</p>
<ol>
<li>自分のパスポートの国・地域が、入管庁の一覧にあるかを確かめる[[s:isa_nomad_list]]。</li>
<li>収入の証明と、条件を満たす保険の証書をそろえる[[s:isa_nomad_en]]。</li>
<li>JNTO から案内されている外務省のページで、いまのビザの必要書類を見る[[s:jnto_nomad]]。</li>
<li>入管庁のページで、この在留資格で初めて入国する人の在留資格認定証明書の案内を読む[[s:isa_nomad_en]]。</li>
<li>滞在は6か月で終わるので、出国の日を決めておく[[s:isa_nomad_en]]。</li>
</ol>
<p>2つのページで分からないことは、外務省か入管庁に聞くのがいいと思います。日本に入ってから切り替えるのは、期待されているより難しいです。入管法では、短期滞在の人が日本の中で在留資格を変えられるのは「やむを得ない特別の事情」があるときだけです[[s:egov_immig_act]]。だから、観光で入ってから切り替えようとするより、出発の前に在留資格の手続きを済ませておくのが筋だと思います。</p>

<h2>このビザで手に入らないものは何か</h2>
<p>在留カードです。そして、そこから多くのことが決まります。入管法では、デジタルノマドとその家族は中長期在留者に当たらないので、カードは出ません[[s:egov_immig_act,egov_immig_rules]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>在留カードがある人</th><th>デジタルノマドの在留資格</th></tr></thead>
<tbody>
<tr><td>住民登録（住民票）</td><td>カードのある外国人住民は、住んでいる所で登録される[[s:soumu_juki]]</td><td>登録されない</td></tr>
<tr><td>国民健康保険</td><td>登録された外国人住民が入れる[[s:egov_nhi_rules]]</td><td>入れない[[s:egov_nhi_rules]]。それとは別に、この在留資格では民間の保険が条件になっている[[s:isa_nomad_en]]</td></tr>
<tr><td>普通の賃貸</td><td>国の大家さん向けのガイドラインが、本人確認の書類の例の1つにカードを挙げている[[s:mlit_foreign_rental]]</td><td>私たちの見方では難しい。家具付きの月単位の部屋のほうがたいてい簡単</td></tr>
</tbody></table></div>
<p>いちばん影響を感じるのは部屋を借りるときです。国の大家さん向けのガイドラインは、本人確認の書類の例にパスポートと在留カードを挙げ、何を求めるかは大家さんと借りる人の間に任せています[[s:mlit_foreign_rental]]。日本の銀行口座と、日本で使える電話があるかも聞くように書いています[[s:mlit_foreign_rental]]。カードも日本の口座もないなら、家具付きで月単位に借りる部屋のほうが楽だと私たちは考えています。</p>
<p>税金も、よく誤解されるところです。日本の所得税では、日本に住所があるか、1年以上続けて住んでいる人が居住者になります[[s:nta_2875]]。非居住者は日本の国内源泉所得にだけ課税され、日本でした仕事への報酬は国内源泉所得に当たります[[s:nta_nonresident]]。租税条約で変わることもあるので[[s:nta_2875]]、「6か月なら税金はかからない」は単純すぎます。自分の国と日本の租税条約に詳しい税理士に聞くのがいちばんです。</p>
<p>ここに書いたのは、すべて2026年11月時点の決まりです。自分の場合については、外務省、出入国在留管理庁、またはビザを扱う行政書士に確かめてください。</p>

<h2>6か月、どこを拠点にするか</h2>
<p>大事なのは5つだと私たちは考えています。仕事の時間ずっと頼れる回線、東京と空港への電車、月単位で借りられる家具付きの部屋、かかれる診療所、そして季節です。東京はこのうちいくつかでは勝ちますが、全部ではありません。私たちの見方をまとめると、次のようになります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>東京</th><th>地方の都市</th><th>東京から2〜3時間の小さな町</th></tr></thead>
<tbody>
<tr><td>家具付きの月単位の部屋</td><td>選択肢がいちばん多い</td><td>ある程度ある</td><td>少ないので、早めに予約する</td></tr>
<tr><td>空港への行き来</td><td>楽</td><td>たいてい楽</td><td>遠くなるので、計画が要る</td></tr>
<tr><td>英語での暮らし</td><td>いちばん楽</td><td>ところによる</td><td>ところによる。翻訳アプリが助けになる</td></tr>
<tr><td>引き換えにするもの</td><td>広さと静けさ</td><td>どれも少しずつ</td><td>選択肢と便利さ。代わりに広さ、静けさ、ゆっくりした毎日</td></tr>
</tbody></table></div>
<p>光回線は、思われているほど心配いりません。2025年3月末の推計で、光回線を引ける世帯は、東京都で96.3%、下田市で約93.8%です[[s:soumu_ftth_2025]]。これは建物まで回線が届くかどうかの数字で速さではなく、引くまでに時間がかかることもあります。私たちが下田で宿を開いたときは、繁忙期で回線の工事に2か月以上かかり、置くだけのホームルーターでしのぎました。もう回線が入っている部屋なら、その待ち時間がありません。</p>
<p>JNTO には、都道府県・言語・診療科で医療機関を探せる英語の検索があり、行く前にそれぞれに確かめるよう案内しています[[s:jnto_medical]]。いちばん近い診療所は、必要になった日より、着いた日に調べておくほうが楽です。</p>
<p>[[l:ja-izu|伊豆半島]]の下田は、東京から行ける小さな町の一例です。2026年11月時点で、東京駅からの直通の電車は2時間29分〜44分で[[s:jre_tt_tokyo]]、行き方は[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。私たちの NODE Shimoda は、伊豆急下田駅から歩いて8分の約40㎡のアパートの一室で、ワークデスク、Wi-Fi、キッチン、洗濯機とガス乾燥機があります[[s:node_site,node_room]]。長く滞在するリモートワーカーを考えて作ったので、長めの滞在を考えているなら、気軽に聞いてください。ひと季節がうまくいって家を探しはじめたら、[[l:ja-akiya-try-first|空き家を買う前にその町で暮らしてみる話]]も読んでみてください。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律・在留手続き・税の助言ではありません。</p>',
  "faq": [
    ("日本のデジタルノマドビザは、どれくらいいられますか？",
     "最長6か月です。2026年11月時点で、出入国在留管理庁は延長できないとしています[[s:isa_nomad_en]]。"),
    ("日本のデジタルノマドビザは延長できますか？",
     "できません。日本を出てから6か月たてば、同じ在留資格でまた来られるので[[s:isa_nomad_en]]、6か月いて、6か月離れる形になります。"),
    ("デジタルノマドビザで在留カードはもらえますか？",
     "もらえません。デジタルノマドとその家族は中長期在留者に当たらないので、カードは出ません[[s:egov_immig_act,egov_immig_rules]]。そのため、住民登録もされず、国民健康保険にも入れません[[s:soumu_juki,egov_nhi_rules]]。"),
    ("デジタルノマドビザで家族を連れて来られますか？",
     "本人に扶養される配偶者と子どもは、家族のための在留資格で来られます[[s:jnto_nomad,isa_nomad_en]]。家族は査証免除の国・地域のパスポートと、本人と同じ条件の保険が要ります[[s:isa_nomad_en]]。結婚していない場合は、先に入管庁に聞いてください。"),
    ("このビザで日本の会社で働けますか？",
     "働けません。入管庁は、この在留資格では日本の公私の機関との雇用契約などにもとづいて働くことはできない、としています[[s:isa_nomad_en]]。対象は、雇われている外国の組織のためのオンラインの仕事か、日本の外の取引先への有償の仕事です。"),
  ],
 },
}
