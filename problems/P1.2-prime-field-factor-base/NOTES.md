# Notes

## Formal resolution

[PROVED] Under standard generalized L-notation and a summand count $m$ fixed
independently of $p$, P1.2 is impossible as written. A base of size
$s\le L_p[1/2,c]=p^{o(1)}$ reaches at most $s^m=p^{o(1)}$ targets, whereas
Hasse's bound gives $\#E(\mathbb F_p)=p^{1+o(1)}$. Thus uniform-target success
is at most $p^{-1+o(1)}$, below every inverse polynomial in $\log p$.
`CLAIM.md` contains the full proof, adversarial checks, and quantified repairs.

[PROVED] For fixed $m$ and inverse-polylogarithmic success, counting requires
$s\ge p^{1/m-o(1)}$. If the standard $L_p[1/2,c]$ bound is retained, counting
requires
$m\ge(1/c+o(1))\sqrt{\log p/\log\log p}$; neither necessary condition alone
provides an efficient algorithm.

[CONDITIONAL: $L_p(1/2)$ meant $p^{1/2}$] The experimental square-root regime
below remains relevant, but it is a corrected problem rather than the formal
statement under standard notation.

## A008 preprocessing and nonuniformity audit

[PROVED] In a cyclic group of order $r$, the union of $m$ positional digit
sets has size at most $m\lceil r^{1/m}\rceil$ and represents every group
element with exactly $m$ summands. A target-indexed table makes online
decomposition a lookup but uses $r$ entries.

| Tag | $p$ | $r$ | $m$ | Radix | Base size | $\lfloor\sqrt p\rfloor$ | Table entries | Stored point references | Invalid sums |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [EMPIRICAL: 16-bit exhaustive] | 65,519 | 65,537 | 3 | 41 | 120 | 255 | 65,537 | 262,148 | 0 |
| [EMPIRICAL: 18-bit exhaustive] | 262,139 | 261,431 | 3 | 64 | 190 | 511 | 261,431 | 1,045,724 | 0 |
| [EMPIRICAL: 20-bit exhaustive] | 1,048,571 | 1,046,897 | 3 | 102 | 304 | 1,023 | 1,046,897 | 4,187,588 | 0 |

[EMPIRICAL: all 1,373,865 target rows] Every target was covered; every returned
term passed factor-base membership and every returned sum was correct.

[PROVED] With $m=3$ the base is $O(p^{1/3})$, so it eventually lies below a
square-root bound. The table and construction are nevertheless
$p^{1+o(1)}$-scale and therefore exponential in input length. This resolves an
online-only specification loophole, not the uniform decomposition problem.

`CORRECTED_VARIANTS.md` records two explicit specification proposals: a
succinct square-root/fixed-length variant and a standard-L/growing-length
variant, both charging input-specific construction, advice, preprocessing,
and storage.

## A009 translate-probe lower bound

[PROVED] A translate-probe three-sum decoder stores shifts $a=P+Q$ and tests
$R-a\in\mathcal F$. After $T$ fixed probes its success set lies in a union of
$T$ translates of $\mathcal F$, so
$$
\Pr[\mathrm{success}]\le \frac{T|\mathcal F|}{r}.
$$
The same bound holds for failure-adaptive schedules because every execution
before its first success follows the single all-zero path, and for randomized
schedules by conditioning on their coins.

[PROVED] Candidate A has at most $2\lfloor\sqrt p\rfloor$ points. Hence
inverse-polylogarithmic success in this model requires
$T\ge p^{1/2-o(1)}$ membership probes. The implemented lexicographic scan is
inside this model; coordinate-aware algorithms and A008's target table are not.

| Tag | Group order | Base size | Probes $T$ | Shift schedules | Bound $Ts$ | Min support | Max support | Strict schedules | Violations |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [EMPIRICAL: exhaustive] | 19 | 4 | 1 | 19 | 4 | 4 | 4 | 0 | 0 |
| [EMPIRICAL: exhaustive] | 19 | 4 | 2 | 171 | 8 | 6 | 8 | 95 | 0 |
| [EMPIRICAL: exhaustive] | 19 | 4 | 3 | 969 | 12 | 8 | 12 | 950 | 0 |
| [EMPIRICAL: exhaustive] | 19 | 4 | 4 | 3,876 | 16 | 9 | 14 | 3,876 | 0 |

