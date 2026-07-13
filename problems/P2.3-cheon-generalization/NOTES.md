# Notes — P2.3

## Stable facts

- [CITED] For \(d\mid n-1\), Cheon's Theorem 1 gives a two-stage recovery
  cost of \(O(\log n(\sqrt{(n-1)/d}+\sqrt d))\) primitive group operations
  (Cheon 2006, EUROCRYPT, LNCS 4004, Theorem 1; `refs/cheon2006.md`).
- [EMPIRICAL: exhaustive n in {17,19,31}] `code/cheon.py` recovered every
  tested secret in both the opaque simulator and the concrete order-19 curve
  tests (`code/tests/test_cheon.py`).
- [EMPIRICAL: 328 trials, 70913 <= n <= 17592207015937] With \(d=2^m\) and
  \((n-1)/d\) selected near \(d\), the fitted exponentiation-call slope is
  0.25001 with 95% within-size bootstrap interval [0.24610, 0.25351]
  (`data/run_scaling_fit_hb8-22_t41_s2303_20260713.json`).

## Working observations

- [CONJECTURE] The divisor condition supplies the two exact multiplicative
  orbits used by the implementation; a useful SG-04 adaptation must identify
  a replacement search set rather than merely substitute a nearby integer
  for \(d\). This is refuted by an algorithm using the same inputs for some
  \(d\nmid n\pm1\) whose measured cost is below generic square-root search on
  a controlled infinite family.
