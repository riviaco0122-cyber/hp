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

---

## リサーチメモ（2026-11-20）

リサーチ部。条文は e-Gov 法令 API（`laws.e-gov.go.jp/api/2/`）で、**2026年10月1日施行の版（令和8年法律第32号の一部施行後。e-Gov の「現在施行中」）**を開いて読んだ。外務省（`www.mofa.go.jp`）と入管（`www.moj.go.jp/isa`）は開けなかったので、その2つの中身は「検索結果で確認」にとどまり、**記事には書かない**扱いにした（3-2）。

### 0. 戦略部に戻すかの判断に必要な結論（R4・R5）

- **R4（長期観光の特定活動）: 一部だけ確かめられた。** 開いた一次の出典（国民健康保険法施行規則 第1条第3号・第4号、e-Gov）で、「法務大臣が定める特定活動のうち、**1年を超えない期間**滞在して**観光・保養**などを行う**18歳以上**の人と、**同行する配偶者**」という区分があることは書ける。入管法 第19条の3・施行規則 第19条の5 から、この区分は在留カードの対象から外れていない（＝3か月を超える期間なら在留カードが出る）ことも条文で言える。**預貯金3,000万円・最初の6か月と更新で最長1年・対象国（査証免除の国）・医療保険・申請先**は、外務省のページを開けず検索結果でしか見ていないので、**書かない**。
- **R5（ワーキングホリデー）: 確かめられなかった。** 外務省（403）・在外公館（プロキシで接続できない）・JNTO（ワーキングホリデーの案内ページは今は visa-info のトップと同じ中身で、説明がない）・e-Gov（条文・規則に載っていない）のどれでも、一次の出典を開けなかった。年齢・期間・国・国の数は**すべて書かない**。
- **判断材料**: 地図の表は、今のままだと「①短期滞在 90日 ②ノマド 6か月 ③観光・保養の特定活動 最長1年（条件は公式へ送る形）」の3行まではできる。ワーキングホリデーの行は作れない。構成案の決まり（R4・R5 が取れなければ戦略部へ戻す）に厳密に当てはめると、**R5 が取れていないので戻す条件に当たる**。ただし、R4 の行が条文で立つので、akiya-try-first の表（短期滞在とノマドの2行）とは中身が分かれる。**在外公館のドメイン（`*.emb-japan.go.jp`）を許可に足せば、R4・R5・R2③ の多くが開けそうなので（下の「開けなかったドメイン」）、まず許可の相談、だめなら戦略部へ戻す**のがよいと考える。

### 1. 事実の表（記事に使ってよいもの）

