# 実行環境（アキヤド）の許可ドメイン

公式ページの本文を取得して照合するために、環境の「Network access → Custom → Allowed domains」に貼る一覧。1行に1つ。`*.` を付けると配下のサブドメインすべてを許可する。
画面: claude.ai/code → 入力欄の上の雲のアイコン → Cloud → 「アキヤド」の歯車。

## 1. いま登録済み（確認済み。2026-10-12 に接続を試して 200 を確認）

```
www.mlit.go.jp
www.nta.go.jp
www.stat.go.jp
www.soumu.go.jp
www.reinfolib.mlit.go.jp
*.lg.jp
note.com
www.youtube.com
```

## 2. 追加するもの（静岡県内の自治体を網羅するとき）

いちばん簡単なのは、次の1行です（静岡県・県内35市町の公式サイトは、ほぼすべて `*.shizuoka.jp` か `*.lg.jp` の下にあります）。

```
*.shizuoka.jp
www.e-stat.go.jp
```

## 3. 1行で足りないとき用の、市町ごとのドメイン一覧（コピペ用）

次の一覧は、各市町の公式サイトのドメインを、公開されている URL の形から書いたものです。**接続して確かめたものではなく、一部は違う可能性があります**（例: `lg.jp` か `shizuoka.jp` かの違い）。2 の `*.shizuoka.jp` と、すでに登録済みの `*.lg.jp` で、ほとんどは足ります。足りない市町が出たら、ここから該当の行を足してください。

```
city.shizuoka.lg.jp
city.hamamatsu.shizuoka.jp
city.numazu.shizuoka.jp
city.atami.lg.jp
city.mishima.shizuoka.jp
city.fujinomiya.shizuoka.jp
city.ito.shizuoka.jp
city.shimada.shizuoka.jp
city.fuji.shizuoka.jp
city.iwata.shizuoka.jp
city.yaizu.lg.jp
city.kakegawa.shizuoka.jp
city.fujieda.shizuoka.jp
city.gotemba.shizuoka.jp
city.fukuroi.shizuoka.jp
city.shimoda.shizuoka.jp
city.susono.shizuoka.jp
city.kosai.shizuoka.jp
city.izu.shizuoka.jp
city.omaezaki.shizuoka.jp
city.kikugawa.shizuoka.jp
city.izunokuni.shizuoka.jp
city.makinohara.shizuoka.jp
town.higashiizu.shizuoka.jp
town.kawazu.shizuoka.jp
town.minamiizu.shizuoka.jp
town.matsuzaki.shizuoka.jp
town.nishiizu.shizuoka.jp
town.kannami.shizuoka.jp
town.shimizu.shizuoka.jp
town.nagaizumi.shizuoka.jp
town.oyama.shizuoka.jp
town.yoshida.shizuoka.jp
town.kawanehon.shizuoka.jp
town.morimachi.shizuoka.jp
pref.shizuoka.jp
```

## 他県の例を使うとき

県ごとに `*.<県名>.jp` を足す（例: `*.hokkaido.jp`、`*.oita.jp`）。市の公式サイトが `*.lg.jp` の場合は、すでに登録済みの `*.lg.jp` で足りる。

## 全国47都道府県の自治体サイト用（`*.<県名>.jp`。コピペ用）

他県の事例を使うときに、まとめて貼る。市町村のサイトは `*.lg.jp`（登録済み）か、この `*.<県名>.jp` のどちらかにあることが多い。ただし、`city.sapporo.jp` のように県名を含まない独自のドメインを使う市は入らない（足りない市が出たら個別に足す）。

```
*.hokkaido.jp
*.aomori.jp
*.iwate.jp
*.miyagi.jp
*.akita.jp
*.yamagata.jp
*.fukushima.jp
*.ibaraki.jp
*.tochigi.jp
*.gunma.jp
*.saitama.jp
*.chiba.jp
*.tokyo.jp
*.kanagawa.jp
*.niigata.jp
*.toyama.jp
*.ishikawa.jp
*.fukui.jp
*.yamanashi.jp
*.nagano.jp
*.gifu.jp
*.shizuoka.jp
*.aichi.jp
*.mie.jp
*.shiga.jp
*.kyoto.jp
*.osaka.jp
*.hyogo.jp
*.nara.jp
*.wakayama.jp
*.tottori.jp
*.shimane.jp
*.okayama.jp
*.hiroshima.jp
*.yamaguchi.jp
*.tokushima.jp
*.kagawa.jp
*.ehime.jp
*.kochi.jp
*.fukuoka.jp
*.saga.jp
*.nagasaki.jp
*.kumamoto.jp
*.oita.jp
*.miyazaki.jp
*.kagoshima.jp
*.okinawa.jp
```
