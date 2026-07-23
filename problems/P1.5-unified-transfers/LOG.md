# Log

## Session 1 - 2026-06-26

**Goal:** Complete SG-01 through SG-07 at toy scale: reproduce both known
transfers, isolate their shared structure, and prove the strongest restricted
classification supported by the checked literature and direct arguments.

**Prediction (written before running anything):** The anomalous reduction will
be reproducible with arithmetic modulo $p^2$ and the formal parameter
$-x/y$, while a supersingular $j=1728$ curve will give a deterministic
embedding-degree-two Tate-pairing example. The requested broad classification
will remain open, but algebraic-group homomorphisms from an elliptic curve
should admit a short restricted classification by properness and dimension.

**Positive result criterion:** Both scripts recover fixed known logarithms,
independent group calculations verify the answers, smoke mode finishes in under
10 seconds, and every candidate family receives either a proved/cited exclusion
or a precisely logged gap.

**Negative result criterion:** A reduction fails a known-answer or bilinearity
test, a supposedly injective map collides on the tested subgroup, or a candidate
cannot be excluded without an unsupported structural assertion.

**Did:**

- Defined a uniform transfer package with target complexity measured in
  $n=\lceil\log_2 r\rceil$, full input length $L=n^{O(1)}$, and explicit
  treatment of qualifying Weil descent.
- Exposed the Smart formal-group character in `lib/anomalous.py`, added exact
  anomalous search and a $j=1728$ CM embedding-degree-two constructor in
  `lib/curves.py`, and used the staged pairing implementation in `lib/pairing.py`.
- Added known-answer and homomorphism tests, a smoke path, seven-size timing
  matrices, power-law fits, and per-point residuals.
- Checked primary sources for the two elementary attacks, Weil descent,
  high-genus target algorithms, Drinfeld-module structure, and algebraic-group
  structure.
- Reconciled concurrent shared-library work instead of overwriting it; the
  final baseline contains extension-field, pairing, height, and binary-field
  changes from the overlapping session.

**Found:**

- [EMPIRICAL: seven anomalous curves, 101 <= p <= 6421] Exact point counts and
  source-group checks passed, all homomorphism samples passed, and every fixed
  logarithm was recovered.
- [EMPIRICAL: seven k=2 subgroups, 43 <= p <= 8011 and 11 <= r <= 2003] Exact
  group orders, embedding degrees, bilinearity samples, target orders, and all
  recovered logarithms passed.
- [EMPIRICAL: Windows 11, Python 3.13.4, 50 timing repeats] The additive and
  affine-Tate map times fit exponents 1.050508 and 1.052569 against their
  explicit work predictors; all log-residuals are in the scaling CSV.
- [CITED] Belding (2007) supplies a pairing on characteristic-$p$ torsion over
  dual numbers and explicitly relates the Semaev--Ruck and MOV viewpoints.
- [PROVED] Every algebraic-group homomorphism from an elliptic curve to an
  affine algebraic group is trivial; every nontrivial algebraic-group image is
  an elliptic abelian subvariety and the source map is an isogeny.
- [CITED] Under the adopted definition, qualifying Weil-descent instances are
  a known third geometric transfer family, not a newly discovered mechanism.
- [EMPIRICAL: final local verification on 2026-06-26] All 53 shared-library
  tests and both P1.5 driver tests passed, bytecode compilation succeeded, and
  the smoke experiment completed in 1.4 seconds.

**Prediction vs. outcome:** Matched on both implementations and on the
restricted algebraic-group classification. The literature supplied a stronger
common pairing framework than the initial formal-log-versus-pairing contrast,
and the broad definition made the Weil-descent decision explicit rather than
terminological.

**Did not work:** The first full run used 200 timing repeats and hit the
30-second command ceiling before writing data. Repeating at 50 completed in
about 21 seconds. Initial microsecond additive timings were noisy, so the
driver now uses at least 5,000 calls for that map; the final residual range is
stored rather than hidden.

**Changed my mind about:** The additive and multiplicative cases are not merely
analogous at the level of "linearization." Belding's dual-number construction
makes a pairing-based umbrella precise, while Weil descent remains a separate
geometric route under the operational definition.

**Next:** Work A001 on the smallest ordinary CM curves: enumerate natural
point-to-ideal assignments, reject those that fail the homomorphism identity on
the full toy subgroup, and record the first structural obstruction.

