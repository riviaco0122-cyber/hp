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
| `GA4_PROPERTY_ID` | 手順3で控えた数字 |
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
