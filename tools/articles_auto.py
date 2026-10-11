# AI社員チーム（日次サイクル）が追加する記事。build.py が読み込む。
# 1記事＝1つの dict。形式は既存の articles_series1.py などと同じ（項目の説明は .claude/agents/engineer.md）。
# 例:
# dict(
#     slug="akiya-kaitai-hiyou",                      # URL（/media/<slug>.html）。英小文字とハイフン
#     date="2026-12-11",                               # 公開日（日本時間）。この日まで一覧などから自動で隠れる
#     topics=["sell", "money"],                        # テーマ（先頭がカテゴリ）: sell/lend/house/start/money/operate/trend
#     photo=("old-town-street", "古い町家が並ぶ通り"),   # images/photos/<名前>.jpg と代替テキスト（既存の写真だけ）
#     guides=[("sell", 2)],                            # ガイドの何番目の Step に入るか: sell/use/side（なければ []）
#     title="…", short="一覧用の短い題\n2行まで", description="…（50〜140字）",
#     services=["operation"],                          # 関連サービス: operation/management/partnership/marketing/recruit
#     keypoints=["…", "…", "…"],                      # この記事のポイント（3〜5）
#     sections=[("id", "見出し", """<p>本文の HTML</p>""")],
#     faq=[("質問", "答え")],
#     sources=["発行元「資料名」（公表年）"],
# ),
ARTICLES_AUTO = [
]
