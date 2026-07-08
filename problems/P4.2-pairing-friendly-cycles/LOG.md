# Archived log - P4.2 - sessions 1-3 through A016

## Session 1 - 2026-06-27

**Goal:** Complete SG-01 and reconstruct the published parameter-\(x=3\)
MNT6/MNT4 2-cycle end to end for SG-02, with exhaustive and BSGS point counts
on both curves and exact embedding-degree checks.

**Prediction (written before running the P4.2 computation):** [CONJECTURE] The
published equations over \(\mathbb F_{37}\) and \(\mathbb F_{43}\) will have
orders 43 and 37 under both point-counting methods, and their exact embedding
degrees will be 6 and 4. This prediction is refuted by any order mismatch, any
smaller exponent producing residue 1, or disagreement between the two point
counts.

**Positive result criterion:** [CONJECTURE] Both independently implemented
point counts agree with the published order on each curve, the two orders close
the cycle, and the exact embedding-degree checks return \((6,4)\).

**Negative result criterion:** [CONJECTURE] Any published coefficient fails to
define a nonsingular curve, either point-counting path disagrees with the stated
order, the cycle equalities fail, or either exact embedding degree differs from
the published value.

**Did:**
- Loaded `00_SCAFFOLD.md` and the supplied P4.2 problem statement.
- Initialized the P4.2 persistent files because no prior P4.2 state existed.
- Ran `env/check_env.py`: Python 3.13.4 is available; SageMath, Singular, and
  msolve are unavailable.
- Ran all 34 pre-existing shared-library tests successfully.

**Found:** Pending the predeclared computation.

**Prediction vs. outcome:** Pending.

**Did not work:** Pending.

**Changed my mind about:** Pending.

**Next:** Run the published MNT regression and record the exact results.

### SG-04 pre-run amendment

**Goal:** After the positive SG-02 regression, freeze and exhaust the prime
space in `SEARCH_SPACE.md`.

**Prediction (written before the SG-04 full computation):** [CONJECTURE] The
search will reproduce the known \((6,4)\) arithmetic pairs and find no hit with
a different degree pair. This is refuted by any full hit outside \((6,4)\) or
failure to recover \((37,43,6,4)\).

**Prediction after the smoke run, before explicit construction:**
[CONJECTURE] Every arithmetic hit from the full search can be instantiated as
two explicit short-Weierstrass curves within 20,000 seeded model trials per
curve, and both a Hasse/BSGS count and direct equation enumeration will return
the target orders. Failure for any hit refutes this validation prediction; it
does not refute existence of the corresponding isogeny class.

### SG-05 pre-run amendment

**Goal:** Derive the directed length-3 equations and exhaust the frozen
16-bit, degree-at-most-12 space in `THREE_CYCLE_CONDITIONS.md`.

**Prediction (written before the SG-05 computation):** [CONJECTURE] No directed
triple will have all three exact embedding degrees in 3 through 12. Any such
triple refutes the prediction and must be explicitly constructed before being
treated as an exhibited cycle.

**Prediction after the SG-05 search, before explicit construction:**
[CONJECTURE] All five arithmetic hits can be instantiated within 20,000 seeded
coefficient trials per curve, and both point-counting paths will match all 15
target orders. Any mismatch or exhausted model search refutes this validation
prediction.

### SG-06 pre-run amendment

**Goal:** Hold the 16-bit prime space fixed and raise only the exact embedding
degree ceiling from 12 to 18 for lengths 2 and 3.

**Prediction (written before the SG-06 computation):** [CONJECTURE] At least
one degree-12 near-miss will become a full hit. This is refuted if both the
2-cycle and 3-cycle full-hit ledgers are unchanged.

### Session 1 completion

**Did:**
- Derived the general trace equations, the telescoping trace sum, the 2-cycle
  Frobenius-discriminant identity, and the directed 3-cycle degree conditions.
- Reproduced the published parameter-3 MNT6/MNT4 cycle using two point-counting
  paths and exact residue checks.
- Froze the 16-bit, degree-12 2-cycle space before searching it; enumerated all
  21,382,530 unordered prime pairs and 204,074 Hasse-valid pairs.
- Constructed and independently counted all 52 curves from the 26 primary
  2-cycle hits.
- Froze the analogous directed 3-cycle space before searching it; enumerated
  408,148 Hasse edges and 6,922,890 directed triangles.
- Constructed and independently counted all 15 curves from the five primary
  directed 3-cycle hits.
- Raised only the degree ceiling to 18 and independently verified all 36
  2-cycle hits and all 12 directed 3-cycle hits in the relaxed ledgers.
