# Figure F15.1 — Classical and quantum unstructured-search query scaling

**Status:** Wolfram-generated and visually inspected vector candidate. Independent review and final-width acceptance pending.

**Caption.** Asymptotic oracle-query counts for unstructured search of an $N$-element domain: classical bounded-error randomized search requires $\Theta(N)$ queries, while Grover's quantum algorithm uses $\Theta(\sqrt N)$ queries in the standard black-box model with one marked item. The solid and dashed curves show representative growth laws, not empirical timings. The improvement is quadratic in $N$, not necessarily polynomial in the input length $\log_2 N$; for $N=2^n$, $\sqrt N=2^{n/2}$ is still exponential in $n$. Gate, memory, oracle-implementation, hardware and fault-tolerance costs are deliberately omitted.

**Accessibility:** Distinct line styles (solid and dashed), independently labeled in the legend. The image remains meaningful in grayscale.

**Reproduction:** `figures/src/F15_1_grover_query_scaling.wl`. Vector output `figures/generated/F15_1_grover_query_scaling.svg`. Verify final manuscript width and mathematical label rendering before acceptance.
