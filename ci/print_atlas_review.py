"""Render a single tagged PDF, not a concatenation of tagged chapter PDFs.

Review-only. Tag structure is not a PDF/UA conformance or screen-reader test.
Run after persisted figure verification and strict integrated staging.
"""
from pathlib import Path
from functools import partial
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import html, json, re, subprocess
from collections import Counter
from pypdf.generic import IndirectObject
import markdown
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"build/atlas-site"
OUT=ROOT/"build/atlas-print-review"
OUT.mkdir(parents=True,exist_ok=True)
commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
def persisted(rel):
    path=ROOT/rel
    blob=subprocess.check_output(["git","show",f"HEAD:{rel}"],cwd=ROOT)
    if blob != path.read_bytes():
        raise RuntimeError(f"Uncommitted asset {rel}")
    return sha256(blob).hexdigest()
figures={p.relative_to(ROOT).as_posix():persisted(p.relative_to(ROOT).as_posix())
         for p in (ROOT/"figures/generated").glob("*.svg")}
assert len(figures)>=29
titles=[]
articles=[]
for n in range(1,24):
    id=f"C{n:02}"
    source=(ROOT/"chapters"/(id+".md")).read_text()
    title=source.splitlines()[0].removeprefix("# ")
    titles.append((id,title))
    body=markdown.markdown("\n".join(source.splitlines()[1:]),extensions=["tables","fenced_code","pymdownx.arithmatex"],extension_configs={"pymdownx.arithmatex":{"generic":True}})
    body=re.sub(r"<(/?)h([2-5])>",lambda m:f"<{m[1]}h{int(m[2])+1}>",body)
    body=body.replace('src="../figures/','src="figures/')
    body=re.sub(r'href="\.\./figures/([^"]+)_CAPTION\.md"',r'href="#caption-\1"',body)
    articles.append(f'<article id="{id}"><h2>{html.escape(title)}</h2>{body}</article>')
captions=[]
for p in sorted((ROOT/"figures").glob("*_CAPTION.md")):
    if p.stem=="F1_1_CAPTION":
        continue # exploratory raster not included in the manuscript
    raw=p.read_text()
    title=raw.splitlines()[0].removeprefix("# ")
    # Caption appendix carries full prose, not merely inaccessible vector glyphs.
    content=markdown.markdown("\n".join(raw.splitlines()[1:]),extensions=["tables","pymdownx.arithmatex"],extension_configs={"pymdownx.arithmatex":{"generic":True}})
    # Caption-relative local links become durable exact-commit repository links.
    content=re.sub(r'href="(?!https?://|#|mailto:)([^"]+)"',lambda m:'href="https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/blob/'+commit+'/figures/'+html.escape(m[1],quote=True)+'"',content)
    captions.append(f'<section id="caption-{p.stem.removesuffix("_CAPTION")}"><h3>{html.escape(title)}</h3>{content}</section>')
