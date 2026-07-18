# Log — P2.2

## Session 1 — 2026-06-30

**Goal:** Complete SG-01 and SG-02 far enough to support one explicit failed
reduction attempt for SG-04 and a precisely scoped SG-05 target.

**Prediction (written before literature search):** [CONJECTURE] The clean graph will be much
sparser than survey terminology suggests: several apparent “implications” will
turn out to compare differently typed or differently parameterized variants.
The direct SXDH attempt will fail at challenge embedding because a constant-size
DDH/SXDH tuple exposes only a fixed-dimensional rational-function span, whereas
the $q$-SDH adversary expects $q+1$ correlated powers.

**Did:**
- Initialized the problem record after confirming that the target folder was absent.
- Ran `env/check_env.py`; Python 3.13.4 is available and SageMath, Singular, and
  msolve are unavailable.
- Read the primary definitions and proof bodies in Boneh–Boyen,
  Boneh–Boyen–Goh, Chase–Meiklejohn, Cheon, and Lu–Zhandry.
- Fixed typed notation, audited every implication edge and loss, catalogued the
  static candidates, and completed A001 and A002.
- [EMPIRICAL: Python 3.13.4 on 2026-06-30] Ran the repository unit suite; all
  45 tests discovered in the final run passed.

**Found:**
- [CITED] Lu and Zhandry already prove the precisely scoped separation sought
  here: a fully black-box generic reduction from prime-order $q$-SDH to a true
  fixed-size assumption would generically break that fixed-size assumption.
  [Lu–Zhandry 2024]
- [CITED] The exact thresholds are $n<q-1$ without pairing and
  $\binom{n+2}{2}<q$ with a bilinear map.  [Lu–Zhandry 2024]
- [PROVED] The direct straight-line SXDH embedding fails before the first
  oracle call because the random DDH exponent span cannot contain both a
  nonconstant $x$ and $x^2$.
- [CITED] Composite-order Déjà Q is the positive counterpoint and does not
  contradict the prime-order meta-reduction.  [Chase–Meiklejohn 2014;
  Lu–Zhandry 2024]

**Prediction vs. outcome:** [PROVED] The predicted fixed-dimensional embedding
failure was correct, and the graph was sparse once variants were typed.
[CITED] The unexpected outcome was that the broader generic meta-reduction had
already been proved, so SG-05 could be completed rather than merely posed as a
target.  [Lu–Zhandry 2024]

**Did not work:** [PROVED] A001 cannot embed a nontrivial $q$-SDH ladder from a
single DDH/SXDH challenge in the stated straight-line algebraic class.

**Changed my mind about:** [CITED] The prompt's table made Coron-style meta-reduction
work look prospective, but the current best-known result is the explicit
Lu–Zhandry prime-order separation.  The problem should be labeled partial, not
open, for the scoped generic class.  [Lu–Zhandry 2024]

**Next:** Pursue Q003 only if a separation beyond generic/algebraic fully
black-box reductions is required.

**End checklist:**

- [x] Log includes prediction versus outcome.
- [x] State and next action updated.
- [x] A001 has a post-mortem; A002 records the completed scoped result.
- [x] [PROVED] Every new mathematical claim is tagged and no `[UNVERIFIED]` remains.
- [x] No new script was needed for this theory session.
- [x] Bibliography and glossary updated.
- [x] Handoff regenerated below 120 lines and is sufficient for resumption.

## Session 2 -- 2026-07-09

**Goal:** Formalize the strongest clean corollary for reductions that are
uniform over prime-order group representations, then attempt to remove that
uniformity and identify the exact failure point.

**Prediction (written before the session-2 literature search):** [CONJECTURE]
Any single standard-oracle reduction required to work over every admissible
prime-order group representation is already covered by the Lu--Zhandry
type-safe/generic-representation formulation after instantiation with a random
sparse encoding.  A reduction guaranteed only for one concrete representation
escapes because the meta-reduction is not entitled to replace that
representation by a random relabeling.

