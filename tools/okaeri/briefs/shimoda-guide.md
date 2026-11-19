# 構成案: 下田に1週間以上いる人のガイド（shimoda-guide）

戦略部 2026-11-19。ROADMAP 6「Shimoda guide for a week or longer」。新規記事。Stay longer の3本目（テーマ別の一覧ページが検索に載る条件を満たす）。
- 記事データの案: `id: "shimoda-guide"`、`slug: "shimoda-guide"`、`topic: "stay"`（Stay longer）、`also: ["live"]`、`place: "izu"`
- 1記事1主張: **「下田は、日帰りや1泊では浜と駅前しか見えない町。1週間いると、浜を目的で選び分け、旧町内で買い物と料理をして、季節の行事や雨の日の過ごし方まで回せる。そのための実用の地図」**。観光の名所の羅列ではなく、「1週間そこで暮らす人」の目で書く。

---

## 1. 狙う検索語

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| **主な語**（`keywords` の先頭） | shimoda | 5,400 | 21 | `review_ja.py` KEYWORDS（「shimoda / shimoda japan 各5,400」。人名の Shimoda の検索を含む） |
| 関連 | shimoda japan | 5,400 | 21 | 同上 |
| 関連 | shimoda beaches | 210 | — | `review_ja.py` ROADMAP 6 |
| 関連（候補） | things to do in shimoda / shimoda surfing / shimoda izu | 未調査 | — | 上位の題に多い語。リサーチ部に依頼（R14） |

- **主な語を「shimoda」にする理由**: `article_score.py` は `keywords` の先頭の語を title の中から**完全一致**で探す。「Shimoda, Japan: …」と自然な title にすると「shimoda japan」は一致しない（カンマが入る）。先頭を「shimoda」、2番目を「shimoda japan」にすれば、自然な title のまま満点になり、検索の狙いも変わらない。
- **共食いの線引き**（品質保証部は `keywords` と h2 で照合する）:
  - **伊豆の場所のページ（`IZU`）**: いま `keywords` に「shimoda japan」が入っている。**この記事を出すときに `IZU` の keywords から「shimoda japan」を外し、この記事に移す**（エンジニア部への依頼。`IZU` は「izu peninsula」「shuzenji」が残る）。あわせて、IZU のページの「Guides to the Izu Peninsula」の一覧にこの記事を足し、町の一覧の Shimoda の行から `[[l:shimoda-guide|…]]` で送る。
  - **izu-from-tokyo**（行き方・運賃・Japan Rail Pass・日帰りか・町の選び方・車なしで回れるか・海水浴の期間・バスのフリーきっぷ）: この記事では**行き方・運賃・フリーきっぷの値段・2026年の海水浴の期間を書かない**。1文で触れて izu-from-tokyo へ送る。h2 にも「get to」「cost」「day trip」「without a car」「best time to visit the Izu Peninsula」の形を使わない。この記事の浜の節は「**どの浜が何に向くか**」（浜ごとの性格の比較）で、izu-from-tokyo の「いつ泳げるか」とは疑問が違う。
  - **kinmedai**（金目鯛・どこで食べるか）: 食べる店の話は書かない。「魚を買って自分で料理する」側（漁協の直売所など）だけ書き、金目鯛は1文＋リンク。
  - **monthly-rental**（1か月の部屋の借り方）: 宿の種類の比較・借り方は書かない。最後の節で「1か月以上なら」とリンクで送る。
  - **akiya-try-first**: 重ならない（町を試す話は1文のリンクまで）。

## 2. 読み手と検索意図

- 入口: **Stay longer**（1週間〜1か月の旅）。also: Live part-time（夏をまるごと・毎年来る人）。
- 検索意図: **Know → Do**。「下田はどんな町で、何があるか」（Know）から、「1週間をどう過ごし、どの浜に行き、どこに泊まるか」（Do）。
- その先で本当に困っていること:
  - 上位のページは「下田の名所7選」で、1〜2日の観光の前提。**1週間いたら何をするのか、毎日の暮らし（買い物・料理・ごみ）はどうなるのか**が分からない
  - 浜が多く、どれも「beautiful beach」と書かれていて、**泳ぐ・子ども連れ・サーフィン・静かに過ごす、のどれにどの浜が向くか**が分からない
  - 夏以外に行って楽しめるのか、何が開いていて、何の季節なのか
  - 海の町なので、**津波のときどうすればよいのか**（日本語が読めない人には、警報の意味も避難の場所も分からない）
  - 1週間なら、駅に近い旧町内と浜の近くのどちらに泊まるのがよいか

