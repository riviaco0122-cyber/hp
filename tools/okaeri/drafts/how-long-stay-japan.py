# -*- coding: utf-8 -*-
"""how-long-stay の新規記事（2026-11-20 執筆部）。構成案とリサーチメモ: tools/okaeri/briefs/how-long-stay-japan.md（7. 追記まで）。
制度の事実は、リサーチ部が開いて確かめた出典（e-Gov の入管法・施行規則・国保法施行規則、JNTO、衆議院、観光庁）と、
編集長が 2026-11-16 に確かめた入管庁のデジタルノマドのページ（既存 isa_nomad_en）だけを使う。
ワーキングホリデー、取り決めで6か月まで延長できる国、「1年に180日」、長期観光の預貯金・対象国・保険の条件は、公式の出典を開けないので書かない（編集長の判断）。
見出し写真は編集長が用意する（"TODO-PHOTO"）。content.py の ARTICLES の1件と同じ形。"""

SOURCES_NEW = {
    # 既存キー。正式名の条番号だけ足す（URL・短い名前は同じ）
    "egov_immig_act": ("https://laws.e-gov.go.jp/law/326CO0000000319", "Immigration Control Act", "出入国管理及び難民認定法（e-Gov法令検索）",
                       "Immigration Control and Refugee Recognition Act, Articles 5, 7, 19, 19-3, 20, 21, 24, 24-3, 70 and Appended Table I (e-Gov, version in force 1 October 2026)"),
    "egov_immig_rules": ("https://laws.e-gov.go.jp/law/356M50000010054", "Immigration Control Act ordinance", "出入国管理及び難民認定法施行規則（e-Gov法令検索）",
                         "Ordinance for Enforcement of the Immigration Control and Refugee Recognition Act, Article 19-5 and Appended Table II (e-Gov, version in force 1 October 2026)"),
    # 新しい出典
    "egov_immig_act_jesta": ("https://laws.e-gov.go.jp/law/326CO0000000319/20290331_508AC0000000032", "Immigration Control Act (amended, not yet in force)",
                             "出入国管理及び難民認定法（令和8年法律第32号による改正後・未施行）（e-Gov法令検索）",
                             "Immigration Control and Refugee Recognition Act as amended by Act No. 32 of 2026, Article 7-2 (e-Gov, not yet in force; checked 20 November 2026)"),
    "shugiin_bill221_20": ("https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/keika/1DE1F16.htm", "House of Representatives", "衆議院（議案審議経過情報）",
                           "House of Representatives: Progress of cabinet bill no. 20, 221st Diet session (checked 20 November 2026)"),
    "jta_jesta": ("https://www.mlit.go.jp/kankocho/content/002019837.pdf", "Japan Tourism Agency", "観光庁（JESTA の導入に伴う免税制度の見直し）",
                  "Japan Tourism Agency: Review of tax-free shopping checks following the introduction of JESTA (2026)"),
}

