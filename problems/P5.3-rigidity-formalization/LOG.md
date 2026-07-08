# Log — P5.3

## Session 1 — 2026-06-25

**Goal:** Define a sound rigidity game and choice accounting, prove its main
bound, and use primary specifications to audit five named standard curves.

**Prediction (written before running literature or mathematical checks):** The
bound \(\min(1,2^b\epsilon)\) will follow by a union bound only when the weak
set and designer menu are fixed independently of the generator's fresh random
experiment and every menu entry has weak-set probability at most \(\epsilon\).
Published standards will support exact replay descriptions, but most will not
identify the historical alternative menu, so honest provenance values of
\(b\) will require bounds or an explicit sensitivity profile rather than a
single unconditional number.

**Did:**

- Initialized the P5.3 problem folder and A001.
- Ran `env/check_env.py` and the shared library tests: Python 3.13.4 was
  available, SageMath/Singular/msolve were unavailable, and all 39 tests
  passed.
- Defined a fixed-menu selective-generation game, category accounting,
  projection-sensitive selection capacity, and a reference-source domination
  factor.
- Proved the union bound, gave tight examples, and recorded three quantifier
  failures.
- Constructed an ideal minimal-designer-freedom generator and separated its
  information-theoretic statement from a conditional XOF/beacon refinement.
- Audited P-256, Curve25519, brainpoolP256r1, secp256k1, and BLS12-381 from
  primary specifications or the original construction source.
- Added six source records, repository bibliography/glossary entries, and two
  concrete open questions.
- Implemented and tested the SG-08 toy exact-rejection sampler. The final
  combined suite passed 58 tests, including 3 P5.3 tests.

**Found:**

- [PROVED] If every candidate marginal is dominated by \(\kappa\nu\) and the
  safe weak-set mass under \(\nu\) is at most \(\epsilon\), success is at most
  \(\min(1,2^b\kappa\epsilon)\); candidate independence is unnecessary.
- [PROVED] The requested \(\min(1,2^b\epsilon)\) result is the uniform-source
  case, and it is tight for correlated translated candidates with disjoint
  hit events.
- [PROVED] Without fresh randomness independent of the weak set, \(b=0\)
  expresses reproducibility but does not itself give a probability bound.
- [CITED] Under A256, P-256 has a curve-core cap of 161 bits conditional on
  its field/model/hash rule; Curve25519 given \(p\) and brainpoolP256r1 have
  zero core bits; Curve25519 and Brainpool each expose at most one
  package-only sign bit under the full affine-point projection.
- [CITED] The audited SEC 2 section for secp256k1 and the original BLS12-381
  construction note do not expose finite menus from which unconditional
  provenance \(b\) values can be computed.
- [CONDITIONAL: ideal-XOF outputs are independent uniform byte strings] The
  toy first-passing sampler is uniform over the coefficient encodings passing
  its fixed public predicate.
- [EMPIRICAL: bits=7, p=127, 8 beacon labels] All smoke labels passed by
  counter 13; deterministic replay and independent point enumeration passed.

**Prediction vs. outcome:** matched. The union bound required a marginal
source condition in addition to the quantifier order, and the audit produced
conditional caps plus explicit non-identifiability rather than five
unconditional historical numbers.

**Did not work:** Treating encoded literal length as designer freedom was
rejected because it confuses deterministic outputs with menu size. A single
combined patch also failed on legacy repository text encoding; it was split
into isolated, non-destructive edits with no partial change.

**Changed my mind about:** A deterministic zero-choice generator is not by
itself the desired probabilistic construction. The clean minimum needs either
fresh entropy outside the designer's control or an explicit distribution on
weak sets.

**Next:** Investigate Q014 using archival, pre-publication sources for finite
secp256k1 or BLS12-381 candidate menus; do not replace missing evidence with
later folklore.

## Session 2 — 2026-07-01

**Goal:** Resolve Q014 as far as the surviving primary record permits and
formalize what can still be proved when the historical candidate menu is not
recoverable.

