# 構成案: 日本に何日滞在できるか（how-long-stay-japan）

戦略部 2026-11-19。ROADMAP 9「How long can you stay in Japan?」。新規記事。Live part-time の3本目（テーマ別の一覧ページが検索に載る条件を満たす）。
- 記事データの案: `id: "how-long-stay"`、`slug: "how-long-can-you-stay-in-japan"`、`topic: "live"`（Live part-time）、`also: ["stay"]`、`place: None`
- 1記事1主張: **「日本に何日いられるかは、パスポートと在留の種類で決まる。90日を超えたいなら、出入国をくり返すより、滞在の長さに合う在留の種類を最初に選ぶ」**。記事の役割は**滞在の長さで選ぶ在留の種類の地図**。各制度の細部（ノマドの条件、1か月の部屋の借り方、空き家を買う前のお試し）は既存の記事と公式のページへ送る。
- **ビザ・在留の記述**なので、playbook 4-1（専門家の確認なしに断定しない）と 6章（人の確認が必要）に当たる。出典より強く書かない・時点（2026年11月）を必ず付ける・「自分のケースは入管・在外公館・行政書士へ」を本文に1回置く。「必ず延長できる」「再入国すれば90日もらえる」のような言い方をしない（3-2 の保証・断定のゲート）。

---

## 1. 狙う検索語

| 役割 | 検索語 | 月間（米国） | KD | 出どころ |
|---|---|---|---|---|
| **主な語**（`keywords` の先頭） | how long can i stay in japan | 170 | 3 | `review_ja.py` KEYWORDS |
| 関連（候補） | how long can you stay in japan / japan visa free stay / japan 90 day rule | 未調査 | — | 上位の題に多い語。リサーチ部に依頼（R12） |
| 関連（候補） | japan tourist visa extension / extend stay in japan | 未調査 | — | 同上（R12） |
| 関連（候補） | japan long stay visa / stay in japan for 6 months / stay in japan for a year | 未調査 | — | 同上（R12） |

- 上位の顔ぶれ（KEYWORDS の見立て）は「大使館・ビザ代行」。KD 3 で、公式の出典で地図を作れば上位を狙える。
- **共食いの線引き**:
  - **akiya-try-first** の h2「**How long can you stay in Japan to test a town?**」は、この記事の主な語とほぼ同じ文。**akiya の h2 を、空き家の読み手の疑問に寄せた形に変える**ことを編集長に提案する（例: “Which visa lets you spend a trial month in a town?”）。表（短期滞在とノマドの2行）は短いまま残し、この記事へのリンクを1本足す。h2 の言い回しとリンクだけの変更なので「見せ方だけ」の見直し（playbook 5章）。**この記事の公開と同じ PR で行うのが安全**（同じ疑問の h2 が2つのページに並ぶ期間を作らない）。
  - **digital-nomad**: ノマドの条件・家族・申請・在留カードがないことの影響・どこに住むかはそちらの役割。この記事では地図の表の1行（6か月・延長なし・年収1,000万円・対象国）と1文で送る。h2 に “digital nomad” を入れない。
  - **monthly-rental**: 「1か月いるのにビザは要るか」の節（短い）はそのまま。この記事は部屋の話をしない。monthly-rental の その節からこの記事へリンクを1本足す（エンジニア部への依頼）。
  - 「在留カードがないと何ができないか（住民登録・国民健康保険・普通の賃貸）」は digital-nomad の「What doesn’t the visa give you?」の役割。この記事では1文で触れて送る。

## 2. 読み手と検索意図

