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

---

## リサーチメモ（2026-11-16 リサーチ部）

取得はすべて 2026-11-16（日本時間）。「開いて確認」= curl でページ本文を読んだ。「検索で確認」= 入管・外務省・在外公館のページがこの環境から開けず（403 またはプロキシで遮断）、検索結果の要約・抜粋で中身を確かめた（ページ本文は未読）。**入管（www.moj.go.jp/isa・www.isa.go.jp）の英語版の文言は開けず確かめられなかった**ので、英語の言い回しは JNTO（開いて確認）と e-Gov の条文（日本語。英訳は執筆部）にそろえる。

### A. 制度（R1〜R4・R9・R10）

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | 時点 |
|---|---|---|---|---|
| R1 | The status is “Designated Activities (Digital Nomad)”, and its family version is “Designated Activities (Spouse or Child of Digital Nomad)”. | JNTO「Digital Nomad Visa」 https://www.japan.travel/en/plan/digital-nomad-visa/ （既存 `isa_nomad_en` も同じ名前） | 開いて確認（JNTO）。入管の告示番号（53号・54号）は検索で確認 | 2026-11-16 |
| R1 | The scheme started on 31 March 2024. | 外務省の査証ページ（令和6年3月31日の掲載）・Baker McKenzie（“effective 31 March 2024”） | 検索で確認（外務省は開けず） | 2024-03-31 開始 |
| R1 | It covers remote work for an employer set up under foreign law, or paid services and sales to people outside Japan, done online from Japan — so freelancers with overseas clients fit the wording too. | 出入国管理及び難民認定法施行規則 第19条の5 第3号（e-Gov） https://laws.e-gov.go.jp/law/356M50000010054 | 開いて確認（e-Gov API の条文） | 2026-10-01 施行の版 |
| R1 | You can’t take a job with a Japanese employer on it, and permission for other work is not granted in principle. | 出入国在留管理庁（`isa_nomad_en`）・入管の配偶者/子の説明 | 検索で確認（入管の文言「本邦の公私の機関との雇用契約等に基づく就労活動は不可」「資格外活動許可は原則認められない」） | 2026-11 |
| 共通 | The stay is six months, with no extension. | JNTO（“Six months (No extension will be granted)”）・`isa_nomad_en`（「在留期間 6月（更新不可）」） | JNTO は開いて確認、入管は検索で確認＋編集長の確認（launch-open-items） | 2026-11-16 |
| 共通 | You can come back on the same status once six months have passed since you left Japan. | `isa_nomad_en`（「出国後6か月以降は再度本在留資格で本邦滞在が可能」）・Japan Times 2024-02-02 | 検索で確認＋編集長の確認 | 2026-11 |
| 共通 | The applicant’s own annual income must be ¥10 million or more at the time of application. | `isa_nomad_en`（「申請時点で申請人個人の年収が1,000万円以上」）・JNTO（“a minimum of 10 million yen for the applicant’s income”） | JNTO 開いて確認・入管は検索で確認 | 2026-11 |
| 共通 | You need travel or medical insurance covering death, injury and illness for the whole stay, with at least ¥10 million of cover for medical treatment. | `isa_nomad_en` | 検索で確認＋編集長の確認 | 2026-11 |
| R4 | Eligibility is limited to nationals of countries and regions on the immigration agency’s list, which is built from places that have both a visa exemption and a tax treaty with Japan. | `isa_nomad_list`（PDF）・Japan Times 2024-02-02 | PDF は開けず。条件の考え方は検索で確認＋編集長の確認 | 2026-11 |
| R4 | At launch, the list was reported as 49 countries and regions, including the United States, the United Kingdom and Canada. | Japan Times「Japan’s digital nomad visas to require ¥10 million in income」2024-02-02 https://www.japantimes.co.jp/news/2024/02/02/japan/society/digital-nomad-visa-march/ | 検索で確認（ページは開けず） | 2024-02 時点の報道 |
| R2 | A spouse or child supported by the nomad can come on a separate family status for the same short stay; they can’t work in principle, also need insurance, also get no residence card, and must be nationals of a listed country. | `isa_nomad_en`（告示54号）・施行規則 第19条の5 第4号（e-Gov）・JNTO（“Spouse or child accompanying …”） | 在留カードなしは e-Gov で開いて確認。帯同できることは JNTO で開いて確認。働けない・保険・国籍は検索で確認 | 2026-11 |
| R3 | You apply for the visa at a Japanese embassy or consulate, and the document list is on the Ministry of Foreign Affairs page. | JNTO（MOFA の pagewe_000001_00046 へ誘導） | 開いて確認（JNTO）。MOFA 本体は開けず | 2026-11-16 |
| R3 | Changing from a short-term (tourist) stay to another status inside Japan is only allowed for “unavoidable special circumstances”. | 出入国管理及び難民認定法 第20条第3項ただし書（e-Gov） https://laws.e-gov.go.jp/law/326CO0000000319 | 開いて確認（条文） | 2026-10-01 施行の版 |
| R5 | People given three months or less, short-term visitors, and people named in a ministry ordinance — which includes digital nomads and their families — are not “mid- to long-term residents” and don’t get a residence card. | 入管法 第19条の3・施行規則 第19条の5 第3号・第4号（e-Gov） | 開いて確認（条文） | 2026-10-01 施行の版 |
| R5 | Foreign nationals go on the resident register (juminhyo) as “mid- to long-term residents”, i.e. people who are issued a residence card. | 総務省「外国人住民に係る住民基本台帳制度」（英語版） https://www.soumu.go.jp/main_sosiki/jichi_gyousei/c-gyousei/zairyu/english/index.html ・住民基本台帳法 第30条の45（e-Gov） | 開いて確認 | 2026-11-16 |
| R6 | Foreign nationals who are not registered foreign residents are excluded from National Health Insurance (the rule has narrow exceptions for people already enrolled). | 国民健康保険法 第6条第11号・国民健康保険法施行規則 第1条第1号（e-Gov） https://laws.e-gov.go.jp/law/333M50000100053 | 開いて確認（条文） | 2026-10-01 施行の版 |
| R7 | The government’s guideline for landlords lists a passport and a residence card as examples of ID for tenant screening, and leaves what to ask for to the landlord and tenant. | 国土交通省「外国人の民間賃貸住宅入居円滑化ガイドライン」第2章 Q5 https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000017.html （PDF /common/001265432.pdf） | 開いて確認 | 第2章 PDF は 2018年の版（ページは 2026-11-16 確認） |
| R7 | The same guideline says landlords should ask whether you have a Japanese bank account and a phone that works in Japan, and talk about alternatives if you don’t. | 同上 第2章 | 開いて確認 | 同上 |
| R8 | For income tax, you’re a resident if you have a domicile in Japan or have lived here continuously for a year or more; everyone else is a non-resident. | 国税庁 タックスアンサー No.2875 https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2875.htm ・英語 No.12006 https://www.nta.go.jp/english/taxes/individual/12006.htm | 開いて確認 | 令和8年4月1日現在の法令 |
| R8 | Non-residents are taxed only on Japan-source income, and pay for work done in Japan counts as Japan-source income (tax treaties can change this). | 国税庁 No.12006（2(12)）・No.2875（租税条約） | 開いて確認 | 同上 |
| R8 | 国税庁・財務省のデジタルノマド専用の案内 | 見つからなかった | 検索で確認 | 2026-11-16 |
| R9 | JNTO’s English page matches the immigration rules on six months, no extension, ¥10 million income and family members; it doesn’t give the insurance amount and sends readers to the immigration list and MOFA documents. | JNTO（R1と同じ） | 開いて確認 | 2026-11-16（JNTO は「掲載時点の情報」と注記） |
| R10 | Visitors from visa-exempt countries can usually stay up to 90 days for tourism (some nationalities get 15, 30 or 180 days) and can’t do paid work. | JNTO「Entry Into Japan and Visa Information」 https://www.japan.travel/en/plan/visa-info/visa-immigration/ （既存 `mofa` は開けず） | 開いて確認（JNTO） | 2026-11-16 |

