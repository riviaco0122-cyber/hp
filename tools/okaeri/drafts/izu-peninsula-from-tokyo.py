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
    "shimoda_beach2026_city": ("https://city.shimoda.shizuoka.jp/file/広報しもだ令和8年8月号2-3頁.pdf", "Shimoda City newsletter, August 2026",
                               "広報しもだ 2026年8月号", "Shimoda City newsletter, August 2026: beaches open in Shimoda"),
    "jre_tt_kodama": ("https://timetables.jreast.co.jp/2610/train/175/177601.html", "JR East timetable, October 2026",
                      "JR東日本 時刻表（2026年10月）", "JR East: Shinkansen Kodama (Mishima–Atami–Tokyo) stops and times"),
    "mlit_izuhakone2026": ("https://wwwtb.mlit.go.jp/chubu/press/pdf/tethudo20261016.pdf", "Chubu District Transport Bureau (MLIT)",
                           "国土交通省中部運輸局", "Chubu District Transport Bureau: Izuhakone Railway fare-ceiling application (16 October 2026)"),
    "mlit_izuhakone2022": ("https://wwwtb.mlit.go.jp/kanto/content/000284727.pdf", "Chubu District Transport Bureau (MLIT)",
                           "国土交通省中部運輸局", "Chubu District Transport Bureau: Approval of Izuhakone Railway fare revision (26 December 2022)"),
}

