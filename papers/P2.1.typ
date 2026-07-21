#import "lib/paper.typ": *

#show: paper.with(
  title: "The Auxiliary Curve That Maurer's Reduction Still Lacks",
  subtitle: "Obstruction theorems, conditional abelian-surface existence, and the two algorithmic gaps in the uniform CDH-to-DLP equivalence",
  pid: "P2.1",
  keywords: ("Maurer reduction", "CDH", "DLP", "smooth group orders", "CM method", "algebraic tori", "abelian surfaces"),
  abstract: [
    Maurer and Wolf reduce the discrete logarithm problem in a cyclic group of
    prime order $r$ to the computational Diffie–Hellman problem, *given* an
    auxiliary elliptic curve $E' \/ FF_r$ whose group order is
    $(log r)^(O(1))$-smooth. The reduction is uniform in everything except that
    curve: no algorithm is known that constructs it in $"poly"(log r)$ time for
    every prime $r$, and this single missing object is what separates a
    non-uniform equivalence from a uniform one. This paper reports a
    ten-session research effort on that gap, with partial results on both
    sides. On the negative side we prove, unconditionally, that every proposed
    *full* auxiliary group other than an abelian variety fails on an infinite
    family of primes: the full multiplicative group (via a recent
    shifted-prime theorem), every full norm-one torus menu of bounded degree,
    every full algebraic torus of globally bounded dimension, and — via
    Chevalley decomposition and Lang's theorem — every full connected
    commutative group with a nonzero affine part. A public-coin counting lemma
    further eliminates polylog-smooth *selected subgroups* of one-dimensional
    tori in the recoverable-encoding model. On the positive side, combining a
    prescribed-order theorem for abelian surfaces with an RH-conditional
    short-interval smoothness theorem yields: under the Riemann Hypothesis,
    every sufficiently large prime field admits an ordinary abelian surface
    with polylog-smooth order, and an explicit genus-two Jacobian of that
    order would satisfy the Maurer–Wolf interface. Two algorithmic gaps
    remain and are made exact: finding the smooth order in the central
    $r^(3\/2)$-length interval in polynomial time, and realizing its Weil
    polynomial as an explicit curve equation. We prove that the audited
    generic finder routes cannot close the first gap — Boneh's CRT decoder
    misses the interval for every fixed smoothness exponent above one, and
    exponent-vector searches either provably miss infinitely many prime
    centers or inflate into an exponentially precise subset-sum instance.
    Alongside, seeded experiments through 60 bits quantify blind search,
    an exact iid-oracle query bound, and the striking finite-size success of
    bounded-discriminant CM: all 4,096 tested 60-bit primes admit a cubic-log
    smooth CM order with $abs(D) <= 60^3$. Every claim carries its epistemic
    tag; nothing conditional or empirical is promoted to proved.
  ],
)

= Introduction

Let $G = ⟨g⟩$ be cyclic of prime order $r$. The computational Diffie–Hellman
problem (CDH) in $G$ asks for $g^(u v)$ given $(g, g^u, g^v)$; the discrete
logarithm problem (DLP) asks for $s$ given $g^s$. DLP-hardness trivially upper
bounds CDH-hardness; the converse — that a CDH oracle suffices to compute
discrete logarithms in polynomial time — is the content of the celebrated
reduction of Maurer and Wolf @maurerwolf1999. That reduction is not free: it
consumes an *auxiliary group*, most naturally an elliptic curve
$E' \/ FF_r$, whose group order must be known and
$B$-smooth for $B = (log r)^(O(1))$. Given such a curve, the reduction embeds
implicitly represented field elements into implicit curve points and unwinds
them with generalized Pohlig–Hellman at cost polynomial in $log r$ and $B$.
The curve is the whole difficulty. Maurer and Wolf themselves supply it as
*side information* and record polylogarithmic smoothness in the Hasse interval
as an assumption; twenty-five years later the uniform statement is still open,
and practical instantiations @msv2004 @mayschneider2023 remain
parameter-by-parameter searches.

Problem P2.1 asks for either resolution: an algorithm that, on input $r$,
constructs in $"poly"(log r)$ time an auxiliary elliptic curve over $FF_r$
(or a related structure) with $(log r)^(O(1))$-smooth order — or an infinite
family of primes for which no such curve exists or finding one is hard. This
paper is the record of a fifteen-sub-goal campaign on that question. Neither
branch is closed, and we do not pretend otherwise. What the campaign produced
is a set of unconditional obstruction theorems that eliminate every candidate
auxiliary family *except* abelian varieties, a conditional existence theorem
in dimension two, an exact statement of the two algorithms still missing, and
proofs that the standard generic routes to the first of them fail.

#keybox(title: "Main findings (honest summary)")[
  *(i)* #tag("PROVED") Every full connected commutative auxiliary group of
  globally bounded dimension with a nonzero affine part — multiplicative
  groups, all norm-one tori of bounded degree, all algebraic tori of bounded
  dimension, and their unipotent extensions — admits an infinite family of
  primes $r$ on which its order has a prime factor $r^(Omega(1))$. Only
  abelian varieties survive. Polylog-smooth selected subgroups of
  one-dimensional tori are also ruled out in the public-coin
  recoverable-encoding model.

  *(ii)* #tag("CONDITIONAL", detail: "Riemann Hypothesis") Every sufficiently
  large prime $r$ admits an *ordinary abelian surface* over $FF_r$ with
  $(log r)^(O(1))$-smooth order, and an explicit genus-two Jacobian with that
  order would satisfy the full Maurer–Wolf interface. Existence is not
  construction: a polynomial-time smooth-order finder and an explicit
  curve-equation seed are both missing, and we prove the audited CRT-decoding
  and exponent-vector routes cannot supply the finder.

  *(iii)* #tag("EMPIRICAL", detail: "4,096 descending 60-bit primes")
  Bounded-discriminant CM covers every tested prime at cubic-logarithmic
  bounds ($B = abs(D)_max = 60^3$), yet the same route is asymptotically
  unsupported under the measured random-integer smoothness model. The uniform
  small-CM theorem $sans("SCM")_(C,K)$ remains the blocking open question.
]

== Contributions and scope

