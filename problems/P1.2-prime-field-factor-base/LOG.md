# Archived session log — sessions 1–5

## Session 1 — 2026-06-22

**Goal:** Establish SG-01 at the three requested bit sizes and, if runtime
permits, use the same harness for the SG-03 integer-$x$ candidate.

**Prediction (written before running anything):**

- [HEURISTIC] For random bases, the mean ordered decomposition count will be
  within 15% of $s^3/r$ at each tested size. This prediction is falsified at a
  size if the reported 95% interval for the normalized mean excludes
  $[0.85,1.15]$.
- [HEURISTIC] Candidate A will not change the normalized mean count by more
  than 20% relative to a size-matched random base. This prediction is falsified
  if the 95% interval for the ratio of normalized means excludes
  $[0.8,1.2]$.
- [HEURISTIC] A lexicographic pair scan will require work on the order of
  $r/s$, not a polynomial in $\log p$. A three-size log-log slope inconsistent
  with $1/2$ by more than 0.2, or a candidate-specific polylogarithmic method,
  would falsify this session-level prediction.

**Did:**

- Initialized the problem folder because no P1.2 state existed.
- Recorded the prediction before running mathematical experiments.
- Added shared short-Weierstrass arithmetic and $f_3,f_4,f_5$ evaluation,
  preserving the pre-existing generic-DLP API.
- [EMPIRICAL: unit test over F_17] Validated the pair-sum counter against direct ordered-triple enumeration on
  the known 19-point curve $y^2=x^3+2x+2$ over $\mathbb F_{17}$.
- Ran seed 12022026 at 16, 18, and 20 bits with 96 common targets per curve,
  three random bases per random category, and 2,000 hierarchical-bootstrap
  samples.

**Found:**

- [EMPIRICAL: one prime-order curve at each of p=65519,262139,1048571] The
  random-$\lfloor\sqrt p\rfloor$ normalized mean decomposition counts were
  1.0000, 0.9977, and 0.9976; every 95% interval contained 1 (script
  `code/measure_factor_bases.py`, summary CSV in `data/`).
- [EMPIRICAL: same three curves, 96 targets per candidate] Candidate A's
  normalized-count ratio to the size-matched random baseline was 1.030, 1.002,
  and 1.004; the respective 95% intervals were [0.963,1.118],
  [0.970,1.035], and [0.986,1.023].
- [EMPIRICAL: same three curves] Candidate A's pair-check ratio to the matched
  baseline was 0.938, 1.050, and 0.866; every 95% interval contained 1.
- [EMPIRICAL: 2,016 target/base rows] Every target had at least one
  three-term decomposition, and all 2,016 returned decompositions passed the
  group-law check; all 2,016 also passed $f_4$ because no sampled target or
  returned term was the identity.
- [EMPIRICAL: p=65519 through 1048571] A three-point descriptive fit of mean
  pair checks against $p$ gave slopes 0.529 (random square-root base), 0.437
  (size-matched random), and 0.408 (Candidate A); residuals are stored in the
  scaling CSV.

**Prediction vs. outcome:** [EMPIRICAL: preregistered three-size run] Matched.
The baseline was within the preregistered 15% band, Candidate A's density
effect was within the preregistered 20% band, and every descriptive slope was
within 0.2 of $1/2$.

**Did not work:** Two launches used an accidental one-second shell timeout and
were terminated during curve setup. They produced no result file; the unchanged
command completed in 18.7 seconds with a 120-second execution window. No
polynomial-system solver was tested: $f_4$ was a verifier, not the method that
found decompositions.

**Changed my mind about:**

- [EMPIRICAL: tested range only] Abundant decompositions and 100% observed
  success are weaker evidence than they initially appear: the measured search
  still took hundreds to thousands of pair checks and Candidate A did not
  separate from random density or search work.

**Next:** Implement SG-02 over a tiny cubic extension and recover a known
discrete logarithm end to end.
