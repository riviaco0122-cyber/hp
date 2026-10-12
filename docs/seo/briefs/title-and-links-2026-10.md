# title の短縮と内部リンクの追加（設計）

作成: 2026-10-12 企画・マーケ部（設計のみ。記事データ `tools/articles_*.py`・`tools/build.py` はまだ変えていない）
方針: 読み手が「次に知りたいこと」へ迷わず進め、検索結果で何の記事かひと目で分かること。SEO はその結果。

## 0. 材料と現状（2026-10-12 時点）

- `python3 tools/seo_check.py`: エラー 0 ／ 警告 20。記事は 51 本。title が 40 字超は **12 本**（akiya-rate-and-inn の公開日前警告も1件）、ガイド未配置は **3 本**。
- 公開日: `akiya-rate-and-inn` だけ 2026-10-13 公開予定（予約中）。ほか 50 本は公開済み。Search Console は 0 件（2026-10-10 時点）で、title を変えても失う実績はない。変えるなら実績がたまる前の今がいちばん影響が小さい。
- 主キーワードは `docs/seo/keywords.md` の担当記事の行から取った。表のない記事（series 系 22 本）は `article_score` でも「未指定」で、今回の title 対象にはならない（40 字以内）。
- 前半 20 字に主キーワードがない記事は、keywords.md の語で見直した結果 **0 本**（長い 12 本の title は、どれも主キーワードが先頭 12 字以内にある）。対象は長さの超過だけ。
- 本文から他の記事へのリンクが 2 本未満の記事は **36 本**（0 本が 25 本、1 本が 11 本）。`akiya-rate-and-inn` は 7 本、`minpaku-hard-truth` は 5 本あり十分。
- 見出し h2 の形（疑問・結論の形）は、ほとんどの記事が 0/2 点。今回は対象外だが、別の改善候補として末尾に記す。

### title を変えると同時に変わるもの（エンジニア部向け）

記事データの `title` 1 項目が、`<title>`・og:title・記事の h1・JSON-LD の headline・パンくず・一覧のツールチップ・llms.txt・サイト内検索に使われる。`short`（一覧の2行見出し）と一覧カードの補足（`tools/article_blurbs.py` の BLURBS。対象 12 本はすべて定義済み）は**影響を受けない**。URL・公開日・description も変えない。

---

## 1. title の短縮案（12 本）

ルール: 40 字以内（seo_check と同じ `len()`）／主キーワードは先頭に残す／意味と主張は変えない（「なり得る」など断定を避ける語はそのまま）／削るのは言い換えの重なり（「方法」「わかりやすく解説」「〜の考え方」）と、本文・description に残る補足。

