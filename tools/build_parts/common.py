# -*- coding: utf-8 -*-
# build.py の一部：文字組み（強調のマーカー・見出しの改行位置）と、出力先・日付・計測 ID・サービス一覧・ナビの項目などの設定。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。


_JA = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


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


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import budoux  # 同梱（tools/vendor/budoux）。見出しを単語の途中で改行しないための文節区切り
_budoux = budoux.load_default_japanese_parser()
_VOID = {"br", "wbr", "img", "input", "meta", "link", "hr", "source", "col", "area", "base", "embed", "track"}
# 見出しとして扱う要素：h1〜h6 と、クラス名が「〜__title」「〜__name」「〜__head」「〜heading」などの要素（カードや図の見出し）
_HEADING_CLASS = re.compile(r'class="[^"]*(?:__title|__name|__head\b|heading|-title|__q)\b')
# カードの説明文などの短い文（60字以内）も、見出しと同じく文節の切れ目でだけ改行する（人の指摘 2026-11-06：事業紹介のカード）
_CARD_CLASS = re.compile(r'class="[^"]*__(?:text|desc|sub|blurb|lead)\b')
_CARD_MAX = 60


def _heading_phrases(text):
    """見出しの文字を文節に分け、文節の切れ目にだけ改行候補（<wbr>）を入れる。最後の文節が2文字以下なら、前の文節とつなげる"""
    ph = _budoux.parse(text)
    merged = []
    for x in ph:  # 開きかっこ（「（」など）で終わる文節は、次の文節とつなげる（かっこの直後で改行しない）
        if merged and merged[-1][-1:] in "（(「『【〈《":
            merged[-1] += x
        else:
            merged.append(x)
    ph = merged
    if len(ph) > 1 and len(ph[-1].strip()) <= 2:
        ph[-2:] = [ph[-2] + ph[-1]]
    return "<wbr>".join(e(x, quote=False) for x in ph)


# 数字のまとまり：前の「約」から、単位（「万人」「兆円」「年3月31日」など）まで。単位がないときは直後の1文字（「2つ」）まで
_NUM_TOKEN = re.compile(r"(?:約)?\d[\d,.]*(?:(?:万|億|兆)?(?:人泊|時間|か月|円|人|泊|年|月|日|倍|件|戸|棟|回|歳|㎡|室|%|％)(?:\d+(?:か月|月|日))*|[^\s\d,.、。・（）()「」])")


# 本文の長い段落で使う、短いまとまり：数字と直後の1文字だけ（「5万」「2つ」）。まとまりを長くすると、行末で丸ごと次の行へ送られ、右側が大きく空くため
_NUM_SHORT = re.compile(r"\d[\d,.]*[^\s\d,.、。・（）()「」]")


def _keep_numbers(text, whole=False):
    """数字の途中や、数字と単位の間で改行しない。エスケープ済みの文字列を返す。
    whole=True（表のマス・ラベルなど20文字以下の短い文言）：「約3,188万人」「2027年3月31日」を丸ごとまとめる（「約3,18／8万人」を防ぐ）。
    whole=False（本文の長い段落）：数字と直後の1文字だけをまとめる（「5／万円」は防ぎ、右端のガタつきは増やさない）"""
    out, last = [], 0
    for m in (_NUM_TOKEN if whole else _NUM_SHORT).finditer(text):
        out += [e(text[last:m.start()], quote=False), f"<n-b>{e(m.group(0), quote=False)}</n-b>"]
        last = m.end()
    return "".join(out) + e(text[last:], quote=False)


def _phrase_html(text):
    """短い文（100文字以下）の文字を、言葉の切れ目に改行候補（<wbr>）を入れた HTML にする。数字のまとまりは1つの塊（<n-b>）のまま。
    左揃えでは行末まで詰めて折り返すので見た目は変わらず、中央揃えで表示される文だけ js/main.js が n-w.c にして切れ目でだけ改行させる"""
    out, last = [], 0
    for m in _NUM_TOKEN.finditer(text):
        if text[last:m.start()]:
            out += [e(x, quote=False) for x in _budoux.parse(text[last:m.start()])]
        out.append(f"<n-b>{e(m.group(0), quote=False)}</n-b>")
        last = m.end()
    if text[last:]:
        out += [e(x, quote=False) for x in _budoux.parse(text[last:])]
    return "<wbr>".join(out)


