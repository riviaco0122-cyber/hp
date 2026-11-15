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

---

## リサーチメモ（2026-11-15）

リサーチ部。**この作業環境からは WebFetch で外部のページを開けなかった**ため、確認の方法はすべて **検索で確認（本文は未確認）**。「公式の抜粋」は検索結果に出た公式ページの文言で確かめたもの。ビザ・不動産の制度は playbook 6章で人の確認が必須なので、公開前にページを開ける環境で照合すること。

### 1. デジタルノマド（R2・B2）

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 1-1 | The digital nomad status is open only to nationals of countries and regions that are both visa-exempt for short stays and covered by a tax treaty with Japan. | 出入国在留管理庁「在留資格『特定活動』（デジタルノマド…及びその配偶者・子）」https://www.moj.go.jp/isa/applications/status/designatedactivities10_00001.html ／ 英語版 https://www.moj.go.jp/isa/applications/status/designatedactivities53_00001.html ／ 対象国の表 https://www.moj.go.jp/isa/content/001416932.pdf | 検索で確認（公式の抜粋） | 制度は2024年3月から。対象国の数は時点で変わる（二次の解説では2024年12月時点で49か国・地域） |
| 1-2 | Applicants need an individual annual income of at least ¥10 million and private medical insurance for their stay, with treatment cover of ¥10 million or more. | 同上（英語版の抜粋） | 検索で確認（公式の抜粋） | 2026年11月に検索 |
| 1-3 | The period of stay is six months and cannot be renewed. | 同上 | 検索で確認（公式の抜粋） | 同上 |
| 1-4 | Once six months have passed after leaving Japan, you can come back under the same status again. | 同上（英語版の抜粋 “Once six months have passed after leaving Japan, you can re-enter Japan with the status of residence again.”） | 検索で確認（公式の抜粋） | 同上 |
| 1-5 | Working for a Japanese employer is not allowed; spouses and children can come under a separate digital nomad family status. | 同上・外務省 https://www.mofa.go.jp/ca/fna/pagewe_000001_00046.html | 検索で確認 | 同上 |

**まとめ**: B2 のとおり、対象国の条件（ビザ免除かつ租税条約）を必ず書く。「It cannot be renewed」は公式どおりで正しいが、「出国から6か月たてば再び申請できる」を足すと正確。国の数は書かない（変わる）。

### 2. 短期滞在の90日（R1・B1。参考）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 2-1 | 査証免除の短期滞在（多くは90日まで）。対象の国・地域の数は報道で71〜74とばらつく | 外務省「査証免除措置」https://www.mofa.go.jp/j_info/visit/visa/short/novisa.html（いまの `mofa`） | **一次は未確認**（報道・二次のみ） | — |
| 2-2 | 電子渡航認証（JESTA）は2028年度の導入予定と報道 | 報道（二次） | 検索で確認（一次は未確認） | 2025〜2026年の報道 |

→ 90日は `mofa` を出典に「Most visa-exempt visitors can stay up to 90 days (MOFA, as of November 2026)」と書き、国によって日数が違うことを一言足す。`[[ed:外務省の査証免除のページで、90日と例外の国を開いて確認]]`。JESTA は記事の主題から外れるので書かなくてよい。

