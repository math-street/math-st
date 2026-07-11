---
attempt: A004
status: dead
---
# A004 - Remove the coefficient p from the split norm equation

## Idea

- [CONJECTURE] Replace the decomposition \(f(s,t)+p f(x,y)\) of the special-order norm by another integral two-binary-form parameterization in which every modulus is polylogarithmic in \(p\), so the unconditional Assing--Blomer--Li range applies.
- [CONJECTURE] A refuting test is an invariant forcing the ramified prime \(p\) into at least one coefficient, binary discriminant, or congruence modulus of every such parameterization.

## Prior art

- [CITED] Wesolowski 2022, Lemma 2.3, uses \(B_{p,\infty}=(-q,-p)\) and obtains
  \(\operatorname{Nrd}(s+t\omega+xj+y\omega j)=f(s,t)+p f(x,y)\).
- [CITED] Theorem 5.1 and Corollary 5.8 then call the uniform Titchmarsh estimate with the parameter \(b=p\).
- [CITED] Assing--Blomer--Li 2020, Theorem 2.1, is unconditional only when all auxiliary moduli are bounded by fixed powers of the logarithm of the sampled scale.

## Invariant obstruction

- [PROVED] For odd \(p\), a quaternion Hilbert symbol \((a,b)_{\mathbb Q_p}\) with both \(a\) and \(b\) \(p\)-adic units is split; therefore a presentation of the division algebra \(B_{p,\infty}\) must put odd \(p\)-adic valuation into at least one defining parameter.
- [PROVED] If an imaginary quadratic subfield \(K\) has discriminant coprime to \(p\), then an orthogonal decomposition \(B=K\oplus Kj\) must place the ramified prime in \(j^2\), producing a coefficient divisible by \(p\) in the second binary norm block.
- [PROVED] If the coefficient of the second block is made coprime to \(p\), then the quadratic subfield must instead be ramified at \(p\), so the discriminant/congruence modulus of its binary norm form is divisible by \(p\).
- [PROVED] The same conclusion follows integrally from determinants: for a block form \(F_1\oplus bF_2\), its rank-four Gram determinant is \(b^2\det(F_1)\det(F_2)\), up to a fixed normalization and the square of a lattice index.
- [PROVED] Since a maximal order norm lattice has discriminant \(p^2\), at least one of \(b\), \(\det(F_1)\), \(\det(F_2)\), or the lattice index is divisible by \(p\).
- [PROVED] Each of these locations reappears as an auxiliary modulus or as a parameter whose stated processing cost is polynomial in its numerical value in Wesolowski's Theorem 5.1 architecture.

## Complexity consequence

- [PROVED] If a modulus divisible by \(p\) must satisfy the unconditional condition \(m\le(\log X)^C\), then \(\log X\ge p^{1/C}\).
- [PROVED] This output length is exponential in the problem input length \(\log p\).
- [PROVED] Moving \(p\) from the coefficient \(b\) into a binary discriminant therefore does not repair the reduction; it merely changes which parameter violates the unconditional range.

## Outcome

- [PROVED] No integral orthogonal \(2+2\) norm decomposition can make all parameters entering Theorem 5.1 polylogarithmic in \(p\).
- [PROVED] A basis change within the existing binary-form/Titchmarsh architecture cannot remove D3.
- [PROVED] A genuinely nonorthogonal rank-four representation theorem could evade this specific determinant bookkeeping, but it would no longer be an application of Theorem 5.1 or the checked Assing--Blomer--Li estimate.

## Post-mortem

**Why it failed:**

- [PROVED] Ramification at \(p\) is an invariant of the quaternion algebra, and an integral two-block norm presentation must expose it in a coefficient, block discriminant, or index.

**What transfers:**

- [PROVED] Future approaches should target the full quaternary norm equation or a different algebraic construction, not another basis for the same \(2+2\) split.

**Would it work under different assumptions?**

- [CONDITIONAL: power-modulus Titchmarsh estimate] Yes; the original proof works because GRH permits moduli that are fixed powers of the sampled scale.
