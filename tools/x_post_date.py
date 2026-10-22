#!/usr/bin/env python3
"""X（旧Twitter）の投稿 URL から投稿日（日本時間）を出す。ネットにはつながない。

投稿の ID には投稿時刻が埋め込まれている（Snowflake ID）。WebSearch で x.com に絞って
見つけた投稿は日付が分からないので、これで古い投稿を外す（.claude/skills/trend-research）。

使い方:
  python3 tools/x_post_date.py https://x.com/<アカウント>/status/<ID> [...] [--days 90]
  --days を付けると、その日数より古い投稿に「古い」と印を付ける。
"""
import argparse
import datetime as dt
import re

JST = dt.timezone(dt.timedelta(hours=9))
EPOCH_MS = 1288834974657  # X の Snowflake ID の起点


def post_date(url):
    m = re.search(r"/status(?:es)?/(\d+)", url)
    if not m:
        return None
    return dt.datetime.fromtimestamp(((int(m.group(1)) >> 22) + EPOCH_MS) / 1000, JST)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--days", type=int, default=0)
    a = ap.parse_args()
    now = dt.datetime.now(JST)
    for u in a.urls:
        d = post_date(u)
        if d is None:
            print(f"-          {u}（投稿の URL ではない）")
            continue
        old = " 古い" if a.days and (now - d).days > a.days else ""
        print(f"{d:%Y-%m-%d}{old} {u}")


if __name__ == "__main__":
    main()
