# Handoff - P2.1 - after session 10

## State in five lines

- [PROVED] Fifteen scoped sub-goals are complete and reproducible.
- [PROVED] The requested uniform polynomial-time CDH-to-DLP reduction remains
  open and is recorded as blocking question P2.1/Q005.
- [CONDITIONAL: Riemann Hypothesis] Every sufficiently large prime field has
  a polylog-smooth ordinary abelian-surface order.
- [PROVED] No checked algorithm both finds that order and realizes an explicit
  strongly algebraically defined surface in polynomial time.
- [EMPIRICAL: Python 3.13.4 on Windows 11] All 315 repository tests and 3
  subtests pass; all six P2.1 validation entry points pass.

## What is established

- [CITED] Maurer--Wolf reduces prime-order DLP to CDH given a constant-rank,
  strongly algebraically defined auxiliary group over $\mathbb F_r$ with
  known order $N$ satisfying $P^+(N)=(\log r)^{O(1)}$.
- [PROVED] The exact elliptic CM sufficient condition $\mathsf{SCM}_{C,K}$ is
  recorded in NOTES and Q005, including construction and factorization costs.
- [EMPIRICAL: 4,096 descending 60-bit primes] Bounded CM covered 3,635 inputs
  at discriminant exponent two and all inputs at exponent three for cubic-log
  smoothness; this is finite evidence only.
- [PROVED] Every full algebraic torus of globally bounded dimension has an
  infinite prime family on which its order has a polynomially large factor.
- [PROVED] Chevalley decomposition extends the full-group obstruction to
  every bounded-dimensional connected commutative group with a nonzero affine
  part.
- [PROVED] A public-coin injectivity lemma also rules out polylog-smooth
  selected subgroups of one-dimensional tori with uniformly nonnegligible
  recoverable-encoding success.
- [CONDITIONAL: Riemann Hypothesis] The van Bommel et al. prescribed-order
  interval plus Younis's $\theta=3/4$ theorem gives a smooth ordinary
  abelian-surface order for every sufficiently large prime.
- [PROVED] If an explicit genus-two curve with that Jacobian order is given,
  Cantor arithmetic and the shifted curve-point map provide Maurer--Wolf
  `EMBED/EXTRACT`; the rational-point group has rank at most four.
- [EMPIRICAL: r=251,1019,4091,16363] Every integer in four central intervals,
  including every tested cubic-log-smooth integer, had an ordinary Weil
  polynomial whose isogeny class contains a genus-two Jacobian.

## What is ruled out, within stated models

- [HEURISTIC] Blind random-curve search takes $r^{1/C+o(1)}$ trials under the
  stated random-integer smoothness model; a contrary structured-order theorem
  would falsify this estimate.
- [PROVED] The full multiplicative group, all full bounded-dimensional tori,
  and all full connected commutative groups with affine part are not uniform
  every-prime solutions.
- [PROVED] Boneh's CRT decoder misses the $X^{3/4}$ surface interval for
  smoothness $s=(\log X)^K$ with fixed $K>1$, even under its stronger
  strong-smoothness promise.
- [PROVED] Every globally bounded support size for polylog-smooth products
  misses infinitely many prime-centered surface intervals, even when the
  support is chosen after seeing the input.
- [PROVED] Direct rounding of the unrestricted prime-logarithm subset sum has
  a numerical target $X^{1/4}(\log X)^{O(1)}$; checked pseudopolynomial and
  low-density lattice theorems give no polynomial-time guarantee there.
- [PROVED] HNR certification, Honda--Tate existence, abstract group data, and
  isogeny walks without a seed do not output the explicit recoverable
  auxiliary required by Maurer--Wolf.
- [PROVED] None of these results rules out pure abelian varieties,
  higher-dimensional selected subgroups, or a specialized prime-logarithm
  algorithm.

## Blocking question Q005

[PROVED] A full unconditional reduction needs either the uniform elliptic CM
condition in NOTES, or another every-prime family with a polynomial-time
smooth-order finder, explicit group realization, and recoverable algebraic
embedding.  In the abelian-surface branch the two missing algorithms are:

1. [PROVED] Find a polylog-smooth integer in the central $r^{3/2}$-length
   surface-order interval in time polynomial in $\log r$.
2. [PROVED] Realize its Weil polynomial as an explicit surface with
   polynomial group law and Maurer--Wolf `EMBED/EXTRACT` in the same time.

## Next action

[PROVED] The dimension-one cardinality proof does not cover dimension at least
two.  Next audit higher-dimensional selected subgroups and cofactor-projection
encodings, while keeping the smooth-order finder and explicit surface seed as
independent gaps.

## Invariants

- [PROVED] Smooth means largest prime factor at most the stated bound.
- [PROVED] Finite ensembles are deterministic toy experiments, never
  universal proof.
- [PROVED] The CM scanner tests norm-equation reachability; it does not build
  curves.
- [PROVED] The HNR scanner certifies isogeny-class existence; it does not
  build curves.
- [PROVED] The iid theorem is model-only; actual curve-order maps are
  structured.
- Do not extrapolate experiments beyond $\log_2 r\le60$.

## Files that matter

- `NOTES.md`: stable theorem, evidence, and obstruction record.
- `attempts/A007-abelian-surface-existence.md`: conditional positive theorem.
- `attempts/A008-crt-smooth-finder.md`: exact decoder-radius failure.
- `attempts/A009-explicit-surface-realization.md`: four realization levels.
- `attempts/A010-exponent-vector-finder.md`: latest finder obstruction.
- `code/surface_jacobian_scan.py`: exact toy HNR scanner with tests.
- `audits/AUDIT-20260721-session10.md`: current consistency audit.
- `LOG-archive/LOG-001-010.md`: full session history.

## What I would tell my replacement

[CONDITIONAL: Riemann Hypothesis] The strongest positive result is smooth
surface-order existence, not construction.

[PROVED] The cleanest negative result in the latest session is the bounded-support
coverage theorem; the full-support precision calculation is a barrier for
standard reductions, not a general complexity lower bound.