## 3. 読み手の疑問（品質保証部はこれで採点する）

1. Is Shimoda worth staying in for a week, and what is the town like?
2. Which Shimoda beach is best for swimming, for children, for surfing, or for a quiet day?
3. What is there to do in Shimoda when you’re not on the beach (old town, Perry history, views, hot springs, rainy days)?
4. Is Shimoda worth visiting outside summer, and what happens in each season?
5. Where can I buy food and cook for myself during a week in Shimoda, and how does rubbish work?
6. Is Shimoda safe from tsunamis, and what should I do if there’s a warning?
7. Where should I stay in Shimoda for a week — near the station or near a beach?

## 4. 上位ページの穴（2026-11-19 に英語で検索）

検索「Shimoda Japan travel guide things to do」「Shimoda beaches Izu best beach」の上位: Tokyo Weekender「7 things to do in Shimoda」、whereintheworldisnina、japanstartshere、travelynotes、Expedia・Trip.com・Traveloka（予約サイトの薄い一覧）、japan-guide（Izu beaches）、tsunagujapan、islands.com、worldbeachguide、wanderlog、swimming-in-japan、japanuncharted。

1. **1〜2日の観光が前提**。どのページも「名所の一覧」で終わり、**1週間いる人の暮らし（買い物・料理・ごみ・雨の日・夜）**を書いたページがない。→ 自社が下田の旧町内で長期滞在の宿を運営している立場（確認済み）で、「暮らす1週間」の目で書けば差になる。
2. **浜の比較が感想ベースで、数字が食い違う**（吉佐美大浜の長さが「350m」と別の値で割れている、など）。どの浜がサーフィン向けか・遊泳区域かを、**市・観光協会の公式の情報**で書いたページがない。→ 浜の比較表を公式の出典で作る（R3・R4）。
3. **歴史の事実があいまい・誤りがある**。上位のページに「了仙寺で日米和親条約（神奈川条約）が結ばれた」と読める書き方がある（条約自体は横浜で調印。了仙寺はその後の「下田条約（付録）」の場とされる）。→ 歴史は公式の出典で1〜2文に絞り、正確に書く（R2）。
4. **夏以外の情報が薄い**。「冬は泳げない」で終わり、水仙（爪木崎）・あじさい（下田公園）・黒船祭など季節の行事と、気温の目安を並べたページがない。→ 季節の表（行事＋平年の気温）で差をつける（R6・R8）。
5. **津波・防災に触れたページがない**。海外の読み手にとって切実で、しかも自社に「2025年7月末の津波注意報のとき、外国人ゲストに状況と避難の必要性を逐次伝えた」という確認済みの体験がある。→ 市のハザードマップ・気象庁の警報の意味・観光庁のアプリを出典つきで示し、体験を1〜2文添える（R11）。
6. **予約サイトの自動生成ページが多い**（Expedia・Trip.com・Traveloka）。中身がなく、出典もない。

## 5. 構成

### title（`seo_title`）案
- **Shimoda, Japan: Beaches, Old Town and a Week-Long Stay**（52字・「shimoda」が先頭）
- 予備: Shimoda, Japan: A Guide for a Week or Longer（44字）

### h1 案
- Shimoda, Japan: a guide for a week or longer

### description 案（120〜160字。リサーチの結果に合わせて数字を入れ直す）
- Shimoda is a port town at the tip of the Izu Peninsula with nine official beaches. Which beach suits what, what to do on rainy days, and how a week there works.（157字）

### dek 案（30語以内）
- Shimoda is a small port town at the southern tip of the Izu Peninsula. A week gives you time for several beaches, the old town and an unhurried routine.（29語）

### In short（3項目・各1文・20語以内）
1. Pick a beach by what you want: calm water for swimming, surf beaches for boards, or a quiet cove.（18語。浜の性格は R3・R4 の結果で言い直す）
2. The old town is walkable, with Perry Road, temples, the port and food shops close together.（16語。R2・R13）
3. Outside summer, the town is quieter, with flower festivals in winter and early summer.（14語。R6 の結果で行事名を入れる）

（「In short」は3項目まで。津波の話は In short に入れず、本文の節で落ち着いて書く）

### h2（7個。6割以上を疑問形）と各節で答えること

