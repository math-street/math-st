---
attempt: A004
status: complete
---
# A004 — Registry archaeology and class-uniform toy kernel

## Questions

1. Do crates.io or docs.rs preserve a BLS12-381 design artifact that predates
   the surviving version-0.9.0 Git root?
2. How does A002's uniform distribution on safe coefficient encodings project
   onto \(\mathbb F_p\)-isomorphism classes, and can a forced toy kernel sample
   those classes uniformly?

## Archival success criterion

A numerical historical \(b\) still requires a dated finite candidate domain,
selection/order rule, equivalence convention, and evidence that they were
fixed before selection. Earlier constants or implementation code alone improve
the source trace but do not meet this criterion.

## Computational success criterion

At the fixed smoke prime \(p=127\), enumerate all nonsingular coefficient
pairs, quotient them by explicit short-Weierstrass
\(\mathbb F_p\)-isomorphism, filter by the existing safety profile, and:

- report the exact encoding and class counts;
- verify every class key against explicit scaling orbits;
- prove the induced mass under the coefficient kernel;
- implement exact uniform unranking over canonical safe-class
  representatives; and
- test deterministic replay and first/last rank boundaries.

No production-size parameter search is permitted.

## Prediction

Pre-0.9 package snapshots will improve dating but not recover a complete
historical menu. Safe coefficient classes will have unequal numbers of
encodings because special automorphism classes have smaller scaling orbits,
so coefficient-uniform and class-uniform kernels will differ.

## Registry result

- **[CITED]** The crates.io version record for `pairing` begins at 0.9.0,
  created July 8, 2017 at 17:16:29 UTC. No 0.8.x or earlier registry version
  exists; docs.rs likewise lists 0.9.0 as the earliest version.
- **[CITED]** The 0.9.0 registry date matches the surviving Git root date and
  does not predate the March announcement.
- **[PROVED]** This falsifies the archival prediction's first clause. There is
  no omitted pre-0.9 registry channel to search, and the registry supplies no
  pre-publication menu evidence.

## Class-kernel proof

**[PROVED]** In characteristic greater than three, short-Weierstrass
\(\mathbb F_p\)-isomorphism classes are exactly the orbits of
\((a,b)\mapsto(u^4a,u^6b)\) for \(u\in\mathbb F_p^*\). The existing safety
profile is constant on these orbits because it depends on isomorphism-invariant
curve/twist orders and quantities derived from them.

**[PROVED]** Conditional on safety, A002 assigns an orbit \(O\) mass
\(|O|/\sum_{O'}|O'|\). A class-uniform reference kernel instead exactly
unranks the sorted canonical representatives and assigns each mass
\(1/|\{O\}|\).

**[PROVED]** Uniform distribution uniquely minimizes maximum singleton mass on
a fixed finite class universe. The class-uniform kernel is therefore minimax
for singleton class weaknesses, while retaining \(b=0\) under one forced
future beacon.

## Exact toy result

- **[EMPIRICAL: exhaustive \(0\leq a,b<127\), all \(1\leq u<127\)]**
  16,002 nonsingular encodings form 258 classes; orbit sizes are 21 for six
  classes and 63 for 252 classes.
- **[EMPIRICAL: the fixed A002 safety profile at \(p=127\)]** 4,179 safe
  encodings form 67 safe classes; one has orbit size 21 and 66 have size 63.
- **[PROVED]** Given those exhaustive counts, A002's exceptional-class mass is
  \(21/4179=1/199\), each generic-class mass is \(63/4179=3/199\), the
  class-uniform mass is \(1/67\), and total variation distance is
  \(132/13333\).
- **[EMPIRICAL: six SG-10 regression tests]** Every recorded orbit agrees
  with explicit scaling, the exact counts and rational masses match, boundary
  ranks and subgroup points validate, replay/domain separation pass, and the
  fixed smoke CLI uses the \(p=31\) quick profile.

## Artifacts

- `code/class_uniform_kernel.py`
- `code/tests/test_class_uniform_kernel.py`
- `data/class_kernel_b7_20260708.json`
- `data/class_kernel_b7_20260708.csv`

## Outcome

Both success criteria are met. The registry route is exhausted with a dated
negative result, and the toy reference construction now distinguishes and
implements coefficient-uniform and class-uniform projections exactly. No
production-size computation was performed.
