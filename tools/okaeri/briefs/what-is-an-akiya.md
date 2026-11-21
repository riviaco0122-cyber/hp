# 構成案: What is an akiya?（slug: what-is-an-akiya）

戦略部 2026-11-21。計画（`briefs/plan-2026-11.md`）の3番。入口は **Own a home**（`topic: "own"`、`also: []`）。空き家テーマの **柱（親）記事**。細かい記事（買う前に住む・安い家の本当の費用・外国人は買えるか・空き家バンク・古い家で暮らす）へリンクでつなぐ役。

---

## 1. 狙う検索語

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| **主な語**（`keywords` の先頭） | akiya | 3,600 | 0 | `review_ja.py` KEYWORDS（2026-11-14） |
| 関連 | akiya japan | 1,300 | 3〜7 | 同上 |
| 関連 | akiya houses | 1,300 | 3〜7 | 同上 |
| 関連 | abandoned houses in japan | 1,000 | 3 | 同上 |
| 関連（未調査） | what is an akiya / japan empty houses | — | — | リサーチ部に依頼（R10） |

`keywords` 案: `[("akiya", "3,600", "0"), ("akiya japan", "1,300", "—"), ("akiya houses", "1,300", "—"), ("abandoned houses in japan", "1,000", "3")]`

### 共食いの整理（重要）

- 既存の **akiya-try-first** の `keywords` に `("akiya", "3,600", "0")`（2番目）が入っている。この記事の公開と同時に、**akiya-try-first の `keywords` から "akiya" を外す**（記事データのメタ情報だけの変更。本文・事実は変えない）。エンジニア部への依頼として編集長に回す。
- h2 の重なり: akiya-try-first の h2 は6つ（Can foreigners buy an akiya? / Why live in the town before you buy? / What only shows up once you live in an old house? / Which ways of staying… / Where can you stay for a month… / What does a trial month look like?）。この記事で重なるのは「外国人は買えるか」の1つだけ（7つ中1つ）。その節は3〜4文で要点だけにして、akiya-try-first に送る。
- 読み手の疑問の重なりも8つ中2つ（外国人・安いか）まで。FAQ は akiya-try-first の FAQ（外国人は買えるか・ビザ・安いか・お試し住宅・何戸あるか）と同じ問いを立てない。
- `TOPICS["own"]["coming"]` から "What is an akiya?" を外す（エンジニア部）。

---

## 2. 読み手と検索意図

- 入口: **Own a home**。
- 意図: **Know**（akiya って何？ なぜ日本にはそんなに空き家があるの？ 本当に安く買えるの？）。
- 検索した人: ニュース・動画で「日本では家がタダ同然」「900万戸の空き家」を見て興味を持った欧米の人。まだ買うと決めていない。
- その先で本当に困っていること:
  - 「放置された家が何百万戸もある」という話と、実際に買える家の数・状態との差が分からない（ニュースの数字が大きすぎて、自分にとって現実的かが見えない）。
  - 「安い」の裏に何があるか（直す費用・耐震・税・手続き）が分からない。
  - どこで探せばよいか、外国に住んでいても買えるかの入口が分からない。
- 記事の主張（1記事1主張）: **「akiya はただの空き家で、900万戸の大半は廃屋ではない。買える安い家は、空き家バンクなどで見つかるが、値札より直す費用と町で決まる」**。

---

## 3. 読み手の疑問（品質保証部はこれで採点する）

1. What does “akiya” actually mean? Is every empty house an akiya?
2. How many akiya are there in Japan, and are they really all abandoned?
3. Why does Japan have so many empty houses?
4. Are akiya only in the countryside? Where are most of them?
5. Are akiya really cheap, or even free? What’s the catch?
6. Is an old akiya safe to live in (earthquakes, condition)?
7. Where do you find akiya for sale? What is an akiya bank?
8. Can foreigners buy an akiya?（要点だけ。詳しくは akiya-try-first）

---

## 4. 上位ページの穴（差別化）

WebSearch（2026-11-21、「what is an akiya japan」「akiya japan abandoned houses why so many」「akiya bank … foreigners guide 2026」）で見た上位: akiyajapan.com（What is akiya / glossary）、akiya2.com（beginner’s guide）、tokyocheapo.com、zenbird.media、jobsinjapan.com、ニュース（Yahoo 転載・SCMP・RICS・The Hustle）、物件・仲介系（arealty.jp・mailmate.jp・akiyaportal.com）。
※ akiyajapan.com・akiya2.com・tokyocheapo.com は環境のネットワークで開けず、検索結果の要約からの判断。

