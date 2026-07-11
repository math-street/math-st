---
attempt: A003
status: promising
---
# A003 - Bypass binary forms with a direct quaternary prime sampler

## Idea

- [PROVED] Proposition 3.8 admits an unconditional replacement, with running time polynomial in \(\log p\) and in the numerical value of \(\ell\), by sampling the rank-four norm lattice directly instead of restricting it to a binary form.
- [PROVED] The proof below covers every odd characteristic \(p\) and every prime \(\ell\ne p\); the special case \(\ell=2\) uses the quadratic-reciprocity supplement modulo eight.

## Prior art

- [CITED] For a left ideal \(I\) of a maximal order in \(B_{p,\infty}\), the normalized norm form \(Q=q_I\) is primitive, positive definite, integral, rank four, and has discriminant \(p^2\) (Wesolowski 2022, Lemma 2.4 and the paragraph preceding it).
- [CITED] Rouse 2018, Theorem 1 and its proof, gives an effective polynomial-in-level-and-discriminant crossover beyond which every strongly locally soluble integer is represented by an arbitrary primitive positive-definite quaternary form.
- [CITED] Rouse 2018 proves this by writing \(r_Q(n)=a_E(n)+a_C(n)\), giving a local-density lower bound for \(a_E(n)\), and bounding \(|a_C(n)|\) by a fixed power of the level and discriminant times \(d(n)\sqrt n\).
- [CITED] Goren--Love 2025 records that the theta series of a maximal order norm lattice has weight two and level \(p\), and that ideal lattices with maximal left and right orders are locally similar to such a maximal order.

## Candidate construction

- [PROVED] For odd \(\ell\), let \(M=8\ell\) and choose a primitive \(x\in I\) such that \(a=Q(x)\) is congruent to \(1\pmod8\), is nonzero modulo \(p\), and is a quadratic nonresidue modulo \(\ell\).
- [PROVED] The residue conditions modulo \(M\) can be found by enumerating four coordinates modulo \(M\), which is polynomial in the numerical value of \(\ell\), because the normalized norm lattice is locally the determinant form at every prime dividing \(M\).
- [PROVED] The condition \(Q(x)\not\equiv0\pmod p\) is enforced without enumerating modulo \(p\): add \(kM v\) for a vector \(v\) on which the reduced quadratic polynomial is nonzero and try three values of \(k\); a nonzero quadratic polynomial has at most two roots.
- [PROVED] For \(\ell=2\), take \(M=8\) and choose \(a=Q(x)\equiv3\) or \(5\pmod8\); the rest of the construction is identical.
- [PROVED] Define \(\Lambda=\mathbb Zx+MI\). If \(x\) extends to a basis of \(I\), then \([I:\Lambda]=M^3\).
- [PROVED] The restricted form \(Q_\Lambda\) is primitive: primes dividing \(M\) do not divide its first coefficient \(Q(x)\), while a prime not dividing \(M\) that divided every coefficient would also divide every coefficient of the primitive form \(Q\).
- [PROVED] Its discriminant is \(D_\Lambda=M^6p^2\), because the Gram determinant scales by the square of the lattice index.
- [PROVED] If the level of \(Q\) divides a fixed multiple of \(p\), then the level of \(Q_\Lambda\) divides the same fixed multiple of \(M^2p\): in a basis matrix \(T\) for \(\Lambda\subset I\), both \(MT^{-1}\) and its transpose are integral.

## Strong local solubility check

- [PROVED] For every prime \(r\nmid M\), the lattices \(\Lambda\otimes\mathbb Z_r\) and \(I\otimes\mathbb Z_r\) agree.
- [PROVED] If \(r\ne p\), the normalized local norm form is equivalent to the determinant form on \(M_2(\mathbb Z_r)\); a diagonal matrix gives a good-type representation of every \(r\)-adic integer.
- [PROVED] At \(r=p\), the reduced norm on the maximal order of the local division quaternion algebra maps units onto \(\mathbb Z_p^\times\), and the trace pairing at a unit supplies a nonzero derivative; hence every \(p\)-adic unit is strongly locally represented.
- [PROVED] For \(r\mid M\), every prime \(q\equiv a\pmod M\) satisfies \(q/a\in(\mathbb Z_r^\times)^2\): congruence modulo \(8\) handles \(r=2\), and congruence modulo \(\ell\) handles the odd prime \(r=\ell\).
- [PROVED] Thus \(kx\in\Lambda\otimes\mathbb Z_r\), with \(k^2a=q\), is a good-type local representation at every \(r\mid M\).
- [PROVED] Every prime \(q\equiv a\pmod M\), \(q\ne p\), therefore satisfies Rouse's strong local solubility condition for \(Q_\Lambda\).

## Density-to-sampling calculation

- [CITED] Rouse's effective strong-local argument implies that above a bound \(X_0\le (N(Q_\Lambda)D(Q_\Lambda))^C\), for an absolute constant \(C\), the cusp coefficient is at most half the Eisenstein coefficient after increasing the implicit constant.
- [PROVED] Rouse's local-density inequalities give
  \[
  r_{Q_\Lambda}(q)\ge c\,\frac{q}{\sqrt{D_\Lambda}}\frac{\varphi(N(Q_\Lambda))}{N(Q_\Lambda)}
  \]
  for candidate primes above that crossover, with an effective absolute \(c>0\).
