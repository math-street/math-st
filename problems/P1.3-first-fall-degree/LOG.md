# Log

## Session 1 — 2026-06-23

**Goal:** Complete SG-01: fix the four degree conventions, verify a separating
toy example, and establish an observable route to intermediate degrees.

**Prediction (written before running anything):** The four notions will require
explicit choices of quotient ring, homogenization, monomial order, and
algorithm. A hand-built exact Macaulay computation should expose first degree
falls and the Macaulay solving degree for tiny systems, while an instrumented
Buchberger implementation should demonstrate that an algorithm's traced
maximum degree is a separate implementation statistic.

**Positive result criterion:** Exact row-space or Gröbner-basis calculations
reproduce every number in the toy example and a smoke test finishes in under
10 seconds.

**Negative result criterion:** No toy system can be validated with the locally
available exact-arithmetic tools, or the proposed definitions cannot be made
compatible with the primary sources without leaving an unresolved ambiguity.

**Did:**
- Fixed the first fall, Hilbert-function regularity, solving-degree, and concrete algorithm-trace conventions in `NOTES.md`.
- Checked four primary sources and added per-paper notes plus global bibliography entries.
- Implemented `code/measure_toy_degrees.py` with exact finite-field row reduction, closed Macaulay spaces, a toy first-fall check, monomial regularity, and a traceable Buchberger run.
- Ran `env/check_env.py`, the 13 shared-library tests, the 2 P1.3 tests, and bytecode compilation.

**Found:**
- [PROVED] For the worked system over $\mathbb F_5$, $d_{\mathrm{ff}}=3$, $\operatorname{sd}_{\mathrm{grevlex}}=4$, $d_{\mathrm{reg}}=8$, and the specified naïve Buchberger trace reaches degree 9.
- [PROVED] The problem prompt's parenthetical identification of degree of regularity with solving degree is false without extra hypotheses; the worked system separates them by 4.
- [EMPIRICAL: q=5, one deterministic system] The script reproduces $3,4,8,9$, SymPy 1.14.0 returns the expected Gröbner basis, and both P1.3 regression tests pass in under one second.
- [EMPIRICAL: local environment on 2026-06-23] Sage, Singular, and msolve are unavailable; all 13 shared-library tests pass under Python 3.13.4.

**Prediction vs. outcome:** Matched. Explicit quotient/order/algorithm choices were necessary, and exact Macaulay closure exposed the degree-3 fall and degree-4 Gröbner-basis containment.

**Did not work:** Preferred Gröbner executables were unavailable. The prescribed exact Python fallback was sufficient for SG-01.

**Changed my mind about:** A single quantity called “degree of regularity” cannot safely be copied from the experimental literature. Kousidis–Wiemers' highest Magma step degree belongs in the algorithm-trace column under the conventions fixed here.

**Next:** Start SG-02 by auditing the existing shared Semaev implementation, adding $f_6$, and producing validated degree and term counts.

## Session 2 — 2026-07-01

**Goal:** Complete SG-02 and SG-03, then build and run the smallest exact SG-04/SG-06 experiment matrix that local resources permit.

**Prediction (written before new algebra experiments):** Exact expanded $f_3$ and $f_4$ will be small, expanded $f_5$ will be reachable with sparse resultants, and generic expanded $f_6$ will be the first likely term-explosion boundary. Reducing factor-base variables modulo $x_i^q-x_i$ during arithmetic should keep the actual $n\in\{2,3\}$, $m\leq4$ Weil systems small enough for exact first-fall and solving-degree measurements at $q=3$ and at least part of $q=5$.

**Positive result criterion:** A validated $f_6$ evaluator, explicit coordinate Weil systems with known-root checks, and a CSV containing exact first-fall and solving degrees for more than one independent $q,n,m$ combination.

**Negative result criterion:** A declared per-case time or matrix-size ceiling is reached before Gröbner-basis containment; such a row must be recorded as censored rather than guessed.