We contribute (i) an exact restatement of the Maurer–Wolf requirement and its
reduction mechanics in repository notation (§2); (ii) a reproducible blind-search
baseline with an exact adaptive lower bound in an explicit oracle model (§3,
#ref(<fig:smooth>), #ref(<fig:budget>)); (iii) the small-CM sufficient
condition $sans("SCM")_(C,K)$ with coverage measurements through 60 bits (§4,
#ref(<fig:cm>), #ref(<fig:res>)); (iv) the obstruction theorems for
multiplicative groups, tori, affine parts, and selected subgroups (§5); (v)
the RH-conditional abelian-surface existence theorem, the genus-two Jacobian
interface, and the four-level realization separation (§6); (vi) proofs that
Boneh's CRT decoder and the exponent-vector/subset-sum routes miss the
required interval scale (§7); and (vii) the precise open frontier (§8).

Everything below is grounded in the research record: theorems are stated with
the tags under which they were closed
(#tag("PROVED"), #tag("CITED"), #tag("CONDITIONAL", detail: "…"),
#tag("EMPIRICAL", detail: "…"), #tag("HEURISTIC")), and finite experiments are
never extrapolated beyond their stated ranges (all experiments respect the
scaffold ceiling $log_2 r <= 60$).

= The Maurer–Wolf reduction and its exact requirement

Throughout, $P^(+)(N)$ denotes the largest prime factor of a positive integer
$N$, with $P^(+)(1) = 1$; $N$ is *$B$-smooth* when $P^(+)(N) <= B$. We write
$L = ceil(log_2 r)$.

== The auxiliary-group interface

A group element $g^x$ is an *implicit representation* of $x in FF_r$.
Implicit addition of representations is multiplication in $G$, implicit
negation is inversion in $G$, implicit multiplication is one call to the CDH
oracle $sans("DH")_g (g^u, g^v) = g^(u v)$, and inversion of a nonzero
implicit field element is exponentiation to $r - 2$, costing $O(log r)$
implicit multiplications @maurerwolf1999. The reduction needs an auxiliary
finite abelian group $H$ of constant rank that is *strongly algebraically
defined* over $FF_r$: group elements have coordinate representations of
bounded size, the group operations are given by fixed low-degree algebraic
formulas evaluable on implicit inputs, and there are randomized algorithms
$mono("EMBED")$ and $mono("EXTRACT")$ such that $mono("EMBED")(x, e)$ maps a
field element into $H$ using public randomness $e$ with bounded expected
algebraic cost, and $mono("EXTRACT")(mono("EMBED")(x, e), e) = x$
@maurerwolf1999. In the prime-order setting relevant here, the group order of
$G$ has the single prime divisor $r$, so the multi-prime hypotheses of the
general theorem are vacuous.

#proposition(name: [Maurer–Wolf, restated for prime order])[
  #tag("CITED") Let $G$ be cyclic of prime order $r$ with a CDH oracle, and
  let $H$ be a constant-rank, strongly algebraically defined abelian group
  over $FF_r$ with known order $N$ and $P^(+)(N) <= B$. Then the discrete
  logarithm in $G$ is computable with $"poly"(log r, B)$ oracle calls and
  group operations. An elliptic curve $E' \/ FF_r$ is such a group: it has
  rank at most two and is strongly $(2, O((log r)^2))$-algebraically defined
  @maurerwolf1999.
]

The reduction runs as follows @maurerwolf1999 @msv2004. Given implicit $x$,
choose an explicit uniform shift $e in FF_r$, set $X = x + e$, and evaluate
$D = X^3 + A X + B'$ implicitly on the curve
$E' : y^2 = x^3 + A x + B'$. Test whether $D$ is a quadratic residue (an
implicit Legendre-symbol computation) and, when it is — probability
$approx 1\/2$ per trial — compute an implicit square root $Y$. The pair
$(X, Y)$ is an implicit point of $E'(FF_r)$. Because $N = hash E'(FF_r)$ is
known, $B$-smooth, and of rank at most two, generalized Pohlig–Hellman over
the implicit group makes the point *explicit* using $"poly"(log r, B)$
operations; $mono("EXTRACT")$ then returns $x = X - e$, and applying this to
$x = s$ recovers the input logarithm.

#remark(name: "factorization is not an extra hypothesis")[
  #tag("PROVED") Once $N$ is known and promised $B$-smooth with
  $B = (log r)^C$, trial division through $B$ factors $N$ completely in
  $"poly"(log r)$ time, so requiring the factorization separately does not
  strengthen the condition.
]

The precise object P2.1 asks for is therefore an algorithm producing, for
every prime $r$ in time $"poly"(log r)$: a curve equation over $FF_r$
together with the exact value $N = hash E'(FF_r)$ such that
$P^(+)(N) <= (log r)^C$ for one fixed constant $C$.

== Existence versus construction

Every elliptic-curve order over $FF_r$ lies in the Hasse interval
$[r + 1 - 2 sqrt(r), thin r + 1 + 2 sqrt(r)]$, and every integer in that
interval occurs as the order of a cyclic curve @maurerwolf1999. Maurer and
Wolf define $nu(r)$ as the least value of $P^(+)$ over the interval and
obtain their general equivalence *assuming* $nu(r) = (log r)^(O(1))$, with
the curve supplied non-uniformly @maurerwolf1999. Two analytic facts bound
what current smooth-number technology can say about that assumption.
#tag("CITED") The strongest unconditional all-interval theorem guarantees a
$y$-smooth integer only for
$y >= exp(C (log x)^(2\/3) (log log x)^(4\/3))$ and interval lengths
exceeding $sqrt(x)$ times a growing factor @jain2026 — both requirements fail
the Hasse regime, where $y$ must be polylogarithmic and the length is
$4 sqrt(r)$. #tag("CITED") Under the Riemann Hypothesis, polylogarithmic
smoothness in intervals $[x, x + x^theta]$ is known for every fixed
$theta > 1\/2$ @younis2024 — and the Hasse interval sits exactly at the
excluded endpoint $theta = 1\/2$. #tag("PROVED") Consequently neither
theorem, nor any checked source, establishes $nu(r) = (log r)^(O(1))$; the
existence side is itself open at the Hasse scale, which motivates both the
finite experiments of §3–§4 and the dimension-two escape of §6.

= Blind search: measurements and an exact oracle bound

The naive construction samples curves $y^2 = x^3 + a x + b$ over $FF_r$,
counts points, and stops at the first $B$-smooth order. This section records
what that costs at toy scale and what an idealized model proves about it.

== The seeded baseline

#tag("EMPIRICAL", detail: "one prime per size, 512 curves each, 12–40 bits")
For the largest prime $r < 2^b$ with $r equiv 3 thin (mod thin 4)$ at each
$b in {12, 16, dots, 40}$, the script `measure_smooth_orders.py` sampled 512
seeded nonsingular curves, counted each order exactly with a validated
BSGS/twist counter (matched against exhaustive enumeration on 36 curves with
$101 <= r <= 65519$), and tested smoothness at
$B = ceil(L^2)$ and $B = ceil(L^3)$. The full run took 20.67 s.
#ref(<tab:blind>) and #ref(<fig:smooth>) give the results against the *exact*
$B$-smooth density of the inclusive Hasse interval, computed by segmented
enumeration, with the Dickman approximation shown only as a secondary
heuristic.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    align: (right, right, right, right, right, right, right),
    table.hline(stroke: 0.7pt),
    table.header([*bits*], [*succ. \/512, $B = L^2$*], [*curve rate*],
      [*interval rate*], [*succ. \/512, $B = L^3$*], [*curve rate*],
      [*interval rate*]),
    table.hline(stroke: 0.5pt),
    [12], [268], [0.5234], [0.4275], [461], [0.9004], [0.8118],
    [16], [173], [0.3379], [0.2659], [376], [0.7344], [0.6618],
    [20], [103], [0.2012], [0.1558], [292], [0.5703], [0.5236],
    [24], [71], [0.1387], [0.0902], [233], [0.4551], [0.4090],
    [28], [29], [0.0566], [0.0504], [178], [0.3477], [0.3078],
    [32], [21], [0.0410], [0.0275], [121], [0.2363], [0.2244],
    [36], [14], [0.0273], [0.0147], [97], [0.1895], [0.1630],
    [40], [4], [0.0078], [0.0076], [52], [0.1016], [0.1172],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Seeded blind-search success against the exact Hasse-interval
  baseline (SG-02/SG-03). At 40 bits the quadratic bound first succeeded at
  candidate 65 and the cubic bound at candidate 6. Data:
  `measure_smooth_orders_b12-…-40_t512_e2-3_s21012026_20260629_summary.csv`.],
) <tab:blind>

