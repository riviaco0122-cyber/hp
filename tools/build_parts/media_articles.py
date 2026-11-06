# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：記事データの読み込みと、写真・アイキャッチ・記事カード・ヘッダー・フッター・相談の案内。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- media (articles)
# 読者が「何をしたいか」で探せるテーマ。1つの記事が複数のテーマに入る（先頭が主なテーマ）
MEDIA_CATEGORIES = [
    ("sell", "売る・手放す"),
    ("lend", "貸す・任せる"),
    ("house", "物件・改修"),
    ("start", "開業・手続き"),
    ("money", "お金・税金"),
    ("operate", "集客・運営"),
    ("trend", "観光と地域"),
]
# 以前のカテゴリのURLから、近いテーマへ転送する（vercel.json）
OLD_CATEGORY_REDIRECTS = {"akiya": "house", "market": "trend", "chiho": "trend", "kaigyo": "start", "keiei": "operate"}

from articles_base import ARTICLES_BASE  # 初期の記事（記事データは tools/articles_*.py）
ARTICLES = list(ARTICLES_BASE)


MEDIA_CAT_NAMES = dict(MEDIA_CATEGORIES)
ARTICLE_BY_SLUG = {a["slug"]: a for a in ARTICLES}


def fmt_date(d):
    return d.replace("-", ".")


def read_minutes(a):
    import re as _re
    text = _re.sub(r"<[^>]+>", "", "".join(h for _, _, h in a["sections"]))
    return max(3, round(len(text) / 500))


# 予約公開の記事（2026-11-01 から1日おきに公開。公開日前は一覧に出さない。記事ページは転送せずそのまま表示）
from articles_sched1 import ARTICLES_SCHED1
from articles_sched2 import ARTICLES_SCHED2
from articles_case import ARTICLES_CASE
from articles_series1 import ARTICLES_SERIES1
from articles_series2 import ARTICLES_SERIES2
from articles_series3 import ARTICLES_SERIES3
from articles_auto import ARTICLES_AUTO  # AI社員チームが追加する記事
from articles_interviews import ARTICLES_INTERVIEWS  # 民泊オーナーへの取材をもとにした事例（人から受け取った一次情報）
for _a in ARTICLES_SCHED1 + ARTICLES_SCHED2 + ARTICLES_CASE + ARTICLES_SERIES1 + ARTICLES_SERIES2 + ARTICLES_SERIES3 + ARTICLES_AUTO + ARTICLES_INTERVIEWS:
    _a.setdefault("tone", "sand")
    _a.setdefault("updated", _a["date"])
    ARTICLES.append(_a)
# 削除した記事（2026-10-14 人の依頼。読み手の必要度が低い・専門的すぎる記事）。旧URLは vercel.json で近い記事へ 301
DELETED_ARTICLES = {
    "akiya-rate-and-inn": "why-akiya-utilization-now",
    "akiya-regional-revitalization": "why-akiya-utilization-now",
    "inbound-regional-dispersion": "long-stay-travel-demand",
    "tourism-labor-shortage": "cleaning-linen-operations",
    "kankei-jinko-and-inns": "why-minpaku-for-akiya",
    "akiya-local-resource": "why-akiya-utilization-now",
    "inn-local-economy": "why-minpaku-for-akiya",
    "akiya-data-9-million": "why-akiya-utilization-now",
    "kominka-stay-value": "kominka-renovation-points",
    "minpaku-partner-choose": "minpaku-management-company",
    # 2026-10-22 人の依頼。事例は増え続けるため、項目をそろえて比べる一覧記事は持たない（事例はアキヤドのトップの「民泊オーナーの事例」に自動で並ぶ）。旧URLは /media.html へ 301
    "minpaku-case-list": "",
}
ARTICLES = [_a for _a in ARTICLES if _a["slug"] not in DELETED_ARTICLES]
# 民泊オーナーへの取材事例（slug が case-owner- で始まる記事）。新しい順に自動で並ぶので、事例を足しても一覧の手直しは要らない
CASE_SLUGS = [_a["slug"] for _a in sorted(ARTICLES, key=lambda x: x["date"], reverse=True) if _a["slug"].startswith("case-owner-")]
from case_mixins import MIXINS  # 取材事例・内部リンクの差し込み（節の末尾へ）
for _a in ARTICLES:
    _mx = MIXINS.get(_a["slug"])
    if _mx:
        _secs = []
        for _sid, _h, _body in _a["sections"]:
            _secs.append((_sid, _h, _body + "\n" + _mx[_sid] if _sid in _mx else _body))
        _a["sections"] = _secs
