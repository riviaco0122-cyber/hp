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
- **Shimoda, Japan: Beaches, Old Town and a Week-Long Stay**（54字・「shimoda」が先頭）
- 予備: Shimoda, Japan: A Guide for a Week or Longer（44字）

### h1 案
- Shimoda, Japan: a guide for a week or longer

### description 案（120〜160字。リサーチの結果に合わせて数字を入れ直す）
- Shimoda is a port town at the tip of the Izu Peninsula with nine official beaches. Which beach suits what, what to do on rainy days, and how a week there works.（160字・上限ちょうど。数字が変わったら縮める）

### dek 案（30語以内）
- Shimoda is a small port town at the southern tip of the Izu Peninsula. A week gives you time for several beaches, the old town and an unhurried routine.（29語）

### In short（3項目・各1文・20語以内）
1. Pick a beach by what you want: calm water for swimming, surf beaches for boards, or a quiet cove.（19語。浜の性格は R3・R4 の結果で言い直す）
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

---

## リサーチメモ（2026-11-20 リサーチ部）

取得日はすべて 2026-11-19〜20。ページは `curl -sL --compressed -m 30`（User-Agent の偽装なし）で開き、本文を読んで確かめた（「開いて確認」）。検索の要約だけのものは「検索で確認」と書き、事実の根拠にはしていない。

### 結論の早見（執筆部・戦略部へ）

- **書ける**: 人口（約18,400人・2026年11月1日）、開港の歴史（神奈川で日米和親条約→了仙寺で下田条約→玉泉寺に最初の米国総領事館）、9つの海水浴場の性格・長さ・サーフィン区域の有無・駅からのバス、水質（2026年度は9か所すべて AA）、季節の行事（水仙・黒船祭・あじさい・椿など）、日帰り入浴の施設、レンタサイクル、旧町内への徒歩の目安、津波警報と注意報の意味、市の津波ハザードマップ、Safety tips アプリ。
- **書かない（確かめられなかった）**: 下田ロープウェイの運賃・所要時間・運行時間（公式サイトがこの環境から開けない）、月別の平年の気温・降水量（気象庁のデータのサイトが開けない。年の平均だけ市の紹介にある）、津波の到達時間の想定、ブルーフラッグなど入田浜の「水質の認証」、東海バスの系統名・時刻、道の駅全体の営業時間、スーパーの店名、英語のごみ分別表（見つからない）、R14 の検索数（このエージェントに調査ツールがない）。
- **体験との食い違いに注意（重要）**: 自社の体験は「2025年7月末の**津波注意報**」だが、気象庁の発表では 2025年7月30日 09:40 に**静岡県には「津波警報」**が出ていて、18:30 の時点で「津波注意報」に下がっている（31日 10:45 の時点の一覧には静岡県はない＝解除済み）。体験の文を書くときは、**種類を書かずに “tsunami alerts in late July 2025”**（「2025年7月末の津波の警報・注意報のとき」）とするか、気象庁の事実として「静岡県に津波警報、のちに注意報」を出典つきで書き、体験は「そのとき、ゲストに状況と避難の必要性を逐次伝えた」とする。体験に「警報」と書き換えるのは人の確認が要る（experience.md は「注意報」）。

### R1 人口

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| Shimoda had a registered population of 18,433 on 1 November 2026 (resident register). | 下田市「男女別人口・世帯数」 https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/155431.html | 開いて確認。※ページの表記は「18.433」（小数点の誤記）。前月 18,457・前々月 18,501 から見て 18,433 人。記事では “about 18,400” が安全 | 2026年11月1日 |
| The city covers 104.38 km², with about 47 km of coastline; average annual temperature is about 17°C and annual rainfall a little over 1,900 mm. | 下田市「下田市の紹介」 https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/110963.html | 開いて確認 | ページ更新 2023-03-05（気候の数字の統計期間は書いていない→“the city says” で） |

### R2 開港の歴史

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| The Treaty of Kanagawa (Japan–US Treaty of Peace and Amity) was signed on 3rd day of the 3rd month, 1854 (Japanese calendar), and opened Shimoda immediately and Hakodate a year later. | 下田市「ペリー黒船艦隊来航と日本開国」 https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110778.html | 開いて確認。市のページは条約の調印場所を「江戸湾」の交渉の流れで書き、下田とは書いていない。**了仙寺は付録の下田条約** | 歴史 |
| Perry’s ships arrived in Shimoda from the 18th to 21st of the 3rd month, 1854. | 同上 | 開いて確認 | 歴史 |
| The supplementary Shimoda Treaty (13 articles) was signed in the main hall of Ryosenji temple on the 22nd day of the 5th month, 1854. Before the talks, Perry marched about 300 sailors to Ryosenji. | 同上・下田市「了仙寺」 https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110768.html | 開いて確認 | 歴史 |
| Perry Road takes its name from the route Perry’s party marched to Ryosenji for the Shimoda Treaty; its stone paving runs for about 500 metres along the Hiranamegawa stream. | 下田市「ペリーロード」 https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110766.html | 開いて確認（観光協会のレンタサイクルのページも同じ由来） | ページ更新 2023-03-05 |
| Townsend Harris arrived in 1856 as US Consul General and set up Japan’s first US consulate at Gyokusenji temple in Kakisaki; it closed when Yokohama opened in 1859. Gyokusenji is a national historic site. | 下田市「日本における初代米国総領事ハリス」 https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110776.html ・「玉泉寺」 https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110756.html | 開いて確認 | 歴史 |
| In 1854 (11th month) a large earthquake and tsunami (the Ansei tsunami) swept Shimoda Bay, washing away or destroying most houses in town. | 下田市「プチャーチンによるディアナ号来航と『安政の大津波』」 https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110777.html | 開いて確認（節6で「町は津波を経験してきた」と1文添えるなら使える。死者数は書かなくてよい） | 歴史 |

