#import "lib/paper.typ": *

#show: paper.with(
  title: "The Automorphism Ceiling: What Small CM Discriminant Buys, and Cannot Buy, Against the ECDLP",
  subtitle: "A √6 unit-orbit speedup ceiling, its constant-factor empirical confirmation, and coefficient-tracking obstructions for non-unit CM endomorphisms",
  pid: "P5.2",
  keywords: ("ECDLP", "complex multiplication", "efficient endomorphisms", "Pollard rho", "automorphism classes", "GLV"),
  abstract: [
    An ordinary elliptic curve $E \/ FF_p$ with complex multiplication by an order
    of small discriminant $D$ carries an explicit, efficiently computable
    endomorphism. The security question P5.2 asks whether small $abs(D)$ yields a
    reduction of the discrete logarithm problem (ECDLP) to the general case, or a
    subexponential algorithm exploiting $D$. We answer in the negative for the two
    routes the extra structure actually opens, and we make the boundary between
    them precise. First, the *unit* endomorphisms that exist only for $D = -3$ and
    $D = -4$ act as roots of unity on a prime-order subgroup and induce a
    fixed-order quotient of the Pollard-$rho$ state space; we prove that in the
    ideal-random-mapping cost model the resulting speedup tends to $sqrt(m)$ for a
    unit action of order $m$, that imaginary-quadratic units have order at most
    six, and hence that unit-orbit $rho$ has a hard *constant* ceiling of
    $sqrt(6)$ — no asymptotic gain is possible. A preregistered experiment over
    $3{,}200$ recovered logarithms confirms the ceiling: every $95%$ bootstrap
    interval for the measured speedup contains $sqrt(6)$ (for $D=-3$) or $2$ (for
    $D=-4$), and a log–log fit finds no growing advantage. Second, a general
    *non-unit* efficient endomorphism (we use the GLV discriminant-$-7$ map) acts
    with a scalar eigenvalue whose multiplicative order $m$ *does* grow — we
    measure orders from $116$ to $16{,}415$ — so its orbit quotient is large; but
    we prove this cannot be cashed in. Least-representative canonicalization of a
    length-$m$ orbit needs $m-1$ successor evaluations in a sequential evaluator
    model, addition does not descend to scalar-orbit classes, a coefficient-tracking
    walk must retain the orientation multiplier, and any canonicalizer that returns
    that multiplier is *itself* an ECDLP algorithm using $q+1$ calls for
    $q = (r-1) \/ m$ orbits. The results are proved or empirically validated at toy
    scale ($log_2 p <= 18$); we state honestly what remains open — whether several
    unoriented orbit-membership constraints can be combined in sub-$sqrt(r)$ time
    (logged as Q025) was not settled, and the project was closed before that
    experiment ran.
  ],
)

= Introduction

The hardness of the elliptic-curve discrete logarithm problem (ECDLP) is the
foundation of curve-based public-key cryptography. For a well-chosen ordinary
curve $E \/ FF_p$ of prime order the best known attack is a generic
collision search — Pollard $rho$ @pollard1978 — costing
$Theta(sqrt(r))$ group operations in a subgroup of order $r$, matching the
generic lower bound. Curve-selection guidelines therefore ask whether any
*published* structural feature of a curve erodes that square-root barrier. One
recurring worry is *complex multiplication (CM) of small discriminant*: curves
built by the CM method @atkinmorain1993 come with an explicit endomorphism
$phi.alt$ of small norm that can be evaluated about as cheaply as a point
doubling, and this endomorphism is exactly what the GLV method
@glv2001 uses to *speed up* honest scalar multiplication. If the same map
accelerates the attacker, small $abs(D)$ would be a weakness.

The problem P5.2 poses the question sharply: for ordinary $E \/ FF_p$ with CM by
an order of discriminant $D$ with $abs(D)$ small, either prove a polynomial-time
reduction from small-$abs(D)$ ECDLP to general ECDLP, or give a subexponential
ECDLP algorithm exploiting $abs(D)$. We do neither, because — we argue — neither
exists along the two routes the CM structure genuinely opens. Instead we
characterize precisely what the structure buys.

There are two qualitatively different endomorphisms to worry about, and the
literature on automorphism-class $rho$ @wienerzuccherato1998 @dgm1999 conflates
them at one's peril. The *units* of the endomorphism ring — the roots of unity
in the CM order — are automorphisms fixing the identity; they exist beyond
$plus.minus 1$ only for the two special curves $j = 0$ ($D = -3$) and $j = 1728$
($D = -4$), and they act on a prime-order subgroup as roots of unity of order
$4$ or $6$. A *non-unit* efficient endomorphism (such as GLV's norm-$2$ map for
$D = -7$) is not an automorphism: it acts as multiplication by an eigenvalue
$lambda in FF_r^times$ whose order is typically large. The first kind gives a
genuinely bounded speedup; the second gives a large orbit but, we show, no usable
speedup. Our headline is that the CM discriminant is not a security problem, and
the reason is different in the two cases.

