#!/usr/bin/env python3
"""記事カードの組み込みツール（暮らす旅の手帖）。エンジニア部が記事の追加・削除のたびに使う。

使い方:
  python3 tools/add_article.py <slug>              # 記事を組み込む（追加。既にあれば作り直す）
  python3 tools/add_article.py <slug> --dry-run    # 変更するファイルと件数だけ表示（書き込まない）
  python3 tools/add_article.py --remove <slug>     # カード・sitemap・llms.txt から取り除く
  python3 tools/add_article.py --remove <slug> --dry-run
  オプション: --no-llms（llms.txt を作り直さない）、--today YYYY-MM-DD（llms.txt の判定日。テスト用）

前提:
  pages/media/<slug>.html が、同じカテゴリの既存記事をコピーして作成済みであること。
  このツールは記事ファイルから次の情報を読み取る（どれかが欠けるとエラーで止まる）。
    - カテゴリ     : <a href="../media.html?cat=XXX" class="tag article__cat">ラベル</a>
    - タイトル     : <h1 class="article__title">…</h1> の中身（<wbr> もそのままカードに使う）
    - 公開日       : <article class="article" data-publish="YYYY-MM-DD">（Article の datePublished と一致が必要）
    - 更新日       : Article の dateModified（sitemap の lastmod に使う）
    - サムネイル   : og:image のファイル名 → images/photos/thumb/<同じファイル名>（無ければエラー）
    - 関連サービス : <aside class="article-cta"> 内の ../service-*.html へのリンク

組み込み先とルール（既存28本の全カードから検証して決めたもの。往復テストで元のHTMLと完全一致を確認済み）:
  1. pages/media.html の #media-list と pages/index.html: 全記事。公開日の新しい順。
  2. pages/service-*.html: 記事の article-cta に載っているサービスのページだけ。公開日の新しい順。
  3. 各記事の「あわせて読みたい記事」: 自分以外の全記事。次の4グループの順に並べ、
     各グループ内は公開日の古い順。
       (0) 同じカテゴリ かつ 関連サービス（article-cta）が1つ以上共通
       (1) 同じカテゴリ だが 関連サービスの共通なし
       (2) 別のカテゴリ だが 関連サービスが1つ以上共通
       (3) 別のカテゴリ かつ 関連サービスの共通なし
     新しい記事自身の「あわせて読みたい記事」も、このルールで丸ごと作り直す（コピー元の一覧は捨てる）。
  4. 同じ公開日の記事どうしの順番は、media.html に載っている順（どのリストでも同じ）。
     新しく加える記事は、同じ公開日の既存記事の後ろに入る。
     （注意: 既存の 2026-09-29 の7本は、取り除いて入れ直すと同日グループの末尾に移る）
  5. seo/sitemap.xml: 記事の行を公開日の古い順に並べ、lastmod は dateModified。
     同じ公開日の記事の後ろに入る。
  6. seo/llms.txt: tools/build_llms.py で丸ごと作り直す（公開日を迎えた記事だけが載る）。

何度実行しても結果は同じ（追加は「いったん全ファイルから取り除いてから、正しい位置に入れる」ため、重複しない）。
タイトル・カテゴリ・サムネイル・関連サービスを直したときも、同じコマンドを再実行すれば全カードが更新される。

このツールが更新しないもの（手で更新する）:
  - docs/site-spec.md の「掲載記事」と「公開スケジュール」
  - 記事本文中の他記事へのリンク
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
MEDIA = PAGES / "media"
SITEMAP = ROOT / "seo" / "sitemap.xml"
THUMBS = ROOT / "images" / "photos" / "thumb"
SITE = "https://rivia-co.com"

GRID_RE = re.compile(r'<div class="media-grid[^"]*"[^>]*>\n')
CARD_RE = re.compile(
    r'^          <a href="(?:\.\./)?media/(?P<slug>[\w-]+)\.html" class="media-card[^"]*" '
    r'data-category="(?P<cat>\w+)" data-date="(?P<date>[\d-]+)">\n.*?^          </a>\n',
    re.M | re.S,
)
SITEMAP_ARTICLE_RE = re.compile(
    r'^  <url><loc>' + re.escape(SITE) + r'/media/(?P<slug>[\w-]+)\.html</loc>.*?</url>\n', re.M
)


class ToolError(Exception):
    pass


# ---------------------------------------------------------------- 記事の読み取り

_cache = {}


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

    m = need(r'<a href="\.\./media\.html\?cat=(\w+)" class="tag article__cat">([^<]+)</a>', "カテゴリ（article__cat）")
    cat, cat_label = m.group(1), m.group(2)
    title_html = need(r'<h1 class="article__title">(.*?)</h1>', "タイトル（h1.article__title）", re.S).group(1)
    publish = need(r'<article class="article" data-publish="(\d{4}-\d{2}-\d{2})"', "data-publish").group(1)
    og = need(r'<meta property="og:image" content="([^"]+)"', "og:image").group(1)
    thumb = og.rsplit("/", 1)[-1]
    if not (THUMBS / thumb).is_file():
        raise ToolError(f"{slug}: サムネイル images/photos/thumb/{thumb} がありません（og:image のファイル名と同じ軽量版が必要）")
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
    info = dict(slug=slug, cat=cat, cat_label=cat_label, title_html=title_html, publish=publish,
                modified=modified, thumb=thumb, services=services)
    _cache[slug] = info
    return info


# ---------------------------------------------------------------- カード

def render_card(a: dict, in_media_dir: bool) -> str:
    """既存カードと1文字も違わない形で作る。in_media_dir=True は pages/media/*.html 用"""
    href = f"../media/{a['slug']}.html" if in_media_dir else f"media/{a['slug']}.html"
    img = ("../../" if in_media_dir else "../") + f"images/photos/thumb/{a['thumb']}"
    d = a["publish"]
    return (
        f'          <a href="{href}" class="media-card reveal" data-category="{a["cat"]}" data-date="{d}">\n'
        f'            <div class="thumb thumb--photo">\n'
        f'              <img src="{img}" alt="" loading="lazy" decoding="async" width="720" height="450">\n'
        f'              <span class="thumb__cat">{a["cat_label"]}</span>\n'
        f'            </div>\n'
        f'            <div class="media-card__body">\n'
        f'              <span class="media-card__cat">{a["cat_label"]}</span>\n'
        f'              <h3 class="media-card__title">{a["title_html"]}</h3>\n'
        f'              <time class="media-card__date" datetime="{d}">{d.replace("-", ".")}</time>\n'
        f'            </div>\n'
        f'          </a>\n'
    )


def grid_span(s: str, label: str):
    """(グリッド開始タグの直後の位置, カードのリスト) を返す"""
    grids = list(GRID_RE.finditer(s))
    if len(grids) != 1:
        raise ToolError(f"{label}: media-grid が {len(grids)} 個あります（1個を想定）")
    start = grids[0].end()
    cards = [m for m in CARD_RE.finditer(s) if m.start() >= start]
    # カードはグリッド直後から隙間なく並んでいる前提を確認する
    pos = start
    for m in cards:
        if m.start() != pos:
            raise ToolError(f"{label}: カードの並びの途中に想定外の内容があります（{m.group('slug')} の前）")
        pos = m.end()
    return start, cards


def remove_card(s: str, slug: str, label: str):
    _, cards = grid_span(s, label)
    n = 0
    for m in reversed(cards):
        if m.group("slug") == slug:
            s = s[: m.start()] + s[m.end():]
            n += 1
    return s, n


def insert_card(s: str, card: str, label: str, after) -> str:
    """after(m) が True のカードの後ろ（＝最後に True になったカードの直後）に入れる。
    リストは after が True のものが先頭側に連続している前提（並び順のルールに従っていれば成り立つ）"""
    start, cards = grid_span(s, label)
    pos = start
    for m in cards:
        if after(m):
            pos = m.end()
        else:
            break
    return s[:pos] + card + s[pos:]


# ---------------------------------------------------------------- 並び順

def related_group(base: dict, other: dict) -> int:
    """0: 同じカテゴリ・サービス共通 / 1: 同じカテゴリ・共通なし / 2: 別カテゴリ・共通 / 3: 別カテゴリ・共通なし"""
    same_cat = other["cat"] == base["cat"]
    shares = bool(set(other["services"]) & set(base["services"]))
    return (0 if same_cat else 2) + (0 if shares else 1)


def media_order():
    """media.html に載っている順の slug リスト（同じ公開日どうしの順番の基準）"""
    s = (PAGES / "media.html").read_text(encoding="utf-8")
    _, cards = grid_span(s, "pages/media.html")
    return [m.group("slug") for m in cards]


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
        pos = entries[0].start()
        for m in entries:
            other = m.group("slug")
            try:
                pub = read_article(other)["publish"]
            except ToolError:
                lm = re.search(r"<lastmod>([\d-]+)</lastmod>", m.group(0))
                pub = lm.group(1) if lm else "0000-00-00"
            if pub <= a["publish"]:
                pos = m.end()
            else:
                break
    else:
        m = re.search(r"^  <url><loc>" + re.escape(SITE) + r"/media\.html</loc>.*?</url>\n", s, re.M)
        if not m:
            raise ToolError("seo/sitemap.xml: media.html の行が見つかりません")
        pos = m.end()
    return s[:pos] + line + s[pos:], removed, 1


# ---------------------------------------------------------------- 本体

def listing_files():
    files = [PAGES / "media.html", PAGES / "index.html"] + sorted(PAGES.glob("service-*.html"))
    return files + sorted(MEDIA.glob("*.html"))


def plan(slug: str, remove: bool):
    """{Path: (新しい本文, 取り除いた数, 入れた数)} を返す（書き込みはしない）"""
    a = None if remove else read_article(slug)
    out = {}
    originals = {f: f.read_text(encoding="utf-8") for f in listing_files()}

    # 1) まず全ファイルから取り除く
    work = {}
    for f, s in originals.items():
        label = f.relative_to(ROOT).as_posix()
        if f.parent == MEDIA and f.stem == slug:
            work[f] = [s, 0, 0]
            continue
        s2, n = remove_card(s, slug, label)
        work[f] = [s2, n, 0]

    if a is not None:
        # 2) 一覧（新しい順）。同じ公開日なら既存の後ろ
        def desc_after(m):
            return m.group("date") >= a["publish"]

        targets = [PAGES / "media.html", PAGES / "index.html"]
        targets += [PAGES / svc for svc in a["services"] if (PAGES / svc).is_file()]
        for svc in a["services"]:
            if not (PAGES / svc).is_file():
                print(f"警告: 関連サービス {svc} のページがありません（カードは入れません）", file=sys.stderr)
        for f in targets:
            w = work[f]
            w[0] = insert_card(w[0], render_card(a, False), f.relative_to(ROOT).as_posix(), desc_after)
            w[2] += 1

        # 3) 他の記事の「あわせて読みたい記事」
        new_key = None
        for f in sorted(MEDIA.glob("*.html")):
            if f.stem == slug:
                continue
            base = read_article(f.stem)
            new_key = (related_group(base, a), a["publish"])

            def rel_after(m, base=base, new_key=new_key):
                other = read_article(m.group("slug"))
                return (related_group(base, other), other["publish"]) <= new_key

            w = work[f]
            w[0] = insert_card(w[0], render_card(a, True), f.relative_to(ROOT).as_posix(), rel_after)
            w[2] += 1

        # 4) 新しい記事自身の「あわせて読みたい記事」を丸ごと作り直す
        order = [x for x in _slugs_in(work[PAGES / "media.html"][0]) if x != slug]
        rank = {x: i for i, x in enumerate(order)}
        others = [read_article(x) for x in order if (MEDIA / f"{x}.html").is_file()]
        missing = [x for x in order if not (MEDIA / f"{x}.html").is_file()]
        if missing:
            print(f"警告: media.html にあるが記事ファイルが無い: {', '.join(missing)}", file=sys.stderr)
        others.sort(key=lambda o: (related_group(a, o), o["publish"], rank[o["slug"]]))
        own = MEDIA / f"{slug}.html"
        s = work[own][0]
        start, cards = grid_span(s, own.relative_to(ROOT).as_posix())
        end = cards[-1].end() if cards else start
        new_block = "".join(render_card(o, True) for o in others)
        work[own] = [s[:start] + new_block + s[end:], len(cards), len(others)]

    for f, (s, r, i) in work.items():
        if s != originals[f]:
            out[f] = (s, r, i)

    smap = SITEMAP.read_text(encoding="utf-8")
    s2, r, i = sitemap_update(smap, slug, a)
    if s2 != smap:
        out[SITEMAP] = (s2, r, i)
    return out


def _slugs_in(media_html: str):
    _, cards = grid_span(media_html, "pages/media.html")
    return [m.group("slug") for m in cards]


def main():
    ap = argparse.ArgumentParser(description="暮らす旅の手帖の記事カード・sitemap・llms.txt を更新する")
    ap.add_argument("slug", nargs="?", help="追加する記事のスラッグ（pages/media/<slug>.html）")
    ap.add_argument("--remove", metavar="SLUG", help="このスラッグのカード・sitemap 登録を取り除く")
    ap.add_argument("--dry-run", action="store_true", help="変更するファイルと件数だけ表示する")
    ap.add_argument("--no-llms", action="store_true", help="seo/llms.txt を作り直さない")
    ap.add_argument("--today", help="llms.txt の判定日 YYYY-MM-DD（既定は日本時間の今日）")
    args = ap.parse_args()
    if bool(args.slug) == bool(args.remove):
        ap.error("<slug> か --remove <slug> のどちらか一方を指定してください")
    slug = args.remove or args.slug
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        ap.error(f"スラッグの形式が不正です: {slug}")

    try:
        changes = plan(slug, remove=bool(args.remove))
        if not args.remove:
            a = read_article(slug)
            print(f"{'追加' if not args.dry_run else '追加（dry-run）'}: {slug} ／ {a['cat_label']} ／ 公開日 {a['publish']}"
                  f" ／ 更新日 {a['modified']} ／ サムネイル thumb/{a['thumb']} ／ 関連サービス {', '.join(a['services']) or 'なし'}")
            from build_llms import today_jst
            today = args.today or today_jst()
            if a["publish"] < today:
                print(f"注意: 公開日 {a['publish']} が今日（{today}）より前です。新しい記事なら、公開日をさかのぼって付けていないか確認してください。")
        else:
            print(f"{'削除' if not args.dry_run else '削除（dry-run）'}: {slug}")
    except ToolError as e:
        sys.exit(f"エラー: {e}")

    if not changes:
        print("カード・sitemap: 変更なし（すでにルールどおり）")
    for f in sorted(changes, key=lambda p: p.as_posix()):
        s, r, i = changes[f]
        print(f"  {f.relative_to(ROOT).as_posix()}: 取り除き {r} ／ 挿入 {i}")
        if not args.dry_run:
            f.write_text(s, encoding="utf-8")
    print(f"変更ファイル数: {len(changes)}" + ("（dry-run・書き込みなし）" if args.dry_run else ""))

    if not args.no_llms:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import build_llms
        build_llms.write(args.today, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