ARTICLE = {
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-15",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, passes and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Passes and Where to Stay",
 "description": "The direct Odoriko takes 2 h 49 min from Tokyo to Shimoda, and the JR Tokyo Wide Pass covers it. For Shuzenji, change at Mishima. Stay a week, not a day.",
 "dek": "The south of the Izu Peninsula is too far for a comfortable day trip and just right for a week. The direct Odoriko gets you from Tokyo to Shimoda in 2 hours 49 minutes, and the JR Tokyo Wide Pass covers the whole ride.",
 "card": "The direct Odoriko, the Shinkansen routes via Atami and Mishima, the JR Tokyo Wide Pass and the Japan Rail Pass, and which Izu town to stay in. As of November 2026.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—")],
 "intent": "Do（やり方を知りたい）",
 "points": [
   "The direct Odoriko limited express takes 2 hours 49 minutes from Tokyo to Shimoda, according to JR East (as of November 2026). A day trip there means more than five hours on the train.",
   "For Shuzenji, most people take the Shinkansen to Mishima, about 51 to 54 minutes on a Kodama, and then the Izuhakone Railway, about 35 minutes. In October–November 2026 there were three direct trains a day.",
   "The JR Tokyo Wide Pass (¥16,000 for three days, foreign passports only) covers the Izu Kyuko line’s limited expresses. The Japan Rail Pass doesn’t cover the line south of Ito.",
   "In 2026, Shimoda’s nine official beaches opened on 18 July. Most closed on 23 August, Shirahama Chuo on 30 August, and Shirahama Ohama and Kujukihama on 31 August. Lifeguards are only there in the season.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The simplest way is the Odoriko limited express, which runs from Tokyo down the east coast of the [[l:izu|Izu Peninsula]] to Shimoda without a change. JR East gives the journey as 2 hours 49 minutes and Ito as about 1 hour 40 minutes (as of November 2026) [[s:jre_izu]]. There are a couple of other routes worth knowing, especially for Shuzenji.</p>
<div class="tablewrap"><table>
<thead><tr><th>Route</th><th>Changes</th><th>Time</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Direct Odoriko</strong> to Ito and Izukyu-Shimoda</td><td>None</td><td>About 1 h 40 min to Ito, 2 h 49 min to Shimoda [[s:jre_izu]]</td><td>In the October–November 2026 timetable, the regular trains leave Tokyo between 9:00 and about 13:00, with extra trains on set days [[s:jre_izu_tt]].</td></tr>
<tr><td><strong>Shinkansen to Atami</strong>, then a local train to Shimoda</td><td>One, at Atami</td><td>About 47 min to Atami by Kodama [[s:jre_tt_kodama]], then about 1 h 40 min to 1 h 50 min to Shimoda [[s:jre_tt_local]]</td><td>It isn’t faster than the direct train, but it helps when the direct times don’t suit you.</td></tr>
<tr><td><strong>Shinkansen to Mishima</strong>, then the Izuhakone Railway to Shuzenji</td><td>One, at Mishima</td><td>51 to 54 min to Mishima by Kodama [[s:jre_tt_kodama]], then about 35 min to Shuzenji [[s:jg6311]]</td><td>The usual way to Shuzenji.</td></tr>
<tr><td><strong>Direct Odoriko</strong> to Shuzenji</td><td>None</td><td>A little over 2 h [[s:jre_izu_tt]]</td><td>Three a day in October–November 2026, leaving Tokyo at 9:00, 10:30 and 12:00 [[s:jre_izu_tt]].</td></tr>
</tbody></table></div>
<p class="fine">Times are from JR East’s website and timetables, checked in November 2026.</p>
[[ed:In JR East’s Izu timetable PDF (1 October–30 November 2026), confirm every direct departure from Tokyo to Shimoda, that no regular direct train leaves after about 13:00, and that there are three direct trains to Shuzenji (9:00, 10:30, 12:00). The 13:00 departure is only on an unofficial list.]]
<p>JR East revised its fares on 14 March 2026 [[s:jre_fare2026]], so older fare tables online may be out of date. JR East’s Ekinet booking site shows the exact fare for your date and seat.</p>
[[ed:On Ekinet, check the one-way adult fare with a reserved seat, as of November 2026, from Tokyo to Atami, Ito, Shuzenji and Izukyu-Shimoda. Secondary sites give ¥3,670, ¥4,000, ¥4,750 and ¥6,660. Add them to the table only if they match, with the date checked.]]

<h2>Can you use the Japan Rail Pass or the JR Tokyo Wide Pass to get to Izu?</h2>
<p>Yes, but they don’t reach the same places, so it depends on where you’re going.</p>
<div class="tablewrap"><table>
<thead><tr><th>Pass</th><th>Price and length</th><th>What it covers in Izu</th></tr></thead>
<tbody>
<tr><td><strong>JR Tokyo Wide Pass</strong></td><td>¥16,000 for adults, three days in a row, foreign passport holders only, from 14 March 2026 [[s:jre_widepass]]</td><td>JR East lines in its area, including limited expresses on the Izu Kyuko line to Shimoda [[s:jre_widepass]]</td></tr>
<tr><td><strong>Japan Rail Pass</strong></td><td>¥50,000 for seven days when bought online in yen, ¥53,000 through overseas agents (JR Group notice, 9 April 2026) [[s:jrp_price]]</td><td>The JR sections. You pay extra on the Izu Kyuko line south of Ito [[s:jg6305]].</td></tr>
</tbody></table></div>
<p>The Izuhakone Railway from Mishima to Shuzenji isn’t a JR line, so on the Japan Rail Pass you pay that fare separately. It’s ¥550 as of November 2026, the fare since April 2023 [[s:jg6305,mlit_izuhakone2022]]. The railway applied in October 2026 to raise its fares, with the change on this line planned for spring 2027 if it’s approved [[s:mlit_izuhakone2026]].</p>
[[ed:Confirm on JR East’s Tokyo Wide Pass page whether the Tokaido Shinkansen and the Izuhakone Railway are excluded. Confirm in the Chubu District Transport Bureau papers (16 October 2026) that the Mishima–Shuzenji change is planned for spring 2027.]]

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is, but the south really isn’t. With Shimoda 2 hours 49 minutes away on the direct train [[s:jre_izu]], a return trip means more than five and a half hours on the train for a few hours on the beach. Atami and Ito are closer to Tokyo and work fine as day trips. We think the south coast and the inland hot-spring towns are far better if you stay.</p>

<h2>Which Izu town suits you?</h2>
<p>It mostly comes down to how far you want to go and how long you can stay.</p>
<div class="tablewrap"><table>
<thead><tr><th>Town</th><th>From Tokyo</th><th>What it’s like</th><th>Day trip or stay?</th></tr></thead>
<tbody>
<tr><td><strong>Atami and Ito</strong></td><td>Atami about 47 min by Shinkansen; Ito about 1 h 40 min direct</td><td>The two towns nearest Tokyo, on the east coast. We think they’re the ones that work as a day out, since you can see the sea and soak in a hot spring and still be home for dinner.</td><td>A day trip works</td></tr>
<tr><td><strong>Shuzenji</strong></td><td>51–54 min to Mishima, then about 35 min; or a little over 2 h direct</td><td>An inland hot-spring town along a river [[s:uncharted]]. Its best-known spring, Tokko-no-yu, is for looking at only, but you can put your feet in the free Sugi-no-yu foot bath or at Kawara-yu nearby [[s:izu_tokko]]. We think it suits a quiet night or two more than a rushed visit.</td><td>Better to stay</td></tr>
<tr><td><strong>Shimoda</strong></td><td>2 h 49 min direct</td><td>A port town at the southern tip, with nine official swimming beaches in 2026 [[s:shimoda_beach2026_city]]. JNTO puts Shirahama Beach about 15 minutes by bus from the station [[s:jnto]], and the prefecture describes the harbour as Japan’s top landing port for [[l:kinmedai|kinmedai]] [[s:pref]]. In our view, it’s the town that suits a week best.</td><td>Better to stay</td></tr>
</tbody></table></div>
<p class="fine">Times are from the route table above.</p>

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>For swimming, it’s mid-July to late August. For a quieter stay, we’d pick the months either side.</p>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Swimming season (in 2026, from 18 July to between 23 and 31 August, depending on the beach)</td><td>All nine of Shimoda’s official beaches opened on 18 July 2026, mostly from 8:00 to 16:00. Shirahama Ohama and Kujukihama stayed open until 31 August and Shirahama Chuo until 30 August, but the other six closed on 23 August [[s:shimoda_beach2026_city]]. Outside the season and those hours, there are no lifeguards [[s:shimoda_ohama]].</td></tr>
<tr><td>Late May to September</td><td>In good weather the sea is pleasant [[s:jg6304]], and outside the school holidays there are fewer people around.</td></tr>
<tr><td>The rest of the year</td><td>The towns get much quieter. In our view, it’s the easiest time for hot springs and long walks.</td></tr>
</tbody></table></div>
<p class="fine">The city sets the beach dates each year, so if you’re planning a late-August trip, it’s worth checking which beaches will still be open. Dates for 2027 hadn’t been announced in November 2026.</p>

<h2>What changes when you rent a house in Izu?</h2>
<p>A house turns a short visit into an ordinary week. A hotel room is built around one or two nights and a set dinner time, while a house gives you a kitchen, a washing machine and a table to work at. A typical day ends up as work in the morning, the beach or a hot spring in the afternoon, and dinner at home when you don’t feel like going out.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, about ten minutes on foot from Izukyu-Shimoda Station.]]
<p>If you’d like to try that in Shimoda, our home there, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, has a work desk, a washing machine and dryer, a properly equipped kitchen and self check-in with a smart lock. It’s about ten minutes on foot from Izukyu-Shimoda Station, with restaurants, a convenience store and a supermarket close by.</p>
<p>If a week in Izu gets you thinking about a longer stay, or even a house of your own, here’s why we suggest [[l:akiya-try-first|living in a town for a month before buying a house]].</p>
[[ed:Add the measured Wi-Fi speed and the time of the last bus from the beaches.]]

