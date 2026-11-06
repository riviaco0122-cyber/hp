# -*- coding: utf-8 -*-
# build.py の一部：プラン例（料金と内容）と、協業スキームの三角形の図。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- プラン例（空き家再生事業・開業コンサル）
# 数字はすべて「一例」。物件の立地・規模・改修内容により個別に設計する前提で表示する。
PLAN_AXES = {
    "operation": ["初期費用の負担", "毎月の収入", "収益の伸びしろ"],
    "management": ["運営への関わり", "ノウハウ", "アキヤドへの手数料"],
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
            owner=("key", "オーナー様", "物件を貸す・売る", ["建物をRIVIAに貸す、または売る"]),
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
            dict(split=["rivia", "rivia", "rivia", "rivia", "rivia"], name="アキヤドおまかせプラン", catch="初期費用をかけず、毎月決まった家賃を受け取る",
                 owner_share=10, init="改修・家具などの初期費用は、アキヤドがほぼ全額を負担します。",
                 monthly="毎月、決まった額の家賃", example="例：毎月 3万円（一定）",
                 ratings=[("ほぼなし", "good"), ("毎月一定", "good"), ("控えめ", "low")], who=["手間もお金もかけずに空き家を活かしたい", "毎月の収入を安定させたい"], rec=True),
            dict(split=["share", "share", "rivia", "rivia", "rivia"], name="アキヤド売上シェアプラン", catch="補修・内装をアキヤドと共同出資し、家賃＋売上に応じた上乗せを受け取る",
                 owner_share=45, init="建物の補修・内装リフォームはオーナー様とアキヤドで共同出資し、消防設備・家具・開業準備はアキヤドが負担します。",
                 monthly="最低保証の家賃 ＋ 売上の一定割合", example="例：最低保証 2.5万円 ＋ 売上の10%",
                 ratings=[("一部を負担", "mid"), ("最低保証＋上乗せ", "good"), ("売上に応じて増える", "mid")], who=["安定した収入を確保しつつ、繁忙期の上振れも受け取りたい", "補修・内装の費用を一部なら出せる"], rec=False),
            dict(split=["rivia", "rivia", "rivia", "rivia", "rivia"], name="アキヤド買取プラン", catch="物件をアキヤドが買い取り、管理や相続の手間をなくす",
                 owner_share=0, init="", money_label="受け取り方",
                 monthly="売却代金をまとめて受け取る", example="例：現地を拝見して査定",
                 ratings=[("なし", "good"), ("なし（一括で受取）", "low"), ("売却代金のみ", "low")], who=["将来使う予定がない", "管理や相続の手間をなくしたい"], rec=False),
        ],
        note="※ 金額・割合はイメージです。条件は物件ごとにご提案します。契約は更新を前提としています。",
        advice="相続した空き家なら「アキヤドおまかせプラン」がおすすめです。<br>ご自身で運営に関わり、より大きな利益を目指すなら<a href=\"service-management.html\">開業・運営支援事業</a>がおすすめです。",
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
                 monthly="手数料：売上の10%", example="例：売上30万円なら手数料3万円（手取り27万円）",
                 ratings=[("現場を担う", "good"), ("集客の考え方まで", "mid"), ("手数料10%", "good")], who=["お客様との時間は自分で大切にしたい", "開業準備と集客はプロに任せたい"], rec=True),
            dict(split=["owner", "owner", "rivia", "rivia", "rivia"], name="運営代行コース", brand="アキヤド開業・運営プラン", catch="開業準備から運営まで、まるごと任せる",
                 owner_share=0, init="",
                 monthly="運営手数料：売上の20%", example="例：売上30万円なら手数料6万円（手取り24万円）",
                 ratings=[("経営の判断に集中", "mid"), ("レポートで把握", "mid"), ("手数料20%", "mid")], who=["本業が忙しく、現場に時間をかけられない", "遠方の物件や、複数の施設を持っている"], rec=False),
            dict(split=["share", "share", "rivia", "rivia", "rivia"], name="共同出資コース", brand="アキヤド開業・運営プラン", catch="物件取得と初期費用をアキヤドと共同出資し、利益を分け合う",
                 owner_share=0, init="",
                 monthly="利益を、出資の割合で分配", example="例：出資 6：4 → 利益の60%",
                 ratings=[("経営の判断に集中", "mid"), ("レポートで把握", "mid"), ("出資の割合で", "mid")], who=["初期投資の負担とリスクを抑えたい", "プロと一緒に事業として育てたい"], rec=False),
        ],
        note="※ 手数料は売上に対する割合で、残りがオーナー様の手取りです（例：売上30万円・手数料10%なら、手取り27万円）。金額・割合はイメージです。清掃費などの実費は別途かかります。共同出資コースの利益分配は、開業後も継続します。",
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
    "アキヤドおまかせプラン": ("初期費用", "0円", "初期費用をかけず、毎月決まった家賃を受け取る", 1, 0),
    "アキヤド売上シェアプラン": ("初期費用", "共同出資", "補修・内装を共同出資し、家賃＋売上の上乗せを受け取る", 2, 2),
    "アキヤド買取プラン": ("受け取り方", "一括で売却", "物件をアキヤドが買い取り、管理や相続の手間をなくす", 0, 0),
    "伴走コース": ("アキヤドへの支払い", "手数料：売上の10%", "現場は自分で。開業準備と集客・価格はプロに任せる", 2, 3),
    "運営代行コース": ("アキヤドへの支払い", "手数料：売上の20%", "開業準備から日々の運営まで、まるごと任せる", 1, 3),
    "共同出資コース": ("アキヤドへの支払い", "利益を出資比率で分配", "物件取得と初期費用を共同出資し、利益を分け合う", 1, 2),
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
        plans=[("アキヤド買取プラン", "手放す", ("一括", 1), ("売却", 0), "物件をアキヤドが買い取り、管理や相続の手間をなくす"),
               ("アキヤドおまかせプラン", "貸す", ("一定", 2), ("残る", 2), "初期費用0円で、毎月決まった家賃を受け取る"),
               ("アキヤド売上シェアプラン", "出資して貸す", ("上乗せ", 3), ("残る", 2), "共同出資して、家賃＋売上の上乗せを受け取る")]),
    "management": dict(
        band="アキヤドへの支払い", m=("運営の手間", "初期投資"),
        plans=[("伴走コース", "手数料10%", ("中", 2), ("全額", 3), "現場は自分で。開業準備と集客・価格はプロに任せる"),
               ("運営代行コース", "手数料20%", ("小", 1), ("全額", 3), "開業準備から運営まで、まるごと任せる"),
               ("共同出資コース", "利益を分配", ("小", 1), ("一部", 2), "物件取得と初期費用を共同出資し、利益を分け合う")]),
}


