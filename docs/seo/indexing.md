# インデックス登録されない問題の調べと対策（2026-10-15）

Search Console の「ページがインデックスに登録されなかった理由」（2026-10-15 時点）:

| 理由 | ページ数 | 見立て | 対応 |
|---|---|---|---|
| ページにリダイレクトがあります | 8 | 古い URL（記事の統合・テーマ名の変更で 301 を付けたもの）と、`http://`・`www.` 付きの URL。**意図どおりで、直すものではない** | なし（sitemap・サイト内リンクには載せていないことを確認済み） |
| リダイレクト エラー | 1 | URL は `https://rivia-co.com/media.html`（前回のクロール 2026-10-12）。今の設定（vercel.json）では `media.html` は転送されず 200 を返す。考えられる原因は2つ: ①10/12 はサイトの作り替え（pages/ への移動など）が続いた日で、そのときの一時的な状態 ②sitemap に載せていた公開日前の記事を開くと、`js/main.js` が `media.html` へ転送していた（Google はこれを「リダイレクト」として扱う） | ②を直した（公開日前の記事を sitemap から外す）。人が「URL 検査 → 公開 URL をテスト」で今の状態を確かめ、「修正を検証」を押す |
| 検出 - インデックス未登録 | 69 | Google が URL は知っているが、まだ取りに来ていない。sitemap の 78 件のほぼすべて。**新しいドメインで、短い期間にページが一気に増えたときに典型的な状態**。技術的なブロック（noindex・robots・canonical の誤り）はない | サイト側の改善＋人の作業（下） |

## サイト側で直したこと

1. **トップページへのリンクを `/` にそろえた。** 全ページのロゴ・パンくず・フッターが `/index.html`（214か所）を指していた。`/index.html` は `/` と同じ中身の別 URL として見つかるため、正規の URL（canonical は `/`）と食い違っていた。`tools/build.py` の `relative_to_root()` で、トップへのリンクを `/` に置き換える。
2. **公開日前の記事を sitemap から外した**（2026-10-15 追加）。公開日前の記事ページは JS で記事一覧へ転送するため、Google に転送として見つかるのを避ける。公開日を迎えて作り直すと載る。
3. **sitemap の一覧ページに更新日（lastmod）を付けた。** アキヤドのトップ・テーマ別・ガイド・体系的に学ぶのページに、載っている記事のいちばん新しい更新日を付ける（Google がどれから取りに来るかの手がかり）。

確認済み（問題なし）: robots.txt はすべて許可／sitemap の 78 件はすべて 200・canonical が自分自身・noindex なし／サイト内リンクに転送元の URL はない／記事の一覧はサーバーの HTML にリンクとして出ている（JS がなくてもたどれる）。

## 人にお願いしたいこと

- [x] 「リダイレクト エラー」の URL を確認（`https://rivia-co.com/media.html`）
- [ ] 「URL 検査」に `https://rivia-co.com/media.html` を入れ、「公開 URL をテスト」→「ページは Google に登録できます」と出たら「インデックス登録をリクエスト」
- [ ] この変更が本番に反映されたら、Search Console の「サイトマップ」で `https://rivia-co.com/sitemap.xml` を**もう一度送信**する。
- [ ] 「URL 検査」で、大事なページから順に **「インデックス登録をリクエスト」**（1日10件程度が上限）: `/`、`/about.html`、`/media.html`、サービス5ページ、アクセスを集めたい記事。
- [ ] 「リダイレクト エラー」と「ページにリダイレクトがあります」の行で **「修正を検証」** を押す（後者は意図どおりなので、検証で「失敗」と出ても問題ない）。
- [ ] 外からのリンクを増やす（Google がサイトを見つけて、重要だと判断する一番の手がかり）: Google ビジネスプロフィール、Instagram・X・note のプロフィール、NODE Shimoda の施設サイトや Airbnb の紹介文から `https://rivia-co.com/` へリンクする。
- [ ] 任意: Search Console に**ドメインプロパティ**（`rivia-co.com`）を追加すると、`www.` や `http://` も含めて見られる。

