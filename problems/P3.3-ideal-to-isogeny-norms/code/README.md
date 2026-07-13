# P3.3 code

## `measure_norm_gap.py`

[PROVED] The script samples integral prime-norm left ideals in the explicit
maximal order supported by `lib/quaternion.py`, applies exact norm-aware LLL,
certifies the shortest vector by inverse-Gram bounded enumeration, constructs
the corresponding equivalent ideal, and writes raw data, grouped summaries,
scaling residuals, and SVG/PNG plots. `--ell-policy near-p` removes the
trivial fixed-small-input-norm cap; it does not claim class-group uniformity.

Run the under-10-second smoke test from the repository root:

```powershell
python problems\P3.3-ideal-to-isogeny-norms\code\measure_norm_gap.py --smoke --output-root tmp\p33-smoke
```

Run the recorded 108-instance corrected experiment:

```powershell
python problems\P3.3-ideal-to-isogeny-norms\code\measure_norm_gap.py --primes 2203 2503 2803 3119 3467 3719 560083 640007 720019 800119 880027 960031 145000043 165000023 185000027 205000007 225000011 245000047 --trials-per-p 6 --seed 33032028 --ell-policy near-p
```

## `measure_shape_gap.py`

[PROVED] The script exactly enumerates normalized norms with an
inverse-Gram-certified box and overflow-checked NumPy int64 blocks. It records
the least represented power of 2, power of 3, and 5-smooth norm, constructs
each equivalent ideal witness, and checks its norm and left closure.

```powershell
python problems\P3.3-ideal-to-isogeny-norms\code\measure_shape_gap.py --smoke --output-root tmp\p33-shape-smoke
python problems\P3.3-ideal-to-isogeny-norms\code\measure_shape_gap.py
```

## `measure_power_targets.py`

[PROVED] The script scans only increasing powers of 2 and 3. It certifies each
target with inverse-Gram coefficient bounds, uses vectorized exact integer
evaluation for boxes through `--max-box`, and switches larger boxes to exact
quadratic coordinate elimination. `--max-box` is a strategy threshold, not a
censoring limit. Every witness is converted to an equivalent ideal and checked
for its norm and left closure.

```powershell
python problems\P3.3-ideal-to-isogeny-norms\code\measure_power_targets.py --smoke --output-root tmp\p33-power-smoke
python problems\P3.3-ideal-to-isogeny-norms\code\measure_power_targets.py
```

The recorded full run replays the 18-prime, six-trial A002 seed and scans
targets through $4p$.

Run its tests:

```powershell
python -m unittest discover -s problems\P3.3-ideal-to-isogeny-norms\code\tests -p 'test_*.py' -v
```

[EMPIRICAL: Windows 11, Python 3.13.4] The corrected 108-instance norm-gap run
took 13.17 seconds and exact SVP averaged 0.00453 seconds per row. Shape smoke
took 0.97 seconds; the 70-instance exact shape run took 21.20 seconds. The
108-instance sparse pure-power run took 43.53 seconds with no censored rows.