from article_blurbs import BLURBS  # 一覧カードの「小さな補足」
for _a in ARTICLES:
    # 一覧用の表示名（short の改行を除く）と補足。補足は記事データの blurb > article_blurbs.py > title の「｜」以降
    _a["blurb"] = _a.get("blurb") or BLURBS.get(_a["slug"]) or (_a["title"].split("｜", 1)[1] if "｜" in _a["title"] else "")
ARTICLE_TOPICS = {
    "akiya-inherited-house-to-inn": ["sell", "lend", "money"],
    "akiya-3000man-deduction": ["sell", "money"],
    "akiya-bank-guide": ["house", "sell"],
    "akiya-lease-types": ["lend"],
    "minpaku-management-company": ["lend", "start"],
    "kominka-renovation-points": ["house"],
    "shizuoka-yaizu-akiya-inn": ["house", "trend"],
    "new-build-vs-used-house-inn": ["start", "house", "money"],
    "minpaku-vs-ryokan-law": ["start"],
    "minpaku-start-steps": ["start"],
    "minpaku-fire-safety": ["start"],
    "small-inn-subsidies": ["money", "start"],
    "inn-startup-funding": ["money", "start"],
    "minpaku-investment-yield": ["money"],
    "accommodation-tax": ["money", "trend"],
    "case-rental-house-inn-first-year": ["operate", "money"],
    "airdna-revenue-simulation": ["operate", "money"],
    "inn-kpi-basics": ["operate"],
    "ota-vs-direct-booking": ["operate"],
    "listing-photo-tips": ["operate"],
    "cleaning-linen-operations": ["operate"],
    "guest-review-tips": ["operate"],
    "japan-tourism-market-data": ["trend"],
    "long-stay-travel-demand": ["trend"],
    "inbound-regional-dispersion": ["trend"],
    "inn-local-economy": ["trend"],
    "akiya-regional-revitalization": ["trend"],
    "tourism-labor-shortage": ["trend"],
    "kankei-jinko-and-inns": ["trend"],
}
for _a in ARTICLES:
    _a["topics"] = ARTICLE_TOPICS.get(_a["slug"]) or _a["topics"]
    _a["category"] = _a["topics"][0]
ARTICLE_BY_SLUG = {a["slug"]: a for a in ARTICLES}


ARTICLE_PHOTOS = {
    # 記事ごとに別の写真を使う（同じ写真を2つの記事に使わない）
    "akiya-inherited-house-to-inn": ("old-town-street", "古い町家が並ぶ路地"),
    "japan-tourism-market-data": ("fuji-lake", "湖と富士山の風景"),
    "akiya-regional-revitalization": ("rural-station", "田園と山に囲まれた地方の駅と町並み"),
    "minpaku-vs-ryokan-law": ("temple-bridge", "緑に囲まれた寺院と朱色の橋"),
    "airdna-revenue-simulation": ("koi-pond", "鯉の泳ぐ池"),
    "small-inn-subsidies": ("dark-room", "障子越しに光の入る和室"),
    "new-build-vs-used-house-inn": ("thatched-house", "田園に佇む茅葺きの古民家"),
    "shizuoka-yaizu-akiya-inn": ("town-railway", "住宅街を抜ける線路と町並み"),
    "minpaku-start-steps": ("white-bedroom", "白を基調とした明るい寝室"),
    "akiya-bank-guide": ("green-hills", "緑の丘が連なる山あいの風景"),
    "inn-kpi-basics": ("pillow", "整えられた寝具と枕"),
    "long-stay-travel-demand": ("scene-stay", "縁側の向こうに山と町並みを望む和室"),
    "minpaku-fire-safety": ("hotel-room", "夜の客室"),
    "ota-vs-direct-booking": ("fuji-rapeseed", "菜の花畑と富士山"),
    "kominka-renovation-points": ("irori-room", "囲炉裏のある古民家の座敷"),
    "inn-local-economy": ("scene-walk", "灯りのともる夜の路地"),
    "cleaning-linen-operations": ("white-bed", "白いシーツの整ったベッド"),
    "inbound-regional-dispersion": ("fuji-train", "富士山を背に走る列車"),
    "minpaku-management-company": ("gassho-village", "合掌造りの家と山並み"),
    "akiya-lease-types": ("window-garden", "和室の窓から望む庭"),
    "listing-photo-tips": ("autumn-garden", "紅葉に彩られた日本庭園"),
    "tourism-labor-shortage": ("terraced-fields", "海を望む棚田と茅葺きの小屋"),
    "inn-startup-funding": ("fuji-lupin", "花畑の向こうに望む富士山"),
    "guest-review-tips": ("garden-boat", "庭園の池に浮かぶ舟"),
    "accommodation-tax": ("oshino-mill", "茅葺きの水車小屋と富士山"),
    "akiya-3000man-deduction": ("cherry-river", "川沿いの桜並木"),
    "kankei-jinko-and-inns": ("shrine-path", "木々に囲まれた参道"),
    "minpaku-investment-yield": ("mountain-dawn", "朝の光に照らされた山並み"),
    "case-rental-house-inn-first-year": ("analytics-paper", "数字の推移をまとめた資料（イメージ）"),
}
# 体系的に学ぶシリーズの記事は、記事データに写真（photo）と図解（figure）を持つ
for _a in ARTICLES:
    if "photo" in _a:
        ARTICLE_PHOTOS[_a["slug"]] = _a["photo"]