| # | 事実（英語で1文） | 出典（発行元・資料名・年・URL） | 確認の方法 | いつ時点 |
|---|---|---|---|---|
| R1 | Japan’s immigration rules set the period for a Temporary Visitor at 90, 30 or 15 days (or a number of days up to 90 set for the person). | 法務省令「出入国管理及び難民認定法施行規則」別表第二（第3条関係）・e-Gov https://laws.e-gov.go.jp/law/356M50000010054 | ページ（API）を開いて確認 | 2026-10-01 施行の版 |
| R1 | The Temporary Visitor status covers short stays for sightseeing, recreation, sports, visiting relatives, inspection tours, attending classes or meetings, business liaison and similar activities. | 入管法 別表第一の三（短期滞在）・e-Gov https://laws.e-gov.go.jp/law/326CO0000000319 | 開いて確認 | 2026-10-01 施行の版 |
| R1 | JNTO says passport holders of some countries and regions do not need a visa for stays of 90 days or less for tourism, that most short stays allow up to 90 days, and that some nationalities may be granted 15, 30 or 180 days. | JNTO「Entry into Japan and Visa Information」 `jnto_visa` | 開いて確認 | 2026-11-19 取得 |
| R1 | JNTO says a visitor on a tourist stay cannot do paid work, enrol in long-term education or apply for residency, and points to the Ministry of Foreign Affairs list for which passports are visa-exempt. | `jnto_visa` | 開いて確認 | 2026-11-19 |
| R1 補足 | JNTO の「180日」は、別表第二の短期滞在の期間（最長90日）にないので、**入国時にもらえる日数ではない**。取り決めで延長できる国のことと考えられるが、JNTO はそう書いていない → 記事では「180日」を書かない。 | — | 条文との照合（解釈） | — |
| R2 | A foreign resident may apply to the Minister of Justice to renew their period of stay, and the Minister may grant it only when there are reasonable grounds shown in the documents submitted. | 入管法 第21条第1項〜第3項 | 開いて確認 | 2026-10-01 |
| R2 | If you apply to renew before your period of stay ends and the decision has not been made by then, you may stay until the decision or two months after the old expiry date, whichever comes first — but this does not apply if your period of stay was 30 days or less. | 入管法 第20条第6項（第21条第4項で準用） | 開いて確認 | 2026-10-01 |
| R2 | （書かない）入管は短期滞在の更新を「原則として、人道上のやむを得ない事情など特別な事情（病気の治療など）がある場合に限る」としている。 | 出入国在留管理庁「在留期間更新許可申請」 https://www.moj.go.jp/isa/applications/procedures/16-3.html | **検索結果でのみ確認（403 で開けない）** | 不明 |
| R2③ | （書かない）外務省の一覧の注記で、オーストリア・ドイツ・アイルランド・リヒテンシュタイン・スイス・英国（注8）、メキシコ（注7）は、取り決めで最長6か月までいられ、90日を超えるには入管で延長の申請が要る。 | 外務省「Exemption of Visa」 https://www.mofa.go.jp/j_info/visit/visa/short/novisa.html | **検索結果でのみ確認（403）** | 不明 |
| R3 | At every entry, an immigration inspector must check that the person’s passport is valid, that the activity they plan in Japan is not false and fits a status of residence, and that the requested period fits the rules. | 入管法 第7条第1項第1〜4号 | 開いて確認 | 2026-10-01 |
| R3 | The person applying to land must prove that they meet these conditions. | 入管法 第7条第2項 | 開いて確認 | 2026-10-01 |
| R3 補足 | 入管法・施行規則には、短期滞在の**回数や1年間の合計日数の上限を定めた条文は見当たらなかった**（第7条・別表第二を読んだ範囲）。一方、**在スウェーデン日本大使館のページに「12か月で合計180日まで」とある**と検索結果に出た（開けない）。→ 記事は「1年に180日」を**決まりとして書かない**。同時に「公式の上限はない」とも**書かない**（在外公館が上限を示している可能性があるため）。書けるのは「法律は入国のたびに審査すると定め、自分で立証する」まで。 | 在スウェーデン日本大使館 https://www.se.emb-japan.go.jp/itpr_sv/visa_important_notes.html | 検索結果でのみ（プロキシで接続できない） | 不明 |
| R4 | Japan’s health insurance rules refer to a designated activity for people aged 18 or over who stay up to one year for sightseeing, recreation or similar activities, and to the spouse who comes with them, and exclude both from National Health Insurance. | 厚生労働省令「国民健康保険法施行規則」第1条第3号・第4号・e-Gov `egov_nhi_rules` | 開いて確認 | e-Gov 現在施行中の版（2026-11-20 取得） |
| R4/R9 | A residence card is issued to people with a status of residence except those given three months or less, Temporary Visitors, diplomats and officials, and groups listed in the ordinance. | 入管法 第19条の3 | 開いて確認 | 2026-10-01 |
| R4/R9 | The ordinance’s list of people who get no residence card includes the digital nomad and their family, but not the sightseeing-and-recreation long stay. | 施行規則 第19条の5 | 開いて確認（解釈: 3か月を超えて決定されれば在留カードが出る） | 2026-10-01 |
| R6 | People on statuses in Appended Table I, part 3 (which includes Temporary Visitor) may not run a business that brings in income or do activities for which they receive remuneration, unless they have permission. | 入管法 第19条第1項第2号 | 開いて確認 | 2026-10-01 |
| R6 | A person who clearly does mainly paid work in breach of Article 19(1) can be punished. | 入管法 第70条第1項第4号 | 開いて確認 | 2026-10-01 |
| R6 補足 | **短期滞在中に海外の雇用主のためにリモートで働くこと**について、入管・外務省の公式の見解は見つからなかった。内閣府の資料（地方創生推進事務局、`www.chisou.go.jp`、接続できない）が「海外企業に勤める人がリモートワークしながら観光する場合は短期滞在・最長90日」と書いていると検索結果に出たが、開けない。→ 記事は**断定しない**。書けるのは「短期滞在では報酬を受ける活動はできない（条文・JNTO）」「海外の仕事を続けながら長くいる人向けの在留資格がノマド（施行規則 第19条の5第3号）」まで。 | — | — | — |
| R7 | Staying past your period of stay without renewal or change is a ground for deportation. | 入管法 第24条第4号ロ | 開いて確認 | 2026-10-01 |
| R7 | It is also a crime punishable by up to three years’ imprisonment, a fine of up to ¥3 million, or both. | 入管法 第70条第1項第5号 | 開いて確認 | 2026-10-01 |
| R7 | A person deported from Japan for the first time is generally refused landing for five years from departure, and for ten years if deported before or previously ordered to leave. | 入管法 第5条第1項第9号ハ・ニ | 開いて確認 | 2026-10-01 |
| R7 | A person who left under a departure order is refused landing for one year — but five years if they only declared their intention to leave after the investigation began and want to come back as a Temporary Visitor. | 入管法 第5条第1項第9号ホ・ヘ（第24条の3第1号ロ） | 開いて確認 | **2026-10-01 からの新しい形**（ヘは今回の改正で入った区分。構成案の「出国命令は1年」は、短期滞在で戻りたい人に限り5年の例外がある） |
| R7 | A deportee who left by the date set under Article 52(5) is refused landing for one year, except when they want to return as a Temporary Visitor. | 入管法 第5条第1項第9号ロ | 開いて確認 | 2026-10-01（記事では細かすぎるので省いてよい） |
| R7 | A departure order is available if the overstayer turns up at an immigration office on their own before an investigation starts (or says they will leave before a set notice), has not been deported or ordered to leave before, has no listed criminal convictions, and is sure to leave promptly. | 入管法 第24条の3 | 開いて確認 | 2026-10-01 |
| R7 | 2026年の改正（令和8年法律第32号）は、上の上陸拒否の期間に第9号ロ・ヘを足した（2026-10-01 施行）。ほかの年数（5年・10年・1年）はそのまま。 | e-Gov 改正履歴 https://laws.e-gov.go.jp/api/2/law_revisions/326CO0000000319 | 開いて確認 | 2026-11-20 |
| R8 | The bill to amend the Immigration Control Act (cabinet bill no. 20, 221st Diet) passed the House of Representatives on 28 April 2026 and the House of Councillors on 29 May 2026, and was promulgated on 5 June 2026 as Act No. 32 of 2026. | 衆議院「議案審議経過情報」 https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/keika/1DE1F16.htm | 開いて確認 | 2026-11-20 |
| R8 | The amended Act adds Article 7-2, under which visa-exempt travellers planning a Temporary Visitor stay can give information online in advance and be authorised by the Immigration Services Agency. | 入管法（令和8年法律第32号による改正後・未施行の版）第7条の2・e-Gov https://laws.e-gov.go.jp/law/326CO0000000319/20290331_508AC0000000032 | 開いて確認 | 未施行（e-Gov の注記「令和11年3月31日までの間において政令で定める日」） |
| R8 | The Japan Tourism Agency says this system, called JESTA, is planned to start during fiscal 2028 (April 2028 to March 2029). | 観光庁「電子渡航認証制度（JESTA）の導入に伴う外国人旅行者向け消費税免税制度の確認事務等の見直し」 https://www.mlit.go.jp/kankocho/content/002019837.pdf | 開いて確認 | 2026-11-20 取得 |
| R8 | 2026年11月時点で、第7条の2 は**まだ施行されていない**（e-Gov の状態が UnEnforced）。施行の日は政令で決まり、まだ決まっていない（e-Gov に予定日の記載なし、期限だけ）。 | e-Gov 改正履歴 | 開いて確認 | 2026-11-20 |
| R10 | （書かない）入管の英語の在留資格一覧は開けなかった（403）。行⑤は「留学・就労・家族の在留資格は別の仕組みで、多くは在留カードが出る」を条文（第19条の3）の範囲で1文にとどめる。 | — | — | — |
| R11 | （書かない）査証免除の国・地域の数は、検索結果に「74」と出たが、外務省のページを開けない。**数は書かない**。 | — | 検索結果のみ | — |
| R12 | （未実施）月間検索数・KD を取る道具がこの作業の中で使えなかった。主な語（170・KD 3）だけで進めるか、編集長が別に取る。 | — | — | — |

