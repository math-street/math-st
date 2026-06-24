# P5.1 — Koblitz's conjecture on prime curve orders

## Formal statement

- [CONJECTURE] Let $E/\mathbb{Q}$ be a non-CM elliptic curve and let $N_E$ be its conductor. For a curve with no congruence obstruction to prime orders,
  
  \[
  \#\{p\le x: p\nmid N_E,\ \#E(\mathbb{F}_p)\text{ is prime}\}
  \sim C_{E,1}\frac{x}{(\log x)^2}.
  \]
  
  The corrected constant $C_{E,1}\ge 0$ is defined from the adelic Galois image, and it can vanish. A positive-constant version also assumes that $E$ is not $\mathbb{Q}$-isogenous to a curve with nontrivial rational torsion. (Koblitz 1988, *Pacific Journal of Mathematics* 131; Zywina 2011, *International Journal of Number Theory* 7, arXiv:0909.5280.)

- [CONJECTURE] Zywina's refined formulation fixes an integer $t\ge 1$ and predicts the same asymptotic for primes such that $\#E(\mathbb{F}_p)/t$ is an integer and prime, with constant $C_{E,t}$. (Zywina 2011, *International Journal of Number Theory* 7, arXiv:0909.5280.)

## Session target

- [EMPIRICAL: all good primes $5\le p\le 2^{17}$] Measured prime-order reductions for three non-CM curves representing trivial, rational 2-, and rational 3-torsion.
- [CITED] Implement the universal Euler product and the explicit $10/9$ entanglement correction for Zywina's Serre-curve example $y^2=x^3+6x-2$. (Zywina 2011, Proposition 4.2 and equation (5.1), arXiv:0909.5280.)
- [CITED] Record exactly where the zero-free/GRH hypothesis enters the strongest fixed-curve sieve results. (David and Wu 2012, *Forum Mathematicum* 24, arXiv:0812.2860.)

## Falsifiers

- [HEURISTIC] For $y^2=x^3+6x-2$, a sustained measured/predicted ratio outside the experiment's stated counting interval would challenge the implemented constant or point counter; this heuristic is falsified by such a discrepancy after independent validation.
- [PROVED] For the chosen rational 2- and 3-torsion curves, every good reduction preserving that torsion has composite order once the order exceeds the torsion prime; a single contrary computed reduction would falsify the implementation, because reduction injects prime-to-$p$ rational torsion.
