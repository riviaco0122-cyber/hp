#!/usr/bin/env python3
"""YouTube から記事ネタ・一次情報の手がかりを集める（リサーチ部が使う）。無料の YouTube Data API を使う。

※ このリポジトリは公開されている。コメント本文・個人名・概要欄の全文はファイルに保存しない。
  読者の悩みは、リサーチ部が自分の言葉で要約してリサーチメモに書く。

必要な環境変数:
  YOUTUBE_API_KEY   Google Cloud で発行した API キー（docs/seo/analytics-setup.md の 6 章）

使い方:
  python3 tools/youtube_research.py "民泊 開業 失敗" [--days 180] [--max 10] [--comments 20]

出力:
  ファイル docs/sources/youtube/YYYY-MM-DD_<キーワード>.md
    動画ごとのタイトル・チャンネル名・URL・公開日・再生数などの数値と、概要欄の冒頭（約100字）だけ。
  標準出力（ファイルには残らない）
    人気コメント（--comments 件）。一時的な分析用。読み終えたら、悩みの傾向を自分の言葉で要約して
    リサーチメモに書く。コメントの原文・投稿者名は転記しない。
  ※ 字幕（文字起こし）は API の制約で他人の動画からは取得できない。必要なら人が要約を
    docs/sources/inbox/ に置く。

1日の無料枠は 10,000 ユニット。検索1回=100、動画情報・コメント取得=各1 なので、
1回の実行（検索1＋動画10本）でおよそ 120 ユニット。
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://www.googleapis.com/youtube/v3/"


def call(endpoint, **params):
    params["key"] = os.environ["YOUTUBE_API_KEY"]
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        if endpoint == "commentThreads":  # コメント無効の動画などは飛ばす
            return {"items": []}
        sys.exit(f"YouTube API エラー {e.code}: {body}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--days", type=int, default=365, help="この日数以内に公開された動画に限る")
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--comments", type=int, default=20)
    a = ap.parse_args()
    if not os.environ.get("YOUTUBE_API_KEY"):
        sys.exit("環境変数 YOUTUBE_API_KEY が未設定です（docs/seo/analytics-setup.md の 6 章）")

    after = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    found = call("search", part="snippet", q=a.query, type="video", maxResults=a.max,
                 order="relevance", relevanceLanguage="ja", regionCode="JP", publishedAfter=after)
    ids = [i["id"]["videoId"] for i in found.get("items", [])]
    if not ids:
        sys.exit("該当する動画がありません")
    videos = call("videos", part="snippet,statistics,contentDetails", id=",".join(ids))["items"]

    today = dt.date.today().isoformat()
    L = [f"# YouTube 調査: {a.query}", "",
         f"取得日 {today} ／ 公開 {a.days} 日以内 ／ {len(videos)} 本", "",
         "> 注記: このリポジトリは公開されている。コメント本文・個人名・概要欄の全文を保存しない。",
         "> 読者の悩みは、リサーチ部が自分の言葉で要約してリサーチメモに書く。",
         "> 引用ルール: 動画の内容は要約して使い、発信者（チャンネル名）と動画URLを出典として明記する。"
         "他人の体験を RIVIA の体験として書かない。", ""]
    comment_out = []  # 標準出力にだけ出す（ファイルには保存しない）
    for v in videos:
        s, st = v["snippet"], v.get("statistics", {})
        vid = v["id"]
        desc = re.sub(r"\s+", " ", s.get("description", "")).strip()
        head = (desc[:100] + "…") if len(desc) > 100 else desc
        L += [f"## {s['title']}", "",
              f"- URL: https://www.youtube.com/watch?v={vid}",
              f"- チャンネル: {s['channelTitle']}（https://www.youtube.com/channel/{s['channelId']}）",
              f"- 公開日: {s['publishedAt'][:10]} ／ 再生 {int(st.get('viewCount', 0)):,} ／ 高評価 {int(st.get('likeCount', 0)):,} ／ コメント {int(st.get('commentCount', 0)):,}",
              f"- 概要欄の冒頭（約100字・全文は保存しない）: {head or '（なし）'}", ""]
        if a.comments:
            cm = call("commentThreads", part="snippet", videoId=vid, order="relevance",
                      maxResults=min(a.comments, 100), textFormat="plainText")
            rows = [c["snippet"]["topLevelComment"]["snippet"] for c in cm.get("items", [])]
            if rows:
                comment_out += [f"\n## {s['title']}（https://www.youtube.com/watch?v={vid}）"]
                comment_out += [f"- （高評価 {r.get('likeCount', 0)}）" + r["textDisplay"].replace("\n", " ")[:300] for r in rows]

    if comment_out:
        print("=" * 60)
        print("人気コメント（一時的な分析用。ファイルには保存していない。原文・投稿者名を転記せず、")
        print("悩みの傾向を自分の言葉で要約してリサーチメモに書くこと）")
        print("=" * 60)
        print("\n".join(comment_out))
        print("=" * 60)

    out_dir = ROOT / "docs" / "sources" / "youtube"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[\\/:*?\"<>|\s]+", "_", a.query)[:40]
    out = out_dir / f"{today}_{slug}.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"saved {out.relative_to(ROOT)}（{len(videos)} 本）")


if __name__ == "__main__":
    main()
