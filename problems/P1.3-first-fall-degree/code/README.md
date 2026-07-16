# Code

All commands below are run from this directory with Python 3.13.4 and SymPy
1.14.0. Arithmetic over prime fields is exact.

## `measure_toy_degrees.py`

Implements modular RREF, closed Macaulay spaces, monomial-top-ideal
regularity, and a traceable naive Buchberger run for SG-01.

```powershell
python measure_toy_degrees.py --smoke
```

Validation: reproduces Caminata–Gorla Example 4.2 at $q=5$ and the locally
proved $3,4,8,9$ tuple. Runtime: under one second.

## `sparse_weil.py`

Provides exact polynomial-basis finite fields, sparse polynomials, recursive
Semaev resultants, elliptic-curve arithmetic, constructed decompositions, and
coordinate Weil restriction. It is imported by the measurement scripts.

Validation: finite-field inverse tests, fixed $f_3/f_4$ values, zero-sum
tests through $f_6$, nonsingularity checks, and known-root substitution for
$n=2,3$, $m=2,3,4$.

## `measure_semaev_stats.py`

Expands generic $f_i$ and records term and degree statistics with a separate
worker timeout for each index.

```powershell
python measure_semaev_stats.py --max-index 6 --term-limit 250000 `
  --per-index-timeout 30
```

Recorded runtime: $f_3$ and $f_4$ are subsecond, $f_5$ took 19.1 seconds,
and generic $f_6$ was censored at 30 seconds.

## `measure_weil_degrees.py`

Builds a deterministic odd-characteristic Semaev/Weil system and computes:

- the exact syzygy-quotient first fall in
  $\mathbb F_q[x]/(x_1^q,\ldots,x_m^q)$;
- Hilbert-function degree of regularity after explicit field equations;
- grevlex solving degree by exact closed Macaulay spaces and target
  Gröbner-basis containment.

```powershell
python measure_weil_degrees.py --smoke
python measure_weil_degrees.py --q 19 23 --n 2 --m 2 --modes known `
  --degree-ceiling 30 --case-timeout 90 --output ..\data\check.csv
```

Every row records the field model, curve, target, root check, engine/version,
order, resource ceilings, elapsed time, and last completed pipeline stage.
Recorded range: $q=3,5,7,11,13,17,19,23$, with runtimes from milliseconds
to 26.3 seconds for complete cases. The $q=5,m=4$ cases were censored at 60
seconds after exact first-fall and regularity stages.

## `merge_degree_results.py`

Merges repeated degree runs by retaining the row that reached the furthest
pipeline stage for each $(q,n,m,\text{target mode})$.

```powershell
python merge_degree_results.py
```

Validation: a regression test checks that a later regularity-stage row
replaces an earlier system-build timeout. Runtime: under one second for the
current 34-row canonical table.

## `measure_quadratic_variants.py`

Enumerates exact nonsingular quadratic-extension curves and known non-base
targets, then records the three degree invariants, root checks, core-ideal
nonredundancy, the core basis cutoff, field-equation remainder degrees, and
the low-degree mutant-family invariants.

```powershell
python measure_quadratic_variants.py --q 5 --a0-count 5 `
  --a1-values 1 2 --b0-count 5 --b1-values 0 1 `
  --targets-per-curve 2 --case-timeout 0
```

Validation: 397 complete structured verified-root variants over $q=5,7,11$;
every row
has first fall 5, regularity and solving degree $q$, core solving degree 5,
and mutant solving degree at most 4. This sampler fixed a non-base coefficient
of $A$ and therefore did not cover the A005 counterexample family.

## `certify_quadratic_family.py`

Computes the normalized core Groebner basis and checks explicit identities in
$\mathbb Z[b,c,d,e,f,g,h,i][(c+g^2)^{-1}]$, including every Buchberger pair,
the sole specialization denominator, a unit quartic top-part minor, the Semaev
discriminant identity, and containment in the closed degree-5 core space.

```powershell
python certify_quadratic_family.py
```

Validation: the generated JSON certificate records basis degrees
$4,4,3,3$, leading monomials $xy^3,y^4,x^3,x^2y$, and
$(m_1^2-4m_0)t_1^2/4$ as the exceptional factor.

## `certify_quadratic_field_equations.py`

Checks the symbolic infinite family with redundant field equations and the
smallest concrete counterexample over $\mathbb F_7$.

```powershell
python certify_quadratic_field_equations.py
```

Validation: the concrete on-curve system is nonsingular, has eight distinct
$\mathbb F_7^2$ core zeros, zero normal forms for both field equations, and
$(d_{\mathrm{ff}},d_{\mathrm{reg}},\operatorname{sd})=(5,7,5)$.

## `search_quadratic_counterexamples.py`

Separates the Semaev coefficient constraint from the top shape by searching
both abstract normalized symmetric cores and actual curve/target systems.

```powershell
python search_quadratic_counterexamples.py --q 5 --abstract-trials 1000 `
  --actual-exhaustive
```

Validation: the fixed abstract tuple $(3,1,4,0,1,2,0,3)$ has solving degree
6 and hits the excluded denominator pole; all 6,228 eligible actual $q=5$
systems have solving degree 5.

## `search_quadratic_redundancy.py`

Exhaustively counts rational core zeros for every eligible system at
$q=5,7,9$ and checks exact normal forms for prime-field survivors.

```powershell
python search_quadratic_redundancy.py --q 5 7 9
```

Validation: there are no redundant cases at $q=5$, exactly six at $q=7$,
and none at the non-prime field $q=9$. The scopes contain respectively
6,228, 50,376, and 236,160 eligible systems.

## `summarize_quadratic_variants.py`

Validates and condenses the curve/target CSV files into the three-row
`quadratic_family_summary_20260709.csv` table.

## Tests

```powershell
python -m unittest discover -s tests -v
```

The local suite includes a $q=7,n=m=2$ strict-divergence regression, the
localized-ring core certificate, the genuine redundant $q=7$ Semaev
counterexample, the top-ideal regularity formula, and a fixed abstract
top-shape counterexample with solving degree $q+1$.
