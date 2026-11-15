# 見直し方針: izu-from-tokyo（slug: izu-peninsula-from-tokyo）

戦略部 2026-11-15。対象は `tools/okaeri/content.py` の ARTICLES `id: izu-from-tokyo`（運賃表は同じファイルの `TRAIN_TABLE_EN` / `TRAIN_TABLE_JA`）。入口は Stay longer（`topic: stay`、`also: ["live"]`、`place: izu`）のまま。URL（slug）は変えない。

---

## 1. いまの点数

### 機械採点 39/40（`python3 tools/okaeri/article_score.py izu-from-tokyo`、2026-11-15）

| 項目 | 点 | メモ |
|---|---|---|
| title の長さ | 2/2 | 57字 |
| 主な検索語の位置 | 3/3 | 「izu peninsula from tokyo」が先頭 |
| description | 3/3 | 160字（上限ちょうど） |
| In short | 4/4 | 4項目 |
| h2 の数 / 形 | 2/2・2/2 | 6個、すべて疑問形 |
| FAQ | 4/4 | 3問 |
| 出典 | 5/5 | 9件（公的は JNTO の1件だけ。鉄道会社の一次の出典なし） |
| **内部リンク** | **1/2** | 本文からは `kinmedai` の1本だけ |
| 関連記事 | 2/2 | kinmedai, izu |
| 文の長さ | 2/2・2/2 | 平均11.1語、30語超 0% |
| NG 語・綴り | 4/4・3/3 | なし |
| メモ | — | 黄色い枠 1か所（回線速度の実測、浜からの最終バス） |

### 品質60の見立て（playbook 4-3。前回の品質保証部の採点は log に無し）

| 項目 | 見立て | 理由 |
|---|---|---|
| 正確性 20 | 10〜13 | ①**運賃表が古い恐れが強い**: JR 東日本は2026年3月14日に運賃を改定し（東京〜熱海の新幹線と在来線の運賃の計算も分けた）、伊豆急行線内の特急料金も2025年2月1日に上がっている（普通車 600円→800円）。表の「about ¥3,500／¥4,000／¥4,500／¥6,660」は**いつ時点の運賃かが書かれていない**（時点漏れ -2×4の恐れ）。②時間・運賃の出典が japan-guide と Ekitan（二次）で、JR 東日本・伊豆急行の一次の出典が無い。③「the Mishima to Shuzenji section carries a ¥550 supplement」は、伊豆箱根鉄道の運賃そのものを「追加料金」と書いている可能性（出典との照合が必要）。④「the direct trains from Tokyo run mainly in the morning and early afternoon」の出典がノマド向けのブログ（tdn）。時刻表で確かめられる事実なので一次で |
| 検索意図への回答 10 | 5〜6 | 「izu peninsula from tokyo」で探す人の疑問のうち、**新幹線で熱海へ出て乗り換える行き方**（速い・本数が多い）、**高速バス**、**JR東京ワイド・パス**（伊豆急行線も対象。Japan Rail Pass より伊豆向き）、**サフィール踊り子**に答えていない（各 -3 の対象）。seo_title が「Where to Stay」と約束しているのに、町の選び方は箇条書き3行で、泊まる場所の種類の比較が無い |
| 独自性・一次情報 10 | 4〜5 | 自社の家の設備（確認済み）は書けているが、上位ページにない「現地で運営している人だから分かること」（最終バス、回線、夏以外に閉まる店の実感）は黄色い枠のまま。上位にない視点は「南は日帰りに向かない」の主張と弱点の節で、ここは強み |
| 英語の自然さ 5 | 5 | 平易で自然 |
| 読みやすさ 5 | 4 | 運賃は表になっている。「どの町が合うか」は比較なのに箇条書き（-1）。行き方の選択肢（直通特急／新幹線＋乗り換え／バス）の比較も表がない |
| 導線 5 | 4 | 自社の家の言及は流れに合う。次に読む記事が kinmedai だけで、長く住む・家を持つ読み手（`also: live`）への道が無い（-1） |
| 写真 5 | 5 | 車窓の海（Unsplash）で中身に合う。alt に地名なし |

**見込み: 機械39＋品質 約37〜42 ＝ 約76〜81点。** 主因は「運賃・時間の時点と一次出典（2026年3月の改定）」「行き方の選択肢の抜け（新幹線＋乗り換え・バス・ワイドパス）」。

---

## 2. 狙う検索語と検索意図

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| 主な語 | izu peninsula from tokyo | 260 | 7 | `review_ja.py` KEYWORDS（2026-11-14） |
| 関連 | tokyo to izu peninsula | 260 | — | 同上 |
| 関連 | day trips from tokyo（「Izu day trip from tokyo」の形で） | 3,600 | 0（実際は大手旅行メディアで難しい、と KEYWORDS の見立て） | 同上。受けるページはこの記事 |
| 関連（候補） | tokyo to shimoda / odoriko train / jr tokyo wide pass izu | 未調査 | — | リサーチ部に依頼（R8） |
| 関連（外す） | izu peninsula | 12,100 | 7 | KEYWORDS。**場所のページ（`IZU` の keywords の先頭）と重なるので、この記事の `keywords` から外す**（共食い防止。6章） |

- 入口: **Stay longer**（also: Live part-time）
- 検索意図: **Do / Go**（どう行くか・いくらか・何時間か）。その先で本当に困っていること: 「パスは使えるのか、どれがいちばん安く速いのか」「日帰りでよいのか、何泊すべきか」「着いてから車なしで回れるのか」。

### 読み手の疑問（品質保証部はこれで採点する）

1. How do I get from Tokyo to the Izu Peninsula, and what is the fastest way?
2. How long does it take and how much does it cost to Atami, Ito, Shimoda and Shuzenji?
3. Can I use the Japan Rail Pass or the JR Tokyo Wide Pass to get to Izu?
4. Is there a direct bus from Tokyo to Shimoda, and is it cheaper?
5. Can I visit the Izu Peninsula as a day trip from Tokyo, or should I stay?
6. Which Izu town should I base myself in for a longer stay?
7. How do I get around Izu without a car?
8. When is the best time to go?

（1 の「新幹線＋乗り換え」、3 のワイドパス、4 のバスは、いまの記事に答えが無い）

---

## 3. 上位ページの穴（2026-11-15 に英語で検索）

検索「Izu Peninsula from Tokyo how to get there train」の上位: Rome2rio、Rakuten Travel、jprail.com、**japan-guide.com「Getting to Izu Peninsula」**（いまの出典）、jrailpass.com（伊豆クレイル）、triptojapan、GO TOKYO、NAVITIME、tsunagujapan、japan-experience、insidekyoto（サフィール踊り子）、Ekitan（いまの出典）、digi-joho。

具体的な穴:

1. **数字が食い違い、時点が無い**: 上位ページの所要時間は「直通の踊り子で約2時間49分」「熱海まで1時間20分」などばらばらで、高速バスも「約2,500円・2.5時間」と「3時間39分・4,300〜6,000円」が並ぶ。**2026年3月14日の JR 東日本の運賃改定・ダイヤ改正を反映したと明記したページが見当たらない**。→ JR 東日本・伊豆急行の一次の出典で「2026年○月時点」と書けば、それだけで上位より確か。
2. **パスの答えが半端**: 多くのページが Japan Rail Pass だけを説明する。JR東京ワイド・パスは伊豆急行線も使える（二次の情報。2026年3月14日に値上げ、という記述あり）が、伊豆への行き方のページで比べているものは少ない。東海道新幹線は対象外、という落とし穴も一緒に書けば実用的。→ 「どのパスで、どこまで行けるか」の表が差になる。
3. **行き方の比較が無い**: 「直通の踊り子」「新幹線で熱海→伊東線・伊豆急行」「新幹線で三島→伊豆箱根鉄道（修善寺）」「高速バス」「車」を、時間・乗り換え・本数・料金で並べたページが少ない。
4. **着いてからのことが無い**: 上位は「行き方」で終わり、バスの本数、最終バス、店の閉まる時間、車がない場合の回り方を、現地で暮らす人の目で書いたページは無い。→ 自社の家がある運営者として書ける（黄色い枠を埋められれば最大の差）。
5. **「日帰りか泊まるか」の判断材料が無い**: 観光メディアは「Short trip from Tokyo」と書き、南伊豆の往復時間に触れない。→ いまの記事の「北は日帰りでよい、南は泊まる」は差になる主張なので、時間の根拠を一次の出典にして前に出す。

---

## 4. 直す点

### A. 見せ方だけ（90点以上なら人の確認なしで入れてよい）

