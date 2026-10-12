# C02/C03 editorial return reconciliation 003

**Status:** Correction candidate following authenticated critical `RESULT/1` returns; **not yet independently accepted for admission**.

## Immutable review inputs

- Original manuscript: [PR #25](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/25), head `ce0087442a7c317cf65f38c3ab1cdf1944a4eac3`. Do not change this head while the review evidence is binding.
- C02, [issue #26 RESULT/1](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/26#issuecomment-6116000643), exact chapter blob `032d753274e05f9759b3cd2a6fdd9a110a9f3e6b`, `REQUEST_CHANGES`.
- C03, [issue #27 RESULT/1](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/27#issuecomment-6116001092), exact chapter blob `4c683e533f12c57cb2580fe94175b20c576facbe`, `REQUEST_CHANGES`.
- Protected review activation [run 38190906658](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/actions/runs/38190906658): SUCCESS and both issue fields/labels independently read back AVAILABLE before the reviews. Both returns then projected to RETURNED by the event-driven controller.

## Specific changes and remaining obligations

| Finding | Correction | Evidence/replay obligation |
|---|---|---|
| C02 defined worst-case time only on valid encodings | Now explicitly covers **all** binary strings of a given length for total deciders and distinguishes resource bounds over a promise set | Regression test for malformed input clause and source-MathJax replay |
| C02 encoding invariance underqualified | Now requires polynomial translators **both ways**, yes/no preservation and consistent domain validity | Mathematical check of each assumption |
| C02 omitted standard references | Arora–Barak and Cormen–Leiserson–Rivest–Stein added as teaching references | Confirm attribution and avoid false theorem claims |
| C03 pseudocode written as escaped literal Markdown fences | Replaced with genuine `\`\`\`text` code fence and a regression assertion | Check raw GitHub rendering and MkDocs code block |
| C03 BFS complexity lacked bit-cost qualification | Separated O(|V|+|E|) graph-search core from polynomial parsing on encoded input | Verify the soundness, completeness and complexity argument |
| C03 path-search interpretation ambiguous | Explained BFS predecessor reconstruction and retained P as a class of decision languages | Check no incorrect function-class attribution |
| C03 omitted source context | Added standard BFS/complexity references | Confirm exact references |

The critical pass independently compared BFS with a separate transitive-closure algorithm on all directed graphs up to four vertices including loops, covering **1,053,250 graph/source/target queries**, and found no discrepancy. That finite experiment is a falsification attempt, **not** a universal proof; the chapter's invariant and induction provide the proof.

**Authority:** The critical review used logical role separation under authenticated operator `fyremael`, not a distinct human identity. A separate non-author acceptance at the exact *corrected* successor head is still required by the manuscript merge track. A successful CI preview and the prior non-author approval of the **old** frozen head do not themselves approve this corrected head.

**Figures:** Neither missing C02 growth plot nor C03 BFS-frontier figure is silently represented as complete. They remain new deliverables subject to durable Wolfram source/export/remote-readback **before** display, final-width inspection, accessibility and separate mathematical acceptance.
