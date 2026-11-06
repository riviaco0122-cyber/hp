# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：サービスごとのページ（図・収支シミュレーション・フォーム）と、会社のページ。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

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
         strengths=[("yen", "初期費用をかけずに始められる", "アキヤドおまかせプランなら、改修・家具などの費用はアキヤドがほぼ負担します。"),
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
         lead="物件選び、許可や届出、写真や料金の決め方、開業後の集客まで。実際に宿を運営しているアキヤドが、任せたい範囲に合わせて支援します。",
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
                spec=[("初期費用", "ほぼなし（アキヤドおまかせプラン）"), ("受け取り方", "毎月の家賃")], plans=["アキヤドおまかせプラン", "アキヤド売上シェアプラン"]),
    "side": dict(photo="scene-stay", summary="物件選び・届出から、開業後の集客と運営まで。任せたい範囲に合わせて伴走します。",
                 spec=[("費用", "手数料：売上の10%〜（伴走コース）"), ("任せる範囲", "開業準備のみ〜運営まで")], plans=["伴走コース", "運営代行コース", "共同出資コース"]),
}

# サービスページの読み物（相談の前に、読者が判断できるだけの材料を出す）
# compare：ほかの選択肢との比べ方（アキヤドの行は us=True）／fit_no：ほかの方法が合うかもしれない方／cases：取材した事例
# 体験談・数字は docs/brand/experience.md の「人が確認済み」の節と、公開済みの記事にあるものだけを使う
MEDIA_SERVICE_MORE = {
    "sell": dict(
        compare=dict(cols=["現金に|なるまで", "古い家の|評価", "売る以外の|提案"], note="", rows=[
            ("仲介で|売る", ["△時期が|読めない", "△値段が|つきにくい", "×なし"], False),
            ("一般的な|買取", ["◎早い", "△改修費を|差し引く", "×なし"], False),
            ("アキヤド|買取", ["◎早い", "◎宿として|評価", "◎貸す案も|比べる"], True)]),  # 買取のページなので、借り上げの列は入れない（人の指摘 2026-10-24）
        fit_no=["時間をかけてでも、少しでも高く売りたい（仲介が合う場合があります）", "宿として営業できない条件の物件（法令や建物の状態によっては、お受けできない場合があります）"],
        cases=["akiya-inherited-house-to-inn", "akiya-holding-costs", "akiya-3000man-deduction"], cases_title="手放す前に読んでおきたい記事",
        faq_more=[("相談したら、売らないといけませんか？", "いいえ。ご提案までは無料で、売るかどうかはご提案を見てから決めていただけます。"),
                  ("ほかの不動産会社と比べてもいいですか？", "はい。比べたうえで決めてください。比べやすいよう、査定の根拠もお出しします。"),
                  ("家族の意見がまとまっていなくても相談できますか？", "ご相談いただけます。ご家族に見せられる比較の資料をお渡しします。"),
                  ("遠方の物件でも大丈夫ですか？", "全国の物件のご相談をお受けしています。初回はオンラインでお話しでき、現地の拝見は鍵の受け渡しの方法もご相談ください。")],
        closing=("決めるのは、比べてからで大丈夫です", "相続登記や税の特例には期限があります。売ると決めていなくても、まずは今の家の値段と、残した場合の収入を知っておくと、ご家族で話し合いやすくなります。")),
    "use": dict(
        compare=dict(cols=["初期費用", "手間", "収入"], note="", rows=[
            ("そのまま|持つ", ["◎なし", "△見回り・|草刈り", "×なし"], False),
            ("住まい|として貸す", ["△改修が|要ることも", "○管理会社に|任せる", "○借り手|しだい"], False),
            ("自分で|民泊", ["△改修・|家具・許可", "△集客・|清掃・対応", "○売上−|経費"], False),
            ("おまかせ|プラン", ["◎ほぼ|なし", "◎ほぼ|なし", "◎毎月|一定"], True),
            ("売上シェア|プラン", ["○補修を|共同出資", "◎ほぼ|なし", "◎保証＋|上乗せ"], True)]),
        fit_no=["近いうちに売る可能性が高い（貸すと3,000万円特別控除が使えなくなる場合があるため、先に比べることをおすすめします）", "数年のうちに、ご自身やご家族が住む予定がある"],
        cases=["case-rental-house-inn-first-year", "case-owner-subsidy-akiya", "case-owner-licensed-akiya"], cases_title="空き家が宿になった事例",
        faq_more=[("家賃はどうやって決まりますか？", "周辺の宿の料金と稼働、改修にかかる費用、契約期間をもとに試算し、根拠とあわせてご提示します。"),
                  ("将来、売ることになったら？", "ご希望があれば最初にお聞かせください。相続した家は、貸すと3,000万円特別控除が使えなくなる場合があるため、売る場合との比較もお出しします。"),
                  ("宿の運営の様子は分かりますか？", "運営の状況を定期的にご報告します。近隣への配慮も含めて宿を運営します。"),
                  ("相談したら、契約しないといけませんか？", "いいえ。ご提案までは無料で、条件を見てから決めていただけます。")],
        closing=("家を残すかどうかは、数字を見てから決められます", "空き家は、使わない時間が長いほど傷み、手を入れる費用もかさみます。まずは、宿にした場合の家賃の見込みを知るところから始めてみてください。")),
    "side": dict(
        compare=dict(cols=["自分の|手間", "開業・集客の|ノウハウ", "初期投資"], note="※ 初期投資は、物件の取得・改修・家具などの費用です。", rows=[
            ("すべて|自分で", ["△すべて", "△手探り", "△全額|自分で"], False),
            ("伴走|コース", ["○清掃・|ゲスト対応", "◎プロが|伴走", "△自分で|用意"], True),
            ("運営代行|コース", ["◎経営の|判断だけ", "◎プロが|運営", "△自分で|用意"], True),
            ("共同出資|コース", ["◎経営の|判断だけ", "◎プロと|一緒に", "◎アキヤドと|分担"], True)]),
        fit_no=["短期間で確実にもうかる方法を探している（収益は物件や運営で変わり、保証はできません）", "宿として営業できない条件の物件で始めたい"],
        cases=["case-owner-rental-side-business", "case-owner-diy-cottage", "case-owner-pricing-mistake"], cases_title="副業で宿を始めた人の事例",
        faq_more=[("会社員でも、本当に運営できますか？", "私たちも会社員として、住まいから離れた下田で宿を始めました。いまは現地に行くのは数か月に1回ほどです。清掃の外注やセルフチェックインなど、離れて運営する仕組みづくりからお手伝いします。"),
                  ("どのコースにするか、相談してから決められますか？", "はい。収支の試算を見ながら、本業との両立やご予算に合うコースをご提案します。"),
                  ("相談したら、契約しないといけませんか？", "いいえ。ご提案までは無料で、試算と条件を見てから決めていただけます。")],
        closing=("始めるかどうかは、試算を見てから決めて大丈夫です", "宿づくりは、物件選びと制度選びで結果が大きく変わります。物件を決める前、契約する前にご相談いただくほど、選べる道が広がります。")),
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
         "ご提案を見て、ご家族とも相談のうえで、ご検討ください。", "それぞれの手取りや手間の違いを、わかりやすく比べてご説明します。", "無料（ご提案を見てから、進めるかどうかを決めていただけます）"),
        ("ご契約・お引き渡し", "1〜2か月", "条件にご納得いただけたら、売買契約を結び、代金のお支払いと物件のお引き渡しを行います。",
         "契約書の内容のご確認と、登記に必要な書類のご準備をお願いします。", "契約から登記までの段取りを進めます。必要に応じて司法書士などの専門家とも連携します。", "登記などの実費は、契約前にご説明します"),
    ],
    "use": [
        ("無料相談", "当日〜数日", "フォームからのご連絡のあと、メールかオンラインで、物件の状況と「家をどうしたいか」を伺います。",
         "物件の場所と、わかる範囲の状況をお知らせください。将来使う予定があるかも教えてください。", "ご希望に合いそうな進め方と、現地調査の日程をご提案します。", "無料"),
        ("現地調査・収支の試算", "2〜3週間", "建物の状態と、周辺の宿の料金や稼働を調べ、宿にした場合の収支を試算します。",
         "可能であれば立ち会いをお願いします。図面などの資料があればご用意ください。", "改修が必要な箇所、法令上の条件、見込める家賃をまとめます。", "無料"),
        ("プランと条件のご提案", "調査から1〜2週間", "おまかせプラン・売上シェアプランのうち、物件とご希望に合う条件をご提案します。",
         "家賃や契約期間、将来の使い方のご希望をお聞かせください。", "家賃・契約期間・改修の負担の分け方を、具体的な数字でご提示します。", "無料（ご提案を見てから、進めるかどうかを決めていただけます）"),
        ("ご契約・改修・開業準備", "2〜4か月", "賃貸借契約を結んだあと、アキヤドが改修・家具の準備・許可の手続き・予約ページの作成まで進めます。",
         "契約内容のご確認をお願いします。改修の内容は、事前にご説明して進めます。", "改修、家具・設備、消防や許可の手続き、写真撮影、予約ページの準備を行います。", "アキヤドおまかせプランは初期費用ほぼなし"),
        ("宿として運営・家賃のお支払い", "開業後、毎月", "集客・予約・清掃・ゲスト対応はアキヤドが行い、オーナー様には毎月家賃をお支払いします。",
         "特にありません。気になることがあれば、いつでもご連絡ください。", "運営の状況を定期的にご報告し、近隣への配慮も含めて宿を運営します。", "運営の手間・費用はかかりません"),
    ],
    "side": [
        ("無料相談", "当日〜数日", "フォームからのご連絡のあと、オンラインで、始めたい宿のイメージやご予算、物件の有無を伺います。",
         "物件が決まっていれば場所を、まだなら希望のエリアやご予算をお知らせください。", "進め方の全体像と、最初に確認すべきことをお伝えします。", "無料"),
        ("物件と制度の確認", "1〜3週間", "物件が宿として営業できるか、民泊新法と旅館業のどちらが合うかを確認します。",
         "物件の資料（図面・登記・管理規約など）をご用意ください。", "用途地域や条例、消防の条件を調べ、選ぶべき制度をご提案します。", "無料"),
        ("収支の試算とプランのご提案", "1〜2週間", "周辺の宿の料金と稼働をもとに収支を試算し、伴走・運営代行・共同出資から合うコースをご提案します。",
         "本業との両立や、どこまで自分で関わりたいかを教えてください。", "悲観的な場合も含めた収支の見通しと、プランごとの費用をご提示します。", "無料（ご提案を見てから、進めるかどうかを決めていただけます）"),
        ("開業準備", "1〜3か月", "設備の準備、消防の手続き、届出や許可申請、写真撮影と予約ページの作成を進めます。",
         "プランに応じて、設備の購入や届出の名義人としての手続きをお願いします。", "やることの一覧と期限をお渡しし、手続きや予約ページづくりを一緒に進めます。", "プランの費用は契約前にご説明します。設備などの実費は別途"),
        ("開業・運営", "開業後", "伴走コースは集客と料金の考え方を、運営代行コースは日々の運営まで、アキヤドが担います。",
         "伴走コースでは、清掃やゲスト対応など現場の運営をお願いします。", "予約の状況や売上を定期的にご報告し、改善の打ち手をご提案します。", "売上に応じた手数料（プランにより異なります）"),
    ],
}


