"""SEO/AIO の CV 計画（シミュレーション）と、計画に対する毎日の進捗チェック・週次レポート

前提は docs/seo/plan.json。計画は docs/seo/plan.md、毎日の記録は docs/seo/plan-tracking.md、
週次レポートは docs/seo/reports/weekly-YYYY-Www.md に書き出す。

使い方:
  python3 tools/plan.py simulate            # 前提から月別の計画を作り直す（API 不要）
  python3 tools/plan.py check               # 今月の実績を取り、計画の日割りと比べる（毎日。要 GA4/GSC の環境変数）
  python3 tools/plan.py weekly              # 先週（月〜日）の週次レポートを作る（毎週月曜）
  python3 tools/plan.py check --dry-run     # 記録ファイルに書かずに表示だけ

KPI のつながり（計画の木）:
  CV（お問い合わせ完了 generate_lead。うち資料請求・相談）
    = SEO/AIO からのセッション × CV率
  SEO/AIO からのセッション = 検索のクリック（Search Console）＋ AI 検索からの流入（GA4）
  検索のクリック = 表示回数 × クリック率（CTR）
  表示回数 ← 記事の本数 × 1本あたりの立ち上がり（公開からの月数）
"""
import argparse
import calendar
import datetime as dt
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_JSON = ROOT / "docs" / "seo" / "plan.json"
PLAN_MD = ROOT / "docs" / "seo" / "plan.md"
TRACKING_MD = ROOT / "docs" / "seo" / "plan-tracking.md"
REPORT_DIR = ROOT / "docs" / "seo" / "reports"
JST = dt.timezone(dt.timedelta(hours=9))

KPI = [  # (キー, 名前, 単位)
    ("impressions", "検索の表示回数", "回"),
    ("clicks", "検索のクリック", "回"),
    ("ai_sessions", "AI検索からの流入", "セッション"),
    ("seo_sessions", "SEO/AIO からのセッション", "セッション"),
    ("cv", "CV（SEO/AIO 経由）", "件"),
]

# 遅れている指標ごとの打ち手（日次の PDCA で marketer に渡す）
LEVERS = {
    "impressions": "表示回数が足りない → 記事の本数とインデックスを増やす：Search Console で未登録のページを確認、新規記事を計画どおり出す、内部リンクで新しい記事に回遊させる、キーワード表の優先度「高」から書く",
    "clicks": "クリックが足りない（表示はある）→ クリック率を上げる：表示回数100回以上・CTR1%未満の記事の title と説明文を直す、FAQ の構造化データを整える",
    "ai_sessions": "AI検索からの流入が足りない → 引用されやすくする：記事冒頭の「この記事のポイント」を結論から書く、一次情報（運営実績・数字）を足す、llms.txt に新しい記事を載せる、Bing の登録・サイトマップを確認",
    "seo_sessions": "流入が足りない → 上の表示回数・クリック・AI検索のうち、いちばん遅れている指標の打ち手を優先する",
    "cv": "CV が足りない（流入はある）→ CV率を上げる：流入の多い記事に資料請求・相談の導線（記事中のボタン、関連サービス）を足す、資料請求の訴求（収支シミュレーションが分かる資料）を記事に入れる、フォームの離脱を Clarity で確認",
}


def load_plan(path=PLAN_JSON):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def month_add(ym, n):
    y, m = map(int, ym.split("-"))
    m += n
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    return f"{y:04d}-{m:02d}"


def ramp(age, half, width):
    """公開から age か月（その月の真ん中で数える）の記事が、最大のどれだけ読まれるか（0〜1）"""
    return 1.0 / (1.0 + math.exp(-((age + 0.5) - half) / width))


def simulate(plan, scenario_key):
    sc = plan["scenarios"][scenario_key]
    half, width = plan["ramp"]["half"], plan["ramp"]["width"]
    doc_share = plan["lead_split"]["document"]
    cohorts = []  # (公開月の番号, 本数)
    rows, cum = [], 0.0
    for i in range(plan["months"]):
        ym = month_add(plan["start_month"], i)
        cohorts.append((i, plan["articles_at_start"] if i == 0 else plan["new_articles_per_month"]))
        articles = sum(n for _, n in cohorts)
        clicks = sum(n * sc["clicks_per_article"] * ramp(i - j, half, width) for j, n in cohorts)
        impressions = clicks / sc["ctr"]
        ai = clicks * sc["ai_share"]
        seo = clicks + ai
        cv = seo * sc["cvr"]
        cum += cv
        rows.append({"month": ym, "articles": articles, "impressions": impressions, "clicks": clicks,
                     "ai_sessions": ai, "seo_sessions": seo, "cv": cv,
                     "cv_document": cv * doc_share, "cv_consult": cv * (1 - doc_share), "cv_cum": cum})
    return rows


