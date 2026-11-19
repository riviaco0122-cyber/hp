# 構成案: 日本で1か月、部屋を借りる（monthly-rental-japan）

戦略部 2026-11-16。ROADMAP 2「Renting a house in Japan for a month」。新規記事。
- 記事データの案: `id: "monthly-rental"`、`slug: "monthly-rental-japan"`、`topic: "live"`（Live part-time）、`also: ["stay"]`、`place: None`
- ROADMAP の題は “Renting a house” だが、自社の NODE Shimoda は **アパートの一室** なので、題・本文では “a place / a home / a flat” を使い、自社を “house” と呼ばない（`launch-open-items.md`）。

---

## 1. 狙う検索語

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| **主な語**（`keywords` の先頭） | monthly rental japan | 170 | 16 | `review_ja.py` KEYWORDS |
| 関連 | rent a house in japan / japan house rental | 各1,300 | 41 | 同上（難しい。本文の h2・FAQ で自然に受ける） |
| 関連 | long term stay japan / one month in japan | 50〜90 | 0〜18 | 同上 |
| 関連 | monthly apartment japan / rent apartment japan tourist visa | 未調査 | — | 上位に業者の解説が並ぶ語。数値はリサーチ部に依頼（R12） |

- 主な語を「monthly rental japan」にした理由: title の前半に自然に入り、KD が低い。「rent a house in japan」は KD 41 で、上位は Japan Experience・Airbnb などの予約サイトそのもの。title では狙わず、h2「Can a visitor rent a place in Japan for a month?」と FAQ で受ける。
- **共食いの線引き**:
  - akiya-try-first（主な語 buying an akiya in japan）は「買う前に町を試す」ための滞在先として、お試し住宅・マンスリー・宿を1つの表で触れている。この記事は **家を買うつもりのない人も含めた「1か月借りる方法そのもの」**（契約の種類・費用・合法な貸し部屋の見分け方・聞くこと）に答える。**お試し住宅は1文だけで akiya-try-first へ送る**（制度の説明を繰り返さない）。
  - 「何日いられるか」は ROADMAP 9、デジタルノマドは japan-digital-nomad-visa の役割。この記事のビザの節は2〜3文と1行の表だけにして、ノマドの記事へ送る。

## 2. 読み手と検索意図

- 入口: **Live part-time**（数か月・毎年・仕事をしながら）。1か月が「一年の一部を暮らす」の最初の一歩になる。also に Stay longer。
- 検索意図: **Do**（1か月借りる方法と、何を選べばよいか）＋ 一部 Know（費用・決まり）。
- その先で本当に困っていること:
  - 日本の普通の賃貸は2年契約・保証人・礼金で、旅行者には借りられないと聞いた。じゃあ何を探せばいいのか
  - Airbnb で1か月は合法か、急にキャンセルされないか、法律の上限（180日）は関係あるのか
  - 「月いくら」に何が入っているのか（光熱費・ネット・清掃・保証金）、あとで足される費用は何か
  - 東京ではなく小さな町で1か月暮らしたいが、探し方が分からない・物件が少ない
  - 1か月の暮らしに必要な設備（仕事の机と回線、洗濯、冬の暖房、ごみ）を、予約の前に確かめたい

## 3. 読み手の疑問（品質保証部はこれで採点する）

1. Can I rent an apartment or house in Japan for just one month as a tourist?
2. What's the difference between a monthly apartment (*monthly mansion*), an Airbnb-style holiday rental and a share house?
3. How much does a month cost, and what's usually included (utilities, Wi-Fi, cleaning, deposit)?
4. Is renting an Airbnb in Japan for a month legal, and how can I tell a listing is licensed?
5. Why does the host ask for my passport?
6. What should I ask the host before I book a whole month?
7. Is it easy to rent for a month outside Tokyo, in a small town?
8. Do I need a special visa to stay a month? (短く答え、ノマドの記事と akiya-try-first へ送る)

## 4. 上位ページの穴（2026-11-16 に英語で検索）

検索「monthly rental japan furnished apartment foreigners」「rent a house in japan for a month」「monthly mansion japan tourist visa」の上位: japan-dev.com（東京のマンスリー）、e-housing.jp（2025年10月・2026年9月）、realestate-tokyo.com（Plaza Homes など各社の紹介）、best-estate.jp、mooovin.jp、oakhouse.jp（シェアハウス）、x-house.co.jp、matcha-jp.com、resources.realestate.co.jp、Japan Experience（貸別荘の予約サイト）、Airbnb の「monthly stays」、akiyahub.com の monthly rentals、realestateguide.jp「観光ビザで借りられるか」、expatica。