| 穴 | 具体的に | この記事でどう埋めるか |
|---|---|---|
| 定義があいまい・根拠がない | 「6か月以上空いている家」という定義が出回っている（出典なし）。統計（住宅・土地統計調査）の数え方と、法律（空家法）の「おおむね1年使われていない」の違いを書いたページが見当たらない | h2-1 で、ふだんの言葉・統計・法律の3つの意味を普通の言葉で分ける（R1・R2） |
| 900万戸＝廃屋のように書く | 「900万戸が放置」と書く記事が多い。実際は貸す用・売る用・別荘が半分以上 | h2-2 の表で4つの区分と2018年からの変化を見せ、「廃屋と呼ばれるのは約386万戸」と言い換える（R1） |
| 数字の出典が民間・転載 | 理由（相続・高齢化）の数字が、ニュース経由・出典不明（「59%が相続」など） | 国交省の空き家所有者実態調査（R4）で言い直す |
| 「安い」の裏の制度が古い・ない | 2023年の空家法の改正（放置すると土地の税の軽減が外れうる）、2024年の相続登記の義務化、低い価格の家の仲介手数料の特例（2024年）を、海外向けに書いたページが少ない | h2-5・h2-3 で、読み手にとっての意味（売り手が手放したがる理由・買う側の費用）に言い換えて触れる（R4・R5・R8） |
| 耐震の基準年が出てこない | 「古い家は地震に弱い」で止まる。1981年6月の新しい耐震基準という、物件を見るときの目安がない | h2-5 で「1981年6月より前か後か」を見るポイントとして1文（R6） |
| 一次情報がない | 物件サイト・ニュースの言い換えが中心。直す費用の実例がない | 自社の確認済みの数字（下田の部屋の改修 約410万円＋家具・家電 約240万円、準備 約7か月）を、「買った家ではなく借りた部屋」と断って規模感として1回だけ使う |
| 空き家バンクの実像 | 「空き家バンクで探せ」で終わる。自治体ごとの運営・全国版の窓口・日本語だけ・利用条件がある、が書かれていない | h2-6 で番号つきリスト（探し方の順番）＋自治体の条件の例1つ（R7） |
| 答えが遅い | 定義にたどり着くまでが長い（歴史・ニュースから入る） | dek と In short で「空き家のこと・数・大半は廃屋ではない・外国人も買える」まで言い切る |

---

## 5. 構成

### title・description

- **seo_title 案**: `What Is an Akiya? Japan’s Empty Houses and Who Can Buy One`（58字。主な語が前半）
  - 予備: `What Is an Akiya? Why Japan Has 9 Million Empty Homes`（54字。数字を入れるなら本文と年を合わせる）
- **h1 案**: `What is an akiya? Japan’s empty houses, and what buying one really means`
- **description 案**（120〜160字。執筆部が字数を合わせる）: `An akiya is simply an empty house. Japan had about 9 million in 2023, but most aren’t abandoned, and the cheap ones cost more to fix than to buy.`
  - 目次の読み上げ（Here’s why… / This guide covers…）にしない（playbook 3-1-5）。

### dek（30語以内）と In short（3項目・各20語以内）

- dek 案: `An akiya is just a house nobody lives in. Japan has about 9 million, and the ones people call abandoned are fewer than half of them.`（数字は R1 で確定）
- In short 案:
  1. `Japan had about 9 million empty homes in 2023, a record 13.8% of all housing.`
  2. `Most are waiting for a tenant or buyer; about 3.9 million are simply left unused.`
  3. `Foreigners can buy one, usually through a town’s akiya bank, but repairs often cost more than the house.`

### 書き出し（図鑑調にしない）

定義・語源（空き＋家）から入らない。友人が最初に言うこと＝「ニュースの“タダ同然の家”の話と、実際は少し違う」から入る。例の方向: “If you’ve seen headlines about Japan giving houses away, the real picture is less dramatic and more useful.” のあと、すぐ「akiya は空き家のこと」と言い切る。漢字（空き家）とローマ字の意味はかっこで添えるだけ。

### h2（7つ。すべて疑問形）と各節で答えること

