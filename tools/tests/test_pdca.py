#!/usr/bin/env python3
"""tools/pdca.py と tools/analytics.py の拡張部分のテスト（標準ライブラリのみ。ダミーデータで動く）。

使い方: python3 tools/tests/test_pdca.py   （python3 -m unittest discover -s tools/tests -p "test_pdca.py" でも可）
実データ（GA4・Search Console）にはアクセスしない。
"""
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import analytics as A  # noqa: E402
import pdca as P  # noqa: E402

D = dt.date


def m(**kw):
    """fetch_page_metrics の返り値を模したもの（指定しない指標は 0）"""
    out = {k: 0.0 for k in A.METRIC_KEYS}
    out.update({k: float(v) for k, v in kw.items()})
    return out


LEDGER_HEAD = "# 台帳\n\n説明\n\n```\n### E-20000101-01 見本（読まれない）\n- 状態: 測定中\n```\n\n## 施策一覧\n\n"


def exp_block(eid="E-20260901-01", state="測定中", page="/media/a.html", metric="CTR", target="2.0%",
              implemented="2026-09-01", measure="", ext="0", sub="クリック、掲載順位"):
    return (f"### {eid} テスト施策\n- 状態: {state}\n- 対象ページ: {page}\n- 仮説: 〜すれば〜になる。なぜなら〜\n"
            f"- 施策の種類: title・description\n- 変更内容: title を変更\n- 主指標: {metric}\n- 目標値: {target}\n"
            f"- 副指標: {sub}\n- ベースライン:\n- 実施日: {implemented}\n- 測定日: {measure}\n- 延長回数: {ext}\n"
            f"- 結果:\n- 全体の変化:\n- 判定:\n- 判定の理由:\n- 次の一手: 様子を見る\n- 関連PR: https://example.com/pr/1\n")


def ledger(*blocks):
    return LEDGER_HEAD + P.START + "\n\n" + "\n\n".join(blocks) + "\n" + P.END + "\n\n末尾のメモ\n"


class FakeFetch:
    """期間の前後とページ／サイト全体で返す値を切り替えるダミー。呼ばれた期間を記録する。"""

    def __init__(self, before, after, site_before=None, site_after=None):
        self.v = {"b": before, "a": after, "sb": site_before or m(), "sa": site_after or m()}
        self.calls = []
        self.split = None

    def __call__(self, page, start, end):
        self.calls.append((page, start, end))
        if self.split is None:
            self.split = end  # 最初の呼び出しは前期間
        when = "b" if end <= self.split else "a"
        return self.v[("s" if page is None else "") + when]


