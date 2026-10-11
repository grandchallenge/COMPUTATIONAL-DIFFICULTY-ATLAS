#!/usr/bin/env python3
"""Stage only existing manuscript candidates for a preview, not publication."""
from pathlib import Path
from shutil import copyfile, rmtree

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "chapters"
TARGET = ROOT / "build" / "docs"
if TARGET.exists():
    rmtree(TARGET)
(TARGET / "chapters").mkdir(parents=True)
titles = {
    "C01": "What Is a Computational Problem?",
    "C04": "Verification, Certificates, and NP",
    "C05": "Reductions: Translating Problems",
    "C10": "Space Complexity",
    "C15": "Quantum Computation",
    "C20": "The Boundary of Computability",
}
found = []
for code, title in titles.items():
    source = SOURCE / (code + ".md")
    if not source.is_file():
        if code == "C01":
            print("C01 is separately proposed in PR #6; not included in this preview")
            continue
        raise SystemExit(f"Expected manuscript draft missing: {source}")
    copyfile(source, TARGET / "chapters" / source.name)
    found.append((code, title))
content = [
    "# A Mathematical Atlas of Computational Difficulty",
    "",
    "**Editorial preview — not peer-reviewed, accepted, or certified.**",
    "",
    "These chapters are proposed manuscript content. Rendering confirms neither mathematical correctness nor publication approval.",
    "",
    "## Available manuscript drafts",
    "",
]
content.extend(f"- [{code}: {title}](chapters/{code}.md)" for code, title in found)
content.extend(["", "The editorial authority remains in protected GitHub records; do not cite preview text as a certified result.", ""])
(TARGET / "index.md").write_text("\n".join(content), encoding="utf-8")
print(f"Staged {len(found)} candidate chapters for MkDocs preview")
