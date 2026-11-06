# -*- coding: utf-8 -*-
# build.py の一部：404 ページ・llms.txt・sitemap.xml・robots.txt。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

def not_found_page():
    """存在しないURLを開いたときのページ（Vercel はサイト直下の 404.html を使う）。
    どの階層のURLでも表示できるよう、リンクはすべて / から始まる絶対パスにする"""
    import re as _re
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en">404</p>
        <h1 class="page-hero__ja">お探しのページが見つかりませんでした</h1>
        <p class="page-hero__lead">URLが変わったか、ページが削除された可能性があります。トップページや記事一覧からお探しください。</p>
        <div class="hero__actions" style="margin-top:40px">
          <a href="index.html" class="btn">トップページへ {ARROW}</a>
          <a href="media.html" class="btn btn--ghost">アキヤド（記事一覧）へ</a>
        </div>
      </div>
    </section>"""
    page("404.html", "ページが見つかりません", "お探しのページが見つかりませんでした。", body, noindex=True)
    src = os.path.join(OUT, PAGES_DIR, "404.html")
    html = open(src, encoding="utf-8").read()
    def absolute(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http:", "https:", "#", "data:", "mailto:", "tel:", "/")):
            return m.group(0)
        url = _re.sub(r"^(\.\./)+", "", url)
        return f'{attr}="/{"" if url == "index.html" else url}"'
    html = _re.sub(r'\b(href|src)="([^"]*)"', absolute, html)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    os.remove(src)


def llms_txt():
    """AI（LLM）向けにサイトとメディアの概要をまとめた llms.txt（https://llmstxt.org/ の形式）"""
    lines = ["# 合同会社RIVIA&CO.", "",
             "> 空き家の再生、民泊・小さな宿の開業と運営、WEB集客・採用を支援する会社です。運営メディア「アキヤド（空き家と民泊のメディア）」では、空き家を売りたい方・活かしたい方・副業で民泊をはじめたい方に向けて、悩みの順に記事を公開しています。",
             "", "## 会社", f"- [会社概要]({SITE}/about.html): ミッション・ビジョン・バリューと創業者",
             f"- [お問い合わせ]({SITE}/contact.html): 無料相談の窓口", "", "## サービス", f"- [事業内容]({SITE}/services.html): 5つの事業の一覧"]
    lines += [f"- [{n}]({SITE}/service-{k}.html)" for k, n in SERVICES]
    lines += ["", "## アキヤド（ガイド）"]
    lines += [f"- [{g['title']}]({SITE}/media/guide-{g['key']}.html): {g['lead']}" for g in MEDIA_GUIDES]
    lines += ["", "## アキヤド（記事）"]
    lines += [f"- [{a['title']}]({SITE}/media/{a['slug']}.html): {a['description']}"
              for a in sorted(ARTICLES, key=lambda x: x["date"]) if a["date"] <= BUILD_DATE]
    with open(os.path.join(OUT, SEO_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def sitemap():
    pages = ["", "about.html", "services.html"] + [f"service-{k}.html" for k, _ in SERVICES] + \
            ["media.html"] + [f"media/category-{k}.html" for k, _ in MEDIA_CATEGORIES] + [f"media/guide-{g['key']}.html" for g in MEDIA_GUIDES] + ["media/plans.html"] + [f"media/{sv['slug']}.html" for sv in MEDIA_SERVICES] + ["media/company.html", "media/learn.html", "media/contact.html"] + [f"media/{a['slug']}.html" for a in ARTICLES if a["date"] <= BUILD_DATE] + ["careers.html", "contact.html", "privacy.html"]
    # 公開日前の記事は sitemap に載せない（公開日を迎えて作り直すと載る）。
    # 記事ページは JS で転送しない（転送すると Google に「ページにリダイレクトがあります」と記録されるため。2026-10-22）
    pages += ["en/" + ("" if f == "index.html" else f) for f in EN_PAGES if f != "thanks.html"]
    lastmod = {f"media/{a['slug']}.html": a["updated"] for a in ARTICLES}
    # 記事の一覧ページにも、載せている記事のいちばん新しい更新日を付ける（クロールの優先度の手がかり）
    published = [a for a in ARTICLES if a["date"] <= BUILD_DATE]
    if published:
        newest = max(a["updated"] for a in published)
        for hub in ["media.html", "media/learn.html"] + [f"media/guide-{g['key']}.html" for g in MEDIA_GUIDES]:
            lastmod[hub] = newest
        for k, _ in MEDIA_CATEGORIES:
            ds = [a["updated"] for a in published if k in a.get("topics", [a["category"]])]
            if ds:
                lastmod[f"media/category-{k}.html"] = max(ds)
    urls = "\n".join(
        f"  <url><loc>{SITE}/{p}</loc>" + (f"<lastmod>{lastmod[p]}</lastmod>" if p in lastmod else "") + "</url>"
        for p in pages
    )
    os.makedirs(os.path.join(OUT, SEO_DIR), exist_ok=True)
    with open(os.path.join(OUT, SEO_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")
    with open(os.path.join(OUT, SEO_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        # AI検索・生成AIのロボットも名前を挙げて明示的に許可する（noindex のページは各ページの meta robots で外す。Disallow は置かない）
        bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
                "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "CCBot"]
        f.write("# AI検索・生成AIのロボットも含めて、すべて許可する方針\n\n"
                "User-agent: *\nAllow: /\n\n"
                + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
                + f"Sitemap: {SITE}/sitemap.xml\n")
