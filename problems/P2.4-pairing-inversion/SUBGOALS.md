# Sub-goals — P2.4

- [x] **SG-01:** Implement a reduced Tate pairing over a toy prime-field curve with the Miller loop and final exponentiation exposed; validate composition, bilinearity, and non-degeneracy.
- [x] **SG-02:** Exhaustively enumerate the final-exponentiation fibres for at least two toy parameter sets and compare them with the group-homomorphism prediction.
- [x] **SG-03:** Compute a symbolic fixed-\(P\) Miller function on the first toy curve, reduce it modulo the curve equation where useful, and record numerator/denominator degrees.
- [x] **SG-04:** Invert the raw Miller stage and the composed pairing exhaustively on the same domains; record image sizes, fibre distributions, and timings.
- [x] **SG-05:** Compare the separately measured inversion stages and identify the toy-scale bottleneck without generalizing beyond the measured range.
- [x] **SG-06:** Write the natural ECDLP-to-FAPI reduction attempt and isolate the exact missing cross-group capability.
- [x] **SG-07:** Implement Satoh Algorithm 4.1 at \(k=2\), validate its stated example, and test the distortion-map transfer to the repository's FAPI-1 orientation.
- [x] **SG-08:** Formalize or reject A002 under an oracle model that the problem accepts, including the extent to which target-field structure must remain visible.
- [x] **SG-09:** Audit A002 to closure with primary-source model comparison, exhaustive affine-collision checks, and a fixed-oracle quantifier proof.
- [x] **SG-10:** Adversarially self-verify the resolved theorem, reproduce deterministic data, and independently check the elliptic-curve realization.