WEBP_WIDTHS = (800,)


def webp_variants(name):
    """写真の軽量版（WebP・幅800）を images/photos/w/ に作る。元の写真はそのまま残す"""
    from PIL import Image
    out_dir = os.path.join(OUT, "images", "photos", "w")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(OUT, "images", "photos", f"{name}.jpg")
    im = Image.open(src)
    ow = im.size[0]
    dst = os.path.join(out_dir, f"{name}-800.webp")
    if not (os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)):
        rgb = im.convert("RGB")
        tw = min(800, ow)
        rgb.resize((tw, round(im.size[1] * tw / ow)), Image.LANCZOS).save(dst, "WEBP", quality=76, method=6)
    return ow


def photo(name, cls="", alt="", width=1600, height=1000, sizes="100vw", lazy=True, priority=False):
    """写真を表示する。スマホなど小さい表示では軽量版（WebP・幅800）、大きい表示では元の写真を、ブラウザが自動で選ぶ"""
    ow = webp_variants(name)
    attrs = ' loading="lazy"' if lazy else ""
    attrs += ' fetchpriority="high"' if priority else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="images/photos/{name}.jpg" srcset="images/photos/w/{name}-800.webp 800w, images/photos/{name}.jpg {ow}w" '
            f'sizes="{sizes}" alt="{e(alt)}" width="{width}" height="{height}"{attrs} decoding="async">')


def eyecatch_path(a):
    """アイキャッチの URL。画像は30日キャッシュされるので、中身が変わったら版番号も変わるようにする"""
    rel = f"images/eyecatch/{a['slug']}.jpg"
    return f"{rel}?v={asset_version(rel)}"


def has_eyecatch(a):
    """tools/eyecatch.py で作ったアイキャッチ（記事トップ・OGP用）があるか"""
    return os.path.exists(os.path.join(OUT, "images", "eyecatch", a["slug"] + ".jpg"))


def thumb(a, size=""):
    """記事のサムネイル（写真）。カードは軽量版、記事トップは原寸を使う"""
    name, alt = ARTICLE_PHOTOS[a["slug"]]
    if size == "hero":
        if has_eyecatch(a):
            return f"""<figure class="article__photo article__photo--eyecatch"><img src="{eyecatch_path(a)}" alt="{e(a["short"].replace(chr(10), ""))}" width="1200" height="630" fetchpriority="high" decoding="async"></figure>"""
        return f"""<figure class="article__photo">{photo(name, alt=alt, width=1600, height=700, sizes="(max-width: 899px) 100vw, 800px", lazy=False, priority=True)}</figure>"""
    return f"""<div class="thumb thumb--photo">
              {photo(name, width=720, height=450, sizes="(max-width: 899px) 90vw, 400px")}
              <span class="thumb__cat">{e(MEDIA_CAT_NAMES[a["category"]])}</span>
              {thumb_banner(a)}
            </div>"""


