#import "lib/paper.typ": *

#show: paper.with(
  title: "First Fall Is Not Solving: An Exact Degree Classification of the Quadratic Semaev--Weil Family",
  subtitle: "An unconditional upper bound, a growing first-fall/solving-degree gap, and the refutation of automatic field-equation nonredundancy",
  pid: "P1.3",
  keywords: ("ECDLP", "index calculus", "Semaev summation polynomials", "Weil restriction", "first fall degree", "solving degree", "Gröbner bases"),
  abstract: [
    The subexponential complexity claims for index calculus on elliptic curves
    rest on a heuristic: that the #emph[first fall degree] of the Weil-restricted
    Semaev system approximates the degree at which a Gröbner-basis engine
    actually terminates. The problem P1.3 asks for an unconditional, explicit
    degree bound for these systems that does #emph[not] invoke that heuristic. We
    give one, exactly, for the smallest nontrivial family — extension degree
    $n=2$ and decomposition length $m=2$ — and we show along the way that the
    heuristic is quantitatively false for the very systems it is applied to. We
    first fix four distinct degree invariants (first fall $d_"ff"$, Hilbert
    degree of regularity $d_"reg"$, grevlex solving degree $sans("sd")$, and a
    separate algorithm-trace statistic $D_cal(A)$) and separate all four on a
    single worked system over $FF_5$, where they take the values $3, 8, 4, 9$. We
    then prove that for every odd prime power $q >= 5$, a nonsingular
    short-Weierstrass curve over $FF_(q^2)$, and a non-base target
    $x$-coordinate, the quadratic Weil system satisfies
    $d_"ff" = 5$, $d_"reg" = q$, and $sans("sd")_"grevlex" <= q$
    #emph[unconditionally], the last bound obtained through a constant-degree
    mutant family and Salizzoni's regularity bound rather than through any
    first-fall assumption. The matching equality $sans("sd") = q$ holds for
    $q > 5$ exactly when the field equations enlarge the two-coordinate core
    ideal; the solving-minus-first-fall gap then grows without bound, reaching
    $18$ already at $q = 23$. Crucially, this nonredundancy is #emph[not]
    automatic: we exhibit an infinite family of genuine on-curve Semaev systems
    for every $q equiv 3 mod 4$ with redundant field equations, certified
    concretely at $q = 7$ where $(d_"ff", d_"reg", sans("sd")) = (5, 7, 5)$, and
    confirmed by exhaustive search over 50,376 eligible systems. The result
    is honest about its reach: it is an exact classification of one
    odd-characteristic family, not an all-parameter bound and not a statement
    about the binary $n tilde.op log q$ regime that motivates the cryptanalysis.
  ],
)

= Introduction

Index calculus is the reason elliptic-curve discrete logarithms over
#emph[extension] fields are not as hard as their group order suggests. The
Semaev--Gaudry--Diem template @semaev2004 @gaudry2009 @diem2011 reduces an ECDLP
instance on $E \/ FF_(q^n)$ to the problem of solving a polynomial system: one
writes a summation-polynomial relation $f_(m+1)(x_1, dots, x_m, x_R) = 0$ forcing
$m$ factor-base points to sum to a fixed point $R$, expands it through a
#emph[Weil restriction] into $n$ equations over the base field $FF_q$, and hunts
for base-field solutions with a Gröbner-basis engine. The cost of the whole
attack is dominated by that Gröbner computation, and the cost of the Gröbner
computation is governed by the largest polynomial degree the engine must reach
before it terminates.

That governing degree is hard to control directly, so the literature substitutes
a proxy. Petit and Quisquater @petitquisquater2012 derived their influential
subexponential estimate for binary ECDLP under the explicit assumption that the
#emph[degree of regularity] of the relevant Weil systems is only slightly larger
than their #emph[first fall degree] — the degree at which the first nontrivial
degree drop occurs in a Macaulay-style expansion. Hodges, Petit, and Schlather
@hodgespetit2014 formalized first fall degree through the associated graded
algebra of the finite-field function ring and proved general upper bounds for it,
while flagging (their §6.3) that its closeness to the true termination degree is
a #emph[heuristic]. Kousidis and Wiemers @kousidiswiemers2019 then proved a clean
first-fall bound $d_"ff" <= m^2 - m + 1$ for the binary case, but were careful to
note that a first-fall bound is not, by itself, a solving-degree bound.

The problem posed as P1.3 removes the crutch. It asks: given $q, n, m$, produce an
#emph[unconditional] explicit bound on the degree of regularity or solving degree
of the Weil-restricted Semaev system $S(q, n, m)$ #emph[without] assuming that its
first fall degree approximates either quantity. This is a request for a theorem
where the literature has a heuristic.

We answer it exactly for the smallest nondegenerate family, $n = m = 2$, and in
doing so we find that the heuristic is not merely unproven but quantitatively
wrong for these systems. Our central object is the two-coordinate quadratic Weil
system, and our central finding is a strict, growing separation between the first
fall degree and the solving degree of that system.

