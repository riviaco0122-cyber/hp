# 見直し方針: kinmedai（slug: kinmedai）

戦略部 2026-11-15。対象は `tools/okaeri/content.py` の ARTICLES `id: kinmedai`。入口は Stay longer（`topic: stay`、`place: izu`）のまま変えない。URL（slug）も変えない。

---

## 1. いまの点数

### 機械採点 39/40（`python3 tools/okaeri/article_score.py kinmedai`、2026-11-15）

| 項目 | 点 | メモ |
|---|---|---|
| title の長さ | 2/2 | 56字 |
| 主な検索語の位置 | 3/3 | 「kinmedai」が先頭 |
| description | 3/3 | 153字 |
| In short | 4/4 | 4項目 |
| h2 の数 / 形 | 2/2・2/2 | 6個、すべて疑問形 |
| FAQ | 4/4 | 4問 |
| 出典 | 5/5 | 5件（公的 2件: shimoda_news, pref） |
| **内部リンク** | **1/2** | 本文からは `izu-from-tokyo` の1本だけ |
| 関連記事 | 2/2 | izu-from-tokyo, izu |
| 文の長さ | 2/2・2/2 | 平均12.1語、30語超 2% |
| NG 語・綴り | 4/4・3/3 | なし |
| メモ | — | 黄色い枠 2か所（店、魚を買える場所） |

### 品質60の見立て（playbook 4-3 に照らした弱い点。品質保証部の前回採点は log に無し）

| 項目 | 見立て | 理由 |
|---|---|---|
| 正確性 20 | 13〜15 | ①「Shimoda lands more kinmedai than any other port in Japan」は出典が2016年の市の広報と県のページで、**何年の水揚げ量かが書かれていない**（時点漏れ -2）。全国の最新の産地別統計で裏づけられていない（今回の検索でも最新の「日本一」の根拠は見つからず。静岡県の資料では一都三県で全国の約8割、という書き方）→ 出典より強い表現の恐れ -3。②本文の「The local tourism association also lists…」の出典は Tabi-mag（旅のメディア）で、観光協会ではない（出典の名前のずれ -1〜-3）。③「from 1 to 30 June every year」「Boats do not go out on Tuesdays or Saturdays」は何年の祭りの情報かが無い（時点漏れ -2）。④「It lives around 500 metres down」は出典が旅メディア。生息水深は幅がある（一般に数百m〜1,000m超）ので「around 500 metres」は言い切りすぎ |
| 検索意図への回答 10 | 6〜7 | 「kinmedai」で探す人の多くは、寿司屋・レシピ・海外の魚屋で名前を見た人。**値段（なぜ高いか）、のどぐろとの違い、家での料理法、水銀の目安**に答えていない（各 -3 の対象になりうる） |
| 独自性・一次情報 10 | 4前後 | 自社の確認済みの体験がゼロ（店も魚を買う場所も黄色い枠のまま）。公的な一次情報は市の広報だけ。上位ページにない視点は「地金目と沖金目」「祭りの水揚げ見学」で、ここは強み |
| 英語の自然さ 5 | 4〜5 | おおむね平易。title の「golden-eye snapper」と本文の「neither a sea bream nor a snapper」が並ぶのが読み手には引っかかる |
| 読みやすさ 5 | 4 | 「食べ方」は箇条書きだが、料理法・食べる場所・時期を比べる表がない。季節の答えが「冬」「6月」の2つで、表にすると一目で分かる |
| 導線 5 | 4 | 自社の家への言及は1回で自然。ただ、次に読む記事が `izu-from-tokyo` だけ |
| 写真 5 | 3〜4 | 見出し写真は「焼いた赤い魚」（Unsplash）。金目鯛の定番は煮付けで、焼き魚の写真は中身とずれる（-2 の恐れ）。alt に地名・魚名は無いので可 |

**見込み: 機械39＋品質 約38〜43 ＝ 約77〜82点。** 90点に届かない主因は「正確性（時点・出典）」と「独自性（一次情報ゼロ）」「検索意図（値段・のどぐろ・料理法）」。

---

## 2. 狙う検索語と検索意図

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| 主な語 | kinmedai | 4,400 | 0 | `review_ja.py` KEYWORDS（2026-11-14） |
| 関連 | golden eye snapper / splendid alfonsino / kinme | 未調査 | — | リサーチ部に調査を依頼（下の 5章） |
| 関連（外す） | shimoda japan | 5,400 | 21 | KEYWORDS。**ROADMAP 6「Shimoda guide」の主な語なので、この記事の `keywords` から外す**（共食い防止。6章） |

