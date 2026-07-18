# Cheon — quantitative attacks

Jung Hee Cheon, “Security Analysis of the Strong Diffie-Hellman Problem,”
EUROCRYPT 2006, LNCS 4004, 1–11. DOI: 10.1007/11761679_1.

Primary text:
<https://www.math.snu.ac.kr/~jhcheon/publications/2006/Eurocrypt_Cheon_LNCS.pdf>

## Extracted statements in repository notation

[CITED] If $d\mid r-1$, knowledge of $g^x$ and $g^{x^d}$ permits recovery of
$x$ in $O(\log r(\sqrt{(r-1)/d}+\sqrt d))$ group operations.  [Theorem 1]

[CITED] If $d\mid r+1$, a ladder through degree $2d$ permits recovery of $x$ in
$O(\log r(\sqrt{(r+1)/d}+d))$ group operations.  [Theorem 2]

[PROVED] Either recovery attack solves any inverse or exponent relation whose
hidden value is $x$, including the displayed source-core $q$-SDH relation.

[CITED] The paper's own “strong DH” naming uses an exponent-output variant, so
the repository relies on the supplied-power recovery theorems rather than
equating its acronym with Boneh–Boyen inverse-form $q$-SDH.
