#import "lib/paper.typ": *

#show: paper.with(
  title: "Classifying Weil-Descent Vulnerability of Binary Elliptic Curves by Frobenius Span",
  subtitle: "An exact pure-arithmetic reconstruction of the GHS magic number, an exhaustive genus census for F₂ⁿ (n = 4, 6, 8), and the honest gap between low genus and a discrete-log speedup",
  pid: "P1.4",
  keywords: ("Weil descent", "GHS attack", "elliptic curve discrete logarithm", "hyperelliptic curves", "Frobenius span", "genus"),
  abstract: [
    The GHS attack transfers the discrete logarithm on an elliptic curve
    $E \/ FF_(q^n)$ in characteristic two to a hyperelliptic Jacobian over the
    subfield $FF_q$, and the transfer is dangerous exactly when the resulting
    genus is small enough that index calculus on the Jacobian beats a
    square-root search on the source. Deciding, for a given curve and a genus
    bound, whether such a low-genus cover exists is the classification problem
    posed as P1.4. We report a deliberately narrow but fully exact and
    reproducible slice of that problem. For the ordinary binary model
    $E : y^2 + x y = x^3 + a x^2 + b$ we recompute the GHS invariant with nothing
    but polynomial-basis arithmetic over $FF_2$ and binary Gaussian elimination:
    the magic number is the $FF_2$-dimension $m$ of the span of the pairs
    $(1, sigma^i sqrt(b))$, and Hess's exact formula
    $g = 2^(m-1) - 2^(m-r) + 1$ resolves the genus from the conjugate-span
    dimension $r$. We reproduce the published $FF_(2^155) \/ FF_(2^5)$ example of
    genus $31$ with an independently chosen degree-$155$ modulus, then
    exhaustively census every nonzero $b$ for $n in {4, 6, 8}$ — all $333$
    parameters — verifying Frobenius-invariance of the invariant on each. The
    genus distribution is heavy-tailed and two-branched; the lower branch
    $2^(m-1) - 1$ first appears at $n = 6$; and the low-genus locus
    ${b : g(b) <= 2^(n\/2)}$ is, for each tested degree, exactly the nonzero
    kernel of a single linearized polynomial, with explicit closed-form
    equations in $b$ and in the $j$-coordinate $j = 1 \/ b$. We state the scope
    honestly, as the problem's ground rules demand: this classifies the *genus
    invariant*, not vulnerable curves. The census contains no subgroup orders,
    no explicit cover map, and no Jacobian discrete-log timings, so it cannot on
    its own establish any advantage over Pollard $rho$; a genuine end-to-end
    speedup, and the explicit function-field construction it would require,
    remain open.
  ],
)

= Introduction

Weil descent turns a hard problem over a big field into a possibly-easier
problem over a small one. Fix an elliptic curve $E$ over an extension field
$FF_(q^n)$ of characteristic two. The Weil restriction of scalars produces an
$n$-dimensional abelian variety over the base field $FF_q$; when this variety
contains, or covers, the Jacobian of a curve $C \/ FF_q$ of *low genus*, the
discrete logarithm on $E(FF_(q^n))$ maps into the divisor class group of $C$,
where index calculus can run. This is the GHS attack of Gaudry, Hess, and Smart
@ghs2002. Its danger is entirely a matter of *how low* the genus is: index
calculus on a genus-$g$ hyperelliptic Jacobian over $FF_q$ costs roughly
$q^(2 - 2\/g)$ up to subexponential refinements @gaudry2009 @engegaudrythome2011,
so the transfer is a threat precisely when $g$ is small relative to the group
size but the Jacobian is still large enough to carry the logarithm.

This makes the following a natural decision problem, and it is the one P1.4
poses. Given $E \/ FF_(q^n)$ and a genus bound $B$, decide whether a curve
$C \/ FF_q$ of genus at most $B$ admits a cover $C -> E$ defined over $FF_q$, and
construct the cover when it exists. The full problem is hard: it ranges over all
covers, all characteristics, and would ideally output the descended curve, the
cover map, and the induced homomorphism on divisor classes. We do not solve it.
We report an exact, exhaustively verified, but strictly *invariant-level* slice:
the classical characteristic-two GHS locus for the ordinary binary model, over
the base field $FF_2$, at extension degrees $n in {4, 6, 8}$.

Within that slice everything is decidable by elementary linear algebra over
$FF_2$, with no computer-algebra system in the loop. The GHS construction for the
model $E : y^2 + x y = x^3 + a x^2 + b$ is governed by a single integer, the
*magic number* $m$, defined as the $FF_2$-dimension of the span of the Frobenius
conjugates of $sqrt(b)$ together with the constant $1$ @ghs2002; the genus of the
descended hyperelliptic curve is then $2^(m-1)$ or $2^(m-1) - 1$, and Hess's
revisited analysis @hess2003 pins down which branch by an exact formula. We
compute $m$, the branch, and the genus for every nonzero $b$ in $FF_(2^n)$,
reproduce a published high-degree example as a regression, and read off the exact
structure of the low-genus locus.

