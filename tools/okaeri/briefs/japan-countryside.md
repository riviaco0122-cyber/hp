# 構成案: 日本の田舎に長く滞在する（japan-countryside）

戦略部 2026-11-21。`plan-2026-11.md` の4番「The Japanese countryside for a longer stay」（ROADMAP 7）。新規記事。**Stay longer の柱の記事**（細かい記事へリンクでつなぐ役）。
- 記事データの案: `id: "japan-countryside"`、`slug: "japan-countryside"`、`topic: "stay"`、`also: ["live"]`、`place: None`（特定の場所の記事ではない）
- **1記事1主張**: 「日本の田舎で長めに過ごせるかどうかは、地域の景色より **拠点の選び方** で決まる。駅があり、歩いて行ける店があり、時刻を確かめられるバスがある町を拠点にすれば、車がなくても、日本語ができなくても、数日〜数週間を“暮らすように”過ごせる」。名所の一覧ではなく、選び方の軸と、暮らしの実際（移動・泊まる場所・店・ごみ・病院・言葉・季節）を書く。
- 下田・伊豆は **例の1つ** にとどめる（節2で1文＋リンク、節4で自社の家に1回だけ触れる）。

---

## 1. 狙う検索語

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| **主な語**（`keywords` の先頭） | japan countryside | 9,900 | 6 | `review_ja.py` KEYWORDS（2026-11-14 調査） |
| 関連 | rural japan | 6,600 | 12 | 同上 |
| 関連 | small towns in japan | 1,900 | 7 | 同上（ROADMAP 7 でこの記事が受ける語） |
| 関連（候補） | japanese countryside / countryside japan / rural japan travel | 未調査 | — | 上位の題に多い語。リサーチ部に依頼（R15） |

- `keywords` の案: `[("japan countryside", "9,900", "6"), ("rural japan", "6,600", "12"), ("small towns in japan", "1,900", "7")]`
- title は「Japan Countryside」で始め、後半に「Rural Japan」も入れる（両方の語を自然に入れられる）。
- **共食いの線引き**（品質保証部は `keywords` と h2 で照合する。既存のどの記事とも `keywords` は重ならない）:
  - **izu-from-tokyo**（伊豆への行き方・運賃・JR Pass・南伊豆を車なしで回れるか・伊豆のいつがよいか）: この記事は **日本全国の田舎の一般論**。伊豆の運賃・時刻・フリーきっぷは書かない。h2 に「Izu」「Tokyo to」「cost」を使わない。節3（車）は「田舎全般で車が要るか」で、伊豆の個別の回り方はリンクで送る。
  - **shimoda-guide**（下田の浜・町・買い物と料理・津波・下田の泊まる場所）: 下田の店・浜・行事・津波の話は書かない。節5（店・ごみ）は「小さな町一般の仕組み」で、下田の具体はリンクで送る。
  - **monthly-rental**（1か月の部屋の借り方・合法な民泊の見分け方・予約前に聞くこと・ビザ）: 節4は「田舎にどんな泊まり方があるか（種類の地図）」まで。**合法かの見分け方・1か月の契約の中身・予約前の質問リストは書かず**、リンクで送る。
  - **akiya-try-first**（町を試す・お試し住宅・試しの1か月の過ごし方）: お試し住宅は表の1行＋1文で触れ、条件（移住予定者向け）の詳細はリンクで送る。
  - **digital-nomad**（6か月の拠点・光回線の普及率）・**how-long-stay**（90日・在留）: ビザ・回線の数字は書かず、1文ずつリンク。
  - **kinmedai**: 触れない（必要なら節7の季節の食で1語リンクまで）。
- **エンジニア部への依頼（公開時）**: `TOPICS["stay"]["coming"]` から「The Japanese countryside for a longer stay」を外す。shimoda-guide・izu-from-tokyo・monthly-rental の本文から、この記事へ1本ずつ戻りのリンクを足す（見せ方だけの見直し。playbook 5章）。

## 2. 読み手と検索意図

