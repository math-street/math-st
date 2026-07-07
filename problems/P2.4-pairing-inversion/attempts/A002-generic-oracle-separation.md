---
attempt: A002
status: successful
---
# A002 — Separate FAPI-1 from a source-only ECDLP oracle

## Idea

[PROVED] Give an elliptic-curve-backed generic bilinear algorithm a perfect discrete-log oracle for \(\mathbb G_2\), but no map from \(\mathbb G_T\) back to either source group. ECDLP in \(\mathbb G_2\) is one query, while FAPI-1 remains target DLP and needs generic square-root work.

## Prior art

[CITED] Shoup's generic-group lower-bound method tracks formal exponents and bounds accidental collisions by \(O(q^2/r)\) after \(q\) oracle operations (EUROCRYPT 1997).

[CITED] Galbraith, Hess, and Vercauteren show that FAPI-1 computes source-group homomorphisms and solves BDH-1, but do not give the source-ECDLP equivalence targeted here (IEEE TIT 2008).

## Execution

1. [PROVED] `CLAIM.md` specifies independent typed encodings, group operations, a forward pairing, and \(\operatorname{DLOG}_2\).
2. [PROVED] Target handles remain affine in the hidden FAPI exponent because no target-to-source operation exists.
3. [PROVED] At most \(\binom t2\) challenge values cause informative collisions among \(t\) handles, giving success \(O(t^2/r)\).
4. [PROVED] A Markov–Borel–Cantelli argument converts the ensemble bound into existence of one fixed oracle defeating every probabilistic polynomial-time generic machine.
5. [PROVED] Supersingular curves \(y^2=x^3+x\) with \(p\equiv-1\pmod{4r}\), their distortion maps, and Weil pairings give an elliptic-curve realization with embedding degree two.

## Outcome

[PROVED] A004 closed the adaptive-transcript, fixed-oracle, model-naming, and search-quantifier checks. The construction is an oracle separation under the elliptic-curve-backed RR/Shoup generic bilinear interface. It intentionally does not lower-bound algorithms using concrete target-field addition, multiplication, or coordinate encodings.