def thumb_banner(a):
    """サムネイルの上に、記事の要点を短く載せる（ぱっと見で何の記事か分かるように）"""
    lines = "<br>".join(e(l) for l in a["short"].split("\n"))
    return f'<span class="thumb__banner" aria-hidden="true"><span class="thumb__kicker">{e(MEDIA_CAT_NAMES[a["category"]])}</span><span class="thumb__catch">{lines}</span></span>'


def _thumb_text(a, size=""):
    """記事のサムネイル（画像を使わない文字組みのカバー）"""
    lines = "<br>".join(e(l) for l in a["short"].split("\n"))
    return f"""<div class="thumb thumb--{a["tone"]}{(" thumb--" + size) if size else ""}" aria-hidden="true">
              <span class="thumb__cat">{e(MEDIA_CAT_NAMES[a["category"]])}</span>
              <span class="thumb__title">{lines}</span>
              <span class="thumb__brand">アキヤド</span>
            </div>"""


def card_tags(a):
    """記事カードのタグ：誰向けか（状況）とテーマ。ぱっと見で何の記事か分かるようにする"""
    who = [f'<span class="ctag ctag--who">{e(g["label"])}</span>' for g in guides_of(a["slug"])]
    topics = [f'<span class="ctag">{e(MEDIA_CAT_NAMES[t])}</span>' for t in a["topics"]]
    return f'<span class="ctags">{"".join((who[:1] + topics)[:2])}</span>'


def list_name(a):
    """一覧カードの表示名（短い。1〜2行）。元の title は変えない"""
    # 2行に分けた短い名前は、1行目が句読点で終わっていなければ「｜」でつなぐ（「〜の取り方広さ…」のように続けて読めてしまうため）
    lines = [l.strip() for l in a["short"].split("\n") if l.strip()]
    out = lines[0] if lines else ""
    for l in lines[1:]:
        out += l if out[-1:] in "。、！？」』）" else "｜" + l
    return out


def article_card(a, extra_class=""):
    return f"""          <a href="media/{a["slug"]}.html" class="media-card reveal{extra_class}" data-category="{a["category"]}" data-date="{a["date"]}">
            {thumb(a)}
            <div class="media-card__body">
              {card_tags(a)}
              <h3 class="media-card__title">{"<br>".join(e(l) for l in a["short"].split(chr(10)) if l.strip())}</h3>
              <time class="media-card__date" datetime="{a["date"]}">{fmt_date(a["date"])}</time>
            </div>
          </a>"""


def media_section(articles, eyebrow="Media", title="アキヤド", lead="", more=True, limit=3, keep_order=False):
    if keep_order is False:
        articles = sorted(articles, key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in articles)
    more_html = f'\n        <div class="media-more reveal"><a href="media.html" class="btn btn--ghost">記事一覧を見る {ARROW}</a></div>' if more else ""
    lead_html = f'\n          <p class="section-lead">{e(lead)}</p>' if lead else ""
    # 見出しが「アキヤド」のとき（コーポレートTOP）は、メディアのロゴを見せる
    title_html = (f'<a href="media.html" class="tlogo" aria-label="アキヤド（空き家と民泊のメディア）">{AKIYADO_MARK}'
                  f'<span class="tlogo__ja" translate="no">アキヤド</span></a><span class="tlogo__sub">空き家と民泊のメディア</span>'
                  if title == "アキヤド" else e(title))
    return f"""    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{e(eyebrow)}</span>
          <h2 class="section-title{" section-title--logo" if title == "アキヤド" else ""}">{title_html}</h2>{lead_html}
        </div>
        <div class="media-grid media-grid--scroll" data-limit="{limit}">
{cards}
        </div>{more_html}
      </div>
    </section>"""