- 入口: **Stay longer**（数日〜数週間の旅）。also: Live part-time（毎年・数か月来たい人）。
- 検索意図: **Know → Do**。「日本の田舎はどんなところで、どこがよいか」（Know）から、「どこを拠点に、どう移動し、どこに泊まり、どう暮らすか」（Do）。
- その先で本当に困っていること:
  - 上位は「田舎の名所25選」ばかりで、**1〜2泊の観光が前提**。1週間以上いるなら、どこを拠点にすればいいのか、その選び方が分からない
  - 「田舎は車が必須」と言われるが、**国際運転免許がない・運転に自信がない**。車なしでどこまでできるのか
  - 泊まる場所: ホテルは少なく、古民家・農泊・民泊といった言葉の違いと、長く泊まるのに向くのはどれか
  - 暮らしの不安: 店は近くにあるのか・カードは使えるのか、**ごみの分別**、具合が悪くなったら、英語は通じるのか
  - 季節: 雪・台風・梅雨で、行く時期によって何が変わるのか

## 3. 読み手の疑問（品質保証部はこれで採点する）

1. What is it actually like to spend a week or more in rural Japan, and is it worth it compared with moving every night?
2. Where in the Japanese countryside should I base myself, and how do I choose between regions and small towns?
3. Can I travel around rural Japan without a car, and what do I need if I want to drive (international driving permit)?
4. Where can I stay in the countryside for a week or longer — farm stays, old houses, holiday rentals?
5. Will shops be open and close by, and can I pay by card?
6. How does rubbish sorting work when you're staying somewhere rural?
7. What if I get sick, and will anyone speak English?
8. When is the best time of year for a longer stay — what about snow, typhoons and the rainy season?

## 4. 上位ページの穴（2026-11-21 に英語で検索）

検索「japan countryside travel guide」「rural japan where to stay without a car」「living in rural japan as a foreigner long stay」「rural japan travel tips buses car shops」「small towns in japan to stay a week」の上位: gogonihon（Ultimate Guide to Traveling in the Japanese Countryside）、japanobjects（25 Best Places to Enjoy the Japanese Countryside）、asianwanderlust（10 villages）、japanspecialist（Top 10 countryside places）、japanhighlights（best countryside areas）、NYLON、afar（7 small towns）、directionallychallengedtraveler（20 small towns）、JNTO（Remote and rural Japan: road and rail journeys／Countryside Stays／Buses in Japan／Best Locations for Extended Stays）、Lonely Planet（getting around Japan）、japanlivinglife・GaijinPot（2012）・jobsinjapan・tokyoroomfinder・guidable（田舎に住む外国人向け）。

1. **名所の一覧で終わる**。上位の大半が「〇選」で、1〜2泊の観光の前提。**1週間以上いる人が拠点をどう選ぶか（駅・店・バス・借りられる部屋・病院・季節）を軸で示したページがない**。→ 節2の「拠点を選ぶ表」が最大の差。
2. **移動は「車を借りよう」か「景色のよい列車」で止まる**。Lonely Planet は田舎は車がいちばんと書き、JNTO のメディア向けページは景色のよいドライブ・鉄道の紹介。**車なしで暮らすための具体（整理券で払うバス、IC カードが使えない路線、最終バス、予約制の乗合タクシー・コミュニティバス）を公式の出典で書いたページがない**。国際運転免許の条件もあいまいな書き方が多い。→ 節3を JNTO・国交省・警察（警視庁など）の出典で。
3. **暮らしの情報（店・ごみ・病院・言葉）は「移住者向け」のページにしかない**。しかも古い（GaijinPot 2012年、Japan Times 2008年）・出典がない（「家賃は東京の半分」「N4〜N3 がないと暮らせない」など）。**観光の一覧と移住のガイドの間（数日〜数週間の滞在者）がすっぽり空いている** ＝ Noki の Stay longer の場所。→ 節5・節6を JNTO・消防庁・自治体の出典で。
4. **JNTO の「長期滞在に向く場所」（2021年）は都市だけ**（鎌倉・神戸・福岡・松山・那覇・札幌・名古屋）。田舎の長期滞在を正面から扱った公的な英語のページは見当たらない。JNTO の Countryside Stays は民泊・農泊・ごみの分別に触れるが、移動・病院・季節はない。
5. **季節を「選び方の条件」として扱うページがない**（雪・台風・梅雨は写真の題材として出るだけ）。→ 節7で気象庁・国交省の公的な数字（豪雪地帯の広さ、台風の平年の数など）を表に。
6. **運営者の一次情報がない**。自社は地方の町で、欧米からの長期滞在の人を中心に迎える宿を運営している（確認済み）。→ 拠点の選び方・夏の長期滞在・ごみの扱いなどを “we” で添えられる。
- ※ gogonihon・japanobjects・japanspecialist・japanlivinglife はこの環境から開けず（名前解決不可）、検索結果の要約で見た。JNTO の4ページは curl で本文を確認した。