#keybox(title: "What is established, and what is not")[
  For the ordinary binary curve $E : y^2 + x y = x^3 + b$ over $FF_(2^n)$, the
  classical GHS genus is an *exactly computable* $FF_2$-linear-algebra invariant
  of the Frobenius orbit of $sqrt(b)$. We reconstruct it from scratch, match the
  published $FF_(2^155)$ genus-$31$ example, and give the complete genus census
  for $n in {4, 6, 8}$ (all $333$ parameters). The low-genus locus
  ${b : g(b) <= 2^(n\/2)}$ is, at each degree, a single linearized-polynomial
  kernel with closed-form $b$- and $j$-equations. *This classifies the genus
  invariant, not attackable curves.* Low genus is a necessary ingredient of a
  GHS speedup, not a sufficient one: without subgroup orders, an explicit cover
  map, and a measured Jacobian discrete logarithm, none of these numbers
  demonstrates an advantage over generic square-root search. Those three
  ingredients are absent here and are recorded as open.
]

== Contributions and honest scope

We contribute (i) a self-contained derivation of the GHS magic number and the
exact genus branch as an $FF_2$-linear invariant, matching the implementation in
the repository's `ghs.py` (§3–§4); (ii) an independent reconstruction of the
published $FF_(2^155) \/ FF_(2^5)$ genus-$31$ example (§5); (iii) the complete,
Frobenius-checked genus census for $n in {4, 6, 8}$, with its two-branch
structure made explicit (§6, #ref(<fig:dist>), #ref(<fig:branch>)); (iv) a
closed-form description of the low-genus locus as a linearized-polynomial kernel,
with proved $j$-coordinate equations and Frobenius stability (§7,
#ref(<fig:cum>)); and (v) a faithful account of the obstruction — genus is not a
speedup — and the two open questions it leaves (§8).

The result is *partial by construction*. It closes the linear-algebra sub-goal of
P1.4 exactly and exhaustively at small degree, and it deliberately does not close
the construction sub-goal. We never build the descended function field, the curve
$C$, the cover $C -> E$, or the divisor map, and we never measure a discrete
logarithm; the census carries no elliptic-curve subgroup order. Consequently no
sentence below asserts that any curve in the census is broken. We mark every
claim with the repository's epistemic tags and keep the negative boundary in
plain view.

= Setting and notation

Throughout, $K = FF_(2^N)$ is a finite field of characteristic two, realized in a
polynomial basis: elements are integers $0 <= x < 2^N$ encoding the coefficient
vectors of representatives modulo a fixed irreducible binary polynomial of degree
$N$, and addition is bitwise exclusive-or. The descent base is $k = FF_(2^d)$ with
$d divides N$, the relative degree is $n = N \/ d$, and
$sigma : K -> K$, $sigma(x) = x^(2^d)$, is the $k$-linear Frobenius generating
$"Gal"(K \/ k)$, a cyclic group of order $n$. In the exhaustive census we take
$d = 1$, so $k = FF_2$, $sigma(x) = x^2$, and $n = N$.

We work with the *ordinary* short binary Weierstrass model
$
  E : y^2 + x y = x^3 + a x^2 + b, quad a, b in K, quad b eq.not 0 ,
$
which is nonsingular precisely because $b eq.not 0$, and is ordinary (nonzero
$j$-invariant) as opposed to supersingular. The point at infinity is $O$ and the
group is $E(FF_(q^n))$ with $sigma$ acting coordinatewise. Two elementary facts
about this model recur and are proved once, in §4.

#definition(name: [Frobenius orbit and span])[
  For $beta in K$ the *Frobenius orbit* of $beta$ (relative to $sigma$) is the
  tuple $(beta, sigma beta, dots, sigma^(n-1) beta)$, and its *conjugate span*
  is the $FF_2$-subspace
  $V(beta) = "span"_(FF_2) {sigma^i beta : 0 <= i < n} subset.eq K$. Its
  dimension is the *conjugate rank* $r = dim_(FF_2) V(beta)$.
]

Because $K$ is an $FF_2$-vector space of dimension $N$ and every $sigma^i beta$
is an $N$-bit vector, both the conjugate span and all downstream tests are
computed by binary Gaussian elimination on integers. We write $L_f$ for the
$FF_2$-linear (linearized, or additive) polynomial attached to a binary
polynomial $f(t) = sum_i f_i t^i in FF_2[t]$,
$
  L_f (x) = sum_i f_i x^(2^i) ,
$
so that $f(sigma) beta = 0$ if and only if $L_f (beta) = 0$: evaluating $f$ at
the Frobenius $sigma$ (with $d = 1$) is the same as evaluating the linearized
polynomial $L_f$ on field elements. The *Frobenius annihilator* of $beta$ is the
least-degree monic $f$ with $L_f (beta) = 0$; its degree equals the conjugate
rank $r$.

= The GHS construction as an F₂-linear invariant

We recall the GHS transfer only as far as the genus, which is all the exact slice
needs. The construction realizes the descended curve as the smooth model of a
fixed field inside an Artin–Schreier compositum over the rational function field
$k(x)$. Concretely, writing the source curve as an Artin–Schreier extension
$y^2 + y = f(x)$ of $k(x)$ (after the standard change of variable that clears the
$x y$ term), the descent forms the compositum of the $n$ Frobenius-conjugate
Artin–Schreier extensions $y_i^2 + y_i = sigma^i f(x)$ over $k(x)$ and takes an
$FF_2$-rational sub-extension. The genus of the resulting curve is controlled
entirely by how many of these Artin–Schreier classes are $FF_2$-independent,
which is the linear-algebra content below.

#definition(name: [the GHS magic number])[
  #tag("CITED") For $E : y^2 + x y = x^3 + a x^2 + b$ over $K = FF_(2^N)$ with
  descent base $k = FF_(2^d)$, $n = N \/ d$, the *magic number* is
  $
    m = dim_(FF_2) "span"_(FF_2) {(1, sigma^i sqrt(b)) : 0 <= i < n} ,
  $
  the dimension of the span of the pairs formed by the constant $1$ and the
  Frobenius conjugates of $sqrt(b)$ (Gaudry–Hess–Smart @ghs2002).
]