#keybox(title: "Main result")[
  For every odd prime power $q >= 5$, every nonsingular curve
  $E : Y^2 = X^3 + A X + B$ over $FF_(q^2)$, and every non-base target
  $x$-coordinate $T in.not FF_q$, the quadratic Weil--Semaev system
  $F = {G_0, G_1, x^q - x, y^q - y}$ satisfies, #emph[unconditionally],
  $
    d_"ff" = 5, quad d_"reg" = q, quad sans("sd")_"grevlex" <= q .
  $
  The first two are #emph[exact]; the third is a genuine upper bound obtained by
  a low-degree mutant family, #emph[not] from a first-fall assumption. The
  equality $sans("sd") = q$ holds for $q > 5$ #emph[iff] the field equations
  $x^q - x, y^q - y$ enlarge the core ideal $C = (G_0, G_1)$ — and that
  nonredundancy is #emph[not] automatic, even for nonsingular curves and on-curve
  targets. When it holds, the gap $sans("sd") - d_"ff" = q - 5$ grows without
  bound.
]

== Contributions and honest scope

We contribute (i) four fixed degree conventions and a single worked system over
$FF_5$ that separates all four (§3); (ii) an exact Semaev/Weil pipeline and the
measured expansion boundary of the summation polynomials (§4); (iii) the exact
first-fall and regularity values for the quadratic family, with proofs from the
top-ideal shape (§5); (iv) an #emph[unconditional] solving-degree upper bound via
a constant-degree mutant family and Salizzoni's theorem, plus a conditional
matching lower bound (§6); (v) the refutation of automatic field-equation
nonredundancy through an infinite genuine-Semaev counterexample family and an
exact $q = 7$ certificate (§7); and (vi) exhaustive and structured empirical
validation across $q in {3, dots, 23}$ (§8).

The scope is deliberately narrow and stated plainly. The exact classification is
a theorem only for $n = m = 2$ in odd characteristic. Automatic nonredundancy is
#emph[false], so the equality half of the result is genuinely conditional. We do
not obtain an all-parameter bound, and we do not touch the binary
$n tilde.op log q$ asymptotic regime that Petit--Quisquater and Kousidis--Wiemers
study; the growing gap we prove is not a refutation of their asymptotic
questions, which concern a different characteristic and a different scaling. What
we deliver is exactly what P1.3 asks for at the reachable parameters: an explicit,
heuristic-free degree bound, together with a precise account of where the
first-fall proxy breaks.

= Setting and notation

Fix a base field $FF_q$ with $q$ an odd prime power, and an extension
$FF_(q^n)$. Let $R = FF_q [x_1, dots, x_m]$ be the factor-base polynomial ring,
and let $B_q = R \/ (x_1^q, dots, x_m^q)$ be the finite-field function ring in
which first fall is computed. For a curve $E \/ FF_(q^n)$, Semaev's
$(m+1)$-th summation polynomial $f_(m+1)(X_1, dots, X_(m+1))$ vanishes exactly
when there exist points $P_i in E$ with $x(P_i) = X_i$ and
$P_1 + dots.c + P_(m+1) = O$ @semaev2004. Fixing $X_(m+1) = x(R)$ for a target
point $R$ and substituting $x_i in FF_q$-valued factor-base variables gives one
equation over $FF_(q^n)$; choosing a polynomial basis
$FF_(q^n) = FF_q [alpha]$ and equating the $n$ coordinate polynomials to zero
produces the #emph[Weil-restricted] system
$S(q, n, m) = {g_0, dots, g_(n-1)} subset R$. We write $x, y$ for $x_1, x_2$ in
the quadratic case, and throughout use the grevlex order with
$x_1 > dots.c > x_m$ (i.e. $x > y$).

The three ideal-theoretic invariants below are the fixed literature conventions;
the fourth is a run statistic we keep separate on purpose.

= Four degree invariants and an exact separation

The first task in P1.3, following its session-one target, is to stop conflating
distinct quantities. We adopt the conventions of Caminata and Gorla
@caminatagorla2023, tracing the first-fall definition back to Hodges, Petit, and
Schlather @hodgespetit2014.

#definition(name: "the four degrees")[
  #tag("CITED") For a nonhomogeneous system $F = {f_1, dots, f_s} subset R$ with
  top (highest-degree) parts $f_i^"top"$:

  #emph[(a) First fall degree.] With $"Syz"(F^"top")$ the syzygy module of the
  top parts and $"Triv"$ its trivial submodule (Koszul syzygies together with the
  $(f_i^"top")^(q-1) e_i$ induced by $B_q$),
  $
    d_"ff"(F) = min { d : "Syz"(F^"top")_d \/ "Triv"(F^"top")_d != 0 } .
  $

  #emph[(b) Degree of regularity.] When the top ideal is Artinian,
  $d_"reg"(F) = min { d : (F^"top")_d = R_d }$.

  #emph[(c) Solving degree.] For a degree-compatible order $sigma$,
  $sans("sd")_sigma(F)$ is the least cutoff $d$ for which the closed degree-$d$
  Macaulay row space $V_(F, d)$ contains a $sigma$-Gröbner basis of $(F)$.
]

#remark(name: "a fourth, non-invariant quantity")[
  #tag("PROVED") The largest degree #emph[printed] by a concrete engine,
  $D_cal(A)(F, sigma, theta)$ under a full option set $theta$, is a #emph[run
  statistic], not an ideal invariant: pair-selection criteria and preprocessing
  change it without changing $(F)$. Salizzoni's $V_(F, d)$ construction
  @salizzoni2023 and the closed Macaulay space in (c) are the #emph[same]
  invariant (the mutant solving degree of the XL literature), whereas the highest
  Magma step degree reported by Kousidis and Wiemers @kousidiswiemers2019 belongs
  to the $D_cal(A)$ column. Conflating these is precisely the confusion P1.3
  exists to remove.
]