| # | h2 | この節で答えること（h2 の直後の1〜2文で答えを言い切る） | 表・リスト | 疑問 |
|---|---|---|---|---|
| 1 | Is Shimoda worth a week? | 答え: 浜を1つ見て帰るなら1泊でよいが、浜をいくつも使い分け、旧町内で暮らす調子をつかむなら1週間が合う（見解 “we think”）。町の基本を1〜2文: 伊豆半島の南端の港町、人口（R1）、1854年の開港の町（R2）。行き方は1文で `[[l:izu-from-tokyo|…]]` へ、伊豆全体は `[[l:izu|…]]` へ | — | 1 |
| 2 | Which Shimoda beach suits you? | 答え: 目的で選ぶ。浜ごとに「どんな浜か（砂・波・長さ）」「向いていること（泳ぐ・子ども連れ・サーフィン・静か）」「駅からの行き方（バス停・徒歩）」を公式の出典で（R3・R4）。遊泳区域とサーフィンの区域の決まり（R4）。**海水浴の期間・ライフガードの時間は書かず**「2026年の期間は izu-from-tokyo に」と1文で送る | **表**（浜／どんな浜か／向いていること／行き方）。浜は市の公式の海水浴場から5〜6か所に絞る | 2 |
| 3 | What can you do in Shimoda besides the beach? | 答え: 旧町内の散歩（ペリーロード・了仙寺・港）、寝姿山のロープウェイと眺め、下田公園、温泉（日帰り入浴）、雨の日の過ごし方（R2・R5・R7・R13）。「1週間のうち浜に行かない日」の過ごし方として、文章で書く（名所の箇条書きにしない。3-1） | 必要なら小さな表（場所／駅からの距離・行き方／ひとこと） | 3 |
| 4 | Is Shimoda worth visiting outside summer? | 答え: はい。冬は水仙（爪木崎）、5月は黒船祭、6月はあじさい（下田公園）など、季節ごとの行事があり、気温の目安を平年値で（R6・R8）。夏は浜が混み、宿が埋まりやすい（見解・体験の範囲：夏は長期滞在が多め＝experience.md）。**閑散期に店が早く閉まる、とは書かない**（公的な出典も確認済みの体験もない） | **表**（時期／行事・見どころ／平年の気温の目安） | 4 |
| 5 | How do you shop and cook for a week in Shimoda? | 答え: 魚は漁協の直売所や道の駅で買える（R9）、日用品は町なかのスーパー（店名は公式に出ているものだけ）。宿のキッチンで魚を料理する楽しみ。金目鯛は1文で `[[l:kinmedai|…]]`。ごみは市の分別に従う。宿のルールに合わせる（`shimoda_gomi`・R10） | **番号つきリスト**（着いた日にすること: 1 スーパーと直売所の場所を確かめる 2 ごみの出し方を宿で聞く 3 バスの時刻を確かめる…）。リストはここ1か所だけ | 5 |
| 6 | What should you know about tsunamis in Shimoda? | 答え: 下田は海に面した町で、市が津波のハザードマップと避難の案内を出している（R11）。警報と注意報の違い（気象庁）、揺れを感じたら・警報が出たら高い所へ、観光庁の「Safety tips」アプリ（英語の通知）。**体験（確認済み）**: 2025年7月末の津波注意報のとき、外国人ゲストに Airbnb のメッセージで状況と避難の必要性を逐次伝え、希望に応じてキャンセル・返金に応じた（experience.md 3-2）。怖がらせない・地域を下げない書き方（ゲート「特定の地域を下げる」） | 小さな表（気象庁の「津波警報」「津波注意報」／意味／すること）。数字（想定の津波高）は R11 で公式に確かめられた場合だけ | 6 |
| 7 | Where should you stay in Shimoda for a week? | 答え: 車がないなら、駅に近い旧町内が買い物・バス・電車に便利。浜で過ごす時間を優先するなら浜の近く（見解として、地区ごとの性格を表で）。**自社の家に触れるのはここ1回**（下の「自社の家」）。1か月以上なら `[[l:monthly-rental|…]]` へ | **表**（旧町内（駅の周り）／白浜の周り／南の浜の周り: 向く人・便利なこと・不便なこと）。不便なことは事実（バスの本数など）か “in our view” で | 7 |

