#import "lib/paper.typ": *

#show: paper.with(
  title: "Unified Transfers: Restricted Classification, Quadratic Class-Target Factorization, and Uniform Ring-Class Torsion",
  subtitle: "Why every prime-order imaginary-quadratic Picard image exposes a finite or local residue character",
  pid: "P1.5",
  keywords: ("ECDLP", "transfer maps", "anomalous curves", "MOV/Frey–Rück", "Weil descent", "class groups", "Kummer pairing", "generic group model", "algebraic groups"),
  abstract: [
    The two textbook attacks that break special elliptic curves — the anomalous
    additive reduction of Semaev, Satoh–Araki and Smart, and the
    MOV/Frey–Rück pairing reduction — are both instances of one operation:
    evaluate a nonzero character of a prime-order cyclic source group into a
    group whose discrete logarithm is easy. We formalise this as a *transfer
    package*, an injective homomorphism $phi_I : ⟨ P ⟩ -> G_I$ with polynomial
    setup and evaluation cost and a subexponential target DLP, settle the status
    of Weil descent inside it (it counts, as a known third geometric family),
    and ask the problem's question: does a *structurally different* fourth
    transfer exist, or can one be ruled out in a stated class? We give a
    restricted classification and give an explicit pairing-derived
    ordinary-class control construction. We prove
    (i) an algebraic-group rigidity theorem: every global homomorphism
    $E -> H$ into an affine group is trivial and every nontrivial one has
    elliptic image isogenous to $E$; (ii) a generic-source impossibility
    theorem: any transfer using only a random source-group oracle would, via
    Shoup's $O(m^2 \/ r)$ bound, solve the generic DLP in $r^(o(1))$ queries;
    (iii) rational-evaluator lower bounds — an affine subgroup homomorphism of
    common pole degree $D$ forces $D >= r \/ 2$, a $B$-branch piecewise map
    forces $max(1,D) B^2 >= r \/ 4$, and the decision-tree depth obeys
    $d + 2 b >= log_2 r - O(log log r)$; and (iv) a base classification sending
    finite/local and function-field class targets back to trivial or Jacobian
    ones. An evaluator-sandwich argument makes point-to-class evaluation
    polynomial-time equivalent to the source DLP given a target oracle, so
    class-number size arguments alone cannot close the problem. We first give
    a pairing-derived ordinary ring-class control. We then prove the stronger
    target theorem. Every exact order-$r$ element of an explicit
    imaginary-quadratic Picard group is exposed either by the effective
    conductor residue quotient or by a maximal Kummer character. In the
    latter branch, $frak(a)^r=(alpha)$ defines a canonical virtual unit and a
    suitable split $q equiv 1 mod r$ gives
    $[frak(a)] |-> alpha^((q-1)/r) mod frak(q) in mu_r(FF_q)$.
    Compact relative-generator tracking makes evaluation polynomial without
    expanding $alpha$; under the standing ERH/GRH convention, effective
    Chebotarev finds a short separator in expected polynomial time. Hence
    every ordinary quadratic class evaluator, including arbitrary direct-form
    synthesis, post-composes to a finite/local residue character. The class
    presentation is not an independent fourth mechanism. This is a
    factorization theorem, not a proof that the source evaluator cannot exist
    or that its residue character is pairing-derived. Finally, the separate
    prescribed-order target problem has an unconditional deterministic
    solution: for every odd prime $r$, the reduced form
    $[r^2,2r,r^2+1]$ has exact order $r$ in the order of discriminant
    $-4r^4$. Its encoding has $Theta(log r)$ bits and its subgroup logarithm
    is the exposed wild conductor coordinate.
  ],
)

= Introduction

Most of elliptic-curve cryptography rests on a single empirical fact: for a
well-chosen curve $E \/ FF_q$ and a point $P$ of large prime order $r$, the best
known algorithm for the discrete logarithm problem (ECDLP) in $⟨ P ⟩$ is a
generic square-root method costing $Theta(sqrt(r))$ group operations. The
qualifier *well-chosen* is doing real work. A handful of curve families are
catastrophically weaker, and in each case the break has the same shape: one
constructs an efficiently computable, injective group homomorphism from
$⟨ P ⟩$ into some other group where the discrete logarithm is
subexponential or polynomial, evaluates it on the challenge, and finishes in the
easy target. Two such *transfers* are classical. Anomalous curves over prime
fields, where $hash E(FF_p) = p$, admit the additive reduction of Semaev
@semaev1998, Satoh–Araki @satoharaki and Smart @smart1999, which maps
$⟨ P ⟩$ to $(FF_p, +)$ in linear time. Curves with small embedding degree
$k$ admit the MOV @mov and Frey–Rück @freyruck pairing reduction, which maps
$⟨ P ⟩$ into $mu_r subset FF_(q^k)^times$ and finishes with index calculus in
the finite field.

The problem posed as P1.5 asks whether these are the only mechanisms, or merely
the only *known* ones. Concretely: *classify the curves for which there is a
polynomial-time computable injective homomorphism from $⟨ P ⟩$ to a group with
a subexponential discrete logarithm algorithm.* This is a question about the
existence of transfers, and it is genuinely open in full generality. What we can
do — and what this paper does — is give a precise operational definition,
identify the common structure of the two known cases, prove that entire natural
classes of would-be transfers cannot exist, and identify the exact ordinary
class-group object that had remained. We first construct a pairing-derived
control by composing the known degree-two pairing with a conductor exact
sequence. We then prove that every prime-order subgroup of every explicit
imaginary-quadratic Picard target has a removable finite/local residue
character. We finally solve the separate uniform prescribed-order target
problem by an explicit wild ring-class family. The deliverable is a
*restricted classification*, an evaluator-independent quadratic class-target
factorization, and a succinct exact-order target constructor.

#keybox(title: "Main finding")[
  The anomalous and pairing transfers are two instances of one construction: a
  nonzero character of a prime-order source into an easy target, made injective
  automatically by the prime-order kernel argument. Weil descent is a known
  third *geometric* family under any honest definition. We prove that no
  structurally new transfer can be *generic* in the source (it would break
  Shoup's bound), *rational of low degree* into an affine target
  ($D >= r \/ 2$, and $max(1,D) B^2 >= r \/ 4$ with branching), or *rational
  into a proper or mixed target* (its image is forced to be elliptic and
  isogenous to $E$). The ordinary-class residual nevertheless has a positive
  realization: on a succinct trace-zero $j=1728$ family, pair into
  $mu_r subset FF_(p^2)^times$ and apply the conductor quotient to
  $op("Pic")(ZZ+p ZZ[i])$. The resulting fixed-discriminant reduced-form map is
  injective and has a subexponential target DLP, but it factors through and back
  to the known pairing target. More generally, the conductor/maximal dichotomy
  exposes every order-$r$ quadratic Picard image in a local conductor factor or
  a split-prime Kummer power residue. Algebraic separation is unconditional;
  uniform short-prime setup uses the same ERH/GRH convention as the rigorous
  class-group target route. Separately, no hypothesis or auxiliary prime is
  needed to construct an exact-order target: in
  $op("Pic")(ZZ+r^2 ZZ[i])$, the reduced form
  $[r^2,2r,r^2+1]$ has exact order $r$ and discriminant $-4r^4$. This closes
  the target-only SG-30 problem but supplies no source evaluator.
]

== Contributions and honest scope

