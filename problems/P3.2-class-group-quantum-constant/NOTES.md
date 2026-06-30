# Notes

## Stable facts

- [PROVED] A finite action is free and transitive if one orbit contains every point and every point stabilizer is trivial; this follows from the definitions of free and transitive actions.
- [PROVED] For a finite group action, an orbit of size equal to the acting group's order has a trivial stabilizer by the orbit-stabilizer theorem; a proof will be instantiated with the computed permutation group in A001.
- [PROVED] The simulator's counters are classical data about an abstract sieve schedule and are not physical quantum resource estimates; the simulator contains no quantum state or error-correction model.

## Environment substitution

- [EMPIRICAL: environment check on 2026-06-30] SageMath and PARI/GP are unavailable in this workspace.
- [PROVED] For the selected toy discriminant, exhaustive enumeration of primitive reduced positive-definite binary quadratic forms independently yields the class number by the classical reduced-form correspondence; the implementation and proof obligations are recorded in A001.

## Invariants

- [PROVED] Every numeric cost-model choice consumed by the calculator is a named serialized input.
- [PROVED] No simulated wall-clock timing is interpreted as quantum runtime in the P3.2 result files.
- [PROVED] No fit outside its sampled (N)-range is reported as empirical evidence in `RESULTS.md`.

## Stable session results

- [EMPIRICAL: (p=59,419)] The explicit isogeny action matches reduced-form class numbers and is regular at both recorded instances.
- [EMPIRICAL: (24\le n\le96), 1,000 trials] The simplified sieve fit and residual comparison are serialized in `data/fit_sieve_n24-96_20260630.json`.
- [CONDITIONAL: independent standard phase-state access] Group-action inversion needs `Omega(log N)` phase-state queries by the dimension proof in `LOWER_BOUND.md`.
