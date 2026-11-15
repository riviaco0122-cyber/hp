# -*- coding: utf-8 -*-
"""izu-from-tokyo の書き直し（2026-11-15 品質保証部の指摘とリサーチメモにもとづく）。content.py の ARTICLES の1件と同じ形。
運賃表は content.py の TRAIN_TABLE_EN/JA を使わず、本文に直接書く（運賃の数字は一次で確かめられていないので、黄色い枠で人に回す）。"""

SOURCES_NEW = {
    "jre_odoriko": ("https://www.jreast.co.jp/en/multi/traininformation/odoriko/", "JR East", "JR東日本", "JR East: Limited Express Odoriko"),
    "jre_izu": ("https://www.jreast.co.jp/en/multi/destinations/izu.html", "JR East", "JR東日本", "JR East: Izu"),
    "jre_izu_tt": ("https://www.jreast.co.jp/multi/traininformation/odoriko/pdf/odoriko_timetable.pdf", "JR East timetable, Oct–Nov 2026",
                   "JR東日本 伊豆方面特急時刻表（2026年10〜11月）", "JR East: Timetable of Limited Express bound for Izu area (1 Oct–30 Nov 2026)"),
    "jre_tt_local": ("https://timetables.jreast.co.jp/2610/train/010/013771.html", "JR East timetable, October 2026",
                     "JR東日本 時刻表（2026年10月）", "JR East: Timetable, local train Atami to Izukyu-Shimoda (October 2026)"),
    "jre_fare2026": ("https://www.jreast.co.jp/es/2026unchin-kaitei/", "JR East", "JR東日本", "JR East: Fare revision of 14 March 2026"),
    "jre_widepass": ("https://www.jreast.co.jp/en/multi/pass/tokyowidepass.html", "JR East", "JR東日本", "JR East: JR TOKYO Wide Pass"),
    "jrp_price": ("https://japanrailpass.net/en/purchase/price/", "Japan Rail Pass (JR Group)", "JRグループ", "JR Group: Japan Rail Pass types and prices"),
    "izu_tokko": ("https://kanko.city.izu.shizuoka.jp/sightseeing/tokkonoyu/", "Izu City", "伊豆市", "Izu City tourism: Tokko-no-yu"),
    "shimoda_ohama": ("https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html", "Shimoda City", "下田市",
                      "Shimoda City: Shirahama Ohama Beach"),
    "shimoda_beach2026": ("https://www.shimoda-city.info/post/20260528", "Shimoda Tourism Association", "伊豆下田観光協会",
                          "Shimoda Tourism Association: beaches open from 18 July 2026"),
    "shimoda_beach2026b": ("https://www.shimoda-city.info/post/20260824", "Shimoda Tourism Association", "伊豆下田観光協会",
                           "Shimoda Tourism Association: end of the 2026 beach season"),
}

