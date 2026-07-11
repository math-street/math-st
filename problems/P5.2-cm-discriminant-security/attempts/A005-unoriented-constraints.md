---
attempt: A005
status: dead
---
# A005 - Intersect unoriented collision constraints

## Idea

Model an unoriented orbit collision by the exact constraint
$$\frac{a+bs}{c+ds}\in H=\langle\lambda\rangle\le\mathbb F_r^*$$
and measure how many independently conditioned constraints identify a toy secret when $H$ has index two or three. Count every candidate membership test and keep synthetic constraint generation separate from the unresolved cost of detecting real point-orbit collisions.

## Prior art

- [PROVED] A004 derives the constraint and shows why the ordinary single linear collision equation is unavailable without the orientation multiplier.
- [PROVED] Membership in the known subgroup $H$ of order $m$ is testable in the scalar field by $z^m=1$, but evaluating the needed scalar ratio for an unknown ECDLP secret is only available inside the offline candidate test used here.

## Plan

1. Generate seeded coefficient quadruples conditioned on a known toy secret and a uniformly sampled multiplier in $H$.
2. Intersect the compatible candidates in $\{1,\ldots,r-1\}$ and verify the known secret always survives.
3. Record survivor counts per constraint, constraints to uniqueness, and total membership checks.
4. Compare information reduction with index $q=(r-1)/m$ while making no claim that the synthetic constraints are cheaply obtainable from curve points.

## Prediction

- [CONJECTURE] For the measured index-two and index-three cases, each independently conditioned constraint will reduce the wrong-candidate population by a factor near $q$, and a median of about $\log_q r$ constraints will isolate the secret. A refuting outcome is a survivor curve that persistently fails to decrease geometrically or never reaches one within $2\lceil\log_q r\rceil+8$ constraints.
- [CONJECTURE] Straight candidate intersection will use $\Theta(r)$ subgroup-membership checks despite requiring only $O(\log r)$ constraints, so it will not yield sub-square-root work. A refuting implementation is a validated solver using $o(\sqrt r)$ field/group operations over the tested increasing sizes.

## Execution log

Recorded before implementation or measurement.

## Outcome

- [PROVED] The attempt was stopped before implementation or measurement because the user explicitly requested that the current work be marked as a failure. No synthetic constraint data were generated, and Q025 was not tested.

## Post-mortem

**Why it failed:** The planned experiment was terminated before implementation by explicit user direction. This is a workflow failure record, not evidence that the mathematical route is false.

**What transfers:** The preregistered constraint model, refutation criteria, and measurement plan remain available if the work is resumed.

**Would it work under different assumptions?** Unknown; no implementation or measurement was run.