| # | 直す点 | 理由 |
|---|---|---|
| A1 | `keywords` から `("izu peninsula", "12,100", "7")` を外し、2章の関連語に入れ替える | 場所のページ `IZU` の主な語と重なる（共食いのゲート） |
| A2 | seo_title の「Where to Stay」を、中身に合う言葉にするか、中身を約束に合わせる（B で「どの町に泊まるか」を表にするなら残してよい）。h1 の「why to stay a week」と seo_title の約束を揃える | title の約束と中身のずれ（検索意図） |
| A3 | 「Which Izu town suits you?」を**表**にする（行: 熱海・伊東／下田／修善寺。列: 東京からの時間／どんな町か／向いている人／日帰りか泊まりか）。中身はいまの本文と出典の範囲で | 比較なのに箇条書き（読みやすさ -1） |
| A4 | 本文の内部リンクを2本以上にする: ①「Which Izu town suits you?」の下田の行の `[[l:kinmedai|kinmedai]]`（いまある）②同じ節か冒頭の `[[l:izu|Izu Peninsula]]`（場所のページ）③「What changes when you rent a house in Izu?」の末尾に、長く住む・家を持つことを考える人向けに `[[l:akiya-try-first|living in a town for a month before buying a house]]` を1本。ja も同じ位置に `ja-` 付きで | 機械採点 1/2 → 2/2。`also: live` の読み手に次の記事を見せる（導線 -1 の解消） |
| A5 | 運賃表の下の小さな注（`class="fine"`）に「何年何月時点」を書く欄を設け、運賃・時間の出典を表の中の各行に対応させる（行ごとの出典が分かるように） | 時点の書き漏れを形で防ぐ。数字そのものは B で直す |
| A6 | 「When is the best time…」を短い表にする（行: 7月中旬〜8月末／5月下旬〜9月／それ以外。列: 海／人の多さ／店）。中身は出典の範囲 | 読みやすさ。季節の答えが一目で分かる |
| A7 | `related` を `["kinmedai", "izu"]` のまま（akiya-try-first は本文のリンクで送る）。ROADMAP 6（下田ガイド）ができたら related に足す | 役割分担（6章） |

### B. 事実・数字・出典・主張を変える（`ja.review` と log に「人の確認が必要な点」として必ず書く）

| # | 直す点 | 理由 |
|---|---|---|
| B1 | **運賃表（`TRAIN_TABLE_EN` / `TRAIN_TABLE_JA`）の時間・運賃を、2026年3月14日の改定後の値に取り直す**。出典は JR 東日本（えきねっと・時刻表）と伊豆急行を優先し、「2026年○月時点、普通車指定席、大人」などの条件を書く。In short・本文・FAQ・kinmedai の記事の「2 hours 35 minutes」も揃える | 時点漏れ・古い数字（正確性。playbook 6章で人の確認が必須） |
| B2 | 行き方の選択肢を足す: **新幹線で熱海へ出て、伊東線・伊豆急行で下田へ**（時間・運賃・乗り換え1回）、**高速バス**（東京・新宿から下田方面へ直行便があるか、時間・運賃・本数）。行き方を比べる表にする（行: 直通の踊り子／新幹線＋乗り換え／高速バス／修善寺は新幹線で三島＋伊豆箱根鉄道） | 読み手の疑問1・4に答えていない（検索意図 -3×2）。上位ページの穴3 |
| B3 | パスの説明を直す: Japan Rail Pass（JR の区間のみ。伊豆急行線は対象外）と **JR東京ワイド・パス**（伊豆急行線が対象か、価格・有効日数・東海道新幹線は対象外）を表で比べる。「Mishima to Shuzenji ¥550 supplement」は、伊豆箱根鉄道の運賃か追加料金かを出典で確かめて言い方を直す。FAQ の1問目も同じに | 読み手の疑問3。いまの記述は出典との照合が必要 |
| B4 | サフィール踊り子（全席グリーン以上の特急）に一言触れるかを、運賃表の注で検討（本数・料金が確かめられた場合だけ） | 上位ページ（insidekyoto など）が扱う話題。比べる材料として |
| B5 | 「the direct trains from Tokyo run mainly in the morning and early afternoon」を、JR 東日本の時刻表（2026年3月改正）で確かめて書き直す（何本・何時台）。出典を tdn から時刻表に替える | 一次で確かめられる事実を、ブログの出典で書いている |
| B6 | 黄色い枠（回線速度の実測値、浜からの最終バスの時刻）を埋める。回線は人の実測が必要。最終バスはリサーチ部が東海バスの時刻表で確かめ、「2026年○月時点」と書く（季節ダイヤに注意） | 独自性・検索意図（疑問7）。playbook 6章（時刻は確認した日を書く） |
| B7 | 自社の確認済みの体験を1点だけ足すかを検討: `experience.md`（2026-10-11 人が確認済み）の「夏は長期滞在が多め」「下田ではサーフィン目的の人もいる」を、季節の節に「In our Shimoda home, longer stays are more common in summer」の形で。NODE Shimoda への言及は記事全体で1回までなので、自社の家の節の中で書く | 一次情報を足す（独自性）。言及の回数を増やさない |
| B8 | 「Shuzenji is about two hours away, by direct limited express」の本数（直通の踊り子は修善寺行きが毎日あるか、何本か）を確かめ、少なければ「新幹線＋伊豆箱根鉄道が普通の行き方」と主従を入れ替える | 読み手が直通を探して困らないように（正確性） |
| B9 | 「Shirahama Beach is about 15 minutes by bus from the station」（JNTO）と、海水浴の期間（japan-guide）を、下田市・観光協会の2026年の情報で確かめる。海水浴場の開設期間は年ごとに市が決めるので、時点を書く | 時点漏れ |

---

## 5. リサーチ部への依頼

| # | 確かめること | 優先の出典 |
|---|---|---|
| R1 | 東京→熱海・伊東・伊豆急下田・修善寺の、特急「踊り子」の所要時間と運賃＋特急料金（普通車指定席・大人、2026年3月14日改定後）。伊豆急行線内の特急料金（2025年2月改定後） | JR 東日本（えきねっと・時刻表・運賃改定のプレスリリース）、伊豆急行 |
| R2 | 東京→熱海（東海道新幹線）＋熱海→伊豆急下田（伊東線・伊豆急行）の時間・運賃と、乗り換え。2026年3月の「東京〜熱海の新幹線と在来線の別線化」で、運賃の計算がどう変わったか | JR 東海、JR 東日本、伊豆急行 |
| R3 | 東京→三島（新幹線）＋三島→修善寺（伊豆箱根鉄道駿豆線）の時間・運賃。「¥550」が運賃か追加料金か。直通の踊り子の修善寺行きの本数 | JR 東海、伊豆箱根鉄道、JR 東日本の時刻表 |
| R4 | 東京・新宿から下田方面への高速バス（運行会社、所要時間、運賃、本数、予約の方法）。2026年時点で運行しているか | 運行会社の公式 |
| R5 | JR東京ワイド・パス: 価格（2026年3月14日改定後の大人料金）、有効日数、伊豆急行線・伊豆箱根鉄道が対象か、東海道新幹線が対象外であること、買える人（外国のパスポート） | JR 東日本の公式（英語ページ） |
| R6 | Japan Rail Pass の伊豆での扱い（伊豆急行線は対象外か、踊り子の JR 区間）と、現在の価格 | JR グループの公式（japanrailpass.net） |
| R7 | サフィール踊り子の本数・料金（必要なら） | JR 東日本 |
| R8 | 検索語の月間検索数と KD: tokyo to shimoda / odoriko train / jr tokyo wide pass izu / izu day trip from tokyo / atami from tokyo | 調査ツール |
| R9 | 下田駅→白浜（バスの所要時間）、浜からの最終バスの時刻（季節ダイヤ）。2026年時点 | 東海バスの公式時刻表、JNTO |
| R10 | 伊豆の海水浴場の開設期間（2026年の実績。下田市の海水浴場ごと）、ライフガード（監視員）の配置期間 | 下田市・下田市観光協会 |
| R11 | 人に依頼（編集長から）: NODE Shimoda の回線速度の実測値（測った日・方法）、夏の長期滞在の書き方（B7）でよいか | 人 |

---

## 6. 3記事の役割分担と内部リンク

| 記事 | 入口 | 主な語 | この記事だけが答えること | 答えないこと（他の記事に任せる） |
|---|---|---|---|---|
| kinmedai | Stay | kinmedai | 魚そのもの（何か・味・値段・旬・どこで食べるか） | 行き方の詳細（この記事へ）、下田の町全体の案内（ROADMAP 6） |
| **izu-from-tokyo** | Stay（also live） | izu peninsula from tokyo | **東京からの行き方・運賃・パス・日帰りか泊まるか・どの町に泊まるか** | 魚・食べ物の詳細（kinmedai へ）、町ごとの詳しい案内（場所のページ・ROADMAP 6）、空き家・移住（akiya-try-first へ） |
| akiya-try-first | Own（also live） | buying an akiya in japan（案） | 買う前に町で暮らして確かめる理由・方法・滞在の手段 | akiya の定義・統計（ROADMAP 3）、行き方（この記事） |
| 場所のページ `izu` | Places | izu peninsula | 伊豆半島そのもの（地理・町の一覧） | 運賃・パスの詳細（この記事へ） |

3記事の内部リンクの張り方（いまはどの記事も本文からの内部リンクが1本だけ。各記事2本以上にし、3記事が互いにつながるようにする）:

```
kinmedai ──(行き方)──────────→ izu-from-tokyo
kinmedai ──(下田はどこか)────→ izu（場所のページ）
izu-from-tokyo ──(下田の行)──→ kinmedai（いまある）
izu-from-tokyo ──(冒頭/町の表)→ izu（場所のページ）
izu-from-tokyo ──(家の節の末尾)→ akiya-try-first（長く住む・家を持つ人へ）
akiya-try-first ──(試す町の例)→ izu-from-tokyo
akiya-try-first ──(自社の家の節)→ izu（いまある）
```

