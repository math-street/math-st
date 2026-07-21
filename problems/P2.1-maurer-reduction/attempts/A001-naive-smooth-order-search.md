---
attempt: A001
status: dead
---
# A001 - Naive smooth-order curve search

## Idea

Sample nonsingular curves $y^2=x^3+ax+b$ over $\mathbb F_r$, count each order,
and stop when the largest prime factor is at most a chosen bound $B$.

## Prior art

[CITED] Maurer--Wolf 1999 uses a curve supplied as side information and leaves
polylogarithmic smoothness in the Hasse interval as an assumption; it does not
give a uniform blind-search construction (Sections 4.1.2--4.1.3).

## Plan

1. Validate exact point counting against hand-enumerated examples.
2. For several primes $r$ and bounds $B$, sample a fixed seeded sequence of
   nonsingular curves.
3. Record every order, largest prime factor, point-counting time, and success.
4. Compare the curve success rate with an exactly enumerated integer baseline
   on the Hasse interval, plus a Dickman approximation used only as a secondary
   heuristic.

## Prediction and decision rule

[HEURISTIC] Curve orders will behave like integers sampled from the Hasse
interval with respect to $B$-smoothness. The finite experiment falsifies this
operational version if the Wilson 95% confidence interval for the curve success
probability excludes the exact Hasse-interval integer proportion and the ratio
between the point estimate and baseline is outside $[1/2,2]$.

## Execution log

[EMPIRICAL: 36 curves over 101 <= r <= 65519] The BSGS/twist point counter
matched the exhaustive counter on every validation curve.

[EMPIRICAL: one prime at each of 12,16,...,40 bits; 512 curves per prime]
Ran `code/measure_smooth_orders.py` with seed 21012026 and bounds
$B=\lceil(\log_2 r)^2\rceil,\lceil(\log_2 r)^3\rceil$. The complete run took
20.67 seconds.

[EMPIRICAL: same run] At 40 bits, the quadratic bound had 4 successes in 512
curves and first succeeded at candidate 65; the cubic bound had 52 successes
and first succeeded at candidate 6.

## Outcome

[EMPIRICAL: same run] Every measured curve-to-exact-integer rate ratio lay in
$[0.867,1.859]$, so the pre-registered factor-two rejection rule did not fire.

[PROVED] This attempt supplies a reproducible search baseline but no
worst-case guarantee for every prime $r$.

## Post-mortem

**Why it failed:** [HEURISTIC] Under the very integer-smoothness model supported
by the measurements, blind search for $B=(\log r)^C$ takes
$r^{1/C+o(1)}$ candidates, not $\operatorname{poly}(\log r)$. A proof of a
polylogarithmic candidate bound would refute this diagnosis.

**What transfers:** [PROVED] The exact point counter, smoothness test, exact
Hasse-interval baseline, confidence intervals, raw data, and cost accounting
remain reusable for CM and structured-family experiments.

**Would it work under different assumptions?** [CONDITIONAL: a sampler whose
success probability is at least $1/\operatorname{poly}(\log r)$ for every
$r$] Replacing uniform curve sampling with that sampler, and using a
polylogarithmic point counter such as SEA, would yield expected
polynomial-time search.
