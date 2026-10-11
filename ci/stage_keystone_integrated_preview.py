#!/usr/bin/env python3
"""Stage a visibly unaccepted integrated six-chapter MkDocs preview.

Does not alter the exact copied chapter content or release to GitHub Pages.
Every borrowed chapter/figure is checked against its immutable Git blob SHA.
"""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "preview/KEYSTONE_SOURCE_LOCK.json").read_text())
assert LOCK["status"] == "UNACCEPTED_EDITORIAL_PREVIEW_NOT_PUBLISHED"
assert not LOCK["publisher_authority"] and not LOCK["editorial_acceptance"]
TARGET = ROOT / "build/docs"
if TARGET.exists():
    shutil.rmtree(TARGET)
for folder in ("chapters", "figures/generated", "figures", "sources", "review"):
    (TARGET / folder).mkdir(parents=True, exist_ok=True)

def blob_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

chapters = {
    "C01": "What Is a Computational Problem?",
    "C04": "Verification, Certificates, and NP",
    "C05": "Reductions and Hardness",
    "C10": "Space Complexity and Savitch",
    "C15": "Quantum Computation",
    "C20": "The Limits of Computability",
}
for chapter in chapters:
    source = ROOT / "chapters" / f"{chapter}.md"
    data = source.read_bytes()
    expected = LOCK["chapters"][chapter]["blob_sha"]
    if blob_sha(data) != expected:
        raise SystemExit(f"{chapter}: source changed outside exact-head lock")
    shutil.copyfile(source, TARGET / "chapters" / source.name)

FIGURES = {
    "F3_1": "tsp_formulation_fork",
    "F3_2": "np_verifier",
    "F2_1": "translator_solver",
    "F4_3": "savitch_midpoint",
    "F15_1": "grover_query_scaling",
    "F6_2": "halting_diagonal",
}
for fig, suffix in FIGURES.items():
    svg = ROOT / "figures/generated" / f"{fig}_{suffix}.svg"
    if not svg.exists():
        raise SystemExit(f"Missing figure candidate {svg}")
    if str(svg.relative_to(ROOT)) in LOCK["branch_only_figure_blobs"]:
        if blob_sha(svg.read_bytes()) != LOCK["branch_only_figure_blobs"][str(svg.relative_to(ROOT))]:
            raise SystemExit(f"Changed branch-only figure: {svg}")
    shutil.copyfile(svg, TARGET / "figures/generated" / svg.name)
    caption = ROOT / "figures" / f"{fig}_CAPTION.md"
    if not caption.exists():
        raise SystemExit(f"Missing caption {caption}")
    shutil.copyfile(caption, TARGET / "figures" / caption.name)

shutil.copyfile(ROOT / "reviews/KEYSTONE_PRIMARY_SOURCES_001.md",
                TARGET / "sources/primary_sources.md")
shutil.copyfile(ROOT / "reviews/CDA_REV_C01_002_CAPTURE.md",
                TARGET / "review/C01_return_capture.md")
shutil.copyfile(ROOT / "preview/KEYSTONE_SOURCE_LOCK.json",
                TARGET / "SOURCE_LOCK.json")

index = [
    "# A Mathematical Atlas of Computational Difficulty — integrated keystone preview",
    "",
    "**UNACCEPTED EDITORIAL PREVIEW. These drafts have not passed final mathematical review, figure approval or publication acceptance.**",
    "",
    "The pages reproduce the exact source blobs of the separate chapter proposals; supplemental figures are shown in a review gallery rather than silently inserted into frozen manuscripts.",
    "",
    "## Six keystone chapters",
    "",
]
index += [f"- [{code} — {title}](chapters/{code}.md)" for code, title in chapters.items()]
index += ["", "## Supporting review evidence", "",
          "- [Figure gallery](figures/index.md) — six unreviewed Wolfram vector candidates.",
          "- [Primary-source ledger](sources/primary_sources.md) — bibliography and claim-scope reconnaissance.",
          "- [C01 RESULT/1 capture](review/C01_return_capture.md) — returned critique, not adjudicated.",
          "- [Exact Git source lock](SOURCE_LOCK.json) — immutable source heads and blob hashes.",
          "",
          "No figure or manuscript chapter on this site is certified or authorized for final public release."]
(TARGET / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
gallery = ["# Six keystone figure candidates", "",
           "**All figures are unreviewed vector candidates, not publication-ready graphics.**",
           ""]
for fig, suffix in FIGURES.items():
    label = fig.replace("_", ".")
    gallery.extend([
        f"## {label}",
        "",
        f"![Candidate Wolfram figure {label}; see detailed accessible caption linked below.](generated/{fig}_{suffix}.svg)",
        "",
        f"[Mathematical caption and accessibility description]({fig}_CAPTION.md)",
        "",
    ])
(TARGET / "figures/index.md").write_text("\n".join(gallery) + "\n", encoding="utf-8")
print("Verified exact Git blobs and staged six chapters, six SVG candidates, source ledger and receipt.")
