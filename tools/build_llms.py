#!/usr/bin/env python3
"""seo/llms.txt（AI検索向けのサイト案内）を、pages/ の HTML から作り直す。

使い方:
  python3 tools/build_llms.py              # seo/llms.txt を書き出す
  python3 tools/build_llms.py --dry-run    # 書き出さずに、変わるかどうかと掲載記事数だけ表示
  python3 tools/build_llms.py --stdout     # 生成結果を標準出力に表示（ファイルは変えない）
  python3 tools/build_llms.py --today 2026-11-01   # 判定日を指定（テスト用。既定は日本時間の今日）

仕様（本番ブランチで作られた seo/llms.txt を正として、その形を再現する）:
  - 形式は llmstxt.org（# サイト名 → > 要約 → ## セクションごとのリンク一覧）。
  - 冒頭の要約と「会社」の説明文は、本番ブランチの llms.txt の文言をそのまま定数にしている（下の SUMMARY・COMPANY_PAGES）。
    文言を変えるときはここを直す（事実を足さない）。
  - 「サービス」: 各サービスページの title（「 | 合同会社RIVIA&CO.」を除く）。説明文は付けない。
  - 「アキヤド（ガイド）」: ガイド3ページの title（「｜アキヤド」を除く）と meta description。順は sell → use → side。
  - 「アキヤド（記事）」: pages/media.html の「すべての記事」(#media-list) に載っている記事のうち、
    公開日（data-publish）が今日（日本時間）以前のものだけを、公開日の古い順（同じ日は seo/sitemap.xml の順）に載せる。
    記事名は title（「 | アキヤド」を除く）、説明は meta description。公開日前の記事は載せない（予約公開の記事を AI に先に知らせないため）。
  - 英語版（/en/）・メディアのトップ・カテゴリ一覧・検索・トップページ・採用・プライバシーは載せない（本番ブランチの llms.txt と同じ）。
  - 毎回すべて作り直すので、何度実行しても同じ結果になる。日次の定期実行で毎日実行すれば、
    公開日を迎えた記事が自動で加わる。tools/add_article.py も追加・削除の最後にこれを呼ぶ。
  - 公開URLは vercel.json の rewrites で /llms.txt → /seo/llms.txt。

外部ライブラリは使わない（標準ライブラリのみ）。
"""
import argparse
import datetime
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
OUT = ROOT / "seo" / "llms.txt"
SITEMAP = ROOT / "seo" / "sitemap.xml"
SITE = "https://rivia-co.com"
TITLE_SUFFIXES = (" | 合同会社RIVIA&CO.", " | アキヤド", "｜アキヤド")

SITE_NAME = "合同会社RIVIA&CO."
SUMMARY = ("空き家の再生、民泊・小さな宿の開業と運営、WEB集客・採用を支援する会社です。"
           "運営メディア「アキヤド（空き家と民泊のメディア）」では、空き家を売りたい方・活かしたい方・"
           "副業で民泊をはじめたい方に向けて、悩みの順に記事を公開しています。")
# 並びと見出し・説明は固定（ページを増やしたらここに足す）
COMPANY_PAGES = [
    ("about.html", "会社概要", "ミッション・ビジョン・バリューと創業者"),
    ("contact.html", "お問い合わせ", "無料相談の窓口"),
]
SERVICE_PAGES = [  # ヘッダーのサービスメニュー・sitemap と同じ順
    "service-operation.html",
    "service-management.html",
    "service-partnership.html",
    "service-marketing.html",
    "service-recruit.html",
]
GUIDE_PAGES = ["media/guide-sell.html", "media/guide-use.html", "media/guide-side.html"]


def today_jst() -> str:
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def page_meta(path: Path):
    """(title, description) を返す。title はサイト名の末尾を除き、実体参照を戻す"""
    s = _read(path)
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = html.unescape(m.group(1).strip()) if m else path.stem
    for suf in TITLE_SUFFIXES:
        if title.endswith(suf):
            title = title[: -len(suf)]
            break
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = html.unescape(m.group(1).strip()) if m else ""
    return title, desc