## 5. 構成

### title（`seo_title`）案
- **Japan Countryside: Spending a Week or More in Rural Japan**（57字。「japan countryside」が先頭、「rural japan」も入る）
- 予備: Japan Countryside Stays: Choosing a Base and Getting Around（59字）

### h1 案
- The Japanese countryside for a longer stay: choosing a base, getting around and daily life

### description 案（120〜160字。目次を読み上げず、答えを言う。3-1 の5）
- The Japanese countryside suits a longer stay when your base has a station, a shop you can walk to and buses that run. Then a car becomes optional.（146字）

### dek 案（30語以内）
- You can spend weeks in rural Japan without a car or much Japanese. What matters most is the base: a station, a shop on foot and a bus that runs.（30語）

### In short（3項目・各1文・20語以内）
1. Choose a base before a region: a station, a supermarket on foot and buses you can check.（17語）
2. Rural buses run less often and some don’t take IC cards, so plan around the last bus.（17語。R3）
3. Rubbish rules, shop hours and snow or typhoon seasons differ by town, so ask on your first day.（18語。R7・R10）

### h2（7個。6割以上を疑問・結論の形）と各節で答えること

| # | h2 | この節で答えること（h2 の直後の1〜2文で答えを言い切る） | 表・リスト | 疑問 |
|---|---|---|---|---|
| 1 | What is a longer stay in rural Japan really like? | 答え: 毎晩宿を変える旅と違い、1つの町に荷を下ろし、買い物・料理・バスの時刻に合わせて過ごす。名所を数でこなすより、同じ店や浜に何度も行けるのがよさ（見解 “we think”）。数字は1〜2個まで: 日本の国土の多くが過疎地域に当たること（R1）、外国人の宿泊の多くが大都市に集まっていること（R2）。**図鑑調・定義から入らない**（「Rural Japan is defined as…」にしない）。体験（確認済み）: 自社の宿は欧米からの長期滞在の人が中心で、リモートワークやサーフィン目的の人もいる（experience.md 2026-10-11）。長さの目安は“数日〜数週間”。ビザの上限は1文で `[[l:how-long-stay|…]]` へ | — | 1 |
| 2 | How do you choose a base in the Japanese countryside? | 答え: 景色より、毎日の暮らしが回るかで選ぶ。**表（拠点を選ぶ6つの点）**: 確かめること／長く泊まると何が変わるか／どこで確かめるか（例: 町に駅があるか・新幹線の駅や空港まで何時間か、歩いて行けるスーパーかコンビニ、バスの本数と最終便、週・月で借りられる部屋、近くの病院、雪や台風の季節）。そのあと、場所の性格（海沿いの町・温泉町・山と雪の地域・島・農村）ごとに「どんな人に合うか」を2〜3文の文章で。例は1つだけ: 東京から2時間半ほどの海沿いとして伊豆（`[[l:izu|…]]`、下田の具体は `[[l:shimoda-guide|…]]`）。**地名を並べた“〇選”にしない** | **表**（確かめること／なぜ大事か／どこで確かめるか）。「どこで」は町の観光協会・バス会社の時刻表・JNTO の病院検索（R8）など、読み手が自分で開ける公式の場所 | 2 |
| 3 | Do you need a car in rural Japan? | 答え: 拠点を選べば必須ではない。ただし行ける範囲は狭まる。バスの乗り方（後ろから乗って整理券、降りるとき運賃表で払う、IC カードが使えない路線がある＝JNTO, R3）、本数が少なく最終便が早い地域があること（一般論は公的な出典がある範囲だけ、R4）、予約制の乗合タクシー・コミュニティバス（R4）、タクシー・自転車。運転するなら: 国際運転免許の条件（ジュネーブ条約の IDP、入国から1年まで、一部の国は公式の翻訳文、R5）。**伊豆の回り方は `[[l:izu-from-tokyo|…]]` へ1文**。JR Pass の説明はしない（izu-from-tokyo にある） | **表**（移動の手段／向く使い方／気をつけること: 路線バス・予約制の乗合・タクシー・自転車・レンタカー）。バスの乗り方は **番号つきリスト**（1 後ろのドアから乗り整理券を取る 2 降りるバス停で運賃表の番号を見る 3 前で運賃を払って降りる）＝R3 で手順を確かめる | 3 |
| 4 | Where can you stay in the countryside for a week or more? | 答え: 長く泊まるなら、台所と洗濯機のある貸切の家・部屋（民泊・貸別荘）が中心。農家に泊まる農泊、旅館・民宿、ゲストハウス、マンスリー、町のお試し住宅（移住予定者向け）を **表** で比べる（R11）。旅館・民宿は数泊向き（食事付きで、長くいると割高になりやすい、は見解か出典で）。合法かの見分け方と1か月の契約は `[[l:monthly-rental|…]]` へ、お試し住宅の条件は `[[l:akiya-try-first|…]]` へ。**自社の家に触れるのはここ1回**（下の「自社の家」） | **表**（泊まり方／向く長さ／台所・洗濯／気をつけること） | 4 |
| 5 | How do shops, cash and rubbish work in a small town? | 答え: 店は駅前や幹線道路沿いにまとまり、歩ける範囲にあるかは町による（拠点選びの話に戻す）。道の駅・直売所で地元のものが買える（R14。数字は1つまで）。支払い: 日本全体のキャッシュレスの割合（R6）を1つだけ言い、小さな店やバスでは現金を少し持っておくと安心（JNTO のバスのページなど出典のある範囲で）。ごみ: 分別のルールは市町村ごとに違う（R7）、泊まる宿の決まりに従う（JNTO Countryside Stays に「ごみの分別」の注意あり）。体験（任意）: 自社の宿では、ゲストはごみを室内にまとめ、清掃の担当が分別している（experience.md 3-2）。※名前を出すと自社の家への2回目の言及になるので、“the place we run” とも書かず、“we ask our guests to…” の形で1文に。入れにくければ省く | **番号つきリスト**（着いた日に宿の人に聞くこと: 1 ごみの出し方と曜日 2 近くのスーパー・コンビニと閉まる時間 3 バス停と最終便 4 近くの病院・薬局）。リストはこの記事でここと節3の2か所まで | 5・6 |
| 6 | What if you get sick or need help in English? | 答え: 救急は119（無料）、救急車を呼ぶか迷うときの電話相談（#7119）は地域によってある・ない（R8）。外国語の通じる病院は JNTO の検索で探せる（`jnto_medical`）、24時間の多言語の旅行者向け電話（Japan Visitor Hotline, R8）、観光庁の Safety tips（災害・警報の通知。既存 `jta_safety_tips`）、翻訳アプリ（公的な VoiceTra, R9）。英語が通じる度合いは町による、と見解で。**怖がらせない・地域を下げない**（ゲート） | **表**（困ったとき／連絡先・道具／ひとこと）。番号は R8 で確かめた公式の値だけ | 7 |
| 7 | When is the best season for a longer countryside stay? | 答え: 春と秋が過ごしやすいが、何をしたいかで変わる。梅雨（地域ごとの平年の時期, R10）、夏〜秋の台風（平年の接近数, R10）、冬の雪（豪雪地帯の広さ, R10）を、「長くいると何が変わるか」（バスの運休・道の閉鎖・暖房）とともに。体験（確認済み）: 自社の宿では夏に長期滞在が多め（experience.md 2026-10-11）。**段落で数字を並べない**（3-1 の6）。数字は表に入れ、文は意味だけ | **表**（時期／天気のこと／長く泊まると気をつけること／向く過ごし方）。数字は表の中だけ | 8 |