#keybox(title: "Main result (informal)")[
  Small CM discriminant does *not* reduce ECDLP to an easier problem and does
  *not* yield a subexponential algorithm. It buys exactly one thing: a
  Pollard-$rho$ collision search on a fixed-order *unit* quotient, whose idealized
  speedup tends to $sqrt(m)$ for a unit action of order $m$. Because an
  imaginary-quadratic order has units of order at most six, this speedup has a
  hard *constant* ceiling of $sqrt(6)$ (attained only at $D = -3$; $D = -4$ gives
  $2$; every other $D$ gives at most $sqrt(2)$ from negation). The general
  *non-unit* endomorphism has a growing orbit, but exploiting it requires a
  canonicalizer whose orientation multiplier already solves ECDLP — so it is an
  attack primitive, not a free optimization.
]

== Contributions and honest scope

We contribute: (i) explicit, independently validated unit endomorphisms for the
$D = -3, -4$ toy families and their characteristic equations (§3); (ii) a
generic-group *ceiling theorem* for finite unit actions, including the
imaginary-quadratic "order at most six" bound and its $sqrt(6)$ consequence (§4); (iii)
a preregistered empirical confirmation that the collision-table quotient walk hits
the constant ceiling with no detectable asymptotic drift, over $3{,}200$ recovered
logarithms (§5, #ref(<fig:ceiling>)); (iv) the cautionary finding that cycle
handling and the memory model are part of the algorithmic claim — a naive Floyd
walk and a doubling escape both *lose* the gain (§6, #ref(<fig:variants>)); (v) an
explicit non-unit $D = -7$ construction with measured eigenvalue orders growing to
$16{,}415$, and a proof that its orbit cannot be cashed in as a walk speedup (§7–§8,
#ref(<fig:nonunit>)); and (vi) an honest limitations section (§9).

We state the scope plainly, as the repository's ground rules demand. All positive
statements are either proved in an explicitly named model or measured at toy
parameters ($log_2 p <= 18$); no claim of asymptotic security or insecurity is
made. One question — whether several *unoriented* orbit-collision constraints can
be combined in sub-$sqrt(r)$ time when the quotient index is two or three — was
formulated but not experimentally tested before the project was closed; we record
it as open (Q025) rather than resolve it by assertion.

= Setting and notation

Fix a prime $p > 3$ and a nonsingular short-Weierstrass curve
$
  E : y^2 = x^3 + a x + b, quad a, b in FF_p, quad 4 a^3 + 27 b^2 eq.not 0 .
$
Write $hash E(FF_p)$ for its order and $O$ for the point at infinity. An ECDLP
instance is $(P, Q, r)$ with $P, Q in E(FF_p)$, $r$ a prime divisor of
$hash E(FF_p)$, $⟨ P ⟩$ the order-$r$ subgroup, and $Q = [s] P$ for
an unknown $s in ZZ \/ r ZZ$; the task is to output $s$. We reserve $G = ⟨ P ⟩$
for this subgroup.

#tag("CITED") By Waterhouse's theorem @waterhouse1969, for an ordinary curve over
a finite field the geometric endomorphism ring $sans("End")(E)$ is an order
$cal(O)$ in the imaginary quadratic field $K = QQ(sqrt(-D))$, where $-D$ is the
discriminant of the Frobenius. The Frobenius $pi$ satisfies
$pi^2 - t pi + p = 0$ with trace $t = p + 1 - hash E(FF_p)$, and $t eq.not 0$ is
the ordinary condition. An element $phi.alt in cal(O)$ that is *efficiently
computable* — a low-degree rational map on coordinates — acts on the invariant
cyclic subgroup $G$ as multiplication by a scalar $lambda in FF_r^times$, and this
$lambda$ is a root modulo $r$ of the characteristic polynomial of $phi.alt$
@glv2001. We call $phi.alt$ a *unit* when it is invertible in $cal(O)$ (a root of
unity of $K$) and *non-unit* otherwise.

Throughout, an *orbit walk* is a Pollard-$rho$ iteration performed on the
quotient of $G without {O}$ by a finite group of efficiently computable maps,
storing a canonical representative of each orbit together with the linear
coefficients $(a, b)$ of the tracked state $X = [a] P + [b] Q$. A *baseline walk*
is the same iteration with no quotient. We compare their online transition counts.

= Explicit unit endomorphisms for $D = -3$ and $D = -4$

The only ordinary CM curves with an automorphism beyond $[plus.minus 1]$ are the
two special $j$-invariants, and their automorphisms are written down explicitly.

#proposition(name: [the $j = 0$ unit, $D = -3$])[
  #tag("PROVED") Let $E : y^2 = x^3 + b$ over $FF_p$ with $p equiv 1 mod 3$, and
  let $zeta in FF_p$ be a primitive cube root of unity. The map
  $psi(x, y) = (zeta x, -y)$ fixes $O$, sends $E$ to $E$, has order six, and
  satisfies $psi^2 - psi + [1] = 0$ as an endomorphism.
]

#proof[
  Substituting $(zeta x, -y)$ into $y^2 = x^3 + b$ uses $zeta^3 = 1$, so the image
  lies on $E$. Iterating the coordinate action, $psi^2(x,y) = (zeta^2 x, y)$ and
  $psi^3(x, y) = (x, -y) = [-1](x,y)$, so $psi$ has order six and
  $psi^3 = [-1]$. Writing $phi.alt = -psi$ gives $phi.alt^3 = [1]$ with
  $phi.alt eq.not [1]$, so $phi.alt$ is a primitive cube root of unity and obeys
  $phi.alt^2 + phi.alt + [1] = 0$; substituting $phi.alt = -psi$ yields
  $psi^2 - psi + [1] = 0$.
]

#proposition(name: [the $j = 1728$ unit, $D = -4$])[
  #tag("PROVED") Let $E : y^2 = x^3 + a x$ over $FF_p$ with $p equiv 1 mod 4$, and
  let $iota in FF_p$ satisfy $iota^2 = -1$. The map $psi(x, y) = (-x, iota y)$
  fixes $O$, sends $E$ to $E$, has order four, and satisfies $psi^2 + [1] = 0$.
]

