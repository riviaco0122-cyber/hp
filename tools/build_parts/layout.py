# -*- coding: utf-8 -*-
# build.py の一部：ページの外枠（ヘッダー・フッター・パンくず・版番号）と、共通の部品（相談の案内・流れ・お客様の声・実績・よくある質問）。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- layout

import json

SERVICE_NAMES = dict(SERVICES)

# 各サービスの対象者（トップの「お悩みから探す」と共通）
# TOPの事業紹介（英語名・ひとこと説明・アイコン）
SERVICE_INTRO = {
    "operation": ("Revitalization", "地方の空き家を自社で改修し、「暮らすように旅する」宿として運営します。", "house"),
    "management": ("Management", "民泊・小規模宿の開業から日々の運営まで、個人・法人を問わず伴走します。", "key"),
    "marketing": ("Web Marketing", "自社サイト・広告・SNSなどで、問い合わせと売上が伸びる仕組みをつくります。", "target"),
    "partnership": ("Partnership", "保有物件から民泊向きの物件を選び、利回りの算出から購入後の運営まで担います。", "key"),
    "recruit": ("Web Recruiting", "採用計画から定着まで、地方企業の人材確保を支援します。", "users"),
}

PERSONAS = {
    "operation": "実家・空き家の処分や利活用に悩んでいる",
    "marketing": "集客を強化して、売上を伸ばしたい",
    "recruit": "人手が足りず、採用に悩んでいる",
    "management": "民泊・小規模宿を、プロと始めたい",
    "partnership": "保有物件を、民泊用に販売したい",
}

# トップ: ミッション（大きな絵）→ ビジョン（中期的に取り組むこと）→ バリュー（大切にする姿勢）
MISSION = dict(
    copy="地域に眠る価値を、日本の活力に。",
    lead=["空き家や遊休不動産、食や自然、文化や人の営み。地域には、まだ活かされていない価値が数多く眠っています。",
          "私たちはその価値を掘り起こし、「まちづくり」と「観光づくり」を通じて、人が訪れ、働き、暮らし続けられる地域を増やしていきます。",
          "地域が元気になることが、日本が元気になることだと信じて。"],
)
VISION = dict(
    copy="「暮らすように旅する」滞在を、全国のまちへ。",
    lead="ミッションの実現に向けて、私たちが中期的に取り組むこと。",
    steps=[
        ("見つける", "Discover", "空き家や遊休不動産、食・自然・文化・人の営みなど、地域に眠る資源を掘り起こします。"),
        ("磨く", "Refine", "デザインとテクノロジーの力で、「その土地の日常を体験できる宿」や観光コンテンツへと再生・創出します。"),
        ("届ける", "Deliver", "WEBマーケティングの力で、その価値を求める国内外の旅行者に確実に届けます。"),
        ("循環させる", "Circulate", "人の流れと雇用を地域に生み、持続可能な経済循環とまちづくりへとつなげます。"),
    ],
    outcomes=[("旅行者には", "その土地の日常に溶け込む、新しい滞在価値を。"),
              ("地域には", "眠っていた資源が稼ぎ、雇用と交流が生まれる経済循環を。"),
              ("オーナー様には", "負担だった資産や施設が、収益を生む事業に変わる未来を。")],
)
TOP_CONCEPT = dict(
    copy="日本の魅力を、暮らすように味わう。",
    # 「|」の位置でだけ改行する（文節の途中で折り返さない）
    lead=["この家、どうしよう。|そう迷ったまま、|思い出ごと眠っている空き家が、|地方にはたくさんあります。",
          "私たちはその家を|自分たちの手で宿に再生し、|運営しています。",
          "泊まった人がまちで食べ、|買い、また帰ってくる。|一軒の家から、|地域に経済の循環を生み出します。"],
    # スマホは短く（循環の図が続くので、文章は要点だけ）
    lead_sp=["宿をつくることは、|ゴールではなく始まり。",
             "空き家がひらき、|人が訪れ、|まちが潤い、|また次の空き家が目を覚ます。",
             "私たちは、|地域に続いていく|循環をつくります。"],
)
# 宿を起点に、地域へ人とお金がめぐる循環（TOPのコンセプト横の図）
TOP_CYCLE = [
    ("Revive", "空き家を、", "宿に再生"),
    ("Visit", "旅行者が、", "まちを訪れる"),
    ("Spend", "まちで、", "食べて買う"),
    ("Return", "ファンになり、", "また訪れる"),
]
TOP_SCENES = [
    ("scene-stay.jpg", "50% 50%", "Stay", "空き家を、泊まれる宿に", "眠っていた空き家を、RIVIAが宿に再生。その土地の暮らしに溶け込むように泊まれます。"),
    ("scene-walk.jpg", "50% 60%", "Walk", "宿を拠点に、まちへ", "灯りのともる路地を歩き、地元の店で食べ、買う。旅行者の消費が、宿の外のまちへ広がります。"),
    ("oshino-mill.jpg", "50% 60%", "Connect", "土地とつながり、また訪れる", "食や風土、観光コンテンツ、人。土地の魅力とつながり再訪が生まれ、地域の収益と雇用に。"),
]
# 宿を起点に、地域へお金と人が循環する流れ（情景の下に1行で示す）
MISSION_PROSE = [
    ["空き家や遊休不動産、", "食や自然、文化や人の営み。", "地域には、まだ活かされていない", "価値が数多く眠っています。"],
    ["その土地にとって、", "そこに暮らす人々にとって、", "本当に必要なものは何か。", "私たちは自ら現場に立ち、", "地域と徹底的に向き合います。"],
    ["眠っていた価値を掘り起こし、", "まちづくりと観光づくりへ。", "人が訪れ、働き、", "暮らし続けられる地域を、", "ひとつずつ増やしていく。"],
    ["地域が元気になることが、", "日本が元気になること。", "私たちは、そう信じています。"],
]
VALUES = [
    ("圧倒的当事者であれ", "お客様の課題を、第三者としてではなく自分ごととして捉え、主体的に動く。"),
    ("自ら機会をつくれ", "指示を待たず、自ら課題を見つけて動き、次の機会を生み出す。"),
    ("想いを、成果で示す", "想いだけで終わらせず、数字と結果で応える。"),
    ("続く仕組みをつくる", "一過性で終わらせず、地域に残り、循環する形を選ぶ。"),
]