ARTICLE = {
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, passes and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Passes and Where to Stay",
 "description": "Getting from Tokyo to the Izu Peninsula by train: the direct Odoriko, the Shinkansen routes, which rail passes work and which town to stay in (November 2026).",
 "dek": "The south of the Izu Peninsula is too far for a comfortable day trip and just right for a week. Here’s how to get there by train, which passes help, when to go, and the downsides worth knowing about.",
 "card": "The direct Odoriko, the Shinkansen routes via Atami and Mishima, the JR Tokyo Wide Pass and the Japan Rail Pass, and which Izu town to stay in. As of November 2026.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—")],
 "intent": "Do（やり方を知りたい）",
 "points": [
   "The direct Odoriko limited express takes 2 hours 49 minutes from Tokyo to Shimoda, according to JR East (as of November 2026). A day trip there means more than five hours on the train.",
   "For Shuzenji, most people take the Shinkansen to Mishima and then the Izuhakone Railway, about 35 minutes. There are only a few direct trains a day.",
   "The JR Tokyo Wide Pass (¥16,000 for three days, foreign passports only) covers the Izu Kyuko line’s limited expresses. The Japan Rail Pass doesn’t cover the line south of Ito.",
   "In 2026, Shimoda’s beaches were open for swimming from 18 July to the end of August, and lifeguards are only on duty in the official season.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The simplest way is the Odoriko limited express, which runs from Tokyo down the east coast of the [[l:izu|Izu Peninsula]] to Shimoda without a change. JR East gives the journey as 2 hours 49 minutes and Ito as about 1 hour 40 minutes (as of November 2026) [[s:jre_izu]]. There are a couple of other routes worth knowing, especially for Shuzenji.</p>
<div class="tablewrap"><table>
<thead><tr><th>Route</th><th>Changes</th><th>Time</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Direct Odoriko</strong> to Ito and Izukyu-Shimoda</td><td>None</td><td>About 1 h 40 min to Ito, 2 h 49 min to Shimoda [[s:jre_izu]]</td><td>In October–November 2026, direct trains left Tokyo between about 9:00 and 13:00 [[s:jre_izu_tt]].</td></tr>
<tr><td><strong>Shinkansen to Atami</strong>, then a local train to Shimoda</td><td>One, at Atami</td><td>The Shinkansen leg, plus about 1 h 40 min to 1 h 50 min from Atami [[s:jre_tt_local]]</td><td>It isn’t faster than the direct train, but it helps when the direct times don’t suit you.</td></tr>
<tr><td><strong>Shinkansen to Mishima</strong>, then the Izuhakone Railway to Shuzenji</td><td>One, at Mishima</td><td>About 35 min from Mishima [[s:jg6311]]</td><td>The usual way to Shuzenji.</td></tr>
<tr><td><strong>Direct Odoriko</strong> to Shuzenji</td><td>None</td><td>A little over 2 h [[s:jre_izu_tt]]</td><td>The October–November 2026 timetable shows only about three a day.</td></tr>
</tbody></table></div>
<p class="fine">Times are from JR East’s website and timetables, checked in November 2026.</p>
[[ed:Count the direct Odoriko trains from Tokyo to Shimoda and to Shuzenji in JR East’s Izu timetable PDF (October–November 2026), and add the Shinkansen time from Tokyo to Atami and to Mishima.]]
<p>We’ve left fares out of the table for now. JR East revised its fares on 14 March 2026 [[s:jre_fare2026]], and we haven’t yet checked the new totals against an official source. JR East’s Ekinet booking site shows the exact fare for your date.</p>
[[ed:On Ekinet, check the one-way adult fare with a reserved seat, as of November 2026, from Tokyo to Atami, Ito, Shuzenji and Izukyu-Shimoda. Secondary sites give ¥3,670, ¥4,000, ¥4,750 and ¥6,660. Add them to the table only if they match, with the date checked.]]

<h2>Can you use the Japan Rail Pass or the JR Tokyo Wide Pass to get to Izu?</h2>
<p>Yes, but they don’t reach the same places, so it depends on where you’re going.</p>
<div class="tablewrap"><table>
<thead><tr><th>Pass</th><th>Price and length</th><th>What it covers in Izu</th></tr></thead>
<tbody>
<tr><td><strong>JR Tokyo Wide Pass</strong></td><td>¥16,000 for adults, three days in a row, foreign passport holders only, from 14 March 2026 [[s:jre_widepass]]</td><td>JR East lines in its area, including limited expresses on the Izu Kyuko line to Shimoda [[s:jre_widepass]]</td></tr>
<tr><td><strong>Japan Rail Pass</strong></td><td>¥50,000 for seven days when bought online in yen, ¥53,000 through overseas agents (JR Group notice, 9 April 2026) [[s:jrp_price]]</td><td>The JR sections. You pay extra on the Izu Kyuko line south of Ito [[s:jg6305]].</td></tr>
</tbody></table></div>
<p>The Izuhakone Railway from Mishima to Shuzenji isn’t a JR line, so on the Japan Rail Pass you pay that fare separately. japan-guide gives it as ¥550 [[s:jg6305]].</p>
[[ed:Confirm on JR East’s Tokyo Wide Pass page whether the Tokaido Shinkansen and the Izuhakone Railway are excluded, and whether the Izuhakone Railway’s Mishima–Shuzenji fare changed in 2026.]]

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is, but the south really isn’t. With Shimoda 2 hours 49 minutes away on the direct train [[s:jre_izu]], a return trip means more than five and a half hours on the train for a few hours on the beach. Atami and Ito are closer to Tokyo and work fine as day trips. We think the south coast and the inland hot-spring towns are far better if you stay.</p>

<h2>Which Izu town suits you?</h2>
<p>It mostly comes down to how far you want to go and how long you can stay.</p>
<div class="tablewrap"><table>
<thead><tr><th>Town</th><th>From Tokyo</th><th>What it’s like</th><th>Day trip or stay?</th></tr></thead>
<tbody>
<tr><td><strong>Atami and Ito</strong></td><td>Ito about 1 h 40 min; Atami is closer</td><td>The closest to Tokyo and the busiest, with the most hotels.</td><td>A day trip works</td></tr>
<tr><td><strong>Shuzenji</strong></td><td>About 35 min from Mishima, or a little over 2 h direct</td><td>A hot-spring town inland, along a river, with a bamboo grove and a temple [[s:uncharted]]. The famous Tokko-no-yu spring is for looking at only. If you want to put your feet in, the free Sugi-no-yu foot bath and Kawara-yu are nearby [[s:izu_tokko]].</td><td>Better to stay</td></tr>
<tr><td><strong>Shimoda</strong></td><td>2 h 49 min direct</td><td>A port town with white-sand beaches. JNTO puts Shirahama Beach about 15 minutes by bus from the station [[s:jnto]]. The city and the prefecture describe its harbour as Japan’s top landing port for [[l:kinmedai|kinmedai]] [[s:pref]].</td><td>Better to stay</td></tr>
</tbody></table></div>
<p class="fine">Times are from the route table above.</p>

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>For swimming, it’s mid-July to the end of August. For a quieter stay, we’d pick the months either side.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Swimming season (in 2026, 18 July to 30 or 31 August)</td><td>Shimoda’s beaches open for swimming, with lifeguards. Shirahama Ohama Beach ran from 18 July to 31 August, 8:00 to 16:00, and Shirahama Chuo Beach until 30 August [[s:shimoda_ohama,shimoda_beach2026,shimoda_beach2026b]]. Outside the season and those hours, there are no lifeguards [[s:shimoda_ohama]].</td></tr>
<tr><td>Late May to September</td><td>In good weather the sea is pleasant [[s:jg6304]], and outside the school holidays there are fewer people around.</td></tr>
<tr><td>The rest of the year</td><td>The towns get much quieter. In our view, it’s the easiest time for hot springs and long walks.</td></tr>
</tbody></table></div>
<p class="fine">The city sets the beach dates each year. Dates for 2027 hadn’t been announced in November 2026.</p>

<h2>What changes when you rent a house in Izu?</h2>
<p>A house turns a short visit into an ordinary week. A hotel room is built around one or two nights and a set dinner time, while a house gives you a kitchen, a washing machine and a table to work at. A typical day ends up as work in the morning, the beach or a hot spring in the afternoon, and dinner at home when you don’t feel like going out.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, about ten minutes on foot from Izukyu-Shimoda Station.]]
<p>If you’d like to try that in Shimoda, our home there, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, has a work desk, a washing machine and dryer, a properly equipped kitchen and self check-in with a smart lock. It’s about ten minutes on foot from Izukyu-Shimoda Station, with restaurants, a convenience store and a supermarket close by.</p>
<p>If a week in Izu gets you thinking about a longer stay, or even a house of your own, here’s why we suggest [[l:akiya-try-first|living in a town for a month before buying a house]].</p>
[[ed:Add the measured Wi-Fi speed and the time of the last bus from the beaches.]]

