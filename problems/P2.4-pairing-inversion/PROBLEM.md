# P2.4 — Fixed-argument pairing inversion

## Setting

Let
\[
e:\mathbb G_1\times\mathbb G_2\longrightarrow\mathbb G_T
\]
be a bilinear pairing on an elliptic curve, with embedding degree \(k\).

## Problems

- **FAPI-1:** Given \(e\), \(P\in\mathbb G_1\), and \(z\in\mathbb G_T\), find \(Q\in\mathbb G_2\) such that \(e(P,Q)=z\).
- **FAPI-2:** Exchange the roles of \(\mathbb G_1\) and \(\mathbb G_2\).

## Research task

Prove a polynomial-time equivalence between FAPI-1 and ECDLP in \(\mathbb G_2\), or construct an oracle separation. A realistic partial target is to expose the Miller loop and final exponentiation as separate stages, measure their fibres and inversion costs at toy scale, characterize the fixed-argument Miller function, and state precisely where an attempted ECDLP-to-FAPI reduction stops.

## Scope and validation targets

- Work only with toy parameters satisfying the repository ceiling.
- Validate a staged implementation against an independently published test vector.
- Verify bilinearity and non-degeneracy over many deterministic random trials.
- Keep FAPI-1 and FAPI-2 results explicitly distinguished.

