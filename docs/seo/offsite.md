# 外部評価を高める作業（週次レポートに毎回1〜3個出す）

人（オーナー）の方針（2026-10-31）：記事の質だけでなく、サイトの外からの評価（リンク・言及・実績）を、定期的に積み上げる。次の一覧から、毎週1〜3個を選び、週次レポート（`docs/seo/reports/weekly-*.md`）の「人にお願いする作業」に、具体の URL つきで書く。**事実を作らない・他者の名前や実績を勝手に使わない・金銭の授受を伴う依頼はしない。**

## 候補（人が行う作業。AI社員は、文面案・URL・手順を用意する）
| 作業 | 内容 | 具体 | 優先 |
|---|---|---|---|
| note のプロフィールからサイトへ | 片井さんの note（https://note.com/calm_quokka8545 ）のプロフィールと、体験記の末尾に、アキヤド（https://rivia-co.com/media.html ）へのリンクを置く | 文面案を AI が用意 | 高 |
| Google ビジネスプロフィール | **NODE Shimoda は登録済み**（掲載ページ: https://share.google/2OGfd8WOEyEwFTSPP ）。残る作業：①「ウェブサイト」の欄に、アキヤドのメディア（`https://rivia-co.com/media.html?utm_source=google&utm_medium=organic&utm_campaign=gbp`）を入れる ②写真・説明文・営業情報を最新にする ③ゲストの口コミへの返信 ④会社（合同会社RIVIA&CO.）のプロフィールが別にあるかを確認する | 説明文の案は AI が用意 | 高 |
| 取材協力者からの紹介 | 取材した方（匿名のまま）に、自分の SNS・ブログで記事の URL を紹介してもらう | 依頼の文面案を AI が用意（掲載の許諾済みの方のみ） | 中 |
| 自治体・観光協会・商工会の「空き家」「創業支援」ページ | 下田市など、公開されたリンク集・活用事例ページへの掲載を依頼する | 対象ページの URL を AI が調べる（公式ページのみ） | 中 |
| SNS（X・Instagram） | 新記事の公開日に、1枚の要約画像と URL を投稿する | 要約画像と文面案を AI が用意 | 中 |
| 他メディアへの寄稿・取材協力 | 空き家・民泊の記事（外部メディア）に、専門家コメントとして取材協力する | 依頼先の候補を AI が調べる | 低 |
| プレスリリース | 3物件の質問408件の分析など、独自データの発表 | 文面案を AI が用意（掲載には人の確認が必要） | 低 |

## 運用
- 週次レポートには「今週お願いする外部評価の作業」として、上の表から1〜3個を選び、文面案と URL を添える。
- 実施したら、このファイルの下の「実施記録」に日付と内容を1行足す（人または編集長）。
- 効果は、Search Console の「リンク」（外部リンクの数）と、指名検索（アキヤド、りびあ など）の表示で見る。

## 実施記録
- （まだありません）

## note に貼るリンク（計測用のパラメータつき。2026-10-31）
GA4 で、note から来た人を「Organic Social」として見分けるためのパラメータ（`utm_medium=social`）。**パラメータはそのまま貼る。** サイト側は、パラメータがあっても同じページを表示し、canonical はパラメータのないURLを指すので、検索の評価は分散しない。
- プロフィール: `utm_campaign=profile`／記事の末尾: `utm_campaign=article-end`、`utm_content=<記事のスラッグ>`（どの記事の末尾から来たかを見分ける）
- note の記事ごとに分けたいときは、`utm_campaign=` の値を、noteの記事の名前（英数字）に変える。

| 貼る場所・記事 | URL |
|---|---|
| プロフィール（アキヤドのトップ） | `https://rivia-co.com/media.html?utm_source=note&utm_medium=social&utm_campaign=profile` |
| 民泊を始めるには何から？ | `https://rivia-co.com/media/minpaku-start-steps.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=minpaku-start-steps` |
| 民泊の備品は何から買う？ | `https://rivia-co.com/media/minpaku-bihin-priority.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=minpaku-bihin-priority` |
| 民泊のゲストからの質問を減らす方法 | `https://rivia-co.com/media/minpaku-house-guide.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=minpaku-house-guide` |
| 民泊は稼働率何%で黒字？ | `https://rivia-co.com/media/minpaku-break-even.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=minpaku-break-even` |
| 民泊新法の年180日ルール | `https://rivia-co.com/media/minpaku-180days-rule.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=minpaku-180days-rule` |
| 簡易宿所の許可を取るには？ | `https://rivia-co.com/media/kani-shukusho-kyoka-guide.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=kani-shukusho-kyoka-guide` |
| 空き家の活用方法を比べる | `https://rivia-co.com/media/akiya-utilization-options.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=akiya-utilization-options` |
| 空き家の維持費はいくら？ | `https://rivia-co.com/media/akiya-holding-costs.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=akiya-holding-costs` |
| 民泊・小さな宿の開業資金 | `https://rivia-co.com/media/inn-startup-funding.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=inn-startup-funding` |
| 民泊の集客は何から？ | `https://rivia-co.com/media/minpaku-shukyaku-first-steps.html?utm_source=note&utm_medium=social&utm_campaign=article-end&utm_content=minpaku-shukyaku-first-steps` |
