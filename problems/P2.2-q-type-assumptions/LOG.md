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
