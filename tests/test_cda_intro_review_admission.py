"""Intro-003 admission invariants: no stale PR, no preprotected writes."""
import unittest
from unittest.mock import patch
from ci import cda_intro_review_admission as intro
from ci import cda_review_job_admission as base


def stage(job, pr_head=None):
    body = "\n".join([
        "GCL-CDA-EDITORIAL-AGENT/1",
        "STATE: STAGED_PENDING_AUTHORIZED_QUEUE_ADMISSION",
        f"ASSIGNMENT_ID: {job['assignment_id']}",
        f"CAMPAIGN: {base.CAMPAIGN}",
        f"ROLE: {base.ROLE}",
        f"PICKUP_MODE: {base.PICKUP}",
        f"TARGET_PR: #{job['pr']}",
        f"TARGET_HEAD: {job['head']}",
        f"TARGET_CHAPTER: {job['chapter']}",
        "PROTECTED_OR_RELEASE_MUTATION_AUTHORIZED: NO",
    ])+"\n"
    issue = {"number":job["issue"],"state":"open","body":body,
             "labels":[{"name":name} for name in sorted(base.BASE_LABELS)]}
    pr = {"number":job["pr"], "state":"open",
          "head":{"sha":pr_head or job["head"]}}
    return issue, [], pr, []


class Intro003Tests(unittest.TestCase):
    def test_registry_binds_exact_two_jobs(self):
        jobs = intro.load_jobs()
        self.assertEqual([j["issue"] for j in jobs],[26,27])
        self.assertEqual([j["chapter"] for j in jobs],["C02","C03"])
        self.assertEqual(len({j["head"] for j in jobs}),1)

    def test_staged_packets_pass_read_only_validation(self):
        for job in intro.load_jobs():
            self.assertEqual(base.validate_job(job,*stage(job)),"admit")

    def test_fail_closed_on_stale_head(self):
        for job in intro.load_jobs():
            with self.assertRaisesRegex(ValueError,"stale target PR head"):
                base.validate_job(job,*stage(job,pr_head="a"*40))

    def test_live_preflight_writes_nothing(self):
        jobs = intro.load_jobs()
        with patch.object(base,"read_job",side_effect=[stage(j) for j in jobs]):
            with patch.object(base,"set_fields") as fields:
                with patch.object(base,"add_labels") as labels:
                    intro.run(execute=False)
                    fields.assert_not_called()
                    labels.assert_not_called()

    def test_protected_ref_guard(self):
        jobs = intro.load_jobs()
        with patch.object(base,"read_job",side_effect=[stage(j) for j in jobs]):
            with patch.dict(intro.os.environ,{"GITHUB_REPOSITORY":base.REPO,
                                              "GITHUB_REF":"refs/pull/26/merge"}):
                with self.assertRaisesRegex(ValueError,"outside protected main"):
                    intro.run(execute=True)


if __name__ == "__main__":
    unittest.main()
