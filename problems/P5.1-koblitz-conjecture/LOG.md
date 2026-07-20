# Log — P5.1

## Session 1 — 2026-06-24

**Goal:** Complete SG-01 and the explicit, supported part of SG-02; obtain a first three-curve convergence table and map the GRH dependency.

**Prediction (written before running anything):**

- [HEURISTIC] The trivial-torsion Serre curve will yield a nonzero prime-order count and a measured/predicted ratio compatible with 1 at the largest toy cutoff; this prediction is refuted if the ratio's heuristic 95% interval excludes 1.
- [PROVED] The rational 2- and 3-torsion curves will yield no prime orders beyond finitely many tiny exceptions, because their good reductions contain the corresponding rational torsion point.
- [CITED] The truncated universal product will approach $0.505166168239435774$, and the explicit Serre correction will approach $0.561295742488261971$. (Zywina 2011, equations (2.3) and (5.1), arXiv:0909.5280.)

**Environment preflight:**

- [EMPIRICAL: Python 3.13.4 on Windows 11] `env/check_env.py` found SageMath, PARI/GP, Singular, and msolve unavailable.
- [EMPIRICAL: 34 shared tests] After installing pytest 9.1.1, `python -m pytest -q lib/tests` passed 34/34 tests in 0.94 seconds.

**Did:**

- Implemented `code/measure_density.py` with a deterministic prime sieve, the shared exact Hasse-interval BSGS/twist counter, an explicit exhaustive fallback, CSV output, convergence plots, and a sub-10-second smoke mode.
- Added four P5.1 tests: published constants, LMFDB point counts for 1728.w1, rational torsion certificates, and an end-to-end smoke measurement.
- Ran checkpoints from $2^{10}$ through $2^{17}$ for a trivial-torsion Serre curve and non-CM curves with rational 2- and 3-torsion.
- Audited Zywina's corrected constant and David--Wu's effective-Chebotarev/sieve dependency.

**Found:**

- [EMPIRICAL: 57 tests] `python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests lib/tests` passed 57/57 tests in 1.18 seconds.
- [EMPIRICAL: 67 reductions through $p=97$] The production counter matched exhaustive point counts on every validation case; 66 cases used BSGS/twist and one used the declared exhaustive fallback.
- [EMPIRICAL: Euler factors $\ell\le10^6$] The universal product was $0.505166202477432$ and the corrected Serre constant was $0.561295780530480$, each within $4\mathbin{\cdot}10^{-8}$ of Zywina's published value.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] Curve 1728.w1 had 683 prime-order reductions among 12,249 tested; the refined prediction was 654.886 and observed/predicted was $1.04293$.
- [HEURISTIC] A Poisson-style 95% interval for the final observed/predicted ratio is $[0.9647,1.1211]$; this interval ignores cross-prime dependence and finite-cutoff bias.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The raw $C_{E,1}x/(\log x)^2$ prediction was 529.85, giving observed/predicted $1.2890$, while the refined prime-sum ratio was $1.0429$.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] Both rational-torsion curves had zero prime-order reductions, matching the corrected $C_{E,1}=0$ obstruction.
- [CITED] David and Wu use the theta-zero-free hypothesis in effective Chebotarev error terms for division-field Frobenius counts; these errors set the sieve level $D=x^{(2/5)(1-\theta)(1-\varepsilon)}$. GRH is $\theta=1/2$, but $\theta<11/21$ already suffices for their eight-almost-prime corollary. (David and Wu 2012, Theorem 3.9, Theorem 1.1, and Corollary 1.2, arXiv:0812.2860.)

**Prediction vs. outcome:** matched. [EMPIRICAL: $p\le2^{17}$] The Serre ratio interval contains 1, both rational-torsion prime-order counts are zero, and the implemented constants reproduce the published targets.

**Did not work:**

- [EMPIRICAL: validation curve 112.b4 at $p=11$] Point-order congruences did not isolate the group order within 64 samples; the production path used the declared exhaustive exact fallback and matched the independent exhaustive fixture.

**Changed my mind about:**

- [EMPIRICAL: $p\le2^{17}$] The asymptotic $x/(\log x)^2$ expression is too biased for a useful toy-range comparison; the refined prime sum is not merely cosmetic at this scale.

