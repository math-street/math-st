# Code - P4.2

- `reproduce_mnt_cycle.py` instantiates the two published parameter-\(x=3\)
  MNT curves, counts both groups by direct enumeration and independently by
  Hasse/BSGS plus a twist, checks every embedding-degree residue, and writes a
  two-row CSV.
- `tests/test_reproduce_mnt_cycle.py` fixes the published field sizes, orders,
  traces, common CM radicand, and exact embedding degrees as regression values.
- `search_two_cycles.py` exhausts the prime and degree bounds frozen in
  `../SEARCH_SPACE.md`, writes every one-sided pairing-friendly candidate, and
  distinguishes full hits from near-misses.
- `tests/test_search_two_cycles.py` compares the optimized Hasse-window count
  with a direct all-pairs reference and fixes two published MNT arithmetic
  pairs as known answers.
- `construct_hit_cycles.py` uses seeded Hasse/BSGS model search to instantiate
  both sides of every full arithmetic hit, then independently verifies the
  exact order and rechecks the exact embedding degrees. It uses direct
  equation enumeration through a configurable field limit and a prime-point
  Hasse certificate above it.
- `tests/test_construct_hit_cycles.py` fixes the tiny \((10,3)\) cycle over
  fields 7 and 11 as an explicit-construction regression and compares the
  Hasse certificate with direct counts on the published MNT pair.
- `search_three_cycles.py` builds the directed Hasse graph below a prime bound,
  enumerates every directed triangle up to cyclic rotation, and records all
  two-of-three pairing-friendly near-misses and full hits.
- `tests/test_search_three_cycles.py` compares the optimized triangle count
  with direct permutation enumeration and checks every stored small-degree
  residue.
- `search_three_cycles_targeted.py` enumerates every Hasse edge but joins only
  exact target-degree edges; the coverage proof shows this retains every full
  hit and every two-of-three near-miss while avoiding irrelevant triangles.
  Its cyclotomic-root mode generates the exact target edges without scanning
  the Hasse windows.
- `tests/test_search_three_cycles_targeted.py` compares its complete candidate
  rows with the exhaustive algorithm at two small bounds.
- `search_two_cycles_targeted.py` enumerates every Hasse-valid pair and retains
  complete hit/near-miss rows while factoring discriminants only for retained
  candidates. Its cyclotomic-root mode directly generates every pair having at
  least one target edge.
- `tests/test_search_two_cycles_targeted.py` compares its candidate rows and
  Hasse count with the full algorithm and compares root generation with Hasse
  scanning.
- `analyze_three_cycle_near_misses.py` factors the relevant prime-minus-one
  values and records the exact missing embedding degrees for extension
  near-misses.
- `tests/test_analyze_three_cycle_near_misses.py` fixes a 20-bit missing degree
  of 483,882 as a regression.
- `verify_mnt_parameterization.py` checks every degree-(6,4) or degree-(4,6)
  ledger hit against the elementary MNT converse in `../MNT_CLASSIFICATION.md`.
- `tests/test_verify_mnt_parameterization.py` fixes both x=3 orientations and
  rejects a non-MNT field pair.
- `analyze_mnt_three_chains.py` exhausts the finite x<=1025 remainder in the
  global consecutive-MNT-chain obstruction and records both exact closing
  degrees for every all-prime triple.
- `tests/test_analyze_mnt_three_chains.py` fixes the degree-recurrence table,
  the x=480 near-miss degrees, and the complete four-row finite certificate.
- `classify_three_cycle_near_misses.py` rotates every two-target-edge row to a
  common missing-closing-edge convention and separates consecutive MNT-chain
  orientations from the residual ledger.
- `tests/test_classify_three_cycle_near_misses.py` preserves all 42 source
  rows and fixes both x=480 orientations plus the unique high residual.
- `classify_quadratic_degree_pairs.py` exhausts the Hasse-bounded multiplier
  equations for all ordered 2-cycle degree pairs in {3,4,6}.
- `tests/test_classify_quadratic_degree_pairs.py` fixes the complete 11-row
  multiplier certificate and its two MNT identity cases.
- `classify_mixed_degree_pairs.py` reduces all 24 mixed
  quadratic/quartic ordered degree pairs to 108 bounded multiplier cases and
  finite linear-remainder divisibility checks.
- `tests/test_classify_mixed_degree_pairs.py` fixes all 108 cases, the maximum
  proved gap bound, and the unique exact (10,3) cycle over fields 7 and 11.
- `reduce_quartic_degree_pairs.py` bounds the quotient difference and reduces
  all quartic/quartic ordered pairs to squarefree genus-zero/one discriminant
  equations using SymPy 1.14.0.
- `audit_quartic_degenerate_cases.py` closes all non-genus-one discriminant
  rows by exact sign, root, divisibility, primality, Hasse, and degree checks.
- `audit_quartic_small_gaps.py` exhausts every quartic/quartic divisor
  candidate for even field gaps 2 through 106.
- `construct_three_cycle_hits.py` instantiates every full directed triangle
  and independently counts all three curve equations.
- `tests/test_construct_three_cycle_hits.py` fixes the first tiny directed
  3-cycle over fields 7, 13, and 11 as a construction regression.

