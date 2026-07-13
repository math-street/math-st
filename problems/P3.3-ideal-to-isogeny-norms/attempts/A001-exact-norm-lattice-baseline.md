---
attempt: A001
status: dead
---
# A001 - Exact norm-lattice baseline before KLPT

## Idea

Construct integral prime-norm left ideals in an explicit maximal order of
$B_{p,\infty}$, reduce their positive-definite norm lattices, and certify the
true shortest vector by an exhaustive finite coefficient search.

## Prior art

[CITED] Kohel--Lauter--Petit--Tignol define the normalized norm
$q_I(x)=\operatorname{nrd}(x)/N(I)$ and the equivalent ideal
$I\bar x/N(I)$. [Kohel--Lauter--Petit--Tignol 2014, Section 2.4]

## Plan

1. Validate the order multiplication table and norm form.
2. Form $I=\mathcal O\ell+\mathcal O\alpha$ from a nonzero norm-zero residue
   $\alpha\bmod\ell$ and verify $[\mathcal O:I]=\ell^2$.
3. Apply exact-arithmetic LLL using the reduced-norm bilinear form.
4. Use inverse-Gram coefficient bounds to exhaust every possible vector below
   the initial reduced-basis norm.
5. Record at least 100 instances and stratified summaries.

## Execution log

1. Implemented exact quaternion/order arithmetic, canonical row HNF ideals,
   norm-aware LLL, inverse-Gram exhaustive SVP, and theta prefixes in
   `lib/quaternion.py`.
2. A smoke run exposed a row/column HNF transposition bug. The basis was fixed
   and a randomized closure regression was added.
3. The first 140-instance run accidentally used only $p\equiv3\pmod8$.
   It is retained as a pilot; the main run balances 70 instances in each
   admissible residue class.
4. The balanced run completed in 16.28 seconds and generated the raw data,
   summaries, and plot linked from `RESULTS.md`.

## Outcome

[EMPIRICAL: 140 prime-neighbor ideals, $7\le p\le223$] Norm-aware LLL found
the exact certified optimum on all 140 instances. The median normalized
equivalent-ideal norm was $N(J)/\sqrt p=0.35921$, and the largest observed
exponent was $\log_p N(J)=0.42357$.

[PROVED] The result is promising only as a toy lattice-side baseline. It does
not measure KLPT, impose an $\ell$-power output shape, or establish asymptotic
polynomial time.

## Post-mortem

**Why it failed:** [PROVED] The sampler fixed the input ideal norm at
$\ell\le31$. Since the central element $\ell$ lies in an integral ideal of
norm $\ell$, it supplies $q_I(\ell)=\ell$. Hence every sampled class already
had an equivalent representative of norm at most 31, independent of $p$.
The decreasing ratio to $\sqrt p$ was built into the input distribution.

**What transfers:** The exact quaternion arithmetic, HNF correction, LLL,
inverse-Gram SVP certificate, theta invariant, tests, and plotting pipeline all
transfer to A002 after changing the sampler to $\ell\asymp p$.

**Would it work under different assumptions?** [PROVED] Yes as a regression
suite for ideals known to be close to the principal class, but not as a
Minkowski-scale class sample.
