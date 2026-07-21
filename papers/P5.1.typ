#import "lib/paper.typ": *

#show: paper.with(
  title: "Certified Constants and an Exact CM Reproduction for Koblitz's Prime-Order Conjecture",
  subtitle: "A finite-level quotient certificate for 540.f2, a fifty-checkpoint table verification to one billion, and the norm-pair form of the j = 1728 prime-order event",
  pid: "P5.1",
  keywords: ("Koblitz conjecture", "elliptic curves", "prime order", "adelic Galois image", "Euler products", "CM curves", "sieve parity"),
  abstract: [
    Koblitz conjectured in 1988 that a fixed non-CM elliptic curve $E \/ QQ$
    without congruence obstruction has $tilde.op C_(E,1) x \/ (log x)^2$ primes
    $p <= x$ of good reduction for which $hash E(FF_p)$ is prime; Zywina later
    corrected the constant through the adelic Galois image, which can force
    $C_(E,1) = 0$. This paper reports a five-session research program on P5.1
    that closes every algebraic, computational, and source-audit sub-goal within
    reach of exact finite computation, and states precisely what remains open.
    We reproduce Zywina's universal Euler product and Serre-curve constant to
    within $4 dot 10^(-8)$, measure prime-order densities for three non-CM
    curves through $x = 2^17$ (observed/predicted $1.043$ for the Serre curve
    1728.w1; zero events, as proved, for curves with rational 2- and 3-torsion),
    and certify a quotient constant $C_(E,3) = (5824\/5913) C$ for the 3-torsion
    curve 540.f2 by exhaustively enumerating its 699,840-element mod-90 Galois
    image — a result conditional only on LMFDB's published adelic data. For the
    CM curve $y^2 = x^3 - x$ we implement Walsh's exact trace formula and
    reproduce all 50 checkpoints of Zywina's published table through $x = 10^9$
    with zero mismatches (final observed/predicted $0.99943$). On the theory
    side we prove an exact reduction: apart from the single exceptional prime
    $p = 17$, every CM prime-quotient event lies in the class $p ≡ 5 (mod 8)$
    and is precisely the simultaneous primality of the two Gaussian norms
    $N(a + b i)$ and $N(a + b i + 1)\/8$ — a prime-pair pattern that makes the
    sieve parity obstruction explicit. An audit of the 2025–2026 primary
    literature confirms that the unconditional fixed-curve asymptotic remains
    open; we trace exactly where GRH-strength hypotheses enter the strongest
    partial results and isolate the two logically independent missing
    ingredients. Every computation is deterministic, adversarially
    self-verified, and reproducible from seeded scripts.
  ],
)

= Introduction

Elliptic-curve cryptography wants curves whose group of rational points over a
prime field has prime order, and Koblitz's original question @koblitz1988 is the
natural arithmetic-statistics version: fix one curve $E \/ QQ$ and ask how often
its reductions $E(FF_p)$ have prime order as $p$ ranges over primes of good
reduction. Writing $N_p = hash E(FF_p) = p + 1 - a_p$ with $abs(a_p) <= 2 p^(1\/2)$
by Hasse, the count of prime $N_p$ up to $x$ is conjecturally governed by the
same $x \/ (log x)^2$ scale as twin primes, with a curve-specific constant.
Koblitz built the constant as a product of local densities read from the mod-$ell$
Galois images @koblitz1988; Zywina later showed that independence across primes
$ell$ can fail — division fields entangle — and replaced the naive product by a
finite-level adelic density limit which corrects the constant and can make it
vanish @zywina2011. The corrected conjecture has survived every published
numerical test, yet no fixed-curve instance has ever been proved, and the 2025
literature still describes it as open @lmw2025 @dey2025.

This paper is the record of research problem P5.1: measure the conjecture
honestly at reachable ranges, certify every constant used rather than fitting
anything, reproduce the strongest published computation exactly, and determine —
by proof where possible, by source audit where not — exactly what separates the
finite evidence from the asymptotic theorem. The work spans five sessions,
twelve closed sub-goals (SG-01 through SG-12), 85 passing tests, and three
deterministic data-producing scripts whose outputs back every figure and table
below.

#keybox(title: "Main findings")[
  *(1)* #tag("EMPIRICAL", detail: "all good primes 5 ≤ p ≤ 2^17") The corrected
  predictors track the data at toy scale: the Serre curve 1728.w1 gives
  observed/predicted $1.04293$ (683 prime orders vs. 654.886 predicted), the
  rational-torsion curves give exactly zero prime orders as proved, and a
  certified quotient constant for 540.f2 gives ratio $1.01600$.

  *(2)* #tag("CONDITIONAL", detail: "LMFDB 540.f2 adelic data") Exact
  enumeration of the level-90 Galois image ($699,840$ matrices, $98,280$
  favorable) proves $delta_(E,3)(90) = 91\/648$ and hence
  $C_(E,3) = (5824\/5913) C$ for $y^2 = x^3 + 3 x - 11$.

  *(3)* #tag("EMPIRICAL", detail: "all 50 checkpoints, 2·10^7 ≤ x ≤ 10^9") An
  independent exact implementation — Cornacchia representations plus Walsh's
  trace theorem — reproduces every actual count and every rounded expected
  count in Zywina's published CM table with zero mismatches, in 148.7 seconds.

  *(4)* #tag("PROVED") For $E : y^2 = x^3 - x$, apart from the single event
  $(p, N_p\/8) = (17, 2)$, every prime-quotient event has $p ≡ 5 (mod 8)$ and
  equals the simultaneous primality of $N(a + b i)$ and $N(a + b i + 1)\/8$ in
  $ZZ[i]$. The missing unconditional theorem is therefore a prime-pair
  distribution statement, not a missing trace formula, density, or test.
]

