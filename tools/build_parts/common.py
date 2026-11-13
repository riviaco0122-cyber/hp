# -*- coding: utf-8 -*-
# build.py の一部：文字組み（強調のマーカー・見出しの改行位置）と、出力先・日付・計測 ID・サービス一覧・ナビの項目などの設定。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。


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


# 改行の方針（人の方針 2026-11-13）：本文・見出し・カードは、全部ふつうに右まで詰めて折り返す（文節や1文ごとの改行はしない）。
# 途中で切らないのは、数字と単位（「約3,188万人」「2027年3月31日」）、ハイフンでつないだ英単語（「Wi-Fi」）、会社名（「合同会社RIVIA&CO.」）だけ。
# 最後の行が2〜3文字になることは許す。並んだ項目で続けて起きるときだけ、js/main.js が直す（docs/design-guide.md 3章）
_NUM_TOKEN = re.compile(r"(?<![&#\dA-Za-z])(?:約)?\d[\d,.]*(?:(?:万|億|兆)?(?:人泊|営業日|時間|か月|円|人|泊|年|月|日|倍|件|戸|棟|回|歳|㎡|室|%|％)(?:\d+(?:か月|月|日))*|[^\s\d,.、。・（）()「」<&;])?")  # 文字参照（&#39;）の中は触らない。単位がなければ直後の1文字（「2つ」）まで
_BRAND = r"(?:合同会社)?RIVIA&amp;CO\."
_KEEP = re.compile(_BRAND + r"|(?<![A-Za-z-])[A-Za-z]+(?:-[A-Za-z]+)+|" + _NUM_TOKEN.pattern)


def lines_html(text):
    """リード・コンセプトの文。文字列で渡したときは、ふつうの文として右まで詰めて流す（「|」は書いてあっても無視する）。
    リストで渡したときだけ、要素ごとに行を変え、要素の中は「|」の位置でだけ折る（TOP_CONCEPT のように、行の区切りを手で決めたコピー。.ml-s）"""
    if isinstance(text, list):  # 1要素＝1行。要素の中は「|」の位置でだけ折る（入る限り前の行に詰める。トップのコンセプト文＝人のお手本 2026-11-07）
        return "".join('<span class="ml-s">' + "".join(f"<span>{e(x)}</span>" for x in item.split("|") if x) + "</span>" for item in text)
    return e(text.replace("|", ""))


def phrase_breaks(html):
    """数字と単位・英単語・会社名を、途中で改行しないまとまり（<n-b>）にする。ほかはブラウザに任せて、右まで詰めて折り返す。
    文字の部分だけに効かせる（タグの属性・script・style などは触らない）"""
    head, sep, body = html.partition("<body")
    segs, skip = re.split(r"(<[^>]+>)", body), 0
    for k, sg in enumerate(segs):
        if sg.startswith("<"):
            m = re.match(r"<(/?)(script|style|textarea|select|option|title|svg)\b", sg, re.I)
            if m:
                skip += -1 if m.group(1) else 1
        elif k and not skip:  # k=0 は <body の残り（属性）
            t = _KEEP.sub(lambda m: f"<n-b>{m.group(0)}</n-b>" if len(m.group(0)) >= 2 else m.group(0), sg)
            # まとまりを入れた文は、全体を1つのインライン要素（n-w。見た目は何もしない）で包む。横並び（flex・grid）の親の中で、
            # 文字とまとまりが別々の部品として並んでしまうのを防ぐ（折りたたみの見出し summary がはみ出した。人の方針 2026-11-13 の作り直しで）
            segs[k] = f"<n-w>{t}</n-w>" if t != sg else sg
    return head + sep + "".join(segs)


OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # リポジトリの直下（tools/ の1つ上）
import datetime as _dt
BUILD_DATE = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=9))).date().isoformat()  # 日本時間の今日。llms.txt には公開済みの記事だけを載せる
SITE = "https://rivia-co.com"  # 公開ドメイン
CLARITY_ID = "yrrji51n1y"  # Microsoft Clarity のプロジェクトID
GA_ID = "G-RZVE2XBPQ2"  # Google アナリティクス 4 の測定ID

SERVICES = [
    ("operation", "空き家再生事業"),
    ("management", "開業・運営支援事業"),
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
    ("個人のお客様", [("operation", "空き家を活かしたい・売りたい"), ("management", "民泊を始めたい・任せたい")]),
    ("法人のお客様", [("management", "民泊を始めたい・任せたい"), ("partnership", "物件を民泊用に売りたい"),
                     ("marketing", "集客を伸ばしたい"), ("recruit", "人材を採用したい")]),
]

# 同じサービスでも、お客様の立場によってメニューに出す「お悩み」を変える
NAV_WORRY = {
    ("personal", "management"): "副業や投資目的で、小規模宿の運営を検討中",
    ("business", "management"): "新規事業で、小規模宿に挑戦したい",
}