# メディアの骨格：カテゴリ（一覧ページ）と、目的別のガイド（記事を読む順に並べた特集）
MEDIA_CAT_INFO = {
    "sell": ("Sell", "相続した家を手放すときの流れ、売るときの税金の特例、放置したときのリスク。売るかどうか迷っている段階から読める記事をまとめています。"),
    "lend": ("Lease", "家を貸すときの契約の種類、借り上げ、管理会社への委託。家を手放さずに、毎月の収入に変えるための選択肢をまとめています。"),
    "house": ("House", "空き家バンクでの探し方、宿に向く物件と場所の見極め、古い家の改修。建物と場所選びで失敗しないための知識をまとめています。"),
    "start": ("Start", "民泊と旅館業の違い、届出の流れ、消防設備。小さな宿を開業するまでに必要な手続きを、つまずきやすい点とあわせてまとめています。"),
    "money": ("Money", "開業資金の用意の仕方、補助金、税金、利回り。小さな宿や空き家活用を始める前に押さえておきたい、お金の話をまとめています。"),
    "operate": ("Operation", "稼働率と客室単価、予約サイトの使い方、清掃、レビュー。開業したあとに宿の売上と評判を育てる、運営の知識をまとめています。"),
    "trend": ("Trend", "訪日客の動向、長期滞在の広がり、関係人口。観光と地域の変化を公的なデータをもとに読み解き、地方の小さな宿の可能性を考えます。"),
}
# テーマ一覧ページの title。検索結果ではタイトルしか見られないことが多いので、何の話か（民泊・空き家・宿）を前に置く
MEDIA_CAT_TITLE = {
    "sell": "空き家を売る・手放すときの記事一覧｜アキヤド",
    "lend": "空き家を貸す・管理を任せるときの記事一覧｜アキヤド",
    "house": "民泊・宿にする物件選びと改修の記事一覧｜アキヤド",
    "start": "民泊・小さな宿の開業と手続きの記事一覧｜アキヤド",
    "money": "民泊・空き家活用のお金と税金の記事一覧｜アキヤド",
    "operate": "民泊・宿の集客と運営の記事一覧｜アキヤド",
    "trend": "民泊・宿から見る観光と地域の記事一覧｜アキヤド",
}
# 読者の状況（ペルソナ）別のガイド。悩みが生まれる順に「段階」を分け、記事を並べる
MEDIA_GUIDES = [
    dict(key="sell", label="空き家を売りたい", title="空き家を売りたい方へ", service="operation", photo="old-town-street",
         who="相続した実家や、使っていない家を手放したい方",
         worries=["放置しているとどうなる？", "売るときの税金は？", "売る以外の選択肢は？"],
         lead="相続した実家や、使っていない家を手放したい。そう考えたときに知っておきたいことを、悩みが生まれる順に並べました。",
         stages=[
             ("まず知っておきたいこと", "放置した場合の負担と、空き家をめぐる制度の変化。", ["akiya-inherited-house-to-inn", "akiya-bank-guide"]),
             ("売る前に、比べておきたいこと", "売る以外に「貸す」「宿として活かす」という選択肢も。手取りと将来を比べて判断します。", ["akiya-lease-types", "shizuoka-yaizu-akiya-inn", "new-build-vs-used-house-inn"]),
             ("お金と税金", "売却したときの税金と、使える特例。", ["akiya-3000man-deduction"]),
         ]),
    dict(key="use", label="空き家を活かしたい", title="空き家を活かしたい方へ", service="operation", photo="thatched-house",
         who="家を手放さずに、収入や地域の役に立つ形で活かしたい方",
         worries=["古い家でも宿にできる？", "貸す？任せる？自分でやる？", "改修にいくらかかる？"],
         lead="思い出のある家を手放さずに、収入や地域の役に立つ形で活かしたい。活用の選び方から改修、お金のことまでを順番に。",
         stages=[
             ("活かし方を知る", "空き家が宿として、地域の中でどんな価値を持つのか。", ["akiya-inherited-house-to-inn"]),
             ("活かし方を選ぶ", "貸す・運営を任せる・自分で営業する。契約と法令の違い。", ["akiya-lease-types", "minpaku-vs-ryokan-law", "minpaku-management-company"]),
             ("家を整える", "残すもの・直すもの、消防設備の基準。", ["kominka-renovation-points", "minpaku-fire-safety", "new-build-vs-used-house-inn"]),
             ("お金の見通しを立てる", "補助金と、収益の見込みの立て方。", ["small-inn-subsidies", "airdna-revenue-simulation"]),
         ]),
    dict(key="side", label="副業で宿をはじめたい", title="副業で宿をはじめたい方へ", service="management", photo="white-bedroom",
         who="本業を続けながら、民泊や小さな宿に挑戦してみたい方",
         worries=["副業でも民泊はできる？", "資金はいくら必要？", "本業があっても運営できる？"],
         lead="本業を続けながら、民泊や小さな宿に挑戦してみたい。市場の見方から開業の手続き、資金、運営を任せる方法までを順番に。",
         stages=[
             ("市場と可能性を知る", "どんな旅行者が、どんな宿を求めているのか。投資としての考え方。", ["long-stay-travel-demand", "minpaku-investment-yield"]),
             ("物件とお金を準備する", "物件の探し方、収益の見込み、資金の集め方。", ["akiya-bank-guide", "airdna-revenue-simulation", "inn-startup-funding", "small-inn-subsidies"]),
             ("開業の手続きを進める", "民泊か旅館業か、消防、管理を任せる体制。", ["minpaku-start-steps", "minpaku-vs-ryokan-law", "minpaku-fire-safety", "minpaku-management-company"]),
             ("運営して、育てる", "数字の読み方、集客、レビュー、清掃、宿泊税。", ["inn-kpi-basics", "ota-vs-direct-booking", "listing-photo-tips", "guest-review-tips", "cleaning-linen-operations", "accommodation-tax"]),
         ]),
    # すでに宿を運営している方向け。集客・採用の記事の受け皿（記事データに guides=[("run", 2)] のように書く）
    dict(key="run", label="宿の運営を伸ばしたい", title="宿の運営を伸ばしたい方へ", service="marketing", photo="laptop-dashboard",
         who="すでに民泊や小さな宿を運営していて、予約や人手に悩んでいる方",
         worries=["予約がなかなか増えない", "予約サイトの手数料が重い", "清掃や運営の人手が足りない"],
         lead="民泊や小さな宿を運営していて、予約や人手に悩んでいる。数字の見方から、予約の増やし方、人手と運営の整え方までを順番に。",
         stages=[
             ("数字で今を知る", "稼働率・客室単価の読み方と、赤字にならない線。", ["inn-kpi-basics", "minpaku-break-even"]),
             ("予約を増やす", "予約サイトと自社予約の使い分け、掲載ページ、レビュー、料金、閑散期。", ["ota-vs-direct-booking", "listing-photo-tips", "guest-review-tips", "case-owner-pricing-mistake", "minpaku-off-season"]),
             ("人手と運営を整える", "清掃の仕組み、離れた場所からの運営、近隣との関係、任せる先。", ["cleaning-linen-operations", "minpaku-remote-operation", "minpaku-neighbor-rules", "minpaku-management-company"]),
         ]),
]
# 記事は今後も増える前提。記事データに guides=[("sell", 2)]（ガイドのkey, Stepの番号）と書けば、
# そのガイドの該当Stepの末尾に自動で並ぶ（ここのリストを書き換えなくてよい）
for _a in ARTICLES:
    for _key, _step in _a.get("guides", []):
        _st = next(g for g in MEDIA_GUIDES if g["key"] == _key)["stages"][_step - 1][2]
        if _a["slug"] not in _st:
            _st.append(_a["slug"])
