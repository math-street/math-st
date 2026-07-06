# P4.3 code

## `measure_norm_smoothness.py`

- [PROVED] The fixed toy instance uses $p=5$, $h(t)=t^2+2$, $f(x)=x^3+x+1$, and $g(x)=x^3+x-4$; $h$ and the common reduction of $f,g$ are irreducible modulo $5$, while $f\equiv g\pmod 5$.
- [PROVED] For $a,b\in\mathbb{Z}[\iota]$, $\iota^2=-2$, the script computes the actual exTNFS norm $|\operatorname{Res}_t(\operatorname{Res}_x(a-bx,f),h)|$ and its $g$-side analogue by exact integer arithmetic.
- [PROVED] Every actual norm and every matched baseline integer is completely factored by deterministic trial division before smoothness is recorded.
- [PROVED] Conditional on each candidate's two observed norm magnitudes, the baseline draws are independent across sides and uniform in the corresponding dyadic intervals, so bit sizes are matched candidate by candidate.  Aggregate baseline smoothness indicators may still correlate because both interval sizes depend on the same coefficient vector.

Run the sub-ten-second validation:

```powershell
python problems/P4.3-rigorous-extnfs/code/measure_norm_smoothness.py --smoke
```

Run the recorded exhaustive box:

```powershell
python problems/P4.3-rigorous-extnfs/code/measure_norm_smoothness.py --a-bound 4 --bounds 7,13,31,61 --seed 4304
```

[EMPIRICAL: p=5, A=4, 5,856 primitive pairs] The full command took about 0.6 seconds on Python 3.13 in the recorded environment; see the dated summary CSV for measured densities and Wilson intervals for the random baseline.
