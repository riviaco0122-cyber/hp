# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：民泊できる？1分診断（media/minpaku-check.html）。
# 仕様は docs/tools/minpaku-check.md だけを正とする（質問・判定・点数・数字と出典・案内するプラン・GA4 イベント）。
# 文言と数字はここ（Python）に置き、判定の計算は js/check.js が行う。見た目は css/check.css（このページだけで読む）。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する。

CHECK_SLUG = "minpaku-check"

# 質問（仕様 2章）。(名前, 質問, 補足, [(値, 選択肢)])。5問目は面積と状態の2つを1画面で聞く
CHECK_QUESTIONS = [
    [("place", "物件は、どこにありますか？", "",
      [("izu", "伊豆半島"), ("shizuoka", "静岡県のそのほか"), ("other", "静岡県の外")])],
    [("type", "建物の種類を選んでください", "",
      [("house", "一戸建て"), ("condo", "マンション・アパートの1室")])],
    [("zone", "用途地域は、どれですか？", 'zone',
      [("excl", "低層・中高層の住居専用地域（田園住居を含む）"), ("res", "第一種住居・第二種住居・準住居地域"),
       ("com", "近隣商業・商業・準工業地域"), ("ind", "工業・工業専用地域"), ("chosei", "市街化調整区域"), ("unknown", "わからない")])],
    [("hazard", "ハザードマップで、色が付いていますか？", 'hazard',
      [("none", "色が付いていない"), ("colored", "浸水・土砂災害などの色が付いている"), ("unknown", "わからない")])],
    [("area", "延床面積は、どれくらいですか？", "",
      [("lt60", "60㎡未満"), ("m60", "60〜150㎡"), ("m150", "150〜200㎡"), ("gt200", "200㎡超")]),
     ("state", "建物の状態は？", "",
      [("ready", "すぐ住める"), ("care", "手入れが必要"), ("major", "大きな修繕が必要")])],
    [("goal", "この家を、どうしたいですか？", "",
      [("sell", "売りたい・手放したい"), ("lend", "貸したい・任せたい"), ("start", "自分で宿をはじめたい"), ("undecided", "まだ決めていない")])],
]
CHECK_HELP = {
    "zone": "市町村のホームページにある「都市計画図」で調べられます。わからなければ「わからない」を選んでください。",
    "hazard": '<a href="https://disaportal.gsi.go.jp/" target="_blank" rel="noopener">国土交通省 ハザードマップポータルサイト</a>で、住所を入れて確かめられます。',
}

# 下田の宿の1年目の月別稼働率（仕様 3-3。docs/brand/experience.md 確認済み。開業月の7月を除く）
CHECK_OCC = [("8月", 58), ("9月", 60), ("10月", 52), ("11月", 33), ("12月", 71), ("1月", 39), ("2月", 57), ("3月", 61)]
CHECK_OCC_AVG = 53
CHECK_CASE_SRCS = ["case-rental-house-inn-first-year", "case-owner-setouchi-cycling", "case-owner-castle-town-nagaya", "case-owner-satoyama-airdna"]

CHECK_FAQ = [
    ("用途地域がわからなくても、診断できますか？",
     "できます。「わからない」を選ぶと、制度の判定を保留にして、点数は中間にします。用途地域は、市町村の都市計画図で調べられます。"),
    ("民泊新法と旅館業は、何が違いますか？",
     "民泊新法（住宅宿泊事業）は、住居専用地域でも届出ができますが、営業は年180日までです。旅館業（簡易宿所）は通年で営業できますが、営業できる用途地域が決まっています。"),
    ("診断で出る売上は、私の家でも見込めますか？",
     "お約束するものではありません。表示する数字は、オーナーの事例と、私たちが下田で運営する宿の1年目の実績です。その場所の料金の相場や建物の状態は、現地を見て無料で確かめます。"),
]


