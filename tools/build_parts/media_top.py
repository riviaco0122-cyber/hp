# アキヤドの特徴（2026-11-27 作り直し）。役割は「なぜアキヤドに任せられるか」が3秒で伝わること。
# 写真は使わず、3つの理由を同じ形のカードに並べ、それぞれの「証拠」（運営記録の数字・3つの道・運営の仕組み）を大きく見せる。
# 数字は、どの宿の数字かを同じ枠の中に書く（イメージ写真の下に置くと、写真の宿の数字に見えるため）。
# 見出しの「|」は、スマホで折り返す位置（語の途中で折れないように）
MFEATURES = [
    dict(title="宿を運営する|当事者が答える", text="記事の数字もご提案の見込みも、私たちの運営記録が元です。",
         src="運営している宿の一例：|静岡県下田市・アパートの一室を貸切",
         facts=[("1年目の稼働率", "約", "53", "%"), ("開業費用をほぼ回収", "約", "14", "か月")],
         link=("media/case-rental-house-inn-first-year.html", "この宿の運営事例を読む")),
    dict(title="売る・貸す・はじめるを|並べて比べられる", text="売却・借り上げ・自分で運営の見込みを、並べてお出しします。",
         ways=[("売る", "売却額の目安"), ("借り上げ", "家を残して収入"), ("自分で運営", "宿の収支見込み")],
         cap="※ 収益を保証するものではありません。"),
    dict(title="遠方の家でも回る|運営の仕組み", text="開業2か月目には、現地に行かなくても回る体制にしました。",
         big=("現地に行くのは", "数か月に1回", "ほど"),
         rows=[("清掃", "近隣の方に依頼"), ("入室", "スマートロック"), ("問い合わせ", "翻訳とAIチャット"), ("価格", "時期に合わせて調整")]),
]
# サービスのカードの写真（ガイドのカードと同じ写真を使わない。1枚の写真は1か所だけ）
MSERVICE_PHOTOS = {
    "sell": ("u-weathered-roof-house", "瓦屋根の古い空き家（イメージ）"),
    "use": ("u-renovated-engawa", "手を入れた古い家の縁側（イメージ）"),
    "side": ("u-sunlit-tatami", "日の差す畳の客間（イメージ）"),
}


def mfeature_items():
    out, n = [], len(MFEATURES)
    for i, f in enumerate(MFEATURES, 1):
        if f.get("facts"):
            proof = (f'<div class="mfeat__proof mfeat__proof--facts"><p class="mfeat__src">{lines_html(f["src"])}</p><dl class="mfeat__facts">'
                     + "".join(f'<div><dt>{e(k)}</dt><dd class="mfeat__num"><small>{e(pre)}</small>{num}<small>{e(u)}</small></dd></div>'
                               for k, pre, num, u in f["facts"]) + "</dl></div>")
        elif f.get("ways"):
            proof = '<ol class="mfeat__proof mfeat__ways">' + "".join(f'<li><b>{e(w)}</b><span>{e(d)}</span></li>' for w, d in f["ways"]) + "</ol>"
        else:
            a, b, c = f["big"]
            proof = (f'<div class="mfeat__proof"><p class="mfeat__big">{e(a)}<b>{e(b)}</b>{e(c)}</p><dl class="mfeat__rows">'
                     + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in f["rows"]) + "</dl></div>")
        foot = f'<p class="mfeat__cap">{e(f["cap"])}</p>' if f.get("cap") else ""
        if f.get("link"):
            foot += f'<a href="{f["link"][0]}" class="mfeat__link">{e(f["link"][1])} {ARROW}</a>'
        out.append(f"""          <li class="mfeat reveal">
            <p class="mfeat__no">{i:02d}<span class="mfeat__count" aria-hidden="true">{i} / {n}</span></p>
            <h3 class="mfeat__title">{lines_html(f["title"])}</h3>
            <p class="mfeat__text">{e(f["text"])}</p>
            {proof}
            <div class="mfeat__foot">{foot}</div>
          </li>""")
    return "\n".join(out)


def msec_head(en, title, more=""):
    """節の見出し（全部の節で同じ形：小さな英字＋見出し、右に「一覧へ」）"""
    return f'<div class="msec__head reveal"><div><p class="msec__en">{e(en)}</p><h2 class="msec__title">{e(title)}</h2></div>{more}</div>'


