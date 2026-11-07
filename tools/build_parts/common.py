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
# カードの見出しになる悩みの文（「〜__worry」）も、言葉の切れ目でだけ改行する（人の指摘 2026-11-06）
_HEADING_CLASS = re.compile(r'class="[^"]*(?:__title|__name|__head\b|heading|-title|__q|__worry)\b')
# カードの説明文などの短い文（60字以内）も、見出しと同じく文節の切れ目でだけ改行する（人の指摘 2026-11-06：事業紹介のカード）
_CARD_CLASS = re.compile(r'class="[^"]*__(?:text|desc|sub|blurb|lead)\b')
_CARD_MAX = 60


_NO_SPLIT = ["のしかかる", "ドラッグ&ドロップ"]  # BudouX が途中で区切る言葉（人の指摘で見つけたら足す）


def _sentences(text):
    """文の終わり（「。」「！」「？」）で文に分ける。かっこの中の「。」（「（例外あり。税務署に確認）」）では分けない"""
    sents, depth, cur = [], 0, ""
    for k, ch in enumerate(text):
        cur += ch
        depth += (ch in "（(「『【") - (ch in "）)」』】")
        if depth <= 0 and ch in "。！？" and k + 1 < len(text) and text[k + 1] not in "」』）)】〉》、。！？ \u3000":
            sents.append(cur); cur = ""
    if cur:
        sents.append(cur)
    return sents


def lines_html(text):
    """リード・コンセプトの改行（お手本：トップのコンセプト文。docs/design-guide.md 3章）。
    1文を1まとまり（.ml-s、文の終わりで改行）にし、文の中は「|」の位置で区切る（「|」がない文は、読点「、」のあとで区切る）。
    区切りは inline-block なので、入る限り前の行に詰め、言葉の途中では折れない。4文字未満の区切りは次とつなげる。
    リストで渡したときは、要素ごとに1まとまりにする（TOP_CONCEPT のように、まとまりを手で決めたもの）"""
    out = []
    for sent in (text if isinstance(text, list) else _sentences(text)):
        if "|" in sent:
            segs = [x for x in sent.split("|") if x]
        else:
            segs, depth, cur = [], 0, ""
            for ch in sent:
                cur += ch
                depth += (ch in "（(「『【") - (ch in "）)」』】")
                if depth <= 0 and ch == "、":
                    segs.append(cur); cur = ""
            if cur:
                segs.append(cur)
        merged = []
        for x in segs:
            if merged and len(merged[-1]) < 4:
                merged[-1] += x
            else:
                merged.append(x)
        # 16文字を超える長い区切りは箱（inline-block）にせず流す（1行に入らない箱は行いっぱいを占め、次の区切りが続けられず右が空くため）
        out.append('<span class="ml-s">' + "".join(f'<span{" class=\"ml-l\"" if len(x) > 16 else ""}>{e(x)}</span>' for x in merged) + "</span>")
    return "".join(out)


