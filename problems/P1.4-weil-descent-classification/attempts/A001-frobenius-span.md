---
attempt: A001
status: dead
---
# A001 — Classify the classical binary GHS locus by Frobenius span

## Idea

Represent $\mathbb F_{2^N}$ in a polynomial basis, compute the Frobenius orbit of $\sqrt b$, and use binary Gaussian elimination to obtain both its rank and whether it contains $1$. Apply Hess's specialized genus formula without general function-field machinery.

## Prior art

[CITED] The magic-number construction is due to Gaudry, Hess, and Smart (2002), and the exact genus formula used here is the specialization of Hess (2003).

## Plan

1. Add independently tested binary-field arithmetic to `lib/curves.py`.
2. Add a problem-local GHS module computing conjugates, ranks, magic number, and exact genus.
3. Validate genus 31 against the documented $\mathbb F_{2^{155}}/\mathbb F_{2^5}$ example.
4. Sweep all nonzero $b$ in degrees 4, 6, and 8.
5. Check Frobenius invariance and summarize the low-genus $j=1/b$ locus.

## Execution log

- Added polynomial-basis binary-field arithmetic and exhaustive small-field tests to `lib/curves.py`.
- Implemented exact Frobenius span, containment, annihilator, magic-number, and genus computation in `code/ghs.py`.
- Reproduced the documented genus-31 example over $\mathbb F_{2^{155}}/\mathbb F_{2^5}$.
- Swept all 333 nonzero parameters at degrees 4, 6, and 8 and generated CSV summaries and an SVG plot.
- Converted the low-genus kernels to explicit equations in $j=1/b$.

## Outcome

[EMPIRICAL: all $b\ne0$ at $n\in\{4,6,8\}$] SG-01 through SG-04 and the density half of SG-05 succeeded; exact results are in `RESULTS.md`.

## Post-mortem

**Why it failed:** The attempt stopped at the Frobenius-span invariant. It computes a genus but does not construct the descended curve, the cover/divisor map, or an end-to-end DLP reduction, so it does not complete SG-01 as stated.

**What transfers:** The tested binary-field arithmetic, published genus-31 regression, exhaustive CSV, and low-genus equations remain usable inputs for a later explicit function-field implementation.

**Would it work under different assumptions?** Yes, as a genus-classification fallback only. It is insufficient when “implement the GHS construction” requires the actual curve and map.
