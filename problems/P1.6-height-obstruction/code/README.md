# P1.6 code

## Height-growth experiment

[EMPIRICAL: local Python 3.13.4 environment] The default command runs in about
41 seconds and `--smoke` runs in under two seconds.

```powershell
python problems/P1.6-height-obstruction/code/measure_height_growth.py
python problems/P1.6-height-obstruction/code/measure_height_growth.py --smoke
```

[PROVED] `measure_height_growth.py` constructs a direct single-point short
lift and generalized Weierstrass simultaneous lifts for $k=1,2,3,4$, verifies
their reductions exactly, and refuses non-$p$-integral coefficient solutions.

[EMPIRICAL: default seed 16062026] The script writes point rows, curve/group
rows, summaries, fits, row-level residuals, and a PNG figure under `data/` and
`figures/`; every filename records the sizes, trial count, variant count,
height iterations, seed, and date.

## Literature reproduction

```powershell
python problems/P1.6-height-obstruction/code/reproduce_xedni_probability.py
```

[EMPIRICAL: exact enumeration at p=257] The script reproduces the paper's
$4/(N-3)=4/260=1/65$ small-relation probability for Experiment C.

## Exact relation audit

```powershell
python problems/P1.6-height-obstruction/code/analyze_lift_relations.py
```

[EMPIRICAL: 144 current lift variants, coefficient bound 8] The exact
meet-in-the-middle audit runs in about 76 seconds and separates finite-field
relations, rational relations, censored rows, heights, and discriminant
heights. `--summary-only` regenerates the stratified summary from stored rows.

## Failed p=17 reproduction attempt

`reproduce_xedni_p17.py` is retained as the diagnostic prototype from dead
attempt A002, not as a reproduction script whose rate may be compared with the
paper.

[PROVED] The prototype validates the finite input, projective containment
equations, Smith-lattice construction, and standard-model conversion, but the
source does not specify enough sampling/tie-breaking detail to identify the
published probability distribution.

[EMPIRICAL: local environment on 2026-07-14] The paper's 2-descent dependence
test is unavailable locally, so the bounded-relation diagnostic is not an
equivalent independence test and no generated dependency rate is accepted as
evidence.

## Tests

```powershell
python -m unittest lib.tests.test_heights -v
python -m unittest discover -s problems/P1.6-height-obstruction/code/tests -v
```

[EMPIRICAL: local Python 3.13.4 environment] The tests validate three LMFDB
canonical heights, quadratic scaling, generalized curve arithmetic, direct and
four-point reduction, the published $1/65$ count, exact bounded relations, and
the reusable algebraic components of the failed $p=17$ prototype.