## Session 2 - 2026-07-02

**Goal:** Resolve the natural CM/class-group branch of A001 as far as possible:
test annihilator ideals and kernel-isogeny classes, prove the endomorphism-order
size obstruction for cryptographic-size prime subgroups, and determine whether
ray class groups preserve enough point orientation to survive.

**Prediction (written before new experiments):** Annihilator ideals and
isogenies defined by $\langle P\rangle$ will be constant on every nonzero
multiple of $P$ and therefore cannot be injective for $r>2$. The class group of
the curve's own CM order should also be too small to contain an order-$r$
element when $r=\Theta(q)$. Ray class groups modulo $r$ will be prime-to-$r$
when $r$ is unramified; modulus $r^2$ may contain additive principal units but
will leave the evaluator problem rather than produce a natural point map.

**Positive result criterion:** A candidate produces $r$ distinct target values,
passes the homomorphism identity on a complete toy subgroup, and has a checked
subexponential target algorithm.

**Negative result criterion:** A proof shows the candidate factors through the
unoriented subgroup $\langle P\rangle$, the target order is not divisible by
$r$, or exhaustive evaluation finds a collision or homomorphism failure.

**Did:**

- Added `code/probe_cm_class_targets.py` and five regression tests for
  ordinary $j=1728$ CM eigenlines, annihilators, cyclic kernels, canonical
  Velu quotients, ray class orders, principal units, level-lift fibres, and the
  explicit class-number threshold.
- Split A001 into three dead natural branches: A003 for annihilator/kernel
  labels, A004 for ray principal units and oriented levels, and A005/A006 for
  local and global arithmetic class-pairing specializations.
- Checked primary or authoritative sources for the CM ideal action, ray class
  exact sequence, ring and analytic class-number formulas, arithmetic class
  pairings, and explicit number-field torsion bounds.

**Found:**

- [PROVED] For every nonzero $n\bmod r$,
  $\operatorname{Ann}_R(nP)=\operatorname{Ann}_R(P)$ and
  $\langle nP\rangle=\langle P\rangle$; annihilator, kernel, and quotient
  labels therefore cannot be injective homomorphisms.
- [EMPIRICAL: 8 ordinary j=1728 curves, 13 <= p <= 421, 5 <= r <= 113]
  Exhausting all 368 nonzero points produced exactly one CM eigenvalue,
  annihilator label, cyclic kernel, and canonical Velu quotient per subgroup;
  see `data/probe_cm_class_targets_full_20260702.csv`.
- [PROVED] The ring and analytic class-number formulas plus the elementary
  bound $|L(1,\chi)|\le\log|d|+2$ give
  $h(\operatorname{End}(E))\le(6/\pi)\sqrt q(\log(4q)+2)^2$.
- [PROVED] For $q\ge2^{21}$ and $r\ge q/2$, the last bound is below $r$, so
  the curve's own endomorphism class group cannot contain the source image.
- [PROVED] For $\mathbb Q(i)$, the ray class group modulo $r$ is prime to
  $r$; modulo $r^2$ its principal units linearize, but they move the $r$ level
  lifts above one source point rather than the $r$ source points.
- [CITED] Buell--Call (2016) give genuine point-to-class homomorphisms over
  number fields and relate them to Weil descent; direct finite/local
  specialization has trivial Picard target.
- [CITED] Parent's 1999 bound forces degree
  $d>(r/12480)^{1/7}$ for a number field carrying a rational order-$r$ point,
  which makes standard dense global lifts exponential in $\log r$.
- [EMPIRICAL: final local verification on 2026-07-02] All 63 shared tests and
  7 P1.5 tests passed, bytecode compilation succeeded, both smoke scripts
  completed together in 1.303 seconds, the full CM CSV has 8 rows, and no
  unresolved verification marker remains in P1.5.

**Prediction vs. outcome:** Matched. The annihilator and kernel constructions
were constant, the ordinary class group was too small in the large-prime
regime, and modulus $r^2$ exposed easy principal units without a source
evaluator. The stronger outcome is that standard level structure explains the
failure geometrically, and Parent's theorem closes standard global lifts.

**Did not work:** Annihilator ideals, cyclic-kernel quotients, modulus-$r$ ray
classes, modulus-$r^2$ level rescaling, finite/local arithmetic class pairings,
and standard dense global torsion lifts each fail for a different explicit
reason recorded in A003--A006.

