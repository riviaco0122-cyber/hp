# -*- coding: utf-8 -*-
"""アキヤドの記事に入れる図解（記号のアイコンは使わず、番号と文字と線で見せる）。文字だけの記事を、ひと目で分かるようにする。
図はすべてHTMLとSVGで描く（画像生成と違い、日本語が崩れず、色と線の太さをサイトにそろえられる）。"""
from html import escape as e

# 線のアイコン（24×24、線の太さ1.6）。色はCSSの currentColor
ICON = {
    "house": '<path d="M3.5 11 12 4l8.5 7"/><path d="M5.5 9.5V20h13V9.5"/><path d="M10 20v-5h4v5"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 8-8"/><path d="m16 7 2 2"/><path d="m14 9 2 2"/>',
    "yen": '<path d="m7 4 5 7 5-7"/><path d="M12 11v9"/><path d="M8 13h8"/><path d="M8 16.5h8"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M9 12h6"/><path d="M9 16h6"/>',
    "tool": '<path d="M14.5 5.5a4 4 0 0 0-5 5L4 16l4 4 5.5-5.5a4 4 0 0 0 5-5l-2.5 2.5-3-3z"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.3.2 4 1.8 4.5 4.8"/>',
    "map": '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-4"/><path d="M12 16V8"/><path d="M16 16v-6"/>',
    "calendar": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16"/><path d="M9 3v4"/><path d="M15 3v4"/>',
    "check": '<circle cx="12" cy="12" r="8.5"/><path d="m8.5 12.2 2.4 2.4 4.6-4.8"/>',
    "fire": '<path d="M12 21c-3.6 0-6-2.4-6-5.6 0-3.4 2.6-5 3.4-8.4 1.8 1.2 2.6 2.8 2.6 4.4 1-.6 1.6-1.8 1.8-3 1.6 1.6 4.2 4 4.2 7 0 3.2-2.4 5.6-6 5.6z"/>',
    "bed": '<path d="M3 18V7"/><path d="M3 14h18v4"/><path d="M21 14v-2.5A2.5 2.5 0 0 0 18.5 9H11v5"/><circle cx="7" cy="11" r="1.8"/>',
    "sparkle": '<path d="M12 3.5 13.8 10l6.7 2-6.7 2L12 20.5 10.2 14l-6.7-2 6.7-2z"/>',
    "camera": '<path d="M4 8h3.5L9 5.5h6L16.5 8H20v11H4z"/><circle cx="12" cy="13.5" r="3.3"/>',
    "plane": '<path d="M3 13.5 21 6l-5 14-3.5-5.5z"/><path d="m12.5 14.5 8.5-8.5"/>',
    "leaf": '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14z"/><path d="M5 19 13 11"/>',
    "store": '<path d="M4 9.5 5.5 4.5h13L20 9.5"/><path d="M4 9.5c0 1.5 1.3 2.5 2.7 2.5s2.6-1 2.6-2.5c0 1.5 1.2 2.5 2.7 2.5s2.7-1 2.7-2.5c0 1.5 1.2 2.5 2.6 2.5S20 11 20 9.5"/><path d="M5.5 12v8h13v-8"/>',
    "handshake": '<path d="m3 12 4-4 4 2 2-1.5 4 .5 4 3"/><path d="m7 15 3 3a1.4 1.4 0 0 0 2-2"/><path d="m11 17 1.5 1.5a1.4 1.4 0 0 0 2-2l-1.5-1.5"/><path d="m14 16 1 1a1.4 1.4 0 0 0 2-2l-4-4"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.4 2.4 3.5 5.2 3.5 8.5s-1.1 6.1-3.5 8.5c-2.4-2.4-3.5-5.2-3.5-8.5s1.1-6.1 3.5-8.5z"/>',
    "shield": '<path d="M12 3.5 19 6v5.5c0 4.5-3 7.8-7 9-4-1.2-7-4.5-7-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "bubble": '<path d="M4.5 5.5h15v10h-8L7 19.5v-4H4.5z"/>',
    "route": '<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8 18h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>',
    "train": '<rect x="6" y="3.5" width="12" height="13" rx="3"/><path d="M6 11h12"/><path d="m8 20 1.5-3.5"/><path d="m16 20-1.5-3.5"/>',
    "box": '<path d="M4 7.5 12 4l8 3.5v9L12 20l-8-3.5z"/><path d="m4 7.5 8 3.5 8-3.5"/><path d="M12 11v9"/>',
    "heart": '<path d="M12 19.5s-7.5-4.4-7.5-10A4.2 4.2 0 0 1 12 7a4.2 4.2 0 0 1 7.5 2.5c0 5.6-7.5 10-7.5 10z"/>',
}