# ご相談の流れ（トップ・お問い合わせで共通）
FLOW = [
    ("お問い合わせ", "フォームから24時間受け付けています。2営業日以内に担当者がご連絡します。"),
    ("無料ヒアリング", "現状と課題、目指す姿をお聞きします。考えがまとまる前でも大丈夫です。"),
    ("ご提案", "課題に合わせた支援の内容と進め方、お見積りをご提示します。"),
    ("ご支援開始", "ご納得いただけた場合のみご契約。現場に入り、成果まで伴走します。"),
]

# RIVIAが選ばれる理由（創業メンバーの経歴にもとづく。経歴は FOUNDERS と一致させる）
REASONS_LEAD = "官・大手・ベンチャーで経験を積んだ2人の創業者が、自ら宿を運営する現場の知見とあわせて支援します。"
REASONS = [
    ("リクルート出身の、事業をつくる力", "代表の2人は、ともにリクルート出身。新規事業開発室でのゼロイチの立ち上げや、ベンチャーでの事業創出・組織拡大の経験を、宿と地域の事業づくりに活かします。",
     "リクルート\u00a0／\u00a0HR\u00a0Tech・|サイバーセキュリティ|ベンチャー"),
    ("県庁出身の、地域と行政を知る視点", "代表の片井は静岡県庁の出身。行政の立場で地域課題に向き合ってきた経験から、自治体や地域の方々との対話を、官民両方の視点で進めます。",
     "静岡県庁 ／ 大手メーカー"),
    ("データにもとづく、根拠のある判断", "位置情報データを扱うベンチャーやテクノロジー企業での経験を活かし、需要や収支を数字で見極めます。感覚に頼らない意思決定を支えます。",
     "位置情報データベンチャー ／ 複数企業の経営"),
]


# ---------------------------------------------------------------- layout
def header(current):
    def cur(key):
        return ' aria-current="page"' if current == key else ""

    names = dict(SERVICES)

    # 「〜したい」の一言で、目的からまっすぐサービスを選べるようにする
    items = "".join(
        f'<li class="subnav__aud">{e(aud)}</li>'
        + "".join(
            f'<li><a href="service-{k}.html"{cur(k)}><span class="subnav__text">'
            f'<span class="subnav__intent">{e(intent)}</span><span class="subnav__name">{e(names[k])}</span>'
            f'</span> {ARROW}</a></li>'
            for k, intent in its)
        for aud, its in NAV_INTENTS)
    sub = (f'              <li class="subnav__intents"><ul>{items}</ul></li>\n'
           f'              <li class="subnav__foot"><a href="services.html">事業内容の一覧を見る {ARROW}</a></li>')
    service_cur = ' aria-current="page"' if current in SERVICE_NAMES or current == "services" else ""
    return f"""  <header class="header">
    <div class="container header__inner">
      <a href="index.html" class="logo" aria-label="RIVIA&amp;CO. トップページ"><img src="images/logo/logo.svg" alt="RIVIA&amp;CO." width="325" height="64"><img class="logo__on-photo" src="images/logo/logo-white.svg" alt="" width="325" height="64" aria-hidden="true"></a>

      <nav class="gnav" id="gnav" aria-label="メインナビゲーション">
        <ul class="gnav__list">
          <li><a href="about.html" class="gnav__link"{cur("about")}>私たちについて</a></li>
          <li class="gnav__item--has-sub">
            <button type="button" class="gnav__link" aria-expanded="false" aria-controls="subnav-service"{service_cur}>事業内容 <span class="gnav__caret" aria-hidden="true"></span></button>
            <ul class="subnav" id="subnav-service">
{sub}
            </ul>
          </li>
          <li><a href="index.html#project" class="gnav__link">実績</a></li>
          <li><a href="media.html" class="gnav__link"{cur("media")}>メディア</a></li>
          <li><a href="careers.html" class="gnav__link"{cur("careers")}>採用情報</a></li>
          <li><a href="contact.html{"?category=" + current if current in SERVICE_NAMES else ""}" class="gnav__link"{cur("contact")}>お問い合わせ</a></li>
        </ul>
      </nav>

      <button type="button" class="menu-btn" aria-controls="gnav" aria-expanded="false" aria-label="メニューを開く"><span></span><span></span><span></span></button>
    </div>
  </header>"""


def footer():
    # 文字を詰め込まず、ロゴ・相談ボタン・主要リンクだけのシンプルな構成にする
    links = [("about.html", "私たちについて"), ("services.html", "事業内容"), ("index.html#project", "実績"),
             ("media.html", "メディア"), ("careers.html", "採用情報"), ("contact.html", "お問い合わせ")]
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
    # 目的・お悩みから探す（Serviceメニューと同じ「〜したい」の一覧）
    # 各サービスの案内（サービス名の下に、ページ内の主な項目へのリンク）
    names = dict(SERVICES)
    subs = [("お悩みと解決策", "{k}-issues"), ("プラン例", "plans"), ("ご支援の流れ", "flow"), ("よくあるご質問", "faq")]
    intents = "".join(
        f'<div class="footer__aud"><p>{e(aud)}</p><ul>'
        + "".join(f'<li><a href="service-{k}.html">{e(t)} {ARROW}</a></li>' for k, t in its)
        + '</ul></div>'
        for aud, its in NAV_INTENTS)
    svcs = "".join(
        f'<div class="footer__svc"><a class="footer__svc-name" href="service-{k}.html">{e(names[k])} {ARROW}</a><ul>'
        + "".join(f'<li><a href="service-{k}.html#{a.format(k=k)}">{e(t)}</a></li>' for t, a in subs)
        + '</ul></div>'
        for k, _ in SERVICES)
    return f"""  <footer class="footer footer--simple">
    <div class="container">
      <div class="footer__top">
        <div class="footer__brand">
          <a href="index.html" class="logo"><img src="images/logo/logo-white.svg" alt="RIVIA&amp;CO." width="325" height="64" loading="lazy"></a>
          <p class="footer__copy">地域に眠る価値を、日本の活力に。</p>
        </div>
        <a href="contact.html" class="footer__cta">無料で相談する {ARROW}</a>
      </div>
      <div class="footer__intents">{intents}</div>
      <nav aria-label="フッターナビゲーション"><ul class="footer__links">{nav}</ul></nav>
      <div class="footer__bottom">
        <address class="footer__address">〒121-0012 東京都足立区青井六丁目8番8号 Grand Maison青井201</address>
        <a href="privacy.html">プライバシーポリシー</a>
        <p>&copy; 2026 合同会社RIVIA&amp;CO.</p>
      </div>
    </div>
    <p class="footer__mark" aria-hidden="true">RIVIA&amp;CO.</p>
  </footer>"""


