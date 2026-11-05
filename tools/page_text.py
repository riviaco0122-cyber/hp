#!/usr/bin/env python3
"""生成された HTML を、読むための本文だけのテキストにして出す。

記事の HTML は1ファイル 10万字を超えることがあり（ナビ・フッター・SVG・スクリプトを含む）、
そのまま Read すると AI のトークンを大量に食う。採点・文体の学習・内容の確認はこれで読む。
見た目（スマホ幅の崩れ）は site_check のスクリーンショットで見る。

使い方:
  python3 tools/page_text.py pages/media/<slug>.html [...]
  python3 tools/page_text.py pages/media/<slug>.html --all   # main の外（ナビ等）も含める

出力: タイトル・description のあと、見出し（#）・段落・箇条書き（-）・表（| 区切り）・
画像の alt・リンク先を、本文の順に並べる。行頭の番号は付けない。
"""
import argparse
import re
import sys

from bs4 import BeautifulSoup, NavigableString

BLOCK = {"p", "li", "dt", "dd", "figcaption", "summary", "blockquote", "caption"}
SKIP = {"script", "style", "noscript", "template", "svg"}


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def inline(el):
    parts = []
    for c in el.descendants:
        if isinstance(c, NavigableString):
            if not any(p.name in SKIP for p in c.parents):
                parts.append(str(c))
        elif c.name == "img" and c.get("alt"):
            parts.append(f"[画像: {c['alt']}]")
        elif c.name == "br":
            parts.append(" ")
    return clean("".join(parts))


def walk(el, out):
    for c in el.children:
        if isinstance(c, NavigableString) or c.name in SKIP:
            if c.name == "svg":
                t = c.find("title")
                if t:
                    out.append(f"[図: {clean(t.get_text())}]")
            continue
        if re.fullmatch(r"h[1-6]", c.name):
            out.append("\n" + "#" * int(c.name[1]) + " " + inline(c))
        elif c.name == "table":
            for tr in c.find_all("tr"):
                out.append("| " + " | ".join(inline(td) for td in tr.find_all(["th", "td"])) + " |")
        elif c.name == "img":
            if c.get("alt"):
                out.append(f"[画像: {c['alt']}]")
        elif c.name in BLOCK and not c.find(["p", "ul", "ol", "table", "dl", re.compile(r"h[1-6]")]):
            t = inline(c)
            if t:
                out.append(("- " if c.name == "li" else "") + t)
        else:
            walk(c, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    for f in a.files:
        s = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
        desc = s.find("meta", attrs={"name": "description"})
        print(f"=== {f}")
        print(f"title: {clean(s.title.get_text()) if s.title else ''}")
        print(f"description: {desc.get('content', '') if desc else ''}")
        out = []
        walk(s.body if a.all or not s.find("main") else s.find("main"), out)
        text = "\n".join(out)
        print(re.sub(r"\n{3,}", "\n\n", text).strip() + "\n")


if __name__ == "__main__":
    sys.exit(main())
