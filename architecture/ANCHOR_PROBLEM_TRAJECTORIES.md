# Anchor Problem Trajectories

Status: architecture baseline v0.1

Five recurring problems provide continuity across the monograph. They are not merely examples; each is a pedagogical instrument used to expose a different dimension of computational difficulty.

## A1 — Directed s-t Reachability

**Primary lesson:** resource classification can be much finer than "in P."

Trajectory:
- C01: decision-problem formulation.
- C02: graph size and input encoding.
- C03: polynomial-time solvability.
- C10: NL as a sharper classification; relation to deterministic space.
- C16: parallel-complexity perspective where useful.
- C23: appears on containment and resource maps.

Misconception prevented: "all problems in P are computationally alike."

## A2 — Boolean Satisfiability (SAT)

**Primary lesson:** efficient verification, reductions, and completeness.

Trajectory:
- C04: certificate/witness model.
- C05: first major reduction target.
- C06: Cook-Levin and NP-completeness.
- C08: central P versus NP consequences.
- C13: #SAT as the counting upgrade.
- C14/C19: randomized, heuristic, and distribution-sensitive behavior where appropriate.
- C23: appears on containment, reduction, and practical-solvability maps.

Misconception prevented: "NP-complete means unusable in practice."

## A3 — Traveling Salesperson Problem (TSP)

**Primary lesson:** decision, optimization, approximation, and practical performance are distinct.

Trajectory:
- C01: separate decision and optimization formulations.
- C06: NP-complete decision version.
- C18: approximation behavior and metric restrictions.
- C19: instance structure and practical heuristics.
- C23: used to contrast theoretical and engineering maps.

Misconception prevented: "a problem has one complexity label independent of formulation."

## A4 — Integer Factorization

**Primary lesson:** "not known in P" does not imply NP-complete; computational model matters.

Trajectory:
- C03/C04: distinguish the factorization function/search task from associated decision formulations; discuss efficient verification without implying NP-completeness.
- C07: use an explicitly stated decision formulation when discussing NP/coNP-style certificate structure.
- C08: example of a famous problem not known NP-complete.
- C15: Shor's algorithm and BQP.
- C23: contrast between classical and quantum resource maps.

Misconception prevented: "factorization is NP-complete" and "quantum computers efficiently solve arbitrary NP-complete problems."

## A5 — Halting Problem

**Primary lesson:** undecidability is qualitatively different from high resource cost.

Trajectory:
- C01: problem/language framing.
- C20: diagonalization and undecidability.
- C21: mapping reductions among undecidable problems; Rice's theorem.
- C22: placement in broader computability hierarchies.
- C23: separate decidability map.

Misconception prevented: "undecidable means just extremely slow."

## Anchor-use rule

Every reappearance must add a new conceptual layer. Repetition without conceptual progression is discouraged.

Where an anchor problem has multiple formulations, the formulation must be stated explicitly every time.
