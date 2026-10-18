# Offline six-keystone MathJax renderer

This pinned distribution artifact is used only for the unaccepted six-keystone
editorial preview and PDF replay. It prevents loss of visual verification
when the GitHub Actions browser cannot fetch a remote CDN script.

- Upstream: MathJax 3.2.2, component es5/tex-mml-svg.js
- Source URL: https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-svg.js
- SHA256: 1f17a7ed95ff4a4b27d16bf0fb5f80b915686ee8673e82983a2876ecf8cb9fae
- License: Apache License 2.0, upstream LICENSE included.
- Output: SVG math, avoiding CHTML web-font network dependencies.
- Rendering is still verified in real Chromium; bundling is not acceptance.
