# Current Handoff

Transaction: `CDA-ARCH-V0.1-FOUNDATIONS-001`  
State: **COMPLETED**

The first architecture tranche for *A Mathematical Atlas of Computational Difficulty* is accepted on `main` at:

`322fd653b551ccc93df8fc4339b463d82b9c69a4`

PR #1 merged the pedagogical architecture, six keystone specifications, misconception and claim-status controls, the Wolfram F1.1 candidate, and the adjudicated CDA-REV-001 corrections.

## Review closure

CDA-REV-001 returned on issue #2 against exact head:

`c75d3aeb6ed1ceb4eb57224f025347729aeb627b`

Disposition: **APPROVE_WITH_CORRECTIONS**.

The corrections were admitted and recorded in `reviews/CDA_REV_001_ADJUDICATION.md`. They were limited to the reviewer's requested C15 dependency clarification and review-evidence bookkeeping; no reviewed mathematical claim or Wolfram figure source changed. Issue #2 is operationally closed with `GCL State=CLOSED`.

Post-closure validation found that two durable records had manually mistyped the reviewed SHA even though the issue return and F1.1 caption carried the correct value. PR #4 merged at `cc509d4ab5b8d834f61ed44f012743fa53272bd7`; it corrects those records and adds a canonical review receipt plus CI cross-check so this class of provenance drift fails closed.

## Worker Queue closure

The queue defect that delayed this review has been repaired systemically:

- MATHSOLVE PR #1017 is merged and the canonical worker bootstrap is now pickup-mode aware.
- Project #2 has explicit reservation-controlled versus direct-editorial semantics.
- MATHSOLVE controller transitions reproject immutable job metadata.
- The full cross-repository queue audit is fail-closed and reconciles Project Status with exact bound IDs.
- CDA PR #3 is merged at `aaa4e2b9e19641fbbb14e35f6489c92a65256c38`; future exact-head direct-review `RESULT/1` returns are projected locally to RETURNED without relying on the MATHSOLVE reservation controller.

The returned review itself exercised the repaired path end to end.

## Remaining figure release checks

F1.1 is independently reviewed as a candidate. Publication still requires:

1. regeneration of SVG/PDF from the canonical Wolfram source;
2. typography inspection at final manuscript placement;
3. grayscale/print proof.

These are release checks, not blockers on the accepted architecture.

## Recovery rule

This transaction is closed. Do not reconstruct or reopen it from chat.

The next transaction, when opened, should continue chapter specifications and composition from main commit `322fd653b551ccc93df8fc4339b463d82b9c69a4`.