- 入口: **Stay longer**（変えない）
- 検索意図: **Know**（金目鯛とは何か）が主、**Go**（どこで食べるか）が従。
- その先で本当に困っていること: 「名前は見たが、高い魚を頼む価値があるのか」「日本でどこに行けばいちばん良いものが食べられるのか」「寿司以外でどう食べるのか」。旅の計画のある人には「下田まで行く価値があるか、日帰りでよいか」。

### 読み手の疑問（品質保証部はこれで採点する）

1. What is kinmedai, and is it a snapper or a sea bream?
2. What does kinmedai taste like, and how is it usually eaten (nitsuke, sushi, aburi)?
3. Why is kinmedai so expensive?
4. Is kinmedai the same as nodoguro (blackthroat seaperch)?
5. When is kinmedai in season?
6. Where is the best place in Japan to eat kinmedai, and why Shimoda?
7. Is it safe to eat kinmedai often (mercury, pregnancy)?
8. Can I see the kinmedai landings or the festival, and do I need to stay overnight?

（3・4・7 はいまの記事に答えが無い。7 は短く、公的な出典の範囲だけで書く）

---

## 3. 上位ページの穴（2026-11-15 に英語で検索。上位の顔ぶれと足りないもの）

検索「kinmedai」の上位: washokufood（2008年のブログ）、charminarmi（転載に見えるページ）、thesushilegend.com、Medium の個人記事、jlearn.net（辞書）、cooksense.org、Wiktionary の写し、SoraNews24 のタグページ。
検索「kinmedai Shimoda where to eat」の上位: Wanderlog、japanrailandtravel.com（2019年）、静岡県の食の都サイト、hamoni.jp の店一覧、Tokyo Weekender（店の紹介）、Prince Hotels の宣伝ページ、Tabelog、livejapan。

具体的な穴:

1. **古い・薄い**: 「kinmedai」の上位は辞書・2008年のブログ・個人の Medium が中心。KEYWORDS の見立てどおり「まともな解説がほぼない」。答えが段落の奥にあり、冒頭で定義と食べ方をまとめたページがない。
2. **数字に時点と出典がない**: 生息水深（「25〜1,250m、主に400〜600m」など）や旬（「冬」「2〜4月」「12〜2月と6〜7月」）がページごとに違い、どれも出典が無い。→ この記事は「旬は2つの答えがある」をすでに出典つきで書いているので、ここを**表にして前に出す**と差になる。
3. **値段・水銀・のどぐろとの違いに誰も答えていない**: 寿司ファン向けのページは味と熟成だけ。厚生労働省の「妊婦への魚介類の摂食と水銀」の注意事項（キンメダイが対象魚に入っているか、目安量）は英語の上位に1件も出てこない（リサーチ部で確認）。
4. **「下田で食べる」系は店の一覧だけ**: hamoni・Wanderlog・Tokyo Weekender は店名の羅列。水揚げの見学（祭りの期間・時間・休漁日）、地金目と沖金目の違い、日帰りでは水揚げに間に合わない、という**旅の組み立ての情報がない**。Prince Hotels は自社の宣伝。
5. **一次情報がない**: 運営者が実際に食べた・ゲストに案内している店、魚を買って家で煮る方法、を書いたページは無い。→ 自社の確認済みの体験が入れば最大の差になる（いまは黄色い枠のまま。人に依頼）。

---

## 4. 直す点

### A. 見せ方だけ（90点以上なら人の確認なしで入れてよい）