**Prediction (written before the Session 2 archival search):** Primary SEC 2
editions and dated BLS12-381 implementation history will probably confirm the
published constants and some design criteria, but not a precommitted exhaustive
candidate domain, ordering, and stopping rule.  If that prediction holds, the
positive result will be a provenance non-identifiability theorem: the same
published output is compatible with histories having different menu sizes, so
no function of the final specification alone can recover historical \(b\). A
verifiable provenance certificate will therefore have to commit, before the
fresh experiment, to the meta-specification, candidate domain, enumeration,
stopping rule, randomness origin, equivalence convention, and complete replay
transcript.

**Baseline:** `env/check_env.py` passed with Python 3.13.4; SageMath, GP,
Singular, and msolve were unavailable.  The combined suite passed 61 tests.

**Did:**

- Audited SEC 2 version 1.0 in addition to version 2.0 and recorded the
  original broad repeated-selection criterion for prime-field Koblitz curves.
- Followed the BLS12-381 announcement's implementation link to the surviving
  `zkcrypto/pairing` history, inspected every reachable root, and verified that
  `a06216f` is the sole zero-parent commit, dated July 8, 2017.
- Extracted the initial BLS12-381 README's field-size bounds, residue
  subfamily, low-Hamming-weight objective, optimization claim, and canonical
  G1/G2 generator rule.
- Proved the final-output non-identifiability theorem and a seeded-replay
  corollary, then specified a sufficient provenance certificate.
- Updated the A256 category vector, result table, judgement calls, source
  records, bibliography, open questions, state, subgoals, and handoff.
- Re-ran the environment check, compilation, full tests, tag scan, and
  Markdown control-character scan.

**Found:**

- **[CITED]** SEC 2 v1 says endomorphism-compatible parameters were repeatedly
  selected until a prime-order curve was found, but does not publish the
  candidate domain, order/distribution, failures, or generator derivation.
- **[CITED]** The earliest surviving linked BLS12-381 commit gives materially
  stronger replay evidence than the announcement, including a canonical
  generator rule, but its incomplete \(u\)-domain/objective order and
  post-announcement date do not certify a historical menu.
- **[PROVED]** For any final projected output \(x\), public-output-only
  histories can realize every menu size \(1\leq M\leq|\Omega|\); therefore no
  estimator of the final output alone recovers historical \(b\).
- **[PROVED]** BLS12-381's generator-only residual freedom is zero conditional
  on the surviving canonical rule, while both unconditional A256 capacities
  remain \(\bot\) because the \(u\)-menu is not identified.
- **[EMPIRICAL: final 2026-07-01 validation]** All 66 tests passed in 1.56
  seconds, `compileall` succeeded, no unresolved-status tags remained, and no
  unexpected control characters occurred in P5.3 Markdown files.

**Prediction vs. outcome:** Mostly matched. Neither source yielded a complete
historical menu. The positive archival evidence was stronger than predicted:
SEC 2 v1 supplies a broad stopping criterion, and the initial BLS12-381
repository README supplies a canonical generator rule and an optimization
claim.

**Did not work:** A public Web Archive CDX request timed out, so it supplied no
pre-publication snapshot. The reachable `pairing` Git history begins four
months after the announcement and contains no selection script or rejection
transcript.

**Changed my mind about:** The original BLS12-381 announcement alone leaves
the package generators opaque, but the surviving initial repository commit
supports zero residual generator choice conditional on its conventions. This
does not change the unconditional \(\bot\), which is driven by \(u\).

**Next:** No action is required for the stated P5.3 deliverables. Reopen Q014
only if a dated pre-publication artifact fixes the missing finite domain,
selection order/objective priority, and transcript.

## Session 3 — 2026-07-08

**Goal:** Exhaust the versioned package artifacts omitted by A003 and close
Q015's remaining sampling-kernel ambiguity at the permitted toy scale.

**Prediction (written before the Session 3 registry search or new
experiments):** Because the surviving `pairing` root already declares version
0.9.0, crates.io or docs.rs will preserve versions 0.8.x or earlier that
predate the July Git rewrite. They may move the archival boundary earlier and
recover generator implementation details, but probably will not contain a
precommitted exhaustive BLS12-381 \(u\)-menu. For Q015, exact enumeration at
\(p=127\) will show that uniform safe coefficient encodings are not uniform
over \(\mathbb F_p\)-isomorphism classes; a canonical safe-class unranking
kernel should remove that ambiguity with designer capacity \(b=0\).