**Changed my mind about:** Point-to-class-group homomorphisms do exist in
arithmetic geometry, so their mere existence is not the right obstruction.
The decisive finite-field questions are whether a nontrivial global class
target survives specialization, whether the lift fits the full input budget,
and whether its action follows point addition rather than level rescaling.

**Next:** Work SG-14: either find a finite-field point-to-class formula outside
the four excluded natural branches, or state a restricted oracle model for CM,
ideal, ray, and coordinate operations in which a lower bound is provable.

## Session 3 - 2026-07-06

**Goal:** Complete SG-14 by defining a generic-source transfer model, proving
that no package with a subexponential target DLP can exist in that model, and
locating exactly which representation-specific operations let anomalous,
pairing, and Weil-descent transfers escape.

**Prediction (written before the literature check):** Composing an injective
homomorphic evaluator with its subexponential target DLP algorithm will solve
the generic source DLP using $r^{o(1)}$ source-oracle queries, contradicting
the $\Omega(\sqrt r)$ generic lower bound. The result will classify every
generic-source candidate at once but will not rule out coordinate-sensitive
maps.

**Positive result criterion:** State the source encoding, setup, randomness,
success probability, and query accounting precisely enough that the composed
DLP algorithm falls under a checked published lower bound, then give an
explicit escape clause for every known transfer.

**Negative result criterion:** The published lower bound does not allow the
evaluator's auxiliary computation or preprocessing, or the transfer
definition permits a cross-representation oracle not captured by the model;
in that case narrow the theorem rather than claiming a generic impossibility.

**Did:**

- Defined a classical generic-source transfer model with random injective
  encodings, counted setup/evaluator source queries, explicit success, and no
  encoding-dependent cross-representation advice.
- Split the coordinate-sensitive residual into A008--A013: low-degree affine
  maps, shallow rational circuits, finitely branched affine maps, proper
  targets, piecewise proper targets, and mixed algebraic targets.
- Checked Shoup's primary paper metadata, Miller's republished
  straight-line-program account, the Stacks proper-target extension lemma, and
  Milne's rigidity result for zero-preserving maps of abelian varieties.

**Found:**

- [CITED] Shoup's 1997 random-encoding lower bound makes a prime-order generic
  DLP algorithm with $m$ source queries succeed with probability only
  $O(m^2/r)$.
- [PROVED] Composing a generic-source evaluator with its target DLP and
  truncating expected queries gives $m=r^{o(1)}$ with fixed success, a
  contradiction.  Every qualifying transfer must use a
  representation-specific source operation.
- [PROVED] If a rational map into an affine algebraic group is homomorphic on
  the order-$r$ subgroup and its common pole degree is $D<r/2$, its
  homomorphism defect vanishes globally and the map is trivial.
- [PROVED] A branch-free rational circuit therefore has depth
  $d\ge\log_2r-\log_2(2MD_0)$, and a $B$-branch piecewise-rational evaluator
  satisfies $\max(1,D)B^3\ge r/4$.
- [CITED] Miller's 1986/2024 account explains the matching escape: a
  $\Theta(\log r)$ straight-line program compactly represents a rational
  pairing function whose expanded degree is $\Theta(r)$.
- [PROVED] A rational evaluator into a smooth proper algebraic group extends
  globally.  Even with fewer than $r$ rational branches, two source points in
  one branch force the entire subgroup map to be the restriction of one
  global homomorphism, with trivial or elliptic-isogenous image.
- [PROVED] Chevalley decomposition reduces a single rational mixed-target map
  to its global abelian quotient and an affine-kernel homomorphism defect.  If
  the defect pole degree is below $r$ in the controlled fibres, the whole map
  is global and again has trivial or elliptic-isogenous image.
- [EMPIRICAL: final local verification on 2026-07-06] All 69 shared tests and
  7 P1.5 tests passed, bytecode compilation succeeded, both smoke experiments
  recovered every fixed logarithm, the trailing-whitespace audit passed, and
  P1.5 contains zero unresolved verification markers.

**Prediction vs. outcome:** Matched and strengthened.  The generic
composition did contradict Shoup exactly after query truncation.  The
representation-specific escape audit then yielded quantitative rational
degree, branch, and depth bounds plus a complete proper-target reduction.

**Did not work:** Generic class/ideal arithmetic, affine rational degree below
$r/2$, sublinear-depth rational circuits, polynomially many low-degree affine
branches, and fewer than $r$ proper rational branches all fail for explicit
reasons in A007--A013.

