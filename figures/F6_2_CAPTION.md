# F6.2 — Diagonal contradiction for the universal halting decider

**Status:** Wolfram-generated vector candidate; independent mathematical, accessibility and final-width review pending.

**Caption.** Suppose a total algorithm $H(M,x)$ correctly predicts whether every encoded program $M$ halts on input $x$. Construct a program $D$ whose behavior deliberately contradicts that prediction when asked about its own input: on a program description $y$, loop forever if $H(y,y)=1$, and halt if $H(y,y)=0$. If $d$ is the code of $D$, the two possible outputs of $H(d,d)$ both disagree with the actual behavior of $D(d)$. Therefore no unrestricted total halting decider $H$ exists. The boxes depict a **logical contradiction**, not an algorithm that computes halting facts.

**Accessibility.** One vertical arrow leads from the hypothetical decider to its self-application on the constructed program. The diagram splits into two cases: prediction 1 on the left and prediction 0 on the right. Each leads to the opposite actual behavior and a contradiction. No information is conveyed by color.

**Vector/source paths.** \`figures/generated/F6_2_halting_diagonal.svg\`; \`figures/src/F6_2_halting_diagonal.wl\`.

**Acceptance criteria.** Verify reversal of predicted and actual outcomes in both branches and explain the definition of $D$ explicitly. Inspect mathematical labeling, ordinary-width readability, source reproducibility and screen-reader alternatives.
