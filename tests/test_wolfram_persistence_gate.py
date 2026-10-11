"""Hostile tests of the Git persistence and SVG-completeness gate."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ci import verify_persisted_wolfram_assets as gate


class PersistenceGateTests(unittest.TestCase):
    def test_rejects_truncated_svg(self):
        with self.assertRaisesRegex(ValueError, "malformed SVG"):
            gate.verify_svg(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0,0"', "broken.svg")

    def test_rejects_rootless_graphics(self):
        with self.assertRaisesRegex(ValueError, "Not an SVG root"):
            gate.verify_svg(b'<div xmlns="http://www.w3.org/2000/svg"><path d="M0 0"/></div>', "fake.svg")

    def test_rejects_raster_embedded(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0"/><image href="data:image/png;base64,AAAA"/></svg>'
        with self.assertRaisesRegex(ValueError, "Raster image embedded"):
            gate.verify_svg(svg, "raster.svg")

    def test_accepts_complete_vector(self):
        gate.verify_svg(
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M0 0L1 1"/></svg>',
            "complete.svg",
        )

    def test_rejects_uncommitted_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "source.wl").write_text("modified", encoding="utf-8")
            with patch.object(gate, "ROOT", root):
                with patch.object(gate, "git", side_effect=["a" * 40, "b" * 40]):
                    with self.assertRaisesRegex(ValueError, "Uncommitted"):
                        gate.assert_persisted("source.wl")

    def test_rejects_nonexistent_git_blob(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "source.wl").write_text("created but not committed", encoding="utf-8")
            with patch.object(gate, "ROOT", root):
                with patch.object(gate, "git", side_effect=ValueError("not in Git HEAD")):
                    with self.assertRaisesRegex(ValueError, "not in Git HEAD"):
                        gate.assert_persisted("source.wl")


if __name__ == "__main__":
    unittest.main()
