# 見直し方針: akiya-try-first（slug: akiya-try-before-you-buy）

戦略部 2026-11-15。対象は `tools/okaeri/content.py` の ARTICLES `id: akiya-try-first`。入口は Own a home（`topic: own`、`also: ["live"]`）のまま。URL（slug）は変えない。

---

## 1. いまの点数

### 機械採点 39/40（`python3 tools/okaeri/article_score.py akiya-try-first`、2026-11-15）

| 項目 | 点 | メモ |
|---|---|---|
| title の長さ | 2/2 | 55字 |
| 主な検索語の位置 | 3/3 | 「akiya」が10字目 |
| description | 3/3 | 159字 |
| In short | 4/4 | 4項目 |
| h2 の数 / 形 | 2/2・2/2 | 6個、すべて疑問形 |
| FAQ | 4/4 | 3問 |
| 出典 | 5/5 | 5件（公的 2件: mlit, isa） |
| **内部リンク** | **1/2** | 本文からは `izu` の1本だけ（しかも自社の家の節の中） |
| 関連記事 | 2/2 | izu-from-tokyo, izu |
| 文の長さ | 2/2・2/2 | 平均10.9語、30語超 2% |
| NG 語・綴り | 4/4・3/3 | なし |
| メモ | — | 黄色い枠 1か所（月額・30泊以上・「再生した空き家」と呼べるか・修善寺と焼津） |

### 品質60の見立て（playbook 4-3。前回の品質保証部の採点は log に無し）

| 項目 | 見立て | 理由 |
|---|---|---|
| 正確性 20 | 12〜14 | ①「Visitors from visa-exempt countries can generally stay up to 90 days」に**出典が付いていない**（外務省へのリンクも無い）→ 出典なしの制度の記述はゲートに当たる恐れ。②デジタルノマドの条件から「**ビザ免除かつ租税条約のある国・地域の国籍**」という条件が抜けている（出典より弱い・不正確）。「It cannot be renewed」も、出入国在留管理庁の書き方（再申請の扱い）と照らす必要。③3.85百万戸の出典が民間ニュース（Data Max）。総務省統計局の確報（2024年9月公表）で直接言える。④900万戸の出典が「MLIT, citing…」で、出典の名前があいまい（-1） |
| 検索意図への回答 10 | 5〜6 | 主な語が「akiya」（3,600）なのに、記事は「買う前に住む」の話。「akiya」で来た人の疑問（定義・数・安い理由・買い方）には浅くしか答えず、「買う前に住む」で来た人の疑問（**どこに1か月泊まれるか＝自治体のお試し住宅・マンスリー**、何を確かめるか、建物の何を見るか）にも足りない |
| 独自性・一次情報 10 | 4前後 | 自社の確認済みの体験（下田で古い家を改修して宿にした経験）が**記事に1つも使われていない**。`experience.md` 3-2 に、確認済みで記事に出してよい一次情報（二芯配線で家電の同時使用に制約、Wi-Fi 工事に2か月以上、工事車両の駐車で近隣から指摘、改修 約410万円・準備 約7か月）があるのに、いまは「7つの疑問」の一般論で終わっている |
| 英語の自然さ 5 | 4〜5 | 平易。「The house is the cheap part. The commitment is the town.」は良い |
| 読みやすさ 5 | 4 | 「1か月で確かめること」は箇条書きだが、「どう確かめるか」が無い。滞在の方法（観光の90日・デジタルノマド・自治体のお試し住宅・マンスリー・宿）は**比べる情報なのに表がない**（-1） |
| 導線 5 | 3 | 自社の家の節が h2 1つ分を使い、写真も入って宣伝の比重が大きい（-2 の恐れ）。次に読む記事が `izu` だけ |
| 写真 5 | 4 | 見出し写真は自社の焼津の家（リフォーム前と明記）で中身に合う。説明文「One of our houses」は、焼津が開業前の計画で、契約形態も非公表（`experience.md` 8章）なので言い方を確認したい |