1. **ほぼすべてが東京の話で、売る側が書いている**（マンスリー会社・仲介・シェアハウス運営・予約サイト）。自社の物件に送る作りで、「どれを選ぶべきか」を中立に比べていない。→ 種類ごとの比較表（契約の形・最短の日数・何が含まれるか・海外から予約できるか）で中立に答える。
2. **法律の枠組みに触れていない**。マンスリーは「定期借家契約」、民泊は「住宅宿泊事業法（年180日まで）」、宿は「旅館業法」と、同じ1か月でも中身が違うのに、上位はどれも「マンスリーは最低30日」と業界の慣習だけを書いている。→ 国交省・観光庁・厚労省の一次情報で、「なぜ最低30日なのか」「届出番号・許可番号が掲載に出ていること」「外国人の宿泊者は旅券の写しを求められる理由」を書けば、上位にない情報になる（R1〜R5）。
3. **普通の賃貸がなぜ難しいのかに、公的な裏づけがない**。「在留カードが要る」「保証人が要る」が業者の言い分として書かれているだけ。→ 国交省の「外国人の民間賃貸住宅入居円滑化ガイドライン」など公的資料で説明する（R6）。
4. **費用が「月いくら」の広告の値だけ**。清掃料・光熱費の上限・保証金・予約サイトの手数料など、合計で比べる視点が弱い。→ 金額ではなく「費用の内訳と、確かめる項目」の表にする（業者の値段は時点つきでも二次情報なので、数字は出典がとれたものだけ）。
5. **1か月暮らす側の実務（設備・電気容量・ごみ・洗濯・階段・バスタブの有無）を、運営者の目線で書いたページがない**。→ 自社で長期の滞在者を受けている確認済みの経験（長期滞在とセルフチェックインを前提に設計・洗濯機と乾燥機と調理器具が評価された・古い配線で家電の同時使用に制約）と、自社の公式サイトに出ている事実で「予約の前に聞くこと」を書ける。
6. **小さな町・地方の1か月に答えていない**（上位は東京のエリア選び）。→ 「東京の外で1か月」の節で、物件の少なさ・早めに探す・車・季節（夏の海の町）を書き、伊豆を例に izu-from-tokyo へ送る。

## 5. 構成

### title（`seo_title`）案
- **Monthly Rental in Japan: How to Rent a Place for a Month**（56字・主な語が先頭）
- 予備: Monthly Rentals in Japan: Renting a Place for a Month（53字）

### h1 案
- Monthly rentals in Japan: how to rent a place for a month

### description 案（142字）
- A month in Japan usually means a monthly apartment or a licensed holiday rental, not an ordinary lease. What they cost, and what to ask first.
  - ※「What they cost」は内訳の話。数字を出せないときは「What’s included」に替える。

### dek 案（28語・30語以内）
- Without a residence card, an ordinary Japanese lease is hard to get. For a month, you’re looking at a monthly apartment or a holiday rental with monthly rates.
  - 「hard to get」は R6 の公的資料で裏づけが取れた強さに合わせる（取れなければ “usually isn’t an option for visitors” などに弱める）。

### In short（3項目・各20語以内）
1. Ordinary leases usually expect a residence card and a guarantor, so short-term visitors rarely get one.（16語。R6）
2. Monthly apartments and licensed holiday rentals with monthly rates are the realistic choices for a visitor.（16語）
3. A legal holiday rental shows a licence or notification number, and the host will ask for your passport.（18語。R3・R4）

### h2（7個。6割以上を疑問形）と各節で答えること

| # | h2 | この節で答えること（h2 の直後の1〜2文で答えを言い切る） | 表・リスト |
|---|---|---|---|
| 1 | Can a visitor rent a place in Japan for a month? | 答え: できる。ただし普通の賃貸（2年契約・保証人・礼金・在留カード）ではなく、1か月から借りられる形を選ぶ。普通の賃貸が難しい理由を公的資料で（R6）。疑問1 | — |
| 2 | Monthly apartment, holiday rental or share house: which suits a month? | 種類ごとの比較。契約の法律の枠（定期借家／住宅宿泊事業法／旅館業法）・最短の日数・含まれるもの・海外から予約しやすいか・向いている人。疑問2 | **比較表**（行: monthly apartment／licensed holiday rental（minpaku）／guesthouse or holiday home licensed as lodging（簡易宿所など）／share house／serviced apartment。列: what it is legally・shortest stay・usually included・booking from abroad・good for） |
| 3 | What does a month cost, and what’s included? | 「月いくら」の内訳。家賃・清掃料・光熱費（込みか上限か）・ネット・保証金・予約サイトの手数料・週割と月割。合計で比べる。数字は出典がとれたものだけ、時点つき。疑問3 | **表**（費用の項目／よくある扱い／予約前に聞くこと） |
| 4 | How can you tell a holiday rental is legal? | 民泊は届出が要り、年180日まで（R1）。掲載に届出番号・許可番号が出ている（R3）。宿（旅館業法）は日数の上限がない（R2）。外国人の宿泊者が旅券を求められる理由（R4）。読み手にとっての意味: 番号のない掲載は、途中で泊まれなくなるおそれがある（R3 の公的な注意喚起の範囲で書く）。疑問4・5 | — |
| 5 | What should you ask before booking a whole month? | 1か月暮らす側の確認項目。仕事の机と回線、冬の暖房・夏の冷房、電気の容量（古い建物は家電を同時に使えないことがある＝確認済みの体験）、洗濯機と乾燥機、ごみの出し方（長期の場合）、途中の清掃・リネン、階段・バスタブ、駐車場。**自社の家に触れるのはここ1回**（下の「自社の家」）。疑問6 | **番号つきリスト**（聞く順） |
| 6 | Is it harder to rent for a month outside Tokyo? | 答え: 物件は少ないが、選ぶ基準ははっきりしている。早めに探す、マンスリー会社より宿・貸別荘の月割が中心になりやすい（見解として書く）、車・バス、海の町は夏が混む。東京から2〜3時間の例として伊豆（`[[l:izu-from-tokyo|…]]`）。お試し住宅は1文で `[[l:akiya-try-first|…]]` へ（町の移住者向けで、海外からの旅行者は使えないことが多い、まで）。疑問7 | — |
| 7 | Do you need a visa to stay for a month? | 2〜3文と小さな表1行分まで: 査証免除の国の多くは90日まで（R7、時点つき）。それ以上は在留資格の話で、デジタルノマドの記事へ（`[[l:digital-nomad|…]]`）。疑問8 | — |

- 1記事1主張: **「1か月なら、普通の賃貸ではなく“1か月から借りられる合法の部屋”を選び、合計の費用と暮らしの設備を予約の前に確かめる」**。

