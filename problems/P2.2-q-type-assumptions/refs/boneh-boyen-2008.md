# Boneh–Boyen — SDH signatures

Dan Boneh and Xavier Boyen, “Short Signatures Without Random Oracles and the
SDH Assumption in Bilinear Groups,” *Journal of Cryptology* 21(2), 149–177,
2008. DOI: 10.1007/s00145-007-9005-7.

Primary text: <https://crypto.stanford.edu/~dabo/pubs/papers/bbsigs.pdf>

## Extracted statements in repository notation

[CITED] Section 3.1 gives the typed $q$-SDH tuple: a $\mathbb G_1$ power
ladder through $x^q$, together with $g_2,g_2^x$, and target
$(c,g_1^{1/(x+c)})$.

[CITED] Section 3.3 proves random self-reducibility with one solver call, unchanged
success probability, and $O(q)$ exponentiations.

[CITED] Section 3.3 reduces $q$-aBDH to $q$-SDH with one solver call and unchanged
success probability by the polynomial identity
$(X^{q+2}-(-c)^{q+2})/(X+c)=X^{q+1}+w(X)$, $\deg w\le q$.

[CITED] Theorem 8 proves the main short-signature security statement under
$q$-SDH with $q$ equal to the signing-query bound and approximately a factor-two
advantage loss.

## Audit note

[PROVED] The full reduction calculations in Section 3.3, not only their summary
statements, were read for the implication/loss table.