#tag("EMPIRICAL", detail: "same run") Every curve-to-integer rate ratio lay
in $[0.867, 1.859]$, so the pre-registered factor-two rejection rule for the
random-integer smoothness model did not fire; several small sizes
nevertheless fall outside the Wilson interval, so equality of the two
distributions was *not* established — the model survives as a working
heuristic, no more.

#fig("/figures/P2.1/smoothness.svg", width: 88%, caption: [
  #tag("EMPIRICAL", detail: "512 curves/prime, 12–40 bits, seed 21012026")
  Blind-sampling success probability (markers, Wilson 95% intervals) against
  the exact interval rate (dashed) and Dickman approximation (dotted) at
  $B = L^2$ and $B = L^3$. Curve orders track the integer model to within the
  pre-registered factor-two band throughout.
]) <fig:smooth>

#tag("HEURISTIC") Under the very integer model these measurements support,
setting $B = (log r)^C$ gives Dickman parameter $u = log r \/ (C log log r)$
and expected candidate count $rho(u)^(-1) = r^(1\/C + o(1))$ — exponential in
the input length. Blind search is therefore not the missing algorithm unless
curve orders are provably *non*-random in a favorable way; a proved
polylogarithmic candidate bound would refute this diagnosis.

== An exact lower bound in the iid Hasse-order oracle

The informal claim "adaptivity cannot help blind sampling" can be made a
theorem in an explicit model.

#theorem(name: "optimal adaptive success, iid order oracle")[
  #tag("PROVED") Fix a prime $r$, a bound $B$, the inclusive integer Hasse
  interval $I_r$, and its subset $S_B$ of $B$-smooth values; put
  $alpha = abs(S_B) \/ abs(I_r)$. Consider the oracle that assigns every
  fresh curve label an independent uniform element of $I_r$ (repeat queries
  return the stored value). Every randomized adaptive algorithm making at
  most $q$ distinct-label queries succeeds in finding a $B$-smooth order with
  probability at most $1 - (1 - alpha)^q$, and $q$ fresh queries attain the
  bound.
]

#proof[
  Fix the algorithm's coins. Conditional on any all-failure transcript, the
  value at the next fresh label is still independent and uniform on $I_r$, so
  it fails with probability exactly $1 - alpha$; induction over the (at most
  $q$) fresh queries gives failure probability at least $(1 - alpha)^q$, and
  repeated labels or early stopping cannot lower it. Averaging over coins
  proves the randomized bound; querying fresh labels until the first hit
  attains equality.
]

#corollary(name: "least query budgets")[
  #tag("PROVED") For $0 < alpha < 1$ and target success $delta in (0, 1)$,
  the least admissible budget is
  $q_delta = ceil(log(1 - delta) \/ log(1 - alpha))$.
]

#tag("EMPIRICAL", detail: "exact interval counts, 12–40 bits")
`random_order_lower_bound.py` evaluates the theorem without simulation, using
the exact smooth counts of each interval; exhaustive enumeration of all
answer sequences at small parameters matched $1 - (1 - alpha)^q$ exactly. At
40 bits the idealized 50%/95% budgets are 91/391 queries for $B = L^2$ and
6/25 for $B = L^3$ (#ref(<fig:budget>)); A001's observed first hits (65 and
6) are consistent with the idealized medians. This is a consistency check,
not evidence of independence — and the theorem is *model-only*: real curve
orders are structured, and coefficient-selecting algorithms are outside its
scope.

#fig("/figures/P2.1/budgets.svg", width: 80%, caption: [
  #tag("EMPIRICAL", detail: "exact Hasse-interval smooth counts, 12–40 bits")
  Exact optimal query budgets $q_(0.50)$ and $q_(0.95)$ in the iid
  Hasse-order oracle, from
  `random_order_lower_bound_b12-…-40_e{2,3}_20260629.csv`. The growth tracks
  $alpha^(-1)$, i.e. the reciprocal exact smooth density of the interval.
]) <fig:budget>

= The CM route: a sufficient condition and its finite coverage

Complex multiplication is the one classical technique that constructs a curve
*with prescribed order*. Its reach is governed by a single number-theoretic
condition that the campaign isolated exactly.

#definition(name: [the small-CM condition $sans("SCM")_(C,K)$])[
  #tag("PROVED") For fixed constants $C, K > 0$, say $sans("SCM")_(C,K)(r)$
  holds when there exist a negative fundamental discriminant $D$ and integers
  $t, v$ with
  $ abs(D) <= L^K, quad 4r = t^2 - D v^2, quad P^(+)(r + 1 - t) <= L^C . $
]

The norm equation $4r = t^2 - D v^2$ is the ordinary-CM reachability
criterion @msv2004, and a root of the Hilbert class polynomial $H_D$ modulo
$r$ supplies a CM $j$-invariant @enge2009.