| # | slug（公開日） | 主キーワード | 現在の title（字数） | 新しい title（字数） | short への影響 | 削った内容の行き先・注意 |
|---|---|---|---|---|---|---|
| 1 | airdna-revenue-simulation（09-29） | AirDNA ／ 民泊 収益 シミュレーション | AirDNAで小規模宿の収益をシミュレーションする方法｜数字の見方と「再現性」を高める5つのコツ（48） | AirDNAで小規模宿の収益を試算する方法｜数字の見方と再現性を高める5つのコツ（40） | なし | 「シミュレーション」→「試算」。検索語「シミュレーション」は description に残っている（要確認）。字数が上限ぴったりなので「方法｜」を外す第2案: AirDNAで小規模宿の収益を試算｜数字の見方と再現性を高める5つのコツ（37） |
| 2 | akiya-inherited-house-to-inn（09-29） | 実家 空き家 放置 | 実家・祖父母の家を放置するとどうなる？固定資産税を払い続ける人が「小さな宿」を選ぶ理由（43） | 実家を放置するとどうなる？固定資産税の負担と「小さな宿」という選択（33） | なし | 「祖父母の家」は本文・description に残る。「選ぶ理由」→「選択」に変えるため、主張（宿を選ぶ人がいる）は同じ。 |
| 3 | akiya-regional-revitalization（09-29） | 空き家活用 地方創生 | 空き家活用はなぜ地方創生につながるのか？宿泊施設への再生が地域にもたらす4つの循環（41） | 空き家活用はなぜ地方創生につながる？宿への再生がもたらす4つの循環（33） | なし | 「宿泊施設」→「宿」（サイト内の用語に合わせる）。 |
| 4 | case-rental-house-inn-first-year（10-11） | 民泊 運営事例 ／ 小さな宿 初期投資 回収 | 【運営事例】伊豆・下田の賃貸の一軒家を小さな宿に。開業から約14か月で初期投資をほぼ回収した数字の推移（51） | 【運営事例】下田の賃貸一軒家を小さな宿に｜約14か月で初期投資をほぼ回収（36） | なし | 「伊豆」は BLURBS（伊豆・下田の運営事例）と本文に残る。「約14か月」「ほぼ回収」の表現は元のまま（本文の「約98%」と矛盾しない）。 |
| 5 | guest-review-tips（10-11。keywords.md には 12-01 予定の古い表記） | 民泊 レビュー 評価 上げる | レビューの評価を上げる宿のゲスト対応｜予約前から滞在後まで、満足を積み重ねるポイント（42） | 民泊のレビュー評価を上げるゲスト対応｜予約前から滞在後までのポイント（34） | なし | 主キーワードの「民泊」を先頭に入れた。記事は宿全般の話なので、「民泊」を入れて内容がずれないか執筆担当が本文冒頭で確認する。ずれるなら第2案: 宿のレビュー評価を上げるゲスト対応｜予約前から滞在後までのポイント（33） |
| 6 | kominka-renovation-points | 古民家 宿 改修 | 古民家を宿に改修するときのポイント｜残すもの・変えるもの、断熱・水回り・耐震の考え方（42） | 古民家を宿に改修するポイント｜残すもの・変えるもの、断熱・水回り・耐震（35） | なし | 2026-10-10 の meta 改善案（`meta-improvements-2026-10.md`）と同じ案。 |
| 7 | long-stay-guest-equipment | 長期滞在 ゲスト 設備 | 長期滞在・海外のゲストに選ばれる設備と備品｜キッチン・乾燥機・ワークデスク・Wi-Fi（43） | 長期滞在ゲストに選ばれる宿の設備｜キッチン・乾燥機・Wi-Fi・ワークデスク（38） | なし | 「海外の」が title から消える。本文・description に残るか確認し、検索意図（海外ゲスト向け）を弱めるなら第2案: 長期滞在・海外ゲストに選ばれる設備｜キッチン・乾燥機・Wi-Fi（35） |
| 8 | long-stay-travel-demand | 長期滞在 旅行 ／ ワーケーション 二地域居住 | 「暮らすように旅する」長期滞在が広がる理由｜ワーケーション・二地域居住と小さな宿の可能性（44） | 長期滞在旅行が広がる理由｜ワーケーション・二地域居住と小さな宿（31） | なし | 「暮らすように旅する」は H1 に残らなくなる。ブランドの言葉なので、本文冒頭には残す。meta 改善案の「長期滞在が広がる理由｜…と小さな宿の可能性（33）」でも可（その場合「旅行」は入らない）。 |
| 9 | minpaku-fire-safety | 民泊 消防設備 ／ 消防法令適合通知書 | 民泊・小さな宿の消防設備ガイド｜自動火災報知設備・誘導灯・消防法令適合通知書の基本（41） | 民泊・小さな宿の消防設備ガイド｜火災報知設備・誘導灯・適合通知書の基本（35） | なし | 正式名（自動火災報知設備・消防法令適合通知書）は本文・FAQ に残す。title の略称は検索語の揺れとして許容。正式名を残す第2案（meta 案）: 民泊の消防設備ガイド｜自動火災報知設備・誘導灯・消防法令適合通知書（36） |
| 10 | minpaku-vs-ryokan-law（09-29） | 民泊新法 旅館業 違い ／ 簡易宿所 民泊 | 空き家で宿を始めるには？民泊新法と旅館業（簡易宿所）の違い・選び方をわかりやすく解説（42） | 民泊新法と旅館業（簡易宿所）の違い｜空き家で宿を始める選び方（30） | なし | 主キーワードを先頭へ（現在は12字目）。「わかりやすく解説」を削る。 |
| 11 | new-build-vs-used-house-inn（09-29） | 民泊 新築 中古 どっち | 小規模宿は新築と中古どっちがおすすめ？費用・工期・法令・税金の違いから選び方を解説（41） | 小規模宿は新築と中古どっち？費用・工期・法令・税金の違いと選び方（32） | なし | 「おすすめ」を外すだけで意味は同じ。 |
| 12 | shizuoka-yaizu-akiya-inn（10-01） | 静岡市 焼津 空き家 民泊 | 静岡市・焼津の空き家は宿になる？｜有名観光地でなくても収益物件になり得る理由と見極め方（43） | 静岡市・焼津の空き家は宿になる？観光地でなくても収益物件になり得る理由（35） | なし | 「見極め方」は本文 h2 に残る。「有名」を外す。 |