The pair-span dimension has a transparent reduction to the conjugate rank. The
projection $(1, sigma^i sqrt(b)) |-> sigma^i sqrt(b)$ maps the pair span onto the
conjugate span $V(sqrt(b))$, so $m in {r, r + 1}$, and $m = r$ exactly when the
constant $1$ already lies in $V(sqrt(b))$ as a field element:
$
  m = r + [1 in.not V(sqrt(b))] .
$
The implementation computes $m$ *twice* — once as the rank of the encoded pair
vectors, once from the containment test $1 in V(sqrt(b))$ via the reduction
above — and raises an error unless the two agree; they agree on all $333$
parameters, which is a nontrivial internal consistency check on the
linear-algebra core.

#definition(name: [GHS regularity])[
  #tag("CITED") The GHS genus formula holds under a regularity condition on the
  Artin–Schreier data @ghs2002. For the model above it is met when $n$ is odd, or
  when $m = n$, or when the absolute trace $"Tr"_(K \/ FF_2)(a) = 0$. The census
  fixes $a = 0$, so $"Tr"(a) = 0$ and regularity holds for every swept parameter.
]

Under regularity, GHS gives the genus as $2^(m-1)$ or $2^(m-1) - 1$; Hess's
revisited analysis makes the choice exact.

#proposition(name: [Hess's exact genus, specialized])[
  #tag("CITED") With $r$ the conjugate rank and $m$ the magic number, the genus
  of the descended hyperelliptic curve is
  $
    g = 2^(m-1) - 2^(m-r) + 1 ,
  $
  (Hess @hess2003). Consequently $g = 2^(m-1)$ when $1 in V(sqrt(b))$ (so
  $r = m$), and $g = 2^(m-1) - 1$ when $1 in.not V(sqrt(b))$ (so $m = r + 1$).
]

#proof[
  (Reduction of the branch, given the cited formula.) If $1 in V(sqrt(b))$ then
  $m = r$ and $2^(m-r) = 2^0 = 1$, so $g = 2^(m-1) - 1 + 1 = 2^(m-1)$. If
  $1 in.not V(sqrt(b))$ then $m = r + 1$, so $m - r = 1$ and $2^(m-r) = 2$, giving
  $g = 2^(m-1) - 2 + 1 = 2^(m-1) - 1$. Both are immediate arithmetic once the
  containment test fixes $m - r in {0, 1}$.
]

The two branches differ by exactly one, and the containment test for $1 in V(sqrt(b))$
— a single back-substitution against the echelon basis of the conjugate orbit —
decides between them. This is the sense in which the entire genus is an
$FF_2$-linear invariant of one Frobenius orbit: rank gives $r$, the containment
test $1 in V(sqrt(b))$ gives $m$, and Hess's formula gives $g$.

= The exact invariant algorithm

We describe the computation as implemented, because its exactness is the point:
no floating point, no Gröbner basis, no function-field arithmetic, only integer
bit-vectors over $FF_2$. The following two facts make the square root and the
$j$-coordinate unambiguous and cheap.

#proposition(name: [unique square root])[
  #tag("PROVED") In $K = FF_(2^N)$ every element $b$ has a unique square root,
  namely $sqrt(b) = b^(2^(N-1))$.
]

#proof[
  Squaring $x |-> x^2$ is the Frobenius automorphism of $K$; being an
  automorphism it is a bijection, so square roots are unique. Squaring the claimed
  value gives $lr((b^(2^(N-1))))^2 = b^(2^N) = b$, since $x^(2^N) = x$ for all
  $x in K$. Hence $b^(2^(N-1))$ is the square root. Equivalently $sqrt(b) = sigma_1^(N-1)(b)$
  with $sigma_1(x) = x^2$, which is how the implementation computes it.
]