#proposition(name: "witness search is cheap; curve construction is conditional")[
  #tag("PROVED") If $sans("SCM")_(C,K)(r)$ holds, an integer witness
  $(D, t, v)$ is findable in randomized expected $"poly"(L)$ time: enumerate
  the $O(L^K)$ fundamental discriminants, solve each norm equation by
  Cornacchia's algorithm with randomized modular square roots, and
  trial-divide each candidate order through $L^C$.
  #tag("CONDITIONAL", detail: "certified class-polynomial computation in poly(|D|, log r) time")
  The witness then yields the auxiliary curve: compute and factor $H_D$
  modulo $r$, lift a root to a curve, and select the trace-$t$ twist by exact
  point counting. Enge's $O(abs(D) log^(6+epsilon) abs(D))$ class-polynomial
  bound supplies the needed complexity under its explicitly stated
  floating-point precision heuristic @enge2009; the rigorous height bound
  permits certification but the sharp rounding analysis is not itself proved.
]

Thus a theorem establishing $sans("SCM")_(C,K)(r)$ for *every* prime $r$
would, modulo the stated CM implementation caveat, close P2.1 positively.
That theorem is precisely the blocking open question (§8).

== Coverage measurements through 60 bits

#tag("EMPIRICAL", detail: "32 primes/size at 12–40 bits; 128 primes/size at 44–60 bits")
`measure_cm_coverage.py` enumerates the exact $j = 0$ and $j = 1728$
twist-order families (validated exhaustively for $p in {7, 13, 17, 19, 31, 37}$)
and all ordinary principal-CM traces with bounded fundamental discriminant
(validated against a direct trace scan for $p in {101, 211}$,
$abs(D) <= 200$, and against known class numbers). #ref(<fig:cm>) plots
coverage of descending-prime ensembles. At the cubic bounds
$B = abs(D)_max = L^3$, *every* one of the 640 prime/size instances at 44–60
bits succeeded, while the constant-size explicit families decayed from
52\/128 (44 bits) to 15\/128 (60 bits) — matching the prediction that a
constant candidate list must fade.

#fig("/figures/P2.1/cm_coverage.svg", width: 90%, caption: [
  #tag("EMPIRICAL", detail: "descending-prime ensembles, 12–60 bits")
  Coverage by bounded-discriminant CM and by the explicit $j = 0, 1728$
  families, with Wilson 95% intervals. Ensembles: 32 primes per size through
  40 bits, 128 per size at 44–60 bits (discriminant bound $L^3$ throughout).
  Sources: `measure_cm_coverage_b12-…-40_p32_e2-3_d3` and
  `…_b44-…-60_p128_e2-3_d3` summary CSVs.
]) <fig:cm>

#tag("EMPIRICAL", detail: "4,096 descending 60-bit primes")
The large 60-bit scan sharpens the picture. With $B = 60^3 = 216000$:
bounded CM with $abs(D) <= 60^3$ covered 4096\/4096 (Wilson lower endpoint
0.99906); tightening the discriminant to $abs(D) <= 60^2 = 3600$ dropped
coverage to 3635\/4096 (rate 0.88745, CI 0.87741–0.89677); the explicit
families covered 445\/4096 (0.10864). Eight-worker wall times were 42.95 s
and 28.50 s. The hardest tested instance by the pre-registered
least-discriminant metric was $r = 1152921504606838643 equiv 11 thin (mod thin 12)$,
whose first hit needed $abs(D) = 180331$ with class number 87, $v = 2899546$,
$t = 1759425224$, and order largest prime factor 10,559 — a hardest *tested*
case, not a proved worst case.

#tag("EMPIRICAL", detail: "same 4,096-prime run") Coverage at
$abs(D) <= 60^2$ shows a strong residue effect modulo 12
(#ref(<fig:res>)): 97.07% for $r equiv 1$ but 76.48% for $r equiv 11$.
#tag("PROVED") The explicit-family half of this ordering has a concrete
explanation: the explicit list contains 10, 5, 7, and 1 distinct candidate
orders according as $r mod 12 = 1, 5, 7, 11$ — the $j = 1728$ family splits
when $r equiv 1 thin (mod thin 4)$ and the $j = 0$ family when
$r equiv 1 thin (mod thin 3)$.

#fig("/figures/P2.1/residues.svg", width: 72%, caption: [
  #tag("EMPIRICAL", detail: "4,096 descending 60-bit primes, B=60³, |D|≤60²")
  Bounded-CM coverage by residue class of $r$ modulo 12, with Wilson 95%
  intervals and success counts. Source:
  `measure_cm_coverage_b60_p4096_e3_d2_w8_20260625_residues.csv`.
]) <fig:res>

== Why finite coverage does not settle the asymptotics

#tag("HEURISTIC") For fixed $C, K$, the bounded scan exposes only $O(L^K)$
candidate orders. If their smoothness behaves like that of independent
integers near $r$ — the model the §3 measurements support — a union bound
gives success probability at most $L^K r^(-1\/C + o(1)) -> 0$. At 60 bits
the bound $L^3 = 216000 approx 2^(17.7)$ is far from the regime where this
estimate bites, so the perfect finite coverage and the pessimistic
asymptotic assessment are *consistent*. A proved correlation between small CM
discriminants and smooth norm-equation orders would falsify the assessment;
so would a proved anti-correlation falsify the route. Neither exists. This
tension — finite usefulness versus worst-case ignorance — is the honest
summary of the CM branch.

= Obstruction theorems: everything full except abelian varieties fails

Maurer–Wolf allow any constant-rank strongly algebraically defined abelian
auxiliary group, not only curves @maurerwolf1999. This section closes, one
class at a time, every such candidate whose *full* rational-point group is
used, leaving only abelian varieties standing. All results in this section
are unconditional.

== Full multiplicative groups

If $P^(+)(r - 1) <= (log r)^C$, the group $FF_r^times$ itself is a valid
auxiliary — the den Boer route, made concretely efficient in @bps2025 — and
no curve is needed. But this cannot be uniform:

#proposition(name: [the full $FF_r^times$ route fails on infinitely many primes])[
  #tag("PROVED") For every fixed $C$ there are infinitely many primes $r$
  with $P^(+)(r - 1) > (log r)^C$; consequently the full multiplicative
  group, and the full extension groups $FF_(r^n)^times$ for every $n >= 1$,
  are not uniform auxiliary groups.
]

#proof[
  #tag("CITED") Li's shifted-prime theorem gives infinitely many primes with
  $P^(+)(r - 1) > r^(0.679)$ @li2025, and $r^(0.679)$ eventually exceeds
  every fixed power of $log r$. Since $r - 1 divides r^n - 1$, the same
  family obstructs every full extension group; the additive group is
  unusable outright since its order is $r$.
]

== One-dimensional tori and bounded norm-one menus

The natural repair is the quadratic norm-one torus: for a nonsquare
$d in FF_r$,
$ T_d (FF_r) = {(x, y) : x^2 - d y^2 = 1}, quad
  (x, y)(u, v) = (x u + d y v, thin x v + y u), $
