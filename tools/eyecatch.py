"""記事のアイキャッチ（記事トップの画像・OGP）を作る

各記事の短いキャッチコピー（articles の short）と写真（ARTICLE_PHOTOS）から、
1200×630 の画像を images/eyecatch/<slug>.jpg に書き出す。デザインは2種類を使い分ける。

  - 問いかけ型（キャッチに「？」がある記事）: 生成り色の地に文字が主役、写真は右に添える
  - 写真型（それ以外）: 写真を暗めにして、白い文字をのせる（2行目にマーカー）

使い方:
  python3 tools/eyecatch.py            # すべての記事
  python3 tools/eyecatch.py <slug> ... # 指定した記事だけ

必要なもの: Node.js と playwright（tools/check と同じ）、丸ゴシックの書体
（Zen Maru Gothic・Zen Kaku Gothic New・Dela Gothic One・Shippori Mincho B1。
Google Fonts から読み込むので、ネットにつながる環境で実行する）。
画像を作り直したら python3 tools/build.py を実行してページに反映する。
"""
import html
import importlib.util
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eyecatch_designs import DESIGNS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "images", "eyecatch")

MARK = ('<svg viewBox="0 0 32 32" width="40" height="40"><rect width="32" height="32" rx="9" fill="#2E6B47"/>'
        '<path d="M7.5 15.6 16 8.6l8.5 7v8.6a1.3 1.3 0 0 1-1.3 1.3h-4.7v-5.7h-5v5.7H8.8a1.3 1.3 0 0 1-1.3-1.3z" fill="#fff"/></svg>')

BASE_CSS = """
@import url("https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&family=Zen+Kaku+Gothic+New:wght@400;700;900&family=Dela+Gothic+One&family=Shippori+Mincho+B1:wght@800&display=block");
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



COLORS = dict(green="#2e6b47", deep="#1f3a2b", terra="#c95a35", sand="#f4f1ea", navy="#22364a", mustard="#d7a23f", ink="#1d211f")
DARK_TEXT = {"sand", "mustard"}

# 組み方ごとの CSS。.fit の付いた要素は、枠からはみ出さないよう文字を自動で小さくする
LAYOUT_CSS = {
    "boxes": """
