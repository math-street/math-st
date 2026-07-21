---
attempt: A010
status: dead
---
# A010 - Exponent-vector and logarithmic-lattice smooth finders

## Idea

[CONJECTURE] Represent a candidate as
$N=\prod_{p\le y}p^{e_p}$ and solve
$\sum e_p\log p\in[\log X,\log(X+X^{3/4})]$ by lattice reduction or
subset-product methods in time polynomial in $\log X$.

## Prediction and decision rule

[CONJECTURE] A fixed number of primes gives too few exponent vectors for the
required relative accuracy, whereas using all primes up to
$y=(\log X)^K$ makes the dimension grow polynomially and leaves a hard
high-density subset-product search.  The prediction is refuted by a proved
polynomial-time algorithm with worst-case success for every interval in the
A007 family, or by a cited theorem whose stated parameters imply one.

## Plan

1. [PROVED] Quantify the best resolution obtainable by enumerating exponent
   vectors over a fixed number of primes.
2. [PROVED] Audit lattice, meet-in-the-middle, and smooth-subsum algorithms
   when the number of allowed primes grows.
3. [PROVED] Separate rigorous worst-case algorithms from heuristic factoring
   relation-generation methods.

## Prior art boundary

[CITED] Lagarias--Odlyzko 1985 define the density of a subset-sum instance by

$$
 d=\frac{n}{\log_2(\max_i a_i)}
$$

[CITED] They prove recovery for almost all instances below a fixed low-density
threshold.  Their algorithm always terminates in polynomial time, but its
success theorem is distributional and low-density rather than a worst-case
guarantee for structured logarithms.

[CITED] Bringmann 2017 gives a randomized subset-sum algorithm with running
time $\widetilde O(n+t)$ for positive integer weights and target $t$.  This is
near-linear in the numerical target and therefore pseudopolynomial, not
polynomial in $\log t$.

[CITED] Hittmeir 2023 explicitly presents Smooth Subsum Search as a heuristic
for producing smooth polynomial values in practical integer factorization.
It supplies neither an every-interval theorem nor a worst-case polynomial-time
finder for an already specified interval.

## Bounded-support products cannot cover every prime center

[PROVED] Fix constants $K,k,C>0$, let $L=\log X$, and put $y=L^K$.
Consider all integers $N\in[X/2,3X]$ that are $y$-smooth and supported on at
most $k$ distinct primes.  Every exponent is $O(L)$, while there are at most
$\pi(y)=O(L^K)$ eligible primes.  Consequently the number of such products is
at most

$$
 \sum_{j=0}^k {\pi(y)\choose j} O(L)^j=L^{O_{K,k}(1)}.
$$

[CITED] The prime number theorem gives

$$
 \#\{r\text{ prime}:\sqrt X\le r\le\sqrt{2X}\}
   =\Theta\!\left(\frac{\sqrt X}{L}\right).
$$

[PROVED] For one fixed $N\asymp X$, the condition

$$
 |N-r^2|\le C r^{3/2}
$$

[PROVED] This condition restricts $r$ to an interval of length
$O_C(X^{1/4})$.  This follows from
$|r-\sqrt N|=|r^2-N|/(r+\sqrt N)$ and $r,\sqrt N\asymp\sqrt X$.
Thus all bounded-support products together cover at most
$X^{1/4}L^{O_{K,k}(1)}=o(\sqrt X/L)$ prime centers in the displayed dyadic
block.

[PROVED] For every sufficiently large $X$, some prime
$r\in[\sqrt X,\sqrt{2X}]$ therefore has no $L^K$-smooth bounded-support
product in its central surface interval.  In particular, enumerating exponent
vectors with any globally bounded number of nonzero coordinates cannot be an
every-prime construction, even if the supporting primes may be selected from
the entire growing factor base after seeing $r$.

## Growing support becomes an exponentially precise subset sum

[PROVED] An unrestricted exponent vector can be written as a zero-one subset
sum by giving prime $p\le y$ up to
$\lfloor\log(3X)/\log p\rfloor$ copies of the real weight $\log p$.  If $m$
is the resulting number of items, then

$$
 \pi(y)\le m\le O(L\pi(y)),
 \qquad L^{K+o(1)}\le m\le L^{K+1+o(1)}.
$$

[CITED] The second pair of bounds uses the prime number theorem.  In
particular, $m$ is polynomial in the original input length and grows faster
than $L$ when $K>1$.

[PROVED] For an interval of length $H=\Theta(X^{3/4})$ near $X$, its
logarithmic width is

$$
 \Delta=\log(1+H/X)=\Theta(X^{-1/4}).
$$

[PROVED] If the $m$ logarithmic weights are rounded after multiplication by $Q$, a
worst-case rounding guarantee needs $m/Q=O(\Delta)$, hence
$Q=\Omega(mX^{1/4})$.  At the minimal safe scale
$Q=\Theta(mX^{1/4})$, the corresponding integer target has size

$$
 t=\Theta(Q L)=X^{1/4}L^{O_{K}(1)},
$$

[PROVED] This numerical target is exponential in the input length $L$; any
larger safe rounding scale only increases it.

[PROVED] Substituting this target into Bringmann's
$\widetilde O(n+t)$ bound gives exponential time in $L$.  This conclusion is
about the standard safe rounding reduction; it is not a lower bound against
every algorithm that might exploit the special logarithmic weights directly.

[PROVED] At the minimal safe scale $Q=\Theta(m/\Delta)$, the rounded instance
has

$$
 \log_2(\max_i a_i)=\Theta(L),\qquad
 d=\frac{m}{\log_2(\max_i a_i)}\longrightarrow\infty
$$

[PROVED] For every fixed $K>1$, this density tends to infinity.  The instance
is therefore outside the low-density regime of the
Lagarias--Odlyzko success theorem.  Moreover, repeated rounded copies of
$\log p$ form a highly structured instance rather than the paper's almost-all
ensemble.

## Outcome

[PROVED] The prediction was confirmed for the audited generic routes.
Bounded-support exponent searches provably miss infinitely many prime centers;
unrestricted support restores enough representations only by entering a
high-density, exponentially precise subset-sum instance for which the checked
pseudopolynomial and low-density lattice theorems give no polynomial-time
guarantee.

[PROVED] This is not an impossibility theorem for all exponent-vector
algorithms.  A specialized algorithm using Diophantine structure of prime
logarithms, or a different representation of smooth values, is not covered.

## Post-mortem

**Why it failed:** [PROVED] Polynomially many bounded-support products cannot
cover the $\Theta(\sqrt X/L)$ relevant prime centers, while a faithful integer
encoding of the full factor base must resolve a relative window of width
$X^{-1/4}$.

**What transfers:** [PROVED] Any future smooth-order finder must explain how
it handles both growing support and exponential logarithmic precision without
paying for the numerical subset-sum target or assuming a random low-density
instance.

**Would it work under different assumptions?** [CONDITIONAL: a polynomial-time
oracle for the structured logarithmic interval-subset-sum instance] Yes.  The
oracle would return the exponent vector of a smooth order, after which A007's
Weil-polynomial step applies; the independent explicit-surface realization
gap would remain.
