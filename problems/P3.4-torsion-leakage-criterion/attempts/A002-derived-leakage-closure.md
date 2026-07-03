---
attempt: A002
status: dead
---
# A002 — Compute target-map leakage closure mechanically

## Idea

Represent disclosed source points by coordinate columns in
$(\mathbb Z/N\mathbb Z)^2$, group records by a stable target-map identifier,
and decide whether their span is the full module. Only then derive the action
matrix from the disclosed image columns.

## Prior art

[CITED] The attack templates consume the action on a torsion basis but permit
any equivalent encoding from which that action can be derived
(Castryck--Decru 2023, Eq. (2); Robert 2023, Theorem 1.1 and Lemma 2.2).

## Plan

1. Prove a composite-modulus span criterion using $2\times2$ minors.
2. Implement the criterion and action reconstruction.
3. Reject aggregation across different target-map identifiers.
4. Add mixed-order CRT aggregation prime by prime.
5. Use the derived result as classifier input.

## Execution log

Session 2 initialized after all baseline tests passed.

- Proved the gcd-of-minors criterion constructively by building a right inverse
  from embedded adjugates and Bezout coefficients.
- Implemented `code/leakage_closure.py` and six record-level fixtures.
- Added generalized CRT with overlap checks and stable map/basis identifiers.
- Verified nine P3.4 test methods, including all prior classifier tests.

## Outcome

SG-08 is complete, and the numerical portion of SG-09 is implemented. The
attempt was closed as a failure before SG-10 and SG-11.

## Post-mortem

**Why it failed:** [PROVED] Mechanically deriving a leaked torsion action and
checking auxiliary degree identities removes profile ambiguity, but it does
not establish that the encoded published templates exhaust all possible
higher-dimensional attacks. It therefore cannot close Q011 or satisfy the
unrestricted necessary-and-sufficient statement.

**What transfers:** [PROVED] The gcd-of-minors span certificate, verified action
reconstruction, compatible-basis CRT check, and CD/MM numerical-certificate
checker are independently reusable components.

**Would it work under different assumptions?** [PROVED] Yes: for a fixed named
target map, fixed compatible torsion bases, and the two encoded K2 numerical
relations, the implemented checks decide exactly the finite algebraic
conditions they encode. They still require a separate auxiliary-isogeny
construction witness.
