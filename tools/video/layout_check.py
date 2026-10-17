#!/usr/bin/env python3
"""動画の自動点検（書き出しの前に回す）。決まった間隔でコマを描き、文字まわりの崩れを機械で探す。

見つけるもの:
  covered   文字の上に、別の図形や文字が重なって隠している（例: 札がスマホの裏に隠れる、ハンコが本文を隠す）
  clash     文字どうしが重なっている（見出しとカウントダウン、ラベルどうし など）
  offscreen 文字が画面の外にはみ出している
  subtitle  字幕の帯が、図の文字を隠している
アニメで出入りしている途中（薄い・小さい）の文字は数えない。同じ不具合が続く時間は1件にまとめる。

使い方: python3 tools/video/layout_check.py make_strategy_ep1 [--step 0.5] [--from 秒] [--to 秒]
  問題があれば終了コード1。結果は「秒・種類・文字」の一覧（scratch に PNG は作らない）。
"""
import importlib, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

CHECK_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [html, times] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + html);
  await p.evaluate(async () => { await document.fonts.ready; });
  const out = [];
  for (const t of JSON.parse(times)) {
    await p.evaluate((t) => window.draw(t), t);
    const r = await p.evaluate(() => {
      const svg = document.getElementById('s'), res = [];
      const op = (el) => { let o = 1; for (let e = el; e && e !== svg; e = e.parentNode) { const a = e.getAttribute && e.getAttribute('opacity'); if (a != null) o *= parseFloat(a); const fo = e.getAttribute && e.getAttribute('fill-opacity'); if (fo != null && e === el) o *= parseFloat(fo); } return o; };
      const texts = [...svg.querySelectorAll('text')].filter(e => e.textContent.trim() && op(e) > .85);
      const isSub = (e) => { for (let x = e; x && x !== svg; x = x.parentNode) if (x.dataset && x.dataset.sub) return true; return false; };
      const boxes = texts.map(e => { const r = e.getBoundingClientRect(); return { e, r, s: isSub(e), txt: e.textContent.trim().slice(0, 24), fs: parseFloat(e.getAttribute('font-size') || 30) }; })
        .filter(o => o.r.width > 4 && o.r.height >= 18);  // 人物の名札など、ごく小さい文字は数えない
      // 全面を覆う幕（暗転・場面転換・タイトルなどの手前に出す暗い幕・終わりの画面）の下にある文字は、わざと隠しているので数えない
      const covers = [...svg.querySelectorAll('rect')].filter(el => parseFloat(el.getAttribute('width') || 0) >= 1900 && parseFloat(el.getAttribute('height') || 0) >= 1000 && op(el) >= .3 && !(el.closest && el.closest('clipPath')));
      for (let i = boxes.length - 1; i >= 0; i--) { const e = boxes[i].e; if (covers.some(c => (c.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_PRECEDING) && !c.parentNode.contains(e) )) boxes.splice(i, 1); }
      // 画面の外
      for (const o of boxes) { const r = o.r; if (r.left < -4 || r.top < -4 || r.right > 1924 || r.bottom > 1084) res.push(['offscreen', o.txt]); }
      // 文字どうし
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], c = boxes[j]; if (a.s !== c.s) continue;
        const w = Math.min(a.r.right, c.r.right) - Math.max(a.r.left, c.r.left), h = Math.min(a.r.bottom, c.r.bottom) - Math.max(a.r.top, c.r.top);
        if (w > 6 && h > Math.min(a.r.height, c.r.height) * .35) res.push(['clash', a.txt + ' ／ ' + c.txt]);
      }
      // 隠れている（文字の中の点で、いちばん上にある要素が文字自身でない）
      for (const o of boxes) {
        const r = o.r, pts = []; for (let k = 1; k <= 5; k++) for (const fy of [.4, .6]) pts.push([r.left + r.width * k / 6, r.top + r.height * fy]);
        let hid = 0, bySub = 0;
        for (const [x, y] of pts) { if (x < 0 || y < 0 || x > 1919 || y > 1079) continue; const top = document.elementFromPoint(x, y); if (!top || top === o.e || o.e.contains(top) || top === svg) continue;
          if (top.tagName === 'text' || top.tagName === 'tspan') { const tt = top.tagName === 'tspan' ? top.parentNode : top; if (op(tt) < .3) continue; }
          else { const f = top.getAttribute('fill'), sw = top.getAttribute('stroke'); if ((f === 'none' || !f) && !sw) continue; if (op(top) < .7) continue; }
          if (isSub(top) && !o.s) bySub++; else hid++; }
        if (hid >= 3) res.push(['covered', o.txt]);
        if (bySub >= 3) res.push(['subtitle', o.txt]);
      }
      return res;
    });
    for (const x of r) out.push([t, ...x]);
  }
  console.log(JSON.stringify(out));
  await b.close();
})();
"""


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    mod = importlib.import_module(args[0].replace(".py", ""))
    opt = lambda k, d: float(args[args.index(k) + 1]) if k in args else d
    step = opt("--step", 0.5)
    sc, lines, _, _ = mod.timeline(os.path.join(tempfile.gettempdir(), "akiyado_vv"))
    dur = sc[-1][1]
    t0, t1 = opt("--from", 0.0), min(opt("--to", dur), dur - 0.05)
    html = mod.build_html(sc, lines).replace("if(cur)out+=subtitle(cur,t);", "if(cur)out+=subtitle(cur,t).replace('<g ','<g data-sub=\"1\" ');")
    times = []
    t = t0
    while t < t1:
        times.append(round(t, 2)); t += step
    env = dict(os.environ)
    env["NODE_PATH"] = os.pathsep.join(p for p in ["/opt/node-tools/node_modules", os.path.join(ROOT, "tools", "check", "node_modules"), env.get("NODE_PATH", "")] if p)
    found = []
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(html)
        js = os.path.join(tmp, "c.js"); open(js, "w").write(CHECK_JS)
        for k in range(0, len(times), 200):  # 少しずつ（ブラウザの負荷を抑える）
            r = subprocess.run(["node", js, h, json.dumps(times[k:k + 200])], capture_output=True, text=True, env=env)
            if r.returncode:
                print(r.stderr[-2000:]); sys.exit(2)
            found += json.loads(r.stdout.strip().splitlines()[-1])
    # 同じ種類・同じ文字で続くものは、1件（開始〜終了）にまとめる
    merged = {}
    for t, kind, what in found:
        key = (kind, what)
        if key in merged and t - merged[key][-1][1] <= step * 2.5:
            merged[key][-1][1] = t
        else:
            merged.setdefault(key, []).append([t, t])
    rows = sorted((a, b, k, w) for (k, w), spans in merged.items() for a, b in spans if b - a >= step * 0.99 or k in ("offscreen",))
    scene_of = lambda t: next((i for i, (a, b) in enumerate(sc) if a <= t < b), len(sc) - 1)
    for a, b, k, w in rows:
        i = scene_of(a)
        print(f"{a:7.1f}〜{b:6.1f}秒  場面{i}（{a - sc[i][0]:.1f}秒目）  {k:9s} {w}")
    print(f"点検 {len(times)} コマ（{step}秒ごと）: 問題 {len(rows)} 件")
    sys.exit(1 if rows else 0)


if __name__ == "__main__":
    main()
