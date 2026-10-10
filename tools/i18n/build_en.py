# 日本語のコーポレートページ（pages/*.html）から、英語版（pages/en/*.html）を作る。
# 文言は source.json の順番に対応した英訳（en_1〜en_4）で置き換える。アキヤド（メディア）は日本語のみ。
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from bs4 import NavigableString, Comment
from common import CORP_PAGES, ATTRS, JA, norm, soup_of
from en_1 import EN_1
from en_2 import EN_2
from en_3 import EN_3
from en_4 import EN_4

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(os.path.dirname(os.path.dirname(HERE)), "pages")
SITE = "https://rivia-co.com"


def dictionary():
    src = json.load(open(os.path.join(HERE, "source.json"), encoding="utf-8"))
    en = {**EN_1, **EN_2, **EN_3, **EN_4}
    T = {r["s"]: en[i] for i, r in enumerate(src) if i in en}
    # フォームの隠し項目（社内に届くメールの件名など）は、英語サイトからだと分かる日本語にする
    T.update({
        "【RIVIA&CO.】Webサイトからのお問い合わせ": "【RIVIA&CO.】Webサイトからのお問い合わせ（英語サイト）",
        "【RIVIA&CO.】採用エントリー": "【RIVIA&CO.】採用エントリー（英語サイト）",
        "同意する": "Agree",
        # TOP：地域の経済循環の図
        "空き家を、": "Vacant homes", "宿に再生": "become inns",
        "旅行者が、": "Travelers", "まちを訪れる": "visit the town",
        "まちで、": "They dine", "食べて買う": "and shop locally",
        "ファンになり、": "They become fans", "また訪れる": "and come back",
        "次の空き家へ": "Next home",
        "サービス資料の請求": "Request our service brochure (Japanese)",
        "地域に、": "People and money", "人とお金がめぐる": "circulate locally",
        "空き家を宿に再生し、旅行者がまちを訪れ、まちで食べて買い、ファンになって再び訪れる。その収益で次の空き家を再生する、地域の経済循環":
            "A local economic cycle: vacant homes become inns, travelers visit, dine and shop locally, become fans and return, and the profits revive the next home",
    })
    # サービスページ冒頭のかんたん相談フォーム
    T.update({
        "ご相談内容": "Your message",
        "まだ検討中の段階でも大丈夫です。2営業日以内にご連絡します。": "It's fine if you're still considering. We'll reply within two business days.",
        "物件の場所や、気になっていることなど": "e.g. where the property is, or what's on your mind",
        "送信により": "By sending, you agree to our",
        "に同意したものとします。しつこい営業はしません。": ". We never make pushy sales.",
    })
    for ja in ["空き家再生事業", "宿泊施設 開業・運営支援事業", "不動産事業者様との協業", "WEB集客支援事業", "WEB採用支援事業"]:
        en = T.get(ja, ja)
        T[f"{ja}の無料相談"] = f"Free consultation: {en}"
        # 社内に届く件名・流入元は日本語のまま、英語サイトからと分かるようにする
        T[f"【RIVIA&CO.】{ja}のご相談（サービスページ）"] = f"【RIVIA&CO.】{ja}のご相談（サービスページ・英語サイト）"
        T[f"サービスページ：{ja}"] = f"サービスページ（英語サイト）：{ja}"
    return T


def fix_link(url):
    """英語ページは pages/en/ にあるため、リンクの階層を直す"""
    if not url or url.startswith(("http:", "https:", "#", "mailto:", "tel:", "data:", "/")):
        return url
    path = url.split("#")[0].split("?")[0]
    if path.endswith(".html") and not url.startswith("../"):
        # アキヤド（日本語のみ）は日本語ページへ。それ以外は英語ページ同士でつなぐ
        return "../" + url if (path.startswith("media") ) else url
    return "../" + url  # 画像・CSS・JS など


