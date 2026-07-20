---
attempt: A001
status: promising
---
# A001 — Corrected-constant density measurement

## Idea

- [HEURISTIC] Compare exact fixed-curve counts with Zywina's refined finite-$x$ predictor $C_{E,1}\sum_{p\le x}1/\log(p+1)$; the heuristic is falsified at this range if the largest-cutoff ratio interval excludes 1 after both counter and constant pass independent checks.

## Prior art

- [CITED] Koblitz tabulated three full-image curves through $p<30000$ using the separate-prime product. (Koblitz 1988, Table I, *Pacific Journal of Mathematics* 131.)
- [CITED] Zywina tabulated the Serre curve $y^2=x^3+6x-2$ from $2\mathbin{\cdot}10^7$ through $10^9$ using the corrected constant and refined integral predictor. (Zywina 2011, Table 1, arXiv:0909.5280.)

## Plan

1. Validate BSGS/twist orders against exhaustive orders on fixed small primes.
2. Reproduce both published product constants.
3. Sweep three curves through increasing toy cutoffs.
4. Store deterministic CSV output, plot convergence, and report a Poisson-style heuristic interval.

## Execution log

- [EMPIRICAL: 34 shared tests] Shared-library preflight passed after installing pytest.
- [EMPIRICAL: 67 reductions through $p=97$] The production counter matched exhaustive counts; one non-isolating BSGS/twist case used the declared exact fallback.
- [EMPIRICAL: Euler factors $\ell\le10^6$] Both published product targets were reproduced within $4\mathbin{\cdot}10^{-8}$.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The three-curve sweep completed in 11.2 seconds wall time and produced deterministic CSV and PNG outputs.

## Outcome

- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The Serre curve yielded 683 prime orders versus 654.886 refined-predicted, ratio $1.04293$ with heuristic 95% interval $[0.9647,1.1211]$.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] Both rational-torsion curves yielded zero prime orders, as proved by their torsion injections.
- [EMPIRICAL: $2^{10}\le x\le2^{17}$] The refined-predictor ratio moved from $0.8030$ to $1.0429$; the raw asymptotic ratio remained $1.2890$ at the largest cutoff.
- [PROVED] At the end of Session 1, the implementation supported only a certified Serre correction and rational-torsion zero constants; Sessions 2--3 below add the certified 540.f2 quotient case and the cited CM case, while a generic arbitrary-curve adelic calculator remains out of scope.

## Session 2 extension

- [CONDITIONAL: LMFDB's level and generator data for 540.f2 are correct] Exact enumeration at the modulus required by Zywina's Proposition 2.4 gives $C_{E,3}=(5824/5913)C$ for $y^2=x^3+3x-11$.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The 661 quotient-prime events are $1.015998$ times the refined prediction of 650.592.
- [CITED] The CM case $y^2=x^3-x$ uses $E_{\mathbb Q(i)}$, quotient $t=8$, the split condition $p\equiv1\pmod4$, and a distinct constant approximately $1.067350894$. (Zywina 2011, Section 7.)
- [EMPIRICAL: split good primes $5\le p\le2^{17}$] The CM case has 765 events versus 779.701 predicted, ratio $0.981145$.
- [EMPIRICAL: all good rational primes $5\le p\le2^{17}$] Pooling the CM strata and applying the inapplicable full-$\mathrm{GL}_2$ quotient model gives ratio $4.0508$, confirming that the split-prime convention is mathematically substantive.

## Session 3 extension

- [CITED] Walsh's exact trace theorem supplies a specialized point counter for $y^2=x^3-x$ from a Cornacchia representation of split primes. (Walsh 2022, Theorem 2.1.)
- [EMPIRICAL: every prime $5\le p\le1000$] The specialized counter matches exhaustive point counting at every prime.
- [EMPIRICAL: all 50 checkpoints $2\mathbin{\cdot}10^7\le x\le10^9$] The independent run reproduces every actual and rounded-expected value in Zywina's Table 3 with zero mismatches.
- [EMPIRICAL: $x=10^9$] The final observed/integral-predicted ratio is $0.9994253$ after 1,548,766 quotient-prime events.

## Session 4 self-verification

- [EMPIRICAL: 15 deterministic primes through $9\mathbin{\cdot}10^8$] The specialized CM order and generic BSGS order agree in every split and inert sample.
- [EMPIRICAL: split primes $p\le5\mathbin{\cdot}10^6$] Three sieve implementations produce the same 174,193-element sequence.
- [EMPIRICAL: three cutoffs through $10^9$] Independent SciPy and production mpmath integrals differ by at most $1.2\mathbin{\cdot}10^{-9}$.
- [EMPIRICAL: exact finite enumeration] A CRT-decomposed recomputation recovers $\delta_{E,3}(90)=91/648$ and correction $5824/5913$.
- [PROVED] The published table fixture is comparison-only and has no data-flow path into event counting; a fixture-mutation regression now enforces this invariant.
- [EMPIRICAL: documentation audit] Two stale Session-1 scope statements were corrected; no mathematical or computational result changed.

## Session 5 theory closure

- [CITED] The 2025 literature audit found a conditional derivation of the refined constant, an unconditional theorem on averages of constants, and unconditional CM almost-prime progress, but no unconditional fixed-curve prime-order asymptotic. (Dey et al. 2025; Lee, Mayle, and Wang 2025; Xie 2025.)
- [PROVED] `THEORY_CLOSURE.md` reduces the CM event, apart from $p=17$, to simultaneous primality of $N(a+bi)$ and $N(a+bi+1)/8$.
- [PROVED] The attempt's empirical, finite-group, and algebraic objectives are complete; Q026 records the external asymptotic theorem that is not supplied by this attempt.
