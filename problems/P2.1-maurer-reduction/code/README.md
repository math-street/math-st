# Code

## `measure_smooth_orders.py`

[PROVED] Samples seeded nonsingular short-Weierstrass curves, counts orders
with the exact BSGS/twist counter in `lib/curves.py`, factors the orders, and
writes raw and summary CSV files.

[PROVED] The summary includes Wilson 95% intervals, first-hit positions,
point-counting time, exact $B$-smooth counts in the Hasse interval, and a
numerical Dickman baseline.

[EMPIRICAL: 36 curves over 101 <= r <= 65519] Tests compare the BSGS counter
with exhaustive point counting and compare the segmented smoothness counter
with direct factorization.

Smoke run:

```powershell
python problems\P2.1-maurer-reduction\code\measure_smooth_orders.py --smoke
```

Recorded full run:

```powershell
python problems\P2.1-maurer-reduction\code\measure_smooth_orders.py `
  --bits 12,16,20,24,28,32,36,40 `
  --trials 512 --exponents 2,3 --seed 21012026
```

[EMPIRICAL: Windows 11, Python 3.13.4] The smoke run took 0.002 seconds and
the recorded full run took 20.67 seconds.

Tests:

```powershell
python -m unittest discover -s problems\P2.1-maurer-reduction\code\tests -v
```

## `measure_cm_coverage.py`

[PROVED] Enumerates the exact $j=0$/$j=1728$ twist-order families and the
ordinary principal-CM traces satisfying $4r=t^2-Dv^2$ for negative
fundamental $D$ up to the chosen bit-length power.  It records the first
smooth hit, fundamental class number, Frobenius conductor parameter, and
Wilson coverage intervals.

[EMPIRICAL: p in {7,13,17,19,31,37}] Exhaustive point counting validates all
explicit-family order sets.  [EMPIRICAL: p in {101,211}, |D| <= 200] A direct
trace scan validates the bounded-CM enumeration; known class-number fixtures
validate the reduced-form counter.

Smoke run:

```powershell
python problems\P2.1-maurer-reduction\code\measure_cm_coverage.py --smoke --workers 2
```

Recorded 4,096-prime runs:

```powershell
python problems\P2.1-maurer-reduction\code\measure_cm_coverage.py `
  --bits 60 --primes-per-bit 4096 --exponents 3 `
  --disc-exponent 2 --workers 8
python problems\P2.1-maurer-reduction\code\measure_cm_coverage.py `
  --bits 60 --primes-per-bit 4096 --exponents 3 `
  --disc-exponent 3 --workers 8
```

[EMPIRICAL: Windows 11, Python 3.13.4, 8 workers] The two commands took 28.50
and 42.95 seconds.  Their raw and summary files are
`measure_cm_coverage_b60_p4096_e3_d{2,3}_w8_20260625_{raw,summary}.csv`.

[PROVED] The script measures the CM norm-equation reachability condition; it
does not compute the class polynomial or instantiate the final curve.

## `summarize_cm_residues.py`

[PROVED] Aggregates an existing raw CM CSV by bit length, smoothness exponent,
discriminant bound, and prime residue modulo 12, with Wilson 95% intervals.

Smoke run:

```powershell
python problems\P2.1-maurer-reduction\code\summarize_cm_residues.py --smoke
```

Recorded residue table:

```powershell
python problems\P2.1-maurer-reduction\code\summarize_cm_residues.py `
  --raw problems\P2.1-maurer-reduction\data\measure_cm_coverage_b60_p4096_e3_d2_w8_20260625_raw.csv
```

[EMPIRICAL: 4,096 descending 60-bit primes] The command took under one second
and produced `measure_cm_coverage_b60_p4096_e3_d2_w8_20260625_residues.csv`.

## `random_order_lower_bound.py`

[PROVED] Computes the exact smooth fraction $\alpha$ in each selected Hasse
interval and the optimal iid-oracle success probability
$1-(1-\alpha)^q$.  It records the least query budgets for 50%, 95%, and 99%
success; no Monte Carlo approximation is used.

[PROVED] The result applies to the explicit model in which every fresh label
has an independent uniform order.  It is not a lower bound for structured
elliptic-curve construction algorithms.

Smoke run:

```powershell
python problems\P2.1-maurer-reduction\code\random_order_lower_bound.py --smoke
```

Recorded runs:

```powershell
python problems\P2.1-maurer-reduction\code\random_order_lower_bound.py `
  --bits 12,16,20,24,28,32,36,40 --exponent 2
python problems\P2.1-maurer-reduction\code\random_order_lower_bound.py `
  --bits 12,16,20,24,28,32,36,40 --exponent 3
```

[EMPIRICAL: exact intervals through 40 bits] At 40 bits the 50%/95% budgets
were 91/391 for $B=L^2$ and 6/25 for $B=L^3$.  Exhaustive finite answer-space
tests validate the probability formula and minimum-query calculation.

## `torus_alternative.py`

[PROVED] Implements the explicit norm-one conic
$x^2-dy^2=1$, its multiplication law, and the rational embedding/extraction
between $\mathbb F_r$ and all torus points except $(-1,0)$.  It is validation
tooling for A004, not a large-parameter search.

[EMPIRICAL: all parameters for four toy prime/nonsquare pairs] Exhaustive tests
verify the $r+1$ point count, parametrization, extraction, identity, and group
law closure.

Tests:

```powershell
python -m unittest discover `
  -s problems\P2.1-maurer-reduction\code\tests `
  -p test_torus_alternative.py -v
```

## `surface_jacobian_scan.py`

[PROVED] Exhausts the exact degree-four ordinary Weil-polynomial inequalities
over selected toy prime fields and applies the ordinary cases of
Howe--Nart--Ritzenthaler Theorem 1.2 to mark orders whose isogeny class
contains a genus-two Jacobian.  It then intersects those order sets with an
exact segmented smoothness mask on the central interval
$[r^2-r^{3/2},r^2+r^{3/2}]$.

[PROVED] The script certifies only that some Jacobian exists in an isogeny
class.  It does not construct a curve equation and therefore does not close
the Maurer--Wolf realization gap.

Smoke run:

```powershell
python problems\P2.1-maurer-reduction\code\surface_jacobian_scan.py --smoke
```

Recorded run:

```powershell
python problems\P2.1-maurer-reduction\code\surface_jacobian_scan.py `
  --bits 8,10,12 --exponent 3
```

[EMPIRICAL: r=251,1019,4091] The run took 1.39 seconds in total.  Every one
of the 596,339 interval integers, including all 117,476 smooth integers, had
an ordinary Jacobian-admissible Weil polynomial.  The output is
`data/surface_jacobian_scan_b8-10-12_e3_20260710.csv`.

[EMPIRICAL: r=16363] The 14-bit extension took 10.58 seconds.  All 4,186,243
interval integers and all 528,541 smooth integers were Jacobian-admissible.
The output is `data/surface_jacobian_scan_b14_e3_20260710.csv`.