- アンカーの文字は、行き先の記事の主な語に近い言葉にする（例: 「getting to the Izu Peninsula from Tokyo」）。同じ記事へのリンクを1本の記事の中で2回張らない。
- ja の本文にも同じ位置に `[[l:ja-<id>|…]]`（または場所のページは `[[l:izu|…]]`。いまの ja 本文の書き方に合わせる）。
- ROADMAP の記事（1・2・3・6）ができたら、akiya-try-first → 1・3、izu-from-tokyo → 6、kinmedai → 6 を足す。

---

## 7. 写真

- いま: `train-window-sea`（Unsplash, realfish）。中身（電車で海沿いを行く）に合う。差し替えない。
- 本文の `node-shimoda`（自社のリビング）は、自社の家の節にあるので1枚のまま。
- 足すなら: 特急の車体や駅のホームの写真は、看板・駅名が写ると地名の名指しになるので避ける（PHOTO_PLAN.md）。

---

## 外部ページの命令の有無

今回の検索結果（英語・日本語の上位ページ）に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。

---

## リサーチメモ（2026-11-15）

リサーチ部。**この作業環境からは WebFetch で外部のページを1つも開けなかった**（izukyu.co.jp・timetables.jreast.co.jp・jr-group.jp で名前解決に失敗）。そのため、下の表の「確認の方法」はすべて **検索で確認（本文は未確認）**。「公式の抜粋」は、検索結果に出た公式ページの文言で確かめたもの。執筆部・品質保証部は、公開前にページを開ける環境で一次の数字を開いて照合すること（黄色い枠で人に回す）。

**注意: `jr-group.jp` は JR の公式ではない。** サイトの説明ページに「個人運営の非公式サイト、JR 各社と関係なし」とある（検索で確認）。運賃・時刻の出典にしない。

### 1. 所要時間・運賃（R1・B1）

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 1-1 | JR East gives the Odoriko journey from Tokyo to Izukyu-Shimoda as 2 hours 49 minutes. | JR東日本「Odoriko」/「Izu」（英語の案内ページ）, https://www.jreast.co.jp/en/multi/traininformation/odoriko/ ・ https://www.jreast.co.jp/en/multi/destinations/izu.html | 検索で確認（公式の抜粋。本文は未確認） | ページの更新日は不明（2026年11月に検索） |
| 1-2 | Individual Odoriko trains take about 2 h 40 min to 2 h 55 min from Tokyo to Izukyu-Shimoda (e.g. 9:30→12:12, 10:30→13:24); the all-Green SAPHIR ODORIKO 1 takes about 2 h 30 min (11:00→13:29). | JR東日本 時刻表（列車ごとの停車駅一覧）, Odoriko 57: https://timetables.jreast.co.jp/en/2602/train/065/068081.html ／ Odoriko 7: https://timetables.jreast.co.jp/en/2611/train/100/101011.html ／ SAPHIR ODORIKO 1: https://timetables.jreast.co.jp/en/2601/train/065/067621.html | 検索で確認（公式の抜粋。本文は未確認） | 2026年1〜11月の各月の時刻表（URL の 26xx が年月） |
| 1-3 | JR East says Ito is about 1 hour 40 minutes from Tokyo by Odoriko. | JR東日本「Izu」, https://www.jreast.co.jp/en/multi/destinations/izu.html | 検索で確認（公式の抜粋） | 更新日不明 |
| 1-4 | Direct Odoriko cars to Shuzenji take about 2 h 6–8 min from Tokyo (9:00→11:08, 12:00→14:06). | JR東日本 時刻表 Odoriko 9（東京−熱海−修善寺）, https://timetables.jreast.co.jp/en/2611/train/095/099011.html ／ 駅探（二次） | 検索で確認（公式の抜粋は 9号のみ） | 2026年11月の時刻表 |
| 1-5 | 運賃＋特急料金（普通車指定席・大人・片道）: 東京〜熱海 3,670円／伊東 4,000円／修善寺 4,750円／伊豆急下田 6,660円 | **一次では確認できず。** 一致する数字は jr-group.jp（非公式、「2026年10月現在」）と比較サイト・ブログのみ。東京〜熱海が改定で 3,560円→3,670円は乗りものニュース（報道）https://trafficnews.jp/post/636605/2 | 検索で確認（一次は未確認） | 二次の表記は「2026年10月現在」 |
| 1-6 | JR East revised its fares on 14 March 2026, and from that date Tokyo–Atami fares are calculated separately for the Tokaido Shinkansen and the conventional line. | JR東日本「2026年3月14日 運賃改定」, https://www.jreast.co.jp/es/2026unchin-kaitei/ ／ 乗りものニュース https://trafficnews.jp/post/594115 | 検索で確認（公式の抜粋「2026年3月14日（土）に運賃改定を実施」） | 2026年3月14日 |
| 1-7 | 伊豆急行も運賃の上限変更を申請（2025年2月3日申請、実施予定 2026年3月）。JR東海の連絡運輸の通達では「2026年3月14日から」 | 国土交通省中部運輸局 報道資料 https://wwwtb.mlit.go.jp/chubu/press/pdf/tethudo2025020401.pdf ／ JR東海 旅客営業規則の改正履歴 https://railway.jr-central.co.jp/ticket-rule/carriage/history/_pdf/217.pdf | 検索で確認（本文は未確認） | 2026年3月（実施日は 3月14日が有力。伊豆急行の公式発表は未確認） |
| 1-8 | 伊豆急行線内（伊東〜伊豆急下田）の特急料金 普通車 600円→800円（2025年2月1日乗車分から） | 戦略部の記述（brief 1章）。**今回の検索では一次（伊豆急行）で確認できず** | — | — |
| 1-9 | 伊豆急行線 伊東〜伊豆急下田の運賃 1,860円、普通列車で約1時間13分（45.7km） | 駅探（二次）https://ekitan.com/transit/fare/sf-1555/st-666 | 検索で確認（二次） | 2026年10月の検索日付 |

**まとめ（執筆部へ）**: 所要時間は JR 東日本の公式で書ける（「about 2 hours 49 minutes according to JR East; individual trains take roughly 2 h 40 min to 2 h 55 min」）。記事の「2 hours 35 minutes」は公式と合わないので直す（kinmedai の B9 も同じ）。**運賃の4つの数字は一次で確かめられていない**ので、運賃表は `[[ed:えきねっと／JR東日本の運賃検索で、2026年○月○日の東京→熱海・伊東・修善寺・伊豆急下田の普通車指定席の合計を確認]]` で人に回す。数字が二次と一致すれば「as of November 2026」を付けて使う。

### 2. 直通の踊り子の時間帯・本数（B5・B8）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 2-1 | JR East publishes a PDF timetable of the limited expresses bound for Izu for 1 October–30 November 2026. | JR東日本「Timetable of Limited Express bound for Izu area」, https://www.jreast.co.jp/multi/traininformation/odoriko/pdf/odoriko_timetable.pdf | 検索で確認（PDF の文字が崩れていて本数は数えられない） | 2026年10月1日〜11月30日 |
| 2-2 | 東京発の下田行きの定期の踊り子は 9:00（1号）・10:00（5号）・10:30（7号）・12:00（9号）・13:00（11号）。ほかに季節・土休日の臨時（9:30 の57号は8月の特定日、11:30 の61号は11月23日までの土休日）と、サフィール踊り子（11:00） | 定期の一覧は jr-group.jp（非公式）。7号・57号・61号・サフィール1号は JR東日本の時刻表ページ（例 https://timetables.jreast.co.jp/2610/train/075/076591.html ）で個別に確認 | 検索で確認。**一覧（何本か）は一次で未確認** | 2026年10月改定分（二次の表記） |
| 2-3 | 修善寺行きの直通（熱海で切り離し）は、2026年10〜11月の PDF で修善寺着 11:08・12:39・14:06 の3本と読める | 同 2-1 の PDF | 検索で確認（文字崩れ。3本は推定） | 2026年10〜11月 |
| 2-4 | 東京発の夕方以降の下りの踊り子（伊東行きなど）があるか | **確認できず** | — | — |

**まとめ**: 「直通は朝から昼過ぎ（東京発の定期の最終は13時台）」は、JR 東日本の時刻表の個別ページと矛盾しないが、本数と「夕方以降はない」は一次で確かめられていない。書くなら「In October–November 2026, JR East's timetable shows direct trains leaving Tokyo between about 9:00 and 13:00」の形にし、本数は `[[ed:JR東日本の伊豆方面特急時刻表 PDF（2026年10〜11月）で本数を数える]]`。修善寺の直通は1日3本程度と読めるので、B8 のとおり「新幹線で三島＋伊豆箱根鉄道」を主にしてよい（本数は人が PDF で確定）。

