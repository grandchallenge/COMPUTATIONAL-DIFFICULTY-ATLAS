# F1.1 — First-order landscape of computational difficulty

Status: candidate source revised for readability; publication review pending
Source: `figures/src/F1_1_first_order_landscape.wl`

## Pedagogical question

How can we show the first classical containment spine without teaching the false idea that computational difficulty is one vertical scale?

## Caption

**Figure F1.1 — A first-order containment map, not a total ordering of difficulty.**
For decision problems over finite encodings, $P \subseteq NP \subseteq PSPACE \subsetneq \mathrm{DECIDABLE}$. The containments $P \subseteq NP$ and $NP \subseteq PSPACE$ are proved, but whether either is strict remains open. The strict inclusion $PSPACE \subsetneq \mathrm{DECIDABLE}$ follows because decidable languages exist that require more than polynomial space. The horizontal computability boundary separates decision problems for which a total decider exists from undecidable problems; it is not merely another step on a runtime scale. "NP-hard" is intentionally shown as a reduction-based warning rather than a horizontal region. Integer factorization is also intentionally not assigned an NP-completeness position: its precise classification depends on formulation and computational model, and it is not known to be NP-complete.

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

## Readability revision

The revised candidate uses an 800 pt nominal vector width with deliberately enlarged typography:
- principal labels: 20–26 pt;
- explanatory text: 15–18 pt;
- relation/status labels: 16 pt;
- sidebar text: 15–19 pt.

Long in-box prose was shortened or deliberately wrapped rather than shrunk. Relation labels now occupy clear whitespace with no connector stroke behind them. All boxed text has visible interior clearance and no label crosses or touches a boundary.

## Acceptance checklist

- [x] no vertical "harder problems" axis;
- [x] $P \subseteq NP$ and $NP \subseteq PSPACE$ shown with equality explicitly open;
- [x] $PSPACE \subsetneq \mathrm{DECIDABLE}$ marked as known strict;
- [x] undecidability shown as a computability boundary;
- [x] NP-hardness treated as a reduction property, not a class band;
- [x] factorization not mislabeled NP-complete;
- [x] Wolfram Language source is reproducible;
- [x] SVG/PDF export targets are defined in the Wolfram source;
- [x] Wolfram-rendered PNG review preview is current;
- [ ] SVG/PDF publication exports regenerated and checked in the final production toolchain;
- [x] essential text enlarged for page-width reading;
- [x] no text crosses or touches box boundaries;
- [x] no structural line runs through a relation label;
- [ ] independent mathematical review;
- [ ] typography review at final manuscript placement;
- [ ] grayscale/print proof;
