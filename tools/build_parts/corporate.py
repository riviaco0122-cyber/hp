# -*- coding: utf-8 -*-
# build.py の一部：コーポレート：トップ・会社概要・採用・お問い合わせ・プライバシー・送信完了のページ。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- index
def service_groups_html():
    """事業の一覧（左に届ける価値、右に事業のカード）。トップの「事業紹介」と事業内容のページで共通"""
    names = dict(SERVICES)
    num = 0
    groups_html = []
    # どんな価値を届けるために、どの事業をしているか（左に価値、右に事業。スマホは事業を横スワイプ）
    for g in GROUPS:
        v = TOP_VALUES[g["key"]]
        cards = []
        for i, k in enumerate(g["services"]):
            num += 1
            en, summary, ic = SERVICE_INTRO[k]
            cards.append(f"""            <a href="service-{k}.html" class="vsvc">
              <span class="vsvc__num" aria-hidden="true">{num:02d}</span>
              <span class="vsvc__catch">{e(SERVICE_CATCH[k])}</span>
              <h3 class="vsvc__name">{e(names[k])}</h3>
              <p class="vsvc__text">{e(summary)}</p>
              <span class="vsvc__go" aria-hidden="true"></span>
            </a>""")
        groups_html.append(f"""        <div class="vrow vrow--{len(g["services"])} reveal">
          <div class="vrow__head">
            {photo(v["photo"], cls="vrow__bg", width=v["w"], height=v["h"], sizes="(max-width: 899px) 100vw, 420px")}
            <span class="vrow__en">{e(v["en"])}</span>
            <p class="vrow__value">{v["value"]}</p>
            <p class="vrow__name">{e(g["name"])}</p>
          </div>
          <div class="vrow__list">
{chr(10).join(cards)}
          </div>
        </div>""")
    return "\n".join(groups_html)


# 会社サイトの主要ページ（ヘッダーのメニューと同じ並び・同じ名前）。トップで SiteNavigationElement として伝える
CORP_NAV = [("私たちについて", "about.html"), ("事業内容", "services.html"), ("アキヤド", "media.html"),
            ("採用情報", "careers.html"), ("お問い合わせ", "contact.html")]
CORP_NAV_LD = {"@context": "https://schema.org", "@type": "ItemList", "name": "RIVIA&CO.のメニュー",
               "itemListElement": [{"@type": "SiteNavigationElement", "position": i, "name": n, "url": f"{SITE}/{u}"}
                                   for i, (n, u) in enumerate(CORP_NAV, 1)]}


