# Notes — P5.1

## Stable facts

- [CITED] Koblitz's original positive-constant statement excludes curves that are \(\mathbb{Q}\)-isogenous to curves with nontrivial rational torsion. (Koblitz 1988, *Pacific Journal of Mathematics* 131.)
- [CITED] Zywina replaces the product of separate local densities by a finite-level adelic density limit, which captures entanglement between division fields and may be zero. (Zywina 2011, Definition 2.1, arXiv:0909.5280.)
- [CITED] For full \(\mathrm{GL}_2(\mathbb{F}_\ell)\) local images, the universal local factor is
  \[
  1-\frac{\ell^2-\ell-1}{(\ell-1)^3(\ell+1)}.
  \]
  (Zywina 2011, Proposition 2.4, arXiv:0909.5280.)
- [CITED] The universal product is approximately $0.505166168239435774$. (Zywina 2011, equation (2.3), arXiv:0909.5280.)
- [CITED] The curve $E_0:y^2=x^3+6x-2$ is a Serre curve and has $C_{E_0,1}=(10/9)C\approx0.561295742488261971$. (Zywina 2011, Section 5 and equation (5.1), arXiv:0909.5280.)

## Tool substitution

- [EMPIRICAL: $p\le 2^{17}$] PARI/GP and SageMath were unavailable, so this session used the validated Hasse-interval BSGS/twist counter in `lib/curves.py`, checked against exhaustive counting at small primes.

## Curve certificates

- [CITED] LMFDB identifies $y^2=x^3+6x-2$ as curve 1728.w1, and its q-expansion gives the checked orders $4,7,10,15,24,15,18$ at $p=5,7,11,13,17,19,23$. (LMFDB, curve 1728.w1, accessed 2026-06-24.)
- [CITED] LMFDB identifies $y^2=x^3+x-2$ as curve 112.b4, with no CM and rational torsion of order 2. (LMFDB, curve 112.b4, accessed 2026-06-24.)
- [PROVED] The point $(3,5)$ on $y^2=x^3+3x-11$ has order 3: the tangent slope is 3, so the duplication formula gives $2(3,5)=(3,-5)=-(3,5)$.
- [PROVED] The 2- and 3-torsion test curves are non-CM. Their rational $j$-invariants are respectively $432/7$ and $6912/125$, neither an integer; a CM $j$-invariant is an algebraic integer, and a rational algebraic integer is an integer. (Silverman 2009, *The Arithmetic of Elliptic Curves*, Chapter II, Section 6.)

## Session 1 measurements

- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The production counter agreed with exhaustive counting on all 67 validation cases through $p=97$; 66 used BSGS/twist and one used the declared exhaustive fallback. (`code/measure_density.py`; `data/measure_density_x131072_l1000000_s51012026_20260624.csv`.)
- [EMPIRICAL: Euler factors $\ell\le10^6$] The universal product was $0.505166202477432$, within $3.43\mathbin{\cdot}10^{-8}$ of Zywina's published limit, and the corrected Serre constant was $0.561295780530480$, within $3.80\mathbin{\cdot}10^{-8}$ of the published value. (`code/measure_density.py`.)
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] For 1728.w1, 683 of 12,249 reductions had prime order; the refined predictor was 654.886, giving observed/predicted $1.04293$. (`data/measure_density_x131072_l1000000_s51012026_20260624.csv`.)
- [HEURISTIC] Treating the 683 events as approximately Poisson gives a 95% interval $[0.9647,1.1211]$ for observed/predicted; dependence or finite-cutoff bias can invalidate this interval.
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The raw asymptotic predictor $C_{E,1}x/(\log x)^2$ gave 529.85 rather than 683 events, so observed/predicted was still $1.2890$; Zywina's refined prime-sum predictor reduced this discrepancy to $1.0429$. (`data/measure_density_x131072_l1000000_s51012026_20260624.csv`.)
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] Both rational-torsion curves had zero prime-order reductions. The quotient-order diagnostic found 1 prime value after division by 2 and 661 after division by 3, but this session did not implement $C_{E,t}$ for $t>1$, so no quotient-density comparison is claimed. (`data/measure_density_x131072_l1000000_s51012026_20260624.csv`.)

## Where GRH enters