### FAQ（5問。本文で答えたことの言い直し）
1. Can I rent an apartment in Japan on a tourist visa?（節1）
2. Is it legal to rent an Airbnb in Japan for a month?（節4）
3. Why does a Japanese host need a copy of my passport?（節4）
4. Are utilities and Wi-Fi included in a monthly rental?（節3）
5. Is it easy to find a monthly rental outside Tokyo?（節6）

### 内部リンク（本文から2本以上）
- 節6 → `[[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]]`
- 節6 → `[[l:akiya-try-first|living in a town before you buy]]`（お試し住宅の1文）
- 節7 → `[[l:digital-nomad|Japan’s digital nomad visa]]`（ノマドの記事が先に公開されていない場合は張らない。上の2本で2本以上は満たす）
- 受ける側: akiya-try-first の「Where can you stay for a month to test a town?」の表の “A monthly rental” の行から、この記事へ1本（akiya の見直しで入れる。akiya 側は表の行を短くしたまま、詳しいことをこちらに送る）。

### related（2本以上）
- `["akiya-try-first", "izu-from-tokyo"]`（ノマドの記事が公開されたら `digital-nomad` を先頭に）

### 自社の家に触れる場所（1回まで）
- 節5の最後に2〜3文。事実は公式サイト（`node_room`・`node_site`、2026-11-16 に取得）と `experience.md` 3-2（人が確認済み）だけ:
  - 下田の旧町内、アパートの2階の一室（約40㎡、最大4名。大人2名と子ども2名に向く）。キッチン・洗濯機・ガス乾燥機・ワークデスク・高速 Wi-Fi。シャワーのみでバスタブなし、階段約13段。電気の容量が大きくないので、電子レンジやドライヤーを使うときはエアコンを一時的に切ってもらっている（公式サイト）。
  - 長期の滞在に週割・月割を付けている（`experience.md` 3-2「長期滞在に週割・月割を付けて清掃回数を減らす」。公式サイトのページには書かれていないので、いまも続いているかをリサーチ部が予約画面で確かめる。R11）。
  - 書き方の例: 節5の「聞くこと」を自分たちがどう答えているかの例として出す（宣伝ではなく、答え方の見本）。“house” と書かない。**30泊以上をいつでも受けられるか・月の料金は書かない**（未確認。公式の予約画面は14泊まで）。
- 写真の node-shimoda は akiya-try-first で使っているので、この記事では本文に入れない（1ページ1枚の見出し写真だけ）。

## 6. リサーチ部への依頼（公式ページで確かめる）

| # | 確かめること | 見るべき公式ページ（例） |
|---|---|---|
| R1 | 住宅宿泊事業法（民泊）: 届出制であること、1年の営業日数の上限が180日であること、自治体の条例でさらに制限できること。2026年11月時点 | 観光庁「民泊制度ポータルサイト」（www.mlit.go.jp/kankocho/minpaku/）。英語版のページがあれば英語の出典に |
| R2 | 旅館業法の簡易宿所・旅館ホテル営業には営業日数の上限がないこと。宿泊と賃貸（定期借家など）の線引き: 「1か月以上の契約なら賃貸として扱われる」という通知・Q&A が公的にあるか（上位ページは「マンスリーは最低30日」とだけ書く。その根拠） | 厚生労働省「旅館業法について」・旅館業法の Q&A、国交省・観光庁の民泊ポータルの Q&A |
| R3 | 民泊の届出番号・旅館業の許可番号が、予約サイトの掲載に表示されること（住宅宿泊仲介業者の義務・観光庁の通知）。違法な掲載の削除の経緯（2018年）など、公的に書かれている範囲 | 観光庁 民泊制度ポータル（仲介業者向け・利用者向けのページ） |
| R4 | 外国人の宿泊者（日本に住所のない人）に旅券の提示・写しの保存を求める決まり（旅館業法・住宅宿泊事業法の両方）と、その公式の説明 | 厚生労働省（旅館業法施行規則・通知）、観光庁 民泊制度ポータル |
| R5 | 定期借家契約の公的な説明（期間の満了で終わる・書面で説明が要る）。マンスリーマンションが定期借家で貸されていることの公的・業界団体の説明があれば | 国土交通省「定期借家制度」のページ、（公社）全国宅地建物取引業協会連合会、（公財）日本賃貸住宅管理協会、（公社）全日本不動産協会 |
| R6 | 普通の賃貸が外国人の短期滞在者に難しい理由の公的な裏づけ: 国交省「外国人の民間賃貸住宅入居円滑化ガイドライン」（在留カード・保証人・保証会社・契約期間の扱い）。標準的な契約期間（2年）を言える公的資料（賃貸住宅標準契約書など） | 国土交通省（住宅局）のガイドライン・標準契約書、（公財）日本賃貸住宅管理協会 |
| R7 | 短期滞在の査証免除: 多くの国・地域は90日、例外（15日・30日など）。2026年11月時点。JESTA の導入予定 | 外務省「ビザ免除国・地域（短期滞在）」（`mofa` の出典。**この環境からは 403 で開けない**） |
| R8 | 費用の目安に使える公的な数字があるか（例: 総務省「小売物価統計調査」の民営家賃を東京都区部と静岡市などで比べる）。使うなら「普通の賃貸の家賃であって、マンスリーの値段ではない」と分けて書ける形で | e-Stat（`python3 tools/estat.py search "民営家賃"`）。なければ金額は書かない |
| R9 | 長期滞在のごみの出し方: 下田市など伊豆の町の、ごみの分け方・収集日の英語の案内があるか（「英語版を役所で聞ける」と書けるか） | 下田市公式サイト（city.shimoda.shizuoka.jp）、伊豆の各市町 |
| R10 | 伊豆の町のお試し住宅: 節6では1文だけ使う。`launch-open-items.md` で「本文はまだ開けていない」とされた伊豆市・静岡県のページを開いて、外国籍・海外在住の人が使えるか | 伊豆市 移住サイト（iju.city.izu.shizuoka.jp）、静岡県 移住サイト（iju.pref.shizuoka.jp/measure/503.html） |
| R11 | NODE Shimoda: 週割・月割が今も予約画面で出るか（`nodeshimoda.com` の予約画面、または Airbnb の掲載）。出なければ記事に書かない | nodeshimoda.com（2026-11-16 に /room・/faq・トップは取得済み。週割・月割の記載は無かった） |
| R12 | 検索語の月間検索数と KD: monthly apartment japan / monthly mansion japan / rent apartment japan tourist visa / one month rental japan | 調査ツール（KEYWORDS と同じ方法） |

