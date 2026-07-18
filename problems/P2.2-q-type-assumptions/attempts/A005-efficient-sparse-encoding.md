---
attempt: A005
status: dead
---
# A005 -- Replace random sparse labels by an efficient encoding family

## Goal

[PROVED] Attempt to extend A003 to a reduction promised over every efficiently
computable prime-order representation by replacing the uniformly random
injection in Lu--Zhandry Lemma 3.1 with an efficiently sampled sparse encoding.

## Prediction before literature search

[CONJECTURE] No unconditional extension will follow.  A finitely seeded
efficient encoding family has succinct structure that a possibly inefficient
adversary can identify, whereas the published wrapper uses an
information-theoretically random injection.  A pseudorandom permutation would
replace the missing information-theoretic statement only under an additional
computational assumption.

## Refuting test

[PROVED] The prediction is refuted if either of the following is established:

1. [PROVED] an efficiently computable injective encoding family is
   information-theoretically indistinguishable from a random sparse injection
   for every interaction permitted in the fully-black-box reduction; or
2. [PROVED] the wrapper needs indistinguishability only against a
   polynomial-query view independent of the possibly inefficient adversary's
   internal group queries, so a finite-wise independent construction suffices.

## Plan

[PROVED] Audit the exact query and efficiency quantifiers in the relevant
generic-representation definitions, inspect later work on random versus
efficient representations, then attempt both finite-wise independence and PRP
substitutions before assigning an outcome.

## Execution: finite-seed counting obstruction

[PROVED] Let the encoding domain have $r$ elements, let the label space have
$N\ge r$ elements, and let an efficiently sampled encoding family be indexed by
an $m(\lambda)$-bit seed, where $m$ is polynomial.  The family contains at most
$2^m$ injective tables, whereas the uniform random-injection distribution has
support size
$$
  (N)_r=N(N-1)\cdots(N-r+1).
$$

[PROVED] A possibly inefficient distinguisher queries the encoding on all
$r$ inputs, reconstructs its full table, enumerates all $2^m$ seeds, and accepts
exactly when the table belongs to the efficient family.  It accepts a family
member with probability one and a uniform random injection with probability at
most $2^m/(N)_r$.

[PROVED] Since $r$ is exponential in the security parameter and
$\log (N)_r\ge \log(r!)=\Omega(r\log r)$, while $m$ is polynomial, the latter
probability is negligible.  Thus no polynomial-seed family is
information-theoretically indistinguishable from the random injection against
the possibly inefficient adversaries required by the fully-black-box
definition.

## Why the two proposed substitutions fail

[PROVED] A $t$-wise independent encoding can match at most a bounded-query view;
the exhaustive distinguisher uses $r>t$ queries.  The fully-black-box adversary
quantifier does not supply a polynomial query bound, so finite-wise independence
does not meet the refuting test.

[PROVED] A PRP can replace a random permutation only against computationally
bounded distinguishers.  The exhaustive distinguisher above is allowed here,
so a PRP neither gives an information-theoretic wrapper nor an unconditional
meta-reduction.

[CITED] Zhandry's type-safe query model makes the same distinction especially
explicit: bit computation may be unbounded, and no efficient keyed permutation
pair in that model is a secure PRP.  [Zhandry 2022, §4.2, Thm. 4.10]

[CITED] Wang et al. independently emphasize that the sparse encoding needed to
prevent unqueried valid-label generation excludes important elliptic-curve and
dense/admissibly encoded group behaviors, including in the bilinear extension.
[Wang et al. 2025, abstract]

## Second obstruction: hardness is family-local

[PROVED] Even an attack on a specially constructed efficient encoding of the
abstract cyclic group would refute the fixed-size assumption only for that
encoding.  If the assumption is asserted for a named curve family $G_*$, an
attack on a different artificial family does not contradict its premise.

## Outcome

[PROVED] A005 is dead.  The finite-seed construction fails information
theoretically against the required adversary class, and weakening to efficient
adversaries or a PRP changes the reduction notion.  Moreover, changing the
group family would not by itself refute a family-local static assumption.

## Post-mortem

[PROVED] What transfers is the query-bounded version: if the reduction class
quantifies only over adversaries making at most $t$ encoding/group queries, a
$t$-wise or lazy-table simulation becomes plausible.  That is a different,
strictly narrower class and must state the query bound explicitly.