for _g in MEDIA_GUIDES:
    _g["slugs"] = list(dict.fromkeys(x for _, _, xs in _g["stages"] for x in xs))
MEDIA_GUIDE_FOR_CAT = {"sell": "sell", "lend": "use", "house": "use", "start": "side", "money": "side", "operate": "run", "trend": "use"}
# よくある悩みから記事へ（読者の言葉で書く）
MEDIA_QUESTIONS = [
    ("sell", "相続した実家、放置するとどうなる？", "akiya-inherited-house-to-inn"),
    ("sell", "空き家を売ったら、税金はどれくらいかかる？", "akiya-3000man-deduction"),
    ("use", "観光地ではない場所の空き家でも、宿になる？", "shizuoka-yaizu-akiya-inn"),
    ("use", "家を貸すなら、どんな契約がいい？", "akiya-lease-types"),
    ("use", "古い家を宿にするなら、どこを直すべき？", "kominka-renovation-points"),
    ("side", "副業で民泊をはじめるには、何から？", "minpaku-start-steps"),
    ("side", "民泊と旅館業、どちらで始めればいい？", "minpaku-vs-ryokan-law"),
    ("side", "本業があっても、宿の運営はできる？", "minpaku-management-company"),
    ("side", "開業資金は、どう用意する？", "inn-startup-funding"),
    ("side", "実際、初期投資はどれくらいで回収できる？", "case-rental-house-inn-first-year"),
    ("side", "宿の収益は、どれくらい見込める？", "airdna-revenue-simulation"),
]
MEDIA_LEAD = "空き家を売りたい、活かしたい。副業で民泊をはじめたい。その悩みに、宿を運営する私たちが順を追ってお答えします。"


