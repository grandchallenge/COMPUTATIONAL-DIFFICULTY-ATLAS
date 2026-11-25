"""Reproducible source-locked symbolic chapter diagrams; never displays output."""
from pathlib import Path
import json, subprocess, tempfile, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[3]
SOURCE=Path(__file__).resolve().parent
rows=sum([json.loads(p.read_text()) for p in sorted(SOURCE.glob("part*.json"))],[])
assert len(rows)==len({r["n"] for r in rows})==16
PRE=r"""\documentclass[11pt]{article}
\usepackage{amsmath,amssymb}
\pagestyle{empty}
\setlength{\textwidth}{420pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt}
\begin{document}
"""
def caption(r):
    return f"# FP{r['n']} — {r['title']}\n\n**Status:** Unaccepted vector candidate; chapter-level review and final print/accessibility acceptance pending.\n\n**Caption and text alternative.** {r['cap']}\n\n**Source:** figures/src/progressive/part*.json; export using \`python figures/src/progressive/generate.py\`. Exact mathematical tables/diagrams, not benchmark measurements. Misconceptions: {r['mis']}.\n"
def meta(r):
    return f"figure_id: FP{r['n']}\nchapter: C{r['n']}\ntitle: {r['title']}\nstatus: latex_svg_candidate_unreviewed\nsource: figures/src/progressive/part*.json\ngenerator: LaTeX and dvisvgm\ngeneration_command: python figures/src/progressive/generate.py\noutput_artifact: figures/generated/FP{r['n']}.svg\ncaption: figures/FP{r['n']}_CAPTION.md\nmisconceptions: '{r['mis']}'\nreview_required: [mathematical, pedagogical, final_width_typography, accessibility, reproducible_export]\n"
import sys
if "--prepare" in sys.argv:
    for r in rows:
        (ROOT/f"figures/FP{r['n']}_CAPTION.md").write_text(caption(r))
        (ROOT/f"figures/metadata/FP{r['n']}.yaml").write_text(meta(r))
    raise SystemExit(0)
with tempfile.TemporaryDirectory() as d:
    tmp=Path(d)
    for r in rows:
        id="FP"+r["n"]
        src=tmp/(id+".tex")
        src.write_text(PRE+r"\textbf{\large "+r["title"]+r"}\par\medskip"+"\n"+r["tex"]+"\n"+r"\end{document}"+"\n")
        result=subprocess.run(["latex","-interaction=nonstopmode","-halt-on-error",src.name],cwd=tmp,capture_output=True,text=True)
        if result.returncode:
            raise RuntimeError(result.stdout[-3000:])
        subprocess.run(["dvisvgm","--no-fonts","--exact","--bbox=min","--page=1",f"--output={id}.svg",f"{id}.dvi"],cwd=tmp,check=True,capture_output=True)
        p=tmp/(id+".svg")
        root=ET.parse(p).getroot()
        width=float(root.attrib["viewBox"].split()[2])
        assert root.tag.endswith("}svg") and 0<width<450,(id,width)
        assert any(e.tag.endswith("}path") for e in root.iter())
        assert not any(e.tag.endswith("}image") for e in root.iter())
        print(id,round(width,2))
    for r in rows:
        id="FP"+r["n"]
        (ROOT/f"figures/generated/{id}.svg").write_bytes((tmp/(id+".svg")).read_bytes())