- [PROVED] The elementary lower bound \(\varphi(N)/N\gg1/\log\log(N+3)\) makes this a polylogarithmic, rather than a power-sized, loss.
- [CITED] The Siegel--Walfisz theorem gives \(\gg X/(\varphi(M)\log X)\) primes \(q\in[X/2,X]\) with \(q\equiv a\pmod M\) once \(M\le(\log X)^A\) for fixed \(A\).
- [PROVED] Taking \(\log X\ge M^2\) puts the progression in that unconditional range while keeping the output length polynomial in the numerical value of \(\ell\).
- [PROVED] Summing the preceding representation lower bound over these primes gives at least
  \[
  \gg\frac{X^2}{\sqrt{D_\Lambda}\,\varphi(M)\log X\log\log(N(Q_\Lambda)+3)}
  \]
  prime-valued vectors in the radius-\(X\) ellipsoid.
- [PROVED] Voronoi-cell volume bounds show that the total number of lattice vectors with \(Q_\Lambda(y)\le X\) is \(O(X^2/\sqrt{D_\Lambda})\) once \(X\) exceeds the squared covering radius.
- [PROVED] Consequently a uniform vector in this ellipsoid is prime-valued with probability at least
  \(1/\operatorname{poly}(\ell,\log X,\log p)\).
- [PROVED] For odd \(\ell\), every value of \(Q_\Lambda\) modulo \(\ell\) is a square multiple of the nonresidue \(a\), so a prime output \(q\) satisfies \((q/\ell)=-1\); since \(q\equiv1\pmod4\), quadratic reciprocity gives \((\ell/q)=-1\).
- [PROVED] For \(\ell=2\), every prime output is congruent to \(3\) or \(5\pmod8\), so the supplementary law gives \((2/q)=-1\).

## Resolution of the proof obligations

- [CITED] Kannan 1987 gives exact CVP in \(n^{O(n)}\) arithmetic operations, hence polynomial input-bit complexity in fixed rank four.
- [PROVED] Wesolowski's Voronoi rejection proof extends verbatim to rank four once fixed-rank CVP is available: sampling the ellipsoid enlarged by the covering radius assigns the full equal-volume Voronoi cell to every accepted lattice point, and the acceptance probability is bounded below by \(((r-\mu)/(r+\mu))^4\).
- [PROVED] Sampling the continuous ellipsoid to polynomially many random bits changes the output by negligible statistical distance because cell boundaries have measure zero and the requested success probability is only inverse polynomial.
- [CITED] Rouse 2018 states the strong-local case uniformly in the level and discriminant of an arbitrary primitive quaternary form and explicitly says that this case is effective.
- [PROVED] Fixing \(\epsilon>0\) in Rouse's proof and increasing the crossover by a constant factor makes \(|a_C(q)|\le a_E(q)/2\) at a fixed-power bound in \(N(Q_\Lambda)D(Q_\Lambda)\); no individual-form parameter remains.
- [CITED] Bennett--Martin--O'Bryant--Rechnitzer 2018, Theorems 1.1--1.3, give explicit prime-counting errors for every coprime progression modulo \(M\), with a valid threshold at most \(\exp(0.03\sqrt M\log^3M)\) when \(M>10^5\).
- [PROVED] Choosing \(\log X\ge M^2\) makes the main term in the interval \([X/2,X]\) dominate their explicit error and retains output length polynomial in the numerical value of \(\ell\).
- [PROVED] These resolutions are independent of Brandt mixing, so A002's failure does not propagate to this attempt.

## Outcome

- [PROVED] The construction gives an unconditional replacement for Wesolowski's Proposition 3.8 with expected running time polynomial in \(\log p\) and in the numerical value of \(\ell\).
- [PROVED] It removes D2 from the smooth-path proof: a uniform vector sampled from \(Q_\Lambda(y)\le X\) yields the required equivalent prime-norm ideal with inverse-polynomial success probability.
- [PROVED] The attempt does not prove the full equivalence: the prescribed-norm equation in Algorithm 2, Step 9, still depends on D3 and D4, and the special-model construction still depends on D1.

## Toy refutation attempt

- [EMPIRICAL: p<=31, ell in {3,5}, q<=3000] Across 22 maximal-order or seeded prime-ideal lattices, the residue-lattice discriminant was always \((8\ell)^6p^2\), and all prime-valued vectors had \((\ell/q)=-1\); no reciprocity violation occurred (`code/measure_quaternary_prime_sampler.py`, `data/measure_quaternary_prime_sampler_p31_ells3-5_x3000_20260711.csv`).
- [EMPIRICAL: p<=31, ell in {3,5}, q<=3000] The observed value of \(\Pr[Q_\Lambda(v)\text{ prime}]\log X\) ranged from 0.832 to 1.815, with mean 1.276 over the 22 cases.
- [EMPIRICAL: p<=31, ell in {3,5}, q<=3000] Coverage of admissible progression primes ranged from 0.10 to 0.778, confirming that small cutoffs are below a uniform all-primes representation regime.
- [EMPIRICAL: p in {7,11}, ell=3, 250<=X<=4000] At the largest cutoff, \(\Pr[Q_\Lambda(v)\text{ prime}]\log X\) lay between 0.991 and 1.079 over the four order/ideal cases, while admissible-prime coverage lay between 0.75 and 0.824.
- [PROVED] These computations try to falsify the residue and density mechanism but do not test Rouse's asymptotic crossover or prove a worst-case sampler.
- [PROVED] The original broader grid \(p\le59\), \(\ell\le7\), \(X=5000\) exceeded the 120-second timebox because the first implementation used symbolic matrix multiplication inside the enumeration loop; replacing that loop by integer arithmetic reduced the recorded 22-case grid to 27.84 seconds.
