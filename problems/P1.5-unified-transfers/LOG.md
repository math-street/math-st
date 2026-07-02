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