<h2>What are the downsides of staying in Izu?</h2>
<p>Getting around takes a bit of planning. The regular direct trains from Tokyo leave in the morning and around midday, from 9:00 to about 13:00 in the October–November 2026 timetable [[s:jre_izu_tt]]. It’s worth building your travel day around them. If they don’t fit, you can take the Shinkansen to Atami and change there. Once you’re in Izu, beaches and villages outside the main towns are reached by local bus, and it’s worth looking at the timetable before you set out. If you want to hop between beaches, we think an e-bike or a rental car makes life much easier.</p>
""",
 "faq": [
   ("How long does it take to get from Tokyo to Shimoda?",
    "JR East gives 2 hours 49 minutes on the direct Odoriko limited express to Izukyu-Shimoda (as of November 2026) [[s:jre_izu]]."),
   ("Can I use the Japan Rail Pass to get to Izu?",
    "Partly. It covers the JR sections, but you pay extra on the Izu Kyuko line south of Ito, and the Izuhakone Railway to Shuzenji is a separate fare [[s:jg6305]]. The JR Tokyo Wide Pass does cover the Izu Kyuko line’s limited expresses [[s:jre_widepass]]."),
   ("What’s the best way to get to Shuzenji?",
    "Most people take the Shinkansen to Mishima, 51 to 54 minutes on a Kodama [[s:jre_tt_kodama]], and then the Izuhakone Railway, about 35 minutes [[s:jg6311]]. Direct Odoriko trains run too, three a day in October–November 2026 [[s:jre_izu_tt]]."),
   ("Do I need a car on the Izu Peninsula?",
    "Not to get to Shimoda or Shuzenji. You’ll only really miss one when you want to move between beaches."),
 ],
 "sources": ["jre_izu", "jre_odoriko", "jre_izu_tt", "jre_tt_local", "jre_fare2026", "jre_widepass", "jrp_price", "jg6305", "jg6311",
             "jg6304", "jnto", "uncharted", "izu_tokko", "shimoda_ohama", "shimoda_beach2026_city", "jre_tt_kodama", "mlit_izuhakone2022",
             "mlit_izuhakone2026", "pref"],
 "related": ["kinmedai", "izu"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・パスと、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りにはつらく、1週間ならちょうどいい距離です。東京から下田までは直通の特急「踊り子」で2時間49分。JR東京ワイド・パスなら、その全区間に乗れます。",
  "review": [
   "【2026-11-15 2回目の書き直し】変えた点: ①海水浴場の期間を浜ごとに正確にしました（2026年は9つの浜がすべて7月18日に開設。白浜大浜・九十浜は8月31日、白浜中央は8月30日まで、ほかの6つは8月23日に終了）。出典を観光協会（開けていない）から下田市の広報 2026年8月号（リサーチ部が PDF を開いて確認）に替えました。In short・本文・日本語版とも同じです ②直通の時間帯は「狭い時間帯」「9〜13時」と言い切るのをやめ、「2026年10〜11月の時刻表で、定期の列車は東京を9時〜13時ごろに出る。ほかに決まった日に走る列車もある」に弱め、全列車の確認を黄色い枠で人に回しました ③修善寺への直通は「2026年10〜11月は1日3本（東京9:00・10:30・12:00発）」にしました（黄色い枠で確認を依頼） ④新幹線の所要時間を行き方の表に入れました（こだまで東京〜熱海 約47分、東京〜三島 51〜54分。JR東日本の時刻表） ⑤伊豆箱根鉄道の550円に「2026年11月時点・2023年4月からの運賃」と、「2026年10月に値上げを申請し、認められれば三島〜修善寺は2027年春に変わる予定」を添えました（国土交通省中部運輸局）。新しい額（650円）は二次の情報なので書いていません ⑥町の表を、出典つきの事実と「私たちの見方」に分けて書き直しました（熱海・伊東＝日帰り向きだと思う、修善寺＝1〜2泊で静かに過ごすのが合うと思う、下田＝1週間にいちばん合う町だと思う）。下田は「2026年に正式な海水浴場が9つ」を足しました ⑦「電動自転車かレンタカー」を「私たちは思う」の見解の形にしました ⑧「運賃を公式の出典でまだ確かめられていない」「直行の高速バスは見つからなかった」のような調べた過程の話を本文から消し、高速バスには触れていません ⑨dek・description が中身の目次（how to get there, which passes…）を読み上げていたので、答え（直通で2時間49分・ワイド・パスで乗れる・修善寺は三島で乗り換え・1週間泊まる）に置き換えました",
   "【人に確かめてほしい点】①運賃: えきねっとで、東京→熱海・伊東・修善寺・伊豆急下田の片道（大人・普通車指定席、2026年11月時点）を確認し、表に入れるか（黄色い枠。二次のサイトでは 3,670円・4,000円・4,750円・6,660円） ②JR東日本の伊豆方面特急の時刻表 PDF（2026年10〜11月）で、東京発の下田行きの直通の全列車、13時ごろより後に定期の直通が無いこと、修善寺行きが3本（9:00・10:30・12:00）であること（黄色い枠。13:00発は非公式の一覧でしか確かめられていません） ③ワイド・パスで東海道新幹線・伊豆箱根鉄道が対象外か。伊豆箱根鉄道の値上げが三島〜修善寺で2027年春の予定か（中部運輸局の資料。黄色い枠） ④回線速度の実測値と、浜からの最終バスの時刻（黄色い枠） ⑤白浜までバスで約15分は JNTO の記載で、2026年のダイヤでは確かめていません ⑥新幹線・踊り子の時刻、伊豆箱根鉄道の運賃は、リサーチ部が検索の抜粋で確かめたもので、ページは開けていません。公開の直前に開ける環境で照合してください ⑦町の表の「私たちの見方」（熱海・伊東は日帰り向き、修善寺は1〜2泊、下田は1週間）が、運営者の感覚と合っているか",
   "【入れられなかったこと】運賃の数字（一次で未確認）。高速バス（東京から下田方面のバスを公式で確かめられなかったので、本文では触れていません）。伊豆箱根鉄道の値上げ後の額（二次の情報のみ）。ひかりの所要時間（二次の情報のみ）",
  ],
  "points": [
    "JR東日本によると、東京から下田までは直通の特急「踊り子」で2時間49分（2026年11月時点）。日帰りだと、電車に5時間以上乗ることになります。",
    "修善寺へは、新幹線（こだまで東京〜三島 51〜54分）で三島へ出て、伊豆箱根鉄道で約35分がふつうの行き方です。直通の列車は、2026年10〜11月は1日3本でした。",
    "JR東京ワイド・パス（16,000円・3日間・外国のパスポートの人だけ）なら、伊豆急行線の特急にも乗れます。ジャパン・レール・パスは、伊東より南の区間には使えません。",
    "2026年、下田の9つの海水浴場は7月18日に開きました。多くは8月23日に閉じ、白浜中央は8月30日、白浜大浜と九十浜は8月31日まで。監視員がいるのは期間中だけです。",
  ],
  "body": """