### 2. 構成案への注意（調べて分かったこと）

- **節2**: 「延長は原則難しい」は、条文（第21条第3項「相当の理由があるときに限り」）までなら書ける。「病気などの特別な事情」は入管のページが開けないので書かない（開ければ書ける）。英・独などの「最長6か月」も書かない。In short 2 の「a few nationalities can apply for up to six months」は**足さない**。
- **節3**: 「回数の決まりは見当たらない」は、**法律（入管法・施行規則）の中に**という限定を付けるなら書ける。「公式の上限はない」とは書かない（大使館のページに180日の記述がある可能性）。
- **節4**: ワーキングホリデーの行は作れない。長期観光の行は「up to one year, 18 or over, a spouse can come too, a residence card is issued, no National Health Insurance; check the conditions with a Japanese embassy」程度。**預貯金の額は書かない**。
- **節6**: 「出国命令は1年」は、**短期滞在で戻りたい人が調査の開始後に申し出た場合は5年**という新しい例外があるので、表は「deported (first time) 5 years／deported again 10 years／departure order 1 year (in some cases 5)」の形にする。罰則（3年以下・300万円以下）を足せる。
- **JESTA**: 「2026年に成立（5月29日）・2026年6月5日に公布・2028年度中の導入を目指す・法律上は2029年3月31日までに政令で決める日に施行・2026年11月時点では始まっていない」まで書ける。