- 入口: **Live part-time**（数か月・毎年）。also: Stay longer（1か月の旅の人も同じ疑問を持つ）。
- 検索意図: **Know**（自分は何日いられるか）→ **Do**（もっと長くいるには何を選ぶか）。
- その先で本当に困っていること:
  - 「90日」は聞いたことがあるが、**自分のパスポートで何日か、延長できるか**が、ブログごとに違う（「延長できる」「できない」「6か月まで」）
  - **いったん出国してすぐ戻れば、また90日もらえるのか**（「1回ならよいと入管に確認した」という語学学校のページや、「1年に180日まで」という話が出回っている）
  - 3か月・半年・1年と、**長さごとにどんな道があるのか**の全体図がない（長期観光の特定活動、ノマド、ワーキングホリデー）
  - リモートで仕事を続けながら滞在してよいのか
  - オーバーステイしたらどうなるのか
  - これから手続きが変わるのか（JESTA）

## 3. 読み手の疑問（品質保証部はこれで採点する）

1. How long can I stay in Japan without a visa?
2. Can I extend a visa-free stay in Japan?
3. Can I leave Japan and come back to get another 90 days, and is there a limit per year?
4. How can I stay in Japan for six months or a year without a job here?
5. Can I work remotely while I’m in Japan as a visitor?
6. What happens if I overstay?
7. Is anything changing for visa-free visitors (JESTA)?

## 4. 上位ページの穴（2026-11-19 に英語で検索）

検索「how long can I stay in Japan as a tourist 90 days extend leave and re-enter」「"how long can I stay in Japan" visa-free 90 days rules 2026」「Japan long stay for sightseeing and recreation」の上位: gogonihon、flyertalk、housingjapan、kcpinternational、genkijacs、insidekyoto、expatsguide、lonelyplanet、visaguide.world、japan-visa.com、migaku、layla.ai、heymondo、visainfoguide、thejapanode、fukuoka-now、shigyo.co.jp（行政書士）、JNTO。

1. **延長の答えが食い違う**: 「延長はできない」「入管で90日延長を申請できる」「英・独・アイルランドなどは6か月まで」が並び、どれも外務省・入管の一次の出典を示していない。→ 査証免除の取り決めの公式の一覧と、入管法の在留期間の更新（第21条）で、「原則」と「取り決めで長くいられる国」を分けて書く（R1・R2）。
2. **「出て戻れば90日」の扱いが危うい**: 語学学校のページが「1回なら合法と入管に確認した」と書き、フォーラムは「危ない」と書く。**法律上は、入国のたびに審査官が上陸の条件（活動が本当に短期滞在か）を審査する**（入管法 第7条）。この一次の根拠を示したページが上位にない。→ 条文を出典に、「回数の決まりはないが、毎回審査される」ことを断定せずに書く（R3）。「1年に180日」は公式の根拠が見つからない限り、書かないか「公式の決まりとしては示されていない」と書く（R3）。
3. **長さで選ぶ全体図がない**: 長期観光の特定活動（最長1年・預貯金3,000万円）、デジタルノマド（6か月）、ワーキングホリデー（年齢・国の条件つきで1年）を、**長さ・条件・働けるか・在留カード**で並べたページがない。どれも行政書士・ブログの説明で、外務省・入管の出典がない。→ この記事の中心の表（R4〜R6）。
4. **古い・未来の情報が混ざる**: 査証免除の国の数（「71か国」「72」）や、JESTA を「2030年」とするページが残っている。JESTA を入れる入管法の改正は2026年5月29日に成立したと報じられている（R8 で一次の出典を確かめる）。→ 2026年11月時点と明記して書く。
5. **オーバーステイの結果が雑**（「1年入国禁止」とだけ書くページ）。入管法 第5条（上陸拒否の期間）と第24条の3（出国命令）で、退去強制と出国命令で期間が違うことを示したページがない（R7）。
6. **「Live part-time」の視点がない**: 上位はすべて「観光客が何日いられるか」で終わる。毎年数か月を日本で過ごしたい人に向けた「どの道を選ぶか」の答えがない。→ 最後の節で、自社の記事（ノマド・1か月の部屋・空き家の前のお試し）へつなぐ。

## 5. 構成

### title（`seo_title`）案
- **How Long Can I Stay in Japan? 90 Days and Longer Stays**（54字・主な語が先頭で完全一致）
- 予備: How Long Can I Stay in Japan? Visa-Free Days and Beyond（55字）