def index_page():
    vsteps = "\n".join(
        f"""          <li class="vision__step reveal" data-delay="{i - 1}">
            <span class="vision__num">{i:02d}</span>
            <span class="vision__en">{e(en)}</span>
            <h3 class="vision__title">{e(t)}</h3>
            <p class="vision__text">{e(d)}</p>
          </li>"""
        for i, (t, en, d) in enumerate(VISION["steps"], 1)
    )
    vout = "".join(f'<li><span>{e(a)}</span>{e(b)}</li>' for a, b in VISION["outcomes"])
    # TOPはAboutと内容を重ねず、コンセプトと「地域の経済循環」の図だけを見せる
    arrows = "".join(
        f'<path d="M1.5 0-1.2-1.3v2.6z" transform="translate({50 + 36 * math.cos(math.radians(d)):.2f} {50 + 36 * math.sin(math.radians(d)):.2f}) rotate({d + 90})"/>'
        for d in (-45, 45, 135, 225))
    nodes = "\n".join(
        f"""            <li class="cycle__node cycle__node--{i}"><span class="cycle__en">{i:02d} {e(en)}</span><span class="cycle__t"><span>{e(a)}</span><span>{e(b)}</span></span></li>"""
        for i, (en, a, b) in enumerate(TOP_CYCLE, 1))
    vision = f"""    <section class="section vision" id="vision">
      <div class="container">
        <div class="vision__grid">
          <div class="vision__body">
            <div class="reveal">
              <span class="eyebrow">Concept</span>
              <h2 class="vision__copy">{e(TOP_CONCEPT["copy"]).replace("、", "、<br>", 1)}</h2>
            </div>
            <p class="vision__lead vision__lead--pc reveal" data-delay="1">{"".join("<span class=\"vision__sent\">" + "".join(f"<span>{e(c)}</span>" for c in l.split("|")) + "</span>" for l in TOP_CONCEPT["lead"])}</p>
            <p class="vision__lead vision__lead--sp reveal" data-delay="1">{"".join("<span class=\"vision__sent\">" + "".join(f"<span>{e(c)}</span>" for c in l.split("|")) + "</span>" for l in TOP_CONCEPT["lead_sp"])}</p>
          </div>
          <div class="cycle reveal" data-delay="1" role="img" aria-label="空き家を宿に再生し、旅行者がまちを訪れ、まちで食べて買い、ファンになって再び訪れる。その収益で次の空き家を再生する、地域の経済循環">
            <svg class="cycle__ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="36"/>{arrows}</svg>
            <span class="cycle__orbit" aria-hidden="true"><i></i></span>
            <p class="cycle__center" aria-hidden="true"><span class="cycle__center-en">Local cycle</span><span>地域に、</span><span>循環をつくる</span></p>
            <ol class="cycle__nodes" aria-hidden="true">
{nodes}
            </ol>
            <p class="cycle__loop" aria-hidden="true">次の空き家へ</p>
          </div>
          <p class="vision__more reveal" data-delay="2"><a href="about.html">ミッション・ビジョン・バリューを見る {ARROW}</a></p>
        </div>
      </div>
    </section>"""
    cards = service_groups_html()
    reasons = "\n".join(
        f"""          <li class="reason reveal" data-delay="{i - 1}">
            <span class="reason__num">{i:02d}</span>
            <h3 class="reason__title">{e(t)}</h3>
            <p class="reason__text">{e(d)}</p>
            <p class="reason__career"><span>Career</span>{e(c).replace("|", "<wbr>")}</p>
          </li>"""
        for i, (t, d, c) in enumerate(REASONS, 1)
    )
    slides = "\n".join(
        f'        <img class="hero__bg{" is-active" if i == 0 else ""}" src="images/photos/{n}.jpg" alt="" width="{w}" height="{h}" style="object-position:{pos}"'
        + (' fetchpriority="high"' if i == 0 else ' loading="lazy"') + ' decoding="async">'
        for i, (n, w, h, pos) in enumerate(HERO_SLIDES))
    body = f"""    <section class="hero hero--photo hero--x">
      <div class="hero__slides" aria-hidden="true">
{slides}
      </div>
      <div class="container hero__inner">
        <h1 class="hero__title hero__title--x reveal"><span class="ln"><span>地域に眠る</span></span><span class="ln"><span>価値を、</span></span><span class="ln"><span>日本の<em>活力</em>に。</span></span></h1>
        <div class="hero__actions reveal" data-delay="3">
          <a href="#service" class="btn">事業紹介を見る {ARROW}</a>
          <a href="about.html" class="btn btn--ghost btn--on-photo">私たちについて</a>
        </div>
      </div>
      <a href="#vision" class="hero__badge" aria-label="次のセクションへ">
        <svg viewBox="0 0 120 120" aria-hidden="true"><defs><path id="hero-badge-path" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1-92 0"/></defs><text><textPath href="#hero-badge-path" textLength="284" lengthAdjust="spacing">LOCAL VALUE ✳ JAPAN'S ENERGY ✳ RIVIA&amp;CO. ✳</textPath></text></svg>
        <span class="hero__badge-arrow" aria-hidden="true"></span>
      </a>
      <div class="hero__count" aria-hidden="true"><span class="hero__count-n">01</span><i><b></b></i><span>{len(HERO_SLIDES):02d}</span></div>
    </section>

{vision}

    <section class="section">
      <div class="container news">
        <div class="reveal">
          <span class="eyebrow">News &amp; Topics</span>
          <h2 class="section-title">お知らせ</h2>
        </div>
        <ul class="news__list reveal" data-delay="1">
          <li class="news__item">
            <time class="news__date" datetime="2026-09-01">2026.09.01</time>
            <span class="tag">News</span>
            <p class="news__title">合同会社RIVIA&amp;CO.を設立いたしました。</p>
          </li>
        </ul>
      </div>
    </section>

    <section class="section" id="service">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Service</span>
          <h2 class="section-title">事業紹介</h2>
        </div>
{cards}
      </div>
    </section>

    <section class="section reasons-sec">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Why RIVIA</span>
          <h2 class="section-title">RIVIAが選ばれる理由</h2>
          <p class="section-lead">{e(REASONS_LEAD)}</p>
        </div>
        <ol class="reasons">
{reasons}
        </ol>
      </div>
    </section>

    <section class="section section--soft" id="project">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Project</span>
          <h2 class="section-title">運営実績</h2>
        </div>
{project_card()}
{reviews_html()}      </div>
    </section>

{media_intro()}

{flow_section()}

{cta(text=OPEN_MSG)}

    <section class="section">
      <div class="container">
        <a href="careers.html" class="careers-cta reveal">
          <div class="careers-cta__body">
            <p class="careers-cta__title">CAREERS</p>
            <div class="careers-cta__row">
              <span class="pill">年齢・経験は問いません！</span>
              <p class="careers-cta__text">一緒に働く仲間を募集しています。</p>
            </div>
          </div>
          <span class="careers-cta__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M9 5l7 7-7 7"/></svg></span>
        </a>
      </div>
    </section>"""
    org_ld = org_entity()
    page("index.html", "", "地域に眠る価値を、日本の活力に。空き家の再生や民泊の開業・運営から、集客・採用、まちづくりまでを担う合同会社RIVIA&CO.のコーポレートサイトです。", body, jsonld=[org_ld, {"@context": "https://schema.org", "@type": "WebSite", "@id": WEBSITE_ID, "name": "RIVIA&CO.", "alternateName": ["合同会社RIVIA&CO.", "リビアアンドコー"], "url": f"{SITE}/", "inLanguage": "ja", "publisher": {"@id": ORG_ID}}, CORP_NAV_LD])