<h2>What are the downsides of staying in Izu?</h2>
<p>Getting around takes a bit of planning. The direct trains from Tokyo leave in a fairly narrow window, roughly 9:00 to 13:00 in the October–November 2026 timetable [[s:jre_izu_tt]], so your arrival time is partly decided for you. Once you’re there, beaches and villages outside the main towns are reached by local bus, and it’s worth looking at the timetable before you set out. If you want to hop between beaches, we find an e-bike or a rental car makes life much easier.</p>
""",
 "faq": [
   ("How long does it take to get from Tokyo to Shimoda?",
    "JR East gives 2 hours 49 minutes on the direct Odoriko limited express to Izukyu-Shimoda (as of November 2026) [[s:jre_izu]]."),
   ("Can I use the Japan Rail Pass to get to Izu?",
    "Partly. It covers the JR sections, but you pay extra on the Izu Kyuko line south of Ito, and the Izuhakone Railway to Shuzenji is a separate fare [[s:jg6305]]. The JR Tokyo Wide Pass does cover the Izu Kyuko line’s limited expresses [[s:jre_widepass]]."),
   ("What’s the best way to get to Shuzenji?",
    "Most people take the Shinkansen to Mishima and then the Izuhakone Railway, about 35 minutes [[s:jg6311]]. Direct Odoriko trains run too, but only a few a day [[s:jre_izu_tt]]."),
   ("Do I need a car on the Izu Peninsula?",
    "Not to get to Shimoda or Shuzenji. You’ll only really miss one when you want to move between beaches."),
 ],
 "sources": ["jre_izu", "jre_odoriko", "jre_izu_tt", "jre_tt_local", "jre_fare2026", "jre_widepass", "jrp_price", "jg6305", "jg6311",
             "jg6304", "jnto", "uncharted", "izu_tokko", "shimoda_ohama", "shimoda_beach2026", "shimoda_beach2026b", "pref"],
 "related": ["kinmedai", "izu"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・パスと、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りにはつらく、1週間ならちょうどいい距離です。電車での行き方、使えるパス、いつ行くか、そして知っておきたい弱点をまとめました。",
  "review": [
   "【2026-11-15 品質保証部の指摘を受けた書き直し】変えた点: ①所要時間を JR東日本の公式の値に直しました（下田 2時間35分→2時間49分、伊東 約1時間40分。2026年11月時点） ②運賃は一次の出典で確かめられなかったので、表から数字を外し、黄色い枠で「えきねっとで確認」を人に回しました（二次のサイトの値は枠の中に書いてあります）。2026年3月14日に JR東日本が運賃を改定したことは本文に書きました ③行き方を比べる表にしました（直通の踊り子／新幹線で熱海へ出て乗り換え／修善寺は新幹線で三島へ出て伊豆箱根鉄道／修善寺への直通の踊り子） ④修善寺は「新幹線＋伊豆箱根鉄道がふつう、直通の踊り子は1日3本ほど」と主従を入れ替えました ⑤パスの節を新しく足し、JR東京ワイド・パス（16,000円・連続3日・外国のパスポートの人だけ・伊豆急行の特急も対象。JR東日本）と、ジャパン・レール・パス（7日間 オンライン50,000円・海外の代理店53,000円。2026年4月9日の JR グループのお知らせ）を表にしました ⑥修善寺の足湯: 「無料の足湯がある」→「独鈷の湯は見学のみ。足を入れられるのは杉の湯（無料）と河原湯」（伊豆市） ⑦「夏以外は店が早く閉まる」「配車アプリは使いにくい」を消しました（出典で確かめられないため）。「直通は午前〜昼過ぎ」は JR東日本の2026年10〜11月の時刻表の範囲（9時〜13時ごろ発）に直しました ⑧海水浴の期間を「2026年は7月18日〜8月30・31日、時間外と期間外は監視員なし」と年を付けて、下田市と観光協会の出典にしました ⑨NODE Shimoda の「まさにこういう滞在のために整えた」をやめ、「下田で試すなら」という控えめな紹介にしました ⑩高速バスは、直行便を確かめられなかったので書いていません ⑪title・h1 の「Fares」を「Passes」に変えました（運賃の数字を表に入れられなかったため）",
   "【人に確かめてほしい点】①えきねっとで、東京→熱海・伊東・修善寺・伊豆急下田の片道（大人・普通車指定席）の運賃を確認し、表に入れるか（黄色い枠） ②直通の踊り子の本数（下田行き・修善寺行き）と、東京→熱海・三島の新幹線の所要時間（黄色い枠） ③ワイド・パスで東海道新幹線・伊豆箱根鉄道が対象外か、伊豆箱根鉄道の三島〜修善寺の運賃（550円）が2026年に変わったか（黄色い枠） ④回線速度の実測値と、浜からの最終バスの時刻（黄色い枠） ⑤白浜までバスで約15分は JNTO の記載で、2026年のダイヤでは確かめていません ⑥時刻・パスの値段は変わりやすいので、公開の直前にもう一度確かめてください ⑦出典はリサーチ部が検索で確認したもので、本文のページは開けていません。公開前にページを開いて照合してください",
   "【入れられなかったこと】運賃の数字（一次で未確認）、高速バス（東京・新宿から下田への直行便を確かめられず）、サフィール踊り子の料金、季節で閉まる店の話（出典なし。運営者として確かな体験があれば experience.md に足してから）",
  ],
  "points": [
    "JR東日本によると、東京から下田までは直通の特急「踊り子」で2時間49分（2026年11月時点）。日帰りだと、電車に5時間以上乗ることになります。",
    "修善寺へは、新幹線で三島へ出て、伊豆箱根鉄道で約35分がふつうの行き方です。直通の列車は1日に数本しかありません。",
    "JR東京ワイド・パス（16,000円・3日間・外国のパスポートの人だけ）なら、伊豆急行線の特急にも乗れます。ジャパン・レール・パスは、伊東より南の区間には使えません。",
    "2026年、下田の海水浴場は7月18日から8月末まで開いていました。監視員がいるのは、正式な期間の間だけです。",
  ],
  "body": """