[PROVED] This closes P1.2/Q001 in the explicitly stated generic translate-probe
model. P1.2/Q004 retains the genuinely structural question: whether the
integer-$x$ predicate enables a succinct coordinate-aware algorithm outside
that model.

## A010 smooth-subgroup coordinate predicate

[CITED] Petit–Kosters–Messeng (PKC 2016) replace the interval predicate by
roots of a composable rational map, including smooth multiplicative subgroups
of $\mathbb F_p^*$, but leave the Gröbner complexity of the resulting
prime-field systems open. [CITED] Amadori–Pintore–Sala (FFA 2018) also leave
the complexity of their one-system prime-field variant unresolved.

[PROVED] If $H\subset\mathbb F_p^*$ has smooth order
$n=\prod_{j=1}^{t}\ell_j$, membership in $H$ is the root condition $x^n=1$.
The auxiliary chain $z_0=x$, $z_j=z_{j-1}^{\ell_j}$, $z_t=1$ replaces that
one degree-$n$ condition by $t$ conditions of degrees $\ell_j$.

| Tag | $p$ | $r$ | $|H|$ | Base size | Predicate mismatches | Mean count | Normalized ratio to random (95% CI) | Pair-check ratio (95% CI) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [EMPIRICAL: 96 targets, seed 12022032] | 65,537 | 65,809 | 64 | 60 | 0 | 4.042 | 1.112 [0.819, 1.470] | 0.969 [0.827, 1.130] |

[EMPIRICAL: SymPy 1.14.0, five-second limit] Both the direct and chain $f_4$
systems completed at $p=17$; both timed out at $p=257$ and $p=65537$. At the
largest fixture the chain reduced maximum input degree from 64 to 12 but
increased variables from 3 to 18 and equations from 4 to 19.

[PROVED] The predicate and chain are genuine coordinate structure outside
A009, but predicate evaluation is not a decomposition algorithm. The recorded
timeouts establish only the behavior of this solver and limit, not an
asymptotic lower bound. P1.2/Q004 therefore remains open for Variant S.

## Stable facts

- [PROVED] For a fixed factor base $\mathcal F$ of size $s$ in a group of
  order $r$ and a uniform target $R$, the expected number of ordered
  three-term decompositions is exactly $s^3/r$. Proof: every ordered triple in
  $\mathcal F^3$ sums to one target, so summing the target-wise counts over all
  $r$ targets gives $s^3$; averaging gives $s^3/r$.
- [PROVED] Membership in Candidate A is polynomial in $\log p$: reject the
  identity and compare the canonical integer representative of $x(P)$ with
  $\lfloor\sqrt p\rfloor$.
- [PROVED] Candidate A has at most $2\lfloor\sqrt p\rfloor$ points because a
  fixed $x$ has at most two corresponding $y$-coordinates. This upper bound is
  too large to certify the formal $L_p(1/2)$ requirement, so A001 does not
  establish condition (1).
- [CITED] The implemented $f_3$ formula and recursive resultant definition of
  $f_4,f_5$ agree with Semaev (2004, IACR ePrint 2004/031).
- [EMPIRICAL: unit tests over F_17 and F_101] Curve arithmetic matches the
  known order-19 example; fixed-input $f_3,f_4,f_5$ values match an independent
  symbolic resultant calculation; and each polynomial vanishes on tested
  point tuples summing to the identity (`lib/tests/`).
- [EMPIRICAL: exact point enumeration at the three recorded primes] The
  selected group orders are prime, and the traces are $-17$, $709$, and
  $1675$, all nonzero modulo their characteristics.
- [CITED] The supersingular/ordinary trace classification (Waterhouse 1969)
  then places these three curves in the ordinary case.

## SG-01 random baseline

[EMPIRICAL: one curve at each listed p, seed 12022026] The table reports
ordered decomposition counts for a random base of size
$s=\lfloor\sqrt p\rfloor$. Each row pools 96 common targets across three
independently sampled bases (288 observations); intervals are 95%
hierarchical-percentile bootstrap intervals over base and target sampling.

