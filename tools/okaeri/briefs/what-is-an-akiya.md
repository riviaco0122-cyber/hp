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