== Honest scope

Nothing in this paper proves the Koblitz asymptotic, and no amount of the
computation reported here could: a larger finite cutoff cannot by itself turn
evidence into an asymptotic theorem. #tag("PROVED") What the computations do is
eliminate every non-asymptotic explanation for a failure — wrong constant, wrong
predictor, wrong point counts, circular validation — through independent
cross-checks (§8), so that the surviving gap is exactly the open conjecture
recorded as Q026 (§7). The strongest 2025 fixed-curve result remains conditional
on two unproved hypotheses @dey2025, and the strongest unconditional results are
averages over families @lmw2025 or almost-prime statements @xie2025 @davidwu2012.

= Setting and notation

Fix an elliptic curve $E \/ QQ$ with conductor $N_E$. For a prime $p divides.not N_E$
of good reduction write $N_p = hash E(FF_p) = p + 1 - a_p$, $abs(a_p) <= 2 p^(1\/2)$.
Koblitz's conjecture in Zywina's corrected form @koblitz1988 @zywina2011 reads:

#tag("CONJECTURE") For $E \/ QQ$ non-CM and $t >= 1$ a fixed integer,
$
  hash { p <= x : p divides.not N_E, #h(0.3em) N_p \/ t "an integer and prime" }
  tilde.op C_(E,t) frac(x, (log x)^2),
$
where $C_(E,t) >= 0$ is defined from the adelic Galois image
$rho_E : "Gal"(overline(QQ) \/ QQ) -> "GL"_2 (hat(ZZ))$ as a divisibility-ordered
limit of finite-level densities; the constant captures entanglement between
division fields and can vanish @zywina2011. The case $t = 1$ is the prime-order
conjecture; Koblitz's original positive-constant statement additionally excludes
curves $QQ$-isogenous to curves with nontrivial rational torsion @koblitz1988.

Two normalizations of the finite-cutoff prediction matter below. The *raw
asymptotic predictor* is $C_(E,t) x \/ (log x)^2$. The *refined predictor* of
Zywina §2.4 replaces the asymptotic mass by a prime sum,
$
  "Pred"_t (x) = C_(E,t) sum_(p <= x) frac(1, log(p + 1) - log t),
$
which converges to the same asymptotic but is far less biased at small $x$
@zywina2011. #tag("EMPIRICAL", detail: "p ≤ 2^17") The distinction is not
cosmetic at toy range: for the Serre curve below, the raw predictor is off by
$28.9%$ at $x = 2^17$ while the refined predictor is off by $4.3%$
(#ref(<fig:serre>)).

Throughout, $C$ denotes Zywina's *universal constant*, the value of $C_(E,1)$
for a curve with maximal image at every level (equation (2.3) of @zywina2011),
and all measurements use the fixed seed 51012026 and deterministic pipelines.

= Corrected constants and their certificates

== The universal Euler product

#tag("CITED") For a non-CM curve whose mod-$ell$ image is all of
$"GL"_2 (FF_ell)$, the local factor at $ell$ is
$
  f_ell = 1 - frac(ell^2 - ell - 1, (ell - 1)^3 (ell + 1)),
$
and the universal product is
$
  C = product_ell f_ell = 0.505166168239435774 dots
$
(Zywina @zywina2011, Proposition 2.4 and equation (2.3)). Each factor compares
the density of image matrices without eigenvalue 1 — the Frobenius classes
forcing $ell divides N_p$ — against the density $1 - 1\/ell$ for a random
integer.

#tag("EMPIRICAL", detail: "Euler factors ℓ ≤ 10^6") Our implementation
truncates the product over primes $ell <= 10^6$ and returns
$0.505166202477432$, within $3.43 dot 10^(-8)$ of the published limit; a
60-digit recomputation during the audit differs from the float value by
$9.0 dot 10^(-15)$ (§8).

== The Serre curve 1728.w1

#tag("CITED") The curve $E_0 : y^2 = x^3 + 6 x - 2$ (LMFDB 1728.w1 @lmfdb) is a
Serre curve — its adelic image is as large as the Weil pairing and the
Kronecker–Weber entanglement allow — and Zywina computes its corrected constant
in closed form:
$
  C_(E_0, 1) = frac(10, 9) C approx 0.561295742488261971
$
(@zywina2011, Section 5 and equation (5.1)). The factor $10\/9$ is exactly the
entanglement correction that the naive local product misses.
#tag("EMPIRICAL", detail: "Euler factors ℓ ≤ 10^6") The implemented constant is
$0.561295780530480$, within $3.80 dot 10^(-8)$ of the published value.

== The rational-torsion obstruction

#proposition(name: [vanishing for rational torsion])[
  #tag("PROVED") Let $E \/ QQ$ have a rational point of prime order
  $t in {2, 3}$. Then for every good prime $p > t$ the reduction satisfies
  $t divides N_p$, so $N_p$ is composite whenever $N_p > t$; in particular
  prime orders occur for at most finitely many $p$ and $C_(E,1) = 0$.
]

#proof[
  Reduction modulo a good prime $p$ is injective on prime-to-$p$ rational
  torsion, so the order-$t$ point survives into $E(FF_p)$ and $t divides N_p$
  by Lagrange. Hasse gives $N_p >= p + 1 - 2 p^(1\/2) = (p^(1\/2) - 1)^2 > t$
  for all $p >= 7$, so beyond finitely many primes $N_p$ is a multiple of $t$
  exceeding $t$, hence composite. The corrected constant, which is an average
  of densities of prime values, is then zero @zywina2011.
]

