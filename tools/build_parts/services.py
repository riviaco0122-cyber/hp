# -*- coding: utf-8 -*-
# build.py の一部：コーポレート：しくみの図・対応エリア・かんたんフォームと、サービス一覧・サービスごとのページ。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- しくみ（左から右へ流れるシンプルな図）
# nodes: (アイコン, 名前, 役割)  links: (契約の種類, 右へ流れるもの, 左へ戻るもの)
FLOWS = {
    "operation": dict(
        nodes=[("key", "オーナー様", "空き家の所有者"), ("sparkle", "RIVIA", "改修・宿の運営"), ("users", "ゲスト", "宿泊者")],
        links=[("賃貸借契約 または 売却", "物件を貸す・売る", "家賃・売却代金"), ("宿泊予約", "暮らすように旅する滞在", "宿泊料金")],
        note="改修費はRIVIAが負担することも可能です",
    ),
    "management": dict(
        nodes=[("key", "オーナー様", "投資家・不動産会社"), ("sparkle", "RIVIA", "開業準備・運営"), ("users", "ゲスト", "宿泊者")],
        links=[("運営委託契約", "開業・運営を委託", "売上を分配（手数料を差し引き）"), ("宿泊予約", "集客・おもてなし", "宿泊料金")],
        note="物件の取得・改修はオーナー様のご負担です（共同出資も可能）",
    ),
    "partnership": dict(
        nodes=[("house", "不動産会社様", "物件の販売"), ("users", "投資家様", "物件の購入・保有"), ("sparkle", "RIVIA", "開業準備・運営")],
        links=[("売買契約", "民泊向きの物件を販売", "売買代金"), ("運営委託契約", "購入後の運営を委託", "家賃・収益をお返し")],
        note="販売しにくかった物件も、民泊としての利回りを示すことで売れる商品になります",
    ),
}


def flow_html(key):
    f = FLOWS[key]
    parts = []
    for i, (ic, title, role) in enumerate(f["nodes"]):
        if i:
            pill, fwd, back = f["links"][i - 1]
            parts.append(f"""<div class="sflow__link">
              <span class="sflow__pill">{e(pill)}</span>
              <span class="sflow__fwd">{e(fwd)}</span>
              {f'<span class="sflow__back">{e(back)}</span>' if back else ''}
            </div>""")
        rivia = " sflow__node--rivia" if title == "RIVIA" else ""
        parts.append(f"""<div class="sflow__node{rivia}">
              <p class="sflow__title">{e(title)}</p>
              <p class="sflow__role">{e(role)}</p>
            </div>""")
    return f"""<div class="sflow">
            {"".join(parts)}
          </div>
          <p class="sflow__note">{e(f["note"])}</p>"""


# ---------------------------------------------------------------- 協業スキーム（三角形の図）
TRIANGLES = {
    "partnership": dict(
        title="協業のしくみ",
        lead="RIVIAが物件を見極め、不動産会社様が投資家様へご案内し、購入後はRIVIAが運営を担います。",
        nodes=dict(
            top=("PARTNER", "RIVIA", "物件の選定・開業・運営", ["保有物件から民泊に適した物件を選定", "利回りを算出し、販売用の資料を用意", "購入後の開業準備と日々の運営"], "rivia"),
            left=("REAL ESTATE", "不動産会社様", "投資家様へのご案内・販売", ["説明会・メールマガジンで投資家様へご案内", "物件の販売"], "owner"),
            right=("INVESTOR", "投資家様", "物件の購入・保有", ["物件を購入し、運営をRIVIAへ", "家賃・収益を受け取る"], "investor"),
        ),
        edges=[
            ("left", [("① 民泊に適した物件の選定・利回りの算出", "fwd")], False),
            ("bottom", [("② 説明会・メールマガジンでご案内し、販売", "fwd")], False),
            ("right", [("③ 運営をRIVIAへ", "fwd"), ("④ 家賃・収益をお返し", "rev")], False),
        ],
        note="※ 投資家様向けの説明会は、ご要望に応じてRIVIAも登壇・実施します。",
        summary="不動産会社様・投資家様・RIVIAの三者それぞれにメリットのある協業です。",
    ),
}


def triangle_section(key):
    if key not in TRIANGLES:
        return ""
    t = TRIANGLES[key]
    return f"""    <section class="section section--soft" id="scheme">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Scheme</span>
          <h2 class="section-title">{e(t["title"])}</h2>
          <p class="section-lead">{e(t["lead"])}</p>
        </div>
        <div class="scheme reveal">
          {flow_html(key) if key in FLOWS else tri_html(t["nodes"], t["edges"])}
        </div>
        <p class="plans__note">{e(t["note"])}</p>
        <p class="scheme__summary reveal">{e(t["summary"])}</p>
      </div>
    </section>

"""


# 対応エリア（全国可。今後の展開に合わせて、具体的な地域名は出さない）
AREA_NOTE = {
    "webmarketing": "オンライン対応",
}


def area_html(key):
    g = next(g["key"] for g in GROUPS if key in g["services"])
    note = AREA_NOTE.get(g)
    return f'<p class="area-note reveal" data-delay="2"><span>対応エリア</span>全国可{"・" + e(note) if note else ""}</p>'


