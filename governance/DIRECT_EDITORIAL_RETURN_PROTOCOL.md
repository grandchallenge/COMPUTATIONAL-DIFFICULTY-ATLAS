# CDA Direct Editorial Return Protocol

Status: operational queue projection contract.

A Computational Difficulty Atlas issue is a direct-editorial Worker Queue job only when it carries `gcl-pickup:direct-editorial` and its organization Issue Fields identify campaign `COMPUTATIONAL-DIFFICULTY-ATLAS`.

Workers do not use the MATHSOLVE `/claim` reservation controller for these jobs. They execute the bounded issue instructions and post the requested `RESULT/1` directly on the same issue using an authenticated GitHub identity.

## Return projection

The repository-local `CDA direct editorial returns` workflow listens for newly created issue comments beginning with `RESULT/1`.

Before changing operational state, the projector requires:

- an open non-PR issue;
- `gcl-pickup:direct-editorial`;
- `GCL Campaign=COMPUTATIONAL-DIFFICULTY-ATLAS`;
- `GCL State=AVAILABLE`;
- a bound `ASSIGNMENT_ID` in the issue body;
- a bound 40-hex `TARGET_HEAD` in the issue body;
- returned `assignment_id`, `reviewer_role`, `input_head`, and `disposition`;
- exact assignment and head agreement;
- disposition in `APPROVE`, `APPROVE_WITH_CORRECTIONS`, `REQUEST_CHANGES`, or `BLOCKED`.

A conforming return changes only operational receipt state:

- organization Issue Field `GCL State` → `RETURNED`;
- add `gcl-state:returned`;
- remove `gcl-state:available`.

The workflow reads the Issue Field back after mutation.

## Authority boundary

`RETURNED` means only that issue-bound evidence was handed back. The projector does not adjudicate the review, accept corrections, merge a pull request, certify mathematics, authorize publication, or establish independent-review validity. Those decisions remain with the Atlas controller and repository governance.

Project #2's generic `Status` column is a board-only presentation field and may be reconciled separately by the GCL Worker Queue auditor. Worker discovery uses the authoritative `GCL State` Issue Field, so a successfully projected return immediately leaves the AVAILABLE view.
