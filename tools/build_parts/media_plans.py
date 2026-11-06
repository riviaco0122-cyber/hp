# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：プランのページと、ご相談の解説動画。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- アキヤド：アキヤドのプラン（記事を読んだ人が「頼んだらどうなるか」を知る場所）
# 実際のお客様の声がそろうまでは公開しない（作り話の口コミは、景品表示法の優良誤認やステマ規制に触れるおそれがある）
SHOW_SAMPLE_VOICES = os.environ.get("SHOW_SAMPLE_VOICES") == "1"
SAMPLE_VOICES = [
    ("use", "60代・相続した実家を活用", "アキヤドおまかせプラン",
     "固定資産税と草刈りのためだけに通っていた実家が、毎月の家賃を生む宿になりました。改修の段取りも運営もお任せできたので、私がしたのは契約と、ときどき届くレポートを読むことくらいです。"),
    ("side", "40代・会社員・副業で開業", "伴走コース",
     "届出の順番、写真の撮り方、料金の決め方まで一緒に考えてもらえました。平日は本業に集中して、週末にゲストとの時間を楽しめています。ひとりで始めていたら、途中で止まっていたと思います。"),
    ("sell", "70代・遠方の空き家を売却", "アキヤド買取プラン",
     "遠くて管理に行けず、ずっと気がかりでした。現地を見てもらい、売る場合と貸す場合の両方を説明してもらったうえで、納得して手放せました。家が宿として使われると聞いて、ほっとしています。"),
]
MEDIA_PLAN_GROUPS = [
    ("sell", "空き家を売りたい方", "手放したいけれど、買い手がつくか不安。そんな家もご相談ください。", "operation", ["アキヤド買取プラン"]),
    ("use", "空き家を活かしたい方", "家は持ったまま、宿として活かして収入に。改修や運営の手間はかかりません。", "operation", ["アキヤドおまかせプラン", "アキヤド売上シェアプラン"]),
    ("side", "副業で宿をはじめたい方", "物件選びや許可から開業後の集客まで。任せる範囲を選べます。", "management", ["伴走コース", "運営代行コース", "共同出資コース"]),
]
PLAN_FLOW = [
    ("無料相談・資料請求", "フォームから、物件や状況を気軽にお知らせください。オンラインでもお話しできます。"),
    ("現地調査・収支の試算", "物件と周辺の宿を調べ、売る・貸す・宿にする場合の見込みを無料でお出しします。"),
    ("プランのご提案", "物件とご希望に合わせて、条件を具体的にご提案します。ご提案を見てから、進めるかどうかを決めていただけます。"),
    ("ご契約・開業準備", "改修や許可、写真や予約ページの準備まで、アキヤドが進めます。"),
]
PLAN_FAQ = [
    ("相談だけでも大丈夫ですか？", "はい。売るか活かすか決めていない段階でも、お気軽にご相談ください。ご提案を聞いてから、進めるかどうかを決めていただけます。"),
    ("相談や見積りに費用はかかりますか？", "ご相談、現地調査、収支の試算、プランのご提案までは無料です。"),
    ("遠方の物件でも相談できますか？", "全国の物件のご相談をお受けしています。初回はオンラインでお話しできます。"),
    ("資料には何が書いてありますか？", "各プランの仕組みと条件の考え方、ご相談から開業までの流れ、アキヤドが運営している宿の実績をまとめています。"),
]


def plan_doc_link(category, label="資料をもらう（無料）", cta="media-doc"):
    """サービス資料の請求（お問い合わせフォームで「サービス資料の請求」を選んだ状態にする）"""
    return f'<a href="contact.html?category=document&amp;from=akiyado-{category}" class="mbtn mbtn--sub" data-cta="{cta}">{label} {ARROW}</a>'


def media_plan_card(p, key, money_label="受け取り方"):
    # アキヤドの中では、提供する主語を「アキヤド」に（プランのデータはコーポレートと共通）
    p = {k: (v.replace("RIVIA", "アキヤド") if isinstance(v, str) else v) for k, v in p.items()}
    rec = '<span class="mplan__badge">おすすめ</span>' if p.get("rec") else ""
    init = f'<div><dt>初期費用</dt><dd>{e(p["init"])}</dd></div>' if p.get("init") else ""
    who = "".join(f"<li>{e(w)}</li>" for w in p["who"])
    return f"""            <article class="mplan{" is-rec" if p.get("rec") else ""}">
              {rec}{brand_kicker(p)}<h3 class="mplan__name">{e(p["name"])}</h3>
              <p class="mplan__catch">{e(p["catch"])}</p>
              <dl class="mplan__spec">{init}<div><dt>{e(p.get("money_label", money_label))}</dt><dd>{e(p["monthly"])}<span>{e(p["example"])}</span></dd></div></dl>
              <p class="mplan__who-label">こんな方に</p>
              <ul class="mplan__who">{who}</ul>
            </article>"""