| Tag | $p$ | Curve $(a,b)$ | $r$ | $s$ | Mean count (95% CI) | Exact $s^3/r$ | Normalized mean (95% CI) | Mean pair checks (95% CI) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [EMPIRICAL: 16-bit curve] | 65,519 | (20,289, 54,970) | 65,537 | 255 | 253.01 [248.28, 257.92] | 253.01 | 1.000 [0.982, 1.019] | 428.3 [355.8, 525.2] |
| [EMPIRICAL: 18-bit curve] | 262,139 | (162,850, 139,881) | 261,431 | 511 | 509.21 [501.91, 516.51] | 510.39 | 0.998 [0.984, 1.013] | 915.1 [793.9, 1,034.9] |
| [EMPIRICAL: 20-bit curve] | 1,048,571 | (632,451, 609,922) | 1,046,897 | 1,023 | 1,020.20 [1,004.28, 1,039.32] | 1,022.64 | 0.998 [0.982, 1.017] | 1,856.7 [1,639.4, 2,068.3] |

[EMPIRICAL: the 864 random-square-root target/base rows above] Every search
found a decomposition. The Wilson 95% interval for success at each size is
[0.987,1]. The exact pair table took a mean of 0.033, 0.145, and 0.829 seconds
at 16, 18, and 20 bits, respectively; this preprocessing is exhaustive, not a
polylogarithmic algorithm.

## SG-03 Candidate A versus a size-matched random base

[EMPIRICAL: same three curves and common target sets] Candidate A has one
deterministic base per curve and 96 targets; the matched baseline has three
random bases and 288 target/base observations. Candidate intervals therefore
describe target variation conditional on the selected curve and base, not
curve-to-curve variation.

| Tag | $p$ | Candidate $s$ | Candidate count (95% CI) | Matched-random count (95% CI) | Exact $s^3/r$ | Normalized-count ratio (95% CI) | Pair-check ratio (95% CI) |
|---|---:|---:|---:|---:|---:|---:|---:|
| [EMPIRICAL: 16-bit curve] | 65,519 | 242 | 222.41 [209.09, 240.35] | 215.85 [210.31, 221.14] | 216.25 | 1.030 [0.963, 1.118] | 0.938 [0.729, 1.197] |
| [EMPIRICAL: 18-bit curve] | 262,139 | 506 | 500.06 [486.53, 513.63] | 499.15 [490.96, 507.43] | 495.56 | 1.002 [0.970, 1.035] | 1.050 [0.800, 1.351] |
| [EMPIRICAL: 20-bit curve] | 1,048,571 | 1,072 | 1,177.88 [1,161.72, 1,194.38] | 1,172.97 [1,160.17, 1,186.71] | 1,176.74 | 1.004 [0.986, 1.023] | 0.866 [0.662, 1.104] |

[EMPIRICAL: p=65519 through 1048571] Neither ratio interval excludes 1 at any
size, so this experiment detects no Candidate A effect on decomposition
density or lexicographic pair-scan work.

[EMPIRICAL: three parameter sizes only] Descriptive log-log slopes for mean
pair checks versus $p$ were 0.529 for the random square-root base, 0.437 for
the size-matched random base, and 0.408 for Candidate A. These are not
asymptotic complexity estimates; all observations, fitted values, and log
residuals are stored in `data/*_scaling.csv`.

## Candidate A failure analysis

- [PROVED] Membership passes formal condition (2).
- [PROVED] The only implemented finder performs at most $s^2$ pair tests and
  thus is not polynomial in $\log p$ when $s$ is of square-root scale.
- [EMPIRICAL: tested curves only] Candidate A does not separate from a
  size-matched random base in either normalized density or generic scan work.
- [PROVED] The experiment used $f_4$ only after a group-law decomposition was
  found; polynomial vanishing verified correctness but did not find the
  decomposition.
- [CONJECTURE] Integer intervals give no useful elimination structure for
  prime-field summation polynomials beyond their cardinality. A reproducible
  algorithm with materially sub-square-root pair work over a growing range, or
  a polylogarithmic finder, would refute this conjecture.

## Why prime fields resist the Weil-restriction trick

[PROVED] A subfield of $\mathbb F_p$ contains $1$, hence contains every sum of
$1$ and therefore all of the prime field $\mathbb F_p$; it cannot be a proper
subfield. This is the elementary obstruction that is absent in a proper
extension.

[PROVED] In $\mathbb F_{q^n}$, the equation $x^q=x$ selects exactly the
embedded copy of $\mathbb F_q$. After choosing an $\mathbb F_q$-basis, an
extension-field element has $n$ base-field coordinates while an element of the
subfield has only one, so the condition supplies $n-1$ coordinate constraints.

[PROVED] In the prime-field case $n=1$, every $x\in\mathbb F_p$ satisfies
$x^p=x$ and there are no extra coordinates to eliminate. Reusing the subfield
equation therefore cuts out the whole field rather than a factor base.