.w{position:relative;width:1200px;height:630px;background:#222 var(--pos)/cover no-repeat}
.w::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.45),rgba(0,0,0,.05) 60%)}
.t{position:absolute;z-index:1;right:56px;bottom:64px;left:300px;display:flex;flex-direction:column;align-items:flex-end;gap:10px}
.t .ln{display:inline-block;padding:4px 18px 8px;background:#fff;color:#1d211f;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:64px;line-height:1.15;white-space:nowrap;max-width:100%}
.t .ln em{font-style:normal;color:#c95a35}
.kicker{position:absolute;z-index:1;left:56px;top:48px;padding:6px 16px;background:#c95a35;color:#fff;font-size:20px}
.logo{z-index:1;left:56px;bottom:56px;color:#fff}""",
    "giant": """
.w{position:relative;width:1200px;height:630px;background:#222 var(--pos)/cover no-repeat}
.w::after{content:"";position:absolute;inset:0;background:rgba(14,22,17,.62)}
.t{position:absolute;z-index:1;left:64px;right:64px;top:0;bottom:70px;display:flex;flex-direction:column;justify-content:center;color:#fff}
.big{font-family:"Dela Gothic One";font-size:190px;line-height:1.05;letter-spacing:.02em;white-space:nowrap}
.h{margin-top:18px;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:50px;line-height:1.35;white-space:nowrap}
.h em{font-style:normal;color:#f0b35a}
.sub{margin-top:14px;font-size:24px;opacity:.85}
.kicker{position:absolute;z-index:1;left:64px;top:46px;color:#f0b35a;font-size:22px}
.logo{z-index:1;right:56px;bottom:46px;color:#fff}""",
    "number": """
.w{display:grid;grid-template-columns:560px 1fr;width:1200px;height:630px;background:var(--bg);color:var(--fg)}
.n{position:relative;display:flex;flex-direction:column;justify-content:center;padding:0 0 40px 64px}
.big{font-family:"Dela Gothic One";font-size:250px;line-height:.95;white-space:nowrap;letter-spacing:-.02em}
.big small{font-family:"Dela Gothic One";font-size:64px;margin-left:10px;letter-spacing:0}
.h{margin-top:30px;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:40px;line-height:1.4;white-space:nowrap}
.h em{font-style:normal;background:linear-gradient(transparent 60%,rgba(255,255,255,.28) 60%)}
.p{background:#888 var(--pos)/cover no-repeat;clip-path:polygon(14% 0,100% 0,100% 100%,0 100%)}
.kicker{position:absolute;left:64px;top:46px;font-size:22px;opacity:.9}
.logo{left:64px;bottom:44px;color:var(--fg)}""",
    "poster": """
.w{position:relative;width:1200px;height:630px;background:var(--bg);color:var(--fg);overflow:hidden}
.w::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(-55deg,rgba(255,255,255,.06) 0 26px,transparent 26px 64px)}
.p{position:absolute;right:-40px;top:70px;width:480px;height:480px;border-radius:50%;background:#888 var(--pos)/cover no-repeat;box-shadow:0 0 0 14px rgba(255,255,255,.18)}
.t{position:absolute;left:64px;right:470px;top:0;bottom:60px;display:flex;flex-direction:column;justify-content:center}
.big{font-family:"Dela Gothic One";font-size:150px;line-height:1.08;white-space:nowrap}
.h{margin-top:20px;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:46px;line-height:1.35;white-space:nowrap}
.h em{font-style:normal;display:inline-block;padding:0 12px 4px;background:var(--fg);color:var(--bg)}
.kicker{position:absolute;left:64px;top:46px;font-size:22px}
.logo{left:64px;bottom:44px;color:var(--fg)}""",
    "mincho": """
.w{position:relative;width:1200px;height:630px;background:#222 var(--pos)/cover no-repeat}
.w::after{content:"";position:absolute;inset:0;background:linear-gradient(270deg,rgba(10,14,12,.8) 0%,rgba(10,14,12,.5) 45%,rgba(10,14,12,0) 78%),linear-gradient(0deg,rgba(10,14,12,.55),rgba(10,14,12,0) 30%)}
.t{position:absolute;z-index:1;right:72px;left:420px;top:0;bottom:40px;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;text-align:right;color:#fff}
.v{font-family:"Shippori Mincho B1";font-weight:800;font-size:84px;line-height:1.3;letter-spacing:.08em;white-space:nowrap;max-width:100%}
.sub{margin-top:22px;padding-top:18px;border-top:1px solid rgba(255,255,255,.6);font-family:"Shippori Mincho B1";font-weight:800;font-size:28px;letter-spacing:.14em;white-space:nowrap}
.kicker{position:absolute;z-index:1;left:56px;top:46px;color:#fff;font-size:20px;opacity:.9}
.logo{z-index:1;left:56px;bottom:46px;color:#fff}""",
    "frame": """
.w{position:relative;width:1200px;height:630px;background:var(--bg);padding:34px}
.p{position:absolute;inset:34px 34px 190px 34px;border-radius:6px;background:#888 var(--pos)/cover no-repeat}
.t{position:absolute;left:64px;right:64px;bottom:44px;height:150px;display:flex;flex-direction:column;justify-content:center;color:var(--fg)}
.h{font-family:"Zen Kaku Gothic New";font-weight:900;font-size:56px;line-height:1.25;white-space:nowrap}
.h em{font-style:normal;text-decoration:underline;text-decoration-thickness:6px;text-underline-offset:10px}
.kicker{position:absolute;left:58px;top:58px;z-index:1;padding:6px 16px;background:var(--bg);color:var(--fg);font-size:20px}
.logo{right:64px;bottom:62px;color:var(--fg)}""",
    "quote": """
.w{position:relative;width:1200px;height:630px;background:#f4f1ea;color:#1d211f;display:grid;grid-template-columns:1fr 360px}
.t{position:relative;display:flex;flex-direction:column;justify-content:center;padding:0 40px 50px 110px}
.t::before{content:"“";position:absolute;left:40px;top:40px;font-family:"Shippori Mincho B1";font-size:260px;line-height:1;color:#c95a35;opacity:.9}
.h{font-family:"Zen Kaku Gothic New";font-weight:900;font-size:76px;line-height:1.3;white-space:nowrap}
.h em{font-style:normal;color:#c95a35}
.p{margin:40px 40px 40px 0;border-radius:200px 200px 16px 16px;background:#888 var(--pos)/cover no-repeat}
.kicker{position:absolute;left:110px;top:56px;color:#2e6b47;font-size:22px}
.logo{left:110px;bottom:46px;color:#2e6b47}""",
    "duo": """
.w{position:relative;width:1200px;height:630px;display:grid;grid-template-columns:1fr 1fr;color:#fff}
.half{position:relative;display:flex;align-items:center;justify-content:center;background:#555 var(--pos)/cover no-repeat}
.half::after{content:"";position:absolute;inset:0}
.half.l::after{background:rgba(31,58,43,.78)}.half.r::after{background:rgba(201,90,53,.80)}
.half b{position:relative;z-index:1;display:block;max-width:calc(100% - 110px);text-align:center;overflow:hidden;font-family:"Dela Gothic One";font-weight:400;font-size:112px;white-space:nowrap}
.half.l b{margin-right:40px}.half.r b{margin-left:40px}
.vs{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);z-index:2;width:120px;height:120px;border-radius:50%;background:#fff;color:#1d211f;display:grid;place-items:center;font-family:"Dela Gothic One";font-size:50px}
.t{position:absolute;z-index:2;left:0;right:0;bottom:92px;text-align:center}
.h{display:inline-block;padding:8px 28px 12px;background:#fff;color:#1d211f;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:46px;white-space:nowrap}
.h em{font-style:normal;color:#c95a35}
.kicker{position:absolute;z-index:2;left:48px;top:40px;font-size:20px}
.logo{z-index:2;left:50%;transform:translateX(-50%);bottom:28px;color:#fff}""",
    "case": """
.w{position:relative;width:1200px;height:630px;background:#f4f1ea;color:#1d211f;overflow:hidden}
.w::before{content:"";position:absolute;right:-200px;top:-150px;width:760px;height:900px;border-radius:50%;background:#1f3a2b}
.w::after{content:"";position:absolute;right:64px;top:110px;width:400px;height:400px;border-radius:50%;background:#2e6b47}
.av{position:absolute;z-index:2;right:104px;top:150px;width:320px;height:320px;border-radius:50%;background:#fff center/cover no-repeat;box-shadow:0 0 0 14px #c95a35,0 18px 40px rgba(0,0,0,.25)}
.who{position:absolute;z-index:3;right:160px;top:456px;padding:8px 26px 10px;border-radius:999px;background:#c95a35;color:#fff;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:30px;letter-spacing:.06em;white-space:nowrap}
.tag{position:absolute;z-index:2;left:64px;top:48px;padding:7px 20px 9px;background:#c95a35;color:#fff;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:24px;letter-spacing:.1em}
.t{position:absolute;z-index:2;left:64px;top:128px;width:560px}
.h{font-family:"Zen Kaku Gothic New";font-weight:900;font-size:54px;line-height:1.3;white-space:nowrap}
.h em{font-style:normal;color:#c95a35}
.chips{position:absolute;z-index:2;left:64px;bottom:112px;display:flex;gap:14px}
.chip{padding:10px 16px 12px;background:#fff;border-radius:14px;border:2px solid #1f3a2b;min-width:150px}
.chip small{display:block;font-size:19px;color:#555;letter-spacing:.04em}
.chip b{display:block;margin-top:2px;font-family:"Zen Kaku Gothic New";font-weight:900;font-size:30px;color:#1f3a2b;white-space:nowrap}
.logo{z-index:3;left:64px;bottom:40px;color:#1f3a2b}
.kicker{display:none}
.avs{position:absolute;z-index:2;right:96px;top:120px;width:360px;display:grid;grid-template-columns:repeat(3,108px);gap:18px}
.avs i{display:block;width:108px;height:108px;border-radius:50%;background:#fff center/cover no-repeat;box-shadow:0 0 0 6px #c95a35}""",
    "marker": PHOTO_CSS.replace("--fs", "--fs0") + "\n.h{font-size:66px;white-space:nowrap;line-height:1.38;font-weight:700;margin-top:26px}\n.h em{font-style:normal;background:linear-gradient(transparent 64%,rgba(208,97,59,.9) 64%);padding:0 4px}\n.sub{margin-top:18px;font-size:26px;opacity:.9}",
    "type": TYPE_CSS.replace("--fs", "--fs0") + "\n.h{font-size:64px;white-space:nowrap;line-height:1.42;font-weight:700;margin-top:24px}\n.h em{font-style:normal;color:#2e6b47}",
}



def mark_up(text):
    """[ ] で囲んだ部分を強調にする"""
    return html.escape(text).replace("[", "<em>").replace("]", "</em>")


def design_html(a, b, d):
    layout = d["layout"]
    name = d.get("photo") or b.ARTICLE_PHOTOS[a["slug"]][0]
    photo_url = "file://" + os.path.join(ROOT, "images", "photos", f"{name}.jpg")
    color = d.get("color", "deep")
    bg, fg = COLORS[color], ("#1d211f" if color in DARK_TEXT else "#fff")
    kicker = html.escape(b.MEDIA_CAT_NAMES[a["category"]])
    logo_color = "" if layout not in ("quote",) else ""
    logo = f'<div class="logo">{MARK}アキヤド<small>空き家と民泊のメディア</small></div>{logo_color}'
    lines = d.get("lines", [])
    h = "<br>".join(mark_up(l) for l in lines)
    sub = f'<p class="sub fit">{html.escape(d["sub"])}</p>' if d.get("sub") else ""
    big = mark_up(d.get("big", ""))
    ph = f"background-image:url('{photo_url}')"
    if layout == "boxes":
        inner = f'<div class="w" style="{ph}"><span class="kicker">{kicker}</span><div class="t">' + "".join(f'<span class="ln fit">{mark_up(l)}</span>' for l in lines) + f"</div>{logo}</div>"
    elif layout == "giant":
        inner = f'<div class="w" style="{ph}"><span class="kicker">{kicker}</span><div class="t"><div class="big fit">{big}</div><div class="h fit">{h}</div>{sub}</div>{logo}</div>'
    elif layout == "number":
        unit = f'<small>{html.escape(d.get("unit", ""))}</small>' if d.get("unit") else ""
        inner = f'<div class="w"><div class="n"><span class="kicker">{kicker}</span><div class="big fit">{big}{unit}</div><div class="h fit">{h}</div>{logo}</div><div class="p" style="{ph}"></div></div>'
    elif layout == "poster":
        inner = f'<div class="w"><div class="p" style="{ph}"></div><span class="kicker">{kicker}</span><div class="t"><div class="big fit">{big}</div><div class="h fit">{h}</div></div>{logo}</div>'
    elif layout == "mincho":
        vs = "".join(f'<span class="v fit">{html.escape(l)}</span>' for l in lines)
        sub_v = f'<span class="sub">{html.escape(d["sub"])}</span>' if d.get("sub") else ""
        inner = f'<div class="w" style="{ph}"><span class="kicker">{kicker}</span><div class="t">{vs}{sub_v}</div>{logo}</div>'
    elif layout == "frame":
        inner = f'<div class="w"><div class="p" style="{ph}"></div><span class="kicker">{kicker}</span><div class="t"><div class="h fit">{h}</div></div>{logo}</div>'
    elif layout == "quote":
        inner = f'<div class="w"><div class="t"><span class="kicker">{kicker}</span><div class="h fit">{h}</div>{logo}</div><div class="p" style="{ph}"></div></div>'
    elif layout == "duo":
        inner = (f'<div class="w"><div class="half l" style="{ph}"><b class="fit">{html.escape(d["a"])}</b></div>'
                 f'<div class="half r" style="{ph}"><b class="fit">{html.escape(d["b"])}</b></div><div class="vs">VS</div>'
                 f'<span class="kicker">{kicker}</span><div class="t"><div class="h">{h}</div></div>{logo}</div>')
    elif layout == "case":
        av = os.path.join(ROOT, "images", "portraits", f"user_0{d.get('avatar', 1)}.png")
        chips = "".join(f'<div class="chip"><small>{html.escape(k)}</small><b class="fit">{html.escape(v)}</b></div>' for k, v in d.get("chips", []))
        if d.get("avatars"):
            ava = "".join(f'<i style="background-image:url(\'file://{os.path.join(ROOT, "images", "portraits", f"user_0{n}.png")}\')"></i>' for n in d["avatars"])
            av_html = f'<div class="avs">{ava}</div>'
            who_html = ""
        else:
            av_html = f'<div class="av" style="background-image:url(\'file://{av}\')"></div>'
            who_html = f'<span class="who">{html.escape(d.get("who", ""))}</span>'
        inner = (f'<div class="w">{av_html}'
                 f'{who_html}<span class="tag">OWNER\'S CASE｜オーナーの事例</span>'
                 f'<div class="t"><div class="h fit">{h}</div></div><div class="chips">{chips}</div>{logo}</div>')
    elif layout == "marker":
        inner = f'<div class="w" style="{ph}"><div class="t"><span class="kicker">{kicker}</span><div class="h fit">{h}</div>{sub}</div>{logo}</div>'
    else:  # type
        inner = f'<div class="w"><div class="t"><span class="kicker">{kicker}</span><div class="h fit">{h}</div>{logo}</div><div class="p" style="{ph}"></div></div>'
    pos = d.get("pos", "center")
    vlen = max([len(l) for l in lines] or [1])
    style = f"--bg:{bg};--fg:{fg};--pos:{pos};--vfs:{min(76, int(500 / (vlen * 1.12)))}px"
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{BASE_CSS}{LAYOUT_CSS[layout]}</style></head>'
            f'<body style="{style}">{inner}<img id="pre" src="{photo_url}" alt="" style="display:none"></body></html>')


RENDER_JS = """
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [src, out] of jobs) {
    await p.goto('file://' + src);
    await p.evaluate(async () => { await document.fonts.ready; await document.getElementById('pre').decode().catch(() => {}); });
    await p.evaluate(() => {
      // 枠からはみ出す行は、収まるまで文字を小さくする
      document.querySelectorAll('.fit').forEach(el => {
        let fs = parseFloat(getComputedStyle(el).fontSize);
        const box = el.parentElement;
        const limit = () => el.scrollWidth > el.clientWidth + 1 || el.getBoundingClientRect().right > box.getBoundingClientRect().right + 1 || el.getBoundingClientRect().right > 1200 - 40;
        let guard = 0;
        while (limit() && fs > 16 && guard++ < 200) { fs -= 2; el.style.fontSize = fs + 'px'; }
      });
    });
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
                d = DESIGNS.get(a["slug"])
                f.write(design_html(a, b, d) if d else page_html(a, b))
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
        layout = DESIGNS[a["slug"]]["layout"] if a["slug"] in DESIGNS else "標準:" + style_of(a)
        print(f"{layout:10}  images/eyecatch/{a['slug']}.jpg")


if __name__ == "__main__":
    main(sys.argv[1:])