the kernel of the norm $FF_(r^2)^times -> FF_r^times$, cyclic of order
$r + 1$. #tag("PROVED") The rational maps
$ t |-> ((1 + d t^2)/(1 - d t^2), thin (2t)/(1 - d t^2)), quad quad
  t = y/(x + 1) $
are mutually inverse between $FF_r$ and $T_d (FF_r) without {(-1, 0)}$ (the
denominator cannot vanish since $d$ is a nonsquare), so the torus is a
strongly algebraically defined auxiliary of rank one whenever $r + 1$ is
smooth. #tag("EMPIRICAL", detail: "exhaustive, (r,d) = (7,3),(11,2),(13,2),(17,3)")
The parametrization, extraction, point count $r + 1$, and group-law closure
were verified exhaustively at toy scale (`torus_alternative.py`). The menu
${r - 1, r + 1}$, however, is also not uniform:

#theorem(name: [simultaneous obstruction for $r - 1$ and $r + 1$])[
  #tag("PROVED") There are an absolute constant $c > 0$ and infinitely many
  primes $r$ with
  $ min{P^(+)(r - 1), thin P^(+)(r + 1)} >= c thin r^(1\/10.4) . $
  Hence for every fixed $C'$, no algorithm choosing between the two full
  one-dimensional tori meets $(log r)^(C')$-smoothness for every prime.
]

#proof[
  For large $X$ pick primes $q in (X, 2X)$ and $s in (2X, 4X)$ and choose by
  CRT a residue $a$ with $a equiv 1 thin (mod thin q)$ and
  $a equiv -1 thin (mod thin s)$. Linnik's theorem with Xylouris's admissible
  exponent $L_0 = 5.2$ @xylouris2009 supplies a prime
  $r equiv a thin (mod thin q s)$ with $r <= C (q s)^(L_0) = O(X^(2 L_0))$.
  Then $q divides r - 1$ and $s divides r + 1$, so both largest prime factors are at
  least $X >= c thin r^(1\/(2 L_0))$, and letting $X -> oo$ yields an
  infinite family.
]

#tag("PROVED") The same CRT–Linnik synthesis extends to every *fixed finite
degree menu*: choosing for each $2 <= n <= D$ a comparable prime
$q_n equiv 1 thin (mod thin n)$ (fixed-progression PNT @soprounov1998) and a
residue of exact order $n$ modulo $q_n$ forces
$q_n divides (r^n - 1)\/(r - 1)$ for one Linnik prime $r$ simultaneously for all
$n <= D$, with $q_n >= c_D r^(1\/(D L_0))$. Thus every globally
bounded-degree menu of full norm-one tori is obstructed on an infinite prime
family.

#tag("PROVED") On the constructed family the standard random-shift subgroup
repair also fails: a $(log r)^(C')$-smooth subgroup must omit the forced
prime factor, so its size is $O(r^(1 - eta))$ with $eta = 1\/(2 L_0)$, and a
uniform shift lands in it with probability $O(r^(-eta))$ per attempt. This
bound is for the explicit shift-and-test model only.

== All full algebraic tori of bounded dimension

#theorem(name: "torus obstruction, general form")[
  #tag("PROVED") For every fixed $D >= 1$ there are constants
  $c_D, eta_D > 0$ and infinitely many primes $r$ such that *every*
  nontrivial full algebraic torus $T \/ FF_r$ of dimension at most $D$
  satisfies $P^(+)(abs(T(FF_r))) >= c_D thin r^(eta_D)$ — even when the
  torus is chosen after seeing $r$.
]

#proof[
  #tag("CITED") A $d$-dimensional torus has
  $abs(T(FF_r)) = det(r I - Phi)$ for the finite-order integral Frobenius
  action $Phi$ on its rank-$d$ character lattice @batyrevtschinkel1995.
  Since $Phi$ has finite order, its characteristic polynomial factors as
  $product_n Phi_n (x)^(e_n)$ into cyclotomic polynomials with
  $sum_n e_n phi(n) = d$, so
  $abs(T(FF_r)) = product_n Phi_n (r)^(e_n)$. Only indices in
  $cal(N)_D = {n : phi(n) <= D}$ can occur, and $cal(N)_D$ is finite: if
  $p^a divides n$ then $p^(a-1)(p - 1) divides phi(n)$. Put $k_D = abs(cal(N)_D)$.
  For large $X$ choose distinct primes $ell_n in (X, 2X)$ with
  $ell_n equiv 1 thin (mod thin n)$ for each $n in cal(N)_D$
  @soprounov1998, residues $b_n$ of exact multiplicative order $n$ modulo
  $ell_n$ (with $b_1 = 1$), and combine by CRT; Linnik @xylouris2009 gives a
  prime $r$ congruent to that residue with $r = O(X^(k_D L_0))$. Taking
  $X > D + 1$, the exact-order criterion forces $ell_n divides Phi_n (r)$ for
  every $n in cal(N)_D$, so every possible cyclotomic factor of every
  admissible torus order simultaneously contains a prime
  $>= X >= c_D r^(1\/(k_D L_0))$. Set $eta_D = 1\/(k_D L_0)$.
]

== Affine parts reduce everything to abelian varieties

#theorem(name: "Chevalley reduction")[
  #tag("PROVED") Among full rational-point groups of smooth connected
  commutative algebraic groups of globally bounded dimension over $FF_r$,
  every candidate with a nonzero affine part is obstructed on an infinite
  prime family. The only surviving full connected class is that of abelian
  varieties.
]

#proof[
  Chevalley's theorem gives a unique exact sequence
  $1 -> L -> G -> A -> 1$ with $L$ smooth connected affine commutative and
  $A$ an abelian variety @conrad2002. Over the perfect field $FF_r$ the
  unipotent radical $U subset.eq L$ is split with
  $abs(U(FF_r)) = r^(dim U)$, and $T = L \/ U$ is a torus @conrad2012.
  Lang's theorem @lang1956 makes the rational-point maps to connected
  quotients surjective, so the orders multiply:
  $abs(G(FF_r)) = abs(U(FF_r)) dot abs(T(FF_r)) dot abs(A(FF_r))$. If
  $dim U > 0$, the order is divisible by $r$ itself and is never
  polylog-smooth. If $U$ is trivial and $T$ nontrivial, the torus theorem
  above supplies the infinite family, and $abs(T(FF_r))$ divides the full
  order. What remains is $L$ trivial, i.e. $G = A$.
]

== Selected subgroups in dimension one

Full-group obstructions leave open the idea of embedding into a *smooth
subgroup* that omits the forced factor. A counting argument closes this in
dimension one, in the model that matters for the reduction.

