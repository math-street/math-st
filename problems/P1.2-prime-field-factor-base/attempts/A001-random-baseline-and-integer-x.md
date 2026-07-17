---
attempt: A001
status: dead
---
# A001 — Random baseline and the integer-$x$ factor base

## Idea

Measure exact ordered three-term decomposition counts and naive search work for
a uniformly sampled factor base, then rerun the identical measurement for the
integer-$x$ candidate.

## Prior art

[CITED] Semaev (2004, IACR ePrint 2004/031) defines the short-Weierstrass
summation polynomials used here, and Gaudry (2009, JSC 44) and Diem (2011,
Compositio 147) use algebraic factor bases over extension fields. Verified
metadata and relevance notes are in `refs/` and the root bibliography.

## Plan

1. Validate curve arithmetic and $f_3/f_4$ evaluation on small known cases.
2. Generate seeded prime-order ordinary curves at the requested toy sizes.
3. Build the pair-sum multiplicity table and use it to count all ordered
   decompositions for independently sampled uniform targets.
4. Run the same generic pair scan to the first decomposition and record the
   checked-pair count independently of wall-clock noise.
5. Compare Candidate A with a random factor base of exactly the same size.

## Decision rule written before execution

[HEURISTIC] A density effect is called distinguishable in this attempt only if
the 95% interval for the ratio of normalized mean counts excludes 1. A
findability improvement requires an algorithmic work reduction, not merely a
larger number of decompositions. Repeating with more curve instances or larger
sizes can falsify either conclusion.

## Execution log

The smoke run completed in 0.011 seconds. The recorded run used seed 12022026,
96 targets, three base instances per random category, and 2,000 bootstrap
samples at each of 16, 18, and 20 bits. It completed in 18.7 seconds. Raw,
summary, comparison, and scaling data are in `data/`.

## Outcome

[EMPIRICAL: one curve per size, p=65519 through 1048571] Candidate A's
normalized-count and pair-check ratios versus a size-matched random base both
had 95% intervals containing 1 at every tested size.

[PROVED] Candidate A membership is decidable with one identity check and one
integer comparison on the canonical field representative, so condition (2) is
met in polynomial time in $\log p$.

[PROVED] The tested finder scans at most $s^2$ ordered pairs and performs a
constant number of field operations per pair; this is not a
polylogarithmic-time decomposition algorithm when $s$ grows like $\sqrt p$.

## Post-mortem

**Why it failed:** [PROVED] The attempt supplies no certificate that the
integer-$x$ base meets the formal $L_p(1/2)$ size bound, and its only finder is
a generic pair scan.

[EMPIRICAL: one curve at each of 16, 18, and 20 bits] The measured interval
condition changed neither normalized density nor generic scan work
distinguishably from random in the tested sample.

**What transfers:** [EMPIRICAL: validated harness] The exact-count table,
conditional confidence intervals, pair-check metric, and separate $f_4$
verification form a reusable baseline for later candidates.

**Would it work under different assumptions?** [CONJECTURE] A different
algorithm could still exploit the interval condition in the corrected
square-root-size version; P1.2/Q004 records that coordinate-aware gap.

[PROVED] A different finder cannot repair a size-bound violation.

[EMPIRICAL: p=65519,262139,1048571] The tested Candidate-A bases were
square-root-scale diagnostics, not evidence of a standard-L asymptotic family.
An explicit polylogarithmic finder would refute the attempt's negative
practical assessment only for the corrected version.