These four notions are genuinely different, and a single small system makes the
gaps concrete. It is the $q = 5$ specialization of Caminata--Gorla's Example 4.2
@caminatagorla2023, augmented with the algorithm-trace measurement.

#proposition(name: [a system separating all four degrees])[
  #tag("PROVED") Over $FF_5 [x_1, x_2, x_3]$ with grevlex $x_1 > x_2 > x_3$, set
  $
    F = {x_1 x_2 + x_2, quad x_2^2 - 1, quad x_3^4 - 1, quad x_1^5 - x_1} .
  $
  Then $d_"ff"(F) = 3$, $sans("sd")_"grevlex"(F) = 4$, $d_"reg"(F) = 8$, and the
  specified FIFO naive-Buchberger run reaches degree
  $D_cal(A)(F) = 9$.
]

#proof[
  The nontrivial degree-$3$ relation is
  $x_2 (x_1 x_2) - x_1 (x_2^2) = 0$, giving $d_"ff" = 3$. The closed
  degree-$4$ Macaulay space contains
  $x_1 + 1 = x_2 (x_1 x_2 + x_2) - (x_1 + 1)(x_2^2 - 1)$, hence the whole
  Gröbner basis ${x_1 + 1, x_2^2 - 1, x_3^4 - 1}$, giving
  $sans("sd") = 4$. The top ideal $(x_1 x_2, x_2^2, x_3^4, x_1^5)$ first fills all
  forms in degree $8$, so $d_"reg" = 8$. Finally, the FIFO run processes the
  coprime pair whose leading-monomial LCM is $x_1^5 x_3^4$, of degree $9$. Each
  value is produced by an exact modular row reduction, and SymPy's
  Gröbner routine independently returns the stated basis.
]

The values $3, 8, 4, 9$ are pairwise distinct; in particular $d_"reg" - d_"ff" =
5$ and $sans("sd") - d_"ff" = 1$ #emph[on the same system]. The problem
statement's parenthetical identification of $d_"reg"$ with $sans("sd")$ is
therefore false without extra hypotheses. This is the local baseline against
which the Semaev-specific results below are read: whatever we prove for the Weil
family, we prove for #emph[named] invariants, never for an engine's log label.

= The Semaev--Weil pipeline and its expansion boundary

To measure anything on real systems we need the summation polynomials themselves
and an exact Weil restriction. Both are implemented over exact prime-field and
polynomial-basis arithmetic.

#proposition(name: [the coordinate Weil builder])[
  #tag("PROVED") Represent $FF_(q^n) = FF_q [alpha]$ in a polynomial basis,
  substitute factor-base variables $x_i in FF_q$, expand
  $f_(m+1)(x_1, dots, x_m, x_R)$ as an element of $FF_(q^n)[x_1, dots, x_m]$, and
  equate its $n$ basis coordinates to zero. The resulting base-field system
  $S(q, n, m)$ has exactly the base-field solutions in bijection with the
  extension-field zeros of $f_(m+1)( dot, x_R)$.
]

This is the explicit coordinate construction of Weil restriction used by Petit and
Quisquater @petitquisquater2012 and Kousidis and Wiemers @kousidiswiemers2019, and
matches the formalization of Caminata, Ceria, and Gorla @caminataceriagorla2023.
Every known-target system we build uses the nonsingular curve
$E : y^2 = x^3 + alpha x + 1$ (with $alpha$ the basis generator) unless a curve
is explicitly overridden, and each stored factor-base tuple is verified to vanish
in all $n$ Weil coordinates; singular inputs are rejected.

The Semaev polynomials grow fast, and honesty about #emph[which] ones we can
handle exactly matters. #ref(<fig:semaev>) records the exact sparse expansion
statistics.

#fig("/figures/P1.3/semaev.svg", width: 66%, caption: [
  #tag("EMPIRICAL", detail: "30 s / 250,000-term ceiling") Exact sparse
  expansion of the generic summation polynomials: $f_3$ has $13$ terms and total
  degree $4$, $f_4$ has $540$ terms and degree $12$, $f_5$ has 130,705 terms
  and degree $32$. Generic $f_6$ crosses the declared ceiling and is
  #emph[censored], not extrapolated; its independent recursive evaluator still
  passes a six-point zero-sum test over $FF_101$. Data:
  `measure_semaev_stats_20260623.csv`.
]) <fig:semaev>

The censoring is a hard resource boundary, recorded as such: the generic $f_6$
expansion exceeded both a $30$-second wall clock and a 250,000-term ceiling.
Consequently our exact degree measurements live at $m <= 4$, and our #emph[proved]
results at $m = 2$, where $f_3$ is a $13$-term quartic. All arithmetic is exact;
no numerical approximation enters at any stage.

= The quadratic family: first fall and regularity, exactly

We now fix $n = m = 2$ and prove the two exact invariants. Write
$FF_(q^2) = FF_q [u] \/ (u^2 + m_1 u + m_0)$ with $u^2 + m_1 u + m_0$ irreducible,
and let $T = t_0 + t_1 u$ with $t_1 != 0$ (the target $x$-coordinate is
non-base). For short-Weierstrass coefficients $A, B in FF_(q^2)$, let
$G_0, G_1 in FF_q [x, y]$ be the two Weil coordinates of $f_3(x, y, T)$, and set
$
  F = {G_0, G_1, x^q - x, y^q - y}, quad C = (G_0, G_1) .
