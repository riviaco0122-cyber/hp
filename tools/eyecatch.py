"""記事のアイキャッチ（記事トップの画像・OGP）を作る

各記事の短いキャッチコピー（articles の short）と写真（ARTICLE_PHOTOS）から、
1200×630 の画像を images/eyecatch/<slug>.jpg に書き出す。デザインは2種類を使い分ける。

  - 問いかけ型（キャッチに「？」がある記事）: 生成り色の地に文字が主役、写真は右に添える
  - 写真型（それ以外）: 写真を暗めにして、白い文字をのせる（2行目にマーカー）

使い方:
  python3 tools/eyecatch.py            # すべての記事
  python3 tools/eyecatch.py <slug> ... # 指定した記事だけ

必要なもの: Node.js と playwright（tools/check と同じ）、丸ゴシックの書体
（Zen Maru Gothic を端末に入れておくか、ネットにつながる環境で実行する）。
画像を作り直したら python3 tools/build.py を実行してページに反映する。
"""
import html
import importlib.util
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "images", "eyecatch")

MARK = ('<svg viewBox="0 0 32 32" width="40" height="40"><rect width="32" height="32" rx="9" fill="#2E6B47"/>'
        '<path d="M7.5 15.6 16 8.6l8.5 7v8.6a1.3 1.3 0 0 1-1.3 1.3h-4.7v-5.7h-5v5.7H8.8a1.3 1.3 0 0 1-1.3-1.3z" fill="#fff"/></svg>')

BASE_CSS = """
@import url("https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700&display=block");
*{box-sizing:border-box}
body{margin:0;width:1200px;height:630px;overflow:hidden;font-family:"Zen Maru Gothic",sans-serif;-webkit-font-smoothing:antialiased}
.kicker{display:inline-block;font-size:24px;font-weight:700;letter-spacing:.12em}
.logo{position:absolute;display:flex;align-items:center;gap:12px;font-size:25px;font-weight:700;letter-spacing:.14em}
.logo small{font-size:17px;font-weight:500;letter-spacing:.1em;opacity:.85}
"""

PHOTO_CSS = """
.w{position:relative;width:1200px;height:630px;background:#1b2a21 center/cover no-repeat}
.w::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(18,30,23,.84) 0%,rgba(18,30,23,.62) 50%,rgba(18,30,23,.12) 88%)}
.t{position:absolute;z-index:1;left:76px;right:120px;top:0;bottom:120px;display:flex;flex-direction:column;justify-content:center;color:#fff}
.kicker{align-self:flex-start;padding:7px 18px;border-radius:999px;background:#d0613b;color:#fff;font-size:22px}
h1{margin:26px 0 0;font-size:var(--fs);white-space:nowrap;line-height:1.38;font-weight:700;letter-spacing:.04em}
h1 em{font-style:normal;background:linear-gradient(transparent 64%,rgba(208,97,59,.9) 64%);padding:0 4px}
.logo{z-index:1;left:76px;bottom:54px;color:#fff}
"""

TYPE_CSS = """
.w{display:grid;grid-template-columns:minmax(0,1fr) 430px;width:1200px;height:630px;background:#f4f1ea}
.t{position:relative;display:flex;flex-direction:column;justify-content:center;padding:0 40px 90px 76px;color:#23302a}
.kicker{color:#2e6b47}
h1{margin:24px 0 0;font-size:var(--fs);white-space:nowrap;line-height:1.42;font-weight:700;letter-spacing:.03em}
h1 em{font-style:normal;color:#2e6b47}
.p{background:#cfd8d0 center/cover no-repeat;border-radius:0 0 0 140px}
.logo{left:76px;bottom:52px;color:#2e6b47}
"""


def load_build():
    """build.py を読み込む（記事データ・写真の対応・カテゴリ名を使う）。ページは書き出さない"""
    spec = importlib.util.spec_from_file_location("site_build", os.path.join(ROOT, "tools", "build.py"))
    mod = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    os.chdir(os.path.join(ROOT, "tools"))
    try:
        spec.loader.exec_module(mod)
    finally:
        os.chdir(cwd)
    return mod


def style_of(a):
    return "type" if "？" in a["short"] else "photo"


def headline(a, style):
    """キャッチを2行で組み、強調する行を決める（写真型は2行目、問いかけ型は「？」のある行）"""
    lines = [html.escape(l) for l in a["short"].split("\n")]
    if style == "photo":
        lines[-1] = f"<em>{lines[-1]}</em>"
    else:
        lines = [f"<em>{l}</em>" if "？" in l else l for l in lines]
    return "<br>".join(lines)


def font_size(a, style):
    """いちばん長い行が枠に収まる文字の大きさ（行の途中で折り返さない）"""
    longest = max(len(l) for l in a["short"].split("\n"))
    width, top = (990, 68) if style == "photo" else (650, 64)
    return min(top, int(width / (longest * 1.06)))


def page_html(a, b):
    style = style_of(a)
    name = b.ARTICLE_PHOTOS[a["slug"]][0]
    photo_url = "file://" + os.path.join(ROOT, "images", "photos", f"{name}.jpg")
    kicker = html.escape(b.MEDIA_CAT_NAMES[a["category"]])
    logo = f'<div class="logo">{MARK}アキヤド<small>空き家と民泊のメディア</small></div>'
    if style == "photo":
        body = (f'<div class="w" style="background-image:url(\'{photo_url}\')">'
                f'<div class="t"><span class="kicker">{kicker}</span><h1>{headline(a, style)}</h1></div>{logo}</div>')
        css = PHOTO_CSS
    else:
        body = (f'<div class="w"><div class="t"><span class="kicker">{kicker}</span><h1>{headline(a, style)}</h1>{logo}</div>'
                f'<div class="p" style="background-image:url(\'{photo_url}\')"></div></div>')
        css = TYPE_CSS
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{BASE_CSS}{css}</style></head>'
            f'<body style="--fs:{font_size(a, style)}px">{body}<img id="pre" src="{photo_url}" alt="" style="display:none"></body></html>')


RENDER_JS = """
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [src, out] of jobs) {
    await p.goto('file://' + src);
    await p.evaluate(async () => { await document.fonts.ready; await document.getElementById('pre').decode().catch(() => {}); });
    await p.waitForTimeout(150);
    await p.screenshot({ path: out, type: 'jpeg', quality: 86 });
  }
  await b.close();
})();
"""


def main(slugs):
    b = load_build()
    arts = [a for a in b.ARTICLES if not slugs or a["slug"] in slugs]
    os.makedirs(OUT_DIR, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        jobs = []
        for a in arts:
            src = os.path.join(tmp, a["slug"] + ".html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(page_html(a, b))
            jobs.append([src, os.path.join(OUT_DIR, a["slug"] + ".jpg")])
        js = os.path.join(tmp, "render.js")
        with open(js, "w") as f:
            f.write(RENDER_JS)
        import json
        env = dict(os.environ)
        node_paths = [os.path.join(ROOT, "tools", "check", "node_modules")]
        try:
            node_paths.append(subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
        except OSError:
            pass
        env["NODE_PATH"] = os.pathsep.join(p for p in node_paths + [env.get("NODE_PATH", "")] if p)
        subprocess.run(["node", js, json.dumps(jobs)], check=True, env=env)
    for a in arts:
        print(f"{style_of(a):5}  images/eyecatch/{a['slug']}.jpg")


if __name__ == "__main__":
    main(sys.argv[1:])