We contribute (i) the transfer-package definition and its boundary examples,
with an explicit decision about Weil descent (§3); (ii) a common character
framework for the two elementary transfers, anchored in Belding's dual-number
pairing @belding2007 (§3.2); (iii) a candidate-target taxonomy with a reason for
every verdict (§4, #ref(<fig:tax>)); (iv) the algebraic-group rigidity theorem
(§5); (v) the generic-source impossibility theorem (§6); (vi) rational-evaluator
degree, branch and depth lower bounds, adversarially audited (§7); (vii) the
CM/ray class-group obstructions with explicit class-number bounds (§8); (viii)
  the evaluator sandwich and discriminant-window analysis (§9); (ix) an explicit
  pairing-to-ring-class transfer, with fixed-discriminant form encoding and a
  target-DLP conversion (§9.4); (x) the conductor/maximal Kummer factorization
  for every explicit imaginary-quadratic target (§11); (xi) an unconditional
  uniform exact-order ring-class target of discriminant $-4r^4$ (§11.1); and
  (xii) end-to-end toy
  validation of the known transfers, the ring-class realization, the maximal
  Kummer character, the exact-order constructor, and the negative probes (§10,
  #ref(<fig:scaling>), #ref(<fig:buell>), #ref(<fig:window>)).

We state the scope plainly. This is *not* a solution of the unrestricted
classification over arbitrary target categories. The rational negative
classification is complete only within
the models it names — global algebraic-group homomorphisms, generic source
oracles, rational decision-tree evaluators into affine/proper/mixed targets,
and the standard class-target bases. Outside those models, arbitrary
high-degree or non-rational evaluators remain unclassified in general. For
explicit imaginary-quadratic ordinary-class targets, however, the later
factorization is independent of the evaluator model and closes novelty-grade
Q004 under the stated ERH/GRH convention. The target interface publicly
supplies its maximal discriminant, conductor, and conductor factorization.

= Setting and notation

Fix a finite field $FF_q$ of characteristic $p$ and an elliptic curve
$E \/ FF_q$ with identity $O$. Let $P in E(FF_q)$ have prime order $r$ and write
$C = ⟨ P ⟩$ for the cyclic source group. An instance is a tuple
$I = (q, E, P, r)$ drawn from an infinite family; we set
$n = ceil(log_2 r)$ and let $L$ denote the full encoded input length, requiring
$L = n^(O(1))$ so that "polynomial time" always means polynomial in $n$. For an
imaginary-quadratic order of discriminant $Delta$ we write $h(Delta)$ for its
class number and $B = log_2 abs(Delta)$ for its discriminant bit length. We use
$mod$ for reduction, $⟨ dot ⟩$ for the subgroup generated, and reserve $phi$
for a transfer evaluator. The single standing fact we lean on repeatedly:

#lemma(name: [prime-order kernel])[
  #tag("PROVED") Any nonzero group homomorphism out of a group of prime order is
  injective, because its kernel is a proper subgroup of a group of prime order
  and hence trivial.
]

This is why every transfer question reduces to *nonzero character* plus *easy
target*: injectivity is free once the character is nonzero and the source has
prime order.

= The unified transfer framework

We first make "transfer" precise, so that inclusion and exclusion are decidable
rather than rhetorical.

== The transfer package

#definition(name: "transfer package")[
  For an infinite family of instances $I = (q, E, P, r)$ with $n = ceil(log_2 r)$
  and encoded input length $L = n^(O(1))$, a *transfer package* consists of a
  uniformly and effectively presented finite group $G_I$, setup data of size
  polynomial in $L$, and a uniform evaluator
  $
    phi_I : ⟨ P ⟩ --> G_I
  $
  such that: (1) the encoding length and group-operation cost in $G_I$ are
  polynomial in $L$; (2) $phi_I (Q)$ is computable from the ordinary
  representation of $Q in ⟨ P ⟩$ in expected polynomial time in $L$; (3) $phi_I$
  is a group homomorphism, injective on $⟨ P ⟩$; and (4) given $phi_I (P)$ and
  $phi_I (Q)$, a uniform target algorithm recovers the logarithm in expected
  time $exp(o(n))$, including all precomputation attributable to the instance.
  The evaluator need not compute $phi_I^(-1)$; randomised evaluators and target
  algorithms are allowed with the same expected-cost bounds.
]

The four requirements are exactly what separates a genuine attack from a
tautology. Requirement (1)–(2) rule out the two most tempting cheats.

#remark(name: "boundary examples")[
  #tag("PROVED") A lookup table of all $r$ source points fails: its setup and
  representation cost are exponential in $n$. The abstract isomorphism
  $[m] P |-> m mod r$ is *not* a transfer unless its evaluator is supplied
  independently, because evaluating it *is* the source DLP. A constant map, the
  $x$-coordinate map, and a hash-to-group map fail injectivity, the homomorphism
  requirement, and the homomorphism requirement respectively. An efficiently
  computable isogeny to another generic elliptic curve does not qualify merely
  from being injective: requirement (4) still needs a subexponential target
  algorithm, which a generic curve does not supply.
]

== One character framework for the two elementary transfers

Both classical transfers instantiate the same three-step pattern: build an
auxiliary structure, evaluate a fixed functional that is a nonzero homomorphism
on $C$, and land in an easy target. #ref(<tab:frame>) makes the parallel
literal. Belding's construction @belding2007 of a nondegenerate Weil-pairing
analogue on $p$-torsion over the dual numbers is what turns the loose analogy
"both linearise the group" into an actual common mechanism: the anomalous
reduction is a pairing attack too, into an additive rather than multiplicative
target.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, left, left, left, left),
    table.hline(stroke: 0.7pt),
    table.header(
      [*Case*], [*Auxiliary structure*], [*Fixed functional*], [*Easy target*], [*Nondegeneracy*],
    ),
    table.hline(stroke: 0.5pt),
    [Char. $p$ ($r = p$)],
      [$p$-adic / dual-number thickening],
      [connecting / formal-log map on $p$-torsion],
      [$(FF_q, +)$ or additive quotient],
      [image of $P$ nonzero],
    [Prime-to-$p$],
      [Weil or Tate pairing on $E[r]$],
      [$T |-> e_r (T, Q)$, fixed independent $Q$],
      [$mu_r subset FF_(q^k)^times$],
      [$e_r (P, Q) eq.not 1$],
    table.hline(stroke: 0.7pt),
  ),
  caption: [The two elementary transfers as one construction (SG-04). Each fixed
  functional is a nonzero homomorphism on $C$, hence injective by the
  prime-order kernel lemma; the auxiliary structures differ but the
  nondegeneracy certificate is the same. Belding @belding2007 supplies the
  missing $p$-torsion pairing that makes the top row literally a pairing attack.],
) <tab:frame>

#tag("CITED") Semaev @semaev1998 handles all rational characteristic-$p$
torsion, not only the prime-field equation $hash E(FF_p) = p$; the additive
family is genuinely broader than the anomalous prompt suggests.
#tag("CONJECTURE") A genuinely new *elementary* transfer would need a computable
nonzero character not induced by a local connecting map, a bilinear torsion
pairing, or a geometric descent; any explicit family meeting the transfer
definition and provably outside all three refutes the negative assessment.

== The Weil-descent decision

Weil descent is not excluded by terminology; it is admitted when it meets the
definition. #tag("CITED") Gaudry–Hess–Smart @ghs construct explicit
homomorphisms from selected characteristic-two elliptic-curve groups into
Jacobians over a smaller field. #tag("PROVED") If a constructed homomorphism has
kernel order coprime to $r$, its restriction to $C$ is injective, since the
kernel meets the order-$r$ subgroup trivially; concretely, for a degree-$d$
separable cover $pi : C' -> E$ the composite $pi_* pi^* = [d]$, so pullback is
injective on $r$-torsion whenever $r divides.not d$. #tag("CONDITIONAL", detail: "EGT-2009 family/smoothness hypotheses") A descent into the low-degree
high-genus Jacobian families of Enge–Gaudry–Thomé @egt2009 has a subexponential
$L(1 \/ 3)$ target algorithm. #tag("PROVED") But merely rewriting
$E(FF_(q^n))$ as the rational points of a Weil restriction supplies *no* target
algorithm and fails requirement (4). Thus Weil descent is a known *third
geometric target family* under the definition — prior art, not a newly
discovered mechanism.

= Taxonomy of candidate targets

The problem asks for a candidate-target table with a reason for every verdict.
#ref(<fig:tax>) records ours; §5–§11 supply the proofs. The organising principle
is that a target must be able to *contain* an order-$r$ element and to *receive*
it homomorphically from the source, and that requirement (4) demands the target
DLP be genuinely easier than the source.

