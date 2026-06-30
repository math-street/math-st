# P3.2 code

## Toy action

[PROVED] `verify_toy_action.py` exhaustively enumerates reduced forms and the explicit rational-isogeny orbit, writes the complete transition table, and checks whether the generated permutation action is regular.

```powershell
python problems/P3.2-class-group-quantum-constant/code/verify_toy_action.py --smoke
python problems/P3.2-class-group-quantum-constant/code/verify_toy_action.py
```

[PROVED] The reported `regular` field is true exactly when the enumerated permutation group is transitive and the base-state stabilizer is trivial; this follows from the checks in `build_report`.

[PROVED] The script uses explicit rational Vélu quotients and does not substitute an abstract regular action; inspect `lib/isogeny.py` and the serialized transition table.

## Sieve simulation and fit

[PROVED] `simulate_sieve.py` simulates bucket occupancy, pair formation, combination-measurement success, and final target-label selection for a fixed-batch low-bit-collision schedule over cyclic groups of order (2^n). `fit_sieve.py` fits natural-log query counts to

\[
\ln Q=c\sqrt{\ln N}+d\ln\ln N+k.
\]

```powershell
python problems/P3.2-class-group-quantum-constant/code/simulate_sieve.py --smoke
python problems/P3.2-class-group-quantum-constant/code/simulate_sieve.py
python problems/P3.2-class-group-quantum-constant/code/fit_sieve.py --input problems/P3.2-class-group-quantum-constant/data/simulate_sieve_n24-72_seed20260722_20260630.csv
```

[PROVED] `query_count` is a back-propagated count of abstract input phase states under the simulated batch schedule; it is not elapsed time, a quantum gate count, or a physical resource estimate, by the counter's definition in `simulate_trial`.

## Physical-cost layer

[PROVED] `cost_model.py` reads the simulated counters and a complete JSON assumption set. Its surface-code formula is phenomenological and is explicitly labelled illustrative. `sensitivity.py` varies only the endpoints named in a second JSON file and ranks their effect on physical qubit-seconds.

```powershell
python problems/P3.2-class-group-quantum-constant/code/cost_model.py --sieve-csv problems/P3.2-class-group-quantum-constant/data/simulate_sieve_n24-96_seed20260722_20260630.csv --n-bits 64 --config problems/P3.2-class-group-quantum-constant/code/configs/illustrative_surface_code.json
python problems/P3.2-class-group-quantum-constant/code/sensitivity.py --cost-report problems/P3.2-class-group-quantum-constant/data/cost_model_n64_illustrative_surface_code_20260630.json --ranges problems/P3.2-class-group-quantum-constant/code/configs/illustrative_sensitivity_ranges.json
```

[PROVED] The calculator exposes all operation costs, architecture choices, and error-correction constants in its serialized `assumptions`; the calculation function supplies no numeric defaults.

[PROVED] The output is conditional on the supplied JSON values by direct substitution into the documented formulas; `illustrative_surface_code.json` is not a reproduction of a published CSIDH estimate.

[PROVED] The following fixtures reproduce published logical arithmetic endpoints; their generated physical fields remain illustrative:

```powershell
python problems/P3.2-class-group-quantum-constant/code/cost_model.py --counters-json problems/P3.2-class-group-quantum-constant/code/configs/bonnetain_schrottenloher_2020_section3_3_counters.json --config problems/P3.2-class-group-quantum-constant/code/configs/bonnetain_schrottenloher_2020_section3_3.json
python problems/P3.2-class-group-quantum-constant/code/cost_model.py --counters-json problems/P3.2-class-group-quantum-constant/code/configs/peikert_2020_optimistic_endpoint_counters.json --config problems/P3.2-class-group-quantum-constant/code/configs/peikert_2020_optimistic_endpoint.json
```

[EMPIRICAL: `code/tests/test_cost_model.py`] The fixtures reproduce logical T-gate exponents 71.6 and 56.0, respectively.
