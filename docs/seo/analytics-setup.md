# GA4 / Search Console 連携の設定手順（人が1回だけ行う）

費用はかかりません（Google Cloud のプロジェクト・サービスアカウント・API はすべて無料枠内。課金アカウントの登録も不要）。所要時間は 15〜20 分ほどです。

## 1. Google Cloud でサービスアカウントを作る

1. https://console.cloud.google.com/ を開き、新しいプロジェクトを作る（例: `rivia-seo`）。
2. 「API とサービス」→「ライブラリ」で次の2つを検索して **有効にする**。
   - Google Search Console API
   - Google Analytics Data API
3. 「IAM と管理」→「サービスアカウント」→「サービスアカウントを作成」。名前は `seo-bot` など。権限（ロール）の付与は不要。
4. 作成したアカウントを開き、「キー」→「鍵を追加」→「新しい鍵を作成」→ **JSON** を選ぶ。JSON ファイルがダウンロードされる。
5. サービスアカウントのメールアドレス（`seo-bot@rivia-seo.iam.gserviceaccount.com` のような形）を控えておく。

## 2. Search Console に閲覧権限を付ける

1. https://search.google.com/search-console を開き、rivia-co.com のプロパティを選ぶ。
2. 「設定」→「ユーザーと権限」→「ユーザーを追加」→ 上のメールアドレスを入れ、権限は **制限付き** にする。
3. プロパティの種類を確認する。ドメインプロパティなら `sc-domain:rivia-co.com`、URL プレフィックスなら `https://rivia-co.com/`。
   - 現在は **URL プレフィックス `https://rivia-co.com/`** で登録済み（GA4 のタグで所有者を確認。DNS の設定は不要だった）。

## 3. GA4 に閲覧権限を付ける

1. https://analytics.google.com/ →「管理」→ プロパティの「プロパティのアクセス管理」→「＋」→ 上のメールアドレスを **閲覧者** で追加。
2. 「管理」→「プロパティの詳細」で **プロパティID（数字）** を控える（測定ID `G-RZVE2XBPQ2` とは別物）。

## 4. Claude のクラウド環境に登録する

チャットに鍵を貼り付けないでください。セッション画面のタイトルバーにあるクラウド環境のメニュー →「Edit」から、**環境変数**として次の3つを登録します。

| 変数名 | 値 |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | ダウンロードした JSON ファイルの中身（1行にしてそのまま貼る） |
| `GA4_PROPERTY_ID` | 不要（`556922741` をスクリプトの既定値に設定済み。別のプロパティを使うときだけ登録） |
| `GSC_SITE_URL` | `https://rivia-co.com/`（ドメインプロパティに切り替えた場合は `sc-domain:rivia-co.com`） |

登録後に始めた新しいセッションから使えます。動作確認は `pip install -r tools/requirements.txt && python3 tools/analytics.py`。

## 5. 鍵の管理

- JSON ファイルはリポジトリに入れない（`.gitignore` で `*service-account*.json` などの名前の鍵ファイルを除外済み）。
- 不要になったら Google Cloud でサービスアカウントの鍵を削除すれば、すぐに無効になります。

## 6. YouTube 調査用の API キー（任意・無料）

リサーチ部が YouTube の動画情報・概要欄・人気コメントを集めるために使います。1日 10,000 ユニットの無料枠内で動くので、費用はかかりません。

1. 手順1と同じ Google Cloud プロジェクトで、「API とサービス」→「ライブラリ」→ **YouTube Data API v3** を有効にする。
2. 「API とサービス」→「認証情報」→「認証情報を作成」→「API キー」。
3. 作成したキーの「API の制限」で **YouTube Data API v3 のみ** に制限する（漏れたときの被害を防ぐため）。
4. 手順4と同じ場所に、環境変数 `YOUTUBE_API_KEY` として登録する。

## 7. e-Stat（政府統計）の API（任意・無料）

リサーチ部が、記事に使う統計の数字（宿泊者数・空き家率など）を政府統計の総合窓口 e-Stat から出典つきで取るために使います。無料です。

1. e-Stat（https://www.e-stat.go.jp/）でユーザー登録し、ログイン後「マイページ」→「API機能（アプリケーションID発行）」で、名前と URL（サイトの URL でよい）を入れて **アプリケーションID** を発行する。
2. 手順4と同じ場所に、環境変数 `ESTAT_APP_ID` として登録する。
3. クラウド環境のネットワークの許可ドメインに `api.e-stat.go.jp` を追加する（`www.e-stat.go.jp` は不要）。