#fig("/figures/P1.5/taxonomy.svg", width: 82%, caption: [
  Candidate-target verdicts (SG-05/SG-06/SG-22/SG-33/SG-36). E = excluded by
  proof, K = known established mechanism, C = conditional or neutral, and R =
  residue-factorized by A028.
  Every additive/affine target is excluded away from $r = p$ by exponent or
  algebraic-group rigidity; every natural CM/ray class construction is excluded
  by orientation loss, size, or transparency; covers and descent are the known
  geometric family. Every explicit ordinary imaginary-quadratic target has a
  finite/local post-character, whether its source evaluator is pairing-derived
  or not.
]) <fig:tax>

#tag("PROVED") *Local formal groups and additive char-$p$ rings.* If $r$ is a
unit in the coefficient ring, the formal multiplication series
$[r](T) = r T + O(T^2)$ is invertible, so there is no nonzero formal
$r$-torsion; the underlying additive group of a characteristic-$p$ ring is
killed by $p$ and has no order-$r$ element for $r eq.not p$. The case $r = p$ is
the additive/local family of #ref(<tab:frame>), not a new target.
#tag("CITED") *Drinfeld modules* have underlying group $GG_a$ @poonen2021, so
their finite additive points have exponent $p$; excluded for $r eq.not p$.
#tag("PROVED") *Tori* are affine, so every global algebraic map $E -> T$ is
trivial (§5); the only maps that survive live on $E[r]$ and are the established
pairing route. *Jacobians of covers and Weil restrictions* are the geometric
branch (§3.3). The subtle rows — the endomorphism-order class group, ray class
groups, and a separately constructed number-field class group — are treated in
§8–§9.

= Algebraic-group rigidity

The first structural theorem explains why every *global* attempt to map $E$ into
an affine target dies, and why every nontrivial global map stays on the elliptic
side.

#theorem(name: "algebraic-group classification")[
  #tag("PROVED") Let $k$ be a finite field, $E \/ k$ an elliptic curve, $H \/ k$
  a smooth finite-type algebraic group, and $f : E -> H$ an algebraic-group
  homomorphism. The reduced image of $f$ is either trivial or an elliptic
  abelian subvariety of $H$; in the latter case $f : E -> f(E)$ is an isogeny.
  In particular, if $H$ is affine then $f$ is trivial.
]

#proof[
  $E$ is proper and connected, so $f(E)$ is a proper connected closed subgroup
  of $H$. #tag("CITED") A complete connected group variety is an abelian
  variety, and a complete algebraic group is anti-affine @milne2022. The image
  has dimension at most one: if zero, connectedness makes it the identity; if
  one, it is an elliptic curve. In the nonconstant case the kernel is
  zero-dimensional and finite, so $E$ surjects isogenously onto its elliptic
  image. If $H$ is affine, the image is both proper connected and affine, so
  every coordinate function pulls back to a global regular function on the
  complete curve $E$, hence to a constant, and $f$ is trivial.
]

#remark(name: "why this does not close the problem")[
  #tag("PROVED") The theorem classifies *global morphisms* $E -> H$, but a
  transfer evaluator need only be defined on the finite set $C = ⟨ P ⟩$ and need
  not extend to a morphism on $E$. MOV evades it because fixing the second
  pairing argument gives a character only on $E[r]$, not a global map
  $E -> GG_m$. The anomalous transfer evades it because it uses a lift or
  infinitesimal thickening and a connecting map, not a global map
  $E \/ FF_p -> GG_a$. The theorem is a rigidity backdrop; the real content is
  how far a *subgroup-only* evaluator can escape it.
]

= Generic-source impossibility

If a would-be transfer touches the source only through the abstract group
operations — no coordinates, no lift, no pairing — then it cannot exist. This is
the black-box floor.

#theorem(name: "generic-source impossibility")[
  #tag("PROVED") Fix a uniformly random injective encoding
  $sigma : ZZ \/ r ZZ -> S$ and give the algorithm handles $sigma(1), sigma(x)$
  with only the generic addition, inversion, identity and equality oracles on
  the source. No infinite family of transfer packages whose setup and evaluation
  make $r^(o(1))$ expected source-oracle calls can have both an injective
  homomorphic evaluator and an $exp(o(log r))$ target DLP algorithm.
]

#proof[
  Give the alleged package the generic DLP challenge $(sigma(1), sigma(x))$. Run
  its counted setup and compute $h = phi(sigma(1))$ and $y = phi(sigma(x))$.
  Because $phi$ is a homomorphism, $y = x h$; because the source has prime order
  and $phi$ is injective, $h$ has order $r$, so the promised target algorithm on
  $(h, y)$ returns $x$. Let $q(r) = r^(o(1))$ bound the composition's expected
  source-oracle calls and truncate after $4 q(r) \/ delta$ calls; by Markov's
  inequality the truncated generic DLP algorithm still succeeds with probability
  at least $3 delta \/ 4$, with deterministic query cap $m = r^(o(1))$.
  #tag("CITED") Shoup's random-encoding bound @shoup gives success
  $O(m^2 \/ r) = r^(-1 + o(1))$, which tends to zero — a contradiction. Target
  representation, group operations and precomputation are harmless: after
  composition they are arbitrary local computation by the generic source
  algorithm.
]

The theorem draws the exact boundary. #tag("CITED") The anomalous transfer
crosses it through coordinates and a $p$-adic or dual-number lift; MOV/Frey–Rück
crosses it through line functions, an auxiliary torsion point and extension-field
arithmetic; Weil descent crosses it through equations, Frobenius, a field basis
and divisor maps. #tag("PROVED") Hence *every* qualifying transfer must exploit a
representation-specific source operation — generic ideal, class, ray or level
arithmetic on the target side cannot by itself evade the bound. A surviving
point-to-class candidate must expose the concrete source operation that extracts
scalar-sensitive information; this is a complete black-box classification, not an
unrestricted one.

= Rational-evaluator lower bounds

The next escape is a coordinate formula: a rational map on $E$, homomorphic only
on $C$, computed from ordinary point coordinates. We measure such a map by its
geometric degree and prove it must be either exponentially high-degree,
exponentially branched, or linear-depth. Throughout, fix a faithful closed
immersion $rho : H arrow.hook op("GL")_s$ of the affine target and define the *common
pole degree* $D = delta_rho (F)$ of a rational $F : E arrow.squiggly H$ as the
degree of the least effective divisor $cal(P)(F)$ on $E_(overline(k))$ for which
every matrix entry of $rho F$ lies in $L(cal(P)(F))$. The base change to
$overline(k)$ is essential: all zero counts happen on the geometric curve.

#theorem(name: "affine rational rigidity")[
  #tag("PROVED") Let $H \/ k$ be affine and $F : E arrow.squiggly H$ be defined
  at every point of $C$ with $F|_C$ a homomorphism, and put $D = delta_rho (F)$.
  If $r > 2 D$ then $F$ is the constant identity. Hence every nontrivial, and so
  every injective, rational affine transfer satisfies $D >= r \/ 2$.
]

#proof[
  Put $M = rho(F(P))$. For each entry,
  $g_(i j)(X) = f_(i j)(X + P) - sum_ell f_(i ell)(X) M_(ell j)$ has pole degree
  at most $2 D$ (a translate of $cal(P)(F)$ plus $cal(P)(F)$) and vanishes at all
  $r$ points of $C$ by the subgroup law. Since $r > 2 D$, a nonzero function
  cannot have more zeros than its pole degree, so $g_(i j) equiv 0$ and
  $rho(F(X + P)) = rho(F(X)) M$ identically. Right multiplication by the
  invertible constant $M$ preserves, at each geometric point, the largest pole
  order among the entries, so $cal(P)(F)$ is invariant under translation by $P$.
  Every translation orbit has $r$ points while $deg cal(P)(F) = D < r$, forcing
  $cal(P)(F) = 0$. All entries of $rho F$ are then global regular functions on
  the proper connected curve $E$, hence constants; $F(0) = 1$ makes the constant
  the identity.
]

Branching does not rescue the construction, and the improvement over the
naive bound is real: the adversarial-partition argument gives a quadratic, not
cubic, branch penalty.

