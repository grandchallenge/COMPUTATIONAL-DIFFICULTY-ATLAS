# Six-keystone protected manuscript admission

**Admission status:** PROTECTED MERGED. **Publication status:** NOT AUTHORIZED. **Whole-book status:** INCOMPLETE.

Six mathematical exposition chapters (C01, C04, C05, C10, C15, C20) entered protected main via [PR #22](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/22), merged at `b4183c841cf991f92ccc411a80849ec7eb646a29`. Its exact reviewed author head was `44f4cabb4b94ed2da6c17490f33f57aff481643f`. A non-author review by `jimsteeg`, review ID `5483270111`, approved exactly that head.

All six original issue-bound `RESULT/1` reviews (#9–#14) requested changes. The [review reconciliation ledger](KEYSTONE_SIX_RETURN_RECONCILIATION_002.md) maps substantive corrections to the successor. Original draft PRs #6/#7 were closed unmerged to preserve frozen inputs and prevent re-admission of stale content.

[Exact-head run 38137657658](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/actions/runs/38137657658) successfully replayed mathematical examples, verified six source-committed Wolfram vectors **before display**, built strict MkDocs, and used Chromium/MathJax to check desktop and mobile layouts and render a 24-page PDF. The PDF was an **unpublished review artifact**, not an accessible/tagged publication edition. Figure mathematical and accessibility acceptance remains separately pending.

The Atlas architecture defines **23 chapters**, of which only **six** are manuscript-admitted. Immediate remaining prerequisites for the pedagogical reading path are C02 (asymptotics/cost model) and C03 (polynomial time/P). Then proceed through C06–C09 and the other missing successor chapters. Do not mark the book or figures complete merely because the six-keystone integration is merged.

Operational note: hourly RESULT/1 replay initially failed due to Python import invocation; [PR #23](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS/pull/23) corrected and tested it. A rerun of the old workflow attempt reused the old workflow revision, so a fresh scheduled run is still needed to verify the deployed scheduler.
