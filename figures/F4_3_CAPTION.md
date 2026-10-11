# F4.3 — A midpoint makes reachability recursive

**Status:** Wolfram-generated vector candidate; independent mathematical, accessibility and final-width editorial review pending.

**Caption.** The bounded-reachability predicate $R(u,v,j)$ asks whether a directed path of **at most** $2^j$ transitions connects configuration $u$ to configuration $v$. For $j>0$, the existence of such a path is equivalent to the existence of a midpoint configuration $m$ for which both $R(u,m,j-1)$ and $R(m,v,j-1)$ hold. The recurrence's base case $j=0$ handles a zero-step equality or one legal transition. Savitch's algorithm enumerates midpoint candidates using reusable work space, rather than retaining all possible paths. For space-constructible $s(n)\ge\log n$, this yields the classical $NSPACE(s(n))\subseteq DSPACE(s(n)^2)$ theorem. **The diagram is not a polynomial-time claim**; exhaustive recursive search can be very slow.

**Accessibility.** Three monochrome boxes represent the start configuration $u$, an enumerated midpoint $m$, and the target $v$. Two rightward arrows each represent a reachability subproblem bounded by $2^{j-1}$ steps. A lower label identifies the composed $2^j$ bound; a final note explains the conceptual work-space reuse.

**Primary reference:** Walter J. Savitch, *Relationships between nondeterministic and deterministic tape complexities* (1970), DOI https://doi.org/10.1016/S0022-0000(70)80006-X.

**Reproduce:** figures/src/F4_3_savitch_midpoint.wl; vector artifact figures/generated/F4_3_savitch_midpoint.svg.

**Acceptance:** Confirm the midpoint recurrence in both directions, absence of a false polynomial-time inference, final-width mathematics, and source reproduction. The figure does not certify or replace the chapter proof.