| # | h2 案 | この節で答えること（最初の1〜2文で答えを言い切る） | 表・リスト | 疑問 |
|---|---|---|---|---|
| 1 | What does “akiya” actually mean? | ふだんの言葉では「人が住んでいない家」。数え方は2つある: 国の統計（5年に1度の住宅の調査）は、調査の日に人が住んでいない住宅をすべて数える（貸す用・売る用も含む）。法律（空き家の対策の法律）は「おおむね1年使われていない」建物を扱い、自治体が持ち主に指導できる。読み手にとっての意味: ニュースの「akiya」はたいてい統計の数字で、買える家とは限らない。正式名（Housing and Land Survey / Act on Special Measures concerning Vacant Houses）はかっこで添える | なし（短い段落2つ） | 1 |
| 2 | How many akiya are there, and how many are really abandoned? | 答え: 約900万戸（2023年、住宅の13.8%、過去最多）。そのうち「廃屋」と呼ばれるのは、貸す用・売る用・別荘のどれでもない約386万戸。段落で言う数字はこの2つだけにし、残りは表へ（playbook 3-1-6） | **表**: 区分（for rent / for sale / second homes / left unused (“other”)）× 2023年の戸数 × 2018年からの増減。表の下に「読み手にとっての意味」1文（売りに出ている空き家はごく一部） | 2 |
| 3 | Why are so many houses left empty? | 答え: 持ち主が亡くなる・施設に移ると、離れて暮らす子が相続し、住まず・売らず・壊さずに置く。理由を国交省の所有者の調査で（相続で取得した割合、空けておく理由の上位）。新築を好む傾向は、出典が取れたときだけ書く。2024年から相続の登記が義務になったことを「持ち主が分からない家を減らすため」と言い換えて1文 | 理由が3つ以上なら短いリスト可。ただし理由の説明は文章で | 3 |
| 4 | Are akiya only in the countryside? | 答え: いいえ。空き家の割合は地方の県が高いが、戸数は大都市にも多い（東京都の戸数など）。読み手にとっての意味: 「安い家」が集まるのは、割合が高く人口が減っている地方の町 | **表**: 空き家率の高い県・低い県（上位・下位3つ程度）と東京都の戸数。数字は段落に並べない | 4 |
| 5 | Is an akiya really cheap? | 答え: 値札は安いことがあるが、総額はたいてい安くない。直す費用・耐震（1981年6月の基準より前の建物かどうか）・登記や仲介の費用・毎年の税がかかる。2023年の法改正で、放置されて「管理が不十分」とされた家は土地の税の軽減が外れうる＝売り手が手放したがる理由の1つ。低い価格の家は仲介手数料が上がりうる特例（2024年）も1文。**自社の体験はここで1回だけ**（下の「自社の家に触れる場所」）。詳しい費用は将来の「Cheap and free houses」記事へ（公開されたらリンクを足す）。家の状態の幅（すぐ住める／直せば住める／建て替え・解体が前提）は表で | **表**: 値札以外にかかるもの（項目・何のため・いつ払うか）。金額は出典があるものだけ。なければ項目だけ | 5・6 |
| 6 | Where do you find an akiya for sale? | 答え: いちばん安い物件は、市町村が運営する「空き家バンク（akiya bank）」に出る。国交省が選んだ全国版のサイトで横断して見られるが、載っていない町もある。多くは日本語だけで、町によって利用の条件（移住の予定など）がある。不動産会社の一般の売り物件も別にある | **番号つきリスト**: 探す順番（①全国版のサイトで地域を絞る ②気になる町の空き家バンクのページを見る ③利用の条件を確かめる ④町の窓口に問い合わせる ⑤現地を見る）。手順以外では命令文を続けない | 7 |
| 7 | Can you buy one if you live outside Japan? | 答え: はい。日本に住んでいなくても買える。2026年4月から、海外に住む人が日本の不動産を買うと財務省への報告が要る。2026年10月から登記で国籍を届け出る。家を持ってもビザは付かない（how-long-stay へ）。国会に出ている土地の法案（成立していれば状況を更新）。**3〜4文で止め**、詳しくは akiya-try-first へ | なし | 8 |

h2 は7つ・すべて疑問形（機械採点の条件を満たす）。

### FAQ（3問以上。本文で答えたことの言い直しだけ。akiya-try-first の FAQ と同じ問いを立てない）

1. **Is an akiya the same as an abandoned house?** — No. 統計の「akiya」には貸す用・売る用・別荘も入る。廃屋に近いのは約386万戸（h2-2）。
2. **Why don’t owners just sell or knock them down?** — 所有者の調査の理由（h2-3）と、解体・税の話（h2-5）を短く。
3. **Are there free akiya in Japan?** — 空き家バンクに0円・無償譲渡の物件が出ることはある（R7 で自治体の実例が取れたときだけ。取れなければこの問いは外す）。直す費用・条件が付く。
4. **Can I search akiya banks in English?** — 全国版のサイトと自治体のページは基本的に日本語（R7 で確認できた範囲だけ書く）。

### 内部リンク（本文から2本以上）と related

- 本文から:
  - h2-5 の最後 or h2-7: `[[l:akiya-try-first|living in the town for a month before you buy]]`
  - h2-7: `[[l:how-long-stay|how long you can stay in Japan]]`（家とビザは別）
  - h2-6 の最後（任意）: `[[l:monthly-rental|renting a place by the month]]`（町を見に行くとき）
- `related`: `["akiya-try-first", "how-long-stay", "monthly-rental"]`
- 将来: 「Cheap and free houses」「Can foreigners buy property in Japan?」「Akiya banks explained」「Living in an old Japanese house」が公開されたら、h2-5・h2-7・h2-6・h2-5 からそれぞれリンクを足す（柱の役割）。
- 逆向き: akiya-try-first の冒頭の定義の文に、この記事へのリンクを1本足す（見せ方だけの変更。エンジニア部・任意）。