- 12 本はすべて公開済み（09-29〜10-11）。予約中（10-13）の `akiya-rate-and-inn` は 34 字で対象外。keywords.md の「予約中」表記は古い（記事データの公開日はすでに 10-11 以前）。
- 字数は上の表の 12 案すべて 40 字以内であることを `len()` で確認済み。適用時に `python3 tools/seo_check.py` で再確認する。
- 適用後に直す場所: `docs/seo/keywords.md` の担当記事メモ（「title 41 → 短縮を」など）、`docs/seo/briefs/meta-improvements-2026-10.md` の該当行（この設計に置き換えたと注記）。
- 迷う点（人の判断は不要だが、執筆担当が適用時に確認）: #1 の「試算」、#5 の「民泊」、#7 の「海外」、#8 の「暮らすように旅する」。

### 1-2. 今回は変えない記事

- 40 字ちょうどの `small-inn-subsidies`・`akiya-lease-types`・`cleaning-linen-operations`: 超過ではなく、主キーワードも前半にある。
- 主キーワードが 15〜20 字目にある `minpaku-investment-yield`（民泊が15字目）・`akiya-3000man-deduction`（「3,000万円特別控除」が17字目）: 20 字以内。表示が出て順位が分かってから判断する。

---

## 2. 内部リンクの追加案（36 本）

### 2-0. 方針

- 現在の本数は `python3 tools/article_score.py` の「本文から他の記事へのリンク」と、記事データの sections の `href="media/…"` を数えた。0 本の記事に **2〜3 本**、1 本の記事に **1〜2 本**（合計 2〜3 本以上）を足す。
- リンク先は、同じテーマ・同じガイドの次の Step・読み手が次に抱く疑問が近い記事。検索意図が重なる記事（共食い）には張らない（例: `minpaku-vs-ryokan-law` から `minpaku-start-steps` へは「手順は別記事」と案内するだけで、制度の比較は書かない）。
- 文は「◯◯は、別の記事で詳しく説明しています」の形。新しい事実・数値は足さない。リンク文言は、リンク先の `short`（一覧の見出し）か title の一部。
- 置き場所は本文の節（section id）の**末尾の段落の後**に 1 文を足す（段落の途中に差し込まない）。まとめ節（summary）には足さない。
- 書式はサイト内の既存記事と同じ `<a href="media/<slug>.html">…</a>`（先頭に `/` を付けない。既存の `articles_series1.py` に合わせる）。
- 予約中の `akiya-rate-and-inn`（10-13 公開）へは今回張らない（公開日前の記事に張ると、公開日前に飛べるリンクになるため）。公開後の次回に、`shizuoka-yaizu-akiya-inn`・`akiya-regional-revitalization` から張る案がある。
- 「出典を足す」必要はない（案内文だけ）。

記号: 「0本」「1本」は現在の本文リンク数。リンク文言は 「」で示す。

### 2-1. リンク案（全件）