<h2>東京から伊豆半島への行き方</h2>
<p>いちばん簡単なのは、特急「踊り子」です。東京から[[l:izu|伊豆半島]]の東海岸を下田まで、乗り換えなしで走ります。JR東日本によると、下田まで2時間49分、伊東まで約1時間40分です（2026年11月時点）[[s:jre_izu]]。ほかにも、知っておくと便利な行き方があります。修善寺へ行くなら特にそうです。</p>
<div class="tablewrap"><table>
<thead><tr><th>行き方</th><th>乗り換え</th><th>所要時間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>直通の「踊り子」</strong>で伊東・伊豆急下田へ</td><td>なし</td><td>伊東まで約1時間40分、下田まで2時間49分[[s:jre_izu]]</td><td>2026年10〜11月の時刻表では、定期の列車は東京を9時〜13時ごろに出ます。ほかに、決まった日に走る列車もあります[[s:jre_izu_tt]]。</td></tr>
<tr><td><strong>新幹線で熱海</strong>へ出て、普通列車で下田へ</td><td>1回（熱海）</td><td>こだまで熱海まで約47分[[s:jre_tt_kodama]]、熱海から下田まで約1時間40〜50分[[s:jre_tt_local]]</td><td>直通より速くはありませんが、直通の時間が合わないときに便利です。</td></tr>
<tr><td><strong>新幹線で三島</strong>へ出て、伊豆箱根鉄道で修善寺へ</td><td>1回（三島）</td><td>こだまで三島まで51〜54分[[s:jre_tt_kodama]]、三島から修善寺まで約35分[[s:jg6311]]</td><td>修善寺へのふつうの行き方です。</td></tr>
<tr><td><strong>直通の「踊り子」</strong>で修善寺へ</td><td>なし</td><td>2時間余り[[s:jre_izu_tt]]</td><td>2026年10〜11月は1日3本で、東京を9:00・10:30・12:00に出ます[[s:jre_izu_tt]]。</td></tr>
</tbody></table></div>
<p class="fine">時間は JR東日本のサイトと時刻表によります（2026年11月に確認）。</p>
[[ed:JR東日本の伊豆方面特急の時刻表 PDF（2026年10月1日〜11月30日）で、東京発の下田行きの直通の全列車と、13時ごろより後に定期の直通が無いこと、修善寺行きの直通が3本（9:00・10:30・12:00発）であることを確かめてください。13:00発は非公式の一覧でしか確かめられていません。]]
<p>JR東日本は2026年3月14日に運賃を改定したので[[s:jre_fare2026]]、ネットにある古い運賃表は当てにならないことがあります。乗る日・席の正確な運賃は、JR東日本の予約サイト「えきねっと」で分かります。</p>
[[ed:えきねっとで、2026年11月時点の東京→熱海・伊東・修善寺・伊豆急下田の片道（大人・普通車指定席）の運賃を確認してください。二次のサイトでは 3,670円・4,000円・4,750円・6,660円。一致したら、確認した日を添えて表に入れてください。]]