def swipe_hint(n, what="件"):
    """スマホで横にスワイプする並びの、枚数と案内（PC では出さない。design-guide 3章）"""
    return f'<p class="mswipe" aria-hidden="true">全{n}{what}・横にスワイプ →</p>'


def media_tabs(current=""):
    """PC のヘッダー下のタブ。読者の状況（ガイド）・記事検索・プランに絞る（残りは右上のメニューに入れる）"""
    items = [(g["key"], f"media/guide-{g['key']}.html", g["label"]) for g in MEDIA_GUIDES] + [("search", "media/search.html", "記事をさがす"), ("plans", "media/plans.html", "アキヤドのプラン")]
    cur = ' aria-current="page"'
    lis = "".join(f'<li><a href="{href}"{cur if k == current else ""}>{e(n)}</a></li>' for k, href, n in items)
    return f"""    <nav class="mtabs" aria-label="アキヤドのガイド">
      <div class="container"><ul class="mtabs__list">{lis}</ul></div>
    </nav>"""


def media_nav(current=""):
    """右上のメニューボタン（3本線）で開くメニュー。ガイドを先に、学ぶ・事例・検索・プランを後に置く（トップへはロゴから戻る）"""
    items = [(g["key"], f"media/guide-{g['key']}.html", g["label"]) for g in MEDIA_GUIDES] + \
            [("learn", "media/learn.html", "基礎から学ぶ"), ("cases", "media.html#cases", "事例から探す"), ("search", "media/search.html", "記事をさがす"), ("plans", "media/plans.html", "アキヤドのプラン")]
    cur = ' aria-current="page"'
    lis = "".join(f'<li><a href="{href}"{cur if k == current else ""}>{e(n)}</a></li>' for k, href, n in items)
    # 相談・資料請求のボタンも入れる
    return f"""    <nav class="mnav" id="mnav" aria-label="アキヤドのメニュー">
      <div class="container"><ul class="mnav__list">{lis}</ul>
        <div class="mnav__ctas">
          <a href="contact.html?from=akiyado-menu" class="mbtn" data-cta="media-menu">無料で相談する {ARROW}</a>
          <a href="contact.html?category=document&amp;from=akiyado-menu" class="mbtn mbtn--sub" data-cta="media-menu-doc">資料をもらう（無料） {ARROW}</a>
          <a href="index.html" class="mnav__corp">運営会社：合同会社RIVIA&amp;CO.</a>
        </div>
      </div>
    </nav>"""


SUPERVISOR = dict(
    key="ishihara", name="石原 佑真", role="合同会社RIVIA&CO. 代表社員", photo="founder-ishihara.jpg",
    links=next(f["profiles"] for f in FOUNDERS if f["key"] == "ishihara"),
    bio="株式会社リクルートの新規事業開発室で事業の立ち上げを経験し、その後ベンチャー企業で新規事業の創出と組織の拡大を牽引。RIVIA&CO.を共同創業し、空き家の再生と宿の運営・開業支援に携わる。",
)
# 初めての方が使いそうな言葉を先に並べる
MEDIA_SEARCH_WORDS = ["相続", "固定資産税", "売却", "貸す", "民泊", "開業資金", "補助金", "改修"]


def search_form(action, value=""):
    """記事検索のフォーム（結果は media/search.html に表示）"""
    return f"""
        <form class="msearch reveal" action="{action}" method="get" role="search">
          <label class="visually-hidden" for="msearch-q">記事をキーワードでさがす</label>
          <input class="msearch__input" id="msearch-q" type="search" name="q" value="{e(value)}" placeholder="キーワード（例：相続、補助金）" autocomplete="off">
          <button class="msearch__btn" type="submit">検索</button>
        </form>"""


def media_hero(en, title, lead, crumbs="", search=""):
    return f"""    <section class="mhero">
      <div class="container">{crumbs}
        <p class="mhero__en reveal">{e(en)}</p>
        <h1 class="mhero__title reveal" data-delay="1">{title}</h1>
        <p class="mhero__lead reveal" data-delay="2">{lines_html(lead)}</p>{search}
      </div>
    </section>"""