**Next:** Implement the corrected quotient constant $C_{E,3}$ for the 3-torsion curve, then compare it with the already recorded 661 prime quotient orders.

## Session 2 — 2026-06-29

**Goal:** Finish SG-08 with a certified quotient-order constant, then finish SG-05 with a CM-specific constant, split-prime convention, measurement, and convergence comparison.

**Prediction (written before new computations):**

- [HEURISTIC] A correctly certified $C_{E,3}$ for the rational 3-torsion curve will agree with the existing quotient-prime data to within a Poisson-style 95% interval at $p\le2^{17}$; this is refuted if the interval excludes the predicted constant after independent finite-level validation.
- [HEURISTIC] For a CM curve, pooling split and inert rational primes into the non-CM predictor will fail visibly; this is refuted if the CM-specific and pooled predictors are statistically indistinguishable at the largest cutoff.
- [CITED] The CM local factors depend on splitting in the CM field and therefore differ from the full-$\mathrm{GL}_2$ product. (Koblitz 1988, Section 4; Zywina 2011, Section 2.3.)

**Environment preflight:**

- [EMPIRICAL: Python 3.13.4 on Windows 11] SageMath, PARI/GP, Singular, and msolve remain unavailable.
- [EMPIRICAL: 59 tests] `python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests lib/tests` passed 59/59 tests in 1.35 seconds.

**Did:**

- Retrieved LMFDB's exact level-30 adelic generators for 540.f2 and implemented deterministic subgroup generation plus exhaustive level-90 lifting.
- Derived the non-CM quotient correction from Zywina's finite-level formula without fitting any constant to the existing quotient counts.
- Implemented Zywina's accelerated CM Euler product, the $p\equiv1\pmod4$ split-prime filter, a full-$\mathrm{GL}_2$ negative-control benchmark, CSV output, and a convergence figure.
- Added four regression tests covering the finite group, the published CM constant, CM point-count structure, and the end-to-end measurement.

**Found:**