#proposition(name: [$j$-invariant and the annihilator identity])[
  #tag("PROVED") For $E : y^2 + x y = x^3 + a x^2 + b$ the $j$-invariant is
  $j(E) = 1 \/ b$. Moreover the Frobenius annihilator of $b$ equals the Frobenius
  annihilator of $sqrt(b)$.
]

#proof[
  The characteristic-two Weierstrass invariants of this model give $c_4 = 1$ and
  discriminant $Delta = b$, whence $j = c_4^3 \/ Delta = 1 \/ b$; in particular
  $b eq.not 0$ is exactly nonsingularity and $j eq.not 0$ is ordinariness. For the
  annihilator identity, squaring commutes with Frobenius, so for any binary
  polynomial $f$, $L_f (b) = L_f (sqrt(b)^2) = L_f (sqrt(b))^2$ because $L_f$ is
  $FF_2$-linear and squaring is additive in characteristic two; thus
  $L_f (b) = 0 arrow.l.r.double L_f (sqrt(b)) = 0$, and the least-degree monic annihilators
  coincide. The map $b |-> sqrt(b)$ is an invertible $FF_2$-linear bijection on
  $K$, so it preserves ranks and containment as well.
]

The invariant is then assembled as follows, mirroring the `ghs_profile` routine.

#block(inset: (left: 0.6em), stroke: (left: 1.5pt + rule-col))[
  #set text(size: 9.6pt)
  #set par(first-line-indent: 0em, leading: 0.55em)
  *Input:* the field $K = FF_(2^N)$ (irreducible modulus fixed), a nonzero
  $b in K$, base degree $d divides N$. *Output:* rank $r$, magic number $m$,
  genus $g$.

  1. Compute $sqrt(b) = b^(2^(N-1))$ (Proposition 3).
  2. Form the Frobenius orbit $(sqrt(b), sigma sqrt(b), dots, sigma^(n-1) sqrt(b))$
     with $sigma = x^(2^d)$; verify it closes, i.e. $sigma^n sqrt(b) = sqrt(b)$.
  3. Reduce the orbit to an echelon $FF_2$-basis (`gf2_basis`); its size is the
     conjugate rank $r$.
  4. Find the least-degree monic annihilator $f$ with $L_f (sqrt(b)) = 0$ by
     enumerating candidates up to degree $n$ (`frobenius_annihilator`); assert
     $deg f = r$.
  5. Test whether $1 in V(sqrt(b))$ by back-substitution; set
     $m = r + [1 in.not V(sqrt(b))]$. Cross-check $m$ against the independent
     pair-vector rank.
  6. Return $g = 2^(m-1) - 2^(m-r) + 1$ (Proposition 2).
]

Every step is exact integer arithmetic over $FF_2$. Enumerating the annihilator up
to degree $n$ is the only super-linear step, and at the census degrees $n <= 8$ it
is trivially cheap; the entire sweep of all $333$ parameters runs in well under a
second. The assertion $deg f = r$ in step 4 is a second internal check: the
annihilator degree, computed by search, must equal the rank, computed by
elimination.

= Reproducing the published genus-31 example

Before the census we regression-test the invariant against a documented
high-degree example, exactly as the repository's `verify_published_example.py`
does. The Magma V2.19.8 handbook constructs, over $K = FF_(2^155)$ with
$sigma(x) = x^(2^5)$ and descent base $FF_(2^5)$ (so $n = N \/ d = 155 \/ 5 = 31$),
the element
$
  b = lr((frac(t^31 + 1, t^5 + t^2 + 1)))(sigma) . w
$
for a field generator $w$, and reports a descended function field of genus $31$
over $FF_(2^5)$ @magma2013. We reconstruct it with an *independently chosen*
irreducible degree-$155$ modulus, verifying the mathematics rather than the
handbook's field representation.

#proposition(name: [genus-31 regression])[
  #tag("EMPIRICAL", detail: "F_{2^155}/F_{2^5}, published example") The
  reconstruction finds Frobenius annihilator $t^5 + t^2 + 1$, conjugate rank
  $r = 5$, magic number $m = 6$, and genus $g = 31$, matching the documented
  value exactly.
]

The arithmetic is consistent end to end. The annihilator $t^5 + t^2 + 1$ is a
primitive degree-$5$ binary polynomial whose companion root has multiplicative
order $31 = 2^5 - 1$, so it divides $t^31 + 1$ and the quotient
$(t^31 + 1) \/ (t^5 + t^2 + 1)$ is an exact binary polynomial; applying that
quotient at $sigma$ to the generator projects onto the eigenline annihilated by
$t^5 + t^2 + 1$. The conjugate rank is therefore $r = 5$. The constant $1$ does
*not* lie in the conjugate span (this is a lower-branch case), so $m = r + 1 = 6$,
and Hess's formula returns
$
  g = 2^(m-1) - 2^(m-r) + 1 = 2^5 - 2^1 + 1 = 32 - 2 + 1 = 31 .
$
This single example exercises the full pipeline at a cryptographically
non-trivial degree and on the *lower* genus branch, which the small-degree census
below reaches only at $n = 6$.

= The exhaustive genus census

