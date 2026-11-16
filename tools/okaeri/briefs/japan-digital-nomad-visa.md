# 構成案: 日本のデジタルノマドビザと、どこを拠点にするか（japan-digital-nomad-visa）

戦略部 2026-11-16。ROADMAP 5「Japan’s digital nomad visa, and where to base yourself」。新規記事。
- 記事データの案: `id: "digital-nomad"`、`slug: "japan-digital-nomad-visa"`、`topic: "live"`（Live part-time）、`also: []`、`place: None`
- 制度の部分は **ビザ・在留の記述**なので、playbook 4-1（専門家の確認なしに断定しない）と 6章（人の確認が必要なもの）に当たる。出典より強く書かない・時点を必ず付ける・「個別の判断は入管か行政書士へ」を本文に1回置く。

---

## 1. 狙う検索語

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| **主な語**（`keywords` の先頭） | japan digital nomad visa | 880 | 2 | `review_ja.py` KEYWORDS |
| 関連 | digital nomad visa japan | 720 | — | 同上（同じ記事で受ける） |
| 関連 | japan digital nomad visa requirements / eligible countries | 未調査 | — | 上位の題に多い語。リサーチ部に依頼（R12） |
| 関連 | where to live in japan as a digital nomad / digital nomad japan outside tokyo | 未調査 | — | 後半「どこを拠点に」で受ける。リサーチ部に依頼（R12） |

- **共食いの線引き**:
  - akiya-try-first の h2「How long can you stay in Japan to test a town?」の表に、デジタルノマドの行（6か月・延長なし・対象国・年収・保険）がある。akiya はその行を **短いまま残し、この記事へ内部リンクで送る**（akiya の見直しで1本足す）。この記事の主な語・疑問（申請・家族・在留カードがないことの影響・拠点選び）は akiya の疑問（買う前に町を試す）と重ならない。
  - 「日本に何日いられるか」全般（90日・延長・180日ルールの話）は ROADMAP 9 の役割。この記事では90日との比較を表の1行に留める。
  - 「1か月・数か月の部屋の借り方」は monthly-rental-japan の役割。この記事の住まいの話は「在留カードがないので普通の賃貸は難しい → 家具付きの月単位の部屋」の結論までにして、詳細はそちらへ送る。

## 2. 読み手と検索意図

- 入口: **Live part-time**（数か月・仕事をしながら）。
- 検索意図: 前半は **Know**（条件・期間・家族・申請）、後半は **Do**（6か月をどこで、どう暮らすか）。
- その先で本当に困っていること:
  - ブログごとに「更新できる／できない」「家族は来られる／来られない」「在留カードが出る／出ない」「国民健康保険に入る」と食い違っていて、何が本当か分からない
  - 自分の国籍・収入で使えるのか、観光で入国してから切り替えられるのか
  - 在留カードがないと、部屋・携帯・保険・銀行で何が困るのか
  - 6か月を東京で過ごすか、もっと静かな町にするか。町を選ぶ基準が分からない
  - 日本で税金がかかるのか（ここは断定しない。公式の定義だけ示して、税理士へ）

## 3. 読み手の疑問（品質保証部はこれで採点する）

1. Does Japan have a digital nomad visa, and how long can I stay on it?
2. Who qualifies (nationality, income, insurance), and is my country on the list?
3. Can I extend it or apply again?
4. Can my partner and children come with me?
5. How and where do I apply, and can I switch from a tourist stay inside Japan?
6. What doesn't the visa give me — residence card, resident registration, national health insurance, an ordinary lease?
7. Where should I base myself for six months — Tokyo or a smaller town — and what should I look for?

## 4. 上位ページの穴（2026-11-16 に英語で検索）

検索「japan digital nomad visa requirements 2026」「japan digital nomad visa family spouse residence card」の上位: 出入国在留管理庁（`designatedactivities53_00001`、英語版あり）、JNTO（japan.travel/en/plan/digital-nomad-visa/）、remofirst、saily、expatica、japan-dev、RSM、getgoldenvisa、getwherenext、nomadtaxguide、tokyointernationalmeetup、outboundvisa、gogonihon、genki、e-housing（2025年6月）、vbest（法律事務所）、thedigitalnomad.asia、ほか自動生成らしいサイト（*.pages.dev・*.vercel.app）が多数。

