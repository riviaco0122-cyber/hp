#!/usr/bin/env python3
"""記事の機械採点（100点満点のうち40点分）と、必須条件（ゲート）の判定。品質管理部が使う。

採点基準の全体（機械40点＋品質管理部60点、合格95点以上）は docs/seo/playbook.md 5章。

使い方:
  python3 tools/article_score.py docs/seo/drafts/<slug>.md      # 原稿（執筆担当の Markdown）
  python3 tools/article_score.py pages/media/<slug>.html         # HTML 化した記事
  オプション: --keyword "主キーワード"（省略時は原稿の keyword: か構成案から読む） --json

原稿（Markdown）の決まった形は .claude/agents/writer.md を参照。
終了コード: ゲート違反があれば 2、なければ 0。

判定の要点:
  - 重大NGは、直後（最初の「。」か改行まで・最大16字）に否定（〜わけではない、〜ません など）があれば除く。
  - NG・表記ゆれは、h2 見出しも対象。かぎかっこ「」『』の中と、引用（Markdown の > 行・HTML の <blockquote>）は対象外。
  - 参考資料（原稿）は「- 資料名（発行元・公表年）URL」の形。URL と4桁の年の両方がある行だけ数える。
    HTML の既存記事は URL がなくても数え、根拠欄に「URLなし」と出す。公的機関は go.jp・lg.jp などのドメインか、
    省庁・自治体の正式名称で判定する。
  - 回帰テスト: python3 tools/tests/test_article_score.py（ケースは tools/tests/score_cases.json）
"""
import argparse
import html as htmllib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---- ルール（docs/brand/ng.md・glossary.md から機械判定できるものを抜き出したもの） ----
# 重大な NG（1件でもゲート違反＝不合格）: 誇大・保証・断定
# 直後（「。」・改行まで、最大16字）に否定があるものは除く（NEGATION を参照）。
_P100 = r"[1１][0０][0０]\s?[%％]"
NG_SEVERE = [
    r"必ず(儲|稼|成功|採択|もらえ|許可が(下り|取れ))", r"確実に(儲|稼|成功)",
    r"絶対(に)?(儲|稼|成功|安全|大丈夫|失敗し(ない|ません))",
    r"(利回り|収益|家賃|元本).{0,8}保証", r"満室保証",
    r"[NnＮｎ][OoＯｏ][.．]?\s?[1１](?![0-9０-９])|ナンバーワン|日本一|日本初|国内初|業界初|業界No",
    r"(誰|だれ)でも(簡単|すぐ)", r"手間(ゼロ|なし|いらず)", r"リスク(ゼロ|なし|は(ありません|ない))",
    _P100 + r"\s?の?(安全|成功|稼働|満室)", r"(稼働率?|満室率?|満室)\s?(は|が|も)?\s?" + _P100,
    r"最安", r"唯一", r"自己資金(は|が)?\s?(ゼロ|[0０]\s?円|なし)", r"不労所得", r"放って(おいて|置いて)も",
    r"掘り出し物|掘出物", r"格安物件",
    r"(届出|許可)(は|が|も)?\s?(不要|いりません|要りません|必要ありません|必要ない)",
]
# 否定の判定: マッチの直後から最初の「。」（または改行）までの、最大16字の中だけを見る
NEGATION = r"わけではな|とは限ら|ではありませ|ではな[いく]|ません|ない|にくい|難しい|誤解"
NEG_WINDOW = 16
# 軽い NG（1件ごとに減点）: あおり・言葉づかい
NG_MINOR = [
    r"今すぐ(行動|始め)", r"知らないと(損|大変)", r"手遅れ(です|になります|になる前に)", r"放置すると(必ず|確実に)",
    r"激安|爆益|最強|神(宿|物件)", r"弊社", r"！",
]
# 表記ゆれ（使わない表記 → 統一表記）
GLOSSARY = [
    (r"ヶ月|カ月|ヵ月", "か月"), (r"下さい", "ください"), (r"出来(る|ます|ない)", "できる"),
    (r"様々", "さまざま"), (r"例えば", "たとえば"), (r"問合せ|問合わせ", "問い合わせ"),
    (r"％", "%（半角）"), (r"Web\s?サイト", "ウェブサイト"), (r"二拠点生活", "二地域居住"),
    (r"町並み|街並み", "まちなみ"), (r"宿泊単価", "客室単価"), (r"(?<!ひとつ)ひとつ(?!ひとつ|ずつ)", "一つ"),
    (r"(?<!を)わか(る|ら|り|れ)", "分かる"),
]
# 参考資料: 公的機関の判定（URL のドメイン、または省庁・自治体の正式名称）
PUBLIC_DOMAIN = r"https?://(?:[\w-]+\.)*(?:go\.jp|lg\.jp|e-gov\.go\.jp|(?:pref|city|town|vill)\.[\w.-]+\.jp)(?:[/:?#]|$)"
_PREFS = ("北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県|新潟県|富山県|"
          "石川県|福井県|山梨県|長野県|岐阜県|静岡県|愛知県|三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県|鳥取県|島根県|"
          "岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県")