<h2>東京から伊豆半島への行き方</h2>
<p>いちばん簡単なのは、特急「踊り子」です。東京から[[l:izu|伊豆半島]]の東海岸を下田まで、乗り換えなしで走ります。JR東日本によると、下田まで2時間49分、伊東まで約1時間40分です（2026年11月時点）[[s:jre_izu]]。ほかにも、知っておくと便利な行き方があります。修善寺へ行くなら特にそうです。</p>
<div class="tablewrap"><table>
<thead><tr><th>行き方</th><th>乗り換え</th><th>所要時間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>直通の「踊り子」</strong>で伊東・伊豆急下田へ</td><td>なし</td><td>伊東まで約1時間40分、下田まで2時間49分[[s:jre_izu]]</td><td>2026年10〜11月は、東京を9時〜13時ごろに出る列車でした[[s:jre_izu_tt]]。</td></tr>
<tr><td><strong>新幹線で熱海</strong>へ出て、普通列車で下田へ</td><td>1回（熱海）</td><td>新幹線の時間＋熱海から約1時間40〜50分[[s:jre_tt_local]]</td><td>直通より速くはありませんが、直通の時間が合わないときに便利です。</td></tr>
<tr><td><strong>新幹線で三島</strong>へ出て、伊豆箱根鉄道で修善寺へ</td><td>1回（三島）</td><td>三島から約35分[[s:jg6311]]</td><td>修善寺へのふつうの行き方です。</td></tr>
<tr><td><strong>直通の「踊り子」</strong>で修善寺へ</td><td>なし</td><td>2時間余り[[s:jre_izu_tt]]</td><td>2026年10〜11月の時刻表では、1日3本ほどです。</td></tr>
</tbody></table></div>
<p class="fine">時間は JR東日本のサイトと時刻表によります（2026年11月に確認）。</p>
[[ed:JR東日本の伊豆方面特急の時刻表 PDF（2026年10〜11月）で、東京発の下田行き・修善寺行きの直通の本数を数え、東京から熱海・三島までの新幹線の所要時間を足してください。]]
<p>運賃は、いったん表から外しています。JR東日本は2026年3月14日に運賃を改定していて[[s:jre_fare2026]]、改定後の合計を公式の出典でまだ確かめられていないためです。乗る日の正確な運賃は、JR東日本の予約サイト「えきねっと」で分かります。</p>
[[ed:えきねっとで、2026年11月時点の東京→熱海・伊東・修善寺・伊豆急下田の片道（大人・普通車指定席）の運賃を確認してください。二次のサイトでは 3,670円・4,000円・4,750円・6,660円。一致したら、確認した日を添えて表に入れてください。]]

