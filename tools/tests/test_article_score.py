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

# --slug（記事データの1記事）: build 済みの HTML と記事データが一致し、ゲート違反がないこと
try:
    import build as B  # noqa: E402  要 pip install budoux beautifulsoup4 pillow
except ImportError as ex:
    B = None
    print(f"[slug] build.py を読み込めないため省略: {ex}")
if B is not None:
    for a in B.ARTICLES:
        f = ROOT / "pages/media" / f"{a['slug']}.html"
        check(f.is_file(), f"[slug] {a['slug']} の HTML がある")
        if not f.is_file():
            continue
        h = A.parse_html(f.read_text(encoding="utf-8"))
        stale = A.stale_fields(A.parse_article(a), h)
        check(not stale, f"[slug] {a['slug']} の HTML と記事データが一致", f"→ {stale}（python3 tools/build.py を実行）")
        r = A.score(A.parse_article(a))
        check(not r["ゲート違反"], f"[slug] {a['slug']}（記事データ）", f"→ {r['ゲート違反']}")
    # 食い違いの検出: FAQ を1問書き換えたら「よくある質問」が違うと分かること
    a0 = dict(B.ARTICLES[0], faq=[("書き換えた質問ですか？", "回答")] + list(B.ARTICLES[0]["faq"][1:]))
    h0 = A.parse_html((ROOT / "pages/media" / f"{a0['slug']}.html").read_text(encoding="utf-8"))
    check(A.stale_fields(A.parse_article(a0), h0) == ["よくある質問"], "[slug] 食い違いを検出する")

print("\n".join(fails))
print(f"{count - len(fails)}/{count} 件 OK")
sys.exit(1 if fails else 0)