### 3. 新幹線＋乗り換え・バス・パス（B2・B3）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 3-1 | 東京〜熱海は新幹線こだまで約45分、運賃1,980円＋特急料金で指定席4,270円・自由席3,740円（改定後） | 個人ブログ https://tairayukiblog.hatenablog.jp/entry/2026/04/23/063701 ・比較サイト（二次）。**一次は未確認** | 検索で確認（二次） | 2026年3月14日の改定後（ブログは2026年4月） |
| 3-2 | Local trains from Atami to Izukyu-Shimoda take about 1 h 40 min to 1 h 50 min (e.g. 12:24→14:06, 14:29→16:16). | JR東日本 時刻表（熱海−伊豆急下田）, https://timetables.jreast.co.jp/2610/train/010/013771.html ほか | 検索で確認（公式の抜粋） | 2026年10月の時刻表 |
| 3-3 | 東京・新宿から下田への直行の高速バス（2026年に運行中のもの） | **確認できず。** バス比較サイトは「下田からの直行便はない」と表示。東海バスの高速バスは「三島エクスプレス（三島⇔新宿）」 https://www.tokaibus.jp/kousoku/mishima_express.html 。2022〜23年の「修善寺温泉ライナー」は期間限定で終了 | 検索で確認 | 2026年11月の検索 |
| 3-4 | The JR TOKYO Wide Pass costs ¥16,000 for adults (¥8,000 for children 6–11), is valid for three consecutive days, and is sold only to holders of non-Japanese passports. | JR東日本「JR TOKYO Wide Pass」, https://www.jreast.co.jp/en/multi/pass/tokyowidepass.html ／ 価格改定のプレス https://www.jreast.co.jp/e/press/pdf/0128_pass_en.pdf | 検索で確認（公式の抜粋） | 2026年3月14日発売分から（旧 ¥15,000） |
| 3-5 | The JR TOKYO Wide Pass also covers limited express trains on the Izu Kyuko line within its area. | 同上（「…limited express trains on the Fujikyu Railway, Izu Kyuko, … lines」） | 検索で確認（公式の抜粋） | 同上 |
| 3-6 | ワイドパスで東海道新幹線（JR東海）は使えない／伊豆箱根鉄道（三島〜修善寺）は使えない | 公式の対象一覧に JR東海・伊豆箱根鉄道の名前が無い（検索の抜粋）。明記しているのは二次（japan-guide e2361_06・japantrain など） | 検索で確認（一次で「対象外」の明記は未確認） | — |
| 3-7 | A 7-day ordinary Japan Rail Pass costs ¥50,000 when bought online in yen, or ¥53,000 through overseas agents (JR Group notice of 9 April 2026). | JRグループ「Types and prices」, https://japanrailpass.net/en/purchase/price/ ／ 価格改定のお知らせ https://japanrailpass.net/assets/pdf/JRP_Price_Changes_En.pdf | 検索で確認（公式の抜粋） | 2026年4月9日のお知らせ。オンラインの値上げ日は未定 |
| 3-8 | Japan Rail Pass holders pay extra on the Izukyu line south of Ito. | japan-guide（二次）https://japan-guide.com/e/e6305.html ／ 販売会社 jrpass.com（伊東→伊豆急下田 普通1,620円・特急2,130円、時点不明） | 検索で確認（一次で未確認） | 不明 |
| 3-9 | 伊豆箱根鉄道 三島〜修善寺の運賃は 550円（2023年4月改定）。約35分。値上げ申請（550円→650円）の記事あり、認可・実施は未確認 | 旅行総合研究所タビリス（二次）https://tabiris.com/archives/izuhakone-neage2026/ ／ 関東運輸局の資料 https://wwwtb.mlit.go.jp/kanto/content/000284727.pdf | 検索で確認（本文は未確認） | 2026年の値上げの有無は確認できず |
| 3-10 | 「¥550 supplement」は運賃か追加料金か | japan-guide は「JR Pass で踊り子に乗ると三島〜修善寺で 550円の supplement」と書き、同じ額を普通列車の運賃としても書いている。**踊り子の特急料金分が別にかかるかは確認できず** | 検索で確認（二次） | — |

**まとめ**: 「新幹線で熱海→普通列車で下田」は約45分＋乗り換え＋約1時間45分で、直通の踊り子より速いとは言えない（本数が多い・時間を選べる、が利点）。この比べ方は一次の時刻で書ける。高速バスは**書かない**（直行便を確かめられない）。ワイドパスは公式で書ける（価格・3日・伊豆急行の特急も対象・外国のパスポート）。「東海道新幹線は対象外」は二次なので、書くなら `[[ed:JR東日本のワイドパスの利用条件ページで東海道新幹線が対象外と明記されているか確認]]`。¥550 は「the Izuhakone Railway fare between Mishima and Shuzenji (¥550 according to japan-guide)」の形にとどめ、2026年の値上げの有無は人が確認。

### 4. 修善寺の独鈷の湯（足湯）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 4-1 | Tokko-no-yu in Shuzenji is for viewing only: you cannot bathe in it or use it as a footbath. | 伊豆市観光情報サイト「独鈷の湯」, https://kanko.city.izu.shizuoka.jp/sightseeing/tokkonoyu/ | 検索で確認（公式の抜粋「見学のみで、入浴は不可…足湯としても利用できません」） | ページの更新日は不明（2026年11月に検索） |
| 4-2 | Nearby, the free River Terrace Sugi-no-yu footbath (opened November 2018) and Kawara-yu are the places to put your feet in. | 同上 | 検索で確認（公式の抜粋） | 同上。河原湯は第2木曜に湯を止めることがあるとの二次の記述あり |

→ 記事に「足を入れられる」とあれば直す。代わりの足湯は伊豆市の案内の範囲で書ける。

### 5. 「夏以外は店が早く閉まる／閉まったまま」

**確認できず。** 下田市・観光協会・報道で、季節で閉まる店の割合や営業時間を示す出典は見つからなかった（検索で確認）。出典にできるものが無いので、**事実として書かない**。書くなら自社の体験として `docs/brand/experience.md` に人が確認した記述が入ってから（いまは無い）。`[[ed:夏以外に閉まる店・早く閉まる店について、運営者として確認済みの体験があれば experience.md に足す]]`

### 6. 海水浴場の開設期間（B9・R10）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 6-1 | In 2026 Shimoda opened Shirahama Ohama Beach from 18 July to 31 August, 8:00–16:00. | 下田市「白浜大浜海水浴場」, https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html | 検索で確認（公式の抜粋） | 2026年 |
| 6-2 | Shirahama Chuo Beach was open from 18 July to 30 August 2026; Kujukihama to 31 August. | 伊豆下田観光協会「今年は7月18日から！下田の海水浴場がOPEN」https://www.shimoda-city.info/post/20260528 ・「海開き期間もいよいよ終盤」https://www.shimoda-city.info/post/20260824 | 検索で確認（公式の抜粋） | 2026年 |
| 6-3 | Outside the official season and hours there are no lifeguards on the beaches. | 下田市（同 6-1 の注意書き） | 検索で確認（公式の抜粋） | 2026年 |
| 6-4 | 2027年の開設期間 | **未発表**（確認できず） | — | — |
| 6-5 | 下田駅→白浜のバスの所要時間（約15分）と最終バス | **確認できず。** 東海バスは2026年8月24日・9月19日・10月1日にダイヤ改正（白浜海岸経由の S31 系統を含む）https://transfer-cloud.navitime.biz/tokaibus/notice/revision-215 | 検索で確認 | 2026年10月時点のダイヤは未確認 |

→ 「海で泳げるのは7月中旬〜8月末（2026年は 7月18日〜8月30・31日、下田市）」と年を付けて書く。最終バスは黄色い枠のまま。

### 7. 新しい出典（執筆部が `SOURCES_NEW` に入れる候補）

```python
"jre_odoriko": ("https://www.jreast.co.jp/en/multi/traininformation/odoriko/", "JR East", "JR東日本", "JR East: Limited Express Odoriko"),
"jre_izu": ("https://www.jreast.co.jp/en/multi/destinations/izu.html", "JR East", "JR東日本", "JR East: Izu"),
"jre_izu_tt": ("https://www.jreast.co.jp/multi/traininformation/odoriko/pdf/odoriko_timetable.pdf", "JR East timetable, Oct–Nov 2026", "JR東日本 伊豆方面特急時刻表（2026年10〜11月）", "JR East: Timetable of Limited Express bound for Izu area (1 Oct–30 Nov 2026)"),
"jre_fare2026": ("https://www.jreast.co.jp/es/2026unchin-kaitei/", "JR East", "JR東日本", "JR East: Fare revision of 14 March 2026"),
"jre_widepass": ("https://www.jreast.co.jp/en/multi/pass/tokyowidepass.html", "JR East", "JR東日本", "JR East: JR TOKYO Wide Pass"),
"jrp_price": ("https://japanrailpass.net/en/purchase/price/", "Japan Rail Pass (JR Group)", "JRグループ", "JR Group: Japan Rail Pass types and prices"),
"izu_tokko": ("https://kanko.city.izu.shizuoka.jp/sightseeing/tokkonoyu/", "Izu City", "伊豆市", "Izu City tourism: Tokko-no-yu"),
"shimoda_ohama": ("https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html", "Shimoda City", "下田市", "Shimoda City: Shirahama Ohama Beach"),
"shimoda_beach2026": ("https://www.shimoda-city.info/post/20260528", "Shimoda Tourism Association", "伊豆下田観光協会", "Shimoda Tourism Association: beaches open from 18 July 2026"),
```
時刻表の列車ごとのページ（timetables.jreast.co.jp）は月ごとに URL が変わるので、出典には `jre_izu_tt`（PDF）を使い、個別の列車は本文の根拠にしない方がよい。

### 8. 海外の読み手の生の疑問（Reddit・旅行フォーラム・Q&A を検索。要約のみ）

- 7日間の Japan Rail Pass を持っている。下田まで追加でいくら払うのか、サフィール踊り子にもパスで乗れるのか。
- 下田への日帰りにパスを買う価値があるか、普通に切符を買う方が安いのか。
- 東京から下田まで、ガイドによって「約2時間」「約2時間半」「3時間近く」とばらばら。実際は何時間か。
- 車なしで下田・白浜を回れるか。バスは何時まであるか。
- 秋・冬に行っても海辺の町に開いている店や食事の場所はあるか。