PUBLIC_NAME = (
    r"国土交通省|観光庁|厚生労働省|総務省|国税庁|消防庁|内閣府|内閣官房|法務省|財務省|経済産業省|中小企業庁|文化庁|"
    r"農林水産省|環境省|金融庁|デジタル庁|気象庁|文部科学省|外務省|復興庁|スポーツ庁|林野庁|水産庁|消費者庁|"
    r"出入国在留管理庁|資源エネルギー庁|国立社会保障・人口問題研究所|日本政府観光局|JNTO|e-Gov|法務局|"
    # 都道府県（直後が「の」のもの＝「〇〇県の不動産会社」などは除く）
    r"(?:" + _PREFS + r")(?:庁)?(?!の)"
    # 市区町村は、役所・役場・公式サイト・担当課の形のときだけ
    r"|[一-龥ァ-ヶ]{1,6}[市区町村]\s?(?:役所|役場|公式|ホームページ|ウェブサイト|[一-龥]{1,8}課)"
)
URL_RE = r"https?://\S+"
YEAR_RE = r"(?<![0-9])(19|20)[0-9]{2}(?![0-9])"
# 見出しの形: 疑問・定義・結論・まとめ／比較・やり方の型
HEADING_FORM = r"[？?]$|とは|(です|ます|ましょう|よう|べき)$|まとめ|違い|方法|手順|選び方|ポイント"


def remove_quotes(s):
    """かぎかっこ「」『』の中を除く（レビュー原文などの引用を書き換えさせないため）。入れ子にも対応。"""
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"「[^「」\n]*」|『[^『』\n]*』", "「」", s)
    return s


def is_public(src):
    return bool(re.search(PUBLIC_DOMAIN, src) or re.search(PUBLIC_NAME, src))


def find_severe(text):
    hits = []
    for p in NG_SEVERE:
        for m in re.finditer(p, text):
            after = re.split(r"[。\n]", text[m.end():m.end() + NEG_WINDOW], maxsplit=1)[0]
            if not re.search(NEGATION, after):  # 「必ず採択されるわけではありません」などの否定は除く
                hits.append(m.group(0))
    return hits


def strip_tags(s):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return htmllib.unescape(s)


