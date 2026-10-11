# Keystone chapters — primary-source and claim-scope ledger (SOURCE-001)

**Status:** Author-side bibliographic reconnaissance; not a mathematical review, certified claim record, or publication citation audit.  
**Scope:** Manuscript candidates C01, C04, C05, C10, C15 and C20.  
**Evidence snapshot:** PR #6 at `0deaa8be7f18ad4324f9d1af66dbf7c319c7d1d2`, PR #7 at `8374afeff72a01010b28e739a34bc3408a0003b1`.  
**Source-check date:** 2026-10-11. Publication metadata and abstracts checked against journal/proceedings landing records, not every primary proof independently replayed.

## 1. Source records

| Key | Primary work | Stable publisher identifier | Chapters | Verified relevance |
|---|---|---|---|---|
| TURING-1936-37 | A. M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*, *Proceedings of the London Mathematical Society* s2-42(1), 230–265 (published 1937; received 1936). | [10.1112/plms/s2-42.1.230](https://doi.org/10.1112/plms/s2-42.1.230) | C20 | Computability, universal simulation and the classical undecidability boundary; modern HALT diagonalization is a pedagogical formulation and should not be quoted verbatim as if printed in this form in Turing's paper. |
| SAVITCH-1970 | W. J. Savitch, *Relationships between nondeterministic and deterministic tape complexities*, *J. Comput. Syst. Sci.* **4**(2), 177–192 (1970). | [10.1016/S0022-0000(70)80006-X](https://doi.org/10.1016/S0022-0000(70)80006-X) | C10 | Nondeterministic tape-space can be simulated deterministically with quadratic space when the bound is at least logarithmic. State hypotheses explicitly. |
| COOK-1971 | S. A. Cook, *The complexity of theorem-proving procedures*, *STOC* (1971), 151–158. | [10.1145/800157.805047](https://doi.org/10.1145/800157.805047) | C04, C05, successor C06 | Origin of NP-completeness framework. **Historical-form caveat:** original published abstract emphasizes tautology and oracle-based reduction. A modern SAT many-one-completeness statement is a standard equivalent presentation that needs its own precise argument or explanatory citation, not a fabricated literal quotation from the 1971 paper. |
| KARP-1972 | R. M. Karp, *Reducibility among Combinatorial Problems*, in *Complexity of Computer Computations* (1972), 85–103. | [10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9) | C05, successor C06 | Polynomial reducibility/combinatorial NP-completeness; distinction between many-one and Turing reductions must be maintained. |
| BERNSTEIN-VAZIRANI-1997 | E. Bernstein and U. Vazirani, *Quantum Complexity Theory*, *SIAM J. Comput.* **26**(5), 1411–1473 (1997). | [10.1137/S0097539796300921](https://doi.org/10.1137/S0097539796300921) | C15 | Quantum computational complexity model, efficient universal quantum computation and bounded-error resource notions; do not conflate machine definitions with physically measured hardware performance. |
| SHOR-1997 | P. W. Shor, *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer*, *SIAM J. Comput.* **26**(5), 1484–1509 (1997). | [10.1137/S0097539795293172](https://doi.org/10.1137/S0097539795293172) | C15 | Randomized polynomial-time quantum methods for integer factoring and discrete logarithms. **No unconditional superpolynomial classical lower bound is supplied.** |
| GROVER-1996 | L. K. Grover, *A fast quantum mechanical algorithm for database search*, *STOC* (1996), 212–219. | [10.1145/237814.237866](https://doi.org/10.1145/237814.237866); [author preprint](https://arxiv.org/abs/quant-ph/9605043) | C15 / F15.1 | Quantum upper bound on unstructured search of an \(N\)-item domain, scaling as \(O(\sqrt N)\) oracle queries. F15.1 is **an idealized query-scale plot**, not a hardware benchmark. |
| BBBV-1997 | C. H. Bennett, E. Bernstein, G. Brassard, U. Vazirani, *Strengths and Weaknesses of Quantum Computing*, *SIAM J. Comput.* **26**(5), 1510–1523 (1997). | [10.1137/S0097539796300933](https://doi.org/10.1137/S0097539796300933) | C15 / F15.1 | Oracle-relative query lower-bound context and limits on deductions about NP-versus-quantum polynomial time. **Oracle separations do not settle unrelativized NP versus BQP.** |

## 2. Claims to test during chapter review

| Chapter | Claim/proof obligation | Relevant source | Remaining verification |
|---|---|---|---|
| C01 | Precisely distinguish decision, witness search, optimization, function and counting; explicitly define encodings/bit length; do not label the entire topic TSP “NP-complete.” | Internal definitions and worked exact TSP example | A scholarly textbook/source for presentation conventions, independent figure caption and semantics audit. No claim of originating a theorem. |
| C04 | The verifier definition of NP uses polynomial witness **and** polynomial deterministic checking; \(P\subseteq NP\) is known, strictness open. | COOK-1971 and standard definitions | Verify existential direction/soundness and all SAT examples. Cite the precise modern definition rather than attributing every symbol to the original notation. |
| C05 | \(A\le_m^P B\) points towards the target solver; polynomial output-size bound; composition; NP-hard versus NP-complete. | COOK-1971, KARP-1972 | Document reduction variant for each claim; verify elementary reachability reduction. |
| C10 | \(NSPACE(s)\subseteq DSPACE(s^2)\), with \(s(n)\ge\log n\) and standard hypotheses, implies \(NPSPACE=PSPACE\). | SAVITCH-1970 | Check recurrence base case, midpoint path bound, enumerability/configuration assumptions, and proof-scope caveats. |
| C15 | \(P\subseteq BQP\), factoring quantum upper bound, \(O(\sqrt N)\) Grover query advantage, and no general NP-complete quantum polynomial algorithm established. | BERNSTEIN-VAZIRANI-1997, SHOR-1997, GROVER-1996, BBBV-1997 | Verify uniform quantum model, bounded-error amplification, resource-axis consistency and any displayed figure's labels. |
| C20 | HALT recognizable but undecidable; decidable iff both language and complement recognizable; SAT decidable by exhaustive assignments. | TURING-1936-37 plus elementary explicit proofs in manuscript | Check modern diagonal proof self-encoding conventions, input validity and totality. |

## 3. Source and epistemic cautions

- **Bibliographic verification is not proof validation.** A publisher record confirms source identity, topic, and metadata; it does not discharge every step of the theorem or guarantee the present exposition is correct.
- **Do not substitute oracle-relative lower bounds for unconditional separations.** In particular, BBBV-1997 cannot settle whether \(NP\subseteq BQP\) in the ordinary unrelativized setting.
- **Do not mistake the absence of a known fast factoring algorithm for a proved classical lower bound.** Shor's result is a quantum upper bound.
- **Do not overstate the provenance of standard modern textbook reductions.** Exact historical statements in Cook-1971 and Karp-1972 may differ from today's tutorial formulations.
- **Do not change the pinned review targets silently.** This ledger is independent of the frozen PR #6/#7 heads, to keep the six staged RESULT/1 assignments valid.
- These source records can be integrated as chapter-end bibliographical notes only after the corresponding critical review and protected admission transaction.

## 4. Proposed chapter-end reading design

Use one or two foundational sources per major idea, followed by a short **What this paper actually establishes** note and a **What remains open** note. The bibliographical layer must illuminate rather than distract from the pedagogical progression, and every citation should have a durable DOI or stable proceedings record.

**Handoff:** Parent acceptance issue #8; review packets #9–#14. Source provenance checked against DOI publisher records. This document is candidate supporting evidence, not the final acceptance receipt.