The two test curves realizing this obstruction are
$y^2 = x^3 + x - 2$ (LMFDB 112.b4, torsion order 2 @lmfdb) and
$y^2 = x^3 + 3 x - 11$ (LMFDB 540.f2, torsion $ZZ \/ 3 ZZ$ generated by
$(3, 5)$ @lmfdb).

#remark(name: "both curves are non-CM")[
  #tag("PROVED") The point $(3, 5)$ has order 3 on 540.f2: the tangent slope at
  $(3,5)$ is 3, and the duplication formula gives $2(3,5) = (3,-5) = -(3,5)$.
  Neither curve has CM: their $j$-invariants are $432\/7$ and $6912\/125$, and a
  CM $j$-invariant is an algebraic integer, so a rational CM $j$-invariant must
  be a rational integer @silverman2009.
]

== A certified finite-level quotient constant for 540.f2

Since $C_(E,1) = 0$ for 540.f2, the refined conjecture moves to the quotient
$t = 3$: how often is $N_p \/ 3$ prime? Zywina's Proposition 2.4 reduces
$C_(E,t)$ for a non-CM curve with adelic level $M$ to one exact finite-level
density $delta_(E,t)$ at modulus $t product_(ell divides t M) ell$, times the
universal factors at all other primes @zywina2011.

#tag("CITED") LMFDB records the adelic image of 540.f2 as level $M = 30$, index
16, label `30.16.0-30.b.1.4`, with seven explicit generators modulo 30 @lmfdb.
With $t = 3$ and $M = 30$ the required modulus is $3 (2 dot 3 dot 5) = 90$.

#proposition(name: [exact level-90 density])[
  #tag("CONDITIONAL", detail: "LMFDB 540.f2 level and generators correct")
  Let $G(30) subset "GL"_2 (ZZ \/ 30 ZZ)$ be the subgroup generated by LMFDB's
  seven generators, and let $G(90)$ be its full preimage set of entrywise lifts.
  Exhaustive computation gives $abs(G(30)) = 8640$, hence
  $abs(G(90)) = 8640 dot 3^4 = 699,840$; among these exactly $98,280$ matrices
  $A$ satisfy $gcd(det(I - A), 90) = 3$, the condition that $N_p \/ 3$ be
  coprime to 90. Therefore
  $
    delta_(E,3)(90) = frac(98280, 699840) = frac(91, 648).
  $
]

The condition $det(I - A) in 3 (ZZ \/ 90 ZZ)^times$ is equivalent to
$gcd(det(I - A), 90) = 3$ because $90 = 2 dot 3^2 dot 5$ and divisibility of
$N_p \/ 3$ by 2, 3, or 5 is read off modulo 90. Assembling the constant per
Proposition 2.4: dividing $91\/648$ by the random-integer densities
$(1 - 1\/2)(1 - 1\/3)(1 - 1\/5) = 4\/15$ gives $455\/864$; the universal factors
at the entangled primes are $f_2 = 2\/3$, $f_3 = 27\/32$, $f_5 = 365\/384$ with
product $1095\/2048$; hence

$
  C_(E,3) = frac(455\/864, 1095\/2048) C = frac(5824, 5913) C
  approx 0.497562652330215 .
$

#tag("EMPIRICAL", detail: "Euler factors ℓ ≤ 10^6") The numerical value uses
the truncated universal product. #tag("PROVED") The factor $5824\/5913$ was
derived by exact rational arithmetic and was *not* fitted to the measured
quotient counts; an independent CRT-decomposed recount during the audit
reproduced all three fractions (§8). We flag one boundary of trust explicitly:
the certificate consumes LMFDB's published level-30 generators as input and
does not re-derive them from division polynomials.

= The CM curve $y^2 = x^3 - x$: exact trace and the norm-pair reduction

CM curves need a separate formulation @koblitz1988 @zywina2011. For
$E : y^2 = x^3 - x$ ($j = 1728$), all CM endomorphisms are defined over
$QQ(i)$, the torsion of $E(QQ(i))$ has order 8, and a rational prime
$p ≡ 3 (mod 4)$ is supersingular with $N_p = p + 1$. #tag("CITED") The CM
conjecture therefore studies $N_p \/ 8$ on the *split* stratum
$p ≡ 1 (mod 4)$ only, with constant
$
  C_(E_(QQ(i)), 8)
  = product_(ell eq.not 2)
    lr(( 1 - chi(ell) frac(ell^2 - ell - 1, (ell - chi(ell)) (ell - 1)^2) ))
  approx 1.067350894,
$
where $chi(ell) = (-1)^((ell - 1)\/2)$; the product is evaluated absolutely
convergently after extracting $L(1, chi)^(-1) = 4 \/ pi$ (@zywina2011, Lemma
7.1). #tag("EMPIRICAL", detail: "Euler factors ℓ ≤ 10^6") Our accelerated
implementation returns $1.067350966817026$, within $7.3 dot 10^(-8)$ of the
published approximation.

== Walsh's trace formula, specialized

#tag("CITED") For $E_d : y^2 = x^3 + d x$ and a split prime $p = a^2 + b^2$
normalized by $a ≡ 1 (mod 4)$, $b$ even, Walsh determines
$a_p in {plus.minus 2 a, plus.minus 2 b}$ from the quartic-residue class of $d$
@walsh2022. #tag("PROVED") For $d = -1$: since $-1$ is a fourth power modulo
$p$ exactly when $p ≡ 1 (mod 8)$, Walsh's cases specialize to
$
  a_p = cases(
    2 a & "if" p ≡ 1 (mod 8),
    -2 a & "if" p ≡ 5 (mod 8),
    0 & "if" p ≡ 3 (mod 4),
  )
