# Handoff - P3.3 - after Session 2 continuation

## State in five lines

[PROVED] Session 1's small-$\ell$ distribution was biased by
$q_I(\ell)=\ell$ and is regression-only.
[EMPIRICAL: 108 near-$p$ ideals, 12/20/28 bits] LLL equals exact SVP on every
row; the unconstrained mean exponent is 0.40731.
[EMPIRICAL: same rows, targets through $4p$] Exact $2^e$ and $3^e$ optima are
uncensored, with mean exponents 0.78713 and 0.77643.
[EMPIRICAL: same rows] Overall median shape penalties are 222.64 and 168.23;
28-bit medians are 2476.82 and 2622.49.
The remaining Q099 gap is a matched, validated basic-KLPT comparison.

## What is established

- [CITED] The explicit maximal order and equivalent-ideal construction match
  Kohel--Lauter--Petit--Tignol 2014, Lemmas 2 and 5.
- [PROVED] Inverse-Gram coefficient bounds certify exact SVP, spectrum, and
  sparse-target searches; all witnesses are checked with exact integers.
- [PROVED] A004's coordinate-elimination branch exhausts three coefficients
  and solves the fourth quadratic by exact discriminant and divisibility tests.
- [EMPIRICAL: 108 corrected rows] LLL's exact-hit rate is 100%.
- [EMPIRICAL: same rows] All 216 pure-power optima were found. One $2^e$
  optimum has exponent 1.01280; every other result is at most $p$.
- [CITED] Basic KLPT's complete ideal estimate is near $p^{7/2}$ under its
  heuristics; $p^3$ is the intermediate lifted-quaternion scale.

## Bounded verdict

[EMPIRICAL: measured ranges] Pure-power shape is a material structural cost,
especially by 28 bits, but the exact shaped optima remain below $p^{1.013}$.
The much larger gap to basic KLPT is therefore not explained by shaped
existence alone. No KLPT implementation was run, so its lifting, congruence,
and binary norm-equation costs have not been separated.

## Attempts

A001 is dead as a distributional baseline. A002 is the corrected near-$p$
unconstrained baseline. A003 is the exact small-$p$ spectrum comparison. A004
is the exact 12/20/28-bit sparse-target comparison. A002--A004 are promising.

## Next action

Implement basic KLPT on the same seeded A002/A004 ideals. Validate every
intermediate norm identity and final equivalent ideal, then record output norm,
runtime, success/censoring, and the ratio to A004's exact matching $2^e$ or
$3^e$ optimum.

## Invariants - do not violate

- Plot $q_I(x)=\operatorname{nrd}(x)/N(I)$ as equivalent-ideal norm.
- Use near-$p$ input norms for distributional runs; small-$\ell$ data are
  regression-only.
- Do not claim the near-$p$ sampler is class-group uniform or protocol-derived.
- Preserve exact witness norm, ideal index, equivalence, and closure checks.
- Separate exact shaped existence from KLPT's algorithmic output.
- Preserve the balanced $p\bmod8$ grid and seed 33032028.

## Files that matter

- `lib/quaternion.py`: arithmetic, LLL/SVP, spectrum, sparse targets.
- `code/measure_norm_gap.py`: 108-row unconstrained experiment.
- `code/measure_shape_gap.py`: 70-row small-$p$ spectrum experiment.
- `code/measure_power_targets.py`: 108-row exact sparse-target experiment.
- `RESULTS.md`: corrected tables and bounded verdict.
- `attempts/A004-sparse-power-targets.md`: target method and outcome.
- `data/measure_power_targets_p2203-245000047x18_t6_m4_s33032028_20260713_raw.csv`.
- `figures/measure_power_targets_p2203-245000047x18_t6_m4_s33032028_20260713.png`.

## What I would tell my replacement

Do not spend another session extending exact target existence first. That gap
is closed through 28 bits. The high-value next experiment is matched basic
KLPT versus the exact A004 targets on precisely the same ideals.
