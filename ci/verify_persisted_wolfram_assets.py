#!/usr/bin/env python3
"""Gate Wolfram figure displays on committed, validated source + vector blobs.

Run *before* HTML/PNG/inline preview. A green result attests that files already
exist in Git HEAD, not that a picture is independently mathematically certified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FIGURES = {
    "F2_1": "translator_solver",
    "F3_2": "np_verifier",
    "F4_3": "savitch_midpoint",
    "F6_2": "halting_diagonal",
    "F3_1": "tsp_formulation_fork",
    "F15_1": "grover_query_scaling",
}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args], capture_output=True, text=True
    )
    if result.returncode:
        raise ValueError(f"Git provenance read failed: {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.strip()


def assert_persisted(rel: str) -> dict[str, str | int]:
    """Local bytes must match a blob *already in HEAD*, not uncommitted output."""
    path = ROOT / rel
    if not path.is_file():
        raise ValueError(f"Missing durable asset: {rel}")
    committed_oid = git("rev-parse", "--verify", f"HEAD:{rel}")
    if len(committed_oid) != 40 or not all(c in "0123456789abcdef" for c in committed_oid):
        raise ValueError(f"Invalid Git blob ID: {rel}")
    file_oid = git("hash-object", "--", rel)
    if file_oid != committed_oid:
        raise ValueError(f"Uncommitted/modified figure asset: {rel}")
    data = path.read_bytes()
    if not data:
        raise ValueError(f"Zero-byte figure asset: {rel}")
    return {
        "path": rel,
        "bytes": len(data),
        "git_blob_sha1": committed_oid,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def verify_svg(data: bytes, rel: str) -> None:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f"Truncated or malformed SVG {rel}: {exc}") from exc
    if root.tag.split("}")[-1] != "svg":
        raise ValueError(f"Not an SVG root: {rel}")
    if not root.attrib.get("viewBox"):
        raise ValueError(f"Missing responsive vector viewBox: {rel}")
    tags = [node.tag.split("}")[-1] for node in root.iter()]
    if "path" not in tags:
        raise ValueError(f"No vector glyph/path geometry: {rel}")
    if "image" in tags:
        raise ValueError(f"Raster image embedded in candidate vector: {rel}")


def verify_figure(figure: str) -> dict:
    suffix = FIGURES[figure]
    paths = {
        "source": f"figures/src/{figure}_{suffix}.wl",
        "svg": f"figures/generated/{figure}_{suffix}.svg",
        "caption": f"figures/{figure}_CAPTION.md",
        "metadata": f"figures/metadata/{figure}.yaml",
    }
    blobs = {key: assert_persisted(rel) for key, rel in paths.items()}
    verify_svg((ROOT / paths["svg"]).read_bytes(), paths["svg"])
    wl = (ROOT / paths["source"]).read_text(encoding="utf-8")
    md = (ROOT / paths["metadata"]).read_text(encoding="utf-8")
    caption = (ROOT / paths["caption"]).read_text(encoding="utf-8")
    if "Export[" not in wl or Path(paths["svg"]).name not in wl:
        raise ValueError(f"Wolfram source lacks the export of {figure}")
    if f"source: {paths['source']}" not in md or f"output_artifact: {paths['svg']}" not in md:
        raise ValueError(f"Figure metadata does not bind exact source/output for {figure}")
    if "review_complete: []" not in md or "unreviewed" not in md:
        raise ValueError(f"Figure status is not explicitly unreviewed: {figure}")
    if "Reproduce" not in caption and "reproduce" not in caption.lower():
        raise ValueError(f"Caption lacks reproducibility note: {figure}")
    return {"id": figure, **blobs}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--figures", nargs="+", required=True, choices=sorted(FIGURES)
    )
    parser.add_argument(
        "--manifest", default="build/figure-provenance.json",
        help="Small provenance report, not the durable source of truth",
    )
    args = parser.parse_args()
    if len(set(args.figures)) != len(args.figures):
        raise SystemExit("Duplicate figure IDs")
    commit = git("rev-parse", "--verify", "HEAD")
    manifest = {
        "schema": "CDA-WOLFRAM-PERSISTED-BEFORE-PREVIEW/1",
        "checked_out_commit": commit,
        "display_authorized_only_after_this_check": True,
        "mathematical_acceptance": False,
        "publication_authorized": False,
        "figures": [verify_figure(fid) for fid in args.figures],
    }
    dest = ROOT / args.manifest
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(args.figures)} complete Wolfram figures already persisted in Git {commit}")
    print("SVGs parsed and hashed BEFORE preview; mathematical/visual approval remains separate.")


if __name__ == "__main__":
    main()
