# P4.1 results -- final scoped report

## Cost model and validation

[CITED] Kim and Barbulescu derive exTNFS asymptotic costs for composite extension degrees and a special-form variant relevant to polynomial pairing families (Kim--Barbulescu 2016, CRYPTO, pp. 543--571, doi:10.1007/978-3-662-53018-4_20).

[CITED] Barbulescu and Duquesne model finite SexTNFS cost as relation collection plus sparse linear algebra, with Dickman smoothness probabilities computed from sampled norm sizes (Barbulescu--Duquesne 2019, *Journal of Cryptology* 32(4), Section 4.2 and Equation 2).

[PROVED] `lib/tnfs_cost.py` exposes the coefficient bound, smoothness bound, tower dimension, roots-of-unity quotient, Galois-automorphism quotients, factor-base and matrix numerators, row weight, and cost overheads as named inputs.

[PROVED] Dickman's delay equation is integrated separately on each unit interval from an 80-decimal-digit, degree-30 `mpmath` Chebyshev fit, stored and evaluated in the power basis. This avoids the non-positive values caused by binary64 cumulative quadrature near `rho(10.76)` and remains validated through `u=16`, while retaining `rho(2)=1-log(2)` to displayed precision.

[EMPIRICAL: BD19 BN fixture] The model obtains smoothness log-probabilities -21.410 and -25.295 from the published 414.7/460.8 norm inputs and returns 99.573 bits, 0.117 bits below the published 99.69 and inside the declared 0.2-bit tolerance.

## Independent BLS12 finite-size regression

[CITED] The BLS12 worked row uses `h=t^6-t-1`, `f=P(x^2+t+t^2+t^4+1)`, `g=x^2+t+t^2+t^4+1-u`, `u=-2^77+2^50+2^33`, coefficient bound 1169, and `log2(B)=73.5`; it reports norm sizes 791.2/584.8 and security 131.8 bits (Barbulescu--Duquesne 2019, Section 7.1.2).

[PROVED] `code/sample_bls12_norms.py` samples all twelve coefficients independently and uniformly from the inclusive integer interval `[-A,A]`, computes both nested resultants exactly over the integers, rejects zero norms, and records every sampled coefficient and exact norm.

[EMPIRICAL: 1,024 exact samples, RNG seed 20260722] Mean integer bit lengths are 791.083 on the `f` side and 584.756 on the `g` side. Their normal 95% intervals are `[789.720,792.446]` and `[584.369,585.143]`, both containing the paper's 791.2/584.8 values.

[EMPIRICAL: same sample] Mean real logarithms are 790.593 and 584.253. The approximately half-bit difference shows that the printed paper values follow the integer-bit-length convention despite the surrounding prose describing average logarithms; both metrics are preserved in the JSON artifact.

[EMPIRICAL: same sample and fixed BD19 cost parameters] The sampled means imply smoothness log-probabilities -39.162/-24.668, 69.470 expected relation bits, and 131.789 total cost bits. The published norm inputs independently give -39.171/-24.671, 69.459 relation bits, and 131.800 total cost bits.

[PROVED] No prefactor or overhead was refitted for the BLS12 regression; the finite equation and constants are the same named implementation used by the BN test.

## Cross-family norm and finite-cost audit

[CITED] The authors' surviving public sampler calls Python `randint(-A,A+1)`. Because both endpoints are inclusive, that code draws from `[-A,A+1]`, not the paper's stated `[-A,A]` domain. Both conventions are therefore preserved as separate deterministic experiments rather than silently merged.

[PROVED] `code/sample_family_norms.py` implements the exact published nested-resultant constructions for the BN Section 7.1.1, KSS16 Section 7.1.3, and BLS24 Section 7.2.2 rows. `code/compare_norm_regressions.py` combines those records with the BLS12 run without changing any sampled result.

