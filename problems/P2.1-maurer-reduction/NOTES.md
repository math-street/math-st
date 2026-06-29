# Notes

## Stable facts

### Exact requirement in repo notation

[PROVED] For a positive integer $N$, write $P^+(N)$ for its largest prime
factor, with $P^+(1)=1$, and call $N$ **$B$-smooth** when $P^+(N)\le B$.

[CITED] Let $G=\langle g\rangle$ have prime order $r$, let
$a=g^s$, and suppose an oracle returns
$\mathsf{DH}_g(g^u,g^v)=g^{uv}$. Maurer and Wolf's auxiliary-group theorem
applies with the sole prime divisor $p=r$ of $|G|$; the multiple-prime-factor
condition is vacuous (Maurer--Wolf 1999, Sections 3.1--3.4, Theorem 2).

[CITED] The needed auxiliary object may be any finite abelian group $H$ of
constant rank that is strongly algebraically defined over $\mathbb F_r$, has
known order $N$, and satisfies $P^+(N)\le B$ (Maurer--Wolf 1999, Definitions
3--4 and Theorem 2).

[CITED] An elliptic curve $E'/\mathbb F_r$ is such a group with rank at most
two and is strongly $(2,O((\log r)^2))$-algebraically defined (Maurer--Wolf
1999, Section 4.1.1).

[PROVED] Therefore the precise polynomial-time condition is

$$
  N=\#E'(\mathbb F_r),\qquad
  P^+(N)\le B=(\log r)^C
$$

for one fixed constant $C$, together with a curve equation and the exact value
of $N$ constructible in $\operatorname{poly}(\log r)$ time. The auxiliary
curve group itself need not be cyclic.

[PROVED] Once $N$ is known and promised $B$-smooth with
$B=(\log r)^C$, trial division by all integers through $B$ obtains its full
factorization in $\operatorname{poly}(\log r)$ time; requiring the
factorization separately does not strengthen the asymptotic condition.

### How the reduction uses the curve

[PROVED] A group element $g^x$ is an implicit representation of
$x\in\mathbb F_r$. Implicit addition is multiplication in $G$, implicit
multiplication is one call to $\mathsf{DH}_g$, negation is inversion in $G$,
and inversion of a nonzero field element is exponentiation to $r-2$ using
$O(\log r)$ implicit multiplications.

[CITED] Given implicit $x$, choose explicit random $e\in\mathbb F_r$, set
$X=x+e$, evaluate $D=X^3+AX+B$ implicitly, test whether $D$ is a quadratic
residue, and compute an implicit square root $Y$ when it is; this embeds $x$
as the implicit point $(X,Y)\in E'(\mathbb F_r)$. After making the point
explicit, extraction returns $x=X-e$ (Maurer--Wolf 1999, Sections 3.2--3.4
and 4.1.1).

[CITED] Generalized Pohlig--Hellman over the rank-at-most-two group
$E'(\mathbb F_r)$ makes the implicit point explicit using the known
factorization of $N$; its cost is polynomial in $\log r$ when
$P^+(N)=(\log r)^{O(1)}$ (Maurer--Wolf 1999, Theorem 2 and its proof).

[PROVED] Extraction yields $s\bmod r$, which is the unique discrete logarithm
in the prime-order input group. Thus a uniformly constructible auxiliary curve
meeting the condition gives a polynomial-time Turing reduction
$\mathrm{DLP}_G\le_T\mathrm{CDH}_G$.

### Existence versus construction

[CITED] Every elliptic-curve order over $\mathbb F_r$ lies in
$[r+1-2\sqrt r,r+1+2\sqrt r]$, and Maurer--Wolf state that every integer in
that interval occurs as the order of a cyclic elliptic curve over
$\mathbb F_r$ (Maurer--Wolf 1999, Section 4.1.2).

[CITED] Maurer--Wolf define $\nu(r)$ as the minimum largest-prime-factor among
integers in this Hasse interval and obtain a non-uniform reduction from a
curve supplied as side information; they explicitly leave the polylogarithmic
smoothness assertion as an assumption (Maurer--Wolf 1999, Definition 6,
Theorem 3, and Corollary 4).

[CITED] The 2026 all-interval theorem of Jain guarantees a $y$-smooth integer
only for $y$ at least
$\exp(C(\log x)^{2/3}(\log\log x)^{4/3})$ and interval length at least
$\sqrt{x}$ times a growing factor (Jain 2026, Theorem 1.2).

[PROVED] Jain's theorem does not establish the Maurer condition: a
polylogarithmic $y$ is asymptotically smaller than Jain's lower range, and the
Hasse interval has total length only about $4\sqrt r$.

## Search-cost heuristic

[HEURISTIC] Model sampled curve orders as independent integers near $r$ for
smoothness. This model is falsified at a tested parameter if the Wilson 95%
interval excludes the exact Hasse-interval integer rate and the observed rate
ratio is outside $[1/2,2]$; asymptotically it would be falsified by a proved
different curve-order smoothness law.

[CITED] The Dickman--de Bruijn approximation uses
$u=\log r/\log B$ and density $\rho(u)=u^{-u+o(u)}$ (Jain 2026, Section 3,
which recalls the standard global estimate).