# ---------------------------------------------------------------- about
# 地図の検索語（本店所在地）
from urllib.parse import quote as _quote
MAP_Q = _quote("東京都足立区青井6-8-8")


def company_profile():
    """会社概要（コーポレートの私たちについてと、アキヤドの運営会社ページで共通）"""
    return [
        ("商号", "合同会社RIVIA&amp;CO. (RIVIA&amp;CO. LLC)"),
        ("設立", "2026年9月1日"),
        ("資本金", "1,000,000円"),
        ("代表社員", "片井 進太 ／ 石原 佑真"),
        ("本店所在地", "〒121-0012<br>東京都足立区青井六丁目8番8号 Grand Maison青井201"),
        ("事業内容", "".join(
            f'<span class="profile__group">{e(g["name"])}</span>' + "<br>".join("・" + e(dict(SERVICES)[k]) for k in g["services"])
            for g in GROUPS)),
    ]


# 創業者（about.html の Founders と、構造化データの Person で共通。事実はここに書いてある内容だけ）
FOUNDERS = [
    dict(key="ishihara", name="石原 佑真", en="Yuma Ishihara", role="代表社員 ／ 共同創業者", origin="大阪府出身", photo="founder-ishihara.jpg", photo_type="photo",
         bio="大阪府出身。新卒で株式会社リクルートに入社し、新規事業開発室にてゼロイチの事業立ち上げを経験。その後、HR Techベンチャー、サイバーセキュリティベンチャーにおいて、一貫して新規事業の創出と組織拡大を牽引。新規事業を立ち上げ、事業と組織を成長させてきた経験と、テクノロジー領域での知見を活かし、RIVIA&CO.を共同創業。",
         career=[("株式会社リクルート", "新規事業開発室にて、ゼロイチの事業立ち上げを経験"),
                 ("HR Techベンチャー", "新規事業の創出と組織拡大を牽引"),
                 ("サイバーセキュリティベンチャー", "新規事業の創出と組織拡大を牽引"),
                 ("合同会社RIVIA&CO.", "共同創業")],
         strengths=["新規事業開発", "事業グロース", "組織拡大", "テクノロジー領域の知見"]),
    dict(key="katai", name="片井 進太", en="Shinta Katai", role="代表社員 ／ 共同創業者", origin="静岡県出身", photo="founder-katai.jpg", photo_type="illust",
         bio="静岡県出身。新卒で静岡県庁に入庁し、行政の視点から地域課題に向き合う。その後、大手メーカー、リクルート、HR Techベンチャーを経て、位置情報データを扱うベンチャー企業に参画。官民両方の視点と、多角的な業界知見、データ分析力を強みに持つ。現在、複数企業の経営にも携わりながらRIVIA&CO.を共同創業。",
         career=[("静岡県庁", "行政の視点から地域課題に向き合う"),
                 ("大手メーカー", ""),
                 ("株式会社リクルート", ""),
                 ("HR Techベンチャー", ""),
                 ("位置情報データベンチャー", "位置情報データを活用した事業に参画"),
                 ("合同会社RIVIA&CO.", "共同創業。現在、複数企業の経営にも携わる")],
         strengths=["官民両方の視点", "多角的な業界知見", "データ分析", "企業経営"]),
]


# 構造化データの @id（Organization・Person は about.html で定義し、ほかのページからは @id で参照する）
ORG_ID = f"{SITE}/about.html#organization"
# サイト名の宣言（WebSite）はトップだけに置き、ほかのページは @id で参照する（同じドメインに名前の違う WebSite を置かない）
WEBSITE_ID = f"{SITE}/#website"


def person_id(key):
    return f"{SITE}/about.html#{key}"


