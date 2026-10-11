# A Mathematical Atlas of Computational Difficulty

Grand Challenge Labs (GCL) pedagogical monograph. **Six of the planned 23 chapters are admitted as reviewed manuscripts; the complete book is not yet written or published.**

The governing priorities are mathematical correctness and conceptual clarity, with reproducible Wolfram-first publication typography.

## Read the admitted keystone chapters

- [C01 — What is a computational problem?](chapters/C01.md)
- [C04 — Certificates, verification, and NP](chapters/C04.md)
- [C05 — Reductions and hardness](chapters/C05.md)
- [C10 — Memory, space, and Savitch](chapters/C10.md)
- [C15 — Quantum computation](chapters/C15.md)
- [C20 — Decidability and the halting problem](chapters/C20.md)

**Reading order warning:** C02 (asymptotic cost) and C03 (polynomial time) are not yet drafted; the C04–C05 exposition refers forward/back to these forthcoming chapters.

[Six-keystone protected admission record](reviews/KEYSTONE_SIX_PROTECTED_ADMISSION.md) documents the reviewed head, non-author approval, corrected six RESULT/1 reviews and verified browser/PDF preview. An editorial preview is not a formally certified or publication-accessible edition.

## Architecture and progress

- [Chapter dependency graph — 23 planned chapters](architecture/CHAPTER_DEPENDENCY_GRAPH.md)
- [Five recurring anchor problems](architecture/ANCHOR_PROBLEM_TRAJECTORIES.md)
- [Figure programme and pending acceptance](architecture/FIGURE_PROGRAMME.md)
- [Misconception ledger](architecture/MISCONCEPTION_LEDGER.md)

## Governance, sources, and reproducibility

- [Pedagogical charter](governance/PEDAGOGICAL_CHARTER.md)
- [Visual production specification](governance/VISUAL_PRODUCTION_SPEC.md)
- [Wolfram save-before-display protocol](governance/WOLFRAM_SAVE_BEFORE_DISPLAY.md)
- [Figure typography](governance/WOLFRAM_FIGURE_TYPOGRAPHY.md)
- [Primary-source ledger](reviews/KEYSTONE_PRIMARY_SOURCES_001.md)
- [Editorial acceptance tranche #8](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/8)

Six reproducible Wolfram SVG candidates are committed under `figures/src/` and `figures/generated/`. They must be saved, read back, and validated before any interactive display. **Figure and publication acceptance remain separate from manuscript admission.**

The six-chapter review renderer lives in `.github/workflows/cda-keystone-candidate.yml`; it builds MathJax HTML, browser screenshots and a review-only PDF without deploying GitHub Pages.

## Next editorial work

Complete C02–C03, C06–C09, C11–C14, C16–C19, and C21–C23, together with exercises, consistent mathematical notation, full-width figures, independent critical reviews and publication-accessible output.