- Added nine P4.2 tests, a results write-up, two primary-source notes, and the
  resume packet.

**Found:**
- [EMPIRICAL: published fields 37 and 43] The MNT regression has orders 43 and
  37, traces -5 and 7, common CM radicand 123, and exact degrees (6,4).
- [EMPIRICAL: distinct primes below 2^16, exact degrees 3 through 12] The
  primary 2-cycle census has 26 full hits and 219 one-sided near-misses. Five
  hits have degree pairs outside {(6,4),(4,6)}, all with larger field at most
  31 (`RESULTS.md`).
- [EMPIRICAL: three distinct primes below 2^16, exact degrees 3 through 12]
  The primary directed 3-cycle census has five full hits and 37 two-of-three
  near-misses; every hit uses fields at most 43 (`RESULTS.md`).
- [EMPIRICAL: same prime bounds, exact degrees 3 through 18] The controlled
  relaxation has 36 2-cycle hits and 12 directed 3-cycle hits, all explicitly
  and independently verified (`RESULTS.md`).
- [PROVED] Standard prime-order \(\rho_{\max}<2\) is automatic for distinct
  2-cycles over fields at least 5, so Q010 asks which alternate metric the
  supplied question intended.

**Prediction vs. outcome:** The MNT reproduction prediction matched. Both
no-exception search predictions failed: tiny exceptional 2-cycles and directed
3-cycles exist. Both explicit-construction predictions matched. The degree-18
relaxation prediction matched, adding ten 2-cycles and seven 3-cycles.

**Did not work:** The shared BSGS counter occasionally failed to isolate very
small random model orders within 32 samples. The construction scripts record
these skips explicitly as `bsgs_isolation_failures` and continue to a model on
which BSGS succeeds; every retained model is then independently enumerated.
SageMath was unavailable. `lib/tnfs_cost.py` was absent during the searches but
appeared via a concurrent workspace update before the final shared test pass;
the bounded searches do not import it.

**Changed my mind about:** [EMPIRICAL: primary 16-bit spaces] Pairing-friendly
cycles of lengths 2 and 3 are not absent at toy scale; the obstruction is to
large or scalable instances. [PROVED] The prompt's \(\rho<2\) question cannot
use the standard prime-order maximum without becoming automatic.

**Next:** Extend the prime limit to \(2^{18}\) at the unchanged primary degree
ceiling 12, preserving the same candidate-ledger and independent-construction
rules.

**Final validation:** [EMPIRICAL: Python 3.13.4, 2026-06-27] All 53 shared
tests and all nine P4.2 tests passed after the concurrent shared-library update.

## Session 2 - 2026-07-08

**Goal:** Extend both primary deterministic searches from primes below
\(2^{16}\) to primes below \(2^{18}\), keep exact embedding degrees 3 through
12, and independently verify every newly appearing full hit.

**Prediction (written before running either extension):** [CONJECTURE] The
larger range will add only 2-cycle hits with degree pairs (6,4) or (4,6), and
will add no full directed 3-cycle. This is refuted by a new non-{(6,4),(4,6)}
2-cycle or any new full 3-cycle.

**Positive result criterion:** [CONJECTURE] The full enumerations complete,
the embedded 16-bit counts are recovered as a strict subset, and every new hit
passes both point counters and exact degree checks.

**Negative result criterion:** [CONJECTURE] A deterministic search or subset
check fails, or a newly appearing arithmetic hit cannot be independently
instantiated and counted within the declared 20,000-trial construction bound.

**Did:**
- Reconciled session-1 state and found no incomplete attempt or stale handoff.
- Ran `env/check_env.py`; Python 3.13.4 is available and SageMath, GP,
  Singular, and msolve are unavailable.
- Ran all 55 current shared tests and all nine P4.2 tests successfully.
- Froze the one-axis extension in `EXTENSION_18BIT.md`.

**Found:** Pending the predeclared searches.

**Prediction vs. outcome:** Pending.

**Next:** Run the 18-bit 2-cycle census, then the directed 3-cycle census.

### A005 outcome and A006 pre-run amendment

**A005 outcome:** [EMPIRICAL: primes below 2^18, exact degrees 3 through 12]
The extension added eight MNT-pattern 2-cycle hits, no exceptional 2-cycle,
and no 3-cycle candidate row. All 68 curves in the 34-hit extended 2-cycle
ledger passed both point counters.

