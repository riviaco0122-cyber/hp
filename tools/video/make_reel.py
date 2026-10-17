#!/usr/bin/env python3
"""YouTube 用の動画（横長）から、リール・ショート用の縦長動画（1080×1920）を作る。

横長の動画をそのまま縦にすると、画面が小さく字幕も読めないので、次の形に組み直す:
  上: 「アキヤド 民泊school」とリールの見出し（最初の1秒で何の話かわかる、気になる問い）
  中: 本編の場面（字幕なし）
  下: 大きな字幕（話している人の名前つき）と「フル版は YouTube で」
  最後の約3秒: エンディング「続きは本編で」（ロゴ・番組名・本編のタイトル・▶本編を見る）。表紙の画像（-cover.jpg）も一緒に作る
本編の盛り上がる部分（45〜60秒）を、台本の「場面・セリフ番号」で指定して切り出す。音声も同じ部分を切り出す。

使い方:
  python3 tools/video/make_reel.py <台本スクリプト名> <開始: 場面.セリフ> <終了: 場面.セリフ> "<見出し>" 出力.mp4 [--cover 秒] [--preview 秒 ...]
  例: python3 tools/video/make_reel.py make_strategy_ep1 2.3 2.6 "家賃5万円の家を\\n宿にしたら？" reel.mp4
  見出しの改行は \\n。終了は、そのセリフの終わりまで入る。--preview は切り出した中での秒（PNG を /tmp/reel_preview に）。
"""
import importlib, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import make_explainer as base

FPS = 24

REEL_JS = r"""
function reelWrap(s,n){ // 縦長の字幕は1行 n 文字までで、句読点のあとで分ける
  const out=[];let cur='';
  for(const ch of s){cur+=ch;if(cur.length>=n||(cur.length>=n*.6&&'。、！？'.includes(ch))){out.push(cur);cur=''}}
  if(cur){if(cur.length<=2&&out.length)out[out.length-1]+=cur;else out.push(cur)}
  return out;
}
function REEL(out,t,cur){
  const VY=470,S=1080/1920,CH=880;  // CH: 本編のうち見せる高さ（下の字幕帯の部分は切る）
  let r=`<rect width="1080" height="1920" fill="${G}"/>`;
  for(let k=0;k<10;k++){const x=((k*240+t*60)%2600)-500;r+=`<path d="M${x} 1920 L${x+700} 0" stroke="#fff" stroke-width="44" opacity=".05"/>`}
  r+=`<rect width="1080" height="16" fill="${T}"/><rect y="1904" width="1080" height="16" fill="${Y}"/>`;
  r+=`<g transform="translate(540,110)"><rect x="-300" y="-46" width="600" height="92" rx="46" fill="#fff"/>${MARK(-238,0,.95)}<text x="22" y="17" text-anchor="middle" font-size="46" font-weight="900" fill="${G}">アキヤド <tspan fill="${T}">民泊school</tspan></text></g>`;
  REEL_TITLE.split('\n').forEach((ln,k,a)=>{r+=`<text x="540" y="${300+k*112-(a.length-1)*20}" text-anchor="middle" font-size="96" font-weight="900" fill="#fff" stroke="${DG}" stroke-width="14" paint-order="stroke" stroke-linejoin="round">${ln}</text>`});
  r+=`<rect x="0" y="${VY-6}" width="1080" height="${CH*S+12}" fill="#fff"/><clipPath id="reelclip"><rect x="0" y="${VY}" width="1080" height="${CH*S}"/></clipPath><g clip-path="url(#reelclip)"><g transform="translate(0,${VY}) scale(${S})">${out}</g></g>`;
  if(cur){const o=clamp((t-cur[0]+.05)/.15)*clamp((cur[1]+.25-t)/.15),lines=REEL_SUBS[LINES.indexOf(cur)]||reelWrap(cur[3].join(''),13),y0=1130;
    const nm=VNAME[cur[2]]||'';
    r+=`<g opacity="${o}"><rect x="50" y="${y0-40}" width="980" height="${lines.length*86+70}" rx="36" fill="#fff"/>`+(nm?`<rect x="80" y="${y0-72}" width="${nm.length*36+60}" height="64" rx="32" fill="${VCOL[cur[2]]||T}"/><text x="${110+nm.length*18}" y="${y0-29}" text-anchor="middle" font-size="36" font-weight="900" fill="#fff">${nm}</text>`:'')+lines.map((s,i)=>`<text x="540" y="${y0+52+i*86}" text-anchor="middle" font-size="62" font-weight="900" fill="${DG}">${s}</text>`).join('')+`</g>`;}
  r+=`<g transform="translate(540,1800)"><rect x="-330" y="-50" width="660" height="100" rx="50" fill="${T}"/><text x="0" y="16" text-anchor="middle" font-size="46" font-weight="900" fill="#fff">フル版は YouTube で ▶</text></g>`;
  // エンディング（最後の約3秒）：「続きは本編で」
  const e=clamp((t-REEL_T1)/.35);
  if(e>0){const ep=(typeof EP_TITLE!=='undefined'?EP_TITLE:REEL_TITLE.replace('\n',''));
    r+=`<g opacity="${e}"><rect width="1080" height="1920" fill="${G}"/>`;
    for(let k=0;k<10;k++){const x=((k*240+t*60)%2600)-500;r+=`<path d="M${x} 1920 L${x+700} 0" stroke="#fff" stroke-width="44" opacity=".06"/>`}
    r+=`<rect width="1080" height="16" fill="${T}"/><rect y="1904" width="1080" height="16" fill="${Y}"/>`;
    r+=pop(540,760,clamp((t-REEL_T1-.1)/.5),`<circle cx="540" cy="760" r="150" fill="#fff"/>${MARK(540,760,3.3)}`);
    r+=pop(540,1060,clamp((t-REEL_T1-.35)/.5),`<text x="540" y="1090" text-anchor="middle" font-size="120" font-weight="900" fill="#fff" stroke="${DG}" stroke-width="14" paint-order="stroke" stroke-linejoin="round">続きは本編で</text>`);
    r+=pop(540,1280,clamp((t-REEL_T1-.6)/.5),`<rect x="90" y="1190" width="900" height="200" rx="40" fill="#fff"/><text x="540" y="1266" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">YouTube「アキヤド 民泊school」</text><text x="540" y="1340" text-anchor="middle" font-size="${ep.length>14?40:48}" font-weight="900" fill="${DG}">${ep}</text>`);
    r+=pop(540,1530,clamp((t-REEL_T1-.85)/.5),`<rect x="190" y="1470" width="700" height="120" rx="60" fill="${T}"/><text x="540" y="1550" text-anchor="middle" font-size="54" font-weight="900" fill="#fff">▶ 本編を見る</text>`);
    r+=fade(clamp((t-REEL_T1-1.1)/.5),`<text x="540" y="1700" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">プロフィール・概要欄のリンクから</text>`,0);
    r+=`</g>`;}
  return r;
}
"""