**見込み: 機械39＋品質 約36〜40 ＝ 約75〜79点。** 主因は「検索語と中身のずれ（共食いの恐れも）」「出典の無い制度の記述」「一次情報を使っていない」。

---

## 2. 狙う検索語と検索意図

### 主な語を「akiya」から外す（共食いの解消）

`review_ja.py` の ROADMAP では、「akiya」（3,600）・「akiya japan」（1,300）は **3「What is an akiya?」**、「cheap houses in japan」（1,900）は **4「Cheap and free houses」**、「can foreigners buy property in japan」は **1** が受ける。KEYWORDS でもこの記事は「買う前に住む（この切り口の語はまだ検索が少ない）／上の記事から読者を受ける」と位置づけられている。いまの `keywords` は親記事の語を先取りしていて、親記事を書いた時点で共食いのゲートに当たる。

| 役割 | 検索語（案） | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| 主な語 | buying an akiya in japan（または buy akiya japan） | 未調査 | — | リサーチ部に依頼（R9）。上位は akiyajapan・housingjapan・realestate.co.jp・e-housing の「買う前に知ること」で、意図が近い |
| 関連 | living in an akiya / rent before buying house japan / trial stay rural japan / otameshi jutaku | 未調査 | — | 同上 |
| 関連（残す） | akiya | 3,600 | 0 | KEYWORDS。本文中で自然に出る程度。`keywords` の先頭には置かない |

title は主な語を前半に置いたまま、いまの形（「Buying an Akiya in Japan? Live in One for a Month First」）がそのまま使える。

- 入口: **Own a home**（also: Live part-time）
- 検索意図: **Do**（買う前に何をすればよいか）。その先で本当に困っていること: 「安いからと買って、住めない・直せない・町になじめない家を抱えたくない」「下見の旅行（数日）では判断できない」「どこに、どのビザで、1か月泊まればよいか分からない」。

### 読み手の疑問（品質保証部はこれで採点する）

1. Should I live in the town before I buy an akiya?
2. What can’t I learn from an akiya listing or a short viewing?
3. How long can I stay in Japan to try a town, and which visa do I need?
4. Where can I stay for a month in a small Japanese town (municipal trial homes, monthly rentals, short-stay houses)?
5. What should I check during a trial month, week by week?
6. What problems in an old Japanese house only show up once you live in it (cold, wiring, internet, damp)?
7. Does buying an akiya give me a visa or residency?（短く答え、ROADMAP 1 の記事へ送る）

---

## 3. 上位ページの穴（2026-11-15 に英語で検索）

検索「buying an akiya in Japan what to know before you buy」の上位: realestate.co.jp（Real Estate Japan）、housingjapan.com「Read this before buying an akiya」、e-housing.jp（2025年9月）、akiyahub.com の確認リスト、Business Insider、akiyajapan.com の長い購入ガイド（2025年4月）と点検リスト（2026年2月）、globallawexperts、oldhousesjapan、allakiyas、akiyaportal。
検索「akiya try living before buying trial stay」の上位: akiyajapan.com「Building a life in Japan around your visa」（2026年4月）、oldhousesjapan「Renting before buying: is it worth it」、**akiyahub.com の「monthly rentals」（買う予定の人向けに30日以上の滞在を売っている）**、japanesetaste、housingjapan。

具体的な穴:

