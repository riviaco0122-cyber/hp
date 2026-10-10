#!/usr/bin/env python3
"""GA4 と Google Search Console から直近のデータを取得し、レポートを作る（企画・マーケ部が使う）。

必要な環境変数（クラウド環境の Secret に登録する）:
  GOOGLE_SERVICE_ACCOUNT_JSON  サービスアカウントの鍵（JSONの中身をそのまま）
  GA4_PROPERTY_ID              GA4 のプロパティID（省略時 556922741）
  GSC_SITE_URL                 Search Console のプロパティ（省略時 https://rivia-co.com/）

使い方:
  pip install -r tools/requirements.txt
  python3 tools/analytics.py              # docs/seo/data/ と docs/seo/reports/ に保存
  python3 tools/analytics.py --days 28    # 集計期間（既定 28 日。前の同じ期間と比較）

出力:
  docs/seo/data/YYYY-MM-DD.json     生データ（次回以降の比較用）
  docs/seo/reports/YYYY-MM-DD.md    人とAIが読む要約（伸びしろのあるキーワード・記事）
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://rivia-co.com"
SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]


def session():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("google-auth が未インストールです: pip install -r tools/requirements.txt")
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        sys.exit("環境変数 GOOGLE_SERVICE_ACCOUNT_JSON が未設定です（docs/seo/analytics-setup.md を参照）")
    raw = raw.strip().strip("'\"") if not raw.strip().startswith("{") else raw.strip()
    if not raw.startswith("{"):  # base64 で登録された場合
        import base64
        raw = base64.b64decode(raw).decode("utf-8")
    creds = service_account.Credentials.from_service_account_info(json.loads(raw), scopes=SCOPES)
    return AuthorizedSession(creds)


def gsc(s, site, start, end, dims, limit=250):
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{quote(site, safe='')}/searchAnalytics/query"
    r = s.post(url, json={"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": limit})
    if r.status_code != 200:
        raise RuntimeError(f"Search Console API エラー {r.status_code}: {r.text[:300]}")
    return [
        {**{d: k for d, k in zip(dims, row["keys"])},
         "clicks": row["clicks"], "impressions": row["impressions"],
         "ctr": round(row["ctr"], 4), "position": round(row["position"], 1)}
        for row in r.json().get("rows", [])
    ]


def ga4(s, prop, start, end):
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport"
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [{"name": n} for n in ("screenPageViews", "sessions", "engagementRate",
                                           "averageSessionDuration", "keyEvents")],
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
        "limit": 200,
    }
    r = s.post(url, json=body)
    if r.status_code != 200:
        raise RuntimeError(f"GA4 API エラー {r.status_code}: {r.text[:300]}")
    names = [m["name"] for m in r.json().get("metricHeaders", [])]
    rows = []
    for row in r.json().get("rows", []):
        vals = [float(v["value"]) for v in row["metricValues"]]
        rows.append({"page": row["dimensionValues"][0]["value"], **dict(zip(names, vals))})
    return rows


def ga4_channels(s, prop, start, end):
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport"
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}],
        "metrics": [{"name": "sessions"}, {"name": "keyEvents"}],
    }
    r = s.post(url, json=body)
    if r.status_code != 200:
        raise RuntimeError(f"GA4 API エラー {r.status_code}: {r.text[:300]}")
    return [{"channel": row["dimensionValues"][0]["value"],
             "sessions": float(row["metricValues"][0]["value"]),
             "keyEvents": float(row["metricValues"][1]["value"])}
            for row in r.json().get("rows", [])]


def short(url):
    return url.replace(SITE, "") or "/"


def build_report(d):
    L = [f"# 集客レポート {d['generated']}", "",
         f"期間: {d['period']['start']} 〜 {d['period']['end']}（前期間 {d['prev_period']['start']} 〜 {d['prev_period']['end']}）", ""]

    def tot(rows, k):
        return sum(r[k] for r in rows)

    if d.get("gsc"):
        cur, prev = d["gsc"]["pages"], d["gsc"]["pages_prev"]
        L += ["## 検索（Search Console）", "",
              f"- クリック {tot(cur, 'clicks'):.0f}（前期間 {tot(prev, 'clicks'):.0f}）",
              f"- 表示回数 {tot(cur, 'impressions'):.0f}（前期間 {tot(prev, 'impressions'):.0f}）", ""]
        opp = [q for q in d["gsc"]["queries"] if 4 < q["position"] <= 20 and q["impressions"] >= 20]
        opp.sort(key=lambda q: -q["impressions"])
        L += ["### 伸びしろのあるキーワード（順位5〜20位・表示20回以上）", "",
              "| キーワード | 表示 | クリック | 順位 |", "|---|---|---|---|"]
        L += [f"| {q['query']} | {q['impressions']:.0f} | {q['clicks']:.0f} | {q['position']} |" for q in opp[:20]] or ["| （該当なし） | | | |"]
        low = [p for p in cur if p["impressions"] >= 100 and p["ctr"] < 0.01]
        L += ["", "### 表示はされるがクリックされない記事（表示100回以上・CTR1%未満 → タイトル/説明文の改善候補）", ""]
        L += [f"- `{short(p['page'])}` 表示{p['impressions']:.0f} CTR{p['ctr']*100:.1f}% 順位{p['position']}" for p in low[:15]] or ["- （該当なし）"]
        L += [""]
    if d.get("ga4"):
        L += ["## サイト内の行動（GA4）", "", "| ページ | 表示回数 | エンゲージ率 | キーイベント |", "|---|---|---|---|"]
        L += [f"| `{r['page']}` | {r['screenPageViews']:.0f} | {r['engagementRate']*100:.0f}% | {r['keyEvents']:.0f} |" for r in d["ga4"]["pages"][:20]]
        L += ["", "### 流入チャネル", ""]
        L += [f"- {c['channel']}: セッション {c['sessions']:.0f} ／ キーイベント {c['keyEvents']:.0f}" for c in d["ga4"]["channels"]]
        L += [""]
    for e in d.get("errors", []):
        L += [f"> ⚠️ {e}", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28)
    a = ap.parse_args()
    today = dt.date.today()
    end = today - dt.timedelta(days=3)  # Search Console は 2〜3 日遅れで確定する
    start = end - dt.timedelta(days=a.days - 1)
    pend = start - dt.timedelta(days=1)
    pstart = pend - dt.timedelta(days=a.days - 1)
    f = lambda x: x.isoformat()

    s = session()
    data = {"generated": f(today), "period": {"start": f(start), "end": f(end)},
            "prev_period": {"start": f(pstart), "end": f(pend)}, "errors": []}
    site = os.environ.get("GSC_SITE_URL", "https://rivia-co.com/")
    try:
        data["gsc"] = {
            "pages": gsc(s, site, f(start), f(end), ["page"]),
            "pages_prev": gsc(s, site, f(pstart), f(pend), ["page"]),
            "queries": gsc(s, site, f(start), f(end), ["query"], 500),
            "page_queries": gsc(s, site, f(start), f(end), ["page", "query"], 1000),
        }
    except RuntimeError as e:
        data["errors"].append(str(e))
    prop = os.environ.get("GA4_PROPERTY_ID", "556922741")
    if prop:
        try:
            data["ga4"] = {"pages": ga4(s, prop, f(start), f(end)),
                           "channels": ga4_channels(s, prop, f(start), f(end))}
        except RuntimeError as e:
            data["errors"].append(str(e))
    else:
        data["errors"].append("GA4_PROPERTY_ID が未設定のため GA4 は取得していません")

    for sub in ("data", "reports"):
        (ROOT / "docs" / "seo" / sub).mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/seo/data" / f"{f(today)}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    report = build_report(data)
    (ROOT / "docs/seo/reports" / f"{f(today)}.md").write_text(report, encoding="utf-8")
    print(report)
    if data["errors"] and not (data.get("gsc") or data.get("ga4")):
        sys.exit(1)


if __name__ == "__main__":
    main()
