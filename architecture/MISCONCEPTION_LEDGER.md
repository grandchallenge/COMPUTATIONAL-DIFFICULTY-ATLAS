# Misconception Ledger

Status: active editorial control artifact

Each misconception is a defect class the monograph is required to prevent or explicitly repair.

| ID | Misconception | Corrective target | Primary chapter |
|---|---|---|---|
| M01 | NP means "non-polynomial." | NP is defined via nondeterministic polynomial time / polynomially checkable certificates. | C04 |
| M02 | NP-hard means "outside NP." | Hardness is reduction-relative; NP-hard problems may be inside NP, outside NP, or undecidable. | C05-C06 |
| M03 | NP-hard problems form a horizontal band above NP. | Hardness is relational, not a geometric height. | C05 |
| M04 | NP-complete problems cannot be solved efficiently on useful instances. | Worst-case complexity does not determine every practical instance. | C06, C19 |
| M05 | Factoring is NP-complete. | No such result is known; associated formulations have substantially different status. | C08, C15 |
| M06 | Quantum computers efficiently solve NP-complete problems in general. | BQP is not known to contain NP-complete problems; Shor targets factoring/discrete log structure. | C15 |
| M07 | P means easy in practice. | Polynomial asymptotics are a robustness notion, not a runtime guarantee. | C03 |
| M08 | Exponential means impossible for every instance size. | Complexity is asymptotic and worst-case unless otherwise stated. | C02 |
| M09 | Undecidable means extremely expensive. | No total algorithm exists for all instances. | C20 |
| M10 | If A is contained in B, every problem in B is harder than every problem in A. | Class containment is set inclusion, not total ordering of individual problems. | C03-C05 |
| M11 | A reduction A -> B proves A is harder than B. | It shows B is at least as hard as A under the specified reduction notion. | C05 |
| M12 | Chess and Go each have one unqualified complexity classification. | Classification depends on generalized formulation and rule set. | C11-C12 |
| M13 | Decision, search, optimization, and counting formulations are interchangeable. | Their relations require proof and may change complexity. | C01, C13, C18 |
| M14 | Worst-case complexity directly predicts ordinary runtime. | Instance distributions, structure, algorithms, and parameters matter. | C19 |
| M15 | Complexity classes are totally ordered. | The landscape is partially ordered and contains unresolved relationships. | C23 |
| M16 | NP is the class of problems whose answers are easy to check in every informal sense. | The certificate relation, encoding, and polynomial bound must be formalized. | C04 |
| M17 | A polynomial reduction preserves practical difficulty. | Reductions preserve a formal asymptotic relation, not constant factors or engineering behavior. | C05 |
| M18 | A complete problem is the "hardest single problem" in an absolute sense. | Completeness is relative to a class and reduction type. | C06 |
| M19 | More memory always implies more time, or vice versa. | Time and space are separate resources with nontrivial tradeoffs. | C10 |
| M20 | Randomization or quantum computation merely speeds up the same deterministic algorithm. | They change the computational model and admissible operations/resources. | C14-C15 |

## Editorial rule

Every chapter specification must name the misconception IDs it is responsible for preventing.

A chapter cannot be marked pedagogically complete while its assigned misconceptions remain plausibly inferable from the chapter's figures or prose.
