#!/usr/bin/env python3
"""e-Stat（政府統計の総合窓口）の API から、記事の根拠になる統計を取る（リサーチ部が使う）。標準ライブラリのみ。

必要な環境変数:
  ESTAT_APP_ID   e-Stat の API 機能で発行したアプリケーションID（docs/seo/analytics-setup.md の 7 章）

使い方:
  python3 tools/estat.py lodging 静岡県 [沖縄県 ...] [--years 5]
      宿泊旅行統計調査（観光庁）の都道府県別の延べ宿泊者数・外国人延べ宿泊者数・外国人の割合・実宿泊者数
      ※ e-Stat のデータベースに入っている宿泊旅行統計調査の表は 2016 年分だけなので、総務省「社会・人口統計体系
        都道府県データ」に収録された同調査の数値を使う（出典に原典と収録先の両方を書く）。
        この収録値は観光庁が発表する全施設の年間値より小さい（全国で約8割）。絶対数を記事に書くときは
        観光庁の表で確かめる（出力の「注意」を参照）。
  python3 tools/estat.py akiya 静岡県 [下田市 静岡県伊豆市 ...]
      令和5年住宅・土地統計調査（総務省）の総住宅数・空き家数（種類別）・空き家率。全国・都道府県・市区町村。
      同じ名前の市区町村があるときは「広島県府中市」のように都道府県名を前に付ける。
  python3 tools/estat.py search "キーワード" [--stats 政府統計コード] [--year 2023] [--max 20]
      上の2つ以外の統計を探す（表の ID・統計名・調査年・表の名前・URL を一覧にする）。

出力:
  標準出力と、ファイル docs/sources/estat/YYYY-MM-DD_<種類>_<地域>.md（--no-save で保存しない）。
  どの結果にも出典（統計名・調査年・表の名前・e-Stat の URL・取得日）を付ける。記事に数字を使うときは、
  この出典をそのままリサーチメモと記事の出典欄に写す。

※ アプリケーションIDは表示・保存しない（エラー文からも消す）。
※ e-Stat の利用規約により、API で取ったデータを公開するときは次のクレジットを表示する:
  「このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。」
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.e-stat.go.jp/rest/3.0/app/json/"
CREDIT = "このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。"

# 宿泊: 社会・人口統計体系 都道府県データ 基礎データ「Ｇ 文化・スポーツ」（原典は観光庁「宿泊旅行統計調査」）
LODGING_TABLE = "0000010107"
LODGING_ITEMS = [("G7101", "延べ宿泊者数"), ("G7102", "外国人延べ宿泊者数"),
                 ("G7103", "実宿泊者数"), ("G710301", "外国人実宿泊者数")]
# 空き家: 令和5年住宅・土地統計調査 住宅及び世帯に関する基本集計 表1-2-1（全国・都道府県・市区町村）
AKIYA_TABLE = "0004021421"
AKIYA_ITEMS = [("0", "総住宅数"), ("22", "空き家"),
               ("222", "　うち賃貸用の空き家"), ("223", "　うち売却用の空き家"),
               ("224", "　うち二次的住宅（別荘など）"), ("221", "　うち賃貸・売却用及び二次的住宅を除く空き家")]


def app_id():
    v = os.environ.get("ESTAT_APP_ID", "").strip()
    if not v:
        sys.exit("環境変数 ESTAT_APP_ID が未設定です（docs/seo/analytics-setup.md の 7 章）")
    return v


def call(endpoint, **params):
    key = app_id()
    url = API + endpoint + "?" + urllib.parse.urlencode({"appId": key, **params})
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        sys.exit(f"e-Stat API エラー {e.code}: {body}".replace(key, "***"))
    except urllib.error.URLError as e:
        sys.exit(f"e-Stat API に接続できません: {e.reason}".replace(key, "***"))
    root = next(iter(data.values()))
    res = root.get("RESULT", {})
    if int(res.get("STATUS", 0)) not in (0, 1, 2):  # 0=正常 1=該当なし 2=一部
        sys.exit(f"e-Stat API エラー {res.get('STATUS')}: {res.get('ERROR_MSG')}".replace(key, "***"))
    return root


def as_list(x):
    return x if isinstance(x, list) else ([] if x is None else [x])


def text(x):
    return x.get("$", "") if isinstance(x, dict) else str(x or "")


def table_url(sid):
    return f"https://www.e-stat.go.jp/dbview?sid={sid}"


def meta(sid):
    m = call("getMetaInfo", statsDataId=sid)["METADATA_INF"]
    classes = {c["@id"]: as_list(c["CLASS"]) for c in as_list(m["CLASS_INF"]["CLASS_OBJ"])}
    return m["TABLE_INF"], classes


def resolve_areas(names, areas):
    """地域名（「静岡県」「下田市」「広島県府中市」「全国」）を e-Stat の地域コードに直す。"""
    by_code = {a["@code"]: a for a in areas}
    out = []
    for name in names:
        hits = [a for a in areas if a["@name"] == name]
        if not hits:  # 「静岡県下田市」の形
            hits = [a for a in areas if name.endswith(a["@name"]) and a.get("@parentCode") in by_code
                    and name == by_code[a["@parentCode"]]["@name"] + a["@name"]]
        if not hits and not name.endswith(("都", "道", "府", "県", "市", "区", "町", "村")) and name != "全国":
            hits = [a for a in areas if a["@name"] in (name + "県", name + "府", name + "都")]
        if not hits:
            sys.exit(f"地域が見つかりません: {name}（都道府県名・市区町村名を正式な名前で指定してください）")
        if len(hits) > 1:
            cand = "、".join(by_code.get(a.get("@parentCode"), {}).get("@name", "") + a["@name"] for a in hits)
            sys.exit(f"同じ名前の地域が複数あります: {name}（{cand}）。都道府県名を前に付けてください")
        a = hits[0]
        parent = by_code.get(a.get("@parentCode"), {}).get("@name", "")
        label = a["@name"] if a["@code"].endswith("000") or not parent or parent == "全国" else parent + a["@name"]
        out.append((a["@code"], label))
    return out


def values(sid, **filters):
    d = call("getStatsData", statsDataId=sid, **filters)
    return as_list(d["STATISTICAL_DATA"].get("DATA_INF", {}).get("VALUE"))


def num(v):
    try:
        return float(v.replace(",", ""))
    except (AttributeError, ValueError):
        return None  # 「-」「X」「***」など


def fmt(v, unit=""):
    n = num(v)
    if n is None:
        return f"{v}（数値なし）"
    return f"{n:,.0f}{unit}"


def survey(v):
    v = str(v or "")
    if len(v) == 6 and v.isdigit():
        return f"{v[:4]}年{int(v[4:])}月"
    return v if v and v != "0" else "表の各列の年次を参照"


def source_block(t, extra=None):
    stat = text(t.get("STAT_NAME"))
    title = text(t.get("TITLE"))
    no = t["TITLE"].get("@no", "") if isinstance(t.get("TITLE"), dict) else ""
    lines = ["## 出典", "",
             f"- 統計名: {stat}（{text(t.get('GOV_ORG'))}）／ {t.get('STATISTICS_NAME', '')}",
             f"- 表の名前: {('表' + no + ' ') if no and not no.startswith('0') else ''}{title}",
             f"- 調査年: {survey(t.get('SURVEY_DATE'))} ／ 公開日 {t.get('OPEN_DATE', '')} ／ 更新日 {t.get('UPDATED_DATE', '')}",
             f"- e-Stat の URL: {table_url(t['@id'])}（統計表ID {t['@id']}）",
             f"- 取得日: {dt.date.today().isoformat()}（e-Stat API）"]
    lines += extra or []
    lines += ["", f"> {CREDIT}"]
    return lines


def cmd_lodging(a):
    t, cls = meta(LODGING_TABLE)
    areas = resolve_areas(a.areas, cls["area"])
    times = sorted(c["@code"] for c in cls["time"])[-a.years:]
    tname = {c["@code"]: c["@name"] for c in cls["time"]}
    rows = values(LODGING_TABLE, cdArea=",".join(c for c, _ in areas),
                  cdCat01=",".join(c for c, _ in LODGING_ITEMS), cdTimeFrom=times[0])
    got = {(r["@area"], r["@cat01"], r["@time"]): r.get("$") for r in rows}
    L = ["# e-Stat: 宿泊者数（宿泊旅行統計調査）", ""]
    for code, label in areas:
        L += [f"## {label}", "",
              "| 年 | 延べ宿泊者数（人泊） | うち外国人（人泊） | 外国人の割合 | 実宿泊者数（人） | うち外国人（人） |",
              "|---|---|---|---|---|---|"]
        for tm in times:
            g = lambda c: got.get((code, c, tm))
            total, foreign = num(g("G7101")), num(g("G7102"))
            share = f"{foreign / total * 100:.1f}%" if total and foreign is not None else "—"
            L.append(f"| {tname.get(tm, tm)} | {fmt(g('G7101'))} | {fmt(g('G7102'))} | {share} | {fmt(g('G7103'))} | {fmt(g('G710301'))} |")
        L.append("")
    L += ["外国人の割合 = 外国人延べ宿泊者数 ÷ 延べ宿泊者数（このツールで計算）。", ""]
    L += source_block(t, [
        "- 原典: 観光庁「宿泊旅行統計調査」（https://www.mlit.go.jp/kankocho/tokei_hakusyo/shukuhakutokei.html）",
        "- 記事に書くときは「観光庁『宿泊旅行統計調査』（総務省『社会・人口統計体系』収録値、e-Stat）」のように原典と収録先を両方書く。",
        "- **注意（未確認）**: この表の値は、観光庁が報道発表で出す全施設の年間値より小さい（全国 2024 年: この表 5億4,107万人泊 ／"
        " 観光庁の確定値 6億5,906万人泊、約82%）。従業者数10人以上の施設に限った集計とみられる。都道府県の比較・推移・外国人の割合に使い、"
        "「◯◯県の延べ宿泊者数は◯人泊」と絶対数を書くときは観光庁の表で確かめて、その表を出典にする。",
        "- 年の表記（「2024年度」など）は e-Stat の表のとおり。暦年（1〜12月）か年度かは観光庁の表で確かめる。"])
    return "lodging", areas, L


def cmd_akiya(a):
    t, cls = meta(AKIYA_TABLE)
    areas = resolve_areas(a.areas, cls["area"])
    rows = values(AKIYA_TABLE, cdArea=",".join(c for c, _ in areas),
                  cdCat01=",".join(c for c, _ in AKIYA_ITEMS))
    got = {(r["@area"], r["@cat01"]): r.get("$") for r in rows}
    L = ["# e-Stat: 空き家数・空き家率（令和5年住宅・土地統計調査）", "",
         "| 地域 | " + " | ".join(n.strip("　") for _, n in AKIYA_ITEMS[:2]) + " | 空き家率 | "
         + " | ".join(n.strip("　").replace("うち", "") for _, n in AKIYA_ITEMS[2:]) + " |",
         "|---" * (len(AKIYA_ITEMS) + 2) + "|"]
    for code, label in areas:
        total, akiya = num(got.get((code, "0"))), num(got.get((code, "22")))
        rate = f"{akiya / total * 100:.1f}%" if total and akiya is not None else "—"
        cells = [fmt(got.get((code, c)), "戸") for c, _ in AKIYA_ITEMS]
        L.append(f"| {label} | {cells[0]} | {cells[1]} | {rate} | " + " | ".join(cells[2:]) + " |")
    L += ["", "空き家率 = 空き家数 ÷ 総住宅数（このツールで計算。総務省の公表値と同じ定義）。"
          "数値は標本調査の推計値で、端数を丸めている（内訳の合計が総数と合わないことがある）。", ""]
    L += source_block(t, ["- 調査の時点: 2023年（令和5年）10月1日"])
    return "akiya", areas, L


def cmd_search(a):
    p = {"searchWord": a.query, "limit": a.max}
    if a.stats:
        p["statsCode"] = a.stats
    if a.year:
        p["surveyYears"] = a.year
    d = call("getStatsList", **p)
    tables, seen = [], set()
    for x in as_list(d.get("DATALIST_INF", {}).get("TABLE_INF")):
        if x["@id"] not in seen:
            seen.add(x["@id"])
            tables.append(x)
    L = [f"# e-Stat 検索: {a.query}", "",
         f"該当 {d.get('DATALIST_INF', {}).get('NUMBER', 0)} 件（重複を除いて {len(tables)} 件を表示）", ""]
    for x in tables:
        L += [f"- **{text(x.get('TITLE'))}**",
              f"  - {text(x.get('STAT_NAME'))}（{text(x.get('GOV_ORG'))}）／ {x.get('STATISTICS_NAME', '')}",
              f"  - 調査年 {x.get('SURVEY_DATE')} ／ 更新日 {x.get('UPDATED_DATE')} ／ 統計表ID {x['@id']} ／ {table_url(x['@id'])}"]
    L += ["", "値を取るには、統計表ID を使って getStatsData を呼ぶ処理をこのツールに足す（よく使う表は lodging・akiya のようにサブコマンドにする）。",
          "", f"> {CREDIT}"]
    return "search", [("", a.query)], L


def main():
    ap = argparse.ArgumentParser(description="e-Stat から統計を取る（出典つき）")
    ap.add_argument("--no-save", action="store_true", help="docs/sources/estat/ に保存しない")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("lodging", help="宿泊旅行統計調査：都道府県別の延べ宿泊者数・外国人の割合")
    p.add_argument("areas", nargs="+", help="都道府県名（例: 静岡県）。全国も可")
    p.add_argument("--years", type=int, default=5, help="直近何年分を出すか")
    p = sub.add_parser("akiya", help="住宅・土地統計調査：空き家数・空き家率（都道府県・市区町村）")
    p.add_argument("areas", nargs="+", help="地域名（例: 静岡県 下田市 全国）")
    p = sub.add_parser("search", help="統計表を探す")
    p.add_argument("query")
    p.add_argument("--stats", help="政府統計コード（例: 00200522=住宅・土地統計調査、00601020=宿泊旅行統計調査）")
    p.add_argument("--year", help="調査年（例: 2023）")
    p.add_argument("--max", type=int, default=20)
    a = ap.parse_args()

    kind, areas, L = {"lodging": cmd_lodging, "akiya": cmd_akiya, "search": cmd_search}[a.cmd](a)
    out = "\n".join(L) + "\n"
    print(out)
    if not a.no_save:
        name = "_".join(lbl for _, lbl in areas)[:40]
        for ch in '/\\:*?"<>| 　':
            name = name.replace(ch, "_")
        path = ROOT / "docs/sources/estat" / f"{dt.date.today().isoformat()}_{kind}_{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(out, encoding="utf-8")
        print(f"saved {path.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