## 見通し

「検出 - インデックス未登録」は、新しいサイトでは数週間〜数か月かけて少しずつ減るのがふつう。毎日の定期実行で Search Console のデータを見て、2週間たっても登録数が増えなければ、内部リンクの強化（トップから主要記事へのリンク）や記事数の絞り込みを検討する。

## 2026-10-22 の見直し（Search Console のスクリーンショットより）

| 理由 | ページ数 | 見立て | 対応 |
|---|---|---|---|
| ページにリダイレクトがあります（検証「失敗」） | 10 | ①`kankei-jinko-and-inns` は記事の統合で付けた 301 で、意図どおり。②ほかの記事・`/media/plans.html`・`/service-operation.html` は、今の設定（vercel.json）では転送されず 200 を返す。前回のクロールが 10/12〜10/16 で、サイトの作り替えが続いた時期の状態が残っていると考えられる。③あわせて、**公開日前の記事ページを JS で記事一覧へ転送していた**（`js/main.js`）。記事は一覧のリンク（HTML）から見つかるため、Google がこれを「リダイレクト」と記録しうる | ③をやめた（公開日前の記事ページも、転送せずそのまま表示する。一覧・検索・ガイドからは今までどおり隠す）。site_check も「転送されないこと」を確かめるように変えた |
| 代替ページ（適切な canonical タグあり） | 1 | `/index.html` は `/` と同じ中身で、canonical が `/` を指している。**意図どおりで、直すものではない** | なし |
| クロール済み - インデックス未登録 | 2 | `/about.html`、`cleaning-linen-operations`。技術的な問題はなく、Google が登録を見送った状態 | タイトルの見直し（cleaning-linen-operations）。人が「インデックス登録をリクエスト」 |
| 検出 - インデックス未登録 | 36 | 新しいサイトでは時間とともに減る | 引き続き様子を見る |

あわせて、検索結果で「民泊の記事」と分かるように、記事のタイトルに「民泊」を入れた（29本）。事例を比べる一覧記事（`minpaku-case-list`）は、事例が増え続けるため削除し、`/media.html` へ 301 を付けた。

### 人にお願いしたいこと（2026-10-22）：Search Console の操作手順

**この PR が本番に反映されてから**行う（反映前に検査すると、古い状態のまま記録される）。反映の確認：ブラウザで `https://rivia-co.com/media.html` を開き、ファーストビューに「取材した主な事例」のカルーセルがあれば反映済み。

#### 手順1　サイトマップを送り直す（1回だけ・1分）

1. Search Console（https://search.google.com/search-console ）を開き、左上のプロパティが `https://rivia-co.com/` になっていることを確かめる。
2. 左のメニューの「インデックス作成」→「**サイトマップ**」を押す。
3. 上の「新しいサイトマップの追加」の欄に `sitemap.xml` と入力し（`https://rivia-co.com/` の後ろに続く部分だけ）、「**送信**」を押す。
4. 下の「送信されたサイトマップ」の表で、ステータスが「**成功しました**」、検出されたページ数が 80 前後になっていれば完了。「取得できませんでした」と出たら、数時間おいてもう一度送る。

#### 手順2　大事なページから「インデックス登録をリクエスト」する（1日10件まで・1件1〜2分）

1. 画面いちばん上の検索窓（「https://rivia-co.com/」内のすべての URL を検査）に、下の表の URL を1つ貼り付けて Enter。
2. 結果が出るまで数十秒待つ。
   - 「**URL は Google に登録されています**」→ その URL は済み。次へ。
   - 「**URL が Google に登録されていません**」→ 3へ。
3. 右上の「**公開 URL をテスト**」を押し、1〜2分待つ。
   - 「**URL は Google に登録できる可能性があります**」→ 4へ。
   - 「ページにリダイレクトがあります」「noindex」などと出たら、**リクエストせず**、その URL と画面のスクリーンショットを Claude に送る（サイト側で直す）。
