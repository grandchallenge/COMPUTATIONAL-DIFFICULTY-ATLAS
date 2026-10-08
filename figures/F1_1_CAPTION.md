# F1.1 — First-order landscape of computational difficulty

Status: candidate source established; publication review pending  
Source: `figures/src/F1_1_first_order_landscape.wl`

## Pedagogical question

How can we show the first classical containment spine without teaching the false idea that computational difficulty is one vertical scale?

## Caption

**Figure F1.1 — A first-order containment map, not a total ordering of difficulty.**  
For decision problems over finite encodings, $P \subseteq NP \subseteq PSPACE \subsetneq \mathrm{DECIDABLE}$. The containments $P \subseteq NP$ and $NP \subseteq PSPACE$ are proved, but whether either is strict remains open. The strict inclusion $PSPACE \subsetneq \mathrm{DECIDABLE}$ follows because decidable languages exist that require more than polynomial space. The horizontal computability boundary separates problems for which some total algorithm exists from undecidable problems; it is not merely another step on a runtime scale. "NP-hard" is intentionally shown as a reduction-based warning rather than a horizontal region. Integer factorization is also intentionally not assigned an NP-completeness position: its precise classification depends on formulation and computational model, and it is not known to be NP-complete.

## Misconceptions addressed

M02, M03, M05, M09, M10, M15.

## Deliberate omissions

This first-order map does not yet display:
- $coNP$ or the polynomial hierarchy;
- $EXPTIME$ and larger resource-bounded classes;
- randomized, counting, interactive, parallel, parameterized, or quantum classes;
- search, function, optimization, or counting formulations;
- average-case or practical-solvability overlays.

Those are later map updates, not absent claims.

## Acceptance checklist

- [x] no vertical "harder problems" axis;
- [x] $P \subseteq NP$ and $NP \subseteq PSPACE$ shown with equality explicitly open;
- [x] $PSPACE \subsetneq \mathrm{DECIDABLE}$ marked as known strict;
- [x] undecidability shown as a computability boundary;
- [x] NP-hardness treated as a reduction property, not a class band;
- [x] factorization not mislabeled NP-complete;
- [x] Wolfram Language source is reproducible;
- [x] SVG/PDF export targets are defined;
- [ ] independent mathematical review;
- [ ] typography review at final page width;
- [ ] grayscale/print proof;
