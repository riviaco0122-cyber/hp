#!/usr/bin/env python3
"""YouTube 用の動画（横長）から、リール・ショート用の縦長動画（1080×1920）を作る。

横長の動画をそのまま縦にすると、画面が小さく字幕も読めないので、次の形に組み直す:
  上: 「アキヤド 民泊school」とリールの見出し（最初の1秒で何の話かわかる、気になる問い）
  中: 本編の場面（字幕なし）
  下: 大きな字幕（話している人の名前つき）。「フル版は YouTube で」のボタンは置かない（アプリの関連動画・説明と重なるため）
  各アプリの文字・ボタンが重なる所（下の約480px・右の約160px・上の約200px）には何も置かない
  最後の約3秒: エンディング「続きは本編で」（ロゴ・番組名・本編のタイトル・▶本編を見る）。表紙の画像（-cover.jpg）も一緒に作る
本編の盛り上がる部分（45〜60秒）を、台本の「場面・セリフ番号」で指定して切り出す。音声も同じ部分を切り出す。

使い方:
  python3 tools/video/make_reel.py <台本スクリプト名> <開始: 場面.セリフ> <終了: 場面.セリフ> "<見出し>" 出力.mp4 [--cover 秒] [--cover-only] [--preview 秒 ...]
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
function SKY(){ // 下の飾りの町並み（アプリの説明が重なる所なので、情報は置かない。空っぽに見えないように）
  let g=`<path d="M0 1760 Q270 1700 540 1740 T1080 1730 V1920 H0Z" fill="${DG}" opacity=".35"/>`;
  [[60,1,0],[200,.8,1],[330,1.15,0],[500,.9,1],[640,1.05,0],[790,.85,1],[930,1.1,0],[1050,.8,1]].forEach(([x,k,f])=>{const w=110*k,h=90*k,y=1800;
    g+=`<g opacity=".5"><rect x="${x-w/2}" y="${y-h}" width="${w}" height="${h+120}" fill="${DG}"/><path d="M${x-w/2-14} ${y-h} L${x} ${y-h-62*k} L${x+w/2+14} ${y-h}Z" fill="${DG}"/>`+(f?'':`<rect x="${x-14*k}" y="${y-h+22*k}" width="${28*k}" height="${28*k}" rx="4" fill="${Y}" opacity=".7"/>`)+`</g>`});
  return g+`<rect y="1860" width="1080" height="60" fill="${DG}" opacity=".5"/>`;
}
function REEL(out,t,cur){
  // 各アプリの文字・ボタンが重なる所には大事なものを置かない（安全な範囲: 上210〜下1430。部品どうし（ロゴ・見出し・場面・名前・字幕）は 20px 以上あけて重ねない。字幕とエンディングは左右対称の x 140〜940 にして右のボタン列をよける）
  // 下（約1440より下）はアプリのチャンネル名・説明・関連動画、右はいいね等のボタン、上は再生ボタン類が重なる
  const VY=530,S=1080/1920,CH=880,CX=540;  // CH: 本編のうち見せる高さ（下の字幕帯の部分は切る）
  let r=`<rect width="1080" height="1920" fill="${G}"/>`;
  for(let k=0;k<10;k++){const x=((k*240+t*60)%2600)-500;r+=`<path d="M${x} 1920 L${x+700} 0" stroke="#fff" stroke-width="44" opacity=".05"/>`}
  r+=SKY();
  r+=`<rect width="1080" height="16" fill="${T}"/><rect y="1904" width="1080" height="16" fill="${Y}"/>`;
  const B0=r.length;  // ここから前景（表紙では下にずらす）
  r+=`<g data-reel="ロゴ" transform="translate(540,250)"><rect x="-300" y="-46" width="600" height="92" rx="46" fill="#fff"/>${MARK(-238,0,.95)}<text x="22" y="17" text-anchor="middle" font-size="46" font-weight="900" fill="${G}">アキヤド <tspan fill="${T}">民泊school</tspan></text></g>`;
  r+=`<g data-reel="見出し" data-text="1">`;REEL_TITLE.split('\n').forEach((ln,k,a)=>{r+=`<text x="540" y="${400+k*92-(a.length-1)*0}" text-anchor="middle" font-size="80" font-weight="900" fill="#fff" stroke="${DG}" stroke-width="14" paint-order="stroke" stroke-linejoin="round">${ln}</text>`});r+=`</g>`;
  r+=`<rect data-reel="場面" x="0" y="${VY-6}" width="1080" height="${CH*S+12}" fill="#fff"/><clipPath id="reelclip"><rect x="0" y="${VY}" width="1080" height="${CH*S}"/></clipPath><g clip-path="url(#reelclip)"><g transform="translate(0,${VY}) scale(${S})">${out}</g></g>`;
  if(cur){const o=clamp((t-cur[0]+.05)/.15)*clamp((cur[1]+.25-t)/.15),lines=REEL_SUBS[LINES.indexOf(cur)]||reelWrap(cur[3].join(''),13),y0=1124,LH=Math.min(76,282/Math.max(1,lines.length)),FS=Math.min(52,LH*.7,740/Math.max(...lines.map(l=>l.length)));  // 字幕の箱は下1430まで。行が多いときは字を小さくして収める
    const nm=VNAME[cur[2]]||'';
    r+=`<g opacity="${o}"><rect data-reel="字幕" x="140" y="${y0-40}" width="800" height="${lines.length*LH+64}" rx="36" fill="#fff"/>`+(nm?`<rect data-reel="名前" x="166" y="${y0-72}" width="${nm.length*36+60}" height="64" rx="32" fill="${VCOL[cur[2]]||T}"/><text x="${196+nm.length*18}" y="${y0-29}" text-anchor="middle" font-size="36" font-weight="900" fill="#fff">${nm}</text>`:'')+lines.map((s,i)=>`<text x="${CX}" y="${y0+48+i*LH}" text-anchor="middle" font-size="${FS}" font-weight="900" fill="${DG}">${s}</text>`).join('')+`</g>`;}
  // 表紙: Instagram のプロフィール一覧は縦長の上下を切って 3:4（y 240〜1680）で見せるので、前景を 110 下げて、見出し〜字幕を y 320〜1570 に収める
  if(typeof REEL_COVER!=='undefined')r=r.slice(0,B0)+`<g transform="translate(0,110)">`+r.slice(B0)+`</g>`;
  // エンディング（最後の約3秒）：「続きは本編で」
  const e=clamp((t-REEL_T1)/.35);
  if(e>0){const ep=(typeof EP_TITLE!=='undefined'?EP_TITLE:REEL_TITLE.replace('\n',''));
    r+=`<g opacity="${e}"><rect width="1080" height="1920" fill="${G}"/>`;
    for(let k=0;k<10;k++){const x=((k*240+t*60)%2600)-500;r+=`<path d="M${x} 1920 L${x+700} 0" stroke="#fff" stroke-width="44" opacity=".06"/>`}
    r+=SKY()+`<rect width="1080" height="16" fill="${T}"/><rect y="1904" width="1080" height="16" fill="${Y}"/>`;
    r+=pop(CX,560,clamp((t-REEL_T1-.1)/.5),`<circle cx="${CX}" cy="560" r="130" fill="#fff"/>${MARK(CX,560,2.9)}`);
    r+=pop(CX,830,clamp((t-REEL_T1-.35)/.5),`<text x="${CX}" y="860" text-anchor="middle" font-size="110" font-weight="900" fill="#fff" stroke="${DG}" stroke-width="14" paint-order="stroke" stroke-linejoin="round">続きは本編で</text>`);
    r+=pop(CX,1040,clamp((t-REEL_T1-.6)/.5),`<rect x="140" y="950" width="800" height="190" rx="40" fill="#fff"/><text x="${CX}" y="1022" text-anchor="middle" font-size="40" font-weight="900" fill="${T}">YouTube「アキヤド 民泊school」</text><text x="${CX}" y="1094" text-anchor="middle" font-size="${ep.length>16?34:ep.length>14?38:44}" font-weight="900" fill="${DG}">${ep}</text>`);
    r+=pop(CX,1230,clamp((t-REEL_T1-.85)/.5),`<rect x="${CX-300}" y="1175" width="600" height="110" rx="55" fill="${T}"/><text x="${CX}" y="1248" text-anchor="middle" font-size="52" font-weight="900" fill="#fff">▶ 本編を見る</text>`);
    r+=fade(clamp((t-REEL_T1-1.1)/.5),`<text x="${CX}" y="1360" text-anchor="middle" font-size="38" font-weight="900" fill="#fff">プロフィール・概要欄のリンクから</text>`,0);
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
    cover_only = "--cover-only" in args  # 表紙だけ作り直す（動画は書き出さない）
    if cover_only:
        args.remove("--cover-only")
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
    js = js.replace("if (mode === 'preview') {", """if (mode === 'check') {  // 部品どうしの重なり（20px 未満の近さも）と、安全な範囲（上200〜下1440）からのはみ出しを調べる
    const bad = [];
    for (const t of JSON.parse(arg)) { await p.evaluate((t) => window.draw(t), t); await p.waitForTimeout(30);
      bad.push(...await p.evaluate((t) => { const el = [...document.querySelectorAll('[data-reel]')].filter(e => e.closest('[opacity="0"]') === null).map(e => { const r = e.getBoundingClientRect(); return { k: e.dataset.reel, tx: !!e.dataset.text, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom }; });
        const out = [];
        for (let i = 0; i < el.length; i++) { const a = el[i]; if (a.y0 < 200 || a.y1 > 1440) out.push(t.toFixed(1) + '秒: ' + a.k + ' が安全な範囲の外（y ' + Math.round(a.y0) + '〜' + Math.round(a.y1) + '）');
          for (let j = i + 1; j < el.length; j++) { const b = el[j]; if (a.k === '字幕' && b.k === '名前' || a.k === '名前' && b.k === '字幕') continue;
            const g = (a.tx || b.tx) ? 0 : 20;  /* 文字は行の高さの余白を含むので、重ならなければよい。箱どうしは 20px あける */ if (a.x0 < b.x1 && b.x0 < a.x1 && a.y0 < b.y1 + g && b.y0 < a.y1 + g) out.push(t.toFixed(1) + '秒: ' + a.k + ' と ' + b.k + ' が近すぎる・重なっている'); } }
        return out; }, t)); }
    console.log(JSON.stringify(bad));
  } else if (mode === 'preview') {""")
    js = js.replace("width: 1920, height: 1080", "width: 1080, height: 1920").replace("i / 24", f"{t0} + i / 24").replace("window.draw(t), t)", f"window.draw({t0}+t), t)")
    env = dict(os.environ); env["ROOT_DIR"] = ROOT
    env["NODE_PATH"] = os.pathsep.join(p for p in ["/opt/node-tools/node_modules", os.path.join(ROOT, "tools", "check", "node_modules"), env.get("NODE_PATH", "")] if p)
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "a.html"); open(h, "w", encoding="utf-8").write(html)
        j = os.path.join(tmp, "r.js"); open(j, "w").write(js)
        def make_cover(tmp):
            # 表紙（--cover の秒のコマ）。動画のコマをそのまま使わず、Instagram の一覧（3:4 に切られる）でも見出しが切れない配置で別に描く
            cover = os.path.splitext(out)[0] + "-cover.jpg"
            hc = os.path.join(tmp, "c.html"); open(hc, "w", encoding="utf-8").write(html.replace("const REEL_TITLE=", "const REEL_COVER=true;const REEL_TITLE=", 1))
            cd = os.path.join(tmp, "cover"); os.makedirs(cd)
            subprocess.run(["node", j, hc, cd, "preview", json.dumps([cover_t, cover_t])], check=True, env=env)  # 2回描く（1回目で文字の読み込みを済ませる）
            png = [os.path.join(cd, f) for f in os.listdir(cd) if f.endswith(".png")][0]
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", png, "-q:v", "2", cover], check=True)
        def check_layout(tmp):
            # 自動点検: 動画のセリフごとの真ん中と表紙で、部品の重なり・近すぎ・安全な範囲からのはみ出しを調べる（0件でなければ止める）
            ts_ = [round((l[0] + l[1]) / 2 - t0, 2) for l in lines if t0 <= l[0] < t1]
            hc = os.path.join(tmp, "k.html"); open(hc, "w", encoding="utf-8").write(html)
            r = subprocess.run(["node", j, hc, tmp, "check", json.dumps(ts_)], check=True, env=env, capture_output=True, text=True)
            hc2 = os.path.join(tmp, "k2.html"); open(hc2, "w", encoding="utf-8").write(html.replace("const REEL_TITLE=", "const REEL_COVER=true;const REEL_TITLE=", 1))
            r2 = subprocess.run(["node", j, hc2, tmp, "check", json.dumps([cover_t])], check=True, env=env, capture_output=True, text=True)
            bad = json.loads(r.stdout.strip().splitlines()[-1]) + ["表紙 " + x for x in json.loads(r2.stdout.strip().splitlines()[-1]) if "安全な範囲" not in x]
            if bad:
                sys.exit("リールの配置の自動点検で問題が見つかりました:\n  " + "\n  ".join(bad))
            print("配置の自動点検: 0件（重なり・近すぎ・はみ出しなし）")
        check_layout(tmp)
        if cover_only:
            make_cover(tmp); print(os.path.splitext(out)[0] + "-cover.jpg"); return
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
        make_cover(tmp)
    print(out, round(t1 - t0 + END, 1), "秒")


if __name__ == "__main__":
    main()