- **正しい書き方**: “The Treaty of Kanagawa opened Shimoda as one of Japan’s first two ports in 1854. A few weeks later, the follow-up Shimoda Treaty was signed at Ryosenji, and Perry Road is named after the route his men marched there.” 日付は和暦の月日なので、西暦の月日に直さない（“in 1854” でとどめる）。

### R3・R4 浜（比較表の材料）

出典: 下田市観光協会の浜ごとのページ（2026年の開設期間が入っている＝2026年版）、下田市「海水浴場」 https://www.city.shimoda.shizuoka.jp/category/100100midokoro/155720.html 、静岡県「令和8年度 海水浴場水質調査結果一覧」 https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/050/681/r8kaisuiyokujoitiran.pdf 。すべて開いて確認。バスの「乗り場」は伊豆急下田駅前のバス乗り場の番号（観光協会の記載）。

| 浜（観光協会のローマ字） | 長さ | 性格（観光協会・市の説明の要約） | サーフィン区域（観光協会） | 駅から（観光協会） | 観光協会のページ |
|---|---|---|---|---|---|
| Shirahama Chuo (Nagatahama) | 720 m | 白浜海岸の北端、磯遊びの家族連れが多い静かな浜。下田で唯一 BBQ ができる。快水浴場百選 | あり | 9番 白浜行き 約18分、古根 下車 徒歩1分 | https://www.shimoda-city.info/shirahama-chuo |
| Shirahama Ohama | 700 m（市・観光協会の一覧）／770 m（観光協会の浜のページ）※食い違い | 伊豆最大級、国道沿い、サーファーと若い人でにぎわう | あり | 9番 白浜行き 約15分、レスポ白浜 下車 | https://www.shimoda-city.info/shirahama-ohama |
| Sotoura | 470 m | 入り江で遠浅・波が穏やか、子ども連れに人気。沖はシーカヤック。快水浴場百選。ユニバーサルビーチ（市）の会場 | なし | 9番 白浜行き 約10分、外浦口 下車 徒歩3分 | https://www.shimoda-city.info/sotoura |
| Kujuppama | 50 m | 須崎御用邸の隣の小さな浜、波が穏やか、両側が岩場で磯遊び。大きなテント・タープ不可 | なし | 10番 爪木崎行き 約15分、グリーンエリア前 下車 徒歩3分 | https://www.shimoda-city.info/kujupama |
| Nabetahama | 130 m | 市街にいちばん近い。入り江でほとんど波がない。和歌の浦遊歩道の端。駐車場・シャワーなし | なし | 3番・4番 約7分、鍋田口 下車 徒歩5分 | https://www.shimoda-city.info/nabeta |
| Tatadohama | 450 m | サーフィン・ボディボードで有名、全国大会も。年間を通して使える温水シャワー | あり | 3番・4番 約7分、多々戸 下車 徒歩3分 | https://www.shimoda-city.info/tatado |
| Iritahama | 400 m | ソテツ並木、落ち着いた浜、ロケ地。サーファーも | あり | 3番・4番 約8分、入田 下車 徒歩3分 | https://www.shimoda-city.info/irita |
| Kisami Ohama | 770 m | 大きな浜、国道から離れて静か、サーファーと家族連れ。近くにカフェ | あり | 3番・4番 約10分、吉佐美 下車 徒歩8分 | https://www.shimoda-city.info/kisami |
| Toji | 410 m | 入り組んだ海岸、混みにくい。近くに龍宮窟とサンドスキー場。シャワー・レンタルなし | あり | 2番 田牛行き 約18分、田牛 下車すぐ。**1日4〜5便** | https://www.shimoda-city.info/toji |

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| In the 2026 survey, all nine Shimoda beaches were rated AA, the top grade for water quality (Iritahama was A in 2025). | 静岡県 令和8年度 海水浴場水質調査結果一覧（上記 PDF） | 開いて確認 | 2026年度の調査 |
| Shirahama Chuo and Sotoura are on the Ministry of the Environment’s list of 100 best swimming beaches (Kaisuiyokujo Hyakusen). | 下田市観光協会「下田の海」 https://www.shimoda-city.info/umi （市のページは白浜中央について「平成18年度 快水浴場百選」） | 開いて確認（環境省のページは開いていない→“the tourism association says”） | 2006年度の選定 |
| Six beaches — Shirahama Chuo, Shirahama Ohama, Sotoura, Tatadohama, Iritahama and Kisami Ohama — are certified by the Japan Lifesaving Association (JLA) for beach safety. | 下田市「海水浴場」（上記） | 開いて確認。九十浜・鍋田浜・田牛には記載なし | 2026年11月の掲載 |
| Outside the official season and hours, no lifeguards are on duty. | 同上（既存 `shimoda_ohama` と同じ趣旨） | 開いて確認 | — |
| Banned on Shimoda’s swimming beaches in season: tents (sunshades allowed), open fires and barbecues (except part of Shirahama Chuo), fireworks, camping overnight, and since 2025 amplified speakers. | 観光協会「下田の海」の禁止事項 | 開いて確認 | 2026年度のルール |

