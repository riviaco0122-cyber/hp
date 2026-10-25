#!/usr/bin/env python3
"""動画の自動点検（書き出しの前に回す）。決まった間隔でコマを描き、文字まわりの崩れを機械で探す。

見つけるもの:
  covered   文字の上に、別の図形や文字が重なって隠している（例: 札がスマホの裏に隠れる、ハンコが本文を隠す）
  clash     文字どうしが重なっている（見出しとカウントダウン、ラベルどうし など）
  offscreen 文字が画面の外にはみ出している
  subtitle  字幕の帯が、図の文字を隠している
アニメで出入りしている途中（薄い・小さい）の文字は数えない。同じ不具合が続く時間は1件にまとめる。

図まわりの点検（2026-10-25 追加。manual.md 4-3章。第2回のように card()/bx() でカードを描く台本が対象）:
  cardout   カード（url(#cardG) の白い板）の中身の図形・文字・小物が、カードの枠の外にはみ出している
  offcenter カードの中身をまとめた外接矩形が、カードの中心から左右にずれている（左右の余白の比が 2 倍を超え、差が 80px 以上）
  smalltext 文字が小さすぎる（1080p 換算の font-size が下限未満。既定 26、--min-fs で変える。人物の名札は除く）
  overlap   主役（宿 inn・人物 person）や小物（自転車・スーツケース・ポスト・植木・街灯 など）どうしの重なり
            （宿の中に置いた小物どうし・宿の外の人物や街灯との重なりを見る。壁の前に置くのは数えない）
  numdup    番号の二重表示の疑い（丸や板の中の「①」／「①」と同じ番号の数字が近くにある／同じ画面に ① と 1・2・3 が混在）
  caveat    台本（字幕）に断り書き（「一例です」「限りません」「違います」など）がある。稼働率の必須注意（手間・初期費用が入っていない）は許可リスト
  ※ 黒い幕の下・出入りの途中・影と光（黒の半透明・glow）は数えない。誤検知が出たら、直すか、しきい値（下のオプション）を見直す。

使い方: python3 tools/video/layout_check.py make_strategy_ep2 [--step 0.5] [--from 秒] [--to 秒] [--min-fs 26] [--no-fig]
  --no-fig  図まわりの点検（上の6つ）を飛ばす（文字の点検だけにする）
  問題があれば終了コード1。結果は「秒・種類・文字」の一覧（scratch に PNG は作らない）。
  直したあとは、0.5〜1秒ごとのコマでカードの縁を目で確かめる（manual.md 4-3章）。
"""
import importlib, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

