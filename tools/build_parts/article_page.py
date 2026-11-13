# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：記事ページの組み立て（出典の欄を含む）。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

def source_li(s):
    """参考資料の1行。末尾に URL があれば、その資料名をリンクにする（URL は画面に出さない）。"""
    m = re.match(r"^(.*?)\s*(https?://\S+)$", s)
    if not m:
        return f"<li>{e(s)}</li>"
    return f'<li><a href="{e(m.group(2))}" target="_blank" rel="noopener noreferrer">{e(m.group(1))}</a></li>'


def first_sentence_end(text):
    """一文目の終わり（「。」の直後の位置）。かっこ（）「」の中の「。」では切らない。見つからなければ 0"""
    depth = 0
    for i, ch in enumerate(text):
        if ch in "（「『(":
            depth += 1
        elif ch in "）」』)":
            depth = max(depth - 1, 0)
        elif ch == "。" and depth == 0:
            return i + 1
    return 0


def _kp_grams(s):
    s = re.sub(r"[、。「」『』（）()・：:？！?!\s,.%％0-9０-９]", "", s)
    return collections.Counter(s[i:i + 2] for i in range(len(s) - 1))


def keypoint_sections(a, min_ratio=1.4):
    """「この記事のポイント」の各項目が、どの節の答えかを推定する（なければ None）。
    要点と節（見出し＋本文）の2文字の重なりを、ほかの節にもある言葉ほど軽く、見出しにある言葉ほど重く数え、
    1位が2位の min_ratio 倍以上のときだけ対応づける（迷うときはリンクを付けない。誤ったリンクは、ないより悪い）。
    「まとめ」の節とよくある質問は対象外。記事データに kp_sections=[節のid か None, …] があれば、それを使う"""
    if a.get("kp_sections"):
        return list(a["kp_sections"]) + [None] * (len(a["keypoints"]) - len(a["kp_sections"]))
    secs = [(sid, h, re.sub(r"<[^>]+>|\s", "", b)) for sid, h, b in a["sections"] if not h.startswith("まとめ") and sid != "faq"]
    sg = [_kp_grams(h + b) for _sid, h, b in secs]
    df = collections.Counter(g for c in sg for g in set(c))
    out = []
    for k in a["keypoints"]:
        kg = _kp_grams(k)
        sc = sorted(((sum((1 + 2 * (g in _kp_grams(h))) / df[g] for g in kg if g in c), sid)
                     for (sid, h, _b), c in zip(secs, sg)), reverse=True)
        ok = sc and sc[0][0] > 0 and (len(sc) == 1 or sc[0][0] >= min_ratio * sc[1][0])
        out.append(sc[0][1] if ok else None)
    return out