[CITED] Diem (2011, Compositio 147) makes the extension-field factor base
algebraic by requiring a degree-two covering value to lie in
$\mathbb P^1(\mathbb F_q)$ and derives the decomposition system over
$\mathbb F_q$; Gaudry (2009, JSC 44) analyzes the related Weil-restriction
index calculus heuristically.

[PROVED] The integer interval $0\le x<\sqrt p$ is an external condition on the
chosen representative of one prime-field coordinate. It gives cheap
membership, but it creates no smaller base field and hence no missing
coordinates for Weil restriction to expose. Solving $f_4=0$ with interval
bounds remains a bounded modular root problem.

## Existence is not findability

[PROVED] The identity $\mathbb E[N_R]=s^3/r$ predicts many decompositions when
$s$ is near $\sqrt p$, but it contains no algorithm for locating a contributing
triple.

[EMPIRICAL: all 2,016 recorded rows] Every target decomposed, yet the generic
finder still used means ranging from 428 to 1,857 pair checks for the
random-square-root baseline and from 501 to 1,553 for Candidate A as the field
grew. The session therefore found abundant existence and no polylogarithmic
findability mechanism.

## SG-02 extension-field positive control

[PROVED] The control represents $\mathbb F_{q^3}$ in a cubic polynomial basis,
uses $x^q=x$ as the exact subfield membership predicate, decomposes sampled
linear combinations into three factor-base points, and solves simultaneously
for the factor-base logarithms and the planted target logarithm.

| Tag | $q$ | $|\mathbb F_{q^3}|$ | Group order | Base size | $s^3/r$ | Sampled targets | Relations | Secret recovered |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [EMPIRICAL: seed 12022027] | 5 | 125 | 139 | 8 | 3.683 | 15 | 9 | 37 |
| [EMPIRICAL: seed 12022029] | 7 | 343 | 347 | 8 | 1.476 | 34 | 9 | 83 |
| [EMPIRICAL: seed 12022030] | 11 | 1,331 | 1,367 | 8 | 0.375 | 149 | 9 | 123 |

[EMPIRICAL: q=5,7,11] Every planted logarithm and every solved factor-base
logarithm matched an exhaustive scalar lookup performed only after the linear
solve. This validates the relation signs and the end-to-end machinery.

[PROVED] The implementation is a correctness control rather than an
asymptotic reproduction: it enumerates the extension-field curve and builds an
explicit pair table, so it is not polynomial in the input bit length.

## SG-04 Candidate B — rational reconstruction height

[EMPIRICAL: the three A001 curves] Exact enumeration of
$x\equiv a/b\pmod p$ with strict bounds
$|a|,|b|<\lfloor\sqrt p\rfloor$ gave the following saturation.

| Tag | $p$ | Selected $x$ fraction | Factor-base size | Group fraction | Size / $\sqrt p$ |
|---|---:|---:|---:|---:|---:|
| [EMPIRICAL: 16-bit curve] | 65,519 | 0.999695 | 65,522 | 0.999771 | 255.98 |
| [EMPIRICAL: 18-bit curve] | 262,139 | 0.999893 | 261,406 | 0.999904 | 510.56 |
| [EMPIRICAL: 20-bit curve] | 1,048,571 | 0.999989 | 1,046,880 | 0.999984 | 1,022.35 |

[EMPIRICAL: tested range] Candidate B gives a one-term decomposition for more
than 99.97% of uniform targets, but only because its factor base is essentially
the whole group. The observed base is much larger than even the square-root
diagnostic base and therefore does not approach formal condition (1).

[PROVED] The measured implementation materializes the entire ratio image in
$\Theta(p)$-scale work. It does not certify a polylogarithmic membership
algorithm, although the size failure already prevents this instance from being
a solution.

## SG-05 Candidate C — low-degree maps and auxiliary curves

[PROVED] A rational map $\mathbb P^1\dashrightarrow E$ extends to a morphism.
After factoring off Frobenius in positive characteristic, Riemann–Hurwitz for
the separable part would read $-2=\deg(R)\ge0$ if the map were nonconstant.
Thus every such rational map is constant and its image reaches at most one
target with a fixed number of summands.

[PROVED] A degree-$d$ plane auxiliary curve not containing the cubic $E$ meets
it in at most $3d$ geometric points by Bézout. Consequently a constant-$m$
factor base of this form reaches at most $(3d)^m$ targets. If the auxiliary
curve contains $E$, the factor base instead becomes all of $E(\mathbb F_p)$.