# 記事の途中に置く相談の案内（読者の状況＝ガイドごとに言葉を変える）
CV_MESSAGES = {
    "sell": "売るか、活かすか。物件の状況をうかがい、いちばん負担の少ない方法を無料でご提案します。",
    "use": "その家、宿として活かせるか。現地と周辺の宿を調べ、収支の見込みを無料で試算します。",
    "side": "物件選び、許可、収支の見通し。民泊を始める前の疑問に、アキヤドが無料でお答えします。",
    "run": "予約の伸ばし方、人手の確保。運営中の宿の悩みに、アキヤドを運営するRIVIA&CO.が無料でお答えします。",
    "": "空き家の売却・活用、民泊の開業について、アキヤドが無料でご相談に乗ります。",
}


# 集客・採用の記事は、相談の案内をコーポレートの支援事業に向ける（ガイドより優先）
CV_SERVICE = {
    "marketing": ("予約サイト、掲載ページ、自社予約。宿の集客の見直しに、アキヤドを運営するRIVIA&CO.が無料でお答えします。", "service-marketing.html"),
    "recruit": ("清掃や運営の人手、求人の出し方。宿の採用の悩みに、アキヤドを運営するRIVIA&CO.が無料でお答えします。", "service-recruit.html"),
}
# ガイドごとの「サービスとプランを見る」の行き先（アキヤドのサービスがないガイド）
GUIDE_PLAN_PAGE = {"run": "service-marketing.html"}


def inline_cta_parts(a, g):
    """記事の途中に置く相談の案内の、文言と「サービスとプランを見る」の行き先"""
    if a["services"][0] in CV_SERVICE:
        return CV_SERVICE[a["services"][0]]
    k = g["key"] if g else ""
    href = GUIDE_PLAN_PAGE.get(k) or f'media/{MEDIA_SERVICE_BY_KEY[k or "use"]["slug"]}.html'
    return CV_MESSAGES.get(k, CV_MESSAGES[""]), href


def guide_of(slug):
    return next((g for g in MEDIA_GUIDES if slug in g["slugs"]), None)


def guides_of(slug):
    return [g for g in MEDIA_GUIDES if slug in g["slugs"]]


# アキヤドのマーク（空き家を宿にして住みつくヤドカリ。2026-10-22 人が選んだ案）
AKIYADO_MARK = ('<svg class="amark" viewBox="0 0 67 64" aria-hidden="true">'
                '<g stroke="#CF5F37" stroke-width="3.6" stroke-linecap="round" fill="none"><path d="M14 52l-4 7M21 54l-1 7M28 53l2 6M14 40l-2-9M22 40v-9"/></g>'
                '<ellipse cx="22" cy="46" rx="13" ry="9" fill="#CF5F37"/>'
                '<path d="M3 46a8 8 0 1 1 13-6.5l-6.5 1.5 4 5.5A8 8 0 0 1 3 46z" fill="#CF5F37"/>'
                '<circle cx="12" cy="27" r="4.6" fill="#fff" stroke="#262a27" stroke-width="1.6"/><circle cx="22" cy="27" r="4.6" fill="#fff" stroke="#262a27" stroke-width="1.6"/>'
                '<circle cx="13.2" cy="27.4" r="2.1" fill="#262a27"/><circle cx="23.2" cy="27.4" r="2.1" fill="#262a27"/>'
                '<path class="amark__gap amark__house" d="M30 28 45 14l15 14v18a4 4 0 0 1-4 4H34a4 4 0 0 1-4-4z" stroke-width="2.6" stroke-linejoin="round"/>'
                '<path class="amark__roof" d="M26.5 30.5 45 12.5l18.5 18" fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
                '<rect x="40" y="30" width="10" height="10" rx="2" fill="#F4C65A"/></svg>')


def media_logo(cls="mlogo"):
    """メディアのロゴ（文字組み）。名前「アキヤド」（空き家＋宿）と、何のメディアかを示す添え書き"""
    return f"""<span class="{cls}">{AKIYADO_MARK}<span class="{cls}__ja">アキヤド</span><span class="{cls}__sub">空き家と民泊のメディア</span></span>"""


