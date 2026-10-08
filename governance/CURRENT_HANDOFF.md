# Current Handoff

Transaction: `CDA-ARCH-V0.1-FOUNDATIONS-001`  
State: **WAITING_EXTERNAL_REVIEW**

The first architecture tranche for *A Mathematical Atlas of Computational Difficulty* is instantiated in PR #1 at candidate head:

`c75d3aeb6ed1ceb4eb57224f025347729aeb627b`

The candidate contains the pedagogical architecture, misconception controls, six keystone chapter specifications, and the revised Wolfram-produced F1.1 candidate with enlarged typography, explicit decision-problem formulations, and collision-free box geometry.

An internal hostile preflight is recorded at `reviews/PREFLIGHT_001.md`. It repaired formulation defects and hidden pedagogical dependencies but is author-side evidence only; it does **not** satisfy the independent review gate.

The current review artifact is `figures/generated/F1_1_first_order_landscape.png`, rendered by Wolfram from the canonical source. SVG/PDF remain publication export targets defined by the Wolfram source and require final production regeneration before release.

Independent review job **CDA-REV-001** is issue #2. It is published to GCL Worker Queue Project #2 with the direct-review discovery labels:

- `gcl-job`
- `gcl-state:available`
- `gcl-collab:cooperative`
- `gcl-role:verify`
- `gcl-pickup:direct-editorial`

The review must bind to the exact candidate head it inspected and return one `RESULT/1` comment on issue #2.

## Recovery rule

Do not merge PR #1 merely because it is mechanically mergeable.

On recovery:

1. inspect issue #2 for a conforming review return;
2. confirm the returned `input_head`;
3. compare it with the current PR #1 head;
4. adjudicate corrections;
5. rerender/re-review F1.1 if the reviewed content changes materially;
6. merge only after the review gate is satisfied;
7. verify accepted files on `main`;
8. update this controller state to completed.

There is no Human-Steward action required at this boundary. The outstanding dependency is worker review evidence.