#proof[
  Substituting $(-x, iota y)$ into $y^2 = x^3 + a x$ uses $iota^2 = -1$ and
  $(-x)^3 = -x^3$, so the image lies on $E$. Two applications give
  $psi^2(x, y) = (x, -y) = [-1](x, y)$, hence $psi^2 + [1] = 0$ and $psi$ has
  order four.
]

On the prime-order subgroup $G$, $psi$ acts as a scalar $mu in FF_r^times$ that
is a root of the same quadratic modulo $r$; for $D = -3$ this scalar has exact
order $6$, and for $D = -4$ exact order $4$. These are the *unit orders*
$m in {4, 6}$ that drive the ceiling below.

#tag("EMPIRICAL", detail: "8 curves, p = 4057..261673, 32 seeded checks each") We
constructed one $D = -3$ and one $D = -4$ curve over each of four prime fields,
computed the full order by exhaustive enumeration *and* an independent
Hasse-interval/BSGS counter (the two always agreed), verified that the subgroup
order annihilates the generator, and checked the characteristic equation, the
scalar eigenvalue, and the unit exponent on $32$ seeded points per curve. The
constructions are in #ref(<tab:cm>).

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    align: (right, right, center, center, right, right, center),
    table.hline(stroke: 0.7pt),
    table.header(
      [*bits*], [$p$], [$D$], [$(a, b)$], [$hash E(FF_p)$], [prime $r$], [unit ord],
    ),
    table.hline(stroke: 0.5pt),
    [12], [4057], [$-3$], [$(0, 5)$], [4153], [4153], [6],
    [12], [4057], [$-4$], [$(5, 0)$], [4106], [2053], [4],
    [14], [16381], [$-3$], [$(0, 11)$], [16633], [16633], [6],
    [14], [16381], [$-4$], [$(2, 0)$], [16202], [8101], [4],
    [16], [65437], [$-3$], [$(0, 2)$], [65068], [16267], [6],
    [16], [65437], [$-4$], [$(3, 0)$], [65896], [8237], [4],
    [18], [261673], [$-3$], [$(0, 10)$], [262519], [262519], [6],
    [18], [261673], [$-4$], [$(5, 0)$], [261538], [130769], [4],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Validated CM constructions (SG-01a). Every full order was confirmed by
  exhaustive counting and an independent BSGS counter; every explicit unit map
  passed $32$ seeded characteristic-equation, eigenvalue, and unit-exponent checks.
  Data: `measure_unit_rho_table_..._validation.csv`.],
) <tab:cm>

= The unit-orbit ceiling

We now prove that a finite unit action buys a *bounded* Pollard-$rho$ speedup and
identify the bound.

#lemma(name: [free action and orbit count])[
  #tag("PROVED") Let $G = ⟨ P ⟩$ have prime order $r$, and suppose a
  cyclic endomorphism acts on $G$ as scalar multiplication by $mu in FF_r^times$
  of exact order $m$. Then the induced action of $⟨ mu ⟩$ on
  $G without {O}$ is free, and the quotient has exactly $1 + (r-1) \/ m$ orbits.
]