We now sweep every nonzero $b in FF_(2^n)$ for $n in {4, 6, 8}$ — $15 + 63 + 255 = 333$
parameters — computing the full invariant profile of each and, as a per-row
invariance check, recomputing the profile at the Frobenius image $sigma(b) = b^2$
and asserting it is identical. The check passes on all $333$ rows: the GHS
invariant is constant on Frobenius orbits, as it must be, because the annihilator
identity of Proposition 4 makes $b$ and $sqrt(b)$ (and all their conjugates) share
rank, magic number, and genus.

#figure(
  table(
    columns: (auto,) * 9,
    align: (center, center, center, center, center, left, center, right, right),
    table.hline(stroke: 0.7pt),
    table.header(
      [*n*], [*g*], [*m*], [*r*], [$bold(1 in V)$], [*annihilator* $f(t)$],
      [$bold(ell)$], [*count*], [*density*],
    ),
    table.hline(stroke: 0.5pt),
    [4], [1], [1], [1], [yes], $t+1$, [1], [1], [1/15],
    [4], [2], [2], [2], [yes], $t^2+1$, [2], [2], [2/15],
    [4], [4], [3], [3], [yes], $t^3+t^2+t+1$, [4], [4], [4/15],
    [4], [8], [4], [4], [yes], $t^4+1$, [4], [8], [8/15],
    table.hline(stroke: 0.3pt),
    [6], [1], [1], [1], [yes], $t+1$, [1], [1], [1/63],
    [6], [2], [2], [2], [yes], $t^2+1$, [2], [2], [2/63],
    [6], [3], [3], [2], [no], $t^2+t+1$, [3], [3], [1/21],
    [6], [4], [3], [3], [yes], $t^3+1$, [3], [3], [1/21],
    [6], [8], [4], [4], [yes], $t^4+t^3+t+1$, [6], [6], [2/21],
    [6], [15], [5], [4], [no], $t^4+t^2+1$, [6], [12], [4/21],
    [6], [16], [5], [5], [yes], $t^5+t^4+t^3+t^2+t+1$, [6], [12], [4/21],
    [6], [32], [6], [6], [yes], $t^6+1$, [6], [24], [8/21],
    table.hline(stroke: 0.3pt),
    [8], [1], [1], [1], [yes], $t+1$, [1], [1], [1/255],
    [8], [2], [2], [2], [yes], $t^2+1$, [2], [2], [2/255],
    [8], [4], [3], [3], [yes], $t^3+t^2+t+1$, [4], [4], [4/255],
    [8], [8], [4], [4], [yes], $t^4+1$, [4], [8], [8/255],
    [8], [16], [5], [5], [yes], $t^5+t^4+t+1$, [8], [16], [16/255],
    [8], [32], [6], [6], [yes], $t^6+t^4+t^2+1$, [8], [32], [32/255],
    [8], [64], [7], [7], [yes], $t^7+dots.c+1$, [8], [64], [64/255],
    [8], [128], [8], [8], [yes], $t^8+1$, [8], [128], [128/255],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Complete GHS genus census for the ordinary binary model over
  $FF_(2^n)$, all nonzero $b$, base $FF_2$. Columns: extension degree $n$, genus
  $g$, magic number $m$, conjugate rank $r$, whether $1$ lies in the conjugate
  span, the Frobenius annihilator $f(t)$ of $sqrt(b)$, orbit length $ell$,
  parameter count, and density among the $2^n - 1$ nonzero values. Rows sum to
  $15$, $63$, and $255$. Source:
  `ghs_genus_distribution_n4-6-8_20260623.csv`.],
) <tab:census>

#ref(<tab:census>) is the whole census in one table. Several features are worth
reading off, each tagged by how strongly it is established.

#tag("EMPIRICAL", detail: "n in {4,6,8}") *The distribution is heavy-tailed.*
The largest genus at each degree — $8$, $32$, $128$ for $n = 4, 6, 8$ — is taken
by more than a third of all parameters ($8\/15$, $8\/21$, $128\/255$
respectively), and the genus roughly doubles down the table while the counts fall
off. #ref(<fig:dist>) shows the counts on a log scale; the low-genus tail is thin.

#tag("EMPIRICAL", detail: "n in {4,6,8}") *The lower branch first appears at
$n = 6$.* For $n = 4$ and $n = 8$ every parameter has $1 in V(sqrt(b))$ and hence
takes the upper branch $g = 2^(m-1)$. Only at $n = 6$ does the containment fail:
the three parameters with annihilator $t^2 + t + 1$ give genus $3 = 2^2 - 1$, and
the twelve with annihilator $t^4 + t^2 + 1$ give genus $15 = 2^4 - 1$, a total of
$15$ of the $63$ parameters ($5\/21$) on the lower branch. This is the smallest
tested degree that is not a power of two, and it is the first to exhibit the
$2^(m-1) - 1$ branch at all.

