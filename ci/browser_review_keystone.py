#!/usr/bin/env python3
"""Actual Chromium/MathJax visual and PDF acceptance *candidate* replay.

Runs only after the save-before-display gate and MkDocs build. Produces review
artifacts, not a released or independently certified book.
"""
from pathlib import Path
import json
from pypdf import PdfReader, PdfWriter
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "build/site"
OUT = ROOT / "build/browser-review"
OUT.mkdir(parents=True, exist_ok=True)
CHAPTERS = ["C01", "C04", "C05", "C10", "C15", "C20"]
pages = []
replay = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for id in CHAPTERS:
        page = browser.new_page(viewport={"width": 1240, "height": 860},
                                device_scale_factor=1)
        address = (SITE / "chapters" / id / "index.html").resolve().as_uri()
        page.goto(address, wait_until="load", timeout=90000)
        page.wait_for_function("!!(window.MathJax && window.MathJax.typesetPromise)",
                               timeout=90000)
        page.evaluate("() => window.MathJax.typesetPromise()")
        page.wait_for_function("document.querySelectorAll('mjx-container').length > 0",
                               timeout=90000)
        evidence = page.evaluate("""() => ({
          mathContainers: document.querySelectorAll('mjx-container').length,
          totalImgs: document.querySelectorAll('img').length,
          invalidImgs: [...document.querySelectorAll('img')].filter(
              img => !img.complete || img.naturalWidth === 0).map(img => img.src),
          bodyWidth: document.body.scrollWidth,
          viewportWidth: document.documentElement.clientWidth
        })""")
        if evidence["mathContainers"] < 2 or evidence["invalidImgs"]:
            raise RuntimeError(f"{id}: math images not typeset/rendered: {evidence}")
        # Ensure responsive display does not create major horizontal overflow.
        if evidence["bodyWidth"] > evidence["viewportWidth"] + 24:
            raise RuntimeError(f"{id}: horizontal overflow in desktop preview: {evidence}")
        page.screenshot(path=str(OUT / f"{id}_desktop.png"), full_page=True)
        # Mobile width is tested independently; browser print remains page-size.
        page.set_viewport_size({"width": 430, "height": 880})
        page.screenshot(path=str(OUT / f"{id}_mobile.png"), full_page=True)
        mobile = page.evaluate("""() => ({
          pageWidth: document.documentElement.clientWidth,
          bodyWidth: document.body.scrollWidth,
          htmlWidth: document.documentElement.scrollWidth,
          bodyRect: Math.round(document.body.getBoundingClientRect().width),
          htmlRect: Math.round(document.documentElement.getBoundingClientRect().width),
          bodyMinWidth: getComputedStyle(document.body).minWidth,
          bodyOverflowX: getComputedStyle(document.body).overflowX,
          innerWidth: window.innerWidth,
          offenders: [...document.body.getElementsByTagName('div')].map(el=>({tag:el.tagName,right:Math.round(el.getBoundingClientRect().right),width:Math.round(el.getBoundingClientRect().width)})).filter(z=>z.right>454).slice(0,12)
        })""")
        if mobile["bodyWidth"] > mobile["pageWidth"] + 24:
            raise RuntimeError(f"{id}: mobile overflow: {mobile}")
        page.emulate_media(media="print")
        out_pdf = OUT / f"{id}.pdf"
        page.pdf(path=str(out_pdf), print_background=True, format="A4",
                 margin={"top":"16mm","bottom":"16mm","left":"16mm","right":"16mm"},
                 prefer_css_page_size=False)
        count = len(PdfReader(str(out_pdf)).pages)
        if count < 2:
            raise RuntimeError(f"{id}: suspiciously short PDF, {count} pages")
        pages.append((id, out_pdf))
        replay.append({"chapter":id, "pages":count, "desktop":evidence,
                       "mobile":mobile, "source_url":address})
        page.close()
    browser.close()

writer = PdfWriter()
for id, pdf in pages:
    writer.append(str(pdf), import_outline=True)
writer.add_metadata({
    "/Title":"A Mathematical Atlas of Computational Difficulty — UNACCEPTED Six-Keystone Preview",
    "/Subject":"Review-only browser-typeset manuscript; not an approved publication",
})
result = OUT / "CDA_six_keystones_REVIEW_ONLY.pdf"
with result.open("wb") as f:
    writer.write(f)
total = len(PdfReader(str(result)).pages)
if total != sum(r["pages"] for r in replay):
    raise RuntimeError("Combined PDF page count disagrees with chapter pages")
(OUT / "BROWSER_PDF_REPLAY.json").write_text(
    json.dumps({"schema":"CDA-BROWSER-PDF-REPLAY/1",
                "publication_authorized":False,
                "mathematically_certified":False,
                "total_pages":total, "chapters":replay},indent=2)+"\n",
    encoding="utf-8"
)
print(f"PASS: {len(replay)} browser-rendered MathJax chapters, {total} PDF pages")
print("Desktop/mobile screenshots and review-only PDF saved after persisted-source gate.")