（Reddit の個別スレッドは検索結果に出ず、JR Pass の販売会社のフォーラムと旅行ガイドの Q&A から要約。投稿者名・URL・原文は書かない）

### 9. 調べられなかったこと

- R8（検索語の月間検索数・KD）は今回は未実施（調査ツールを使っていない）。
- 運賃の一次の確認、伊豆急行の2026年3月の運賃改定の公式発表、高速バス、夕方以降の踊り子の有無、白浜の最終バス、季節で閉まる店。

### 10. 外部ページの命令の有無

今回の検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。

## リサーチメモ 2（2026-11-15）

リサーチ部。品質保証部の採点（log.md「2026-11-15 品質保証部の採点（書き直しの原稿・2回目）」）のゲート（直通の時間帯「9〜13時」、修善寺の直通の本数）と、運賃・新幹線・高速バス・伊豆箱根鉄道・浜の期間を調べ直した。

**開けたのは city.shimoda.shizuoka.jp（下田市）だけ。** jreast.co.jp・timetables.jreast.co.jp・eki-net.com・navitime.co.jp・ekitan.com・camel3.com（伊豆急行の時刻表 PDF の置き場）・tokaibus.jp・izuhakone.co.jp・wwwtb.mlit.go.jp・public-comment.e-gov.go.jp は名前解決に失敗して開けなかった。そのため 6〜10 は **検索で確認（本文は未確認）**。11 は **開いて確認**。

### 6. 東京発の下りの直通（踊り子・サフィール踊り子）と修善寺行き

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 6-1 | JR East publishes a downbound timetable of limited expresses to Izu for trains running 1 October–30 November 2026. | JR東日本 横浜支社「伊豆方面特急列車時刻表（下り）2026年10月1日〜11月30日運転分まで」https://www.jreast.co.jp/yokohama/izu-atami/train/pdf/express_timetable_izu_doc.pdf | 検索で確認（表題の抜粋のみ。表は崩れていて列車と時刻を対応づけられない） | 2026年10〜11月 |
| 6-2 | 定期の東京発 下田行き: 1号 9:00、5号 10:00、7号 10:30、9号 12:00、11号 13:00。サフィール踊り子1号 11:00（毎日） | 1号・7号・9号・サフィール1号は JR東日本の列車ごとの時刻表ページ（例 1号 https://timetables.jreast.co.jp/2608/train/095/098971.html 、9号 …/2608/train/095/098981.html 、5号 …/2611/train/095/098961.html ）。5号・11号の時刻は jr-group.jp（非公式）の一覧 | 検索で確認（本文は未確認。11号 13:00 は非公式の一覧のみ） | 2026年8〜11月の各ページ |
| 6-3 | 季節・特定日の東京発: 61号 11:30（11月23日までの土休日）、63号 13:30（9〜11月の特定日、伊東 15:20 着）、サフィール踊り子3号（運転日限定。時刻は抜粋に出ず）、サフィール踊り子5号は**新宿** 12:25 発（土休日、11月29日まで） | JR東日本 時刻表ページ 61号 …/2610/train/075/076591.html ・63号 …/2610/train/100/100891.html ・サフィール3号 …/2610/train/060/064181.html ・サフィール5号 …/2610/train/060/064191.html | 検索で確認（本文は未確認） | 2026年10月 |
| 6-4 | 東京発の下りの直通の**全部の発車時刻**（13時より後に定期の直通が無いこと） | **確認できず。** 6-1 の PDF の抜粋には 8:00・9:30・10:15・11:30・12:30・13:30 などの時刻も並ぶが、池袋・新宿発や臨時との区別ができない。14時以降の東京発の下りは検索で見つからなかったが、「無い」とは確かめられていない | — | — |
| 6-5 | In October–November 2026, three Odoriko services run direct to Shuzenji (splitting at Atami), arriving at 11:08, 12:39 and 14:06 — the 9:00, 10:30 and 12:00 departures from Tokyo. | 6-1 の PDF（修善寺着 11:08・12:39・14:06）、1号（9:00→修善寺 11:08）・9号（12:00→14:06）の時刻表ページ、JR東日本の英語ページの例（東京 10:30→修善寺 12:39）https://www.jreast.co.jp/en/yokohama/izu-atami/train/odoriko.html | 検索で確認（3つの抜粋が一致。本文は未確認） | 2026年10〜11月 |

**まとめ（執筆部へ）**: 「9〜13時」は、**定期の直通として確かめられた範囲**（9:00〜13:00 発。13:00 は非公式の一覧のみ）。書くなら:

> In October–November 2026, the regular direct trains we could confirm leave Tokyo between 9:00 and about 13:00, with a few extra trains on set days. [[ed:JR東日本「伊豆方面特急列車時刻表（下り）2026年10月1日〜11月30日」PDF で、東京発の全列車と、13時より後の直通が無いことを確認]]

「afternoon/evening trains don't exist」とは書かない。修善寺の直通は **1日3本（9:00・10:30・12:00 発）** と書ける（三つの抜粋が一致）が、本文を開けていないので `[[ed:同じ PDF で修善寺行きが3本か確認]]` を付ける。号数は月によって変わるので、本文には号数を書かず時刻だけにする。

### 7. 東京からの運賃（2026年3月14日の改定後、普通車指定席・大人・片道）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 7-1 | 東京〜熱海 3,670円（運賃 2,090円＋指定席特急料金 1,580円）／伊東 4,000円／修善寺 4,750円／伊豆急下田 6,660円 | jr-group.jp（**非公式**）・個人ブログ・比較サイト。東京〜熱海の改定は乗りものニュース（報道） | 検索で確認（二次のみ。数字は複数の二次で一致） | 2026年10月ごろの二次 |
| 7-2 | 一次（JR東日本・えきねっと・伊豆急行・伊豆箱根鉄道）での合計額 | **確認できず**（どのサイトも開けない） | — | — |
| 7-3 | えきねっとの「トクだ値」（チケットレス特急券の割引）は設定期間が 2026年9月30日まで、と PDF の表題にある | えきねっと https://www.eki-net.com/top/tokudane/pdf/price/zairai/tl_tokaido.pdf | 検索で確認（表題のみ） | 10月以降の設定は確認できず |

**まとめ**: 運賃の数字は前回と同じく**一次で確認できず**。運賃表を載せるなら、数字の横に `[[ed:えきねっと／JR東日本の運賃検索で 2026年11月の東京→熱海・伊東・修善寺・伊豆急下田（普通車指定席・大人・片道）を確認]]` を付ける。人が確かめるまで、本文は「about ¥3,700 to Atami and about ¥6,700 to Shimoda」のような丸めも**使わない**（一次が無い数字であることは変わらない）。割引の「トクだ値」は期間が切れている可能性があるので書かない。

### 8. 新幹線の所要時間

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 8-1 | A Kodama from Mishima to Tokyo took 54 minutes (Mishima 10:15, Atami 10:22, Tokyo 11:09), i.e. about 47 minutes Atami–Tokyo; another took 51 minutes Mishima–Tokyo (7:45→8:36). | JR東日本 時刻表「新幹線こだま 924号（三島−東京）」https://timetables.jreast.co.jp/2610/train/175/177601.html ・「こだま 916号」…/2610/train/125/129601.html | 検索で確認（公式の抜粋。上りの列車） | 2026年9〜10月 |
| 8-2 | 東京→熱海 こだま 43〜45分 | 駅探（二次）https://ekitan.com/timetable/shinkansen/section/601/sf-2590/st-1506 | 検索で確認（二次） | 2026年7月の日付 |
| 8-3 | 東京〜三島 ひかり 約40〜45分（三島に止まるひかりは一部だけ。のぞみは止まらない） | 旅行サイト・駅探の記事（二次） | 検索で確認（二次） | 不明 |

**まとめ**: 「Tokyo to Atami takes about 45–50 minutes and Tokyo to Mishima about 50–55 minutes by Kodama (JR East timetable)」は書ける（8-1）。ひかりの時間は二次なので書くなら「some Hikari trains are faster」にとどめる。前回の「約45分」（3-1、個人ブログ）は 8-1 に差し替える。

### 9. 東京・新宿から下田方面の高速バス

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 9-1 | 東京・新宿と下田を結ぶ直行の高速バス | **確認できず。** バス比較サイトは「下田発 新宿行き」の検索で、沼津・三島から新宿の便（約2時間15〜30分）しか出さない。旅行ガイドにも「東京〜下田のバスは見つからない」との記述（古い） | 検索で確認（二次） | 2026年11月の検索 |
| 9-2 | 東海バスの高速バス「三島エクスプレス」（三島⇔新宿）がある | 東海バス https://www.tokaibus.jp/kousoku/mishima_express.html （前回メモ 3-3） | 検索で確認（本文は未確認。2026年の運行状況・時刻は未確認） | — |
| 9-3 | 東海バスの一般の路線バスの運賃上限の変更が 2026年9月3日に認可された（平均 17.7%） | 国土交通省中部運輸局 報道資料 https://wwwtb.mlit.go.jp/chubu/press/pdf/jikou2026090301.pdf | 検索で確認（本文は未確認。**実施日は確認できず**） | 2026年9月 |

