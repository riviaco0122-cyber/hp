---
name: seo-audit
description: サイト全体のテクニカルSEO/AIOチェック（tools/seo_check.py）を実行し、結果を解説して修正方針を出す。「SEOチェックして」「/seo-audit」で使う。
---

# SEO チェック

1. `python3 tools/seo_check.py` を実行する（JSON が必要なら `--json`）。
2. エラーは原因と直し方を、警告は優先度（相談につながる記事か・表示回数が多いか）つきで整理する。
3. 「直して」と言われた場合だけ、エンジニア部（`engineer`）に修正を依頼し、再実行してエラー 0 を確認する。