# サービスページ（LP）の見せ方。読み手が最初に知りたい「いくら？」に先に答え、数字は大きく、文章は短く。
# worries_photo：PCでお悩みのリストの横に置く写真（PCで節が簡素に見えないように。人の指摘 2026-10-24）
# hero：読み手の得を言い切る見出し／price：いくら？の目安（金額はイメージ。物件ごとに変わることを必ず添える）
# risk：大きな数字のタイル（出典の記事へリンク）。(数字, 単位, 何の数字か, 説明, 記事, [しくみの3段階])。放っておくといくら損するかを金額で、なぜそうなるかを「しくみ」で見せる（人の指摘 2026-10-24）
# サービスページの「しくみ」の図（文字を読まなくても、誰が何をして、お金がどう流れるかがわかるように）
# nodes: (アイコン, 名前, していること)  arrows: 左から順の矢印の言葉  ret: (戻りの矢印の起点, 終点, 言葉)
# photos: (写真, 添える言葉。| で改行)。自社物件の写真は、どのプランかと結びつけない（docs/brand/experience.md）
MEDIA_SCHEME = {
    "sell": dict(title="売っていただいた家は、アキヤドが宿として活かします",
                 nodes=[("house", "オーナー様", "家を売る"), ("key", "アキヤド", "改修して宿に"), ("users", "旅行者", "まちに泊まる")],
                 arrows=["買取", "宿を運営"], ret=(1, 0, "代金をお支払い"),
                 photos=[("yaizu-before-engawa-garden", "改修前の空き家（例）"), ("scene-stay", "宿として活かす（イメージ）")]),
    "use": dict(title="家を貸すだけで、毎月の家賃が届くしくみです",
                nodes=[("house", "オーナー様", "家を貸す"), ("key", "アキヤド", "改修・運営"), ("users", "旅行者", "宿に泊まる")],
                arrows=["借り上げ", "宿を運営"], ret=(1, 0, "毎月の家賃"),
                photos=[("yaizu-before-floor-open", "改修前の空き家（例）"), ("scene-stay", "宿にしたあと（イメージ）")]),
    "side": dict(title="宿の主役はあなた。アキヤドは裏方で支援します",
                 nodes=[("compass", "アキヤド", "開業を支援"), ("house", "あなたの宿", "開業・運営"), ("users", "旅行者", "宿に泊まる")],
                 arrows=["支援", "予約"], ret=(2, 1, "宿泊の売上"),
                 photos=[("scene-walk", "地域にお金がめぐる（イメージ）"), ("irori-room", "古いまちなみが残る（イメージ）")]),
}


def scheme_html(key):
    sc = MEDIA_SCHEME[key]
    parts = []
    for i, (ic, name, role) in enumerate(sc["nodes"]):
        if i:
            parts.append(f'<span class="mscheme__arrow" aria-hidden="true"><span>{e(sc["arrows"][i - 1])}</span><i></i></span>')
        us = "アキヤド" in name  # アキヤドの丸には、アイコンの代わりにアキヤドのロゴ（マーク）を入れる
        parts.append(f'<div class="mscheme__node{" is-us" if us else ""}"><span class="mscheme__icon">{AKIYADO_MARK if us else icon(ic)}</span><b>{e(name)}</b><small>{e(role)}</small></div>')
    a, b, lbl = sc["ret"]
    lo, hi = sorted((a, b))
    ret = f'<p class="mscheme__ret mscheme__ret--{lo}{hi}{" is-left" if b < a else ""}" aria-hidden="true"><span>{e(lbl)}</span></p>'
    alt = "、".join(f"{n}が{r}" for _, n, r in sc["nodes"]) + f"。{sc['nodes'][a][1]}から{sc['nodes'][b][1]}へ{lbl}"
    def photo(ph, cap):
        # 「（イメージ）」は添え書きから外して写真の隅に小さく載せ、添え書きを1行に収める
        tag = '<span class="mscheme__tag">イメージ</span>' if cap.endswith("（イメージ）") else ""
        cap = cap.removesuffix("（イメージ）")
        return (f'<figure class="mscheme__photo">{tag}<picture><source srcset="images/photos/w/{ph}-800.webp" type="image/webp"><img src="images/photos/{ph}.jpg" alt="" width="800" height="533" loading="lazy" decoding="async"></picture><figcaption>{"<br>".join(e(c) for c in cap.split("|"))}</figcaption></figure>')
    photos = "".join(photo(ph, cap) for ph, cap in sc["photos"])
    return f"""    <section class="mlp-sec mlp-sec--scheme">
      <div class="container mlp-narrow">
        <p class="mlp-en reveal">How it works</p>
        <h2 class="mlp-title reveal">{e(sc["title"])}</h2>
        <div class="mscheme reveal" role="img" aria-label="{e(alt)}"><div class="mscheme__row">{"".join(parts)}</div>{ret}</div>
        <div class="mscheme__photos reveal">{photos}</div>
      </div>
    </section>
"""