<h2>伊豆へ行くのに、ジャパン・レール・パスや JR東京ワイド・パスは使えるか</h2>
<p>使えます。ただ、使える範囲がそれぞれ違うので、行き先しだいです。</p>
<div class="tablewrap"><table>
<thead><tr><th>パス</th><th>値段と日数</th><th>伊豆で使える範囲</th></tr></thead>
<tbody>
<tr><td><strong>JR東京ワイド・パス</strong></td><td>大人16,000円、連続3日間、外国のパスポートを持つ人だけ（2026年3月14日から）[[s:jre_widepass]]</td><td>エリア内の JR東日本の路線と、下田までの伊豆急行線の特急[[s:jre_widepass]]</td></tr>
<tr><td><strong>ジャパン・レール・パス</strong></td><td>7日間で、オンラインで円で買うと50,000円、海外の代理店では53,000円（2026年4月9日の JR グループのお知らせ）[[s:jrp_price]]</td><td>JR の区間。伊東より南の伊豆急行線は別料金です[[s:jg6305]]。</td></tr>
</tbody></table></div>
<p>三島から修善寺までの伊豆箱根鉄道は JR ではないので、ジャパン・レール・パスでは別に運賃を払います。2026年11月時点で550円で、2023年4月からこの運賃です[[s:jg6305,mlit_izuhakone2022]]。鉄道会社は2026年10月に運賃の値上げを申請していて、認められれば、この区間は2027年春に変わる予定です[[s:mlit_izuhakone2026]]。</p>
[[ed:JR東日本のワイド・パスのページで、東海道新幹線と伊豆箱根鉄道が対象外と明記されているかを確かめてください。中部運輸局の資料（2026年10月16日）で、三島〜修善寺の値上げが2027年春の予定かも確かめてください。]]