def org_ref():
    """ほかのページから会社を参照するときの Organization（@id ＋ 名前・ロゴ。Article の publisher にも使う）"""
    return {"@type": "Organization", "@id": ORG_ID, "name": "合同会社RIVIA&CO.", "url": f"{SITE}/",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo/logo.png"}}


def founder_person(f):
    """創業者の Person（about.html で定義する本体）。sameAs は SNS を載せない方針なので付けない"""
    return {
        "@type": "Person",
        "@id": person_id(f["key"]),
        "name": f["name"],
        "alternateName": f["en"],
        "jobTitle": ["代表社員", "共同創業者"],
        "description": f["bio"],
        "knowsAbout": f["strengths"],
        "worksFor": {"@id": ORG_ID},
        "image": f"{SITE}/images/{f['photo']}",
        "url": f"{SITE}/about.html#founders",
    }


def org_entity(full_founders=False):
    """会社の Organization 本体。about.html では創業者の Person を中に入れ、トップでは @id で参照する"""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "合同会社RIVIA&CO.",
        "alternateName": "RIVIA&CO. LLC",
        "url": f"{SITE}/",
        "logo": f"{SITE}/images/logo/logo.png",
        "foundingDate": "2026-09-01",
        "founder": [founder_person(f) if full_founders else {"@type": "Person", "@id": person_id(f["key"]), "name": f["name"]}
                    for f in FOUNDERS],
        "address": {
            "@type": "PostalAddress",
            "postalCode": "121-0012",
            "addressRegion": "東京都",
            "addressLocality": "足立区",
            "streetAddress": "青井六丁目8番8号 Grand Maison青井201",
            "addressCountry": "JP",
        },
    }