class TestJudge(unittest.TestCase):
    def test_effective(self):
        j = P.judge("CTR", m(ctr=0.012, impressions=500), m(ctr=0.021, impressions=600), "1.2%→2.0%",
                    m(ctr=0.010), m(ctr=0.0105))
        self.assertEqual(j["verdict"], "効果あり")
        self.assertAlmostEqual(j["target"], 0.02)

    def test_target_reached_but_site_grew_more(self):
        j = P.judge("CTR", m(ctr=0.012, impressions=500), m(ctr=0.021, impressions=600), "2.0%",
                    m(ctr=0.010), m(ctr=0.020))
        self.assertEqual(j["verdict"], "一部効果")

    def test_partial(self):
        j = P.judge("クリック", m(clicks=10, impressions=300), m(clicks=14, impressions=300), "20")
        self.assertEqual(j["verdict"], "一部効果")

    def test_no_effect_within_band(self):
        j = P.judge("CTR", m(ctr=0.0120, impressions=500), m(ctr=0.0125, impressions=500), "2.0%")
        self.assertEqual(j["verdict"], "効果なし")

    def test_improved_but_same_as_site(self):
        j = P.judge("セッション", m(sessions=100), m(sessions=130), "200", m(sessions=1000), m(sessions=1400))
        self.assertEqual(j["verdict"], "効果なし")

    def test_worse(self):
        j = P.judge("CTR", m(ctr=0.020, impressions=500), m(ctr=0.012, impressions=500), "2.5%",
                    m(ctr=0.010), m(ctr=0.010))
        self.assertEqual(j["verdict"], "悪化")

    def test_drop_same_as_site_is_not_worse(self):
        j = P.judge("セッション", m(sessions=100), m(sessions=70), "", m(sessions=1000), m(sessions=650))
        self.assertEqual(j["verdict"], "効果なし")

    def test_position_lower_is_better(self):
        j = P.judge("掲載順位", m(position=12.0, impressions=400), m(position=7.5, impressions=400), "8位")
        self.assertEqual(j["verdict"], "効果あり")
        j = P.judge("掲載順位", m(position=7.0, impressions=400), m(position=12.0, impressions=400), "5位")
        self.assertEqual(j["verdict"], "悪化")

    def test_hold_when_impressions_short(self):
        j = P.judge("CTR", m(ctr=0.01, impressions=99), m(ctr=0.05, impressions=500), "2.0%")
        self.assertEqual(j["verdict"], "保留")
        self.assertIn("データ不足", j["reason"])

    def test_hold_when_sessions_short(self):
        j = P.judge("相談率", m(lead_rate=0.1, landing_sessions=40), m(lead_rate=0.2, landing_sessions=29), "+50%")
        self.assertEqual(j["verdict"], "保留")

    def test_undecidable_after_max_extensions(self):
        j = P.judge("CTR", m(impressions=10), m(impressions=10), "2%", extensions=P.MAX_EXTENSIONS)
        self.assertEqual(j["verdict"], "判定不能")

    def test_relative_target(self):
        self.assertAlmostEqual(P.parse_target("+20%", "count", 50), 60)
        self.assertAlmostEqual(P.parse_target("-10%", "rank", 10), 9)
        self.assertAlmostEqual(P.parse_target("90秒", "sec"), 90)
        self.assertIsNone(P.parse_target("", "pct"))

    def test_zero_before(self):
        j = P.judge("相談ボタンのクリック", m(cta_clicks=0, sessions=50), m(cta_clicks=5, sessions=50), "3")
        self.assertEqual(j["verdict"], "効果あり")

    def test_unknown_metric(self):
        with self.assertRaises(ValueError):
            P.metric_info("売上")


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.path = self.dir / "experiments.md"

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_roundtrip_keeps_outside_text(self):
        text = ledger(exp_block(), exp_block("E-20260901-02", state="計画"))
        head, exps, tail = P.parse_ledger(text)
        self.assertEqual([e["id"] for e in exps], ["E-20260901-01", "E-20260901-02"])  # 見本は読まない
        self.assertEqual(exps[0]["主指標"], "CTR")
        self.assertEqual(exps[0]["関連PR"], "https://example.com/pr/1")
        again = P.render_ledger(head, exps, tail)
        self.assertIn("末尾のメモ", again)
        self.assertIn("見本（読まれない）", again)
        self.assertEqual(P.parse_ledger(again)[1], exps)
        self.assertEqual(P.render_ledger(*P.parse_ledger(again)), again)  # 2回目以降は不変

    def test_real_ledger_template_parses(self):
        head, exps, tail = P.load(ROOT / "docs/seo/experiments.md")
        self.assertTrue(all(not e["id"].startswith("E-2000") for e in exps))  # 記入例（ダミー）は読まない

    def test_new_assigns_next_id(self):
        self.path.write_text(ledger(exp_block("E-20261011-01", state="計画")), encoding="utf-8")
        e = P.cmd_new(self.path, D(2026, 10, 11), "/media/b.html", "内部リンク", "サービス移動率", "+30%", out=lambda *_: None)
        self.assertEqual(e["id"], "E-20261011-02")
        _, exps, _ = P.load(self.path)
        self.assertEqual(exps[-1]["状態"], "計画")

    def test_check_effective_writes_result(self):
        self.path.write_text(ledger(exp_block()), encoding="utf-8")
        f = FakeFetch(m(ctr=0.012, impressions=500, clicks=6, position=9.0),
                      m(ctr=0.022, impressions=600, clicks=13, position=8.0),
                      m(ctr=0.010, impressions=5000), m(ctr=0.010, impressions=5000))
        P.cmd_check(self.path, D(2026, 10, 2), fetch=f, out=lambda *_: None)
        e = P.load(self.path)[1][0]
        self.assertEqual(e["判定"], "効果あり")
        self.assertEqual(e["状態"], "判定済み")
        self.assertEqual(e["測定日"], "2026-09-29")
        self.assertIn("副指標: クリック 6→13", e["結果"])
        self.assertIn("サイト全体", e["全体の変化"])
        self.assertEqual(e["次の一手"], "様子を見る")  # 人が書いた項目は残る
        # 比較期間: 前 28 日（08-04〜08-31）と後 28 日（09-02〜09-29）。実施日 09-01 は含まない
        pages = [c for c in f.calls if c[0] == "/media/a.html"]
        self.assertEqual(pages[0][1:], (D(2026, 8, 4), D(2026, 8, 31)))
        self.assertEqual(pages[1][1:], (D(2026, 9, 2), D(2026, 9, 29)))

    def test_check_not_due_yet(self):
        self.path.write_text(ledger(exp_block(state="実施済み")), encoding="utf-8")
        called = []
        P.cmd_check(self.path, D(2026, 10, 1), fetch=lambda *a: called.append(a), out=lambda *_: None)
        e = P.load(self.path)[1][0]
        self.assertEqual(called, [])  # 測定日 09-29 ＋ 3 日 ＝ 10-02 まで測らない
        self.assertEqual(e["状態"], "測定中")
        self.assertEqual(e["測定日"], "2026-09-29")
        self.assertEqual(e["判定"], "")

    def test_check_hold_extends_then_undecidable(self):
        self.path.write_text(ledger(exp_block()), encoding="utf-8")
        short = m(ctr=0.01, impressions=19)
        P.cmd_check(self.path, D(2026, 10, 2), fetch=FakeFetch(short, short), out=lambda *_: None)
        e = P.load(self.path)[1][0]
        self.assertEqual((e["判定"], e["状態"], e["測定日"], e["延長回数"]), ("保留", "測定中", "2026-10-27", "1"))
        # 延長後は前後 56 日で比べる
        f = FakeFetch(short, short)
        P.cmd_check(self.path, D(2026, 10, 30), fetch=f, out=lambda *_: None)
        self.assertEqual(f.calls[0][1:], (D(2026, 7, 7), D(2026, 8, 31)))
        self.assertEqual(f.calls[1][1:], (D(2026, 9, 2), D(2026, 10, 27)))
        e = P.load(self.path)[1][0]
        self.assertEqual((e["延長回数"], e["測定日"]), ("2", "2026-11-24"))
        P.cmd_check(self.path, D(2026, 11, 27), fetch=FakeFetch(short, short), out=lambda *_: None)
        P.cmd_check(self.path, D(2026, 12, 25), fetch=FakeFetch(short, short), out=lambda *_: None)
        e = P.load(self.path)[1][0]
        self.assertEqual((e["判定"], e["状態"], e["延長回数"]), ("判定不能", "判定済み", "3"))

    def test_check_worse_and_no_effect(self):
        self.path.write_text(ledger(exp_block(), exp_block("E-20260901-02", metric="セッション", target="+50%")),
                             encoding="utf-8")

        def fetch(page, start, end):
            before = end < D(2026, 9, 1)
            if page is None:
                return m(ctr=0.01, impressions=9000, sessions=1000)
            return m(ctr=0.02 if before else 0.01, impressions=500, sessions=100 if before else 105)
        P.cmd_check(self.path, D(2026, 10, 5), fetch=fetch, out=lambda *_: None)
        e1, e2 = P.load(self.path)[1]
        self.assertEqual(e1["判定"], "悪化")
        self.assertEqual(e2["判定"], "効果なし")

    def test_check_dry_run_does_not_write(self):
        text = ledger(exp_block())
        self.path.write_text(text, encoding="utf-8")
        f = FakeFetch(m(ctr=0.01, impressions=500), m(ctr=0.03, impressions=500))
        P.cmd_check(self.path, D(2026, 10, 2), fetch=f, dry_run=True, out=lambda *_: None)
        self.assertEqual(self.path.read_text(encoding="utf-8"), text)

    def test_baseline(self):
        self.path.write_text(ledger(exp_block(state="計画", implemented="")), encoding="utf-8")
        calls = []

        def fetch(page, start, end):
            calls.append((page, start, end))
            return m(ctr=0.0123, impressions=350, clicks=4, position=11.2)
        P.cmd_baseline(self.path, "E-20260901-01", D(2026, 10, 11), fetch=fetch, out=lambda *_: None)
        e = P.load(self.path)[1][0]
        self.assertEqual(calls, [("/media/a.html", D(2026, 9, 11), D(2026, 10, 8))])
        self.assertIn("CTR 1.23%（表示回数 350）", e["ベースライン"])
        self.assertIn("掲載順位 11.2位", e["ベースライン"])
        self.assertEqual(e["状態"], "計画")

    def test_report(self):
        done = [exp_block(f"E-20260801-0{i}", state="判定済み") for i in (1, 2, 3)]
        text = ledger(*done, exp_block("E-20260901-04"), exp_block("E-20261001-05", state="計画"))
        head, exps, tail = P.parse_ledger(text)
        exps[0]["判定"], exps[1]["判定"], exps[2]["判定"] = "効果あり", "効果なし", "判定不能"
        md = P.build_report(exps, D(2026, 10, 11))
        self.assertIn("| 1 | 0 | 1 | 3 | 5 |", md)
        self.assertIn("| title・description | 2 | 1 | 0 | 50% |", md)
        self.assertIn("ベースライン未取得", md)
        self.assertIn("に施策はまだありません", P.build_report([], D(2026, 10, 11)))

    def test_cli_without_env(self):
        self.path.write_text(ledger(exp_block()), encoding="utf-8")
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as cm:
                P.main(["--ledger", str(self.path), "--today", "2026-10-11", "check"])
            self.assertIn("GOOGLE_SERVICE_ACCOUNT_JSON", str(cm.exception.code))
            with mock.patch("builtins.print"):
                P.main(["--ledger", str(self.path), "report"])  # report は環境変数なしで動く


