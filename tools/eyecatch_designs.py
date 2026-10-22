"""記事ごとのアイキャッチのデザイン（tools/eyecatch.py が読む）

型を決めて機械的に並べるのではなく、記事ごとに「何を一番大きく見せるか」を決めて組む。
新しい記事を足すときも、ここに1件ずつデザインを書く（書かなければ eyecatch.py の標準デザインになる）。

各項目:
  layout : 組み方（eyecatch.py の LAYOUTS を参照）
  lines  : 見出しの行。[ ] で囲んだ部分を強調する
  sub    : 小さな補足（任意）
  big    : 大きく見せる言葉・数字（giant / number / poster で使う）
  a, b   : 対比の左右（duo で使う）
  color  : 地の色（green / deep / terra / sand / navy / mustard / ink）
  photo  : 写真を記事の写真から変えたいとき（images/photos の名前）
  pos    : 写真の見せる位置（CSS の background-position。例 "30% 50%"）

体験談・数字は記事本文にあるものだけを使う（事実を作らない）。
"""

DESIGNS = {
    # ---- オーナーの事例（取材）: 専用デザイン。顔アイコンと、費用・月商・利益の数字を見せる（数字は各記事の本文にあるものだけ）
    "case-owner-pricing-mistake": dict(layout="case", avatar=1, who="Aさん", lines=["ほぼ満室なのに[赤字]", "単価1.9倍で立て直した"], chips=[("稼働率", "92%→58%"), ("客室単価", "9,800→18,500円"), ("月の売上", "約27→32万円")]),
    "case-owner-diy-cottage": dict(layout="case", avatar=2, who="Bさんご夫婦", lines=["解体200万円の別荘が", "[週末DIY約80万円]で宿に"], chips=[("改修費", "約80万円"), ("月商", "約55万円"), ("月の純利益", "約35万円")]),
    "case-owner-subsidy-akiya": dict(layout="case", avatar=3, who="Cさん", lines=["自己資金100万円で", "空き家を[宿]に"], chips=[("改装の予算", "約450万円"), ("月商", "約45万円"), ("月の純利益", "15〜18万円")]),
    "case-owner-fishing-port": dict(layout="case", avatar=6, who="Dさんご夫婦", lines=["実績ゼロで[融資400万円]", "元・仕出し屋が宿に"], chips=[("工事費用", "約500万円"), ("月商", "60〜70万円"), ("月の純利益", "20〜30万円")]),
    "case-owner-rental-side-business": dict(layout="case", avatar=4, who="Eさん", lines=["[週1〜2時間]で民泊副業", "会社員のまま始めた"], chips=[("初期費用", "約200万円"), ("月商", "約40万円"), ("月の純利益", "12〜15万円")]),
    "case-owner-licensed-akiya": dict(layout="case", avatar=5, who="Fさん", lines=["空き家を[旅館業]で宿に", "初期費用400万円の内訳"], chips=[("初期費用", "約400万円"), ("月商", "平均約55万円"), ("月の純利益", "平均約25万円")]),
    "case-owner-setouchi-cycling": dict(layout="case", avatar=1, who="Gさんご夫婦", lines=["空き店舗を", "[サイクリスト]の宿に"], chips=[("総予算", "約400万円"), ("月商", "40〜45万円"), ("月の純利益", "12〜15万円")]),
    "case-owner-castle-town-nagaya": dict(layout="case", avatar=3, who="Hさんご夫婦", lines=["城下町の[古い長屋]を宿に", "融資の3つの関門"], chips=[("総予算", "約450万円"), ("月商", "45〜55万円"), ("月の純利益", "15〜18万円")]),
    "case-owner-satoyama-airdna": dict(layout="case", avatar=2, who="Iさんご夫婦", lines=["里山の古民家を宿に", "[データ]で融資を通す"], chips=[("総予算", "約350万円"), ("月商", "45〜50万円"), ("月の純利益", "15〜18万円")]),
    "minpaku-chintai-start": dict(layout="poster", big="転貸", lines=["賃貸で民泊を始める", "[承諾書と管理規約]"], color="mustard"),
    "kaishain-minpaku-fukugyo": dict(layout="number", big="20", unit="万円", lines=["会社員の民泊副業", "[就業規則と20万円ルール]"], color="deep"),
    "minpaku-kakutei-shinkoku": dict(layout="poster", big="確定申告", lines=["新法民泊の", "[所得区分と経費]"], color="mustard"),

    # ---- 売る・手放す
    "akiya-inherited-house-to-inn": dict(layout="boxes", lines=["放置された実家が", "[「小さな宿」]に変わる", "理由"]),
    "akiya-3000man-deduction": dict(layout="number", big="3,000", unit="万円", lines=["相続した空き家を売るときの", "[特別控除]"], color="deep"),
    "akiya-law-kanri-fuzen": dict(layout="poster", big="空家法", lines=["改正で、", "[何が変わった？]"], color="mustard"),
    "souzoku-touki-gimuka": dict(layout="frame", lines=["相続登記の[義務化]と", "最初にやること"], color="navy"),
    "akiya-holding-costs": dict(layout="giant", big="維持費", lines=["空き家、持っているだけで", "[毎年いくらかかる？]"]),
    "inherited-house-family-talk": dict(layout="mincho", lines=["相続した実家を", "家族で決める"], sub="話し合いの順番と、決めておくこと"),

    "akiya-demolish-or-renovate": dict(layout="duo", a="解体", b="改修", lines=["空き家は、[壊す？残す？]"]),

    # ---- 物件・改修
    "akiya-bank-guide": dict(layout="marker", lines=["空き家バンクの", "[仕組みと使い方]"], sub="登録・購入の前に知っておきたいこと"),
    "shizuoka-yaizu-akiya-inn": dict(layout="boxes", lines=["観光地でなくても", "[収益物件]になる？"]),
    "kominka-renovation-points": dict(layout="mincho", lines=["古民家を、", "宿に直す"], sub="残すもの・変えるもの", photo="irori-room", pos="50% 62%"),
    "akiya-utilization-options": dict(layout="poster", big="売る？貸す？宿？", lines=["空き家の[活用方法]を比べる"], color="green"),
    "akiya-minpaku-suitability": dict(layout="quote", lines=["その空き家は、", "[民泊に向いている？]"], color="sand", photo="old-town-street", pos="50% 45%"),
    "remote-renovation-tips": dict(layout="frame", lines=["遠方からの", "[改修工事]の進め方"], color="terra", photo="window-garden", pos="50% 55%"),
    "akiya-rate-and-inn": dict(layout="number", big="31.3", unit="%", lines=["下田市の空き家率を、", "[内訳]で読む"], color="deep"),
    "new-build-vs-used-house-inn": dict(layout="duo", a="新築", b="中古", lines=["小さな宿は、[どっちがいい？]"]),

    # ---- 貸す・任せる
    "akiya-lease-types": dict(layout="marker", lines=["空き家を貸すときの", "[契約の種類と違い]"]),
    "minpaku-management-company": dict(layout="type", lines=["住宅宿泊管理業者とは？", "[委託が必要なケース]"], color="sand"),
    "akiyado-what-we-do": dict(layout="giant", big="アキヤド", lines=["が、[できること]"], sub="買取・借り上げから、開業・運営の支援まで"),
    "minpaku-partner-choose": dict(layout="boxes", lines=["相談先・委託先の", "[選び方]"]),

    # ---- 開業・手続き
    "minpaku-vs-ryokan-law": dict(layout="duo", a="民泊新法", b="旅館業", lines=["[どちらで始める？]"]),
    "minpaku-start-steps": dict(layout="number", big="7", unit="STEP", lines=["民泊を始めるまでの", "[7ステップ]"], color="terra"),
    "minpaku-fire-safety": dict(layout="poster", big="消防設備", lines=["民泊・小さな宿の", "[ガイド]"], color="terra"),
    "akiyado-consultation-flow": dict(layout="frame", lines=["相談から開業までの", "[流れ]"], color="green"),

    # ---- お金・税金
    "small-inn-subsidies": dict(layout="giant", big="補助金", lines=["小規模宿で使える", "[支援制度まとめ]"]),
    "inn-startup-funding": dict(layout="type", lines=["小さな宿の開業資金は", "[どう用意する？]"], color="sand"),
    "accommodation-tax": dict(layout="poster", big="宿泊税", lines=["とは？", "[導入が広がる背景]"], color="navy"),
    "minpaku-investment-yield": dict(layout="marker", lines=["不動産投資として見る", "[小さな宿・民泊]"]),
    "minpaku-vs-rental-income": dict(layout="duo", a="民泊", b="賃貸", lines=["[収入の仕組み]の違い"]),

    # ---- 集客・運営
    "airdna-revenue-simulation": dict(layout="giant", big="AirDNA", lines=["で読む、", "[小規模宿の収益と再現性]"]),
    "inn-kpi-basics": dict(layout="poster", big="RevPAR", lines=["稼働率・客室単価と", "[売上を読み解く3つの指標]"], color="ink"),
    "ota-vs-direct-booking": dict(layout="duo", a="予約サイト", b="自社予約", lines=["[どう使い分ける？]"]),
    "cleaning-linen-operations": dict(layout="mincho", lines=["清掃と、", "リネン"], sub="小さな宿の運用ガイド"),
    "listing-photo-tips": dict(layout="boxes", lines=["予約が入る", "[宿のページ]の", "つくり方"]),
    "guest-review-tips": dict(layout="number", big="★5", unit="", lines=["レビューの評価を上げる", "[ゲスト対応]"], color="green"),
    "case-rental-house-inn-first-year": dict(layout="number", big="14", unit="か月", lines=["下田の一軒家を宿に。", "[初期投資を回収]するまで"], color="deep"),
    "minpaku-hard-truth": dict(layout="quote", lines=["「民泊は大変」", "って[本当？]"], color="sand"),
    "minpaku-neighbor-rules": dict(layout="frame", lines=["近隣トラブルを防ぐ", "[ルールづくり]"], color="mustard"),
    "minpaku-off-season": dict(layout="mincho", lines=["閑散期を、", "どう越える"], sub="売上の波をならす工夫", photo="own-fishing-bay", pos="50% 30%"),
    "minpaku-remote-operation": dict(layout="giant", big="遠隔運営", lines=["遠方の物件でも、", "[運営できる？]"]),
    "long-stay-guest-equipment": dict(layout="marker", lines=["長期滞在のゲストに", "[選ばれる設備]"], photo="hotel-room", pos="60% 45%"),

    # ---- 観光と地域
    "japan-tourism-market-data": dict(layout="number", big="5", unit="つの課題", lines=["データで見る日本の観光市場と", "[地方が抱える課題]"], color="navy"),
    "akiya-regional-revitalization": dict(layout="mincho", lines=["空き家活用が、", "地方創生に"], sub="つながる理由", photo="own-breakwater-island", pos="50% 55%"),
    "long-stay-travel-demand": dict(layout="mincho", lines=["暮らすように、", "旅をする"], sub="長期滞在が広がる理由", photo="own-open-sea", pos="50% 45%"),
    "inn-local-economy": dict(layout="boxes", lines=["宿が地域に", "[お金を落とす]", "仕組み"]),
    "inbound-regional-dispersion": dict(layout="giant", big="訪日客を地方へ", lines=["[インバウンドの地方分散]"]),
    "tourism-labor-shortage": dict(layout="quote", lines=["観光業の人手不足を", "[どう乗り越える？]"], color="sand"),
    "kankei-jinko-and-inns": dict(layout="poster", big="関係人口", lines=["と、", "[宿ができること]"], color="green"),
    "akiya-data-9-million": dict(layout="number", big="900", unit="万戸", lines=["データで見る", "[日本の空き家]"], color="ink"),
    "why-akiya-utilization-now": dict(layout="giant", big="なぜ今", lines=["空き家の[活用]が", "注目されるのか"]),
    "akiya-local-resource": dict(layout="mincho", lines=["空き家は、", "地域の資源になる"], sub="まちに人の流れを生む仕組み"),
    "why-minpaku-for-akiya": dict(layout="boxes", lines=["空き家の活用で", "[なぜ民泊]が", "選ばれるのか"]),
    "kominka-stay-value": dict(layout="mincho", lines=["古い家だから", "こその価値"], sub="古民家に泊まるという体験"),
    "kani-shukusho-kyoka-guide": dict(layout="boxes", lines=["簡易宿所の許可", "[広さ・相談先・流れ]", "をやさしく解説"]),
}
