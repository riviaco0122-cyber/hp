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
  docs/seo/reports/YYYY-MM-DD.md    人とAIが読む要約（伸びしろのあるキーワード・記事、
                                    相談につながったページ、AI検索からの流入、記事からサービスへの移動）

ほかのツールから使う関数（tools/pdca.py が使う）:
  fetch_page_metrics(page_path, start, end, s=None)  任意期間・任意ページ（None でサイト全体）の指標を1つの dict で返す
  is_ai_source(text)                                  参照元が AI 検索かどうか

計測の前提と、GA4 Data API で取れないため近い指標にしたもの:
  - 相談（generate_lead）は thanks.html で送っている（form_type: contact / careers / akiyado）。
    そのため「ページ別の generate_lead」は thanks.html にしか付かない。どのページが相談につながったかは
    「そのページを入口（landingPage）にしたセッションのうち、generate_lead が起きたセッション数」で見る。
    件数は eventName='generate_lead' の eventCount／sessions で数える（GA4 で generate_lead を
    キーイベントに設定するまで keyEvents は 0 になりうるため。keyEvents も参考に並べる）。
  - 相談ボタンのクリック（cta_click。js/main.js が contact.html へのリンクのクリックで送る）は
    pagePath 別の eventCount（＝相談の手前の指標）。
  - form_type・cta_position の内訳は、人が GA4 でカスタムディメンションに登録するまで Data API で
    取れない。取れないときはエラーにせず「未登録」と出す。
  - 記事 → サービスページの移動: runReport には「順番つきの遷移」を数える機能がない（ファネルは v1alpha の
    別 API）。代わりに「記事（/media/ 配下の記事）を入口にしたセッションのうち、service-*.html または
    contact.html の page_view を含むセッション数」（landingPage × pagePath の正規表現フィルタでの sessions）
    を使う。入口が記事なので、サービスページの閲覧は記事より後と見なせる。
  - AI 検索からの流入: sessionSource または pageReferrer が AI_SOURCE_PATTERN に一致するセッション。
    ChatGPT などは参照元を送らないことがあり、その分は「direct」に入るので実際より少なく出る（下限の値）。
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


# ---------------------------------------------------------------------------
# 拡張（ページ別の詳細・相談・AI検索・記事→サービス・日別）
# ---------------------------------------------------------------------------
GA4_URL = "https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport"
LEAD_EVENT = "generate_lead"
CTA_EVENT = "cta_click"
# AI 検索とみなす参照元（sessionSource / pageReferrer に部分一致。GA4 の PARTIAL_REGEXP にもそのまま使う）
AI_SOURCES = [
    r"chatgpt\.com", r"chat\.openai\.com", r"openai\.com", r"perplexity\.ai", r"perplexity",
    r"gemini\.google\.com", r"bard\.google\.com", r"copilot\.microsoft\.com", r"bing\.com/chat",
    r"claude\.ai", r"(^|[/.])you\.com", r"phind", r"poe\.com", r"felo\.ai", r"genspark",
    r"chat\.deepseek\.com", r"meta\.ai",
]
AI_SOURCE_PATTERN = "|".join(AI_SOURCES)
SERVICE_PATH_PATTERN = r"^/(service-[^/]*\.html|contact\.html)$"
ARTICLE_LANDING_PATTERN = r"^/media/(?!guide-|category-|search\.html)[^/]+\.html$"
ARTICLE_LANDING_RE2 = r"^/media/[^/]+\.html$"  # GA4 は RE2（先読みなし）。ガイド・カテゴリは後で除く
UNREGISTERED = "未登録"


def is_ai_source(text):
    """参照元（sessionSource・pageReferrer など）が AI 検索なら True。"""
    import re
    return bool(text) and re.search(AI_SOURCE_PATTERN, str(text).lower()) is not None


def is_article_path(path):
    import re
    return re.match(ARTICLE_LANDING_PATTERN, path or "") is not None


def _sf(field, value, match="EXACT"):
    """GA4 の文字列フィルタ（match: EXACT / BEGINS_WITH / PARTIAL_REGEXP / FULL_REGEXP）"""
    return {"filter": {"fieldName": field, "stringFilter": {"matchType": match, "value": value}}}


