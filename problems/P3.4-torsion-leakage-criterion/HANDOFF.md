# Handoff -- P3.4 -- failure closure after session 2

## State in five lines

[PROVED] The project is abandoned and recorded as failure at the user's request.
[PROVED] The universal necessary-and-sufficient leakage criterion was not proved.
[PROVED] A scoped R8/K2-CD/K2-MM invocation checklist remains as a partial artifact.
[PROVED] Coordinate-level leakage closure and numerical K2 checks were implemented.
[PROVED] A001 and A002 are dead; Q011 is the mathematical obstruction.

## What is established (tagged)

- [CITED] Full rank-two smooth torsion action can trigger Robert's
  dimension-8 recovery route under its degree, access, and recovery hypotheses
  (Robert 2023).
- [CITED] K2 surface routes need protocol-specific auxiliary construction
  witnesses in addition to degree identities (Castryck--Decru 2023;
  Maino--Martindale 2023).
- [PROVED] Source records in $(\mathbb Z/N\mathbb Z)^2$ span the full module
  exactly when $N$ and all $2\times2$ source minors have gcd one; Section 8 of
  `CHECKLIST.md` contains the proof.
- [PROVED] Same-map action matrices combine across orders only with compatible
  bases and generalized-CRT agreement on the overlap.
- [EMPIRICAL: 15 P3.4 test methods] Classifier, closure, and surface-certificate
  tests pass; 61 shared tests also pass.

## What is ruled out

- A001 is dead: finite published-template normalization cannot prove universal
  necessity against unenumerated higher-dimensional attacks.
- A002 is dead: mechanizing leakage closure and integer certificates does not
  close the same template-completeness gap.
- [PROVED] A valid numerical K2 identity does not prove that an auxiliary
  isogeny exists or is efficiently evaluable.

## Active thread

None. The problem is abandoned.

## Next action

None unless explicitly reopened. A reopening should address Q011 before adding
more classifier fields.

## Invariants -- do not violate

- `NO_PUBLISHED_ROUTE` is not a security proof.
- Do not mix records from different target maps or incompatible torsion bases.
- Keep numerical K2 validity separate from construction/evaluation evidence.
- Do not describe the partial checklist as a universal necessary condition.

## Files that matter

- `CHECKLIST.md`: partial scoped result and failure banner.
- `attempts/A001-known-attack-checklist.md`: first failure post-mortem.
- `attempts/A002-derived-leakage-closure.md`: second failure post-mortem.
- `code/leakage_checklist.py`: scoped classifier.
- `code/leakage_closure.py`: coordinate-level action derivation.
- `code/surface_certificates.py`: numerical K2 checks only.
- `OPEN_QUESTIONS.md` Q011: missing universal-completeness theorem.

## What I would tell my replacement

[PROVED] The partial implementation is not the failed part; the failure is the
unclosed quantifier over all Kani embeddings and higher-dimensional recovery
routes. More fixtures cannot resolve that logical gap.