def build(filename, T, missing):
    soup = soup_of(open(os.path.join(PAGES, filename), encoding="utf-8").read())
    soup.html["lang"] = "en"
    # 構造化データは日本語のままなので外す
    for s in soup.find_all("script", type="application/ld+json"):
        s.decompose()
    head = soup.head
    # アキヤド（日本語のみ）の欄は英語版にないため、ロゴ用のフォントも読み込まない
    for l in head.find_all("link", href=lambda h: h and "Zen+Maru+Gothic" in h):
        l.decompose()
    t = head.find("title")
    if t:
        t.string = T.get(norm(t.get_text()), norm(t.get_text()))
    for m in head.find_all("meta"):
        c = m.get("content", "")
        if JA.search(c):
            k = norm(c)
            if k in T:
                m["content"] = T[k]
            else:
                missing.add(k)
        if m.get("property") == "og:url":
            m["content"] = m["content"].replace(SITE + "/", SITE + "/en/", 1)
        if m.get("property") == "og:locale":
            m["content"] = "en_US"
    can = head.find("link", rel="canonical")
    if can:
        can["href"] = can["href"].replace(SITE + "/", SITE + "/en/", 1)
    # 本文のテキストと属性
    for node in list(soup.body.descendants):
        if isinstance(node, Comment):
            continue
        if isinstance(node, NavigableString):
            if node.parent.name in ("script", "style"):
                continue
            raw = str(node)
            k = norm(raw)
            if k and JA.search(k):
                if k in T:
                    lead = " " if raw[:1].isspace() else ""
                    trail = " " if raw[-1:].isspace() else ""
                    node.replace_with(lead + T[k] + trail)
                else:
                    missing.add(k)
        elif hasattr(node, "attrs"):
            for a in ATTRS + ["value"]:
                v = node.attrs.get(a)
                if isinstance(v, str) and JA.search(v):
                    k = norm(v)
                    if k in T:
                        node[a] = T[k]
                    else:
                        missing.add(k)
    # リンクの階層
    for tag in soup.find_all(True):
        for a in ("href", "src"):
            if tag.has_attr(a) and not (tag.name == "link" and tag.get("rel") in (["canonical"], ["alternate"])):
                tag[a] = fix_link(tag[a])
        if tag.has_attr("srcset"):
            tag["srcset"] = ", ".join(" ".join([fix_link(p.split(" ")[0])] + p.split(" ")[1:]) for p in tag["srcset"].split(", "))
        if tag.name == "form" and tag.has_attr("data-thanks"):
            pass  # thanks.html は英語ページ同士の相対リンクのまま
    # 言語切り替え：英語ページから日本語ページへ
    sw = soup.select_one(".lang-switch")
    if sw:
        sw["href"] = "../" + filename
        sw["hreflang"] = "ja"
        sw["lang"] = "ja"
        sw.string = "JP"
        sw["aria-label"] = "日本語"
    # メディア（アキヤド）は日本語のみであることを示す
    for a in soup.select('a[href="../media.html"]'):
        if a.get_text(strip=True) == "Media":
            a.string = "Media (JP)"
    html = str(soup)
    # 日本語は単語の間に空白がないため、太字・リンクの前後で英単語がくっつかないよう空白を補う
    html = re.sub(r"([A-Za-z0-9,;:%)])(<(?:strong|a|em|b)\b[^>]*>)", r"\1 \2", html)
    html = re.sub(r"(</(?:strong|a|em|b)>)([A-Za-z0-9(“\"])", r"\1 \2", html)
    os.makedirs(os.path.join(PAGES, "en"), exist_ok=True)
    with open(os.path.join(PAGES, "en", filename), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    T = dictionary()
    missing = set()
    for f in CORP_PAGES:
        build(f, T, missing)
    if missing:
        print("未翻訳:", len(missing))
        for m in sorted(missing)[:40]:
            print("  -", m)
    print("英語ページ:", len(CORP_PAGES))


if __name__ == "__main__":
    main()