def _and(*exprs):
    exprs = [e for e in exprs if e]
    if not exprs:
        return None
    return exprs[0] if len(exprs) == 1 else {"andGroup": {"expressions": list(exprs)}}


def _or(*exprs):
    return {"orGroup": {"expressions": list(exprs)}}


def ai_filter():
    return _or(_sf("sessionSource", AI_SOURCE_PATTERN, "PARTIAL_REGEXP"),
               _sf("pageReferrer", AI_SOURCE_PATTERN, "PARTIAL_REGEXP"))


def page_filter(field, page_path):
    """page_path が None ならフィルタなし（サイト全体）。末尾が / なら前方一致（例: /media/）、それ以外は完全一致。"""
    if not page_path:
        return None
    if page_path.endswith("/") and page_path != "/":
        return _sf(field, page_path, "BEGINS_WITH")
    return _sf(field, page_path)


def ga4_run(s, prop, start, end, dims, metrics, flt=None, limit=1000, order=None):
    """GA4 runReport の汎用版。行を {次元名: 値, 指標名: 数値} の dict で返す。"""
    body = {"dateRanges": [{"startDate": start, "endDate": end}],
            "metrics": [{"name": m} for m in metrics], "limit": limit}
    if dims:
        body["dimensions"] = [{"name": d} for d in dims]
    if flt:
        body["dimensionFilter"] = flt
    if order:
        body["orderBys"] = [{"metric": {"metricName": order}, "desc": True}]
    r = s.post(GA4_URL.format(prop=prop), json=body)
    if r.status_code != 200:
        raise RuntimeError(f"GA4 API エラー {r.status_code}: {r.text[:300]}")
    js = r.json()
    dn = [h["name"] for h in js.get("dimensionHeaders", [])] or list(dims or [])
    mn = [h["name"] for h in js.get("metricHeaders", [])] or list(metrics)
    out = []
    for row in js.get("rows", []):
        d = {k: v["value"] for k, v in zip(dn, row.get("dimensionValues", []))}
        d.update({k: float(v["value"]) for k, v in zip(mn, row.get("metricValues", []))})
        out.append(d)
    return out


def _total(rows, metric):
    return sum(r.get(metric, 0.0) for r in rows)


def _merge(base, extra, key, fields):
    idx = {r[key]: r for r in extra}
    for r in base:
        e = idx.get(r[key], {})
        for src, dst in fields.items():
            r[dst] = e.get(src, 0.0)
    return base


def ga4_pages_detail(s, prop, start, end):
    """ページ別: 表示回数・セッション・エンゲージメント率・平均エンゲージメント時間（秒）・
    generate_lead の件数（eventCount と keyEvents）・相談ボタンのクリック（cta_click）。"""
    rows = ga4_run(s, prop, start, end, ["pagePath"],
                   ["screenPageViews", "sessions", "engagementRate", "userEngagementDuration",
                    "activeUsers", "keyEvents"], order="screenPageViews", limit=500)
    for r in rows:
        r["page"] = r.pop("pagePath")
        r["avgEngagementTime"] = round(r["userEngagementDuration"] / r["activeUsers"], 1) if r.get("activeUsers") else 0.0
    ev = ga4_run(s, prop, start, end, ["pagePath", "eventName"], ["eventCount"],
                 _or(_sf("eventName", LEAD_EVENT), _sf("eventName", CTA_EVENT)), limit=1000)
    for r in rows:
        r["leadEvents"] = _total([e for e in ev if e["pagePath"] == r["page"] and e["eventName"] == LEAD_EVENT], "eventCount")
        r["ctaClicks"] = _total([e for e in ev if e["pagePath"] == r["page"] and e["eventName"] == CTA_EVENT], "eventCount")
    return rows


def ga4_landing(s, prop, start, end):
    """入口ページ別: セッション・エンゲージメント率と、その中で generate_lead に至ったセッション数・件数。"""
    rows = ga4_run(s, prop, start, end, ["landingPage"], ["sessions", "engagementRate", "keyEvents"],
                   order="sessions", limit=500)
    lead = ga4_run(s, prop, start, end, ["landingPage"], ["sessions", "eventCount"],
                   _sf("eventName", LEAD_EVENT), limit=500)
    _merge(rows, lead, "landingPage", {"sessions": "leadSessions", "eventCount": "leadEvents"})
    for r in rows:
        r["page"] = r.pop("landingPage")
    return rows


