#!/usr/bin/env python3
"""記事の組み込みツール（アキヤド）。エンジニア部が記事の追加・削除のたびに使う。

使い方:
  python3 tools/add_article.py <slug>              # 記事を組み込む（追加。既にあれば作り直す）
  python3 tools/add_article.py <slug> --dry-run    # 変更するファイルと件数だけ表示（書き込まない）
  python3 tools/add_article.py --remove <slug>     # カード・索引・sitemap・llms.txt から取り除く
  python3 tools/add_article.py --remove <slug> --dry-run
  python3 tools/add_article.py --sync              # 追加・削除はせず、ガイドから作られる部分と日付だけをそろえる
  オプション: --no-llms（llms.txt を作り直さない）、--today YYYY-MM-DD（llms.txt の判定日。テスト用）

前提:
  pages/media/<slug>.html が、同じカテゴリの既存記事をコピーして作成済みであること。
  このツールは記事ファイルから次の情報を読み取る（どれかが欠けるとエラーで止まる）。
    - カテゴリ     : <a href="../media/category-XXX.html" class="tag article__cat">ラベル</a>
    - タイトル     : <h1 class="article__title">…</h1> の中身（<wbr> もそのままカードに使う）
    - 公開日       : <article class="article" data-publish="YYYY-MM-DD">（Article の datePublished と一致が必要）
    - 更新日       : Article の dateModified（sitemap の lastmod に使う）
    - 写真         : <figure class="article__photo"> の img（images/photos/<名前>.jpg と
                     images/photos/w/<名前>-800.webp が必要。カードは同じ写真の WebP 軽量版＋原寸を srcset で使う）
    - 関連サービス : <aside class="article-cta"> 内の ../service-*.html へのリンク
    - ガイド       : <div class="article__for">（こんな方に）内の ../media/guide-*.html へのリンク
    - 検索の索引   : meta description、「この記事のポイント」、本文の見出し・段落・表・リスト、FAQ の質問

組み込み先と並び順（本番ブランチの HTML 全体から検証して決めたもの）:
  記事カード（.media-grid の中の a.media-card。どのページでも同じ形）
    1. pages/media.html の「新着記事」と「すべての記事」(#media-list)、pages/index.html: 全記事。
    2. pages/service-*.html: 記事の article-cta に載っているサービスのページだけ。
    3. pages/media/category-<カテゴリ>.html: 同じカテゴリの記事だけ。
       1〜3 はすべて公開日の新しい順。
    4. 各記事の「あわせて読みたい記事」: 自分以外の全記事。次の4グループの順に並べ、
       各グループ内は seo/sitemap.xml の記事の並び順（＝記事を組み込んだ順。sitemap には公開日の古い順に入れるので、
       ふつうは公開日の古い順になる）。
         (0) 同じカテゴリ かつ 関連サービス（article-cta）が1つ以上共通
         (1) 同じカテゴリ だが 関連サービスの共通なし
         (2) 別のカテゴリ だが 関連サービスが1つ以上共通
         (3) 別のカテゴリ かつ 関連サービスの共通なし
       新しい記事自身の「あわせて読みたい記事」は、このルールで丸ごと作り直す（コピー元の一覧は捨てる）。
    5. 同じ公開日の記事どうしの順番は、seo/sitemap.xml の記事の並び順（どのリストでも同じ）。
       新しく加える記事は、同じ公開日の既存記事の後ろに入る。
       注意: case-rental-house-inn-first-year（2026-10-10）は、本番ブランチで sitemap の末尾に足されたため、
       sitemap と「あわせて読みたい記事」では公開日がもっと新しい記事より後ろにある（4 のルールどおり）。
       取り除いて入れ直すと、sitemap の公開日どおりの位置に移り、「あわせて読みたい記事」でも前に移る。
       既存の 2026-09-29 の7本も、取り除いて入れ直すと同じ日の末尾に移る。
  そのほか
    6. pages/media.html の構造化データ CollectionPage の hasPart: 「すべての記事」と同じ順。
    7. js/media-index.js（記事検索の索引）: 公開日の新しい順（同じ日は sitemap の順）。
    8. seo/sitemap.xml: 新しい記事の行は、公開日がそれより新しい最初の記事の行の前に入れる（同じ公開日の記事の後ろ）。
       lastmod は dateModified。記事の行は、ガイドの行より後ろに置く。
    9. seo/llms.txt: tools/build_llms.py で丸ごと作り直す。
  ガイド（pages/media/guide-*.html）から作られる部分（毎回ガイドのページに合わせて作り直す）
   10. 各記事の「この記事を含むガイド」(nav.guide-box): その記事の「こんな方に」の最初のガイドの記事一覧（ガイドの順）。
   11. ガイドのページの構造化データ ItemList: ページ上の記事（li.guide-step）の順。
   12. ガイドの li.guide-step、各記事の guide-box、media.html の「よくある悩み」(.mq) の data-date: 記事の公開日。

  ガイドのページ自体（どの Step の何番目に置くか、ステップ番号）と「よくある悩み」の質問文は編集の判断なので、
  このツールは足しも消しもしない。「こんな方に」にあるのにガイドに載っていない記事は警告を出すので、
  既存の <li class="guide-step"> をコピーして手で足し（番号 01, 02… も振り直す）、もう一度このツールを実行する。
  --remove のときも、ガイド・「よくある悩み」に残っているリンクは警告で知らせる（手で外す）。

何度実行しても結果は同じ（追加は「いったん全ファイルから取り除いてから、正しい位置に入れる」ため、重複しない）。
タイトル・カテゴリ・写真・関連サービス・公開日を直したときも、同じコマンドを再実行すれば全カードが更新される。

このツールが更新しないもの（手で更新する）:
  - docs/site-spec.md の「掲載記事」と「公開スケジュール」
  - 記事本文中の他記事へのリンク、ガイドのページ、「よくある悩み」の質問
"""
import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
MEDIA = PAGES / "media"
SITEMAP = ROOT / "seo" / "sitemap.xml"
SEARCH_INDEX = ROOT / "js" / "media-index.js"
PHOTOS = ROOT / "images" / "photos"
SITE = "https://rivia-co.com"
GUIDES = ("sell", "use", "side")  # ナビ・「こんな方に」と同じ順