- **サーフィンの区域の分け方**: 観光協会の各浜のページに「サーフィンエリア：あり／なし」があるだけで、区域の線引きの決まりの本文は確かめていない（観光協会の「利用者ルール（PDF）」は開いていない）。→ 書けるのは「どの浜にサーフィンの区域があるか」まで。
- **入田浜の「水質の認証」（上位ページの記述）**: ブルーフラッグなどの認証は公式で確かめられなかった → **書かない**。代わりに県の水質 AA と JLA の認定を書く。
- **浜の長さの食い違い**: 白浜大浜は市と観光協会の一覧が 700 m、観光協会の浜のページが 770 m（吉佐美大浜と同じ値）。**白浜大浜は “about 700 m” と市の値で書くか、長さの列を外す**。白浜中央の 720 m も、市のページには長さがない。表に長さを入れるなら「観光協会の値」と明記。
- 海水浴の期間（2026年は7月18日から8月23日・30日・31日まで、浜で違う）は構成案どおり **この記事では書かず** izu-from-tokyo へ送る。

### R5 寝姿山・ロープウェイ

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| The Shimoda Ropeway station is a one-minute walk from Izukyu-Shimoda Station; from the top of Mt Nesugata you can see the town, the port, the Izu Islands and the Amagi mountains. Parking at the ropeway is free. | 下田市「寝姿山」 https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110764.html | 開いて確認 | 2026年11月の掲載 |
| Shimoda Ropeway is an Izukyu group company. | 伊豆急行「グループ会社」 https://www.izukyu.co.jp/link/group.php | 開いて確認 | — |

- **運賃・所要時間・運行時間は書かない**。公式は `ropeway.co.jp`（観光協会・伊豆急行のリンク先。構成案の `ropeway.izukyu.co.jp` ではない）で、この環境から開けない（プロキシの 403）。検索の要約（るるぶ等）では往復1,050円・約3分半とあるが、出典にしない。

### R6 季節の行事（観光協会「イベント」 `shimoda_kanko_event` と各ページ。開いて確認）

| 時期 | 行事・見どころ（英語の要点） | 出典 | 時点 |
|---|---|---|---|
| 20 Dec – 31 Jan | Daffodil festival at Tsumekizaki; up to about 3 million daffodils, usually at their best in January. Bus no. 10 from the station, about 20 minutes to the last stop. Parking ¥800 a car. | https://www.shimoda-city.info/suisen ・遊歩道のページ（「毎年12月20日から1月31日まで」）https://www.shimoda-city.info/promenade | 2026〜27年の案内（イベントの日付が 12月20日=日曜 なので 2026年冬）。回数は「第60回」の表記が前シーズンの記事にもあり不明確→回数は書かない |
| 5 Dec 2026 – 3 Jan 2027 | Aloe flowers at Itado, Shirahama | 観光協会「イベント」 | 2026〜27年 |
| Dec – Mar | Camellias in Shimoda Park (161 varieties, 5,000 trees per the association; the city says about 160 garden varieties) | 観光協会「イベント」・下田市「下田公園」 https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110769.html | 例年 |
| 27 Mar（毎年同じ日） | Okichi memorial | 観光協会「イベント」 | 例年 |
| mid-Mar – early Apr | Cherry blossoms | 同上 | 例年 |
| May | Black Ship Festival (Kurofune Matsuri), started in 1934; in 2026 it ran 15–17 May with fireworks over the port, a US–Japan parade and a re-enactment of the Shimoda Treaty at Ryosenji | https://www.shimoda-city.info/kurofune | 2026年。**2027年の日程は未発表**→“held every May; in 2026 it was 15–17 May” |
| 1–30 Jun | Hydrangea festival in Shimoda Park, about 3 million blooms, 100+ varieties (55th festival in 2026). The park is hilly; carts for people who find walking hard | https://www.shimoda-city.info/ajisai | 2026年 |
| late Jul | Shirahama fireworks (25 Jul 2026), marlin tournament (23–26 Jul 2026) | 観光協会「イベント」 | 2026年 |
| 14–15 Aug | Shimoda Taiko Matsuri, the festival of Hachiman shrine in the old town | 同上 | 例年 |
| Oct | Te-zutsu hand-held fireworks (10 Oct 2026), Shirahama shrine festival (28–30 Oct) | 同上 | 2026年・例年 |
| late Sep – early May | Ise-ebi (spiny lobster) season | 同上 | 例年 |

