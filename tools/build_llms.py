#!/usr/bin/env python3
"""seo/llms.txt（AI検索向けのサイト案内）を、pages/ の HTML から作り直す。

使い方:
  python3 tools/build_llms.py              # seo/llms.txt を書き出す
  python3 tools/build_llms.py --dry-run    # 書き出さずに、変わるかどうかと掲載記事数だけ表示
  python3 tools/build_llms.py --stdout     # 生成結果を標準出力に表示（ファイルは変えない）
  python3 tools/build_llms.py --today 2026-11-01   # 判定日を指定（テスト用。既定は日本時間の今日）

仕様:
  - 形式は llmstxt.org（# サイト名 → > 要約 → ## セクションごとのリンク一覧と1行説明）。
  - 説明文は各ページの meta description をそのまま使う（事実を足さない）。
  - 記事は pages/media.html の #media-list に載っている記事のうち、
    公開日（data-publish）が今日（日本時間）以前のものだけを、新しい順に載せる。
    公開日前の記事は載せない（予約公開の記事を AI に先に知らせないため）。
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
SITE = "https://rivia-co.com"
TITLE_SUFFIX = " | 合同会社RIVIA&CO."

# 並びと見出しは固定（ページを増やしたらここに足す）
COMPANY_PAGES = [
    ("index.html", "トップページ"),
    ("about.html", None),
    ("contact.html", None),
]
SERVICE_PAGES = [  # ヘッダーのサービスメニュー・sitemap と同じ順
    "service-operation.html",
    "service-management.html",
    "service-partnership.html",
    "service-marketing.html",
    "service-recruit.html",
]
OPTIONAL_PAGES = ["careers.html", "privacy.html"]


def today_jst() -> str:
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def page_meta(path: Path):
    """(title, description) を返す。title はサフィックスを除き、実体参照を戻す"""
    s = _read(path)
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = html.unescape(m.group(1).strip()) if m else path.stem
    if title.endswith(TITLE_SUFFIX):
        title = title[: -len(TITLE_SUFFIX)]
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = html.unescape(m.group(1).strip()) if m else ""
    return title, desc


def public_url(rel: str) -> str:
    if rel == "index.html":
        return SITE + "/"
    return f"{SITE}/{rel}"


def registered_articles():
    """media.html の #media-list に載っている記事の (slug, date) を、載っている順（新しい順）で返す"""
    s = _read(PAGES / "media.html")
    return re.findall(
        r'<a href="media/([\w-]+)\.html" class="media-card[^"]*" data-category="\w+" data-date="([\d-]+)"', s
    )


def article_info(slug: str):
    s = _read(PAGES / "media" / f"{slug}.html")
    title, desc = page_meta(PAGES / "media" / f"{slug}.html")
    m = re.search(r'data-publish="([\d-]+)"', s)
    pub = m.group(1) if m else ""
    m = re.search(r'class="tag article__cat">([^<]+)</a>', s)
    cat = html.unescape(m.group(1).strip()) if m else ""
    return title, desc, pub, cat


def link_line(title: str, url: str, desc: str) -> str:
    title = title.replace("[", "［").replace("]", "］")
    return f"- [{title}]({url}): {desc}" if desc else f"- [{title}]({url})"


def build(today: str):
    """(llms.txt の本文, 掲載した記事の slug のリスト) を返す"""
    _, index_desc = page_meta(PAGES / "index.html")
    _, media_desc = page_meta(PAGES / "media.html")
    lines = [
        "# 合同会社RIVIA&CO.",
        "",
        f"> {index_desc}",
        "",
        "このサイトには、会社とサービスの案内と、オウンドメディア「暮らす旅の手帖」があります。"
        f"「暮らす旅の手帖」は、{media_desc}",
        "記事には公開日・更新日・参考資料を記載しています。数値や制度は公開日時点の情報です。",
        "",
        "## 会社情報",
        "",
    ]
    for rel, label in COMPANY_PAGES:
        title, desc = page_meta(PAGES / rel)
        lines.append(link_line(label or title, public_url(rel), desc))
    lines += ["", "## サービス", ""]
    for rel in SERVICE_PAGES:
        title, desc = page_meta(PAGES / rel)
        lines.append(link_line(title, public_url(rel), desc))
    lines += ["", "## 暮らす旅の手帖（記事）", ""]
    title, desc = page_meta(PAGES / "media.html")
    lines.append(link_line(title, public_url("media.html"), desc))
    included = []
    for slug, card_date in registered_articles():
        path = PAGES / "media" / f"{slug}.html"
        if not path.is_file():
            continue
        title, desc, pub, cat = article_info(slug)
        pub = pub or card_date
        if not pub or pub > today:
            continue  # 公開日前の記事は載せない
        extra = f"（カテゴリ: {cat}／公開日: {pub}）" if cat else f"（公開日: {pub}）"
        lines.append(link_line(title, f"{SITE}/media/{slug}.html", desc + extra))
        included.append(slug)
    lines += ["", "## Optional", ""]
    for rel in OPTIONAL_PAGES:
        title, desc = page_meta(PAGES / rel)
        lines.append(link_line(title, public_url(rel), desc))
    return "\n".join(lines) + "\n", included


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