**開けない可能性があるドメイン**（2026-11-16、この環境から curl で確認）:
- `www.mofa.go.jp` … 403（Access Denied）。R7 に必要。
- `www.zentaku.or.jp`（全宅連）・`www.retpc.jp`（不動産流通推進センター）… 接続できず。R5・R6 で業界団体を使うなら必要。
- `iju.pref.shizuoka.jp`・`iju.city.izu.shizuoka.jp` … `launch-open-items.md` で接続できなかったと記録あり（R10）。
- `www.mlit.go.jp`・`www.jnto.go.jp` は 200 で開けた。

## 7. 写真

- 見出し写真に欲しい絵: **家具付きの小さな部屋で暮らしている気配**（窓辺の机とノートPC、キッチンのある明るい部屋、洗濯物など）。観光の絵ではなく「暮らす」絵。
- 既存の `photos/` から: `window-room`（窓辺の低い椅子と机、水辺の眺め）は Stay の入口写真なので、一覧で重なる。`town-lane` は Live の入口写真。どちらも避けたい。→ **Unsplash で探す**（検索語の例: “small apartment kitchen japan” “japanese apartment interior” “laptop desk window room”）。`PHOTO_PLAN.md` の手順どおり `download_asset` で記録し、画像を見て選ぶ。
- alt・説明文は写っているものだけ（地名を書かない）。自社の写真（node-shimoda）は見出しに使わない（宣伝の比重を上げないため）。

---

外部のページに書かれた命令: 今回読んだ検索結果・ページに、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。

---

## リサーチメモ（2026-11-16）

リサーチ部。ページはすべて 2026-11-16 に `curl` で本文を開いて確かめた（「検索結果で確認」と書いたものを除く）。英語の公式ページがあるものは英語版を出典にした。

