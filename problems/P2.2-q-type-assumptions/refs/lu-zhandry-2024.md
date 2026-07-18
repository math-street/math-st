# Lu–Zhandry — prime-order separation

George Lu and Mark Zhandry, “Limits on the Power of Prime-Order Groups:
Separating Q-Type from Static Assumptions,” CRYPTO 2024, Part V, LNCS 14924,
46–74; IACR ePrint 2024/993.

Primary text: <https://eprint.iacr.org/2024/993.pdf>

## Exact scope

[CITED] Section 3.2 formalizes a generic-representation reduction that is
fully black-box in every possibly inefficient adversary and can observe the
adversary's group-operation queries.

[CITED] A GR algorithm receives concrete bit-string labels and may apply
ordinary bit gates to them.  Representation independence is enforced by
defining its advantage as the infimum over all possibly inefficient group
implementations, rather than by hiding the labels.  [§3.2]

[CITED] Lemma 3.1 uses a random injection into a sparse label space to equate
type-safe and GR security for sufficiently large label length.  Lemma 3.2 lifts
the wrapper argument to reductions and proves that TS-BB and GR-BB reductions
exist if and only if one another for single-stage games.  [§3.3]

[CITED] Definitions 4.1–4.2 allow interactive fixed-size and $q$-type
assumptions; fixed size counts at most $n$ challenger-produced group elements,
while $q$-type requires at least $q$ independent bounded-degree polynomial
functions tied to a recoverable hidden value.

## Main results

[CITED] Theorem 5.2 says that a reduction from such a $q$-type assumption to a
fixed-size assumption with $n<q-1$ yields a GGM attack on the fixed-size
assumption.

[CITED] Theorem 5.10 gives the bilinear threshold
$\binom{n+2}{2}<q$ because pairings enlarge the trace space to quadratic
monomials.

[CITED] Claim 6.2 instantiates the class with $q$-SDH, and Corollary 6.1 states
that no generic reduction from $q$-SDH to a true fixed-size assumption exists.

## Audit note

[PROVED] The GR-BB definition in Section 3.2, Definitions 4.1 and 4.2, the proofs of Theorems 5.2 and 5.10,
and the $q$-SDH instantiation in Claim 6.2 were checked in the primary text.

[CITED] The paper does not claim an impossibility for representation-dependent
or non-black-box-in-the-adversary standard-model reductions.  [§§1.3–1.4]

[CITED] Section 3.5 does not completely rule out groups derived using auxiliary
bit strings, equality-dependent operations, or concrete representation bits;
its structural reduction to products of the base group assumes a natural
affine algebraic form for the derived group law.