| # | 直す点 | 理由 |
|---|---|---|
| A1 | 「Why is Shimoda the place…」の節に、場所のページへの内部リンク `[[l:izu|Izu Peninsula]]` を足す（ja も `[[l:izu|伊豆半島]]`）。最後の節の `izu-from-tokyo` と合わせて本文2本にする | 機械採点の内部リンク 1/2 → 2/2。読み手が「下田はどこか」を知る導線にもなる |
| A2 | 「When is the best time…」を **表** にする（列: 時期／理由／出典。行: 冬・6月・祭りの水揚げ見学）。本文の文章は1〜2文に縮める | 旬の答えが2つあるのが一目で分かる。上位ページの「旬がバラバラ」という穴に対する答えを前に出す（読みやすさ・検索意図） |
| A3 | 「How is kinmedai eaten?」を、料理法ごとの短い表（料理名／ローマ字＋意味／どこで食べられるか）にするか、いまの箇条書きのまま各項目の頭にローマ字の読みを揃える。nitsuke の初出に「fish simmered in soy and sugar」の形で意味を添える（playbook 3章） | 比較の情報なので表が向く。固有名詞の初出ルールに合わせる |
| A4 | `keywords` から `("shimoda japan", "5,400", "21")` を外し、関連語は 2章のとおり（数値はリサーチ部の結果で入れる。分からなければ語だけ） | ROADMAP 6 の下田ガイドと主な語が重なる（共食いのゲート） |
| A5 | In short の4点目「June is festival month. Winter is the other season locals name.」を、疑問に答える形に揃える（例: 旬は冬と6月の2つ、6月は水揚げを見られる祭り）。中身は本文と同じ範囲で | 冒頭だけで答えが出ている状態にする（playbook 2-1） |
| A6 | `related` を `["izu-from-tokyo", "izu"]` のままにする。本文末の「Routes and fares…」の一文は残す | 役割分担（6章）どおり |
| A7 | 見出し写真の差し替え候補を探す（煮付けか、赤い魚が並ぶ市場の写真。地名は書かない）。見つからなければ今の写真のまま、alt はいまのまま | 中身（煮付けが定番）と写真のずれ（写真 -2 の恐れ）。差し替えはエンジニア部・PHOTO_PLAN.md の決まりで |

### B. 事実・数字・出典・主張を変える（`ja.review` と log に「人の確認が必要な点」として必ず書く）

| # | 直す点 | 理由 |
|---|---|---|
| B1 | 「Shimoda lands more kinmedai than any other port in Japan」に**時点**を付ける（例: 市が2016年の広報でそう説明している、と出典の年を書く）。最新の全国統計で確かめられなければ「the city and the prefecture describe Shimoda as Japan’s top landing port for kinmedai」のように**出典の言い方の範囲に弱める**。In short・FAQ・card・description・ja も同じに | 時点漏れ・出典より強い表現（正確性）。今回の検索では最新の「日本一」の根拠が見つからなかった |
| B2 | 「The local tourism association also lists…」を、出典の実際の名前（Tabi-mag）に合わせて直すか、観光協会（下田市観光協会）の一次の出典に差し替える | 出典の名前のずれ（正確性 -1〜-3） |
| B3 | 「It lives around 500 metres down」を、出典つきの幅のある書き方（例: 「usually several hundred metres down」）に直すか、水産研究機関・県の資料に差し替える | 1つの旅メディアの数字で言い切っている |
| B4 | 祭りの期間・見学時間・休漁日（火・土）に**何年の情報か**を付ける。2027年の開催情報が出ていればそれで確認 | 時点漏れ（-2×最大3か所） |
| B5 | **新しい節を1つ足す**: 「Why is kinmedai expensive, and how is it different from nodoguro?」（値段の目安・高い理由・のどぐろとの違い）。値段は出典か、自社の確認済みの体験がある場合だけ数字を書く | 読み手の疑問3・4に答えていない（検索意図 -3×2） |
| B6 | **短い注意を1つ足す**（FAQ か「How is it eaten」の節の末尾）: 厚生労働省の妊婦向けの魚と水銀の注意事項で、キンメダイがどう扱われているか。出典は厚労省のページのみ。医療の助言にしない書き方で | 読み手の疑問7。英語の上位に1件もない公的な一次情報（独自性） |
| B7 | 黄色い枠2か所（ゲストに案内している店2〜3軒、魚を買える場所）を、`docs/brand/experience.md` の確認済みの体験で埋める。**いまは確認済みの記述が無いので、人に依頼する**。埋まらなければ枠のまま（公開不可のまま） | 独自性（一次情報0件で最大4点） |
| B8 | 家で煮る（nitsuke）手順を短い番号つきリストで足すかは、B7 で「ゲストが魚を買って家で料理した」体験が確認できた場合だけ。作り話のレシピは書かない | 「Do」の疑問（家での料理）。一次情報がなければ入れない |
| B9 | 東京からの所要時間「about 2 hours 35 minutes」（ekitan）を、伊豆の記事の更新後の数字と揃える（2026年3月の JR の運賃改定・ダイヤ改正後の値。伊豆の記事の B 項目と同じ確認） | 2記事で数字が食い違わないように |