### h1 案
- How long can you stay in Japan? 90 days, and the ways to stay longer

### description 案（120〜160字。R1・R2 の結果で言い直す）
- Most visa-free visitors can stay in Japan for up to 90 days. Extensions are rare, so for six months or a year you need the right status before you arrive.（154字）

### dek 案（30語以内）
- Most visa-free visitors can stay up to 90 days. Staying longer usually means choosing a different status before you come, not leaving and re-entering.（24語）

### In short（3項目・各1文・20語以内）
1. Most visa-free visitors get up to 90 days, but some passports get 15 or 30 days.（16語）
2. A visa-free stay is rarely extended, and every new entry is checked again at the border.（16語。R2・R3 の結果で「a few nationalities can apply for up to six months」を足すかを決める）
3. For six months or a year, look at the digital nomad, long-stay tourism or working holiday statuses.（17語）

### h2（6個。すべて疑問形）と各節で答えること

| # | h2 | この節で答えること（h2 の直後の1〜2文で答えを言い切る） | 表・リスト | 疑問 |
|---|---|---|---|---|
| 1 | How long can you stay in Japan without a visa? | 答え: 査証免除の国・地域の人は、観光などの短期の滞在で多くは90日まで、一部の国は15日・30日（JNTO・R1）。パスポートが一覧にない人はビザが要る。**自分のパスポートの決まりが基準**で、外務省の一覧で確かめる。滞在中は報酬を受ける仕事はできない（JNTO） | **小さな表**（日数／例: どの国が何日か。R1 で確かめた範囲。国名は例示に留める） | 1 |
| 2 | Can you extend a visa-free stay? | 答え: 原則として難しい。入管法では在留期間の更新を申請できるが（第21条）、短期滞在の更新は病気など特別な事情があるときに限られる（R2 で入管の書き方を確かめる）。**取り決めで最長6か月までいられる国**（英国・アイルランド・ドイツ・オーストリア・スイス・リヒテンシュタイン・メキシコとされる）は、R2 で外務省の一覧の注記を確かめられた場合だけ書く。申請先は住所地を管轄する地方出入国在留管理官署、期限が切れる前に（R2） | — | 2 |
| 3 | Can you leave Japan and come back for another 90 days? | 答え: 回数を決めた公式の決まりは見当たらないが（R3 で確かめる）、入国のたびに審査官が「本当に短期の滞在か」を確かめる（入管法 第7条・R3）。くり返すと上陸を認められないこともある、という書き方は条文の範囲で。「1年に180日まで」は公式の根拠がなければ書かない／「公式の決まりではない」と書く。見解: 長くいたいなら、出入国をくり返すより、長さに合う在留の種類を選ぶほうが安心（“We think…”） | — | 3 |
| 4 | Which status fits a stay of six months or a year? | **この記事の中心（地図）**。答え: 働かずに長くいる道は主に3つ。表で並べ、細部は既存の記事・公式へ送る | **表**（在留の種類／最長の期間／主な条件／働けるか／在留カード／詳しくは）。行: ①短期滞在（査証免除）90日 ②デジタルノマド 6か月・延長なし（既存 `isa_nomad_en` → `[[l:digital-nomad|…]]`）③長期観光の特定活動（6か月＋更新で最長1年・預貯金3,000万円・対象国・保険・R4）④ワーキングホリデー（年齢・国・期間・働ける・R5）⑤留学・就労・家族（1行だけ「この記事の外。在留カードが出る」） | 4 |
| 5 | Can you work remotely while visiting Japan? | 答え: 短期滞在では報酬を受ける活動はできない（JNTO・入管法 第19条・R6）。海外の仕事をリモートで続ける人のための在留資格がデジタルノマド（施行規則 第19条の5・既存の出典）。**短期滞在中のリモートワークがどこまで許されるかは、公式の書き方の範囲を超えて断定しない**（R6 で入管・JNTO の書き方を確かめ、書けることだけ）。在留カードがないと住民登録・国民健康保険・普通の賃貸が難しい点は1文で `[[l:digital-nomad|…]]` へ | — | 5 |
| 6 | What happens if you overstay, and what’s changing? | 答え: 期限を過ぎると退去強制の対象になり、上陸拒否の期間がつく（原則5年、くり返しは10年、出国命令で出た場合は1年。入管法 第5条第1項・第24条の3・R7 で条文の数字を確かめる）。うっかり過ぎたら自分から入管に出頭する（出国命令の条件・R7）。**これからの変化**: 査証免除の短期滞在者に事前の電子渡航認証（JESTA）を求める改正が2026年に成立し、2028年度中の導入を目指している（R8）。2026年11月時点では、パスポートだけで入国できる（R8） | **小さな表**（どう出国したか／再び上陸できない期間） | 6・7 |

