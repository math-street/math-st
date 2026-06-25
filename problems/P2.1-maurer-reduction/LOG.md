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

## Session 2 - 2026-06-25

**Goal:** Complete SG-04, then use its output to start SG-05 and isolate the
constructive obstruction in SG-06.

**Prediction (written before running the Session 2 experiments):** [HEURISTIC]
The constant-size $j=0$/$j=1728$ order lists will show decreasing smooth-order
success as the field size grows, while a bounded-discriminant CM search with
$|D|\le(\log_2 r)^3$ will fail for at least one tested prime through 40 bits.
The explicit-family part is falsified by a stable nondecreasing Wilson trend
over the largest three sizes; the bounded-CM part is falsified if every tested
prime has a qualifying smooth order.

**Did:**
- Reopened the completed SG-01--03 handoff and initialized A002.
- Wrote validation tests first, then implemented the explicit $j=0$/$j=1728$
  order lists and bounded fundamental-discriminant CM scanner.
- Added process parallelism after the serial 44--60-bit commands exceeded the
  interactive wait window; the serial jobs ultimately completed and their
  189.47-second and 747.32-second files were retained.
- Extended the run to 4,096 descending 60-bit primes at discriminant bounds
  $60^2$ and $60^3$, then added a tested residue-class aggregator.
- Checked the CM construction and complexity qualifiers in
  Muzereau--Smart--Vercauteren 2004, Enge 2009, and May--Schneider 2023.

**Found:**
- [EMPIRICAL: p in {7,13,17,19,31,37}] The explicit twist formulas matched
  exhaustive point counts for every tested coefficient.
- [EMPIRICAL: p in {101,211}, |D| <= 200] Cornacchia enumeration matched a
  direct ordinary-trace scan, and four known class numbers matched.
- [EMPIRICAL: 128 descending primes at each of 44,48,52,56,60 bits]
  $B=|D|=L^3$ succeeded for all 640 prime/size instances, while explicit
  success declined from 52/128 to 15/128.
- [EMPIRICAL: 4,096 descending 60-bit primes, B=60^3] The explicit families,
  $|D|\le60^2$ CM scan, and $|D|\le60^3$ CM scan covered respectively
  445, 3,635, and 4,096 primes.
- [EMPIRICAL: same 4,096 primes, B=60^3 and |D|<=60^2] Coverage ranged from
  97.07% for $r\equiv1\pmod{12}$ to 76.48% for
  $r\equiv11\pmod{12}$; the explicit list has respectively 10 and 1
  candidate orders in those classes.
- [CITED] Muzereau--Smart--Vercauteren 2004 already isolates the need for a
  small CM discriminant whose associated order is smooth; May--Schneider 2023
  instead uses finite random curve searches and calls the auxiliary curve the
  non-uniform part of the reduction.
- [CONDITIONAL: Enge's floating-point precision heuristic] A
  polylogarithmic-discriminant witness can be converted through a class
  polynomial within a polynomial bit complexity; Enge's height bound is
  rigorous but its combined sharp rounding conclusion is explicitly
  heuristic.
- [EMPIRICAL: all 7,731 successful rows in the two 4,096-prime files] A final
  audit rechecked $t^2-Dv^2=4r$, $N=r+1-t$, and the recorded smoothness bound
  for every hit.
- [EMPIRICAL: 63 shared tests and 8 P2.1 tests] The final environment and full
  regression suite passed on Python 3.13.4.

**Prediction vs. outcome:** [EMPIRICAL: the recorded ensembles] The explicit
decay prediction matched qualitatively.  The bounded-CM prediction was
falsified already through 40 bits and more strongly by all-success $L^3$
coverage on the 44--60-bit and 4,096-prime runs.

**Did not work:** [HEURISTIC] Neither explicit families nor bounded-CM search
became a proof for every prime.  A fixed $L^K$ discriminant range exposes only
polynomially many candidate orders, for which the supported random-integer
model predicts $L^K r^{-1/C+o(1)}\to0$ coverage.  A proved arithmetic
correlation would falsify this assessment.

**Changed my mind about:** [EMPIRICAL: all 4,096 tested 60-bit primes] Cubic
discriminant coverage is much stronger at the permitted toy scale than the
pre-registered expectation.  It is worth retaining as a practical finite-size
strategy, but the same result does not support a worst-case asymptotic claim.

**Next:** Q005 is now the only blocking thread: prove or refute a uniform
small-CM/smooth-order correlation, or replace CM by a structured family with
proved coverage.  Do not extend the same finite scan past the 60-bit scaffold
ceiling.
