# Sub-goals

- [x] **SG-01a:** Validate short-Weierstrass arithmetic, exact point counting,
  prime-order curve search, and $f_3/f_4$ evaluation on known small examples.
- [x] **SG-01b:** For prime fields near $2^{16},2^{18},2^{20}$, sample random
  factor bases of size $\lfloor\sqrt p\rfloor$, count all ordered three-term
  decompositions for random targets, and record exhaustive-search work.
- [x] **SG-01c:** Report 95% confidence intervals and compare counts with
  $|\mathcal F|^3/r$.
- [x] **SG-03a:** Repeat the same measurements for
  $\mathcal F=\{P:0\le x(P)<\lfloor\sqrt p\rfloor\}$ and compare normalized
  effects with a size-matched random base.
- [x] **SG-03b:** Determine whether any observed structure yields a
  polylogarithmic decomposition algorithm; keep density and findability
  conclusions separate. [EMPIRICAL: tested sample only] No such structure was
  detected by this attempt; P1.2/Q004 records that A009's later lower bound
  still does not cover every coordinate-aware algorithm.
- [x] **SG-02:** Reproduce the extension-field case at toy scale. Planted
  logarithms were recovered end to end over $\mathbb F_{q^3}$ for
  $q=5,7,11$.
- [x] **SG-04:** Measure bounded rational reconstruction. The symmetric
  square-root bounds selected more than 99.97% of every tested curve group and
  failed the size requirement.
- [x] **SG-05:** Analyze low-degree rational maps and auxiliary plane curves.
  Rational maps from $\mathbb P^1$ are constant; a distinct degree-$d$ plane
  curve contributes at most $3d$ points.
- [x] **SG-06 (proxy):** Measure the denominator-one integral-lift proxy. The
  observed bases had sizes 0, 0, and 2. P1.2/Q002 records why this does not
  settle the full canonical-height predicate.
- [x] **SG-07:** Consolidate the density, size, membership, and findability
  failure modes with explicit falsifiers.
- [x] **SG-08:** Attack the formal support-size obstruction across exact and
  variable length, repetitions, ordering, signs, randomized/nonuniform
  decoders, randomized bases, and toy groups; derive minimal non-vacuous
  repairs. The claim survived and is proved in `CLAIM.md`.
- [x] **SG-09:** Audit the likely square-root correction for uncharged
  preprocessing. Construct a positional radix base, exhaustively cover every
  target on the recorded 16–20-bit curves, quantify the linear-size target
  table, and write non-vacuous uniform variants.
- [x] **SG-10:** Define the translate-probe model containing the generic pair
  scan, prove its $T|\mathcal F|/r$ success bound for fixed, failure-adaptive,
  and randomized schedules, and exhaustively test all one-to-four-shift
  schedules on the order-19 fixture.
- [x] **SG-11:** Audit a coordinate-aware smooth-subgroup factor base. Validate
  its low-degree membership chain exhaustively at $p=65537$, compare density
  and generic search with matched random bases, and benchmark direct versus
  chain Gröbner encodings at $p=17,257,65537$ with timeout distinguished from
  mathematical failure.
