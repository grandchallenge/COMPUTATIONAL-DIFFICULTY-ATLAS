#!/usr/bin/env python3
"""Test integrated MkDocs HTML structure and source lock (not a browser proof)."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "build/site"
CHAPTERS = ["C01", "C04", "C05", "C10", "C15", "C20"]
FIGURES = ["F3_1_tsp_formulation_fork", "F3_2_np_verifier",
           "F2_1_translator_solver", "F4_3_savitch_midpoint",
           "F15_1_grover_query_scaling", "F6_2_halting_diagonal"]
home = (SITE / "index.html").read_text(encoding="utf-8").lower()
assert "unaccepted editorial preview" in home
assert "not certified" in home or "not passed" in home
lock = json.loads((SITE / "SOURCE_LOCK.json").read_text())
assert len(lock["chapters"]) == 6 and not lock["publisher_authority"]
for chapter in CHAPTERS:
    html = (SITE / "chapters" / chapter / "index.html").read_text(encoding="utf-8")
    assert "arithmatex" in html, f"{chapter}: equations were not wrapped"
    assert "mathjax" in html.lower(), f"{chapter}: math runtime absent"
gallery = (SITE / "figures/index.html").read_text(encoding="utf-8")
for name in FIGURES:
    svg = SITE / "figures/generated" / (name + ".svg")
    root = ET.parse(svg).getroot()
    assert root.tag.endswith("svg") and root.get("viewBox"), name
    assert any(el.tag.endswith("path") for el in root.iter()), name
    assert not any(el.tag.endswith("image") for el in root.iter()), name
    assert name + ".svg" in gallery, name
assert "F3_1_tsp_formulation_fork.svg" in (SITE / "chapters/C01/index.html").read_text()
assert "F15_1_grover_query_scaling.svg" in (SITE / "chapters/C15/index.html").read_text()
assert (SITE / "sources/primary_sources/index.html").is_file()
assert (SITE / "review/C01_return_capture/index.html").is_file()
print("Integrated MkDocs: six chapter pages, math wrappers, six SVGs and exact-head source-lock PASS.")
print("No final-width visual proof, independent mathematical acceptance, PDF or Pages publication asserted.")