def phrase_breaks(html):
    """日本語の改行（人の方針 2026-11-05・11-06）。
    - 本文：ふつうに行末まで詰めて折り返す（両端揃え・字間の調整はしない）。段落・ラベルの最後（と <br> の手前）の3文字だけは
      ひとまとまり（<n-b>、改行しない）にして、最後の行に1〜2文字だけがはみ出して残らないようにする。
      数字と直後の単位（「2つ」「5万円」）の間でも改行しない。
    - 見出し：単語の途中で切れないよう、文節の切れ目（<wbr>）でだけ改行する（<n-w class="h">、word-break: keep-all）。"""
    head, sep, body = html.partition("<body")
    parts = re.split(r"(<[^>]+>)", body)
    skip = 0
    stack = []  # (タグ名, 見出しの中か)
    row_first = False  # <tr> が開いて、まだ最初のマス（<td>・<th>）が来ていない
    block_end = re.compile(r"</(p|li|dd|dt|blockquote|figcaption|h[1-6]|th|td|span|a|button|label|summary)>")
    inline_end = re.compile(r"</(strong|em|b|a|span|small)>")
    for i, p in enumerate(parts):
        if p.startswith("<"):
            m = re.match(r"<(/?)(script|style|textarea|select|option|title|svg)\b", p, re.I)
            if m:
                skip += -1 if m.group(1) else 1
            t = re.match(r"<(/?)([a-zA-Z][\w-]*)", p)
            if t and not p.startswith("<!"):
                name = t.group(2).lower()
                if t.group(1):
                    if any(n == name for n, _ in stack):
                        while stack and stack.pop()[0] != name:
                            pass
                elif name not in _VOID and not p.endswith("/>"):
                    up = stack[-1][1] if stack else False
                    if up is True or re.fullmatch(r"h[1-6]", name) or _HEADING_CLASS.search(p):
                        in_h = True
                    elif up == "card" or _CARD_CLASS.search(p):
                        in_h = "card"
                    elif name in ("td", "th") and row_first:
                        in_h = "label"  # 表の1行目のマス（項目名）。短ければ見出しと同じく文節の切れ目で改行する
                    else:
                        in_h = False
                    if name == "tr":
                        row_first = True
                    elif name in ("td", "th"):
                        row_first = False
                    stack.append((name, in_h))
            continue
        text = unescape(p)
        body_text = text.rstrip()
        if skip or not _JA.search(body_text):
            continue
        mode = stack[-1][1] if stack else False
        if mode is True or (mode == "card" and len(body_text.strip()) <= _CARD_MAX) or (mode == "label" and len(body_text.strip()) <= 20):
            parts[i] = f'<n-w class="h">{_heading_phrases(body_text)}</n-w>{e(text[len(body_text):], quote=False)}'
            continue
        if len(body_text.strip()) < 6:
            if re.search(r"\d", text):
                parts[i] = _keep_numbers(text, whole=len(text.strip()) <= 20)
            continue
        j = i + 1
        while j < len(parts) and (parts[j] == "" or (inline_end.fullmatch(parts[j]) and not block_end.fullmatch(parts[j]))):
            j += 1
        if j >= len(parts) or not (block_end.fullmatch(parts[j]) or re.fullmatch(r"<br\b[^>]*>", parts[j])):
            if re.search(r"\d", text):
                parts[i] = _keep_numbers(text, whole=len(text.strip()) <= 20)
            continue
        # 全体を <n-w> で包む（横並び（flex）の中でも、文字が1つのまとまりのまま並ぶように）
        # 最後の3文字の切れ目が数字のまとまりの途中に入るときは、まとまりの頭から送る（「約3,18／8万人」を防ぐ）
        short = len(body_text.strip()) <= 20
        whole_cut = len(body_text.strip()) <= 100
        cut = len(body_text) - 3
        for m in (_NUM_TOKEN if whole_cut else _NUM_SHORT).finditer(body_text):
            if m.start() < cut < m.end():
                cut = m.start()
        # 100文字以下の文は、言葉の切れ目に改行候補を入れておく（中央揃えで表示されるときに、語の途中で折れないように。人の指摘 2026-11-06）
        head_html = _phrase_html(body_text[:cut]) if len(body_text.strip()) <= 100 else _keep_numbers(body_text[:cut], whole=short)
        parts[i] = (f"<n-w>{head_html}<n-b>{e(body_text[cut:], quote=False)}</n-b></n-w>"
                    f"{e(text[len(body_text):], quote=False)}")
    return head + sep + "".join(parts)


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