$
so $N_p$ is computable from one Cornacchia representation of $p$ — an
$O(log p)$ computation replacing the $O(p^(1\/4))$-group-operation BSGS
counter. This is what makes the $x = 10^9$ reproduction of §5.4 feasible in
pure Python.

== The norm identity and its consequences

Everything in this subsection is unconditional given Walsh's cited theorem; the
complete derivations are in the repository's `THEORY_CLOSURE.md`.

#theorem(name: [norm form of the CM order])[
  #tag("PROVED") Let $p ≡ 1 (mod 4)$ be prime, $p = a^2 + b^2$ with
  $a ≡ 1 (mod 4)$. Put $epsilon_p = 1$ if $p ≡ 1 (mod 8)$ and
  $epsilon_p = -1$ if $p ≡ 5 (mod 8)$. Then
  $
    N_p = p + 1 - 2 epsilon_p a = (a - epsilon_p)^2 + b^2
        = N_(ZZ[i] \/ ZZ)(a + b i - epsilon_p).
  $
]

#proof[
  Substitute $p = a^2 + b^2$ into $p + 1 - 2 epsilon_p a$ and use
  $epsilon_p^2 = 1$: the result is $(a - epsilon_p)^2 + b^2$, which is the
  Gaussian norm of $a + b i - epsilon_p$.
]

#lemma(name: [divisibility by 8])[
  #tag("PROVED") In the setting of the theorem, $8 divides N_p$. More
  precisely, $16 divides N_p$ when $p ≡ 1 (mod 8)$, while
  $N_p ≡ 8 (mod 16)$ when $p ≡ 5 (mod 8)$.
]

#proof[
  If $p ≡ 1 (mod 8)$: $a$ is odd so $a^2 ≡ 1 (mod 8)$, forcing
  $b^2 ≡ 0 (mod 8)$, hence $4 divides b$; and $a ≡ 1 (mod 4)$ gives
  $4 divides a - 1$. Then $(a-1)^2$ and $b^2$ are both $≡ 0 (mod 16)$.
  If $p ≡ 5 (mod 8)$: now $b^2 ≡ 4 (mod 8)$ forces $b ≡ 2 (mod 4)$, and
  $a + 1 ≡ 2 (mod 4)$; each of $(a+1)^2, b^2$ is $≡ 4 (mod 16)$, so their sum
  is $≡ 8 (mod 16)$.
]

#proposition(name: [the class $p ≡ 1 (mod 8)$ is finite])[
  #tag("PROVED") If $p ≡ 1 (mod 8)$, then $N_p \/ 8$ is even, and it is prime
  only for $p = 17$, where $N_p \/ 8 = 2$.
]

#proof[
  By the lemma $16 divides N_p$, so $N_p \/ 8$ is even; if prime it must equal
  2, i.e. $N_p = 16$. The equation $(a - 1)^2 + b^2 = 16$ with $4 divides a - 1$
  and $4 divides b$ admits $(a, b) = (1, plus.minus 4)$, giving the prime
  $p = 17$, and $(a - 1, b) = (plus.minus 4, 0)$, giving $p = a^2 in {9, 25}$,
  not prime. Hence $p = 17$ is the only event in this class.
]

#corollary(name: [the norm-pair reduction])[
  #tag("PROVED") Apart from the single event $(p, N_p \/ 8) = (17, 2)$, every
  prime $p$ with $N_p \/ 8$ prime satisfies $p ≡ 5 (mod 8)$ and
  $
    p = N(a + b i), quad quad frac(N_p, 8) = frac(N(a + b i + 1), 8),
  $
  i.e. the CM Koblitz event is exactly the *simultaneous* primality of two
  explicit Gaussian norms. Writing $u = (a + 1)\/2$ and $v = b\/2$ (both odd),
  the second value is the integral quadratic-form value
  $
    frac(N_p, 8) = frac(u^2 + v^2, 2)
    = lr(( frac(u + v, 2) ))^2 + lr(( frac(u - v, 2) ))^2 .
  $
]

#tag("EMPIRICAL", detail: "all 74,416 split primes 5 ≤ p ≤ 2·10^6") An
independent Session-5 check verified the norm identity, the divisibility by 8,
and the uniqueness of the $(17, 2)$ event on every split prime in range; a
persistent regression repeats the identity through $10^5$.

#tag("HEURISTIC") The reduction explains the parity barrier: the event is a
Gaussian-integer analogue of a prime-pair problem, precisely the shape on which
classical sieves lose to parity. This explanatory analogy would be falsified if
a sieve using only divisibility data proved the required prime lower bound
without a parity-breaking input.

= Empirical validation

All measurements use exact point counting — the shared Hasse-interval
BSGS/twist counter with a declared exhaustive fallback for the non-CM sweeps,
and the Cornacchia–Walsh trace for the CM reproduction — validated against
exhaustive counts at small primes before each run. #tag("EMPIRICAL", detail:
"67 validation cases, p ≤ 97") The production counter agreed with exhaustive
counting on all validation cases (66 via BSGS/twist, one via the declared
fallback). PARI/GP and SageMath were unavailable in the environment; the
pure-Python counter substitutes for them and is itself cross-validated (§8).

== Non-CM prime-order densities through $x = 2^17$

