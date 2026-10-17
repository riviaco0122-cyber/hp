#!/usr/bin/env python3
"""サイト全体の SEO / AIO を機械的にチェックする（品質管理部・エンジニア部が使う）。

使い方:
  python3 tools/seo_check.py            # Markdown のレポートを表示
  python3 tools/seo_check.py --json     # JSON で出力（ダッシュボード生成用）

終了コード: エラーが 1 件でもあれば 1、警告だけなら 0。
外部ライブラリは使わない（標準ライブラリのみ）。

pages/・seo/ は tools/build.py が作る。エラーが出たら HTML ではなく build.py・記事データ（tools/articles_*.py）を直して作り直す。
vercel.json の redirects（英語版 /en/ → /、旧カテゴリ → 新テーマ）をたどってリンク先を判定する。
表示の確認（JS エラー・画像・はみ出し・見た目の変化）は node tools/check/site_check.js で行う。
"""
import datetime
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
SITE = "https://rivia-co.com"
# title の末尾に付くサイト名（長さの判定では除く）
TITLE_SUFFIXES = (" | 合同会社RIVIA&CO.", " | アキヤド", "｜アキヤド")
TITLE_SUFFIX = TITLE_SUFFIXES[0]  # 互換のため残す
TODAY = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()  # 日本時間

# 日本語の目安（Google の検索結果で切れにくい長さ）
TITLE_MAX = 40          # サフィックスを除いたタイトルの文字数
DESC_MIN, DESC_MAX = 50, 140
# 英語ページ（<html lang="en">）の目安。英語は半角なので、タイトル全体で 60 字・説明 160 字程度
TITLE_MAX_EN = 60       # サフィックス込みのタイトル全体の文字数
DESC_MIN_EN, DESC_MAX_EN = 50, 160

# アキヤドの title の「｜」より前に入れたい主題の語
TOPIC_WORDS = ("民泊", "空き家", "空家", "宿", "旅館", "簡易宿所", "実家", "古民家", "別荘", "インバウンド", "観光")

# 記事の構造化データとして扱う型
ARTICLE_TYPES = ("Article", "BlogPosting", "NewsArticle")
# 公開フォルダ直下に置かれ、pages/ の外にある HTML（Vercel が直接配信する）
ROOT_HTML = ("404.html",)


def load_redirects():
    """vercel.json の redirects（source → destination）。:file のような名前つきの部分は正規表現にする"""
    f = ROOT / "vercel.json"
    if not f.is_file():
        return []
    try:
        conf = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    out = []
    for r in conf.get("redirects", []):
        src, dst = r.get("source", ""), r.get("destination", "")
        names = re.findall(r":(\w+)", src)
        pat = "^" + re.sub(r":(\w+)", lambda m: f"(?P<{m.group(1)}>[^/]+)", re.escape(src).replace("\\:", ":")) + "$"
        out.append((re.compile(pat), dst, names))
    return out


REDIRECTS = load_redirects()


def redirect_target(path: str):
    """公開URLのパスが vercel.json の redirects で転送されるなら、転送先のパス。されなければ None"""
    for pat, dst, names in REDIRECTS:
        m = pat.match(path)
        if m:
            for n in names:
                dst = dst.replace(":" + n, m.group(n))
            return dst
    return None


def public_path(file: Path) -> str:
    """pages/ 以下のファイル → 公開URLのパス（vercel.json の rewrites と対応）。
    リポジトリ直下の 404.html などは、そのまま /404.html"""
    if file.parent == ROOT:
        return "/" + file.name
    rel = file.relative_to(PAGES).as_posix()
    return "/" + rel


def canonical_path(pp: str) -> str:
    """公開URLのパス → canonical にすべきパス。
    / と /en/ は vercel.json で pages/index.html・pages/en/index.html に対応づけている"""
    if pp == "/index.html":
        return "/"
    if pp == "/en/index.html":
        return "/en/"
    return pp


def page_kind(pp: str, ld_types, has_publish: bool) -> str:
    """ページの種類: article（記事）/ media（記事以外のメディアページ）/ page（会社サイト）"""
    if any(t in ARTICLE_TYPES for t in ld_types) or (pp.startswith("/media/") and has_publish):
        return "article"
    if pp == "/media.html" or pp.startswith("/media/"):
        return "media"
    return "page"


