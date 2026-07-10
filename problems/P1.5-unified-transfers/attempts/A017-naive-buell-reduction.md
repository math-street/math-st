---
attempt: A017
status: dead
---
# A017 - Apply the Buell point-to-form formula to finite-field coordinate lifts

## Idea

- [CONJECTURE] The explicit number-field formula behind the Buell--Call class
  pairing might accept canonical integer representatives of
  $Q\in E(\mathbb F_p)$ and output a quadratic form in one fixed imaginary
  quadratic class group, avoiding a global torsion-point lift.

## Formula and prediction

- [CITED] For the integral model
  $$y^2=4x(x^2+Bx+C)+\mathcal D,$$
  the integral-point specialization of the Buell formula assigns
  $$Q=(a,b)\longmapsto
  [aX^2+bXY+(a^2+Ba+C)Y^2],$$
  whose discriminant is $b^2-4a(a^2+Ba+C)=\mathcal D$ when $Q$ is an actual
  integral point (Buell--Call 2016, Equation (1) and its cited Buell sources).
- [CONJECTURE] For canonical representatives of a point only satisfying the
  curve equation modulo $p$, the displayed discriminant will equal
  $\mathcal D+k_Qp$ with a point-dependent nonzero $k_Q$ on almost all points.
  The outputs will therefore live in different quadratic orders and cannot be
  elements of one target group.

## Positive and negative criteria

- [PROVED] A positive outcome requires one fixed discriminant on all $r$
  source points, followed by a reduced-form class computation that passes the
  full subgroup homomorphism law.
- [PROVED] A negative outcome is complete subgroup enumeration finding two
  different lifted discriminants; this refutes the canonical-representative
  formula, though not a more sophisticated global lift.

## Plan

1. Enumerate toy reductions of fixed integral models and find prime-order
   subgroups.
2. Evaluate the lifted discriminant on every nonzero subgroup point.
3. Record the number of distinct discriminants, the number equal to the model
   discriminant, and divisibility of every discrepancy by $p$.

## Execution log

- [EMPIRICAL: 10 nonsingular reductions, 23 <= p <= 59, 13 <= r <= 37,
  218 nonzero subgroup points] `code/probe_buell_reduction.py` found 218
  distinct lifted discriminants - one per tested point - and only two points
  whose lifted discriminant equalled the fixed model discriminant.  Every
  discrepancy was divisible by $p$; see
  `data/probe_buell_reduction_full_20260710.csv`.
- [EMPIRICAL: same 218 points] Only 195 lifted discriminants were negative and
  only 199 coefficient triples were primitive, so even before comparing
  classes, some outputs failed the basic imaginary-order or primitive-form
  requirements.
- [EMPIRICAL: validation on 2026-07-10] The order-29 curve at
  $(B,C,\mathcal D,p)=(0,1,-7,23)$ was exhaustively point-counted, all ten
  subgroup laws closed, three dedicated tests passed, and the full P1.5 suite
  increased to ten passing tests.

## Proof of the interface failure

- [PROVED] For canonical representatives $0\le a,b<p$, the finite-field curve
  equation gives only
  $$b^2-4a(a^2+Ba+C)\equiv\mathcal D\pmod p.$$
  Thus the displayed quadratic form has discriminant
  $\mathcal D_Q=\mathcal D+k_Qp$, not discriminant $\mathcal D$ unless
  $k_Q=0$.
- [PROVED] Binary quadratic forms with different discriminants represent ideal
  classes of different orders; there is no group law that makes these outputs
  elements of one fixed target class group.
- [PROVED] Choosing noncanonical integer or rational lifts to force
  $\mathcal D_Q=\mathcal D$ means solving the original integral/number-field
  curve equation exactly.  To preserve the subgroup law, those choices must
  be globally coherent, returning to the arithmetic lift branch A006 rather
  than defining a direct residue-coordinate formula.

## Outcome

- [PROVED] The canonical-coordinate specialization of the explicit Buell
  point-to-form formula does not define a finite-field transfer: it does not
  even land in one class group.

## Post-mortem

**Why it failed:** [PROVED] Reduction modulo $p$ preserves the form
discriminant only modulo $p$, whereas ideal-class composition requires one
fixed integral discriminant.

**What transfers:** [PROVED] Any cross-characteristic point-to-form proposal
must specify a coherent exact lift of the discriminant, not merely integer
representatives of residue coordinates.

**Would it work under different assumptions?** [CITED] The formula works for
actual rational or number-field points on the integral curve, which is the
Buell--Call setting.  A polynomial-size coherent lift of the finite-field
subgroup would revive the idea but is precisely the surviving A001/A006 gap.

