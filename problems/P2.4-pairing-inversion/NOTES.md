# Notes — P2.4

## Stable facts

- [PROVED] Let \(N=q^k-1\), let \(r\mid N\), and put \(d=N/r\). On the cyclic group \(\mathbb F_{q^k}^{\times}\), the map \(x\mapsto x^d\) has kernel size \(d\), image size \(r\), and exactly \(d\) preimages for every target in its image. Proof: for a cyclic group of order \(N\), a power map has kernel size \(\gcd(N,d)=d\); the first isomorphism theorem gives the image and fibre sizes.
- [PROVED] For nonzero fixed \(P\) in a non-degenerate prime-order pairing, \(Q\mapsto e(P,Q)\) is a bijection from the cyclic group \(\mathbb G_2\) to \(\mu_r\). Consequently, for every nonidentity target whose direct Miller evaluation is defined, exactly one of the \(d\) final-exponentiation preimages is the raw Miller value of the unique \(Q\in\mathbb G_2\).
- [PROVED] For an odd order \(r\), the left-to-right binary Miller expression for \(f_{r,P}\), after its final vertical-line cancellation, has \(r-2\) affine line factors in its numerator and \(r-3\) vertical factors in its denominator. Proof: an intermediate expression for scalar \(n\) has \(n-1\) factors in each side; the last bit doubles \((r-1)/2\) to \(-P\), adds \(P\), introduces no final denominator, and cancels the common vertical through \(P\).
- [CITED] Galbraith, Hess, and Vercauteren prove that one-sided FAPI gives a cross-source homomorphism and solves the corresponding BDH problem; both FAPI directions solve CDH. Their paper does not state a reduction from ECDLP in \(\mathbb G_2\) to FAPI-1 (IEEE TIT 2008, Theorem 2, Lemma 3, Corollary 10).
- [CITED] Satoh gives polynomial-time Miller inversion with fixed \(q\)-eigenspace argument and variable base-field argument: deterministic \(O((k\log q)^3)\) bit operations for even \(k\), and probabilistic average \(O(k^6(\log q)^3)\) for odd \(k\), assuming the stated square-root precomputation (IACR ePrint 2019/385, revised January 2025). Directly this is the repository's FAPI-2 Miller orientation.
- [PROVED] On the supersingular \(j=1728\), degree-two family, the distortion map \(\psi(x,y)=(-x,iy)\) transfers the normalized functions by \(f_{r,P}(\psi(R))=i^{-r}f_{r,\psi^{-1}P}(R)\). Therefore multiplying a raw FAPI-1 Miller target by \(i^r\) puts it in Satoh's orientation, yielding polynomial-time raw MI on this family.

## Validated implementation and data

- [EMPIRICAL: \(p=43,r=11,k=2\)] The composed pairing matches Stögbauer's published vector exactly: \(e(P,Q)=11+3t\), \(e(2P,Q)=26+23t\), and the raw loop follows `double,double,add,double,add`; see `lib/tests/test_pairing.py`.
- [EMPIRICAL: \(p\in\{43,59,83,103,131,163\}\), \(r\in\{5,7,11,13,41\}\), 300 trials] All 300 deterministic random bilinearity tests passed and every base pairing was nonidentity of order \(r\); see `data/measure_pairing_stages_p43-59-83-103-131-163_20260624.csv`.
- [EMPIRICAL: same six curves, exhaustive \(\mathbb F_{p^2}^{\times}\)] Every final-exponentiation fibre had its predicted size \(d\in[168,1560]\), and every nonidentity pairing target had exactly one compatible raw Miller value on the cyclic FAPI-1 domain.
- [EMPIRICAL: same six curves, all 82 nonidentity targets] The canonical root returned by the experiment's target-subgroup-DLP method was Miller-compatible in 0 of 82 cases. This tests one deterministic root selector, not all root-extraction algorithms.
- [EMPIRICAL: same six curves, 50 timings per curve] Naive raw Miller inversion took 1.99–55.59 ms per target, while finding an arbitrary final-exponentiation root through a toy target-subgroup DLP took 13.58–101.99 microseconds; the former was 147–545 times slower in this unoptimized Python implementation. The CSV stores per-curve 95% normal-approximation confidence half-widths and probe counts.
- [EMPIRICAL: Satoh Example 4.4] The implementation reproduces \(u=131\), x-candidates \(59,75\), solution \((59,-54)\), and raw target \(25\theta+109\) for \(p=139,\ell=35,d=140\).
- [EMPIRICAL: same six curves, all 82 nonidentity raw targets] The normalized distortion identity and Satoh-based FAPI-1 raw inverse both passed exhaustively, using at most four tested points per target; see `data/reproduce_satoh_mi_p43-59-83-103-131-163_20260627.csv`.
- [EMPIRICAL: same 82 reduced targets] The canonical final root in \(\mu_r\) was compatible with the raw Miller image in 0 cases, confirming that fast MI does not by itself solve final-fibre representative selection.