### 3. 新しい出典（`SOURCES_NEW` に入れる形）

```python
"egov_immig_act": ("https://laws.e-gov.go.jp/law/326CO0000000319", "Immigration Control Act", "出入国管理及び難民認定法（e-Gov法令検索）",
                   "Immigration Control and Refugee Recognition Act, Articles 5, 7, 19, 19-3, 20, 21, 24, 24-3, 70 and Appended Table I (e-Gov, version in force 1 October 2026)"),  # 既存キー。正式名だけ条番号を足す
"egov_immig_rules": ("https://laws.e-gov.go.jp/law/356M50000010054", "Immigration Control Act ordinance", "出入国管理及び難民認定法施行規則（e-Gov法令検索）",
                     "Ordinance for Enforcement of the Immigration Control and Refugee Recognition Act, Article 19-5 and Appended Table II (e-Gov, version in force 1 October 2026)"),  # 既存キー。正式名に別表第二を足す
"egov_nhi_rules": 既存キーのまま（第1条第3号・第4号を使う。正式名に条番号を足すなら "Article 1"）
"egov_immig_act_jesta": ("https://laws.e-gov.go.jp/law/326CO0000000319/20290331_508AC0000000032", "Immigration Control Act (amended, not yet in force)",
                         "出入国管理及び難民認定法（令和8年法律第32号による改正後・未施行）（e-Gov法令検索）",
                         "Immigration Control and Refugee Recognition Act as amended by Act No. 32 of 2026, Article 7-2 (e-Gov, not yet in force; checked 20 November 2026)"),
"shugiin_bill221_20": ("https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/keika/1DE1F16.htm", "House of Representatives", "衆議院（議案審議経過情報）",
                       "House of Representatives: Progress of cabinet bill no. 20, 221st Diet session (checked 20 November 2026)"),
"jta_jesta": ("https://www.mlit.go.jp/kankocho/content/002019837.pdf", "Japan Tourism Agency", "観光庁（JESTA の導入に伴う免税制度の見直し）",
              "Japan Tourism Agency: Review of tax-free shopping checks following the introduction of JESTA (2026)"),
```

### 4. 海外の読み手の生の疑問（Reddit・FlyerTalk・JREF・expat フォーラムなど。要約）

- 90日いて隣の国に数日出て、戻ればまた90日もらえるか。何日外にいればよいか（決まった日数を求める声が多い）。
- 出入国をくり返して、入国審査で目的を細かく聞かれた・入国を断られたという体験談があり、自分も断られないか不安。
- 自分の国籍は「90日」なのか「6か月まで延長できる」国なのか、ブログごとに違って分からない。
- 観光で来て、自国の会社の仕事をリモートで続けてよいのか（「グレー」「だめ」「黙認」と答えが割れている）。
- 3か月を超えて、仕事をせずに半年〜1年いる方法はあるか（年齢・貯金の条件で使えない人が多い）。
- 帰りの便が遅れる・病気などで90日を少し過ぎそうなとき、どうすればよいか。
- これから事前の電子申請（JESTA）が要るようになるのか、いつからか。

### 5. 開けなかったドメイン（2026-11-20、この環境から）

**許可に足せば開けそうなもの（プロキシで止められた: CONNECT 403 / 接続 000）**
- `*.emb-japan.go.jp`（在外公館。例 `www.uk.emb-japan.go.jp`・`www.us.emb-japan.go.jp`・`www.ie.emb-japan.go.jp`・`www.se.emb-japan.go.jp`）→ R2③（6か月の国）・R3（180日の記述）・R4（長期観光の条件）・R5（ワーキングホリデー）の多くはここで取れそう。**いちばん効果が大きい**。
- `www.chisou.go.jp`（内閣府 地方創生推進事務局）→ R6（短期滞在中のリモートワークの扱い）
- `www.sangiin.go.jp`（R8 は衆議院で足りたので不要）
- （参考）`www.gov.uk`・`travel.state.gov`・`www.canada.ca` なども止められているが、日本の政府の出典ではないので優先度は低い。

**相手側が拒んでいるもの（403。サーバーは Akamai）**
- `www.mofa.go.jp`（外務省。R1・R2③・R4・R5・R11）。WebFetch は「許可されていないドメイン」として名前解決に失敗し、curl はつながるが相手が 403。
- `www.moj.go.jp`（入管。`www.isa.go.jp` はここへ転送される。R2・R10）。2026-11-15 にはこの環境から取れた記録があり、相手側の自動判定で止められている可能性。

### 6. 外部のページに書かれた命令

今回読んだページ・検索結果に、ファイル操作・URL へのアクセス・ルールの変更などの命令は見当たらなかった。
