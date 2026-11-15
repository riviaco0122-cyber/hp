# Noki 写真の差し替え計画（Unsplash）

2026-11-15 作成。images.unsplash.com への通信が許可された新しい会話で実行する。

## 手順

1. Unsplash コネクタの `search_photos` で候補を探す（下の「枠」ごと。1語〜3語の短い検索語で）。
2. 候補ごとに `download_asset` を呼んでダウンロード URL を受け取る（Unsplash の規約上、使う写真は必ずこれでダウンロードを記録する）。
3. その URL から作業環境に落とし、**実際に画像を見て**選ぶ（説明文だけで決めない）。
4. `tools/okaeri/photos/<名前>-{640,1200,1600}.webp` に切り抜き・軽量化して置く（幅1600以上の元画像なら1600も作る）。
5. `tools/okaeri/content.py` と `build.py` の写真の名前を差し替え、クレジットを入れる（下の「決まり」）。
6. `python3 tools/okaeri/build.py` → `python3 tools/build.py` → 両方の `seo_check.py` でエラー0を確認。スマホとPCの表示を画像で確認。

## 決まり

- **場所を名指ししない**：フリー素材を「下田」「伊豆」「焼津」の写真として載せない。alt と説明文は写っているものだけを書く。Unsplash の撮影地情報があり、それが本当にその場所でも、自社の記事の主役の場所としては使わない。
- **自社の写真はそのまま**：NODE Shimoda のリビング（node-shimoda）、焼津の家のリフォーム前（yaizu-engawa、「before renovation」と明記）は差し替えない。
- **クレジット**：Unsplash の API 経由で使う写真は「Photo by 撮影者 on Unsplash」を、撮影者ページと Unsplash へのリンク付きで載せる（写真の説明文か、ページ下の「Photo credits」）。リンクには `?utm_source=noki&utm_medium=referral` を付ける。
- 人の顔、店の看板・商標がはっきり写ったものは避ける。
- `content.py` に写真ごとの出典（撮影者名・URL・Unsplash の写真ID）を残す。

## 枠と、いまの写真

| 枠 | いまの写真 | 欲しい絵 | 検索語の例 |
|---|---|---|---|
| トップのFV（横長・全面） | terraced-fields（アキヤドの素材） | 海と山のある小さな町を、少し高い所から。明るく、文字を重ねられる余白 | japanese coastal village / japanese seaside town / rural japan sea |
| Stay longer の入口・一覧 | scene-stay | 和室や縁側から外を眺める、ゆったりした旅 | japanese room window view / ryokan window / engawa |
| Live part-time の入口・一覧 | town-railway（伊豆の記事と重複） | 古い家でノートPCを開いて仕事、または町で暮らす日常 | laptop japanese house / remote work japan / rural japan daily life |
| Own a home の入口・一覧 | thatched-house | 古い日本家屋（できれば改修中・空き家らしさ） | old japanese house / kominka / abandoned house japan |
| Places の一覧 | own-open-sea（自社・撮影地不明） | 日本の海岸線 | japanese coastline / japan coast cliffs |
| 金目鯛の記事の冒頭 | own-fishing-bay | 金目鯛（赤い魚）そのもの、または煮付け・刺身 | kinmedai / red fish japanese market / japanese fish market |
| 東京から伊豆の記事の冒頭 | town-railway | 海沿いを走る日本の列車、または特急の車窓 | japanese train coast / train window sea japan |

## この会話で見つけた候補（説明文のみ。まだ画像は見ていない）

検索語「japanese coastal village」より：

- `jb0SsX_Bz_E` Traditional japanese buildings line a bay with green hills（PJH, 7008×4672）→ FV 候補
- `94YojUZRCy8` Traditional houses line a calm waterfront beneath a green hill（PJH）→ FV 候補
- `NZhQjmkR5wg` Scenic bay with a boat, traditional houses, and green mountain（PJH）→ FV / Places 候補
- `ze3rMm6TWfs` Coastal village with boats docked in a calm bay（PJH）→ Places 候補
- `Kjbhq8BJZTE` 地方の日常（軽トラ・トタンの小屋・古い家と緑の山）（Loris Boulinguez, 5901×3934）→ Live part-time 候補
- `8xjIJk7SbsA` fishing village（漁村）（moreau tokyo, 7360×4912）→ Places 候補

## 実施結果（2026-11-14）

候補を画像で見比べて選び、すべて `download_asset` でダウンロードを記録した。出典は `content.py` の `PHOTO_CREDITS`、クレジットは各ページ下の「Photo credits」（そのページで使った写真の撮影者だけ）。

| 枠 | 新しい写真（名前） | Unsplash ID | 撮影者 |
|---|---|---|---|
| トップのFV | coastal-village | jb0SsX_Bz_E | PJH |
| Stay longer | window-room | fta5pzyM0T8 | ZENG YILI |
| Live part-time | town-lane | stvwZJNN6Qo | PJH |
| Own a home | empty-tatami-room | IAgczbi1B-M | ayumi kubo |
| Places | rocky-coast | a3e4znCn-0o | Lucius Hunter |
| 金目鯛の記事 | grilled-red-fish（alt は「赤い魚の焼き物」。金目鯛とは書かない） | lFG7xubInhE | kazuend |
| 東京から伊豆の記事 | train-window-sea | E401NBqwIGg | realfish |

使わなくなった terraced-fields・scene-stay・town-railway・thatched-house・own-open-sea・own-fishing-bay は photos/ から消した。