[PROVED] Substituting $B=(\log r)^C$ into that approximation gives
$u=\log r/(C\log\log r)$.

[HEURISTIC] Consequently a random-order search needs
$\rho(u)^{-1}=r^{1/C+o(1)}$ candidates, which is exponential rather than
polynomial in the input length $\log r$. This prediction is refuted by a
proved polylogarithmic expected-candidate bound for the sampled curve family.

[HEURISTIC] The entire Hasse interval is expected to contain
$r^{1/2-1/C+o(1)}$ such integers, so existence can be plausible for $C>2$
even while blind sampling remains too expensive. This prediction is refuted
by a contrary short-interval theorem or asymptotic count.

### Exact lower bound in an independent-order oracle

[PROVED] Fix a prime $r$, a bound $B$, the inclusive integer Hasse interval
$I_r$, and its subset $S_B$ of $B$-smooth orders.  Put

$$
  \alpha=\frac{|S_B|}{|I_r|}.
$$

Define an idealized oracle by assigning every fresh curve label an independent
uniform element of $I_r$; querying a label again returns its already assigned
value.  Any randomized adaptive algorithm making at most $q$ distinct-label
queries has success probability at most

$$
  1-(1-\alpha)^q.
$$

[PROVED] To see this, first fix the algorithm's random coins.  Conditional on
any transcript containing only failures, the value at the next fresh label is
still independent and uniform, so its conditional failure probability is
$1-\alpha$.  Induction gives failure probability at least
$(1-\alpha)^q$; repeated labels and early stopping cannot improve it.
Querying $q$ fresh labels until the first hit attains equality, and averaging
over the fixed coins proves the randomized statement.

[PROVED] For $0<\alpha<1$, the least query budget attaining success at least
$\delta\in(0,1)$ is therefore

$$
  q_\delta=\left\lceil
    \frac{\log(1-\delta)}{\log(1-\alpha)}
  \right\rceil.
$$

The cases $\alpha=0$ and $\alpha=1$ respectively make success impossible and
make one query sufficient.

[PROVED] This theorem is exact only for the stated independent-order oracle.
Actual elliptic-curve orders are structured and non-uniform, and a strategy
may select coefficients using arithmetic information; the theorem is not a
lower bound for every real curve-construction algorithm.

[EMPIRICAL: exact smooth counts in one Hasse interval at each of 12--40 bits]
`random_order_lower_bound.py` evaluated the theorem without simulation.  The
following are the exact median and 95%-success budgets for the same prime
sequence used in A001.

| bits | $B=L^2$: $\alpha$ | $q_{0.50}$ | $q_{0.95}$ | $B=L^3$: $\alpha$ | $q_{0.50}$ | $q_{0.95}$ |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 0.42745 | 2 | 6 | 0.81176 | 1 | 2 |
| 16 | 0.26588 | 3 | 10 | 0.66178 | 1 | 3 |
| 20 | 0.15580 | 5 | 18 | 0.52357 | 1 | 5 |
| 24 | 0.09015 | 8 | 32 | 0.40896 | 2 | 6 |
| 28 | 0.05042 | 14 | 58 | 0.30776 | 2 | 9 |
| 32 | 0.02755 | 25 | 108 | 0.22442 | 3 | 12 |
| 36 | 0.01471 | 47 | 203 | 0.16297 | 4 | 17 |
| 40 | 0.00764 | 91 | 391 | 0.11719 | 6 | 25 |

[EMPIRICAL: exhaustive finite answer spaces in the test suite] Directly
counting all length-$q$ answer sequences for small $(|S_B|,|I_r|,q)$ matched
$1-(1-\alpha)^q$ exactly.  At 40 bits A001's first hits were 65 for $L^2$
and 6 for $L^3$, compared with idealized median budgets 91 and 6; this is a
consistency check, not evidence that real curve orders are independent.

## Experiment

[PROVED] `lib/curves.py::curve_order_bsgs` computes exact orders by obtaining
exact sampled-point orders with bounded BSGS on a curve and its quadratic
twist, then returning only when the resulting congruences leave one integer
in the Hasse interval. Its bounded discrete logarithms use
$O(r^{1/4})$ group operations, so it is measurement tooling rather than the
polylogarithmic point counter required by the target reduction.

[EMPIRICAL: 36 curves over 101 <= r <= 65519] The BSGS counter matched
exhaustive enumeration on every validation curve; see `lib/tests/test_curves.py`,
`code/tests/test_measure_smooth_orders.py`, and the recorded 16-bit manual
cross-check in Session 1.

[EMPIRICAL: one prime at each of 12,16,...,40 bits; 512 curves per prime]
The seeded run below measured the following success counts. `Interval rate`
is the exact proportion of $B$-smooth integers in the inclusive Hasse
interval; `Curve 95% CI` is Wilson's interval.