def ld_type_list(obj):
    """JSON-LD の最上位の型を平らなリストで返す（配列・@graph・@type の配列にも対応）"""
    out = []
    items = obj if isinstance(obj, list) else obj.get("@graph", [obj]) if isinstance(obj, dict) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        t = it.get("@type")
        out.extend(t if isinstance(t, list) else [t])
    return [t for t in out if t]


def ld_find(objs, types):
    """JSON-LD の中から最初に見つかった types の型のオブジェクト"""
    for obj in objs:
        items = obj if isinstance(obj, list) else obj.get("@graph", [obj]) if isinstance(obj, dict) else []
        for it in items:
            if isinstance(it, dict):
                t = it.get("@type")
                ts = t if isinstance(t, list) else [t]
                if any(x in types for x in ts):
                    return it
    return None


def resolve_file(path: str):
    """公開URLのパス → リポジトリ内のファイル。見つからなければ None"""
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return PAGES / "index.html"
    dst = redirect_target(path)  # vercel.json の redirects（例: 英語版 /en/ → /、旧カテゴリ → 新テーマ）
    if dst is not None and dst != path:
        return resolve_file(dst)
    if path in ("/robots.txt", "/sitemap.xml", "/llms.txt"):  # vercel.json で /seo/ に対応づけ
        cand = ROOT / "seo" / path.lstrip("/")
        return cand if cand.is_file() else None
    for cand in (PAGES / path.lstrip("/"), ROOT / path.lstrip("/")):
        if cand.is_file():
            return cand
    return None


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in = None
        self.meta = {}
        self.links = []          # (tag, attr, value)
        self.canonical = None
        self.alternates = []     # (hreflang, href)
        self.lang = ""
        self.h1 = 0
        self.h1_text = []
        self.imgs_no_alt = []
        self.ldjson = []
        self._buf = []
        self.article_publish = None
        self.times = []          # (label_context, datetime)
        self._last_text = ""
        self.faq_q = []          # 画面のよくある質問（<summary class="faq__q">）の文
        self._faq_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in = "title"
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.alternates.append((a["hreflang"], a.get("href", "")))
        elif tag == "h1":
            self.h1 += 1
            self._in = "h1"
        elif tag == "img":
            if "alt" not in a:
                self.imgs_no_alt.append(a.get("src", "?"))
            if a.get("src"):
                self.links.append(("img", a["src"]))
        elif tag == "a" and a.get("href"):
            self.links.append(("a", a["href"]))
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
            self._buf = []
        elif tag == "article" and "data-publish" in a:
            self.article_publish = a["data-publish"]
        elif tag == "time" and a.get("datetime"):
            self.times.append((self._last_text.strip(), a["datetime"]))
        if tag == "summary" and "faq__q" in (a.get("class") or "").split():
            self._faq_depth = 1
            self.faq_q.append("")
        elif self._faq_depth and tag == "span" and "faq__mark" in (a.get("class") or "").split():
            self._faq_depth = 2  # 「Q」の印は質問の文に含めない

    def handle_endtag(self, tag):
        if tag == "script" and self._in == "ld":
            self.ldjson.append("".join(self._buf))
            self._in = None
        elif tag in ("title", "h1"):
            self._in = None
        if tag == "summary":
            self._faq_depth = 0
        elif tag == "span" and self._faq_depth == 2:
            self._faq_depth = 1

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "h1":
            self.h1_text.append(data)
        elif self._in == "ld":
            self._buf.append(data)
        if self._faq_depth == 1:
            self.faq_q[-1] += data
        if data.strip():
            self._last_text = data