---

## 5. リサーチ部への依頼

| # | 確かめること | 優先の出典 |
|---|---|---|
| R1 | キンメダイの水揚げ量で、下田（下田市魚市場）が全国で何位か。最新年の数字と、比べる相手（銚子・伊豆諸島の港など） | 農林水産省「漁業・養殖業生産統計」、静岡県水産・海洋技術研究所、下田市の最新資料。見つからなければ「市と県がそう説明している（何年）」で止める |
| R2 | 下田市の広報（2016年6月号）の記述が、いまの市・県のページでも同じか | 下田市・静岡県 |
| R3 | 生息水深と分布（一般的な幅） | 水産研究・教育機構（FRA）の資源評価、県の水産試験場 |
| R4 | 下田きんめ祭り: 2026年の実績と2027年の予定（期間・水揚げ見学の時間・休漁日） | 下田市観光協会・下田市の公式ページ（Tabi-mag は二次として残す） |
| R5 | 「市場の食堂 金目亭」の営業時間・定休日の最新（県のページは2025年3月更新） | 静岡県・店の公式 |
| R6 | 厚生労働省「妊婦への魚介類の摂食と水銀に関する注意事項」で、キンメダイの扱い（対象か、目安量）。英語版の資料の有無 | 厚生労働省 |
| R7 | 金目鯛の値段の目安（市場価格・店での煮付け定食の価格帯）と、高い理由（漁獲量・深海の釣り漁など）を出典つきで | 東京都中央卸売市場の市場統計、県・市の資料 |
| R8 | 金目鯛とのどぐろ（アカムツ）の違い（科・見た目・産地）を出典つきで | 水産研究・教育機構、県の資料、図鑑 |
| R9 | 関連語の月間検索数と KD: golden eye snapper / splendid alfonsino / kinme / nodoguro / kinmedai sushi | 調査ツール（KEYWORDS と同じ方法） |
| R10 | 東京→伊豆急下田の特急「踊り子」の所要時間・運賃（2026年3月の JR 東日本の運賃改定後の値） | JR 東日本・伊豆急行の公式（伊豆の記事と共通） |
| R11 | 人に依頼（リサーチ部ではなく編集長から）: ゲストに実際に案内している店、魚を買える店、家で金目鯛を料理したゲストの例。`experience.md` に確認済みとして足されたものだけ使う | 人 |

---

## 6. 3記事の役割分担と内部リンク

| 記事 | 入口 | 主な語 | この記事だけが答えること | 答えないこと（他の記事に任せる） |
|---|---|---|---|---|
| kinmedai | Stay | kinmedai | 魚そのもの（何か・味・値段・旬・どこで食べるか） | 行き方の詳細（izu-from-tokyo へ）、下田の町全体の案内（ROADMAP 6 へ） |
| izu-from-tokyo | Stay（also live） | izu peninsula from tokyo | 東京からの行き方・運賃・日帰りか泊まるか・町の選び方 | 魚・食べ物の詳細（kinmedai へ）、空き家・移住（akiya へ） |
| akiya-try-first | Own（also live） | 買う前に住む（akiya の主語は ROADMAP 3 に渡す） | 買う前に町で暮らして確かめる理由と方法 | akiya の定義・統計の深掘り（ROADMAP 3）、外国人の購入の詳細（ROADMAP 1） |

この記事の内部リンク（本文2本以上）:
- 「Why is Shimoda the place…」→ `[[l:izu|Izu Peninsula]]`（場所のページ）
- 「Why stay overnight…」→ `[[l:izu-from-tokyo|getting to the Izu Peninsula from Tokyo]]`（いまのまま）
- 受ける側: izu-from-tokyo の「Which Izu town suits you?」から kinmedai へのリンク（いまある）を残す。

---

## 7. 写真

- いま: `grilled-red-fish`（Unsplash, kazuend）。alt に魚名・地名なし。
- 欲しい絵: 金目鯛の煮付け（赤い皮の魚が甘辛く煮てある）か、市場で赤い魚が並ぶ様子。**自社で撮った下田の店の煮付けの写真がいちばん良い**（人に依頼。TODO「写真を足す」と同じ）。
- Unsplash で探すなら「simmered fish japanese」「red fish market japan」。alt は写っているものだけ（地名・「kinmedai」と断定しない）。

