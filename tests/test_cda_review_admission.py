"""Pure admission-plan adversarial tests; never write GitHub state."""
import copy
import unittest

from ci import cda_review_job_admission as m


def issue(job, labels=None, state="STAGED_PENDING_AUTHORIZED_QUEUE_ADMISSION"):
    label_names = m.BASE_LABELS if labels is None else labels
    return {
        "number": job["issue"],
        "state": "open",
        "labels": [{"name": label} for label in label_names],
        "body": "\n".join([
            "GCL-CDA-EDITORIAL-AGENT/1",
            f"STATE: {state}",
            f"ASSIGNMENT_ID: {job['assignment_id']}",
            f"CAMPAIGN: {m.CAMPAIGN}",
            f"ROLE: {m.ROLE}",
            f"PICKUP_MODE: {m.PICKUP}",
            f"TARGET_PR: #{job['pr']}",
            f"TARGET_HEAD: {job['head']}",
            f"TARGET_CHAPTER: {job['chapter']}",
            "PROTECTED_OR_RELEASE_MUTATION_AUTHORIZED: NO",
        ])
    }


def field_rows():
    return [
        {"issue_field_name": name, "single_select_option": {"name": value}}
        for name, value in m.FIELD_VALUES.items()
    ]


class AdmissionInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.job = m.load_registry()[0]

    def pr(self):
        return {"number": self.job["pr"], "state": "open", "head": {"sha": self.job["head"]}}

    def test_immutable_registry(self):
        jobs = m.load_registry()
        self.assertEqual(len(jobs), 6)
        self.assertEqual({j["issue"] for j in jobs}, {9, 10, 11, 12, 13, 14})

    def test_staged_admits_only_when_fields_empty(self):
        self.assertEqual(m.validate_job(self.job, issue(self.job), [], self.pr()), "admit")

    def test_matching_partial_fields_resume_without_false_availability(self):
        self.assertEqual(
            m.validate_job(self.job, issue(self.job), field_rows()[:1], self.pr()),
            "finish_fields",
        )

    def test_hostile_partial_field_value_fails_closed(self):
        hostile = field_rows()[:1]
        hostile[0]["single_select_option"]["name"] = "RETURNED"
        with self.assertRaises(ValueError):
            m.validate_job(self.job, issue(self.job), hostile, self.pr())

    def test_restart_after_field_write(self):
        self.assertEqual(
            m.validate_job(self.job, issue(self.job), field_rows(), self.pr()),
            "finish_labels",
        )

    def test_restart_after_one_label(self):
        partial = m.BASE_LABELS | {"gcl-pickup:direct-editorial"}
        self.assertEqual(
            m.validate_job(self.job, issue(self.job, labels=partial), field_rows(), self.pr()),
            "finish_labels",
        )

    def test_finish_body_after_readback(self):
        self.assertEqual(
            m.validate_job(self.job, issue(self.job, labels=m.AVAILABLE_LABELS),
                           field_rows(), self.pr()),
            "finish_body",
        )

    def test_already_available_is_idempotent(self):
        self.assertEqual(
            m.validate_job(self.job, issue(self.job, labels=m.AVAILABLE_LABELS,
                                            state="AVAILABLE"), field_rows(), self.pr()),
            "already_available",
        )

    def test_stale_target_head_blocks(self):
        stale = self.pr()
        stale["head"]["sha"] = "a" * 40
        with self.assertRaises(ValueError):
            m.validate_job(self.job, issue(self.job), [], stale)

    def test_missing_role_label_blocks(self):
        wrong = {"gcl-job", "gcl-collab:cooperative"}
        with self.assertRaises(ValueError):
            m.validate_job(self.job, issue(self.job, labels=wrong), [], self.pr())

    def test_fake_available_label_without_fields_blocks(self):
        with self.assertRaises(ValueError):
            m.validate_job(self.job, issue(self.job, labels=m.AVAILABLE_LABELS),
                           [], self.pr())

    def test_duplicate_binding_blocks(self):
        bad = issue(self.job)
        bad["body"] += "\nTARGET_HEAD: " + self.job["head"]
        with self.assertRaises(ValueError):
            m.validate_job(self.job, bad, [], self.pr())

    def test_wrong_campaign_blocks(self):
        bad = issue(self.job)
        bad["body"] = bad["body"].replace(m.CAMPAIGN, "OTHER-CAMPAIGN")
        with self.assertRaises(ValueError):
            m.validate_job(self.job, bad, [], self.pr())


if __name__ == "__main__":
    unittest.main()
