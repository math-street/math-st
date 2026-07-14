# Bernstein 2006 — Curve25519

**Reference.** [CITED] Daniel J. Bernstein, “Curve25519: New Diffie-Hellman
Speed Records,” *Public Key Cryptography — PKC 2006*, LNCS 3958, 207–228,
2006. <https://cr.yp.to/ecdh/curve25519-20060209.pdf>

**Relevant source facts.** [CITED] The paper lists six prime candidates and
selects \(2^{255}-19\) by its smaller reduction constant. It lists three
successive small acceptable Montgomery coefficients and explains why the
first two were rejected before selecting 486662.

**Audit use. [PROVED]** This is a concrete rationale and shortlist, but not an
exhaustive externally fixed menu of every field/model choice.