---

## 外部ページの命令の有無

今回の検索結果（英語・日本語の上位ページ）に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。

---

## リサーチメモ（2026-11-15）

リサーチ部。**この作業環境からは WebFetch で外部のページを開けなかった**ため、確認の方法はすべて **検索で確認（本文は未確認）**。「公式の抜粋」は検索結果に出た公式ページの文言で確かめたもの。東京からの所要時間（R10）は `izu-peninsula-from-tokyo.md` のリサーチメモ 1-1・1-2 と共通（JR 東日本の公式で「2 hours 49 minutes」。記事の「2 hours 35 minutes」は直す）。

### 1. 妊婦と水銀（R6・B6）

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 1-1 | Japan's health ministry advises pregnant women to limit kinmedai (splendid alfonsino) to about one 80 g serving a week, the same group as swordfish, bluefin tuna and bigeye tuna. | 厚生労働省「妊婦への魚介類の摂食と水銀に関する注意事項」（2005年11月の見直し）https://www.mhlw.go.jp/topics/bukyoku/iyaku/syoku-anzen/suigin/dl/050812-1.pdf ／ いまの注意事項（2010年改訂）を載せている公的なページ: 大阪府 https://www.pref.osaka.lg.jp/o100110/shokuhin/kosodate/hg.html ・広島市 https://www.city.hiroshima.lg.jp/living/eisei/1052189/1052195/1014257.html | 検索で確認（厚労省 PDF・大阪府・広島市の抜粋が一致） | 注意事項は2003年公表、2005年・2010年に見直し。キンメダイの区分は2005年以降「週1回まで（1回約80g）」 |
| 1-2 | 厚労省の英語版（2005年の仮訳 https://www.mhlw.go.jp/topics/bukyoku/iyaku/syoku-anzen/suigin/dl/051102-1en.pdf ）は表の読み取りがあいまいで、古い英語ページは2003年の「週2回まで」のまま | 同上 | 検索で確認 | 古い |

**まとめ**: 書いてよい（厚労省の区分として）。英語版は古い・あいまいなので**出典に英語版を使わない**。言い方は医療の助言にせず「Japan's Ministry of Health, Labour and Welfare lists kinmedai among fish that pregnant women should limit to about 80 g once a week」。厚労省のいまの注意事項のページ（2010年改訂版）そのものは開けていないので、`[[ed:厚労省の現行ページ（2010年改訂）でキンメダイの区分を開いて確認し、URL を差し替える]]` を付けるか、大阪府のページを出典にする。

### 2. 値段・高い理由・のどぐろとの違い（R3・R7・R8・B3・B5）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 2-1 | Kinmedai live in deep water beyond 200 m, mostly on continental slopes and the slopes and tops of seamounts. | 水産研究・教育機構の研究資料（キンメダイは水深200mを超える深場）https://fra.repo.nii.ac.jp/record/2009184/files/kamisu_s_2018_13.pdf ／ 水産庁「キンメダイ太平洋系群 令和元年度資源評価結果」https://www.jfa.maff.go.jp/j/suisin/s_kouiki/taiheiyo/attach/pdf/index-100.pdf | 検索で確認（本文は未確認） | 2018〜2019年の資料 |
| 2-2 | Chiba Prefecture's assessment describes kinmedai off its coast at about 200–800 m. | 千葉県「沿岸重要水産資源 平成30年度資源評価 キンメダイ」https://www.pref.chiba.lg.jp/gyoshigen/shingikai/saibai-shigen/kekka/documents/h30sanko3-2.pdf | 検索で確認 | 2018年度 |
| 2-3 | Off the Pacific coast, kinmedai are caught with vertical and bottom longlines (one hook line at a time), not trawls. | 水産庁「キンメダイ太平洋系群に関する資源管理の基本的な考え方」（2022年12月）https://www.jfa.maff.go.jp/j/council/seisaku/kanri/syuhou/attach/pdf/221220-10.pdf ・同 index-204 | 検索で確認 | 2022年 |
| 2-4 | The Pacific stock's catch was 5,302 t in 2018 (4,298 t from Chiba, Tokyo, Kanagawa and Shizuoka); it has been falling since 2010 and the stock was judged low. | 水産庁 資源評価（令和元年度）index-100（同 2-1） | 検索で確認 | 2018年の漁獲量（令和元年度の評価） |
| 2-5 | 金目鯛の市場価格（円/kg）・店の煮付け定食の価格帯 | **確認できず。** 東京都中央卸売市場の週間市況 PDF は見つかったが、キンメダイの単価は抜粋に無い | — | — |
| 2-6 | 「高いのは○○だから」と因果を言い切る公的な出典 | **確認できず。** 2-1〜2-4（深い・一本ずつ釣る・漁獲が減っている・資源は低位）を事実として並べるところまで | — | — |
| 2-7 | Nodoguro is the local name for akamutsu (blackthroat seaperch), a different fish in a different family (Acropomatidae) from kinmedai. | 京都府「アカムツ」https://www.pref.kyoto.jp/kaiyo/documents/akamutu.pdf ／ 茨城県水産試験場 https://www.pref.ibaraki.jp/nourinsuisan/suishi/teichaku/documents/r7akamutu.pdf | 検索で確認（ホタルジャコ科・赤い体・口の中が黒い） | 府県の資料（年は資料ごと） |
| 2-8 | Akamutsu live shallower than kinmedai, around 80–150 m. | 茨城県水産試験場（同上） | 検索で確認 | 同上 |
| 2-9 | キンメダイがキンメダイ科（Berycidae）であること | 一般的な分類だが、**今回の検索で公的な出典の文言は確認できず** | — | — |

