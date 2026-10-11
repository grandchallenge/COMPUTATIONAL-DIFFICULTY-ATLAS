# F6.2 — Diagonal contradiction for the universal halting decider

**Status:** Wolfram-generated vector candidate; independent mathematical, accessibility, and final-width editorial review pending.

**Caption.** Suppose a total algorithm (H(M,x)) correctly predicts whether every encoded program (M) halts on input (x). Define a new program (D) to do the opposite of that prediction when queried about its input: on a program description (y), loop forever if (H(y,y)=1), and halt if (H(y,y)=0). With (d) the code of (D), the two possible outputs of (H(d,d)) both disagree with the actual behavior of (D(d)). Therefore no unrestricted total halting decider (H) exists. The boxes depict a logical contradiction, **not** an algorithm that computes halting facts.

**Accessibility.** A vertical arrow leads from the hypothetical universal decider to its self-application on the constructed program. The diagram splits into two horizontal cases: prediction 1 on the left and prediction 0 on the right. Each case leads vertically to the opposite behavior and a contradiction. No color is required.

**Vector/source paths.** `figures/generated/F6_2_halting_diagonal.svg`; `figures/src/F6_2_halting_diagonal.wl`.

**Acceptance criteria.** Verify the reversal of predicted and actual outcomes in both branches; explicitly explain that (D) is defined to contradict (H), with no assumption of an executable actual decider. Inspect ordinary-width legibility, figure claims, and source–SVG correspondence.
