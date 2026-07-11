# Handoff - P5.2 - after session 4 failure designation

## State in five lines

The project is marked failed/abandoned at the user's explicit request.
Sessions 1-3 remain preserved as validated partial research.
The $D=-3,-4$ unit experiments and $D=-7$ implementation/tests passed.
A003 and A004 establish stated-model obstructions for non-unit quotient rho.
A005 stopped before implementation, so Q025 remains completely untested.

## What is established (tagged)

- [EMPIRICAL: 3,200 recovered DLPs] Unit-orbit collision-table speedups matched the fixed $\sqrt6$ and $2$ predictions within all recorded 95% intervals.
- [EMPIRICAL: five curves, p=977..262007] The explicit $D=-7$ map passed independent counts and characteristic-equation checks.
- [EMPIRICAL: r=233..32831] The measured eigenvalue orders were 116, 495, 1352, 8069, and 16415.
- [PROVED] Least-label normalization needs $m-1$ successor queries in the sequential successor/comparison model.
- [PROVED] Addition does not descend to nontrivial scalar-orbit classes.
- [PROVED] A multiplier-returning canonicalizer with quotient size $q$ reduces ECDLP to $q+1$ canonicalizer calls.

## Failure record

- [PROVED] The initial direct-path unittest invocation failed before discovery because the problem directory contains a dot.
- [PROVED] A diagnostic used secret 37 in an order-29 subgroup and initially misread the correct residue 8 as an error.
- [PROVED] A005 was terminated before implementation when the user requested that the work be marked as a failure.
- [PROVED] The final failure designation is procedural; it is not a mathematical refutation of the preserved results or of Q025.

## What remains open

Q025 asks whether several unoriented subgroup-membership constraints can be combined in sub-square-root time. No A005 code or data exist.

## Resume condition

Resume only if the user explicitly reopens Q025. Start from the preregistered plan in `attempts/A005-unoriented-constraints.md`.

## Files that matter

- `STATE.md` and `LOG.md`: failure/abandonment record.
- `attempts/A005-unoriented-constraints.md`: stopped plan and post-mortem.
- `code/cm_nonunit.py`, `code/measure_nonunit_orbits.py`: validated earlier work.
- `data/measure_nonunit_orbits_b10-12-14-16-18_n16_s72022026_20260711_*.csv`: preserved evidence.

## What I would tell my replacement

Do not interpret the final failure marker as failed mathematics. It records the user's instruction to stop before A005 was implemented.