| bits | $B$ | successes / 512 | curve rate (95% CI) | interval rate | first hit | mean count ms |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 144 | 268 | 0.5234 (0.4802--0.5664) | 0.4275 | 1 | 0.088 |
| 12 | 1,728 | 461 | 0.9004 (0.8714--0.9234) | 0.8118 | 1 | 0.088 |
| 16 | 256 | 173 | 0.3379 (0.2983--0.3799) | 0.2659 | 2 | 0.185 |
| 16 | 4,096 | 376 | 0.7344 (0.6945--0.7708) | 0.6618 | 2 | 0.185 |
| 20 | 400 | 103 | 0.2012 (0.1687--0.2381) | 0.1558 | 8 | 0.289 |
| 20 | 8,000 | 292 | 0.5703 (0.5271--0.6125) | 0.5236 | 1 | 0.289 |
| 24 | 576 | 71 | 0.1387 (0.1114--0.1713) | 0.0902 | 1 | 0.476 |
| 24 | 13,824 | 233 | 0.4551 (0.4124--0.4984) | 0.4090 | 1 | 0.476 |
| 28 | 784 | 29 | 0.0566 (0.0397--0.0802) | 0.0504 | 2 | 0.789 |
| 28 | 21,952 | 178 | 0.3477 (0.3077--0.3899) | 0.3078 | 2 | 0.789 |
| 32 | 1,024 | 21 | 0.0410 (0.0270--0.0619) | 0.0275 | 31 | 4.686 |
| 32 | 32,768 | 121 | 0.2363 (0.2016--0.2750) | 0.2244 | 2 | 4.686 |
| 36 | 1,296 | 14 | 0.0273 (0.0164--0.0454) | 0.0147 | 12 | 10.502 |
| 36 | 46,656 | 97 | 0.1895 (0.1579--0.2257) | 0.1630 | 2 | 10.502 |
| 40 | 1,600 | 4 | 0.0078 (0.0030--0.0199) | 0.0076 | 65 | 20.252 |
| 40 | 64,000 | 52 | 0.1016 (0.0783--0.1308) | 0.1172 | 6 | 20.252 |

[EMPIRICAL: same run] Each field prime was the largest prime below the named
power of two that is congruent to $3\bmod4$; the experiment therefore measures
one reproducible prime sequence, not a distribution over primes.

[EMPIRICAL: same run] Every curve-to-integer rate ratio was between 0.867 and
1.859, so A001's pre-registered factor-two decision rule did not reject the
integer-smoothness model. Several small-size baselines nevertheless fall
outside the corresponding Wilson interval, so equality of the two
distributions was not established.

[EMPIRICAL: same run] At 40 bits, point counting 512 curves took 10.37 seconds;
the complete run, including exact interval baselines for both bounds, took
20.67 seconds. The raw and summary data are in
`data/measure_smooth_orders_b12-16-20-24-28-32-36-40_t512_e2-3_s21012026_20260629_{raw,summary}.csv`.

## CM route

### A minimal sufficient number-theory condition

[PROVED] Put $L=\lceil\log_2 r\rceil$.  For fixed constants $C,K>0$, define
$\mathsf{SCM}_{C,K}(r)$ to mean that there are a negative fundamental
discriminant $D$ and integers $t,v$ satisfying

$$
  |D|\le L^K,\qquad 4r=t^2-Dv^2,\qquad
  P^+(r+1-t)\le L^C.
$$

[CITED] The norm equation is the ordinary-CM reachability criterion used by
Muzereau--Smart--Vercauteren (2004, Section 5), and a root of the corresponding
class polynomial modulo $r$ supplies a CM $j$-invariant (Enge 2009, Section
2).

[PROVED] If $\mathsf{SCM}_{C,K}(r)$ holds, its integer witness can be found in
randomized expected $\operatorname{poly}(L)$ time: enumerate the $O(L^K)$
negative fundamental discriminants, solve each norm equation with Cornacchia
and randomized modular square roots, and trial-divide every candidate order
through $L^C$.  The exceptional unit groups for $D=-3,-4$ contribute only the
finite extra traces explicitly enumerated in `measure_cm_coverage.py`.

[CONDITIONAL: the class-polynomial computation returns a certified correct
polynomial in time polynomial in $|D|$ and $\log r$] A witness to
$\mathsf{SCM}_{C,K}(r)$ gives the required auxiliary curve in randomized
expected $\operatorname{poly}(L)$ time: compute and factor $H_D$ modulo $r$,
turn a root into a curve, and use exact polynomial-time point counting to
select the trace-$t$ twist.  Enge's 2009 Corollary 1.3 supplies the needed
$O(|D|\log^{6+\epsilon}|D|)$ class-polynomial bound under its explicitly
stated floating-point precision heuristic; its rigorous height bound permits
certification but does not by itself prove that sharp rounding analysis.

[PROVED] Thus a theorem establishing $\mathsf{SCM}_{C,K}(r)$ for every prime
$r$, together with the stated certified CM implementation bound, is a concrete
sufficient route to the uniform Maurer reduction.  It is stronger than mere
existence of a smooth integer in the Hasse interval because it also forces a
polylogarithmic CM discriminant.

### Why finite CM success does not settle the asymptotic problem

[HEURISTIC] For fixed $C,K$, the bounded-CM scan exposes only
$O((\log r)^K)$ candidate orders.  If their smoothness behaves like that of
independent integers near $r$, a union estimate gives success probability at
most

$$
  (\log r)^K r^{-1/C+o(1)}=o(1).
$$

This assessment is falsified by a proved arithmetic correlation that gives
uniform bounded-CM coverage, or by a proved non-random smoothness law for these
norm-equation orders.