def public_url(rel: str) -> str:
    if rel == "index.html":
        return SITE + "/"
    return f"{SITE}/{rel}"


def registered_articles():
    """media.html の「すべての記事」(#media-list) に載っている記事の (slug, date) を、載っている順で返す"""
    s = _read(PAGES / "media.html")
    i = s.find('id="media-list"')
    if i >= 0:
        s = s[i: s.find("</section>", i)]
    return re.findall(
        r'<a href="media/([\w-]+)\.html" class="media-card[^"]*" data-category="\w+" data-date="([\d-]+)"', s
    )


def sitemap_order():
    s = _read(SITEMAP) if SITEMAP.is_file() else ""
    slugs = re.findall(r"<loc>" + re.escape(SITE) + r"/media/([\w-]+)\.html</loc>", s)
    return {x: i for i, x in enumerate(slugs)}


def article_info(slug: str):
    path = PAGES / "media" / f"{slug}.html"
    title, desc = page_meta(path)
    m = re.search(r'data-publish="([\d-]+)"', _read(path))
    return title, desc, (m.group(1) if m else "")


def link_line(title: str, url: str, desc: str = "") -> str:
    title = title.replace("[", "［").replace("]", "］")
    return f"- [{title}]({url}): {desc}" if desc else f"- [{title}]({url})"


def build(today: str):
    """(llms.txt の本文, 掲載した記事の slug のリスト) を返す"""
    lines = [f"# {SITE_NAME}", "", f"> {SUMMARY}", "", "## 会社"]
    for rel, label, desc in COMPANY_PAGES:
        lines.append(link_line(label, public_url(rel), desc))
    lines += ["", "## サービス"]
    for rel in SERVICE_PAGES:
        title, _ = page_meta(PAGES / rel)
        lines.append(link_line(title, public_url(rel)))
    lines += ["", "## アキヤド（ガイド）"]
    for rel in GUIDE_PAGES:
        title, desc = page_meta(PAGES / rel)
        lines.append(link_line(title, public_url(rel), desc))
    lines += ["", "## アキヤド（記事）"]
    rank = sitemap_order()
    rows = []
    for slug, card_date in registered_articles():
        if not (PAGES / "media" / f"{slug}.html").is_file():
            continue
        title, desc, pub = article_info(slug)
        pub = pub or card_date
        if not pub or pub > today:
            continue  # 公開日前の記事は載せない
        rows.append((pub, rank.get(slug, 10 ** 6), slug, title, desc))
    rows.sort()
    for pub, _, slug, title, desc in rows:
        lines.append(link_line(title, f"{SITE}/media/{slug}.html", desc))
    return "\n".join(lines) + "\n", [r[2] for r in rows]


def write(today: str = None, dry_run: bool = False, quiet: bool = False):
    """llms.txt を作り直す。変わったら True"""
    today = today or today_jst()
    text, included = build(today)
    old = OUT.read_text(encoding="utf-8") if OUT.is_file() else None
    changed = old != text
    if not quiet:
        state = "変更あり" if changed else "変更なし"
        verb = "（dry-run・書き込みなし）" if dry_run else ""
        print(f"seo/llms.txt: {state}{verb} ／ 掲載記事 {len(included)} 本（{today} 時点で公開日を迎えたもの）")
    if changed and not dry_run:
        OUT.write_text(text, encoding="utf-8")
    return changed


def main():
    ap = argparse.ArgumentParser(description="seo/llms.txt を pages/ から作り直す")
    ap.add_argument("--dry-run", action="store_true", help="書き込まずに結果だけ表示")
    ap.add_argument("--stdout", action="store_true", help="生成結果を標準出力に出す（書き込まない）")
    ap.add_argument("--today", help="判定日 YYYY-MM-DD（既定は日本時間の今日）")
    args = ap.parse_args()
    if args.today and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.today):
        sys.exit("--today は YYYY-MM-DD で指定してください")
    if args.stdout:
        sys.stdout.write(build(args.today or today_jst())[0])
        return
    write(args.today, args.dry_run)


if __name__ == "__main__":
    main()
