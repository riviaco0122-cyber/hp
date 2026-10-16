"""サービスページの見出しの図（私たちについての日本地図と同じ「点で描く」表現）

深い緑の面に、細かな白い点で事業を象徴する形を描き、ところどころを朱の点で灯す。
build.py の service_page() から art_svg(key) を呼ぶ。動きは css/style.css の .sdots__*。
"""
import math

S = 900      # 図の大きさ（正方形）
STEP = 13    # 点の間隔


def _grid():
    for y in range(STEP // 2, S, STEP):
        for x in range(STEP // 2, S, STEP):
            yield x, y


def _in_poly(x, y, poly):
    hit, j = False, len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


def _rect(x, y, x0, y0, x1, y1):
    return x0 <= x <= x1 and y0 <= y <= y1


def _house(x, y):
    """空き家再生：古民家（大きな屋根と母屋）。窓に灯り"""
    roof = [(90, 430), (450, 150), (810, 430)]
    body = _rect(x, y, 170, 430, 730, 760)
    ground = 790 <= y <= 800 and 40 <= x <= 860
    inside = _in_poly(x, y, roof) or body or ground
    door = _rect(x, y, 400, 560, 500, 760)
    win = _rect(x, y, 230, 500, 340, 600) or _rect(x, y, 560, 500, 670, 600)
    if door:
        return None
    if win:
        return "accent"
    return "base" if inside else None


def _calendar(x, y):
    """開業・運営支援：予約のカレンダー（7列×5段）。埋まった日が朱に灯る"""
    x0, y0, cell, gap = 80, 170, 92, 14
    booked = {(1, 0), (2, 0), (5, 0), (6, 0), (0, 1), (4, 1), (5, 1), (6, 1), (2, 2), (3, 2), (5, 2), (6, 2),
              (0, 3), (1, 3), (4, 3), (5, 3), (6, 3), (3, 4), (5, 4), (6, 4)}
    if 90 <= y <= 130 and 80 <= x <= 820:   # 見出しの帯
        return "base"
    for r in range(5):
        for c in range(7):
            cx, cy = x0 + c * (cell + gap), y0 + r * (cell + gap)
            if _rect(x, y, cx, cy, cx + cell, cy + cell):
                edge = x - cx < STEP or cx + cell - x < STEP or y - cy < STEP or cy + cell - y < STEP
                if (c, r) in booked:
                    return "accent"
                return "base" if edge else None
    return None


def _venn(x, y):
    """不動産事業者様との協業：物件・事業者・RIVIA の3つの円。重なる真ん中が朱"""
    cs = [(330, 360), (570, 360), (450, 570)]
    inn = [math.hypot(x - cx, y - cy) <= 230 for cx, cy in cs]
    ring = [abs(math.hypot(x - cx, y - cy) - 230) <= 8 for cx, cy in cs]
    if all(inn):
        return "accent"
    if any(ring):
        return "base"
    return None


def _waves(x, y):
    """WEB集客：一点から広がる波紋。波の先に届いた点が朱に灯る"""
    ox, oy = 120, 780
    d = math.hypot(x - ox, y - oy)
    if d < 30:
        return "accent"
    ang = math.degrees(math.atan2(oy - y, x - ox))
    if not (-5 <= ang <= 95):
        return None
    for k, r in enumerate((150, 290, 430, 570, 710)):
        if abs(d - r) <= 7:
            return "accent" if k == 4 and int(ang) % 17 < 4 else "base"
    return None


def _people(x, y):
    """WEB採用：並んだ人の形。出会えた人が朱に灯る"""
    match = {(1, 0), (3, 1), (0, 2)}
    for r in range(3):
        for c in range(4):
            cx, cy = 150 + c * 200, 180 + r * 240
            head = math.hypot(x - cx, y - cy) <= 40
            body = (y - (cy + 120)) ** 2 / 70 ** 2 + (x - cx) ** 2 / 80 ** 2 <= 1 and y <= cy + 120
            if head or body:
                return "accent" if (c, r) in match else "base"
    return None


SHAPES = {"operation": _house, "management": _calendar, "partnership": _venn, "marketing": _waves, "recruit": _people}


def art_svg(key):
    f = SHAPES[key]
    base, accent = [], []
    for x, y in _grid():
        k = f(x, y)
        if k == "base":
            base.append(f'<circle cx="{x}" cy="{y}" r="2.6"/>')
        elif k == "accent":
            accent.append(f'<circle style="--d:{(x + y) % 900 / 300:.2f}s" cx="{x}" cy="{y}" r="3.2"/>')
    return (f'<svg class="sdots sdots--{key}" viewBox="0 0 {S} {S}" aria-hidden="true">'
            f'<g class="sdots__base">{"".join(base)}</g><g class="sdots__accent">{"".join(accent)}</g></svg>')


if __name__ == "__main__":
    for k in SHAPES:
        print(k, len(art_svg(k)))