#proof[
  If $mu^j s = s$ for $s eq.not 0$ in $FF_r$, then $mu^j = 1$, so $m divides j$;
  the stabilizer of every nonzero point is trivial and the action is free. By
  orbit–stabilizer each nonzero orbit has size $m$, and $r - 1$ is divisible by
  $m$ (since $mu in FF_r^times$ has order $m$), giving $(r-1) \/ m$ nonzero orbits
  plus the singleton orbit ${O}$.
]

#proposition(name: [ideal quotient speedup])[
  #tag("HEURISTIC") Model a well-mixed $rho$ walk as an ideal random mapping. On a
  set of size $N$ the expected number of steps to the first repeat is
  asymptotic to $sqrt(pi N \/ 2)$ @harris1960 @wangzhang2011. Quotienting the
  order-$r$ subgroup by a unit action of order $m$ replaces $N = r$ by
  $N = 1 + (r-1) \/ m$, so the ratio of baseline to quotient first-repeat work
  tends to $sqrt(m)$; for fixed $m$ the quotient changes only the multiplicative
  constant, not the $sqrt(r)$ growth.
]

The key structural fact is that $m$ cannot grow for a *unit*.

#theorem(name: [imaginary-quadratic unit ceiling])[
  #tag("PROVED") A unit of an order in an imaginary quadratic field has
  multiplicative order at most six. Consequently unit-orbit $rho$ on an ordinary
  CM curve has an idealized speedup ceiling of $sqrt(6)$, attained only by the
  $D = -3$ unit group; $D = -4$ gives at most $2$, and every other imaginary
  quadratic order gives at most $sqrt(2)$, coming from negation alone.
]

#proof[
  A root of unity of order $n$ generates $QQ(zeta_n)$, of degree $phi.alt(n)$ over
  $QQ$. A unit lying in an imaginary quadratic field forces
  $phi.alt(n) <= 2$, hence $n in {1, 2, 3, 4, 6}$. The maximal $n$ compatible with
  a nontrivial CM order is $n = 6$ (at $D = -3$) and $n = 4$ (at $D = -4$); for
  every other discriminant the only units are $plus.minus 1$, of order $2$.
  Substituting the maximal $m in {6, 4, 2}$ into the $sqrt(m)$ idealized speedup
  gives the stated ceilings.
]

#remark(name: "what the ceiling does and does not say")[
  #tag("PROVED") This is a ceiling for *finite unit actions* in an
  ideal-random-mapping cost model. It proves that no choice of small $abs(D)$
  yields more than a fixed constant-factor collision speedup through units, and in
  particular that no unit action produces an *asymptotic* improvement over
  $sqrt(r)$. It is *not* a proof that small CM discriminant cannot aid *any*
  algorithm; the non-unit endomorphisms of §7 have unbounded orbit order and are
  handled separately.
]

The ceiling reframes the security question. For the two special curves, the worst
an attacker gains from the published automorphism is a factor of at most $sqrt(6)$
— the same order of magnitude as the negation-map speedup available on *every*
curve — and this is a constant, not a break. Whether even that constant is
*realizable* is a separate, implementation-level question we address empirically.

= Empirical confirmation of the ceiling

We preregistered two refutable predictions before running anything: (P1) the
collision-table quotient walk reduces mean transitions by factors whose $95%$
bootstrap intervals contain $sqrt(6)$ (for $D = -3$) and $2$ (for $D = -4$) at
each of four subgroup sizes; (P2) no speedup grows with subgroup order once the
orbit size is fixed, tested by a log–log fit whose slope interval must exclude a
positive value. Both were confirmed.

#tag("EMPIRICAL", detail: "3,200 recovered DLPs, r = 2053..262519, seed 52022026")
Using a collision-table variant that detects exact-state recurrence directly (see
§6 for why this matters), with an identical $20$-adding transition design in both
arms and $200$ paired trials per case, we recovered every logarithm and measured
the ratio of mean online transitions in #ref(<tab:speedup>). Every $95%$
paired-bootstrap interval contains the predicted orbit factor.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto),
    align: (right, center, right, right, right, right, center),
    table.hline(stroke: 0.7pt),
    table.header(
      [*bits*], [$D$], [$r$], [base], [quot], [speedup (95% CI)], [target],
    ),
    table.hline(stroke: 0.5pt),
    [12], [$-3$], [4153], [83.04], [33.11], [2.508 (2.267, 2.758)], [$sqrt(6)$],
    [14], [$-3$], [16633], [161.86], [65.70], [2.464 (2.221, 2.716)], [$sqrt(6)$],
    [16], [$-3$], [16267], [167.85], [63.02], [2.664 (2.413, 2.961)], [$sqrt(6)$],
    [18], [$-3$], [262519], [657.51], [271.30], [2.424 (2.197, 2.670)], [$sqrt(6)$],
    table.hline(stroke: 0.3pt),
    [12], [$-4$], [2053], [58.81], [27.19], [2.163 (1.936, 2.408)], [$2$],
    [14], [$-4$], [8101], [115.77], [57.85], [2.001 (1.800, 2.220)], [$2$],
    [16], [$-4$], [8237], [122.63], [56.10], [2.186 (1.976, 2.423)], [$2$],
    [18], [$-4$], [130769], [450.38], [243.07], [1.853 (1.671, 2.043)], [$2$],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Collision-table unit-orbit speedup (SG-03a/SG-04a). "base"/"quot" are
  mean online transitions; the target column is the ideal ceiling
  $sqrt(6) approx 2.449$ or $2$. All eight intervals contain their target. Data:
  `measure_unit_rho_table_..._summary.csv`.],
) <tab:speedup>