**まとめ**: 「のどぐろとは別の魚（科が違う、のどぐろの方が浅い所にいる）」は府県の資料で書ける。値段の数字は**書かない**（自社の確認済みの体験が入れば別）。「なぜ高いか」は「deep-water fish, caught one line at a time, and catches have fallen since 2010 (Fisheries Agency)」と事実を並べ、「that's why」と言い切らない。生息水深は「usually deeper than 200 m」（水産研究・教育機構・水産庁）に直す（B3）。

### 3. 下田きんめ祭り（R4・B4）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 3-1 | During the Kinme Matsuri you can watch kinmedai being landed at the Shimoda fish market from about 7:30 to 9:00, except on Tuesdays and Saturdays when boats don't go out; times may change. | 伊豆下田観光協会「きんめ祭り」https://www.shimoda-city.info/event/kinme.html | 検索で確認（公式の抜粋。**ページに年の記載なし**） | 年不明（2017年のスタッフブログと同じ内容） |
| 3-2 | 期間は毎年6月1日〜30日（あじさい祭と同じ時期） | 旅マガジン（二次）・観光協会のスタッフブログ（年は古い） | 検索で確認 | **2026年の期間を書いた公式のページは見つからず** |
| 3-3 | 2026年に観光協会が出した6月のページは「赤いかキャンペーン（2026年6月1日〜30日）」で、きんめ祭りの2026年の告知は検索に出なかった | 伊豆下田観光協会 https://www.shimoda-city.info/akaika | 検索で確認 | 2026年 |
| 3-4 | 2027年の予定 | **未発表**（確認できず） | — | — |

**まとめ**: 「毎年6月」は二次と古い資料のみ。書くなら「The festival has been held every June (Shimoda Tourism Association); check dates for the year you visit」とし、`[[ed:2026年に開催されたか、2027年の予定を観光協会に確認]]`。見学時間・休漁日は観光協会のページで書けるが、年が無いので「according to the tourism association's festival page (checked November 2026)」と確認した日を書く。出典は Tabi-mag から観光協会に差し替えられる（B2）。

### 4. 水揚げ日本一の根拠（R1・R2・B1）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 4-1 | Shimoda's tourism association describes Shimoda as Japan's top port for kinmedai landings, with over 1,000 tonnes a year, and says about 80% of the fish landed there are kinmedai. | 伊豆下田観光協会「下田の金目鯛」https://www.shimoda-city.info/kinem ・ https://www.shimoda-city.info/shimoda/kinme.html | 検索で確認（公式の抜粋。統計の出典・年の記載なし） | 年不明（2026年11月に検索） |
| 4-2 | 下田市の広報（2016年6月号）は「漁獲量日本一の金目鯛」と書いている | 広報しもだ 平成28年6月号16頁（いまの `shimoda_news`） | 検索で確認 | 2016年 |
| 4-3 | 港別の最新の全国統計で下田が1位であること | **確認できず。** 農林水産省の統計・水産庁の資料には港別の順位が出てこない（水産庁は「一都三県で太平洋系群の約8割」の書き方） | — | — |