def _heading_phrases(text):
    """見出しの文字を文節に分け、文節の切れ目にだけ改行候補（<wbr>）を入れる。最後の文節が2文字以下なら、前の文節とつなげる。
    文の終わり（「。」「！」「？」）のあとに次の文が続くときは、そこで改行し（<br class="sb">）、文ごとに組む。短い文では、
    A の文の直後に B の文を続けず、文ごとに行を分けたほうが読みやすく、右に中途半端な空きもできない（人の方針 2026-11-07）。
    ただし前後の文がどちらも8文字以上のときだけ（「空き家を売る。活かす。」のような短いキャッチは1行で読ませる）"""
    sents = _sentences(text)
    if len(sents) > 1:
        groups = [sents[0]]
        for x in sents[1:]:
            if len(groups[-1].strip()) >= 8 and len(x.strip()) >= 8:
                groups.append(x)
            else:
                groups[-1] += x
        if len(groups) > 1:
            return '<br class="sb">'.join(_heading_phrases(g) for g in groups)
    ph = _budoux.parse(text)
    merged = []
    for x in ph:  # 開きかっこ（「（」など）で終わる文節は、次の文節とつなげる（かっこの直後で改行しない）
        if merged and merged[-1][-1:] in "（(「『【〈《":
            merged[-1] += x
        elif merged and merged[-1][-1:] == "と" and x.startswith("して"):  # 「第三者と／してではなく」→「第三者として／ではなく」
            merged[-1] += "して"
            if x[2:]:
                merged.append(x[2:])
        else:
            merged.append(x)
    ph = merged
    # 「」『』で囲んだ言葉（12文字以内）は、途中で改行しない1つのまとまりにする（「暮らすように／旅する」を防ぐ。人の指摘 2026-11-06）
    merged, buf = [], None  # buf: かっこの中の文節を集めているところ（元の文節のリスト）
    for x in ph:
        if buf is not None:
            m = re.search(r"[」』]", x)
            if not m:
                buf.append(x)
                continue
            inner = buf + [x[:m.end()]]
            if len("".join(inner)) <= 13:
                merged.append("".join(inner))
            else:
                merged.extend(inner)
            if x[m.end():]:
                merged.append(x[m.end():])
            buf = None
            continue
        if ("「" in x and "」" not in x[x.index("「"):]) or ("『" in x and "』" not in x[x.index("『"):]):
            buf = [x]
            continue
        merged.append(x)
    if buf is not None:
        merged.extend(buf)
    # BudouX が語の途中で区切ってしまう言葉は、区切りを外す（見つけたら _NO_SPLIT に足す）
    joined, pos, cuts = "".join(merged), 0, []
    for x in merged[:-1]:
        pos += len(x); cuts.append(pos)
    bad = {c for w in _NO_SPLIT for m in re.finditer(re.escape(w), joined) for c in cuts if m.start() < c < m.end()}
    if bad:
        out_, cur, pos = [], "", 0
        for x in merged:
            cur += x; pos += len(x)
            if pos not in bad:
                out_.append(cur); cur = ""
        if cur:
            out_.append(cur)
        merged = out_
    # 「・」で終わる文節（「個人・」）と、数字が途中で分かれた文節（「202」「6年」）は、次の文節とつなげる
    ph, merged = merged, []
    for x in ph:
        if merged and (merged[-1].endswith("・") or (merged[-1][-1:].isdigit() and x[:1].isdigit()) or re.search(r"[A-Za-z]$", merged[-1]) and re.match(r"[A-Za-z]", x)):
            merged[-1] += x
        else:
            merged.append(x)
    ph = merged
    if len(ph) > 1 and len(ph[-1].strip()) <= 2:
        ph[-2:] = [ph[-2] + ph[-1]]
    # 最後の4文字は改行しないまとまり（<n-b>）にする。左揃えで右に大きな空きができて、js/main.js が言葉の途中でも折れる形
    # （n-w.fill）に切り替えたときも、最後の行が2〜3文字だけにならないように（人の指摘 2026-11-06）
    cut = len("".join(ph)) - 4 if len("".join(ph)) > 6 else -1
    for m in _KEEP_LONG.finditer("".join(ph)):  # 切れ目が数字と単位の途中（「80万／円の事例」）なら、数字の頭から送る
        if m.start() < cut < m.end():
            cut = m.start()
    out, pos, opened = "", 0, False
    for i, x in enumerate(ph):
        if i and pos <= cut:
            out += "<wbr>"
        if not opened and cut >= 0 and pos <= cut < pos + len(x):
            out += e(x[:cut - pos], quote=False) + "<n-b>" + e(x[cut - pos:], quote=False)
            opened = True
        elif not opened and "・" in x.rstrip("・") and len(x) <= 12:
            out += "<n-b>" + e(x, quote=False) + "</n-b>"  # 「個人・法人を」：「・」のあとは keep-all でも折れるので、文節ごとまとめる
        else:
            out += e(x, quote=False)
        pos += len(x)
    if opened:
        out += "</n-b>"
    # 会社名（合同会社RIVIA&CO.）の途中には改行候補を入れない
    return re.sub(r"(?<=合同会社)<wbr>(?=RIVIA)|(?<=RIVIA)<wbr>(?=&amp;)|(?<=RIVIA&amp;)<wbr>(?=CO\.)", "", out)


# 数字のまとまり：前の「約」から、単位（「万人」「兆円」「年3月31日」など）まで。単位がないときは直後の1文字（「2つ」）まで
_NUM_TOKEN = re.compile(r"(?:約)?\d[\d,.]*(?:(?:万|億|兆)?(?:人泊|営業日|時間|か月|円|人|泊|年|月|日|倍|件|戸|棟|回|歳|㎡|室|%|％)(?:\d+(?:か月|月|日))*|[^\s\d,.、。・（）()「」])[、。，．）」』]*")


