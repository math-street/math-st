---
attempt: A002
status: completed
---
# A002 — Audit and instantiate the Lu–Zhandry meta-reduction

## Target

[CITED] Rule out reductions that are polynomial-time, independent of the
prime-order group representation, and fully black-box in every potentially
inefficient adversary for $q$-SDH.  [Lu–Zhandry 2024, §3.2]

## Instantiation to $q$-SDH

[CITED] The $q$-SDH ladder exposes at least $q$ linearly independent
polynomials in its hidden exponent, and knowledge of that exponent permits an
efficient valid answer by selecting any $c\ne-x$ after a generic consistency check.
[Lu–Zhandry 2024, Claim 6.2]

[CITED] Therefore $q$-SDH belongs to the paper's $q$-type class, and its main
theorem applies to every interactive fixed-size assumption whose challenger
emits at most $n$ group elements.  [Lu–Zhandry 2024, Defs. 4.1–4.2]

## Meta-reduction

[CITED] Choose an inefficient perfect $q$-SDH adversary that brute-forces
discrete logarithms, checks that its input is a consistent power ladder, and
then answers the relation.  A purported fully black-box reduction must work
with this adversary.  [Lu–Zhandry 2024, Thm. 5.2 proof]

[CITED] Trace every group element formed by the reduction as a coefficient
vector over the fixed challenge elements.  Any oracle query containing $q$
independent polynomial evaluations lies in a subspace of dimension at most
$n+1$; a Vandermonde determinant and finite-field root finding recover the
polynomially many hidden-exponent candidates.  Generic equality tests select
consistent candidates, so the meta-reduction simulates the inefficient
adversary efficiently.  [Lu–Zhandry 2024, Thm. 5.2 proof]

[CITED] The supposed reduction, with its oracle replaced by that simulation,
is an efficient generic attack on the fixed-size assumption whenever
$n<q-1$.  [Lu–Zhandry 2024, Thm. 5.2]

[CITED] In the bilinear setting, pairing products enlarge the trace space to
all degree-at-most-two monomials in the $n$ challenge exponents, of dimension
$\binom{n+2}{2}$; the attack follows when $\binom{n+2}{2}<q$.
[Lu–Zhandry 2024, Thm. 5.10]

## Outcome

[CITED] Corollary 6.1 states the instantiated separation: there is no generic
reduction from $q$-SDH to a true fixed-size assumption in this fully black-box
model.  [Lu–Zhandry 2024, Cor. 6.1]

[CITED] The proof does not establish an unrestricted standard-model separation;
representation-dependent and non-black-box-in-the-adversary reductions remain
outside the theorem.  [Lu–Zhandry 2024, §§1.3–1.4]
