# Six-keystone review reconciliation — tranche 002

**Disposition:** All six original independent-*logical-role* critical reviews have returned. This ledger maps their findings to the successor six-chapter manuscript candidate; it does not convert their returns into approvals.

**Original frozen source heads:** C01 PR #6 at `0deaa8be7f18ad4324f9d1af66dbf7c319c7d1d2`; C04/C05/C10/C15/C20 PR #7 at `8374afeff72a01010b28e739a34bc3408a0003b1`.

| Chapter | Return issue / RESULT/1 comment | Original disposition | Applied correction in successor PR #22 |
|---|---|---|---|
| C01 | [#9](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/9#issuecomment-6108010031) | REQUEST_CHANGES | Five versus four formulations clarified; misleading internal commission note removed; Karp 1972 DOI |
| C04 | [#10](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/10#issuecomment-6108604232) | REQUEST_CHANGES | F3.2 linked with status/scope; Cook reference; no asserted strict P/NP separation |
| C05 | [#11](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/11#issuecomment-6108604592) | REQUEST_CHANGES | F2.1 embedded; separate missing figure variants disclosed; Cook/Karp primary citations |
| C10 | [#12](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/12#issuecomment-6108604896) | REQUEST_CHANGES | Exact N-increment counter corrected (not N−1); configuration count changed to K; F4.3 and Savitch DOI |
| C15 | [#13](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/13#issuecomment-6108605198) | REQUEST_CHANGES | Uniform circuit generator outputs polynomial-size description, not exactly n bits; foundational quantum sources; F15.1 appropriately scoped |
| C20 | [#14](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/issues/14#issuecomment-6108605500) | REQUEST_CHANGES | Effective pair-encoding clarified; terminating-subclass promise specified; F6.2 and Turing reference |

**Review identity:** critical role performed under authenticated operator `fyremael`, which may overlap with drafting. Do not misdescribe as six independent humans; this is logical-role separation for routine editorial mathematical checking, not formal certification or publication approval.

**Evidence:** The six issue fields and lifecycle labels were read back as `RETURNED` after production controller capture. All review input commits are immutable. The corrected source is deliberately on a new branch based on protected `main`, with original PR #6/#7 preserved as review evidence.

**Still required:** CI and strict MkDocs replay at the exact corrected PR #22 head; independent non-author approval according to protected branch policy; explicit acceptance/adjudication for the six findings; final-width figure typography and accessibility; publication workflow and PDF checks. No `ACCEPTED` or `CERTIFIED` decision is asserted here.

**Durability:** Wolfram source, SVG, caption and metadata must already be full Git blobs before any preview. See protected `governance/WOLFRAM_SAVE_BEFORE_DISPLAY.md`. A 14-day GitHub Action artifact is an inspection convenience, never source of truth.
