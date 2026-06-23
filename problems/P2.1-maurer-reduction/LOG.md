# Archived log - Sessions 1--10

## Session 1 - 2026-06-23

**Goal:** Complete SG-01 and build a validated first baseline for SG-02/SG-03.

**Prediction (written before running anything):** [HEURISTIC] For uniformly
sampled nonsingular short-Weierstrass curves, the measured probability that
$\#E(\mathbb F_r)$ is $B$-smooth will have the same order of magnitude as the
probability for a random integer near $r$; this prediction is falsified in the
tested range if the observed binomial confidence interval excludes the stated
integer baseline by a practically significant factor fixed in A001 before the
run.

**Did:**
- Initialized the P2.1 persistent folder and inspected the shared curve and DLP
  helpers.
- Ran the environment check and all shared tests before new mathematics.
- Verified the exact auxiliary-group condition and curve embedding directly in
  Maurer--Wolf 1999.
- Added an exact BSGS/twist point counter to `lib/curves.py`, tests, a seeded
  measurement script, exact interval baselines, Dickman estimates, and Wilson
  intervals.
- Ran 512 curves at each of 12, 16, ..., 40 bits for smoothness exponents 2
  and 3.

**Found:**
- [CITED] The auxiliary curve may be noncyclic, but its exact order must be
  known and $(\log r)^{O(1)}$-smooth; the rank-at-most-two curve group is
  handled by generalized Pohlig--Hellman (Maurer--Wolf 1999, Theorem 2 and
  Section 4.1.1).
- [PROVED] The DH oracle performs multiplication on implicit
  $\mathbb F_r$ elements, enabling the randomized curve embedding and final
  extraction of the target logarithm.
- [EMPIRICAL: 36 curves over 101 <= r <= 65519] The new point counter matched
  exhaustive enumeration in every validation.
- [EMPIRICAL: one prime at each of 12,16,...,40 bits; 512 curves per prime]
  At 40 bits, $B=1600$ succeeded 4/512 times (first hit 65) and $B=64000$
  succeeded 52/512 times (first hit 6); full details are in the summary CSV.
- [CITED] Jain's 2026 all-interval theorem remains outside the needed regime:
  its smoothness lower bound is super-polylogarithmic and its required
  interval is longer than the Hasse interval (Jain 2026, Theorem 1.2).

**Prediction vs. outcome:** [EMPIRICAL: same 4,096-curve run] Matched the
pre-registered factor-two criterion: all curve-to-integer rate ratios were in
$[0.867,1.859]$. Some small-size integer rates were outside the Wilson
interval, so the stronger claim of identical finite distributions was not
supported.

**Did not work:** [HEURISTIC] Blind random search does not plausibly become a
polylogarithmic construction: with $B=(\log r)^C$, the Dickman model predicts
$r^{1/C+o(1)}$ candidates. A proved polylogarithmic candidate bound would
falsify this assessment.

**Changed my mind about:** [HEURISTIC] The obstruction is sharper than "point counting is
expensive": even granting polynomial-time SEA per candidate, the candidate
count predicted for a polylogarithmic smoothness bound is super-polynomial in
$\log r$. A proved polylogarithmic candidate bound would refute this view.

**Next:** Enumerate the explicit CM order families from Maurer--Wolf Section
4.1.3 and measure what fraction of the smooth Hasse orders they can realize.
