# P2.4 code

- [EMPIRICAL: six toy curves] `measure_pairing_stages.py` validates the staged pairing, enumerates final and Miller fibres, and times four direct inversion strategies. Default output is a dated CSV under `../data/`; `--smoke` finishes in under one second.
- [EMPIRICAL: \(p=43,r=11\)] `analyze_miller_function.py` expands the published fixed-argument Miller function in the curve coordinate ring, validates it at all ten nonidentity \(G_2\) points, and records factor-degree growth for odd orders 3 through 41.
- [EMPIRICAL: Satoh Example 4.4 and 82 raw targets] `reproduce_satoh_mi.py` reproduces Satoh's published degree-two Miller-inversion example and exhaustively validates the distortion-map transfer for the fixed-base `FAPI-1` raw Miller orientation.
- [EMPIRICAL: small prime orders] `verify_generic_oracle_bound.py` exhausts or reproducibly samples affine-form sets and checks the collision union bound used by A002.
- `tests/test_measure_pairing_stages.py` checks the published \(p=43,r=11\) fibre sizes and non-degeneracy.
- `tests/test_analyze_miller_function.py` checks the exact symbolic vector and the \((r-2,r-3)\) factor-degree sequence.
- `tests/test_reproduce_satoh_mi.py` checks the published Satoh vector and the full \(p=43\) raw-target transfer.

Reproduce the recorded data from the repository root:

```powershell
python problems\P2.4-pairing-inversion\code\analyze_miller_function.py --seed 2404 --trials 1
python problems\P2.4-pairing-inversion\code\measure_pairing_stages.py --p 43 --p 59 --p 83 --p 103 --p 131 --p 163 --trials 50 --seed 2404
python problems\P2.4-pairing-inversion\code\reproduce_satoh_mi.py --p 43 --p 59 --p 83 --p 103 --p 131 --p 163 --trials 50 --seed 2404
python problems\P2.4-pairing-inversion\code\verify_generic_oracle_bound.py --p 5 --p 7 --p 11 --trials 10000 --seed 2404
python -m unittest discover -s problems\P2.4-pairing-inversion\code\tests -v
```

[EMPIRICAL: Python 3.13.4] The original six-curve stage measurement took 16.6 seconds, and the standalone Satoh reproduction took 3.0 seconds. All four scripts use only the standard library and shared repository modules.

[EMPIRICAL: Python 3.13.4] The standalone affine-collision audit took 0.9 seconds for \(p\in\{5,7,11\}\), \(t\le4\), and 10,000 seeded non-exhaustive trials.
