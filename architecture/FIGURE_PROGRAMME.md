# Figure Programme

Status: architecture baseline v0.1  
Governed by: `governance/VISUAL_PRODUCTION_SPEC.md`

The figure programme is designed around conceptual transitions, not decoration.

## Figure families

### F1 — Progressive landscape maps

Purpose: build the reader's global model gradually.

- F1.1 First-order landscape: P, NP, PSPACE, decidable, undecidable.
- F1.2 Membership versus hardness: remove the false "NP-hard band."
- F1.3 Resource axes: time, space, randomness, interaction, quantum.
- F1.4 Known versus conjectured class relations.
- F1.5 Practical-solvability overlay.
- F1.6 Final multi-map atlas.

Default production: Wolfram for computed layout; alternate vector composition if it yields clearer semantics.

### F2 — Reduction mechanics

Purpose: make reductions operational rather than mystical.

- F2.1 "Translator + solver" reduction schematic.
- F2.2 Direction-of-hardness diagram.
- F2.3 Reduction composition.
- F2.4 Same problem under different reduction notions.

Default production: TikZ or equivalent exact vector diagram if clearer than Wolfram.

### F3 — Anchor problem trajectories

One visual sequence per anchor:
- reachability,
- SAT,
- TSP,
- factorization,
- halting.

Each sequence shows how the same example acquires new meaning as the reader advances.

Default production: Wolfram where layouts are data-driven; otherwise exact vector composition.

### F4 — Quantifier and game views

- SAT versus QBF quantifier structure.
- Alternating-choice game tree.
- PSPACE intuition through reusable memory rather than exhaustive storage.

Wolfram priority for trees and state-space graphics.

### F5 — Resource tradeoff plots

- asymptotic growth comparisons;
- time-space intuition;
- parameterized-complexity surfaces;
- approximation tradeoffs;
- randomized amplification;
- Grover/Shor conceptual resource comparisons.

Wolfram priority.

### F6 — Computability boundary

- finite-resource hierarchy versus computability boundary;
- diagonalization schematic;
- recognizability/decidability relationships;
- arithmetical hierarchy introduction.

Use the simplest exact medium that preserves the conceptual distinction.

## Figure acceptance metadata

Each production figure should record:

- figure ID;
- chapter;
- pedagogical question;
- misconception IDs addressed;
- source path;
- generation command/notebook;
- output artifact path;
- caption;
- theorem/claim dependencies;
- status: sketch / candidate / reviewed / publication-ready.

## Immediate production target

The first publication-grade figure to build is **F1.1**, replacing the exploratory generated image that initiated the project.

Acceptance criteria:
1. no false total ordering by "hardness";
2. explicit proved/unknown status where relevant;
3. correct placement of factoring and NP-hardness caveat;
4. no unqualified chess/Go classification;
5. vector-quality output;
6. exact mathematical typography;
7. readable at ordinary page width;
8. caption states the limits of the map.
