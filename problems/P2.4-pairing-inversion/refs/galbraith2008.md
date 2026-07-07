# Galbraith–Hess–Vercauteren 2008

Steven D. Galbraith, Florian Hess, and Frederik Vercauteren, “Aspects of Pairing Inversion,” *IEEE Transactions on Information Theory* 54(12), 5719–5728, 2008. DOI: 10.1109/TIT.2008.2006431. Earlier version: IACR ePrint 2007/256.

## Main results in repository notation

- [CITED] FAPI-1 and FAPI-2 together give polynomial-time CDH algorithms in \(\mathbb G_1\), \(\mathbb G_2\), and \(\mathbb G_T\) (Theorem 2).
- [CITED] FAPI-1 computes every nontrivial homomorphism \(\mathbb G_1\to\mathbb G_2\), and FAPI-2 gives the reverse-direction homomorphisms (Lemmas 3 and 4).
- [CITED] FAPI-1 alone solves BDH-1, and FAPI-2 alone solves BDH-2 (Corollaries 10 and 11).
- [CITED] Pairing inversion decomposes into final-exponentiation inversion followed by Miller inversion, but the usefulness of an arbitrary final root depends on the Miller image and chosen divisor domain (Sections V–VII).
- [CITED] For their larger Tate–Lichtenbaum divisor domain, a random final root is sufficient with non-negligible probability; this is not the same domain as the cyclic \(\mathbb G_2\) used in the formal P2.4 statement (Example 18 and conclusion).

## Assumptions

- [CITED] The main group-theoretic results assume non-degenerate bilinear pairings between cyclic groups of prime order \(r\).

## What it rules out and leaves open

- [CITED] Efficient one-sided FAPI has consequences stronger than merely evaluating the pairing: it creates cross-source maps and breaks the corresponding BDH problem.
- [CITED] The paper does not prove equivalence between FAPI-1 and ECDLP in \(\mathbb G_2\), and its conclusion reports no pairing inversion algorithm for cryptographically useful curves.

## Verification performed here

- [EMPIRICAL: \(p\le163\)] The P2.4 data reproduces the paper's qualitative distinction between arbitrary final roots and roots lying in the Miller image, with the important cyclic-domain restriction recorded in `NOTES.md`.