#figure(
  table(
    columns: (1fr, auto, auto, auto, auto, auto, auto),
    align: (left, center, center, center, center, center, center),
    table.hline(stroke: 0.7pt),
    table.header(
      [*Curve*], [*Torsion*], [*$C_(E,1)$*], [*Good $p$*],
      [*Prime $N_p$*], [*Refined pred.*], [*Obs./pred.*],
    ),
    table.hline(stroke: 0.5pt),
    [1728.w1 \ $y^2 = x^3 + 6x - 2$], [trivial], [$(10\/9) C$],
      [12,249], [683], [654.886], [1.04293],
    [112.b4 \ $y^2 = x^3 + x - 2$], [$ZZ\/2ZZ$], [0],
      [12,248], [0], [0], [—],
    [540.f2 \ $y^2 = x^3 + 3x - 11$], [$ZZ\/3ZZ$], [0],
      [12,248], [0], [0], [—],
    table.hline(stroke: 0.7pt),
  ),
  caption: [#tag("EMPIRICAL", detail: "all good primes 5 ≤ p ≤ 2^17") The
  three-curve sweep at the largest cutoff. Data:
  `measure_density_x131072_l1000000_s51012026_20260624.csv`, seed 51012026,
  11.2 s wall time.],
) <tab:density>

#ref(<tab:density>) summarizes the largest cutoff. Three observations, in
decreasing order of strength.

*Zero is exact.* #tag("EMPIRICAL", detail: "p ≤ 2^17") Both rational-torsion
curves produced *no* prime orders across 12,248 good primes each — the
obstruction of Proposition 1 realized in data. With zero events the heuristic
95% upper bound on the measured constant is $-ln(0.05)\/B(x) approx 0.00257$
at $x = 2^17$ (where $B(x)$ is the refined baseline), consistent with
$C_(E,1) = 0$ and two orders of magnitude below the Serre-curve constant. A
single contrary reduction would have falsified the implementation, since
reduction injects prime-to-$p$ torsion.

*The refined predictor matters.* #tag("EMPIRICAL", detail: "p ≤ 2^17") For
1728.w1 the refined prediction is $654.886$ against 683 observed
(ratio $1.04293$), while the raw asymptotic expression $C_(E_0,1) x\/(log x)^2$
predicts only $529.85$ (ratio $1.28904$). #ref(<fig:serre>) shows both ratios
across cutoffs $2^10 <= x <= 2^17$: the refined ratio moves
$0.8030, 1.0372, 1.1561, 1.0950, 1.0944, 1.0567, 1.0466, 1.0429$ — into and
then along the heuristic band — while the raw ratio stays above $1.28$
throughout.

*The interval is heuristic.* #tag("HEURISTIC") Treating the 683 events as
approximately Poisson gives the 95% interval $[0.9647, 1.1211]$ for
observed/predicted, which contains 1; cross-prime dependence or finite-cutoff
bias could invalidate this interval, so we report it as a heuristic band, not a
confidence statement.

#fig("/figures/P5.1/serre_convergence.svg", width: 78%, caption: [
  #tag("EMPIRICAL", detail: "5 ≤ p ≤ 2^17") Observed/predicted prime-order
  counts for the Serre curve 1728.w1 under the refined prime-sum predictor
  (blue) and the raw asymptotic predictor (orange), with the heuristic Poisson
  band around the refined ratio. Data:
  `measure_density_x131072_l1000000_s51012026_20260624.csv`.
]) <fig:serre>

== Certified quotient cases and a negative control

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    align: (left, center, center, center, center, center),
    table.hline(stroke: 0.7pt),
    table.header(
      [*Case*], [*Eligible $p$*], [*Events*], [*Predicted*],
      [*Obs./pred.*], [*Measured const. [95%]*],
    ),
    table.hline(stroke: 0.5pt),
    [540.f2, $t = 3$, all good $p$], [12,248], [661], [650.592], [1.01600],
      [0.5055 [0.4670, 0.5441]],
    [$y^2 = x^3 - x$, $t = 8$, split $p$], [6,094], [765], [779.701], [0.98114],
      [1.0472 [0.9730, 1.1214]],
    [pooled full-$"GL"_2$ control, $t = 8$], [all good $p$], [987], [243.653],
      [4.05084], [—],
    table.hline(stroke: 0.7pt),
  ),
  caption: [#tag("EMPIRICAL", detail: "5 ≤ p ≤ 2^17, seed 51012026") Quotient
  cases at the largest cutoff. The certified constants are $0.497563$ (540.f2)
  and $1.067351$ (CM); both measured intervals contain their predictions. The
  deliberately invalid pooled model is a negative control. Data:
  `measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv`.],
) <tab:corrected>

#tag("EMPIRICAL", detail: "p ≤ 2^17") The certified 540.f2 constant of §3.4
predicts 650.592 quotient-prime events; the sweep observed 661, ratio
$1.015998$, and the measured-constant interval $[0.466985, 0.544060]$ contains
the certified prediction $0.497563$. The ratio across cutoffs
$2^10 <= x <= 2^17$ is $1.0767, 1.1480, 0.9618, 1.1734, 1.0715, 1.0232,
0.9796, 1.0160$ (#ref(<fig:corrected>)). Because the constant was derived by
exact finite-group enumeration *before* comparison — never fitted — this
agreement is a genuine test of Zywina's Proposition 2.4 on a curve with an
entangled level-30 image.

#tag("EMPIRICAL", detail: "split primes ≤ 2^17") The CM case observed 765
events among 6,094 split primes against 779.701 predicted, ratio $0.981145$,
rising steadily with cutoff from $0.8443$ at $x = 2^10$ (#ref(<fig:corrected>));
the measured interval again contains the published constant.

#tag("EMPIRICAL", detail: "all good rational primes ≤ 2^17") The *negative
control* pools the CM curve's split and supersingular strata and applies the
inapplicable full-$"GL"_2$ quotient model: it predicts 243.653 events but 987
occur — ratio $4.05084$. The split-prime convention is mathematically
substantive, not presentational: using the wrong stratum model fails by a
factor of four while both certified predictors sit within a few percent of 1.

#fig("/figures/P5.1/corrected_ratios.svg", width: 78%, caption: [
  #tag("EMPIRICAL", detail: "5 ≤ p ≤ 2^17") Observed/predicted ratios for the
  two certified quotient cases and the deliberately invalid pooled
  full-$"GL"_2$ control, which diverges to $4.05$. Data:
  `measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv`.
]) <fig:corrected>

