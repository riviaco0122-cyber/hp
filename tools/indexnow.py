#!/usr/bin/env python3
"""IndexNow で、新しい・直したページの URL を検索エンジン（Bing・Yandex・Naver など）に知らせる。

ChatGPT の検索や Microsoft Copilot は Bing の索引を使うので、Bing に早く取りに来てもらうと、
AI 検索に載るまでが早くなる（playbook 12-4）。Google は IndexNow に対応していない（Search Console で送る）。

使い方:
  python3 tools/indexnow.py diff <基準のコミット> [--wait] [--dry-run]
      基準のコミットの seo/sitemap.xml と今の sitemap.xml を比べ、増えた URL・lastmod が変わった URL・
      消えた URL（301 や削除を知らせる）を送る。GitHub Actions（.github/workflows/indexnow.yml）が
      本番ブランチへの反映のたびに実行する。
  python3 tools/indexnow.py urls <URL...> [--dry-run]   指定した URL だけ送る
  python3 tools/indexnow.py all [--dry-run]             sitemap の全 URL を送る（初回だけ）

鍵: リポジトリ直下の <32桁の16進>.txt（中身も同じ文字列）。IndexNow の鍵は、サイトに置いて
  公開するのが仕様（https://www.indexnow.org/documentation）で、秘密の値ではない。
  --wait は、送る前に鍵のファイルと新しいページが本番で開ける（200）まで待つ（Vercel の反映待ち。最大10分）。
"""
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://rivia-co.com"
HOST = "rivia-co.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP = "seo/sitemap.xml"
URL_RE = re.compile(r"<loc>([^<]+)</loc>(?:<lastmod>([^<]+)</lastmod>)?")


def key():
    files = [p for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem)]
    if len(files) != 1:
        sys.exit(f"鍵のファイル（直下の <32桁の16進>.txt）が1つではありません: {[p.name for p in files]}")
    return files[0].stem


def parse(text):
    return {u: m or "" for u, m in URL_RE.findall(text)}


def sitemap_at(ref):
    r = subprocess.run(["git", "show", f"{ref}:{SITEMAP}"], cwd=ROOT, capture_output=True, text=True)
    return parse(r.stdout) if r.returncode == 0 else {}


def changed(base):
    old, new = sitemap_at(base), parse((ROOT / SITEMAP).read_text(encoding="utf-8"))
    upd = [u for u, m in new.items() if u not in old or old[u] != m]
    gone = [u for u in old if u not in new]
    return upd, gone


def status(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "akiyado-indexnow"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def wait_live(urls, k, limit=600):
    targets = [f"{SITE}/{k}.txt"] + urls
    end = time.time() + limit
    while True:
        bad = [u for u in targets if status(u) != 200]
        if not bad:
            return
        if time.time() > end:
            print(f"本番で開けないまま10分たちました（先に進みます）: {bad[:5]}")
            return
        time.sleep(30)


def submit(urls, k, dry):
    urls = sorted(set(u for u in urls if u.startswith(SITE)))
    if not urls:
        print("送る URL はありません")
        return
    print(f"送る URL {len(urls)} 件:")
    for u in urls:
        print("  " + u)
    if dry:
        print("（--dry-run なので送っていません）")
        return
    body = json.dumps({"host": HOST, "key": k, "keyLocation": f"{SITE}/{k}.txt",
                       "urlList": urls[:10000]}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: {r.status}（200・202 は受け付け）")
    except urllib.error.HTTPError as e:
        sys.exit(f"IndexNow: {e.code} {e.read()[:300]!r}（403 は鍵のファイルが本番で開けない、422 はホスト違い）")


def main(argv):
    dry, wait = "--dry-run" in argv, "--wait" in argv
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    k, cmd = key(), args[0]
    if cmd == "diff" and len(args) == 2:
        upd, gone = changed(args[1])
        if wait and not dry and (upd or gone):
            wait_live(upd, k)
        submit(upd + gone, k, dry)
    elif cmd == "urls" and len(args) > 1:
        submit(args[1:], k, dry)
    elif cmd == "all":
        submit(list(parse((ROOT / SITEMAP).read_text(encoding="utf-8"))), k, dry)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
