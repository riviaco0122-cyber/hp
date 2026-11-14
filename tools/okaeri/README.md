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

## どこを直すか

| 直したいもの | ファイル |
|---|---|
| 記事（英語・日本語レビュー版・FAQ・出典・狙う語） | `tools/okaeri/content.py` |
| トップ・伊豆半島・運営者情報の本文 | `tools/okaeri/build.py` の `page_home` `page_izu` `page_about` |
| 見た目 | `tools/okaeri/site.css` |
| 写真 | `tools/okaeri/photos/`（<名前>-1200.webp と -640.webp）と `content.py` の `PHOTOS` |
| SEO計画・キーワード・公開までの作業（日本語） | `tools/okaeri/review_ja.py` |

`okaeri/` の HTML は生成物。直接書き換えない。

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