[CONDITIONAL: d and m are polylogarithmically bounded] The first branch has
success below $1/\operatorname{poly}(\log p)$ at prime-field group scale, and
the second branch fails the size condition. This rules out the natural
bounded-degree plane subclass, not all higher-dimensional constructions.

## SG-06 Candidate D — integral-lift proxy

[PROVED] The tested proxy uses the centered lift
$y^2=x^3+\widetilde a x+\widetilde b$, restricts to integral points with
$|x|<\lfloor\sqrt p\rfloor$, and has polynomial-time membership because the
integer lift of $x$ is unique in that window.

| Tag | $p$ | Base size | Max canonical height | Reachable three-sum targets | Uniform-target success |
|---|---:|---:|---:|---:|---:|
| [EMPIRICAL: 16-bit curve] | 65,519 | 0 | — | 0 | 0 |
| [EMPIRICAL: 18-bit curve] | 262,139 | 0 | — | 0 | 0 |
| [EMPIRICAL: 20-bit curve] | 1,048,571 | 2 | 4.72408 | 4 | $3.82\times10^{-6}$ |

[EMPIRICAL: tested range] The simplest cheaply decidable lift condition is too
sparse for non-negligible decomposition.

[EMPIRICAL: one surviving integral x-coordinate] The height value is a
seven-step exact-doubling estimate with final-step delta
$5.42\times10^{-5}$; the two factor-base points are the two signs above
$x=-563$ and share the same canonical height.

[PROVED] This denominator-one proxy is not the full canonical-height
candidate. A complete Candidate D must specify the rational preimages allowed
above a residue-class point and prove that bounded-height existence is
decidable in polynomial time; P1.2/Q002 remains open.

## SG-07 consolidated comparison

| Candidate | Evidence tag | Size behavior | Membership | Three-term existence / finder | Outcome |
|---|---|---|---|---|---|
| Random baseline | [EMPIRICAL: 16–20 bits] | $\approx\sqrt p$ | explicit table | counts match $s^3/r$; pair scan grows | calibration only |
| A: integer $x$ interval | [EMPIRICAL: 16–20 bits] | $\approx\sqrt p$ | [PROVED] polylog | density and scan work indistinguishable from random | no advantage detected |
| B: rational height | [EMPIRICAL: 16–20 bits] | $>99.97\%$ of group | not certified by measured implementation | trivial one-term success | far too large |
| C: low-degree map/curve | [PROVED] | singleton, $\le3d$, or whole curve | algebraic | too sparse, or whole curve | restricted class ruled out |
| D: integral-lift proxy | [EMPIRICAL: 16–20 bits] | 0, 0, 2 points | [PROVED] polylog | success 0, 0, $3.82\times10^{-6}$ | too sparse; full D open |
| E: smooth subgroup | [EMPIRICAL: one 17-bit curve] | 60 points from $|H|=64$ | [PROVED] six quadratic steps | density and generic scan match random; Gröbner timed out from $p=257$ | succinct predicate, finder missing |

[CONJECTURE] In the corrected square-root-size regime, a short one-coordinate
predicate over a prime field tends to be too sparse, random-like at useful
density, or nearly universal. A square-root-size family with a proved
polylogarithmic decomposition algorithm on a growing prime-field range would
refute this trichotomy.

[CONJECTURE] What the extension-field construction contributes is an effective
dimension drop, not merely a subset of the right cardinality. A prime-field
predicate that makes the associated summation-polynomial system provably
polylogarithmic would refute this proposed common obstruction.

## Limits of this session

- [EMPIRICAL: recorded design] Only one curve was selected per bit size, so no
  inference across the distribution of prime-order curves is justified.
- [EMPIRICAL: recorded design] Counts are for ordered three-term
  decompositions with repetition allowed.
- [EMPIRICAL: recorded design] Candidate B and the Candidate D proxy reuse one
  curve at each bit size; curve-to-curve variation was not measured.
- [PROVED] The Candidate C result covers rational images of $\mathbb P^1$ and
  bounded-degree plane intersections only; it does not cover arbitrary
  higher-dimensional auxiliary constructions.
- [PROVED] The full canonical-height Candidate D remains unresolved because
  the membership predicate is not yet specified; only its integral-point
  subset was measured. This no longer affects the negative resolution of the
  standard-L formal statement, but it remains open for corrected variants.
