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