#theorem(name: "piecewise overlap obstruction")[
  #tag("PROVED") Let $phi : C -> H(k)$ be an injective homomorphism agreeing on
  each of $B$ nonempty branch sets with a rational map of common pole degree at
  most $D$, and put $m = ceil(r \/ B)$ and $D_+ = max(1, D)$. Then
  $
    m (m - 1) <= 2 D (r - 1), quad "hence" quad D_+ B^2 >= r \/ 4 .
  $
]

#proof[
  Take a largest branch $S$, $abs(S) = eta >= m$, with rational map $F$. For
  $t in C$ set $R(t) = abs({x in S : x + t in S})$; counting ordered pairs of
  $S$ by difference gives $sum_(t eq.not 0) R(t) = eta(eta - 1)$. If some
  $R(t) > 2 D$, then at more than $2 D$ points both $x, x + t in S$, so
  $F(x + t) = phi(t) F(X)$; the entrywise defect
  $rho(F(X + t)) - rho(phi(t)) rho(F(X))$ has pole degree at most $2 D$ and more
  than $2 D$ zeros, hence vanishes identically. As $t eq.not 0$ has order $r$,
  translation invariance forces $cal(P)(F) = 0$, $F$ constant, and
  $rho(phi(t)) = I$, contradicting injectivity. Thus every
  $R(t) <= 2 D$, so $eta(eta - 1) <= 2 D (r - 1)$; monotonicity in $eta >= m$
  and a short case split on $r$ versus $2 B$ give $D_+ B^2 >= r \/ 4$.
]

#corollary(name: [decision-tree depth])[
  #tag("PROVED") In the rational decision-tree model — base functions of pole
  degree $<= D_0$, binary $+, -, times, \/$ gates, at most $b$ binary decisions
  per path ($B <= 2^b$ transcripts), arithmetic depth $<= d$, and $M$ output
  entries — pole growth gives $D <= M 2^d D_0$, so an injective affine transfer
  obeys $d + 2 b >= log_2 r - log_2 (4 M D_0)$. For $M D_0 = (log r)^(O(1))$ this
  reads $d + 2 b >= n - O(log n)$; with no branching, $d >= log_2 r - log_2(2 M D_0)$.
]

#tag("CITED") These are depth lower bounds in a restricted algebraic model, not
superpolynomial-time bounds: depth $Theta(n)$ with polynomial size is compatible
with them, and Miller's pairing program is exactly that case — a linear-length
straight-line program representing a function of expanded degree $Theta(r)$
@miller2024. #tag("CITED") The bound also refuses to exclude MOV: a Miller
function has divisor of size $Theta(r)$, so its pole degree already exceeds the
$r \/ 2$ threshold, and its polynomial-time evaluation lives entirely in the
short-program exit. Proper and mixed targets are equally rigid.

#theorem(name: "proper and mixed targets")[
  #tag("PROVED") (i) A rational $F : E arrow.squiggly H$ into a smooth proper
  algebraic group with $F(0) = 1_H$ extends to a global homomorphism
  $E -> H^0$, with trivial or elliptic-isogenous image. (ii) Fewer than $r$
  rational branches into such an $H$ collapse to one global homomorphism on $C$,
  even for disconnected or noncommutative $H$. (iii) For a single rational map
  into a smooth algebraic group with Chevalley sequence
  $1 -> L -> H^0 -> A -> 1$, the proper projection is global; if the affine
  cocycle $c(X, Y) = F(X + Y)(F(X) F(Y))^(-1)$ has fibrewise pole degree $D < r$
  in each controlled fibre, then $F$ is global with trivial or
  elliptic-isogenous image.
]

#proof[
  #tag("CITED") A rational map from the normal curve $E$ to a proper variety
  extends uniquely to a morphism @stacks; its image lies in the identity
  component $H^0$, an abelian variety over the perfect field $k$
  @milne2022, and a zero-preserving morphism of abelian varieties is a
  homomorphism by rigidity @milneav; §5 then classifies the image. For (ii),
  some branch has distinct $X, Y$; setting $t = F(0)$ and
  $alpha(Z) = t^(-1) F(Z)$ gives a pointed morphism, and
  $beta = "Int"(t) compose alpha$ is a global homomorphism agreeing with $phi$ on
  the generator $X - Y$, hence on all of $C$. For (iii), the projection
  $pi F$ is global by (i), so $c$ is $L$-valued and vanishes on $C^2$; each
  entry of $rho(c) - I$ has the $r$ points of $C$ as zeros and pole degree
  $D < r$ in each fibre, so it vanishes, $F$ is a rational homomorphism, and the
  translation trick removes its poles with Galois descent to $k$ @conrad2002.
]

The adversarial audit behind these statements — constant maps, translations,
disconnected and noncommutative targets, non-faithful representations,
exceptional characteristic, and adversarial partitions — is recorded in full in
the repository's rational-transfer review; the closest prior art is
interpolation and zero-estimate theory on commutative algebraic groups
@fischlernakamaye2014, which does not state the prime-subgroup defect bound, the
$B^2$ tradeoff, or the proper-branch collapse.

= The CM and ray class-group obstructions

The most natural place to look for a fourth transfer is a class group, where an
order-$r$ element is plausible and the Hafner–McCurley relation method
@hafnermccurley gives a subexponential target DLP. Every *natural* class
construction nonetheless fails, for three distinct reasons.

== Orientation loss

#lemma(name: "orientation loss")[
  #tag("PROVED") If $P$ has prime order $r$, then for every $1 <= m < r$ one has
  $⟨ m P ⟩ = ⟨ P ⟩$ and, for any endomorphism subring $R$,
  $"Ann"_R (m P) = "Ann"_R (P)$, because multiplication by $m$ is an
  automorphism of the order-$r$ subgroup. Hence any label determined only by the
  annihilator, the cyclic kernel, or the kernel-isogeny quotient is constant on
  the nonzero source points and cannot be an injective homomorphism for odd $r$.
]

#tag("EMPIRICAL", detail: "8 ordinary j=1728 curves, 13<=p<=421, 368 points")
Complete enumeration on ordinary $j = 1728$ curves found exactly one CM
eigenvalue, annihilator label, cyclic kernel and canonical Vélu quotient per
subgroup, matching the lemma
(`probe_cm_class_targets_full_20260702.csv`). #tag("CITED") The standard CM
construction runs the *other* way — an ideal $frak(a)$ defines a kernel
$E[frak(a)]$ and an oriented quotient @chvw2022 — so it is not a
point-to-ideal character.

== The endomorphism class group is too small

Even ignoring orientation, the curve's own endomorphism class group cannot hold
a large-prime image, by an explicit analytic bound.

#proposition(name: [class-number bound])[
  #tag("PROVED") Every imaginary-quadratic order of discriminant $Delta$
  satisfies $h(Delta) <= (3 \/ pi) sqrt(abs(Delta)) (log abs(Delta) + 2)^2$.
  Consequently the endomorphism order of an ordinary $E \/ FF_q$, whose
  discriminant divides the Frobenius discriminant $t^2 - 4 q$, has
  $h(op("End") E) <= (6 \/ pi) sqrt(q)(log(4 q) + 2)^2$, which is below $q \/ 2$
  for every $q >= 2^21$. Thus it cannot contain an order-$r$ image when
  $r >= q \/ 2$.
]

#proof[
  #tag("CITED") The ring class-number formula @cox2013 writes $h(f^2 d_K)$ as
  $h(d_K) f$ times local factors over a unit index, and the imaginary-quadratic
  analytic formula @milnecft gives $h(d_K) = w_K sqrt(abs(d_K)) L(1, chi_(d_K)) \/ (2 pi)$.
  #tag("PROVED") Splitting the $L$-series into blocks of length $abs(d_K)$ and
  using $sum_(a) chi(a) = 0$ per block gives $abs(L(1, chi)) <= log abs(d_K) + 2$;
  with $w_K <= 6$ and $product_(ell divides f)(1 + 1 \/ ell) <= log f + 1$ the
  order bound follows. Substituting $abs(Delta_(op("End") E)) <= 4 q$ and
  checking the ratio to $q \/ 2$ decreases past $q = 2^21$ gives the threshold.
]

#tag("PROVED") This does not exclude a *separately constructed* order of much
larger discriminant, nor the regime $r << q$ — which is precisely why the
residual survives.

