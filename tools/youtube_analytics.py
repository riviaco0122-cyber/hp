#!/usr/bin/env python3
"""アキヤドの YouTube チャンネルの数字を取る（YouTube Studio と同じ数字を API で取る）。週次の改善（PDCA）に使う。

取るもの（自分のチャンネルの動画ごと）:
  再生回数・総再生時間・平均視聴時間・平均再生率・登録者の増減・高評価・コメント数
  サムネイルの表示回数とクリック率（API が対応していれば。だめなら「Studio で確認」と出す）
  視聴者維持のグラフ（動画のどこで離れたか。--retention で、落ちこみの大きい場所を時間で出す）
  視聴の入口（検索・おすすめ・関連動画・外部 など）
収益（金額）は取らない・書かない（このリポジトリは公開されているため）。コメントの本文・投稿者名も保存しない。

準備（一度だけ。docs/seo/analytics-setup.md の 8 章）:
  環境変数 YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN（チャンネルの持ち主の Google アカウントで許可した OAuth）
使い方:
  python3 tools/youtube_analytics.py report [--days 28]        すべての動画の一覧と数字 → docs/youtube/reports/YYYY-MM-DD.md
  python3 tools/youtube_analytics.py retention <動画ID>          視聴者維持（どこで離れたか）を表示
  python3 tools/youtube_analytics.py check                       鍵と接続の確認だけ
"""
import datetime as dt, json, os, pathlib, sys, urllib.parse, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
JST = dt.timezone(dt.timedelta(hours=9))


def token():
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    miss = [k for k in need if not os.environ.get(k)]
    if miss:
        sys.exit(f"環境変数 {', '.join(miss)} が未設定です（docs/seo/analytics-setup.md の 8 章）")
    data = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data), timeout=30)
    except urllib.error.HTTPError as e:
        sys.exit(f"OAuth の更新に失敗しました（{e.code}）。リフレッシュトークンが失効していないか確認してください（8 章の「アプリを本番にする」）")
    return json.load(r)["access_token"]


TOK = None


def get(url, params):
    global TOK
    TOK = TOK or token()
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers={"Authorization": "Bearer " + TOK})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code}: {e.read().decode()[:300]}")


def videos():
    ch = get("https://www.googleapis.com/youtube/v3/channels", {"part": "contentDetails,snippet", "mine": "true"})["items"][0]
    up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while True:
        p = {"part": "contentDetails", "playlistId": up, "maxResults": 50}
        if page:
            p["pageToken"] = page
        r = get("https://www.googleapis.com/youtube/v3/playlistItems", p)
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        page = r.get("nextPageToken")
        if not page:
            break
    out = []
    for k in range(0, len(ids), 50):
        r = get("https://www.googleapis.com/youtube/v3/videos", {"part": "snippet,contentDetails,status", "id": ",".join(ids[k:k + 50])})
        for v in r["items"]:
            out.append({"id": v["id"], "title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"][:10],
                        "duration": v["contentDetails"]["duration"], "privacy": v["status"]["privacyStatus"]})
    return ch["snippet"]["title"], out


def report_rows(start, end, metrics, dims="video", filters=None, sort=None, maxr=200):
    p = {"ids": "channel==MINE", "startDate": start, "endDate": end, "metrics": metrics, "dimensions": dims, "maxResults": maxr}
    if filters:
        p["filters"] = filters
    if sort:
        p["sort"] = sort
    r = get("https://youtubeanalytics.googleapis.com/v2/reports", p)
    cols = [c["name"] for c in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in r.get("rows", [])]