1. **上位のほとんどが売る側**（不動産会社・物件サイト・購入代行）。「買う前に住んでみる」を勧めるページも、自社の物件・自社のマンスリーに送る作り。→ この記事の「私たちは家を売らない」という立場は差になる（ただし書いてよいかは人の確認。B5）。
2. **自治体の「お試し住宅（お試し移住）」の制度に、英語の上位が答えていない**。oldhousesjapan が「多くの自治体にある」と一言触れるだけで、どこで探すか、外国籍・観光の在留資格で使えるか、最短・最長の日数、料金の目安が無い。公的な出典（自治体・移住ポータル）で書ければ、上位にない一次情報になる。
3. **制度の数字に時点と出典が無い**: 90日、デジタルノマドの条件（年収1,000万円・保険・**対象国**）、「12か月で180日を超えると入国審査で問われる」といった話が、出典なしで書かれている。→ 外務省・出入国在留管理庁の一次情報で、時点つきで書く。
4. **運営者の体験が無い**: 上位は「寒い」「直すと高い」の一般論。古い家を実際に改修して1年以上運営した人の、具体的な落とし穴（古い配線で家電を同時に使えない、回線の工事に2か月以上、工事車両の駐車で近所から指摘、地元の工務店の条件が補助金に付く）を書いたページは無い。→ 確認済みの一次情報で書ける（B3）。
5. **建物そのものの点検が「住んで確かめる」と結びついていない**: 上位は「1981年6月より前の建物は旧耐震」「購入価格の外に7〜10%の費用」を挙げるが、「住んでいる間に何を見ておくか」の形になっていない。→ 1か月の手順に、建物の点検の項目（出典つき）を足すと、買う前の行動に直結する。

---

## 4. 直す点

### A. 見せ方だけ（90点以上なら人の確認なしで入れてよい）

| # | 直す点 | 理由 |
|---|---|---|
| A1 | `keywords` を 2章の案に差し替える（主な語は「buying an akiya in japan」系。数値はリサーチ部の結果で）。「akiya」「cheap houses in japan」「akiya japan」を先頭から外す | ROADMAP 1・3・4 との共食いを先に防ぐ（ゲート） |
| A2 | h2「What is an akiya?」を独立の節として残さず、dek か最初の節の1〜2文に縮める（数字はいまの出典のまま）。h2 の枠は「Where can you stay for a month to test a town?」に回す | 親記事（ROADMAP 3）の役割を先取りしない。検索意図（疑問4）に枠を使う |
| A3 | h2「Can foreigners buy an akiya?」も短くし（2文）、In short と FAQ の答えはいまの範囲のまま。ROADMAP 1 の記事ができたら、ここからリンクする（それまでは張らない） | ROADMAP 1 との共食い防止。いまの答え自体は残す |
| A4 | 本文の内部リンクを2本以上にする: ①「How long can you stay…」または新しい「Where can you stay…」の節で、1か月泊まれる場所の例として `[[l:izu-from-tokyo|the Izu Peninsula, two to three hours from Tokyo]]` ②自社の家の節の `[[l:izu|Izu Peninsula]]`（いまある）。ja も同じ位置に `[[l:ja-izu-from-tokyo|…]]` などで | 機械採点 1/2 → 2/2。読み手が「試す町」を具体的に想像できる先へ送る |
| A5 | 「滞在の方法」を**表**にする（行: 観光の短期滞在／デジタルノマド／自治体のお試し住宅／マンスリー・宿。列: 最長の日数／条件／向いている人／出典）。表の中身は B の確認が済んだものだけ | 比較なのに表がない（読みやすさ -1）。上位ページの穴 2・3 への答えを一目で出す |
| A6 | 「Why live in the town…」の7項目を、「何を確かめるか／どう確かめるか」の2列の表にするか、各項目に「どう確かめるか」を一言ずつ足す（例: 回線 → 仕事の日に実際に使う。ごみ → 役所で収集日を聞く）。新しい事実は足さない | いまは疑問の羅列で、行動につながらない（Do の意図） |
| A7 | 自社の家の節を短くし、h2 を読み手の疑問の形にする（例: 「Can you stay in a renovated old house before buying one?」）。写真は1枚のまま、本文は2〜3文に。末尾の案内はテンプレートが出すので重ねない | 宣伝の比重を下げる（導線 -2 の恐れ）。playbook 2-6（言及は1回まで） |
| A8 | `related` を `["izu-from-tokyo", "izu"]` のまま。ROADMAP 1・2・3 の記事ができたら差し替える | 役割分担（6章） |

### B. 事実・数字・出典・主張を変える（`ja.review` と log に「人の確認が必要な点」として必ず書く）

