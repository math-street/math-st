# P3.1 experiment code

## `measure_quaternary_prime_sampler.py`

- [PROVED] The script enumerates the rank-four residue sublattice used in attempt A003 for toy primes \(p\equiv3\pmod4\), checks its known discriminant \((8\ell)^6p^2\), and measures prime-valued vector density and admissible-progression coverage.
- [PROVED] `--smoke` uses \(p\in\{7,11\}\), \(\ell=3\), cutoff 1000, and completes in under ten seconds on the recorded environment.
- [EMPIRICAL: p<=31, ell in {3,5}, q<=3000] The 22-case grid took 27.84 seconds; the prime-density statistic multiplied by \(\log X\) ranged from 0.832 to 1.815 and had mean 1.276. Data: `../data/measure_quaternary_prime_sampler_p31_ells3-5_x3000_20260711.csv`.
- [EMPIRICAL: p in {7,11}, ell=3, 250<=q<=4000] Five cutoff files record the small-scale approach of the scaled prime density toward a value near one.

## `toy_deuring_roundtrip.py`

- [PROVED] The script evaluates the special-order generators \(i\) and \(j\) as the automorphism \(\iota\) and Frobenius on \(E:y^2=x^3-x\), converts a norm-\(\ell\) ideal into its torsion kernel, applies a Velu step, and recovers the original ideal.
- [PROVED] It computes the exact embedded right order, checks its trace discriminant, and matches it to the quotient `deuring_key`.
- [PROVED] It constructs the dual kernel from the image of \(E[\ell]\), checks \(I\bar I=\ell O\), and validates that the two degree-\(\ell\) steps return to the source `deuring_key` with degree product \(\ell^2\).
- [PROVED] The validated fixture is \(p=11\), \(\ell=3\), where \(\#E(\mathbb F_{p^2})=144\), the nonzero rational 3-torsion has eight points, and exactly four norm-3 neighbor ideals occur.
- [EMPIRICAL: p=11, ell=3, 30 independent seeds] The separately named validation run records 30/30 ideal, embedded-right-order, dual-ideal-product, and terminal-curve matches, covering all four neighbor ideals and two intermediate target curve classes. Data: `../data/toy_deuring_roundtrip_p11_ell3_trials30_20260711.csv`.

## `fit_roundtrip_cost.py`

- [PROVED] The script fits `seconds_per_trial` to a power law in \(p\) by ordinary least squares in logarithmic coordinates and stores the fitted exponent, its classical 95% interval, and per-size residuals.
- [PROVED] The fit implementation is validated against the exact synthetic relation \(t=2p^{3/2}\); `--smoke` fits three recorded rows in under one second without overwriting the five-row result.
- [EMPIRICAL: p in {11,23,47,59,71}, ell=3, n=5] The right-order-aware two-step fit has exponent 1.6796, classical 95% interval \([1.2366,2.1226]\), and \(R^2=0.9798\); it measures exhaustive toy code, not the cryptographic reduction.