### B. 拠点選び（R11）

| # | 事実（英語で1文） | 出典 | 確認の方法 | 時点 |
|---|---|---|---|---|
| R11 | Fibre broadband covered an estimated 97.13% of households in Japan, 96.7% in Shizuoka Prefecture, 96.3% in Tokyo and about 93.8% in Shimoda. | 総務省「令和6年度末FTTH世帯カバー率（都道府県別・市区町村別）」 https://www.soumu.go.jp/main_content/001088979.xlsx ・報道資料 https://www.soumu.go.jp/menu_news/s-news/01kiban07_02000124.html | 開いて確認（Excel の値） | 2025年3月末（推計。公表は 2026-08-28） |
| R11 | 伊豆の他の市町（同じ表）: 伊東 95.6%・伊豆 95.3%・伊豆の国 90.6%・東伊豆 95.0%・河津 92.5%・南伊豆 93.4%・松崎 91.9%・西伊豆 93.8%・熱海 93.4% | 同上 | 開いて確認 | 同上 |
| R11 | JNTO has an English search for medical institutions by prefecture, language and department, and says to check each one before you go. | JNTO「Guide for when you are feeling ill」 https://www.jnto.go.jp/emergency/eng/mi_guide.html | 開いて確認 | 2026-11-16 |
| 自社 | NODE Shimoda is a private apartment of about 40 m², 8 minutes’ walk from Izukyu-Shimoda Station, with a work desk, high-speed Wi-Fi, a kitchen, a washing machine and a gas dryer; there is a shower booth, no bathtub. | `node_site`・`node_room` | 開いて確認 | 2026-11-16 |
| 自社 | （体験）長期滞在とセルフチェックインを前提に設計／家具は睡眠（マットレス）と仕事（ワークデスク）に投資／洗濯機・乾燥機と調理器具がレビューで評価された／**開業時、Wi-Fi の工事は申し込みから2か月以上かかり、据え置き型のホームルーターでしのいだ** | `docs/brand/experience.md` 3-2（人が確認済み） | 照合済み | 開業時 |

