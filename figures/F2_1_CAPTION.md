# F2.1 — A reduction is an executable translation

**Status:** Wolfram-generated vector candidate; independent mathematical, accessibility and final-width review pending.

**Caption.** A polynomial-time many-one reduction $A\le_m^P B$ computes one instance $f(x)$ of the **target** problem $B$ from an instance $x$ of the **source** problem $A$, preserving yes/no membership: $x\in A\iff f(x)\in B$. Thus a decider for $B$ can decide $A$ after translation. If $B\in P$, this shows $A\in P$. An efficient algorithm for $A$ does **not** follow for $B$ from this arrow's direction. This diagram depicts one validly specified reduction and an abstract target solver; it does not establish hardness or completeness of either problem.

**Accessibility.** Four horizontal boxes depict an encoded A-instance, a polynomial-time translator $f$, the target B-instance $f(x)$, and a B-decider. Three rightward arrows indicate dataflow. A bottom statement emphasizes that a solver for B enables deciding A. Black arrows and white boxes remain distinguishable in grayscale.

**Vector/source paths.** \`figures/generated/F2_1_translator_solver.svg\`; \`figures/src/F2_1_translator_solver.wl\`.

**Acceptance criteria.** Verify arrow direction and the required biconditional, typography at final width, no label collisions, grayscale readability, and source–SVG reproduction.
