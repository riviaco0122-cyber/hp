"""サービスページの見出しの背景（写真の代わりに、深い緑の面に事業ごとの線画を描く）

文字が写真の色と重なって読みにくかったため、私たちについての日本地図と同じ方針で、
暗い面に細い線と朱の点だけの図を描く。線は控えめにし、文字の読みやすさを優先する。
build.py の service_page() から art_svg(key) を呼ぶ。動きは css/style.css の .hart__*。
"""
import random

W, H = 1600, 900


def _svg(inner, key):
    return (f'<svg class="hart hart--{key}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'{inner}</svg>')


def _town():
    """空き家再生：家並みの線画。窓に朱の灯りが順にともる（眠っていた家が、また使われる）"""
    rnd = random.Random(7)
    out, wins = [], []
    x = -40
    i = 0
    while x < W + 40:
        w = rnd.choice([120, 150, 180, 210])
        h = rnd.choice([120, 150, 180])
        roof = rnd.choice([50, 64, 80])
        base = H - 40
        top = base - h
        out.append(f'<path class="hart__line" d="M{x} {base}V{top}L{x + w / 2:.0f} {top - roof}L{x + w} {top}V{base}"/>')
        for wx in (x + w * 0.22, x + w * 0.58):
            lit = rnd.random() < 0.35
            cls = "hart__win is-lit" if lit else "hart__win"
            wins.append(f'<rect class="{cls}" style="--i:{i}" x="{wx:.0f}" y="{top + h * 0.28:.0f}" width="{w * 0.2:.0f}" height="{h * 0.22:.0f}"/>')
            i += 1
        x += w + rnd.choice([16, 24, 36])
    ground = f'<path class="hart__line" d="M0 {H - 40}H{W}"/>'
    return "".join(out) + ground + "".join(wins)


def _calendar():
    """開業・運営支援：予約のカレンダー。マスが少しずつ埋まっていく（宿が回り始める）"""
    rnd = random.Random(11)
    size, gap = 54, 14
    out = []
    i = 0
    cols = W // (size + gap) + 1
    rows = H // (size + gap) + 1
    for r in range(rows):
        for c in range(cols):
            x, y = c * (size + gap) + 10, r * (size + gap) + 10
            # 右下ほど埋まる（運営が進むイメージ）。左上の文字のあたりは空ける
            p = 0.04 + 0.2 * (c / cols) * (r / rows) * 2
            booked = rnd.random() < p and not (c < cols * 0.45 and r < rows * 0.75)
            cls = "hart__cell is-booked" if booked else "hart__cell"
            out.append(f'<rect class="{cls}" style="--i:{i % 23}" x="{x}" y="{y}" width="{size}" height="{size}" rx="10"/>')
            i += 1
    return "".join(out)


def _triangle():
    """不動産事業者様との協業：オーナー・事業者・RIVIA・ゲストを結ぶ線を、光の点が行き来する"""
    nodes = [(780, 300, "PROPERTY"), (1120, 520, "RIVIA"), (820, 780, "GUEST"), (1200, 150, "PARTNER")]
    out = []
    pairs = [(0, 1), (1, 2), (2, 0), (3, 1), (3, 0)]
    for k, (a, b) in enumerate(pairs):
        (x1, y1, _), (x2, y2, _) = nodes[a], nodes[b]
        mx, my = (x1 + x2) / 2 + (y2 - y1) * 0.15, (y1 + y2) / 2 - (x2 - x1) * 0.15
        d = f"M{x1} {y1}Q{mx:.0f} {my:.0f} {x2} {y2}"
        out.append(f'<path id="hart-p{k}" class="hart__line" d="{d}"/>')
        out.append(f'<circle class="hart__spark" r="5"><animateMotion dur="{5 + k}s" repeatCount="indefinite" rotate="auto">'
                   f'<mpath href="#hart-p{k}"/></animateMotion></circle>')
    for x, y, label in nodes:
        main = label == "RIVIA"
        out.append(f'<circle class="hart__ring{" is-main" if main else ""}" cx="{x}" cy="{y}" r="{64 if main else 46}"/>'
                   f'<circle class="hart__node{" is-main" if main else ""}" cx="{x}" cy="{y}" r="{9 if main else 6}"/>'
                   f'<text class="hart__label" x="{x}" y="{y + (96 if main else 78)}" text-anchor="middle">{label}</text>')
    return "".join(out)


def _reach():
    """WEB集客：伸びていく線グラフと、届く先の人の点が灯る"""
    rnd = random.Random(5)
    out = []
    for gy in range(140, H, 120):
        out.append(f'<path class="hart__grid" d="M0 {gy}H{W}"/>')
    pts, y = [], 760
    for gx in range(0, W + 1, 80):
        y = max(140, y - rnd.uniform(-10, 42))
        pts.append(f"{gx} {y:.0f}")
    out.append(f'<path class="hart__chart" pathLength="1" d="M{" L".join(pts)}"/>')
    for k in range(70):
        x, yy = rnd.uniform(560, W - 20), rnd.uniform(60, H - 60)
        out.append(f'<circle class="hart__person" style="--i:{k % 17}" cx="{x:.0f}" cy="{yy:.0f}" r="{rnd.choice([2.5, 3, 4])}"/>')
    return "".join(out)


def _network():
    """WEB採用：人と人がつながる網。ところどころの点が朱に灯る"""
    rnd = random.Random(3)
    pts = [(rnd.uniform(520, W - 30), rnd.uniform(40, H - 40)) for _ in range(46)]
    out = []
    for i, (x1, y1) in enumerate(pts):
        near = sorted(pts, key=lambda p: (p[0] - x1) ** 2 + (p[1] - y1) ** 2)[1:3]
        for x2, y2 in near:
            out.append(f'<path class="hart__line" d="M{x1:.0f} {y1:.0f}L{x2:.0f} {y2:.0f}"/>')
    for i, (x, y) in enumerate(pts):
        lit = i % 6 == 0
        out.append(f'<circle class="hart__person{" is-lit" if lit else ""}" style="--i:{i % 13}" cx="{x:.0f}" cy="{y:.0f}" r="{6 if lit else 3.5}"/>')
    return "".join(out)


ART = {"operation": _town, "management": _calendar, "partnership": _triangle, "marketing": _reach, "recruit": _network}


def art_svg(key):
    return _svg(ART[key](), key)


if __name__ == "__main__":
    for k in ART:
        print(k, len(art_svg(k)))
