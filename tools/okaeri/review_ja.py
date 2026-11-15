# -*- coding: utf-8 -*-
"""日本語のレビュー用ページ（試作にだけ入る。本番の dist には出さない）。"""

# キーワード調査（2026-11-14、米国の Google、月間検索回数と難易度 KD は調査ツールの推定値）
# (グループ, キーワード, 月間検索, KD, 上位の顔ぶれ・見立て, 受けるページ, 状態)
KEYWORDS = [
 ("空き家", "akiya", "3,600", "0", "物件サイト（akiyajapan・allakiyas・akiya2）と体験記。新しい専門サイトが多い", "「akiya とは」の解説記事", "次に書く"),
 ("空き家", "cheap houses in japan", "1,900", "4", "物件一覧サイトが中心。解説記事は少ない", "「安い家の本当の費用」", "次に書く"),
 ("空き家", "buy a house in japan", "1,900", "17", "不動産会社の解説", "「外国人は買えるか」", "次に書く"),
 ("空き家", "akiya japan / akiya houses", "各1,300", "3〜7", "物件サイト", "「akiya とは」", "次に書く"),
 ("空き家", "can foreigners buy property in japan", "1,000", "2", "上位に日本語・ドイツ語・ロシア語のページが混ざり、英語の良い答えが少ない。狙い目", "「外国人は買えるか」", "最優先"),
 ("空き家", "abandoned houses in japan", "1,000", "3", "ニュース・動画", "「akiya とは」", "次に書く"),
 ("空き家", "old house in japan", "1,300", "8", "体験記", "「古い家で暮らす」", "後で"),
 ("空き家", "house prices in japan", "880", "10", "統計・不動産会社", "「安い家の本当の費用」", "後で"),
 ("空き家", "free houses in japan", "480", "0", "ニュース", "「安い家の本当の費用」", "次に書く"),
 ("空き家", "akiya bank", "390", "19", "物件サイト", "「空き家バンクの使い方」", "後で"),
 ("空き家", "買う前に住む（この切り口の語はまだ検索が少ない）", "—", "—", "競合なし。上の記事から読者を受ける", "空き家を買う前に1か月住む", "公開準備"),
 ("長期滞在", "rent a house in japan / japan house rental", "各1,300", "41", "Reddit・Vrbo・移住者向けメディア。難しいが、予約に最も近い", "「日本で家を1か月借りる」", "最優先"),
 ("長期滞在", "japan digital nomad visa", "880", "2", "1位は外務省。体験記（tokyodev など）が上位に入れている", "「デジタルノマドビザと、どの町に住むか」", "次に書く"),
 ("長期滞在", "digital nomad visa japan", "720", "—", "同上（同じ記事で受ける）", "同上", "次に書く"),
 ("長期滞在", "best places to live in japan", "590", "0", "移住者向けメディア", "「東京の外で暮らす町の選び方」", "後で"),
 ("長期滞在", "monthly rental japan", "170", "16", "マンスリーマンション会社", "「日本で家を1か月借りる」", "最優先"),
 ("長期滞在", "how long can i stay in japan", "170", "3", "大使館・ビザ代行", "「日本に何日滞在できるか」", "後で"),
 ("長期滞在", "long term stay japan / one month in japan", "50〜90", "0〜18", "少ないが目的がはっきりしている", "「日本で家を1か月借りる」", "最優先"),
 ("町と地域", "izu peninsula", "12,100", "7", "japan-guide・Wikipedia・日本政府観光局・Klook。1ページ目は遠い", "伊豆半島のページ", "公開準備"),
 ("町と地域", "japan countryside", "9,900", "6", "個人ブログ・ツアー会社。大手が少ない", "「日本の田舎に滞在する」", "次に書く"),
 ("町と地域", "rural japan", "6,600", "12", "同上", "同上", "次に書く"),
 ("町と地域", "shimoda / shimoda japan", "各5,400", "21", "Wikivoyage・静岡県公式・Tripadvisor（人名の「Shimoda」の検索も含む数字）", "「下田ガイド」", "次に書く"),
 ("町と地域", "kinmedai", "4,400", "0", "Pinterest・写真素材サイト・動画。まともな解説がほぼない。狙い目", "金目鯛の記事", "公開準備"),
 ("町と地域", "day trips from tokyo", "3,600", "0", "大手旅行メディア（数字より難しい）", "東京から伊豆半島へ", "公開準備"),
 ("町と地域", "small towns in japan", "1,900", "7", "個人ブログ", "「日本の田舎に滞在する」", "次に書く"),
 ("町と地域", "shuzenji / shuzenji onsen", "各1,000", "0", "旅館・観光サイト", "「修善寺ガイド」", "物件が決まったら"),
 ("町と地域", "surfing in japan", "1,000", "0", "サーフィンメディア", "「下田でサーフィン」", "後で"),
 ("町と地域", "izu peninsula from tokyo / tokyo to izu peninsula", "各260", "7", "japan-guide・ブログ", "東京から伊豆半島へ", "公開準備"),
 ("町と地域", "onsen towns near tokyo / best beaches near tokyo", "260 / 210", "0", "旅行メディア", "伊豆の記事から受ける", "後で"),
 ("町と地域", "yaizu / yaizu japan", "110 / 170", "0", "ほぼ空白", "「焼津ガイド」", "開業に合わせて"),
]

