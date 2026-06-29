# P3.1 — Unconditional endomorphism-ring equivalence

## Setting

- [CITED] Supersingular elliptic curves over $\mathbb F_{p^2}$ have endomorphism algebras isomorphic to the quaternion algebra $B_{p,\infty}$ ramified exactly at $p$ and $\infty$ (Deuring 1941).
- **Problem A:** given supersingular $E_1,E_2/\mathbb F_{p^2}$, find an isogeny $E_1\to E_2$ of smooth degree.
- **Problem B:** given supersingular $E/\mathbb F_{p^2}$, compute $\operatorname{End}(E)$ as an explicit maximal order.

## Targets

1. Prove that Problems A and B are equivalent without assuming GRH.
2. Separately quantify the concrete security loss of the reductions as a function of $p$.

## First deliverable

Produce a GRH usage map for the existing equivalence proof: identify every GRH-dependent lemma, the exact effective bound it needs, and the strongest relevant unconditional substitute. Mark reconstructed entries `[UNVERIFIED]` when the source text cannot be checked.

## Success conditions

- Task 1 succeeds only with an unconditional equivalence proof or a precise necessity result for GRH.
- Task 2 succeeds only with an experimentally validated concrete loss function.
- A source-checked GRH usage map is a useful partial result, not a solution to Task 1.