<h2>伊豆半島は、東京から日帰りできるか</h2>
<p>北のほうはできますが、南はあまり向きません。直通の電車でも下田まで2時間49分かかるので[[s:jre_izu]]、往復すると、浜で過ごす数時間のために5時間半以上電車に乗ることになります。東京に近い熱海や伊東なら、日帰りでも十分楽しめます。南の海岸と内陸の温泉町は、泊まったほうがずっと楽しめると私たちは思います。</p>

<h2>伊豆のどの町が合うか</h2>
<p>決め手は、どこまで行きたいかと、どれくらいいられるかです。</p>
<div class="tablewrap"><table>
<thead><tr><th>町</th><th>東京から</th><th>どんな町か</th><th>日帰りか、泊まりか</th></tr></thead>
<tbody>
<tr><td><strong>熱海と伊東</strong></td><td>熱海まで新幹線で約47分、伊東まで直通で約1時間40分</td><td>東海岸の、東京にいちばん近い2つの町。海を眺めて温泉に入り、夕食には帰れるので、日帰りに向いているのはこの2つだと私たちは思います。</td><td>日帰りでも楽しめる</td></tr>
<tr><td><strong>修善寺</strong></td><td>三島まで51〜54分、そこから約35分。または直通で2時間余り</td><td>川沿いの内陸の温泉町です[[s:uncharted]]。いちばん有名な「独鈷の湯」は見るだけの湯ですが、近くの無料の足湯「杉の湯」や「河原湯」なら足を入れられます[[s:izu_tokko]]。慌ただしく立ち寄るより、1〜2泊して静かに過ごすのが合う町だと私たちは思います。</td><td>泊まるのがおすすめ</td></tr>
<tr><td><strong>下田</strong></td><td>直通で2時間49分</td><td>半島の南端の港町で、2026年は正式な海水浴場が9つありました[[s:shimoda_beach2026_city]]。JNTO によると、白浜海岸は駅からバスで約15分で[[s:jnto]]、静岡県は、この港を[[l:ja-kinmedai|金目鯛]]の水揚げ日本一の港と説明しています[[s:pref]]。1週間過ごすのにいちばん合う町だと、私たちは思います。</td><td>泊まるのがおすすめ</td></tr>
</tbody></table></div>
<p class="fine">時間は上の行き方の表によります。</p>

