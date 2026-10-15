#!/usr/bin/env python3
"""アキヤドのサービス紹介動画（約35秒・1920×1080・字幕つき・BGMつき）を作る。

使い方: python3 tools/video/make_intro.py [出力先.mp4]
- 映像: 場面ごとに「背景の写真（ゆっくり拡大）＋文字（Playwright で透明PNGに描く）」を ffmpeg で重ね、場面をクロスフェードでつなぐ。
- BGM: Python で合成（やわらかいコードとアルペジオ。既存の曲は使わない＝著作権の問題なし）。
- 文言は、サイトに載っているサービスの説明（tools/build.py の MEDIA_SERVICES）と、取材事例の件数だけを使う。数字を作らない。
- 必要なもの: ffmpeg、Node.js と playwright（tools/check と同じ）。書体は Google Fonts から読み込む。
"""
import json, math, os, struct, subprocess, sys, tempfile, wave, array, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "media", "akiyado-service-intro.mp4")
FPS = 30
XF = 0.6  # クロスフェードの秒数

MARK = ('<svg viewBox="0 0 32 32" width="64" height="64"><rect width="32" height="32" rx="9" fill="#2E6B47"/>'
        '<path d="M7.5 15.6 16 8.6l8.5 7v8.6a1.3 1.3 0 0 1-1.3 1.3h-4.7v-5.7h-5v5.7H8.8a1.3 1.3 0 0 1-1.3-1.3z" fill="#fff"/></svg>')
LOGO = f'<div class="logo">{MARK}<span>アキヤド</span><small>空き家と民泊のメディア</small></div>'

# 場面: (秒, 背景(写真名 or #色), 本文のHTML)
SCENES = [
    (5.0, "old-town-street", '<div class="big">空き家を、売る。<br>活かす。<br><em>民泊を、はじめる。</em></div>'),
    (5.0, "riverside-town", '<div class="mid">空き家と民泊のメディア</div><div class="big">アキヤド</div><div class="sub">悩みの順に、お答えします。</div>'),
    (5.6, "thatched-house", '<div class="tag">空き家を売りたい方へ</div><div class="big s">アキヤド買取プラン</div><div class="sub">「宿として再生できるか」という目で、物件を見ます。<br>一般の仲介では値段がつきにくい家も、<br>ご相談ください。</div>'),
    (5.6, "irori-room", '<div class="tag">空き家を活かしたい方へ</div><div class="big s">アキヤド借り上げプラン</div><div class="sub">アキヤドが借り上げ、改修から宿の運営まで行います。<br>運営の手間をかけず、家賃を受け取れます。</div>'),
    (5.6, "white-bedroom", '<div class="tag">副業で宿をはじめたい方へ</div><div class="big s">アキヤド開業・運営プラン</div><div class="sub">物件選び、許可や届出、集客まで。<br>実際に宿を運営しているアキヤドが、<br>任せたい範囲に合わせて支えます。</div>'),
    (4.8, "#1f3a2b", '<div class="mid light">取材した、6人のオーナーの事例も公開中</div><div class="avs">{AVS}</div><div class="sub light">初期費用・月商・純利益を、オーナーの申告の数字で。</div>'),
    (4.8, "#f4f1ea", '<div class="big dark">まずは、<em>無料</em>でご相談ください。</div><div class="sub dark">相談・お見積りは無料、全国対応です。</div><div class="url">rivia-co.com</div>'),
]

