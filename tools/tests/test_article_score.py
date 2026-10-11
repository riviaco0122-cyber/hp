#!/usr/bin/env python3
"""tools/article_score.py の回帰テスト（標準ライブラリのみ）。

使い方: python3 tools/tests/test_article_score.py
ケースは tools/tests/score_cases.json。失敗が1件でもあれば終了コード 1。
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import article_score as A  # noqa: E402

CASES = json.loads((HERE / "score_cases.json").read_text(encoding="utf-8"))
fails = []
count = 0


def check(ok, label, detail=""):
    global count
    count += 1
    if not ok:
        fails.append(f"NG {label} {detail}")


def md_doc(body, sources=()):
    src = "\n".join(f"- {s}" for s in sources)
    return (f"---\ntitle: テスト記事\ndescription: テスト\nkeyword: テスト\n---\n"
            f"## この記事のポイント\n- 要点\n\n## 本文の見出し\n導入の文です。\n\n{body}\n\n"
            f"## よくある質問\n### Q. 質問ですか？\n回答です。\n\n## 参考資料\n{src}\n")


def html_doc(body, sources=()):
    li = "".join(f"<li>{s}</li>" for s in sources)
    return (f'<h1 class="article__title">テスト記事</h1><p class="article__lead">導入です。</p>'
            f'<section class="article__section" id="s1">{body}</section>'
            f'<section class="sources"><ul>{li}</ul></section>')


def run_md(body, sources=()):
    return A.score(A.parse_md(md_doc(body, sources)))


def item(r, prefix):
    return next(i for i in r["項目"] if i["項目"].startswith(prefix))


for c in CASES["gate"]:
    r = run_md(c["text"])
    check(bool(r["ゲート違反"]), f"[gate] {c['case']}", f"text={c['text']!r} → ゲート違反なし")
for c in CASES["no_gate"]:
    r = run_md(c["text"])
    check(not r["ゲート違反"], f"[no_gate] {c['case']}", f"text={c['text']!r} → {r['ゲート違反']}")
for c in CASES["minor"]:
    note = item(run_md(c["text"]), "NG表現（軽微）")["根拠"]
    got = [] if note == "なし" else note.split("、")
    check(got == c["expect"], f"[minor] {c['case']}", f"got={got} expect={c['expect']}")
for c in CASES["glossary"]:
    note = item(run_md(c["text"]), "表記ゆれ")["根拠"]
    got = [] if note == "なし" else note.split("、")
    check(got == c["expect"], f"[glossary] {c['case']}", f"got={got} expect={c['expect']}")
for h in CASES["headings"]["pass"]:
    check(bool(re.search(A.HEADING_FORM, h)), f"[heading pass] {h}")
for h in CASES["headings"]["fail"]:
    check(not re.search(A.HEADING_FORM, h), f"[heading fail] {h}")
for c in CASES["sources_md"]:
    note = item(run_md("本文です。", [c["line"]]), "参考資料")["根拠"]
    m = re.match(r"(\d+)件（うち公的機関 (\d+)件", note)
    check(m and (int(m.group(1)) == 1) == c["counted"] and (int(m.group(2)) == 1) == c["public"],
          f"[sources_md] {c['case']}", f"note={note}")
for c in CASES["sources_html"]:
    note = item(A.score(A.parse_html(html_doc("<h2>見出し</h2><p>本文です。</p>", [c["line"]]))), "参考資料")["根拠"]
    m = re.match(r"(\d+)件（うち公的機関 (\d+)件", note)
    check(m and m.group(1) == "1" and (m.group(2) == "1") == c["public"] and "URLなし" in note,
          f"[sources_html] {c['case']}", f"note={note}")
for c in CASES["html"]:
    r = A.score(A.parse_html(html_doc(c["body"])))
    check(bool(r["ゲート違反"]) == c["gate"], f"[html] {c['case']}", f"→ {r['ゲート違反']}")

# 既存記事でゲート違反が出ないこと
articles = [p for p in sorted((ROOT / "pages/media").glob("*.html"))
            if not p.stem.startswith(("category-", "guide-", "search"))]
names = {p.stem for p in articles}
for slug in CASES["existing_no_gate"]:
    check(slug in names, f"[existing] {slug} が存在する")
for p in articles:
    r = A.score(A.parse_html(p.read_text(encoding="utf-8")))
    check(not r["ゲート違反"], f"[existing] {p.stem}", f"→ {r['ゲート違反']}")

print("\n".join(fails))
print(f"{count - len(fails)}/{count} 件 OK")
sys.exit(1 if fails else 0)
