#!/usr/bin/env python3
"""改善施策の台帳（docs/seo/experiments.md）を読み書きし、効果を測る（SEO/AIO の PDCA）。

使い方:
  python3 tools/pdca.py new --page /media/xxx.html --type "title・description" --metric CTR --target 2.0%
                                        # 台帳に「計画」の施策を1件足す（ID は自動で振る）
  python3 tools/pdca.py baseline E-20261011-01   # 実施前に、変更前28日のベースラインを取って台帳に書く
  python3 tools/pdca.py check [--dry-run]        # 測定日を迎えた施策の前後28日を比べ、結果と判定を書く
  python3 tools/pdca.py report [--out PATH]      # 台帳の状況を Markdown で出す（環境変数なしで動く）
  共通: --ledger PATH（既定 docs/seo/experiments.md）、--today YYYY-MM-DD（既定は今日。テスト用）

GA4・Search Console からの取得は tools/analytics.py の fetch_page_metrics を使う
（環境変数 GOOGLE_SERVICE_ACCOUNT_JSON が必要。ないときは分かりやすいメッセージで止まる）。

測定のルール（数値は下の定数）:
  - 比較期間: 実施日の前 N 日（実施日−N 〜 実施日−1）と後 N 日（実施日＋1 〜 実施日＋N）。実施日当日は除く。
    N ＝ 測定日 − 実施日（はじめは 28。延長するたびに 28 ずつ伸びる）。
  - check の対象: 状態が「実施済み」「測定中」で、今日が 測定日＋DATA_LAG_DAYS 以降のもの
    （Search Console の数値は 2〜3 日遅れで確定するため）。
  - データ不足: 主指標の母数が前後どちらかで下限未満（MIN_IMPRESSIONS / MIN_SESSIONS）
      → 「保留」にして測定日を 28 日延長（最大 MAX_EXTENSIONS 回。超えたら「判定不能」）。
  - 判定（主指標の「良くなった割合」で見る。掲載順位は小さいほど良い）:
      目標値に届き、改善していて、サイト全体の変化を上回る → 効果あり
      目標値に届いたが、サイト全体の変化を上回らない        → 一部効果（季節要因の可能性）
      目標値に届かないが +10% を超えて改善し、全体を上回る  → 一部効果
      ±10% 以内、または全体並みの改善・低下                → 効果なし
      −10% を超えて悪化し、全体の変化より悪い              → 悪化
"""
import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "seo" / "experiments.md"

# ---- 判定ルールの定数 -------------------------------------------------------
WINDOW_DAYS = 28            # 前後の比較期間（日）
EXTEND_DAYS = 28            # 保留のときに測定日を延ばす日数
MAX_EXTENSIONS = 3          # 延長の上限（これを超えてデータ不足なら「判定不能」）
DATA_LAG_DAYS = 3           # 測定日から何日待ってから check するか（Search Console の確定待ち）
MIN_IMPRESSIONS = 100       # Search Console の指標の母数（表示回数）の下限（各期間）
MIN_SESSIONS = 30           # GA4 の指標の母数（セッション／入口セッション）の下限（各期間）
NO_CHANGE_BAND = 0.10       # ±10% 以内は「変化なし」

STATES = ("計画", "実施済み", "測定中", "判定済み")
VERDICTS = ("効果あり", "一部効果", "効果なし", "悪化", "保留", "判定不能")
TYPES = ("title・description", "本文の書き直し", "内部リンク", "新規記事", "構造化データ・AIO", "技術")
FIELDS = ("状態", "対象ページ", "仮説", "施策の種類", "変更内容", "主指標", "目標値", "副指標",
          "ベースライン", "実施日", "測定日", "延長回数", "結果", "全体の変化", "判定", "判定の理由",
          "次の一手", "関連PR")
START, END = "<!-- pdca:start -->", "<!-- pdca:end -->"
ID_RE = re.compile(r"^E-(\d{8})-(\d{2,})$")