# ---- analytics.py の拡張（API のレスポンスを模したダミー） ----------------------
class Resp:
    def __init__(self, data, status=200):
        self.status_code, self._d, self.text = status, data, json.dumps(data)

    def json(self):
        return self._d


def ga4_resp(dims, metrics, rows):
    return {"dimensionHeaders": [{"name": d} for d in dims], "metricHeaders": [{"name": n} for n in metrics],
            "rows": [{"dimensionValues": [{"value": v} for v in r[:len(dims)]],
                      "metricValues": [{"value": str(v)} for v in r[len(dims):]]} for r in rows]}


class FakeSession:
    """リクエストの中身を見てダミーのレスポンスを返す。"""

    def __init__(self, handler):
        self.handler, self.bodies = handler, []

    def post(self, url, json=None):
        self.bodies.append((url, json))
        return self.handler(url, json)


def flt_text(body):
    return json.dumps(body.get("dimensionFilter", {}), ensure_ascii=False)


class TestAnalytics(unittest.TestCase):
    def test_ai_source(self):
        for s in ("chatgpt.com", "https://chat.openai.com/", "perplexity.ai", "www.perplexity.ai",
                  "gemini.google.com", "copilot.microsoft.com", "https://www.bing.com/chat?q=x", "claude.ai",
                  "you.com", "phind.com"):
            self.assertTrue(A.is_ai_source(s), s)
        for s in ("google", "bing.com", "(direct)", "yahoo.co.jp", "about-you.company.jp", ""):
            self.assertFalse(A.is_ai_source(s), s)

    def test_article_path(self):
        self.assertTrue(A.is_article_path("/media/akiya-minpaku.html"))
        for p in ("/media/guide-sell.html", "/media/category-akiya.html", "/media/search.html", "/media.html",
                  "/service-minpaku.html"):
            self.assertFalse(A.is_article_path(p), p)

    def test_fetch_page_metrics(self):
        def handler(url, body):
            if "searchconsole" in url:
                f = body["dimensionFilterGroups"][0]["filters"][0]
                self.assertEqual(f, {"dimension": "page", "operator": "equals",
                                     "expression": "https://rivia-co.com/media/a.html"})
                return Resp({"rows": [{"clicks": 3, "impressions": 150, "ctr": 0.02, "position": 8.5}]})
            names = [x["name"] for x in body["metrics"]]
            ft = flt_text(body)
            if "screenPageViews" in names:
                vals = [40, 35, 0.6, 1200, 30, 0]
            elif "generate_lead" in ft:
                vals = [2, 3]
            elif "cta_click" in ft:
                vals = [7]
            elif "service-" in ft:
                vals = [5]
            elif "chatgpt" in ft:
                vals = [4]
            else:  # landingPage のみ
                vals = [25]
            self.assertIn("/media/a.html", ft)
            return Resp(ga4_resp([], names, [vals]))
        s = FakeSession(handler)
        r = A.fetch_page_metrics("/media/a.html", "2026-09-01", "2026-09-28", s=s, prop="1", site="https://rivia-co.com/")
        self.assertEqual((r["impressions"], r["clicks"], r["ctr"], r["position"]), (150, 3, 0.02, 8.5))
        self.assertEqual((r["views"], r["sessions"], r["avg_engagement_time"]), (40, 35, 40.0))
        self.assertEqual((r["landing_sessions"], r["leads"], r["lead_events"], r["cta_clicks"]), (25, 2, 3, 7))
        self.assertEqual((r["service_sessions"], r["ai_sessions"]), (5, 4))
        self.assertAlmostEqual(r["lead_rate"], 0.08)
        self.assertAlmostEqual(r["service_rate"], 0.2)
        self.assertEqual(set(r), set(A.METRIC_KEYS))

    def test_fetch_site_total_and_empty(self):
        def handler(url, body):
            if "searchconsole" in url:
                self.assertNotIn("dimensionFilterGroups", body)
                return Resp({})  # データ0件
            return Resp({"metricHeaders": [{"name": x["name"]} for x in body["metrics"]]})  # 行なし
        r = A.fetch_page_metrics(None, "2026-09-01", "2026-09-28", s=FakeSession(handler), prop="1", site="x")
        self.assertTrue(all(v == 0 for v in r.values()))

    def test_prefix_filter(self):
        self.assertEqual(A.page_filter("pagePath", "/media/")["filter"]["stringFilter"]["matchType"], "BEGINS_WITH")
        self.assertEqual(A._gsc_page_filter("/media/")["operator"], "includingRegex")

    def test_report_sections_and_unregistered(self):
        def handler(url, body):
            if "searchconsole" in url:
                return Resp({"rows": [{"keys": ["2026-09-01"], "clicks": 0, "impressions": 2, "ctr": 0, "position": 30}]})
            dims = [x["name"] for x in body.get("dimensions", [])]
            names = [x["name"] for x in body["metrics"]]
            ft = flt_text(body)
            if any(d.startswith("customEvent:") for d in dims):
                return Resp({"error": "not a valid dimension"}, 400)  # カスタムディメンション未登録
            if dims == ["pagePath"]:
                return Resp(ga4_resp(dims, names, [["/media/a.html", 10, 8, 0.5, 300, 6, 0], ["/thanks.html", 1, 1, 1, 5, 1, 1]]))
            if dims == ["pagePath", "eventName"]:
                return Resp(ga4_resp(dims, names, [["/media/a.html", "cta_click", 3], ["/thanks.html", "generate_lead", 1]]))
            if dims == ["landingPage"] and "generate_lead" in ft:
                return Resp(ga4_resp(dims, names, [["/media/a.html", 1, 1]]))
            if dims == ["landingPage"] and "service-" in ft:
                return Resp(ga4_resp(dims, names, [["/media/a.html", 2]]))
            if dims == ["landingPage"] and "FULL_REGEXP" in ft:
                return Resp(ga4_resp(dims, names, [["/media/a.html", 6], ["/media/guide-sell.html", 3]]))
            if dims == ["landingPage"]:
                return Resp(ga4_resp(dims, names, [["/media/a.html", 6, 0.5, 1], ["/", 4, 0.5, 0]]))
            if dims == ["sessionSource", "landingPage"]:
                return Resp(ga4_resp(dims, names, [["chatgpt.com", "/media/a.html", 2, 1, 0]]))
            return Resp(ga4_resp(dims, names, []))
        data = {"generated": "2026-10-11", "period": {"start": "2026-09-10", "end": "2026-10-08"},
                "prev_period": {"start": "2026-08-13", "end": "2026-09-09"}, "errors": [],
                "gsc": {"pages": [], "pages_prev": [], "queries": [], "page_queries": []},
                "ga4": {"pages": [], "channels": []}}
        A.collect_extra(FakeSession(handler), data, "https://rivia-co.com/", "1", "2026-09-10", "2026-10-08")
        self.assertEqual(data["errors"], [])
        self.assertEqual(data["ga4"]["form_type"], A.UNREGISTERED)
        self.assertEqual(len(data["gsc"]["daily"]), 1)
        self.assertEqual(data["ga4"]["article_to_service"],
                         [{"page": "/media/a.html", "sessions": 6, "serviceSessions": 2}])  # ガイドは除く
        md = A.build_report(data)
        for h in ("## 相談につながったページ", "## AI検索からの流入", "## 記事からサービスへの移動",
                  "form_type の内訳: 未登録", "cta_position の内訳: 未登録", "`/media/a.html` クリック 3",
                  "| `/media/a.html` | 6 | 1 | 16.7% |", "- chatgpt.com: 2", "| `/media/a.html` | 6 | 2 | 33.3% |"):
            self.assertIn(h, md)
        self.assertIn("## サイト内の行動（GA4）", md)  # 既存の節は残る

    def test_existing_report_unchanged_without_extra(self):
        data = {"generated": "2026-10-11", "period": {"start": "a", "end": "b"},
                "prev_period": {"start": "c", "end": "d"}, "errors": [],
                "ga4": {"pages": [{"page": "/", "screenPageViews": 19, "engagementRate": 0.5, "keyEvents": 0}],
                        "channels": [{"channel": "Direct", "sessions": 5, "keyEvents": 0}]}}
        md = A.build_report(data)
        self.assertNotIn("相談につながった", md)
        self.assertIn("| `/` | 19 | 50% | 0 |", md)


if __name__ == "__main__":
    unittest.main(verbosity=1)
