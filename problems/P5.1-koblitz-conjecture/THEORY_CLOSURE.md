# Theory closure boundary -- P5.1

## Verdict

- [CITED] The fixed-curve Koblitz asymptotic remains an open conjecture: Lee--Mayle--Wang describe it as open, while their unconditional results concern averages of constants over curve families and congruence classes. (Lee, Mayle, and Wang 2025, *Canadian Journal of Mathematics*, arXiv:2408.16641.)
- [CITED] The closest directly targeted 2025 fixed-curve result derives the refined constant only after assuming both an elliptic analogue of Elliott--Halberstam and a separate conjecture on the average growth of the reduction orders. (Dey, Saha, Sivaraman, and Vatwani 2025, *Journal of Mathematical Analysis and Applications* 546, article 129212.)
- [CITED] The 2025 unconditional advance for the CM curve $y^2=x^3-x$ proves bounded-almost-prime statements over prime-power fields, not primality of the order over $mathbb F_p$ and not the Koblitz asymptotic. (Xie 2025, arXiv:2504.18732.)
- [PROVED] Consequently, none of the primary results audited here supplies an unconditional fixed-curve prime-order asymptotic: the first is an average theorem, the second assumes two unproved inputs, and the third replaces prime values by bounded-almost-prime values.
- [EMPIRICAL: primary-source audit through 2026-07-20] Searches by title, conjecture name, prime-order terminology, and cited follow-up chains found no later primary source claiming the missing unconditional theorem.

## Exact CM prime-pair reduction

- [CITED] Let $E:y^2=x^3-x$, let $p>2$ be a rational prime with $p\equiv1\pmod4$, and choose $a,b\in\mathbb Z$ with $p=a^2+b^2$ and $a\equiv1\pmod4$.  Walsh's trace formula specializes to
  \[
  a_p=\begin{cases}
  2a,&p\equiv1\pmod8,\\
  -2a,&p\equiv5\pmod8.
  \end{cases}
  \]
  (Walsh 2022, Theorem 2.1.)
- [PROVED] Put $\varepsilon_p=1$ for $p\equiv1\pmod8$ and $\varepsilon_p=-1$ for $p\equiv5\pmod8$.  Then
  \[
  \#E(\mathbb F_p)
    =p+1-2\varepsilon_pa
    =(a-\varepsilon_p)^2+b^2
    =N_{\mathbb Z[i]/\mathbb Z}(a+bi-\varepsilon_p).
  \]
  **Proof.** Substitute $p=a^2+b^2$ and expand $(a-\varepsilon_p)^2$, using $\varepsilon_p^2=1$.
- [PROVED] The displayed order is divisible by $8$.  **Proof.** If $p\equiv1\pmod8$, then $a-1$ and $b$ are divisible by $4$, so the order is divisible by $16$.  If $p\equiv5\pmod8$, then $a+1\equiv b\equiv2\pmod4$, so their two squares are each $4\pmod{16}$ and their sum is $8\pmod{16}$.
- [PROVED] In the class $p\equiv1\pmod8$, the quotient $\#E(\mathbb F_p)/8$ is prime only for $p=17$, where it equals $2$.  **Proof.** The quotient is even, hence primality forces $\#E(\mathbb F_p)=16$.  The equation $(a-1)^2+b^2=16$, together with $4\mid a-1$ and $4\mid b$, gives $(a,b)=(1,\pm4)$ as the only case with $a^2+b^2$ prime, hence $p=17$.
- [PROVED] For every remaining possible event, $p\equiv5\pmod8$ and
  \[
  p=N(a+bi),\qquad
  \frac{\#E(\mathbb F_p)}8=\frac{N(a+bi+1)}8.
  \]
  Thus the CM Koblitz event is exactly a simultaneous two-prime norm pattern, apart from the proved exceptional event $p=17$.
- [PROVED] Writing $u=(a+1)/2$ and $v=b/2$ in the $p\equiv5\pmod8$ case gives
  \[
  \frac{\#E(\mathbb F_p)}8
   =\frac{u^2+v^2}{2}
   =\left(\frac{u+v}{2}\right)^2+\left(\frac{u-v}{2}\right)^2,
  \]
  because $u$ and $v$ are odd.  This makes the second prime value an explicit integral quadratic-form value.
- [HEURISTIC] The simultaneous primality condition is a Gaussian-integer analogue of a prime-pair problem and explains the observed parity barrier; this analogy would be falsified as an explanation of the asymptotic if a sieve using only divisibility data proved the required prime lower bound without an additional parity-breaking input.

## What is closed unconditionally in this repository

- [PROVED] The algebraic reduction above is unconditional once Walsh's cited trace theorem is accepted; it contains no GRH, Chebotarev, or distributional assumption.
- [EMPIRICAL: every split prime $5\le p\le10^9$] The audited program exhaustively finds 1,548,766 primes for which $\#E(\mathbb F_p)/8$ is prime among 25,423,491 split primes; every one of Zywina's 50 published checkpoints is reproduced exactly. (`code/reproduce_cm_table.py`; `data/reproduce_cm_table_x1000000000_s51012026_20260720.csv`.)
- [EMPIRICAL: Session 4 independent checks] Generic BSGS point counting, three sieve paths, three primality implementations, two quadratures, high-precision Euler products, and fixture mutation found no discrepancy in the finite computation. (`audits/SELF-CHECK-20260713.md`.)
- [EMPIRICAL: all 74,416 split primes $5\le p\le2,000,000$] An additional Session 5 check verified the norm identity, divisibility by $8$, and that the only $p\equiv1\pmod8$ prime quotient is $(p,\#E(\mathbb F_p)/8)=(17,2)$; a persistent regression repeats the identity through $10^5$.
- [CONDITIONAL: LMFDB's level-30 adelic generators and level declaration for 540.f2 are correct] Exact finite enumeration proves $\delta_{E,3}(90)=91/648$ and $C_{E,3}=(5824/5913)C$ for the recorded quotient case.

## The irreducible missing implication

- [CITED] David--Wu's effective Chebotarev input, even at GRH strength, yields an eight-almost-prime lower bound and a prime-order upper bound, but no prime-order lower bound. (David and Wu 2012, Theorems 1.1 and 1.3.)
- [CITED] Dey--Saha--Sivaraman--Vatwani obtain the conjectured refined constant only after adding an elliptic Elliott--Halberstam hypothesis and a conjecture controlling average growth of $N_p=\#E(\mathbb F_p)$. (Dey et al. 2025.)
- [PROVED] Therefore an unconditional proof still needs two logically separate ingredients: sufficiently uniform distribution of the divisibility conditions and an input that converts those conditions into an asymptotic for prime values rather than merely almost-prime values.  The first follows from the roles assigned to Chebotarev and Elliott--Halberstam in the cited works; the second follows from the explicit absence of a prime lower bound in David--Wu and the extra prime-value assumptions in Dey et al.
- [CONJECTURE] A fixed-curve proof can be completed by an unconditional theorem matching both of those roles with errors summable over the required sieve moduli; this is refuted if such estimates are proved yet the prime-order asymptotic still fails.

## Final classification

- [PROVED] There is no unresolved ambiguity about the repository's result: the exact algebraic reduction, finite computations, constants, tests, and source assumptions are closed and auditable.
- [CITED] There remains one external mathematical conjecture, Q026, because labeling it solved would contradict the 2025 primary literature and would promote finite evidence to an asymptotic theorem. (Dey et al. 2025; Lee, Mayle, and Wang 2025.)
