#!/usr/bin/env python3
"""Structural, provenance and accessibility checks for F2.1/F6.2 candidate SVGs.

This does NOT constitute a Wolfram-engine replay or independent visual acceptance.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "F2_1": {
        "name": "translator_solver",
        "claim": "many_one_polynomial_reduction_direction_not_hardness_proof",
        "required": ("many-one reduction", "decider for", "does **not**"),
    },
    "F6_2": {
        "name": "halting_diagonal",
        "claim": "diagonal_proof_schematic_not_computation",
        "required": ("total algorithm", "both disagree", "logical contradiction"),
    },
}
errors = []
for stem, contract in FILES.items():
    output = ROOT / "figures" / "generated" / f"{stem}_{contract['name']}.svg"
    source = ROOT / "figures" / "src" / f"{stem}_{contract['name']}.wl"
    caption = ROOT / "figures" / f"{stem}_CAPTION.md"
    metadata = ROOT / "figures" / "metadata" / f"{stem}.yaml"
    for f in (output, source, caption, metadata):
        if not f.is_file():
            errors.append(f"{stem}: missing {f}")
    if any(not f.is_file() for f in (output, source, caption, metadata)):
        continue
    try:
        root = ET.parse(output).getroot()
    except ET.ParseError as exc:
        errors.append(f"{output}: invalid vector XML: {exc}")
        continue
    if not root.tag.endswith("svg"):
        errors.append(f"{output}: missing SVG root")
    if not root.get("viewBox"):
        errors.append(f"{output}: missing viewBox for responsive scaling")
    if not any(el.tag.endswith("path") for el in root.iter()):
        errors.append(f"{output}: no vector path geometry")
    if any(el.tag.endswith("image") for el in root.iter()):
        errors.append(f"{output}: contains embedded raster image")
    raw = output.read_text(encoding="utf-8")
    if raw.count("<g") != raw.count("</g>"):
        errors.append(f"{output}: mismatched vector group count")
    if raw.count("<symbol") != raw.count("</symbol>"):
        errors.append(f"{output}: mismatched glyph-symbol count")
    body = caption.read_text(encoding="utf-8")
    for expected in contract["required"]:
        if expected.casefold() not in body.casefold():
            errors.append(f"{caption}: missing semantic scope: {expected}")
    if "**Status:**" not in body or "pending" not in body.lower():
        errors.append(f"{caption}: must identify unreviewed acceptance status")
    if "Accessibility" not in body:
        errors.append(f"{caption}: missing accessible verbal description")
    if r"\(" in body or r"\[" in body:
        errors.append(f"{caption}: use GitHub-native dollar mathematical delimiters")
    if any(line.count("$") % 2 for line in body.splitlines()):
        errors.append(f"{caption}: mismatched inline math delimiters")
    md = metadata.read_text(encoding="utf-8")
    if "status: wolfram_svg_candidate_unreviewed" not in md:
        errors.append(f"{metadata}: status must remain unreviewed")
    if contract["claim"] not in md:
        errors.append(f"{metadata}: missing exact claim scope")
    wl = source.read_text(encoding="utf-8")
    if f"{stem}_{contract['name']}.svg" not in wl or "Export[" not in wl:
        errors.append(f"{source}: no Wolfram export reproduction command")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("Two figure SVGs parse, preserve vector glyphs, carry scope/accessibility and Wolfram reproduction source.")
print("NOT mathematical acceptance or verified source-render equivalence.")