$

The whole analysis is driven by the shape of the top parts.

#proposition(name: [the quadratic top shape])[
  #tag("PROVED") The top parts of the two $f_3$ coordinates are
  $
    G_0^"top" = x^2 y^2, quad
    G_1^"top" = c thin x y (x + y), quad c != 0 .
  $
]

#proof[
  Semaev's third polynomial for $E : y^2 = x^3 + A x + B$ is
  $
    f_3(X_1, X_2, X_3) = (X_1 - X_2)^2 X_3^2
      - 2 lr(((X_1 + X_2)(X_1 X_2 + A) + 2 B)) X_3
      + (X_1 X_2 - A)^2 - 4 B (X_1 + X_2) .
  $
  Taking the terms of highest factor-base degree in $x = X_1, y = X_2$ and
  splitting the two extension coordinates of the coefficient of $X_3 = T$ leaves
  $x^2 y^2$ in the coordinate along $1$ and $c thin x y (x + y)$ in the coordinate
  along $u$, with $c$ a nonzero $FF_q$-multiple of $t_1$; irreducibility of the
  modulus and $t_1 != 0$ give $c != 0$.
]

#theorem(name: [first fall degree of the quadratic family])[
  #tag("PROVED") For every odd prime power $q >= 5$ and non-base target,
  $d_"ff"(G_0, G_1) = 5$.
]

#proof[
  At degree $5$ the relation
  $
    (x + y) G_0^"top" - c^(-1) x y thin G_1^"top" = 0
  $
  holds identically, since both terms equal $x^2 y^2 (x + y)$. It is nontrivial:
  the first Koszul syzygy has degree $deg G_0^"top" + deg G_1^"top" = 7$, and the
  quotient-trivial syzygies $(G_i^"top")^(q-1) e_i$ occur in degree
  $(q-1) dot deg G_i^"top" >= 8$. No relation exists in degree $3$ (a single
  generator cannot syzygy alone). A putative degree-$4$ relation
  $A' G_0^"top" + (B' x + C' y) G_1^"top" = 0$ expands to
  $A' x^2 y^2 + c B'(x^3 y + x^2 y^2) + c C'(x^2 y^2 + x y^3)$; the coefficients
  of the distinct monomials $x^3 y$ and $x y^3$ force $B' = C' = 0$, then
  $A' = 0$. Hence the first nontrivial relation is in degree $5$.
]

#theorem(name: [degree of regularity of the quadratic family])[
  #tag("PROVED") For every odd prime power $q >= 5$ and non-base target,
  $d_"reg"(F) = q$.
]

#proof[
  The top ideal of $F$ is
  $J = (x^2 y^2, thin x y (x + y), thin x^q, thin y^q)$ (the last two from the
  field equations). The monomial $x^(q-1)$ is divisible by none of the
  generators of degree $<= q - 1$ — those are $x^2 y^2$ and $x y (x + y)$, each
  requiring both variables — so $J_(q-1) != R_(q-1)$. In degree $q$: the pure
  powers $x^q, y^q in J$; every mixed monomial $x^a y^(q - a)$ with
  $2 <= a <= q - 2$ is divisible by $x^2 y^2$. The two boundary monomials are
  reached through $x y (x + y)$: since
  $x^(q-3) dot x y (x + y) = x^(q-1) y + x^(q-2) y^2$ and the second term is
  divisible by $x^2 y^2$, we get $x^(q-1) y in J$ modulo covered monomials, and
  symmetrically $x y^(q-1) in J$. Thus $J_q = R_q$ while $J_(q-1) != R_(q-1)$, so
  $d_"reg"(F) = q$.
]

Two facts deserve emphasis. First, $d_"reg"$ depends on the input #emph[top
parts], not on the ideal alone: it is the field-equation top parts $x^q, y^q$
that drive $d_"reg"$ up to $q$, exactly as Caminata and Gorla warn
@caminatagorla2023. Second, $d_"ff" = 5$ is #emph[constant] in $q$, so the pair
$(d_"ff", d_"reg") = (5, q)$ already exhibits an unbounded gap — but $d_"reg"$ is
an over-estimate of the true solving cost, and the interesting question is where
$sans("sd")$ actually lands.

= The solving-degree bounds

The heart of P1.3 is a solving-degree bound that does not assume first fall is a
good proxy. We give an unconditional #emph[upper] bound and a conditional
matching #emph[lower] bound.

== An unconditional upper bound via a mutant family

The strategy is to replace the two degree-$q$ field equations by low-degree
remainders modulo a #emph[universal] Gröbner basis of the core $C$, staying
inside the original closed degree-$q$ Macaulay space the whole time.

#lemma(name: [the universal core basis])[
  #tag("PROVED") Write $s = x + y$, $p = x y$. In these symmetric variables the
  two core coordinates normalize by invertible row operations to
  $
    H_0 = p^2 + b p + c s^2 + d s + e, quad
    H_1 = p s + f p + g s^2 + h s + i .
  $
  Over the localized ring
  $ZZ[b, c, d, e, f, g, h, i][(c + g^2)^(-1)]$ the grevlex ($x > y$) Gröbner
  basis of $(H_0, H_1)$ has exactly four elements, of total degrees $4, 4, 3, 3$
  and leading monomials $x y^3, thin y^4, thin x^3, thin x^2 y$. The only
  nonconstant denominator arising in the computation is $c + g^2$, and for the
  Semaev specialization
  $
    c + g^2 = (m_1^2 - 4 m_0) t_1^2 \/ 4 != 0 .
  $
]