def about_page():
    founders = FOUNDERS
    fhtml = "\n".join(
        f"""          <article class="founder reveal" data-delay="{i}">
            <div class="founder__head">
              <figure class="founder__photo founder__photo--{f["photo_type"]}"><img src="images/{f["photo"]}" alt="{e(f["name"])}の写真" width="600" height="600" loading="lazy" decoding="async"></figure>
              <div>
                <p class="founder__role">{e(f["role"])}</p>
                <h3 class="founder__name">{e(f["name"])}</h3>
                <p class="founder__en">{e(f["en"])}<span class="founder__origin">{e(f["origin"])}</span></p>
              </div>
            </div>
            <p class="founder__bio">{e(f["bio"])}</p>
            <details class="founder__block spfold" open><summary>経歴を見る</summary>
              <span class="founder__label">経歴</span>
              <ol class="founder__career">
{chr(10).join(f'                <li><strong>{e(c)}</strong>{("<span>" + e(d) + "</span>") if d else ""}</li>' for c, d in f["career"])}
              </ol>
            </details>
            <div class="founder__block">
              <span class="founder__label">強み</span>
              <ul class="founder__tags">{"".join(f"<li>{e(t)}</li>" for t in f["strengths"])}</ul>
            </div>
{sns_html(f)}          </article>"""
        for i, f in enumerate(founders)
    )
    profile = company_profile()
    phtml = "\n".join(f'          <div class="profile__row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in profile)
    prose = "\n".join(
        '          <div class="about-para reveal">' + "".join(f'<p class="about-line" style="--i:{j}">{e(l)}</p>' for j, l in enumerate(para)) + "</div>"
        for para in MISSION_PROSE)
    pillars = "\n".join(
        f"""          <li class="reveal" data-delay="{i - 1}"><span class="about-pillar__num">{i:02d}</span><span class="about-pillar__en">{e(en)}</span><h3>{e(t)}</h3><p class="about-pillar__text">{e(d)}</p></li>"""
        for i, (t, en, d) in enumerate(VISION["steps"], 1))
    values = "\n".join(
        f"""          <li class="reveal" data-delay="{(i - 1) % 2}"><span class="about-value__num">{i:02d}</span><div><h3>{e(t)}</h3><p class="about-value__text">{e(d)}</p></div></li>"""
        for i, (t, d) in enumerate(VALUES, 1))
    import japan_map
    body = f"""    <section class="page-hero page-hero--about page-hero--map">
      <div class="container about-hero">
        <div class="about-hero__text">
          <p class="page-hero__en ttl-x reveal"><span class="ln"><span>About Us</span></span></p>
          <h1 class="page-hero__ja reveal" data-delay="1">私たちについて</h1>
          <p class="about-hero__lead reveal" data-delay="2">東京と静岡を拠点に、<br>全国のまちづくり・地方創生へ。</p>
        </div>
        <div class="jmap reveal" data-delay="1">
          <img class="jmap__dots" src="images/about/japan-dots.svg" alt="" width="{japan_map.W}" height="{japan_map.H}" fetchpriority="high" decoding="async">
          {japan_map.overlay_svg()}
        </div>
      </div>
    </section>

    <section class="section about-sec">
      <div class="container container--narrow">
        <p class="about-big reveal" aria-hidden="true">Mission</p>
        <h2 class="about-copy reveal">{e(MISSION["copy"]).replace("、", "、<br>", 1).replace("日本の活力", "日本の<em>活力</em>", 1)}</h2>
        <div class="about-prose">
{prose}
        </div>
      </div>
    </section>

    <section class="section about-sec about-sec--dark">
      <div class="container">
        <p class="about-big reveal" aria-hidden="true">Vision</p>
        <h2 class="about-copy reveal">{e(VISION["copy"]).replace("滞在を、", "滞在を、<br>", 1).replace("全国のまち", "<em>全国のまち</em>", 1)}</h2>
        <p class="about-note reveal">{e(VISION["lead"])}</p>
        <ol class="about-pillars reveal">
{pillars}
        </ol>
        <ul class="vision__outcomes about-outcomes reveal">{"".join(f'<li><span>{e(x)}</span>{e(y)}</li>' for x, y in VISION["outcomes"])}</ul>
      </div>
    </section>

    <section class="section about-sec">
      <div class="container">
        <p class="about-big reveal" aria-hidden="true">Values</p>
        <h2 class="about-copy reveal">私たちが大切にすること</h2>
        <ul class="about-values">
{values}
        </ul>
      </div>
    </section>

    <section class="section" id="founders">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Founders</span>
          <h2 class="section-title">創業者</h2>
        </div>
        <div class="founders">
{fhtml}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Company Profile</span>
          <h2 class="section-title">会社概要</h2>
        </div>
        <div class="company">
          <dl class="profile reveal">
{phtml}
          </dl>
          <div class="company__map reveal" data-delay="1">
            <p class="company__map-label">本店所在地</p>
            <div class="map">
              <iframe src="https://www.google.com/maps?q={MAP_Q}&amp;output=embed" title="合同会社RIVIA&amp;CO. 本店所在地の地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
            </div>
            <a href="https://www.google.com/maps/search/?api=1&amp;query={MAP_Q}" class="company__map-link" target="_blank" rel="noopener">Googleマップで開く {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

{cta()}"""
    ld = [org_entity(full_founders=True),
          {"@context": "https://schema.org", "@type": "AboutPage", "name": "私たちについて・会社概要", "url": f"{SITE}/about.html",
           "about": {"@id": ORG_ID}, "mainEntity": {"@id": ORG_ID}}]
    page("about.html", "私たちについて・会社概要", "合同会社RIVIA&CO.のミッション・ビジョン・バリュー、創業者紹介、会社概要です。空き家の再生と宿の運営を担う会社の考え方を紹介します。", body, current="about", jsonld=ld)


# ---------------------------------------------------------------- forms
UPLOAD = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v4h16v-4"/></svg>'


def file_box(name, title, hint, accept, attrs="", cls="", indent="            "):
    """ファイルの添付欄（点線の枠。選んだファイル名は js/main.js が file__name に出す）。全フォームで共通"""
    i = indent
    return f"""{i}<label class="file{(" " + cls) if cls else ""}">
{i}  <input type="file" name="{name}" accept="{accept}"{(" " + attrs) if attrs else ""}>
{i}  {UPLOAD}
{i}  <span class="file__title">{title}</span>
{i}  <span class="file__name" data-default="{hint}">{hint}</span>
{i}</label>"""


# メールマガジンの受け取りの同意（任意・初期状態はチェックなし＝特定電子メール法のオプトイン）。
# 値は tools/forms/Code.gs がスプレッドシートの「メルマガ」列に記録する（配信そのものは今後、配信サービスにつなぐ）
NEWSLETTER_LABEL = "RIVIA&amp;CO.からのお知らせ（空き家活用・民泊のメールマガジン）を受け取る"
NEWSLETTER_NOTE = "いつでも配信停止できます。"


def consent(id_, newsletter=False):
    news = f"""
            <div class="form__optin">
              <label class="check" for="{id_}-news">
                <input type="checkbox" id="{id_}-news" name="newsletter" value="希望する">
                <span>{NEWSLETTER_LABEL} <span class="opt">任意</span></span>
              </label>
              <p class="form__optin-note">{NEWSLETTER_NOTE}</p>
            </div>""" if newsletter else ""
    return f"""          <div class="form__consent">
            <label class="check" for="{id_}">
              <input type="checkbox" id="{id_}" name="privacy_agree" value="同意する" required>
              <span><a href="privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>に同意する <span class="req">必須</span></span>
            </label>{news}
          </div>"""


def careers_page():
    def career_file(name, title):
        return file_box(name, title, "クリックまたはドラッグ&amp;ドロップでファイルを選択", ".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png", attrs="required")

    body = f"""    <section class="page-hero page-hero--contact">
      <div class="container">
        <p class="page-hero__en ttl-x reveal"><span class="ln"><span>Careers</span></span></p>
        <h1 class="page-hero__ja reveal" data-delay="1">採用情報</h1>
        <p class="page-hero__lead reveal" data-delay="2">一緒に働く仲間を募集しています。<br>年齢・経験は問いません。お気軽にご連絡ください。</p>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <div class="section-head reveal">
          <span class="eyebrow">Entry</span>
          <h2 class="section-title">エントリーフォーム</h2>
        </div>
        <form class="form form--steps reveal" action="https://script.google.com/macros/s/AKfycbx-SeTX9iRu6f45DUkCBj28vYeyQZnXH-958CJ6XYU0y7Ie1Pn1hDV1ahcyxWaBX3Uc/exec" method="POST" enctype="multipart/form-data" data-thanks="thanks.html?form=careers">
          <input type="text" name="_hp" class="hp-field" tabindex="-1" autocomplete="off" data-lpignore="true" data-1p-ignore aria-hidden="true">
          <input type="hidden" name="_subject" value="【RIVIA&amp;CO.】採用エントリー">
          <div class="form__field">
            <label for="c-name">お名前 <span class="req">必須</span></label>
            <input type="text" id="c-name" name="name" placeholder="名字 名前" autocomplete="name" required>
          </div>
          <div class="form__field">
            <label for="c-email">Email <span class="req">必須</span></label>
            <input type="email" id="c-email" name="email" placeholder="Email@address" autocomplete="email" required>
          </div>
          <div class="form__field">
            <label for="c-detail">詳細 <span class="req">必須</span></label>
            <textarea id="c-detail" name="detail" placeholder="志望動機や希望年収、思っていることを教えてください。" required></textarea>
          </div>
          <fieldset class="form__field form__fieldset">
            <legend class="form__legend">添付ファイル <span class="req">必須</span></legend>
            <p class="form__notes form__notes--above">職務経歴書・履歴書を添付してください。</p>
            <div class="files">
{career_file("resume", "職務経歴書")}
{career_file("cv", "履歴書")}
            </div>
          </fieldset>
{consent("c-agree")}
          <div class="form__submit"><button type="submit" class="btn btn--lg">送信する {ARROW}</button></div>
        </form>
      </div>
    </section>"""
    page("careers.html", "採用情報", "合同会社RIVIA&CO.の採用情報です。年齢・経験は問いません。空き家の再生や宿の運営に、一緒に関わる仲間を募集しています。", body, current="careers")


def contact_page():
    # 「サービス資料の請求」の値は tools/forms/Code.gs の DOC_REQUEST_VALUES（資料の自動添付の判定）と一致させる
    short = {"operation": "空き家再生", "management": "開業・運営支援", "partnership": "不動産協業",
             "marketing": "WEB集客", "recruit": "WEB採用"}
    # ご相談カテゴリ：まずお客様の立場（個人／法人）を選び、その立場の「〜したい」から選ぶ（ナビと同じ NAV_INTENTS）
    names = dict(SERVICES)
    who_keys = ["personal", "corporate"]
    tabs = "".join(
        f'<button type="button" class="catpick__tab" role="tab" data-who="{who_keys[i]}" aria-selected="{"true" if i == 0 else "false"}">'
        f'<span class="catpick__tab-en">{"Personal" if i == 0 else "Business"}</span>{e(aud)}</button>'
        for i, (aud, _its) in enumerate(NAV_INTENTS))
    # 物件をどうするか決まっていない相談がいちばん多いので、どちらの立場にも先頭に置く（値は「物件の相談」）
    property_card = {"personal": ("持っている物件について相談したい", "売る・貸す・宿にする、どれが良いかから一緒に考えます"),
                     "corporate": ("保有物件について相談したい", "活かし方・売り方・運営の任せ方から一緒に考えます")}
    def card(value, key, intent, sub, extra=""):
        return (f'<label class="catpick__card{extra}"><input type="radio" name="category" value="{value}" data-key="{key}">'
                f'<span class="catpick__body"><span class="catpick__intent">{e(intent)}</span><span class="catpick__svc">{e(sub)}</span></span>'
                f'<span class="catpick__check" aria-hidden="true"></span></label>')
    panels = "\n".join(
        f'            <div class="catpick__panel" role="tabpanel" data-who="{who_keys[i]}" aria-label="{e(aud)}">'
        + card("物件の相談", "property", *property_card[who_keys[i]], extra=" catpick__card--wide")
        + "".join(card(short[k], k, t, names[k]) for k, t in its)
        + "</div>"
        for i, (aud, its) in enumerate(NAV_INTENTS))
    more = (card("サービス資料の請求", "document", "まずは資料がほしい", "サービス資料をメールでお送りします", extra=" catpick__card--sub")
            + card("その他", "other", "その他のご相談", "取材・ご提案・そのほかのお問い合わせ", extra=" catpick__card--sub"))
    catpick = f"""          <fieldset class="form__field form__fieldset catpick">
            <legend class="form__legend">ご相談カテゴリ <span class="opt">任意</span></legend>
            <p class="form__notes form__notes--above">あてはまるものを選ぶと、お問い合わせ内容に書き出しが入ります。</p>
            <div class="catpick__tabs" role="tablist" aria-label="お客様の立場">{tabs}</div>
{panels}
            <p class="catpick__more-label">ほかのご用件</p>
            <div class="catpick__more">{more}</div>
          </fieldset>"""
    body = f"""    <section class="page-hero page-hero--contact">
      <div class="container">
        <p class="page-hero__en ttl-x reveal"><span class="ln"><span>Contact</span></span></p>
        <h1 class="page-hero__ja reveal" data-delay="1">お問い合わせ</h1>
        <p class="page-hero__lead reveal" data-delay="2">観光地でなくても、収益物件になり得ます。<br>お気軽にお問い合わせください。</p>
        <p class="page-hero__area reveal" data-delay="2"><span>対応エリア</span>全国可</p>
        <ul class="assure reveal" data-delay="3">
          <li>ご相談・お見積りは無料</li>
          <li>無理な営業は一切なし</li>
          <li>2営業日以内にご連絡</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <form class="form form--steps reveal" action="https://script.google.com/macros/s/AKfycbx-SeTX9iRu6f45DUkCBj28vYeyQZnXH-958CJ6XYU0y7Ie1Pn1hDV1ahcyxWaBX3Uc/exec" method="POST" enctype="multipart/form-data" data-thanks="thanks.html?form=contact">
          <input type="text" name="_hp" class="hp-field" tabindex="-1" autocomplete="off" data-lpignore="true" data-1p-ignore aria-hidden="true">
          <input type="hidden" name="_subject" value="【RIVIA&amp;CO.】Webサイトからのお問い合わせ">
          <input type="hidden" name="流入元" id="from-field" value="">
          <div class="form__step">
            <p class="form__step-head"><span>01</span>ご相談の内容</p>
{catpick}
          </div>
          <div class="form__step">
            <p class="form__step-head"><span>02</span>ご連絡先</p>
            <div class="form__grid">
          <div class="form__field">
            <label for="name">お名前 <span class="req">必須</span></label>
            <input type="text" id="name" name="name" placeholder="山田 太郎" autocomplete="name" required>
          </div>
          <div class="form__field">
            <label for="company">会社名・施設名 <span class="opt">任意</span></label>
            <input type="text" id="company" name="company" placeholder="個人の方は空欄で構いません" autocomplete="organization">
          </div>
          <div class="form__field">
            <label for="tel">電話番号 <span class="req">必須</span></label>
            <input type="tel" id="tel" name="tel" placeholder="090-1234-5678" autocomplete="tel" inputmode="tel" pattern="[0-9０-９+\\-－ー\\(\\)（） ]{{10,}}" title="電話番号を数字で入力してください（例：090-1234-5678）" required>
          </div>
          <div class="form__field">
            <label for="email">メールアドレス <span class="req">必須</span></label>
            <input type="email" id="email" name="email" placeholder="your@email.com" autocomplete="email" required>
          </div>
            </div>
          </div>
          <div class="form__step">
            <p class="form__step-head"><span>03</span>くわしく教えてください</p>
          <div class="form__field">
            <label for="message">お問い合わせ内容 <span class="req">必須</span></label>
            <textarea id="message" name="message" placeholder="ご相談内容をご記入ください。まだ考えがまとまっていない段階でも構いません。" required></textarea>
          </div>
          <fieldset class="form__field form__fieldset">
            <legend class="form__legend">添付ファイル <span class="opt">任意</span></legend>
            <p class="form__notes form__notes--above">物件の資料・写真・図面などがあれば添付してください。PDF・画像・Word・Excelなど、合計10MBまでを目安にお送りください。</p>
{file_box("attachment", "ファイルを添付する", "クリックまたはドラッグ&amp;ドロップでファイルを選択（複数可）", ".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.jpg,.jpeg,.png,.heic", attrs="multiple")}
          </fieldset>
          </div>
{consent("agree", newsletter=True)}
          <div class="form__notes">
            <p>※無理な営業や電話勧誘は一切いたしません。</p>
            <p>※ご入力いただいた情報は厳重に管理し、お問い合わせ対応以外には使用いたしません。</p>
          </div>
          <div class="form__submit"><button type="submit" class="btn btn--lg">送信する {ARROW}</button></div>
        </form>
      </div>
    </section>

{flow_section(soft=True)}"""
    page("contact.html", "お問い合わせ", "合同会社RIVIA&CO.へのお問い合わせはこちらから。ご相談は無料です。2営業日以内に担当者よりご連絡いたします。", body, current="contact")


# ---------------------------------------------------------------- privacy
PRIVACY = [
    ("個人情報の取得", "当社は、お問い合わせフォームおよび採用エントリーフォームを通じて、氏名、会社名・施設名、電話番号、メールアドレス、お問い合わせ内容、職務経歴書・履歴書その他ご本人が入力・送付された情報を、適正な手段により取得します。"),
    ("利用目的", "取得した個人情報は、次の目的の範囲内で利用します。<br>（1）お問い合わせ・ご相談への回答およびご連絡<br>（2）当社サービスのご提案、お見積り、契約の締結・履行<br>（3）採用選考および採用に関するご連絡<br>（4）上記に付随する業務"),
    ("第三者提供", "当社は、法令に基づく場合を除き、ご本人の同意を得ることなく個人情報を第三者に提供しません。"),
    ("業務の委託", "当社は、利用目的の達成に必要な範囲で、フォーム送信サービス等の外部事業者に個人情報の取扱いを委託することがあります。この場合、委託先に対して必要かつ適切な監督を行います。"),
    ("アクセス解析ツールについて", "当社ウェブサイトでは、利用状況の把握とサイト改善のため、Google LLC が提供するアクセス解析ツール「Google アナリティクス」を利用しています。Google アナリティクスは Cookie を使用して、個人を特定しない形でトラフィックデータを収集します。この機能は、ブラウザの設定で Cookie を無効にすることで拒否できます。詳しくは <a href=\"https://marketingplatform.google.com/about/analytics/terms/jp/\" target=\"_blank\" rel=\"noopener\">Google アナリティクス利用規約</a> および <a href=\"https://policies.google.com/technologies/partner-sites?hl=ja\" target=\"_blank\" rel=\"noopener\">Google のポリシーと規約</a> をご覧ください。"),
    ("安全管理措置", "当社は、個人情報の漏えい、滅失またはき損の防止その他の安全管理のために、必要かつ適切な措置を講じます。"),
    ("開示・訂正・利用停止等", "ご本人から個人情報の開示、訂正、追加、削除、利用停止等のご請求があった場合は、ご本人であることを確認のうえ、法令に従い遅滞なく対応します。"),
    ("お問い合わせ窓口", "個人情報の取扱いに関するお問い合わせは、<a href=\"contact.html\">お問い合わせフォーム</a>よりご連絡ください。<br>合同会社RIVIA&amp;CO.<br>〒121-0012 東京都足立区青井六丁目8番8号 Grand Maison青井201"),
    ("改定", "当社は、必要に応じて本ポリシーを改定することがあります。改定後の内容は、本ページに掲載した時点から効力を生じるものとします。"),
]


def privacy_page():
    items = "\n".join(
        f"""          <section class="policy__item">
            <h2>{i}. {e(t)}</h2>
            <p>{b}</p>
          </section>"""
        for i, (t, b) in enumerate(PRIVACY, 1)
    )
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en reveal">Privacy Policy</p>
        <h1 class="page-hero__ja reveal" data-delay="1">プライバシーポリシー</h1>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <!-- 本ポリシーは一般的なひな形です。公開前に内容をご確認ください。 -->
        <p class="policy__intro">合同会社RIVIA&amp;CO.（以下「当社」）は、お客様の個人情報を適切に取り扱うことが社会的責務であると考え、個人情報の保護に関する法律その他の関係法令を遵守し、以下のとおり個人情報を取り扱います。</p>
        <div class="policy">
{items}
        </div>
        <p class="policy__date">制定日：2026年9月1日</p>
      </div>
    </section>"""
    page("privacy.html", "プライバシーポリシー", "合同会社RIVIA&CO.のプライバシーポリシー（個人情報の取扱いについて）です。お問い合わせなどで取得する個人情報の扱いを定めています。", body)

def thanks_page():
    """フォーム送信後の完了ページ。GA4 では generate_lead イベントを「キーイベント（コンバージョン）」に設定して計測する"""
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en reveal">Thank you</p>
        <h1 class="page-hero__ja reveal" data-delay="1">送信が完了しました</h1>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow thanks">
        <p class="thanks__lead reveal">送信いただき、ありがとうございます。<br>内容を確認のうえ、2営業日以内に担当者よりご連絡いたします。</p>
        <p class="thanks__note reveal">連絡が届かない場合は、迷惑メールフォルダもご確認ください。</p>
        <div class="thanks__actions reveal">
          <a href="index.html" class="btn">トップページへ戻る {ARROW}</a>
          <a href="media.html" class="btn btn--ghost">アキヤドを読む</a>
        </div>
      </div>
    </section>
    <script>
      // フォーム送信の完了を GA4 に記録（どのフォームからかを form_type、相談か資料請求かを lead_type で区別。lead は js/main.js が付ける）
      if (typeof gtag === 'function') {{
        var q = new URLSearchParams(location.search), form = q.get('form') || 'contact';
        gtag('event', 'generate_lead', {{ form_type: form, lead_type: q.get('lead') || (form === 'careers' ? 'careers' : 'consult') }});
      }}
    </script>"""
    page("thanks.html", "送信完了", "お問い合わせを受け付けました。", body, noindex=True)