GRID_RE = re.compile(r'^(?P<ind> *)<div class="media-grid[^"]*"[^>]*>\n', re.M)
CARD_RE = re.compile(
    r'^(?P<ind> *)<a href="(?:\.\./)?media/(?P<slug>[\w-]+)\.html" class="media-card[^"]*" '
    r'data-category="(?P<cat>\w+)" data-date="(?P<date>[\d-]+)">\n.*?^(?P=ind)</a>\n',
    re.M | re.S,
)
SITEMAP_ARTICLE_RE = re.compile(
    r'^  <url><loc>' + re.escape(SITE) + r'/media/(?P<slug>[\w-]+)\.html</loc>.*?</url>\n', re.M
)
LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


class ToolError(Exception):
    pass


def _plain(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


# ---------------------------------------------------------------- 検索の索引の本文

class _BodyText(HTMLParser):
    """本文（section.article__section。FAQ を除く）の段落・表の行・リスト・小見出し・callout を
    1つずつ取り出す。既存の js/media-index.js と同じく、実体参照（&amp; など）はそのまま残す"""
    BLOCKS = ("tr", "p", "li", "h3", "h4", "dt", "dd")

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts, self.cur, self.sec, self.secdepth = [], None, None, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "section" and "article__section" in cls and self.sec is None:
            self.sec, self.secdepth = a.get("id"), 1
            return
        if self.sec is not None and tag == "section":
            self.secdepth += 1
        if self.sec is None or self.sec == "faq":
            return
        if self.cur is None and (tag in self.BLOCKS or (tag == "div" and "callout" in cls)):
            self.cur = [tag, [], 0]
        elif self.cur is not None and tag == self.cur[0]:
            self.cur[2] += 1

    def handle_endtag(self, tag):
        if self.sec is not None and tag == "section":
            self.secdepth -= 1
            if self.secdepth == 0:
                self.sec = None
            return
        if self.cur and tag == self.cur[0]:
            if self.cur[2] > 0:
                self.cur[2] -= 1
                return
            txt = "".join(self.cur[1]).strip()
            if txt:
                self.parts.append(txt)
            self.cur = None

    def handle_entityref(self, name):
        if self.cur:
            self.cur[1].append(f"&{name};")

    def handle_charref(self, name):
        if self.cur:
            self.cur[1].append(f"&#{name};")

    def handle_data(self, data):
        if self.cur:
            self.cur[1].append(data)


def search_text(s: str, title: str, desc: str) -> str:
    kp = re.search(r'<section class="keypoints".*?<ul>(.*?)</ul>', s, re.S)
    keypoints = [_plain(x) for x in re.findall(r"<li>(.*?)</li>", kp.group(1), re.S)] if kp else []
    heads = [_plain(h) for sid, h in re.findall(
        r'<section class="article__section" id="([\w-]+)">\s*<h2>(.*?)</h2>', s, re.S) if sid != "faq"]
    faq = [_plain(q) for q in re.findall(
        r'<summary class="faq__q"><span class="faq__mark">Q</span><span>(.*?)</span><span class="faq__toggle"', s, re.S)]
    body = _BodyText()
    body.feed(s)
    return " ".join([title, desc] + keypoints + heads + faq + body.parts) + " "


# ---------------------------------------------------------------- 記事の読み取り

_cache = {}


def article_slugs():
    """記事ファイル（data-publish を持つ pages/media/*.html）の slug"""
    return sorted(f.stem for f in MEDIA.glob("*.html") if "data-publish=" in f.read_text(encoding="utf-8"))


def read_article(slug: str) -> dict:
    if slug in _cache:
        return _cache[slug]
    path = MEDIA / f"{slug}.html"
    if not path.is_file():
        raise ToolError(f"記事ファイルがありません: {path.relative_to(ROOT)}")
    s = path.read_text(encoding="utf-8")

    def need(pattern, what, flags=0):
        m = re.search(pattern, s, flags)
        if not m:
            raise ToolError(f"{slug}: {what} が見つかりません（パターン: {pattern}）")
        return m

    m = need(r'<a href="\.\./media/category-(\w+)\.html" class="tag article__cat">([^<]+)</a>', "カテゴリ（article__cat）")
    cat, cat_label = m.group(1), m.group(2)
    if not (MEDIA / f"category-{cat}.html").is_file():
        raise ToolError(f"{slug}: カテゴリ一覧 pages/media/category-{cat}.html がありません")
    title_html = need(r'<h1 class="article__title">(.*?)</h1>', "タイトル（h1.article__title）", re.S).group(1)
    publish = need(r'<article class="article" data-publish="(\d{4}-\d{2}-\d{2})"', "data-publish").group(1)
    m = need(r'<figure class="article__photo"><img src="\.\./\.\./images/photos/([\w-]+)\.jpg" '
             r'srcset="\.\./\.\./images/photos/w/\1-800\.webp 800w, \.\./\.\./images/photos/\1\.jpg (\d+)w"',
             "記事の写真（figure.article__photo の src・srcset）")
    photo, photo_w = m.group(1), m.group(2)
    for p in (PHOTOS / f"{photo}.jpg", PHOTOS / "w" / f"{photo}-800.webp"):
        if not p.is_file():
            raise ToolError(f"{slug}: 写真 {p.relative_to(ROOT)} がありません（原寸の jpg と幅800の WebP の両方が必要）")
    art = None
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            raise ToolError(f"{slug}: 構造化データの JSON が壊れています: {e}")
        if isinstance(data, dict) and data.get("@type") in ("Article", "BlogPosting", "NewsArticle"):
            art = data
    if not art:
        raise ToolError(f"{slug}: 構造化データ Article がありません")
    if art.get("datePublished") != publish:
        raise ToolError(f"{slug}: data-publish({publish}) と datePublished({art.get('datePublished')}) が不一致")
    modified = art.get("dateModified") or publish
    cta = need(r'<aside class="article-cta">(.*?)</aside>', "関連サービス（aside.article-cta）", re.S).group(1)
    services = re.findall(r'href="\.\./(service-[\w-]+\.html)"', cta)
    fr = re.search(r'<div class="article__for">(.*?)</div>', s, re.S)
    guides = re.findall(r'href="\.\./media/guide-(\w+)\.html"', fr.group(1)) if fr else []
    title = _plain(title_html)
    desc = html.unescape(need(r'<meta name="description" content="([^"]*)"', "meta description").group(1))
    info = dict(slug=slug, cat=cat, cat_label=cat_label, title_html=title_html, title=title,
                headline=art.get("headline") or title, publish=publish, modified=modified,
                photo=photo, photo_w=photo_w, services=services, guides=guides, desc=desc,
                text=search_text(s, title, desc))
    _cache[slug] = info
    return info


# ---------------------------------------------------------------- カード

def render_card(a: dict, in_media_dir: bool, ind: str = " " * 10) -> str:
    """既存カードと1文字も違わない形で作る。in_media_dir=True は pages/media/*.html 用"""
    href = f"../media/{a['slug']}.html" if in_media_dir else f"media/{a['slug']}.html"
    img = ("../../" if in_media_dir else "../") + "images/photos/"
    p, d = a["photo"], a["publish"]
    return (
        f'{ind}<a href="{href}" class="media-card reveal" data-category="{a["cat"]}" data-date="{d}">\n'
        f'{ind}  <div class="thumb thumb--photo">\n'
        f'{ind}    <img src="{img}{p}.jpg" srcset="{img}w/{p}-800.webp 800w, {img}{p}.jpg {a["photo_w"]}w" '
        f'sizes="(max-width: 899px) 90vw, 400px" alt="" width="720" height="450" loading="lazy" decoding="async">\n'
        f'{ind}    <span class="thumb__cat">{a["cat_label"]}</span>\n'
        f'{ind}  </div>\n'
        f'{ind}  <div class="media-card__body">\n'
        f'{ind}    <span class="media-card__cat">{a["cat_label"]}</span>\n'
        f'{ind}    <h3 class="media-card__title">{a["title_html"]}</h3>\n'
        f'{ind}    <time class="media-card__date" datetime="{d}">{d.replace("-", ".")}</time>\n'
        f'{ind}  </div>\n'
        f'{ind}</a>\n'
    )


def grids(s: str, label: str):
    """[(グリッド開始タグの直後の位置, カードのインデント, カードのリスト)]。カードはグリッド直後から隙間なく並ぶ前提"""
    out = []
    for g in GRID_RE.finditer(s):
        pos, cards = g.end(), []
        for m in CARD_RE.finditer(s, pos):
            if m.start() != pos:
                break
            cards.append(m)
            pos = m.end()
        out.append((g.end(), g.group("ind") + "  ", cards))
    return out


def remove_cards(s: str, slug: str, label: str):
    n = 0
    for _, _, cards in reversed(grids(s, label)):
        for m in reversed(cards):
            if m.group("slug") == slug:
                s = s[: m.start()] + s[m.end():]
                n += 1
    return s, n


def insert_cards(s: str, a: dict, in_media_dir: bool, label: str, comes_after) -> (str, int):
    """すべての .media-grid に a のカードを入れる。comes_after(slug) が True の最初のカードの前に入れ、
    なければ末尾に入れる"""
    n = 0
    for start, ind, cards in reversed(grids(s, label)):
        pos = cards[-1].end() if cards else start
        for m in cards:
            if comes_after(m.group("slug")):
                pos = m.start()
                break
        s = s[:pos] + render_card(a, in_media_dir, ind) + s[pos:]
        n += 1
    return s, n


# ---------------------------------------------------------------- 並び順

def related_group(base: dict, other: dict) -> int:
    """0: 同じカテゴリ・サービス共通 / 1: 同じカテゴリ・共通なし / 2: 別カテゴリ・共通 / 3: 別カテゴリ・共通なし"""
    same_cat = other["cat"] == base["cat"]
    shares = bool(set(other["services"]) & set(base["services"]))
    return (0 if same_cat else 2) + (0 if shares else 1)


def sitemap_ranks(smap: str) -> dict:
    return {m.group("slug"): i for i, m in enumerate(SITEMAP_ARTICLE_RE.finditer(smap))}


# ---------------------------------------------------------------- sitemap

def sitemap_update(s: str, slug: str, a=None):
    """slug の行を取り除き、a があれば正しい位置に入れ直す。(新しい本文, 取り除いた数, 入れた数)"""
    removed = 0
    for m in reversed(list(SITEMAP_ARTICLE_RE.finditer(s))):
        if m.group("slug") == slug:
            s = s[: m.start()] + s[m.end():]
            removed += 1
    if a is None:
        return s, removed, 0
    line = f"  <url><loc>{SITE}/media/{slug}.html</loc><lastmod>{a['modified']}</lastmod></url>\n"
    entries = list(SITEMAP_ARTICLE_RE.finditer(s))
    if entries:
        pos = entries[-1].end()
        for m in entries:
            other = m.group("slug")
            try:
                pub = read_article(other)["publish"]
            except ToolError:
                lm = re.search(r"<lastmod>([\d-]+)</lastmod>", m.group(0))
                pub = lm.group(1) if lm else "0000-00-00"
            if pub > a["publish"]:
                pos = m.start()
                break
    else:
        m = list(re.finditer(r"^  <url><loc>" + re.escape(SITE) + r"/media/guide-\w+\.html</loc>.*?</url>\n", s, re.M)) or \
            list(re.finditer(r"^  <url><loc>" + re.escape(SITE) + r"/media\.html</loc>.*?</url>\n", s, re.M))
        if not m:
            raise ToolError("seo/sitemap.xml: 記事を入れる位置（media.html かガイドの行）が見つかりません")
        pos = m[-1].end()
    return s[:pos] + line + s[pos:], removed, 1


# ---------------------------------------------------------------- 検索の索引（js/media-index.js）

def search_index_update(s: str, slug: str, a, rank: dict):
    head, sep, rest = s.partition("window.MEDIA_INDEX = ")
    if not sep or not rest.rstrip().endswith(";"):
        raise ToolError("js/media-index.js: 「window.MEDIA_INDEX = [...];」の形になっていません")
    data = json.loads(rest.rstrip()[:-1])
    before = len(data)
    data = [d for d in data if d.get("slug") != slug]
    removed = before - len(data)
    inserted = 0
    if a is not None:
        entry = {"slug": slug, "title": a["title"], "cat": a["cat_label"], "date": a["publish"],
                 "thumb": a["photo"], "desc": a["desc"], "text": a["text"]}
        pos = len(data)
        for i, d in enumerate(data):
            if desc_comes_after(d["slug"], d["date"], a, rank):
                pos = i
                break
        data.insert(pos, entry)
        inserted = 1
    return head + sep + json.dumps(data, ensure_ascii=False) + ";\n", removed, inserted


def desc_comes_after(other_slug, other_date, a, rank):
    """新しい順のリストで、other が a より後ろに来るか（同じ日は sitemap の順）"""
    if other_date != a["publish"]:
        return other_date < a["publish"]
    return rank.get(other_slug, 10 ** 6) > rank.get(a["slug"], 10 ** 6)


# ---------------------------------------------------------------- 構造化データ

def replace_ld(s: str, type_name: str, fn, label: str) -> str:
    """@type が type_name の JSON-LD を fn(obj) で書き換える（書式は既存と同じ json.dumps）"""
    for m in LD_RE.finditer(s):
        try:
            obj = json.loads(m.group(2))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("@type") == type_name:
            fn(obj)
            return s[: m.start(2)] + json.dumps(obj, ensure_ascii=False) + s[m.end(2):]
    raise ToolError(f"{label}: 構造化データ {type_name} が見つかりません")


def collection_update(s: str) -> str:
    """media.html の CollectionPage の hasPart を「すべての記事」の順に作り直す"""
    i = s.find('id="media-list"')
    if i < 0:
        raise ToolError("pages/media.html: #media-list が見つかりません")
    order = [m.group("slug") for m in CARD_RE.finditer(s, s.rfind("<div", 0, i))]

    def fn(obj):
        obj["hasPart"] = [{"@type": "Article", "headline": read_article(x)["headline"],
                           "url": f"{SITE}/media/{x}.html"} for x in order]
    return replace_ld(s, "CollectionPage", fn, "pages/media.html")


# ---------------------------------------------------------------- ガイド

GUIDE_STEP_RE = re.compile(
    r'(<li class="guide-step[^"]*" data-date=")([\d-]+)(">\s*<a href="\.\./media/)([\w-]+)(\.html")')


def guide_pages(texts: dict):
    """{guide: dict(path, name_html, steps=[slug...])}（texts は作業中の本文）"""
    out = {}
    for g in GUIDES:
        f = MEDIA / f"guide-{g}.html"
        if f not in texts:
            continue
        s = texts[f]
        m = re.search(r'<h1 class="mhero__title[^"]*"[^>]*>(.*?)</h1>', s, re.S)
        out[g] = dict(path=f, name_html=m.group(1) if m else g, steps=[m.group(4) for m in GUIDE_STEP_RE.finditer(s)])
    return out


def render_guide_box(g: str, guide: dict, slug: str) -> str:
    items = []
    for x in guide["steps"]:
        o = read_article(x)
        if x == slug:
            items.append(f'<li data-date="{o["publish"]}" aria-current="page"><span><n-w>{o["title"]}</n-w></span></li>')
        else:
            items.append(f'<li data-date="{o["publish"]}"><a href="../media/{x}.html"><n-w>{o["title"]}</n-w></a></li>')
    i = " " * 8
    return (f'{i}<nav class="guide-box" aria-label="この記事を含むガイド">\n'
            f'{i}  <p class="guide-box__label">この記事を含むガイド</p>\n'
            f'{i}  <a href="../media/guide-{g}.html" class="guide-box__title">{guide["name_html"]}</a>\n'
            f'{i}  <ol class="guide-box__list">{"".join(items)}</ol>\n'
            f'{i}  <div class="guide-box__pager"></div>\n'
            f'{i}</nav>\n\n')


def sync_guides(work: dict, warnings: list):
    """ガイドのページから作られる部分（ItemList・各記事の guide-box・data-date）をそろえる"""
    texts = {f: w[0] for f, w in work.items()}
    guides = guide_pages(texts)
    known = set(article_slugs())

    # ガイドのページ: data-date を記事の公開日に、ItemList をページ上の並びに
    for g, guide in guides.items():
        f = guide["path"]
        s = work[f][0]

        def fix_date(m):
            x = m.group(4)
            return m.group(1) + (read_article(x)["publish"] if x in known else m.group(2)) + "".join(m.group(3, 4, 5))
        s = GUIDE_STEP_RE.sub(fix_date, s)
        for x in guide["steps"]:
            if x not in known:
                warnings.append(f"guide-{g}.html: 記事ファイルがない {x} が載っています（手で外してください）")

        def fn(obj, steps=guide["steps"]):
            obj["itemListElement"] = [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/media/{x}.html"}
                                      for i, x in enumerate(steps)]
        s = replace_ld(s, "ItemList", fn, f.relative_to(ROOT).as_posix())
        work[f][0] = s
        guide["steps"] = [x for x in guide["steps"] if x in known]

    # 各記事の「この記事を含むガイド」
    for x in known:
        f = MEDIA / f"{x}.html"
        a = read_article(x)
        for g in a["guides"]:
            if g in guides and x not in guides[g]["steps"]:
                warnings.append(f"{x}: 「こんな方に」に guide-{g} があるが、guide-{g}.html に載っていない"
                                "（既存の li.guide-step をコピーして手で足し、もう一度実行）")
        for g, guide in guides.items():
            if x in guide["steps"] and g not in a["guides"]:
                warnings.append(f"{x}: guide-{g}.html に載っているが、記事の「こんな方に」に guide-{g} がない")
        g = next((g for g in a["guides"] if g in guides and x in guides[g]["steps"]), None)
        box = render_guide_box(g, guides[g], x) if g else ""
        s = work[f][0]
        m = re.search(r'(<section class="sources">.*?</section>\n\n)(.*?)(        <div class="share">)', s, re.S)
        if not m:
            warnings.append(f"{x}: 参考資料とシェアの間（guide-box の位置）が見つからないため、guide-box を更新しませんでした")
            continue
        new = "\n" + box
        if m.group(2) != new:
            work[f][0] = s[: m.start(2)] + new + s[m.end(2):]

    # media.html の「よくある悩み」の data-date
    f = PAGES / "media.html"
    s = work[f][0]
    work[f][0] = re.sub(r'(<li data-date=")([\d-]+)("><a href="media/([\w-]+)\.html" class="mq__item">)',
                        lambda m: m.group(1) + (read_article(m.group(4))["publish"] if m.group(4) in known else m.group(2)) + m.group(3),
                        s)


# ---------------------------------------------------------------- 本体

def listing_files():
    files = [PAGES / "media.html", PAGES / "index.html"] + sorted(PAGES.glob("service-*.html"))
    return files + sorted(MEDIA.glob("*.html"))


def plan(slug, remove: bool):
    """{Path: (新しい本文, 取り除いた数, 入れた数)} と警告のリストを返す（書き込みはしない）。
    slug が None のときは同期（--sync）だけ"""
    a = None if (remove or slug is None) else read_article(slug)
    warnings = []
    originals = {f: f.read_text(encoding="utf-8") for f in listing_files()}
    originals[SITEMAP] = SITEMAP.read_text(encoding="utf-8")
    originals[SEARCH_INDEX] = SEARCH_INDEX.read_text(encoding="utf-8")
    work = {f: [s, 0, 0] for f, s in originals.items()}

    if slug is not None:
        # 1) sitemap（同じ公開日どうしの順番の基準になるので最初に）
        w = work[SITEMAP]
        w[0], w[1], w[2] = sitemap_update(w[0], slug, a)
        rank = sitemap_ranks(w[0])

        # 2) 全ファイルのカードから取り除く
        for f in listing_files():
            if f.parent == MEDIA and f.stem == slug:
                continue
            w = work[f]
            w[0], n = remove_cards(w[0], slug, f.relative_to(ROOT).as_posix())
            w[1] += n

        # 3) 検索の索引
        w = work[SEARCH_INDEX]
        w[0], r, i = search_index_update(w[0], slug, a, rank)
        w[1] += r
        w[2] += i

    if a is not None:
        # 4) 一覧（新しい順）: media.html・index.html・関連サービス・カテゴリ一覧
        def desc_after(other):
            return desc_comes_after(other, read_article(other)["publish"], a, rank)

        targets = [PAGES / "media.html", PAGES / "index.html"]
        targets += [PAGES / svc for svc in a["services"] if (PAGES / svc).is_file()]
        targets += [MEDIA / f"category-{a['cat']}.html"]
        for svc in a["services"]:
            if not (PAGES / svc).is_file():
                warnings.append(f"関連サービス {svc} のページがありません（カードは入れません）")
        for f in targets:
            w = work[f]
            label = f.relative_to(ROOT).as_posix()
            if not grids(w[0], label):
                raise ToolError(f"{label}: media-grid が見つかりません")
            w[0], n = insert_cards(w[0], a, f.parent == MEDIA, label, desc_after)
            w[2] += n

        # 5) 他の記事の「あわせて読みたい記事」
        others = [x for x in article_slugs() if x != slug]
        big = 10 ** 6
        for x in others:
            base = read_article(x)
            new_key = (related_group(base, a), rank.get(slug, big))

            def rel_after(o, base=base, new_key=new_key):
                return (related_group(base, read_article(o)), rank.get(o, big)) > new_key

            f = MEDIA / f"{x}.html"
            w = work[f]
            w[0], n = insert_cards(w[0], a, True, f.relative_to(ROOT).as_posix(), rel_after)
            w[2] += n

        # 6) 新しい記事自身の「あわせて読みたい記事」を丸ごと作り直す
        own = MEDIA / f"{slug}.html"
        s = work[own][0]
        gl = grids(s, own.relative_to(ROOT).as_posix())
        if len(gl) != 1:
            raise ToolError(f"{own.relative_to(ROOT).as_posix()}: media-grid が {len(gl)} 個あります（1個を想定）")
        start, ind, cards = gl[0]
        end = cards[-1].end() if cards else start
        rel = sorted((read_article(x) for x in others),
                     key=lambda o: (related_group(a, o), rank.get(o["slug"], big)))
        work[own] = [s[:start] + "".join(render_card(o, True, ind) for o in rel) + s[end:], len(cards), len(rel)]

    if slug is not None:
        # 7) media.html の CollectionPage
        work[PAGES / "media.html"][0] = collection_update(work[PAGES / "media.html"][0])

    # 8) ガイドから作られる部分と日付
    sync_guides(work, warnings)

    if remove:
        left = [f.relative_to(PAGES).as_posix() for f, (s, _, _) in sorted(work.items())
                if f.suffix == ".html" and f.stem != slug
                and re.search(r'href="(?:\.\./)?media/' + re.escape(slug) + r'\.html"', s)]
        hubs = [x for x in left if x == "media.html" or x.startswith("media/guide-")]
        if left:
            warnings.append(
                f"{slug} へのリンクが {len(left)} ファイルに残っています（ガイド・「よくある悩み」・本文中のリンク・"
                "ガイドから作る「この記事を含むガイド」）。記事を残すなら問題なし。記事を消すなら、"
                f"まず {', '.join(hubs) or 'ガイド'} と本文のリンクを手で外し、--sync を実行する: {', '.join(left)}")

    out = {}
    for f, (s, r, i) in work.items():
        if s != originals[f]:
            out[f] = (s, r, i)
    return out, warnings


def main():
    ap = argparse.ArgumentParser(description="アキヤドの記事カード・検索の索引・sitemap・llms.txt を更新する")
    ap.add_argument("slug", nargs="?", help="追加する記事のスラッグ（pages/media/<slug>.html）")
    ap.add_argument("--remove", metavar="SLUG", help="このスラッグのカード・索引・sitemap 登録を取り除く")
    ap.add_argument("--sync", action="store_true", help="追加・削除はせず、ガイドから作られる部分と日付だけをそろえる")
    ap.add_argument("--dry-run", action="store_true", help="変更するファイルと件数だけ表示する")
    ap.add_argument("--no-llms", action="store_true", help="seo/llms.txt を作り直さない")
    ap.add_argument("--today", help="llms.txt の判定日 YYYY-MM-DD（既定は日本時間の今日）")
    args = ap.parse_args()
    if sum(map(bool, (args.slug, args.remove, args.sync))) != 1:
        ap.error("<slug>、--remove <slug>、--sync のどれか1つを指定してください")
    slug = args.remove or args.slug
    if slug and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        ap.error(f"スラッグの形式が不正です: {slug}")
    if slug and (slug.startswith(("guide-", "category-")) or slug == "search"):
        ap.error(f"{slug} は記事ではありません（ガイド・カテゴリ一覧・検索のページ）")

    from build_llms import today_jst
    try:
        changes, warnings = plan(slug, remove=bool(args.remove))
        if args.slug:
            a = read_article(slug)
            print(f"{'追加' if not args.dry_run else '追加（dry-run）'}: {slug} ／ {a['cat_label']} ／ 公開日 {a['publish']}"
                  f" ／ 更新日 {a['modified']} ／ 写真 {a['photo']} ／ 関連サービス {', '.join(a['services']) or 'なし'}"
                  f" ／ ガイド {', '.join(a['guides']) or 'なし'}")
            today = args.today or today_jst()
            if a["publish"] < today:
                print(f"注意: 公開日 {a['publish']} が今日（{today}）より前です。新しい記事なら、公開日をさかのぼって付けていないか確認してください。")
        elif args.remove:
            print(f"{'削除' if not args.dry_run else '削除（dry-run）'}: {slug}")
        else:
            print(f"同期{'（dry-run）' if args.dry_run else ''}: ガイド・日付")
    except ToolError as e:
        sys.exit(f"エラー: {e}")

    for w in warnings:
        print(f"警告: {w}", file=sys.stderr)
    if not changes:
        print("カード・索引・sitemap: 変更なし（すでにルールどおり）")
    for f in sorted(changes, key=lambda p: p.as_posix()):
        s, r, i = changes[f]
        print(f"  {f.relative_to(ROOT).as_posix()}: 取り除き {r} ／ 挿入 {i}")
        if not args.dry_run:
            f.write_text(s, encoding="utf-8")
    print(f"変更ファイル数: {len(changes)}" + ("（dry-run・書き込みなし）" if args.dry_run else ""))

    if not args.no_llms:
        import build_llms
        build_llms.write(args.today, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
