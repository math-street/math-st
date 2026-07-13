# Archived session log — sessions 1–5

## Session 1 — 2026-06-22

**Goal:** Establish SG-01 at the three requested bit sizes and, if runtime
permits, use the same harness for the SG-03 integer-$x$ candidate.

**Prediction (written before running anything):**

- [HEURISTIC] For random bases, the mean ordered decomposition count will be
  within 15% of $s^3/r$ at each tested size. This prediction is falsified at a
  size if the reported 95% interval for the normalized mean excludes
  $[0.85,1.15]$.
- [HEURISTIC] Candidate A will not change the normalized mean count by more
  than 20% relative to a size-matched random base. This prediction is falsified
  if the 95% interval for the ratio of normalized means excludes
  $[0.8,1.2]$.
- [HEURISTIC] A lexicographic pair scan will require work on the order of
  $r/s$, not a polynomial in $\log p$. A three-size log-log slope inconsistent
  with $1/2$ by more than 0.2, or a candidate-specific polylogarithmic method,
  would falsify this session-level prediction.

**Did:**

- Initialized the problem folder because no P1.2 state existed.
- Recorded the prediction before running mathematical experiments.
- Added shared short-Weierstrass arithmetic and $f_3,f_4,f_5$ evaluation,
  preserving the pre-existing generic-DLP API.
- [EMPIRICAL: unit test over F_17] Validated the pair-sum counter against direct ordered-triple enumeration on
  the known 19-point curve $y^2=x^3+2x+2$ over $\mathbb F_{17}$.
- Ran seed 12022026 at 16, 18, and 20 bits with 96 common targets per curve,
  three random bases per random category, and 2,000 hierarchical-bootstrap
  samples.

**Found:**

- [EMPIRICAL: one prime-order curve at each of p=65519,262139,1048571] The
  random-$\lfloor\sqrt p\rfloor$ normalized mean decomposition counts were
  1.0000, 0.9977, and 0.9976; every 95% interval contained 1 (script
  `code/measure_factor_bases.py`, summary CSV in `data/`).
- [EMPIRICAL: same three curves, 96 targets per candidate] Candidate A's
  normalized-count ratio to the size-matched random baseline was 1.030, 1.002,
  and 1.004; the respective 95% intervals were [0.963,1.118],
  [0.970,1.035], and [0.986,1.023].
- [EMPIRICAL: same three curves] Candidate A's pair-check ratio to the matched
  baseline was 0.938, 1.050, and 0.866; every 95% interval contained 1.
- [EMPIRICAL: 2,016 target/base rows] Every target had at least one
  three-term decomposition, and all 2,016 returned decompositions passed the
  group-law check; all 2,016 also passed $f_4$ because no sampled target or
  returned term was the identity.
- [EMPIRICAL: p=65519 through 1048571] A three-point descriptive fit of mean
  pair checks against $p$ gave slopes 0.529 (random square-root base), 0.437
  (size-matched random), and 0.408 (Candidate A); residuals are stored in the
  scaling CSV.

**Prediction vs. outcome:** [EMPIRICAL: preregistered three-size run] Matched.
The baseline was within the preregistered 15% band, Candidate A's density
effect was within the preregistered 20% band, and every descriptive slope was
within 0.2 of $1/2$.

**Did not work:** Two launches used an accidental one-second shell timeout and
were terminated during curve setup. They produced no result file; the unchanged
command completed in 18.7 seconds with a 120-second execution window. No
polynomial-system solver was tested: $f_4$ was a verifier, not the method that
found decompositions.

**Changed my mind about:**

- [EMPIRICAL: tested range only] Abundant decompositions and 100% observed
  success are weaker evidence than they initially appear: the measured search
  still took hundreds to thousands of pair checks and Candidate A did not
  separate from random density or search work.

**Next:** Implement SG-02 over a tiny cubic extension and recover a known
discrete logarithm end to end.

## Session 2 — 2026-06-25

**Goal:** Complete the remaining sub-goal ladder: first the cubic-extension
positive control, then Candidates B–D, and finally the SG-07 synthesis.

**Prediction (written before running session-2 experiments):**

- [HEURISTIC] Over a tiny $\mathbb F_{q^3}$, the subfield-$x$ factor base will
  have size on the order of $q$, and three-term decompositions will occur often
  enough to recover a planted discrete logarithm within 5,000 sampled
  relations. Failure to reach full rank or recovery of the wrong secret
  falsifies the end-to-end prediction.