def _check_step(i, groups):
    n = len(CHECK_QUESTIONS)
    multi = len(groups) > 1
    inner = []
    for gi, (name, q, help_key, opts) in enumerate(groups):
        qid = f"mchk-q-{name}"
        items = "".join(f'<label class="mchk__opt"><input type="radio" name="{name}" value="{v}"><span>{e(t)}</span></label>' for v, t in opts)
        help_html = f'<p class="mchk__help">{CHECK_HELP[help_key]}</p>' if help_key else ""
        head = (f'<h2 class="mchk__q" id="{qid}" tabindex="-1">{e(q)}</h2>' if gi == 0 and not multi else
                f'<p class="mchk__subq" id="{qid}">{e(q)}</p>')
        inner.append(f"""<div class="mchk__group" role="radiogroup" aria-labelledby="{qid}">{head}{help_html}
            <div class="mchk__opts mchk__opts--{len(opts)}">{items}</div></div>""")
    title = (f'<h2 class="mchk__q" tabindex="-1">広さと状態は？</h2>' if multi else "")
    return f"""          <section class="mchk__step" data-step="{i}" data-multi="{1 if multi else 0}"{"" if i == 1 else " hidden"} aria-label="質問 {i} / {n}">
            {title}{"".join(inner)}
          </section>"""


def _check_chart():
    bars = "".join(f'<li class="mchk-bars__item" style="--v:{v}"><span class="mchk-bars__v">{v}<small>%</small></span>'
                   f'<span class="mchk-bars__bar" aria-hidden="true"></span><span class="mchk-bars__m">{m}</span></li>' for m, v in CHECK_OCC)
    alt = "下田の宿の1年目の月別稼働率。" + "、".join(f"{m} {v}%" for m, v in CHECK_OCC) + f"。平均は約{CHECK_OCC_AVG}%。"
    return f"""<figure class="mchk-chart" role="img" aria-label="{e(alt)}">
              <figcaption class="mchk-chart__cap"><b>下田の宿の1年目の稼働率</b><span>月別・開業月を除く</span><span class="mchk-chart__avg" aria-hidden="true">平均 約{CHECK_OCC_AVG}%</span></figcaption>
              <div class="mchk-bars" style="--avg:{CHECK_OCC_AVG}" aria-hidden="true">
                <span class="mchk-bars__avg"></span>
                <ol>{bars}</ol>
              </div>
            </figure>"""