== Constants: predicted vs. measured

#ref(<fig:constants>) collects the three certified constants against their
measured values at $x = 2^17$. All three heuristic intervals contain their
certified predictions; none was tuned. The universal product $C$ is drawn for
reference — the Serre correction lifts it by $10\/9$, the 540.f2 quotient
correction lowers it by $5824\/5913$, and the CM constant lives on a different
Euler product entirely.

#fig("/figures/P5.1/constants.svg", width: 80%, caption: [
  Certified predicted constants (open diamonds) vs. measured constants with
  heuristic 95% intervals (filled, at $x = 2^17$), against the universal
  product $C = 0.505166 dots$ (dashed). Data: the two CSVs of
  #ref(<tab:density>) and #ref(<tab:corrected>).
]) <fig:constants>

== Exact reproduction of Zywina's CM table through $x = 10^9$

Zywina's strongest published numerical evidence is his Table 3: counts of split
primes $p <= x$ with $N_p \/ 8$ prime for $y^2 = x^3 - x$, at fifty checkpoints
$x = 2 dot 10^7, 4 dot 10^7, dots, 10^9$, against the integral predictor of his
equation (7.1),
$
  "Pred"(x) = frac(C_(E_(QQ(i)), 8), 2)
  integral_9^x frac(d t, log t dot (log(t + 1) - log 8)),
$
the factor $1\/2$ being the density of the split stratum. Session 3
re-implemented the entire computation from scratch — segmented sieve,
Cornacchia representations, Walsh traces, Hasse-bounded quotient-primality
sieve, and mpmath quadrature — and ran all fifty checkpoints.

#tag("EMPIRICAL", detail: "all 50 checkpoints, 2·10^7 ≤ x ≤ 10^9") *Every
computed actual count equals Zywina's published value, and every computed
integral rounds to his published expected value: both mismatch totals are
zero.* The complete run processed 25,423,491 split primes in 148.7 seconds
(Python 3.13.4, Windows 11). #ref(<tab:cm>) shows seven of the fifty rows;
#ref(<fig:cm>) shows all fifty.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    align: (right, right, right, right, center, center, center),
    table.hline(stroke: 0.7pt),
    table.header(
      [*$x$*], [*Split $p$*], [*Events*], [*Integral pred.*],
      [*Rounded*], [*Obs./pred.*], [*$Delta$ vs. published*],
    ),
    table.hline(stroke: 0.5pt),
    [$2 dot 10^7$], [635,170], [49,847], [50,062.774], [50,063], [0.99569], [0 / 0],
    [$10^8$], [2,880,504], [202,316], [202,534.443], [202,534], [0.99892], [0 / 0],
    [$2 dot 10^8$], [5,538,820], [372,142], [372,237.484], [372,237], [0.99974], [0 / 0],
    [$4 dot 10^8$], [10,667,607], [686,710], [686,545.808], [686,546], [1.00024], [0 / 0],
    [$6 dot 10^8$], [15,661,930], [983,415], [983,645.382], [983,645], [0.99977], [0 / 0],
    [$8 dot 10^8$], [20,572,460], [1,270,215], [1,270,341.147], [1,270,341], [0.99990], [0 / 0],
    [$10^9$], [25,423,491], [1,548,766], [1,549,656.621], [1,549,657], [0.99943], [0 / 0],
    table.hline(stroke: 0.7pt),
  ),
  caption: [#tag("EMPIRICAL", detail: "7 of 50 checkpoints shown") Exact CM
  reproduction. $Delta$ columns: difference from Zywina's published actual
  count / published rounded expected count — zero at every one of the fifty
  checkpoints. Data:
  `reproduce_cm_table_x1000000000_s51012026_20260720.csv`.],
) <tab:cm>

#fig("/figures/P5.1/cm_table.svg", width: 94%, caption: [
  #tag("EMPIRICAL", detail: "50 checkpoints through 10^9") Left: exact
  prime-quotient counts (points) against the equation-(7.1) integral predictor
  (line). Right: the observed/predicted ratio, confined to
  $[0.99569, 1.00024]$ across the entire range. Data:
  `reproduce_cm_table_x1000000000_s51012026_20260720.csv`.
]) <fig:cm>

#tag("EMPIRICAL", detail: "x = 10^9") At the final checkpoint the ratio is
$0.9994253$ (integral predictor) and $0.9994797$ (direct split-prime-sum
predictor). The agreement of an independent implementation with all one hundred
published numbers — fifty counts and fifty rounded integrals — is strong
evidence that both Zywina's computation and ours are correct, and it promotes
the toy-scale CM measurement of §5.2 to the full published range.

= Where GRH enters the strongest partial results

The strongest fixed-curve theorems toward Koblitz's conjecture are the
almost-prime results of David and Wu @davidwu2012, and it matters for P5.1
exactly *where* their conditionality lives. The following chain is cited from
their paper; nothing in it is original here.