def media_search_page():
    """記事検索。全記事の索引（js/media-index.js）をブラウザで絞り込む。公開日前の記事は出さない"""
    import re as _re
    idx = []
    for a in sorted(ARTICLES, key=lambda x: x["date"], reverse=True):
        key = " ".join([a["title"], a["description"], " ".join(a["keypoints"]),
                        " ".join(h for _, h, _ in a["sections"]), " ".join(q for q, _ in a["faq"]),
                        " ".join(MEDIA_CAT_NAMES[t] for t in a["topics"])])
        text = _re.sub(r"<[^>]+>", "", " ".join(h for _, _, h in a["sections"]) + " " + " ".join(ans for _, ans in a["faq"]))
        idx.append(dict(slug=a["slug"], title=a["title"], cat=MEDIA_CAT_NAMES[a["category"]], date=a["date"],
                        thumb=ARTICLE_PHOTOS[a["slug"]][0], desc=a["description"], short=a["short"],
                        key=_re.sub(r"\s+", " ", key), text=_re.sub(r"\s+", " ", text)))
    with open(os.path.join(OUT, "js", "media-index.js"), "w", encoding="utf-8") as f:
        f.write("// アキヤドの記事検索用の索引（build で自動生成。手で編集しない）\nwindow.MEDIA_INDEX = " + json.dumps(idx, ensure_ascii=False) + ";\n")
    chips = "".join(f'<li><a href="media/search.html?q={_quote(w)}">{e(w)}</a></li>' for w in MEDIA_SEARCH_WORDS)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("記事をさがす", "")])
    body = f"""{media_hero("Search", "記事をさがす", "キーワードで、アキヤドの記事をさがせます。", crumbs, search_form("search.html"))}

    <section class="section msec msec--first">
      <div class="container">
        <div class="msearch-words"><p class="msearch-words__label">キーワードの例</p><ul>{chips}</ul></div>
        <h2 class="visually-hidden">検索結果</h2>
        <p class="msearch-status" aria-live="polite"></p>
        <div class="media-grid" id="search-results"></div>
        <div class="msearch-empty" hidden>
          <p>ぴったりの記事が見つかりませんでした。別のキーワードで試すか、状況に合ったガイドから読んでみてください。具体的なご相談には、アキヤドが無料でお答えします。</p>
          <ul>{"".join(f'<li><a href="media/guide-{g["key"]}.html">{e(g["title"])} {ARROW}</a></li>' for g in MEDIA_GUIDES)}</ul>
        </div>
        <div class="msearch-weak" hidden>
          <h3 class="msearch-weak__title"></h3>
          <ul class="msearch-weak__list"></ul>
        </div>
      </div>
    </section>
    <script src="js/media-index.js"></script>

{media_cta()}"""
    page("media/search.html", "記事をさがす｜アキヤド", "アキヤドの記事をキーワードでさがせます。", body, current="media", noindex=True, mnav="search")


def media_crumbs(items):
    """パンくず（最後は現在のページ）"""
    parts = [f'<a href="{h}">{e(n)}</a>' if h else f'<span aria-current="page">{e(n)}</span>' for n, h in items]
    sep = '<span class="crumbs__sep">/</span>'
    return f'\n        <nav class="crumbs" aria-label="パンくずリスト">{sep.join(parts)}</nav>'


def guide_card(g, i):
    worries = "".join(f"<li>{e(w)}</li>" for w in g["worries"])
    return f"""          <a href="media/guide-{g["key"]}.html" class="persona-card reveal" data-delay="{i}">
            <div class="persona-card__photo">{photo(g["photo"], width=720, height=450, sizes="(max-width: 899px) 34vw, 400px")}</div>
            <div class="persona-card__body">
              <p class="persona-card__who">{e(g["who"])}</p>
              <h3 class="persona-card__title">{lines_html(g["label"].replace("を", "を|", 1))}</h3>
              <ul class="persona-card__worries">{worries}</ul>
              <span class="persona-card__more">ガイドを見る {ARROW}</span>
            </div>
          </a>"""