FIG_JS = r"""
// ---- 図まわりの点検（カード・小物・主役・番号・文字サイズ） ----
function figChecks(svg, op, texts, covers, res, OPT) {
  const R = (e) => e.getBoundingClientRect();
  const inDefs = (e) => !!(e.closest && (e.closest('defs') || e.closest('clipPath') || e.closest('mask')));
  const clipped = (e) => { for (let x = e; x && x !== svg; x = x.parentNode) if (x.getAttribute && x.getAttribute('clip-path')) return true; return false; };
  const covered = (e) => covers.some(c => (c.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_PRECEDING) && !c.parentNode.contains(e));
  // 影・光・飾りの透明な塗りは、図形として数えない
  const isDeco = (e) => {
    const f = (e.getAttribute('fill') || '').trim(), o = parseFloat(e.getAttribute('opacity') || 1), st = e.getAttribute('stroke');
    if (/^url\(#(glow|b\d+r)\)/.test(f)) return true;
    if ((f === '#000' || f === '#000000') && o <= .3) return true;
    if (f === '#fff' && o <= .35 && !st) return true;           // 光沢の白いすじ
    if ((f === 'none' || !f) && !st) return true;
    if (o < .05) return true;
    return false;
  };
  const leaves = (root) => [...root.querySelectorAll('rect,circle,ellipse,path,polygon,polyline,line,text,image')]
    .filter(e => !inDefs(e) && !isDeco(e) && !clipped(e) && !(e.tagName === 'text' && !e.textContent.trim()));
  const union = (els) => { let L = 1e9, T = 1e9, Rr = -1e9, B = -1e9, n = 0; for (const e of els) { const r = R(e); if (r.width < .5 && r.height < .5) continue; L = Math.min(L, r.left); T = Math.min(T, r.top); Rr = Math.max(Rr, r.right); B = Math.max(B, r.bottom); n++; } return n ? { left: L, top: T, right: Rr, bottom: B, width: Rr - L, height: B - T } : null; };
  const opAnc = (e) => op(e);

  // (a)(b) カード
  const cards = [...svg.querySelectorAll('rect')].filter(r => (r.getAttribute('fill') || '') === 'url(#cardG)' && parseFloat(r.getAttribute('width')) >= 300 && parseFloat(r.getAttribute('height')) >= 200 && !inDefs(r));
  for (const c of cards) {
    if (covered(c) || op(c) < .99) continue;
    const cw = parseFloat(c.getAttribute('width')), cr = R(c);
    if (Math.abs(cr.width - cw) > 2) continue;                        // 出入りの途中（拡大縮小中）は数えない
    const label = 'カード(' + Math.round(parseFloat(c.getAttribute('x'))) + ',' + Math.round(parseFloat(c.getAttribute('y'))) + ')';
    const kids = [];
    for (let n = c.nextElementSibling; n; n = n.nextElementSibling) kids.push(n);
    const items = kids.flatMap(k => (/^(rect|circle|ellipse|path|polygon|polyline|line|text|image)$/.test(k.tagName) ? (isDeco(k) || clipped(k) ? [] : [k]) : leaves(k)));
    const vis = items.filter(e => op(e) > .85);
    // 上の縁にまたがる「見出しの札」（丸い帯で、中心がカードの内側にあり、はみ出しが高さの6割以下）は、わざとなので数えない
    const tabs = vis.filter(e => { if (e.tagName !== 'rect') return false; const r = R(e), rx = parseFloat(e.getAttribute('rx') || 0);
      return rx >= r.height * .45 && r.top < cr.top - 4 && r.bottom < cr.bottom && cr.top - r.top <= r.height * .6 && r.left > cr.left && r.right < cr.right; }).map(R);
    const inTab = (r) => tabs.some(t => r.left >= t.left - 4 && r.right <= t.right + 4 && r.top >= t.top - 4 && r.bottom <= t.bottom + 4);
    for (const e of vis) {
      const r = R(e), tol = 4;
      if (inTab(r) || tabs.some(t => t.left === r.left && t.top === r.top)) continue;
      if (r.width < 1 && r.height < 1) continue;
      if (r.left < cr.left - tol || r.right > cr.right + tol || r.top < cr.top - tol || r.bottom > cr.bottom + tol) {
        const what = e.tagName === 'text' ? '「' + e.textContent.trim().slice(0, 14) + '」' : e.tagName;
        res.push(['cardout', label + ' から ' + what + ' がはみ出し']);
      }
    }
    // (b) 左右のずれ（カード幅の 92% 以上ある下地・帯は除く。出入りの途中の要素も入れて、完成形で見る）
    const body = items.filter(e => { const r = R(e); return r.width < cw * .92 && op(e) > .5; });
    const u = union(body);
    if (u && body.length >= 2 && vis.length === items.filter(e => op(e) > .05).length) {
      const l = u.left - cr.left, rr = cr.right - u.right;
      if (Math.abs(l - rr) >= 80 && Math.max(l, rr) > 2 * Math.max(Math.min(l, rr), 1)) res.push(['offcenter', label + ' 左余白' + Math.round(l) + ' 右余白' + Math.round(rr)]);
    }
  }

  // (c) 文字サイズ
  const minFs = OPT.minFs || 26;
  for (const e of texts) {
    if (e.closest && e.closest('[data-obj="person"]')) continue;
    if (covered(e)) continue;
    const m = e.getScreenCTM(), fs = parseFloat(e.getAttribute('font-size') || 30) * (m ? Math.hypot(m.a, m.b) : 1);
    if (fs < minFs - .01) res.push(['smalltext', Math.round(fs) + 'px 「' + e.textContent.trim().slice(0, 18) + '」']);
  }

  // (d) 主役・小物の重なり
  const objs = [...svg.querySelectorAll('[data-obj]')].filter(g => !covered(g) && op(g) > .85);
  const box = (g) => {
    // 入れ子の別の物（宿の中の小物など）は含めず、自分の図形だけで外接矩形を作る
    const own = leaves(g).filter(e => e.closest('[data-obj]') === g);
    return union(own);
  };
  const info = objs.map(g => { const own = leaves(g).filter(e => e.closest('[data-obj]') === g && R(e).width > 3 && R(e).height > 3); return { g, k: g.dataset.obj, own, rs: own.map(R), b: union(own) }; }).filter(o => o.b && o.b.width > 8 && o.b.height > 8);
  const nm = (o) => ({ inn: '宿', person: '人物', prop: o.g.dataset.name || '小物', lamp: '街灯' }[o.k] || o.k);
  for (let i = 0; i < info.length; i++) for (let j = i + 1; j < info.length; j++) {
    const a = info[i], b = info[j];
    if (a.g.contains(b.g) || b.g.contains(a.g)) continue;   // 宿と、その中に置いた小物の関係は見ない（壁の前に置くのは普通）
    if (a.k === 'lamp' && b.k === 'lamp') continue;
    if (Math.min(a.b.right, b.b.right) - Math.max(a.b.left, b.b.left) <= 8 || Math.min(a.b.bottom, b.b.bottom) - Math.max(a.b.top, b.b.top) <= 8) continue;
    // 外接矩形ではなく、1つ1つの図形（腕・車輪・柱など）どうしが重なっているかを見る
    let best = 0, bx = 0;
    for (const p of a.rs) for (const q of b.rs) {
      const w = Math.min(p.right, q.right) - Math.max(p.left, q.left), h = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
      if (w > 8 && h > 8 && w * h > best) { best = w * h; bx = (Math.max(p.left, q.left) + Math.min(p.right, q.right)) / 2; }
    }
    if (best < 200) continue;
    res.push(['overlap', [nm(a), nm(b)].sort().join(' と ') + ' が重なっている x≈' + Math.round(bx / 40) * 40]);
  }

  // (e) 番号の二重表示
  const CIRC = /[①-⑳❶-❿⓵-⓾]/;
  const circNo = (s) => { const m = s.match(CIRC); if (!m) return null; const c = m[0].charCodeAt(0); return c >= 0x2460 && c <= 0x2473 ? c - 0x2460 + 1 : c >= 0x2776 && c <= 0x277F ? c - 0x2776 + 1 : c - 0x24F5 + 1; };
  const tt = texts.filter(e => !covered(e)).map(e => ({ e, s: e.textContent.trim(), r: R(e) }));
  const circs = tt.filter(o => circNo(o.s) != null), plain = tt.filter(o => /^[0-9]{1,2}$/.test(o.s));
  const shapes = [...svg.querySelectorAll('circle,rect')].filter(e => !inDefs(e) && !isDeco(e) && op(e) > .85);
  for (const o of circs) {
    const cx = (o.r.left + o.r.right) / 2, cy = (o.r.top + o.r.bottom) / 2;
    // 丸・板の中に「①」だけが入っている（丸の数字なのに、さらに丸がある）
    if (o.s.length <= 2) {
      const ring = shapes.some(e => { const r = R(e); const sq = Math.abs(r.width - r.height) < 4 && r.width < 150 && r.width > o.r.width * .9; return (e.tagName === 'circle' || (e.tagName === 'rect' && parseFloat(e.getAttribute('rx') || 0) >= r.width * .4)) && sq && cx > r.left && cx < r.right && cy > r.top && cy < r.bottom && !e.closest('defs'); });
      if (ring) res.push(['numdup', '丸の中に「' + o.s + '」（丸の数字を二重に飾っている疑い）']);
    }
    const n = circNo(o.s);
    for (const p of plain) { if (parseInt(p.s, 10) === n && Math.hypot((p.r.left + p.r.right) / 2 - cx, (p.r.top + p.r.bottom) / 2 - cy) < 160) res.push(['numdup', '「' + o.s + '」と数字「' + p.s + '」が近くにある']); }
  }
  if (circs.length && plain.some(p => parseInt(p.s, 10) >= 1 && parseInt(p.s, 10) <= 9 && p.r.width < 80)) res.push(['numdup', '同じ画面に「' + circs[0].s + '」と数字（' + plain.map(p => p.s).slice(0, 3).join('・') + '）が混在']);
}
window.figChecks = figChecks;
"""