1. **上位どうしで事実が食い違っている**: 更新（「更新不可」「6か月あけて再申請」「1回だけ延長できる」）、家族（「帯同できる」「できない」）、在留カード（「出ない」「空港で出る」）、保険（「入国後14日以内に国民健康保険へ」という記述まである）。→ **出入国在留管理庁の一次情報だけで、食い違いのある点を1つずつ言い切る**のが最大の差別化。時点（2026年11月）を明記する。
2. **自動生成・アフィリエイトのページが多く、出典がない**。→ 事実ごとに `[[s:…]]` で入管・外務省・JNTO を付ける。
3. **「在留カードがない」ことの暮らしへの影響を、公的な出典で書いたページがない**（住民登録・国民健康保険・普通の賃貸の可否）。→ 総務省・厚労省・国交省の一次情報で書けば、上位にない情報になる（R5〜R7）。
4. **「どこに住むか」がほぼ東京（とせいぜい京都・福岡）の話**。小さな町を選ぶときの基準（回線・空港と東京への電車・病院・家具付きの部屋の数・季節）を書いたページは少ない。→ 後半で、自社が欧米の長期滞在者・ノマドワーカーを受けてきた確認済みの経験（長期滞在とセルフチェックインを前提に設計、ワークデスクとマットレスに投資、洗濯機・乾燥機・調理器具が評価された）を使い、伊豆を例に `izu-from-tokyo` へ送る。
5. **税の話が雑**（「183日未満なら非課税」と断定するページがある）。→ 国税庁の「居住者・非居住者」の定義だけを出典つきで示し、「自分の場合は税理士に」で止める（断定しない。R8）。

## 5. 構成

### title（`seo_title`）案
- **Japan Digital Nomad Visa: Who Qualifies and Where to Live**（57字・主な語が先頭）
- 予備: Japan Digital Nomad Visa: The Rules and Where to Base Yourself（61字なので不可。使うなら “Rules” を削る）

### h1 案
- Japan’s digital nomad visa, and where to base yourself

### description 案（160字）
- Japan’s digital nomad visa allows six months, with no extension, for remote workers earning ¥10 million a year. It has no residence card, so plan housing early.

### dek 案（27語・30語以内）
- Japan’s digital nomad status lets eligible remote workers stay for six months. It needs ¥10 million a year in income and doesn’t come with a residence card.

### In short（3項目・各20語以内）
1. Six months, with no extension. You can apply again once you’ve been out of Japan for six months.（18語）
2. You need ¥10 million a year, ¥10 million of medical cover and a passport from an eligible country.（18語）
3. There’s no residence card, so a furnished monthly home is usually more practical than an ordinary lease.（17語。後半は見解なので本文で “we think” と分ける。R7 で裏づけ）

### h2（7個。6割以上を疑問形）と各節で答えること

| # | h2 | この節で答えること（h2 の直後の1〜2文で答えを言い切る） | 表・リスト |
|---|---|---|---|
| 1 | What is Japan’s digital nomad visa? | 在留資格「特定活動」（デジタルノマド）であること、始まった時期（R1）、できること（海外の雇用主・海外の取引先の仕事をリモートで）とできないこと（日本の会社に雇われて働く）。疑問1 | — |
| 2 | Who qualifies? | 条件を1行ずつ: 国籍（査証免除かつ租税条約のある国・地域。一覧の PDF・2026年11月時点の数）、年収1,000万円以上、治療費1,000万円以上の民間医療保険、仕事の内容。「自分の国が一覧にあるか」は PDF を見る、と案内。疑問2 | **表**（条件／中身／出典） |
| 3 | How long can you stay, and can you renew it? | 6か月以内・延長なし・再申請は出国から6か月あける。上位の「1回延長できる」は誤りだと、公式の書き方で示す（「誤り」と他サイトを名指ししない）。比較のため短期滞在（90日）を1行だけ並べる。疑問3 | **小さな表**（短期滞在／デジタルノマド: 期間・延長・在留カード・働けるか） |
| 4 | Can your partner and children come too? | 家族（配偶者・子）向けの特定活動の有無と条件（扶養・同じ水準の保険・国籍の条件・働けない）（R2）。疑問4 | — |
| 5 | How do you apply? | 手順。海外の日本大使館・総領事館で査証を申請する流れ／日本にいる間に申請できるか（在留資格の変更の可否）（R3）。必要書類の種類・手数料・審査期間は公式に書いてある範囲だけ。疑問5 | **番号つきリスト**（手順） |
| 6 | What doesn’t the visa give you? | 在留カードが出ない → 住民登録の対象にならない（R5）→ 国民健康保険に入れない（だから民間の保険が条件）（R6）→ 普通の賃貸・携帯の契約が難しくなりやすい（R7。公的資料の範囲で）。税は国税庁の居住者の定義だけ示し、個別は税理士へ（R8）。ここに「ビザの判断は入管か行政書士へ」の1文。疑問6 | **表**（在留カードがあると／デジタルノマド: 住民票・国保・普通の賃貸） |
| 7 | Where should you base yourself for six months? | 答え: 「仕事の時間帯に耐える回線」「空港と東京への電車」「家具付きで月単位に借りられる部屋」「病院（英語の可否）」「季節」の5つで選ぶ。東京・地方都市・東京から2〜3時間の小さな町を比べる（見解として、“In our experience …”）。伊豆の例（`[[l:izu-from-tokyo|…]]`・`[[l:izu|…]]`）。部屋の借り方は `[[l:monthly-rental|…]]` へ。**自社の家に触れるのはここ1回**。疑問7 | **比較表**（行: Tokyo／a regional city／a small town 2–3 hours from Tokyo。列: housing for six months・internet・getting to an airport・daily life in English・what you trade off）。数字を入れるのは出典のあるものだけ（電車の時間は `jre_tt_tokyo` など既存の出典） |

