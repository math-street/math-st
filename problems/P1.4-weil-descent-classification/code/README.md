# P1.4 code

## Commands

Run the problem-local tests:

```powershell
python -m unittest discover -s problems/P1.4-weil-descent-classification/code/tests -v
```

Reproduce the published genus-31 regression:

```powershell
python problems/P1.4-weil-descent-classification/code/verify_published_example.py
```

Regenerate the complete census, summaries, and plot:

```powershell
python problems/P1.4-weil-descent-classification/code/sweep_ghs_genus.py --degrees 4 6 8 --date 20260722
```

Both command-line scripts accept `--smoke` and finish in under ten seconds on the recorded environment.

## Files

- `ghs.py`: binary Gaussian elimination, Frobenius orbits and annihilators, and the exact GHS profile.
- `sweep_ghs_genus.py`: exhaustive parameter sweep, invariant checks, CSV summaries, and SVG plot.
- `verify_published_example.py`: independent reconstruction of the Magma V2.19.8 H42E45 genus-31 example.
- `tests/`: known-answer and invariant tests for every script and core routine.

## Mathematical basis

[CITED] The magic number follows Gaudry–Hess–Smart (2002), and the exact genus branch follows Hess (2003). See `../refs/` and `../RESULTS.md`.