# サービスページの「未来の手元」の試算（モデル物件で、オーナー様の手元に残るお金を図で見せる）
# 買取プランには入れない（人の方針 2026-10-24。売ったら代金が入るだけで、未来の収支を見せる意味が薄い）
# 数字はすべて「前提」に書いた仮定・出典から計算する。モデル物件は架空。実績物件（下田・焼津）とプランを結びつけない
# split: (見出し, [(名前, 万円, "cost"|"keep", 添え書き)])  1か月のお金の内訳。任意（借り上げは折れ線で伝わるので付けない。人の判断 2026-10-24）。プランが2つなら splits=[split, split] で並べられる  future: (見出し, [(名前, 万円, 添え書き, アキヤドか)])
# chart: 手元の累計の折れ線（損益分岐点＝0円の線を越える月を見せる）。series: (色, [(月, 万円)])、future の行と同じ順
#   marks: (月, 万円, 言葉, 色, 言葉の置き方 r=右／ur=右上／dr=右下／up=上／down=下)。言葉は「元が取れる」の1つだけにして、ごちゃごちゃさせない
# summary: グラフの前に置く、結論の1〜2文（数学が苦手な人にも伝わる言葉で。「損益分岐点」「累計」「稼働率」などの言葉は使わない）
# big: (ラベル, 前置き, 数字, 単位)  extra: 補足の1文  srcs: 根拠の記事
MEDIA_SIM_MODEL = ["築45年・木造2階建て", "4LDK・約100㎡", "観光地まで車で15分ほど", "相続から5年、空き家のまま"]
MEDIA_SIM = {
    "use": dict(title="借り上げなら、10年でどれだけ変わる？",
                lead="アキヤドが借り上げた場合の2つのプランを、モデル物件で比べました。宿の売上は、私たちの宿やオーナーの事例をもとにしたシミュレーション例です。",
                future=("10年で、手元のお金はどう変わる？", [("おまかせプラン", 333, "最初の出費ほぼなし。毎月3万円の家賃", False), ("売上シェアプラン", 713, "最初に100万円（仮定）出資し、毎月約7万円を受け取る", True)]),
                chart=dict(months=120, xstep=60, x0="今", series=[("sub", [(0, 0), (120, 333.4)]), ("us", [(0, -100), (120, 713.4)])],
                           marks=[(14.75, 0, "約15か月で元が取れる", "us", "dr")]),
                summary="おまかせプランは、最初の出費がほぼなく、毎月家賃が入ります。売上シェアプランは、最初に出すお金を100万円と仮定すると、約15か月で取り戻し、そのあとは大きく増えていく計算です。（空き家のままだと、10年で約63万円が出ていきます）",
                extra="売上シェアプランは、宿の売上が伸びるほど受け取りも増えます。おまかせプランは、売上にかかわらず毎月決まった家賃です。",
                assumptions=["モデル物件は、説明のための架空の物件です。",
                             "おまかせプランの家賃は月3万円（プランの例）。売上シェアプランは、最低保証2.5万円＋売上の10%（プランの例）で、宿の売上を月45万円（1泊2.5万円で、月に18日ほど泊まる）と仮定し、月の受け取りは約7万円です。",
                             "宿の売上の月45万円は、シミュレーション例としての想定です。オーナーの事例では月商が約40万〜55万円の宿があり、私たちの下田の宿は1年目の稼働率が約53%でした。",
                             "売上シェアプランの補修・内装の共同出資は、オーナー様の分を100万円と仮定しています（物件ごとに決めます）。",
                             "家賃・受け取り・期間は、物件と契約で決まります。10年間、同じ条件と仮定しています。",
                             "土地の固定資産税は年26,600円（評価額1,200万円の住宅の敷地。大津市の計算例）で、借り上げ後もオーナー様の負担と仮定。建物の分・都市計画税・保険・所得税などの税金は含みません。",
                             "空き家のままの見回りは月1回3,000円（二本松市のシルバー人材センターの例）。草刈り・修繕は含みません。"],
                srcs=["akiya-holding-costs", "akiya-lease-types", "case-owner-satoyama-airdna"]),
    "side": dict(title="宿を始めたら、5年でいくら残る？",
                 lead="持ち家の空き家を一棟貸しの宿にした場合を、モデル物件で試算しました。私たちの下田の宿と、オーナーの事例（総予算350万〜450万円・月商40万〜55万円）をもとにした、シミュレーション例です。",
                 split=("1か月に45万円売れたら、手元にいくら残る？", [("予約サイトの手数料", 6.8, "cost", "売上の約15%"), ("清掃の委託", 7.2, "cost", "売上の約16%"), ("光熱水費・Wi-Fi・消耗品", 3.0, "cost", "月3万円"), ("アキヤドの手数料", 4.5, "cost", "伴走コース・売上の10%"), ("あなたの手元", 23.5, "keep", "")]),
                 future=("5年で、手元のお金はどう変わる？", [("控えめ（月に14日ほど泊まる）", 615, "毎月 約16.9万円が残り、約24か月で元が取れる", False), ("標準（月に18日ほど泊まる）", 1013, "毎月 約23.5万円が残り、約17か月で元が取れる", True)]),
                 chart=dict(months=60, xstep=12, x0="開業", series=[("sub", [(0, -400), (60, 614.6)]), ("us", [(0, -400), (60, 1013)])],
                            marks=[(17, 0, "約17か月で元が取れる", "us", "up"), (23.7, 0, "", "sub", "dr")]),
                 summary="最初にかかる費用を400万円と仮定すると、毎月 約23.5万円ずつ手元に残り、約17か月で取り戻せる計算です。そのあとは、残ったお金がそのまま増えていきます。",
                 big=("元が取れるまで（標準）", "約", "17", "か月"),
                 extra="あくまでシミュレーション例です。実際のご相談では、悲観的な場合も含めて試算し、赤字にならない計画かを一緒に確かめてから始めます。",
                 assumptions=["モデル物件は、説明のための架空の物件で、持ち家（家賃なし）とします。",
                              "1泊の料金は2.5万円（一棟貸し・6人ほどまで）と仮定。泊まる日は、標準で月18日ほど（稼働率60%）、控えめで月14日ほど（45%）。下田の宿は、1年目が約53%、2年目の上半期が約66%でした。",
                              "標準の月の売上45万円は、オーナーの事例（月商 約40万〜55万円）の範囲です。",
                              "初期費用は400万円（改修・家具・家電・消防設備・申請など）と仮定。オーナーの事例の総予算は約350万〜450万円で、物件の状態で大きく変わります（下田の宿は、改修と家具などで約650万円）。",
                              "予約サイトの手数料（売上の約15%）と清掃の委託（約16%）は、下田の宿の1年目の割合。光熱水費・Wi-Fi・消耗品の月3万円は、下田の宿の開業時の資料の値です。アキヤドの手数料は、伴走コースの売上の10%です。",
                              "毎月同じ売上と仮定しています（実際は季節で大きく変わり、閑散期に赤字の月が出ることもあります）。融資の返済、固定資産税・所得税などの税金、保険、修繕や設備の買い替え、ご自身の手間は含みません。"],
                 srcs=["case-rental-house-inn-first-year", "case-owner-setouchi-cycling", "case-owner-castle-town-nagaya", "case-owner-satoyama-airdna"]),
}