<h2>伊豆へ行くのに、ジャパン・レール・パスや JR東京ワイド・パスは使えるか</h2>
<p>使えます。ただ、使える範囲がそれぞれ違うので、行き先しだいです。</p>
<div class="tablewrap"><table>
<thead><tr><th>パス</th><th>値段と日数</th><th>伊豆で使える範囲</th></tr></thead>
<tbody>
<tr><td><strong>JR東京ワイド・パス</strong></td><td>大人16,000円、連続3日間、外国のパスポートを持つ人だけ（2026年3月14日から）[[s:jre_widepass]]</td><td>エリア内の JR東日本の路線と、下田までの伊豆急行線の特急[[s:jre_widepass]]</td></tr>
<tr><td><strong>ジャパン・レール・パス</strong></td><td>7日間で、オンラインで円で買うと50,000円、海外の代理店では53,000円（2026年4月9日の JR グループのお知らせ）[[s:jrp_price]]</td><td>JR の区間。伊東より南の伊豆急行線は別料金です[[s:jg6305]]。</td></tr>
</tbody></table></div>
<p>三島から修善寺までの伊豆箱根鉄道は JR ではないので、ジャパン・レール・パスでは別に運賃を払います。japan-guide によると550円です[[s:jg6305]]。</p>
[[ed:JR東日本のワイド・パスのページで、東海道新幹線と伊豆箱根鉄道が対象外と明記されているか、伊豆箱根鉄道の三島〜修善寺の運賃が2026年に変わったかを確かめてください。]]