**Changed my mind about:** Coordinate access is necessary but not sufficient
for a new affine transfer.  The decisive resource is enough geometric degree,
branch complexity, or non-rational structure to cross an essentially
linear-in-$\log r$ boundary.  Proper targets are even more rigid: polynomially
many rational pieces collapse to one global elliptic-isogenous map.

**Next:** Continue A001 only in the genuine residual class: specify one
high-degree or non-rational coordinate/lift/valuation interface for a succinct
point-to-class evaluator, then either construct the homomorphism or prove a
lower bound for that exact interface.

## Session 4 - 2026-07-10

**Goal:** Push Q004 beyond the generic/rational lower bounds by classifying
class-group targets according to their base - finite/local rings, global
function fields, and number fields - and reduce the last succinct
cross-characteristic evaluator to an exact computational problem.

**Prediction (written before the literature search):** Finite and local bases
will have trivial Picard targets; global function-field class groups will be
Jacobians and hence fall under the proper-target classification; standard
number-field lifts will remain excluded by A006.  The only survivor will be a
direct bit/coordinate-to-ideal algorithm for a separately constructed number
field order.  Its evaluation complexity will be sandwiched between source
ECDLP and target class-group DLP, so an unconditional exclusion will require a
new concrete-coordinate lower bound rather than more CM size arguments.

**Positive result criterion:** Exhibit one uniform family of orders, known
order-$r$ ideal classes, and a polynomial-time coordinate evaluator that passes
the homomorphism law and nonzero-image test, with all setup and target DLP costs
inside SG-01.

**Negative result criterion:** Prove that an entire base category reduces to a
previously classified target, or state a two-way reduction showing exactly
which unresolved evaluator problem remains and why the existing lower bounds
do not cover it.

**Did:**

- Split A001 into A014--A022, covering class-target bases, evaluator
  reductions, discriminant budgets, the Buell residue-coordinate formula,
  checked literature, prescribed-order targets, and the ray evaluator.
- Added `code/probe_buell_reduction.py` with three tests and two CSVs, and
  `code/probe_exact_order_targets.py` with three tests and two CSVs.
- Checked primary or authoritative sources for Picard groups of finite rings,
  function-field class groups, Buell--Soleng point-to-class constructions,
  modern class-pairing specializations, and prescribed-order imaginary
  quadratic class groups.
- Updated P1.5/Q004 with an explicit positive and negative closure criterion.

**Found:**

- [PROVED] Finite and local bases have trivial Picard groups, while a pointed
  global function-field class group is a Jacobian rational-point group; a
  genuinely distinct class target must be a global number-field order.
- [PROVED] Evaluation and source DLP are polynomial-time equivalent given a
  target-DLP oracle.  A polynomial evaluator plus an $\exp(o(\log r))$ target
  algorithm is exactly a subexponential source-DLP reduction, not a
  contradiction to a known unrestricted lower bound.
- [PROVED] For discriminant bit length $B$ and
  $n=\lceil\log_2r\rceil$, the checked Hafner--McCurley route requires
  $2n-O(\log n)\le B=o(n^2/\log n)$.
- [CITED] All checked Buell, Soleng, Buell--Call, Gillibert, and
  Blum--Choi--Hoey--Iskander--Lakein--Martinez point-to-class maps use
  characteristic-zero rational or algebraic points.
- [EMPIRICAL: bounded primary-source search on 2026-07-10] No checked source
  supplied a direct $E(\mathbb F_q)[r]$-to-fixed-number-field-class
  homomorphism; this is a bounded search result, not a nonexistence theorem.
- [PROVED] Canonical integer representatives in the Buell formula produce
  discriminant $\mathcal D+k_Qp$, so different source points generally land
  in different quadratic orders rather than one class group.
- [EMPIRICAL: 10 nonsingular reductions, $23\le p\le59$, $13\le r\le37$,
  218 nonzero points] All 218 lifted discriminants were distinct, only two
  equalled the model discriminant, every discrepancy was divisible by $p$,
  195 were negative, and 199 form triples were primitive.
- [PROVED] For every prime $r\ge3$, the ideal
  $(2,(1+\sqrt{1-4\cdot2^r})/2)$ has exact class order $r$, but its
  discriminant has $\Theta(r)$ bits and violates SG-01.
