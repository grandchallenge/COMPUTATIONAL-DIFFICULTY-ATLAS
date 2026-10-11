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
    # GitHub documents dollar-delimited math; Arithmatex handles the same source.
    # Unsupported TeX wrappers can pass a naive balance check but display raw on GitHub.
    if r"\(" in text or r"\)" in text or r"\[" in text or r"\]" in text:
        ERRORS.append(f"{path}: unsupported math wrapper; use $...$ or standalone $")
    display_count = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.strip() == "$":
            display_count += 1
            continue
        if "$" in line:
            ERRORS.append(f"{path}:{line_number}: display $ must occupy its own line")
        if line.replace("$", "").count("$") % 2:
            ERRORS.append(f"{path}:{line_number}: odd number of inline-dollar delimiters")
    if display_count % 2:
        ERRORS.append(f"{path}: odd number of standalone display-math delimiters")
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
