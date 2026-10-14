# 取材事例（case-owner-*）と、内部リンクの差し込み。記事データを直接変えず、作る時に節の末尾へ足す。
# 事実は取材記事（人から受け取った一次情報・2025年9〜12月・オーナー申告）の範囲だけ。確認していないことは書かない。
def _c(slug, text):
    return f'<p class="case-mix">取材したオーナーの例です。{text}詳しくは「<a href="media/{slug[0]}.html">{slug[1]}</a>」で紹介しています。</p>'

MIXINS = {
    "inn-kpi-basics": {"trap": _c(("case-owner-pricing-mistake", "民泊の価格設定で失敗｜ほぼ満室でも赤字から、単価1.9倍で立て直した事例"),
        "稼働率92%でも、清掃が月25回以上かかって実質赤字だったAさんは、単価を9,800円から18,500円に戻して稼働率を58%に落としたところ、月の売上が約27万円から約32万円に増え、清掃は月7回前後になりました（本人の申告）。"),
        "summary": '<p>収益の試算のしかたは、「<a href="media/airdna-revenue-simulation.html">AirDNAで小規模宿の収益をシミュレーション</a>」で紹介しています。</p>'},
    "akiya-demolish-or-renovate": {"renovate": _c(("case-owner-diy-cottage", "築古の別荘を週末DIYで民泊に｜改修費80万円・月の純利益35万円の事例"),
        "解体に200万〜300万円と言われた別荘を、夫婦の週末作業で約半年かけて改修し、改修費約80万円で宿にしたBさんご夫婦の例があります（80万円に許可費用や消防設備が含まれるかは確認していません）。"),
        "summary": '<p>新築と中古の違いは、「<a href="media/new-build-vs-used-house-inn.html">小規模宿は新築と中古どっち？</a>」で比べています。</p>'},
    "small-inn-subsidies": {"case": _c(("case-owner-subsidy-akiya", "空き家を買って民泊に｜補助金と公庫融資を組み合わせた事例"),
        "自己資金100万円に、補助金（本人の申告で約150万円）と日本政策金融公庫の融資200万円を組み合わせ、総額約450万円の改装の予算を確保したCさんの例があります（補助金の受領額と制度の上限の関係は確認していません）。")},
    "inn-startup-funding": {"loan": _c(("case-owner-fishing-port", "元・仕出し屋を民泊に｜公庫融資400万円で改装、月商60〜70万円の事例"),
        "実績ゼロの個人事業主として、観光動向と体験プランまで盛り込んだ事業計画書で、日本政策金融公庫の融資400万円を受けたDさんご夫婦の例があります。")
        + _c(("case-owner-rental-side-business", "会社員の民泊副業｜賃貸で始め、月の純利益12〜15万円・作業は週1〜2時間の事例"),
        "賃貸マンションを借りて民泊にしたEさんは、自己資金50万円と公庫の融資150万円で、初期費用約200万円で始めました。"),
        "plan": '<p>収益の見込みの立て方は、「<a href="media/airdna-revenue-simulation.html">AirDNAで小規模宿の収益をシミュレーション</a>」も参考になります。</p>'},
    "minpaku-off-season": {"prepare": _c(("case-owner-licensed-akiya", "空き家を旅館業で民泊に｜初期費用400万円・月の純利益は平均25万円の事例"),
        "Fさんの宿では、月の純利益が、冬の閑散期は約8万円、夏の繁忙期は約40万円で、平均は約25万円でした。最も悪い月でも続けられるかを確かめておくことが、ポイントだと話しています。")},
    "listing-photo-tips": {"price": _c(("case-owner-pricing-mistake", "民泊の価格設定で失敗｜ほぼ満室でも赤字から、単価1.9倍で立て直した事例"),
        "Aさんは、最初の10件のレビューが集まるまでは低めの価格にし、★4.8以上で10件たまってから適正価格へ戻す、という順番で価格を決めました。")},
    "minpaku-start-steps": {"summary": _c(("case-owner-licensed-akiya", "空き家を旅館業で民泊に｜初期費用400万円・月の純利益は平均25万円の事例"),
        "旅館業の許可を取って空き家を宿にしたFさんは、事前相談から営業開始まで約6か月かかりました。想定外は、消防設備の費用、開業直後の低い稼働、冬の光熱費の3つでした。")
        + '<p>自治体によっては、宿泊者から宿泊税を預かって納める仕組みがあります。「<a href="media/accommodation-tax.html">宿泊税とは？民泊は対象？</a>」で説明しています。</p>'},
    "minpaku-remote-operation": {"delegate": _c(("case-owner-rental-side-business", "会社員の民泊副業｜賃貸で始め、月の純利益12〜15万円・作業は週1〜2時間の事例"),
        "都内で働く会社員のEさんは、清掃と現場の対応を代行業者に任せ、自分の作業は週1〜2時間に収めています。")},
    "minpaku-investment-yield": {"actual": _c(("case-owner-rental-side-business", "会社員の民泊副業｜賃貸で始め、月の純利益12〜15万円・作業は週1〜2時間の事例"),
        "Eさんは、賃貸マンションを借りて民泊にし、初期費用約200万円で、月の純利益は12万〜15万円（本人の申告。範囲は事例ごとに違います）でした。")},
    "long-stay-travel-demand": {"summary": '<p>訪日客数などの全体のデータは、「<a href="media/japan-tourism-market-data.html">データで見る日本の観光市場</a>」で紹介しています。</p>'},
    "why-minpaku-for-akiya": {"caution": '<p>市場の全体像は、「<a href="media/japan-tourism-market-data.html">データで見る日本の観光市場</a>」で紹介しています。</p>'},
    "kominka-renovation-points": {"summary": '<p>新築と中古のどちらにするかは、「<a href="media/new-build-vs-used-house-inn.html">小規模宿は新築と中古どっち？</a>」で比べています。</p>'},
    "akiya-holding-costs": {"summary": '<p>活用が注目されている背景は、「<a href="media/why-akiya-utilization-now.html">なぜ今「空き家の活用」が注目されているのか</a>」で紹介しています。</p>'},
    "akiya-inherited-house-to-inn": {"summary": '<p>活用が注目されている背景は、「<a href="media/why-akiya-utilization-now.html">なぜ今「空き家の活用」が注目されているのか</a>」で紹介しています。</p>'},
    "inherited-house-family-talk": {"split": '<p>活用が注目されている背景は、「<a href="media/why-akiya-utilization-now.html">なぜ今「空き家の活用」が注目されているのか</a>」で紹介しています。</p>'},
}