- [EMPIRICAL: every negative order discriminant with
  $|\Delta|\le200000$, 13 primes $3\le r\le43$] Each least discriminant with
  $r\mid h(\Delta)$ had $h(\Delta)=r$ and
  $0.684711\le|\Delta|/r^2\le2.555556$; each recorded nonprincipal reduced
  form therefore has exact order $r$.
- [PROVED] The last census is nonuniform: exhaustive class-number search does
  not give a polynomial-time growing-family target constructor.
- [EMPIRICAL: bounded prescribed-order primary-source search on 2026-07-10]
  Checked exact-order theorems use $n$-th-power discriminant families or
  fixed-$n$ ineffective thresholds; no checked theorem supplied the uniform
  polynomial-bit constructor required by SG-01.
- [PROVED] Any nonzero evaluator into the modulus-$r^2$ Gaussian
  principal-unit target immediately reveals the source scalar through
  $1+rz\mapsto z\bmod r$.  Ray evaluation and source DLP are polynomial-time
  equivalent, so this easy target has no intermediate subexponential regime.
- [EMPIRICAL: final local verification on 2026-07-10] Python 3.13.4 was
  available while SageMath, PARI/GP, Singular, and msolve were unavailable;
  all 70 shared and 13 P1.5 tests passed, bytecode compilation succeeded, all
  four smoke scripts completed, the full exact-target census took 2.72
  seconds, the trailing-whitespace audit passed, and P1.5 contains zero
  unresolved verification markers.

**Prediction vs. outcome:** Matched and strengthened.  The target-base
taxonomy and evaluator sandwich left the predicted cross-characteristic
ordinary-class evaluator.  The stronger outcome separates two additional
issues: explicit prescribed-order targets can be either provably oversized or
small but nonuniform, and the ray principal-unit fallback is already
polynomially equivalent to source DLP.

**Did not work:** The direct Buell residue-coordinate formula failed because
its discriminant varied by multiples of $p$.  The self-certifying exact-order
target had exponential input length.  The small-target census found excellent
toy instances but only by exhaustive search.  Bounded literature searches
found no direct finite-field evaluator or uniform succinct prescribed-order
constructor.  Two initially selected Buell fixtures were singular and were
replaced by nonsingular cases; the new census test initially lacked the
repository import path and was repaired before the final run.

**Changed my mind about:** The ordinary target and the evaluator must be
treated as separate construction problems.  Small exact-order class targets
exist throughout the toy range, but this does not make them uniform; conversely
the uniform ray target is too transparent to provide a merely subexponential
reduction.  The main residual is now specifically an ordinary number-field
class target with a nontransparent target DLP and a direct
cross-characteristic evaluator.

**Next:** Work SG-32 first.  Fix one concrete ordinary-class output encoding
and one allowed coordinate/lift/valuation instruction set, then either build a
nonzero evaluator inside the SG-25 target window or prove a lower bound for
that exact program model.  SG-30 remains the separate prescribed-order target
construction task.

## Session 5 - 2026-07-15

**Goal:** Reconstruct and adversarially audit A008--A013, decide whether they
form a correct nontrivial restricted classification, and replace the scattered
claims by one externally reviewable theorem package.

**Prediction:** The one-branch affine and proper arguments would survive after
base-change and specialization cleanup, while the computational corollary
would need a narrower explicit model.  The \(B^3\) branch exponent looked like
a coloring artifact and might improve.

**Positive result criterion:** Every zero count has an intrinsic pole bound,
every proper/mixed argument handles components and descent, adversarial branch
sets are covered, and the circuit statement names a model that actually
implies a degree bound.

**Negative result criterion:** A constant/translation/disconnected-target,
vertical-denominator, characteristic, or branch-partition counterexample
survives the stated hypotheses; in that case replace the claim rather than
strengthening it silently.

**Did:**

- Read all P1.5 core files, A007--A016, A018, relevant references, every P1.5
  code file, and every P1.5 test.
- Reproved the affine theorem using one generator and translation invariance
  of the least common pole divisor, avoiding an unnecessary second
  specialization.
- Replaced the triple-color branch proof by a largest-branch
  ordered-difference argument.
- Restated proper rigidity over a perfect base, with explicit handling of
  disconnected and noncommutative targets.
- Restated the Chevalley defect theorem with the exact specialized and generic
  fibre pole bounds used by the proof and explicit descent.