- きんめ祭りは構成案どおり書かない（観光協会の行事のページにない）。
- **気温の列（R8）**: 月別の平年値は取れない → **表から気温の列を外す**。代わりに表の下に1文 “Shimoda City puts the average annual temperature at about 17°C.”（`shimoda_profile`）。

### R7 温泉（日帰り）

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| The tourism association lists eight hotels and inns that take day bathers, from ¥600 to ¥1,500 for adults, mostly from mid-afternoon; at busy times they may turn you away. | 観光協会「下田の温泉」 https://www.shimoda-city.info/onsen | 開いて確認 | 2026年11月の掲載 |
| Examples: Izumiso, Nishi-Hongo (¥600, 15:00–21:00); Kurhaus Ishibashi Ryokan, Rendaiji (¥1,100 weekdays / ¥1,430 weekends, 10:00–21:00). | 同上 | 開いて確認 | 同上（料金は変わるので “as of November 2026”） |
| Free footbaths: Kaikoku-no-yu in front of Izukyu-Shimoda Station (9:00–17:00), one at Madogahama park by the port, and one on Shoin-dori in Rendaiji. | 同上・下田市「開国の足湯」「海遊の足湯」（一覧に名前がある） | 開いて確認（観光協会） | 同上 |

- 「共同浴場（公衆浴場）」は公式の案内に見当たらない → 書かない。施設名を出すのは1〜2か所までにし、あとは観光協会の一覧へのリンクが安全。

### R9 魚と食材

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| The Izu Fisheries Cooperative shop is on the ground floor (west wing) of Michi-no-Eki Kaikoku Shimoda Minato, a 10-minute walk from the station; it sells kinmedai, live spiny lobster, turban shells and other seafood, and opens 8:00–16:30 with no fixed closing day. | 静岡県（既存 `pref_izu_gyokyo_shop`、更新 2025-04-24）・観光協会「買う」（既存 `shimoda_kanko_gift`）・下田市「道の駅開国下田みなと」 https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110763.html | 開いて確認 | 県 2025年4月更新 |
| The JA farmers’ shop in the same Michi-no-Eki sells local vegetables, wasabi and New Summer orange products. | 観光協会「買う」 | 開いて確認 | 2026年11月 |
| The Michi-no-Eki has a harbour museum on the 4th floor about Shimoda’s history. | 下田市「道の駅開国下田みなと」 | 開いて確認 | — |

- 道の駅全体の営業時間・公式サイトは確かめられない → 書かない。スーパーの店名も公式の案内がない → 書かない（`node_access` の「スーパー3分」は自社の宿の説明としてだけ使える）。

### R10 ごみ（既存 `shimoda_gomi`。開いて確認）

| 事実（英語） | 確認 | 時点 |
|---|---|---|
| Shimoda collects burnable rubbish twice a week in city-designated bags; cans, bottles, PET bottles, paper and other recyclables are collected twice a month, sorted into separate containers or bags. | 開いて確認 | 2025年4月版の分別表（PDF「R7.4 家庭ごみの分け方・出し方」）が最新 |

- 英語の分別表は市のページに見つからない → 「英語版がある」とは書かない。旅行者が宿で出すごみの扱いを定めた市の文書も見つからない → “Your host will tell you how to sort; Shimoda’s rules are strict” は**一般的な案内・見解**として書く（市の区分だけに出典）。

