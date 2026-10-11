# F2.1 — A reduction is an executable translation

**Status:** Wolfram-generated vector candidate; independent mathematical, accessibility, and final-width editorial review pending.

**Caption.** A polynomial-time many-one reduction (A\le_m^P B) computes one instance (f(x)) of the **target** problem (B) from an instance (x) of the **source** problem (A), preserving yes/no membership: (x\in A\iff f(x)\in B). Thus a decider for (B) can decide (A) after translation. If (B\in P), this shows (A\in P). An efficient algorithm for (A) **does not follow** to (B) from the arrow's direction. This diagram represents one fixed reduction and an abstract target solver; it makes no hardness/completeness claim about either depicted problem.

**Accessibility.** Four horizontal boxes depict problem A's input, a polynomial-time translator (f), target problem B's translated instance, and the B-decider. Three rightward arrows indicate dataflow. A bottom statement emphasizes that solving B enables a solution to A. Boxes and arrows are monochrome; no color perception is necessary.

**Vector/source paths.** `figures/generated/F2_1_translator_solver.svg`; `figures/src/F2_1_translator_solver.wl`.

**Acceptance criteria.** Verify correct arrow direction and logical implication, balanced typography at final width, no arrow-label collisions, grayscale contrast, and exact source–SVG reproducibility.
