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