**Baseline:** `env/check_env.py` passed with Python 3.13.4; the combined suite
passed 68 tests.

**Did:**

- Checked the crates.io API and docs.rs version index, recorded the primary
  links in `refs/crates-pairing2017.md`, and added the result to the audit.
- Implemented `code/class_uniform_kernel.py` with explicit scaling orbits,
  lexicographic canonical representatives, exact safe-class enumeration, and
  SHAKE256 rejection/unranking.
- Added five focused kernel tests, generated the 67-row JSON/CSV census, and
  replayed both outputs byte-for-byte.
- Updated `DEFINITIONS.md` with the short-Weierstrass isomorphism criterion,
  orbit-projection formula, fixed-universe minimax theorem, and forced
  class-uniform generator.

**Found:**

- **[CITED]** The public crates.io/docs.rs history starts at `pairing` 0.9.0
  on 2017-07-08. It contains no 0.8.x or earlier snapshot, so the predicted
  pre-0.9 registry channel does not exist.
- **[EMPIRICAL: exhaustive enumeration at \(p=127\)]** The 16,002
  nonsingular coefficient encodings form 258 classes with orbit histogram
  \(\{21:6,63:252\}\). The safety predicate retains 4,179 encodings in 67
  classes with histogram \(\{21:1,63:66\}\).
- **[PROVED]** Conditional on those exact counts, coefficient-uniform class
  masses are \(1/199\) and \(3/199\), class-uniform mass is \(1/67\), and the
  total-variation distance is \(132/13333\).
- **[CONDITIONAL: SHAKE256 blocks are independent uniform strings]** The A004
  rank sampler is exactly uniform over the 67 safe classes; with an
  unselectable, non-restartable, non-suppressible beacon its designer capacity
  is \(b=0\).
- **[PROVED]** Uniform is the unique distribution on a fixed finite universe
  whose maximum singleton probability reaches the lower bound \(1/N\).
- **[EMPIRICAL: final 2026-07-08 replay]** The JSON SHA-256 is
  `1BA019A7DA47C2FB64764B3D9A79680C7CB2904D6AD9062899069689AEB03F15`
  and the CSV SHA-256 is
  `EDC4C7875E2CE7A0AB0F44529BD65A99D35ADF5A57C8E485070B983DBFD382A9`.

**Prediction outcome:** The predicted coefficient-to-class bias and its
class-uniform repair were confirmed. The predicted earlier registry versions
were falsified: version 0.9.0 is the registry boundary.

**Did not work:** Searching for pre-0.9 registry packages could not move the
archival boundary because neither registry indexes such a version. Casting
every API version to PowerShell's `System.Version` also rejected a modern
prerelease label; the returned metadata itself remained usable and the dated
version boundary was independently checked against docs.rs.

**Changed my mind about:** Coefficient-uniform rejection is exact for the
encoding projection but is not the strongest fixed-profile answer. Once the
equivalence projection is fixed to isomorphism classes, canonical
class-uniform unranking supplies the unique minimax singleton distribution.

**Final validation:** **[EMPIRICAL: combined shared and P5.3 suite]** All 77
tests passed; `compileall` succeeded, the unresolved-status scan was empty,
and the Markdown control-character scan was clean.

**Next:** None at the authorized scope. Reopen Q014 only on a dated
pre-publication artifact fixing the missing historical fiber. Treat any
production-scale sampling profile as a new, separately authorized problem.

### Correction to Session 3 final validation

The scaffold audit required an explicit `--smoke` mode in the new class
kernel. It now runs the fixed \(p=31\) profile, has a dedicated CLI regression
test, and leaves the checked-in \(p=127\) data unchanged.

**[EMPIRICAL: corrected combined shared and P5.3 suite]** All 78 tests passed
in 11.27 seconds; the six A004 kernel tests passed in 3.33 seconds, and
`compileall` succeeded.