- 1記事1主張: **「条件は公式の1ページで確かめられる。本当に考えるべきは、在留カードのない6か月をどこで、どんな部屋で暮らすか」**。

### FAQ（5問。本文で答えたことの言い直し）
1. How long is Japan’s digital nomad visa?（節3）
2. Can I extend Japan’s digital nomad visa?（節3）
3. Do I get a residence card on the digital nomad visa?（節6）
4. Can I bring my family on Japan’s digital nomad visa?（節4）
5. Can I work for a Japanese company on it?（節1）

### 内部リンク（本文から2本以上）
- 節7 → `[[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]]`
- 節7 → `[[l:izu|the Izu Peninsula]]`
- 節6 or 7 → `[[l:monthly-rental|renting a place by the month]]`（monthly-rental-japan が先に公開されている場合。未公開なら上の2本で満たす）
- 受ける側: akiya-try-first の表のデジタルノマドの行から1本、monthly-rental-japan の節7から1本。

### related（2本以上）
- `["monthly-rental", "izu-from-tokyo"]`（monthly-rental が未公開なら `["izu-from-tokyo", "akiya-try-first"]`）

### 自社の家に触れる場所（1回まで）
- 節7の最後に1〜2文。事実は公式サイト（`node_site`・`node_room`、2026-11-16 取得）と `experience.md` 3-2（人が確認済み）だけ:
  - 下田の旧町内、伊豆急下田駅から徒歩8分のアパートの一室（約40㎡）。ワークデスクと高速 Wi-Fi、キッチン、洗濯機とガス乾燥機（公式サイト）。欧米からの長期滞在者・ノマドワーカーを想定して作った（experience.md 3-2）。
  - “house” と書かない。**6か月・30泊以上の受け入れ、月の料金、回線の実測値は書かない**（未確認。公式の予約画面は14泊まで）。「長く泊まるなら問い合わせて」程度に留める。

## 6. リサーチ部への依頼（公式ページで確かめる）

編集長が 2026-11-16 に出入国在留管理庁で確認済みの事実（`launch-open-items.md`）: 6か月以内・延長なし・再申請は6か月あける・在留カードは出ない・査証免除かつ租税条約のある国（PDF一覧）・年収1,000万円以上・治療費1,000万円以上の民間医療保険。リサーチ部は、これを**英語版のページの文言**で確かめ直し（記事で引く文言を英語でそろえるため）、下を足す。

