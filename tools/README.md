# サイトを作るスクリプト（tools/）

`pages/`・`css/`・`js/`・`seo/` の中身は、このフォルダのスクリプトで作っています。
HTMLを直接書き換えず、ここを直してから作り直してください。
このフォルダは公開されません（`.vercelignore` で除外）。

## 作り直す

```sh
pip install budoux beautifulsoup4 pillow
python3 tools/build.py
```

日本語のページを作ったあと、英語版（`pages/en/`）も自動で作ります。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `build.py` | 全ページの文言・構成・プラン・アキヤドの設定（テーマ、ガイド、よくある悩みなど） |
| `articles_sched1.py`・`articles_sched2.py`・`articles_case.py` | アキヤドの記事（公開日は各記事の `date`） |
| `articles_auto.py` | AI社員チーム（毎朝の日次サイクル）が追加する記事 |
| `figures.py` | 記事の図解（`ARTICLE_FIGURES` に、記事ごとの図を書く） |
| `i18n/` | 英語版の作成（`build_en.py`）と英訳（`en_1.py`〜`en_4.py`） |
| `check/enchk.js` | 英語版のリンク切れ・はみ出し・訳し漏れの確認 |
| `check/site_check.js` | サイト全体の点検（全ページ×スマホ・PC幅で、JSエラー・読み込み失敗・リンク切れ・はみ出し・本番との見た目の差分。例：`node tools/check/site_check.js --no-visual`） |
| `forms/Code.gs` | お問い合わせフォームの受け口（Google Apps Script。自動返信・添付ファイル保存） |
| `check/lazyshot.js` | ページ全体のスクリーンショット（例：`node tools/check/lazyshot.js media.html 390 shot.png`） |

## よく使う設定

* 記事の公開日：記事の `date` を変える（公開日前の記事は、自動で一覧から隠れる）
* お客様の声：実際の声がそろったら `build.py` の `SAMPLE_VOICES` を差し替え、`SHOW_SAMPLE_VOICES=1 python3 tools/build.py` で確認
* フォームの送信先：`YOUR_FORM_ID`・`YOUR_CAREERS_FORM_ID` を Formspree の発行IDに置き換える
