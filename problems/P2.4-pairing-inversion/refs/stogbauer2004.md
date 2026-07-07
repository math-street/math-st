# Stögbauer 2004

Marcus Stögbauer, “Efficient Algorithms for Pairing-Based Cryptosystems,” diploma thesis, Technische Universität Darmstadt, 2004, Appendix B.

## Published vector

- [CITED] The vector uses \(E/\mathbb F_{43}:y^2=x^3+x\), \(r=11\), \(k=2\), \(P=(23,8)\), \(Q=(20,8t)\), and \(t^2=-1\).
- [CITED] The optimized Miller loop records raw representatives \(38+13t\) and \(28+40t\), which reduce to \(11+3t\) and \(26+23t\); the latter values satisfy the published doubling identity.

## Verification performed here

- [EMPIRICAL: this single vector] `lib/tests/test_pairing.py` reproduces both reduced values, the doubling identity, and the `double,double,add,double,add` loop trace.
- [PROVED] Different raw representatives may differ by a nonzero \(\mathbb F_{43}\) factor because the source omits vertical denominators; the final exponent \(168\) kills every such factor since \(42\mid168\).