- 段落の目安: 各節は h2 直後の答え1〜2文 → 表かリスト → 2〜3文の補足（なぜそうか・どんな人に合うか）。スマホで文章だけが3画面続かない。
- **3-1 の6（ガイドブック調）に特に注意する節**: 節1（統計の読み上げにしない。数字は2つまで）、節2（地名と名物の並べ立てにしない。「どんな人に合うか」を添える）、節6（「Japan Visitor Hotline (operated by …)」のようなお役所言葉の正式名から入らない。“a 24-hour helpline for visitors run by Japan’s tourism board (the Japan Visitor Hotline)” のように普通の言葉が先）、節7（気象の数字は表へ）。
- 1つの話題に「事実1つ＋読み手にとっての意味1つ」。例: ✕ Buses run 6 times a day and the last leaves at 18:10. → ◯ Some rural routes only run a handful of times a day, so the last bus shapes your evening more than any restaurant does.（数字は出典がある場合だけ、表か例として）

### FAQ（5問。本文の言い直し。本文にないことを書かない）
1. Can you visit the Japanese countryside without a car?（節3）
2. Where should you stay in rural Japan for a week?（節2・4）
3. Do people speak English in rural Japan?（節6。見解として、翻訳アプリと公的な多言語の窓口）
4. How does rubbish sorting work in rural Japan?（節5）
5. What is the best time of year to visit the Japanese countryside?（節7）

