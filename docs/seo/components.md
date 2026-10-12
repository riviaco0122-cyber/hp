# 記事の部品（図解中心の構成用）

スマホ1画面（約700字相当）に文章だけが続かないよう、記事本文（`sections` の本文 HTML）で使える部品。CSS は `css/style.css` の末尾にある。記事データの本文にそのまま書く（build.py の変更は不要）。3〜4画面に1回は、どれかを入れる（playbook 2-1）。

部品の中の文は、`<p>` でなく `<span>`・`<div>` を使うものがある。本文の `<p>` の体裁が当たらないようにするため、下の例のとおり書く。

## 1. 要点ボックス（結論1文）
見出し直後の結論や、節の要点を目立たせる。1記事に2つまで。

```html
<div class="callout callout--answer">
<p class="callout__label">結論</p>
<p>空き家率は、住宅の余り具合を表す数字で、宿の需要は表しません。</p>
</div>
```
注意書きは `callout callout--note`（ラベル「注意」）。

## 2. カルーセルカード（横スワイプ）
3〜5枚の短いカード。注意点・ポイント・事例の並びに向く。右端が少し見えて続きが分かる。直後にヒント文を置く。1枚は見出し（15字前後）＋本文（60字前後）に収める。

```html
<div class="carousel" role="group" aria-label="◯◯（横にスワイプ）">
<div class="carousel__card"><span class="carousel__no">注意 1</span><p class="carousel__title">短い見出し</p><p class="carousel__text">本文を60字ほど。</p></div>
<div class="carousel__card"><span class="carousel__no">注意 2</span><p class="carousel__title">短い見出し</p><p class="carousel__text">本文。</p></div>
</div>
<p class="carousel__hint">横にスワイプで続きを見られます</p>
```
PC（900px 以上）では3枚が並んで見える。順番に意味がある手順は、カルーセルでなく `<ol class="steps">`。

## 3. 比較カード（2〜3列）
2つ・3つの選択肢を、同じ項目で比べる。2列は、スマホでは縦に並ぶ。3列（`compare--3`）は、スマホでは横スワイプ。行の左が項目名、右が値（1行に収まる短さ）。長い説明が要るときは表にする。

```html
<div class="compare">
<div class="compare__col"><p class="compare__head">民泊新法</p>
<p class="compare__row"><span>営業日数</span><span>年180日まで</span></p>
<p class="compare__row"><span>手続き</span><span>届出</span></p></div>
<div class="compare__col compare__col--b"><p class="compare__head">旅館業</p>
<p class="compare__row"><span>営業日数</span><span>制限なし</span></p>
<p class="compare__row"><span>手続き</span><span>許可</span></p></div>
</div>
```
3列は `<div class="compare compare--3">` にし、3つめの列に `compare__col--c` を付ける（見出しの下線の色が変わる）。数値は出典と時点を本文に書く。

## 4. 数字ハイライト
大きい数字＋ラベル。3つ（既定）か2つ（`stats--2`）。強調したい1つに `stat--accent`。数字の単位は `<small>` で小さくする。数値・時点・出典は本文に必ず書く（部品だけで出典なしにしない）。

```html
<div class="stats" role="group" aria-label="空き家率の比較">
<div class="stat stat--accent"><span class="stat__num">31.3<small>%</small></span><span class="stat__label">下田市</span><span class="stat__note">全国の約2.3倍</span></div>
<div class="stat"><span class="stat__num">13.8<small>%</small></span><span class="stat__label">全国</span><span class="stat__note">2023年10月時点</span></div>
</div>
```
ラベルは8字、補足（`stat__note`）は12字までに収める（3列のとき1行に収まる）。

## 5. 一覧に出る短い表示名と補足（記事データ）
ガイド・学ぶ・記事一覧のカードは、title でなく次を表示する。title・SEO 用の title タグは変えない。

- `short`：表示名。〜22字。`\n` で2行に分ける（サムネイルの文字にも使う）。
- `blurb`：補足（1行・〜18字）。省略すると `tools/article_blurbs.py`、それも無ければ title の「｜」以降。新しい記事は `blurb="…"` を記事データに書く。
- ガイドの Step は、記事が4本を超えると先頭3本だけ見せて「残りの◯本を見る」で開く（js/main.js）。

## 使い分けの目安
| 見せたいもの | 部品 |
|---|---|
| 結論・要点 | 要点ボックス |
| 3〜5個の注意点・ポイント | カルーセルカード |
| 2〜3つの選択肢の違い | 比較カード（細かい数値の対応は表） |
| 大事な数字 | 数字ハイライト |
| 順番のある手順 | `<ol class="steps">` |
| 地域別・年別の数値表 | `<table class="table">`（列は4つ以内） |