# 指標: 表示名 → (キー, 単位, 向き, 母数のキー, 母数の下限)
#   単位 pct=割合（0〜1 を % で表示）、count=件数、sec=秒、rank=順位。向き up=大きいほど良い、down=小さいほど良い
METRICS = {
    "CTR": ("ctr", "pct", "up", "impressions", MIN_IMPRESSIONS),
    "クリック": ("clicks", "count", "up", "impressions", MIN_IMPRESSIONS),
    "表示回数": ("impressions", "count", "up", "impressions", MIN_IMPRESSIONS),
    "掲載順位": ("position", "rank", "down", "impressions", MIN_IMPRESSIONS),
    "ページビュー": ("views", "count", "up", "sessions", MIN_SESSIONS),
    "セッション": ("sessions", "count", "up", "sessions", MIN_SESSIONS),
    "エンゲージメント率": ("engagement_rate", "pct", "up", "sessions", MIN_SESSIONS),
    "平均エンゲージメント時間": ("avg_engagement_time", "sec", "up", "sessions", MIN_SESSIONS),
    "相談ボタンのクリック": ("cta_clicks", "count", "up", "sessions", MIN_SESSIONS),
    "入口セッション": ("landing_sessions", "count", "up", "landing_sessions", MIN_SESSIONS),
    "相談": ("leads", "count", "up", "landing_sessions", MIN_SESSIONS),
    "相談件数": ("lead_events", "count", "up", "landing_sessions", MIN_SESSIONS),
    "相談率": ("lead_rate", "pct", "up", "landing_sessions", MIN_SESSIONS),
    "サービス移動": ("service_sessions", "count", "up", "landing_sessions", MIN_SESSIONS),
    "サービス移動率": ("service_rate", "pct", "up", "landing_sessions", MIN_SESSIONS),
    "AI検索流入": ("ai_sessions", "count", "up", "landing_sessions", MIN_SESSIONS),
}
KEY2LABEL = {v[0]: k for k, v in METRICS.items()}
BASE_LABEL = {"impressions": "表示回数", "sessions": "セッション", "landing_sessions": "入口セッション"}


def metric_info(name):
    """表示名（CTR など）または内部キー（ctr など）から指標の定義を返す。"""
    name = (name or "").strip()
    if name in METRICS:
        return (name,) + METRICS[name]
    if name in KEY2LABEL:
        return (KEY2LABEL[name],) + METRICS[KEY2LABEL[name]]
    raise ValueError(f"未知の指標です: {name!r}（使える指標: {'、'.join(METRICS)}）")


# ---- 台帳の読み書き ---------------------------------------------------------
def parse_ledger(text):
    """台帳を (前置き, 施策のリスト, 後書き) に分ける。施策は dict（id・title・各項目・_extra）。
    <!-- pdca:start --> と <!-- pdca:end --> の間だけを読む（書式見本・記入例はその外のコードブロックに置く）。"""
    if START not in text or END not in text:
        raise ValueError(f"台帳に {START} と {END} がありません")
    head, rest = text.split(START, 1)
    body, tail = rest.split(END, 1)
    exps, cur = [], None
    for line in body.splitlines():
        m = re.match(r"^###\s+(E-\d{8}-\d{2,})\s*(.*)$", line)
        if m:
            cur = {"id": m.group(1), "title": m.group(2).strip(), "_extra": []}
            exps.append(cur)
            continue
        if cur is None:
            continue
        f = re.match(r"^-\s*([^:：]+?)\s*[:：]\s?(.*)$", line)
        if f and f.group(1) in FIELDS:
            cur[f.group(1)] = f.group(2).strip()
        elif line.strip():
            cur["_extra"].append(line.rstrip())
    return head + START, exps, END + tail


def render_exp(e):
    L = [f"### {e['id']}" + (f" {e['title']}" if e.get("title") else "")]
    for k in FIELDS:
        v = str(e.get(k, "") or "").replace("\n", " ").strip()
        L.append(f"- {k}: {v}" if v else f"- {k}:")
    L += e.get("_extra", [])
    return "\n".join(L)


def render_ledger(head, exps, tail):
    body = "\n\n".join(render_exp(e) for e in exps)
    return head + "\n\n" + (body + "\n\n" if body else "") + tail


def load(path):
    return parse_ledger(Path(path).read_text(encoding="utf-8"))


def save(path, head, exps, tail):
    Path(path).write_text(render_ledger(head, exps, tail), encoding="utf-8")


def next_id(exps, today):
    prefix = f"E-{today:%Y%m%d}-"
    n = [int(e["id"].rsplit("-", 1)[1]) for e in exps if e["id"].startswith(prefix)]
    return f"{prefix}{(max(n) + 1 if n else 1):02d}"