### 3. 外国人の不動産購入の2026年の制度の動き（R6・法務のゲート）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 3-1 | Since 1 April 2026, non-residents who acquire property in Japan must file a report under the Foreign Exchange Act within 20 days, including homes bought to live in. | 財務省「外国為替の取引等の報告に関する省令の一部を改正します（令和8年2月20日）」https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/recent_revised/gaitamehou_20260220.html ／ 財務省 リーフレット（2026年6月）https://www.mof.go.jp/policy/international_policy/gaitame_kawase/real_property/real_property_leafletJ.pdf ・FAQ https://www.mof.go.jp/policy/international_policy/gaitame_kawase/real_property/FAQ_J.pdf | 検索で確認（公式の抜粋「令和８年４月１日から施行」） | 2026年2月20日公布、4月1日施行 |
| 3-2 | The report is based on residence, not nationality, so Japanese citizens living abroad are covered too; it is a reporting duty, not a ban. | 同上（FAQ）。「禁止・制限ではない」は解説（二次）の言い方 | 検索で確認 | 同上 |
| 3-3 | Since 5 October 2026, everyone registering a purchase of property (including Japanese citizens) must give their nationality to the Legal Affairs Bureau; it is kept as internal data and does not appear on the public register. | 法務省 民事局長通達（令和8年9月4日 法務省民二第872号）https://www.moj.go.jp/content/001470076.pdf ／ 法務局「不動産登記の申請書様式について」https://houmukyoku.moj.go.jp/homu/minji79.html | 検索で確認（公式の抜粋） | 2026年10月5日から（不動産登記規則の改正、令和8年法務省令第23号） |
| 3-4 | A government expert panel recommended in October 2026 that buying land near key defence facilities and on border islands should need government permission, regardless of the buyer's nationality. | 内閣官房「外国人による土地取得等のルールの在り方検討会 提言」（令和8年10月）https://www.cas.go.jp/jp/seisaku/symbiotic_society/gaikokujin_tochishutoku/kaisai-jokyo/dai5/teigen.pdf | 検索で確認（抜粋と報道） | 2026年10月2日に提出（報道） |
| 3-5 | A bill to amend the Act on important land (重要土地等調査法) was submitted to the Diet on 23 October 2026; as of mid-November 2026 it had not been passed. | 内閣府「第222回臨時国会 提出法案」https://www.cao.go.jp/houan/222/index.html | 検索で確認（提出日は抜粋。**成立していないことは衆院の質疑の報道からの推定**） | 2026年11月15日時点（審議中とみられる） |
| 3-6 | 一般の住宅・土地の購入に、国籍・在留資格による禁止や許可制がある | **見つからなかった**（上の 3-1〜3-5 はどれも報告・届出、または安全保障上の重要な区域に限った話）。報道では「マンション取得の規制は当面見送り」 | 検索で確認 | 2026年11月 |

**記事で「購入に国籍・在留の制限はない」と書いてよいか**: そのままの断定はやめる（2026年に報告・届出が増え、重要な区域の許可制の法案が国会にあるため、「制限はない」だけでは読み手に誤解を与える）。正確な言い方の案:

> As of November 2026, Japan does not ban foreigners or non-residents from buying a home, and you don't need a visa to buy. But there is more paperwork than before: since April 2026 non-residents must report a purchase under the Foreign Exchange Act, and since October 2026 every buyer gives their nationality when the purchase is registered. A bill now before the Diet would require permission to buy land near key defence sites and on border islands, whatever your nationality.

出典は 3-1（財務省）・3-3（法務省）・3-5（内閣府）。法務のゲートなので、この段落は人の確認に必ず回す（`[[ed:2026年11月時点の法案の審議状況と、言い方を人が確認]]`）。詳しくは ROADMAP 1 の記事に任せ、この記事は2〜3文にとどめる（A3）。

