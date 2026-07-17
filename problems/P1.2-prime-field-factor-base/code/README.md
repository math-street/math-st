# Experiment code

`measure_factor_bases.py` implements SG-01 and the first SG-03 comparison. It
uses an exact ordered-pair sum table to count all ordered three-term
decompositions, then independently scans ordered pairs to find the first one.

Run the under-ten-second validation path from the repository root:

```text
python problems/P1.2-prime-field-factor-base/code/measure_factor_bases.py --smoke
```

Run the recorded experiment:

```text
python problems/P1.2-prime-field-factor-base/code/measure_factor_bases.py --bits 16 18 20 --targets 96 --replicates 3 --bootstrap 2000 --seed 12022026
```

The driver writes raw target rows, hierarchical-bootstrap summaries, the
Candidate-A versus size-matched-random comparison, and a three-point scaling
fit with every log residual to `../data/`. The primary search cost is
`pair_checks`; wall time is included only as an implementation measurement.
The exact count includes ordered triples and permits repeated factor-base
points within a decomposition.

`tests/test_formal_support_bound.py` exhaustively checks the information-
theoretic support bound on the 19-point test curve for factor-base sizes one
through five and decomposition lengths zero through four. It deliberately
enumerates ordered tuples with repetition, which upper-bounds the unordered
and distinct-summand variants as well.

`run_extension_control.py` is the SG-02 positive control. It constructs a tiny
cubic extension, finds a prime-order curve, uses the algebraic condition
$x^q=x$ for the factor base, decomposes sampled relations into three base
points, and solves simultaneously for all factor-base logarithms and a planted
target logarithm. Exhaustive scalar labels are used only after the solve as an
independent validation.

```text
python problems/P1.2-prime-field-factor-base/code/run_extension_control.py --smoke
```

`measure_structured_candidates.py` evaluates Candidate B exactly as the image
of bounded numerator/denominator pairs and evaluates a deliberately narrower
integral-lift proxy for Candidate D. The proxy is not presented as a canonical
height implementation; its purpose is to quantify the sparsity and membership
tradeoff of the simplest lift-based condition. For every surviving integral
lift it now records the validated doubling-limit canonical-height estimate from
`lib/heights.py` and its convergence delta.

```text
python problems/P1.2-prime-field-factor-base/code/measure_structured_candidates.py --smoke
```

`audit_preprocessing_loophole.py` is a specification audit for the corrected
square-root-size variant. It constructs a radix factor base that covers every
target, but deliberately stores one target-to-decomposition entry per group
element. This separates fast online lookup from linear-size preprocessing and
advice; it is not presented as an efficient ECDLP algorithm.

```text
python problems/P1.2-prime-field-factor-base/code/audit_preprocessing_loophole.py --smoke
python problems/P1.2-prime-field-factor-base/code/audit_preprocessing_loophole.py
```

`audit_translate_probe.py` exhaustively checks A009's translated-set union
bound for every one-to-four-shift schedule on the order-19 fixture. The proof
is finite-set counting; the computation is a regression against model or
implementation mistakes, not evidence for a general coordinate-aware lower
bound.

```text
python problems/P1.2-prime-field-factor-base/code/audit_translate_probe.py --smoke
python problems/P1.2-prime-field-factor-base/code/audit_translate_probe.py
```

`measure_smooth_subgroup.py` reproduces the smooth-multiplicative-subgroup
factor-base idea of Petit–Kosters–Messeng on a Fermat-prime toy field. It
exhaustively validates the repeated-squaring membership chain, measures exact
three-term counts, and compares generic finder work with matched random bases.
It does not claim that the low-degree constraint chain solves the resulting
summation-polynomial system efficiently.

```text
python problems/P1.2-prime-field-factor-base/code/measure_smooth_subgroup.py --smoke
python problems/P1.2-prime-field-factor-base/code/measure_smooth_subgroup.py
```

`benchmark_smooth_groebner.py` constructs the actual $f_4$ plus subgroup-root
systems using either direct equations $x_i^n-1$ or repeated-squaring chains.
Each Gröbner run occurs in a timeout-controlled subprocess. Completion records
basis size, degree, and terms; timeout is recorded separately from
mathematical nonexistence.

```text
python problems/P1.2-prime-field-factor-base/code/benchmark_smooth_groebner.py --smoke
python problems/P1.2-prime-field-factor-base/code/benchmark_smooth_groebner.py
```