def find(exps, eid):
    for e in exps:
        if e["id"] == eid:
            return e
    raise SystemExit(f"台帳に {eid} がありません")


# ---- 値の扱い ---------------------------------------------------------------
def parse_date(s):
    s = (s or "").strip()
    m = re.search(r"\d{4}-\d{2}-\d{2}", s)
    return dt.date.fromisoformat(m.group(0)) if m else None


def fmt(v, unit):
    if v is None:
        return "—"
    if unit == "pct":
        return f"{v * 100:.2f}%"
    if unit == "sec":
        return f"{v:.1f}秒"
    if unit == "rank":
        return f"{v:.1f}位"
    return f"{v:.0f}"


def parse_target(text, unit, before=None):
    """目標値の文字列を数値にする。
    "2.0%"（割合の指標は 0.02）、"120秒"、"8位"、"50"、"1.2%→2.0%"（矢印の後ろを使う）、
    "+20%"・"-15%"（符号つきは before からの相対。before がないと None）。空なら None。"""
    t = (text or "").strip()
    if not t:
        return None
    if "→" in t:
        t = t.split("→")[-1].strip()
    m = re.match(r"^([+\-−])\s*([\d.]+)\s*%$", t)
    if m:
        if before is None:
            return None
        r = float(m.group(2)) / 100 * (-1 if m.group(1) in "-−" else 1)
        return before * (1 + r)
    m = re.match(r"^([\d.]+)\s*(%|秒|位|件|回)?", t)
    if not m:
        raise ValueError(f"目標値を読めません: {text!r}")
    v = float(m.group(1))
    return v / 100 if unit == "pct" and m.group(2) == "%" else v


def improvement(before, after, direction):
    """良くなった割合（正なら改善）。before が 0 のときは after>0 で +inf、同じなら 0。"""
    if before is None or after is None:
        return None
    if before == 0:
        if after == before:
            return 0.0
        return float("inf") if (after > 0) == (direction == "up") else float("-inf")
    r = (after - before) / abs(before)
    return r if direction == "up" else -r


def pct(r):
    if r is None:
        return "—"
    if r in (float("inf"), float("-inf")):
        return "（0から変化）"
    return f"{r * 100:+.1f}%"


def judge(metric, before, after, target_text="", site_before=None, site_after=None, extensions=0):
    """判定する。before/after/site_* は fetch_page_metrics の返り値（dict）。
    返り値: {"verdict", "reason", "rel", "site_rel", "before", "after", "target", "sample"}"""
    label, key, unit, direction, base_key, base_min = metric_info(metric)
    b, a = before.get(key), after.get(key)
    sb, sa = before.get(base_key, 0) or 0, after.get(base_key, 0) or 0
    res = {"before": b, "after": a, "rel": None, "site_rel": None, "target": None,
           "sample": (sb, sa), "label": label, "unit": unit}
    if sb < base_min or sa < base_min:
        why = (f"データ不足: {BASE_LABEL[base_key]}が 前 {sb:.0f}／後 {sa:.0f}"
               f"（各期間 {base_min} 以上が必要）")
        if extensions >= MAX_EXTENSIONS:
            res.update(verdict="判定不能", reason=f"{why}。延長 {extensions} 回でも足りないため判定不能")
        else:
            res.update(verdict="保留", reason=f"{why}。測定日を {EXTEND_DAYS} 日延長")
        return res
    rel = improvement(b, a, direction)
    site_rel = None
    if site_before is not None and site_after is not None:
        site_rel = improvement(site_before.get(key), site_after.get(key), direction)
    target = parse_target(target_text, unit, b)
    beats = site_rel is None or rel > site_rel
    reached = target is not None and (a >= target if direction == "up" else a <= target)
    res.update(rel=rel, site_rel=site_rel, target=target)
    vs = "" if site_rel is None else f"／サイト全体 {pct(site_rel)}"
    head = f"{label} {fmt(b, unit)}→{fmt(a, unit)}（{pct(rel)}）{vs}"
    tgt = f"目標 {fmt(target, unit)}" if target is not None else "目標なし"
    if reached and rel > 0 and beats:
        v, why = "効果あり", f"{tgt}に到達し、全体の変化を上回った"
    elif reached and rel > 0:
        v, why = "一部効果", f"{tgt}に到達したが、全体の変化を上回らない（季節要因の可能性）"
    elif rel > NO_CHANGE_BAND and beats:
        v, why = "一部効果", f"{tgt}には届かないが改善し、全体の変化を上回った"
    elif rel > NO_CHANGE_BAND:
        v, why = "効果なし", "改善したが全体並み（季節要因・サイト全体の伸びの範囲）"
    elif rel >= -NO_CHANGE_BAND:
        v, why = "効果なし", f"変化が ±{NO_CHANGE_BAND * 100:.0f}% 以内"
    elif site_rel is None or rel < site_rel:
        v, why = "悪化", f"{NO_CHANGE_BAND * 100:.0f}% を超えて悪化し、全体の変化より悪い"
    else:
        v, why = "効果なし", "低下したが全体並み（季節要因の可能性）"
    res.update(verdict=v, reason=f"{head}。{why}")
    return res


