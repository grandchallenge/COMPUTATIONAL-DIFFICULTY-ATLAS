# PREFLIGHT-001 — Architecture and F1.1 internal audit

Status: completed internal preflight; **does not satisfy independent review gate**
Input head: `238d69297afc462f118653a991da6b1bec397d40`

## Purpose

Run a hostile internal pass before asking an independent reviewer to spend attention on avoidable defects.

## Corrections made

1. **F1.1 NP shorthand strengthened.**
   Replaced the under-specified "polynomial-time verifier" label with an explicit polynomial-size witness plus polynomial-time verifier formulation.

2. **Decision/search formulation repaired.**
   Changed the P anchor from generic "shortest paths" to "shortest-path decision" because F1.1 is explicitly a decision-problem containment map.

3. **Computability language tightened.**
   Replaced "total algorithm" / "no total algorithm" with "total decider exists" / "no total decider" in the figure and C20-facing doctrine.

4. **Factorization trajectory tightened.**
   The architecture now distinguishes the factorization function/search task from associated decision formulations before discussing NP/coNP-style certificate structure.

5. **Quantum formulation tightened.**
   C15 now explicitly calls integer factorization and discrete logarithm function problems when discussing Shor-type polynomial-time quantum algorithms.

6. **Hidden pedagogical dependency exposed.**
   C20's computability branch now records C03 and C04 as pedagogical prerequisites in addition to C01, because its intended contrast with resource-bounded decidable problems otherwise imported earlier concepts silently.

7. **F1.1 geometry reflowed.**
   Enlarged the nominal figure to 800 pt, deliberately wrapped the NP descriptor, split the longest P anchor example over two lines, and rechecked the rendering for box-boundary collisions.

## Render status

A fresh Wolfram-rendered PNG review preview is committed. The Wolfram source remains canonical and defines SVG/PDF publication exports. The publication vector artifacts must be regenerated and checked in the final production toolchain before release.

## Residual gate

Independent review on issue #2 remains required. This preflight is author-side evidence only and grants no acceptance, merge, certification, or publication authority.
