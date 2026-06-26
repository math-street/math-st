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