def periods(implemented, measure):
    n = (measure - implemented).days
    d = dt.timedelta
    return (implemented - d(days=n), implemented - d(days=1)), (implemented + d(days=1), implemented + d(days=n))


def page_of(e):
    p = (e.get("対象ページ") or "").strip().strip("`")
    return None if p in ("", "サイト全体", "全体", "*") else p


def sub_metrics(e):
    return [x.strip() for x in re.split(r"[、,，]", e.get("副指標", "") or "") if x.strip()]


def describe(metrics_list, data):
    out = []
    for name in metrics_list:
        try:
            label, key, unit, *_ = metric_info(name)
        except ValueError:
            continue
        out.append(f"{label} {fmt(data.get(key), unit)}")
    return "、".join(out)


def describe_change(metrics_list, b, a):
    out = []
    for name in metrics_list:
        try:
            label, key, unit, direction, *_ = metric_info(name)
        except ValueError:
            out.append(f"{name}（未知の指標）")
            continue
        out.append(f"{label} {fmt(b.get(key), unit)}→{fmt(a.get(key), unit)}（{pct(improvement(b.get(key), a.get(key), direction))}）")
    return "、".join(out)


# ---- 取得 -------------------------------------------------------------------
def require_env():
    if not os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON"):
        sys.exit("環境変数 GOOGLE_SERVICE_ACCOUNT_JSON が未設定のため、GA4・Search Console から数値を取れません。\n"
                 "  設定方法: docs/seo/analytics-setup.md\n"
                 "  台帳の状況だけ見るなら: python3 tools/pdca.py report")


def default_fetcher():
    require_env()
    sys.path.insert(0, str(ROOT / "tools"))
    import analytics
    s = analytics.session()
    cache = {}

    def fetch(page, start, end):
        k = (page, start, end)
        if k not in cache:
            cache[k] = analytics.fetch_page_metrics(page, start.isoformat(), end.isoformat(), s=s)
        return cache[k]
    return fetch


# ---- コマンド ---------------------------------------------------------------
def due(e, today):
    if e.get("状態") not in ("実施済み", "測定中"):
        return False
    imp = parse_date(e.get("実施日"))
    if not imp:
        return False
    meas = parse_date(e.get("測定日")) or imp + dt.timedelta(days=WINDOW_DAYS)
    return today >= meas + dt.timedelta(days=DATA_LAG_DAYS)