<h2>伊豆半島は、東京から日帰りできるか</h2>
<p>北のほうはできますが、南はあまり向きません。直通の電車でも下田まで2時間49分かかるので[[s:jre_izu]]、往復すると、浜で過ごす数時間のために5時間半以上電車に乗ることになります。東京に近い熱海や伊東なら、日帰りでも十分楽しめます。南の海岸と内陸の温泉町は、泊まったほうがずっと楽しめると私たちは思います。</p>

<h2>伊豆のどの町が合うか</h2>
<p>決め手は、どこまで行きたいかと、どれくらいいられるかです。</p>
<div class="tablewrap"><table>
<thead><tr><th>町</th><th>東京から</th><th>どんな町か</th><th>日帰りか、泊まりか</th></tr></thead>
<tbody>
<tr><td><strong>熱海と伊東</strong></td><td>伊東まで約1時間40分。熱海はもっと近い</td><td>東京に最も近く、いちばんにぎやか。ホテルも最も多い町です。</td><td>日帰りでも楽しめる</td></tr>
<tr><td><strong>修善寺</strong></td><td>三島から約35分、または直通で2時間余り</td><td>川沿いに広がる内陸の温泉町で、竹林や寺があります[[s:uncharted]]。有名な「独鈷の湯」は見るだけの湯です。足を入れたいなら、近くに無料の足湯「杉の湯」と「河原湯」があります[[s:izu_tokko]]。</td><td>泊まるのがおすすめ</td></tr>
<tr><td><strong>下田</strong></td><td>直通で2時間49分</td><td>白い砂浜のある港町。JNTO によると、白浜海岸は駅からバスで約15分です[[s:jnto]]。下田市と静岡県は、[[l:ja-kinmedai|金目鯛]]の水揚げ日本一の港と説明しています[[s:pref]]。</td><td>泊まるのがおすすめ</td></tr>
</tbody></table></div>
<p class="fine">時間は上の行き方の表によります。</p>

