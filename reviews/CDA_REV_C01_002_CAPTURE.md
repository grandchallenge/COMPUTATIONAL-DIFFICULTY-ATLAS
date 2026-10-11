# CDA-REV-C01-002 — returned C01 critical review capture

**Status:** RETURNED and captured; corrections proposed; **not adjudicated or accepted for publication.**

## Exact return evidence

- Assignment: `CDA-REV-C01-002`; issue [#9](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/9).
- Result comment ID: `6108010031`, [source RESULT/1](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/9#issuecomment-6108010031).
- Reviewed input head: `0deaa8be7f18ad4324f9d1af66dbf7c319c7d1d2`; reviewer role `INDEPENDENT_MATHEMATICAL_EDITORIAL_VERIFY`; result `REQUEST_CHANGES`.
- GitHub return projection run [38131556560](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/actions/runs/38131556560) **SUCCESS**; authoritative `GCL State=RETURNED`, `gcl-state:returned` present and AVAILABLE removed at readback.
- The logical review and drafting work used the same authenticated GitHub login `fyremael`. It therefore does not constitute distinct-human or independent-publishing review.

## Findings and proposed correction correspondence

| Finding | Exact original location | Author-side corrective action | Verified status |
|---|---|---|---|
| Five formulations but “four different answer types” | C01 §4, worked TSP example | Clarify all five formulations; figure F3.1 intentionally depicts four selected variants | Applied to PR #6 head `2e769e4d…` |
| Stale instruction to commission an already-existing figure | C01, “Notes for editorial review” | Remove internal editorial section from reader-facing chapter | Applied to PR #6 |
| Foundational reference missing for classical decision TSP | C01 §4 | Add Karp 1972 DOI with precise decision-language scope and forward reference | Applied to PR #6 |
| Final-width Wolfram F3.1 typography and accessibility | Figure caption and metadata | Preserve candidate status; require separate production acceptance | **Open** |

The four-city TSP numerical witness was independently enumerated through Wolfram: distinct undirected tour costs `{8,18,18}`, exactly one tour under threshold 9, none under threshold 7. That is evidence for the worked example, not proof of all C01 claims.

## New head and replay requirements

The correction candidate is [PR #6](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/6), head `2e769e4da18423f39d58f95b8fae55748492205e`. Its exact-head `c01-preview` and `direct-return-contract` checks passed after corrections.

**No editorial acceptance has been asserted.** The controller must explicitly adjudicate whether a focused review of corrections suffices or whether a new role-scoped review at the new head is required. F3.1 final-width review remains outstanding either way. No formal mathematical certification, published monograph, or PDF is authorized by this record.