def brand_kicker(p):
    """コースの上に、属する「アキヤド〇〇プラン」の名前を小さく出す"""
    return f'<span class="plan-brand">{e(p["brand"])}</span>' if p.get("brand") else ""


def pd_name_html(name):
    """プラン比較の図のプラン名：スマホの細い帯でも、言葉の途中で折り返さないようにする"""
    m = re.match(r"(アキヤド)?(.+?)(プラン[①②③]?)$", name)
    if not m:
        return e(name)
    brand, body, tail = m.groups()
    parts = (f'<span class="pd__brandword">{brand}</span>' if brand else "") + f'<span class="pd__nb">{e(body)}</span><wbr><span class="pd__nb">{tail}</span>'
    return parts


def plan_diagram(key):
    g = PLAN_DIAGRAM[key]
    by_name = {p["name"]: p for p in PLANS[key]["plans"]}
    # 説明文はプランの正本（PLANS の catch）にそろえる（アキヤドのページと同じ文言）
    g = dict(g, plans=[(n, v, m1_, m2_, by_name[n]["catch"]) for n, v, m1_, m2_, _ in g["plans"]])
    m1, m2 = g["m"]
    cols = []
    for i, (name, val, (w1, s1), (w2, s2), desc) in enumerate(g["plans"], 1):
        p = by_name[name]
        badge = '<span class="pd__badge">おすすめ</span>' if p["rec"] else ""
        cols.append(f"""          <div class="pd__plan pd__plan--{i}">
            <div class="pd__seg">
              {badge}{brand_kicker(p)}<p class="pd__name">{pd_name_html(name)}</p>
              <p class="pd__label">{e(g["band"])}</p>
              <p class="pd__value">{e(val)}</p>
            </div>
            <div class="pd__body">
              <div class="pd__metrics">
                <div><span>{e(m1)}</span><b class="pd__c pd__c--a pd__c--{s1}">{e(w1)}</b></div>
                <div><span>{e(m2)}</span><b class="pd__c pd__c--b pd__c--{s2}">{e(w2)}</b></div>
              </div>
              <p class="pd__desc">{e(desc)}</p>
              <a href="contact.html?category={key}" class="pd__cta">{"このコースを相談する" if p["name"].endswith("コース") else "このプランを相談する"} {ARROW}</a>
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
        desc = p.get("catch") or desc  # 説明はプランの正本にそろえる
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
