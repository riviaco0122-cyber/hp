# 英語版を作るための共通処理：日本語ページのHTMLを正規化し、訳すべき文字列（テキスト・属性）を取り出す
import re
from bs4 import BeautifulSoup, NavigableString, Comment

JA = re.compile(r"[ぁ-んァ-ヶ一-龥々〆ヵヶ「」『』（）、。・〜！？]")
CORP_PAGES = ["index.html", "about.html", "careers.html", "contact.html", "privacy.html", "thanks.html",
              "service-operation.html", "service-management.html", "service-partnership.html",
              "service-marketing.html", "service-recruit.html"]
ATTRS = ["alt", "aria-label", "placeholder", "title", "data-default", "data-label"]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def drop_media(soup):
    """アキヤド（日本語のみのメディア）の記事一覧は英語版に載せない"""
    for g in soup.select(".media-grid"):
        sec = g.find_parent("section")
        if sec:
            sec.decompose()


def soup_of(html):
    html = html.replace("<wbr>", "")
    soup = BeautifulSoup(html, "html.parser")
    drop_media(soup)
    for t in soup.find_all(["n-w", "n-b"]):
        t.unwrap()
    soup.smooth()
    return soup


def block_text(node):
    """テキストが属する段落（ブロック）全体の文字列。訳すときの文脈に使う"""
    p = node.parent
    while p is not None and p.name not in ("p", "li", "h1", "h2", "h3", "h4", "td", "th", "dd", "dt", "label", "button", "a", "figcaption", "blockquote", "summary", "option", "title"):
        p = p.parent
    return norm(p.get_text(" ")) if p is not None else ""


def segments(soup):
    """(種類, 文字列, 文脈) を順に返す。種類は text / attr:名前 / meta"""
    out = []
    head = soup.find("head")
    if head:
        t = head.find("title")
        if t and JA.search(t.get_text()):
            out.append(("text", norm(t.get_text()), "page title"))
        for m in head.find_all("meta"):
            c = m.get("content", "")
            if (m.get("name") in ("description",) or m.get("property") in ("og:title", "og:description", "og:site_name")) and JA.search(c):
                out.append(("meta", norm(c), "meta " + (m.get("name") or m.get("property"))))
    body = soup.find("body")
    for node in body.descendants:
        if isinstance(node, Comment):
            continue
        if isinstance(node, NavigableString):
            if node.parent.name in ("script", "style"):
                continue
            s = norm(str(node))
            if s and JA.search(s):
                out.append(("text", s, block_text(node)))
        elif hasattr(node, "attrs"):
            for a in ATTRS:
                v = node.attrs.get(a)
                if isinstance(v, str) and JA.search(v):
                    out.append(("attr:" + a, norm(v), node.name))
            if node.name == "input" and node.get("type") in ("submit", "button") and JA.search(node.get("value", "")):
                out.append(("attr:value", norm(node["value"]), "button"))
    return out