- [CITED] LMFDB records 540.f2 with equation $y^2=x^3+3x-11$, torsion order 3, adelic level 30, index 16, group order 8640 at level 30, and seven published generators. (LMFDB, curve 540.f2, accessed 2026-06-29.)
- [CONDITIONAL: LMFDB's level and generator data for 540.f2 are correct] Exact enumeration gives $|G(90)|=699840$, $|G(90)\cap\Psi_3(90)|=98280$, $\delta_{E,3}(90)=91/648$, and $C_{E,3}=(5824/5913)C$.
- [EMPIRICAL: Euler factors $\ell\le10^6$] The truncated 540.f2 quotient constant is $0.497562652330215$.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The 540.f2 quotient count is 661 versus 650.592 predicted, ratio $1.015998$; its measured-constant interval $[0.466985,0.544060]$ contains the prediction.
- [EMPIRICAL: Euler factors $\ell\le10^6$] The accelerated CM product is $1.067350966817026$, within $7.3\mathbin{\cdot}10^{-8}$ of Zywina's published $1.067350894$.
- [EMPIRICAL: split good primes $5\le p\le2^{17}$] The CM count is 765 among 6094 split primes versus 779.701 predicted, ratio $0.981145$; its measured-constant interval $[0.973017,1.121435]$ contains the prediction.
- [EMPIRICAL: all good rational primes $5\le p\le2^{17}$] The deliberately invalid pooled full-$\mathrm{GL}_2$ predictor gives 243.653 versus 987 observed, ratio $4.0508$.
- [EMPIRICAL: 70 tests] The complete P5.1 and shared suite passed 70/70 tests in 1.97 seconds.

**Prediction vs. outcome:** matched. [EMPIRICAL: $p\le2^{17}$] Both corrected predictors lie inside their heuristic intervals, and the invalid pooled CM benchmark fails by a factor of $4.05$.

**Did not work:**

- [EMPIRICAL: $p=7,t=8$] The first smoke run exposed a zero denominator in the refined weight at the finite endpoint $p+1=t$; the implementation now assigns no asymptotic baseline weight to $p+1\le t$.
- [EMPIRICAL: small CM primes] Hasse-interval point-order congruences sometimes did not isolate the curve order; the declared exhaustive exact fallback handled four cases in the full CM sweep.

**Changed my mind about:**

- [EMPIRICAL: $p\le2^{17}$] The CM split restriction is already visible at toy scale: it is not a presentation detail, because the pooled full-image model misses by a factor exceeding four.

**Next:** All stated empirical and theory deliverables are complete; an optional next experiment is to reproduce Zywina's published $x=2\mathbin{\cdot}10^7$ CM table row with the integral predictor and a faster point-count backend.

### Correction to Session 2

- [EMPIRICAL: 71 tests] The final post-documentation run of `python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests lib/tests` passed 71/71 tests in 1.93 seconds; this supersedes the earlier 70-test intermediate count.

## Session 3 -- 2026-07-06

**Goal:** Complete SG-09 by replacing general BSGS point counting with an exact $j=1728$ CM trace routine, validating it against exhaustive and BSGS counts, and reproducing Zywina's $x=2\mathbin{\cdot}10^7$ table entry.

**Prediction (written before new computations):**

- [EMPIRICAL: target $x=2\mathbin{\cdot}10^7$] An independently implemented exact CM counter will reproduce Zywina's published 49,847 quotient-prime events exactly; this prediction is refuted by any nonzero discrepancy after boundary conventions are aligned.
- [HEURISTIC] The refined CM prediction will remain close to the published expected count 50,063, with observed/predicted within 1%; this is refuted if the ratio lies outside $[0.99,1.01]$.
- [PROVED] A specialized $O(\log p)$ sum-of-two-squares trace computation per split prime removes the square-root-in-$p$ group-operation cost of the general Hasse-interval BSGS counter, once its sign convention is established and validated.

**Environment preflight:**

- [EMPIRICAL: Python 3.13.4 on Windows 11] SageMath, PARI/GP, Singular, and msolve remain unavailable.
- [EMPIRICAL: 73 tests] `python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests lib/tests` passed 73/73 tests in 2.27 seconds.

**Extended prediction (written after the first-row run but before the full-table run):**

- [EMPIRICAL: target checkpoints $2\mathbin{\cdot}10^7,4\mathbin{\cdot}10^7,\ldots,10^9$] The segmented exact counter will match all 50 published actual counts and all 50 rounded integral predictions in Zywina's Table 3; any nonzero row discrepancy refutes this prediction.

**Did:**

- Implemented Cornacchia's algorithm and Walsh's exact $d=-1$ trace specialization for $y^2=x^3-x$.
- Validated the specialized order against exhaustive point counting at every prime through 1000.
- Added a bounded-memory segmented sieve, a Hasse-bounded quotient-primality sieve, the equation-(7.1) numerical integral, 50 published regression fixtures, deterministic CSV output, and a convergence figure.
- Ran the complete published checkpoint sequence through $x=10^9$.

**Found:**

- [EMPIRICAL: every prime $5\le p\le1000$] The Cornacchia--Walsh order equals the exhaustive order at every tested prime.
- [EMPIRICAL: $x=2\mathbin{\cdot}10^7$] The counter returns 49,847 and the integral rounds to 50,063, reproducing Zywina's first actual and expected entries exactly.
- [EMPIRICAL: all 50 checkpoints $2\mathbin{\cdot}10^7\le x\le10^9$] All 50 actual-count differences and all 50 rounded-integral differences are zero.
- [EMPIRICAL: $x=10^9$] The final count is 1,548,766 versus 1,549,656.621 predicted, ratio $0.9994253$; 25,423,491 split primes were processed.
- [EMPIRICAL: Python 3.13.4, Windows 11] The full run took 148.7 seconds.

**Prediction vs. outcome:** matched exactly. [EMPIRICAL: all 50 published checkpoints] Both mismatch totals are zero, and observed/integral-predicted remains in $[0.9956899,1.0002392]$, inside the predicted 1% band.

**Did not work:** nothing remained unresolved. [EMPIRICAL: first smoke run] The small-endpoint baseline issue had already been fixed in Session 2, and both full and segmented sieves agree at $x=2\mathbin{\cdot}10^7$.

**Changed my mind about:**

- [EMPIRICAL: $x\le10^9$] A pure-Python exact reproduction at the paper's full range is practical once the CM trace replaces generic BSGS; the complete table requires under three minutes on the recorded host.

**Next:** No scoped computational deliverable remains; further progress would require new mathematics toward the unconditional Koblitz asymptotic rather than a larger reproduction.

**Final validation:**

- [EMPIRICAL: 81 tests] `python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests lib/tests` passed 81/81 tests in 9.13 seconds after the full-table implementation and documentation updates.

## Session 4 -- 2026-07-13

**Goal:** Adversarially self-verify the completed work through independent computational paths and explicit data-flow review, with emphasis on detecting circular validation.

**Prediction (written before the new checks):**

- [CONJECTURE] The Cornacchia--Walsh CM orders will match the generic Hasse-interval BSGS counter on deterministic large-prime samples through $10^9$; one mismatch refutes this prediction.
- [CONJECTURE] Independent SciPy quadrature will agree with the mpmath equation-(7.1) implementation to substantially below the 0.5 rounding threshold at every audited cutoff; a discrepancy of at least $10^{-3}$ refutes this prediction.
- [CONJECTURE] Full and segmented sieves will yield identical split-prime sequences at an enlarged audit bound, and the published table fixture will have no data-flow path into event counting; any mismatch or fixture-dependent count refutes this prediction.
- [CONDITIONAL: LMFDB's 540.f2 adelic generators and level are correct] An independent exact-arithmetic recomputation will recover $\delta_{E,3}(90)=91/648$ and correction $5824/5913$; any different fraction refutes the implementation.

**Environment preflight:**

- [EMPIRICAL: Python 3.13.4 on Windows 11] SageMath, PARI/GP, Singular, and msolve remain unavailable.
- [EMPIRICAL: 81 tests] The pre-audit shared and P5.1 suite passed 81/81 tests in 8.22 seconds.

**Did:**

- Compared the specialized CM counter with generic BSGS on deterministic split and inert primes spanning five orders of magnitude.
- Wrote an independent odd-only prime sieve and compared its full sequence with both production sieve modes.
- Evaluated equation (7.1) independently with SciPy quadrature in logarithmic coordinates.
- Recomputed both Euler products at 60-digit precision and decomposed the 540.f2 lift count into CRT-local conditions.
- Inspected the counting function's AST, corrupted a published fixture deliberately, and added persistent large-prime and anti-circularity regression tests.
- Audited the prose for stale range claims and wrote `audits/SELF-CHECK-20260713.md`.

**Found:**

- [EMPIRICAL: 12 split primes $10009\le p\le900010009$ and 3 inert primes $10007\le p\le100000007$] Every specialized CM order equals the generic BSGS order.
- [EMPIRICAL: split primes $p\le5000000$] Independent odd-only, production full, and production segmented sieves return the identical 174,193-element sequence.
- [EMPIRICAL: $x\in\{2\mathbin{\cdot}10^7,4\mathbin{\cdot}10^8,10^9\}$] SciPy and mpmath integral predictions differ by at most $1.2\mathbin{\cdot}10^{-9}$.
- [EMPIRICAL: Euler factors $\ell\le10^6$] Sixty-digit recomputation differs from the float universal and CM products by $9.0\mathbin{\cdot}10^{-15}$ and $2.4\mathbin{\cdot}10^{-13}$ respectively.
- [EMPIRICAL: 500 deterministic quotient samples below $10^9$] Eratosthenes, repository Miller--Rabin, and SymPy primality results have zero mismatches.
- [EMPIRICAL: exact CRT-decomposed enumeration] The independent count gives 98,280 favorable lifts out of 699,840 and reproduces $91/648$, $455/864$, and $5824/5913$.
- [PROVED] `measure` does not reference `PUBLISHED_TABLE`; corrupting the $x=10000$ fixture leaves the computed count at 105 and changes only the comparison field.
- [EMPIRICAL: documentation audit] Two stale Session-1 scope sentences were corrected, with no effect on code or data.
- [EMPIRICAL: 83 tests] The final suite passed 83/83 tests in 5.62 seconds.

**Prediction vs. outcome:** matched. [EMPIRICAL: all Session 4 checks] No production discrepancy or circular-validation path was found.

**Did not work:**

- [EMPIRICAL: disposable audit harness] The first odd-only sieve used an off-by-one extended-slice length and raised `ValueError`; deriving the slice count from its start index fixed the harness, after which all three sequences agreed. This code never entered a repository artifact.

**Changed my mind about:**

- [EMPIRICAL: documentation audit] Chronologically true claims can become misleading when later sections extend their scope; session-qualified wording is necessary even when append-only logs remain unchanged.

**Next:** The self-verification is complete. Q026 remains the explicit theoretical boundary; no computational or documentation defect is open.

## Session 5 -- 2026-07-20

**Goal:** Determine whether the theoretical gap can honestly be closed using primary literature available through 2026; if not, prove the strongest finite or conditional closure statement and isolate the irreducible missing theorem.

**Prediction (written before the literature audit):**

- [CONJECTURE] No primary source through 2026 proves the unconditional fixed-curve Koblitz asymptotic with positive corrected constant; a verified theorem doing so refutes this prediction.
- [CITED] Removing GRH from David--Wu's Chebotarev estimates alone will not produce the target asymptotic, because their method supplies no prime-order lower bound even under its zero-free hypothesis. (David and Wu 2012, Theorems 1.1 and 1.3.)
- [CONJECTURE] The strongest honest repository-level closure will be an exact finite-range theorem plus a conditional asymptotic statement whose unproved prime-value input is explicit; this prediction is refuted if the literature audit yields an unconditional asymptotic.

**Environment preflight:**

- [EMPIRICAL: Python 3.13.4 on Windows 11] SageMath, PARI/GP, Singular, and msolve remain unavailable.
- [EMPIRICAL: 84 tests] The pre-audit shared and P5.1 suite passed 84/84 tests in 6.10 seconds.

**Did:**

- Audited 2025--2026 primary literature for fixed-curve, average-family, and almost-prime results.
- Wrote `THEORY_CLOSURE.md` with an exact CM norm reduction and an explicit classification of unconditional, conditional, empirical, and still-open statements.
- Added three paper-specific reference notes and the mandatory fifth-session audit.
- Tested the new norm identity and residue-class exception independently, then added a persistent regression.

**Found:**

- [CITED] Dey--Saha--Sivaraman--Vatwani obtain the refined fixed-curve constant only under an elliptic Elliott--Halberstam conjecture and a separate conjecture on average growth of $N_p$. (Dey et al. 2025, DOI 10.1016/j.jmaa.2024.129212.)
- [CITED] Lee--Mayle--Wang explicitly state that the refined Koblitz conjecture remains open; their unconditional results are moments of constants over curve families. (Lee, Mayle, and Wang 2025, arXiv:2408.16641.)
- [CITED] Xie's 2025 unconditional CM advance concerns bounded-almost-prime quotients over prime-power fields, not prime values of $\#E(\mathbb F_p)/8$. (Xie 2025, arXiv:2504.18732.)
- [PROVED] For $E:y^2=x^3-x$, all prime-quotient events except $p=17$ lie in $p\equiv5\pmod8$ and are exactly simultaneous primality of $N(a+bi)$ and $N(a+bi+1)/8$. (`THEORY_CLOSURE.md`.)
- [EMPIRICAL: all 74,416 split primes $5\le p\le2,000,000$] The norm identity, divisibility by $8$, and unique $p\equiv1\pmod8$ event $(17,2)$ all matched the independent check.
- [EMPIRICAL: fifth-session audit] No unresolved verification tag, stale attempt, missing script validation, contradiction, or vague sub-goal was found. (`audits/AUDIT-20260720.md`.)

**Prediction vs. outcome:** matched. [CITED] The latest directly targeted fixed-curve theorem remains conditional, while the unconditional advances are averages or almost-prime results. (Dey et al. 2025; Lee, Mayle, and Wang 2025; Xie 2025.)

**Did not work:**

- [EMPIRICAL: first disposable Session 5 harness] The initial check called `is_prime` from the reproduction module, where it is not exported; importing the independently tested shared primality routine fixed the harness without changing any result or repository production code.

**Changed my mind about:**

- [PROVED] The CM residue classes sharpen the generic parity diagnosis: $p\equiv1\pmod8$ contributes only $p=17$, so the unbounded count is concentrated in one explicit simultaneous norm-prime pattern.

**Next:** Q026 is the only remaining theoretical statement: replace both distributional and parity-breaking conjectural inputs with unconditional theorems. No further numerical extension is logically required for the scoped closure.

**Final validation:**

- [EMPIRICAL: 85 tests] `python -m pytest -q problems/P5.1-koblitz-conjecture/code/tests lib/tests` passed 85/85 tests in 6.93 seconds after the theory regression and documentation updates.