| # | 記事（現在） | 置く節（section id） | 自然な 1 文（リンク文言つき） | リンク先 | 理由（読み手の次の疑問） |
|---|---|---|---|---|---|
| 1 | accommodation-tax（0本） | `operator` | 宿泊税を含めた売上や客室単価の見方は、「<a>稼働率・客室単価・RevPARとは？</a>」で説明しています。 | inn-kpi-basics | 税を取り込んだ売上の見方 |
| 2 | 同上 | `price` | 予約サイトと自社予約での料金の見せ方は、「<a>予約サイト（OTA）と自社予約、どう使い分ける？</a>」で詳しく説明しています。 | ota-vs-direct-booking | 料金表示の場所 |
| 3 | airdna-revenue-simulation（0本） | `example` | 稼働率や客室単価の意味は、「<a>稼働率・客室単価・RevPARとは？</a>」で説明しています。 | inn-kpi-basics | 計算例に出る指標の定義 |
| 4 | 同上 | `limits` | 季節による売上の波への備えは、「<a>閑散期をどう乗り越える？</a>」で説明しています。 | minpaku-off-season | 平均値では見えない波 |
| 5 | akiya-3000man-deduction（0本） | `compare` | 売る以外の活用方法の比べ方は、「<a>空き家の活用方法を比べる</a>」で説明しています。 | akiya-utilization-options | 「売る」と「活かす」の比較の続き |
| 6 | 同上 | `compare` | 貸す場合の契約の違いは、「<a>空き家を貸すときの契約の種類と違い</a>」で説明しています。 | akiya-lease-types | 貸す選択肢 |
| 7 | akiya-bank-guide（0本） | `owner` | 空き家を貸す場合の契約の種類は、「<a>空き家を貸すときの契約の種類と違い</a>」で説明しています。 | akiya-lease-types | 登録後の貸し方 |
| 8 | 同上 | `user` | 物件が宿に向くかの見方は、「<a>その空き家、民泊に向いている？</a>」で説明しています。 | akiya-minpaku-suitability | 探す人の次の疑問 |
| 9 | 同上 | `support` | 宿の開業で使える補助金は、「<a>小規模宿で使える補助金・支援制度まとめ</a>」で説明しています。 | small-inn-subsidies | 自治体支援の次は国の制度 |
| 10 | akiya-lease-types（0本） | `inn` | 運営を任せる場合の管理会社の選び方は、「<a>住宅宿泊管理業者とは？</a>」で説明しています。 | minpaku-management-company | 宿として貸すときの委託先 |
| 11 | 同上 | `inn` | 民泊新法と旅館業の違いは、「<a>民泊新法と旅館業、どちらで始める？</a>」で説明しています。 | minpaku-vs-ryokan-law | 宿として貸す前提の制度 |
| 12 | akiya-regional-revitalization（0本） | `cycles` | お金の流れの詳しい仕組みは、「<a>宿が地域にお金を落とす仕組み</a>」で説明しています。 | inn-local-economy | 「循環」の中身 |
| 13 | 同上 | `success` | 地域と継続的に関わる人を増やす考え方は、「<a>「関係人口」と宿ができること</a>」で説明しています。 | kankei-jinko-and-inns | 3つのポイントの続き |
| 14 | 同上 | `background` | 空き家の数と割合のデータは、「<a>データで見る日本の空き家</a>」で説明しています。 | akiya-data-9-million | 背景の数字の根拠 |
| 15 | akiyado-consultation-flow（0本） | `flow` | アキヤドができることの全体は、「<a>アキヤドができること</a>」で説明しています。 | akiyado-what-we-do | 相談の前に全体像 |
| 16 | 同上 | `ask` | 相談先の比べ方は、「<a>相談先・委託先の選び方</a>」で説明しています。 | minpaku-partner-choose | 他社と比べたい読者 |
| 17 | 同上 | `prepare` | 物件の見極め方は、「<a>その空き家は民泊に向いている？</a>」で説明しています。 | akiya-minpaku-suitability | 準備として自分で確認 |
| 18 | cleaning-linen-operations（0本） | `why` | レビューとの関係は、「<a>民泊のレビュー評価を上げるゲスト対応</a>」で説明しています。 | guest-review-tips | 清潔さ→評価 |
| 19 | 同上 | `staff` | 遠方からの運営の仕組みは、「<a>遠方の物件でも運営できる？</a>」で説明しています。 | minpaku-remote-operation | 清掃の外注とセット |
| 20 | guest-review-tips（0本） | `before` | 掲載ページの写真と紹介文は、「<a>予約が入る宿のページのつくり方</a>」で説明しています。 | listing-photo-tips | 予約前の対応 |
| 21 | 同上 | `stay` | 清掃・リネンの仕組みは、「<a>小さな宿の清掃・リネン運用ガイド</a>」で説明しています。 | cleaning-linen-operations | 滞在中の満足 |
| 22 | inbound-regional-dispersion（0本） | `now` | 訪日客数などの全体データは、「<a>データで見る日本の観光市場</a>」で説明しています。 | japan-tourism-market-data | 数字の根拠 |
| 23 | 同上 | `chance` | 長期滞在の需要は、「<a>長期滞在旅行が広がる理由</a>」で説明しています。 | long-stay-travel-demand | 地方の宿の機会 |
| 24 | 同上 | `chance` | 物件が宿に向くかの見方は、「<a>その空き家、民泊に向いている？</a>」で説明しています。 | akiya-minpaku-suitability | 自分の物件への当てはめ |
| 25 | inn-kpi-basics（0本） | `example` | 収益の試算のしかたは、「<a>AirDNAで読む小規模宿の収益と再現性</a>」で説明しています。 | airdna-revenue-simulation | 指標→試算 |
| 26 | 同上 | `trap` | 季節の波への対応は、「<a>閑散期をどう乗り越える？</a>」で説明しています。 | minpaku-off-season | 稼働率が下がる時期 |
| 27 | 同上 | `use` | 集客チャネルの使い分けは、「<a>予約サイトと自社予約、どう使い分ける？</a>」で説明しています。 | ota-vs-direct-booking | 打ち手 |
| 28 | inn-local-economy（0本） | `akiya` | 空き家活用と地方創生の関係は、「<a>空き家活用が地方創生につながる理由</a>」で説明しています。 | akiya-regional-revitalization | 空き家再生の続き |
| 29 | 同上 | `guide` | 地域との関わりを続ける人については、「<a>「関係人口」と宿ができること</a>」で説明しています。 | kankei-jinko-and-inns | 案内役の先 |
| 30 | japan-tourism-market-data（0本） | `issues` | 人手不足の課題は、「<a>観光業の人手不足をどう乗り越える？</a>」で説明しています。 | tourism-labor-shortage | 5つの課題の1つ |
| 31 | 同上 | `inbound` | 地方への誘客は、「<a>訪日客を地方へ</a>」で説明しています。 | inbound-regional-dispersion | 数字の次の動き |
| 32 | 同上 | `opportunity` | 長期滞在の広がりは、「<a>長期滞在旅行が広がる理由</a>」で説明しています。 | long-stay-travel-demand | 滞在型観光の詳細 |
| 33 | kankei-jinko-and-inns（0本） | `inn` | 宿の経済効果は、「<a>宿が地域にお金を落とす仕組み</a>」で説明しています。 | inn-local-economy | 関係人口→経済 |
| 34 | 同上 | `why` | 空き家活用と地方創生は、「<a>空き家活用が地方創生につながる理由</a>」で説明しています。 | akiya-regional-revitalization | 注目の背景 |
| 35 | kominka-renovation-points（0本） | `law` | 消防設備の基準は、「<a>民泊・小さな宿の消防設備ガイド</a>」で説明しています。 | minpaku-fire-safety | 設計への反映の続き |
| 36 | 同上 | `water` | 遠方からの工事の進め方は、「<a>遠方からの改修工事の進め方</a>」で説明しています。 | remote-renovation-tips | 発注の注意 |
| 37 | 同上 | `concept` | 古い家が宿として選ばれる理由は、「<a>古い家だからこそ価値になる</a>」で説明しています。 | kominka-stay-value | 残すものの根拠 |
| 38 | listing-photo-tips（0本） | `review` | レビューを上げるゲスト対応は、「<a>民泊のレビュー評価を上げるゲスト対応</a>」で説明しています。 | guest-review-tips | 返信の次 |
| 39 | 同上 | `price` | 集客チャネルの使い分けは、「<a>予約サイトと自社予約、どう使い分ける？</a>」で説明しています。 | ota-vs-direct-booking | 掲載先 |
| 40 | long-stay-travel-demand（0本） | `needs` | 設備の考え方は、「<a>長期滞在ゲストに選ばれる宿の設備</a>」で説明しています。 | long-stay-guest-equipment | 求めるもの→設備 |
| 41 | 同上 | `inn` | 閑散期への備えは、「<a>閑散期をどう乗り越える？</a>」で説明しています。 | minpaku-off-season | 長期滞在が支える稼働 |
| 42 | 同上 | `why` | 地方への誘客の動きは、「<a>訪日客を地方へ</a>」で説明しています。 | inbound-regional-dispersion | 背景 |
| 43 | minpaku-fire-safety（0本） | `process` | 開業までの全体の手順は、「<a>民泊を始めるまでの7ステップ</a>」で説明しています。 | minpaku-start-steps | 消防→全体 |
| 44 | 同上 | `type` | 古い建物の改修の考え方は、「<a>古民家を宿に改修するポイント</a>」で説明しています。 | kominka-renovation-points | 建物の使い方→改修 |
| 45 | 同上 | `why` | 民泊新法と旅館業の違いは、「<a>民泊新法と旅館業、どちらで始める？</a>」で説明しています。 | minpaku-vs-ryokan-law | 制度で設備が変わる |
| 46 | minpaku-management-company（0本） | `when` | 相談先・委託先の比べ方は、「<a>相談先・委託先の選び方</a>」で説明しています。 | minpaku-partner-choose | 管理会社以外も含め比較 |
| 47 | 同上 | `tasks` | 清掃・リネンの仕組みは、「<a>小さな宿の清掃・リネン運用ガイド</a>」で説明しています。 | cleaning-linen-operations | 業務の中身 |
| 48 | 同上 | `choose` | 遠方からの運営の仕組みは、「<a>遠方の物件でも運営できる？</a>」で説明しています。 | minpaku-remote-operation | 任せる体制 |
| 49 | minpaku-vs-ryokan-law（0本） | `flow` | 開業までの全体の手順は、「<a>民泊を始めるまでの7ステップ</a>」で説明しています。 | minpaku-start-steps | 制度→手順 |
| 50 | 同上 | `pitfall` | 消防設備については、「<a>民泊・小さな宿の消防設備ガイド</a>」で説明しています。 | minpaku-fire-safety | 失敗の代表 |
| 51 | 同上 | `choose` | 運営を任せる管理会社については、「<a>住宅宿泊管理業者とは？</a>」で説明しています。 | minpaku-management-company | 民泊新法の次 |
| 52 | new-build-vs-used-house-inn（0本） | `used` | 古民家の改修のポイントは、「<a>古民家を宿に改修するポイント</a>」で説明しています。 | kominka-renovation-points | 中古を選んだ後 |
| 53 | 同上 | `used` | 空き家の探し方は、「<a>空き家バンクの仕組みと使い方</a>」で説明しています。 | akiya-bank-guide | 中古の入手 |
| 54 | 同上 | `tax` | 資金の用意の仕方は、「<a>小さな宿の開業資金はどう用意する？</a>」で説明しています。 | inn-startup-funding | 融資の続き |
| 55 | ota-vs-direct-booking（0本） | `direct` | 掲載ページの作り方は、「<a>予約が入る宿のページのつくり方</a>」で説明しています。 | listing-photo-tips | 自社予約を育てる |
| 56 | 同上 | `ota` | 数字の見方は、「<a>稼働率・客室単価・RevPARとは？</a>」で説明しています。 | inn-kpi-basics | OTA経由の成果の測り方 |
| 57 | 同上 | `step` | レビューへの対応は、「<a>民泊のレビュー評価を上げるゲスト対応</a>」で説明しています。 | guest-review-tips | 段階的な運営 |
| 58 | shizuoka-yaizu-akiya-inn（0本） | `check` | 物件ごとの見極め方は、「<a>その空き家、民泊に向いている？</a>」で説明しています。 | akiya-minpaku-suitability | チェックの続き |
| 59 | 同上 | `demand` | 地方への誘客の動きは、「<a>訪日客を地方へ</a>」で説明しています。 | inbound-regional-dispersion | 需要の裏付け |
| 60 | 同上 | `merit` | 制度の違いは、「<a>民泊新法と旅館業、どちらで始める？</a>」で説明しています。 | minpaku-vs-ryokan-law | 始め方 |
| 61 | small-inn-subsidies（0本） | `caution` | 資金全体の組み合わせは、「<a>小さな宿の開業資金はどう用意する？</a>」で説明しています。 | inn-startup-funding | 補助金だけでは足りない |
| 62 | 同上 | `local` | 空き家の探し方は、「<a>空き家バンクの仕組みと使い方</a>」で説明しています。 | akiya-bank-guide | 空き家改修補助の前提 |
| 63 | tourism-labor-shortage（0本） | `dx` | 遠方からの運営の仕組みは、「<a>遠方の物件でも運営できる？</a>」で説明しています。 | minpaku-remote-operation | 業務の効率化 |
| 64 | 同上 | `keep` | 清掃・リネンの仕組みは、「<a>小さな宿の清掃・リネン運用ガイド</a>」で説明しています。 | cleaning-linen-operations | 業務の仕組み化 |
| 65 | 同上 | `why` | 地域と関わる人については、「<a>「関係人口」と宿ができること</a>」で説明しています。 | kankei-jinko-and-inns | 人材の入口 |