def media_check_page():
    n = len(CHECK_QUESTIONS)
    steps = "\n".join(_check_step(i, g) for i, g in enumerate(CHECK_QUESTIONS, 1))
    labels = {name: dict(opts) for groups in CHECK_QUESTIONS for name, _, _, opts in groups}
    order = [name for groups in CHECK_QUESTIONS for name, _, _, _ in groups]
    short = dict(place="場所", type="建物", zone="用途地域", hazard="ハザードマップ", area="延床面積", state="建物の状態", goal="ご希望")  # 相談のメッセージ欄に入れる見出し
    plans = {sv["key"]: dict(name=sv["name"], who=sv["eyebrow"], title=sv["title"].replace("\n", ""), href=f"{sv['slug']}.html")
             for sv in MEDIA_SERVICES}
    data = dict(n=n, labels=labels, order=order, short=short, plans=plans, occAvg=CHECK_OCC_AVG)
    srcs = "".join(f'<li><a href="media/{sl}.html">{e(ARTICLE_BY_SLUG[sl]["title"])}</a></li>' for sl in CHECK_CASE_SRCS if sl in ARTICLE_BY_SLUG)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("民泊できる？1分診断", "")])
    score_rows = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{p}点</td><td>{e(d)}</td></tr>" for k, p, d in [
        ("制度", 40, "旅館業できそう 40／民泊新法のみ 25／わからない・要相談 20／難しい 0"),
        ("災害", 20, "色なし 20／わからない 10／色あり 5"),
        ("建物の状態", 25, "すぐ住める 25／手入れが必要 15／大きな修繕が必要 5"),
        ("広さ", 15, "60〜150㎡ 15／150〜200㎡ 12／60㎡未満 8／200㎡超 8")])
    body = f"""    <section class="mhero mchk-hero">
      <div class="container">{crumbs}
        <p class="mhero__en">Check</p>
        <h1 class="mhero__title mchk-hero__title">空き家で民泊できる？<br>1分診断</h1>
        <p class="mchk-hero__lead">6つの質問に答えると、営業できそうな制度と、宿としての目安の点数、事例の数字がわかります。</p>
        <ul class="mchk-hero__chips"><li>全{n}問</li><li>約1分</li><li>名前・連絡先の入力なし</li></ul>
      </div>
    </section>

    <section class="mchk-sec">
      <div class="container">
        <div class="mchk" id="mchk">
          <noscript><p class="mchk__noscript">この診断は JavaScript を使います。ブラウザの設定で有効にしてください。</p></noscript>
          <div class="mchk__panel" id="mchk-panel">
            <div class="mchk__top">
              <button type="button" class="mchk__back" hidden><span aria-hidden="true">←</span> 戻る</button>
              <p class="mchk__count" aria-live="polite">質問 <b>1</b> / {n}</p>
            </div>
            <div class="mchk__progress" role="progressbar" aria-label="進み具合" aria-valuemin="0" aria-valuemax="{n}" aria-valuenow="1"><i style="width:{100 / n:.2f}%"></i></div>
            <form class="mchk__form" onsubmit="return false">
{steps}
              <div class="mchk__nav"><button type="button" class="mbtn mchk__next" disabled>次へ</button></div>
            </form>
          </div>

          <div class="mchk__result" id="mchk-result" hidden>
            <div class="mchk-res__head">
              <h2 class="mchk-res__title" tabindex="-1">診断の結果</h2>
              <button type="button" class="mchk__retry">はじめからやり直す</button>
            </div>
            <div class="mchk-res__grid">
              <div class="mchk-card mchk-score">
                <p class="mchk-card__label">宿としての目安</p>
                <p class="mchk-score__num"><b data-out="score">0</b><small>/ 100点</small></p>
                <p class="mchk-score__band" data-out="band"></p>
                <div class="mchk-meter" aria-hidden="true"><i data-out="meter"></i><span style="left:45%"></span><span style="left:70%"></span></div>
                <p class="mchk-meter__legend" aria-hidden="true"><span>宿以外の道も</span><span>条件しだい</span><span>有望</span></p>
                <ul class="mchk-break" data-out="break"></ul>
              </div>
              <div class="mchk-card mchk-law">
                <p class="mchk-card__label">営業できそうな制度</p>
                <ul class="mchk-law__list" data-out="law"></ul>
              </div>
            </div>

            <div class="mchk-card mchk-nums">
              <p class="mchk-card__label">事例の数字</p>
              <div class="mchk-nums__grid">
                <dl class="mchk-stats">
                  <div class="mchk-stat"><dt>一棟貸しの宿の売上</dt><dd><small>月 約</small>40万〜55万<small>円</small></dd><p>オーナーの事例</p></div>
                  <div class="mchk-stat" data-out="cost"></div>
                </dl>
                {_check_chart()}
              </div>
              <p class="mchk-nums__note" data-out="note180" hidden></p>
              <p class="mchk-nums__note" data-out="place"></p>
            </div>

            <div class="mchk-res__grid mchk-know">
              <div class="mchk-card"><p class="mchk-card__label mchk-know__h">わかったこと</p><ul class="mchk-know__list mchk-know__list--ok" data-out="found"></ul></div>
              <div class="mchk-card"><p class="mchk-card__label mchk-know__h">まだわからないこと</p><ul class="mchk-know__list" data-out="unknown"></ul>
                <p class="mchk-know__close">この先は、現地を見て私たちが無料で確かめます。</p></div>
            </div>

            <div class="mchk-plans">
              <h2 class="mchk-plans__title">この結果に合うご相談</h2>
              <p class="mchk-plans__lead" data-out="plead"></p>
              <div class="mchk-plans__list" data-out="plans"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="mchk-doc">
      <div class="container mchk-doc__wrap">
        <h2 class="mchk-doc__title">判定のしくみ</h2>
        <p>制度は、用途地域と建物の種類・広さで判定します。旅館業（簡易宿所）は、建築基準法の別表第二で、第一種住居・第二種住居・準住居地域と、近隣商業・商業・準工業地域で営業できそうと判定します（第一種住居地域は3,000㎡以下）。民泊新法（住宅宿泊事業）は住居専用地域でも届出ができますが、年180日までで、条例で日数・区域が制限されることがあります（住宅宿泊事業法 第18条）。工業専用地域は住宅が建てられないため対象外です。</p>
        <p>市街化調整区域は、旅館業では用途の変更に許可が要り、難しいことが多く、民泊新法は自治体の判断によるため、保健所・市町村への事前の相談が必要と出します。マンション・アパートの1室は、管理規約で民泊が禁止されていないことが必要で、旅館業は現実的に難しい扱いにしています。200㎡を超える建物を旅館業にするには、用途変更の確認申請が要ります（2019年の建築基準法の改正で、200㎡以下は不要になりました）。</p>
        <div class="mchk-doc__table"><table>
          <caption>点数の決め方（100点満点・目安）</caption>
          <thead><tr><th scope="col">項目</th><th scope="col">配点</th><th scope="col">決め方</th></tr></thead>
          <tbody>{score_rows}</tbody>
        </table></div>
        <p class="mchk-doc__note">※ 70点以上は「宿として有望」、45〜69点は「条件しだいで有望」、44点以下は「宿以外の道も比べたい」と表示します。</p>

        <h2 class="mchk-doc__title">前提と出典</h2>
        <ul class="mchk-doc__list">
          <li>一棟貸しの宿の売上（月 約40万〜55万円）と初期費用（総予算 約350万〜450万円）は、オーナーの事例です。</li>
          <li>稼働率と初期費用（改修 約410万円＋家具・家電・備品 約240万円）は、創業メンバーが静岡県下田市で開業した宿（賃貸・家具家電込み）の1年目の実績です。</li>
          <li>民泊新法の年180日の上限と比べる泊数は、下田の宿の1年目の稼働率 約53%から計算しています。</li>
        </ul>
        <ul class="mchk-doc__srcs">
          <li><a href="https://laws.e-gov.go.jp/law/325AC0000000201" target="_blank" rel="noopener">建築基準法（別表第二）｜e-Gov 法令検索</a></li>
          <li><a href="https://laws.e-gov.go.jp/law/429AC0000000065" target="_blank" rel="noopener">住宅宿泊事業法（第18条）｜e-Gov 法令検索</a></li>
          <li><a href="https://disaportal.gsi.go.jp/" target="_blank" rel="noopener">ハザードマップポータルサイト｜国土交通省</a></li>
          {srcs}
        </ul>

        <h2 class="mchk-doc__title">よくある質問</h2>
        <div class="faq">
{faq_html(CHECK_FAQ)}
        </div>
        <p class="mchk-doc__disclaim">この診断は、答えをもとにした目安です。<strong>将来の収益や金額を保証・約束するものではありません。</strong>表示する数字は事例で、実際の収支は、物件・立地・季節・運営によって大きく変わります。営業できるかどうかは、保健所・市町村・消防への相談で決まります。</p>
      </div>
    </section>
    <script type="application/json" id="mchk-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>
    <script src="js/check.js?v={asset_version("js/check.js")}" defer></script>"""
    # このページだけの見た目（css/check.css）。本文の先頭で読み込む（共通の <head> は layout.py が作るため）
    body = f'    <link rel="stylesheet" href="css/check.css?v={asset_version("css/check.css")}">\n' + body
    ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": "空き家で民泊できる？1分診断", "applicationCategory": "UtilitiesApplication",
           "operatingSystem": "Web", "url": f"{SITE}/media/{CHECK_SLUG}.html", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"}},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in CHECK_FAQ]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"},
              {"@type": "ListItem", "position": 2, "name": "民泊できる？1分診断"}]}]
    page(f"media/{CHECK_SLUG}.html", "空き家で民泊できる？1分診断｜用途地域・災害・売上の目安｜アキヤド",
         "6つの質問で、空き家が旅館業・民泊新法で営業できそうか、宿としての目安の点数、事例の売上・稼働率がわかります。名前・連絡先の入力はいりません。",
         body, current="media", jsonld=ld)