def quick_form(key, name):
    """かんたんな相談フォーム（名前とメールだけで送れる。アキヤドのサービス紹介ページで使う）"""
    return f"""        <form class="qform reveal" data-delay="2" action="https://script.google.com/macros/s/AKfycbx-SeTX9iRu6f45DUkCBj28vYeyQZnXH-958CJ6XYU0y7Ie1Pn1hDV1ahcyxWaBX3Uc/exec" method="POST" enctype="multipart/form-data" data-thanks="thanks.html?form=contact">
          <p class="qform__title">{e(name)}の無料相談</p>
          <p class="qform__lead">まだ検討中の段階でも大丈夫です。2営業日以内にご連絡します。</p>
          <input type="text" name="_hp" class="hp-field" tabindex="-1" autocomplete="off" data-lpignore="true" data-1p-ignore aria-hidden="true">
          <input type="hidden" name="_subject" value="【RIVIA&amp;CO.】{e(name)}のご相談（サービスページ）">
          <input type="hidden" name="ご相談カテゴリ" value="{e(name)}">
          <input type="hidden" name="流入元" value="サービスページ：{e(name)}">
          <label class="qform__field"><span>お名前 <em>必須</em></span><input type="text" name="name" placeholder="山田 太郎" autocomplete="name" required></label>
          <label class="qform__field"><span>メールアドレス <em>必須</em></span><input type="email" name="email" placeholder="your@email.com" autocomplete="email" required></label>
          <label class="qform__field"><span>ご相談内容 <small>任意</small></span><textarea name="message" rows="3" placeholder="物件の場所や、気になっていることなど"></textarea></label>
          <div class="qform__field qform__file"><span>ファイル <small>任意・物件の写真や図面など</small></span>
{file_box("attachment", "ファイルを添付する", "写真・図面など（複数可・合計10MBまで）", "image/*,.pdf,.doc,.docx,.xls,.xlsx", attrs="multiple", cls="file--compact", indent="            ")}
          </div>
          <button type="submit" class="btn qform__submit">無料で相談する {ARROW}</button>
          <p class="qform__note">送信により<a href="privacy.html">プライバシーポリシー</a>に同意したものとします。しつこい営業はしません。</p>
        </form>"""


def services_page():
    """事業内容の一覧ページ。メニューの「事業内容」と同じ名前の1ページを置き、5つの事業をその下の階層として見せる"""
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en ttl-x reveal"><span class="ln"><span>Service</span></span></p>
        <h1 class="page-hero__ja reveal" data-delay="1">事業内容</h1>
        <p class="page-hero__lead reveal" data-delay="2">宿泊施設の運営・開業と、WEBマーケティング支援。<br>2つの軸で、5つの事業を行っています。</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
{service_groups_html()}
      </div>
    </section>

{flow_section(soft=True)}

