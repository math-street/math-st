---
attempt: A002
status: promising
---
# A002 - Locate the exact-LLL scaling crossover

## Idea

Keep the rank, ideal sampler, norm convention, and validation checks fixed
while increasing only the quaternion prime size. This isolates whether the
perfect Session 1 LLL rate and tiny exact certificates persist as coefficients
grow.

## Prior art

[CITED] Kohel--Lauter--Petit--Tignol report that Minkowski-reduced normalized
ideal norms have successive-minimum product controlled by $p^2$ and expect the
largest minimum near $\widetilde O(\sqrt p)$ for generic ideals.
[Kohel--Lauter--Petit--Tignol 2014, Section 3.1]

## Plan

1. Select six primes per band, balanced between $3$ and $7$ modulo 8.
2. Sample five ideals per prime for 30 instances in each band.
3. Reuse exact equivalence, closure, theta-prefix, and inverse-Gram checks.
4. Store per-band means, maxima, exact-hit rates, and runtime residuals.
5. If LLL remains exact, test a constrained smooth/power norm search rather
   than increasing BKZ strength.

## Positive and negative outcomes

[HEURISTIC] A positive persistence result is a per-band LLL exact-hit rate of
at least 95% with every exact coefficient box at most 10,000 tuples. A negative
result is a lower hit rate or a larger certificate. Either outcome is limited
to the selected prime-neighbor sampler.

## Execution log

1. The first 12/20/28-bit run reused $\ell\le31$ and exposed the A001 sampling
   flaw because $N(J)/\sqrt p$ collapsed in the 20-bit band.
2. Added exact Tonelli--Shanks isotropic sampling for large prime norms and a
   `near-p` policy with $p<\ell<1.08p$ in the recorded grid.
3. Ran 108 ideals over 18 primes, six per prime and 36 per bit band.
4. Stored per-band timing fits and residuals in the scaling CSV.

## Outcome

[EMPIRICAL: 108 near-$p$ prime-neighbor ideals, 12/20/28-bit $p$] Norm-aware
LLL found the certified exact optimum on 108/108 instances. The median
$N(J)/\sqrt p$ was 0.37974 and the maximum exact coefficient box contained 81
tuples including zero.

[EMPIRICAL: same range] Mean exact exponents rose from 0.36378 at 12 bits to
0.41647 at 20 bits and 0.44167 at 28 bits, while mean
$N(J)/\sqrt p$ stayed between 0.35809 and 0.37189.

[PROVED] The near-$p$ neighbor sampler removes the trivial fixed-$\ell$ upper
bound but is not proved uniform in the ideal class group.