### 自社の家に触れる場所（1回まで）

- **h2-5**（安いのか）で、規模感として1回: 創業メンバーが下田の旧町内の古い部屋を宿にしたとき、改修 約410万円、家具・家電・備品 約240万円、準備 約7か月（`docs/brand/experience.md` 3-2、人が確認済み）。**「買った空き家ではなく、借りた部屋」と必ず断る**（他者所有の賃貸）。合計額は書かない（資料で揺れているため。experience.md の注意どおり）。
- 二芯配線・Wi-Fi 工事の話は akiya-try-first で使っているので、ここでは使わない（重複を避ける）。
- 焼津の家は契約形態・費用が非公表、写真（yaizu-engawa）も akiya-try-first で使用済みなので使わない。
- NODE Shimoda の宣伝・予約の誘導はしない（末尾の案内はテンプレートが出す）。

### トーンの注意（playbook 3-1、とくに6）

- h2-2・h2-4 は数字が多い節。**段落で言う数字は1〜2個**（約900万・約386万など）にし、残りは表へ。数字の文を3つ続けない。
- 制度は普通の言葉が先、正式名はかっこ（例: “a law on empty houses (the Act on Special Measures concerning Vacant Houses)”、“a national housing survey every five years (the Housing and Land Survey)”）。
- 「X is famous for…」「rich culture」型の書き方、図鑑調の定義からの書き出しをしない。
- 各節に「読み手にとっての意味」を1文添える（例: 売りに出ているのはごく一部 → 探すなら空き家バンク）。
- 法律・税・不動産取引は断定しない（ゲート）。「〜の場合がある」「〜とされうる」で、誰に・いつ時点かを書く。

---

## 6. リサーチ部への依頼（すべて公的な出典で。英語版があれば英語版も）

| # | 確かめること | 出典の候補 |
|---|---|---|
| R1 | 2023年住宅・土地統計調査（確報）: 空き家総数（約900万戸）・空き家率13.8%・過去最多であること。区分ごとの戸数（賃貸用・売却用・二次的住宅・賃貸売却用及び二次的住宅を除く空き家＝約386万戸）と、2018年の値（増減）。調査での「空き家」の定義（用語の解説）と、調査の日付（2023年10月1日） | 総務省統計局 `stat_housing2023`（既存の出典キー）、同調査の「用語の解説」 |
| R2 | 空家法での「空家等」の定義（居住その他の使用がなされていないことが常態）と、国の基本指針の「おおむね年間を通して使用実績がない」の目安。英語の法令名 | e-Gov 法令検索（空家等対策の推進に関する特別措置法）、国交省の基本指針・空き家対策のページ |
| R3 | 2023年の都道府県別の空き家率（高い県・低い県それぞれ上位3）と、東京都の空き家の戸数。大都市にも戸数が多いことが言える数字 | 総務省統計局（同調査の都道府県別の結果） |
| R4 | 空き家の持ち主の実態: 相続で取得した割合、所有者の住まいとの距離、空けておく理由・売らない理由の上位（最新の調査年） | 国交省「空き家所有者実態調査」（令和元年など最新版） |
| R4b | 相続登記の義務化（2024年4月1日から、期限・対象）。目的を普通の言葉で言える公式の説明 | 法務省（相続登記の申請義務化） |
| R5 | 2023年の空家法の改正（施行日）: 「管理不全空家」の新設、勧告を受けると固定資産税の住宅用地特例が外れる（特定空家と同じ扱い） | 国交省（改正空家法の概要）、e-Gov |
| R6 | 新しい耐震基準が1981年6月1日から適用されたこと。国・自治体の耐震診断・改修の補助がある、という一般的な事実（個別の額は不要） | 国交省（住宅・建築物の耐震化）、可能なら住宅・土地統計調査の「建築の時期」 |
| R7 | 空き家バンク: 国交省が選んだ全国版空き家・空き地バンク（運営会社2社）と、参加している自治体の数（時点つき）。自治体ごとに運営し、全国版に載らない町もあること。利用の条件の実例を1つ（例: 移住・定住の意思、登録の要件。伊豆・静岡の町の空き家バンクだと流れがよい）。0円・無償譲渡の物件が自治体の空き家バンクに出ている実例（自治体のページで、時点つき。取れなければ FAQ 3 を外す）。英語で検索できるかどうか | 国交省（全国版空き家・空き地バンク）、各自治体の空き家バンクのページ |
| R8 | 低い価格の空き家などの仲介手数料の特例（2024年7月1日施行。800万円以下の物件で、上限 30万円×1.1 など） | 国交省（宅建業者が受け取れる報酬額の告示の改正） |
| R9 | 外国人の購入（akiya-try-first と同じ出典で、2026-11-21 時点に更新）: 財務省への事後報告（2026年4月〜）、登記での国籍の届け出（2026年10月〜）、国会に出ている土地の法案（衆議院の議案の審議状況。成立していれば内容と施行時期） | `mof_fefta2026`・`mof_realprop_faq`・`moj_nationality`・`shugiin_bill18`・`cao_land_bill_outline`（既存） |
| R10 | 検索数: what is an akiya / akiya houses / japan empty houses / abandoned houses in japan（米国の月間・KD。調べられたら出どころつきで1節目の表を更新） | キーワード調査ツール |
| R11（任意） | 地方の町の、古い一戸建ての実際の取引価格の例（公的データで1〜2件、時点つき）。上位ページにない一次情報になる | 国交省 不動産情報ライブラリ（不動産取引価格情報） |

