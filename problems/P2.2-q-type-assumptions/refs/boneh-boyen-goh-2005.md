# Boneh–Boyen–Goh — BDHI variants

Dan Boneh, Xavier Boyen, and Eu-Jin Goh, “Hierarchical Identity Based
Encryption with Constant Size Ciphertext,” EUROCRYPT 2005, LNCS 3494,
440–456; full version dated 20 June 2005.

Primary text: <https://crypto.stanford.edu/~dabo/papers/shibe.pdf>

## Extracted statements in repository notation

[CITED] Section 2.3 defines $q$-BDHI, $q$-wBDHI, and $q$-wBDHI$^*$ with targets
$e(w,w)^{1/\beta}$, $e(g,h)^{1/\alpha}$, and
$e(g,h)^{\alpha^{q+1}}$, respectively.

[CITED] Reversing the power ladder with new hidden exponent $1/\alpha$ gives a
linear-time, one-call equivalence between $q$-wBDHI and $q$-wBDHI$^*$.

[CITED] A $q$-wBDHI$^*$ solver tightly solves $q$-BDHI by using base
$w^{\beta^q}$, the reversed ladder, independent generator $h=w^s$, and raising
the returned target to $1/s$.

## Audit note

[PROVED] The construction following equations (2)–(3) was read and its target
exponent was recomputed before recording the graph edges.

