#!/usr/bin/env python3
"""Check generated MkDocs HTML and math wrappers; not a browser/MathJax test."""
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

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
# Figure fidelity: ensure the actual Wolfram SVG is shipped with the generated site.
svg = ROOT / "build" / "site" / "figures" / "generated" / "F15_1_grover_query_scaling.svg"
c15 = HTML / "C15" / "index.html"
if not svg.is_file():
    issues.append("C15 Wolfram F15.1 SVG absent from rendered site")
else:
    try:
        root = ET.parse(svg).getroot()
        if not root.tag.endswith("svg"):
            issues.append("F15.1 is not an SVG root")
        if not any(node.tag.endswith("path") for node in root.iter()):
            issues.append("F15.1 lacks vector path geometry")
        if any(node.tag.endswith("image") for node in root.iter()):
            issues.append("F15.1 contains an embedded raster image")
    except ET.ParseError as exc:
        issues.append(f"Invalid F15.1 SVG XML: {exc}")
if c15.is_file():
    rendered = c15.read_text(encoding="utf-8")
    if "F15_1_grover_query_scaling.svg" not in rendered:
        issues.append("C15 does not embed its Wolfram figure")
    if "F15_1_CAPTION" not in rendered:
        issues.append("C15 does not reference the scoped F15.1 caption")

if issues:
    print("\n".join(issues), file=sys.stderr)
    raise SystemExit(1)
print("MkDocs preview pages and Arithmatex wrappers present; visual/browser review still required.")
