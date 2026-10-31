#!/usr/bin/env python3
"""順位の見張り（Search Console）と、書き直しの効果測定。

  python3 tools/rank_watch.py              あと一歩の検索語（順位8〜20位で表示がある）と、表示はあるのにクリックがないページを docs/seo/rank-watch.md に書く
  python3 tools/rank_watch.py baseline     書き直した記事の、書き直し前の数字（直近28日）を docs/seo/data/rewrite-baseline.json に保存する
  python3 tools/rank_watch.py compare      baseline のあとの28日と比べて、docs/seo/rewrite-effect.md に書く

要: tools/analytics.py と同じ環境変数（GOOGLE_SERVICE_ACCOUNT_JSON）。Search Console は2〜3日遅れで確定する。
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analytics as an  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "docs/seo/data/rewrite-baseline.json"
# 2026-10-30・31 に読みやすさを書き直した記事（効果測定の対象）。ページ名は /media/<slug>.html
REWRITTEN = """
akiya-inherited-house-to-inn akiya-demolish-or-renovate minpaku-shukyaku-first-steps kani-shukusho-kyoka-guide
minpaku-break-even kaishain-minpaku-fukugyo minpaku-chintai-start minpaku-seisou-kojin-kakunin minpaku-180days-rule
japan-tourism-market-data minpaku-vs-ryokan-law airdna-revenue-simulation small-inn-subsidies new-build-vs-used-house-inn
shizuoka-yaizu-akiya-inn case-rental-house-inn-first-year case-owner-pricing-mistake case-owner-diy-cottage
case-owner-subsidy-akiya case-owner-fishing-port case-owner-rental-side-business case-owner-licensed-akiya
minpaku-start-steps inn-kpi-basics long-stay-travel-demand minpaku-fire-safety ota-vs-direct-booking
kominka-renovation-points cleaning-linen-operations minpaku-management-company akiya-lease-types listing-photo-tips
inn-startup-funding guest-review-tips accommodation-tax akiya-3000man-deduction minpaku-investment-yield
why-akiya-utilization-now akiya-law-kanri-fuzen souzoku-touki-gimuka akiya-holding-costs akiya-utilization-options
inherited-house-family-talk why-minpaku-for-akiya minpaku-vs-rental-income akiya-minpaku-suitability
minpaku-hard-truth minpaku-neighbor-rules minpaku-off-season minpaku-remote-operation akiyado-what-we-do
akiyado-consultation-flow remote-renovation-tips long-stay-guest-equipment
""".split()


def period(days, end=None):
    end = end or (dt.date.today() - dt.timedelta(days=3))
    return (end - dt.timedelta(days=days - 1)).isoformat(), end.isoformat()


def page_slug(url):
    return url.rstrip("/").split("/")[-1].replace(".html", "")


def rank_watch(days):
    s = an.session()
    site = os.environ.get("GSC_SITE_URL", "https://rivia-co.com/")
    start, end = period(days)
    pq = an.gsc(s, site, start, end, ["page", "query"], 1000)
    pages = an.gsc(s, site, start, end, ["page"], 500)
    near = sorted([r for r in pq if 8 <= r["position"] <= 20 and r["impressions"] >= 3],
                  key=lambda r: -r["impressions"])
    no_click = sorted([r for r in pages if r["impressions"] >= 5 and r["clicks"] == 0],
                      key=lambda r: -r["impressions"])
    low_ctr = sorted([r for r in pq if r["position"] < 8 and r["impressions"] >= 5 and r["ctr"] < 0.03],
                     key=lambda r: -r["impressions"])
    out = [f"# 順位の見張り（{start}〜{end}）", "",
           "`python3 tools/rank_watch.py` で自動生成。毎週、上から順に、title・見出し・表・内部リンクの施策（PDCA）を1つ選ぶ。", "",
           "## あと一歩の検索語（順位8〜20位・表示3以上）：1ページ目に押し上げる候補", "",
           "| ページ | 検索語 | 順位 | 表示 | クリック |", "|---|---|---|---|---|"]
    out += [f"| {page_slug(r['page'])} | {r['query']} | {r['position']} | {r['impressions']} | {r['clicks']} |" for r in near[:30]] or ["| （なし） | | | | |"]
    out += ["", "## 順位は高いのにクリックされない検索語（順位8位より上・表示5以上・CTR3%未満）：title・description の見直し候補", "",
            "| ページ | 検索語 | 順位 | 表示 | CTR |", "|---|---|---|---|---|"]
    out += [f"| {page_slug(r['page'])} | {r['query']} | {r['position']} | {r['impressions']} | {r['ctr']:.1%} |" for r in low_ctr[:20]] or ["| （なし） | | | | |"]
    out += ["", "## 表示はあるのにクリックが0のページ（表示5以上）", "", "| ページ | 表示 | 平均順位 |", "|---|---|---|"]
    out += [f"| {page_slug(r['page'])} | {r['impressions']} | {r['position']} |" for r in no_click[:20]] or ["| （なし） | | |"]
    (ROOT / "docs/seo/rank-watch.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


def snapshot(days, end=None):
    s = an.session()
    site = os.environ.get("GSC_SITE_URL", "https://rivia-co.com/")
    start, end = period(days, end)
    rows = an.gsc(s, site, start, end, ["page"], 500)
    by = {page_slug(r["page"]): r for r in rows}
    data = {"start": start, "end": end, "days": days,
            "pages": {slug: {k: by[slug][k] for k in ("impressions", "clicks", "ctr", "position")} for slug in REWRITTEN if slug in by}}
    return data


def baseline(days):
    data = snapshot(days)
    data["taken"] = dt.date.today().isoformat()
    data["note"] = "書き直し（2026-10-30・31）より前の28日。比べるのは、書き直しが反映されたあとの28日"
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = lambda k: sum(v[k] for v in data["pages"].values())
    print(f"baseline 保存: {BASELINE}（{data['start']}〜{data['end']}、{len(data['pages'])}ページ。表示 {tot('impressions')}・クリック {tot('clicks')}）")


def compare(days):
    if not BASELINE.exists():
        sys.exit("先に python3 tools/rank_watch.py baseline を実行してください")
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    now = snapshot(days)
    rows = []
    for slug, b in base["pages"].items():
        n = now["pages"].get(slug, {"impressions": 0, "clicks": 0, "ctr": 0, "position": 0})
        rows.append((slug, b, n))
    tb = lambda k: sum(b[k] for _, b, _ in rows)
    tn = lambda k: sum(n[k] for _, _, n in rows)
    out = ["# 書き直しの効果測定", "",
           f"- 書き直し前: {base['start']}〜{base['end']}（{base['days']}日）／書き直し後: {now['start']}〜{now['end']}（{now['days']}日）",
           f"- 合計（対象 {len(rows)} ページ）: 表示 {tb('impressions')}→{tn('impressions')}、クリック {tb('clicks')}→{tn('clicks')}",
           "- 注意: 記事が増えた・公開から日が浅い・季節の影響があるので、合計の増減だけで効果とは言えない。ページごとの動きと、書き直していない記事との比較も見る。", "",
           "| ページ | 表示（前→後） | クリック（前→後） | 順位（前→後） |", "|---|---|---|---|"]
    for slug, b, n in sorted(rows, key=lambda x: -(x[2]["impressions"] - x[1]["impressions"])):
        out.append(f"| {slug} | {b['impressions']}→{n['impressions']} | {b['clicks']}→{n['clicks']} | {b['position']}→{n['position']} |")
    (ROOT / "docs/seo/rewrite-effect.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="watch", choices=["watch", "baseline", "compare"])
    ap.add_argument("--days", type=int, default=28)
    a = ap.parse_args()
    {"watch": rank_watch, "baseline": baseline, "compare": compare}[a.cmd](a.days)


if __name__ == "__main__":
    main()