**まとめ**: B1 のとおり「Shimoda's city and tourism association describe it as Japan's top landing port for kinmedai」に弱め、市の広報は「2016」と年を付ける。「over 1,000 tonnes a year」は観光協会の記述として書けるが年が無いので、使うなら「the tourism association says」を付ける。

### 5. 旬（参考。品質保証部の指摘「冬の旬・一年中脂に出典の印がない」）

| # | 事実 | 出典 | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| 5-1 | The tourism association says kinmedai is landed all year; the flesh is firmest in winter and fattiest in early summer. | 伊豆下田観光協会「下田の金目鯛」https://www.shimoda-city.info/kinem | 検索で確認（公式の抜粋） | 年不明 |
| 5-2 | Another association page gives the peak season as December–February, adding that June–July fish are also rich. | 伊豆下田観光協会 https://www.shimoda-city.info/shimoda/kinme.html | 検索で確認（公式の抜粋） | 年不明 |

→ 旬の表（A2）は、この2つと市の広報（2016年）で出典の印を付けられる。

### 6. 新しい出典（`SOURCES_NEW` の候補）

```python
"mhlw_mercury": ("https://www.mhlw.go.jp/topics/bukyoku/iyaku/syoku-anzen/suigin/dl/050812-1.pdf", "Ministry of Health, Labour and Welfare", "厚生労働省", "MHLW: Advice for pregnant women on fish and mercury (2005 revision)"),
"osaka_mercury": ("https://www.pref.osaka.lg.jp/o100110/shokuhin/kosodate/hg.html", "Osaka Prefecture", "大阪府", "Osaka Prefecture: Fish and mercury advice for pregnant women"),
"jfa_kinme": ("https://www.jfa.maff.go.jp/j/suisin/s_kouiki/taiheiyo/attach/pdf/index-100.pdf", "Fisheries Agency", "水産庁", "Fisheries Agency: Splendid alfonsino, Pacific stock assessment (FY2019)"),
"jfa_kinme_mgmt": ("https://www.jfa.maff.go.jp/j/council/seisaku/kanri/syuhou/attach/pdf/221220-10.pdf", "Fisheries Agency", "水産庁", "Fisheries Agency: Management of the Pacific splendid alfonsino stock (2022)"),
"kyoto_akamutsu": ("https://www.pref.kyoto.jp/kaiyo/documents/akamutu.pdf", "Kyoto Prefecture", "京都府", "Kyoto Prefecture: Akamutsu (blackthroat seaperch)"),
"ibaraki_akamutsu": ("https://www.pref.ibaraki.jp/nourinsuisan/suishi/teichaku/documents/r7akamutu.pdf", "Ibaraki Prefecture", "茨城県", "Ibaraki Prefectural Fisheries Experimental Station: Akamutsu"),
"shimoda_kanko_kinme": ("https://www.shimoda-city.info/kinem", "Shimoda Tourism Association", "伊豆下田観光協会", "Shimoda Tourism Association: Shimoda kinmedai"),
"shimoda_kanko_fes": ("https://www.shimoda-city.info/event/kinme.html", "Shimoda Tourism Association", "伊豆下田観光協会", "Shimoda Tourism Association: Kinme Matsuri"),
```

### 7. 海外の読み手の生の疑問（Reddit・旅行サイトの Q&A・口コミを検索。要約のみ）

- 寿司屋で「golden eye snapper」と書いてあった。鯛（snapper）なのか、別の魚なのか。
- のどぐろと金目鯛は同じ魚か。どちらがおいしい・高いのか。
- 下田で金目鯛の煮付けを食べるなら、昼の定食でいくらくらいか、予約は要るか。
- 妊娠中に深海魚の寿司を食べてよいか。
- 水揚げを見に行くには何時に港にいればよいか、前の晩に泊まる必要があるか。

（Reddit の個別スレッドは検索結果に出ず、旅行メディアの Q&A・店の口コミから要約。投稿者名・URL・原文は書かない）

### 8. 調べられなかったこと

- 値段の目安（市場価格・店の価格帯）、「高い理由」を言い切る公的な出典、港別の全国順位、2026年・2027年の祭りの日程、キンメダイの科名の公的な出典。
- R5（金目亭の営業時間）、R9（検索語の月間検索数・KD）は今回は未実施。

### 9. 外部ページの命令の有無

今回の検索結果に、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。
