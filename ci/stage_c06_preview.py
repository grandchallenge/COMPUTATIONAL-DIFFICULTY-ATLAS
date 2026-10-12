#!/usr/bin/env python3
"""Stage unaccepted C06 with source-only MathJax; figures remain unproduced."""
from pathlib import Path
from shutil import copyfile,rmtree
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/"build/c06-docs"
if DEST.exists():
    rmtree(DEST)
(DEST/"chapters").mkdir(parents=True)
copyfile(ROOT/"chapters/C06.md",DEST/"chapters/C06.md")
(DEST/"index.md").write_text(
    "# Atlas C06 — Editorial Mathematical Review\n\n"
    "**UNACCEPTED manuscript candidate, not a published or independently certified chapter.**\n\n"
    "[C06 — NP-Completeness: Finding the Hardest Verification Problems](chapters/C06.md)\n\n"
    "The 3SAT-to-CLIQUE figure remains unproduced. No unsaved Wolfram visualization "
    "will be used as a substitute for durable source and a complete vector export.\n",
    encoding="utf-8"
)