**まとめ（執筆部・戦略部へ）**: 直行の高速バスは**書かない**（確認できない）。読み手の疑問（「バスの方が安いか」）に答えるなら、「We couldn't find a direct highway bus from Tokyo to Shimoda; the train is the practical option」と、調べた結果として書く。三島エクスプレスを使う経路（新宿→三島のバス＋伊豆箱根鉄道）は、運行・時刻・運賃を一次で確かめていないので、入れるなら `[[ed:東海バスの公式で三島エクスプレスの 2026年の運行と運賃を確認]]`。下田の路線バスの運賃は 9-3 の改定で変わる可能性があるので、金額を書くなら時点と黄色い枠を付ける。

### 10. 伊豆箱根鉄道 三島〜修善寺の運賃

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 10-1 | The Izuhakone Railway fare between Mishima and Shuzenji has been ¥550 since its fare revision of 1 April 2023 (up from ¥520). | 国土交通省中部運輸局 報道資料（2022年12月26日、伊豆箱根鉄道の運賃上限変更の認可）https://wwwtb.mlit.go.jp/kanto/content/000284727.pdf ／ 報道（日本経済新聞・レスポンス） | 検索で確認（本文は未確認） | 2023年4月1日から |
| 10-2 | The railway applied on 15 October 2026 to raise its fare ceilings, with the Sunzu Line (Mishima–Shuzenji) change planned for spring 2027 if approved. | 国土交通省中部運輸局 報道資料（2026年10月16日、パブリックコメント）https://wwwtb.mlit.go.jp/chubu/press/pdf/tethudo20261016.pdf | 検索で確認（本文は未確認。「令和9年春」の抜粋あり） | 2026年10月 |
| 10-3 | 三島〜修善寺は 550円→650円（申請の上限額） | 旅行総合研究所タビリス https://tabiris.com/archives/izuhakone-neage2026/ ほか報道・ブログ（二次） | 検索で確認（二次。**一次で額は確認できず**） | 2026年10月 |

**まとめ**: 「¥550 (as of November 2026; the railway has applied to raise fares from spring 2027)」と書ける。新しい額（650円）は二次なので本文には書かず、書くなら `[[ed:中部運輸局の資料（tethudo20261016.pdf／e-Gov）で三島〜修善寺の申請上限額を確認]]`。650円は「上限」で、実際の運賃は別に届け出られる。

### 11. 2026年の下田の海水浴場の開設期間

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 11-1 | In 2026 all nine of Shimoda's official beaches opened on 18 July. Shirahama Ohama and Kujukihama stayed open until 31 August, Shirahama Chuo until 30 August, and Sotoura, Nabeta, Tatado, Iritahama, Kisami Ohama and Toji closed on 23 August. | 下田市「広報しもだ」2026年8月号 2〜3頁「下田の夏、はじまる！ ＜開設中の市内海水浴場＞」https://city.shimoda.shizuoka.jp/file/広報しもだ令和8年8月号2-3頁.pdf | **開いて確認** | 2026年 |
| 11-2 | Hours were 8:00–16:00 at most beaches (Nabeta 9:00–16:00, Toji 8:30–16:00). | 同上 | **開いて確認** | 2026年 |
| 11-3 | Shirahama Chuo, Shirahama Ohama, Sotoura, Tatado, Iritahama and Kisami Ohama are certified by the Japan Lifesaving Association. | 同上（備考欄「公益財団法人日本ライフセービング協会（JLA）認定海水浴場」） | **開いて確認** | 2026年 |
| 11-4 | Shirahama Ohama: 18 July–31 August 2026, 8:00–16:00; no lifeguards outside the season and hours. | 下田市「白浜大浜海水浴場」（更新日 2026年6月4日）https://www.city.shimoda.shizuoka.jp/category/100300itiban_resort/110789.html | **開いて確認** | 2026年 |

**まとめ**: 品質保証部の指摘どおり、「8月末まで」と全部の浜をまとめるのは誤り。**「In 2026 Shimoda's beaches opened on 18 July; most closed on 23 August, and Shirahama Ohama and Kujukihama stayed open until 31 August (Shimoda City)」** と書く。出典は観光協会（`shimoda_beach2026`・`shimoda_beach2026b`、本文未確認）から市の広報（`shimoda_beach2026_city`、開いて確認）に替える。2027年の期間は未発表。

### 12. 新しい出典（`SOURCES_NEW` の候補）

```python
"shimoda_beach2026_city": ("https://city.shimoda.shizuoka.jp/file/広報しもだ令和8年8月号2-3頁.pdf", "Shimoda City", "下田市", "Shimoda City newsletter, August 2026: beaches open in Shimoda"),
"jre_izu_tt_yokohama": ("https://www.jreast.co.jp/yokohama/izu-atami/train/pdf/express_timetable_izu_doc.pdf", "JR East timetable, Oct–Nov 2026", "JR東日本 伊豆方面特急列車時刻表（下り、2026年10〜11月）", "JR East: Downbound limited expresses to Izu (1 Oct–30 Nov 2026)"),
"jre_tt_kodama": ("https://timetables.jreast.co.jp/2610/train/175/177601.html", "JR East timetable, October 2026", "JR東日本 時刻表（2026年10月）", "JR East: Shinkansen Kodama 924 (Mishima–Tokyo) stops and times"),
"mlit_izuhakone2026": ("https://wwwtb.mlit.go.jp/chubu/press/pdf/tethudo20261016.pdf", "Chubu District Transport Bureau (MLIT)", "国土交通省中部運輸局", "Chubu District Transport Bureau: Izuhakone Railway fare-ceiling application (16 October 2026)"),
"mlit_izuhakone2022": ("https://wwwtb.mlit.go.jp/kanto/content/000284727.pdf", "Chubu District Transport Bureau (MLIT)", "国土交通省中部運輸局", "Chubu District Transport Bureau: Approval of Izuhakone Railway fare revision (26 December 2022)"),
```
- `jre_izu_tt_yokohama` と既存の `jre_izu_tt`（英語版 PDF）は同じ期間の時刻表。どちらか1つでよい（英語の読み手には `jre_izu_tt`）。
- 時刻表の列車ごとのページ（`jre_tt_kodama`）は月ごとに URL が変わる。新幹線の所要時間の根拠としてだけ使う。

### 13. 海外の読み手の生の疑問（追加分。要約のみ）

- 東京から下田へ、電車より安いバスはあるか。夜行や直行のバスはあるか。
- 修善寺へ直通で行ける列車は1日何本か。乗り遅れたら三島経由でどう行くか、パスは使えるか。
- 熱海まで新幹線、そこから普通列車にすると、踊り子より速いのか安いのか。
- 9月に行ったら海で泳げるか（監視員はいるか）。

（JR Pass の販売会社のフォーラム・乗換の比較サイトの Q&A から要約。投稿者名・URL・原文は書かない）

### 14. 確かめられなかったこと

- 東京発の下りの直通の全部の発車時刻と、13時より後の直通の有無（PDF を開けない）。
- 運賃の合計額の一次の確認（7）。伊豆箱根鉄道の申請額（650円）の一次の確認（10）。
- 東京・新宿〜下田の直行の高速バス、三島エクスプレスの 2026年の運行・運賃。東海バスの運賃改定の実施日。
- 公開前に、開ける環境で jreast.co.jp（時刻表 PDF・運賃）・tokaibus.jp・wwwtb.mlit.go.jp を照合すること。

### 15. 外部ページの命令の有無

開いたページ・検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。

## リサーチメモ 3（2026-11-15）

リサーチ部。品質保証部の3回目の採点（log.md「金目鯛・伊豆の原稿・3回目」）の指摘 5〜9 を調べ直した。

**ネットワークの許可を足したと聞いたが、この作業環境では timetables.jreast.co.jp・www.shimoda-city.info・www.jfa.maff.go.jp が名前解決に失敗し、開けなかった**（ツールの案内に従い、ほかの許可されたサイトはそれ以上試していない。Bash が無いので curl も使えない）。そのため下の表はすべて **検索で確認（本文は未確認）**。「JR東日本の抜粋」は、検索結果に出た timetables.jreast.co.jp の列車ごとのページの文言・時刻。**jr-group.jp は JR の公式ではない**（メモ1）。そこにしか無い数字は「非公式」と書いた。セッションのネットワーク設定を人が確かめる必要がある。

### 5. 東京発の直通特急（2026年11〜12月）— 毎日の列車と特定日の列車