### R11 津波

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| Shimoda City publishes tsunami hazard maps and evacuation maps for five districts, based on Shizuoka Prefecture’s 4th earthquake damage estimate (in Japanese). | 下田市「津波ハザードマップ・津波避難計画地図」 https://www.city.shimoda.shizuoka.jp/category/010300tiiki_bousai/120138.html | 開いて確認（英語版は見当たらない） | 2026年11月 |
| The city designates four tsunami evacuation buildings (e.g. the Shimoda regional government building in Nishi-Hongo). | 下田市「津波避難ビル」 https://www.city.shimoda.shizuoka.jp/category/010400hinan_basyo/111108.html | 開いて確認。建物名は書かず “a few designated buildings” でよい | 2026年11月 |
| The city has an online map that shows the height above sea level of any point you click. | 下田市「ここは海抜何メートル」 https://www.city.shimoda.shizuoka.jp/category/010500bousai_tishiki/159625.html | 開いて確認 | 2026年11月 |
| In the worst-case Nankai Trough scenario, Shizuoka’s estimate puts the maximum tsunami height in Shimoda at 33 m (average 15 m). | 広報しもだ 2013年8月号 https://city.shimoda.shizuoka.jp/file/平成25年8月号2頁3頁.pdf | 開いて確認（表の「最大 33ｍ・平均 15ｍ」）。**使うなら「想定（2013年）」と明記**。怖がらせない書き方にする。到達時間は確かめられない→書かない | 2013年の想定 |
| JMA issues a tsunami advisory for expected waves of 0.2–1 m (get out of the water and away from the shore), a tsunami warning for 1–3 m and a major tsunami warning above 3 m (move to high ground or an evacuation building at once), aiming to issue them about three minutes after an earthquake. | 気象庁「津波警報・注意報、津波情報、津波予報について」 https://www.jma.go.jp/jma/kishou/know/jishin/joho/tsunamiinfo.html | 開いて確認（日本語。英語の気象庁のページは開けなかった） | 2026年11月 |
| JMA also says: if you feel strong shaking, or weak but long shaking, start evacuating without waiting for a warning; tsunamis come repeatedly, so stay until the warning is lifted. | 同上 | 開いて確認 | 同上 |
| After the M8.7 earthquake near Kamchatka at about 8:25 on 30 July 2025, JMA issued a tsunami warning for the Shizuoka coast (09:40 list); by 18:30 Shizuoka was under an advisory, and by 10:45 on 31 July it was no longer listed. The highest wave recorded at Shimoda port was 0.6 m (00:06, 31 July). | 気象庁 報道発表 https://www.jma.go.jp/jma/press/2507/30a/202507301010.html ・ https://www.jma.go.jp/jma/press/2507/30c/202507301910.html ・ https://www.jma.go.jp/jma/press/2507/31a/kaisetsu202507311115.pdf | 開いて確認 | 2025年7月30〜31日 |
| “Safety tips” is a free app from the Japan Tourism Agency that pushes earthquake early warnings, tsunami warnings and weather warnings in English and other languages (iOS 13+, Android 5+). | 観光庁「Safety tips」 https://www.jnto.go.jp/safety-tips/eng/app.html | 開いて確認 | 2026年11月 |

- 体験との食い違いは冒頭の「結論の早見」を参照（体験は「注意報」、気象庁では静岡県は最初「警報」）。

### R12 町なかの移動

| 事実（英語） | 出典 | 確認 | 時点 |
|---|---|---|---|
| Buses to the beaches leave from numbered stops outside Izukyu-Shimoda Station: no. 9 for Shirahama and Sotoura, nos. 3 and 4 for Nabeta, Tatado, Irita and Kisami, no. 10 for Kujuppama and Tsumekizaki, no. 2 for Toji (only 4–5 buses a day). | 観光協会の浜のページ（R3 の表） | 開いて確認 | 2026年版 |
| The tourism association’s information centre near the station (1-4-28 Shimoda, a short walk from the station) opens 9:00–16:45; its main office in the Michi-no-Eki opens 8:30–17:00, every day. | 観光協会「下田市観光協会について」 https://www.shimoda-city.info/about | 開いて確認 | 2026年11月 |
| Bikes, including e-bikes, can be rented at the tourism association in the Michi-no-Eki (from ¥500 for an hour, ¥2,000 for a day, 9:00–17:00, no booking, ID such as a passport needed) and at the station information centre (day only, ¥2,000). | 観光協会「レンタサイクル」 https://www.shimoda-city.info/access-bicycle | 開いて確認。※観光協会の「アクセス」のページの料金（4時間以上2,000円）と書き方が違う→レンタサイクルのページの値を使う | 2026年11月 |

- **東海バスの系統名・時刻は書かない**。`www.tokaibus.jp` は 2026-11-20 時点で「メンテナンス（脆弱性への対応で公開を見合わせ）」の表示で、路線・フリーきっぷのページの中身が見られない（既存の `tokaibus_freepass`・`tokaibus_highway` も今日は確かめ直せない。リンク切れの点検で引っかかる可能性あり）。

### R13 旧町内の距離感

| 事実（英語） | 出典 | 確認 |
|---|---|---|
| From Izukyu-Shimoda Station on foot: the ropeway 1 min, the Michi-no-Eki (port) 10 min, Perry Road and Ryosenji 15 min, Shimoda Park 20 min. | 下田市の各「みどころ」（寝姿山・道の駅・ペリーロード・了仙寺・下田公園） | 開いて確認 |
| Perry Road’s stone paving is about 500 m long. | 下田市「ペリーロード」 | 開いて確認 |
| Walks: Wakanoura promenade (1.2 km, about 15 min, from the aquarium to Oura beach); Shimoda Park paths (2.4 km, about 1 h 30 min); Green Area path at Tsumekizaki (2 km, about 1 h 15 min). | 観光協会「遊歩道」 https://www.shimoda-city.info/promenade | 開いて確認 |

