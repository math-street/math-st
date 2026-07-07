# Satoh 2025 revision

Takakazu Satoh, “Miller Inversion is Easy for the Reduced Tate Pairing of Embedding Degree Greater than one,” IACR ePrint 2019/385, revised January 2025.

## Main theorem in repository notation

- [CITED] Fix an order-\(\ell\) point \(A\) in the \(q\)-eigenspace and a raw Miller target \(v\). Satoh recovers a base-field point \(Q\) with \(h_{\ell,A}(Q)=v\), or reports nonexistence, in polynomial time after the stated 2-Sylow square-root precomputation.
- [CITED] The even-\(k\) algorithm is deterministic with \(O((k\log q)^3)\) bit complexity (Algorithm 4.1 and Theorem 4.2).
- [CITED] The odd-\(k\) algorithm is probabilistic with average \(O(k^6(\log q)^3)\) bit complexity (Algorithm 5.2 and Theorem 5.3).
- [CITED] Example 4.4 explicitly shows that FEI must provide the correct raw representative before MI can select the desired point.

## Orientation and assumptions

- [CITED] The fixed argument \(A\) lies in the extension-field \(q\)-eigenspace, while the recovered argument \(Q\) lies in \(E(\mathbb F_q)\). Under P2.4's convention \(\mathbb G_1=E(\mathbb F_q)[r]\), this is the FAPI-2 Miller orientation.
- [CITED] The theorem assumes odd characteristic, embedding degree greater than one, and a precomputed generator for a 2-Sylow subgroup used in square-root recovery.

## What it rules out and leaves open

- [CITED] Miller inversion in this orientation cannot be treated as the unresolved hard stage for reduced Tate pairings.
- [PROVED] For the repository's normalized Miller function on the supersingular \(j=1728\), degree-two family, conjugation by \(\psi(x,y)=(-x,iy)\) gives \(f_{r,P}(\psi(R))=i^{-r}f_{r,\psi^{-1}P}(R)\). Hence the raw FAPI-1 Miller target transfers to Satoh's orientation by multiplication by \(i^r\).
- [PROVED] This orientation transfer solves raw MI on that family but does not select the Miller-compatible representative from a reduced-pairing final-exponentiation fibre.

## Verification performed here

- [EMPIRICAL: Satoh Example 4.4] `lib/tests/test_pairing.py` reproduces \(u=131\), x-candidates \(59,75\), solution \((59,-54)\), and the raw target \(25\theta+109\).
- [EMPIRICAL: six curves, 82 nonidentity targets] `code/reproduce_satoh_mi.py` exhaustively validates the normalized FAPI-1 transfer and raw inverse with at most four tested candidates per target.
