# RIVIA&CO. コーポレートサイト ／ 暮らす旅の手帖 — 全社ルール

このリポジトリは合同会社RIVIA&CO.のサイト（静的 HTML/CSS/JS、GitHub → Vercel で公開）。オウンドメディア「暮らす旅の手帖」の SEO/AIO 運用を、AI社員のチームで自動化している。

## 組織（AI社員8部署）

| 部署 | 実体 | 役割 |
|---|---|---|
| 編集長（秘書室） | メインのセッション（このファイル＋Skills） | 定期実行の起点。作業を決めて各部署に振り、PR にまとめる |
| 進行管理部 | `.claude/agents/pm.md` | カレンダー・在庫・鮮度の管理、ログ・ダッシュボード・PR説明 |
| リサーチ部 | `.claude/agents/researcher.md` | ネタ箱の一次情報、YouTube・公的資料・競合の調査 |
| 企画・マーケ部 | `.claude/agents/marketer.md` | GA4/Search Console の分析、キーワード選定、構成案 |
| 執筆・編集担当 | `.claude/agents/writer.md` | 原稿の執筆・書き直し |
| エンジニア部 | `.claude/agents/engineer.md` | HTML化・組み込み、テクニカルSEO/AIO |
| 品質管理部 | `.claude/agents/qa.md` | 採点と差し戻し（評価者） |
| ブランド学習係 | `.claude/agents/brand-learner.md` | `docs/brand/` の作成・更新 |

定型業務は `.claude/skills/`: `/seo-daily`（日次サイクル・毎朝9時の定期実行の入口）、`/write-article`、`/seo-audit`、`/source-intake`、`/brand-learn`。

## 絶対のルール

1. **main に直接 push しない・マージしない。** 必ず作業ブランチ → main 向け PR。人が Vercel のプレビューを見てマージする（＝最終確認）。
2. **事実を作らない。** 数値・制度には出典。RIVIA の体験談は `docs/brand/experience.md` にあるものだけ。他者の発信は出典（発信者名・URL）つきで要約して使う。
3. **人の確認が必要なもの**（`docs/seo/playbook.md` 6章）は、PR の「人の確認が必要な点」に必ず書き出す。
4. `python3 tools/seo_check.py` のエラーが 0 でない状態で PR を出さない。
5. 既存ページの URL を変えない。公開日を過去にさかのぼって付けない。
6. 鍵・トークンをファイルに書かない、コミットしない（環境変数から読む）。

## 判断基準・資料

- サイトの仕様（文言・構成・デザイン方針）: `docs/site-spec.md` ← ページを変えたらここも一致させる
- SEO/AIO の基準と品質の採点基準: `docs/seo/playbook.md`
- ブランド（文体・用語・思想・体験・NG）: `docs/brand/`
- 一次情報の置き場と扱い方: `docs/sources/README.md`（人が `docs/sources/inbox/` にメモを置く）
- カレンダー／キーワード／ログ: `docs/seo/calendar.md`、`docs/seo/keywords.md`、`docs/seo/log.md`
- ダッシュボード（自動生成）: `docs/dashboard.md`
- GA4/Search Console/YouTube の設定手順: `docs/seo/analytics-setup.md`

## サイトの構造（エンジニア部向けの要点）

- HTML はすべて `pages/` にある。公開URLは `vercel.json` の rewrites で `/xxx.html` → `pages/xxx.html`、`/media/xxx.html` → `pages/media/xxx.html`。ページ内のリンクは公開URL基準の相対パス（記事からは `../media.html`、`../../images/...`）。
- `docs/`・`tools/`・`.claude/`・`CLAUDE.md` は `.vercelignore` で公開対象外。
- 記事 HTML は元々リポジトリ外の生成スクリプトで作られており、`<n-w>`（改行制御）・`<wbr>` を多用している。新しい記事は **同じカテゴリの既存記事をコピーして雛形にする**。
- 記事カードは `media.html`・`index.html`・サービスページ・全記事の「あわせて読みたい記事」に入っている。追加は `tools/add_article.py`（エンジニア部が初回に作成）で行う。
- 予約公開: 現在は `js/main.js` が `data-publish`／`data-date` と今日の日付を比べて、公開日前の記事を隠している（HTML と sitemap には載っている）。
- 計測: GA4（G-RZVE2XBPQ2）と Microsoft Clarity のタグが全ページの head にある。消さない。

## ツール

| コマンド | 用途 |
|---|---|
| `python3 tools/seo_check.py [--json]` | 全ページの SEO/AIO チェック（標準ライブラリのみ） |
| `python3 tools/analytics.py` | GA4/Search Console のレポート（要 `pip install -r tools/requirements.txt` と環境変数） |
| `python3 tools/youtube_research.py "キーワード"` | YouTube の動画情報・概要欄・人気コメント（要 `YOUTUBE_API_KEY`） |
| `python3 tools/build_dashboard.py` | `docs/dashboard.md` の再生成 |

## 書き方

- コミットメッセージ・PR・ドキュメントは日本語。
- 日付は日本時間で扱う。