== Ray classes and their transparency

#tag("PROVED") For $K = QQ(i)$ and odd $r$, Milne's ray-class formula @milnecft
gives $abs(op("Cl")_r (QQ(i))) = (r - 1)^2 \/ 4$ if $r equiv 1 mod 4$ and
$(r^2 - 1) \/ 4$ if $r equiv 3 mod 4$, so $r$ does not divide the modulus-$r$
ray class number. #tag("PROVED") At modulus $r^2$ the $r$-adic valuation is $2$,
and the congruence subgroup linearises:
$
  (1 + r ZZ[i]) \/ (1 + r^2 ZZ[i]) tilde.equiv (ZZ[i] \/ r ZZ[i], +), quad
  1 + r z |-> z ,
$
because $(1 + r x)(1 + r y) equiv 1 + r(x + y) mod r^2$. #tag("PROVED") This
yields an order-$r$ target with an immediate logarithm — but $[m] P |-> 1 + r m$
is only an abstract homomorphism, since evaluating it from $[m] P$ is the source
DLP. The principal units move *lifts* inside one fibre of multiplication-by-$r$,
not the $r$ source points, and full level rescaling reaches the multiples $m P$
through $(ZZ \/ r ZZ)^times$, a multiplicative action of order $r - 1$ that omits
the identity and does not respect the additive source law. #ref(<fig:tax>)'s ray
cell is excluded on these grounds, sharpened in §9.

= The evaluator sandwich and the ordinary-class control

Class-group size alone does not construct an evaluator. The reason is a two-way
reduction that we make explicit; the construction later in this section supplies
the missing evaluator through pairing data rather than through size estimates.

#theorem(name: "evaluator sandwich")[
  #tag("PROVED") Let $phi : C -> G$ be a fixed nonzero homomorphism with all
  public setup supplied, $h = phi(P)$ of order $r$, so $phi(x P) = h^x$. Write
  $T_"src"$, $T_"eval"$, $T_"tgt"$ for source-DLP, evaluation, and target-DLP
  costs. Then
  $
    T_"eval" <= T_"src" + O(log r) T_G, quad
    T_"src" <= T_"eval" + T_"tgt" + (log r)^(O(1)) .
  $
  Hence, given a target-DLP oracle, evaluation and source DLP are polynomial-time
  Turing equivalent; a polynomial evaluator plus an $exp(o(log r))$ target DLP is
  exactly a subexponential source ECDLP reduction.
]

#proof[
  Source DLP recovers $x = log_P Q$ and computes $h^x$ by double-and-add, giving
  the first bound. Evaluation followed by target DLP computes $Y = phi(Q)$ and
  recovers $x = log_h Y$, giving the second. The two together are a Turing
  equivalence.
]

#tag("PROVED") The sandwich is the honest heart of the problem. It shows that
target ideal arithmetic and class-number estimates *alone* can never give an
unconditional negative answer: once a known order-$r$ target element exists, the
only remaining content is the complexity of converting a concrete source point
into the corresponding power of that element. A universal impossibility theorem
  for an arbitrary evaluator must therefore restrict its coordinate/bit/lift
interface or prove a genuinely new lower bound for the concrete source family.

== Base classification and the discriminant window

#tag("PROVED") The possible *bases* of a class target collapse cleanly. Every
finite or local base has trivial Picard group, since every invertible module
over a local ring is free of rank one and a finite ring is a product of local
ones @stacks. A pointed global function-field class group is
$op("Pic")^0(C') tilde.equiv J_(C')(FF_q)$ @milnejv, a Jacobian target already
covered by §7; a modulus produces a generalised Jacobian, a mixed target also
covered. Thus a genuinely distinct class target must be a global number-field
order. #tag("PROVED") Standard dense global lifts are excluded by Parent's
torsion bound @parent1999: a rational order-$r$ point over a degree-$d$ number
field forces $r <= 65(3 d - 1)(2 d)^6$, so $d > (r \/ 12480)^(1\/7)$ and the
lifted encoding is exponential in $n$.

Any qualifying class target must therefore satisfy a two-sided discriminant
constraint, from which the window is immediate.

#proposition(name: [discriminant window])[
  #tag("PROVED") If an imaginary-quadratic order of discriminant bit length
  $B = log_2 abs(Delta)$ contains an order-$r$ class, the class-number bound
  forces $B >= 2 n - O(log n)$ with $n = ceil(log_2 r)$.
  #tag("CONDITIONAL", detail: "ERH + factor-base decomposition") The
  Hafner–McCurley target route @hafnermccurley costs
  $exp(O(sqrt(B log B)))$, which is $exp(o(n))$ exactly when $B log B = o(n^2)$.
  Hence the checked target route requires
  $
    2 n - O(log n) <= B = o(n^2 \/ log n) .
  $
]

#tag("PROVED") The window is nonempty but strict: a target discriminant must
carry roughly twice the source bit length, yet stay below the $n^2 \/ log n$
scale or the subexponential target advantage evaporates. Polynomial bit length
alone is insufficient; the growth exponent must land in the window.

== Why the ray shortcut is not a shortcut

One might hope to substitute the transparent modulus-$r^2$ ray target for the
opaque ordinary class group. It fails for a sharp reason.

#proposition(name: [ray evaluator equivalence])[
  #tag("PROVED") For the linearisation $theta(1 + r z) = z mod r$ and any nonzero
  homomorphism $psi : C -> U_r$ with $U_r = (1 + r ZZ[i]) \/ (1 + r^2 ZZ[i])$,
  pick a nonzero coordinate $u_j$ of $u = theta(psi(P))$; on $Q = x P$ the same
  coordinate of $theta(psi(Q))$ is $x u_j$, so one evaluator call and a field
  inversion return $x$. Thus a ray evaluator and source DLP are polynomial-time
  equivalent.
]

#tag("PROVED") Because the target logarithm is transparent in the ordinary
encoding, any nonzero point evaluator into $U_r$ is *already* a polynomial-time
source-DLP algorithm; the ray target has no intermediate subexponential regime.
This is why the ray target cannot supply the required intermediate
subexponential regime. Before the construction below, the ordinary-class branch
had two logically separate tasks: *construct* a certified order-$r$ class in a
polynomial-bit order inside the window, and *evaluate* a nonzero homomorphism
from finite-field coordinates into it. The sandwich explains why solving only
the first would not have supplied the second.

== Pairing values as ordinary ring classes

#theorem(name: "pairing-to-ring-class transfer")[
  #tag("PROVED") Let $r$ be an odd prime and let $p$ be a prime satisfying
  $p equiv 3 mod 4$ and $r divides p+1$. On
  $E_p : y^2=x^3+x$ over $FF_p$, choose $P$ of order $r$ and the distortion map
  $psi(x,y)=(-x,i y)$ over $FF_(p^2)=FF_p(i)$. If
  $z(Q)=e_r(Q,psi(P))$, then
  $
    phi(Q)=kappa(z(Q)) in op("Pic")(cal(O)_p),
    quad cal(O)_p=ZZ+p ZZ[i],
  $
  is a polynomial-time injective homomorphism. For $z(Q)=a+b i$ with
  $a eq.not 0$, put $t=b a^(-1) mod p$; a canonical output is the reduced
  primitive form equivalent to
  $
    (1+t^2, 2 p t, p^2),
  $
  whose discriminant is always $-4p^2$. The $a=0$ branch is principal and
  makes the evaluator total.
]

#proof[
  #tag("CITED") The conductor exact sequence @conradconductor, specialized to
  $ZZ+p ZZ[i] subset ZZ[i]$, gives
  $
    op("Pic")(cal(O)_p)
    tilde.equiv FF_(p^2)^times/(FF_p^times ⟨ i ⟩),
    quad h(-4p^2)=(p+1)/2,
  $
  and sends a residue $alpha$ to
  $[alpha ZZ[i] inter cal(O)_p]$. #tag("PROVED") The quotient kernel has
  order $2(p-1)$, coprime to the odd prime $r divides p+1$, so it is injective
  on $mu_r$. Directly solving the contraction for $alpha=1+t i$ gives
  $[1+t^2,-p t+p i]$, which is the displayed form under the convention
  $[A,(-B+sqrt(Delta))/2]$. Miller evaluation, one field inversion, and Gauss
  reduction are polynomial in $log p$.
]