{cta(text=OPEN_MSG)}"""
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "事業内容", "url": f"{SITE}/services.html",
           "isPartOf": {"@id": f"{SITE}/#website"},
           "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i, "name": n, "url": f"{SITE}/service-{k}.html"} for i, (k, n) in enumerate(SERVICES, 1)]}}]
    page("services.html", "事業内容",
         "合同会社RIVIA&CO.の事業内容です。空き家再生、宿泊施設の開業・運営支援、不動産事業者様との協業、WEB集客支援、WEB採用支援の5つの事業を紹介します。",
         body, current="services", jsonld=ld)


def service_page(key, name):
    d = SERVICE_DATA[key]


    # 個人のお客様向けのサービスは「経営」ではなく、暮らしの言葉で見せる
    personal = key in dict((a["key"], [k for _, ks in a["groups"] for k in ks]) for a in NAV_AUDIENCES)["personal"]
    lbl = (dict(label="お悩み", scene="よくあるお声", kpi="変わること") if personal else
           dict(label="経営課題", scene="現場で起きていること", kpi="改善する経営指標"))
    issues = []
    for i, it in enumerate(d["issues"], 1):
        solve = "".join(f'<li><span class="issue__step-num">{n}</span><p>{e(p)}</p></li>' for n, p in enumerate(it["solve"], 1))
        kpi = "".join(f"<li>{e(k)}</li>" for k in it["kpi"])
        issues.append(f"""          <article class="issue reveal">
            <div class="issue__problem">
              <div class="issue__head">
                <span class="issue__mark" aria-hidden="true">{i:02d}</span>
                <p class="issue__meta"><span class="issue__num">ISSUE<span class="issue__n"> {i:02d}</span></span><span class="issue__label">{lbl["label"]}</span></p>
              </div>
              <h3 class="issue__title">{e(it["title"])}</h3>
            </div>
            <div class="issue__scene">
                <span class="issue__avatar issue__avatar--guest" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="8.5" r="3.6"/><path d="M4.8 20c.9-3.9 3.7-6 7.2-6s6.3 2.1 7.2 6"/></svg></span>
                <span class="issue__sublabel">{lbl["scene"]}</span>
                <p class="issue__voice">{e(it["voice"])}</p>
            </div>
            <div class="issue__answer">
              <span class="issue__avatar issue__avatar--rivia" aria-hidden="true">R</span>
              <span class="issue__sublabel issue__sublabel--accent">RIVIAの打ち手</span>
              <div class="issue__reply">
                <ol class="issue__steps">{solve}</ol>
              </div>
              <div class="issue__kpi">
                <span class="issue__sublabel">{lbl["kpi"]}</span>
                <ul>{kpi}</ul>
              </div>
            </div>
          </article>""")
    issues_html = "\n".join(issues)

    steps = "\n".join(
        f"""          <li class="timeline__step reveal" data-delay="{i - 1}">
            <span class="timeline__num">STEP {i:02d}{f'<span class="timeline__for timeline__for--{"inv" if "投資家" in st[3] else "re"}">{e(st[3])}</span>' if len(st) > 3 else ""}</span>
            <h3 class="timeline__title">{e(st[0])}</h3>
            <span class="timeline__term">{e(st[1])}</span>
            <p class="timeline__desc">{e(st[2])}</p>
          </li>"""
        for i, st in enumerate(d["steps"], 1)
    )

    names = dict(SERVICES)
    related_groups = []
    for g in GROUPS:
        cards = "\n".join(
            f"""            <a href="service-{k}.html" class="related__card reveal">
              <span class="related__worry">「{e(PERSONAS[k])}」</span>
              <span class="related__name">{e(names[k])} {ARROW}</span>
            </a>"""
            for k in g["services"] if k != key
        )
        if not cards:
            continue
        own = key in g["services"]
        label = g["name"]
        related_groups.append((not own, f"""        <div class="related-group">
          <p class="group-label"><span>{e(g["en"])}</span>{e(label)}</p>
          <div class="related">
{cards}
          </div>
        </div>"""))
    # 同じ領域を先に表示
    related_groups.sort(key=lambda t: t[0])
    related = "\n".join(h for _, h in related_groups)

    shots = SERVICE_COLLAGE[key]
    collage = "".join(
        photo(n, cls=f"collage__img collage__img--{i}", width=w, height=h, sizes="(max-width: 899px) 60vw, 420px",
              lazy=False, priority=(i == 0)).replace("<img ", f'<img style="object-position:{pos}" ', 1)
        for i, (n, w, h, pos) in enumerate(shots))
    body = f"""    <section class="page-hero page-hero--collage">
      <div class="container svc-hero">
        <div class="collage reveal" aria-hidden="true">{collage}<p class="collage__v">{e(SERVICE_VERTICAL[key])}</p></div>
        <div class="svc-hero__text" data-no="{[k for k, _ in SERVICES].index(key) + 1:02d}">
          <div class="svc-name reveal"><span class="svc-name__no">Service {[k for k, _ in SERVICES].index(key) + 1:02d}</span><h1 class="svc-name__ja">{" ".join(f'<span class="nw">{e(w)}</span>' for w in name.split(" "))}</h1></div>
          <p class="page-hero__lead svc-hero__lead reveal" data-delay="1">{e(d["overview"])}</p>
          <p class="page-hero__target reveal" data-delay="2"><span>こんな方へ</span>「{e(PERSONAS[key])}」</p>
          {area_html(key)}
        </div>
      </div>
    </section>

    <section class="section section--soft" id="{key}-issues">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Issues &amp; Solutions</span>
          <h2 class="section-title">こんなお悩みはありませんか？</h2>
          <p class="section-lead">{e(d["issues_lead"])}</p>
        </div>
        <div class="issues">
{issues_html}
        </div>
      </div>
    </section>

    <section class="section" id="flow">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Process</span>
          <h2 class="section-title">ご支援の流れ（一例）</h2>
          <p class="section-lead">内容や期間は、お選びいただくプランや状況によって変わります。</p>
        </div>
        <ol class="timeline">
{steps}
        </ol>
      </div>
    </section>

{plans_section(key)}{triangle_section(key)}    <section class="section" id="project">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Project</span>
          <h2 class="section-title">RIVIAの運営実績</h2>
        </div>
{project_card(compact=True)}
{reviews_html()}      </div>
    </section>

{cta(key, text=OPEN_MSG if key in GROUPS[0]["services"] else "")}

    <section class="section" id="faq">
      <div class="container container--narrow">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">FAQ</span>
          <h2 class="section-title">よくあるご質問</h2>
        </div>
        <div class="faq reveal">
{faq_html(d["faq"])}
        </div>
      </div>
    </section>

{media_section([a for a in ARTICLES if key in a["services"]], eyebrow="Media", title="関連する記事", lead="このサービスに関連するテーマを、「アキヤド」で詳しく解説しています。") if any(key in a["services"] for a in ARTICLES) else ""}

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Other Services</span>
          <h2 class="section-title">そのほかのサービス</h2>
        </div>
{related}
      </div>
    </section>"""

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]
        ],
    }
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "name": "事業内容", "item": f"{SITE}/services.html"}, {"@type": "ListItem", "name": name}]}
    page(f"service-{key}.html", name, d["description"], body, current=key, jsonld=[faq_ld, crumbs])