- 段落の目安: 各節は h2 の直後の答え1〜2文 → 表かリスト → 2〜3文の補足。スマホで文章だけが3画面続かない（4-3 読みやすさ）。
- 節3 は名所の羅列にしやすいので注意。「浜に行かない日」の1日の流れの例として文章でつなぐ（例: 朝ロープウェイで眺め → 旧町内を歩いて昼 → 午後は日帰り温泉）。ただし所要・時間は R5・R7 で確かめた数字だけ。

### FAQ（5問。本文で答えたことの言い直し。本文にないことを書かない）
1. Is Shimoda worth visiting?（節1）
2. What is the best beach in Shimoda?（節2。「目的による」と答え、泳ぐ／サーフィンの浜を1つずつ）
3. Can you swim in Shimoda outside summer?（節2・4。監視のある期間は市が毎年決める。期間外は監視員がいない＝既存 `shimoda_ohama`）
4. What is there to do in Shimoda in winter?（節4）
5. What should I do if there’s a tsunami warning in Shimoda?（節6）

### 内部リンク（本文から3本以上）
- 節1 → `[[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]]`（行き方・運賃はそちら）
- 節1 → `[[l:izu|the Izu Peninsula]]`
- 節2 → `[[l:izu-from-tokyo|this year’s beach season and bus passes]]` は節1と重なるなら省く（同じ記事へのリンクは本文で2回まで）
- 節5 → `[[l:kinmedai|kinmedai]]`
- 節7 → `[[l:monthly-rental|renting a place by the month]]`
- 受ける側（エンジニア部への依頼）: `IZU` のページの町の一覧（Shimoda の行）と「Guides to the Izu Peninsula」、izu-from-tokyo の「Which Izu town suits you?」の Shimoda の行、kinmedai の最後の節から、この記事へ1本ずつ。※既存記事の本文にリンクを足すのは「見せ方だけ」の見直し（playbook 5章）。

### related（2本以上）
- `["izu-from-tokyo", "kinmedai", "monthly-rental"]`

### 自社の家に触れる場所（1回まで）
- **節7の最後に1〜2文**。事実は公式サイト（`node_site`・`node_room`・`node_access`）と `experience.md`（人が確認済みの節）だけ:
  - 下田の旧町内にある、アパートの一室を改装した貸切の宿（約40㎡・最大4名）。伊豆急下田駅から平らな道を徒歩8分、コンビニ2分・スーパー3分・ペリーロード5分（`node_site`/`node_access`）。キッチン・洗濯機とガス乾燥機・ワークデスク（`node_room`）。2階で階段約13段・シャワーのみ（`node_room`。長く泊まる人には大事なので、正直に1語で触れてよい）。
  - **“house” と書かない**（launch-open-items: 公式は「アパートの一室」）。料金・週割・月割・最低泊数・30泊以上の可否は書かない。予約画面の90泊・Airbnb の28泊以上は、1週間の記事には要らないので書かない。
  - 写真 `node-shimoda` は izu-from-tokyo の本文と IZU のページで使っている（1枚を1記事だけ、の決まり）ので、**この記事の本文には入れない**。末尾の案内はテンプレートが出す（`cta(ctx, photo=True)` で写真付きになるかはエンジニア部が確認）。
- 体験として使えるもの（`experience.md` 人が確認済み）: ゲストは訪日客が中心・ワーケーションやサーフィン目的の人もいる・夏は長期滞在が多め（2026-10-11 の回答）／2025年7月末の津波注意報の対応（3-2）／旧町内の中心でペリーロードなどへ徒歩で行ける（3章）。**ゲストの声**（「海が近く初日の出が見られた、スーパーが近く便利」2026年1月）は要約して1回まで使える（引用符を付けず、名前を出さない）。
- **使わないもの**: 案内している店、Wi-Fi の実測、浜からの最終バスの時刻（launch-open-items で確かめられなかった）、月別稼働率（読み手に関係がない）。

## 6. リサーチ部への依頼（公式のページで確かめる）

既存の出典で使えるもの（新たに確かめなくてよいが、最新かは見る）: `jnto`（白浜中央海岸・バスで約15分）、`shimoda_ohama`（白浜大浜・期間外は監視員なし）、`shimoda_beach2026_city`（2026年の9か所の海水浴場）、`shimoda_kanko_kinme`、`shimoda_kanko_event`、`shimoda_kanko_gift`、`pref_izu_gyokyo_shop`、`shimoda_gomi`、`tokaibus_freepass`、`node_site`・`node_room`・`node_access`。

