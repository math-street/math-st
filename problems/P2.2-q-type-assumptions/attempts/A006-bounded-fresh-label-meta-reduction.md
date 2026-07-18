---
attempt: A006
status: completed
---
# A006 -- Meta-reduction with bounded representation-native fresh labels

## Goal

[PROVED] Extend the prime-order $q$-SDH meta-reduction to a concrete
representation-dependent reduction that may synthesize valid group encodings
outside the traced group interface, provided it introduces at most $s$ such
fresh source-group labels per execution.

## Prediction after A005, before the proof attempt

[CONJECTURE] The Lu--Zhandry trace survives after allocating one new formal
basis coordinate to every representation-native fresh label.  The single-group
threshold should become $n+s<q-1$, and the safe bilinear threshold should become
$\binom{n+s+2}{2}+t<q$ when at most $t$ unexplained target-group labels are also
introduced.

## Refuting test

[PROVED] The prediction is refuted by either (1) an execution with at most $s$
fresh labels whose adversary-query exponents do not lie in a known
$(n+s+1)$-dimensional linear span, or (2) a step in the inefficient-adversary
simulation that requires the discrete logarithm of a fresh label rather than
only the label and its formal coordinate.

## Plan

[PROVED] Define freshness operationally, rebuild the coefficient trace, replay
the finite-field root-list simulation with the enlarged basis, and then test
adaptive freshness, hidden algebraic relations, equality branches, and pairing
outputs against the claimed dimension bound.

## Reduction class

[PROVED] Fix a concrete prime-order group implementation $G_*$ with efficient
validity, equality, group operations, and known-scalar exponentiation, and a
fixed-size assumption $F^{G_*}$ whose challenger returns at most $n$ source-
group elements over an execution.  A PPT oracle reduction $R$ is **$s$-fresh**
if it is fully black-box in every, possibly inefficient, $q$-SDH adversary and,
on every execution, at most $s$ distinct valid source-group labels first appear
without one of these explanations: challenger output, the public generator,
known-scalar labeling, or a previously observed group operation.

[PROVED] “First appear” is tested when a bit string is first used as a typed
group element, including when it is supplied directly in a $q$-SDH oracle
query.  Thus validation, decompression, hash-to-group, table lookup, and
arbitrary bit-dependent native code are allowed, but every distinct valid
output that lacks a recorded algebraic explanation consumes one freshness
unit.

[PROVED] The freshness bound is semantic and execution-wise; it need not be
derivable from the source code of $R$.  The meta-reduction only maintains a
counter and invokes the theorem under the promise that the counter never
exceeds $s$.

## Bounded-fresh-label separation

[PROVED] **Theorem.** For polynomially bounded $q,n,s$, if $n+s<q-1$, an
$s$-fresh PPT fully-black-box reduction from $q$-SDH to $F^{G_*}$ yields a PPT
attack on $F^{G_*}$ with the reduction's success probability against a perfect
$q$-SDH adversary.  Consequently, if $F^{G_*}$ is hard, no such reduction
exists at that threshold.

### Enlarged coefficient trace

[PROVED] The meta-reduction runs $R$ on the real $F^{G_*}$ challenge and keeps
a dictionary from every typed source label seen so far to a vector in
$\mathbb Z_r^{n+s+1}$.  The coordinates correspond to the at most $n$
challenger labels, the at most $s$ native fresh labels, and the public
generator.

[PROVED] A newly returned challenger label and a newly encountered fresh label
receive their next unused unit vector.  Known-scalar labeling receives the
corresponding multiple of the generator vector.  For a group operation, a new
output label receives the sum or difference of its operands' vectors; if the
actual output label is already in the dictionary, its old vector is retained.

[PROVED] Let $b\in\mathbb Z_r^{n+s+1}$ contain the actual discrete logarithms
of these basis labels relative to the public generator.  Inductively, every
dictionary vector $D(P)$ satisfies
$$
  \log_g P=\langle D(P),b\rangle.
$$
Retaining an old vector after an actual-label collision preserves this
invariant because both candidate vectors evaluate to the same group element;
the meta-reduction never needs to discover the resulting hidden linear
relation among the entries of $b$.

