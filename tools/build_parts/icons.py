# -*- coding: utf-8 -*-
# build.py の一部：アイコン（SVG）と SNS のリンク。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- icons
ICONS = {
    "house": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "yen": '<circle cx="12" cy="12" r="9"/><path d="M8.5 7.5 12 12l3.5-4.5M12 12v5M9 13h6M9 15.5h6"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "chart": '<path d="M4 20h16"/><path d="M6 16l4-4 3 3 5-6"/><path d="M15 9h3v3"/>',
    "scale": '<path d="M12 4v16M8 20h8M5 7h14"/><path d="M5 7l-3 6a3 3 0 0 0 6 0z"/><path d="M19 7l-3 6a3 3 0 0 0 6 0z"/>',
    "phone": '<rect x="7" y="3" width="10" height="18" rx="1.5"/><path d="M11 18h2"/>',
    "camera": '<path d="M4 8h4l2-2h4l2 2h4v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8.3 5 2.6 5 5.8"/>',
    "door": '<path d="M14 4H6v16h8"/><path d="M10 12h11M18 9l3 3-3 3"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "doc": '<path d="M6 3h9l3 3v15H6z"/><path d="M9 10h6M9 14h6M9 18h4"/>',
    "book": '<path d="M4 4h6a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h6z"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5 13.5 13.5 8.5 15.5 10.5 10.5z"/>',
    "bed": '<path d="M3 6v13M3 15h18v4M21 15v-3a3 3 0 0 0-3-3h-7v6"/><circle cx="7" cy="11.5" r="1.8"/>',
    "car": '<path d="M3 16v-3l2.5-5h13l2.5 5v3z"/><circle cx="7.5" cy="17" r="1.8"/><circle cx="16.5" cy="17" r="1.8"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3M12 15v2"/>',
}


# 代表の個人SNS（共有用の追跡パラメータは除去済み）
# 例: FOUNDER_SNS = {"ishihara": "https://www.linkedin.com/in/..."}。founders の sns=[(種類, 表示名, URL)] で表示
FOUNDER_SNS = {}


def sns_html(f):
    """代表の SNS リンク。登録がない代表には何も出さない"""
    links = "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="{e(f["name"])}の{lbl}（別タブで開きます）">{SNS_ICONS[k]}<span>{lbl}</span></a></li>'
        for k, lbl, u in f.get("sns", [])
    )
    return f'            <ul class="founder__sns">{links}</ul>\n' if links else ""

SNS_ICONS = {
    "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4v11H3zm7 0h3.8v1.6h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1v5.35h-4v-4.74c0-1.13-.02-2.59-1.58-2.59-1.58 0-1.82 1.23-1.82 2.5v4.83h-4z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.87.25-1.46 1.5-1.46h1.55V4.47A20.7 20.7 0 0 0 14.3 4.3c-2.24 0-3.8 1.37-3.8 3.9v2.3H8v3h2.5V21z"/></svg>',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


ARROW = '<span class="arrow" aria-hidden="true"></span>'


def br(lines):
    """行のリストを <br> で結合（各行はエスケープ）"""
    return "<br>".join(e(l) for l in lines)


# TOPのファーストビュー：写真を切り替えながら、ゆっくり寄っていく（ファイル名, 幅, 高さ, 見せる位置）
HERO_SLIDES = [
    ("autumn-garden", 1616, 1079, "50% 45%"),
    ("thatched-house", 1920, 1080, "50% 60%"),
    ("riverside-town", 1620, 1080, "50% 55%"),
    ("fuji-lake", 1620, 1080, "50% 40%"),
]


# TOPの事業紹介：事業の括りごとに「届ける価値」を大きく見せる
TOP_VALUES = {
    "hospitality": dict(en="Revive & Run", value="眠る空き家を、<br>稼ぐ宿に変える", photo="dark-room", w=1080, h=1620),
    "webmarketing": dict(en="Reach & Hire", value="地域の魅力を、<br>人に届ける", photo="laptop-dashboard", w=1516, h=1080),
}
# 事業ごとのひとこと（何をしてくれる事業か）
SERVICE_CATCH = {
    "operation": "空き家を宿に再生・運営",
    "management": "開業から日々の運営まで伴走",
    "partnership": "民泊向きの物件選びから運営まで",
    "marketing": "問い合わせと売上を伸ばす",
    "recruit": "地方企業の人材確保を支援",
}


# サービスページの見出しで、写真に食い込ませる縦書きの言葉
SERVICE_VERTICAL = {"operation": "空き家を、灯す。", "management": "宿を、事業に。", "partnership": "物件を、宿に。",
                    "marketing": "魅力を、届ける。", "recruit": "人と、出会う。"}
# サービスページの見出しの写真3枚（大きな横長・右上の縦長・右下）。(ファイル名, 幅, 高さ, 見せる位置)
SERVICE_COLLAGE = {
    "operation": [("thatched-house", 1920, 1080, "55% 55%"), ("gassho-village", 1080, 1620, "50% 40%"), ("window-garden", 1079, 1349, "50% 50%")],
    "management": [("irori-room", 1623, 1079, "50% 55%"), ("scene-stay", 1080, 1350, "50% 50%"), ("pillow", 1619, 1079, "50% 50%")],
    "partnership": [("riverside-town", 1620, 1080, "50% 50%"), ("old-town-street", 1080, 1437, "50% 50%"), ("white-bedroom", 1620, 1080, "50% 50%")],
    "marketing": [("laptop-dashboard", 1516, 1080, "50% 50%"), ("scene-walk", 901, 1350, "50% 50%"), ("fuji-lake", 1620, 1080, "50% 50%")],
    "recruit": [("rural-station", 1918, 1080, "50% 50%"), ("town-railway", 1080, 1620, "50% 50%"), ("green-hills", 1620, 1080, "50% 50%")],
}