def secs(iso):  # PT8M19S → 499
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def cmd_report(days):
    today = dt.datetime.now(JST).date()
    start, end = str(today - dt.timedelta(days=days)), str(today)
    title, vids = videos()
    base = {r["video"]: r for r in report_rows(start, end, "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments", sort="-views")}
    try:
        imp = {r["video"]: r for r in report_rows(start, end, "videoThumbnailImpressions,videoThumbnailImpressionsClickRate")}
    except RuntimeError:
        imp = None
    L = [f"# YouTube の数字（{title}）", "", f"- 期間: {start}〜{end}（日本時間、直近{days}日）", f"- 取得: {dt.datetime.now(JST):%Y-%m-%d %H:%M}（tools/youtube_analytics.py）",
         "- サムネイルの表示回数・クリック率: " + ("API で取得" if imp is not None else "API で取れないため、YouTube Studio の「アナリティクス → リーチ」で確認して手で書き足す"), "",
         "| 動画 | 公開日 | 長さ | 再生 | 平均視聴 | 平均再生率 | 表示回数 | クリック率 | 登録者 | 高評価 | コメント |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for v in sorted(vids, key=lambda x: x["published"], reverse=True):
        b, i = base.get(v["id"], {}), (imp or {}).get(v["id"], {})
        d = secs(v["duration"])
        L.append(f"| [{v['title']}](https://www.youtube.com/watch?v={v['id']}) | {v['published']} | {d // 60}:{d % 60:02d} | {b.get('views', 0)} | "
                 f"{int(b.get('averageViewDuration', 0)) // 60}:{int(b.get('averageViewDuration', 0)) % 60:02d} | {b.get('averageViewPercentage', 0):.1f}% | "
                 f"{i.get('videoThumbnailImpressions', '—')} | {(str(round(i['videoThumbnailImpressionsClickRate'] * (100 if i['videoThumbnailImpressionsClickRate'] < 1 else 1), 1)) + '%') if 'videoThumbnailImpressionsClickRate' in i else '—'} | "
                 f"{b.get('subscribersGained', 0) - b.get('subscribersLost', 0):+d} | {b.get('likes', 0)} | {b.get('comments', 0)} |")
    try:
        src = report_rows(start, end, "views,estimatedMinutesWatched", dims="insightTrafficSourceType", sort="-views")
        L += ["", "## 視聴の入口（チャンネル全体）", "", "| 入口 | 再生 | 再生時間（分） |", "|---|---|---|"]
        L += [f"| {r['insightTrafficSourceType']} | {r['views']} | {r['estimatedMinutesWatched']} |" for r in src]
    except RuntimeError as e:
        L += ["", f"（視聴の入口は取得できませんでした: {e}）"]
    out = ROOT / "docs" / "youtube" / "reports" / f"{today}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L)); print("\n保存:", out.relative_to(ROOT))


def cmd_retention(vid):
    today = dt.datetime.now(JST).date()
    _, vids = videos()
    v = next((x for x in vids if x["id"] == vid), None)
    if not v:
        sys.exit("自分のチャンネルの動画IDではありません")
    d = secs(v["duration"])
    rows = report_rows(v["published"], str(today), "audienceWatchRatio,relativeRetentionPerformance", dims="elapsedVideoTimeRatio", filters=f"video=={vid}")
    if not rows:
        sys.exit("視聴者維持のデータがまだありません（再生が少ないと出ません）")
    print(f"# 視聴者維持: {v['title']}（{d // 60}:{d % 60:02d}）\n")
    prev = None; drops = []
    for r in rows:
        x, w = r["elapsedVideoTimeRatio"], r["audienceWatchRatio"]
        t = int(x * d)
        print(f"{t // 60}:{t % 60:02d}  残っている割合 {w * 100:5.1f}%  同じ長さの動画とくらべて {r['relativeRetentionPerformance']:.2f}")
        if prev is not None:
            drops.append((prev - w, t))
        prev = w
    print("\n落ちこみの大きい場所（ここの台本・画面を見直す）:")
    for dw, t in sorted(drops, reverse=True)[:5]:
        print(f"  {t // 60}:{t % 60:02d} で {dw * 100:.1f} ポイント減")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(2)
    if a[0] == "check":
        t, v = videos(); print(f"接続できました: {t}（動画 {len(v)} 本）")
    elif a[0] == "report":
        cmd_report(int(a[a.index("--days") + 1]) if "--days" in a else 28)
    elif a[0] == "retention" and len(a) > 1:
        cmd_retention(a[1])
    else:
        print(__doc__); sys.exit(2)