- [CITED] David and Wu assume a theta-zero-free hypothesis for Dedekind zeta functions and the relevant Artin $L$-functions attached to division fields; GRH is the case $\theta=1/2$. (David and Wu 2012, Hypothesis 3.4, arXiv:0812.2860.)
- [CITED] The hypothesis is used in effective Chebotarev estimates for primes whose Frobenius class forces divisibility of $\#E(\mathbb{F}_p)$ by squarefree $d$; these estimates supply the uniform remainder bound required by the weighted and Selberg sieves. (David and Wu 2012, Theorem 3.9 and equations (4.11)--(4.14), arXiv:0812.2860.)
- [CITED] Their usable sieve level is $D=x^{(2/5)(1-\theta)(1-\varepsilon)}$; the resulting almost-prime parameter is $r=\lfloor(18+2\theta)/(5(1-\theta))\rfloor+1$. At $\theta=1/2$ this yields $P_8$, while any $\theta<11/21$ still yields the stated eight-almost-prime corollary. (David and Wu 2012, Theorem 1.1 and Corollary 1.2, arXiv:0812.2860.)
- [CITED] The same theta-hypothesis gives a prime-order upper bound with factor $5/(1-\theta)+\varepsilon$, hence factor $10+\varepsilon$ under GRH; it does not give a lower bound for prime orders. (David and Wu 2012, Theorem 1.3 and equation (5.2), arXiv:0812.2860.)
- [CITED] Unconditionally, the fixed-curve upper bound recorded by Zywina is weaker, of order $x/(\log x\log\log x)$, whereas CM curves admit stronger unconditional almost-prime results. (Zywina 2011, Sections 9.1--9.2, arXiv:0909.5280.)
- [CITED] Thus GRH can already be weakened to the explicit theta-hypothesis for these partial results; making them unconditional requires an unconditional replacement for the division-field Chebotarev error at a positive sieve level, and the cited sieve still stops at almost-primes rather than proving the Koblitz asymptotic. (David and Wu 2012, Sections 3--5, arXiv:0812.2860.)

## Limits

- [PROVED] `corrected_constant` is a registry of certified cases, not a generic adelic-image calculator: it implements only Zywina's $10/9$ Serre correction and the elementary rational-torsion obstruction.
- [EMPIRICAL: Session 1, $p\le2^{17}$] The original toy sweep was far below Zywina's published range and served only as a validation and convergence demonstration; Session 3 later reproduced the complete published CM table through $10^9$.

## Session 2 finite-level certificate for the 3-torsion quotient

