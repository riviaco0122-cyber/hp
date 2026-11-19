"""Noki の sitemap を Search Console に送る（人の方針 2026-11-19: 編集長が人に聞かずに送ってよい）。

使い方:
  python3 tools/okaeri/submit_sitemap.py          # 送って、送ったあとの状態を出す
  python3 tools/okaeri/submit_sitemap.py --check  # 送らずに、いまの状態と権限だけ出す

- 環境変数 GOOGLE_SERVICE_ACCOUNT_JSON（JSON そのもの か base64）と GSC_SITE_URL を使う（tools/analytics.py と同じ）。
- 送信には、Search Console でサービスアカウントの権限が「フル」か「オーナー」である必要がある。
  「制限付き」だと 403 になるので、そのときは権限を上げてもらうよう人に伝える。
- Noki が本番に出る前に送ると、Google は 404 を記録するだけなので、本番の /noki/sitemap.xml が 200 を返すことを先に確かめる。
"""
import base64
import json
import os
import sys
import urllib.request
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "site.json"), encoding="utf-8"))
SITEMAP = CFG["origin"].rstrip("/") + CFG["prefix"].rstrip("/") + "/sitemap.xml"
API = "https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps"


def session():
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip().strip("'\"")
    if not raw:
        sys.exit("環境変数 GOOGLE_SERVICE_ACCOUNT_JSON が未設定です")
    if not raw.startswith("{"):
        raw = base64.b64decode(raw).decode("utf-8")
    creds = service_account.Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/webmasters"])
    return AuthorizedSession(creds)


def live():
    try:
        with urllib.request.urlopen(SITEMAP, timeout=20) as r:
            return r.status
    except Exception as e:  # 404 など
        return getattr(e, "code", str(e))


def main():
    site = os.environ.get("GSC_SITE_URL")
    if not site:
        sys.exit("環境変数 GSC_SITE_URL が未設定です")
    s = session()
    perm = [x["permissionLevel"] for x in s.get("https://www.googleapis.com/webmasters/v3/sites").json().get("siteEntry", []) if x["siteUrl"] == site]
    print(f"Search Console のプロパティ: 権限 {perm[0] if perm else '見つからない'}")
    status = live()
    print(f"{SITEMAP}: {status}")
    base = API.format(site=quote(site, safe=""))
    if "--check" not in sys.argv:
        if status != 200:
            sys.exit("本番の sitemap がまだ開けないので送らない（Noki の PR がマージされてから送る）")
        r = s.put(base + "/" + quote(SITEMAP, safe=""))
        if r.status_code == 403:
            sys.exit("送信を断られた（403）。Search Console の「設定 → ユーザーと権限」で、サービスアカウントの権限を「フル」にしてもらう")
        r.raise_for_status()
        print("送信しました")
    for x in s.get(base).json().get("sitemap", []):
        print(f"- {x.get('path')}  最後に送った日時 {x.get('lastSubmitted')}  エラー {x.get('errors')}  警告 {x.get('warnings')}")


if __name__ == "__main__":
    main()