| # | 確かめること | 見るべき公式ページ（例） |
|---|---|---|
| R1 | 下田市の人口（最新の住民基本台帳の月次、または2020年国勢調査）と、日付 | 下田市（city.shimoda.shizuoka.jp の人口・世帯数のページ）、e-Stat |
| R2 | 開港の歴史を1〜2文で正確に: 1854年の日米和親条約で下田が開港したこと、了仙寺で結ばれたもの（下田条約＝日米和親条約付録、1854年）、ペリーロードの名前の由来、玉泉寺（最初の米国総領事館）。上位ページの「了仙寺で神奈川条約」は誤りの可能性が高いので、正しい書き方を出典つきで | 下田市（文化財・歴史）、下田市観光協会（www.shimoda-city.info/shimoda・/guide）、静岡県の文化財のページ。※文化遺産オンライン（bunka.nii.ac.jp）はこの環境から開けない |
| R3 | 浜の比較表の材料: 市の公式の海水浴場（2026年は9か所）の名前の英語表記と、浜ごとの長さ・砂の色・波の穏やかさ・駐車場・トイレ・シャワー・子ども向けの設備（市や観光協会が書いている範囲だけ）。伊豆急下田駅からの行き方（バスの系統・降りるバス停・所要の目安、または徒歩） | 下田市（海水浴場のページ。既存 `shimoda_ohama` と同じカテゴリ `100300itiban_resort`）、下田市観光協会 www.shimoda-city.info/umi、`shimoda_beach2026_city`（広報しもだ 2026年8月号）、JNTO の各浜のページ（japan.travel/en/spot/…） |
| R4 | サーフィン: どの浜がサーフィンに使われているか（多々戸浜・入田浜・吉佐美大浜・白浜大浜など）、海水浴の期間中の遊泳区域とサーフィンの区域の分け方（市・観光協会・地元のサーフィン連盟などの公式の決まり）。水質の認証（上位ページに「入田浜は水質の認証を取った数少ない浜」とある。ブルーフラッグなどの認証が本当にあるか、どの浜か、何年か） | 下田市、観光協会 /umi、ブルーフラッグの日本の窓口（FEE Japan）の公式ページ、環境省の「快水浴場百選」など |
| R5 | 寝姿山: 伊豆急下田駅の近くから山頂へ行く下田ロープウェイの所要時間・運行時間・大人の往復運賃（確認日を付ける）・山頂から見えるもの | 下田市観光協会 www.shimoda-city.info/kanko/nesugatayama、伊豆急グループの公式（ropeway.izukyu.co.jp は**この環境から開けない**。観光協会のページで足りなければ izukyu.co.jp 内を探す） |
| R6 | 季節の行事: 爪木崎の水仙まつり（2026〜27年の期間・場所・入場）、黒船祭（2027年5月の日程が出ていれば。出ていなければ「例年5月」の根拠）、下田公園のあじさい祭（例年6月の根拠・株数）、ほかに観光協会が載せている年間の行事。※きんめ祭りは観光協会の行事のページに載っていない（launch-open-items）ので書かない | 下田市観光協会 www.shimoda-city.info/event・/suisen、下田市の観光のページ |
| R7 | 温泉: 下田の温泉（下田温泉・蓮台寺温泉など）で、旅行者が日帰りで入れる公衆浴場・共同浴場が公式に案内されているか（名前・場所・料金・定休日） | 下田市、観光協会 /taiken2・/guide |
| R8 | 気候: 下田に最も近い気象庁の観測点（石廊崎か稲取。どちらが近いか・平年値があるか）の月別の平均気温・降水量の平年値（1991〜2020年） | 気象庁 www.jma.go.jp（平年値の検索 data.jma.go.jp は**この環境から開けない**。開けなければ静岡県・下田市が引用している数字を探すか、表から気温の列を外す） |
| R9 | 魚と食材を買える公式の場所: 伊豆漁協の直売所（ベイステージ下田の中。既存 `pref_izu_gyokyo_shop`）の営業日・時間、道の駅「開国下田みなと」の営業時間・中身。観光協会の /eat・/gift に載っている市場・朝市があるか | 静岡県（既存）、道の駅の公式サイト（ドメイン未確認）、観光協会 /eat・/gift |
| R10 | ごみ: 下田市の分別の区分（既存 `shimoda_gomi`）の要点と、英語の分別表があるか。旅行者が宿で出すごみは宿のルールに従う、と書ける公式の根拠（市の事業系ごみの扱いなど。なければ「宿の決まりに従う」は一般的な案内として書き、市の区分は出典つきで） | 下田市（`shimoda_gomi` のページ） |
| R11 | 津波: ①下田市の津波ハザードマップ・避難の案内のページ（英語版があるか）と、町なかの「津波避難ビル」「海抜表示」の案内 ②静岡県の第4次地震被害想定で示された下田市の最大の津波の高さ・到達時間（使うなら「想定」と明記） ③気象庁の「津波警報」「大津波警報」「津波注意報」の意味と、とるべき行動（英語のページがあれば） ④2025年7月30日のカムチャツカ半島付近の地震で、静岡県の沿岸に津波注意報（または警報）が出たか（自社の体験「2025年7月末の津波注意報」と日付・種類がそろうか） ⑤観光庁の「Safety tips」アプリの公式の説明 | 下田市（防災のページ）、静岡県 www.pref.shizuoka.jp/bosaikinkyu/、気象庁 www.jma.go.jp（津波警報・注意報の解説、2025年7月の報道発表）、観光庁 www.mlit.go.jp/kankocho（Safety tips） |
| R12 | 町なかの移動: 旧町内から白浜・吉佐美（外浦・多々戸・入田）方面への東海バスの系統の名前（時刻は書かない。最終便の時刻は launch-open-items で確かめられなかった）、駅前の観光案内所の場所・営業時間、公式に案内されているレンタサイクル・電動自転車の貸出（場所・料金） | 東海バス www.tokaibus.jp（個別の時刻表 transfer-cloud.navitime.biz は**相手側の 403 で開けない**）、観光協会 /guide・/access・/about |
| R13 | 旧町内の距離感: 伊豆急下田駅からペリーロード・了仙寺・下田港（ベイステージ）までの徒歩の目安（公式の地図・案内にある範囲）。ペリーロードの長さ | 観光協会 /guidemap（ガイドマップの PDF）、下田市、`node_site`（ペリーロードまで徒歩5分は既存の事実） |
| R14 | 検索語の月間検索数と KD: things to do in shimoda / shimoda beach / shimoda surfing / shimoda izu / shimoda onsen | 調査ツール（KEYWORDS と同じ方法） |