### 1. 事実の表

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| R1-a | Since June 2018, anyone offering paid lodging in a home in Japan must either hold a licence under the Hotel Business Act (*Ryokan-gyo-ho*), be certified as special-zone minpaku, or notify the authorities under the Private Lodging Business Act. | 観光庁 民泊制度ポータル “What is Private Lodging?”（英語版） https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/index_en.html | ページを開いて確認 | 2026-11-16 閲覧 |
| R1-b | A home run under the Private Lodging Business Act (minpaku) can host guests on no more than 180 nights a year, and local ordinances can restrict it further. | 同上（3つの制度の比較表）、観光庁 “About Private Lodging Business Act” https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/law1_en.html | ページを開いて確認 | 同上 |
| R1-c | The 180 nights are counted per property, in a year that runs from noon on 1 April. | 観光庁 law1_en（同上） | ページを開いて確認 | 同上 |
| R2-a | Lodging licensed under the Hotel Business Act (for example, simple lodging) has no annual limit on operating days. | 観光庁 民泊制度ポータル（比較表。英語版 index_en.html の “Limitation on days of operation: No limitation”） | ページを開いて確認 | 同上 |
| R2-b | Japan's tourism and health authorities treat a stay of under one month as, in principle, lodging (a hotel-type service); a listing for a short-term lease has to require at least a one-month stay and say clearly that it is a rental, not lodging. | 観光庁観光産業課長・厚生労働省生活衛生課長「住宅宿泊仲介業者等における短期賃貸借物件等の取扱いについて」（観観産第545号・薬生衛発1106第1号、2018年11月6日） https://www.mlit.go.jp/kankocho/content/001260338.pdf | PDF を開いて確認 | 2018年11月の通知。民泊ポータルの「違法物件の掲載の防止について」に 2026-11-16 時点で掲載 |
| R2-c | The same notice explains why: a lodging contract and a lease give the two sides different rights and duties, and in lodging the operator is responsible for keeping the room clean and the guest doesn't make the room their home. | 同上（1・2項）。厚労省「民泊サービスと旅館業法に関するQ&A」Q1 も同じ2条件 https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000111008.html | PDF・ページを開いて確認 | 同上 |
| R2-d | The government guideline says monthly apartments ("monthly mansions") shouldn't be listed alongside short-stay minpaku on the same booking site. | 同上（住宅宿泊事業法施行要領4-5③を引用） | PDF を開いて確認 | 2018年 |
| R3-a | Booking sites registered as minpaku agents must show each listing's notification number (or similar licence details) so users can see it is legal. | 観光庁 “Main Points of the Measures for the Prevention of Illegal Properties…”（英語版） https://www.mlit.go.jp/kankocho/content/001218228.pdf ／ 日本語「違法物件の掲載の防止について」 https://www.mlit.go.jp/kankocho/minpaku/business/mediation/prevention.html | PDF・ページを開いて確認 | 2018年の通知。ページは 2026-11-16 閲覧 |
| R3-b | The Japan Tourism Agency tells minpaku users to check, on the booking site, whether the registration number and the property's address can be confirmed. | 観光庁 “Safety-assured Private Lodging”（英語版） https://www.mlit.go.jp/kankocho/minpaku/environment_en.html | ページを開いて確認 | 2026-11-16 閲覧 |
| R3-c | When the law took effect in June 2018, booking sites had to cancel future reservations at unregistered properties or move guests to legal ones. | 観光庁観光産業課長通知（2018年6月1日、英語版） https://www.mlit.go.jp/kankocho/content/001244950.pdf | PDF を開いて確認 | 2018年6月 |
| R3-d | Registered agents report listed properties to the Japan Tourism Agency every six months and must promptly remove listings found to be illegal when asked. | 「違法物件の掲載の防止について」（R3-a と同じ日本語ページ） | ページを開いて確認 | 2026-11-16 閲覧 |
| R3-e | The agency's advice to guests is to book minpaku only through registered agents or travel agencies, which don't handle illegal listings. | 観光庁「宿泊者の皆様へ ～違法民泊の利用はやめましょう～」 https://www.mlit.go.jp/kankocho/minpaku/announcement.html | ページを開いて確認 | 2026-11-16 閲覧 |
| R4-a | Under the Private Lodging Business Act, a guest who is a foreign national without an address in Japan must give their nationality and passport number, and the host keeps a copy of the passport. | 観光庁 “Safety-assured Private Lodging”（英語版。R3-b と同じ） | ページを開いて確認 | 2026-11-16 閲覧 |
| R4-b | Under the Hotel Business Act, the guest register must include the nationality and passport number of foreign guests with no address in Japan, and the health ministry asks operators to see the passport and keep a copy with the register. | 厚生労働省「確認の求めに対する回答の内容の公表」（2020年4月6日回答。健康局長通知 健発第0209001号・2005年を引用） https://www.mhlw.go.jp/content/000659685.pdf | PDF を開いて確認 | 2020年4月の回答（2023年の旅館業法改正のあとの条番号は未確認。条番号は書かない） |
| R4-c | All three systems (hotel licence, special-zone minpaku, minpaku notification) require a guest register. | 観光庁 比較表（R1-a と同じ） | ページを開いて確認 | 2026-11-16 閲覧 |
| R5-a | A fixed-term lease (*teiki shakuya*) ends when its term is up, with no renewal, though both sides can agree to sign a new one. | 国土交通省「定期借家権に関するQ&A」 https://www.mlit.go.jp/jutakukentiku/house/teishaku/111215-4.htm | ページを開いて確認 | 2000年の制度開始時の Q&A（いまも掲載） |
| R5-b | A fixed-term lease must be made in writing, and the landlord must explain in a separate document that it won't be renewed. | 同上 | ページを開いて確認 | 同上 |
| R6-a | Japanese private rental contracts normally require a guarantee of the rent, either through a rent-guarantee company or a joint guarantor. | 国土交通省「外国人の民間賃貸住宅入居円滑化ガイドライン」第2章 Q6 https://www.mlit.go.jp/common/001265432.pdf（入口のページ https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk3_000017.html） | PDF を開いて確認 | 第2章の PDF は2018年作成。ガイドラインの表紙は2022年1月版 |
| R6-b | The guideline tells landlords to check a foreign applicant's status of residence first, and notes that if the visa ends before the lease term, the contract can end early. | 同上 Q4 | PDF を開いて確認 | 同上 |
| R6-c | The residence card is issued to foreign nationals allowed to stay mid- to long-term (the guideline lists it, with the passport, as an ID document for screening). | 同上 Q5 | PDF を開いて確認 | 同上 |
| R6-d | An ordinary lease usually runs for two years; key money (*reikin*) of about one to two months' rent is common in the Kanto region and is not refunded; a deposit of about one to two months' rent is refunded after deductions. | 同上（用語の説明） | PDF を開いて確認 | 同上 |
| R7-a | Passport holders of some countries and regions don't need a visa for tourism stays of 90 days or less; most short-term stays allow up to 90 days, and some nationalities get 15, 30 or 180 days. | JNTO “Visa Information” https://www.japan.travel/en/plan/visa-info/ （`/visa-immigration/` から転送） | ページを開いて確認 | 2026-11-16 閲覧 |
| R7-b | On a tourist stay you can't do paid work, enrol in long-term education or apply for residency. | 同上（FAQ “What can’t I do on a visa for tourists?”） | ページを開いて確認 | 同上 |
| R8-a | In 2025, average private-sector rent was ¥9,803 per 3.3 m² per month in Tokyo's 23 wards and ¥4,621 in Shizuoka City. | 総務省統計局「小売物価統計調査（動向編）調査品目の年平均価格」統計表ID 0003420453（e-Stat API） https://www.e-stat.go.jp/dbview?sid=0003420453 | e-Stat API で値を取得 | 2025年平均（2026-04-24 更新の表） |
| R8-b | That figure is the total rent of surveyed private rental homes divided by their floor area, expressed per 3.3 m² (one *tsubo*); it's ordinary-lease rent, not a monthly-apartment price. | 総務省統計局「小売物価統計調査（動向編）利用上の注意 2024年」 https://www.stat.go.jp/data/kouri/doukou/2024np/pdf/riyou2024.pdf | PDF を開いて確認 | 2024年版の注意（2025年の表も同じ定義と判断） |
| R9-a | Shimoda City publishes a guide to sorting household rubbish and a collection calendar for FY2026, in Japanese. | 下田市「家庭ごみの分け方・出し方」 https://www.city.shimoda.shizuoka.jp/category/020100gomi_recycle/110876.html ／「可燃ごみ収集日程表・リサイクル分別収集予定表」 …/155503.html | ページを開いて確認 | 分け方は令和7年4月版、日程表は令和8年度 |
| R9-b | NODE Shimoda asks guests to put burnables in the bin and rinse cans, bottles and PET bottles and leave them in the kitchen, and to contact them about rubbish for long stays. | NODE Shimoda 公式サイト（客室） https://nodeshimoda.com/room（`node_room`） | ページを開いて確認 | 2026-11-16 閲覧 |
| R10-a | Shizuoka City's trial homes are for people living outside Shizuoka Prefecture who are considering moving to the city and have talked to its relocation advisers first. | 静岡市「静岡市お試し住宅」 https://www.city.shizuoka.lg.jp/ijuteiju/s000050.html（`shizuoka_trial`。2026-10-05 更新） | ページを開いて確認 | 2026-11-16 閲覧 |
| R11-a | NODE Shimoda's site says it suits mid- to long-term stays and workations, but doesn't mention weekly or monthly rates. | https://nodeshimoda.com/ ・/room ・/faq ・/reserve（`node_site`・`node_room`） | ページを開いて確認 | 2026-11-16 閲覧 |
| R11-b | NODE Shimoda facts for section 5: a whole flat of about 40 m² on the second floor (about 13 steps), up to 4 guests (best for 2 adults and 2 children), shower only with no bathtub, free washing machine and gas dryer, work desk and fast Wi-Fi; because the electrical capacity is small, guests are asked to switch the air conditioner off briefly when using a microwave, vacuum cleaner or hairdryer. 8 minutes' walk from Izukyu-Shimoda Station. | https://nodeshimoda.com/room ・/faq ・トップ | ページを開いて確認 | 2026-11-16 閲覧（Airbnb の評価はトップで ★4.88・57件。使うなら時点つき） |