### 内部リンク（本文から5本以上。同じ記事へは本文で2回まで）
- 節1 → `[[l:how-long-stay|how long you can stay in Japan]]`
- 節2 → `[[l:izu|the Izu Peninsula]]`、`[[l:shimoda-guide|our Shimoda guide]]`
- 節3 → `[[l:izu-from-tokyo|getting to Izu from Tokyo]]`
- 節4 → `[[l:monthly-rental|renting a place by the month]]`、`[[l:akiya-try-first|trying out a town before you buy]]`
- （節1か節4で、リモートワークの人向けに `[[l:digital-nomad|Japan’s digital nomad visa]]` を1文で。入れすぎるなら省く）

### related（2本以上）
- `["shimoda-guide", "monthly-rental", "izu-from-tokyo"]`

### 自社の家に触れる場所（1回まで）
- **節4の最後に1〜2文**。拠点選びの軸（駅・店に歩ける）の実例として:
  - 下田の旧町内にある、アパートの一室を改装した貸切の宿（約40㎡）。伊豆急下田駅から徒歩8分、コンビニ2分・スーパー3分（`node_site`・`node_room`・`node_access`）。キッチン・洗濯機とガス乾燥機（`node_room`）。
  - **“house” と書かない**（公式は「アパートの一室」）。料金・割引・最低泊数は書かない。長さに触れるなら「Airbnb のページで28泊以上も受けている」（launch-open-items の確認済みの事実）まで。
  - 写真 `node-shimoda` は使用済みなので本文に入れない。末尾の案内はテンプレートが出す。
- 体験として使えるもの（`experience.md` の人が確認済みの節だけ）: ゲストは欧米からの長期滞在が中心・リモートワークやサーフィン目的の人も・夏は長期滞在が多め（2026-10-11 回答、8章の「欧米からの長期滞在の客が中心」）／旧町内の中心で観光地へ徒歩（3章）／ごみは室内にまとめてもらい清掃パートナーが分別（3-2）。
- **使わないもの**: Wi-Fi の工事に2か月（digital-nomad・akiya-try-first で使用済み。重ねない）、古い配線（akiya-try-first で使用済み）、津波注意報の対応（shimoda-guide で使用済み）、稼働率・売上、焼津・竹原の計画（この記事の主張に関係しない）。

## 6. リサーチ部への依頼（公式のページで確かめる）