#tag("CITED") *Hypothesis.* David–Wu assume a $theta$-zero-free hypothesis: the
Dedekind zeta functions and relevant Artin $L$-functions of the division fields
$QQ(E[d])$ have no zeros with real part exceeding $theta$; GRH is the case
$theta = 1\/2$ (their Hypothesis 3.4).

#tag("CITED") *Where it is consumed.* The hypothesis powers effective
Chebotarev estimates (their Theorem 3.9) for the primes whose Frobenius forces
$d divides N_p$ for squarefree $d$ — precisely the divisibility data a sieve
needs. These estimates supply the uniform remainder bound for the weighted and
Selberg sieves through their equations (4.11)–(4.14), giving a usable level of
distribution
$
  D = x^((2\/5)(1 - theta)(1 - epsilon)).
$

#tag("CITED") *What comes out.* The weighted sieve yields $N_p = P_r$ (at most
$r$ prime factors) for $gt.tilde x \/ (log x)^2$ primes, with
$
  r = floor(frac(18 + 2 theta, 5 (1 - theta))) + 1,
$
so GRH gives $P_8$, and any $theta < 11\/21$ still gives the same $P_8$
corollary. The companion Selberg-sieve upper bound for *prime* orders carries
the factor $5\/(1 - theta) + epsilon$, i.e. $10 + epsilon$ times the conjectured
count under GRH (their Theorems 1.1, 1.3 and Corollary 1.2). Unconditionally,
the best fixed-curve upper bound recorded by Zywina is weaker by a logarithm,
of order $x \/ (log x log log x)$ @zywina2011.

#tag("CITED") *What does not come out.* No prime-order *lower* bound follows at
any $theta$ — the method stops at almost-primes. So GRH can already be relaxed
to an explicit zero-free region for these partial results, but making them
unconditional requires replacing the division-field Chebotarev input at a
positive level of distribution, and even the conditional sieve cannot cross
from $P_8$ to primes. That crossing is the parity problem, and §4 shows it in
its sharpest form for the CM curve: the event *is* a prime pair.

= Theory closure: the 2025–2026 boundary and the irreducible gap

Session 5 audited the primary literature through 2026-07-20 for any
unconditional fixed-curve prime-order asymptotic.
#tag("EMPIRICAL", detail: "primary-source audit through 2026-07-20") Searches
by title, conjecture name, prime-order terminology, and citation chains found
none. The closest results triangulate the gap:

- #tag("CITED") Dey, Saha, Sivaraman, and Vatwani determine the refined
  fixed-curve constant only after assuming *both* an elliptic analogue of the
  Elliott–Halberstam conjecture *and* a separate conjecture on the average
  growth of $N_p$ @dey2025.
- #tag("CITED") Lee, Mayle, and Wang state explicitly that Zywina's refined
  conjecture remains open; their unconditional theorems concern moments of
  Koblitz constants over curve families and congruence classes, not any fixed
  curve @lmw2025.
- #tag("CITED") Xie's unconditional CM advance proves bounded-almost-prime
  statements for quotients over prime-power fields $FF_(p^ell)$; it does not
  prove primality of $N_p \/ 8$ over $FF_p$ @xie2025.

#proposition(name: [two independent missing ingredients])[
  #tag("PROVED") An unconditional proof of the fixed-curve asymptotic still
  requires two logically separate inputs: (i) sufficiently uniform distribution
  of the divisibility conditions $d divides N_p$ over the required moduli —
  the role played by effective Chebotarev in @davidwu2012 and by elliptic
  Elliott–Halberstam in @dey2025 — and (ii) an input that converts divisibility
  data into an asymptotic for *prime* values rather than almost-prime values —
  absent from @davidwu2012 at any $theta$ and supplied in @dey2025 only by
  assumption.
]

#proof[
  (Sketch; the full argument is the closure classification in
  `THEORY_CLOSURE.md`.) For (i): both cited routes to the constant consume a
  uniform remainder bound at level $x^delta$, $delta > 0$; without one, no
  current sieve produces even the almost-prime lower bound. For (ii): David–Wu
  supply (i) at GRH strength yet obtain only $P_8$ and a prime-order *upper*
  bound, so (i) alone provably does not yield prime values by these methods;
  and Dey et al., who assume a stronger form of (i), still must add a separate
  prime-value hypothesis. Hence neither ingredient implies the other within
  the audited methods.
]

This is recorded as the open question Q026: *what input can break the
prime-order sieve parity barrier for a fixed curve?*
#tag("CONJECTURE") The only route consistent with the audit is an
unconditional theorem supplying both roles with errors summable over the sieve
moduli; this route is refuted if such estimates are proved and the predicted
asymptotic still fails — and a sustained departure of the measured ratios of
§5 from 1 at larger ranges would falsify the implemented constants or counter
independently of Q026. For the CM curve, the norm-pair reduction of §4 pins the
missing statement to a completely explicit object: a simultaneous prime-value
asymptotic for $N(a + b i)$ and $N(a + b i + 1)\/8$ over $p ≡ 5 (mod 8)$ —
a Gaussian analogue of a Hardy–Littlewood prime-pair problem. Nothing about
the trace formula, the local densities, or the finite computations is any
longer in the way.

= Adversarial verification