（上は 0 本の 25 本分。#1〜2 は accommodation-tax、…と記事ごとに 2〜3 件。リンク文言は目的の記事の `short` を使い、句点の前に置く。）

#### 1 本あるものの追加（11 本）

| # | 記事（現在の本文リンク） | 置く節 | 自然な 1 文 | リンク先 |
|---|---|---|---|---|
| 66 | akiya-holding-costs（utilization-options） | `reduce` | 売ったときの税金の特例は、「<a>相続した空き家を売るときの3,000万円特別控除</a>」で説明しています。 | akiya-3000man-deduction |
| 67 | 同上 | `hidden` | 管理不全空家と固定資産税の特例は、「<a>空家法の改正で何が変わった？</a>」で説明しています。 | akiya-law-kanri-fuzen |
| 68 | inherited-house-family-talk（akiya-lease-types） | `prepare` | 相続登記については、「<a>相続登記の義務化と最初にやること</a>」で説明しています。 | souzoku-touki-gimuka |
| 69 | 同上 | `decide` | 活用方法の比べ方は、「<a>空き家の活用方法を比べる</a>」で説明しています。 | akiya-utilization-options |
| 70 | case-rental-house-inn-first-year（inn-kpi-basics） | `invest` | 資金の集め方は、「<a>小さな宿の開業資金はどう用意する？</a>」で説明しています。 | inn-startup-funding |
| 71 | 同上 | `payback` | 不動産としての見方は、「<a>不動産投資として見る小さな宿・民泊</a>」で説明しています。 | minpaku-investment-yield |
| 72 | inn-startup-funding（small-inn-subsidies） | `plan` | 収益の試算は、「<a>AirDNAで読む小規模宿の収益と再現性</a>」で説明しています。 | airdna-revenue-simulation |
| 73 | 同上 | `breakdown` | 開業までの手順は、「<a>民泊を始めるまでの7ステップ</a>」で説明しています。 | minpaku-start-steps |
| 74 | long-stay-guest-equipment（long-stay-travel-demand） | `invest` | 資金の考え方は、「<a>小さな宿の開業資金はどう用意する？</a>」で説明しています。 | inn-startup-funding |
| 75 | 同上 | `why` | 閑散期への備えは、「<a>閑散期をどう乗り越える？</a>」で説明しています。 | minpaku-off-season |
| 76 | minpaku-investment-yield（airdna-revenue-simulation） | `risk` | 季節の波への備えは、「<a>閑散期をどう乗り越える？</a>」で説明しています。 | minpaku-off-season |
| 77 | 同上 | `compare` | 賃貸との収入の仕組みの違いは、「<a>民泊と賃貸、収入の仕組みの違い</a>」で説明しています。 | minpaku-vs-rental-income |
| 78 | minpaku-neighbor-rules（minpaku-management-company） | `trouble` | 遠方からの運営の仕組みは、「<a>遠方の物件でも運営できる？</a>」で説明しています。 | minpaku-remote-operation |
| 79 | 同上 | `before` | 開業までの手順は、「<a>民泊を始めるまでの7ステップ</a>」で説明しています。 | minpaku-start-steps |
| 80 | minpaku-off-season（airdna-revenue-simulation） | `ideas` | 長期滞在の需要は、「<a>長期滞在旅行が広がる理由</a>」で説明しています。 | long-stay-travel-demand |
| 81 | 同上 | `use` | 清掃・リネンの仕組みは、「<a>小さな宿の清掃・リネン運用ガイド</a>」で説明しています。 | cleaning-linen-operations |
| 82 | minpaku-partner-choose（minpaku-management-company） | `five` | 遠方からの運営の仕組みは、「<a>遠方の物件でも運営できる？</a>」で説明しています。 | minpaku-remote-operation |
| 83 | 同上 | `check` | 借り上げの契約の種類は、「<a>空き家を貸すときの契約の種類と違い</a>」で説明しています。 | akiya-lease-types |
| 84 | minpaku-start-steps（minpaku-vs-ryokan-law） | `fire` | 消防設備については、「<a>民泊・小さな宿の消防設備ガイド</a>」で説明しています。 | minpaku-fire-safety |
| 85 | 同上 | `operation` | 管理会社の選び方は、「<a>住宅宿泊管理業者とは？</a>」で説明しています。 | minpaku-management-company |
| 86 | akiya-inherited-house-to-inn（minpaku-vs-ryokan-law） | `cost` | 維持費の内訳は、「<a>空き家の維持費の内訳と見落としがちな費用</a>」で説明しています。 | akiya-holding-costs |
| 87 | 同上 | `law` | 空家法の改正は、「<a>空家法の改正で何が変わった？</a>」で説明しています。 | akiya-law-kanri-fuzen |

