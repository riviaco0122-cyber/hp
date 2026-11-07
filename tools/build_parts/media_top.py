# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：ナビ・トップ・テーマ別・ガイド・検索のページ。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

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
              <h3 class="persona-card__title">{e(g["label"])}</h3>
              <ul class="persona-card__worries">{worries}</ul>
              <span class="persona-card__more">ガイドを見る {ARROW}</span>
            </div>
          </a>"""


def media_index_page():
    ordered = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in ordered)
    case_cards = "\n".join(article_card(ARTICLE_BY_SLUG[sl]) for sl in CASE_SLUGS)
    # ファーストビューの「主な事例」: 自分たちの運営事例と、オーナー取材の事例（新しい順）。アイキャッチの画像で見せる
    top_cases = [ARTICLE_BY_SLUG[sl] for sl in ["case-rental-house-inn-first-year"] + CASE_SLUGS if sl in ARTICLE_BY_SLUG]
    top_case_cards = "\n".join(f'''            <a href="media/{a["slug"]}.html" class="mtop-case" data-date="{a["date"]}">
              <span class="mtop-case__img"><img src="{eyecatch_path(a)}" alt="" width="1200" height="630" loading="{"eager" if i < 2 else "lazy"}" decoding="async"></span>
              <span class="mtop-case__body"><span class="mtop-case__tag">{"運営事例" if not a["slug"].startswith("case-owner-") else "オーナー取材"}</span><span class="mtop-case__title">{e(a["title"])}</span></span>
            </a>''' for i, a in enumerate(top_cases))
    _guide = {g["key"]: g for g in MEDIA_GUIDES}
    service_cards = "".join(f'''<li class="reveal" data-delay="{i}"><a href="media/{sv["slug"]}.html" class="mservice">
          <span class="mservice__img">{photo(_guide[sv["key"]]["photo"], width=720, height=450, sizes="(max-width: 899px) 100vw, 360px")}</span>
          <span class="mservice__who">{e(sv["eyebrow"])}</span><span class="mservice__name">{e(sv["name"])}</span>
          <span class="mservice__text">{e(sv["lead"])}</span>
          <span class="mservice__more">詳しく見る <span aria-hidden="true">›</span></span></a></li>''' for i, sv in enumerate(MEDIA_SERVICES))
    guides = "\n".join(guide_card(g, i) for i, g in enumerate(MEDIA_GUIDES))
    labels = {g["key"]: g["label"] for g in MEDIA_GUIDES}
    questions = "\n".join(f"""          <li data-date="{ARTICLE_BY_SLUG[slug]["date"]}"><a href="media/{slug}.html" class="mq__item">
            <span class="mq__who">{e(labels[k])}</span><span class="mq__q">{e(q)}</span><span class="mq__arrow">{ARROW}</span></a></li>""" for k, q, slug in MEDIA_QUESTIONS)
    entries = "".join(f'<li><a href="media/guide-{g["key"]}.html">{e(g["label"])} {ARROW}</a></li>' for g in MEDIA_GUIDES)
    tiles = "".join(
        f'<li><a href="media/guide-{g["key"]}.html" class="mtile"><span class="mtile__img">{photo(g["photo"], width=720, height=450, sizes="72px")}</span>'
        f'<span class="mtile__label">{e(g["label"])}</span><span class="mtile__arrow" aria-hidden="true">→</span></a></li>' for g in MEDIA_GUIDES)
    body = f"""    <section class="mtop">
      <div class="container mtop__inner">
        <div class="mtop__text">
          <p class="mtop__eyebrow reveal">空き家と民泊のメディア「アキヤド」</p>
          <h1 class="mtop__title reveal" data-delay="1"><span class="mtop__line">空き家を</span><span class="mtop__line"><em>売る。活かす。</em></span><span class="mtop__line"><em>民泊</em>をはじめる。</span></h1>
          <p class="mtop__lead reveal" data-delay="1">{lines_html("宿を運営する私たちが、空き家と民泊の悩みに、実際の数字でお答えします。")}</p>
          <div class="mtop__btns reveal" data-delay="2">
            <a href="contact.html?category=operation&amp;from=akiyado-fv" class="mbtn mtop__btn" data-cta="media-fv">無料で相談する {ARROW}</a>
            <a href="contact.html?category=document&amp;from=akiyado-fv" class="mtop__btn mtop__btn--sub" data-cta="media-fv-doc">資料をダウンロード</a>
          </div>{search_form("media/search.html").replace('class="msearch reveal"', 'class="msearch msearch--top reveal" data-delay="3"').replace('placeholder="キーワード（例：相続、補助金）"', 'placeholder="キーワードで記事をさがす"')}
          <ul class="mtop__chips reveal" data-delay="3">{"".join(f'<li><a href="media/guide-{g["key"]}.html">{e(g["label"])}</a></li>' for g in MEDIA_GUIDES)}</ul>
        </div>
        <div class="mtop__cases reveal" data-delay="2" data-carousel>
          <div class="mtop__cases-head">
            <p class="mtop__cases-label">取材した<b>主な事例</b></p>
            <div class="mtop__nav">
              <button type="button" class="mtop__arrow" data-dir="-1" aria-label="前の事例">‹</button>
              <span class="mtop__count" aria-live="polite"><span data-cur>1</span> / <span data-total>{len(top_cases)}</span></span>
              <button type="button" class="mtop__arrow" data-dir="1" aria-label="次の事例">›</button>
            </div>
          </div>
          <div class="mtop__track" tabindex="0" aria-label="主な事例（横にスワイプ）">
{top_case_cards}
          </div>
        </div>
      </div>
    </section>

    <section class="section msec mservices" id="services">
      <div class="container">
        <div class="mcenter-head reveal"><p class="msec__en">Services</p><h2 class="mcenter-head__title">アキヤドのサービス</h2><p class="mcenter-head__lead">{lines_html("空き家の状況とご希望に合わせて、個別にご提案しています。")}</p></div>
        <ul class="mservice-cards">{service_cards}</ul>
        <p class="mservices__more reveal">プランごとの条件の目安は「<a href="media/plans.html">アキヤドのプラン</a>」、相談から開業までの流れは「<a href="media/akiyado-consultation-flow.html">相談から開業までの流れ</a>」で紹介しています。</p>
      </div>
    </section>

    <section class="section msec mfeatures">
      <div class="container">
        <div class="mcenter-head reveal"><p class="msec__en">Features</p><h2 class="mcenter-head__title">アキヤドの特徴</h2></div>
        <ul class="mfeat-cards">
          <li class="mfeat reveal">
            <p class="mfeat__head"><span class="mfeat__no">01</span>宿を運営する<br>当事者が答える</p>
            <div class="mfeat__fig">
              <p class="mfeat-case">運営している宿の一例<span>静岡県下田市・一棟貸し</span></p>
              <div class="mfeat-stats">
                <div class="mfeat-stat"><svg class="mfeat-donut" viewBox="0 0 42 42" aria-hidden="true"><circle cx="21" cy="21" r="16" pathLength="100"/><circle class="mfeat-donut__v" cx="21" cy="21" r="16" pathLength="100" stroke-dasharray="53 47"/></svg><p class="mfeat-stat__n"><small class="mfeat-stat__pre">約</small>53<small>%</small></p><p class="mfeat-stat__k">1年目の稼働率</p></div>
                <div class="mfeat-stat"><p class="mfeat-stat__n mfeat-stat__n--top"><small class="mfeat-stat__pre">約</small>14<small>か月</small></p><span class="mfeat-bar" aria-hidden="true"><i></i></span><p class="mfeat-stat__k">開業費用をほぼ回収</p></div>
              </div>
            </div>
            <p class="mfeat__text">{lines_html("記事の数字もご提案の見込みも、私たちの運営記録が元です。")}</p>
          </li>
          <li class="mfeat reveal" data-delay="1">
            <p class="mfeat__head"><span class="mfeat__no">02</span>売る・貸す・はじめるを<br>並べて比べられる</p>
            <div class="mfeat__fig">
              <p class="mfeat-pill">あなたの空き家</p>
              <svg class="mfeat-branch" viewBox="0 0 300 36" preserveAspectRatio="none" aria-hidden="true"><path d="M150 0v12M50 36V22a10 10 0 0 1 10-10h180a10 10 0 0 1 10 10v14M150 12v24"/></svg>
              <div class="mfeat-three">
                <p><span class="mfeat-three__no">1</span><b>売る</b>売却額の目安</p>
                <p><span class="mfeat-three__no">2</span><b>借り上げ</b>家を残して収入</p>
                <p><span class="mfeat-three__no">3</span><b>自分で運営</b>宿の収支見込み</p>
              </div>
              <svg class="mfeat-branch mfeat-branch--in" viewBox="0 0 300 36" preserveAspectRatio="none" aria-hidden="true"><path d="M50 0v14a10 10 0 0 0 10 10h180a10 10 0 0 0 10-10V0M150 0v36"/></svg>
              <p class="mfeat-goal"><span>ご家族が<b>納得できる方法</b>を選べる</span></p>
            </div>
            <p class="mfeat__text">{lines_html("3つの見込みを、並べてお出しします。")}</p>
            <p class="mfeat__note">※ 収益を保証するものではありません。</p>
          </li>
          <li class="mfeat reveal" data-delay="2">
            <p class="mfeat__head"><span class="mfeat__no">03</span>遠方の家でも<br>回る運営の仕組み</p>
            <div class="mfeat__fig">
              <p class="mfeat-big"><span>現地に行くのは</span><b>数か月に1回</b><span>ほど</span></p>
              <ul class="mfeat-rows">
                <li><span class="mfeat-rows__k">清掃</span><b>近隣の方に依頼</b></li>
                <li><span class="mfeat-rows__k">入室</span><b>スマートロック</b></li>
                <li><span class="mfeat-rows__k">問い合わせ</span><b>翻訳とAIチャット</b></li>
                <li><span class="mfeat-rows__k">価格</span><b>時期に合わせて調整</b></li>
              </ul>
            </div>
            <p class="mfeat__text">{lines_html("開業2か月目には、行かなくても回る体制にしました。")}</p>
          </li>
        </ul>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">For you</p><h2 class="msec__title">ご自身の状況から読む</h2></div></div>
        <p class="msec__lead">{lines_html("いまの状況に近いものを選んでください。知っておきたいことを、悩みが生まれる順に並べたガイドをご用意しています。")}</p>
        <div class="persona-cards">
{guides}
        </div>
      </div>
    </section>

    <section class="section msec" id="cases">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Cases</p><h2 class="msec__title">民泊オーナーの事例</h2></div></div>
        <p class="msec__lead">{lines_html("実際に民泊を運営しているオーナーへの取材です。初期費用・月商・純利益と、うまくいかなかったことまで、自分に近い事例から読めます。")}</p>
        <div class="media-grid media-grid--scroll" data-limit="{len(CASE_SLUGS)}">
{case_cards}
        </div>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Questions</p><h2 class="msec__title">よくある悩みから探す</h2></div></div>
        <ul class="mq reveal">
{questions}
        </ul>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Learn</p><h2 class="msec__title">ゼロから体系的に学ぶ</h2></div><a href="media/learn.html" class="msec__more">コースの一覧へ {ARROW}</a></div>
        <ul class="lcards">{"".join(f'<li class="reveal"><a href="media/learn.html#{c["key"]}" class="lcard"><span class="lcard__en">{e(c["en"])}</span><span class="lcard__title">{e(c["title"])}</span><span class="lcard__text">{e(c["lead"])}</span><span class="lcard__count">全{len(c["chapters"])}章</span></a></li>' for c in MEDIA_COURSES)}</ul>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Latest</p><h2 class="msec__title">新着記事</h2></div></div>
        <div class="media-grid media-grid--feature" data-limit="4">
{cards}
        </div>
      </div>
    </section>

    <section class="section msec" id="all">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Archive</p><h2 class="msec__title">すべての記事</h2></div></div>
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
