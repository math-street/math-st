---
attempt: A004
status: promising
---
# A004 - Sparse exact pure-power targets through 28 bits

## Idea

Measure the structural price of an exact $2^e$ or $3^e$ ideal norm on the
same 108 near-$p$ ideals as A002, without enumerating all smaller normalized
norms.

## Method

[PROVED] For each increasing target $T$, inverse-Gram diagonal bounds contain
every coefficient vector satisfying $q_I(x)=T$. Small boxes are evaluated in
overflow-checked int64 blocks. If the box exceeds $10^9$ tuples, the solver
enumerates three coordinates and solves the fourth from

$$a x^2+2h x+k=2TN(I).$$

The discriminant square and divisibility tests are necessary and sufficient,
and every returned witness is rechecked with exact integers. The first
represented target is therefore exact within the increasing target list.

## Execution log

1. Validated the sparse solver against the full exact spectrum.
2. Added a forced coordinate-elimination regression test.
3. Replayed the A002 seed, 18 primes, and six trials per prime.
4. Scanned powers of 2 and 3 through $4p$ and reconstructed every equivalent
   ideal, checking its norm and left closure.
5. Visually inspected the SVG/PNG output.

## Outcome

[EMPIRICAL: 108 near-$p$ ideals, 12/20/28-bit $p$, targets through $4p$]
All 216 pure-power optima were found without censoring. Mean exponents were
0.78713 for $2^e$ and 0.77643 for $3^e$, versus 0.40731 unconstrained.
Overall median penalties were 222.64 and 168.23; maximum penalties were
$209{,}715.2$ and $43{,}554.86$.

[EMPIRICAL: same range] The 28-bit median penalties were 2476.82 and 2622.49.
One $2^e$ optimum had exponent 1.01280; all other optima were at most $p$.
Only two rows required coordinate elimination.

[PROVED] A004 measures exact shaped existence, not KLPT. A matched basic-KLPT
implementation remains necessary to attribute its additional output-norm and
runtime gap.