def icon(name):
    return f'<svg class="fig-icon" viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg>'


def _figure(kind, title, inner, note=""):
    note_html = f'\n            <figcaption class="fig__note">{e(note)}</figcaption>' if note else ""
    return f"""          <figure class="fig fig--{kind}">
            <p class="fig__title">{e(title)}</p>
{inner}{note_html}
          </figure>"""


def compare(title, cols, note=""):
    """比べる：列ごとに、アイコン・見出し・要点を並べる。cols = [(icon, 見出し, 一言, [要点])]"""
    items = "\n".join(
        f"""              <div class="fig-col{' fig-col--accent' if i == len(cols) - 1 and accent else ''}">
                <p class="fig-col__name">{e(name)}</p>
                <p class="fig-col__sub">{e(sub)}</p>
                <ul class="fig-col__list">{''.join(f'<li>{e(p)}</li>' for p in points)}</ul>
              </div>"""
        for i, (ic, name, sub, points, *rest) in enumerate(cols) for accent in [bool(rest and rest[0])])
    return _figure("compare", title, f'            <div class="fig-cols fig-cols--{len(cols)}">\n{items}\n            </div>', note)


def flow(title, steps, note=""):
    """順番：アイコン・番号・見出し・一言を、矢印でつなぐ。steps = [(icon, 見出し, 一言)]"""
    items = "\n".join(
        f"""              <li class="fig-step"><span class="fig-step__no">{i:02d}</span>"""
        f"""<p class="fig-step__name">{e(name)}</p>{f'<p class="fig-step__sub">{e(sub)}</p>' if sub else ''}</li>"""
        for i, (ic, name, sub) in enumerate(steps, 1))
    return _figure("flow", title, f'            <ol class="fig-steps fig-steps--{len(steps)}">\n{items}\n            </ol>', note)


def cycle(title, center, nodes, note=""):
    """めぐる：4つの段階を円でつなぐ。nodes = [(icon, 見出し)]（4つ）"""
    items = "".join(f'<li class="fig-cyc__node fig-cyc__node--{i}"><span class="fig-cyc__no">{i:02d}</span><span>{e(n)}</span></li>'
                    for i, (ic, n) in enumerate(nodes, 1))
    arrows = "".join(f'<path d="M1.6 0-1.2-1.4v2.8z" transform="translate({x} {y}) rotate({r})"/>'
                     for x, y, r in [(75.5, 24.5, 45), (75.5, 75.5, 135), (24.5, 75.5, 225), (24.5, 24.5, 315)])
    inner = f"""            <div class="fig-cyc">
              <svg class="fig-cyc__ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="36"/>{arrows}</svg>
              <p class="fig-cyc__center">{e(center)}</p>
              <ol class="fig-cyc__nodes">{items}</ol>
            </div>"""
    return _figure("cycle", title, inner, note)