- Defined a rational decision-tree evaluator and separated algebraic depth
  from general polynomial-time bit complexity.
- Performed a focused primary-literature search around interpolation and zero
  estimates on algebraic groups, proper-map rigidity, Chevalley decomposition,
  and algebraic computation trees.
- Wrote RATIONAL_TRANSFER_REVIEW.md and added an exhaustive finite
  combinatorial falsification certificate.

**Found:**

- [PROVED] A rational affine subgroup homomorphism of common pole degree
  \(D<r/2\) is the identity.  The proof works in every characteristic, but the
  degree is relative to a fixed faithful representation over \(\bar k\).
- [PROVED] For \(B\) arbitrary nonempty affine branches,
  \[
  \left\lceil\frac rB\right\rceil
  \left(\left\lceil\frac rB\right\rceil-1\right)\le2D(r-1).
  \]
  Hence \(\max(1,D)B^2\ge r/4\).  The previous \(B^3\) proof is correct but
  strictly weaker.
- [PROVED] In the rational decision-tree model the circuit corollary is
  \(d+2b\ge\log_2r-\log_2(4MD_0)\).  This is not a lower bound against
  arbitrary polynomial-time evaluators, and linear depth remains polynomial.
- [PROVED] A pointed rational map from \(E\) to a smooth proper algebraic group
  is global.  With fewer than \(r\) rational branches, any subgroup
  homomorphism equals one global homomorphism on \(C\), including for
  disconnected/noncommutative targets.
- [PROVED] The mixed Chevalley/cocycle theorem is valid under explicit
  fibrewise pole assumptions.  A generic displayed bidegree alone is
  insufficient to control vertical specialization.
- [PROVED] No exceptional-characteristic or purely inseparable counterexample
  occurs.  Genuine out-of-scope counterexamples arise from non-faithful
  representations, maps defined only on \(C\), \(r\) singleton proper
  branches, or programs with no controlled rational realization.
- [EMPIRICAL: bounded primary-source search, 2026-07-15] The closest checked
  prior art is Masser/Fischler/Fischler--Nakamaye interpolation on commutative
  algebraic groups, Gomez-Perez--Shparlinski on rational-function values in
  finite-field subgroups, Miller on short curve-function programs, and Ben-Or
  on algebraic computation trees.  No checked source states the same
  prime-subgroup defect, \(B^2\) branch, or proper-branch collapse theorem.
  This is not a certified novelty claim.
- [EMPIRICAL: final verification on 2026-07-15] All 70 shared and 16 P1.5
  tests passed, bytecode compilation succeeded, all four existing smoke
  drivers and the new certificate completed, and the edited-file trailing
  whitespace audit passed.

**Prediction vs. outcome:** The core affine/proper/mixed arguments survived
with explicit hypotheses.  The branch exponent improved from \(3\) to \(2\),
and the main correction was interpretive: polynomial time is not itself tied
to low geometric degree or sublinear algebraic depth.

**Classification status:** P1.5 now contains a repository-original synthesis
of restricted classification statements. The proper-target part is largely
standard rigidity, and the quantitative affine mechanism requires the A023
prior-art reconciliation. The package is neither an unrestricted solution nor
a certified literature novelty claim.

**Next:** Return to SG-32's non-rational coordinate/lift/valuation evaluator
model.  Do not apply the rational circuit theorem to that residual without an
explicit reduction to the audited decision-tree model.

## Session 6 - 2026-07-20

**Goal:** Reconcile the rational-transfer package with the missed
cryptographic interpolation and efficiently computable-homomorphism
literature before doing any further construction work, then resume SG-32 in
one exact non-rational evaluator model while leaving SG-30 separate.

**Prediction:** Coppersmith--Shparlinski would recover the quadratic
arbitrary-subset overlap scale but not the elliptic-source/arbitrary-target
theorems. Character-sum refinements would need structure absent from an
adversarial branch partition. A Verheul-style consequence would require
pairing structure unavailable in an ordinary reduced-form target, so SG-32
would need a model-internal lower bound.

**Positive result criterion:** A023 gives one proof-or-citation verdict for
all five synthesis items and directly answers both the \(B^2\) and
character-sum questions. Only after that audit, SG-32 fixes one canonical
ordinary output and finite lift/valuation instruction set and proves either a
nonzero evaluator or a lower bound in exactly that model.

