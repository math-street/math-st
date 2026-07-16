---
attempt: A003
status: completed-with-condition
---
# A003 — Growing field-equation gap in a quadratic Semaev descent

## Idea

[EMPIRICAL: initial $q=7,11,13,17$ rows] The $n=m=2$ known-target rows suggested a constant first fall degree and solving degree growing with the base field. The goal was to determine whether this was a one-off or a reproducible family pattern.

## Prior art

[CITED] Caminata and Gorla (2023), Section 4, prove that first fall and solving degree can be arbitrarily far apart for general finite-field systems. Their Example 4.2 has a field-equation-driven gap, but it is not a Semaev/Weil system.

[CITED] Kousidis and Wiemers (2019) prove a first-fall upper bound and report F4 step degrees for binary Semaev descents. Their asymptotic question is not settled by odd-characteristic, fixed-$n$ data.

## Plan

1. Prove the observed first-fall value from the top-coordinate shape.
2. Extend the exact Macaulay computation to larger independent $q$.
3. Require a constructed decomposition and verify it as a root.
4. State only the finite observation as empirical; expose the family formula as a falsifiable conjecture.

## Execution log

[PROVED] For a non-base quadratic target, the top parts are $x_1^2x_2^2$ and $c x_1x_2(x_1+x_2)$, $c\ne0$. Their first nontrivial syzygy is in degree 5; the support argument excluding degrees 3 and 4 is in `NOTES.md`.

[EMPIRICAL: $q=19,23$] Both extension runs completed. They returned $(d_{\mathrm{ff}},d_{\mathrm{reg}},\operatorname{sd})=(5,19,19)$ and $(5,23,23)$, with verified known decompositions.

[PROVED] Session 3 proved $d_{\mathrm{reg}}=q$ from the four-generator top
ideal and proved $\operatorname{sd}\ge q$ whenever the field equations enlarge
the core ideal.

[PROVED] Attempt A004 constructs a degree-at-most-4 mutant family inside the
original degree-$q$ closed Macaulay space. Salizzoni's general bound gives the
mutant family solving degree at most 5, hence the original solving degree is at
most $q$ for every odd prime power $q\ge5$.

## Outcome

[EMPIRICAL: $q\in\{7,11,13,17,19,23\}$] The solving-minus-first-fall gaps are $2,6,8,12,14,18$. The prompt's concrete-divergence falsifier is met at the first row and strengthened by the growing sequence.

[CONDITIONAL: the field equations enlarge the core ideal] The exact family
formula is now
$d_{\mathrm{ff}}=5<d_{\mathrm{reg}}=\operatorname{sd}=q$ for $q>5$, and
all three quantities equal 5 at $q=5$.

[REFUTED by A005] The nonredundancy condition is not automatic. A genuine
eligible Semaev system over $q=7$ has
$(d_{\mathrm{ff}},d_{\mathrm{reg}},\operatorname{sd})=(5,7,5)$, and A005
gives an infinite redundant family for $q\equiv3\pmod4$.

[EMPIRICAL: 397 structured verified-root variants over $q\in\{5,7,11\}$]
Every sampled curve and target has nonredundant field equations and matches
the conditional theorem. A005 showed that the sampler's fixed non-base
coefficient of $A$ excluded the base-defined counterexample family.

## Limitation

[PROVED] Field-equation nonredundancy is false in general. The growing-gap
formula remains exact for nonredundant systems, but this attempt does not
transfer to characteristic two, $m>2$, or the $n\sim\log q$ regime.
