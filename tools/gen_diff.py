#!/usr/bin/env python3
"""生成物（pages/・404.html・js/media-index.js・seo/）の変化を、短く要約して出す。

生成物は .gitattributes で -diff にしてあり、git diff では本文が出ない（1行が長く、
1文字の変更でも大量の差分になって AI のトークンを食うため）。中身の変化はこれで見る。

使い方:
  python3 tools/gen_diff.py                 # 作業ツリー（未コミットを含む）と HEAD を比べる
  python3 tools/gen_diff.py origin/<本番>   # 本番ブランチと比べる（PR の確認用）
  python3 tools/gen_diff.py <基準> --files pages/media/x.html   # ファイルを絞る
  python3 tools/gen_diff.py --max 40        # 1つの変化パターンに出す最大文字数など（既定 160）

出力: 同じ変化（変更前→変更後の組）が何ファイルで起きたかをまとめて、多い順に並べる。
例えば CSS の版番号（?v=）だけが変わったなら、「?v=… → ?v=…」が全ファイルの1パターンだけ出る。
"""
import argparse
import difflib
import re
import subprocess
from collections import defaultdict

GEN = ["pages", "404.html", "js/media-index.js", "seo"]
TOKEN = re.compile(r"<[^>]*>|[^<]+")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout


def changed_files(base, only):
    paths = only or GEN
    out = git("diff", "--name-status", base, "--", *paths)
    out += "".join(f"A\t{p}\n" for p in git("ls-files", "--others", "--exclude-standard", "--", *paths).split())
    rows = []
    for line in out.splitlines():
        st, *names = line.split("\t")
        rows.append((st[0], names[-1]))
    return rows


def tokens(text):
    # タグと文字の塊に分ける。長い文字の塊は句点・空白でさらに分け、差分を細かくする
    res = []
    for t in TOKEN.findall(text):
        if t.startswith("<"):
            res.extend(re.findall(r'[^\s"]+|"|\s+', t) if len(t) > 200 else [t])
        else:
            res.extend(re.findall(r"[^。、\s]+[。、]?|\s+", t) or [t])
    return res


def short(s, n):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n // 2] + " … " + s[-n // 2:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", nargs="?", default="HEAD")
    ap.add_argument("--files", nargs="*")
    ap.add_argument("--max", type=int, default=160, help="1つの変化に出す最大文字数")
    ap.add_argument("--top", type=int, default=40, help="出す変化パターンの数")
    a = ap.parse_args()

    rows = changed_files(a.base, a.files)
    if not rows:
        print("生成物の変化なし")
        return
    patterns = defaultdict(set)
    added, deleted, spaces = [], [], set()
    for st, path in rows:
        if st == "A":
            added.append(path)
            continue
        if st == "D":
            deleted.append(path)
            continue
        old = git("show", f"{a.base}:{path}")
        try:
            new = open(path, encoding="utf-8").read()
        except FileNotFoundError:
            deleted.append(path)
            continue
        ot, nt = tokens(old), tokens(new)
        sm = difflib.SequenceMatcher(None, ot, nt, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            before = short("".join(ot[i1:i2]), a.max)
            after = short("".join(nt[j1:j2]), a.max)
            if before == after:  # 空白・改行だけの変化
                spaces.add(path)
                continue
            # 版番号などの数字・英数字のハッシュは、まとめるときに同じものとみなす
            key = (re.sub(r"[0-9a-f]{6,}", "#", before), re.sub(r"[0-9a-f]{6,}", "#", after))
            patterns[key].add(path)

    print(f"生成物の変化: {len(rows)} ファイル（基準 {a.base}）")
    if added:
        print(f"- 新しく増えた: {', '.join(added)}")
    if deleted:
        print(f"- 消えた: {', '.join(deleted)}")
    if spaces:
        print(f"- 空白・改行だけの変化があった: {len(spaces)} ファイル")
    items = sorted(patterns.items(), key=lambda kv: -len(kv[1]))
    print(f"- 変化のパターン: {len(items)} 種類（多い順。# は英数字のハッシュ）\n")
    for (before, after), files in items[: a.top]:
        where = ", ".join(sorted(files)[:3]) + (f" ほか{len(files) - 3}件" if len(files) > 3 else "")
        note = "（英数字のハッシュ・版番号だけの変化）" if before == after else ""
        print(f"[{len(files)}ファイル] {where}{note}")
        print(f"  前: {before or '（なし）'}")
        print(f"  後: {after or '（なし）'}")
    if len(items) > a.top:
        print(f"\n…ほか {len(items) - a.top} パターン（--top で増やせる。--files でファイルを絞れる）")


if __name__ == "__main__":
    main()
