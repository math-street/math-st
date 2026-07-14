---
attempt: A002
status: dead
---
# A002 - Reproduce the p=17 Experiment A dependency count

## Idea

[CITED] Jacobson, Koblitz, Silverman, Stein, and Teske (2000) report 317
dependent cases among 100,000 executions of Experiment A at $p=17$, using
projective lattice lifts, small curve coefficients, and 2-descent.

## Prior art

[CITED] Section 5.4 specifies the finite curve
$y^2=x^3+2x+2$, its order 19, generator $(3,1)$, the restriction
$P_1\ne\pm P_2$, and the broad lattice steps, but it refers implementation
details to Silverman's paper and reports that the computation used LiDIA and
SIMATH.

## Plan

1. Reproduce the published finite input exactly.
2. Sample short projective vectors reducing to the selected finite points.
3. Solve the seven-coefficient congruence lattice over the integers.
4. Select a small-discriminant nearby curve.
5. Search dependence relations with coefficient bound eight and compare the
   observed rate with $317/100000$.

## Execution log

[PROVED] `code/reproduce_xedni_p17.py` reconstructs the finite input, computes
integer solution lattices through Smith decomposition, converts valid
projective models to standard Weierstrass form, and rechecks containment and
reduction exactly.

[EMPIRICAL: three smoke rows only] The prototype can generate internally valid
lifted curves and run the bounded-relation diagnostic.

## Outcome

[PROVED] This is not a reproduction of the published experiment and no
dependency-rate comparison from it is accepted as evidence.

## Post-mortem

**Why it failed:** [PROVED] The source does not specify a probability
distribution or tie-breaking rule over the many short projective lattice
vectors and nearby coefficient-lattice vectors. Those choices directly change
the discriminant distribution and therefore the dependence rate.

**Why it failed:** [EMPIRICAL: local environment on 2026-07-14] The LiDIA/
SIMATH implementation and the paper's 2-descent dependence test are not
available locally. A coefficient-eight search can certify a found relation but
cannot certify rational independence, so it is not an equivalent replacement.

**What transfers:** [PROVED] The finite parameters, projective containment
equations, Smith-lattice construction, and standard-model conversion are
validated components that can be reused if the original sampling code or a
fully specified distribution becomes available.

**Would it work under different assumptions?** [CONDITIONAL: the original
LiDIA/SIMATH code or a complete specification of its sampling and 2-descent
pipeline, as recorded in Q018] The 100,000-run count could be reproduced and
compared fairly.
