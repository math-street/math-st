# Handoff - P1.5 - after session 6

## State in five lines

SG-01--SG-29 and SG-31--SG-32 are complete at their stated scopes.
P1.5/Q004 is still open; do not call the unrestricted problem solved.
The A008--A013 rational package survived audit; use
RATIONAL_TRANSFER_REVIEW.md as the authoritative statement.
Its affine piecewise bound is \(D_+B^2\ge r/4\), not the older \(B^3\) bound.
A023 records that this quadratic-overlap mechanism has direct scalar
interpolation prior art; call the package a repository-original synthesis.
A024 gives one exact VFB evaluator model a transcript lower bound, but leaves
direct coordinate-to-form and polynomial-length VFB programs open.
SG-30 remains the separate, untouched target-construction task.

## What is established (tagged)

- [CITED] Anomalous, pairing, and qualifying Weil-descent transfers are known
  local, bilinear, and geometric mechanisms.
- [PROVED] Generic-source transfers contradict Shoup; affine rational
  evaluators satisfy the strengthened exact overlap, \(B^2\), and
  rational-decision-tree depth lower bounds; proper or
  low-defect mixed rational targets collapse to global elliptic-isogenous maps.
- [CITED] Coppersmith--Shparlinski already prove the scalar
  arbitrary-subset quadratic-overlap mechanism; the checked interpolation
  papers neither state the faithful affine-target theorem nor improve the
  adversarial \(B^2\) exponent.
- [PROVED] In A024's fixed VFB model, every nonzero evaluator obeys
  \(C+\sum_j\log_2(h_j+1)\ge\log_2r\). Polynomial-height operands and
  sublinear comparison count therefore require
  \(\Omega(\log r/\log\log r)\) valuations.
- [PROVED] Finite/local Picard targets are trivial. Pointed global
  function-field class groups are Jacobians or generalized Jacobians.
- [PROVED] Number fields are the only genuinely distinct class-target base.
- [PROVED] For a nonzero homomorphism, evaluation and source DLP are
  polynomial-time equivalent given a target-DLP oracle.
- [PROVED] Under the checked Hafner--McCurley route, discriminant bits obey
  $2n-O(\log n)\le B=o(n^2/\log n)$ for $n=\lceil\log_2r\rceil$.
- [CITED] Checked Buell--Soleng and later point-to-class maps use rational or
  algebraic points over number fields, not finite-field source points.
- [EMPIRICAL: bounded primary-source search, 2026-07-10] No checked direct
  $E(\mathbb F_q)[r]$-to-fixed-number-field-class evaluator was found.
- [PROVED] Direct canonical residue substitution in the Buell form has
  point-dependent discriminant $\mathcal D+k_Qp$ and no fixed target.
- [EMPIRICAL: 10 reductions, 218 nonzero points] All lifted Buell
  discriminants were distinct; only two equalled the model discriminant.
- [PROVED] Discriminant $1-4\cdot2^r$ has an explicit exact order-$r$ class,
  but its $\Theta(r)$-bit encoding violates SG-01.
- [EMPIRICAL: exhaustive $|\Delta|\le200000$, primes $3\le r\le43$] Every
  least qualifying toy discriminant had $h(\Delta)=r$ and
  $0.684711\le|\Delta|/r^2\le2.555556$.
- [EMPIRICAL: bounded prescribed-order search, 2026-07-10] No checked theorem
  gave a uniform polynomial-bit exact-order constructor as $r$ grows.
- [PROVED] A modulus-$r^2$ Gaussian principal-unit evaluator reveals the
  source scalar through $1+rz\mapsto z$; ray evaluation and ECDLP are
  polynomial-time equivalent.
- [EMPIRICAL: final verification 2026-07-20] 70 shared and 16 P1.5 tests and
  bytecode compilation pass. The A023/A024 control-character,
  trailing-whitespace, and unresolved-marker audits also pass; the four
  legacy smoke runs and finite-overlap certificate remain covered by the
  preceding session.

## What is ruled out

- A003--A006: natural CM labels, standard ray action, local class pairing,
  and dense global torsion lifts.
- A007--A013: generic, low-degree/shallow/piecewise rational, proper, and
  controlled mixed algebraic evaluators, under the exact models in
  RATIONAL_TRANSFER_REVIEW.md.
- A017: canonical finite-field use of the Buell formula.
- A019: self-certifying exact-order target with exponential input length.
- A022: ray principal units as an intermediate subexponential target.

## Active threads

A001 remains the ordinary number-field point-to-class character.
A002 remains a viable but known cover/Jacobian/Weil-descent framework.
SG-30 asks for a uniform succinct prescribed-order ordinary target.
A024 closes SG-32 only for the VFB model. Direct MAKEFORM-style use of raw
coordinates and polynomial-length VFB programs remain evaluator residuals.

## Next action

If evaluator work continues, specify the direct raw-coordinate-to-form
extension excluded by A024 and find an invariant that either proves
homomorphy/nonzeroness or yields a lower bound. Keep SG-30 separate; do not
smuggle target construction into the evaluator model.

## Invariants - do not violate

- Full input/setup length is $(\log r)^{O(1)}$.
- An abstract map $xP\mapsto h^x$ is circular without an evaluator.
- Target size or class-number divisibility does not construct the evaluator.
- Finite censuses are empirical and do not define a uniform family.
- A bounded literature search is not a nonexistence theorem.
- Ray evaluation would already be a polynomial-time source-DLP algorithm.
- Q004 closes only by the explicit criteria in `OPEN_QUESTIONS.md`.

## Files that matter

- `NOTES.md`: stable facts through SG-32.
- `attempts/A001-class-group-character.md`: active synthesis and falsifier.
- `attempts/A015-evaluator-sandwich.md`: evaluator/source/target reductions.
- `attempts/A017-naive-buell-reduction.md`: fixed-discriminant failure.
- `attempts/A019-oversized-exact-order-class.md`: exact order proof.
- `attempts/A020-succinct-target-census.md`: toy target census.
- `attempts/A021-succinct-exact-order-audit.md`: construction literature.
- `attempts/A022-ray-evaluator-equivalence.md`: transparent ray log proof.
- `attempts/A023-interpolation-prior-art-audit.md`: five-item reconciliation.
- `attempts/A024-valuation-factor-base-model.md`: fixed VFB model and bound.
- `code/probe_buell_reduction.py`: validated 218-point experiment.
- `code/probe_exact_order_targets.py`: validated full discriminant census.

## What I would tell my replacement

Do not conflate four facts: small targets exist at toy scale, uniform target
construction is not known here, the point evaluator is an independent ECDLP
reduction, and A024 excludes only low-observation VFB recipes. The central
unanswered object is still a concrete finite-field coordinate program
producing ordinary number-field ideal classes while respecting point
addition.