[PROVED] Adaptivity and representation-bit branches do not change the
invariant: the meta-reduction executes the same concrete code on the same
labels, and coefficients may depend on all previously observed bits and
equalities.  Every unexplained valid label created along the chosen branch is
instead charged to the freshness budget.

### Simulating the inefficient adversary

[PROVED] In each oracle call made by $R$, the labels of the proposed $q$-SDH
power ladder therefore form the rows of a known matrix with at most $n+s+1$
columns.  Applying the low-dimensional subspace root-list argument from the
proof of Lu--Zhandry Theorem 5.2 with this enlarged matrix enumerates all
hidden-exponent candidates in polynomial time when $n+s<q-1$.

[PROVED] Concretely, let $M$ contain the coefficient rows for any $q$
independent ladder polynomials, and let $w$ be the actual discrete logarithm of
the queried generator.  For a valid nonidentity tuple with hidden exponent
$x$, the evaluation invariant gives
$$
  M(b/w)^T=(s_1(x),\ldots,s_q(x))^T.
$$
Hence the actual $x$ belongs to the root list even when the basis logarithms
have unknown relations; only the dimension of the column space is used.

[PROVED] Fix the perfect adversary to reject an invalid or identity-generator
tuple and otherwise use deterministic tie-breaking.  For each listed candidate
$x$, the simulator checks the ladder equations by ordinary scalar
exponentiation and equality in the real group.  The nonidentity first ladder
element makes a consistent $x$ unique; the simulator chooses a public
$c\ne-x$ and returns the queried generator raised to $(x+c)^{-1}$.  This uses
labels and formal coefficients only, not the discrete logarithms of the fresh
basis elements.

[PROVED] Rewinding and multiple adaptive oracle calls are covered because the
dictionary and freshness counter persist across the whole execution.  The
simulation is transcript-exact for the selected perfect adversary and adds
only polynomial field arithmetic, root finding, and group operations, so it
introduces no success-probability loss.

## Bilinear extension

[PROVED] For typed $q$-SDH whose oracle instance lies in one source group,
pairing outputs do not enlarge that source-group trace.  If $n_1$ counts all
fixed-assumption challenge labels that can reach that source through recorded
source-to-source maps and $s_1$ counts unexplained labels in that source, the
same proof gives the sharper threshold $n_1+s_1<q-1$, provided there is no
unrecorded target-to-source conversion.

[PROVED] For a broader bilinear $q$-type game whose independent polynomial
family may occur in the target group, or for a conservative common-space
bound, at most $s$ unexplained source labels and $t$ unexplained target labels
give trace dimension
$$
  \binom{n+s+2}{2}+t.
$$
The quadratic term contains all degree-at-most-two monomials in the
$n+s+1$ source coordinates, and each unexplained target label receives one
additional independent coordinate.

[PROVED] Replaying Lu--Zhandry Theorem 5.10 therefore gives that broader
bilinear separation whenever
$$
  \binom{n+s+2}{2}+t<q.
$$
This bound deliberately overcounts monomials that typing may forbid, so it is a
safe sufficient threshold rather than a claimed tight one.

## Outcome and boundary

[PROVED] The refuting test did not fire: every native fresh source label adds
exactly one coordinate, and the adversary simulation never requests its
discrete logarithm.  The prediction is proved for the stated class.

[PROVED] Contrapositively, any fully-black-box fixed-representation reduction
that coexists with hardness of $F^{G_*}$ must, in some execution, introduce at
least $q-1-n_1$ unexplained labels in the $q$-SDH source group, or use an
unrecorded conversion into that source.  For a broader bilinear $q$-type game,
the conservative alternative is to make the enlarged quadratic dimension reach
at least $q$.

[PROVED] This is strictly more representation-dependent than A003: $R$ may
inspect encodings and use native operations in the named implementation.  It
is not an unrestricted black-box impossibility because a reduction with
freshness growing linearly in $q$, or a reduction that reads the adversary's
code, remains outside the theorem.

[CITED] The only imported mathematical ingredient is the low-dimensional
root-list simulation and its bilinear quadratic lift; A006 changes its column
count but not its proof.  [Lu--Zhandry 2024, Lem. 5.1 and Thms. 5.2, 5.10]