- [HEURISTIC] With numerator and denominator bounds
  $|a|,|b|<\lfloor\sqrt p\rfloor$, Candidate B will cover a positive fraction
  of all $x\in\mathbb F_p$ and therefore produce a factor base far larger than
  the square-root diagnostic base. Coverage below 25% at all three recorded
  primes falsifies this session-level prediction.
- [HEURISTIC] The integral-point proxy for Candidate D with
  $|x|<\lfloor\sqrt p\rfloor$ will be too sparse for non-negligible
  three-term decomposition. A reachable-target fraction above 1% at any
  recorded prime falsifies this prediction.

**Did:**

- Added cubic polynomial-basis finite fields and elliptic-curve arithmetic over
  $\mathbb F_{q^3}$ with exhaustive inverse and Frobenius tests.
- Ran the SG-02 control at $q=5,7,11$, collected genuine three-term relations,
  and solved for planted target logarithms without using scalar labels during
  the solve.
- Enumerated the exact bounded-rational image for Candidate B and the exact
  integral-lift proxy for Candidate D on all three A001 curves.
- Derived the Candidate C obstruction from rational-map extension,
  inseparable factorization, Riemann–Hurwitz, and Bézout.

**Found:**

- [EMPIRICAL: q=5,7,11] The extension controls recovered secrets 37, 83, and
  123 in prime-order groups of orders 139, 347, and 1367. Each solve used nine
  relations and required 15, 34, and 149 sampled targets.
- [EMPIRICAL: p=65519,262139,1048571] Candidate B selected 99.9771%,
  99.9904%, and 99.9984% of the curve groups and therefore collapsed to an
  almost-full-group factor base.
- [EMPIRICAL: the same curves] Candidate D's integral-lift proxy had base sizes
  0, 0, and 2; the exact three-term success probabilities were 0, 0, and
  $3.82\times10^{-6}$.
- [EMPIRICAL: surviving 20-bit integral lift] The rational point above
  $x=-563$ has estimated canonical height 4.72408 with seven-step convergence
  delta $5.42\times10^{-5}$; its two signs are the only proxy points.
- [PROVED] Every rational map $\mathbb P^1\dashrightarrow E$ is constant, and
  a distinct degree-$d$ plane auxiliary curve supplies at most $3d$ points.
- [PROVED] None of the tested prime-field candidates supplies all three formal
  requirements; the successful SG-02 control is outside the prime-field regime.

**Prediction vs. outcome:** [EMPIRICAL: session-2 registered tests] Matched.
The extension relation systems reached full rank well before 5,000 attempts,
Candidate B coverage was far above 25%, and the Candidate D-proxy success rate
stayed far below 1%.

**Did not work:** The first standalone 2×2 linear-solver fixture used a matrix
whose determinant was zero modulo 5 and correctly raised an inconsistency. The
fixture was replaced with a nonsingular known-answer system; the end-to-end
extension control had already passed. The full canonical-height Candidate D
could not be measured because its lift/preimage membership predicate is not
specified; A005 measures a strict denominator-one proxy and Q002 records the
gap.

**Changed my mind about:**

- [EMPIRICAL: tested range] Symmetric numerator/denominator bounds at
  square-root scale are not a modest refinement of the integer interval: they
  are almost universal. Candidate B fails by being too dense, while the cheap
  lift proxy fails by being too sparse.

**Next:** For further work, test asymmetric rational bounds below product
$p$, and resolve Q001 or Q002 with an explicit algorithmic model rather than
additional density-only measurements.

## Correction to Session 2 — 2026-06-25

**Reason for correction:** The preceding “formal problem remains open”
assessment overlooked a direct cardinality incompatibility between conditions
(1) and (3). This was discovered after the candidate-by-candidate synthesis;
it was not a preregistered prediction.

**Did:**

- Quarantined the observation in `CLAIM.md` for adversarial checking before
  relying on it.
- Checked standard generalized L-notation against Lenstra 2017 and Hasse's
  bound against Sutherland's MIT 18.783 point-counting slides.
- Attacked exact versus variable length, ordering, repetitions, signs,
  randomized and nonuniform decoders, randomized factor bases, target
  dependence, and uniform-point oracle access.
- [EMPIRICAL: cyclic group of order 19] Exhaustively enumerated reachable sets
  for base sizes one through five and lengths zero through four; all 20
  base/length cases obeyed the support bound.

**Found:**

- [PROVED] A fixed-$m$ sum of a base of size
  $L_p[1/2,c]=p^{o(1)}$ reaches at most $p^{o(1)}$ targets.
