#!/usr/bin/env python3
"""コードの健康診断（月1回の点検。/seo-daily の「毎月21日以降の最初の実行」で使う）。

使い方:
  python3 tools/code_health.py            # 数字を表示する
  python3 tools/code_health.py --record   # 数字を docs/seo/code-health.md の表に1行足す（前回と比べられるように）

見るもの（増え続けていたら、整理の合図）:
  - 大きいファイルの行数（build.py・style.css・main.js・figures.py）
  - CSS の !important の数、同じ条件（@media）で同じセレクタを何度も書いている数、
    どのページでも使われていないルールの数（消すのは python3 tools/css_prune.py --apply）
  - SEO の点検（seo_check）のエラー・警告の数（インデックス登録の土台: sitemap・canonical・noindex・リンク切れ・孤立ページ・robots.txt・重複 URL）
数字の目安と、整理のやり方は .claude/skills/seo-daily/SKILL.md の「月1回のコードの点検」。
"""
import collections
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import css_prune  # noqa: E402

RECORD = os.path.join(ROOT, "docs", "seo", "code-health.md")
FILES = ["tools/build.py", "css/style.css", "js/main.js", "tools/figures.py"]


def lines(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return sum(1 for _ in f)


def css_stats():
    text = open(css_prune.CSS, encoding="utf-8").read()
    plain = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    counts = collections.Counter()

    def walk(start, end, ctx):
        for it in css_prune.parse_block(text, start, end):
            if it["kind"] == "group":
                walk(it["body_start"], it["body_end"], ctx + (it["prelude"],))
            elif it["kind"] == "rule":
                counts[(ctx, it["prelude"])] += 1

    walk(0, len(text), ())
    removals, rewrites, _ = css_prune.plan(text, css_prune.make_alive(*css_prune.load_usage()))
    return {
        "important": plain.count("!important"),
        "repeated": sum(1 for v in counts.values() if v > 1),
        "unused": len(removals) + len(rewrites),
    }


def seo_stats():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "seo_check.py"), "--json"], capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"errors": "?", "warnings": "?"}
    return {"errors": len(data.get("errors", [])), "warnings": len(data.get("warnings", []))}


def main():
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()
    sizes = {f: lines(f) for f in FILES}
    css = css_stats()
    seo = seo_stats()
    print("## コードの健康診断", today)
    for f, n in sizes.items():
        print(f"- {f}: {n} 行")
    print(f"- CSS の !important: {css['important']} 個")
    print(f"- CSS で同じ条件・同じセレクタを2回以上書いている: {css['repeated']} 件")
    print(f"- CSS のどのページでも使われていないルール: {css['unused']} 件（python3 tools/css_prune.py で一覧）")
    print(f"- seo_check: エラー {seo['errors']} 件・警告 {seo['warnings']} 件")
    if "--record" in sys.argv:
        row = (f"| {today} | " + " | ".join(str(sizes[f]) for f in FILES)
               + f" | {css['important']} | {css['repeated']} | {css['unused']} | {seo['errors']}/{seo['warnings']} | |\n")
        with open(RECORD, "a", encoding="utf-8") as f:
            f.write(row)
        print(f"\n{os.path.relpath(RECORD, ROOT)} に1行足した（「整理したこと」の欄は手で書く）")


if __name__ == "__main__":
    main()
