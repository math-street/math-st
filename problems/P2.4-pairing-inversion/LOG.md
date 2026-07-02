# Log — P2.4

## Session 1 — 2026-06-24

**Goal:** Complete SG-01 and obtain reproducible data for SG-02 through SG-05; then document the obstruction in SG-06.

**Prediction (written before running anything):** The final exponentiation will have a large, exactly characterizable kernel and cheap constructive inversion at toy scale, while fixed-argument Miller inversion will require searching or solving a structured curve equation; therefore the Miller stage will dominate direct inversion in the measured toy instances.

**Did:**
- Initialized the problem workspace and attempt A001.

**Found:**
- No experimental result has been recorded yet.

**Prediction vs. outcome:** Pending.

**Did not work:** Nothing yet.

**Changed my mind about:** Nothing yet.

**Next:** Run repository checks, implement the staged pairing, and validate it before measuring inversion.

## Session 1 — completion note — 2026-06-24

**Goal:** Close the initial staged experiment, interpret it against verified literature, and leave a precise reduction obstruction.

**Prediction (carried from session start):** Raw Miller inversion would dominate measured toy runtime, while final exponentiation would have a large, regular fibre.

**Did:**
- Added `lib/pairing.py` with exposed Miller, final-exponentiation, trace, and distortion-map calls.
- Validated against Stögbauer's published \(\mathbb F_{43}\) vector and ran all shared tests.
- Exhaustively enumerated six final-exponentiation maps and six cyclic FAPI-1 Miller domains.
- Expanded the fixed-\(P\) Miller function in the curve coordinate ring and checked it at all ten nonidentity \(G_2\) points.
- Verified Galbraith–Hess–Vercauteren and found Satoh's revised 2025 MI theorem.
- Wrote A002 and `CLAIM.md` for a candidate source-ECDLP/FAPI generic-oracle separation.

**Found:**
- [EMPIRICAL: \(p=43,r=11\)] The composed pairing equals the two published reduced values and follows the published five-operation Miller trace.
- [EMPIRICAL: six curves, \(43\le p\le163\), \(5\le r\le41\)] Every final fibre has size \((p^2-1)/r\), all 300 bilinearity trials pass, and the cyclic raw Miller image contributes one representative to each nonidentity target fibre.
- [EMPIRICAL: 82 nonidentity targets] The experiment's canonical final root was compatible with the raw cyclic Miller image 0 times.
- [EMPIRICAL: six curves, 50 timings each] Naive raw Miller inversion was 147–545 times slower than the implemented arbitrary-root method, but this is an implementation result rather than an asymptotic lower bound.
- [PROVED] On the cyclic FAPI domain the compatible fraction of each nonidentity final fibre is exactly \(1/d\), where \(d=(p^2-1)/r\).
- [CITED] Satoh proves polynomial-time MI for the opposite fixed-argument orientation, so the `[UNVERIFIED]` Satoh lead in the prompt is resolved but does not automatically settle this repository's FAPI-1 orientation (IACR ePrint 2019/385, revised 2025).

**Prediction vs. outcome:** Matched for the measured brute-force code, but the literature forced a distinction between computational timing and mathematical obstruction. Miller evaluation dominated runtime; final exponentiation created the representative-selection gap.

**Did not work:** Omitting all vertical denominators did not reproduce the source's raw intermediate values because optimized Miller representatives can differ by prime-subfield factors. The final exponentiation nevertheless matched both published outputs exactly, so the test now compares the invariant reduced values.

**Changed my mind about:** The most defensible answer is not “one stage is always hard.” In this FAPI-1 implementation the raw stage is slower, while the loss of the unique compatible representative occurs at final exponentiation; Satoh shows that MI complexity also depends on argument orientation.

**Next:** Reproduce Satoh Algorithm 4.1 at \(k=2\), then decide Q005 and Q006.

### Correction to Session 1 completion note

The global question IDs changed concurrently: the next decisions are Q006 (Satoh orientation transfer) and Q007 (oracle-model scope). Q005 belongs to P2.1.
[2026-06-24] [NOTE] Session 2 goal: reproduce Satoh's even-embedding-degree Miller-inversion algorithm on the published p=139 example, derive and exhaustively test the distortion-map transfer from the fixed-base FAPI-1 orientation to Satoh's fixed-extension-point orientation, and either formalize or reject the candidate generic oracle separation.
[2026-06-24] [NOTE] Session 2 prediction: the published example and the j=1728 transfer will validate with a normalization constant determined by the local parameter at infinity; this will remove the Miller-inversion bottleneck on the supersingular toy family, while the oracle result will remain explicitly limited to a generic bilinear-group interface rather than a lower bound for concrete finite-field representations.

## Session 2 outcome — 2026-06-27

