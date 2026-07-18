---
attempt: A003
status: completed
---
# A003 -- Representation-uniform fully black-box reductions

## Goal

[PROVED] Define a standard-oracle reduction class that may inspect group
encodings as bit strings but whose single machine and security guarantee are
uniform over every admissible prime-order group representation, and test
whether this class is strictly stronger than Lu--Zhandry GR-BB.

## Prediction before the literature audit

[CONJECTURE] Once the quantifiers are explicit, this class is not an extension:
instantiating the universal guarantee with a random sparse encoding yields the
type-safe/generic-representation experiment, so the Lu--Zhandry separation
applies unchanged.  Only a guarantee tied to a particular representation, or
a reduction that reads the adversary's code, should escape that conclusion.

## Refuting test

[PROVED] The prediction is refuted if there exists one reduction machine that
uses only the standard group interface, is guaranteed to work for every
admissible encoding, yet cannot be expressed as a Lu--Zhandry
generic-representation reduction; alternatively, a step in the random-encoding
instantiation must require an assumption absent from the universal guarantee.

## Status

[CITED] Lu--Zhandry GR algorithms may use arbitrary bit gates on concrete group
labels, while their advantage is the infimum over all possibly inefficient
implementations of the group.  Thus the GR model does not forbid looking at
representation bits; it forbids relying for success on one representation.
[Lu--Zhandry 2024, §3.2]

## Definition: UR-FBB

[PROVED] For single-stage prime-order group games $F$ and $Q$, call a reduction
**universally representation-uniform fully black-box** (UR-FBB) if a single PPT
oracle machine $R$ has the following properties:

1. [PROVED] $R$ treats the $Q$-adversary as an oracle, although it may run
   multiple copies and rewind them.
2. [PROVED] $R$ uses the group through labeling, group-operation, equality, and,
   when present, pairing interfaces; it may otherwise perform arbitrary bit
   computations on the labels it receives.
3. [PROVED] For every admissible implementation $G$ of the prime-order group,
   including possibly inefficient implementations, and every possibly
   inefficient adversary $A$, the following uniform implication holds: for
   every non-negligible lower bound $\epsilon$, there is a non-negligible
   $\delta$ independent of $G$ and $A$ such that
   $\operatorname{Adv}_{Q^G}(A)\ge\epsilon$ implies
   $\operatorname{Adv}_{F^G}(R^{A,G})\ge\delta$.  The machine is also
   independent of $G$.

[CITED] Conditions 1 and 2 match the ordinary fully-black-box analysis
interface: a fixed efficient oracle machine converts every, even inefficient,
adversary by oracle access only.  [Reingold--Trevisan--Vadhan 2004, Def. 3;
Lu--Zhandry 2024, §2]

## Boundary corollary

[PROVED] **Corollary.** If a UR-FBB reduction from a $q$-type game $Q$ to a
fixed-size game $F$ exists, then a Lu--Zhandry GR-BB reduction from $Q$ to $F$
exists.

[PROVED] **Proof.** A GR adversary is one oracle circuit whose advantage is
non-negligible under the infimum over all group implementations.  Hence it
has a common non-negligible lower bound $\epsilon$ against $Q^G$ for every
implementation $G$.  Apply UR-FBB condition 3 pointwise to obtain one
non-negligible $\delta$ such that
$$
 \inf_G\operatorname{Adv}_{F^G}(R^{A,G})\ge\delta.
$$
Conditions 1 and 2 make $R$ a GR oracle circuit, so this is a GR-BB reduction
(and is stronger than the source definition, which may assign a reduction to
each adversary).

[CITED] For single-stage games, the same conclusion can be stated in the
type-safe model because TS-BB and GR-BB reductions exist if and only if one
another.  [Lu--Zhandry 2024, Lem. 3.2]

[CITED] The random sparse-encoding wrapper explains why label inspection does
not invalidate the corollary: for
$\ell>\log_2 r+\omega(\log\lambda)$, a polynomial interaction guesses a valid
but previously unseen random label only with negligible probability, and the
wrapper perfectly simulates every other labeling and group-operation query.
[Lu--Zhandry 2024, Lem. 3.1]

## Instantiation to $q$-SDH

[CITED] Since $q$-SDH is a Lu--Zhandry $q$-type game, no UR-FBB reduction can
base it on a true fixed-size prime-order assumption of size $n$ when $n<q-1$;
in the generic bilinear setting the corresponding threshold is
$\binom{n+2}{2}<q$.  [Lu--Zhandry 2024, Thms. 5.2, 5.10, Claim 6.2, Cor. 6.1]

## Outcome

[PROVED] The prediction survived its refuting test: UR-FBB is not a new class
beyond GR-BB.  It is a clean standard-oracle corollary of the published
separation, and it makes explicit that arbitrary computation on encoding bits
does not help when the success guarantee is universal over representations.

[PROVED] The qualifier “universal” includes possibly inefficient random sparse
implementations.  A guarantee only over efficiently computable or standardized
representations need not include them and is not promoted to GR-BB by this
argument.
