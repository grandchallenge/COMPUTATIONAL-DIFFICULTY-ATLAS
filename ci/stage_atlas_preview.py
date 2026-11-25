"""Build the integrated review edition; never deploy."""
from pathlib import Path
from shutil import copyfile, rmtree
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"build"/"atlas-docs"
if OUT.exists():
    rmtree(OUT)
for d in ("chapters","figures/generated","assets"):
    (OUT/d).mkdir(parents=True,exist_ok=True)
vendor=ROOT/"vendor/mathjax/tex-mml-svg.js"
assert sha256(vendor.read_bytes()).hexdigest()=="1f17a7ed95ff4a4b27d16bf0fb5f80b915686ee8673e82983a2876ecf8cb9fae"
copyfile(vendor,OUT/"assets/mathjax-3.2.2-tex-mml-svg.js")
copyfile(ROOT/"ci/assets/keystone-review.css",OUT/"assets/keystone-review.css")
index=["# A Mathematical Atlas of Computational Difficulty","","**Integrated review candidate. Not approved for publication.**","","## Chapters",""]
for n in range(1,24):
    name=f"C{n:02}.md"
    source=ROOT/"chapters"/name
    title=source.read_text().splitlines()[0].removeprefix("# ")
    copyfile(source,OUT/"chapters"/name)
    index.append(f"- [{title}](chapters/{name})")
for source in (ROOT/"figures/generated").iterdir():
    if source.is_file():
        copyfile(source,OUT/"figures/generated"/source.name)
for source in (ROOT/"figures").glob("*_CAPTION.md"):
    copyfile(source,OUT/"figures"/source.name)
(OUT/"index.md").write_text("\n".join(index)+"\n")
print("Staged 23 chapters for review only.")