- 雨の日の候補（公式で場所が確かめられたもの）: 道の駅4階のハーバーミュージアム（市）、了仙寺の宝物館（市）、日帰り入浴（観光協会）。水族館（下田海中水族館）は観光協会に名前と住所があるが、公式サイト（`shimoda-aquarium.com`）が開けないので、営業時間・料金は書かない。

### R14 検索語

- **未調査**。このエージェントには検索数の調査ツールがない。主な語「shimoda」「shimoda japan」は構成案（`review_ja.py` の KEYWORDS）のまま。things to do in shimoda などの数字は、編集長が調査ツールで取るか、空欄のままにする（記事の中身には影響しない）。

### 海外の読み手の疑問（WebSearch の旅行ガイド・レビューの要約。投稿者・URL は書かない）

1. 車がなくても浜をいくつも回れるのか。浜どうしは歩けない距離で、夏の週末は道が混む、と書くガイドが多い。→ 節2・7で「駅からのバスの番号と所要」「田牛は1日数本」で答えられる。
2. 1週間いるなら、何日を下田に、何日を半島のほかの町に使うべきか。→ 節1の見解で答える。
3. 冬や秋に行って楽しめるのか、泳げないなら何をするのか。浜の散歩・温泉・水仙が挙がるが、何が開いているかの情報が薄い。→ 節4の季節の表。
4. 白浜と吉佐美・多々戸のどちらに泊まる・通うのがよいか（にぎやか／静か、サーフィン）。→ 節2の表、節7。
5. ロープウェイや見どころの営業時間が季節で変わるのか。→ 時刻は書けないので「公式で確かめて」と1文。
6. 津波の警報が出たら外国人旅行者はどうすればよいのか、英語の情報はあるのか。→ 節6（気象庁の区分・Safety tips）。

### 新しく使う出典（`SOURCES_NEW` 用。キー: (URL, 英語の短い名前, 日本語名, 英語の正式名)）