def first_month(rows, key, threshold):
    for r in rows:
        if r[key] >= threshold:
            return r["month"]
    return "（12か月以内には届かない）"


def ym_label(ym):
    y, m = ym.split("-")
    return f"{y}年{int(m)}月"


def fmt(v, digits=0):
    if digits == 0:
        return f"{round(v):,}"
    return f"{v:,.{digits}f}"


def render_plan(plan):
    out = []
    w = out.append
    tgt = plan["target_scenario"]
    res = {k: simulate(plan, k) for k in plan["scenarios"]}
    std = res[tgt]
    last = std[-1]
    w("# SEO/AIO の CV 計画（シミュレーション）")
    w("")
    w(f"> `python3 tools/plan.py simulate` で `docs/seo/plan.json` から自動生成（手で編集しない）。最終更新: {dt.datetime.now(JST).date()}")
    w("")
    w("## 1. 結論（標準シナリオ＝目標）")
    w("")
    w(f"- 計画の期間: {ym_label(std[0]['month'])}〜{ym_label(last['month'])}（{plan['months']}か月）。記事は {plan['articles_at_start']} 本から、毎月 {plan['new_articles_per_month']} 本ずつ増やす")
    w(f"- **SEO/AIO 経由の CV が月1件を超えるのは {ym_label(first_month(std, 'cv', 1))}、月3件を超えるのは {ym_label(first_month(std, 'cv', 3)) if '（' not in first_month(std, 'cv', 3) else first_month(std, 'cv', 3)}**")
    w(f"- {ym_label(last['month'])}の目標: **CV 月{fmt(last['cv'], 1)}件**（資料請求 {fmt(last['cv_document'], 1)}・相談 {fmt(last['cv_consult'], 1)}）、SEO/AIO からのセッション 月{fmt(last['seo_sessions'])}、検索の表示回数 月{fmt(last['impressions'])}")
    w(f"- 12か月の CV 累計: 保守 {fmt(res['conservative'][-1]['cv_cum'], 1)}件 ／ **標準 {fmt(last['cv_cum'], 1)}件** ／ 挑戦 {fmt(res['stretch'][-1]['cv_cum'], 1)}件")
    w("- 最初の3〜4か月は、新しいサイトが検索エンジンに評価されるまでの「立ち上がり期間」。この時期は CV ではなく、**表示回数・インデックス・記事の本数（先行指標）** で進み具合を判断する")
    w("")
    w("## 2. 計画の木（どの数字を伸ばせば CV が増えるか）")
    w("")
    w("```")
    w("CV（お問い合わせ完了。資料請求＋相談）")
    w(" = SEO/AIO からのセッション × CV率")
    w("     ├ 検索のクリック = 表示回数 × クリック率（CTR）")
    w("     │                  └ 表示回数 ← 記事の本数 × 公開からの月数（立ち上がり）")
    w("     └ AI検索からの流入（ChatGPT・Perplexity・Gemini など）")
    w("```")
    w("")
    w("毎日の PDCA では、この木の上から順に（表示回数 → クリック → AI検索 → CV）計画との差を見て、いちばん遅れている指標の打ち手から実行する（`tools/plan.py` の LEVERS）。")
    w("")
    w("## 3. 前提（`docs/seo/plan.json`）")
    w("")
    w("| 項目 | 保守 | 標準（目標） | 挑戦 | 根拠・考え方 |")
    w("|---|---|---|---|---|")
    sc = plan["scenarios"]
    w(f"| 1記事が育ちきったときの検索クリック（月） | {sc['conservative']['clicks_per_article']} | {sc['standard']['clicks_per_article']} | {sc['stretch']['clicks_per_article']} | 仮定。空き家・民泊のロングテール（地域名・手続き名などの具体的な検索）を狙う記事の想定。実績が出たら見直す |")
    w(f"| クリック率（CTR） | {sc['conservative']['ctr']:.1%} | {sc['standard']['ctr']:.1%} | {sc['stretch']['ctr']:.1%} | 仮定。表示回数の目安を出すために使う（平均順位10〜20位台を想定） |")
    w(f"| AI検索からの流入（検索クリックに対する割合） | {sc['conservative']['ai_share']:.0%} | {sc['standard']['ai_share']:.0%} | {sc['stretch']['ai_share']:.0%} | 仮定。GA4 の「AI検索」チャネルの実績で見直す |")
    w(f"| CV率（SEO/AIO からのセッションあたり） | {sc['conservative']['cvr']:.1%} | {sc['standard']['cvr']:.1%} | {sc['stretch']['cvr']:.1%} | 仮定。情報を調べる段階の読者が中心のメディアとして控えめに置き、資料請求（低いハードル）で上積みする |")
    w(f"| 立ち上がり | 公開から約{plan['ramp']['half']}か月で最大の半分 | 同 | 同 | 新しいドメインは評価に時間がかかる前提 |")
    w(f"| 記事の本数 | {plan['articles_at_start']}本＋毎月{plan['new_articles_per_month']}本 | 同 | 同 | 2026年10月時点の公開済み50本＋毎日の定期実行（週1本ペース） |")
    w(f"| CV の内訳 | 資料請求 {plan['lead_split']['document']:.0%}・相談 {1 - plan['lead_split']['document']:.0%} | 同 | 同 | 仮定。資料請求はハードルが低いため多めに置く |")
    w("")
    w("**注意**：数字は仮定によるシミュレーションで、成果を約束するものではない。会社のサイト（トップ・サービスページ）への直接の来訪や紹介からの CV は、この計画に含めない（SEO/AIO の効果だけを見るため）。")
    w("")
    w("## 4. 月別の計画（標準＝目標）")
    w("")
    w("| 月 | 記事数 | 表示回数 | 検索クリック | AI検索 | SEO/AIOセッション | CV | うち資料請求 | うち相談 | CV累計 |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for r in std:
        w(f"| {r['month']} | {r['articles']} | {fmt(r['impressions'])} | {fmt(r['clicks'])} | {fmt(r['ai_sessions'])} | {fmt(r['seo_sessions'])} | {fmt(r['cv'], 1)} | {fmt(r['cv_document'], 1)} | {fmt(r['cv_consult'], 1)} | {fmt(r['cv_cum'], 1)} |")
    w("")
    w("## 5. シナリオ別の CV（月）")
    w("")
    w("| 月 | 保守 | 標準（目標） | 挑戦 |")
    w("|---|---|---|---|")
    for a, b, c in zip(res["conservative"], std, res["stretch"]):
        w(f"| {b['month']} | {fmt(a['cv'], 1)} | **{fmt(b['cv'], 1)}** | {fmt(c['cv'], 1)} |")
    w("")
    w("## 6. 進め方（PDCA）と見直しのルール")
    w("")
    w("- **毎日（Check→Act）**：定期実行の最初に `python3 tools/plan.py check` で今月の実績を取り、計画の日割りと比べる（順調 ≥ {:.0%}・注意 ≥ {:.0%}・遅れ）。遅れている指標のうち、計画の木の上流にあるものの打ち手を、その日の作業の1つ目にする。結果は `docs/seo/plan-tracking.md` に1行ずつ残る".format(plan["pace_thresholds"]["on_track"], plan["pace_thresholds"]["warn"]))
    w("- **毎週月曜（報告）**：`python3 tools/plan.py weekly` で先週の週次レポートを作り、定期実行の完了メールと PR に要点を載せる")
    w("- **毎月1日（Plan の見直し）**：前月の実績で、仮定（1記事あたりのクリック・CTR・AI検索の割合・CV率）を見直す。**2か月続けて「遅れ」なら、仮定ではなく打ち手を変える**（記事のテーマ・導線・本数）。計画そのものを下げるときは、PR の「人の確認が必要な点」に理由を書いて人の判断を仰ぐ")
    w("- 立ち上がり期間（最初の3か月）は CV の数が小さく、日割りの判定がぶれやすい。この期間は表示回数・クリックの判定を優先する")
    w("")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- 実績の取得
def fetch_actuals(start, end, gsc_end=None):
    """start〜end（YYYY-MM-DD）の実績。Search Console は2〜3日遅れて確定するので gsc_end までで取る。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import analytics
    s = analytics.session()
    prop = os.environ.get("GA4_PROPERTY_ID", "556922741")
    site = os.environ.get("GSC_SITE_URL", "https://rivia-co.com/")
    g = analytics.gsc_total(s, site, start, gsc_end or end)
    ch = analytics.ga4_run(s, prop, start, end, ["sessionDefaultChannelGroup"], ["sessions", "keyEvents"])
    organic = [r for r in ch if r["sessionDefaultChannelGroup"] == "Organic Search"]
    ai = analytics.ga4_run(s, prop, start, end, [], ["sessions", "keyEvents"], analytics.ai_filter())
    org_sessions = sum(r["sessions"] for r in organic)
    org_cv = sum(r["keyEvents"] for r in organic)
    ai_sessions = sum(r["sessions"] for r in ai)
    ai_cv = sum(r["keyEvents"] for r in ai)
    leads = analytics.ga4_custom_breakdown(s, prop, start, end, "generate_lead", "lead_type")
    lead_types = {} if leads == analytics.UNREGISTERED else {r["value"]: r["eventCount"] for r in leads}
    return {"impressions": g["impressions"], "clicks": g["clicks"], "position": g["position"],
            "organic_sessions": org_sessions, "ai_sessions": ai_sessions,
            "seo_sessions": org_sessions + ai_sessions, "cv": org_cv + ai_cv,
            "lead_types": lead_types}


def plan_for_month(plan, ym):
    rows = simulate(plan, plan["target_scenario"])
    for r in rows:
        if r["month"] == ym:
            return r
    return None


def judge(ratio, th, small=False):
    if small:
        return "判定には早い"
    if ratio >= th["on_track"]:
        return "順調"
    if ratio >= th["warn"]:
        return "注意"
    return "遅れ"


def pace_table(plan, target, actual, frac_ga4, frac_gsc):
    th = plan["pace_thresholds"]
    rows = []
    for key, name, unit in KPI:
        frac = frac_gsc if key in ("impressions", "clicks") else frac_ga4
        exp = target[key] * frac
        act = actual.get(key, 0.0)
        ratio = act / exp if exp > 0 else 0.0
        small = exp < (1 if key == "cv" else 5)
        rows.append({"key": key, "name": name, "unit": unit, "expected": exp, "actual": act,
                     "monthly": target[key], "ratio": ratio, "status": judge(ratio, th, small)})
    return rows


def bottleneck(rows):
    """計画の木の上流から見て、最初に「遅れ」（なければ「注意」）の指標"""
    for level in ("遅れ", "注意"):
        for key in ("impressions", "clicks", "ai_sessions", "cv"):
            r = next(x for x in rows if x["key"] == key)
            if r["status"] == level:
                return r
    return None


def cmd_check(plan, today, fetch=fetch_actuals, dry_run=False, out=print):
    ym = today.strftime("%Y-%m")
    target = plan_for_month(plan, ym)
    if not target:
        out(f"{ym} は計画の期間外です（docs/seo/plan.json の start_month・months を確認）")
        return None
    first = today.replace(day=1)
    days = calendar.monthrange(today.year, today.month)[1]
    ga4_end = today - dt.timedelta(days=1)          # 昨日まで
    gsc_end = today - dt.timedelta(days=3)          # Search Console は約3日遅れ
    if ga4_end < first:
        out("月初のため、今月の実績はまだありません（明日から判定します）")
        return None
    frac_ga4 = ga4_end.day / days
    frac_gsc = max(gsc_end.day, 0) / days if gsc_end >= first else 0.0
    actual = fetch(first.isoformat(), ga4_end.isoformat(), gsc_end.isoformat() if gsc_end >= first else first.isoformat())
    rows = pace_table(plan, target, actual, frac_ga4, frac_gsc)
    b = bottleneck(rows)
    out(f"## 計画に対する進み具合（{ym}・{ga4_end} まで）")
    out("")
    out("| 指標 | 今月の実績 | 計画（日割り） | 進み具合 | 判定 | 今月の計画 |")
    out("|---|---|---|---|---|---|")
    for r in rows:
        out(f"| {r['name']} | {fmt(r['actual'], 1 if r['key'] == 'cv' else 0)} | {fmt(r['expected'], 1)} | {r['ratio']:.0%} | {r['status']} | {fmt(r['monthly'], 1 if r['key'] == 'cv' else 0)} |")
    lt = actual.get("lead_types") or {}
    if lt:
        out("")
        out("お問い合わせの内訳（全チャネル）: " + "、".join(f"{k or '（なし）'} {int(v)}件" for k, v in lt.items()))
    out("")
    if b:
        out(f"**今日の最優先**：{b['name']}が{b['status']}（{b['ratio']:.0%}）。{LEVERS[b['key']]}")
    else:
        out("**今日の最優先**：大きな遅れはなし。計画どおり新規記事・既存記事の改善を進める")
    if not dry_run:
        line = (f"| {today} | {fmt(actual['impressions'])} | {fmt(actual['clicks'])} | {fmt(actual['ai_sessions'])} | "
                f"{fmt(actual['seo_sessions'])} | {fmt(actual['cv'], 1)} | "
                + " ".join(f"{r['name'][:6]}:{r['status']}" for r in rows) + f" | {b['name'] if b else '—'} |")
        if not TRACKING_MD.exists():
            TRACKING_MD.write_text("# 計画に対する毎日の記録（tools/plan.py check が追記）\n\n"
                                   "数字は、その月の1日から前日まで（検索は約3日前まで）の累計。\n\n"
                                   "| 日付 | 表示回数 | 検索クリック | AI検索 | SEO/AIOセッション | CV | 判定 | 最優先の指標 |\n"
                                   "|---|---|---|---|---|---|---|---|\n", encoding="utf-8")
        with TRACKING_MD.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    return {"rows": rows, "bottleneck": b, "actual": actual}


def cmd_weekly(plan, today, fetch=fetch_actuals, out=print):
    """先週（月〜日）のレポート。今日が何曜日でも、直近の完了した週を対象にする。"""
    last_sun = today - dt.timedelta(days=today.isoweekday())
    mon = last_sun - dt.timedelta(days=6)
    prev_mon, prev_sun = mon - dt.timedelta(days=7), mon - dt.timedelta(days=1)
    gsc_end = min(last_sun, today - dt.timedelta(days=3))
    cur = fetch(mon.isoformat(), last_sun.isoformat(), gsc_end.isoformat())
    prev = fetch(prev_mon.isoformat(), prev_sun.isoformat(), prev_sun.isoformat())
    target = plan_for_month(plan, last_sun.strftime("%Y-%m")) or {}
    days = calendar.monthrange(last_sun.year, last_sun.month)[1]
    iso = last_sun.isocalendar()
    lines = []
    w = lines.append
    w(f"# 週次レポート {iso[0]}年 第{iso[1]}週（{mon}〜{last_sun}）")
    w("")
    w("> `python3 tools/plan.py weekly` で自動生成。計画は `docs/seo/plan.md`")
    w("")
    w("## 1. 先週の数字（計画との比較）")
    w("")
    w("| 指標 | 先週 | 前の週 | 増減 | 計画（週あたり） | 計画比 |")
    w("|---|---|---|---|---|---|")
    for key, name, unit in KPI:
        a, p = cur.get(key, 0.0), prev.get(key, 0.0)
        wk = target.get(key, 0.0) / days * 7 if target else 0.0
        diff = f"{(a - p) / p:+.0%}" if p else ("—" if not a else "新規")
        ratio = f"{a / wk:.0%}" if wk >= (1 if key == "cv" else 5) else "（判定には早い）"
        d = 1 if key == "cv" else 0
        w(f"| {name} | {fmt(a, d)} | {fmt(p, d)} | {diff} | {fmt(wk, 1)} | {ratio} |")
    lt = cur.get("lead_types") or {}
    if lt:
        w("")
        w("お問い合わせの内訳（全チャネル）: " + "、".join(f"{k or '（なし）'} {int(v)}件" for k, v in lt.items()))
    w("")
    w("## 2. 今月の進み具合")
    w("")
    res = cmd_check(plan, today, fetch=fetch, dry_run=True,
                    out=lambda s: lines.append(s) if not s.startswith("## ") else None)
    if res is None:
        w("（月初のため、今月の判定は明日から）")
    w("")
    w("## 3. 先週やったこと・今週やること")
    w("")
    w("- 先週やったこと：`docs/seo/log.md` の該当日を要約して編集長が書く")
    w("- 今週やること：上の「今日の最優先」の打ち手を、月曜の Plan（`marketer`）で施策台帳 `docs/seo/experiments.md` に登録して進める")
    w("")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"weekly-{iso[0]}-W{iso[1]:02d}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out(f"週次レポートを書き出しました: {path.relative_to(ROOT)}")
    out("\n".join(lines))
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["simulate", "check", "weekly"])
    ap.add_argument("--date", help="今日の日付（YYYY-MM-DD、日本時間。省略時は今日）")
    ap.add_argument("--dry-run", action="store_true", help="check で記録ファイルに書かない")
    a = ap.parse_args()
    plan = load_plan()
    today = dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(JST).date()
    if a.cmd == "simulate":
        PLAN_MD.write_text(render_plan(plan), encoding="utf-8")
        print(f"計画を書き出しました: {PLAN_MD.relative_to(ROOT)}")
    elif a.cmd == "check":
        cmd_check(plan, today, dry_run=a.dry_run)
    else:
        cmd_weekly(plan, today)


if __name__ == "__main__":
    main()
