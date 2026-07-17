---
attempt: A007
status: promising
---
# A007 — Formal support-size obstruction

## Idea

[PROVED] Count the image of the sum map $\mathcal F^m\to E(\mathbb F_p)$
before attempting any further structured factor base. The count is independent
of how membership or decomposition is implemented.

## Prior art

[CITED] Lenstra 2017 supplies the standard generalized L-notation used by the
formal size bound, and Sutherland 2025 supplies Hasse's point-count bound.
The remaining support argument is elementary and is proved in `CLAIM.md`.

## Plan and execution

- [PROVED] Upper-bound exact and variable-length reachable sets.
- [PROVED] Check random, nonuniform, signed, repeated, and unordered variants.
- [EMPIRICAL: cyclic group of order 19] Exhaustively test the bound at toy
  scale.
- [PROVED] Derive the minimum factor-base size for fixed $m$ and the minimum
  growth of $m$ for an $L_p[1/2,c]$ base.

## Outcome

[PROVED] Under standard L-notation and fixed $m$, conditions (1) and (3) are
mutually inconsistent. The complete proof and its notation caveat are in
`CLAIM.md`.

## Post-mortem

**Why the requested construction fails:** [PROVED] A fixed number of summands
from a subexponential base has only $p^{o(1)}$ candidate tuples but the curve
group has $p^{1+o(1)}$ targets.

**What transfers:** [PROVED] The same obstruction holds in any finite group of
order $p^{1+o(1)}$ and does not depend on elliptic-curve geometry.

**Would it work under different assumptions?** [CONDITIONAL: corrected
statement] Counting no longer rules out a base of size $p^{1/m-o(1)}$ or a
summand count growing at least on the order derived in `CLAIM.md`; efficient
findability would still need a separate proof.
