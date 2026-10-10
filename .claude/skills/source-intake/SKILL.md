---
name: source-intake
description: ネタ箱（docs/sources/inbox）の一次情報やYouTube調査を、記事ネタ・ブランドの体験談に振り分ける。「ネタ箱を処理して」「YouTubeで◯◯を調べて」「/source-intake」で使う。
---

# 一次情報の取り込み

1. `researcher` に `docs/sources/README.md` のルールで inbox の処理を依頼する。キーワードの指定があれば `tools/youtube_research.py` での調査も依頼する。
2. 追加された記事ネタ（`docs/seo/keywords.md`）と体験談（`docs/brand/experience.md`）を一覧にして報告する。
3. コミットして push する（記事本文の変更はないので、PR は日次サイクルにまとめてよい）。