**開けない・開けない可能性があるドメイン**（2026-11-19、この環境から curl で確認）:
- 開ける（200）: `www.shimoda-city.info`（/umi・/guide・/suisen・/event・/kanko/nesugatayama など）、`www.city.shimoda.shizuoka.jp`・`city.shimoda.shizuoka.jp`、`www.pref.shizuoka.jp`、`www.jma.go.jp`、`www.izukyu.co.jp`、`www.tokaibus.jp`、`www.japan.travel`、`www.jnto.go.jp`、`www.e-stat.go.jp`、`www.mlit.go.jp`。
- 開けない（接続できない）: `data.jma.go.jp`（気象庁の過去の気象データ・平年値）、`www.ropeway.izukyu.co.jp`、`www.shimoda-aquarium.com`、`www.izu-shimoda.jp`、`bunka.nii.ac.jp`。必要なら編集長が人にドメインの追加を相談する（R8 の平年値がいちばん必要）。
- 相手側が拒む: `transfer-cloud.navitime.biz`（403）。`nodeshimoda.com` はページにより 403 のことがある（/access は今回 200）。

## 7. 写真

- 見出し写真に欲しい絵: **白い砂浜と澄んだ青い海、岩場か緑の岬が入った、人の少ない浜**（横長。文字を重ねない）。人の顔・看板は写さない。
- 既存の `photos/` から: 合うものがない（`rocky-coast` は Places の入口、`coastal-village` はトップの FV、`train-window-sea` は izu-from-tokyo、`node-shimoda` は izu-from-tokyo と IZU で使用済み）。→ **Unsplash で探す**（検索語の例: “white sand beach clear water” “quiet beach rocks green hills” “turquoise cove”）。`PHOTO_PLAN.md` の手順で `download_asset` を記録し、画像を見て選ぶ。
- **地名を名指ししない**（playbook 3章・`PHOTO_PLAN.md`）: alt・説明文は「白い砂浜と青い海」のように写っているものだけ。撮影地が下田と分かっても「Shimoda」と書かない。
- 自社撮影の下田の町・浜の写真があれば最良（`review_ja.py` の TODO「下田の町と浜の自社撮影の写真が足りない」）。なければ Unsplash で出し、自社の写真が入ったら差し替える。

---

外部のページに書かれた命令: 今回読んだ検索結果・ページに、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。