使わない: 民間の将来推計（NRI の「3戸に1戸」など）、物件サイトの掲載件数・価格の幅、ニュースの転載の数字。

---

## 7. 写真

- 見出し写真に欲しい絵: **古い木造の日本家屋の外観**。手入れが止まった感じ（雨戸が閉まっている・庭に草）はよいが、崩れた廃墟の見せ物（ruin porn）にはしない。人の顔・表札・看板・車のナンバーなし。
- 既存の `photos/` からは選べない: `yaizu-engawa`（akiya-try-first で使用済み）・`empty-tatami-room`（Own の入口で使用中）・`town-lane`（Live の入口）・`coastal-village`（トップ）。記事の写真は1枚を1つの記事にだけ使う。
- **Unsplash で探す**（`PHOTO_PLAN.md` の手順。`download_asset` で記録、クレジットは `PHOTO_CREDITS`）。検索語の例: `old japanese house` / `kominka` / `japanese wooden house` / `rural japan house`。2026-11-14 の候補 `Kjbhq8BJZTE`（軽トラ・トタンの小屋・古い家と緑の山、Loris Boulinguez）は未使用なので、まず画像を見て合うか確かめる。
- alt・説明文は写っているものだけ（地名を書かない。playbook 4-3、`PHOTO_PLAN.md` の決まり）。

---

## 8. 外部のページの命令

検索結果の要約に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。akiyajapan.com・akiya2.com・tokyocheapo.com は環境のネットワークで開けず、中身は検索結果の要約だけで判断した（上位ページの穴の判断を確かめるなら、編集長がこの3つを許可に足す）。

---

## リサーチメモ（2026-11-21）

リサーチ部。すべて 2026-11-21 に確認。「開いて確認」＝ curl でページ・PDF を開いて本文を読んだもの。「検索結果で確認」＝ ページが開けず、検索結果の要約だけで確かめたもの（執筆部は数字の言い切りを避け、出典の扱いに注意）。

### R1 空き家の数と区分（2023年住宅・土地統計調査）

| 事実（英語で1文） | 出典 | 確認 | 時点 |
|---|---|---|---|
| Japan had 9,002,000 vacant dwellings, a record high, and 13.8% of all housing (also a record). | 総務省統計局「令和5年住宅・土地統計調査 住宅及び世帯に関する基本集計（確報集計）結果の概要」2024-09-25 `stat_housing2023`（既存） | 開いて確認 | 2023-10-01 |
| That was up 513,000 from 8,489,000 in 2018 (13.6%); the number has roughly doubled in the 30 years since 1993. | 同上 | 開いて確認 | 2018→2023 |
| By type (thousand): for rent 4,436 (2018: 4,327, +109) / for sale 326 (293, +33) / second homes 384 (381, +3) / “other” vacant (not for rent, sale or second use) 3,856 (3,487, +369). | 同上 表2-1 | 開いて確認 | 2023-10-01 |
| The “other” group is 5.9% of all housing and 42.8% of vacant homes; for rent is 49.3%. | 同上 | 開いて確認 | 同上 |
| Of 3.52 million vacant detached houses, 80.9% (2.85 million) are in the “other” group; 78.5% of vacant apartment units are for rent. | 同上 表2-2 | 開いて確認 | 同上 |
| The survey counts a dwelling as vacant if no household usually lives there on the survey day; the “other” group includes homes empty for a long time because the occupant moved or is in hospital, and homes due to be torn down. | 総務省統計局（英語）“Explanation of Terms of the 2023 Survey” | 開いて確認 | 2023年調査 |
| The survey is held every five years (since 1948; 2023 was the 16th). | `stat_housing2023` | 開いて確認 | — |

