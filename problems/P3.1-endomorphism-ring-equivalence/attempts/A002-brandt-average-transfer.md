---
attempt: A002
status: dead
---
# A002 - Transfer average binary-form prime bounds through Brandt mixing

## Idea

- [CITED] Wesolowski's Algorithm 2 first makes the input quaternion ideal class nearly uniform by a Brandt-graph walk and then invokes Proposition 3.8 to replace that ideal by an equivalent ideal of prime norm (Wesolowski 2022, Theorem 6.2 and Algorithm 2).
- [CONJECTURE] The proposed shortcut was that this first randomization might make an unconditional average-over-binary-form-classes prime theorem sufficient even though Proposition 3.4 is pointwise.
- [CONJECTURE] A refuting test is a proof that the deterministic binary-subform map used in Proposition 3.5 can concentrate a uniform Brandt class distribution on an exceptional family of binary forms.

## Prior art

- [CITED] Sardari 2019, Theorem 1.1 and Corollary 1.3, controls the proportion of binary form or ideal classes that represent a prime in a specified range.
- [CITED] Ditchen 2018, Theorems 1.1--1.2 and Corollary 1.8, averages first over negative fundamental discriminants and then over form classes; it gives its strongest least-prime conclusion for most forms attached to most discriminants.
- [CITED] Wesolowski 2022, Proposition 3.5, maps a rank-four norm form to a binary form by choosing the first LLL vector, partially factoring its value, and constructing a second vector by coefficient gcd tests.

## Plan

- [PROVED] The distribution supplied by Brandt mixing must be pushed through the exact deterministic map in Proposition 3.5 before any binary average theorem can be applied.
- [PROVED] It would suffice to prove that the pushforward places at least inverse-polylogarithmic mass on binary classes having inverse-polylogarithmic prime density in a polynomial-bit-length interval.

## Execution log

- [CITED] Theorem 6.2 makes the quaternion ideal class nearly uniform, with pointwise error controlled by the Ramanujan eigenvalue bound (Wesolowski 2022).
- [CITED] Proposition 3.5 then chooses the binary restriction
  \(g_{u,v}(x,y)=q_{I'}(xu+yv)\), where \(u\) is an LLL vector and \(v\) depends on the factor/gcd pattern of \(q_{I'}(u)\) (Wesolowski 2022).
- [PROVED] Consequently the sampled object is a quaternion ideal class, not a uniform binary-form class of a fixed discriminant.
- [PROVED] The discriminant and class of \(g_{u,v}\) both vary with \(I'\), and no symmetry in the Brandt action makes the LLL-and-gcd selection equivariant under binary class-group composition.
- [PROVED] Sardari's and Ditchen's exceptional-set estimates therefore cannot be applied to this pushforward without an additional anti-concentration theorem for the map \([I']\mapsto[g_{u,v}]\).
- [PROVED] Knowing that a positive proportion of all binary classes is good does not help if this deterministic map is allowed to concentrate on the complementary set.

## Outcome

- [PROVED] Brandt mixing alone does not convert the checked average binary-form theorems into a proof of Proposition 3.8.
- [PROVED] The exact missing statement is an anti-concentration or domination bound for the pushforward of the uniform Brandt-class measure under Proposition 3.5's LLL-and-gcd binary-subform selection.
- [CITED] No such statement occurs in Sardari 2019, Ditchen 2018, or Wesolowski 2022.
- [PROVED] This negative result is specific to the proposed transfer; it does not rule out bypassing the binary restriction and sampling the rank-four norm form directly.

## Post-mortem

**Why it failed:**

- [PROVED] The two probability spaces do not match, and the deterministic map between them has no checked distributional guarantee.

**What transfers:**

- [PROVED] Any future average theorem must either be stated directly for norm forms of random quaternion ideal classes or prove an explicit pushforward domination bound for the binary restriction used by the algorithm.

**Would it work under different assumptions?**

- [CONDITIONAL: pushforward anti-concentration] Yes; inverse-polylogarithmic domination of the relevant binary-class measure would make an average prime-density theorem usable after the Brandt walk.
