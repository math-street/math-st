# Results - P3.3 after Session 2 continuation

## Correction to the Session 1 baseline

[PROVED] The original 140-row dataset with input norms $\ell\le31$ is not a
valid Minkowski-scale class sample. For an integral ideal $I$ of norm $\ell$,
the central element $\ell\in I$ has

$$
q_I(\ell)=\frac{\operatorname{nrd}(\ell)}{N(I)}
=\frac{\ell^2}{\ell}=\ell.
$$

Thus those rows had the built-in upper bound $N(J)\le31$ for every $p$. They
remain useful arithmetic regressions but are superseded for all distributional
claims.

## Corrected unconstrained experiment

[EMPIRICAL: 108 near-$p$ prime-neighbor ideals, 12/20/28-bit $p$] The main
dataset uses 18 primes, six trials per prime, and 36 rows per bit band. Each
band is balanced between $p\equiv3$ and $7\pmod8$. The input norm is selected
from eight primes in the interval approximately $[p,1.08p]$, removing the
fixed-small-norm cap. Uniformity in the ideal class group is not assumed.

[PROVED] Every exact SVP certificate is exhaustive. If $H$ is the doubled norm
Gram matrix in the reduced coefficient basis and $c^THc\le2R$, then
Cauchy--Schwarz gives $|c_i|^2\le2R(H^{-1})_{ii}$. The script evaluates every
integer tuple in that certified box with the exact integral norm form.

| $p$ bits | $n$ | LLL exact hits | Mean $\log_pN(J)$ | Mean $N(J)/\sqrt p$ | Max nonzero box tuples |
|---:|---:|---:|---:|---:|---:|
| 12 | 36 | 36 | 0.36378 | 0.36186 | 80 |
| 20 | 36 | 36 | 0.41647 | 0.37189 | 80 |
| 28 | 36 | 36 | 0.44167 | 0.35809 | 80 |

[EMPIRICAL: same range] Across all 108 rows, LLL's approximation factor was
exactly 1, median $N(J)/\sqrt p$ was 0.37974, mean
$N(J)/\sqrt p$ was 0.36395, and the maximum observed exponent was 0.47016.

[EMPIRICAL: same range] A three-point fit of mean exact-search time gives slope
0.07064 for $\log_2(\text{seconds})$ against $\log_2p$, with residuals
$(-0.05264,0.10528,-0.05264)$. This tiny, noisy range is stored for
reproducibility and is not an asymptotic complexity claim.

### Dependence audit

[EMPIRICAL: same 108 rows] Mean exponents for $p\equiv3$ and $7\pmod8$ were
0.40468 and 0.40993, with normal 95% half-widths 0.01726 and 0.01256. Mean
$N(J)/\sqrt p$ was 0.36511 and 0.36279. No material $p\bmod8$ effect is visible
at this resolution.

[EMPIRICAL: same 108 rows] Splitting the input norm by
$\ell\equiv1$ or $3\pmod4$ gives mean exponents 0.40937 and 0.40539, with
overlapping normal 95% intervals. Exact input norms form 77 groups and 107 of
108 finite theta fingerprints are unique, so this design cannot separately
estimate input-norm or ideal-class effects. Those grouped rows remain in the
summary CSV rather than being promoted to a dependence claim.

## Exact norm-shape penalty

[EMPIRICAL: 70 near-$p$ prime-neighbor ideals, $7\le p\le223$] A separate
exact spectrum experiment enumerated all represented normalized norms through
$p$. Every row contained a power of 2, a power of 3, and a 5-smooth norm by
that first cutoff; no extension to $2p,4p,8p,$ or $16p$ was needed.

| Shape | Mean $\log_pN(J)$ | Median $\log_pN(J)$ | Median penalty over unconstrained | Maximum penalty |
|---|---:|---:|---:|---:|
| Unconstrained | 0.22152 | 0.24283 | 1.00 | 1.00 |
| $2^e$ | 0.31608 | 0.30642 | 1.00 | 21.33 |
| $3^e$ | 0.38109 | 0.40635 | 1.50 | 20.25 |
| 5-smooth | 0.22488 | 0.24283 | 1.00 | 1.43 |

[EMPIRICAL: same range] The pure-power constraint creates a real tail penalty,
but the exact constrained optima remain at exponent at most 1 on every row.
Fifteen of 70 rows were principal, so the sampler still overrepresents easy
classes relative to an unknown uniform-class baseline.

