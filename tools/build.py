# -*- coding: utf-8 -*-
"""RIVIA&CO. サイトの静的HTMLを生成する（作業用スクリプト）"""
from html import escape as e, unescape
import math
import os
import re
import budoux  # pip install budoux（日本語の文節区切り）
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures import insert_figure  # 記事の図解

_JA = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
_budoux = budoux.load_default_japanese_parser()


def _merge_short(chunks):
    """「伸ば｜したい」「宿と｜して」のような2文字以下の切れ端は、前後の文節とつなげて改行させない
    （句読点や閉じかっこの直後は自然な区切りなので、そこではつなげない）"""
    out = []
    sticky = False
    for c in chunks:
        joinable = out and not re.search(r"[、。」）!?！？]$", out[-1])
        if joinable and (sticky or len(c) <= 2 or len(out[-1]) <= 2):
            out[-1] += c
        else:
            out.append(c)
        sticky = len(c) <= 2 and not re.search(r"[、。」）!?！？]$", c)
    return out


# 本文中で強調する言葉（お客様にとっての「結果・メリット」）。各ページで最初の1回だけマーカーを引く
HIGHLIGHTS = [
    "毎月の家賃収入", "収支を比較", "次の世代へつなぎます", "負担がいちばん小さい方法",
    "リピートを自社に集めます", "「どこで何件獲るか」", "「探したときに見つかる」状態", "成果の出る施策に予算を寄せます",
    "「成長投資」", "成果の出る手段に予算を集中", "「働く魅力」を言語化", "ミスマッチを防ぎます",
    "契約前に確認", "無理のない計画", "運営の手間から解放", "手元に残る利益を増やします",
    "収益が見込める物件", "根拠のある利回り", "一括で担います", "宿にできるかを事前に判定",
    "毎月のレポートと振り返り",
]


def highlight(html):
    head, sep, body = html.partition("<body")
    parts = re.split(r"(<[^>]+>)", body)
    done = set()
    skip = 0
    for i, p in enumerate(parts):
        if p.startswith("<"):
            m = re.match(r"<(/?)(script|style|title|h[1-6]|a|button|strong|label|option|textarea)\b", p, re.I)
            if m:
                skip += -1 if m.group(1) else 1
            continue
        if skip:
            continue
        for w in HIGHLIGHTS:
            ew = e(w, quote=False)
            if w not in done and ew in p:
                p = p.replace(ew, f'<strong class="hl">{ew}</strong>', 1)
                done.add(w)
        parts[i] = p
    return head + sep + "".join(parts)


def phrase_breaks(html):
    """日本語の改行を整える。
    - 見出しと短い文言（20字以内）：文節ごとに改行候補（<wbr>）を入れ、CSS の
      word-break: keep-all で単語の途中で折り返さないようにする。
    - 本文（長い文）：<n-w> で包んで通常どおり行末まで詰めて折り返し、両端揃え（CSS）で
      右端のガタつきをなくす。短い最終行は js/main.js が字間の微調整で防ぐ。"""
    head, sep, body = html.partition("<body")
    parts = re.split(r"(<[^>]+>)", body)
    # 段落（p・li など）ごとの文字数を先に数え、太字などで分かれたテキストも段落単位で判定する
    block_len = {}
    stack = []
    for i, p in enumerate(parts):
        m = re.match(r"<(/?)(p|li|dd|blockquote|figcaption|h[1-6])\b", p)
        if m and not m.group(1):
            stack.append((i, m.group(2)))
        elif m and stack:
            start, _ = stack.pop()
            idx = [k for k in range(start + 1, i) if not parts[k].startswith("<")]
            total = sum(len(unescape(parts[k]).strip()) for k in idx)
            for k in idx:
                block_len.setdefault(k, total)
    skip = heading = 0
    lead = False  # 一文のリード（サービス概要など）も見出しと同じく文節で改行する
    for i, p in enumerate(parts):
        if p.startswith("<"):
            m_lead = re.match(r'<(p|span) class="(overview__text|hero__sub|cta__text|page-hero__lead|page-hero__target|about-line|mq__q|guide-step__title|mhero__lead)\b', p)
            if m_lead:
                lead = m_lead.group(1)
            elif lead and p == f"</{lead}>":
                lead = False
            m = re.match(r"<(/?)(script|style|textarea|select|option|title|h[1-4])\b", p, re.I)
            if m:
                step = -1 if m.group(1) else 1
                if m.group(2).lower().startswith("h"):
                    heading += step
                else:
                    skip += step
            continue
        text = unescape(p)
        if skip or not _JA.search(text):
            continue
        if heading or lead or block_len.get(i, len(text.strip())) <= 20:
            parts[i] = "<wbr>".join(e(c, quote=False) for c in _merge_short(_budoux.parse(text)))
            continue
        body_text = text.rstrip()
        trail = text[len(body_text):]
        # 本文：行末まで詰めて折り返し、両端揃えで右端を揃える。
        # 最後の行が短くなる場合は、表示時に js/main.js が字間をわずかに調整して整える
        # 60字を超える長い段落だけ両端揃え（短い文は字間を一定に保つため左揃え）
        tag = '<n-w class="j">' if block_len.get(i, len(body_text.strip())) > 60 else "<n-w>"
        parts[i] = f'{tag}{e(body_text, quote=False)}</n-w>{e(trail, quote=False)}'
    return head + sep + "".join(parts)


OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # リポジトリの直下（tools/ の1つ上）
import datetime as _dt
BUILD_DATE = _dt.date.today().isoformat()  # llms.txt には公開済みの記事だけを載せる
SITE = "https://rivia-co.com"  # 公開ドメイン
CLARITY_ID = "yrrji51n1y"  # Microsoft Clarity のプロジェクトID
GA_ID = "G-RZVE2XBPQ2"  # Google アナリティクス 4 の測定ID

SERVICES = [
    ("operation", "アキヤド空き家再生"),
    ("management", "アキヤド開業・運営支援"),
    ("partnership", "不動産事業者様との協業"),
    ("marketing", "WEB集客支援事業"),
    ("recruit", "WEB採用支援事業"),
]

# 事業の2つの軸（ナビ・一覧はこの括りで表示する）
GROUPS = [
    dict(key="hospitality", en="Hospitality", name="宿泊施設の運営・開業",
         lead="空き家の再生から既存施設の運営、これから宿を始める方の開業、不動産事業者様との協業まで。自ら宿を運営する当事者として支援します。",
         services=["operation", "management", "partnership"]),
    dict(key="webmarketing", en="Web Marketing", name="WEBマーケティング支援",
         lead="地方の事業者様の「集客」と「採用」を、WEBマーケティングの力で経営課題から解決します。",
         services=["marketing", "recruit"]),
]

# ナビゲーション（Serviceメニュー）：まずお客様の立場（個人／法人・事業者）を選び、
# その立場に合うサービスだけを「目的・お悩み」から探せるようにする
NAV_AUDIENCES = [
    dict(key="personal", name="個人のお客様", note="空き家・副業・投資",
         groups=[(None, ["operation", "management"])]),
    dict(key="business", name="法人・事業者のお客様", note="宿の運営・不動産・集客・採用",
         groups=[("宿泊施設の開業・運営・不動産", ["management", "partnership"]),
                 ("集客・採用（WEBマーケティング）", ["marketing", "recruit"])]),
]

# ナビゲーション（Serviceメニュー）に出す「やりたいこと」
NAV_INTENTS = [
    ("個人のお客様", [("operation", "空き家を活かしたい・売りたい"), ("management", "民泊を始めたい")]),
    ("法人のお客様", [("management", "民泊を始めたい"), ("partnership", "物件を民泊用に売りたい"),
                     ("marketing", "集客を伸ばしたい"), ("recruit", "人材を採用したい")]),
]

# 同じサービスでも、お客様の立場によってメニューに出す「お悩み」を変える
NAV_WORRY = {
    ("personal", "management"): "副業や投資目的で、小規模宿の運営を検討中",
    ("business", "management"): "新規事業で、小規模宿に挑戦したい",
}

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


# ---------------------------------------------------------------- layout

import json

SERVICE_NAMES = dict(SERVICES)

# 各サービスの対象者（トップの「お悩みから探す」と共通）
# TOPの事業紹介（英語名・ひとこと説明・アイコン）
SERVICE_INTRO = {
    "operation": ("Revitalization", "地方の空き家を自社で改修し、「暮らすように旅する」宿として運営します。", "house"),
    "management": ("Management", "民泊・小規模宿の開業から日々の運営まで、個人・法人を問わず伴走します。", "key"),
    "marketing": ("Web Marketing", "自社サイト・広告・SNSなどで、問い合わせと売上が伸びる仕組みをつくります。", "target"),
    "partnership": ("Partnership", "保有物件から民泊向きの物件を選び、利回りの算出から購入後の運営まで担います。", "key"),
    "recruit": ("Web Recruiting", "採用計画から定着まで、地方企業の人材確保を支援します。", "users"),
}

PERSONAS = {
    "operation": "実家・空き家の処分や利活用に悩んでいる",
    "marketing": "集客を強化して、売上を伸ばしたい",
    "recruit": "人手が足りず、採用に悩んでいる",
    "management": "民泊・小規模宿を、プロと始めたい",
    "partnership": "保有物件を、民泊用に販売したい",
}

# トップ: ミッション（大きな絵）→ ビジョン（中期的に取り組むこと）→ バリュー（大切にする姿勢）
MISSION = dict(
    copy="地域に眠る価値を、日本の活力に。",
    lead=["空き家や遊休不動産、食や自然、文化や人の営み。地域には、まだ活かされていない価値が数多く眠っています。",
          "私たちはその価値を掘り起こし、「まちづくり」と「観光づくり」を通じて、人が訪れ、働き、暮らし続けられる地域を増やしていきます。",
          "地域が元気になることが、日本が元気になることだと信じて。"],
)
VISION = dict(
    copy="「暮らすように旅する」滞在を、全国のまちへ。",
    lead="ミッションの実現に向けて、私たちが中期的に取り組むこと。",
    steps=[
        ("見つける", "Discover", "空き家や遊休不動産、食・自然・文化・人の営みなど、地域に眠る資源を掘り起こします。"),
        ("磨く", "Refine", "デザインとテクノロジーの力で、「その土地の日常を体験できる宿」や観光コンテンツへと再生・創出します。"),
        ("届ける", "Deliver", "WEBマーケティングの力で、その価値を求める国内外の旅行者に確実に届けます。"),
        ("循環させる", "Circulate", "人の流れと雇用を地域に生み、持続可能な経済循環とまちづくりへとつなげます。"),
    ],
    outcomes=[("旅行者には", "その土地の日常に溶け込む、新しい滞在価値を。"),
              ("地域には", "眠っていた資源が稼ぎ、雇用と交流が生まれる経済循環を。"),
              ("オーナー様には", "負担だった資産や施設が、収益を生む事業に変わる未来を。")],
)
TOP_CONCEPT = dict(
    copy="日本の魅力を、暮らすように味わう。",
    lead=["私たちは、単なる宿泊施設を提供するのではありません。",
          "地域に眠る資源（空き家や遊休不動産）を、デザインとテクノロジーの力で「その土地の日常を体験できる居場所」へとアップデートします。",
          "旅行者には新しい滞在価値を、地域には持続可能な経済循環を。"],
)
# 宿を起点に、地域へ人とお金がめぐる循環（TOPのコンセプト横の図）
TOP_CYCLE = [
    ("Revive", "空き家を、", "宿に再生"),
    ("Visit", "旅行者が、", "まちを訪れる"),
    ("Spend", "まちで、", "食べて買う"),
    ("Return", "ファンになり、", "また訪れる"),
]
TOP_SCENES = [
    ("scene-stay.jpg", "50% 50%", "Stay", "空き家を、泊まれる宿に", "眠っていた空き家を、RIVIAが宿に再生。その土地の暮らしに溶け込むように泊まれます。"),
    ("scene-walk.jpg", "50% 60%", "Walk", "宿を拠点に、まちへ", "灯りのともる路地を歩き、地元の店で食べ、買う。旅行者の消費が、宿の外のまちへ広がります。"),
    ("oshino-mill.jpg", "50% 60%", "Connect", "土地とつながり、また訪れる", "食や風土、観光コンテンツ、人。土地の魅力とつながり再訪が生まれ、地域の収益と雇用に。"),
]
# 宿を起点に、地域へお金と人が循環する流れ（情景の下に1行で示す）
MISSION_PROSE = [
    ["空き家や遊休不動産、", "食や自然、文化や人の営み。", "地域には、まだ活かされていない", "価値が数多く眠っています。"],
    ["その土地にとって、", "そこに暮らす人々にとって、", "本当に必要なものは何か。", "私たちは自ら現場に立ち、", "地域と徹底的に向き合います。"],
    ["眠っていた価値を掘り起こし、", "まちづくりと観光づくりへ。", "人が訪れ、働き、", "暮らし続けられる地域を、", "ひとつずつ増やしていく。"],
    ["地域が元気になることが、", "日本が元気になること。", "私たちは、そう信じています。"],
]
VALUES = [
    ("圧倒的当事者であれ", "自ら宿を運営し、現場で確かめたことだけを提案する。"),
    ("自ら機会をつくれ", "指示を待たず、自ら課題を見つけて動き、次の機会を生み出す。"),
    ("想いを、成果で示す", "想いだけで終わらせず、数字と結果で応える。"),
    ("続く仕組みをつくる", "一過性で終わらせず、地域に残り、循環する形を選ぶ。"),
]


# ご相談の流れ（トップ・お問い合わせで共通）
FLOW = [
    ("お問い合わせ", "フォームから24時間受け付けています。2営業日以内に担当者よりご連絡いたします。"),
    ("無料ヒアリング", "現状と課題、目指したい姿をお伺いします。まだ考えがまとまっていない段階でも構いません。"),
    ("ご提案", "課題に合わせた支援内容・進め方・お見積りをご提示します。"),
    ("ご支援開始", "ご納得いただけた場合のみご契約。現場に入り、成果が出るまで伴走します。"),
]

# RIVIAが選ばれる理由
REASONS = [
    ("自ら宿を運営する「当事者」", "下田市の「NODE Shimoda」など、自ら宿を運営。現場で検証したノウハウをお届けします。"),
    ("運営・集客・採用をワンストップで", "運営・集客・人材は、すべてつながっています。窓口をひとつにまとめ、一貫して支援します。"),
    ("事業づくりとデータ分析の経験", "新規事業開発、行政、データ分析のキャリアを持つ創業メンバーが、数字にもとづいて意思決定を支援します。"),
]


# ---------------------------------------------------------------- layout
def header(current):
    def cur(key):
        return ' aria-current="page"' if current == key else ""

    names = dict(SERVICES)

    # 「〜したい」の一言で、目的からまっすぐサービスを選べるようにする
    items = "".join(
        f'<li class="subnav__aud">{e(aud)}</li>'
        + "".join(
            f'<li><a href="service-{k}.html"{cur(k)}><span class="subnav__text">'
            f'<span class="subnav__intent">{e(intent)}</span><span class="subnav__name">{e(names[k])}</span>'
            f'</span> {ARROW}</a></li>'
            for k, intent in its)
        for aud, its in NAV_INTENTS)
    sub = (f'              <li class="subnav__intents"><ul>{items}</ul></li>\n'
           f'              <li class="subnav__foot"><a href="index.html#service">すべてのサービスを見る {ARROW}</a></li>')
    service_cur = ' aria-current="page"' if current in SERVICE_NAMES else ""
    return f"""  <header class="header">
    <div class="container header__inner">
      <a href="index.html" class="logo" aria-label="RIVIA&amp;CO. トップページ"><img src="images/logo/logo.svg" alt="RIVIA&amp;CO." width="325" height="64"></a>

      <nav class="gnav" id="gnav" aria-label="メインナビゲーション">
        <ul class="gnav__list">
          <li><a href="about.html" class="gnav__link"{cur("about")}>私たちについて</a></li>
          <li class="gnav__item--has-sub">
            <button type="button" class="gnav__link" aria-expanded="false" aria-controls="subnav-service"{service_cur}>事業内容 <span class="gnav__caret" aria-hidden="true"></span></button>
            <ul class="subnav" id="subnav-service">
{sub}
            </ul>
          </li>
          <li><a href="index.html#project" class="gnav__link">実績</a></li>
          <li><a href="media.html" class="gnav__link"{cur("media")}>メディア</a></li>
          <li><a href="careers.html" class="gnav__link"{cur("careers")}>採用情報</a></li>
          <li><a href="contact.html{"?category=" + current if current in SERVICE_NAMES else ""}" class="gnav__link"{cur("contact")}>お問い合わせ</a></li>
        </ul>
      </nav>

      <button type="button" class="menu-btn" aria-controls="gnav" aria-expanded="false" aria-label="メニューを開く"><span></span><span></span><span></span></button>
    </div>
  </header>"""


def footer():
    # 文字を詰め込まず、ロゴ・相談ボタン・主要リンクだけのシンプルな構成にする
    links = [("about.html", "私たちについて"), ("index.html#service", "事業内容"), ("index.html#project", "実績"),
             ("media.html", "メディア"), ("careers.html", "採用情報"), ("contact.html", "お問い合わせ")]
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links)
    # 目的・お悩みから探す（Serviceメニューと同じ「〜したい」の一覧）
    # 各サービスの案内（サービス名の下に、ページ内の主な項目へのリンク）
    names = dict(SERVICES)
    subs = [("お悩みと解決策", "{k}-issues"), ("プラン例", "plans"), ("ご支援の流れ", "flow"), ("よくあるご質問", "faq")]
    intents = "".join(
        f'<div class="footer__aud"><p>{e(aud)}</p><ul>'
        + "".join(f'<li><a href="service-{k}.html">{e(t)} {ARROW}</a></li>' for k, t in its)
        + '</ul></div>'
        for aud, its in NAV_INTENTS)
    svcs = "".join(
        f'<div class="footer__svc"><a class="footer__svc-name" href="service-{k}.html">{e(names[k])} {ARROW}</a><ul>'
        + "".join(f'<li><a href="service-{k}.html#{a.format(k=k)}">{e(t)}</a></li>' for t, a in subs)
        + '</ul></div>'
        for k, _ in SERVICES)
    return f"""  <footer class="footer footer--simple">
    <div class="container">
      <div class="footer__top">
        <div class="footer__brand">
          <a href="index.html" class="logo"><img src="images/logo/logo.svg" alt="RIVIA&amp;CO." width="325" height="64" loading="lazy"></a>
          <p class="footer__copy">地域に眠る価値を、日本の活力に。</p>
        </div>
        <a href="contact.html" class="footer__cta">無料で相談する {ARROW}</a>
      </div>
      <div class="footer__intents">{intents}</div>
      <nav aria-label="フッターナビゲーション"><ul class="footer__links">{nav}</ul></nav>
      <div class="footer__bottom">
        <address class="footer__address">〒121-0012 東京都足立区青井六丁目8番8号 Grand Maison青井201</address>
        <a href="privacy.html">プライバシーポリシー</a>
        <p>&copy; 2026 合同会社RIVIA&amp;CO.</p>
      </div>
    </div>
  </footer>"""


FAVICON = "data:image/svg+xml," + (
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23111'/%3E"
    "%3Ctext x='32' y='45' text-anchor='middle' font-family='Georgia,serif' font-size='38' fill='%23fff'%3ER%3C/text%3E"
    "%3Ccircle cx='49' cy='44' r='3' fill='%232d6a43'/%3E%3C/svg%3E"
)


FONTS_CSS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Noto+Sans+JP:wght@400;500&family=Noto+Serif+JP:wght@200;300;400&display=swap"


EN_PAGES = ["index.html", "about.html", "careers.html", "contact.html", "privacy.html", "thanks.html",
            "service-operation.html", "service-management.html", "service-partnership.html",
            "service-marketing.html", "service-recruit.html"]


def url_for(filename):
    return f"{SITE}/" + ("" if filename == "index.html" else filename)


def page(filename, title, description, body, current="", jsonld=None, og_type=None, og_image="images/ogp.jpg", noindex=False, mnav="", cv_category="operation"):
    # サービスページは、画面下に常に「無料で相談する」を表示する
    fixed_cta = (f'  <div class="fixed-cta"><a href="contact.html?category={current}" class="btn">無料で相談する {ARROW}</a></div>'
                 if current in SERVICE_NAMES else "")
    is_media = current == "media"
    logo_font = ('\n  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700&text=%E3%82%A2%E3%82%AD%E3%83%A4%E3%83%89&display=swap" media="print" onload="this.media=\'all\'">'
                 if filename == "index.html" else "")
    fonts_css = FONTS_CSS.replace("&display=swap", "&family=Zen+Maru+Gothic:wght@500;700&display=swap") if is_media else FONTS_CSS
    if is_media and filename not in ("media/contact.html", "media/thanks.html"):
        fixed_cta = (f'  <div class="fixed-cta fixed-cta--media"><a href="contact.html?category={cv_category}&amp;from=akiyado" class="btn" data-cta="media-fixed">'
                     f'無料で相談する {ARROW}</a></div>')
    # コーポレートページは英語版（/en/）があるため、言語の対応を検索エンジンに伝え、ヘッダーに切り替えを置く
    has_en = not is_media and filename in EN_PAGES
    en_url = f"{SITE}/en/" + ("" if filename == "index.html" else filename)
    hreflang = (f'\n  <link rel="alternate" hreflang="ja" href="{url_for(filename)}">'
                f'\n  <link rel="alternate" hreflang="en" href="{en_url}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{url_for(filename)}">') if has_en else ""
    lang_switch = (f'<a href="en/{filename}" class="lang-switch" hreflang="en" lang="en" aria-label="English">EN</a>\n      '
                   if has_en else "")
    full_title = f"{title} | 合同会社RIVIA&CO." if title else "合同会社RIVIA&CO. | 地域に眠る価値を、日本の活力に。"
    if is_media:
        # メディアはサイトの一部（rivia-co.com/media/）だが、見え方は独立したメディアにする
        full_title = title if "アキヤド" in title else f"{title} | アキヤド"
        if og_image == "images/ogp.jpg":
            og_image = "images/ogp-media.jpg"
    url = f"{SITE}/" + ("" if filename == "index.html" else filename)
    ld = ""
    if jsonld:
        ld = "\n".join(
            f'  <script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld
        ) + "\n"
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{GA_ID}');
  </script>
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{CLARITY_ID}");
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{url}">{hreflang}
{'  <meta name="robots" content="noindex">' + chr(10) if noindex else ""}  <link rel="icon" href="images/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="images/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="apple-touch-icon" href="images/apple-touch-icon.png">

  <!-- OGP（SNSやLINEでシェアされたときの表示。画像は横長 1200×630） -->
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="{og_type or ("website" if filename == "index.html" else "article")}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/{og_image}">{"" if og_image not in ("images/ogp.jpg", "images/ogp-media.jpg") else chr(10) + '  <meta property="og:image:width" content="1200">' + chr(10) + '  <meta property="og:image:height" content="630">'}
  <meta property="og:site_name" content="{"アキヤド" if is_media else "合同会社RIVIA&amp;CO."}">
  <meta property="og:locale" content="ja_JP">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="{fonts_css}" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="{fonts_css}"></noscript>{logo_font}
  <link rel="stylesheet" href="css/style.css">
  <script>
    // JS が有効なときだけアニメーション用の非表示を使う。
    // main.js が読み込めなかった場合は 2 秒後に全コンテンツを表示する（表示抜けの防止）。
    document.documentElement.classList.add('js');
    setTimeout(function () {{ if (!window.RIVIA_READY) document.documentElement.classList.remove('js'); }}, 2000);
  </script>
{ld}</head>
<body{' class="is-media"' if is_media else ""}>

{media_header(mnav) if is_media else header(current).replace('<button type="button" class="menu-btn"', lang_switch + '<button type="button" class="menu-btn"', 1)}

  <main>
{body}
  </main>

{media_footer() if is_media else footer()}
{fixed_cta}
  <script src="js/main.js"></script>
</body>
</html>
"""
    if is_media:
        # アキヤドの中の相談・資料請求は、アキヤド専用のお問い合わせページへ（運営会社への問い合わせだけはコーポレートへ）
        html = html.replace('href="contact.html', 'href="media/contact.html').replace('href="CORP_CONTACT"', 'href="contact.html?from=akiyado"')
    html = phrase_breaks(highlight(relative_to_root(html, filename)))
    path = os.path.join(OUT, PAGES_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


PAGES_DIR = "pages"  # HTMLはすべて pages/ にまとめる（公開URLは vercel.json の書き換えで今までどおり）
SEO_DIR = "seo"      # robots.txt / sitemap.xml の置き場所（公開URLはサイト直下のまま）


def relative_to_root(html, filename):
    """HTMLは pages/ 以下に置くため、リンクの先を種類ごとに直す。
    - ページ同士のリンク（○○.html）：pages/ の中での相対パス
    - 画像・CSS・JS など：サイト直下（pages/ の1つ上）への相対パス"""
    import re as _re
    depth = filename.count("/")
    page_prefix = "../" * depth
    asset_prefix = "../" * (depth + 1)
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http:", "https:", "#", "data:", "mailto:", "tel:", "/")) or not url:
            return m.group(0)
        is_page = _re.match(r"^(?:\.\./)*[^?#]*\.html(?:[?#].*)?$", url) is not None
        if url.startswith("../"):
            return m.group(0) if is_page else f'{attr}="../{url}"'
        return f'{attr}="{(page_prefix if is_page else asset_prefix)}{url}"'
    html = _re.sub(r'\b(href|src)="([^"]*)"', fix, html)
    # srcset（"画像 幅w, 画像 幅w"）の各画像にも同じ直しをかける
    def fix_srcset(m):
        parts = []
        for item in m.group(1).split(","):
            url, _, w = item.strip().partition(" ")
            parts.append(fix(_re.match(r'(src)="([^"]*)"', f'src="{url}"')).split('"')[1] + (" " + w if w else ""))
        return f'srcset="{", ".join(parts)}"'
    return _re.sub(r'\bsrcset="([^"]*)"', fix_srcset, html)


# 空き家・物件をお持ちの方に向けた、相談のハードルを下げる一言（対応エリアとは別に、相談の呼びかけとして置く）
OPEN_MSG = "観光地でなくても、収益物件になり得ます。お気軽にお問い合わせください。"


def cta(category="", title="まずは、現状をお聞かせください。", text=""):
    q = f"?category={category}" if category else ""
    # 見出しは読点の後で改行（スマホ）。一言は文ごとに改行して、変な位置で折り返さないようにする
    title_html = e(title).replace("、", '、<br class="sp-only">', 1)
    sub = ("\n        " + f'<p class="cta__text">{"<br>".join(e(t) + "。" for t in text.split("。") if t)}</p>') if text else ""
    return f"""    <section class="section cta cta--photo">
      <img class="cta__bg" src="images/photos/garden-boat.jpg" alt="" width="1617" height="1079" loading="lazy" decoding="async">
      <div class="container reveal">
        <h2 class="cta__title">{title_html}</h2>
        <div class="cta__btn"><a href="contact.html{q}" class="btn btn--lg">ご相談はこちらから {ARROW}</a></div>{sub}
      </div>
    </section>"""


def flow_section(soft=False):
    steps = "\n".join(
        f"""          <li class="flow__step reveal" data-delay="{i - 1}">
            <span class="flow__num">{i:02d}</span>
            <h3 class="flow__title">{e(t)}</h3>
            <p class="flow__desc">{e(d)}</p>
          </li>"""
        for i, (t, d) in enumerate(FLOW, 1)
    )
    return f"""    <section class="section{' section--soft' if soft else ''}">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Flow</span>
          <h2 class="section-title">ご相談の流れ</h2>
          <p class="section-lead">ご契約までに費用がかかることはありません。まずはお気軽にお問い合わせください。</p>
        </div>
        <ol class="flow">
{steps}
        </ol>
      </div>
    </section>"""


# NODE Shimoda のゲストレビュー（Airbnb に実際に投稿されたものだけを、原文のまま載せる）
# 例: dict(text="原文のまま", who="ゲスト（東京都）", date="2026年8月"),
NODE_REVIEWS = [
    dict(text="和モダンな室内がとてもオシャレで、快適でした！お部屋の居心地がよく、下田旅行の素敵な思い出になりました。",
         who="Airbnbゲスト・1泊", date="2026年9月"),
    dict(text="駅から近くアクセスが良く利便性が高いと感じました。室内も清潔で過ごしやすかったです。",
         who="Airbnbゲスト・1泊", date="2026年9月"),
    dict(text="海も近く初日の出も見ることができ、スーパーも近かったのでとても便利で快適な時間を過ごすことができました！",
         who="Airbnbゲスト・数泊", date="2026年1月"),
]


def reviews_html():
    if not NODE_REVIEWS:
        return ""
    items = "\n".join(
        f"""            <figure class="review reveal" data-delay="{i % 3}">
              <blockquote class="review__text">「{e(r["text"])}」</blockquote>
              <figcaption class="review__who">{e(r["who"])}{f'<span>{e(r["date"])}</span>' if r.get("date") else ""}</figcaption>
            </figure>"""
        for i, r in enumerate(NODE_REVIEWS))
    return f"""        <div class="reviews">
          <p class="reviews__head">ゲストの声 <span>Airbnb のレビュー（★5）より抜粋</span></p>
          <div class="reviews__list">
{items}
          </div>
        </div>
"""


def project_card(compact=False):
    return f"""        <a href="https://nodeshimoda.com/" class="project{' project--compact' if compact else ''} reveal" target="_blank" rel="noopener">
          <div class="project__img">
            <div class="project__photo" role="img" aria-label="NODE Shimoda のリビング"></div>
          </div>
          <div>
            <span class="project__badge">運営施設の一例</span>
            <h3 class="project__name">NODE Shimoda</h3>
            <p class="project__meta">静岡県下田市 ｜ 一棟貸しバケーションレンタル</p>
            <p class="project__desc">下田市旧町内の空き家を改修した滞在型アパート。RIVIAが運営・集客・DX化を担っています。</p>
            <div class="project__rating"><strong><span class="project__star" aria-hidden="true">★</span>4.88</strong><span>Airbnb評価（51件）</span></div>
            <span class="project__link">施設サイトを見る（別タブで開きます） {ARROW}</span>
          </div>
        </a>"""

SERVICE_DATA = {
    "operation": dict(
        message=["空き家を、", "地域を照らす新たな拠点へ。"],
        description="地方に眠る空き家や遊休不動産を、自社で企画・リノベーションし、宿泊施設として運営する事業です。",
        overview="地方の空き家を自社で改修し、「暮らすように旅する」宿として再生・運営する事業です。",
        issues_lead="空き家は、放置するほど費用と建物の傷みが増えていきます。",
        issues=[
            dict(icon="yen", title="お金と手間だけがかかる実家",
                 voice="相続した実家は空き家のまま。固定資産税と管理の手間だけが重くのしかかる。",
                 solve=["RIVIAが家を借りて宿として運営し、日々の管理も引き受けます。", "出ていくだけだった維持費が、毎月の家賃収入に変わります。"],
                 kpi=["毎年の維持費", "家賃などの収入", "管理の手間"]),
            dict(icon="compass", title="売れない・壊せない、行き場のない家",
                 voice="解体には数百万円、古すぎて売れない。処分も活用もできず途方に暮れている。",
                 solve=["現地・市場調査をもとに、「解体」「売却」「活用」の収支を比較してご提示します。", "改修から運営までRIVIAが担います。手放したい場合は買取も可能です。"],
                 kpi=["解体費用", "家から得られる収入", "家の価値"]),
            dict(icon="heart", title="思い出の家を、地域に残したい",
                 voice="思い出の実家は壊したくない。喜ばれる形で残したいが、やり方がわからない。",
                 solve=["家はお持ちのまま、思い出を活かした「暮らすように旅する」宿に再生します。", "地域の人や旅行者が集まる場所として、家を次の世代へつなぎます。"],
                 kpi=["家の保全", "地域を訪れる人", "地域とのつながり"]),
            dict(icon="chart", title="活用してうまくいくのか分からない",
                 voice="改修費がいくらかかるのか、本当にお客様が来るのかが分からず、一歩を踏み出せない。",
                 solve=["現地と周辺の宿を調べ、改修費と見込める収入を試算してお見せします。", "貸す・売るの両面から、負担がいちばん小さい方法をご提案します。"],
                 kpi=["初期費用", "元が取れるまでの期間", "宿の稼働の見込み"]),
        ],
        steps=[
            ("物件調査・ポテンシャル診断", "1〜2週間", "現地と周辺の宿を調べ、宿にできるかを判断します。"),
            ("事業計画・コンセプト策定", "2〜3週間", "宿のコンセプトと収支の見通しをつくります。"),
            ("空間デザイン・リノベーション", "1〜2ヶ月", "改修・家具の手配から予約の仕組みまで整えます。"),
            ("運営開始・地域連携", "継続", "運営を始め、地域と連携した滞在体験をつくります。"),
        ],
        faq=[
            ("ボロボロで雨漏りしているような空き家でも見てもらえますか？", "はい、構造部分（柱や基礎）が生きていればリノベーション前提で再生可能です。まずは現地確認をさせていただきます。"),
            ("手放したくないのですが、所有権を残したまま借り上げてもらうことは可能ですか？", "可能です。弊社が賃貸借契約を結んで月々の家賃をお支払いするプランと、売却されるプランの双方をご提案できます。"),
            ("解体費用に数百万かかると不動産業者に言われました。", "解体せず宿泊施設として活用すれば、解体コストゼロで逆に収益を生む資産に変えられる可能性が高いです。"),
            ("どのような地域・物件が対象になりますか？", "全国の空き家・遊休不動産が対象です。戸建て・古民家・アパートなど種別も問いません。まずは所在地と物件の状況をお聞かせください。"),
        ],
    ),
    "marketing": dict(
        message=["事業の魅力を、", "WEBで届ける。"],
        description="業種を問わず、地方の事業者様の集客をWEBマーケティングで支援する事業です。自社サイト、SEO、Googleマップ、WEB広告、SNS、予約・ECサイトなど手段を限定せず、問い合わせと売上が伸びる集客の仕組みをつくります。",
        overview="業種を問わず、自社サイトから広告・SNSまで、問い合わせと売上が伸びる集客を設計します。",
        issues_lead="集客の悩みは手段ではなく、自社で集客をコントロールできていない経営構造の問題です。",
        issues=[
            dict(icon="scale", title="外部サイト頼みで、利益と価格決定権を握られている",
                 voice="集客は予約・ポータルサイト頼みで手数料が重い。値下げ競争で、利益が残らない。",
                 solve=["自社サイトを直接の受け皿に整え、外部サイトは新規客の窓口として使い分けます。", "メールやLINEでお客様とつながり、リピートを自社に集めます。"],
                 kpi=["直接の問い合わせ比率", "販売手数料額", "営業利益率"]),
            dict(icon="compass", title="売上目標と集客施策がつながっていない",
                 voice="HPもSNSも広告も手を付けてはいるが、何に力を入れるべきか分からない。",
                 solve=["売上と流入経路を分析し、目標から逆算して「どこで何件獲るか」を設計します。", "各チャネルの役割と予算配分を決め、優先順位のついた実行計画に落とし込みます。"],
                 kpi=["チャネル別売上", "集客コスト比率", "問い合わせ・予約件数"]),
            dict(icon="target", title="事業の魅力がWEB上で伝わらず、選ばれない",
                 voice="自社サイトが古いまま。検索しても地図でも見つけてもらえず、良さが伝わっていない。",
                 solve=["自社サイトやSEO、Googleマップを整え、「探したときに見つかる」状態をつくります。", "写真・動画・記事・SNSで魅力を一貫して伝え、名前で選ばれる会社・お店にします。"],
                 kpi=["指名検索数", "自然検索からの流入", "サイトの問い合わせ率"]),
            dict(icon="chart", title="集客投資の費用対効果が見えない",
                 voice="広告や制作にお金をかけても、売上につながったか分からず、次の判断ができない。",
                 solve=["施策ごとに「いくら使い、いくら売れたか」を計測し、見える化します。", "検索・SNS広告を運用し、月次レポートで成果の出る施策に予算を寄せます。"],
                 kpi=["CPA（獲得単価）", "ROAS（広告費用対効果）", "チャネル別ROI"]),
        ],
        steps=[
            ("集客診断・戦略設計", "1〜2週間", "売上と流入経路を分析し、集客の戦略を決めます。"),
            ("自社サイト・計測環境の構築", "2週間〜", "自社サイトと問い合わせの流れ、効果の計測を整えます。"),
            ("集客施策の実行", "1ヶ月目〜", "SEO・Googleマップ・SNSなどの施策を実行します。"),
            ("WEB広告運用・分析改善", "継続", "広告を運用し、月次レポートで予算配分を見直します。"),
        ],
        faq=[
            ("宿泊施設以外の業種でも依頼できますか？", "はい。飲食店・小売店・観光事業・地方の中小企業など、業種を問わずご相談いただけます。"),
            ("SNS運用だけの支援ですか？", "いいえ。自社サイトの構築、SEO・オウンドメディア、Googleビジネスプロフィール、WEB広告、SNS、リピーター施策まで、手段を限定せずに事業に合った組み合わせをご提案します。"),
            ("自社サイトが古い、または持っていないのですが大丈夫ですか？", "はい。問い合わせや予約につながる自社サイトの新規制作やリニューアルから対応します。既存のサイトを活かせる場合は、改善提案から始めることも可能です。"),
            ("高品質な写真や動画が手元に一枚もないのですが大丈夫ですか？", "ご安心ください。弊社のプロカメラマンが現地へ出張り、自社サイトやWEB広告、SNSで最も目を引くカットを撮影・編集いたします。"),
            ("広告予算は毎月どれくらい必要ですか？", "月数万円程度の少額からスタート可能です。特定の媒体に限定せず、CPA（獲得単価）を見極めながら成果の出る媒体へ徐々に予算を寄せていくことをお勧めしています。"),
        ],
    ),
    "recruit": dict(
        message=["地域の未来を創る、", "最適な人材と出会うために。"],
        description="地方企業の「人材不足」という経営課題を、WEBマーケティングの手法で解決する採用支援事業です。業種を問わず、採用計画から採用ブランディング、母集団形成、定着までを一貫して支援します。",
        overview="業種を問わず、地方企業の人材不足を、採用計画から発信・定着まで一貫して解決します。",
        issues_lead="「応募が来ない」「すぐ辞める」は、事業計画・組織・発信の問題。採用を経営から設計し直します。",
        issues=[
            dict(icon="users", title="人手不足が、売上と事業成長の上限になっている",
                 voice="人が足りず、受けられる仕事や営業時間を絞っている。新しい事業にも踏み出せない。",
                 solve=["事業計画から逆算し、いつまでに・どの職種を・何人採るかの要員計画を設計します。", "採用を「欠員補充」ではなく「成長投資」と捉え、優先度の高い職種から進めます。"],
                 kpi=["人員充足率", "受けられる仕事の量", "人手不足による機会損失"]),
            dict(icon="yen", title="採用費が「掛け捨て」になり、投資として管理できていない",
                 voice="求人サイトに50万円以上払ったのに、応募は1件でドタキャン。毎回何も残らない。",
                 solve=["採用サイトを軸に、求人検索・スカウト・広告・SNSなどを最適に組み合わせます。", "チャネルごとの応募数・採用数・費用を計測し、成果の出る手段に予算を集中させます。"],
                 kpi=["採用単価", "チャネル別の採用数", "媒体費用"]),
            dict(icon="target", title="「選ばれる理由」がなく、条件競争で負けている",
                 voice="「田舎だから」「無名だから」と諦めている。給与や休日では大手に勝てない。",
                 solve=["経営者・現場へのヒアリングから、自社ならではの「働く魅力」を言語化します。", "採用サイトや社員の声で、地方で働くことに価値を感じる人材に魅力を届けます。"],
                 kpi=["応募数", "求める人材の応募比率", "内定承諾率"]),
            dict(icon="door", title="採用しても定着せず、投資が回収できない",
                 voice="採用しても「思っていた仕事と違う」と数ヶ月で辞めてしまい、費用と時間が無駄になる。",
                 solve=["仕事の実像を入社前に伝え、選考基準とカジュアル面談を設計してミスマッチを防ぎます。", "入社後のフォロー体制を整え、定着し活躍できる状態をつくります。"],
                 kpi=["早期離職率", "定着率", "採用・教育コストの回収"]),
        ],
        steps=[
            ("経営課題の整理・採用計画の設計", "1〜2週間", "事業計画から、必要な職種と人数を決めます。"),
            ("採用ブランディング・採用サイト制作", "2〜4週間", "働く魅力を言葉にし、採用サイトで伝えます。"),
            ("母集団形成・チャネル運用", "1ヶ月目〜", "求人検索・スカウト・広告などで応募を集めます。"),
            ("選考・定着プロセスの改善", "継続", "選考と入社後のフォローを整え、定着につなげます。"),
        ],
        faq=[
            ("求人媒体に出すのと何が違うのですか？", "媒体に掲載費を払い続ける採用ではなく、採用サイトやコンテンツを自社の資産として積み上げ、複数のチャネルから直接応募が集まる仕組みをつくります。媒体も、必要に応じて組み合わせの一つとして活用します。"),
            ("SNS運用や面接対策だけをお願いすることはできますか？", "個別の施策からのご相談も可能です。ただし成果を出すには、事業計画や採用ターゲットとのつながりが欠かせないため、まず現状の課題を整理したうえで最適な進め方をご提案します。"),
            ("観光業以外の業種でも依頼できますか？", "はい。製造・建設・介護・小売・観光など、業種を問わず地方企業の採用を支援しています。"),
            ("地方の企業でも、都市部から人が集まりますか？", "はい。Uターン・Iターンや地域貢献、自由な働き方に価値を感じる都市部の人材へ、魅力を的確に届けるアプローチが可能です。"),
            ("採用した後の定着まで支援してもらえますか？", "はい。ミスマッチを防ぐ選考設計から、内定者・新入社員のフォロー体制づくりまで、定着と活躍を見据えて支援します。"),
        ],
    ),
    "management": dict(
        message=["理想の小規模宿を、", "確かな事業へ。"],
        description="個人・法人を問わず、宿泊施設の開業から運営代行までを支援する事業です。立地選定・許認可・開業準備から、日々の運営・収益管理まで、必要な範囲でRIVIAが担います。",
        overview="民泊・小規模宿の開業から運営まで、オーナー様と共同で取り組み、事業を一緒に育てます。",
        issues_lead="開業前の不安から、開業後の運営の負担まで。一つの窓口で解決します。",
        issues=[
            dict(icon="doc", title="許可が取れるか分からず不安",
                 voice="民泊を開業したいが、物件探しから保健所の許可まで、何から始めればいいか分からない。",
                 solve=["物件が法令や保健所の要件を満たせるか、契約前に確認します。", "行政へ事前に相談し、「許可が下りずにお金が無駄になる」ことを防ぎます。"],
                 kpi=["開業までの期間", "投資の手戻り", "許可取得の確実性"]),
            dict(icon="yen", title="いくらかかり、いつ回収できるか分からない",
                 voice="必要な資金と、何年で回収できるのかが見えず、投資に踏み切れない。",
                 solve=["買う・借りるそれぞれの必要資金と回収期間を比べ、無理のない計画を立てます。", "自ら運営する小規模宿の実データをもとに、収支を試算します。"],
                 kpi=["必要な資金", "想定利回り", "回収までの期間"]),
            dict(icon="clock", title="開業後の運営まで手が回るか不安",
                 voice="本業があるので、深夜のチェックインや問い合わせ、清掃まで対応できるか不安。",
                 solve=["AIチャットと24時間サポートで、問い合わせ対応を仕組み化します。", "清掃や予約対応までRIVIAが担い、運営の手間から解放します。"],
                 kpi=["対応にかかる時間", "対応品質", "レビュー評価"]),
            dict(icon="chart", title="始めても利益が残るか分からない",
                 voice="予約サイトの手数料や清掃費を引くと、手元にいくら残るのか見当がつかない。",
                 solve=["稼働率・単価・コストを分析し、利益を圧迫している要因を特定します。", "価格の自動調整と直接予約の強化で、手元に残る利益を増やします。"],
                 kpi=["客単価・稼働率", "予約サイトの手数料", "手元に残る利益"]),
        ],
        steps=[
            ("事業構想・物件診断", "2週間", "予算を決め、物件が許可を取れるかを確認します。"),
            ("コンセプト設計・許認可サポート", "1ヶ月", "コンセプトを決め、許可の申請に伴走します。"),
            ("開業準備・運営体制づくり", "1ヶ月", "家具・予約サイト・清掃の段取りまで整えます。"),
            ("運営開始・毎月の振り返り", "継続", "毎月のレポートと振り返りで、収益を伸ばします。"),
        ],
        faq=[
            ("宿泊業の経験が全くなくても開業できますか？", "はい。立地選定や許認可から開業準備まで伴走し、運営の実務もお伝えします。運営をRIVIAにお任せいただくこともできます。"),
            ("すでに営業中の民泊・小規模宿でも依頼できますか？", "このサービスは、これから民泊・小規模宿を始める方向けです。営業中の施設の集客については、「WEB集客支援事業」でご相談いただけます。"),
            ("法人の新規事業として、民泊を始めたい場合も相談できますか？", "はい。工務店や不動産会社など、新規事業として宿泊施設を始めたい法人様からのご相談もお受けしています。事業計画から開業・運営まで支援します。"),
            ("料金の体系はどうなっていますか？", "運営をお任せいただく場合は、任せる業務の範囲に応じて売上の10〜20%を手数料としていただきます（物件の取得や改修などの初期費用はオーナー様のご負担です）。初期費用をRIVIAと共同出資し、出資の割合に応じて利益を分け合うプランもあります。"),
            ("毎月のレポートでは、何が分かりますか？", "稼働率・客単価・売上・レビューなどを毎月まとめてお送りし、オンラインで振り返りの場を設けます。次の月に何をするかまで、一緒に決めます。"),
            ("夜間の緊急対応も任せられますか？", "はい。多言語AIチャットボットと24時間体制のオンラインサポートで、深夜の問い合わせや駆けつけ対応も代行します。"),
        ],
    ),
    "partnership": dict(
        message=["保有する不動産を、", "選ばれる投資商品へ。"],
        description="不動産会社様との協業事業です。保有物件の中から民泊に適した物件をRIVIAが選定・利回りを算出し、不動産会社様が投資家様へ販売。購入後はRIVIAが開業・運営を担い、家賃や収益を投資家様へお返しします。",
        overview="不動産会社様の保有物件を民泊の投資物件として販売できるよう、選定から購入後の運営まで担います。",
        issues_lead="売れない理由は価格だけではありません。投資商品としての魅力を一緒につくります。",
        issues=[
            dict(icon="house", title="通常の賃貸・売買では、物件の魅力が伝わりにくい",
                 voice="地方や築年数の古い物件は、一般的な賃貸の利回りでは投資家に響かず、販売が長期化してしまう。",
                 solve=["立地や建物の特徴をふまえ、民泊として収益が見込める物件をRIVIAが選定します。", "「宿として運営すれば、この利回り」という新しい切り口で、物件の価値を伝えます。"],
                 kpi=["販売までの期間", "販売価格", "問い合わせ数"]),
            dict(icon="chart", title="想定利回りの根拠を示せない",
                 voice="民泊なら高利回りと言われても裏付けがなく、投資家に自信を持って説明できない。",
                 solve=["市場データと自社の運営実績をもとに、根拠のある利回りを算出します。", "販売資料に使える形でご用意し、ご要望に応じて投資家様向けの説明会にも登壇します。"],
                 kpi=["収支計画の精度", "成約率", "投資家からの信頼"]),
            dict(icon="key", title="購入後の運営を任せられる先がない",
                 voice="投資家から「買った後は誰が運営してくれるのか」と聞かれても、紹介できる運営会社がない。",
                 solve=["購入後は、RIVIAが開業準備から集客・清掃・ゲスト対応まで一括で担います。", "家賃や収益の分配、毎月のレポートまで、手間をかけない形でお返しします。"],
                 kpi=["投資家の運営負担", "購入後の稼働率", "収益の安定性"]),
            dict(icon="doc", title="許認可や改修の要否がわからない",
                 voice="宿泊施設として使えるのか、どこまで改修が必要なのかが分からず、販売前の整備に踏み切れない。",
                 solve=["旅館業法・民泊新法・消防法の要件を確認し、宿にできるかを事前に判定します。", "改修の範囲と概算費用を整理し、販売前か購入後か、実施時期の判断をお手伝いします。"],
                 kpi=["許認可取得の確実性", "改修費用", "開業までの期間"]),
        ],
        steps=[
            ("物件の選定・利回りの算出", "2〜3週間", "保有物件から民泊向きの物件を選び、根拠のある利回りを出します。", "不動産会社様へのご支援"),
            ("販売資料・説明会のサポート", "販売期間中", "販売資料をご用意し、ご要望に応じて投資家様向けの説明会にも登壇します。", "不動産会社様へのご支援"),
            ("購入後の開業準備", "1〜3ヶ月", "物件を購入された投資家様に代わり、許可申請・改修・予約サイト掲載まで進めます。", "投資家様へのご支援"),
            ("運営・収益のお返し", "開業後〜", "運営はRIVIAが担い、投資家様へ収益と月次レポートをお届けします。", "投資家様へのご支援"),
        ],
        faq=[
            ("どのような物件が対象になりますか？", "戸建て・古民家・小規模な一棟アパートなど、宿泊施設として運営できる可能性のある物件が対象です。地方や築年数の古い物件でも、まずは一度ご相談ください。"),
            ("投資家様への販売は、どなたが行いますか？", "投資家様へのご案内と販売は、不動産会社様に説明会やメールマガジンなどで行っていただきます。RIVIAは物件の選定と利回りの算出、販売資料のご用意を担い、ご要望に応じて説明会にも登壇します。"),
            ("投資家様への利回りは保証されますか？", "契約の形によって異なります。家賃を固定でお支払いする形のほか、売上に連動して収益をお返しする形もあります。物件と投資家様のご意向に合わせてご提案します。"),
            ("RIVIAはどのように収益を得るのですか？", "物件の購入後、RIVIAが開業・運営を担い、宿泊の売上の一部を運営の対価としていただきます。投資家様には、家賃や収益の分配という形でお返しします。"),
        ],
    ),
}



def faq_html(items):
    return "\n".join(
        f"""          <details class="faq__item">
            <summary class="faq__q"><span class="faq__mark">Q</span><span>{e(q)}</span><span class="faq__toggle" aria-hidden="true"></span></summary>
            <div class="faq__a"><span class="faq__mark">A</span><p>{e(a)}</p><span></span></div>
          </details>"""
        for q, a in items
    )


# ---------------------------------------------------------------- プラン例（アキヤド空き家再生・開業コンサル）
# 数字はすべて「一例」。物件の立地・規模・改修内容により個別に設計する前提で表示する。
PLAN_AXES = {
    "operation": ["初期費用の負担", "毎月の収入", "収益の伸びしろ"],
    "management": ["運営への関わり", "ノウハウ", "RIVIAへの報酬"],
    "marketing": ["費用の目安", "社内の手間", "RIVIAの対応範囲"],
    "recruit": ["費用の目安", "社内の手間", "RIVIAの対応範囲"],
}
# 初期費用・業務の分担（誰が負担／担当するか）。owner / rivia / half
SPLIT_ITEMS = {
    "operation": ("初期費用の負担", ["建物の補修", "内装リフォーム", "消防・許可申請", "家具・家電・備品", "毎月の運営費"]),
    "management": ("費用・業務の分担", ["物件取得", "改修・家具の費用", "開業準備・許認可", "集客・価格の調整", "ゲスト対応・清掃"]),
    "marketing": ("業務の分担", ["集客戦略・KPIの設計", "予約・ポータルサイトの運用改善", "自社サイト・導線の構築", "広告・SNS・SEOの運用"]),
    "recruit": ("業務の分担", ["採用計画・採用要件の設計", "求人原稿・採用ページの作成", "求人媒体・広告の運用、スカウト", "応募者対応・面接調整", "面接・採用の決定"]),
}
PLANS = {
    "operation": dict(
        title="オーナー様の収益プラン例",
        lead="改修から運営までRIVIAが担います。「貸す」なら2つ、「手放す」なら買取の、3つのプラン例から選べます。",
        scheme=dict(
            owner=("key", "オーナー様", "物件を貸す・売る", ["建物をRIVIAに貸す、または売る", "建物の構造部分の補修（貸す場合）"]),
            prop=("house", "空き家", "宿泊施設に再生"),
            rivia=("sparkle", "RIVIA", "改修・運営", ["改修・家具など開業準備", "集客・予約・清掃・接客"]),
            left="賃貸借契約", right="改修・運営",
            money=[("users", "ゲスト（宿泊者）"), ("sparkle", "RIVIA"), ("key", "オーナー様")],
            money_labels=["宿泊料金", "家賃（＋売上に応じた上乗せ）"],
            summary="「貸す」か「売る」かを選ぶだけ。運営の手間はかかりません。",
            third=("ゲスト（宿泊者）", "宿に滞在", ["暮らすように旅する滞在", "宿泊料金を支払う"]),
            tri=[("left", [("① 物件を貸す・売る", "rev"), ("④ 家賃・売却代金", "fwd")], False),
                 ("right", [("② 宿として運営・おもてなし", "rev"), ("③ 宿泊料金", "fwd")], False),
                 ("bottom", [("思い出の家が、旅人の滞在先に", "none")], True)],
        ),
        plans=[
            dict(split=["rivia", "rivia", "rivia", "rivia", "rivia"], name="おまかせコース", brand="アキヤド借り上げプラン", catch="初期費用をかけず、毎月決まった家賃を受け取る",
                 owner_share=10, init="改修・家具などの初期費用は、RIVIAがほぼ全額を負担します（建物の構造的な補修のみオーナー様）。",
                 monthly="毎月、決まった額の家賃", example="例：毎月 3万円（一定）",
                 ratings=[("ほぼなし", "good"), ("毎月一定", "good"), ("控えめ", "low")], who=["手間もお金もかけずに空き家を活かしたい", "毎月の収入を安定させたい"], rec=True),
            dict(split=["share", "share", "rivia", "rivia", "rivia"], name="売上シェアコース", brand="アキヤド借り上げプラン", catch="補修・内装をRIVIAと共同出資し、家賃＋売上に応じた上乗せを受け取る",
                 owner_share=45, init="建物の補修・内装リフォームはオーナー様とRIVIAで共同出資し、消防設備・家具・開業準備はRIVIAが負担します。",
                 monthly="最低保証の家賃 ＋ 売上の一定割合", example="例：最低保証 2.5万円 ＋ 売上の10%",
                 ratings=[("一部を負担", "mid"), ("最低保証＋上乗せ", "good"), ("売上に応じて増える", "mid")], who=["安定した収入を確保しつつ、繁忙期の上振れも受け取りたい", "補修・内装の費用を一部なら出せる"], rec=False),
            dict(split=["rivia", "rivia", "rivia", "rivia", "rivia"], name="アキヤド買取プラン", catch="物件をRIVIAが買い取り、宿として再生・運営する",
                 owner_share=0, init="", money_label="受け取り方",
                 monthly="売却代金をまとめて受け取る", example="例：現地を拝見して査定",
                 ratings=[("なし", "good"), ("なし（一括で受取）", "low"), ("売却代金のみ", "low")], who=["将来使う予定がない", "管理や相続の手間をなくしたい"], rec=False,
                 cta="買取について相談する"),
        ],
        note="※ 金額・割合はイメージです。条件は物件ごとにご提案します。契約は更新を前提としています。",
        advice="相続した空き家なら「アキヤド借り上げプラン」のおまかせコースがおすすめです。<br>ご自身で運営に関わり、より大きな利益を目指すなら<a href=\"service-management.html\">アキヤド開業・運営支援</a>がおすすめです。",
    ),
    "management": dict(
        title="開業・運営のプラン例",
        lead="これから民泊・小規模宿を始める方向けに、運営の任せ方や出資の形で選べる3つのプラン例です。どのプランも開業準備から伴走します。",
        scheme=dict(
            owner=("key", "オーナー様", "投資家・不動産会社", ["物件の取得・改修に投資", "運営をRIVIAに委託"]),
            prop=("house", "民泊・小規模宿", "開業・運営"),
            rivia=("sparkle", "RIVIA", "開業準備・運営の受託", ["許認可・開業準備", "集客・運営（プランによる）"]),
            left="運営委託", right="開業準備・運営",
            money=[("users", "ゲスト（宿泊者）"), ("sparkle", "RIVIA"), ("key", "オーナー様")],
            money_labels=["宿泊料金", "手数料を引いて分配"],
            summary="売上はRIVIAが受け取り、手数料を引いてオーナー様へ分配します。",
            third=("ゲスト（宿泊者）", "民泊に滞在", ["宿を予約・滞在", "宿泊料金を支払う"]),
            tri=[("left", [("① 開業・運営を委託", "rev"), ("④ 売上を分配", "fwd")], False),
                 ("right", [("② 集客・運営（プランによる）", "rev"), ("③ 宿泊料金", "fwd")], False),
                 ("bottom", [("空いた物件が、収益を生む宿に", "none")], True)],
        ),
        plans=[
            dict(split=["owner", "owner", "rivia", "rivia", "owner"], name="伴走コース", brand="アキヤド開業・運営プラン", catch="現場は自分で。開業準備と集客・価格はプロに任せる",
                 owner_share=0, init="",
                 monthly="売上 − 手数料10%", example="例：売上30万円 → 27万円",
                 ratings=[("現場を担う", "good"), ("集客の考え方まで", "mid"), ("手数料10%", "good")], who=["お客様との時間は自分で大切にしたい", "開業準備と集客はプロに任せたい"], rec=True),
            dict(split=["owner", "owner", "rivia", "rivia", "rivia"], name="運営代行コース", brand="アキヤド開業・運営プラン", catch="開業準備から日々の運営まで、まるごと任せる",
                 owner_share=0, init="",
                 monthly="売上 − 運営手数料20%", example="例：売上30万円 → 24万円",
                 ratings=[("経営の判断に集中", "mid"), ("レポートで把握", "mid"), ("手数料20%", "mid")], who=["本業が忙しく、現場に時間をかけられない", "遠方の物件や、複数の施設を持っている"], rec=False),
            dict(split=["share", "share", "rivia", "rivia", "rivia"], name="共同出資コース", brand="アキヤド開業・運営プラン", catch="物件取得と初期費用をRIVIAと共同出資し、利益を分け合う",
                 owner_share=0, init="",
                 monthly="利益を、出資の割合で分配", example="例：出資 6：4 → 利益の60%",
                 ratings=[("経営の判断に集中", "mid"), ("レポートで把握", "mid"), ("出資の割合で", "mid")], who=["初期投資の負担とリスクを抑えたい", "プロと一緒に事業として育てたい"], rec=False),
        ],
        note="※ 金額・割合はイメージです。清掃費などの実費は別途かかります。共同出資コースの利益分配は、開業後も継続します。",
        advice="初めての民泊で、お客様との時間は自分で大切にしたいなら、開業準備と集客をプロに任せられる「アキヤド開業・運営プラン」の伴走コースがおすすめです。",
    ),
    "marketing": dict(
        title="集客支援のプラン例",
        lead="戦略の相談から集客の丸ごとまで。どこまでRIVIAが担うかで、3つのプラン例から選べます。",
        owner_name="事業者様",
        scheme=dict(
            owner=("key", "オーナー様", "施設の経営", ["宿の魅力・サービスをつくる", "方針や予算の最終判断"]),
            prop=("house", "集客チャネル", "OTA・自社サイト・広告・SNS"), prop_en="CHANNEL",
            rivia=("sparkle", "RIVIA", "集客の設計・運用", ["集客戦略・KPIの設計", "OTA・広告・SNSなどの運用（プランによる）"]),
            left="方針の決定", right="設計・運用",
            money=[("users", "ゲスト（宿泊者）"), ("key", "オーナー様"), ("sparkle", "RIVIA")],
            money_labels=["宿泊料金", "集客支援の費用"],
            summary="集客のプロを、必要な分だけ。予約と売上が伸びるしくみをRIVIAがつくります。",
            third=("ゲスト（宿泊者）", "宿を探す・予約する", ["OTA・検索・SNSで宿を比較", "予約して宿泊料金を支払う"]),
            tri=[("left", [("① 集客を依頼", "rev"), ("④ 集客支援の費用", "rev")], False),
                 ("right", [("② OTA・広告・SNSで魅力を届ける", "rev")], False),
                 ("bottom", [("③ 予約・宿泊料金", "rev")], False)],
        ),
        plans=[
            dict(split=["rivia", "owner", "owner", "owner"], name="集客コンサルプラン", catch="集客の戦略づくりと改善のアドバイスを、定期的に受ける",
                 costs=[("コンサル", "月額5万円〜")], monthly="", example="月1回の定例＋改善提案",
                 ratings=[("抑えめ", "good"), ("実行は自社で", "low"), ("戦略・アドバイス", "low")], who=["社内に実行できるスタッフがいる", "まずは現状の課題を整理したい"], rec=False),
            dict(split=["rivia", "rivia", "owner", "rivia"], name="運用代行プラン", catch="広告・SNS・予約サイトの運用をまとめて任せ、成果につなげる",
                 money_label="費用", monthly="個別見積もり", example="事業の状況と組み合わせる施策に応じてお見積もりします",
                 ratings=[("個別見積もり", "mid"), ("ほぼなし", "good"), ("集客の運用まで", "good")], who=["集客に手が回らず、売上が伸び悩んでいる", "予約サイトや広告の見せ方を改善したい"], rec=True),
            dict(split=["rivia", "rivia", "rivia", "rivia"], name="自社サイト構築＋運用プラン", catch="問い合わせ・予約ができる自社サイトをつくり、運用まで任せる",
                 money_label="費用", monthly="個別見積もり", example="サイトの規模と施策に応じてお見積もりします",
                 ratings=[("個別見積もり", "mid"), ("ほぼなし", "good"), ("サイト制作〜運用", "good")], who=["自社サイトがない、または古くて成果につながらない", "リピーターや直接の問い合わせを増やしたい"], rec=False),
        ],
        note="※ 金額はイメージです。広告費などの媒体費は別途実費です。",
        advice="集客に手が回らない事業者様には、広告・SNSなどをまとめて任せられる「運用代行プラン」がおすすめです。",
        money_label="毎月の費用",
    ),
    "recruit": dict(
        title="採用支援のプラン例",
        lead="計画の相談から応募者対応まで。どこまでRIVIAが担うかで、3つのプラン例から選べます。",
        owner_name="事業者様",
        scheme=dict(
            owner=("key", "事業者様", "採用の決定", ["面接・採用の最終判断", "入社後の受け入れ・育成"]),
            prop=("house", "採用活動", "計画・発信・応募対応"), prop_en="HIRING",
            rivia=("sparkle", "RIVIA", "採用の設計・代行", ["採用計画・求人原稿・採用ページ", "媒体運用・応募者対応（プランによる）"]),
            left="採用の決定", right="設計・代行",
            money=[("key", "事業者様"), ("sparkle", "RIVIA")],
            money_labels=["採用支援の費用"],
            summary="採用の「手間」はRIVIAに。事業者様は「誰と働くか」の判断に集中できます。",
            third=("求職者", "応募・入社", ["求人・採用ページで会社を知る", "応募して面接を受ける"]), third_en="CANDIDATE",
            tri=[("left", [("① 採用を依頼", "rev"), ("④ 採用支援の費用", "rev")], False),
                 ("right", [("② 求人・スカウトで魅力を届ける", "rev")], False),
                 ("bottom", [("③ 応募・面接・入社", "rev")], False)],
        ),
        plans=[
            dict(split=["rivia", "owner", "owner", "owner", "owner"], name="採用コンサルプラン", catch="採用計画と求人の打ち手を、プロと一緒に設計する",
                 costs=[("コンサル", "月額5万円〜")], monthly="", example="月1回の定例＋採用計画づくり",
                 ratings=[("抑えめ", "good"), ("実行は自社で", "low"), ("計画・アドバイス", "low")], who=["採用担当者はいるが、打ち手に迷っている", "採用計画から見直したい"], rec=False),
            dict(split=["rivia", "rivia", "rivia", "owner", "owner"], name="求人媒体の運用プラン", catch="求人原稿の作成と媒体・広告の運用を任せ、応募を増やす",
                 costs=[("媒体・広告運用", "広告費＋20%")], monthly="", example="例：広告費30万円なら手数料6万円（原稿作成を含む）",
                 ratings=[("中程度", "mid"), ("応募対応は自社で", "mid"), ("原稿〜媒体運用", "mid")], who=["求人を出しても応募が集まらない", "応募者対応は社内でできる"], rec=False),
            dict(split=["rivia", "rivia", "rivia", "rivia", "owner"], name="採用代行（RPO）プラン", catch="専任の担当者が、広告運用・スカウト・応募者対応まで採用業務をまるごと代行する",
                 costs=[("専任担当 1名", "月額20万円〜"), ("媒体・広告", "広告費＋20%")], monthly="", example="担当1名で広告運用・スカウト・応募者対応まで。増員は人数分",
                 ratings=[("しっかり投資", "low"), ("ほぼなし", "good"), ("応募者対応まで", "good")], who=["採用担当者がいない・手が回らない", "繁忙期までに確実に人を採りたい"], rec=True),
        ],
        note="※ 金額・割合はイメージです。媒体・広告の費用は、広告費に手数料20%を加えた金額です。",
        advice="採用担当がいない企業には、採用業務をまるごと任せられる「採用代行（RPO）プラン」がおすすめです。",
        money_label="毎月の費用",
    ),
}


WHO_LABEL = {"owner": "オーナー様", "rivia": "RIVIA", "half": "折半", "co": "一緒に", "none": "不要", "share": "共同出資"}


NO_SCHEME = {"marketing", "recruit"}   # 三角形の図を出さないサービス


def TRI_NODES(sc, owner_name):
    oic, otitle, orole, oitems = sc["owner"]
    ric, rtitle, rrole, ritems = sc["rivia"]
    gtitle, grole, gitems = sc["third"]
    return dict(
        top=("PARTNER", rtitle, rrole, ritems, "rivia"),
        left=(sc.get("owner_en", "OWNER" if owner_name == "オーナー様" else "CLIENT"), otitle, orole, oitems, "owner"),
        right=(sc.get("third_en", "GUEST"), gtitle, grole, gitems, "investor"),
    )


# プランカードの中身（名前 → 見出しの項目, 一番大事な数字, 一言, 目安1, 目安2）。目安は 0=なし 1=小 2=中 3=大
PLAN_DOTS_AXES = {
    "operation": ("収入の伸びしろ", "初期費用の負担"),
    "management": ("運営の手間", "初期投資の負担"),
    "marketing": ("社内の手間", "RIVIAの対応範囲"),
    "recruit": ("社内の手間", "RIVIAの対応範囲"),
}
PLAN_SIMPLE = {
    "おまかせコース": ("初期費用", "0円", "初期費用をかけず、毎月決まった家賃を受け取る", 1, 0),
    "売上シェアコース": ("初期費用", "共同出資", "補修・内装を共同出資し、家賃＋売上の上乗せを受け取る", 2, 2),
    "アキヤド買取プラン": ("受け取り方", "一括で売却", "物件をRIVIAが買い取り、管理や相続の手間をなくす", 0, 0),
    "伴走コース": ("RIVIAへの報酬", "売上の10%", "現場は自分で。開業準備と集客・価格はプロに任せる", 2, 3),
    "運営代行コース": ("RIVIAへの報酬", "売上の20%", "開業準備から日々の運営まで、まるごと任せる", 1, 3),
    "共同出資コース": ("RIVIAへの報酬", "出資比率で分配", "物件取得と初期費用を共同出資し、利益を分け合う", 1, 2),
    "集客コンサルプラン": ("費用の目安", "月額5万円〜", "集客の戦略づくりと改善のアドバイスを受ける", 3, 1),
    "運用代行プラン": ("費用の目安", "個別見積もり", "広告・SNS・予約サイトの運用をまとめて任せる", 1, 2),
    "自社サイト構築＋運用プラン": ("費用の目安", "個別見積もり", "予約・問い合わせができる自社サイトをつくり、運用まで任せる", 1, 3),
    "採用コンサルプラン": ("費用の目安", "月額5万円〜", "採用計画と求人の打ち手を、プロと一緒に設計する", 3, 1),
    "求人媒体の運用プラン": ("費用の目安", "広告費＋20%", "求人原稿の作成と媒体・広告の運用を任せる", 2, 2),
    "採用代行（RPO）プラン": ("費用の目安", "月額20万円〜", "専任担当が、広告運用から応募者対応まで代行する", 1, 3),
}


# プランの図：1本の帯が右（スマホは下）へ行くほど高く・濃くなる。帯の高さ＝ band の大きさ。
# 各プラン：(プラン名, 帯の数字, (指標1の言葉, 大きさ0-3), (指標2の言葉, 大きさ0-3), 一言)
PLAN_DIAGRAM = {
    "operation": dict(
        band="オーナー様の関わり", m=("毎月の収入", "物件"),
        plans=[("アキヤド買取プラン", "手放す", ("一括", 1), ("売却", 0), "物件をRIVIAが買い取り、管理や相続の手間をなくす"),
               ("おまかせコース", "貸す", ("一定", 2), ("残る", 2), "初期費用0円で、毎月決まった家賃を受け取る"),
               ("売上シェアコース", "出資して貸す", ("上乗せ", 3), ("残る", 2), "補修・内装を共同出資し、家賃＋売上の上乗せを受け取る")]),
    "management": dict(
        band="RIVIAへの報酬", m=("運営の手間", "初期投資"),
        plans=[("伴走コース", "売上の10%", ("中", 2), ("全額", 3), "現場は自分で。開業準備と集客・価格はプロに任せる"),
               ("運営代行コース", "売上の20%", ("小", 1), ("全額", 3), "開業準備から日々の運営まで、まるごと任せる"),
               ("共同出資コース", "出資比率で分配", ("小", 1), ("一部", 2), "物件取得と初期費用を共同出資し、利益を分け合う")]),
}


def brand_kicker(p):
    """コースの上に、属する「アキヤド〇〇プラン」の名前を小さく出す"""
    return f'<span class="plan-brand">{e(p["brand"])}</span>' if p.get("brand") else ""


def plan_diagram(key):
    g = PLAN_DIAGRAM[key]
    by_name = {p["name"]: p for p in PLANS[key]["plans"]}
    m1, m2 = g["m"]
    cols = []
    for i, (name, val, (w1, s1), (w2, s2), desc) in enumerate(g["plans"], 1):
        p = by_name[name]
        badge = '<span class="pd__badge">おすすめ</span>' if p["rec"] else ""
        cols.append(f"""          <div class="pd__plan pd__plan--{i}">
            <div class="pd__seg">
              {badge}{brand_kicker(p)}<p class="pd__name">{e(name)}</p>
              <p class="pd__label">{e(g["band"])}</p>
              <p class="pd__value">{e(val)}</p>
            </div>
            <div class="pd__body">
              <div class="pd__metrics">
                <div><span>{e(m1)}</span><b class="pd__c pd__c--a pd__c--{s1}">{e(w1)}</b></div>
                <div><span>{e(m2)}</span><b class="pd__c pd__c--b pd__c--{s2}">{e(w2)}</b></div>
              </div>
              <p class="pd__desc">{e(desc)}</p>
              <a href="contact.html?category={key}" class="pd__cta">{"買取を相談する" if p.get("cta") else ("このコースを相談する" if p.get("brand") else "このプランを相談する")} {ARROW}</a>
            </div>
          </div>""")
    return '        <div class="pd reveal">\n' + "\n".join(cols) + "\n        </div>"


def plans_section(key):
    if key not in PLANS:
        return ""
    d = PLANS[key]
    sc = d["scheme"]
    axes = PLAN_AXES[key]
    split_label, split_items = SPLIT_ITEMS[key]
    scheme_html = "" if key in NO_SCHEME else f"""        <div class="scheme reveal">
          <p class="scheme__head">しくみ</p>
          {flow_html(key) if key in FLOWS else tri_html(TRI_NODES(sc, d.get("owner_name", "オーナー様")), sc["tri"])}
          <p class="scheme__summary">{e(sc["summary"])}</p>
        </div>
"""
    owner_name = d.get("owner_name", "オーナー様")
    who_label = dict(WHO_LABEL, owner=owner_name)

    def node(n, cls):
        ic, title, role, items = n
        lis = "".join(f"<li>{e(x)}</li>" for x in items)
        return f"""<div class="scheme__node scheme__node--{cls}">
              <span class="scheme__en">{"PARTNER" if cls == "rivia" else sc.get("owner_en", "OWNER" if owner_name == "オーナー様" else "CLIENT")}</span>
              <p class="scheme__title">{e(title)}</p>
              <p class="scheme__role">{e(role)}</p>
              <ul class="scheme__list">{lis}</ul>
            </div>"""

    pic, ptitle, prole = sc["prop"]
    money = []
    for i, (ic, label) in enumerate(sc["money"]):
        who = "rivia" if label == "RIVIA" else ("owner" if label == owner_name else "guest")
        money.append(f'<div class="flow-chip flow-chip--{who}">{e(label)}</div>')
        if i < len(sc["money_labels"]):
            money.append(f'<div class="flow-arrow"><span>{e(sc["money_labels"][i])}</span></div>')

    # WEBマーケティング（集客・採用）は支援内容が伝わるよう、分担表・費用・こんな方にを載せた詳しいカード
    cards = []
    for i, p in enumerate(d["plans"], 1):
        rows = "".join(
            f'<li><span class="plan__axis">{e(a)}</span><span class="plan__val plan__val--{lv}">{e(t)}</span></li>'
            for a, (t, lv) in zip(axes, p["ratings"]))
        who = "".join(f"<li>{e(w)}</li>" for w in p["who"])
        split = "".join(
            f'<li><span class="plan__split-item">{e(it)}</span><span class="who who--{w}">{who_label[w]}</span></li>'
            for it, w in zip(split_items, p["split"]))
        badge = '<span class="plan__badge">おすすめ</span>' if p["rec"] else ""
        cards.append(f"""          <article class="plan{' plan--rec' if p['rec'] else ''} reveal" data-delay="{i - 1}">
            {badge}<span class="plan__no">PLAN {i:02d}</span>
            {brand_kicker(p)}<h3 class="plan__name">{e(p["name"])}</h3>
            <p class="plan__catch">{e(p["catch"])}</p>
            <div class="plan__block">
              <span class="plan__label">{e(split_label)}</span>
              <ul class="plan__split{' plan__split--tall' if max(len(x) for x in split_items) > 10 else ''}">{split}</ul>
            </div>
            <div class="plan__block plan__money">
              <span class="plan__label">{p.get("money_label", d.get("money_label", "毎月の受け取り方"))}</span>
              {('<dl class="plan__costs">' + "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in p["costs"]) + "</dl>") if p.get("costs") else f'<p class="plan__monthly">{e(p["monthly"]).replace(chr(10), "<br>")}</p>'}
              <p class="plan__example">{e(p["example"])}</p>
            </div>
            <div class="plan__who">
              <span class="plan__label">こんな方に</span>
              <ul>{who}</ul>
            </div>
            <a href="contact.html?category={key}" class="plan__cta">{e(p.get("cta", "このプランについて相談する"))} {ARROW}</a>
          </article>""")

    detailed_cards = cards
    plans_html = plan_diagram(key) if key in PLAN_DIAGRAM else f"""        <div class="plans__legend reveal"><span class="plans__legend-text">色の見方</span><span class="who who--owner">{e(owner_name)}</span><span class="who who--rivia">RIVIA</span>{'<span class="who who--half">折半</span>' if any("half" in p["split"] for p in d["plans"]) else ""}{'<span class="who who--co">一緒に</span>' if any("co" in p["split"] for p in d["plans"]) else ""}{'<span class="who who--share">共同出資</span>' if any("share" in p["split"] for p in d["plans"]) else ""}</div>
        <div class="plans plans--{len(d["plans"])}">
{chr(10).join(detailed_cards)}
        </div>"""

    # プランは「一番大事な数字」と、2つの目安（小・中・大）、一言だけのシンプルなカードで見せる
    ax1, ax2 = PLAN_DOTS_AXES[key]
    lv_word = {0: "なし", 1: "小", 2: "中", 3: "大"}

    def dots(axis, lv):
        marks = "".join(f'<i class="{"on" if n <= lv else ""}"></i>' for n in (1, 2, 3))
        return f'<li><span class="pcard__axis">{e(axis)}</span><span class="pcard__dots" aria-hidden="true">{marks}</span><span class="pcard__lv">{lv_word[lv]}</span></li>'

    cards = []
    n = len(d["plans"])
    for i, p in enumerate(d["plans"], 1):
        label, value, desc, l1, l2 = PLAN_SIMPLE[p["name"]]
        badge = '<span class="pcard__badge">おすすめ</span>' if p["rec"] else ""
        cards.append(f"""          <article class="pcard{' pcard--rec' if p['rec'] else ''} reveal" data-delay="{i - 1}">
            <div class="pcard__head pcard__head--{i if n == 3 else i + 1}">
              {badge}{brand_kicker(p)}<p class="pcard__name">{e(p["name"])}</p>
              <p class="pcard__label">{e(label)}</p>
              <p class="pcard__value">{e(value)}</p>
            </div>
            <div class="pcard__body">
              <ul class="pcard__meter">{dots(ax1, l1)}{dots(ax2, l2)}</ul>
              <p class="pcard__desc">{e(desc)}</p>
              <a href="contact.html?category={key}" class="pcard__cta">{e(p.get("cta", "このプランについて相談する"))} {ARROW}</a>
            </div>
          </article>""")

    return f"""    <section class="section section--soft" id="plans">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Plans</span>
          <h2 class="section-title">{e(d["title"])}</h2>
          <p class="section-lead">{e(d["lead"])}</p>
        </div>

{scheme_html}
{plans_html}
        <p class="plans__note">{e(d["note"])}</p>
        <div class="plans__advice reveal"><span class="plans__advice-label">RIVIAからのアドバイス</span><p class="plans__advice-text">{d["advice"]}</p></div>
      </div>
    </section>

"""


def tri_html(nodes, edges):
    """三者の関係を三角形で描く。edges: (pos, [(ラベル, 向き), ...], 点線)。
    pos: left=上→左下 / bottom=左下→右下 / right=右下→上。向き: fwd / rev / none（辺の向きに対して）。
    1つの番号に1本の矢印を描く。同じ辺に2つの流れがあるときは、2本の矢印を平行に並べる。
    PCは各矢印の横に説明を、スマホは矢印の上に番号だけを置き、説明は図の下に番号順で並べる。"""
    import math
    def node(pos):
        en, title, role, items, cls = nodes[pos]
        lis = "".join(f"<li>{e(x)}</li>" for x in items)
        return f"""<div class="tri__node tri__node--{pos} tri__node--{cls}">
              <span class="scheme__en">{e(en)}</span>
              <p class="scheme__title">{e(title)}</p>
              <p class="scheme__role">{e(role)}</p>
              <ul class="scheme__list">{lis}</ul>
            </div>"""
    def layout(cls, W, H, T, L, R, cuts, gap, lab_out, lab_in):
        C = ((T[0] + L[0] + R[0]) / 3, (T[1] + L[1] + R[1]) / 3)
        ends = {"left": (T, L, cuts[0], cuts[1]), "bottom": (L, R, cuts[2], cuts[2]), "right": (R, T, cuts[1], cuts[0])}
        lines, marks = [], []
        for pos, flows, dashed in edges:
            a, b, ca, cb = ends[pos]
            dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy); ux, uy = dx / n, dy / n
            px, py = -uy, ux                      # 辺に垂直な向き（外側を正にそろえる）
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if (mx + px - C[0]) ** 2 + (my + py - C[1]) ** 2 < (mx - C[0]) ** 2 + (my - C[1]) ** 2:
                px, py = -px, -py
            k = len(flows)
            for idx, (label, direction) in enumerate(flows):
                off = 0 if k == 1 else (gap / 2 if idx == 0 else -gap / 2)   # 1本目を外側、2本目を内側に
                x1, y1 = a[0] + ux * ca + px * off, a[1] + uy * ca + py * off
                x2, y2 = b[0] - ux * cb + px * off, b[1] - uy * cb + py * off
                attrs = ""
                if direction == "fwd":
                    attrs += f' marker-end="url(#{cls}-a)"'
                if direction == "rev":
                    attrs += f' marker-start="url(#{cls}-s)"'
                if dashed:
                    attrs += ' class="is-dashed"'
                lines.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"{attrs}/>')
                side = 1 if (k == 1 or idx == 0) else -1
                d = lab_out if side == 1 else lab_in
                lx, ly = mx + px * (off + side * d), my + py * (off + side * d)
                t = 0.5 if k == 1 else (0.36 if idx == 0 else 0.64)
                bx, by = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
                ax = 0 if pos == "bottom" else (1 if lx > mx + px * off else -1)   # 線の右側なら左寄せ、左側なら右寄せ
                marks.append((pos, idx, label, dashed, lx / W * 100, ly / H * 100, bx / W * 100, by / H * 100, ax))
        svg = f"""<svg class="tri__lines {cls}" viewBox="0 0 {W} {H}" aria-hidden="true">
            <defs>
              <marker id="{cls}-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z"/></marker>
              <marker id="{cls}-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 L0 5 L10 10z"/></marker>
            </defs>
            {"".join(lines)}
          </svg>"""
        return svg, marks
    pc, pc_marks = layout("tri-pc", 1000, 740, (500, 110), (200, 630), (800, 630), (125, 125, 165), 22, 26, 26)
    sp, sp_marks = layout("tri-sp", 1000, 800, (500, 130), (190, 667), (810, 667), (160, 160, 190), 64, 0, 0)
    labels = "".join(
        f'<p class="tri__label{" is-soft" if dashed else ""}" style="left:{lx:.1f}%;top:{ly:.1f}%;transform:translate({ {-1: "-100%", 0: "-50%", 1: "0"}[ax]}, -50%)">{e(label)}</p>'
        for pos, idx, label, dashed, lx, ly, _, _, ax in pc_marks)
    nums = "".join(
        f'<span class="tri__num" style="left:{mx:.1f}%;top:{my:.1f}%">{"①②③④⑤⑥⑦⑧⑨".index(label[:1]) + 1}</span>'
        for pos, idx, label, dashed, _, _, mx, my, _ in sp_marks if not dashed)
    items = sorted((label for _, flows, dashed in edges if not dashed for label, _ in flows), key=lambda t: t[:1])
    steps = "".join(f'<li><span class="tri__step-no">{e(t[:1])}</span>{e(t[1:].strip())}</li>' for t in items)
    return f"""<div class="tri">
          {pc}
          {sp}
          {node("top")}
          {node("left")}
          {node("right")}
          {labels}
          {nums}
        </div>
        <ol class="tri__steps">{steps}</ol>"""


# ---------------------------------------------------------------- しくみ（左から右へ流れるシンプルな図）
# nodes: (アイコン, 名前, 役割)  links: (契約の種類, 右へ流れるもの, 左へ戻るもの)
FLOWS = {
    "operation": dict(
        nodes=[("key", "オーナー様", "空き家の所有者"), ("sparkle", "RIVIA", "改修・宿の運営"), ("users", "ゲスト", "宿泊者")],
        links=[("賃貸借契約 または 売却", "物件を貸す・売る", "家賃・売却代金"), ("宿泊予約", "暮らすように旅する滞在", "宿泊料金")],
        note="改修費はRIVIAが負担することも可能です",
    ),
    "management": dict(
        nodes=[("key", "オーナー様", "投資家・不動産会社"), ("sparkle", "RIVIA", "開業準備・運営"), ("users", "ゲスト", "宿泊者")],
        links=[("運営委託契約", "開業・運営を委託", "売上を分配（手数料を差し引き）"), ("宿泊予約", "集客・おもてなし", "宿泊料金")],
        note="物件の取得・改修はオーナー様のご負担です（共同出資も可能）",
    ),
    "partnership": dict(
        nodes=[("house", "不動産会社様", "物件の販売"), ("users", "投資家様", "物件の購入・保有"), ("sparkle", "RIVIA", "開業準備・運営")],
        links=[("売買契約", "民泊向きの物件を販売", "売買代金"), ("運営委託契約", "購入後の運営を委託", "家賃・収益をお返し")],
        note="販売しにくかった物件も、民泊としての利回りを示すことで売れる商品になります",
    ),
}


def flow_html(key):
    f = FLOWS[key]
    parts = []
    for i, (ic, title, role) in enumerate(f["nodes"]):
        if i:
            pill, fwd, back = f["links"][i - 1]
            parts.append(f"""<div class="sflow__link">
              <span class="sflow__pill">{e(pill)}</span>
              <span class="sflow__fwd">{e(fwd)}</span>
              {f'<span class="sflow__back">{e(back)}</span>' if back else ''}
            </div>""")
        rivia = " sflow__node--rivia" if title == "RIVIA" else ""
        parts.append(f"""<div class="sflow__node{rivia}">
              <p class="sflow__title">{e(title)}</p>
              <p class="sflow__role">{e(role)}</p>
            </div>""")
    return f"""<div class="sflow">
            {"".join(parts)}
          </div>
          <p class="sflow__note">{e(f["note"])}</p>"""


# ---------------------------------------------------------------- 協業スキーム（三角形の図）
TRIANGLES = {
    "partnership": dict(
        title="協業のしくみ",
        lead="RIVIAが物件を見極め、不動産会社様が投資家様へご案内し、購入後はRIVIAが運営を担います。",
        nodes=dict(
            top=("PARTNER", "RIVIA", "物件の選定・開業・運営", ["保有物件から民泊に適した物件を選定", "利回りを算出し、販売用の資料を用意", "購入後の開業準備と日々の運営"], "rivia"),
            left=("REAL ESTATE", "不動産会社様", "投資家様へのご案内・販売", ["説明会・メールマガジンで投資家様へご案内", "物件の販売"], "owner"),
            right=("INVESTOR", "投資家様", "物件の購入・保有", ["物件を購入し、運営をRIVIAへ", "家賃・収益を受け取る"], "investor"),
        ),
        edges=[
            ("left", [("① 民泊に適した物件の選定・利回りの算出", "fwd")], False),
            ("bottom", [("② 説明会・メールマガジンでご案内し、販売", "fwd")], False),
            ("right", [("③ 運営をRIVIAへ", "fwd"), ("④ 家賃・収益をお返し", "rev")], False),
        ],
        note="※ 投資家様向けの説明会は、ご要望に応じてRIVIAも登壇・実施します。",
        summary="不動産会社様・投資家様・RIVIAの三者それぞれにメリットのある協業です。",
    ),
}


def triangle_section(key):
    if key not in TRIANGLES:
        return ""
    t = TRIANGLES[key]
    return f"""    <section class="section section--soft" id="scheme">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Scheme</span>
          <h2 class="section-title">{e(t["title"])}</h2>
          <p class="section-lead">{e(t["lead"])}</p>
        </div>
        <div class="scheme reveal">
          {flow_html(key) if key in FLOWS else tri_html(t["nodes"], t["edges"])}
        </div>
        <p class="plans__note">{e(t["note"])}</p>
        <p class="scheme__summary reveal">{e(t["summary"])}</p>
      </div>
    </section>

"""


# 対応エリア（全国可。今後の展開に合わせて、具体的な地域名は出さない）
AREA_NOTE = {
    "webmarketing": "オンライン対応",
}


def area_html(key):
    g = next(g["key"] for g in GROUPS if key in g["services"])
    note = AREA_NOTE.get(g)
    return f'<p class="area-note reveal" data-delay="2"><span>対応エリア</span>全国可{"・" + e(note) if note else ""}</p>'


def quick_form(key, name):
    """サービスページ冒頭の、かんたんな相談フォーム（名前とメールだけで送れる）"""
    return f"""        <form class="qform reveal" data-delay="2" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" enctype="multipart/form-data" data-thanks="thanks.html?form=contact">
          <p class="qform__title">{e(name)}の無料相談</p>
          <p class="qform__lead">まだ検討中の段階でも大丈夫です。2営業日以内にご連絡します。</p>
          <input type="hidden" name="_subject" value="【RIVIA&amp;CO.】{e(name)}のご相談（サービスページ）">
          <input type="hidden" name="ご相談カテゴリ" value="{e(name)}">
          <input type="hidden" name="流入元" value="サービスページ：{e(name)}">
          <label class="qform__field"><span>お名前 <em>必須</em></span><input type="text" name="name" placeholder="山田 太郎" autocomplete="name" required></label>
          <label class="qform__field"><span>メールアドレス <em>必須</em></span><input type="email" name="email" placeholder="your@email.com" autocomplete="email" required></label>
          <label class="qform__field"><span>ご相談内容 <small>任意</small></span><textarea name="message" rows="3" placeholder="物件の場所や、気になっていることなど"></textarea></label>
          <label class="qform__field qform__file"><span>ファイル <small>任意・物件の写真や図面など</small></span><input type="file" name="attachment" multiple accept="image/*,.pdf,.doc,.docx,.xls,.xlsx"></label>
          <button type="submit" class="btn qform__submit">無料で相談する {ARROW}</button>
          <p class="qform__note">送信により<a href="privacy.html">プライバシーポリシー</a>に同意したものとします。しつこい営業はしません。</p>
        </form>"""


def service_page(key, name):
    d = SERVICE_DATA[key]


    # 個人のお客様向けのサービスは「経営」ではなく、暮らしの言葉で見せる
    personal = key in dict((a["key"], [k for _, ks in a["groups"] for k in ks]) for a in NAV_AUDIENCES)["personal"]
    lbl = (dict(label="お悩み", scene="よくあるお声", kpi="変わること") if personal else
           dict(label="経営課題", scene="現場で起きていること", kpi="改善する経営指標"))
    issues = []
    for i, it in enumerate(d["issues"], 1):
        solve = "".join(f'<li><span class="issue__step-num">{n}</span><p>{e(p)}</p></li>' for n, p in enumerate(it["solve"], 1))
        kpi = "".join(f"<li>{e(k)}</li>" for k in it["kpi"])
        issues.append(f"""          <article class="issue reveal">
            <div class="issue__problem">
              <div class="issue__head">
                <p class="issue__meta"><span class="issue__num">ISSUE {i:02d}</span><span class="issue__label">{lbl["label"]}</span></p>
              </div>
              <h3 class="issue__title">{e(it["title"])}</h3>
              <div class="issue__scene">
                <span class="issue__sublabel">{lbl["scene"]}</span>
                <p class="issue__voice">{e(it["voice"])}</p>
              </div>
            </div>
            <div class="issue__bridge" aria-hidden="true"><span></span></div>
            <div class="issue__answer">
              <span class="issue__sublabel issue__sublabel--accent">RIVIAの打ち手</span>
              <ol class="issue__steps">{solve}</ol>
              <div class="issue__kpi">
                <span class="issue__sublabel">{lbl["kpi"]}</span>
                <ul>{kpi}</ul>
              </div>
            </div>
          </article>""")
    issues_html = "\n".join(issues)

    steps = "\n".join(
        f"""          <li class="timeline__step reveal" data-delay="{i - 1}">
            <span class="timeline__num">STEP {i:02d}{f'<span class="timeline__for timeline__for--{"inv" if "投資家" in st[3] else "re"}">{e(st[3])}</span>' if len(st) > 3 else ""}</span>
            <h3 class="timeline__title">{e(st[0])}</h3>
            <span class="timeline__term">{e(st[1])}</span>
            <p class="timeline__desc">{e(st[2])}</p>
          </li>"""
        for i, st in enumerate(d["steps"], 1)
    )

    names = dict(SERVICES)
    related_groups = []
    for g in GROUPS:
        cards = "\n".join(
            f"""            <a href="service-{k}.html" class="related__card reveal">
              <span class="related__worry">「{e(PERSONAS[k])}」</span>
              <span class="related__name">{e(names[k])} {ARROW}</span>
            </a>"""
            for k in g["services"] if k != key
        )
        if not cards:
            continue
        own = key in g["services"]
        label = g["name"]
        related_groups.append((not own, f"""        <div class="related-group">
          <p class="group-label"><span>{e(g["en"])}</span>{e(label)}</p>
          <div class="related">
{cards}
          </div>
        </div>"""))
    # 同じ領域を先に表示
    related_groups.sort(key=lambda t: t[0])
    related = "\n".join(h for _, h in related_groups)

    ph, pw, phh, ppos, *bright = SERVICE_PHOTOS[key]
    body = f"""    <section class="page-hero page-hero--photo{" page-hero--bright" if bright else ""}">
      <img class="page-hero__bg" src="images/photos/{ph}.jpg" alt="" width="{pw}" height="{phh}" style="object-position:{ppos}" fetchpriority="high" decoding="async">
      <div class="container svc-hero">
        <div class="svc-hero__text">
          <p class="page-hero__label reveal">{e(name)}</p>
          <h1 class="page-hero__title reveal" data-delay="1">{br(d["message"])}</h1>
          <p class="page-hero__target reveal" data-delay="2"><span>こんな方へ</span>「{e(PERSONAS[key])}」</p>
          <div class="page-hero__actions reveal" data-delay="2">
            <a href="#{key}-issues" class="btn btn--ghost btn--on-photo">お悩みと解決策を見る</a>
          </div>
        </div>
{quick_form(key, name)}
      </div>
    </section>

    <section class="section section--overview">
      <div class="container overview">
        <div class="reveal">
          <span class="eyebrow">Overview</span>
          <h2 class="section-title">サービス概要</h2>
        </div>
        <div>
          <p class="overview__text reveal" data-delay="1">{e(d["overview"])}</p>
          {area_html(key)}
        </div>
      </div>
    </section>

    <section class="section section--soft" id="{key}-issues">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Issues &amp; Solutions</span>
          <h2 class="section-title">こんなお悩みはありませんか？</h2>
          <p class="section-lead">{e(d["issues_lead"])}</p>
        </div>
        <div class="issues">
{issues_html}
        </div>
      </div>
    </section>

    <section class="section" id="flow">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Process</span>
          <h2 class="section-title">ご支援の流れ（一例）</h2>
          <p class="section-lead">内容や期間は、お選びいただくプランや状況によって変わります。</p>
        </div>
        <ol class="timeline">
{steps}
        </ol>
      </div>
    </section>

{plans_section(key)}{triangle_section(key)}    <section class="section" id="project">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Project</span>
          <h2 class="section-title">RIVIAの運営実績</h2>
        </div>
{project_card(compact=True)}
{reviews_html()}      </div>
    </section>

{cta(key, text=OPEN_MSG if key in GROUPS[0]["services"] else "")}

    <section class="section" id="faq">
      <div class="container container--narrow">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">FAQ</span>
          <h2 class="section-title">よくあるご質問</h2>
        </div>
        <div class="faq reveal">
{faq_html(d["faq"])}
        </div>
      </div>
    </section>

{media_section([a for a in ARTICLES if key in a["services"]], eyebrow="Media", title="関連する記事", lead="このサービスに関連するテーマを、「アキヤド」で詳しく解説しています。") if any(key in a["services"] for a in ARTICLES) else ""}

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Other Services</span>
          <h2 class="section-title">そのほかのサービス</h2>
        </div>
{related}
      </div>
    </section>"""

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]
        ],
    }
    page(f"service-{key}.html", name, d["description"], body, current=key, jsonld=[faq_ld])


# ---------------------------------------------------------------- index
def index_page():
    vsteps = "\n".join(
        f"""          <li class="vision__step reveal" data-delay="{i - 1}">
            <span class="vision__num">{i:02d}</span>
            <span class="vision__en">{e(en)}</span>
            <h3 class="vision__title">{e(t)}</h3>
            <p class="vision__text">{e(d)}</p>
          </li>"""
        for i, (t, en, d) in enumerate(VISION["steps"], 1)
    )
    vout = "".join(f'<li><span>{e(a)}</span>{e(b)}</li>' for a, b in VISION["outcomes"])
    # TOPはAboutと内容を重ねず、コンセプトと「地域の経済循環」の図だけを見せる
    arrows = "".join(
        f'<path d="M1.5 0-1.2-1.3v2.6z" transform="translate({50 + 36 * math.cos(math.radians(d)):.2f} {50 + 36 * math.sin(math.radians(d)):.2f}) rotate({d + 90})"/>'
        for d in (-45, 45, 135, 225))
    nodes = "\n".join(
        f"""            <li class="cycle__node cycle__node--{i}"><span class="cycle__en">{i:02d} {e(en)}</span><span class="cycle__t"><span>{e(a)}</span><span>{e(b)}</span></span></li>"""
        for i, (en, a, b) in enumerate(TOP_CYCLE, 1))
    vision = f"""    <section class="section vision" id="vision">
      <div class="container">
        <div class="vision__grid">
          <div class="vision__body">
            <div class="reveal">
              <span class="eyebrow">Concept</span>
              <h2 class="vision__copy">{e(TOP_CONCEPT["copy"]).replace("、", "、<br>", 1)}</h2>
            </div>
            <p class="vision__lead reveal" data-delay="1">{"<br>".join(e(l) for l in TOP_CONCEPT["lead"])}</p>
          </div>
          <div class="cycle reveal" data-delay="1" role="img" aria-label="空き家を宿に再生し、旅行者がまちを訪れ、まちで食べて買い、ファンになって再び訪れる。その収益で次の空き家を再生する、地域の経済循環">
            <svg class="cycle__ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="36"/>{arrows}</svg>
            <p class="cycle__center" aria-hidden="true"><span class="cycle__center-en">Local cycle</span><span>地域に、</span><span>人とお金がめぐる</span></p>
            <ol class="cycle__nodes" aria-hidden="true">
{nodes}
            </ol>
            <p class="cycle__loop" aria-hidden="true">次の空き家へ</p>
          </div>
          <p class="vision__more reveal" data-delay="2"><a href="about.html">ミッション・ビジョン・バリューを見る {ARROW}</a></p>
        </div>
      </div>
    </section>"""
    names = dict(SERVICES)
    num = 0
    groups_html = []
    for g in GROUPS:
        cards = []
        for i, k in enumerate(g["services"]):
            num += 1
            en, summary, ic = SERVICE_INTRO[k]
            cards.append(f"""            <a href="service-{k}.html" class="persona__card biz-card reveal" data-delay="{i % 3}">
              <span class="biz-card__num">{num:02d}</span>
              <div class="biz-card__body">
                <span class="biz-card__en">{e(en)}</span>
                <h3 class="biz-card__name">{e(names[k])}</h3>
                <p class="biz-card__text">{e(summary)}</p>
              </div>
              <span class="persona__to">詳しく見る {ARROW}</span>
            </a>""")
        groups_html.append(f"""        <div class="persona-group">
          <div class="persona-group__head reveal">
            <p class="group-label"><span>{e(g["en"])}</span>{e(g["name"])}</p>
          </div>
          <div class="persona persona--{len(g["services"])}">
{chr(10).join(cards)}
          </div>
        </div>""")
    cards = "\n".join(groups_html)
    reasons = "\n".join(
        f"""          <li class="reason reveal" data-delay="{i - 1}">
            <span class="reason__num">{i:02d}</span>
            <h3 class="reason__title">{e(t)}</h3>
            <p class="reason__text">{e(d)}</p>
          </li>"""
        for i, (t, d) in enumerate(REASONS, 1)
    )
    body = f"""    <section class="hero hero--photo">
      <img class="hero__bg" src="images/photos/autumn-garden.jpg" alt="" width="1616" height="1079" fetchpriority="high" decoding="async">
      <div class="container">
        <h1 class="hero__title reveal">地域に眠る価値を、<br>日本の活力に。</h1>
        <p class="hero__sub reveal" data-delay="2">「暮らすように旅する」滞在を軸に、<br>宿の再生から集客・採用、まちづくりまで。</p>
        <div class="hero__actions reveal" data-delay="3">
          <a href="contact.html" class="btn">無料で相談する {ARROW}</a>
          <a href="#service" class="btn btn--ghost btn--on-photo">事業紹介を見る</a>
        </div>
      </div>
      <span class="hero__scroll" aria-hidden="true">Scroll</span>
    </section>

{vision}

    <section class="section">
      <div class="container news">
        <div class="reveal">
          <span class="eyebrow">News &amp; Topics</span>
          <h2 class="section-title">お知らせ</h2>
        </div>
        <ul class="news__list reveal" data-delay="1">
          <li class="news__item">
            <time class="news__date" datetime="2026-09-01">2026.09.01</time>
            <span class="tag">News</span>
            <p class="news__title">合同会社RIVIA&amp;CO.を設立いたしました。</p>
          </li>
        </ul>
      </div>
    </section>

    <section class="section" id="service">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Service</span>
          <h2 class="section-title">事業紹介</h2>
        </div>
{cards}
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Why RIVIA</span>
          <h2 class="section-title">RIVIAが選ばれる理由</h2>
        </div>
        <ol class="reasons">
{reasons}
        </ol>
      </div>
    </section>

    <section class="section section--soft" id="project">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Project</span>
          <h2 class="section-title">運営実績</h2>
        </div>
{project_card()}
{reviews_html()}      </div>
    </section>

{media_intro()}

{flow_section()}

{cta(text=OPEN_MSG)}

    <section class="section">
      <div class="container">
        <a href="careers.html" class="careers-cta reveal">
          <div class="careers-cta__body">
            <p class="careers-cta__title">CAREERS</p>
            <div class="careers-cta__row">
              <span class="pill">年齢・経験は問いません！</span>
              <p class="careers-cta__text">一緒に働く仲間を募集しています。</p>
            </div>
          </div>
          <span class="careers-cta__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M9 5l7 7-7 7"/></svg></span>
        </a>
      </div>
    </section>"""
    org_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "合同会社RIVIA&CO.",
        "alternateName": "RIVIA&CO. LLC",
        "url": f"{SITE}/",
        "logo": f"{SITE}/images/logo/logo.png",
        "foundingDate": "2026-09-01",
        "founder": [
            {"@type": "Person", "name": "片井 進太"},
            {"@type": "Person", "name": "石原 佑真"},
        ],
        "address": {
            "@type": "PostalAddress",
            "postalCode": "121-0012",
            "addressRegion": "東京都",
            "addressLocality": "足立区",
            "streetAddress": "青井六丁目8番8号 Grand Maison青井201",
            "addressCountry": "JP",
        },
    }
    page("index.html", "", "地域に眠る価値を、日本の活力に。空き家の再生や民泊の開業・運営から、集客・採用、まちづくりまでを担う合同会社RIVIA&CO.のコーポレートサイトです。", body, jsonld=[org_ld])


# ---------------------------------------------------------------- about
# 地図の検索語（本店所在地）
from urllib.parse import quote as _quote
MAP_Q = _quote("東京都足立区青井6-8-8")


def company_profile():
    """会社概要（コーポレートの私たちについてと、アキヤドの運営会社ページで共通）"""
    return [
        ("商号", "合同会社RIVIA&amp;CO. (RIVIA&amp;CO. LLC)"),
        ("設立", "2026年9月1日"),
        ("資本金", "1,000,000円"),
        ("代表社員", "片井 進太 ／ 石原 佑真"),
        ("本店所在地", "〒121-0012<br>東京都足立区青井六丁目8番8号 Grand Maison青井201"),
        ("事業内容", "".join(
            f'<span class="profile__group">{e(g["name"])}</span>' + "<br>".join("・" + e(dict(SERVICES)[k]) for k in g["services"])
            for g in GROUPS)),
    ]


def about_page():
    founders = [
        dict(name="石原 佑真", en="Yuma Ishihara", role="代表社員 ／ 共同創業者", origin="大阪府出身", photo="founder-ishihara.jpg", photo_type="photo",
             bio="大阪府出身。新卒で株式会社リクルートに入社し、新規事業開発室にてゼロイチの事業立ち上げを経験。その後、HR Techベンチャー、サイバーセキュリティベンチャーにおいて、一貫して新規事業の創出と組織拡大を牽引。新規事業を立ち上げ、事業と組織を成長させてきた経験と、テクノロジー領域での知見を活かし、RIVIA&CO.を共同創業。",
             career=[("株式会社リクルート", "新規事業開発室にて、ゼロイチの事業立ち上げを経験"),
                     ("HR Techベンチャー", "新規事業の創出と組織拡大を牽引"),
                     ("サイバーセキュリティベンチャー", "新規事業の創出と組織拡大を牽引"),
                     ("合同会社RIVIA&CO.", "共同創業")],
             strengths=["新規事業開発", "事業グロース", "組織拡大", "テクノロジー領域の知見"]),
        dict(name="片井 進太", en="Shinta Katai", role="代表社員 ／ 共同創業者", origin="静岡県出身", photo="founder-katai.jpg", photo_type="illust",
             bio="静岡県出身。新卒で静岡県庁に入庁し、行政の視点から地域課題に向き合う。その後、大手メーカー、リクルート、HR Techベンチャーを経て、位置情報データを扱うベンチャー企業に参画。官民両方の視点と、多角的な業界知見、データ分析力を強みに持つ。現在、複数企業の経営にも携わりながらRIVIA&CO.を共同創業。",
             career=[("静岡県庁", "行政の視点から地域課題に向き合う"),
                     ("大手メーカー", ""),
                     ("株式会社リクルート", ""),
                     ("HR Techベンチャー", ""),
                     ("位置情報データベンチャー", "位置情報データを活用した事業に参画"),
                     ("合同会社RIVIA&CO.", "共同創業。現在、複数企業の経営にも携わる")],
             strengths=["官民両方の視点", "多角的な業界知見", "データ分析", "企業経営"]),
    ]
    fhtml = "\n".join(
        f"""          <article class="founder reveal" data-delay="{i}">
            <div class="founder__head">
              <figure class="founder__photo founder__photo--{f["photo_type"]}"><img src="images/{f["photo"]}" alt="{e(f["name"])}の写真" width="600" height="600" loading="lazy" decoding="async"></figure>
              <div>
                <p class="founder__role">{e(f["role"])}</p>
                <h3 class="founder__name">{e(f["name"])}</h3>
                <p class="founder__en">{e(f["en"])}<span class="founder__origin">{e(f["origin"])}</span></p>
              </div>
            </div>
            <p class="founder__bio">{e(f["bio"])}</p>
            <div class="founder__block">
              <span class="founder__label">経歴</span>
              <ol class="founder__career">
{chr(10).join(f'                <li><strong>{e(c)}</strong>{("<span>" + e(d) + "</span>") if d else ""}</li>' for c, d in f["career"])}
              </ol>
            </div>
            <div class="founder__block">
              <span class="founder__label">強み</span>
              <ul class="founder__tags">{"".join(f"<li>{e(t)}</li>" for t in f["strengths"])}</ul>
            </div>
{sns_html(f)}          </article>"""
        for i, f in enumerate(founders)
    )
    profile = company_profile()
    phtml = "\n".join(f'          <div class="profile__row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in profile)
    prose = "\n".join(
        '          <div class="about-para reveal">' + "".join(f'<p class="about-line">{e(l)}</p>' for l in para) + "</div>"
        for para in MISSION_PROSE)
    pillars = "\n".join(
        f"""          <li class="reveal" data-delay="{i - 1}"><span class="about-pillar__num">{i:02d}</span><span class="about-pillar__en">{e(en)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>"""
        for i, (t, en, d) in enumerate(VISION["steps"], 1))
    values = "\n".join(
        f"""          <li class="reveal" data-delay="{(i - 1) % 2}"><span class="about-value__num">{i:02d}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>"""
        for i, (t, d) in enumerate(VALUES, 1))
    body = f"""    <section class="page-hero page-hero--photo page-hero--about">
      <img class="page-hero__bg" src="images/photos/irori-room.jpg" alt="" width="1623" height="1079" style="object-position:50% 60%" fetchpriority="high" decoding="async">
      <div class="container">
        <p class="page-hero__en reveal">About Us</p>
        <h1 class="page-hero__ja reveal" data-delay="1">私たちについて</h1>
      </div>
    </section>

    <section class="section about-sec">
      <div class="container container--narrow">
        <p class="about-big reveal" aria-hidden="true">Mission</p>
        <h2 class="about-copy reveal">{e(MISSION["copy"]).replace("、", "、<br>", 1)}</h2>
        <div class="about-prose">
{prose}
        </div>
      </div>
    </section>

    <section class="section section--soft about-sec">
      <div class="container">
        <p class="about-big reveal" aria-hidden="true">Vision</p>
        <h2 class="about-copy reveal">{e(VISION["copy"]).replace("滞在を、", "滞在を、<br>", 1)}</h2>
        <p class="about-note reveal">{e(VISION["lead"])}</p>
        <ol class="about-pillars">
{pillars}
        </ol>
        <ul class="vision__outcomes about-outcomes reveal">{"".join(f'<li><span>{e(x)}</span>{e(y)}</li>' for x, y in VISION["outcomes"])}</ul>
      </div>
    </section>

    <section class="section about-sec">
      <div class="container">
        <p class="about-big reveal" aria-hidden="true">Values</p>
        <h2 class="about-copy reveal">私たちが大切にすること</h2>
        <ul class="about-values">
{values}
        </ul>
      </div>
    </section>

    <section class="section" id="founders">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Founders</span>
          <h2 class="section-title">創業者</h2>
        </div>
        <div class="founders">
{fhtml}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Company Profile</span>
          <h2 class="section-title">会社概要</h2>
        </div>
        <div class="company">
          <dl class="profile reveal">
{phtml}
          </dl>
          <div class="company__map reveal" data-delay="1">
            <p class="company__map-label">本店所在地</p>
            <div class="map">
              <iframe src="https://www.google.com/maps?q={MAP_Q}&amp;output=embed" title="合同会社RIVIA&amp;CO. 本店所在地の地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
            </div>
            <a href="https://www.google.com/maps/search/?api=1&amp;query={MAP_Q}" class="company__map-link" target="_blank" rel="noopener">Googleマップで開く {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

{cta()}"""
    page("about.html", "About Us", "合同会社RIVIA&CO.のミッション・ビジョン・バリュー、創業者紹介、会社概要です。", body, current="about")


# ---------------------------------------------------------------- forms
UPLOAD = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v4h16v-4"/></svg>'


def consent(id_):
    return f"""          <div class="form__consent">
            <label class="check" for="{id_}">
              <input type="checkbox" id="{id_}" name="privacy_agree" value="同意する" required>
              <span><a href="privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>に同意する <span class="req">必須</span></span>
            </label>
          </div>"""


def careers_page():
    def file_box(name, title):
        return f"""            <label class="file">
              <input type="file" name="{name}" accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png" required>
              {UPLOAD}
              <span class="file__title">{title}</span>
              <span class="file__name" data-default="クリックまたはドラッグ&amp;ドロップでファイルを選択">クリックまたはドラッグ&amp;ドロップでファイルを選択</span>
            </label>"""

    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en reveal">Careers</p>
        <h1 class="page-hero__ja reveal" data-delay="1">採用情報</h1>
        <p class="page-hero__lead reveal" data-delay="2">一緒に働く仲間を募集しています。<br>年齢・経験は問いません。お気軽にご連絡ください。</p>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <div class="section-head reveal">
          <span class="eyebrow">Entry</span>
          <h2 class="section-title">エントリーフォーム</h2>
        </div>
        <!--
          ▼ 送信先の設定（要対応）
          Formspree で採用用のフォームを作成し、「YOUR_CAREERS_FORM_ID」を発行された ID に置き換えてください。
          ※ Formspree でのファイル添付は有料プランのみ対応です。
        -->
        <form class="form reveal" action="https://formspree.io/f/YOUR_CAREERS_FORM_ID" method="POST" enctype="multipart/form-data" data-thanks="thanks.html?form=careers">
          <input type="hidden" name="_subject" value="【RIVIA&amp;CO.】採用エントリー">
          <div class="form__field">
            <label for="c-name">お名前 <span class="req">必須</span></label>
            <input type="text" id="c-name" name="name" placeholder="名字 名前" autocomplete="name" required>
          </div>
          <div class="form__field">
            <label for="c-email">Email <span class="req">必須</span></label>
            <input type="email" id="c-email" name="email" placeholder="Email@address" autocomplete="email" required>
          </div>
          <div class="form__field">
            <label for="c-detail">詳細 <span class="req">必須</span></label>
            <textarea id="c-detail" name="detail" placeholder="志望動機や希望年収、思っていることを是非教えてください。" required></textarea>
          </div>
          <fieldset class="form__field form__fieldset">
            <legend class="form__legend">添付ファイル <span class="req">必須</span></legend>
            <p class="form__notes form__notes--above">職務経歴書・履歴書を添付してください。</p>
            <div class="files">
{file_box("resume", "職務経歴書")}
{file_box("cv", "履歴書")}
            </div>
          </fieldset>
{consent("c-agree")}
          <div class="form__submit"><button type="submit" class="btn btn--lg">送信する {ARROW}</button></div>
        </form>
      </div>
    </section>"""
    page("careers.html", "Careers", "合同会社RIVIA&CO.の採用情報です。年齢・経験は問いません。一緒に働く仲間を募集しています。", body, current="careers")


def contact_page():
    short = {"operation": "アキヤド空き家再生", "management": "アキヤド開業・運営支援", "partnership": "不動産協業",
             "marketing": "WEB集客", "recruit": "WEB採用"}
    ohtml = "\n".join(
        f'                <optgroup label="{e(g["name"])}">\n'
        + "\n".join(f'                  <option value="{short[k]}" data-key="{k}">{short[k]}</option>' for k in g["services"])
        + "\n                </optgroup>"
        for g in GROUPS
    ) + '\n                <option value="サービス資料の請求" data-key="document">サービス資料の請求</option>' + '\n                <option value="その他" data-key="other">その他</option>'
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en reveal">Contact</p>
        <h1 class="page-hero__ja reveal" data-delay="1">お問い合わせ</h1>
        <p class="page-hero__lead reveal" data-delay="2">観光地でなくても、収益物件になり得ます。<br>お気軽にお問い合わせください。</p>
        <p class="page-hero__area reveal" data-delay="2"><span>対応エリア</span>全国可</p>
        <ul class="assure reveal" data-delay="3">
          <li>ご相談・お見積りは無料</li>
          <li>無理な営業は一切なし</li>
          <li>2営業日以内にご連絡</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <!--
          ▼ 送信先の設定（要対応）
          1. https://formspree.io にログインし「+ New Form」でフォームを作成
             （通知先メールアドレス: rivia.co0122@gmail.com）
          2. 下記 action の「YOUR_FORM_ID」を、発行された ID（例: abcdwxyz）に置き換える
          ※ Formspree でのファイル添付は有料プランのみ対応です。
        -->
        <form class="form reveal" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" enctype="multipart/form-data" data-thanks="thanks.html?form=contact">
          <input type="hidden" name="_subject" value="【RIVIA&amp;CO.】Webサイトからのお問い合わせ">
          <input type="hidden" name="流入元" id="from-field" value="">
          <div class="form__field">
            <label for="name">お名前 <span class="req">必須</span></label>
            <input type="text" id="name" name="name" placeholder="山田 太郎" autocomplete="name" required>
          </div>
          <div class="form__field">
            <label for="company">会社名・施設名 <span class="opt">任意</span></label>
            <input type="text" id="company" name="company" placeholder="個人の方は空欄で構いません" autocomplete="organization">
          </div>
          <div class="form__field">
            <label for="tel">電話番号 <span class="opt">任意</span></label>
            <input type="tel" id="tel" name="tel" placeholder="090-1234-5678" autocomplete="tel">
          </div>
          <div class="form__field">
            <label for="email">メールアドレス <span class="req">必須</span></label>
            <input type="email" id="email" name="email" placeholder="your@email.com" autocomplete="email" required>
          </div>
          <div class="form__field">
            <label for="category">ご相談カテゴリ <span class="opt">任意</span></label>
            <div class="select">
              <select id="category" name="category">
                <option value="" selected>選択してください</option>
{ohtml}
              </select>
            </div>
          </div>
          <div class="form__field">
            <label for="message">お問い合わせ内容 <span class="req">必須</span></label>
            <textarea id="message" name="message" placeholder="ご相談内容をご記入ください。まだ考えがまとまっていない段階でも構いません。" required></textarea>
          </div>
          <fieldset class="form__field form__fieldset">
            <legend class="form__legend">添付ファイル <span class="opt">任意</span></legend>
            <p class="form__notes form__notes--above">物件の資料・写真・図面などがあれば添付してください。PDF・画像・Word・Excelなど、合計10MBまでを目安にお送りください。</p>
            <label class="file">
              <input type="file" name="attachment" accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.jpg,.jpeg,.png,.heic" multiple>
              {UPLOAD}
              <span class="file__title">ファイルを添付する</span>
              <span class="file__name" data-default="クリックまたはドラッグ&amp;ドロップでファイルを選択（複数可）">クリックまたはドラッグ&amp;ドロップでファイルを選択（複数可）</span>
            </label>
          </fieldset>
{consent("agree")}
          <div class="form__notes">
            <p>※無理な営業や電話勧誘は一切いたしません。</p>
            <p>※ご入力いただいた情報は厳重に管理し、お問い合わせ対応以外には使用いたしません。</p>
          </div>
          <div class="form__submit"><button type="submit" class="btn btn--lg">送信する {ARROW}</button></div>
        </form>
      </div>
    </section>

{flow_section(soft=True)}"""
    page("contact.html", "Contact", "合同会社RIVIA&CO.へのお問い合わせはこちらから。ご相談は無料です。2営業日以内に担当者よりご連絡いたします。", body, current="contact")


# ---------------------------------------------------------------- privacy
PRIVACY = [
    ("個人情報の取得", "当社は、お問い合わせフォームおよび採用エントリーフォームを通じて、氏名、会社名・施設名、電話番号、メールアドレス、お問い合わせ内容、職務経歴書・履歴書その他ご本人が入力・送付された情報を、適正な手段により取得します。"),
    ("利用目的", "取得した個人情報は、次の目的の範囲内で利用します。<br>（1）お問い合わせ・ご相談への回答およびご連絡<br>（2）当社サービスのご提案、お見積り、契約の締結・履行<br>（3）採用選考および採用に関するご連絡<br>（4）上記に付随する業務"),
    ("第三者提供", "当社は、法令に基づく場合を除き、ご本人の同意を得ることなく個人情報を第三者に提供しません。"),
    ("業務の委託", "当社は、利用目的の達成に必要な範囲で、フォーム送信サービス等の外部事業者に個人情報の取扱いを委託することがあります。この場合、委託先に対して必要かつ適切な監督を行います。"),
    ("アクセス解析ツールについて", "当社ウェブサイトでは、利用状況の把握とサイト改善のため、Google LLC が提供するアクセス解析ツール「Google アナリティクス」を利用しています。Google アナリティクスは Cookie を使用して、個人を特定しない形でトラフィックデータを収集します。この機能は、ブラウザの設定で Cookie を無効にすることで拒否できます。詳しくは <a href=\"https://marketingplatform.google.com/about/analytics/terms/jp/\" target=\"_blank\" rel=\"noopener\">Google アナリティクス利用規約</a> および <a href=\"https://policies.google.com/technologies/partner-sites?hl=ja\" target=\"_blank\" rel=\"noopener\">Google のポリシーと規約</a> をご覧ください。"),
    ("安全管理措置", "当社は、個人情報の漏えい、滅失またはき損の防止その他の安全管理のために、必要かつ適切な措置を講じます。"),
    ("開示・訂正・利用停止等", "ご本人から個人情報の開示、訂正、追加、削除、利用停止等のご請求があった場合は、ご本人であることを確認のうえ、法令に従い遅滞なく対応します。"),
    ("お問い合わせ窓口", "個人情報の取扱いに関するお問い合わせは、<a href=\"contact.html\">お問い合わせフォーム</a>よりご連絡ください。<br>合同会社RIVIA&amp;CO.<br>〒121-0012 東京都足立区青井六丁目8番8号 Grand Maison青井201"),
    ("改定", "当社は、必要に応じて本ポリシーを改定することがあります。改定後の内容は、本ページに掲載した時点から効力を生じるものとします。"),
]


def privacy_page():
    items = "\n".join(
        f"""          <section class="policy__item">
            <h2>{i}. {e(t)}</h2>
            <p>{b}</p>
          </section>"""
        for i, (t, b) in enumerate(PRIVACY, 1)
    )
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en reveal">Privacy Policy</p>
        <h1 class="page-hero__ja reveal" data-delay="1">プライバシーポリシー</h1>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow">
        <!-- 本ポリシーは一般的なひな形です。公開前に内容をご確認ください。 -->
        <p class="policy__intro">合同会社RIVIA&amp;CO.（以下「当社」）は、お客様の個人情報を適切に取り扱うことが社会的責務であると考え、個人情報の保護に関する法律その他の関係法令を遵守し、以下のとおり個人情報を取り扱います。</p>
        <div class="policy">
{items}
        </div>
        <p class="policy__date">制定日：2026年9月1日</p>
      </div>
    </section>"""
    page("privacy.html", "プライバシーポリシー", "合同会社RIVIA&CO.のプライバシーポリシー（個人情報の取扱いについて）です。", body)

def thanks_page():
    """フォーム送信後の完了ページ。GA4 では generate_lead イベントを「キーイベント（コンバージョン）」に設定して計測する"""
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en reveal">Thank you</p>
        <h1 class="page-hero__ja reveal" data-delay="1">送信が完了しました</h1>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow thanks">
        <p class="thanks__lead reveal">送信いただき、ありがとうございます。<br>内容を確認のうえ、2営業日以内に担当者よりご連絡いたします。</p>
        <p class="thanks__note reveal">連絡が届かない場合は、迷惑メールフォルダもご確認ください。</p>
        <div class="thanks__actions reveal">
          <a href="index.html" class="btn">トップページへ戻る {ARROW}</a>
          <a href="media.html" class="btn btn--ghost">アキヤドを読む</a>
        </div>
      </div>
    </section>
    <script>
      // フォーム送信の完了を GA4 に記録（どのフォームからかを form_type で区別）
      if (typeof gtag === 'function') {{
        gtag('event', 'generate_lead', {{ form_type: new URLSearchParams(location.search).get('form') || 'contact' }});
      }}
    </script>"""
    page("thanks.html", "送信完了", "お問い合わせを受け付けました。", body, noindex=True)


# ---------------------------------------------------------------- spec (md)
def spec_md():
    L = []
    w = L.append

    w("# RIVIA&CO. コーポレートサイト 指示書（最新版）")
    w("")
    w("> このドキュメントは、公開用HTMLと同じデータから自動生成しています。サイトの文言・構成を変更する場合は、この指示書とHTMLの両方が一致するように更新してください。")
    w("")
    w("## 1. サイトの目的とデザイン方針")
    w("")
    w("* **目的:** 宿泊施設・空き家・地方ビジネスに課題を持つ方が、自分の悩みに合うサービスを見つけ、無料相談（お問い合わせ）に進むこと。")
    w("* **ターゲットデザイン:** 株式会社SUMUS（https://sumus-inc.co.jp/）のような、スタイリッシュで情報が整理されたモダン・ミニマルなデザイン。大きな余白、洗練されたタイポグラフィ、スクロールに応じた上品なフェードイン。")
    w("* **トーン＆マナー:** 全ページ共通で白基調（#FFFFFF）・黒文字（#111111）。罫線は1pxの極細グレー（#EEEEEE）。アクセントカラー（深緑 #1A472A）はロゴの「&」のみに限定。")
    w("* **フォント:** 見出し＝Noto Serif JP（Light）、本文＝Noto Sans JP、英字・数字＝Cormorant Garamond（Light）。")
    w("* **除外要素:** 「Seminar & Event」「マガジン」「SNSへのリンク」は置かない。")
    w("* **技術スタック:** HTML / CSS / JavaScript（外部ライブラリなし）。GitHub → Vercel で公開。")
    w("")
    w("### ファイル構成")
    w("")
    w("検索エンジンが事業ごとのページを個別に評価できるよう、ページごとにHTMLファイルを分ける。ページ本体は一番上の階層に置き、スタイル・スクリプト・画像・記事・社内資料は役割ごとのフォルダに分ける。")
    w("")
    w("```")
    w("rivia-hp/")
    w("├── pages/                   すべてのHTML（公開URLは今までどおり rivia-co.com/○○.html。vercel.json で振り分け）")
    w("│   ├── index.html           トップページ")
    w("│   ├── about.html           About Us")
    for k, n in SERVICES:
        w(("│   ├── " + f"service-{k}.html").ljust(29) + n)
    w("│   ├── careers.html         採用情報")
    w("│   ├── contact.html         お問い合わせ")
    w("│   ├── privacy.html         プライバシーポリシー")
    w("│   ├── thanks.html          送信完了ページ（検索結果には出さない設定）")
    w("│   ├── media.html           アキヤド 記事一覧")
    w("│   └── media/               記事ページ（1記事＝1ファイル）")
    for a in ARTICLES:
        w(f"│       ├── {a['slug']}.html")
    w("├── css/style.css            全ページ共通スタイル")
    w("├── js/main.js               メニュー、フェードイン、絞り込み、フォーム送信など")
    w("├── images/                  画像（ogp.jpg はSNSシェア画像 1200×630）")
    w("├── seo/                     sitemap.xml / robots.txt（公開URLはサイト直下 /sitemap.xml・/robots.txt）")
    w("├── docs/site-spec.md        この指示書（公開サーバーには置かない）")
    w("├── vercel.json              pages/・seo/ の中身を、今までどおりのURLで公開するための設定")
    w("└── .vercelignore           docs/ を Vercel の公開対象から外す設定")
    w("```")
    w("")
    w("* media/ フォルダ内の記事ページでは、ほかのページ・css・js へのリンクを ../ から始める（例: ../css/style.css）。")
    w("* ヘッダー・フッターは全ページ共通。変更する場合は全HTMLを同じ内容に揃える。")
    w("* フェードインは「画面内に入った要素・通り過ぎた要素をすべて表示」する方式。main.js が読み込めなかった場合も、2秒後に全コンテンツを表示する（表示抜けの防止）。")
    w("* 相談ボタン：ヘッダーの「無料で相談する」ボタンがPC・スマホとも常に画面上部に表示されるため、画面下の固定相談バーは設けない。サービスページでは問い合わせ種別を自動選択する。")
    w("")
    w("---")
    w("")
    w("## 2. 共通パーツ")
    w("")
    w("### Header（ヘッダー）")
    w("* 画面最上部に固定。スクロールすると下端に1pxの罫線が出る。")
    w("* **左:** ロゴ「RIVIA&CO.」（トップへのリンク）")
    w("* **中央（横並び）:** About ／ Service（事業内容） ／ Project（トップの運営実績へ） ／ Media（自社メディア） ／ Careers")
    w("* **右:** 「無料で相談する」ボタン（黒塗りの目立つボタン。お問い合わせページへ。サービスページでは問い合わせ種別を自動選択）")
    w("* **Service のドロップダウン:** PCはマウスを乗せると、スマホはタップすると、ヘッダー直下に5事業の一覧が開く。Escキーやメニュー外のクリックで閉じる。")
    w("* **事業は2つの軸で括って表示する**（ドロップダウン・フッター・トップのお悩み別導線・サービスページの関連サービス・お問い合わせのカテゴリ・会社概要のすべてで共通）。")
    names = dict(SERVICES)
    for g in GROUPS:
        w(f"    * **{g['name']}（{g['en']}）**")
        for k in g["services"]:
            w(f"        * {names[k]}")
    w("* **スマホ表示（幅900px未満）:** ヘッダーは1段で、ロゴ・「無料で相談する」ボタン・右上のメニューボタン（3本線）。メニューを開くと、Service（個人／法人・事業者のタブ付き）・About・Project・Media・Careers を全画面で表示する。")
    w("")
    w("### Footer（フッター）")
    w("* **フッター:** ロゴ、コピー「地域に眠る価値を、日本の活力に。」、「無料で相談する」ボタン、主要リンク1行、所在地・プライバシーポリシー・コピーライト")
    w("* **右:** About ／ Service（2つの軸ごとに見出しを付けて5事業） ／ Project ／ Careers ／ Contact")
    w("* **下部:** プライバシーポリシーへのリンク、「© 2026 合同会社RIVIA&CO. All Rights Reserved.」")
    w("")
    w("### スマホ用の固定相談ボタン（追加）")
    w("* スマホ表示で、少しスクロールすると画面下部に「ご相談は無料です ／ 無料で相談する」のバーを固定表示する。")
    w("* サービスページから押した場合は、お問い合わせフォームの「ご相談カテゴリ」がそのサービスで選択された状態になる。")
    w("* お問い合わせ・採用・プライバシーポリシーのページには表示しない。")
    w("")
    w("### パンくずリスト")
    w("* 画面上には表示しない（ページ名と重複し、文字が多く見えるため）。記事ページのみ構造化データ（BreadcrumbList）で検索エンジンに現在地を伝える。")
    w("")
    w("### SEO・計測（追加）")
    w("* 全ページ: 個別の title / description / canonical / OGP（og:image は ogp.jpg、1200×630）/ ファビコン（HTMLに埋め込み）。")
    w("* トップ: 会社情報の構造化データ（Organization）。サービスページ: よくある質問の構造化データ（FAQPage）。")
    w("* Googleアナリティクス4（測定ID: G-RZVE2XBPQ2）の計測タグを、全ページの `<head>` の直後に設置済み。")
    w("* フォーム（お問い合わせ・採用エントリー）は画面を移動せずに送信し、成功したら thanks.html へ移動する。thanks.html で GA4 の `generate_lead` イベント（form_type: contact / careers）を送るので、GA4 の管理画面で `generate_lead` を「キーイベント」に設定すると問い合わせ数を計測できる。")
    w("* 運営実績の下に「ゲストの声（Airbnb のレビューより）」を表示できる。build.py の `NODE_REVIEWS` に、実際のレビューを原文のまま入れたときだけ表示される（空のときは非表示）。")
    w("* **公開ドメインは https://rivia-co.com（canonical / OGP / 構造化データ / sitemap に反映済み）。**")
    w("")
    w("---")
    w("")
    w("## 3. トップページ（index.html）")
    w("")
    w("### Hero / First View")
    w("* 写真は使わない。白地に縦の極細線を3本引き、大きな明朝体のコピーのみで構成。")
    w("* **メインコピー:** 地域に眠る価値を、／日本の活力に。")
    w("* **サブコピー:** 「暮らすように旅する」滞在を軸に、／宿の再生から集客・採用、まちづくりまで。")
    w("* **ボタン（追加）:** 「無料で相談する」（お問い合わせへ）、「お悩みから探す」（下のお悩み別導線へ）")
    w("")
    w("### Mission / Vision / Values")
    w(f"* **ミッション:** {MISSION['copy']} — " + "".join(MISSION["lead"]))
    w(f"* **ビジョン:** {VISION['copy']}")
    for i, (t, en, d) in enumerate(VISION["steps"], 1):
        w(f"    {i}. **{t}（{en}）** — {d}")
    w("* **生まれる価値（3つ）:** " + " ／ ".join(f"{a}{b}" for a, b in VISION["outcomes"]))
    w("* **バリュー:** " + " ／ ".join(f"{t}：{d}" for t, d in VALUES))
    w("")
    w("### News & Topics")
    w("* 1行リスト（日付 ／ カテゴリタグ ／ タイトル）。")
    w("* 2026.09.01 [News] 合同会社RIVIA&CO.を設立いたしました。")
    w("")
    w("### 事業紹介（Service）")
    w("* 展開している事業をシンプルに紹介する。2つの軸ごとに見出しと説明文を付け、各カードはアイコン・英語名・事業名・ひとこと説明・「詳しく見る」で構成する。")
    w("* 「目的・お悩みから探す」導線は、ヘッダーの Service メニューに集約している（下記の対応表を参照）。")
    i = 0
    for g in GROUPS:
        w(f"    * **{g['name']}（{g['en']}）** — {g['lead']}")
        for k in g["services"]:
            i += 1
            w(f"        {i}. 「{PERSONAS[k]}」 → {names[k]}")
    w("")
    w("### ナビゲーション（Serviceメニュー）")
    w("* まず「個人のお客様」「法人・事業者のお客様」をタブで選び、その立場に合うサービスだけを「目的・お悩み」から探せる。表示中のサービスページの立場のタブが最初に開く。")
    w("* " + " ／ ".join(a["name"] + "：" + "、".join((f"[{l}] " if l else "") + "・".join(dict(SERVICES)[k] for k in ks) for l, ks in a["groups"]) for a in NAV_AUDIENCES))
    w("* TOPの事業紹介は、事業の軸（宿泊施設の運営・開業／WEBマーケティング支援）で分ける。")
    w("")
    w("### ロゴ")
    w("* シンボル：ブランドグリーン #1a472a の角丸スクエアに、白の細い円（地域とのつながり）＋明朝体のR＋屋根の一線（家・宿）。ファビコンと同じデザイン。ワードマーク：Cormorant Garamond の RIVIA&CO.（& のみブランドグリーン #1a472a）。文字はアウトライン化済み。")
    w("* ファイル：images/logo/（logo.svg 横組み／logo-white.svg 暗い背景用／logo-mark.svg シンボルのみ／logo-square.svg・logo.png 512px 正方形）、images/favicon.svg・favicon-48.png・apple-touch-icon.png")
    w("* 検索結果向けに、構造化データ（Organization の logo）へ logo.png を指定している。")
    w("")
    w("### プラン例（各サービスページ）")
    w("* 「しくみ図（だれが何を担うか＋お金の流れ）」と「3つのプラン例カード」で、初めての方にも分かるように見せる。数字はすべてイメージで、個別提案が前提。")
    for k in PLANS:
        w(f"    * **{dict(SERVICES)[k]}** — " + " ／ ".join(("★" if pl["rec"] else "") + pl["name"] for pl in PLANS[k]["plans"]))
    w("")
    w("### RIVIAが選ばれる理由（追加）")
    for i, (t, d) in enumerate(REASONS, 1):
        w(f"    {i}. **{t}** — {d}")
    w("")
    w("### Project（運営実績）")
    w("* お悩み別導線より下に1か所だけ配置。カード全体がリンクで、施設サイト（https://nodeshimoda.com/）を別タブで開く。ホバーで写真が少し拡大。")
    w("* **NODE Shimoda** ｜ 静岡県下田市 ｜ 一棟貸しバケーションレンタル")
    w("* 下田市旧町内の空き家を改修した滞在型アパート。RIVIAが運営・集客・DX化を担っています。")
    w("* ★ 4.88 Airbnb評価（51件）")
    w("* **NODE Shimodaは複数ある運営施設の「一例」であることを明示する。** カードに「運営施設の一例」のラベルを付ける（サービスページの実績欄も同様）。")
    w("")
    w("### ご相談の流れ（追加）")
    for i, (t, d) in enumerate(FLOW, 1):
        w(f"    {i}. **{t}** — {d}")
    w("")
    w("### 相談CTA（追加）")
    w("* 「まずは、現状をお聞かせください。」＋「ご相談はこちらから」ボタン。宿泊系サービスとTOPでは、ボタンの下に「観光地でなくても、収益物件になり得ます。／お気軽にお問い合わせください。」を2行で添える（※の注記は置かない）。")
    w("")
    w("### Careers バナー")
    w("* 「CAREERS」（大見出し）、「年齢・経験は問いません！」（ピル型タグ）、「一緒に働く仲間を募集しています。」、右に丸枠の矢印。")
    w("")
    w("---")
    w("")
    w("## 4. About Us（about.html）")
    w("* Message、Company Profile は従来の内容どおり。")
    w("* **Founders:** 各代表について、役職（代表社員 ／ 共同創業者）、氏名・ローマ字・出身、紹介文（従来の全文）に加え、「経歴」（所属の流れを縦のタイムラインで表示）と「強み」（タグ）を表示する。")
    w("    * 石原 佑真: 株式会社リクルート（新規事業開発室）→ HR Techベンチャー → サイバーセキュリティベンチャー → RIVIA&CO. 共同創業 ／ 強み: 新規事業開発・事業グロース・組織拡大・テクノロジー領域の知見")
    w("    * 代表個人のSNSリンクは現在掲載しない（会社のSNSも載せない）。")
    w("    * 片井 進太: 静岡県庁 → 大手メーカー → 株式会社リクルート → HR Techベンチャー → 位置情報データベンチャー → RIVIA&CO. 共同創業（複数企業の経営にも参画） ／ 強み: 官民両方の視点・多角的な業界知見・データ分析・企業経営")
    w("* 会社概要に「事業内容」（2つの軸ごとに5事業）を追加。ページ末尾に相談CTAを追加。")
    w("* **Googleマップ（追加）:** 会社概要の表の右側（スマホでは下）に本店所在地の地図を埋め込み、「Googleマップで開く」リンクを置く。APIキー不要の埋め込み（`https://www.google.com/maps?q=住所&output=embed`）を使用。")
    w("")
    w("---")
    w("")
    w("## 5. サービスページ（全5ページ共通構造）")
    w("")
    w("**構成:** ページ見出し → サービス概要 → こんなお悩みはありませんか？（経営課題と打ち手） → ご支援の流れ（一例） → 運営実績 → 相談CTA → よくあるご質問 → そのほかのサービス")
    w("")
    w("### 共通のデザイン指定")
    w("")
    w("1. **ページ見出し:** サービス名、トップメッセージ（明朝体・大）、「こんな方へ」（トップのお悩み文と同じ）、ボタン2つ（「無料で相談する」「お悩みと解決策を見る」）。写真は使わない。")
    w("2. **こんなお悩みはありませんか？:** 表面的な悩みではなく経営課題として整理する。**全サービス4件ずつ**。1件ごとに、左に「経営課題」（線画アイコン＋見出し）と「現場で起きていること」（お客様の声）、右に「RIVIAの打ち手」「改善する経営指標」（タグ）「この課題について相談する」リンク（ご相談カテゴリを自動選択してお問い合わせへ）を置き、矢印でつなぐ。")
    w("    * 個人のお客様も対象のサービス（アキヤド空き家再生・アキヤド開業・運営支援）は「経営課題」ではなく「お悩み」、「現場で起きていること」は「よくあるお声」、「改善する経営指標」は「変わること」と表記し、暮らしの言葉で書く。")
    w("3. **ご支援の流れ（一例）:** 「内容や期間は、お選びいただくプランや状況によって変わります。」と添えたうえで、4つのSTEPを1pxの線と丸でつないだタイムライン（PCは横、スマホは縦）。各STEPは名前・期間の目安・一行の説明だけを示す（具体的な打ち手はお悩みカード側で説明する）。")
    w("4. **運営実績（追加）:** トップと同じNODE Shimodaのカード（「運営施設の一例」と明示）。")
    w("5. **相談CTA:** 「ご相談はこちらから」ボタン（お問い合わせへ。ご相談カテゴリを自動選択）。宿泊系サービスはボタンの下に「観光地でなくても、収益物件になり得ます。お気軽にお問い合わせください。」")
    w("6. **よくあるご質問:** クリックで開閉するアコーディオン。")
    w("7. **そのほかのサービス（追加）:** 他の4サービスへのカード（お悩み文＋サービス名）。同じ軸のサービスを先に表示する。")
    w("")

    for k, n in SERVICES:
        d = SERVICE_DATA[k]
        w("---")
        w("")
        w(f"### {n}（`service-{k}.html`）")
        w("")
        w(f"* **トップメッセージ:** {''.join(d['message'])}")
        w(f"* **こんな方へ:** 「{PERSONAS[k]}」")
        w(f"* **サービス概要:** {d['overview']}")
        w("")
        w("**こんなお悩みはありませんか？（経営課題と打ち手）**")
        w("")
        w(f"* 導入文: {d['issues_lead']}")
        w("")
        for i, it in enumerate(d["issues"], 1):
            w(f"{i}. **{it['title']}**")
            w(f"    * 現場で起きていること: {it['voice']}")
            w(f"    * RIVIAの打ち手: {' '.join(it['solve'])}")
            w(f"    * 改善する経営指標: {' ／ '.join(it['kpi'])}")
        w("")
        w("**ご支援の流れ（一例）**")
        w("")
        for i, (t, term, desc, *who) in enumerate(d["steps"], 1):
            w(f"* **STEP {i}：{t}**（{term}{'・' + who[0] if who else ''}） {desc}")
        w("")
        w("**よくあるご質問**")
        w("")
        for q, a in d["faq"]:
            w(f"* **Q: {q}**")
            w(f"    A: {a}")
        w("")

    w("---")
    w("")
    w("## 5-2. アキヤド（media.html ／ media/*.html・追加）")
    w("")
    w("### 目的")
    w("* 空き家オーナー・宿の開業検討者・観光事業者が検索する悩みに答え、サービスページとお問い合わせへつなげる。")
    w("* SEO（検索エンジン）と AIO（AIによる検索回答・要約）の両方で引用されやすい構成にする。")
    w("")
    w("### メディアの構成（URLは rivia-co.com/media/ 配下。サブドメインは使わない）")
    w("* カテゴリ一覧（media/category-○○.html）：" + " ／ ".join(n for _, n in MEDIA_CATEGORIES) + "。カテゴリの説明文、関連するガイドへの導線、記事一覧（12件ずつ追加表示）。検索結果に出る独立したページにする。")
    w("* 見え方：URLは会社サイトの一部（rivia-co.com/media/）のまま、ヘッダー・フッターはメディア専用（ロゴ「アキヤド」、状況別ガイド・テーマ・検索のナビ、運営会社への小さなリンク）にして、独立したメディアとして見せる。タイトルの末尾・OGPのサイト名も「アキヤド」。")
    w("* メディアトップのFV：写真を全面に敷き、ロゴ・一言・状況別の入口（3つ）・検索窓を1画面に置いて、最初の画面から次の行動を選べるようにする（離脱を防ぐ）。")
    w("* 想定する読者（ペルソナ）：① 空き家を売りたい方 ② 空き家を活かしたい方 ③ 副業で宿をはじめたい方。記事は、この3者が悩む順番をもとに企画する。")
    w("* 記事を追加するとき：記事データに guides=[(\"sell\", 2)] のように「ガイド（sell／use／side）とStep番号」を書けば、ガイドの該当Stepに自動で並ぶ。公開日前は「公開予定」と表示される。よくある悩みの一覧（MEDIA_QUESTIONS）にも、読者の言葉の質問を1行足すと入口が増える。")
    w("* ガイド（media/guide-○○.html）：" + " ／ ".join(g["title"] for g in MEDIA_GUIDES) + "。読者の状況ごとに、悩みが生まれる順の「段階（Step）」に分けて記事を並べる。公開前の記事は「○月○日公開予定」と表示し、リンクにしない。")
    for g in MEDIA_GUIDES:
        w(f"    * {g['title']}：" + " → ".join(f"{lb}（{len(xs)}本）" for lb, _, xs in g["stages"]))
    w("* メディアトップの順：検索窓 → あなたの状況から読む（ガイド3つ）→ よくある悩みから探す（読者の言葉の質問から記事へ）→ 新着記事 → すべての記事（上にテーマのタグ5つ）。カテゴリページにも同じタグを置き、いま見ているテーマを強調して他のテーマへ移れるようにする。")
    w("* 記事ページの冒頭に「こんな方に」として、その記事を含むガイドを表示する。")
    w("* 記事ページ：パンくず（TOP ／ アキヤド ／ カテゴリ）、ガイドに含まれる記事は「この記事を含むガイド」と前後の記事、シェア（X ／ LINE ／ Facebook ／ リンクをコピー）を表示。")
    w("* 旧URL（media.html?cat=○○）はカテゴリ一覧へ移動する。")
    w("* サムネイルは記事ごとの写真（images/photos/w/ の WebP 軽量版。大きな表示では元の写真）。記事トップは原寸の写真を使い、OGP画像にも同じ写真を設定する。割り当ては build 内の ARTICLE_PHOTOS。")
    w("* 写真の配置：TOPヒーロー（素材⑧・暗めのグラデーションを重ねて白文字）、相談CTA（全ページ共通）、各サービスページTOPの背景写真、代表者の顔写真。写真は原寸のまま格納し再圧縮しない。")
    w("* トップページ（運営実績の下）と、各サービスページ（よくある質問の下）にも関連記事を3件まで表示する。")
    w("")
    w("### 記事ページの構成（SEO・AIO対策）")
    w("1. カテゴリ・タイトル（検索されるキーワードを前半に）・公開日・更新日・読了目安・執筆者")
    w("2. リード文（meta description と同じ要約）")
    w("3. **この記事のポイント**：結論を3〜5行の箇条書きで先に示す（AIの要約・引用に使われやすい）")
    w("4. 目次（ページ内リンク）")
    w("5. 本文：見出しは検索される疑問文・結論型にし、表・手順リストで整理。数値には必ず出典を明記")
    w("6. よくある質問（FAQ。構造化データ FAQPage を設定）")
    w("7. 参考資料（公的機関の資料名）と「公開日時点の情報」である旨の注記")
    w("8. 執筆者情報（E-E-A-T。監修者を立てる場合はここに追加）")
    w("9. 関連サービスへのリンクと相談ボタン、あわせて読みたい記事")
    w("* 構造化データ: Article ／ FAQPage ／ BreadcrumbList。sitemap.xml に全記事を登録。")
    w("")
    w("### 公開日の扱い（予約公開）")
    w("* 記事ごとに実際の公開日を設定し、公開日を迎えた記事だけを一覧・トップ・関連記事に表示する（main.js が日付を判定）。")
    w("* ファイルは先にまとめてアップロードしてよい。表示される公開日と、実際に読めるようになる日が一致するため、日付を偽らずに「別々の日に公開された」見せ方になる。")
    w("* 公開日より前の日付（過去の日付）を付けることはしない。公開予定を変える場合は、記事データの date / updated を変更する。")
    w("* 公開スケジュール: " + " ／ ".join(f"{a['date']} {a['title'][:18]}…" for a in sorted(ARTICLES, key=lambda x: x['date'])))
    w("")
    w("### 掲載記事")
    for a in ARTICLES:
        w("")
        w(f"#### {a['title']}（`media/{a['slug']}.html`）")
        w(f"* カテゴリ: {MEDIA_CAT_NAMES[a['category']]} ／ 公開日: {a['date']} ／ 関連サービス: " + "、".join(dict(SERVICES)[k] for k in a['services']))
        w(f"* 説明文: {a['description']}")
        w("* この記事のポイント:")
        for k in a["keypoints"]:
            w(f"    * {k}")
        w("* 見出し構成: " + " → ".join(h for _, h, _ in a["sections"]) + " → よくある質問")
        w("* 参考資料: " + " ／ ".join(a["sources"]))
    w("")
    w("> ⚠ 記事内の数値は公的機関の公表資料にもとづいて記載しているが、公開前に各資料の最新値を確認する。記事を追加するときも、数値には必ず出典を付ける。")
    w("")
    w("---")
    w("")
    w("## 6. Careers（careers.html）")
    w("* **ファーストビュー:** 写真は使わず、ほかの下層ページと同じ白基調の見出し（Careers ／ 採用情報）。")
    w("* **トップメッセージ:** 一緒に働く仲間を募集しています。／年齢・経験は問いません。お気軽にご連絡ください。")
    w("    * ⚠ サイト内に MISSION / VALUES の記載がないため、About に追加するか文言を調整する。")
    w("* **エントリーフォーム:** お名前*（名字 名前）／ Email*（Email@address）／ 詳細*（志望動機や希望年収、思っていることを是非教えてください。）／ 添付ファイル*（職務経歴書・履歴書：点線枠のファイル選択×2。選択後はファイル名を表示）／ プライバシーポリシーへの同意*（追加）／ [送信する]")
    w("* 送信先: Formspree（`YOUR_CAREERS_FORM_ID` を発行IDに置き換え。ファイル添付は有料プランのみ）")
    w("")
    w("## 7. Contact（contact.html）")
    w("* **見出し:** Contact ／ お問い合わせ")
    w("* **リード文:** まずは気軽にご相談ください。無料でご相談をお受けしています。2営業日以内に担当者よりご連絡いたします。")
    w("* **安心材料（追加）:** ご相談・お見積りは無料 ／ 無理な営業は一切なし ／ 2営業日以内にご連絡")
    w("* **フォーム:** お名前* ／ 会社名・施設名（任意。個人の不動産投資家など一般の方からの相談も想定）／ 電話番号* ／ メールアドレス* ／ ご相談カテゴリ（【宿泊施設の運営・開業】宿泊施設運営 / 運営委託 / 開業・運営コンサル 【WEBマーケティング支援】WEB集客 / WEB採用 ／ その他）／ お問い合わせ内容* ／ プライバシーポリシーへの同意*（追加）")
    w("* **マイクロコピー:** ※無理な営業や電話勧誘は一切いたしません。／※ご入力いただいた情報は厳重に管理し、お問い合わせ対応以外には使用いたしません。")
    w("* **フォーム下（追加）:** ご相談の流れ（4ステップ）")
    w("* 送信先: Formspree（`YOUR_FORM_ID` を発行IDに置き換え。通知先 rivia.co0122@gmail.com）")
    w("* 添付ファイル（任意・複数可）: 物件資料・写真・図面などを添付できる。PDF・画像・Word・Excel等、合計10MB目安。Formspree でのファイル添付は有料プランのみ対応")
    w("")
    w("## 8. プライバシーポリシー（privacy.html・追加）")
    w("* フォームで個人情報を取得するため新設。一般的なひな形のため、公開前に内容を確認する。")
    for i, (t, _) in enumerate(PRIVACY, 1):
        w(f"    {i}. {t}")
    w("")
    w("---")
    w("")
    w("## 9. 公開前チェックリスト")
    w("")
    w("- [ ] Formspree のフォームIDを設定する（お問い合わせ・採用）")
    w("- [ ] 市場データの出典を確認し、確認できない数値を差し替え・削除する")
    w("- [ ] Careers の MISSION / VALUES の扱いを決める")
    w("- [ ] プライバシーポリシーの内容を確認する")
    w("- [x] Googleアナリティクス4の計測タグを設置する（G-RZVE2XBPQ2）")
    w("- [ ] （任意）送信完了ページ（サンクスページ）を用意する")
    w("- [ ] Google Search Console に https://rivia-co.com/sitemap.xml を登録する")
    w("- [ ] メディア記事の数値（訪日客数・消費額・空き家数など）を公開前に最新の公表値と照合する")

    os.makedirs(os.path.join(OUT, "docs"), exist_ok=True)
    with open(os.path.join(OUT, "docs", "site-spec.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


# ---------------------------------------------------------------- media (articles)
# 読者が「何をしたいか」で探せるテーマ。1つの記事が複数のテーマに入る（先頭が主なテーマ）
MEDIA_CATEGORIES = [
    ("sell", "売る・手放す"),
    ("lend", "貸す・任せる"),
    ("house", "物件・改修"),
    ("start", "開業・手続き"),
    ("money", "お金・税金"),
    ("operate", "集客・運営"),
    ("trend", "観光と地域"),
]
# 以前のカテゴリのURLから、近いテーマへ転送する（vercel.json）
OLD_CATEGORY_REDIRECTS = {"akiya": "house", "market": "trend", "chiho": "trend", "kaigyo": "start", "keiei": "operate"}

ARTICLES = [
    dict(
        slug="akiya-inherited-house-to-inn",
        category="akiya",
        tone="sand",
        date="2026-09-29",
        updated="2026-09-29",
        title="実家・祖父母の家を放置するとどうなる？固定資産税を払い続ける人が「小さな宿」を選ぶ理由",
        short="放置された実家が\n「小さな宿」に変わる理由",
        description="相続した実家や祖父母の家を空き家のまま放置すると、固定資産税や管理の負担、法改正によるリスクが増えていきます。売却・解体・賃貸と比較しながら、小規模な宿として活用する人が増えている背景と、始める前に確認すべきポイントを解説します。",
        services=["operation", "management"],
        keypoints=[
            "全国の空き家は約900万戸、空き家率は13.8%と、いずれも過去最高です（総務省「令和5年住宅・土地統計調査」）。",
            "空き家を放置しても、固定資産税・修繕・管理の負担は毎年続きます。2023年の法改正で、管理が不十分な空き家は税の軽減が外れるリスクも高まりました。",
            "2024年4月から相続登記が義務化され、「とりあえず放置」はしにくくなっています。",
            "売却・解体・賃貸が難しい地方の家でも、滞在型観光の需要を取り込めば「小さな宿」として収益化できる可能性があります。",
            "始める前に「建物の状態」「立地の需要」「法令」「収支」の4点を確認することが重要です。",
        ],
        sections=[
            ("why", "なぜ今、実家の空き家が問題になっているのか", """
<p>総務省「令和5年住宅・土地統計調査」によると、2023年10月時点の全国の空き家数は<strong>約900万戸</strong>、住宅全体に占める空き家率は<strong>13.8%</strong>で、いずれも過去最高を更新しました。5年前の調査から約51万戸増えています。</p>
<p>なかでも注目すべきなのが、賃貸用・売却用・別荘などに当てはまらない<strong>「使用目的のない空き家」で、約385万戸</strong>にのぼります。その多くは、親や祖父母が住んでいた家を相続したものの、住む予定も売る予定もないまま残されている住宅だと考えられます。</p>
<div class="callout"><p class="callout__label">よくある状況</p><p>「実家は地方にあり、自分は都市部に住んでいる」「兄弟の誰も住む予定がない」「思い出があって手放す決心がつかない」。こうした理由から、判断を先送りにしたまま時間が経ってしまうケースが少なくありません。</p></div>
"""),
            ("cost", "空き家を放置すると、毎年どんな負担がかかるのか", """
<p>誰も住んでいなくても、家を所有している限り負担は続きます。主なものは次のとおりです。</p>
<table class="table">
<thead><tr><th>負担の種類</th><th>内容</th></tr></thead>
<tbody>
<tr><td>税金</td><td>固定資産税（市街化区域では都市計画税も）が毎年かかります。</td></tr>
<tr><td>維持管理</td><td>草刈り、庭木の剪定、換気・通水、郵便物の確認など。遠方に住んでいる場合は交通費と時間もかかります。</td></tr>
<tr><td>修繕</td><td>人が住まない家は傷みが早く、雨漏りや設備の故障が起きやすくなります。</td></tr>
<tr><td>保険・リスク</td><td>火災保険の維持に加え、倒壊・部材の落下・不法侵入などで近隣に迷惑をかけた場合、所有者として責任を問われる可能性があります。</td></tr>
</tbody>
</table>
<p>これらは「使っていない家」から一切の収入がないまま、毎年出ていく支出です。放置期間が長くなるほど建物の傷みが進み、活用や売却の選択肢が狭まっていく点にも注意が必要です。</p>
"""),
            ("law", "法改正で「放置」のリスクが高まっている", """
<h3>管理が不十分な空き家は、固定資産税の軽減が外れる可能性</h3>
<p>住宅が建っている土地には「住宅用地特例」があり、固定資産税の課税標準が最大で6分の1に軽減されています。2023年12月に施行された改正空家等対策特別措置法では、放置すれば危険な状態になるおそれのある空き家を<strong>「管理不全空家」</strong>として新たに位置づけました。自治体から勧告を受けると、この特例の対象から外れ、<strong>土地の固定資産税が大きく増える可能性</strong>があります。</p>
<h3>相続登記が義務になった</h3>
<p>2024年4月1日から、<strong>相続登記の申請が義務化</strong>されました。相続で不動産を取得したことを知った日から3年以内に登記する必要があり、正当な理由なく怠ると10万円以下の過料の対象になります。2024年4月より前に相続した不動産も対象で、2027年3月31日までに登記が必要です。</p>
<p>「名義は亡くなった親のまま、特に何もしていない」という状態は、今後ますます続けにくくなっていきます。</p>
"""),
            ("options", "売る・壊す・貸す・活かす：4つの選択肢を比較", """
<p>空き家になった実家の扱いには、大きく4つの選択肢があります。</p>
<table class="table">
<thead><tr><th>選択肢</th><th>メリット</th><th>注意点</th></tr></thead>
<tbody>
<tr><td>売却する</td><td>管理の負担から解放され、現金化できる</td><td>地方や築年数の古い家は買い手が見つかりにくい。売却益には税金がかかる（要件を満たせば、相続空き家の3,000万円特別控除などの特例あり）</td></tr>
<tr><td>解体する</td><td>倒壊などのリスクがなくなり、土地として売りやすくなる</td><td>解体費用がかかる。更地にすると住宅用地特例が使えず、土地の固定資産税が上がる</td></tr>
<tr><td>賃貸に出す</td><td>家賃収入が得られ、所有も続けられる</td><td>入居者を募るための改修費がかかる。地方では借り手の需要が限られる場合がある</td></tr>
<tr><td>宿として活かす</td><td>所有を続けながら収益化でき、家の雰囲気や記憶も残せる</td><td>法令の手続き・改修・運営の手間がかかる（運営は専門会社への委託で軽減できる）</td></tr>
</tbody>
</table>
<p>どれが正解かは、建物の状態・立地・ご家族の意向によって変わります。大切なのは、「何もしない」ことも一つの選択であり、そのコストが毎年かかり続けていると認識することです。</p>
"""),
            ("inn", "なぜ「小さな宿」を選ぶ人が増えているのか", """
<h3>旅のスタイルが「観光地巡り」から「滞在」へ</h3>
<p>有名な観光地を短期間で巡る旅行だけでなく、その土地に数日滞在し、地元の食や暮らしを味わう旅が広がっています。こうした旅行者にとっては、ホテルよりも<strong>一棟貸しの古民家や、生活感のある家</strong>のほうが魅力的に映ります。</p>
<h3>「古さ」や「地方の立地」が価値になる</h3>
<p>賃貸や売却では弱みになりがちな築年数の古さや、都市部から離れた立地も、宿としては「その土地らしさ」という強みに変わります。改修によって水回りや断熱を整えつつ、梁や建具など家の個性を残すことで、他にはない宿になります。</p>
<h3>所有を続けたまま、家の記憶を次につなげられる</h3>
<p>「思い出の詰まった家を壊したくない」という理由で判断を先送りしている方にとって、宿としての活用は、家を手放さずに活かす現実的な選択肢です。地域を訪れる人に使われ続けることで、家そのものが地域の拠点にもなります。</p>
<h3>運営を任せる方法もある</h3>
<p>「遠方に住んでいて自分では運営できない」という場合でも、清掃・ゲスト対応・予約管理を運営会社に委託したり、事業者に建物を貸して家賃を受け取ったりする方法があります。</p>
"""),
            ("check", "始める前に確認したい4つのポイント", """
<ol class="steps">
<li><strong>建物の状態</strong>：柱や基礎などの構造、雨漏り、耐震性を確認します。構造が健全であれば、改修で再生できるケースは少なくありません。</li>
<li><strong>立地と需要</strong>：周辺の観光資源、アクセス、競合する宿の状況から、どれくらいの宿泊需要が見込めるかを調べます。</li>
<li><strong>法令</strong>：住宅宿泊事業法（民泊新法）の届出にするか、旅館業法の許可を取るかで、営業できる日数や必要な設備が変わります。用途地域や消防設備の確認も必要です。</li>
<li><strong>収支</strong>：改修費・運営費と、想定される稼働率・宿泊単価から、何年で投資を回収できるかを試算します。</li>
</ol>
<p>法令の違いについては、<a href="media/minpaku-vs-ryokan-law.html">民泊新法と旅館業（簡易宿所）の違い・選び方</a>の記事で詳しく解説しています。</p>
"""),
            ("summary", "まとめ：「放置」を続けるコストと、活かす選択肢", """
<p>相続した実家や祖父母の家は、放置しても負担がなくなるわけではありません。税金・管理・修繕のコストは毎年かかり続け、法改正によってそのリスクは高まっています。</p>
<p>一方で、滞在型の旅を求める旅行者が増えたことで、地方の古い家が「小さな宿」として新しい価値を持つ可能性も広がっています。売却・解体・賃貸と並べて、宿としての活用も一度検討してみてはいかがでしょうか。</p>
"""),
        ],
        faq=[
            ("空き家を放置すると固定資産税は上がりますか？", "放置しただけで直ちに上がるわけではありません。ただし、管理が不十分で自治体から「特定空家」や「管理不全空家」として勧告を受けると、住宅用地特例の対象外となり、土地の固定資産税が大きく増える可能性があります。"),
            ("相続した実家の登記をまだしていません。どうなりますか？", "2024年4月1日から相続登記が義務化され、相続を知った日から3年以内の申請が必要です。それ以前に相続した不動産も対象で、2027年3月31日までに登記する必要があります。正当な理由なく怠ると10万円以下の過料の対象になります。"),
            ("古い家でも宿泊施設にできますか？", "柱や基礎などの構造が健全であれば、改修によって宿泊施設として再生できるケースは少なくありません。ただし耐震性・消防設備・用途地域など確認事項が多いため、専門家による現地調査をおすすめします。"),
            ("遠方に住んでいて、自分で運営する時間がありません。", "清掃・ゲスト対応・予約管理を運営会社に委託する方法や、事業者に建物を貸して家賃を受け取る方法（借り上げ）があります。"),
        ],
        sources=[
            "総務省「令和5年住宅・土地統計調査」",
            "国土交通省「空家等対策の推進に関する特別措置法の一部を改正する法律」",
            "法務省「相続登記の申請義務化について」",
            "国税庁「被相続人の居住用財産（空き家）を売ったときの特例」",
        ],
    ),
    dict(
        slug="japan-tourism-market-data",
        category="market",
        tone="mist",
        date="2026-09-29",
        updated="2026-09-29",
        title="データで見る日本の観光市場｜インバウンド拡大の裏で地方が抱える5つの課題",
        short="データで見る日本の観光市場と\n地方が抱える5つの課題",
        description="訪日外国人旅行者数は2024年に過去最高の約3,687万人、旅行消費額は約8.1兆円に達しました。政府は2030年に6,000万人・15兆円を目標に掲げています。一方で、都市部への集中や人手不足など、地方の観光には構造的な課題も残ります。公的データをもとに整理します。",
        services=["marketing", "recruit"],
        keypoints=[
            "2024年の訪日外国人旅行者数は約3,687万人で過去最高です（日本政府観光局）。コロナ前の2019年（約3,188万人）を上回りました。",
            "訪日外国人の旅行消費額は約8.1兆円（2024年、観光庁）で、2019年の約4.8兆円から大きく伸びています。",
            "政府は「観光立国推進基本計画」で、2030年に訪日客6,000万人・旅行消費額15兆円を目標に掲げています。",
            "一方で、大都市圏への集中、宿泊業の人手不足、地方の受け皿不足、デジタル化の遅れ、人口減少という課題が残ります。",
            "地方にとっては、空き家などの既存資源を活かした「滞在型」の受け皿づくりと、自ら集客できる仕組みが成長の鍵になります。",
        ],
        sections=[
            ("inbound", "訪日外国人旅行者数は過去最高を更新", """
<p>日本政府観光局（JNTO）の推計によると、2024年の訪日外国人旅行者数は<strong>約3,687万人</strong>となり、それまで最高だった2019年の約3,188万人を上回りました。観光庁の調査では、訪日外国人の旅行消費額も<strong>約8.1兆円</strong>と、過去最高を記録しています。</p>
<table class="table">
<thead><tr><th>年</th><th>訪日外国人旅行者数</th><th>訪日外国人旅行消費額</th></tr></thead>
<tbody>
<tr><td>2019年</td><td>約3,188万人</td><td>約4.8兆円</td></tr>
<tr><td>2024年</td><td>約3,687万人</td><td>約8.1兆円</td></tr>
<tr><td>2030年（政府目標）</td><td>6,000万人</td><td>15兆円</td></tr>
</tbody>
</table>
<p class="table-note">出典：日本政府観光局「訪日外客統計」、観光庁「訪日外国人消費動向調査」「観光立国推進基本計画」</p>
<p>旅行者数の伸び以上に消費額が伸びている点は、1人あたりの消費が増えていることを示しています。宿泊・飲食・体験への支出が、日本経済にとって大きな産業になりつつあります。</p>
"""),
            ("policy", "政府目標は2030年に6,000万人・15兆円", """
<p>政府は2023年3月に閣議決定した「観光立国推進基本計画」で、<strong>「持続可能な観光」「消費額拡大」「地方誘客促進」</strong>の3つをキーワードに掲げました。2030年に訪日外国人旅行者数6,000万人、旅行消費額15兆円という目標の達成に向けて、観光客を大都市だけでなく地方へ広げていくことが重要な方針になっています。</p>
<p>つまり国の政策としても、<strong>「地方にどれだけ旅行者を呼び込み、滞在してもらえるか」</strong>が問われているのです。</p>
"""),
            ("issues", "地方の観光が抱える5つの課題", """
<h3>1. 大都市圏・有名観光地への集中</h3>
<p>旅行者の多くは、東京・大阪・京都などの大都市圏や、一部の有名観光地に集中しています。人気の地域では混雑や住民生活への影響（いわゆるオーバーツーリズム）が問題になる一方、地方の多くは観光需要の拡大を十分に取り込めていません。</p>
<h3>2. 宿泊業の人手不足</h3>
<p>宿泊業は慢性的な人手不足に直面しています。厚生労働省「一般職業紹介状況」でも、旅館・ホテルの接客スタッフを含む「接客・給仕の職業」の有効求人倍率は、全職業の平均を上回っています（2026年7月時点）。需要があっても、人が足りずに客室を開けられない施設もあります。</p>
<h3>3. 受け皿となる宿泊施設・体験の不足</h3>
<p>地方には魅力的な自然や食、文化がありながら、旅行者が泊まれる施設や、地域ならではの体験コンテンツが不足している地域が少なくありません。泊まる場所がなければ、日帰りで通過されてしまい、地域に消費が落ちにくくなります。</p>
<h3>4. デジタル化・情報発信の遅れ</h3>
<p>旅行者は検索エンジン、地図アプリ、SNS、予約サイトなど、さまざまなWEB上の接点で旅先を探します。多言語での情報発信や、予約まで迷わず進める導線が整っていない施設は、そもそも候補に入りにくくなっています。</p>
<h3>5. 人口減少による担い手不足</h3>
<p>国立社会保障・人口問題研究所の推計（令和5年推計）では、日本の総人口は2070年に約8,700万人まで減少するとされています。地方ほど人口減少と高齢化が早く進み、観光を支える事業者や働き手の確保が難しくなっています。</p>
"""),
            ("opportunity", "地方にとってのチャンス：「滞在型観光」の広がり", """
<p>課題がある一方で、地方にとって追い風となる変化もあります。</p>
<ul>
<li><strong>リピーターの地方志向</strong>：日本を何度も訪れる旅行者ほど、大都市以外の地域や、その土地ならではの体験を求める傾向があります。</li>
<li><strong>「暮らすように旅する」ニーズ</strong>：観光名所を巡るだけでなく、地元の食や日常に触れる滞在型の旅が広がっています。</li>
<li><strong>働き方の変化</strong>：リモートワークの普及により、ワーケーションや長期滞在という新しい旅のかたちも生まれています。</li>
</ul>
<p>これらのニーズに応えられるのは、大型ホテルよりも、地域に溶け込んだ小規模な宿や体験です。</p>
"""),
            ("action", "地方の事業者・自治体は何をすべきか", """
<ol class="steps">
<li><strong>既存の資源を受け皿に変える</strong>：新しく建物を建てるのではなく、空き家や遊休不動産を宿泊施設として再生すれば、投資を抑えながら受け皿を増やせます。</li>
<li><strong>自ら集客できる仕組みをつくる</strong>：予約サイト（OTA）だけに頼らず、自社サイト・検索・地図アプリ・SNSなどを組み合わせ、直接予約を増やす仕組みを整えます。</li>
<li><strong>地域で体験をつくる</strong>：飲食店・生産者・体験事業者と連携し、泊まることで地域全体を楽しめる滞在をデザインします。</li>
<li><strong>人材の確保と定着</strong>：地方や観光業ならではの働く魅力を言語化し、共感する人材に届けます。</li>
</ol>
"""),
            ("summary", "まとめ：成長市場を地方の力に変えるために", """
<p>訪日外国人旅行者数と旅行消費額は過去最高を更新し、観光は日本の成長産業になっています。一方で、その恩恵を地方が十分に受けられているとは言えません。</p>
<p>大都市への集中、人手不足、受け皿不足といった課題を乗り越える鍵は、地域に眠る資源を活かした滞在型の受け皿づくりと、自ら集客・採用できる仕組みにあります。</p>
"""),
        ],
        faq=[
            ("2024年の訪日外国人旅行者数は何人でしたか？", "日本政府観光局（JNTO）の推計で約3,687万人となり、過去最高を記録しました。コロナ前の2019年の約3,188万人を上回っています。"),
            ("日本政府の観光に関する目標は何ですか？", "「観光立国推進基本計画」で、2030年に訪日外国人旅行者数6,000万人、訪日外国人旅行消費額15兆円を目標に掲げています。"),
            ("地方の観光の主な課題は何ですか？", "大都市圏・有名観光地への集中、宿泊業の人手不足、宿泊施設や体験コンテンツなど受け皿の不足、デジタル化・情報発信の遅れ、人口減少による担い手不足などが挙げられます。"),
            ("空き家は観光の受け皿になりますか？", "なり得ます。立地や建物の状態、法令の要件を満たせば、空き家を一棟貸しなどの宿泊施設として再生し、滞在型の旅行者を受け入れることができます。"),
        ],
        sources=[
            "日本政府観光局（JNTO）「訪日外客統計」",
            "観光庁「訪日外国人消費動向調査」",
            "観光庁「観光立国推進基本計画」（2023年3月閣議決定）",
            "厚生労働省「一般職業紹介状況」",
            "国立社会保障・人口問題研究所「日本の将来推計人口（令和5年推計）」",
        ],
    ),
    dict(
        slug="akiya-regional-revitalization",
        category="chiho",
        tone="sage",
        date="2026-09-29",
        updated="2026-09-29",
        title="空き家活用はなぜ地方創生につながるのか？宿泊施設への再生が地域にもたらす4つの循環",
        short="空き家活用が\n地方創生につながる理由",
        description="空き家を宿泊施設として再生すると、観光消費・雇用・関係人口・まちなみの継承という4つの循環が地域に生まれます。人口減少が進む地方で、空き家活用が地方創生の手段として注目される理由と、成功させるためのポイントを解説します。",
        services=["operation", "management"],
        keypoints=[
            "人口減少が進むなか、空き家は全国で約900万戸に増え、景観・防災・地域の魅力の面で負担になりつつあります。",
            "空き家を宿泊施設に再生すると、①観光消費 ②雇用 ③関係人口 ④まちなみ・文化の継承、という4つの循環が地域に生まれます。",
            "旅行者が「泊まる」ことで、飲食・体験・買い物など、地域の中での消費が広がりやすくなります。",
            "成功の鍵は、地域の日常を体験できるコンセプト、地域事業者との連携、集客と運営の仕組み化の3つです。",
        ],
        sections=[
            ("background", "人口減少と空き家の増加は、同じ問題の表と裏", """
<p>国立社会保障・人口問題研究所の推計（令和5年推計）では、日本の総人口は2070年に約8,700万人まで減少するとされています。人が減れば、住む人のいない家が増えるのは自然な流れです。</p>
<p>実際に、総務省「令和5年住宅・土地統計調査」では全国の空き家数は<strong>約900万戸</strong>、空き家率は<strong>13.8%</strong>と過去最高になりました。特に地方では、かつて町の中心だった地域でも空き家が目立つようになっています。</p>
"""),
            ("burden", "放置された空き家が地域に与える影響", """
<ul>
<li><strong>景観・まちの魅力の低下</strong>：手入れされない家が増えると、まち全体の印象が損なわれ、訪れる人や住みたい人が減ってしまいます。</li>
<li><strong>防災・防犯のリスク</strong>：老朽化した建物は、台風や地震での倒壊、部材の飛散、不法侵入や放火のリスクを高めます。</li>
<li><strong>地域経済の縮小</strong>：人が住まず、使われない建物が増えるほど、地域の中でお金が回らなくなります。</li>
</ul>
<p>一方で、空き家は見方を変えれば、<strong>すでに建っていて、地域の歴史や暮らしが刻まれた資源</strong>でもあります。この資源を「負担」から「価値」に変えることが、地方創生の一つの入り口になります。</p>
"""),
            ("cycles", "宿泊施設への再生が生む4つの循環", """
<h3>① 観光消費の循環</h3>
<p>観光庁「旅行・観光消費動向調査」でも、宿泊を伴う旅行は日帰り旅行に比べて1人あたりの消費額が大きいことが示されています。地域に泊まる場所があれば、旅行者は夕食や朝食、周辺の散策、体験、お土産など、地域の中でお金を使う時間が長くなります。宿が一軒増えることは、<strong>地域全体の消費を呼び込む入口</strong>が一つ増えることでもあります。</p>
<h3>② 雇用と仕事の循環</h3>
<p>宿の運営には、清掃、リネン、修繕、ゲスト対応などの仕事が生まれます。改修工事や備品の調達、食事の提供などを地元の事業者に依頼すれば、<strong>地域の中で仕事とお金が回る</strong>ようになります。</p>
<h3>③ 関係人口の循環</h3>
<p>総務省は、移住した「定住人口」でも、観光に来た「交流人口」でもない、地域と多様に関わる人々を<strong>「関係人口」</strong>と呼び、地域づくりの担い手として重視しています。地域に滞在し、暮らすように過ごした旅行者は、再訪したり、二拠点生活や移住を検討したりする関係人口になり得ます。</p>
<h3>④ まちなみ・文化の継承</h3>
<p>古民家や町家を壊さずに宿として使い続けることは、<strong>まちなみや建築文化を次の世代へ残す</strong>ことにつながります。修繕を通じて、地元の職人の技術が受け継がれていく効果もあります。</p>
"""),
            ("success", "空き家活用を地方創生につなげる3つのポイント", """
<ol class="steps">
<li><strong>その土地ならではのコンセプト</strong>：どこにでもあるホテルではなく、地域の食・自然・暮らしを体験できる「暮らすように旅する」宿をつくることで、わざわざ訪れる理由が生まれます。</li>
<li><strong>地域の事業者との連携</strong>：宿だけで完結させず、飲食店・生産者・体験事業者とつながることで、消費と関わりが地域全体に広がります。</li>
<li><strong>集客と運営の仕組み化</strong>：自社サイトやSNSなどで直接予約を集める仕組み、スマートチェックインや多言語対応などのデジタル化によって、少人数でも持続できる運営体制をつくります。</li>
</ol>
"""),
            ("case", "アキヤドの取り組み：NODE Shimoda（静岡県下田市）", """
<p>RIVIA&amp;CO.が運営する施設の一例である「NODE Shimoda」は、静岡県下田市の旧町内の中心部にある空き家をリノベーションした滞在型アパートです。ペリーロードなどの観光スポットへも徒歩で行ける立地を活かし、運営・集客・DX化（多言語AIチャットボットの導入）までを一貫して手がけています。</p>
<p>空き家を「暮らすように旅する」拠点へ再生し、国内外の旅行者に地域の日常を楽しんでもらうことで、地域への人の流れをつくっています。</p>
"""),
            ("summary", "まとめ：空き家は地域の未来をつくる資源になる", """
<p>空き家は、放置すれば地域の負担になりますが、活かせば観光消費・雇用・関係人口・まちなみの継承という4つの循環を生む資源になります。</p>
<p>人口減少が避けられない地方にとって、今ある資源を活かして人の流れと経済の循環をつくることは、持続可能な地域づくりの現実的な一歩です。</p>
"""),
        ],
        faq=[
            ("空き家の活用はなぜ地方創生につながるのですか？", "空き家を宿泊施設などに再生すると、旅行者の消費、運営に伴う雇用、地域と継続的に関わる関係人口、まちなみの継承といった循環が地域に生まれるためです。放置すれば負担になる建物が、人と経済の流れをつくる拠点に変わります。"),
            ("「関係人口」とは何ですか？", "総務省が提唱する考え方で、移住した「定住人口」でも観光に来た「交流人口」でもない、地域と多様に関わる人々を指します。地域づくりの新たな担い手として期待されています。"),
            ("空き家活用に使える自治体の支援制度はありますか？", "多くの自治体が、空き家バンクや改修費の補助などの制度を設けています。内容や条件は自治体ごとに異なるため、物件がある自治体の窓口やウェブサイトで確認してください。"),
        ],
        sources=[
            "国立社会保障・人口問題研究所「日本の将来推計人口（令和5年推計）」",
            "総務省「令和5年住宅・土地統計調査」",
            "総務省「関係人口ポータルサイト」",
            "観光庁「旅行・観光消費動向調査」",
        ],
    ),
    dict(
        slug="minpaku-vs-ryokan-law",
        category="kaigyo",
        tone="stone",
        date="2026-09-29",
        updated="2026-09-29",
        title="空き家で宿を始めるには？民泊新法と旅館業（簡易宿所）の違い・選び方をわかりやすく解説",
        short="民泊新法と旅館業、\nどちらで始める？",
        description="空き家を宿泊施設にするには、住宅宿泊事業法（民泊新法）の届出か、旅館業法の許可（簡易宿所など）が必要です。営業日数・手続き・設備要件の違いを比較し、目的に合った選び方と開業までの流れを解説します。",
        services=["management", "operation"],
        keypoints=[
            "宿泊料を受け取って人を泊めるには、原則として「住宅宿泊事業法の届出」か「旅館業法の許可」が必要です。",
            "民泊新法（住宅宿泊事業法）は届出制で始めやすい一方、営業日数は年間180日が上限です。自治体の条例でさらに制限される場合もあります。",
            "旅館業（簡易宿所）は許可制で要件は厳しくなりますが、営業日数の上限がなく、事業として収益を上げやすい仕組みです。",
            "どちらを選ぶ場合も、消防法・建築基準法・自治体の条例の確認が欠かせません。物件を取得する前に、行政へ事前相談するのが安全です。",
        ],
        sections=[
            ("need", "そもそも許可や届出は必要？", """
<p>宿泊料を受け取って人を宿泊させる営業は、原則として<strong>旅館業法の許可</strong>が必要です。例外として、2018年6月に施行された<strong>住宅宿泊事業法（いわゆる民泊新法）</strong>にもとづいて届出をすれば、住宅を使って一定の範囲で宿泊サービスを提供できます。</p>
<p>「空き家を少し貸すだけ」でも、宿泊料を受け取って不特定の人を泊める場合は、どちらかの手続きが必要になると考えてください。</p>
"""),
            ("compare", "民泊新法と旅館業（簡易宿所）の違い", """
<table class="table">
<thead><tr><th>項目</th><th>住宅宿泊事業法（民泊新法）</th><th>旅館業法（簡易宿所）</th></tr></thead>
<tbody>
<tr><td>手続き</td><td>都道府県等への届出</td><td>都道府県知事等（保健所）の許可</td></tr>
<tr><td>営業日数</td><td>年間180日まで（条例でさらに制限される場合あり）</td><td>上限なし</td></tr>
<tr><td>建物</td><td>台所・浴室・便所・洗面設備を備えた「住宅」</td><td>簡易宿所の構造設備基準を満たす施設</td></tr>
<tr><td>面積の目安</td><td>宿泊者1人あたり3.3㎡以上の居室</td><td>客室の延床面積33㎡以上（宿泊者10人未満の場合は1人あたり3.3㎡以上）</td></tr>
<tr><td>立地（用途地域）</td><td>住居専用地域でも可能（条例で制限される場合あり）</td><td>住居専用地域などでは原則として営業できない</td></tr>
<tr><td>管理体制</td><td>家主が不在になる場合は、住宅宿泊管理業者への委託が必要</td><td>施設ごとに管理体制を整える</td></tr>
</tbody>
</table>
<p class="table-note">※ 要件の詳細は自治体によって異なります。必ず物件所在地の自治体・保健所・消防署に確認してください。</p>
"""),
            ("choose", "目的別：どちらを選ぶべきか", """
<h3>民泊新法が向いているケース</h3>
<ul>
<li>自宅の一部や、ときどき使う家を活用したい</li>
<li>まずは小さく試してみたい</li>
<li>住居専用地域にある物件を活用したい</li>
</ul>
<h3>旅館業（簡易宿所）が向いているケース</h3>
<ul>
<li>年間を通して営業し、事業として収益を上げたい</li>
<li>投資額を回収できるだけの稼働日数を確保したい</li>
<li>一棟貸しの宿として本格的に運営したい</li>
</ul>
<p>なお、一部の地域では、国家戦略特別区域法にもとづく「特区民泊」という制度も利用できます。</p>
"""),
            ("flow", "開業までの流れ", """
<ol class="steps">
<li><strong>目的と予算を決める</strong>：副業として小さく始めるのか、事業として収益を最大化するのかで、選ぶ制度が変わります。</li>
<li><strong>物件の法令チェック</strong>：用途地域、建築基準法、消防法の観点から、宿泊施設として使えるかを確認します。</li>
<li><strong>行政への事前相談</strong>：保健所・消防署・建築の担当部署に相談し、必要な設備や手続きを確認します。</li>
<li><strong>改修・設備工事</strong>：消防設備（自動火災報知設備など）や水回り、客室を整えます。</li>
<li><strong>届出・許可申請</strong>：必要書類を揃えて届出または許可申請を行います。</li>
<li><strong>運営準備</strong>：予約サイトへの掲載、予約管理システム、清掃体制、ゲスト対応の準備をします。</li>
</ol>
"""),
            ("pitfall", "よくある失敗と注意点", """
<ul>
<li><strong>物件を買ってから許可が取れないと分かる</strong>：用途地域や建物の構造によっては、旅館業の許可が取れない場合があります。必ず取得前に確認しましょう。</li>
<li><strong>消防設備の費用を想定していない</strong>：宿泊施設には一般住宅より厳しい消防設備が求められることがあり、想定外の費用がかかるケースがあります。</li>
<li><strong>条例による営業制限を見落とす</strong>：民泊は自治体の条例で営業できる地域や期間が制限される場合があります。</li>
<li><strong>近隣への説明不足</strong>：ゲストの騒音やごみ出しでトラブルにならないよう、事前の説明とルールづくりが大切です。</li>
</ul>
"""),
            ("summary", "まとめ：制度選びは「目的」と「物件」で決まる", """
<p>空き家で宿を始めるには、民泊新法の届出か旅館業法の許可のどちらかが必要です。始めやすさを重視するなら民泊新法、年間を通した収益性を重視するなら旅館業（簡易宿所）が有力な選択肢になります。</p>
<p>いずれの場合も、物件を取得する前の法令チェックと行政への事前相談が、失敗を防ぐいちばんの近道です。</p>
"""),
        ],
        faq=[
            ("民泊と簡易宿所では、どちらが収益を上げやすいですか？", "一般に、営業日数の上限がない旅館業（簡易宿所）のほうが、年間を通して稼働できるため収益を上げやすい仕組みです。ただし許可要件や初期費用も異なるため、物件と目的に合わせて比較することが大切です。"),
            ("賃貸物件でも宿泊施設を始められますか？", "可能な場合もありますが、建物所有者の承諾が必要です。マンションの場合は、管理規約で民泊が禁止されていないかも確認してください。"),
            ("開業までにどれくらいの期間がかかりますか？", "物件の状態や改修の規模、自治体の手続きによって大きく異なり、数週間から数か月かかるのが一般的です。事前相談の段階からスケジュールを立てておくと安心です。"),
        ],
        sources=[
            "観光庁「民泊制度ポータルサイト」",
            "厚生労働省「旅館業法について」",
            "国土交通省「住宅宿泊事業法」関連資料",
        ],
    ),
]

ARTICLES += [
    dict(
        slug="airdna-revenue-simulation",
        category="keiei",
        tone="mist",
        date="2026-09-29",
        updated="2026-09-29",
        title="AirDNAで小規模宿の収益をシミュレーションする方法｜数字の見方と「再現性」を高める5つのコツ",
        short="AirDNAで読む\n小規模宿の収益と再現性",
        description="民泊・一棟貸しの市場データを提供するAirDNAを使うと、エリアの稼働率や平均客室単価から、小規模宿の売上と利回りを事前に試算できます。シミュレーションの手順と具体的な計算例、データの限界を踏まえて試算の「再現性」を高めるコツを解説します。",
        services=["management", "operation"],
        keypoints=[
            "AirDNAは、Airbnbなどに掲載された宿泊施設の公開情報をもとに、エリアごとの稼働率・平均客室単価（ADR）・季節変動などを推計するデータサービスです。",
            "年間売上は「ADR × 営業日数 × 稼働率」で試算し、そこから販売手数料・清掃費・運営費などを差し引いて、手元に残る利益と利回りを計算します。",
            "AirDNAの数値は推計値で、予約サイト以外の直接予約が含まれないなどの限界があります。「平均値」をそのまま使うと、試算が楽観的になりがちです。",
            "再現性を高めるには、条件の近い競合だけを比べる、悲観・標準・楽観の3パターンで試算する、開業直後の立ち上がり期間を見込む、といった工夫が有効です。",
        ],
        sections=[
            ("what", "AirDNAとは？小規模宿の事業計画で使われる理由", """
<p>AirDNAは、Airbnbなどの予約サイトに掲載されている民泊・バケーションレンタルの公開情報をもとに、<strong>エリアごとの稼働率、平均客室単価（ADR）、1室あたり売上、季節ごとの変動</strong>などを推計して提供しているデータサービスです。</p>
<p>小規模な宿の開業を検討するとき、「このエリアで宿をやったら、年間いくら売上が立つのか」は最も知りたい情報の一つです。ホテルのように業界統計が整っていない一棟貸しや民泊の市場では、AirDNAのような推計データが、<strong>勘に頼らず事業計画を立てるための出発点</strong>になります。</p>
<div class="callout"><p class="callout__label">主に確認できる指標</p><p>稼働率（予約が入った日の割合）、ADR（1泊あたりの平均販売単価）、RevPAR（販売可能な1日あたりの売上）、エリア内の掲載件数の推移、月ごとの需要の波など。機能名や料金プランは変更される場合があるため、利用時に公式情報をご確認ください。</p></div>
<p class="table-note">※ RIVIA&amp;CO.はAirDNA社と提携関係はありません。本記事は一般的な活用方法を解説するものです。</p>
"""),
            ("formula", "収益シミュレーションの基本式", """
<p>小規模宿の収益シミュレーションは、次の3つの式で組み立てます。</p>
<ol class="steps">
<li><strong>年間売上 ＝ ADR × 営業日数 × 稼働率</strong>：旅館業（簡易宿所）なら営業日数は最大365日、住宅宿泊事業法（民泊新法）なら年間180日が上限です。</li>
<li><strong>手元に残る利益 ＝ 年間売上 － 運営にかかる費用</strong>：販売手数料、清掃・リネン、水道光熱・通信、消耗品、運営委託費、保険・税金・修繕積立などを差し引きます。</li>
<li><strong>利回り ＝ 手元に残る利益 ÷ 投資額</strong>：投資額は、物件の取得費と改修・家具家電などの初期費用の合計です。投資額を利益で割ると、おおよその回収年数も分かります。</li>
</ol>
<p>AirDNAから得られるのは、主に1つ目の式の<strong>ADRと稼働率</strong>です。費用の側は、物件と運営体制に合わせて自分で積み上げる必要があります。</p>
"""),
            ("example", "【計算例】地方の一棟貸し（定員6名）の場合", """
<p>ここでは、次の条件で試算してみます。数値はすべて<strong>説明のための仮定</strong>で、特定のエリアの実績ではありません。</p>
<table class="table">
<thead><tr><th>項目</th><th>仮定</th></tr></thead>
<tbody>
<tr><td>施設</td><td>地方の空き家を改修した一棟貸し（定員6名）、旅館業（簡易宿所）で年間営業</td></tr>
<tr><td>投資額</td><td>1,500万円（物件取得・改修・家具家電の合計）</td></tr>
<tr><td>ADR</td><td>25,000円（競合施設のデータから設定）</td></tr>
<tr><td>販売手数料</td><td>売上の12%</td></tr>
<tr><td>運営委託費</td><td>売上の15%</td></tr>
<tr><td>清掃・リネン</td><td>1回8,000円（平均2泊で1回と仮定）</td></tr>
<tr><td>固定費</td><td>年81万円（水道光熱・通信36万円、消耗品15万円、保険・税金・修繕積立30万円）</td></tr>
</tbody>
</table>
<p>このうえで、稼働率を3パターンに分けて計算した結果が次の表です。</p>
<table class="table">
<thead><tr><th>パターン</th><th>悲観（稼働率40%）</th><th>標準（55%）</th><th>楽観（65%）</th></tr></thead>
<tbody>
<tr><td>年間売上</td><td>約365万円</td><td>約502万円</td><td>約593万円</td></tr>
<tr><td>運営費用</td><td>約238万円</td><td>約297万円</td><td>約336万円</td></tr>
<tr><td>手元に残る利益</td><td>約127万円</td><td>約205万円</td><td>約257万円</td></tr>
<tr><td>利回り</td><td>約8.5%</td><td>約13.7%</td><td>約17.1%</td></tr>
<tr><td>回収年数の目安</td><td>約11.8年</td><td>約7.3年</td><td>約5.8年</td></tr>
</tbody>
</table>
<p class="table-note">※ 所得税・住民税、借入金の返済、大規模修繕は含みません。</p>
<p>同じ物件でも、稼働率が15ポイント違うだけで、回収年数は約6年も変わります。<strong>「平均的な稼働率」を1つだけ置いて計画を立てることの危うさ</strong>が分かるはずです。</p>
<p>なお、同じ条件を民泊新法（年間180日上限）で運営する場合、仮に180日すべて埋まっても年間売上は450万円が上限です。制度の選択が収益の天井を決めることも、試算の段階で押さえておきましょう。</p>
"""),
            ("limits", "AirDNAのデータを使うときに知っておきたい限界", """
<h3>推計値であり、実績そのものではない</h3>
<p>AirDNAの数値は、予約サイト上の公開情報から推計されたものです。予約の入っていない日と、オーナーが自分で販売を止めた日（ブロック）を完全に見分けることは難しく、稼働率には誤差が含まれます。</p>
<h3>予約サイト以外の売上は含まれない</h3>
<p>自社サイトからの直接予約や、対象外の予約サイト経由の売上は反映されません。直接予約の多い人気施設ほど、実態より低く見えることがあります。</p>
<h3>掲載件数が少ないエリアほどブレが大きい</h3>
<p>地方では、比較できる施設の数自体が少なく、1〜2軒の数字に平均値が大きく引っ張られます。定員や価格帯の違う施設が混ざると、自分の物件とは前提が合わなくなります。</p>
<h3>過去のデータは未来を保証しない</h3>
<p>新しい宿の開業が相次げば、エリアの供給が増えて稼働率は下がります。規制の変更やイベントの有無によっても、需要は大きく動きます。</p>
"""),
            ("repro", "シミュレーションの「再現性」を高める5つのコツ", """
<ol class="steps">
<li><strong>条件の近い競合だけを比べる</strong>：エリア全体の平均ではなく、定員・広さ・価格帯・レビュー評価が近い施設を数軒選び、その数値を基準にします。</li>
<li><strong>悲観・標準・楽観の3パターンで試算する</strong>：上の計算例のように稼働率とADRに幅を持たせ、悲観パターンでも赤字にならないかを確認します。</li>
<li><strong>開業直後の立ち上がり期間を見込む</strong>：レビューが少ない最初の数か月は、実績のある施設と同じ稼働率にはなりません。初年度は低めに見込むのが安全です。</li>
<li><strong>季節変動を月単位で確認する</strong>：年間平均だけでなく、閑散期の月にどれだけ売上が落ちるかを見て、資金繰りを計画します。</li>
<li><strong>現地の実態で裏づけをとる</strong>：予約サイトのカレンダーや料金設定、地元の不動産会社・観光協会への聞き取りなど、複数の情報源で数字を確かめます。</li>
</ol>
<p>データはあくまで「仮説を立てる道具」です。開業後は実際の稼働率・単価を毎月記録し、試算とのズレを検証しながら価格設定や集客を改善していくことで、初めて計画の精度が上がっていきます。</p>
"""),
            ("summary", "まとめ：データを「使える数字」に変えるのは、前提の置き方", """
<p>AirDNAを使えば、小規模宿の売上や利回りを、勘ではなくデータから見積もることができます。一方で、推計データの限界を理解せずに平均値をそのまま使うと、楽観的な計画になりがちです。</p>
<p>条件の近い競合を選ぶこと、複数パターンで試算すること、開業後に検証し続けること。この3つを押さえれば、シミュレーションは投資判断の頼れる土台になります。</p>
"""),
        ],
        faq=[
            ("AirDNAの稼働率はどのくらい正確ですか？", "予約サイト上の公開情報からの推計値のため、誤差があります。とくに掲載件数の少ない地方や、直接予約の多い施設では実態とずれやすくなります。複数の情報源で裏づけをとったうえで使うのがおすすめです。"),
            ("シミュレーションで最低限入れるべき費用は何ですか？", "販売手数料、清掃・リネン費、水道光熱・通信費、消耗品費、運営を委託する場合の委託費、保険・税金・修繕積立です。借入がある場合は返済額、所得にかかる税金も別途考慮してください。"),
            ("小規模宿の利回りはどれくらいを目安にすべきですか？", "物件や運営方法によって大きく異なるため一概には言えませんが、悲観的な稼働率でも赤字にならず、想定した年数で投資を回収できるかを基準に判断することが大切です。"),
            ("開業したばかりの宿でも、競合と同じ稼働率になりますか？", "多くの場合、レビューが少ない開業直後は競合より稼働率が低くなります。初年度は低めに見込み、レビューの蓄積とともに改善していく前提で計画するのが安全です。"),
        ],
        sources=[
            "AirDNA 公式サイト（サービス・指標の説明）",
            "観光庁「民泊制度ポータルサイト」",
            "厚生労働省「旅館業法について」",
        ],
    ),
    dict(
        slug="small-inn-subsidies",
        category="kaigyo",
        tone="sand",
        date="2026-09-29",
        updated="2026-09-29",
        title="小規模宿の開業・運営で使える補助金・支援制度まとめ｜申請前に知っておきたい注意点",
        short="小規模宿で使える\n補助金・支援制度まとめ",
        description="小規模な宿の開業・運営では、販路開拓やIT導入、空き家の改修、地方での起業などを支援する補助金を活用できる場合があります。代表的な制度の種類と対象になりやすい経費、申請前に知っておきたい注意点を解説します。",
        services=["management", "marketing"],
        keypoints=[
            "小規模宿で活用を検討しやすいのは、①販路開拓（小規模事業者持続化補助金など）、②IT・DX導入、③空き家・古民家の改修（自治体の補助）、④地方での起業・移住の支援、⑤観光庁などの宿泊業向け事業、の5種類です。",
            "補助金の多くは「後払い（精算払い）」で、交付決定の前に発注・契約した経費は対象外になるのが原則です。",
            "制度の名称・上限額・補助率・対象経費は年度や公募回ごとに変わります。必ず最新の公募要領を確認してください。",
            "補助金ありきで計画を立てず、「採択されなくても成り立つ事業計画」に上乗せする考え方が安全です。",
        ],
        sections=[
            ("types", "小規模宿で活用を検討しやすい補助金・支援制度の種類", """
<p>宿泊施設の開業・運営に使える制度は、国・都道府県・市区町村がそれぞれ用意しており、目的によって大きく5つに分けられます。</p>
<table class="table">
<thead><tr><th>目的</th><th>代表的な制度の例</th><th>対象になりやすい経費</th></tr></thead>
<tbody>
<tr><td>販路開拓</td><td>小規模事業者持続化補助金</td><td>自社ホームページ、チラシ、広告、販路開拓に伴う店舗改装など</td></tr>
<tr><td>IT・DX導入</td><td>IT導入補助金（年度により名称・枠組みが変わる場合あり）</td><td>予約管理システム（PMS）、会計ソフト、セルフチェックインなど</td></tr>
<tr><td>空き家・古民家の改修</td><td>市区町村の空き家改修補助、古民家活用の補助</td><td>改修工事費、家財の処分費など</td></tr>
<tr><td>地方での起業・移住</td><td>地方創生の起業支援金・移住支援金（実施自治体のみ）</td><td>起業に必要な経費、移住に伴う支援</td></tr>
<tr><td>宿泊業の高付加価値化・省力化</td><td>観光庁などが年度ごとに公募する宿泊事業者向けの事業</td><td>施設改修、省力化設備の導入など</td></tr>
</tbody>
</table>
<p class="table-note">※ 2026年10月時点の一般的な整理です。制度の有無・名称・内容は年度や地域によって異なります。</p>
"""),
            ("jizokuka", "小規模事業者持続化補助金：集客の仕組みづくりに", """
<p>小規模事業者が販路開拓や業務効率化に取り組む費用の一部を補助する制度で、全国の商工会議所・商工会が窓口になっています。宿泊業の場合、<strong>常時使用する従業員が20人以下</strong>であれば小規模事業者に該当します。</p>
<p>通常枠の補助上限は50万円、補助率は3分の2が基本で、賃上げなどの要件を満たすと上限が引き上げられる特例があります（公募回によって異なります）。自社予約サイトの制作や広告など、<strong>OTAに頼らない集客の仕組みづくり</strong>と相性の良い制度です。</p>
<p>申請には、商工会議所・商工会の確認を受けた事業計画書が必要です。締切直前は窓口が混み合うため、早めの相談をおすすめします。</p>
"""),
            ("it", "IT導入補助金：少人数運営を支えるシステムに", """
<p>中小企業・小規模事業者が、あらかじめ登録されたITツールを導入する費用の一部を補助する制度です。宿泊施設では、予約管理システム（PMS）や会計ソフト、セルフチェックインなどが対象になり得ます。</p>
<p>補助を受けるには、<strong>登録されたIT導入支援事業者を通じて、登録されたツールを導入する</strong>必要があります。自分で選んだツールを自由に買えばよいわけではない点に注意しましょう。年度によって名称や枠組みが見直されることがあるため、最新の情報を確認してください。</p>
"""),
            ("local", "自治体の空き家改修補助・起業支援", """
<h3>空き家・古民家の改修補助</h3>
<p>多くの市区町村が、空き家の活用を促すために改修費の一部を補助しています。<strong>空き家バンクに登録された物件であること</strong>や、<strong>一定期間その用途で使い続けること</strong>などが条件になっている場合が多く、内容は自治体ごとに大きく異なります。</p>
<h3>地方での起業・移住の支援</h3>
<p>国の地方創生の枠組みを活用し、東京圏から地方へ移住して起業する人などを対象に、起業支援金や移住支援金を用意している自治体があります。対象地域・要件・金額は自治体ごとに定められているため、事業を行う地域の都道府県・市区町村の窓口で確認しましょう。</p>
"""),
            ("kanko", "観光庁などの宿泊業向け事業", """
<p>観光庁は、宿泊施設の改修による高付加価値化や、人手不足に対応するための省力化投資などを支援する事業を、年度ごとに公募してきました。地域単位での計画づくりが前提になっているものや、公募期間が短いものもあります。</p>
<p>こうした事業は予算年度ごとに内容が変わるため、観光庁のウェブサイトや、地域の観光協会・DMOの情報を定期的に確認しておくと、チャンスを逃しにくくなります。</p>
"""),
            ("caution", "申請前に知っておきたい5つの注意点", """
<ol class="steps">
<li><strong>原則として後払い</strong>：補助金は、事業を実施して経費を支払ったあとに、報告を経て受け取るのが一般的です。いったんは自己資金や融資で立て替える必要があります。</li>
<li><strong>交付決定前の発注は対象外</strong>：採択・交付決定の前に契約・発注した経費は、原則として補助の対象になりません。工事や購入のスケジュールに注意しましょう。</li>
<li><strong>公募期間と採択の不確実性</strong>：募集は期間限定で、申請しても必ず採択されるわけではありません。</li>
<li><strong>対象者の要件</strong>：開業届を出していない個人や、業種・規模の要件を満たさない場合は対象外になることがあります。</li>
<li><strong>事業後の報告義務</strong>：補助を受けた後も、一定期間の報告や、取得した設備を処分しないことなどが求められる場合があります。</li>
</ol>
<p>資金計画では、補助金とあわせて日本政策金融公庫の創業向け融資などの選択肢も比較しておくと、計画に余裕が生まれます。</p>
"""),
            ("summary", "まとめ：補助金は「成り立つ計画」に上乗せするもの", """
<p>小規模宿の開業・運営では、販路開拓、IT導入、空き家の改修、地方での起業など、目的に応じてさまざまな支援制度を活用できる可能性があります。</p>
<p>一方で、補助金は後払いで採択も約束されていません。<strong>補助金がなくても成り立つ事業計画をつくり、使える制度があれば上乗せする</strong>という順番で考えることが、失敗しない活用のコツです。</p>
"""),
        ],
        faq=[
            ("民泊や一棟貸しの開業費用に使える補助金はありますか？", "制度や地域によっては対象になる場合があります。販路開拓の費用であれば小規模事業者持続化補助金、改修費であれば市区町村の空き家改修補助などが候補になります。対象経費や要件は制度ごとに異なるため、最新の公募要領を確認してください。"),
            ("補助金はいつもらえますか？", "多くの補助金は、事業を実施して経費を支払い、実績報告の審査を経たあとに支払われる後払い（精算払い）です。そのため、いったんは自己資金や融資で立て替える必要があります。"),
            ("副業で宿を始める個人でも補助金を申請できますか？", "開業届を提出して事業として営んでいることなどが求められる制度が多く、副業の個人では対象外になる場合もあります。制度ごとの対象者の要件を確認してください。"),
            ("すでに工事を始めてしまった経費も対象になりますか？", "原則として、交付決定の前に契約・発注した経費は対象外です。補助金の活用を考えている場合は、発注の前に申請スケジュールを確認しましょう。"),
        ],
        sources=[
            "中小企業庁「小規模事業者持続化補助金」",
            "IT導入補助金 事務局サイト",
            "内閣官房・内閣府「地方創生（移住支援金・起業支援金）」",
            "観光庁「宿泊施設・観光産業に関する支援事業」",
            "日本政策金融公庫「創業融資のご案内」",
        ],
    ),
    dict(
        slug="new-build-vs-used-house-inn",
        category="kaigyo",
        tone="sage",
        date="2026-09-29",
        updated="2026-09-29",
        title="小規模宿は新築と中古どっちがおすすめ？費用・工期・法令・税金の違いから選び方を解説",
        short="小規模宿は\n新築と中古、どっちがいい？",
        description="小規模な宿を始めるとき、新築で建てるか、中古の住宅や空き家を改修するかは大きな分かれ道です。初期費用・工期・法令への対応・減価償却・融資・集客上の魅力の違いを比較し、どんな人にどちらが向いているかを解説します。",
        services=["management", "operation"],
        keypoints=[
            "初期費用と工期を抑えやすく、地域らしさを活かしやすいのは「中古（空き家の改修）」。設計の自由度と長期の安心感を重視するなら「新築」が向いています。",
            "中古は、1981年5月以前の旧耐震基準の建物、雨漏り・シロアリ、再建築不可の土地など、購入前に確認すべきリスクがあります。",
            "宿泊施設への用途変更は、床面積が200㎡以下であれば建築確認の手続きが不要になりました（2019年の建築基準法改正）。小規模宿には追い風です。",
            "築年数が法定耐用年数を超えた中古の木造住宅は、減価償却の期間が短くなる一方、融資期間も短くなりやすい点に注意が必要です。",
        ],
        sections=[
            ("compare", "新築と中古の違いを一覧で比較", """
<table class="table">
<thead><tr><th>比較項目</th><th>新築</th><th>中古（空き家の改修）</th></tr></thead>
<tbody>
<tr><td>初期費用</td><td>土地がない場合は土地代＋建築費で高額になりやすい</td><td>物件価格＋改修費。地方の空き家は取得費を抑えやすい</td></tr>
<tr><td>開業までの期間</td><td>設計から完成まで長くなりやすい</td><td>改修の規模次第で比較的短期間での開業も可能</td></tr>
<tr><td>設計の自由度</td><td>間取り・動線・設備を宿泊用に最適化できる</td><td>既存の構造に制約される</td></tr>
<tr><td>法令への対応</td><td>最初から宿泊施設の基準で設計できる</td><td>用途地域・消防設備・耐震性などの確認と改修が必要</td></tr>
<tr><td>集客上の魅力</td><td>新しさ・快適性が強み</td><td>古民家などは「その土地らしさ」が強い差別化要素になる</td></tr>
<tr><td>修繕リスク</td><td>当面は小さい</td><td>見えない劣化（雨漏り・シロアリ・配管）が見つかることがある</td></tr>
<tr><td>減価償却</td><td>法定耐用年数にもとづき長期で償却</td><td>築年数によっては短期間で償却できる</td></tr>
<tr><td>融資</td><td>比較的長い期間で組みやすい</td><td>建物の残存耐用年数を理由に期間が短くなりやすい</td></tr>
</tbody>
</table>
"""),
            ("used", "中古（空き家の改修）が向いているケース", """
<ul>
<li><strong>初期投資を抑えて始めたい</strong>：地方の空き家は取得費が比較的安く、改修費と合わせても新築より投資額を抑えやすい傾向があります。</li>
<li><strong>地域らしさを宿の魅力にしたい</strong>：梁や建具、土間などを活かした古民家は、新築では出せない雰囲気があり、滞在型の旅行者に選ばれる理由になります。</li>
<li><strong>早く開業して検証したい</strong>：大規模な建て替えをしなければ、比較的短い期間で開業し、実際の需要を確かめられます。</li>
<li><strong>相続した実家や空き家がある</strong>：すでに所有している建物を活かせば、取得費がかからず、放置による負担の解消にもつながります。</li>
</ul>
"""),
            ("new", "新築が向いているケース", """
<ul>
<li><strong>宿泊に最適化した設計にしたい</strong>：客室の数や広さ、水回りの数、清掃の動線まで、運営しやすい建物をゼロから設計できます。</li>
<li><strong>長期で安定して運営したい</strong>：当面の大規模修繕リスクが小さく、長期の事業計画を立てやすくなります。</li>
<li><strong>土地をすでに持っている、または理想の立地が更地</strong>：条件に合う中古物件が見つからない場合は、新築が現実的な選択肢になります。</li>
</ul>
"""),
            ("check", "中古物件を選ぶときのチェックポイント", """
<h3>耐震性（1981年6月の基準改正）</h3>
<p>建築基準法の耐震基準は1981年6月に大きく改正されました。<strong>それ以前に建築確認を受けた「旧耐震基準」の建物</strong>は、耐震診断や補強が必要になる場合があり、費用と工期に影響します。</p>
<h3>雨漏り・シロアリ・配管の劣化</h3>
<p>長く空き家だった建物は、見えない部分の劣化が進んでいることがあります。購入前に専門家による建物調査（インスペクション）を行うと安心です。</p>
<h3>用途変更の手続き</h3>
<p>住宅を宿泊施設（旅館業）として使う場合は「用途変更」にあたります。2019年の建築基準法改正で、<strong>床面積200㎡以下であれば用途変更の建築確認申請が不要</strong>になりました。ただし、手続きが不要でも、建物を宿泊施設の基準に適合させる必要がある点は変わりません。</p>
<h3>土地の条件（接道・再建築不可・用途地域）</h3>
<p>建築基準法上の道路に接していない土地は、建て替えができない「再建築不可」の場合があります。また、用途地域によっては旅館業の営業ができないこともあるため、<strong>購入前に行政へ確認</strong>しましょう。</p>
"""),
            ("tax", "減価償却と融資：お金の面での違い", """
<p>建物は、法定耐用年数に応じて毎年少しずつ経費（減価償却費）として計上します。木造住宅の法定耐用年数は22年です。</p>
<p>法定耐用年数を過ぎた中古の木造住宅を取得した場合、簡便法では<strong>耐用年数が4年</strong>（22年×20%）となり、建物の取得価額を短期間で経費にできます。一方で、金融機関は建物の残存耐用年数をもとに融資期間を判断することが多く、<strong>中古は融資期間が短くなり、毎月の返済額が大きくなりやすい</strong>点に注意が必要です。</p>
<p class="table-note">※ 税務上の取り扱いは個別の状況によって異なります。具体的な判断は税理士にご相談ください。</p>
"""),
            ("summary", "まとめ：地方の小規模宿なら、まず「中古の活用」から検討を", """
<p>新築と中古のどちらが正解かは、予算・立地・目指す宿のコンセプトによって変わります。ただ、地方で小規模な宿を始める場合、<strong>初期費用を抑えやすく、地域らしさを魅力にできる中古（空き家の改修）</strong>は、有力な選択肢です。</p>
<p>そのうえで、耐震性や劣化、法令・土地の条件といったリスクを購入前に確認することが欠かせません。物件選びの段階から、宿の運営を知る専門家に相談することで、見落としを防げます。</p>
"""),
        ],
        faq=[
            ("古民家を宿にするとき、費用はどれくらいかかりますか？", "建物の状態、改修の範囲、必要な消防設備などによって大きく異なります。構造がしっかりしていれば費用を抑えられる一方、耐震補強や水回りの全面改修が必要になると高額になります。購入前に建物調査と概算見積もりを取ることをおすすめします。"),
            ("旧耐震基準の建物でも宿泊施設にできますか？", "直ちに不可能というわけではありませんが、安全性の確保のために耐震診断や補強工事が必要になる場合があります。費用と工期が増えるため、物件選びの段階で確認しておきましょう。"),
            ("中古住宅を宿にするのに、建築確認の手続きは必要ですか？", "宿泊施設（旅館業）への用途変更で、床面積が200㎡を超える場合は建築確認申請が必要です。200㎡以下であれば申請は不要ですが、建物を基準に適合させる必要はあります。"),
            ("新築と中古、融資を受けやすいのはどちらですか？", "一般に、新築のほうが長い融資期間を組みやすい傾向があります。中古は建物の残存耐用年数を理由に期間が短くなりやすいため、返済計画をあらかじめ確認しておくことが大切です。"),
        ],
        sources=[
            "国土交通省「建築基準法の一部を改正する法律（平成30年法律第67号）について」",
            "国土交通省「住宅・建築物の耐震化について」",
            "国税庁「中古資産の耐用年数」",
            "厚生労働省「旅館業法について」",
        ],
    ),
]

MEDIA_CAT_NAMES = dict(MEDIA_CATEGORIES)
ARTICLE_BY_SLUG = {a["slug"]: a for a in ARTICLES}


def fmt_date(d):
    return d.replace("-", ".")


def read_minutes(a):
    import re as _re
    text = _re.sub(r"<[^>]+>", "", "".join(h for _, _, h in a["sections"]))
    return max(3, round(len(text) / 500))


SERVICE_PHOTOS = {
    # サービスページTOPの背景（全面に敷くため、横長で解像度の高い写真を使う）
    "operation": ("irori-room", 1623, 1079, "50% 55%"),
    "management": ("thatched-house", 1920, 1080, "50% 50%"),
    "marketing": ("laptop-dashboard", 1516, 1080, "50% 50%", True),
    "recruit": ("rural-station", 1918, 1080, "50% 50%"),
    "partnership": ("analytics-paper", 1619, 1080, "50% 50%", True),
}
ARTICLES += [
    dict(
        slug="shizuoka-yaizu-akiya-inn",
        category="akiya",
        tone="sand",
        date="2026-10-01",
        updated="2026-10-01",
        title="静岡市・焼津の空き家は宿になる？｜有名観光地でなくても収益物件になり得る理由と見極め方",
        short="静岡市・焼津の空き家は\n宿になる？",
        description="有名な観光地でなくても、空き家が宿として収益を生むケースは少なくありません。静岡市・焼津を例に、観光以外の宿泊需要の見つけ方、物件の見極め方、始める前に確認したい制度と費用を解説します。",
        services=["operation", "management"],
        keypoints=[
            "宿の需要は観光だけではありません。出張・工事・帰省・家族の集まり・合宿・長期滞在など、「暮らしの用事」による宿泊は観光地以外にもあります。",
            "静岡市は新幹線の停車駅を持ち、ビジネスや帰省、イベントでの来訪が見込めます。焼津は漁港と温泉の町で、食を目的にした来訪や、工事・業務での滞在もあります。",
            "観光地に比べて物件の取得費や家賃を抑えやすい一方、ビジネスホテルとの比較は避けられません。一棟貸しならではの広さ・キッチン・駐車場が差別化のポイントです。",
            "始める前に、旅館業法と住宅宿泊事業法（民泊新法）のどちらで運営するか、自治体の条例による制限、消防設備などを確認する必要があります。",
        ],
        sections=[
            ("demand", "観光地でなくても、宿の需要はある", """
<p>「うちの実家は観光地ではないから、宿にはならない」。空き家のご相談で、よく伺う言葉です。たしかに、有名な観光地ほど宿泊需要がわかりやすいのは事実です。</p>
<p>一方で、人が泊まる理由は観光だけではありません。<strong>出張や工事での滞在、帰省、法事や結婚式などの家族の集まり、部活動やサークルの合宿、移住前のお試し滞在</strong>。こうした「暮らしの用事」による宿泊は、観光地でなくても一定の需要があります。</p>
<div class="callout"><p class="callout__label">一棟貸しが選ばれやすい場面</p><p>大人数でまとまって泊まりたい、キッチンで自炊したい、車で来て駐車場が必要、数日〜数週間の滞在になる。ホテルの客室では満たしにくいこうした条件では、一棟貸しの宿が選ばれやすくなります。</p></div>
"""),
            ("area", "静岡市・焼津の場合：どんな人が泊まりに来るのか", """
<h3>静岡市：新幹線の停車駅と、出張・帰省・イベントの需要</h3>
<p>静岡市は東海道新幹線の停車駅を持ち、東京・名古屋方面との行き来がしやすい街です。県庁所在地として出張での来訪があるほか、帰省や家族の集まり、スポーツやコンサートなどのイベントでの宿泊も見込めます。</p>
<p>観光面でも、富士山の世界文化遺産の構成資産である三保松原や、富士山と駿河湾を望む日本平など、日帰りで回られがちな見どころがあります。「泊まる理由」をつくれれば、滞在型の観光につなげられる余地があります。</p>
<h3>焼津：漁港と温泉、食を目的にした来訪</h3>
<p>焼津は、かつおやまぐろの水揚げで知られる漁港の町です。海の幸を目的にした来訪や、温泉、港周辺の散策に加え、工事や業務で一定期間滞在する人の宿泊需要もあります。東名高速道路のインターチェンジがあり、車での来訪がしやすいのも特徴です。</p>
<p class="table-note">※ 需要の大きさは、エリアや時期によって大きく異なります。実際の判断には、物件ごとの調査が必要です。</p>
"""),
            ("merit", "観光地以外で宿を始めるメリットと注意点", """
<h3>メリット：取得費・家賃を抑えやすく、利回りの余地がある</h3>
<p>有名な観光地では、物件の価格や家賃が上がりやすく、宿の数も多いため競争が激しくなりがちです。観光地以外では、<strong>初期費用を抑えたうえで、競合の少ない立地で運営できる</strong>可能性があります。</p>
<h3>注意点：ビジネスホテルや他の宿との比較は避けられない</h3>
<p>出張や帰省の需要では、駅前のビジネスホテルが比較の対象になります。一人で1泊するだけなら、ホテルの方が選ばれやすいでしょう。<strong>家族やグループ、長期滞在、車での来訪</strong>など、一棟貸しの強みが活きる人に向けて、広さ・設備・価格を設計することが大切です。</p>
<h3>注意点：平日と週末で需要の中身が変わる</h3>
<p>平日は出張・工事、週末は家族や観光、と曜日によって泊まる人が変わることがあります。曜日ごとに料金や最低宿泊日数を調整すると、稼働を平準化しやすくなります。</p>
"""),
            ("check", "宿にできるかを見極める5つのチェックポイント", """
<ol class="steps">
<li><strong>誰が泊まりに来るか</strong>：周辺の企業・工場・学校・病院・イベント会場・観光地など、泊まる理由になる場所を書き出します。</li>
<li><strong>アクセス</strong>：最寄り駅や高速道路のインターチェンジからの距離、駐車場を確保できるかを確認します。</li>
<li><strong>建物の状態</strong>：雨漏り・シロアリ・水回りの傷みなど、改修費が大きくなる要因がないかを確認します。</li>
<li><strong>制度と条例</strong>：旅館業法（簡易宿所）か住宅宿泊事業法（民泊新法）か。用途地域や、自治体の条例による営業日・区域の制限も確認します。</li>
<li><strong>収支の見通し</strong>：周辺の宿の料金と稼働を調べ、悲観的な想定でも赤字にならないかを試算します。</li>
</ol>
"""),
            ("summary", "まとめ：「観光地ではない」は、あきらめる理由にならない", """
<p>宿の需要は、観光地だけにあるわけではありません。静岡市や焼津のように、出張・帰省・食・イベントといった「泊まる理由」がある地域では、空き家が収益物件になり得ます。</p>
<p>大切なのは、誰が泊まりに来るかを具体的に描き、その人に合った宿をつくることです。RIVIA&amp;CO.は全国のご相談に対応していますので、「うちの空き家でもできるのか」という段階から、お気軽にご相談ください。</p>
"""),
        ],
        faq=[
            ("観光地ではない場所の空き家でも、宿にできますか？", "可能性はあります。出張・工事・帰省・家族の集まり・長期滞在など、観光以外の宿泊需要があれば、宿として収益が見込めることがあります。物件ごとに需要と収支を調べたうえで判断します。"),
            ("静岡市や焼津以外の地域でも相談できますか？", "はい。RIVIA&CO.は全国のご相談に対応しています。まずは物件の所在地と状態をお知らせください。"),
            ("宿にするには、どのくらいの費用がかかりますか？", "建物の状態や改修の範囲によって大きく異なります。現地を確認したうえで、改修費と見込める収入を試算してご提示します。"),
        ],
        sources=[
            "観光庁「民泊制度ポータルサイト」",
            "厚生労働省「旅館業法について」",
            "静岡市・焼津市 公式ウェブサイト",
        ],
    ),
]

# 予約公開の記事（2026-11-01 から1日おきに公開。公開日前は一覧に出さず、記事ページは一覧へ戻す）
from articles_sched1 import ARTICLES_SCHED1
from articles_sched2 import ARTICLES_SCHED2
from articles_case import ARTICLES_CASE
for _a in ARTICLES_SCHED1 + ARTICLES_SCHED2 + ARTICLES_CASE:
    _a.setdefault("tone", "sand")
    _a.setdefault("updated", _a["date"])
    ARTICLES.append(_a)
ARTICLE_TOPICS = {
    "akiya-inherited-house-to-inn": ["sell", "lend", "money"],
    "akiya-3000man-deduction": ["sell", "money"],
    "akiya-bank-guide": ["house", "sell"],
    "akiya-lease-types": ["lend"],
    "minpaku-management-company": ["lend", "start"],
    "kominka-renovation-points": ["house"],
    "shizuoka-yaizu-akiya-inn": ["house", "trend"],
    "new-build-vs-used-house-inn": ["start", "house", "money"],
    "minpaku-vs-ryokan-law": ["start"],
    "minpaku-start-steps": ["start"],
    "minpaku-fire-safety": ["start"],
    "small-inn-subsidies": ["money", "start"],
    "inn-startup-funding": ["money", "start"],
    "minpaku-investment-yield": ["money"],
    "accommodation-tax": ["money", "trend"],
    "case-rental-house-inn-first-year": ["operate", "money"],
    "airdna-revenue-simulation": ["operate", "money"],
    "inn-kpi-basics": ["operate"],
    "ota-vs-direct-booking": ["operate"],
    "listing-photo-tips": ["operate"],
    "cleaning-linen-operations": ["operate"],
    "guest-review-tips": ["operate"],
    "japan-tourism-market-data": ["trend"],
    "long-stay-travel-demand": ["trend"],
    "inbound-regional-dispersion": ["trend"],
    "inn-local-economy": ["trend"],
    "akiya-regional-revitalization": ["trend"],
    "tourism-labor-shortage": ["trend"],
    "kankei-jinko-and-inns": ["trend"],
}
for _a in ARTICLES:
    _a["topics"] = ARTICLE_TOPICS[_a["slug"]]
    _a["category"] = _a["topics"][0]
ARTICLE_BY_SLUG = {a["slug"]: a for a in ARTICLES}


ARTICLE_PHOTOS = {
    # 記事ごとに別の写真を使う（同じ写真を2つの記事に使わない）
    "akiya-inherited-house-to-inn": ("old-town-street", "古い町家が並ぶ路地"),
    "japan-tourism-market-data": ("fuji-lake", "湖と富士山の風景"),
    "akiya-regional-revitalization": ("rural-station", "田園と山に囲まれた地方の駅と町並み"),
    "minpaku-vs-ryokan-law": ("temple-bridge", "緑に囲まれた寺院と朱色の橋"),
    "airdna-revenue-simulation": ("koi-pond", "鯉の泳ぐ池"),
    "small-inn-subsidies": ("dark-room", "障子越しに光の入る和室"),
    "new-build-vs-used-house-inn": ("thatched-house", "田園に佇む茅葺きの古民家"),
    "shizuoka-yaizu-akiya-inn": ("town-railway", "住宅街を抜ける線路と町並み"),
    "minpaku-start-steps": ("white-bedroom", "白を基調とした明るい寝室"),
    "akiya-bank-guide": ("green-hills", "緑の丘が連なる山あいの風景"),
    "inn-kpi-basics": ("pillow", "整えられた寝具と枕"),
    "long-stay-travel-demand": ("scene-stay", "縁側の向こうに山と町並みを望む和室"),
    "minpaku-fire-safety": ("hotel-room", "夜の客室"),
    "ota-vs-direct-booking": ("fuji-rapeseed", "菜の花畑と富士山"),
    "kominka-renovation-points": ("irori-room", "囲炉裏のある古民家の座敷"),
    "inn-local-economy": ("scene-walk", "灯りのともる夜の路地"),
    "cleaning-linen-operations": ("white-bed", "白いシーツの整ったベッド"),
    "inbound-regional-dispersion": ("fuji-train", "富士山を背に走る列車"),
    "minpaku-management-company": ("gassho-village", "合掌造りの家と山並み"),
    "akiya-lease-types": ("window-garden", "和室の窓から望む庭"),
    "listing-photo-tips": ("autumn-garden", "紅葉に彩られた日本庭園"),
    "tourism-labor-shortage": ("terraced-fields", "海を望む棚田と茅葺きの小屋"),
    "inn-startup-funding": ("fuji-lupin", "花畑の向こうに望む富士山"),
    "guest-review-tips": ("garden-boat", "庭園の池に浮かぶ舟"),
    "accommodation-tax": ("oshino-mill", "茅葺きの水車小屋と富士山"),
    "akiya-3000man-deduction": ("cherry-river", "川沿いの桜並木"),
    "kankei-jinko-and-inns": ("shrine-path", "木々に囲まれた参道"),
    "minpaku-investment-yield": ("mountain-dawn", "朝の光に照らされた山並み"),
    "case-rental-house-inn-first-year": ("analytics-paper", "数字の推移をまとめた資料（イメージ）"),
}


WEBP_WIDTHS = (800,)


def webp_variants(name):
    """写真の軽量版（WebP・幅800）を images/photos/w/ に作る。元の写真はそのまま残す"""
    from PIL import Image
    out_dir = os.path.join(OUT, "images", "photos", "w")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(OUT, "images", "photos", f"{name}.jpg")
    im = Image.open(src)
    ow = im.size[0]
    dst = os.path.join(out_dir, f"{name}-800.webp")
    if not (os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)):
        rgb = im.convert("RGB")
        tw = min(800, ow)
        rgb.resize((tw, round(im.size[1] * tw / ow)), Image.LANCZOS).save(dst, "WEBP", quality=76, method=6)
    return ow


def photo(name, cls="", alt="", width=1600, height=1000, sizes="100vw", lazy=True, priority=False):
    """写真を表示する。スマホなど小さい表示では軽量版（WebP・幅800）、大きい表示では元の写真を、ブラウザが自動で選ぶ"""
    ow = webp_variants(name)
    attrs = ' loading="lazy"' if lazy else ""
    attrs += ' fetchpriority="high"' if priority else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="images/photos/{name}.jpg" srcset="images/photos/w/{name}-800.webp 800w, images/photos/{name}.jpg {ow}w" '
            f'sizes="{sizes}" alt="{e(alt)}" width="{width}" height="{height}"{attrs} decoding="async">')


def thumb(a, size=""):
    """記事のサムネイル（写真）。カードは軽量版、記事トップは原寸を使う"""
    name, alt = ARTICLE_PHOTOS[a["slug"]]
    if size == "hero":
        return f"""<figure class="article__photo">{photo(name, alt=alt, width=1600, height=700, sizes="(max-width: 899px) 100vw, 800px", lazy=False, priority=True)}</figure>"""
    return f"""<div class="thumb thumb--photo">
              {photo(name, width=720, height=450, sizes="(max-width: 899px) 90vw, 400px")}
              <span class="thumb__cat">{e(MEDIA_CAT_NAMES[a["category"]])}</span>
              {thumb_banner(a)}
            </div>"""


def thumb_banner(a):
    """サムネイルの上に、記事の要点を短く載せる（ぱっと見で何の記事か分かるように）"""
    lines = "<br>".join(e(l) for l in a["short"].split("\n"))
    return f'<span class="thumb__banner" aria-hidden="true"><span class="thumb__kicker">{e(MEDIA_CAT_NAMES[a["category"]])}</span><span class="thumb__catch">{lines}</span></span>'


def _thumb_text(a, size=""):
    """記事のサムネイル（画像を使わない文字組みのカバー）"""
    lines = "<br>".join(e(l) for l in a["short"].split("\n"))
    return f"""<div class="thumb thumb--{a["tone"]}{(" thumb--" + size) if size else ""}" aria-hidden="true">
              <span class="thumb__cat">{e(MEDIA_CAT_NAMES[a["category"]])}</span>
              <span class="thumb__title">{lines}</span>
              <span class="thumb__brand">アキヤド</span>
            </div>"""


def card_tags(a):
    """記事カードのタグ：誰向けか（状況）とテーマ。ぱっと見で何の記事か分かるようにする"""
    who = [f'<span class="ctag ctag--who">{e(g["label"])}</span>' for g in guides_of(a["slug"])]
    topics = [f'<span class="ctag">{e(MEDIA_CAT_NAMES[t])}</span>' for t in a["topics"]]
    return f'<span class="ctags">{"".join((who[:1] + topics)[:3])}</span>'


def article_card(a, extra_class=""):
    return f"""          <a href="media/{a["slug"]}.html" class="media-card reveal{extra_class}" data-category="{a["category"]}" data-date="{a["date"]}">
            {thumb(a)}
            <div class="media-card__body">
              {card_tags(a)}
              <h3 class="media-card__title">{e(a["title"])}</h3>
              <time class="media-card__date" datetime="{a["date"]}">{fmt_date(a["date"])}</time>
            </div>
          </a>"""


def media_section(articles, eyebrow="Media", title="アキヤド", lead="", more=True, limit=3, keep_order=False):
    if keep_order is False:
        articles = sorted(articles, key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in articles)
    more_html = f'\n        <div class="media-more reveal"><a href="media.html" class="btn btn--ghost">記事一覧を見る {ARROW}</a></div>' if more else ""
    lead_html = f'\n          <p class="section-lead">{e(lead)}</p>' if lead else ""
    # 見出しが「アキヤド」のとき（コーポレートTOP）は、メディアのロゴを見せる
    title_html = (f'<a href="media.html" class="tlogo" aria-label="アキヤド（空き家と民泊のメディア）">{AKIYADO_MARK}'
                  f'<span class="tlogo__ja" translate="no">アキヤド</span></a><span class="tlogo__sub">空き家と民泊のメディア</span>'
                  if title == "アキヤド" else e(title))
    return f"""    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{e(eyebrow)}</span>
          <h2 class="section-title{" section-title--logo" if title == "アキヤド" else ""}">{title_html}</h2>{lead_html}
        </div>
        <div class="media-grid media-grid--scroll" data-limit="{limit}">
{cards}
        </div>{more_html}
      </div>
    </section>"""


# メディアの骨格：カテゴリ（一覧ページ）と、目的別のガイド（記事を読む順に並べた特集）
MEDIA_CAT_INFO = {
    "sell": ("Sell", "相続した家を手放すときの流れ、売るときの税金の特例、放置したときのリスク。売るかどうか迷っている段階から読める記事をまとめています。"),
    "lend": ("Lease", "家を貸すときの契約の種類、借り上げ、管理会社への委託。家を手放さずに、毎月の収入に変えるための選択肢をまとめています。"),
    "house": ("House", "空き家バンクでの探し方、宿に向く物件と場所の見極め、古い家の改修。建物と場所選びで失敗しないための知識をまとめています。"),
    "start": ("Start", "民泊と旅館業の違い、届出の流れ、消防設備。小さな宿を開業するまでに必要な手続きを、つまずきやすい点とあわせてまとめています。"),
    "money": ("Money", "開業資金の用意の仕方、補助金、税金、利回り。小さな宿や空き家活用を始める前に押さえておきたい、お金の話をまとめています。"),
    "operate": ("Operation", "稼働率と客室単価、予約サイトの使い方、清掃、レビュー。開業したあとに宿の売上と評判を育てる、運営の知識をまとめています。"),
    "trend": ("Trend", "訪日客の動向、長期滞在の広がり、関係人口。観光と地域の変化を公的なデータをもとに読み解き、地方の小さな宿の可能性を考えます。"),
}
# 読者の状況（ペルソナ）別のガイド。悩みが生まれる順に「段階」を分け、記事を並べる
MEDIA_GUIDES = [
    dict(key="sell", label="空き家を売りたい", title="空き家を売りたい方へ", service="operation", photo="old-town-street",
         who="相続した実家や、使っていない家を手放したい方",
         worries=["放置しているとどうなる？", "売るときの税金は？", "売る以外の選択肢は？"],
         lead="相続した実家や、使っていない家を手放したい。そう考えたときに知っておきたいことを、悩みが生まれる順に並べました。",
         stages=[
             ("まず知っておきたいこと", "放置した場合の負担と、空き家をめぐる制度の変化。", ["akiya-inherited-house-to-inn", "akiya-bank-guide"]),
             ("売る前に、比べておきたいこと", "売る以外に「貸す」「宿として活かす」という選択肢も。手取りと将来を比べて判断します。", ["akiya-lease-types", "shizuoka-yaizu-akiya-inn", "new-build-vs-used-house-inn"]),
             ("お金と税金", "売却したときの税金と、使える特例。", ["akiya-3000man-deduction"]),
         ]),
    dict(key="use", label="空き家を活かしたい", title="空き家を活かしたい方へ", service="operation", photo="thatched-house",
         who="家を手放さずに、収入や地域の役に立つ形で活かしたい方",
         worries=["古い家でも宿にできる？", "貸す？任せる？自分でやる？", "改修にいくらかかる？"],
         lead="思い出のある家を手放さずに、収入や地域の役に立つ形で活かしたい。活用の選び方から改修、お金のことまでを順番に。",
         stages=[
             ("活かし方を知る", "空き家が宿として、地域の中でどんな価値を持つのか。", ["akiya-inherited-house-to-inn", "akiya-regional-revitalization", "inn-local-economy"]),
             ("活かし方を選ぶ", "貸す・運営を任せる・自分で営業する。契約と法令の違い。", ["akiya-lease-types", "minpaku-vs-ryokan-law", "minpaku-management-company"]),
             ("家を整える", "残すもの・直すもの、消防設備の基準。", ["kominka-renovation-points", "minpaku-fire-safety", "new-build-vs-used-house-inn"]),
             ("お金の見通しを立てる", "補助金と、収益の見込みの立て方。", ["small-inn-subsidies", "airdna-revenue-simulation"]),
         ]),
    dict(key="side", label="副業で宿をはじめたい", title="副業で宿をはじめたい方へ", service="management", photo="white-bedroom",
         who="本業を続けながら、民泊や小さな宿に挑戦してみたい方",
         worries=["副業でも民泊はできる？", "資金はいくら必要？", "本業があっても運営できる？"],
         lead="本業を続けながら、民泊や小さな宿に挑戦してみたい。市場の見方から開業の手続き、資金、運営を任せる方法までを順番に。",
         stages=[
             ("市場と可能性を知る", "どんな旅行者が、どんな宿を求めているのか。投資としての考え方。", ["long-stay-travel-demand", "inbound-regional-dispersion", "minpaku-investment-yield"]),
             ("物件とお金を準備する", "物件の探し方、収益の見込み、資金の集め方。", ["akiya-bank-guide", "airdna-revenue-simulation", "inn-startup-funding", "small-inn-subsidies"]),
             ("開業の手続きを進める", "民泊か旅館業か、消防、管理を任せる体制。", ["minpaku-start-steps", "minpaku-vs-ryokan-law", "minpaku-fire-safety", "minpaku-management-company"]),
             ("運営して、育てる", "数字の読み方、集客、レビュー、清掃、宿泊税。", ["inn-kpi-basics", "ota-vs-direct-booking", "listing-photo-tips", "guest-review-tips", "cleaning-linen-operations", "accommodation-tax"]),
         ]),
]
# 記事は今後も増える前提。記事データに guides=[("sell", 2)]（ガイドのkey, Stepの番号）と書けば、
# そのガイドの該当Stepの末尾に自動で並ぶ（ここのリストを書き換えなくてよい）
for _a in ARTICLES:
    for _key, _step in _a.get("guides", []):
        _st = next(g for g in MEDIA_GUIDES if g["key"] == _key)["stages"][_step - 1][2]
        if _a["slug"] not in _st:
            _st.append(_a["slug"])
for _g in MEDIA_GUIDES:
    _g["slugs"] = list(dict.fromkeys(x for _, _, xs in _g["stages"] for x in xs))
MEDIA_GUIDE_FOR_CAT = {"sell": "sell", "lend": "use", "house": "use", "start": "side", "money": "side", "operate": "side", "trend": "use"}
# よくある悩みから記事へ（読者の言葉で書く）
MEDIA_QUESTIONS = [
    ("sell", "相続した実家、放置するとどうなる？", "akiya-inherited-house-to-inn"),
    ("sell", "空き家を売ったら、税金はどれくらいかかる？", "akiya-3000man-deduction"),
    ("use", "観光地ではない場所の空き家でも、宿になる？", "shizuoka-yaizu-akiya-inn"),
    ("use", "家を貸すなら、どんな契約がいい？", "akiya-lease-types"),
    ("use", "古い家を宿にするなら、どこを直すべき？", "kominka-renovation-points"),
    ("side", "副業で民泊をはじめるには、何から？", "minpaku-start-steps"),
    ("side", "民泊と旅館業、どちらで始めればいい？", "minpaku-vs-ryokan-law"),
    ("side", "本業があっても、宿の運営はできる？", "minpaku-management-company"),
    ("side", "開業資金は、どう用意する？", "inn-startup-funding"),
    ("side", "実際、初期投資はどれくらいで回収できる？", "case-rental-house-inn-first-year"),
    ("side", "宿の収益は、どれくらい見込める？", "airdna-revenue-simulation"),
]
MEDIA_LEAD = "空き家を売りたい、活かしたい。副業で民泊をはじめたい。その悩みに、宿を運営する私たちが順を追ってお答えします。"


# 記事の途中に置く相談の案内（読者の状況＝ガイドごとに言葉を変える）
CV_MESSAGES = {
    "sell": "売るか、活かすか。物件の状況をうかがい、いちばん負担の少ない方法を無料でご提案します。",
    "use": "その家、宿として活かせるか。現地と周辺の宿を調べ、収支の見込みを無料で試算します。",
    "side": "物件選び、許可、収支の見通し。民泊を始める前の疑問に、宿を運営する私たちが無料でお答えします。",
    "": "空き家の売却・活用、民泊の開業について、宿を運営する私たちが無料でご相談に乗ります。",
}


def guide_of(slug):
    return next((g for g in MEDIA_GUIDES if slug in g["slugs"]), None)


def guides_of(slug):
    return [g for g in MEDIA_GUIDES if slug in g["slugs"]]


# アキヤドのマーク（角の丸い四角に、家のかたち）
AKIYADO_MARK = ('<svg class="amark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#2E6B47"/>'
                '<path d="M7.5 15.6 16 8.6l8.5 7v8.6a1.3 1.3 0 0 1-1.3 1.3h-4.7v-5.7h-5v5.7H8.8a1.3 1.3 0 0 1-1.3-1.3z" fill="#fff"/></svg>')


def media_logo(cls="mlogo"):
    """メディアのロゴ（文字組み）。名前「アキヤド」（空き家＋宿）と、何のメディアかを示す添え書き"""
    return f"""<span class="{cls}">{AKIYADO_MARK}<span class="{cls}__ja">アキヤド</span><span class="{cls}__sub">空き家と民泊のメディア</span></span>"""


def media_header(current=""):
    return f"""  <header class="header header--media">
    <div class="container mheader__inner">
      <a href="media.html" class="mheader__logo">{media_logo()}</a>
      <div class="mheader__right">
      <a href="contact.html?category=document&amp;from=akiyado-header" class="mheader__cta mheader__cta--sub" data-cta="media-header-doc">資料請求</a>
      <a href="contact.html?from=akiyado" class="mheader__cta" data-cta="media-header">無料相談</a>
      <button type="button" class="mmenu-btn" aria-label="メニューを開く" aria-expanded="false" aria-controls="mnav"><span></span><span></span></button>
      </div>
    </div>
{media_nav(current)}
  </header>"""


def media_footer():
    guides = "".join(f'<li><a href="media/guide-{g["key"]}.html">{e(g["title"])}</a></li>' for g in MEDIA_GUIDES)
    themes = "".join(f'<li><a href="media/category-{k}.html">{e(n)}</a></li>' for k, n in MEDIA_CATEGORIES)
    return f"""  <footer class="mfooter">
    <div class="container">
      <div class="mfooter__top">
        <div>
          <a href="media.html" class="mfooter__logo">{media_logo()}</a>
          <p class="mfooter__lead">空き家を、売る。活かす。民泊を、はじめる。<br>宿を運営する私たちが、悩みに沿ってお届けします。</p>
        </div>
        <div class="mfooter__cols">
          <div><p class="mfooter__label">状況から読む</p><ul>{guides}</ul></div>
          <div><p class="mfooter__label">テーマから探す</p><ul>{themes}</ul></div>
          <div><p class="mfooter__label">アキヤドについて</p><ul>
            <li><a href="media/learn.html">基礎から学ぶ</a></li>
            <li><a href="media/search.html">記事をさがす</a></li>
            <li><a href="media/plans.html">アキヤドのプラン</a></li>
            <li><a href="media/company.html">運営会社について</a></li>
            <li><a href="contact.html">ご相談・お問い合わせ</a></li>
            <li><a href="privacy.html">プライバシーポリシー</a></li>
          </ul></div>
        </div>
      </div>
      <div class="mfooter__bottom">
        <a href="index.html" class="mfooter__corp"><img src="images/logo/logo-white.svg" alt="RIVIA&amp;CO." width="325" height="64" loading="lazy"><span>このメディアは合同会社RIVIA&amp;CO.が運営しています</span></a>
        <p>&copy; 2026 合同会社RIVIA&amp;CO.</p>
      </div>
    </div>
  </footer>"""


def media_cta(category="operation"):
    """アキヤドの相談ブロック。気軽さ（無料・全国・営業なし）を先に伝える"""
    return f"""    <section class="section mcta">
      <div class="container">
        <div class="mcta__box reveal">
          <p class="mcta__en">Consultation</p>
          <h2 class="mcta__title">空き家のこと、<br class="sp-only">まずは気軽にご相談ください。</h2>
          <p class="mcta__lead">売るか、活かすか、民泊にするか。まだ決めていない段階でも大丈夫です。<br class="pc-only">宿を運営する私たちが、物件の状況に合わせてお答えします。</p>
          <ul class="mcta__points"><li>相談・お見積りは無料</li><li>全国対応・オンライン可</li><li>しつこい営業はしません</li></ul>
          <div class="mcta__btns">
            <a href="contact.html?category={category}&amp;from=akiyado" class="mbtn" data-cta="media-bottom">無料で相談する {ARROW}</a>
            {plan_doc_link("bottom")}
          </div>
          <p class="mcta__plans"><a href="media/plans.html">アキヤドのプランを見る {ARROW}</a></p>
          <p class="mcta__note">運営：合同会社RIVIA&amp;CO.（宿泊施設の運営・空き家再生）</p>
        </div>
      </div>
    </section>"""


# ---------------------------------------------------------------- アキヤド：アキヤドのプラン（記事を読んだ人が「頼んだらどうなるか」を知る場所）
# 実際のお客様の声がそろうまでは公開しない（作り話の口コミは、景品表示法の優良誤認やステマ規制に触れるおそれがある）
SHOW_SAMPLE_VOICES = os.environ.get("SHOW_SAMPLE_VOICES") == "1"
SAMPLE_VOICES = [
    ("use", "60代・相続した実家を活用", "おまかせコース",
     "固定資産税と草刈りのためだけに通っていた実家が、毎月の家賃を生む宿になりました。改修の段取りも運営もお任せできたので、私がしたのは契約と、ときどき届くレポートを読むことくらいです。"),
    ("side", "40代・会社員・副業で開業", "伴走コース",
     "届出の順番、写真の撮り方、料金の決め方まで一緒に考えてもらえました。平日は本業に集中して、週末にゲストとの時間を楽しめています。ひとりで始めていたら、途中で止まっていたと思います。"),
    ("sell", "70代・遠方の空き家を売却", "アキヤド買取プラン",
     "遠くて管理に行けず、ずっと気がかりでした。現地を見てもらい、売る場合と貸す場合の両方を説明してもらったうえで、納得して手放せました。家が宿として使われると聞いて、ほっとしています。"),
]
MEDIA_PLAN_GROUPS = [
    ("sell", "空き家を売りたい方", "手放したいけれど、買い手がつくか不安。そんな家もご相談ください。", "operation", ["アキヤド買取プラン"]),
    ("use", "空き家を活かしたい方", "家は持ったまま、宿として活かして収入に。改修や運営の手間はかかりません。", "operation", ["おまかせコース", "売上シェアコース"]),
    ("side", "副業で宿をはじめたい方", "物件選びや許可から開業後の集客まで。任せる範囲を選べます。", "management", ["伴走コース", "運営代行コース", "共同出資コース"]),
]
PLAN_FLOW = [
    ("無料相談・資料請求", "フォームから、物件や状況を気軽にお知らせください。オンラインでもお話しできます。"),
    ("現地調査・収支の試算", "物件と周辺の宿を調べ、売る・貸す・宿にする場合の見込みを無料でお出しします。"),
    ("プランのご提案", "物件とご希望に合わせて、条件を具体的にご提案します。ここで断っていただいても構いません。"),
    ("ご契約・開業準備", "改修や許可、写真や予約ページの準備まで、アキヤドが進めます。"),
]
PLAN_FAQ = [
    ("相談だけでも大丈夫ですか？", "はい。売るか活かすか決めていない段階でも、お気軽にご相談ください。ご提案を聞いたうえで、お断りいただいても構いません。"),
    ("相談や見積りに費用はかかりますか？", "ご相談、現地調査、収支の試算、プランのご提案までは無料です。"),
    ("遠方の物件でも相談できますか？", "全国の物件のご相談をお受けしています。初回はオンラインでお話しできます。"),
    ("資料には何が書いてありますか？", "各プランの仕組みと条件の考え方、ご相談から開業までの流れ、アキヤドが運営している宿の実績をまとめています。"),
]


def plan_doc_link(category, label="資料をもらう（無料）", cta="media-doc"):
    """サービス資料の請求（お問い合わせフォームで「サービス資料の請求」を選んだ状態にする）"""
    return f'<a href="contact.html?category=document&amp;from=akiyado-{category}" class="mbtn mbtn--sub" data-cta="{cta}">{label} {ARROW}</a>'


def media_plan_card(p, key, money_label="受け取り方"):
    # アキヤドの中では、提供する主語を「アキヤド」に（プランのデータはコーポレートと共通）
    p = {k: (v.replace("RIVIA", "アキヤド") if isinstance(v, str) else v) for k, v in p.items()}
    rec = '<span class="mplan__badge">おすすめ</span>' if p.get("rec") else ""
    init = f'<div><dt>初期費用</dt><dd>{e(p["init"])}</dd></div>' if p.get("init") else ""
    who = "".join(f"<li>{e(w)}</li>" for w in p["who"])
    return f"""            <article class="mplan{" is-rec" if p.get("rec") else ""}">
              {rec}{brand_kicker(p)}<h3 class="mplan__name">{e(p["name"])}</h3>
              <p class="mplan__catch">{e(p["catch"])}</p>
              <dl class="mplan__spec">{init}<div><dt>{e(p.get("money_label", money_label))}</dt><dd>{e(p["monthly"])}<span>{e(p["example"])}</span></dd></div></dl>
              <p class="mplan__who-label">こんな方に</p>
              <ul class="mplan__who">{who}</ul>
            </article>"""


def media_plans_page():
    """アキヤドのプラン一覧。まずカードで端的に紹介し、詳しくは各サービスのページへ"""
    from figures import icon
    groups = []
    for sv in MEDIA_SERVICES:
        c = MEDIA_SERVICE_CARDS[sv["key"]]
        spec = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in c["spec"])
        tags = "".join(f'<li>{e(n)}</li>' for n in c["plans"])
        groups.append(f"""        <article class="msvc reveal" id="{sv["key"]}">
          <div class="msvc__visual">{photo(c["photo"], width=720, height=540, sizes="(max-width: 899px) 100vw, 360px")}<p class="msvc__who">{e(sv["eyebrow"])}</p></div>
          <div class="msvc__body">
            <h2 class="msvc__name">{e(sv["name"])}</h2>
            <p class="msvc__summary">{e(c["summary"])}</p>
            <dl class="msvc__spec">{spec}</dl>
            <p class="msvc__plans-label">選べるプラン</p>
            <ul class="msvc__plans">{tags}</ul>
            <a href="media/{sv["slug"]}.html" class="mbtn mbtn--sub msvc__more" data-cta="media-service-card">サービスの詳細を見る {ARROW}</a>
          </div>
        </article>""")
    voices = ""
    if SHOW_SAMPLE_VOICES:
        vs = "\n".join(f"""          <figure class="mvoice reveal">
            <blockquote class="mvoice__text">{e(t)}</blockquote>
            <figcaption class="mvoice__who"><span class="mvoice__plan">{e(plan)}</span>{e(who)}</figcaption>
          </figure>""" for _, who, plan, t in SAMPLE_VOICES)
        voices = f"""
    <section class="section msec" id="voices">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Voices</p><h2 class="msec__title">ご利用いただいた方の声</h2></div></div>
        <div class="mvoices">
{vs}
        </div>
      </div>
    </section>
"""
    flow = "\n".join(f"""          <li class="mflow__step reveal"><span class="mflow__no">{i:02d}</span><h3 class="mflow__title">{e(t)}</h3><p class="mflow__text">{e(d)}</p></li>"""
                     for i, (t, d) in enumerate(PLAN_FLOW, 1))
    def jump_item(sv):
        worries = "".join(f'<span class="mjump__worry">{e(w)}</span>' for w in sv["worries"][:2])
        return (f'<li><a href="#{sv["key"]}" class="mjump__item"><span class="mjump__who">{e(sv["eyebrow"])}</span>'
                f'{worries}<span class="mjump__name">→ {e(sv["name"])}</span></a></li>')
    jump = "".join(jump_item(sv) for sv in MEDIA_SERVICES)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("アキヤドのプラン", "")])
    body = f"""{media_hero("Services", "アキヤドのプラン", "記事を読んで、具体的に考えたくなったら。空き家の買取・借り上げから、民泊の開業・運営まで。宿を運営するアキヤドにご相談いただけることをまとめました。", crumbs)}

    <section class="section msec msec--first">
      <div class="container">
        <p class="mjump__label reveal">こんなお悩みなら</p>
        <ul class="mjump reveal">{jump}</ul>
        <div class="msvcs">
{chr(10).join(groups)}
        </div>
      </div>
    </section>
{voices}
    <section class="section section--soft msec" id="flow">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Flow</p><h2 class="msec__title">ご相談から開業まで</h2></div></div>
        <ol class="mflow">
{flow}
        </ol>
        <div class="mplans__cta reveal">
          <a href="contact.html?category=operation&amp;from=akiyado-plans" class="mbtn" data-cta="media-plans">無料で相談する {ARROW}</a>
          {plan_doc_link("plans")}
        </div>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">FAQ</p><h2 class="msec__title">よくある質問</h2></div></div>
        <div class="faq reveal">
{faq_html(PLAN_FAQ)}
        </div>
      </div>
    </section>

{media_cta()}"""
    ld = [{"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PLAN_FAQ]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "TOP", "item": f"{SITE}/"},
              {"@type": "ListItem", "position": 2, "name": "アキヤド", "item": f"{SITE}/media.html"},
              {"@type": "ListItem", "position": 3, "name": "アキヤドのプラン"}]}]
    page("media/plans.html", "アキヤドのプラン｜空き家の買取・借り上げ、民泊の開業・運営支援｜アキヤド",
         "空き家の買取、借り上げ（固定家賃・売上シェア）、民泊の開業・運営代行まで。宿を運営するアキヤドに任せた場合のプランと条件の目安、ご相談から開業までの流れをまとめています。",
         body, current="media", jsonld=ld, mnav="plans")


# ---------------------------------------------------------------- アキヤド：サービスごとのページ（読者の状況ごとに、悩み→解決→プラン→流れ→実績→質問）
MEDIA_SERVICES = [
    dict(key="sell", slug="service-kaitori", name="アキヤド買取プラン", category="operation",
         eyebrow="空き家を売りたい方へ", title="買い手が見つからない家も、\n宿として活かせるなら買い取れます。",
         lead="相続した家、遠方で管理できない家。アキヤドは「宿として再生できるか」という目で物件を見るため、一般の仲介では値段がつきにくい家もご相談いただけます。",
         worries=["相続した実家を、どうしたらいいか決められない", "遠方に住んでいて、管理や草刈りに通うのが負担", "不動産会社に「古いので売れにくい」と言われた",
                  "固定資産税だけを払い続けている", "手放す前に、ほかの選択肢とも比べたい"],
         strengths=[("bed", "宿として活かす目線で査定", "立地や建物を「宿になるか」で見るため、住まいとしては評価されにくい古い家でも検討できます。"),
                    ("handshake", "売る・貸すを比べてご提案", "買取だけでなく、借り上げで家を残す場合の収入も試算します。比べたうえで選べます。"),
                    ("doc", "売却までの段取りを一緒に", "必要な手続きや、専門家に相談する順番を一緒に整理します。")],
         steps=[("bubble", "無料相談", "状況やご希望を伺います"), ("search", "現地を拝見・査定", "宿として活かせるかも確認"),
                ("handshake", "売る・貸すを比べてご提案", "収支の見込みとあわせて"), ("key", "ご契約・お引き渡し", "")],
         faq=[("古くて傷んでいても、買い取ってもらえますか？", "建物の状態や立地によります。宿として再生できるかを現地で確認したうえで、ご提案します。"),
              ("家の中に荷物が残っていても大丈夫ですか？", "まずはそのままの状態で拝見します。片付けの進め方も含めてご相談ください。"),
              ("査定に費用はかかりますか？", "現地の拝見と査定、ご提案までは無料です。"),
              ("相続の手続きが終わっていなくても相談できますか？", "ご相談いただけます。売却には名義の変更が必要になるため、進め方も一緒に整理します。")]),
    dict(key="use", slug="service-kariage", name="アキヤド借り上げプラン", category="operation",
         eyebrow="空き家を活かしたい方へ", title="家は持ったまま、\n宿として活かして毎月の収入に。",
         lead="アキヤドが空き家を借り上げ、改修から宿の運営まで行います。オーナー様は運営の手間をかけずに、家賃を受け取れます。",
         worries=["思い出のある家を、手放したくはない", "空き家のまま傷んでいくのが心配", "貸したいが、借り手が見つかる地域ではない",
                  "改修にまとまったお金はかけられない", "宿に興味はあるが、運営する時間がない"],
         strengths=[("yen", "初期費用をかけずに始められる", "おまかせコースなら、改修・家具などの費用はアキヤドがほぼ負担します（建物の構造的な補修を除く）。"),
                    ("bed", "宿の運営はすべてアキヤド", "集客・予約・清掃・ゲスト対応まで、宿を運営している私たちが行います。"),
                    ("heart", "家を残し、まちに人を呼ぶ", "家は持ったまま。旅行者が訪れることで、まちにも人の流れが生まれます。")],
         steps=[("house", "オーナー様が家を貸す", "家はオーナー様のまま"), ("tool", "アキヤドが改修・開業準備", "家具・設備・許可まで"),
                ("bed", "宿として運営", "集客・清掃・ゲスト対応"), ("yen", "毎月の家賃をお支払い", "プランに応じて上乗せも")],
         faq=[("契約期間はどれくらいですか？", "物件ごとにご提案します。改修の費用をアキヤドが負担するため、一定の期間を前提にした契約になります。契約は更新を前提としています。"),
              ("将来、家を使いたくなったらどうなりますか？", "契約の形（定期借家など）によっては、期間の満了で返していただくこともできます。ご希望を最初にお聞かせください。"),
              ("どんな家でも借り上げてもらえますか？", "立地や建物の状態、法令上、宿として営業できるかによります。現地調査と収支の試算をしたうえでご提案します。"),
              ("近所に迷惑がかからないか心配です。", "利用ルールの案内や、騒音・ごみへの対応など、周辺への配慮も運営に含めて行います。")]),
    dict(key="side", slug="service-kaigyo", name="アキヤド開業・運営プラン", category="management",
         eyebrow="副業で宿をはじめたい方へ", title="はじめての民泊を、\n開業準備から運営まで伴走します。",
         lead="物件選び、許可や届出、写真や料金の決め方、開業後の集客まで。実際に宿を運営しているアキヤドが、任せたい範囲に合わせて支えます。",
         worries=["何から始めればいいか分からない", "民泊と旅館業、どちらで始めるべきか迷っている", "本業が忙しく、運営に時間をかけられない",
                  "物件が宿として収益を出せるか見通せない", "予約が入るページのつくり方が分からない"],
         strengths=[("doc", "開業までの手続きを一緒に", "制度の選び方、消防や届出の段取りなど、つまずきやすいところを先回りして進めます。"),
                    ("chart", "収支の見通しを数字で", "周辺の宿の料金と稼働を調べ、無理のない計画を一緒に立てます。"),
                    ("users", "任せる範囲を選べる", "現場は自分で担う伴走から、まるごと任せる運営代行、共同出資まで選べます。")],
         steps=[("search", "物件と制度の確認", "民泊新法か旅館業か"), ("chart", "収支の試算", "周辺の宿の料金と稼働から"),
                ("tool", "開業準備", "設備・届出・予約ページ"), ("bed", "開業・運営", "任せる範囲はプランで選ぶ")],
         faq=[("物件をまだ持っていなくても相談できますか？", "はい。物件選びの段階からご相談いただけます。"),
              ("遠方の物件でも、運営を任せられますか？", "運営代行コースでは、清掃や駆けつけの体制も含めてご提案します。対応エリアはご相談ください。"),
              ("手数料のほかに、かかる費用はありますか？", "清掃費・リネン・光熱費などの実費は別途かかります。プランごとに事前にご説明します。"),
              ("民泊新法と旅館業、どちらがいいですか？", "営業したい日数や物件の条件で変わります。目的を伺ったうえで、おすすめをお伝えします。")]),
]
MEDIA_SERVICE_BY_KEY = {sv["key"]: sv for sv in MEDIA_SERVICES}
# 一覧ページのカード：アイコン・ひとこと・条件の目安
MEDIA_SERVICE_CARDS = {
    "sell": dict(photo="old-town-street", summary="宿として活かせるかという目線で、相続した家や使っていない家を買い取ります。貸した場合との比較もお出しします。",
                 spec=[("受け取り方", "売却代金を一括で"), ("費用", "相談・査定は無料")], plans=["アキヤド買取プラン"]),
    "use": dict(photo="irori-room", summary="家は持ったまま。アキヤドが借り上げて宿に改修・運営し、オーナー様に家賃をお支払いします。",
                spec=[("初期費用", "ほぼなし（おまかせコース）"), ("受け取り方", "毎月の家賃")], plans=["おまかせコース", "売上シェアコース"]),
    "side": dict(photo="scene-stay", summary="物件選び・届出から、開業後の集客と運営まで。任せたい範囲に合わせて伴走します。",
                 spec=[("費用", "売上の10%〜（伴走コース）"), ("任せる範囲", "開業準備のみ〜運営まで")], plans=["伴走コース", "運営代行コース", "共同出資コース"]),
}



# サービスページの「ご相談からの流れ」。顧客が不安にならないよう、期間・お願いすること・費用まで書く
# 各ステップ：(見出し, 期間の目安, 内容, お客様にお願いすること, アキヤドが行うこと, 費用)
MEDIA_FLOWS = {
    "sell": [
        ("無料相談", "当日〜数日", "フォームからのご連絡のあと、メールかオンラインで状況とご希望を伺います。まだ売ると決めていなくても大丈夫です。",
         "物件の場所と、わかる範囲の状況（築年数・空き家になった時期など）をお知らせください。", "ご相談内容を確認し、現地調査の日程をご提案します。", "無料"),
        ("現地を拝見・査定", "1〜2週間", "建物の状態や周辺の環境を確認し、宿として活かせるかも含めて査定します。",
         "立ち会いが難しい場合は、鍵の受け渡し方法をご相談ください。図面や固定資産税の通知書があればご用意ください。", "建物・立地・法令上の条件を調べ、査定額と根拠をまとめます。", "無料"),
        ("売る・貸すを比べてご提案", "調査から1〜2週間", "買取の金額に加えて、借り上げで家を残した場合の収入の見込みもお出しします。",
         "ご提案を見て、ご家族とも相談のうえで、ご検討ください。", "それぞれの手取りや手間の違いを、わかりやすく比べてご説明します。", "無料。ここでお断りいただいても構いません"),
        ("ご契約・お引き渡し", "1〜2か月", "条件にご納得いただけたら、売買契約を結び、代金のお支払いと物件のお引き渡しを行います。",
         "契約書の内容のご確認と、登記に必要な書類のご準備をお願いします。", "契約から登記までの段取りを進めます。必要に応じて司法書士などの専門家とも連携します。", "登記などの実費は、契約前にご説明します"),
    ],
    "use": [
        ("無料相談", "当日〜数日", "フォームからのご連絡のあと、メールかオンラインで、物件の状況と「家をどうしたいか」を伺います。",
         "物件の場所と、わかる範囲の状況をお知らせください。将来使う予定があるかも教えてください。", "ご希望に合いそうな進め方と、現地調査の日程をご提案します。", "無料"),
        ("現地調査・収支の試算", "2〜3週間", "建物の状態と、周辺の宿の料金や稼働を調べ、宿にした場合の収支を試算します。",
         "可能であれば立ち会いをお願いします。図面などの資料があればご用意ください。", "改修が必要な箇所、法令上の条件、見込める家賃をまとめます。", "無料"),
        ("コースと条件のご提案", "調査から1〜2週間", "おまかせコース・売上シェアコースのうち、物件とご希望に合う条件をご提案します。",
         "家賃や契約期間、将来の使い方のご希望をお聞かせください。", "家賃・契約期間・改修の負担の分け方を、具体的な数字でご提示します。", "無料。ここでお断りいただいても構いません"),
        ("ご契約・改修・開業準備", "2〜4か月", "賃貸借契約を結んだあと、アキヤドが改修・家具の準備・許可の手続き・予約ページの作成まで進めます。",
         "契約内容のご確認をお願いします。改修の内容は、事前にご説明して進めます。", "改修、家具・設備、消防や許可の手続き、写真撮影、予約ページの準備を行います。", "おまかせコースは初期費用ほぼなし（建物の構造的な補修を除く）"),
        ("宿として運営・家賃のお支払い", "開業後、毎月", "集客・予約・清掃・ゲスト対応はアキヤドが行い、オーナー様には毎月家賃をお支払いします。",
         "特にありません。気になることがあれば、いつでもご連絡ください。", "運営の状況を定期的にご報告し、近隣への配慮も含めて宿を運営します。", "運営の手間・費用はかかりません"),
    ],
    "side": [
        ("無料相談", "当日〜数日", "フォームからのご連絡のあと、オンラインで、始めたい宿のイメージやご予算、物件の有無を伺います。",
         "物件が決まっていれば場所を、まだなら希望のエリアやご予算をお知らせください。", "進め方の全体像と、最初に確認すべきことをお伝えします。", "無料"),
        ("物件と制度の確認", "1〜3週間", "物件が宿として営業できるか、民泊新法と旅館業のどちらが合うかを確認します。",
         "物件の資料（図面・登記・管理規約など）をご用意ください。", "用途地域や条例、消防の条件を調べ、選ぶべき制度をご提案します。", "無料"),
        ("収支の試算とコースのご提案", "1〜2週間", "周辺の宿の料金と稼働をもとに収支を試算し、伴走・運営代行・共同出資から合うコースをご提案します。",
         "本業との両立や、どこまで自分で関わりたいかを教えてください。", "悲観的な場合も含めた収支の見通しと、コースごとの費用をご提示します。", "無料。ここでお断りいただいても構いません"),
        ("開業準備", "1〜3か月", "設備の準備、消防の手続き、届出や許可申請、写真撮影と予約ページの作成を進めます。",
         "コースに応じて、設備の購入や届出の名義人としての手続きをお願いします。", "やることの一覧と期限をお渡しし、手続きや予約ページづくりを一緒に進めます。", "コースの費用は契約前にご説明します。設備などの実費は別途"),
        ("開業・運営", "開業後", "伴走コースは集客と料金の考え方を、運営代行コースは日々の運営まで、アキヤドが担います。",
         "伴走コースでは、清掃やゲスト対応など現場の運営をお願いします。", "予約の状況や売上を定期的にご報告し、改善の打ち手をご提案します。", "売上に応じた手数料（コースにより異なります）"),
    ],
}


def detail_flow(key):
    steps = MEDIA_FLOWS[key]
    items = "\n".join(f"""          <li class="dflow__step reveal">
            <div class="dflow__head"><span class="dflow__no">STEP {i:02d}</span><span class="dflow__term">{e(term)}</span></div>
            <div class="dflow__body">
              <h3 class="dflow__title">{e(t)}</h3>
              <p class="dflow__text">{e(d)}</p>
              <dl class="dflow__roles">
                <div><dt>お客様にお願いすること</dt><dd>{e(you)}</dd></div>
                <div><dt>アキヤドが行うこと</dt><dd>{e(we)}</dd></div>
              </dl>
              <p class="dflow__cost"><span>費用</span>{e(cost)}</p>
            </div>
          </li>""" for i, (t, term, d, you, we, cost) in enumerate(steps, 1))
    return f"""        <ol class="dflow">
{items}
        </ol>
        <ul class="dflow__notes reveal">
          <li>ご提案まではすべて無料です。どの段階でも、お断りいただけます。</li>
          <li>しつこい営業や、ご希望のない電話はいたしません。</li>
          <li>期間は目安です。物件の状態や手続きの状況によって前後します。</li>
        </ul>"""


def media_service_page(sv):
    from figures import icon, flow as fig_flow
    key = sv["key"]
    grp = next(g for g in MEDIA_PLAN_GROUPS if g[0] == key)
    _, label, _, src, names = grp
    money_label = "受け取り方" if src == "operation" else "費用"
    plans = sorted((p for p in PLANS[src]["plans"] if p["name"] in names), key=lambda p: names.index(p["name"]))
    plan_cards = "\n".join(media_plan_card(p, key, money_label) for p in plans)
    worries = "".join(f'<li>{e(w)}</li>' for w in sv["worries"])
    strengths = "\n".join(f"""          <li class="msv-point reveal" data-delay="{i - 1}">
            <span class="msv-point__no">POINT {i:02d}</span>
            <h3 class="msv-point__title">{e(t)}</h3>
            <p class="msv-point__text">{e(d)}</p>
          </li>""" for i, (ic, t, d) in enumerate(sv["strengths"], 1))
    g = next((x for x in MEDIA_GUIDES if x["key"] == key), None)
    related = [ARTICLE_BY_SLUG[sl] for sl in (g["slugs"] if g else [])]
    reviews = "\n".join(f"""            <figure class="mvoice reveal"><blockquote class="mvoice__text">{e(r["text"])}</blockquote>
              <figcaption class="mvoice__who"><span class="mvoice__plan">NODE Shimoda</span>{e(r["who"])}・{e(r["date"])}</figcaption></figure>""" for r in NODE_REVIEWS)
    title_html = "<br>".join(e(t) for t in sv["title"].split("\n"))
    crumbs = media_crumbs([("アキヤド", "media.html"), ("アキヤドのプラン", "media/plans.html"), (sv["name"], "")])
    cta_band = f"""        <div class="msv-band reveal">
          <p class="msv-band__text">まずは話を聞いてみたい方も、資料で比べたい方も。<br class="pc-only">ご相談・資料のお届けは無料です。</p>
          <div class="msv-band__btns">
            <a href="#msv-form" class="mbtn" data-cta="media-service-mid">無料で相談する {ARROW}</a>
            {plan_doc_link(sv["slug"])}
          </div>
        </div>"""
    body = f"""    <section class="mhero msv-hero">
      <div class="container">{crumbs}
        <div class="msv-hero__grid">
          <div class="msv-hero__text">
            <p class="mhero__en reveal">{e(sv["eyebrow"])}</p>
            <h1 class="msv-hero__title reveal" data-delay="1">{title_html}</h1>
            <p class="mhero__lead reveal" data-delay="2">{e(sv["lead"])}</p>
            <ul class="mcta__points msv-hero__points reveal" data-delay="2"><li>相談・お見積りは無料</li><li>全国対応・オンライン可</li><li>しつこい営業はしません</li></ul>
          </div>
          <div id="msv-form">
{quick_form(sv["category"], sv["name"]).replace('class="qform reveal"', 'class="qform qform--media reveal"').replace('data-thanks="thanks.html?form=contact"', 'data-thanks="thanks.html"').replace("【RIVIA&amp;CO.】", "【アキヤド】")}
          </div>
        </div>
      </div>
    </section>

    <section class="section msec msec--first">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Worries</p><h2 class="msec__title">こんなお悩みはありませんか？</h2></div></div>
        <ul class="msv-worries reveal">{worries}</ul>
        <p class="msv-answer reveal">そのお悩み、<strong>宿を運営するアキヤド</strong>にご相談ください。</p>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Why Akiyado</p><h2 class="msec__title">{e(sv["name"])}が選ばれる理由</h2></div></div>
        <ol class="msv-points">
{strengths}
        </ol>
{cta_band}
      </div>
    </section>

    <section class="section msec" id="plans">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Plans</p><h2 class="msec__title">プランと条件の目安</h2></div></div>
        <div class="mplans__cards mplans__cards--{len(plans)} reveal">
{plan_cards}
        </div>
        <p class="mplans__note">{e(PLANS[src]["note"])}</p>
        <p class="mcta__plans"><a href="media/plans.html">ほかのサービスも見る {ARROW}</a></p>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">How it works</p><h2 class="msec__title">ご相談からの流れ</h2></div></div>
{detail_flow(key)}
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Track record</p><h2 class="msec__title">アキヤドが運営している宿</h2></div></div>
        <div class="msv-record reveal">
          <p class="msv-record__lead">アキヤドは、静岡県下田市で一棟貸しの宿「NODE Shimoda」を自ら運営しています。<br class="pc-only">記事やご提案は、現場で確かめた運営の知識をもとにしています。</p>
          <p class="msv-record__label">ゲストの声（Airbnbのレビューより抜粋）</p>
          <div class="mvoices">
{reviews}
          </div>
          <p class="mcta__plans"><a href="index.html#project">運営実績を見る {ARROW}</a></p>
        </div>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">FAQ</p><h2 class="msec__title">よくある質問</h2></div></div>
        <div class="faq reveal">
{faq_html(sv["faq"])}
        </div>
{cta_band}
      </div>
    </section>

{media_section(related, eyebrow="Articles", title=f"{label}におすすめの記事", more=False, keep_order=True)}

{media_cta(sv["category"])}"""
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": sv["name"], "provider": {"@type": "Organization", "name": "合同会社RIVIA&CO.", "url": SITE},
           "areaServed": "JP", "description": sv["lead"]},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sv["faq"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"},
              {"@type": "ListItem", "position": 2, "name": "アキヤドのプラン", "item": f"{SITE}/media/plans.html"},
              {"@type": "ListItem", "position": 3, "name": sv["name"]}]}]
    page(f"media/{sv['slug']}.html", f"{sv['name']}｜{sv['eyebrow']}｜アキヤド",
         f"{sv['lead']}相談・お見積りは無料、全国対応です。", body, current="media", jsonld=ld, mnav="plans", cv_category=sv["category"])


def media_company_page():
    """アキヤドの運営会社。誰が書いているか・何を頼めるかを1ページで伝える（会社概要はコーポレートと共通）"""
    rows = company_profile() + [("運営メディア", "アキヤド（空き家と民泊のメディア）"), ("運営している宿", "NODE Shimoda（静岡県下田市・一棟貸し）")]
    profile = "\n".join(f'          <div class="mprofile__row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    services = "\n".join(f"""          <a href="media/{sv['slug']}.html" class="mcomp-svc reveal">
            <span class="mcomp-svc__who">{e(sv['eyebrow'])}</span>
            <span class="mcomp-svc__name">{e(sv['name'])}</span>
            <span class="mcomp-svc__more">詳しく見る {ARROW}</span>
          </a>""" for sv in MEDIA_SERVICES)
    reviews = "\n".join(f"""            <figure class="mvoice reveal"><blockquote class="mvoice__text">{e(r["text"])}</blockquote>
              <figcaption class="mvoice__who"><span class="mvoice__plan">NODE Shimoda</span>{e(r["who"])}・{e(r["date"])}</figcaption></figure>""" for r in NODE_REVIEWS)
    band = f"""        <div class="msv-band reveal">
          <p class="msv-band__text">サービスの内容や条件の考え方は、資料にまとめています。<br class="pc-only">ご相談・資料のお届けは無料です。</p>
          <div class="msv-band__btns">
            {plan_doc_link("company")}
            <a href="contact.html?from=akiyado-company" class="mbtn" data-cta="media-company">無料で相談する {ARROW}</a>
          </div>
        </div>"""
    crumbs = media_crumbs([("アキヤド", "media.html"), ("運営会社", "")])
    body = f"""{media_hero("About us", "運営会社", "アキヤドは、宿泊施設の運営と空き家の再生を行う、合同会社RIVIA&CO.が運営しています。", crumbs)}

    <section class="section msec msec--first">
      <div class="container">
{band}
        <div class="msec__head reveal"><div><p class="msec__en">Company</p><h2 class="msec__title">会社概要</h2></div></div>
        <dl class="mprofile reveal">
{profile}
        </dl>
        <p class="mcta__plans"><a href="about.html">ミッション・ビジョン・バリューを見る {ARROW}</a></p>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Why we write</p><h2 class="msec__title">アキヤドを運営する理由</h2></div></div>
        <div class="mcomp-why reveal">
          <p>私たちは、自ら宿を運営する「当事者」です。空き家を宿として再生し、旅行者を迎え、地域のお店や人とつながる。その現場で確かめたことを、空き家に悩む方や、宿をはじめたい方に届けたいと考えています。</p>
          <p>記事は、公的な資料と、私たちの運営の経験をもとに書いています。読んで終わりではなく、具体的に考えたくなったときには、私たちが直接ご相談に乗ります。</p>
        </div>
        <aside class="supervisor mcomp-sup reveal">
          <figure class="supervisor__photo"><img src="images/{SUPERVISOR["photo"]}" alt="{e(SUPERVISOR["name"])}の写真" width="600" height="600" loading="lazy" decoding="async"></figure>
          <div>
            <p class="author__label">記事の監修</p>
            <p class="author__name">{e(SUPERVISOR["name"])}<span class="supervisor__role">{e(SUPERVISOR["role"])}</span></p>
            <p class="author__text">{e(SUPERVISOR["bio"])}</p>
          </div>
        </aside>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Services</p><h2 class="msec__title">アキヤドにご相談いただけること</h2></div></div>
        <div class="mcomp-svcs">
{services}
        </div>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Our inn</p><h2 class="msec__title">運営している宿：NODE Shimoda</h2></div></div>
        <p class="msv-record__label">ゲストの声（Airbnbのレビューより抜粋）</p>
        <div class="mvoices">
{reviews}
        </div>
{band}
      </div>
    </section>

{media_cta()}"""
    ld = [{"@context": "https://schema.org", "@type": "AboutPage", "name": "アキヤドの運営会社",
           "about": {"@type": "Organization", "name": "合同会社RIVIA&CO.", "url": SITE, "foundingDate": "2026-09-01"}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"},
              {"@type": "ListItem", "position": 2, "name": "運営会社"}]}]
    page("media/company.html", "運営会社｜空き家と民泊のメディア アキヤド",
         "アキヤドを運営する合同会社RIVIA&CO.の会社概要です。静岡県下田市で一棟貸しの宿を運営し、空き家の買取・借り上げ、民泊の開業・運営支援を行っています。",
         body, current="media", jsonld=ld)


def media_intro():
    """コーポレートTOPのメディア紹介。記事を並べるのではなく、アキヤドが何のメディアかを伝える"""
    entries = "".join(
        f'<li><a href="media/guide-{g["key"]}.html" class="mintro__entry"><span class="mintro__who">{e(g["label"])}方へ</span>'
        f'<span class="mintro__desc">{e(MEDIA_INTRO_DESC[g["key"]])}</span><span class="mintro__arrow">{ARROW}</span></a></li>'
        for g in MEDIA_GUIDES)
    return f"""    <section class="section mintro">
      <div class="container">
        <div class="mintro__grid">
          <div class="mintro__text">
            <span class="eyebrow reveal">Media</span>
            <h2 class="section-title section-title--logo reveal"><a href="media.html" class="tlogo" aria-label="アキヤド（空き家と民泊のメディア）">{AKIYADO_MARK}<span class="tlogo__ja" translate="no">アキヤド</span></a><span class="tlogo__sub">空き家と民泊のメディア</span></h2>
            <p class="mintro__copy reveal" data-delay="1">空き家を、売る。活かす。<br>民泊を、はじめる。</p>
            <p class="mintro__lead reveal" data-delay="1">アキヤドは、RIVIA&amp;CO.が運営する空き家と民泊のメディアです。自ら宿を運営する私たちが、相続した家をどうするか、宿として活かせるか、民泊をどう始めるかを、悩みが生まれる順にお答えしています。読んで具体的に考えたくなったら、アキヤドの買取・借り上げ・開業運営のプランでご相談いただけます。</p>
            <div class="mintro__btns reveal" data-delay="2">
              <a href="media.html" class="btn">アキヤドを見る {ARROW}</a>
              <a href="media/plans.html" class="btn btn--ghost">アキヤドのプラン</a>
            </div>
          </div>
          <figure class="mintro__photo reveal" data-delay="1">{photo("scene-stay", width=1080, height=1350, sizes="(max-width: 899px) 100vw, 480px")}</figure>
        </div>
        <ul class="mintro__entries reveal">{entries}</ul>
      </div>
    </section>"""


MEDIA_INTRO_DESC = {
    "sell": "相続した家を手放すときの流れ、税金の特例、放置したときのリスク",
    "use": "家を残したまま宿として活かす方法、貸す契約、改修の考え方",
    "side": "民泊の始め方、制度と届出、開業資金、集客と運営",
}


# ---------------------------------------------------------------- アキヤド：基礎から学ぶ（記事を、コースと章の順に並べて体系的に学べるようにする）
MEDIA_COURSES = [
    dict(key="akiya", en="Course 01", title="空き家の基礎知識", lead="相続した家や使っていない家を、どうするか決めるための基本です。",
         chapters=[("空き家を放置するとどうなるか", "税や管理の負担、法改正で高まる「放置」のリスクと、4つの選択肢。", ["akiya-inherited-house-to-inn"]),
                   ("売るときに知っておきたいこと", "相続した家を売るときの税の特例と、空き家バンクの使い方。", ["akiya-3000man-deduction", "akiya-bank-guide"]),
                   ("貸すときの契約", "普通借家・定期借家・借り上げの違いと、選び方。", ["akiya-lease-types"]),
                   ("宿として活かす", "観光地でなくても宿になる理由と、古い家を改修するときの考え方。", ["shizuoka-yaizu-akiya-inn", "kominka-renovation-points"]),
                   ("空き家と地域のこれから", "空き家の再生が、地域に人とお金の流れを生む仕組み。", ["akiya-regional-revitalization"])]),
    dict(key="minpaku", en="Course 02", title="民泊・小さな宿の基礎知識", lead="これから宿をはじめる方が、開業までに押さえたい制度とお金の基本です。",
         chapters=[("民泊新法と旅館業", "2つの制度の違いと、目的と物件に合った選び方。", ["minpaku-vs-ryokan-law"]),
                   ("開業までの流れ", "届出までの7ステップと、消防の手続き。", ["minpaku-start-steps", "minpaku-fire-safety"]),
                   ("物件の選び方", "新築と中古、それぞれの費用・工期・法令の違い。", ["new-build-vs-used-house-inn"]),
                   ("お金の準備", "開業資金の用意の仕方、補助金、利回りの見方。", ["inn-startup-funding", "small-inn-subsidies", "minpaku-investment-yield"]),
                   ("運営の任せ方", "住宅宿泊管理業者の役割と、管理会社の選び方。", ["minpaku-management-company"])]),
    dict(key="operate", en="Course 03", title="宿の運営", lead="開業したあと、宿の売上と評判を育てるための知識です。",
         chapters=[("売上を読み解く", "稼働率・客室単価・RevPARと、収益シミュレーションの考え方。", ["inn-kpi-basics", "airdna-revenue-simulation"]),
                   ("集客の考え方", "予約サイトと自社予約の使い分けと、選ばれる予約ページのつくり方。", ["ota-vs-direct-booking", "listing-photo-tips"]),
                   ("品質と評価", "清掃・リネンの仕組みと、レビューの評価を上げるゲスト対応。", ["cleaning-linen-operations", "guest-review-tips"]),
                   ("運営の事例", "一軒家を小さな宿にした、開業からの数字の推移。", ["case-rental-house-inn-first-year"])]),
    dict(key="region", en="Course 04", title="観光と地域を知る", lead="宿を取り巻く観光の動きと、地域との関わりを、データとともに読み解きます。",
         chapters=[("日本の観光市場", "訪日客の動向と、地方が抱える課題、地方分散のチャンス。", ["japan-tourism-market-data", "inbound-regional-dispersion"]),
                   ("旅のスタイルの変化", "「巡る旅」から「滞在する旅」へ。長期滞在が広がる理由。", ["long-stay-travel-demand"]),
                   ("宿と地域の経済", "旅行者のお金が地域に広がる仕組みと、関係人口。", ["inn-local-economy", "kankei-jinko-and-inns"]),
                   ("制度と担い手", "宿泊税の仕組みと、観光業の人手不足への向き合い方。", ["accommodation-tax", "tourism-labor-shortage"])]),
]


def media_learn_page():
    jump = "".join(f'<li><a href="#{c["key"]}" class="ttag">{e(c["title"])}</a></li>' for c in MEDIA_COURSES)
    courses = []
    for c in MEDIA_COURSES:
        chs = []
        for i, (t, d, slugs) in enumerate(c["chapters"], 1):
            links = "".join(f'<li data-date="{ARTICLE_BY_SLUG[sl]["date"]}"><a href="media/{sl}.html">{e(ARTICLE_BY_SLUG[sl]["title"])}</a></li>' for sl in slugs)
            chs.append(f"""            <li class="lchap reveal">
              <p class="lchap__no">第{i}章</p>
              <div class="lchap__body">
                <h3 class="lchap__title">{e(t)}</h3>
                <p class="lchap__text">{e(d)}</p>
                <ul class="lchap__list">{links}</ul>
              </div>
            </li>""")
        courses.append(f"""        <section class="lcourse" id="{c["key"]}" aria-labelledby="course-{c["key"]}">
          <div class="lcourse__head reveal">
            <p class="lcourse__en">{e(c["en"])}</p>
            <h2 class="lcourse__title" id="course-{c["key"]}">{e(c["title"])}</h2>
            <p class="lcourse__lead">{e(c["lead"])}</p>
          </div>
          <ol class="lchaps">
{chr(10).join(chs)}
          </ol>
        </section>""")
    crumbs = media_crumbs([("アキヤド", "media.html"), ("基礎から学ぶ", "")])
    body = f"""{media_hero("Learn", "空き家と民泊を、ゼロから体系的に学ぶ", "4つのコースに、記事を学ぶ順番で並べました。はじめての方は第1章から、気になるところからでも読めます。", crumbs, search_form("search.html"))}

    <section class="section msec msec--first">
      <div class="container">
        <nav class="ttags lcourse__jump reveal" aria-label="コース"><ul>{jump}</ul></nav>
{chr(10).join(courses[:2])}
        <div class="msv-band reveal">
          <p class="msv-band__text">読んで具体的に考えたくなったら、アキヤドにご相談ください。<br class="pc-only">ご相談・資料のお届けは無料です。</p>
          <div class="msv-band__btns">
            <a href="contact.html?from=akiyado-learn" class="mbtn" data-cta="media-learn">無料で相談する {ARROW}</a>
            {plan_doc_link("learn")}
          </div>
        </div>
{chr(10).join(courses[2:])}
      </div>
    </section>

{media_cta()}"""
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"},
        {"@type": "ListItem", "position": 2, "name": "基礎から学ぶ"}]}]
    page("media/learn.html", "空き家と民泊を、ゼロから体系的に学ぶ｜アキヤド",
         "空き家の基礎知識、民泊・小さな宿の基礎知識、宿の運営、観光と地域。アキヤドの記事を、4つのコースと章の順に並べました。はじめての方は第1章から読めます。",
         body, current="media", jsonld=ld, mnav="learn")


# ---------------------------------------------------------------- アキヤド：お問い合わせ（コーポレートとは別の、アキヤド専用のページ）
MEDIA_CONTACT_TOPICS = [
    ("sell", "アキヤド買取プラン（空き家を売りたい）",
     "【買取について】\n・売りたい物件：\n・空き家になった時期：\n・気になっていること（例：古くて売れるか不安）：\n"),
    ("use operation", "アキヤド借り上げプラン（空き家を活かしたい）",
     "【借り上げについて】\n・活かしたい物件：\n・家を残したい理由や、将来使う予定：\n・気になっていること（例：改修の費用）：\n"),
    ("side management", "アキヤド開業・運営プラン（民泊・小さな宿をはじめたい）",
     "【開業・運営について】\n・物件の有無（ある／探している）：\n・はじめたい宿のイメージ：\n・ご予算の目安：\n・自分で運営に関わりたい範囲：\n"),
    ("document", "サービス資料がほしい", "【資料について】\nサービス資料を希望します。\n"),
    ("other", "まだ決めていない・その他", "【ご相談】\n・いまの状況：\n・聞いてみたいこと：\n"),
]
MEDIA_CONTACT_SOURCES = ["検索（Google・Yahoo!など）", "AI（ChatGPTなど）", "SNS", "知人の紹介", "不動産会社・専門家の紹介", "その他"]


def media_contact_page():
    topics = "\n".join(
        f'              <label class="mform__check"><input type="checkbox" name="ご相談の内容" value="{e(t)}" data-keys="{k}" data-template="{e(tpl)}"><span>{e(t)}</span></label>'
        for k, t, tpl in MEDIA_CONTACT_TOPICS)
    def select(id_, name, label, options):
        opts = "".join(f'<option value="{e(o)}">{e(o)}</option>' for o in options)
        return f"""          <div class="mform__field">
            <label for="{id_}">{label} <span class="mform__opt">任意</span></label>
            <div class="select"><select id="{id_}" name="{name}"><option value="" selected>選択してください</option>{opts}</select></div>
          </div>"""
    prop = "\n".join([
        select("m-type", "物件の種類", "物件の種類", ["一戸建て", "古民家", "マンション・アパート", "土地", "まだ物件はない", "その他"]),
        select("m-state", "物件の状況", "物件の状況", ["空き家になっている", "住んでいる・使っている", "相続の手続き中", "購入を検討している", "その他"]),
        select("m-age", "築年数の目安", "築年数の目安", ["20年未満", "20〜40年", "40年以上", "わからない"]),
        select("m-when", "ご検討の時期", "ご検討の時期", ["すぐにでも", "3か月以内", "半年〜1年以内", "まだ決めていない"]),
    ])
    contact_ways = "".join(f'<label class="mform__radio"><input type="radio" name="ご希望の連絡方法" value="{w}"{" checked" if i == 0 else ""}><span>{w}</span></label>' for i, w in enumerate(["メール", "電話", "オンライン面談"]))
    sources = "".join(f'<option value="{e(x)}">{e(x)}</option>' for x in MEDIA_CONTACT_SOURCES)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("無料相談・お問い合わせ", "")])
    body = f"""{media_hero("Contact", "無料相談・お問い合わせ", "空き家の売却・活用、民泊の開業について、アキヤドが無料でご相談に乗ります。まだ決めていない段階でも大丈夫です。2営業日以内に、メールでご連絡します。", crumbs)}

    <section class="section msec msec--first">
      <div class="container mform-wrap">
        <ul class="mcta__points mform__points reveal"><li>相談・お見積りは無料</li><li>全国対応・オンライン可</li><li>しつこい営業はしません</li></ul>
        <form class="mform reveal" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" enctype="multipart/form-data" data-thanks="thanks.html">
          <input type="hidden" name="_subject" value="【アキヤド】無料相談・お問い合わせ">
          <input type="hidden" name="流入元" id="from-field" value="">
          <div class="mform__field">
            <label for="m-name">お名前 <span class="mform__req">必須</span></label>
            <input type="text" id="m-name" name="name" placeholder="山田 太郎" autocomplete="name" required>
          </div>
          <div class="mform__field">
            <label for="m-email">メールアドレス <span class="mform__req">必須</span></label>
            <input type="email" id="m-email" name="email" placeholder="your@email.com" autocomplete="email" required>
          </div>
          <div class="mform__field">
            <label for="m-tel">電話番号 <span class="mform__opt">任意</span></label>
            <input type="tel" id="m-tel" name="tel" placeholder="090-1234-5678" autocomplete="tel">
            <p class="mform__help">お電話でのご連絡を希望される場合のみご記入ください。</p>
          </div>
          <fieldset class="mform__field">
            <legend>ご相談の内容 <span class="mform__opt">複数選択可</span></legend>
            <div class="mform__checks">
{topics}
            </div>
          </fieldset>
          <fieldset class="mform__field">
            <legend>ご希望の連絡方法</legend>
            <div class="mform__radios">{contact_ways}</div>
          </fieldset>
          <p class="mform__group">物件について <span>わかる範囲で大丈夫です</span></p>
          <div class="mform__field">
            <label for="m-place">物件の所在地 <span class="mform__opt">任意</span></label>
            <input type="text" id="m-place" name="物件の所在地" placeholder="例：静岡県下田市（市区町村まででも大丈夫です）">
          </div>
{prop}
          <div class="mform__field">
            <label for="m-message">ご相談の詳細 <span class="mform__opt">任意</span></label>
            <textarea id="m-message" name="message" rows="5" placeholder="物件の状況や、気になっていることをご自由にお書きください。上の「ご相談の内容」を選ぶと、書き方の例が入ります。"></textarea>
          </div>
          <div class="mform__field">
            <label for="m-file">ファイル <span class="mform__opt">任意</span></label>
            <input type="file" id="m-file" name="attachment" multiple accept="image/*,.pdf,.doc,.docx,.xls,.xlsx">
            <p class="mform__help">物件の写真や図面があれば添付してください（合計10MBまで）。</p>
          </div>
          <div class="mform__field">
            <label for="m-source">アキヤドを知ったきっかけ <span class="mform__opt">任意</span></label>
            <div class="select"><select id="m-source" name="知ったきっかけ"><option value="" selected>選択してください</option>{sources}</select></div>
          </div>
          <label class="mform__agree"><input type="checkbox" name="プライバシーポリシーへの同意" value="同意する" required><span><a href="privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>に同意する <span class="mform__req">必須</span></span></label>
          <button type="submit" class="mbtn mform__submit">【無料】相談・お問い合わせをする {ARROW}</button>
          <p class="mform__note">ご提案まではすべて無料です。ご相談のあと、お断りいただいても構いません。</p>
        </form>
        <p class="mform__corp reveal">アキヤドは、合同会社RIVIA&amp;CO.が運営しています。不動産会社様との協業や、WEB集客・採用のご相談は<a href="CORP_CONTACT">RIVIA&amp;CO.のお問い合わせ</a>からお願いします。</p>
      </div>
    </section>"""
    page("media/contact.html", "無料相談・お問い合わせ｜空き家と民泊のメディア アキヤド",
         "アキヤドへの無料相談・お問い合わせ。空き家の買取・借り上げ、民泊の開業・運営について、相談・お見積りは無料です。全国対応・オンライン可。",
         body, current="media")


def media_thanks_page():
    body = f"""{media_hero("Thank you", "送信が完了しました", "お問い合わせいただき、ありがとうございます。内容を確認のうえ、2営業日以内にメールでご連絡します。")}

    <section class="section msec msec--first">
      <div class="container mform-wrap">
        <p class="mform__help">連絡が届かない場合は、迷惑メールフォルダもご確認ください。</p>
        <div class="msv-band__btns mthanks__btns">
          <a href="media.html" class="mbtn">アキヤドのトップへ {ARROW}</a>
          <a href="media/learn.html" class="mbtn mbtn--sub">基礎から学ぶ {ARROW}</a>
        </div>
      </div>
    </section>
    <script>
      if (typeof gtag === 'function') {{ gtag('event', 'generate_lead', {{ form_type: 'akiyado' }}); }}
    </script>"""
    page("media/thanks.html", "送信完了｜アキヤド", "アキヤドへのお問い合わせを受け付けました。", body, current="media", noindex=True)


def media_nav(current=""):
    """メディア内の共通ナビ。読者の状況（ガイド）を先に、テーマと検索を後に置く"""
    items = [("top", "media.html", "トップ")] + [(g["key"], f"media/guide-{g['key']}.html", g["label"]) for g in MEDIA_GUIDES] + \
            [("learn", "media/learn.html", "基礎から学ぶ"), ("themes", "media.html#themes", "テーマから探す"), ("search", "media/search.html", "記事をさがす"), ("plans", "media/plans.html", "アキヤドのプラン")]
    cur = ' aria-current="page"'
    lis = "".join(f'<li><a href="{href}"{cur if k == current else ""}>{e(n)}</a></li>' for k, href, n in items)
    # スマホでは、ヘッダーのボタンで開くメニューにする（相談・資料請求のボタンも入れる）
    return f"""    <nav class="mnav" id="mnav" aria-label="アキヤドのメニュー">
      <div class="container"><ul class="mnav__list">{lis}</ul>
        <div class="mnav__ctas">
          <a href="contact.html?from=akiyado-menu" class="mbtn" data-cta="media-menu">無料で相談する {ARROW}</a>
          <a href="contact.html?category=document&amp;from=akiyado-menu" class="mbtn mbtn--sub" data-cta="media-menu-doc">資料をもらう（無料） {ARROW}</a>
          <a href="index.html" class="mnav__corp">運営会社：合同会社RIVIA&amp;CO.</a>
        </div>
      </div>
    </nav>"""


SUPERVISOR = dict(
    name="石原 佑真", role="合同会社RIVIA&CO. 代表社員", photo="founder-ishihara.jpg",
    links=[("YOUTRUST", "https://youtrust.jp/users/yumayade__2210"), ("LinkedIn", "https://www.linkedin.com/in/%E4%BD%91%E7%9C%9F-%E7%9F%B3%E5%8E%9F-7a4bb929b"),
           ("Wantedly", "https://www.wantedly.com/id/tasuku_ishihara_g")],
    bio="株式会社リクルートの新規事業開発室で事業の立ち上げを経験し、その後ベンチャー企業で新規事業の創出と組織の拡大を牽引。RIVIA&CO.を共同創業し、空き家の再生と宿の運営・開業支援に携わる。",
)
# 初めての方が使いそうな言葉を先に並べる
MEDIA_SEARCH_WORDS = ["相続", "固定資産税", "売却", "貸す", "民泊", "開業資金", "補助金", "改修"]


def search_form(action, value=""):
    """記事検索のフォーム（結果は media/search.html に表示）"""
    return f"""
        <form class="msearch reveal" action="{action}" method="get" role="search">
          <label class="visually-hidden" for="msearch-q">記事をキーワードでさがす</label>
          <input class="msearch__input" id="msearch-q" type="search" name="q" value="{e(value)}" placeholder="キーワード（例：相続、補助金）" autocomplete="off">
          <button class="msearch__btn" type="submit">検索</button>
        </form>"""


def media_hero(en, title, lead, crumbs="", search=""):
    return f"""    <section class="mhero">
      <div class="container">{crumbs}
        <p class="mhero__en reveal">{e(en)}</p>
        <h1 class="mhero__title reveal" data-delay="1">{title}</h1>
        <p class="mhero__lead reveal" data-delay="2">{e(lead)}</p>{search}
      </div>
    </section>"""


def media_search_page():
    """記事検索。全記事の索引（js/media-index.js）をブラウザで絞り込む。公開日前の記事は出さない"""
    import re as _re
    idx = []
    for a in sorted(ARTICLES, key=lambda x: x["date"], reverse=True):
        key = " ".join([a["title"], a["description"], " ".join(a["keypoints"]),
                        " ".join(h for _, h, _ in a["sections"]), " ".join(q for q, _ in a["faq"]),
                        " ".join(MEDIA_CAT_NAMES[t] for t in a["topics"])])
        text = _re.sub(r"<[^>]+>", "", " ".join(h for _, _, h in a["sections"]) + " " + " ".join(ans for _, ans in a["faq"]))
        idx.append(dict(slug=a["slug"], title=a["title"], cat=MEDIA_CAT_NAMES[a["category"]], date=a["date"],
                        thumb=ARTICLE_PHOTOS[a["slug"]][0], desc=a["description"], short=a["short"],
                        key=_re.sub(r"\s+", " ", key), text=_re.sub(r"\s+", " ", text)))
    with open(os.path.join(OUT, "js", "media-index.js"), "w", encoding="utf-8") as f:
        f.write("// アキヤドの記事検索用の索引（build で自動生成。手で編集しない）\nwindow.MEDIA_INDEX = " + json.dumps(idx, ensure_ascii=False) + ";\n")
    chips = "".join(f'<li><a href="media/search.html?q={_quote(w)}">{e(w)}</a></li>' for w in MEDIA_SEARCH_WORDS)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("記事をさがす", "")])
    body = f"""{media_hero("Search", "記事をさがす", "キーワードで、アキヤドの記事をさがせます。", crumbs, search_form("search.html"))}

    <section class="section msec msec--first">
      <div class="container">
        <div class="msearch-words"><p class="msearch-words__label">キーワードの例</p><ul>{chips}</ul></div>
        <h2 class="visually-hidden">検索結果</h2>
        <p class="msearch-status" aria-live="polite"></p>
        <div class="media-grid" id="search-results"></div>
        <div class="msearch-empty" hidden>
          <p>ぴったりの記事が見つかりませんでした。別のキーワードで試すか、状況に合ったガイドから読んでみてください。具体的なご相談には、宿を運営する私たちが無料でお答えします。</p>
          <ul>{"".join(f'<li><a href="media/guide-{g["key"]}.html">{e(g["title"])} {ARROW}</a></li>' for g in MEDIA_GUIDES)}</ul>
        </div>
        <div class="msearch-weak" hidden>
          <h3 class="msearch-weak__title"></h3>
          <ul class="msearch-weak__list"></ul>
        </div>
      </div>
    </section>
    <script src="js/media-index.js"></script>

{media_cta()}"""
    page("media/search.html", "記事をさがす｜アキヤド", "アキヤドの記事をキーワードでさがせます。", body, current="media", noindex=True, mnav="search")


def media_crumbs(items):
    """パンくず（最後は現在のページ）"""
    parts = [f'<a href="{h}">{e(n)}</a>' if h else f'<span aria-current="page">{e(n)}</span>' for n, h in items]
    sep = '<span class="crumbs__sep">/</span>'
    return f'\n        <nav class="crumbs" aria-label="パンくずリスト">{sep.join(parts)}</nav>'


def guide_card(g, i):
    worries = "".join(f"<li>{e(w)}</li>" for w in g["worries"])
    return f"""          <a href="media/guide-{g["key"]}.html" class="persona-card reveal" data-delay="{i}">
            <div class="persona-card__photo">{photo(g["photo"], width=720, height=450, sizes="(max-width: 899px) 34vw, 400px")}</div>
            <div class="persona-card__body">
              <p class="persona-card__who">{e(g["who"])}</p>
              <h3 class="persona-card__title">{e(g["label"])}</h3>
              <ul class="persona-card__worries">{worries}</ul>
              <span class="persona-card__more">ガイドを見る {ARROW}</span>
            </div>
          </a>"""


def media_index_page():
    ordered = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in ordered)
    guides = "\n".join(guide_card(g, i) for i, g in enumerate(MEDIA_GUIDES))
    labels = {g["key"]: g["label"] for g in MEDIA_GUIDES}
    questions = "\n".join(f"""          <li data-date="{ARTICLE_BY_SLUG[slug]["date"]}"><a href="media/{slug}.html" class="mq__item">
            <span class="mq__who">{e(labels[k])}</span><span class="mq__q">{e(q)}</span><span class="mq__arrow">{ARROW}</span></a></li>""" for k, q, slug in MEDIA_QUESTIONS)
    entries = "".join(f'<li><a href="media/guide-{g["key"]}.html">{e(g["label"])} {ARROW}</a></li>' for g in MEDIA_GUIDES)
    tiles = "".join(
        f'<li><a href="media/guide-{g["key"]}.html" class="mtile"><span class="mtile__img">{photo(g["photo"], width=720, height=450, sizes="72px")}</span>'
        f'<span class="mtile__label">{e(g["label"])}</span><span class="mtile__arrow" aria-hidden="true">→</span></a></li>' for g in MEDIA_GUIDES)
    body = f"""    <section class="mfv">
      <div class="container mfv__inner">
        <div class="mfv__text">
          <p class="mfv__eyebrow reveal">空き家と民泊のメディア「アキヤド」</p>
          <h1 class="mfv__title reveal" data-delay="1">空き家を、売る。活かす。<br>民泊を、はじめる。</h1>
          <p class="mfv__lead reveal" data-delay="1">宿を運営する私たちが、悩みの順にお答えします。</p>
          <p class="mfv__entry-label reveal" data-delay="2">あなたの状況から読む</p>
          <ul class="mfv__tiles reveal" data-delay="2">{tiles}</ul>{search_form("media/search.html").replace('class="msearch reveal"', 'class="msearch msearch--fv reveal" data-delay="3"').replace('placeholder="キーワード（例：相続、補助金）"', 'placeholder="キーワードで記事をさがす"')}
        </div>
        <figure class="mfv__photo reveal" data-delay="1">{photo("scene-stay", width=1080, height=1350, sizes="(max-width: 899px) 100vw, 520px", lazy=False, priority=True, alt="縁側の向こうに山と町並みを望む和室")}</figure>
      </div>
    </section>

    <section class="section msec msec--first">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">For you</p><h2 class="msec__title">あなたの状況から読む</h2></div></div>
        <p class="msec__lead">いまの状況に近いものを選んでください。知っておきたいことを、悩みが生まれる順に並べたガイドをご用意しています。</p>
        <div class="persona-cards">
{guides}
        </div>
      </div>
    </section>

    <section class="section section--soft msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Questions</p><h2 class="msec__title">よくある悩みから探す</h2></div></div>
        <ul class="mq reveal">
{questions}
        </ul>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Learn</p><h2 class="msec__title">ゼロから体系的に学ぶ</h2></div><a href="media/learn.html" class="msec__more">コースの一覧へ {ARROW}</a></div>
        <ul class="lcards">{"".join(f'<li class="reveal"><a href="media/learn.html#{c["key"]}" class="lcard"><span class="lcard__en">{e(c["en"])}</span><span class="lcard__title">{e(c["title"])}</span><span class="lcard__text">{e(c["lead"])}</span><span class="lcard__count">全{len(c["chapters"])}章</span></a></li>' for c in MEDIA_COURSES)}</ul>
      </div>
    </section>

    <section class="section msec mplanband">
      <div class="container">
        <div class="mplanband__box reveal">
          <div class="mplanband__text">
            <p class="msec__en">Plans</p>
            <h2 class="msec__title">アキヤドに任せると、どうなる？</h2>
            <p class="mplanband__lead">記事を運営する私たちは、実際に宿を運営しています。売る・貸す・宿をはじめる、それぞれのプランと条件の目安をまとめました。</p>
          </div>
          <ul class="mplanband__list">{"".join(f'<li><a href="media/{MEDIA_SERVICE_BY_KEY[k]["slug"]}.html"><span class="mplanband__who">{e(l)}</span><span class="mplanband__names">{e(MEDIA_SERVICE_BY_KEY[k]["name"])}{"" if names == [MEDIA_SERVICE_BY_KEY[k]["name"]] else "（" + "・".join(e(n) for n in names) + "）"}</span><span class="mplanband__arrow">→</span></a></li>' for k, l, _, _, names in MEDIA_PLAN_GROUPS)}</ul>
        </div>
      </div>
    </section>

    <section class="section msec">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Latest</p><h2 class="msec__title">新着記事</h2></div></div>
        <div class="media-grid media-grid--feature" data-limit="4">
{cards}
        </div>
      </div>
    </section>

    <section class="section msec" id="all">
      <div class="container">
        <div class="msec__head reveal"><div><p class="msec__en">Archive</p><h2 class="msec__title">すべての記事</h2></div></div>
        <div id="themes" class="ttags-wrap reveal"><p class="ttags__label">テーマから探す</p>{theme_tags("all")}</div>
        <div class="media-grid" id="media-list" data-page-size="9">
{cards}
        </div>
        <div class="media-more"><button type="button" class="btn btn--ghost media-more__btn" hidden>もっと記事を見てみる ＋</button></div>
      </div>
    </section>

{media_cta()}"""
    ld = [{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "アキヤド",
        "alternateName": "空き家と民泊のメディア アキヤド",
        "url": f"{SITE}/media.html",
        "inLanguage": "ja",
        "publisher": {"@type": "Organization", "name": "合同会社RIVIA&CO.", "url": f"{SITE}/", "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo/logo.png"}},
    }, {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "アキヤド",
        "url": f"{SITE}/media.html",
        "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/media/{a['slug']}.html"} for a in ordered],
    }]
    page("media.html", "アキヤド｜空き家の売却・活用と、副業ではじめる民泊のメディア", "空き家を売りたい方、活かしたい方、副業で民泊や小さな宿をはじめたい方に向けて、宿を運営する合同会社RIVIA&CO.が悩みに沿って解説するメディアです。", body, current="media", jsonld=ld, mnav="top")


def theme_tags(current=None, all_href="media.html#all"):
    def tag(href, label, on):
        return f'<li><a href="{href}" class="ttag is-current" aria-current="page">{label}</a></li>' if on else f'<li><a href="{href}" class="ttag">{label}</a></li>'
    items = [tag(all_href, "すべて", current == "all")] + [tag(f"media/category-{k}.html", e(n), current == k) for k, n in MEDIA_CATEGORIES]
    return f'<nav class="ttags" aria-label="テーマから探す"><ul>{"".join(items)}</ul></nav>'


def media_category_page(k, n):
    ordered = sorted((a for a in ARTICLES if k in a["topics"]), key=lambda a: a["date"], reverse=True)
    cards = "\n".join(article_card(a) for a in ordered)
    g = next((x for x in MEDIA_GUIDES if x["key"] == MEDIA_GUIDE_FOR_CAT.get(k)), None)
    guide_html = f"""
        <a href="media/guide-{g["key"]}.html" class="guide-link reveal">
          <span class="guide-link__label">はじめての方は、ガイドから</span>
          <span class="guide-link__title">{e(g["title"])} {ARROW}</span>
        </a>""" if g else ""
    crumbs = media_crumbs([("アキヤド", "media.html"), (n, "")])
    body = f"""{media_hero(MEDIA_CAT_INFO[k][0], e(n), MEDIA_CAT_INFO[k][1], crumbs, search_form("search.html"))}

    <section class="section msec msec--first">
      <div class="container">
        {theme_tags(k)}{guide_html}
        <h2 class="visually-hidden">{e(n)}の記事</h2>
        <div class="media-grid" id="media-list" data-page-size="12">
{cards}
        </div>
        <p class="media-empty" hidden>このカテゴリの記事は準備中です。</p>
        <div class="media-more"><button type="button" class="btn btn--ghost media-more__btn" hidden>もっと記事を見てみる ＋</button></div>
      </div>
    </section>

{media_cta()}"""
    ld = [{
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TOP", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "アキヤド", "item": f"{SITE}/media.html"},
            {"@type": "ListItem", "position": 3, "name": n},
        ]}]
    page(f"media/category-{k}.html", f"{n}の記事一覧｜空き家と民泊のメディア アキヤド", MEDIA_CAT_INFO[k][1], body, current="media", jsonld=ld, mnav="themes")


def media_guide_page(g):
    stages, no = [], 0
    for si, (label, desc, slugs) in enumerate(g["stages"], 1):
        items = []
        for slug in slugs:
            no += 1
            a = ARTICLE_BY_SLUG[slug]
            pn = ARTICLE_PHOTOS[slug][0]
            items.append(f"""            <li class="guide-step reveal" data-date="{a["date"]}">
              <a href="media/{slug}.html" class="guide-step__body">
                <span class="guide-step__no">{no:02d}</span>
                <span class="guide-step__thumb">{photo(pn, width=720, height=450, sizes="(max-width: 899px) 30vw, 220px")}</span>
                <span class="guide-step__text">
                  <span class="guide-step__cat">{e(MEDIA_CAT_NAMES[a["category"]])}<span class="guide-step__min">約{read_minutes(a)}分で読める</span></span>
                  <span class="guide-step__title">{e(a["title"])}</span>
                  <span class="guide-step__more">記事を読む {ARROW}</span>
                </span>
              </a>
            </li>""")
        stages.append(f"""        <section class="guide-stage">
          <div class="guide-stage__head reveal"><span class="guide-stage__no">Step {si}</span><h2 class="guide-stage__title">{e(label)}</h2><p class="guide-stage__desc">{e(desc)}</p></div>
          <ol class="guide-steps">
{chr(10).join(items)}
          </ol>
        </section>""")
    crumbs = media_crumbs([("アキヤド", "media.html"), (g["title"], "")])
    worries = "".join(f"<li>{e(w)}</li>" for w in g["worries"])
    body = f"""{media_hero("Guide", e(g["title"]), g["lead"], crumbs)}

    <section class="section msec msec--first">
      <div class="container container--article">
        <div class="guide-worries reveal"><p class="guide-worries__label">こんな悩みに答えます</p><ul>{worries}</ul></div>
{chr(10).join(stages)}
      </div>
    </section>

{media_cta(g["service"])}"""
    ld = [{
        "@context": "https://schema.org", "@type": "ItemList", "name": g["title"],
        "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{SITE}/media/{s_}.html"} for i, s_ in enumerate(g["slugs"], 1)],
    }]
    page(f"media/guide-{g['key']}.html", f"{g['title']}｜アキヤド", g["lead"], body, current="media", jsonld=ld, mnav=g["key"])


def article_page(a):
    names = dict(SERVICES)
    toc = "".join(f'<li><a href="#{sid}">{e(h)}</a></li>' for sid, h, _ in a["sections"])
    keypoints = "".join(f"<li>{e(k)}</li>" for k in a["keypoints"])
    def tables(html):
        html = html.replace('<table class="table">', '<div class="table-scroll"><table class="table">').replace("</table>", "</table></div>")
        return re.sub(r"<td>((?:約|―|—)?[0-9０-９.,]+(?:%|倍|か月)?(?:（[^<]{0,12}）)?)</td>", r'<td class="num">\1</td>', html)
    sections = "\n".join(
        f"""        <section class="article__section" id="{sid}">
          <h2>{e(h)}</h2>
{html.strip()}
        </section>"""
        for sid, h, html in [(x, y, insert_figure(a["slug"], x, tables(z))) for x, y, z in a["sections"]]
    )
    sources = "".join(f"<li>{e(s)}</li>" for s in a["sources"])
    svc = a["services"][0]
    svc_links = "".join(
        f'<li><a href="service-{k}.html">{e(names[k])} {ARROW}</a></li>' for k in a["services"]
    )
    # 同じカテゴリ・同じ関連サービスの記事を優先
    related = sorted(
        (x for x in ARTICLES if x["slug"] != a["slug"]),
        key=lambda x: (x["category"] != a["category"], not set(x["services"]) & set(a["services"])),
    )
    from urllib.parse import quote
    share_url = quote(f"{SITE}/media/{a['slug']}.html", safe="")
    share_text = quote(f"{a['title']}｜アキヤド", safe="")
    for_links = "".join(f'<li><a href="media/guide-{x["key"]}.html">{e(x["title"])}</a></li>' for x in guides_of(a["slug"]))
    for_html = f'<div class="article__for"><span>こんな方に</span><ul>{for_links}</ul></div>' if for_links else ""
    g = guide_of(a["slug"])
    guide_box = ""
    if g:
        idx = g["slugs"].index(a["slug"])
        lis = "".join(
            (f'<li data-date="{ARTICLE_BY_SLUG[s_]["date"]}" aria-current="page"><span>{e(ARTICLE_BY_SLUG[s_]["title"])}</span></li>' if s_ == a["slug"] else
             f'<li data-date="{ARTICLE_BY_SLUG[s_]["date"]}"><a href="media/{s_}.html">{e(ARTICLE_BY_SLUG[s_]["title"])}</a></li>')
            for s_ in g["slugs"])
        guide_box = f"""
        <nav class="guide-box" aria-label="この記事を含むガイド">
          <p class="guide-box__label">この記事を含むガイド</p>
          <a href="media/guide-{g["key"]}.html" class="guide-box__title">{e(g["title"])}</a>
          <ol class="guide-box__list">{lis}</ol>
          <div class="guide-box__pager"></div>
        </nav>
"""
    body = f"""    <article class="article" data-publish="{a["date"]}">
      <header class="article__header">
        <div class="container container--article">
          {media_crumbs([("アキヤド", "media.html"), (MEDIA_CAT_NAMES[a["category"]], f"media/category-{a['category']}.html")]).strip()}
          <div class="article__cats">{"".join(f'<a href="media/category-{t}.html" class="tag article__cat">{e(MEDIA_CAT_NAMES[t])}</a>' for t in a["topics"])}</div>
          <h1 class="article__title">{e(a["title"])}</h1>
          <p class="article__meta">
            <span>公開日 <time datetime="{a["date"]}">{fmt_date(a["date"])}</time></span>
            <span>更新日 <time datetime="{a["updated"]}">{fmt_date(a["updated"])}</time></span>
            <span>読了目安 約{read_minutes(a)}分</span>
            <span>執筆：アキヤド編集部</span>
            <span>監修：{e(SUPERVISOR["name"])}</span>
          </p>
          {for_html}
          {thumb(a, "hero")}
        </div>
      </header>

      <div class="container container--article article__body">
        <p class="article__lead">{e(a["description"])}</p>

        <section class="keypoints" aria-labelledby="keypoints-title">
          <h2 id="keypoints-title" class="keypoints__title">この記事のポイント</h2>
          <ul>{keypoints}</ul>
        </section>

        <aside class="inline-cta">
          <p class="inline-cta__text">{e(CV_MESSAGES.get(g["key"] if g else "", CV_MESSAGES[""]))}</p>
          <div class="inline-cta__actions">
            <a href="contact.html?category={a["services"][0]}&amp;from=akiyado" class="btn mbtn" data-cta="media-inline">無料で相談する {ARROW}</a>
            <a href="media/{MEDIA_SERVICE_BY_KEY[g["key"] if g else "use"]["slug"]}.html" class="inline-cta__plan">サービスとプランを見る {ARROW}</a>
          </div>
        </aside>

        <nav class="toc" aria-label="目次">
          <p class="toc__title">目次</p>
          <ol>{toc}<li><a href="#faq">よくある質問</a></li></ol>
        </nav>

{sections}

        <section class="article__section" id="faq">
          <h2>よくある質問</h2>
          <div class="faq">
{faq_html(a["faq"])}
          </div>
        </section>

        <section class="sources">
          <h2 class="sources__title">参考資料</h2>
          <ul>{sources}</ul>
          <p class="sources__note">※ 本記事の数値・制度は公開日時点で公表されている資料にもとづきます。最新の情報は各機関の発表をご確認ください。</p>
        </section>

{guide_box}
        <div class="share">
          <p class="share__label">この記事をシェアする</p>
          <ul class="share__list">
            <li><a href="https://twitter.com/intent/tweet?url={share_url}&amp;text={share_text}" target="_blank" rel="noopener">X</a></li>
            <li><a href="https://social-plugins.line.me/lineit/share?url={share_url}" target="_blank" rel="noopener">LINE</a></li>
            <li><a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" rel="noopener">Facebook</a></li>
            <li><button type="button" class="share__copy" data-url="{SITE}/media/{a["slug"]}.html">リンクをコピー</button></li>
          </ul>
        </div>

        <aside class="author">
          <p class="author__label">この記事を書いた人</p>
          <p class="author__name">アキヤド編集部</p>
          <p class="author__text">合同会社RIVIA&amp;CO.のメディア編集部。空き家の再生から宿泊施設の運営・開業支援、WEB集客・採用支援まで、自ら宿を運営する当事者の視点で、地域の価値を活かすための情報をお届けします。</p>
        </aside>

        <aside class="supervisor">
          <figure class="supervisor__photo"><img src="images/{SUPERVISOR["photo"]}" alt="{e(SUPERVISOR["name"])}の写真" width="600" height="600" loading="lazy" decoding="async"></figure>
          <div>
            <p class="author__label">この記事の監修者</p>
            <p class="author__name">{e(SUPERVISOR["name"])}<span class="supervisor__role">{e(SUPERVISOR["role"])}</span></p>
            <p class="author__text">{e(SUPERVISOR["bio"])}</p>
            <div class="supervisor__links">
              <a href="about.html#founders" class="supervisor__more">プロフィールを見る {ARROW}</a>
              <ul>{"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SUPERVISOR["links"])}</ul>
            </div>
          </div>
        </aside>

        <aside class="article-cta">
          <p class="article-cta__title">この記事に関連するサービス</p>
          <ul class="article-cta__links">{svc_links}</ul>
          <a href="contact.html?category={svc}" class="btn btn--lg">無料で相談する {ARROW}</a>
        </aside>
      </div>
    </article>

{media_section(related, eyebrow="Related", title="あわせて読みたい記事", more=False, keep_order=True)}"""

    ld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": a["title"],
            "description": a["description"],
            "datePublished": a["date"],
            "dateModified": a["updated"],
            "image": f"{SITE}/images/ogp.jpg",
            "mainEntityOfPage": f"{SITE}/media/{a['slug']}.html",
            "author": {"@type": "Organization", "name": "アキヤド編集部（合同会社RIVIA&CO.）", "url": f"{SITE}/about.html"},
            "contributor": {"@type": "Person", "name": SUPERVISOR["name"], "jobTitle": "合同会社RIVIA&CO. 代表社員（監修）", "url": f"{SITE}/about.html#founders", "sameAs": [u for _, u in SUPERVISOR["links"]]},
            "publisher": {"@type": "Organization", "name": "合同会社RIVIA&CO.", "logo": {"@type": "ImageObject", "url": f"{SITE}/images/logo/logo.png"}},
            "articleSection": MEDIA_CAT_NAMES[a["category"]],
            "inLanguage": "ja",
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "TOP", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "アキヤド", "item": f"{SITE}/media.html"},
                {"@type": "ListItem", "position": 3, "name": MEDIA_CAT_NAMES[a["category"]], "item": f"{SITE}/media/category-{a['category']}.html"},
                {"@type": "ListItem", "position": 4, "name": a["title"]},
            ],
        },
    ]
    page(f"media/{a['slug']}.html", a["title"], a["description"], body, current="media", jsonld=ld, cv_category=a["services"][0],
         og_type="article", og_image=f"images/photos/{ARTICLE_PHOTOS[a['slug']][0]}.jpg")


def not_found_page():
    """存在しないURLを開いたときのページ（Vercel はサイト直下の 404.html を使う）。
    どの階層のURLでも表示できるよう、リンクはすべて / から始まる絶対パスにする"""
    import re as _re
    body = f"""    <section class="page-hero">
      <div class="container">
        <p class="page-hero__en">404</p>
        <h1 class="page-hero__ja">お探しのページが見つかりませんでした</h1>
        <p class="page-hero__lead">URLが変わったか、ページが削除された可能性があります。トップページや記事一覧からお探しください。</p>
        <div class="hero__actions" style="margin-top:40px">
          <a href="index.html" class="btn">トップページへ {ARROW}</a>
          <a href="media.html" class="btn btn--ghost">アキヤド（記事一覧）へ</a>
        </div>
      </div>
    </section>"""
    page("404.html", "ページが見つかりません", "お探しのページが見つかりませんでした。", body, noindex=True)
    src = os.path.join(OUT, PAGES_DIR, "404.html")
    html = open(src, encoding="utf-8").read()
    def absolute(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http:", "https:", "#", "data:", "mailto:", "tel:", "/")):
            return m.group(0)
        url = _re.sub(r"^(\.\./)+", "", url)
        return f'{attr}="/{"" if url == "index.html" else url}"'
    html = _re.sub(r'\b(href|src)="([^"]*)"', absolute, html)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    os.remove(src)


def llms_txt():
    """AI（LLM）向けにサイトとメディアの概要をまとめた llms.txt（https://llmstxt.org/ の形式）"""
    lines = ["# 合同会社RIVIA&CO.", "",
             "> 空き家の再生、民泊・小さな宿の開業と運営、WEB集客・採用を支援する会社です。運営メディア「アキヤド（空き家と民泊のメディア）」では、空き家を売りたい方・活かしたい方・副業で民泊をはじめたい方に向けて、悩みの順に記事を公開しています。",
             "", "## 会社", f"- [会社概要]({SITE}/about.html): ミッション・ビジョン・バリューと創業者",
             f"- [お問い合わせ]({SITE}/contact.html): 無料相談の窓口", "", "## サービス"]
    lines += [f"- [{n}]({SITE}/service-{k}.html)" for k, n in SERVICES]
    lines += ["", "## アキヤド（ガイド）"]
    lines += [f"- [{g['title']}]({SITE}/media/guide-{g['key']}.html): {g['lead']}" for g in MEDIA_GUIDES]
    lines += ["", "## アキヤド（記事）"]
    lines += [f"- [{a['title']}]({SITE}/media/{a['slug']}.html): {a['description']}"
              for a in sorted(ARTICLES, key=lambda x: x["date"]) if a["date"] <= BUILD_DATE]
    with open(os.path.join(OUT, SEO_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def sitemap():
    pages = ["", "about.html"] + [f"service-{k}.html" for k, _ in SERVICES] + \
            ["media.html"] + [f"media/category-{k}.html" for k, _ in MEDIA_CATEGORIES] + [f"media/guide-{g['key']}.html" for g in MEDIA_GUIDES] + ["media/plans.html"] + [f"media/{sv['slug']}.html" for sv in MEDIA_SERVICES] + ["media/company.html", "media/learn.html", "media/contact.html"] + [f"media/{a['slug']}.html" for a in ARTICLES] + ["careers.html", "contact.html", "privacy.html"]
    pages += ["en/" + ("" if f == "index.html" else f) for f in EN_PAGES if f != "thanks.html"]
    lastmod = {f"media/{a['slug']}.html": a["updated"] for a in ARTICLES}
    urls = "\n".join(
        f"  <url><loc>{SITE}/{p}</loc>" + (f"<lastmod>{lastmod[p]}</lastmod>" if p in lastmod else "") + "</url>"
        for p in pages
    )
    os.makedirs(os.path.join(OUT, SEO_DIR), exist_ok=True)
    with open(os.path.join(OUT, SEO_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")
    with open(os.path.join(OUT, SEO_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

if __name__ == "__main__":
    index_page()
    about_page()
    for k, n in SERVICES:
        service_page(k, n)
    careers_page()
    contact_page()
    privacy_page()
    thanks_page()
    media_index_page()
    media_plans_page()
    for sv in MEDIA_SERVICES:
        media_service_page(sv)
    media_company_page()
    media_learn_page()
    media_contact_page()
    media_thanks_page()
    for k, n in MEDIA_CATEGORIES:
        media_category_page(k, n)
    for g in MEDIA_GUIDES:
        media_guide_page(g)
    media_search_page()
    not_found_page()
    for a in ARTICLES:
        article_page(a)
    sitemap()
    llms_txt()
    # 英語版（コーポレートページのみ）
    import subprocess
    subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n", "build_en.py")], check=True)
    spec_md()
    print("done")
