# Toy Deuring round-trip specification

## Scope

- [PROVED] This specification fixes equality and acceptance conventions for SG-03 before any new \(\mathbb F_{p^2}\) isogeny code is written.
- [PROVED] It is restricted to exhaustive toy experiments with \(p<2^{16}\); its canonicalization procedures are not claimed to be efficient at cryptographic size.

## Field and element encoding

- [PROVED] For \(p>3\), choose the least positive quadratic nonresidue \(\nu\pmod p\) and represent \(\mathbb F_{p^2}=\mathbb F_p[u]/(u^2-\nu)\).
- [PROVED] Encode \(a+bu\) by the integer pair \((a,b)\) with \(0\le a,b<p\), ordered lexicographically.
- [PROVED] The Frobenius map is computed by exponentiation \(z\mapsto z^p\); this avoids relying on a sign formula tied to a particular \(\nu\).

## Curve-class encoding

- [PROVED] A curve is stored as a nonsingular short Weierstrass equation \(E_{A,B}:y^2=x^3+Ax+B\) over \(\mathbb F_{p^2}\), with the ordered coefficient encoding \((A,B)\).
- [PROVED] Two such equations are \(\mathbb F_{p^2}\)-isomorphic exactly when some \(c\in\mathbb F_{p^2}^\times\) sends their coefficients by \((A,B)\mapsto(c^4A,c^6B)\).
- [PROVED] Define `curve_key(E)` as the lexicographically least coefficient pair in this finite scaling orbit; exhaustive enumeration costs \(O(p^2)\) field operations and is acceptable only at toy scale.
- [PROVED] Define `deuring_key(E)=min(curve_key(E),curve_key(E^{(p)}))`, where \(E^{(p)}\) has coefficients \((A^p,B^p)\).
- [CITED] Deuring correspondence identifies maximal-order isomorphism classes with supersingular curve classes modulo the action of \(\operatorname{Gal}(\mathbb F_{p^2}/\mathbb F_p)\) (Wesolowski 2022, Section 2.4).
- [PROVED] Therefore `deuring_key`, rather than `curve_key`, is the correct endpoint equality test for a round trip that starts from an abstract maximal order without a chosen orientation.

## Isogeny and ideal encoding

- [PROVED] A smooth isogeny is stored as an ordered chain of prime-degree Vélu steps; each step contains the source `curve_key`, the prime degree, a canonical generator or canonical list of the cyclic kernel, and the target `curve_key`.
- [PROVED] A quaternion element uses exact rational coordinates in a fixed basis of \(B_{p,\infty}\).
- [PROVED] A full ideal or order lattice uses a row-Hermite-normal-form basis after clearing a single positive common denominator; the denominator is part of the encoding.
- [PROVED] The normalized ideal norm is the positive square root of its lattice index in its left maximal order, and the normalized quadratic form is \(q_I(\alpha)=\operatorname{Nrd}(\alpha)/\operatorname{Nrd}(I)\).

## Forward and reverse acceptance rules

- [PROVED] For an ideal-to-isogeny conversion \(I\mapsto\phi_I:E_0\to E'\), accept the endpoint exactly when `deuring_key(E')=deuring_key(E_target)` and the product of recorded step degrees equals \(\operatorname{Nrd}(I)\).
- [PROVED] For an isogeny-to-ideal conversion \(\phi\mapsto I_\phi\), accept the ideal exactly when it is closed under the fixed left order, its normalized norm equals \(\deg\phi\), and converting it forward again passes the preceding endpoint test.
- [PROVED] A direct equality test between the recovered right order and a target endomorphism ring is optional in the first implementation because `deuring_key` already accounts for the unavoidable Frobenius ambiguity.
- [PROVED] No test may accept merely because two theta-series prefixes agree; distinct quaternion ideal lattices can be isospectral (Goren--Love 2025, Example 3.1).

## Required validation fixtures

- [PROVED] The first implementation must validate field multiplication and Frobenius against exhaustive tables for \(p\in\{7,11\}\).
- [PROVED] It must validate curve canonicalization by applying every nonzero scaling to at least one curve and checking a single key.
- [PROVED] It must validate one prime-degree Vélu step by kernel annihilation, preservation of the point count, and equality of the recorded and recomputed target key.
- [PROVED] It must validate one ideal norm identity against `lib/quaternion.py` before attempting a complete Deuring round trip.