CHECK_JS = r"""
const { chromium } = require('playwright');

const FIGSRC = __FIGSRC__;
(async () => {
  const [html, times, optsJson] = process.argv.slice(2);
  const OPT = JSON.parse(optsJson || '{}');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + html);
  await p.evaluate(async () => { await document.fonts.ready; });
  await p.addScriptTag({ content: FIGSRC });
  const out = [];
  for (const t of JSON.parse(times)) {
    await p.evaluate((t) => window.draw(t), t);
    const r = await p.evaluate((OPT) => {
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
      if (!OPT.noFig) window.figChecks(svg, op, texts, covers, res, OPT);
      return res;
    }, OPT);
    for (const x of r) out.push([t, ...x]);
  }
  console.log(JSON.stringify(out));
  await b.close();
})();
"""


# 主役・小物の関数を、点検用に <g data-obj="種類"> で包む（絵は変わらない。点検用の HTML にだけ入れる）
OBJ_WRAP = {"inn": ("inn", ""), "person": ("person", ""), "person2": ("person", ""), "lamp": ("lamp", ""),
            "bike": ("prop", "自転車"), "suitcase": ("prop", "スーツケース"), "postbox": ("prop", "ポスト"), "plant": ("prop", "植木"),
            "keyp": ("prop", "鍵"), "lantern": ("prop", "提灯")}