**Baseline:** [EMPIRICAL: Python 3.13.4 on Windows 11, 2026-07-09]
`env/check_env.py` completed successfully; SageMath, GP/PARI, Singular, and
msolve are unavailable.  All 53 tests discovered by the repository unit suite
passed before session-2 research began.

**Did:**
- Read Lu--Zhandry Sections 1.3--1.4, 2, 3.2--3.5 and the proofs of Lemmas
  3.1--3.2, then checked Reingold--Trevisan--Vadhan Definition 3 in the primary
  text.
- Completed A003 by defining UR-FBB with a representation-independent success
  lower bound and proving that it implies GR-BB.
- Ran A004: attempted to randomly relabel a reduction promised only for a
  concrete representation, and preserved the failed attempt with two exact
  failure points.
- Cross-checked title/author/ePrint searches and citation indexes through
  2026-07-09; added the 2025 BBS/BBS+ concrete-security result and the 2026 BBS
  tightness result to the scheme taxonomy.

**Found:**
- [CITED] GR machines may inspect actual encoding bits; their uniformity comes
  from advantage defined over every possibly inefficient group implementation.
  [Lu--Zhandry 2024, §3.2]
- [PROVED] A classical fixed-transformer, fully-black-box reduction with a
  pointwise guarantee over all such representations is a strict special case of
  GR-BB and is ruled out for $q$-SDH at the existing thresholds.
- [PROVED] A guarantee over only efficient/standardized representations is not
  enough for this corollary if that class omits the possibly inefficient random
  sparse representation used by the wrapper.
- [CITED] Current BBS/BBS+ work reinforces rather than removes $q$-dependence:
  scheme security implies $\Theta(q)$-SDH for the audited variants, and a later
  tight proof still assumes $q$-SDH.  [Chairattana-Apirom--Tessaro 2025;
  Chairattana-Apirom--Hofheinz--Tessaro 2026]

**Prediction vs. outcome:** [PROVED] The central prediction was correct: true
representation uniformity collapses A003 to GR-BB, while A004 fails at the
representation quantifier.  The refinement discovered during validation is
that “all efficient representations” is still weaker than the required
quantifier and must remain in the residual gap.

**Did not work:** [PROVED] From a premise for $G_*$, random relabeling needs a
conclusion for $G_L$ that is not logically available.  Native encoding
operations also need not emit algebraic explanations, so the fixed-span trace
cannot be reconstructed from group-operation queries alone.

**Changed my mind about:** [PROVED] The residual representation-dependent case
is broader than a single named elliptic curve: any promised representation
class not closed under information-theoretic random sparse relabeling remains
outside A003, including an efficient-only class.

**Next:** Q003 is now narrowed to a representation class excluding random
sparse implementations, or to non-black-box use of the adversary's code.  A new
simulation invariant or a positive reduction is required; repeating random
relabeling is not useful.

**End checklist:**

- [x] Log includes prediction versus outcome.
- [x] A003 is completed and A004 has a precise post-mortem.
- [x] [PROVED] New mathematical claims are tagged; no unresolved
  `[UNVERIFIED]` claim was introduced.
- [x] Bibliography, glossary, open question, state, and handoff updated.
- [x] [EMPIRICAL: Python 3.13.4 on Windows 11, 2026-07-09] The final validation
  run passed all 62 tests discovered by the repository unit suite.

## Session 3 -- 2026-07-18

**Goal:** Determine whether the GR-BB impossibility can be extended from all
possibly inefficient representations to a fully-black-box reduction guaranteed
over every efficiently computable representation.

**Prediction (written before session-3 literature search):** [CONJECTURE] An
efficient sparse encoding cannot unconditionally replace the uniformly random
injection because its finite description is detectable by a possibly
inefficient adversary.  A finite-wise independent encoding works only if all
relevant group queries are polynomially bounded, and a PRP substitution adds a
computational premise rather than yielding the desired unconditional
meta-reduction.

**Refuting test:** [PROVED] Construct an efficient information-theoretic
encoding wrapper for the full adversary/reduction interaction, or prove from
the model that only a polynomial-query transcript must be simulated.