#lemma(name: "public-coin counting")[
  #tag("PROVED") Let $S$ be a finite input set, $H$ a finite target group,
  and let public randomness $e$ (independent of $x in S$) select an encoder
  $f_e : S -> H union {bot}$ such that a decoder $d$ satisfies
  $d(e, f_e (x)) = x$ whenever $f_e (x) != bot$. Then
  $ 1/abs(S) sum_(x in S) op("Pr")_e [f_e (x) != bot] <= abs(H)/abs(S) . $
]

#proof[
  For fixed $e$, the successful restriction of $f_e$ is injective — two
  successful inputs sharing an image would force the decoder to return two
  values on one pair $(e, h)$. Hence the number of successful inputs at
  each $e$ is at most $abs(H)$; average over $e$.
]

#corollary(name: "no smooth selected subgroup of a one-dimensional torus")[
  #tag("PROVED") On the prime family of the torus obstruction, any
  $(log r)^C$-smooth subgroup $H$ of a one-dimensional torus omits a prime
  factor $ell >= c r^eta$ of the ambient order $O(r)$, so
  $abs(H) = O(r^(1 - eta))$; with $S = FF_r$, every correct public-coin
  recoverable encoding into $H$ has average success $O(r^(-eta))$. No such
  encoding has inverse-polylogarithmic success on every input.
]

#tag("PROVED") The same count does *not* close dimension two or higher: an
ambient order near $r^d$ can lose a factor $r^eta$ and still contain
$r$ elements. Higher-dimensional selected subgroups, private-coin encodings,
and abelian varieties are exactly the branches the lemma leaves open —
which is where the next section goes.

= The abelian-surface branch: conditional existence, explicit interface, missing seed

Dimension two enlarges the order interval from Hasse's
$4 sqrt(r)$ to $Theta(r^(3\/2))$ around $r^2$, moving the smooth-number
problem off the excluded endpoint $theta = 1\/2$. This buys a conditional
theorem — and isolates precisely what a construction still lacks.

== Conditional existence

#theorem(name: "polylog-smooth surface orders exist under RH")[
  #tag("CONDITIONAL", detail: "Riemann Hypothesis") For every sufficiently
  large prime $r$ there is an integer $N$ with $P^(+)(N) <= (log r)^(O(1))$
  in the central interval $[r^2 - lambda r^(3\/2), r^2 + lambda r^(3\/2)]$
  (any fixed $1\/2 < lambda < 4 - 2 sqrt(2)$), and $N$ is the order of an
  ordinary abelian surface over $FF_r$.
]

#proof[
  (Sketch; the full synthesis is recorded in attempt A007.) #tag("CITED")
  For any fixed $0 < lambda < 4 - 2 sqrt(2)$ and all large $r$, *every*
  integer in the displayed interval is the order of an ordinary abelian
  surface over $FF_r$ — the fixed-dimension prescribed-order theorem
  @vanbommel2025 (Theorem 1.7, Remark 1.11). The interval has length
  $Theta(r^(3\/2)) = Theta(X^(3\/4))$ around $X = r^2$, so it contains a
  subinterval $[X, X + X^(3\/4)]$. #tag("CITED") Under RH, the
  short-interval smoothness theorem of @younis2024 (Theorem 1.3) at
  $theta = 3\/4$ counts $y$-smooth integers there asymptotically for
  $y = (log X)^(K(3\/4))$; positivity of the count supplies the required
  $N$, and $log X = (2 + o(1)) log r$ makes $y$ polylogarithmic in $r$.
  #tag("PROVED") The synthesis is unavailable unconditionally from the
  checked sources: Younis's unconditional range at $theta = 3\/4$ requires
  $y >= exp((log X)^(2\/3 + epsilon))$, which is super-polylogarithmic.
]

== An explicit genus-two Jacobian would suffice

#proposition(name: "the Jacobian interface")[
  #tag("PROVED") Let $C : y^2 = f(x)$ be an explicitly supplied nonsingular
  genus-two curve over $FF_r$ ($f$ squarefree of degree five) with known
  $(log r)^(O(1))$-smooth Jacobian order. Then $J(C)(FF_r)$ is a
  constant-rank strongly algebraically defined Maurer–Wolf auxiliary group.
]

#proof[
  Jacobian elements have constant-size Mumford representations and Cantor's
  algorithm performs the group law in a constant number of bounded-degree
  polynomial operations @cantor1987, so the group is strongly algebraically
  defined. For embedding: given implicit $x$ and public random $e$, set
  $X = x + e$, test whether $f(X)$ is a square, and on success take an
  implicit square root $Y$; the divisor class $[(X, Y) - oo]$ has Mumford
  representation $u(z) = z - X$, $v(z) = Y$, and extraction reads $X$ from
  $u$ and returns $X - e$. The Weil bound
  $abs(sum_(X in FF_r) chi(f(X))) <= 4 sqrt(r)$ makes each trial succeed
  with probability $1\/2 + O(r^(-1\/2))$, so the expected number of trials
  is bounded. Finally, for every prime $ell != r$ the $ell$-torsion of a
  two-dimensional abelian variety embeds in $(ZZ \/ ell ZZ)^4$, so the group
  rank is at most four — a constant.
]

== Four output levels, and where the seed problem sits

#tag("PROVED") The following outputs are logically distinct, and only the
last is a Maurer–Wolf auxiliary: (1) an integral degree-four Weil polynomial
$f$ with $f(1) = N$; (2) a Honda–Tate certificate that an isogeny class with
polynomial $f$ exists @vanbommel2025; (3) a Howe–Nart–Ritzenthaler
certificate that the class contains a genus-two Jacobian @hnr2009; (4) an
explicit curve equation with group law and recoverable
$mono("EMBED")$/$mono("EXTRACT")$. Levels 1–3 specify coefficients, an
isogeny class, and an existence predicate — no projective model and no
coordinate algorithms.