toc="".join(f'<li><a href="#{id}">{html.escape(title)}</a></li>' for id,title in titles)
css=r"""
@page {size:A4; margin:18mm 17mm 18mm 17mm; @bottom-center {content:counter(page);font-size:9pt}}
html{font-family:Georgia,'Times New Roman',serif;font-size:11pt;color:#111;background:white}
body{margin:0;line-height:1.43;overflow-wrap:anywhere}
h1{font-size:28pt;line-height:1.14}
h2{font-size:22pt;line-height:1.2}
h3{font-size:15pt}h4{font-size:12pt}
h1,h2,h3,h4{break-after:avoid}
article, .appendix{break-before:page}
p,li{orphans:3;widows:3}
img{display:block;max-width:100%;max-height:165mm;width:auto;height:auto;margin:8pt auto}
p:has(>img){break-inside:avoid}
pre{white-space:pre-wrap;font-size:9pt;break-inside:avoid}
table{border-collapse:collapse;max-width:100%;font-size:10pt}
th,td{border-bottom:1px solid #aaa;padding:3pt 5pt;text-align:left}
tr{break-inside:avoid}thead{display:table-header-group}
mjx-container[display="true"]{break-inside:avoid;max-width:100%;overflow-wrap:normal}
a{color:#222;text-decoration:underline}
.cover{break-after:page}.toc{break-after:page}
"""
doc=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>A Mathematical Atlas of Computational Difficulty — Review edition</title><style>{css}</style><script>window.MathJax={{options:{{enableAssistiveMml:true}}}};</script><script defer src="assets/mathjax-3.2.2-tex-mml-svg.js"></script></head><body><main><section class="cover"><h1>A Mathematical Atlas of Computational Difficulty</h1><p>Grand Challenge Labs</p><p><strong>Editorial review candidate — not approved for publication.</strong></p><p>Source revision: {commit}</p></section><nav class="toc" aria-label="Table of contents"><h2>Contents</h2><ol>{toc}<li><a href="#captions">Figure descriptions and provenance</a></li></ol></nav>{''.join(articles)}<section class="appendix" id="captions"><h2>Figure descriptions and provenance</h2>{''.join(captions)}</section></main></body></html>"""
(SITE/"print-review.html").write_text(doc)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=str(SITE)))
Thread(target=server.serve_forever,daemon=True).start()
pdf=OUT/"CDA_atlas_REVIEW_ONLY.pdf"
try:
    with sync_playwright() as p:
        browser=p.chromium.launch()
        page=browser.new_page(viewport={"width":665,"height":1123})
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        response=page.goto(f"http://127.0.0.1:{server.server_port}/print-review.html",wait_until="load",timeout=90000)
        assert response.status==200
        page.wait_for_function("!!(window.MathJax && window.MathJax.startup && window.MathJax.startup.promise)",timeout=90000)
        page.evaluate("() => window.MathJax.startup.promise")
        page.emulate_media(media="print")
        evidence=page.evaluate("""() => ({
          articles:document.querySelectorAll('article').length,
          math:document.querySelectorAll('mjx-container').length,
          assistive:document.querySelectorAll('mjx-assistive-mml').length,
          mathErrors:document.querySelectorAll('mjx-merror,[data-mml-node=merror]').length,
          images:document.images.length,
          badImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth||!i.alt.trim()).map(i=>i.src),
          badLinks:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash),
          lang:document.documentElement.lang,
          overflow:document.body.scrollWidth>document.documentElement.clientWidth+24
        })""")
        assert evidence["articles"]==23 and evidence["math"]>1000 and evidence["assistive"]==evidence["math"] and evidence["images"]>=29,evidence
        assert not (evidence["mathErrors"] or evidence["badImages"] or evidence["badLinks"] or errors),evidence
        # Preserve browser MathML in the HTML artifact. Chromium PDF does not
        # export MathML as Formula tags; for print only, mark each rendered
        # expression as an image with the exact source TeX as a text fallback.
        tagged_math=page.evaluate("""() => {
          let count=0;
          for(const item of MathJax.startup.document.math) {
            const el=item.typesetRoot;
            if(!el || !item.math) continue;
            const wrapper=el.parentElement;
            if(!wrapper || !wrapper.classList.contains('arithmatex')) continue;
            const svg=el.querySelector('svg');
            if(!svg) continue;
            const rect=svg.getBoundingClientRect();
            const align=svg.style.verticalAlign;
            const clone=svg.cloneNode(true);
            clone.removeAttribute('aria-hidden');
            clone.setAttribute('xmlns','http://www.w3.org/2000/svg');
            clone.setAttribute('width',String(rect.width));
            clone.setAttribute('height',String(rect.height));
            clone.style.verticalAlign='';
            const img=new Image();
            img.alt='Mathematical expression (TeX): '+item.math;
            img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(clone));
            img.style.cssText='display:inline-block;margin:0;max-width:100%;height:auto;width:'+rect.width+'px;vertical-align:'+align;
            el.replaceWith(img);
            count++;
          }
          return count;
        }""")
        assert tagged_math==evidence["math"],(tagged_math,evidence["math"])
        evidence["print_math_text_alternatives"]=tagged_math
        page.evaluate("() => Promise.all([...document.images].map(i=>i.decode()))")
        assert page.evaluate("() => [...document.images].every(i=>i.complete && i.naturalWidth>0 && i.alt.trim())")
        assert not evidence["overflow"],evidence
        page.pdf(path=pdf,prefer_css_page_size=True,print_background=True,tagged=True,outline=True)
        browser.close()
finally:
    server.shutdown()
    server.server_close()
reader=PdfReader(pdf)
root=reader.trailer["/Root"]
marked=bool(root.get("/MarkInfo",{}).get("/Marked",False))
tagged="/StructTreeRoot" in root
def flatten(items):
    for item in items:
        if isinstance(item,list):
            yield from flatten(item)
        else:
            yield str(getattr(item,"title",""))
bookmarks=list(flatten(reader.outline))
chapter_bookmarks=[id for id,title in titles if any(t.startswith(id+" ") for t in bookmarks)]
roles=Counter()
alt=Counter()
seen=set()
def visit(x):
    if isinstance(x,IndirectObject):
        key=(x.idnum,x.generation)
        if key in seen:
            return
        seen.add(key)
        x=x.get_object()
    if isinstance(x,list):
        for y in x:
            visit(y)
    elif isinstance(x,dict):
        role=str(x.get("/S",""))
        if role:
            roles[role]+=1
            if "/Alt" in x:
                description=str(x["/Alt"])
                alt["math" if description.startswith("Mathematical expression (TeX): ") else "other"]+=1
        if "/K" in x:
            visit(x["/K"])
visit(root["/StructTreeRoot"])
assert marked and tagged and len(chapter_bookmarks)==23 and len(reader.pages)>23
assert alt["math"]==evidence["math"] and alt["other"]==evidence["images"],(alt,evidence)
assert str(root.get("/Lang",""))=="en"
evidence.update(source_commit=commit,pages=len(reader.pages),tagged=tagged,marked=marked,
    outline_entries=len(bookmarks),chapter_bookmarks=len(chapter_bookmarks),
    pdf_lang=str(root.get("/Lang","")),pdf_structure_roles=dict(roles),
    pdf_math_tex_alt=alt["math"],pdf_illustration_alt=alt["other"],
    pdf_sha256=sha256(pdf.read_bytes()).hexdigest(),pdf_bytes=pdf.stat().st_size,
    figure_sha256=figures,publication_authorized=False,pdf_ua_certified=False,
    math_accessibility_boundary="Exact TeX alternatives on PDF Figure tags, not semantic Formula tags or a validated spoken-math experience; HTML retains assistive MathML.")
(OUT/"PRINT_REVIEW.json").write_text(json.dumps(evidence,indent=2)+"\n")
print(json.dumps({k:v for k,v in evidence.items() if k!="figure_sha256"},indent=2))