#proof[
  The exact certificate `certify_quadratic_family.py` checks every one of the
  six Buchberger pairs over the localized ring, records explicit basis
  representations, and finds maximum denominator power $3$ in $(c + g^2)$. The
  nonvanishing of $c + g^2$ uses irreducibility of the odd-characteristic
  quadratic modulus (so its discriminant $m_1^2 - 4 m_0 != 0$) and $t_1 != 0$; a
  quartic top-part minor of determinant $-1$ certifies the rank claim after every
  valid finite-field specialization. The results are stored in
  `certify_quadratic_family_20260716.json`.
]

#theorem(name: [unconditional solving-degree upper bound])[
  #tag("PROVED") For every odd prime power $q >= 5$ and non-base target,
  $sans("sd")_"grevlex"(F) <= q$.
]

#proof[
  By the lemma the four core-basis elements have degree $<= 4$ and lie in the
  closed degree-$5$ core space $V_({G_0, G_1}, 5)$: three appear in the initial
  degree-$5$ Macaulay span and the fourth is obtained by multiplying lower-degree
  rows inside the closed space. Divide $x^q - x$ and $y^q - y$ by this basis;
  the leading monomials $x y^3, y^4, x^3, x^2 y$ leave remainders $r_x, r_y$
  supported on standard monomials of degree $<= 3$. Polynomial division is
  degree-compatible and the basis is already in $V_(F, q)$, so
  $r_x, r_y in V_(F, q)$. The mutant family
  $
    F' = { "four core-basis elements", thin r_x, thin r_y }
  $
  generates $(F)$, has maximum input degree $<= 4$, and has degree of regularity
  $<= 4$ because its top ideal already contains leading monomials covering every
  degree-$4$ monomial. Salizzoni's Proposition 3.10 @salizzoni2023,
  $
    sans("sd")_sigma(F') <= max { d_"reg"(F') + 1, thin max_(f in F') deg f } ,
  $
  gives $sans("sd")(F') <= 5$. Since $F' subset.eq V_(F, q)$ and $q >= 5$,
  closed-space stability yields $V_(F', 5) subset.eq V_(F, q)$, so a grevlex
  basis of $(F') = (F)$ lies in $V_(F, q)$, i.e. $sans("sd")_"grevlex"(F) <= q$.
]

This is exactly the deliverable P1.3 requests: an explicit degree bound derived
from commutative-algebra invariants (a constant-degree mutant family and
Salizzoni's regularity bound), with #emph[no] appeal to the first-fall heuristic.
We tried the more obvious route first — bounding solving degree by the
Castelnuovo--Mumford regularity of the homogenized input, per Caminata--Gorla
@caminatagorla2021 — and it fails: the representative $q = 5$ system is #emph[not]
$t$-saturated, its saturation adding the low-degree elements $x + y - t$ and
$y^2 - t y$. Remark 4.6 of @caminatagorla2021 is precisely this warning, and it
is why the mutant-family route is necessary.

== A conditional matching lower bound

#theorem(name: [conditional lower bound and exact equality])[
  #tag("CONDITIONAL", detail: "(F) ⊋ C") If at least one field equation lies
  outside the core ideal $C$, then $sans("sd")_"grevlex"(F) >= q$, and combined
  with the upper bound, $sans("sd")_"grevlex"(F) = q$.
]

#proof[
  For $d < q$ the degree-$q$ field equations cannot enter the closed space, so
  $V_(F, d) = V_({G_0, G_1}, d) subset.eq C$. If this space contained a Gröbner
  basis of $(F)$, then $(F) subset.eq C$, contradicting $(F) supset.neq C$.
  Hence no cutoff below $q$ suffices, and $sans("sd")(F) >= q$.
]

So the entire equality $sans("sd") = q$ hinges on whether the field equations are
#emph[redundant] over the core. Because $C$ is symmetric in $x, y$, either both
field equations belong to $C$ or neither does, and the redundancy question has a
clean algebraic characterization.

#proposition(name: [the redundancy criterion])[
  #tag("PROVED") Let $A_C = FF_q [x, y] \/ C$. The universal core basis has
  standard monomials $1, y, y^2, y^3, x, x y, x y^2, x^2$, so
  $dim_(FF_q) A_C = 8$. The following are equivalent:
  #box(inset: (left: 0.6em))[
    #set enum(numbering: "(1)")
    + $x^q - x, thin y^q - y in C$;
    + both field-equation normal forms by the core basis are zero;
    + the $q$-Frobenius endomorphism of $A_C$ is the identity;
    + $A_C tilde.equiv FF_q^8$;
    + the core has eight distinct algebraic-closure zeros, all in $FF_q^2$.
  ]
]

Nonredundancy — the hypothesis of the equality theorem — is exactly the failure
of (1)–(5). One might hope it is #emph[automatic] for genuine on-curve Semaev
systems. It is not, and that is the subject of the next section.

= Refuting automatic field-equation nonredundancy

Session four's decisive finding is a negative one, and we present it as such: the
tempting conjecture that a nonsingular curve with an on-curve non-base target
always yields nonredundant field equations is #emph[false], with an infinite
explicit counterexample family.