#tag("EMPIRICAL", detail: "r = 251, 1019, 4091, 16363")
The exact ordinary cases of the HNR criterion are implementable with integer
arithmetic alone; `surface_jacobian_scan.py` enumerated every degree-four
ordinary Weil polynomial over four toy fields and intersected the resulting
order sets with segmented smoothness masks (#ref(<tab:scan>)). Every integer
in all four central intervals — 4.78 million integers in total, including
every $floor(L^3)$-smooth one — was the order of a Jacobian-containing
isogeny class. This strengthens the finite existence picture and constructs
*no* curve: the criterion certifies, it does not realize.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: (right, right, right, right, right, right),
    table.hline(stroke: 0.7pt),
    table.header([*$r$*], [*interval integers*], [*ordinary orders*],
      [*Jacobian-admissible*], [*$L^3$-smooth*], [*smooth admissible*]),
    table.hline(stroke: 0.5pt),
    [251], [7,953], [7,953], [7,953], [3,038], [3,038],
    [1,019], [65,057], [65,057], [65,057], [17,379], [17,379],
    [4,091], [523,329], [523,329], [523,329], [97,059], [97,059],
    [16,363], [4,186,243], [4,186,243], [4,186,243], [528,541], [528,541],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Exhaustive HNR scan of the central intervals
  $[r^2 - floor(r^(3\/2)), r^2 + floor(r^(3\/2))]$ (SG-14). Every interval
  integer, smooth or not, had an ordinary Jacobian-admissible Weil
  polynomial. Runtimes: 1.39 s (first three fields), 10.58 s (14-bit field).
  Data: `surface_jacobian_scan_b8-10-12_e3` and `_b14_e3` CSVs.],
) <tab:scan>

#tag("PROVED") The realization gap is a *seed problem*. Genus-two CM
constructions with prescribed Jacobian order have exponential worst-case
complexity @bhls2015, and the heuristic polynomial-time algorithm in the same
work prescribes $hash C(FF_p)$ — the curve's point count, not its Jacobian
order — so it solves a different inverse problem. An isogeny walk cannot
start without an explicit member of the target class, since isogenous
varieties share the Frobenius polynomial and walking presupposes a model to
walk from. And an abstract finite group of order $N$, even with ideal-module
data, instantiates neither the algebraic $mono("EMBED")$ map from implicit
field elements nor extraction — the interface a Jacobian gets from its
Mumford coordinate ($u(z) = z - (x + e)$ is *readable*), which an arbitrary
explicit surface would still have to supply separately.

Two exact algorithmic gaps therefore remain in this branch:

#keybox(title: "The two missing algorithms (surface branch)")[
  *(F)* #tag("PROVED") Given $r$, find a $(log r)^(O(1))$-smooth integer in
  the central $r^(3\/2)$-length interval around $r^2$ in
  $"poly"(log r)$ time. (Existence is guaranteed under RH; the analytic
  proof enumerates nothing.)

  *(R)* #tag("PROVED") Given $(r, N)$, output an explicit strongly
  algebraically defined abelian surface of order $N$ — an explicit
  genus-two Jacobian suffices — in $"poly"(log r)$ time. (Honda–Tate and
  HNR certify existence at every tested scale; no checked route outputs an
  equation.)
]

= Why the audited smooth-order finders fail

Gap (F) looks approachable: the target interval is long
($X^(3\/4)$ at scale $X = r^2$) and, under RH, provably contains smooth
integers. The campaign audited the standard algorithmic routes and closed
each with a proof. Throughout, $L = log X$ and the smoothness threshold is
$y = L^K$ for fixed $K > 1$.

== Boneh's CRT decoder misses the interval

#tag("CITED") Boneh's method finds every integer $N$ in an interval
$I = [U, V]$, $H = V - U$, whose gcd with
$S = product_(p < s) p^(floor(log_p s))$ exceeds a threshold
$T > S^epsilon$, where
$epsilon = sqrt(log(4H) \/ log S) + 5\/(4d)$ for a degree parameter $d$; if
$V < 2T$, every *strongly $s$-smooth* integer (all prime powers at most $s$)
in $I$ is found @boneh2002.

#proposition(name: "radius mismatch at polylogarithmic smoothness")[
  #tag("PROVED") At the surface scales $U asymp X$, $H = X^(3\/4 + o(1))$,
  listing all strongly smooth values forces $log T = (1 + o(1)) L$, and a
  necessary limit of Boneh's sufficient condition is
  $log(4H) < (log T)^2 \/ log S$. With $s = L^K$, the prime number theorem
  gives $log S = (1 + o(1)) s = L^(K + o(1))$, so the right side is
  $L^(2 - K + o(1)) = o(L)$ while $log H = (3\/4 + o(1)) L$. The decoder
  inequality fails for every choice of $d$ — even when the target is
  promised strongly $s$-smooth.
]

#tag("PROVED") The only asymptotic window the decoder does reach is
$s = c log X$ with $1 <= c <= 4\/3$: reaching a divisor of $S$ near $X$
needs $c >= 1$, and width $X^(3\/4)$ needs $c <= 4\/3$. But strongly
$c log X$-smooth integers are globally sparse — every one divides $S$ and
$log tau(S) <= pi(s) log(1 + log s \/ log 2) = o(log X)$, so there are at
most $X^(o(1))$ of them in total, and at most a fraction
$X^(-1\/4 + o(1))$ of the disjoint length-$X^(3\/4)$ intervals in $[X, 2X]$
contains one. No checked existence theorem places one in the special
intervals centered at $r^2$; Younis's theorem counts *ordinary* smooth
integers, a much larger class.

== Bounded-support products miss infinitely many prime centers

The next route represents the target as $N = product_(p <= y) p^(e_p)$ and
searches exponent vectors.

#theorem(name: "bounded-support coverage obstruction")[
  #tag("PROVED") Fix constants $K, k, C > 0$ and let $y = L^K$. In every
  sufficiently large dyadic range, some prime
  $r in [sqrt(X), sqrt(2X)]$ has *no* $y$-smooth integer supported on at
  most $k$ distinct primes within distance $C r^(3\/2)$ of $r^2$ — even
  when the $k$ supporting primes may be chosen from the whole factor base
  after seeing $r$.
]

#proof[
  Each admissible product in $[X\/2, 3X]$ has every exponent $O(L)$ and its
  support inside a set of $pi(y) = O(L^K)$ primes, so the number of such
  products is at most
  $sum_(j = 0)^k binom(pi(y), j) O(L)^j = L^(O_(K,k)(1))$, polynomial in
  $L$. For one fixed $N asymp X$, the condition
  $abs(N - r^2) <= C r^(3\/2)$ confines $r$ to an interval of length
  $O_C (X^(1\/4))$, since
  $abs(r - sqrt(N)) = abs(r^2 - N) \/ (r + sqrt(N))$ with
  $r, sqrt(N) asymp sqrt(X)$. All bounded-support products together
  therefore cover at most $X^(1\/4) L^(O_(K,k)(1))$ prime centers, while
  the prime number theorem puts $Theta(sqrt(X) \/ L)$ primes in
  $[sqrt(X), sqrt(2X)]$. Since
  $X^(1\/4) L^(O(1)) = o(sqrt(X) \/ L)$, some prime center is missed.
]

== Growing support hits an exponential-precision barrier

