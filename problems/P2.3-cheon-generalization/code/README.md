# Code — P2.3

- `cheon.py` implements the two-stage \(d\mid n-1\) recovery over a minimal
  scalar-multiplication group interface. It also supplies an opaque cyclic
  group simulator whose counters distinguish scalar-multiplication calls from
  primitive double-and-add group operations.
- `run_scaling.py` selects primes \(n=2^m e+1\) with odd \(e\) near \(2^m\),
  runs seeded recovery trials, and writes row-level data, size summaries,
  residuals, and a bootstrap confidence interval for the log-log slope.
- `tests/test_cheon.py` exhaustively checks three simulated prime-order groups
  and the concrete order-19 elliptic-curve group from `lib/tests/test_dlog.py`.

Run the tests from the repository root:

```powershell
python -m unittest discover -s problems/P2.3-cheon-generalization/code/tests -v
```

Run a sub-10-second smoke experiment:

```powershell
python problems/P2.3-cheon-generalization/code/run_scaling.py --smoke
```

Run the predeclared SG-02 experiment:

```powershell
python problems/P2.3-cheon-generalization/code/run_scaling.py
```