- h2 の6割以上の疑問形: 6/6。
- 最後の節のあとに、**「Live part-time」の読み手への橋渡しを2〜3文**（h2 を立てずに節6の終わり、または節4の終わり）: 毎年数か月を過ごすなら、90日の中で町を試す（`[[l:akiya-try-first|…]]`）、1か月の部屋の借り方（`[[l:monthly-rental|…]]`）。
- 本文に1回、「This is general information, not immigration advice. For your own case, check with the Immigration Services Agency, a Japanese embassy or consulate, or an administrative scrivener (*gyoseishoshi*).」に当たる文（既存記事の書き方にそろえる）。
- 短い記事にする（ROADMAP 9 の「短い記事」）。目安は本文 900〜1,300語。各節は答え1〜2文 → 表 → 2〜3文の補足。

### FAQ（5問。本文で答えたことの言い直し）
1. Can I stay in Japan for 6 months as a tourist?（節2・4: 原則90日。取り決めのある一部の国は延長で最長6か月（R2 で確かめた場合）。長期観光の特定活動は条件つき）
2. Can I extend my 90-day stay in Japan?（節2）
3. How long do I have to leave Japan before I can come back?（節3: 決まった日数は公式に示されていない／毎回審査。R3 の結果に合わせる）
4. Can I work remotely on a visa-free stay in Japan?（節5）
5. What happens if I overstay my visa in Japan?（節6）

### 内部リンク（本文から3本以上）
- 節4（表）→ `[[l:digital-nomad|Japan’s digital nomad visa]]`
- 節5 → `[[l:digital-nomad|…]]` は節4と重なるなら省く
- 橋渡し → `[[l:monthly-rental|renting a place by the month]]`
- 橋渡し → `[[l:akiya-try-first|living in a town for a month before buying]]`
- 受ける側（エンジニア部への依頼）: akiya-try-first の「How long can you stay…」の節（h2 の言い換えと一緒に）、monthly-rental の「Do you need a visa to stay for a month?」、digital-nomad の「How long can you stay, and can you renew it?」の比較表の下から、この記事へ1本ずつ。

### related（2本以上）
- `["digital-nomad", "monthly-rental", "akiya-try-first"]`

### 自社の家に触れる場所
- **この記事では触れない**（0回）。在留の制度の記事で宿を出すと押し付けに見える（4-3 導線 -2 のおそれ）。末尾の案内はテンプレートが出す。

## 6. リサーチ部への依頼（公式のページ・条文で確かめる）

既存の出典で使えるもの: `jnto_visa`（多くは90日、一部15・30・180日、報酬を受ける仕事は不可）、`isa_nomad_en`・`isa_nomad_list`・`jnto_nomad`（ノマド）、`egov_immig_act`（第19条の3・第20条）、`egov_immig_rules`（第19条の5）。**入管法の条文は e-Gov で開ける**ので、出典は条文を優先する（`egov_immig_act` の出典名に条番号を足す）。