The measured values sit at or just below the ceiling and show no upward drift with
$r$. #ref(<fig:ceiling>) plots them against the two theoretical lines.

#fig("/figures/P5.2/ceiling.svg", width: 78%, caption: [
  #tag("EMPIRICAL", detail: "200 trials per case") Measured mean-transition speedup
  (points, $95%$ bootstrap error bars) against the $sqrt(6)$ and $2$ ceilings
  (dashed). The $D = -3$ series tracks $sqrt(6) approx 2.449$ and the $D = -4$
  series tracks $2$ across all four field sizes, with every interval covering its
  target.
]) <fig:ceiling>

#tag("EMPIRICAL", detail: "four sizes, 200 trials each") The log–log fit of
$log("speedup")$ against $log r$ has slope $-0.0109$ with $95%$ bootstrap interval
$[-0.0420, 0.0209]$ for $D = -3$, and $-0.0385$ with interval
$[-0.0731, -0.0027]$ for $D = -4$. Neither interval lies above zero, so prediction
P2 holds: no growing advantage is detected over the tested range. (The $D = -4$
interval is marginally negative — the constant is being *approached from above* as
$r$ grows, consistent with a fixed asymptotic factor of $2$, not with a decay to
$1$.) This is exactly the signature the ceiling theorem predicts: a constant, not
a slope.

= Cycle handling is part of the claim

The ceiling is idealized; a real implementation must handle the *fruitless cycles*
that equivalence-class walks are known to produce @bkl2010 @bls2011 @wangzhang2011.
We tried two constant-memory designs and both *destroyed* the gain, which we
record as a first-class finding rather than suppress.

#tag("EMPIRICAL", detail: "naive Floyd, same range") A naive Floyd walk that
canonicalizes each state suffers zero-denominator fruitless cycles that grow with
$r$: at the largest size the mean-work ratio fell to $0.916$ ($D = -3$) and
$0.617$ ($D = -4$) — i.e. the "speedup" became a *slowdown*. Its log–log slope is
strongly negative ($-0.206$ and $-0.255$), the fingerprint of a defect that
worsens with scale, not of the flat constant the theory predicts.

#tag("EMPIRICAL", detail: "history-local doubling escape, A002, same range") A
doubling escape that, on detecting a fruitless collision, doubles and
re-canonicalizes the offending point rather than restarting, was worse still: it
reached mean transition counts of $36{,}878$ ($D = -3$) and $32{,}470$ ($D = -4$)
at the largest size, with means of $172$ and $211$ escape doublings per recovery
and individual trials exceeding $1{,}500$ escapes. This attempt is *dead*.

#remark(name: "why the escape recurs")[
  #tag("PROVED") Doubling is a permutation of the odd prime-order subgroup, so it
  does not by itself move the escaped state out of a fruitless component; the rule
  was history-local rather than a globally specified iteration with a canonical
  escape point, and the data show recurrence dominating. The transferable lesson
  is that zero-denominator collisions must be *counted*, and any orbit-speedup
  claim must state its cycle-handling and memory model. The collision-table variant
  used in §5 sidesteps this by detecting exact-state recurrence directly — at the
  cost of $O(sqrt(r))$ memory, so it isolates the orbit-space factor rather than
  claiming a constant-memory implementation.
]

#fig("/figures/P5.2/variants.svg", width: 92%, caption: [
  #tag("EMPIRICAL", detail: "three walk variants, 200 trials per case") Speedup
  ratio (log scale) for the collision-table walk (which tracks the ideal dotted
  line), the naive Floyd walk (which decays below $1$ at the largest size), and the
  doubling escape (which collapses by an order of magnitude). The thin solid line
  marks ratio $1$ (no gain). Realizing even the constant ceiling requires correct
  cycle handling. Data: the three `..._summary.csv` files.
]) <fig:variants>

Literature negation-map algorithms using block minima, distinguished points, or
branchless formulations make the overhead small for the order-two negation map
@bkl2010 @bls2011 @wangzhang2011; extending those exact constructions to the
order-four and order-six unit actions was not attempted here and is a natural
follow-up. But the constant they chase is still bounded by $sqrt(6)$.