- 記事での書き方: 段落は「約900万戸・13.8%・過去最多」と「“other” が約386万戸」の2つだけ。表は4区分×2023年×2018年からの増減（上の数字）。“For sale” はわずか約33万戸＝「売りに出ている空き家はごく一部」が読み手にとっての意味（ただし統計の「売却用」は売り出し中の空き家の数で、空き家バンクの件数とは別物）。廃屋に近い層は一戸建てに偏る、も1文で使える。
- In short 2 の “Most are waiting for a tenant or buyer” は、賃貸用＋売却用＝約476万戸（52.9%）なので「半分強」と書くのが正確。
- 英語の区分名は統計局の英訳に合わせる: For Rent / For Sale / As Second Dwellings / “Vacant, Excluding For Rent, For Sale and As Second Dwellings”。

### R2 法律の定義

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| Under the Act on Special Measures concerning Vacant Houses (2014), a “vacant house” is a building that is normally not lived in or otherwise used, together with its land (houses owned by the state or local governments are excluded). | e-Gov 法令検索「空家等対策の推進に関する特別措置法」（平成26年法律第127号）第2条1項 | 開いて確認（e-Gov API） | 2026-09-03 施行の版 |
| The national guideline says that a building showing no use for roughly a whole year is one yardstick for “normally not used”. | 国交省「空家等に関する施策を総合的かつ計画的に実施するための基本的な指針」（最終改正 2026-09-03） | 開いて確認 | 同上 |
| A “specified vacant house” is one that, if left alone, risks collapse or is seriously unsanitary, unsightly, or otherwise harmful to the neighbourhood. | 同法 第2条2項 | 開いて確認 | 同上 |

- 記事での書き方: 「統計は調査日に人が住んでいない住宅をすべて数える／法律はおおむね1年使われていない建物を扱い、市町村が持ち主に助言・指導できる」。「6か月以上空いている家」という定義は、公的な出典が見つからないので書かない。
- 法令名の英訳は政府の公式英訳を確認できていない。“a law on empty houses (often called the Vacant Houses Act)” のように説明で書き、正式な英語名として断定しない。

### R3 都道府県別（2023年）

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| Highest vacancy rates: Tokushima 21.3%, Wakayama 21.2%, Kagoshima 20.5% (next Yamanashi 20.4%, Kochi 20.3%, Nagano 20.1%). | `stat_housing2023` 付表（都道府県別の主な指標） | 開いて確認 | 2023-10-01 |
| Lowest: Saitama 9.3%, Okinawa 9.4%, Kanagawa 9.8%. | 同上 | 開いて確認 | 同上 |
| Tokyo has the most vacant homes of any prefecture, 897,000 (10.9%), followed by Osaka 702,000; but only 214,000 of Tokyo’s are in the “other” group (2.6% of housing). | 同上 | 開いて確認 | 同上 |
| Shizuoka: 296,000 vacant, 16.7%. | 同上 | 開いて確認 | 同上 |

- 記事での書き方: 表に高い3県・低い3県・東京都。読み手にとっての意味＝「戸数は都会に多いが、その多くは空室の賃貸。放置型が多いのは地方」（東京は“other”の割合が2.6%、和歌山・徳島は12%台）。

### R4 持ち主の実態（国交省 令和6年空き家所有者実態調査。2025-08-29 公表。令和元年版より新しいのでこちらを使う）

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| About 58% (57.9%) of owned vacant homes were inherited. | 国交省「令和6年空き家所有者実態調査 結果のポイント」 | 開いて確認 | 調査基準日 2024-12-01 |
| Of inherited vacant homes, over 70% were built in 1980 or earlier, and about 58% became empty when the occupant died (11.3% after moving into a care home). | 同上 | 開いて確認 | 同上 |
| About 80% of vacant homes are within an hour (on foot, or by car or train) of the owner’s home. | 同報告書（図表3関連「所有世帯の居住地からの所要時間」） | 開いて確認 | 同上 |
| Owners who plan to keep a home empty most often say they need it for storage (56%), don’t want to pay for demolition (47%), or the house is too old (37%); 28% say demolishing would raise their property tax. | 同報告書 図表3-45（複数回答、N=32.3万世帯） | 開いて確認 | 同上 |
| Among owners of unused vacant homes, about 40% plan to keep them empty, and just under 40% plan to demolish or sell. | 結果のポイント | 開いて確認 | 同上 |
| In the 2023 housing survey too, 61.6% of household-owned “other” vacant homes were acquired by inheritance or gift, and about 70% were built in 1980 or earlier. | 総務省統計局「住宅の構造等に関する集計（確報集計）結果の概要」2025-01-29 | 開いて確認 | 2023-10-01 |

- 記事での書き方: 「約6割が相続」「多くは持ち主の死がきっかけ」「物置に使う・解体費を払いたくない・古すぎる」。ブリーフの仮説「持ち主は遠くに住む」は**逆**: 約8割は1時間以内に住んでいる。「離れて暮らす子が相続」とは書かない。「新築を好む傾向」は今回の公的な出典で確認していないので書かない。