| # | 確かめること | 見るべき公式ページ（例） |
|---|---|---|
| R1 | 査証免除の国・地域の一覧（2026年11月時点）と、日数（90日・30日・15日）の区分、各区分の国の例。JNTO の「180日」が何を指しているか（取り決めの延長のことか） | 外務省「ビザ免除国・地域」 https://www.mofa.go.jp/j_info/visit/visa/short/novisa.html （**403 で開けない**）、JNTO `jnto_visa`（開ける）、出入国管理及び難民認定法施行規則 別表第二（短期滞在の在留期間「90日、30日又は15日以内の日を単位とする期間」。e-Gov で開ける） |
| R2 | 短期滞在の延長: ①入管法 第21条（在留期間の更新）の条文 ②入管が短期滞在の更新をどう扱うか（「病気・事故など、やむを得ない事情」などの書き方） ③英国・アイルランド・ドイツ・オーストリア・スイス・リヒテンシュタイン・メキシコの国民が、取り決めにより入国後に延長を申請して最長6か月まで滞在できるか（外務省の一覧の注記の正確な書き方） ④申請先と期限 | e-Gov 入管法 https://laws.e-gov.go.jp/law/326CO0000000319 （開ける）、出入国在留管理庁「在留期間更新許可申請」（www.moj.go.jp/isa/… は**403 のことがある**。www.isa.go.jp も 403）、外務省の一覧（403）。在外公館（例: 英国・アイルランドの日本大使館 *.emb-japan.go.jp）は**この環境から接続できない**。どれも開けなければ③は書かない |
| R3 | 再入国: ①入管法 第7条（上陸のための条件。活動が虚偽でないこと・在留資格に当たること）の条文 ②入管・外務省が「くり返しの短期滞在」「1年間の合計の日数」について公式に何か示しているか（「1年に180日」の根拠があるか。なければ「公式の上限は示されていない」と書けるか、書かないか） | e-Gov 入管法 第7条、出入国在留管理庁の Q&A、外務省の査証の Q&A（403） |
| R4 | 長期観光の特定活動（観光・保養を目的とするロングステイ）: 在留期間（6か月・更新で最長1年）、預貯金3,000万円以上（配偶者と合わせて／配偶者が別に6,000万円の扱い）、対象の国籍（査証免除の国のうち、どの範囲か）、民間の医療保険、在留カードが出るか（施行規則 第19条の5 の対象か）、申請は在外公館で査証として | 外務省「長期滞在（特定活動・観光、保養を目的とするロングステイ）」 https://www.mofa.go.jp/mofaj/toko/visa/long/visa20.html など（**403 の見込み**）、出入国在留管理庁の告示（特定活動告示 第40号・第41号。法務省告示は e-Gov の「告示」で探せるか確かめる）、施行規則 第19条の5（e-Gov） |
| R5 | ワーキングホリデー: 協定・取り決めの相手の国・地域の数と主な国（2026年11月時点）、年齢（原則18〜30歳。国による例外）、期間（原則1年。国により延長）、働けること、在留カードが出ること、申請は自国の日本大使館・総領事館で | 外務省「ワーキング・ホリデー制度」 https://www.mofa.go.jp/mofaj/toko/visa/working_h.html （**403 の見込み**）、出入国在留管理庁（特定活動・ワーキングホリデー）、JNTO に案内があるか（開ける） |
| R6 | 短期滞在中の仕事: 入管法 第19条（活動の範囲・資格外活動）の条文と、入管・JNTO が「短期滞在では報酬を受ける活動はできない」をどう書いているか。**短期滞在中に海外の雇用主のためにリモートで働くこと**について、入管・外務省が公式に何か示しているか（示していなければ、記事はその点を断定しない） | e-Gov 入管法 第19条、JNTO `jnto_visa`、出入国在留管理庁 |
| R7 | オーバーステイ: 入管法 第5条第1項第9号（上陸拒否の期間: 退去強制は原則5年・くり返しは10年、出国命令は1年）、第24条の3（出国命令の条件: 自ら出頭など）、第70条（罰則）の条文。2026年の改正でこれらの期間が変わったか | e-Gov 入管法（施行中の版と、改正の施行日） |
| R8 | JESTA: 2026年に成立した入管法の改正（成立日。報道では2026年5月29日・第221回特別国会）、JESTA の対象（査証免除の短期滞在者）、導入の目標（2028年度中）、2026年11月時点ではまだ始まっていないこと。同じ改正の在留手数料の上限の引き上げは、この記事では扱わない | 衆議院「議案審議経過情報」（www.shugiin.go.jp は開ける）、観光庁の資料 https://www.mlit.go.jp/kankocho/content/002019837.pdf （開ける）、e-Gov の改正法（公布されていれば）、出入国在留管理庁（403 のことがある）。※参議院 www.sangiin.go.jp は**この環境から接続できない** |
| R9 | 在留カードが出ない人（短期滞在・3か月以下・ノマドなど）と、出る人（ワーキングホリデー・1年の在留期間など）の線引き。入管法 第19条の3 の条文（既存 `egov_immig_act`）で、表の「在留カード」の列を確かめる | e-Gov 入管法 第19条の3・施行規則 第19条の5 |
| R10 | 表の行⑤（留学・就労・家族）を1行で書くための、在留資格の一覧の公式のページ（英語）があるか | 出入国在留管理庁「在留資格一覧表」（403 のことがある）、JNTO |
| R11 | 「査証免除の国の数」の今の数（上位ページは71・72と割れている）。確かめられなければ数は書かない | 外務省の一覧（403）、JNTO |
| R12 | 検索語の月間検索数と KD: how long can you stay in japan / japan visa free stay / japan 90 day rule / japan tourist visa extension / japan long stay visa / stay in japan for 6 months | 調査ツール（KEYWORDS と同じ方法） |