def formula(title, terms, result=None, note=""):
    """式：terms = [(見出し, 一言), "×", ...]。result = (見出し, 一言) を左辺に置く"""
    parts = []
    if result:
        parts.append(f'<span class="fig-term fig-term--result"><b>{e(result[0])}</b><small>{e(result[1])}</small></span><span class="fig-op">＝</span>')
    for t in terms:
        if isinstance(t, str):
            paren = " fig-op--paren" if t in ("（", "）") else ""
            parts.append(f'<span class="fig-op{paren}">{e(t)}</span>')
        else:
            parts.append(f'<span class="fig-term"><b>{e(t[0])}</b><small>{e(t[1])}</small></span>')
    return _figure("formula", title, f'            <div class="fig-formula">{"".join(parts)}</div>', note)


def bars(title, items, note=""):
    """割合：items = [(項目, 割合%, 一言)]。いちばん大きい項目を強調する"""
    top = max(v for _, v, _ in items)
    rows = "\n".join(
        f"""              <li class="fig-bar{' is-top' if v == top else ''}"><span class="fig-bar__label">{e(l)}</span>"""
        f"""<span class="fig-bar__track"><span class="fig-bar__fill" style="width:{v / top * 100:.0f}%"></span></span>"""
        f"""<span class="fig-bar__value">約{v}%</span>{f'<span class="fig-bar__sub">{e(s)}</span>' if s else ''}</li>"""
        for l, v, s in items)
    return _figure("bars", title, f'            <ul class="fig-bars">\n{rows}\n            </ul>', note)


def points(title, items, note=""):
    """要点の一覧：アイコンつきのカードを並べる。items = [(icon, 見出し, 一言)]"""
    cards = "\n".join(
        f"""              <li class="fig-point"><span class="fig-point__no">{i:02d}</span><p class="fig-point__name">{e(n)}</p><p class="fig-point__sub">{e(s)}</p></li>"""
        for i, (ic, n, s) in enumerate(items, 1))
    return _figure("points", title, f'            <ul class="fig-points fig-points--{len(items)}">\n{cards}\n            </ul>', note)


