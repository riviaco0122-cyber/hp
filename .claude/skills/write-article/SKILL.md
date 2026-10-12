---
name: write-article
description: 指定したテーマ（またはキーワード表の次の候補）で、新規記事を1本、リサーチ→構成→執筆→品質管理→HTML化→PRまで作る。「記事を1本書いて」「/write-article <テーマ>」で使う。
---

# 記事を1本作る

引数にテーマがあればそれを、なければ `docs/seo/keywords.md` の「記事化予定」の先頭を使う。
日次サイクル（`/seo-daily`）と同じ日には実行しない（同じ記事を二重に作らないため）。不合格のときの扱いは playbook 5-4 に従う。新規記事は週2本まで（playbook 1章）。

1. 作業ブランチ `seo/article-<スラッグ>` を作る。
2. `researcher` → リサーチメモ（YouTube 調査・一次情報・出典の確認）。統計の数字が要るときは、先に編集長が `python3 tools/estat.py` で e-Stat から取って渡す（出典つき）
3. `marketer` → 構成案 `docs/seo/briefs/<スラッグ>.md`。公開予定日は **今日（日本時間）の翌日**（人が確認してマージした日の翌日に公開するため。人の方針 2026-10-12）。マージが遅れたら日次サイクルが付け直す。
4. `writer` → 原稿 `docs/seo/drafts/<スラッグ>.md`（自己採点で `tools/article_score.py` の機械採点40点にしてから提出）
5. `qa` → 100点満点で採点（playbook 5章）。**95点未満・ゲート違反なら、qa が指定した戻る工程（2 リサーチ／3 構成案／4 執筆）からやり直し、最初から採点し直す**（最大5回）。
6. `engineer` → 記事データ（`tools/articles_auto.py`）に足し、`python3 tools/eyecatch.py <スラッグ>` でアイキャッチを作ってから `python3 tools/build.py` で作り直す（一覧・sitemap・llms.txt・仕様書まで自動で更新）。seo_check エラー0・`node tools/check/site_check.js --no-visual` 重大0、seo_check のエラー 0 を確認
7. `qa` → HTML を採点（95点以上・ゲート違反なし）。PR の前に `node tools/check/site_check.js`（本番との見た目の比較つき）を実行する。不合格なら同じく戻る
8. 5回で95点に届かなければ PR に入れず、採点結果をログに残して終える
9. `bash tools/sync_base.sh` で本番ブランチを取り込み衝突を自動解消（seo-daily と同じ）。`pm` → 記録と PR 説明（採点表の内訳を載せる） → コミット・push・本番ブランチ（GitHub のデフォルトブランチ）向け PR 作成（マージはしない）
10. PR の説明の冒頭に確認用リンク（`/media/<スラッグ>.html?preview=1`）を書く（予約公開の記事は `?preview=1` がないとプレビューで見えない。seo-daily と同じ）
