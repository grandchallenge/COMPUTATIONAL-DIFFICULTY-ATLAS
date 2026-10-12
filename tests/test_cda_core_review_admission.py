"""Hostile CORE-004 admission preflight tests."""
import unittest
from unittest.mock import patch
from ci import cda_core_review_admission as core
from ci import cda_review_job_admission as base


def staged(job, pr_head=None):
    body="\n".join([
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
    issue={"number":job["issue"],"state":"open","body":body,
           "labels":[{"name":label} for label in sorted(base.BASE_LABELS)]}
    pr={"number":job["pr"],"state":"open","head":{"sha":pr_head or job["head"]}}
    return issue, [], pr, []


class Core004Tests(unittest.TestCase):
    def test_identity_bound(self):
        jobs=core.load_jobs()
        self.assertEqual([j["issue"] for j in jobs],[35,36,37,38])
        self.assertEqual([j["chapter"] for j in jobs],["C06","C07","C08","C09"])
        self.assertEqual(len({j["head"] for j in jobs}),4)

    def test_staged_full_cohort_valid(self):
        for j in core.load_jobs():
            self.assertEqual(base.validate_job(j,*staged(j)),"admit")

    def test_hostile_head_rejected(self):
        for j in core.load_jobs():
            with self.assertRaisesRegex(ValueError,"stale target PR head"):
                base.validate_job(j,*staged(j,pr_head="e"*40))

    def test_mutual_nonwrite_on_read_only(self):
        jobs=core.load_jobs()
        with patch.object(base,"read_job",side_effect=[staged(j) for j in jobs]):
            with patch.object(base,"set_fields") as f, patch.object(base,"add_labels") as l:
                core.run(execute=False)
                f.assert_not_called()
                l.assert_not_called()

    def test_pull_request_cannot_activate(self):
        jobs=core.load_jobs()
        with patch.object(base,"read_job",side_effect=[staged(j) for j in jobs]):
            with patch.dict(core.os.environ,{"GITHUB_REPOSITORY":base.REPO,
                                            "GITHUB_REF":"refs/pull/39/merge"}):
                with self.assertRaisesRegex(ValueError,"not protected main"):
                    core.run(execute=True)


if __name__=="__main__":
    unittest.main()