def load_sitemap():
    tree = ET.parse(ROOT / "seo" / "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    out = {}
    for url in tree.getroot().findall("s:url", ns):
        loc = url.find("s:loc", ns).text.strip()
        lm = url.find("s:lastmod", ns)
        out[loc] = lm.text.strip() if lm is not None else None
    return out


def html_files():
    """チェック対象: pages/ 以下の全 HTML と、リポジトリ直下の 404.html など"""
    files = sorted(PAGES.rglob("*.html"))
    files += [ROOT / n for n in ROOT_HTML if (ROOT / n).is_file()]
    return files


def media_list_slugs():
    """media.html の #media-list（すべての記事）に載っている記事の slug"""
    f = PAGES / "media.html"
    if not f.is_file():
        return None
    s = f.read_text(encoding="utf-8")
    i = s.find('id="media-list"')
    if i < 0:
        return None
    end = s.find("</section>", i)
    return re.findall(r'<a href="media/([\w-]+)\.html" class="media-card', s[i:end])


def search_index_slugs():
    """js/media-index.js（記事検索の索引）に載っている slug。ファイルが無ければ None"""
    f = ROOT / "js" / "media-index.js"
    if not f.is_file():
        return None
    s = f.read_text(encoding="utf-8")
    try:
        data = json.loads(s[s.index("["): s.rindex("]") + 1])
    except (ValueError, json.JSONDecodeError):
        return []
    return [d.get("slug") for d in data if isinstance(d, dict)]


def check():
    issues = []  # dict(level, page, msg)
    articles = []

    def add(level, page, msg):
        issues.append({"level": level, "page": page, "msg": msg})

    sitemap = load_sitemap()
    seen_titles, seen_descs = {}, {}
    indexable_urls, noindex_urls = set(), set()
    alternates = {}  # canonical URL → {hreflang: href}

    for file in html_files():
        pp = public_path(file)
        text = file.read_text(encoding="utf-8")
        p = PageParser()
        p.feed(text)
        robots = p.meta.get("robots", "")
        noindex = "noindex" in robots
        english = p.lang.lower().startswith("en")
        expected_canonical = SITE + canonical_path(pp)
        if redirect_target(pp) is not None:
            add("error", pp, f"vercel.json の redirects で {redirect_target(pp)} へ転送されるため、このページは表示されない（不要なら消す。英語版は公開をやめた）")
        if noindex:
            noindex_urls.add(expected_canonical)
        elif p.article_publish and p.article_publish > TODAY:
            pass  # 公開日前の記事は sitemap に載せない（公開日を迎えてから作り直すと載る）
        else:
            indexable_urls.add(expected_canonical)

        # 構造化データ（先に読んで、ページの種類を決める）
        types = []
        ld_objs = []
        for raw in p.ldjson:
            try:
                obj = json.loads(raw)
                ld_objs.append(obj)
                types.extend(ld_type_list(obj))
            except json.JSONDecodeError as e:
                add("error", pp, f"構造化データ(JSON-LD)の書式エラー: {e}")
        kind = page_kind(pp, types, bool(p.article_publish))

        # タイトル（日本語はサイト名を除いて 40 字、英語はタイトル全体で 60 字が目安）
        title = p.title.strip()
        core = title
        for suf in TITLE_SUFFIXES:
            if core.endswith(suf):
                core = core[: -len(suf)]
                break
        if not title:
            add("error", pp, "title がない")
        elif not noindex:
            if english and len(title) > TITLE_MAX_EN:
                add("warn", pp, f"title が長い（{len(title)}字・英語の目安{TITLE_MAX_EN}字以内）: {title}")
            elif not english and len(core) > TITLE_MAX:
                add("warn", pp, f"title が長い（{len(core)}文字・目安{TITLE_MAX}文字以内）: {core}")
        # アキヤドの記事・一覧：検索結果でタイトルだけ見ても何の話か分かるよう、「｜」より前に主題の語を入れる（playbook 2章）
        if title and not noindex and pp.startswith("/media/") and not english:
            head = core.split("｜")[0].split(" | ")[0]
            # 会社・プラン・お問い合わせなど「アキヤド」の名前で探されるページは除く
            if "アキヤド" not in head and not pp.endswith(("/contact.html", "/thanks.html")) and not any(w in head for w in TOPIC_WORDS):
                add("warn", pp, f"title の「｜」より前に、民泊・空き家・宿などの主題の語がない（検索結果で何の話か伝わりにくい）: {core}")
        if title and not noindex:
            if title in seen_titles:
                add("error", pp, f"title が {seen_titles[title]} と重複")
            seen_titles[title] = pp

        # meta description
        desc = p.meta.get("description", "").strip()
        dmin, dmax = (DESC_MIN_EN, DESC_MAX_EN) if english else (DESC_MIN, DESC_MAX)
        if not desc and not noindex:
            add("error", pp, "meta description がない")
        elif desc and not noindex:
            if not (dmin <= len(desc) <= dmax):
                add("warn", pp, f"meta description の長さ {len(desc)}文字（{'英語の' if english else ''}目安{dmin}〜{dmax}）")
            if desc in seen_descs:
                add("error", pp, f"meta description が {seen_descs[desc]} と重複")
            seen_descs[desc] = pp

        # canonical / OGP
        if not noindex:
            if not p.canonical:
                add("error", pp, "canonical がない")
            elif p.canonical != expected_canonical:
                add("error", pp, f"canonical が想定と違う: {p.canonical}（想定 {expected_canonical}）")
            if p.meta.get("og:url") and p.canonical and p.meta["og:url"] != p.canonical:
                add("warn", pp, "og:url と canonical が一致しない")
            for k in ("og:title", "og:description", "og:image"):
                if k not in p.meta:
                    add("warn", pp, f"{k} がない")

        # hreflang（日本語版と英語版の対応）
        if p.alternates:
            alternates[expected_canonical] = dict(p.alternates)
            for lang, href in p.alternates:
                u = urlparse(href)
                if u.netloc != urlparse(SITE).netloc or resolve_file(u.path) is None:
                    add("error", pp, f"hreflang={lang} の URL が存在しない: {href}")

        # よくある質問: 画面の質問と構造化データ FAQPage の質問を一致させる
        faq_ld = ld_find(ld_objs, ("FAQPage",))
        if faq_ld is not None or p.faq_q:
            norm = lambda x: re.sub(r"\s+", "", x or "")
            shown_q = [norm(q) for q in p.faq_q]
            ld_q = [norm(q.get("name")) for q in (faq_ld or {}).get("mainEntity", []) if isinstance(q, dict)]
            if faq_ld is not None and shown_q != ld_q:
                add("error", pp, f"画面のよくある質問（{len(shown_q)}問）と構造化データ FAQPage（{len(ld_q)}問）の質問が一致しない")

        # 見出し
        if p.h1 != 1:
            add("error", pp, f"h1 が {p.h1} 個（1個にする）")

        # 画像の alt
        for src in p.imgs_no_alt:
            add("error", pp, f"alt 属性がない画像: {src}")

        # 内部リンク切れ
        relative_links = 0
        for tag, href in p.links:
            if href.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
                continue
            absu = urljoin(page_url_of(pp), href)
            u = urlparse(absu)
            if u.netloc != urlparse(SITE).netloc:
                continue
            if not urlparse(href).netloc and not href.startswith("/"):
                relative_links += 1
            if resolve_file(u.path) is None:
                add("error", pp, f"リンク切れ: {href}")
            elif redirect_target(u.path) is not None:
                add("warn", pp, f"転送（リダイレクト）されるURLへのリンク: {href} → {redirect_target(u.path)}（転送先に直す）")
        if pp == "/404.html" and relative_links:
            # 404 ページはどの階層の URL でも表示されるので、相対リンクだと階層によって切れる
            add("warn", pp, f"相対パスのリンク・画像が {relative_links} 件（404 ページは / から始まるパスにする）")

        if kind == "article":
            check_article(add, pp, page_url_of(pp), text, p, ld_objs, types, sitemap, articles, core)
        elif kind == "media" and not noindex:
            check_media_page(add, pp, text, ld_objs, types)

    # sitemap の網羅性（noindex のページは載せない）
    for url in sorted(indexable_urls - set(sitemap)):
        add("error", "seo/sitemap.xml", f"sitemap に未登録: {url}")
    for url in sorted(set(sitemap) - indexable_urls):
        if url in noindex_urls:
            add("error", "seo/sitemap.xml", f"noindex のページが sitemap に載っている: {url}")
        else:
            add("error", "seo/sitemap.xml", f"sitemap にあるが存在しない: {url}")

    # hreflang の相互参照（日本語版 ⇄ 英語版）
    for url, alts in sorted(alternates.items()):
        for lang, href in alts.items():
            if lang == "x-default" or href == url:
                continue
            back = alternates.get(href)
            if back is not None and url not in back.values():
                add("warn", url.replace(SITE, ""), f"hreflang={lang} の相手（{href}）からこのページへの hreflang がない")

    # 記事の登録先（一覧・検索の索引）
    art_slugs = {a["path"].rsplit("/", 1)[-1][:-5] for a in articles}
    listed = media_list_slugs()
    if listed is not None:
        for slug in sorted(art_slugs - set(listed)):
            add("error", "/media.html", f"記事 {slug} が「すべての記事」(#media-list) にない（python3 tools/build.py で作り直す）")
        for slug in sorted(set(listed) - art_slugs):
            add("error", "/media.html", f"「すべての記事」に、記事ファイルがない {slug} のカードがある")
    indexed = search_index_slugs()
    if indexed is not None:
        for slug in sorted(art_slugs - set(indexed)):
            add("warn", "js/media-index.js", f"記事 {slug} が検索の索引にない（python3 tools/build.py で作り直す）")
        for slug in sorted(set(indexed) - art_slugs):
            add("error", "js/media-index.js", f"検索の索引に、記事ファイルがない {slug} がある")

    # 記事の掲載先（ガイド・体系的に学ぶ）。tools/build.py の記事データ guides= と MEDIA_COURSES から作られる
    guide_text = "".join(f.read_text(encoding="utf-8") for f in sorted(PAGES.glob("media/guide-*.html")))
    learn = PAGES / "media" / "learn.html"
    learn_text = learn.read_text(encoding="utf-8") if learn.is_file() else None
    for slug in sorted(art_slugs):
        if guide_text and f"media/{slug}.html" not in guide_text:
            add("warn", f"/media/{slug}.html", "どのガイドにも入っていない（「こんな方に」が出ない。記事データの guides= で配置する）")
        if learn_text is not None and f"media/{slug}.html" not in learn_text:
            add("warn", f"/media/{slug}.html", "「体系的に学ぶ」（learn.html）のどの章にも入っていない（tools/build.py の MEDIA_COURSES に足す）")

    # AIO 用ファイル（llms.txt: 公開日を迎えた記事だけを載せる。tools/build.py の llms_txt() が作る）
    llms = resolve_file("/llms.txt")
    if llms is None:
        add("warn", "(site)", "llms.txt がない（AI検索向けのサイト案内。推奨）")
    else:
        ltext = llms.read_text(encoding="utf-8")
        lurls = re.findall(r"\]\((https?://[^)\s]+)\)", ltext)
        for u in lurls:
            pu = urlparse(u)
            if pu.netloc == urlparse(SITE).netloc and resolve_file(pu.path) is None:
                add("error", "seo/llms.txt", f"リンク切れ: {u}")
        listed_l = {u.rsplit("/", 1)[-1][:-5] for u in lurls if "/media/" in u}
        for a in articles:
            slug = a["path"].rsplit("/", 1)[-1][:-5]
            if not a["published"]:
                continue
            if a["published"] <= TODAY and slug not in listed_l:
                add("warn", "seo/llms.txt", f"公開済みの記事 {slug} が llms.txt にない（python3 tools/build.py で作り直す）")
            elif a["published"] > TODAY and slug in listed_l:
                add("warn", "seo/llms.txt", f"公開日前（{a['published']}）の記事 {slug} が llms.txt に載っている")

    return issues, articles


def page_url_of(pp: str) -> str:
    return SITE + pp


def check_article(add, pp, page_url, text, p, ld_objs, types, sitemap, articles, core):
    """記事ページ（Article の構造化データを持つ pages/media/*.html）"""
    art = ld_find(ld_objs, ARTICLE_TYPES)
    for t in ("Article", "BreadcrumbList"):
        if t == "Article" and art is not None:
            continue
        if t not in types:
            add("error", pp, f"構造化データ {t} がない")
    if "FAQPage" not in types:
        add("warn", pp, "構造化データ FAQPage がない（AIO向けに推奨）")
    if 'class="keypoints' not in text:
        add("warn", pp, "「この記事のポイント」がない（AIO向けに推奨）")
    pub = art.get("datePublished") if art else None
    mod = art.get("dateModified") if art else None
    if not p.article_publish:
        add("error", pp, "<article data-publish=\"YYYY-MM-DD\"> がない（予約公開の判定に使う）")
    elif art and pub != p.article_publish:
        add("error", pp, f"data-publish({p.article_publish}) と datePublished({pub}) が不一致")
    shown = dict(p.times)
    if pub and shown.get("公開日") and shown["公開日"] != pub:
        add("error", pp, f"表示の公開日({shown['公開日']}) と datePublished({pub}) が不一致")
    if mod and shown.get("更新日") and shown["更新日"] != mod:
        add("error", pp, f"表示の更新日({shown['更新日']}) と dateModified({mod}) が不一致")
    if pub and pub > TODAY and page_url in sitemap:
        add("warn", pp, f"公開日前（{pub}）なのに sitemap に載っている（AIクローラーには本文も見えている）")
    if page_url in sitemap and mod and sitemap[page_url] != mod:
        add("warn", pp, f"sitemap の lastmod({sitemap[page_url]}) が dateModified({mod}) と違う")
    articles.append({
        "path": pp,
        "title": art.get("headline") if art else core,
        "category": art.get("articleSection") if art else "",
        "published": pub,
        "modified": mod,
    })


def check_media_page(add, pp, text, ld_objs, types):
    """記事以外のメディアページ（メディアのトップ・ガイド・カテゴリ一覧）。
    Article・FAQPage・「この記事のポイント」は求めない。種類ごとに、いまのファイルに入っている構造化データを確認する"""
    name = pp.rsplit("/", 1)[-1]
    if pp == "/media.html":
        for t in ("WebSite", "CollectionPage"):
            if t not in types:
                add("warn", pp, f"構造化データ {t} がない（メディアのトップに推奨）")
        col = ld_find(ld_objs, ("CollectionPage",))
        listed = media_list_slugs()
        if col is not None and listed is not None:
            parts = [h.get("url", "").rsplit("/", 1)[-1][:-5] for h in col.get("hasPart", []) if isinstance(h, dict)]
            if parts != listed:
                add("warn", pp, "CollectionPage の hasPart が「すべての記事」の記事・並び順と一致しない")
    elif name.startswith("guide-"):
        if "ItemList" not in types:
            add("warn", pp, "構造化データ ItemList がない（ガイドの記事の並びを伝える）")
        else:
            il = ld_find(ld_objs, ("ItemList",))
            urls = [e.get("url", "") for e in il.get("itemListElement", []) if isinstance(e, dict)]
            steps = re.findall(r'<li class="guide-step[^"]*"[^>]*>\s*<a href="\.\./media/([\w-]+)\.html"', text)
            if [u.rsplit("/", 1)[-1][:-5] for u in urls] != steps:
                add("warn", pp, "ItemList の並びがページ上のガイドの記事の並びと一致しない")
        if "BreadcrumbList" not in types:
            add("warn", pp, "構造化データ BreadcrumbList がない（画面にはパンくずがある。検索結果での現在地の表示に推奨）")
    elif name.startswith("category-"):
        if "BreadcrumbList" not in types:
            add("warn", pp, "構造化データ BreadcrumbList がない")
    elif not types:
        add("warn", pp, "構造化データがない")


def main():
    issues, articles = check()
    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    if "--json" in sys.argv:
        print(json.dumps({"errors": errors, "warnings": warns, "articles": articles},
                         ensure_ascii=False, indent=1))
    else:
        print(f"# SEOチェック結果\n\nエラー {len(errors)} 件 ／ 警告 {len(warns)} 件 ／ 記事 {len(articles)} 本\n")
        for label, rows in (("エラー（必ず直す）", errors), ("警告（改善候補）", warns)):
            if rows:
                print(f"## {label}\n")
                for r in rows:
                    print(f"- `{r['page']}` {r['msg']}")
                print()
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
