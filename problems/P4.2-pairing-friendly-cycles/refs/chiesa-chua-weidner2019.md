# Chiesa, Chua, and Weidner (2019)

Alessandro Chiesa, Lynn Chua, and Matthew Weidner, "On Cycles of
Pairing-Friendly Elliptic Curves," *SIAM Journal on Applied Algebra and
Geometry* 3(2), 175-192, 2019. DOI: 10.1137/18M1173708. arXiv:1803.02067.

Primary-source copy: <https://arxiv.org/abs/1803.02067>

## Main results in repo notation

[CITED] Proposition 4.1 classifies MNT cycles: their lengths are 2 or 4 and
their embedding degrees alternate as \((6,4)\) or \((6,4,6,4)\).

[CITED] Table 4.1 parameterizes an MNT6/MNT4 2-cycle by field sizes
\(4x^2+1\) and \(4x^2+2x+1\), with the order of either curve equal to the
other field size.

[CITED] Example 4.9 sets \(x=3\) and gives four explicit equations. Its first
two are \(y^2=x^3+24x+16\) over \(\mathbb F_{37}\) and
\(y^2=x^3+36x+5\) over \(\mathbb F_{43}\).

[CITED] Proposition 5.1 rules out pairing-friendly 2-cycles with embedding
degree pairs \((5,10)\), \((8,8)\), and \((12,12)\).

## Assumptions and limits

[CITED] The MNT classification applies when every curve in the cycle belongs
to an MNT family. It is not a classification of arbitrary pairing-friendly
cycles.

## Verification status

The parameter-\(x=3\) equations are the SG-02 regression target. Computed
verification is recorded in `../LOG.md` and `../data/` after execution.

