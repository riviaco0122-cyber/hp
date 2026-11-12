# -*- coding: utf-8 -*-
"""RIVIA&CO. サイトの静的HTMLを生成する（作業用スクリプト）"""
from html import escape as e, unescape
import collections
import math
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures import insert_figure, cycle as fig_cycle  # 記事の図解


# ---------------------------------------------------------------- 本体（tools/build_parts/）
# 中身は役割ごとのファイルに分けてある（AI・人が、直したい部分だけを開けるように）。
# 上から順に、このファイルの続きとして実行する（1つの大きなファイルだったときと同じ動き）。
# 順番に意味がある（後のファイルは、前のファイルの定数・関数を使う）。足すときは BUILD_PARTS に書く。
BUILD_PARTS = [
    "common.py",  # 文字組み（強調のマーカー・見出しの改行位置）と、出力先・日付・計測 ID・サービス一覧・ナビの項目などの設定
    "icons.py",  # アイコン（SVG）と SNS のリンク
    "layout.py",  # ページの外枠（ヘッダー・フッター・パンくず・版番号）と、共通の部品（相談の案内・流れ・お客様の声・実績・よくある質問）
    "plans.py",  # プラン例（料金と内容）と、協業スキームの三角形の図
    "services.py",  # コーポレート：しくみの図・対応エリア・かんたんフォームと、サービス一覧・サービスごとのページ
    "corporate.py",  # コーポレート：トップ・会社概要・採用・お問い合わせ・プライバシー・送信完了のページ
    "spec.py",  # 仕様書 docs/site-spec.md の生成
    "media_articles.py",  # アキヤド：記事データの読み込みと、写真・アイキャッチ・記事カード・ヘッダー・フッター・相談の案内
    "media_plans.py",  # アキヤド：プランのページと、ご相談の解説動画
    "media_services.py",  # アキヤド：サービスごとのページ（図・収支シミュレーション・フォーム）と、会社のページ
    "media_learn.py",  # アキヤド：基礎から学ぶ（learn.html）
    "media_contact.py",  # アキヤド：お問い合わせ・送信完了のページ
    "media_top.py",  # アキヤド：ナビ・トップ・テーマ別・ガイド・検索のページ
    "article_page.py",  # アキヤド：記事ページの組み立て（出典の欄を含む）
    "seo_files.py",  # 404 ページ・llms.txt・sitemap.xml・robots.txt
]
_PARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_parts")
for _part in BUILD_PARTS:
    _path = os.path.join(_PARTS_DIR, _part)
    with open(_path, encoding="utf-8") as _f:
        exec(compile(_f.read(), _path, "exec"), globals())


if __name__ == "__main__":
    index_page()
    about_page()
    services_page()
    for k, n in SERVICES:
        service_page(k, n)
    careers_page()
    contact_page()
    privacy_page()
    thanks_page()
    media_index_page()
    media_plans_page()
    for sv in MEDIA_SERVICES:
        media_service_page(sv)
    media_company_page()
    media_learn_page()
    media_contact_page()
    media_thanks_page()
    for k, n in MEDIA_CATEGORIES:
        media_category_page(k, n)
    for g in MEDIA_GUIDES:
        media_guide_page(g)
    media_search_page()
    not_found_page()
    for a in ARTICLES:
        article_page(a)
    sitemap()
    llms_txt()
    # 英語版（コーポレートページのみ。いまは出していない）
    if BUILD_EN:
        import subprocess
        subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n", "build_en.py")], check=True)
    spec_md()
    print("done")