### 2. 書かないと決めたこと（確かめられなかった・根拠が弱い）

1. **「マンスリーマンションは定期借家契約で貸される」**: 公的な資料・業界団体の資料で言い切ったものが見つからない（国交省の資料は定期借家そのものの説明、2018年の通知は「賃貸借」とだけ言う）。業界団体（全宅連・日管協）のサイトは開けない。→ 比較表の “what it is legally” は **“a short-term lease (a rental, not lodging)”** までにし、「定期借家」は契約の種類の一例として R5 の説明だけにとどめる（「マンスリーはふつう定期借家」と書かない）。
2. **「普通の賃貸は在留カードがないと借りられない」と言い切ること**: 国交省ガイドラインは「まず在留資格を確かめる」「保証が要るのがふつう」「ビザが契約期間より先に切れると途中で終わることがある」まで。在留カードが必須とは書いていない。→ In short と dek は **“usually expect a guarantor and a status of residence that covers the lease”** のように弱める。dek の “hard to get” は「旅行者にはふつう選べない（usually isn’t an option for visitors）」の強さに（見解として “In our view” を添えてもよい）。
3. **標準的な契約期間2年の根拠**: 国交省ガイドラインの用語説明に「通常2年間」とあるので書いてよい（R6-d）。ただし「法律で2年」とは書かない。
4. **JESTA（電子渡航認証）の導入時期**: 報道（2026年3月の閣議決定、2028年度目標）だけで、入管の公式ページを確かめられなかった。→ **書かない**。
5. **査証免除の国の一覧・例外の国名（15日・30日の国）**: 外務省のページが 403。JNTO は「15・30・180日の国もある」までで国名がない。→ 国名は **書かない**。「多くは90日まで。国籍で違うので外務省の一覧で確かめて」と書き、`mofa` の出典を付けるのは、人が外務省のページを開いて確かめてから（`launch-open-items.md` の残り）。それまでは JNTO（新キー `jnto_visa`）を出典にする。
6. **伊豆の町（伊豆市・南伊豆町）のお試し住宅の条件**: 静岡県の移住サイトは接続できず、伊豆市の移住サイトはメンテナンス中（503）。→ 伊豆の町の条件・料金は **書かない**。節6のお試し住宅の1文は、静岡市の例（R10-a・既存の `shizuoka_long_trial` の国籍の条件）で「移住を考えている人向けで、相談が先」と書き、`akiya-try-first` へ送る。
7. **下田市のごみの英語版**: 公式サイトに英語版が見つからない。「役所で英語版を聞ける」は **書かない**。書けるのは「市が分け方の冊子と収集日程表を出している（日本語）」「長期の滞在は宿にごみの出し方を聞く」まで。
8. **費用の相場（マンスリーの月額・清掃料・光熱費の上限など）**: 業者のページの数字だけ（業者ごとに大きく食い違う）。→ マンスリーの金額は **書かない**。表は「項目・よくある扱い・聞くこと」で作る。公的な数字は R8 の普通の賃貸の家賃だけ（使うなら「普通の賃貸の家賃で、マンスリーの値段ではない」と同じ文で断る）。
9. **NODE Shimoda の週割・月割（R11）**: 予約画面（beds24.com）と Airbnb の掲載がこの環境から開けず、公式サイトにも記載がない。→ **いまの料金の話としては書かない**（`content.py` の `NODE_FACTS` の “Weekly and monthly discounts” も同じ理由で根拠がない。下の「編集長への報告」）。
   - 書いてよい範囲（判断）: `experience.md` 3-2（人が確認済み）の「長期滞在に週割・月割を付けて清掃回数を減らす」を、**開業のときの考え方として過去形で**、節3の「なぜ月割があるのか」の説明に使うのはよい。例: “When we opened NODE Shimoda, we added weekly and monthly discounts, because a guest who stays longer means fewer cleans.” 割引の率・月の料金・「いまも出ている」とは書かない。30泊以上を受けられるかも書かない（公式の予約画面は14泊まで）。
