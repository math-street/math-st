# Adversarial self-check -- P5.1 -- 2026-07-13

## Verdict

- [EMPIRICAL: Session 4 checks below] No counting, constant, quadrature, sieve, or circular-validation defect was found.
- [EMPIRICAL: documentation audit] Two stale Session-1 scope statements were found and corrected: the attempt file's former "supports only" sentence and `NOTES.md`'s former "remains far below" sentence.
- [CITED] The computations validate published conjectural predictions but do not prove the unconditional Koblitz asymptotic. (Zywina 2011, Section 9; David and Wu 2012.)

## Independent checks

### Point counting

- [EMPIRICAL: 12 split primes $10009\le p\le900010009$] The Cornacchia--Walsh order matched the generic Hasse-interval BSGS order in every case.
- [EMPIRICAL: 3 inert primes $10007\le p\le100000007$] The generic BSGS order equaled $p+1$ in every case.
- [EMPIRICAL: every prime $5\le p\le1000$] The existing exhaustive comparison remains a stronger dense small-range check.

### Prime enumeration and quotient primality

- [EMPIRICAL: split primes $p\le5000000$] An independently written odd-only sieve, the production full sieve, and the production segmented sieve returned the same 174,193-element sequence; its SHA-256 digest is `a55430b1fa955f47c75a2d4c4b3191123866f2246021e3b922d4d69c6e300285`.
- [EMPIRICAL: 500 deterministic split-prime samples below $10^9$] The quotient-primality answers from the production Eratosthenes table, `lib.curves.is_prime`, and SymPy `isprime` had zero mismatches.
- [PROVED] The allocated quotient table is safe under Hasse's bound: if $p\le X$, then $\#E(\mathbb F_p)/8\le\lfloor(X+1+2\sqrt X)/8\rfloor$, and the implementation's ceiling with a seven-unit padding dominates this integer bound.

### Numerical integration and Euler products

- [EMPIRICAL: $x\in\{2\mathbin{\cdot}10^7,4\mathbin{\cdot}10^8,10^9\}$] Independent SciPy quadrature in logarithmic coordinates differed from the production mpmath integral by at most $1.2\mathbin{\cdot}10^{-9}$.
- [EMPIRICAL: Euler factors $\ell\le10^6$ at 60 decimal digits] The high-precision universal product differs from the float implementation by $9.0\mathbin{\cdot}10^{-15}$, and the CM product differs by $2.4\mathbin{\cdot}10^{-13}$.

### Finite-level 540.f2 certificate

- [EMPIRICAL: exact finite enumeration] A forward-generator-only closure independently recovered $|G(30)|=8640$ and exactly the production subgroup; its projections modulo $2,3,5$ have sizes $6,6,480$.
- [EMPIRICAL: CRT-decomposed lift count] Counting the mod-2 and mod-5 exclusions separately from the mod-9 lifts gave 98,280 favorable elements out of 699,840, hence $\delta_{E,3}(90)=91/648$, low-prime multiplier $455/864$, and correction $5824/5913$.
- [CONDITIONAL: LMFDB's level-30 generators and adelic-level declaration for 540.f2 are correct] The finite computation certifies the claimed quotient constant; the database input itself was not re-proved from division polynomials.

### Anti-circularity and artifact integrity

- [PROVED] Static AST inspection finds no reference to `PUBLISHED_TABLE` inside `measure`; the fixture is read only when `_result_row` computes comparison columns after the count is supplied.
- [EMPIRICAL: deliberately corrupted $x=10000$ fixture] Replacing the fixture count by 999,999 left the independently computed count at 105 and changed only the reported difference.
- [EMPIRICAL: canonical files at audit time] The full-table CSV SHA-256 is `7b40cfbfafa2a7b33a3759b9cd27656d0d3e7a6fda19298ceea1ce1f36d8e68f`; the production script SHA-256 is `d7c2b3022a013b269aa94accdffd0955c337f5e82106cf5ddad84d378359976b`.

## Attempt to falsify and residual trust boundary

- [EMPIRICAL: Session 4 audit harness] The first independent odd-only sieve attempt had an off-by-one slice-length error; correcting its index-count formula made all three sieve sequences agree. This defect was confined to the disposable audit harness and never entered production code or data.
- [CITED] The exact trace sign relies on Walsh's theorem, and the CM constant and published table rely on Zywina's paper. (Walsh 2022, Theorem 2.1; Zywina 2011, Lemma 7.1 and Table 3.)
- [CONDITIONAL: cited source and LMFDB data are accurate] The numerical and finite-group conclusions survive all independent checks performed here.
- [HEURISTIC] Agreement through $10^9$ does not establish an asymptotic; a future range can still depart from the predicted ratio, and Q026 records the theoretical obstruction.