# これから書く記事（優先順）
ROADMAP = [
 ("1", "Can foreigners buy property in Japan?（外国人は日本の家を買えるか）", "can foreigners buy property in japan 1,000／buy a house in japan 1,900", "家を持つ", "上位が弱い。答えを最初の1文で言い切り、登記・税・ビザの関係を出典つきで"),
 ("2", "Renting a house in Japan for a month（日本で家を1か月借りる）", "rent a house in japan 1,300／monthly rental japan 170", "一年の一部を暮らす", "予約にいちばん近い記事。マンスリー・民泊・賃貸の違いを表に。自社の家への導線を強く"),
 ("3", "What is an akiya?（akiya とは）", "akiya 3,600／akiya japan 1,300／abandoned houses 1,000", "家を持つ", "空き家テーマの親記事。定義・数字・種類。ほかの空き家記事へつなぐ"),
 ("4", "Cheap and free houses in Japan: the real cost（安い家・無料の家の本当の費用）", "cheap houses in japan 1,900／free houses in japan 480", "家を持つ", "下田の改修費（約410万円）など、公開してよい自社の数字が強みになる"),
 ("5", "Japan’s digital nomad visa, and where to base yourself（デジタルノマドビザと住む町）", "japan digital nomad visa 880＋720", "一年の一部を暮らす", "制度は外務省・入管の一次情報で。後半を「東京の外の拠点」にして差をつける"),
 ("6", "Shimoda guide for a week or longer（下田に1週間以上いる人のガイド）", "shimoda japan 5,400／shimoda beaches 210", "長めに旅する＋場所（伊豆）", "店・スーパー・バス・浜を、運営者の案内として。写真が必須"),
 ("7", "The Japanese countryside for a longer stay（日本の田舎に長く滞在する）", "japan countryside 9,900／rural japan 6,600／small towns in japan 1,900", "長めに旅する", "検索は多いが目的が広い。「観光ではなく滞在」に絞った町の選び方"),
 ("8", "Living in an old Japanese house（古い日本の家で暮らす）", "old house in japan 1,300", "家を持つ", "冬の寒さ・古い配線・湿気。下田の開業で分かったことが使える"),
 ("9", "How long can you stay in Japan?（日本に何日滞在できるか）", "how long can i stay in japan 170", "一年の一部を暮らす", "短い記事。90日・デジタルノマド6か月を表で"),
 ("10", "Akiya banks explained（空き家バンクの使い方）", "akiya bank 390", "家を持つ", "アキヤドの空き家バンク記事を、海外の読み手向けに書き直す"),
]

