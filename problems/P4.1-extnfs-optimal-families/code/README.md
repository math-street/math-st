# P4.1 code

## `search_families.py`

[PROVED] `toy` mode enumerates every integer seed in the requested inclusive interval and accepts a row only after deterministic primality, curve-order divisibility, and least-embedding-degree checks.

[HEURISTIC] `extrapolate` mode replaces each family polynomial by its degree and leading coefficient, then applies a selected o(1)-less TNFS model. Its output is a size-model optimization, not a list of concrete production seeds.

```powershell
python problems/P4.1-extnfs-optimal-families/code/search_families.py --smoke
python problems/P4.1-extnfs-optimal-families/code/search_families.py
```

## `sample_bls12_norms.py`

[PROVED] Each row contains the exact integer
`abs(Res_t(Res_x(a(t)-x*b(t), f(t,x)), h(t)))` on both sides of the BLS12 SexTNFS construction in Barbulescu--Duquesne Section 7.1.2.

[EMPIRICAL: Windows 11, Python 3.13.4, RNG seed 20260722] The checked-in 1,024-sample run reproduces the paper's 791.2/584.8 norm-size inputs with mean integer bit lengths 791.083/584.756 and produces a 131.789-bit finite-cost estimate.

```powershell
python problems/P4.1-extnfs-optimal-families/code/sample_bls12_norms.py --smoke
python problems/P4.1-extnfs-optimal-families/code/sample_bls12_norms.py --samples 1024
```

[PROVED] The JSON reports both `mean(log2(N))` and `mean(N.bit_length())`. This distinction is necessary because the printed paper values match the latter convention, with an expected offset of roughly half a bit from the former.

## `certify_kss16_ceiling.py`

[PROVED] For every integer KSS16 seed with generated field prime candidate `p < 2^60`, the script either rejects non-integral family values or records exact factorizations. An analytic magnitude bound reduces the infinite seed set to the 511 integers in `[-255,255]`.

```powershell
python problems/P4.1-extnfs-optimal-families/code/certify_kss16_ceiling.py
```

[PROVED] The resulting certificate contains eight integral below-ceiling parameter sets and zero prime `(p,r)` pairs.

## `sample_family_norms.py`

[PROVED] This sampler implements the exact BN-128, KSS16-128, and BLS24-192 polynomial/tower selections printed in Barbulescu--Duquesne Sections 7.1.1, 7.1.3, and 7.2.2. Every CSV row retains the coefficient tuples and both exact integer nested resultants.

```powershell
python problems/P4.1-extnfs-optimal-families/code/sample_family_norms.py --smoke
python problems/P4.1-extnfs-optimal-families/code/sample_family_norms.py --profiles bn-128 kss16-128 bls24-192 --samples 512 --distribution paper-code
```

`--distribution exact-domain` uses the paper's stated inclusive `[-A,A]` domain. `--distribution paper-code` reproduces the surviving public source's inclusive `randint(-A,A+1)`, hence `[-A,A+1]`. `--sampling-bound` is an explicit one-profile sensitivity override; it never changes the printed `A` retained by the finite-cost calculation.

The preregistered BLS24 sensitivity can be reproduced with:

```powershell
python problems/P4.1-extnfs-optimal-families/code/sample_family_norms.py --profiles bls24-192 --samples 128 --rng-seed 20260724 --distribution paper-code --sampling-bound 10 --date 20260722
```

## `compare_norm_regressions.py`

[PROVED] The comparison script loads the checked-in BLS12, BN, KSS16, and BLS24 sample reports and writes one eight-row CSV/JSON audit. It reports mismatches and the BLS24 sensitivity separately; it does not recalibrate samples.

```powershell
python problems/P4.1-extnfs-optimal-families/code/compare_norm_regressions.py --date 20260722
```