def sim_chart_html(ch, rows):
    """手元の累計の折れ線。線は SVG（縦横に伸びる）、文字と点は HTML で重ねる（スマホでも文字が小さくならない）"""
    vals = [v for _, pts in ch["series"] for _, v in pts] + [0]
    lo, hi = min(vals), max(vals)
    step = next(st for st in (50, 100, 200, 250, 500, 1000) if (hi - lo) / st <= 4)
    lo_t, hi_t = (lo // step) * step, -(-hi // step) * step
    lo_t, hi_t = lo_t - step * 0.15, hi_t + step * 0.15
    X = lambda m: m / ch["months"] * 100
    Y = lambda v: (hi_t - v) / (hi_t - lo_t) * 100
    y0 = Y(0)
    grid = "".join(f'<line x1="{X(m) * 10:.1f}" y1="0" x2="{X(m) * 10:.1f}" y2="400"/>' for m in range(ch["xstep"], ch["months"], ch["xstep"]))
    lines = "".join(f'<polyline class="mchart__line mchart__line--{c}" points="{" ".join(f"{X(m) * 10:.1f},{Y(v) * 4:.1f}" for m, v in pts)}"/>' for c, pts in ch["series"])
    yt, v = [], (lo // step) * step
    while v <= hi:
        if v >= lo - 1e-9:
            yt.append(v)
        v += step
    yt = sorted(set(yt) | {pts[0][1] for _, pts in ch["series"]})  # 線の始まり（最初に出すお金）も目盛りに出す
    ylabels = "".join(f'<span class="mchart__y{" is-zero" if t == 0 else ""}" style="top:{Y(t):.1f}%">{"0" if t == 0 else ("−" if t < 0 else "") + f"{abs(t):,.0f}"}</span>' for t in yt)
    xlabels = "".join(f'<span class="mchart__x{" is-last" if m == ch["months"] else ""}" style="left:{X(m):.1f}%">{e(ch["x0"]) if m == 0 else f"{m // 12}年"}</span>' for m in range(0, ch["months"] + 1, ch["xstep"]))
    marks = "".join(f'<span class="mchart__dot mchart__dot--{c}" style="left:{X(m):.1f}%;top:{Y(v):.1f}%"></span>{f'<span class="mchart__mark mchart__mark--{c} mchart__mark--{pos}" style="left:{X(m):.1f}%;top:{Y(v):.1f}%">{e(t)}</span>' if t else ""}' for m, v, t, c, pos in ch["marks"])
    # 線の終わりの金額は、グラフの右の外に、線の終わりの高さで書く（線に重ならないように）
    ends = "".join(f'<span class="mchart__end mchart__end--{c}" style="top:{Y(pts[-1][1]):.1f}%">{"−" if pts[-1][1] < 0 else "＋"}{abs(round(pts[-1][1])):,}<small>万円</small></span>' for c, pts in ch["series"])
    return f"""<div class="mchart">
            <div class="mchart__plot">
              <svg viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true"><g class="mchart__grid">{grid}</g><line class="mchart__zero" x1="0" y1="{y0 * 4:.1f}" x2="1000" y2="{y0 * 4:.1f}"/>{lines}</svg>
              {ylabels}{xlabels}{marks}{ends}
            </div>
            <p class="mchart__unit">手元のお金（万円）</p>
          </div>"""


def sim_html(key):
    from figures import icon
    sm = MEDIA_SIM[key]
    fmt = lambda v: f"{v:,.1f}".removesuffix(".0")
    splits = sm.get("splits") or ([sm["split"]] if sm.get("split") else [])  # 1か月のお金の内訳（プランごとに1枚）

    def split_html(split_t, parts):
        total = sum(v for _, v, _, _ in parts)
        n_cost = 0
        segs, legend = [], []
        for name, v, kind, note in parts:
            if kind == "cost":
                n_cost += 1
            cls = "keep" if kind == "keep" else f"c{n_cost}"
            segs.append(f'<i class="msim__seg msim__seg--{cls}" style="flex-grow:{v}"></i>')
            legend.append(f'<li class="msim__li msim__li--{cls}"><span class="msim__sw" aria-hidden="true"></span><span class="msim__li-name">{e(name)}{f"<small>{e(note)}</small>" if note else ""}</span><b>{"" if kind == "keep" else "−"}{fmt(v)}<small>万円</small></b></li>')
        return f"""<div class="msim__split">
            <p class="msim__h">{e(split_t)}{"" if f"{fmt(total)}万円" in split_t else f'<span>{"計 " if any(k == "keep" for _, _, k, _ in parts) else "計 −"}{fmt(total)}万円</span>'}</p>
            <div class="msim__bar" aria-hidden="true">{"".join(segs)}</div>
            <ul class="msim__legend" aria-hidden="true">{"".join(legend)}</ul>
          </div>"""
    fut_t, rows = sm["future"]
    rows_html = "".join(f"""<li class="msim__row{" is-us" if us else ""}{" is-minus" if v < 0 else ""}">
            <p class="msim__row-name">{e(n)}<small>{e(nt)}</small></p>
            <span class="msim__sw msim__sw--{c}" aria-hidden="true"></span>
            <p class="msim__row-num">{"−" if v < 0 else "＋"}{abs(v):,}<small>万円</small></p>
          </li>""" for (n, v, nt, us), (c, _) in zip(rows, sm["chart"]["series"]))
    big = ""
    if sm.get("big"):  # 大きな数字の枠（凡例と同じ金額を繰り返すなら付けない）
        bl, bpre, bnum, bunit = sm["big"]
        big = f'<p class="msim__big"><span>{e(bl)}</span><b><small>{e(bpre)}</small>{e(bnum)}<small>{e(bunit)}</small></b></p>'
    specs = "".join(f"<li>{e(x)}</li>" for x in MEDIA_SIM_MODEL)
    assum = "".join(f"<li>{e(x)}</li>" for x in sm["assumptions"])
    srcs = "".join(f'<a href="media/{sl}.html">{e(ARTICLE_BY_SLUG[sl]["title"])} {ARROW}</a>' for sl in sm["srcs"])
    alt = "".join(f"{t}：" + "、".join(f"{n} {fmt(v)}万円" for n, v, _, _ in ps) + "。" for t, ps in splits) + f"{fut_t}：" + "、".join(f"{n} {v}万円" for n, v, _, _ in rows)
    return f"""    <section class="mlp-sec mlp-sec--sim">
      <div class="container">
        <p class="mlp-en reveal">Simulation</p>
        <h2 class="mlp-title reveal">{e(sm["title"])}</h2>
        <p class="mlp-lead reveal">{e(sm["lead"])}</p>
        <div class="msim{" msim--solo" if not splits else " msim--multi" if len(splits) > 1 else ""} reveal" role="img" aria-label="{e(alt)}">
          <div class="msim__model">
            <p class="msim__badge">モデル物件（架空）</p>
            <span class="msim__house" aria-hidden="true">{icon("house")}</span>
            <ul class="msim__specs">{specs}</ul>
          </div>
          {"".join(split_html(t, ps) for t, ps in splits)}
        </div>
        <div class="msim__future reveal" aria-hidden="true">
          <p class="msim__h msim__h--c">{e(fut_t)}</p>
          <p class="msim__summary">{e(sm["summary"])}</p>
          <ul class="msim__howto"><li><b>線が上がる</b>手元のお金が増える</li><li><b>線が下がる</b>お金が出ていく</li><li><b>点線より上</b>プラス（得をしている）</li></ul>
          <div class="msim__fwrap">
            {sim_chart_html(sm["chart"], rows)}
            <div class="msim__fside">
              <ul class="msim__rows msim__rows--{len(rows)}">{rows_html}</ul>
              {big}
            </div>
          </div>
        </div>
        <p class="msim__extra reveal">{e(sm["extra"])}</p>
        <details class="mlp-fold msim__fold reveal"><summary>試算の前提</summary><ul>{assum}</ul><p class="msim__srcs">{srcs}</p></details>
        <p class="msim__disclaim">この試算は、架空のモデル物件でのシミュレーションです。<strong>将来の収益や金額を保証・約束するものではありません。</strong>実際の収支は、物件・立地・季節・運営によって大きく変わります。お持ちの物件は、現地を拝見したうえで試算します。</p>
      </div>
    </section>
"""


# letter：創業者からの一言の、サービスごとの最後の一文
MEDIA_SERVICE_LP = {
    "sell": dict(
        photo="old-town-street",
        hero="古くて売れない家も、<br><em>宿として活かせるなら</em><br>買い取ります。",
        hero_sub="相続した家、遠方で管理できない家。住まいとしては値段がつきにくい家も、宿として活かせるなら買い取れます。",
        hero_sub_sp="値段がつきにくい家も、|宿として活かせるなら買い取れます。",
        worries_title="こんなお悩み、ひとりで抱えていませんか？", worries_photo="dark-room",
        price=dict(title="買取価格は、宿として稼げるかで決まります",
                   lead="宿の収益から考えるので、古い家・地方の家にも値段がつくことがあります。",
                   # (式の言葉, 補足, スマホで式に書く短い言葉)
                   formula=[("宿にしたときに見込める収益", "周辺の宿の料金と稼働から", "宿の収益"), ("宿にするための改修の費用", "建物の状態と法令の条件から", "改修費"), ("買取価格のめやす", "根拠とあわせて書面で", "買取価格")],
                   facts=[("無料", "相談・拝見・査定"), ("2〜4週間", "ご提示までの目安"), ("不要", "仲介手数料")],
                   note="金額は物件の状態・立地・法令の条件で変わります。現地を拝見し、根拠とあわせて書面でご提示します。"),
        risk_title="空き家は、放っておくほど選べる道が減っていきます",
        risk=[("10", "万円以下", "名義変更をしないときの過料", "2024年4月から、相続を知った日から3年以内の名義変更が義務に。昔の相続でも2027年3月31日までに申請が必要です（正当な理由がない場合が対象）。", "souzoku-touki-gimuka", ["家を相続する", "3年以内に名義変更", "しないと過料の対象に"]),
              ("約14", "万円／年", "土地の固定資産税が増える額", "評価額1,200万円の土地なら、年2.8万円の税が16.8万円に（計算のもとが6倍）。実際は数年かけて、この額まで上がります。", "akiya-holding-costs", ["管理が行き届かない", "市から勧告を受ける", "税を軽くする特例が外れる"]),
              ("最高3,000", "万円", "期限を過ぎると使えなくなる控除", "売った利益から最高3,000万円を引ける特例です。2027年末までの売却が対象で、相続後に貸したり宿にしたりしても使えなくなります。条件は税務署・税理士に確認を。", "akiya-3000man-deduction", ["相続した古い家を売るなら", "相続から3年後の年末までが期限", "過ぎると、控除が使えない"])],
        points_title="売るだけでなく、家を残す道も一緒に比べます",
        letter="手放すと決める前に、[[宿として活かす道があるか]]を、一緒に確かめさせてください。"),
    "use": dict(
        photo="irori-room",
        hero="初期費用は<em>ほぼ0円</em>。<br>空き家を、毎月の家賃に。",
        hero_sub="アキヤドが借り上げ、改修から宿の運営まで行います。家は持ったまま、手間をかけずに家賃を受け取れます。",
        hero_sub_sp="家は持ったまま、|手間をかけずに家賃を受け取れます。",
        worries_title="こんなお悩み、ひとりで抱えていませんか？", worries_photo="window-garden",
        price=dict(title="家賃は、いくらになる？",
                   lead="周辺の宿の料金と稼働、広さ、改修にかかる費用から、物件ごとに試算します。受け取り方は2つから選べます。",
                   cards=[("アキヤドおまかせプラン", "毎月", "3", "万円", "決まった額の家賃（例）", "改修・家具などの初期費用は、アキヤドがほぼ全額を負担します"),
                          ("アキヤド売上シェアプラン", "最低保証", "2.5", "万円＋売上の10%", "（例）売上40万円の月なら 6.5万円", "補修・内装はオーナー様とアキヤドで共同出資。繁忙期の上振れも受け取れます")],
                   factors=["立地（周辺の宿の料金と稼働）", "広さ・泊まれる人数", "建物の状態（改修の費用）", "契約期間"],
                   note="金額はイメージです。物件によって変わります。現地調査のうえ、根拠とあわせてご提示します。"),
        risk_title="使っていない家にも、お金と手間はかかり続けます",
        risk=[("約14", "万円／年", "土地の固定資産税が増える額", "評価額1,200万円の土地なら、年2.8万円の税が16.8万円に（計算のもとが6倍）。実際は数年かけて、この額まで上がります。", "akiya-holding-costs", ["管理が行き届かない", "市から勧告を受ける", "税を軽くする特例が外れる"]),
              ("約63", "万円", "何もしなくても、10年で出ていくお金", "評価額1,200万円の土地・月1回の見回り（1回3,000円）の例。建物の分の税・草刈り・修繕は別にかかります。", "akiya-holding-costs", ["土地の税 年2.7万円", "見回り 年3.6万円", "10年続くと約63万円"]),
              ("10", "万円以下", "名義変更をしないときの過料", "2024年4月から、相続を知った日から3年以内の名義変更が義務に。昔の相続でも2027年3月31日までに申請が必要です（正当な理由がない場合が対象）。", "souzoku-touki-gimuka", ["家を相続する", "3年以内に名義変更", "しないと過料の対象に"])],
        points_title="改修から宿の運営まで、すべてアキヤドが行います",
        letter="思い出のある家を、[[壊さず、手放さずに活かす]]。その道があるかを、数字でお見せします。"),
    "side": dict(
        photo="scene-stay",
        hero="はじめての民泊を、<br><em>宿を運営する私たち</em>が伴走します。",
        hero_sub="物件選び、許可や届出、料金の決め方、開業後の集客まで。会社員のまま宿を始めた私たちが、任せたい範囲に合わせて支援します。",
        hero_sub_sp="物件選びから集客まで、|任せたい範囲だけ支援します。",
        worries_title="こんなところで、止まっていませんか？", worries_photo="analytics-paper",
        price=dict(title="いくらかかって、いくら残る？ 私たちの宿の数字です",
                   lead="創業メンバーが下田（静岡県）で、借りた家を一棟貸しの宿にしたときの数字です。物件や運営で変わりますが、計画を立てるときの目安になります。",
                   cards=[("初期費用", "約", "650", "万円", "改修 約410万円＋家具・家電・備品 約240万円", "物件は賃貸のため、取得費はかかっていません"),
                          ("月の手残り", "売上の約", "67", "%", "2年目上半期の営業利益率", "清掃を自分たちで行った期間の値（自分たちの人件費は含みません）。融資の返済・税金の前です"),
                          ("投資の回収", "約", "14", "か月", "初期投資の約98%を回収", "営業利益で回収（2026年9月時点）。家具・家電・設備工事などの購入費を基準にした割合です")],
                   fee="アキヤドの手数料は、伴走コースで売上の10%（例：売上30万円の月なら3万円）。運営代行コースは20%です。",
                   note="数字は一つの宿の実績で、収益を保証するものではありません。くわしくは運営事例の記事をご覧ください。", src="case-rental-house-inn-first-year"),
        risk_title="自己流で始めると、ここでつまずきます",
        risk=[("180", "日", "民泊新法で営業できる、年の上限", "通年で営業するなら旅館業の許可が必要。番号がないと予約サイトで予約を受けられません。", "minpaku-vs-ryokan-law"),
              ("2", "か月以上", "Wi-Fi工事にかかった期間（私たちの開業）", "古い家の配線で家電が同時に使えない、工事後の想定外の請求なども経験しました。", "case-rental-house-inn-first-year"),
              ("稼働率92", "%でも赤字", "取材したオーナーの宿の例", "清掃が月25回以上かかり、実質赤字でした。1泊の料金を9,800円から18,500円に上げると、売上が増え、清掃は月7回前後に減りました。", "case-owner-pricing-mistake")],
        points_title="私たちがつまずいたところを、あなたは先回りできます",
        letter="[[私たちがつまずいたところは、先回りできます。]]始めるかどうかは、試算を見てから決めてください。"),
}


def detail_flow(key):
    steps = MEDIA_FLOWS[key]
    items = "\n".join(f"""          <li class="dflow__step reveal">
            <div class="dflow__head"><span class="dflow__no">STEP {i:02d}</span><span class="dflow__term">{e(term)}</span></div>
            <div class="dflow__body">
              <h3 class="dflow__title">{e(t)}</h3>
              <p class="dflow__text">{e(d)}</p>
              <details class="spfold" open><summary>お願いすること</summary>
              <dl class="dflow__roles">
                <div><dt>お客様にお願いすること</dt><dd>{e(you)}</dd></div>
                <div><dt>アキヤドが行うこと</dt><dd>{e(we)}</dd></div>
              </dl>
              <p class="dflow__cost"><span>費用</span>{e(cost)}</p>
              </details>
            </div>
          </li>""" for i, (t, term, d, you, we, cost) in enumerate(steps, 1))
    return f"""        <ol class="dflow">
{items}
        </ol>
        <ul class="dflow__notes reveal">
          <li>ご提案まではすべて無料です。内容を見てから、進めるかどうかを決めていただけます。</li>
          <li>しつこい営業や、ご希望のない電話はいたしません。</li>
          <li>期間は目安です。物件の状態や手続きの状況によって前後します。</li>
        </ul>"""


NOTE_STORY_URL = "https://note.com/calm_quokka8545/n/n6de4ea4f8b5f"


NOTE_STORY_ARTICLES = {"minpaku-start-steps", "case-rental-house-inn-first-year", "minpaku-remote-operation",
                       "inn-startup-funding", "minpaku-vs-ryokan-law"}


def note_story(indent="        "):
    """代表・片井が、はじめて民泊に挑戦したときの体験記（note）への案内"""
    return f"""{indent}<a href="{NOTE_STORY_URL}" class="mstory reveal" target="_blank" rel="noopener" data-cta="note-story">
{indent}  <span class="mstory__photo" aria-hidden="true"></span>
{indent}  <span class="mstory__body">
{indent}    <span class="mstory__en">Founder's story</span>
{indent}    <span class="mstory__title">会社員が片道2時間の下田で、民泊を始めた記録</span>
{indent}    <span class="mstory__text">合同会社RIVIA&CO.の代表社員の片井が、はじめて民泊に挑戦したときの体験記です。開業までのリアルと、開業後3か月の歩みをnoteにまとめています。</span>
{indent}    <span class="mstory__link">noteで読む（別タブで開きます） {ARROW}</span>
{indent}  </span>
{indent}</a>
"""


def media_form(sv):
    """サービスページのフォーム。最初に「無料で相談する／資料をもらう」を選び、名前とメールを送る。
    資料を選ぶと「ご相談カテゴリ」を「サービス資料の請求」にする（tools/forms/Code.gs が資料の請求と判定し、自動返信に資料を付ける）"""
    reps = [('class="qform reveal" data-delay="2"', 'class="qform qform--media mform2__form"'),
            ('data-thanks="thanks.html?form=contact"', 'data-thanks="thanks.html"'),
            ("【RIVIA&amp;CO.】", "【アキヤド】"),
            (f'<p class="qform__title">{e(sv["name"])}の無料相談</p>\n', ''),
            ('<p class="qform__lead">まだ検討中の段階でも大丈夫です。2営業日以内にご連絡します。</p>\n', ''),
            (f'<input type="hidden" name="ご相談カテゴリ" value="{e(sv["name"])}">',
             f'<input type="hidden" name="ご相談カテゴリ" value="{e(sv["name"])}" data-consult="{e(sv["name"])}" data-doc="サービス資料の請求">'),
            ('<label class="qform__field"><span>ご相談内容', '<label class="qform__field mform2__consult-only"><span>ご相談内容'),
            ('<div class="qform__field qform__file">', '<div class="qform__field qform__file mform2__consult-only">'),
            (f'<button type="submit" class="btn qform__submit">無料で相談する {ARROW}</button>',
             f'<button type="submit" class="btn qform__submit"><span class="mform2__submit-t">無料で相談する</span> {ARROW}</button>')]
    form = quick_form(sv["category"], sv["name"])
    for old, rep in reps:
        assert old in form, old
        form = form.replace(old, rep)
    return f"""          <div class="mform2" id="diag"><span id="diag-doc" class="mform2__anchor"></span>
            <p class="mform2__title">{e(sv["name"])}について</p>
            <div class="mform2__modes" role="radiogroup" aria-label="ご希望">
              <button type="button" class="mform2__mode" role="radio" aria-checked="true" data-mode="consult"><strong>無料で相談する</strong><span>2営業日以内にご連絡します</span></button>
              <button type="button" class="mform2__mode" role="radio" aria-checked="false" data-mode="doc"><strong>資料をもらう</strong><span>プランの資料をメールでお送りします</span></button>
            </div>
{form}
          </div>"""


def media_service_page(sv):
    from figures import icon
    key = sv["key"]
    lp = MEDIA_SERVICE_LP[key]
    more = MEDIA_SERVICE_MORE[key]
    grp = next(g for g in MEDIA_PLAN_GROUPS if g[0] == key)
    _, label, _, src, names = grp
    money_label = "受け取り方" if src == "operation" else "費用"
    plans = sorted((p for p in PLANS[src]["plans"] if p["name"] in names), key=lambda p: names.index(p["name"]))
    plan_cards = "\n".join(media_plan_card(p, key, money_label) for p in plans)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("アキヤドのプラン", "media/plans.html"), (sv["name"], "")])
    worries = "".join(f'<li>{e(w)}</li>' for w in sv["worries"])

    # いくら？
    pr = lp["price"]
    if "formula" in pr:
        steps = []
        # スマホは「宿の収益 − 改修費 ＝ 買取価格」と短い言葉の式だけにする（縦に積むと式に見えず、長い言葉を横に並べると窮屈。説明を足すと文字が多い。人の指摘 2026-10-24）
        for i, (t, n, sh) in enumerate(pr["formula"]):
            op = ["", '<span class="mprice__op" aria-hidden="true">−</span>', '<span class="mprice__op" aria-hidden="true">＝</span>'][i]
            steps.append(f'{op}<div class="mprice__term{" is-result" if i == 2 else ""}"><span class="mprice__term-t"><span class="pc-only">{e(t)}</span><span class="sp-only">{e(sh)}</span></span><span class="mprice__term-n pc-only">{e(n)}</span></div>')
        facts = "".join(f'<li><span class="mprice__fact-big">{e(b)}</span><span class="mprice__fact-l">{e(l)}</span></li>' for b, l in pr["facts"])
        price_body = f"""        <div class="mprice__formula reveal">{"".join(steps)}</div>
        <ul class="mprice__facts reveal">{facts}</ul>"""
    else:
        cards = "".join(f"""<li class="mprice__card">
            <p class="mprice__card-label">{e(lbl)}</p>
            <p class="mprice__card-num"><small>{e(pre)}</small>{e(num)}<small>{e(unit)}</small></p>
            <p class="mprice__card-ex">{e(ex)}</p>
            <p class="mprice__card-note">{e(nt)}</p>
          </li>""" for lbl, pre, num, unit, ex, nt in pr["cards"])
        extra = ""
        if pr.get("factors"):
            extra += '<div class="mprice__factors reveal"><p>家賃が決まる4つのこと</p><ul>' + "".join(f"<li>{e(f)}</li>" for f in pr["factors"]) + "</ul></div>"
        if pr.get("fee"):
            extra += f'<p class="mprice__fee reveal">{e(pr["fee"])}</p>'
        price_body = f"""        <ul class="mprice__cards mprice__cards--{len(pr["cards"])} reveal">{cards}</ul>
        {extra}"""
    src_link = f' <a href="media/{pr["src"]}.html">運営事例の記事 {ARROW}</a>' if pr.get("src") else ""

    risks = "".join(f"""<li class="mrisk">
            <p class="mrisk__num">{(lambda m: (f'<small class="mrisk__pre">{e(m.group(1))}</small>' if m.group(1) else "") + e(m.group(2)))(re.match(r"(\D*)(.*)", n))}<small>{e(u)}</small></p>
            <p class="mrisk__label">{e(l)}</p>
            {(lambda how: f'<div class="mrisk__how"><p class="mrisk__how-h">しくみ</p><ol>' + "".join(f"<li>{e(x)}</li>" for x in how) + "</ol></div>" if how else "")(r[5] if len(r) > 5 else None)}
            <p class="mrisk__text">{e(t)}</p>
            <a class="mrisk__link" href="media/{sl}.html">くわしく {ARROW}</a>
          </li>""" for r in lp["risk"] for n, u, l, t, sl in [r[:5]])

    points = "\n".join(f"""          <li class="mpoint reveal">
            <span class="mpoint__icon" aria-hidden="true">{icon(ic)}</span>
            <div><h3 class="mpoint__title">{e(t)}</h3><p class="mpoint__text">{e(d)}</p></div>
          </li>""" for ic, t, d in sv["strengths"])

    founders = "".join(f'<figure class="mletter__face"><img src="images/{f["photo"]}" alt="{e(f["name"])}" width="96" height="96" loading="lazy" decoding="async"><figcaption>{e(f["name"])}<small>代表社員</small></figcaption></figure>'
                       for f in FOUNDERS)
    review = NODE_REVIEWS[0]
    cmp = more["compare"]
    wb = lambda t: e(t).replace("|", "<wbr>")  # 「|」は改行してよい位置
    # 各マスの先頭の記号（◎○△×）を、色つきの大きな評価マークにする。言葉は小さく添える
    marks = {"◎": ("good", "とてもよい"), "○": ("ok", "よい"), "△": ("bad", "負担・注意"), "×": ("none", "なし")}
    # 記号は文字ではなく図形で描く（文字だとフォントによって丸の中心から上下にずれるため）
    _mk = '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
    mark_svg = {"◎": _mk.format('<circle cx="10" cy="10" r="7"/><circle cx="10" cy="10" r="3.6"/>'),
                "○": _mk.format('<circle cx="10" cy="10" r="6.5"/>'),
                "△": _mk.format('<path d="M10 3.6 17 15.6H3z"/>'),
                "×": _mk.format('<path d="M4.8 4.8l10.4 10.4M15.2 4.8 4.8 15.2"/>')}
    def cmp_cell(c, us=False):
        cls = ' class="is-us"' if us else ""
        m = marks.get(c[:1])
        if not m:
            return f"<td{cls}>{wb(c)}</td>"
        return f'<td{cls}><span class="mcmp__mark mcmp__mark--{m[0]}" role="img" aria-label="{m[1]}">{mark_svg[c[:1]]}</span><span class="mcmp__t">{wb(c[1:])}</span></td>'
    # 選択肢を横（列）、比べることを縦（行）に並べる。スマホは1列目を止めたまま、左右にスライドして見比べる（人の指摘 2026-10-24）
    cmp_head = "".join(f'<th scope="col"{" class=\"is-us\"" if us else ""}>{wb(n)}</th>' for n, _, us in cmp["rows"])
    cmp_rows = "\n".join(f"""              <tr><th scope="row">{wb(col)}</th>{"".join(cmp_cell(cells[i], us) for _, cells, us in cmp["rows"])}</tr>"""
                         for i, col in enumerate(cmp["cols"]))
    fit_no = "".join(f"<li>{e(x)}</li>" for x in more["fit_no"])
    cases = [ARTICLE_BY_SLUG[sl] for sl in more["cases"]]
    closing_t, closing_d = more["closing"]

    body = f"""    <section class="mlp-hero">
      <div class="container">{crumbs}
        <div class="mlp-hero__grid">
          <div class="mlp-hero__text">
            <p class="mlp-hero__eyebrow reveal">{e(sv["eyebrow"])}<span class="pc-only">｜{e(sv["name"])}</span></p>
            <h1 class="mlp-hero__title reveal" data-delay="1">{lp["hero"]}</h1>
            <p class="mlp-hero__sub pc-only reveal" data-delay="2">{e(lp["hero_sub"])}</p>
            <p class="mlp-hero__sub mlp-hero__sub--sp sp-only reveal" data-delay="2">{e(lp["hero_sub_sp"]).replace("|", "<br>")}</p>
            <ul class="mlp-hero__promise reveal" data-delay="2"><li><strong>無料</strong>相談・試算</li><li><strong>2営業日</strong>以内にご連絡</li><li><strong>全国</strong>オンライン可</li></ul>
            <picture class="mlp-hero__photo reveal" data-delay="3"><source srcset="images/photos/w/{lp["photo"]}-800.webp" type="image/webp"><img src="images/photos/{lp["photo"]}.jpg" alt="" width="800" height="533" loading="eager" decoding="async"></picture>
          </div>
{media_form(sv)}
        </div>
      </div>
    </section>

    <section class="mlp-sec mlp-sec--worry">
      <div class="container mlp-narrow">
        <h2 class="mlp-title reveal">{e(lp["worries_title"])}</h2>
        <div class="mlp-worry reveal">
          <picture class="mlp-worry__photo pc-only"><source srcset="images/photos/w/{lp["worries_photo"]}-800.webp" type="image/webp"><img src="images/photos/{lp["worries_photo"]}.jpg" alt="" width="800" height="1000" loading="lazy" decoding="async"></picture>
          <div class="mlp-worry__body">
            <ul class="mlp-worries">{worries}</ul>
            <p class="mlp-worry__cta"><a href="#diag" data-cta="media-service-worry">ひとつでも当てはまったら、<br class="sp-only">まずは無料でご相談ください {ARROW}</a></p>
          </div>
        </div>
      </div>
    </section>

{scheme_html(key)}
    <section class="mlp-sec mlp-sec--soft">
      <div class="container">
        <p class="mlp-en reveal">How much?</p>
        <h2 class="mlp-title reveal">{e(pr["title"])}</h2>
        <p class="mlp-lead reveal">{e(pr["lead"])}</p>
{price_body}
        <p class="mprice__note">※ {e(pr["note"])}{src_link}</p>
      </div>
    </section>

{sim_html(key) if key in MEDIA_SIM else ""}
    <section class="mlp-sec">
      <div class="container">
        <p class="mlp-en reveal">Risk</p>
        <h2 class="mlp-title reveal">{e(lp["risk_title"])}</h2>
        <ul class="mrisks reveal">{risks}</ul>
        <p class="mrisks__hint" aria-hidden="true">横にスワイプして、{len(lp["risk"])}つ見られます →</p>
      </div>
    </section>

    <section class="mlp-sec mlp-sec--green">
      <div class="container">
        <h2 class="mlp-title mlp-title--light reveal">{e(lp["points_title"])}</h2>
        <ol class="mpoints">
{points}
        </ol>
        <div class="mlp-ctarow reveal"><a href="#diag" class="mbtn" data-cta="media-service-mid">無料で相談する {ARROW}</a><a href="#diag-doc" class="mbtn mbtn--sub" data-cta="media-service-mid-doc">資料をもらう（無料） {ARROW}</a></div>
      </div>
    </section>

    <section class="mlp-sec">
      <div class="container">
        <div class="mletter reveal">
          <p class="mlp-en">Message</p>
          <h2 class="mletter__title">会社員から宿を始めた私たちが、<br class="pc-only">ご相談をお受けします</h2>
          <div class="mletter__faces">{founders}</div>
          <div class="mletter__body">
            <p>はじめまして。アキヤドを運営する合同会社RIVIA&amp;CO.の、石原と片井です。</p>
            <p>私たちは宿泊業の経験がない会社員として、住まいから離れた静岡県下田市で、借りた家を宿にしました。準備に約7か月。法人での融資の相談が見送られたこと、工事のあとの想定外の請求、古い配線で家電が同時に使えないこと。つまずきは、ひと通り経験しました。</p>
            <p>それでも、清掃を地域の方にお願いし、セルフチェックインなどの仕組みを整えたことで、いまは<strong class="hl">現地に行くのは数か月に1回ほどで宿が回っています</strong>。</p>
            <p>空き家は、手を入れれば旅をする人の滞在先になり、まちに人の流れを生みます。{e(lp["letter"]).replace("[[", "<strong class=\"hl\">").replace("]]", "</strong>")}</p>
            <p class="mletter__sign">合同会社RIVIA&amp;CO. 代表社員<br>石原 佑真・片井 進太</p>
          </div>
          <p class="msv-stats__cap">運営する宿の一例<span>NODE Shimoda（静岡県下田市）</span></p>
          <ul class="msv-stats">
            <li><p class="msv-stats__num"><small class="msv-stats__pre">約</small>14<small>か月</small></p><p class="msv-stats__label">初期投資を回収</p><p class="msv-stats__note">約98%（購入費が基準）</p></li>
            <li><p class="msv-stats__num"><small class="msv-stats__pre">約</small>53<small>%</small></p><p class="msv-stats__label">1年目の稼働率</p><p class="msv-stats__note">計画の約1.3倍</p></li>
            <li><p class="msv-stats__num">★4.88</p><p class="msv-stats__label">Airbnb の評価</p><p class="msv-stats__note">51件・掲載時点</p></li>
          </ul>
          <figure class="mletter__voice"><blockquote><p class="mletter__q">{e(review["text"])}</p></blockquote><figcaption>NODE Shimoda のゲスト<br>{e(review["who"])}・{e(review["date"])}</figcaption></figure>
          <p class="mletter__more"><a href="media/case-rental-house-inn-first-year.html">下田の宿の運営データを見る {ARROW}</a><a href="{NOTE_STORY_URL}" target="_blank" rel="noopener" data-cta="note-story">開業の体験記（note） {ARROW}</a></p>
        </div>
      </div>
    </section>

    <section class="mlp-sec mlp-sec--soft" id="plans">
      <div class="container">
        <p class="mlp-en reveal">Plans</p>
        <h2 class="mlp-title reveal">プランと条件の目安</h2>
        <div class="mplans__cards mplans__cards--{len(plans)} reveal">
{plan_cards}
        </div>
        {f'<p class="mrisks__hint" aria-hidden="true">横にスワイプして、{len(plans)}つ見比べられます →</p>' if len(plans) > 1 else ""}
        <p class="mplans__note">{e(PLANS[src]["note"])}</p>
      </div>
    </section>

    <section class="mlp-sec">
      <div class="container">
        <p class="mlp-en reveal">Compare</p>
        <h2 class="mlp-title reveal">ほかの方法と、ここが違います</h2>
        <p class="mcmp__legend" aria-hidden="true"><span><b class="mcmp__mark mcmp__mark--good">{mark_svg["◎"]}</b>とてもよい</span><span><b class="mcmp__mark mcmp__mark--ok">{mark_svg["○"]}</b>よい</span><span><b class="mcmp__mark mcmp__mark--bad">{mark_svg["△"]}</b>負担・注意</span><span><b class="mcmp__mark mcmp__mark--none">{mark_svg["×"]}</b>なし</span></p>
        <p class="msv-compare__swipe" aria-hidden="true">表は左右にスライドできます →</p>
        <div class="msv-compare msv-compare--cols reveal">
          <table>
            <thead><tr><th scope="col">比べる<wbr>こと</th>{cmp_head}</tr></thead>
            <tbody>
{cmp_rows}
            </tbody>
          </table>
        </div>
        <p class="msv-compare__note">※ 読み手から見た一般的な傾向の目安です。実際の条件は物件や契約によって変わります。{(" " + e(cmp["note"])) if cmp.get("note") else ""}</p>
        <details class="mlp-fold reveal"><summary>ほかの方法が合うかもしれない方</summary><ul>{fit_no}</ul></details>
      </div>
    </section>

    <section class="mlp-sec mlp-sec--soft">
      <div class="container">
        <p class="mlp-en reveal">Flow</p>
        <h2 class="mlp-title reveal">ご相談からの流れ。<br>ご提案までは無料です</h2>
        <div class="mlp-flow">
{detail_flow(key)}
        </div>
      </div>
    </section>

    <section class="mlp-sec">
      <div class="container mlp-narrow">
        <p class="mlp-en reveal">FAQ</p>
        <h2 class="mlp-title reveal">よくある質問</h2>
        <div class="faq reveal">
{faq_html(sv["faq"] + more["faq_more"])}
        </div>
      </div>
    </section>

    <section class="mlp-sec mlp-sec--final">
      <div class="container mlp-narrow">
        <h2 class="mlp-title reveal">{e(closing_t)}</h2>
        <p class="mlp-lead reveal">{e(closing_d)}</p>
        <div class="mlp-ctarow reveal"><a href="#diag" class="mbtn" data-cta="media-service-bottom">無料で相談する {ARROW}</a><a href="#diag-doc" class="mbtn mbtn--sub" data-cta="media-service-bottom-doc">資料をもらう（無料） {ARROW}</a></div>
        <p class="mlp-final__note">相談・試算は無料。しつこい営業はしません。</p>
      </div>
    </section>

{media_section(cases, eyebrow="Cases", title=more["cases_title"], more=False, keep_order=True)}"""
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": sv["name"], "provider": org_ref(),
           "areaServed": "JP", "description": sv["lead"]},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sv["faq"] + more["faq_more"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"},
              {"@type": "ListItem", "position": 2, "name": "アキヤドのプラン", "item": f"{SITE}/media/plans.html"},
              {"@type": "ListItem", "position": 3, "name": sv["name"]}]}]
    page(f"media/{sv['slug']}.html", f"{sv['name']}｜{sv['eyebrow']}｜アキヤド",
         f"{sv['lead']}相談・お見積りは無料、全国対応です。", body, current="media", jsonld=ld, mnav="plans", cv_category=sv["category"])