def reel_wrap(s, n):
    """縦長の字幕の改行。句読点で区切った語句を、1行 n+2 文字までに詰める（語句の途中で切らない）。
    1つの語句が長すぎるときだけ、まん中に近い助詞のあとで切る（数字・単位の途中では切らない）"""
    import re
    chunks = [c for c in re.split(r"(?<=[、。！？])", s) if c]
    pieces = []
    for c in chunks:
        while len(c) > n + 2:
            mid = len(c) / 2; best = None
            for i in range(3, len(c) - 2):
                a, b = c[i - 1], c[i]
                if a in "はがをにでともへや" and not b.isdigit() and b not in "、。":
                    sc = abs(i - mid)
                    if best is None or sc < best[0]:
                        best = (sc, i)
            i = best[1] if best else n
            pieces.append(c[:i]); c = c[i:]
        pieces.append(c)
    out = []
    for p in pieces:
        if out and len(out[-1]) + len(p) <= n + 2:
            out[-1] += p
        else:
            out.append(p)
    return out

def main():
    args = sys.argv[1:]
    prev = None
    cover_t = 0.8
    if "--cover" in args:  # 表紙にするコマ（切り出した中での秒）。見出しと、いちばん「へえ」となる図が出ている瞬間を選ぶ
        k = args.index("--cover"); cover_t = float(args[k + 1]); del args[k:k + 2]
    if "--preview" in args:
        k = args.index("--preview"); prev = [float(x) for x in args[k + 1:]]; args = args[:k]
    modname, a, b, title, out = args[:5]
    title = title.replace("\\n", "\n")
    mod = importlib.import_module(modname.replace(".py", ""))
    sc, lines, voices, sfx = mod.timeline(os.path.join(tempfile.gettempdir(), "akiyado_vv"))
    find = lambda p: next(l for l in lines if (l[4], l[5]) == tuple(int(x) for x in p.split(".")))
    t0 = max(0.0, find(a)[0] - 0.05); ts = find(a)[0] + 0.35; t1 = find(b)[1] + 0.35; END = 3.2  # END: エンディング（続きは本編で）の秒数
    html = mod.build_html(sc, lines)
    html = html.replace("if(cur)out+=subtitle(cur,t);", "")
    html = html.replace("window.draw=function(t){", "window.draw=function(TT){let t=Math.min(Math.max(TT,REEL_TS),REEL_T1);  /* 最初は前の場面の残りを見せず、1コマ目から今回の場面で始める */")
    html = html.replace("document.getElementById('s').innerHTML=out.replaceAll", "document.getElementById('s').innerHTML=REEL(out,TT,TT>REEL_T1?null:cur).replaceAll")
    html = html.replace("width:1920px;height:1080px", "width:1080px;height:1920px")
    html = html.replace('<svg id="s" width="1920" height="1080" viewBox="0 0 1920 1080">', '<svg id="s" width="1080" height="1920" viewBox="0 0 1080 1920">')
    i = html.index("window.draw=function")
    subs = [reel_wrap("".join(l[3]), 13) for l in lines]
    html = html[:i] + f"const REEL_TITLE={json.dumps(title, ensure_ascii=False)};const REEL_SUBS={json.dumps(subs, ensure_ascii=False)};const REEL_T1={t1};const REEL_TS={ts};" + REEL_JS + html[i:]
    assert "REEL(out,t,cur)" in html and 'viewBox="0 0 1080 1920"' in html, "台本スクリプトの形が想定とちがいます"
    js = base.RENDER_JS.replace("await p.evaluate((r) => { window.ROOT = r; }, process.env.ROOT_DIR);", "await p.evaluate((r) => { window.ROOT = r; }, process.env.ROOT_DIR); await p.evaluate(() => window.draw(%s)); await p.waitForTimeout(1500); await p.evaluate(async () => { await document.fonts.ready; });" % t0)
    js = js.replace("width: 1920, height: 1080", "width: 1080, height: 1920").replace("i / 24", f"{t0} + i / 24").replace("window.draw(t), t)", f"window.draw({t0}+t), t)")
    env = dict(os.environ); env["ROOT_DIR"] = ROOT
    env["NODE_PATH"] = os.pathsep.join(p for p in ["/opt/node-tools/node_modules", os.path.join(ROOT, "tools", "check", "node_modules"), env.get("NODE_PATH", "")] if p)
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(html)
        j = os.path.join(tmp, "r.js"); open(j, "w").write(js)
        if prev is not None:
            od = os.path.join(tempfile.gettempdir(), "reel_preview"); os.makedirs(od, exist_ok=True)
            subprocess.run(["node", j, h, od, "preview", json.dumps(prev)], check=True, env=env)
            print("preview", od, "長さ", round(t1 - t0 + END, 1), "秒"); return
        fr = os.path.join(tmp, "fr"); os.makedirs(fr)
        subprocess.run(["node", j, h, fr, "video", str(int((t1 - t0 + END) * FPS))], check=True, env=env)
        import pop_audio
        wav = os.path.join(tmp, "a.wav"); pop_audio.write(wav, sc[-1][1], sfx, bgm_gain=0.22, voices=voices, duck=0.3)
        endw = os.path.join(tmp, "end.wav"); pop_audio.write(endw, END, [(0.1, "bling"), (0.95, "chime")], bgm_gain=0.22)
        body = os.path.join(tmp, "body.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t0), "-t", str(t1 - t0), "-i", wav,
                        "-af", f"afade=t=out:st={max(0, t1 - t0 - 0.5):.2f}:d=0.5", "-ar", "44100", "-ac", "2", body], check=True)
        audio = os.path.join(tmp, "audio.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", body, "-i", endw, "-filter_complex",
                        "[1:a]aformat=sample_rates=44100:channel_layouts=stereo[e];[0:a][e]concat=n=2:v=0:a=1[a]", "-map", "[a]", audio], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%05d.jpg"), "-i", audio,
                        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", out], check=True)
        cover = os.path.splitext(out)[0] + "-cover.jpg"  # リールの表紙（--cover の秒のコマ：見出しと図が出ている）
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", str(cover_t), "-i", out, "-frames:v", "1", "-q:v", "2", cover], check=True)
    print(out, round(t1 - t0 + END, 1), "秒")


if __name__ == "__main__":
    main()