#tag("EMPIRICAL", detail: "full-degree parameters, n in {4,6,8}") *Full-degree
parameters have a genus floor.* Restricting to parameters whose Frobenius orbit
has full length $ell = n$ (equivalently, $sqrt(b)$ generates $FF_(2^n)$ and lies
in no proper subfield), the minimum genus is $4$, $8$, and $16$ for
$n = 4, 6, 8$, attained by $4$, $6$, and $16$ parameters respectively. These are
the genuinely $n$-dimensional descents; the smaller genera in the table come from
$b$ lying in a proper subfield, where the orbit is short and the invariant
degenerates.

#fig("/figures/P1.4/distribution.svg", width: 86%, caption: [
  #tag("EMPIRICAL", detail: "all 333 nonzero b") The exact GHS genus census as a
  grouped log-scale histogram: number of nonzero $b in FF_(2^n)$ attaining each
  genus, one colour per degree $n in {4, 6, 8}$. The low-genus cells are sparsely
  populated; most parameters land in the largest few genera. Source:
  `ghs_genus_distribution_n4-6-8_20260623.csv`.
]) <fig:dist>

The two-branch structure is clearest against the magic number. Genus grows as
$2^(m-1)$ along the upper envelope, and the lower-branch points sit exactly one
below it. #ref(<fig:branch>) plots genus against $m$ with the two theoretical
envelopes, marking each census class by degree and branch.

#fig("/figures/P1.4/branch.svg", width: 78%, caption: [
  #tag("EMPIRICAL", detail: "distribution rows, n in {4,6,8}") Genus versus magic
  number $m$. Every census class lies on one of the two envelopes
  $g = 2^(m-1)$ (upper, $1 in V$) or $g = 2^(m-1) - 1$ (lower, $1 in.not V$);
  marker shape encodes the branch and colour encodes the degree. Point area grows
  with the (log) parameter count. The lower-branch squares occur only at $n = 6$
  in this range. Source: `ghs_genus_distribution_n4-6-8_20260623.csv`.
]) <fig:branch>

= The low-genus locus is one linearized-polynomial kernel

The security-relevant question is which parameters give *small* genus, so we fix a
uniform experimental slice and describe it exactly. For each degree put the
threshold $B_n = 2^(n\/2)$, and consider the low-genus locus
$
  cal(L)_n = {b in FF_(2^n)^times : g(b) <= B_n} .
$
The thresholds are $B_4 = 4$, $B_6 = 8$, $B_8 = 16$. We stress at the outset that
"$g <= B_n$" is a declared experimental convenience, *not* a proven attackability
boundary; §8 returns to this.

The structure of $cal(L)_n$ is strikingly simple: after adjoining $0$, it is
exactly the kernel of a single linearized polynomial. The mechanism is that the
genera below the threshold are realized by annihilators that all divide one
distinguished annihilator, so their kernels nest.

#proposition(name: [low-genus locus as a kernel])[
  #tag("EMPIRICAL", detail: "n in {4,6,8}") For each $n in {4, 6, 8}$ there is a
  binary polynomial $f_n$ such that $cal(L)_n union {0}$ equals the kernel
  ${x in FF_(2^n) : L_(f_n)(x) = 0}$ of the linearized polynomial $L_(f_n)$. The
  distinguished annihilators are
  $
    f_4 = t^3 + t^2 + t + 1 = (t + 1)^3, quad
    f_6 = t^4 + t^3 + t + 1 = (t + 1)^2 (t^2 + t + 1),
  $
  $
    f_8 = t^5 + t^4 + t + 1 = (t + 1)^5 ,
  $
  and the loci have $lr(|cal(L)_n|) = 7, 15, 31$ with densities $7\/15$, $5\/21$,
  $31\/255$ among the nonzero parameters.
]

The reason this holds, and is not a coincidence, is divisibility of annihilators.
The genus of a class is a monotone function of its annihilator under division: if
$f' divides f$ then $ker L_(f') subset.eq ker L_f$. Reading the census
(#ref(<tab:census>)), every annihilator whose class has $g <= B_n$ divides
$f_n$. For $n = 4$ the classes with $g in {1, 2, 4}$ have annihilators
$t + 1$, $t^2 + 1 = (t+1)^2$, and $t^3 + t^2 + t + 1 = (t+1)^3$, all dividing
$(t+1)^3 = f_4$; the counts $1 + 2 + 4 = 7$ fill $ker L_(f_4)$ exactly. For
$n = 6$ the classes with $g in {1, 2, 3, 4, 8}$ have annihilators
$t + 1$, $(t+1)^2$, $t^2 + t + 1$, $t^3 + 1 = (t+1)(t^2+t+1)$, and
$(t+1)^2(t^2+t+1) = f_6$, again nested, with $1 + 2 + 3 + 3 + 6 = 15$. For
$n = 8$ the classes with $g <= 16$ have annihilators $(t+1)^k$ for
$k = 1, dots, 5$, nested in $(t+1)^5 = f_8$, with $1 + 2 + 4 + 8 + 16 = 31$. The
locus is a single kernel because the largest-genus annihilator within the bound
is divisible by every smaller one.

That kernel is an $FF_2$-vector space, and it transports to a closed-form equation
in the geometric coordinate $j = 1 \/ b$.

#proposition(name: [locus equations and their properties])[
  #tag("PROVED") Each $cal(L)_n union {0}$ is an $FF_2$-vector space, being the
  kernel of the $FF_2$-linear map $L_(f_n)$. Writing $f_n = sum_i (f_n)_i t^i$ of
  degree $delta$, the locus is cut out in $b$ by
  $L_(f_n)(b) = sum_i (f_n)_i b^(2^i) = 0$, and in the nonzero $j$-coordinate
  $j = 1 \/ b$ by
  $
    sum_i (f_n)_i j^(2^delta - 2^i) = 0 .
  $
  Both loci are Frobenius-stable. Explicitly:
  $
    n = 4: quad b^8 + b^4 + b^2 + b = 0, quad j^7 + j^6 + j^4 + 1 = 0 ,
  $
  $
    n = 6: quad b^16 + b^8 + b^2 + b = 0, quad j^15 + j^14 + j^8 + 1 = 0 ,
  $
  $
    n = 8: quad b^32 + b^16 + b^2 + b = 0, quad j^31 + j^30 + j^16 + 1 = 0 .
  $
]

