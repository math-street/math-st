# P5.4 code

## `validate_rfc_maps.py`

Exhaustively compares the shared straight-line SSWU and Elligator 2
implementations with separately structured, branch-using RFC formula oracles.

```powershell
python problems\P5.4-hash-to-curve\code\validate_rfc_maps.py --smoke
python problems\P5.4-hash-to-curve\code\validate_rfc_maps.py
```

- [EMPIRICAL: $p\in\{11,13,29,37\}$, all inputs] The full run validated 180 map inputs, with every output on-curve and equal to its oracle output.
- [EMPIRICAL: same range] Every fixed fixture had one schedule variant, including 6 direct-SSWU exceptional inputs and 2 Elligator 2 exceptional inputs.
- [EMPIRICAL: Python 3.13.4 on Windows 11] The recorded full run took 0.001352 seconds, excluding process startup.

The deterministic result is
`data/validate_rfc_maps_p11-13-29-37_20260704.csv`.

## `measure_map_timing.py`

Measures every input of the fixed $p=11$ fixtures in randomized blocks, then
compares exceptional and ordinary inputs with a paired-round percentile
bootstrap.

```powershell
python problems\P5.4-hash-to-curve\code\measure_map_timing.py --smoke
python problems\P5.4-hash-to-curve\code\measure_map_timing.py
```

- [EMPIRICAL: Python 3.13.4, 240 rounds, batch 100, seed 5402] Elligator 2 had a mean ratio of 1.01162 with 95% CI $[0.99911,1.02450]$.
- [EMPIRICAL: same run] SSWU had a mean ratio of 0.99121 with 95% CI $[0.98059,1.00210]$.
- [EMPIRICAL: same run] The full measurement and 2,000 paired bootstrap resamples completed in 1.478962 seconds, excluding process startup.
- [PROVED] These measurements characterize this Python run only and do not certify a compiled constant-time backend.

Raw observations and summaries are in
`data/measure_map_timing_p11_s240_b100_seed5402_20260704_{raw,summary}.csv`.

## `validate_svdw.py`

Exhausts the RFC SvdW fallback on ordinary, $j=0$, and $j=1728$ fixtures.

```powershell
python problems\P5.4-hash-to-curve\code\validate_svdw.py --smoke
python problems\P5.4-hash-to-curve\code\validate_svdw.py
```

- [EMPIRICAL: 12 fixtures, all 270 inputs] Every output was on-curve, equal to the independent oracle, and part of one fixed-fixture schedule.
- [EMPIRICAL: Python 3.13.4] The recorded full run took 0.002856 seconds, excluding startup.

## `search_exceptional_isogenies.py`

Enumerates every rational 3/5-subgroup of every nonsingular $AB\ne0$ curve over the requested toy primes.

```powershell
python problems\P5.4-hash-to-curve\code\search_exceptional_isogenies.py --smoke
python problems\P5.4-hash-to-curve\code\search_exceptional_isogenies.py
```

- [EMPIRICAL: primes $5\le p<100$] The full run checked 62,664 curves and 45,166 kernels and wrote 1,492 exceptional-invariant targets.
- [EMPIRICAL: Python 3.13.4] The recorded full run took 11.026610 seconds; smoke mode took 0.032785 seconds.

## `validate_isogeny_workarounds.py`

Checks the selected $j=0$ and $j=1728$ SSWU-to-isogeny paths, including exact kernels and all source group-law pairs.

```powershell
python problems\P5.4-hash-to-curve\code\validate_isogeny_workarounds.py --smoke
python problems\P5.4-hash-to-curve\code\validate_isogeny_workarounds.py
```

- [EMPIRICAL: fixed $p=29$ and $p=59$ paths] All 88 SSWU inputs avoided the kernels and all 4,500 homomorphism pairs passed.
- [EMPIRICAL: Python 3.13.4] The recorded full run took 0.004689 seconds.

## `validate_hash_pipeline.py`

Validates RFC XMD anchors and exhausts the two-map sum plus cofactor clearing for six short-Weierstrass suites.

```powershell
python problems\P5.4-hash-to-curve\code\validate_hash_pipeline.py --smoke
python problems\P5.4-hash-to-curve\code\validate_hash_pipeline.py
```

- [PROVED] Two RFC 9380 Appendix K.1 SHA-256 XMD vectors pass.
- [EMPIRICAL: all 8,982 field pairs] Every output landed in the declared order-three or order-five subgroup and every subgroup point occurred.
- [EMPIRICAL: Python 3.13.4] The recorded full run took 0.157056 seconds.

## `validate_curve_transports.py`

Checks direct Montgomery Elligator 2, Elligator-to-Edwards transport, and generic SvdW-to-Montgomery transport.

```powershell
python problems\P5.4-hash-to-curve\code\validate_curve_transports.py --smoke
python problems\P5.4-hash-to-curve\code\validate_curve_transports.py
```

- [EMPIRICAL: $p=7$ and $p=11$, all 25 registered map inputs] Every transport matched its independent oracle and stayed on the target curve.
- [EMPIRICAL: two $p=7$ pipelines, all 98 field pairs] Cofactor clearing stayed in the declared order-three subgroup.
- [EMPIRICAL: Python 3.13.4] The final full run took 0.018224 seconds.

## `measure_extended_timing.py`

Measures six SvdW, isogeny, and form-transport input partitions in randomized full-field rounds.