def media_index_page():
    ordered = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in ordered)
    case_cards = "\n".join(article_card(ARTICLE_BY_SLUG[sl]) for sl in CASE_SLUGS)
    n_sv = len(MEDIA_SERVICES)
    service_cards = "".join(f'''<li class="reveal" data-delay="{i}"><a href="media/{sv["slug"]}.html" class="mservice">
          <span class="mservice__img">{photo(MSERVICE_PHOTOS[sv["key"]][0], alt=MSERVICE_PHOTOS[sv["key"]][1], width=720, height=480, sizes="(max-width: 899px) 80vw, 380px")}<span class="mservice__count" aria-hidden="true">{i + 1} / {n_sv}</span></span>
          <span class="mservice__who">{e(sv["eyebrow"])}</span><span class="mservice__name">{e(sv["name"])}</span>
          <span class="mservice__text">{e(sv["lead"])}</span>
          <span class="mservice__more">詳しく見る <span aria-hidden="true"></span></span></a></li>''' for i, sv in enumerate(MEDIA_SERVICES))
    guides = "\n".join(guide_card(g, i) for i, g in enumerate(MEDIA_GUIDES))
    feat_items = mfeature_items()
    labels = {g["key"]: g["label"] for g in MEDIA_GUIDES}
    questions = "\n".join(f"""          <li data-date="{ARTICLE_BY_SLUG[slug]["date"]}"><a href="media/{slug}.html" class="mq__item">
            <span class="mq__who">{e(labels[k])}</span><span class="mq__q">{e(q)}</span><span class="mq__arrow">{ARROW}</span></a></li>""" for k, q, slug in MEDIA_QUESTIONS)
    more = lambda href, label: f'<a href="{href}" class="msec__more">{e(label)} {ARROW}</a>'
    body = f"""    <section class="mtop">
      <figure class="mtop__photo">{photo("u-thatched-village", alt="山あいの集落に建つ茅葺きの家と棚田（イメージ）", width=1920, height=2412, sizes="(max-width: 899px) 100vw, 50vw", lazy=False, priority=True)}</figure>
      <div class="container mtop__inner">
        <div class="mtop__text">
          <p class="mtop__eyebrow reveal">空き家と民泊のメディア「アキヤド」</p>
          <h1 class="mtop__title reveal" data-delay="1"><span class="mtop__line">空き家を</span><span class="mtop__line"><em>売る。活かす。</em></span><span class="mtop__line"><em>民泊</em>をはじめる。</span></h1>
          <p class="mtop__lead reveal" data-delay="1">{lines_html("宿を運営する私たちが、空き家と民泊の悩みに、|実際の数字でお答えします。")}</p>
          <div class="mtop__btns reveal" data-delay="2">
            <a href="contact.html?category=operation&amp;from=akiyado-fv" class="mbtn mtop__btn" data-cta="media-fv">無料で相談する {ARROW}</a>
            <a href="contact.html?category=document&amp;from=akiyado-fv" class="mtop__btn mtop__btn--sub" data-cta="media-fv-doc">資料をダウンロード</a>
          </div>{search_form("media/search.html").replace('class="msearch reveal"', 'class="msearch msearch--top reveal" data-delay="3"').replace('placeholder="キーワード（例：相続、補助金）"', 'placeholder="キーワードで記事をさがす"')}
        </div>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        {msec_head("For you", "ご自身の状況から読む")}
        <p class="msec__lead">{lines_html("いまの状況に近いものを選んでください。知っておきたいことを、悩みが生まれる順に並べたガイドをご用意しています。")}</p>
        <div class="persona-cards">
{guides}
        </div>
      </div>
    </section>

    <section class="section msec mservices" id="services">
      <div class="container">
        {msec_head("Services", "アキヤドのサービス", more("media/plans.html", "プランの条件を見る"))}
        <p class="msec__lead">{lines_html("空き家の状況とご希望に合わせて、個別にご提案しています。")}</p>
        {swipe_hint(n_sv)}
        <ul class="mservice-cards">{service_cards}</ul>
        <p class="mservices__more reveal">相談から開業までの流れは「<a href="media/akiyado-consultation-flow.html">相談から開業までの流れ</a>」で紹介しています。</p>
      </div>
    </section>

    <section class="section section--soft msec mfeatures">
      <div class="container">
        {msec_head("Features", "アキヤドの特徴")}
        {swipe_hint(len(MFEATURES))}
        <ol class="mfeat-list">
{feat_items}
        </ol>
      </div>
    </section>

    <section class="section msec" id="cases">
      <div class="container">
        {msec_head("Cases", "民泊オーナーの事例")}
        <p class="msec__lead">{lines_html("実際に民泊を運営しているオーナーへの取材です。初期費用・月商・純利益と、うまくいかなかったことまで、自分に近い事例から読めます。")}</p>
        {swipe_hint(len(CASE_SLUGS))}
        <div class="media-grid media-grid--scroll" data-limit="{len(CASE_SLUGS)}">
{case_cards}
        </div>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        {msec_head("Questions", "よくある悩みから探す")}
        <ul class="mq reveal">
{questions}
        </ul>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        {msec_head("Learn", "ゼロから体系的に学ぶ", more("media/learn.html", "コースの一覧へ"))}
        <ul class="lcards">{"".join(f'<li class="reveal"><a href="media/learn.html#{c["key"]}" class="lcard"><span class="lcard__en">{e(c["en"])}</span><span class="lcard__title">{e(c["title"])}</span><span class="lcard__text">{e(c["lead"])}</span><span class="lcard__count">全{len(c["chapters"])}章</span></a></li>' for c in MEDIA_COURSES)}</ul>
      </div>
    </section>

    <section class="section msec" id="all">
      <div class="container">
        {msec_head("Latest", "新着記事", more("media/search.html", "記事をさがす"))}
        <div id="themes" class="ttags-wrap reveal"><p class="ttags__label">テーマから探す</p>{theme_tags("all")}</div>
        <div class="media-grid" id="media-list" data-page-size="9">
{cards}
        </div>
        <div class="media-more"><button type="button" class="btn btn--ghost media-more__btn" hidden>もっと記事を見てみる ＋</button></div>
      </div>
    </section>

{media_cta()}"""
    ld = [{
        # アキヤドは rivia-co.com の中のメディア。WebSite（サイト名の宣言）はトップだけに置き、ここではサイトの一部として伝える
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "アキヤド",
        "alternateName": "空き家と民泊のメディア アキヤド",
        "url": f"{SITE}/media.html",
        "inLanguage": "ja",
        "isPartOf": {"@id": WEBSITE_ID},
        "publisher": org_ref(),
        "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/media/{a['slug']}.html"} for a in ordered],
    }, {
        # アキヤドの主なページ（検索結果のサイトリンクの候補になるページを、名前つきで伝える）
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "アキヤドのメニュー",
        "itemListElement": [{"@type": "SiteNavigationElement", "position": i, "name": n, "url": f"{SITE}/{u}"} for i, (n, u) in enumerate([
            ("空き家を手放したい方へ", "media/guide-sell.html"), ("空き家を任せたい方へ", "media/guide-use.html"),
            ("宿をはじめたい方へ", "media/guide-side.html"), ("宿の運営を伸ばしたい方へ", "media/guide-run.html"), ("アキヤドのプラン", "media/plans.html"),
            ("ゼロから体系的に学ぶ", "media/learn.html"), ("無料相談・お問い合わせ", "media/contact.html"),
            ("運営者情報", "media/company.html")], 1)],
    }]
    page("media.html", "アキヤド｜空き家の売却・活用と、副業ではじめる民泊のメディア", "空き家を手放したい方、任せたい方、自分で民泊や小さな宿をはじめたい方、運営を伸ばしたい方に向けて、宿を運営する合同会社RIVIA&CO.が悩みに沿って解説するメディアです。", body, current="media", jsonld=ld, mnav="top")


