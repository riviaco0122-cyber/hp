#!/usr/bin/env python3
"""2つのフォルダのスクリーンショット（同じファイル名の PNG）を比べ、差分の割合を JSON で出す。
tools/check/site_check.js の見た目の回帰テストから呼ぶ（単体でも使える）。

使い方: python3 tools/check/img_diff.py <基準のフォルダ> <比べるフォルダ> <差分画像の出力フォルダ>
出力（標準出力・JSON）: [{"name": ..., "ratio": 0.0123, "base_h": ..., "cur_h": ..., "diff": "差分画像のパス"}, ...]

差分の割合 = 色が変わった画素（RGB のどれかが 32 以上違う）＋高さの違いではみ出した部分 ÷ 大きいほうの画像の面積。
差分画像は、変わった画素を赤で塗り、元の画像（作業ブランチ）を薄くして重ねたもの。
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

THRESHOLD = 32


def compare(base_path, cur_path, out_path):
    a = Image.open(base_path).convert("RGB")
    b = Image.open(cur_path).convert("RGB")
    w = max(a.width, b.width)
    h = max(a.height, b.height)
    ow, oh = min(a.width, b.width), min(a.height, b.height)
    diff = ImageChops.difference(a.crop((0, 0, ow, oh)), b.crop((0, 0, ow, oh)))
    # どれかのチャンネルが THRESHOLD 以上違えば「変わった」画素とする
    r, g, bl = diff.split()
    mask = ImageChops.lighter(ImageChops.lighter(r, g), bl).point(lambda v: 255 if v >= THRESHOLD else 0)
    changed = mask.histogram()[255]
    outside = w * h - ow * oh  # 高さ（幅）の違いではみ出した部分は、すべて変わったものとして数える
    ratio = (changed + outside) / float(w * h) if w * h else 0.0
    if out_path:
        canvas = Image.new("RGB", (w, h), (255, 0, 0))
        faded = Image.blend(b, Image.new("RGB", b.size, (255, 255, 255)), 0.7)
        canvas.paste(faded, (0, 0))
        red = Image.new("RGB", (ow, oh), (255, 0, 0))
        region = canvas.crop((0, 0, ow, oh))
        region.paste(red, (0, 0), mask)
        canvas.paste(region, (0, 0))
        canvas.save(out_path)
    return ratio, a.height, b.height


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    base, cur, out = (Path(x) for x in sys.argv[1:4])
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted(cur.glob("*.png")):
        bf = base / f.name
        if not bf.is_file():
            rows.append({"name": f.name, "ratio": None, "note": "基準（本番ブランチ）のスクリーンショットがない"})
            continue
        dp = out / f.name
        ratio, bh, ch = compare(bf, f, dp)
        rows.append({"name": f.name, "ratio": round(ratio, 4), "base_h": bh, "cur_h": ch, "diff": str(dp)})
    print(json.dumps(rows, ensure_ascii=False))


if __name__ == "__main__":
    main()
