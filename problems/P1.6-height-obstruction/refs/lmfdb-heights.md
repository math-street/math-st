# LMFDB and Sage canonical-height checks

Sources:

- <https://www.lmfdb.org/knowledge/show/ec.canonical_height>
- <https://www.lmfdb.org/EllipticCurve/Q/37/a/1>
- <https://www.lmfdb.org/EllipticCurve/Q/data/389.a1>
- <https://www.lmfdb.org/EllipticCurve/Q/data/11.a2>
- <https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/height.html>

[CITED] The reviewed LMFDB definition uses
$\widehat h(P)=\lim n^{-2}h_x([n]P)$ and its 389.a1 data record generator
heights $0.32700077365160495$ and $0.47671165934373954$.

[CITED] The Sage documentation gives
$\widehat h((0,0))=0.0511114082399688$ for the generator of 37.a1.

[CITED] The 11.a2 data record rank zero, torsion structure $\mathbb Z/5\mathbb
Z$, and torsion generator $(5,5)$.

[EMPIRICAL: nine exact doublings] `lib/tests/test_heights.py` reproduces all
three nonzero reference heights within $2\cdot10^{-6}$.