**A006 goal:** Validate a target-edge-complete 3-cycle algorithm against both
prior bounds, then extend the unchanged primary conditions to primes below
\(2^{20}\).

**A006 prediction (written before implementation and execution):**
[CONJECTURE] Targeted and exhaustive candidate rows will agree exactly below
\(2^{16}\) and \(2^{18}\). The 20-bit extension will add only MNT-pattern
2-cycles and no new 3-cycle candidate row.

**A006 outcome:** [EMPIRICAL: primes below 2^20, exact degrees 3 through 12]
Only 13 MNT-pattern 2-cycle hits were added and all were independently
verified. No 3-cycle hit appeared, but three two-of-three near-misses refuted
the stronger no-new-candidate prediction. Their missing exact degrees are
483882, 2055, and 115320.

**A007 goal:** Validate a candidate-complete targeted 2-cycle algorithm and
extend both primary searches to primes below \(2^{22}\).

**A007 prediction (written before implementation and execution):**
[CONJECTURE] All new 2-cycle hits will have degree pair (6,4) or (4,6), and no
new full directed 3-cycle will appear. New near-misses are allowed.

### A009 pre-run amendment

**Goal:** Prove that the consecutive MNT prime 3-chain
\((4x^2-2x+1,4x^2+1,4x^2+2x+1)\) cannot close in either orientation with all
exact degrees at most 12.

**Prediction (written before the finite remainder search):** [CONJECTURE] The
linear recurrence rules out every \(x\ge1026\), and exhaustive enumeration of
\(1\le x\le1025\) will find no closing degree at most 12. One finite hit
refutes the claim.

### Session 2 completion

**Did:**
- Completed the exhaustive 18-bit primary searches and constructed every
  2-cycle hit in the extended ledger.
- Proved candidate completeness for target-edge 2-cycle and 3-cycle searches,
  validated their rows against prior exhaustive ledgers, and extended both
  primary spaces to 20 and 22 bits.
- Computed the exact missing degrees of every newly appearing 3-cycle
  near-miss.
- Constructed and independently counted all 13 new 20-bit 2-cycles and all 29
  new 22-bit 2-cycles.
- Proved an elementary converse identifying every exact degree-(6,4) or
  degree-(4,6) prime-order 2-cycle with the standard MNT parameter formulas.
- Derived a quadratic remainder recurrence and excluded closure of the
  consecutive MNT prime 3-chain for every integer parameter.

**Found:**
- [EMPIRICAL: primes below 2^22, exact degrees 3 through 12] There are 76
  2-cycle hits and 819 one-sided near-misses. The five exceptional hits are
  unchanged from 16 bits; all 71 degree-{4,6} hits match the MNT formulas.
- [EMPIRICAL: three distinct primes below 2^22, exact degrees 3 through 12]
  There are five directed 3-cycle hits and 42 two-of-three near-misses. No hit
  contains a field above 43.
- [PROVED] Every exact degree-(6,4) or degree-(4,6) prime-order 2-cycle is an
  MNT polynomial instance (`MNT_CLASSIFICATION.md`).
- [PROVED] The consecutive MNT 3-chain never closes in either orientation
  with all exact degrees in 3 through 12
  (`MNT_THREE_CHAIN_OBSTRUCTION.md`).

**Prediction vs. outcome:** A005 and A007 matched fully. A006 matched on full
hits but not on its stronger near-miss prediction. A009 matched: the four
all-prime parameters at most 1025 have closing degrees above 12, and the
remainder proof covers all larger parameters.

**Did not work:** A first 20,000-trial construction cap missed one 20-bit
curve. Adding quadratic-twist complement recovery and raising the declared cap
to 100,000 found it; the later 22-bit construction needed at most 43,462
trials. Exhaustive directed-triangle enumeration became wasteful beyond 18
bits, so the candidate-complete target-edge join replaced it.

**Changed my mind about:** The persistent large 3-cycle near-misses are not
evidence that the consecutive MNT chain is close to closing: their missing
orders grow far beyond the target interval, and the entire class is now
excluded by a parameter-uniform remainder argument.

**Next:** Classify the remaining non-MNT two-target-edge near-miss families
before extending the finite bound again.

**Final validation:** [EMPIRICAL: Python 3.13.4, 2026-07-08] All 69 shared
tests and all 19 P4.2 tests passed. Every P4.2 Python file compiled, and
cross-file certificate assertions recovered 76/819 2-cycle hits/near-misses,
5/42 3-cycle hits/near-misses, 58 correctly counted new 22-bit curve rows, 71
MNT parameter rows, and four non-closing all-prime MNT triples.