## Fixed-argument Miller structure at the published vector

- [EMPIRICAL: \(E/\mathbb F_{43}:y^2=x^3+x\), \(P=(23,8)\), all 10 nonidentity \(G_2\) points] In \(\mathbb F_{43}[x,y]/(y^2-x^3-x)\), the validated raw function is
  \[
  f_{11,P}(x,y)=\frac{(y+19x+28)^4(y+39x+20)^2(y+14x+14)^2(y+36x+24)}{(x+29)^4(x+12)^2(x+30)^2}.
  \]
- [EMPIRICAL: same fixed vector] The factor degrees are \(9/8\); after reducing powers of \(y\), the numerator is \(A(x)+B(x)y\) with \(\deg A=13\), \(\deg B=12\), while the denominator has \(x\)-degree 8. Complete coefficient arrays are in `data/analyze_miller_function_p43_r11_20260624.csv`.

## Bottleneck determination

- [EMPIRICAL: same six curves and algorithms] If a correct raw target is already supplied, naive Miller inversion is the measured computational bottleneck; final exponentiation adds little to direct exhaustive FAPI-1 inversion.
- [PROVED] If only the pairing target is supplied, arbitrary final-stage inversion is insufficient on the cyclic domain because a fraction exactly \(1/d\) of its fibre is Miller-compatible. Thus the information-selection obstruction lies at the interface created by final exponentiation, even when a chosen Miller-inversion algorithm is fast.
- [CITED] Satoh's Example 4.4 makes the same distinction in the opposite argument orientation: MI returns a point only when FEI supplies the correct representative, and different points with the same reduced value require different MI inputs (IACR ePrint 2019/385, revised 2025).

## Reduction attempt

- [PROVED] A \(\mathbb G_2\)-ECDLP oracle alone does not implement the natural FAPI-1 route: the target \(z\in\mathbb G_T\) must first be mapped back to some \(\mathbb G_2\) element before that oracle has a valid input, and constructing precisely that cross-group inverse is FAPI-1.
- [PROVED] With fixed generators and a \(\mathbb G_2\)-DLP oracle, FAPI-1 and DLP in \(\mathbb G_T\) reduce to one another: target DLP gives the scalar needed for the FAPI output, while FAPI followed by source DLP gives the target scalar.
- [PROVED] Attempt A002 gives an elliptic-curve-backed RR/Shoup generic oracle separation. It places a perfect DLP oracle only on \(\mathbb G_2\), proves the explicit FAPI-1 bound \((\binom t2+1)/r+O(q/2^L)\), and uses a Markov–Borel–Cantelli argument to obtain one fixed oracle against all probabilistic polynomial-time machines. A004 records the completed audit.
- [PROVED] The A002 theorem is explicitly scoped to generic typed encodings. It does not claim a lower bound for the concrete \(\mathbb F_{q^k}\) target representation or for algorithms using target-field addition.

## Resolved questions

- [PROVED] Q006 is resolved for the measured supersingular degree-two family by the local-parameter normalization proof and exhaustive transfer validation in A003.
- [PROVED] Q007 is resolved as a model decision: A002 is stated as a standard generic-bilinear oracle separation backed by actual elliptic curves; the stronger coordinate-exposing model is outside the claim rather than silently assumed.
- [PROVED] Q019 is resolved by A004: the random-encoding coupling, worst-case search implication, cross-parameter independence, and fixed-oracle quantifiers have explicit proofs, corroborated by the primary-source model comparison and exhaustive affine audit.

## Oracle-bound validation

- [EMPIRICAL: \(p\in\{5,7,11\},2\le t\le4\)] The affine verifier checked 541,966 form sets exhaustively plus 10,000 seeded sets, with zero violations of \(|R_F|\le\min(p,\binom t2)\).
- [EMPIRICAL: same exact rows] Every exhaustive row attained the applicable upper bound, so the check exercised tight collision patterns rather than only sparse cases; see `data/verify_generic_oracle_bound_p5-7-11_t4_20260702.csv`.

## Post-resolution self-verification

- [PROVED] A005 broadened the negligible blind-label term from source-DLP probes to arbitrary unregistered inputs across all typed oracle interfaces. Independent encodings keep the total contribution \(O(q/2^L)\), so the theorem statement is unchanged.
- [EMPIRICAL: deterministic rerun] The affine CSV reproduced byte-for-byte with SHA-256 `8A69F4ACE2D21F1AA34105603A295121A4DE8A6F7746FD54779BD3682EE2A042`.
- [EMPIRICAL: six curves] Independent recomputation checked the congruence, curve order, point order, pairing nonidentity, and target torsion conditions for every measured realization.
- [PROVED] The resolved status survived the self-verification; A005 records the attacks, correction, and negative controls.