def wrap_objects(html):
    extra = ""
    for name, (kind, label) in OBJ_WRAP.items():
        h2 = re.sub(r"function\s+%s\s*\(" % name, "function __o_%s(" % name, html, count=1)
        if h2 == html:
            h2 = re.sub(r"const\s+%s\s*=\s*\(" % name, "const __o_%s=(" % name, html, count=1)
        if h2 == html:
            continue  # この台本にない部品
        html = h2
        extra += "var %s=function(...a){const r=__o_%s(...a);return typeof r==='string'&&r?'<g data-obj=\"%s\" data-name=\"%s\">'+r+'</g>':r};" % (name, name, kind, label)
    # function 宣言の名前は巻き上げられるので、var で上書きできる。const の名前は上書きできないため、別名で作って差し替える
    return html, extra


# 台本（字幕）の断り書き。話が途切れる原因になるので、本文には入れず注意書き欄にまとめる（manual.md 4-3章）
CAVEAT_RE = re.compile(r"(事例です|一例です|ひとつの例です|1例です|1件の|1人の事例|あくまで|限りません|とは限|話ではありません|(?:とは|は|も)違います|違いますが|個人の|経験です)")
CAVEAT_OK = re.compile(r"(入っていません|含まれていません|含みません|手間.*初期|初期.*手間)")  # 稼働率の必須注意


def caveats(lines, sc):
    out = []
    for l in lines:
        txt = "".join(l[3]) if isinstance(l[3], (list, tuple)) else str(l[3]).replace("\n", "")
        m = CAVEAT_RE.search(txt)
        if m and not CAVEAT_OK.search(txt):
            out.append((l[0], l[1], "caveat", f"「{m.group(0)}」 {txt[:30]}"))
    return out


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
    nofig = "--no-fig" in args
    if not nofig:
        html, extra = wrap_objects(html)
        html = html.replace("</script></body></html>", extra + "</script></body></html>")
    times = []
    t = t0
    while t < t1:
        times.append(round(t, 2)); t += step
    env = dict(os.environ)
    env["NODE_PATH"] = os.pathsep.join(p for p in ["/opt/node-tools/node_modules", os.path.join(ROOT, "tools", "check", "node_modules"), env.get("NODE_PATH", "")] if p)
    found = []
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(html)
        js = os.path.join(tmp, "c.js"); open(js, "w").write(CHECK_JS.replace("__FIGSRC__", json.dumps(FIG_JS)))
        opts = json.dumps({"noFig": nofig, "minFs": opt("--min-fs", 26)})
        for k in range(0, len(times), 200):  # 少しずつ（ブラウザの負荷を抑える）
            r = subprocess.run(["node", js, h, json.dumps(times[k:k + 200]), opts], capture_output=True, text=True, env=env)
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
    if not nofig:  # 台本の断り書き（字幕が出ている時間を1件として出す）
        rows += [(a, b, k, w) for a, b, k, w in caveats(lines, sc) if a <= t1 and b >= t0]
        rows.sort()
    scene_of = lambda t: next((i for i, (a, b) in enumerate(sc) if a <= t < b), len(sc) - 1)
    for a, b, k, w in rows:
        i = scene_of(a)
        print(f"{a:7.1f}〜{b:6.1f}秒  場面{i}（{a - sc[i][0]:.1f}秒目）  {k:9s} {w}")
    print(f"点検 {len(times)} コマ（{step}秒ごと）: 問題 {len(rows)} 件")
    sys.exit(1 if rows else 0)


if __name__ == "__main__":
    main()