- [EMPIRICAL: Satoh Example 4.4] The new implementation reproduced \(u=131\), x-candidates \(59,75\), solution \((59,-54)\), and raw target \(25\theta+109\) for \(p=139,\ell=35,d=140\).
- [PROVED] The shared Miller loop now handles addition chains that pass through the identity by using \(g_{\mathcal O,T}=g_{T,\mathcal O}=1\); the composite-scalar published example is its regression test.
- [PROVED] With \(\tau=x/y\) and \(\psi(x,y)=(-x,iy)\), normalized functions satisfy \(f_{r,P}(\psi(R))=i^{-r}f_{r,\psi^{-1}P}(R)\). Multiplication by \(i^r\) therefore transfers a raw FAPI-1 target to Satoh's orientation.
- [EMPIRICAL: six curves, all 82 nonidentity raw targets] The pullback identity and Satoh-based raw inverse passed exhaustively, testing no more than four candidate points per inverse.
- [EMPIRICAL: same 82 reduced targets] The canonical root in \(\mu_r\) was Miller-compatible 0 times. Fast raw MI therefore left the final-fibre representative-selection obstruction intact for this selector.
- [PROVED] With a \(\mathbb G_2\)-DLP oracle, FAPI-1 is polynomial-time equivalent to target-group DLP, not automatically to source-group DLP.
- [UNVERIFIED] A002 now specifies an elliptic-curve-backed generic oracle with free \(\mathbb G_2\)-DLP and proves candidate FAPI-1 success bound \(O(q^2/r)\), including a probability-one fixed-oracle selection. The claim is frozen for independent review in Q019.
- [EMPIRICAL: Python 3.13.4] All 63 shared-library tests, all 5 P2.4 experiment tests, and compile checks passed. The standalone six-curve Satoh run took 3.0 seconds and wrote the dated CSV.

**Prediction vs. outcome:** [PROVED] The normalization constant was \(i^{-r}\), Satoh removed raw-MI search on the supersingular degree-two family, and FAPI-1 plus source DLP is exactly target DLP. [EMPIRICAL: six curves] The transfer succeeded on every tested raw target. The prediction that the oracle result would remain scoped to generic typed encodings was correct.

**Self-attack outcome:** [PROVED] Adaptive branching on target-label bits is covered by lazy sampling; blind source-label guesses are negligible; Markov plus Borel–Cantelli supplies a fixed oracle; and a \(j=1728\) torsion/Weil-pairing construction supplies an underlying elliptic curve. [PROVED] Exposing concrete target-field addition invalidates the affine-transcript proof and is explicitly outside the claim.

**Next:** Obtain an independent audit of `CLAIM.md` under Q019. No additional toy experiment is needed to evaluate that proof-quantifier question.

## Session 3 — 2026-07-02

**Goal:** Close Q019 by auditing the random-encoding lower bound and fixed-oracle quantifiers, adding an exhaustive affine-collision verifier at small prime orders, and either promoting A002 to a scoped proved oracle separation or recording a concrete fatal counterexample.

**Prediction (written before the audit):** The lazy-sampling collision argument and the probability-one fixed-oracle extraction will survive after making cross-parameter independence and arbitrary bit-string branching explicit. Exhaustive small-order checks will attain but not exceed the union-bound bad set. The result will remain a generic-encoding oracle separation and will not extend to coordinate-exposing target fields.

## Session 3 outcome — 2026-07-02

- [CITED] Shoup's RR model, Maurer's affine hidden-state argument, and Zhandry's RR/TS distinction confirm that A002 must name its model explicitly and that FAPI-1 is an applicable single-stage game.
- [PROVED] The adaptive proof now uses a collision-free simulator coupled separately to a uniform encoding for each challenge. It no longer makes the false intermediate assertion that one fixed encoding supplies the same challenge label for different exponents.
- [PROVED] For at most \(t\) target handles, the registered-handle success bound is exactly at most \((\binom t2+1)/r\); \(q\) blind source-label probes add \(O(q/2^L)\).
- [PROVED] A worst-case bounded-error FAPI solver would retain its success under the uniform challenge distribution, so the distributional bound excludes the ordinary search solver.
- [PROVED] Conditioning on every other security-parameter component leaves the current random encoding independent. Markov and the first Borel–Cantelli lemma give an eventually negligible bound for each machine on almost every fixed oracle; countable intersection supplies one oracle for all machines.
- [EMPIRICAL: 541,966 exact sets plus 10,000 seeded sets] The affine collision audit found zero violations for \(p\in\{5,7,11\}\), \(2\le t\le4\), and attained the applicable bound in every exhaustive row.
- [EMPIRICAL: Python 3.13.4] The audit ran in 0.9 seconds. All 64 shared tests, all 7 P2.4 tests, and compile checks passed.
- [PROVED] A002 is promoted to a scoped theorem and Q019 is closed. The theorem is an elliptic-curve-backed RR/Shoup generic oracle separation; it makes no claim for coordinate-exposing target-field arithmetic.

**Prediction vs. outcome:** [PROVED] The prediction matched. The proof survived only after explicitly separating the random-encoding coupling from the later fixed-oracle extraction. [EMPIRICAL: small prime orders] The bad-set bound was both respected and tight.

**Did not work:** [PROVED] Holding one concrete encoding fixed while varying \(c\) does not preserve the initial challenge label. That phrasing was rejected and replaced by the standard coupled random-encoding experiment before applying the fixed-oracle existence argument.

**Next:** P2.4 has no remaining required sub-goal or open question. A coordinate-exposing finite-field separation would be a strictly stronger new problem, not unfinished work in the stated generic oracle theorem.

### Resolution of historical provisional tags

[PROVED] The append-only Session 1 Satoh lead was resolved by A003, and the Session 2 `[UNVERIFIED]` A002 entry was resolved by A004. Those earlier strings remain only as chronological records; `CLAIM.md`, `STATE.md`, `NOTES.md`, and `OPEN_QUESTIONS.md` contain no unresolved P2.4 claim.