CSS = """
@import url("https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700&family=Zen+Kaku+Gothic+New:wght@700;900&family=Shippori+Mincho+B1:wght@800&display=block");
*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;background:transparent;overflow:hidden;font-family:"Zen Maru Gothic",sans-serif;-webkit-font-smoothing:antialiased}
.f{position:relative;width:1920px;height:1080px;color:#fff}
.f.photo::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,24,18,.86) 0%,rgba(14,24,18,.68) 46%,rgba(14,24,18,.10) 90%)}
.t{position:absolute;left:150px;top:0;bottom:150px;width:1560px;display:flex;flex-direction:column;justify-content:center}
.f.center .t{left:0;right:0;width:auto;align-items:center;text-align:center}
.big{font-family:"Shippori Mincho B1",serif;font-weight:800;font-size:128px;line-height:1.28;letter-spacing:.06em}
.big.s{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:92px;letter-spacing:.03em;margin-top:26px}
.big em{font-style:normal;color:#f0b35a}.big.dark{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:104px;color:#1f3a2b}.big.dark em{color:#c95a35}
.mid{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:700;font-size:54px;letter-spacing:.12em;margin-bottom:18px}.mid.light{margin-bottom:46px}
.sub{margin-top:38px;font-size:48px;line-height:1.7;font-weight:500;letter-spacing:.05em}.sub.light{color:#e8efe9}.sub.dark{color:#3a4a41}
.tag{align-self:flex-start;padding:10px 30px 12px;background:#c95a35;color:#fff;font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:44px;letter-spacing:.1em}
.avs{display:flex;gap:34px;justify-content:center}.avs i{display:block;width:190px;height:190px;border-radius:50%;background:#fff center/cover no-repeat;box-shadow:0 0 0 6px #fff}
.url{margin-top:54px;padding:14px 48px 18px;background:#c95a35;color:#fff;font-family:"Zen Kaku Gothic New",sans-serif;font-weight:900;font-size:56px;letter-spacing:.08em}
.logo{position:absolute;left:150px;bottom:70px;display:flex;align-items:center;gap:20px;font-size:46px;font-weight:700;letter-spacing:.14em}.logo small{font-size:28px;font-weight:500;letter-spacing:.1em;opacity:.85}
.f.centerlogo .logo{left:0;right:0;justify-content:center}.f.dark .logo{color:#1f3a2b}
"""


def overlay_html(i, body, bg):
    avs = ""
    if "{AVS}" in body:
        avs = "".join(f'<i style="background-image:url(\'file://{ROOT}/images/portraits/circle/user_0{n}.png\')"></i>' for n in (1, 2, 3, 6, 4, 5))
        body = body.replace("{AVS}", avs)
    cls = "f photo" if not bg.startswith("#") else ("f center centerlogo" + (" dark" if bg == "#f4f1ea" else ""))
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="{cls}"><div class="t">{body}</div>{LOGO}</div></body></html>'


RENDER_JS = """
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const [src, out] of jobs) {
    await p.goto('file://' + src);
    await p.evaluate(async () => { await document.fonts.ready; });
    await p.waitForTimeout(300);
    await p.screenshot({ path: out, omitBackground: true });
  }
  await b.close();
})();
"""


