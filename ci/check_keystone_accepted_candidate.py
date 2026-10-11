#!/usr/bin/env python3
"""Mechanical chapter and rendered HTML acceptance preflight; not peer review."""
from pathlib import Path
from xml.etree import ElementTree as ET
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ("C01", "C04", "C05", "C10", "C15", "C20")
FIGURES = {
    "C01": "F3_1_tsp_formulation_fork",
    "C04": "F3_2_np_verifier",
    "C05": "F2_1_translator_solver",
    "C10": "F4_3_savitch_midpoint",
    "C15": "F15_1_grover_query_scaling",
    "C20": "F6_2_halting_diagonal",
}
errors = []
for chapter in CHAPTERS:
    path = ROOT / "chapters" / (chapter + ".md")
    if not path.is_file():
        errors.append(f"missing source chapter {chapter}")
        continue
    src = path.read_text(encoding="utf-8")
    for section in ("Exercises", "Map update"):
        if not any(line.startswith("## ") and line.rstrip().endswith(section) for line in src.splitlines()):
            errors.append(f"{chapter} missing {section} section")
    if not src.startswith(f"# {chapter}"):
        errors.append(f"{chapter} incorrect title")
    if len(src) < 3000:
        errors.append(f"{chapter} shorter than minimum candidate length")
    if any(ch in src for ch in (r"\(", r"\)", r"\[", r"\]")):
        errors.append(f"{chapter} unsupported GitHub MathJax delimiters")
    if any(ord(ch) < 32 and ch not in "\t\r\n" for ch in src):
        errors.append(f"{chapter} control characters")
    displays = 0
    for n, line in enumerate(src.splitlines(), start=1):
        if line.strip() == "$$":
            displays += 1
        elif "$$" in line or line.count("$") % 2:
            errors.append(f"{chapter}:{n} invalid math dollars")
    if displays % 2:
        errors.append(f"{chapter} unbalanced display math")
    if FIGURES[chapter] + ".svg" not in src:
        errors.append(f"{chapter} missing its figure embed")
    if (ROOT / "build/site").exists():
        html = ROOT / f"build/site/chapters/{chapter}/index.html"
        if not html.is_file():
            errors.append(f"{chapter}: missing HTML")
            continue
        content = html.read_text(encoding="utf-8")
        if "arithmatex" not in content or "mathjax" not in content.lower():
            errors.append(f"{chapter}: MathJax/Arithmatex not integrated")
        if FIGURES[chapter] + ".svg" not in content:
            errors.append(f"{chapter}: figure missing from HTML")
if (ROOT / "build/site").exists():
    site = ROOT / "build/site"
    home = (site / "index.html").read_text(encoding="utf-8")
    if "NOT YET ACCEPTED FOR PUBLICATION" not in home:
        errors.append("missing visible preview-not-publication declaration")
    for id in FIGURES.values():
        svg = site / "figures/generated" / (id + ".svg")
        try:
            root = ET.parse(svg).getroot()
            if not root.tag.endswith("svg"):
                errors.append(f"{id}: invalid vector root")
        except (ET.ParseError, FileNotFoundError) as exc:
            errors.append(f"{id}: missing or invalid SVG: {exc}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("PASS: 6 chapters, figure refs, MathJax source and built HTML (when present).")
print("Not an independent mathematical, accessibility, PDF, or publication approval.")
