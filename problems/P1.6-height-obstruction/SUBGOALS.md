# Sub-goals

- **SG-01 (complete):** [EMPIRICAL: three LMFDB values] The exact height estimator matches the database within $2\cdot10^{-6}$.
- **SG-02 (complete):** [PROVED] Direct single-point lifts have height $O(\log p)$; [EMPIRICAL: six primes] the stored measurements include fits and residuals.
- **SG-03 (complete for construction and measurement):** [PROVED] Full-row-rank tuples with $k=2,3,4$ have simultaneous $O_k(\log p)$ lifts; [EMPIRICAL: six primes] all reductions were checked exactly.
- **SG-04 (partial):** [EMPIRICAL: three sampled variants per input] Least-norm corrections beat both bounded nullspace variants in all 72 comparisons; total ranks remain unavailable.
- **SG-05 (complete):** [EMPIRICAL: exact enumeration at p=257] The failure analysis's $1/65$ probability is reproduced.
- **SG-06 (complete):** [CONJECTURE] Least-norm random lifts have maximum height $\Theta_k(\log p)$ in probability; `NOTES.md` states a three-part falsifier.
- **SG-07 (complete for the literal single-point target):** [PROVED] The requested positive-power lower bound is refuted by an explicit upper bound; the missing attack input is a rank/dependence theorem under a no-small-relation distribution.

- **SG-08 (complete):** [EMPIRICAL: 144 curve variants at bits 5,7,9,11 and coefficient bound 8] Exact arithmetic found 99 finite-field relations and two rational relations; both rational witnesses are the same $p=31$, $k=1$ two-torsion input under two lift variants, while all 108 $k=2,3,4$ variants had no rational relation through the bound.
- **SG-09 (failed; A002 dead; Q018):** [PROVED] The local $p=17$ prototype is not a reproduction of Table 3 because the source does not fix the sampling/tie-breaking distribution and the published 2-descent dependence test is unavailable; no dependency rate from it is accepted.