def ga4_article_to_service(s, prop, start, end):
    """記事を入口にしたセッションのうち、service-*.html か contact.html も見たセッション数（近い代替指標。
    モジュール冒頭の説明を参照）。"""
    land = ga4_run(s, prop, start, end, ["landingPage"], ["sessions"],
                   _sf("landingPage", ARTICLE_LANDING_RE2, "FULL_REGEXP"), limit=500)
    moved = ga4_run(s, prop, start, end, ["landingPage"], ["sessions"],
                    _and(_sf("landingPage", ARTICLE_LANDING_RE2, "FULL_REGEXP"),
                         _sf("pagePath", SERVICE_PATH_PATTERN, "FULL_REGEXP")), limit=500)
    _merge(land, moved, "landingPage", {"sessions": "serviceSessions"})
    out = []
    for r in land:
        if not is_article_path(r["landingPage"]):
            continue
        out.append({"page": r["landingPage"], "sessions": r["sessions"], "serviceSessions": r["serviceSessions"]})
    out.sort(key=lambda r: (-r["serviceSessions"], -r["sessions"]))
    return out


def ga4_ai(s, prop, start, end):
    """AI 検索からの流入（参照元別・入口ページ別）。"""
    by_src = ga4_run(s, prop, start, end, ["sessionSource", "landingPage"],
                     ["sessions", "engagedSessions", "keyEvents"], ai_filter(), limit=500)
    by_ref = ga4_run(s, prop, start, end, ["pageReferrer", "pagePath"], ["screenPageViews"],
                     _sf("pageReferrer", AI_SOURCE_PATTERN, "PARTIAL_REGEXP"), limit=500)
    return {"sessions": by_src, "referrers": by_ref}


def ga4_custom_breakdown(s, prop, start, end, event, param):
    """カスタムディメンション（form_type・cta_position）の内訳。未登録なら UNREGISTERED を返す。"""
    try:
        rows = ga4_run(s, prop, start, end, [f"customEvent:{param}"], ["eventCount"],
                       _sf("eventName", event), limit=50)
    except RuntimeError:
        return UNREGISTERED
    return [{"value": r.get(f"customEvent:{param}", ""), "eventCount": r["eventCount"]} for r in rows]


def gsc_daily(s, site, start, end):
    """Search Console の日別の推移（クリック・表示回数・CTR・平均順位）"""
    return gsc(s, site, start, end, ["date"], 500)


def _gsc_page_filter(page_path):
    if not page_path:
        return None
    if page_path.endswith("/") and page_path != "/":
        return {"dimension": "page", "operator": "includingRegex",
                "expression": "^" + SITE.replace(".", r"\.") + page_path.replace(".", r"\.")}
    return {"dimension": "page", "operator": "equals", "expression": SITE + page_path}


