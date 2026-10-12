#!/usr/bin/env python3
"""Validate strict MkDocs C06 preview; not independent mathematical review."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"build/c06-site"
html=(SITE/"chapters/C06/index.html").read_text(encoding="utf-8")
assert "<h1" in html and "NP-Completeness" in html
assert html.count("arithmatex")>=8 and "mathjax" in html.lower()
assert "Exercises" in html and "Map update" in html
assert "Theorem" in html and "Cook" in html and "CLIQUE" in html
assert "UNACCEPTED manuscript candidate" in (SITE/"index.html").read_text()
print("C06 mathematical source and strict MathJax HTML preview PASS; editorial approval pending.")