#tag("CITED") CRT and Linnik's theorem with Xylouris's exponent $5.2$
@xylouris2011 give, for every odd prime $r$, a prime in the class
$p equiv 3 mod 4$, $p equiv -1 mod r$ with $p <= C(4r)^(5.2)$. Thus the valid
instance family is infinite and $log p=O(log r)$. This is an existence and
input-succinctness statement; the uniform transfer algorithms operate on the
supplied valid tuple $(p,E_p,P,r)$.

#proposition(name: "ring-class target logarithm")[
  #tag("PROVED") Given a primitive reduced form $(A,B,C)$ of discriminant
  $-4p^2$, extend its ideal $J=[A,-B/2+p i]$ to $ZZ[i]$ and compute
  $gamma=gcd_(ZZ[i])(A,-B/2+p i)$. Then
  $
    tau([J])=(gamma mod p)^(2(p-1)) in FF_(p^2)^times
  $
  is independent of representatives. On $kappa(mu_r)$ it is exponentiation by
  $2(p-1) equiv -4 mod r$, hence injective and logarithm-preserving.
]

#proof[
  #tag("PROVED") Primitivity forces $p divides.not A$. Extension to the Euclidean
  domain $ZZ[i]$ is principal, and contraction recovers $J$. Changing the
  Gaussian generator multiplies $gamma$ by a unit, while changing the residue
  representative contributes an $FF_p^times$ factor; exponent $2(p-1)$ kills
  both. Its residue exponent is invertible modulo odd $r$. The Gaussian
  Euclidean algorithm is polynomial in $log p$.
]

#tag("CITED") The remaining finite-field logarithm is exactly the degree-two
target DLP already used by MOV/Frey--Rück; under the same NFS convention its
cost is $L_(p^2)[1/3,O(1)]=exp(o(log r))$ @schirokauer2008. Independently, the
Hafner--McCurley route is conditional on its stated ERH and factor-base
hypotheses. Since $log_2 abs(-4p^2)=Theta(log r)$, the target lies inside the
discriminant window. Thus the construction is a complete control instance.
The efficient map back to the same torus also proves why it is not
novelty-grade Q004 closure: this is an ordinary ring-class presentation of the
known pairing mechanism, not a fourth one.

= Empirical validation

Every positive claim about the two elementary transfers and their ring-class
composition is backed by an end-to-end toy run, and every negative probe by an
exhaustive enumeration. #ref(<tab:val>) collects the parameters; the scripts
recover fixed seeded logarithms and log the work actually performed.

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: (left, left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Transfer / probe*], [*Parameters*], [*What is measured*], [*Status*]),
    table.hline(stroke: 0.5pt),
    [Additive (anomalous)], [7 curves, $101 <= p <= 6421$, $r = p$],
      [$hash E = p$, 5 scalar-homomorphism checks/curve, seeded log recovered],
      [validated],
    [Pairing (MOV/Tate)], [7 subgroups, $(p, r)$ from $(43, 11)$ to $(8011, 2003)$, $k = 2$],
      [order + $k$ checks, 4 bilinearity checks/curve, seeded log recovered],
      [validated],
    [Pairing to ring class], [$(p,r)=(43,11),(211,53),(331,83)$],
      [all $(p+1)/2$ classes, injective source image, Gaussian-gcd log recovery],
      [validated],
    [Maximal Kummer character], [10 primes, $3 <= r <= 31$],
      [split separator, exact character order, every scalar log recovered],
      [validated],
    [Buell reduction], [10 reductions, $23 <= p <= 59$, $13 <= r <= 37$, 218 points],
      [distinct lifted discriminants, points hitting model $cal(D)$],
      [negative],
    [CM class labels], [8 $j = 1728$ curves, $13 <= p <= 421$, 368 points],
      [distinct CM/annihilator/kernel/Vélu labels per subgroup],
      [negative],
    [Exact-order census], [$abs(Delta) <= 200000$, primes $3 <= r <= 43$],
      [least $abs(Delta)$ with $r divides h(Delta)$, exact-order form],
      [existence only],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Validation audit. Positive rows recover a fixed known logarithm and
  confirm the homomorphism; negative rows exhaust a toy family and record the
  obstruction. Parameters and every recovered value are in the cited CSVs.],
) <tab:val>

== The two transfers scale as predicted

#tag("EMPIRICAL", detail: "Windows 11, Python 3.13.4, 50 timing repeats") The
median additive-map time fits a work exponent of $1.050508$ against lifted
group-operation count, and the affine Tate map fits $1.052569$ against
Miller-line count times field bit length, with all log-residuals stored in
`run_transfers_full_20260626_scaling.csv`. #ref(<fig:scaling>) shows the fits.
#tag("PROVED") The additive evaluator uses double-and-add for the scalar $p$ and
so $O(log p)$ lifted operations, with recorded counts rising from $10$ to $18$;
the Tate map uses an $O(log r)$ Miller loop, counts rising from $5$ to $17$.
#tag("PROVED") Critically, the toy multiplicative logarithms are solved by BSGS
of width $ceil(sqrt(r))$, not index calculus, so the timings validate the *map
and recovered answer* but do *not* establish the finite-field subexponential
asymptotic that requirement (4) invokes in principle — a limitation we mark
rather than hide.

#fig("/figures/P1.5/scaling.svg", width: 100%, caption: [
  Measured median evaluator time versus the explicit work predictor for the
  additive lift, the affine Tate map, and the toy target BSGS solver, with the
  recorded power-law fits (dashed). Fit exponents $1.0505$, $1.0526$, $0.4897$
  are read directly from the experiment driver. Source:
  `run_transfers_full_20260626_scaling.csv`.
]) <fig:scaling>

== The naive class-group formula does not even land in one group

#tag("EMPIRICAL", detail: "10 reductions, 218 nonzero points") Applying the
explicit Buell point-to-form formula to canonical integer representatives of a
finite-field point produces, on almost every point, a *different* lifted
discriminant $cal(D) + k_Q p$: complete enumeration found $218$ distinct lifted
discriminants — one per point — and only two equal to the model discriminant,
with every discrepancy divisible by $p$
(`probe_buell_reduction_full_20260710.csv`). #ref(<fig:buell>) shows this per
subgroup. #tag("PROVED") Since binary quadratic forms of different discriminants
represent classes of different orders, the outputs do not share a target group;
forcing a fixed discriminant means solving the integral curve equation exactly,
which returns to the excluded dense-lift branch.

#fig("/figures/P1.5/buell.svg", width: 80%, caption: [
  Canonical Buell reduction over ten toy prime-order subgroups: nearly every
  nonzero point yields its own lifted discriminant (blue), and almost none hit
  the fixed model discriminant (orange). The map does not land in one class
  group. Source: `probe_buell_reduction_full_20260710.csv`.
]) <fig:buell>

== Small exact-order targets exist, but not uniformly

#tag("EMPIRICAL", detail: "exhaustive |Delta|<=200000, primes 3<=r<=43") For
every tested prime the least discriminant with $r divides h(Delta)$ in fact had
$h(Delta) = r$, with $abs(Delta) \/ r^2 in [0.684711, 2.555556]$
(`probe_exact_order_targets_full_20260710.csv`); each carries a nonprincipal
reduced form of exact order $r$. #ref(<fig:window>) contrasts these succinct
census targets with the self-certifying family
$Delta_r = 1 - 4 dot 2^r$, which yields a provable exact order-$r$ ideal class
$frak(a) = (2, alpha)$ but has $Theta(r)$ discriminant bits and violates the
input budget. #tag("PROVED") The census locates each target by exhaustive
class-number search, whose cost is not polynomial in $n$; it demonstrates
small-target *existence*, not a uniform growing-family constructor.
#tag("CITED") Prescribed-order existence theorems @lim2016 @ouyangsong2024
@chakrabortyhoque2020 use $n$-th-power discriminant families or ineffective
thresholds; #tag("EMPIRICAL", detail: "bounded primary-source search 2026-07-10")
no checked theorem supplied a uniform polynomial-bit exact-order constructor.

