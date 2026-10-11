# Figure F3.1 — One setting, several computational problems

**Status:** Wolfram-rendered vector candidate. Editorial and final-width typography acceptance pending.

**Caption.** The traveling-salesperson setting induces distinct computational tasks. The **decision** question asks whether a tour of cost at most \(B\) exists; **search** requests one such tour; **optimization** requests a minimum-cost tour; and **counting** requests the number of tours meeting the bound. Each variant has its own output contract. The graphic does not assert equality of running times, membership in a particular complexity class, or an equivalence of their hardness notions. The budget is supplied only where it is needed.

**Accessibility:** Four directed arrows fan out from the same weighted-graph setting to four labeled tasks. Arrow meanings are "formulate as"; their presence is not a computational reduction claim. No color distinction is required.

**Reproduce:** `figures/src/F3_1_tsp_formulation_fork.wl`. Vector output `figures/generated/F3_1_tsp_formulation_fork.svg`. Verify page-width legibility and source/output match before acceptance.
