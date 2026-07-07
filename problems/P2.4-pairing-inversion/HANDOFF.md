# Handoff — P2.4 — after session 4

## State in five lines

[PROVED] A002 supplies an elliptic-curve-backed RR/Shoup generic oracle separation.
[PROVED] With source DLP supplied, FAPI-1 is exactly target DLP at fixed generators.
[PROVED] Satoh raw MI transfers to FAPI-1 on the measured degree-two family.
[EMPIRICAL: 82 targets] Every transferred raw inverse passed; canonical final roots passed 0 times.
[PROVED] A005 independently self-verified the result and every P2.4 sub-goal is complete.

## Formal result

- [PROVED] The oracle gives one-query \(G_2\)-ECDLP and no target-to-source operation.
- [PROVED] With at most \(t\) target handles and \(q\) total queries, FAPI-1 success is at most \((\binom t2+1)/r+O(q/2^L)\).
- [PROVED] The random-encoding coupling handles arbitrary branching on label bits.
- [PROVED] Arbitrary unregistered strings through any typed oracle interface add only the explicit \(O(q/2^L)\) term.
- [PROVED] Markov–Borel–Cantelli plus countable intersection selects one fixed infinite oracle against every probabilistic polynomial-time machine.
- [PROVED] Supersingular \(j=1728\) curves, distortion maps, and Weil pairings give the hidden groups an actual elliptic-curve realization with polynomial-bit-size public parameters.
- [PROVED] The theorem is scoped to RR/Shoup generic typed encodings, not ordinary coordinate-exposing \(\mathbb F_{p^2}\) arithmetic.

## Staged pairing result

- [PROVED] The final power map has fibre size \(d=(q^k-1)/r\), with one cyclic Miller-compatible value per nonidentity target.
- [PROVED] The binary fixed-argument Miller expression has factor degrees \((r-2,r-3)\) after final cancellation.
- [CITED] Satoh gives polynomial-time MI for the fixed-extension/variable-base orientation.
- [PROVED] For \(\psi(x,y)=(-x,iy)\), \(f_{r,P}(\psi(R))=i^{-r}f_{r,\psi^{-1}P}(R)\), transferring Satoh to raw FAPI-1 MI.
- [EMPIRICAL: Satoh Example 4.4] The published \(p=139,\ell=35,d=140\) vector reproduces exactly.
- [EMPIRICAL: six curves, 82 raw targets] Every transfer and inverse passed with at most four tested candidates.
- [EMPIRICAL: six curves, 300 trials] All bilinearity and non-degeneracy checks passed.

## Oracle-proof audit

- [CITED] Shoup 1997 supplies the RR random-encoding method.
- [CITED] Maurer 2005 states the affine-expression collision argument.
- [CITED] Zhandry 2022 separates RR from TS terminology and relates applicable single-stage security games.
- [EMPIRICAL: \(p=5,7,11\)] 541,966 affine sets were checked exhaustively and 10,000 additionally sampled; zero exceeded \(\min(p,\binom t2)\), and every exact row attained its applicable bound.

## Post-resolution self-verification

- [EMPIRICAL] A fresh affine CSV reproduced byte-for-byte with SHA-256 `8A69F4ACE2D21F1AA34105603A295121A4DE8A6F7746FD54779BD3682EE2A042`.
- [EMPIRICAL: six curves] Fresh checks passed the congruence, curve order, point order, pairing nonidentity, and target torsion conditions.
- [PROVED] Red-teaming arbitrary blind inputs found one too-narrow sentence; the corrected all-interface argument leaves the theorem unchanged.
- [EMPIRICAL: Python 3.13.4] All 66 shared tests, 7 P2.4 tests, and compile checks passed after correction.

## What is ruled out

- [PROVED] A source-only DLP call cannot consume a target handle; its missing operation is FAPI itself.
- [PROVED] Polynomial-time raw MI does not solve reduced FAPI without the unique compatible final-exponentiation representative.
- [PROVED] An arbitrary final root succeeds on only a \(1/d\) fraction of a cyclic fibre.
- [PROVED] No coordinate-aware finite-field lower bound follows from the generic oracle theorem.

## Next action

None for P2.4. Treat any coordinate-exposing oracle separation as a new stronger problem with a new claim and sub-goals.

## Files that matter

`CLAIM.md`, `attempts/A002-generic-oracle-separation.md`, `attempts/A004-oracle-proof-audit.md`, `attempts/A005-self-verification.md` — completed separation and two audits.

`code/verify_generic_oracle_bound.py`, `data/verify_generic_oracle_bound_p5-7-11_t4_20260702.csv` — exact collision-bound counterexample search.

`lib/pairing.py`, `lib/tests/test_pairing.py`, `code/reproduce_satoh_mi.py` — Satoh transfer and published regressions.

`code/measure_pairing_stages.py`, `code/analyze_miller_function.py` and their dated CSVs — stage fibres, timings, and exact fixed Miller function.

## What I would tell my replacement

[PROVED] The proof has two distinct randomness steps: first couple each challenge to a uniform encoding to obtain the query bound, then use Markov–Borel–Cantelli to select one fixed infinite oracle. Conflating those steps was the only genuine proof-level defect found in the audit, and A004 records its repair.