= Beyond units: the non-unit $D = -7$ endomorphism

The ceiling theorem covers units. A *non-unit* efficient endomorphism has an
eigenvalue $lambda$ whose order need not be bounded, so its orbit quotient can be
large — superficially a bigger prize. We instantiate the smallest textbook example
and measure it.

#tag("CITED") GLV Example 5 @glv2001 gives, for $omega = (1 + sqrt(-7)) \/ 2$ and
$a = (omega - 3) \/ 4$, the degree-two map on $E_3 : y^2 = x^3 - 3 x^2 \/ 4 - 2 x - 1$,
$
  x' = omega^(-2) frac(x^2 - omega, x - a), quad
  y' = omega^(-3) y frac(x^2 - 2 a x + omega, (x - a)^2) .
$

#tag("PROVED") The substitution $x_"old" = x + 1 \/ 4$ carries this to the short
model $y^2 = x^3 - 35 x \/ 16 - 49 \/ 32$, on which we evaluate the rational map
directly (with the exceptional denominator case returning $O$). On every invariant
prime-order subgroup $G$ the action is $phi.alt(P) = [lambda] P$ with
$lambda^2 - lambda + 2 equiv 0 mod r$, because the point relation is
$phi.alt^2 - phi.alt + [2] = 0$.

#tag("EMPIRICAL", detail: "5 curves, p = 977..262007, Python 3.13.4") Each curve
passed independent exhaustive and BSGS point counts and $32$ seeded
characteristic-equation checks. We then recovered the eigenvalue $lambda$ and its
exact multiplicative order $m = "ord"_r (lambda)$; #ref(<tab:nonunit>) shows $m$
growing from $116$ to $16{,}415$ as $r$ grows, with the nonzero orbit quotient
containing only two or three orbits in each case (i.e. $lambda$ nearly generates
$FF_r^times$).

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto),
    align: (right, right, right, right, right, right, right, right),
    table.hline(stroke: 0.7pt),
    table.header(
      [*bits*], [$p$], [$r$], [$lambda$], [$m$], [$(r-1)\/m$], [$m-1$ evals], [$sqrt(m)$],
    ),
    table.hline(stroke: 0.5pt),
    [10], [977], [233], [203], [116], [2], [115], [10.77],
    [12], [4013], [991], [45], [495], [2], [494], [22.25],
    [14], [16249], [4057], [3635], [1352], [3], [1351], [36.77],
    [16], [64661], [16139], [1546], [8069], [2], [8068], [89.83],
    [18], [262007], [32831], [25875], [16415], [2], [16414], [128.12],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Non-unit $D = -7$ orbit structure (SG-07a). The eigenvalue order $m$
  grows with $r$, so the orbit quotient $(r-1) \/ m$ is small (two or three
  orbits); but the exhaustive least-representative canonicalizer uses exactly
  $m - 1$ map evaluations, while the ideal gain is only $sqrt(m)$. Data:
  `measure_nonunit_orbits_..._{summary,validation}.csv`.],
) <tab:nonunit>

Here is the trap. The ideal collision-space gain from an order-$m$ orbit is
$sqrt(m)$, but *choosing* the canonical representative of a length-$m$ orbit by
exhaustive enumeration costs $m - 1$ map evaluations per walk step. The ratio
$(m - 1) \/ sqrt(m)$ grows from $10.68$ to $128.11$ over the measured range: the
per-step canonicalization cost overwhelms the collision gain, and grows with it.
#ref(<fig:nonunit>) shows the two curves diverging.

#fig("/figures/P5.2/nonunit.svg", width: 74%, caption: [
  #tag("EMPIRICAL", detail: "5 curves, exact orders") The exhaustive
  canonicalizer cost $m - 1$ (per walk step) against the ideal orbit gain
  $sqrt(m)$, on a log scale, versus subgroup size. The gap widens monotonically:
  enumerating the orbit to normalize a state costs far more than the collision
  search it accelerates. Labels give the measured eigenvalue order $m$.
]) <fig:nonunit>

= Why the non-unit orbit cannot be cashed in

One might hope a *cleverer* canonicalizer — sub-linear in $m$, or one that avoids
canonicalization altogether — rescues the non-unit route. We prove three
obstructions that, together, close the standard algorithmic avenues.

#theorem(name: [least-representative query lower bound])[
  #tag("PROVED") Fix an opaque cycle $x, T(x), dots, T^(m-1)(x)$ of known length
  $m$. In a model exposing only a successor query $T$ and comparisons of opaque
  labels, every deterministic algorithm that always returns the least label needs
  at least $m - 1$ successor queries in the worst case.
]