既存の出典で使えるもの（最新かだけ見る）: `jnto_medical`、`jta_safety_tips`、`jta_minpaku_overview`・`jta_minpaku_users`（民泊の種類の説明が要るときだけ）、`shimoda_gomi`（市町村ごとの分別の例として使うなら）、`node_site`・`node_room`・`node_access`、`minamialps_trial`・`shizuoka_trial`（お試し住宅の1行）。

| # | 確かめること | 見るべき公式ページ（例） |
|---|---|---|
| R1 | 過疎地域の広さ: 過疎関係市町村の数・全市町村に占める割合・国土の面積に占める割合・人口に占める割合（最新の年度と時点）。記事では「国土の○割が過疎地域、人口は1割ほど」の1文に使う想定 | 総務省「過疎対策」（www.soumu.go.jp の過疎対策の現況・過疎地域市町村等一覧）|
| R2 | 外国人の延べ宿泊者数のうち、三大都市圏と地方部の割合（2024年の確定値、2025年が出ていればそれ） | 観光庁「宿泊旅行統計調査」（www.mlit.go.jp/kankocho/tokei_hakusyo/shukuhakutokei.html）|
| R3 | 地方のバスの乗り方: 整理券・運賃表・前から降りて払う・IC カードが使えない路線がある（英語の本文の該当箇所と取得日）。手順を番号つきリストにしてよい根拠 | JNTO「Buses in Japan」 https://www.japan.travel/en/plan/getting-around/buses/ （2026-11-21 に curl で開けた。“Outside of the main cities, some buses calculate their fares by journey traveled… it might not be possible to use IC cards” の記述あり）|
| R4 | 地方の公共交通の現状を1〜2点: ①路線バスの減便・廃止の動き（国交省の公的な数字、例: 年間の廃止キロ）②予約制の乗合タクシー（デマンド交通）・コミュニティバスを走らせている市町村の数か、制度の公式の説明。旅行者が乗れるか（地域の住民向けに限る例もある）が分かる公的な説明があれば | 国土交通省「交通政策白書」・地域公共交通のページ（www.mlit.go.jp）|
| R5 | 国際運転免許: 日本で運転できる条件（1949年ジュネーブ条約の国際運転免許証、上陸の日から1年以内、外国の免許＋公式の翻訳文で運転できる国・地域の一覧＝スイス・ドイツ・フランス・ベルギー・モナコ・台湾など）。英語のページがあれば優先。2025年以降の変更があれば | 警察庁（www.npa.go.jp は **この環境から開けない**。開けなければ編集長がネットワークの許可に足す）、警視庁の英語ページ（www.keishicho.metro.tokyo.lg.jp）、JAF の公式の翻訳文のページ |
| R6 | 日本のキャッシュレス決済の割合（最新の年と値）。記事では全国の数字として1つだけ使う（「田舎ほど現金」は公的な出典がなければ書かない） | 経済産業省（www.meti.go.jp のキャッシュレス決済比率の公表）|
| R7 | ごみの分別は市町村ごとに決める、と言える公的な根拠（環境省の説明、または廃棄物処理法の市町村の責任）。JNTO「Countryside Stays」のごみの分別・近所への配慮の記述（https://www.japan.travel/en/guide/homestay-farmstay/ 、2026-11-21 に開けた）| 環境省（www.env.go.jp）、JNTO |
| R8 | 困ったときの連絡先: ①救急車は119・無料（消防庁の英語の案内「救急車利用ガイド」）②#7119 を使える地域（消防庁の一覧。全国ではないこと）③Japan Visitor Hotline の番号・24時間・対応言語 ④外国語が通じる医療機関の探し方（JNTO の検索、既存 `jnto_medical`）| 総務省消防庁（www.fdma.go.jp）、JNTO（www.jnto.go.jp）|
| R9 | 翻訳アプリ: 国の研究機関の VoiceTra（無料・対応言語数・提供元）。※民間のアプリ名は出さない | 情報通信研究機構 NICT（voicetra.nict.go.jp）|
| R10 | 季節の表の材料: ①梅雨入り・梅雨明けの平年の時期（地方ごと。沖縄・九州〜東北の幅で）②台風の平年の発生数・接近数・上陸数（1991〜2020年の平年値）と多い月 ③豪雪地帯・特別豪雪地帯の市町村数と、国土の面積に占める割合 | 気象庁（www.jma.go.jp の梅雨の時期の平年値・台風の平年値。data.jma.go.jp は開けない）、国土交通省（豪雪地帯対策のページ）|
| R11 | 泊まり方の表の材料: ①農泊（農林水産省の定義と英語の言い方、農泊に取り組む地域の数）②JNTO の Countryside Stays の minpaku／nouhaku／kominka の説明 ③旅館・民宿の違いを公的に説明したページがあれば（なければ表の説明は一般的な言い方にとどめる）④お試し住宅は既存の出典（`minamialps_trial`・`shizuoka_trial`）で足りるか | 農林水産省「農泊」（www.maff.go.jp）、JNTO、観光庁 |
| R12 | 「拠点を選ぶ表」の“どこで確かめるか”の列に入れる公式の窓口: JNTO の観光案内所（認定外国人観光案内所）の検索ページ、JNTO の医療機関の検索。英語で使えるか | JNTO（www.japan.travel / www.jnto.go.jp）|
| R13 | 外国人の旅行者が地方で困ったこと（公的な調査）: 観光庁「訪日外国人旅行者の受入環境整備に関するアンケート」の最新版で、「困ったこと」の上位（多言語の案内・公共交通・決済など）。記事の節5・6の裏づけに1つだけ使う | 観光庁（www.mlit.go.jp/kankocho）|
| R14 | 道の駅の数（最新の登録数と日付）と、どんなところかの公式の英語の説明。節5で「地元の野菜や魚を買える場所」として1回だけ使う | 国土交通省「道の駅」（www.mlit.go.jp/road/Michi-no-Eki/）|
| R15 | 検索語の月間検索数と KD: japanese countryside / countryside japan / rural japan travel / japan countryside stay / small town japan | 調査ツール（KEYWORDS と同じ方法）|