| Profile and draw convention | Samples | mean norm bits `f/g` | printed norm bits | sampled cost | printed cost |
|---|---:|---:|---:|---:|---:|
| BLS12-128, paper domain | 1,024 | 791.083 / 584.756 | 791.2 / 584.8 | 131.789 | 131.8 |
| BN-128, paper domain | 512 | 554.373 / 809.398 | 557.0 / 808.9 | 131.326 | 131.3 |
| BN-128, public-code bound | 512 | 554.320 / 809.625 | 557.0 / 808.9 | 131.335 | 131.3 |
| KSS16-128, paper domain | 512 | 911.504 / 628.463 | 920.4 / 628.9 | 138.153 | 139.0 |
| KSS16-128, public-code bound | 512 | 921.818 / 629.650 | 920.4 / 628.9 | 138.880 | 139.0 |
| BLS24-192, paper domain | 512 | 1241.572 / 1455.863 | 1295 / 1460 | 201.255 | 203.72 |
| BLS24-192, public-code bound | 512 | 1262.322 / 1457.418 | 1295 / 1460 | 201.803 | 203.72 |
| BLS24-192, public-code bound with sampling `A=10` | 128 | 1295.867 / 1461.000 | 1295 / 1460 | 203.171 | 203.72 |

[EMPIRICAL: checked-in seeded samples] BLS12 and BN sampled costs agree with their printed rows within 0.04 bits. The public-code convention reduces the KSS16 discrepancy from 0.85 to 0.12 bits. With the printed BLS24 bound `A=9`, both stated conventions remain too low; the public-code run is 1.92 bits below the printed cost.

[EMPIRICAL: preregistered BLS24 sensitivity, RNG seed 20260724] Changing only the coefficient draw bound from 9 to 10 places both printed norm values inside the 95% intervals and reduces the cost discrepancy to 0.55 bits. This supports, but does not prove, the inference that the historical run used a rounded internal bound near 10 before the public code applied its extra upper endpoint. The unavailable historical setting is recorded as non-blocking Q027 rather than tuned away.

## Family validation and exhaustive toy search

[CITED] The BN, BLS12, BLS24, and KSS16 polynomials implemented in `lib/curves.py` are the parameterizations restated by Barbulescu and Duquesne (2019, Sections 2.1--2.3).

[EMPIRICAL: BN `u=-2`, BLS12 `u=-2`, BLS24 `u=-5`] The prime toy fixtures satisfy `r | p+1-t` and have least embedding degrees 12, 12, and 24; `lib/tests/test_pairing_families.py` performs the independent modular checks.

[EMPIRICAL: published BLS12-381 constants] Evaluation at `u=-0xd201000000010000` matches the published 381-bit `p` and 255-bit `r` exactly and has least embedding degree 12 (Bowe 2017).

[EMPIRICAL: every integer seed `-10000 <= u <= 10000`, `p < 2^60`] The bounded sweep accepts 273 BN, 24 BLS12, five BLS24, and zero KSS16 candidates after deterministic primality, order-divisibility, and least-embedding-degree checks; all 302 rows are stored in `data/search_families_m10000_10000_20260626.csv`.

[EMPIRICAL: those 302 rows] No row meets a production target: the largest generic-group estimate is only 29.153 bits.

## Complete KSS16 toy-ceiling certificate

[PROVED] Let `N(u)` be the numerator of the KSS16 field polynomial and `x=|u|`. For `x>=256`, triangle inequality gives

`N(u) >= x^6 (x^4 - 2x^3 - 5x^2 - 6588)`.

[PROVED] The right-hand side is positive and increasing for `x>=256`; its value at 256 is greater than `980*2^60`. Therefore every integral KSS16 seed with `p=N(u)/980 < 2^60` lies in `[-255,255]`.

[PROVED] `code/certify_kss16_ceiling.py` exhausts all 511 integers in that interval. Exactly eight seeds produce positive integral family parameters below the ceiling: `-115,-95,-45,-25,25,45,95,115`.

[PROVED] Exact factorizations in `data/kss16_p_lt_2pow60_certificate_20260715.json` show that none of those eight rows has both `p` and `r` prime. Thus no valid KSS16 prime-pair fixture exists under the scaffold ceiling.

## Extrapolated optimization tables

[HEURISTIC] Every row below uses only family-polynomial degrees and leading coefficients. `minimum log2|u|` is a continuous size threshold, not a concrete seed, and primality is neither tested nor claimed.

