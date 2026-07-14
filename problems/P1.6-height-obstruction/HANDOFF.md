# Handoff - P1.6 - after session 2

## State in five lines

[PROVED] The literal $\Omega(p^c)$ height target is false.
[PROVED] Single points and full-row-rank tuples with $k\leq4$ admit $O_k(\log p)$ lifts.
[EMPIRICAL: 144 variants, relation bound 8] SG-08 found 99 finite relations but only two rational two-torsion relations.
[PROVED] Bounded non-detection is not a Mordell-Weil independence certificate.
[PROVED] SG-09 failed: A002 is not a reproduction and supplies no accepted dependency rate.

## What is established

- [PROVED] The balanced direct short lift has canonical height $O(\log p)$.
- [PROVED] The five-coefficient linear lift has height $O_k(\log p)$ when its constraint matrix has row rank $k$ modulo $p$.
- [EMPIRICAL: three LMFDB values] `lib/heights.py` agrees within $2\cdot10^{-6}$.
- [EMPIRICAL: six primes, three trials each] General least-norm logarithmic slopes are $4.543,6.983,8.643,10.308$ for $k=1,2,3,4$.
- [EMPIRICAL: exact p=257 enumeration] The paper's Experiment C probability $1/65$ is reproduced.
- [EMPIRICAL: 108 k=2,3,4 variants] No rational relation through coefficient bound eight was found.
- [CITED] Jacobson et al. obtain conditional failure from bounded relation coefficients, not a $p^c$ height lower bound for selected lifts.

## Failed attempt A002

- [CITED] The target was Table 3's 317 dependent cases in 100,000 $p=17$ Experiment A runs.
- [PROVED] The source does not fix the sampling/tie-breaking distribution over short projective and coefficient-lattice vectors.
- [EMPIRICAL: local environment on 2026-07-14] The LiDIA/SIMATH and 2-descent pipeline is unavailable.
- [PROVED] `code/reproduce_xedni_p17.py` is a diagnostic prototype only; do not report or compare a rate from it.
- [CONDITIONAL: original code or complete sampling specification plus equivalent 2-descent] Reuse the validated lattice and model-conversion components.

## Active thread

[PROVED] A001 corrects the formulation but does not force rational dependence. A002 is dead. The remaining problem is a dependence-conditioned structural theorem or a genuinely faithful historical reproduction.

## Next action

Do not rerun A002 as evidence. Resolve Q018 by obtaining the original sampling/2-descent pipeline before reopening SG-09; otherwise work from the exact SG-08 bounded-relation table.

## Invariants

- Use the LMFDB/Sage non-normalized canonical height.
- Keep `rank_status=unavailable` until an actual rank computation is run.
- Say `no relation through bound 8`, never `independent`, for SG-08 negatives.
- State the coefficient-lift sampling rule; least Euclidean norm is a construction bias.
- Do not infer a positive power exponent from the six-prime range.
- Do not call A002 a reproduction or use its prototype output as evidence.

## Files that matter

- `NOTES.md`: proofs, measurements, SG-08 audit, and A002 failure boundary.
- `attempts/A001-explicit-small-lifts.md`: successful formulation correction.
- `attempts/A002-p17-experiment-reproduction.md`: dead attempt and post-mortem.
- `code/analyze_lift_relations.py`: exact bounded-relation audit.
- `data/analyze_lift_relations_b5-7-9-11_B8_allv_20260714_{rows,summary}.csv`: SG-08 output.
- `code/reproduce_xedni_p17.py`: failed-attempt prototype, reusable components only.
- `refs/jacobson-et-al2000.md`: primary-source result and assumptions.
- `OPEN_QUESTIONS.md` Q018: exact condition for reopening SG-09.

## What I would tell my replacement

[PROVED] Small simultaneous lifts are easy at fixed $k$; the missing xedni ingredient is rational dependence compatible with finite inputs that exclude useful small relations. The exact audit sharpens that distinction, while A002 must remain recorded as a failure unless its missing reproduction inputs are supplied.
