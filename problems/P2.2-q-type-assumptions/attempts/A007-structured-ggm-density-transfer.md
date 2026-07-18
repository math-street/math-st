---
attempt: A007
status: dead
---
# A007 -- Can structured-GGM density control native freshness?

## Goal

[PROVED] Test whether the density parameter in the structured generic-group
model converts a representation-dependent reduction into A006's bounded-fresh
class, thereby extending the $q$-SDH separation to reductions that exploit a
sparse amount of public label structure.

## Prediction after reading the model definition, before the transfer attempt

[CONJECTURE] The density $\delta$ alone will not give a deterministic bound on
the number of native labels a reduction can first-use.  The model controls the
probability that a random challenge interaction hits the structured region,
whereas A006 needs an execution-wise dimension bound on adaptively chosen
labels.

## Refuting test

[PROVED] The prediction is refuted if Theorem 3.2, from $\delta$ and the number
$T$ of generic group-oracle queries alone, implies a bound
$s=o(q_{\mathrm{lad}})$ on the distinct valid labels that a PPT reduction can
introduce natively, where $q_{\mathrm{lad}}$ is the $q$ in $q$-SDH.

## Audited structured-GGM statement

[CITED] A structured label space supplies a partial operation $\star$ on
labels, and every defined value agrees with the hidden group operation.  The
algorithm may evaluate $\star$ for free; only generic group-operation-oracle
queries count toward $T$.  [Corrigan-Gibbs--Henzinger--Wu 2026, Defs. 2.2--2.4]

[CITED] A label is constrained when it participates nontrivially in a defined
$\star$ relation.  For a prime-order-$r$ structured group in which a $\delta$
fraction of labels are constrained, Theorem 3.2 constructs a distribution over
labelings for which every $T$-query discrete-log algorithm has advantage at
most
$$
  \delta(3T+2)+\frac{(3T+1)^2}{r}+\frac1r.
$$
[Corrigan-Gibbs--Henzinger--Wu 2026, Def. 3.1 and Thm. 3.2]

[CITED] The hard distribution fixes the discrete logarithms of all constrained
labels according to one structured labeling and randomly completes the
unconstrained labels.  The theorem is existential in that distribution and is
not a hardness claim for every named concrete labeling.  [Corrigan-Gibbs--
Henzinger--Wu 2026, proof of Thm. 3.2]

## Transfer attempt

[PROVED] The first proposed transfer was to identify A006's freshness budget
with the expected number $O(\delta T)$ of interactions with constrained labels.
This is invalid: the $\delta T$ term is a bad-event probability in a random-
challenge discrete-log hybrid, not a count of labels chosen by an algorithm.

[PROVED] Density does not impose an execution-wise freshness bound.  If the
publicly recognizable constrained subset has size $\delta r\ge
q_{\mathrm{lad}}$, an algorithm can address $q_{\mathrm{lad}}$ distinct labels
from that subset even when $\delta$ is negligible; its choices are not uniform
samples from the full label space.

[PROVED] The model is even less compatible with the desired count because
$\star$ evaluations and all other computation are free in its lower-bound cost
measure.  Hence the theorem's $T$ generic-oracle queries do not bound the
number of labels enumerated, parsed, or produced through $\star$ and then used
as group elements.

[PROVED] The second proposed transfer was to instantiate the hard structured
labeling distribution and invoke a purported reduction there.  This repeats
A004's quantifier error: a reduction guaranteed only for one concrete labeling
need not retain its guarantee on the theorem's newly constructed distribution.

## What does transfer

[PROVED] If a separate premise bounds by $u$ the total number of distinct
valid labels first-used through raw representation code or free $\star$
evaluation, then A006 applies verbatim with $s=u$.  Thus
$n_1+u<q_{\mathrm{lad}}-1$ is sufficient for the source-group separation.

[PROVED] Merely charging $T_\star$ evaluations of $\star$ gives at most
$3T_\star$ participating labels from those evaluations, but raw valid labels
must still be counted separately.  This conditional accounting is absent from
Theorem 3.2, where $T_\star$ is free and unbounded by the stated query measure.

## Outcome and post-mortem

[PROVED] The refuting test did not fire.  The $\delta$ parameter controls a
random-hybrid collision probability, not A006's adversarially selected trace
dimension, and the structured-GGM lower bound is for discrete log rather than
a $q$-type-to-static reduction.

[PROVED] This attempt is dead as an automatic density-to-freshness transfer.
Reviving it requires an additional explicit budget on distinct native labels,
or a new structured meta-reduction whose invariant exploits the algebraic
relations revealed by $\star$ instead of assigning one independent coordinate
per native label.

[PROVED] The failed transfer narrows Q003: “structure is sparse” is not itself
a sufficient scope condition.  The relevant resource is the rank or number of
native labels actually injected into the adversary transcript.