注: 上の表で #1〜#65 の通し番号は 25 記事（0 本の記事）の追加分、#66〜#87 は 11 記事（1 本の記事）の追加分。合計 **87 リンク／36 記事**。1 記事あたり 2〜3 本（akiya-inherited-house-to-inn は 1+2=3 本）。

### 2-2. ガイドに入っていない 3 記事の配置案

`guides=[(key, step)]` を記事データに書く（`tools/build.py` が Step の末尾に並べる）。いずれも編集は `tools/articles_sched2.py` の記事データ。

| slug | 追加する `guides` | 理由 |
|---|---|---|
| japan-tourism-market-data | `[("side", 1)]` | 副業ガイドの Step 1「市場と可能性を知る」の入口。同じ Step に `long-stay-travel-demand`・`inbound-regional-dispersion` がある。 |
| kankei-jinko-and-inns | `[("use", 1)]` | 活用ガイドの Step 1「活かし方を知る」（地域にとっての価値を知る段）。同じ Step に `inn-local-economy`・`akiya-regional-revitalization` がある。 |
| tourism-labor-shortage | `[("side", 4)]` | 副業ガイドの Step 4「運営して、育てる」。同じ Step に `cleaning-linen-operations` などがある。副業で運営する人にとっては人手の確保が運営の一部。 |