def parse_html(text):
    d = {}
    m = re.search(r'<h1[^>]*class="article__title"[^>]*>(.*?)</h1>', text, re.S)
    d["title"] = strip_tags(m.group(1)).strip() if m else ""
    m = re.search(r'<meta name="description" content="([^"]*)"', text)
    d["description"] = htmllib.unescape(m.group(1)) if m else ""
    m = re.search(r'<section class="keypoints".*?</section>', text, re.S)
    d["keypoints"] = [strip_tags(x).strip() for x in re.findall(r"<li>(.*?)</li>", m.group(0), re.S)] if m else []
    secs = re.findall(r'<section class="article__section" id="([^"]*)">(.*?)</section>', text, re.S)
    body_secs = [(i, s) for i, s in secs if i != "faq"]
    d["h2"] = [strip_tags(h).strip() for _, s in body_secs for h in re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)]
    body = "".join(s for _, s in body_secs)
    lead = re.search(r'<p class="article__lead">(.*?)</p>', text, re.S)
    d["body_text"] = (strip_tags(lead.group(1)) if lead else "") + "\n" + strip_tags(body)
    # NG・表記ゆれの判定用: <blockquote>（引用）を除いた本文
    unq = re.sub(r"<blockquote\b.*?</blockquote>", "\n", body, flags=re.S)
    d["check_text"] = (strip_tags(lead.group(1)) if lead else "") + "\n" + strip_tags(unq)
    d["format"] = "html"
    d["faq"] = [strip_tags(q).strip() for q in re.findall(r'<summary class="faq__q">(.*?)</summary>', text, re.S)]
    d["faq_text"] = strip_tags(" ".join(re.findall(r'<div class="faq__a">(.*?)</div>', text, re.S)))
    faq_ld = re.search(r'"@type": "FAQPage", "mainEntity": (\[.*?\])\}</script>', text, re.S)
    d["faq_ld"] = len(json.loads(faq_ld.group(1))) if faq_ld else 0
    m = re.search(r'<section class="sources">.*?</section>', text, re.S)
    d["sources"] = [strip_tags(x).strip() for x in re.findall(r"<li>(.*?)</li>", m.group(0), re.S)] if m else []
    links = re.findall(r'href="([^"]+)"', body)
    d["article_links"] = sorted({l for l in links if re.search(r"media/[a-z0-9-]+\.html", l) and "category-" not in l and "guide-" not in l})
    cta = re.search(r'<aside class="article-cta">.*?</aside>', text, re.S)
    d["service_links"] = sorted(set(re.findall(r'href="[^"]*(service-[a-z]+\.html)', body + (cta.group(0) if cta else ""))))
    d["keyword"] = ""
    return d


def parse_md(text):
    d = {"keyword": ""}
    fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", fm.group(1), re.M)) if fm else {}
    body = text[fm.end():] if fm else text
    d["title"] = meta.get("title", "").strip()
    d["description"] = meta.get("description", "").strip()
    d["keyword"] = meta.get("keyword", "").strip()
    parts = re.split(r"(?m)^## ", body)
    sec = {p.split("\n", 1)[0].strip(): (p.split("\n", 1)[1] if "\n" in p else "") for p in parts[1:]}
    kp = next((v for k, v in sec.items() if "ポイント" in k and "この記事" in k), "")
    d["keypoints"] = [x.strip() for x in re.findall(r"(?m)^[-*]\s+(.*)$", kp)]
    fixed = ("この記事のポイント", "よくある質問", "参考資料")
    body_keys = [k for k in sec if not any(f in k for f in fixed)]
    d["h2"] = body_keys
    # 本文には h2 見出しも含める（見出しの NG・表記ゆれも判定するため）
    d["body_text"] = parts[0] + "\n" + "\n".join(k + "\n" + sec[k] for k in body_keys)
    # NG・表記ゆれの判定用: Markdown の引用（> で始まる行）を除いた本文
    d["check_text"] = "\n".join(l for l in d["body_text"].split("\n") if not l.lstrip().startswith(">"))
    d["format"] = "md"
    faq = next((v for k, v in sec.items() if "よくある質問" in k), "")
    d["faq"] = re.findall(r"(?m)^### (?:Q[.:：]?\s*)?(.*)$", faq)
    d["faq_ld"] = len(d["faq"])
    d["faq_text"] = faq
    src = next((v for k, v in sec.items() if "参考資料" in k), "")
    d["sources"] = [x.strip() for x in re.findall(r"(?m)^[-*]\s+(.*)$", src)]
    links = re.findall(r"\]\(([^)]+)\)", d["body_text"])
    d["article_links"] = sorted({l for l in links if re.search(r"media/[a-z0-9-]+\.html", l)})
    d["service_links"] = sorted({m for l in re.findall(r"\]\(([^)]+)\)", body) for m in re.findall(r"service-[a-z]+\.html", l)})
    return d


