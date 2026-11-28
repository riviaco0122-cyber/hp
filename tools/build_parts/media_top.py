# アキヤドのトップ（2026-11-28 3回目の作り直し。企画は docs/design-guide.md 9章）。
# 読み手は空き家・民泊の初心者。ページの仕事は ①3秒で「何のメディアか」と「自分はどこから読むか」を決めてもらう
# ②「宿を運営する当事者」が書いていると信じてもらう ③あとは事例・学ぶ・新着・相談へ流す、の3つ。
# 節は役割ごとに形を変える：表紙（写真＋目次）／当事者の記録（濃い帯・実物の写真・大きな数字）／事例（大きな1本＋一覧）／
# はじめての方へ（学ぶと悩みの2つの目次）／新着（カードの格子はここだけ）／3つの道（サービスの比較）／相談。

# 当事者の記録：数字は全部、私たちが運営する下田の宿のもの。どの宿の・いつの数字かを、数字の下に必ず書く
# （イメージ写真の宿の数字に見せない。写真はこの宿の実物だけを使う）
MRECORD_FACTS = [
    ("約", "53", "%", "1年目の稼働率", "開業1年目の月ごとの平均（開業月を除く）"),
    ("約", "14", "か月", "初期投資をほぼ回収", "約14か月で、初期投資の約98%を回収"),
    ("数か月に", "1", "回ほど", "現地に行くのは、いま", "清掃は近隣の方、入室はスマートロック。遠方から運営しています"),
]
# 3つの道（サービス）：道の名前と、何の見込みを出すか。MEDIA_SERVICES と同じ順番（買取・借り上げ・開業運営）
MWAYS = {"sell": ("売る", "売却額の目安"), "use": ("借り上げ", "家を残して収入"), "side": ("自分で運営", "宿の収支見込み")}


def msec_head(en, title, more=""):
    """節の見出し（全部の節で同じ形：小さな英字＋見出し、右に「一覧へ」）"""
    return f'<div class="msec__head reveal"><div><p class="msec__en">{e(en)}</p><h2 class="msec__title">{e(title)}</h2></div>{more}</div>'


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


def mcase_item(a, lead=False):
    """事例の1本。lead=True は大きな写真と要約つきの1本（特集）、それ以外は小さな写真の一覧の1行"""
    name, alt = ARTICLE_PHOTOS[a["slug"]]
    title = e("".join(l.strip() for l in a["short"].split("\n")))
    cat = f'<span class="mcase__cat">{e(MEDIA_CAT_NAMES[a["category"]])}</span>'
    date = f'<time class="mcase__date" datetime="{a["date"]}">{fmt_date(a["date"])}</time>'
    if lead:
        return f"""<a href="media/{a["slug"]}.html" class="mcase mcase--lead reveal">
          <span class="mcase__photo">{photo(name, alt=alt, width=1200, height=900, sizes="(max-width: 899px) 100vw, 680px")}</span>
          <span class="mcase__body">{cat}<span class="mcase__title">{title}</span><span class="mcase__text">{e(a["description"])}</span>{date}</span>
        </a>"""
    return f"""<li data-date="{a["date"]}"><a href="media/{a["slug"]}.html" class="mcase">
            <span class="mcase__photo">{photo(name, alt="", width=360, height=270, sizes="120px")}</span>
            <span class="mcase__body">{cat}<span class="mcase__title">{title}</span>{date}</span>
          </a></li>"""