4. 「**インデックス登録をリクエスト**」を押す。1〜2分の確認のあと「**インデックス登録をリクエスト済み**」と出たら完了。「割り当て量を超えました」と出たら、その日はおしまい（翌日に続きを）。
5. 次の URL へ。1日10件を目安に、下の順で進める。

| 日 | リクエストする URL（上から順に） |
|---|---|
| 1日目 | `https://rivia-co.com/`、`/media.html`、`/about.html`、`/media/guide-sell.html`、`/media/guide-use.html`、`/media/guide-side.html`、`/media/plans.html`、`/service-operation.html`、`/media/akiyado-what-we-do.html`、`/media/why-akiya-utilization-now.html` |
| 2日目 | 「ページにリダイレクトがあります」に出ていたページ：`/media/case-owner-rental-side-business.html`、`/media/akiya-demolish-or-renovate.html`、`/media/akiya-lease-types.html`、`/media/minpaku-management-company.html`、`/media/minpaku-vs-rental-income.html`、`/media/inn-kpi-basics.html`、`/media/cleaning-linen-operations.html`、`/media/learn.html`、`/media/service-kariage.html`、`/media/service-kaigyo.html` |
| 3日目 | `/media/akiya-utilization-options.html`、`/media/inn-startup-funding.html`、`/media/akiya-minpaku-suitability.html`、`/media/minpaku-start-steps.html`、`/media/akiya-inherited-house-to-inn.html`、`/media/case-rental-house-inn-first-year.html`、`/media/akiyado-consultation-flow.html`、`/media/service-kaitori.html`、`/service-management.html`、`/contact.html` |
| 4日目以降 | 「検出 - インデックス未登録」の一覧（ページ → その行を押す → 下の「例」）に残っている URL を、上から10件ずつ |

※ URL はすべて `https://rivia-co.com` を頭に付けて貼る（例：`https://rivia-co.com/media.html`）。
※ 新しい事例（`case-owner-setouchi-cycling`・`case-owner-castle-town-nagaya`・`case-owner-satoyama-airdna`）は、**公開日（10/23・10/25・10/27）を過ぎてから**リクエストする。公開日前は一覧に出ず、sitemap にも載らないため。

#### 手順3　「修正を検証」をもう一度押す（手順2の2日目が終わってから・1分）

1. 左のメニューの「インデックス作成」→「**ページ**」を押す。
2. 下の「ページがインデックスに登録されなかった理由」の表で、「**ページにリダイレクトがあります**」の行を押す。
3. 上の「**修正を検証**」を押す（前回の検証が「失敗」でも押せる）。
4. 「確認」の欄が「開始」になる。結果が出るまで、数日〜2週間ほどかかる。
   - `https://rivia-co.com/media/kankei-jinko-and-inns.html` と `https://rivia-co.com/media/minpaku-case-list.html` は、記事の統合・削除で付けた**意図どおりの 301 転送**なので、この2件は残ってよい。
   - それ以外が「失敗」で残ったら、その URL を Claude に送る。

#### 手順4　待つもの（操作は不要）

- 「**検出 - インデックス未登録**」（前回のクロールが「該当なし」）：Google が URL は知っているが、まだ一度も取りに来ていない状態。エラーではない。新しいサイトでは数週間〜数か月かけて減る。手順2で早められる。
- 「**代替ページ（適切な canonical タグあり）**」の `/index.html`：`/` と同じ中身で、正しい扱い。何もしなくてよい。
- 「**クロール済み - インデックス未登録**」：手順2でリクエストしたうえで、2〜3週間待つ。

#### 手順5　2〜3週間後に見るところ

- 「ページ」の上のグラフで、緑（登録済み）が増えているか。
- 増えていなければ、「ページ」の画面のスクリーンショットを Claude に送る（トップから主要記事へのリンクの強化や、記事の絞り込みを検討する）。
- あわせて、外からのリンクを増やす：Google ビジネスプロフィール、Instagram・X・note のプロフィール、Airbnb の紹介文などに `https://rivia-co.com/` を載せる（Google がサイトを見つけて大事だと判断する、いちばんの手がかり）。