#fig("/figures/P1.5/window.svg", width: 72%, caption: [
  Target discriminant bit length versus prime $r$. The self-certifying
  $1 - 4 dot 2^r$ family (red) grows linearly in $r$ and fails the input budget;
  the census least $abs(Delta)$ with $r divides h(Delta)$ (blue) tracks the
  window floor $2 log_2 r + 1$ (dashed) but is found only by exhaustive search.
  Source: `probe_exact_order_targets_full_20260710.csv`.
]) <fig:window>

= Restricted classification and quadratic class-target factorization

We can now state what is settled.

#keybox(title: "Restricted classification")[
  Let $C = ⟨ P ⟩$ have prime order $r$ and consider a transfer family.
  #tag("PROVED") (1) If the source is available only through a random generic
  encoding with $r^(o(1))$ queries, no transfer exists. (2) If the target is a
  smooth proper algebraic group and the evaluator uses fewer than $r$ rational
  branches, it is one global homomorphism with trivial or elliptic-isogenous
  image. (3) If the target is affine and the evaluator is piecewise rational with
  $B$ branches of pole degree $<= D$, then $max(1, D) B^2 >= r \/ 4$, and a
  rational circuit obeys $d + 2 b >= n - O(log n)$. (4) Finite/local class
  targets are trivial and function-field ones are Jacobians; only a global
  number-field order is genuinely distinct. #tag("CITED") The anomalous, pairing,
  and qualifying Weil-descent transfers occupy the three known exits: a
  non-rational lift, a high-degree short-program pairing, and the proper/geometric
  side.
]

#tag("PROVED") The former literal positive checklist is met by the
pairing-to-ring-class theorem: it accepts ordinary finite-field point
encodings, outputs canonical reduced ideal classes of one fixed polynomial-bit
discriminant, is nonzero and homomorphic, and admits the required target
logarithm. #tag("PROVED") Its factorization through $mu_r$, together with the
polynomial map back to that torus, places it inside the established pairing
mechanism and prevents it from closing novelty-grade Q004.

#tag("CITED") The first attempted strengthening of this control is also prior
art. Huehnlein--Takagi reduce the class-number-one nonmaximal-order DLP to a
finite-field DLP @huehnleintakagi1999, while Castagnos--Laguillaumie give the
effective isomorphism between a general conductor kernel and its finite
residue quotient, including the inverse from reduced ideals
@castagnoslaguillaumie2009. Kopp--Lagarias place the order-change sequence in
a general ray-class framework @kopplagarias2024. Thus effective conductor
extraction is a control, not the missing discovery.

#tag("PROVED") A source-side theorem does survive. Let $E / FF_p$ be
ordinary, let $P$ have prime order $r != p$, put
$K = op("End")(E) ⊗ QQ$, and assume
$r > h(cal(O)_K)$ and $r > 2 sqrt(p) + 2$. If the target is an order in $K$
whose conductor is supported only on $p$ and $r$, then every nonzero transfer
has one of two outcomes. Its $r$-local projection has an explicit
$FF_r$ logarithm and therefore recovers the source scalar in polynomial time;
or its $p$-local projection forces $r divides p-1$. Since also
$r divides p+1-t$, Hasse forces $t=2$, so the source already has embedding
degree one. This theorem permits arbitrary coordinate, lift, valuation,
branching, and direct-form evaluators.

#tag("PROVED") Consequently a still-genuine transfer into an order of the
source CM field must use an external conductor prime $ell$ satisfying
$r divides ell-chi_K(ell)$, or survive in the maximal-order component. In the
split case $ell >= 2r+1$; in the inert case $ell >= 2r-1$.

The residual looks wider than it is. Its conductor and maximal components are
both residue characters.

#theorem(name: "quadratic class-target factorization")[
  #tag("PROVED", detail: "GRH only for uniform short-prime setup") Let
  $r >= 5$ be prime and let $h$ have exact order $r$ in
  $op("Pic")(cal(O)_f)$, where
  $cal(O)_f=ZZ+f cal(O)_K$ is an explicit imaginary-quadratic order whose
  maximal discriminant, conductor, and conductor factorization are public.
  There is a target-side homomorphism $Lambda_h$, nonzero on $h$, into one of
  $
    FF_ell^times, quad
    FF_(ell^2)^times \/ FF_ell^times, quad
    (FF_r,+), quad
    mu_r(FF_q).
  $
  Evaluation is polynomial in the target bit length. In the last case
  $q equiv 1 mod r$ splits in $K$; a separating $q$ exists unconditionally,
  and under GRH it can be found in Las Vegas expected-polynomial time with
  $log q=O(log r+log(log abs(D_K)+2))$.
]

#proof[
  #tag("CITED") The conductor exact sequence @conradconductor
  $
    (cal(O)_K \/ f cal(O)_K)^times \/ (ZZ \/ f ZZ)^times
    -> op("Pic")(cal(O)_f) -> op("Cl")(cal(O)_K) -> 1
  $
  is effective on its kernel @castagnoslaguillaumie2009. Since imaginary
  quadratic units have order dividing six, they contribute no $r$-torsion.
  If $h$ dies maximally, one nonzero CRT component is therefore a tame split
  or inert finite-field torus, or a wild principal-unit $FF_r$ line.

  Otherwise its maximal projection $bar(h)$ has exact order $r$. Choose
  $frak(a)$ representing it and write
  $frak(a)^r=(alpha)$. The virtual-unit exact sequence identifies
  $op("Cl")(cal(O)_K)[r]$ with the classes
  $alpha K^(times r)$ whose finite valuations are divisible by $r$; the unit
  ambiguity vanishes because raising to the $r$-th power is an automorphism of
  $cal(O)_K^times$. Thus $alpha$ is canonical modulo $r$-th powers and is not
  itself an $r$-th power.

  Put $M=K(zeta_r)$. Restriction remains injective on
  $K^times \/ K^(times r)$ because $[M:K]$ divides $r-1$ and
  corestriction after restriction is multiplication by $[M:K]$. Hence
  $M(root(r, alpha)) \/ M$ is a nontrivial Kummer extension. Chebotarev gives
  infinitely many rational primes splitting in $M$ with nontrivial Kummer
  Frobenius. For a selected $frak(q)$ above such a $q$,
  $
    lambda_(frak(q))([frak(a)])
    = alpha^((q-1)\/r) mod frak(q) in mu_r(FF_q)
  $
  is nonzero and therefore injective on the prime-order line.

  Expanding $alpha$ would be exponential. Instead, binary ideal powering
  reduces after each of $O(log r)$ multiplications and records each relative
  generator in a compact power-product graph @vollmer2003
  @jacobsonsawillawilliams2006. Hensel-lifting the selected square root of
  $D_K$ evaluates every compact factor locally, cancels its recorded
  $frak(q)$-valuation, and computes the unit residue by repeated squaring.
  This is polynomial without expanding $alpha$.

  Finally, the normal closure
  $N=K(zeta_r,root(r,alpha),root(r,bar(alpha)))$ has degree $O(r^3)$ and
  $log abs(op("Disc") N)=O(r^3(log abs(D_K)+log r))$: the virtual-unit
  condition makes the Kummer layer unramified away from primes above $r$.
  Effective Chebotarev @lagariasodlyzko1977 and the prescribed-Artin bound
  @bachsorenson1996 give the stated GRH size and Las Vegas search bounds.
]

#tag("PROVED") For any source evaluator $phi$ and $h=phi(P)$, the theorem gives
$
  Lambda_h(phi(x P))=Lambda_h(h)^x
$
in a multiplicative branch, or $x Lambda_h(h)$ in the additive branch.
Therefore an ordinary imaginary-quadratic class presentation cannot be an
independent fourth endpoint. If the composite is not anomalous or
MOV/Frey–Rück, its novelty already lies in a direct source-to-finite-field
character; the class layer is removable. This does not prove that $phi$ cannot
exist and does not claim that every resulting character is pairing-derived.