#proof[
  Kernels of $FF_2$-linear maps are $FF_2$-subspaces, giving the first claim and
  the $b$-equation directly from the definition of $L_(f_n)$. For the
  $j$-equation, substitute $b = j^(-1)$ into $L_(f_n)(b) = sum_i (f_n)_i j^(-2^i) = 0$
  and multiply by the nonzero quantity $j^(2^delta)$, which is legitimate for
  $j eq.not 0$; each term becomes $(f_n)_i j^(2^delta - 2^i)$ and every step is
  reversible, so the two equations have the same nonzero solution set. Frobenius
  stability of the $b$-locus is $L_(f_n)(b)^2 = L_(f_n)(b^2)$, valid because the
  coefficients are in $FF_2$ and squaring is additive; stability of the $j$-locus
  follows because squaring commutes with inversion on $K^times$. Substituting the
  three annihilators $f_n$ from Proposition 6 and their degrees $delta = 3, 4, 5$
  produces the displayed equations.
]

One negative structural fact is worth recording, because it shows the $j$-locus is
genuinely a curve-theoretic object rather than an additive shadow of the
$b$-locus.

#tag("EMPIRICAL", detail: "exhaustive, n in {4,6,8}") After adjoining $0$, the
$b$-locus is an additive subgroup (it is a kernel), but *none* of the three
$j$-loci is: exhaustive testing finds pairs $j_1, j_2$ in the locus with
$j_1 + j_2$ outside it. Inversion does not respect addition, so the $FF_2$-linear
structure present in the $b$-coordinate does not survive the passage to $j$.

#ref(<fig:cum>) shows the same thinning as a cumulative distribution: the fraction
of parameters with genus at most a threshold, per degree, with the $B_n$ slices
marked. The low-genus densities $7\/15 approx 0.47$, $5\/21 approx 0.24$,
$31\/255 approx 0.12$ fall with degree, consistent with low genus becoming rarer
as the field grows.

#fig("/figures/P1.4/cumulative.svg", width: 74%, caption: [
  #tag("EMPIRICAL", detail: "all 333 nonzero b") Cumulative fraction of nonzero
  $b in FF_(2^n)$ with GHS genus at most a threshold, per degree, against
  $log_2 g$. Dotted verticals mark the experimental slice $B_n = 2^(n\/2)$; the
  annotated fractions are the exact low-genus densities $7\/15$, $5\/21$,
  $31\/255$. Source: `ghs_genus_distribution_n4-6-8_20260623.csv`.
]) <fig:cum>

= What the census does not show: genus is not a speedup

We now state the obstruction plainly, because it is the honest core of the
result and it dictates what remains open. Everything above is an exact
classification of a genus *invariant*. It is not a classification of vulnerable
curves, and it cannot be, for three concrete reasons drawn directly from the
research record.

#tag("PROVED") *The census carries no discrete-log cost.* A GHS speedup exists
only if index calculus on the descended genus-$g$ Jacobian over $FF_q$ is cheaper
than a generic square-root search on the relevant prime-order subgroup of
$E(FF_(q^n))$. That comparison needs three numbers the census does not contain:
the order of the target subgroup on $E$, the order of the descended Jacobian, and
a measured (or rigorously bounded) index-calculus cost. Low genus is *necessary*
for the Jacobian side to be cheap, but it is not *sufficient*: a low-genus
Jacobian whose relevant subgroup is small, or whose order does not receive the
source logarithm, yields no advantage. The data here contains neither
elliptic-curve subgroup orders nor Jacobian-DLP timings, so no row of it
demonstrates a speedup over Pollard $rho$.

