# Handoff — P4.3 — failed after session 2

## Terminal state

The formal objective failed: no unconditional $L_Q(1/3,c)$ complexity theorem was proved for exTNFS or for a complete modified DLP algorithm. At the user's request, the task is marked abandoned, the scaffold's terminal equivalent of failed.

SG-01 through SG-12 produced a rigorous obstruction audit and several partial theorems. These artifacts are retained because they identify exactly what a future proof must add.

## Established results

- The exTNFS pipeline has been decomposed into ten numbered analytic and algorithmic assumptions.
- Each smoothness assumption is stated as a uniform density claim for the relevant norm form, with known, partial, or open status.
- Exact toy experiments compare tower-norm smoothness against independently factored random-integer baselines.
- A003 gives exact quadratic norm identities and proves algebraic surjectivity of a kernel-randomized coefficient map under an ideal-coprimality condition.
- A003 also proves the decisive degree barrier: fixed outer degree gives norms larger than the optimized $L_Q(2/3)$ scale in the strict medium-characteristic interior, while optimal parameters force the outer degree to grow.
- A004 isolates the missing relation-rank statement as a quantitative hyperplane-escape condition for accepted relation rows.
- A005 proves an unconditional $L_Q(1/3,O(1))$ relation-supply theorem only for a restricted boundary family with ell_p = 2/3, p congruent to 3 modulo 4, and eta = 2.
- A006 proves a counting obstruction to placing generic full-size targets in a low-degree tower subspace.
- A007 records the resultant bidegree obstruction: the A005 smoothness argument applies to linear relation polynomials, whereas generic targets and descent objects have growing degree.

## Why the formal target failed

The A005 theorem is not a DLP theorem. It supplies sufficiently many candidate relations only in a restricted fixed-quadratic boundary family. It does not prove:

1. that accepted relations span the required relation lattice;
2. that arbitrary targets split into objects covered by the same smoothness theorem;
3. that special-q descent succeeds with the necessary uniform probability and cost;
4. that the construction survives the growing outer degree required by optimized strict-medium exTNFS.

The central unresolved dependencies remain Q016 and Q017, together with assumptions S-04 through S-08.

## Resume conditions

There is no next action while this terminal status stands. Resume only if the abandoned decision is intentionally reversed.

A valid continuation would need a new theorem or algorithmic modification addressing at least one of:

- uniform lower bounds for smooth values of growing-degree tower norm forms;
- character cancellation or hyperplane escape after conditioning on simultaneous smoothness;
- a provable target-splitting distribution compatible with the restricted relation generator;
- a rigorous special-q descent whose degrees and coefficient sizes remain within the claimed complexity.

Do not promote A005 to an unconditional exTNFS or DLP complexity theorem: it proves restricted relation supply only.