| # | 直す点 | 理由 |
|---|---|---|
| B1 | 90日の記述に**外務省の出典と時点**を付ける（「2026年11月時点」など）。本文と ja の両方 | 出典なしの制度の記述（ゲート） |
| B2 | デジタルノマドの条件を出入国在留管理庁のページどおりに直す: 対象国・地域（ビザ免除かつ租税条約）、年収1,000万円以上、民間の医療保険、6か月、更新できない／再び申請できる条件。時点を付ける | 条件の書き漏れ（正確性）。ビザの記述は playbook 6章で人の確認が必須 |
| B3 | 「古い家で、住んでみて初めて分かること」の節（または 7項目の中）に、**確認済みの自社の体験を1〜3点**入れる。使えるのは `docs/brand/experience.md` 3-2（人が確認済み）の範囲だけ: 古い住居の二芯配線で、エアコン・冷蔵庫・電子レンジの同時使用に制約が出た／回線の工事が繁忙期で申し込みから2か月以上かかった／工事車両の駐車で近所から指摘を受けた。書き方は「創業メンバーが下田で借りた古い家を宿に改修したとき」（**RIVIA&CO. が開業、とは書かない**。物件は他者所有の賃貸で、空き家を買った体験ではないことも明記する） | 独自性（一次情報0件 → 最大4点の縛りを外す）。上位ページにない視点 |
| B4 | 「Where can you stay for a month…」の節を新しく書く: 自治体のお試し住宅（制度の概要・探し方・外国籍の人が使えるかは自治体ごと）、マンスリーの部屋、宿。数字・条件はリサーチ部が確かめたものだけ | 読み手の疑問4（いまは答えが無い）。上位ページの穴2 |
| B5 | 「We do not sell houses or act as agents」を確認する。`experience.md`（2026-10-11 人が確認済み）では RIVIA は「買取・借り上げ・運営受託」に対応しており、アキヤドでは「買取プラン」を出している。「売買の仲介はしない」「家を売っていない」は事実か、Okaeri では言わない方がよいか | 主張の事実確認（ゲート: 事実の誤り） |
| B6 | 自社の家の節の「We look after homes in small towns in Shizuoka」（複数形・静岡に限定）を、確認済みの範囲に直す。NODE Shimoda 以外の施設名・数は非公表。焼津は「2026年末に開業を予定」、広島県竹原市は「2027年4月に開業を予定」までは書いてよい（`experience.md` 8章）。**修善寺は `experience.md` に記述が無い**（黄色い枠の「Add Shuzenji」も含め、人に確認） | 確認済みでない自社の体験・実績（ゲート） |
| B7 | 「restored akiya」と呼べるか: `experience.md` 3章（サイトの記載）に「下田市旧町内の空き家を改修した滞在型アパート」とある。この言い方で黄色い枠の1点目を埋めてよいか人に確認。月額料金・30泊以上を常に受けられるかは記述が無いので、枠のまま残す | 黄色い枠の解消（人の確認） |
| B8 | 3.85百万戸の出典を Data Max から**総務省統計局「令和5年住宅・土地統計調査」**（確報の概要）に差し替える。900万戸・13.8% の出典名も「MLIT, citing…」から統計局（または国交省の資料名を正確に）にする。900万戸は速報値で確報の総数と同じかも確認 | 公的な一次の出典へ（正確性・出典の名前のあいまいさ -1） |
| B9 | 写真の説明文「One of our houses, in Iwashigashima, Yaizu, before renovation.」を確認: 焼津は開業前で、契約形態・所有は非公表（`experience.md` 8章）。「A house in Iwashigashima, Yaizu, that we are preparing to open, before renovation.」のような言い方でよいか | 実績物件の契約形態を推測させない（法務・配慮） |
| B10 | 1か月の手順（Week three など）に、建物の点検の項目を出典つきで足すかを検討: 1981年6月の新耐震基準（建築確認の日付）、自治体の空き家の窓口で聞くこと、改修の補助金の条件（地元業者の指定がありうる）。出典は国交省・自治体だけ | 上位ページの穴5。制度の記述なので人の確認 |

---

## 5. リサーチ部への依頼

