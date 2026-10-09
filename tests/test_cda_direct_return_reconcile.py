from __future__ import annotations

import unittest

from ci.cda_direct_return_reconcile import reconcile

HEAD = "c75d3aeb6ed1ceb4eb57224f025347729aeb627b"


def issue() -> dict:
    return {
        "number": 2,
        "state": "open",
        "body": (
            "GCL-CDA-EDITORIAL-AGENT/1\n"
            "ASSIGNMENT_ID: CDA-REV-001\n"
            "CAMPAIGN: COMPUTATIONAL-DIFFICULTY-ATLAS\n"
            "ROLE: INDEPENDENT_MATHEMATICAL_EDITORIAL_VERIFY\n"
            "PICKUP_MODE: DIRECT_EDITORIAL_NO_CLAIM\n"
            f"TARGET_HEAD: {HEAD}\n"
        ),
        "labels": [
            {"name": "gcl-job"},
            {"name": "gcl-pickup:direct-editorial"},
            {"name": "gcl-state:available"},
            {"name": "gcl-role:verify"},
            {"name": "gcl-collab:cooperative"},
        ],
    }


def fields() -> list[dict]:
    return [
        {"issue_field_name": "GCL State", "single_select_option": {"name": "AVAILABLE"}},
        {"issue_field_name": "GCL Campaign", "value": "COMPUTATIONAL-DIFFICULTY-ATLAS"},
        {"issue_field_name": "GCL Role", "single_select_option": {"name": "VERIFY"}},
        {"issue_field_name": "GCL Collaboration", "single_select_option": {"name": "COOPERATIVE"}},
    ]


def valid_comment(comment_id: int = 10) -> dict:
    return {
        "id": comment_id,
        "created_at": "2026-10-09T01:00:00Z",
        "body": (
            "RESULT/1\n"
            "assignment_id: CDA-REV-001\n"
            "reviewer_role: INDEPENDENT_MATHEMATICAL_EDITORIAL_VERIFY\n"
            f"input_head: {HEAD}\n"
            "disposition: APPROVE_WITH_CORRECTIONS\n"
        ),
        "user": {"login": "reviewer"},
    }


class DirectReturnReconcileTests(unittest.TestCase):
    def test_replays_valid_missed_result(self):
        out = reconcile(issue(), fields(), [valid_comment()])
        self.assertTrue(out["project"])
        self.assertTrue(out["replayed"])
        self.assertEqual(out["comment_id"], 10)

    def test_skips_invalid_result_then_replays_valid(self):
        bad = valid_comment(5)
        bad["body"] = bad["body"].replace(HEAD, "0" * 40)
        good = valid_comment(10)
        out = reconcile(issue(), fields(), [bad, good])
        self.assertTrue(out["project"])
        self.assertEqual(out["comment_id"], 10)
        self.assertEqual(out["examined_result_comments"], 2)

    def test_non_result_comments_are_ignored(self):
        out = reconcile(
            issue(),
            fields(),
            [{"id": 1, "created_at": "2026-10-09T00:00:00Z", "body": "hello", "user": {"login": "x"}}],
        )
        self.assertFalse(out["project"])
        self.assertEqual(out["reason"], "no_conforming_result")
        self.assertEqual(out["examined_result_comments"], 0)

    def test_closed_issue_is_not_replayed(self):
        i = issue()
        i["state"] = "closed"
        out = reconcile(i, fields(), [valid_comment()])
        self.assertFalse(out["project"])
        self.assertEqual(out["reason"], "not_open_issue")

    def test_invalid_only_result_reports_reason(self):
        bad = valid_comment()
        bad["body"] = bad["body"].replace("CDA-REV-001", "OTHER")
        out = reconcile(issue(), fields(), [bad])
        self.assertFalse(out["project"])
        self.assertEqual(out["reason"], "no_conforming_result")
        self.assertEqual(out["rejected"][0]["reason"], "wrong_assignment")


if __name__ == "__main__":
    unittest.main()