### 4. 自治体のお試し住宅（R4・B4）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 4-1 | Trial homes are run by each municipality, and the rules differ: typical conditions are living outside the area, seriously considering moving there, and having a consultation with the town first. | 南アルプス市 https://www.city.minami-alps.yamanashi.jp/docs/12876.html ・京丹後市 https://www.city.kyotango.lg.jp/top/soshiki/mayoroffice/seisakukikaku/4/iewo_sagasu/14414.html ・中種子町の要綱 https://town.nakatane.kagoshima.jp/tiiki/otameshizyuutaku/documents/otameshizyuutaku_youkou.pdf | 検索で確認（公式の抜粋） | 2026年11月に検索 |
| 4-2 | Lengths and prices vary widely, from a day to two months, and from free to a small daily fee. | 静岡市（中心部: 日帰り〜7日、1人1日1,500円、料理・洗濯不可。オクシズ: 3泊4日〜2週間、宿泊無料＋体験料1組1日300円）https://www.city.shizuoka.lg.jp/ijuteiju/s000050.html ・ https://www.city.shizuoka.lg.jp/s8937/okushizuoka/s000018.html ／ 京丹後市（1〜2か月）／大館市（無料）https://www.city.odate.lg.jp/kurashi/subsidy/p12452 | 検索で確認（公式の抜粋） | オクシズのページは2025年3月更新。ほかは更新日不明 |
| 4-3 | 探し方: 都道府県の移住ポータル（静岡県 https://iju.pref.shizuoka.jp/ ）と、移住・交流推進機構（JOIN）の「お試し移住」の一覧、各市町の移住担当課 | JOIN（2023年6月時点で1,471市区町村が会員）／静岡県 | 検索で確認 | — |
| 4-4 | 外国籍の人・観光の在留資格の人が使えるか | **確認できず。** 国籍・在留資格を書いた要綱は見つからなかった。多くは「○○外に住民登録がある人」が条件で、海外に住む人（日本に住民登録が無い人）が当てはまるかは自治体ごとに不明 | — | — |
| 4-5 | 伊豆の市町（下田市・南伊豆町など）のお試し住宅 | **確認できず。** 下田市は2024年に1泊2日の「お試し移住体験ツアー」（宿泊費の補助 1人1泊4,000円まで）https://city.shimoda.shizuoka.jp/file/農ある暮らし体験_お試し移住体験ツアー.pdf 。いまも実施しているかは未確認 | 検索で確認 | 2024年 |
| 4-6 | 移住希望者に空き家を短期で貸す場合、一定の条件で旅館業法の対象外とする扱い（2016年の通知）があり、お試し居住に使いやすくなった | 総務省の資料 https://www.soumu.go.jp/main_content/001009830.pdf | 検索で確認 | 2016年の通知 |

**まとめ**: 「Many towns run trial homes for people thinking of moving there; stays range from a day to a couple of months and conditions vary」は自治体の例を出典にして書ける。**外国籍の人が使えると書かない**。「Most are aimed at people planning to move to the town, so ask the town's relocation office whether you qualify」とし、`[[ed:伊豆の市町（下田市・南伊豆町・伊豆市）にお試し住宅があるか、外国籍・海外在住の人が使えるかを問い合わせ]]`。

### 5. 空き家の数（R3・B8）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 5-1 | Japan had 9.002 million vacant dwellings in 2023, a record 13.8% of all housing. | 総務省統計局「令和5年住宅・土地統計調査 住宅及び世帯に関する基本集計（確報集計）結果」https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf ／ 英語: Statistics Bureau News Bulletin https://www.stat.go.jp/english/info/news/20241030.html | 検索で確認（公式の抜粋） | 調査時点 2023年10月1日、確報の公表 2024年9月25日 |
| 5-2 | Of these, 3.856 million — 5.9% of all housing — were not for rent, for sale or second homes, up 369,000 from 2018. | 同上（確報）。速報（2024年4月30日）では 385万戸・5.9%・37万戸増 https://www.stat.go.jp/data/jyutaku/2023/pdf/g_kekka.pdf | 検索で確認（公式の抜粋） | 同上 |
| 5-3 | 900万戸は速報と確報で同じ（確報は 900万2千戸） | 統計局 メールニュース https://www.stat.go.jp/info/mail/pdf/20240925_no1693.pdf | 検索で確認 | 2024年9月25日 |

→ `datamax` と「MLIT, citing…」を、統計局の確報（`stat_housing2023`）1つに置き換えられる。

### 6. 新しい出典（`SOURCES_NEW` の候補）