- 回線の数字の注意: 「世帯カバー率」は、光回線を**引ける**世帯の割合の推計（実際の速さではない）。書くなら “an estimated … of households can get fibre” とし、2025年3月末と書く。宿の回線の実測値は書かない。
- 最後の Wi-Fi 工事の話は「町を選ぶとき、回線がもう入っている部屋を選ぶ」理由として節7で使える（体験として “When we opened …”）。

### C. 書かないと決めたこと（確かめられなかった）

1. **対象国・地域の今の数**と一覧の版（PDF が開けない。49・50・51 と食い違い）→ 数は書かず「一覧の PDF で確かめて」と案内。2024年2月の報道の「49」は、使うなら “was reported as 49 at launch” と時点つきでのみ。
2. **短期滞在のまま日本でノマドに切り替えられるか**（ノマド専用の可否は確かめられず）→ 入管法 第20条第3項の一般のルールだけ示し、「出発前に申請するつもりで」と書く。
3. **在留資格認定証明書（COE）が要るか・2つの申請の道**（米国の在外公館のページ題に “without a Certificate of Eligibility” があるが、ページは開けず）→ 書かない。
4. **審査の期間・手数料**（在外公館の資料で「COE ありは5営業日・なしは未定」との検索結果、手数料が2026年に変わったとの記述もあるが未確認）→ 書かない。
5. **必要書類の細目**（外務省のページは開けず）→ 種類を並べず、外務省のページへ。
6. **家族の保険を本人の保険でまとめられるか**（食い違い）→ 書かない。「家族も保険が要る」までにする。
7. **発給の件数**（2024年 257件・2025年 646件という外務省の査証統計の二次集計と Japan Times の記事が検索に出たが、一次の外務省統計を開けず）→ 書かない。
8. **携帯・銀行口座が在留カードなしで作れるか**の公的な出典 → 見つからない。国交省のガイドラインで「大家が聞くもの」として出ている範囲までにする。
9. **外国語対応の病院の、伊豆の具体的な名前・数**（静岡県の一覧は今回未調査）→ JNTO の検索で確かめられる、までにする。
10. **R12 の検索数・KD** → この部署から調査ツールが使えなかった。戦略部が同じ方法で取り直す。