- [CITED] LMFDB identifies $y^2=x^3+3x-11$ as 540.f2, with rational torsion $\mathbb Z/3\mathbb Z$ and adelic image of level 30, index 16, and label `30.16.0-30.b.1.4`; it publishes seven generators modulo 30. (LMFDB, curve 540.f2, accessed 2026-06-29.)
- [CITED] For a non-CM curve and a valid adelic level $M$, Zywina's Proposition 2.4 computes $C_{E,t}$ from $\delta_{E,t}(t\prod_{\ell\mid tM}\ell)$ and the universal factors away from $tM$. (Zywina 2011, Proposition 2.4, arXiv:0909.5280.)
- [PROVED] With $t=3$ and $M=30$, the required modulus is $3(2\cdot3\cdot5)=90$; at this modulus, $\det(I-A)\in3(\mathbb Z/90\mathbb Z)^\times$ is equivalent to $\gcd(\det(I-A),90)=3$.
- [CONDITIONAL: LMFDB's level and generator data for 540.f2 are correct] `code/measure_corrected_cases.py` exhaustively generates 8640 matrices in $G(30)$ and all $3^4=81$ entrywise lifts of each matrix, obtaining $|G(90)|=699840$ and $|G(90)\cap\Psi_3(90)|=98280$.
- [CONDITIONAL: LMFDB's level and generator data for 540.f2 are correct] The exact density is $98280/699840=91/648$; dividing by $(1-1/2)(1-1/3)(1-1/5)$ gives $455/864$, while the universal product's factors at $2,3,5$ multiply to $1095/2048$, so
  \[
  C_{E,3}=\frac{455/864}{1095/2048}C=\frac{5824}{5913}C.
  \]
- [EMPIRICAL: Euler factors $\ell\le10^6$] The resulting truncated value is $C_{E,3}=0.497562652330215$. (`code/measure_corrected_cases.py`.)
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] There are 661 prime values of $\#E(\mathbb F_p)/3$ versus 650.592 predicted; observed/predicted is $1.015998$, and the measured-constant interval is $[0.466985,0.544060]$, which contains the certified prediction. (`data/measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv`.)
- [EMPIRICAL: $2^{10}\le x\le2^{17}$] The corrected quotient ratio is $1.0767,1.1480,0.9618,1.1734,1.0715,1.0232,0.9796,1.0160$ at consecutive powers of two. (`data/measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv`.)

## Session 2 CM case

- [CITED] For $E:y^2=x^3-x$, all CM endomorphisms are defined over $\mathbb Q(i)$, $E(\mathbb Q(i))_{\mathrm{tors}}$ has order 8, and split rational primes are exactly $p\equiv1\pmod4$; the CM conjecture therefore studies $\#E(\mathbb F_p)/8$ on this split stratum. (Zywina 2011, Section 7.)
- [CITED] Zywina's CM constant is
  \[
  C_{E_{\mathbb Q(i)},8}=\prod_{\ell\ne2}\left(1-\chi(\ell)\frac{\ell^2-\ell-1}{(\ell-\chi(\ell))(\ell-1)^2}\right)\approx1.067350894,
  \]
  where $\chi(\ell)=(-1)^{(\ell-1)/2}$; an absolutely convergent evaluation extracts $L(1,\chi)=\pi/4$. (Zywina 2011, Lemma 7.1.)
- [EMPIRICAL: Euler factors $\ell\le10^6$] The accelerated implementation returns $1.067350966817026$, within $7.3\mathbin{\cdot}10^{-8}$ of the published approximation. (`code/measure_corrected_cases.py`.)
- [EMPIRICAL: split good primes $5\le p\le2^{17}$] Among 6094 split primes, 765 yield prime $\#E(\mathbb F_p)/8$ versus 779.701 predicted; observed/predicted is $0.981145$, and the measured-constant interval $[0.973017,1.121435]$ contains the published prediction. (`data/measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv`.)
- [EMPIRICAL: $2^{10}\le x\le2^{17}$, split primes] The CM corrected ratio rises from $0.8443$ to $0.9811$, while remaining within its heuristic interval at the largest cutoff. (`data/measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv`.)
- [EMPIRICAL: all good rational primes $5\le p\le2^{17}$] The deliberately invalid pooled full-$\mathrm{GL}_2$ $t=8$ benchmark predicts 243.653 events but observes 987, ratio $4.0508$; this diagnoses model misuse, not failure of the CM conjecture, whose rational-prime formulation retains only the split stratum. (`data/measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv`.)

## Session 3 exact CM trace and complete published-table reproduction

- [CITED] Walsh's trace theorem for $E_d:y^2=x^3+dx$ starts from $p=a^2+b^2$ with $a\equiv1\pmod4$ and assigns the trace from the quartic-residue class of $d$. (Walsh 2022, Theorem 2.1, DOI 10.33039/ami.2022.11.003.)
- [PROVED] For $d=-1$, Walsh's theorem specializes to $a_p=2a$ when $p\equiv1\pmod8$, $a_p=-2a$ when $p\equiv5\pmod8$, and $a_p=0$ when $p\equiv3\pmod4$; hence $\#E(\mathbb F_p)=p+1-a_p$ is computable after one Cornacchia representation.
- [EMPIRICAL: every prime $5\le p\le1000$] `code/reproduce_cm_table.py` agrees with exhaustive point counting for every prime and verifies the sum-of-two-squares identity at every split prime.
- [EMPIRICAL: $x=2\mathbin{\cdot}10^7$] The exact counter returns 49,847 events and the equation-(7.1) integral returns 50,062.774, rounding to 50,063; both differences from Zywina's first Table 3 row are zero.
- [EMPIRICAL: all 50 checkpoints $2\mathbin{\cdot}10^7\le x\le10^9$] Every computed actual count equals Zywina's Table 3 value and every computed integral rounds to the published expected value; both mismatch totals are zero. (`data/reproduce_cm_table_x1000000000_s51012026_20260720.csv`.)
- [EMPIRICAL: all 50 checkpoints $2\mathbin{\cdot}10^7\le x\le10^9$] Observed/integral-predicted ranges from $0.9956899$ at $2\mathbin{\cdot}10^7$ to $1.0002392$ at $4\mathbin{\cdot}10^8$.
- [EMPIRICAL: $x=10^9$] The run counts 1,548,766 quotient-prime events among 25,423,491 split primes versus 1,549,656.621 integral-predicted, giving ratio $0.9994253$; the direct split-prime-sum ratio is $0.9994797$.
- [EMPIRICAL: Python 3.13.4, Windows 11] The complete 50-row run took 148.7 seconds using a segmented prime sieve and an exact Cornacchia--Walsh trace backend.

## Session 5 theory closure

- [CITED] A 2025 fixed-curve paper determines the refined Koblitz constant only under an elliptic Elliott--Halberstam conjecture and a separate conjecture on the average growth of $N_p=\#E(\mathbb F_p)$. (Dey, Saha, Sivaraman, and Vatwani 2025, DOI 10.1016/j.jmaa.2024.129212.)
- [CITED] A current primary account still describes the refined Koblitz conjecture as open and proves unconditional moment results over curve families rather than a fixed-curve asymptotic. (Lee, Mayle, and Wang 2025, arXiv:2408.16641.)
- [CITED] Xie's unconditional 2025 CM result concerns bounded-almost-prime quotients over prime-power fields; it does not prove primality of $\#E(\mathbb F_p)/8$. (Xie 2025, arXiv:2504.18732.)
- [PROVED] For $E:y^2=x^3-x$ and a split prime $p=a^2+b^2$ normalized by $a\equiv1\pmod4$, Walsh's trace formula gives
  \[
  \#E(\mathbb F_p)=N(a+bi-1)\quad(p\equiv1\pmod8),
  \qquad
  \#E(\mathbb F_p)=N(a+bi+1)\quad(p\equiv5\pmod8).
  \]
  The complete derivation is in `THEORY_CLOSURE.md`.
- [PROVED] The $p\equiv1\pmod8$ quotient $\#E(\mathbb F_p)/8$ is even and is prime only at $p=17$; all other possible events are simultaneous prime values of $N(a+bi)$ and $N(a+bi+1)/8$ in the class $p\equiv5\pmod8$. (`THEORY_CLOSURE.md`.)
- [PROVED] This exact reduction separates the completed algebra and finite computation from Q026: the unresolved statement is a prime-pair distribution asymptotic, not a missing trace formula, local density, or test.
