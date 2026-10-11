"""tools/plan.py のテスト（API を使わない）: python3 -m unittest tools/tests/test_plan.py"""
import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import plan as P  # noqa: E402


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.plan = P.load_plan()

    def test_simulate_grows_and_scenarios_ordered(self):
        rows = {k: P.simulate(self.plan, k) for k in self.plan["scenarios"]}
        std = rows["standard"]
        self.assertEqual(len(std), self.plan["months"])
        self.assertTrue(all(b["cv"] >= a["cv"] for a, b in zip(std, std[1:])))
        self.assertLess(rows["conservative"][-1]["cv_cum"], std[-1]["cv_cum"])
        self.assertLess(std[-1]["cv_cum"], rows["stretch"][-1]["cv_cum"])
        r = std[-1]
        self.assertAlmostEqual(r["cv_document"] + r["cv_consult"], r["cv"])

    def test_check_finds_upstream_bottleneck(self):
        def fake(start, end, gsc_end):
            return {"impressions": 0, "clicks": 0, "ai_sessions": 0, "seo_sessions": 500,
                    "cv": 0, "lead_types": {}}
        out = []
        res = P.cmd_check(self.plan, dt.date(2027, 3, 30), fetch=fake, dry_run=True, out=out.append)
        self.assertEqual(res["bottleneck"]["key"], "impressions")
        self.assertIn("今日の最優先", "\n".join(out))

    def test_check_on_track(self):
        target = P.plan_for_date(self.plan, dt.date(2027, 3, 20))
        def fake(start, end, gsc_end):
            return {k: target[k] for k in ("impressions", "clicks", "ai_sessions", "seo_sessions", "cv")} | {"lead_types": {}}
        res = P.cmd_check(self.plan, target["end"], fetch=fake, dry_run=True, out=lambda s: None)
        self.assertIsNone(res["bottleneck"])

    def test_first_day_has_no_data(self):
        res = P.cmd_check(self.plan, dt.date(2026, 10, 11), fetch=None, dry_run=True, out=lambda s: None)
        self.assertIsNone(res)


if __name__ == "__main__":
    unittest.main()