使い方（結果は標準出力と `docs/sources/estat/` に保存。どの結果にも出典＝統計名・調査年・表の名前・e-Stat の URL・取得日が付く）:

```bash
python3 tools/estat.py lodging 静岡県 沖縄県 --years 5     # 宿泊旅行統計調査：延べ宿泊者数・外国人の割合（都道府県別）
python3 tools/estat.py akiya 全国 静岡県 下田市            # 住宅・土地統計調査（令和5年）：空き家数・空き家率（市区町村も可）
python3 tools/estat.py search "空き家" --stats 00200522 --year 2023   # ほかの統計表を探す
```

- 同じ名前の市区町村は「広島県府中市」のように都道府県名を前に付ける。
- 宿泊者数は、e-Stat のデータベースに観光庁の表が 2016 年分しか入っていないため、総務省「社会・人口統計体系」に収録された値を使う。この値は観光庁が発表する全施設の年間値より小さい（全国で約8割。従業者数10人以上の施設の集計とみられる）。県どうしの比較・推移・外国人の割合に使い、絶対数を記事に書くときは観光庁の表で確かめる。
- API で取った数字を記事などで公開するときは、e-Stat の利用規約に沿って出典を書く（ツールの出力のとおり）。
- アプリケーションIDは表示・保存しない。ツールのエラー文からも消している。

## 8. YouTube アナリティクス（チャンネルの数字・任意・無料）

週1回の YouTube の定期実行（`/youtube-weekly`）が、YouTube Studio と同じ数字（再生回数・平均再生率・視聴者維持・登録者の増減・視聴の入口など）を API で取り、次の動画の改善に使うためのものです。**チャンネルの持ち主の Google アカウントでの許可（OAuth）** が必要です（サービスアカウントでは取れません）。費用はかかりません。

1. 手順1と同じ Google Cloud プロジェクトで、「API とサービス」→「ライブラリ」から **YouTube Analytics API** と **YouTube Data API v3** を有効にする。
2. 「API とサービス」→「OAuth 同意画面」を作る（ユーザーの種類「外部」、アプリ名は「アキヤド 分析」など、サポートメールは自分）。スコープは追加しなくてよい。**作ったら「アプリを公開」で「本番環境」にする**（「テスト」のままだと、許可が7日で切れて毎週やり直しになる。自分だけで使うので Google の審査は不要。許可するときに「確認されていないアプリ」と出たら「詳細」→「（安全ではないページ）に移動」で進む）。
3. 「認証情報」→「認証情報を作成」→「OAuth クライアント ID」→ 種類「ウェブ アプリケーション」。「承認済みのリダイレクト URI」に `https://developers.google.com/oauthplayground` を追加して作成し、**クライアント ID** と **クライアント シークレット** を控える。
4. ブラウザ（スマホでも可）で https://developers.google.com/oauthplayground を開く。
   - 右上の歯車 →「Use your own OAuth credentials」にチェック → 3 のクライアント ID とシークレットを入れる。
   - 左の「Input your own scopes」に次の2つを空白区切りで入れて「Authorize APIs」:
     `https://www.googleapis.com/auth/yt-analytics.readonly https://www.googleapis.com/auth/youtube.readonly`
   - **アキヤドのチャンネルを持っている Google アカウント**（ブランドアカウントならそのチャンネル）を選んで許可する。
   - 「Exchange authorization code for tokens」を押し、表示された **Refresh token** を控える。
5. 手順4と同じ場所（クラウド環境の環境変数）に、`YT_CLIENT_ID`・`YT_CLIENT_SECRET`・`YT_REFRESH_TOKEN` の3つを登録する。**ファイルやチャットには書かない。**
6. ネットワークの許可ドメインに `oauth2.googleapis.com`・`youtubeanalytics.googleapis.com`・`www.googleapis.com` があるか確かめる（なければ追加）。
7. 確認: `python3 tools/youtube_analytics.py check` で「接続できました」と出れば完了。

- 読み取り専用の許可です（動画の公開・削除・編集はできません）。
- 不要になったら、Google アカウントの「セキュリティ → サードパーティのアクセス」から許可を取り消せば、すぐに無効になります。