# 本文の長い段落で使う、短いまとまり：数字と直後の1文字だけ（「5万」「2つ」）。まとまりを長くすると、行末で丸ごと次の行へ送られ、右側が大きく空くため
_NUM_SHORT = re.compile(r"\d[\d,.]*[^\s\d,.、。・（）()「」][、。，．）」』]*")  # 直後の「、」「。」もまとめる（行頭に「、」が来ないように）
# 会社名（「合同会社RIVIA&CO.」）は、数字のまとまりと同じく途中で改行しない（「RIVIA&／CO.」を防ぐ。人の指摘 2026-11-06）
_BRAND = r"(?:合同会社)?RIVIA&CO\."
_KEEP_LONG = re.compile(_BRAND + "|" + _NUM_TOKEN.pattern)
_KEEP_SHORT = re.compile(_BRAND + "|" + _NUM_SHORT.pattern)


def _keep_numbers(text, whole=False):
    """数字の途中や、数字と単位の間で改行しない。エスケープ済みの文字列を返す。
    whole=True（表のマス・ラベルなど20文字以下の短い文言）：「約3,188万人」「2027年3月31日」を丸ごとまとめる（「約3,18／8万人」を防ぐ）。
    whole=False（本文の長い段落）：数字と直後の1文字だけをまとめる（「5／万円」は防ぎ、右端のガタつきは増やさない）"""
    out, last = [], 0
    for m in (_KEEP_LONG if whole else _KEEP_SHORT).finditer(text):
        out += [e(text[last:m.start()], quote=False), f"<n-b>{e(m.group(0), quote=False)}</n-b>"]
        last = m.end()
    return "".join(out) + e(text[last:], quote=False)


def _phrase_html(text):
    """短い文（100文字以下）の文字を、言葉の切れ目に改行候補（<wbr>）を入れた HTML にする。数字のまとまりは1つの塊（<n-b>）のまま。
    左揃えでは行末まで詰めて折り返すので見た目は変わらず、中央揃えで表示される文だけ js/main.js が n-w.c にして切れ目でだけ改行させる"""
    out, last = [], 0
    for m in _KEEP_LONG.finditer(text):
        if text[last:m.start()]:
            out += [e(x, quote=False) for x in _budoux.parse(text[last:m.start()])]
        out.append(f"<n-b>{e(m.group(0), quote=False)}</n-b>")
        last = m.end()
    if text[last:]:
        out += [e(x, quote=False) for x in _budoux.parse(text[last:])]
    return "<wbr>".join(out)


def _glue_short_tail(parts, i):
    """段落の最後が「<strong>契約前に確認</strong>します。」のように、短い文字（6文字未満）で終わるとき、
    直前の太字・リンクごと改行しないまとまり（<n-b>）にする（「確認し／ます。」を防ぐ。人の指摘 2026-11-06）。
    直前の要素の中身が8文字を超えるときは何もしない（狭い枠ではみ出さないように）。<wbr> のあとの短い語（「ベンチャー」など）は、その語だけをまとめる"""
    j = i + 1
    while j < len(parts) and parts[j] == "":
        j += 1
    if j >= len(parts) or not re.fullmatch(r"</(p|li|dd|dt|blockquote|figcaption|td|th)>", parts[j]):
        return False
    k = i - 1
    while k >= 0 and parts[k] == "":
        k -= 1
    if k >= 0 and re.fullmatch(r"<wbr\s*/?>", parts[k]):
        parts[i] = "<n-b>" + e(unescape(parts[i]), quote=False) + "</n-b>"
        return True
    m = re.fullmatch(r"</(strong|em|b|a|span)>", parts[k]) if k >= 0 else None
    if not m:
        return False
    if re.fullmatch(r"[。、．，）」』！？!?)\s]+", unescape(parts[i])):
        # 句読点だけが残るとき（「…<strong>集めます</strong>。」）：「。」は行頭に来ないので、太字の中の最後の3文字をまとめれば足りる
        t = k - 1
        while t >= 0 and parts[t] == "":
            t -= 1
        if t >= 0 and not parts[t].startswith("<") and len(unescape(parts[t]).strip()) > 4:
            txt = unescape(parts[t])
            parts[t] = e(txt[:-3], quote=False) + "<n-b>" + e(txt[-3:], quote=False) + "</n-b>"
            return True
        return False
    name, depth, o = m.group(1), 0, k
    while o >= 0:
        if re.fullmatch(rf"</{name}>", parts[o]):
            depth += 1
        elif re.match(rf"<{name}\b", parts[o]):
            depth -= 1
            if depth == 0:
                break
        o -= 1
    if o < 0:
        return False
    inner = "".join(x for x in parts[o + 1:k] if not x.startswith("<"))
    if len(unescape(inner).strip()) > 8 or any(re.match(r"</?(p|div|li|ul|ol|br)\b", x) for x in parts[o + 1:k]):
        return False
    parts[o] = "<n-b>" + parts[o]
    parts[i] = e(unescape(parts[i]), quote=False) + "</n-b>"
    return True


