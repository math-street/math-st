# Cheon 2006 — divisor-dependent recovery

## Bibliographic record

[CITED] Jung Hee Cheon, “Security Analysis of the Strong Diffie-Hellman
Problem,” *Advances in Cryptology — EUROCRYPT 2006*, LNCS 4004, pages 1–11,
Springer, 2006, doi:10.1007/11761679_1.

Primary text checked at:
<https://www.iacr.org/archive/eurocrypt2006/40040001/40040001.pdf>

## Main theorem in repository notation

[CITED] Let \(G=\langle g\rangle\) have prime order \(n\), let
\(x\in\mathbb Z_n\), and let \(d\mid n-1\). From \(g,g^x,g^{x^d}\),
Theorem 1 recovers \(x\) using
\(O(\log n(\sqrt{(n-1)/d}+\sqrt d))\) primitive group operations and
\(O(\max\{\sqrt{(n-1)/d},\sqrt d\})\) memory.

## Assumptions used

[CITED] The proof uses the cyclic multiplicative group
\(\mathbb F_n^*\), an element of order \((n-1)/d\) to identify \(x^d\),
and an element of order \(d\) to select the correct root using \(g^x\).

## What it rules out

[CITED] When \(n-1\) has a divisor near \(\sqrt n\) and the auxiliary
element \(g^{x^d}\) is available, generic square-root discrete-log search is
not the best known use of those inputs; Theorem 1 has quarter-power scale up
to its logarithmic factor.

## What it leaves open

[CITED] Theorem 1 assumes \(d\mid n-1\). The paper's \(n+1\) theorem uses a
larger supplied power ladder, and neither theorem supplies a general invariant
for arbitrary polynomial auxiliary exponents.

## Verification in this repository

[EMPIRICAL: exhaustive n in {17,19,31}] `../code/tests/test_cheon.py`
validates the theorem's two-stage construction on toy groups, including the
concrete order-19 elliptic-curve group.
