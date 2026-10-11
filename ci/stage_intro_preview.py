#!/usr/bin/env python3
"""Build an unaccepted C02/C03 editorial reading preview; no Pages publishing."""
from pathlib import Path
from shutil import copyfile, rmtree

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "build" / "intro-docs"
if DEST.exists():
    rmtree(DEST)
(DEST / "chapters").mkdir(parents=True)
for code in ("C02", "C03"):
    file = ROOT / "chapters" / f"{code}.md"
    assert file.is_file()
    copyfile(file, DEST / "chapters" / file.name)
(DEST / "index.md").write_text(
    "# Computational Difficulty Atlas — introductory manuscript review\n\n"
    "**UNACCEPTED EDITORIAL CANDIDATES; NOT A PUBLIC RELEASE.**\n\n"
    "- [C02 — Cost models and asymptotics](chapters/C02.md)\n"
    "- [C03 — Deterministic polynomial time and P](chapters/C03.md)\n\n"
    "These two chapters connect the protected C01/C04 content but are not "
    "yet mathematically accepted. Full Wolfram figures will be developed separately "
    "under save-before-display provenance requirements.\n",
    encoding="utf-8"
)