```python
"isa_nomad_en": ("https://www.moj.go.jp/isa/applications/status/designatedactivities53_00001.html", "Immigration Services Agency", "出入国在留管理庁", "Immigration Services Agency: Designated Activities (Digital Nomad)"),
"isa_nomad_list": ("https://www.moj.go.jp/isa/content/001416932.pdf", "Immigration Services Agency", "出入国在留管理庁", "Immigration Services Agency: Eligible countries and regions for the digital nomad status"),
"mof_fefta2026": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/recent_revised/gaitamehou_20260220.html", "Ministry of Finance", "財務省", "Ministry of Finance: Revision of reporting rules under the Foreign Exchange Act (20 February 2026)"),
"mof_realprop_faq": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/real_property/FAQ_J.pdf", "Ministry of Finance", "財務省", "Ministry of Finance: FAQ on reports of real property acquisition (June 2026)"),
"moj_nationality": ("https://www.moj.go.jp/content/001470076.pdf", "Ministry of Justice", "法務省", "Ministry of Justice: Notice on recording nationality in property registration (4 September 2026)"),
"cao_land_bill": ("https://www.cao.go.jp/houan/222/index.html", "Cabinet Office", "内閣府", "Cabinet Office: Bills submitted to the 222nd Diet session"),
"cas_land_teigen": ("https://www.cas.go.jp/jp/seisaku/symbiotic_society/gaikokujin_tochishutoku/kaisai-jokyo/dai5/teigen.pdf", "Cabinet Secretariat", "内閣官房", "Cabinet Secretariat: Expert panel recommendations on land acquisition rules (October 2026)"),
"stat_housing2023": ("https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf", "Statistics Bureau of Japan", "総務省統計局", "Statistics Bureau of Japan: 2023 Housing and Land Survey, final basic tabulation (2024)"),
"shizuoka_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000050.html", "Shizuoka City", "静岡市", "Shizuoka City: Trial homes for people considering a move"),
"okushizuoka_trial": ("https://www.city.shizuoka.lg.jp/s8937/okushizuoka/s000018.html", "Shizuoka City", "静岡市", "Shizuoka City: Okushizuoka trial homes"),
```
（いまの `isa` は日本語ページ。英語の記事なので `isa_nomad_en` に替えるとよい）

### 7. 海外の読み手の生の疑問（旅行・移住フォーラム、Q&A を検索。要約のみ）

- 空き家を買えばビザが出るのか、家があれば日本に長く住めるのか。
- 1年のうち数か月しか住まない予定でも買ってよいか。空けている間の管理はどうするのか。
- 買う前に借りて住んでみたいが、1か月だけ貸してくれる古い家や部屋はどこで探せるのか。
- 自治体によっては「何年か住むこと」を条件にしているが、ビザの期間と合わない場合はどうなるのか。
- 町の人口が減り続けたら、将来売れなくなるのではないか。

（Reddit の個別スレッドは検索結果に出ず、移住・不動産の Q&A フォーラムとガイドの読者の質問から要約。投稿者名・URL・原文は書かない）

### 8. 調べられなかったこと

- お試し住宅を外国籍・海外在住の人が使えるか、伊豆の市町のお試し住宅の有無。
- 重要土地等調査法の改正案が成立したか（審議中とみられるが一次で未確認）。
- 外務省の査証免除のページの本文（90日と例外の国）。
- R5（新耐震基準の英語の公的な出典）、R9（検索語の月間検索数・KD）は今回は未実施。

### 9. 外部ページの命令の有無

今回の検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。

---

## リサーチメモ 2（2026-11-15）

リサーチ部。公開前の出典の差し替え（`tools/okaeri/log.md` の「品質保証部の採点（akiya-try-first・組み込み後のページ）」）のための追加調査。今回は自治体のページ（city.kyotango.lg.jp・city.shizuoka.lg.jp・city.minami-alps.yamanashi.jp）は WebFetch で開けた。jreast.co.jp・chisou.go.jp はこの環境から名前解決できず、検索で確認にとどまる。

