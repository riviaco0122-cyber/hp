#!/usr/bin/env python3
"""書き出した動画から、「主役がほぼ変わらない区間」を探す（話に画面が合っているかの点検。manual.md 4-3章・1-4章⑤）。

連続するコマの差を計算する。見る範囲は、図の主要部（人物と字幕・左上の札・右上の進行表示を除いた中央〜右）。
  - 基準のコマと比べて、「大きく違う画素」が一定の割合を超えたら「主役が変わった」と数え、基準を取り直す。
  - 変わらない時間が --max 秒（既定 8）以上続いたら、その区間を出す。
  - 浮遊・きらめき・雲・太陽・暖簾のゆれなど、小さな動きは「変化」に数えない（割合が小さい。--thr で変える）。
使い方: python3 tools/video/static_check.py 動画.mp4 [--max 8] [--thr 0.012] [--fps 4]
終了コード: 検出が 1 件でもあれば 1。
"""
import subprocess, sys
import numpy as np

W, H = 192, 108

def main():
    a = sys.argv[1:]
    def opt(n, d):
        return type(d)(a[a.index(n) + 1]) if n in a else d
    path = a[0]; mx = opt("--max", 8.0); thr = opt("--thr", 0.012); fps = opt("--fps", 4)
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
    # 見る範囲: 左の人物（x<30%）・字幕の帯（y>76%）・上の札と進行表示（y<14%）を除く
    x0, x1, y0, y1 = int(W * .30), W, int(H * .14), int(H * .76)
    reg = fr[:, y0:y1, x0:x1]
    anchor = 0; out = []; t_open = 3.6  # オープニングは数えない
    start = int(t_open * fps); anchor = start
    last_change = start
    for i in range(start + 1, len(reg)):
        d = (np.abs(reg[i] - reg[anchor]) > 50).mean()
        if d > thr:
            if (i - last_change) / fps >= mx:
                out.append((last_change / fps, i / fps))
            anchor = i; last_change = i
    if (len(reg) - last_change) / fps >= mx:
        out.append((last_change / fps, len(reg) / fps))
    for s, e in out:
        print(f"{s:7.1f}〜{e:7.1f}秒 ({e - s:.1f}秒)  主役がほぼ変わらない")
    print(f"静止区間の点検（{mx:.0f}秒以上・{len(reg)/fps:.0f}秒の動画）: {len(out)} 件")
    sys.exit(1 if out else 0)

if __name__ == "__main__":
    main()
