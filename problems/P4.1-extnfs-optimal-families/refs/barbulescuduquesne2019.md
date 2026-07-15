# Barbulescu--Duquesne 2019

[CITED] Razvan Barbulescu and Sylvain Duquesne, "Updating Key Size Estimations for Pairings," *Journal of Cryptology* 32(4), 1298--1336, 2019, doi:10.1007/s00145-018-9280-5; IACR ePrint 2017/334.

## Main results used here

[CITED] The paper gives explicit finite-size relation-collection and sparse-linear-algebra equations for SexTNFS, estimates average norm sizes by Monte Carlo sampling, and optimizes the sieve coefficient and smoothness bounds (Section 4).

[CITED] Its worked BN instance at `u=-2^62-2^55-1` reports average norm sizes 414.7 and 460.8 bits, smoothness-bound bit size 57, and total cost 99.69 bits (Section 5.2).

[CITED] Its Section 2 gives the BN, BLS12, BLS24, and KSS16 parameterizations implemented by `lib/curves.py`.

[CITED] Section 3.1 defines each norm as the nested resultant `Res_t(Res_x(a(t)-x*b(t), f(t,x)), h(t))`; Section 4.2 samples 25,600 coefficient tuples uniformly from `[-A,A]`.

[CITED] The BLS12 row in Section 7.1.2 uses `u=-2^77+2^50+2^33`, `h=t^6-t-1`, the stated quadratic tower substitution, coefficient bound 1169, and smoothness-bound bit size 73.5. It reports norm sizes 791.2/584.8 and security 131.8 bits.

[CITED] The KSS16 Section 7.1.3 row reports coefficient bound 12, norm sizes 920.4/628.9, and security 139.0 bits. The BLS24 Section 7.2.2 row uses `h=t^24+t^4-t^3-t-1`, coefficient bound 9, norm sizes 1295/1460, and security 203.72 bits.

[CITED] The authors' public scripts page is `https://razvanbarbulescu.pages.math.cnrs.fr/Pairings/Pairings.html`; its surviving `compute_distribution.py` calls inclusive Python `randint(-A,A+1)`, so the implementation samples `[-A,A+1]` although Section 4.2 states `[-A,A]`.

## Assumptions and interpretation

[CITED] The paper sets the basic sieving-cost constant to one and derives Dickman probabilities from sampled norm sizes (Section 4.2).

[EMPIRICAL: P4.1 exact sampler] The printed BLS12 norm values agree with mean integer bit lengths, while mean real logarithms are roughly half a bit lower. The repository records both conventions rather than silently choosing one.

[EMPIRICAL: P4.1 cross-family audit] The public-code coefficient convention closely reproduces BN and KSS16. Printed BLS24 `A=9` remains low, while a preregistered draw-bound-10 sensitivity reproduces both printed norms within one bit. This supports an internal-rounding explanation but does not recover the unavailable historical setting.

## What it leaves open

[CITED] Norm sizes depend on polynomial selection and are not functions only of `(p,k)`; applying the finite estimate to another family still requires its polynomial/tower construction and simulation (Sections 3--4).

[HEURISTIC] The surviving paper, script, and parameter archive do not uniquely identify the historical BLS24 integer draw bound; this non-blocking reproducibility gap is Q027.
