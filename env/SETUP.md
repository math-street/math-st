# Environment

The recorded P1.2 run used Python 3.13.4 on Windows 11. The experiment itself
uses only Python's standard library. SymPy 1.14.0 was used once to obtain
independent fixed-input resultant values for the unit tests. SageMath,
Singular, and msolve were unavailable and were not required.

Run `python env/check_env.py` from the repository root to inspect the core
environment.

The recorded P3.3 run used Python 3.13.4, SymPy 1.14.0 for exact Hermite normal
forms, and Matplotlib 3.11.1 for deterministic SVG output. SageMath was
unavailable; exact rank-4 LLL and certified enumeration are implemented in
`lib/quaternion.py`.

Session 2 also used NumPy 2.4.6 for overflow-checked int64 batch evaluation of
certified coefficient boxes. Exact witness norms are re-evaluated with Python
integers before they are accepted.

## P1.6 height experiment

[EMPIRICAL: local environment on 2026-07-03] The P1.6 run used Python 3.13.4,
NumPy 2.4.6, SciPy 1.17.1, SymPy 1.14.0, and Matplotlib 3.11.1.

[EMPIRICAL: local environment on 2026-07-03] SageMath and PARI/GP were
unavailable; `lib/heights.py` therefore used exact `Fraction` arithmetic and a
finite canonical-height limit validated against LMFDB values.

The recorded P2.1 run used the same Python/Windows environment plus SymPy
1.14.0 for factoring toy curve orders and NumPy 2.3.1 for exact segmented
smoothness counts. SageMath/PARI was unavailable; the validated BSGS/twist
counter in `lib/curves.py` was used instead.

The recorded P3.2 run used Python 3.13.4 and NumPy 2.4.6 for seeded multinomial,
binomial, least-squares, and bootstrap computations. SageMath/PARI was
unavailable; exhaustive reduced binary quadratic forms and the validated
prime-field Vélu routines in `lib/isogeny.py` were used at toy scale.

The recorded P5.1 run used Python 3.13.4, pytest 9.1.1, NumPy 2.4.6, and
Matplotlib 3.11.1 on Windows 11. SageMath and PARI/GP were unavailable. Exact
fixed-curve orders used the validated BSGS/twist counter with an explicitly
recorded exhaustive fallback when its point-order congruences did not isolate
the group order.

The recorded P5.4 run used Python 3.13.4 on Windows 11 and only the standard
library. SageMath, Singular, and msolve were unavailable; exhaustive
prime-field formula oracles replaced production-suite execution under the
shared toy-parameter ceiling.

The recorded P4.1 final run used Python 3.13.4, mpmath 1.3.0 at 80 decimal
digits for stable interval-Chebyshev Dickman integration, and SymPy 1.14.0 for
exact nested resultants and KSS16 factorization certificates. SageMath,
PARI/GP, Singular, and msolve were unavailable and were not required.