[HEURISTIC] The bounded-CM route is therefore not an asymptotic construction
under the same random-integer model that fit A001, despite its high toy-scale
success below.  At 60 bits the bound $L^3=216{,}000$ is still about $2^{17.7}$,
so the experiment is far from the regime in which the preceding asymptotic
estimate becomes small; a scaling theorem or substantially larger permitted
range would refute or support this extrapolation.

### Validation and measurements

[PROVED] `measure_cm_coverage.py` enumerates the exact $j=0$ and $j=1728$
twist-order lists, then scans negative fundamental discriminants in increasing
absolute value, solves $4r=t^2-Dv^2$, and records the first order whose largest
prime factor meets the selected bound.  The recorded `cm_conductor` is the
index parameter $v$ of the Frobenius order, while `cm_class_number` belongs to
the fundamental order of discriminant $D$.

[EMPIRICAL: all nonzero coefficients for p in {7,13,17,19,31,37}] The
explicit-family order formulas matched exhaustive point counts for every
$j=0$ and $j=1728$ twist in the validation set.

[EMPIRICAL: p in {101,211}, |D| <= 200] The Cornacchia enumeration matched a
brute scan of all nonnegative ordinary traces, and the class-number routine
matched the known values $h(-3)=h(-4)=1$, $h(-20)=2$, and $h(-23)=3$; see
`code/tests/test_measure_cm_coverage.py`.

[EMPIRICAL: first 128 descending primes below each of 2^44,...,2^60] With
$|D|\le L^3$, bounded CM found an $L^3$-smooth order for every tested prime,
while explicit-family success decreased from 52/128 at 44 bits to 15/128 at
60 bits.  Tightening only the order bound to $L^2$ caused bounded-CM coverage
to fall to 42/128 at 60 bits.

| bits | explicit, $B=L^3$ | bounded CM, $B=L^3$ | bounded CM, $B=L^2$ |
|---:|---:|---:|---:|
| 44 | 52/128 | 128/128 | 120/128 |
| 48 | 42/128 | 128/128 | 107/128 |
| 52 | 34/128 | 128/128 | 83/128 |
| 56 | 24/128 | 128/128 | 60/128 |
| 60 | 15/128 | 128/128 | 42/128 |

[EMPIRICAL: 4,096 descending 60-bit primes, B=60^3] The explicit families
succeeded for 445/4096 primes, rate 0.10864 with Wilson 95% interval
0.09948--0.11854.  Bounded CM succeeded for 3635/4096 with
$|D|\le60^2$, rate 0.88745 (0.87741--0.89677), and for all 4096 with
$|D|\le60^3$, whose Wilson lower endpoint is 0.99906.  See the matching
`measure_cm_coverage_b60_p4096_e3_d{2,3}_w8_20260625_{raw,summary}.csv` files.

[PROVED] The explicit list contains respectively 10, 5, 7, and 1 distinct
orders when $r\bmod12$ is 1, 5, 7, and 11: the $j=1728$ family splits when
$r\equiv1\pmod4$, the $j=0$ family splits when $r\equiv1\pmod3$, and the
otherwise available trace-zero orders coincide.  This gives a concrete
candidate-count explanation for the observed residue ordering.

[EMPIRICAL: same 4,096-prime run, B=60^3 and |D|<=60^2] Bounded-CM coverage
was 1027/1058 for residue 1, 899/1013 for residue 5, 932/1009 for residue 7,
and 777/1016 for residue 11 modulo 12.  The raw-to-table computation is in
`summarize_cm_residues.py` and
`measure_cm_coverage_b60_p4096_e3_d2_w8_20260625_residues.csv`.

| $r\bmod12$ | successes / primes | rate (Wilson 95% CI) |
|---:|---:|---:|
| 1 | 1027/1058 | 0.97070 (0.95871--0.97928) |
| 5 | 899/1013 | 0.88746 (0.86652--0.90548) |
| 7 | 932/1009 | 0.92369 (0.90565--0.93851) |
| 11 | 777/1016 | 0.76476 (0.73772--0.78982) |

[EMPIRICAL: same 4,096-prime run, B=|D|=60^3] The largest first-hit
discriminant was $|D|=180{,}331$ for
$r=1{,}152{,}921{,}504{,}606{,}838{,}643\equiv11\pmod{12}$; its recorded
class number was 87, $v=2{,}899{,}546$, $t=1{,}759{,}425{,}224$, and the
resulting order had largest prime factor 10,559.  This prime is the hardest
tested instance by the pre-registered least-discriminant metric, not a proved
worst case.

[EMPIRICAL: Windows 11, Python 3.13.4] The serial 128-prime, five-size,
two-bound run took 747.32 seconds.  Eight-worker 4,096-prime runs took 28.50
seconds for $|D|\le60^2$ and 42.95 seconds for $|D|\le60^3$; these are wall
times, while the summary CSVs retain aggregate per-prime CPU measurements.

[PROVED] The bounded scan covers ordinary principal-CM traces with small
fundamental discriminant and the separately coded $j=0,1728$ families; it is
not an exhaustive catalogue of every possible explicit or supersingular
construction.  It measures order reachability and discriminant/class-number
cost, but it does not implement the class-polynomial-to-curve step.

## Alternative auxiliary groups

