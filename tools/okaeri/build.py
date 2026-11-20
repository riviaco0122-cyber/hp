#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Noki のサイトを作る。

  python3 tools/okaeri/build.py     本番用の okaeri/（https://rivia-co.com/okaeri）と、試作の tools/okaeri/preview/ を作る

記事は tools/okaeri/content.py、設定は tools/okaeri/site.json。okaeri/ の HTML は直接書き換えない。
アキヤド（tools/build.py）とは別に動く。sitemap は <公開フォルダ>/sitemap.xml（いまは noki/sitemap.xml）に出し、robots.txt から案内する。
"""
import html as htmllib
import json
import os
import re
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402
import review_ja as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # リポジトリの直下
CFG = json.load(open(os.path.join(HERE, "site.json"), encoding="utf-8"))
SITE = CFG["origin"].rstrip("/")                        # https://rivia-co.com
PRE = CFG["prefix"].rstrip("/")                         # /noki
DIST = os.path.join(ROOT, PRE.strip("/"))               # 公開フォルダ（URL と同じ場所に置く）
PREVIEW = os.path.join(HERE, "preview")                 # 試作（.gitignore 済み。公開されない）
NAME = CFG["name"]
CSS = open(os.path.join(HERE, "site.css"), encoding="utf-8").read()
WEBSITE_ID = SITE + "/#website"                         # サイト名の宣言はドメインのトップだけ（アキヤド側）
ORG_ID = SITE + "/about.html#organization"              # 会社（アキヤド側の about.html で定義）
TODAY = date.today().isoformat()
TOPIC_INDEX_MIN = 3  # テーマ別の一覧ページを検索に載せる（index）最少の記事数。それ未満は noindex,follow でメニューからだけ使う

FONTS_EN = "https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap"  # 見出し=明朝（Shippori Mincho）・UI=Zen Kaku Gothic New・本文=Source Serif 4
FONTS_ALL = "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Shippori+Mincho:wght@700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap"
# ロゴのツバメ（右を向いた、丸い体のツバメ。笑って細めた目・白いお腹・頬の赤・長い燕尾。2026-11-16 かわいく描き直し）。ヘッダー・ファビコン（SVG）とロゴ・OGP（PNG）は、この1つの形から作る。
# 色: ink=文字色 / paper=背景色（白目・お腹） / red=のど。パスは絶対座標の M・L・C・Z だけで書く（PNG 用に折れ線へ直すため）。
MARK_SHAPES = [
    ("ink", "M19.25 33C13.25 30 8.25 27 3.25 23C7.25 29 10.25 33 12.25 36.5C9.25 40 6.25 44 3.75 49C9.25 46 14.25 43 20.25 40.5Z"),  # 燕尾（長く細い）
    ("ink", "M55.15 31.01C56.1 40.08 48.41 48.31 37.97 49.41C27.54 50.51 18.31 44.05 17.35 34.99C16.4 25.92 24.09 17.69 34.53 16.59C44.96 15.49 54.19 21.95 55.15 31.01Z"),  # 体（丸い）
    ("ink", "M26.25 24C22.25 18 16.25 14.5 8.25 14C12.25 19.5 17.25 24 24.25 28Z"),  # 翼（後ろへ流す）
    ("paper", "M52.65 39.35C53.17 43.63 47.6 47.83 40.2 48.74C32.8 49.65 26.38 46.92 25.85 42.65C25.33 38.37 30.9 34.17 38.3 33.26C45.7 32.35 52.12 35.08 52.65 39.35Z"),  # お腹
    ("ink", "M54.25 28L60.75 30.5L54.25 33Z"),  # くちばし
    ("red", "M53.35 34.69C53.72 36.41 52.09 38.22 49.72 38.73C47.34 39.24 45.11 38.24 44.75 36.51C44.38 34.79 46.01 32.98 48.38 32.47C50.76 31.96 52.99 32.96 53.35 34.69Z"),  # 頬（のどの赤）
    ("paper", "M41.75 28.3C41.75 26.09 43.54 24.3 45.75 24.3C47.96 24.3 49.75 26.09 49.75 28.3L47.85 28.3C47.85 27.37 46.91 26.62 45.75 26.62C44.59 26.62 43.65 27.37 43.65 28.3Z"),  # 目（笑って細めた目）
]


def mark_svg(colors=None, attrs='class="mark" aria-hidden="true"'):
    """ロゴの SVG。colors を渡すと色を固定する（ファビコン用）"""
    c = colors or {"ink": "var(--mark-body,currentColor)", "paper": "var(--mark-light,var(--paper))", "red": "var(--shu)"}  # ダークモードでは site.css の --mark-body・--mark-light で体を明るい青、お腹と目を白にする（反転すると口を開けた顔に見えるため）
    parts = [f'<circle cx="{v[0]}" cy="{v[1]}" r="{v[2]}" fill="{c[k]}"/>' if isinstance(v, tuple) else f'<path fill="{c[k]}" d="{v}"/>'
             for k, v in MARK_SHAPES]
    return f'<svg {attrs} viewBox="0 0 64 64">{"".join(parts)}</svg>'


def mark_polys(steps=12):
    """ロゴの形を (色, 折れ線の点) と (色, 円) に直す（PNG 用）"""
    out = []
    for k, v in MARK_SHAPES:
        if isinstance(v, tuple):
            out.append((k, v))
            continue
        nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", v)]
        cmds = re.findall(r"[MLCZ]", v)
        pts, n = [], 0
        for cmd in cmds:
            if cmd in "ML":
                pts.append((nums[n], nums[n + 1])); n += 2
            elif cmd == "C":
                (x0, y0), (x1, y1, x2, y2, x3, y3) = pts[-1], nums[n:n + 6]; n += 6
                for t in (i / steps for i in range(1, steps + 1)):
                    u = 1 - t
                    pts.append((u**3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * x3, u**3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * y3))
        out.append((k, pts))
    return out


MARK = mark_svg()

esc = htmllib.escape
ART = {a["id"]: a for a in C.ARTICLES}
PUBLISHED = [a for a in C.ARTICLES if a["published"] <= TODAY]

# ページID → 本番のパス
# アキヤドと同じく .html の URL（このドメインは末尾スラッシュなし・拡張子ありで運用している）
PATHS = {"home": PRE, "guides": PRE + "/guides.html", "izu": PRE + "/izu-peninsula.html", "about": PRE + "/about.html"}
for a in C.ARTICLES:
    PATHS[a["id"]] = f"{PRE}/guides/{a['slug']}.html"
def hub_articles(k):
    """一覧に載る記事。段階（stay/live/own）はその段階の記事、場所（places）は場所のある記事"""
    return [a for a in PUBLISHED if (a.get("place") if k == "places" else a["topic"] == k)]


# 入口（テーマ別の一覧ページ・メニュー・トップの道しるべ）は、記事が1本以上あるテーマだけ出す。
# 中身のない入口（Guides coming soon）は作りかけのサイトに見えるため（2026-11-16）
HUB_TOPICS = [k for k in C.TOPICS if hub_articles(k)]
OPEN_PLANS = [k for k in C.PLANS if k in HUB_TOPICS]


def hub_also(k):
    return [a for a in PUBLISHED if k in a.get("also", [])]


INDEXED_TOPICS = [k for k in C.TOPICS if len(hub_articles(k)) >= TOPIC_INDEX_MIN]
for k in HUB_TOPICS:
    PATHS["topic-" + k] = f"{PRE}/{k}.html"

ednotes = []  # (ページID, 文章) 残っている黄色い枠


def fmt_date(iso):
    y, m, d = iso.split("-")
    months = "January February March April May June July August September October November December".split()
    return f"{int(d)} {months[int(m) - 1]} {y}"


def fmt_date_ja(iso):
    y, m, d = iso.split("-")
    return f"{y}年{int(m)}月{int(d)}日"


class Ctx:
    """mode: 'dist'（本番・実URL）か 'preview'（試作・#ページID）"""

    def __init__(self, mode, page_id, lang="en"):
        self.mode, self.page_id, self.lang = mode, page_id, lang
        self.photos = []  # このページで使った写真（ページ下のクレジット用）
        self.cites = []   # 本文で出典を挙げた順（番号 = この順。ページ下の出典一覧も同じ順）

    def src_id(self, n):
        """出典一覧の各行の id。試作は全ページが1ファイルなので、ページIDを付けて重ならないようにする"""
        return f"src-{n}" if self.mode == "dist" else f"{self.page_id}-src-{n}"

    def sources(self, keys, heading):
        """ページ下の出典一覧。本文で番号を振った順に並べ、本文で挙げていない出典はその後ろに続ける"""
        order = self.cites + [k for k in keys if k not in self.cites]
        items = "".join(f'<li id="{self.src_id(i)}"><a href="{esc(C.SOURCES[k][0])}" rel="noopener">{esc(C.SOURCES[k][3])}</a></li>' for i, k in enumerate(order, 1))
        return f'<section class="sources"><h2>{heading}</h2><ol>{items}</ol></section>'

    def href(self, pid, frag=""):
        if self.mode == "preview":
            return "#" + pid
        base = PATHS.get(pid.replace("ja-", ""), PRE)
        return base + (("#" + frag) if frag else "")

    def expand(self, s):
        ja = self.lang == "ja"

        def src(m):
            # 本文の出典は小さな番号にして、名前はページ下の出典一覧にまとめる（名前が文中に続くと読む流れが止まるため。2026-11-16）
            nums = []
            for k in m.group(1).split(","):
                if k not in self.cites:
                    self.cites.append(k)
                nums.append((self.cites.index(k) + 1, k))
            links = [f'<a href="#{self.src_id(n)}" title="{esc(C.SOURCES[k][2 if ja else 1])}" aria-label="{"出典" if ja else "Source"} {n}">{n}</a>' for n, k in sorted(nums)]  # 1か所に並ぶ番号は小さい順
            return '<sup class="cite">' + ",".join(links) + '</sup>'

        def bare(m):
            k = m.group(1)
            return f'<a href="{esc(C.SOURCES[k][0])}" rel="noopener">{esc(C.SOURCES[k][2 if ja else 1])}</a>'

        def link(m):
            return f'<a href="{self.href(m.group(1))}">{m.group(2)}</a>'

        def ed(m):
            ednotes.append((self.page_id, m.group(1)))
            label = "運営者の一次情報で埋める箇所" if ja else "Editor’s note · remove before publishing"
            return f'<aside class="ednote"><p class="ednote__label">{label}</p><p>{m.group(1)}</p></aside>'

        s = re.sub(r"\s*\[\[s:([\w,]+)\]\]", src, s)
        s = re.sub(r"\[\[a:(\w+)\]\]", bare, s)
        s = re.sub(r"\[\[l:([\w-]+)\|([^\]]+)\]\]", link, s)
        s = re.sub(r"\[\[img:([\w-]+)\|([^|\]]+)\|([^\]]*)\]\]", lambda m: img(self, m.group(1), m.group(2), m.group(3)), s)
        s = re.sub(r"\[\[ed:(.+?)\]\]", ed, s, flags=re.S)
        s = re.sub(r"(\d) (m²|m|km|min)\b", "\\1&nbsp;\\2", s)  # 数字と単位を行末で切り離さない（例: 470 m）
        return stack_tables(s)


