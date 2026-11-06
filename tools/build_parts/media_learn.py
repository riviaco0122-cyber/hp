# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：基礎から学ぶ（learn.html）。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- アキヤド：基礎から学ぶ（記事を、コースと章の順に並べて体系的に学べるようにする）
MEDIA_COURSES = [
    dict(key="why-akiya", en="Course 01", title="なぜ今、空き家の活用なのか", lead="空き家の今と、放置したときの負担、制度の変化。活かし方を比べて、家族で決めるまで。",
         chapters=[("空き家の今を知る", "数字で見る空き家と、活用が注目されている理由。", ["why-akiya-utilization-now"]),
                   ("放置のリスクと制度の変化", "空家法の改正、相続登記の義務化、持ち続ける費用。", ["akiya-law-kanri-fuzen", "souzoku-touki-gimuka", "akiya-holding-costs", "akiya-inherited-house-to-inn"]),
                   ("活かし方を比べる", "売る・貸す・宿にするの違いと、契約や税の基本。", ["akiya-utilization-options", "akiya-lease-types", "akiya-demolish-or-renovate", "akiya-3000man-deduction", "akiya-bank-guide"]),
                   ("家族で決める", "相続した実家を、家族でどう決めるか。", ["inherited-house-family-talk"])]),
    dict(key="why-minpaku", en="Course 02", title="なぜ民泊・小さな宿なのか", lead="空き家の活かし方のなかで、宿が選ばれる理由。旅の変化と、向いている家、収益の考え方。",
         chapters=[("空き家と宿の相性", "宿が選ばれる理由と、賃貸との収入の違い。", ["why-minpaku-for-akiya", "minpaku-vs-rental-income"]),
                   ("旅の変化と需要", "訪日客の動向、地方への分散、長期滞在の広がり。", ["japan-tourism-market-data", "long-stay-travel-demand"]),
                   ("古い家・地方だからこその価値", "古民家の魅力と、観光地でなくても宿になる理由。", ["shizuoka-yaizu-akiya-inn"]),
                   ("向いている家を見極める", "立地・建物・法令・運営のチェックと、中古と新築の違い。", ["akiya-minpaku-suitability", "new-build-vs-used-house-inn"]),
                   ("収益の考え方", "指標の読み方、収益の試算、投資としての見方、運営の事例。", ["inn-kpi-basics", "minpaku-break-even", "airdna-revenue-simulation", "minpaku-investment-yield", "case-rental-house-inn-first-year"])]),
    dict(key="challenges", en="Course 03", title="民泊の課題と、乗り越え方", lead="「民泊は大変」と言われる理由と、実際の乗り越え方。手続き、お金、運営、集客まで。",
         chapters=[("よく聞く課題を知る", "手続き・近隣・運営・季節・費用の5つの課題。", ["minpaku-hard-truth"]),
                   ("制度と手続き", "民泊と旅館業の違い、開業までの流れ、会社員の副業の確認、消防。", ["minpaku-vs-ryokan-law", "minpaku-start-steps", "minpaku-180days-rule", "kaishain-minpaku-fukugyo", "minpaku-chintai-start", "kani-shukusho-kyoka-guide", "minpaku-fire-safety"]),
                   ("お金と改修", "開業資金、補助金、改修の進め方、宿泊税。", ["inn-startup-funding", "small-inn-subsidies", "kominka-renovation-points", "remote-renovation-tips", "accommodation-tax"]),
                   ("運営の課題", "近隣との関係、ハウスガイド、設備、清掃、清掃を頼む人、閑散期、遠方からの運営、津波注意報のとき。", ["minpaku-neighbor-rules", "minpaku-house-guide", "long-stay-guest-equipment", "minpaku-bihin-priority", "cleaning-linen-operations", "minpaku-seisou-kojin-kakunin", "minpaku-off-season", "minpaku-remote-operation", "tsunami-advisory-guest-response"]),
                   ("集客と評価", "予約サイトの使い方、予約ページ、レビュー。", ["minpaku-shukyaku-first-steps", "ota-vs-direct-booking", "listing-photo-tips", "guest-review-tips"]),
                   ("オーナーの事例", "民泊オーナーへの取材。費用、収支、うまくいかなかったこと。", CASE_SLUGS)]),
    dict(key="akiyado", en="Course 04", title="アキヤドが支援できること", lead="買取・借り上げ・開業と運営の支援。任せる相手の選び方と、相談から開業までの流れ。",
         chapters=[("アキヤドができること", "3つのプランと、相談すると分かること。", ["akiyado-what-we-do"]),
                   ("任せ方を選ぶ", "相談先・委託先の選び方と、管理業者の役割。", ["minpaku-management-company"]),
                   ("相談から開業まで", "初回の相談で聞かれること、準備しておくもの。", ["akiyado-consultation-flow"])]),
]