### Full multiplicative groups

[CITED] Bollauf--Parisella--Siim 2025 gives a concretely efficient version of
the den Boer reduction using $\mathbb F_r^*$ when $r-1$ is sufficiently
smooth.  Its factor-dependent Pohlig--Hellman cost is polynomial in $\log r$
under the asymptotic condition

$$
  \mathsf{MUL}_C(r):\qquad P^+(r-1)\le(\log r)^C
$$

for a fixed $C$.

[PROVED] On inputs satisfying $\mathsf{MUL}_C$, this removes the curve-search
problem entirely: the group and its order $r-1$ are explicit, and trial
division through $(\log r)^C$ factors the promised-smooth order in polynomial
time.

[CITED] Li 2025 proves that $P^+(r-1)>r^{0.679}$ for infinitely many primes
$r$.

[PROVED] Consequently, for every fixed $C$, infinitely many primes violate
$\mathsf{MUL}_C(r)$, since $r^{0.679}>(\log r)^C$ eventually.  Thus the full
multiplicative group is a valid parameter-specific alternative but cannot
complete the every-prime Maurer reduction.

[PROVED] Passing to the full extension group $\mathbb F_{r^n}^*$ does not
remove this obstruction: $r-1$ divides $r^n-1$, so the same infinite prime
family leaves a super-polylogarithmic prime factor in the full group order for
every $n\ge1$.  The additive group is also unusable for this purpose because
its order is $r$ itself.

[PROVED] These arguments do **not** rule out selected subgroups of extension
fields, norm-one tori, elliptic curves, or other constant-rank algebraic
groups whose orders omit the offending factor.  Such a route still needs an
every-prime smooth-order theorem plus Maurer's efficient algebraic embedding
and extraction properties.

### The quadratic norm-one torus, and a simultaneous obstruction

[PROVED] Let $d$ be a nonsquare in $\mathbb F_r$ and define

$$
  T_d(\mathbb F_r)=\{(x,y):x^2-dy^2=1\}.
$$

Multiplication of $x+y\sqrt d$ gives the polynomial group law

$$
  (x,y)(u,v)=(xu+dyv,xv+yu).
$$

This is the kernel of the norm
$\mathbb F_{r^2}^*\to\mathbb F_r^*$, hence is cyclic of order $r+1$.

[PROVED] The formulas

$$
  t\longmapsto
  \left(\frac{1+dt^2}{1-dt^2},\frac{2t}{1-dt^2}\right),
  \qquad
  t=\frac{y}{x+1}
$$

give mutually inverse maps between $\mathbb F_r$ and
$T_d(\mathbb F_r)\setminus\{(-1,0)\}$.  The denominator $1-dt^2$ never
vanishes because $d$ is a nonsquare.  These constant-degree formulas and the
group law use only field operations, so the CDH oracle evaluates them on
implicit field elements exactly as in the elliptic construction.  If $r+1$
were polylogarithmically smooth, generalized Pohlig--Hellman on this cyclic
torus would therefore give a curve-free Maurer-style reduction.

[PROVED] The remaining setup is also polynomial: a random nonzero field
element is a nonsquare with probability $1/2$, and after factoring the smooth
order, random explicit torus points can be tested against every prime divisor
of $r+1$ to obtain a generator in expected polynomial time.

[EMPIRICAL: every parameter over $(r,d)=(7,3),(11,2),(13,2),(17,3)$] The
parametrization produced exactly the $r$ nonexceptional torus points without
duplicates, extraction recovered every $t$, each full torus had $r+1$
points, and the group law was exhaustively closed in the test fixtures.

[CITED] Linnik's theorem, with Xylouris's admissible exponent $L_0=5.2$,
states that the least prime in any coprime residue class $a\bmod m$ is at most
$C m^{L_0}$ for an absolute effective $C$.

[PROVED] For every large $X$, choose primes
$q\in(X,2X)$ and $s\in(2X,4X)$ and use CRT to select $a$ with

$$
  a\equiv1\pmod q,\qquad a\equiv-1\pmod s.
$$

Since $\gcd(a,qs)=1$, Linnik supplies a prime

$$
  r\equiv a\pmod{qs},\qquad
  r\le C(qs)^{L_0}\le C8^{L_0}X^{2L_0}.
$$

Thus $q\mid r-1$, $s\mid r+1$, and for an absolute $c>0$,

$$
  \min\{P^+(r-1),P^+(r+1)\}
  \ge X\ge c r^{1/(2L_0)}=c r^{1/10.4}.
$$

As $X\to\infty$ the resulting primes are unbounded, so an infinite distinct
subsequence exists.