```python
"shimoda_population": ("https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/155431.html", "Shimoda City (population)", "下田市（男女別人口・世帯数）", "Shimoda City: Population and households from the resident register (1 November 2026)"),
"shimoda_profile": ("https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/110963.html", "Shimoda City (about the city)", "下田市（下田市の紹介）", "Shimoda City: About Shimoda"),
"shimoda_hist_perry": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110778.html", "Shimoda City (Perry and the opening of Japan)", "下田市（ペリー黒船艦隊来航と日本開国）", "Shimoda City: Perry’s Black Ships and the opening of Japan"),
"shimoda_hist_harris": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110776.html", "Shimoda City (Townsend Harris)", "下田市（日本における初代米国総領事ハリス）", "Shimoda City: Townsend Harris, the first US Consul General in Japan"),
"shimoda_hist_ansei": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110777.html", "Shimoda City (the Ansei tsunami)", "下田市（ディアナ号来航と安政の大津波）", "Shimoda City: Putyatin, the Diana and the Ansei tsunami"),
"shimoda_perryroad": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110766.html", "Shimoda City (Perry Road)", "下田市（ペリーロード）", "Shimoda City: Perry Road"),
"shimoda_ryosenji": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110768.html", "Shimoda City (Ryosenji)", "下田市（了仙寺）", "Shimoda City: Ryosenji temple"),
"shimoda_gyokusenji": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110756.html", "Shimoda City (Gyokusenji)", "下田市（玉泉寺）", "Shimoda City: Gyokusenji temple"),
"shimoda_nesugata": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110764.html", "Shimoda City (Mt Nesugata)", "下田市（寝姿山）", "Shimoda City: Mt Nesugata"),
"shimoda_park": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110769.html", "Shimoda City (Shimoda Park)", "下田市（下田公園）", "Shimoda City: Shimoda Park"),
"shimoda_michinoeki": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110763.html", "Shimoda City (Michi-no-Eki)", "下田市（道の駅開国下田みなと）", "Shimoda City: Michi-no-Eki Kaikoku Shimoda Minato"),
"shimoda_beaches_city": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/155720.html", "Shimoda City (beaches)", "下田市（海水浴場）", "Shimoda City: Swimming beaches (2026 season, checked November 2026)"),
"shimoda_kanko_umi": ("https://www.shimoda-city.info/umi", "Shimoda Tourism Association (beaches)", "下田市観光協会（下田の海）", "Shimoda Tourism Association: Shimoda’s nine beaches and beach rules (checked November 2026)"),
"shimoda_kanko_beach_shirahamachuo": ("https://www.shimoda-city.info/shirahama-chuo", "Shimoda Tourism Association (Shirahama Chuo)", "下田市観光協会（白浜中央海水浴場）", "Shimoda Tourism Association: Shirahama Chuo (Nagatahama) Beach (2026)"),
"shimoda_kanko_beach_shirahama": ("https://www.shimoda-city.info/shirahama-ohama", "Shimoda Tourism Association (Shirahama Ohama)", "下田市観光協会（白浜大浜海水浴場）", "Shimoda Tourism Association: Shirahama Ohama Beach (2026)"),
"shimoda_kanko_beach_sotoura": ("https://www.shimoda-city.info/sotoura", "Shimoda Tourism Association (Sotoura)", "下田市観光協会（外浦海水浴場）", "Shimoda Tourism Association: Sotoura Beach (2026)"),
"shimoda_kanko_beach_kujuppama": ("https://www.shimoda-city.info/kujupama", "Shimoda Tourism Association (Kujuppama)", "下田市観光協会（九十浜海水浴場）", "Shimoda Tourism Association: Kujuppama Beach (2026)"),
"shimoda_kanko_beach_nabeta": ("https://www.shimoda-city.info/nabeta", "Shimoda Tourism Association (Nabetahama)", "下田市観光協会（鍋田浜海水浴場）", "Shimoda Tourism Association: Nabetahama Beach (2026)"),
"shimoda_kanko_beach_tatado": ("https://www.shimoda-city.info/tatado", "Shimoda Tourism Association (Tatadohama)", "下田市観光協会（多々戸浜海水浴場）", "Shimoda Tourism Association: Tatadohama Beach (2026)"),
"shimoda_kanko_beach_irita": ("https://www.shimoda-city.info/irita", "Shimoda Tourism Association (Iritahama)", "下田市観光協会（入田浜海水浴場）", "Shimoda Tourism Association: Iritahama Beach (2026)"),
"shimoda_kanko_beach_kisami": ("https://www.shimoda-city.info/kisami", "Shimoda Tourism Association (Kisami Ohama)", "下田市観光協会（吉佐美大浜海水浴場）", "Shimoda Tourism Association: Kisami Ohama Beach (2026)"),
"shimoda_kanko_beach_toji": ("https://www.shimoda-city.info/toji", "Shimoda Tourism Association (Toji)", "下田市観光協会（田牛海水浴場）", "Shimoda Tourism Association: Toji Beach (2026)"),
"pref_beach_water_2026": ("https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/050/681/r8kaisuiyokujoitiran.pdf", "Shizuoka Prefecture, 2026", "静岡県（令和8年度 海水浴場水質調査結果一覧）", "Shizuoka Prefecture: Beach water quality survey results, FY2026"),
"shimoda_kanko_suisen": ("https://www.shimoda-city.info/suisen", "Shimoda Tourism Association (daffodil festival)", "下田市観光協会（水仙まつり）", "Shimoda Tourism Association: Daffodil festival at Tsumekizaki (2026–27 season)"),
"shimoda_kanko_kurofune": ("https://www.shimoda-city.info/kurofune", "Shimoda Tourism Association (Black Ship Festival)", "下田市観光協会（黒船祭）", "Shimoda Tourism Association: Black Ship Festival (2026 edition)"),
"shimoda_kanko_ajisai": ("https://www.shimoda-city.info/ajisai", "Shimoda Tourism Association (hydrangea festival)", "下田市観光協会（あじさい祭）", "Shimoda Tourism Association: Hydrangea festival in Shimoda Park (2026)"),
"shimoda_kanko_onsen": ("https://www.shimoda-city.info/onsen", "Shimoda Tourism Association (hot springs)", "下田市観光協会（下田の温泉）", "Shimoda Tourism Association: Day hot springs and footbaths (checked November 2026)"),
"shimoda_kanko_bicycle": ("https://www.shimoda-city.info/access-bicycle", "Shimoda Tourism Association (bike rental)", "下田市観光協会（レンタサイクル）", "Shimoda Tourism Association: Bike rental (checked November 2026)"),
"shimoda_kanko_promenade": ("https://www.shimoda-city.info/promenade", "Shimoda Tourism Association (walks)", "下田市観光協会（遊歩道）", "Shimoda Tourism Association: Walking paths (checked November 2026)"),
"shimoda_kanko_about": ("https://www.shimoda-city.info/about", "Shimoda Tourism Association (information centres)", "下田市観光協会（観光協会について）", "Shimoda Tourism Association: Information centres and opening hours (checked November 2026)"),
"shimoda_tsunami_map": ("https://www.city.shimoda.shizuoka.jp/category/010300tiiki_bousai/120138.html", "Shimoda City (tsunami hazard maps)", "下田市（津波ハザードマップ・津波避難計画地図）", "Shimoda City: Tsunami hazard maps and evacuation maps (in Japanese)"),
"shimoda_tsunami_bldg": ("https://www.city.shimoda.shizuoka.jp/category/010400hinan_basyo/111108.html", "Shimoda City (tsunami evacuation buildings)", "下田市（津波避難ビル）", "Shimoda City: Tsunami evacuation buildings"),
"shimoda_elevation_map": ("https://www.city.shimoda.shizuoka.jp/category/010500bousai_tishiki/159625.html", "Shimoda City (height above sea level map)", "下田市（ここは海抜何メートル）", "Shimoda City: Online map of height above sea level"),
"shimoda_news_2013_08": ("https://city.shimoda.shizuoka.jp/file/平成25年8月号2頁3頁.pdf", "Shimoda City newsletter, August 2013", "広報しもだ 2013年8月号", "Shimoda City newsletter, August 2013: Shizuoka’s 4th earthquake damage estimate for Shimoda"),
"jma_tsunami_warnings": ("https://www.jma.go.jp/jma/kishou/know/jishin/joho/tsunamiinfo.html", "Japan Meteorological Agency", "気象庁（津波警報・注意報、津波情報、津波予報について）", "Japan Meteorological Agency: Tsunami warnings, advisories and information (in Japanese, checked November 2026)"),
"jma_kamchatka_2025": ("https://www.jma.go.jp/jma/press/2507/30a/202507301010.html", "Japan Meteorological Agency, 30 July 2025", "気象庁 報道発表（2025年7月30日10時10分）", "Japan Meteorological Agency: Earthquake near the Kamchatka Peninsula at about 8:25 on 30 July 2025 (press release)"),
"jma_kamchatka_2025_eve": ("https://www.jma.go.jp/jma/press/2507/30c/202507301910.html", "Japan Meteorological Agency, 30 July 2025 (evening)", "気象庁 報道発表（2025年7月30日19時10分）", "Japan Meteorological Agency: Earthquake near the Kamchatka Peninsula, third report (30 July 2025)"),
"jma_kamchatka_2025_obs": ("https://www.jma.go.jp/jma/press/2507/31a/kaisetsu202507311115.pdf", "Japan Meteorological Agency, 31 July 2025", "気象庁 報道発表資料（2025年7月31日11時15分）", "Japan Meteorological Agency: Earthquake near the Kamchatka Peninsula, fourth report with tsunami observations (31 July 2025)"),
"jta_safety_tips": ("https://www.jnto.go.jp/safety-tips/eng/app.html", "Japan Tourism Agency (Safety tips)", "観光庁（Safety tips アプリ）", "Japan Tourism Agency: The app “Safety tips” (checked November 2026)"),
"izukyu_group": ("https://www.izukyu.co.jp/link/group.php", "Izukyu (group companies)", "伊豆急行（グループ会社）", "Izu Kyuko: Group companies (checked November 2026)"),
```

