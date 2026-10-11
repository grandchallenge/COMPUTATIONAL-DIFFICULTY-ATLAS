"""Regression for the hourly workflow's cwd/module import contract."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_cda_direct_return_reconcile import issue, fields, valid_comment

ROOT = Path(__file__).resolve().parents[1]


class ReplayEntrypointTests(unittest.TestCase):
    def test_module_invocation_from_repository_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "issue.json").write_text(json.dumps(issue()), encoding="utf-8")
            (path / "fields.json").write_text(json.dumps(fields()), encoding="utf-8")
            (path / "comments.json").write_text(
                json.dumps([valid_comment()]), encoding="utf-8"
            )
            output = path / "result.json"
            run = subprocess.run(
                [sys.executable, "-m", "ci.cda_direct_return_reconcile",
                 "--issue", str(path / "issue.json"),
                 "--issue-fields", str(path / "fields.json"),
                 "--comments", str(path / "comments.json"),
                 "--output", str(output)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            projected = json.loads(output.read_text(encoding="utf-8"))
            self.assertTrue(projected["project"])
            self.assertEqual(projected["comment_id"], 10)
            self.assertFalse(projected["editorial_accepted"])
            self.assertFalse(projected["publication_authorized"])


if __name__ == "__main__":
    unittest.main()
