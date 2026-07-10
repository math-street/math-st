---
attempt: A018
status: folded-into-A001
---
# A018 - Audit direct finite-field point-to-number-field class maps

## Question and search boundary

- [PROVED] SG-24 asks only for a direct evaluator from a finite-field elliptic
  point to a class in one fixed number-field order; ideal actions in the
  reverse direction, function-field Jacobians, and maps whose source point is
  rational over a number field are different branches.
- [EMPIRICAL: bounded literature search on 2026-07-10] Searches combined
  `finite field`, `elliptic curve points`, `class group`, `homomorphism`,
  `ideal class pairing`, `Buell`, and `Soleng` across arXiv, AMS, journal
  metadata, references of Buell--Call (2016), and Gillibert (2018).

## Checked positive constructions

- [CITED] Buell (1977) constructs a point-to-class map for rational points on
  an elliptic curve over \(\mathbb Q\) and a quadratic number field; the
  domain is characteristic zero.
- [CITED] Soleng (1994) constructs homomorphisms from rational elliptic-curve
  points to class groups of quadratic number fields; Gillibert (2018)
  identifies them with line-bundle specialization/class pairings.
- [CITED] Buell--Call (2016) treats elliptic curves over number fields and
  relates the class pairing to Weil descent after fixing a torsion argument.
- [CITED] Gillibert (2018) specializes line bundles on curves over
  \(\mathbb Q\) at algebraic points into class groups of their number fields.
- [CITED] Blum--Choi--Hoey--Iskander--Lakein--Martinez (2022) give explicit
  maps \(\Phi_{u,v}:E(\mathbb Q)\to\operatorname{Cl}(-D_E(u,v))\).
- [CITED] The checked finite-field CM literature instead uses ideal classes
  acting on oriented elliptic curves; this is the opposite
  ideal-to-curve direction recorded in A003.

## Outcome

- [EMPIRICAL: bounded literature search on 2026-07-10] No checked source in
  the stated boundary supplied a direct homomorphism
  \(E(\mathbb F_q)[r]\to\operatorname{Cl}(\mathcal O)\) for one fixed
  number-field order \(\mathcal O\).
- [PROVED] This search result is not a nonexistence theorem and therefore does
  not close Q004 by itself.
- [PROVED] All checked positive point-to-class constructions require
  characteristic-zero rational/algebraic points or global arithmetic models;
  applying their coordinate formulas to residue representatives is exactly
  the interface failure tested in A017.
- [PROVED] The surviving A001 object is consequently stated without an
  unsearched synonym: a uniform cross-characteristic algorithm taking an
  ordinary representation of \(Q\in E(\mathbb F_q)[r]\) directly to a class
  in one separately constructed number-field order, with no coherent global
  lift supplied as advice.

## What transfers

- [PROVED] Any future literature lead must be checked first for the direction
  of the map, the characteristic of the source point, whether the target order
  is fixed across all source points, and whether setup encodes a dense lift or
  a table.
