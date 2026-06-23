# Sub-goals

- [ ] **SG-01 overall: FAILED this session.** The genus invariant was implemented, but the descended curve and cover map were not constructed.

- [x] SG-01a: implement polynomial-basis $\mathbb F_{2^N}$ arithmetic in `lib/curves.py` and validate field axioms at degrees 4, 6, and 8.
- [x] SG-01b: implement the GHS magic-number and exact genus branch calculation for $E:y^2+xy=x^3+ax^2+b$.
- [x] SG-01c: reproduce the genus-31 characteristic-two example in the Magma Weil-descent documentation.
- [x] SG-02: exhaustively sweep every $b\ne0$ at $n\in\{4,6,8\}$ and write deterministic CSV data and a distribution plot.
- [x] SG-03: verify for every swept parameter that the recorded genus agrees with the span-rank formula.
- [x] SG-04: record the low-genus locus in the $j=1/b$ coordinate and test Frobenius stability.
- [x] SG-05a: report exact low-genus-locus densities for the covered degrees.
- [ ] SG-05b: compare the observed counts with the general finite-field type-counting formula in Maurer–Menezes–Teske.
- [ ] SG-06: implement an end-to-end toy GHS map and Jacobian DLP after function-field construction is available or hand-built.
