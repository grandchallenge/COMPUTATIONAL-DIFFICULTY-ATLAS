"""Integrated review-only browser acceptance; no publication or certification."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/"build/atlas-site"
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server = ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=str(SITE)))
Thread(target=server.serve_forever,daemon=True).start()
records=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for n in range(1,24):
            page=browser.new_page(viewport={"width":1240,"height":860})
            errors=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            resp=page.goto(f"http://127.0.0.1:{server.server_port}/chapters/C{n:02}/",wait_until="load",timeout=30000)
            page.wait_for_function("!!(window.MathJax && window.MathJax.typesetPromise)",timeout=15000)
            page.evaluate("() => window.MathJax.typesetPromise()")
            info=page.evaluate("""() => ({
                math:document.querySelectorAll('mjx-container').length,
                mathErrors:[...document.querySelectorAll('mjx-merror,[data-mml-node=merror]')].map(x=>x.textContent),
                brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.src),
                wide:document.body.scrollWidth>document.documentElement.clientWidth+24,
                numericIds:[...document.querySelectorAll('h2,h3')].filter(x=>/^[0-9]/.test(x.id)).map(x=>x.id)
            })""")
            page.set_viewport_size({"width":430,"height":880})
            info["mobileWide"]=page.evaluate("document.body.scrollWidth>document.documentElement.clientWidth+24")
            info.update(chapter=n,status=resp.status,js=errors)
            records.append(info)
            page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
out=ROOT/"build/atlas-browser-review.json"
out.write_text(json.dumps(records,indent=2)+"\n")
bad=[r for r in records if r["status"]!=200 or not r["math"] or r["mathErrors"] or r["brokenImages"] or r["wide"] or r["mobileWide"] or r["numericIds"] or r["js"]]
if len(records)!=23 or bad:
    raise SystemExit(f"Browser replay failed: {bad}")
print(f"PASS: {len(records)} chapters; desktop and mobile layout, MathJax, images, heading IDs and JavaScript.")
