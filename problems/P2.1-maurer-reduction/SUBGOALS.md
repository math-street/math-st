# Sub-goals

- **SG-01 (completed):** State the auxiliary field, curve-order factorization,
  subgroup condition, oracle interface, and largest-prime-factor bound needed by
  Maurer's reduction; verify each point against a primary source.
- **SG-02 (completed):** Validate point counting on hand-countable curves,
  then sample curves over prime fields and record the first $B$-smooth order.
- **SG-03 (completed for the initial baseline):** Compare observed success rates with a precisely defined
  Dickman-style smoothness baseline and include binomial confidence intervals.
- **SG-04 (completed, A002):** Enumerate ordinary CM-reachable smooth orders
  through 60 bits, validate the trace formulas, and record the least
  fundamental discriminant and class-number cost.
- **SG-05 (completed for the recorded ensemble):** Rank the 4,096 tested
  60-bit primes by least discriminant and aggregate coverage modulo 12 with
  Wilson intervals; retain the result as finite evidence only.
- **SG-06 (completed as an obstruction, not a solution):** Reduce the CM route
  to the explicit $\mathsf{SCM}_{C,K}$ condition and show why blind and
  polylog-candidate searches remain super-polynomial under the stated
  smoothness heuristic.  The missing uniform theorem is Q005.
- **SG-07 (completed, A003):** Audit multiplicative and current
  short-interval alternatives.  Prove that infinitely many shifted-prime
  inputs rule out the full multiplicative auxiliary group, while recording
  exactly why this does not eliminate selected subgroups, tori, or curves.
- **SG-08 (completed in an explicit model, A003):** Prove and test the optimal
  adaptive success probability $1-(1-\alpha)^q$ for an iid Hasse-order oracle,
  and separate that theorem from any unproved lower bound for real curve
  construction.
- **SG-09 (completed, A004):** Give and exhaustively validate the quadratic
  norm-one torus embedding, then use CRT and Linnik's theorem to construct an
  infinite prime family on which both $r-1$ and $r+1$ have polynomially large
  factors.  Generalize the obstruction to every fixed bounded-degree menu of
  full norm-one tori.  This does not rule out selected subgroups, general
  bounded-dimensional tori, or elliptic curves.
- **SG-10 (completed, A005):** Use the finite-order Frobenius character lattice
  to express every bounded-dimensional full torus order through a finite
  cyclotomic menu, then force a polynomially large factor in every menu entry
  simultaneously by PNT, CRT, and Linnik.
- **SG-11 (completed, A006):** Use Chevalley decomposition, the split
  unipotent radical, and Lang's theorem to reduce every full smooth connected
  commutative auxiliary group of bounded dimension to the pure abelian-
  variety case.  Prove a public-coin counting lemma that also rules out
  polylog-smooth selected subgroups of one-dimensional tori with uniformly
  nonnegligible recoverable-encoding success.
- **SG-12 (completed, A007):** Combine the fixed-dimension prescribed-order
  interval with the RH short-interval smooth-number theorem to prove
  every-prime polylog-smooth abelian-surface order existence under RH.  Show
  explicitly why finding the order and constructing a strongly algebraically
  defined surface remain separate polynomial-time gaps, while proving that an
  explicit genus-two Jacobian would satisfy the embedding interface.
- **SG-13 (completed, A008):** Substitute the abelian-surface interval and
  polylogarithmic smoothness scales into Boneh's exact CRT-decoding bound.
  Show that the decoder misses the required interval for every fixed
  smoothness exponent greater than one, even under a strong-smoothness
  promise, and isolate the sparse $s=\Theta(\log X)$ window it can reach.
- **SG-14 (completed, A009):** Separate Weil-polynomial construction,
  Honda--Tate existence, Jacobian-in-isogeny-class existence, and explicit
  strong algebraic definition.  Implement the exact ordinary HNR criterion
  at toy scale and show that existence survives throughout four central
  intervals, while the curve-equation seed remains unavailable uniformly.
- **SG-15 (completed as an obstruction, A010):** Audit exponent-vector,
  subset-product, and logarithmic-lattice finders.  Prove that every bounded-
  support product menu misses infinitely many prime-centered surface
  intervals, and show that the standard full-factor-base rounding has an
  exponential numerical target and lies outside the checked low-density
  lattice regime.