**Did:**
- Added `f6_value` to shared tooling and validated it on six curve points summing to zero.
- Implemented exact sparse summation-polynomial expansion, polynomial-basis extension fields, elliptic-curve decomposition construction, and coordinate Weil restriction.
- Implemented the general syzygy-quotient first fall, Hilbert-function regularity, and closed-Macaulay solving degree with explicit field equations.
- Ran deterministic known and external targets through $q=3,5,7$, extended known $m=2$ targets through $q=23$, and stored stage-aware timeouts.
- Optimized Macaulay closure by batching new rows before RREF, which converted previously censored $q=3,m=4$, $q=5,m=3$, and $q=17,n=2,m=2$ cases into complete rows.
- Added a deterministic merge script and generated one 34-row canonical comparison table.
- Checked the results against Caminata–Gorla's invariant separations, Kousidis–Wiemers' binary scope, and Caminata–Ceria–Gorla's general Weil-restriction bounds.

**Found:**
- [EMPIRICAL: generic expansion with a 30-second/index ceiling] $f_3,f_4,f_5$ have respectively 13, 540, and 130,705 terms and total degrees 4, 12, and 32. Generic $f_6$ expansion crossed the declared ceiling; its evaluator is validated independently.
- [EMPIRICAL: 34 canonical cases] Thirty-two cases completed and the two $q=5,m=4$ known-target cases reached exact first fall and regularity before their 60-second solving-stage timeout.
- [PROVED] In the quadratic $m=2$ non-base-target shape, the top coordinates are $x_1^2x_2^2$ and $c x_1x_2(x_1+x_2)$, $c\ne0$, and their first fall degree is exactly 5 for odd $q\ge5$.
- [EMPIRICAL: $q\in\{7,11,13,17,19,23\},n=m=2$, known decompositions] The exact values are $d_{\mathrm{ff}}=5$ and $d_{\mathrm{reg}}=\operatorname{sd}_{\mathrm{grevlex}}=q$. The gap grows from 2 to 18, and every stored decomposition is a root.
- [EMPIRICAL: $q\in\{3,5,7,11,13,17\},n=3,m=2$, known decompositions] Solving degree stays 4 after $q=3$, while regularity grows with $q$; this independently confirms that regularity and solving degree are separate columns.
- [CITED] Caminata and Gorla (2023) already prove arbitrary invariant gaps for general systems, including a field-equation-driven family. The local observation is specific to the deterministic odd-characteristic Semaev/Weil construction and does not settle the binary asymptotic question.

**Prediction vs. outcome:** The prediction was accurate about $f_5$ being reachable and generic $f_6$ being the expansion boundary. The function reduction kept all $q=3,m\le4$ cases and the $q=5,m\le3$ cases solvable; $q=5,m=4$ was the first solving-stage boundary. The unpredicted positive result was a growing, known-solution first-fall/solving-degree divergence already visible at $m=2$.

**Did not work:** Sage, Singular, msolve, and Macaulay2 were unavailable. A first all-in-one $q=5,m=4$ run timed out without stage detail, and a first generic-$f_6$ attempt exceeded its external timeout. Both were replaced by worker-isolated, stage-aware runs; superseded rows remain in raw data but are removed by the canonical merge rule.

**Changed my mind about:** The most useful falsifier is not necessarily at $m\approx n$. In the odd-characteristic quadratic cases, a low-degree core syzygy coexists with field-equation-controlled Macaulay termination, producing a clearer growing gap at $m=n=2$.

**Next:** Test whether the $\operatorname{sd}=q$ pattern survives curve and target changes, and seek a proof or counterexample for the deterministic family before attempting a broad explicit upper bound.

**Final validation:** [EMPIRICAL: local environment on 2026-07-01] The final smoke case completed with a verified root and degrees (4,4,4); all 55 currently present shared tests and all 13 P1.3 tests passed, bytecode compilation passed, the canonical table had 34 unique keys, and `HANDOFF.md` remained below its 120-line cap.

## Session 3 — 2026-07-09

**Goal:** Push the quadratic divergence from a deterministic six-prime pattern toward a theorem: vary curves and targets, prove the uniform regularity and solving-degree lower bound, and either prove the matching upper bound or isolate its exact obstruction.

**Prediction (written before new experiments):** For every odd (q\ge5) and quadratic non-base target, the top Weil coordinates will force (d_{\mathrm{ff}}=5) and, after field equations, (d_{\mathrm{reg}}=q). The lower bound (\operatorname{sd}\ge q) should follow whenever the field equations genuinely shrink the core ideal. The difficult step will be (\operatorname{sd}\le q): it may require a field-equation theorem with additional hypotheses or explicit degree-(q) representations of a Gröbner basis. Varying curves and targets should preserve the first-fall/regularity values but may falsify the solving-degree equality.

