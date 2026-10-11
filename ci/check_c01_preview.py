#!/usr/bin/env python3
"""Stage and check C01 GitHub-compatible maths and Wolfram SVG for MkDocs preview.

This is mechanical evidence, not an independent mathematical review.
"""
from pathlib import Path
import shutil
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
chapter = ROOT / "chapters/C01.md"
svg = ROOT / "figures/generated/F3_1_tsp_formulation_fork.svg"
caption = ROOT / "figures/F3_1_CAPTION.md"
source = ROOT / "figures/src/F3_1_tsp_formulation_fork.wl"
metadata = ROOT / "figures/metadata/F3_1.yaml"
for file in (chapter, svg, caption, source, metadata):
    if not file.exists():
        raise SystemExit(f"Missing required C01 review input: {file}")
text = chapter.read_text(encoding="utf-8")
if any(mark in text for mark in (r"\(", r"\)", r"\[", r"\]")):
    raise SystemExit("C01 uses unsupported GitHub mathematical delimiters")
if any(ord(c) < 32 and c not in "\n\r\t" for c in text):
    raise SystemExit("C01 has invalid control characters")
if "F3_1_tsp_formulation_fork.svg" not in text or "F3_1_CAPTION.md" not in text:
    raise SystemExit("C01 must embed and caption its TSP formulation figure")
display = 0
for i, line in enumerate(text.splitlines(), start=1):
    if line.strip() == "$$":
        display += 1
    elif "$$" in line or line.count("$") % 2:
        raise SystemExit(f"Invalid math delimiter on C01 line {i}")
if display % 2:
    raise SystemExit("Unbalanced C01 display math")
try:
    root = ET.parse(svg).getroot()
except ET.ParseError as err:
    raise SystemExit(f"Invalid Wolfram SVG: {err}")
if not root.tag.endswith("svg") or not any(e.tag.endswith("path") for e in root.iter()):
    raise SystemExit("Wolfram F3.1 SVG has no vector geometry")
if any(e.tag.endswith("image") for e in root.iter()):
    raise SystemExit("Wolfram F3.1 SVG embeds a raster image")
if "render_candidate_unreviewed" not in metadata.read_text(encoding="utf-8"):
    raise SystemExit("F3.1 candidate must preserve explicit unreviewed status")

target = ROOT / "build/docs"
if target.exists():
    shutil.rmtree(target)
(target / "chapters").mkdir(parents=True)
(target / "figures/generated").mkdir(parents=True)
shutil.copyfile(chapter, target / "chapters/C01.md")
shutil.copyfile(svg, target / "figures/generated/F3_1_tsp_formulation_fork.svg")
shutil.copyfile(caption, target / "figures/F3_1_CAPTION.md")
(target / "index.md").write_text(
    "# Computational Difficulty Atlas — C01 editorial preview\n\n"
    "**Not yet independently reviewed or approved for publication.**\n\n"
    "[C01 manuscript draft](chapters/C01.md)\n", encoding="utf-8"
)
print("C01 source + complete vector SVG verified and staged for MkDocs")