def synth_bgm(path, dur):
    """やわらかい和音（パッド）と、ゆっくりしたアルペジオ。約78BPM。numpy で合成する。"""
    import numpy as np
    sr = 32000
    n = int(dur * sr)
    L = np.zeros(n); R = np.zeros(n)
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    beat = 60 / 78
    chords = [[48, 52, 55, 59], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 53]]  # Cmaj7 Am7 Fmaj7 G7(軽く)
    bar = beat * 4
    t, c = 0.0, 0
    while t < dur:
        ch = chords[c % 4]
        ln = int(min(bar + 1.2, dur - t + 1.2) * sr)
        tt = np.arange(ln) / sr
        env = np.minimum(1.0, tt / 0.9) * np.where(tt < bar, 1.0, np.clip(1 - (tt - bar) / 1.2, 0, 1))
        s0 = int(t * sr)
        for m in ch:
            f = hz(m)
            v = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2 * tt + 0.3) + 0.12 * np.sin(2 * np.pi * f * 3 * tt)) * env * 0.045
            e = min(n, s0 + ln)
            L[s0:e] += v[: e - s0]; R[s0:e] += v[: e - s0]
        arp = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 12, ch[1] + 12, ch[3] + 12, ch[2] + 12, ch[0] + 24]
        for j, m in enumerate(arp):
            f = hz(m)
            a0 = int((t + j * beat / 2) * sr)
            ln2 = int(1.4 * sr)
            tt2 = np.arange(ln2) / sr
            env2 = np.exp(-tt2 * 3.2) * np.minimum(1.0, tt2 / 0.01)
            v = (np.sin(2 * np.pi * f * tt2) + 0.3 * np.sin(2 * np.pi * f * 2 * tt2)) * env2 * 0.05
            pan = 0.35 + 0.3 * (j % 2)
            e = min(n, a0 + ln2)
            if a0 < n:
                L[a0:e] += v[: e - a0] * (1 - pan) * 1.4; R[a0:e] += v[: e - a0] * pan * 1.4
        t += bar; c += 1
    d1, d2 = int(0.31 * sr), int(0.47 * sr)
    L2, R2 = L.copy(), R.copy()
    L2[d1:] += 0.28 * L[:-d1]; R2[d1:] += 0.28 * R[:-d1]
    L2[d2:] += 0.16 * R[:-d2]; R2[d2:] += 0.16 * L[:-d2]
    peak = max(np.abs(L2).max(), np.abs(R2).max()) or 1.0
    g = 0.7 / peak
    idx = np.arange(n)
    e = np.minimum(1.0, np.minimum(idx / int(1.5 * sr), (n - idx) / int(2.5 * sr)))
    st = np.empty(n * 2, dtype=np.int16)
    st[0::2] = np.clip(L2 * g * e, -1, 1) * 32767
    st[1::2] = np.clip(R2 * g * e, -1, 1) * 32767
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(st.tobytes())


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        jobs, ov = [], []
        for i, (d, bg, body) in enumerate(SCENES):
            src = os.path.join(tmp, f"s{i}.html")
            open(src, "w", encoding="utf-8").write(overlay_html(i, body, bg))
            png = os.path.join(tmp, f"o{i}.png")
            jobs.append([src, png]); ov.append(png)
        js = os.path.join(tmp, "r.js"); open(js, "w").write(RENDER_JS)
        env = dict(os.environ)
        env["NODE_PATH"] = os.pathsep.join(p for p in ["/opt/node-tools/node_modules", os.path.join(ROOT, "tools", "check", "node_modules"), env.get("NODE_PATH", "")] if p)
        subprocess.run(["node", js, json.dumps(jobs)], check=True, env=env)
        clips = []
        for i, (d, bg, body) in enumerate(SCENES):
            clip = os.path.join(tmp, f"c{i}.mp4")
            dur = d + XF  # 次の場面と重ねる分
            frames = int(dur * FPS)
            if bg.startswith("#"):
                inputs = ["-f", "lavfi", "-t", f"{dur}", "-i", f"color=c={bg}:s=1920x1080:r={FPS}"]
                base = "[0:v]format=yuv420p[b]"
            else:
                inputs = ["-i", os.path.join(ROOT, "images", "photos", bg + ".jpg")]
                base = (f"[0:v]scale=2200:-1,crop=2200:1238,zoompan=z='1+0.00035*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={FPS},format=yuv420p[b]")
            fl = (f"{base};[1:v]format=rgba,fade=t=in:st=0.5:d=0.9:alpha=1[o];[b][o]overlay=0:0:format=auto,format=yuv420p[v]")
            cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-loop", "1", "-t", f"{dur}", "-i", ov[i], "-filter_complex", fl, "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", clip]
            subprocess.run(cmd, check=True)
            clips.append(clip)
        # クロスフェードでつなぐ
        total = sum(d for d, _, _ in SCENES) + XF
        ins = []
        for c in clips: ins += ["-i", c]
        fl = ""; last = "[0:v]"; off = 0.0
        for i in range(1, len(clips)):
            off += SCENES[i - 1][0]
            fl += f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off}[x{i}];"
            last = f"[x{i}]"
        merged = os.path.join(tmp, "m.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", fl.rstrip(";"), "-map", last.replace("[", "[").strip(), "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", merged], check=True)
        wav = os.path.join(tmp, "bgm.wav")
        synth_bgm(wav, total)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", merged, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT], check=True)
    print(OUT, round(total, 1), "秒")


if __name__ == "__main__":
    main()
