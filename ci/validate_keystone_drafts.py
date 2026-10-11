#!/usr/bin/env python3
"""Fail-closed structural check for candidate chapters; not a render or peer review."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("C01", "C04", "C05", "C10", "C15", "C20")
ERRORS = []
for name in REQUIRED:
    path = ROOT / "chapters" / f"{name}.md"
    # C01 is on separate PR; assess it only when the two PRs have been integrated.
    if not path.exists():
        if name == "C01":
            print("NOTE: C01 is in independent PR #6; integration pending")
            continue
        ERRORS.append(f"{path}: missing")
        continue
    text = path.read_text(encoding="utf-8")
    for opening, closing in ((r"\(", r"\)"), (r"\[", r"\]")):
        if text.count(opening) != text.count(closing):
            ERRORS.append(f"{path}: mismatched {opening}/{closing} delimiters")
    required = ("## Question", "## Exercises", "## Map update")
    for section in required:
        if section not in text:
            ERRORS.append(f"{path}: missing {section}")
    if len(text) < 1500:
        ERRORS.append(f"{path}: below draft-length sanity threshold")
if ERRORS:
    print("\n".join(ERRORS), file=sys.stderr)
    raise SystemExit(1)
print("Structural checks passed (NOT typeset/rendered or independently reviewed).")
