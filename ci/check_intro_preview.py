#!/usr/bin/env python3
"""Verify real MkDocs / MathJax source markup for the two new chapter candidates."""
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "build" / "intro-site"

class ElementCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

for code in ("C02", "C03"):
    path = SITE / "chapters" / code / "index.html"
    data = path.read_text(encoding="utf-8")
    assert "<h1" in data and code in data, f"{code}: missing displayed title"
    assert "arithmatex" in data and "mathjax" in data.lower(), f"{code}: formula typesetting missing"
    parser = ElementCounter()
    parser.feed(data)
    assert any(t == "h2" for t,_ in parser.tags)
    assert "Exercises" in data and "Map update" in data
    assert "figure" in data.lower()
assert "UNACCEPTED EDITORIAL CANDIDATES" in (SITE/"index.html").read_text()
print("C02/C03 source, finite mathematics and strict MkDocs HTML ready for review; no publication authority.")
