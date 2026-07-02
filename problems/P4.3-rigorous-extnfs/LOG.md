# Session log

## Session 1 — 2026-07-02

**Goal:** Complete SG-01–SG-03 and attempt SG-04 only if the actual norm forms can be instantiated without substituting a proxy.

**Prediction (written before running checks or experiments):** [CONJECTURE] The relation-yield assertion will require a uniform lower bound for simultaneous smooth values of two correlated, parameter-dependent norm forms; no cited theorem will cover the full exTNFS range. A refuting result would be a published unconditional theorem whose hypotheses include those two forms and whose lower bound has the required $L(1/3)$ exponent uniformly over exTNFS polynomial selection.

**Did:**
- Initialized the problem directory because it was absent from the fresh repository.
- [PROVED] The repository baseline has Python 3.13.4 and all 34 shared tests pass; Sage, Singular, and msolve are unavailable but are not required for SG-01--SG-04.

**SG-04 prediction (written before running the experiment):** [CONJECTURE] The two actual norm sides will be positively correlated because both contain the same $a^3+ab^2$ term, so the joint-smooth density will exceed the product of the two actual marginal densities. A refuting test is a joint-dependence ratio at most $1$ for at least three of the four recorded bounds. A practically significant divergence from the random model is declared only if the exact actual joint density lies outside the baseline's 95% Wilson interval and differs by a factor of at least $1.5$ at two adjacent bounds.

**Found:**
- Pending.

**Prediction vs. outcome:** Pending.

**Did not work:** Pending.

**Changed my mind about:** Pending.

**Next:** Run the repository environment check and shared tests, then reconstruct the algorithm from primary sources.

## Session 1 completion addendum - 2026-07-02

**Did:**
- Read and checked the primary exTNFS, random-integer smoothness, fixed-form smoothness, randomized NFS, rigorous finite-field DLP, and smoothness-testing sources recorded in `refs/`.
- Wrote the complete algorithm and numbered statements S-01--S-10 in `SMOOTHNESS_ASSUMPTIONS.md`.
- Implemented and tested `code/measure_norm_smoothness.py`; ran the smoke and exhaustive $A=4$ experiment.
- Independently checked all stored factorizations with SymPy and checked 64 stratified norm values against nested symbolic resultants.

**Found:**
- [PROVED] The minimal relation-supply input is the joint lower bound (RC) for $F_fF_g$; separate marginal density claims do not imply it.
- [CITED] The fixed-form and fixed-field theorems checked do not have the varying-field, multivariate, sparse-smoothness, and adaptive-lattice quantifiers required by exTNFS.
- [PROVED] Special-$q$ descent requires (SQ) uniformly over an adaptive family of prime-ideal lattices, which is stronger than the unconditioned relation statement.
- [CITED] Hyperelliptic smoothness testing discharges the accepted-candidate factorization cost, while Canfield--Erdos--Pomerance discharges only the random-integer benchmark.
- [CITED] Bender--Pomerance supply a rigorous finite-field DLP fallback, but its medium-characteristic cost has exponent $1/2$ or $\ell_p$, not $1/3$.
- [EMPIRICAL: p=5, eta=2, kappa=3, A=4, 5,856 primitive vectors] The actual/baseline joint-smooth rate ratios at $B=7,13,31,61$ are 8.50, 7.76, 3.66, and 3.05; the exact actual joint rates lie above every corresponding baseline 95% Wilson interval.

**Prediction vs. outcome:** The theory prediction matched: no checked theorem covers the full simultaneous tower-norm claim uniformly.  The empirical positive-dependence prediction also matched at all four bounds, and the declared divergence criterion was met at all four.

**Did not work:** [PROVED] Lee--Venkatesan coefficient randomization cannot be transferred literally: after the relative resultant varies in the tower order, the outer field norm is nonlinear and is not an integer arithmetic progression.  [PROVED] Fixed-field smooth-ideal counts also do not pair a short generator with a smooth value on the second side.

**Changed my mind about:** [PROVED] The main statement's obstruction is not one generic “norm smoothness heuristic.”  It consists of distinct relation, target-splitting, squarefree, local special-$q$, and adaptive-uniformity assertions; polynomial selection and matrix rank are additional non-smoothness gaps.

**Next:** Investigate Q013 first at fixed tower degree $\eta=2$ by expanding randomized outer norms and testing whether any candidate-rich slice falls under an existing binary-form theorem.

### Correction to the Session 1 completion addendum

[PROVED] `OPEN_QUESTIONS.md` already contained Q013--Q015 when the final repository-wide scan was run.  The two new P4.3 gaps are therefore Q016 (tower coefficient randomization) and Q017 (relation-matrix rank); the preceding `Next` line's Q013 label should be read as Q016.

[PROVED] The four `Pending` placeholders in the initial Session 1 entry are superseded by the completion addendum above; they are retained only because `LOG.md` is append-only.

[PROVED] Final validation after all edits passed 58 shared tests and all 3 P4.3 tests; the deterministic smoke run reproduced 544 candidates and the dated output files.

[PROVED] A final independent SymPy replay matched all 23,424 stored factorizations and 128 nested resultants from 64 stratified candidates in the exhaustive $A=4$ data.
