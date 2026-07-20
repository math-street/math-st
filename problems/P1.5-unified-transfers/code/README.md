# Experiment code

`run_transfers.py` constructs exact toy instances for both known elementary
transfer mechanisms, recovers a seeded logarithm, records operation counts and
median timings, and fits power laws against the algorithms' explicit work
predictors.

Run the under-ten-second validation path from the repository root:

```text
python problems/P1.5-unified-transfers/code/run_transfers.py --smoke
```

Reproduce the recorded seven-size experiment for each transfer:

```text
python problems/P1.5-unified-transfers/code/run_transfers.py --repeats 50 --seed 15072026
```

The raw CSV contains the exact curve, generator, secret, recovered logarithm,
target image, construction attempts, core-step counts, work predictors, and
timings. The pairing predictor multiplies Miller-line count by field bit length
because the auditable affine implementation retains denominator inversions. The scaling
CSV contains every fitted value and log-residual rather than only a fitted
exponent.

`probe_cm_class_targets.py` exhausts the natural CM annihilator, cyclic-kernel,
canonical Velu-quotient, and ray-class candidates on ordinary $j=1728$ toy
curves. It also validates the explicit class-number threshold and principal-unit
linearization.

Run the under-ten-second validation path:

```text
python problems/P1.5-unified-transfers/code/probe_cm_class_targets.py --smoke
```

Reproduce the eight-curve complete enumeration:

```text
python problems/P1.5-unified-transfers/code/probe_cm_class_targets.py
```

The full CSV checks every nonzero point in prime subgroups of order 5 through
113. On Python 3.13.4 the recorded full run completed in under one second.

`probe_buell_reduction.py` tests the explicit Buell point-to-quadratic-form
formula after replacing a number-field point by canonical integer
representatives of a finite-field point. It exhausts every nonzero point of ten
toy prime-order subgroups and records whether the resulting forms retain one
fixed discriminant.

Run the short validation path:

```text
python problems/P1.5-unified-transfers/code/probe_buell_reduction.py --smoke
```

Run the complete ten-case matrix:

```text
python problems/P1.5-unified-transfers/code/probe_buell_reduction.py
```

`probe_exact_order_targets.py` batch-enumerates every primitive reduced
positive form through a toy discriminant bound and records the least
discriminant whose class number is divisible by each tested prime.  This is an
existence census, not a uniform exact-order class constructor.

Run the known-answer and short-range path:

```text
python problems/P1.5-unified-transfers/code/probe_exact_order_targets.py --smoke
```

Run the complete census through discriminant magnitude 200,000:

```text
python problems/P1.5-unified-transfers/code/probe_exact_order_targets.py
```

`audit_rational_tradeoffs.py` exhausts small subsets of cyclic prime-order
groups and checks the ordered-difference identity and integer constants used
in the strengthened piecewise-rational $B^2$ theorem. It is a finite
falsification certificate, not a proof of the algebraic-geometric result.

```text
python problems/P1.5-unified-transfers/code/audit_rational_tradeoffs.py
```
