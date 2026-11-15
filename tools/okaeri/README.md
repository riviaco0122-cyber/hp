# Okaeri Japan（仮称）— 海外向け英語メディア

日本に長く滞在したい海外の人と、日本の空き家を買う・活かすことを考えている海外の人に向けたメディア。
公開先は https://rivia-co.com/okaeri （アキヤドと同じドメインの下のフォルダ）。

## 使い方

```
python3 tools/okaeri/build.py              # okaeri/（公開フォルダ）と tools/okaeri/preview/（試作）を作る
python3 tools/build.py                     # アキヤド側。robots.txt と llms.txt に Okaeri Japan の案内が入る
python3 tools/okaeri/seo_check.py          # Okaeri Japan の点検（エラー0で公開）
python3 tools/okaeri/seo_check.py --launch # 公開前の点検（黄色い枠・未接続のフォームもエラーにする）
python3 tools/seo_check.py                 # アキヤド側の点検
```

順番は「okaeri の build → アキヤドの build → 両方の点検」。

## 記事の作り方・見直し方（部署の分担と採点）

記事は `/okaeri-article <テーマ or 記事id>` で、戦略部 → リサーチ部 → 執筆部 → 品質保証部 → エンジニア部 → 品質保証部の順に回す（アキヤドと同じ仕組み）。100点満点（機械40＋品質60）で90点以上、ゲート違反なしのものだけを入れる。

| 資料 | 場所 |
|---|---|
| 基準（部署・書き方・採点・戻る工程・人の確認） | `tools/okaeri/playbook.md` |
| 機械採点（40点）とゲート | `python3 tools/okaeri/article_score.py <記事id or 下書き.py>`（`--all` で全記事） |
| 部署 | `.claude/agents/okaeri-strategist.md`・`okaeri-researcher.md`・`okaeri-writer.md`・`okaeri-engineer.md`・`okaeri-qa.md` |
| 構成案・下書き・採点ログ | `tools/okaeri/briefs/`・`tools/okaeri/drafts/`・`tools/okaeri/log.md` |

## どこを直すか

| 直したいもの | ファイル |
|---|---|
| 記事（英語・日本語レビュー版・FAQ・出典・狙う語） | `tools/okaeri/content.py` |
| トップ・伊豆半島・運営者情報の本文 | `tools/okaeri/build.py` の `page_home` `page_izu` `page_about` |
| 見た目 | `tools/okaeri/site.css` |
| 写真 | `tools/okaeri/photos/`（<名前>-1200.webp と -640.webp）と `content.py` の `PHOTOS` |
| SEO計画・キーワード・公開までの作業（日本語） | `tools/okaeri/review_ja.py` |

`okaeri/` の HTML は生成物。直接書き換えない。

## ブランドデザイン（2026-11-15。欧米の人が思い浮かべる Cool Japan・四季）

日本らしさは「控えめな和の要素を、決まった場所にだけ」使って出す。観光パンフレットのような飾り（桜の花びらの散らし・和柄の全面敷き・筆文字の多用）はしない。

| 要素 | 決まり | 場所 |
|---|---|---|
| 色 | 地=和紙（生成り）、文字=墨、主色=藍、差し色=朱。暗い表示は夜の墨と和紙色の文字 | `site.css` の `:root` |
| 四季の色 | 入口ごとに1色（春=桜=Stay、夏=青葉=Live、秋=紅葉=Own、冬=雪=Places）。カードの上線・印・ラベルにだけ使う | `.t-<キー>` と `--season` |
| 書体 | 見出し=明朝（Shippori Mincho）、ナビ・ボタン・ラベル=Zen Kaku Gothic New、本文=Source Serif 4 | `--head`・`--display`・`--body` |
| 漢字の印 | 入口に漢字一文字（旅・暮・家・地）。カードの角の印と、入口ページの見出しの大きな薄い字 | `content.py` の `TOPICS[*]["kanji"]` |
| 文様 | 青海波。藍の帯（自社の家の紹介）とフッターの上端だけ | `--seigaiha` |
| ロゴ | 横向きで飛ぶツバメ（白いお腹・赤いのど） | `build.py` の `MARK_SHAPES` |

色を足す・変えるときは、地の色（和紙・カード）に対して文字のコントラスト比 4.5 以上を計算で確かめる（いまの色はすべて 5.0 以上）。

## アキヤドとの関係

- 同じドメインなので、サイト名の宣言（WebSite）は rivia-co.com のトップだけ。Okaeri Japan には置かない。運営会社は about.html の Organization を同じ @id で参照する。
- sitemap は `okaeri/sitemap.xml`（アキヤドの sitemap とは別）。`seo/robots.txt` に2本目の `Sitemap:` として入る。
- URL はアキヤドと同じ形（末尾スラッシュなし・`.html`）。トップだけ `/okaeri`（`vercel.json` の rewrites で `okaeri/index.html` に対応）。
- `/en/` はトップへの転送が残っているので使わない。
- 日本語レビュー版と SEO計画は `tools/okaeri/preview/` にだけ入る（.gitignore 済み。公開されない）。

## 決まり

- 事実を作らない。数字と制度には出典。自社の体験は docs/brand/experience.md の確認済みのものだけ。未確認は `[[ed:…]]`（黄色い枠）で残す。
- 黄色い枠が残っている間は `--launch` の点検が通らない。
- 更新日（`updated`）は、内容を実際に直したときだけ変える。
- URL（`slug`）は公開後に変えない。変えるときは `vercel.json` に 301 を足す。
- テーマ別の一覧（/okaeri/akiya.html など）は、公開記事が3本以上になったテーマだけ自動でできる。
- 英語の記事には、日本語レビュー版（`ja`）を必ず対で書く。
