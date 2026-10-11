#!/usr/bin/env python3
"""docs/dashboard.md を作り直す（進行管理部が毎回の作業の最後に実行する）。

材料: 記事ページ（tools/seo_check.py の結果）、docs/seo/calendar.md、docs/seo/log.md、
      docs/seo/data/ の最新データ。GitHub 上でそのまま読める Markdown で出力する。
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import seo_check  # noqa: E402


def section(md_path):
    p = ROOT / md_path
    return p.read_text(encoding="utf-8") if p.exists() else ""


def calendar_rows():
    """calendar.md の表のうち、未完了の行を返す"""
    rows = []
    text = section("docs/seo/calendar.md")
    m = re.search(r"(?ms)^## 進行中\s*$(.*?)(?=^## |\Z)", text)
    for line in (m.group(1) if m else "").splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line) and "状態" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and "完了" not in cells[-1]:
                rows.append(line)
    return rows


def log_entries(n=10):
    text = re.sub(r"(?s)```.*?```", "", section("docs/seo/log.md"))  # 書式見本を除く
    entries = re.split(r"(?m)^(?=## )", text)
    entries = [e.strip() for e in entries if e.startswith("## ")]
    return entries[:n]  # 新しいものが上


def latest_data():
    files = sorted((ROOT / "docs/seo/data").glob("*.json"))
    if not files:
        return None, None
    return files[-1].stem, json.loads(files[-1].read_text(encoding="utf-8"))


def main():
    today = seo_check.TODAY
    issues, articles = seo_check.check()
    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    live = [a for a in articles if a["published"] and a["published"] <= today]
    future = sorted([a for a in articles if a["published"] and a["published"] > today], key=lambda a: a["published"])

    L = ["# アキヤド 運用ダッシュボード", "",
         f"> 自動生成（`python3 tools/build_dashboard.py`）／最終更新 {today}。手で編集しないでください。", "",
         "## いまの状況", "",
         "| 指標 | 値 |", "|---|---|",
         f"| 公開中の記事 | {len(live)} 本 |",
         f"| 予約中の記事 | {len(future)} 本（最終 {future[-1]['published'] if future else '—'}） |",
         f"| SEOチェック | エラー {len(errors)} 件 ／ 警告 {len(warns)} 件 |"]
    day, data = latest_data()
    if data and data.get("gsc"):
        clicks = sum(r["clicks"] for r in data["gsc"]["pages"])
        imps = sum(r["impressions"] for r in data["gsc"]["pages"])
        pclicks = sum(r["clicks"] for r in data["gsc"]["pages_prev"])
        L += [f"| 検索クリック（直近28日） | {clicks:.0f}（前期間 {pclicks:.0f}） |",
              f"| 検索表示回数（直近28日） | {imps:.0f} |",
              f"| 最新レポート | [docs/seo/reports/{day}.md](seo/reports/{day}.md) |"]
    else:
        L += ["| 検索データ | 未取得（GA4/Search Console 連携の設定待ち） |"]

    # 記事の在庫が少ないと警告
    days_left = (dt.date.fromisoformat(future[-1]["published"]) - dt.date.fromisoformat(today)).days if future else 0
    if days_left < 21:
        L += ["", f"> ⚠️ 予約記事の在庫が残り {days_left} 日分です。企画・執筆を前倒ししてください。"]

    L += ["", "## これからの公開予定", "", "| 公開日 | カテゴリ | タイトル |", "|---|---|---|"]
    L += [f"| {a['published']} | {a['category']} | {a['title']} |" for a in future[:10]] or ["| — | | |"]

    cal = calendar_rows()
    L += ["", "## 制作中・企画中（docs/seo/calendar.md）", ""]
    if len(cal) > 0:
        head = [l for l in section("docs/seo/calendar.md").splitlines() if l.startswith("|")][:2]
        L += head + cal
    else:
        L += ["（なし）"]

    L += ["", "## SEOチェックのエラー", ""]
    L += [f"- `{e['page']}` {e['msg']}" for e in errors] or ["- なし ✅"]

    L += ["", "## 最近の稼働ログ（docs/seo/log.md）", ""]
    for e in log_entries(5):
        L += [e.replace("## ", "### ", 1), ""]

    out = ROOT / "docs" / "dashboard.md"
    out.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print(f"updated {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
