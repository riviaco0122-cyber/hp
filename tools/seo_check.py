#!/usr/bin/env python3
"""サイト全体の SEO / AIO を機械的にチェックする（品質管理部・エンジニア部が使う）。

使い方:
  python3 tools/seo_check.py            # Markdown のレポートを表示
  python3 tools/seo_check.py --json     # JSON で出力（ダッシュボード生成用）

終了コード: エラーが 1 件でもあれば 1、警告だけなら 0。
外部ライブラリは使わない（標準ライブラリのみ）。
"""
import datetime
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
SITE = "https://rivia-co.com"
TITLE_SUFFIX = " | 合同会社RIVIA&CO."
TODAY = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()  # 日本時間

# 日本語の目安（Google の検索結果で切れにくい長さ）
TITLE_MAX = 40          # サフィックスを除いたタイトルの文字数
DESC_MIN, DESC_MAX = 50, 140


def public_path(file: Path) -> str:
    """pages/ 以下のファイル → 公開URLのパス（vercel.json の rewrites と対応）"""
    rel = file.relative_to(PAGES).as_posix()
    return "/" + rel


def resolve_file(path: str):
    """公開URLのパス → リポジトリ内のファイル。見つからなければ None"""
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return PAGES / "index.html"
    if path in ("/robots.txt", "/sitemap.xml"):
        return ROOT / "seo" / path.lstrip("/")
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
        self.h1 = 0
        self.h1_text = []
        self.imgs_no_alt = []
        self.ldjson = []
        self._buf = []
        self.article_publish = None
        self.times = []          # (label_context, datetime)
        self._last_text = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in = "title"
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
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

    def handle_endtag(self, tag):
        if tag == "script" and self._in == "ld":
            self.ldjson.append("".join(self._buf))
            self._in = None
        elif tag in ("title", "h1"):
            self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "h1":
            self.h1_text.append(data)
        elif self._in == "ld":
            self._buf.append(data)
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


def check():
    issues = []  # dict(level, page, msg)
    articles = []

    def add(level, page, msg):
        issues.append({"level": level, "page": page, "msg": msg})

    sitemap = load_sitemap()
    seen_titles, seen_descs = {}, {}
    indexable_urls = set()

    for file in sorted(PAGES.rglob("*.html")):
        pp = public_path(file)
        page_url = SITE + pp
        p = PageParser()
        p.feed(file.read_text(encoding="utf-8"))
        robots = p.meta.get("robots", "")
        noindex = "noindex" in robots
        expected_canonical = SITE + "/" if pp == "/index.html" else page_url
        if not noindex:
            indexable_urls.add(expected_canonical)

        # タイトル
        title = p.title.strip()
        core = title.replace(TITLE_SUFFIX, "")
        if not title:
            add("error", pp, "title がない")
        elif len(core) > TITLE_MAX and not noindex:
            add("warn", pp, f"title が長い（{len(core)}文字・目安{TITLE_MAX}文字以内）: {core}")
        if title and not noindex:
            if title in seen_titles:
                add("error", pp, f"title が {seen_titles[title]} と重複")
            seen_titles[title] = pp

        # meta description
        desc = p.meta.get("description", "").strip()
        if not desc and not noindex:
            add("error", pp, "meta description がない")
        elif desc and not noindex:
            if not (DESC_MIN <= len(desc) <= DESC_MAX):
                add("warn", pp, f"meta description の長さ {len(desc)}文字（目安{DESC_MIN}〜{DESC_MAX}）")
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

        # 見出し
        if p.h1 != 1:
            add("error", pp, f"h1 が {p.h1} 個（1個にする）")

        # 画像の alt
        for src in p.imgs_no_alt:
            add("error", pp, f"alt 属性がない画像: {src}")

        # 構造化データ
        types = []
        ld_objs = []
        for raw in p.ldjson:
            try:
                obj = json.loads(raw)
                ld_objs.append(obj)
                types.append(obj.get("@type"))
            except json.JSONDecodeError as e:
                add("error", pp, f"構造化データ(JSON-LD)の書式エラー: {e}")

        # 内部リンク切れ
        for tag, href in p.links:
            if href.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
                continue
            absu = urljoin(page_url, href)
            u = urlparse(absu)
            if u.netloc != urlparse(SITE).netloc:
                continue
            if resolve_file(u.path) is None:
                add("error", pp, f"リンク切れ: {href}")

        # 記事ページ固有
        if pp.startswith("/media/"):
            art = next((o for o in ld_objs if o.get("@type") == "Article"), None)
            for t in ("Article", "BreadcrumbList"):
                if t not in types:
                    add("error", pp, f"構造化データ {t} がない")
            if "FAQPage" not in types:
                add("warn", pp, "構造化データ FAQPage がない（AIO向けに推奨）")
            if 'class="keypoints' not in file.read_text(encoding="utf-8"):
                add("warn", pp, "「この記事のポイント」がない（AIO向けに推奨）")
            pub = art.get("datePublished") if art else None
            mod = art.get("dateModified") if art else None
            if art and p.article_publish and pub != p.article_publish:
                add("error", pp, f"data-publish({p.article_publish}) と datePublished({pub}) が不一致")
            shown = dict(p.times)
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

    # sitemap の網羅性
    for url in sorted(indexable_urls - set(sitemap)):
        add("error", "seo/sitemap.xml", f"sitemap に未登録: {url}")
    for url in sorted(set(sitemap) - indexable_urls):
        add("error", "seo/sitemap.xml", f"sitemap にあるが存在しない/noindex: {url}")

    # AIO 用ファイル
    if resolve_file("/llms.txt") is None:
        add("warn", "(site)", "llms.txt がない（AI検索向けのサイト案内。推奨）")

    return issues, articles


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
