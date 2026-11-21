# -*- coding: utf-8 -*-
"""Noki の記事・ページのデータ。HTML は直接書き換えず、ここを直して build.py を実行する。

本文で使える記法:
  [[s:キー,キー]]   出典を（リンク; リンク）の形で入れる
  [[a:キー]]        出典を文中リンクとして入れる（かっこなし）
  [[l:ページID|文字]] サイト内リンク（本番は実URL、試作は #ページID に変わる）
  [[img:名前|代替テキスト|説明]] 写真（photos/ の <名前>-1200.webp と -640.webp）
  [[ed:文章]]       公開前に運営者の一次情報で埋める箇所（残っていると seo_check が公開不可にする）
"""

# ---------------------------------------------------------------- 出典
# key: (URL, 英語の短い名前, 日本語の短い名前, 出典一覧に出す名前)
SOURCES = {
    "shimoda_kanko_kinme": ("https://www.shimoda-city.info/kinem", "Shimoda Tourism Association", "下田市観光協会（下田の金目鯛）", "Shimoda Tourism Association: Shimoda kinmedai (checked November 2026)"),
    "node_site": ("https://nodeshimoda.com/", "NODE Shimoda", "NODE Shimoda 公式サイト", "NODE Shimoda official site (checked November 2026)"),
    "node_room": ("https://nodeshimoda.com/room", "NODE Shimoda (room)", "NODE Shimoda 公式サイト（客室・設備）", "NODE Shimoda official site: room and facilities (checked November 2026)"),
    "shimoda_news": ("https://www.city.shimoda.shizuoka.jp/file/広報しもだ平成28年6月号16頁.pdf",
                     "Shimoda City newsletter, June 2016", "広報しもだ 2016年6月号", "Shimoda City newsletter, June 2016"),
    "pref": ("https://www.pref.shizuoka.jp/sangyoshigoto/suisan/suisangyo/uocching/1003397/1043925/1028101.html",
             "Shizuoka Prefecture", "静岡県", "Shizuoka Prefecture: Ichiba no Shokudo Kinmetei"),
    "tabimag": ("https://tabi-mag.jp/kinmefes/", "Tabi-mag", "旅マガジン", "Tabi-mag: Shimoda Kinme Matsuri"),
    "tvtokyo": ("https://www.tv-tokyo.co.jp/adomachi/backnumber/20140315/100043.html",
                "TV Tokyo, 2014", "テレビ東京 2014年", "TV Tokyo, Ado-machi: Izu Shimoda (2014)"),
    "rej": ("https://resources.realestate.co.jp/buy/what-restrictions-are-there-on-foreigners-buying-a-home-in-japan-compared-to-other-countries/",
            "Real Estate Japan", "Real Estate Japan", "Real Estate Japan: restrictions on foreign buyers"),
    "jg6305": ("https://japan-guide.com/e/e6305.html", "japan-guide.com", "japan-guide.com", "japan-guide.com: Getting to Izu Peninsula"),
    "jg6311": ("https://japan-guide.com/e/e6311.html", "japan-guide.com", "japan-guide.com", "japan-guide.com: Shuzenji access"),
    "jg6322": ("https://japan-guide.com/e/e6322.html", "japan-guide.com", "japan-guide.com", "japan-guide.com: Izu beaches"),
    "jnto": ("https://www.japan.travel/en/spot/1273/", "JNTO", "日本政府観光局", "JNTO: Shirahama Chuo Beach"),
    "tdn": ("https://www.thedigitalnomad.asia/travel-tips/shimoda-for-digital-nomads/", "The Digital Nomad Asia",
            "The Digital Nomad Asia", "The Digital Nomad Asia: Shimoda for Digital Nomads"),
    "stat_housing2023": ("https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf", "Statistics Bureau of Japan", "総務省統計局",
                         "Statistics Bureau of Japan: 2023 Housing and Land Survey, final basic tabulation (2024)"),
    "isa_nomad_en": ("https://www.moj.go.jp/isa/applications/status/designatedactivities53_00001.html", "Immigration Services Agency",
                     "出入国在留管理庁", "Immigration Services Agency: Designated Activities (Digital Nomad)"),
    "isa_nomad_list": ("https://www.moj.go.jp/isa/content/001416932.pdf", "Immigration Services Agency (country list)", "出入国在留管理庁（対象の国・地域）",
                       "Immigration Services Agency: Eligible countries and regions for the digital nomad status"),
    "mof_fefta2026": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/gaitame/recent_revised/gaitamehou_20260220.html",
                      "Ministry of Finance", "財務省", "Ministry of Finance: Revision of reporting rules under the Foreign Exchange Act (20 February 2026)"),
    "mof_realprop_faq": ("https://www.mof.go.jp/policy/international_policy/gaitame_kawase/real_property/FAQ_J.pdf", "Ministry of Finance (FAQ)",
                         "財務省（FAQ）", "Ministry of Finance: FAQ on reports of real property acquisition (June 2026)"),
    "moj_nationality": ("https://www.moj.go.jp/content/001470076.pdf", "Ministry of Justice", "法務省",
                        "Ministry of Justice: Notice on recording nationality in property registration (4 September 2026)"),
    "cao_land_bill": ("https://www.cao.go.jp/houan/222/index.html", "Cabinet Office", "内閣府", "Cabinet Office: Bills submitted to the 222nd Diet session"),
    "minamialps_trial": ("https://www.city.minami-alps.yamanashi.jp/docs/12876.html", "Minami-Alps City", "南アルプス市",
                         "Minami-Alps City: Trial homes for people considering a move"),
    "shizuoka_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000050.html", "Shizuoka City", "静岡市",
                       "Shizuoka City: Trial homes for people considering a move"),
    "cao_land_bill_outline": ("https://www.cao.go.jp/houan/pdf/222/222_1gaiyou.pdf", "Cabinet Office (bill outline)", "内閣府（法案の概要）",
                              "Cabinet Office: Outline of the bill to amend the Act on the Review and Regulation of the Use of Real Estate around Important Facilities and on Remote Territorial Islands (2026)"),
    "shizuoka_long_trial": ("https://www.city.shizuoka.lg.jp/ijuteiju/s000158.html", "Shizuoka City (long-term)", "静岡市（長期）",
                            "Shizuoka City: Long-term trial homes for people moving to the city"),
    "jre_tt_tokyo": ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetables", "JR東日本の時刻表",
                     "JR East timetables from Tokyo Station: Tokaido Shinkansen and Tokaido, Ito and Izukyu lines (November 2026)"),
    "jfa_kinme_2021": ("https://www.pref.kanagawa.jp/documents/83073/siryou4-1.pdf", "Fisheries Agency, 2021", "水産庁 2021年",
        "Fisheries Agency: Pacific splendid alfonsino — FY2021 stock assessment and wide-area management (committee papers, November 2021)"),
    "chiba_kinme_r6": ("https://www.pref.chiba.lg.jp/gyoshigen/sigenhyoka/documents/01-r6kinme.pdf", "Chiba Prefecture, 2025", "千葉県 2025年",
        "Chiba Prefecture: Coastal fisheries resource assessment FY2024 — splendid alfonsino"),
    "shizuoka_kinme_fat": ("https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/025/667/06kinme.pdf", "Shizuoka Prefecture (fisheries research)", "静岡県（水産技術研究所）",
        "Shizuoka Prefecture: A new season for kinmedai based on fat content"),
    "tokyo_kinme_tag": ("https://www.ifarc.metro.tokyo.lg.jp/watch/uploads/e1b51dd9a8029f8a3c05613d0c07008c.pdf", "Tokyo Metropolitan Government", "東京都",
        "Tokyo Metropolitan Islands Area Research and Development Center: Tagged kinmedai report No. 217 (2019)"),
    "tokushima_akamutsu": ("https://www.pref.tokushima.lg.jp/file/attachment/175834.pdf", "Tokushima Prefecture", "徳島県",
        "Tokushima Prefecture: Akamutsu (nodoguro) catch and stock status (2015)"),
    "kyoto_akamutsu": ("https://www.pref.kyoto.jp/kaiyo/documents/akamutu.pdf", "Kyoto Prefecture", "京都府",
        "Kyoto Prefecture: Akamutsu (blackthroat seaperch)"),
    "ibaraki_akamutsu": ("https://www.pref.ibaraki.jp/nourinsuisan/suishi/teichaku/documents/r7akamutu.pdf", "Ibaraki Prefecture", "茨城県",
        "Ibaraki Prefectural Fisheries Experimental Station: Akamutsu, habitat depth (2026)"),
    "mhlw_mercury2010": ("https://www.mhlw.go.jp/topics/bukyoku/iyaku/syoku-anzen/suigin/dl/index-a.pdf", "Ministry of Health, Labour and Welfare", "厚生労働省",
        "MHLW: Advice for pregnant women on fish and mercury (revised June 2010)"),
    "fishbase_beryx": ("https://www.fishbase.se/summary/1320", "FishBase", "FishBase",
        "FishBase: Beryx splendens, splendid alfonsino"),
    "fishbase_nodoguro": ("https://fishbase.se/summary/4599", "FishBase", "FishBase",
        "FishBase: Doederleinia berycoides, blackthroat seaperch"),
    "shimoda_kanko_event": ("https://www.shimoda-city.info/event", "Shimoda Tourism Association (events)", "下田市観光協会（イベント）",
                            "Shimoda Tourism Association: Events calendar (checked November 2026)"),
    "shimoda_kanko_gift": ("https://www.shimoda-city.info/gift", "Shimoda Tourism Association (shopping)", "下田市観光協会（買う・おみやげ）",
                           "Shimoda Tourism Association: Shopping and souvenirs (checked November 2026)"),
    "pref_izu_gyokyo_shop": ("https://www.pref.shizuoka.jp/sangyoshigoto/suisan/suisangyo/uocching/1003392/1043930/1028021.html", "Shizuoka Prefecture (fish shop)",
                             "静岡県（伊豆漁協ベイステージ直売所）", "Shizuoka Prefecture: Izu Fisheries Cooperative Bay Stage shop (updated April 2025)"),
    "node_access": ("https://nodeshimoda.com/access", "NODE Shimoda (access)", "NODE Shimoda 公式サイト（アクセス）",
                    "NODE Shimoda official site: access (checked November 2026)"),
    "shugiin_bill18": ("https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/keika/1DE36CA.htm", "House of Representatives", "衆議院（議案審議経過情報）",
                       "House of Representatives: Progress of cabinet bill no. 18, 222nd Diet session (checked 16 November 2026)"),
    "jnto_visa": ("https://www.japan.travel/en/plan/visa-info/visa-immigration/", "JNTO", "日本政府観光局（入国とビザ）",
                  "JNTO: Entry into Japan and visa information (checked November 2026)"),
    "shimoda_stay_subsidy": ("https://city.shimoda.shizuoka.jp/file/下田市移住希望者滞在費補助金交付要綱.pdf", "Shimoda City", "下田市（移住希望者滞在費補助金交付要綱）",
                             "Shimoda City: Rules for the stay subsidy for people considering a move (amended March 2026)"),
    "jnto_nomad": ("https://www.japan.travel/en/plan/digital-nomad-visa/", "JNTO", "日本政府観光局（デジタルノマドビザ）",
                   "JNTO: Digital Nomad Visa (checked November 2026)"),
    "egov_immig_act": ("https://laws.e-gov.go.jp/law/326CO0000000319", "Immigration Control Act", "出入国管理及び難民認定法（e-Gov法令検索）",
                       "Immigration Control and Refugee Recognition Act, Articles 5, 7, 7-2, 19, 19-3, 20, 21, 24, 24-3, 70 and Appended Table I (e-Gov, version in force 1 October 2026)"),
    "egov_immig_rules": ("https://laws.e-gov.go.jp/law/356M50000010054", "Immigration Control Act ordinance", "出入国管理及び難民認定法施行規則（e-Gov法令検索）",
                         "Ordinance for Enforcement of the Immigration Control and Refugee Recognition Act, Article 19-5 (e-Gov, version in force 1 October 2026)"),
    "soumu_juki": ("https://www.soumu.go.jp/main_sosiki/jichi_gyousei/c-gyousei/zairyu/english/index.html", "Ministry of Internal Affairs and Communications",
                   "総務省（外国人住民の住民基本台帳制度）", "Ministry of Internal Affairs and Communications: Basic Resident Registration System for foreign residents"),
    "egov_nhi_rules": ("https://laws.e-gov.go.jp/law/333M50000100053", "National Health Insurance Act ordinance", "国民健康保険法施行規則（e-Gov法令検索）",
                       "Ordinance for Enforcement of the National Health Insurance Act, Article 1 (e-Gov, version in force 1 October 2026)"),
    "mlit_foreign_rental": ("https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000017.html", "Ministry of Land, Infrastructure, Transport and Tourism",
                            "国土交通省（外国人の民間賃貸住宅入居円滑化ガイドライン）",
                            "MLIT: Guideline for Facilitating Looking for and Moving in Rental Housing for Foreign Nationals"),
    "nta_2875": ("https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2875.htm", "National Tax Agency", "国税庁（タックスアンサー No.2875）",
                 "National Tax Agency: Tax Answer No.2875, residents and non-residents (law as of 1 April 2026)"),
    "nta_nonresident": ("https://www.nta.go.jp/english/taxes/individual/12006.htm", "National Tax Agency", "国税庁（非居住者の課税）",
                        "National Tax Agency: No.12006 Tax on the income of a non-resident"),
    "soumu_ftth_2025": ("https://www.soumu.go.jp/main_content/001088979.xlsx", "MIC, 2025", "総務省（令和6年度末 FTTH世帯カバー率）",
                        "Ministry of Internal Affairs and Communications: Fibre household coverage by prefecture and municipality, end of March 2025"),
    "jnto_medical": ("https://www.jnto.go.jp/emergency/eng/mi_guide.html", "JNTO", "日本政府観光局（医療機関の検索）",
                     "JNTO: Guide for when you are feeling ill (medical institution search)"),
    "jta_minpaku_overview": ("https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/index_en.html", "Japan Tourism Agency", "観光庁（民泊制度ポータル）",
                             "Japan Tourism Agency, Minpaku portal: What is private lodging? (checked November 2026)"),
    "jta_minpaku_act": ("https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/law1_en.html", "Japan Tourism Agency (Private Lodging Business Act)", "観光庁（住宅宿泊事業法とは）",
                        "Japan Tourism Agency, Minpaku portal: About the Private Lodging Business Act (checked November 2026)"),
    "jta_minpaku_users": ("https://www.mlit.go.jp/kankocho/minpaku/environment_en.html", "Japan Tourism Agency (for guests)", "観光庁（安心できる民泊環境）",
                          "Japan Tourism Agency, Minpaku portal: Safety-assured private lodging (checked November 2026)"),
    "jta_minpaku_illegal": ("https://www.mlit.go.jp/kankocho/minpaku/announcement.html", "Japan Tourism Agency (illegal minpaku)", "観光庁（違法民泊の利用はやめましょう）",
                            "Japan Tourism Agency: To guests — please don’t use illegal minpaku (checked November 2026)"),
    "jta_listing_rules": ("https://www.mlit.go.jp/kankocho/content/001218228.pdf", "Japan Tourism Agency, 2018", "観光庁 2018年（違法物件の掲載防止）",
                          "Japan Tourism Agency: Main points of the measures to prevent illegal properties on booking sites (2018)"),
    "jta_listing_page": ("https://www.mlit.go.jp/kankocho/minpaku/business/mediation/prevention.html", "Japan Tourism Agency (booking sites)", "観光庁（違法物件の掲載の防止について）",
                         "Japan Tourism Agency: Preventing illegal listings on booking sites (checked November 2026)"),
    "jta_cancel_2018": ("https://www.mlit.go.jp/kankocho/content/001244950.pdf", "Japan Tourism Agency, June 2018", "観光庁 2018年6月",
                        "Japan Tourism Agency: Handling of reservations at illegal properties after the Private Lodging Business Act took effect (1 June 2018)"),
    "jta_short_lease_2018": ("https://www.mlit.go.jp/kankocho/content/001260338.pdf", "Japan Tourism Agency and MHLW, 2018", "観光庁・厚生労働省 2018年",
                             "Japan Tourism Agency and Ministry of Health, Labour and Welfare: Handling of short-term rental properties by booking sites (6 November 2018)"),
    "mhlw_passport": ("https://www.mhlw.go.jp/content/000659685.pdf", "Ministry of Health, Labour and Welfare, 2020", "厚生労働省 2020年",
                      "MHLW: Published reply on storing passport copies with the guest register (April 2020)"),
    "mlit_foreign_rental_qa": ("https://www.mlit.go.jp/common/001265432.pdf", "Ministry of Land, Infrastructure, Transport and Tourism", "国土交通省（外国人の民間賃貸住宅入居円滑化ガイドライン）",
                            "MLIT: Guideline for facilitating rental housing for foreign nationals, chapter 2 (Q&A)"),
    "mlit_fixed_term": ("https://www.mlit.go.jp/jutakukentiku/house/teishaku/111215-4.htm", "MLIT (fixed-term leases)", "国土交通省（定期借家権Q&A）",
                        "MLIT: Q&A on fixed-term building leases"),
    "estat_rent_2025": ("https://www.e-stat.go.jp/dbview?sid=0003420453", "Statistics Bureau of Japan, 2025", "総務省統計局 小売物価統計調査 2025年",
                        "Statistics Bureau of Japan: Retail Price Survey, annual average prices 2025 — private rent"),
    "stat_rent_note": ("https://www.stat.go.jp/data/kouri/doukou/2024np/pdf/riyou2024.pdf", "Statistics Bureau of Japan (survey notes)", "総務省統計局（小売物価統計調査 利用上の注意）",
                       "Statistics Bureau of Japan: Retail Price Survey, notes for users 2024"),
    "shimoda_gomi": ("https://www.city.shimoda.shizuoka.jp/category/020100gomi_recycle/110876.html", "Shimoda City", "下田市（家庭ごみの分け方・出し方）",
                     "Shimoda City: How to sort and put out household rubbish (in Japanese)"),
    "izukyu_fares": ("https://www.izukyu.co.jp/fares/index.php", "Izukyu", "伊豆急行（各駅運賃表）",
                     "Izu Kyuko Railway: Fares between stations (revised 14 March 2026)"),
    "izukyu_express": ("https://www.izukyu.co.jp/fares/express.php", "Izukyu (express charges)", "伊豆急行（特急・新幹線料金）",
                       "Izu Kyuko Railway: Limited express, Green Car and Shinkansen charges (for journeys from 1 February 2025, checked November 2026)"),
    "izuhakone_fares": ("https://www.izuhakone.co.jp/sunzudaiyu/zunzu_sub_nav/schedule/p010102.html", "Izuhakone Railway (fares)",
                        "伊豆箱根鉄道（運賃表）", "Izuhakone Railway: Fare table for the Sunzu Line (checked November 2026)"),
    "izuhakone_tt": ("https://www.izuhakone.co.jp/sunzudaiyu/sunzu-recommendation-article/p010438.html", "Izuhakone Railway (timetable)",
                     "伊豆箱根鉄道（駿豆線の時刻表）", "Izuhakone Railway: Sunzu Line timetable (revised 15 March 2025, checked November 2026)"),
    "izuhakone_fare2026": ("https://www.izuhakone.co.jp/izu-group/izu-news/p010993.html", "Izuhakone Railway (fare application)",
                           "伊豆箱根鉄道（運賃の改定申請）", "Izuhakone Railway: Application to revise fares (15 October 2026)"),
    "jrp_route": ("https://japanrailpass.net/en/about_jrp/route/", "JAPAN RAIL PASS (scope of validity)", "JAPAN RAIL PASS 公式（使える範囲）",
                  "JAPAN RAIL PASS official site: Scope of validity, including JR trains running through non-JR lines (checked November 2026)"),
    "jrp_conditions": ("https://japanrailpass.net/en/use/conditions-for-use/", "JAPAN RAIL PASS (conditions of use)", "JAPAN RAIL PASS 公式（利用条件）",
                       "JAPAN RAIL PASS official site: Conditions for use (current as of April 2026)"),
    "jrp_vehicle": ("https://japanrailpass.net/en/about_jrp/vehicle/", "JAPAN RAIL PASS (trains and cars)", "JAPAN RAIL PASS 公式（使える列車と車両）",
                    "JAPAN RAIL PASS official site: Trains and cars you can use (checked November 2026)"),
    "jrp_price": ("https://japanrailpass.net/en/purchase/price/", "JAPAN RAIL PASS (prices)", "JAPAN RAIL PASS 公式（値段）",
                  "JAPAN RAIL PASS official site: Prices (checked November 2026)"),
    "jrp_eligibility": ("https://japanrailpass.net/en/about_jrp/riyou/", "JAPAN RAIL PASS (who can use it)", "JAPAN RAIL PASS 公式（使える人）",
                        "JAPAN RAIL PASS official site: Eligibility (checked November 2026)"),
    "tokaibus_highway": ("https://www.tokaibus.jp/kousoku/", "Tokai Bus (highway buses)", "東海バス（高速バス）",
                         "Tokai Bus: Highway bus routes (checked November 2026)"),
    "tokaibus_freepass": ("https://www.tokaibus.jp/rosen/freekippu_shimoda_minamiizu.html", "Tokai Bus (bus passes)",
                          "東海バス（下田・南伊豆のフリーきっぷ）", "Tokai Bus: Shimoda and Minami-Izu two-day bus passes (checked November 2026)"),
    "izu_tokko": ("https://kanko.city.izu.shizuoka.jp/sightseeing/tokkonoyu/", "Izu City", "伊豆市", "Izu City tourism: Tokko-no-yu"),
    "shimoda_ohama": ("https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html", "Shimoda City", "下田市",
                      "Shimoda City: Shirahama Ohama Beach"),
    "shimoda_beach2026_city": ("https://city.shimoda.shizuoka.jp/file/広報しもだ令和8年8月号2-3頁.pdf", "Shimoda City newsletter, August 2026",
                               "広報しもだ 2026年8月号", "Shimoda City newsletter, August 2026: beaches open in Shimoda"),
    "shimoda_population": ("https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/155431.html", "Shimoda City (population)",
                           "下田市（男女別人口・世帯数）", "Shimoda City: Population and households from the resident register (1 November 2026)"),
    "shimoda_profile": ("https://www.city.shimoda.shizuoka.jp/category/070200shinogaiyou/110963.html", "Shimoda City (about the city)",
                        "下田市（下田市の紹介）", "Shimoda City: About Shimoda"),
    "shimoda_hist_perry": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110778.html", "Shimoda City (Perry and the opening of Japan)",
                           "下田市（ペリー黒船艦隊来航と日本開国）", "Shimoda City: Perry’s Black Ships and the opening of Japan"),
    "shimoda_hist_harris": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110776.html", "Shimoda City (Townsend Harris)",
                            "下田市（日本における初代米国総領事ハリス）", "Shimoda City: Townsend Harris, the first US Consul General in Japan"),
    "shimoda_hist_ansei": ("https://www.city.shimoda.shizuoka.jp/category/100400shimodanorekishi/110777.html", "Shimoda City (the Ansei tsunami)",
                           "下田市（ディアナ号来航と安政の大津波）", "Shimoda City: Putyatin, the Diana and the Ansei tsunami"),
    "shimoda_perryroad": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110766.html", "Shimoda City (Perry Road)",
                          "下田市（ペリーロード）", "Shimoda City: Perry Road"),
    "shimoda_ryosenji": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110768.html", "Shimoda City (Ryosenji)",
                         "下田市（了仙寺）", "Shimoda City: Ryosenji temple"),
    "shimoda_gyokusenji": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110756.html", "Shimoda City (Gyokusenji)",
                           "下田市（玉泉寺）", "Shimoda City: Gyokusenji temple"),
    "shimoda_nesugata": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110764.html", "Shimoda City (Mt Nesugata)",
                         "下田市（寝姿山）", "Shimoda City: Mt Nesugata"),
    "shimoda_park": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110769.html", "Shimoda City (Shimoda Park)",
                     "下田市（下田公園）", "Shimoda City: Shimoda Park"),
    "shimoda_michinoeki": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/110763.html", "Shimoda City (Michi-no-Eki)",
                           "下田市（道の駅開国下田みなと）", "Shimoda City: Michi-no-Eki Kaikoku Shimoda Minato"),
    "shimoda_beaches_city": ("https://www.city.shimoda.shizuoka.jp/category/100100midokoro/155720.html", "Shimoda City (beaches)",
                             "下田市（海水浴場）", "Shimoda City: Swimming beaches (2026 season, checked November 2026)"),
    "shimoda_kanko_umi": ("https://www.shimoda-city.info/umi", "Shimoda Tourism Association (beaches)", "下田市観光協会（下田の海）",
                          "Shimoda Tourism Association: Shimoda’s nine beaches and beach rules (checked November 2026)"),
    "shimoda_kanko_beach_shirahamachuo": ("https://www.shimoda-city.info/shirahama-chuo", "Shimoda Tourism Association (Shirahama Chuo)",
                                          "下田市観光協会（白浜中央海水浴場）", "Shimoda Tourism Association: Shirahama Chuo (Nagatahama) Beach (2026)"),
    "shimoda_kanko_beach_shirahama": ("https://www.shimoda-city.info/shirahama-ohama", "Shimoda Tourism Association (Shirahama Ohama)",
                                      "下田市観光協会（白浜大浜海水浴場）", "Shimoda Tourism Association: Shirahama Ohama Beach (2026)"),
    "shimoda_kanko_beach_sotoura": ("https://www.shimoda-city.info/sotoura", "Shimoda Tourism Association (Sotoura)",
                                    "下田市観光協会（外浦海水浴場）", "Shimoda Tourism Association: Sotoura Beach (2026)"),
    "shimoda_kanko_beach_kujuppama": ("https://www.shimoda-city.info/kujupama", "Shimoda Tourism Association (Kujuppama)",
                                      "下田市観光協会（九十浜海水浴場）", "Shimoda Tourism Association: Kujuppama Beach (2026)"),
    "shimoda_kanko_beach_nabeta": ("https://www.shimoda-city.info/nabeta", "Shimoda Tourism Association (Nabetahama)",
                                   "下田市観光協会（鍋田浜海水浴場）", "Shimoda Tourism Association: Nabetahama Beach (2026)"),
    "shimoda_kanko_beach_tatado": ("https://www.shimoda-city.info/tatado", "Shimoda Tourism Association (Tatadohama)",
                                   "下田市観光協会（多々戸浜海水浴場）", "Shimoda Tourism Association: Tatadohama Beach (2026)"),
    "shimoda_kanko_beach_irita": ("https://www.shimoda-city.info/irita", "Shimoda Tourism Association (Iritahama)",
                                  "下田市観光協会（入田浜海水浴場）", "Shimoda Tourism Association: Iritahama Beach (2026)"),
    "shimoda_kanko_beach_kisami": ("https://www.shimoda-city.info/kisami", "Shimoda Tourism Association (Kisami Ohama)",
                                   "下田市観光協会（吉佐美大浜海水浴場）", "Shimoda Tourism Association: Kisami Ohama Beach (2026)"),
    "shimoda_kanko_beach_toji": ("https://www.shimoda-city.info/toji", "Shimoda Tourism Association (Toji)",
                                 "下田市観光協会（田牛海水浴場）", "Shimoda Tourism Association: Toji Beach (2026)"),
    "pref_beach_water_2026": ("https://www.pref.shizuoka.jp/_res/projects/default_project/_page_/001/050/681/r8kaisuiyokujoitiran.pdf",
                              "Shizuoka Prefecture, 2026", "静岡県（令和8年度 海水浴場水質調査結果一覧）",
                              "Shizuoka Prefecture: Beach water quality survey results, FY2026"),
    "shimoda_kanko_suisen": ("https://www.shimoda-city.info/suisen", "Shimoda Tourism Association (daffodil festival)", "下田市観光協会（水仙まつり）",
                             "Shimoda Tourism Association: Daffodil festival at Tsumekizaki (2026–27 season)"),
    "shimoda_kanko_kurofune": ("https://www.shimoda-city.info/kurofune", "Shimoda Tourism Association (Black Ship Festival)", "下田市観光協会（黒船祭）",
                               "Shimoda Tourism Association: Black Ship Festival (2026 edition)"),
    "shimoda_kanko_ajisai": ("https://www.shimoda-city.info/ajisai", "Shimoda Tourism Association (hydrangea festival)", "下田市観光協会（あじさい祭）",
                             "Shimoda Tourism Association: Hydrangea festival in Shimoda Park (2026)"),
    "shimoda_kanko_onsen": ("https://www.shimoda-city.info/onsen", "Shimoda Tourism Association (hot springs)", "下田市観光協会（下田の温泉）",
                            "Shimoda Tourism Association: Day hot springs and footbaths (checked November 2026)"),
    "shimoda_kanko_bicycle": ("https://www.shimoda-city.info/access-bicycle", "Shimoda Tourism Association (bike rental)", "下田市観光協会（レンタサイクル）",
                              "Shimoda Tourism Association: Bike rental (checked November 2026)"),
    "shimoda_kanko_promenade": ("https://www.shimoda-city.info/promenade", "Shimoda Tourism Association (walks)", "下田市観光協会（遊歩道）",
                                "Shimoda Tourism Association: Walking paths (checked November 2026)"),
    "shimoda_kanko_about": ("https://www.shimoda-city.info/about", "Shimoda Tourism Association (information centres)", "下田市観光協会（観光協会について）",
                            "Shimoda Tourism Association: Information centres and opening hours (checked November 2026)"),
    "shimoda_tsunami_map": ("https://www.city.shimoda.shizuoka.jp/category/010300tiiki_bousai/120138.html", "Shimoda City (tsunami hazard maps)",
                            "下田市（津波ハザードマップ・津波避難計画地図）", "Shimoda City: Tsunami hazard maps and evacuation maps (in Japanese)"),
    "shimoda_tsunami_bldg": ("https://www.city.shimoda.shizuoka.jp/category/010400hinan_basyo/111108.html", "Shimoda City (tsunami evacuation buildings)",
                             "下田市（津波避難ビル）", "Shimoda City: Tsunami evacuation buildings"),
    "shimoda_elevation_map": ("https://www.city.shimoda.shizuoka.jp/category/010500bousai_tishiki/159625.html", "Shimoda City (height above sea level map)",
                              "下田市（ここは海抜何メートル）", "Shimoda City: Online map of height above sea level"),
    "shimoda_news_2013_08": ("https://city.shimoda.shizuoka.jp/file/平成25年8月号2頁3頁.pdf", "Shimoda City newsletter, August 2013",
                             "広報しもだ 2013年8月号", "Shimoda City newsletter, August 2013: Shizuoka’s 4th earthquake damage estimate for Shimoda"),
    "jma_tsunami_warnings": ("https://www.jma.go.jp/jma/kishou/know/jishin/joho/tsunamiinfo.html", "Japan Meteorological Agency",
                             "気象庁（津波警報・注意報、津波情報、津波予報について）",
                             "Japan Meteorological Agency: Tsunami warnings, advisories and information (in Japanese, checked November 2026)"),
    "jma_kamchatka_2025": ("https://www.jma.go.jp/jma/press/2507/30a/202507301010.html", "Japan Meteorological Agency, 30 July 2025",
                           "気象庁 報道発表（2025年7月30日10時10分）",
                           "Japan Meteorological Agency: Earthquake near the Kamchatka Peninsula at about 8:25 on 30 July 2025 (press release)"),
    "jma_kamchatka_2025_eve": ("https://www.jma.go.jp/jma/press/2507/30c/202507301910.html", "Japan Meteorological Agency, 30 July 2025 (evening)",
                               "気象庁 報道発表（2025年7月30日19時10分）",
                               "Japan Meteorological Agency: Earthquake near the Kamchatka Peninsula, third report (30 July 2025)"),
    "jta_safety_tips": ("https://www.jnto.go.jp/safety-tips/eng/app.html", "Japan Tourism Agency (Safety tips)", "観光庁（Safety tips アプリ）",
                        "Japan Tourism Agency: The app “Safety tips” (checked November 2026)"),
    "egov_immig_act_jesta": ("https://laws.e-gov.go.jp/law/326CO0000000319/20290331_508AC0000000032", "Immigration Control Act (amended, not yet in force)",
                             "出入国管理及び難民認定法（令和8年法律第32号による改正後・未施行）（e-Gov法令検索）",
                             "Immigration Control and Refugee Recognition Act as amended by Act No. 32 of 2026, Article 7-2 (e-Gov, not yet in force; checked 20 November 2026)"),
    "shugiin_bill221_20": ("https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/keika/1DE1F16.htm", "House of Representatives", "衆議院（議案審議経過情報）",
                           "House of Representatives: Progress of cabinet bill no. 20, 221st Diet session (checked 20 November 2026)"),
    "jta_jesta": ("https://www.mlit.go.jp/kankocho/content/002019837.pdf", "Japan Tourism Agency", "観光庁（JESTA の導入に伴う免税制度の見直し）",
                  "Japan Tourism Agency: Review of tax-free shopping checks following the introduction of JESTA (2026)"),
}

# ---------------------------------------------------------------- 記事のテーマ
# テーマ別の一覧ページ（/noki/akiya.html など）は、公開記事が3本以上になったテーマだけ自動で作る（薄い一覧を作らないため）
# 読み手の入口は「どこまで日本に深く関わるか」の1本の軸で分ける（重ならず、漏れない）:
#   stay = 旅行者として1週間〜1か月滞在する ／ live = 一年の一部を暮らす（数か月・毎年・仕事をしながら）／ own = 家を持つ（空き家を買う・直す・運営する）
# 記事は必ずこの3つのどれか1つ（"topic"）に入れる。ほかの段階の読み手にも役立つ記事は "also" に足す（一覧の「こちらも役立つ」に出る）。
# kanji は入口の印（漢字一文字）。季節の色は site.css の .t-<キー>（春=旅・夏=暮らし・秋=家・冬=場所）。
# 場所（places）は別の軸。記事に "place" があれば場所の一覧にも出る。
TOPICS = {
    "stay": {"kind": "plan", "name": "Stay longer", "ja": "長めに旅する", "kanji": "旅", "photo": "window-room",
             "photo_alt": "Two low chairs and a small table by a window with paper screens, looking out over water",
             "path_label": "A longer trip", "path_desc": "A week to a month as a visitor: towns, food, getting there.",
             "path_ja": "長めの旅（旅行者として1週間〜1か月）",
             "seo_title": "Slow Travel in Small-Town Japan: Week- and Month-Long Trips",
             "description": "Guides for travellers who want a week or a month in one small Japanese town instead of a different city every night: access, seasons, food and where to stay.",
             "intro": "For a week or a month as a visitor. One town instead of a different hotel every night: how to get there, when to go, what to eat and how a house changes the trip.",
             "coming": ["Shimoda for a week or longer", "The Japanese countryside for a longer stay"]},
    "live": {"kind": "plan", "name": "Live part-time", "ja": "一年の一部を暮らす", "kanji": "暮", "photo": "town-lane",
             "photo_alt": "Quiet paved lane between hedges and low houses, with green hills behind",
             "path_label": "Living here part of the year", "path_desc": "Months at a time, or every year: remote work, visas, monthly homes.",
             "path_ja": "一年の一部を暮らす（数か月・毎年・仕事をしながら）",
             "seo_title": "Living in Japan Part-Time: Long Stays, Visas, Remote Work",
             "description": "How to live in small-town Japan for months at a time or every year: how long you can stay, Japan’s digital nomad visa, monthly homes and working remotely.",
             "intro": "For months at a time, or a season every year. How long you can stay, Japan’s digital nomad visa, renting a home by the month and working remotely from a small town.",
             "coming": ["Renting a house in Japan for a month", "Japan’s digital nomad visa, and where to base yourself", "How long can you stay in Japan?"]},
    "own": {"kind": "plan", "name": "Own a home", "ja": "家を持つ", "kanji": "家", "photo": "empty-tatami-room",
            "photo_alt": "Empty tatami room in an old wooden house, with sliding windows open to a garden",
            "path_label": "Owning a home here", "path_desc": "Buying, restoring or running an akiya.",
            "path_ja": "家を持つ（空き家を買う・直す・運営する）",
            "seo_title": "Akiya in Japan: Buying, Restoring and Owning an Old House",
            "description": "Plain guides to owning an akiya, one of Japan’s vacant houses: who can buy one, what it really costs, restoring it and testing the town before you commit.",
            "intro": "Japan has about nine million empty homes, and foreigners can buy them. The listings are the easy part. These guides cover what an akiya really costs, what owning one does and does not give you, and how to try a town before you sign.",
            "coming": ["Can foreigners buy property in Japan?", "What is an akiya?", "Cheap and free houses in Japan: the real cost", "Akiya banks explained"]},
    "places": {"kind": "place", "name": "Places", "ja": "場所", "kanji": "地", "photo": "rocky-coast",
               "photo_alt": "Waves breaking against dark volcanic cliffs on a rocky coastline",
               "seo_title": "Small-Town Japan: Place Guides for Longer Stays",
               "description": "Guides to the towns where we run homes and the regions around them, starting with the Izu Peninsula, written for people staying a week or longer.",
               "intro": "We write about the places where we run homes, starting with the Izu Peninsula south-west of Tokyo.",
               "coming": []},
}
PLANS = [k for k, v in TOPICS.items() if v["kind"] == "plan"]