**Negative result criterion:** A checked interpolation theorem derives the
full P1.5 statement or improves the worst-case exponent, requiring the
repository claims to be withdrawn; or the SG-32 interface cannot support a
sound nontrivial theorem without implicitly solving SG-30.

**Did:**

- Added seven P1.5 reference records and matching bibliography/BibTeX entries
  for Coppersmith--Shparlinski, Lange--Winterhof, Kiltz--Winterhof,
  Winterhof/Meidl--Winterhof, Verheul, Moody, and Koblitz--Menezes.
- Corrected the requested Meidl--Winterhof attribution: the discrete-logarithm
  interpolation paper is sole-authored by Winterhof, while the actual
  Meidl--Winterhof paper concerns a polynomial Diffie--Hellman
  representation.
- Wrote A023, reconciled Section 10, replaced novelty-adjacent wording by
  repository-original synthesis, and recorded the SG-14 and SG-23 conceptual
  overlaps.
- After A023 was complete, fixed A024's canonical reduced-form output and VFB
  instruction set, including exact coordinate lifts, integer arithmetic,
  valuations, comparisons, and fixed-factor-base target operations.
- Checked the Verheul/Moody pairing-and-distortion template before proving a
  model-internal transcript lower bound. SG-30 was not started.

**Found:**

- [CITED] Coppersmith--Shparlinski Theorem 1 proves
  \[
  d\ge |S|(|S|-1)/(2(p-2))
  \]
  for a polynomial computing discrete logarithms on an arbitrary subset.
  This is direct prior art for the quadratic-overlap mechanism and recovers
  \(D_+B^2=\Omega(r)\) in its scalar finite-field specialization.
- [PROVED] The checked interpolation papers do not state the elliptic-source,
  arbitrary faithfully represented affine-target result, nor the proper or
  mixed-target theorems. All five requested comparison verdicts are therefore
  (b), with the scalar scale and proof patterns explicitly credited.
- [PROVED] The checked character-sum improvements require dense, random, or
  otherwise structured sample sets. For an arbitrary branch the universal
  identity remains
  \(\sum_{t\ne0}|S\cap(S-t)|=|S|(|S|-1)\), so no improvement from \(B^2\)
  toward \(B\) follows.
- [PROVED] A024's VFB theorem states that a nonzero evaluator with \(C\)
  comparisons and valuation-operand bit bounds \(h_j\) must satisfy
  \[
  C+\sum_j\log_2(h_j+1)\ge\log_2r.
  \]
  Thus polynomial-height operands and \(C=o(\log r)\) require
  \(\Omega(\log r/\log\log r)\) valuation observations.
- [PROVED] Verheul/Moody would give a conditional Diffie--Hellman consequence
  if the ordinary target supplied an efficient pairing, distortion map, and
  tractable paired-target logarithm. No checked reduced-form construction has
  that package, so the template is not an unconditional lower bound here.
- [PROVED] A024 completes SG-32 only at the requested one-model scope. Its
  bound is compatible with polynomial time and excludes neither
  polynomial-length VFB programs nor direct raw-coordinate form synthesis.
  P1.5/Q004 remains open.
- [EMPIRICAL: final verification on 2026-07-20] All 70 shared and 16 P1.5
  tests passed, bytecode compilation succeeded, and the edited-file control
  character, unresolved-marker, and trailing-whitespace audits passed.

**Prediction vs. outcome:** Matched. The closest literature materially
narrows the novelty wording without deriving the repository's full theorem
statements. The Verheul/Moody template clarified the missing target structure,
and the exact VFB boundary supported a clean information-transcript lower
bound without entering SG-30.

**Next:** Keep SG-30 separate and untouched. If evaluator work continues,
formalize the direct raw-coordinate MAKEFORM-style extension excluded by VFB;
its fixed-discriminant and homomorphism invariants, rather than generic or
bounded-degree rational arguments, are the next unresolved issue.

## Session 7 - 2026-07-23

**Goal:** Finish Q004 under its recorded positive or negative closure criterion,
without conflating it with the stronger target-only SG-30 problem or claiming
that a repackaging of a known transfer is a new mechanism.

**Prediction:** The missing MAKEFORM invariant might be supplied by a standard
exact sequence rather than by a new point-to-class pairing. In the
embedding-degree-two Gaussian setting, the conductor quotient for
\(\mathbb Z+p\mathbb Z[i]\) should turn projective finite-field residues into
ordinary ring classes; the decisive tests are injectivity on \(\mu_r\), a
fixed-discriminant canonical form, and an explicit target-logarithm route.