def gsc_total(s, site, start, end, page_path=None):
    """期間の合計（page_path を指定するとそのページだけ）。"""
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{quote(site, safe='')}/searchAnalytics/query"
    body = {"startDate": start, "endDate": end, "rowLimit": 1}
    f = _gsc_page_filter(page_path)
    if f:
        body["dimensionFilterGroups"] = [{"filters": [f]}]
    r = s.post(url, json=body)
    if r.status_code != 200:
        raise RuntimeError(f"Search Console API エラー {r.status_code}: {r.text[:300]}")
    rows = r.json().get("rows", [])
    if not rows:
        return {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": 0.0}
    row = rows[0]
    return {"clicks": float(row["clicks"]), "impressions": float(row["impressions"]),
            "ctr": float(row["ctr"]), "position": float(row["position"])}


# fetch_page_metrics が返す指標（pdca.py の台帳で使う名前）
METRIC_KEYS = ("impressions", "clicks", "ctr", "position",            # Search Console
               "views", "sessions", "engagement_rate", "avg_engagement_time",
               "landing_sessions", "leads", "lead_events", "key_events", "cta_clicks",
               "service_sessions", "ai_sessions", "lead_rate", "service_rate")


def fetch_page_metrics(page_path, start, end, s=None, prop=None, site=None):
    """任意期間（start〜end、YYYY-MM-DD、両端を含む）の指標を返す。

    page_path: "/media/xxx.html" のような公開URLのパス。末尾が "/" なら前方一致（例 "/media/"）。
               None ならサイト全体。
    返り値（すべて float）:
      impressions, clicks, ctr, position   Search Console（ctr は 0〜1、position は小さいほど上位）
      views, sessions, engagement_rate, avg_engagement_time   そのページを含むセッション基準（秒）
      landing_sessions   そのページを入口にしたセッション
      leads              入口セッションのうち generate_lead に至ったセッション（サイト全体なら全セッション基準）
      lead_events        同じく generate_lead の件数（eventCount）
      key_events         keyEvents（GA4 でキーイベント設定前は 0 になりうる）
      cta_clicks         そのページでの相談ボタンのクリック（cta_click の eventCount）
      service_sessions   入口セッションのうち service-*.html / contact.html も見たセッション
      ai_sessions        入口セッションのうち AI 検索から来たセッション
      lead_rate, service_rate   leads / landing_sessions、service_sessions / landing_sessions
    """
    s = s or session()
    prop = prop or os.environ.get("GA4_PROPERTY_ID", "556922741")
    site = site or os.environ.get("GSC_SITE_URL", "https://rivia-co.com/")
    out = {k: 0.0 for k in METRIC_KEYS}
    out.update(gsc_total(s, site, start, end, page_path))

    def one(metrics, flt):
        rows = ga4_run(s, prop, start, end, [], metrics, flt, limit=1)
        return rows[0] if rows else {m: 0.0 for m in metrics}

    pf, lf = page_filter("pagePath", page_path), page_filter("landingPage", page_path)
    a = one(["screenPageViews", "sessions", "engagementRate", "userEngagementDuration", "activeUsers", "keyEvents"], pf)
    out.update(views=a["screenPageViews"], sessions=a["sessions"], engagement_rate=a["engagementRate"],
               key_events=a["keyEvents"],
               avg_engagement_time=round(a["userEngagementDuration"] / a["activeUsers"], 1) if a["activeUsers"] else 0.0)
    out["landing_sessions"] = one(["sessions"], lf)["sessions"] if page_path else a["sessions"]
    b = one(["sessions", "eventCount"], _and(lf, _sf("eventName", LEAD_EVENT)))
    out.update(leads=b["sessions"], lead_events=b["eventCount"])
    out["cta_clicks"] = one(["eventCount"], _and(pf, _sf("eventName", CTA_EVENT)))["eventCount"]
    out["service_sessions"] = one(["sessions"], _and(lf, _sf("pagePath", SERVICE_PATH_PATTERN, "FULL_REGEXP")))["sessions"]
    out["ai_sessions"] = one(["sessions"], _and(lf, ai_filter()))["sessions"]
    ls = out["landing_sessions"]
    out["lead_rate"] = out["leads"] / ls if ls else 0.0
    out["service_rate"] = out["service_sessions"] / ls if ls else 0.0
    return out


def build_extra_report(d):
    """拡張の3節（相談につながったページ／AI検索からの流入／記事からサービスへの移動）。"""
    g = d.get("ga4") or {}
    L = []
    if "landing" in g:
        rows = [r for r in g["landing"] if r.get("leadSessions", 0) > 0]
        rows.sort(key=lambda r: -r["leadSessions"])
        total = sum(r.get("leadEvents", 0) for r in g["landing"])
        L += ["## 相談につながったページ（入口ページ別・generate_lead）", "",
              f"- 期間内の相談（generate_lead）: {total:.0f} 件（eventCount で集計。キーイベント設定前でも数える）"]
        ft = g.get("form_type")
        if ft == UNREGISTERED or ft is None:
            L += [f"- form_type の内訳: {UNREGISTERED}（GA4 でカスタムディメンションに登録すると表示）"]
        else:
            L += ["- form_type の内訳: " + ("、".join(f"{x['value'] or '(空)'} {x['eventCount']:.0f}" for x in ft) or "なし")]
        L += ["", "| 入口ページ | 入口セッション | 相談に至ったセッション | 相談率 |", "|---|---|---|---|"]
        L += [f"| `{r['page']}` | {r['sessions']:.0f} | {r['leadSessions']:.0f} | "
              f"{(r['leadSessions'] / r['sessions'] * 100 if r['sessions'] else 0):.1f}% |" for r in rows[:20]] \
            or ["| （該当なし） | | | |"]
        cta = sorted([r for r in g.get("pages_detail", []) if r.get("ctaClicks", 0) > 0], key=lambda r: -r["ctaClicks"])
        L += ["", "### 相談ボタンのクリック（cta_click・ページ別。相談の手前の指標）", ""]
        cp = g.get("cta_position")
        L += [f"- cta_position の内訳: {UNREGISTERED}（GA4 でカスタムディメンションに登録すると表示）"
              if cp == UNREGISTERED or cp is None else
              "- cta_position の内訳: " + ("、".join(f"{x['value'] or '(空)'} {x['eventCount']:.0f}" for x in cp) or "なし")]
        L += [f"- `{r['page']}` クリック {r['ctaClicks']:.0f}（表示 {r['screenPageViews']:.0f}）" for r in cta[:15]] or ["- （該当なし）"]
        L += [""]
    if "ai" in g:
        rows = g["ai"]["sessions"]
        by_src, by_page = {}, {}
        for r in rows:
            by_src[r["sessionSource"]] = by_src.get(r["sessionSource"], 0) + r["sessions"]
            by_page[r["landingPage"]] = by_page.get(r["landingPage"], 0) + r["sessions"]
        L += ["## AI検索からの流入", "",
              f"- セッション {_total(rows, 'sessions'):.0f}（ChatGPT などは参照元を送らないことがあり、実際より少なく出る）"]
        L += [f"- {k}: {v:.0f}" for k, v in sorted(by_src.items(), key=lambda x: -x[1])] or []
        L += ["", "| 入口ページ | AI検索からのセッション |", "|---|---|"]
        L += [f"| `{k}` | {v:.0f} |" for k, v in sorted(by_page.items(), key=lambda x: -x[1])[:20]] or ["| （該当なし） | |"]
        L += [""]
    if "article_to_service" in g:
        rows = g["article_to_service"]
        ts, tm = _total(rows, "sessions"), _total(rows, "serviceSessions")
        L += ["## 記事からサービスへの移動", "",
              f"- 記事を入口にしたセッション {ts:.0f} のうち、サービスページ・お問い合わせも見たセッション {tm:.0f}"
              f"（{(tm / ts * 100 if ts else 0):.1f}%）",
              "- 集計方法: 入口が記事で、同じセッションに service-*.html / contact.html の表示があるもの（順番つきの遷移ではない近い指標）",
              "", "| 記事（入口） | 入口セッション | サービス・問い合わせも見た | 割合 |", "|---|---|---|---|"]
        L += [f"| `{r['page']}` | {r['sessions']:.0f} | {r['serviceSessions']:.0f} | "
              f"{(r['serviceSessions'] / r['sessions'] * 100 if r['sessions'] else 0):.1f}% |" for r in rows[:20]] \
            or ["| （該当なし） | | | |"]
        L += [""]
    return L


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
    L += build_extra_report(d)
    for e in d.get("errors", []):
        L += [f"> ⚠️ {e}", ""]
    return "\n".join(L)


def collect_extra(s, data, site, prop, start, end):
    """拡張分の取得。1つが失敗しても他と既存の出力は残す。"""
    if data.get("gsc") is not None:
        try:
            data["gsc"]["daily"] = gsc_daily(s, site, start, end)
        except RuntimeError as e:
            data["errors"].append(str(e))
    if prop and data.get("ga4") is not None:
        g = data["ga4"]
        for key, fn in (("pages_detail", ga4_pages_detail), ("landing", ga4_landing),
                        ("article_to_service", ga4_article_to_service), ("ai", ga4_ai)):
            try:
                g[key] = fn(s, prop, start, end)
            except RuntimeError as e:
                data["errors"].append(str(e))
        g["form_type"] = ga4_custom_breakdown(s, prop, start, end, LEAD_EVENT, "form_type")
        g["cta_position"] = ga4_custom_breakdown(s, prop, start, end, CTA_EVENT, "cta_position")


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
    collect_extra(s, data, site, prop, f(start), f(end))

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