def stack_tables(s):
    """文章の表（class="free"）で3列以上のものは、スマホ幅で行ごとのカードに組み替える（site.css の table.stack）。
    セルに列名（data-label）を付けて、カードの中でも何の列か分かるようにする。"""
    def one(m):
        heads = [strip_tags(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", m.group(2), flags=re.S)]
        if len(heads) < 3:
            return m.group(0)

        def row(r):
            cells = iter(heads)
            return re.sub(r"<td(?=[\s>])", lambda c: f'<td data-label="{esc(next(cells, ""))}"', r.group(0))
        body = re.sub(r"<tr>.*?</tr>", row, m.group(3), flags=re.S)
        return f'<table class="{m.group(1)} stack">{m.group(2)}{body}</table>'
    return re.sub(r'<table class="(free)">(.*?</thead>)(.*?)</table>', one, s, flags=re.S)


def _photo_files(name):
    """photos/<名前>-<幅>.webp の一覧 [(幅, 高さ, ファイル名)]"""
    from PIL import Image
    out = []
    for f in sorted(os.listdir(os.path.join(HERE, "photos"))):
        if f.startswith(name + "-") and f.endswith(".webp") and f[len(name) + 1:-5].isdigit():
            w, h = Image.open(os.path.join(HERE, "photos", f)).size
            out.append((w, h, f))
    if not out:
        raise SystemExit(f"写真がない: photos/{name}-*.webp")
    return sorted(out)


def photo_src(ctx, name, want=1200):
    files = _photo_files(name)
    base = "assets/photos/" if ctx.mode == "preview" else PRE + "/assets/photos/"
    pick = min(files, key=lambda x: abs(x[0] - want))
    return base, files, pick


def img(ctx, name, alt, caption="", eager=False, cls="photo", sizes="(max-width: 44rem) 100vw, 44rem", want=1200, bare=False):
    base, files, pick = photo_src(ctx, name, want)
    if name not in ctx.photos:
        ctx.photos.append(name)
    srcset = ", ".join(f"{base}{f} {w}w" for w, h, f in files)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    tag = (f'<img src="{base}{pick[2]}" srcset="{srcset}" sizes="{sizes}" width="{pick[0]}" height="{pick[1]}" alt="{esc(alt)}" {load}>')
    if bare:
        return tag
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="{cls}">{tag}{cap}</figure>'


def strip_tags(s):
    s = re.sub(r" ?\[\[s:[\w,]+\]\]", "", s)
    s = re.sub(r"\[\[a:(\w+)\]\]", lambda m: C.SOURCES[m.group(1)][1], s)
    s = re.sub(r"\[\[l:[\w-]+\|([^\]]+)\]\]", r"\1", s)
    return htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def crumbs(ctx, trail):
    """trail: [(名前, ページID or None)]"""
    items = []
    for name, pid in trail:
        items.append(f'<li><a href="{ctx.href(pid)}">{esc(name)}</a></li>' if pid else f'<li aria-current="page">{esc(name)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def read_min(a):
    words = len(re.sub(r"<[^>]+>", " ", a["body"] + " ".join(q + " " + x for q, x in a["faq"])).split())
    return max(3, round(words / 220))


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def topic_chip(ctx, k):
    if k not in HUB_TOPICS:
        return ""
    return f'<a class="chip t-{k}" href="{ctx.href("topic-" + k)}">{esc(C.TOPICS[k]["name"])}</a>'


def article_chips(ctx, a):
    out = topic_chip(ctx, a["topic"])
    if a.get("place"):
        pl = C.PLACES[a["place"]]
        out += f'<a class="chip t-places" href="{ctx.href(pl["page"])}">{esc(pl["name"])}</a>'
    return out


def card(ctx, a, size="m"):
    name, alt, _ = a["photo"]
    sizes = "(max-width: 40rem) 100vw, 40rem" if size == "l" else "(max-width: 40rem) 100vw, 22rem"
    return (f'<article class="acard acard--{size}"><a class="acard__img" href="{ctx.href(a["id"])}" tabindex="-1" aria-hidden="true">'
            f'{img(ctx, name, alt, bare=True, sizes=sizes, want=1200 if size == "l" else 640)}</a>'
            f'<div class="acard__body"><p class="acard__meta">{topic_chip(ctx, a["topic"])}<span>{read_min(a)} min read</span></p>'
            f'<h3><a href="{ctx.href(a["id"])}">{a["h1"]}</a></h3><p>{a["card"]}</p></div></article>')


def cta(ctx, photo=True):
    """記事の下の自社の家の案内。同じ写真は1ページに1回まで（本文に NODE Shimoda の写真がある記事では photo=False）"""
    facts = "".join(f"<li>{esc(x)}</li>" for x in C.NODE_FACTS[:4])
    pic = img(ctx, "node-shimoda", "Living room of NODE Shimoda with a sofa and sliding paper screens", bare=True, sizes="(max-width: 44rem) 100vw, 22rem", want=640) if photo else ""
    return (f'<aside class="stay-cta" data-nosnippet>{pic}'
            '<div class="stay-cta__body"><p class="kicker">Stay with us</p><h2>Try the town for a week or a month</h2>'
            '<p>NODE Shimoda is our home in the old town of Shimoda, set up for long stays.</p>'
            f'<ul class="ticks">{facts}</ul>'
            f'<div class="btns"><a class="btn btn--solid" href="{C.BOOK_URL}" rel="noopener">See NODE Shimoda on Airbnb</a></div></div></aside>')


# ------------------------------------------------------------------ 各ページの本文
def page_home(ctx):
    """トップ: キャッチコピー → 記事 → 自社の家（1回）。中身のない入口・まだ開いていない町・つながっていないメール登録は出さない（2026-11-16）"""
    feat = PUBLISHED[1] if len(PUBLISHED) > 1 else PUBLISHED[0]
    rest = [a for a in PUBLISHED if a is not feat]
    facts = "".join(f"<li>{esc(x)}</li>" for x in C.NODE_FACTS)
    kicker = " · ".join(C.TOPICS[k]["name"] for k in OPEN_PLANS)
    return f"""
<section class="hero">
{img(ctx, "coastal-village", "Wooden houses along a calm bay below green wooded hills", bare=True, eager=True, sizes="100vw", want=1600)}
<div class="hero__shade"></div>
<div class="wrap wide hero__inner">
<p class="hero__kicker">{esc(kicker)}</p>
<h1>Small-town Japan, beyond a quick visit.</h1>
<p class="hero__lead">Straight answers about longer trips, living here part of the year and buying an old house outside the big cities, from the people who run a place to stay in Shimoda.</p>
<div class="btns"><a class="btn btn--light" href="#start">Read the guides</a></div>
</div>
</section>

<section class="band wrap wide" id="start" aria-labelledby="latest-h">
<div class="band__head"><div><p class="kicker">Guides</p><h2 id="latest-h">Start here</h2></div><a class="more" href="{ctx.href('guides')}">All guides →</a></div>
<div class="feat">{card(ctx, feat, "l")}<div class="feat__side">{"".join(card(ctx, a, "s") for a in rest)}</div></div>
</section>

<section class="homes" id="homes" aria-labelledby="homes-h">
<div class="wrap wide homes__grid">
<div class="homes__photo">{img(ctx, "node-shimoda", "Living room with a grey sofa, low table and sliding paper screens", "NODE Shimoda, in the old town of Shimoda on the Izu Peninsula.", sizes="(max-width: 52rem) 100vw, 30rem")}</div>
<div class="homes__body">
<p class="kicker">Our homes</p>
<h2 id="homes-h">A place to come back to</h2>
<p>We renovate older places in small towns and open them to guests who stay a while. Our first is NODE Shimoda, a renovated apartment in the old town of Shimoda, sleeping up to four.</p>
<ul class="ticks">{facts}</ul>
<div class="btns"><a class="btn btn--light" href="{C.BOOK_URL}" rel="noopener">See NODE Shimoda on Airbnb</a><a class="btn btn--line" href="{ctx.href('about')}">How we write our guides</a></div>
</div>
</div>
</section>"""


def page_guides(ctx):
    out = [f'<section class="pagehead"><div class="wrap wide">{crumbs(ctx, [(NAME, "home"), ("Guides", None)])}'
           f'<p class="kicker">Guides</p><h1>{C.GUIDES["h1"]}</h1><p class="dek">{C.GUIDES["dek"]}</p>'
           '<nav class="chips" aria-label="Topics">' + "".join(topic_chip(ctx, k) for k in HUB_TOPICS) + '</nav></div></section>'
           '<div class="wrap wide">']
    for k in C.PLANS:
        t = C.TOPICS[k]
        arts = hub_articles(k)
        if not arts:
            continue
        out.append(f'<section class="band"><div class="band__head"><div><h2>{esc(t["name"])}</h2><p class="band__sub">{esc(t["description"])}</p></div>'
                   f'<a class="more" href="{ctx.href("topic-" + k)}">More →</a></div>'
                   f'<div class="grid3">{"".join(card(ctx, a) for a in arts)}</div></section>')
    out.append(cta(ctx) + "</div>")
    return "".join(out)


def page_topic(ctx, k):
    t = C.TOPICS[k]
    arts = hub_articles(k)
    also = [a for a in hub_also(k) if a not in arts]
    coming = "".join(f"<li>{esc(x)}</li>" for x in t.get("coming", []))
    others = "".join(topic_chip(ctx, o) for o in HUB_TOPICS if o != k)
    if t["kind"] == "place":
        regions = "".join(f'<li><a href="{ctx.href(p["page"])}">{esc(p["name"])}</a></li>' for p in C.PLACES.values())
        first = f'<section class="band"><h2>Regions</h2><ul class="coming">{regions}</ul></section>'
    else:
        first = ""
    main = (f'<section class="band"><div class="band__head"><h2>{plural(len(arts), "guide") if arts else "Guides for this plan are on the way"}</h2></div>'
            + (f'<div class="grid3">{"".join(card(ctx, a) for a in arts)}</div>' if arts else "") + '</section>')
    also_html = (f'<section class="band"><div class="band__head"><h2>Also useful</h2></div><p class="band__sub">Filed under another plan, but they cover part of this one.</p>'
                 f'<div class="grid3">{"".join(card(ctx, a) for a in also)}</div></section>') if also else ""
    return (f'<section class="topichead t-{k}">{img(ctx, t["photo"], t["photo_alt"], bare=True, eager=True, sizes="100vw", want=1600)}<div class="hero__shade"></div><span class="topichead__kanji" lang="ja" aria-hidden="true">{t["kanji"]}</span>'
            f'<div class="wrap wide topichead__inner">{crumbs(ctx, [(NAME, "home"), ("Guides", "guides"), (t["name"], None)])}'
            f'<h1>{esc(t["name"])}</h1><p>{esc(t["intro"])}</p></div></section>'
            f'<div class="wrap wide">{first}{main}{also_html}'
            + (f'<section class="band"><h2>Coming next</h2><ul class="coming">{coming}</ul></section>' if coming else "")
            + f'<section class="band"><h2>Other ways in</h2><nav class="chips" aria-label="Other topics">{others}</nav></section>{cta(ctx)}</div>')


def page_izu(ctx):
    body = f"""
<h2>Where is the Izu Peninsula?</h2>
<p>The Izu Peninsula is in Shizuoka Prefecture, south-west of Tokyo. Atami, at its northern end, is about 80 minutes from Tokyo by limited express, and Shimoda, at the southern tip, is 2 hours 29 to 44 minutes on the daily direct limited express (November 2026 timetable) [[s:jg6305,jre_tt_tokyo]]. Full routes and fares are in [[l:izu-from-tokyo|Izu Peninsula from Tokyo: trains, fares and why to stay a week]].</p>
<h2>Which towns are on the Izu Peninsula?</h2>
<ul>
<li><strong>Shimoda.</strong> Port town at the southern tip. Beaches, a fish market and more than 1,000 tonnes of [[l:kinmedai|kinmedai]] landed a year, which the local tourism association says is the most of any port in Japan [[s:shimoda_kanko_kinme]].</li>
<li><strong>Shuzenji.</strong> Inland hot-spring town, 35 minutes by local line from Mishima [[s:jg6311]].</li>
<li><strong>Atami and Ito.</strong> The closest towns to Tokyo, with the most hotels.</li>
</ul>
<h2>When is the Izu Peninsula at its best?</h2>
<p>The official swimming season at Izu beaches runs from around mid-July to late August [[s:jg6322]]. Outside summer the towns are much quieter, and many restaurants and shops close early [[s:tdn]]. That quiet is the reason to come for a week instead of a weekend.</p>
<h2>Guides to the Izu Peninsula</h2>
<ul>
<li>[[l:shimoda-guide|Shimoda, Japan: a guide for a week or longer]]</li>
<li>[[l:izu-from-tokyo|Izu Peninsula from Tokyo: trains, fares and why to stay a week]]</li>
<li>[[l:kinmedai|Kinmedai: Japan’s golden-eye snapper and where to eat it]]</li>
</ul>
<h2>Where do we stay in Shimoda?</h2>
<p>Our place is <a href="{C.NODE_URL}" rel="noopener">NODE Shimoda</a>, a renovated apartment of about 40 m² on the second floor of a building in the old town. It’s 8 minutes on foot from Izukyu-Shimoda Station on a flat road, with a convenience store 2 minutes away, a supermarket 3 minutes away and Perry Road 5 minutes away [[s:node_site]]. There’s a shower but no bathtub, and about 13 steps up to the door [[s:node_room]].</p>
"""
    return (f'<div class="wrap"><article class="post">{crumbs(ctx, [(NAME, "home"), ("Places", "topic-places"), ("Izu Peninsula", None)])}'
            f'<p class="kicker">Places</p><h1>{C.IZU["h1"]}</h1><p class="dek">{C.IZU["dek"]}</p>'
            f'{img(ctx, "node-shimoda", "Living room with a sofa, low table and sliding paper screens", "NODE Shimoda, our home in the old town of Shimoda.", eager=True)}{ctx.expand(body)}'
            f'{ctx.sources([], "Sources")}{cta(ctx, photo=False)}</article></div>')


def page_about(ctx):
    body = f"""
<h2>Who runs Noki?</h2>
<p>Noki is run by RIVIA&amp;CO. LLC, a company based in Tokyo that renovates older houses in regional Japan and runs them as places to stay. Our first place to stay, <a href="{C.NODE_URL}" rel="noopener">NODE Shimoda</a>, is in Shimoda on the [[l:izu|Izu Peninsula]], and we are renovating an older house in Yaizu on Suruga Bay.</p>
<h2>Who writes the guides?</h2>
<p>Noki is put together by the two founders of RIVIA&amp;CO. We research and draft the guides with the help of AI tools, check every figure and rule against its source, and one of us reads each guide before it goes live.</p>
<ul class="people">
<li><strong>Shinta Katai</strong>, co-founder. Grew up in Shizuoka Prefecture and started his career at the Shizuoka Prefectural Government, then worked at a large manufacturer, at Recruit and at start-ups in HR tech and location data. He has run NODE Shimoda since July 2025.</li>
<li><strong>Yuma Ishihara</strong>, co-founder. From Osaka. He started in Recruit’s new-business development office and went on to build new businesses at start-ups in HR tech and cybersecurity.</li>
</ul>
<h2>Why “Noki”?</h2>
<p><em>Noki</em> (軒) are the eaves of a Japanese house. Swallows build their nests under them and often come back to the same one each spring. It’s also the word Japanese uses to count houses, one <em>ken</em> at a time. We hope you’ll find a place here that you keep coming back to.</p>
<h2>How are the guides written?</h2>
<ul>
<li><strong>Every figure and rule links to its source.</strong> Where we can, that is a government office or the operator itself, with the date we checked.</li>
<li><strong>We say which parts are our own experience.</strong> Anything about our homes comes from running them.</li>
<li><strong>We change the date only when the content changes.</strong> Fares, opening hours and visa rules move, so check the linked source before you book.</li>
<li><strong>We do not sell houses or give legal advice.</strong> Guides about akiya and visas are general information.</li>
</ul>
<h2>How do you tell us something is wrong?</h2>
<p>Write to us through our <a href="{SITE}/contact.html" hreflang="ja">contact form</a> (the form is in Japanese, but you’re welcome to write in English) and we will check the source and correct the guide. Company details, including our registered address, are on the <a href="{SITE}/about.html" hreflang="ja">RIVIA&amp;CO. company page</a> (in Japanese).</p>
<h2>Where to start</h2>
<ul>
<li>[[l:guides|All guides to long stays and akiya in Japan]]</li>
<li>[[l:akiya-try-first|Buying an akiya in Japan? Live in one for a month first]]</li>
</ul>
"""
    return (f'<div class="wrap"><article class="post">{crumbs(ctx, [(NAME, "home"), ("About", None)])}'
            f'<p class="kicker">About</p><h1>{C.ABOUT["h1"]}</h1><p class="dek">{C.ABOUT["dek"]}</p>{ctx.expand(body)}</article></div>')


def faq_html(ctx, faq, heading):
    return f"<h2>{heading}</h2>" + "".join(f"<h3>{q}</h3><p>{ctx.expand(a)}</p>" for q, a in faq)


def related_html(ctx, a):
    rel = [ART[p] for p in a.get("related", []) if p in ART and ART[p] in PUBLISHED]
    rel += [x for x in PUBLISHED if x is not a and x not in rel and set(x["topics"]) & set(a["topics"])]
    rel += [x for x in PUBLISHED if x is not a and x not in rel]
    cards = "".join(card(ctx, x) for x in rel[:3])
    return (f'<section class="related" aria-labelledby="rel-h"><div class="band__head"><h2 id="rel-h">Keep reading</h2>'
            f'<a class="more" href="{ctx.href("guides")}">All guides →</a></div><div class="grid3">{cards}</div></section>')


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", strip_tags(s).lower()).strip("-")[:60]


def add_ids(body_html):
    """本文の h2 に id を付け、目次を返す"""
    toc = []

    def f(m):
        text = m.group(1)
        sid = slugify(text)
        toc.append((sid, strip_tags(text)))
        return f'<h2 id="{sid}">{text}</h2>'
    return re.sub(r"<h2>(.+?)</h2>", f, body_html), toc


def page_article(ctx, a):
    k = a["topic"]
    trail = [(NAME, "home"), ("Guides", "guides"), (C.TOPICS[k]["name"], "topic-" + k), (a["h1"], None)]
    switch = f'<a class="switch" href="#ja-{a["id"]}">日本語レビュー版を見る →</a>' if ctx.mode == "preview" else ""
    pts = "".join(f"<li>{p}</li>" for p in a["points"])
    upd = "Updated" if a["updated"] != a["published"] else "Published"
    body, toc = add_ids(ctx.expand(a["body"]))
    toc.append(("common-questions", "Common questions"))
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    name, alt, caption = a["photo"]
    faq = "".join(f"<h3>{q}</h3><p>{ctx.expand(x)}</p>" for q, x in a["faq"])
    return (f'<header class="arthead"><div class="wrap wide">{crumbs(ctx, trail)}'
            f'<p class="acard__meta">{article_chips(ctx, a)}</p><h1>{a["h1"]}</h1><p class="dek">{a["dek"]}</p>'
            f'<p class="meta">By the <a href="{ctx.href("about")}">Noki team</a> · {upd} <time datetime="{a["updated"]}">{fmt_date(a["updated"])}</time> · {read_min(a)} min read</p>{switch}</div>'
            f'<div class="wrap wide">{img(ctx, name, alt, caption, eager=True, cls="photo photo--lead", sizes="(max-width: 62rem) 100vw, 62rem", want=1200)}</div></header>'
            f'<div class="wrap wide artgrid"><article class="post">'
            f'<div class="points"><p class="points__label">In short</p><ul>{pts}</ul></div>'
            + f'<details class="toc toc--inline"><summary>On this page</summary><ol>{toc_html}</ol></details>'
            f'{body}<h2 id="common-questions">Common questions</h2>{faq}{a.get("after_faq", "")}{ctx.sources(a["sources"], "Sources")}'
            f'<section class="byline" data-nosnippet>{MARK}<div><p><strong>Written by the Noki team</strong></p><p>Shinta Katai and Yuma Ishihara, the founders of RIVIA&amp;CO., who run NODE Shimoda, a place for long stays in Shimoda. '
            f'<a href="{ctx.href("about")}">How we write and check our guides</a>.</p></div></section></article>'
            f'<aside class="side" aria-label="On this page"><div class="side__sticky"><nav class="toc"><p class="toc__label">On this page</p><ol>{toc_html}</ol></nav></div></aside></div>'
            f'<div class="wrap wide">{related_html(ctx, a)}{cta(ctx, photo="[[img:node-shimoda" not in a["body"] and name != "node-shimoda")}</div>')


def serp_box(a_title, path, desc):
    return (f'<div class="serp" lang="en"><p class="serp__cap" lang="ja">Google の検索結果での見え方（英語のまま出ます）</p>'
            f'<p class="serp__url">{SITE}{path}</p><p class="serp__title">{a_title} | {NAME}</p><p class="serp__desc">{desc}</p></div>')


def page_article_ja(ctx, a):
    j = a["ja"]
    kws = "、".join(f"{k}（月{v}回・難易度{d}）" for k, v, d in a["keywords"])
    rv = "".join(f"<li>{p}</li>" for p in j["review"])
    pts = "".join(f"<li>{p}</li>" for p in j["points"])
    return (f'<div class="wrap"><article class="post"><p class="kicker">日本語レビュー版</p><h1>{j["h1"]}</h1><p class="dek">{j["dek"]}</p>'
            f'<p class="meta">{fmt_date_ja(a["updated"])} · Noki 編集部</p><a class="switch" href="#{a["id"]}">英語の本番記事を見る →</a>'
            f'<div class="review"><p class="review__label">レビューで見てほしい点</p><ul>{rv}</ul>'
            f'<p class="kw">狙う語：{kws}　／　検索する人の目的：{a["intent"]}</p>'
            f'<p class="review__foot">この日本語版は確認用です。公開するのは英語版だけで、本番のサイトには出力しません。</p></div>'
            f'{serp_box(a["seo_title"], PATHS[a["id"]], a["description"])}'
            f'<div class="points"><p class="points__label">この記事のポイント</p><ul>{pts}</ul></div>{ctx.expand(j["body"])}'
            f'{faq_html(ctx, j["faq"], "よくある質問")}{j.get("after_faq", "")}{ctx.sources(a["sources"], "出典")}</article></div>')


def table(head, rows, cls="free", num_cols=()):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f'<td{" class=n" if i in num_cols else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def page_ja_notes(ctx):
    arts = "".join(f'<li><a href="#ja-{a["id"]}">{a["ja"]["h1"]}</a><br><span class="fine">英語の題：{a["h1"]}</span></li>' for a in C.ARTICLES)
    left = {}
    for pid, _ in ednotes_en:
        left[pid] = left.get(pid, 0) + 1
    names = {"izu": "伊豆半島のページ", "about": "運営者情報のページ", **{a["id"]: a["ja"]["h1"] for a in C.ARTICLES}}
    ed = "".join(f"<li>{names.get(p, p)}：{n}か所</li>" for p, n in left.items())
    return f"""<div class="wrap"><article class="post">
<p class="kicker">日本語レビュー</p>
<h1>試作の確認ポイント</h1>
<p class="dek">英語メディア「Noki」の確認用ページです。英語の本番記事と、同じ内容の日本語レビュー版を対にしてあります。SEO の方針は<a href="#seo-plan">SEO計画</a>にまとめました。</p>

<h2>3記事の日本語レビュー版</h2>
<ul class="checklist">{arts}</ul>

<h2>確認が済んで、記事に入っている自社の情報</h2>
<ul class="checklist">
<li>下田の家「NODE Shimoda」は駅から徒歩約10分。飲食店・コンビニ・スーパーが徒歩圏</li>
<li>ワークデスク、洗濯機と乾燥機、調理器具のそろったキッチン、スマートロックのセルフチェックイン</li>
<li>長期滞在向けに改修した古い家。旅館業法の許可で通年営業。週割・月割あり</li>
<li>ゲストは欧米からが中心で、リモートワークの人が多い</li>
<li>運営会社は RIVIA&amp;CO. LLC（東京）</li>
<li>施設サイト https://nodeshimoda.com/ へのリンク（トップ、各記事の最後、本文の中）</li>
</ul>

<h2>写真</h2>
<p>自社の写真（NODE Shimoda のリビング、焼津の家のリフォーム前）はそのまま。ほかは Unsplash の写真に替えました。地名は書かず、写っているものだけを説明しています。クレジットは各ページの下の「Photo credits」に出ます。</p>
<ul class="checklist">
<li><strong>トップのFV</strong>：山と入り江の小さな町（coastal-village）</li>
<li><strong>長めに旅する</strong>：障子の窓辺の椅子と机、外に水辺（window-room）</li>
<li><strong>一年の一部を暮らす</strong>：生け垣と低い家の静かな道、後ろに緑の山（town-lane）</li>
<li><strong>家を持つ</strong>：古い木造の家の、何も置いていない和室（empty-tatami-room）</li>
<li><strong>場所</strong>：岩の海岸線（rocky-coast）</li>
<li><strong>金目鯛の記事</strong>：赤い魚の焼き物の定食（grilled-red-fish。金目鯛とは書いていません）</li>
<li><strong>伊豆の記事</strong>：電車の窓から見る海（train-window-sea）</li>
<li>まだ足りないもの：下田の町と浜、家のキッチン・ワークデスク・外観（自社で撮る）</li>
</ul>

<h2>まだ埋まっていない黄色い枠</h2>
<ul class="checklist">{ed}</ul>

<h2>トップページの文言（日本語訳）</h2>
{table(["英語", "日本語"], R.HOME_STRINGS)}

<h2>運営者情報のページ（About）の文言（日本語訳）</h2>
{table(["英語", "日本語"], R.ABOUT_STRINGS)}
<p class="fine">「なぜ Noki か」の節に、軒先に毎年帰ってくるツバメと、家を数える「軒」の話を入れ、「ここで、何度も帰ってきたくなる場所を見つけてほしい」と結んでいます。実感と違えば差し替えます。</p>
</article></div>"""


def page_seo_plan(ctx):
    def state(s):
        return f'<span class="tag{" tag--done" if s == "公開準備" else ""}">{s}</span>'
    kw_rows = [(g, k, v, d, note, page, state(s)) for g, k, v, d, note, page, s in R.KEYWORDS]
    done = "".join(f"<li><strong>{t}</strong><br>{d}</li>" for t, d in R.DONE)
    todo = "".join(f"<li><strong>{t}</strong><br>{d}</li>" for t, d in R.TODO)
    aki = "".join(f"<li>{t}</li>" for t in R.FROM_AKIYADO)
    pages = [("トップ", PATHS["home"], C.HOME["seo_title"]), ("記事一覧", PATHS["guides"], C.GUIDES["seo_title"]), ("伊豆半島", PATHS["izu"], C.IZU["seo_title"]), ("運営者情報", PATHS["about"], C.ABOUT["seo_title"])]
    pages += [(a["ja"]["h1"], PATHS[a["id"]], a["seo_title"]) for a in C.ARTICLES]
    return f"""<div class="wrap wide"><article class="post">
<p class="kicker">SEO計画</p>
<h1>Noki の SEO 計画</h1>
<p class="dek">狙う読み手は2つです。日本に長く滞在したい海外の人と、日本の空き家を買う・活かすことを考えている海外の人。どちらも最後は「まず自社の家に泊まってみる」につなげます。</p>

<div class="points"><p class="points__label">結論</p><ul>
<li>空き家の語は検索が多く、上位に新しい専門サイトが並んでいます。英語の良い解説が少ない「外国人は買えるか」「安い家の本当の費用」から入れます。</li>
<li>長期滞在の語は検索が少なめですが、予約に近い人が探しています。「日本で家を1か月借りる」を、自社の家への入口にします。</li>
<li>町の語（伊豆半島・下田）は大手が強く、時間がかかります。金目鯛のように、上位が弱い語から町を知ってもらいます。</li>
<li>新しいドメインは、成果が出るまで数か月かかります。順位の約束はできません。</li>
</ul></div>

<h2>キーワードマップ</h2>
<p class="fine">2026年11月14日に調べた、米国の Google での月間検索回数と難易度（0〜100。調査ツールの推定値）です。英国・豪州などの検索は含みません。難易度は被リンクからの推定で、「上位の顔ぶれ」の方が実態に近い手がかりです。</p>
{table(["テーマ", "キーワード", "月間検索", "難易度", "上位の顔ぶれ・見立て", "受けるページ", "状態"], kw_rows, num_cols=(2, 3))}

<h2>これから書く記事（優先順）</h2>
{table(["順", "記事", "狙う語と月間検索", "テーマ", "書き方の要点"], R.ROADMAP)}
<p class="fine">同じテーマの記事が3本そろうと、テーマ別の一覧ページ（/noki/akiya.html など）が自動でできます。</p>

<h2>ページと URL、検索結果に出る題</h2>
{table(["ページ", "URL", "検索結果に出る題（title）"], pages)}

<h2>今回、本番用に実装したもの</h2>
<ul class="checklist">{done}</ul>

<h2>公開までに、人が決める・用意すること</h2>
<ul class="checklist">{todo}</ul>

<h2>アキヤドから取り入れたこと</h2>
<ul class="checklist">{aki}</ul>
</article></div>"""


# ------------------------------------------------------------------ 構造化データ
# 書き手（About の「Who writes the guides?」と同じ2人。人の了承 2026-11-19）
AUTHORS = [{"@type": "Person", "name": n, "jobTitle": "Co-founder", "worksFor": {"@id": ORG_ID}, "url": SITE + PATHS["about"]} for n in ("Shinta Katai", "Yuma Ishihara")]


def org_ld():
    """運営会社。本体はアキヤド側の about.html にあり、ここでは同じ @id で参照する"""
    return {"@type": "Organization", "@id": ORG_ID, "name": CFG["operator_name"], "alternateName": CFG["operator_alt"], "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": SITE + "/images/logo/logo.png"}}


def crumb_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}


def ld_for(page):
    k, path = page["kind"], page["path"]
    url = SITE + path
    part = {"@id": WEBSITE_ID}
    g = []
    if k == "home":
        # WebSite は置かない（同じドメインに名前の違う WebSite を置くと、サイト名の判定がぶれる）
        g += [{"@type": "CollectionPage", "@id": url, "url": url, "name": NAME, "description": page["description"], "isPartOf": part, "inLanguage": "en",
               "publisher": {"@id": ORG_ID}}, org_ld()]
    elif k in ("guides", "topic"):
        arts = page["articles"]
        g += [{"@type": "CollectionPage", "@id": url, "url": url, "name": page["seo_title"], "description": page["description"], "isPartOf": part, "inLanguage": "en",
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": SITE + PATHS[a["id"]], "name": strip_tags(a["h1"])} for i, a in enumerate(arts)]}},
              crumb_ld(page["trail"])]
    elif k == "izu":
        g += [{"@type": "WebPage", "@id": url, "url": url, "name": page["seo_title"], "description": page["description"], "isPartOf": part, "inLanguage": "en",
               "about": {"@type": "Place", "name": "Izu Peninsula", "address": {"@type": "PostalAddress", "addressRegion": "Shizuoka", "addressCountry": "JP"}},
               "publisher": {"@id": ORG_ID}}, org_ld(), crumb_ld(page["trail"])]
    elif k == "about":
        g += [{"@type": "AboutPage", "@id": url, "url": url, "name": page["seo_title"], "description": page["description"], "isPartOf": part, "inLanguage": "en",
               "mainEntity": {"@id": ORG_ID}}, org_ld(), crumb_ld(page["trail"])]
    elif k == "article":
        a = page["article"]
        g += [{"@type": "Article", "@id": url + "#article", "headline": strip_tags(a["h1"]), "description": a["description"],
               "image": [SITE + PRE + f"/assets/og/{a['slug']}.png"] + ([SITE + PRE + "/assets/photos/node-shimoda-1200.webp"] if "[[img:node-shimoda" in a["body"] else []), "datePublished": a["published"], "dateModified": a["updated"], "inLanguage": "en",
               "author": AUTHORS, "publisher": {"@id": ORG_ID}, "isPartOf": part,
               "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
              org_ld(), crumb_ld(page["trail"]),
              {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                  {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(ans)}} for q, ans in a["faq"]]}]
    if not g:
        return ""
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + "</script>"


# ------------------------------------------------------------------ 本番ページの外枠
def header(ctx, preview=False):
    extra = ""
    topics = "".join(f'<li><a href="{ctx.href("topic-" + k)}">{esc(C.TOPICS[k]["name"])}</a></li>' for k in HUB_TOPICS)
    menu_topics = "".join(
        f'<li><a href="{ctx.href("topic-" + k)}"><strong>{esc(C.TOPICS[k]["name"])}</strong><span>{esc(C.TOPICS[k]["path_desc"])}</span></a></li>' for k in OPEN_PLANS)
    menu_arts = "".join(f'<li><a href="{ctx.href(a["id"])}">{a["h1"]}</a></li>' for a in PUBLISHED)
    return (f'<header class="top"><div class="wrap wide top__bar"><a class="brand" href="{ctx.href("home")}">{MARK}<span>{NAME}</span></a>'
            f'<nav class="nav" aria-label="Main"><ul>{topics}<li><a href="{ctx.href("about")}">About</a></li></ul></nav>'
            f'{extra}<a class="btn btn--solid btn--sm top__cta" href="{C.BOOK_URL}" rel="noopener">Stay with us</a>'
            f'<details class="menu"><summary aria-label="Menu"><span></span><span></span><span></span></summary>'
            f'<div class="menu__panel"><p class="menu__h">Your plan</p><ul class="menu__topics">{menu_topics}</ul>'
            f'<p class="menu__h">Places</p><ul class="menu__list">' + "".join(f'<li><a href="{ctx.href(p["page"])}">{esc(p["name"])}</a></li>' for p in C.PLACES.values()) + f'<li><a href="{ctx.href("topic-places")}">All places</a></li></ul>'
            f'<p class="menu__h">Latest guides</p><ul class="menu__list">{menu_arts}</ul>'
            f'<ul class="menu__list"><li><a href="{ctx.href("guides")}">All guides</a></li><li><a href="{ctx.href("about")}">About us</a></li></ul>'
            f'<a class="btn btn--solid" href="{C.BOOK_URL}" rel="noopener">Stay at NODE Shimoda</a></div></details></div></header>')


def credits(names):
    """Unsplash の写真のクレジット（Photo by 撮影者 on Unsplash）。そのページで使った写真の撮影者ごとに1行"""
    u = C.UNSPLASH_UTM
    items = [f'<li>Photo by <a href="{c[1]}{u}" rel="noopener">{esc(c[0])}</a> on <a href="https://unsplash.com/{u}" rel="noopener">Unsplash</a></li>'
             for c in {C.PHOTO_CREDITS[n][1]: C.PHOTO_CREDITS[n] for n in names if n in C.PHOTO_CREDITS}.values()]
    return f'<div class="wrap wide foot__credits"><p class="foot__h">Photo credits</p><ul>{"".join(items)}</ul></div>' if items else ""


def footer(ctx, photos=None):
    topics = "".join(f'<li><a href="{ctx.href("topic-" + k)}">{esc(C.TOPICS[k]["name"])}</a></li>' for k in OPEN_PLANS)
    arts = "".join(f'<li><a href="{ctx.href(a["id"])}">{a["h1"]}</a></li>' for a in PUBLISHED[:5])
    corp = "https://rivia-co.com/" if ctx.mode == "preview" else "/"
    return (f'<footer class="foot"><div class="wrap wide foot__grid">'
            f'<div><a class="brand brand--foot" href="{ctx.href("home")}">{MARK}<span>{NAME}</span></a><p>{esc(CFG["tagline"])}.</p>'
            f'<p>Run by <a href="{corp}" hreflang="ja">RIVIA&amp;CO.</a> (site in Japanese).</p></div>'
            f'<nav aria-label="Your plan"><p class="foot__h">Your plan</p><ul>{topics}<li><a href="{ctx.href("guides")}">All guides</a></li></ul></nav>'
            f'<nav aria-label="Places"><p class="foot__h">Places</p><ul><li><a href="{ctx.href("topic-places")}">All places</a></li><li><a href="{ctx.href("izu")}">Izu Peninsula</a></li></ul></nav>'
            f'<nav aria-label="Popular guides"><p class="foot__h">Popular guides</p><ul>{arts}</ul></nav>'
            f'<nav aria-label="About"><p class="foot__h">Noki</p><ul><li><a href="{C.NODE_URL}" rel="noopener">NODE Shimoda</a></li>'
            f'<li><a href="{ctx.href("home", "homes")}">Our homes</a></li><li><a href="{ctx.href("about")}">About us</a></li></ul></nav>'
            f'</div>{credits(ctx.photos if photos is None else photos)}</footer>')


# 宿の予約ページ（Airbnb）・公式サイトへのクリックを GA4 のイベント cta_click として記録する（アキヤドと同じイベント名。どの記事から予約に向かったかを見るため）
CTA_JS = ("document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a||typeof gtag!=='function')return;"
          "var h=a.getAttribute('href');if(h.indexOf('airbnb.com/rooms')<0&&h.indexOf('nodeshimoda.com')<0)return;"
          "gtag('event','cta_click',{cta:'node_shimoda',site:'noki',link_url:h,link_text:(a.textContent||'').trim().slice(0,60),page_path:location.pathname});});")


def dist_html(page, main, ctx):
    url = SITE + page["path"]
    title = page["seo_title"] if page["kind"] == "home" else f'{page["seo_title"]} | {NAME}'
    og_img = SITE + PRE + (f"/assets/og/{page['article']['slug']}.png" if page["kind"] == "article" else "/assets/og/default.png")
    robots = "noindex" if page.get("noindex") else "index,follow,max-image-preview:large"
    head = [
        '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(title)}</title>", f'<meta name="description" content="{esc(page["description"])}">',
        f'<meta name="robots" content="{robots}">',
    ]
    if not page.get("noindex"):
        head.append(f'<link rel="canonical" href="{url}">')
    head += [
        f'<meta property="og:type" content="{"article" if page["kind"] == "article" else "website"}">',
        f'<meta property="og:site_name" content="{NAME}">', f'<meta property="og:title" content="{esc(page["seo_title"])}">',
        f'<meta property="og:description" content="{esc(page["description"])}">', f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{og_img}">', '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
        f'<meta property="og:locale" content="{CFG["locale"]}">', '<meta name="twitter:card" content="summary_large_image">',
    ]
    if page["kind"] == "article":
        a = page["article"]
        head += [f'<meta property="article:published_time" content="{a["published"]}">', f'<meta property="article:modified_time" content="{a["updated"]}">']
    head += [
        f'<link rel="icon" href="{PRE}/assets/favicon.svg" type="image/svg+xml">', f'<link rel="apple-touch-icon" href="{PRE}/assets/apple-touch-icon.png">',
        '<meta name="theme-color" content="#f7f3ea" media="(prefers-color-scheme: light)">', '<meta name="theme-color" content="#12161f" media="(prefers-color-scheme: dark)">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">', '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link href="{FONTS_EN}" rel="stylesheet">', f'<link rel="stylesheet" href="{PRE}/assets/site.css">', ld_for(page),
    ]
    if CFG.get("ga4_id"):
        gid = CFG["ga4_id"]
        head.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{gid}");</script>')
    return (f'<!DOCTYPE html>\n<html lang="en"><head>\n' + "\n".join(h for h in head if h) + '\n</head><body>'
            f'<a class="skip" href="#main">Skip to content</a>{header(ctx)}<main id="main" class="page is-static">{main}</main>{footer(ctx)}'
            + (f'<script>{CTA_JS}</script>' if CFG.get("ga4_id") else "") + '</body></html>\n')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def make_images():
    from PIL import Image, ImageDraw, ImageFont
    serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if not os.path.exists(serif):
        return False
    ink, paper, red, sea = (28, 34, 48), (247, 243, 234), (185, 61, 38), (43, 74, 126)  # site.css の墨・和紙・朱・藍
    shapes = mark_polys()

    def mark(im, x, y, s, fill):
        """ロゴを im の (x, y) に倍率 s で置く。4倍で描いて縮め、縁をなめらかにする"""
        k = 4
        w, h = int(64 * s) + 1, int(64 * s) + 1
        big = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(big)
        col = {"ink": fill, "paper": paper, "red": red}
        for name, v in shapes:
            if isinstance(v[0], tuple):
                d.polygon([(px * s * k, py * s * k) for px, py in v], fill=col[name])
            else:
                cx, cy, r = v
                d.ellipse([(cx - r) * s * k, (cy - r) * s * k, (cx + r) * s * k, (cy + r) * s * k], fill=col[name])
        small = big.resize((w, h), Image.LANCZOS)
        im.paste(small, (round(x), round(y)), small)

    def og(path, title, kicker):
        im = Image.new("RGB", (1200, 630), paper)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 1200, 14], fill=sea)
        mark(im, 70, 60, 1.6, ink)
        d.text((190, 86), NAME, font=ImageFont.truetype(serif, 44), fill=ink)
        d.text((80, 220), kicker.upper(), font=ImageFont.truetype(sans, 26), fill=red)
        size = 68
        while True:
            f = ImageFont.truetype(serif, size)
            lines, cur = [], ""
            for w in title.split():
                t = (cur + " " + w).strip()
                if d.textlength(t, font=f) <= 1040:
                    cur = t
                else:
                    lines.append(cur)
                    cur = w
            lines.append(cur)
            if len(lines) <= 4 or size <= 40:
                break
            size -= 6
        y = 270
        for ln in lines:
            d.text((80, y), ln, font=f, fill=ink)
            y += int(size * 1.22)
        d.text((80, 560), CFG["tagline"], font=ImageFont.truetype(sans, 26), fill=(85, 101, 111))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        im.save(path, optimize=True)

    og(os.path.join(DIST, "assets/og/default.png"), "Stay a while in small-town Japan.", "Homes in small-town Japan")
    for a in C.ARTICLES:
        og(os.path.join(DIST, f"assets/og/{a['slug']}.png"), strip_tags(a["h1"]), a["kicker"])
    for name, size in (("logo.png", 512), ("apple-touch-icon.png", 180)):
        im = Image.new("RGB", (size, size), paper)
        sc = size / 72  # 形の範囲（x 3〜61.6、y 8.5〜49.5）を真ん中に置く
        mark(im, size / 2 - 32.3 * sc, size / 2 - 29 * sc, sc, ink)
        im.save(os.path.join(DIST, "assets", name), optimize=True)
    return True