#tag("CITED") Virtual units and Kummer pairings are classical class field
theory; a modern explicit Selmer presentation appears in
@breenvarmavoight2023. #tag("EMPIRICAL", detail: "bounded primary-source search through 2026-07-23")
The checked literature contains the classical ingredients and the
Hühnlein–Takagi conductor reduction, but no source found in this audit states
the full effective conductor/maximal prime-order dichotomy above. The novelty
claim is therefore the repository-original synthesis, not any ingredient.

#tag("EMPIRICAL", detail: "ten exact-order targets, all scalars") On the
A019 exact-order test family
$D_r=1-4 dot 2^r$, $frak(a)=(2,omega)$, $frak(a)^r=(omega)$, the new probe
finds a nontrivial split-prime character for
$r=3,5,7,11,13,17,19,23,29,31$ and recovers all $r$ scalar logarithms. The
nontrivial values certify a nonzero maximal projection in those ten cases.
The order discriminant is not proved fundamental for every prime $r$, so
A019 is not claimed as an infinite maximal-order family. Instead, Lim's
prescribed-order theorem @lim2016 supplies rigorous infinitude: for every
fixed odd prime $r$, infinitely many imaginary quadratic fields have a
maximal ideal class of exact order $r$, and A028 gives infinitely many
separators for each. Those maximal-order results do not by themselves solve
the separate succinct-target SG-30 problem. The wild conductor branch does.

#pagebreak(weak: true)

== A uniform succinct exact-order target

#theorem(name: "uniform wild ring-class target")[
  #tag("PROVED") For every odd prime $r$, put
  $
    cal(O)_r=ZZ+r^2 ZZ[i], quad Delta_r=-4r^4.
  $
  The primitive reduced form
  $
    F_r=[r^2,2r,r^2+1]
  $
  has exact order $r$ in $op("Pic")(cal(O)_r)$. The pair
  $(Delta_r,F_r)$ and an exact-order certificate are computable
  deterministically in time polynomial in $log r$, and
  $log_2 abs(Delta_r)=2+4log_2 r$. On the generated subgroup, the target
  logarithm is computable in polynomial time through the wild conductor
  coordinate.
]

#proof[
  #tag("CITED") Since $op("Cl")(ZZ[i])=1$, the conductor exact sequence
  @conradconductor identifies $op("Pic")(cal(O)_r)$ with
  $
    (ZZ[i]\/r^2 ZZ[i])^times
    \/
    ((ZZ\/r^2 ZZ)^times dot ZZ[i]^times).
  $
  Let $z_r=1+r i$. It is a unit modulo $r^2$, and the binomial theorem gives
  $z_r^r equiv 1 mod r^2$. Its residue is nontrivial in the displayed
  quotient: multiplication of a rational unit by one of
  $plus.minus 1, plus.minus i$ has a zero real or imaginary coordinate,
  whereas $1+r i$ has neither. Thus its image has exact order $r$.

  The contraction map sends $z_r$ to
  $
    z_r ZZ[i] inter cal(O)_r
    =[1+r^2,-r^3+r^2 i],
  $
  whose form is $[1+r^2,2r^3,r^4]$. One integral shift by $-r$, followed by
  the proper swap, gives
  $
    [1+r^2,2r^3,r^4]
    tilde.equiv [1+r^2,-2r,r^2]
    tilde.equiv [r^2,2r,r^2+1].
  $
  The last form is primitive and reduced. More generally,
  $(1+r a i)(1+r b i) equiv 1+r(a+b)i mod r^2$, so these residues form an
  additive $FF_r$ line and their logarithm is $1+r a i mapsto a$. The effective
  conductor inverse @castagnoslaguillaumie2009 recovers that coordinate from
  a form in the subgroup. All displayed integers have $O(log r)$ bits.
]

#tag("CITED") The conductor sequence, contraction, effective inverse, and wild
principal-unit filtration are classical; their existence is not a new
ingredient. #tag("PROVED") The repository-original contribution here is the
extraction of the closed reduced family, exact-order certificate, and
$Theta(log r)$ SG-25 bit audit. This theorem closes SG-30 positively and
unconditionally. It does not construct a source point-to-class evaluator and
therefore is not a fourth Q004 transfer mechanism.

= Conclusion

The problem asked for a classification of curves admitting a polynomial-time
injective homomorphism into an easy-DLP group, together with an explicit decision
about Weil descent, validated demonstrations of both known transfers, a common
structural description, a candidate table, and a restricted classification. We
delivered all of these in their honest form. The two elementary transfers are one
character construction (#ref(<tab:frame>)); Weil descent counts as a known third
geometric family; and the candidate table (#ref(<fig:tax>)) has a proof, a
citation, or an explicit construction behind every verdict. The structural core is a
chain of exclusions — algebraic-group rigidity, generic-source impossibility,
rational degree/branch/depth bounds, and proper/mixed rigidity — that together
rule out every generic and rational construction and force any nontrivial global
image back onto the elliptic side. The empirical layer validates both elementary
transfers, the ring-class composition, the maximal Kummer character, and each
negative probe at toy scale.

A025 is a complete control theorem. On the Linnik-succinct trace-zero family,
the conductor quotient turns every pairing value into a canonical reduced form
of discriminant $-4p^2$, injectively on the source subgroup, and Gaussian ideal
extension reduces its target logarithm to the accepted finite-field DLP. The
construction also settles its own classification: it factors through the known
pairing and efficiently returns to the same torus, so it is an ordinary
ring-class presentation rather than a new attack mechanism.

A028 supplies the genuinely broader conclusion. Every prime-order subgroup of
an explicit imaginary-quadratic Picard target has an injective post-character
in a conductor residue group or a maximal Kummer power-residue group. The
proof is independent of the source evaluator and therefore includes direct
form synthesis, external conductor support, and unrelated maximal quadratic
fields. Algebraic separation and compact evaluation are unconditional; the
uniform short separator uses the standing ERH/GRH convention. Novelty-grade
Q004 is resolved at that convention: the ordinary class presentation is never
an independent fourth endpoint.

The target-only problem is now closed independently and unconditionally.
For every odd prime $r$, the wild conductor element $1+r i$ in the order
$ZZ+r^2ZZ[i]$ contracts and reduces to $[r^2,2r,r^2+1]$, an exact-order-$r$
class with only $Theta(log r)$ discriminant bits and an exposed additive
target logarithm. The hidden obstruction in the earlier search was an
unnecessary maximal-order requirement. What remains open is the unrestricted
classification over other target categories and, in particular, the
construction or exclusion of source evaluators outside the classified models.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
All computations use toy parameters under the repository's 60-bit ceiling. The
two elementary transfer demonstrations and their timing matrices are produced by
`run_transfers.py` (raw and scaling CSVs dated `20260626`); the CM/annihilator,
ray-class and principal-unit probes by `probe_cm_class_targets.py`; the Buell
residue-coordinate experiment by `probe_buell_reduction.py`; the exact-order
census by `probe_exact_order_targets.py`; the pairing-to-ring-class validation
by `probe_ring_class_transfer.py`; the maximal Kummer-character checks by
`probe_kummer_class_character.py`; and the finite piecewise-overlap
falsification certificate by `audit_rational_tradeoffs.py`. The all-conductor,
wild-layer, and intrinsic trace-two checks are produced by
`probe_conductor_universality.py`. The uniform prescribed-order theorem and
its closed reduction certificate are checked by
`construct_sg30_ring_class_target.py`, with a permanent 15-prime CSV. Each
writes a seeded CSV named in
the captions and figures above. The four figures are regenerated
by `figures/P1.5/make.py` directly from those CSVs. Every mathematical claim
carries one of the epistemic tags #tag("PROVED"), #tag("CITED"),
#tag("EMPIRICAL", detail: "range"), #tag("CONDITIONAL", detail: "hypothesis"),
or #tag("CONJECTURE") exactly as used in the research log; untagged sentences are
exposition, not claims. In particular the toy multiplicative targets are solved
by BSGS, so they validate the map and answer but not the finite-field
subexponential asymptotic, and the literature and census results are bounded
searches, not nonexistence or uniformity theorems.
]

#bibliography("refs/P1.5.bib", title: [References], style: "ieee")