# 記事ごとの図：slug → (入れる節のid, 図)
ARTICLE_FIGURES = {
    "akiya-inherited-house-to-inn": ("options", compare("相続した家の、4つの選択肢", [
        ("yen", "売る", "手放して、まとまったお金に", ["管理や税の負担がなくなる", "家は残らない"]),
        ("tool", "壊す", "更地にする", ["解体費がかかる", "土地の税の軽減がなくなることも"]),
        ("key", "貸す", "住まいとして貸す", ["毎月の家賃収入", "修繕などは貸主の負担が残る"]),
        ("bed", "宿として活かす", "事業者に任せることもできる", ["家を残したまま収入に", "地域に人が訪れる"], True),
    ])),
    "japan-tourism-market-data": ("issues", points("地方の観光が抱える5つの課題", [
        ("map", "都市への集中", "旅行者が大都市と一部の観光地に偏る"),
        ("users", "宿の人手不足", "人が足りず、客室を開けられない"),
        ("bed", "宿・体験の不足", "泊まる場所がなく、日帰りで通過される"),
        ("globe", "情報発信の遅れ", "多言語の案内や予約の導線が弱い"),
        ("leaf", "担い手の減少", "人口減少で、支える人が減っていく"),
    ])),
    "akiya-regional-revitalization": ("cycles", cycle("空き家の再生から始まる、地域の循環", "地域に、人とお金がめぐる", [
        ("house", "空き家を宿に再生"), ("plane", "旅行者が訪れる"), ("store", "地域でお金が使われる"), ("users", "仕事と担い手が育つ"),
    ])),
    "minpaku-vs-ryokan-law": ("compare", compare("民泊新法と旅館業（簡易宿所）の違い", [
        ("house", "民泊新法", "住宅宿泊事業法", ["届出で始められる", "営業は年180日まで", "住宅のまま使える"]),
        ("bed", "旅館業（簡易宿所）", "旅館業法", ["許可が必要", "営業日数の上限なし", "用途や設備の基準を満たす"]),
    ], "※ 自治体の条例で、区域や営業日がさらに制限されることがあります。")),
    "airdna-revenue-simulation": ("formula", formula("収益シミュレーションの基本式", [
        ("販売できる日数", "年間の営業日"), "×", ("稼働率", "埋まった日の割合"), "×", ("客室単価", "1泊あたりの料金"),
    ], result=("売上", "1年間"), note="ここから予約サイトの手数料・清掃費・光熱費などを引いたものが、手元に残る利益です。")),
    "small-inn-subsidies": ("types", points("小規模宿で検討しやすい補助金・支援制度", [
        ("bubble", "集客の仕組みづくり", "小規模事業者持続化補助金"),
        ("chart", "システムの導入", "IT導入補助金"),
        ("house", "改修・起業", "自治体の空き家改修補助・起業支援"),
        ("plane", "宿泊業の受け入れ整備", "観光庁などの事業"),
    ], "※ 公募の時期や条件は年度ごとに変わります。最新の公募要領をご確認ください。")),
    "new-build-vs-used-house-inn": ("compare", compare("新築と中古（空き家の改修）の違い", [
        ("house", "中古（空き家の改修）", "既存の建物を活かす", ["費用を抑えやすい", "開業までが早い", "建物の状態の見極めが必要"], True),
        ("tool", "新築", "一から建てる", ["間取りや設備を自由に設計", "初期費用が大きい", "工期が長くなりやすい"]),
    ])),
    "shizuoka-yaizu-akiya-inn": ("check", points("宿にできるかを見極める5つのチェック", [
        ("users", "誰が泊まるか", "企業・学校・病院・イベントなど、泊まる理由"),
        ("train", "アクセス", "駅やインターからの距離、駐車場"),
        ("house", "建物の状態", "雨漏り・シロアリ・水回りの傷み"),
        ("doc", "制度と条例", "旅館業か民泊新法か、区域や営業日の制限"),
        ("chart", "収支の見通し", "悲観的な想定でも赤字にならないか"),
    ])),
    "minpaku-start-steps": ("flow", flow("民泊の開業までの7ステップ", [
        ("house", "物件と方針を決める", ""), ("doc", "法令・条例・規約を確認", ""), ("fire", "消防署に相談", ""),
        ("tool", "設備を整える", ""), ("check", "届出をする", ""), ("users", "運営体制をつくる", ""), ("camera", "集客を始める", ""),
    ])),
    "akiya-bank-guide": ("what", flow("空き家バンクのしくみ", [
        ("house", "所有者が登録", "自治体に物件の情報を届け出る"),
        ("globe", "自治体が掲載", "ホームページなどで紹介する"),
        ("search", "利用希望者が問い合わせ", "気になる物件を見学する"),
        ("handshake", "交渉・契約", "当事者どうし、または不動産会社を通じて"),
    ])),
    "inn-kpi-basics": ("three", formula("宿の売上を読み解く3つの指標", [
        ("稼働率", "販売できた日のうち、埋まった割合"), "×", ("客室単価（ADR）", "1泊あたりの平均料金"),
    ], result=("RevPAR", "販売できる1日あたりの売上"), note="稼働率だけ、単価だけではなく、両方をかけたRevPARで売上の効率を見ます。")),
    "long-stay-travel-demand": ("change", compare("旅のスタイルの変化", [
        ("route", "巡る旅", "これまで", ["名所を短い日程で回る", "泊まる場所は寝るだけ"]),
        ("bed", "滞在する旅", "これから", ["ひとつの土地に長く泊まる", "暮らすように過ごす"], True),
    ])),
    "minpaku-fire-safety": ("process", flow("開業までの消防の手続き", [
        ("doc", "事前相談", "図面を持って消防署へ"),
        ("tool", "設備の工事", "資格者に依頼して設置"),
        ("check", "検査・通知書", "消防法令適合通知書の交付"),
        ("key", "届出・許可申請", "通知書を添えて申請"),
    ])),
    "ota-vs-direct-booking": ("compare", compare("予約サイト（OTA）と自社予約の違い", [
        ("globe", "予約サイト（OTA）", "新しいお客様との出会い", ["集客力が大きい", "手数料がかかる", "開業直後から使える"]),
        ("heart", "自社予約", "お客様との関係づくり", ["手数料を抑えられる", "リピーターとつながれる", "集客は自分で育てる"], True),
    ], "開業直後は予約サイトで知ってもらい、少しずつ自社予約を育てるのが現実的です。")),
    "kominka-renovation-points": ("concept", compare("改修の前に決める「残すもの」と「変えるもの」", [
        ("leaf", "残すもの", "時間が生む魅力", ["太い梁や柱、吹き抜け", "土間・縁側・囲炉裏", "格子戸・欄間などの建具", "庭や周辺の景色"]),
        ("tool", "変えるもの", "快適さと安全", ["浴室・トイレ・キッチン", "断熱・すきま風対策", "照明・コンセント・Wi-Fi", "耐震性・防火性"], True),
    ])),
    "inn-local-economy": ("flow", flow("旅行者のお金が、地域に広がる流れ", [
        ("bed", "宿泊", "宿の運営者と建物の所有者の収入に"),
        ("store", "宿の外での消費", "飲食店・商店・温泉・体験の売上に"),
        ("box", "宿からの発注", "清掃・リネン・食材・修繕の仕事に"),
        ("users", "雇用と所得", "働く人の所得が、地域での消費に"),
    ])),
    "cleaning-linen-operations": ("system", points("清掃の品質を安定させる3つの仕組み", [
        ("check", "チェックリスト", "掃除する場所と確認項目を、順番どおりに"),
        ("camera", "写真で報告", "決めた位置から撮って、離れていても確認"),
        ("sparkle", "見本の写真", "完成形を示して、誰がやっても同じ仕上がりに"),
    ])),
    "inbound-regional-dispersion": ("chance", points("地方の小さな宿にできること", [
        ("globe", "多言語で届ける", "紹介文や館内の案内を英語などで"),
        ("map", "過ごし方を案内", "周辺の店・体験・移動手段をまとめる"),
        ("house", "土地らしさを魅力に", "建物そのものが日本の暮らしの体験に"),
        ("train", "移動の不安を減らす", "駅からのアクセスや公共交通の使い方"),
    ])),
    "minpaku-management-company": ("tasks", points("住宅宿泊管理業者が担う主な業務", [
        ("users", "宿泊者への対応", "本人確認・名簿・利用ルールの説明"),
        ("bubble", "周辺への配慮", "騒音・ごみなどの苦情への対応"),
        ("sparkle", "衛生管理", "清掃・換気・リネンの交換"),
        ("shield", "安全管理", "非常用照明・避難経路・設備の点検"),
        ("clock", "緊急時の対応", "トラブルや事故の際に駆けつける"),
    ])),
    "akiya-lease-types": ("types", compare("空き家を貸す、3つの契約の形", [
        ("calendar", "普通借家契約", "長く貸し続けたい", ["借主が望めば原則として更新", "返してもらうのが難しい"]),
        ("clock", "定期借家契約", "将来、使う・売るかもしれない", ["期間が来れば終了", "再契約もできる"]),
        ("handshake", "借り上げ（サブリース）", "運営の手間をかけたくない", ["事業者が借りて宿などに", "毎月の家賃を受け取る"], True),
    ])),
    "listing-photo-tips": ("order", flow("予約ページの写真の並べ方", [
        ("sparkle", "いちばんの魅力", "外観・印象的な空間"), ("house", "過ごす場所", "リビング・居間"), ("bed", "寝室", "ベッドの数と配置"),
        ("tool", "水回り", "キッチン・浴室・トイレ"), ("map", "周辺", "景色・近くの店・自然"),
    ])),
    "tourism-labor-shortage": ("summary", compare("人手不足に、3つを同時に", [
        ("bubble", "採用", "魅力を伝える", ["仕事の内容と地域の暮らしを伝える"]),
        ("heart", "定着", "働き続けやすく", ["無理のない働き方と、育てる仕組み"]),
        ("chart", "効率化", "人に頼り切らない", ["予約・鍵・清掃の報告を仕組みに"]),
    ])),
    "inn-startup-funding": ("sources", compare("開業資金の、主な用意の仕方", [
        ("yen", "自己資金", "計画の土台", ["多いほど返済の負担が軽い", "融資の審査でも重視される"]),
        ("handshake", "融資", "日本政策金融公庫・地域の金融機関", ["創業向けの制度がある", "自治体の制度融資も"]),
        ("doc", "補助金・助成金", "条件に合えば上乗せ", ["多くは後払い", "採択されるとは限らない"]),
    ])),
    "guest-review-tips": ("gap", flow("評価を上げる、お客様との接点", [
        ("calendar", "予約から到着まで", "案内で期待をそろえる"), ("key", "到着", "迷わない道順と鍵の受け渡し"),
        ("bed", "滞在中", "困りごとにすぐ応える"), ("heart", "チェックアウト後", "お礼とレビューのお願い"),
        ("bubble", "レビューへの返信", "次のお客様も読んでいる"),
    ])),
    "accommodation-tax": ("what", flow("宿泊税のしくみ", [
        ("users", "宿泊者が支払う", "宿泊料金とあわせて"),
        ("bed", "宿が預かる", "宿が受け取って記録する（特別徴収）"),
        ("doc", "自治体に納める", "定められた期限までに申告・納付"),
        ("map", "観光に使われる", "受け入れ環境の整備や観光振興に"),
    ])),
    "akiya-3000man-deduction": ("conditions", points("「3,000万円特別控除」の主な条件", [
        ("house", "1981年5月31日以前の家", "区分所有建物を除く"),
        ("users", "亡くなった方が一人で住んでいた", "老人ホーム入所などの例外あり"),
        ("key", "相続後は使っていない", "事業・貸付・居住に使っていない"),
        ("calendar", "期限内に売る", "相続から3年目の年末まで"),
        ("yen", "売却価格1億円以下", ""),
        ("tool", "耐震改修または解体", "売った翌年2月15日までに買主が行うことも可"),
    ], "※ 主な条件の要約です。国税庁の案内や税理士にご確認ください。")),
    "kankei-jinko-and-inns": ("what", flow("地域との関わり方のグラデーション", [
        ("plane", "交流人口", "観光などで一時的に訪れる人"),
        ("heart", "関係人口", "地域と継続的に関わる人"),
        ("house", "定住人口", "その地域に住む人"),
    ], "宿は、旅行者が「また来たい」から「関わりたい」へ進む入口になれます。")),
    "minpaku-investment-yield": ("yield", formula("宿の利回りは「運営費を引いて」見る", [
        "（", ("売上", "宿泊料金の合計"), "−", ("運営費", "手数料・清掃・光熱費など"), "）", "÷", ("投資額", "取得費・改修費など"),
    ], result=("実質利回り", "1年間"), note="宿は賃貸より運営費が大きいため、売上だけで見ると利回りを高く見誤ります。")),
    "case-rental-house-inn-first-year": ("invest", bars("初期投資の内訳（全体を100としたとき）", [
        ("家電", 44, "エアコン・冷蔵庫・洗濯機・ガス衣類乾燥機など"), ("家具", 15, ""), ("設備工事", 13, "電気工事"), ("寝具", 9, ""),
        ("写真・ロゴ・看板", 6, ""), ("鍵・チェックイン・防犯", 5, ""), ("その他", 8, "キッチン用品・リネン・消防用品など"),
    ])),
}


def insert_figure(slug, sid, html):
    """節の最初の段落のあとに図を入れる（段落がなければ見出しの直後）"""
    fig = ARTICLE_FIGURES.get(slug)
    if not fig or fig[0] != sid:
        return html
    i = html.find("</p>")
    return (html[:i + 4] + "\n" + fig[1] + "\n" + html[i + 4:]) if i >= 0 else fig[1] + "\n" + html
