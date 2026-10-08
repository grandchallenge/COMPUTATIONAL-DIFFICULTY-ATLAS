# Chapter Dependency Graph

Status: architecture baseline v0.1

The chapter order is pedagogical rather than encyclopedic. Later material may cite earlier chapters only along the dependency edges below.

## Core spine

```text
C01 What is a computational problem?
  |
  v
C02 Algorithms, cost models, asymptotics
  |
  v
C03 Efficient computation and P
  |
  v
C04 Verification and NP
  |
  v
C05 Reductions: transporting difficulty
  |
  +----------------------+
  |                      |
  v                      v
C06 NP-completeness   C07 coNP and complements
  |                      |
  +----------+-----------+
             v
        C08 P versus NP
             |
             v
        C09 Quantifiers and PH
             |
             v
        C10 Space and PSPACE
             |
             v
        C11 QBF and games
             |
             v
        C12 Time beyond polynomial
```

## Orthogonal resource branches

These chapters depend on the core spine but introduce distinct computational resources.

```text
C05 reductions
  +--> C13 Counting: #P and PP
  +--> C14 Randomness: RP, coRP, ZPP, BPP
  +--> C15 Quantum computation: BQP, QMA
  +--> C16 Parallel complexity: NC and P-completeness
  +--> C17 Parameterized complexity: FPT and W-hierarchy
  +--> C18 Approximation and optimization
  +--> C19 Average-case and distributional complexity
```

Additional prerequisites:

- C15 requires C04 and C05; factoring is used as the primary bridge.
- C18 requires C06 and the decision/optimization distinction from C01.
- C19 requires C06 and the worst-case framing from C02.

## Computability branch

```text
C01 problem formalization
  |
  v
C20 Decidability and the halting problem
  |
  v
C21 Reductions beyond decidability
  |
  v
C22 Arithmetical hierarchy and degrees of unsolvability
```

This branch deliberately begins after the reader has already seen resource-bounded complexity, so the change from "expensive" to "not computable at all" is explicit.

## Synthesis

All branches converge on:

C23 — The Atlas

C23 contains separate maps for:
- containment,
- reductions,
- computational resources,
- proved separations,
- conjectured separations,
- practical solvability,
- decidability and undecidability.

No single diagram is permitted to collapse all of these relations into one vertical notion of "harder."

## Dependency invariant

A chapter may introduce a symbol early for orientation, but may not rely on a formal property before the chapter that establishes it.

The dependency graph is therefore also an editorial validation instrument: unexplained forward dependencies are defects.
