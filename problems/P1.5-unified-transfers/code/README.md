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

`probe_ring_class_transfer.py` validates A025's pairing-to-ordinary-ring-class
transfer. It maps every projective residue in
$\mathbb F_{p^2}^{\times}/\mathbb F_p^\times$ to a reduced primitive form of
discriminant $-4p^2$, verifies the conductor-unit quotient, and checks that
the pairing images of source orders $11$, $53$, and $83$ remain injective.
It also converts reduced forms back to the finite-field torus through a
Gaussian gcd and recovers the seeded logarithms.

```text
python problems/P1.5-unified-transfers/code/probe_ring_class_transfer.py --smoke
python problems/P1.5-unified-transfers/code/probe_ring_class_transfer.py
```

`probe_conductor_universality.py` is the A026/A027 falsification driver. It
checks the conductor-torus order formula against complete reduced-form
enumeration, inverts arbitrary Gaussian reduced forms through conductor-
coprime shearing and a Gaussian gcd, realizes the wild principal-unit line in
the ordinary class group of conductor \(p^2\), and checks the intrinsic
source-characteristic implication \(r\mid p-1\Rightarrow t=2\) under the
stated Hasse threshold.

```text
python problems/P1.5-unified-transfers/code/probe_conductor_universality.py --smoke
python problems/P1.5-unified-transfers/code/probe_conductor_universality.py
```

The full profile checks all source scalars for \(p=101,211,401\), all 44
projective tame residues at conductor 43, and three exact trace-two
divisibility fixtures. These are regression checks for the proofs, not
evidence that A026's effective conductor inverse is new: the prior-art audit
locates that general inverse in Castagnos--Laguillaumie (2009).

`probe_kummer_class_character.py` validates A028's maximal-order residue
character on the explicit A019 family
\(\Delta_r=1-4\cdot2^r\), \(\mathfrak a=(2,\omega)\),
\(\mathfrak a^r=(\omega)\). It finds a split
\(q\equiv1\pmod r\), verifies that
\(\omega^{(q-1)/r}\) has exact order \(r\), and recovers every scalar in the
target subgroup.

```text
python problems/P1.5-unified-transfers/code/probe_kummer_class_character.py --smoke
python problems/P1.5-unified-transfers/code/probe_kummer_class_character.py
```

The full profile covers ten primes \(3\le r\le31\). It is a finite
falsification certificate for the algebraic character, not a verification of
Chebotarev or of the GRH-conditional expected-polynomial auxiliary-prime
bound.

`construct_sg30_ring_class_target.py` implements A029's unconditional
target-only constructor. On every odd prime \(r\), it outputs the order of
discriminant \(-4r^4\), the contracted form
\([1+r^2,2r^3,r^4]\), and its canonical reduced representative
\([r^2,2r,r^2+1]\). Exact Gaussian residue arithmetic certifies class order
\(r\) without a class-group search.

```text
python problems/P1.5-unified-transfers/code/construct_sg30_ring_class_target.py --smoke
python problems/P1.5-unified-transfers/code/construct_sg30_ring_class_target.py
python problems/P1.5-unified-transfers/code/construct_sg30_ring_class_target.py --prime 101
```

The full profile contains 15 primes through \(10007\), keeps every target
discriminant within the repository's 60-bit ceiling, and independently checks
small complete class groups in the regression suite.
