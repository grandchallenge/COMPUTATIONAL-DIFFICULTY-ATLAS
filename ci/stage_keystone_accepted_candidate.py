#!/usr/bin/env python3
"""Stage the six corrected keystone chapters for an UNACCEPTED MkDocs review.

All Wolfram source+SVG assets must already be committed and validated by
ci/verify_persisted_wolfram_assets.py before this script may run.
"""
from pathlib import Path
from shutil import copyfile, rmtree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "docs"
CHAPTERS = {
    "C01": "What Is a Computational Problem?",
    "C04": "Verification, Certificates, and NP",
    "C05": "Reductions: Transporting Difficulty",
    "C10": "Time, Space, and Savitch's Theorem",
    "C15": "Quantum Computation",
    "C20": "Undecidability and the Halting Problem",
}
FIGURES = {
    "F3_1": "tsp_formulation_fork",
    "F3_2": "np_verifier",
    "F2_1": "translator_solver",
    "F4_3": "savitch_midpoint",
    "F15_1": "grover_query_scaling",
    "F6_2": "halting_diagonal",
}
if OUT.exists():
    rmtree(OUT)
for directory in ("chapters", "figures/generated", "figures", "sources"):
    (OUT / directory).mkdir(parents=True, exist_ok=True)
for id in CHAPTERS:
    path = ROOT / "chapters" / (id + ".md")
    if not path.exists():
        raise SystemExit(f"Missing chapter: {path}")
    copyfile(path, OUT / "chapters" / path.name)
for id, name in FIGURES.items():
    for rel in (f"figures/generated/{id}_{name}.svg", f"figures/{id}_CAPTION.md"):
        file = ROOT / rel
        if not file.exists():
            raise SystemExit(f"Missing Wolfram figure or caption: {rel}")
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        copyfile(file, dest)
copyfile(ROOT / "reviews/KEYSTONE_PRIMARY_SOURCES_001.md",
         OUT / "sources/primary_sources.md")
intro = [
    "# A Mathematical Atlas of Computational Difficulty",
    "",
    "**EDITORIAL CANDIDATE — NOT YET ACCEPTED FOR PUBLICATION.**",
    "",
    "Six keystone chapters corrected after authenticated GCL mathematical critiques.",
    "The figures are saved and source-linked but remain candidates pending final-width",
    "mathematical, typography, and accessibility acceptance. This preview is not deployed",
    "to the public MkDocs site.",
    "",
    "## Chapters", "",
]
intro += [f"- [{name}](chapters/{id}.md)" for id, name in CHAPTERS.items()]
intro += ["", "## Source and figure evidence", "",
          "- [Primary mathematical sources](sources/primary_sources.md)",
          "- [All six Wolfram figure captions](figures/index.md)", "",
          "Successful CI and rendering do not substitute for a non-author editorial approval.", ""]
(OUT / "index.md").write_text("\n".join(intro), encoding="utf-8")
gallery = [
    "# Wolfram figure inventory",
    "",
    "**All six are saved vector graphics; none is yet a certified publication figure.**",
    "",
]
for id, name in FIGURES.items():
    gallery.extend([f"## {id.replace('_', '.')}", "",
                    f"![Wolfram mathematical diagram {id}; see the linked full caption for a detailed accessible description.](generated/{id}_{name}.svg)",
                    "",
                    f"[Mathematical caption and accessibility description]({id}_CAPTION.md)", ""])
(OUT / "figures" / "index.md").write_text("\n".join(gallery), encoding="utf-8")
print("Staged 6 editorial chapters, 6 committed SVG figures and source ledger.")