**Positive result criterion:** A proved parameter-uniform statement stronger than the finite table, plus exact curve/target-variation data with verified roots; ideally a complete proof of (d_{\mathrm{ff}}=5<\operatorname{sd}=d_{\mathrm{reg}}=q) under explicit hypotheses.

**Negative result criterion:** A varied known-solution system with (\operatorname{sd}\ne q), or a precise theorem hypothesis that cannot be established for these systems. Either outcome must replace the current broad conjecture with a narrower falsifiable statement.

**Did:**
- Added explicit curve, target, and known-root overrides to the exact measurement pipeline.
- Enumerated 397 verified-root variants over $q=5,7,11$, recording core-ideal nonredundancy, core solving degree, field-equation remainder degrees, and mutant-family invariants.
- Derived the quadratic top-ideal proof $d_{\mathrm{reg}}=q$ and the nonredundancy lower bound $\operatorname{sd}\ge q$.
- Audited Caminata-Gorla's homogenized-regularity result and Salizzoni's closed-space bound; rejected raw $t$-saturation after an exact representative saturation calculation.
- Normalized the Semaev core in symmetric variables and generated an exact fraction-field Groebner certificate with sole exceptional factor $(m_1^2-4m_0)t_1^2/4$.
- Constructed a degree-at-most-4 mutant family inside the original degree-$q$ space and applied Salizzoni's bound to prove $\operatorname{sd}\le q$.
- Searched 566 abstract top-shape systems until finding a degree-$q+1$ counterexample, then exhaustively checked all 6,228 eligible actual $q=5$ curve/target systems.

**Found:**
- [PROVED] For every odd prime power $q\ge5$ and quadratic non-base target, $d_{\mathrm{ff}}=5$, $d_{\mathrm{reg}}=q$, and $\operatorname{sd}_{\mathrm{grevlex}}\le q$.
- [CONDITIONAL: the field equations enlarge the core ideal] The matching lower bound proves $\operatorname{sd}_{\mathrm{grevlex}}=q$.
- [PROVED] The normalized core basis has degrees $4,4,3,3$, leading monomials $xy^3,y^4,x^3,x^2y$, and lies in the closed degree-5 core space.
- [PROVED] Field-equation remainders have degree at most 3; the same-ideal mutant family has maximum degree and degree of regularity at most 4, hence solving degree at most 5 by Salizzoni (2023), Proposition 3.10.
- [EMPIRICAL: 397 verified-root variants over $q=5,7,11$] Every row has nonredundant field equations and $(d_{\mathrm{ff}},d_{\mathrm{reg}},\operatorname{sd})=(5,q,q)$.
- [EMPIRICAL: exhaustive actual $q=5$] All 6,228 eligible systems have solving degree 5.
- [EMPIRICAL: deterministic abstract $q=5$ search, seed 20260722] The tuple $(3,1,4,0,1,2,0,3)$ has solving degree 6 and $c+g^2=0$, proving that the top shape alone does not imply the upper bound.

**Prediction vs. outcome:** The first-fall, regularity, and lower-bound predictions matched. The upper bound was easier after abandoning raw homogenization saturation: a low-degree same-ideal mutant family made Salizzoni's general bound sharp enough. No actual varied counterexample appeared, but the abstract counterexample precisely identified the missing Semaev coefficient constraint.

**Did not work:** Raw homogenization is not $t$-saturated in the representative $q=5$ case; saturation adds $x+y-t$ and $y^2-ty$. A proof based on equality with the homogenized affine ideal was therefore invalid. The top shape alone also failed, as shown by the exact solving-degree-6 abstract counterexample.

**Changed my mind about:** The decisive structure is not just the degree-4/degree-3 top pair. It is the nonvanishing quadratic-modulus discriminant factor, which forces a constant-degree core basis and makes the field equations fall to cubic remainders.

**Next:** Prove or refute automatic field-equation nonredundancy, then test the constant-degree mutant-family strategy at $n=3,m=2$.

**Final validation:** [EMPIRICAL: local environment on 2026-07-09] All 69 shared-library tests and all 17 P1.3 tests passed, bytecode compilation passed, the symbolic JSON certificate regenerated successfully, the variant summary contained exactly 397 rows, the exhaustive actual $q=5$ search contained 6,228 eligible cases, and `HANDOFF.md` had 87 lines.