| Target | Family | minimum `log2|u|` | estimated `p` bits | estimated `r` bits | rho estimate | field/Pollard bits | proxy |
|---:|---|---:|---:|---:|---:|---:|---:|
| 128 | **BN** | 109.439 | 442.925 | 442.925 | **1.0000** | 128.0 / 221.5 | 1344 |
| 128 | BLS12 | 74.085 | 442.925 | 296.340 | 1.4947 | 128.0 / 148.2 | 889 |
| 128 | BLS24 | 32.000 | 318.415 | 256.000 | 1.2438 | 150.4 / 128.0 | 768 |
| 128 | KSS16 | 34.213 | 332.194 | 257.802 | 1.2886 | 128.0 / 128.9 | 547 |
| 192 | **BN** | 278.334 | 1118.508 | 1118.508 | **1.0000** | 192.0 / 559.3 | 3371 |
| 192 | BLS12 | 186.682 | 1118.508 | 746.728 | 1.4979 | 192.0 / 373.4 | 2240 |
| 192 | BLS24 | 56.084 | 559.254 | 448.671 | 1.2465 | 192.0 / 224.3 | 1346 |
| 192 | KSS16 | 84.882 | 838.881 | 663.152 | 1.2650 | 192.0 / 331.6 | 1358 |
| 256 | **BN** | 550.941 | 2208.935 | 2208.935 | **1.0000** | 256.0 / 1104.5 | 6642 |
| 256 | BLS12 | 368.420 | 2208.935 | 1473.680 | 1.4989 | 256.0 / 736.8 | 4421 |
| 256 | BLS24 | 110.605 | 1104.468 | 884.842 | 1.2482 | 256.0 / 442.4 | 2655 |
| 256 | KSS16 | 166.664 | 1656.702 | 1317.408 | 1.2575 | 256.0 / 658.7 | 2667 |

[PROVED] Within this four-family leading-term model, BN is the unique minimum-rho row at every target because its estimated `p` and `r` sizes are equal, while each competing row has strictly larger estimated `p` size than `r` size.

## Sensitivity and practical meaning

| Target | calibrated SexTNFS `c=32` field bits | o(1)-less SexTNFS `c=32` field bits | composite exTNFS `c=48` field bits | rho optimum |
|---:|---:|---:|---:|---|
| 128 | 5315 | 5004 | 3618 | BN |
| 192 | 13422 | 12870 | 9241 | BN |
| 256 | 26507 | 25666 | 18348 | BN |

[EMPIRICAL: three named scenarios and three targets] The family label does not move, but the predicted required field size changes by about 45--47% between the calibrated special-form and composite-exTNFS scenarios. The full 36-row table is `data/optimization_extrapolated_20260715.csv`.

[PROVED] This label stability is caused by the formal minimum-rho objective, not by stable security estimation; minimizing rho alone rewards BN even when its required base field and pairing proxy are much larger.

[CITED] Practical 128-bit and 192-bit recommendations consider arithmetic and pairing costs in a wider family space and therefore favor BLS12, BLS24, or other alternatives in cases where a rho-only ranking chooses BN (Guillevic 2020; Aranha--Fotiadis--Guillevic 2024).

[PROVED] Those recommendations do not contradict this result: they optimize a different objective, while the P4.1 primary table minimizes rho and uses a deterministic Miller-scalar-size proxy only as a tie-breaker.

## Scope and conclusion

[PROVED] The search tool delivers an optimum with proof inside the explicitly stated four-family leading-term model for each requested target and each named cost scenario.

[HEURISTIC] The production-size optimization rows remain model extrapolations rather than concrete prime-seed recommendations. Exact finite-size regressions now cover BN, BLS12, KSS16, and BLS24, while the BLS24 audit also demonstrates that coefficient-bound conventions can move a printed estimate by multiple bits.

[PROVED] The result is not a theorem over every pairing-friendly construction in the Freeman--Scott--Teske taxonomy; adding MNT, KSS18, Cocks--Pinch, Brezing--Weng, or implementation-level operation costs would define a larger optimization problem.