## Exact sparse pure-power targets through 28 bits

[PROVED] For a fixed target $T$, the target solver first applies the same
inverse-Gram bounds to every coefficient. Certified boxes of at most $10^9$
tuples are scanned in overflow-checked int64 blocks. For a larger box, it
enumerates three coefficients and writes the remaining equation as

$$
a x^2+2h x+k=2T N(I).
$$

The fourth coefficient exists exactly when
$h^2+a(2TN(I)-k)$ is a square with an integral in-range root. Thus this
coordinate-elimination branch is exhaustive, not heuristic. Scanning target
powers in increasing order certifies the first represented power.

[EMPIRICAL: 108 near-$p$ ideals, 12/20/28-bit $p$, targets through $4p$] The
solver determined both pure-power optima on all 108 rows without censoring.
Two rows used coordinate elimination; the largest certified full box had
$5{,}254{,}365{,}169$ tuples, but the successful elimination needed only
$1{,}241{,}059$ triples on that row.

| $p$ bits | $n$ | Unconstrained mean exponent | $2^e$ mean exponent | $2^e$ median penalty | $3^e$ mean exponent | $3^e$ median penalty |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 36 | 0.36378 | 0.68955 | 18.31 | 0.67265 | 11.86 |
| 20 | 36 | 0.41647 | 0.82582 | 255.28 | 0.79410 | 166.13 |
| 28 | 36 | 0.44167 | 0.84601 | 2476.82 | 0.86253 | 2622.49 |
| All | 108 | 0.40731 | 0.78713 | 222.64 | 0.77643 | 168.23 |

[EMPIRICAL: same range] The maximum penalties were $209{,}715.2$ for $2^e$
and $43{,}554.86$ for $3^e$. One $2^e$ optimum was above $p$, at exponent
1.01280; every other $2^e$ optimum and every $3^e$ optimum was at most $p$.
The maximum $3^e$ exponent was 0.97585.

## Structural-versus-algorithmic verdict

[EMPIRICAL: 108 rows through 28 bits] No unconstrained lattice-reduction gap is
visible: norm-aware rank-4 LLL always equals exact SVP and stays at a constant
fraction of $\sqrt p$ on average.

[EMPIRICAL: 108 rows through 28 bits] Requiring an exact power of 2 or 3 is a
substantial structural constraint: median penalties grow from tens at 12 bits
to thousands at 28 bits. The small-$p$ spectrum experiment therefore hid a
real finite-size tail. Nevertheless every measured optimum is below
$p^{1.013}$, still far below the basic KLPT estimate near $p^{7/2}$.

[PROVED] No KLPT implementation was run, so the experiment cannot allocate the
remaining gap among KLPT's lifting, congruence, and binary norm-equation steps.
The bounded verdict is: prescribed pure-power shape explains a material part
of the gap over unconstrained SVP, while the much larger gap from the exact
shaped optimum to basic KLPT remains algorithmic/search-structural in the
tested ranges.

## Literature correction

[CITED] The 2014 paper estimates the complete basic $\ell$-power ideal output
near $p^{7/2}$ under optimistic heuristics; $p^3$ is the scale of its
intermediate lifted quaternion. [Kohel--Lauter--Petit--Tignol 2014, Theorem 7]

## Main artifacts

- Unconstrained raw data:
  `data/measure_norm_gap_p2203-245000047x18_t6_s33032028_enearp_20260701_raw.csv`
- Unconstrained scaling/residuals:
  `data/measure_norm_gap_p2203-245000047x18_t6_s33032028_enearp_20260701_scaling.csv`
- Unconstrained plot:
  `figures/measure_norm_gap_p2203-245000047x18_t6_s33032028_enearp_20260701.png`
- Shape raw data:
  `data/measure_shape_gap_p7-223x14_t5_m16_b5_s33032030_20260713_raw.csv`
- Shape plot:
  `figures/measure_shape_gap_p7-223x14_t5_m16_b5_s33032030_20260713.png`
- Sparse pure-power raw data:
  `data/measure_power_targets_p2203-245000047x18_t6_m4_s33032028_20260713_raw.csv`
- Sparse pure-power summary:
  `data/measure_power_targets_p2203-245000047x18_t6_m4_s33032028_20260713_summary.csv`
- Sparse pure-power plot:
  `figures/measure_power_targets_p2203-245000047x18_t6_m4_s33032028_20260713.png`