#theorem(name: [an infinite redundant Semaev family])[
  #tag("PROVED") Let $q equiv 3 mod 4$, $q >= 7$, and
  $FF_(q^2) = FF_q [u] \/ (u^2 + 1)$. Choose
  $h in FF_q^times without {1, -1}$ and set
  $
    rho = (h + h^(-1)) \/ 2, quad
    sigma = (h^(-1) - h) \/ 2, quad
    a = -4 sigma^2 .
  $
  Then $E : Y^2 = X^3 + a X$ is nonsingular, the point
  $R = (2 u, thin 2 rho (1 - u))$ lies on $E$ with non-base $x$-coordinate, and
  the two coordinates of $f_3(x, y, 2 u)$ generate the same ideal as
  $
    H_0 = (x y - a)^2 - 4 (x - y)^2, quad H_1 = (x + y)(x y + a) .
  $
  Both field equations $x^q - x, thin y^q - y$ are redundant: they lie in
  $C = (H_0, H_1)$.
]

#proof[
  Since $-1$ is a nonsquare (as $q equiv 3 mod 4$) and
  $rho^2 - sigma^2 = 1$, one has $rho != 0$ and, by the restriction on $h$,
  $sigma != 0$, so $a != 0$ and $E$ is nonsingular. Both sides of the curve
  equation at $R$ equal $-8 rho^2 u$. The branch $x + y = 0$ of $C$ gives the
  four points $(z, -z)$ with $z in {plus.minus 2(1 + rho), plus.minus 2(1 -
  rho)}$; the branch $x y = -a = 4 sigma^2$ gives two ordered roots of sum
  $4 sigma rho$ (discriminant $16 sigma^4$), their swap, and both negatives.
  These eight points are distinct and lie in $FF_q^2$; a collision between
  branches would make $-1$ a square. The universal basis gives quotient dimension
  $8$ (its sole specialization factor is $(m_1^2 - 4 m_0) t_1^2 \/ 4 = -4 != 0$
  here), so eight distinct zeros force $A_C tilde.equiv FF_q^8$; by the
  redundancy criterion the field equations belong to $C$.
]

#corollary(name: [the smallest concrete counterexample])[
  #tag("PROVED") Take $q = 7$, $h = 2$, so $rho = 3$, $sigma = 1$, $a = 3$. Over
  $FF_49 = FF_7 [u] \/ (u^2 + 1)$ use $E : Y^2 = X^3 + 3 X$ and
  $R = (2 u, thin 6 + u)$. Then both field-equation normal forms vanish and
  $
    (d_"ff", d_"reg", sans("sd")_"grevlex") = (5, 7, 5) .
  $
]

#proof[
  The core generators are $G_0 = x^2 y^2 + 3 x^2 + 2 x y + 3 y^2 + 2$ and
  $G_1 = 3 x^2 y + 3 x y^2 + 2 x + 2 y$, with reduced grevlex basis
  ${x y^3 - 3 x^2 + x y - 2, thin y^4 - 3 y^2 + 2, thin x^3 + x + y^3 + y, thin
  x^2 y + x y^2 + 3 x + 3 y}$. Exact division gives zero normal forms for both
  $x^7 - x$ and $y^7 - y$. The closed degree-$4$ space has rank $4$ and omits two
  basis elements; the degree-$5$ space contains all four. Hence $sans("sd") = 5$,
  strictly below $d_"reg" = 7$. The certificate
  `certify_quadratic_field_equations.py` checks the symbolic family over
  $ZZ[1\/2, h, h^(-1), u] \/ (u^2 + 1)$ and the concrete normal forms, quotient
  multiplication matrices, and closed spaces.
]

This is a counterexample #emph[inside the actual on-curve Semaev family], not
merely inside an abstract family with the same top-degree shape. Its eight core
zeros, split cleanly across the two branches, are shown in the right panel of
#ref(<fig:redundancy>). The left panel is the exhaustive census that both locates
these six redundant $q = 7$ systems and confirms their absence at $q = 5, 9$.

#fig("/figures/P1.3/redundancy.svg", width: 100%, caption: [
  #tag("EMPIRICAL", detail: "exhaustive q=5,7,9") #emph[Left:] histogram of the
  number of rational core-ideal zeros over all eligible nonsingular
  curve/non-base-target systems; redundancy requires the maximum count of eight,
  achieved only by six systems at $q = 7$. #emph[Right:] the eight base-field
  core zeros of the $q = 7$ counterexample, four on the branch $x + y = 0$ and
  four on $x y = 4$. Data: `search_quadratic_redundancy_20260716.json`,
  `certify_quadratic_field_equations_20260716.json`.
]) <fig:redundancy>

Consequently the unconditional statement is $sans("sd") <= q$, and the equality
$sans("sd") = q$ genuinely requires the nonredundancy hypothesis — which cannot be
dropped. We flag this exactly as the research log does: a former six-prime
solving-degree #emph[conjecture] survives only as a #emph[conditional] theorem.

= Empirical validation

Every proved value is anchored by exact measurement, and the honest ranges,
censored rows, and search counts are reported without smoothing.

== The measured degree table

#ref(<fig:growth>) plots the two families that matter, and #ref(<tab:main>)
tabulates the underlying rows. All values come from exact closed Macaulay spaces
with SymPy-verified Gröbner-basis containment; a dash is a #emph[censored] value,
never an estimate.

