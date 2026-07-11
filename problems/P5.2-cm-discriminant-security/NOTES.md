# Notes - P5.2

## Stable facts

- [PROVED] On $E:y^2=x^3+b$ over a prime field containing a primitive cube root $\zeta$, the map $\psi(x,y)=(\zeta x,-y)$ fixes the identity, has order six, and satisfies $\psi^2-\psi+[1]=0$. Substitution proves that the image remains on $E$; iterating the coordinates gives $\psi^3=[-1]$; and the displayed endomorphism equation follows by replacing $\psi=-\phi$ in $\phi^2+\phi+[1]=0$.
- [PROVED] On $E:y^2=x^3+ax$ over a prime field containing $i^2=-1$, the map $\psi(x,y)=(-x,iy)$ fixes the identity, has order four, and satisfies $\psi^2+[1]=0$, directly by two coordinate applications.
- [CITED] Gallant, Lambert, and Vanstone (CRYPTO 2001, LNCS 2139) give these explicit $j=0$ and $j=1728$ endomorphisms and prove that on a prime-order invariant subgroup they act as scalars satisfying the corresponding quadratic congruences.
- [CITED] For an ordinary elliptic curve over a finite field, the geometric endomorphism ring is an order in an imaginary quadratic field (Waterhouse 1969, *Annales scientifiques de l'Ecole Normale Superieure*).
- [PROVED] The tested maps generate the maximal quadratic orders of discriminants $-3$ and $-4$: their monic polynomials have those discriminants, and an order containing a maximal order equals it. The nonzero traces in the validation table certify that all eight concrete curves are ordinary by the cited finite-field trace criterion.

## Validated constructions

- [EMPIRICAL: p in {4057, 16381, 65437, 261673}; 32 seeded map checks per curve] Exhaustive point enumeration and the independent Hasse-interval/BSGS counter agreed on every full order; subgroup annihilation, scalar eigenvalue, characteristic equation, and unit exponent checks all passed. See `data/measure_unit_rho_table_r20_b12-14-16-18_t200_s52022026_20260707_validation.csv`.

| bits | $p$ | $D$ | curve coefficients $(a,b)$ | $#E(\mathbb F_p)$ | prime $r$ | unit order |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 4057 | -3 | (0,5) | 4153 | 4153 | 6 |
| 12 | 4057 | -4 | (5,0) | 4106 | 2053 | 4 |
| 14 | 16381 | -3 | (0,11) | 16633 | 16633 | 6 |
| 14 | 16381 | -4 | (2,0) | 16202 | 8101 | 4 |
| 16 | 65437 | -3 | (0,2) | 65068 | 16267 | 6 |
| 16 | 65437 | -4 | (3,0) | 65896 | 8237 | 4 |
| 18 | 261673 | -3 | (0,10) | 262519 | 262519 | 6 |
| 18 | 261673 | -4 | (5,0) | 261538 | 130769 | 4 |

## Unit-orbit ceiling

### Theorem (finite unit action in the ideal-random-mapping model)

- [PROVED] Let $G=\langle P\rangle$ have prime order $r$, and let a cyclic endomorphism action be scalar multiplication by $\mu\in\mathbb F_r^*$ of exact order $m$. Then its action is free on $G\setminus\{0\}$, and the quotient has exactly $1+(r-1)/m$ orbits.
- [PROVED] Freeness follows because $\mu^j s=s$ with $s\ne0$ implies $\mu^j=1$; orbit-stabilizer then gives $(r-1)/m$ nonzero orbits plus the identity orbit.
- [CITED] An ideal random mapping on a set of size $N$ has expected first-repeat work asymptotic to $\sqrt{\pi N/2}$ (Harris 1960, as used in Wang-Zhang 2011, IACR ePrint 2011/008).
- [PROVED] Under that model, quotienting changes $N=r$ to $N=1+(r-1)/m$, so the asymptotic speedup tends to $\sqrt m$; it changes only the multiplicative constant whenever $m$ is fixed.
- [PROVED] A unit in an imaginary quadratic order has order at most six: a primitive $n$-th root in a quadratic field requires $\varphi(n)\le2$, hence $n\in\{1,2,3,4,6\}$. Therefore unit-orbit rho on an ordinary CM elliptic curve has an idealized speedup ceiling of $\sqrt6$, attained only by the discriminant $-3$ unit group; discriminant $-4$ gives at most $2$, and every other imaginary quadratic order gives at most $\sqrt2$ from negation.
- [PROVED] This theorem is a ceiling for finite **unit** actions and an ideal-random-mapping cost model, not a proof that small CM discriminant cannot aid any algorithm.

## Measurements

- [EMPIRICAL: 3,200 recovered DLPs; p=4057..261673; r=2053..262519] With a collision table and the same 20-adding transition design in both arms, the ratio of mean online transitions was 2.424-2.664 for $D=-3$ and 1.853-2.186 for $D=-4$. Every 95% paired-bootstrap interval contained the predictions $\sqrt6$ and $2$, respectively. See `data/measure_unit_rho_table_r20_b12-14-16-18_t200_s52022026_20260707_summary.csv`.
- [EMPIRICAL: four subgroup sizes and 200 trials per size] The fitted slope in $\log(\text{speedup})$ versus $\log r$ was $-0.0109$ with 95% bootstrap interval $[-0.0420,0.0209]$ for $D=-3$, and $-0.0385$ with interval $[-0.0731,-0.0027]$ for $D=-4$. Thus no growing advantage was detected over the tested range; residuals are stored beside the fit JSON.
- [PROVED] The collision-table variant uses memory proportional to the number of stored walk states, so this experiment isolates the orbit-space factor but is not a constant-memory Pollard-rho implementation.
- [EMPIRICAL: same curves, seeds, and 200 trials per size] The naive constant-memory Floyd walk suffered growing zero-denominator cycle overhead: at the largest size its mean-work ratio was only 0.916 for $D=-3$ and 0.617 for $D=-4$, with mean quotient restarts 6.76 and 8.79. See `data/measure_unit_rho_b12-14-16-18_t200_s52022026_20260702_summary.csv`.
- [EMPIRICAL: same curves, seeds, and 200 trials per size] The attempted history-local doubling escape was worse, reaching mean transition counts 36,878 and 32,470 at the largest $D=-3$ and $D=-4$ cases. See `data/measure_unit_rho_escape_b12-14-16-18_t200_s52022026_20260707_summary.csv` and A002.
- [CITED] Fruitless cycles and the need for a carefully designed deterministic escape or distinguished-point strategy are established for negation-map rho by Bos-Kleinjung-Lenstra (ANTS 2010), Bernstein-Lange-Schwabe (PKC 2011; ePrint 2011/003), and Wang-Zhang (ePrint 2011/008).

## Boundary beyond units

- [CITED] A general efficient endomorphism acts as scalar multiplication $[\lambda]$ on an invariant prime-order cyclic subgroup; GLV uses the quadratic relation to accelerate scalar multiplication (Gallant-Lambert-Vanstone 2001).
- [PROVED] The image $\phi(P)=[\lambda]P$ supplies no second independent group direction: every expression in $P$ and $\phi(P)$ remains a scalar multiple of $P$.
- [PROVED] Under P1.5's operational definition, $\phi:\langle P\rangle\to\langle P\rangle$ is not a transfer to an easier group: even when injective, its target is the same ECDLP subgroup and no subexponential target algorithm is supplied.
- [PROVED] The $\sqrt6$ proof does not cover a non-unit $\phi$: its eigenvalue $\lambda\bmod r$ is not a geometric unit, so the imaginary-quadratic root-of-unity classification supplies no bound on its modular multiplicative order. The present canonicalizer costs linear time in whatever that order is.

> **Resolved boundary.** [PROVED] A003 supplies the requested $D=-7$ construction and a tight lower bound in the sequential successor/comparison model, resolving Q020 as stated for that model. Richer exponent-free or batched access remains open and is logged as Q024.

## The discriminant -7 non-unit case

- [CITED] GLV Example 5 (Gallant-Lambert-Vanstone 2001, CRYPTO 2001) gives the degree-two map on $E_3:y^2=x^3-3x^2/4-2x-1$ with $\omega=(1+\sqrt{-7})/2$ and $a=(\omega-3)/4$:
  $$x'=\omega^{-2}\frac{x^2-\omega}{x-a},\qquad y'=\omega^{-3}y\frac{x^2-2ax+\omega}{(x-a)^2}.$$
- [PROVED] Substituting $x_{\rm old}=x+1/4$ gives the short model $y^2=x^3-35x/16-49/32$; direct rational-function evaluation and the exceptional denominator case implement this map in `code/cm_nonunit.py`.
- [PROVED] On every invariant prime-order subgroup $\langle P\rangle$ of order $r$, the tested action $\phi(P)=[\lambda]P$ obeys $\lambda^2-\lambda+2=0\pmod r$ because the point relation is $\phi^2-\phi+[2]=0$.
- [EMPIRICAL: five curves, 80 normalized points, Python 3.13.4] The following independently counted cases passed 32 seeded full-curve characteristic checks each; every normalization returned the checked exponent and used exactly $m-1$ map evaluations. Data: `data/measure_nonunit_orbits_b10-12-14-16-18_n16_s72022026_20260711_{raw,summary,validation}.csv`.

| bits | $p$ | $r$ | $\lambda$ | $m=\operatorname{ord}_r(\lambda)$ | $(r-1)/m$ | $m-1$ evaluations | ideal $\sqrt m$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 977 | 233 | 203 | 116 | 2 | 115 | 10.770 |
| 12 | 4013 | 991 | 45 | 495 | 2 | 494 | 22.249 |
| 14 | 16249 | 4057 | 3635 | 1352 | 3 | 1351 | 36.770 |
| 16 | 64661 | 16139 | 1546 | 8069 | 2 | 8068 | 89.828 |
| 18 | 262007 | 32831 | 25875 | 16415 | 2 | 16414 | 128.121 |

### Theorem (least representative in the sequential evaluator model)

- [PROVED] Fix an opaque cycle $x,T(x),\ldots,T^{m-1}(x)$ of known length $m$. In a model that exposes only a successor query $T$ and comparisons of opaque labels, every deterministic algorithm that always returns the least label needs at least $m-1$ successor queries in the worst case.
- [PROVED] After fewer than $m-1$ queries, the algorithm has seen fewer than all $m$ labels. An adversary can assign an unseen label below every seen label without changing any query answer or comparison already observed, so the algorithm's selected seen label is not always minimal. Conversely, $m-1$ queries expose every cycle element and suffice. Hence the query complexity is exactly $m-1$.
- [PROVED] The lower bound applies to the exhaustive least-coordinate canonicalizer in `cm_nonunit.py`; it does not apply to a richer representation that exploits algebra beyond sequential map evaluation and label comparison.

### Theorem (exponent-returning canonicalization reduces ECDLP)

- [PROVED] Let $G=\langle P\rangle$ have prime order $r$, let $\lambda\in\mathbb F_r^*$ have order $m$, and put $q=(r-1)/m$. Suppose $C(X)=(R,j)$ returns a common representative for the orbit of $X$ and an exponent satisfying $R=[\lambda^j]X$. Given a primitive root $g\bmod r$, ECDLP requires at most $q+1$ calls to $C$, $O(q)$ stored representatives, and ordinary scalar arithmetic.
- [PROVED] The scalars $g^i$, $0\le i<q$, represent all cosets of $\langle\lambda\rangle$. Precompute $C([g^i]P)=(R_i,j_i)$. For $Q=[s]P$, compute $C(Q)=(R,j)$ and find the unique $i$ with $R_i=R$. Equality gives $[\lambda^{j_i}g^i]P=[\lambda^j s]P$, so $s=\lambda^{j_i-j}g^i\pmod r$.
- [PROVED] If $q$ and the running time of $C$ are polynomial in $\log r$, this is a polynomial-time ECDLP algorithm; if $m=r-1$, then $q=1$ and just $C(P)$ and $C(Q)$ recover the logarithm. A quotient-rho implementation needs the exponent or an equivalent coefficient transformation, so such a normalizer cannot be counted as cost-free when assessing its speedup.
- [PROVED] This reduction does not construct a fast $C$, prove that the measured orders grow asymptotically, or rule out richer exponent-free or batched methods. That remaining boundary is Q024.

### Theorem (addition does not descend to scalar-orbit classes)

- [PROVED] Let the nontrivial subgroup $H\le\mathbb F_r^*$ act by scalar multiplication on the additive group $G=\langle P\rangle$ of prime order $r$, and let $\pi:G\to G/H$ be the orbit map. There is no binary operation $\oplus$ on $G/H$ satisfying $\pi(X+Y)=\pi(X)\oplus\pi(Y)$ for every $X,Y\in G$.
- [PROVED] Choose $h\in H$ with $h\ne1$. The points $P$ and $[h]P$ have the same orbit, so well-definedness with $Y=-P$ would equate the orbits of $P-P=0$ and $[h]P-P=[h-1]P$. The first orbit is the singleton $\{0\}$ and the second is nonzero because $r$ is prime and $h\ne1$, a contradiction.
- [PROVED] Consequently, orbit classes alone cannot implement the addition of a fixed r-adding table entry: the result depends on the relative orientation of the chosen representatives.

### Consequence for coefficient-tracking rho

- [PROVED] In the standard algebraic coefficient model, a rho state carries the formal invariant $X=[a]P+[b]Q$, represented by $a+bz\in\mathbb F_r[z]$ before specializing $Q=[s]P$. Adding a table entry $(u,v)$ gives $(a+u)+(b+v)z$; normalizing the resulting point to $R=[h]X$ forces the new formal coefficients to be $h(a+u)$ and $h(b+v)$. Thus a correct canonicalized transition must retain $h$ or information that recovers $h$.
- [PROVED] If two un-oriented states collide only as orbit classes, their known coefficients give
  $$a+bs=h(c+ds)\quad\text{for some }h\in H.$$
  For each $h$ with $b-hd\ne0$, this permits the candidate $s=(hc-a)/(b-hd)$, so one collision can leave as many as $m=|H|$ candidates instead of the single linear solution supplied by an oriented collision.
- [PROVED] Keeping the unnormalized point and its coefficients while using a normalized point only for partition selection preserves correctness, but exact-state collision detection then occurs in $G$, not $G/H$; declaring orbit collisions again produces the unresolved $H$-membership equation above.

### Theorem (a returned multiplier is already sufficient for the reduction)

- [PROVED] The canonicalizer-to-ECDLP reduction does not require an exponent $j$. If $C(X)=(R,h)$ returns $h\in H$ with $R=[h]X$, precompute $C([g^i]P)=(R_i,h_i)$ for $0\le i<q=(r-1)/m$. For $C(Q)=(R,h)$, the unique equality $R=R_i$ gives $s=h^{-1}h_i g^i\pmod r$ directly.
- [PROVED] Therefore any polynomial-time multiplier-returning canonicalizer with polynomially many quotient orbits is a polynomial-time ECDLP algorithm. A batch routine returning multipliers yields the same reduction in one requested batch containing the $q$ transversal inputs and $Q$.
- [PROVED] This resolves Q024 for standard algebraic coefficient-tracking rho and multiplier-returning batches. A nonlinear solver that combines several orientation-free $H$-membership constraints without recovering individual multipliers is not excluded; that precise gap is Q025.

## Working definitions

- A **unit orbit** is the set obtained from a subgroup point by applying the finite group generated by the explicit CM unit and negation.
- A **quotient walk** stores a canonical representative of each unit orbit together with transformed linear coefficients.