**開けるドメイン（2026-11-21、この環境から curl で確認）**: `www.japan.travel`（JNTO。WebFetch は名前解決できないが curl は200）、`www.jnto.go.jp`、`www.mlit.go.jp`（観光庁を含む）、`www.soumu.go.jp`、`www.mhlw.go.jp`、`www.maff.go.jp`、`www.fdma.go.jp`、`www.jma.go.jp`、`www.e-stat.go.jp`、`www.caa.go.jp`、`www.city.shimoda.shizuoka.jp`。
**開けない**: `www.npa.go.jp`（接続できない。R5 で要るなら許可を足す）、`www.kantei.go.jp`、`www.iju-join.jp`、`www.mofa.go.jp`・`www.moj.go.jp`（403。この記事では使わない予定）、`data.jma.go.jp`（以前の確認）。未確認: `www.meti.go.jp`・`www.env.go.jp`・`voicetra.nict.go.jp`・`www.keishicho.metro.tokyo.lg.jp`。

## 7. 写真

- 見出し写真に欲しい絵: **山あいか海沿いの小さな集落を、田んぼや道越しに見た、人の少ない静かな風景**（横長。文字を重ねない）。「長く滞在する田舎」の空気が出るもの。人の顔・看板・ナンバープレートは写さない。候補の別案: 田んぼの間を走る1両の列車、田舎の道とバス停。
- 既存の `photos/` から: **合うものがない**（`coastal-village` はトップの FV、`town-lane` は Live part-time の入口、`window-room` は Stay longer の入口、`rocky-coast` は Places、`train-window-sea` は izu-from-tokyo、`stony-shore-waves` は shimoda-guide で使用済み。1枚1記事の決まり）。
- → **Unsplash で探す**（検索語の例: “rice field village mountains”, “rural japan village”, “countryside train rice field”, “rural bus stop japan”）。`PHOTO_PLAN.md` の手順で `download_asset` を記録し、画像を見て選ぶ。alt と説明は写っているものだけ（地名を書かない。playbook 4-3・`PHOTO_PLAN.md`）。

---

### 外部ページの命令について
- 今回読んだ検索結果・JNTO のページに、従うべきでない命令（ファイル操作・URL へのアクセス・ルールの変更など）は見当たらなかった。