- [PROVED] Hasse's bound makes the group size $p^{1+o(1)}$, so uniform-target
  success is at most $p^{-1+o(1)}$, below every inverse polynomial in
  $\log p$.
- [PROVED] Fixed $m$ requires a base of size at least
  $p^{1/m-o(1)}$ for inverse-polylogarithmic success; retaining an
  $L_p[1/2,c]$ base requires
  $m\ge(1/c+o(1))\sqrt{\log p/\log\log p}$.

**Changed my mind about:** [PROVED] The formal statement is not merely missing
a known structured predicate; under the standard notation it is
information-theoretically impossible. The square-root experiments address a
different, potentially intended problem.

**Next:** Stop for the statement as written. Resume only after explicitly
replacing the size bound or allowing $m$ to grow; P1.2/Q003 records the notation
ambiguity.

## Validation addendum — 2026-06-25

- [EMPIRICAL: local CPython 3.13.4] All 34 shared-library unit tests and all 10
  P1.2 unit tests passed after the formal-resolution changes.
- [EMPIRICAL: smoke configurations] The SG-01/Candidate-A driver, SG-02 cubic-
  extension control, and Candidates-B/D driver all completed successfully.
- [EMPIRICAL: cyclic group of order 19] The two new formal-support tests cover
  20 base-size/length cases and a collision case with support strictly below
  the ordered-tuple count.

## Session 3 — 2026-06-30

**Goal:** Continue beyond the resolved standard-L statement by auditing the
likely intended $p^{1/2+o(1)}$ variant, especially whether an unbounded
input-specific preprocessing table makes its online decomposition requirement
vacuous.

**Prediction (written before running the experiment):**

- [HEURISTIC] On the recorded 16-bit prime-order curve, a three-position radix
  construction will cover every group element with a factor base of size at
  most $3\lceil r^{1/3}\rceil$, and a full target-to-decomposition table will
  give constant-number dictionary operations online. Failure to cover one
  target or one invalid returned sum falsifies the construction prediction.
- [HEURISTIC] The factor base will be smaller than the recorded
  $\lfloor\sqrt p\rfloor$ baseline but the preprocessing table will have
  exactly $r$ target entries, demonstrating a linear-in-$p$ hidden resource.
  A base at least as large as the square-root baseline, or a sublinear table,
  falsifies the measured resource prediction.

**Plan:** Implement the construction separately from Candidate A, validate all
targets exhaustively at 16 bits, and state which construction-time,
description-size, preprocessing, and storage bounds a non-vacuous corrected
problem must add.

**Did:**

- Added `code/audit_preprocessing_loophole.py` and two unit tests covering
  exact integer roots and full radix-table decomposition on the order-19
  fixture.
- Exhaustively built and queried the table on all three recorded prime-order
  curves, not only the preregistered 16-bit curve.
- Proved the general cyclic-group radix construction and wrote two explicit
  resource-bounded alternatives in `CORRECTED_VARIANTS.md`.

**Found:**

- [EMPIRICAL: p=65519,262139,1048571] Base sizes were 120, 190, and 304,
  strictly below the square-root diagnostics 255, 511, and 1,023.
- [EMPIRICAL: all 1,373,865 targets] Coverage was 100%; no returned term was
  outside the base and no returned sum was invalid.
- [EMPIRICAL: same curves] Target-table sizes were exactly 65,537, 261,431,
  and 1,046,897, with four stored point references per target for $m=3$.
- [PROVED] For any cyclic order-$r$ group, the positional construction has
  size at most $m\lceil r^{1/m}\rceil$ and covers every target with exactly
  $m$ terms.
- [CONDITIONAL: unbounded input-specific description and preprocessing]
  Balanced lookup structures satisfy polylogarithmic online membership and
  decomposition time, but use $\Theta(rm\log p)$ bits and $\Omega(r)$
  preprocessing.

**Prediction vs. outcome:** [EMPIRICAL: preregistered 16-bit audit] Matched.
The base had 120 points, below 255; every one of 65,537 targets was valid; and
the decoder stored exactly 65,537 target entries. The extension to 18 and 20
bits showed the same exact behavior.

**Did not work:** The first launch called `Curve.is_on_curve`, while the shared
API names that method `Curve.contains`. Tests stopped before construction; the
call was corrected and all launches then passed. A later combined validation
passed the literal `*.py` string to `py_compile` because PowerShell did not
expand that wildcard; a file-by-file loop then compiled every P1.2 Python file
successfully.