10. **2018年に Airbnb が掲載を消した件数（報道の 48,000件・約8割など）**: 公的な資料に件数がない。→ 件数は **書かない**。書くのは R3-c（違法な物件の予約は取り消し・合法の物件への振り替えを求められた）まで。

### 3. 構成案への補足（執筆部へ）

- **節4の「途中で泊まれなくなるおそれ」**: R3-c・R3-d（違法と分かった掲載は削除、2018年は予約の取り消し）で裏づけられる。ただし「番号のない掲載は必ず違法」とは言わない（旅館業の許可の物件は「届出番号」ではなく許可番号などで、表示の形が違う）。“Look for a notification or licence number on the listing” の強さで。
- **「なぜ最低30日（1か月）なのか」**: R2-b がそのまま答え。上位のページにない一次情報。“Japan’s tourism and health authorities treat anything shorter than a month as lodging, so a monthly rental has to require at least a month” の言い方で `[[s:jta_short_lease_2018]]`。
- **節5の確認項目**: 自社の確認済みの事実に加えて、`experience.md` 9章（人が確認済み）の「アキヤドの運営チームが関わる3物件」の分析が使える。予約の前に聞かれることが多い・好評/不評が出た点として、①階段・階数（急な階段を予約前に説明していたことが好評）②洗濯乾燥機 ③長期の滞在でのごみ置き場のにおい（少数の指摘）④Wi-Fi のルーターの場所と再起動の手順。**使うときの決まり**: エリア（区・駅・町）を伏せる、件数は「ひとつの事例」として、ゲストの言葉は要約、3物件が自社運営か支援かは書かない（9章の注意）。英語では “three homes our team helps run” のように。
- **節5の電気の容量**: 公式サイト（R11-b）と `experience.md` 3-2（古い二芯配線でエアコン・冷蔵庫・電子レンジの同時使用に制約）の両方で裏づけあり。
- **節2の比較表の “what it is legally”**: monthly apartment＝short-term lease（R2-b）／licensed holiday rental（minpaku）＝notified under the Private Lodging Business Act, 180 nights a year（R1）／guesthouse or holiday home licensed as lodging＝Hotel Business Act licence, no annual cap（R2-a）／share house・serviced apartment＝出典なし（share house は「賃貸で、運営会社ごとに条件が違う」以上を書かない。serviced apartment は公的な定義がないので、表から外すか「契約の形は運営会社に確かめる」とする）。
- **節1（普通の賃貸）**: R6-a〜d。“Most ordinary leases run for two years, need a guarantor or a guarantee company, and the landlord will check that your status of residence covers the lease” ＋ “In our view, that rules it out for most visitors on a short stay.”（見解と分ける）
- **節7（ビザ）**: R7-a（JNTO）で2文。ノマドは既存の `isa_nomad_en`。
- **ごみ**: R9。“Rules differ by town; Shimoda’s guide is in Japanese, so for a month-long stay it’s worth asking the host how rubbish works.”

### 4. 新しく使う出典（`SOURCES_NEW` に入れる形）

```python
"jta_minpaku_overview": ("https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/index_en.html", "Japan Tourism Agency", "観光庁（民泊制度ポータル）", "Japan Tourism Agency, Minpaku portal: What is private lodging? (checked November 2026)"),
"jta_minpaku_act": ("https://www.mlit.go.jp/kankocho/minpaku/overview/minpaku/law1_en.html", "Japan Tourism Agency (Private Lodging Business Act)", "観光庁（住宅宿泊事業法とは）", "Japan Tourism Agency, Minpaku portal: About the Private Lodging Business Act (checked November 2026)"),
"jta_minpaku_users": ("https://www.mlit.go.jp/kankocho/minpaku/environment_en.html", "Japan Tourism Agency (for guests)", "観光庁（安心できる民泊環境）", "Japan Tourism Agency, Minpaku portal: Safety-assured private lodging (checked November 2026)"),
"jta_minpaku_illegal": ("https://www.mlit.go.jp/kankocho/minpaku/announcement.html", "Japan Tourism Agency (illegal minpaku)", "観光庁（違法民泊の利用はやめましょう）", "Japan Tourism Agency: To guests — please don’t use illegal minpaku (checked November 2026)"),
"jta_listing_rules": ("https://www.mlit.go.jp/kankocho/content/001218228.pdf", "Japan Tourism Agency, 2018", "観光庁 2018年（違法物件の掲載防止）", "Japan Tourism Agency: Main points of the measures to prevent illegal properties on booking sites (2018)"),
"jta_listing_page": ("https://www.mlit.go.jp/kankocho/minpaku/business/mediation/prevention.html", "Japan Tourism Agency (booking sites)", "観光庁（違法物件の掲載の防止について）", "Japan Tourism Agency: Preventing illegal listings on booking sites (checked November 2026)"),
"jta_cancel_2018": ("https://www.mlit.go.jp/kankocho/content/001244950.pdf", "Japan Tourism Agency, June 2018", "観光庁 2018年6月", "Japan Tourism Agency: Handling of reservations at illegal properties after the Private Lodging Business Act took effect (1 June 2018)"),
"jta_short_lease_2018": ("https://www.mlit.go.jp/kankocho/content/001260338.pdf", "Japan Tourism Agency and MHLW, 2018", "観光庁・厚生労働省 2018年", "Japan Tourism Agency and Ministry of Health, Labour and Welfare: Handling of short-term rental properties by booking sites (6 November 2018)"),
"mhlw_minpaku_qa": ("https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000111008.html", "Ministry of Health, Labour and Welfare", "厚生労働省（民泊サービスと旅館業法Q&A）", "MHLW: Q&A on minpaku services and the Hotel Business Act (checked November 2026)"),
"mhlw_passport": ("https://www.mhlw.go.jp/content/000659685.pdf", "Ministry of Health, Labour and Welfare, 2020", "厚生労働省 2020年", "MHLW: Published reply on storing passport copies with the guest register (April 2020)"),
"mlit_foreign_rental": ("https://www.mlit.go.jp/common/001265432.pdf", "Ministry of Land, Infrastructure, Transport and Tourism", "国土交通省（外国人の民間賃貸住宅入居円滑化ガイドライン）", "MLIT: Guideline for facilitating rental housing for foreign nationals, chapter 2 (Q&A)"),
"mlit_fixed_term": ("https://www.mlit.go.jp/jutakukentiku/house/teishaku/111215-4.htm", "MLIT (fixed-term leases)", "国土交通省（定期借家権Q&A）", "MLIT: Q&A on fixed-term building leases"),
"jnto_visa": ("https://www.japan.travel/en/plan/visa-info/", "JNTO", "日本政府観光局（ビザ）", "JNTO: Visa information (checked November 2026)"),
"estat_rent_2025": ("https://www.e-stat.go.jp/dbview?sid=0003420453", "Statistics Bureau of Japan, 2025", "総務省統計局 小売物価統計調査 2025年", "Statistics Bureau of Japan: Retail Price Survey, annual average prices 2025 — private rent"),
"shimoda_gomi": ("https://www.city.shimoda.shizuoka.jp/category/020100gomi_recycle/110876.html", "Shimoda City", "下田市（家庭ごみの分け方・出し方）", "Shimoda City: How to sort and put out household rubbish (in Japanese)"),
```