### 1. 京丹後市のお試し住宅（出典 `kyotango_trial`）

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| K-1 | The old URL in `kyotango_trial` (…/iewo_sagasu/14414.html) returns 404. | 京丹後市（旧URL） | ページを開いて確認（HTTP 404） | 2026-11-15 |
| K-2 | Kyotango City closed its city-run trial homes at the end of September 2026. | 京丹後市 移住支援サイト「お試し住宅」https://www.city.kyotango.lg.jp/ijushien/ie/16904.html （【重要】市営お試し住宅閉鎖のお知らせ） | ページを開いて確認 | ページの更新日 2026-10-01 |
| K-3 | The city now refers people to trial homes and share houses run by local groups and private owners, through its relocation desk (Tango Kurashi Tankyusha). | 同上 | ページを開いて確認 | 同上 |
| K-4 | 「同一年度に1か月以上2か月以内、月4.5万円」 | **公式では確認できず。** 検索では第三者の生活情報サイトにだけ出てくる。一方、市の2020年11月の報道資料（検索の抜粋）では「3日〜30日/年、3日分4,500円、4日目以降1日1,500円」で、条件が食い違う。どちらにせよ市営の住宅は閉鎖済み | 検索で確認（本文は未確認。報道資料 PDF は 404） | — |

**結論**: 京丹後市は、**今はこの記事の例として使えない**。`kyotango_trial` を記事から外す（`[[s:minamialps_trial,kyotango_trial]]` → `[[s:minamialps_trial,shizuoka_long_trial]]` など）。「1日から2か月ほどまで」の「2か月」の根拠もなくなるので、下の 2 の例（南アルプス市 1〜3か月、静岡市の長期 半年〜2年）に合わせて言い方を直す。

### 2. 「1か月以上」泊まれるお試し住宅の公式の例

| # | 事実（英語で1文） | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| T-1 | Minami-Alps City (Yamanashi) rents its Ashiyasu trial home for one to three months at ¥21,000 a month (¥700 a day), paid in advance, plus ¥1,000 a month for the neighbourhood rubbish fee. | 南アルプス市「お試し住宅（芦安）」https://www.city.minami-alps.yamanashi.jp/docs/12876.html （既存の `minamialps_trial`） | ページを開いて確認 | 掲載日 2026-02-02 |
| T-2 | It is for people registered as living outside Yamanashi Prefecture who intend to move to the city and have registered for a relocation consultation; bookings cannot span two fiscal years. | 同上 | ページを開いて確認 | 同上 |
| T-3 | 南アルプス市のページに国籍・在留資格の条件は**書かれていない**。海外に住む人（日本に住民登録が無い人）が「県外に住民登録がある方」に当たるかは**確認できず** | 同上 | ページを開いて確認 | 同上 |
| T-4 | Shizuoka City offers "long-term trial homes" in city-run apartments for six months to under two years, at roughly ¥42,000–¥83,000 a month depending on the estate, with utilities extra and rent paid three months in advance. | 静岡市「長期お試し住宅（移住者向け住まい提供事業）」https://www.city.shizuoka.lg.jp/ijuteiju/s000158.html | ページを開いて確認 | ページの更新日 2026-08-20 |
| T-5 | It is for people living outside Shizuoka Prefecture who have decided, or are preparing, to move to the city and will stay on afterwards; foreign nationals qualify only with permanent resident, spouse of a Japanese national, long-term resident or special permanent resident status. | 同上 | ページを開いて確認 | 同上 |
| T-6 | 伊豆の市町（下田市・南伊豆町・伊豆市・河津町・東伊豆町・松崎町・西伊豆町）で、1か月以上泊まれるお試し住宅の公式ページ | **確認できず。** 伊豆市は「お試し住宅（土肥・中伊豆）」があることだけ報道（2026年5月の移住ツアーの告知）で確認、期間・料金は不明。南伊豆町は県の移住サイトの PDF と内閣府の資料（2023〜2024年度）に「お試し移住」の住宅がある旨が出るが、PDF は開けず（503・名前解決できず）、期間・料金は未確認。ほかの町は見つからなかった | 検索で確認（本文は未確認） | 2023〜2026年 |