**Positive result criterion:** Give an infinite family of polynomial-length
instances, one fixed ordinary class group per instance, a uniform evaluator
from ordinary point encodings, complete homomorphism and injectivity proofs,
and an \(\exp(o(\log r))\) target DLP including instance precomputation.

**Negative result criterion:** If the conductor quotient kills the order-
\(r\) pairing image, the form coefficients cannot be canonicalized in
polynomial time, or target forms cannot be converted to a qualifying DLP, close
the exact model negatively and leave Q004 open outside it.

**Did:**

- Defined \(\mathcal O_p=\mathbb Z+p\mathbb Z[i]\) for
  \(p\equiv3\pmod4\) and specialized Conrad's conductor exact sequence.
- Composed its quotient map with the nondegenerate degree-two pairing on
  \(E_p:y^2=x^3+x\), using \(\psi(x,y)=(-x,iy)\).
- Derived the direct fixed-discriminant output
  \((1+t^2,2pt,p^2)\), followed by ordinary positive-form reduction.
- Proved a Gaussian-gcd conversion from reduced target forms back to the same
  finite-field torus and preserved logs by exponent \(-4\bmod r\).
- Used CRT plus Linnik--Xylouris to obtain an infinite family with
  \(\log p=O(\log r)\), keeping SG-30 untouched.
- Added A025, its implementation and four regression tests; synchronized
  NOTES, STATE, HANDOFF, SUBGOALS, OPEN_QUESTIONS, PROBLEM, A001, the rational
  review postscript, references, bibliography, paper source, taxonomy figure,
  and the regenerated PDF.

**Found:**

- [PROVED] The exact sequence gives
  \[
  \operatorname{Pic}(\mathcal O_p)\cong
  \mathbb F_{p^2}^{\times}/
  (\mathbb F_p^{\times}\langle i\rangle),
  \qquad h(-4p^2)=(p+1)/2.
  \]
- [PROVED] Its kernel has order \(2(p-1)\), so it meets the odd order-
  \(r\) pairing image trivially when \(r\mid p+1\).
- [PROVED] For a projective pairing residue \(1+ti\), contraction is
  \([1+t^2,-pt+pi]\), represented by the primitive form
  \((1+t^2,2pt,p^2)\) of discriminant \(-4p^2\).
- [PROVED] Extending a reduced ideal to \(\mathbb Z[i]\), taking a Gaussian
  gcd \(\gamma\), and returning
  \((\gamma\bmod p)^{2(p-1)}\) is well defined and acts by
  \(-4\bmod r\) on the transfer image.
- [PROVED] The target DLP therefore reduces to the same degree-two finite-field
  DLP accepted for MOV/Frey--Ruck; independently, the stated conditional
  Hafner--McCurley route also fits the SG-25 window because
  \(\log|\Delta|=\Theta(\log r)\).
- [PROVED] Q004 is closed positively, but A025 is not a structurally new
  transfer: it factors through the known pairing and efficiently returns to
  that same torus. A004's ray-principal-unit negative result remains intact.
- [EMPIRICAL: complete \(p=43,211,331\) class groups] The A025 driver enumerated
  22, 106, and 166 reduced classes, obtained injective images of sizes 11, 53,
  and 83, and recovered every seeded logarithm.
- [EMPIRICAL: final verification on 2026-07-23] All 70 shared and 20 P1.5 tests
  passed, bytecode compilation succeeded, and the source control-character,
  unresolved-marker, trailing-whitespace, and bibliography-brace audits passed.
  Typst 0.14.2 rebuilt a 17-page PDF; raster inspection found no clipping,
  overlap, broken table, or unreadable formula on the updated pages.

**Prediction vs. outcome:** Matched, with a stronger positive outcome than the
VFB lower-bound path suggested. The conductor exact sequence supplies the
previously missing homomorphism invariant and canonical MAKEFORM instruction,
but it does so only after the known pairing has exposed the projective residue.

**Next:** Treat Q004 as closed. Keep SG-30 separate and unchecked; it asks for
a prescribed-order ordinary target from arbitrary \(r\), which A025 neither
needs nor supplies. Any future unrestricted-classification work must also keep
the pairing-derived A025 family distinct from a genuinely new mechanism.
