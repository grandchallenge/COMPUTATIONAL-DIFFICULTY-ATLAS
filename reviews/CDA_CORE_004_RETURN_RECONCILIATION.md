# CORE-004 mathematical editorial return reconciliation

**Authority status: corrected author candidate, NOT independent acceptance, figure certification, or public publication.**

This file maps four authenticated logical critical-role `RESULT/1` returns to a successor manuscript based on protected main. The original reviewers' frozen PR commits and Git blobs remain unchanged. The critical role was operated as authenticated `fyremael`, potentially shared with drafting, not four independent human logins. Non-author GitHub PR review and protected admission remain separate.

| Chapter | Original frozen PR/head | Original Git chapter blob | RESULT/1 issue and comment | Disposition |
|---|---|---|---|---|
| C06 | [#31](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/31) `c6c86aa100c27c5b02ab82587786e39cccc885d6` | `46f6f0da854a6d3a4b696c1ca5a0b5be2a076539` | [#35](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/35#issuecomment-6116522686) | REQUEST_CHANGES |
| C07 | [#32](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/32) `f75b70f8af4f659253dba03725d67af73c9930b1` | `afaa524d1813df49541d39ba78d0e52660ba5683` | [#36](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/36#issuecomment-6116523124) | APPROVE_WITH_CORRECTIONS |
| C08 | [#33](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/33) `3ae0f47f1027e1cef69f35f48b81e79abe4b2975` | `47d014d90999877a16f4822ea3e5830f1fe052a4` | [#37](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/37#issuecomment-6116523652) | REQUEST_CHANGES |
| C09 | [#34](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/34) `0313be68831af2fab312a53a9d64ad84e1bbac8c` | `7d2df4a96cd59608e470e7b8c428f5ec9ed16ed8` | [#38](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/38#issuecomment-6116524083) | REQUEST_CHANGES |

## Corrected mathematical contracts

**C06:** Source reduction from all binary 3SAT encodings now validates the source string and maps malformed strings to a fixed CLIQUE NO-instance. Valid empty conjunction and empty clause cases retain their independently correct fixed YES/NO images. Cook–Levin is cited as an imported theorem; the unsupported specific Levin bibliography is deliberately narrowed. Additional test tries malformed codes and fixed graph responses.

**C07:** Replaces ambiguous general comments about short tautology proofs by the Cook–Reckhow proposition: a polynomially bounded propositional proof system exists if and only if NP = coNP. Clarifies that particular restricted systems can have proven lower bounds, adds verified primary publication [Cook–Reckhow 1979](https://doi.org/10.2307/2273702).

**C08:** Adds primary evidence for the deterministic time-hierarchy theorem, Baker–Gill–Solovay relativization, Razborov–Rudich natural-proofs barrier and Aaronson–Wigderson algebrization, with explicitly conditional scopes. SAT witness recovery now specifies a well-formed encoded formula, malformed-string treatment, polynomial variable count and polynomial substitution/encoding cost. It does not claim SAT is in P.

**C09:** Replaces a purported three-block example that had only two blocks with a genuine ∃u∀x∃z strategy. Derives rather than assumes the restricted ∃X∀Y-CNF truth problem reduces to SAT: discard clauses tautological in the universally quantified Y variables, remove remaining Y-literals and solve CNF on X. Tests enumerate 85² two-clause signed-literal CNFs including empty clauses; class NP-completeness depends on the unrestricted-CNF representation. Adds Stockmeyer and Wrathall primary source records.

## Scope and remaining obligations

All original review issue fields and labels were read back as `RETURNED` after [protected CORE-004 activation run 38194667754](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/actions/runs/38194667754) and production return capture.

Green source tests/MathJax formatting are neither independent mathematical adjudication nor browser/full-width figure acceptance. The corrected successor must pass its **new exact-head** four-chapter CI, then an applicable non-author review, and protected merge/readback. Do not reuse the original PR approvals as approvals of this new head.

All C06–C09 proposed Wolfram diagrams remain *unproduced* and must be saved to committed source and exported complete SVG, XML-validated and remote-verified before any figure display. A final visual/a11y pass, tagged PDF and public MkDocs admission remain separate.