def check_one(e, today, fetch):
    """1件を測って e を書き換える。判定の dict を返す。"""
    imp = parse_date(e["実施日"])
    meas = parse_date(e.get("測定日")) or imp + dt.timedelta(days=WINDOW_DAYS)
    (bs, be), (as_, ae) = periods(imp, meas)
    page = page_of(e)
    b, a = fetch(page, bs, be), fetch(page, as_, ae)
    sb, sa = (fetch(None, bs, be), fetch(None, as_, ae)) if page else (None, None)
    ext = int(re.sub(r"\D", "", e.get("延長回数", "") or "0") or 0)
    j = judge(e.get("主指標", ""), b, a, e.get("目標値", ""), sb, sa, ext)
    label, key, unit, direction, base_key, _ = metric_info(e.get("主指標", ""))
    span = f"前 {bs}〜{be}・後 {as_}〜{ae}（各 {(be - bs).days + 1} 日、実施日当日を除く）"
    parts = [f"{label} {fmt(j['before'], unit)}→{fmt(j['after'], unit)}（{pct(j['rel'])}）",
             f"母数 {BASE_LABEL[base_key]} {j['sample'][0]:.0f}→{j['sample'][1]:.0f}"]
    if sub_metrics(e):
        parts.append("副指標: " + describe_change(sub_metrics(e), b, a))
    parts.append(f"比較期間 {span}")
    e["結果"] = "／".join(parts)
    if sb is not None:
        e["全体の変化"] = (f"サイト全体 {label} {fmt(sb.get(key), unit)}→{fmt(sa.get(key), unit)}"
                       f"（{pct(improvement(sb.get(key), sa.get(key), direction))}）")
        if j["rel"] is not None and j["site_rel"] is not None:
            diff = j["rel"] - j["site_rel"]
            e["全体の変化"] += ("／対象ページは全体を上回る" if diff > 0 else "／対象ページは全体を上回らない")
    else:
        e["全体の変化"] = "（対象がサイト全体のため比較なし）"
    e["判定"] = j["verdict"]
    e["判定の理由"] = f"{j['reason']}（{today} 判定）"
    if j["verdict"] == "保留":
        e["測定日"] = (meas + dt.timedelta(days=EXTEND_DAYS)).isoformat()
        e["延長回数"] = str(ext + 1)
        e["状態"] = "測定中"
    else:
        e["測定日"] = meas.isoformat()
        e["延長回数"] = str(ext)
        e["状態"] = "判定済み"
    return j


def cmd_check(path, today, fetch=None, dry_run=False, out=print):
    head, exps, tail = load(path)
    changed = False
    for e in exps:  # 実施済みで測定日が空なら埋める
        imp = parse_date(e.get("実施日"))
        if e.get("状態") in ("実施済み", "測定中") and imp and not parse_date(e.get("測定日")):
            e["測定日"] = (imp + dt.timedelta(days=WINDOW_DAYS)).isoformat()
            changed = True
        if e.get("状態") == "実施済み" and imp and imp < today:
            e["状態"] = "測定中"
            changed = True
    targets = [e for e in exps if due(e, today)]
    if not targets:
        out(f"測定日を迎えた施策はありません（{today}。測定日＋{DATA_LAG_DAYS}日以降が対象）")
    else:
        fetch = fetch or default_fetcher()
        for e in targets:
            j = check_one(e, today, fetch)
            out(f"- {e['id']}: {j['verdict']} — {j['reason']}")
        changed = True
    if changed and not dry_run:
        save(path, head, exps, tail)
    return exps


def cmd_baseline(path, eid, today, fetch=None, out=print):
    head, exps, tail = load(path)
    e = find(exps, eid)
    label, key, unit, direction, base_key, _ = metric_info(e.get("主指標", ""))
    imp = parse_date(e.get("実施日"))
    end = imp - dt.timedelta(days=1) if imp and imp <= today else today - dt.timedelta(days=DATA_LAG_DAYS)
    start = end - dt.timedelta(days=WINDOW_DAYS - 1)
    fetch = fetch or default_fetcher()
    d = fetch(page_of(e), start, end)
    s = f"{label} {fmt(d.get(key), unit)}（{BASE_LABEL[base_key]} {d.get(base_key, 0):.0f}）"
    if sub_metrics(e):
        s += "／副指標: " + describe(sub_metrics(e), d)
    s += f"／期間 {start}〜{end}（{WINDOW_DAYS} 日、{today} 取得）"
    e["ベースライン"] = s
    save(path, head, exps, tail)
    out(f"{eid} のベースライン: {s}")
    return e


def cmd_new(path, today, page, typ, metric, target, title="", out=print):
    head, exps, tail = load(path)
    metric_info(metric)
    if typ not in TYPES:
        raise SystemExit(f"施策の種類は {'／'.join(TYPES)} のどれか: {typ!r}")
    e = {"id": next_id(exps, today), "title": title, "_extra": [], "状態": "計画", "対象ページ": page,
         "施策の種類": typ, "主指標": metric, "目標値": target, "延長回数": "0"}
    exps.append(e)
    save(path, head, exps, tail)
    out(f"{e['id']} を台帳に追加しました（仮説・変更内容・副指標を記入してください）")
    return e


