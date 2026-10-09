# CDA Direct Editorial Return Protocol

Status: operational queue projection contract.

A Computational Difficulty Atlas issue is a direct-editorial Worker Queue job only when it carries `gcl-pickup:direct-editorial` and its organization Issue Fields identify campaign `COMPUTATIONAL-DIFFICULTY-ATLAS`.

Workers do not use the MATHSOLVE `/claim` reservation controller for these jobs. They execute the bounded issue instructions and post the requested `RESULT/1` directly on the same issue using an authenticated GitHub identity.

## Return projection

The repository-local `CDA direct editorial returns` workflow listens for newly created issue comments beginning with `RESULT/1`.

Before changing operational state, the projector requires:

- an open non-PR issue;
- the `gcl-job` label;
- exactly the configured direct pickup label `gcl-pickup:direct-editorial`;
- exact state-label/field agreement at `AVAILABLE`;
- exactly one recognized role label agreeing with `GCL Role`;
- exactly one recognized collaboration label agreeing with `GCL Collaboration`;
- `GCL Campaign=COMPUTATIONAL-DIFFICULTY-ATLAS`;
- a bound issue-body `CAMPAIGN: COMPUTATIONAL-DIFFICULTY-ATLAS`;
- a bound issue-body `PICKUP_MODE: DIRECT_EDITORIAL_NO_CLAIM`;
- a bound `ASSIGNMENT_ID`, `ROLE`, and 40-hex `TARGET_HEAD` in the issue body;
- returned `assignment_id`, `reviewer_role`, `input_head`, and `disposition`;
- exact assignment, reviewer-role, and head agreement;
- disposition in `APPROVE`, `APPROVE_WITH_CORRECTIONS`, `REQUEST_CHANGES`, or `BLOCKED`.

A conforming return changes only operational receipt state:

- organization Issue Field `GCL State` → `RETURNED`;
- add `gcl-state:returned`;
- remove `gcl-state:available`.

The workflow reads both the Issue Field and lifecycle labels back after mutation and fails if RETURNED is not present or AVAILABLE remains.

## Authority boundary

`RETURNED` means only that issue-bound evidence was handed back. The projector does not adjudicate the review, accept corrections, merge a pull request, certify mathematics, authorize publication, or establish independent-review validity. Those decisions remain with the Atlas controller and repository governance.

Project #2's generic `Status` column is a board-only presentation field and may be reconciled separately by the GCL Worker Queue auditor. Worker discovery uses the authoritative `GCL State` Issue Field, so a successfully projected return immediately leaves the AVAILABLE view.

## Provenance consistency

Adjudicated review evidence is represented by a canonical repository receipt.
For CDA-REV-001 this is `reviews/CDA_REV_001_RECEIPT.json`. CI verifies that
the receipt, adjudication record, F1.1 metadata, and F1.1 caption all name the
same exact reviewed head, comment, assignment, and disposition. This prevents a
manually mistyped SHA from silently becoming the durable review authority.
