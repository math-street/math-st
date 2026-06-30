# Handoff — P3.2 — after session 1

**Overall outcome: FAILED.**

## State in five lines

- [PROVED] The formal problem is marked abandoned because neither requested formal result was achieved.
- [EMPIRICAL: (p=59,419)] Explicit rational Vélu actions are regular and match reduced-form class numbers 9 and 27.
- [EMPIRICAL: (24\le n\le96)] A simplified fixed-batch sieve has 1,000 stored trials and a three-term natural-log fit.
- [PROVED] The physical calculator has no numeric defaults inside `calculate_cost`; all inputs are serialized JSON assumptions.
- [EMPIRICAL: published logical fixtures] Logical T-gate exponents 71.6 and 56.0 are reproduced exactly.
- [CONDITIONAL: independent standard phase-state access] The query lower bound is `Omega(log N)`; arbitrary coherent structured-action queries remain Q012.

## What is established

- [EMPIRICAL: (p=419), degrees (3,5,7)] (h(-1676)=27), orbit size 27, action-group order 27, commuting generators, transitive action, and trivial stabilizer.
- [EMPIRICAL: 10 sizes and 100 trials per size] The fit is (\ln Q=2.68677\sqrt{\ln N}-0.93996\ln\ln N+4.85231), with trial-bootstrap (c\)-CI ([2.65454,2.71923]).
- [PROVED] The CI excludes schedule and extrapolation uncertainty because it resamples trials only within fixed sizes.
- [PROVED] `LOWER_BOUND.md` proves (P_{\rm succ}\le2^m/N) for (m) independent phase-state queries.
- [EMPIRICAL: final validation on 2026-06-30] All 63 shared tests, 10 P3.2 tests, five smoke modes, compilation, and artifact-format audits passed.

## What is not established

- [PROVED] The simplified low-bit-pair simulator is not Kuperberg's or Peikert's full phase-vector collimation sieve.
- [PROVED] The surface-code outputs are illustrative and are not published CSIDH physical estimates.
- [PROVED] No lower bound is proved for an arbitrary coherent call to a structured CSIDH action circuit.

## Active thread

[PROVED] There is no active implementation attempt; A001 completed its experimental objective and is marked promising.

## Next action

[PROVED] Reimplement the binary phase-vector collimation recursion from Peikert 2020, validate it against one published experiment row, and only then compare its finite-size constant with the current simplified schedule.

## Invariants

- [PROVED] Classical simulator wall-clock is never a quantum cost.
- [PROVED] QRACM, quantum memory, classical memory, logical gates, depth, and physical qubits remain separate metrics.
- [PROVED] The (c=2.68677) estimate is reported only for the sampled simplified schedule and range.

## Files that matter

- [PROVED] `RESULTS.md` is the concise result ledger; `ASSUMPTIONS.md` explains the published disagreement.
- [PROVED] `code/verify_toy_action.py` and `lib/isogeny.py` implement the explicit toy action.
- [PROVED] `code/simulate_sieve.py`, `code/fit_sieve.py`, `code/cost_model.py`, and `code/sensitivity.py` implement the experiment pipeline.
- [PROVED] `data/simulate_sieve_n24-96_seed20260722_20260630.csv` and `data/fit_sieve_n24-96_20260630.json` are the principal sieve artifacts.

## What I would tell my replacement

[PROVED] Do not improve the current regression before replacing the simplified schedule: the dominant scientific gap is algorithm fidelity, not another fit to the same finite-range staircase.