**Baseline:** [EMPIRICAL: Python 3.13.4 with NumPy 2.4.6 on Windows 11,
2026-07-18] `env/check_env.py` completed successfully; all 64 tests discovered
by the repository unit suite passed before session-3 research began.

**Did:**
- Completed A005 by proving the finite-seed support distinguisher and
  separating it from the named-representation quantifier obstruction.
- Audited Zhandry's labeling/query-cost model and the 2025 sparse-GGM
  separation, then recorded why finite-wise independence and a PRP do not
  preserve the possibly inefficient adversary class.
- Completed A006: defined execution-wise native freshness, enlarged the
  Lu--Zhandry coefficient dictionary, and proved the resulting fixed-
  representation meta-reduction.
- Re-read Lemma 5.1 and the full dictionary/root-list proof of Theorem 5.2 to
  verify the column-count substitution and the inclusion
  $M(b/w)^T=(s_1(x),\ldots,s_q(x))^T$.
- Audited the 2026 structured generic-group model and ran A007 against the
  proposed density-to-freshness transfer.

**Found:**
- [PROVED] A polynomial-seed sparse encoding cannot replace an information-
  theoretic random injection for a possibly inefficient adversary: exhaustive
  seed enumeration distinguishes their table supports with overwhelming
  advantage.
- [PROVED] For a named efficiently operated representation, an $s$-fresh
  fully-black-box reduction yields a PPT fixed-assumption attack when
  $n+s<q-1$.  The proof tolerates adaptive encoding-bit branches, hidden
  relations among fresh labels, collisions, and multiple oracle calls.
- [PROVED] For typed source-valued $q$-SDH in a pairing setting, pairing
  outputs do not enlarge the source trace.  The sharper condition is
  $n_1+s_1<q-1$ absent an unrecorded target-to-source conversion; the quadratic
  trace bound remains a safe extension for broader target-valued bilinear
  $q$-type games.
- [CITED] Structured-GGM Theorem 3.2 bounds a random-hybrid event using
  constrained-label density and charges only generic group-oracle queries.
  [Corrigan-Gibbs--Henzinger--Wu 2026]
- [PROVED] Consequently, density $\delta$ alone does not bound the number or
  rank of native labels deliberately selected by a reduction.

**Prediction vs. outcome:** [PROVED] The session prediction was correct about
efficient sparse encodings: finite descriptions fail information-
  theoretically and PRPs add a computational restriction.  The constructive
surprise was A006: random relabeling is unnecessary once the number of native
fresh labels is explicitly bounded, because one coordinate per label restores
the root-list invariant.

**Did not work:** [PROVED] A005's efficient-encoding substitution fails against
unbounded computation, and A007's structured-density transfer fails because a
probability mass bound is not an execution-wise trace-dimension bound.

**Changed my mind about:** [PROVED] The residual fixed-representation gap is
not usefully described as “any native encoding operation.”  Bounded native
operations are now covered; the remaining resource is source-label rank large
enough to grow linearly with the $q$-SDH ladder, or an unrecorded conversion
that supplies such labels.

**Next:** Pursue Q003 only through a new invariant for linear native-label rank
or an explicitly non-black-box construction.  Do not repeat random relabeling,
finite-seed substitution, or density-to-count transfer.

**End checklist:**

- [x] Log records prediction versus outcome and both failed attempts have
  post-mortems.
- [x] State, sub-goals, bibliography, glossary, open question, and handoff are
  updated.
- [x] [PROVED] New mathematical claims are tagged and no unresolved
  `[UNVERIFIED]` claim was introduced.
- [x] [PROVED] A006 states the reduction class, validity interfaces, exact
  dimension invariant, success loss, and remaining scope.
- [x] [EMPIRICAL: Python 3.13.4 on Windows 11, 2026-07-18] All 69 shared-library
  tests passed.  The full repository suite passed 274 tests and 3 subtests; one
  unrelated P1.1 display-format assertion failed.
- [x] [PROVED] `HANDOFF.md` remains below its 120-line cap and suffices for
  resumption.