既存のキーで使うもの: `node_site`・`node_room`（自社の事実）、`shizuoka_trial`・`shizuoka_long_trial`（お試し住宅の条件）、`isa_nomad_en`（ノマド）。`mofa` は開けないので、確かめられるまで使わない。
`estat_rent_2025` の定義の注は `https://www.stat.go.jp/data/kouri/doukou/2024np/pdf/riyou2024.pdf`（出典欄に足すなら `stat_rent_note` などのキーで）。

### 5. 海外の読み手の生の疑問（Reddit・旅行フォーラム・Q&A を検索して要約）

Reddit そのもののスレッドは検索に出てこなかった（業者の記事が上位を占める）。旅行フォーラム（JREF・Rick Steves のフォーラム）と、業者の記事が拾っている質問から、自分の言葉で要約する。
1. 観光で入国していても、ウィークリー・マンスリーの部屋なら借りられるのか。普通のアパートとは何が違うのか。
2. 「月いくら」に光熱費は入っているのか。上限を超えたら払うのか、最初に一括で払うのか。
3. 途中で帰ることになったら、残りの家賃は戻るのか（途中解約の扱い）。
4. 1か月の Airbnb は合法か。2018年のように突然キャンセルされることはないか。
5. 東京・京都の外、田舎に行くほど短期で借りられる物件が減ると聞くが、どう探すのか。車は要るか。
6. 古い建物のマンスリーは状態がまちまちと聞く。予約の前に何を見て・聞けばよいか（写真・最近のレビュー）。
7. シェアハウスと個室のマンスリー、どちらが1か月に向くか。
8. 普通の賃貸で言われる礼金・敷金・保証人は、1か月の部屋でも要るのか。

（3の途中解約は、構成案の節3の表に「途中で出る場合の扱い（残りの日数の返金の有無）」の行を足すとよい。公的な出典はないので「聞くこと」として書く。）

### 6. 編集長への報告

- **`content.py` の `NODE_FACTS` の “Weekly and monthly discounts”**: 公式サイト（トップ・/room・/faq・/reserve）に記載がなく、予約画面（beds24.com）と Airbnb はこの環境から開けないので、いま出ているかを確かめられない。`experience.md` 3-2 は開業時の方針。いまの事実として出すなら、人の確認か予約画面での確認が要る（公開済みのページに出ているなら、見直しの対象）。
- **公式サイトの Airbnb の評価が「★4.88・57件」になっている**（`experience.md` 3章は51件）。記事で使うなら時点つきで57件に。
- **既存の出典 `minamialps_trial`（南アルプス市）が 404**。サイトのトップも 404 で、サイトの移転か一時的な不具合かは分からない。`akiya-try-first` の出典なので、次の見直しで確かめる。
- **e-Stat の検索で `docs/sources/estat/2026-11-16_search_小売物価統計調査_民営家賃.md` ができた**（`tools/estat.py search` が自動で保存する。コミットするかは編集長の判断）。
- R12（検索語の月間検索数・KD）は、この部署から調査ツールを使えないため **未調査**。

### 7. 開けなかったドメイン

| ドメイン | 状態 | 何のために要るか |
|---|---|---|
| `www.mofa.go.jp` | 403 | R7: 査証免除の国の一覧（国名・日数の例外） |
| `beds24.com` | 接続できず（プロキシで CONNECT 403） | R11: NODE Shimoda の予約画面（週割・月割、最長の泊数） |
| `www.airbnb.jp`・`airbnb.jp` | 接続できず | R11: NODE Shimoda の Airbnb の掲載（週割・月割） |
| `iju.pref.shizuoka.jp` | 接続できず | R10: 静岡県の「お試し住宅一覧」 |
| `iju.city.izu.shizuoka.jp` | 503（サイト側のメンテナンス中の画面） | R10: 伊豆市のお試し住宅。許可の問題ではないので、日を改めて開く |
| `www.zentaku.or.jp`・`www.retpc.jp`・`www.jpm.jp` | 接続できず | R5: マンスリーと定期借家の関係を業界団体の資料で確かめる |

### 8. 外部のページに書かれた命令

今回開いたページ・PDF・検索結果に、ファイル操作・URL へのアクセス・ルールの変更などの命令は見当たらなかった。