### R4b 相続登記の義務化

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| Heirs who acquire real estate must apply to register the transfer within three years of learning they inherited it; failing to do so without good reason can bring a non-criminal fine of up to ¥100,000. | e-Gov「不動産登記法」第76条の2・第164条 | 開いて確認 | 現行（2026-06-24 施行の版） |
| The duty took effect on 1 April 2024 and also covers inheritances before that date; those must be registered by 31 March 2027. | 法務省「相続登記の申請義務化について」 | **検索結果で確認**（moj.go.jp が開けない） | — |

- 記事での書き方: 「2024年から、家を相続したら3年以内に登記することが義務になった。持ち主の分からない家や土地を減らすため」。目的の言い回しは法務省のページを読めていないので、「持ち主を分かるようにするため」程度の一般的な説明にとどめる。過料の額は書かなくてよい（読み手に不要）。

### R5 2023年の空家法の改正

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| An amendment in force since 13 December 2023 created a new category of “poorly managed vacant houses” that could become dangerous if left alone; the town can give the owner guidance and then a formal recommendation. | 国交省「空家等対策の推進に関する特別措置法の一部を改正する法律」概要（令和5年法律第50号）／e-Gov 同法 第13条 | 開いて確認 | 施行 2023-12-13 |
| Once such a recommendation is issued, the land loses the residential-land property tax reduction (which cuts the tax base to 1/6, among other rates). | 国交省 改正法の概要 | 開いて確認 | 同上 |

- 記事での書き方: 「放置して“管理が不十分”と勧告されると、土地の税の軽減が外れうる」→ 売り手が手放したい理由の1つ。「税が6倍になる」とは書かない（軽減が外れる仕組みの説明にとどめる）。

### R6 耐震

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| Buildings designed under the older seismic standard, before the revised standard applied from June 1981, often lack enough earthquake resistance; the ministry urges owners of pre-1981 buildings to get a seismic assessment. | 国交省「住宅・建築物の耐震化について」／国交省資料「新耐震基準（昭和56年6月～）」 | 開いて確認 | — |
| National and local governments offer joint support for seismic assessments and retrofits. | 国交省「住宅・建築物の耐震化について」 | 開いて確認 | — |
| About 70% of household-owned “other” vacant homes were built in 1980 or earlier. | `stat_housing2023_structure` | 開いて確認 | 2023-10-01 |

- 記事での書き方: 「1981年6月より前の基準で建てられた家かどうか」。日付（6月1日）までは出さない（判定は建築確認の日による、など細かいため）。補助の額は書かない（自治体で違う）。

### R7 空き家バンク

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| The ministry’s national akiya bank lets you search listings from many municipalities in one place; it is run by two companies chosen by public tender, LIFULL and At Home, and has been fully running since April 2018. | 国交省「空き家・空き地バンク総合情報ページ」／「『全国版空き家・空き地バンク』について」 | 開いて確認 | — |
| 1,155 municipalities take part, 750 of them currently have listings, and about 29,000 properties have found buyers or tenants (municipal survey estimate). | 国交省「『全国版空き家・空き地バンク』について」 | 開いて確認 | 2026-10-31 |
| About 20,000 listings were live at the end of the month (both sites combined, with duplicates). | 国交省「参加自治体数・物件掲載件数推移」 | 開いて確認 | 2026-10末 |
| Nationwide, 65.5% of municipalities take part, so some towns’ banks are not on the national site. | 国交省「都道府県別 参加表明状況」 | 開いて確認 | 2026-10末 |
| Banks differ by town: Shizuoka City’s bank covers only homes inside its urbanised zone, and only real-estate agents can list properties. | 静岡市「静岡市空き家情報バンク」 | 開いて確認 | 2026-11 |
| Kamiichi Town (Toyama) runs a “zero-yen” akiya bank where owners give away land and house free; two houses (built 1965 and 1968) were listed as of 18 November 2026. | 上市町「上市町0円空家バンク」（更新 2026-11-18） | 開いて確認 | 2026-11-18 |
| In Kamiichi’s scheme, the town only shares information; buyer and owner negotiate directly, and the new owner pays registration costs, repairs, moving, gift tax, real-estate acquisition tax and property tax. | 上市町「0円空家バンク及び空家解消特別推進事業の流れ」 | 開いて確認 | — |

- 記事での書き方: FAQ 3（free akiya）は**残してよい**。上市町を例に「0円の家は実在するが、税・登記・修繕は自分持ち」。物件の詳細（住所・番号）は書かない（すぐ変わる）。
- **書かないこと**: 「英語で検索できるか」— 全国版の2サイト（homes.co.jp・akiya-athome.jp）が開けず確認できない。FAQ 4 は外すか、「自治体のページは基本的に日本語」も含めて確認できるまで書かない。伊豆の町の利用者側の条件（移住の意思など）は確認できなかったので書かない（下田市の空き家バンクの本体ページは見つからず）。

