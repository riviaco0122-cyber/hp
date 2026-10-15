"""「私たちについて」の見出しの日本地図（点で描いた日本と、拠点から全国へ伸びる線）

- 地図の形: tools/data/japan.json（Natural Earth 1:50m、パブリックドメイン）
- 点の地図は images/about/japan-dots.svg に書き出す（`python3 tools/japan_map.py`）
- 拠点の印と全国へ伸びる線は、build.py が overlay_svg() でページに直接書く（CSS で動かすため）
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LON0, LAT0, LAT1 = 127.5, 30.0, 45.8   # 地図に入れる範囲（西端・南端・北端）
LON1 = 146.2
K = 60                                  # 1度あたりの大きさ
COS = math.cos(math.radians(36))        # 経度方向の縮み（日本の中ほどの緯度）
W = round((LON1 - LON0) * COS * K)
H = round((LAT1 - LAT0) * K)
STEP = 11                               # 点の間隔

# 拠点（東京・静岡）と、線を伸ばす先（全国のイメージ。特定の案件の場所ではない）
BASES = [("Tokyo", "東京", 139.69, 35.69), ("Shizuoka", "静岡", 138.38, 34.98)]
REACH = [(141.35, 43.06), (140.87, 38.27), (140.10, 39.72), (136.66, 36.56), (135.77, 35.01),
         (132.46, 34.40), (133.53, 33.56), (130.40, 33.59), (130.56, 31.60), (138.19, 36.65)]


def project(lon, lat):
    return ((lon - LON0) * COS * K, (LAT1 - lat) * K)


def _polygons():
    with open(os.path.join(ROOT, "tools", "data", "japan.json"), encoding="utf-8") as f:
        return [[project(x, y) for x, y in p] for p in json.load(f)["polygons"]]


def _inside(x, y, poly):
    hit = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


def dots():
    polys = _polygons()
    out = []
    for gy in range(STEP // 2, H, STEP):
        for gx in range(STEP // 2, W, STEP):
            if any(_inside(gx, gy, p) for p in polys):
                out.append((gx, gy))
    return out


def dots_svg():
    circles = "".join(f'<circle cx="{x}" cy="{y}" r="2.6"/>' for x, y in dots())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<g fill="#ffffff" fill-opacity="0.32">{circles}</g></svg>\n')


def overlay_svg():
    """拠点の印と、拠点から全国へ伸びる弧（ページに直接書き、CSS で動かす）"""
    bx = [project(lon, lat) for _, _, lon, lat in BASES]
    arcs = []
    for i, (lon, lat) in enumerate(REACH):
        sx, sy = bx[i % len(bx)]
        tx, ty = project(lon, lat)
        mx, my = (sx + tx) / 2, (sy + ty) / 2
        dx, dy = tx - sx, ty - sy
        d = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / d * d * 0.22, my + dx / d * d * 0.22  # 少しふくらませた弧
        arcs.append(f'<path class="jmap__arc" style="--i:{i}" pathLength="1" d="M{sx:.0f} {sy:.0f}Q{cx:.0f} {cy:.0f} {tx:.0f} {ty:.0f}"/>'
                    f'<circle class="jmap__dot" style="--i:{i}" cx="{tx:.0f}" cy="{ty:.0f}" r="5"/>')
    bases = "".join(
        f'<g class="jmap__base" transform="translate({x:.0f} {y:.0f})"><circle class="jmap__pulse" r="12"/><circle r="8"/>'
        f'<text x="{-18 if en == "Shizuoka" else 18}" y="{30 if en == "Shizuoka" else -14}" text-anchor="{"end" if en == "Shizuoka" else "start"}">{en.upper()}</text></g>'
        for (en, _ja, _lo, _la), (x, y) in zip(BASES, bx))
    return (f'<svg class="jmap__over" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(arcs)}{bases}</svg>')


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "images", "about"), exist_ok=True)
    path = os.path.join(ROOT, "images", "about", "japan-dots.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(dots_svg())
    print(path, W, H, len(dots()), "dots")
