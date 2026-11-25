#!/usr/bin/env bash
# Exact symbolic map export, no display. Run from repository root.
set -euo pipefail
ROOT=$(pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
latex -interaction=nonstopmode -halt-on-error -output-directory="$TMP" figures/src/F23_atlas_maps.tex > "$TMP/latex.log"
dvisvgm --no-fonts --exact --bbox=min --page=1-7 --output="$TMP/F23_%p.svg" "$TMP/F23_atlas_maps.dvi"
python - "$TMP" "$ROOT" <<'PY'
from pathlib import Path
import sys,xml.etree.ElementTree as ET
tmp,root=map(Path,sys.argv[1:])
for n in range(1,8):
    p=tmp/f"F23_{n}.svg"
    r=ET.parse(p).getroot()
    assert r.tag.endswith("}svg") and "viewBox" in r.attrib
    assert any(e.tag.endswith("}path") for e in r.iter())
    assert not any(e.tag.endswith("}image") for e in r.iter())
    dest=root/"figures/generated"/p.name
    dest.write_bytes(p.read_bytes())
PY
