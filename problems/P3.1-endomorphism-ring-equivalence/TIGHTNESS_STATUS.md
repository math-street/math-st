# Tightness status - P3.1

## Measured component

- [EMPIRICAL: p in {11,23,47,59,71}, ell=3, one timed trial per p] The exhaustive right-order-aware two-step dual round trip took 0.193, 0.458, 1.663, 2.634, and 4.702 seconds respectively (`code/toy_deuring_roundtrip.py`).
- [EMPIRICAL: p in {11,23,47,59,71}, ell=3, n=5] A log--log least-squares fit gives \(T(p)=0.002926p^{1.6796}\) seconds, \(R^2=0.9798\), and a classical 95% exponent interval \([1.2366,2.1226]\) (`code/fit_roundtrip_cost.py`, `data/fit_roundtrip_cost_ell3_p11-71_20260711.csv`).
- [PROVED] The residual CSV stores all five observed and predicted times, linear residuals, log residuals, the fitted coefficient and exponent, and the sample count.
- [EMPIRICAL: p=11, ell=3, 30 independent seeds] All 30 ideal--kernel--ideal, right-order lookup, and dual two-step checks succeeded; all four embedded right orders were visited with trace discriminant \(11^2\), every identity \(I\bar I=3O\) held, and each terminal curve returned the source `deuring_key`; the Wilson 95% interval is approximately \([0.886,1]\) (`data/toy_deuring_roundtrip_p11_ell3_trials30_20260711.csv`).

## Interpretation boundary

- [PROVED] The fitted exponent describes this exhaustive toy implementation only: it enumerates \(\mathbb F_{p^2}\) points, all norm-\(\ell\) neighbor ideals, and curve-scaling orbits.
- [PROVED] Those exhaustive operations are excluded from the intended cryptographic-size reduction, so the fitted exponent is not an asymptotic exponent for Wesolowski's reduction.
- [PROVED] The recorded path has `oracle_queries=0`; it validates the local Deuring dictionary rather than implementing a black-box reduction from Problem A to Problem B or conversely.
- [PROVED] Consequently the bit-loss proxy \(\Delta(p)\) from `REDUCTION_COST_SPEC.md` is not defined on these rows, because its \(\log_2 Q(p)\) and oracle-time terms require a genuine reduction with at least one oracle query.
- [PROVED] Assigning a numerical security-bit loss from the current timings would therefore conflate validation overhead with reduction loss.

## What remains for Task 2

- [PROVED] A valid first bit-loss row must instrument one complete oracle reduction, record \(Q(p)\ge1\), oracle and non-oracle time separately, and estimate success from at least 200 seeds before evaluating \(\Delta(p)\).
- [PROVED] The conditional Wesolowski route and the unconditional unrestricted-isogeny route must remain separate rows because only the former targets prescribed smooth degree.
- [PROVED] Task 2 remains open; the present deliverable supplies the first measured component and a precise non-identifiability statement, not a concrete security-loss function.