#proof[
  After fewer than $m - 1$ queries the algorithm has seen fewer than all $m$
  labels. An adversary can assign an as-yet-unseen label a value below every seen
  label without changing any query answer or comparison already observed, so the
  algorithm's chosen label is not always minimal. Conversely $m - 1$ queries expose
  every element and suffice. Hence the query complexity is exactly $m - 1$, and the
  exhaustive enumerator is optimal in this model.
]

This proves the enumeration cost in #ref(<tab:nonunit>) is not an artifact of a
lazy implementation: in the stated sequential evaluator model no normalizer beats
$m - 1$. But could a normalizer that *does* exploit richer algebra be
cost-free? No — because merely *returning* the orbit transformation already breaks
ECDLP.

#theorem(name: [a multiplier-returning canonicalizer solves ECDLP])[
  #tag("PROVED") Let $G = ⟨ P ⟩$ have prime order $r$, let
  $lambda in FF_r^times$ have order $m$, and put $q = (r - 1) \/ m$. Suppose a
  routine $C(X) = (R, h)$ returns a common orbit representative $R$ and the
  multiplier $h in H = ⟨ lambda ⟩$ with $R = [h] X$. Then ECDLP
  requires at most $q + 1$ calls to $C$, $O(q)$ stored representatives, and
  ordinary scalar arithmetic.
]

#proof[
  Let $g$ be a primitive root modulo $r$; the scalars $g^i$ for $0 <= i < q$
  represent all cosets of $H$. Precompute $C([g^i] P) = (R_i, h_i)$. For
  $Q = [s] P$, compute $C(Q) = (R, h)$ and find the unique $i$ with $R_i = R$.
  Equality of representatives gives $[h_i g^i] P = [h s] P$, hence
  $s = h^(-1) h_i g^i mod r$. No discrete logarithm inside $H$ is needed — only the
  returned multiplier. A batched canonicalizer that returns the multipliers for a
  requested batch achieves the same reduction with one batch of the $q$ transversal
  inputs plus $Q$.
]

#corollary(name: [normalization is an attack, not a free step])[
  #tag("PROVED") If $q = (r-1) \/ m$ and the running time of $C$ are both
  polynomial in $log r$, then $C$ *is* a polynomial-time ECDLP algorithm. In the
  extreme $m = r - 1$ (so $q = 1$), the two calls $C(P)$ and $C(Q)$ already recover
  $s$. A quotient-$rho$ implementation that needs the exponent or an equivalent
  coefficient transformation therefore cannot count its normalizer as cost-free
  when assessing speedup.
]

The measured $D = -7$ cases have $q in {2, 3}$, so this corollary is not
hypothetical: a cheap normalizer for them would be a near-total ECDLP break, which
is precisely why none is expected to be cheap. Finally, we show the orbit class
*without* orientation cannot even carry the walk.

#theorem(name: [addition does not descend to scalar-orbit classes])[
  #tag("PROVED") Let a nontrivial subgroup $H <= FF_r^times$ act by scalar
  multiplication on the additive group $G = ⟨ P ⟩$ of prime order $r$,
  and let $pi : G -> G \/ H$ be the orbit map. There is no binary operation
  $⊕$ on $G \/ H$ with $pi(X + Y) = pi(X) ⊕ pi(Y)$ for all
  $X, Y in G$.
]

#proof[
  Pick $h in H$ with $h eq.not 1$. Then $P$ and $[h] P$ share an orbit, so
  well-definedness with $Y = -P$ would force the orbits of $P - P = O$ and
  $[h] P - P = [h - 1] P$ to coincide. But ${O}$ is a singleton orbit and
  $[h - 1] P eq.not O$ (as $r$ is prime and $h eq.not 1$), a contradiction.
]

#proposition(name: [coefficient-tracking must retain the orientation])[
  #tag("PROVED") In the standard algebraic model, an $r$-adding state carries the
  formal invariant $X = [a] P + [b] Q$ as $a + b z in FF_r [z]$. Canonicalizing
  $X$ to $R = [h] X$ multiplies the coefficient by $h$, forcing the new
  coefficients to be $h(a + u)$ and $h(b + v)$ after adding a table entry
  $(u, v)$. Thus a correct canonicalized transition must retain $h$, or
  information from which $h$ is recovered. Consequently an *unoriented* collision
  between states $(a, b)$ and $(c, d)$ yields only the membership constraint
  $
    frac(a + b s, c + d s) in H = ⟨ lambda ⟩,
  $
  which, lacking the orientation, admits up to $abs(H) = m$ candidate logarithms
  $s = (h c - a) \/ (b - h d)$ (one per $h in H$ with $b - h d eq.not 0$) instead
  of the single linear solution an oriented collision supplies.
]