# ---------------------------------------------------------------- 記事
ARTICLES = [
# ============================================================ 金目鯛
{
 "id": "kinmedai", "slug": "kinmedai", "topic": "stay", "place": "izu", "also": [],
 "photo": ("grilled-red-fish", "A whole grilled red fish with rice, soup and small side dishes on a wooden table", ""),
 "published": "2026-11-14", "updated": "2026-11-16",
 "kicker": "Food and port towns",
 "h1": "Kinmedai: Japan’s golden-eye snapper and where to eat it",
 "seo_title": "Kinmedai: Japan’s Golden-Eye Snapper and Where to Eat It",
 "description": "Kinmedai is a red, golden-eyed deep-sea fish, often simmered as nitsuke. It’s fattiest around June, and the port of Shimoda in Izu is a good place to try it.",
 "dek": "Kinmedai is a red, golden-eyed deep-sea fish, often simmered in soy and sugar. Shimoda, said to be Japan’s top kinmedai port, is a good place to try it.",
 "card": "Kinmedai is a fatty, red deep-sea fish, often simmered in soy and sugar. It’s fattiest around June, and Shimoda, said to be Japan’s top kinmedai port, is a good place to try it.",
 "keywords": [("kinmedai", "4,400", "0")],
 "intent": "Know（知りたい）",
 "points": [
   "Its English name is splendid alfonsino, and whatever a menu calls it, it isn’t a sea bream, snapper or nodoguro.",
   "The white flesh carries fat all year, and we’d start with <em>nitsuke</em>, though raw or lightly seared works too.",
   "We’d spend a night in Shimoda: kinmedai for dinner, then breakfast at the fish-market canteen next morning.",
 ],
 "body": """
<h2>What is kinmedai?</h2>
<p>Kinmedai is the bright red fish with big golden eyes, and in Shimoda you’ll find it on menus all over town. In English it’s called splendid alfonsino (<em>Beryx splendens</em>) [[s:fishbase_beryx]]. It lives deep down, at around 200 to 800 metres off Chiba [[s:jfa_kinme_2021,chiba_kinme_r6]], and once it’s landed, the skin turns red all over in about 40 minutes [[s:shimoda_news]].</p>
<p>The name is written 金目鯛, which literally means “golden-eye sea bream”. If you’ve seen it called golden-eye snapper on an English menu, it’s the same fish. Despite the name, it isn’t a sea bream [[s:shimoda_kanko_kinme]], and it isn’t a snapper either: it belongs to the alfonsino family, Berycidae [[s:tokyo_kinme_tag]].</p>

<h2>What does kinmedai taste like, and how is it eaten?</h2>
<p>Kinmedai is a rich white fish that carries plenty of fat, and it stays that way all year. That’s down to life in deep water, and it means the fish works in lots of different dishes [[s:shimoda_news]]. If you only try it once, we’d go for <em>nitsuke</em>, fish simmered in soy sauce and sugar, though in our view it’s just as good raw or lightly seared.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Dish</th><th>What it is</th></tr></thead>
<tbody>
<tr><td><strong>Nitsuke</strong></td><td>A whole fish or a thick cut, simmered until the sauce turns glossy. Our pick for a first try. A bigger fish is worth paying a bit more for, we think, because bigger kinmedai carry more fat (a 2007–2011 Shizuoka study of fish from Inatori) [[s:shizuoka_kinme_fat]].</td></tr>
<tr><td><strong>Sashimi and aburi</strong></td><td>Raw slices, or slices with the skin lightly seared.</td></tr>
<tr><td><strong>Shabu-shabu</strong></td><td>Thin slices swished through hot broth at the table. If you see it on a menu, we’d give it a try.</td></tr>
<tr><td><strong>Everything else</strong></td><td>You’ll also find kinmedai ramen, burgers and croquettes [[s:tabimag]].</td></tr>
</tbody></table></div>
<p>If you’re buying a whole fish, look for clear golden eyes and bright red skin; both turn whitish as it ages [[s:shimoda_news]].</p>

<h2>Why is kinmedai expensive?</h2>
<p>We think it mostly comes down to how it’s caught and how little of it there is. Kinmedai live deep, so boats off the Kanto coast and the Izu Islands go after them with hook-and-line gear lowered a long way down. Most of it is done on vertical longlines (<em>tatenawa</em>) and bottom-set longlines (<em>soko-tate-haenawa</em>) [[s:jfa_kinme_2021,chiba_kinme_r6]]. And the catch is a lot smaller than it used to be.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Where</th><th>Before</th><th>More recently</th></tr></thead>
<tbody>
<tr><td><strong>Tokyo, Chiba, Kanagawa and Shizuoka</strong></td><td>Just under 7,000 tonnes a year (2005–2009)</td><td>3,797 tonnes (2020) [[s:jfa_kinme_2021]]</td></tr>
<tr><td><strong>Chiba alone</strong></td><td>2,263 tonnes (2007)</td><td>1,467 tonnes (2023) [[s:chiba_kinme_r6]]</td></tr>
</tbody></table></div>
<p>The good news is that the stock seems to be recovering. The Fisheries Agency’s 2021 assessment rated it low in 2020, with the breeding (spawning) stock flat for the previous five years [[s:jfa_kinme_2021]]. By 2023, the national assessment had the spawning stock above its target level and rising [[s:chiba_kinme_r6]].</p>
<p>That target is the level that should allow the largest catch year after year without shrinking the stock. For you, it means kinmedai isn’t a fish you need to avoid, but it isn’t plentiful either. In our view, that’s a big part of the price.</p>

<h2>How is kinmedai different from nodoguro?</h2>
<p>Nodoguro is a different fish altogether: it’s the market name for <em>akamutsu</em>, known in English as blackthroat seaperch [[s:kyoto_akamutsu,fishbase_nodoguro]]. The two are easy to mix up, since both are red and both are prized. But they sit in different families and different orders, and nodoguro lives much shallower. If a menu offers both, you’re choosing between two different fish.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>Kinmedai</th><th>Nodoguro</th></tr></thead>
<tbody>
<tr><td><strong>Order</strong></td><td>Beryciformes, the alfonsino order [[s:tokyo_kinme_tag]]</td><td>Perciformes, the perch-like fishes [[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>Family</strong></td><td>Alfonsinos (Berycidae) [[s:tokyo_kinme_tag]]</td><td>Acropomatidae [[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>Depth</strong></td><td>About 200–800 m off Chiba [[s:chiba_kinme_r6]]</td><td>About 80–150 m in the south-western Sea of Japan [[s:ibaraki_akamutsu]], about 100–200 m in Tokushima’s account [[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>Name</strong></td><td>金目鯛, “golden-eye sea bream”</td><td>“Black throat”, for the black lining inside its mouth [[s:kyoto_akamutsu]]</td></tr>
</tbody></table></div>
<p>Fish classification gets revised now and then, so other books may file these two a little differently.</p>

<h2>Is kinmedai safe to eat when you’re pregnant?</h2>
<p>Because of mercury, Japan’s health ministry advises pregnant women to limit some fish to about one 80 g serving a week. Kinmedai is on that list, along with swordfish, bluefin tuna and bigeye tuna [[s:mhlw_mercury2010]]. The same advice puts one piece of sushi or sashimi at about 15 g, so 80 g is roughly five pieces. It’s aimed at protecting the unborn baby, not at children or other adults [[s:mhlw_mercury2010]]. It’s general public guidance rather than medical advice, so if you’re pregnant, your own doctor or midwife is the person to ask.</p>

<h2>Where can you eat kinmedai in Shimoda?</h2>
<p>Plenty of places in town serve it, and the tourism association’s list is a good place to start. It’s a long one, with 19 restaurants and 34 hotels and inns on it in November 2026 [[s:shimoda_kanko_kinme]]. Some may take kinmedai off the menu depending on the catch, so it’s not a bad idea to ask when you book [[s:shimoda_kanko_kinme]].</p>
<p>No wonder it’s on so many menus. Shimoda, at the southern tip of the [[l:izu|Izu Peninsula]], is said to be Japan’s top kinmedai port, and kinmedai make up about 80% of the fish landed there (over 1,000 tonnes a year, by the tourism association’s count in November 2026) [[s:shimoda_kanko_kinme]]. You may hear locals talk about two kinds: <em>jikinme</em>, caught close by between Oshima and Kozushima, and <em>oki-kinme</em>, from grounds further out (as a 2014 TV Tokyo programme put it) [[s:tvtokyo]].</p>
<p>If you only have time for one meal, we’d start at Ichiba no Shokudo Kinmetei, a canteen inside the Shimoda fish market. You can have a kinmedai rice bowl served three ways, or a whole simmered kinmedai set [[s:pref]]. Hours do change, so a quick check before you walk over can save a wasted trip.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Kinmetei</th><th>Details</th></tr></thead>
<tbody>
<tr><td><strong>Getting there</strong></td><td>About ten minutes on foot from Izukyu-Shimoda Station [[s:pref]]</td></tr>
<tr><td><strong>Morning set</strong></td><td>7:00–9:30</td></tr>
<tr><td><strong>Lunch</strong></td><td>11:00–15:00</td></tr>
<tr><td><strong>Closed</strong></td><td>Tuesdays (Shizuoka Prefecture’s page, updated March 2025) [[s:pref]]</td></tr>
</tbody></table></div>

<h2>When is kinmedai in season?</h2>
<p>Kinmedai is a deep-sea fish, so it’s landed all year, and the tourism association says it’s in season all year too [[s:shimoda_kanko_kinme]]. Locals still point to two high points: winter, and early summer around June, when the fish are fattiest.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>When</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Winter</td><td>The traditional season, when kinmedai goes into hot pots [[s:shimoda_news,shizuoka_kinme_fat]] and the flesh is at its firmest [[s:shimoda_kanko_kinme]].</td></tr>
<tr><td>Around June</td><td>Before spawning, when the fish carry the most fat. When Shizuoka researchers measured Inatori fish through the year, fat peaked in June at about 10% (2007–2011 study) [[s:shimoda_news,shizuoka_kinme_fat]].</td></tr>
<tr><td>Kinme Matsuri (all of June in 2016)</td><td>In 2016 you could watch the landings from a spot outside the fish market, from about 7:30 to 9:00 a.m. It was closed on Tuesdays and Saturdays, and bad weather could cancel it [[s:shimoda_news]].</td></tr>
</tbody></table></div>
<p>So in 2016, June was the month to see the boats’ catch come in. For upcoming events, the tourism association’s events calendar is the place to look [[s:shimoda_kanko_event]], and the association can help if you’d like to plan a trip around one.</p>

<h2>Why stay overnight instead of visiting for the day?</h2>
<p>In our view, a night in town is what makes a kinmedai trip relaxed. You can have kinmedai for dinner and wake up with nowhere you need to be. There’s time for a walk down to the harbour, then breakfast at the market canteen, which opens at 7:00 [[s:pref]]. The morning set changes daily with the catch [[s:pref]], and there’s no train to rush back for. If you can stay longer, our [[l:shimoda-guide|guide to a week in Shimoda]] covers the beaches and the rest of the town.</p>
<p>A day trip is possible, but only just. From Tokyo, the earliest you can get to Izukyu-Shimoda is 7:59, on a 4:35 local from Shinagawa that connects at Atami (JR East’s November 2026 timetable) [[s:jre_tt_tokyo]]. If the viewing still ran until about 9:00, as it did in 2016 [[s:shimoda_news]], you’d still have most of an hour after the ten-minute walk to the market. Routes are in our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]].</p>
<p>If you’d like to cook a fish yourself, the Izu Fisheries Cooperative runs a shop on the ground floor of the Kaikoku Shimoda Minato roadside station that sells Shimoda kinmedai [[s:shimoda_kanko_gift]]. It’s about ten minutes on foot from the station [[s:pref_izu_gyokyo_shop]]. It’s open 8:00 to 16:30, with no regular closing day [[s:pref_izu_gyokyo_shop]]. Those are the hours as of April 2025, so a quick check before you go is a good idea. You’ll need a kitchen, of course. Our apartment in the old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is eight minutes’ walk from the station [[s:node_access]]. Its kitchen has a gas hob, fridge, rice cooker and cookware [[s:node_room]].</p>
""",
 "faq": [
   ("Is kinmedai the same as red snapper?",
    "No. Kinmedai belongs to the alfonsino family (Berycidae), not the snapper or sea bream families [[s:tokyo_kinme_tag]]. Whatever an English menu calls it, it isn’t a snapper."),
   ("Why is kinmedai so expensive?",
    "We think it’s mainly how it’s caught and how little there is. It lives deep, at around 200 to 800 metres off Chiba, and is caught on hook-and-line gear, mostly vertical longlines [[s:jfa_kinme_2021,chiba_kinme_r6]]. By 2020, catches from Tokyo to Shizuoka were down to 3,797 tonnes. That’s a little over half the late-2000s level [[s:jfa_kinme_2021]]. The good news is that a later national assessment found the 2023 breeding stock above its target level and rising [[s:chiba_kinme_r6]]."),
   ("Is kinmedai the same as nodoguro?",
    "No. Nodoguro is the market name for akamutsu, or blackthroat seaperch [[s:fishbase_nodoguro]], a red fish from a different order and family (Perciformes, Acropomatidae). It lives in shallower water, at around 80 to 200 metres depending on the area [[s:tokushima_akamutsu,ibaraki_akamutsu]]."),
   ("Can I eat kinmedai when I’m pregnant?",
    "Japan’s health ministry advises pregnant women to keep kinmedai to about one 80 g serving a week because of mercury, which is roughly five pieces of sushi [[s:mhlw_mercury2010]]. Your doctor or midwife can tell you what applies to you."),
   ("When is kinmedai in season?",
    "It’s landed all year, and Shimoda’s tourism association calls it in season all year [[s:shimoda_kanko_kinme]]. Winter is the traditional season, and the fish are fattiest around June [[s:shimoda_news,shizuoka_kinme_fat]]."),
   ("Can I see the kinmedai landings on a day trip from Tokyo?",
    "In 2016, visitors could watch the early-morning landings during the June festival [[s:shimoda_news]], and upcoming events are on the tourism association’s events calendar [[s:shimoda_kanko_event]]. Getting there in time is the hard part. The earliest connection from Tokyo, a 4:35 local from Shinagawa, reaches Shimoda at 7:59 [[s:jre_tt_tokyo]]. We’d rather stay the night before and have breakfast at the market canteen."),
   ("How do you say kinmedai?",
    "Roughly “kin-meh-dye”. Locals often shorten it to <em>kinme</em>."),
 ],
 "sources": ["shimoda_kanko_kinme", "shimoda_news", "pref", "shizuoka_kinme_fat", "chiba_kinme_r6", "jfa_kinme_2021",
             "tokyo_kinme_tag", "tokushima_akamutsu", "kyoto_akamutsu", "ibaraki_akamutsu", "mhlw_mercury2010",
             "tvtokyo", "tabimag", "jre_tt_tokyo", "shimoda_kanko_event", "shimoda_kanko_gift", "pref_izu_gyokyo_shop",
             "node_room", "node_access", "fishbase_beryx", "fishbase_nodoguro"],
 "related": ["izu-from-tokyo", "izu"],
 "ja": {
  "h1": "金目鯛とは：日本の「ゴールデンアイ・スナッパー」と、食べられる場所",
  "dek": "金目鯛は、赤い皮と金色の目をした深海魚で、醤油と砂糖で煮る煮付けでよく食べられます。金目鯛の水揚げ日本一と言われる下田は、食べに行くのにちょうどいい場所です。",
  "review": [
   "2026-11-21 ネイティブ感の仕上げ（playbook 3-1 の6 の後半）: 冒頭を図鑑の書き方（分類・すむ場所）から「真っ赤で目が金色、下田では町のあちこちで食べられる魚」に。水揚げの段落の数字を1文にまとめ、日帰りの段落は「東京方面からいちばん早く着けるのは7:59」だけにしました（東京駅5:20発の文を外した）。事実・数値・出典は変えていません。",
   "2026-11-20 見せ方のリライト（人の方針「ガイドブックのような固い文章は読みづらい」、playbook 3-1 の6）: ①「なぜ高いのか」の漁獲量の数字（4都県と千葉県）を本文から小さな表に移し、本文は「深い所で釣る・量が減った・資源は持ち直してきている」という流れで話すようにしました ②金目亭の行き方・営業時間・定休日を小さな表にし、本文は「1食だけならここ」というすすめ方に。観光協会の一覧の店の数も短い文に分けました ③日帰りの段落・自炊の段落・NODE Shimoda の文・FAQ（なぜ高い・日帰り）で、1文に詰めていた数字や条件を分けました。FAQ の「なぜ高い」は 7,000トン弱を「2000年代後半の半分ちょっと」と言い換えています（数字は本文の表にそのまま残しています） ④品質保証部の指摘（89点）を受けて、本文の出典の前置き（「下田市の広報によると」「静岡県の研究者が…」「旅マガジンは」「千葉県によると」など）を減らし、出典の番号は同じ文に残しました。行事は「これからの行事は観光協会の行事のページで」に、メニューから消える条件は出典どおり「水揚げによっては」にしています ⑤事実・数値・出典・体験は変えていません。時点（観光協会の数字は2026年11月時点、直売所の営業時間は2025年4月時点）も残しています。本文から消したのは、のどぐろとの表の下の「目と科は、東京都と徳島県の水産の資料での分け方です」という一文だけです（表の各マスの出典番号はそのまま）。",
   "【2026-11-16 書き直し（品質保証部の HTML 84点・原稿 85点の指摘と、黄色い枠をなくす決まり〔playbook 3-2〕）】変えた点: ①黄色い枠をすべてなくしました。公式のページで確かめられたことだけで書き、確かめられないこと（いまの祭りの開催、祭り以外の日の見学、私たちが案内している店）は書いていません ②下田の水揚げは「日本一の港と言われ、年1,000トン以上・下田で揚がる魚の約8割」と観光協会の言い方のまま書き、時点（観光協会のページ、2026年11月時点）を付けました。dek・card も「日本一と言われる」に ③「一年中揚がる・1年中が旬」「冬は身が引き締まる」に観光協会の出典を付けました ④きんめ祭りは2016年の記録（6月、市場の外で7時半〜9時ごろ、火・土は休み、天候で中止あり）として表に残し、「いまの行事は観光協会の行事のページで。行事に合わせるなら観光協会に」としました。調べた過程（「確かめられなかった」など）は書いていません ⑤日帰り: 「間に合っても終わりのほうだけ」を「2016年と同じ時間なら、駅から約10分歩いても1時間近く残る」に直しました ⑥In short の3つ目を「1泊して、夕食に金目鯛、翌朝は市場の食堂で朝ごはん」に（朝も金目鯛が出るとは書いていません。金目亭の朝は日替わり定食のみで、その日の水揚げで変わるため。本文にもそう書きました） ⑦のどぐろとの表の「目」の行に キンメダイ目／スズキ目 を入れ、「東京都と徳島県の水産の資料での分け方。分類は見直されることがある」と添えました。「独自の科」はやめ、キンメダイ科（Berycidae）と書きました ⑧出典名の二重かっこをやめ、出典は番号だけにしました ⑨食べられる店は、観光協会の一覧（飲食店19軒・宿34軒）へのリンクにしました。店名は県の出典がある金目亭だけです ⑩自炊用に買える所として、道の駅 開国下田みなと1階の伊豆漁協の直売所（観光協会と県のページ。住所・電話が同じ同じ店）を足しました ⑪NODE Shimoda は「旧町内のアパートの一室」とし、キッチンの設備は公式サイトの記載（ガスコンロ・冷蔵庫・炊飯器・調理器具）、駅から徒歩8分（公式のアクセス）で書きました。触れるのは本文で1回です ⑫新しい出典: shimoda_kanko_event・shimoda_kanko_gift・pref_izu_gyokyo_shop・node_access（SOURCES_NEW）",
   "【変わりやすい数字（確認した日）】観光協会の一覧の店の数（飲食店19軒・宿34軒、2026-11-16）、年1,000トン以上・約8割（観光協会のページ、2026-11-16）、金目亭の営業時間（静岡県のページ 2025年3月更新）、伊豆漁協の直売所の営業時間（静岡県のページ 2025年4月更新）、品川4:35発→伊豆急下田7:59着（JR東日本の時刻表 2026年11月）、NODE Shimoda の徒歩8分と設備（公式サイト、2026-11-16）",
  ],
  "points": [
    "英語の名前は splendid alfonsino。メニューで何と呼ばれていても、鯛でもフエダイ（スナッパー）でもなく、のどぐろとも別の魚です。",
    "白身には一年中脂がのっています。私たちならまず煮付けを選びますが、刺身やさっと炙ったものもおいしいです。",
    "私たちなら下田に1泊します。夕食に金目鯛を食べて、翌朝は魚市場の食堂で朝ごはんです。",
  ],
  "body": """
<h2>金目鯛とはどんな魚か</h2>
<p>金目鯛は、真っ赤な体に大きな金色の目をした魚で、下田では町のあちこちの店で食べられる魚です。英語では splendid alfonsino（学名 <em>Beryx splendens</em>）と呼ばれます[[s:fishbase_beryx]]。千葉の沖では水深200〜800メートルほどの深い所にすみ[[s:jfa_kinme_2021,chiba_kinme_r6]]、水揚げされると、40分ほどで全身が赤くなります[[s:shimoda_news]]。</p>
<p>漢字では「金目鯛」と書きます。英語のメニューで golden-eye snapper と見かけたなら同じ魚です。名前に「鯛」がついていますが鯛の仲間ではなく[[s:shimoda_kanko_kinme]]、フエダイ（スナッパー）の仲間でもありません。キンメダイ科（Berycidae）の魚です[[s:tokyo_kinme_tag]]。</p>

<h2>金目鯛はどんな味で、どうやって食べるのか</h2>
<p>金目鯛は、脂のたっぷりのった、こくのある白身で、それが一年中変わりません。深い海にすむからで、そのおかげでいろいろな料理に向きます[[s:shimoda_news]]。1回だけ食べるなら、私たちは醤油と砂糖で煮る「煮付け」をすすめます。ただ、生でも、さっと炙っても同じくらいおいしいと私たちは思います。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>料理</th><th>どんなものか</th></tr></thead>
<tbody>
<tr><td><strong>煮付け</strong></td><td>丸ごと、または厚い切り身を、たれに照りが出るまで煮たもの。最初の1回に、私たちがすすめる食べ方です。少し高くても大きめの魚を選ぶ価値があると思います。大きい金目鯛ほど脂が多いからです（静岡県による稲取の魚の調査、2007〜2011年度）[[s:shizuoka_kinme_fat]]。</td></tr>
<tr><td><strong>刺身と炙り</strong></td><td>生の切り身や、皮目をさっと炙った切り身です。</td></tr>
<tr><td><strong>しゃぶしゃぶ</strong></td><td>薄切りを、卓上の熱い出汁にくぐらせて食べます。メニューで見かけたら、私たちなら試してみます。</td></tr>
<tr><td><strong>そのほか</strong></td><td>金目鯛のラーメン、バーガー、コロッケもあります[[s:tabimag]]。</td></tr>
</tbody></table></div>
<p>丸ごと買うなら、目が澄んだ金色で、皮が鮮やかな赤いものを選びましょう。古くなるとどちらも白っぽくなります[[s:shimoda_news]]。</p>

<h2>金目鯛はなぜ高いのか</h2>
<p>いちばんの理由は、とり方と、とれる量の少なさだと私たちは見ています。金目鯛は深い所にいるので、関東の沖や伊豆諸島の船は、仕掛けを深くまで下ろして釣ります。おもに「立縄」と「底立延縄」です[[s:jfa_kinme_2021,chiba_kinme_r6]]。しかも、とれる量は昔よりずいぶん減っています。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>どこで</th><th>以前</th><th>最近</th></tr></thead>
<tbody>
<tr><td><strong>東京・千葉・神奈川・静岡</strong></td><td>年7,000トン弱（2005〜09年）</td><td>3,797トン（2020年）[[s:jfa_kinme_2021]]</td></tr>
<tr><td><strong>千葉県だけ</strong></td><td>2,263トン（2007年）</td><td>1,467トン（2023年）[[s:chiba_kinme_r6]]</td></tr>
</tbody></table></div>
<p>うれしいことに、資源は持ち直してきているようです。水産庁の2021年の評価では、2020年の資源は「低位」で、親魚の量はそれまでの5年ほど横ばいでした[[s:jfa_kinme_2021]]。2023年には、国の評価で親魚の量が目標の水準を上回り、増えているとされました[[s:chiba_kinme_r6]]。</p>
<p>この目標の水準は、資源を減らさずに、毎年いちばん多くとり続けられる量の目安です。旅行者にとっては、避けなくてもいい魚だけれど、たくさんいるわけでもない、ということ。それが値段の大きな理由だと私たちは思います。</p>

<h2>金目鯛とのどぐろは、どう違うのか</h2>
<p>のどぐろは、まったく別の魚です。「アカムツ」の市場での呼び名で、英語では blackthroat seaperch と呼ばれます[[s:kyoto_akamutsu,fishbase_nodoguro]]。どちらも赤くて高級なので混同されがちです。でも、科も目（もく）も違い、のどぐろのほうがずっと浅い所にすんでいます。メニューに両方あれば、2つの違う魚から選んでいることになります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>金目鯛</th><th>のどぐろ</th></tr></thead>
<tbody>
<tr><td><strong>目（もく）</strong></td><td>キンメダイ目[[s:tokyo_kinme_tag]]</td><td>スズキ目[[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>科</strong></td><td>キンメダイ科[[s:tokyo_kinme_tag]]</td><td>ホタルジャコ科[[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>すむ深さ</strong></td><td>千葉の沖で200〜800メートルほど[[s:chiba_kinme_r6]]</td><td>日本海の南西の海域で80〜150メートルほど[[s:ibaraki_akamutsu]]、徳島県の資料では100〜200メートルほど[[s:tokushima_akamutsu]]</td></tr>
<tr><td><strong>名前の由来</strong></td><td>漢字で「金目鯛」（金色の目の鯛）</td><td>口の中（のど）が黒いこと[[s:kyoto_akamutsu]]</td></tr>
</tbody></table></div>
<p>魚の分類はときどき見直されるので、本によっては、この2つを少し違う分け方にしていることがあります。</p>

<h2>妊娠中に金目鯛を食べてもいいか</h2>
<p>厚生労働省は、水銀のために、妊婦が食べる量を「週1回・1回約80gまで」とする魚に、メカジキ、クロマグロ、メバチと並んで金目鯛を入れています[[s:mhlw_mercury2010]]。同じ注意事項では、寿司や刺身1貫は約15gなので、80gは寿司でだいたい5貫です。これはおなかの赤ちゃんを守るための目安で、子どもやほかの大人向けではありません[[s:mhlw_mercury2010]]。一般向けの目安で、医療の助言ではないので、妊娠中なら、かかりつけの医師や助産師に聞くのがいちばんです。</p>

<h2>下田のどこで金目鯛を食べられるか</h2>
<p>町には金目鯛を出す店がたくさんあって、手始めには観光協会の一覧が便利です。載っているのは飲食店19軒と、ホテル・旅館34軒（2026年11月時点）[[s:shimoda_kanko_kinme]]。水揚げによっては出せない日もあるそうなので、予約のときに聞いておくと安心です[[s:shimoda_kanko_kinme]]。</p>
<p>これだけ多いのには理由があります。下田は[[l:ja-izu|伊豆半島]]の南端にあり、金目鯛の水揚げ量日本一の港と言われています。年1,000トン以上（観光協会のページ、2026年11月時点）が揚がり、下田で揚がる魚の約8割を占めるそうです[[s:shimoda_kanko_kinme]]。地元では、2つの呼び名を耳にするかもしれません。大島から神津島にかけての近海でとれる「地金目」と、もっと遠くの漁場でとれる「沖金目」です（2014年のテレビ東京の番組での説明）[[s:tvtokyo]]。</p>
<p>1食だけなら、私たちはまず下田市魚市場の中にある食堂「市場の食堂 金目亭」をすすめます。金目鯛を3通りで味わう丼や、丸ごとの煮付けの定食があります[[s:pref]]。営業時間は変わることがあるので、出かける前にさっと確かめておくと、無駄足になりません。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>金目亭</th><th>くわしく</th></tr></thead>
<tbody>
<tr><td><strong>行き方</strong></td><td>伊豆急下田駅から歩いて約10分[[s:pref]]</td></tr>
<tr><td><strong>朝定食</strong></td><td>7:00〜9:30</td></tr>
<tr><td><strong>昼</strong></td><td>11:00〜15:00</td></tr>
<tr><td><strong>定休日</strong></td><td>火曜（静岡県のページ、2025年3月更新）[[s:pref]]</td></tr>
</tbody></table></div>

<h2>金目鯛の旬はいつか</h2>
<p>金目鯛は深海魚なので一年中揚がり、観光協会は「1年中が旬」と言っています[[s:shimoda_kanko_kinme]]。それでも地元では、とくにおいしい時期として2つの季節がよく挙がります。冬と、脂がいちばん乗る初夏の6月ごろです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>時期</th><th>理由</th></tr></thead>
<tbody>
<tr><td>冬</td><td>鍋の季節で、昔からの旬とされる時期です[[s:shimoda_news,shizuoka_kinme_fat]]。身がいちばん引き締まります[[s:shimoda_kanko_kinme]]。</td></tr>
<tr><td>6月ごろ</td><td>産卵の前で、脂がいちばん多い時期。静岡県の研究者が稲取の魚を1年を通して測ると、脂は6月に最も多く、約10%でした（2007〜2011年度の調査）[[s:shimoda_news,shizuoka_kinme_fat]]。</td></tr>
<tr><td>きんめ祭り（2016年は6月いっぱい）</td><td>2016年は、魚市場の外に見学場所があり、朝7時半〜9時ごろに水揚げを見られました（火曜・土曜は休み、天候で中止もあり）[[s:shimoda_news]]。</td></tr>
</tbody></table></div>
<p>つまり2016年は、6月が水揚げを見に行く月でした。これからの行事は、観光協会の行事のページで見られます[[s:shimoda_kanko_event]]。行事に合わせて旅を組みたいなら、観光協会に聞くのが確実です。</p>

<h2>日帰りではなく、泊まったほうがいい理由</h2>
<p>私たちは、町に1泊すると金目鯛の旅がずっとゆったりすると思っています。夕食に金目鯛を食べたら、翌朝は急ぐ用事もありません。港までのんびり歩いて、7時に開く市場の食堂で朝ごはん[[s:pref]]。朝はその日の水揚げで変わる日替わりの定食です[[s:pref]]。帰りの電車に追われることもありません。もっと長くいられるなら、浜や町の過ごし方を[[l:ja-shimoda-guide|下田で1週間過ごすためのガイド]]にまとめました。</p>
<p>日帰りもできますが、ぎりぎりです。東京方面からいちばん早く伊豆急下田に着けるのは、品川4:35発の普通で熱海で乗り継ぐ行き方で、7:59着です（JR東日本の2026年11月の時刻表）[[s:jre_tt_tokyo]]。2016年のように見学が9時ごろまであれば[[s:shimoda_news]]、駅から市場まで約10分歩いても、1時間近く残ります。行き方は、[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>魚を自分で料理してみたいなら、道の駅「開国下田みなと」の1階で、伊豆漁協が下田の金目鯛などを売る店を開いています[[s:shimoda_kanko_gift]]。駅から歩いて約10分です[[s:pref_izu_gyokyo_shop]]。営業は8時〜16時30分で、定休日はありません[[s:pref_izu_gyokyo_shop]]。2025年4月時点の営業時間なので、出かける前にさっと確かめておくと安心です。もちろん、料理するにはキッチンが要ります。旧町内にある私たちのアパートの一室「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、駅から歩いて8分です[[s:node_access]]。キッチンには、ガスコンロ・冷蔵庫・炊飯器・調理器具がそろっています[[s:node_room]]。</p>
""",
  "faq": [
    ("金目鯛は、レッドスナッパーと同じですか",
     "違います。金目鯛はキンメダイ科の魚で、名前に「鯛」が付くだけです。鯛の仲間でも、スナッパー（フエダイ）の仲間でもありません[[s:tokyo_kinme_tag]]。英語のメニューに何と書いてあっても、スナッパーではありません。"),
    ("金目鯛はなぜ高いのですか",
     "おもに、とり方と、とれる量の少なさだと私たちは見ています。千葉の沖では水深200〜800メートルほどの深い所にすみ、主に釣り（おもに立縄）でとります[[s:jfa_kinme_2021,chiba_kinme_r6]]。2020年には、東京から静岡までの漁獲量は3,797トンに減りました。2000年代後半の半分ちょっとです[[s:jfa_kinme_2021]]。うれしいことに、その後の国の評価では、2023年の親魚の量は目標の水準を上回り、増えています[[s:chiba_kinme_r6]]。"),
    ("金目鯛とのどぐろは同じ魚ですか",
     "違います。のどぐろは「アカムツ」の呼び名で[[s:fishbase_nodoguro]]、スズキ目ホタルジャコ科という、目も科も違う赤い魚です。すむ深さは、海域によって80〜200メートルほどと、金目鯛より浅い所です[[s:tokushima_akamutsu,ibaraki_akamutsu]]。"),
    ("妊娠中に金目鯛を食べてもいいですか",
     "厚生労働省は、水銀のために、妊婦は金目鯛を「週1回・1回約80gまで」にするよう勧めています。寿司ならだいたい5貫です[[s:mhlw_mercury2010]]。自分の場合どうかは、医師や助産師に聞いてください。"),
    ("金目鯛の旬はいつですか",
     "一年中揚がり、下田の観光協会は「1年中が旬」と言っています[[s:shimoda_kanko_kinme]]。昔からの旬は冬で、脂がいちばん乗るのは6月ごろです[[s:shimoda_news,shizuoka_kinme_fat]]。"),
    ("東京から日帰りで、金目鯛の水揚げを見られますか",
     "2016年は、6月のきんめ祭りの期間に、朝の水揚げを見学できました[[s:shimoda_news]]。これからの行事は、観光協会の行事のページで見られます[[s:shimoda_kanko_event]]。難しいのは間に合うかどうかで、東京からいちばん早い品川4:35発の普通でも、下田に着くのは7:59です[[s:jre_tt_tokyo]]。私たちなら前の晩に泊まって、市場の食堂で朝ごはんにします。"),
    ("kinmedai はどう発音しますか",
     "英語を話す人には “kin-meh-dye” が近い音です。地元では「キンメ」と略すこともよくあります。"),
  ],
 },
},
# ============================================================ 空き家
{
 "id": "akiya-try-first", "slug": "akiya-try-before-you-buy", "topic": "own", "place": None, "also": ["live"],
 "photo": ("yaizu-engawa", "Old wooden house with a long veranda and an overgrown garden", "An older house in Iwashigashima, Yaizu, before renovation."),
 "published": "2026-11-14", "updated": "2026-11-16",
 "kicker": "Own a home",
 "h1": "Buying an akiya in Japan? Live in one for a month first",
 "seo_title": "Buying an Akiya in Japan? Live in One for a Month First",
 "description": "Japan has nine million empty homes. Non-residents can buy one, reporting it to the Ministry of Finance since April 2026. A month in the town tells you more.",
 "dek": "Japan had about nine million empty homes in 2023, and non-residents can buy one. But you’re buying into a town, and a month there tells you more than any listing.",
 "card": "You can buy one of Japan’s nine million empty homes, but the town matters more than the house. A month there shows you what heating or cooling really costs, whether you need a car and how the neighbours are, and a monthly rental or guesthouse is the realistic way to do it from abroad.",
 "keywords": [("buying an akiya in japan", "—", "—"), ("akiya", "3,600", "0")],
 "intent": "Do（比べたい・やり方）",
 "points": [
   "Since April 2026, non-residents who buy a home have had to report it to the Ministry of Finance.",
   "A month shows you whether you need a car, how the neighbours are and what heating or cooling really costs.",
   "From abroad, a monthly rental or a guesthouse with monthly rates is usually more realistic than a town’s trial home.",
 ],
 "body": """
<p>An akiya (空き家) is simply a house that nobody lives in, and Japan has a record number of them: about 9 million in the 2023 housing survey, or 13.8% of all homes [[s:stat_housing2023]]. Plenty of those are just waiting for a tenant or a buyer, though [[s:stat_housing2023]]. In our experience, when people talk about Japan’s abandoned houses, they mean the 3.86 million that aren’t for rent, for sale or anyone’s second home. That group is still growing: there are more of them now than in 2018 [[s:stat_housing2023]].</p>

<h2>Can foreigners buy an akiya?</h2>
<p>Yes, non-residents can buy. What’s changed is the paperwork, and the Ministry of Finance’s rules spell it out. Since April 2026, if you buy property in Japan while living abroad, you have to report it to the ministry under the Foreign Exchange Act, even if it’s a home you plan to live in [[s:mof_fefta2026,mof_realprop_faq]]. Real Estate Japan, a property site for foreign buyers, puts it simply: you don’t need to live in Japan to buy [[s:rej]]. And since 5 October 2026, every buyer, Japanese or not, gives their nationality when the purchase is registered [[s:moj_nationality]].</p>
<p>The rules are still moving, though. A bill before the Diet would create new zones within about 1 km of some defence and coast guard sites, and on uninhabited border islands [[s:cao_land_bill,cao_land_bill_outline]]. Inside those zones, every transfer of land ownership would need the government’s approval in advance. The changes would take effect within 18 months of the act being promulgated [[s:cao_land_bill_outline]]. As of mid-November 2026, the bill was still before the House of Representatives, so it isn’t law yet [[s:shugiin_bill18]]. If a house you like is near one of those sites, that bill is the one to keep an eye on.</p>
<p>We’d also treat a house and a visa as two separate questions. If you’re hoping that owning a home will help you stay in Japan longer, it’s worth checking with an administrative scrivener (<em>gyoseishoshi</em>) who handles visas before you count on it. And with the rules changing this fast, we think it’s sensible to have a lawyer or judicial scrivener (<em>shiho shoshi</em>) look at your own case before you sign.</p>

<h2>Why live in the town before you buy?</h2>
<p>Buying the house is the easy part. What you’re really committing to is the town, and a listing can only tell you so much: the price, the floor plan, a few photos. The things that decide whether you’ll be happy there only show up once you’ve lived there for a while.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What you want to know</th><th>How a month shows you</th></tr></thead>
<tbody>
<tr><td>How cold an old wooden house gets in January, and what heating costs</td><td>You’ll feel it on the first cold night and see it on the electricity bill.</td></tr>
<tr><td>Whether daily life works without a car</td><td>A week of shopping and errands on foot, by bus or by bike makes it obvious, especially if you try the trips that aren’t on your doorstep, too.</td></tr>
<tr><td>Where you’ll buy food, and when the shops close</td><td>Cooking most of your own meals soon shows you what’s easy to find and what isn’t.</td></tr>
<tr><td>How rubbish sorting works on that street</td><td>You’ll be following the local collection calendar like everyone else. If there’s an English version, it’s worth asking city hall for it.</td></tr>
<tr><td>Whether the internet holds up for a working day</td><td>Normal working hours, video calls included, are the real test.</td></tr>
<tr><td>What humid months and typhoons do to the building</td><td>Neighbours and local builders know what tends to fail first in houses like it.</td></tr>
<tr><td>How the neighbourhood treats a newcomer</td><td>Saying hello, joining a clean-up day if there is one, and asking how other newcomers settled in will tell you a lot. Neighbours notice small things, too. When our broadband was being installed in Shimoda, we heard from neighbours about where the engineer’s van was parked.</td></tr>
</tbody></table></div>
<p>None of this comes up in a viewing.</p>

<h2>What only shows up once you live in an old house?</h2>
<p>The wiring and the internet, in our experience. We learnt this when one of our founding members rented an older flat in Shimoda from its owner and turned it into a guesthouse. We rented rather than bought, but we think a buyer would run into the same things.</p>
<p>The old two-wire electrics couldn’t run the air conditioner, the fridge and the microwave all at once, so we had to ask guests not to use them together. Upgrading the wiring costs real money, so it’s something to find out before you budget, not after. Getting broadband put in took more than two months because it was the busy season, and we got by on a plug-in home router until then.</p>
<p>The wiring and the wait for broadband are small examples of a bigger point. With a cheap old house, the asking price is only part of what you’ll pay. Renovation, taxes, insurance and upkeep come on top, and they vary so much from one building to the next that only written quotes will tell you the real figure.</p>

<h2>Which ways of staying let you try out a town properly?</h2>
<p>For most people, there are two: a visa-free short stay and the six-month digital nomad status. Neither needs a work visa or a move to Japan, and both give you plenty of time to settle into a town and see how it suits you. The rules below are as of November 2026.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Way to stay</th><th>How long</th><th>Who it’s for</th></tr></thead>
<tbody>
<tr><td><strong>Short-term visitor</strong>, visa-exempt</td><td>Up to 90 days for most visa-exempt nationalities, though some are given 15, 30 or 180 days [[s:jnto_visa]].</td><td>Anyone from a visa-exempt country or region. You can’t do paid work on this status, and the rule for your own passport is the one that counts [[s:jnto_visa]].</td></tr>
<tr><td><strong>Digital nomad</strong> status</td><td>Six months, and it can’t be renewed. You can apply for it again six months after you leave Japan [[s:isa_nomad_en]].</td><td>Nationals of countries and regions that are both visa-exempt and have a tax treaty with Japan [[s:isa_nomad_list]]. You need an annual income of at least ¥10 million and private medical insurance with at least ¥10 million of treatment cover, and you can’t work for a Japanese employer [[s:isa_nomad_en]].</td></tr>
</tbody></table></div>
<p>If the digital nomad route fits you, our [[l:digital-nomad|guide to Japan’s digital nomad visa]] has more on who qualifies and how it works.</p>
<p>For extensions, longer statuses and what happens if you leave and come back, see our guide to [[l:how-long-stay|how long you can stay in Japan]].</p>
<p class="fine">This is general information, not immigration advice. The list of eligible countries for the digital nomad status changes, so check it for your own passport.</p>

<h2>Where can you stay for a month to test a town?</h2>
<p>You’ve got three main choices: a town’s trial home, a monthly rental, or a guesthouse with monthly rates. Which one works depends on the town, and on where you’re coming from.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Option</th><th>How long</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>A town’s trial home</strong> (<em>otameshi jutaku</em>)</td><td>From a day or two up to a few months, and in one city for up to just under two years [[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>Each town sets its own rules, mostly for people planning to move. Minami-Alps City rents its trial home for one to three months at ¥21,000 a month (February 2026) [[s:minamialps_trial]].</td></tr>
<tr><td><strong>A monthly rental</strong></td><td>A month or more</td><td>A furnished room or flat let by the month. In a small town there may be few to choose from, so it helps to search early.</td></tr>
<tr><td><strong>A guesthouse or holiday home with monthly rates</strong></td><td>A week to a month or more</td><td>Often the easiest to book from abroad, and you can try daily life in the town without committing to anything.</td></tr>
</tbody></table></div>
<p>Trial homes sound ideal, but there’s a catch: they’re built for people who are moving, not for people testing a town from abroad. Minami-Alps City’s home is for people registered as living outside Yamanashi who intend to move to the city and have signed up for a relocation consultation [[s:minamialps_trial]]. Nationality isn’t one of the listed conditions, so if you live overseas, the city’s relocation desk can tell you whether you’d qualify.</p>
<p>Some cities spell it out. Shizuoka City’s long-term trial flats are city-run apartments you can rent for six months to under two years. They’re only for people who live outside Shizuoka Prefecture and have decided, or are preparing, to move to the city. If you’re not Japanese, you also need permanent or long-term residence, special permanent residence, or to be the spouse or child of a Japanese national (August 2026) [[s:shizuoka_long_trial]]. So a tourist or digital nomad stay won’t get you in.</p>
<p>That’s why, if you’re coming from abroad, we think a monthly rental or a guesthouse is usually the realistic choice. Our [[l:monthly-rental|guide to monthly rentals in Japan]] explains how they work. If you’ve set your heart on a trial home, the town’s relocation office is the first call to make.</p>
<p>Shimoda City does it differently. Under rules in force since April 2026, it pays half the rate at designated hotels for people thinking of moving there [[s:shimoda_stay_subsidy]]. The help covers up to 10 nights, at up to ¥4,000 a night [[s:shimoda_stay_subsidy]]. The catch is that you need to be registered as living in Japan outside Shizuoka Prefecture, so it won’t help if you’re coming from abroad [[s:shimoda_stay_subsidy]].</p>
<p>Towns within easy reach of Tokyo are the simplest to test, because getting there and back is easy. Shimoda, on the [[l:izu|Izu Peninsula]], is one of them: direct trains from Tokyo Station run every day and take about two and a half hours (2 hours 29 to 44 minutes on the November 2026 timetable) [[s:jre_tt_tokyo]], and our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] has the details.</p>
<p>If Shimoda is on your list, we run a small place there called <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, which can be a base while you get a feel for the town. It’s a renovated flat of about 40 m² in an apartment building in the old town, 8 minutes’ walk from Izukyu-Shimoda Station [[s:node_room,node_access]]. Our site describes it as handy for medium and long stays [[s:node_site]], and it’s licensed under Japan’s Hotel Business Act. Most of our guests so far have come from Europe and North America, and some come to work remotely.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, our flat in Shimoda’s old town.]]

<h2>What does a trial month look like?</h2>
<p>Mostly, it looks like ordinary life, with a few deliberate tests built in. Based on what caught us out in Shimoda, we’d plan it roughly week by week.</p>
<p>The first week goes on settling in: the supermarket, the clinic, the bus stop and the rubbish calendar. If you’re staying in an older building, it’s worth asking your host what amperage the electricity contract allows and where the breaker box is. The old wiring in our Shimoda flat couldn’t run the air conditioner, fridge and microwave at the same time. The amperage tells you roughly how much you can run at once, and knowing where the breaker box is turns a tripped switch into a quick fix.</p>
<p>By the second week you’re working your usual hours and cooking at home. That’s when you find out whether the connection survives a day of video calls, and you’ll see what heating or cooling really costs. It’s also a good moment to ask a local provider how long a new line takes there, since ours took more than two months.</p>
<p>The third week is for asking around. You might visit the city hall desk that handles empty houses, talk to a local agent, or ask a builder roughly what rewiring an old house costs. Neighbours are often the best people to tell you what humid summers and typhoons do to houses like theirs.</p>
<p>By the fourth week you’ll have a fair idea of what would need to change, about the house and about the way you live. Writing those costs and doubts down while they’re fresh makes it much easier to compare towns, or to walk away.</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
   ("Can foreigners buy property in Japan?",
    "Yes. Non-residents can buy, and since April 2026 they’ve had to report the purchase to the Ministry of Finance under the Foreign Exchange Act. Every buyer also gives their nationality at registration [[s:mof_fefta2026,moj_nationality]]. The rules are changing, so a lawyer or judicial scrivener can check your own case."),
   ("Will owning a house in Japan help me get a visa?",
    "We wouldn’t count on it. We treat a house and a visa as separate questions, so if staying longer is part of your plan, ask an administrative scrivener (<em>gyoseishoshi</em>) who handles visas before you buy."),
   ("Is a cheap house in Japan really cheap?",
    "Not always. The purchase price is only one part of the bill. Renovation, taxes, insurance and upkeep come on top. They vary a lot from one building to the next, so written quotes are the only way to know before you commit."),
   ("Can I use a town’s trial home as a foreigner?",
    "It depends on the town. Trial homes are mostly for people who plan to move there, and some spell out who qualifies. As of August 2026, Shizuoka City’s long-term trial flats took foreign nationals only with permanent, long-term or special permanent residence, or as the spouse or child of a Japanese national [[s:shizuoka_long_trial]]. The town’s relocation office will know the current rules."),
   ("How many akiya are there in Japan?",
    "About 9.0 million, according to the 2023 Housing and Land Survey [[s:stat_housing2023]]. That’s a record 13.8% of all housing."),
 ],
 "sources": ["stat_housing2023", "rej", "mof_fefta2026", "mof_realprop_faq", "moj_nationality", "cao_land_bill", "cao_land_bill_outline", "shugiin_bill18", "jnto_visa",
             "isa_nomad_en", "isa_nomad_list", "minamialps_trial", "shizuoka_trial", "shizuoka_long_trial", "shimoda_stay_subsidy", "jre_tt_tokyo",
             "node_site", "node_room", "node_access"],
 "related": ["monthly-rental", "izu-from-tokyo", "izu"],
 "ja": {
  "h1": "空き家を買う前に、まず1か月住んでみる",
  "dek": "2023年、日本には約900万戸の空き家があり、日本に住んでいない人も買えます。でも、買うことで引き受けるのは町のほう。そこで1か月暮らすと、物件情報よりずっと多くのことが分かります。",
  "review": [
   "2026-11-21 ネイティブ感の仕上げ（playbook 3-1 の6 の後半）: 冒頭の段落で数字が4つ続いていたのを、900万戸・13.8%と、放置された家の386万戸に絞り、「次の借り手や買い手を待っているだけの家も多い」を足しました（同じ統計が出典）。36万9千戸は「2018年より増えている」と言い換えました。事実・数値・出典は変えていません。",
   "2026-11-20 見せ方のリライト: 友人が話すような語り口に直しました。①1文に数字や条件を詰めた文（空き家の数・下田市の補助・東京からの所要時間・FAQ の2問）を2〜3文に分け、詰め込みすぎの文を6件から0件にしました ②在留資格の節の見出しを「1か月」に縛られない「町をじっくり試すには、どんな滞在のしかたがあるか」にし、最初の文で2つの方法を言う形に ③静岡市のお試し住宅の段落を2つに分け、「だから海外からならマンスリーか宿」という私たちの見方を独立させました。法案の段落に「気になる家がそうした施設の近くなら気にかけておきたい」と読み手にとっての意味を1文足しました ④命令文（ask…）を「聞いておくと安心」の形に。事実・数値・出典・リンク・体験の中身は変えていません（空き家の数の「10月1日」を「10月」に、FAQ の答えから調査日を省いただけです）。人に確かめてほしい点: なし",
   "【2026-11-19 公開前の導線の直し】①「1か月泊まれる場所」の節にマンスリーの部屋の記事へのリンク、ビザの表の下にデジタルノマドビザの記事へのリンクを1本ずつ足しました ②関連記事の先頭にマンスリーの部屋の記事を入れました（3本） ③一覧のカードの「冬の寒さ」を「冷暖房に実際いくらかかるか」に替え、本文・In short とそろえました。事実・出典は変えていません",
   "【2026-11-16 品質保証部（91点・ゲート違反1）の指摘での直し】変えた点: ①【ゲート】NODE Shimoda の段落の「上の宿の選択肢の1つ」をやめ、表の「月割のある宿（1か月以上）」の行とつながらないようにしました。「町の様子をつかむあいだの拠点にしてもらえる」「公式サイトでは中長期の滞在にも便利な宿として紹介」までにし、月割や1か月以上泊まれるとは書いていません ②下田市の補助に「2026年4月施行の要綱」と時点を足し、1〜2文に短くしました（1泊4,000円までと、海外からは使えないことだけ。11〜30泊の80,000円は本文から外しました） ③法案の施行を「公布から18か月以内（within 18 months of the act being promulgated）」にそろえ、law の重なりをなくしました ④法案の段落の時点を「2026年11月中旬」の1回だけにしました（冒頭の「2026年11月時点で」を削除）",
   "【2026-11-16 手離れ（黄色い枠をすべてなくした。playbook 3-2）】変えた点: ①【事実の追加】土地の法案: 衆議院の議案審議経過で「2026年11月中旬の時点で、まだ衆議院で審議中。法律になっていない」と書きました（出典 shugiin_bill18。10月23日受理・11月10日に内閣委員会に付託、成立・公布はまだ）。施行は「公布から18か月（1年6か月）以内」に英語版・日本語版ともそろえました ②【事実の変更】ビザなしの短期滞在: 出典を外務省（この環境から開けない mofa）から日本政府観光局の入国・ビザのページ（jnto_visa）に替え、「15日や30日の国もある」→「15日・30日・180日の国もある」に。「パスポートに条件が付く場合もある」は出典にないので削り、「この滞在では報酬を得る仕事はできない」を足しました ③デジタルノマドは編集長が出入国在留管理庁のページで確かめた内容と一致しているので、本文はそのままで枠だけ外しました ④家と在留資格の関係は公的な出典が見つからないため、断定は書かず、「家とビザは別の問題として考え、あてにする前に行政書士に聞く」という私たちの見方だけを残しました ⑤【事実の追加】伊豆の町のお試し住宅（伊豆市・南伊豆町）は公式ページで確かめられなかったので書いていません。代わりに、下田市の移住希望者の滞在費補助（市が指定する宿の宿泊料の半分、10泊まで1泊4,000円まで、11〜30泊続けてなら80,000円まで）を書き、対象が「静岡県外ですでに日本に住民登録があり、移住相談に登録した人」なので、海外から来る人は使えないと分かるようにしました（出典 shimoda_stay_subsidy。2026年3月改正の要綱） ⑥【事実の変更】NODE Shimoda を「古い家（older house）」→「旧町内のアパートの一室（約40㎡）を改装したもの、伊豆急下田駅から徒歩8分」に（公式サイトの客室・アクセスのページ）。「長めの滞在にも向く」は公式サイトの「中長期の滞在にも便利」にもとづき、30泊以上を受けるとは書いていません。写真の説明も「私たちの部屋」に ⑦体験の節の「下田の古い家を借りた」→「下田の古い部屋（older flat）を借りた」、1週目の「私たちの家の古い配線」→「下田の私たちの部屋の古い配線」に（experience.md 3-2 で NODE Shimoda と同じ施設と確認済み）。一軒家と読める言い方をなくしました ⑧宿の行の「古い家での暮らしを試せる」→「その町での暮らしを試せる」、1週目の「古い家に泊まっているなら」→「古い建物に泊まっているなら」 ⑨出典: shugiin_bill18・jnto_visa・shimoda_stay_subsidy・node_access を新しく（SOURCES_NEW）、node_site・node_room を使い、mofa を外しました",
   "【今回、人に確かめてほしい点】なし（黄色い枠はありません）。参考までに: 下田市の補助の対象の宿の一覧は確かめていないので、NODE Shimoda が対象かは書いていません。デジタルノマドの条件は、出入国在留管理庁のページがこの環境から開けず、編集長が2026-11-16に確かめた内容を使っています",
   "【2026-11-16 冒頭を短く（playbook 2章の1）】dek を2文・30語以内、In short を3項目・各20語以内にしました。空き家の数に「2023年時点」を付け、In short の「冬の寒さ」（冬の1か月でないと成り立たない）を、本文にある「冷暖房に実際いくらかかるか」に替えました。外した情報（空き家の割合13.8%、家とビザは別の話、2026年11月時点の90日の滞在・デジタルノマド、冬の寒さ）は本文にそのまま残っています。",
   "【2026-11-15 品質保証部（HTML）の指摘での書き直し】変えた点: ①デジタルノマド: 入管庁の英語のページに合わせ「出国後6か月たてば、もう一度申請できる（apply for it again six months after you leave）」に ②【言い方の変更】購入: 「日本は外国人の購入を禁止していない」をやめ、財務省の制度を主語に「日本に住んでいない人も買える。2026年4月からは、住むための家でも外為法にもとづいて財務省に報告する」にしました。民間サイト Real Estate Japan（rej）は「買うのに日本に住んでいる必要はない」という補足の1文だけに使っています。description・dek・card・In short・FAQ もそろえました ③静岡市の長期お試し住宅: 「移住を決めた、または準備している人」「日本人の配偶者等（配偶者や子）」に（本文・FAQ） ④「これは安い家すべてに言えること」を、「配線と回線工事の待ちは、もっと大きな話の小さな例。安い古い家では、売り出し価格はかかるお金の一部にすぎない」と、下田の体験から一般論へつなぐ形に ⑤1週目の「この2つが分かると…」を2文に分け、アンペア数＝一度にどれくらい使えるか、ブレーカーの場所＝落ちてもすぐ戻せる、と何を指すかをはっきりさせました ⑥「なぜ町で暮らすのか」の表の車の行から自社の家への言及を外しました（自社の家に触れるのは NODE Shimoda の段落の1回だけ） ⑦一覧のカード（card）を、目次の読み上げから答え（買えるが町のほうが大事、1か月で冬の寒さ・車・近所が分かる、海外からはマンスリーか宿）に替えました ⑧お試しの1か月の節の冒頭の「私たちならこう過ごす、という例です」というページの予告を、「週ごとにおおよそこう組み立てると思います」に",
   "【2026-11-15 時点の確認事項（2026-11-16 にすべて解決）】①NODE Shimoda を英語で「house（一軒家）」と呼んでよいか、さらに「older house（古い家）」と呼んでよいか、1週目の「私たちの家の古い配線」がこの家を指してよいか（黄色い枠） ②「買うのに日本に住んでいる必要はない」は Real Estate Japan（民間）の記載として書いています。ページの記載と合っているか ③購入の手続き（財務省への報告）は法務・制度の記述なので、公開前に財務省のページを開いて確かめてください",
   "【2026-11-15 組み込み前の仕上げ（品質保証部 90点・合格のあとの編集長の指摘8点）】変えた点: ①「家は安いほうの買い物」→「家を買うこと自体は簡単なほう」（リードと FAQ に合わせました）。配線の節の後に、改修・税金・保険・維持費が上乗せされ、本当の金額は書面の見積もりで分かる、の2文を足しました ②FAQ のお試し住宅の答えに特別永住者を足しました ③行政書士を英語で「在留資格（ビザ）の手続きを扱う行政書士（administrative scrivener）」と資格の名前で書きました（本文・FAQ） ④【事実の変更】「下田まで直通で3時間かからない」→「2026年11月時点で、東京駅から毎日走る直通で2時間29〜44分」。出典を編集長が確かめた JR東日本の東京駅の時刻表（jre_tt_tokyo）に替え、踊り子のページ（jreast_odoriko）は外しました ⑤南アルプス市の条件を「国籍は条件に挙げられていない」と制度の側から書きました ⑥NODE Shimoda の段落を3文にし、「一年中泊まれ、週割・月割がある」を削りました（黄色い枠から月額料金も外しました） ⑦「なぜ町で暮らすのか」の表の2行を、確認済みの体験（experience.md 3-2）につなげました。車の行に「下田の家は駅から徒歩10分ほどで、スーパー・コンビニ・飲食店が近い」、近所の行に「回線工事の車の停め方で近所から声をかけられた」 ⑧お試し1週目の「エアコン・冷蔵庫・電子レンジを同時に使ってみる」を、「泊まり先の人に契約のアンペア数とブレーカーの場所を聞く」に替えました。人に確かめてほしい点: 近所の行の書き方（experience.md では「工事の車両の駐車で近隣から指摘を受けた」）が、やわらげすぎ・強すぎになっていないか",
   "【2026-11-15 3回目の書き直し（品質保証部 84点・ゲート違反1、リサーチメモ 3）】変えた点: ①【事実の変更】土地の法案を、内閣府の法案の概要どおりに直しました。「重要な防衛施設の周りや国境の離島、国籍を問わず許可」→「一部の防衛関係施設と海上保安庁の施設の周り（おおむね1km）と無人の国境離島に区域をつくり、区域内の土地の所有権の移転はすべて事前許可。公布から1年6か月以内に施行」。審議の状況は「2026年11月時点で国会にかかっている」だけにし、10月23日の日付と内閣官房の提言の出典（cas_land_teigen）は外しました。新しい出典 cao_land_bill_outline を足しました ②【主張の変更】「家を買っても在留資格は付かない」「買うのにビザは要らない」は公的な出典が見つからなかったので、断定をやめました。本文・In short・FAQ とも「家とビザは別々の問題として考える、あてにする前に行政書士に聞く」という私たちの見方にし、黄色い枠を足しました ③description・card・In short の4項目目に「2026年11月時点」、FAQ のお試し住宅に「2026年8月時点」を入れました ④「海外に住む人が対象か確かめられなかった」という調べた側の言い方をやめ、「市の移住の窓口に聞けば分かる」にしました ⑤「it’s worth …」を7回から1回に減らし、締めの言い方を変えました（日本語版の「〜しておくと安心です」も同じように減らしました） ⑥「泊まれる場所」の節の最初の文で3つの選択肢の名前を言い、表のお試し住宅の欄を短くしました（静岡市オクシズの例と出典 okushizuoka_trial は外しました） ⑦「お試しの1か月」の節を、下田での体験（配線・回線工事の待ち）と表の項目につなげ、週ごとに試すこと（家電の同時使用、ビデオ会議と冷暖房費、回線工事にかかる期間を業者に聞く、配線のやり直しの費用を工務店に聞く、湿気・台風のことを近所に聞く、費用と迷いを書きとめる）を具体的にしました。新しい事実は足していません ⑧日本語版の伊豆半島への内部リンクを、日本語版の記事（ja-izu）に向くよう直しました ⑨In short の5項目目に「海外からならマンスリーか宿が現実的」を足しました（本文の見方と同じ）",
   "【2026-11-15 2回目の書き直し（リサーチメモ 2・組み込み後の採点の指摘）】変えた点: ①【事実の変更】京丹後市のお試し住宅は2026年9月末で市営の住宅が閉鎖されたため（市の閉鎖のお知らせ）、京丹後市を例から外し、出典 kyotango_trial も消しました。京丹後市にもとづいていた「1日から2か月ほどまで」は、「1〜2日から数か月まで、2年まで住める市もある」に直しました（静岡市 中心部・南アルプス市 1〜3か月・静岡市 長期 半年〜2年） ②お試し住宅の例を、リサーチ部が公式ページを開いて確かめた2つにしました。南アルプス市（芦安、1〜3か月・月21,000円、山梨県外に住民登録があり移住するつもりで移住相談に登録した人。国籍の記載なし）と、静岡市の長期お試し住宅（市営住宅に半年以上2年未満、静岡県外に住み移住を決めた人、外国籍は永住者・定住者・特別永住者・日本人の配偶者等に限る） ③お試し住宅は「移住する人のための仕組み」で、観光やデジタルノマドの滞在では使えない市があることを正直に書き、海外から来るならマンスリーか宿のほうが現実的だという見方を「私たちの考え」として添えました。FAQ の「外国人でも使えるか」も静岡市の例で答え直しました ④前の「たいてい町の外に住民登録がある人」という言い方（実際は県外が多い）をやめ、市ごとの条件をそのまま書きました ⑤「下田まで直通で3時間以内」に JR東日本（踊り子）の出典を付けました。数字は出していません ⑥「お試しの1か月」の節を、「1週目：…」のラベルの箇条書きから、ふつうの文章の段落に直しました ⑦伊豆の市町の黄色い枠を「1か月以上泊まれるか・料金・外国籍や海外在住の人が使えるか」に広げました",
   "【2026-11-15 品質保証部の指摘を受けた書き直し】変えた点: ①「購入に国籍・在留の制限はない」の断定をやめ、「2026年11月時点で禁止はないが、手続きは増えた（2026年4月から非居住者は外為法の報告、10月5日から登記で国籍の届出）。重要な区域の土地の許可制の法案が10月23日に国会に出ている」の形にし、専門家（弁護士・司法書士）に確かめるよう添えました（財務省・法務省・内閣府・内閣官房の出典） ②デジタルノマドを、出入国在留管理庁の条件どおりに直しました（対象はビザ免除かつ租税条約のある国・地域の人、年収1,000万円以上、治療費1,000万円以上の民間医療保険、日本の会社には雇われない、6か月で更新不可、出国から6か月たてば再び可）。時点は2026年11月 ③滞在の手段（観光の短期滞在・デジタルノマド）を表にしました ④空き家の数の出典を、総務省統計局の確報（2024年9月公表）1つにしました（900万戸・13.8%・過去最高、使い道のない空き家 約386万戸・2018年から36.9万戸増） ⑤「1か月泊まれる場所」の節を新しく書き、自治体のお試し住宅（自治体ごと、条件は町の外に住民登録があって移住を考えている人など。例は静岡市オクシズの3泊〜2週間・1組1日300円）、マンスリー、宿を表で並べました。NODE Shimoda はその中の1つとして紹介しています ⑥創業メンバーが下田で借りた古い家を宿に改修したときの体験を2点入れました（古い2芯の配線でエアコン・冷蔵庫・電子レンジを同時に使えなかった／繁忙期で回線工事に2か月以上かかり、置き型のルーターでしのいだ）。「買った」とは書かず「持ち主から借りた」と明記しています ⑦ゲストを「リモートで働く人がたくさん」→「リモートで働きに来る人もいる」に ⑧前の最後の節の「いちばんの近道」という押しの強い言い方をやめ、最後は1か月の過ごし方の節にしました。4週目も「決める」→「振り返る」に ⑨FAQ に「外国人は買えるか」「お試し住宅は外国人も使えるか」を足して5問にしました",
   "【以前の確認事項（2026-11-16 の手離れで解決・または書かないことにした）】⓪(a) 土地の法案が成立したか、いつ公布・施行か（黄色い枠。審議入りの報道は政党の機関紙でしか確認できず、記事には「国会にかかっている」とだけ書いています） (b)「外国人が家を買うことは禁止されていない」の出典の1つ rej（Real Estate Japan）は民間の不動産サイトです。もう1つは財務省の FAQ ですが、在留資格と不動産の関係は公的な出典が見つからず、行政書士か入管で確かめてほしい点として黄色い枠を置きました (c) NODE Shimoda を英語で「older house」（古い家）と呼んでよいか（experience.md では「旧町内の空き家を改修した」とあり、築年数は未確認） (d)「お試しの1か月」の節の「私たちならこう過ごす」は私たちの見方として書いています。言い方に違和感がないか ①法務・在留の記述（不動産購入の手続き、法案の審議状況、デジタルノマドの条件、90日と例外の国）は、公開の直前に一次のページを開いて確かめてください（黄色い枠4か所） ②創業メンバーの体験（配線・回線）の書き方が、事実と合っているか。「私たち（we）」の体験として書いています ③伊豆の市町（下田市・南伊豆町・伊豆市）に1か月以上泊まれるお試し住宅があるか、料金、外国籍・海外在住の人が使えるか（黄色い枠） ④月額料金、30泊以上を常に受けられるか、「再生した空き家」と呼んでよいか（黄色い枠） ⑤法務・在留の出典はリサーチ部が検索で確認したもので、本文のページは開けていません ⑥「下田まで直通の電車で3時間かからない」の出典の JR東日本の踊り子のページ（東京〜伊豆急下田 2時間49分）は、この環境から開けず検索でしか確かめていません。公開前にページを開いて確かめてください（ほかの記事は駅探の約2時間35分を使っているので、数字は出していません） ⑦南アルプス市・静岡市のお試し住宅の条件と料金（2026年11月15日にリサーチ部がページを開いて確認）が、公開の時点でも変わっていないか ⑧京丹後市を外したことでよいか（市営のお試し住宅は2026年9月末で閉鎖。民間・地域のお試し住宅は案内されていますが、例には使っていません）",
   "【入れられなかったこと】外為法の不動産取得の報告の細かい範囲（財務省の制度の概要のページを本文で確認できていないため）、在留資格と不動産の所有の関係を書いた公的な出典、海外に住む人が南アルプス市などのお試し住宅の対象に入るか（ページに記載がなく、町に聞くように書きました）、伊豆の市町のお試し住宅の有無、新耐震基準（1981年）など建物の点検の項目（公的な出典を未確認）、マンスリーの部屋の相場（出典なし）。焼津・修善寺の家は、状況が決まるまで書いていません",
  ],
  "points": [
    "2026年4月からは、日本に住んでいない人が家を買ったら、財務省への報告が要ります。",
    "1か月暮らすと、車が要るか、近所の人のこと、冷暖房に実際いくらかかるかが分かります。",
    "海外から来るなら、自治体のお試し住宅より、マンスリーの部屋か月割のある宿のほうが、たいてい現実的です。",
  ],
  "body": """
<p>akiya（空き家）は、ひとことで言えば、誰も住んでいない家のことです。2023年の住宅の調査では約900万戸と過去最多で、住宅全体の13.8%にあたります[[s:stat_housing2023]]。ただ、その中には、次の借り手や買い手を待っているだけの家もたくさんあります[[s:stat_housing2023]]。私たちの感覚では、「日本の放置された家」と言うときに指しているのは、貸すためでも売るためでも別荘でもない約386万戸のほうで、2018年の調査から増え続けています[[s:stat_housing2023]]。</p>

<h2>外国人は空き家を買えるのか</h2>
<p>買えます。日本に住んでいない人も買えます。変わったのは手続きのほうで、何をすればいいかは財務省の決まりに書かれています。2026年4月から、海外に住んだまま日本の不動産を買うと、住むための家でも、外為法にもとづいて財務省に報告することになりました[[s:mof_fefta2026,mof_realprop_faq]]。外国からの買い手向けの不動産サイト Real Estate Japan も、買うのに日本に住んでいる必要はないと、はっきり書いています[[s:rej]]。それから2026年10月5日からは、日本人も含めて、買った人はみな登記のときに国籍を届け出ます[[s:moj_nationality]]。</p>
<p>ただ、決まりはまだ動いています。国会に出ている法案は、一部の防衛関係施設と海上保安庁の施設の周り（おおむね1km）と、無人の国境離島に、新しい区域をつくる内容です[[s:cao_land_bill,cao_land_bill_outline]]。その区域で土地の所有権を移すときは、すべて事前に国の許可が要ります。施行は、公布から1年6か月以内です[[s:cao_land_bill_outline]]。2026年11月中旬の時点で、法案はまだ衆議院で審議中で、法律にはなっていません[[s:shugiin_bill18]]。気になる家がそうした施設の近くにあるなら、この法案は気にかけておきたいところです。</p>
<p>家とビザは、別々の問題として考えたほうがいいと私たちは思います。家を持つことで日本に長くいられるようになると期待しているなら、あてにする前に、在留資格（ビザ）の手続きを扱う行政書士に確かめておくと安心です。それに、決まりがこれだけ速く変わっているので、契約の前に、自分の場合を弁護士や司法書士に見てもらうのが賢明だと思います。</p>

<h2>なぜ、買う前にその町で暮らすのか</h2>
<p>家を買うこと自体は、簡単なほうです。本当に引き受けるのは町のほうで、物件情報から分かるのは、価格と間取りと何枚かの写真くらい。そこで楽しく暮らせるかを決めることは、しばらく住んでみて初めて見えてきます。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>知りたいこと</th><th>1か月暮らすと、こう分かる</th></tr></thead>
<tbody>
<tr><td>古い木造の家が1月にどれくらい寒いか、暖房にいくらかかるか</td><td>最初の寒い夜に体で分かり、電気代の請求で数字でも分かります。</td></tr>
<tr><td>車なしで毎日の暮らしが回るか</td><td>1週間、買い物や用事を徒歩・バス・自転車で済ませてみると、はっきりします。家のすぐ近くでは済まない用事も、あわせて試してみてください。</td></tr>
<tr><td>どこで食料を買うか、店は何時に閉まるか</td><td>食事をほとんど自炊していると、手に入りやすいものとそうでないものが、すぐに分かります。</td></tr>
<tr><td>その通りのごみの分別の仕組み</td><td>地域の収集カレンダーに合わせて、みんなと同じように出すことになります。英語版があれば、役所でもらっておくと便利です。</td></tr>
<tr><td>一日仕事をしても回線がもつか</td><td>ビデオ会議も含めて、いつもどおりに働いてみるのが一番の確かめ方です。</td></tr>
<tr><td>湿気の多い時期や台風で、建物がどうなるか</td><td>同じような家でどこから傷みやすいかは、近所の人や地元の工務店がよく知っています。</td></tr>
<tr><td>新しく来た人を、近所がどう迎えるか</td><td>あいさつをしたり、清掃の日があれば参加したり、先に移ってきた人にどうなじんだかを聞いたりすると、よく分かります。近所の人は小さなことにも気づきます。下田で回線の工事をしたとき、工事の車をどこに停めたかについて、近所の方から声をかけられました。</td></tr>
</tbody></table></div>
<p>どれも、内見では出てこないことばかりです。</p>

<h2>古い家で、住んでみて初めて分かることは何か</h2>
<p>私たちの経験では、配線と回線です。創業メンバーの1人が、下田の古い部屋を持ち主から借りて、宿に改修したときに知りました。買ったのではなく借りた部屋ですが、買った人も同じことにぶつかると私たちは思います。</p>
<p>古い2芯の配線では、エアコンと冷蔵庫と電子レンジを同時に使えず、ゲストに同時に使わないようお願いすることになりました。配線をやり直すにはそれなりの費用がかかるので、予算を組む前に知っておきたいことです。インターネットの回線工事は、繁忙期だったこともあって申し込みから2か月以上かかり、それまでは置き型のホームルーターでしのぎました。</p>
<p>配線と回線工事の待ちは、もっと大きな話の小さな例です。安い古い家では、売り出し価格は、かかるお金の一部にすぎません。改修、税金、保険、維持費が上乗せされ、建物ごとに大きく変わるので、本当の金額は書面の見積もりを取って初めて分かります。</p>

<h2>町をじっくり試すには、どんな滞在のしかたがあるか</h2>
<p>多くの人には2つあります。ビザなしの短期滞在と、6か月のデジタルノマドの在留資格です。どちらも就労ビザや日本への移住は要らず、町に落ち着いて自分に合うかを確かめるのに十分な期間があります。下の条件は2026年11月時点のものです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>滞在のしかた</th><th>期間</th><th>対象</th></tr></thead>
<tbody>
<tr><td><strong>短期滞在</strong>（ビザ免除）</td><td>ビザ免除の国・地域の多くは90日まで。15日・30日・180日の国もあります[[s:jnto_visa]]。</td><td>ビザ免除の国・地域の人。この滞在では報酬を得る仕事はできません。大事なのは、自分のパスポートの条件です[[s:jnto_visa]]。</td></tr>
<tr><td><strong>デジタルノマド</strong>の在留資格</td><td>6か月で、更新はできません。出国後6か月たてば、もう一度申請できます[[s:isa_nomad_en]]。</td><td>ビザ免除で、かつ日本と租税条約のある国・地域の人[[s:isa_nomad_list]]。年収1,000万円以上と、治療費1,000万円以上を補償する民間の医療保険が必要で、日本の会社に雇われて働くことはできません[[s:isa_nomad_en]]。</td></tr>
</tbody></table></div>
<p>デジタルノマドの在留資格が合いそうなら、[[l:ja-digital-nomad|日本のデジタルノマドビザの記事]]に、対象になる人と仕組みをくわしくまとめています。</p>
<p>延長、もっと長い在留資格、いったん出国してまた来る場合のことは、[[l:ja-how-long-stay|日本に何日いられるかのガイド]]にまとめました。</p>
<p class="fine">これは一般的な情報で、在留手続きの助言ではありません。デジタルノマドの対象の国は変わるので、自分のパスポートで確かめてください。</p>

<h2>町を試すために1か月泊まれる場所はどこか</h2>
<p>おもな選択肢は、自治体のお試し住宅、マンスリーの部屋、月割のある宿の3つです。どれが合うかは、町と、どこから来るかによります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>選択肢</th><th>期間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>自治体のお試し住宅</strong></td><td>町によって、1〜2日から数か月まで。2年近く住める市もあります[[s:shizuoka_trial,minamialps_trial,shizuoka_long_trial]]</td><td>決まりは町ごとで、多くは移住するつもりの人向け。南アルプス市は1〜3か月、月21,000円で貸しています（2026年2月）[[s:minamialps_trial]]。</td></tr>
<tr><td><strong>マンスリーの部屋</strong></td><td>1か月以上</td><td>家具付きの部屋を月単位で借ります。小さな町では選べる数が少ないこともあるので、早めに探すと安心です。</td></tr>
<tr><td><strong>月割のある宿・貸別荘</strong></td><td>1週間〜1か月以上</td><td>海外からいちばん予約しやすいことが多く、何も契約せずにその町での暮らしを試せます。</td></tr>
</tbody></table></div>
<p>お試し住宅はよさそうに見えますが、落とし穴があります。移住する人のための仕組みで、海外から町を試しに来る人向けではないのです。南アルプス市のお試し住宅は、山梨県の外に住民登録があり、市に移住するつもりで、移住の相談に登録した人が対象です[[s:minamialps_trial]]。国籍は条件に挙げられていないので、海外に住んでいるなら、対象に入るかは市の移住の窓口に聞けば分かります。</p>
<p>はっきり書いている市もあります。静岡市の「長期お試し住宅」は、市営住宅に半年以上2年未満住めるものです。対象は、静岡県の外に住んでいて、市への移住を決めた、または準備している人。外国籍の人は、さらに永住者・定住者・特別永住者の在留資格か、日本人の配偶者や子であることが条件です（2026年8月）[[s:shizuoka_long_trial]]。つまり、観光やデジタルノマドの滞在では入れません。</p>
<p>だから海外から来るなら、マンスリーの部屋か宿のほうが、たいてい現実的だと私たちは思います。マンスリーの仕組みは、[[l:ja-monthly-rental|日本のマンスリーの部屋の記事]]にくわしく書いています。どうしてもお試し住宅を使いたいなら、まずは町の移住の窓口に連絡するのが近道です。</p>
<p>下田市は別のやり方です。2026年4月施行の要綱で、移住を考えている人が市の指定する宿に泊まると、宿泊料の半分を補助しています[[s:shimoda_stay_subsidy]]。対象は10泊までで、1泊4,000円までです[[s:shimoda_stay_subsidy]]。ただ、静岡県の外で日本に住民登録がある人が対象なので、海外から来る場合は使えません[[s:shimoda_stay_subsidy]]。</p>
<p>東京から行きやすい町のほうが、行き来が大ごとにならないぶん試しやすいです。[[l:ja-izu|伊豆半島]]の下田もその1つで、東京駅から毎日走る直通の電車なら2時間29〜44分です[[s:jre_tt_tokyo]]。これは2026年11月時点の時刻表で、くわしくは[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>下田が候補に入っているなら、私たちが下田で営んでいる小さな宿「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」を、町の様子をつかむあいだの拠点にしてもらえます。旧町内のアパートの一室（約40㎡）を改装したもので、伊豆急下田駅から歩いて8分です[[s:node_room,node_access]]。公式サイトでは中長期の滞在にも便利な宿として紹介していて[[s:node_site]]、旅館業法の許可を受けています。これまでのゲストは欧米の人が中心で、リモートで働きに来る人もいます。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|下田の旧町内にある私たちの部屋「NODE Shimoda」のリビング。]]

<h2>お試しの1か月は、どんなふうに過ぎるか</h2>
<p>ほとんどは、ふだんの暮らしそのものです。そこに、いくつか意識して試すことを入れます。下田で私たちがつまずいたことをもとに、週ごとにおおよそこう組み立てると思います。</p>
<p>最初の1週間は、落ち着くための時間です。スーパー、診療所、バス停、ごみの収集日を覚えます。古い建物に泊まっているなら、泊まり先の人に、電気の契約のアンペア数とブレーカーの場所を聞いておくと安心です。下田の私たちの部屋の古い配線では、エアコンと冷蔵庫と電子レンジを同時に使えませんでした。アンペア数が分かれば、一度にどれくらい使えるかの見当がつきます。ブレーカーの場所を知っていれば、落ちてもすぐに戻せます。</p>
<p>2週目には、いつもの時間に働き、家で料理をするようになります。ビデオ会議の続く一日に回線がもつか、冷暖房に実際いくらかかるかが分かるのはこの頃です。地元の回線業者に、そこで新しく回線を引くとどれくらいかかるかを聞いておくのもいい時期です。私たちのときは2か月以上かかりました。</p>
<p>3週目は、聞いてまわる週です。役所の空き家の窓口に行ったり、地元の不動産屋と話したり、工務店に古い家の配線のやり直しがおおよそいくらかを聞いたりできます。湿気の多い夏や台風で家がどうなるかは、近所の人がいちばんよく知っています。</p>
<p>4週目には、家について、そして自分の暮らし方について、何を変える必要がありそうか、だいたい見えています。費用や迷いを忘れないうちに書きとめておくと、町どうしを比べるときにも、見送ると決めるときにも、ずっと楽になります。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
    ("外国人は日本の不動産を買えますか",
     "買えます。日本に住んでいない人も買うことができ、2026年4月からは、外為法にもとづいて財務省に報告することになりました。買った人はみな、登記のときに国籍も届け出ます[[s:mof_fefta2026,moj_nationality]]。決まりが変わりつつあるので、自分の場合は弁護士や司法書士に見てもらうと安心です。"),
    ("日本で家を持つと、ビザを取りやすくなりますか",
     "あてにしないほうがいいと私たちは思います。家とビザは別々の問題として考えているので、長く住むことも計画に入っているなら、買う前に、在留資格（ビザ）の手続きを扱う行政書士に聞いてみてください。"),
    ("日本の安い家は、本当に安いのですか",
     "そうとは限りません。購入価格は、かかるお金の一部です。改修、税金、保険、維持費が上乗せされます。金額は建物によって大きく変わるので、決める前に知るには、書面の見積もりを取るしかありません。"),
    ("外国人でも、自治体のお試し住宅を使えますか",
     "町しだいです。お試し住宅は、多くが移住するつもりの人向けで、対象をはっきり書いている町もあります。たとえば静岡市の長期お試し住宅は、2026年8月時点で、外国籍の人なら、永住者・定住者・特別永住者の在留資格か、日本人の配偶者や子である場合に限られていました[[s:shizuoka_long_trial]]。いまの決まりは、町の移住の窓口が知っています。"),
    ("日本に空き家は何戸ありますか",
     "2023年の住宅・土地統計調査によると、約900万戸です[[s:stat_housing2023]]。住宅全体の13.8%にあたり、過去最高です。"),
  ],
 },
},
# ============================================================ 伊豆
{
 "id": "izu-from-tokyo", "slug": "izu-peninsula-from-tokyo", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("train-window-sea", "The sea and breaking waves seen through a train window", ""),
 "published": "2026-11-14", "updated": "2026-11-19",
 "kicker": "Izu Peninsula",
 "h1": "Izu Peninsula from Tokyo: trains, fares and why to stay a week",
 "seo_title": "Izu Peninsula from Tokyo: Trains, Fares and Where to Stay",
 "description": "Direct trains reach Shimoda from Tokyo in about 2½ hours, for about ¥6,660 with a reserved seat. The Japan Rail Pass covers JR to Ito; beyond, you pay Izukyu.",
 "dek": "Southern Izu is too far for a day trip but just right for a week. Direct trains take you from Tokyo to Shimoda in about 2½ hours.",
 "card": "Direct trains reach Shimoda from Tokyo in about 2½ hours, for about ¥6,660 one way with a reserved seat. The south of Izu is a long way for a day, but just right for a week.",
 "keywords": [("izu peninsula from tokyo", "260", "7"), ("tokyo to izu peninsula", "260", "—")],
 "intent": "Do（やり方を知りたい）",
 "points": [
   "Shimoda is about 2½ hours on the direct Odoriko, about ¥6,660 with a reserved seat (November 2026).",
   "Shuzenji is about two hours direct, or about 50 minutes by Shinkansen to Mishima plus a 35-minute local line.",
   "The Japan Rail Pass covers JR to Ito and Mishima; beyond, you pay the fare and limited-express charge.",
 ],
 "body": """
<h2>How do you get to the Izu Peninsula from Tokyo?</h2>
<p>The easiest way is the Odoriko limited express. It runs from Tokyo down the east coast of the [[l:izu|Izu Peninsula]] all the way to Shimoda, so you can settle in for the whole ride without changing trains. Five leave Tokyo each day, on the hour between 9:00 and 13:00 [[s:jre_tt_tokyo]]. You’ll reach Ito in about 1 hour 40 minutes and Izukyu-Shimoda in about two and a half hours [[s:jre_tt_tokyo]].</p>
<p>If you’re heading inland to Shuzenji, the Shinkansen and a short local line often suit you better. The table below compares the four routes.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Route</th><th>Changes</th><th>Time</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Direct Odoriko</strong> to Ito and Izukyu-Shimoda</td><td>None</td><td>About 1 h 40 min to Ito, 2 h 29 min to 2 h 44 min to Shimoda [[s:jre_tt_tokyo]]</td><td>Five a day, leaving Tokyo at 9:00, 10:00, 11:00, 12:00 and 13:00, with extra trains on set days [[s:jre_tt_tokyo]]. The 11:00 is the Saphir Odoriko, which only has Green Car and premium seats [[s:izukyu_express]].</td></tr>
<tr><td><strong>Shinkansen to Atami</strong>, then a local train to Shimoda</td><td>One, at Atami</td><td>43 to 45 min to Atami by Kodama, then 1 h 29 min to 1 h 49 min to Shimoda [[s:jre_tt_tokyo]]</td><td>With a good connection, it can beat the direct train. The 6:30 Kodama and the 7:23 local from Atami get you to Shimoda at 8:52, in 2 h 22 min [[s:jre_tt_tokyo]].</td></tr>
<tr><td><strong>Shinkansen to Mishima</strong>, then the Izuhakone Railway to Shuzenji</td><td>One, at Mishima</td><td>50 to 53 min to Mishima by Kodama [[s:jre_tt_tokyo]], then about 35 min to Shuzenji [[s:izuhakone_tt]]</td><td>Local trains to Shuzenji run about three times an hour for most of the day [[s:izuhakone_tt]], so the change at Mishima is easy to fit in.</td></tr>
<tr><td><strong>Direct Odoriko</strong> to Shuzenji</td><td>None</td><td>2 h 6 min to 2 h 8 min [[s:jre_tt_tokyo]]</td><td>Two a day, leaving Tokyo at 9:00 and 12:00. A third, at 10:30, runs only on set days [[s:jre_tt_tokyo]].</td></tr>
</tbody></table></div>
<p class="fine">Times are from JR East’s Tokyo Station timetables for November 2026 and the Izuhakone Railway’s Sunzu Line timetable. Timetables change with the seasons, so it’s a good idea to look up the times for your travel date.</p>
<p>What about the bus? Tokai Bus doesn’t run a highway bus from Tokyo to Shimoda or Shuzenji. The closest you’ll get is its Mishima Express from Shinjuku to Mishima, from ¥2,300 one way [[s:tokaibus_highway]]. From there, the Izuhakone Railway takes you on to Shuzenji [[s:izuhakone_tt]]. For Shimoda, the train really is the simple answer.</p>

<h2>How much does the train from Tokyo to Izu cost?</h2>
<p>To Shimoda on the direct Odoriko, you’ll pay about ¥6,660 one way with a reserved seat. That’s the ¥4,280 fare plus a ¥2,380 seat charge [[s:izukyu_fares,izukyu_express]]. It’s worth buying the seat before you board, because it costs more on the train [[s:izukyu_express]]. If you’re mixing routes or using a rail pass, the table below breaks down the other fares and charges.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What you pay</th><th>One way, adult</th></tr></thead>
<tbody>
<tr><td>Fare, Tokyo to Izukyu-Shimoda</td><td>¥4,280 (¥4,276 with an IC card) [[s:izukyu_fares]]</td></tr>
<tr><td>Fare, Tokyo to Ito</td><td>¥2,420, plus a seat charge on the Odoriko [[s:izukyu_fares]]</td></tr>
<tr><td>Odoriko seat charge, Tokyo to Shimoda</td><td>¥2,380 bought before boarding, ¥2,640 on the train [[s:izukyu_express]]</td></tr>
<tr><td>Saphir Odoriko Green Car charge, Tokyo to Shimoda</td><td>¥6,260 in the normal season, up to ¥400 more at the busiest times and ¥200 less in quiet ones [[s:izukyu_express]]</td></tr>
<tr><td>Shinkansen charge, Tokyo to Atami</td><td>¥2,290 reserved, ¥1,760 unreserved, in the normal season, on top of the fare [[s:izukyu_express]]</td></tr>
<tr><td>Local train, Atami to Shimoda</td><td>¥2,210 [[s:izukyu_fares]]</td></tr>
<tr><td>Izu Kyuko line, Ito to Shimoda</td><td>¥1,860 (¥1,856 with an IC card) [[s:izukyu_fares]]</td></tr>
<tr><td>Izuhakone Railway, Mishima to Shuzenji</td><td>¥550 [[s:izuhakone_fares]]</td></tr>
</tbody></table></div>
<p class="fine">Fares and charges as of November 2026. Izukyu’s fares are from its table revised on 14 March 2026. The Izuhakone Railway applied in October 2026 to raise its fares, with the change on the Mishima–Shuzenji line planned for spring 2027 [[s:izuhakone_fare2026]].</p>

<h2>Can you use the Japan Rail Pass to get to Izu?</h2>
<p>Yes, as far as Ito and Mishima. The pass covers ordinary cars on JR lines, including Kodama Shinkansen trains and limited expresses like the Odoriko [[s:jrp_conditions,jrp_vehicle]]. South of Ito, the line belongs to Izukyu, and from Mishima to Shuzenji it’s the Izuhakone Railway. On those stretches you pay the fare and charges yourself, even if you stay on the same Odoriko [[s:jrp_route]].</p>
<p>So on an ordinary pass to Shimoda, you’ll still pay Izukyu for the last leg. That’s ¥1,860 from Ito, plus Izukyu’s limited express charge of ¥800, which is the same for any distance on its line [[s:izukyu_fares,izukyu_express]]. To Shuzenji, it’s ¥550 from Mishima on a local train [[s:izuhakone_fares]]. If you sit in a Green Car on an ordinary pass, you pay the Green Car charge and the limited express charge too [[s:jrp_conditions]]. That matters most on the Saphir Odoriko, which has no ordinary seats at all [[s:izukyu_express]].</p>
<p>As of November 2026, a 7-day ordinary pass costs adults ¥50,000 online, or ¥53,000 through an overseas agent [[s:jrp_price]]. It’s mainly for visitors who enter Japan as a “Temporary Visitor”, and the official site sets out who else qualifies [[s:jrp_eligibility]]. With a Tokyo–Shimoda trip at about ¥6,660 each way, we think the pass only pays off when Izu is one stop on a longer journey around Japan.</p>

<h2>Is the Izu Peninsula a day trip from Tokyo?</h2>
<p>The north is, but the south really isn’t. Even on the direct train, Shimoda is about two and a half hours from Tokyo [[s:jre_tt_tokyo]], so a return trip means about five hours on the train for a few hours on the beach. Atami and Ito are a different story. Atami is about 45 minutes by Shinkansen, and Ito is under two hours on the direct train, so we think both work well as day trips. The south coast and the inland hot-spring towns, in our experience, are far better if you stay a few nights and let the days slow down.</p>

<h2>Which Izu town suits you?</h2>
<p>It mostly comes down to how far you want to go and how long you can stay.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Town</th><th>From Tokyo</th><th>What it’s like</th><th>Day trip or stay?</th></tr></thead>
<tbody>
<tr><td><strong>Atami and Ito</strong></td><td>Atami 43–45 min by Shinkansen; Ito about 1 h 40 min direct</td><td>The two towns nearest Tokyo, on the east coast.</td><td>A day trip works</td></tr>
<tr><td><strong>Shuzenji</strong></td><td>50–53 min to Mishima, then about 35 min; or about 2 h direct</td><td>An inland hot-spring town, said to be the oldest in Izu. You can look at the Tokko-no-yu spring but not bathe in it, and there are two foot baths nearby, Kawara-yu and Sugi-no-yu [[s:izu_tokko]]. It suits a quiet night or two more than a rushed visit.</td><td>Better to stay</td></tr>
<tr><td><strong>Shimoda</strong></td><td>2 h 29 min to 2 h 44 min direct</td><td>A port town at the southern tip, with nine official swimming beaches in 2026 [[s:shimoda_beach2026_city]]. The prefecture calls Shimoda Japan’s top port for landing [[l:kinmedai|kinmedai]] [[s:pref]]. In our view, it’s the town that suits a week best, and our [[l:shimoda-guide|Shimoda guide]] covers how to spend one.</td><td>Better to stay</td></tr>
</tbody></table></div>

<h2>Can you get around southern Izu without a car?</h2>
<p>Yes, for the town and the nearby beaches. Shirahama Beach is about 15 minutes by bus from Izukyu-Shimoda Station, on a bus bound for Itadoichiki [[s:jnto]]. Tokai Bus sells two-day passes that cover most of what you’d want to see, valid on the day you buy them and the next [[s:tokaibus_freepass]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Pass</th><th>Adult price</th><th>Where it takes you</th></tr></thead>
<tbody>
<tr><td><strong>Shimoda 2-day pass</strong></td><td>¥1,350</td><td>Shimoda town, Ryugu cave, Tsumekizaki and Shirahama [[s:tokaibus_freepass]]</td></tr>
<tr><td><strong>Irozaki–Shimoda 2-day pass</strong></td><td>¥2,850</td><td>All of the above, plus Cape Irozaki, Yumigahama, Shimokamo, Kawazu and Inatori [[s:tokaibus_freepass]]</td></tr>
</tbody></table></div>
<p>You can buy both at Tokai Bus’s office by Shimoda Station. It’s open every day from 8:45 to 17:00, with a lunch break from 12:30 to 13:30 [[s:tokaibus_freepass]]. Buses to the outer beaches don’t run often, so check the return times before you head out. If you want to hop between several beaches in one day, an e-bike or a rental car makes life much easier.</p>

<h2>When is the best time to visit the Izu Peninsula?</h2>
<p>For swimming in Shimoda, the 2026 season ran from mid-July to late August. For a quieter stay, we’d pick the months either side.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>When</th><th>What to expect</th></tr></thead>
<tbody>
<tr><td>Swimming season in Shimoda (in 2026, from 18 July to between 23 and 31 August, depending on the beach)</td><td>All nine of Shimoda’s official beaches opened on 18 July 2026, mostly from 8:00 to 16:00. Shirahama Ohama and Kujuppama stayed open until 31 August and Shirahama Chuo until 30 August, but the other six closed on 23 August [[s:shimoda_beach2026_city]]. Outside the season and those hours, there are no lifeguards [[s:shimoda_ohama]].</td></tr>
<tr><td>The rest of the year</td><td>We find the towns much quieter then, and it’s the easiest time for hot springs and long walks.</td></tr>
</tbody></table></div>
<p class="fine">The city sets the beach dates each year, so if you’re planning a late-August trip, check which beaches will still be open before you book.</p>

<h2>Why stay a week in Izu rather than a night?</h2>
<p>A week turns a trip into ordinary life, and that’s when the slow pace of the south starts to make sense. A hotel room is built around one or two nights and a set dinner time. A place with a kitchen and a washing machine lets you work in the morning, head to the beach or a hot spring in the afternoon, and eat in when you don’t feel like going out.</p>
[[img:node-shimoda|Living room with a sofa, low table and sliding paper screens|The living room of NODE Shimoda, eight minutes on foot from Izukyu-Shimoda Station.]]
<p>If you’d like to try that in Shimoda, our apartment in the old town, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, is set up for that kind of week. It’s about 40 m² on the first floor, with a work desk, a washing machine and gas dryer, and a kitchen with cookware [[s:node_room]]. It’s eight minutes’ walk on the flat from Izukyu-Shimoda Station, with a convenience store two minutes away and a supermarket three [[s:node_access]]. Most of our guests come from abroad, some to work remotely and some to surf, and in summer more of them stay longer.</p>
<p>If a week in Izu gets you thinking about a longer stay, or even a house of your own, here’s why we suggest [[l:akiya-try-first|living in a town for a month before buying a house]].</p>
""",
 "faq": [
   ("How long does it take to get from Tokyo to Shimoda?",
    "About two and a half hours on the direct Odoriko limited express [[s:jre_tt_tokyo]]. In the November 2026 timetable, five run a day. They leave Tokyo on the hour between 9:00 and 13:00 [[s:jre_tt_tokyo]]."),
   ("How much is the train from Tokyo to Shimoda?",
    "About ¥6,660 one way on the Odoriko with a reserved seat. That’s the ¥4,280 fare plus a ¥2,380 seat charge, if you buy the seat before you board [[s:izukyu_fares,izukyu_express]]. Those are November 2026 prices."),
   ("Can I use the Japan Rail Pass to get to Izu?",
    "Yes, on JR as far as Ito and Mishima. From Ito to Izukyu-Shimoda and from Mishima to Shuzenji, you pay the fare and charges separately, even on the Odoriko [[s:jrp_route]]. A week-long ordinary pass costs ¥50,000 online, as of November 2026 [[s:jrp_price]]."),
   ("What’s the best way to get to Shuzenji?",
    "For most people, we think the Shinkansen to Mishima is the easiest way: 50 to 53 minutes on a Kodama [[s:jre_tt_tokyo]]. From there, the Izuhakone Railway gets you to Shuzenji in about 35 minutes for ¥550 [[s:izuhakone_tt,izuhakone_fares]]. If you’d rather not change, two direct Odoriko trains run every day, at 9:00 and 12:00, and take about two hours [[s:jre_tt_tokyo]]."),
   ("Is there a bus from Tokyo to Shimoda?",
    "Tokai Bus doesn’t run one. Its highway buses go to Mishima instead, including the Mishima Express from Shinjuku from ¥2,300 [[s:tokaibus_highway]]. For Shimoda, the train really is the simple answer."),
   ("Do I need a car on the Izu Peninsula?",
    "Not for Shimoda town and the nearby beaches. Shirahama is about 15 minutes by bus from the station [[s:jnto]], and Tokai Bus’s two-day Shimoda pass costs ¥1,350 [[s:tokaibus_freepass]]. A car only really helps when you want to hop between beaches."),
 ],
 "sources": ["jre_tt_tokyo", "izukyu_fares", "izukyu_express", "izuhakone_tt", "izuhakone_fares", "izuhakone_fare2026",
             "jrp_route", "jrp_conditions", "jrp_vehicle", "jrp_price", "jrp_eligibility",
             "tokaibus_highway", "tokaibus_freepass", "jnto", "izu_tokko", "shimoda_beach2026_city", "shimoda_ohama", "pref",
             "node_room", "node_access"],
 "related": ["kinmedai", "izu", "akiya-try-first"],
 "ja": {
  "h1": "東京から伊豆半島へ：電車・運賃と、1週間泊まる理由",
  "dek": "伊豆半島の南は、日帰りには遠いけれど、1週間ならちょうどいい距離です。東京から直通の特急に乗れば、下田まで2時間半ほどです。",
  "review": [
   "2026-11-20 見せ方のリライト: 人の方針「ガイドブックのような固い文章は読みづらい」に合わせて、語り口だけを直しました（事実・数値・出典・リンク・写真・体験は変えていません）。①1文に数字や条件を詰めた文を分けました（詰め込みすぎの文 12件→0件）。細かい所要時間は表に任せ、本文は「伊東まで1時間40分ほど、下田まで2時間半ほど」に ②伊豆急行の運賃表・料金表の日付（2026年3月14日改定・2025年2月1日以降）は、本文から表の下の注に移しました ③dek と FAQ の所要時間を「約2時間半」に（正確な2時間29〜44分は表に残しています）。特急券は乗る前に買うほうが安い、日帰りより何泊か、といった読み手にとっての意味を添えました ④updated を 2026-11-20 に",
   "【2026-11-19 合格（91点）のあとの言い方の直し（事実・出典は変えていない）】①パスの使える人を「おもに『Temporary Visitor』のスタンプで入国した人。ほかの条件は公式サイトで」に（海外に住む日本人の条件を落とさないため）②修善寺の550円に「普通列車で」を付けました ③In short の3項目目を「その先は運賃と特急料金を払う」に ④出典のない見解（熱海・伊東は日帰り向き、南は泊まるほうがずっといい、それ以外の時期は町が静か）を、私たちの見方・実感と分かる形にしました",
   "【2026-11-17 品質保証部（86点）の指摘での2回目の直し】変えた点: ①ジャパン・レール・パスの節を新しく作りました（JAPAN RAIL PASS の公式で確認）。JR の普通車（こだまや踊り子などの特急を含む）にパスで乗れる＝伊東・三島まで。伊東〜伊豆急下田（伊豆急行）と三島〜修善寺（伊豆箱根鉄道）は、同じ踊り子に乗ったままでも運賃・料金を別に払う。下田まで行くなら伊東〜下田の1,860円と、伊豆急行線内の特急料金800円（区間にかかわらず同じ）。修善寺へは三島から550円。普通車用のパスでグリーン車に乗るとグリーン料金と特急料金が要り、サフィール踊り子は普通車がない。値段は2026年11月に公式サイトで見た値（7日間の普通車、オンラインで大人50,000円、海外の代理店で53,000円）。使えるのは「短期滞在（Temporary Visitor）」で入国した人だけ。「東京〜下田が片道約6,660円なので、伊豆だけならパスは元が取れず、日本を長く回る旅の途中なら」という私たちの見方を1文。FAQ にも1問足しました。ワイド・パスなどほかのきっぷは書いていません ②運賃の表に、伊豆急行の同じ運賃表にある東京〜伊東 2,420円を足しました（踊り子の特急料金は別）。熱海・三島までの JR の運賃は公式の表で取れないので書いていません ③冒頭で値段に答えるよう、In short を「下田は直通の踊り子で約2時間半、指定席で約6,660円（2026年11月）」「修善寺」「ジャパン・レール・パスは伊東・三島まで、その先は伊豆急行・伊豆箱根鉄道の運賃」の3つにしました（海水浴と路線バスの項目は本文に） ④正確性: 運賃（2026年3月14日改定）と特急料金（2025年2月1日以降の乗車分の料金表）の時点を分けて書きました。「半島のおもなバス会社」を消し「東海バスは東京から下田・修善寺への高速バスを走らせていない」に。海水浴の期間は「下田で、2026年は7月中旬〜8月下旬」と場所と年を付けました（季節の表の見出しも） ⑤独自性: 町の表の熱海・伊東の行を短くしました。experience.md の確認済みの節（ゲストの層: 訪日客が中心、ワーケーションやサーフィンの人もいる、夏は長期滞在が多め）を NODE Shimoda の段落に1文入れました ⑥トーン: description の後半を目次から答え（パスは伊東まで、その先は伊豆急行に払う）に。「私たちは思う／見ている」を減らし（見解の形は、パスの元が取れるか・下田が1週間に合う・季節の選び方など4か所に）、「〜だろうと見ています」の推測文（三島で乗り換える人が多いだろう・シーズン前後は人が少ないだろう）をなくしました。季節の表の「シーズンの前後」の行は外しました ⑦出典: jre_tt_tokyo と node_access は content.py にあるので SOURCES_NEW から外しました。JAPAN RAIL PASS の公式（jrp_route・jrp_conditions・jrp_vehicle・jrp_price・jrp_eligibility）を足しました。updated を 2026-11-17 に",
   "【2026-11-16 手離れでの書き直し（事実・出典の変更あり）】変えた点: 黄色い枠を4つともなくしました。運賃を伊豆急行・伊豆箱根鉄道の公式の運賃表に（japan-guide の改定前の目安をやめた）。三島〜修善寺は公式の時刻表で約35分、値上げは2027年春の予定（公式の申請のお知らせ）。直行バスは「東海バスにはない」まで。車なしで回る節（白浜までバスで約15分、下田2日券1,350円・石廊崎・下田2日券2,850円）を新しく作りました。修善寺の足湯（河原湯・杉の湯）は伊豆市の公式で確認。修善寺の所要時間を「直通で約2時間、または新幹線で三島まで約50分＋35分」に直しました。東京〜下田は JR東日本の時刻表（2026年11月）の2時間29〜44分にそろえました。NODE Shimoda は公式サイトどおり「アパートの一室」・約40㎡・2階・徒歩8分に。浜からの最終バスと Wi-Fi の実測は書いていません",
   "【人に確かめてほしい点】①変わりやすい数字: 運賃・特急料金（伊豆急行・伊豆箱根鉄道、2026-11-16 確認）、ジャパン・レール・パスの値段と利用条件（公式、2026-11-17 確認。利用条件は2026年4月時点の記載）、時刻（JR東日本 2026年11月・伊豆箱根鉄道 2025年3月改正）、東海バスのきっぷと三島エクスプレスの値段（2026-11-16 確認）、2026年の下田の海水浴場の期間",
  ],
  "points": [
    "下田へは直通の踊り子で約2時間半、指定席で約6,660円です（2026年11月）。",
    "修善寺は直通で約2時間。または新幹線で三島まで約50分、そこからローカル線で35分です。",
    "ジャパン・レール・パスは伊東と三島までの JR で使えます。その先は、運賃と特急料金を払います。",
  ],
  "body": """
<h2>東京から伊豆半島へは、どう行くか</h2>
<p>いちばん簡単なのは、特急「踊り子」です。東京から[[l:ja-izu|伊豆半島]]の東海岸を下田まで走るので、乗り換えなしで、座ったままのんびり向かえます。東京を出るのは毎日5本で、9時から13時まで毎時ちょうどです[[s:jre_tt_tokyo]]。伊東までは1時間40分ほど、伊豆急下田までは2時間半ほどで着きます[[s:jre_tt_tokyo]]。</p>
<p>内陸の修善寺へ行くなら、新幹線と短いローカル線のほうが合うことが多いです。行き方ごとの細かい時間は、表にまとめました。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>行き方</th><th>乗り換え</th><th>所要時間</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>直通の「踊り子」</strong>で伊東・伊豆急下田へ</td><td>なし</td><td>伊東まで約1時間40分、下田まで2時間29分〜2時間44分[[s:jre_tt_tokyo]]</td><td>毎日5本で、東京を9:00・10:00・11:00・12:00・13:00に出ます。決まった日だけ走る列車もあります[[s:jre_tt_tokyo]]。11:00発は「サフィール踊り子」で、グリーン車とその上の席だけの列車です[[s:izukyu_express]]。</td></tr>
<tr><td><strong>新幹線で熱海</strong>へ出て、普通列車で下田へ</td><td>1回（熱海）</td><td>こだまで熱海まで43〜45分、熱海から下田まで1時間29分〜1時間49分[[s:jre_tt_tokyo]]</td><td>乗り継ぎがよければ、直通より速く着くこともあります。こだま6:30発、熱海7:23発の普通に乗り継ぐと、下田に8:52に着きます（2時間22分）[[s:jre_tt_tokyo]]。</td></tr>
<tr><td><strong>新幹線で三島</strong>へ出て、伊豆箱根鉄道で修善寺へ</td><td>1回（三島）</td><td>こだまで三島まで50〜53分[[s:jre_tt_tokyo]]、三島から修善寺まで約35分[[s:izuhakone_tt]]</td><td>修善寺行きの普通は、昼間はだいたい1時間に3本あるので[[s:izuhakone_tt]]、三島での乗り換えは組みやすいです。</td></tr>
<tr><td><strong>直通の「踊り子」</strong>で修善寺へ</td><td>なし</td><td>2時間6分〜2時間8分[[s:jre_tt_tokyo]]</td><td>毎日2本で、東京を9:00と12:00に出ます。10:30発の3本目は、決まった日だけです[[s:jre_tt_tokyo]]。</td></tr>
</tbody></table></div>
<p class="fine">時刻は、JR東日本の東京駅の時刻表（2026年11月）と、伊豆箱根鉄道の駿豆線の時刻表によります。時刻表は季節で変わるので、乗る日の時刻を調べておくと安心です。</p>
<p>バスはどうでしょう。東海バスは、東京から下田や修善寺への高速バスを走らせていません。いちばん近いのは新宿から三島までの「三島エクスプレス」で、片道2,300円からです[[s:tokaibus_highway]]。三島からは、伊豆箱根鉄道で修善寺へ行けます[[s:izuhakone_tt]]。下田へは、やはり電車がいちばん簡単です。</p>

<h2>東京から伊豆までの電車代は、いくらか</h2>
<p>直通の「踊り子」で下田まで、指定席で片道約6,660円です。運賃4,280円に、特急料金2,380円を足した額です[[s:izukyu_fares,izukyu_express]]。特急券は車内で買うと高くなるので、乗る前に買っておくのがおすすめです[[s:izukyu_express]]。ほかの行き方を組み合わせるときや、レールパスを使うときは、下の表を見てください。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>払うもの</th><th>片道・大人</th></tr></thead>
<tbody>
<tr><td>運賃（東京〜伊豆急下田）</td><td>4,280円（IC カードは4,276円）[[s:izukyu_fares]]</td></tr>
<tr><td>運賃（東京〜伊東）</td><td>2,420円。踊り子に乗るなら特急料金が別に要ります[[s:izukyu_fares]]</td></tr>
<tr><td>踊り子の特急料金（東京〜下田）</td><td>乗る前に買うと2,380円、車内で買うと2,640円[[s:izukyu_express]]</td></tr>
<tr><td>サフィール踊り子のグリーン（東京〜下田）</td><td>通常期6,260円。いちばん混む時期は最大400円高く、すいている時期は200円安くなります[[s:izukyu_express]]</td></tr>
<tr><td>新幹線の特急料金（東京〜熱海）</td><td>通常期で指定席2,290円、自由席1,760円。運賃は別です[[s:izukyu_express]]</td></tr>
<tr><td>普通列車（熱海〜下田）</td><td>2,210円[[s:izukyu_fares]]</td></tr>
<tr><td>伊豆急行線（伊東〜下田）</td><td>1,860円（IC カードは1,856円）[[s:izukyu_fares]]</td></tr>
<tr><td>伊豆箱根鉄道（三島〜修善寺）</td><td>550円[[s:izuhakone_fares]]</td></tr>
</tbody></table></div>
<p class="fine">2026年11月時点の運賃・料金です。伊豆急行の運賃は2026年3月14日に改定された運賃表によります[[s:izukyu_fares,izukyu_express]]。伊豆箱根鉄道は2026年10月に運賃の値上げを申請していて、三島〜修善寺の線は2027年春に変わる予定です[[s:izuhakone_fare2026]]。</p>

<h2>伊豆へ行くのに、ジャパン・レール・パスは使えるか</h2>
<p>使えます。ただし伊東と三島までです。パスでは、こだまの新幹線や踊り子のような特急を含め、JR の線の普通車に乗れます[[s:jrp_conditions,jrp_vehicle]]。伊東より南は伊豆急行の線、三島から修善寺までは伊豆箱根鉄道の線で、この区間は、同じ踊り子に乗ったままでも、運賃と料金を自分で払います[[s:jrp_route]]。</p>
<p>つまり、普通車用のパスで下田へ行っても、最後の区間は伊豆急行に払うことになります。伊東から1,860円と、伊豆急行線内の特急料金800円です。特急料金は、区間にかかわらず同じです[[s:izukyu_fares,izukyu_express]]。修善寺へは、三島から普通列車で550円です[[s:izuhakone_fares]]。普通車用のパスでグリーン車に座ると、グリーン料金と特急料金も要ります[[s:jrp_conditions]]。普通車がまったくないサフィール踊り子では、ここがいちばん効いてきます[[s:izukyu_express]]。</p>
<p>7日間の普通車用は、2026年11月時点で、オンラインなら大人50,000円、海外の代理店なら53,000円です[[s:jrp_price]]。使えるのはおもに「Temporary Visitor」のスタンプで入国した人で、ほかに使える人の条件はパスの公式サイトに書いてあります[[s:jrp_eligibility]]。東京〜下田が片道約6,660円なので、パスの元が取れるのは、日本をあちこち回る長い旅の途中に伊豆を入れるときだけだと私たちは思います。</p>

<h2>伊豆半島は、東京から日帰りできるか</h2>
<p>北のほうはできますが、南はあまり向きません。直通の電車でも下田まで2時間半ほどかかるので[[s:jre_tt_tokyo]]、往復すると、浜で過ごす数時間のために5時間ほど電車に乗ることになります。熱海と伊東は話が別です。熱海は新幹線で45分ほど、伊東は直通で2時間かからないので、どちらも日帰りで十分楽しめると私たちは思います。南の海岸と内陸の温泉町は、何泊かして、日々のペースをゆるめたほうがずっと楽しめるというのが私たちの実感です。</p>

<h2>伊豆のどの町が合うか</h2>
<p>決め手は、どこまで行きたいかと、どれくらいいられるかです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>町</th><th>東京から</th><th>どんな町か</th><th>日帰りか、泊まりか</th></tr></thead>
<tbody>
<tr><td><strong>熱海と伊東</strong></td><td>熱海まで新幹線で43〜45分、伊東まで直通で約1時間40分</td><td>東海岸の、東京にいちばん近い2つの町です。</td><td>日帰りでも楽しめる</td></tr>
<tr><td><strong>修善寺</strong></td><td>三島まで50〜53分、そこから約35分。または直通で約2時間</td><td>伊豆でいちばん古いと言われる、内陸の温泉町です。「独鈷の湯」は見るだけで入れませんが、近くに「河原湯」と「杉の湯」の2つの足湯があります[[s:izu_tokko]]。慌ただしく立ち寄るより、1〜2泊して静かに過ごすのが合う町です。</td><td>泊まるのがおすすめ</td></tr>
<tr><td><strong>下田</strong></td><td>直通で2時間29分〜2時間44分</td><td>半島の南端の港町で、2026年は正式な海水浴場が9つありました[[s:shimoda_beach2026_city]]。静岡県は、下田を[[l:ja-kinmedai|金目鯛]]の水揚げ日本一の港と紹介しています[[s:pref]]。1週間過ごすのにいちばん合う町だと、私たちは思います。過ごし方は[[l:ja-shimoda-guide|下田のガイド]]にまとめました。</td><td>泊まるのがおすすめ</td></tr>
</tbody></table></div>

<h2>南伊豆は、車なしで回れるか</h2>
<p>町と近くの浜なら、回れます。白浜海岸へは、伊豆急下田駅から板戸一色行きのバスで約15分です[[s:jnto]]。東海バスが、見たい所の多くを回れる2日間のフリーきっぷを出していて、買った日と次の日に使えます[[s:tokaibus_freepass]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>きっぷ</th><th>大人の値段</th><th>行ける所</th></tr></thead>
<tbody>
<tr><td><strong>下田2日券</strong></td><td>1,350円</td><td>下田の町、龍宮窟、爪木崎、白浜[[s:tokaibus_freepass]]</td></tr>
<tr><td><strong>石廊崎・下田2日券</strong></td><td>2,850円</td><td>上の範囲に加えて、石廊崎、弓ヶ浜、下賀茂、河津、稲取[[s:tokaibus_freepass]]</td></tr>
</tbody></table></div>
<p>どちらのきっぷも、下田駅前の東海バスの案内所で買えます。毎日8:45〜17:00に開いていて、12:30〜13:30は昼休みです[[s:tokaibus_freepass]]。外れの浜へのバスは本数が多くないので、出かける前に帰りの時刻を調べておくと安心です。1日にいくつもの浜を回りたいなら、電動自転車かレンタカーがあると、ぐっと動きやすくなります。</p>

<h2>伊豆半島はいつ行くのがいいか</h2>
<p>下田で泳ぐなら、2026年の期間は7月中旬から8月下旬でした。静かに過ごしたいなら、私たちはその前後の月を選びます。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>時期</th><th>どんな感じか</th></tr></thead>
<tbody>
<tr><td>下田の海水浴の期間（2026年は7月18日から、浜によって8月23〜31日まで）</td><td>2026年は、下田の9つの海水浴場がすべて7月18日に開き、多くは8時〜16時でした。白浜大浜と九十浜は8月31日まで、白浜中央は8月30日まで開いていましたが、ほかの6つは8月23日に閉じました[[s:shimoda_beach2026_city]]。期間外と時間外は、監視員がいません[[s:shimoda_ohama]]。</td></tr>
<tr><td>それ以外</td><td>町はぐっと静かになると私たちは感じていて、温泉や長い散歩にはいちばん過ごしやすい時期です。</td></tr>
</tbody></table></div>
<p class="fine">海水浴場の期間は、市が毎年決めます。8月の終わりに行くなら、どの浜がまだ開いているかを見ておくと安心です。</p>

<h2>伊豆では、なぜ1泊より1週間なのか</h2>
<p>1週間いると、旅がふだんの暮らしに変わり、南伊豆のゆっくりした時間の流れがしっくりきはじめます。ホテルの部屋は1〜2泊と決まった夕食の時間が前提です。キッチンと洗濯機のある部屋なら、午前は仕事、午後は浜か温泉、出かける気分でない夜は部屋で夕食、という過ごし方ができます。</p>
[[img:node-shimoda|ソファとローテーブル、障子のあるリビング|伊豆急下田駅から歩いて8分の「NODE Shimoda」のリビング。]]
<p>下田で試してみたいなら、旧町内にある私たちのアパートの一室「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」は、そんな1週間に向くように整えています。約40㎡の2階の部屋で、ワークデスク、洗濯機とガス乾燥機、調理器具のそろったキッチンがあります[[s:node_room]]。伊豆急下田駅から平坦な道を歩いて8分で、コンビニまで2分、スーパーまで3分です[[s:node_access]]。泊まる方の多くは海外からで、リモートで仕事をする人もサーフィンに来る人もいて、夏は長く泊まる人が増えます。</p>
<p>伊豆で1週間過ごして、もっと長く住むことや、自分の家を持つことが気になり始めたら、[[l:ja-akiya-try-first|家を買う前に1か月その町に住む]]ことをすすめる理由も読んでみてください。</p>
""",
  "faq": [
    ("東京から下田まで、何時間かかりますか",
     "直通の特急「踊り子」で2時間半ほどです[[s:jre_tt_tokyo]]。2026年11月の時刻表では毎日5本で、東京を9時から13時まで毎時ちょうどに出ます[[s:jre_tt_tokyo]]。"),
    ("東京から下田までの電車代はいくらですか",
     "踊り子の指定席で片道約6,660円です。運賃4,280円に、乗る前に買った場合の特急料金2,380円を足した額です[[s:izukyu_fares,izukyu_express]]。2026年11月時点の値段です。"),
    ("伊豆へ行くのに、ジャパン・レール・パスは使えますか",
     "伊東と三島までの JR で使えます。伊東〜伊豆急下田と三島〜修善寺は、踊り子に乗ったままでも運賃と料金を別に払います[[s:jrp_route]]。7日間の普通車用は、オンラインで50,000円です（2026年11月時点）[[s:jrp_price]]。"),
    ("修善寺へは、どう行くのがいいですか",
     "多くの人には、新幹線で三島へ出るのがいちばん楽だと私たちは思います。こだまで50〜53分です[[s:jre_tt_tokyo]]。三島からは伊豆箱根鉄道で、修善寺まで約35分、550円です[[s:izuhakone_tt,izuhakone_fares]]。乗り換えたくなければ、直通の「踊り子」も毎日2本（9:00・12:00発）あり、約2時間です[[s:jre_tt_tokyo]]。"),
    ("東京から下田へのバスはありますか",
     "東海バスは走らせていません。東海バスの高速バスで行けるのは三島までです。新宿からの「三島エクスプレス」は2,300円からです[[s:tokaibus_highway]]。下田へは、電車がいちばん簡単です。"),
    ("伊豆半島で車は必要ですか",
     "下田の町と近くの浜なら要りません。白浜へは駅からバスで約15分で[[s:jnto]]、東海バスの「下田2日券」は1,350円です[[s:tokaibus_freepass]]。車があると助かるのは、浜から浜へ動きたいときくらいです。"),
  ],
 },
},
# ============================================================ デジタルノマド
{
 "id": "digital-nomad", "slug": "japan-digital-nomad-visa", "topic": "live", "place": None, "also": [],
 "photo": ("laptop-plants-desk", "A laptop open on a wooden desk among potted plants, with a notebook and pen", ""),
 "published": "2026-11-16", "updated": "2026-11-16",
 "kicker": "Live part-time",
 "h1": "Japan’s digital nomad visa, and where to base yourself",
 "seo_title": "Japan Digital Nomad Visa: Who Qualifies and Where to Live",
 "description": "Japan’s digital nomad visa gives remote workers earning ¥10 million a year up to six months, with no extension or residence card, so where you live matters.",
 "dek": "Japan’s digital nomad status gives eligible remote workers up to six months. You’ll need a ¥10 million income, and there’s no residence card, which shapes where you can live.",
 "card": "Six months, no extension, ¥10 million a year in income and ¥10 million of medical cover. With no residence card, the real question is where you’ll live and work for those six months, and Tokyo isn’t the only sensible answer.",
 "keywords": [("japan digital nomad visa", "880", "2"), ("digital nomad visa japan", "720", "—")],
 "intent": "Know（条件・期間・家族・申請）→ Do（6か月をどこで暮らすか）",
 "points": [
   "You get up to six months with no extension, and you can apply again after six months away.",
   "You need ¥10 million a year in income, ¥10 million of medical cover and a passport from a listed country.",
   "There’s no residence card, so we think a furnished monthly place beats an ordinary lease.",
 ],
 "body": """
<p>If you’ve read a few blogs about this visa, you’ve probably seen them disagree on everything: renewals, family, residence cards. The good news is that the official rules are short and fit on one page [[s:isa_nomad_en]]. Once you’ve got them straight, the more interesting question is where you’ll spend six months without a residence card.</p>

<h2>What is Japan’s digital nomad visa?</h2>
<p>It lets you stay up to six months while you work online for someone outside Japan. Its official name is Designated Activities (Digital Nomad), and there’s a family version called Designated Activities (Spouse or Child of Digital Nomad) [[s:jnto_nomad]].</p>
<p>Two kinds of online work count. One is a job with a foreign employer, doing its overseas work remotely from Japan. The other is providing paid services, or selling goods, to people outside Japan [[s:isa_nomad_en,egov_immig_rules]]. So it isn’t just for employees: freelancers with clients abroad qualify too.</p>
<p>What it isn’t is a way into a job in Japan. On this status, you can’t be employed by a Japanese company or public body [[s:isa_nomad_en]]. If a Japanese employer is what you’re after, you’re looking at a different status.</p>

<h2>Who qualifies?</h2>
<p>You need three things: a passport from a listed country, a high income and private medical insurance. Here’s how they look as of November 2026 [[s:isa_nomad_en]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Condition</th><th>What it means</th></tr></thead>
<tbody>
<tr><td>Nationality</td><td>A passport from a country or region on the agency’s list. The list is built from places that have both a visa exemption and a tax treaty with Japan [[s:isa_nomad_en,isa_nomad_list]].</td></tr>
<tr><td>Income</td><td>¥10 million or more a year, counted as the applicant’s own income [[s:isa_nomad_en,jnto_nomad]].</td></tr>
<tr><td>Insurance</td><td>Private insurance covering death, injury and illness during your stay, with at least ¥10 million of cover for medical treatment [[s:isa_nomad_en]].</td></tr>
<tr><td>Your work</td><td>Online work from Japan for a foreign organisation that employs you, or paid work for clients and customers outside Japan. Work under an employment contract with a Japanese organisation isn’t allowed [[s:isa_nomad_en,egov_immig_rules]].</td></tr>
</tbody></table></div>
<p>The list is a PDF, and it’s the one place to check your own passport [[s:isa_nomad_list]]. Country counts on other sites go out of date, so we’d go by the current PDF. The income test is about you as the applicant, so it’s safer not to count on adding a partner’s earnings.</p>

<h2>How long can you stay, and can you renew it?</h2>
<p>Six months at most, and it can’t be extended [[s:isa_nomad_en,jnto_nomad]]. You can come back on the same status once six months have passed since you left Japan [[s:isa_nomad_en]]. In practice, that means half the year here and half somewhere else. If you’re weighing it against other ways to stay, our guide to [[l:how-long-stay|how long you can stay in Japan]] compares them.</p>
<p>You’ll still see sites promising one extension. The official page says there isn’t one, so that’s the version to plan around. Here’s how it compares with an ordinary visa-free visit.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>Short-term visitor (visa-exempt)</th><th>Digital nomad</th></tr></thead>
<tbody>
<tr><td>How long</td><td>Usually up to 90 days, though some nationalities get 15, 30 or 180 days [[s:jnto_visa]]</td><td>Up to six months, no extension [[s:isa_nomad_en]]</td></tr>
<tr><td>Work</td><td>No paid work [[s:jnto_visa]]</td><td>Online work for a foreign employer or paid work for clients abroad, but not for a Japanese employer [[s:isa_nomad_en]]</td></tr>
<tr><td>Residence card</td><td>No [[s:egov_immig_act]]</td><td>No [[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>

<h2>Can your partner and children come too?</h2>
<p>Yes, if they’re your spouse or a child you support. They come on the family version of the status, which covers their everyday life as your dependants [[s:isa_nomad_en,jnto_nomad]]. Like you, they won’t get a residence card [[s:egov_immig_rules]].</p>
<p>Their conditions are a little different from yours. Family members need a passport from a visa-exempt country or region, and the tax treaty test applies only to you [[s:isa_nomad_en]]. Each of them also needs their own policy on the same terms as yours, covering death, injury and illness, with at least ¥10 million for treatment [[s:isa_nomad_en]]. If you and your partner aren’t married, it’s worth asking the agency before you plan around it, because the status is written for a spouse or a child.</p>

<h2>How do you apply?</h2>
<p>The details are split across two official pages, which can feel a little scattered at first. The Ministry of Foreign Affairs issues the visa, and JNTO points you to its page for the documents [[s:jnto_nomad]]. If it’s your first entry on this status, the Immigration Services Agency explains how to apply for a pre-approval document (officially a Certificate of Eligibility) [[s:isa_nomad_en]].</p>
<ol>
<li>Find your passport’s country or region on the agency’s list [[s:isa_nomad_list]].</li>
<li>Gather proof of your income and an insurance policy that meets the conditions [[s:isa_nomad_en]].</li>
<li>Read the Ministry of Foreign Affairs page that JNTO links to for the current visa documents [[s:jnto_nomad]].</li>
<li>Read the agency’s guidance on the pre-approval document (Certificate of Eligibility) for a first entry [[s:isa_nomad_en]].</li>
<li>Plan your exit date, since the stay ends at six months [[s:isa_nomad_en]].</li>
</ol>
<p>It makes sense to sort out the status before you fly, rather than arrive as a tourist and try to switch. Switching inside Japan is harder than many people hope: a short-term visitor can only change status here when there are “unavoidable special circumstances” [[s:egov_immig_act]]. For anything the two pages don’t answer, ask the ministry or the agency.</p>

<h2>What doesn’t the visa give you?</h2>
<p>A residence card, and more follows from that than you might expect. Japan’s immigration law doesn’t treat digital nomads and their families as mid- to long-term residents, so no card is issued [[s:egov_immig_act,egov_immig_rules]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>With a residence card</th><th>On the digital nomad status</th></tr></thead>
<tbody>
<tr><td>Resident register (<em>juminhyo</em>)</td><td>Foreign residents with a card are registered where they live [[s:soumu_juki]]</td><td>You won’t be on it</td></tr>
<tr><td>National Health Insurance</td><td>Open to registered foreign residents [[s:egov_nhi_rules]]</td><td>You can’t join it [[s:egov_nhi_rules]]. Separately, the status requires private insurance [[s:isa_nomad_en]]</td></tr>
<tr><td>An ordinary lease</td><td>The government’s guideline for landlords gives the card as one example of ID [[s:mlit_foreign_rental]]</td><td>Harder, in our view. A furnished monthly place is usually simpler</td></tr>
</tbody></table></div>
<p>Renting is where you’ll feel it most. The government’s guideline for landlords gives a passport and a residence card as examples of ID, and leaves which ID to ask for up to the landlord and tenant [[s:mlit_foreign_rental]]. Landlords are also told to ask whether you have a Japanese bank account and a phone that works here [[s:mlit_foreign_rental]]. Without a card or a local account, we think a furnished place rented by the month is the easier route. Our guide to [[l:monthly-rental|renting a place by the month in Japan]] covers how to find one.</p>
<p>Tax is the other thing people get wrong, and “six months means no tax” is too simple. For Japanese income tax, you’re a resident if you have a domicile here, or have lived here continuously for a year or more [[s:nta_2875]]. As a non-resident, you’re taxed only on Japan-source income, and that includes pay for work you do while you’re here [[s:nta_nonresident]]. Tax treaties can change that [[s:nta_2875]], so a tax adviser who knows your home country’s treaty with Japan is the person to ask.</p>
<p>All of this reflects the rules as of November 2026. For your own case, it’s worth checking with the Ministry of Foreign Affairs, the Immigration Services Agency or an administrative scrivener (<em>gyoseishoshi</em>) who handles visas.</p>

<h2>Where should you base yourself for six months?</h2>
<p>Tokyo isn’t the only sensible answer, and for six months we don’t think it’s always the best one. In our view, four things matter most:</p>
<ul>
<li>an internet connection you can trust all working day</li>
<li>trains to Tokyo and an airport</li>
<li>a furnished place you can rent by the month</li>
<li>a clinic you can use</li>
</ul>
<p>Tokyo wins on some of these, but not all. Here’s how we see the trade-offs.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>Tokyo</th><th>A regional city</th><th>A small town 2–3 hours from Tokyo</th></tr></thead>
<tbody>
<tr><td>Furnished monthly places</td><td>The most choice</td><td>Some choice</td><td>Few, so you book further ahead</td></tr>
<tr><td>Getting to an airport</td><td>Easy</td><td>Usually easy</td><td>A longer trip, so it takes planning</td></tr>
<tr><td>Daily life in English</td><td>Easiest</td><td>Patchier</td><td>Patchy, and a translation app helps</td></tr>
<tr><td>What you give up</td><td>Space and quiet</td><td>A little of everything</td><td>Choice and convenience, for space, quiet and a slower week</td></tr>
</tbody></table></div>
<p>Fibre is less of a worry than people expect, even in a small town. Government estimates for the end of March 2025 put it within reach of 96.3% of households in Tokyo [[s:soumu_ftth_2025]]. Shimoda isn’t far behind, at about 93.8% [[s:soumu_ftth_2025]]. Those figures are about whether a line reaches the building, though, not its speed, and getting one installed can take time. When we opened our place in Shimoda, broadband took more than two months in the busy season, so we got by on a plug-in home router. A place that already has a working line saves you that wait.</p>
<p>It’s much easier to find your nearest clinic on day one than on the day you need it. JNTO has an English search that filters by prefecture, language and department, and it suggests contacting a clinic before you go [[s:jnto_medical]].</p>
<p>Shimoda, on the [[l:izu|Izu Peninsula]], is one example of a small town in reach, close enough, we find, for a day in Tokyo when you need one. Direct trains from Tokyo Station take about two and a half hours (2 hours 29–44 minutes on the November 2026 timetable) [[s:jre_tt_tokyo]]. Our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] has the routes.</p>
<p>Our own place there, NODE Shimoda, is an apartment of about 40 m², eight minutes’ walk from Izukyu-Shimoda Station [[s:node_site,node_room]]. It has a work desk and Wi-Fi, plus a kitchen, washing machine and gas dryer for everyday life [[s:node_site,node_room]]. We set it up with long-staying remote workers in mind, so if you’re planning something longer, just ask us. If a season goes well and you start looking at houses, read our piece on [[l:akiya-try-first|living in a town before you buy an akiya]].</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal, immigration or tax advice.</p>',
 "faq": [
   ("How long is Japan’s digital nomad visa?",
    "Up to six months, and as of November 2026 the stay can’t be extended [[s:isa_nomad_en]]."),
   ("Can I extend Japan’s digital nomad visa?",
    "No. You can come back on the same status once six months have passed since you left Japan [[s:isa_nomad_en]], so the pattern is six months in, six months away."),
   ("Do I get a residence card on the digital nomad visa?",
    "No. Digital nomads and their families aren’t treated as mid- to long-term residents, so no card is issued [[s:egov_immig_act,egov_immig_rules]]. That also means you won’t be on the resident register or in National Health Insurance [[s:soumu_juki,egov_nhi_rules]]."),
   ("Can I bring my family on Japan’s digital nomad visa?",
    "A spouse or child you support can come on the family version of the status [[s:jnto_nomad,isa_nomad_en]]. They need a passport from a visa-exempt country or region and the same insurance as you [[s:isa_nomad_en]]. If you aren’t married, ask the agency first."),
   ("Can I work for a Japanese company on it?",
    "No. On this status, you can’t be employed by a Japanese company or public body [[s:isa_nomad_en]]. It’s meant for online work for a foreign organisation that employs you, or paid work for clients outside Japan."),
 ],
 "sources": ["isa_nomad_en", "isa_nomad_list", "jnto_nomad", "jnto_visa", "egov_immig_act", "egov_immig_rules", "soumu_juki", "egov_nhi_rules",
             "mlit_foreign_rental", "nta_2875", "nta_nonresident", "soumu_ftth_2025", "jnto_medical", "jre_tt_tokyo", "node_site", "node_room"],
 "related": ["izu-from-tokyo", "akiya-try-first"],
 "ja": {
  "h1": "日本のデジタルノマドビザと、どこを拠点にするか",
  "dek": "日本のデジタルノマドの在留資格なら、条件を満たすリモートワーカーは最長6か月滞在できます。年収1,000万円以上が必要で、在留カードが出ないので、どこに住めるかも変わってきます。",
  "review": [
   "2026-11-21 ネイティブ感の仕上げ（playbook 3-1 の6 の後半）: 在留資格認定証明書を「事前の証明書（正式名 Certificate of Eligibility）」と普通の言葉で先に言う形に（必要かどうかは書いていません）。事実・数値・出典は変えていません。",
   "2026-11-20 見せ方のリライト: 人の方針（ガイドブックのような固い文章は読みづらい）に合わせ、英語と日本語の語り口を「詳しい友人の話」に寄せました。①「入管庁のページには〜とある」のような出典の前置きを本文・FAQ から減らし、言い切りに（出典の番号はそのまま）。②拠点選びの5つの条件を短いリストにし、光回線の数字・下田の電車の時間・NODE Shimoda の設備を、1文に詰めずに分けました。③段落の頭に答え（出発前に手続きを済ませる、診療所は着いた日に調べる、など）を置きました。④dek を言い換え、updated を 2026-11-20 に。事実・数値・出典・リンク・体験の中身は変えていません。見解として「6か月なら東京がいつもいちばんとは思わない」「下田は用があれば東京に日帰りできる距離」を足しています（電車の所要時間からの見方で、新しい事実ではありません）。",
   "【2026-11-16 品質保証部の採点（89点・ゲート違反2）を受けた書き直し】変えた点: ①【事実の変更】申請: 「大使館・総領事館で申請する」（本文と手順の2か所）をやめ、「ビザは外務省が出し、必要な書類は外務省のページにある（JNTO）」と「入管庁のページに、この在留資格で新しく入国する人の在留資格認定証明書の交付申請の案内がある」だけで書きました。手数料・期間・どちらを先にするかは書いていません。手順の番号つきリストもこれに合わせました。②「私たちの経験では、6か月暮らしたい人は小さな町のほうがうまくいく」を消しました（確認済みの体験にないため）。比較表の前の文を「私たちの見方をまとめると」にして、表が見解だと分かるようにしています。③国民健康保険: 「入れない。だから民間の保険が条件」の理由づけをやめ、「入れない」と「それとは別に、民間の保険が条件」を並べました。④【言い切りに変更】仕事の範囲: 入管庁のページの原文（外国の組織との雇用契約で外国の業務をする／外国にいる人に有償で役務・物品を提供する、日本の公私の機関との雇用契約などにもとづいて働くことはできない）を出典に、「フリーランスも当てはまる」「日本の会社では働けない」を本文・表・FAQ で言い切りました。⑤【事実の追加】家族: 本人に扶養される配偶者・子として日常の活動をする資格であること、家族の国籍の条件は査証免除の国・地域（租税条約の条件は本人だけ）、家族の保険の条件は本人と同じ、を足しました。家族が働けるかは書いていません。⑥【事実の追加】保険の条件に「滞在中の死亡・けが・病気を補償」を足しました。⑦“we’d”（私たちなら）を減らし、description の末尾を文にしました。⑧光回線の段落を4文にし（静岡県の96.7%は外しました）、最後の節の表のあとの段落を5つから3つにしました（空き家の記事への案内は下田の段落にまとめました）。",
   "【2026-11-16 新規（執筆部）】書いた点: 条件・期間・延長・再申請・在留カード・家族は、編集長が 2026-11-16 に出入国在留管理庁のページで確かめた内容と JNTO の英語のページだけで書き、すべて「2026年11月時点」と書いています。在留カードが出ないこと、日本の中での在留資格の変更（やむを得ない特別の事情があるときだけ）は e-Gov の条文で裏付けました。在留カードがないことの影響（住民登録・国民健康保険・普通の賃貸）は総務省・国保法施行規則・国交省のガイドラインで書き、賃貸は「借りられない」とは書かず見解にしています。税は国税庁の居住者・非居住者の定義と国内源泉所得までで、自分の場合は税理士に、で止めました。拠点選びは、光回線の世帯カバー率（総務省、2025年3月末の推計）、JNTO の医療機関の検索、東京駅から下田の直通の所要時間（JR東日本の時刻表、2026年11月）、確認済みの体験（開業時に Wi-Fi の工事に2か月以上かかり、ホームルーターでしのいだ）で書きました。NODE Shimoda に触れるのは最後の節の1回で、公式サイトの事実だけです（30泊以上・6か月の受け入れ、料金、回線の実測値は書いていません）。",
   "【写真】編集長が入れた laptop-plants-desk（観葉植物のある木の机に開いたノートPC）をそのまま使っています。",
   "【書かなかったこと（確かめられなかったため）】制度が始まった日、対象の国・地域の数と、米英などが入っているか（一覧の PDF で確かめるよう案内しています）、家族が働けるか、手数料・審査の期間・ビザと在留資格認定証明書のどちらを先にするか、必要書類の細目、発給件数、在留カードなしで携帯・銀行口座を作れるか。月単位の部屋の記事（monthly-rental）はまだないので、内部リンクは伊豆・伊豆への行き方・空き家の記事に送っています。",
  ],
  "points": [
    "滞在は最長6か月で延長はできず、日本を出て6か月たてば、また申請できます。",
    "年収1,000万円以上、治療費1,000万円以上の医療保険、対象の国・地域のパスポートが要ります。",
    "在留カードが出ないので、普通の賃貸より家具付きの月単位の部屋のほうがいい、と私たちは考えています。",
  ],
  "body": """
<p>このビザについてブログをいくつか読むと、更新、家族、在留カードと、言うことがほとんどばらばらなのに気づくと思います。でも安心してください。公式の決まりは短く、1つのページに収まっています[[s:isa_nomad_en]]。それが分かったら、考えがいがあるのは、在留カードのない6か月をどこで過ごすかです。</p>

<h2>日本のデジタルノマドビザとは</h2>
<p>日本の外の誰かのためにオンラインで働きながら、最長6か月いられる在留資格です。正式な名前は「特定活動（デジタルノマド）」で、家族のための「特定活動（デジタルノマドの配偶者又は子）」もあります[[s:jnto_nomad]]。</p>
<p>対象になるオンラインの仕事は2種類です。1つは、外国の組織との雇用契約にもとづいて、その組織の外国での業務をすること。もう1つは、日本の外にいる人に、有償でサービスを提供したり、物を売ったりすることです[[s:isa_nomad_en,egov_immig_rules]]。なので、会社員だけでなく、海外に取引先のあるフリーランスの人も当てはまります。</p>
<p>一方で、日本で仕事に就くための資格ではありません。この在留資格では、日本の組織（公的なものも民間も）との雇用契約にもとづいて働くことはできません[[s:isa_nomad_en]]。日本の雇用主のもとで働きたいなら、別の在留資格を考えることになります。</p>

<h2>誰が対象になるのか</h2>
<p>必要なのは、対象の国・地域のパスポート、高い収入、民間の医療保険の3つです。2026年11月時点では、次のとおりです[[s:isa_nomad_en]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>条件</th><th>中身</th></tr></thead>
<tbody>
<tr><td>国籍</td><td>入管庁の一覧にある国・地域のパスポート。一覧は、日本との間で査証免除と租税条約の両方がある国・地域から作られています[[s:isa_nomad_en,isa_nomad_list]]。</td></tr>
<tr><td>収入</td><td>申請する本人の年収が1,000万円以上[[s:isa_nomad_en,jnto_nomad]]。</td></tr>
<tr><td>保険</td><td>滞在中の死亡・けが・病気を補償し、治療費1,000万円以上をカバーする民間の保険[[s:isa_nomad_en]]。</td></tr>
<tr><td>仕事</td><td>日本からのオンラインの仕事で、雇われている外国の組織のための仕事か、日本の外の取引先・お客さんへの有償の仕事。日本の組織との雇用契約にもとづいて働くことはできない[[s:isa_nomad_en,egov_immig_rules]]。</td></tr>
</tbody></table></div>
<p>一覧は PDF で、自分のパスポートが対象かを確かめられるのはそこだけです[[s:isa_nomad_list]]。ほかのサイトに載っている国の数は古くなるので、私たちならいまの版だけを信じます。収入の条件は申請するあなた自身のものなので、パートナーの収入を足して届かせることはあてにしないほうが安全です。</p>

<h2>どれくらいいられて、更新はできるのか</h2>
<p>最長6か月で、延長はできません[[s:isa_nomad_en,jnto_nomad]]。日本を出てから6か月たてば、同じ在留資格でまた来られます[[s:isa_nomad_en]]。実際には、1年の半分を日本で、残りの半分をほかの場所で過ごす形になります。ほかの滞在のしかたと比べたいなら、[[l:ja-how-long-stay|日本に何日いられるかのガイド]]も読んでみてください。</p>
<p>いまでも「1回だけ延長できる」と書いているサイトを見かけます。公式のページには延長はないとあるので、計画はそちらに合わせるのがいいと思います。ふつうのビザなしの滞在と比べると、次のとおりです。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>短期滞在（査証免除）</th><th>デジタルノマド</th></tr></thead>
<tbody>
<tr><td>期間</td><td>たいてい最長90日。国籍によっては15日・30日・180日[[s:jnto_visa]]</td><td>最長6か月、延長なし[[s:isa_nomad_en]]</td></tr>
<tr><td>仕事</td><td>報酬を受ける仕事はできない[[s:jnto_visa]]</td><td>外国の雇用主や海外の取引先のためのオンラインの仕事。日本の雇用主のためには働けない[[s:isa_nomad_en]]</td></tr>
<tr><td>在留カード</td><td>出ない[[s:egov_immig_act]]</td><td>出ない[[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>

<h2>パートナーや子どもも一緒に来られるのか</h2>
<p>配偶者か、あなたが扶養している子どもなら来られます。家族のための在留資格で来ることになり、対象は扶養を受ける家族としての日常の活動です[[s:isa_nomad_en,jnto_nomad]]。本人と同じく、家族にも在留カードは出ません[[s:egov_immig_rules]]。</p>
<p>家族の条件は、本人と少し違います。家族は査証免除の国・地域のパスポートが要りますが、租税条約の条件は本人だけのものです[[s:isa_nomad_en]]。保険も一人ひとりに、本人と同じ条件のもの（滞在中の死亡・けが・病気を補償し、治療費1,000万円以上）が要ります[[s:isa_nomad_en]]。パートナーと結婚していないなら、計画を立てる前に入管庁に聞いてみるといいと思います。この在留資格は配偶者か子どものためのものだからです。</p>

<h2>どうやって申請するのか</h2>
<p>見るページが2つに分かれていて、最初は少し分かりにくいかもしれません。ビザは外務省が出し、必要な書類は外務省のページにあると JNTO が案内しています[[s:jnto_nomad]]。この在留資格で初めて入国するなら、在留資格認定証明書の申請のしかたを入管庁が案内しています[[s:isa_nomad_en]]。</p>
<ol>
<li>自分のパスポートの国・地域が、入管庁の一覧にあるかを確かめる[[s:isa_nomad_list]]。</li>
<li>収入の証明と、条件を満たす保険の証書をそろえる[[s:isa_nomad_en]]。</li>
<li>JNTO から案内されている外務省のページで、いまのビザの必要書類を見る[[s:jnto_nomad]]。</li>
<li>入管庁のページで、この在留資格で初めて入国する人の在留資格認定証明書の案内を読む[[s:isa_nomad_en]]。</li>
<li>滞在は6か月で終わるので、出国の日を決めておく[[s:isa_nomad_en]]。</li>
</ol>
<p>観光で入ってから切り替えようとするより、出発の前に在留資格の手続きを済ませておくのがいいと思います。日本に入ってから切り替えるのは、思っているより難しいからです。短期滞在の人が日本の中で在留資格を変えられるのは「やむを得ない特別の事情」があるときだけです[[s:egov_immig_act]]。2つのページで分からないことは、外務省か入管庁に聞いてみてください。</p>

<h2>このビザで手に入らないものは何か</h2>
<p>在留カードです。そして、そこから思った以上に多くのことが決まります。入管法では、デジタルノマドとその家族は中長期在留者に当たらないので、カードは出ません[[s:egov_immig_act,egov_immig_rules]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>在留カードがある人</th><th>デジタルノマドの在留資格</th></tr></thead>
<tbody>
<tr><td>住民登録（住民票）</td><td>カードのある外国人住民は、住んでいる所で登録される[[s:soumu_juki]]</td><td>登録されない</td></tr>
<tr><td>国民健康保険</td><td>登録された外国人住民が入れる[[s:egov_nhi_rules]]</td><td>入れない[[s:egov_nhi_rules]]。それとは別に、この在留資格では民間の保険が条件になっている[[s:isa_nomad_en]]</td></tr>
<tr><td>普通の賃貸</td><td>国の大家さん向けのガイドラインが、本人確認の書類の例の1つにカードを挙げている[[s:mlit_foreign_rental]]</td><td>私たちの見方では難しい。家具付きの月単位の部屋のほうがたいてい簡単</td></tr>
</tbody></table></div>
<p>いちばん影響を感じるのは部屋を借りるときです。国の大家さん向けのガイドラインは、本人確認の書類の例にパスポートと在留カードを挙げ、何を求めるかは大家さんと借りる人に任せています[[s:mlit_foreign_rental]]。大家さんは、日本の銀行口座と日本で使える電話があるかも聞くように言われています[[s:mlit_foreign_rental]]。カードも日本の口座もないなら、家具付きで月単位に借りる部屋のほうが楽だと私たちは考えています。探し方は[[l:ja-monthly-rental|日本で部屋を月単位で借りる記事]]にまとめています。</p>
<p>税金も、よく誤解されるところです。「6か月なら税金はかからない」は単純すぎます。日本の所得税では、日本に住所があるか、1年以上続けて住んでいる人が居住者になります[[s:nta_2875]]。非居住者は日本の国内源泉所得にだけ課税され、日本でした仕事への報酬は国内源泉所得に当たります[[s:nta_nonresident]]。租税条約で変わることもあるので[[s:nta_2875]]、自分の国と日本の租税条約に詳しい税理士に聞くのがいちばんです。</p>
<p>ここに書いたのは、すべて2026年11月時点の決まりです。自分の場合については、外務省、出入国在留管理庁、またはビザを扱う行政書士に確かめてみてください。</p>

<h2>6か月、どこを拠点にするか</h2>
<p>答えは東京だけではありませんし、6か月なら東京がいつもいちばんだとも私たちは思っていません。大事なのは次の4つだと考えています。</p>
<ul>
<li>仕事の時間ずっと頼れる回線</li>
<li>東京と空港への電車</li>
<li>月単位で借りられる家具付きの部屋</li>
<li>通いやすい診療所</li>
</ul>
<p>東京が有利なのはこのうちいくつかで、全部ではありません。私たちの見方をまとめると、次のようになります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th></th><th>東京</th><th>地方の都市</th><th>東京から2〜3時間の小さな町</th></tr></thead>
<tbody>
<tr><td>家具付きの月単位の部屋</td><td>選択肢がいちばん多い</td><td>ある程度ある</td><td>少ないので、早めに予約する</td></tr>
<tr><td>空港への行き来</td><td>楽</td><td>たいてい楽</td><td>遠くなるので、計画が要る</td></tr>
<tr><td>英語での暮らし</td><td>いちばん楽</td><td>ところによる</td><td>ところによる。翻訳アプリが助けになる</td></tr>
<tr><td>あきらめるもの</td><td>広さと静けさ</td><td>どれも少しずつ</td><td>選択肢と便利さ。代わりに広さ、静けさ、ゆっくりした毎日</td></tr>
</tbody></table></div>
<p>光回線は、小さな町でも思われているほど心配いりません。国の2025年3月末の推計では、東京都で96.3%の世帯が光回線を引けます[[s:soumu_ftth_2025]]。下田市も約93.8%で、大きくは変わりません[[s:soumu_ftth_2025]]。ただ、これは建物まで回線が届くかどうかの数字で速さではなく、引くまでに時間がかかることもあります。私たちが下田で宿を開いたときは、繁忙期で回線の工事に2か月以上かかり、置くだけのホームルーターでしのぎました。もう回線が入っている部屋なら、その待ち時間がありません。</p>
<p>いちばん近い診療所は、必要になった日より、着いた日に調べておくほうがずっと楽です。JNTO には、都道府県・言語・診療科で探せる英語の検索があり、行く前に連絡して確かめるよう案内しています[[s:jnto_medical]]。</p>
<p>[[l:ja-izu|伊豆半島]]の下田は、東京から行ける小さな町の一例で、用があれば東京に日帰りもできる距離だと私たちは感じています。東京駅からの直通の電車で2時間半ほどです（2026年11月の時刻表で2時間29分〜44分）[[s:jre_tt_tokyo]]。行き方は[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>私たちの NODE Shimoda は、伊豆急下田駅から歩いて8分の、約40㎡のアパートの一室です[[s:node_site,node_room]]。ワークデスクと Wi-Fi に加えて、暮らしに要るキッチン、洗濯機とガス乾燥機もあります[[s:node_site,node_room]]。長く滞在するリモートワーカーを考えて作ったので、長めの滞在を考えているなら、気軽に聞いてください。ひと季節がうまくいって家を探しはじめたら、[[l:ja-akiya-try-first|空き家を買う前にその町で暮らしてみる話]]も読んでみてください。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律・在留手続き・税の助言ではありません。</p>',
  "faq": [
    ("日本のデジタルノマドビザは、どれくらいいられますか？",
     "最長6か月で、2026年11月時点では延長できません[[s:isa_nomad_en]]。"),
    ("日本のデジタルノマドビザは延長できますか？",
     "できません。日本を出てから6か月たてば、同じ在留資格でまた来られるので[[s:isa_nomad_en]]、6か月いて、6か月離れる形になります。"),
    ("デジタルノマドビザで在留カードはもらえますか？",
     "もらえません。デジタルノマドとその家族は中長期在留者に当たらないので、カードは出ません[[s:egov_immig_act,egov_immig_rules]]。そのため、住民登録もされず、国民健康保険にも入れません[[s:soumu_juki,egov_nhi_rules]]。"),
    ("デジタルノマドビザで家族を連れて来られますか？",
     "本人に扶養される配偶者と子どもは、家族のための在留資格で来られます[[s:jnto_nomad,isa_nomad_en]]。家族は査証免除の国・地域のパスポートと、本人と同じ条件の保険が要ります[[s:isa_nomad_en]]。結婚していない場合は、先に入管庁に聞いてください。"),
    ("このビザで日本の会社で働けますか？",
     "働けません。この在留資格では、日本の組織（公的なものも民間も）との雇用契約にもとづいて働くことはできません[[s:isa_nomad_en]]。対象は、雇われている外国の組織のためのオンラインの仕事か、日本の外の取引先への有償の仕事です。"),
  ],
 },
},
# ============================================================ 1か月の部屋
{
 "id": "monthly-rental", "slug": "monthly-rental-japan", "topic": "live", "place": None, "also": ["stay"],
 "photo": ("studio-apartment", "A small furnished studio with a compact kitchen, a dining table and a long wooden floor", ""),
 "published": "2026-11-16", "updated": "2026-11-16",
 "kicker": "Live part-time",
 "h1": "Monthly rentals in Japan: how to rent a place for a month",
 "seo_title": "Monthly Rental in Japan: How to Rent a Place for a Month",
 "description": "A month in Japan usually means a monthly apartment or a licensed holiday rental, not an ordinary lease. What’s included, and what to ask first.",
 "dek": "An ordinary Japanese lease usually isn’t an option for a visitor. For a month, you’re looking at a monthly apartment or a licensed holiday rental with monthly rates.",
 "card": "Ordinary leases in Japan run for years and need a guarantee, so a month means a monthly apartment or a licensed holiday rental. Compare the total cost, check the listing’s licence number, and ask about the things you’ll live with every day.",
 "keywords": [("monthly rental in japan", "—", "—"), ("monthly rental japan", "170", "16"), ("rent a house in japan", "1,300", "41"),
              ("long term stay japan / one month in japan", "50〜90", "0〜18")],
 "intent": "Do（やり方・何を選ぶか）",
 "points": [
   "Ordinary leases usually run for two years and need a rent guarantee, so they rarely suit a one-month stay.",
   "Monthly apartments and licensed holiday rentals with monthly rates are the realistic choices for a visitor.",
   "Registered booking sites show a legal rental’s licence or notification number, and you’ll be asked for your passport.",
 ],
 "body": """
<p>A month is too long for a hotel to feel like home, and far too short for a normal Japanese lease. Japan has a few legal ways to fill that gap, and the law treats each one differently. That difference decides who cleans, what you pay and what happens if a listing turns out to be illegal.</p>

<h2>Can a visitor rent a place in Japan for a month?</h2>
<p>Yes, but usually not with an ordinary lease. You’ll want a place that’s set up to be let by the month.</p>
<p>An ordinary Japanese lease usually runs for two years, and landlords normally want a guarantee for the rent, either from a rent-guarantee company or by a joint guarantor [[s:mlit_foreign_rental_qa]]. The government’s guideline for landlords tells them to check a foreign applicant’s status of residence first. It also notes that if your permission to stay ends before the lease does, the contract can end early [[s:mlit_foreign_rental_qa]].</p>
<p>Then there’s the money up front. Key money (<em>reikin</em>) of one to two months’ rent is common in the Kanto region and isn’t refunded, and a deposit of about the same is returned after deductions [[s:mlit_foreign_rental_qa]]. In our view, that rules out an ordinary lease for most people coming for a month. The good news is that Japan has places built for exactly this kind of stay.</p>

<h2>Monthly apartment, holiday rental or share house: which suits a month?</h2>
<p>For most visitors, it comes down to a monthly apartment or a licensed holiday rental. The difference is mostly legal, but it changes who cleans, what’s included and how you book.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Type</th><th>What it is in law</th><th>Shortest stay</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><strong>Monthly apartment</strong> (“monthly mansion”)</td><td>A short-term lease: a rental, not lodging [[s:jta_short_lease_2018]]</td><td>Usually a month [[s:jta_short_lease_2018]]</td><td>A furnished flat let by the month. You sign a rental contract, so read what the rent covers.</td></tr>
<tr><td><strong>Licensed holiday rental</strong> (<em>minpaku</em>)</td><td>A home notified to the authorities under the Private Lodging Business Act [[s:jta_minpaku_overview]]</td><td>Set by the host</td><td>It can host guests on no more than 180 nights a year, and local rules can cut that further [[s:jta_minpaku_act]].</td></tr>
<tr><td><strong>Guesthouse or holiday home</strong> with a lodging licence</td><td>Licensed under the Hotel Business Act, for example as simple lodging [[s:jta_minpaku_overview]]</td><td>Set by the host</td><td>There’s no yearly limit on operating days, so it can take guests all year [[s:jta_minpaku_overview]].</td></tr>
<tr><td><strong>Share house</strong></td><td>Usually a rental, on terms set by each operator</td><td>Set by the operator</td><td>Your own bedroom, with the kitchen and bathroom shared. Terms vary a lot, so it helps to get them in writing.</td></tr>
</tbody></table></div>
<p>Why does a monthly apartment usually ask for at least a month? It’s about where Japan draws the line. In principle, the tourism and health authorities treat a stay of under a month as lodging, not renting. So a short-term lease should normally require at least a month and say clearly that it’s a rental, though a local authority can use a different yardstick [[s:jta_short_lease_2018]]. Monthly apartments also shouldn’t sit next to short-stay holiday rentals on the same site, which is why you’ll often find them in different places [[s:jta_short_lease_2018]].</p>
<p>The two give you different things, too. With lodging, keeping the room clean is the operator’s job, and you’re a guest rather than someone who lives there. With a lease, the place is your home for the length of the contract [[s:jta_short_lease_2018]]. Whichever you choose, it’s worth asking who cleans, and how often.</p>
<p>You may also see the term fixed-term lease (<em>teiki shakuya</em>). It’s a type of Japanese lease, not another name for a monthly apartment, and what it means for you is that you can’t count on extending. It ends on the date in the contract and isn’t renewed, though you and the landlord can agree a new one. It has to be in writing, and the landlord must explain in a separate document that it won’t be renewed [[s:mlit_fixed_term]].</p>

<h2>What does a month cost, and what’s included?</h2>
<p>The rent is only part of the bill, so it’s the total you want to compare. Prices vary too much from town to town for one figure to help. What stays much the same everywhere is the list of extras, and here’s what we’d ask about each.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>What you pay for</th><th>Why it matters</th><th>What to ask</th></tr></thead>
<tbody>
<tr><td>Rent or nightly rate</td><td>The figure you see first, and the one that’s easiest to compare</td><td>Is there a weekly or monthly discount, and is it already in this price?</td></tr>
<tr><td>Cleaning</td><td>It can be a one-off fee, regular cleans during the stay, or nothing at all</td><td>Is cleaning included during the stay, and how often?</td></tr>
<tr><td>Electricity, gas and water</td><td>They can be included, capped or charged by what you use</td><td>Is there a cap, and what happens if you go over it?</td></tr>
<tr><td>Internet</td><td>A slow line is hard to live with for a month if you work</td><td>Is it fixed broadband or a mobile router?</td></tr>
<tr><td>Deposit</td><td>Money you’ll want back at the end</td><td>Is there one, and when and how is it returned?</td></tr>
<tr><td>Booking site fees</td><td>The price you first see may not be the final total</td><td>Does the total include the booking site’s service fee?</td></tr>
<tr><td>Leaving early</td><td>Plans change over a month</td><td>If you leave early, are any unused nights refunded?</td></tr>
</tbody></table></div>
<p>Monthly rates exist for a reason. From the host’s side, a longer stay means fewer cleans between guests. That’s why, when we opened our first place to stay, we added weekly and monthly discounts. If a listing doesn’t show one, there’s no harm in asking.</p>

<h2>How can you tell a holiday rental is legal?</h2>
<p>The quickest sign is a notification or licence number on the listing. Since June 2018, anyone offering paid stays in a home in Japan has needed a licence or a notification [[s:jta_minpaku_overview]]. That means one of three things: a Hotel Business Act licence, special-zone certification or a notification under the Private Lodging Business Act [[s:jta_minpaku_overview]].</p>
<p>Booking sites registered as minpaku agents have to show each listing’s notification number or similar licence details [[s:jta_listing_rules]]. The Japan Tourism Agency’s tip is to make sure you can see both that number and the property’s address on the site [[s:jta_minpaku_users]]. A place with a lodging licence shows a licence number rather than a notification number, so the format won’t always look the same. We know this from the host’s side: until our licence came through, we couldn’t take bookings on Airbnb.</p>
<p>On a month-long stay, the real worry is that an illegal listing can vanish while you’re booked in it. Registered sites report their listings to the agency every six months and must promptly remove illegal ones when asked [[s:jta_listing_page]]. When the law took effect in June 2018, booking sites had to cancel future reservations at unregistered properties or move guests to legal ones [[s:jta_cancel_2018]]. The agency’s advice is to book minpaku only through registered sites or travel agencies [[s:jta_minpaku_illegal]].</p>
<p>The 180-night limit on a minpaku is the host’s limit, not yours. It’s counted per property, in a year that starts at noon on 1 April [[s:jta_minpaku_act]], so it only means that kind of home can’t be let all year.</p>
<p>Why does the host want your passport? Because the law asks them to. Under the Private Lodging Business Act, foreign guests without an address in Japan give their nationality and passport number. The host then keeps a copy of the passport [[s:jta_minpaku_users]]. Places with a lodging licence work the same way: the guest register includes those details, and the health ministry asks operators to see the passport and keep a copy [[s:mhlw_passport]]. At three homes our team helps run, questions about the guest register were among the most common we got, so you’re not alone in wondering.</p>

<h2>What should you ask before booking a whole month?</h2>
<p>The things you’ll live with every day, not just what’s in the photos. These are the questions we’d want answered, in the order we’d ask them.</p>
<ol>
<li><strong>Internet.</strong> Is it fixed broadband, and where’s the router if it needs restarting? If you’ll be on video calls, a proper desk matters as much as the speed.</li>
<li><strong>Electricity.</strong> How much can you run at once? In our first flat, the old two-wire wiring couldn’t run the air conditioner, fridge and microwave together, so knowing where the breaker box is helps too.</li>
<li><strong>Heating and cooling.</strong> Is there an air conditioner in the room you’ll sleep in, and is the electricity for it included?</li>
<li><strong>Washing.</strong> Is there a washing machine, and a dryer? Our guests have praised both in their reviews, and a month of rainy-season laundry explains why.</li>
<li><strong>Rubbish.</strong> How does it work on a long stay? Each town has its own sorting rules and collection days. In Shimoda, for example, the city’s guide is in Japanese [[s:shimoda_gomi]]. At the three homes our team helps run, a small number of reviews from long stays mentioned smells from the bin area.</li>
<li><strong>Cleaning and bedding.</strong> Is there a clean or a change of sheets during the stay, or is it all on you?</li>
<li><strong>Stairs and bathroom.</strong> Which floor is it on, is there a lift, and is there a bath or only a shower? At one of the homes our team helps run, explaining the steep stairs before people booked went down well.</li>
<li><strong>Getting around.</strong> Is there parking, or a bus stop and a supermarket within walking distance?</li>
<li><strong>Leaving early.</strong> If your plans change, what happens to the nights you don’t use?</li>
</ol>
<p>To show what useful answers look like, here’s how we’d answer for our own flat, <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>. It’s a whole flat of about 40 m², up about 13 steps, with a shower but no bathtub [[s:node_room]]. There’s a work desk, fast Wi-Fi, and a free washing machine and gas dryer [[s:node_room]]. The electrical supply is small, so we ask guests to switch the air conditioner off for a moment while they use the microwave, vacuum cleaner or hairdryer [[s:node_room]]. Burnable rubbish goes in the bin, rinsed cans and bottles stay in the kitchen, and long-stay guests get in touch with us about the rest [[s:node_room]].</p>

<h2>Is it harder to rent for a month outside Tokyo?</h2>
<p>There’s less to choose from, but it’s very doable if you start early. We think you’ll find fewer monthly apartments in a small town, and more guesthouses and holiday homes that offer monthly rates.</p>
<p>Housing does get cheaper away from the capital. Rent per square metre in Shizuoka City is less than half what it is in Tokyo’s 23 wards [[s:estat_rent_2025]]. These figures come from ordinary leases, not monthly apartments [[s:stat_rent_note]], but they give you a sense of the gap.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Place</th><th>Average private rent per 3.3 m² a month (2025)</th></tr></thead>
<tbody>
<tr><td>Tokyo’s 23 wards</td><td>¥9,803 [[s:estat_rent_2025]]</td></tr>
<tr><td>Shizuoka City</td><td>¥4,621 [[s:estat_rent_2025]]</td></tr>
</tbody></table></div>
<p>Getting around matters more, too. Buses can be few, so a place within walking distance of a supermarket makes daily life much easier without a car. Seaside towns also fill up in summer. In Shimoda, where we host, summer brings people for the beaches and surfing, so a month in July or August needs booking well ahead.</p>
<p>If you want a small town that’s still easy to reach, the Izu Peninsula is one option. Direct trains run every day from Tokyo Station, and the ride to Shimoda takes between 2 hours 29 minutes and 2 hours 44 minutes [[s:jre_tt_tokyo]]. That’s from the November 2026 timetable, so it’s worth checking the current one before you travel. Our guide to [[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]] has the routes.</p>
<p>You may also come across towns’ trial homes (<em>otameshi jutaku</em>). They sound perfect, but they’re mostly for people planning to move. Shizuoka City’s, for example, are for people living outside Shizuoka Prefecture who are thinking of moving there and have talked to its relocation advisers first [[s:shizuoka_trial]]. We look at them in [[l:akiya-try-first|living in a town for a month before you buy]].</p>

<h2>Do you need a visa to stay for a month?</h2>
<p>For many visitors, no. Passport holders of many countries and regions can visit Japan for tourism without a visa, and most get up to 90 days (as of November 2026) [[s:jnto_visa]]. Some nationalities may be given 15, 30 or 180 days instead, so it’s your own passport that decides [[s:jnto_visa]].</p>
<p>On that kind of stay you can’t do paid work [[s:jnto_visa]]. If you’d like to work remotely from Japan for longer, [[l:digital-nomad|Japan’s digital nomad visa]] allows a stay of up to six months for some nationalities [[s:isa_nomad_en]]. Our guide to [[l:how-long-stay|how long you can stay in Japan]] covers the other options, from extensions to longer statuses.</p>
<p class="fine">This is general information, not legal or immigration advice. Rules can change, so check the official pages for your own case.</p>
""",
 "faq": [
   ("Can I rent an apartment in Japan on a tourist visa?",
    "An ordinary lease usually isn’t realistic. It typically runs for two years, needs a rent guarantee, and the landlord checks your status of residence first [[s:mlit_foreign_rental_qa]]. For a month, a monthly apartment or a licensed holiday rental with monthly rates is the usual choice."),
   ("Is it legal to rent an Airbnb in Japan for a month?",
    "Yes, if the place is licensed or notified. Registered booking sites have to show the listing’s notification number or licence details [[s:jta_listing_rules]]. A minpaku can host guests on up to 180 nights a year, while a place with a lodging licence has no yearly limit [[s:jta_minpaku_overview]]."),
   ("Why does a Japanese host need a copy of my passport?",
    "Because the law asks them to. If you’re a foreign national without an address in Japan, hosts record your nationality and passport number and keep a copy of your passport, both in minpaku and in licensed lodging [[s:jta_minpaku_users,mhlw_passport]]."),
   ("Are utilities and Wi-Fi included in a monthly rental?",
    "It depends on the place. Some include them, some set a cap and some charge for what you use, so it’s best to ask before you book and to compare the total rather than the monthly rate."),
   ("Is it easy to find a monthly rental outside Tokyo?",
    "There’s less choice, so start early. We think guesthouses and holiday homes with monthly rates make up much of what’s on offer in small towns, and seaside towns fill up in summer."),
 ],
 "sources": ["mlit_foreign_rental_qa", "jta_short_lease_2018", "mlit_fixed_term", "jta_minpaku_overview", "jta_minpaku_act", "jta_listing_rules", "jta_minpaku_users",
             "jta_listing_page", "jta_cancel_2018", "jta_minpaku_illegal", "mhlw_passport", "shimoda_gomi", "node_room", "estat_rent_2025", "stat_rent_note",
             "jre_tt_tokyo", "shizuoka_trial", "jnto_visa", "isa_nomad_en"],
 "related": ["digital-nomad", "akiya-try-first", "izu-from-tokyo"],
 "ja": {
  "h1": "日本で1か月、部屋を借りるには",
  "dek": "日本のふつうの賃貸は、旅行で来る人にはたいてい選べません。1か月なら、マンスリーの部屋か、月割のある許可・届出済みの貸し部屋（民泊など）を探すことになります。",
  "review": [
   "2026-11-20 見せ方のリライト: 詰め込みすぎの文（数字・読点が多い文）4件を0件に。2025年の家賃（東京都区部・静岡市）は小さな表に移し、本文は「静岡市は東京都区部の半分もない」と意味だけを言う形に。下田までの所要時間・ビザの日数は文を分け、「2026年11月時点」の前置きを文末側に寄せました。費用の節の冒頭は、内訳の並べ立てをやめて「比べるのは合計、内訳は下の表」に。合法かの見分け方・1か月以上の理由・違法掲載が消える話・お試し住宅の段落を、答えから入る話し言葉寄りに直しました。事実・数値・出典・リンク・体験は変えていません。",
   "【2026-11-17 品質保証部（原稿 89点・ゲート1）の指摘での書き直し】変えた点: ①【ゲート】ごみ: 「下田市の案内は日本語だけ」→「日本語で書かれている」（確かめた範囲だけ。英語版の有無は書いていません） ②【言い方の変更】2018年11月の通知は「原則1か月が望ましい・自治体に別の目安があればそれで判断」までなので、「決まって1か月以上」→「たいてい1か月以上」、表の最短を「たいてい1か月」にし、「自治体が別の目安を使うこともある」を足しました ③ビザの節に「2026年11月時点」 ④宿泊と賃貸の違いの文を「宿泊では掃除は運営者の仕事で、あなたは住む人ではなく泊まる客。賃貸では契約の期間そこがあなたの住まい」に書き直しました ⑤定期借家の段落に「日本の賃貸契約の種類の1つで、マンスリーの別名ではない」「借りる側にとっては延長をあてにできない」を足しました ⑥費用の節の最初の文を、内訳（家賃・清掃・光熱費・ネット・保証金・手数料）を挙げて「比べるのは合計」と言い切る形に ⑦3物件のごみ置き場のにおいを「長期滞在のレビューの一部」に ⑧In short の3項目めを「登録した予約サイトでは、掲載に許可番号か届出番号が出る」と、予約サイトの掲載の話と分かる形に ⑨人に確かめてほしい点から、写真（編集長が studio-apartment を入れ済み）と、ノマドの記事へのリンクの扱い（同時に公開する前提）を消しました",
   "【2026-11-16 新規（執筆部）】書いた点: ①1記事1主張は「1か月なら、ふつうの賃貸ではなく“1か月から借りられる合法の部屋”を選び、合計の費用と暮らしの設備を予約の前に確かめる」 ②h2 は構成案どおり7つ（借りられるか／種類の比較表／費用の内訳表／合法かの見分け方とパスポート／予約前に聞くことの番号つきリスト／東京の外／ビザ）、FAQ 5問 ③事実はリサーチメモの公的な出典だけで書きました（国交省の外国人の賃貸ガイドライン・定期借家Q&A、観光庁の民泊ポータルと2018年の通知、厚労省の回答、日本政府観光局のビザのページ、総務省の小売物価統計、下田市のごみのページ、NODE Shimoda の公式サイト）。リサーチメモで「書かない」と決めた10件（マンスリー＝定期借家と言い切る、在留カード必須と言い切る、法律で2年、JESTA、査証免除の国名、伊豆の町のお試し住宅、下田市のごみの英語版、マンスリーの相場、NODE Shimoda のいまの週割・月割、2018年の削除件数）は書いていません ④黄色い枠はありません",
   "【自社の体験の使い方（experience.md の人が確認済みの節だけ）】3-2: 開業時に週割・月割を付けた（過去形。「最初の宿」とだけ書き、いまの割引・月額・30泊以上は書いていません）／許可番号が出るまで Airbnb で予約を受けられなかった／古い2芯の配線でエアコン・冷蔵庫・電子レンジを同時に使えなかった／洗濯機と乾燥機がレビューで評価された／夏は海水浴・サーフィンの客が来る。9章: 「私たちのチームが関わる3つの家」として、名簿の質問が多い種類の1つだった・長期滞在のゴミ置き場のにおいの指摘が少しあった・急な階段を予約前に説明したことが好評だった（エリア・件数・自社運営か支援かは書いていません）",
   "【NODE Shimoda に触れるのは節5の最後の1回】公式サイトの客室のページの事実だけ: 約40㎡の一室・階段約13段・シャワーのみでバスタブなし・ワークデスク・高速 Wi-Fi・無料の洗濯機とガス乾燥機・電気の容量が小さいので電子レンジ・掃除機・ドライヤーの間はエアコンを一時止めてもらう・燃えるごみは袋へ、缶やびんはすすいで台所へ、長期滞在はごみについて連絡してもらう。“house” とは呼ばず “flat” にしています。英国英語の “second floor” は日本の3階の意味になるので、階数は書かず「階段約13段」にしました",
   "【検索語】構成案の主な語は “monthly rental japan” ですが、題の “Monthly Rental in Japan” にそのまま入らないため、keywords の先頭を同じ検索の自然な形 “monthly rental in japan” にし、“monthly rental japan”（170・KD16）を2番目に残しました（akiya-try-first の “buying an akiya in japan” と同じ扱い）",
   "【人に確かめてほしい点】①出典 jnto_visa は akiya-try-first の下書きと同じ定義（URL も同じ）にしてあります。リサーチメモでは転送先の /visa-info/ を挙げていますが、同じページです ②法律・制度の記述（playbook 6章）: 賃貸のガイドライン、定期借家、民泊の180日・届出番号の表示・2018年の取り消し、1か月未満は宿泊として扱う通知（2018年11月）、パスポートの写しの保存、ビザなしの滞在日数。どれも 2026-11-16 にリサーチ部が公式ページで確かめたものです ③変わりやすい数字: 下田までの直通 2時間29〜44分（2026年11月の時刻表）、2025年の民営家賃（東京都区部 3.3㎡あたり月9,803円・静岡市 4,621円）",
  ],
  "points": [
    "ふつうの賃貸は2年契約が多く、家賃の保証も求められるので、1か月の滞在にはまず向きません。",
    "旅行で来る人に現実的なのは、マンスリーの部屋か、月割のある許可・届出済みの貸し部屋です。",
    "登録した予約サイトでは、合法の貸し部屋の掲載に許可番号か届出番号が出ていて、泊まるときはパスポートを求められます。",
  ],
  "body": """
<p>1か月は、ホテルでは落ち着かないほど長く、日本のふつうの賃貸を借りるには短すぎます。そのすき間を埋める合法の方法はいくつかありますが、法律の上では同じものではありません。その違いで、掃除を誰がするか、何にお金を払うか、掲載が違法だったときにどうなるかが変わります。</p>

<h2>旅行で来た人が、日本で1か月部屋を借りられるか</h2>
<p>借りられます。ただ、ふつうの賃貸ではなく、1か月単位で貸す前提の部屋を探すことになります。</p>
<p>日本のふつうの賃貸は、たいてい2年契約で、家賃の保証を求められるのがふつうです。保証会社を使うか、連帯保証人を立てます[[s:mlit_foreign_rental_qa]]。国の大家さん向けのガイドラインでは、外国人の申し込みでは、まず在留資格を確かめるよう書かれています。在留期間が契約期間より先に切れると、契約が途中で終わることがある、とも書かれています[[s:mlit_foreign_rental_qa]]。</p>
<p>最初に払うお金もあります。関東では家賃の1〜2か月分の礼金がよくあり、戻ってきません。同じくらいの敷金は、差し引きのあとで戻ります[[s:mlit_foreign_rental_qa]]。私たちの見方では、1か月だけ来る人の多くにとって、ふつうの賃貸は選択肢に入りません。うれしいことに、日本にはちょうどこういう滞在のための部屋があります。</p>

<h2>マンスリー、民泊、シェアハウス：1か月に向くのはどれか</h2>
<p>多くの人は、マンスリーの部屋か、許可・届出済みの貸し部屋かのどちらかになります。違いはおもに法律の上のものですが、掃除を誰がするか、何が含まれるか、どう予約するかが変わります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>種類</th><th>法律の上では</th><th>最短の日数</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>マンスリーの部屋</strong>（マンスリーマンション）</td><td>短期の賃貸借。宿泊ではなく賃貸です[[s:jta_short_lease_2018]]</td><td>たいてい1か月[[s:jta_short_lease_2018]]</td><td>家具付きの部屋を月単位で借ります。賃貸の契約を結ぶので、家賃に何が含まれるかを読んでおきます。</td></tr>
<tr><td><strong>民泊</strong>（届出済みの貸し部屋）</td><td>住宅宿泊事業法にもとづいて届け出た住宅[[s:jta_minpaku_overview]]</td><td>ホストが決める</td><td>ゲストを泊められるのは年180日までで、自治体の条例でさらに制限されることもあります[[s:jta_minpaku_act]]。</td></tr>
<tr><td><strong>宿・貸別荘</strong>（旅館業の許可あり）</td><td>旅館業法の許可を受けたもの。たとえば簡易宿所[[s:jta_minpaku_overview]]</td><td>ホストが決める</td><td>営業日数の上限がないので、一年中泊められます[[s:jta_minpaku_overview]]。</td></tr>
<tr><td><strong>シェアハウス</strong></td><td>たいていは賃貸で、条件は運営会社ごと</td><td>運営会社が決める</td><td>寝室は自分だけ、台所と浴室は共用です。条件の差が大きいので、書面でもらっておくと安心です。</td></tr>
</tbody></table></div>
<p>マンスリーの部屋が、なぜたいてい1か月以上なのか。日本がどこで線を引いているか、という話です。観光庁と厚生労働省は、1か月に満たない滞在を、原則として賃貸ではなく宿泊として扱っています。そのため短期の賃貸は、原則1か月以上の滞在を条件にし、賃貸だとはっきり書くことになっています。ただし、自治体が別の目安を使うこともあります[[s:jta_short_lease_2018]]。マンスリーは短期の民泊と同じサイトに並べて載せないことにもなっていて、そのため、探す場所が分かれていることがよくあります[[s:jta_short_lease_2018]]。</p>
<p>受けられるものも違います。宿泊では、部屋を清潔に保つのは運営者の仕事で、あなたはそこに住む人ではなく、泊まる客です。賃貸では、契約の期間、そこがあなたの住まいになります[[s:jta_short_lease_2018]]。どちらを選ぶにしても、掃除を誰がどれくらいの頻度でするかは、聞いておくといいと思います。</p>
<p>「定期借家」という言葉を目にすることもあるかもしれません。これは日本の賃貸契約の種類の1つで、マンスリーの部屋の別名ではありません。借りる側にとっての意味は、延長をあてにできないことです。契約に書いた日で終わり、更新はありません。ただし、貸す人と借りる人が合意すれば、新しく契約を結べます。書面で契約し、更新がないことを、貸す人が別の書面で説明しなければなりません[[s:mlit_fixed_term]]。</p>

<h2>1か月いくらかかり、何が含まれるか</h2>
<p>家賃は費用の一部にすぎないので、比べたいのは合計です。値段は町によって違いすぎて、1つの数字ではあまり役に立ちません。どこでもだいたい同じなのは、家賃のほかにかかるものの種類です。それぞれ、私たちなら次のことを聞きます。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>何に払うか</th><th>なぜ大事か</th><th>聞くこと</th></tr></thead>
<tbody>
<tr><td>家賃・1泊の料金</td><td>最初に目に入る数字で、いちばん比べやすい</td><td>週割・月割はあるか。この料金にもう入っているか</td></tr>
<tr><td>清掃</td><td>1回分の料金のことも、滞在中の定期的な清掃のことも、まったくないこともある</td><td>滞在中の清掃は含まれるか。どれくらいの頻度か</td></tr>
<tr><td>電気・ガス・水道</td><td>込みのことも、上限つきのことも、使った分だけ払うこともある</td><td>上限はあるか。超えたらどうなるか</td></tr>
<tr><td>インターネット</td><td>仕事をするなら、遅い回線で1か月は厳しい</td><td>固定回線か、モバイルルーターか</td></tr>
<tr><td>保証金</td><td>最後に返してほしいお金</td><td>あるか。いつ、どうやって戻るか</td></tr>
<tr><td>予約サイトの手数料</td><td>最初に見た料金が、最後の合計とは限らない</td><td>合計に予約サイトのサービス料は入っているか</td></tr>
<tr><td>途中で帰る場合</td><td>1か月のあいだには予定が変わることもある</td><td>早く帰ったら、使わなかった分は返金されるか</td></tr>
</tbody></table></div>
<p>月割があるのには理由があります。貸す側から見ると、長く泊まってもらえれば、ゲストの入れ替えの清掃が減ります。だから私たちも、最初の宿を開いたとき、週割と月割を付けました。掲載に割引が出ていなくても、聞いてみて損はありません。</p>

<h2>民泊が合法かどうか、どう見分けるか</h2>
<p>いちばん手早い目印は、掲載に届出番号か許可番号が出ているかです。2018年6月から、日本で住宅に有料で人を泊めるには、きちんとした許可などが必要になりました[[s:jta_minpaku_overview]]。旅館業法の許可、特区民泊の認定、住宅宿泊事業法の届出のどれかです[[s:jta_minpaku_overview]]。</p>
<p>住宅宿泊仲介業者として登録した予約サイトは、掲載ごとに届出番号などを表示しなければなりません[[s:jta_listing_rules]]。観光庁は、予約サイトで届出番号と物件の住所が確かめられるかを見るよう勧めています[[s:jta_minpaku_users]]。旅館業の許可の宿は、届出番号ではなく許可番号を出すので、表示の形はいつも同じとは限りません。私たちも貸す側としてこれを知っています。許可が下りるまで、Airbnb で予約を受けられませんでした。</p>
<p>1か月の滞在でいちばん困るのは、予約している違法な掲載が、途中で消えてしまうことです。登録した予約サイトは、半年ごとに掲載している物件を観光庁に報告し、違法と分かった掲載は、求められたらすぐに削除しなければなりません[[s:jta_listing_page]]。法律が始まった2018年6月には、予約サイトは届出のない物件の先の予約を取り消すか、合法の物件に移すよう求められました[[s:jta_cancel_2018]]。観光庁は、民泊は登録した予約サイトか旅行会社を通して予約するよう呼びかけています[[s:jta_minpaku_illegal]]。</p>
<p>民泊の年180日の上限は、ホストの側の上限で、泊まる人の上限ではありません。物件ごとに、4月1日の正午から始まる1年で数えます[[s:jta_minpaku_act]]。つまり、そういう住宅は一年中は貸せない、というだけのことです。</p>
<p>ホストはなぜパスポートを求めるのか。法律でそう決まっているからです。住宅宿泊事業法では、日本に住所のない外国籍の宿泊者は、国籍と旅券番号を伝え、ホストは旅券の写しを保存します[[s:jta_minpaku_users]]。旅館業の許可の宿でも同じで、宿泊者名簿に国籍と旅券番号を書き、厚生労働省は、旅券を確かめて写しを名簿と一緒に保存するよう求めています[[s:mhlw_passport]]。私たちのチームが関わる3つの家でも、宿泊者名簿についての質問は、とくに多いものの1つでした。気になるのはあなただけではありません。</p>

<h2>1か月まるごと予約する前に、何を聞くか</h2>
<p>写真に写っていることより、毎日付き合うことを聞きます。私たちなら、次の順に聞きます。</p>
<ol>
<li><strong>インターネット</strong>　固定回線か。調子が悪いとき、ルーターはどこにあって、どう再起動するか。ビデオ会議があるなら、速さと同じくらい、ちゃんとした机が大事です。</li>
<li><strong>電気</strong>　一度にどれくらい使えるか。私たちの最初の部屋では、古い2芯の配線で、エアコンと冷蔵庫と電子レンジを同時に使えませんでした。ブレーカーの場所を知っておくのも役に立ちます。</li>
<li><strong>冷暖房</strong>　寝る部屋にエアコンがあるか。その電気代は含まれているか。</li>
<li><strong>洗濯</strong>　洗濯機と乾燥機はあるか。私たちのゲストもレビューで両方をほめてくれました。梅雨の1か月の洗濯を考えれば、理由は分かると思います。</li>
<li><strong>ごみ</strong>　長期の滞在ではどうするか。分け方と収集日は町ごとに違い、たとえば下田市の案内は日本語で書かれています[[s:shimoda_gomi]]。私たちのチームが関わる3つの家では、長期滞在のレビューの一部に、ごみ置き場のにおいの指摘がありました。</li>
<li><strong>清掃と寝具</strong>　滞在中に清掃やシーツの交換はあるか。それとも全部自分でするのか。</li>
<li><strong>階段と浴室</strong>　何階か、エレベーターはあるか、浴槽はあるかシャワーだけか。私たちのチームが関わる家の1つでは、急な階段のことを予約の前に説明しておいたのが好評でした。</li>
<li><strong>移動</strong>　駐車場はあるか。バス停やスーパーは歩いて行けるか。</li>
<li><strong>途中で帰る場合</strong>　予定が変わったら、使わなかった日の分はどうなるか。</li>
</ol>
<p>役に立つ答えがどんなものか、私たちの部屋「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」で答えてみます。約40㎡の部屋をまるごと貸していて、階段を約13段上がり、シャワーはありますが浴槽はありません[[s:node_room]]。ワークデスク、速い Wi-Fi、無料の洗濯機とガス乾燥機があります[[s:node_room]]。電気の容量が小さいので、電子レンジ・掃除機・ドライヤーを使うあいだは、エアコンを少しだけ止めてもらっています[[s:node_room]]。燃えるごみはごみ箱へ、すすいだ缶やびんは台所に置いてもらい、長く泊まる方には、ほかのことは連絡してもらうようにしています[[s:node_room]]。</p>

<h2>東京の外で1か月借りるのは、むずかしいか</h2>
<p>選べる数は少なくなりますが、早めに探せば十分できます。小さな町では、マンスリーの部屋は少なく、月割のある宿や貸別荘のほうが多いと私たちは思います。</p>
<p>住まいの値段は、東京を離れると下がります。静岡市の民営家賃は、面積あたりで東京都区部の半分もありません[[s:estat_rent_2025]]。これは調べた住宅のふつうの賃貸の家賃で、マンスリーの値段ではありませんが[[s:stat_rent_note]]、差の大きさの目安になります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>場所</th><th>民営家賃の平均（3.3㎡あたり月額・2025年）</th></tr></thead>
<tbody>
<tr><td>東京都区部</td><td>9,803円[[s:estat_rent_2025]]</td></tr>
<tr><td>静岡市</td><td>4,621円[[s:estat_rent_2025]]</td></tr>
</tbody></table></div>
<p>移動の手段も大事になります。バスが少ないこともあるので、スーパーまで歩いて行ける部屋なら、車がなくても毎日がずっと楽です。海の町は夏に混みます。私たちが宿をしている下田でも、夏は海水浴やサーフィンの人が来るので、7月や8月の1か月は、かなり早めに予約したほうがいいです。</p>
<p>小さな町で、それでも行きやすいところなら、伊豆半島は1つの候補です。東京駅から直通の電車が毎日走っていて、下田まで2時間29〜44分です[[s:jre_tt_tokyo]]。2026年11月の時刻表なので、出かける前に一度見ておくと安心です。くわしい行き方は[[l:ja-izu-from-tokyo|東京から伊豆半島への行き方の記事]]にまとめています。</p>
<p>自治体の「お試し住宅」を目にすることもあると思います。ぴったりに見えますが、多くは移住するつもりの人向けで、たとえば静岡市のお試し住宅は、静岡県の外に住んでいて、市への移住を考えていて、先に市の移住の相談員と話した人が対象です[[s:shizuoka_trial]]。お試し住宅のことは、[[l:ja-akiya-try-first|買う前にその町で1か月暮らす記事]]で取り上げています。</p>

<h2>1か月いるのに、ビザは要るか</h2>
<p>多くの人は要りません。多くの国・地域のパスポートを持つ人は、観光ならビザなしで日本に来られ、ほとんどは90日までです（2026年11月時点）[[s:jnto_visa]]。国籍によっては15日・30日・180日になることもあるので、決め手になるのは自分のパスポートです[[s:jnto_visa]]。</p>
<p>この滞在では、報酬を得る仕事はできません[[s:jnto_visa]]。もっと長く、日本からリモートで働きたいなら、[[l:ja-digital-nomad|日本のデジタルノマドビザ]]で、一部の国籍の人は最長6か月滞在できます[[s:isa_nomad_en]]。延長やもっと長い在留資格など、ほかの方法は[[l:ja-how-long-stay|日本に何日いられるかのガイド]]にまとめました。</p>
<p class="fine">これは一般的な情報で、法律や在留手続きの助言ではありません。決まりは変わることがあるので、自分の場合は公式のページで確かめてください。</p>
""",
  "faq": [
    ("観光ビザで、日本のアパートを借りられますか",
     "ふつうの賃貸は、たいてい現実的ではありません。多くは2年契約で、家賃の保証が要り、大家さんはまず在留資格を確かめます[[s:mlit_foreign_rental_qa]]。1か月なら、マンスリーの部屋か、月割のある許可・届出済みの貸し部屋を選ぶのがふつうです。"),
    ("日本で Airbnb を1か月借りるのは合法ですか",
     "許可か届出のある部屋なら合法です。登録した予約サイトは、掲載に届出番号などを出さなければなりません[[s:jta_listing_rules]]。民泊がゲストを泊められるのは年180日までで、旅館業の許可の宿には年の上限がありません[[s:jta_minpaku_overview]]。"),
    ("日本のホストは、なぜパスポートの写しが要るのですか",
     "法律でそう決まっているからです。日本に住所のない外国籍の人なら、民泊でも旅館業の宿でも、ホストは国籍と旅券番号を記録し、パスポートの写しを保存します[[s:jta_minpaku_users,mhlw_passport]]。"),
    ("マンスリーの部屋に、光熱費や Wi-Fi は含まれていますか",
     "部屋によります。込みのところも、上限つきのところも、使った分だけ払うところもあるので、予約の前に聞いて、月の料金ではなく合計で比べるのがいちばんです。"),
    ("東京の外で、マンスリーの部屋は見つかりやすいですか",
     "選べる数は少ないので、早めに探してください。小さな町では、月割のある宿や貸別荘が選択肢の多くを占めると私たちは思います。海の町は夏に混みます。"),
  ],
 },
},
# ============================================================ 下田
{
 "id": "shimoda-guide", "slug": "shimoda-guide", "topic": "stay", "place": "izu", "also": ["live"],
 "photo": ("stony-shore-waves", "Waves breaking on a stony beach under a clear blue sky, with one person walking at the water’s edge", ""),
 "published": "2026-11-20", "updated": "2026-11-20",
 "kicker": "Izu Peninsula",
 "h1": "Shimoda, Japan: a guide for a week or longer",
 "seo_title": "Shimoda, Japan: Beaches, Old Town and a Week-Long Stay",
 "description": "Shimoda is a small port town at the tip of Izu with nine official beaches. A week lets you pick beaches by mood, walk the old town and cook local fish.",
 "dek": "Shimoda is a small port town at the southern tip of the Izu Peninsula. In a week, you can pick beaches by mood, cook local fish and settle in.",
 "card": "Shimoda is a port town at the southern tip of Izu, with nine official beaches and an old town you can walk. A week gives you time to pick beaches by mood, shop for fish and cook, and see the town outside the summer rush.",
 "keywords": [("shimoda", "5,400", "21"), ("shimoda japan", "5,400", "21"), ("shimoda beaches", "210", "—")],
 "intent": "Know → Do（どんな町か → 1週間をどう過ごすか）",
 "points": [
   "Pick a beach by what you want: calm coves for children, surf beaches, or a quieter stretch of sand.",
   "The old town is easy on foot: the ropeway, port and Perry Road are within 15 minutes of the station.",
   "Outside summer it’s quieter, with daffodils in winter, the Black Ship Festival in May and hydrangeas in June.",
 ],
 "body": """
<h2>Is Shimoda worth a week?</h2>
<p>We think so, if you want more than one beach and a quick look at the station area. A night is enough to swim once and eat well. A week lets you try different beaches, find a café you like and fall into the town’s slower rhythm.</p>
<p>Shimoda sits at the southern tip of the [[l:izu|Izu Peninsula]], and it’s a small town of about 18,400 people (November 2026) [[s:shimoda_population]]. The coastline, though, runs for around 47 kilometres [[s:shimoda_profile]], so there’s far more shore to explore than the size suggests.</p>
<p>This is also where Japan first opened its doors to America. Under the 1854 Treaty of Kanagawa, Shimoda became one of the country’s first two open ports [[s:shimoda_hist_perry]], and you’ll keep bumping into that story as you walk the old town.</p>
<p>The train ride from Tokyo is long enough that you’ll want to stay put once you’re here. We’ve covered trains, fares and bus passes in [[l:izu-from-tokyo|our guide to getting to Izu from Tokyo]]. If you have more than a week, we’d spend most of it in Shimoda and add a night or two elsewhere on the peninsula.</p>

<h2>Which Shimoda beach suits you?</h2>
<p>It depends on what you want from the day, because Shimoda’s nine official beaches are surprisingly different. Some are sheltered coves where small children can paddle, and others are known for surfing.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Beach</th><th>What it’s like</th><th>Good for</th><th>From Izukyu-Shimoda Station</th></tr></thead>
<tbody>
<tr><td><strong>Nabetahama</strong> (130 m)</td><td>The beach closest to town, in an inlet with hardly any waves. There’s no car park or shower [[s:shimoda_kanko_beach_nabeta]].</td><td>A quick swim, small children</td><td>Bus from stand 3 or 4, about 7 min, then 5 min on foot [[s:shimoda_kanko_beach_nabeta]]</td></tr>
<tr><td><strong>Sotoura</strong> (470 m)</td><td>A cove with shallow, calm water, popular with families. People sea-kayak further out. No surfing area [[s:shimoda_kanko_beach_sotoura]].</td><td>Children, calm swimming</td><td>Bus from stand 9, about 10 min, then 3 min on foot [[s:shimoda_kanko_beach_sotoura]]</td></tr>
<tr><td><strong>Shirahama Chuo</strong> (720 m)</td><td>The quiet north end of the Shirahama coast, with rock pools. It’s the only beach in Shimoda where you can barbecue [[s:shimoda_kanko_beach_shirahamachuo]].</td><td>Families, rock pools</td><td>Bus from stand 9, about 18 min, then 1 min on foot [[s:shimoda_kanko_beach_shirahamachuo]]</td></tr>
<tr><td><strong>Shirahama Ohama</strong> (about 700 m)</td><td>One of the largest beaches in Izu, by the main coast road and busy with surfers and young people [[s:shimoda_beaches_city,shimoda_kanko_beach_shirahama]].</td><td>A lively day, surfing</td><td>Bus from stand 9, about 15 min [[s:shimoda_kanko_beach_shirahama]]</td></tr>
<tr><td><strong>Tatadohama</strong> (450 m)</td><td>Well known for surfing and bodyboarding, with national contests. It has warm showers you can use all year [[s:shimoda_kanko_beach_tatado]].</td><td>Surfing</td><td>Bus from stand 3 or 4, about 7 min, then 3 min on foot [[s:shimoda_kanko_beach_tatado]]</td></tr>
<tr><td><strong>Kisami Ohama</strong> (770 m)</td><td>A big beach away from the main road, so it feels quieter. Surfers and families share it, and there are cafés nearby [[s:shimoda_kanko_beach_kisami]].</td><td>A long, quieter day</td><td>Bus from stand 3 or 4, about 10 min, then 8 min on foot [[s:shimoda_kanko_beach_kisami]]</td></tr>
</tbody></table></div>
<p class="fine">Beach lengths are the tourism association’s figures; for Shirahama Ohama, the city’s list. The “stand” is the numbered bus stop outside the station.</p>
<p>That leaves three more. Iritahama is a calm beach lined with cycad trees, and surfers use it too [[s:shimoda_kanko_beach_irita]]. Kujuppama is a 50-metre cove next to the Suzaki Imperial Villa, with rock pools on both sides and no large tents allowed [[s:shimoda_kanko_beach_kujuppama]]. Toji is rarely crowded and close to the Ryugu sea cave, but only four or five buses a day go there [[s:shimoda_kanko_beach_toji]], so it’s a beach you plan your day around.</p>
<p>Wherever you end up, the water’s clean. In Shizuoka Prefecture’s 2026 survey, all nine beaches got the top AA grade [[s:pref_beach_water_2026]]. Six of them (every beach in the table except Nabetahama, plus Iritahama) also hold a safety certification from the Japan Lifesaving Association [[s:shimoda_beaches_city]].</p>
<p>Lifeguards are only on duty during the official season, which the city sets each year [[s:shimoda_ohama]]. Our [[l:izu-from-tokyo|Izu travel guide]] has the 2026 dates. The season also comes with a few rules that are worth knowing before you pack [[s:shimoda_kanko_umi]]:</p>
<ul>
<li>No tents, though sunshades are fine.</li>
<li>No open fires or barbecues, except in part of Shirahama Chuo.</li>
<li>No fireworks and no overnight camping.</li>
<li>No amplified speakers, a rule added in 2025 [[s:shimoda_kanko_umi]].</li>
</ul>

<h2>What can you do in Shimoda besides the beach?</h2>
<p>Quite a lot, and most of it is within a short walk of the station. On a day off the sand, we’d start high up, wander the old town and finish in a hot bath.</p>
<p>The Shimoda Ropeway station is a one-minute walk from Izukyu-Shimoda Station. From the top of Mt Nesugata you can see the town, the port, the Izu Islands and the Amagi mountains [[s:shimoda_nesugata]]. Back down, the port and the Michi-no-Eki, a roadside market building, are about 10 minutes away on foot [[s:shimoda_michinoeki]].</p>
<p>For the history, head to Perry Road and Ryosenji temple, about 15 minutes from the station [[s:shimoda_perryroad,shimoda_ryosenji]]. Perry Road follows the route Perry’s men marched to the temple. Today it’s about 500 metres of stone paving beside a small stream [[s:shimoda_hist_perry,shimoda_perryroad]], and we think it’s one of the nicest short walks in town. Later in 1854, the follow-up Shimoda Treaty was signed in Ryosenji’s main hall [[s:shimoda_hist_perry]]. If you’d like to go further, Gyokusenji temple housed Japan’s first US consulate, opened by Townsend Harris in 1856 [[s:shimoda_hist_harris,shimoda_gyokusenji]].</p>
<p>To end the day in hot water, eight hotels and inns open their baths to day visitors [[s:shimoda_kanko_onsen]]. Adults pay between ¥600 and ¥1,500 (as of November 2026). Each place opens at its own time, somewhere between 10:00 and 15:00, and they may turn you away when they’re busy [[s:shimoda_kanko_onsen]]. If you just want to warm your feet, the Kaikoku-no-yu footbath in front of the station is open from 9:00 to 17:00 [[s:shimoda_kanko_onsen]].</p>
<p>Rain doesn’t have to ruin the day. The Michi-no-Eki has a harbour museum about the town’s history on its fourth floor [[s:shimoda_michinoeki]], and Ryosenji has a treasure hall [[s:shimoda_ryosenji]]. On a dry day, the Wakanoura promenade takes you 1.2 kilometres along the coast in about 15 minutes [[s:shimoda_kanko_promenade]]. For something longer, the paths round Shimoda Park take about an hour and a half [[s:shimoda_kanko_promenade]].</p>

<h2>Is Shimoda worth visiting outside summer?</h2>
<p>Yes. The beaches go quiet, but there’s something on in most seasons. It’s mild, too: the city puts the average yearly temperature at about 17°C [[s:shimoda_profile]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>When</th><th>What’s on</th></tr></thead>
<tbody>
<tr><td>20 December to 31 January</td><td>The daffodil festival at Tsumekizaki, with up to about 3 million flowers, usually at their best in January. The bus from stand 10 outside the station takes about 20 minutes [[s:shimoda_kanko_suisen]].</td></tr>
<tr><td>Winter into early spring</td><td>Camellias in Shimoda Park, with about 160 garden varieties [[s:shimoda_park]]. Cherry blossoms follow from mid-March to early April [[s:shimoda_kanko_event]].</td></tr>
<tr><td>May</td><td>The Black Ship Festival, held since 1934. In 2026 it ran from 15 to 17 May, with fireworks over the port, a US–Japan parade and a re-enactment of the Shimoda Treaty at Ryosenji [[s:shimoda_kanko_kurofune]].</td></tr>
<tr><td>June</td><td>The hydrangea festival in Shimoda Park, with about 3 million blooms of over 100 varieties (1 to 30 June in 2026). The park is hilly, and carts are on hand for people who find walking hard [[s:shimoda_kanko_ajisai]].</td></tr>
<tr><td>July and August</td><td>Beach season. In 2026 there were fireworks at Shirahama on 25 July, and the old town’s Taiko Matsuri drum festival is held on 14 and 15 August [[s:shimoda_kanko_event]].</td></tr>
<tr><td>Autumn</td><td>Hand-held <em>te-zutsu</em> fireworks (10 October in 2026), the Shirahama shrine festival in late October, and the start of the spiny lobster (<em>ise-ebi</em>) season, which runs to early May [[s:shimoda_kanko_event]].</td></tr>
</tbody></table></div>
<p>Summer is when the town fills up, and in our experience it’s also when more of our guests stay for longer. If you’d rather walk, soak and eat well than swim, we’d pick the cooler months.</p>

<h2>How do you shop and cook for a week in Shimoda?</h2>
<p>Our advice is to buy your fish at the port and cook it yourself, which is half the fun of having a kitchen. The Izu Fisheries Cooperative shop is on the ground floor of the Michi-no-Eki Kaikoku Shimoda Minato. It’s where you’ll find kinmedai, live spiny lobster, turban shells and other seafood [[s:pref_izu_gyokyo_shop,shimoda_kanko_gift]]. It’s open from 8:00 to 16:30 with no fixed closing day (as of April 2025) [[s:pref_izu_gyokyo_shop]]. The JA farmers’ shop in the same building has local vegetables, wasabi and products made from New Summer oranges [[s:shimoda_kanko_gift]].</p>
<p>If you’d rather have someone else cook the town’s famous red fish, our [[l:kinmedai|guide to kinmedai]] covers where to eat it. For everyday shopping, there are supermarkets and convenience stores in town, so a kitchen makes a week much cheaper and more relaxed.</p>
<p>Rubbish takes a little learning. Burnable rubbish goes out twice a week in city bags [[s:shimoda_gomi]]. Cans, bottles, PET bottles and paper are collected separately, twice a month [[s:shimoda_gomi]]. Every place has its own system, though, so it’s easiest to ask your host when you arrive. Here’s what else we’d do on day one:</p>
<ol>
<li>Find the nearest supermarket and the fish shop at the Michi-no-Eki.</li>
<li>Ask your host how to sort rubbish and where it goes.</li>
<li>Pick up a map at the tourism information centre near the station, open from 9:00 to 16:45 [[s:shimoda_kanko_about]].</li>
<li>Look up the bus times for the beaches you want, since some routes run only a few times a day.</li>
<li>Find the nearest high ground from where you’re staying (see the next section).</li>
</ol>

<h2>What should you know about tsunamis in Shimoda?</h2>
<p>If you feel a strong earthquake near the coast, go to high ground straight away, without waiting for a warning [[s:jma_tsunami_warnings]]. Shimoda faces the open sea, and in 1854 the Ansei tsunami swept Shimoda Bay and destroyed most of the town’s houses [[s:shimoda_hist_ansei]].</p>
<p>Shizuoka Prefecture’s 2013 estimate looked at the worst case, which it describes as extremely unlikely, and put the highest possible tsunami in Shimoda at 33 metres [[s:shimoda_news_2013_08]]. It isn’t a forecast, but it’s why the advice is to get up high, fast. Japan’s weather agency, JMA, aims to issue alerts about three minutes after an earthquake [[s:jma_tsunami_warnings]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Alert</th><th>Expected wave</th><th>What to do</th></tr></thead>
<tbody>
<tr><td><strong>Tsunami advisory</strong></td><td>0.2 to 1 m</td><td>Get out of the water and away from the shore [[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>Tsunami warning</strong></td><td>1 to 3 m</td><td>Move to high ground or an evacuation building at once [[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>Major tsunami warning</strong></td><td>Over 3 m</td><td>Move to high ground or an evacuation building at once [[s:jma_tsunami_warnings]]</td></tr>
</tbody></table></div>
<p>Tsunamis come in several waves, so JMA advises you to stay on high ground until the warning or advisory is lifted [[s:jma_tsunami_warnings]]. The city publishes hazard and evacuation maps, though only in Japanese [[s:shimoda_tsunami_map]]. It has also named a few tsunami evacuation buildings [[s:shimoda_tsunami_bldg]], and it runs an online map that shows the height above sea level of any spot you tap [[s:shimoda_elevation_map]].</p>
<p>The Japan Tourism Agency’s free app, Safety tips, sends earthquake, tsunami and weather warnings in English and other languages [[s:jta_safety_tips]]. We’d install it before you arrive. In late July 2025, there was a tsunami warning for the Shizuoka coast, later downgraded to an advisory [[s:jma_kamchatka_2025,jma_kamchatka_2025_eve]]. As things changed, we messaged our overseas guests to tell them what was happening and that they needed to evacuate. Guests thanked us afterwards.</p>

<h2>Where should you stay in Shimoda for a week?</h2>
<p>Without a car, we’d stay in the old town near the station. Shops, the port and every bus route are close by. If the beach is the whole point of your trip, staying near it saves you the bus rides.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Area</th><th>Suits you if…</th><th>Keep in mind</th></tr></thead>
<tbody>
<tr><td><strong>Old town, near the station</strong></td><td>You want to walk to shops, the port and Perry Road, and reach any beach by bus.</td><td>You’ll need a bus or a bike for most beaches.</td></tr>
<tr><td><strong>Shirahama</strong></td><td>You want the big beaches on your doorstep.</td><td>It’s about 15 minutes by bus from town [[s:shimoda_kanko_beach_shirahama]], so evenings out mean a ride back.</td></tr>
<tr><td><strong>Southern beaches</strong> (Tatado, Irita, Kisami)</td><td>You’re here to surf or want a quieter beach.</td><td>They’re 7 to 10 minutes by bus from the station [[s:shimoda_kanko_beach_tatado,shimoda_kanko_beach_kisami]], plus a short walk.</td></tr>
</tbody></table></div>
<p>Wherever you stay, a bike makes the week much easier. The tourism association rents bikes and e-bikes at the Michi-no-Eki, from ¥500 for an hour or ¥2,000 for a day [[s:shimoda_kanko_bicycle]]. Rentals run from 9:00 to 17:00. You don’t need to book, but you’ll need ID such as a passport [[s:shimoda_kanko_bicycle]].</p>
<p>We run <a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>, an apartment of about 40 m² in the old town for up to four guests. It has a kitchen, a washing machine and gas dryer, and a work desk. It’s on the first floor, up about 13 steps, with a shower but no bath [[s:node_room]]. It’s an eight-minute walk on the flat from the station [[s:node_access]]. The supermarket is three minutes away, and Perry Road five. One guest who stayed in January wrote that the sea was close by, they could see the year’s first sunrise, and the supermarket was handy.</p>
<p>If a week turns into thoughts of a month or more, our guide to [[l:monthly-rental|renting a place by the month in Japan]] explains how that works.</p>
""",
 "faq": [
   ("Is Shimoda worth visiting?",
    "Yes, especially for a week. It’s a small port town at the tip of Izu with nine official beaches, a walkable old town and seasonal festivals [[s:shimoda_population,shimoda_kanko_umi,shimoda_kanko_event]]. A week lets you try several beaches and live at the town’s pace."),
   ("What is the best beach in Shimoda?",
    "It depends on what you want. Sotoura and Nabetahama are calm coves that suit children [[s:shimoda_kanko_beach_sotoura,shimoda_kanko_beach_nabeta]]. Tatadohama is especially well known among surfers [[s:shimoda_kanko_beach_tatado]], and Kisami Ohama is big and quieter [[s:shimoda_kanko_beach_kisami]]."),
   ("Can you swim in Shimoda outside summer?",
    "Lifeguards only work during the official season, which the city sets each year, so outside it you swim without them [[s:shimoda_ohama]]. Tatadohama has warm showers you can use all year [[s:shimoda_kanko_beach_tatado]]."),
   ("What is there to do in Shimoda in winter?",
    "The daffodil festival at Tsumekizaki runs from 20 December to 31 January [[s:shimoda_kanko_suisen]], and camellias bloom in Shimoda Park [[s:shimoda_park]]. Day hot springs, the ropeway and coastal walks fill the rest of the week [[s:shimoda_kanko_onsen,shimoda_nesugata,shimoda_kanko_promenade]]."),
   ("What should I do if there’s a tsunami warning in Shimoda?",
    "Move to high ground or an evacuation building at once, and stay until the warning is lifted. If you feel strong shaking near the coast, go without waiting for a warning [[s:jma_tsunami_warnings]]. The free Safety tips app sends alerts in English [[s:jta_safety_tips]]."),
 ],
 "sources": ["shimoda_population", "shimoda_profile", "shimoda_hist_perry", "shimoda_hist_harris", "shimoda_hist_ansei",
             "shimoda_perryroad", "shimoda_ryosenji", "shimoda_gyokusenji", "shimoda_nesugata", "shimoda_park", "shimoda_michinoeki",
             "shimoda_beaches_city", "shimoda_kanko_umi", "shimoda_kanko_beach_nabeta", "shimoda_kanko_beach_sotoura",
             "shimoda_kanko_beach_shirahamachuo", "shimoda_kanko_beach_shirahama", "shimoda_kanko_beach_tatado",
             "shimoda_kanko_beach_kisami", "shimoda_kanko_beach_irita", "shimoda_kanko_beach_kujuppama", "shimoda_kanko_beach_toji",
             "pref_beach_water_2026", "shimoda_ohama", "shimoda_kanko_onsen", "shimoda_kanko_promenade", "shimoda_kanko_suisen",
             "shimoda_kanko_event", "shimoda_kanko_kurofune", "shimoda_kanko_ajisai", "pref_izu_gyokyo_shop", "shimoda_kanko_gift",
             "shimoda_gomi", "shimoda_kanko_about", "jma_tsunami_warnings", "jma_kamchatka_2025", "jma_kamchatka_2025_eve", "shimoda_news_2013_08", "shimoda_tsunami_map",
             "shimoda_tsunami_bldg", "shimoda_elevation_map", "jta_safety_tips", "shimoda_kanko_bicycle", "node_room", "node_access"],
 "related": ["izu-from-tokyo", "kinmedai", "monthly-rental"],
 "ja": {
  "h1": "下田（日本）：1週間以上いる人のためのガイド",
  "dek": "下田は、伊豆半島の南端にある小さな港町です。1週間いれば、その日の気分で浜を選び、地元の魚を料理して、町の暮らしになじめます。",
  "review": [
   "2026-11-20 見せ方のリライト: 「ガイドブックのような固さ」をなくすため、英語と日本語の語り口を直しました。①1文に数字や条件を詰めた文を分け、海水浴期間中の禁止事項は短いリストにしました（詰め込みすぎの文 7件→1件。日帰り入浴の料金の文は短いので残しました） ②「歴史の大きな場所」のような決まり文句を、具体的な言い方（アメリカに初めて開いた港、旧町内で出会う話）に ③名所に「読み手にとっての意味」を1言ずつ（例: 田牛は時刻表に合わせて予定を組む浜、ライフセービングの認定は表の浜のうち鍋田浜以外の5つと入田浜、ペリーロードは気持ちのいい散歩道だと私たちは思う） ④漁協の直売所の時間は「（2025年4月時点）」と時点だけを添えました。事実・数値・出典・リンク・体験の中身は変えていません。",
   "【2026-11-20 品質保証部（83点・ゲート違反1）の指摘での直し（英語と日本語の両方）】①駅前の足湯「開国の湯」の「無料」を消しました（公式の出典に料金の記載がないため。時間9時〜17時だけ） ②日帰り入浴の「多くは午後の半ばから」を「開く時間は10時〜15時と施設によって違う」に ③FAQ の多々戸浜を「いちばん知られた」から「サーファーの間で特に有名」に ④「残りの3つは小さめ」をやめました（入田浜400m・田牛410mは鍋田浜より長いため） ⑤下田条約の時期を「同じ1854年のうちに」に（英語の Later in 1854 と同じ） ⑥漁協の直売所の時間に「県のページ、2025年4月更新」を付けました ⑦水仙まつりへのバスを「駅前の10番乗り場から」に（英語も stop 10） ⑧気象庁の呼びかけを「解除されるまで高い所にとどまる」に ⑨33mの文は「発生する頻度は極めて低い（出典の記載）」を同じ文に入れ、「怖がらせたいのではありません」の文を消しました ⑩津波の体験は、experience.md の記録（2026-11-20 人の了承で直った）どおり「2025年7月末、静岡県の沿岸に津波警報が出て、のちに注意報に切り替わった」と気象庁の報道発表を出典に書き、最後を「ゲストからは、あとで感謝の言葉をもらった」にしました（新しい出典 jma_kamchatka_2025・jma_kamchatka_2025_eve） ⑪1月のゲストの声を「海が近く、初日の出も見られ、スーパーも便利」の並列に（因果を足さない）",
   "【2026-11-20 新規の下書き（執筆部）】書いた点: ①7つの節（1週間いる価値／浜の選び方／浜以外の過ごし方／夏以外の季節／買い物と料理・ごみ／津波／どこに泊まるか）。事実はすべて、市・県・観光協会・気象庁・観光庁の公式のページによります ②浜の表は6つ（鍋田浜・外浦・白浜中央・白浜大浜・多々戸浜・吉佐美大浜）、残りの3つ（入田浜・九十浜・田牛）は文章で。白浜大浜の長さは市の一覧の「約700m」、ほかの長さは観光協会の値です ③人口は「約18,400人（2026年11月の住民基本台帳）」。日米和親条約は「1854年に下田を最初に開いた2つの港の1つにした」とだけ書き、調印の場所は書いていません。了仙寺は付録の「下田条約」の場として書きました ④静岡県の2013年の想定（最悪の場合、下田の最大の津波の高さ33m。発生頻度は極めて低い）を1文入れました。到達時間は書いていません ⑤NODE Shimoda は最後の節で1回だけ（アパートの一室・約40㎡・最大4名・2階で階段約13段・シャワーのみ・駅から平坦な道で徒歩8分・スーパー3分・ペリーロード5分）。料金・週割・泊数の上限は書かず、本文に写真も入れていません ⑥共食いを避けるため、行き方・運賃・フリーきっぷ・2026年の海水浴の期間は書かず、izu-from-tokyo へリンクで送りました。店で食べる金目鯛は kinmedai、1か月以上の部屋は monthly-rental へ ⑦確かめられなかったこと（ロープウェイの運賃・時間、月別の平年値、津波の到達時間、水質の「認証」、サーフィン区域の線引き、バスの系統名・時刻、道の駅全体の営業時間、スーパーの店名、英語のごみ分別表、共同浴場、水族館の営業時間・料金）は書いていません ⑧見出し写真は stony-shore-waves（石の多い浜と青い海。alt に地名なし）",
   "【人に確かめてほしい点】変わりやすい数字（2026年11月に確認）: 日帰り入浴の料金（600〜1,500円）と開く時間、レンタサイクルの料金と時間、観光案内所の時間、漁協の直売所の時間（県のページは2025年4月更新）、行事の日付（黒船祭・あじさい祭・花火は2026年の日付、水仙まつりは毎年12月20日〜1月31日）、2026年度の水質",
   "【エンジニア部へ】組み込みのときに、IZU の keywords から「shimoda japan」を外してこの記事に移し、IZU・izu-from-tokyo・kinmedai からこの記事へのリンクを足す（構成案の依頼）",
  ],
  "points": [
    "浜は、目的で選びます。子ども連れには穏やかな入り江、サーフィンならサーフィンの浜、静かに過ごすなら広い浜です。",
    "旧町内は歩いて回れます。ロープウェイ、港、ペリーロードは、どれも駅から15分以内です。",
    "夏以外は静かで、冬は水仙、5月は黒船祭、6月はあじさいがあります。",
  ],
  "body": """
<h2>下田に1週間いる価値はあるか</h2>
<p>浜を1つ見て駅前を少し歩くだけでは物足りないなら、あると私たちは思います。1泊なら、1回泳いでおいしいものを食べれば終わりです。1週間あれば、いろいろな浜を試し、気に入ったカフェを見つけ、町のゆっくりした調子に体がなじんでいきます。</p>
<p>下田は[[l:ja-izu|伊豆半島]]の南端にある、人口約18,400人（2026年11月）の小さな町です[[s:shimoda_population]]。それでも海岸線は約47kmもあるので[[s:shimoda_profile]]、町の大きさのわりに、歩いてみたい海辺がたくさんあります。</p>
<p>下田は、日本がアメリカに初めて扉を開いた町でもあります。1854年の日米和親条約で、日本で最初に開かれた2つの港の1つになりました[[s:shimoda_hist_perry]]。旧町内を歩いていると、その話にあちこちで出会います。</p>
<p>東京からの電車はそれなりに長いので、着いたら腰を落ち着けたくなるはずです。電車・運賃・バスのきっぷは、[[l:ja-izu-from-tokyo|東京から伊豆への行き方の記事]]にまとめています。1週間より長くいられるなら、私たちならほとんどを下田で過ごし、半島のほかの町に1〜2泊足します。</p>

<h2>下田のどの浜が合うか</h2>
<p>その日に何をしたいかで決まります。下田の9つの海水浴場は、思った以上に性格が違うからです。小さな子どもが水遊びできる穏やかな入り江もあれば、サーフィンで知られる浜もあります。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>浜</th><th>どんな浜か</th><th>向いていること</th><th>伊豆急下田駅から</th></tr></thead>
<tbody>
<tr><td><strong>鍋田浜</strong>（130m）</td><td>町にいちばん近い浜で、入り江のためほとんど波がありません。駐車場とシャワーはありません[[s:shimoda_kanko_beach_nabeta]]。</td><td>ちょっと泳ぐ、小さな子ども</td><td>3番か4番乗り場のバスで約7分、そこから徒歩5分[[s:shimoda_kanko_beach_nabeta]]</td></tr>
<tr><td><strong>外浦</strong>（470m）</td><td>遠浅で波の穏やかな入り江で、家族連れに人気です。沖ではシーカヤックをする人もいます。サーフィンの区域はありません[[s:shimoda_kanko_beach_sotoura]]。</td><td>子ども連れ、穏やかに泳ぐ</td><td>9番乗り場のバスで約10分、そこから徒歩3分[[s:shimoda_kanko_beach_sotoura]]</td></tr>
<tr><td><strong>白浜中央</strong>（720m）</td><td>白浜海岸の北の端の静かな浜で、磯遊びができます。下田で唯一バーベキューができる浜です[[s:shimoda_kanko_beach_shirahamachuo]]。</td><td>家族連れ、磯遊び</td><td>9番乗り場のバスで約18分、そこから徒歩1分[[s:shimoda_kanko_beach_shirahamachuo]]</td></tr>
<tr><td><strong>白浜大浜</strong>（約700m）</td><td>伊豆でも最大級の浜で、国道沿いにあり、サーファーや若い人でにぎわいます[[s:shimoda_beaches_city,shimoda_kanko_beach_shirahama]]。</td><td>にぎやかな1日、サーフィン</td><td>9番乗り場のバスで約15分[[s:shimoda_kanko_beach_shirahama]]</td></tr>
<tr><td><strong>多々戸浜</strong>（450m）</td><td>サーフィンとボディボードで知られ、全国大会も開かれます。一年中使える温水シャワーがあります[[s:shimoda_kanko_beach_tatado]]。</td><td>サーフィン</td><td>3番か4番乗り場のバスで約7分、そこから徒歩3分[[s:shimoda_kanko_beach_tatado]]</td></tr>
<tr><td><strong>吉佐美大浜</strong>（770m）</td><td>国道から離れた大きな浜で、静かに感じます。サーファーと家族連れが一緒に使い、近くにカフェもあります[[s:shimoda_kanko_beach_kisami]]。</td><td>長く、静かに過ごす1日</td><td>3番か4番乗り場のバスで約10分、そこから徒歩8分[[s:shimoda_kanko_beach_kisami]]</td></tr>
</tbody></table></div>
<p class="fine">浜の長さは観光協会の値です（白浜大浜は市の一覧の値）。「乗り場」は、駅前のバス乗り場の番号です。</p>
<p>残りの3つは、こんな浜です。入田浜はソテツの並ぶ落ち着いた浜で、サーファーも使います[[s:shimoda_kanko_beach_irita]]。九十浜は須崎御用邸の隣の50mの入り江で、両側の岩場で磯遊びができ、大きなテントは使えません[[s:shimoda_kanko_beach_kujuppama]]。田牛は混みにくく龍宮窟にも近いのですが、バスは1日4〜5本だけなので[[s:shimoda_kanko_beach_toji]]、時刻表に合わせて1日の予定を組む浜です。</p>
<p>どの浜を選んでも、水はきれいです。静岡県の2026年度の調査で、9つの浜はすべていちばん上の「AA」でした[[s:pref_beach_water_2026]]。そのうち、表の浜から鍋田浜を除いた5つと入田浜の6つは、日本ライフセービング協会の安全の認定も受けています[[s:shimoda_beaches_city]]。</p>
<p>監視員がいるのは、市が毎年決める海水浴の期間だけです[[s:shimoda_ohama]]。2026年の期間は[[l:ja-izu-from-tokyo|伊豆の旅の記事]]に載せています。期間中は、荷物を詰める前に知っておきたい決まりがいくつかあります[[s:shimoda_kanko_umi]]。</p>
<ul>
<li>テントは禁止。日よけのパラソルは使えます。</li>
<li>直火とバーベキューは禁止（白浜中央の一部を除く）。</li>
<li>花火と、泊まりがけのキャンプも禁止。</li>
<li>音を大きくするスピーカーも禁止（2025年から）[[s:shimoda_kanko_umi]]。</li>
</ul>

<h2>下田で、浜のほかに何ができるか</h2>
<p>けっこうたくさんあり、ほとんどが駅から歩いて行けます。浜に行かない日なら、私たちは高い所から始めて、旧町内を歩き、最後に温泉に入ります。</p>
<p>下田ロープウェイの乗り場は、伊豆急下田駅から歩いて1分です。寝姿山の山頂からは、町、港、伊豆諸島、天城の山々が見えます[[s:shimoda_nesugata]]。下りたら、港と道の駅（道路沿いの市場のような建物）までは歩いて約10分です[[s:shimoda_michinoeki]]。</p>
<p>歴史にふれるなら、駅から約15分のペリーロードと了仙寺へ[[s:shimoda_perryroad,shimoda_ryosenji]]。ペリーロードは、ペリーの一行が了仙寺まで行進した道です。いまは小さな川に沿って約500mの石畳が続いていて[[s:shimoda_hist_perry,shimoda_perryroad]]、町でも気持ちのいい散歩道のひとつだと私たちは思います。同じ1854年のうちに、日米和親条約の付録の「下田条約」が了仙寺の本堂で結ばれました[[s:shimoda_hist_perry]]。もう少し足をのばすなら、玉泉寺には、1856年にハリスが開いた日本で最初の米国総領事館が置かれました[[s:shimoda_hist_harris,shimoda_gyokusenji]]。</p>
<p>1日の終わりに温泉に入るなら、日帰り入浴のできるホテル・旅館が8軒あります[[s:shimoda_kanko_onsen]]。大人は600〜1,500円です（2026年11月時点）。開く時間は施設ごとに10時〜15時のあいだで違い、混んでいるときは断られることもあります[[s:shimoda_kanko_onsen]]。足だけ温まりたいなら、駅前の足湯「開国の湯」が9時〜17時に使えます[[s:shimoda_kanko_onsen]]。</p>
<p>雨の日も、楽しみ方はあります。道の駅の4階には町の歴史を伝えるハーバーミュージアムがあり[[s:shimoda_michinoeki]]、了仙寺には宝物館があります[[s:shimoda_ryosenji]]。晴れた日なら、和歌の浦遊歩道で海沿いを1.2km、約15分歩けます[[s:shimoda_kanko_promenade]]。もっと歩きたいなら、下田公園の遊歩道がひと回り約1時間半です[[s:shimoda_kanko_promenade]]。</p>

<h2>夏以外の下田は、行く価値があるか</h2>
<p>あります。浜は静かになりますが、たいていの季節に何かしらの行事があります。気候も穏やかで、市は年の平均気温を約17℃としています[[s:shimoda_profile]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>時期</th><th>行事・見どころ</th></tr></thead>
<tbody>
<tr><td>12月20日〜1月31日</td><td>爪木崎の水仙まつり。最大で約300万本の水仙が咲き、見ごろはたいてい1月です。駅前の10番乗り場から、バスで約20分です[[s:shimoda_kanko_suisen]]。</td></tr>
<tr><td>冬から早春</td><td>下田公園の椿。園芸品種は約160種あります[[s:shimoda_park]]。3月中旬〜4月上旬は桜です[[s:shimoda_kanko_event]]。</td></tr>
<tr><td>5月</td><td>1934年から続く黒船祭。2026年は5月15〜17日で、港の花火、日米のパレード、了仙寺での下田条約の再現がありました[[s:shimoda_kanko_kurofune]]。</td></tr>
<tr><td>6月</td><td>下田公園のあじさい祭。100種以上・約300万輪が咲きます（2026年は6月1〜30日）。公園は坂が多く、歩くのがつらい人のためのカートがあります[[s:shimoda_kanko_ajisai]]。</td></tr>
<tr><td>7月・8月</td><td>海水浴の季節。2026年は7月25日に白浜で花火があり、旧町内の太鼓祭りは8月14・15日です[[s:shimoda_kanko_event]]。</td></tr>
<tr><td>秋</td><td>手筒花火（2026年は10月10日）、10月下旬の白浜神社の例大祭、そして5月上旬まで続く伊勢海老の季節の始まりです[[s:shimoda_kanko_event]]。</td></tr>
</tbody></table></div>
<p>町がいちばんにぎわうのは夏で、私たちの宿でも、夏は長く泊まる人が増えます。泳ぐより、歩いて、温泉に入って、おいしいものを食べたいなら、私たちは涼しい季節を選びます。</p>

<h2>下田で1週間、どう買い物して料理するか</h2>
<p>魚は港で買って、自分で料理するのがおすすめです。キッチンのある宿の楽しみの半分はそこにあります。伊豆漁協の直売所は、道の駅「開国下田みなと」の1階にあります。金目鯛、生きた伊勢海老、サザエなどの魚介がそろいます[[s:pref_izu_gyokyo_shop,shimoda_kanko_gift]]。営業は8時〜16時30分で、定休日はありません（2025年4月時点）[[s:pref_izu_gyokyo_shop]]。同じ建物の JA の直売所には、地元の野菜、わさび、ニューサマーオレンジを使った品があります[[s:shimoda_kanko_gift]]。</p>
<p>町の名物の赤い魚を誰かに料理してもらいたいなら、[[l:ja-kinmedai|金目鯛の記事]]に食べられる所をまとめています。日々の買い物には町なかにスーパーやコンビニがあるので、キッチンがあれば、1週間がずっと安く、気楽になります。</p>
<p>ごみの出し方は、少し慣れが要ります。燃えるごみは週2回、市の指定袋で出します[[s:shimoda_gomi]]。缶・びん・ペットボトル・紙などは、それぞれ分けて月2回の収集です[[s:shimoda_gomi]]。ただ、泊まる所ごとにやり方があるので、着いたときに宿の人に聞くのがいちばん簡単です。ほかに初日、私たちならこんなことをします。</p>
<ol>
<li>いちばん近いスーパーと、道の駅の魚の直売所の場所を確かめる。</li>
<li>ごみの分け方と出す場所を、宿の人に聞く。</li>
<li>駅の近くの観光案内所（9時〜16時45分）で地図をもらう[[s:shimoda_kanko_about]]。</li>
<li>行きたい浜のバスの時刻を調べる。1日に数本しかない路線もあります。</li>
<li>泊まる所から、いちばん近い高い場所を確かめる（次の節）。</li>
</ol>

<h2>下田の津波について、何を知っておくべきか</h2>
<p>海の近くで強い揺れを感じたら、警報を待たずに、すぐ高い所へ逃げてください[[s:jma_tsunami_warnings]]。下田は外洋に面していて、1854年には安政の大津波が下田湾を襲い、町の家のほとんどが流されたり壊れたりしました[[s:shimoda_hist_ansei]]。</p>
<p>静岡県の2013年の想定では、発生する頻度は極めて低いものの、最悪の場合の下田の最大の津波の高さを33mとしています[[s:shimoda_news_2013_08]]。予報ではありませんが、「とにかく早く高い所へ」と言われるのはそのためです。気象庁は、地震からおよそ3分で津波の警報・注意報を出すことを目指しています[[s:jma_tsunami_warnings]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>発表</th><th>予想される高さ</th><th>すること</th></tr></thead>
<tbody>
<tr><td><strong>津波注意報</strong></td><td>0.2〜1m</td><td>海から上がり、海岸から離れる[[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>津波警報</strong></td><td>1〜3m</td><td>すぐに高台か避難ビルへ[[s:jma_tsunami_warnings]]</td></tr>
<tr><td><strong>大津波警報</strong></td><td>3mを超える</td><td>すぐに高台か避難ビルへ[[s:jma_tsunami_warnings]]</td></tr>
</tbody></table></div>
<p>津波は何度も来るので、気象庁は、警報・注意報が解除されるまで高い所にとどまるよう呼びかけています[[s:jma_tsunami_warnings]]。市は津波ハザードマップと避難の地図を出していますが、日本語だけです[[s:shimoda_tsunami_map]]。津波避難ビルもいくつか指定していて[[s:shimoda_tsunami_bldg]]、地図で場所をタップすると海抜が分かる、オンラインの地図もあります[[s:shimoda_elevation_map]]。</p>
<p>観光庁の無料のアプリ「Safety tips」は、地震・津波・気象の警報を英語などで知らせてくれます[[s:jta_safety_tips]]。着く前に入れておくのがおすすめです。2025年7月末には、静岡県の沿岸に津波警報が出て、のちに津波注意報に切り替わりました[[s:jma_kamchatka_2025,jma_kamchatka_2025_eve]]。私たちは海外からのゲストに、状況が変わるたびにメッセージを送り、何が起きているかと、避難が必要なことを伝えました。ゲストからは、あとで感謝の言葉をもらいました。</p>

<h2>下田で1週間、どこに泊まるか</h2>
<p>車がないなら、私たちは駅に近い旧町内に泊まります。店も港も、どのバスの路線もすぐ近くです。浜が旅のいちばんの目的なら、浜の近くに泊まればバスに乗らずに済みます。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>地区</th><th>こんな人に合う</th><th>知っておきたいこと</th></tr></thead>
<tbody>
<tr><td><strong>旧町内（駅の周り）</strong></td><td>店・港・ペリーロードに歩いて行き、浜へはバスで行きたい人。</td><td>たいていの浜へは、バスか自転車が要ります。</td></tr>
<tr><td><strong>白浜</strong></td><td>大きな浜をすぐ目の前にしたい人。</td><td>町からバスで約15分なので[[s:shimoda_kanko_beach_shirahama]]、夜に町へ出ると帰りもバスです。</td></tr>
<tr><td><strong>南の浜</strong>（多々戸・入田・吉佐美）</td><td>サーフィンが目的の人、静かな浜がいい人。</td><td>駅からバスで7〜10分[[s:shimoda_kanko_beach_tatado,shimoda_kanko_beach_kisami]]、そこから少し歩きます。</td></tr>
</tbody></table></div>
<p>どこに泊まっても、自転車があると1週間がぐっと楽になります。観光協会が道の駅で、自転車と電動自転車を1時間500円から、1日2,000円で貸しています[[s:shimoda_kanko_bicycle]]。時間は9時〜17時です。予約は要りませんが、パスポートなどの身分証が要ります[[s:shimoda_kanko_bicycle]]。</p>
<p>私たちは、旧町内で「<a href="https://nodeshimoda.com/" rel="noopener">NODE Shimoda</a>」を運営しています。約40㎡のアパートの一室で、最大4名まで泊まれます。キッチン、洗濯機とガス乾燥機、ワークデスクがあります。2階で階段は約13段、浴室はシャワーだけで浴槽はありません[[s:node_room]]。駅から平坦な道を歩いて8分です[[s:node_access]]。スーパーまでは3分、ペリーロードまでは5分です。1月に泊まったゲストは、海が近く、初日の出も見られ、スーパーも近くて便利だったとレビューに書いてくれました。</p>
<p>1週間が、1か月以上いたい気持ちに変わったら、[[l:ja-monthly-rental|日本で1か月単位で部屋を借りる記事]]に仕組みをまとめています。</p>
""",
  "faq": [
    ("下田は行く価値がありますか",
     "あります。特に1週間いるなら。伊豆の南端の小さな港町で、9つの海水浴場、歩いて回れる旧町内、季節の行事があります[[s:shimoda_population,shimoda_kanko_umi,shimoda_kanko_event]]。1週間あれば、いくつもの浜を試し、町の調子で暮らせます。"),
    ("下田でいちばんいい浜はどこですか",
     "何をしたいかによります。外浦と鍋田浜は穏やかな入り江で、子ども連れに合います[[s:shimoda_kanko_beach_sotoura,shimoda_kanko_beach_nabeta]]。多々戸浜はサーファーの間で特に有名で[[s:shimoda_kanko_beach_tatado]]、吉佐美大浜は大きくて静かめです[[s:shimoda_kanko_beach_kisami]]。"),
    ("夏以外でも、下田で泳げますか",
     "監視員がいるのは市が毎年決める海水浴の期間だけなので、期間外は監視員なしで泳ぐことになります[[s:shimoda_ohama]]。多々戸浜には一年中使える温水シャワーがあります[[s:shimoda_kanko_beach_tatado]]。"),
    ("冬の下田では、何ができますか",
     "爪木崎の水仙まつりが12月20日〜1月31日にあり[[s:shimoda_kanko_suisen]]、下田公園では椿が咲きます[[s:shimoda_park]]。日帰り温泉、ロープウェイ、海沿いの散歩で、1週間はすぐに埋まります[[s:shimoda_kanko_onsen,shimoda_nesugata,shimoda_kanko_promenade]]。"),
    ("下田で津波警報が出たら、どうすればいいですか",
     "すぐに高台か避難ビルへ移り、警報が解除されるまでとどまります。海の近くで強い揺れを感じたら、警報を待たずに逃げます[[s:jma_tsunami_warnings]]。無料のアプリ「Safety tips」が英語で知らせてくれます[[s:jta_safety_tips]]。"),
  ],
 },
},
# ============================================================ 日本に何日いられるか
{
 "id": "how-long-stay", "slug": "how-long-can-you-stay-in-japan", "topic": "live", "place": None, "also": ["stay"],
 "photo": ("passport-stamps", "An open passport with colourful entry and exit stamps on its pages", ""),
 "published": "2026-11-20", "updated": "2026-11-20",
 "kicker": "Live part-time",
 "h1": "How long can you stay in Japan? 90 days, and the ways to stay longer",
 "seo_title": "How Long Can I Stay in Japan? 90 Days and Longer Stays",
 "description": "Most visa-free visitors can stay in Japan for up to 90 days, and extensions need good reason. For six months or a year, pick the right status before you come.",
 "dek": "Most visa-free visitors get up to 90 days, though some nationalities may get less, or 180. For six months or a year, you’ll want the right status first.",
 "card": "Visa-free visitors usually get up to 90 days, though JNTO notes some nationalities may be granted 15, 30 or 180. Extensions need good reason and every entry is checked again, so for six months or a year it’s better to choose the right status before you travel.",
 "keywords": [("how long can i stay in japan", "170", "3"), ("how long can you stay in japan", "—", "—"),
              ("japan visa free stay / japan 90 day rule", "—", "—"), ("extend stay in japan / stay in japan for 6 months", "—", "—")],
 "intent": "Know（自分は何日いられるか）→ Do（もっと長くいるには何を選ぶか）",
 "points": [
   "Most visa-free stays last up to 90 days, though some nationalities may get less, or up to 180.",
   "Extensions need good reason, and every time you come back, you’re checked again at the border.",
   "For six months or a year, we’d look at the digital nomad status or the long stay for sightseeing.",
 ],
 "body": """
<p>Ask online how long you can stay in Japan and you’ll get answers from 90 days to a year, sometimes in the same thread. The real answer depends on two things: the passport you hold and the status you enter on. Everything below describes the rules as of November 2026.</p>

<h2>How long can you stay in Japan without a visa?</h2>
<p>Usually up to 90 days. Officially you come in as a Temporary Visitor [[s:egov_immig_act]], and for most people that means up to 90 days [[s:jnto_visa]]. Some nationalities may be granted a shorter stay of 15 or 30 days. Others may get as long as 180 [[s:jnto_visa]].</p>
<p>Which one you get comes down to your passport. The Ministry of Foreign Affairs keeps the list of visa-exempt countries and regions, and that’s the one to trust for your own case [[s:jnto_visa]]. If your passport isn’t on it, you’ll need a visa before you travel.</p>
<p>The status is built for short stays like a holiday, sport, visiting family, or business meetings [[s:egov_immig_act]]. It doesn’t cover paid work, long-term study or applying to live here [[s:jnto_visa]]. So it suits a holiday or a family visit, but it isn’t a way to move here.</p>

<h2>Can you extend a visa-free stay?</h2>
<p>You can apply, but we wouldn’t plan a trip around it: an extension is only granted when there are reasonable grounds [[s:egov_immig_act]].</p>
<p>Timing matters if your plans fall apart near the end. Say you apply before your period of stay ends and there’s no decision yet. You can then stay until the decision or two months after your old expiry date, whichever comes first [[s:egov_immig_act]]. That grace period doesn’t apply if you were given 30 days or less [[s:egov_immig_act]]. So if you think you’ll go over, it’s worth talking to the immigration authorities before the date, not after.</p>
<p>Switching to another status from inside Japan is just as narrow. For a short-term visitor, the Act only allows a change of status when there are unavoidable special circumstances [[s:egov_immig_act]]. That’s why we’d sort out any longer status before you fly.</p>

<h2>Can you leave Japan and come back for another 90 days?</h2>
<p>You can come back, but a new entry isn’t a fresh 90 days by right. Each time you land, an immigration inspector checks that your passport is valid and that what you plan to do here is genuine and fits your status. They also check that the period fits the rules [[s:egov_immig_act]]. It’s up to you to show that you meet those conditions [[s:egov_immig_act]].</p>
<p>People often ask how many days they need to spend abroad before coming back, or whether there’s a limit per year. What the law sets out is the check itself. Each time, the inspector decides whether you meet the entry conditions, such as whether the purpose of your trip is genuine [[s:egov_immig_act]]. We don’t know of a number of days that makes the next entry safe, so we wouldn’t build a plan on leaving and coming back again and again.</p>
<p>In our view, the better plan for anything beyond 90 days is to pick a status that fits the length of your stay, before you come.</p>

<h2>Which status fits six months or a year?</h2>
<p>If you aren’t taking a job here, there are two main routes past 90 days. One is the digital nomad status, for up to six months. The other is a long stay for sightseeing and recreation, for up to a year.</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>Status</th><th>How long</th><th>Who it’s for</th><th>Residence card</th></tr></thead>
<tbody>
<tr><td><strong>Temporary Visitor</strong>, visa-exempt</td><td>Usually up to 90 days. Some nationalities may get 15 or 30. Others may get 180 [[s:jnto_visa]]</td><td>Short stays such as sightseeing. No paid work [[s:egov_immig_act,jnto_visa]]</td><td>No [[s:egov_immig_act]]</td></tr>
<tr><td><strong>Digital nomad</strong> (Designated Activities)</td><td>Up to six months, with no extension [[s:isa_nomad_en]]</td><td>Remote workers with an employer or clients outside Japan who meet the income and insurance rules [[s:isa_nomad_en]]</td><td>No [[s:egov_immig_act,egov_immig_rules]]</td></tr>
<tr><td><strong>Long stay for sightseeing and recreation</strong> (Designated Activities)</td><td>A stay of up to one year [[s:egov_nhi_rules]]</td><td>People aged 18 or over staying for sightseeing and recreation, and a spouse who comes with them [[s:egov_nhi_rules]]</td><td>Yes, if you’re given more than three months [[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>
<p>Study, work and family statuses work differently. For those, you apply for a pre-approval document from Japan’s immigration authorities before you travel (officially a Certificate of Eligibility), and someone at the school or company taking you on can apply on your behalf [[s:egov_immig_act]].</p>
<p>The digital nomad status suits people who want to keep working for an employer or clients abroad. It needs ¥10 million a year in income [[s:isa_nomad_en]], and our [[l:digital-nomad|guide to Japan’s digital nomad visa]] covers who qualifies and what it’s like to live here without a residence card.</p>
<p>The long stay for sightseeing is less well known. It does come with a residence card for stays of more than three months, but it still doesn’t let you join National Health Insurance [[s:egov_immig_act,egov_immig_rules,egov_nhi_rules]], so you’ll want private health cover. Its other conditions, such as which passports qualify and what you need to show, are best checked with a Japanese embassy or consulate in your country.</p>
<p>For many people, though, 90 days is plenty for a first season. It’s enough to [[l:akiya-try-first|live in a town for a month or two before you buy a house]]. Our guide to [[l:monthly-rental|renting a place by the month]] covers where you’d stay.</p>

<h2>Can you work remotely while visiting Japan?</h2>
<p>The law says a short-term visitor can’t run a business that brings in income or do activities they’re paid for without permission [[s:egov_immig_act]]. JNTO also says a tourist stay doesn’t allow paid work [[s:jnto_visa]]. So we wouldn’t assume it’s fine just because the money comes from abroad. How the rule applies to your own job is a question for the immigration authorities.</p>
<p>Whether answering a few emails for your employer counts depends on what you actually do, and we won’t guess at it for you. What’s clear is that Japan has a status built for remote work. If you want to keep working for an employer or clients abroad while you stay longer, the digital nomad status is the one written for that [[s:egov_immig_rules,isa_nomad_en]].</p>

<h2>What happens if you overstay?</h2>
<p>It’s serious, and it can keep you out of Japan for years. If you stay past your permitted date without extending or changing your status, you can be deported [[s:egov_immig_act]]. It’s also a crime, with up to three years’ imprisonment, a fine of up to ¥3 million, or both [[s:egov_immig_act]].</p>
<p>How long you’re kept out depends on how you leave. Here’s how the Act sets it out, in the version in force from 1 October 2026 [[s:egov_immig_act]].</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>How you leave</th><th>How long you can’t come back</th></tr></thead>
<tbody>
<tr><td>Deported for the first time</td><td>Five years from your departure [[s:egov_immig_act]]</td></tr>
<tr><td>Deported after an earlier deportation or departure order</td><td>Ten years [[s:egov_immig_act]]</td></tr>
<tr><td>Under a departure order</td><td>One year. It’s five years if you only said you’d leave after an investigation began and you want to come back as a visitor [[s:egov_immig_act]]</td></tr>
</tbody></table></div>
<p>A departure order is the gentler route, and it’s mostly in your hands. You may get one if you go to an immigration office yourself, intending to leave quickly. You also need a clean record: no past deportation or departure order, no listed criminal convictions, and you need to be able to leave promptly [[s:egov_immig_act]]. If you realise you’ve gone over, going in early is far better than waiting.</p>

<h2>Is anything changing for visa-free visitors?</h2>
<p>Yes, but not for a while. Japan has changed the law so that visa-exempt short-term visitors will give their details online before they travel. The Immigration Services Agency then authorises them [[s:egov_immig_act_jesta]].</p>
<p>The law passed in May 2026 [[s:shugiin_bill221_20]], but the part that affects you isn’t in force yet. The plan is to launch it, as JESTA, sometime between April 2028 and March 2029 [[s:jta_jesta]], and the law says it has to start by 31 March 2029 [[s:egov_immig_act_jesta]]. Until it does, nothing changes when you travel.</p>
<p>All of this is general information as of November 2026, not immigration advice. For your own case, it’s best to check with a Japanese embassy or consulate, the Immigration Services Agency, or an administrative scrivener (<em>gyoseishoshi</em>) who handles visas.</p>
""",
 "after_faq": '<p class="fine">This article is general information, not legal or immigration advice.</p>',
 "faq": [
   ("How long can I stay in Japan without a visa?",
    "Usually up to 90 days. Some nationalities may be granted a shorter stay of 15 or 30 days. Others may get 180 [[s:jnto_visa]]. The Ministry of Foreign Affairs list is the place to check yours [[s:jnto_visa]]."),
   ("Can I extend my 90-day stay in Japan?",
    "You can apply, but it’s only granted when there are reasonable grounds [[s:egov_immig_act]]. If you might go over, talk to the immigration authorities before your stay ends, not after."),
   ("Can I leave Japan and come back for another 90 days?",
    "You can come back, but each entry is checked again. The immigration inspector decides whether you meet the entry conditions, such as whether your plans are genuine and fit your status, and it’s up to you to show that [[s:egov_immig_act]]. We don’t know of a number of days abroad, or a yearly pattern, that makes the next entry safe, so we wouldn’t plan on going in and out."),
   ("Can I stay in Japan for six months or a year without a job?",
    "There are two main routes. One is the digital nomad status, for up to six months with no extension [[s:isa_nomad_en]]. The other is a long stay for sightseeing and recreation of up to a year, for people aged 18 or over [[s:egov_nhi_rules]]. A Japanese embassy or consulate can tell you whether you qualify."),
   ("Can I work remotely on a visa-free stay in Japan?",
    "A short-term visitor can’t do activities they’re paid for without permission [[s:egov_immig_act,jnto_visa]]. How that applies to your own job is a question for the immigration authorities. If you want to keep working for an employer or clients abroad for longer, the digital nomad status is built for that [[s:isa_nomad_en]]."),
   ("What happens if I overstay in Japan?",
    "Overstaying can get you deported, and it’s also a crime [[s:egov_immig_act]]. A first deportation keeps you out for five years, while leaving under a departure order usually means one year [[s:egov_immig_act]]."),
 ],
 "sources": ["jnto_visa", "egov_immig_act", "egov_immig_rules", "egov_nhi_rules", "isa_nomad_en", "shugiin_bill221_20", "egov_immig_act_jesta", "jta_jesta"],
 "related": ["digital-nomad", "monthly-rental", "akiya-try-first"],
 "ja": {
  "h1": "日本に何日いられる？ 90日と、もっと長くいる方法",
  "dek": "ビザなしで来る人の多くは、最長90日いられます。パスポートによってはそれより短いことも、180日まで認められることもあります。半年や1年いたいなら、先に合った在留資格を用意しておきたいところです。",
  "review": [
   "2026-11-21 ネイティブ感の仕上げ（playbook 3-1 の6 の後半）: お役所言葉を普通の言葉に: 在留資格認定証明書は「来る前に入管に申請する事前の証明書（正式名）」、延長は「相当の理由があるときだけ認められる」、退去強制は「退去させられることがある」。第7条などの条文番号を本文から外し、JESTA の段落の数字を2文にまとめました。事実・数値・出典は変えていません。",
   "2026-11-20 見せ方のリライト: ガイドブックのような固さを減らすため、数字を詰めた文（日数の「15・30・180日」、JESTA の成立・公布・開始時期・施行期限）を2〜3文に分けました。JESTA の節は、仕組みの段落と「法律は成立したがまだ施行されていない、2028年度に始まる予定」の段落の2つにまとめ、公布の月と法律番号は本文から外しました（出典の注に残っています）。dek・In short は「短いことも、180日までのことも」とまとめ、細かい日数は本文・表・FAQ に残しています。「JNTO によると」などの出典の前置きを本文から減らし（出典の番号はそのまま）、短期滞在の節に「休暇や家族の訪問には合うが、移り住むためのものではない」という読み手にとっての意味を1文足しました。事実・数値・出典・リンクは変えていません（品質保証部の指摘で、短期滞在の根拠に入管法の出典を足し、dek の「may」を戻しました）。",
   "【2026-11-20 品質保証部の1回目（86点・ゲート違反3）を受けた直し（執筆部）】変えた点: ①【事実の変更】留学・仕事・家族の在留資格の1文: 「来る前に大使館・総領事館で手続き」をやめ、入管法 第7条の2（現行。e-Gov で条文を確認）どおり「法務大臣に在留資格認定証明書を前もって申請でき、受け入れる学校や会社の人が代わりに申請できる」にしました ②【事実の変更】短期滞在の日数: JNTO の言い方にそろえ、「たいてい最長90日。国籍によっては15日・30日・180日が認められることもある」にしました（dek・In short・本文・表・FAQ1。akiya-try-first・monthly-rental と同じ）。施行規則の「90日・30日・15日以内」は本文から外しました。表の列名は「期間（How long）」です ③ja 本文の「ソウルへ短い旅」の文を消しました（英語版の「a short trip abroad」の文も、下の④の形に置き換えました） ④出て戻る節: 「1年に上限はあるか」に、「法律が定めているのは審査そのもので、入国のたびに審査官が第7条の上陸の条件（滞在の目的が本当か など）で判断する」までを出典つきで書き、出入りをくり返す前提の計画はすすめない形にしました。「上限はない」とは書いていません。FAQ3 も同じ形にしました ⑤年収1,000万円に出典（isa_nomad_en）を付けました ⑥リモートワーク: 「日本で報酬を受ける仕事はできない」をやめ、法律の言い方（許可なしに報酬を受ける活動はできない）で始め、「お金が海外から払われるから大丈夫、とは考えないほうがいい」を足しました ⑦節3の「In our view」を1回にしました",
   "【2026-11-20 新規の下書き（執筆部）】書いた点: 1記事1主張は「何日いられるかはパスポートと在留資格で決まる。90日を超えたいなら、出入国をくり返すより、来る前に合った在留資格を選ぶ」。h2 は7つで、すべて疑問形です。制度の事実は、開いて確かめた条文（e-Gov の入管法・施行規則は2026年10月1日施行の版、国保法施行規則）、JNTO、衆議院の議案審議経過、観光庁の資料によります。延長は「相当の理由があるときに限り許可」（第21条）と、申請中の2か月の猶予（第20条第6項。30日以下の人は除く）、日本の中での変更は「やむを得ない特別の事情」があるときだけ（第20条第3項）。地図の表は3行（短期滞在／デジタルノマド／観光・保養の長期滞在）で、長期滞在は「最長1年・18歳以上・同行する配偶者・3か月を超えれば在留カード・国民健康保険に入れない」だけを書き、ほかの条件は大使館・総領事館へ。オーバーステイは罰則と上陸拒否の期間の表（2026年10月1日施行の版）と出国命令の条件。JESTA は成立・公布・観光庁の予定（2028年度）・施行の期限（2029年3月31日までの政令で定める日）・2026年11月時点で未施行まで。NODE Shimoda と自社の体験には触れていません",
   "【人に確かめてほしい点】①ビザ・在留・JESTA の記述すべて（playbook 6章。2026年11月時点）。特に、観光・保養の長期滞在に「3か月を超えて決まれば在留カードが出る」と書いた点は、入管法 第19条の3・施行規則 第19条の5 の条文の読みによります",
   "【書かなかったこと（公式の出典を開けないため）】ワーキングホリデー、取り決めで最長6か月まで延長できる国、「1年に180日」、短期滞在の更新が認められる例（病気など）、観光・保養の長期滞在の預貯金・対象国・保険・最初の期間と更新・申請先、査証免除の国・地域の数、短期滞在中のリモートワークの公式の扱い",
   "【写真】編集長が入れた passport-stamps（スタンプの押されたパスポート）をそのまま使っています",
   "【エンジニア部へ】①SOURCES_NEW の egov_immig_act・egov_immig_rules は既存のキーの上書きです。egov_immig_act は正式名に条番号（第7条の2 など）を足しただけ、egov_immig_rules は既存と同じ中身です（URL・短い名前は同じ。既存記事の表示に問題なし） ②akiya-try-first の h2「How long can you stay in Japan to test a town?」の言い換えとこの記事へのリンク、monthly-rental・digital-nomad からこの記事へのリンクを、この記事の公開と同じ PR で",
  ],
  "points": [
    "ビザなしの滞在は、多くの人が最長90日です。国籍によっては、それより短いことも、180日までのこともあります。",
    "延長には相当の理由が要ります。また、出て戻るたびに、入国のときにあらためて審査されます。",
    "半年や1年なら、デジタルノマドの在留資格か、観光・保養の長期滞在を考えるのがいいと思います。",
  ],
  "body": """
<p>日本に何日いられるかをネットで調べると、90日から1年まで、同じスレッドの中でさえ答えがばらばらです。本当の答えは、持っているパスポートと、何の在留資格で入るかの2つで決まります。以下はすべて2026年11月時点の決まりです。</p>

<h2>ビザなしで、日本に何日いられるのか</h2>
<p>たいてい最長90日です。正式には「短期滞在」の在留資格で入り[[s:egov_immig_act]]、多くの人は最長90日です[[s:jnto_visa]]。国籍によっては、15日や30日と短めのこともあります。逆に、180日まで認められることもあります[[s:jnto_visa]]。</p>
<p>どれになるかは、パスポートで決まります。外務省が査証免除の国・地域の一覧を出していて、自分の場合はその一覧がいちばん確かです[[s:jnto_visa]]。パスポートが一覧にないなら、出発の前にビザが要ります。</p>
<p>この在留資格は、観光や保養、スポーツ、親族の訪問、会議や業務連絡といった短い滞在のためのものです[[s:egov_immig_act]]。報酬を受ける仕事、長い期間の勉強、日本に住むための申請はできません[[s:jnto_visa]]。休暇や家族に会いに来るのには合いますが、移り住むためのものではありません。</p>

<h2>ビザなしの滞在は延長できるのか</h2>
<p>申請はできますが、延長をあてにして旅の計画を立てるのはおすすめしません。延長が認められるのは、相当の理由があるときだけです[[s:egov_immig_act]]。</p>
<p>終わり近くで予定が崩れたときは、タイミングが大事です。在留期間が終わる前に申請して、まだ決定が出ていなければ、決定の日か、元の期限から2か月のどちらか早い日まではいられます[[s:egov_immig_act]]。ただし、もらった期間が30日以下なら、この猶予はありません[[s:egov_immig_act]]。過ぎてしまいそうなら、期限の後ではなく前に、入管に相談するのがいいと思います。</p>
<p>日本の中で別の在留資格に切り替えるのも、同じくらい狭き門です。入管法では、短期滞在の人が在留資格を変えられるのは、やむを得ない特別の事情があるときだけです[[s:egov_immig_act]]。だから、長くいるための在留資格は、飛行機に乗る前に済ませておくのがいいと私たちは考えています。</p>

<h2>一度出国して戻れば、また90日いられるのか</h2>
<p>戻ってくることはできますが、入国すれば当然にまた90日もらえるわけではありません。入国のたびに、入国審査官が、パスポートが有効か、日本でする予定のことが本当で在留資格に当たるか、期間が決まりに合っているかを確かめます[[s:egov_immig_act]]。条件を満たしていることは、自分で示す必要があります[[s:egov_immig_act]]。</p>
<p>何日、日本の外にいればまた入れるのか、1年に上限はあるのか、とよく聞かれます。法律が定めているのは、審査そのものです。入国のたびに、審査官が入国の条件、たとえば滞在の目的が本当かどうかで判断します[[s:egov_immig_act]]。次の入国が安全になる日数を私たちは知らないので、出入りをくり返す前提で計画を立てることはおすすめしません。</p>
<p>90日を超えて過ごしたいなら、来る前に、滞在の長さに合った在留資格を選ぶほうがいい、と私たちは考えています。</p>

<h2>半年や1年なら、どの在留資格が合うのか</h2>
<p>日本で仕事に就くのでなければ、90日を超える道は主に2つです。1つは最長6か月のデジタルノマドの在留資格、もう1つは最長1年の観光・保養の長期滞在です。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>在留資格</th><th>期間</th><th>対象</th><th>在留カード</th></tr></thead>
<tbody>
<tr><td><strong>短期滞在</strong>（査証免除）</td><td>たいてい最長90日。国籍によっては15日や30日。180日のことも[[s:jnto_visa]]</td><td>観光などの短い滞在。報酬を受ける仕事はできない[[s:egov_immig_act,jnto_visa]]</td><td>出ない[[s:egov_immig_act]]</td></tr>
<tr><td><strong>デジタルノマド</strong>（特定活動）</td><td>最長6か月。延長なし[[s:isa_nomad_en]]</td><td>日本の外の雇用主や取引先のために働くリモートワーカーで、収入と保険の条件を満たす人[[s:isa_nomad_en]]</td><td>出ない[[s:egov_immig_act,egov_immig_rules]]</td></tr>
<tr><td><strong>観光・保養の長期滞在</strong>（特定活動）</td><td>最長1年の滞在[[s:egov_nhi_rules]]</td><td>観光・保養のために滞在する18歳以上の人と、同行する配偶者[[s:egov_nhi_rules]]</td><td>3か月を超えて決まれば出る[[s:egov_immig_act,egov_immig_rules]]</td></tr>
</tbody></table></div>
<p>留学・仕事・家族のための在留資格は、仕組みが違います。これらは、来る前に入管に在留資格認定証明書を申請でき、受け入れる学校や会社の人が代わりに申請することもできます[[s:egov_immig_act]]。</p>
<p>デジタルノマドの在留資格は、海外の雇用主や取引先の仕事を続けたい人に向いています。年収1,000万円以上が必要で[[s:isa_nomad_en]]、対象になる人や、在留カードなしで暮らすとどうなるかは、[[l:ja-digital-nomad|日本のデジタルノマドビザの記事]]にまとめています。</p>
<p>観光・保養の長期滞在は、あまり知られていません。3か月を超える滞在なら在留カードが出ますが、それでも国民健康保険には入れないので[[s:egov_immig_act,egov_immig_rules,egov_nhi_rules]]、民間の医療保険があると安心です。どのパスポートが対象か、何を示す必要があるかといった、ほかの条件は、計画を立てる前に自分の国の日本大使館・総領事館で確かめるのがいいと思います。</p>
<p>とはいえ、最初のひと季節なら、90日で十分という人も多いはずです。[[l:ja-akiya-try-first|家を買う前に1〜2か月その町で暮らしてみる]]には足りますし、どこに泊まるかは[[l:ja-monthly-rental|月単位で部屋を借りる記事]]にまとめています。</p>

<h2>旅行中に、リモートで仕事をしてもいいのか</h2>
<p>法律では、短期滞在の人は、許可なしに収入を伴う事業を営んだり、報酬を受ける活動をしたりできません[[s:egov_immig_act]]。JNTO も、観光の滞在では報酬を受ける仕事はできないとしています[[s:jnto_visa]]。なので、お金が海外から払われるから大丈夫、とは考えないほうがいいと思います。自分の仕事にどう当たるかは、入管に聞くべきことです。</p>
<p>雇い主からのメールに少し返事をするのがそれに当たるかは、実際に何をするかによるので、私たちが代わりに判断することはしません。はっきりしているのは、日本にはリモートワークのための在留資格があることです。海外の雇用主や取引先の仕事を続けながら長くいたいなら、そのために作られたのがデジタルノマドの在留資格です[[s:egov_immig_rules,isa_nomad_en]]。</p>

<h2>オーバーステイすると、どうなるのか</h2>
<p>重い違反で、何年も日本に入れなくなることがあります。更新や変更をせずに在留期間を過ぎると、退去強制の理由になります[[s:egov_immig_act]]。犯罪でもあり、3年以下の拘禁刑か300万円以下の罰金、またはその両方が科されることがあります[[s:egov_immig_act]]。</p>
<p>どれくらい入れなくなるかは、どう出国するかで変わります。2026年10月1日から施行されている入管法では、次のとおりです[[s:egov_immig_act]]。</p>
<div class="tablewrap"><table class="free">
<thead><tr><th>どう出国するか</th><th>再び入国できない期間</th></tr></thead>
<tbody>
<tr><td>初めての退去強制</td><td>出国から5年[[s:egov_immig_act]]</td></tr>
<tr><td>過去に退去強制か出国命令を受けたことがある人の退去強制</td><td>10年[[s:egov_immig_act]]</td></tr>
<tr><td>出国命令</td><td>1年。調査が始まってから出国の意思を示し、短期滞在で戻りたい場合は5年[[s:egov_immig_act]]</td></tr>
</tbody></table></div>
<p>出国命令のほうが軽く済み、それを選べるかはおおむね自分の動き方しだいです。すみやかに出国するつもりで自分から入管に出向き、過去に退去強制や出国命令を受けたことがなく、決められた罪で刑を受けたことがなく、すぐに出国できるなら、出国命令を受けられることがあります[[s:egov_immig_act]]。期限を過ぎたと気づいたら、待つより早く出向くほうがずっといいです。</p>

<h2>ビザなしで来る人の手続きは、これから変わるのか</h2>
<p>変わりますが、もう少し先の話です。ビザなしで短期滞在に来る人が、出発の前にオンラインで情報を出すように法律が変わりました。それを出入国在留管理庁が認証する仕組みです[[s:egov_immig_act_jesta]]。</p>
<p>法律は2026年5月に成立しましたが[[s:shugiin_bill221_20]]、旅行者に関わる部分はまだ施行されていません。観光庁は JESTA という名前で、2028年4月〜2029年3月のどこかで始める予定で[[s:jta_jesta]]、法律では遅くとも2029年3月31日までに始まります[[s:egov_immig_act_jesta]]。それまでは、いまの手続きのままです。</p>
<p>ここに書いたのは、2026年11月時点の一般的な情報で、在留手続きの助言ではありません。自分の場合については、日本の大使館・総領事館、出入国在留管理庁、またはビザを扱う行政書士に確かめてください。</p>
""",
  "after_faq": '<p class="fine">この記事は一般的な情報で、法律や在留手続きの助言ではありません。</p>',
  "faq": [
    ("ビザなしで、日本に何日いられますか？",
     "たいてい最長90日です。国籍によっては、15日や30日と短めのことがあります。180日まで認められることもあります[[s:jnto_visa]]。自分の場合は、外務省の一覧で確かめるのが確かです[[s:jnto_visa]]。"),
    ("90日の滞在は延長できますか？",
     "申請はできますが、許可されるのは相当の理由があるときに限られます[[s:egov_immig_act]]。過ぎてしまいそうなら、期限の後ではなく前に入管に相談してください。"),
    ("一度出国して戻れば、また90日いられますか？",
     "戻ることはできますが、入国のたびにあらためて審査されます。審査官は、予定が本当で在留資格に当たるかといった上陸の条件で判断し、それを示すのは自分です[[s:egov_immig_act]]。次の入国が安全になる、日本の外にいる日数や1年の過ごし方を私たちは知らないので、出入りをくり返す前提の計画はおすすめしません。"),
    ("仕事をせずに、半年や1年日本にいられますか？",
     "主な道は2つで、最長6か月・延長なしのデジタルノマドの在留資格[[s:isa_nomad_en]]と、18歳以上の人のための最長1年の観光・保養の長期滞在です[[s:egov_nhi_rules]]。対象になるかは、日本の大使館・総領事館で確かめられます。"),
    ("ビザなしの滞在中に、リモートで仕事をしてもいいですか？",
     "短期滞在の人は、許可なしに報酬を受ける活動はできません[[s:egov_immig_act,jnto_visa]]。それが自分の仕事にどう当たるかは、入管に聞くべきことです。海外の雇用主や取引先の仕事を続けながら長くいたいなら、そのための在留資格がデジタルノマドです[[s:isa_nomad_en]]。"),
    ("日本でオーバーステイすると、どうなりますか？",
     "退去強制の理由になり、犯罪にもなります[[s:egov_immig_act]]。初めての退去強制では5年、出国命令で出た場合はふつう1年、日本に入れなくなります[[s:egov_immig_act]]。"),
  ],
 },
},
]

# ---------------------------------------------------------------- 固定ページの文言
HOME = {
 "seo_title": "Noki | Slow Travel, Part-Time Life and Akiya in Japan",
 "description": "Plain guides to longer trips, living part of the year and buying an akiya in small-town Japan, from the people who run a place to stay in Shimoda.",
}
GUIDES = {
 "h1": "Guides to long stays and akiya in Japan",
 "seo_title": "Guides to Long Stays and Akiya in Japan",
 "description": "Guides for people who want more than a quick holiday in Japan: longer trips, remote work, monthly rentals, akiya and old houses, and the small towns we know.",
 "dek": "For people who want more than a quick holiday in Japan: longer trips, living here part of the year and old houses."
}
IZU = {
 "h1": "Izu Peninsula",
 "seo_title": "Izu Peninsula Guide: Towns, Access and Long Stays",
 "description": "The Izu Peninsula is a mountainous peninsula south-west of Tokyo with beaches on the coast and onsen towns inland. Where to base yourself and how to get there.",
 "dek": "The Izu Peninsula is a mountainous peninsula south-west of Tokyo with beaches on the coast and hot-spring towns inland. Our first homes are in Shimoda and Shuzenji.",
 "keywords": [("izu peninsula", "12,100", "7"), ("shuzenji", "1,000", "0")],
}
ABOUT = {
 "h1": "About Noki",
 "seo_title": "About Noki: Who Runs It and How We Write",
 "description": "Noki is written by the team behind NODE Shimoda, a home for long stays on the Izu Peninsula, for people who want more than a few nights in small-town Japan.",
 "dek": "We run NODE Shimoda, a home for long stays on the Izu Peninsula, and we write the guides we wish our guests could read before they arrive.",
}

# ---------------------------------------------------------------- 写真・施設
# 写真は photos/<名前>-<幅>.webp（大きさは build.py がファイルから読む）。
# node-shimoda と yaizu-* は自社の写真（アキヤドの images/photos から）。ほかは Unsplash の写真（PHOTO_CREDITS）。
# Unsplash の写真は場所を特定しない雰囲気の写真として使い、alt・説明文に地名を書かない（撮影地が分かっても、自社の記事の主役の場所としては使わない）。
# yaizu-* は「リフォーム前」と明記する（docs/brand/experience.md の確認済みの条件）。
NODE_URL = "https://nodeshimoda.com/"
# 予約の案内（ボタン）の行き先。公式サイトは日本語だけなので、英語で予約できる Airbnb の部屋のページに送る（2026-11-20 編集長の判断。人の一任）
BOOK_URL = "https://www.airbnb.com/rooms/1444912427010224732"

# Unsplash の写真の出典（写真の名前 → 撮影者・撮影者ページ・写真ページ・写真ID）。2026-11-14 に download_asset でダウンロードを記録して取得。
# ページ下の「Photo credits」に、そのページで使った写真の分だけ「Photo by 撮影者 on Unsplash」を出す（build.py の footer）。
UNSPLASH_UTM = "?utm_source=noki&utm_medium=referral"
PHOTO_CREDITS = {
    "passport-stamps": ("Kit (formerly ConvertKit)", "https://unsplash.com/@kit", "https://unsplash.com/photos/htQznS-Rx7w", "htQznS-Rx7w"),
    "stony-shore-waves": ("Jivan Garcha", "https://unsplash.com/@jivangarcha", "https://unsplash.com/photos/okKMbCtaNNQ", "okKMbCtaNNQ"),
    "studio-apartment": ("Aquilion Property", "https://unsplash.com/@aquilionproperty", "https://unsplash.com/photos/hrY-pZqFGyI", "hrY-pZqFGyI"),
    "laptop-plants-desk": ("Rui Silvestre", "https://unsplash.com/@ruisilvestrecreative", "https://unsplash.com/photos/9vxJQmZmTYU", "9vxJQmZmTYU"),
    "coastal-village": ("PJH", "https://unsplash.com/@dokae", "https://unsplash.com/photos/jb0SsX_Bz_E", "jb0SsX_Bz_E"),
    "window-room": ("ZENG YILI", "https://unsplash.com/@zengyili", "https://unsplash.com/photos/fta5pzyM0T8", "fta5pzyM0T8"),
    "town-lane": ("PJH", "https://unsplash.com/@dokae", "https://unsplash.com/photos/stvwZJNN6Qo", "stvwZJNN6Qo"),
    "empty-tatami-room": ("ayumi kubo", "https://unsplash.com/@ayumikubo", "https://unsplash.com/photos/IAgczbi1B-M", "IAgczbi1B-M"),
    "rocky-coast": ("Lucius Hunter", "https://unsplash.com/@lucius_x14", "https://unsplash.com/photos/a3e4znCn-0o", "a3e4znCn-0o"),
    "grilled-red-fish": ("kazuend", "https://unsplash.com/@kazuend", "https://unsplash.com/photos/lFG7xubInhE", "lFG7xubInhE"),
    "train-window-sea": ("realfish", "https://unsplash.com/@realfish", "https://unsplash.com/photos/E401NBqwIGg", "E401NBqwIGg"),
}
NODE_FACTS = [  # 公式サイト nodeshimoda.com（2026-11-16 取得）と experience.md（人が確認済み）にあることだけ
    "Whole apartment of about 40 m², 8 minutes’ walk from Izukyu-Shimoda Station",
    "Work desk, fast Wi-Fi, free washing machine and gas dryer",
    "Kitchen with gas hob, rice cooker, pans and tableware",
    "Self check-in with a keypad lock",
    "Sleeps up to four; shower only, no bathtub",
    "Licensed under Japan’s Hotel Business Act, open all year",
]

# 場所（"place" のキー → 名前とページ）
PLACES = {"izu": {"name": "Izu Peninsula", "page": "izu"}}
for _a in ARTICLES:
    _a["topics"] = [_a["topic"]] + (["places"] if _a.get("place") else [])
