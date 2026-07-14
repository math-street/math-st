# Lochter–Merkle 2010 — RFC 5639

**Reference.** [CITED] Manfred Lochter and Johannes Merkle, *Elliptic Curve
Cryptography (ECC) Brainpool Standard Curves and Curve Generation*, RFC 5639,
March 2010, doi:10.17487/RFC5639.
<https://www.rfc-editor.org/rfc/rfc5639.html>

**Relevant source facts.** [CITED] Appendix A fixes the bit ordering, SHA-1
mapping, seed increment, first-prime rule, curve tests, and stopping rule.
Field seeds are derived from \(\pi\); curve seeds are derived from \(e\).
Base-point construction includes an explicit random choice between \(Q\) and
\(-Q\).

**Audit use. [PROVED]** The curve core has zero residual bits under A256. The explicit
sign choice contributes one bit only to the full package.