def build_report(exps, today):
    L = [f"## 改善施策（PDCA）の状況（{today} 時点・`python3 tools/pdca.py report`）", ""]
    if not exps:
        return "\n".join(L + ["- 台帳（docs/seo/experiments.md）に施策はまだありません", ""])
    by_state = {s: [e for e in exps if e.get("状態") == s] for s in STATES}
    L += ["| 計画 | 実施済み | 測定中 | 判定済み | 合計 |", "|---|---|---|---|---|",
          "| " + " | ".join(str(len(by_state[s])) for s in STATES) + f" | {len(exps)} |", ""]
    done = by_state["判定済み"]
    if done:
        cnt = {v: sum(1 for e in done if e.get("判定") == v) for v in VERDICTS}
        L += ["判定の内訳: " + "、".join(f"{v} {n}" for v, n in cnt.items() if n), ""]
        L += ["### 施策の種類別の効果（判定済み。判定不能を除く）", "",
              "| 施策の種類 | 判定済み | 効果あり | 一部効果 | 効果ありの割合 |", "|---|---|---|---|---|"]
        types = list(TYPES) + sorted({e.get("施策の種類", "") for e in done} - set(TYPES))
        for t in types:
            rows = [e for e in done if e.get("施策の種類") == t and e.get("判定") != "判定不能"]
            if not rows:
                continue
            ok = sum(1 for e in rows if e.get("判定") == "効果あり")
            part = sum(1 for e in rows if e.get("判定") == "一部効果")
            L.append(f"| {t or '（未記入）'} | {len(rows)} | {ok} | {part} | {ok / len(rows) * 100:.0f}% |")
        L.append("")
    meas = sorted(by_state["測定中"] + by_state["実施済み"], key=lambda e: e.get("測定日") or "9999")
    if meas:
        L += ["### 測定待ち", ""]
        for e in meas:
            m = parse_date(e.get("測定日"))
            ready = m and today >= m + dt.timedelta(days=DATA_LAG_DAYS)
            L.append(f"- {e['id']} `{e.get('対象ページ', '')}` {e.get('主指標', '')} 測定日 {e.get('測定日') or '未定'}"
                     + (f"（延長 {e.get('延長回数')} 回）" if (e.get("延長回数") or "0") not in ("", "0") else "")
                     + ("　← check の対象" if ready else ""))
        L.append("")
    if by_state["計画"]:
        L += ["### 計画中", ""]
        L += [f"- {e['id']} `{e.get('対象ページ', '')}` {e.get('施策の種類', '')}"
              + ("" if e.get("ベースライン") else "（ベースライン未取得）") for e in by_state["計画"]]
        L.append("")
    recent = [e for e in done if e.get("判定") in ("効果あり", "一部効果", "悪化")][-5:]
    if recent:
        L += ["### 最近の判定（効果あり・一部効果・悪化）", ""]
        L += [f"- {e['id']} {e.get('判定')}: {e.get('判定の理由', '')}" for e in recent]
        L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="SEO/AIO の改善施策の台帳と効果測定")
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--today", help="今日の日付（YYYY-MM-DD。テスト用）")
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("check")
    c.add_argument("--dry-run", action="store_true", help="台帳に書かずに結果だけ表示")
    b = sp.add_parser("baseline")
    b.add_argument("id")
    r = sp.add_parser("report")
    r.add_argument("--out")
    n = sp.add_parser("new")
    n.add_argument("--page", required=True)
    n.add_argument("--type", required=True, choices=TYPES)
    n.add_argument("--metric", required=True)
    n.add_argument("--target", default="")
    n.add_argument("--title", default="")
    a = ap.parse_args(argv)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    if a.cmd == "check":
        cmd_check(a.ledger, today, dry_run=a.dry_run)
    elif a.cmd == "baseline":
        cmd_baseline(a.ledger, a.id, today)
    elif a.cmd == "new":
        cmd_new(a.ledger, today, a.page, a.type, a.metric, a.target, a.title)
    else:
        _, exps, _ = load(a.ledger)
        md = build_report(exps, today)
        if a.out:
            Path(a.out).write_text(md + "\n", encoding="utf-8")
        print(md)


if __name__ == "__main__":
    main()