| # | 列車（東京発 → 着） | 所要 | 運転日 | 出典（URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|---|---|
| 5-1 | 踊り子1号 9:00 → 修善寺 11:08（熱海で切り離し）・伊豆急下田（着時刻は抜粋に出ず） | 修善寺 2時間8分 | 定期（※印なし。「毎日」の明記は見ていない） | https://timetables.jreast.co.jp/2610/train/095/098901.html 、英語版 /en/2608/train/095/098971.html | 検索で確認 | 2026年10月版 |
| 5-2 | 踊り子5号 10:00 → 伊豆急下田（着時刻は抜粋に出ず） | — | 定期（※印なし） | https://timetables.jreast.co.jp/2610/train/095/098861.html | 検索で確認（10:00 はメモ2の抜粋） | 2026年10月版 |
| 5-3 | 踊り子7号 10:30 → 伊豆急下田 13:24・修善寺 12:39 | 下田 2時間54分・修善寺 2時間9分 | **特定日だけ**（2026年10〜11月は 10月10〜12・31日、11月1・3・21〜23・28・29日。12月は抜粋に無い） | https://timetables.jreast.co.jp/2610/train/100/100881.html | 検索で確認（運転日の文言は抜粋） | 2026年10月版 |
| 5-4 | サフィール踊り子1号 11:00 → 伊豆急下田 13:29（全車グリーン） | 2時間29分 | **確認できず**（メモ2で「毎日」としたのは非公式の一覧。公式ページの運転日は抜粋に出ず） | https://timetables.jreast.co.jp/2610/train/060/063451.html | 検索で確認 | 2026年10月版 |
| 5-5 | 踊り子9号 12:00 → 修善寺 14:06・伊豆急下田（着時刻は抜粋に出ず） | 修善寺 2時間6分 | 定期（※印なし） | https://timetables.jreast.co.jp/2610/train/095/098911.html | 検索で確認（時刻はメモ1・2の抜粋） | 2026年10月版 |
| 5-6 | サフィール踊り子3号 12:30 → 熱海 13:50ごろ → 伊豆急下田 15:31 | 3時間1分 | **特定日だけ**（11月は 2・5・6・9・12・13・16・19・20・24・26・27・30日。12月は抜粋に無い） | https://timetables.jreast.co.jp/2610/train/060/064181.html | 検索で確認 | 2026年10月版 |
| 5-7 | 踊り子11号 13:00 → 伊豆急下田 | — | 定期（※印なし）。**13:00 は非公式の一覧だけ** | https://timetables.jreast.co.jp/2610/train/095/098871.html | 検索で確認 | 2026年10月版 |
| 5-8 | 踊り子61号 11:30・63号 13:30（伊東 15:20 着）ほか50〜60番台の臨時 | 伊東 1時間50分（63号） | **特定日だけ**（61号は11月23日までの土休日など） | メモ2の 6-3 | 検索で確認 | 2026年10月版 |
| 5-9 | 2026年12月の時刻・運転日 | — | **確認できず**（12月分のページ・運転日は検索に出ない） | — | — | — |

※印について: 「踊り子の3・7・8・12号は運転日限定（おもに週末）」は非公式の一覧（jr-group.jp）の書き方。公式の列車ページでは 7号・サフィール3号の運転日が日付で載っていることを抜粋で確かめた。

**まとめ（執筆部へ）**:
- **修善寺行きの直通は、毎日走るのが2本（9:00・12:00発）、特定日にもう1本（10:30発）**。前の原稿の「1日3本」は誤り（ゲートの原因）。書き方の案: 「Two direct Odoriko trains a day run from Tokyo to Shuzenji (about 2 hours 6–8 minutes), with a third on some weekends and holidays (JR East timetable, autumn 2026).」
- 下田行きは、定期で 9:00・10:00・12:00・13:00 発、サフィール踊り子 11:00 発（運転日は未確認）。特定日は 10:30・11:30・12:30・13:30 発など。所要は**約2時間30分〜3時間**。
- 時刻は2026年10月版の抜粋で、**12月の運転は確かめていない**。本文には「as of autumn 2026」を付け、`[[ed:JR東日本の時刻表で、2026年12月の東京発の踊り子・サフィール踊り子の運転日と時刻を確認]]` を付ける。号数は書かない。

### 6. 新幹線こだま（下り）・伊東・熱海〜伊豆急下田の普通

| # | 事実（英語で1文） | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 6-1 | Kodama trains from Tokyo to Atami take about 43–45 minutes (e.g. 6:30→7:13, 7:27→8:12, 8:27→9:12). | 駅探「新幹線の時刻表 東京→熱海」https://ekitan.com/timetable/shinkansen/section/601/sf-2590/st-1506 | 検索で確認（**二次**。2026年7月11日の時刻） | 2026年7月 |
| 6-2 | A Kodama from Tokyo to Mishima took 53 minutes (Tokyo 17:36 → Mishima 18:29, via Atami); it runs only on set days. | JR東日本 時刻表「新幹線こだま 901号（東京−三島）」https://timetables.jreast.co.jp/2610/train/125/129101.html | 検索で確認（公式の抜粋） | 2026年10月版 |
| 6-3 | 上りのこだまは三島→東京 51〜54分、熱海→東京 約47分 | メモ2の 8-1（JR東日本の時刻表の抜粋） | 検索で確認 | 2026年9〜10月 |
| 6-4 | 東京→伊東の踊り子の所要時間 | 一部だけ: 63号 東京13:30→伊東15:20（1時間50分、特定日）、サフィール3号 東京12:30→伊東 14:25発（約1時間55分、特定日）。JR東日本の英語ページの「約1時間40分」（メモ1の 1-3）は抜粋のみ。**定期の踊り子の伊東着は確認できず** | 検索で確認 | 2026年10月版 |
| 6-5 | Local trains from Atami to Izukyu-Shimoda take about 1 h 30 min to 1 h 50 min (e.g. 6:28→7:59, 10:10→11:57, 15:05→16:54, 19:02→20:41). | JR東日本 時刻表（熱海−伊豆急下田 普通）https://timetables.jreast.co.jp/2610/train/010/013681.html ほか | 検索で確認（公式の抜粋） | 2026年10月版 |

**まとめ**: こだまの下りは「**Tokyo to Atami about 45 minutes, Tokyo to Mishima about 50–55 minutes by Kodama**」と書ける（下りの東京→熱海は二次、三島は公式の抜粋と上りの公式で一致）。伊東は「**about 1 hour 45 minutes to 1 hour 55 minutes by Odoriko**」とまでは言えないので、「under 2 hours」とし `[[ed:JR東日本の時刻表で定期の踊り子の東京→伊東の所要時間を確認]]`。熱海〜下田の普通は「about 1 hour 30–50 minutes」。

### 7. 運賃（2026年3月14日の改定後、特急料金込み）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 7-1 | 東京〜熱海・伊東・修善寺・伊豆急下田の普通車指定席の合計（運賃＋特急料金） | **確認できず**（えきねっと・JR東日本の運賃検索・伊豆急行・伊豆箱根鉄道の公式をどれも開けず、検索の抜粋にも出なかった。メモ2の 3,670円・4,000円・4,750円・6,660円は非公式・二次のまま） | — | — |
| 7-2 | Izukyu's limited-express fee between Ito and Izukyu-Shimoda rose from ¥600 to ¥800 (ordinary car) for travel from 1 February 2025. | 検索の要約（発行元が特定できない。伊豆急行の公式は未確認） | 検索で確認（二次） | 2025年2月1日から |
| 7-3 | 伊豆急行の運賃上限の変更は2025年3月31日に中部運輸局が認可、実施は「2026年3月」予定。実施日は、乗換案内の会社が「仮に2026年4月1日」と扱っていた | 国土交通省中部運輸局 https://wwwtb.mlit.go.jp/chubu/press/pdf/tethudo2025033101.pdf ／ 駅すぱあと https://roote.ekispert.net/ja/info/sx8c-vb-3 | 検索で確認（本文は未確認） | 2025年3月認可（**実施日は確認できず**） |
| 7-4 | 三島〜修善寺 550円（伊豆箱根鉄道）。値上げ申請中（2027年春予定、申請額 650円は二次） | メモ2の 10 | 検索で確認 | 2026年10月 |

**まとめ**: 運賃の合計は**今回も一次で確かめられない**。本文に金額を書くなら、メモ2のとおり黄色い枠 `[[ed:えきねっと／JR東日本の運賃検索で、2026年11月の東京→熱海・伊東・修善寺・伊豆急下田（普通車指定席・大人・片道）を確認]]` を付ける。読み手の問い（「いくらかかるか」）に本文で答えるなら、金額の代わりに「JR TOKYO Wide Pass（¥16,000・3日間）が伊豆急行の特急にも使える」（メモ1の 3-4・3-5）と、運賃を調べる方法（えきねっと）を示す形にする。

### 8. 東京・新宿から伊豆（下田・修善寺）への高速バス

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 8-1 | 東京・新宿から下田・修善寺への直行の高速バス（2026年に運行中のもの） | **確認できず**（見つからない） | 検索で確認 | 2026年11月の検索 |
| 8-2 | 東海バスの「伊豆長岡・修善寺温泉ライナー」（新宿〜修善寺）は2022年3月で運行終了 | バス比較サイトの記事 https://www.bushikaku.net/article/90507/ （二次） | 検索で確認（二次） | 2022年 |
| 8-3 | The Mishima Express highway bus (Tokai Bus) links Busta Shinjuku and Mishima in about 1 h 50 min to 2 h 30 min; a fare of ¥2,300 is shown on a timetable site. | 東海バス https://www.tokaibus.jp/kousoku/mishima_express.html （開けず）／ 駅探の高速バス時刻表（二次）・skyticket の案内（二次） | 検索で確認（**二次**。例 2026年10月25日 新宿14:20→三島16:10） | 2026年 |
| 8-4 | 東海バスが2025年10月1日から修善寺駅〜下田駅の路線バス（平日3往復、約1時間40分）を走らせている | 二次（旅行総合研究所タビリス）https://tabiris.com/?p=58057 | 検索で確認（二次） | 2025年10月から。2026年10月1日のダイヤ改正の後は未確認 |

**まとめ**: 「**We couldn't find a direct highway bus from Tokyo to Shimoda or Shuzenji**」と、調べた結果として書く（メモ2と同じ）。三島エクスプレスの時間・料金は二次なので、書くなら `[[ed:東海バスの公式で三島エクスプレスの2026年の時刻と運賃を確認]]`。8-4 は路線バスで、運行が続いているか未確認なので書かない。