#proposition(name: "the safe rounding is exponentially precise")[
  #tag("PROVED") Encode an unrestricted exponent vector as a 0–1 subset sum
  by giving each prime $p <= y$ up to $floor(log(3X) \/ log p)$ copies of
  the weight $log p$; the item count $m$ satisfies
  $L^(K + o(1)) <= m <= L^(K + 1 + o(1))$. The target logarithmic interval
  has width $Delta = log(1 + H\/X) = Theta(X^(-1\/4))$, so a worst-case
  safe rounding at scale $Q$ needs $m\/Q = O(Delta)$, i.e.
  $Q = Omega(m X^(1\/4))$, and the rounded integer target has size
  $t = Theta(Q L) = X^(1\/4) L^(O_K (1))$ — exponential in the input
  length.
]

#tag("CITED") Substituting this target into Bringmann's
$tilde(O)(n + t)$ subset-sum algorithm @bringmann2017 gives exponential time
in $L$: the algorithm is pseudopolynomial, near-linear in the *numerical*
target. #tag("PROVED") The lattice alternative fares no better: at the
minimal safe scale the rounded instance has
$log_2 (max_i a_i) = Theta(L)$ and density
$m \/ log_2 (max_i a_i) -> oo$ for every fixed $K > 1$, far outside the
low-density regime of the Lagarias–Odlyzko success theorem
@lagariasodlyzko1985 — which is in any case distributional ("almost all
instances"), whereas repeated rounded copies of $log p$ form a highly
structured instance. #tag("CITED") The practical Smooth Subsum Search
heuristic is explicitly presented as a factorization heuristic and supplies
no every-interval worst-case theorem @hittmeir2023.

#tag("PROVED") Scope of these negatives: they close the audited generic
routes — bounded-support enumeration, pseudopolynomial dynamic programming
on the standard rounding, and low-density lattice guarantees. They are *not*
an impossibility theorem for every algorithm; a specialized method
exploiting the Diophantine structure of prime logarithms, or a different
representation of smooth values, is not covered. Under a polynomial-time
oracle for the structured logarithmic interval-subset-sum instance, the
finder gap (F) would close and only the realization gap (R) would remain.

= What remains open

The blocking question, recorded as P2.1/Q005, now has an exact shape.

*The uniform small-CM theorem.* Prove that for some fixed $C, K$, every
prime $r$ satisfies $sans("SCM")_(C,K)(r)$ — i.e. the norm-equation family
${r + 1 - t : 4r = t^2 - D v^2, thin abs(D) <= L^K}$ of $O(L^K)$ candidate
orders always contains an $L^C$-smooth member. The 4,096-prime experiment
makes this plausible at 60 bits and the random-integer heuristic makes it
implausible asymptotically; a proved correlation in either direction would
be decisive. Together with a certified CM implementation @enge2009, a
positive answer closes P2.1.

*The two surface algorithms.* Under RH the existence side is settled in
dimension two; gaps (F) and (R) of §6 are precisely what remain. For (F),
§7 shows the answer must exploit structure the generic routes ignore. For
(R), the missing step is a single explicit genus-two Jacobian seed in a
prescribed isogeny class — CM is exponential @bhls2015, walks need a seed,
and abstract groups lack the embedding interface.

*Higher-dimensional selected subgroups.* The public-coin counting lemma
dies in dimension two ($abs(H) >= r$ survives the forced-factor loss). The
recorded next action is an audit of higher-dimensional selected subgroups
and cofactor-projection encodings, where the dimension-one cardinality
obstruction no longer applies.

*The hardness branch.* P2.1's alternative resolution — an infinite prime
family on which no polylog-smooth auxiliary curve exists, or finding one is
hard — is equally open. The obstruction technology of §5 (CRT + Linnik
against explicit order polynomials) does not apply to curve orders, whose
traces do not factor through cyclotomic values; and the iid-oracle bound of
§3 is model-only. No lower bound is known in a model containing the real
algebraic construction algorithms.

= Conclusion

P2.1 asked for a uniform polynomial-time construction of a polylog-smooth
auxiliary curve — the one missing ingredient of the Maurer CDH-to-DLP
equivalence — or evidence that none exists. Ten sessions produced a partial
but sharply structured answer. Unconditionally: every full connected
commutative auxiliary group with any affine part is dead on an infinite
prime family, by a single CRT–Linnik mechanism pushed through the character
lattice and Chevalley decomposition (§5); dimension-one selected subgroups
are dead in the recoverable-encoding model; and the generic smooth-order
finders — CRT decoding, bounded-support products, safe-rounded subset sums —
are dead at the surface interval scale (§7). Conditionally: under RH, a
polylog-smooth ordinary abelian-surface order exists over every large prime
field, and an explicit genus-two Jacobian of that order would finish the
reduction (§6). Empirically: bounded-discriminant CM covers every tested
prime through 60 bits at cubic bounds, while its asymptotic status hangs on
an unproved correlation (§4). The frontier is exact: prove
$sans("SCM")_(C,K)$ uniformly, or find the smooth surface order and its
Jacobian seed in polynomial time, or push the obstructions into abelian
varieties themselves. None of these is closed here, and we have been
careful to claim only what the record supports.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
All experiments run under Python 3.13 on the repository's deterministic
harness; every executable module carries known-answer tests (315 repository
tests pass, including six P2.1 validation entry points). The measurement
scripts are `measure_smooth_orders.py` (seeded blind search; BSGS/twist
counter validated against exhaustive enumeration; 20.67 s full run),
`measure_cm_coverage.py` (norm-equation and explicit-family scan; Cornacchia
solving, class numbers via reduced forms, Wilson intervals; 747.32 s serial
five-size run, 28.50 s and 42.95 s for the eight-worker 4,096-prime runs),
`summarize_cm_residues.py` (residue aggregation), `random_order_lower_bound.py`
(exact iid-oracle budgets, no Monte Carlo), `torus_alternative.py`
(exhaustive norm-one torus validation), and `surface_jacobian_scan.py`
(exact ordinary HNR criterion; 1.39 s and 10.58 s recorded runs). The
figures in this paper are generated directly from the recorded CSVs:
`measure_smooth_orders_…_summary.csv` (#ref(<fig:smooth>)),
`random_order_lower_bound_…_e{2,3}.csv` (#ref(<fig:budget>)),
`measure_cm_coverage_…_{p32,p128}_…_summary.csv` (#ref(<fig:cm>)), and
`measure_cm_coverage_b60_p4096_e3_d2_w8_…_residues.csv` (#ref(<fig:res>)).
Every mathematical claim above carries the epistemic tag under which it was
closed in the research log; untagged sentences are exposition, not claims.
Finite ensembles are deterministic toy experiments through
$log_2 r <= 60$ and are never universal proof.
]

#bibliography("refs/P2.1.bib", title: [References], style: "ieee")