#fig("/figures/P1.3/growth.svg", width: 100%, caption: [
  #tag("EMPIRICAL", detail: "known-target rows, q up to 23") #emph[Left:]
  $n = m = 2$. First fall stays at $5$ while $sans("sd") = d_"reg" = q$, so the
  solving-minus-first-fall gap grows to $18$ at $q = 23$. #emph[Right:]
  $n = 3, thin m = 2$. Here $sans("sd")$ stays at $4$ while $d_"reg"$ climbs with
  $q$ — a live demonstration that $d_"reg"$ and $sans("sd")$ are different
  columns. Data: `first_fall_vs_solving_20260701.csv`.
]) <fig:growth>

#figure(
  table(
    columns: (auto,) * 8,
    align: (center,) * 8,
    table.hline(stroke: 0.7pt),
    table.header(
      [$q$], [$n$], [$m$], [$d_"ff"$], [$d_"reg"$], [$sans("sd")$],
      [$sans("sd") - d_"ff"$], [root],
    ),
    table.hline(stroke: 0.5pt),
    [3], [2], [2], [4], [4], [4], [0], [✓],
    [5], [2], [2], [5], [5], [5], [0], [✓],
    [7], [2], [2], [5], [7], [7], [2], [✓],
    [11], [2], [2], [5], [11], [11], [6], [✓],
    [13], [2], [2], [5], [13], [13], [8], [✓],
    [17], [2], [2], [5], [17], [17], [12], [✓],
    [19], [2], [2], [5], [19], [19], [14], [✓],
    [23], [2], [2], [5], [23], [23], [18], [✓],
    table.hline(stroke: 0.3pt),
    [3], [3], [2], [3], [4], [4], [1], [✓],
    [5], [3], [2], [3], [5], [4], [1], [✓],
    [7], [3], [2], [3], [7], [4], [1], [✓],
    [11], [3], [2], [3], [11], [4], [1], [✓],
    [13], [3], [2], [3], [13], [4], [1], [✓],
    [17], [3], [2], [3], [17], [4], [1], [✓],
    table.hline(stroke: 0.3pt),
    [5], [2], [3], [12], [12], [12], [0], [✓],
    [5], [3], [3], [11], [12], [12], [1], [✓],
    [3], [2], [4], [8], [8], [8], [0], [✓],
    [5], [2], [4], [16], [16], [—], [—], [✓],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Known-target subset of `first_fall_vs_solving_20260701.csv`. The
  $n = m = 2$ block realizes the exact theorem; the $n = 3, m = 2$ block shows
  $sans("sd") = 4 < d_"reg" = q$; the last rows reach the resource boundary
  ($q = 5, m = 4$ is censored after the regularity stage at $60$ s).],
) <tab:main>

Two independent separations appear in one table. In the $n = m = 2$ block,
$sans("sd") - d_"ff"$ grows as $q - 5$; in the $n = 3, m = 2$ block, $d_"reg"$
grows to $q$ while $sans("sd")$ is pinned at $4$. The first refutes "first fall
approximates solving"; the second refutes "regularity equals solving." Both are
exactly the confusions P1.3 targets.

== Curve/target variation and exhaustive searches

Beyond the single known target, we varied curves and targets extensively.
#ref(<tab:searches>) collects the two kinds of evidence: a structured
verified-root sample, and #emph[exhaustive] enumeration at small $q$.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, center, center, center, left),
    table.hline(stroke: 0.7pt),
    table.header(
      [*Search*], [$q$], [*Eligible*], [*Redundant*], [*Outcome*],
    ),
    table.hline(stroke: 0.5pt),
    [Structured verified-root sample], [5], [171], [0],
      [all $(5, q, q)$],
    [ (fixed non-base $A_1$)], [7], [190], [0], [all $(5, q, q)$],
    [], [11], [36], [0], [all $(5, q, q)$],
    table.hline(stroke: 0.3pt),
    [Exhaustive curve/target], [5], [6,228], [0], [no redundant core],
    [], [7], [50,376], [6], [six redundant systems],
    [], [9], [236,160], [0], [no redundant core],
    table.hline(stroke: 0.3pt),
    [Abstract top-shape trials], [5], [566], [—],
      [tuple $(3,1,4,0,1,2,0,3)$: $sans("sd") = 6$],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Validation searches. The $397$-case structured sample
  (`quadratic_family_summary_20260709.csv`) fixed a non-base coefficient of $A$
  and so #emph[missed] the base-defined counterexample family — a selection bias
  the exhaustive $q = 7$ enumeration
  (`search_quadratic_redundancy_20260716.json`) exposed. The abstract trial
  (`search_quadratic_counterexamples_20260709.csv`) hits $c + g^2 = 0$, the very
  denominator pole excluded by the Semaev modulus.],
) <tab:searches>

Three lessons are recorded. First, the exhaustive $q = 7$ search finds #emph[all
six] redundant systems and matches the infinite-family construction; the
structured sampler found none because it fixed a nonzero extension coordinate of
$A$, excluding the base-defined curves $Y^2 = X^3 + a X$ where redundancy occurs.
Second, at $q = 9$ (the smallest non-prime odd prime power in scope) an
exhaustive search over 236,160 eligible on-curve targets finds no redundant
core, consistent with the family's $q equiv 3 mod 4$ hypothesis. Third, the
abstract counterexample $(3, 1, 4, 0, 1, 2, 0, 3)$ with $sans("sd") = 6$ shows the
top shape #emph[alone] does not force $sans("sd") <= q$: the nonvanishing of
$c + g^2$ is essential, and it fails for that abstract tuple while holding for
every genuine Semaev system.