**記事への使い方の案**:
- 静岡市の長期お試し住宅（T-5）は、**外国籍の人の扱いを公式に書いた例**として価値が高い。観光（短期滞在）やデジタルノマドの在留資格では使えないことが読み取れる。言い方の案: “Some towns spell out who qualifies. Shizuoka City’s long-term trial flats, for example, are open to foreign nationals only if they hold permanent or long-term residence or are married to a Japanese citizen [[s:shizuoka_long_trial]], so a tourist or digital nomad stay won’t qualify there.”
- 期間の幅は “from a day or two up to a few months, and in a few cities up to two years” などに直す（静岡市 中心部 日帰り〜7日、南アルプス市 1〜3か月、静岡市 長期 半年〜2年）。
- 伊豆の市町の例は書かない。`[[ed:伊豆市（土肥・中伊豆）・南伊豆町のお試し住宅の期間・料金と、外国籍・海外在住の人が使えるかを問い合わせ]]` を残すかは執筆部の判断。

### 3. 東京〜伊豆急下田の所要時間（JR東日本）

| # | 事実（英語で1文） | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| J-1 | JR East says the Odoriko takes 2 hours and 49 minutes from Tokyo Station to Izukyu-Shimoda Station. | JR東日本 “Odoriko (E257 series)” https://www.jreast.co.jp/en/multi/traininformation/odoriko/index.html （日本語の入口 https://www.jreast.co.jp/multi/traininformation/odoriko/ ） | **検索で確認（本文は未確認）**。この環境から jreast.co.jp を開けない。仏・独・西・インドネシア語版の検索の抜粋も同じ 2時間49分 | 更新日は不明（2026-11 に検索） |
| J-2 | 列車によって時間は違う。駅探（`ekitan`）は約2時間35分、JR東日本の時刻表（timetables.jreast.co.jp）の列車ごとの停車駅の表でも2時間36分ほどの列車がある | `ekitan`、JR東日本 時刻表 | 検索で確認 | 2026年の時刻表 |

**キー**: `content.py` の `SOURCES` に **JR東日本の出典キーは無い**（東京〜下田の時間は `ekitan`、伊豆全体は `jg6305`）。新しいキー `jreast_odoriko` を足す。
**注意**: 「within three hours」は 2時間49分（JR東日本）でも 2時間35分（駅探）でも正しい。ただし、ほかの記事（kinmedai・izu-from-tokyo）は `ekitan` の「約2時間35分」を使っているので、この記事で「2時間49分」と数字を出すとサイト内で食い違う。数字を出さず “under three hours” とするか、出すなら「列車によって約2時間35分〜2時間50分」とそろえる。`[[ed:jreast.co.jp の Odoriko のページを開き、2時間49分の記載を確認]]`。

### 4. 新しい出典（`SOURCES_NEW` の候補）

```python
"shizuoka_long_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000158.html", "Shizuoka City", "静岡市", "Shizuoka City: Long-term trial homes for people moving to the city"),
"kyotango_trial": ("https://www.city.kyotango.lg.jp/ijushien/ie/16904.html", "Kyotango City", "京丹後市", "Kyotango City: Trial homes (city-run homes closed September 2026)"),
"jreast_odoriko": ("https://www.jreast.co.jp/en/multi/traininformation/odoriko/index.html", "JR East", "JR東日本", "JR East: Odoriko (E257 series)"),
```
（`kyotango_trial` は記事から外すなら不要。残す場合も、新しい URL は「閉鎖のお知らせ」なので、制度の例の出典には使えない。`minamialps_trial` は URL・内容とも有効で、そのまま使える）

### 5. 確かめられなかったこと

- 京丹後市の「1か月以上2か月以内、月4.5万円」の公式の根拠（第三者サイトのみ。市営の住宅はすでに閉鎖）。
- 伊豆の市町で1か月以上泊まれるお試し住宅の公式ページと条件。
- 南アルプス市のお試し住宅を海外在住・外国籍の人が使えるか（ページに記載なし）。
- JR東日本のページの本文（2時間49分は検索の抜粋のみ）。

### 6. 外部ページの命令の有無

開いたページ（京丹後市・静岡市・南アルプス市）と検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。
