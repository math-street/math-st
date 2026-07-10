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