def media_index_page():
    ordered = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in ordered)
    more = lambda href, label: f'<a href="{href}" class="msec__more">{e(label)} {ARROW}</a>'

    # 1. 表紙：写真の上に「何のメディアか」を言い切り、すぐ下の目次で自分の状況を選ぶ（最初の行動はこれ1つ）
    index = "\n".join(f"""          <li><a href="media/guide-{g["key"]}.html" class="mindex__item" data-cta="media-fv-guide">
            <span class="mindex__no" aria-hidden="true">{i:02d}</span><span class="mindex__label">{e(g["label"])}</span>
            <span class="mindex__who">{e(g["who"])}</span><span class="mindex__go">{ARROW}</span></a></li>""" for i, g in enumerate(MEDIA_GUIDES, 1))
    # 2. 当事者の記録：実物の写真と、大きな数字。数字ごとに、どの宿の・いつの数字かを添える
    facts = "\n".join(f"""            <div class="mrecord__fact"><dt>{e(label)}</dt><dd class="mrecord__num">{f'<small class="mrecord__pre">{e(pre)}</small>' if pre else ""}{num}{f"<small>{e(unit)}</small>" if unit else ""}</dd><dd class="mrecord__note">{e(note)}</dd></div>"""
                      for pre, num, unit, label, note in MRECORD_FACTS)
    # 3. 事例：いちばん新しい1本を大きく、残りは小さな写真の一覧（スマホは先頭の4件、残りはボタンで開く）
    cases = [ARTICLE_BY_SLUG[sl] for sl in CASE_SLUGS]
    case_rest = "\n".join(mcase_item(a) for a in cases[1:])
    # 4. はじめての方へ：体系的に学ぶコースと、よくある悩み（どちらも目次の形）
    courses = "".join(f"""<li class="reveal"><a href="media/learn.html#{c["key"]}" class="mcourse">
            <span class="mcourse__no" aria-hidden="true">{i:02d}</span><span class="mcourse__title">{e(c["title"])}</span>
            <span class="mcourse__text">{e(c["lead"])}</span><span class="mcourse__count">全{len(c["chapters"])}章</span></a></li>""" for i, c in enumerate(MEDIA_COURSES, 1))
    labels = {g["key"]: g["label"] for g in MEDIA_GUIDES}
    questions = "\n".join(f"""          <li data-date="{ARTICLE_BY_SLUG[slug]["date"]}"><a href="media/{slug}.html" class="mq__item">
            <span class="mq__who">{e(labels[k])}</span><span class="mq__q">{e(q)}</span><span class="mq__arrow">{ARROW}</span></a></li>""" for k, q, slug in MEDIA_QUESTIONS)
    # 5. 3つの道：売る・借り上げ・自分で運営を、同じ物差しで横に並べる（カードの写真は使わない。比べる表の形）
    ways = "".join(f"""<li class="reveal" data-delay="{i}"><a href="media/{sv["slug"]}.html" class="mway">
          <span class="mway__no" aria-hidden="true">{i + 1:02d}</span><span class="mway__word">{e(MWAYS[sv["key"]][0])}</span><span class="mway__what">{e(MWAYS[sv["key"]][1])}</span>
          <span class="mway__who">{e(sv["eyebrow"])}</span><span class="mway__name">{e(sv["name"])}</span>
          <span class="mway__text">{e(sv["lead"])}</span><span class="mway__more">詳しく見る {ARROW}</span></a></li>""" for i, sv in enumerate(MEDIA_SERVICES))
    shimoda = ARTICLE_BY_SLUG["case-rental-house-inn-first-year"]
    body = f"""    <section class="mcover">
      <div class="mcover__visual">
        <figure class="mcover__photo">{photo("u-thatched-terraces", alt="棚田の奥に建つ茅葺きの家と、山の森（イメージ）", width=1920, height=1080, sizes="100vw", lazy=False, priority=True)}</figure>
        <div class="container mcover__text">
          <p class="mcover__eyebrow reveal">空き家と民泊のメディア「アキヤド」</p>
          <h1 class="mcover__title reveal" data-delay="1"><span class="mcover__line">空き家を</span><span class="mcover__line"><em>売る。活か{pe("す。")}</em></span><span class="mcover__line"><em>民泊</em>をはじめ{pe("る。")}</span></h1>
          <p class="mcover__lead reveal" data-delay="2">{lines_html("宿を運営する私たちが、空き家と民泊の悩みに、|実際の数字でお答えします。")}</p>
        </div>
      </div>
      <div class="container mcover__index">
        <nav class="mindex reveal" data-delay="2" aria-labelledby="mindex-title">
          <div class="mindex__head"><h2 class="mindex__title" id="mindex-title">ご自身の状況から読む</h2><p class="mindex__lead">いまの状況に近いものを選んでください。悩みが生まれる順に、記事を並べたガイドです。</p></div>
          <ol class="mindex__list">
{index}
          </ol>
        </nav>
        <p class="mcover__sub"><span>まだ決めていない段階でも大丈夫です。</span>
          <a href="contact.html?category=operation&amp;from=akiyado-fv" data-cta="media-fv">無料で相談する {ARROW}</a>
          <a href="contact.html?category=document&amp;from=akiyado-fv" data-cta="media-fv-doc">資料をダウンロード {ARROW}</a></p>
      </div>
    </section>

    <section class="section section--dark msec mrecord" id="record">
      <div class="container mrecord__grid">
        <figure class="mrecord__photo reveal">
          <img src="images/photos/node-shimoda.avif" alt="NODE Shimoda のリビング。白い壁と木の床に、ソファとローテーブル" width="1440" height="960" loading="lazy" decoding="async">
          <figcaption>私たちが運営する宿「NODE Shimoda」（静岡県下田市・アパートの一室を貸切）</figcaption>
        </figure>
        <div class="mrecord__body">
          <div class="msec__head reveal"><div><p class="msec__en">Our record</p><h2 class="msec__title">{lines_html("宿を運営する当事者が、|書いています。")}</h2></div></div>
          <p class="mrecord__lead reveal">記事の数字もご提案の見込みも、私たちの運営記録が元です。</p>
          <dl class="mrecord__facts reveal">
{facts}
          </dl>
          <p class="mrecord__src">数字はすべて、写真の宿（静岡県下田市）の運営記録です。収益を保証するものではありません。</p>
          <a href="media/{shimoda["slug"]}.html" class="mrecord__link">この宿の運営事例を読む {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="section msec mcases" id="cases">
      <div class="container">
        {msec_head("Cases", "民泊オーナーの事例")}
        <p class="msec__lead">{lines_html("実際に民泊を運営しているオーナーへの取材です。初期費用・月商・純利益と、うまくいかなかったことまで、自分に近い事例から読めます。")}</p>
        <div class="mcases__grid">
        {mcase_item(cases[0], lead=True)}
        <ul class="mcases__list reveal" data-fold-sp="4">
{case_rest}
        </ul>
        </div>
      </div>
    </section>

    <section class="section section--soft msec mstart" id="learn">
      <div class="container mstart__grid">
        <div class="mstart__col">
          {msec_head("Learn", "ゼロから体系的に学ぶ", more("media/learn.html", "コースの一覧へ"))}
          <ol class="mcourses">{courses}</ol>
        </div>
        <div class="mstart__col" id="questions">
          {msec_head("Questions", "よくある悩みから探す")}
          <ul class="mq reveal" data-fold-sp="5">
{questions}
          </ul>
        </div>
      </div>
    </section>

    <section class="section msec mways-sec" id="services">
      <div class="container">
        {msec_head("Services", "アキヤドのサービス", more("media/plans.html", "プランの条件を見る"))}
        <p class="msec__lead">{lines_html("空き家の状況とご希望に合わせて、個別にご提案しています。売却・借り上げ・自分で運営の見込みを、並べてお出しします。")}</p>
        <ol class="mways">{ways}</ol>
        <p class="mways__note reveal">※ 収益を保証するものではありません。相談から開業までの流れは「<a href="media/akiyado-consultation-flow.html">相談から開業までの流れ</a>」で紹介しています。</p>
      </div>
    </section>

    <section class="section section--soft msec" id="all">
      <div class="container">
        {msec_head("Latest", "新着記事")}
        {search_form("media/search.html").replace('placeholder="キーワード（例：相続、補助金）"', 'placeholder="キーワードで記事をさがす"')}
        <div id="themes" class="ttags-wrap reveal"><p class="ttags__label">テーマから探す</p>{theme_tags("all")}</div>
        <div class="media-grid" id="media-list" data-page-size="9" data-page-size-sp="5">
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