def theme_tags(current=None, all_href="media.html#all"):
    def tag(href, label, on):
        return f'<li><a href="{href}" class="ttag is-current" aria-current="page">{label}</a></li>' if on else f'<li><a href="{href}" class="ttag">{label}</a></li>'
    items = [tag(all_href, "すべて", current == "all")] + [tag(f"media/category-{k}.html", e(n), current == k) for k, n in MEDIA_CATEGORIES]
    return f'<nav class="ttags" aria-label="テーマから探す"><ul>{"".join(items)}</ul></nav>'


def media_category_page(k, n):
    ordered = sorted((a for a in ARTICLES if k in a["topics"]), key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in ordered)
    g = next((x for x in MEDIA_GUIDES if x["key"] == MEDIA_GUIDE_FOR_CAT.get(k)), None)
    guide_html = f"""
        <a href="media/guide-{g["key"]}.html" class="guide-link reveal">
          <span class="guide-link__label">はじめての方は、ガイドから</span>
          <span class="guide-link__title">{e(g["title"])} {ARROW}</span>
        </a>""" if g else ""
    crumbs = media_crumbs([("アキヤド", "media.html"), (n, "")])
    body = f"""{media_hero(MEDIA_CAT_INFO[k][0], e(n), MEDIA_CAT_INFO[k][1], crumbs, search_form("search.html"))}

    <section class="section msec msec--first">
      <div class="container">
        {theme_tags(k)}{guide_html}
        <h2 class="visually-hidden">{e(n)}の記事</h2>
        <div class="media-grid" id="media-list" data-page-size="12">
{cards}
        </div>
        <p class="media-empty" hidden>このカテゴリの記事は準備中です。</p>
        <div class="media-more"><button type="button" class="btn btn--ghost media-more__btn" hidden>もっと記事を見てみる ＋</button></div>
      </div>
    </section>

{media_cta()}"""
    ld = [{
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TOP", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "アキヤド", "item": f"{SITE}/media.html"},
            {"@type": "ListItem", "position": 3, "name": n},
        ]}]
    page(f"media/category-{k}.html", MEDIA_CAT_TITLE[k], MEDIA_CAT_INFO[k][1], body, current="media", jsonld=ld, mnav="themes")


