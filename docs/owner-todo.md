# お願いしたいこと（人の作業リスト）

AI社員チームが自動で動くために、人にしかできない作業をまとめました。すべて無料でできます。
チェックが付いたら、Claude に「終わった」と伝えてください。

---

## 1. GA4・Search Console・YouTube の連携設定（1回だけ）

詳しい手順は [`docs/seo/analytics-setup.md`](seo/analytics-setup.md) にあります。

### ✅ 済んだこと
- [x] Google Cloud のプロジェクトとサービスアカウントを作成（`seo-bot@rivia-seo.iam.gserviceaccount.com`）
- [x] Search Console を URL プレフィックス（`https://rivia-co.com/`）で登録し、GA4 を使って所有者を確認
- [x] Search Console に `seo-bot@rivia-seo.iam.gserviceaccount.com` を「制限付き」で追加

### 1-1. Google Cloud（https://console.cloud.google.com/ ・プロジェクト `rivia-seo`）
- [ ] 「API とサービス」→「ライブラリ」で次の3つを **有効にする**（済んでいれば不要）
  - Google Search Console API
  - Google Analytics Data API
  - YouTube Data API v3
- [ ] 「IAM と管理」→「サービスアカウント」→ `seo-bot` →「キー」→「鍵を追加」→「新しい鍵を作成」→ **JSON** をダウンロード
- [ ] 「API とサービス」→「認証情報」→「認証情報を作成」→「API キー」を作成し、「API の制限」で **YouTube Data API v3 のみ** に制限する

### 1-2. GA4（https://analytics.google.com/ ）
- [ ] 「管理」→「プロパティのアクセス管理」→「＋」→ `seo-bot@rivia-seo.iam.gserviceaccount.com` を **閲覧者** で追加
- [ ] 「管理」→「プロパティの詳細」で **プロパティID（数字）** を控える（`G-RZVE2XBPQ2` とは別物）

### 1-3. Claude のクラウド環境に登録する
⚠️ 鍵をチャットに貼らないでください。

セッション画面のタイトルバーにあるクラウド環境のメニュー →「Edit」→ 環境変数に登録します。

| 変数名 | 値 |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | ダウンロードした JSON ファイルの中身（1行にして貼る） |
| `GA4_PROPERTY_ID` | 1-2 で控えたプロパティID（数字） |
| `GSC_SITE_URL` | `https://rivia-co.com/` |
| `YOUTUBE_API_KEY` | 1-1 で作成した API キー |

- [ ] 4つを登録した
- [ ] 登録後に **新しいセッション** を始め、Claude に「連携の動作確認をして」と伝える（いまのセッションには反映されません）

### 後回しでよいこと
- [ ] お名前.com のパスワードを再発行したら、Search Console にドメインプロパティ（`rivia-co.com`）も追加する（`www.` や `http://` も含めて集計できるようになる。任意）

---

## 2. ブランド学習の確認（フェーズ2のあと・1回だけ）

- [ ] ブランド学習係が作る `docs/brand/` を読み、違和感のある箇所を直す（または Claude に指示する）
  - 特に `philosophy.md`（RIVIA の考え方）と `experience.md`（記事に使ってよい実績・体験）
- [ ] 確認が済んだ節には `<!-- 人が確認済み -->` と書く（AI がその部分を勝手に書き換えなくなります）

---

## 3. 一次情報をネタ箱に入れる（思いついたときに・随時）

`docs/sources/inbox/` にファイルを置くだけです（GitHub のスマホアプリやブラウザの「Add file」から作れます）。形式は自由です。

| 入れるもの | 例 | 価値 |
|---|---|---|
| 代表のメモ・音声の文字起こし | `2026-10-12_清掃の外注で失敗した話.md` | ★★★（いちばん高い） |
| 運営で得た数値・事例 | 稼働率の推移、オーナーからの相談内容（個人が特定できない形で） | ★★★ |
| 気になった X のポスト | URL と本文のコピー | ★★ |
| 参考になった YouTube の要約 | URL と要約（Gemini の要約でも可） | ★★ |

---

## 4. PR の確認とマージ（毎週・10分ほど）

週次サイクルが終わると、main 向けの PR ができます。

- [ ] PR の **「人の確認が必要な点」** を読む（法律・税金・補助金の記述、RIVIA の実績、デザインの変更など）
- [ ] PR に付く **Vercel のプレビューURL** で、指定されたページの見た目を確認する
- [ ] 問題なければ **マージ**（＝公開）。直してほしい点があれば、PR にコメントするか Claude に伝える

運用状況は [`docs/dashboard.md`](dashboard.md) でいつでも確認できます。

---

## 5. Claude に伝えてほしいこと（いま）

- [ ] **フェーズ2（ブランド学習）を始めてよいか**
- [ ] 週次サイクルを動かす **曜日と時刻**（例: 毎週月曜 朝9時）