### D. 新しく使う出典（`SOURCES_NEW` 用）

```python
"jnto_nomad": ("https://www.japan.travel/en/plan/digital-nomad-visa/", "JNTO", "日本政府観光局（デジタルノマドビザ）", "JNTO: Digital Nomad Visa (checked November 2026)"),
"jnto_visa": ("https://www.japan.travel/en/plan/visa-info/visa-immigration/", "JNTO", "日本政府観光局（入国とビザ）", "JNTO: Entry into Japan and visa information (checked November 2026)"),
"egov_immig_act": ("https://laws.e-gov.go.jp/law/326CO0000000319", "Immigration Control Act", "出入国管理及び難民認定法（e-Gov法令検索）", "Immigration Control and Refugee Recognition Act, Articles 19-3 and 20 (e-Gov, version in force 1 October 2026)"),
"egov_immig_rules": ("https://laws.e-gov.go.jp/law/356M50000010054", "Immigration Control Act ordinance", "出入国管理及び難民認定法施行規則（e-Gov法令検索）", "Ordinance for Enforcement of the Immigration Control and Refugee Recognition Act, Article 19-5 (e-Gov, version in force 1 October 2026)"),
"soumu_juki": ("https://www.soumu.go.jp/main_sosiki/jichi_gyousei/c-gyousei/zairyu/english/index.html", "Ministry of Internal Affairs and Communications", "総務省（外国人住民の住民基本台帳制度）", "Ministry of Internal Affairs and Communications: Basic Resident Registration System for foreign residents"),
"egov_nhi_rules": ("https://laws.e-gov.go.jp/law/333M50000100053", "National Health Insurance Act ordinance", "国民健康保険法施行規則（e-Gov法令検索）", "Ordinance for Enforcement of the National Health Insurance Act, Article 1 (e-Gov, version in force 1 October 2026)"),
"mlit_foreign_rental": ("https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000017.html", "Ministry of Land, Infrastructure, Transport and Tourism", "国土交通省（外国人の民間賃貸住宅入居円滑化ガイドライン）", "MLIT: Guideline for Facilitating Looking for and Moving in Rental Housing for Foreign Nationals"),
"nta_2875": ("https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2875.htm", "National Tax Agency", "国税庁（タックスアンサー No.2875）", "National Tax Agency: Tax Answer No.2875, residents and non-residents (law as of 1 April 2026)"),
"nta_nonresident": ("https://www.nta.go.jp/english/taxes/individual/12006.htm", "National Tax Agency", "国税庁（非居住者の課税）", "National Tax Agency: No.12006 Tax on the income of a non-resident"),
"soumu_ftth_2025": ("https://www.soumu.go.jp/main_content/001088979.xlsx", "MIC, 2025", "総務省（令和6年度末 FTTH世帯カバー率）", "Ministry of Internal Affairs and Communications: Fibre household coverage by prefecture and municipality, end of March 2025"),
"jnto_medical": ("https://www.jnto.go.jp/emergency/eng/mi_guide.html", "JNTO", "日本政府観光局（医療機関の検索）", "JNTO: Guide for when you are feeling ill (medical institution search)"),
```

