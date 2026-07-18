# Chairattana-Apirom--Tessaro -- concrete BBS/BBS+ security

Rutchathon Chairattana-Apirom and Stefano Tessaro, “On the Concrete Security of
BBS/BBS+ Signatures,” ASIACRYPT 2025; IACR ePrint 2025/1093, revised
2025-10-22.

Primary record: <https://eprint.iacr.org/2025/1093>

## Relevant result

[CITED] The abstract states that after observing $q$ signatures, attacks on
BBS+ and deterministic BBS recover the secret key with the complexity of the
$\Theta(q)$-discrete-log problem, which is $O(\sqrt{p/q})$ for many choices of
$q$.

[CITED] The abstract also states a reduction showing that security of BBS+ and
deterministic BBS implies the $\Theta(q)$-SDH assumption.  This direction does
not base the schemes or $q$-SDH on a static assumption.

## Audit limit

[PROVED] The ePrint abstract and revision metadata were checked.  No claim here
depends on an unaudited theorem number or an exact hidden constant in
$\Theta(q)$.