DONE = [
 ("デザインの作り直し（2026-11-14）", "写真全面のFVと目的別の入口3つ、スマホ用メニュー、入口別のページ（Stay longer・Live part-time・Own a home）と場所のページ、記事の見出し写真・目次・読了時間・関連記事のカード・NODE Shimoda の案内。海外の不動産・長期滞在メディア（akiyajapan.com・Tokyo Cheapo など）の、カテゴリと読了時間を冒頭に出す・記事の途中と最後に予約や物件への案内を置く作りを取り入れました"),
 ("読み手の入口の分け方（2026-11-14 見直し）", "「どこまで日本に深く関わるか」の1本の軸で3つに分けました。① Stay longer＝旅行者として1週間〜1か月（長めに旅する）② Live part-time＝数か月・毎年・仕事をしながら（一年の一部を暮らす）③ Own a home＝空き家を買う・直す・運営する（家を持つ）。記事は必ずどれか1つに入れ、ほかの段階にも役立つ記事は一覧の「こちらも役立つ」に出します。場所（伊豆など）は別の軸として、メニューと記事のラベルで分けました。①→②→③は、自社の宿に泊まる人が、やがて二拠点や空き家の購入に進む流れとも重なります"),
 ("テーマ別ページの検索への載せ方", "メニューの入口として3つとも作りますが、記事が3本そろうまでは noindex（検索に載せない）にして sitemap からも外しています。中身の薄い一覧ページが検索に出ると、サイト全体の評価を下げるためです"),
 ("ページごとの実URL", "rivia-co.com/noki/guides/kinmedai.html のように、1記事1URLにしました。アキヤドと同じドメインの下に置き、URL の形（.html）もそろえています"),
 ("title と説明文", "全ページに固有の title（60字以内）と説明文（110〜160字）。狙う語を前半に置きました"),
 ("正規URL（canonical）とトップへのリンク", "トップへのリンクは / にそろえています（アキヤドで /index.html との食い違いが出た点を先に避けました）"),
 ("構造化データ", "サイト名の宣言（WebSite）はドメインのトップ（アキヤド側）だけにして、Noki には置いていません。全ページにパンくず、記事に Article と FAQPage、一覧に CollectionPage。FAQ は本文と同じ文から自動で作ります"),
 ("sitemap・robots.txt・llms.txt", "Noki 用の sitemap（/noki/sitemap.xml）を作り、アキヤドの robots.txt と llms.txt に案内を足しました"),
 ("SNS で共有したときの画像（OGP）", "記事ごとに題名入りの画像を自動で作ります（1200×630）"),
 ("内部リンク", "パンくず、記事どうしの関連リンク、伊豆のページと記事の相互リンク、フッターの共通メニュー"),
 ("日本語レビュー版の扱い", "本番には出力しません。試作でだけ見られます"),
 ("公開前チェック", "seo_check.py が、title・説明文の長さと重複、h1、リンク切れ、構造化データ、sitemap の食い違い、黄色い枠の残りを点検します"),
 ("薄いページを作らない仕組み", "テーマ別の一覧ページは、公開記事が3本以上になったテーマだけ自動で作ります"),
 ("アキヤドのリポジトリに同居", "tools/okaeri/ が元データと生成スクリプト、noki/ が公開フォルダです。アキヤドのビルドと点検には影響しません（両方の点検がエラー0になることを確認済み）"),
]

TODO = [
 ("黄色い枠を埋める", "店・回線速度・料金など。残っている間は seo_check.py が公開不可にします"),
 ("写真を足す", "NODE Shimoda のリビングと海の写真を入れました。金目鯛、下田の町と浜、キッチン・ワークデスク・外観の自社撮影の写真が足りません"),
 ("英語を母語とする人の確認", "3記事と固定ページ"),
 ("Search Console に sitemap を追加", "rivia-co.com のプロパティに https://rivia-co.com/noki/sitemap.xml を追加で送信します（Bing も同じ）。検索結果のサイト名は RIVIA&CO. になります"),
 ("アキヤド側から Noki へリンクを張る", "フッターや会社概要に「English: Noki」のリンクを1つ置くと、同じドメインの評価が流れ、Google も見つけやすくなります。いまは sitemap でしか見つけられません"),
 ("GA4 で分けて見る", "アキヤドと同じ測定IDを入れてあります。レポートでは、ページのパスが /noki で始まるものに絞ると Noki だけを見られます"),
 ("メール登録・問い合わせをつなぐ", "いまは見た目だけです。アキヤドの Google Apps Script の仕組みを流用できます"),
 ("外からのリンクを用意する", "こちらから NODE Shimoda の施設サイトへのリンクは入れました。逆向きに、NODE Shimoda の施設サイト、Airbnb の紹介文、RIVIA&CO. のサイト、Instagram から。新しいドメインは、外からのリンクがないと Google がなかなか読みに来ません"),
 ("記事を一度に出しすぎない", "アキヤドでは、新しいドメインで78ページを一気に出して69ページが「検出 - インデックス未登録」になりました。最初は3記事＋固定ページで出し、週1〜2本ずつ足すのが安全です"),
]