def media_plans_page():
    """アキヤドのプラン一覧。まずカードで端的に紹介し、詳しくは各サービスのページへ"""
    from figures import icon
    groups = []
    for sv in MEDIA_SERVICES:
        c = MEDIA_SERVICE_CARDS[sv["key"]]
        spec = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in c["spec"])
        tags = "".join(f'<li>{e(n)}</li>' for n in c["plans"])
        groups.append(f"""        <article class="msvc reveal" id="{sv["key"]}">
          <div class="msvc__visual">{photo(c["photo"], width=720, height=540, sizes="(max-width: 899px) 100vw, 360px")}<p class="msvc__who">{e(sv["eyebrow"])}</p></div>
          <div class="msvc__body">
            <h2 class="msvc__name">{e(sv["name"])}</h2>
            <p class="msvc__summary">{e(c["summary"])}</p>
            <dl class="msvc__spec">{spec}</dl>
            <p class="msvc__plans-label">選べるプラン</p>
            <ul class="msvc__plans">{tags}</ul>
            <a href="media/{sv["slug"]}.html" class="mbtn mbtn--sub msvc__more" data-cta="media-service-card">サービスの詳細を見る {ARROW}</a>
          </div>
        </article>""")
    voices = ""
    if SHOW_SAMPLE_VOICES:
        vs = "\n".join(f"""          <figure class="mvoice reveal">
            <blockquote class="mvoice__text">{e(t)}</blockquote>
            <figcaption class="mvoice__who"><span class="mvoice__plan">{e(plan)}</span>{e(who)}</figcaption>
          </figure>""" for _, who, plan, t in SAMPLE_VOICES)
        voices = f"""
    <section class="section msec" id="voices">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Voices</p><h2 class="msec__title">ご利用いただいた方の声</h2></div></div>
        <div class="mvoices">
{vs}
        </div>
      </div>
    </section>
"""
    flow = "\n".join(f"""          <li class="mflow__step reveal"><span class="mflow__no">{i:02d}</span><h3 class="mflow__title">{e(t)}</h3><p class="mflow__text">{e(d)}</p></li>"""
                     for i, (t, d) in enumerate(PLAN_FLOW, 1))
    def jump_item(sv):
        worries = "".join(f'<span class="mjump__worry">{e(w)}</span>' for w in sv["worries"][:2])
        return (f'<li><a href="#{sv["key"]}" class="mjump__item"><span class="mjump__who">{e(sv["eyebrow"])}</span>'
                f'{worries}<span class="mjump__name">→ {e(sv["name"])}</span></a></li>')
    jump = "".join(jump_item(sv) for sv in MEDIA_SERVICES)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("アキヤドのプラン", "")])
    body = f"""{media_hero("Services", "アキヤドのプラン", "記事を読んで、具体的に考えたくなったら。空き家の買取・借り上げから、民泊の開業・運営まで。宿を運営するアキヤドにご相談いただけることをまとめました。", crumbs)}

    <section class="section msec msec--first">
      <div class="container">
        {guide_video()}
        <p class="mjump__label reveal">こんなお悩みなら</p>
        <ul class="mjump reveal">{jump}</ul>
        <div class="msvcs">
{chr(10).join(groups)}
        </div>
      </div>
    </section>
{voices}
    <section class="section section--soft msec" id="flow">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Flow</p><h2 class="msec__title">ご相談から開業まで</h2></div></div>
        <ol class="mflow">
{flow}
        </ol>
        <div class="mplans__cta reveal">
          <a href="contact.html?category=operation&amp;from=akiyado-plans" class="mbtn" data-cta="media-plans">無料で相談する {ARROW}</a>
          {plan_doc_link("plans")}
        </div>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">FAQ</p><h2 class="msec__title">よくある質問</h2></div></div>
        <div class="faq reveal">
{faq_html(PLAN_FAQ)}
        </div>
      </div>
    </section>

{media_cta()}"""
    ld = [{"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PLAN_FAQ]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "TOP", "item": f"{SITE}/"},
              {"@type": "ListItem", "position": 2, "name": "アキヤド", "item": f"{SITE}/media.html"},
              {"@type": "ListItem", "position": 3, "name": "アキヤドのプラン"}]},
          guide_video_ld(f"{SITE}/media/plans.html")]
    page("media/plans.html", "アキヤドのプラン｜空き家の買取・借り上げ、民泊の開業・運営支援｜アキヤド",
         "空き家の買取、借り上げ（固定家賃・売上シェア）、民泊の開業・運営代行まで。宿を運営するアキヤドに任せた場合のプランと条件の目安、ご相談から開業までの流れをまとめています。",
         body, current="media", jsonld=ld, mnav="plans")


# ---------------------------------------------------------------- アキヤド：ご相談の解説動画（tools/video/make_explainer.py で作り、videos/ に軽量版を置く）
GUIDE_VIDEO = dict(src="videos/akiyado-guide.mp4", poster="images/video/akiyado-guide-poster.jpg", duration="PT1M34S", upload="2026-10-15T00:00:00+09:00",
                   title="1分半でわかる、アキヤドへのご相談",
                   lead="空き家を放っておくと、何が起きるのか。売る・貸す・宿をはじめる、どの道があるのか。無料相談で分かることまで、アニメで紹介します。")


def guide_video(compact=False):
    """解説動画のブロック。押したときだけ読み込む（preload="none"）。字幕は映像に入っている"""
    v = GUIDE_VIDEO
    head = "" if compact else f"""<div class="mvideo__text"><p class="msec__en">Movie</p><h2 class="msec__title">{e(v["title"])}</h2><p class="mvideo__lead">{e(v["lead"])}</p></div>"""
    return f"""<div class="mvideo{' mvideo--compact' if compact else ''} reveal">{head}<div class="mvideo__frame"><video class="mvideo__player" controls playsinline preload="none" poster="{v["poster"]}" width="1920" height="1080" data-video="akiyado-guide"><source src="{v["src"]}" type="video/mp4"></video></div></div>"""


def guide_video_ld(page_url):
    v = GUIDE_VIDEO
    return {"@context": "https://schema.org", "@type": "VideoObject", "name": v["title"], "description": v["lead"],
            "thumbnailUrl": f"{SITE}/{v['poster']}", "contentUrl": f"{SITE}/{v['src']}", "uploadDate": v["upload"], "duration": v["duration"],
            "inLanguage": "ja", "url": page_url}
