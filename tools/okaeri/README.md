# Noki — 海外向け英語メディア

> 2026-11-15 に「Okaeri Japan」→（一時 Homeward Japan）→「Noki」に改名。okaeri は欧米の読み手に意味が伝わらず、Homeward は意味がそのままで捻りがないため。Noki（軒）は、ツバメが毎年帰ってくる家の軒先と、家を数える「軒」から。短く英語圏でも読みやすい名前にし、意味はキャッチコピーと About で補う（SANU などの考え方）。公開URL・公開フォルダ・サイト上の名前は `noki`。**作業用の名前**（このフォルダ `tools/okaeri/`、部署名 `okaeri-*`、スキル `/okaeri-article`、ブランチ `okaeri-japan`）は旧名のまま。名前とURLは `site.json` の `name`・`prefix` の1か所で決まる。

日本に長く滞在したい海外の人と、日本の空き家を買う・活かすことを考えている海外の人に向けたメディア。
公開先は https://rivia-co.com/noki （アキヤドと同じドメインの下のフォルダ）。

## 使い方

```
python3 tools/okaeri/build.py              # okaeri/（公開フォルダ）と tools/okaeri/preview/（試作）を作る
python3 tools/build.py                     # アキヤド側。robots.txt と llms.txt に Noki の案内が入る
python3 tools/okaeri/seo_check.py          # Noki の点検（エラー0で公開）
python3 tools/okaeri/seo_check.py --launch # 公開前の点検（黄色い枠・未接続のフォームもエラーにする）
python3 tools/seo_check.py                 # アキヤド側の点検
```

順番は「Noki の build（tools/okaeri/build.py）→ アキヤドの build → 両方の点検」。

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
| 漢字の印 | 入口に漢字一文字（旅・暮・家・地）。入口ページの見出しの大きな薄い字 | `content.py` の `TOPICS[*]["kanji"]` |
| 文様 | 青海波。藍の帯（自社の家の紹介）とフッターの上端だけ | `--seigaiha` |
| ロゴ | 右を向いた丸いツバメ（笑って細めた目・白いお腹・頬の赤・長い燕尾）。こわい・驚いた顔に見えないよう、白目の輪は使わない。ダークモードでは色を反転させず、体を明るい青・お腹と目を白にする（反転すると口を開けた顔に見える）（2026-11-16） | `build.py` の `MARK_SHAPES` |

**同じ写真は1ページに1回まで**（人の指摘 2026-11-15）。記事の下の「Stay with us」は、本文にその写真がないページでだけ写真を出す（`cta(ctx, photo=...)`）。`seo_check.py` が、同じ写真が2回以上出たページを警告する。

**UI の原則**（人と合意 2026-11-16。初めて来た欧米の読み手の目で見直した結果）:

1. **中身のない入口は出さない。** 押して「準備中」だと作りかけのサイトに見える。テーマ（入口）は記事が1本以上あるものだけ、メニュー・フッター・チップ・一覧ページに出す（`build.py` の `HUB_TOPICS`・`OPEN_PLANS`）。まだ開いていない町のカード、つながっていないフォーム（メール登録）も、使えるようになるまで出さない。
2. **トップは短く、読み物を先に。** キャッチコピー → 記事 → 自社の家の紹介（1回）の3段。スマホで5画面以内。
3. **自社の家の案内は1ページに1回**（ヘッダーの「Stay with us」のボタンは除く）。記事では記事の下の「Stay with us」だけにし、冒頭や横の欄に重ねない。本文で NODE Shimoda に触れるのは、流れで役立つ場所に1回まで（playbook 2章）。
4. **本文の出典は小さな番号（上付き）にする。** 名前が文中に続くと論文のようになり、読む流れが止まる。番号を押すとページ下の出典一覧のその行に飛ぶ（`Ctx.expand` の `[[s:…]]` と `Ctx.sources`。番号は本文で初めて挙げた順）。
5. **ブランドと関係のない飾りは置かない。** 旧名の名残り（縦書きの「おかえり」など）は消す。
6. **見出しと押せるものを、色と形で分ける**（人の指摘 2026-11-16）。同じ色・同じ太さだと、どれが押せるのか分からない。見出し（フッター・メニューの YOUR PLAN など）は小さく薄い色（`--muted`）の大文字に下線を引いて区切り、押せる文字はリンクの色（`--ai`）にする。メニューの縦に並ぶリンクには右に「›」を付ける。明るい表示とダークモードの両方で確かめる。

**表**: 文章の入る表は `class="free"`。3列以上の文章の表は、スマホ幅で1行ずつのカードになる（`build.py` の `stack_tables`）。

色を足す・変えるときは、地の色（和紙・カード）に対して文字のコントラスト比 4.5 以上を計算で確かめる（いまの色はすべて 5.0 以上）。

## アキヤドとの関係

**指示書は別**: Noki の作業では Noki の指示書だけを使う（入口は `tools/okaeri/CLAUDE.md`）。以下は、同じドメイン・同じリポジトリにある技術的なつながり。

- 同じドメインなので、サイト名の宣言（WebSite）は rivia-co.com のトップだけ。Noki には置かない。運営会社は about.html の Organization を同じ @id で参照する。
- sitemap は `noki/sitemap.xml`（アキヤドの sitemap とは別）。`seo/robots.txt` に2本目の `Sitemap:` として入る。
- URL はアキヤドと同じ形（末尾スラッシュなし・`.html`）。トップだけ `/noki`（`vercel.json` の rewrites で `noki/index.html` に対応）。
- `/en/` はトップへの転送が残っているので使わない。
- 日本語レビュー版と SEO計画は `tools/okaeri/preview/` にだけ入る（.gitignore 済み。公開されない）。

## 決まり

- 事実を作らない。数字と制度には出典。自社の体験は docs/brand/experience.md の確認済みのものだけ。未確認は `[[ed:…]]`（黄色い枠）で残す。
- 黄色い枠が残っている間は `--launch` の点検が通らない。
- 更新日（`updated`）は、内容を実際に直したときだけ変える。
- URL（`slug`）は公開後に変えない。変えるときは `vercel.json` に 301 を足す。
- テーマ別の一覧（/noki/akiya.html など）は、公開記事が3本以上になったテーマだけ自動でできる。
- 英語の記事には、日本語レビュー版（`ja`）を必ず対で書く。
