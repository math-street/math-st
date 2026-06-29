# Review — P1.1 lower bounds beyond the generic group model

## Outcome status

**FAILED.** The formal free-coordinate model refutation is retained, as are
the passing toy fixtures, but this work does not satisfy the requested full
endpoint. The only executable GHS transfer is the degenerate genus-one case in
A004; no genuinely higher-genus Jacobian transfer or meaningful attack-cost
comparison was completed.

## Scoped disposition

The requested pure cost model has been exhausted in direction (b), for the
formal model class defined in this folder.

[PROVED] In both the literal free-coordinate machine $\mathsf{CCA}_0$ and the
read-only machine $\mathsf{ROCCA}_0$, ECDLP has zero charged group-oracle query
complexity. The proofs are [MODEL.md](MODEL.md) and
[READ_ONLY_MODEL.md](READ_ONLY_MODEL.md).

[PROVED] The conclusion extends to every explicit canonical representation for
which the representation-level group law and equality are operations in the
free language: exhaustive virtual iteration solves DLP without calling the
separately charged oracle.

[PROVED] Consequently, a nonzero lower bound that counts only a named group
oracle cannot coexist with free, unrestricted coordinate programs that can
evaluate and compose the same group law.

This is a scoped model refutation, not a claim that the broader open problem of
lower bounds for restricted coordinate computation has been solved.

## Deliverable check

- [NOTES.md](NOTES.md) contains the attack-by-primitive matrix, a justification
  for every nontrivial cell, Shoup's proof in repository notation, and the
  candidate-model comparison.
- [MODEL.md](MODEL.md) gives syntax and semantics for the literal model and an
  explicit zero-charge BSGS and summation-polynomial compiler.
- [READ_ONLY_MODEL.md](READ_ONLY_MODEL.md) gives typed read-only semantics, the
  point-handle invariant, the zero-query theorem, and the general no-go result.
- [attempts/A001-coordinate-oracle-bypass.md](attempts/A001-coordinate-oracle-bypass.md)
  and [attempts/A002-read-only-coordinates.md](attempts/A002-read-only-coordinates.md)
  preserve the two failed lower-bound candidates and their post-mortems.
- [attempts/A004-genus-one-ghs-transfer.md](attempts/A004-genus-one-ghs-transfer.md)
  records the exact specialization that closes the remaining executable GHS
  transfer gap without claiming a higher-genus speedup.
- This file records the final audit and limitations.

## Why Shoup's proof does not transfer

[CITED] Shoup's 1997 generic lower bound represents each visible group element
by an opaque random encoding and lets the simulator assign a fresh label to
each newly formed affine-linear expression in the hidden logarithm.

[PROVED] Coordinate projection breaks that coupling before a group-element
collision: a free coordinate program can inspect algebraic relations among the
input representations and can directly evaluate the curve law.

[PROVED] Forbidding `PACK` repairs neither fact. A solver can store all derived
points as field tuples, iterate affine formulas, compare the tuples with the
target coordinates, and output the matching scalar.

## Attack expressibility

[PROVED] BSGS, Pollard rho, and Pohlig–Hellman compile point state into virtual
coordinate tuples and therefore require zero charged oracle calls in either
formal model.

[PROVED] SSSA/Smart computations can represent lifted points by coordinate
tuples over the lifted ring and evaluate the formal parameter without base
point handles.

[PROVED] MOV/Frey–Rück computations can represent extension-field points and
Miller functions as ordinary field data, after which the auxiliary
multiplicative DLP is outside the charged elliptic-curve oracle.

[PROVED] GHS equations, divisor representations, and target class-group data
can likewise be ordinary polynomial data; the read-only restriction on input
elliptic-curve handles does not constrain them.

[PROVED] Semaev/Gaudry/Diem relation collection uses coordinate polynomials,
factor-base tests, system solving, and relation data already admitted by the
free language.

## Executable audit

| Row | Fixed toy evidence | Result |
|---|---|---|
| Generic algorithms | [EMPIRICAL: p=17, order 19; p=7, order 12] Shared tests cover BSGS, rho, and the $2^2\cdot3$ Pohlig–Hellman decomposition. | Passed. |
| Coordinate compiler | [EMPIRICAL: p=17, order 19] The same BSGS instance records 17 charged operations through the oracle spelling and zero through the coordinate spelling. | Passed. |
| SSSA / Smart | [EMPIRICAL: p=17, anomalous order 17] The fixed trace recovers secret 7 after two lifts modulo $p^2$. | Passed. |
| MOV / Frey–Rück | [EMPIRICAL: p=43, subgroup order 11] The reduced Tate values match the fixed vector and preserve secret 2 in $\mathbb F_{43^2}^{*}$. | Passed. |
| Prime-field decomposition | [EMPIRICAL: p=17] Twenty-five $f_3$ evaluations yield two polynomial zero pairs and two verified ordered decompositions. | Passed. |
| Extension-field decomposition | [EMPIRICAL: q=5, n=3] Twenty-five $f_3$ evaluations over a subfield factor base yield one verified ordered decomposition after three-coordinate basis expansion. | Passed. |
| GHS | [EMPIRICAL: $\mathbb F_{2^{10}}/\mathbb F_{2^2}$, order-three subgroup] The source coefficient and generator are genuinely outside the base field; the five-conjugate genus-one conorm/norm map preserves every subgroup scalar and target DLP recovers secret 2. Independent fixtures also verify higher-genus invariants. | Passed for an exact genus-one specialization. |

[PROVED] For the odd-degree magic-number-one specialization, the descended
Jacobian is the auxiliary elliptic curve and the published conorm/norm reduces
to the implemented sum of Frobenius conjugates. A003 preserves why the earlier
structural fixture was insufficient; A004 supplies the missing map and DLP.
This does not implement a genuinely higher-genus Jacobian or demonstrate an
asymptotic attack advantage.

## What would constitute a different model

[PROVED] Charging field operations removes the free compiler but changes the
cost measure from group operations to joint field/group computation.

[PROVED] Bounding total coordinate-circuit size or algebraic degree can remove
the exhaustive virtual-point program, but it no longer grants unrestricted
free coordinate manipulation.

[PROVED] Charging every extensional evaluation of the elliptic-curve addition
map can preserve a group-law cost, but the model must define how algebraically
equivalent, batched, or partially evaluated formulas are recognized.

No lower bound is asserted for any of those repaired models.

## Reproducibility

[EMPIRICAL: 2026-06-29 local run] The six P1.1 known-answer observation tests
and all 63 shared library tests pass. The recorded CSV files are under
[data](data), and the commands are documented in [code/README.md](code/README.md).

## Final boundary

[PROVED] The literal target “general coordinate arithmetic is free, only group
operations are counted” is vacuous as a group-operation security argument.

[PROVED] The exact killer primitive is closure of the free coordinate language
under iterated evaluation of the representation-level group law; free
coordinate-to-point reification is sufficient but unnecessary.

The GHS row remains incomplete for the full validation target. Its genus-one
evidence is exact but does not exercise higher-genus divisor arithmetic or the
class-group attack that makes GHS non-generic. Consequently, the overall task
is marked failed rather than complete.