**Changed my mind about:** [PROVED] A square-root substitution alone does not
produce a clean open problem. Without uniformity and offline-resource bounds,
nonuniform advice makes it trivial; with the bounds in Variant S, Candidate A
again becomes a genuine finder question.

**Next:** Treat the standard-L statement as resolved and the literal
online-only square-root version as specification-audited. Continue Q001 only
under an explicitly selected Variant-S resource model.

**Final validation:**

- [EMPIRICAL: local CPython 3.13.4] All 62 currently present shared-library
  tests and all 12 P1.2 tests passed.
- [EMPIRICAL: four smoke configurations] SG-01/Candidate A, the SG-02 cubic
  extension, Candidates B/D, and A008 all completed successfully.
- [EMPIRICAL: syntax audit] Every Python file directly under P1.2 `code/`
  passed `py_compile` in the corrected file-by-file invocation.

## Session 4 — 2026-07-07

**Goal:** Resolve Q001 for the explicit translate-probe model containing the
implemented lexicographic pair scan, while separating that result from
coordinate-aware algorithms for Candidate A.

**Prediction (written before the toy experiment):**

- [HEURISTIC] For every subset $\mathcal F$ of the order-19 test group and
  every list of $T$ shifts, the union of the translated sets
  $a_j+\mathcal F$ will contain at most $T|\mathcal F|$ targets. Exhaustive
  enumeration of all shift subsets for $1\le T\le4$ on the existing
  four-point base will falsify the implementation if any larger union appears.
- [HEURISTIC] Collisions will make the inequality strict for at least one
  nontrivial list, illustrating that the union bound is an upper bound rather
  than an assumed random-independence equality.

**Plan:** Prove the bound for fixed schedules, failure-adaptive schedules, and
randomized schedules; add an exhaustive toy regression; and record the exact
model boundary around target-coordinate access.

**Did:**

- Defined translate-probe schedules, including adaptation based on prior
  failures and randomized mixtures.
- Proved the translated-set union bound and specialized it to Candidate A.
- Added `code/audit_translate_probe.py`, a unit regression, and a four-row raw
  audit CSV covering every one-to-four-shift subset of the order-19 group.

**Found:**

- [PROVED] After $T$ translate probes, success is at most
  $T|\mathcal F|/r$ for fixed, failure-adaptive, and randomized schedules.
- [PROVED] Candidate A has at most $2\lfloor\sqrt p\rfloor$ points, so
  inverse-polylogarithmic success needs $T\ge p^{1/2-o(1)}$ in this model.
- [EMPIRICAL: 5,035 shift schedules in the order-19 group] No schedule
  exceeded the union bound. For $T=2,3,4$, respectively 95, 950, and 3,876
  schedules were strictly below it because of translate collisions.

**Prediction vs. outcome:** [EMPIRICAL: preregistered exhaustive toy audit]
Matched. There were zero violations, and strict inequality occurred for every
nontrivial probe count tested.

**Did not work:** Nothing mathematical failed. The experiment exercised a
strictly stronger shift universe than valid stored pair sums, so passing it
also covers the pair-sum-only schedules used by the model.

**Changed my mind about:** [PROVED] The measured $\sqrt p$ pair-scan behavior
now has a genuine restricted-model explanation, not merely a three-point
scaling fit. It remains invalid to extrapolate this lower bound to an algorithm
that exploits target coordinates.

**Next:** Q001 is closed for translate probes. Any continuation of Variant S
must address P1.2/Q004 and state how coordinate access is modeled without
allowing A008-style target-indexed advice.

**Final validation:**

- [EMPIRICAL: local CPython 3.13.4] All 63 currently present shared tests and
  all 13 P1.2 tests passed after A009.
- [EMPIRICAL: translate-probe smoke] The one- and two-shift audit completed
  with zero violations, and the full one-to-four-shift CSV was regenerated.
- [EMPIRICAL: syntax and tag audit] Every P1.2 code driver compiled, and no
  unresolved `[UNVERIFIED]` or compound epistemic tag remained in P1.2.

## Session 5 — 2026-07-13

**Goal:** Attack the coordinate-aware residual P1.2/Q004 using the concrete
smooth-subgroup factor base of Petit–Kosters–Messeng rather than another
target-oblivious pair schedule.

**Prediction (written before the experiment):**

- [HEURISTIC] Over a prime-order curve above $p=65537$, the multiplicative
  subgroup $H\subset\mathbb F_p^*$ of order $64=2^6$ will yield between 32 and
  96 curve points and its six-squaring membership chain will agree with
  $x^{64}=1$ on every field element. Any predicate mismatch or base size
  outside that range falsifies this prediction.
