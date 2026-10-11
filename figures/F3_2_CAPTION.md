# F3.2 — Certificates and deterministic verification

**Status:** Wolfram-generated vector candidate; independent mathematical, accessibility and final-width editorial review pending.

**Caption.** The decision problem supplies an encoded input $x$; an alleged **yes-witness** $w$ has length polynomial in $|x|$. A deterministic verifier $V(x,w)$ checks that one pair within polynomial time in the total input length. The language belongs to NP when $x\in L$ if and only if **some** bounded witness is accepted. Thus every yes-instance has at least one accepted witness, while **every** proposed witness must be rejected on a no-instance. The diagram does not assert that discovering $w$ is efficient, that no-instances have equally short certificates, or that $P\ne NP$.

**Accessibility.** Two arrows convey an input instance and a short witness into one deterministic verification box. A third arrow leads to an accept/reject result. Below, separate statements summarize the existential yes condition and universal rejection of witnesses on no-instances. The diagram is monochrome.

**Reproduce:** figures/src/F3_2_np_verifier.wl; vector artifact figures/generated/F3_2_np_verifier.svg.

**Acceptance:** Check witness length and verifier time bounds, soundness and completeness, legibility and noncolliding arrows at page width, and Wolfram source–SVG correspondence. Its review is separate from publication authorization.
