#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""okaeri/（Okaeri Japan の公開フォルダ）の全ページを点検する。エラーが1件でもあれば終了コード1。
アキヤドの点検（tools/seo_check.py）は pages/ だけを見るので、Okaeri Japan はこちらで見る。

  python3 tools/okaeri/seo_check.py           点検
  python3 tools/okaeri/seo_check.py --launch  公開前の点検（黄色い枠・未接続のフォームもエラーにする）
"""
import json
import os
import re
import sys
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CFG = json.load(open(os.path.join(HERE, "site.json"), encoding="utf-8"))
SITE = CFG["origin"].rstrip("/")
PRE = CFG["prefix"].rstrip("/")
DIST = os.path.join(ROOT, PRE.strip("/"))
LAUNCH = "--launch" in sys.argv
errors, warns = [], []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    (errors if LAUNCH else warns).append(f"{page}: {msg}")


def path_of(file):
    rel = os.path.relpath(file, DIST).replace(os.sep, "/")
    return PRE if rel == "index.html" else PRE + "/" + rel


def text(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True))


files = [os.path.join(d, f) for d, _, fs in os.walk(DIST) for f in fs if f.endswith(".html")]
pages = {path_of(f): BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser") for f in files}
sitemap = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(DIST, "sitemap.xml"), encoding="utf-8").read())
titles, descs = {}, {}

for p, s in sorted(pages.items()):
    noindex = "noindex" in (s.find("meta", attrs={"name": "robots"}) or {}).get("content", "")
    if s.html.get("lang") != "en":
        err(p, "html の lang が en ではない")
    t = s.title.string if s.title else ""
    if not t:
        err(p, "title がない")
    core = t.split(" | ")[0] if " | " in t and not t.startswith(CFG["name"]) else t
    if len(core) > 60:
        err(p, f"title が長い（{len(core)}字。60字以内）: {core}")
    if t.count("|") > 1:
        err(p, "title の | が2つ以上ある")
    d = (s.find("meta", attrs={"name": "description"}) or {}).get("content", "")
    if not noindex and not (110 <= len(d) <= 160):
        err(p, f"説明文の長さが範囲外（{len(d)}字。110〜160字）")
    if not noindex:
        titles.setdefault(t, []).append(p)
        descs.setdefault(d, []).append(p)
    h1 = s.find_all("h1")
    if len(h1) != 1:
        err(p, f"h1 が {len(h1)} 個（1個にする）")
    can = s.find("link", rel="canonical")
    if noindex:
        if SITE + p in sitemap:
            err(p, "noindex のページが sitemap に載っている")
    else:
        if not can or can.get("href") != SITE + p:
            err(p, "canonical が自分の URL と違う")
        if SITE + p not in sitemap:
            err(p, "sitemap に載っていない")
        for prop in ("og:title", "og:description", "og:url", "og:image"):
            if not s.find("meta", property=prop):
                err(p, f"{prop} がない")
        img = (s.find("meta", property="og:image") or {}).get("content", "")
        if img.startswith(SITE) and not os.path.exists(os.path.join(ROOT, img[len(SITE):].lstrip("/"))):
            err(p, "og:image のファイルがない")
    # 内部リンク
    for a in s.find_all("a", href=True):
        h = a["href"]
        if h == "/":
            pass  # 運営会社（アキヤド側のトップ）へのリンク
        elif h.startswith("/"):
            target = h.split("#")[0]
            if target.endswith("/index.html") or target.endswith("/"):
                err(p, f"index.html か末尾スラッシュつきのリンクがある（このドメインは末尾スラッシュなしで運用）: {h}")
            if target not in pages:
                err(p, f"リンク切れ: {h}")
            frag = h.split("#")[1] if "#" in h else ""
            if frag and target in pages and not pages[target].find(id=frag):
                err(p, f"リンク先に #{frag} がない: {h}")
        elif h.startswith("#"):
            if h != "#main" and not s.find(id=h[1:]):
                err(p, f"ページ内リンクの先がない: {h}")
        elif not h.startswith(("http://", "https://", "mailto:")):
            err(p, f"相対リンクがある（/ から始める）: {h}")
        if not text(a) and not a.find("svg") and not (a.find("img", alt=True) or a.get("aria-hidden") == "true"):
            err(p, f"リンクの文字が空: {h}")
    for im in s.find_all("img"):
        if not im.has_attr("alt"):
            err(p, "alt のない画像がある（飾りの画像は alt=\"\" にする）")
        elif not im["alt"] and not im.find_parent("a", class_="inline-stay"):
            err(p, "alt が空の画像がある（飾り以外は内容を書く）")
        if not (im.get("width") and im.get("height")):
            err(p, "width・height のない画像がある")
        if not os.path.exists(os.path.join(ROOT, im["src"].lstrip("/"))):
            err(p, f"画像のファイルがない: {im['src']}")
    # 構造化データ
    types, graph = [], []
    for sc in s.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string)
        except Exception as e:  # noqa: BLE001
            err(p, f"構造化データが JSON として読めない: {e}")
            continue
        graph += data.get("@graph", [data])
    types = [g.get("@type") for g in graph]
    if "WebSite" in types:
        err(p, "WebSite の宣言がある（サイト名の宣言は rivia-co.com のトップだけに置く）")
    if p != PRE:
        bc = [g for g in graph if g.get("@type") == "BreadcrumbList"]
        if not bc:
            err(p, "パンくずの構造化データがない")
        else:
            items = bc[0]["itemListElement"]
            if items[0]["name"] != CFG["name"] or items[0]["item"] != SITE + PRE or items[-1]["item"] != SITE + p:
                err(p, "パンくずが Okaeri Japan のトップから始まり自分で終わる形になっていない")
            vis = [text(li) for li in s.select(".crumbs li")]
            if vis != [i["name"] for i in items]:
                err(p, "見えているパンくずと構造化データが違う")
    if p.startswith(PRE + "/guides/"):
        art = [g for g in graph if g.get("@type") == "Article"]
        faq = [g for g in graph if g.get("@type") == "FAQPage"]
        if not art:
            err(p, "Article がない")
        else:
            a = art[0]
            if a["headline"] != text(h1[0]):
                err(p, "Article の headline と h1 が違う")
            if a["dateModified"] < a["datePublished"]:
                err(p, "更新日が公開日より前")
            tm = s.find("time")
            if not tm or tm.get("datetime") != a["dateModified"]:
                err(p, "表示している日付と dateModified が違う")
        if not faq:
            err(p, "FAQPage がない")
        else:
            qs = [text(h) for h in s.find_all("h3")]
            body = text(s.find("article"))
            for q in faq[0]["mainEntity"]:
                if q["name"] not in qs:
                    err(p, f"FAQ の質問が本文にない: {q['name']}")
                if q["acceptedAnswer"]["text"][:40] not in body:
                    err(p, f"FAQ の答えが本文と違う: {q['name']}")
            if len(faq[0]["mainEntity"]) < 3:
                err(p, "FAQ が3問未満")
        h2 = s.select("article h2")
        n = len([h for h in h2 if not h.find_parent(class_=["sources", "related", "cta"])])
        if not (4 <= n <= 9):
            warn(p, f"h2 が {n} 個（4〜9個が目安）")
        if len(s.select(".sources li")) < 3:
            err(p, "出典が3件未満")
        inner = {a["href"].split("#")[0] for a in s.select("article a[href^='/']") if not a.find_parent(class_=["crumbs", "cta", "byline", "related"])}
        if len(inner - {p}) < 1:
            warn(p, "本文からほかのページへの内部リンクがない")
    n_ed = len(s.select(".ednote"))
    if n_ed:
        warn(p, f"黄色い枠（未確認の箇所）が {n_ed} か所残っている")
    if s.find("form", attrs={"data-proto": True}):
        warn(p, "メール登録フォームがまだつながっていない")

for t, ps in titles.items():
    if len(ps) > 1:
        err(", ".join(ps), "title が重複")
for d, ps in descs.items():
    if len(ps) > 1:
        err(", ".join(ps), "説明文が重複")
for u in sitemap:
    if not u.startswith(SITE) or u[len(SITE):] not in pages:
        err("sitemap.xml", f"存在しない URL: {u}")
rb = open(os.path.join(ROOT, "seo", "robots.txt"), encoding="utf-8").read()
if f"Sitemap: {SITE}{PRE}/sitemap.xml" not in rb:
    err("seo/robots.txt", f"Okaeri Japan の sitemap（{PRE}/sitemap.xml）の行がない。tools/build.py を実行する")
vj = json.load(open(os.path.join(ROOT, "vercel.json"), encoding="utf-8"))
if not any(r.get("source") == PRE and r.get("destination") == PRE + "/index.html" for r in vj.get("rewrites", [])):
    err("vercel.json", f"{PRE} → {PRE}/index.html の rewrites がない（トップが開けない）")
for r in vj.get("redirects", []):
    if r.get("source", "").startswith(PRE):
        err("vercel.json", f"{PRE} に redirects がかかっている: {r['source']}")
if PRE + "/sitemap.xml" in "".join(sitemap):
    err("sitemap.xml", "sitemap 自身が載っている")
if not CFG.get("ga4_id"):
    warn("site.json", "GA4 の測定IDが未設定")

print(f"点検: {len(pages)} ページ ／ エラー {len(errors)} ／ 警告 {len(warns)}")
for e in errors:
    print("  エラー  " + e)
for w in warns:
    print("  警告    " + w)
sys.exit(1 if errors else 0)
