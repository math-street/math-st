---
attempt: A003
status: completed
---
# A003 - Alternative auxiliary groups and a rigorous search lower bound

## Idea

[CONJECTURE] A different constant-rank algebraic group may avoid the small-CM
condition, or failing that, the random-order heuristic can at least be replaced
by a precise adaptive-query theorem in an explicit oracle model.  The first
branch is refuted by an every-prime construction with proved polynomial cost;
the second is refuted by an adaptive strategy beating the reciprocal smooth
fraction in the stated independent-order model.

## Prior art

[CITED] Maurer--Wolf 1999 permits constant-rank strongly algebraically defined
abelian auxiliary groups, not only elliptic curves.

[CITED] May--Schneider 2023 uses elliptic curves and finite random search; its
discussion points to multiplicative-group and tightness variants but does not
state an unconditional every-prime construction.

## Plan

1. Audit current primary work on multiplicative, toric, CM, and higher-
   dimensional auxiliary groups.
2. Check whether any route has order that is provably polylog-smooth for every
   prime while retaining polynomial implicit arithmetic and decoding.
3. Define an independent random-order oracle on the exact Hasse interval.
4. Prove the optimal adaptive success probability and validate it by exhaustive
   toy dynamic programming or simulation.
5. State exactly which conclusion transfers, and which remains model-only.

## Prediction and decision rule

[CONJECTURE] The literature branch will close negatively under the explicit
three-part test: uniformity for every prime, polylogarithmic largest factor,
and polynomial construction cost.  One primary result satisfying all three
falsifies the prediction.

[PROVED] In an oracle returning independent uniform Hasse-interval orders for
new labels, adaptivity cannot change the per-query hit probability $\alpha$;
after $q$ distinct labels the success probability should be
$1-(1-\alpha)^q$.  A counterexample policy in an exhaustive finite model
falsifies the proposed proof.

## Execution log

- [CITED] Checked Bollauf--Parisella--Siim 2025's current den Boer reduction.
  The full multiplicative auxiliary group gives polynomial asymptotic cost
  when $P^+(r-1)=(\log r)^{O(1)}$.
- [CITED] Checked Li 2025's shifted-prime theorem, which gives infinitely many
  primes with $P^+(r-1)>r^{0.679}$.
- [PROVED] Therefore the full $\mathbb F_r^*$ route fails the every-prime test
  for every fixed polylogarithmic bound.  Full extension groups do not repair
  it because $r-1\mid r^n-1$; additive groups have the large prime order $r$.
- [CITED] Checked Younis 2024's smooth-short-interval results.  Even under RH,
  the polylogarithmic range requires fixed interval exponent $\theta>1/2$ and
  excludes the Hasse endpoint.
- [PROVED] Defined an iid oracle that assigns every fresh curve label a
  uniform Hasse-interval order.  Conditioning on an all-failure transcript
  proves that every next fresh query fails with probability $1-\alpha$, hence
  no adaptive policy exceeds $1-(1-\alpha)^q$ after $q$ distinct queries.
  Fresh independent queries attain equality.
- [PROVED] Added `random_order_lower_bound.py` and first wrote failing tests
  for the probability, minimum-query, and exhaustive-sequence functions.
- [EMPIRICAL: exhaustive small answer spaces] Exact sequence counts matched
  the closed formula for all test fixtures.
- [EMPIRICAL: exact Hasse-interval counts at 12,16,...,40 bits] For $B=L^2$,
  the idealized 50%-success budget grew from 2 to 91 and the 95% budget from 6
  to 391.  For $B=L^3$, the corresponding budgets grew from 1 to 6 and from 2
  to 25.  The recorded CSVs are in `data/random_order_lower_bound_*`.

## Outcome

[PROVED] The oracle branch succeeded exactly in its stated model.  It replaces
the informal claim that adaptivity cannot help *blind independent sampling*
with a theorem and an attaining policy.  It does not transfer to structured
curve families or coefficient-selection algorithms.

[EMPIRICAL: primary-source audit through 2026-06-29] The literature prediction
was not falsified: no checked route met every-prime coverage,
polylogarithmic-smooth order, and polynomial construction simultaneously.
This finite audit is not a proof that no such construction exists.

[PROVED] A genuine new obstruction was obtained for one branch: Li's theorem
rules out the full multiplicative group (and full multiplicative extension
groups) as a uniform solution.  It does not rule out subgroups, norm-one
tori, elliptic curves, or general admissible auxiliary groups.  A003 therefore
narrows Q005 but does not complete the unconditional CDH-to-DLP reduction.