ガイドを増やすと、記事末尾の「こんな方に」が出て、ガイドページの記事数も増える。順番は Step 末尾なので既存の並びは変わらない。

---

## 3. 適用の優先順位と、1 回で適用できる件数

### 優先順位

1. **A: title の短縮 12 本（#1〜#12）**。変更が `title` 1 項目だけで、ほかの記事に影響しない。seo_check の警告 12 件がそのまま減る。
2. **B: ガイド未配置の 3 本**。`guides=` の 1 行ずつ。seo_check の警告 3 件が減る。
3. **C: リンク 0 本の記事のうち、ガイドの Step の途中に入る記事から**: 0 本の 25 記事のうち、入口に近い順（読み手の流入が多くなりやすい順）に
   - C1（Step の入口）: `minpaku-vs-ryokan-law`・`akiya-bank-guide`・`akiya-lease-types`・`inn-kpi-basics`・`ota-vs-direct-booking`・`minpaku-management-company`・`minpaku-fire-safety`・`akiya-3000man-deduction`・`shizuoka-yaizu-akiya-inn`・`small-inn-subsidies`（10 記事）
   - C2（残りの 0 本）: `accommodation-tax`・`airdna-revenue-simulation`・`akiya-regional-revitalization`・`akiyado-consultation-flow`・`cleaning-linen-operations`・`guest-review-tips`・`inbound-regional-dispersion`・`inn-local-economy`・`japan-tourism-market-data`・`kankei-jinko-and-inns`・`kominka-renovation-points`・`listing-photo-tips`・`long-stay-travel-demand`・`new-build-vs-used-house-inn`・`tourism-labor-shortage`（15 記事）
