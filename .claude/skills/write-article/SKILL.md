---
name: write-article
description: 指定したテーマ（またはキーワード表の次の候補）で、新規記事を1本、リサーチ→構成→執筆→品質管理→HTML化→PRまで作る。「記事を1本書いて」「/write-article <テーマ>」で使う。
---

# 記事を1本作る

引数にテーマがあればそれを、なければ `docs/seo/keywords.md` の「記事化予定」の先頭を使う。

1. 作業ブランチ `seo/article-<スラッグ>` を作る。
2. `researcher` → リサーチメモ（YouTube 調査・一次情報・出典の確認）
3. `marketer` → 構成案 `docs/seo/briefs/<スラッグ>.md`。公開予定日は、予約済みの最後の記事の 2 日後（`docs/dashboard.md` 参照）。
4. `writer` → 原稿 `docs/seo/drafts/<スラッグ>.md`
5. `qa` → 採点。不合格なら writer に差し戻し（最大3回）。
6. `engineer` → HTML 化と一覧・sitemap・site-spec への組み込み、seo_check のエラー 0 を確認
7. `qa` → HTML の最終確認
8. `pm` → 記録と PR 説明 → コミット・push・main 向け PR 作成（マージはしない）