FROM_AKIYADO = [
 "サイトは生成スクリプトで作り、HTML を直接書き換えない（記事はデータ、build.py が全ページを作る）",
 "seo_check.py でエラー0を確かめてから公開する",
 "WebSite の宣言はトップだけ。ほかのページはパンくずを「Home」から始める",
 "トップへのリンクは / にそろえる。sitemap に noindex のページを載せない",
 "記事の形：冒頭の要点、疑問形の見出しとすぐの答え、数字に出典と時点、FAQ、出典一覧",
 "各節は、その節だけ読んでも意味が通るように書く（AI は段落単位で引用するため）",
 "筆者欄・相談の案内には data-nosnippet を付け、検索結果の説明文に出ないようにする",
 "robots.txt で AI のクローラーを許可し、llms.txt で案内する",
 "事実を作らない。自社の体験は「確認済み」のものだけ使い、未確認は黄色い枠に残す",
 "更新日は、内容を実際に直したときだけ変える",
]

HOME_STRINGS = [
 ("Live in small-town Japan for a month.", "日本の小さな町に、1か月暮らしてみる。（FVの見出し）"),
 ("Homes for a week, a month or a season, and straight answers about visas, old houses and daily life outside the big cities, from the people who run them.", "1週間、1か月、ひと季節泊まれる家と、ビザ・古い家・大都市の外での暮らしについての率直な答え。家を運営している本人たちから。"),
 ("Where do I start? ／ See our Shimoda home", "どこから読めばいい？／下田の家を見る（ボタン）"),
 ("How deep do you want to go?", "日本とどこまで深く関わりたい？（入口の見出し）"),
 ("A longer trip ／ Living here part of the year ／ Owning a home here", "長めの旅（1週間〜1か月）／一年の一部を暮らす（数か月・毎年・仕事をしながら）／家を持つ（空き家を買う・直す・運営する）"),
 ("Start here", "まずはここから（おすすめ記事）"),
 ("A house to come back to", "また帰ってきたくなる家（NODE Shimoda の紹介）"),
 ("Guides you can check", "確かめられるガイド（家を運営している／数字には出典／内容を直したときだけ日付を変える）"),
 ("One email when a new home opens", "新しい家が開いたら、メールを1通だけ"),
]

ABOUT_STRINGS = [
 ("Who runs Noki?", "Noki は誰が運営しているか"),
 ("Noki is run by RIVIA&CO. LLC, a company based in Tokyo that renovates older houses in regional Japan and runs them as places to stay.", "Noki は、東京に本社を置く合同会社RIVIA&CO.が運営しています。地方の古い家を改修し、宿として運営している会社です。"),
 ("Our first home is in Shimoda, on the Izu Peninsula. We are preparing homes in Shuzenji and Yaizu.", "1軒目の家は伊豆半島の下田にあります。修善寺と焼津でも準備を進めています。"),
 ("Why “Noki”?", "なぜ Noki という名前か"),
 ("Noki (軒) are the eaves of a Japanese house. Swallows build their nests under them and often come back to the same one each spring. It’s also the word Japanese uses to count houses.", "軒（のき）は、日本の家の軒先のこと。ツバメはその下に巣を作り、毎年春に同じ巣へ帰ってくることがよくあります。家を「一軒、二軒」と数えるときの言葉でもあります。"),
 ("How are the guides written?", "記事の作り方"),
 ("Every figure and rule links to its source… / We say which parts are our own experience… / We change the date only when the content changes… / We do not sell houses or give legal advice…", "数字と制度には出典のリンクを付ける／自分たちの体験はそうと分かるように書く／更新日は内容を直したときだけ変える／家の売買や法律の助言はしない"),
]