Together these say: the non-unit orbit is large, but the only ways to *use* it in
a coefficient-tracking walk either (i) require an orientation multiplier that, once
returned, already solves ECDLP (Theorems 5–6), or (ii) discard the orientation and
inflate each collision into an $m$-way membership constraint (Proposition 7). Both
close the standard route. This resolves the boundary questions Q020 and Q024 in
their stated models.

= Limitations and open questions

We flag the boundaries of these results as sharply as the repository's ground
rules require.

*Model and scale.* The $sqrt(m)$ speedup (Proposition 3) is an
*ideal-random-mapping* heuristic, not a proof about a specific walk; the collision
table that realizes the ceiling uses $O(sqrt(r))$ memory and is therefore not a
constant-memory Pollard $rho$. All measurements are at toy scale
($log_2 p <= 18$, $r <= 262519$), and the five non-unit orders — however
suggestive — are five data points, not an asymptotic theorem that $m$ grows.

*The unoriented-constraint gap (Q025).* Proposition 7 leaves one avenue formally
open: a *nonlinear* solver that combines several unoriented membership constraints
$(a + b s) \/ (c + d s) in H$ directly, without reconstructing any individual
orientation multiplier, when the quotient index $q$ is two or three. We
preregistered an experiment (attempt A005) to intersect such synthetic constraints
at the five measured $D = -7$ sizes and count whether $O(log_q r)$ constraints
isolate the secret while total work stays sub-$sqrt(r)$. #tag("PROVED") That
experiment was *stopped before implementation* when the project was closed at the
user's direction; no A005 code or data exist, and Q025 is untested. We record this
as a workflow termination, not a mathematical refutation — the preregistered
constraint model and refutation criteria remain available for a future resumption.

*Cycle handling for higher-order units.* The order-four and order-six analogues of
the branchless / distinguished-point negation-map algorithms
@bkl2010 @bls2011 @wangzhang2011 were not built; our constant-memory attempts
(§6) failed, and only the memory-heavy collision table realized the ceiling. This
does not affect the *ceiling* itself, which bounds any correct implementation, but
it leaves the constant's practical realizability for $m in {4, 6}$ open.

*What we did not attempt.* We did not pursue the full class-polynomial CM method
@atkinmorain1993, using instead the two class-number-one explicit models and one
textbook non-unit example; and we did not seek non-cyclic or larger-$abs(D)$
endomorphism actions, which cannot beat the $sqrt(6)$ unit ceiling but might change
the non-unit orbit statistics.

= Conclusion

Small CM discriminant does not reduce ECDLP to an easier problem and does not
furnish a subexponential algorithm; the two structural routes it opens are both
bounded. The *unit* route ($D = -3, -4$) yields a Pollard-$rho$ collision speedup
whose idealized value is $sqrt(m)$ but whose exponent $m$ is capped at six by the
classification of imaginary-quadratic units, giving a hard constant ceiling of
$sqrt(6)$ — confirmed empirically over $3{,}200$ logarithms with no detectable
asymptotic drift, and realizable only with correct cycle handling. The *non-unit*
route ($D = -7$ and its kin) offers a large orbit, but we proved that selecting an
orbit representative costs $m - 1$ evaluations in the sequential model, that
addition does not descend to orbit classes, and that any canonicalizer returning
the orientation multiplier is itself an ECDLP solver in $q + 1$ calls — so the
orbit cannot be cashed in as a walk speedup. The one avenue we could not close —
combining several unoriented constraints nonlinearly when the index is two or
three (Q025) — is stated as open, with its experiment preregistered but unrun. The
CM discriminant is a scalar-multiplication accelerator, as GLV intended, and not a
door into the discrete logarithm.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
All results run at the toy parameters stated inline
($log_2 p <= 18$). The unit-orbit constructions and measurements use
`code/cm_units.py` and `code/measure_unit_rho.py`; the non-unit endomorphism and
its orbit costs use `code/cm_nonunit.py` and `code/measure_nonunit_orbits.py`.
The three principal datasets are the collision-table run
`measure_unit_rho_table_r20_b12-14-16-18_t200_s52022026_20260707_*` (raw, summary,
residuals, validation, and fit JSON), the naive-Floyd and doubling-escape variants
under the same stem, and the non-unit sweep
`measure_nonunit_orbits_b10-12-14-16-18_n16_s72022026_20260711_*`. Full commands
are in `code/README.md`; the collision-table sweep recovered all $3{,}200$
logarithms in $18.5$ s and the non-unit sweep validated five curves in $3.0$ s. The
three figures regenerate from the summary CSVs via
`papers/figures/P5.2/make.py`. Every mathematical claim above carries one of the
epistemic tags #tag("PROVED"), #tag("CITED"), #tag("HEURISTIC"),
#tag("EMPIRICAL", detail: "range") as used in the research log; untagged sentences
are exposition, not claims.
]

#bibliography("refs/P5.2.bib", title: [References], style: "ieee")