def article_page(a):
    names = dict(SERVICES)
    toc = "".join(f'<li><a href="#{sid}">{e(h)}</a></li>' for sid, h, _ in a["sections"])
    kp_to = keypoint_sections(a)
    def kp_item(i, k):
        # 最初の一文を太字の要点、残りを補足（小さく・淡く）にして、短く見せる。
        # 答えが載っている節があれば、要点の文そのものをその節へのリンクにする（「○章で詳しく」の行を足さず、縦に長くしない。人の方針 2026-11-13）
        n = first_sentence_end(k)
        main_text, sub = (k[:n], k[n:].strip()) if n and k[n:].strip() else (k, "")
        main = f'<span class="kp__main">{e(main_text)}</span>'
        if kp_to[i]:
            main = f'<a class="kp__link" href="#{kp_to[i]}">{main}</a>'
        return f'<li>{main}' + (f'<span class="kp__sub">{e(sub)}</span>' if sub else "") + '</li>'
    keypoints = "".join(kp_item(i, k) for i, k in enumerate(a["keypoints"]))
    def lead_sentence(html):
        """節の最初の段落（<p>）の一文目を強調する。2文以上あり、一文目にタグを含まない段落だけ。"""
        m = re.match(r"(\s*<p>)([^<]+)", html)
        n = first_sentence_end(m.group(2)) if m else 0
        if not n or not html[m.start(2) + n:].lstrip()[:1] or html[m.start(2) + n:][:1] in ("<", " ", "\n"):
            return html
        return html[:m.end(1)] + f'<span class="lead-s">{m.group(2)[:n]}</span>' + html[m.start(2) + n:]
    def calc_lists(html):
        """式が並ぶ箇条書き（÷・×・= を含む項目だけの <ul>）に calc クラスを付けて、式として見せる"""
        def sub(m):
            items = re.findall(r"<li>(.*?)</li>", m.group(2), re.S)
            if items and all(re.search(r"[÷×=＝]", x) for x in items):
                return f'<ul class="calc"{m.group(1)}>{m.group(2)}</ul>'
            return m.group(0)
        return re.sub(r"<ul([^>]*)>(.*?)</ul>", lambda m: sub(m) if 'class=' not in m.group(1) else m.group(0), html, flags=re.S)
    def auto_stack_tables(html):
        """スマホで1列目が細く縦に伸びる表を、見やすい形に変える（人の方針 2026-10-12。比べる表は design-guide 6章）。
        見出し行があり、1列目の文字が長い（12字超）か、ほかのマスが長い（24字超）表が対象。
        - 2列の表（項目と内容）：文字が長いときだけ、1行ずつのカード（table--stack）に積み替える。項目名がカードの見出しになるので、ラベルは付けない
        - 3列以上の表：比べるための表なので、文字の長さによらずカードにせず、1列目を止めて左右にスライドする表（table--wide）にする
          （短い表もスマホで潰れないように。表が画面に収まるときは、js/main.js がスライドの案内を隠す）"""
        def conv(m):
            t = m.group(0)
            heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
            rows = re.findall(r"<tr>(.*?)</tr>", t.split("</thead>")[-1], re.S) if "</thead>" in t else []
            if len(heads) < 2 or not rows:
                return t
            parsed = [re.findall(r"<td([^>]*)>(.*?)</td>", r, re.S) for r in rows]
            if any(len(c) != len(heads) for c in parsed):
                return t
            first = max(len(re.sub(r"<[^>]+>", "", c[0][1]).strip()) for c in parsed)
            other = max(len(re.sub(r"<[^>]+>", "", x[1]).strip()) for c in parsed for x in c[1:])
            if len(heads) >= 3:
                return ('<p class="table-hint" aria-hidden="true">表は左右にスライドできます →</p>'
                        '<div class="table-scroll table-scroll--wide"><table class="table table--wide">' + t[len('<table class="table">'):])
            if first <= 12 and other <= 24:
                return t
            return '<div class="table-scroll table-scroll--stack"><table class="table table--stack">' + t[len('<table class="table">'):]
        return re.sub(r'<table class="table">.*?</table>', conv, html, flags=re.S)
    def thin_strong(html):
        """強調（太字）を絞る（playbook 13-4。人の方針 2026-10-12）。段落（<p>）の中の太字は、節の最初の太字（結論の1文）だけ残し、
        あとは太字を外す。箇条書きの項目名・表・注意枠の見出しの太字は、構造なので残す。"""
        first = [True]
        def p_fix(m):
            inner = m.group(2)
            if "<strong>" not in inner:
                return m.group(0)
            if first[0]:
                first[0] = False
                n = inner.count("<strong>")
                if n <= 1:
                    return m.group(0)
                head, _, rest = inner.partition("</strong>")
                rest = rest.replace("<strong>", "").replace("</strong>", "")
                return m.group(1) + head + "</strong>" + rest + "</p>"
            inner = inner.replace("<strong>", "").replace("</strong>", "")
            return m.group(1) + inner + "</p>"
        return re.sub(r"(<p(?: [^>]*)?>)(.*?)</p>", p_fix, html, flags=re.S)
    def talk_lists(html):
        """会話の吹き出しの直後の箇条書きは、話している人の言葉の続きとして吹き出しの中に入れる"""
        return re.sub(r'(<div class="talk__body">(?:(?!</div>).)*?)</div></div>\s*(<(ul|ol)>.*?</\3>)',
                      lambda m: m.group(1) + m.group(2).replace(f"<{m.group(3)}>", f'<{m.group(3)} class="talk__list">', 1) + "</div></div>", html, flags=re.S)
    def talk_questions(html):
        """聞き手の質問（<p class="talk__q">）を、アキヤドのマークを顔にした「編集部」の吹き出しにして、対話の形で見せる"""
        return re.sub(r'<p class="talk__q">(.*?)</p>',
                      lambda m: f'<div class="talk talk--q"><span class="talk__img talk__img--logo">{AKIYADO_MARK}</span><div class="talk__body"><p class="talk__name">編集部</p><p>{m.group(1)}</p></div></div>',
                      html, flags=re.S)
    def label_lists(html):
        """表の1列目の項目名が、3つ以上を「・」でつないだ長いもの（9文字以上）なら、1つずつ改行した箇条書きにする
        （「鍵・／チェックイン／・防犯」のように「・」が行頭・行末に残って見えるため。人の指摘 2026-11-06）"""
        def sub(m):
            items = m.group(2).split("・")
            if len(items) < 3 or len(m.group(2)) < 9 or "（" in m.group(2) or not all(items):
                return m.group(0)
            return m.group(1) + "<br>".join("・" + x for x in items) + m.group(3)
        return re.sub(r"(<tr>\s*<td(?:\s[^>]*)?>)([^<]+)(</td>)", sub, html)
    def tables(html):
        html = talk_questions(talk_lists(html))
        html = calc_lists(label_lists(html))
        html = auto_stack_tables(html)
        html = html.replace('<table class="table">', '<div class="table-scroll"><table class="table">').replace("</table>", "</table></div>")
        return re.sub(r"<td>((?:約|―|—)?[0-9０-９.,]+(?:%|倍|か月)?(?:（[^<]{0,12}）)?)</td>", r'<td class="num">\1</td>', html)
    def card_headings(html):
        """カルーセル／比較カードの見出し（<p class="carousel__title"|"compare__head">）を本物の見出しにする。
        節内の先行する h3 の下なら h4、そうでなければ h3（見た目は CSS で <p> 時代と同じに固定）。"""
        out, pos, level = [], 0, 3
        for m in re.finditer(r'<h3[ >]|<p class="(?:carousel__title|compare__head)">(.*?)</p>', html, re.S):
            out.append(html[pos:m.start()])
            if m.group(0).startswith("<h3"):
                level = 4
                out.append(m.group(0))
            else:
                cls = re.match(r'<p class="([^"]+)"', m.group(0)).group(1)
                out.append(f'<h{level} class="{cls}">{m.group(1)}</h{level}>')
            pos = m.end()
        out.append(html[pos:])
        return "".join(out)
    sections = "\n".join(
        f"""        <section class="article__section" id="{sid}">
          <h2>{e(h)}</h2>
{lead_sentence(html.strip())}
        </section>"""
        for sid, h, html in [(x, y, insert_figure(a["slug"], x, card_headings(tables(thin_strong(z))), a.get("figure"))) for x, y, z in a["sections"]]
    )
    sources = "".join(source_li(s) for s in a["sources"])
    svc = a["services"][0]
    svc_links = "".join(
        f'<li><a href="service-{k}.html">{e(names[k])} {ARROW}</a></li>' for k in a["services"]
    )
    # 同じカテゴリ・同じ関連サービスの記事を優先
    related = sorted(
        (x for x in ARTICLES if x["slug"] != a["slug"]),
        key=lambda x: (x["category"] != a["category"], not set(x["services"]) & set(a["services"])),
    )
    # 事例（オーナー取材）を、近いテーマのものから1本、先頭に出す
    if not a["slug"].startswith("case-owner-"):
        _ct = {"money": "case-owner-subsidy-akiya", "operate": "case-owner-pricing-mistake", "start": "case-owner-licensed-akiya",
               "house": "case-owner-diy-cottage", "sell": "case-owner-diy-cottage", "lend": "case-owner-fishing-port", "trend": "case-owner-fishing-port"}
        _c = ARTICLE_BY_SLUG.get(_ct.get((a.get("topics") or ["start"])[0], "case-owner-licensed-akiya"))
        if _c:
            related = [_c] + [x for x in related if x["slug"] != _c["slug"]]
    from urllib.parse import quote
    share_url = quote(f"{SITE}/media/{a['slug']}.html", safe="")
    share_text = quote(f"{a['title']}｜アキヤド", safe="")
    for_links = "".join(f'<li><a href="media/guide-{x["key"]}.html">{e(x["title"])}</a></li>' for x in guides_of(a["slug"]))
    for_html = f'<div class="article__for"><span>こんな方に</span><ul>{for_links}</ul></div>' if for_links else ""
    g = guide_of(a["slug"])
    cv_text, cv_href = inline_cta_parts(a, g)
    guide_box = ""
    if g:
        idx = g["slugs"].index(a["slug"])
        def _gb_item(n_, s_):
            x = ARTICLE_BY_SLUG[s_]
            inner = (f'<span class="guide-box__no">{n_:02d}</span>'
                     f'<span class="guide-box__text"><span class="guide-box__name">{e(list_name(x))}</span>'
                     f'<span class="guide-box__blurb">{e(x["blurb"])}</span></span>')
            if s_ == a["slug"]:
                return (f'<li data-date="{x["date"]}" aria-current="page"><span class="guide-box__item">{inner}'
                        f'<span class="guide-box__here">この記事</span></span></li>')
            return (f'<li data-date="{x["date"]}"><a href="media/{s_}.html" class="guide-box__item" title="{e(x["title"])}">{inner}'
                    f'<span class="guide-box__go" aria-hidden="true">›</span></a></li>')
        lis = "".join(_gb_item(n_, s_) for n_, s_ in enumerate(g["slugs"], 1))
        guide_box = f"""
        <nav class="guide-box" aria-label="この記事を含むガイド">
          <p class="guide-box__label">この記事を含むガイド</p>
          <a href="media/guide-{g["key"]}.html" class="guide-box__title">{e(g["title"])}</a>
          <ol class="guide-box__list">{lis}</ol>
          <a href="media/guide-{g["key"]}.html" class="guide-box__all">ガイドを全部見る {ARROW}</a>
        </nav>
"""
    body = f"""    <article class="article" data-publish="{a["date"]}">
      <header class="article__header">
        <div class="container container--article">
          {media_crumbs([("アキヤド", "media.html"), (MEDIA_CAT_NAMES[a["category"]], f"media/category-{a['category']}.html")]).strip()}
          <div class="article__cats">{"".join(f'<a href="media/category-{t}.html" class="tag article__cat">{e(MEDIA_CAT_NAMES[t])}</a>' for t in a["topics"])}</div>
          <h1 class="article__title">{e(a["title"])}</h1>
          <p class="article__meta">
            <span>公開日 <time datetime="{a["date"]}">{fmt_date(a["date"])}</time></span>
            <span>更新日 <time datetime="{a["updated"]}">{fmt_date(a["updated"])}</time></span>
            <span>読了目安 約{read_minutes(a)}分</span>
            <span>執筆：アキヤド編集部</span>
            <span>監修：{e(SUPERVISOR["name"])}</span>
          </p>
          {for_html}
          {thumb(a, "hero")}
        </div>
      </header>

      <div class="container container--article article__body">
        <p class="article__lead">{lines_html(a["description"])}</p>

        <section class="keypoints" aria-labelledby="keypoints-title">
          <h2 id="keypoints-title" class="keypoints__title">この記事のポイント</h2>
          <ul>{keypoints}</ul>
        </section>

        <aside class="inline-cta">
          <p class="inline-cta__text">{e(cv_text)}</p>
          <div class="inline-cta__actions">
            <a href="contact.html?category={a["services"][0]}&amp;from=akiyado" class="btn mbtn" data-cta="media-inline">無料で相談する {ARROW}</a>
            <a href="{cv_href}" class="inline-cta__plan">サービスとプランを見る {ARROW}</a>
          </div>
        </aside>

        <a class="to-toc" href="#toc" hidden>目次に戻る<span aria-hidden="true"> ↑</span></a>
        <nav class="toc" id="toc" aria-label="目次">
          <details class="toc__details">
            <summary class="toc__title">目次を開く（全{len(a["sections"]) + 1}章）</summary>
            <ol>{toc}<li><a href="#faq">よくある質問</a></li></ol>
          </details>
        </nav>

{sections}

        <section class="article__section" id="faq">
          <h2>よくある質問</h2>
          <div class="faq">
{faq_html(a["faq"])}
          </div>
        </section>

{note_story() if a["slug"] in NOTE_STORY_ARTICLES else ""}        <section class="sources">
          <details class="sources__fold">
            <summary class="sources__title">参考資料（{len(a["sources"])}件）</summary>
            <ul>{sources}</ul>
            <p class="sources__note">※ 本記事の数値・制度は公開日時点で公表されている資料にもとづきます。最新の情報は各機関の発表をご確認ください。</p>
          </details>
        </section>

{guide_box}
        <div class="share">
          <p class="share__label">この記事をシェアする</p>
          <ul class="share__list">
            <li><a href="https://twitter.com/intent/tweet?url={share_url}&amp;text={share_text}" target="_blank" rel="noopener">X</a></li>
            <li><a href="https://social-plugins.line.me/lineit/share?url={share_url}" target="_blank" rel="noopener">LINE</a></li>
            <li><a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" rel="noopener">Facebook</a></li>
            <li><button type="button" class="share__copy" data-url="{SITE}/media/{a["slug"]}.html">リンクをコピー</button></li>
          </ul>
        </div>

        <section class="author" data-nosnippet>
          <p class="author__label">この記事を書いた人</p>
          <p class="author__name">アキヤド編集部</p>
          <p class="author__text">合同会社RIVIA&amp;CO.のメディア編集部。空き家の再生から宿泊施設の運営・開業支援、WEB集客・採用支援まで、自ら宿を運営する当事者の視点で、地域の価値を活かすための情報をお届けします。</p>
          <p class="author__text">実績：「NODE Shimoda」（静岡県下田市）を開業・運営。アキヤドの運営チームが関わる3物件では、ゲストの質問408件とレビュー79件を分析して記事にまとめています（2026年）。</p>
        </section>

        <section class="supervisor" data-nosnippet>
          <figure class="supervisor__photo"><img src="images/{SUPERVISOR["photo"]}" alt="{e(SUPERVISOR["name"])}の写真" width="600" height="600" loading="lazy" decoding="async"></figure>
          <div>
            <p class="author__label">この記事の監修者</p>
            <p class="author__name">{e(SUPERVISOR["name"])}<span class="supervisor__role">{e(SUPERVISOR["role"])}</span></p>
            <p class="author__text">{e(SUPERVISOR["bio"])}</p>
            <div class="supervisor__links">
              <a href="about.html#founders" class="supervisor__more">プロフィールを見る {ARROW}</a>
              <ul>{"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SUPERVISOR["links"])}</ul>
            </div>
          </div>
        </section>

        <aside class="article-cta">
          <p class="article-cta__title">この記事に関連するサービス</p>
          <ul class="article-cta__links">{svc_links}</ul>
          <a href="contact.html?category={svc}" class="btn btn--lg">無料で相談する {ARROW}</a>
        </aside>
      </div>
    </article>

{media_section(related, eyebrow="Related", title="あわせて読みたい記事", more=False, keep_order=True)}"""

    ld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": a["title"],
            "description": a["description"],
            "datePublished": a["date"],
            "dateModified": a["updated"],
            "image": (f"{SITE}/{eyecatch_path(a)}" if has_eyecatch(a) else f"{SITE}/images/ogp.jpg"),
            "mainEntityOfPage": f"{SITE}/media/{a['slug']}.html",
            "author": {"@type": "Organization", "name": "アキヤド編集部（合同会社RIVIA&CO.）", "url": f"{SITE}/about.html", "parentOrganization": {"@id": ORG_ID}},
            "contributor": {"@type": "Person", "@id": person_id(SUPERVISOR["key"]), "name": SUPERVISOR["name"], "jobTitle": "合同会社RIVIA&CO. 代表社員（監修）", "url": f"{SITE}/about.html#founders", "sameAs": [u for _, u in SUPERVISOR["links"]]},
            "publisher": org_ref(),
            "articleSection": MEDIA_CAT_NAMES[a["category"]],
            "inLanguage": "ja",
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "TOP", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "アキヤド", "item": f"{SITE}/media.html"},
                {"@type": "ListItem", "position": 3, "name": MEDIA_CAT_NAMES[a["category"]], "item": f"{SITE}/media/category-{a['category']}.html"},
                {"@type": "ListItem", "position": 4, "name": a["title"]},
            ],
        },
    ]
    page(f"media/{a['slug']}.html", a["title"], a["description"], body, current="media", jsonld=ld, cv_category=a["services"][0],
         og_type="article", og_image=(eyecatch_path(a) if has_eyecatch(a) else f"images/photos/{ARTICLE_PHOTOS[a['slug']][0]}.jpg"))