FAVICON = "data:image/svg+xml," + (
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23111'/%3E"
    "%3Ctext x='32' y='45' text-anchor='middle' font-family='Georgia,serif' font-size='38' fill='%23fff'%3ER%3C/text%3E"
    "%3Ccircle cx='49' cy='44' r='3' fill='%232d6a43'/%3E%3C/svg%3E"
)


FONTS_CSS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Noto+Sans+JP:wght@400;500&family=Noto+Serif+JP:wght@200;300;400&display=swap"


# 英語版は2026年10月に公開をやめた（ブラウザの翻訳で足りるため）。
# もう一度出すときは、BUILD_EN を True にし、vercel.json の /en のリダイレクトを外す（英訳は tools/i18n/ に残してある）
BUILD_EN = False
EN_PAGES = ["index.html", "about.html", "careers.html", "contact.html", "privacy.html", "thanks.html",
            "service-operation.html", "service-management.html", "service-partnership.html",
            "service-marketing.html", "service-recruit.html"] if BUILD_EN else []


def url_for(filename):
    return f"{SITE}/" + ("" if filename == "index.html" else filename)


def asset_version(path):
    """CSS・JSのURLに付ける版番号（中身が変わると番号も変わり、ブラウザの古いキャッシュを使わなくなる）"""
    import hashlib
    with open(os.path.join(OUT, path), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def with_breadcrumbs(filename, title, jsonld, noindex):
    """パンくずの構造化データ（BreadcrumbList）を、全ページ「ホーム（rivia-co.com/）」から始まる同じ形にそろえる。
    ないページ（コーポレートのページ）には「ホーム > ページ名」を足す。Google にサイトの階層を伝え、サイトリンクの選び方を助ける"""
    jsonld = list(jsonld or [])
    found = False
    for j in jsonld:
        if j.get("@type") != "BreadcrumbList":
            continue
        found = True
        items = j["itemListElement"]
        if items and items[0].get("item") == f"{SITE}/":
            items[0]["name"] = "ホーム"
        else:
            items.insert(0, {"@type": "ListItem", "name": "ホーム", "item": f"{SITE}/"})
        for n, it in enumerate(items, 1):
            it["position"] = n
    if not found and not noindex and title and "/" not in filename and filename not in ("index.html", "404.html"):
        jsonld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": title}]})
    return jsonld


def page(filename, title, description, body, current="", jsonld=None, og_type=None, og_image="images/ogp.jpg", noindex=False, mnav="", cv_category="operation"):
    # サービスページは、画面下に常に「無料で相談する」を表示する
    fixed_cta = (f'  <div class="fixed-cta"><a href="contact.html?category={current}" class="btn">無料で相談する {ARROW}</a></div>'
                 if current in SERVICE_NAMES else "")
    is_media = current == "media"
    logo_font = ('\n  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700&text=%E3%82%A2%E3%82%AD%E3%83%A4%E3%83%89&display=swap" media="print" onload="this.media=\'all\'">'
                 if filename == "index.html" else "")
    fonts_css = FONTS_CSS.replace("&display=swap", "&family=Zen+Maru+Gothic:wght@500;700&display=swap") if is_media else FONTS_CSS
    if is_media and filename not in ("media/contact.html", "media/thanks.html"):
        fixed_cta = (f'  <div class="fixed-cta fixed-cta--media"><a href="contact.html?category={cv_category}&amp;from=akiyado" class="btn" data-cta="media-fixed">'
                     f'無料で相談する {ARROW}</a></div>')
    # コーポレートページは英語版（/en/）があるため、言語の対応を検索エンジンに伝え、ヘッダーに切り替えを置く
    has_en = not is_media and filename in EN_PAGES
    en_url = f"{SITE}/en/" + ("" if filename == "index.html" else filename)
    hreflang = (f'\n  <link rel="alternate" hreflang="ja" href="{url_for(filename)}">'
                f'\n  <link rel="alternate" hreflang="en" href="{en_url}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{url_for(filename)}">') if has_en else ""
    lang_switch = (f'<a href="en/{filename}" class="lang-switch" hreflang="en" lang="en" aria-label="English">EN</a>\n      '
                   if has_en else "")
    full_title = f"{title} | 合同会社RIVIA&CO." if title else "合同会社RIVIA&CO. | 地域に眠る価値を、日本の活力に。"
    if is_media:
        # メディアはサイトの一部（rivia-co.com/media/）だが、見え方は独立したメディアにする
        full_title = title if "アキヤド" in title else f"{title} | アキヤド"
        if og_image == "images/ogp.jpg":
            og_image = "images/ogp-media.jpg"
    url = f"{SITE}/" + ("" if filename == "index.html" else filename)
    jsonld = with_breadcrumbs(filename, title, jsonld, noindex)
    ld = ""
    if jsonld:
        ld = "\n".join(
            f'  <script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld
        ) + "\n"
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{GA_ID}');
  </script>
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{CLARITY_ID}");
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{url}">{hreflang}
{'  <meta name="robots" content="noindex">' + chr(10) if noindex else ""}  <link rel="icon" href="images/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="images/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="apple-touch-icon" href="images/apple-touch-icon.png">

  <!-- OGP（SNSやLINEでシェアされたときの表示。画像は横長 1200×630） -->
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="{og_type or ("website" if filename == "index.html" else "article")}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/{og_image}">{"" if og_image not in ("images/ogp.jpg", "images/ogp-media.jpg") and not og_image.startswith("images/eyecatch/") else chr(10) + '  <meta property="og:image:width" content="1200">' + chr(10) + '  <meta property="og:image:height" content="630">'}
  <meta property="og:site_name" content="{"アキヤド" if is_media else "合同会社RIVIA&amp;CO."}">
  <meta property="og:locale" content="ja_JP">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="{fonts_css}" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="{fonts_css}"></noscript>{logo_font}
  <link rel="stylesheet" href="css/style.css?v={asset_version("css/style.css")}">
  <script>
    // JS が有効なときだけアニメーション用の非表示を使う。
    // main.js が読み込めなかった場合は 2 秒後に全コンテンツを表示する（表示抜けの防止）。
    document.documentElement.classList.add('js');
    setTimeout(function () {{ if (!window.RIVIA_READY) document.documentElement.classList.remove('js'); }}, 2000);
  </script>
{ld}</head>
<body class="{"is-media" if is_media else "is-corp"}{" is-top" if filename == "index.html" else ""}">
{"" if is_media else '  <div class="progress" aria-hidden="true"><span></span></div>' + chr(10)}
{media_header(mnav) if is_media else header(current).replace('<button type="button" class="menu-btn"', lang_switch + '<button type="button" class="menu-btn"', 1)}

  <main>
{body}
  </main>

{media_footer() if is_media else footer()}
{fixed_cta}
  <script src="js/main.js?v={asset_version("js/main.js")}"></script>
</body>
</html>
"""
    if is_media:
        # アキヤドの中の相談・資料請求は、アキヤド専用のお問い合わせページへ（運営会社への問い合わせだけはコーポレートへ）
        html = html.replace('href="contact.html', 'href="media/contact.html').replace('href="CORP_CONTACT"', 'href="contact.html?from=akiyado"')
    html = phrase_breaks(highlight(relative_to_root(html, filename)))
    path = os.path.join(OUT, PAGES_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


PAGES_DIR = "pages"  # HTMLはすべて pages/ にまとめる（公開URLは vercel.json の書き換えで今までどおり）
SEO_DIR = "seo"      # robots.txt / sitemap.xml の置き場所（公開URLはサイト直下のまま）


def relative_to_root(html, filename):
    """HTMLは pages/ 以下に置くため、リンクの先を種類ごとに直す。
    - ページ同士のリンク（○○.html）：pages/ の中での相対パス
    - 画像・CSS・JS など：サイト直下（pages/ の1つ上）への相対パス"""
    import re as _re
    depth = filename.count("/")
    page_prefix = "../" * depth
    asset_prefix = "../" * (depth + 1)
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http:", "https:", "#", "data:", "mailto:", "tel:", "/")) or not url:
            return m.group(0)
        is_page = _re.match(r"^(?:\.\./)*[^?#]*\.html(?:[?#].*)?$", url) is not None
        if url.startswith("../"):
            return m.group(0) if is_page else f'{attr}="../{url}"'
        return f'{attr}="{(page_prefix if is_page else asset_prefix)}{url}"'
    html = _re.sub(r'\b(href|src|poster)="([^"]*)"', fix, html)
    # srcset（"画像 幅w, 画像 幅w"）の各画像にも同じ直しをかける
    def fix_srcset(m):
        parts = []
        for item in m.group(1).split(","):
            url, _, w = item.strip().partition(" ")
            parts.append(fix(_re.match(r'(src)="([^"]*)"', f'src="{url}"')).split('"')[1] + (" " + w if w else ""))
        return f'srcset="{", ".join(parts)}"'
    html = _re.sub(r'\bsrcset="([^"]*)"', fix_srcset, html)
    # トップページへのリンクは、正規のURL（/）にそろえる。/index.html へのリンクは
    # 同じ中身の別URLとして検索エンジンに見つかり、インデックス登録の妨げになるため
    return _re.sub(r'\bhref="(?:\.\./)*index\.html(?=[#"])', 'href="/', html)


# 空き家・物件をお持ちの方に向けた、相談のハードルを下げる一言（対応エリアとは別に、相談の呼びかけとして置く）
OPEN_MSG = "観光地でなくても、収益物件になり得ます。お気軽にお問い合わせください。"


def cta(category="", title="まずは、現状をお聞かせください。", text=""):
    q = f"?category={category}" if category else ""
    # 見出しは読点の後で改行（スマホ）。一言は文ごとに改行して、変な位置で折り返さないようにする
    head_, sep_, rest_ = e(title).partition("、")
    title_html = f'{head_}{sep_}<br class="sp-only"><n-b>{rest_}</n-b>' if sep_ else e(title)
    sub = ("\n        " + f'<p class="cta__text">{"<br>".join(e(t) + "。" for t in text.split("。") if t)}</p>') if text else ""
    return f"""    <section class="section cta cta--photo">
      <img class="cta__bg" src="images/photos/garden-boat.jpg" alt="" width="1617" height="1079" loading="lazy" decoding="async">
      <div class="container reveal">
        <h2 class="cta__title">{title_html}</h2>
        <div class="cta__btn"><a href="contact.html{q}" class="btn btn--lg">ご相談はこちらから {ARROW}</a></div>{sub}
      </div>
    </section>"""


def flow_section(soft=False):
    steps = "\n".join(
        f"""          <li class="flow__step reveal" data-delay="{i - 1}">
            <span class="flow__num">{i:02d}</span>
            <h3 class="flow__title">{e(t)}</h3>
            <p class="flow__desc">{e(d)}</p>
          </li>"""
        for i, (t, d) in enumerate(FLOW, 1)
    )
    return f"""    <section class="section{' section--soft' if soft else ''}">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Flow</span>
          <h2 class="section-title">ご相談の流れ</h2>
          <p class="section-lead">ご契約までに費用がかかることはありません。まずはお気軽にお問い合わせください。</p>
        </div>
        <ol class="flow">
{steps}
        </ol>
      </div>
    </section>"""


# NODE Shimoda のゲストレビュー（Airbnb に実際に投稿されたものだけを、原文のまま載せる）
# 例: dict(text="原文のまま", who="ゲスト（東京都）", date="2026年8月"),
NODE_REVIEWS = [
    dict(text="和モダンな室内がとてもオシャレで、快適でした！お部屋の居心地がよく、下田旅行の素敵な思い出になりました。",
         who="Airbnbゲスト・1泊", date="2026年9月"),
    dict(text="駅から近くアクセスが良く利便性が高いと感じました。室内も清潔で過ごしやすかったです。",
         who="Airbnbゲスト・1泊", date="2026年9月"),
    dict(text="海も近く初日の出も見ることができ、スーパーも近かったのでとても便利で快適な時間を過ごすことができました！",
         who="Airbnbゲスト・数泊", date="2026年1月"),
]


def reviews_html():
    if not NODE_REVIEWS:
        return ""
    items = "\n".join(
        f"""            <figure class="review reveal" data-delay="{i % 3}">
              <blockquote class="review__text">「{e(r["text"])}」</blockquote>
              <figcaption class="review__who">{e(r["who"])}{f'<span>{e(r["date"])}</span>' if r.get("date") else ""}</figcaption>
            </figure>"""
        for i, r in enumerate(NODE_REVIEWS))
    return f"""        <div class="reviews">
          <p class="reviews__head">ゲストの声 <span>Airbnb のレビュー（★5）より抜粋</span></p>
          <div class="reviews__list">
{items}
          </div>
        </div>
"""


def project_card(compact=False):
    return f"""        <a href="https://nodeshimoda.com/" class="project{' project--compact' if compact else ''} reveal" target="_blank" rel="noopener">
          <div class="project__img">
            <div class="project__photo" role="img" aria-label="NODE Shimoda のリビング"></div>
          </div>
          <div>
            <span class="project__badge">運営施設の一例</span>
            <h3 class="project__name">NODE Shimoda</h3>
            <p class="project__meta">静岡県下田市 ｜ 一棟貸しバケーションレンタル</p>
            <p class="project__desc">下田市旧町内の空き家を改修した滞在型アパート。RIVIAが運営・集客・DX化を担っています。</p>
            <div class="project__rating"><strong><span class="project__star" aria-hidden="true">★</span><span data-count="4.88">4.88</span></strong><span>Airbnb評価（51件）</span></div>
            <span class="project__link">施設サイトを見る（別タブで開きます） {ARROW}</span>
          </div>
        </a>"""

SERVICE_DATA = {
    "operation": dict(
        message=["空き家を、", "宿に再生する。"],
        description="地方に眠る空き家や遊休不動産を、自社で企画・リノベーションし、宿泊施設として運営する事業です。買取・借り上げから改修、運営までを担います。",
        overview="地方の空き家を自社で改修し、「暮らすように旅する」宿として再生・運営する事業です。",
        issues_lead="空き家は、放置するほど費用と建物の傷みが増えていきます。",
        issues=[
            dict(icon="yen", title="お金と手間だけがかかる実家",
                 voice="相続した実家は空き家のまま。固定資産税と管理の手間だけが重くのしかかる。",
                 solve=["RIVIAが家を借りて宿として運営し、日々の管理も引き受けます。", "出ていくだけだった維持費が、毎月の家賃収入に変わります。"],
                 kpi=["毎年の維持費", "家賃などの収入", "管理の手間"]),
            dict(icon="compass", title="売れない・壊せない、行き場のない家",
                 voice="解体には数百万円、古すぎて売れない。処分も活用もできず途方に暮れている。",
                 solve=["現地・市場調査をもとに、「解体」「売却」「活用」の収支を比較してご提示します。", "改修から運営までRIVIAが担います。手放したい場合は買取も可能です。"],
                 kpi=["解体費用", "家から得られる収入", "家の価値"]),
            dict(icon="heart", title="思い出の家を、地域に残したい",
                 voice="思い出の実家は壊したくない。喜ばれる形で残したいが、やり方がわからない。",
                 solve=["家はお持ちのまま、思い出を活かした「暮らすように旅する」宿に再生します。", "地域の人や旅行者が集まる場所として、家を次の世代へつなぎます。"],
                 kpi=["家の保全", "地域を訪れる人", "地域とのつながり"]),
            dict(icon="chart", title="活用してうまくいくのか分からない",
                 voice="改修費がいくらかかるのか、本当にお客様が来るのかが分からず、一歩を踏み出せない。",
                 solve=["現地と周辺の宿を調べ、改修費と見込める収入を試算してお見せします。", "貸す・売るの両面から、負担がいちばん小さい方法をご提案します。"],
                 kpi=["初期費用", "元が取れるまでの期間", "宿の稼働の見込み"]),
        ],
        steps=[
            ("物件調査・ポテンシャル診断", "1〜2週間", "現地と周辺の宿を調べ、宿にできるかを判断します。"),
            ("事業計画・コンセプト策定", "2〜3週間", "宿のコンセプトと収支の見通しをつくります。"),
            ("空間デザイン・リノベーション", "1〜2ヶ月", "改修・家具の手配から予約の仕組みまで整えます。"),
            ("運営開始・地域連携", "継続", "運営を始め、地域と連携した滞在体験をつくります。"),
        ],
        faq=[
            ("ボロボロで雨漏りしているような空き家でも見てもらえますか？", "はい、構造部分（柱や基礎）が生きていればリノベーション前提で再生可能です。まずは現地確認をさせていただきます。"),
            ("手放したくないのですが、所有権を残したまま借り上げてもらうことは可能ですか？", "可能です。弊社が賃貸借契約を結んで月々の家賃をお支払いするプランと、売却されるプランの双方をご提案できます。"),
            ("解体費用に数百万かかると不動産業者に言われました。", "解体せず宿泊施設として活用すれば、解体コストゼロで逆に収益を生む資産に変えられる可能性が高いです。"),
            ("どのような地域・物件が対象になりますか？", "全国の空き家・遊休不動産が対象です。戸建て・古民家・アパートなど種別も問いません。まずは所在地と物件の状況をお聞かせください。"),
        ],
    ),
    "marketing": dict(
        message=["WEBで、", "集客と売上を伸ばす。"],
        description="業種を問わず、地方の事業者様の集客をWEBマーケティングで支援する事業です。自社サイト、SEO、Googleマップ、WEB広告、SNS、予約・ECサイトなど手段を限定せず、問い合わせと売上が伸びる集客の仕組みをつくります。",
        overview="業種を問わず、自社サイトから広告・SNSまで、問い合わせと売上が伸びる集客を設計します。",
        issues_lead="集客の悩みは手段ではなく、自社で集客をコントロールできていない経営構造の問題です。",
        issues=[
            dict(icon="scale", title="外部サイト頼みで、利益と価格決定権を握られている",
                 voice="集客は予約・ポータルサイト頼みで手数料が重い。値下げ競争で、利益が残らない。",
                 solve=["自社サイトを直接の受け皿に整え、外部サイトは新規客の窓口として使い分けます。", "メールやLINEでお客様とつながり、リピートを自社に集めます。"],
                 kpi=["直接の問い合わせ比率", "販売手数料額", "営業利益率"]),
            dict(icon="compass", title="売上目標と集客施策がつながっていない",
                 voice="HPもSNSも広告も手を付けてはいるが、何に力を入れるべきか分からない。",
                 solve=["売上と流入経路を分析し、目標から逆算して「どこで何件獲るか」を設計します。", "各チャネルの役割と予算配分を決め、優先順位のついた実行計画に落とし込みます。"],
                 kpi=["チャネル別売上", "集客コスト比率", "問い合わせ・予約件数"]),
            dict(icon="target", title="事業の魅力がWEB上で伝わらず、選ばれない",
                 voice="自社サイトが古いまま。検索しても地図でも見つけてもらえず、良さが伝わっていない。",
                 solve=["自社サイトやSEO、Googleマップを整え、「探したときに見つかる」状態をつくります。", "写真・動画・記事・SNSで魅力を一貫して伝え、名前で選ばれる会社・お店にします。"],
                 kpi=["指名検索数", "自然検索からの流入", "サイトの問い合わせ率"]),
            dict(icon="chart", title="集客投資の費用対効果が見えない",
                 voice="広告や制作にお金をかけても、売上につながったか分からず、次の判断ができない。",
                 solve=["施策ごとに「いくら使い、いくら売れたか」を計測し、見える化します。", "検索・SNS広告を運用し、月次レポートで成果の出る施策に予算を寄せます。"],
                 kpi=["CPA（獲得単価）", "ROAS（広告費用対効果）", "チャネル別ROI"]),
        ],
        steps=[
            ("集客診断・戦略設計", "1〜2週間", "売上と流入経路を分析し、集客の戦略を決めます。"),
            ("自社サイト・計測環境の構築", "2週間〜", "自社サイトと問い合わせの流れ、効果の計測を整えます。"),
            ("集客施策の実行", "1ヶ月目〜", "SEO・Googleマップ・SNSなどの施策を実行します。"),
            ("WEB広告運用・分析改善", "継続", "広告を運用し、月次レポートで予算配分を見直します。"),
        ],
        faq=[
            ("宿泊施設以外の業種でも依頼できますか？", "はい。飲食店・小売店・観光事業・地方の中小企業など、業種を問わずご相談いただけます。"),
            ("SNS運用だけの支援ですか？", "いいえ。自社サイトの構築、SEO・オウンドメディア、Googleビジネスプロフィール、WEB広告、SNS、リピーター施策まで、手段を限定せずに事業に合った組み合わせをご提案します。"),
            ("自社サイトが古い、または持っていないのですが大丈夫ですか？", "はい。問い合わせや予約につながる自社サイトの新規制作やリニューアルから対応します。既存のサイトを活かせる場合は、改善提案から始めることも可能です。"),
            ("高品質な写真や動画が手元に一枚もないのですが大丈夫ですか？", "ご安心ください。提携するプロカメラマンが現地へ出張り、自社サイトやWEB広告、SNSで最も目を引くカットを撮影・編集いたします。"),
            ("広告予算は毎月どれくらい必要ですか？", "月数万円程度の少額からスタート可能です。特定の媒体に限定せず、CPA（獲得単価）を見極めながら成果の出る媒体へ徐々に予算を寄せていくことをお勧めしています。"),
        ],
    ),
    "recruit": dict(
        message=["WEBで、", "地方の採用を支える。"],
        description="地方企業の「人材不足」という経営課題を、WEBマーケティングの手法で解決する採用支援事業です。業種を問わず、採用計画から採用ブランディング、母集団形成、定着までを一貫して支援します。",
        overview="業種を問わず、地方企業の人材不足を、採用計画から発信・定着まで一貫して解決します。",
        issues_lead="「応募が来ない」「すぐ辞める」は、事業計画・組織・発信の問題。採用を経営から設計し直します。",
        issues=[
            dict(icon="users", title="人手不足が、売上と事業成長の上限になっている",
                 voice="人が足りず、受けられる仕事や営業時間を絞っている。新しい事業にも踏み出せない。",
                 solve=["事業計画から逆算し、いつまでに・どの職種を・何人採るかの要員計画を設計します。", "採用を「欠員補充」ではなく「成長投資」と捉え、優先度の高い職種から進めます。"],
                 kpi=["人員充足率", "受けられる仕事の量", "人手不足による機会損失"]),
            dict(icon="yen", title="採用費が「掛け捨て」になり、投資として管理できていない",
                 voice="求人サイトに50万円以上払ったのに、応募は1件でドタキャン。毎回何も残らない。",
                 solve=["採用サイトを軸に、求人検索・スカウト・広告・SNSなどを最適に組み合わせます。", "チャネルごとの応募数・採用数・費用を計測し、成果の出る手段に予算を集中させます。"],
                 kpi=["採用単価", "チャネル別の採用数", "媒体費用"]),
            dict(icon="target", title="「選ばれる理由」がなく、条件競争で負けている",
                 voice="「田舎だから」「無名だから」と諦めている。給与や休日では大手に勝てない。",
                 solve=["経営者・現場へのヒアリングから、自社ならではの「働く魅力」を言語化します。", "採用サイトや社員の声で、地方で働くことに価値を感じる人材に魅力を届けます。"],
                 kpi=["応募数", "求める人材の応募比率", "内定承諾率"]),
            dict(icon="door", title="採用しても定着せず、投資が回収できない",
                 voice="採用しても「思っていた仕事と違う」と数ヶ月で辞めてしまい、費用と時間が無駄になる。",
                 solve=["仕事の実像を入社前に伝え、選考基準とカジュアル面談を設計してミスマッチを防ぎます。", "入社後のフォロー体制を整え、定着し活躍できる状態をつくります。"],
                 kpi=["早期離職率", "定着率", "採用・教育コストの回収"]),
        ],
        steps=[
            ("経営課題の整理・採用計画の設計", "1〜2週間", "事業計画から、必要な職種と人数を決めます。"),
            ("採用ブランディング・採用サイト制作", "2〜4週間", "働く魅力を言葉にし、採用サイトで伝えます。"),
            ("母集団形成・チャネル運用", "1ヶ月目〜", "求人検索・スカウト・広告などで応募を集めます。"),
            ("選考・定着プロセスの改善", "継続", "選考と入社後のフォローを整え、定着につなげます。"),
        ],
        faq=[
            ("求人媒体に出すのと何が違うのですか？", "媒体に掲載費を払い続ける採用ではなく、採用サイトやコンテンツを自社の資産として積み上げ、複数のチャネルから直接応募が集まる仕組みをつくります。媒体も、必要に応じて組み合わせの一つとして活用します。"),
            ("SNS運用や面接対策だけをお願いすることはできますか？", "個別の施策からのご相談も可能です。ただし成果を出すには、事業計画や採用ターゲットとのつながりが欠かせないため、まず現状の課題を整理したうえで最適な進め方をご提案します。"),
            ("観光業以外の業種でも依頼できますか？", "はい。製造・建設・介護・小売・観光など、業種を問わず地方企業の採用を支援しています。"),
            ("地方の企業でも、都市部から人が集まりますか？", "はい。Uターン・Iターンや地域貢献、自由な働き方に価値を感じる都市部の人材へ、魅力を的確に届けるアプローチが可能です。"),
            ("採用した後の定着まで支援してもらえますか？", "はい。ミスマッチを防ぐ選考設計から、内定者・新入社員のフォロー体制づくりまで、定着と活躍を見据えて支援します。"),
        ],
    ),
    "management": dict(
        message=["宿の開業から、", "運営までを支える。"],
        description="個人・法人を問わず、宿泊施設の開業から運営代行までを支援する事業です。立地選定・許認可・開業準備から、日々の運営・収益管理まで、必要な範囲でRIVIAが担います。",
        overview="民泊・小規模宿の開業から運営まで、オーナー様と共同で取り組み、事業を一緒に育てます。",
        issues_lead="開業前の不安から、開業後の運営の負担まで。一つの窓口で解決します。",
        issues=[
            dict(icon="doc", title="許可が取れるか分からず不安",
                 voice="民泊を開業したいが、物件探しから保健所の許可まで、何から始めればいいか分からない。",
                 solve=["物件が法令や保健所の要件を満たせるか、契約前に確認します。", "行政へ事前に相談し、「許可が下りずにお金が無駄になる」ことを防ぎます。"],
                 kpi=["開業までの期間", "投資の手戻り", "許可取得の確実性"]),
            dict(icon="yen", title="いくらかかり、いつ回収できるか分からない",
                 voice="必要な資金と、何年で回収できるのかが見えず、投資に踏み切れない。",
                 solve=["買う・借りるそれぞれの必要資金と回収期間を比べ、無理のない計画を立てます。", "自ら運営する小規模宿の実データをもとに、収支を試算します。"],
                 kpi=["必要な資金", "想定利回り", "回収までの期間"]),
            dict(icon="clock", title="開業後の運営まで手が回るか不安",
                 voice="本業があるので、深夜のチェックインや問い合わせ、清掃まで対応できるか不安。",
                 solve=["AIチャットと24時間サポートで、問い合わせ対応を仕組み化します。", "清掃や予約対応までRIVIAが担い、運営の手間から解放します。"],
                 kpi=["対応にかかる時間", "対応品質", "レビュー評価"]),
            dict(icon="chart", title="始めても利益が残るか分からない",
                 voice="予約サイトの手数料や清掃費を引くと、手元にいくら残るのか見当がつかない。",
                 solve=["稼働率・単価・コストを分析し、利益を圧迫している要因を特定します。", "価格の自動調整と直接予約の強化で、手元に残る利益を増やします。"],
                 kpi=["客単価・稼働率", "予約サイトの手数料", "手元に残る利益"]),
        ],
        steps=[
            ("事業構想・物件診断", "2週間", "予算を決め、物件が許可を取れるかを確認します。"),
            ("コンセプト設計・許認可サポート", "1ヶ月", "コンセプトを決め、許可の申請に伴走します。"),
            ("開業準備・運営体制づくり", "1ヶ月", "家具・予約サイト・清掃の段取りまで整えます。"),
            ("運営開始・毎月の振り返り", "継続", "毎月のレポートと振り返りで、収益を伸ばします。"),
        ],
        faq=[
            ("宿泊業の経験が全くなくても開業できますか？", "はい。立地選定や許認可から開業準備まで伴走し、運営の実務もお伝えします。運営をRIVIAにお任せいただくこともできます。"),
            ("すでに営業中の民泊・小規模宿でも依頼できますか？", "このサービスは、これから民泊・小規模宿を始める方向けです。営業中の施設の集客については、「WEB集客支援事業」でご相談いただけます。"),
            ("法人の新規事業として、民泊を始めたい場合も相談できますか？", "はい。工務店や不動産会社など、新規事業として宿泊施設を始めたい法人様からのご相談もお受けしています。事業計画から開業・運営まで支援します。"),
            ("料金の体系はどうなっていますか？", "運営をお任せいただく場合は、任せる業務の範囲に応じて売上の10〜20%を手数料としていただきます（物件の取得や改修などの初期費用はオーナー様のご負担です）。初期費用をアキヤドと共同出資し、出資の割合に応じて利益を分け合うプランもあります。"),
            ("毎月のレポートでは、何が分かりますか？", "稼働率・客単価・売上・レビューなどを毎月まとめてお送りし、オンラインで振り返りの場を設けます。次の月に何をするかまで、一緒に決めます。"),
            ("夜間の緊急対応も任せられますか？", "はい。多言語AIチャットボットと24時間体制のオンラインサポートで、深夜の問い合わせや駆けつけ対応も代行します。"),
        ],
    ),
    "partnership": dict(
        message=["保有物件を、", "民泊用に販売する。"],
        description="不動産会社様との協業事業です。保有物件の中から民泊に適した物件をRIVIAが選定・利回りを算出し、不動産会社様が投資家様へ販売。購入後はRIVIAが開業・運営を担い、家賃や収益を投資家様へお返しします。",
        overview="不動産会社様の保有物件を民泊の投資物件として販売できるよう、選定から購入後の運営まで担います。",
        issues_lead="売れない理由は価格だけではありません。投資商品としての魅力を一緒につくります。",
        issues=[
            dict(icon="house", title="通常の賃貸・売買では、物件の魅力が伝わりにくい",
                 voice="地方や築年数の古い物件は、一般的な賃貸の利回りでは投資家に響かず、販売が長期化してしまう。",
                 solve=["立地や建物の特徴をふまえ、民泊として収益が見込める物件をRIVIAが選定します。", "「宿として運営すれば、この利回り」という新しい切り口で、物件の価値を伝えます。"],
                 kpi=["販売までの期間", "販売価格", "問い合わせ数"]),
            dict(icon="chart", title="想定利回りの根拠を示せない",
                 voice="民泊なら高利回りと言われても裏付けがなく、投資家に自信を持って説明できない。",
                 solve=["市場データと自社の運営実績をもとに、根拠のある利回りを算出します。", "販売資料に使える形でご用意し、ご要望に応じて投資家様向けの説明会にも登壇します。"],
                 kpi=["収支計画の精度", "成約率", "投資家からの信頼"]),
            dict(icon="key", title="購入後の運営を任せられる先がない",
                 voice="投資家から「買った後は誰が運営してくれるのか」と聞かれても、紹介できる運営会社がない。",
                 solve=["購入後は、RIVIAが開業準備から集客・清掃・ゲスト対応まで一括で担います。", "家賃や収益の分配、毎月のレポートまで、手間をかけない形でお返しします。"],
                 kpi=["投資家の運営負担", "購入後の稼働率", "収益の安定性"]),
            dict(icon="doc", title="許認可や改修の要否がわからない",
                 voice="宿泊施設として使えるのか、どこまで改修が必要なのかが分からず、販売前の整備に踏み切れない。",
                 solve=["旅館業法・民泊新法・消防法の要件を確認し、宿にできるかを事前に判定します。", "改修の範囲と概算費用を整理し、販売前か購入後か、実施時期の判断をお手伝いします。"],
                 kpi=["許認可取得の確実性", "改修費用", "開業までの期間"]),
        ],
        steps=[
            ("物件の選定・利回りの算出", "2〜3週間", "保有物件から民泊向きの物件を選び、根拠のある利回りを出します。", "不動産会社様へのご支援"),
            ("販売資料・説明会のサポート", "販売期間中", "販売資料をご用意し、ご要望に応じて投資家様向けの説明会にも登壇します。", "不動産会社様へのご支援"),
            ("購入後の開業準備", "1〜3ヶ月", "物件を購入された投資家様に代わり、許可申請・改修・予約サイト掲載まで進めます。", "投資家様へのご支援"),
            ("運営・収益のお返し", "開業後〜", "運営はRIVIAが担い、投資家様へ収益と月次レポートをお届けします。", "投資家様へのご支援"),
        ],
        faq=[
            ("どのような物件が対象になりますか？", "戸建て・古民家・小規模な一棟アパートなど、宿泊施設として運営できる可能性のある物件が対象です。地方や築年数の古い物件でも、まずは一度ご相談ください。"),
            ("投資家様への販売は、どなたが行いますか？", "投資家様へのご案内と販売は、不動産会社様に説明会やメールマガジンなどで行っていただきます。RIVIAは物件の選定と利回りの算出、販売資料のご用意を担い、ご要望に応じて説明会にも登壇します。"),
            ("投資家様への利回りは保証されますか？", "契約の形によって異なります。家賃を固定でお支払いする形のほか、売上に連動して収益をお返しする形もあります。物件と投資家様のご意向に合わせてご提案します。"),
            ("RIVIAはどのように収益を得るのですか？", "物件の購入後、RIVIAが開業・運営を担い、宿泊の売上の一部を運営の対価としていただきます。投資家様には、家賃や収益の分配という形でお返しします。"),
        ],
    ),
}



def faq_html(items):
    return "\n".join(
        f"""          <details class="faq__item">
            <summary class="faq__q"><span class="faq__mark">Q</span><span class="faq__qt">{e(q)}</span><span class="faq__toggle" aria-hidden="true"></span></summary>
            <div class="faq__a"><span class="faq__mark">A</span><p>{e(a)}</p><span></span></div>
          </details>"""
        for q, a in items
    )