Because every headline number above is produced by our own code, Session 4 ran
an adversarial self-check aimed at the failure modes that would be invisible to
agreement with published values: circular validation, shared bugs between
"independent" paths, and fixture leakage. #ref(<tab:audit>) summarizes.

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Check*], [*Scope*], [*Outcome*]),
    table.hline(stroke: 0.5pt),
    [CM trace vs. generic BSGS], [12 split + 3 inert primes, $10^4$–$9 dot 10^8$],
      [all orders equal],
    [Sieve triple agreement], [split primes $p <= 5 dot 10^6$],
      [identical 174,193-element sequences],
    [Primality triple agreement], [500 quotient samples $< 10^9$],
      [zero mismatches (Eratosthenes / Miller–Rabin / SymPy)],
    [Quadrature cross-check], [$x in {2 dot 10^7, 4 dot 10^8, 10^9}$],
      [SciPy vs. mpmath differ $<= 1.2 dot 10^(-9)$],
    [Euler products at 60 digits], [$ell <= 10^6$],
      [differ from float by $9.0 dot 10^(-15)$ / $2.4 dot 10^(-13)$],
    [540.f2 CRT recount], [exact enumeration],
      [reproduces 98,280 / 699,840, $91\/648$, $5824\/5913$],
    [Anti-circularity], [AST inspection + fixture mutation],
      [counting path never reads the published table],
    table.hline(stroke: 0.7pt),
  ),
  caption: [#tag("EMPIRICAL", detail: "Session 4 audit") Independent
  verification paths. Full details and artifact hashes:
  `audits/SELF-CHECK-20260722.md`.],
) <tab:audit>

Two audit results deserve emphasis. #tag("PROVED") *Anti-circularity:* static
AST inspection shows the counting function never references the published
table fixture, and deliberately corrupting the $x = 10^4$ fixture to 999,999
leaves the computed count unchanged at 105, altering only the comparison
column — the reproduction of §5.4 cannot have copied its answers. The one
defect found anywhere was an off-by-one in a *disposable audit harness*
sieve, fixed without touching production code or data; the final suite stands
at 85 passing tests.

= Limitations and open questions

We list the limitations exactly as the research notes record them.

- #tag("EMPIRICAL", detail: "p ≤ 2^17") The non-CM sweeps stop at $2^17$ —
  far below Zywina's published range. They are convergence demonstrations and
  certificate tests, not new numerical territory; only the CM computation
  reaches $10^9$.
- #tag("HEURISTIC") All quoted intervals are Poisson-style approximations;
  dependence across reductions or finite-cutoff bias can invalidate them.
- #tag("CONDITIONAL", detail: "LMFDB 540.f2 adelic data") The $C_(E,3)$
  certificate consumes LMFDB's level-30 generators as input; the finite
  computation on them is exact and independently recounted, but the generators
  were not re-derived from division polynomials.
- #tag("PROVED") The constant registry is exactly that — a registry of
  certified cases (Serre $10\/9$, rational-torsion zero, 540.f2 quotient, CM
  $t = 8$) — not a general adelic-image calculator; no constant is guessed for
  arbitrary curves. The $t = 2$ quotient diagnostic for 112.b4 (1 prime
  quotient value recorded) has *no* certified constant, so no comparison is
  claimed.
- #tag("PROVED") A larger finite cutoff cannot by itself convert any of this
  evidence into the asymptotic; and the two ingredients of Proposition 8 are
  genuinely independent, so progress on distribution alone (e.g. removing GRH
  from Chebotarev inputs) cannot close Q026.

The open questions are correspondingly sharp: Q026 itself — an unconditional
fixed-curve theorem supplying uniform divisibility distribution *and* a
parity-breaking prime-value input — and its CM specialization, a simultaneous
prime-value asymptotic for $N(a+b i)$ and $N(a+b i+1)\/8$ on $p ≡ 5 (mod 8)$.

= Conclusion

P5.1 set out to test Koblitz's conjecture with certified constants, exact
counts, independent implementations, and no fitting anywhere. The results: an
exact reproduction of all fifty published CM checkpoints, a new certified
constant ($C_(E,3) = (5824\/5913) C$ for 540.f2, conditional only on LMFDB's
adelic data), three corrected predictors landing within a few percent of measured
counts while a deliberately wrong model fails by a factor of four, and one
theorem — the norm-pair reduction — compressing the remaining difficulty of
the CM case into one explicit prime-pair statement with one exceptional
prime, $p = 17$. P5.1 cannot prove the asymptotic: §7 shows the 2025 state of
the art still needs two unproved inputs, and §6 shows GRH-strength
distribution alone stops at almost-primes.
The conjecture is exactly as open as it was — but for $y^2 = x^3 - x$, it is
now open in its cleanest form.

#v(0.4em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.1em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
All data, scripts, and audits live in the P5.1 problem directory. The
producers are `code/measure_density.py` (three-curve sweep, 11.2 s at
$x = 2^17$), `code/measure_corrected_cases.py` (quotient certificates, 9.0 s),
and `code/reproduce_cm_table.py` (Cornacchia–Walsh segmented sieve, 148.7 s
through $x = 10^9$),
all run with seed 51012026 on Python 3.13.4 / Windows 11 with SageMath and
PARI/GP unavailable; the full suite passes 85 tests. Figure CSVs are named in
each caption; SHA-256 hashes of the canonical artifacts are recorded in
`audits/SELF-CHECK-20260722.md`. Every
mathematical claim above carries one of the epistemic tags #tag("PROVED"),
#tag("CITED"), #tag("CONDITIONAL", detail: "assumption"),
#tag("EMPIRICAL", detail: "range"), #tag("HEURISTIC"), or #tag("CONJECTURE") — untagged sentences are exposition,
not claims.
]

#show bibliography: set text(size: 9.3pt)
#bibliography("refs/P5.1.bib", title: [References], style: "ieee")