def media_guide_page(g):
    stages, no = [], 0
    for si, (label, desc, slugs) in enumerate(g["stages"], 1):
        items = []
        for slug in slugs:
            no += 1
            a = ARTICLE_BY_SLUG[slug]
            pn = ARTICLE_PHOTOS[slug][0]
            items.append(f"""            <li class="guide-step reveal" data-date="{a["date"]}">
              <a href="media/{slug}.html" class="guide-step__body" title="{e(a["title"])}">
                <span class="guide-step__no">{no:02d}</span>
                <span class="guide-step__thumb">{photo(pn, alt="", width=720, height=450, sizes="64px")}</span>
                <span class="guide-step__text">
                  <span class="guide-step__title">{e(list_name(a))}</span>
                  <span class="guide-step__more">{e(MEDIA_CAT_NAMES[a["category"]])} ・ 約{read_minutes(a)}分</span>
                </span>
                <span class="guide-step__go" aria-hidden="true">›</span>
              </a>
            </li>""")
        stages.append(f"""        <section class="guide-stage">
          <div class="guide-stage__head reveal"><span class="guide-stage__no">Step {si}</span><h2 class="guide-stage__title">{e(label)}</h2><p class="guide-stage__desc">{e(desc)}</p></div>
          <ol class="guide-steps" data-fold="3">
{chr(10).join(items)}
          </ol>
        </section>""")
    crumbs = media_crumbs([("アキヤド", "media.html"), (g["title"], "")])
    worries = "".join(f"<li>{e(w)}</li>" for w in g["worries"])
    _gc = {"use": ["case-owner-diy-cottage", "case-owner-subsidy-akiya", "case-owner-fishing-port", "case-owner-licensed-akiya"],
           "side": ["case-owner-pricing-mistake", "case-owner-rental-side-business", "case-owner-licensed-akiya", "case-owner-subsidy-akiya"],
           "sell": ["case-owner-diy-cottage"],
           "run": ["case-owner-pricing-mistake", "case-owner-rental-side-business"]}.get(g["key"], [])
    guide_cases = media_section([ARTICLE_BY_SLUG[x] for x in _gc if x in ARTICLE_BY_SLUG], eyebrow="Cases", title="近い事例を読む", lead="実際に民泊を運営しているオーナーへの取材です。", more=False, limit=4, keep_order=True) if _gc else ""
    body = f"""{media_hero("Guide", e(g["title"]), g["lead"], crumbs)}

    <section class="section msec msec--first">
      <div class="container container--article">
        <div class="guide-worries reveal"><p class="guide-worries__label">こんな悩みに答えます</p><ul>{worries}</ul></div>
{chr(10).join(stages)}
      </div>
    </section>

{guide_cases}

{media_cta(g["service"])}"""
    ld = [{
        "@context": "https://schema.org", "@type": "ItemList", "name": g["title"],
        "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{SITE}/media/{s_}.html"} for i, s_ in enumerate(g["slugs"], 1)],
    }]
    ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"}, {"@type": "ListItem", "position": 2, "name": g["title"], "item": f"{SITE}/media/guide-{g['key']}.html"}]})
    page(f"media/guide-{g['key']}.html", f"{g['title']}｜アキヤド", g["lead"], body, current="media", jsonld=ld, mnav=g["key"])