```powershell
python problems\P5.4-hash-to-curve\code\measure_extended_timing.py --smoke
python problems\P5.4-hash-to-curve\code\measure_extended_timing.py
```

- [EMPIRICAL: Python 3.13.4, 160 rounds, batch 80, seed 5408] Mean ratios ranged from $0.965472$ to $0.995130$; every paired-bootstrap interval intersected the preregistered $[0.8,1.25]$ band.
- [EMPIRICAL: same run] The full measurement took 15.726984 seconds.
- [PROVED] Two unadjusted intervals excluded one by a few percent; neither this nor the fixed schedules certifies a constant-time backend.

## Library module

- [PROVED] `hash_pipeline.py` contains the RFC-shaped SHA-256 XMD, prime-field `hash_to_field`, compile-time short-Weierstrass suite family, and toy Montgomery/Edwards pipelines.
- [PROVED] It is correctness and composition code, not a production constant-time cryptographic library.

## `validate_extension_svdw.py`

Exhausts generic SvdW over a true cubic extension and compares against a branch-using candidate/root oracle.

```powershell
python problems\P5.4-hash-to-curve\code\validate_extension_svdw.py --smoke
python problems\P5.4-hash-to-curve\code\validate_extension_svdw.py
```

- [EMPIRICAL: $\mathbb F_{7^3}$, all 343 inputs] All outputs matched the oracle, were on-curve, and shared one recorded schedule; all 342 nonzero elements passed inversion checks.
- [EMPIRICAL: Python 3.13.4] The recorded run took 0.725829 seconds.

## `validate_small_characteristic.py`

Validates the cited characteristic-three and odd-degree binary encodings, plus the preregistered out-of-scope characteristic-three SvdW algebraic probe.

```powershell
python problems\P5.4-hash-to-curve\code\validate_small_characteristic.py --smoke
python problems\P5.4-hash-to-curve\code\validate_small_characteristic.py
```

- [EMPIRICAL: $\mathbb F_3$ and $\mathbb F_{2^n}$ for $n=3,5,7$, 174 inputs] Every output passed its registered oracle or algebraic probe and curve-membership test with one schedule.
- [EMPIRICAL: binary fixtures] The maximum observed preimage size was six, and all 17,472 fixed-loop multiplication results matched the branch-using field oracle.
- [EMPIRICAL: Python 3.13.4] The recorded full run took 0.245098 seconds.

## `validate_extension_pipeline.py`

Builds the full cubic-extension group, exhausts masked complete addition, and checks every two-map/cofactor-64 pair using validated Cayley tables.

```powershell
python problems\P5.4-hash-to-curve\code\validate_extension_pipeline.py --smoke
python problems\P5.4-hash-to-curve\code\validate_extension_pipeline.py
```

- [EMPIRICAL: $\mathbb F_{7^3}$] All 102,400 ordered group pairs and 117,649 field pairs passed oracle, order-five subgroup, support, and schedule checks.
- [EMPIRICAL: Python 3.13.4] The full run took 11.145540 seconds; smoke mode took 0.076104 seconds.

## `validate_compiled_backend.py`

Compiles the specialized Rust backend, exhausts its maps/group law/two-map pipeline against Python, and audits optimized assembly.

```powershell
python problems\P5.4-hash-to-curve\code\validate_compiled_backend.py --smoke
python problems\P5.4-hash-to-curve\code\validate_compiled_backend.py
```

- [EMPIRICAL: rustc 1.93.1, x86-64 Windows] All 11 maps, 144 ordered group pairs, and 121 hash pairs matched; all hash outputs passed the order-three subgroup check.
- [EMPIRICAL: same build] The audited exported functions contained no integer divide and no non-loop conditional jump; source secret paths contained no branch or indexed access.

## `validate_small_characteristic_pipelines.py`

Exhausts masked complete group laws and two-map/cofactor pipelines for the characteristic-three and binary fixtures.

```powershell
python problems\P5.4-hash-to-curve\code\validate_small_characteristic_pipelines.py --smoke
python problems\P5.4-hash-to-curve\code\validate_small_characteristic_pipelines.py
```

- [EMPIRICAL: four groups] All 20,853 ordered group pairs matched branch-using oracles.
- [EMPIRICAL: all 17,481 field pairs] Every pipeline matched its oracle, landed in the declared prime-order subgroup, reached every subgroup point, and used one schedule per fixture.
- [EMPIRICAL: Python 3.13.4] The full run took 13.831443 seconds; smoke mode took 0.016523 seconds.

## `measure_compiled_timing.py`

Runs randomized-order paired timing rounds inside the compiled backend and reports a paired bootstrap interval plus a paired sign-permutation test.

```powershell
python problems\P5.4-hash-to-curve\code\measure_compiled_timing.py --smoke
python problems\P5.4-hash-to-curve\code\measure_compiled_timing.py
```

- [EMPIRICAL: 400 rounds, batch 1,000, seed 5409] The fixed-pair ratio was $1.000555$, its 95% interval was $[0.998811,1.002232]$, and permutation $p=0.524248$.
- [PROVED] This is a leakage screen for one compiled toy target, not a portable constant-time certificate.

## Tests

```powershell
python -m unittest discover -s problems\P5.4-hash-to-curve\code\tests -v
```

The tests include fixed known outputs, RFC XMD vectors, exhaustive square-root
checks, independent-oracle comparisons, isogeny/group-law checks, subgroup
clearing, model transports, invalid-applicability rejection, exceptional
cases, schedule invariance, source auditing, and timing-helper smoke checks.