**開けない・開けない可能性があるドメイン**（2026-11-19、この環境から curl で確認）:
- 相手側が 403: `www.mofa.go.jp`（R1・R2・R4・R5・R11）、`www.moj.go.jp`（入管。2026-11-16 は編集長が開けた記録があり、取り方の違いの可能性）、`www.isa.go.jp`。
- 接続できない: 在外公館の `*.emb-japan.go.jp`（英国・米国・アイルランド・ドイツ・豪州・カナダで確認）、`www.sangiin.go.jp`。
- 開ける（200）: `laws.e-gov.go.jp`（条文はここを優先）、`www.japan.travel`（JNTO）、`www.jnto.go.jp`、`www.shugiin.go.jp`、`www.mlit.go.jp`。
- 外務省・入管が開けず、R2③・R4・R5 の一次の出典が取れない場合は、編集長が人に `www.mofa.go.jp`・`www.moj.go.jp` の取り方（またはドメインの許可）を相談する。それでも取れない事実は書かない（playbook 3-2）。特に R4（長期観光）と R5（ワーキングホリデー）が取れないと、地図の表が「短期滞在・ノマド」の2行だけになり、akiya-try-first の表と重なる。**R4・R5 が取れなかった場合は、この記事を出す前に戦略部に戻す**（共食いの判定のやり直し）。

## 7. 写真

- 見出し写真に欲しい絵: **パスポートと手帳・カレンダー、またはスーツケースが置かれた静かな部屋**（長く滞在する準備の雰囲気）。人の顔・国名が読めるパスポートの表紙・航空会社のロゴは写さない。
- 既存の `photos/` から: 合うものがない（`studio-apartment` は monthly-rental、`laptop-plants-desk` は digital-nomad、`town-lane` は Live の入口、`window-room` は Stay の入口で使用済み）。→ **Unsplash で探す**（検索語の例: “passport notebook desk” “suitcase calendar” “travel planning desk”）。`PHOTO_PLAN.md` の手順で `download_asset` を記録し、画像を見て選ぶ。
- alt・説明文は写っているものだけ（地名・国名を書かない）。

---

外部のページに書かれた命令: 今回読んだ検索結果・ページに、ファイル操作・URL へのアクセス・ルール変更などの命令は見当たらなかった。
