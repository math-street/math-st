---
attempt: A001
status: dead
---
# A001 — Embed a constant-size DDH/SXDH challenge into $q$-SDH

## Idea

[PROVED] Use one source-group DDH challenge, hence one component of an SXDH
challenge, to synthesize the correlated source power ladder required by a
$q$-SDH adversary and use its answer to decide DDH.

## Reduction class tested

[PROVED] The attempted reduction is straight-line, type preserving, and
algebraic: it combines challenge elements with group operations and known
scalar exponentiation, invokes one $q$-SDH adversary, and has no source-group
encoding of a target-group pairing result.

## Execution

[PROVED] Write the source challenge exponents as $(1,a,b,z)$, with $z=ab$ in
the real branch and independent $z$ in the random branch.  Before the oracle
call, every source element created by this reduction has exponent in
$L=\operatorname{span}\{1,a,b,z\}$.

[PROVED] A valid nonconstant ladder prefix requires $x,x^2\in L$.  In the
random branch, put $x=A+Ba+Cb+Dz$.  Since $a,b,z$ are algebraically
independent, the identity $x^2\in L$ forces the coefficients of
$a^2,b^2,z^2,ab,az,bz$ to vanish; over an odd prime field this gives
$B=C=D=0$.

[PROVED] The only possible $x$ is therefore a known constant, statistically
independent of the DDH challenge bit.  Such an oracle query cannot transfer a
nonzero DDH distinguishing advantage.

[PROVED] Pairing does not repair the embedding: it produces degree-two
exponents in $\mathbb G_T$, while $q$-SDH requires the missing powers in
$\mathbb G_1$, and the typed interface contains no map back to a source group.

## Outcome

[PROVED] The direct embedding is dead already at $x^2$ for the stated
straight-line algebraic class.

[PROVED] This is not a proof against rewinding, multiple adaptive adversary calls,
or representation-dependent computation.

## Post-mortem

[CITED] Lu and Zhandry's meta-reduction turns this fixed-dimensional-span
failure into a separation for the substantially broader fully black-box
generic-representation class; see A002.  [Lu–Zhandry 2024, Thms. 5.2, 5.10]
