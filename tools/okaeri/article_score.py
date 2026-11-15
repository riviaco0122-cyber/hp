# -*- coding: utf-8 -*-
"""Okaeri Japan の記事の機械採点（40点）とゲート判定。基準は tools/okaeri/playbook.md 4章。

使い方:
  python3 tools/okaeri/article_score.py kinmedai              # content.py の記事（id か slug）
  python3 tools/okaeri/article_score.py tools/okaeri/drafts/x.py  # 下書き（ARTICLE = {...} を書いたファイル）
  python3 tools/okaeri/article_score.py --all                 # content.py の全記事
  --json で結果を JSON で出す。

終了コード: 0 = ゲート違反なし／2 = ゲート違反あり（点数に関係なく不合格）
合格は、品質保証部の60点と合わせて90点以上（このツールだけでは決まらない）。
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C  # noqa: E402

# 誇大・観光パンフレット調、AI が書いたような語（1件 -2）
SOFT_NG = [
    "hidden gem", "must-see", "must see", "must-visit", "breathtaking", "nestled", "off the beaten path", "off the beaten track",
    "paradise", "unforgettable", "once-in-a-lifetime", "once in a lifetime", "best-kept secret", "best kept secret",
    "delve", "tapestry", "testament to", "fast-paced", "it's worth noting", "it’s worth noting", "embark on", "a myriad of",
    "navigate the complexities", "unlock the", "elevate your", "seamless", "look no further", "in conclusion",
]
# 保証・断定（ゲート）
HARD_NG = [
    "guaranteed", "guarantee you", "risk-free", "risk free", "you will definitely", "always profitable", "100% safe",
    "no visa needed for anyone", "anyone can buy", "never lose",
]
# 英国式と米国式の組（同じ記事で両方出たら1組 -1）
SPELL = [("metre", "meter"), ("colour", "color"), ("centre", "center"), ("travelling", "traveling"), ("travelled", "traveled"),
         ("organise", "organize"), ("realise", "realize"), ("neighbour", "neighbor"), ("favourite", "favorite"),
         ("kilometre", "kilometer"), ("programme", "program"), ("cheque", "check"), ("flavour", "flavor"),
         ("harbour", "harbor"), ("theatre", "theater"), ("apologise", "apologize"), ("recognise", "recognize")]
OFFICIAL = ("go.jp", "japan.travel", "lg.jp", "pref.", "city.", "town.", ".gov", "jnto", "mlit", "moj", "mofa", "e-stat", "stat.go")
Q_START = ("what", "how", "why", "when", "where", "which", "who", "can", "is", "are", "do", "does", "should", "will")


def load(arg):
    if arg.endswith(".py") and os.path.exists(arg):
        spec = importlib.util.spec_from_file_location("draft", arg)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        C.SOURCES.update(getattr(m, "SOURCES_NEW", {}))  # 下書きで足す出典
        return m.ARTICLE
    for a in C.ARTICLES:
        if arg in (a["id"], a["slug"]):
            return a
    raise SystemExit(f"記事が見つからない: {arg}")


def plain(s):
    """本文の記法とタグを外して、読み手が読む文にする"""
    s = re.sub(r"\[\[ed:.+?\]\]", " ", s, flags=re.S)
    s = re.sub(r"\[\[img:[^\]]+\]\]", " ", s)
    s = re.sub(r" ?\[\[s:[\w,]+\]\]", "", s)
    s = re.sub(r"\[\[a:(\w+)\]\]", lambda m: C.SOURCES.get(m.group(1), ("", m.group(1)))[1], s)
    s = re.sub(r"\[\[l:[\w-]+\|([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"<(h[1-6]|p|li|td|th|tr|div|section|aside|figure|figcaption|table|ul|ol)\b[^>]*>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[ \t]+", " ", s)


def sentences(text):
    out = []
    for block in text.split("\n"):
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z“\"(])", block.strip()):
            words = re.findall(r"[A-Za-z0-9’'¥%-]+", sent)
            if len(words) >= 3:
                out.append(len(words))
    return out


IMPERATIVE = ("check", "visit", "ask", "write", "take", "find", "book", "bring", "try", "go", "plan", "order", "walk", "look",
              "buy", "get", "make", "use", "avoid", "remember", "consider", "read", "work", "cook", "notice", "stay", "talk", "shop")
CONTRACTION = re.compile(r"\b\w+(?:’|')(?:s|re|ll|ve|d|t|m)\b", re.I)


def tone(text):
    """説明書っぽさの目安（playbook 3-1）。点数ではなくメモ"""
    sents = []
    for block in text.split("\n"):
        sents += [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z“\"(])", block.strip()) if len(re.findall(r"[A-Za-z]+", x)) >= 1]
    if not sents:
        return []
    first = [re.sub(r"^[^A-Za-z]+", "", x).split(" ")[0].lower() for x in sents]
    imp = sum(1 for w in first if w in IMPERATIVE)
    frag = sum(1 for x in sents if 1 <= len(re.findall(r"[A-Za-z0-9’']+", x)) <= 4)
    contr = len(CONTRACTION.findall(text))
    out = [f"トーンの目安: 命令文で始まる文 {imp}/{len(sents)}（{imp / len(sents):.0%}。15%を超えると説明書っぽい）、"
           f"4語以下の短い文 {frag}、短縮形 {contr}個（0〜2個だと硬い）"]
    return out


def score(a):
    res, gates, notes = [], [], []
    body = a["body"]
    faq_text = " ".join(q + " " + x for q, x in a.get("faq", []))
    text = plain(body + "\n" + faq_text + "\n" + a.get("dek", "") + "\n" + "\n".join(a.get("points", [])))
    low = text.lower()

    def add(name, got, full, why=""):
        res.append({"項目": name, "点": got, "満点": full, "メモ": why})

    t = a.get("seo_title", "")
    add("title の長さ", 2 if len(t) <= 60 else 0, 2, f"{len(t)}字")
    kw = (a.get("keywords") or [("",)])[0][0].lower()
    pos = t.lower().find(kw) if kw else -1
    add("主な検索語の位置", 3 if 0 <= pos <= len(t) / 2 else (1 if pos > 0 else 0), 3, f"「{kw}」の位置 {pos}")
    d = a.get("description", "")
    add("description", 3 if 120 <= len(d) <= 160 else (1 if 100 <= len(d) <= 175 else 0), 3, f"{len(d)}字")
    n = len(a.get("points", []))
    add("In short（points）", 4 if 3 <= n <= 5 else 0, 4, f"{n}項目")
    h2 = [plain(h).strip() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", body, flags=re.S)]
    add("h2 の数", 2 if 4 <= len(h2) <= 8 else 0, 2, f"{len(h2)}個")
    qs = [h for h in h2 if h.endswith("?") or h.lower().split(" ")[0] in Q_START or ":" in h]
    rate = len(qs) / len(h2) if h2 else 0
    add("h2 の形", 2 if rate >= 0.6 else (1 if rate >= 0.4 else 0), 2, f"疑問・結論の形 {len(qs)}/{len(h2)}")
    nf = len(a.get("faq", []))
    add("FAQ", 4 if nf >= 3 else (2 if nf == 2 else 0), 4, f"{nf}問")
    keys = set(a.get("sources", []))
    for m in re.findall(r"\[\[s:([\w,]+)\]\]", body + faq_text):
        keys.update(m.split(","))
    keys = [k for k in keys if k in C.SOURCES]
    official = [k for k in keys if any(o in C.SOURCES[k][0] for o in OFFICIAL)]
    sp = (3 if len(keys) >= 3 else len(keys)) + (2 if official else 0)
    add("出典", sp, 5, f"{len(keys)}件（公的機関 {len(official)}件: {', '.join(official) or 'なし'}）")
    links = re.findall(r"\[\[l:([\w-]+)\|", body)
    add("内部リンク", 2 if len(links) >= 2 else len(links), 2, f"{len(links)}本")
    rel = a.get("related", [])
    add("関連記事", 2 if len(rel) >= 2 else len(rel), 2, f"{len(rel)}件")
    ss = sentences(text)
    avg = sum(ss) / len(ss) if ss else 0
    add("1文の平均", 2 if avg <= 20 else (1 if avg <= 24 else 0), 2, f"{avg:.1f}語（{len(ss)}文）")
    long_rate = sum(1 for x in ss if x > 30) / len(ss) if ss else 0
    add("長い文の割合", 2 if long_rate <= 0.05 else (1 if long_rate <= 0.1 else 0), 2, f"30語超 {long_rate:.0%}")
    hits = [w for w in SOFT_NG if w in low]
    add("誇大・AI っぽい語", max(0, 4 - 2 * len(hits)), 4, ", ".join(hits) or "なし")
    mixed = [f"{uk}/{us}" for uk, us in SPELL if re.search(rf"\b{uk}", low) and re.search(rf"\b{us}s?\b", low)]
    add("綴りの統一", max(0, 3 - len(mixed)), 3, ", ".join(mixed) or "混在なし")

    hard = [w for w in HARD_NG if w in low]
    if hard:
        gates.append(f"保証・断定の表現: {', '.join(hard)}")
    ja = a.get("ja")
    if not isinstance(ja, dict) or not ja.get("body") or not ja.get("faq"):
        gates.append("日本語レビュー版（ja）がない、または本文・FAQ が欠けている")
    elif len(ja.get("faq", [])) != nf:
        notes.append(f"日本語版の FAQ の数（{len(ja['faq'])}）が英語版（{nf}）と違う")
    unknown = sorted({k for m in re.findall(r"\[\[s:([\w,]+)\]\]", body + faq_text) for k in m.split(",")} - set(C.SOURCES))
    if unknown:
        gates.append(f"SOURCES にない出典キー: {', '.join(unknown)}")
    notes += tone(plain(re.sub(r"<table.*?</table>", " ", body, flags=re.S) + "\n" + faq_text + "\n" + a.get("dek", "")))  # 表のマスは文として数えない
    eds = len(re.findall(r"\[\[ed:", body + faq_text))
    if eds:
        notes.append(f"黄色い枠（未確認の箇所）が {eds} か所（公開前に人が埋める）")
    total = sum(r["点"] for r in res)
    return {"id": a.get("id"), "機械採点": total, "満点": 40, "内訳": res, "ゲート違反": gates, "メモ": notes}


def show(r):
    print(f"\n# {r['id']}  機械採点 {r['機械採点']}/40")
    for x in r["内訳"]:
        mark = "" if x["点"] == x["満点"] else "  ←"
        print(f"  {x['項目']:<12} {x['点']}/{x['満点']}  {x['メモ']}{mark}")
    for g in r["ゲート違反"]:
        print(f"  [ゲート違反] {g}")
    for m in r["メモ"]:
        print(f"  [メモ] {m}")


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    targets = [a["id"] for a in C.ARTICLES] if "--all" in sys.argv else args
    if not targets:
        raise SystemExit(__doc__)
    results = [score(load(t)) for t in targets]
    if "--json" in sys.argv:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for r in results:
            show(r)
    sys.exit(2 if any(r["ゲート違反"] for r in results) else 0)


if __name__ == "__main__":
    main()