<h2>伊豆半島はいつ行くのがいいか</h2>
<p>泳ぐなら7月中旬から8月末。静かに過ごしたいなら、私たちはその前後の月を選びます。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>どんな感じか</th></tr></thead>
<tbody>
<tr><td>海水浴の期間（2026年は7月18日〜8月30・31日）</td><td>下田の海水浴場が開き、監視員がいます。白浜大浜海水浴場は7月18日〜8月31日の8時〜16時、白浜中央海水浴場は8月30日まででした[[s:shimoda_ohama,shimoda_beach2026,shimoda_beach2026b]]。期間外と時間外は、監視員がいません[[s:shimoda_ohama]]。</td></tr>
<tr><td>5月下旬〜9月</td><td>天気がよければ海は気持ちよく[[s:jg6304]]、学校の休み以外は人も少なめです。</td></tr>
<tr><td>それ以外</td><td>町はぐっと静かになります。温泉や長い散歩には、いちばん過ごしやすい時期だと私たちは思います。</td></tr>
</tbody></table></div>
<p class="fine">海水浴場の期間は、市が毎年決めます。2027年の期間は、2026年11月の時点ではまだ発表されていませんでした。</p>

<h2>伊豆で家を借りると、何が変わるか</h2>
<p>家を借りると、短い旅が、ふだんの1週間に変わります。ホテルの部屋は1〜2泊と決まった夕食の時間が前提ですが、家ならキッチン、洗濯機、仕事ができる机があります。午前は仕事、午後は浜か温泉、出かける気分でない夜は家で夕食。だいたいそんな一日になります。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて約10分の「NODE Shimoda」のリビング。]]
<p>下田で試してみたいなら、私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」には、ワークデスク、洗濯機と乾燥機、調理器具のそろったキッチンがあり、スマートロックでセルフチェックインできます。伊豆急下田駅から歩いて約10分で、飲食店、コンビニ、スーパーもすぐ近くです。</p>
<p>伊豆で1週間過ごして、もっと長く住むことや、自分の家を持つことが気になり始めたら、[[l:ja-akiya-try-first|家を買う前に1か月その町に住む]]ことをすすめる理由も読んでみてください。</p>
[[ed:回線速度の実測値と、浜からの最終バスの時刻を入れてください。]]

<h2>伊豆に泊まる弱点は何か</h2>
<p>移動には、少し計画が要ります。東京からの直通列車が出る時間帯はわりと狭く、2026年10〜11月の時刻表では9時〜13時ごろでした[[s:jre_izu_tt]]。着く時間は、ある程度それで決まってしまいます。着いてからも、大きな町の外の浜や集落へは路線バスで行くことになるので、出かける前に時刻表を見ておくと安心です。浜から浜へ移動したいなら、電動自転車かレンタカーがあると、ぐっと動きやすくなると私たちは感じています。</p>
""",
  "faq": [
    ("東京から下田まで、何時間かかりますか",
     "JR東日本によると、直通の特急「踊り子」で伊豆急下田まで2時間49分です（2026年11月時点）[[s:jre_izu]]。"),
    ("伊豆へ行くのに、ジャパン・レール・パスは使えますか",
     "一部で使えます。JR の区間は対象ですが、伊東より南の伊豆急行線は別料金で、修善寺までの伊豆箱根鉄道も別の運賃です[[s:jg6305]]。JR東京ワイド・パスなら、伊豆急行線の特急にも乗れます[[s:jre_widepass]]。"),
    ("修善寺へは、どう行くのがいいですか",
     "多くの人は、新幹線で三島へ出て、伊豆箱根鉄道で約35分です[[s:jg6311]]。直通の「踊り子」もありますが、1日に数本です[[s:jre_izu_tt]]。"),
    ("伊豆半島で車は必要ですか",
     "下田や修善寺へ行くだけなら要りません。車がほしくなるのは、浜から浜へ移動したいときくらいです。"),
  ],
 },
}