def media_header(current=""):
    return f"""  <header class="header header--media">
    <div class="container mheader__inner">
      <a href="media.html" class="mheader__logo">{media_logo()}</a>
      <div class="mheader__right">
      <a href="contact.html?category=document&amp;from=akiyado-header" class="mheader__cta mheader__cta--sub" data-cta="media-header-doc">資料請求</a>
      <a href="contact.html?from=akiyado" class="mheader__cta" data-cta="media-header">無料相談</a>
      <button type="button" class="mmenu-btn" aria-label="メニューを開く" aria-expanded="false" aria-controls="mnav"><span></span><span></span></button>
      </div>
    </div>
{media_tabs(current)}
{media_nav(current)}
  </header>"""


def media_footer():
    guides = "".join(f'<li><a href="media/guide-{g["key"]}.html">{e(g["title"])}</a></li>' for g in MEDIA_GUIDES)
    themes = "".join(f'<li><a href="media/category-{k}.html">{e(n)}</a></li>' for k, n in MEDIA_CATEGORIES)
    return f"""  <footer class="mfooter">
    <div class="container">
      <div class="mfooter__top">
        <div>
          <a href="media.html" class="mfooter__logo">{media_logo()}</a>
          <p class="mfooter__lead">空き家を売る。活かす。民泊をはじめる。<br>宿を運営する私たちが、悩みに沿ってお届けします。</p>
        </div>
        <div class="mfooter__cols">
          <div><p class="mfooter__label">状況から読む</p><ul>{guides}</ul></div>
          <div><p class="mfooter__label">テーマから探す</p><ul>{themes}</ul></div>
          <div><p class="mfooter__label">アキヤドについて</p><ul>
            <li><a href="media/learn.html">基礎から学ぶ</a></li>
            <li><a href="media/search.html">記事をさがす</a></li>
            <li><a href="media/plans.html">アキヤドのプラン</a></li>
            <li><a href="media/company.html">運営者情報</a></li>
            <li><a href="{NOTE_STORY_URL}" target="_blank" rel="noopener" data-cta="note-story-footer">代表・片井の体験記（note）</a></li>
            <li><a href="contact.html">ご相談・お問い合わせ</a></li>
            <li><a href="privacy.html">プライバシーポリシー</a></li>
          </ul></div>
        </div>
      </div>
      <div class="mfooter__bottom">
        <a href="index.html" class="mfooter__corp"><img src="images/logo/logo-white.svg" alt="RIVIA&amp;CO." width="325" height="64" loading="lazy"><span>このメディアは合同会社RIVIA&amp;CO.が運営しています</span></a>
        <p>&copy; 2026 合同会社RIVIA&amp;CO.</p>
      </div>
    </div>
  </footer>"""


MEDIA_CTA_TEXT = {
    "": ('空き家のこと、<br class="sp-only">まずは気軽にご相談ください。',
         '売るか、活かすか、民泊にするか。まだ決めていない段階でも大丈夫です。<br class="pc-only">宿を運営する私たちが、物件の状況に合わせてお答えします。'),
    "marketing": ('宿の集客や人手のこと、<br class="sp-only">まずは気軽にご相談ください。',
                  '予約が伸びない、手数料が重い、人が足りない。原因がはっきりしない段階でも大丈夫です。<br class="pc-only">宿を運営する私たちが、いまの状況に合わせてお答えします。'),
}


def media_cta(category="operation"):
    """アキヤドの相談ブロック。気軽さ（無料・全国・営業なし）を先に伝える"""
    title, lead = MEDIA_CTA_TEXT.get(category, MEDIA_CTA_TEXT[""])
    return f"""    <section class="section mcta">
      <div class="container">
        <div class="mcta__box reveal">
          <p class="mcta__en">Consultation</p>
          <h2 class="mcta__title">{title}</h2>
          <p class="mcta__lead">{lead}</p>
          <ul class="mcta__points"><li>相談・お見積りは無料</li><li>全国対応・オンライン可</li><li>しつこい営業はしません</li></ul>
          <div class="mcta__btns">
            <a href="contact.html?category={category}&amp;from=akiyado" class="mbtn" data-cta="media-bottom">無料で相談する {ARROW}</a>
            {plan_doc_link("bottom")}
          </div>
          <p class="mcta__plans"><a href="media/plans.html">アキヤドのプランを見る {ARROW}</a></p>
          <p class="mcta__note">運営：合同会社RIVIA&amp;CO.（宿泊施設の運営・空き家再生）</p>
        </div>
      </div>
    </section>"""