ARTICLE = {
 "id": "how-long-stay", "slug": "how-long-can-you-stay-in-japan", "topic": "live", "place": None, "also": ["stay"],
 "photo": ("passport-stamps", "An open passport with colourful entry and exit stamps on its pages", ""),
 "published": "2026-11-20", "updated": "2026-11-20",
 "kicker": "Live part-time",
 "h1": "How long can you stay in Japan? 90 days, and the ways to stay longer",
 "seo_title": "How Long Can I Stay in Japan? 90 Days and Longer Stays",
 "description": "Most visa-free visitors can stay in Japan for up to 90 days, and extensions need good reason. For six months or a year, pick the right status before you come.",
 "dek": "Most visa-free visitors can stay up to 90 days, and some passports get less. If you want six months or a year, pick the right status before you come.",
 "card": "Most visa-free visitors get up to 90 days, and some passports get less. Extensions need good reason and every entry is checked again, so for six months or a year it’s better to choose the right status before you travel.",
 "keywords": [("how long can i stay in japan", "170", "3"), ("how long can you stay in japan", "—", "—"),
              ("japan visa free stay / japan 90 day rule", "—", "—"), ("extend stay in japan / stay in japan for 6 months", "—", "—")],
 "intent": "Know（自分は何日いられるか）→ Do（もっと長くいるには何を選ぶか）",
 "points": [
   "Most visa-free visitors get up to 90 days, though some passports get 30 days or less.",
   "Extensions need good reason, and every time you come back, you’re checked again at the border.",
   "For six months or a year, look at the digital nomad status or the long stay for sightseeing.",
 ],
 "body": """
<p>Ask online how long you can stay in Japan and you’ll get answers from 90 days to a year, sometimes in the same thread. The real answer depends on two things: the passport you hold and the status you enter on. Everything below describes the rules as of November 2026.</p>

<h2>How long can you stay in Japan without a visa?</h2>
<p>For most visa-free visitors, up to 90 days. Japan’s rules give a short-term visitor (officially, a Temporary Visitor) 90 days, 30 days or up to 15 days, and JNTO says most visa-free short stays get up to 90 [[s:egov_immig_rules,jnto_visa]].</p>
<p>Which one you get comes down to your passport. JNTO points to the Ministry of Foreign Affairs list of visa-exempt countries and regions, and that list is the one to trust for your own case [[s:jnto_visa]]. If your passport isn’t on it, you’ll need a visa before you travel.</p>
<p>The status is meant for short stays: sightseeing, recreation, sport, visiting relatives, attending meetings and business liaison, among other things [[s:egov_immig_act]]. It doesn’t cover paid work, long-term study or applying to live here [[s:jnto_visa]].</p>

<h2>Can you extend a visa-free stay?</h2>
<p>You can apply, but we wouldn’t plan a trip around it. Japan’s Immigration Control Act lets you apply to renew your period of stay, and the Minister of Justice can grant it only when there are reasonable grounds [[s:egov_immig_act]].</p>
<p>Timing matters if your plans fall apart near the end. Say you apply before your period of stay ends and there’s no decision yet. You can then stay until the decision or two months after your old expiry date, whichever comes first [[s:egov_immig_act]]. That grace period doesn’t apply if you were given 30 days or less [[s:egov_immig_act]]. So if you think you’ll go over, it’s worth talking to the immigration authorities before the date, not after.</p>
<p>Switching to another status from inside Japan is just as narrow. For a short-term visitor, the Act only allows a change of status when there are unavoidable special circumstances [[s:egov_immig_act]]. That’s why we’d sort out any longer status before you fly.</p>

<h2>Can you leave Japan and come back for another 90 days?</h2>
<p>You can come back, but a new entry isn’t a fresh 90 days by right. Each time you land, an immigration inspector checks that your passport is valid and that what you plan to do here is genuine and fits your status. They also check that the period fits the rules [[s:egov_immig_act]]. It’s up to you to show that you meet those conditions [[s:egov_immig_act]].</p>
<p>People often ask how many days they need to spend abroad before coming back. We don’t know of a number that makes the next entry safe, because the decision is made at the border each time, on what you can show. In our view, a short trip abroad between two long stays doesn’t change how those stays look.</p>
<p>In our view, the better plan for anything beyond 90 days is to pick a status that fits the length of your stay, before you come.</p>

<h2>Which status fits six months or a year?</h2>
<p>If you aren’t taking a job here, there are two main routes past 90 days. One is the digital nomad status, for up to six months. The other is a long stay for sightseeing and recreation, for up to a year.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Status</th><th>Longest stay</th><th>Who it’s for</th><th>Residence card</th></tr></thead>
<tbody>
<tr><td><strong>Temporary Visitor</strong>, visa-exempt</td><td>90 days, 30 days or up to 15 days, depending on your passport [[s:egov_immig_rules,jnto_visa]]</td><td>Short stays such as sightseeing. No paid work [[s:egov_immig_act,jnto_visa]]</td><td>No [[s:egov_immig_act]]</td></tr>
<tr><td><strong>Digital nomad</strong> (Designated Activities)</td><td>Six months, with no extension [[s:isa_nomad_en]]</td><td>Remote workers with an employer or clients outside Japan who meet the income and insurance rules [[s:isa_nomad_en]]</td><td>No [[s:egov_immig_act,egov_immig_rules]]</td></tr>
<tr><td><strong>Long stay for sightseeing and recreation</strong> (Designated Activities)</td><td>Up to one year [[s:egov_nhi_rules]]</td><td>People aged 18 or over staying for sightseeing and recreation, and a spouse who comes with them [[s:egov_nhi_rules]]</td><td>Yes, if you’re given more than three months [[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>
<p>Statuses for study, work or family are a separate process, and you’ll need to arrange them through a Japanese embassy or consulate before you come.</p>
<p>The digital nomad status suits people who want to keep working for an employer or clients abroad. It needs ¥10 million a year in income, and our [[l:digital-nomad|guide to Japan’s digital nomad visa]] covers who qualifies and what it’s like to live here without a residence card.</p>
<p>The long stay for sightseeing is less well known. It does come with a residence card for stays of more than three months, but it still doesn’t let you join National Health Insurance [[s:egov_immig_act,egov_immig_rules,egov_nhi_rules]], so you’ll want private health cover. Its other conditions, such as which passports qualify and what you need to show, are best checked with a Japanese embassy or consulate in your country.</p>
<p>For many people, though, 90 days is plenty for a first season. It’s enough to [[l:akiya-try-first|live in a town for a month or two before you buy a house]]. Our guide to [[l:monthly-rental|renting a place by the month]] covers where you’d stay.</p>

<h2>Can you work remotely while visiting Japan?</h2>
<p>Not for pay in Japan, and how that applies to your job back home is a question for the immigration authorities. Under the Act, a short-term visitor can’t run a business that brings in income or do activities they’re paid for without permission [[s:egov_immig_act]]. JNTO also says a tourist stay doesn’t allow paid work [[s:jnto_visa]].</p>
<p>Whether answering a few emails for your employer counts depends on what you actually do, and we won’t guess at it for you. What’s clear is that Japan has a status built for remote work. If you want to keep working for an employer or clients abroad while you stay longer, the digital nomad status is the one written for that [[s:egov_immig_rules,isa_nomad_en]].</p>

<h2>What happens if you overstay?</h2>
<p>It’s serious, and it can keep you out of Japan for years. Staying past your period of stay without renewing or changing it is a ground for deportation [[s:egov_immig_act]]. It’s also a crime, with up to three years’ imprisonment, a fine of up to ¥3 million, or both [[s:egov_immig_act]].</p>
<p>How long you’re kept out depends on how you leave. Here’s how the Act sets it out, in the version in force from 1 October 2026 [[s:egov_immig_act]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>How you leave</th><th>How long you can’t come back</th></tr></thead>
<tbody>
<tr><td>Deported for the first time</td><td>Five years from your departure [[s:egov_immig_act]]</td></tr>
<tr><td>Deported after an earlier deportation or departure order</td><td>Ten years [[s:egov_immig_act]]</td></tr>
<tr><td>Under a departure order</td><td>One year. It’s five years if you only said you’d leave after an investigation began and you want to come back as a visitor [[s:egov_immig_act]]</td></tr>
</tbody></table></div>
<p>A departure order is the gentler route, and it’s mostly in your hands. You may get one if you go to an immigration office yourself, intending to leave quickly. You also need a clean record: no past deportation or departure order, no listed criminal convictions, and a departure that’s sure to happen promptly [[s:egov_immig_act]]. If you realise you’ve gone over, going in early is far better than waiting.</p>

<h2>Is anything changing for visa-free visitors?</h2>
<p>Yes, but not yet. In June 2026, Japan promulgated an amendment to the Immigration Control Act, Act No. 32 of 2026, after it passed the Diet on 29 May [[s:shugiin_bill221_20]]. It adds a system that lets visa-exempt short-term visitors give their details online in advance and be authorised by the Immigration Services Agency [[s:egov_immig_act_jesta]].</p>
<p>The Japan Tourism Agency calls the system JESTA and says it’s planned to start in the 2028 financial year, which runs from April 2028 to March 2029 [[s:jta_jesta]]. Under the Act, that part comes into force on a date set by cabinet order, no later than 31 March 2029, and as of November 2026 it isn’t in force [[s:egov_immig_act_jesta]]. Until then, nothing about it changes your trip.</p>
<p>All of this is general information as of November 2026, not immigration advice. For your own case, it’s best to check with a Japanese embassy or consulate, the Immigration Services Agency, or an administrative scrivener (<em>gyoseishoshi</em>) who handles visas.</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
   ("How long can I stay in Japan without a visa?",
    "Most visa-free visitors get up to 90 days, but the rules also allow 30 days or up to 15, depending on your passport [[s:egov_immig_rules,jnto_visa]]. The Ministry of Foreign Affairs list, which JNTO links to, is where to check yours [[s:jnto_visa]]."),
   ("Can I extend my 90-day stay in Japan?",
    "You can apply, but it’s only granted when there are reasonable grounds [[s:egov_immig_act]]. If you might go over, talk to the immigration authorities before your stay ends, not after."),
   ("Can I leave Japan and come back for another 90 days?",
    "You can come back, but each entry is checked again. The inspector looks at whether your plans are genuine and fit your status, and it’s up to you to show that [[s:egov_immig_act]]. We don’t know of a number of days abroad that makes the next entry safe."),
   ("Can I stay in Japan for six months or a year without a job?",
    "There are two main routes. One is the digital nomad status, for up to six months with no extension [[s:isa_nomad_en]]. The other is a long stay for sightseeing and recreation of up to a year, for people aged 18 or over [[s:egov_nhi_rules]]. A Japanese embassy or consulate can tell you whether you qualify."),
   ("Can I work remotely on a visa-free stay in Japan?",
    "A short-term visitor can’t do activities they’re paid for without permission [[s:egov_immig_act,jnto_visa]]. How that applies to your own job is a question for the immigration authorities. If you want to keep working for an employer or clients abroad for longer, the digital nomad status is built for that [[s:isa_nomad_en]]."),
   ("What happens if I overstay in Japan?",
    "Overstaying is a ground for deportation and a crime [[s:egov_immig_act]]. A first deportation keeps you out for five years, while leaving under a departure order usually means one year [[s:egov_immig_act]]."),
 ],
 "sources": ["jnto_visa", "egov_immig_act", "egov_immig_rules", "egov_nhi_rules", "isa_nomad_en", "shugiin_bill221_20", "egov_immig_act_jesta", "jta_jesta"],
 "related": ["digital-nomad", "monthly-rental", "akiya-try-first"],
 "ja": {
  "h1": "日本に何日いられる？ 90日と、もっと長くいる方法",
  "dek": "ビザなしで来る人の多くは、最長90日いられます。もっと短いパスポートもあります。半年や1年いたいなら、来る前に合った在留資格を選びましょう。",
  "review": [
   "【2026-11-20 新規の下書き（執筆部）】書いた点: ①1記事1主張は「何日いられるかはパスポートと在留資格で決まる。90日を超えたいなら、出入国をくり返すより、来る前に合った在留資格を選ぶ」。h2 は7つ（ビザなしで何日／延長できるか／出て戻ればまた90日か／半年・1年に合う在留資格／リモートワーク／オーバーステイ／これからの変化）で、すべて疑問形です ②制度の事実は、すべて開いて確かめた条文（e-Gov の入管法・施行規則は2026年10月1日施行の版、国保法施行規則）、JNTO、衆議院の議案審議経過、観光庁の資料によります。時点は本文の冒頭と最後の節に「2026年11月時点」と書きました ③短期滞在の日数は「90日・30日・15日以内」（施行規則 別表第二）。既存記事にある JNTO の「180日」は、入国時にもらえる日数ではないので、この記事では書いていません ④延長は「申請はできるが、相当の理由があるときに限り許可」（第21条）までで、「病気などのとき」とは書いていません。更新の申請中は、決定か元の期限から2か月のどちらか早い日までいられる（30日以下の人は除く。第20条第6項）を足しました。日本の中での在留資格の変更は「やむを得ない特別の事情」があるときだけ（第20条第3項）も書きました ⑤出て戻る話は「入国のたびに審査され、条件を満たすことは自分で示す」（第7条）までで、回数や「1年に180日」は書いていません。「次の入国が安全になる日数は、私たちは知らない」は見解として書きました ⑥地図の表は編集長の判断どおり3行（短期滞在／デジタルノマド／観光・保養の長期滞在）。観光・保養の長期滞在は「最長1年・18歳以上・同行する配偶者」（国保法施行規則 第1条第3号・第4号）と、「3か月を超えて決まれば在留カードが出る」（入管法 第19条の3・施行規則 第19条の5 に例外として載っていない、という条文の読み）、「国民健康保険に入れない」だけで、預貯金・対象国・保険・申請先は書かず、大使館・総領事館で確かめるよう送りました。留学・就労・家族は表の下に1文で「来る前に日本の大使館・総領事館で手続きが要る」とし、ワーキングホリデーという語は使っていません ⑦リモートワークは断定していません（短期滞在では報酬を受ける活動はできない・自分の仕事にどう当たるかは入管に・海外の仕事を続けて長くいるならデジタルノマド） ⑧オーバーステイは、退去強制の理由・罰則（3年以下の拘禁刑か300万円以下の罰金、または両方）・上陸拒否の期間の表（初めての退去強制5年／くり返し10年／出国命令1年、ただし調査が始まってから出国の意思を示し、短期滞在で戻りたい場合は5年。2026年10月1日施行）・出国命令の条件を書きました ⑨JESTA は「2026年5月29日に成立・6月に公布（令和8年法律第32号）・観光庁は2028年度中に始める予定・法律上は2029年3月31日までの政令で定める日に施行・2026年11月時点で未施行」まで ⑩NODE Shimoda と自社の体験には触れていません。内部リンクは本文から3本（digital-nomad・akiya-try-first・monthly-rental）",
   "【人に確かめてほしい点】①ビザ・在留の記述すべて（playbook 6章）。特に、観光・保養の長期滞在に「3か月を超えて決まれば在留カードが出る」と書いた点は条文の読みによります ②留学・就労・家族の在留資格を「来る前に日本の大使館・総領事館で手続きが要る」と1文で書いた点（編集長の判断の文面どおり。日本の中での変更はふれていません） ③出典 egov_immig_act・egov_immig_rules は既存のキーで、正式名に条番号・別表を足しました（SOURCES_NEW で上書き。他の記事の出典欄の表記も変わります） ④英語版の「A short trip to Seoul」（ソウルへの短い旅）は、行き先の例として出しただけです。地名を出したくなければ「a short trip abroad」に変えられます",
   "【書かなかったこと（公式の出典を開けないため）】ワーキングホリデー、取り決めで最長6か月まで延長できる国（英・独など）、「1年に180日」、短期滞在の更新が認められる例（病気など）、観光・保養の長期滞在の預貯金・対象国・保険・最初の期間と更新・申請先、査証免除の国・地域の数、短期滞在中のリモートワークの公式の扱い",
   "【写真】TODO-PHOTO（編集長が用意）。alt の案は「木のテーブルの上のパスポート・ノート・ペンと、そばの小さなスーツケース」。国名が読めるパスポートの表紙・人の顔・航空会社のロゴは写さないものを選んでください",
   "【共食い】akiya-try-first の h2「How long can you stay in Japan to test a town?」はこの記事の主な語とほぼ同じなので、構成案のとおり、同じ PR で空き家の読み手向けの言い方に変え、この記事へのリンクを足すことを編集長に提案します（この下書きでは触っていません）",
  ],
  "points": [
    "ビザなしで来る人の多くは最長90日です。ただ、30日以下のパスポートもあります。",
    "延長には相当の理由が要ります。また、出て戻るたびに、入国のときにあらためて審査されます。",
    "半年や1年なら、デジタルノマドの在留資格か、観光・保養の長期滞在を考えてみてください。",
  ],
  "body": """
<p>日本に何日いられるかをネットで調べると、90日から1年まで、同じスレッドの中でさえ答えがばらばらです。本当の答えは、持っているパスポートと、何の在留資格で入るかの2つで決まります。以下はすべて2026年11月時点の決まりです。</p>

<h2>ビザなしで、日本に何日いられるのか</h2>
<p>ビザなしで来る人の多くは、最長90日です。日本の決まりでは、短期滞在の期間は90日・30日・15日以内のどれかで、JNTO は、ビザなしの短い滞在の多くは最長90日だとしています[[s:egov_immig_rules,jnto_visa]]。</p>
<p>どれになるかは、パスポートで決まります。JNTO は外務省の査証免除の国・地域の一覧を案内していて、自分の場合はその一覧がいちばん確かです[[s:jnto_visa]]。パスポートが一覧にないなら、出発の前にビザが要ります。</p>
<p>この在留資格は短い滞在のためのもので、観光、保養、スポーツ、親族の訪問、会議への参加、業務連絡などが当たります[[s:egov_immig_act]]。報酬を受ける仕事、長い期間の勉強、日本に住むための申請はできません[[s:jnto_visa]]。</p>

<h2>ビザなしの滞在は延長できるのか</h2>
<p>申請はできますが、延長をあてにして旅の計画を立てるのはおすすめしません。入管法では在留期間の更新を申請できますが、法務大臣が許可できるのは、相当の理由があるときに限られます[[s:egov_immig_act]]。</p>
<p>終わり近くで予定が崩れたときは、タイミングが大事です。在留期間が終わる前に申請して、まだ決定が出ていなければ、決定の日か、元の期限から2か月のどちらか早い日まではいられます[[s:egov_immig_act]]。ただし、もらった期間が30日以下なら、この猶予はありません[[s:egov_immig_act]]。過ぎてしまいそうなら、期限の後ではなく前に、入管に相談するのがいいと思います。</p>
<p>日本の中で別の在留資格に切り替えるのも、同じくらい狭き門です。入管法では、短期滞在の人が在留資格を変えられるのは、やむを得ない特別の事情があるときだけです[[s:egov_immig_act]]。だから、長くいるための在留資格は、飛行機に乗る前に済ませておくのがいいと私たちは考えています。</p>

<h2>一度出国して戻れば、また90日いられるのか</h2>
<p>戻ってくることはできますが、入国すれば当然にまた90日もらえるわけではありません。入国のたびに、入国審査官が、パスポートが有効か、日本でする予定のことが本当で在留資格に当たるか、期間が決まりに合っているかを確かめます[[s:egov_immig_act]]。条件を満たしていることは、自分で示す必要があります[[s:egov_immig_act]]。</p>
<p>何日、日本の外にいればまた入れるのか、とよく聞かれます。次の入国が安全になる日数を、私たちは知りません。毎回その場で、示せることをもとに決まるからです。長い滞在の間にソウルへ短い旅をはさんでも、その滞在の見え方は変わらない、と私たちは思います。</p>
<p>90日を超えて過ごしたいなら、来る前に、滞在の長さに合った在留資格を選ぶほうがいい、と私たちは考えています。</p>

<h2>半年や1年なら、どの在留資格が合うのか</h2>
<p>日本で仕事に就くのでなければ、90日を超える道は主に2つです。1つは最長6か月のデジタルノマドの在留資格、もう1つは最長1年の観光・保養の長期滞在です。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>在留資格</th><th>いちばん長い期間</th><th>対象</th><th>在留カード</th></tr></thead>
<tbody>
<tr><td><strong>短期滞在</strong>（査証免除）</td><td>90日・30日・15日以内。パスポートによる[[s:egov_immig_rules,jnto_visa]]</td><td>観光などの短い滞在。報酬を受ける仕事はできない[[s:egov_immig_act,jnto_visa]]</td><td>出ない[[s:egov_immig_act]]</td></tr>
<tr><td><strong>デジタルノマド</strong>（特定活動）</td><td>6か月。延長なし[[s:isa_nomad_en]]</td><td>日本の外の雇用主や取引先のために働くリモートワーカーで、収入と保険の条件を満たす人[[s:isa_nomad_en]]</td><td>出ない[[s:egov_immig_act,egov_immig_rules]]</td></tr>
<tr><td><strong>観光・保養の長期滞在</strong>（特定活動）</td><td>最長1年[[s:egov_nhi_rules]]</td><td>観光・保養のために滞在する18歳以上の人と、同行する配偶者[[s:egov_nhi_rules]]</td><td>3か月を超えて決まれば出る[[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>
<p>留学・仕事・家族のための在留資格は別の手続きで、来る前に日本の大使館・総領事館で手続きをすることになります。</p>
<p>デジタルノマドの在留資格は、海外の雇用主や取引先の仕事を続けたい人に向いています。年収1,000万円以上が必要で、対象になる人や、在留カードなしで暮らすとどうなるかは、[[l:ja-digital-nomad|日本のデジタルノマドビザの記事]]にまとめています。</p>
<p>観光・保養の長期滞在は、あまり知られていません。3か月を超える滞在なら在留カードが出ますが、それでも国民健康保険には入れないので[[s:egov_immig_act,egov_immig_rules,egov_nhi_rules]]、民間の医療保険があると安心です。どのパスポートが対象か、何を示す必要があるかといった、ほかの条件は、計画を立てる前に自分の国の日本大使館・総領事館で確かめるのがいいと思います。</p>
<p>とはいえ、最初のひと季節なら、90日で十分という人も多いはずです。[[l:ja-akiya-try-first|家を買う前に1〜2か月その町で暮らしてみる]]には足りますし、どこに泊まるかは[[l:ja-monthly-rental|月単位で部屋を借りる記事]]にまとめています。</p>

<h2>旅行中に、リモートで仕事をしてもいいのか</h2>
<p>日本で報酬を受ける仕事はできません。それが自分の国の仕事にどう当たるかは、入管に聞くべきことです。入管法では、短期滞在の人は、許可なしに収入を伴う事業を営んだり、報酬を受ける活動をしたりできません[[s:egov_immig_act]]。JNTO も、観光の滞在では報酬を受ける仕事はできないとしています[[s:jnto_visa]]。</p>
<p>雇い主からのメールに少し返事をするのがそれに当たるかは、実際に何をするかによるので、私たちが代わりに判断することはしません。はっきりしているのは、日本にはリモートワークのための在留資格があることです。海外の雇用主や取引先の仕事を続けながら長くいたいなら、そのために作られたのがデジタルノマドの在留資格です[[s:egov_immig_rules,isa_nomad_en]]。</p>

<h2>オーバーステイすると、どうなるのか</h2>
<p>重いことで、何年も日本に入れなくなることがあります。更新や変更をせずに在留期間を過ぎると、退去強制の理由になります[[s:egov_immig_act]]。犯罪でもあり、3年以下の拘禁刑か300万円以下の罰金、またはその両方が科されることがあります[[s:egov_immig_act]]。</p>
<p>どれくらい入れなくなるかは、どう出国するかで変わります。2026年10月1日から施行されている入管法では、次のとおりです[[s:egov_immig_act]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>どう出国するか</th><th>再び入国できない期間</th></tr></thead>
<tbody>
<tr><td>初めての退去強制</td><td>出国から5年[[s:egov_immig_act]]</td></tr>
<tr><td>過去に退去強制か出国命令を受けたことがある人の退去強制</td><td>10年[[s:egov_immig_act]]</td></tr>
<tr><td>出国命令</td><td>1年。調査が始まってから出国の意思を示し、短期滞在で戻りたい場合は5年[[s:egov_immig_act]]</td></tr>
</tbody></table></div>
<p>出国命令はより穏やかな道で、その多くは自分しだいです。すみやかに出国するつもりで自分から入管に出向き、過去に退去強制や出国命令を受けたことがなく、決められた罪で刑を受けたことがなく、すぐに出国することが確かなら、出国命令を受けられることがあります[[s:egov_immig_act]]。期限を過ぎたと気づいたら、待つより早く出向くほうがずっといいです。</p>

<h2>ビザなしで来る人の手続きは、これから変わるのか</h2>
<p>変わりますが、まだです。2026年5月29日に国会で成立した入管法の改正（令和8年法律第32号）が、6月に公布されました[[s:shugiin_bill221_20]]。この改正で、ビザなしで短期滞在に来る人が、前もってオンラインで情報を出し、出入国在留管理庁の認証を受ける仕組みができます[[s:egov_immig_act_jesta]]。</p>
<p>観光庁はこの仕組みを JESTA と呼び、2028年度（2028年4月〜2029年3月）に始める予定としています[[s:jta_jesta]]。法律では、この部分は2029年3月31日までの間に政令で決める日に施行され、2026年11月時点ではまだ施行されていません[[s:egov_immig_act_jesta]]。それまでは、旅の手続きは何も変わりません。</p>
<p>ここに書いたのは、2026年11月時点の一般的な情報で、在留手続きの助言ではありません。自分の場合については、日本の大使館・総領事館、出入国在留管理庁、またはビザを扱う行政書士に確かめてください。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
    ("ビザなしで、日本に何日いられますか？",
     "多くの人は最長90日ですが、パスポートによっては30日や15日以内のこともあります[[s:egov_immig_rules,jnto_visa]]。自分の場合は、JNTO が案内している外務省の一覧で確かめてください[[s:jnto_visa]]。"),
    ("90日の滞在は延長できますか？",
     "申請はできますが、許可されるのは相当の理由があるときに限られます[[s:egov_immig_act]]。過ぎてしまいそうなら、期限の後ではなく前に入管に相談してください。"),
    ("一度出国して戻れば、また90日いられますか？",
     "戻ることはできますが、入国のたびにあらためて審査されます。審査官は、予定が本当で在留資格に当たるかを見て、それを示すのは自分です[[s:egov_immig_act]]。次の入国が安全になる、日本の外にいる日数を、私たちは知りません。"),
    ("仕事をせずに、半年や1年日本にいられますか？",
     "主な道は2つで、最長6か月・延長なしのデジタルノマドの在留資格[[s:isa_nomad_en]]と、18歳以上の人のための最長1年の観光・保養の長期滞在です[[s:egov_nhi_rules]]。対象になるかは、日本の大使館・総領事館で確かめられます。"),
    ("ビザなしの滞在中に、リモートで仕事をしてもいいですか？",
     "短期滞在の人は、許可なしに報酬を受ける活動はできません[[s:egov_immig_act,jnto_visa]]。それが自分の仕事にどう当たるかは、入管に聞くべきことです。海外の雇用主や取引先の仕事を続けながら長くいたいなら、そのための在留資格がデジタルノマドです[[s:isa_nomad_en]]。"),
    ("日本でオーバーステイすると、どうなりますか？",
     "退去強制の理由になり、犯罪にもなります[[s:egov_immig_act]]。初めての退去強制では5年、出国命令で出た場合はふつう1年、日本に入れなくなります[[s:egov_immig_act]]。"),
  ],
 },
}