既存のキーで使うもの: `shimoda_gomi`・`pref_izu_gyokyo_shop`・`shimoda_kanko_gift`・`shimoda_kanko_event`・`shimoda_ohama`・`jnto`・`node_site`・`node_room`・`node_access`（`shimoda_beaches_city` は `shimoda_ohama` と同じカテゴリの一覧ページ。浜1つなら既存のキーで足りる）。

### 確かめた件数・書かない件数

- **確かめた事実**: 約50件（表の行。R3 の浜の表は9浜×5項目を1件ずつ数えず「浜ごと1件」で数えた）。
- **書かないと決めた事実**: 12件 — ①ロープウェイの運賃 ②同所要時間 ③同運行時間 ④月別の平年の気温・降水量 ⑤津波の到達時間の想定 ⑥入田浜などのブルーフラッグ・水質の認証 ⑦サーフィン区域の線引きの決まり ⑧東海バスの系統名・時刻 ⑨道の駅全体の営業時間 ⑩スーパーの店名 ⑪英語のごみ分別表 ⑫共同浴場（公衆浴場）。あわせて、水族館の営業時間・料金、R14 の検索数も書かない（未調査）。

### 開けなかったドメイン

**プロキシで止められた（許可に足せば開けそう）** — curl が `CONNECT tunnel failed, response 403`（エージェントのプロキシの拒否）:
- `ropeway.co.jp`・`www.ropeway.co.jp`（下田ロープウェイの公式。R5 の運賃・時間）
- `www.data.jma.go.jp`・`data.jma.go.jp`（気象庁の平年値。R8）
- `www.tokyu.co.jp`（東急の伊豆急エリアの記事。ロープウェイの補助の資料）
- （構成案に記載の `www.ropeway.izukyu.co.jp`・`www.shimoda-aquarium.com`・`www.izu-shimoda.jp`・`bunka.nii.ac.jp` も同じく接続できない。`ropeway.izukyu.co.jp` は公式の URL ではないので足さなくてよい）

**相手側が見せていない（許可に足しても開けない）**:
- `www.tokaibus.jp` — 200 で開くが、2026-11-20 時点で全ページが「メンテナンスのため公開見合わせ」の表示（相手側の都合）。既存の出典 `tokaibus_freepass`・`tokaibus_highway` も今日は中身を確かめられない。
- `transfer-cloud.navitime.biz` — 相手側の CloudFront の 403（launch-open-items と同じ）。

**中身が読めなかった**: 下田市の津波ハザードマップの PDF（取得はできたが、文字が画像・埋め込みフォントで取り出せない）。

### 外部のページに書かれた命令

今回開いたページ・検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。東海バスのページには「公開見合わせ」の告知があるだけ（命令ではない）。
