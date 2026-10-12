#!/usr/bin/env python3
"""Source-locked nonpublic C07 math review preview."""
from pathlib import Path
from shutil import copyfile,rmtree
root=Path(__file__).resolve().parents[1]
docs=root/"build/c07-docs"
if docs.exists():
    rmtree(docs)
(docs/"chapters").mkdir(parents=True)
copyfile(root/"chapters/C07.md",docs/"chapters/C07.md")
(docs/"index.md").write_text(
    "# C07 — coNP editorial review\n\n"
    "**UNACCEPTED editorial manuscript: no mathematical certification or public release.**\n\n"
    "[Read C07: coNP, counterexamples and tautology](chapters/C07.md)\n\n"
    "Figures are unproduced; none are rendered from an unsaved Wolfram output.\n",
    encoding="utf-8"
)