= Relation to prior bounds, obstruction, and limitations

The result sits precisely against the literature it draws on, and its boundaries
are sharp.

#emph[Against the first-fall heuristic.] Petit and Quisquater
@petitquisquater2012 assume $d_"reg" approx d_"ff"$ for binary Weil systems; for
our odd-characteristic quadratic family $d_"reg" = q$ while $d_"ff" = 5$, so the
proxy is off by $q - 5$. This is not a contradiction of their asymptotic claim —
their regime is binary with $n$ large — but it is a concrete demonstration, on
genuine Semaev systems, that the gap the heuristic assumes away can be arbitrarily
large. Hodges, Petit, and Schlather @hodgespetit2014 anticipated exactly this by
labelling the closeness a heuristic; we make the failure quantitative.

#emph[Against general invariant-gap examples.] Caminata and Gorla
@caminatagorla2023 already prove families with arbitrarily large gaps in either
direction, and their Example 4.2 has $d_"ff" = 3$, $sans("sd") = q - 1$,
$d_"reg" = 2 q - 2$ even after field equations. Our contribution is #emph[not] the
existence of a gap in the abstract; it is the exact classification of a
#emph[specific, deterministic, odd-characteristic Semaev/Weil family] with
verified roots. The local result is new only as an exact observation about this
construction.

#emph[Against the solving-degree bounds we use.] Caminata, Ceria, and Gorla
@caminataceriagorla2023 give general Weil-restriction solving-degree bounds via
homogenized source regularity; Salizzoni @salizzoni2023 gives the closed-space
bound we invoke. Converting the general bounds into a #emph[sharp] explicit
function of $q, n, m$ still needs control of the source-system regularity, which
our experiments do not supply beyond $n = m = 2$. That is the honest obstruction.

#emph[Limitations, stated without hedging.] The exact theorem holds only for
$n = m = 2$ in odd characteristic. Automatic field-equation nonredundancy is
#emph[false], so the equality half is conditional and the condition is not
cosmetic. A bounded $n = 3, m = 2$ check over $q in {3, 5, 7, 11}$ found
core bases of degree $<= 3$ and field remainders of degree $<= 2$, hinting at a
low-degree mutant mechanism — but this is #emph[empirical only], not a symbolic
$n = 3$ theorem. The $q = 5, m = 4$ cases were censored after the exact
first-fall and regularity stages ($d_"ff" = d_"reg" = 16$) but before
Gröbner-basis containment at a $60$-second ceiling. And nothing here transfers to
the binary $n tilde.op log q$ regime studied by Kousidis and Wiemers
@kousidiswiemers2019: their $d_"ff" <= m^2 - m + 1$ bound and its asymptotic
question live in a different characteristic and scaling, untouched by this
odd-characteristic, fixed-$n$ classification.

= Conclusion

P1.3 asked for an unconditional, explicit degree bound on Weil-restricted Semaev
systems that does not lean on the first-fall heuristic. For the smallest
nontrivial family we delivered exactly that: $d_"ff" = 5$ and $d_"reg" = q$ are
proved from the top-ideal shape, and $sans("sd")_"grevlex" <= q$ is proved
#emph[unconditionally] through a constant-degree mutant family and Salizzoni's
regularity bound — a commutative-algebra argument, not a heuristic. Along the way
the heuristic itself is shown to fail quantitatively for these systems: the
solving-minus-first-fall gap grows as $q - 5$, reaching $18$ at $q = 23$. The
matching equality $sans("sd") = q$ is genuinely conditional on the field
equations enlarging the core ideal, and we proved that this nonredundancy is
#emph[not] automatic by exhibiting an infinite on-curve counterexample family for
every $q equiv 3 mod 4$, certified concretely at $q = 7$ and confirmed by
exhaustive search. What remains open is the all-parameter bound and even a
symbolic $n = 3, m = 2$ theorem; we record the promising bounded evidence for the
latter as evidence, not as a claim.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
All computations are exact over prime fields and polynomial-basis extensions
using Python 3.13.4 and SymPy 1.14.0; Sage, Singular, msolve, and Macaulay2 were
unavailable in the working environment, and the closed-Macaulay solving-degree
routine is a hand-built exact implementation. The measurement scripts are
`measure_toy_degrees.py` (the four-degree separation), `sparse_weil.py` and
`measure_semaev_stats.py` (Semaev expansion and Weil restriction),
`measure_weil_degrees.py` (the canonical degree table),
`measure_quadratic_variants.py` and `summarize_quadratic_variants.py`
(curve/target variation), `certify_quadratic_family.py` (the localized-ring core
certificate), `certify_quadratic_field_equations.py` (the infinite counterexample
family and the $q = 7$ certificate), and `search_quadratic_redundancy.py` and
`search_quadratic_counterexamples.py` (the exhaustive and abstract searches).
Each degree row records the field model, curve, target, root check,
engine/version, monomial order, resource ceilings, elapsed time, and last
completed pipeline stage; censored rows are preserved as such and never
extrapolated. Every mathematical claim above carries one of the epistemic tags
#tag("PROVED"), #tag("CITED"), #tag("CONDITIONAL", detail: "hypothesis"), or
#tag("EMPIRICAL", detail: "range") as used in the research log; untagged sentences
are exposition, not claims.
]

#bibliography("refs/P1.3.bib", title: [References], style: "ieee")