| # | 確かめること | 優先の出典 |
|---|---|---|
| R1 | 短期滞在の査証免除: 対象の国・地域と、滞在できる日数（90日が原則、例外の国）。2026年11月時点。JESTA（電子渡航認証）の導入予定の時期 | 外務省 |
| R2 | 特定活動（デジタルノマド）の条件の全部: 対象国・地域、年収、保険、期間、更新・再申請、家族の帯同。2026年11月時点 | 出入国在留管理庁 |
| R3 | 令和5年住宅・土地統計調査の確報: 空き家総数・空き家率、「賃貸・売却用及び二次的住宅を除く空き家」385万戸・5.9%。公表日と、英語の資料（Statistics Bureau の English page）の有無 | 総務省統計局（stat.go.jp の `kouzou_gaiyou.pdf` など） |
| R4 | 自治体の「お試し住宅（お試し移住）」: 制度の一般的な形（日数・料金の幅）、全国の探し方（移住ポータル）、外国籍の人・観光の在留資格の人が使えるかの扱い。静岡県内（伊豆の市町）の例があれば | 自治体・都道府県・移住ポータル（JOIN など）の公式 |
| R5 | 新耐震基準（1981年6月1日）の英語での説明に使える公的な出典 | 国土交通省 |
| R6 | 外国人が日本の不動産を買うときの規制の現状（2026年時点で、国籍・在留の条件が無いことに変わりないか。重要土地等調査法など、取引の届出に関する制度の有無） | 法務省・国交省・内閣府。いまの出典（housingjapan・realestate.co.jp）は二次として残す |
| R7 | 空き家バンクの扱い（外国籍の人が登録・利用できるか）は ROADMAP 10 の範囲。この記事では触れる場合だけ一言 | 自治体 |
| R8 | 人に確認（編集長から）: B5〜B7・B9 の自社の記述、NODE Shimoda の月額料金・30泊以上の受け入れ、修善寺の状況 | 人 |
| R9 | 検索語の月間検索数と KD: buying an akiya in japan / buy akiya japan / living in an akiya / rent before buying japan / otameshi jutaku / trial stay rural japan | 調査ツール（KEYWORDS と同じ方法） |

---

## 6. 3記事の役割分担と内部リンク

| 記事 | 入口 | 主な語 | この記事だけが答えること | 答えないこと（他の記事に任せる） |
|---|---|---|---|---|
| kinmedai | Stay | kinmedai | 魚そのもの（何か・味・値段・旬・どこで食べるか） | 行き方の詳細、下田の町全体の案内（ROADMAP 6） |
| izu-from-tokyo | Stay（also live） | izu peninsula from tokyo | 東京からの行き方・運賃・日帰りか泊まるか・町の選び方 | 魚の詳細、空き家・移住 |
| **akiya-try-first** | Own（also live） | buying an akiya in japan（案） | **買う前に町で暮らして確かめる理由・方法・滞在の手段** | akiya の定義・統計の深掘り（ROADMAP 3）、外国人の購入の法律（ROADMAP 1）、本当の費用（ROADMAP 4）、何日いられるかの詳細（ROADMAP 9） |

この記事の内部リンク（本文2本以上）:
- 「Where can you stay for a month…」→ `[[l:izu-from-tokyo|…]]`（東京から2〜3時間で1か月試せる地域の例として）
- 自社の家の節 → `[[l:izu|Izu Peninsula]]`（いまある）
- 受ける側: izu-from-tokyo の「What changes when you rent a house in Izu?」の節から、長く住む・家を持つことを考える人向けに `[[l:akiya-try-first|…]]` を1本（izu-from-tokyo の見直しで入れる）。

---

## 7. 写真

- いま: `yaizu-engawa`（自社の写真・焼津の家のリフォーム前）。中身（古い家を買う前に）に合っている。差し替えない（PHOTO_PLAN.md の決まり）。説明文だけ B9 で確認。
- 本文の `node-shimoda`（リビング）は、自社の家の節にあるので1枚のまま。

---

## 外部ページの命令の有無

今回の検索結果（英語・日本語の上位ページ）に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。