def build():
    global ednotes, ednotes_en
    for d in (DIST, PREVIEW):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)

    # ---- ページの一覧（本番）
    G = ("Guides", PATHS["guides"])
    pages = [
        {"id": "home", "kind": "home", "path": PATHS["home"], **C.HOME},
        {"id": "guides", "kind": "guides", "path": PATHS["guides"], "articles": PUBLISHED, "trail": [(NAME, PRE), G], **C.GUIDES},
        {"id": "izu", "kind": "izu", "path": PATHS["izu"], "trail": [(NAME, PRE), ("Places", PATHS["topic-places"]), ("Izu Peninsula", PATHS["izu"])], **C.IZU},
        {"id": "about", "kind": "about", "path": PATHS["about"], "trail": [(NAME, PRE), ("About", PATHS["about"])], **C.ABOUT},
    ]
    for k in HUB_TOPICS:
        t = C.TOPICS[k]
        pages.append({"id": "topic-" + k, "kind": "topic", "topic": k, "path": PATHS["topic-" + k], "seo_title": t["seo_title"], "description": t["description"],
                      "noindex": k not in INDEXED_TOPICS,
                      "articles": hub_articles(k) + [a for a in hub_also(k) if a not in hub_articles(k)], "trail": [(NAME, PRE), G, (t["name"], PATHS["topic-" + k])]})
    for a in PUBLISHED:
        trail = [(NAME, PRE), G, (C.TOPICS[a["topic"]]["name"], PATHS["topic-" + a["topic"]])]
        trail.append((strip_tags(a["h1"]), PATHS[a["id"]]))
        pages.append({"id": a["id"], "kind": "article", "path": PATHS[a["id"]], "article": a, "seo_title": a["seo_title"], "description": a["description"], "trail": trail})

    def render(ctx, p):
        k = p["kind"]
        return {"home": page_home, "guides": page_guides, "izu": page_izu, "about": page_about}[k](ctx) if k in ("home", "guides", "izu", "about") \
            else page_topic(ctx, p["topic"]) if k == "topic" else page_article(ctx, p["article"])

    # ---- 本番の公開フォルダ（site.json の prefix と同じ名前）
    def out_file(path):
        return os.path.join(DIST, "index.html") if path == PRE else os.path.join(ROOT, path.lstrip("/"))

    ednotes = []
    for p in pages:
        write(out_file(p["path"]), dist_html(p, render(rctx := Ctx("dist", p["id"]), p), rctx))
    ednotes_en = list(ednotes)
    write(os.path.join(DIST, "assets/site.css"), CSS)
    write(os.path.join(DIST, "assets/favicon.svg"), mark_svg({"ink": "#1c2230", "paper": "#f7f3ea", "red": "#b93d26"}, 'xmlns="http://www.w3.org/2000/svg"'))
    make_images()
    shutil.copytree(os.path.join(HERE, "photos"), os.path.join(DIST, "assets/photos"))
    shutil.copytree(os.path.join(HERE, "photos"), os.path.join(PREVIEW, "assets/photos"))

    # sitemap（Noki の分だけ。robots.txt に2本目の Sitemap として書く）
    newest = max([a["updated"] for a in PUBLISHED] or [TODAY])
    lastmod = {p["path"]: (p["article"]["updated"] if p["kind"] == "article" else newest) for p in pages}
    urls = "\n".join(f"  <url><loc>{SITE}{p['path']}</loc><lastmod>{lastmod[p['path']]}</lastmod></url>" for p in pages if not p.get("noindex"))
    write(os.path.join(DIST, "sitemap.xml"), f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    # llms.txt に足す段落（アキヤドの build が seo/llms.txt の末尾に付ける）
    ll = ["## Noki (English)", "", "> Noki is RIVIA&CO.’s English-language guide for people who want to travel slowly in small-town Japan, live here part of the year, work remotely or buy an akiya (vacant house).", "",
          f"- [Noki]({SITE}{PRE}): {C.HOME['description']}", f"- [Izu Peninsula]({SITE}{PATHS['izu']}): {C.IZU['description']}"]
    ll += [f"- [{strip_tags(a['h1'])}]({SITE}{PATHS[a['id']]}): {a['description']}" for a in PUBLISHED]
    write(os.path.join(HERE, "llms_section.txt"), "\n".join(ll) + "\n")

    # ---- 試作 preview/index.html（1ファイル。ページは # で切り替え）
    ednotes = []
    mains = []
    for p in pages:
        ctx = Ctx("preview", p["id"])
        title = p["seo_title"] if p["kind"] == "home" else f'{p["seo_title"]} | {NAME}'
        mains.append(f'<main class="page" data-page="{p["id"]}" data-title="{esc(title)}" lang="en">{render(ctx, p)}</main>')
    for a in C.ARTICLES:
        ctx = Ctx("preview", "ja-" + a["id"], "ja")
        mains.append(f'<main class="page" data-page="ja-{a["id"]}" data-title="{esc(a["ja"]["h1"])}（レビュー版）" lang="ja">{page_article_ja(ctx, a)}</main>')
    mains.append(f'<main class="page" data-page="ja-notes" data-title="試作の確認ポイント" lang="ja">{page_ja_notes(Ctx("preview", "ja-notes", "ja"))}</main>')
    mains.append(f'<main class="page" data-page="seo-plan" data-title="SEO計画" lang="ja">{page_seo_plan(Ctx("preview", "seo-plan", "ja"))}</main>')
    pctx = Ctx("preview", "home")
    router = """(function(){var pages=[].slice.call(document.querySelectorAll('.page'));function show(first){var h=(location.hash||'').slice(1)||'home';var t=pages.filter(function(p){return p.getAttribute('data-page')===h;})[0];var el=null;if(!t){el=h&&document.getElementById(h);if(el){t=el.closest('.page');}}t=t||pages[0];pages.forEach(function(p){p.classList.toggle('is-active',p===t);});document.title=t.getAttribute('data-title');if(el){el.scrollIntoView();}else if(!first){window.scrollTo(0,0);}}window.addEventListener('hashchange',function(){show(false);});show(true);})();"""
    prev = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Noki 試作</title>'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{FONTS_ALL}" rel="stylesheet"><style>{CSS}</style></head><body>'
            f'<div class="proto" lang="ja"><div class="wrap">試作です（本番は1ページごとに別のURL）。<a href="#ja-notes">日本語レビュー</a>・<a href="#seo-plan">SEO計画</a></div></div>'
            f'{header(pctx, preview=True)}{"".join(mains)}{footer(pctx, list(C.PHOTO_CREDITS))}<script>{router}</script></body></html>')
    write(os.path.join(PREVIEW, "index.html"), prev)

    print(f"{PRE.strip('/')}/: {len(pages)} ページ ／ 公開記事 {len(PUBLISHED)} 本 ／ テーマ別一覧 {len(HUB_TOPICS)}（検索に載せる {len(INDEXED_TOPICS)}） ／ 黄色い枠 {len(ednotes_en)} か所")


ednotes_en = []
if __name__ == "__main__":
    build()
