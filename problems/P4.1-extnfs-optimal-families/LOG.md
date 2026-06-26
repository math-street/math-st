# P4.1 research log

## Session 1 — 2026-06-26

**Goal:** Build a validated first version of the cost model, family generators, deterministic search, and sensitivity report.

**Prediction (written before running anything):** [HEURISTIC] A single calibrated $L_{p^k}(1/3,c)$ model will reproduce its BN254 anchor by construction but will not justify a unique cross-family optimum because special-form and tower advantages require family-dependent assumptions. This prediction is falsified if one literature-derived, fully specified constant independently matches multiple published estimates across the required families without recalibration.

**Did:**
- Initialized the problem record and attempt A001.
- Added `lib/tnfs_cost.py`, four exact family evaluators in `lib/curves.py`, and seven shared known-answer tests.
- Added the deterministic search/extrapolation CLI and its subprocess smoke test.
- Verified primary literature and recorded six references.
- Generated the bounded-search CSV, 36-row sensitivity CSV, and JSON proof-scope summary.

**Found:**
- [EMPIRICAL: BD19 BN fixture, final stable evaluator] The finite model returns 99.573 bits against 99.69 published, a 0.117-bit difference within the declared 0.2-bit tolerance.
- [EMPIRICAL: published BLS12-381 constants] The generated $p$ and $r$ match exactly and the least embedding degree is 12.
- [EMPIRICAL: every integer seed $-10{,}000\le u\le10{,}000$, $p<2^{60}$] The accepted counts are BN 273, BLS12 24, BLS24 5, and KSS16 0; no accepted row meets any production target.
- [PROVED] In the implemented four-family leading-term objective, BN is the unique minimum estimated $\rho$ at 128, 192, and 256 bits under every sensitivity scenario.
- [EMPIRICAL: three named scenarios] The selected family is stable, while the estimated BN field size changes by roughly 45–47% between calibrated special-form and composite-exTNFS scenarios.

**Prediction vs. outcome:** [EMPIRICAL: session 1] Partly matched. The explicit finite-size equation reproduced the BN anchor without a fitted overhead, which was better than predicted; cross-family finite-size validation still remains Q009, and the practical recommendation differs once operation cost is made an objective.

**Did not work:** [EMPIRICAL: stated toy interval] No prime KSS16 fixture was found in the original bounded scan. Treating the raw BN factor base as the relation target also appeared to miss sufficiency by about 0.03 bits; the final implementation distinguishes the raw factor base from the Galois-reduced target required by the paper.

**Changed my mind about:** [PROVED] The formal minimum-$\rho$ objective is too narrow to reproduce practical family recommendations; it selects BN even when higher-$\rho$ families have far smaller base fields and pairing proxies.

**Next:** Implement the published norm sampling process for BLS12 and attempt an independent finite-size match without recalibration.