def media_learn_page():
    jump = "".join(f'<li><a href="#{c["key"]}" class="ttag">{e(c["title"])}</a></li>' for c in MEDIA_COURSES)
    courses = []
    for c in MEDIA_COURSES:
        chs = []
        for i, (t, d, slugs) in enumerate(c["chapters"], 1):
            # 記事への行は、短いキャッチ＋「読む →」で、押せることが一目で分かるようにする
            links = "".join(f'<li data-date="{ARTICLE_BY_SLUG[sl]["date"]}"><a href="media/{sl}.html" class="lchap__link" title="{e(ARTICLE_BY_SLUG[sl]["title"])}">'
                            f'<span class="lchap__ltext"><span class="lchap__name">{e(list_name(ARTICLE_BY_SLUG[sl]))}</span></span><span class="lchap__go">読む {ARROW}</span></a></li>' for sl in slugs)
            chs.append(f"""            <li class="lchap reveal">
              <p class="lchap__no">第{i}章</p>
              <div class="lchap__body">
                <h3 class="lchap__title">{e(t)}</h3>
                <p class="lchap__text">{e(d)}</p>
                <ul class="lchap__list">{links}</ul>
              </div>
            </li>""")
        courses.append(f"""        <section class="lcourse" id="{c["key"]}" aria-labelledby="course-{c["key"]}">
          <div class="lcourse__head reveal">
            <p class="lcourse__en">{e(c["en"])}</p>
            <h2 class="lcourse__title" id="course-{c["key"]}">{e(c["title"])}</h2>
            <p class="lcourse__lead">{e(c["lead"])}</p>
          </div>
          <ol class="lchaps">
{chr(10).join(chs)}
          </ol>
        </section>""")
    crumbs = media_crumbs([("アキヤド", "media.html"), ("基礎から学ぶ", "")])
    body = f"""{media_hero("Learn", "空き家と民泊を、ゼロから体系的に学ぶ", "なぜ空き家を活かすのか、なぜ宿なのか、どんな課題があるのか、アキヤドに何を任せられるのか。4つのコースに、学ぶ順番で記事を並べました。", crumbs, search_form("search.html"))}

    <section class="section msec msec--first">
      <div class="container">
        <nav class="ttags lcourse__jump reveal" aria-label="コース"><ul>{jump}</ul></nav>
{chr(10).join(courses[:2])}
        <div class="msv-band reveal">
          <p class="msv-band__text">読んで具体的に考えたくなったら、アキヤドにご相談ください。<br class="pc-only">ご相談・資料のお届けは無料です。</p>
          <div class="msv-band__btns">
            <a href="contact.html?from=akiyado-learn" class="mbtn" data-cta="media-learn">無料で相談する {ARROW}</a>
            {plan_doc_link("learn")}
          </div>
        </div>
{chr(10).join(courses[2:])}
      </div>
    </section>

{media_cta()}"""
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"},
        {"@type": "ListItem", "position": 2, "name": "基礎から学ぶ"}]}]
    page("media/learn.html", "空き家と民泊をゼロから学ぶ｜アキヤド",
         "なぜ今、空き家の活用なのか。なぜ民泊・小さな宿なのか。民泊の課題と乗り越え方。アキヤドが支援できること。4つのコースで、空き家と民泊を体系的に学べます。",
         body, current="media", jsonld=ld, mnav="learn")