4. **D: 1 本あるものの追加 11 記事（#66〜#87）**。すでに最低限の導線があるため最後。ただし `akiya-inherited-house-to-inn` は最も入口に近い記事なので C1 と一緒に先に入れてよい。

### 1 回で適用できる件数の目安

- 1 回の作業（1 PR）で **A（12 本）+ B（3 本）+ C1（10 記事・約 26 リンク）** が目安。`title` と `guides` と本文 1 文の追加だけで、事実・数値・出典・体験は変えない。
- 次の回で **C2（15 記事・約 38 リンク）+ D（11 記事・22 リンク）**。
- 毎回、`python3 tools/build.py` → `python3 tools/seo_check.py`（エラー 0）→ `node tools/check/site_check.js`（重大 0・リンク切れ 0）→ `python3 tools/article_score.py` で該当記事のリンク数 2 本以上を確認。title 変更は一覧ページのカード（`short`・blurb）が崩れていないかスマホ幅で目視。
- これらの変更は「見せ方・案内文の追加」で、既存記事の事実・数値・出典・体験・主張は変えない。title の言い換え（#1 試算、#5 民泊、#7 海外、#8 暮らすように旅する）は、主張を変えない範囲だが、最終確認は人に出す（定期実行の PR なら人を通す）。

---

## 4. リスク

- **title の変更**: 公開済み 12 本。Search Console の実績がまだ 0 件なので、失う順位はない。ただし、検索エンジンが認識した title が一度変わるので、反映までに数週間かかることがある。#8 では「暮らすように旅する」、#2 では「祖父母の家」を title から外す。いずれも本文に残る。
- **h1 も同時に変わる**（記事データの `title` を直接使う）。SNS 共有文・パンくずも変わる。
- **リンクの文言**: 同じリンク文言を使い回すと不自然。実装時は、本文の前後の文に合わせて語尾だけ変えてよい（リンク先と文の意味は変えない）。
- **リンクの偏り**: C を全件入れると、`minpaku-vs-ryokan-law`・`inn-kpi-basics`・`minpaku-start-steps`・`minpaku-remote-operation`・`long-stay-travel-demand` へのリンクが多くなる（内部の被リンクが集まる記事は、実際に入口になる重要記事）。逆に、被リンクが少なくなる記事は `akiyado-what-we-do`・`akiya-data-9-million` など。ガイドの Step の並びと矛盾しないが、適用後に被リンク数を集計して偏りを見る。
- **共食いのリスク**: リンク先を「別の記事で説明」に限り、同じ見出しの内容を本文にコピーしない。`minpaku-vs-ryokan-law`（制度）↔`minpaku-start-steps`（手順）、`inn-startup-funding`↔`small-inn-subsidies`（資金）は、役割の違いが記事冒頭に書かれているか適用時に確認する。
- **予約中の記事**: `akiya-rate-and-inn`（10-13 公開）にはリンクを張らない。公開後に張る。
- **meta 改善案との重複**: `meta-improvements-2026-10.md` の title 案（#6・#9 など）と同じ記事を扱う。この設計の案を優先し、適用後に meta 側の該当行を「適用済み」にする。

## 5. 別の改善候補（今回は対象外）

- 見出し h2 の疑問・結論の形（60% 以上）は、`article_score` で満点の記事が一部（akiya-rate-and-inn・minpaku-vs-rental-income・minpaku-management-company・new-build-vs-used-house-inn・ota-vs-direct-booking の5本）にとどまり、多くが 0/2 点。見せ方の書き直し（見出し短縮）として別の回で扱う。
- `docs/seo/keywords.md` の「予約中」表記が古い（実際は 10-11 に公開日が揃っている）。進行管理部が更新する。