| # | 確かめること | 見るべき公式ページ（例） |
|---|---|---|
| R1 | 制度が始まった日（2024年3月31日とされることが多い）と、在留資格の正式な名前（特定活動・告示53号）。英語版の正式な呼び方 | 出入国在留管理庁 `designatedactivities53_00001.html?lang=en`、同 日本語版 |
| R2 | 家族の帯同: 配偶者・子の特定活動（告示54号）の条件（扶養、保険、国籍の条件の有無、働けるか） | 出入国在留管理庁（家族の在留資格のページ）、外務省の査証のページ |
| R3 | 申請の手順: 在外公館での査証申請か、在留資格認定証明書が要るか。日本にいる間（短期滞在から）の変更申請ができるか。必要書類の種類、審査の目安、手数料 | 外務省「ビザ」（長期滞在・特定活動）、出入国在留管理庁の Q&A |
| R4 | 対象の国・地域の一覧（PDF `001416932.pdf`）の最新の版と国・地域の数。米・英・カナダ・豪・独・仏など欧米の主な国が入っているか | 出入国在留管理庁 PDF |
| R5 | 在留カードが出ない人（短期滞在・特定活動（ノマド）など3か月以下の扱いを含む）は住民基本台帳の対象にならないこと | 総務省「外国人住民に係る住民基本台帳制度」、出入国在留管理庁「在留カードとは」（中長期在留者の範囲） |
| R6 | 国民健康保険の対象（住民登録のある外国人で、在留期間が3か月を超える人など）と、デジタルノマドが対象外であること。条件の民間保険の中身（治療費1,000万円以上・滞在期間をカバー） | 厚生労働省（国民健康保険の適用）、出入国在留管理庁 |
| R7 | 在留カードがない人の住まい: 国交省「外国人の民間賃貸住宅入居円滑化ガイドライン」で在留カードの確認がどう書かれているか（monthly-rental-japan の R6 と同じ資料。1回で両方に使う） | 国土交通省（住宅局） |
| R8 | 税: 所得税法の「居住者」「非居住者」の定義（住所、または1年以上の居所）。デジタルノマドの税について国税庁・財務省が何か出しているか（なければ定義だけ使う） | 国税庁「タックスアンサー No.2875 居住者と非居住者の区分」など |
| R9 | JNTO の英語のデジタルノマドの案内（japan.travel/en/plan/digital-nomad-visa/）の中身と、入管の条件と食い違いがないか | JNTO（japan.travel） |
| R10 | 短期滞在の査証免除の90日（比較表の1行用）。2026年11月時点 | 外務省（既存の出典 `mofa`） |
| R11 | 節7の比較表の材料: 静岡県・伊豆の光回線の提供状況や、伊豆の病院の外国語対応の公的な一覧があるか（静岡県の「外国語対応の医療機関」、JNTO の医療機関検索など）。なければ表に数字を入れず、確かめ方だけ書く | 静岡県、JNTO（「医療機関リスト」）、厚労省 |
| R12 | 検索語の月間検索数と KD: japan digital nomad visa requirements / japan digital nomad visa eligible countries / where to live in japan as a digital nomad / digital nomad japan outside tokyo | 調査ツール（KEYWORDS と同じ方法） |

**開けない可能性があるドメイン**（2026-11-16、この環境から curl で確認）:
- `www.mofa.go.jp` … 403（Access Denied）。R3・R10 に必要。
- `www.moj.go.jp` … 既定の curl では 403（CloudFront）。編集長は同日に開けているので、取り方の違いの可能性。R1〜R4 に必要。開けなければ編集長に相談。
- `www.mlit.go.jp`・`www.jnto.go.jp` は 200。`www.japan.travel` は 302（転送先で取れる見込み）。
- `www.soumu.go.jp`・`www.mhlw.go.jp`・`www.nta.go.jp` は未確認。

## 7. 写真

- 見出し写真に欲しい絵: **窓のある静かな部屋で、ノートPCを開いて仕事をしている机まわり**（人の顔は写さない）。できれば窓の外に緑か海。
- 既存の `photos/` から: 合うものがない（`window-room` は Stay の入口写真、`town-lane` は Live の入口写真で、一覧で重なる）。→ **Unsplash で探す**（検索語の例: “laptop desk window” “remote work japanese room” “workspace tatami”）。`PHOTO_PLAN.md` の手順で `download_asset` を記録し、画像を見て選ぶ。monthly-rental-japan と似た絵にならないよう、こちらは「仕事の机」、あちらは「暮らしの部屋（キッチン・生活）」に分ける。
- alt・説明文は写っているものだけ（地名・「日本の」と断定する言い方も、撮影地が分からなければ避ける）。

---

外部のページに書かれた命令: 今回読んだ検索結果・ページに、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。