_SHORT_BLOCKS = {"p", "li", "dd", "dt", "blockquote", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "summary", "label", "button", "div", "span", "a"}
_SHORT_MAX = 60


def _block_text_lengths(parts):
    """開きタグの位置ごとに、その要素の中の文字数（空白を除く）を数える"""
    out, stack, skip = {}, [], 0
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
                        while stack:
                            n, ix = stack.pop()
                            if n == name:
                                break
                elif name not in _VOID and not p.endswith("/>"):
                    stack.append((name, i))
                    out[i] = 0
            continue
        if skip:
            continue
        k = len(re.sub(r"\s", "", unescape(p)))
        if k:
            for _n, ix in stack:
                out[ix] += k
    return out


def phrase_breaks(html):
    """日本語の改行（人の方針 2026-11-05・11-06）。
    - 本文：ふつうに行末まで詰めて折り返す（両端揃え・字間の調整はしない）。段落・ラベルの最後（と <br> の手前）の4文字だけは
      ひとまとまり（<n-b>、改行しない）にして、最後の行に1〜2文字だけがはみ出して残らないようにする。
      数字と直後の単位（「2つ」「5万円」）の間でも改行しない。
    - 見出し：単語の途中で切れないよう、文節の切れ目（<wbr>）でだけ改行する（<n-w class="h">、word-break: keep-all）。"""
    head, sep, body = html.partition("<body")
    parts = re.split(r"(<[^>]+>)", body)
    skip = 0
    stack = []  # (タグ名, 見出しの中か, parts の位置)
    blen = _block_text_lengths(parts)  # 開きタグの位置 → その要素の中の文字数
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
                    if any(n == name for n, *_ in stack):
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
                    stack.append((name, in_h, i))
            continue
        text = unescape(p)
        body_text = text.rstrip()
        if skip:
            continue
        if 0 < len(body_text.strip()) < 6 and _glue_short_tail(parts, i):  # 「…<strong>集めます</strong>。」の「。」など
            continue
        if not _JA.search(body_text):
            continue
        mode = stack[-1][1] if stack else False
        # 短い文（段落・項目・引用・ラベルなど、まとまり全体で60文字以内）は、見出しと同じく言葉の切れ目でだけ改行し、
        # 行の長さをそろえる（CSS の text-wrap: balance）。右に大きな空きや、語の途中の改行を作らない（人の方針 2026-11-06）
        blk = next((ix for n, _m, ix in reversed(stack) if n in _SHORT_BLOCKS), None)
        if blk is not None and 0 < blen.get(blk, 999) <= _SHORT_MAX:
            mode = True
        if mode is True or (mode == "card" and len(body_text.strip()) <= _CARD_MAX) or (mode == "label" and len(body_text.strip()) <= 20):
            parts[i] = f'<n-w class="h">{_heading_phrases(body_text)}</n-w>{e(text[len(body_text):], quote=False)}'
            continue
        if len(body_text.strip()) < 6:
            if re.search(r"\d|RIVIA&", text):
                parts[i] = _keep_numbers(text, whole=len(text.strip()) <= 20)
            continue
        j = i + 1
        while j < len(parts) and (parts[j] == "" or (inline_end.fullmatch(parts[j]) and not block_end.fullmatch(parts[j]))):
            j += 1
        if j >= len(parts) or not (block_end.fullmatch(parts[j]) or re.fullmatch(r"<br\b[^>]*>", parts[j])):
            if re.search(r"\d|RIVIA&", text):
                parts[i] = _keep_numbers(text, whole=len(text.strip()) <= 20)
            continue
        # 全体を <n-w> で包む（横並び（flex）の中でも、文字が1つのまとまりのまま並ぶように）
        # 最後の4文字の切れ目が数字のまとまりの途中に入るときは、まとまりの頭から送る（「約3,18／8万人」を防ぐ）
        short = len(body_text.strip()) <= 20
        whole_cut = len(body_text.strip()) <= 100
        cut = len(body_text) - 4  # 最後の4文字をまとめる（最後の行が2〜3文字だけにならないように。人の指摘 2026-11-06）
        for m in (_KEEP_LONG if whole_cut else _KEEP_SHORT).finditer(body_text):
            if m.start() < cut < m.end():
                cut = m.start()
        # 100文字以下の文は、言葉の切れ目に改行候補を入れておく（中央揃えで表示されるときに、語の途中で折れないように。人の指摘 2026-11-06）
        head_html = _phrase_html(body_text[:cut])  # 長さにかかわらず言葉の切れ目に改行候補を入れる（中央揃えで表示されたときに語の途中で折れないように。人の指摘 2026-11-06）
        parts[i] = (f"<n-w>{head_html}<n-b>{e(body_text[cut:], quote=False)}</n-b></n-w>"
                    f"{e(text[len(body_text):], quote=False)}")
    out = "".join(parts)
    # かっこ・句読点の内側には改行候補を置かない（「力で、「／その土地…」のように「「」だけが行末に残るのを防ぐ。人の指摘 2026-11-06）
    out = re.sub(r"(?<=[「『（(【〈《［・])((?:</?n-[bw][^>]*>)*)<wbr>", r"\1", out)
    out = re.sub(r"<wbr>((?:</?n-[bw][^>]*>)*)(?=[」』）)】〉》］、。，．・：；？！ー])", r"\1", out)
    # 開きかっこの直前と直後の文字を、改行しないまとまりにする（keep-all でない本文でも、「「」だけが行末に残らないように）
    # （文字の部分だけに効かせる。タグの属性（フォームの隠し項目の値など）・script・style は触らない）
    segs, skip_ = re.split(r"(<[^>]+>)", out), 0
    for k, sg in enumerate(segs):
        if sg.startswith("<"):
            m = re.match(r"<(/?)(script|style|textarea|title|svg)\b", sg, re.I)
            if m:
                skip_ += -1 if m.group(1) else 1
        elif k and not skip_:
            segs[k] = re.sub(r"([^\s「『（(【〈《])([「『（【〈《])([^\s」』）】〉》])", r"<n-b>\1\2\3</n-b>", sg)
    out = "".join(segs)
    # 「・」の前後で改行しない（「再生・／創出」「家具・／家電」を防ぐ。人の指摘 2026-11-06）。前後の1文字とまとめる
    segs, skip_ = re.split(r"(<[^>]+>)", out), 0
    for k, sg in enumerate(segs):
        if sg.startswith("<"):
            m = re.match(r"<(/?)(script|style|textarea|title|svg)\b", sg, re.I)
            if m:
                skip_ += -1 if m.group(1) else 1
        elif not skip_ and "・" in sg:
            segs[k] = re.sub(r"([^\s・])・([^\s・])", r"<n-b>\1・\2</n-b>", sg)
    # 「Wi-Fi」「e-Gov」：ハイフンのあとで改行しない。文の終わりの「ます。」を切らない（文字の部分だけを見る。タグの中・script・style は触らない）
    segs, skip_ = re.split(r"(<[^>]+>)", "".join(segs)), 0
    for k, sg in enumerate(segs):
        if sg.startswith("<"):
            m = re.match(r"<(/?)(script|style|textarea|title|svg)\b", sg, re.I)
            if m:
                skip_ += -1 if m.group(1) else 1
        elif k and not skip_:  # k=0 は <body の残り（属性）なので触らない
            if re.search(r"[A-Za-z]-[A-Za-z]", sg):
                sg = re.sub(r"(?<![A-Za-z-])([A-Za-z]+(?:-[A-Za-z]+)+)", r"<n-b>\1</n-b>", sg)
            # 文の終わりの「かな2文字＋。」（「ます。」「です。」）は切らない（「お聞きしま／す。」のように「す。」だけを行頭に送らない）
            segs[k] = re.sub(r"([ぁ-ん]{2}[。！？])", r"<n-b>\1</n-b>", sg)
    out = "".join(segs)
    return head + sep + out


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
