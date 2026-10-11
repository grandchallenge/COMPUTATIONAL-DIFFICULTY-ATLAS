#!/usr/bin/env python3
"""Check generated MkDocs HTML and math wrappers; not a browser/MathJax test."""
from pathlib import Path
import sys
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
STAGED = ROOT / "build" / "docs" / "chapters"
HTML = ROOT / "build" / "site" / "chapters"
issues = []
index = ROOT / "build" / "site" / "index.html"
if not index.exists() or "Editorial preview" not in index.read_text(encoding="utf-8"):
    issues.append("Missing preview/disclaimer landing page")
for md in sorted(STAGED.glob("C*.md")):
    dest = HTML / md.stem / "index.html"
    if not dest.exists():
        issues.append(f"Missing rendered page {dest}")
        continue
    html = dest.read_text(encoding="utf-8")
    source = md.read_text(encoding="utf-8")
    if any(ord(c) < 32 and c not in "\r\n\t" for c in source):
        issues.append(f"Unexpected control character in {md}")
    if (r"\(" in source or r"\[" in source) and "arithmatex" not in html:
        issues.append(f"Math not wrapped by Arithmatex in {dest}")
    if r"\solid" in html:
        issues.append(f"Unrecognized solid command in {dest}")
    if "mathjax" not in html.lower():
        issues.append(f"MathJax runtime not referenced in {dest}")
if issues:
    print("\n".join(issues), file=sys.stderr)
    raise SystemExit(1)
print("MkDocs preview pages and Arithmatex wrappers present; visual/browser review still required.")
