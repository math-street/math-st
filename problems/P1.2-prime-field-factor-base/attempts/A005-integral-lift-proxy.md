---
attempt: A005
status: dead
---
# A005 — Integral-height lift proxy

## Idea

Choose the centered integral lift
$\widetilde E:y^2=x^3+\widetilde a x+\widetilde b$ and retain reductions of
integral points with $|x|<\lfloor\sqrt p\rfloor$. This is a strict, cheaply
testable proxy for the broader canonical-height Candidate D.

## Plan

Enumerate the unique centered integer lifts in the bound, test whether the
integer right-hand side is a square, reduce valid points, and enumerate every
reachable three-term sum.

## Execution log

`code/measure_structured_candidates.py` ran the proxy on the same three curves
used by A001 and stored exact base sizes and reachable-target fractions.

## Outcome

[PROVED] Proxy membership is polynomial in $\log p$: within a bound below
$p/2$, the centered lift of $x$ is unique, and membership uses integer
arithmetic, an integer-square test, and reduction of the two possible signs.

[EMPIRICAL: p=65519,262139,1048571] The proxy factor-base sizes were 0, 0, and
2. At 20 bits the two points reached exactly four targets with three summands,
for success probability $3.82\times10^{-6}$; the other two success
probabilities were zero.

[EMPIRICAL: the surviving 20-bit lift] The two reductions come from the sign
pair above the integral point $x=-563$, $|y|=7442$. The validated seven-step
doubling estimate gives canonical height 4.72408 with final-step delta
$5.42\times10^{-5}$.

[EMPIRICAL: tested range only] The cheap integral condition is therefore far
too sparse for the required non-negligible decomposition probability.

[PROVED] This proxy does not implement canonical height on all rational lifts:
it restricts to denominator-one points and a naive-height window. It cannot be
used to rule out the full Candidate D.

## Post-mortem

**Why it failed:** [EMPIRICAL: tested curves] Requiring a modular point to come
from a genuinely small integral point changed the Candidate B saturation
problem into the opposite extreme: almost no points survived.

**What transfers:** [PROVED] A lift-based candidate must specify the curve
lift, the allowed rational preimages of a residue-class point, the height
bound, and a membership algorithm; omitting any one leaves condition (2)
undefined or unverified.

**Would it work under different assumptions?** [CONJECTURE] Allowing bounded
denominators may increase density, but deciding whether a small-height rational
preimage exists appears to become a Diophantine search. A polynomial-time
membership algorithm plus a non-negligible measured decomposition rate would
refute this assessment.