def md_plain(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`>#|]", "", s)
    return s


def score(d):
    items, gates = [], []

    def add(name, got, mx, note):
        items.append({"項目": name, "得点": max(0, min(mx, got)), "満点": mx, "根拠": note})

    title, kw = d["title"], d["keyword"]
    tl = len(title)
    add("title の長さ（40字以内）", 2 if 0 < tl <= 40 else (1 if tl <= 45 else 0), 2, f"{tl}字")
    head = kw.split()[0] if kw else ""
    pos = title.find(head) if head else -1
    add("主キーワードが title の前半（20字以内）にある", 3 if 0 <= pos <= 20 else 0, 3,
        f"キーワード「{head or '未指定'}」の位置 {pos if pos >= 0 else 'なし'}")
    dl = len(d["description"])
    add("meta description（50〜140字）", 3 if 50 <= dl <= 140 else (1 if 40 <= dl <= 160 else 0), 3, f"{dl}字")
    kp = len(d["keypoints"])
    add("この記事のポイント（3〜5項目）", 4 if 3 <= kp <= 5 else (2 if kp in (2, 6) else 0), 4, f"{kp}項目")
    h2 = d["h2"]
    form = sum(1 for h in h2 if re.search(HEADING_FORM, h))
    add("見出し h2 の数（4〜8個）", 2 if 4 <= len(h2) <= 8 else (1 if 3 <= len(h2) <= 10 else 0), 2, f"{len(h2)}個")
    ratio = form / len(h2) if h2 else 0
    add("見出しが疑問・結論の形（60%以上）", 2 if ratio >= 0.6 else (1 if ratio >= 0.4 else 0), 2, f"{form}/{len(h2)}")
    fq = len(d["faq"])
    ok_ld = d["faq_ld"] == fq
    add("よくある質問（3問以上・構造化データと一致）", (2 if fq >= 3 else 0) + (2 if ok_ld and fq else 0), 4,
        f"{fq}問／構造化データ {d['faq_ld']}問")
    src = d["sources"]
    if d.get("format") == "html":
        # 既存の HTML 記事は参考資料に URL がないものが多いので、URL なしでも数える（根拠欄に明記）
        counted = src
        no_url = sum(1 for s in src if not re.search(URL_RE, s))
        extra = f"・URLなし {no_url}件" if no_url else ""
    else:
        # 原稿: 「- 資料名（発行元・公表年）URL」。URL と4桁の年の両方がある行だけ数える
        counted = [s for s in src if re.search(URL_RE, s) and re.search(YEAR_RE, s)]
        skipped = len(src) - len(counted)
        extra = f"・URLか年がなく数えない行 {skipped}件" if skipped else ""
    pub = sum(1 for s in counted if is_public(s))
    add("参考資料（3件以上・公的機関を含む）", (3 if len(counted) >= 3 else len(counted)) + (2 if pub else 0), 5,
        f"{len(counted)}件（うち公的機関 {pub}件{extra}）")
    al, sl = d["article_links"], d["service_links"]
    add("本文から他の記事へのリンク（2本以上）", 2 if len(al) >= 2 else len(al), 2, f"{len(al)}本")
    add("関連サービスへのリンク（1本以上）", 2 if sl else 0, 2, ", ".join(sl) or "なし")

    text = d["body_text"]
    plain = md_plain(text)
    sents = [s.strip() for s in re.split(r"[。！？\n]", plain) if len(s.strip()) >= 5]
    avg = sum(map(len, sents)) / len(sents) if sents else 0
    long_ = sum(1 for s in sents if len(s) > 80)
    lr = long_ / len(sents) if sents else 0
    add("1文の平均（60字以下）", 2 if avg <= 60 else (1 if avg <= 70 else 0), 2, f"平均 {avg:.0f}字（{len(sents)}文）")
    add("80字を超える文（5%以下）", 2 if lr <= 0.05 else (1 if lr <= 0.10 else 0), 2, f"{long_}文（{lr*100:.0f}%）")

    # NG・表記ゆれの判定対象: 引用（> 行・<blockquote>）とかぎかっこ「」『』の中を除く
    check = md_plain(d.get("check_text", text))
    faq_plain = md_plain(d.get("faq_text", ""))
    full = remove_quotes("\n".join([title, d["description"], *d["keypoints"], check, *d["faq"], faq_plain]))
    severe = find_severe(full)
    minor = [m.group(0) for p in NG_MINOR for m in re.finditer(p, full)]
    add("NG表現（軽微）なし", 4 - 2 * len(minor), 4, "、".join(minor) or "なし")
    if severe:
        gates.append("重大なNG表現（誇大・保証・断定）: " + "、".join(severe))
    gloss = []
    for p, right in GLOSSARY:
        for m in re.finditer(p, remove_quotes(check + "\n" + "\n".join(d["keypoints"] + d["faq"]) + "\n" + faq_plain)):
            gloss.append(f"{m.group(0)}→{right}")
    add("表記ゆれなし（glossary）", 3 - len(gloss), 3, "、".join(gloss[:8]) or "なし")

    # 出典の付いていない数値（ゲートではなく品質管理部への注意喚起）
    nums = re.findall(r"[0-9０-９][0-9,，.．]*\s?(?:%|万|億|円|件|人|泊|室|日|か月|年)", plain)
    total = sum(i["得点"] for i in items)
    return {"機械採点": total, "機械満点": 40, "項目": items, "ゲート違反": gates,
            "数値の出現数": len(nums), "注意": "数値ごとの出典の確認は品質管理部（正確性・20点）が行う"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--keyword", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = Path(a.path)
    text = p.read_text(encoding="utf-8")
    d = parse_html(text) if p.suffix == ".html" else parse_md(text)
    if a.keyword:
        d["keyword"] = a.keyword
    if not d["keyword"]:
        brief = ROOT / "docs/seo/briefs" / f"{p.stem}.md"
        if brief.exists():
            m = re.search(r"(?m)^(?:[-*]\s*)?(?:\*\*)?(?:主キーワード|狙うキーワード|キーワード)(?:\*\*)?[:：]\s*(.+)$", brief.read_text(encoding="utf-8"))
            d["keyword"] = m.group(1).strip().strip("「」`") if m else ""
    if not d["keyword"]:  # キーワード表の「担当記事」から読む
        kw = ROOT / "docs/seo/keywords.md"
        if kw.exists():
            for line in kw.read_text(encoding="utf-8").splitlines():
                if f"media/{p.stem}.html" in line:
                    first = line.strip("|").split("|")[0]
                    d["keyword"] = re.split(r"[／（(]", first)[0].strip()
                    break
    r = score(d)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(f"# 機械採点: {r['機械採点']} / 40 点（{p}）\n")
        print("| 項目 | 得点 | 根拠 |\n|---|---|---|")
        for i in r["項目"]:
            print(f"| {i['項目']} | {i['得点']}/{i['満点']} | {i['根拠']} |")
        print(f"\nゲート違反: {'、'.join(r['ゲート違反']) or 'なし'}")
        print(f"数値の出現: {r['数値の出現数']} か所（すべて出典との照合が必要）")
    sys.exit(2 if r["ゲート違反"] else 0)


if __name__ == "__main__":
    main()