<h2>伊豆半島はいつ行くのがいいか</h2>
<p>泳ぐなら7月中旬から8月下旬。静かに過ごしたいなら、私たちはその前後の月を選びます。</p>
<div class="tablewrap"><table>
<thead><tr><th>時期</th><th>どんな感じか</th></tr></thead>
<tbody>
<tr><td>海水浴の期間（2026年は7月18日から、浜によって8月23〜31日まで）</td><td>2026年は、下田の9つの海水浴場がすべて7月18日に開き、多くは8時〜16時でした。白浜大浜と九十浜は8月31日まで、白浜中央は8月30日まで開いていましたが、ほかの6つは8月23日に閉じました[[s:shimoda_beach2026_city]]。期間外と時間外は、監視員がいません[[s:shimoda_ohama]]。</td></tr>
<tr><td>5月下旬〜9月</td><td>天気がよければ海は気持ちよく[[s:jg6304]]、学校の休み以外は人も少なめです。</td></tr>
<tr><td>それ以外</td><td>町はぐっと静かになります。温泉や長い散歩には、いちばん過ごしやすい時期だと私たちは思います。</td></tr>
</tbody></table></div>
<p class="fine">海水浴場の期間は、市が毎年決めます。8月の終わりに行くなら、どの浜がまだ開いているか確かめておくと安心です。2027年の期間は、2026年11月の時点ではまだ発表されていませんでした。</p>

<h2>伊豆で家を借りると、何が変わるか</h2>
<p>家を借りると、短い旅が、ふだんの1週間に変わります。ホテルの部屋は1〜2泊と決まった夕食の時間が前提ですが、家ならキッチン、洗濯機、仕事ができる机があります。午前は仕事、午後は浜か温泉、出かける気分でない夜は家で夕食。だいたいそんな一日になります。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて約10分の「NODE Shimoda」のリビング。]]
<p>下田で試してみたいなら、私たちの家「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」には、ワークデスク、洗濯機と乾燥機、調理器具のそろったキッチンがあり、スマートロックでセルフチェックインできます。伊豆急下田駅から歩いて約10分で、飲食店、コンビニ、スーパーもすぐ近くです。</p>
<p>伊豆で1週間過ごして、もっと長く住むことや、自分の家を持つことが気になり始めたら、[[l:ja-akiya-try-first|家を買う前に1か月その町に住む]]ことをすすめる理由も読んでみてください。</p>
[[ed:回線速度の実測値と、浜からの最終バスの時刻を入れてください。]]

<h2>伊豆に泊まる弱点は何か</h2>
<p>移動には、少し計画が要ります。東京からの定期の直通列車は、朝から昼ごろに出ます。2026年10〜11月の時刻表では9時〜13時ごろでした[[s:jre_izu_tt]]。移動の日は、この列車に合わせて組み立てるのがおすすめです。合わなければ、新幹線で熱海まで行って乗り換える手もあります。着いてからも、大きな町の外の浜や集落へは路線バスで行くことになるので、出かける前に時刻表を見ておくと安心です。浜から浜へ移動したいなら、電動自転車かレンタカーがあると、ぐっと動きやすくなると私たちは思います。</p>
""",
  "faq": [
    ("東京から下田まで、何時間かかりますか",
     "JR東日本によると、直通の特急「踊り子」で伊豆急下田まで2時間49分です（2026年11月時点）[[s:jre_izu]]。"),
    ("伊豆へ行くのに、ジャパン・レール・パスは使えますか",
     "一部で使えます。JR の区間は対象ですが、伊東より南の伊豆急行線は別料金で、修善寺までの伊豆箱根鉄道も別の運賃です[[s:jg6305]]。JR東京ワイド・パスなら、伊豆急行線の特急にも乗れます[[s:jre_widepass]]。"),
    ("修善寺へは、どう行くのがいいですか",
     "多くの人は、新幹線で三島へ出て（こだまで51〜54分）[[s:jre_tt_kodama]]、伊豆箱根鉄道で約35分です[[s:jg6311]]。直通の「踊り子」もあり、2026年10〜11月は1日3本でした[[s:jre_izu_tt]]。"),
    ("伊豆半島で車は必要ですか",
     "下田や修善寺へ行くだけなら要りません。車がほしくなるのは、浜から浜へ移動したいときくらいです。"),
  ],
 },
}