def media_company_page():
    """アキヤドの運営会社。誰が書いているか・何を頼めるかを1ページで伝える（会社概要はコーポレートと共通）"""
    rows = company_profile() + [("運営メディア", "アキヤド（空き家と民泊のメディア）"), ("運営している宿", "NODE Shimoda（静岡県下田市・一棟貸し）ほか")]
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
    crumbs = media_crumbs([("アキヤド", "media.html"), ("運営者情報", "")])
    body = f"""{media_hero("About us", "運営者情報", "アキヤドは、宿泊施設の運営と空き家の再生を行う、合同会社RIVIA&CO.が運営しています。", crumbs)}

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
        <div class="msec__head reveal"><div><p class="msec__en">Our inn</p><h2 class="msec__title">運営している宿の一例：NODE Shimoda</h2></div></div>
        <p class="msv-record__lead"><span class="ex-badge">運営施設の一例</span>複数ある運営施設のうちの1つです。</p>
        <p class="msv-record__label">ゲストの声（Airbnbのレビューより抜粋）</p>
        <div class="mvoices">
{reviews}
        </div>
{band}
      </div>
    </section>

{media_cta()}"""
    ld = [{"@context": "https://schema.org", "@type": "AboutPage", "name": "アキヤドの運営者情報", "isPartOf": {"@id": WEBSITE_ID},
           "about": org_ref()},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"},
              {"@type": "ListItem", "position": 2, "name": "運営者情報"}]}]
    # 会社概要の本体はコーポレートの about.html。ここは「メディアを誰が・どう書いているか」のページとして、名前と説明を分ける
    page("media/company.html", "アキヤドの運営者情報｜記事の書き手と監修",
         "空き家と民泊のメディア「アキヤド」の運営者情報です。記事を書く理由と監修者、運営している宿の一例、アキヤドに相談できることを紹介します。運営は合同会社RIVIA&CO.です。",
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
            <p class="mintro__copy reveal" data-delay="1">空き家を売る。活かす。<br>民泊をはじめる。</p>
            <p class="mintro__lead reveal" data-delay="1">自ら宿を運営する私たちが、空き家と民泊の悩みに<br class="pc-only">順を追ってお答えするメディアです。</p>
            <div class="mintro__btns reveal" data-delay="2">
              <a href="media.html" class="btn">アキヤドを見る {ARROW}</a>
            </div>
          </div>
          <a href="media.html" class="mintro__shots reveal" data-delay="1" aria-label="アキヤドを見る">
            <span class="mintro__pc"><span class="mintro__bar" aria-hidden="true"><i></i><i></i><i></i></span><img src="images/media-preview-pc.webp?v={asset_version("images/media-preview-pc.webp")}" alt="アキヤドのトップページ（パソコン表示）" width="1440" height="900" loading="lazy" decoding="async"></span>
            <span class="mintro__sp"><img src="images/media-preview-sp.webp?v={asset_version("images/media-preview-sp.webp")}" alt="アキヤドのトップページ（スマホ表示）" width="520" height="1040" loading="lazy" decoding="async"></span>
          </a>
        </div>
        <ul class="mintro__entries reveal">{entries}</ul>
      </div>
    </section>"""


MEDIA_INTRO_DESC = {
    "sell": "相続した家を手放すときの流れ、税金の特例、放置したときのリスク",
    "use": "家を残したまま宿として活かす方法、貸す契約、改修の考え方",
    "side": "民泊の始め方、制度と届出、開業資金、集客と運営",
    "run": "運営中の宿の数字の見方、予約の増やし方、人手と運営の整え方",
}