- 既存の `isa_nomad_en`・`isa_nomad_list`・`node_site`・`node_room` はそのまま使う。`mofa` は開けなかったので、90日の行は `jnto_visa` を使う。
- `japantimes_nomad_2024`（49か国の報道）を使う場合だけ: `("https://www.japantimes.co.jp/news/2024/02/02/japan/society/digital-nomad-visa-march/", "The Japan Times, 2024", "ジャパンタイムズ 2024年", "The Japan Times: Japan’s digital nomad visas to require ¥10 million in income (2 February 2024)")`（ページは開けず、検索で確認）。

### E. 書き方の注意（断定しすぎない）

- ビザ・在留の条件は **出入国在留管理庁の2026年11月時点** と書く（“As of November 2026, the Immigration Services Agency says …”）。「個別の判断は在外公館・入管か行政書士へ」を節6に1回。
- 国保は「対象外」と言い切れる根拠が条文（施行規則 第1条第1号）にあるが、例外の書き方が細かいので “Because you won’t be on the resident register, you can’t join National Health Insurance, which is why private cover is a condition.” 程度に留める。
- 賃貸は「借りられない」と書かない。国交省のガイドラインは在留カードを**例として**挙げているだけ。“Many ordinary leases expect a residence card, a Japanese bank account and a local phone number, so …” と見解寄りに書くなら “In our experience / we think” を付ける（自社の体験には賃貸の審査の話はないので、見解として書く）。
- 税は定義（No.2875）と「日本での仕事への報酬は国内源泉所得」（No.12006）まで。「183日未満なら非課税」とは書かない。租税条約で変わりうると添えて、税理士へ。

### F. 海外の読み手の生の疑問（Reddit・旅行フォーラム・体験記。要約）

1. 在留カードは空港でもらえるのか、もらえないのか（ブログと掲示板で答えが割れている）。
2. 国民健康保険に入れないなら、どんな保険なら大使館で通るのか。手持ちの保険の証書に「日本でも有効」と明記がなく、旅行保険を買い足した、という声。
3. 会社員でなくフリーランス（海外の取引先）でも対象か。収入は何で証明するのか。
4. 結婚していないパートナーは一緒に来られるのか。
5. 6か月のあと、いったん出て戻ってこられるのか。何か月あければよいのか。
6. 観光で入ってから、日本の中で切り替えられるのか。
7. 家具付きの部屋を予約したら写真と違った、という不満。在留カードなしで普通の部屋を借りられるのか。
8. 東京以外の町だと回線は大丈夫か、コワーキングはあるか、現金しか使えない店が多いのでは。
9. 日本で家を買えばビザが出るのか（出ない、という前提の確認）。
10. 年収1,000万円は、手取りか税引き前か、家族の収入を足してよいか（入管は「申請人個人の年収」）。

### G. 開けなかったドメイン（編集長へ）

| ドメイン | 状態 | 何に要るか |
|---|---|---|
| `www.moj.go.jp`（入管のノマドのページ・対象国 PDF・Q&A） | 403（CloudFront。curl・WebFetch とも） | R1〜R4 の英語の文言、対象国の今の数、家族の条件の原文 |
| `www.isa.go.jp` | 403 | 同上（英語版） |
| `www.mofa.go.jp` | 403 | R3（必要書類・COE・手数料）、R10、査証発給統計（件数） |
| `*.emb-japan.go.jp`（在外公館。例 www.fi.emb-japan.go.jp・www.houston.us.emb-japan.go.jp・www.chicago.us.emb-japan.go.jp） | プロキシで遮断（接続 000・名前解決できず） | COE なしの申請の道・審査期間 |
| `www.japantimes.co.jp` | プロキシで遮断（000） | 開始時の対象国の数（49）・2025年の発給件数の報道 |

### H. 外部のページに書かれた命令

今回読んだページ・検索結果に、ファイル操作・URL へのアクセス・ルールの変更などの命令は見当たらなかった。
