# Handoff — P1.4 — after session 1

**Outcome: FAILED.** Preserve the partial data, but do not treat this session as completion of SG-01 or of the requested deliverables.

## State in five lines

- Basic binary GHS span/genus computation is implemented and validated.
- Every nonzero $b$ was swept at $n=4,6,8$ (333 rows total).
- The documented $\mathbb F_{2^{155}}/\mathbb F_{2^5}$ example reproduces genus 31.
- Low-genus $b$- and $j$-loci have explicit equations in `RESULTS.md`.
- No explicit cover map or end-to-end DLP has been built.

## What is established

- [CITED] GHS magic number: Gaudry–Hess–Smart (2002).
- [CITED] Exact genus branch: Hess (2003).
- [EMPIRICAL: all $b\ne0$, $n\in\{4,6,8\}$] Full census and Frobenius-invariance checks pass.
- [EMPIRICAL: published Magma V2.19.8 example] Rank 5, magic 6, genus 31.
- [EMPIRICAL: all full-degree parameters, same range] Minimum genera are 4, 8, 16.

## What is ruled out

- Genus alone is not evidence of a faster attack; no subgroup-order or Jacobian-DLP cost was measured.
- The current code computes the GHS invariant but does not construct $C$, $C\to E$, or the divisor map.

## Active thread

A001 is dead as an implementation of SG-01: the Frobenius-span classification works, but it never constructs the required function field, curve, or map.

## Next action

Derive the $n=4,6,8$ distribution from the Maurer–Menezes–Teske type-counting theorem, then select the $n=6$, genus-3 subfield case for a hand-built cover-map experiment.

## Invariants — do not violate

- Curves use $y^2+xy=x^3+ax^2+b$ with $b\ne0$ and $j=1/b$.
- Sweeps set $a=0$, so the GHS regularity trace condition holds.
- “Low genus” in the locus CSV means the declared experimental bound $B_n=2^{n/2}$, not proven attackability.
- The 155-bit run is only the justified published-example regression; routine experiments stay below the 60-bit ceiling.

## Files that matter

- `code/ghs.py`: validated invariant implementation.
- `code/verify_published_example.py`: genus-31 regression.
- `code/sweep_ghs_genus.py`: deterministic census and summaries.
- `data/sweep_ghs_genus_n4-6-8_20260623.csv`: all 333 rows.
- `data/ghs_genus_distribution_n4-6-8_20260623.csv`: exact distribution.
- `data/ghs_low_genus_locus_n4-6-8_20260623.csv`: equations and densities.
- `RESULTS.md`: concise interpretation and limitations.

## What I would tell my replacement

The useful object is the Frobenius annihilator, not just the rank. For the selected bounds, the union of low-rank classes is a single kernel, which makes the $j$-locus equation immediate after inversion.