[PROVED] Consequently, for every fixed polylogarithmic exponent $C'$, there
are infinitely many primes on which **both** the split torus of order $r-1$
and the quadratic nonsplit torus of order $r+1$ violate the required
$(\log r)^{C'}$ smoothness.  An algorithm restricted to choosing between
these two full one-dimensional tori cannot be uniform.

[PROVED] This simultaneous theorem still leaves selected smooth subgroups,
higher-degree tori, and elliptic curves untouched.  In particular, a large
prime factor in the ambient order does not show that every sufficiently large
smooth divisor or efficiently decodable subgroup is absent.

[PROVED] It does, however, rule out the standard random-shift subgroup repair
on the constructed family.  Put $\eta=1/(2L_0)$.  A
$(\log r)^{C'}$-smooth subgroup of either cyclic torus cannot contain its
forced prime factor, so its size is $O(r^{1-\eta})$.  A uniform random shift
of the implicit input is uniform in $\mathbb F_r$; under the split-torus
identity parametrization or the nonsplit-torus bijection above, its chance of
landing in such a subgroup is therefore $O(r^{-\eta})$.  Independent
shift-and-membership trials need $\Omega(r^\eta)$ expected attempts.

[PROVED] This last lower bound is only for that explicit shift-and-test model.
It does not exclude an embedding that uses different algebraic structure,
nonuniform advice, or a subgroup not reached by uniform parameter shifts.

### Every bounded-degree full norm-one menu is obstructed

[PROVED] The preceding CRT--Linnik argument extends from degree two to every
fixed finite degree bound.  Fix $D\ge2$.  For $2\le n\le D$, the full norm-one
torus

$$
  T_n(\mathbb F_r)=\ker\!\left(
    N_{\mathbb F_{r^n}/\mathbb F_r}\right)
$$

has order $(r^n-1)/(r-1)$.

[CITED] The prime number theorem for fixed arithmetic progressions gives, for
all sufficiently large $X$, distinct primes
$q_n\in(X,2X)$ with $q_n\equiv1\pmod n$ for $2\le n\le D$; also choose a
distinct $q_1\in(X,2X)$ (Soprounov 1998, Theorem 2.1).

[PROVED] Because $\mathbb F_{q_n}^*$ is cyclic, choose $a_n$ of exact order
$n$ modulo $q_n$, taking $a_1=1$.  CRT gives one reduced residue $a$ modulo
$M=\prod_{n=1}^Dq_n$ with $a\equiv a_n\pmod{q_n}$.  Linnik then supplies a
prime

$$
  r\equiv a\pmod M,\qquad
  r\le C M^{L_0}\le C(2X)^{DL_0}.
$$

For $n=1$, $q_1\mid r-1$.  For every $n\ge2$, the exact order condition gives
$q_n\mid r^n-1$ but $q_n\nmid r-1$, hence
$q_n\mid(r^n-1)/(r-1)$.  Consequently an infinite unbounded set of primes
satisfies, simultaneously for every $1\le n\le D$,

$$
  P^+(|T_n(\mathbb F_r)|)\ge c_D r^{1/(DL_0)},
$$

where $T_1$ denotes the split torus of order $r-1$.

[PROVED] Thus no algorithm that chooses, as a function of $r$, among full
norm-one tori of any globally bounded extension degree can meet a fixed
polylogarithmic smoothness bound for every prime.  This covers the canonical
full norm-one family at constant rank.  It does not classify or obstruct all
algebraic tori of bounded dimension, nor their selected subgroups.

### All full algebraic tori of bounded dimension are obstructed

[CITED] Let $T/\mathbb F_r$ be a $d$-dimensional algebraic torus.  Its rank-$d$
character lattice carries a finite-order integral Frobenius matrix $\Phi$, and
Batyrev--Tschinkel 1995, Theorem 1.3.11, gives

$$
  |T(\mathbb F_r)|=\det(rI-\Phi).
$$

[PROVED] If $\Phi^m=I$, its minimal polynomial divides $x^m-1$.  Hence its
characteristic polynomial over $\mathbb Z$ has the form

$$
  \chi_\Phi(x)=\prod_{n\ge1}\Phi_n(x)^{e_n},
  \qquad
  \sum_{n\ge1}e_n\varphi(n)=d,
$$

where the first $\Phi$ denotes the Frobenius matrix and $\Phi_n(x)$ denotes
the $n$th cyclotomic polynomial.  Consequently

$$
  |T(\mathbb F_r)|=\prod_{n\ge1}\Phi_n(r)^{e_n}.
$$

[PROVED] For a fixed dimension bound $D$, only the finite index set

$$
  \mathcal N_D=\{n:\varphi(n)\le D\}
$$

can occur.  Finiteness follows directly: if $p^a\mid n$, then
$p^{a-1}(p-1)\mid\varphi(n)$, so $p\le D+1$ and $p^{a-1}\le D$ whenever
$\varphi(n)\le D$.

[PROVED] Put $k_D=|\mathcal N_D|$.  For every sufficiently large $X$, the
fixed-progression prime number theorem supplies distinct primes

$$
  \ell_n\in(X,2X),\qquad \ell_n\equiv1\pmod n
  \quad(n\in\mathcal N_D).
$$

Choose $b_n$ of exact multiplicative order $n$ modulo $\ell_n$ (and
$b_1=1$), and use CRT to choose $b$ modulo
$M=\prod_{n\in\mathcal N_D}\ell_n$ with $b\equiv b_n\pmod{\ell_n}$.
Linnik's theorem supplies a prime

$$
  r\equiv b\pmod M,
  \qquad r\le C M^{L_0}\le C(2X)^{k_DL_0}.
$$

[PROVED] Taking $X>D+1$ makes $\ell_n\nmid n$.  The exact-order criterion then
gives $\ell_n\mid\Phi_n(r)$ for every $n\in\mathcal N_D$.  Also
$\ell_1\mid r-1$, so the resulting primes $r$ grow unboundedly with $X$.
Thus an infinite distinct subsequence satisfies, simultaneously for **every**
nontrivial full torus $T/\mathbb F_r$ of dimension at most $D$,

$$
  P^+(|T(\mathbb F_r)|)
  \ge X\ge c_D r^{1/(k_DL_0)}.
$$

[PROVED] Since a fixed power of $r$ eventually exceeds every fixed power of
$\log r$, no algorithm choosing arbitrary **full algebraic tori of globally
bounded dimension** can provide Maurer's polylog-smooth auxiliary order for
every prime.  This strictly extends A004 beyond norm-one tori.

[PROVED] The theorem still does not rule out a selected subgroup that omits
the forced factor, a disconnected non-torus auxiliary group, an abelian
variety such as an elliptic curve, or an embedding whose useful auxiliary
object is not the full rational-point group of a bounded-dimensional torus.

### Affine factors reduce the full connected case to abelian varieties

[CITED] Chevalley's theorem gives every smooth connected commutative
$G/\mathbb F_r$ a unique exact sequence
$1\to L\to G\to A\to1$, with $L$ connected affine and $A$ an abelian
variety (Conrad 2002, Theorem 1.1).

[CITED] Over the perfect field $\mathbb F_r$, the unipotent radical $U$ of
$L$ is split, $T=L/U$ is a torus, and
$|U(\mathbb F_r)|=r^{\dim U}$.  Lang's theorem makes rational-point maps to
the connected quotients surjective, so

$$
  |G(\mathbb F_r)|
  =|U(\mathbb F_r)|\,|T(\mathbb F_r)|\,|A(\mathbb F_r)|.
$$

[PROVED] If $U$ is nontrivial, the full order has the prime factor $r$.  If
$U$ is trivial but $T$ is nontrivial, A005's simultaneous torus theorem gives
an infinite prime family on which the full order has a factor
$r^{\Omega_D(1)}$.  Therefore every full bounded-dimensional smooth
connected commutative group with nonzero affine part is obstructed.  Only
pure abelian varieties remain in this full connected class.

### A general selected-subgroup bound in dimension one

[PROVED] Let a public coin $e$, independent of $x\in S$, select an encoder
$f_e:S\to H\cup\{\bot\}$, and suppose a decoder satisfies
$d(e,f_e(x))=x$ whenever encoding succeeds.  For each fixed $e$, successful
encoding is injective, and hence

$$
  \frac1{|S|}\sum_{x\in S}\Pr_e[f_e(x)\ne\bot]\le\frac{|H|}{|S|}.
$$

[PROVED] On A005's prime family, a polylog-smooth subgroup $H$ of a one-
dimensional torus must omit a factor $\ell\ge c r^\eta$.  Since the full torus
has order $O(r)$, $|H|=O(r^{1-\eta})$.  Taking $S=\mathbb F_r$ proves that
every correct public-coin recoverable encoding into $H$ has average success
$O(r^{-\eta})$.  Thus the selected-subgroup escape is closed for dimension
one in this model, not merely for random shifts.

[PROVED] The same count does not close dimension at least two: after removing
a factor $r^\eta$ from an ambient group of order about $r^d$, a selected
subgroup can still have at least $r$ elements.  Abelian varieties and higher-
dimensional selected subgroups are the remaining structural branches.

### Abelian surfaces remove the RH short-interval endpoint, but not uniformity

[CITED] Van Bommel--Costa--Poonen--Smith--Li 2025, Theorem 1.7 and Remark
1.11, imply that for any fixed $0<\lambda<4-2\sqrt2$, every integer in

$$
  [r^2-\lambda r^{3/2},\ r^2+\lambda r^{3/2}]
$$

is the order of an ordinary abelian surface over $\mathbb F_r$ for all
sufficiently large primes $r$.

[CONDITIONAL: Riemann Hypothesis] After fixing
$1/2<\lambda<4-2\sqrt2$, this interval contains a subinterval
$[X,X+X^{3/4}]$ with $X=r^2+O(r^{3/2})$.  Younis 2024, Theorem 1.3, gives a
positive asymptotic count of $(\log X)^{K(3/4)}$-smooth integers there.  Thus
every sufficiently large prime admits a full ordinary abelian surface order
with largest prime factor $(\log r)^{O(1)}$.

[PROVED] This is not a construction.  The analytic theorem does not find the
smooth order in polynomial time, and the prescribed-order theorem does not
output a surface equation plus Maurer--Wolf's required strong embedding.

[PROVED] If a nonsingular genus-two curve $C:y^2=f(x)$ with smooth Jacobian
order is explicitly available, its Jacobian does satisfy the interface.
Cantor arithmetic uses constant-size Mumford representations.  Given implicit
$x$ and public random $e$, set $X=x+e$, take an implicit square root
$Y^2=f(X)$ when it exists, and output the divisor class with
$u(z)=z-X,v(z)=Y$.  The Weil character bound gives success
$1/2+O(r^{-1/2})$, and extraction returns $X-e=x$.  The group rank is at most
four.

[CITED] Bröker--Howe--Lauter--Stevenhagen 2015 show that prescribed-Jacobian-
order genus-two CM constructions have exponential worst-case running time.
Their heuristic polynomial-time construction instead prescribes
$|C(\mathbb F_p)|$, not $|J(C)(\mathbb F_p)|$, so it is not an alternative
construction for the Maurer auxiliary group.

### Weil-polynomial realization is a separate inverse problem

[CITED] Van Bommel--Costa--Poonen--Smith--Li construct the prescribed-order
Weil polynomial and invoke Honda--Tate for the corresponding isogeny-class
existence.  The proof does not output equations for a member of that class.

[CITED] Howe--Nart--Ritzenthaler 2009 gives a complete criterion for whether
an abelian-surface isogeny class contains a genus-two Jacobian, but it is an
existence criterion rather than a curve-construction algorithm.

[EMPIRICAL: r=251,1019,4091,16363] Exact enumeration found that every integer
in the four central intervals of half-width $\lfloor r^{3/2}\rfloor$ had an
ordinary Jacobian-admissible Weil polynomial.  Every
$\lfloor(\log_2r)^3\rfloor$-smooth integer in those intervals did as well.

[PROVED] This does not produce equations.  CM has exponential worst cases;
an isogeny walk needs an explicit seed already in the target isogeny class;
and an abstract finite group of the right order does not supply the
recoverable algebraic `EMBED/EXTRACT` interface.

### Exponent-vector finders do not yet construct the smooth order

[PROVED] Fix constants $K,k,C>0$, put $X\asymp r^2$, and allow prime factors
up to $(\log X)^K$.  The number of products near $X$ supported on at most $k$
distinct primes is $(\log X)^{O_{K,k}(1)}$.  Each such product can lie within
$C r^{3/2}$ of $r^2$ for only $O_C(X^{1/4})$ integer values of $r$.

[CITED] The prime number theorem gives $\Theta(\sqrt X/\log X)$ prime values
of $r$ in a fixed dyadic square-root range.

[PROVED] Since
$X^{1/4}(\log X)^{O_{K,k}(1)}=o(\sqrt X/\log X)$, every sufficiently large
dyadic range contains a prime center missed by all bounded-support products.
This permits the supporting primes to be selected after seeing $r$; only the
number of nonzero exponents is globally bounded.

[PROVED] With unrestricted support, replacing each exponent by repeated
copies of $\log p$ yields polynomially many real subset-sum items.  The target
logarithmic interval has width $\Theta(X^{-1/4})$, however, so a direct safe
integer rounding needs scale $Q=\Omega(mX^{1/4})$ and numerical target
$t=\Theta(QL)=X^{1/4}L^{O(1)}$ for $L=\log X$.

[CITED] Bringmann's $\widetilde O(n+t)$ subset-sum algorithm is
pseudopolynomial in this numerical target.  Lagarias--Odlyzko's lattice
success theorem covers almost all low-density instances, whereas the
minimally rounded logarithmic instance has density tending to infinity for
every fixed smoothness exponent $K>1$ and has repeated structured weights.

[PROVED] These facts rule out the audited bounded-support enumeration,
pseudopolynomial dynamic-programming, and low-density lattice guarantees as
uniform polynomial-time bridges.  They do not prove a lower bound against a
specialized algorithm for structured prime logarithms.

[CITED] Hittmeir's Smooth Subsum Search is explicitly a heuristic for smooth
polynomial values in integer factorization and does not supply an every-
interval worst-case theorem.

### Current short-interval boundary

[CITED] Younis 2024 proves a polylogarithmic-smoothness asymptotic under the
Riemann Hypothesis for intervals of length $x^\theta$ at every fixed
$\theta>1/2$.

[PROVED] The Hasse interval lies at the missing endpoint
$\theta=1/2$ (up to a constant factor), so even this conditional theorem does
not establish a polylogarithmically smooth integer in every Hasse interval.
Unconditionally, Younis's smoothness range remains super-polylogarithmic,
consistent with the stronger all-interval limitation recorded from Jain 2026.

[EMPIRICAL: primary-source audit through 2026-06-29] No checked source on
multiplicative groups, extension fields, elliptic CM constructions, or smooth
numbers in short intervals supplied all three missing properties: every-prime
coverage, polylogarithmic largest prime factor, and polynomial construction.
This is a bounded literature finding, not a nonexistence theorem.

## What remains

> **Gap.** [PROVED] I do not know how to prove $\mathsf{SCM}_{C,K}(r)$ for
> every prime $r$ for any fixed $C,K$, how to replace it by another uniform
> auxiliary-group construction, or how to prove an infinite family obstructing
> every admissible small-CM or constant-rank construction.  The proved
> obstructions cover full bounded-dimensional connected groups with affine
> part, one-dimensional selected torus subgroups in the public-coin model,
> bounded-support smooth products, and the stated generic finder routes; they
> do not cover pure abelian varieties, higher-dimensional selected subgroups,
> or every specialized algorithm on prime logarithms.  Under RH, the surface
> branch still needs both a polynomial-time smooth-order finder and an
> explicit strongly algebraically defined realization.  Resolving Q005
> requires a uniform small-CM correlation, both missing surface algorithms, a
> different every-prime auxiliary family, or a lower bound in a model that
> contains the real algebraic construction algorithms. Blocking: yes for the
> full reduction.