### R8 仲介手数料の特例

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| Since 1 July 2024, for properties priced at ¥8 million or less, an agent may charge up to ¥300,000 plus tax (×1.1) per client, above the normal percentage cap, to cover the cost of handling them; the agent must explain and agree the fee in advance. | 国交省「空き家等に係る媒介報酬規制の見直し」（令和6年6月公布・7月1日施行） | 開いて確認 | 2024-07-01 施行 |

- 記事での書き方: 「安い家ほど、仲介手数料が価格に比べて高くなることがある（上限 30万円＋税）」。

### R9 外国人の購入（akiya-try-first と同じ出典の更新）

| 事実 | 出典 | 確認 | 時点 |
|---|---|---|---|
| From 1 April 2026, non-residents buying Japanese property, including homes to live in, must file an after-the-fact report with the Ministry of Finance (within 20 days of acquisition). | `mof_fefta2026`・`mof_realprop_faq` | 開いて確認 | 2026-11-21 時点で変更なし |
| Buyers state their nationality at registration from 5 October 2026. | `moj_nationality` | **今回は開けず**（moj.go.jp）。既存記事で確認済みの内容をそのまま使う | 前回確認 |
| The land bill (cabinet bill no. 18, 222nd Diet) was received by the House of Representatives on 23 October 2026 and referred to the Cabinet Committee on 10 November 2026; it has not passed. | `shugiin_bill18` | 開いて確認 | 2026-11-21 |

- 記事での書き方: 「国会で土地の法案を審議中（2026年11月時点で未成立）」。内容の細部は akiya-try-first に任せる。

### R10 検索数 → 書かない（未調査）

キーワード調査のツール（OpenRush・OpenSEO）がこの部署の実行環境で使えず、数字を取れなかった。1節目の表は戦略部の既存の数字のまま。編集長側で必要なら別途。

### R11 取引価格の実例 → 書かない

国交省 不動産情報ライブラリの API は鍵が必要（401）、Web 画面は curl では中身が取れない。確認できなかったので記事に使わない。

### ブリーフの仮説で直すべき点（執筆部へ）

- 「離れて暮らす子が相続し…」→ 所有者の約8割は1時間以内に住む。「相続した家を、物置にしたり解体費を惜しんだりして置いておく」に書き換える。
- 「新築を好む傾向」→ 公的出典なし。書かない。
- 「6か月以上」の定義 → 公的出典なし。誤りとして触れるなら「公式の定義ではない」とだけ。
- 法令名の英語の正式名 → 未確認。説明的に書く。

### 海外の読み手の疑問（検索で集めたもの。要約）

- 0円・数百ドルの家は本当にあるのか、なぜそんなに安いのか（裏に何があるのか）。
- 外国人・日本に住んでいない人が買えるか。家を持てば住めるのか（ビザ）。
- 日本に住んでいないとローンが組めず、現金で買うしかないのか。
- 直す費用が値段を大きく上回るのでは。建て替えが前提なのか。
- 買ったあとの税金や、放置したときのペナルティ。
- 田舎すぎて車がない・店がない場所ばかりではないか。
- 物件を英語で探せるか、どこから始めればよいか。

### 新しく使う出典（`SOURCES_NEW` 用）

```python
"stat_housing2023_terms": ("https://www.stat.go.jp/english/data/jyutaku/pdf/05terms.pdf", "Statistics Bureau of Japan (terms)", "総務省統計局（用語の解説・英語）",
                           "Statistics Bureau of Japan: Explanation of Terms of the 2023 Housing and Land Survey"),
"stat_housing2023_structure": ("https://www.stat.go.jp/data/jyutaku/2023/pdf/kouzou_gaiyou.pdf", "Statistics Bureau of Japan, 2025", "総務省統計局（住宅の構造等に関する集計）",
                               "Statistics Bureau of Japan: 2023 Housing and Land Survey, tabulation on housing structure (January 2025)"),
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
                          "Real Property Registration Act, Act No. 123 of 2004, Articles 76-2 and 164 (e-Gov)"),
"moj_inheritance_reg": ("https://www.moj.go.jp/MINJI/minji05_00565.html", "Ministry of Justice", "法務省（相続登記の申請義務化）",
                        "Ministry of Justice: Mandatory registration of inherited real estate"),  # 今回は検索結果でのみ確認
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
```

### 開けなかったドメイン

- `www.moj.go.jp`・`houmukyoku.moj.go.jp`（CloudFront の 403 “Request blocked”。相続登記のページ、`moj_nationality` の PDF）
- `www.gov-online.go.jp`（プロキシで拒否）
- `www.homes.co.jp`・`www.akiya-athome.jp`（全国版空き家バンクの2サイト。接続できず → 英語で検索できるかを確認できない）
- `www.reinfolib.mlit.go.jp` の API（鍵が必要。ネットワークではなく認証の問題）

### 外部ページの命令

開いたページ・検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。
