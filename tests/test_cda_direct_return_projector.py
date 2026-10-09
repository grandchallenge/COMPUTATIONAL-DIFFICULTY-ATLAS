from __future__ import annotations

import unittest

from ci.cda_direct_return_projector import evaluate

HEAD = "c75d3aeb6ed1ceb4eb57224f025347729aeb627b"


def event(
    *,
    body: str | None = None,
    issue_body: str | None = None,
    labels: list[str] | None = None,
    actor: str = "reviewer",
) -> dict:
    if body is None:
        body = (
            "RESULT/1\n"
            "assignment_id: CDA-REV-001\n"
            "reviewer_role: INDEPENDENT_MATHEMATICAL_EDITORIAL_VERIFY\n"
            f"input_head: {HEAD}\n"
            "disposition: APPROVE_WITH_CORRECTIONS\n"
        )
    if issue_body is None:
        issue_body = (
            "GCL-CDA-EDITORIAL-AGENT/1\n"
            "ASSIGNMENT_ID: CDA-REV-001\n"
            "CAMPAIGN: COMPUTATIONAL-DIFFICULTY-ATLAS\n"
            f"TARGET_HEAD: {HEAD}\n"
        )
    if labels is None:
        labels = ["gcl-job", "gcl-pickup:direct-editorial", "gcl-state:available"]
    return {
        "action": "created",
        "repository": {"full_name": "grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS"},
        "issue": {
            "number": 2,
            "state": "open",
            "body": issue_body,
            "labels": [{"name": x} for x in labels],
        },
        "comment": {
            "id": 99,
            "body": body,
            "user": {"login": actor},
        },
    }


def fields(state: str = "AVAILABLE", campaign: str = "COMPUTATIONAL-DIFFICULTY-ATLAS") -> list[dict]:
    return [
        {
            "issue_field_name": "GCL State",
            "single_select_option": {"name": state},
        },
        {
            "issue_field_name": "GCL Campaign",
            "value": campaign,
        },
    ]


class DirectReturnProjectorTests(unittest.TestCase):
    def test_valid_exact_head_result_projects_returned(self):
        out = evaluate(event(), fields())
        self.assertTrue(out["project"])
        self.assertEqual(out["state_to_write"], "RETURNED")
        self.assertFalse(out["review_adjudicated"])
        self.assertFalse(out["editorial_accepted"])

    def test_wrong_head_is_rejected(self):
        bad = "0" * 40
        body = (
            "RESULT/1\n"
            "assignment_id: CDA-REV-001\n"
            "reviewer_role: INDEPENDENT_MATHEMATICAL_EDITORIAL_VERIFY\n"
            f"input_head: {bad}\n"
            "disposition: APPROVE\n"
        )
        self.assertEqual(evaluate(event(body=body), fields())["reason"], "wrong_input_head")

    def test_wrong_assignment_is_rejected(self):
        body = (
            "RESULT/1\n"
            "assignment_id: OTHER\n"
            "reviewer_role: VERIFY\n"
            f"input_head: {HEAD}\n"
            "disposition: APPROVE\n"
        )
        self.assertEqual(evaluate(event(body=body), fields())["reason"], "wrong_assignment")

    def test_non_direct_issue_is_ignored(self):
        out = evaluate(event(labels=["gcl-job", "gcl-state:available"]), fields())
        self.assertEqual(out["reason"], "not_direct_editorial")

    def test_wrong_campaign_is_ignored(self):
        self.assertEqual(
            evaluate(event(), fields(campaign="OTHER"))["reason"],
            "wrong_campaign",
        )

    def test_non_available_state_is_ignored(self):
        self.assertEqual(
            evaluate(event(), fields(state="BLOCKED"))["reason"],
            "state_not_available",
        )

    def test_already_returned_is_idempotent(self):
        self.assertEqual(
            evaluate(event(), fields(state="RETURNED"))["reason"],
            "already_returned",
        )

    def test_bad_disposition_is_rejected(self):
        body = (
            "RESULT/1\n"
            "assignment_id: CDA-REV-001\n"
            "reviewer_role: VERIFY\n"
            f"input_head: {HEAD}\n"
            "disposition: CERTIFIED\n"
        )
        self.assertEqual(
            evaluate(event(body=body), fields())["reason"],
            "invalid_disposition",
        )


if __name__ == "__main__":
    unittest.main()