- [HEURISTIC] Three-term decomposition counts for this base will be within 25%
  of the exact random-base expectation $s^3/r$, and its generic pair-scan work
  will not improve by a factor of two over a size-matched random base. The
  respective bootstrap interval excluding $[0.75,1.25]$ or pair-work ratio
  interval lying wholly below $0.5$ falsifies the prediction.
- [HEURISTIC] The low-degree composition chain will make membership succinct
  but will not by itself produce a polylogarithmic decomposition finder. A
  validated coordinate solver whose operation count is polynomial in
  $\log p$ would falsify this assessment.

**Plan:** Find a deterministic prime-order toy curve over $\mathbb F_{65537}$,
validate the subgroup and chain exhaustively, compare 96 common targets against
three matched random bases with hierarchical bootstrap intervals, and keep
predicate structure separate from actual finder complexity.

**Additional Gröbner prediction (written after the density run but before any
Gröbner benchmark):**

- [HEURISTIC] Both the direct root constraint and repeated-squaring chain will
  complete on the tiny $p=17$, order-4 subgroup fixture, but moving to
  $p=257$, subgroup order 16 will either trigger a five-second timeout in at
  least one encoding or increase the returned basis size, maximum degree, or
  term count. If both encodings complete without any such growth, this
  prediction is falsified.
- [HEURISTIC] A completion at tiny scale is a correctness control, not an
  asymptotic complexity result. Only a proved polynomial bound in $\log p$ or
  stable completion over separated growing sizes would falsify the assessment
  that the coordinate solver remains missing.

**Did:**

- Read and summarized Petit–Kosters–Messeng (PKC 2016) and
  Amadori–Pintore–Sala (FFA 2018) in `refs/` and the root bibliography.
- Added `code/measure_smooth_subgroup.py`, exhaustively checked its subgroup
  and curve predicates, and compared it with matched random bases.
- Added `code/benchmark_smooth_groebner.py` with subprocess timeouts and
  separate direct and repeated-squaring encodings of the actual $f_4$ system.
- Added four unit tests and repaired the shared finite-field compatibility API
  without removing the newer tuple-based API used elsewhere.

**Found:**

- [PROVED] The order-64 subgroup predicate is exactly expressible by six
  quadratic squaring steps and is coordinate-aware, so A009 does not cover it.
- [EMPIRICAL: all field and curve elements at $p=65537$] The explicit
  subgroup, $x^{64}=1$, and chain predicates had zero mismatches; the curve
  factor base had size 60.
- [EMPIRICAL: 96 targets, three matched random controls] The normalized count
  ratio was 1.112 with 95% interval $[0.819,1.470]$; the pair-check ratio was
  0.969 with interval $[0.827,1.130]$.
- [EMPIRICAL: SymPy 1.14.0] Both encodings completed at $p=17$ and both timed
  out after five seconds at $p=257$ and $p=65537$. At the largest fixture the
  chain changed maximum input degree 64 to 12 and variable count 3 to 18.
- [CITED] Both audited papers leave the relevant prime-field polynomial-system
  complexity open; neither supplies the Variant-S decoder.

**Prediction vs. outcome:** [EMPIRICAL: preregistered experiment] Matched.
Every correctness and size control passed, neither bootstrap interval showed
the preregistered advantage, and the $p=257$ systems timed out.

**Did not work:** [EMPIRICAL: tested solver and timeout] Low-degree subgroup
membership did not translate into a completed Gröbner solve beyond the tiny
fixture. The timeout is recorded as solver status, not as nonexistence of a
decomposition or a general lower bound.

**Changed my mind about:** [PROVED] Coordinate structure exists in prime-field
factor bases outside translate-probe search. [EMPIRICAL: tested range] Making
that structure low-degree can trade degree for auxiliary variables without
making the decomposition finder efficient.

**Next:** None for literal P1.2. If the human selects Variant S, attack Q004
through a coordinate-aware complexity model or a solver with a proved total
resource bound; do not repeat generic pair scanning.

**Final validation:**

- [EMPIRICAL: local CPython 3.13.4] All 69 shared-library tests and all 17
  P1.2 tests passed.
- [EMPIRICAL: seven smoke drivers] Every documented P1.2 smoke command
  completed, including both smooth-subgroup Gröbner encodings.
- [EMPIRICAL: syntax audit] Every Python file directly under P1.2 `code/`
  passed `py_compile`.