#tag("CITED") *Feasibility requires more than genus.* Maurer, Menezes, and Teske
compare GHS against generic attacks only after imposing subgroup-size and
hyperelliptic-DLP feasibility conditions; in their analysis genus alone is
insufficient to conclude an attack is faster @mmt2002. The relevant subexponential
Jacobian algorithms — Gaudry's index calculus and the $L(1\/3)$ low-degree-curve
algorithm — apply only in genus and field-size regimes that our small-degree
census does not reach @gaudry2009 @engegaudrythome2011. The census is therefore
best read as the *input* to such a feasibility analysis, not its conclusion.

#tag("PROVED") *No cover was constructed.* The invariant computation stops at the
genus. It never builds the fixed field of the Artin–Schreier compositum, the
descended curve $C$, the cover map $C -> E$, or the point-to-divisor map. These
are exactly the objects an end-to-end attack needs, and their construction — in
pure Python, without SageMath or Magma — is the missing piece. The repository
records this as an explicit gap.

These are the two open questions the slice leaves, stated as the research log
states them.

#keybox(title: "Open (recorded as P1.4/Q002 and P1.4/Q003)")[
  *(Q002) Explicit construction.* #tag("CONJECTURE") Build the descended function
  field, curve, and divisor map for the classical binary GHS descent in pure
  arithmetic, starting with a genus-$2$ or genus-$3$ case, without a
  computer-algebra backend. The present work supplies the genus but not the
  geometry.

  *(Q003) When does low genus become a speedup?* #tag("CONJECTURE") Instrument an
  end-to-end toy descent with elliptic subgroup orders, an explicit Jacobian, and
  a measured discrete logarithm, and compare directly against Pollard $rho$ on the
  same subgroup. Only such a comparison can turn a low-genus census row into
  evidence of vulnerability.
]

The tool constraint that forced the invariant-only slice was concrete:
SageMath, Singular, and `msolve` were unavailable in the working environment, so
the descent was reduced to what direct $FF_2$-polynomial arithmetic can compute
exactly. That reduction succeeds completely for the genus invariant and does not
touch the geometry; the honest position is that the linear-algebra sub-goal is
closed and the construction sub-goal is not.

= Conclusion

We set out to classify, exactly and reproducibly, the classical characteristic-two
GHS genus for the ordinary binary model at small extension degree. We recomputed
the GHS magic number as the $FF_2$-dimension of the pair span of the Frobenius
conjugates of $sqrt(b)$, derived the genus from Hess's exact formula
$g = 2^(m-1) - 2^(m-r) + 1$ as a pure $FF_2$-linear invariant of one Frobenius
orbit (§3–§4), reproduced the published $FF_(2^155)$ genus-$31$ example on the
lower branch (§5), and gave the complete Frobenius-checked genus census for
$n in {4, 6, 8}$ — all $333$ parameters, two-branched, heavy-tailed, with the
lower branch first appearing at $n = 6$ (§6). We described the low-genus locus
${b : g(b) <= 2^(n\/2)}$ exactly as a single linearized-polynomial kernel, with
proved closed-form $b$- and $j$-equations and Frobenius stability, and noted that
its additive structure is genuinely lost under $b |-> 1\/b$ (§7).

The scope is exactly what the mathematics supports and no more. This is a
classification of a genus invariant, obtained without any function-field
machinery; it is *not* a classification of attackable curves, because it contains
no subgroup orders, no explicit cover, and no measured discrete logarithm, and
because low genus is necessary but not sufficient for a GHS speedup (§8). The two
open questions — an explicit pure-arithmetic cover construction, and an
end-to-end toy speedup comparison against Pollard $rho$ — are recorded as such
rather than papered over. Within its declared boundary the slice is complete,
exact, and independently checkable; outside it, the interesting problem is still
open.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
All numbers above come from the repository's validated pure-Python
implementation. Polynomial-basis $FF_(2^N)$ arithmetic, Frobenius spans,
annihilators, the magic number, and the exact genus branch are in `ghs.py`
(`gf2_basis`, `gf2_in_span`, `frobenius_orbit`, `frobenius_annihilator`,
`ghs_profile`); the published genus-$31$ regression is
`verify_published_example.py`; the exhaustive census, Frobenius-invariance
checks, distribution, and low-genus locus are `sweep_ghs_genus.py`, which writes
the three source CSVs named in the captions
(`sweep_ghs_genus_n4-6-8_20260623.csv`,
`ghs_genus_distribution_n4-6-8_20260623.csv`,
`ghs_low_genus_locus_n4-6-8_20260623.csv`). The census sweeps every nonzero
$b in FF_(2^n)$ for $n in {4, 6, 8}$ with $a = 0$ (so GHS regularity holds), and
recomputes each profile at $sigma(b) = b^2$ as an invariance check; all $333$
rows pass. The three figures are regenerated from those CSVs by
`figures/P1.4/make.py`. Every mathematical claim above carries one of the tags
#tag("PROVED"), #tag("CITED"), #tag("EMPIRICAL", detail: "range"), or
#tag("CONJECTURE") exactly as the research log records it; untagged sentences are
exposition, not claims. No cryptographic-scale parameters were attacked and no
curve in the census is claimed to be broken.
]

#bibliography("refs/P1.4.bib", title: [References], style: "ieee")