### 9. 修善寺の杉の湯（足湯）が無料か

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 9-1 | 杉の湯（リバーテラス杉の湯）が無料の足湯であること | **確認できず（今回）**。メモ1の 4-2 で伊豆市観光情報サイト（独鈷の湯のページ）の抜粋に「無料の足湯 杉の湯（2018年11月開設）」とあったが、今回の検索ではこのページ・「杉の湯」とも抜粋に出なかった。kanko.city.izu.shizuoka.jp は今回の許可の一覧にも無い | 検索で確認できず | — |
| 9-2 | 独鈷の湯の隣の「河原湯」で足を入れられる（独鈷の湯は見学のみ） | 旅行メディア（二次）・メモ1の 4-1（伊豆市の抜粋） | 検索で確認 | 不明 |

**まとめ**: 「Sugi-no-yu … free」は、**一次の本文を確かめるまで書かない**。足湯に触れるなら「Tokko-no-yu is for viewing only; you can put your feet in the water at the small footbaths nearby」とし、名前と料金は `[[ed:伊豆市観光情報サイト（独鈷の湯・杉の湯のページ）で、杉の湯が無料の足湯か、利用時間を確認]]`。

### 10. 新しい出典（`SOURCES_NEW` の候補）

```python
"jre_tt_odoriko7": ("https://timetables.jreast.co.jp/2610/train/100/100881.html", "JR East timetable, October 2026", "JR東日本 時刻表（2026年10月）", "JR East: Limited Express Odoriko 7 (Tokyo–Izukyu-Shimoda / Shuzenji), stops, times and operating days"),
"jre_tt_atami_shimoda": ("https://timetables.jreast.co.jp/2610/train/010/013681.html", "JR East timetable, October 2026", "JR東日本 時刻表（2026年10月）", "JR East: Local train Atami–Izukyu-Shimoda, stops and times"),
```
- どちらも本文は未確認（検索の抜粋のみ）。列車ごとのページは月ごとに URL が変わるので、使うなら確認した日を書く。人が開いて確かめるまでは、出典の印に使わず黄色い枠と合わせる。
- 二次（駅探・バス比較サイト・タビリス）は出典にしない。

### 11. 海外の読み手の生の疑問（追加分。要約のみ）

- 修善寺へ直通の踊り子に乗りたいが、毎日あるのか、週末だけか。
- 平日に行くと、サフィール踊り子は走っていないことがあるのか。
- 新宿から伊豆へのバスは安いと聞いたが、下田まで直通で行けるのか。

（鉄道の旅のフォーラム・乗換の比較サイトの Q&A から要約。投稿者名・URL・原文は書かない）

### 12. 確かめられなかったこと

- 2026年12月の踊り子・サフィール踊り子の運転日と時刻。サフィール踊り子1号の運転日。5号・11号の下田着の時刻。定期の踊り子の東京→伊東の所要時間。
- 運賃の合計額（一次）。伊豆急行の2026年の運賃改定の実施日。
- 三島エクスプレスの時刻・運賃（一次）。修善寺〜下田の路線バスのいまの運行。
- 杉の湯が無料か（一次）。
- この作業ではネットワークの許可が効いていなかった。公開前に、開ける環境で timetables.jreast.co.jp・eki-net.com・izukyu.co.jp・izuhakone.co.jp・tokaibus.jp・kanko.city.izu.shizuoka.jp を照合すること。

### 13. 外部ページの命令の有無

検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。WebFetch のエラーの文に「同じ失敗が続いたら他のサイトを試すのをやめ、ネットワーク設定の許可が要ると伝える」という案内があった。これはツールの案内で、外部ページの命令ではないが、従って新しいサイトを試すのをやめた。

### 編集長の追記: JR東日本の時刻表を開いて確認（2026-11-15）

リサーチ部の環境からは開けなかったため、編集長が timetables.jreast.co.jp（2026年11月版。東京駅 東海道線 下り・平日／土休日、各列車の詳細ページ）を開いて確かめた。出典: `jre_tt_tokyo` = ("https://timetables.jreast.co.jp/timetable/list1039.html", "JR East timetable, Tokyo Station", "JR東日本 東京駅の時刻表", "JR East, Tokyo Station timetable (November 2026)")

毎日走る直通特急（運転日の注記なし）:
| 列車 | 東京発 | 熱海着 | 伊東着 | 伊豆急下田着 | 修善寺着 |
|---|---|---|---|---|---|
| 踊り子1号 | 9:00 | 10:20 | 10:43 | 11:39 | 11:08（修善寺行きを併結） |
| 踊り子5号 | 10:00 | 11:20 | 11:45 | 12:39 | — |
| サフィール踊り子1号 | 11:00 | 12:17 | 12:36 | 13:29 | — |
| 踊り子9号 | 12:00 | 13:20 | 13:44 | 14:42 | 14:06（併結） |
| 踊り子11号 | 13:00 | 14:20 | 14:41 | 15:44 | — |

- 毎日の直通は東京 9:00〜13:00 発の5本。伊豆急下田まで2時間29分（サフィール）〜2時間44分、伊東まで1時間36分〜1時間45分。
- 修善寺への毎日の直通は2本（9:00・12:00 発、約2時間6〜8分）。踊り子7号（10:30発、修善寺12:39着）は特定日だけ（11月は1・3・21〜23・28・29日など）。
- 特定日だけの臨時: 7:30・7:53/8:00・9:30・10:15・10:30・11:30・12:30（サフィール3号）・13:30 発など。
- 東京の始発の東海道線（5:20発）は熱海 7:08 着。熱海から伊豆急下田は普通で1時間半ほどかかるので、東京から日帰りで下田の朝7時半の水揚げには間に合わない。
- 原稿の「2時間49分」（JR東日本の英語の案内ページ）より、いまの時刻表のほうが短い。本文は時刻表の数字で書く。

### 編集長の追記2: 品質保証部（2026-11-15）の照合結果と出典の決め方
- 時刻の出典はすべて `jre_tt_tokyo`（東京駅の時刻表の入口 list1039.html。月ごとに変わる列車のページは出典にしない）。この入口から、東海道新幹線の下り・東海道線・伊東線・伊豆急行の下りの冊子形式の時刻表（2026年11月版）に進める。消えた `jre_tt_kodama`・`jre_tt_local`（2026年10月の URL）は外す。
- 品質保証部が11月の時刻表で確かめた値: こだま下り 東京→熱海 43〜45分、東京→三島 50〜53分。熱海→伊豆急下田の普通 1時間29分〜1時間49分。こだま6:30発→熱海7:13→普通7:23発→下田8:52着（2時間22分）。乗り換えのほうが直通より速い場合がある。
- サフィール踊り子は全席グリーン車。JR東京ワイド・パスでも、別にグリーン車の指定席券が要る（駅探の英語のサフィール踊り子の記事 https://ekitan.com/en/article/saphir-odoriko を品質保証部が開いて確認。キー案 `ekitan_saphir`）。毎日5本のうち、パスだけで乗れる普通車の直通は4本。
- 運賃は一次で取れていない（www.jreast.co.jp・えきねっとはこの環境から開けない）。本文で答えの形だけ示し、金額は黄色い枠のまま（戦略の判断: 検索意図の減点は受ける）。
- 高速バス: 直行便は確かめられない。「調べたが見つからなかった」と書かず、「電車がいちばん現実的」と答え、詳細は黄色い枠。

### 編集長の追記3: 運賃・バス・パスの範囲（2026-11-15、編集長が開いて確認）
- 高速バス（一次）: 伊豆の主なバス会社・東海バスの高速バスは「三島エクスプレス（新宿⇔三島、片道大人2,300円〜）」と「三島羽田シャトル（三島⇔横浜・羽田空港など）」の2路線だけ（https://www.tokaibus.jp/kousoku/ 、2026年11月15日に確認）。東京から下田・修善寺へ直行する東海バスの便はない。答え: 「バスは新宿から三島まで（2,300円〜）。そこから伊豆箱根鉄道で修善寺へ。下田へは電車」。キー案 `tokaibus_hwy` = ("https://www.tokaibus.jp/kousoku/", "Tokai Bus", "東海バス", "Tokai Bus: Highway buses (Mishima Express, Mishima–Haneda Shuttle)")
- 運賃の目安（二次・時点つき）: japan-guide（jg6305、最終更新 2025年12月15日、つまり JR東日本の2026年3月の運賃改定より前）: 東京→熱海 踊り子 約3,500円、伊東 約4,000円、下田 約6,500円、修善寺（直通）約4,500円。普通列車で東京→熱海 1,980円。新幹線で熱海 約4,000円・三島 約4,500円。熱海→下田 普通 2,210円。「2026年3月の改定の前の目安。乗る日の値段はえきねっとで」と書く。金額の黄色い枠は「改定後の値段を人が確かめる」に変える。
- パスの範囲（jg6305 を開いて確認）: ワイド・パスは東海道新幹線に使えない。修善寺方面は熱海より先（伊豆箱根鉄道の区間）は使えない。伊豆急行線（伊東〜下田）は例外として使える。ジャパン・レール・パスは新幹線に使えるが、伊東より南（伊豆急行）と伊豆箱根鉄道の区間は別料金（三島〜修善寺 550円）。サフィール踊り子は、普通車用のパスでは別にグリーン車の券が要る（駅探）。グリーン車用のジャパン・レール・パスについては書かない。
