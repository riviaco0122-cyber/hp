#!/usr/bin/env python3
"""css/style.css の「どのページでも使われていないルール」を見つけて消す（月1回のコードの点検で使う）。

使い方:
  python3 tools/css_prune.py            # 使われていないクラスと、それだけでできたルールの一覧（変更しない）
  python3 tools/css_prune.py --apply    # 一覧のルールを css/style.css から消す（先に python3 tools/build.py を済ませる）

「使われている」とみなすもの（消しすぎないよう、広めに残す）:
  - 生成した HTML（pages/・404.html）の class に出てくる
  - js/・tools/ のソース（記事データ・figures.py・build.py など）に、そのクラス名が文字として出てくる
  - ソースで組み立てて作るクラス（例: f'fig-points--{n}'、"thumb--" + size）の頭の部分が一致する
  - 「--」の付いた形（例: stats--1）で、元のクラス（stats）が使われている（記事で使える部品の型として残す）
  - :not() の中のクラスは、ルールが生きているかの判定に使わない（:is()・:where()・:has() の中も同じ）

消すもの: 中身が空のルール。同じ条件（@media）・同じセレクタ・同じ中身のルールが2つ以上あるときの、前のほう（後ろのほうが必ず勝つ）。
セレクタの一部が使われていないクラスを含む場合、その部分だけをセレクタの並びから外す。
すべてが使われていなければ、ルールごと消す（中身が空になった @media も消す）。
消したあとは、python3 tools/build.py で作り直し、site_check で見た目が変わっていないことを確かめる。
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, "css", "style.css")


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_usage():
    """使われているクラスの判定に使う、生成 HTML の class 一覧とソースの全文。"""
    html_classes = set()
    for f in glob.glob(os.path.join(ROOT, "pages", "**", "*.html"), recursive=True) + [os.path.join(ROOT, "404.html")]:
        for m in re.finditer(r'class="([^"]*)"', _read(f)):
            html_classes.update(m.group(1).split())
    srcs = glob.glob(os.path.join(ROOT, "js", "*.js"))
    srcs += [f for f in glob.glob(os.path.join(ROOT, "tools", "**", "*.py"), recursive=True) if not f.endswith("css_prune.py")]
    srcs += glob.glob(os.path.join(ROOT, "tools", "**", "*.js"), recursive=True)
    return html_classes, "\n".join(_read(f) for f in srcs)


def make_alive(html_classes, src):
    cache = {}

    def literal(c):
        return c in html_classes or re.search(r"(?<![\w-])" + re.escape(c) + r"(?![\w-])", src) is not None

    def dynamic(c):
        for m in re.finditer(r"--|__|-", c):
            pre = c[: m.end()]
            if re.search(r"(?<![\w-])" + re.escape(pre) + r"(\{|\"\s*\+|'\s*\+|\$\{)", src):
                return True
        return False

    def alive(c):
        if c not in cache:
            cache[c] = literal(c) or dynamic(c) or ("--" in c and literal(c.rsplit("--", 1)[0]))
        return cache[c]

    return alive


# ---------------------------------------------------------------- CSS を「ルール単位」に分ける（コメント・文字列を飛ばす）
def _skip(text, i):
    """コメント・文字列なら、その終わりの次の位置を返す。どちらでもなければ None。"""
    if text.startswith("/*", i):
        j = text.find("*/", i + 2)
        return len(text) if j < 0 else j + 2
    if text[i] in "\"'":
        q, j = text[i], i + 1
        while j < len(text) and text[j] != q:
            j += 2 if text[j] == "\\" else 1
        return j + 1
    return None


def _match_brace(text, i):
    """text[i] == '{' に対応する '}' の位置。"""
    depth = 0
    while i < len(text):
        s = _skip(text, i)
        if s is not None:
            i = s
            continue
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("波かっこの対応がとれません")


def parse_block(text, start, end):
    """[start, end) のルールの並びを返す。各要素は dict(kind, start, end, prelude, body_start, body_end)。"""
    items, i = [], start
    while i < end:
        s = _skip(text, i)
        if s is not None:
            i = s
            continue
        if text[i].isspace() or text[i] == ";":
            i += 1
            continue
        j = i
        while j < end and text[j] not in "{;":
            s = _skip(text, j)
            j = s if s is not None else j + 1
        if j >= end or text[j] == ";":  # @import / @charset など
            i = j + 1
            continue
        close = _match_brace(text, j)
        prelude = re.sub(r"/\*.*?\*/", "", text[i:j], flags=re.S).strip()
        if prelude.startswith("@"):
            kind = "group" if re.match(r"@(media|supports)\b", prelude) else "at"
        else:
            kind = "rule"
        items.append(dict(kind=kind, start=i, end=close + 1, prelude=prelude, body_start=j + 1, body_end=close))
        i = close + 1
    return items


def split_selectors(sel):
    parts, depth, cur = [], 0, ""
    for ch in sel:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return parts


def _strip_functional(sel):
    """:not() / :is() / :where() / :has() の中身を除く（中のクラスは「生きているか」の判定に使わない）。"""
    out, i = "", 0
    while i < len(sel):
        m = re.match(r":(not|is|where|has)\(", sel[i:])
        if m:
            depth, j = 1, i + len(m.group(0))
            while j < len(sel) and depth:
                depth += {"(": 1, ")": -1}.get(sel[j], 0)
                j += 1
            out += ":x"
            i = j
        else:
            out += sel[i]
            i += 1
    return out


def dead_classes_in(selector, alive):
    return [c for c in re.findall(r"\.([A-Za-z_][\w-]*)", _strip_functional(selector)) if not alive(c)]


# ---------------------------------------------------------------- 消す範囲を決める
def plan(text, alive):
    """(消す範囲のリスト, セレクタの書き換えのリスト, 報告用の行) を返す。"""
    removals, rewrites, report = [], [], []

    def walk(start, end, ctx):
        items = parse_block(text, start, end)
        kept = 0
        for it in items:
            if it["kind"] == "group":
                if walk(it["body_start"], it["body_end"], ctx + [it["prelude"]]) == 0:
                    removals.append((it["start"], it["end"]))
                else:
                    kept += 1
                continue
            if it["kind"] == "at":
                kept += 1
                continue
            if not re.sub(r"/\*.*?\*/", "", text[it["body_start"]:it["body_end"]], flags=re.S).strip():
                removals.append((it["start"], it["end"]))  # 中身が空のルール（効き目がない）
                report.append(f"{text.count(chr(10), 0, it['start']) + 1}: 空    {it['prelude'][:90]}")
                continue
            parts = split_selectors(it["prelude"])
            dead = [p for p in parts if dead_classes_in(p, alive)]
            line = text.count("\n", 0, it["start"]) + 1
            where = (" @ " + " / ".join(ctx)) if ctx else ""
            if len(dead) == len(parts):
                removals.append((it["start"], it["end"]))
                report.append(f"{line}: 削除  {it['prelude'][:90]}{where}")
            else:
                kept += 1
                if dead:
                    sel_end = it["body_start"] - 1
                    rewrites.append((it["start"], sel_end, ", ".join(p for p in parts if p not in dead)))
                    report.append(f"{line}: 一部  {', '.join(dead)[:90]}{where}")
        return kept

    walk(0, len(text), [])

    # 同じ条件（@media）・同じセレクタ・同じ中身のルールが2つ以上あれば、後ろの1つだけを残す（後ろが必ず勝つので、見た目は変わらない）
    seen = {}

    def walk_dup(start, end, ctx):
        for it in parse_block(text, start, end):
            if it["kind"] == "group":
                walk_dup(it["body_start"], it["body_end"], ctx + (it["prelude"],))
            elif it["kind"] == "rule":
                body = re.sub(r"\s+", " ", re.sub(r"/\*.*?\*/", "", text[it["body_start"]:it["body_end"]], flags=re.S)).strip()
                seen.setdefault((ctx, re.sub(r"\s+", " ", it["prelude"]), body), []).append(it)

    walk_dup(0, len(text), ())
    for (ctx, sel, _), its in seen.items():
        for it in its[:-1]:
            if not any(s <= it["start"] < e for s, e in removals):
                removals.append((it["start"], it["end"]))
                line = text.count("\n", 0, it["start"]) + 1
                report.append(f"{line}: 重複  {sel[:90]}" + ((" @ " + " / ".join(ctx)) if ctx else ""))
    return removals, rewrites, report


def apply_rewrites(text, rewrites):
    """セレクタの並びから、使われていない部分を外す。"""
    for s, e, new in sorted(rewrites, reverse=True):
        text = text[:s] + new + " " + text[e:]
    return text


def apply_removals(text, removals):
    """範囲を消す。もともと中身があって、消したあと空白だけになった行は、行ごと消す。"""
    mask = bytearray(len(text))
    for s, e in removals:
        mask[s:e] = b"\x01" * (e - s)
    out, pos = [], 0
    for ln in text.split("\n"):
        s, e = pos, pos + len(ln)
        pos = e + 1
        if not any(mask[s:e]):
            out.append(ln)
            continue
        rest = "".join(ch for ch, m in zip(ln, mask[s:e]) if not m)
        if rest.strip():
            out.append(rest.rstrip())
    return "\n".join(_drop_orphan_comments(out))


def _drop_blank_runs(lines, _):
    out = []
    for ln in lines:
        if ln.strip() == "" and out and out[-1].strip() == "":
            continue
        out.append(ln)
    return out


def _drop_orphan_comments(lines):
    """1行のコメントだけの行で、次の中身のある行がコメント・「}」・ファイルの終わりのものは、説明する相手がいないので消す。"""
    def is_comment(ln):
        s = ln.strip()
        return s.startswith("/*") and s.endswith("*/") and "*/" not in s[2:-2]

    changed = True
    while changed:
        changed = False
        for i, ln in enumerate(lines):
            if not is_comment(ln) or "=====" in ln:
                continue
            nxt = next((l2.strip() for l2 in lines[i + 1:] if l2.strip()), "")
            if nxt == "" or nxt.startswith("}") or nxt.startswith("/*"):
                del lines[i]
                changed = True
                break
    return _drop_blank_runs(lines, None)


def main():
    text = _read(CSS)
    alive = make_alive(*load_usage())
    removals, rewrites, report = plan(text, alive)
    print("\n".join(report))
    print(f"\n削除の対象: {len(removals)} 件（使われていない・重複）、{len(rewrites)} 件はセレクタの一部だけ外す")
    if "--apply" in sys.argv:
        new = apply_rewrites(text, rewrites)
        while True:  # 消したあとに中身が空になった @media も消えるまで繰り返す
            removals, _, _ = plan(new, alive)
            if not removals:
                break
            new = apply_removals(new, removals)
        with open(CSS, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"css/style.css: {text.count(chr(10))} 行 → {new.count(chr(10))} 行")


if __name__ == "__main__":
    main()