Run the tests from the repository root:

```powershell
python -m unittest discover -s problems/P4.2-pairing-friendly-cycles/code/tests -v
```

Run the sub-10-second smoke regression:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/reproduce_mnt_cycle.py --smoke
```

Run the recorded SG-02 regression:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/reproduce_mnt_cycle.py --seed 4202
```

Run the bounded search smoke test:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/search_two_cycles.py --smoke
```

Run the frozen SG-04 search:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/search_two_cycles.py --limit 65536 --max-degree 12
```

Observed runtime: 0.53 s on Python 3.13.4; exact runtime is in the summary JSON.

Construct and verify every full hit from that search:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/construct_hit_cycles.py --seed 4203 --max-attempts 20000
```

Construct only hits newly appearing at a larger prime boundary:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/construct_hit_cycles.py --candidates <extended.csv> --minimum-field 262144 --max-attempts 100000
```

For fields above the 22-bit direct-enumeration range, retain exact independent
verification with the prime-point Hasse certificate:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/construct_hit_cycles.py --candidates <extended.csv> --minimum-field 4194304 --exhaustive-limit 4194303 --max-attempts 500000
```

Run the frozen length-3 search:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/search_three_cycles.py --limit 65536 --max-degree 12
```

Observed runtime: 8.04 s on Python 3.13.4; exact runtime is in the summary JSON.

Construct and verify every full length-3 hit:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/construct_three_cycle_hits.py --seed 4303 --max-attempts 20000
```

Run the targeted search used beyond 18-bit bounds:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/search_three_cycles_targeted.py --limit 1048576 --max-degree 12
```

Run the candidate-complete targeted 2-cycle search:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/search_two_cycles_targeted.py --limit 4194304 --max-degree 12
```

At the 22-bit bound this took 82.28 s; the targeted 3-cycle search took
85.48 s. Exact runtimes and coverage counts are in their summary JSON files.

Compute exact degrees for newly appearing 3-cycle near-misses:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/analyze_three_cycle_near_misses.py --candidates problems/P4.2-pairing-friendly-cycles/data/search_three_cycles_targeted_p5-4194303_k3-12_20260708_candidates.csv --minimum-field 1048576
```

Verify the MNT parameterization of the 22-bit degree-{4,6} ledger:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/verify_mnt_parameterization.py --candidates problems/P4.2-pairing-friendly-cycles/data/search_two_cycles_targeted_p5-4194303_k3-12_20260708_candidates.csv
```

Exhaust the finite remainder of the consecutive-MNT-chain obstruction:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/analyze_mnt_three_chains.py --max-x 1025
```

The last three analyses each run in under one second on Python 3.13.4.

Run the proved-complete cyclotomic-root searches used at 26 and 28 bits:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/search_two_cycles_targeted.py --limit 268435456 --max-degree 12 --pair-generator cyclotomic_roots
python problems/P4.2-pairing-friendly-cycles/code/search_three_cycles_targeted.py --limit 268435456 --max-degree 12 --edge-generator cyclotomic_roots
```

The recorded 28-bit runtimes are 301.0 seconds and 427.7 seconds.

Reproduce the global {3,4,6}-degree multiplier certificate:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/classify_quadratic_degree_pairs.py
```

Reproduce the mixed and quartic symbolic classifications:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/classify_mixed_degree_pairs.py
python problems/P4.2-pairing-friendly-cycles/code/reduce_quartic_degree_pairs.py --h-bound 24
python problems/P4.2-pairing-friendly-cycles/code/audit_quartic_small_gaps.py --maximum-gap 106
python problems/P4.2-pairing-friendly-cycles/code/audit_quartic_degenerate_cases.py --h-bound 24
```

Apply the complete local, real, and finite-gap sieve pipeline:

```powershell
python problems/P4.2-pairing-friendly-cycles/code/sieve_quartic_local_obstructions.py --prime-bound 251
python problems/P4.2-pairing-friendly-cycles/code/sieve_quartic_archimedean.py --prime-bound 251
python problems/P4.2-pairing-friendly-cycles/code/lift_quartic_singular_primes.py --maximum-exponent 8
python problems/P4.2-pairing-friendly-cycles/code/lift_quartic_two_adic.py --maximum-exponent 12
python problems/P4.2-pairing-friendly-cycles/code/search_quartic_integral_points.py --maximum-gap 10000000
python problems/P4.2-pairing-friendly-cycles/code/canonicalize_quartic_survivors.py
python problems/P4.2-pairing-friendly-cycles/code/canonicalize_quartic_survivors.py --exclude-odd-obstructions
```

The recorded runtimes are 1.4 seconds for the 750-row local sieve, 2.1
seconds for the real sieve, 2.5 seconds for singular lifting, 4.1 seconds for
the two-adic audit, and 8.2 seconds for all 11,333,558 wheel candidates through
gap 10,000,000 on Python 3.13.4 with SymPy 1.14.0.

The final exact global computations use Magma V2.29-8 inputs
`magma_pointed_quartics.m`, `magma_two_cover_descent.m`, and
`magma_reducible_rank.m`. Their tagged outputs are stored in `data/` and are
regression-checked locally.
