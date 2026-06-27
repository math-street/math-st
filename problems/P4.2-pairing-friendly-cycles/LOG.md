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
