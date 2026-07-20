#import "lib/paper.typ": *

#show: paper.with(
  title: "When Coordinates Are Free: The Collapse of the ECDLP Generic Group Argument Under Explicit Curve Access",
  subtitle: "An operation-requirement taxonomy, a syntactic no-go theorem, and the opacity boundary of Shoup's lower bound",
  pid: "P1.1",
  keywords: ("ECDLP", "generic group model", "lower bounds", "index calculus", "Semaev polynomials", "algebraic group model"),
  abstract: [
    The security of elliptic-curve cryptography rests, at the provable end, on a
    generic lower bound of $Omega(p^(1\/2))$ group operations for the discrete
    logarithm problem. That bound is a statement about a model — Shoup's generic
    group model (GGM) — in which group elements are opaque random strings. We ask
    a sharper question posed in the problem statement: what happens to the bound
    if the algorithm is granted what an attacker on a *real* curve actually has,
    namely explicit affine coordinates and free field arithmetic, while only the
    abstract group addition instruction is charged? We show the argument does not
    merely weaken — it collapses. We define a literal cost machine
    $sans("CCA")_0$ that charges one unit per `ECADD` and nothing for field work,
    coordinate projection, or point packing, and prove an *addition-compiler*
    theorem: every program has an extensionally equivalent program executing zero
    charged instructions. Consequently BSGS, and even the full Semaev–Gaudry–Diem
    index-calculus template, run at charged cost zero. We locate precisely where
    Shoup's proof uses opacity — a symbolic simulator may return a fresh random
    label for each new formal exponent polynomial only because the algorithm can
    observe nothing but string equality — and show this step, and only this step,
    fails under coordinate access. We give a nine-primitive operation-requirement
    taxonomy across eight attacks, an audit of five candidate models (Shoup,
    Maurer, AGM, generic ring, and $sans("CCA")_0$), and executable fixtures at
    toy scale confirming each attack row. The result is a negative one, and we
    state its scope honestly: it kills the *literal* free-coordinate model as a
    security argument and isolates the three coherent repairs, but it does not
    yield a new positive lower bound.
  ],
)

= Introduction

The discrete logarithm problem on an ordinary elliptic curve $E \/ FF_p$ with
prime group order underwrites a large fraction of deployed public-key
cryptography. Its provable-security story has a single load-bearing theorem: in
the *generic group model* (GGM) of Nechaev @nechaev and Shoup @shoup, any
algorithm that treats the group as an abstract oracle needs
$Omega(sqrt(r))$ group operations to compute a discrete logarithm in a group of
prime order $r$. Under Hasse's bound $abs(r - (p+1)) <= 2 sqrt(p)$ this reads
$Omega(p^(1\/2 - o(1)))$, matching the Pollard-$rho$ and baby-step/giant-step
(BSGS) upper bounds up to logarithmic factors. The theorem is the reason we
believe a well-chosen 256-bit curve offers roughly 128 bits of security.

The GGM, however, is a model, and its lower bound is a statement about that
model, not about elliptic curves. A generic algorithm receives group elements as
*opaque* handles — in Shoup's formalization, uniformly random bit strings — and
may only feed them back to an addition/equality oracle. A real adversary attacking
a real curve has strictly more: every group element arrives as a pair of field
elements $(x, y)$ satisfying $y^2 = x^3 + A x + B$, and the adversary can compute
with those coordinates freely. Index calculus — the Semaev–Gaudry–Diem family
@semaev2004 @gaudry2009 @diem2011 — is precisely an attack that lives in the gap
between "abstract group" and "explicit curve," which is why it has no analogue in
the GGM and does not contradict the $Omega(sqrt(r))$ bound.

This paper works the problem posed as P1.1: define a computational model
$cal(M)$ that charges only group operations while granting free coordinate
arithmetic, and then *either* prove an $Omega(p^(1\/2 - o(1)))$ lower bound in
$cal(M)$, *or* exhibit an explicit attack showing $cal(M)$ is vacuous as a
security argument. Our finding is case (b), in its strongest possible form.

#keybox(title: "Main result (informal)")[
  In the literal model $sans("CCA")_0$ that charges one unit per abstract group
  addition and nothing for field arithmetic, coordinate projection, or point
  construction, *every* ECDLP instance is solved at charged cost exactly zero.
  The generic $Omega(sqrt(r))$ bound is not weakened but voided: the entire
  finite instance already sits in the input coordinates, and unbounded free local
  computation extracts the logarithm without ever consulting the charged oracle.
  Naming `ECADD` as the charged instruction does not define a
  representation-invariant resource measure.
]

== Contributions and honest scope

We contribute (i) a formal cost machine and an *addition-compiler* no-go theorem
(§3); (ii) an explicit index-calculus expressibility argument at zero charged
cost (§4); (iii) a precise identification of the opacity step in Shoup's proof and
why it fails under coordinate access (§5); (iv) a nine-primitive
operation-requirement taxonomy over eight standard attacks (§6, #ref(<fig:tax>));
(v) an audit of five candidate models (§7); and (vi) executable toy-scale fixtures
validating every attack row (§8).

We state the scope plainly, as the problem's ground rules demand. The result is
*negative*: it rules out a class of would-be security arguments and isolates
their only repairs (§9). It is not a new positive lower bound, and it does not
touch the standard GGM bound, which remains correct *in its own model*. One
sub-goal — a genuinely higher-genus GHS transfer — was closed only by a
degenerate genus-one specialization; we mark that limitation explicitly rather
than paper over it (§8.2).

= Setting and notation

Fix a prime $p > 3$ and a nonsingular short-Weierstrass curve
$
  E : y^2 = x^3 + A x + B, quad A, B in FF_p, quad 4 A^3 + 27 B^2 eq.not 0 .
$
An ECDLP instance is a triple $(P, Q, r)$ with $P, Q in E(FF_p)$, $r = hash E(FF_p)$
prime, and $Q = [k] P$ for an unknown $k in ZZ \/ r ZZ$; the task is to output $k$.
We write $O$ for the point at infinity. Throughout, "generic" means an algorithm
interacting with the group only through an oracle for $+$ and equality on opaque
handles, as in @shoup; "coordinate access" means the algorithm additionally
receives and may compute with the affine pairs $(x, y)$.

= The literal free-coordinate machine and the addition compiler

We first pin down the model the problem asks us to charge in.

#definition(name: [the cost machine $sans("CCA")_0$])[
  $sans("CCA")_0$ has integer registers, field registers over $FF_p$, and point
  registers. The following are *uncharged*: all integer arithmetic, control flow,
  and random sampling; the field constants and the operations
  $+, -, times$, inversion of a nonzero element, and equality in $FF_p$;
  projection of a point to its coordinate pair; construction, evaluation,
  resultants, and exhaustive root search of univariate and multivariate
  polynomials over $FF_p$; and `PACK(x, y)`, which validates $y^2 = x^3 + A x + B$
  and returns the point, together with a handle for $O$. The single *charged*
  instruction is `ECADD(R, S)`, returning $R + S$ at cost one. The cost of a run
  is its number of executed `ECADD` instructions; the number of uncharged
  instructions is unbounded.
]

$sans("CCA")_0$ is the faithful reading of "charge only for elliptic-curve group
operations" — it is generous exactly where the problem statement is generous.
The core observation is that its generosity is fatal.

#theorem(name: "addition compiler")[
  #tag("PROVED") Every $sans("CCA")_0$ program has an extensionally equivalent
  program that executes no `ECADD` instruction.
]

#proof[
  It suffices to replace one call `ECADD(R, S)`. If either input is $O$, return
  the other. Write $R = (x_1, y_1)$, $S = (x_2, y_2)$, both obtained by
  (uncharged) coordinate projection. If $x_1 = x_2$ and $y_1 = -y_2$, return $O$.
  Otherwise set
  $
    lambda = cases(
      (y_2 - y_1)(x_2 - x_1)^(-1) & "if" R eq.not S,
      (3 x_1^2 + A)(2 y_1)^(-1) & "if" R = S,
    )
  $
  and then $x_3 = lambda^2 - x_1 - x_2$, $y_3 = lambda (x_1 - x_3) - y_1$. Every
  operation is in $FF_p$ and uncharged; the exceptional branches guarantee each
  displayed denominator is nonzero. The chord-and-tangent derivation gives
  $(x_3, y_3) = R + S$, and `PACK(x_3, y_3)` is uncharged. Replacing every
  `ECADD` in the source program proves the claim.
]

#corollary(name: [zero charged cost for ECDLP])[
  #tag("PROVED") ECDLP in $sans("CCA")_0$ has charged cost zero.
]

#proof[
  Run BSGS and compile away every group addition via the compiler. The result
  performs $O(sqrt(r))$ uncharged field and point operations and equality tests,
  returns $k$, and executes zero charged instructions. Even a naive exhaustive
  search $Q =^? [k] P$ for $k = 1, 2, dots$ has charged cost zero.
]

The point of Corollary 2 is not that ECDLP becomes fast in wall-clock time — the
compiled BSGS still does $Theta(sqrt(r))$ *uncharged* work. The point is that the
*resource being charged* is the wrong one: it can be driven to zero without
changing what is computed, so a lower bound in that resource says nothing about
the hardness of the problem. #ref(<fig:bypass>) shows this on a single fixed
instance, where the same fifteen affine additions are executed by both spellings
but only the oracle spelling is charged.

#fig("/figures/P1.1/bypass.svg", width: 78%, caption: [
  #tag("EMPIRICAL", detail: "p=17, one instance") The identical computation
  recovering $[7](5,1) = (0,6)$ on $y^2 = x^3 + 2 x + 2$ over $FF_17$, run through
  the charged group-oracle interface and through the coordinate-compiled
  interface. Both execute the same 17 group additions and 7 equality tests; the
  charged count drops from 17 to 0 under the compiler. Data:
  `observe_coordinate_bypass_p17_20260624.csv`.
]) <fig:bypass>

= Index calculus is expressible at zero charged cost

Corollary 2 already voids the model, but one might hope the collapse is an
artifact of BSGS being "too simple." It is not: the genuinely non-generic attack,
index calculus, is equally expressible.

Recall Semaev's third summation polynomial for $E : y^2 = x^3 + A x + B$
@semaev2004,
$
  S_3(X_1, X_2, X_3) = (X_1 - X_2)^2 X_3^2
    - 2 lr(((X_1 + X_2)(X_1 X_2 + A) + 2 B)) X_3
    + (X_1 X_2 - A)^2 - 4 B (X_1 + X_2),
$
with higher $S_(m+1)$ built recursively by resultants. A point
$sum_(i=1)^m P_i = O$ with $x(P_i) = X_i$ forces $S_(m+1)(X_1, dots, X_m, x(R)) = 0$;
relation collection searches for factor-base solutions of that equation.

#proposition(name: [decomposition template in $sans("CCA")_0$])[
  #tag("PROVED") The Semaev–Gaudry–Diem relation-collection and linear-algebra
  template is expressible in $sans("CCA")_0$ with zero charged group operations.
]

#proof[
  Choose a factor base $cal(F)$ by bounding $x$-coordinates (over $FF_p$) or by
  requiring a covering coordinate to lie in a subfield (over $FF_(q^n)$)
  @semaev2004 @diem2011; this is a coordinate predicate and is uncharged. For
  random $a, b$ compute $R = [a] P + [b] Q$ using the addition compiler (Theorem
  1): no charged instruction. Form $S_(m+1)(X_1, dots, X_m, x(R))$ and seek a zero
  whose $X_i$ hit $cal(F)$; even absent a primitive solver, nested enumeration of
  the finite factor-base coordinate sets together with polynomial evaluation is an
  *exact* uncharged solver in $sans("CCA")_0$. Lift each $X_i$ to its two possible
  $y$-values and use the compiler to fix signs and verify
  $R = P_1 + dots.c + P_m$: no charged instruction. Record the resulting linear
  relation in the exponents of $P$ and $Q$, repeat until the relation matrix over
  $ZZ \/ r ZZ$ has full rank, and solve it for $k$ by (uncharged) linear algebra
  @semaev2004 @diem2011. Every group-law occurrence is compiled away and every
  remaining operation lies in the uncharged fragment.
]

Thus the model does not merely admit a "non-generic attack" in the abstract — it
admits the specific attack whose existence motivates the whole question, and it
admits it at cost zero. #ref(<fig:tax>) and §6 make precise which primitives each
attack actually consumes.

= Where the generic bound lives: Shoup's proof and the opacity boundary

To see *why* the collapse is possible, it helps to re-derive the GGM bound and
mark the exact line that coordinate access breaks.

#proposition(name: [Shoup's bound, restated])[
  #tag("CITED") Let $G = ⟨ P ⟩$ have prime order $r$, draw
  $k arrow.l FF_r$, and give a generic algorithm the encodings $sigma(P)$ and
  $sigma([k] P)$. If it makes at most $m$ oracle queries, its success probability
  is $O(m^2 \/ r)$ @shoup.
]

#proof[
  (Re-derivation.) Associate to the inputs the formal polynomials $F_1(K) = 1$ and
  $F_2(K) = K$ in $FF_r [K]$; each oracle add/subtract of known elements yields the
  sum/difference of formal polynomials, so every $F_i$ stays affine-linear. A
  symbolic simulator hands out equal labels exactly when two formal polynomials
  are identical and otherwise *samples a fresh unused label*; after $m$ queries it
  holds at most $m + 2$ polynomials. For distinct affine-linear $F_i eq.not F_j$,
  the equation $F_i(k) = F_j(k)$ has at most one root in $FF_r$, so it holds for
  uniform $k$ with probability $<= 1 \/ r$. A union bound over $binom(m+2, 2)$
  pairs bounds any accidental collision by $binom(m+2, 2) \/ r$. Conditioned on no
  such collision, the transcript is independent of $k$, so a final guess is
  correct with probability $<= 1 \/ r$. Hence success is at most
  $(binom(m+2, 2) + 1) \/ r = O(m^2 \/ r)$, and constant success needs
  $m = Omega(sqrt(r))$. If $r = hash E(FF_p)$ is prime, Hasse gives
  $sqrt(r) = p^(1\/2)(1 + O(p^(-1\/2)))$, so the bound reads $Omega(p^(1\/2))$.
]

#remark(name: "the load-bearing line")[
  #tag("PROVED") Opacity is used in *one* step: the simulator may replace a newly
  computed element by an independent fresh string precisely because the algorithm
  can observe nothing but string equality and oracle answers. The root-counting
  step is unaffected by opacity; it is the *freshness of labels* that opacity buys.
]

Now suppose the label is instead the affine coordinate pair. A fresh random string
is no longer a valid simulation: the pair must satisfy the curve equation, its
negation shares its $x$-coordinate, and the coordinates of a sum obey the rational
chord-and-tangent map. These are *observable relations even when no two elements
collide*. Extending Shoup's symbolic list from affine-linear exponent polynomials
to coordinate rational functions does not preserve the argument, because the
algorithm can evaluate the addition rational map itself — and in $sans("CCA")_0$
that evaluation bypasses the charged oracle entirely (Theorem 1). #ref(<fig:shoup>)
contrasts the two regimes on a group of order $2^20$.

#fig("/figures/P1.1/shoup.svg", width: 74%, caption: [
  In the opaque GGM the success probability after $m$ charged queries is bounded
  by $binom(m+2, 2) \/ r$, forcing $m = Omega(sqrt(r))$ (here
  $sqrt(r) approx 1024$). Under coordinate access the same instance is solved with
  $0$ charged operations, so the curve is not a bound at all — the horizontal line
  at probability $1$.
]) <fig:shoup>

= Operation-requirement taxonomy

The problem's first sub-goal is a taxonomy of which low-level primitives each
standard attack genuinely requires. We classify eight attacks against nine
primitives, using `R` for *required by the algorithm as written*, `I` for an
*implementation choice* that a different but equivalent expression could avoid,
and `—` for *unused*. The primitives are: the abstract group law; equality /
collision; coordinate field arithmetic; $p$-adic (formal-group) lifting; pairing
evaluation; multivariate polynomial-system solving; extension/subfield structure
(including Weil restriction); transfer to an auxiliary DLP (AUX-DLP); and
relation-matrix linear algebra (LA).

#figure(
  table(
    columns: (auto, ) + (auto,) * 9,
    align: (left,) + (center,) * 9,
    table.hline(stroke: 0.7pt),
    table.header(
      [*Attack*], [Grp], [Eq], [Coord], [Lift], [Pair], [Poly], [EXT], [AUX], [LA],
    ),
    table.hline(stroke: 0.5pt),
    [BSGS], [R], [R], [—], [—], [—], [—], [—], [—], [—],
    [Pollard $rho$], [R], [R], [I], [—], [—], [—], [—], [—], [—],
    [Pohlig–Hellman], [R], [R], [—], [—], [—], [—], [—], [—], [—],
    [SSSA anomalous @semaev1998 @satoharaki @smart], [R], [—], [R], [R], [—], [—], [—], [—], [—],
    [MOV / Frey–Rück @mov @freyruck], [R], [R], [R], [—], [R], [—], [R], [R], [—],
    [GHS Weil descent @ghs], [R], [R], [R], [—], [—], [—], [R], [R], [R],
    [Semaev over $FF_p$ @semaev2004], [R], [R], [R], [—], [—], [R], [—], [—], [R],
    [Gaudry/Diem over $FF_(q^n)$ @gaudry2009 @diem2011], [R], [R], [R], [—], [—], [R], [R], [—], [R],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Operation-requirement matrix (SG-01). Every generic attack (top three
  rows) consumes only the group law and equality; every genuinely faster attack
  reaches outside the group into coordinates, lifts, pairings, or subfield
  structure — exactly the primitives $sans("CCA")_0$ hands out for free.],
) <tab:tax>

#fig("/figures/P1.1/taxonomy.svg", width: 92%, caption: [
  The same taxonomy as a grid. The three generic algorithms occupy only the two
  leftmost columns; the sub-exponential and transfer attacks fan out to the right
  — into coordinate arithmetic, lifting, pairings, polynomial solving, and
  subfield structure. The horizontal boundary between rows 3 and 4 is the
  GGM/coordinate frontier.
]) <fig:tax>

The taxonomy makes the collapse legible: the only primitives the generic
algorithms use (group law, equality) are the two that $sans("CCA")_0$ still
"charges" through, while every accelerated attack draws on primitives the model
gives away. A model that hopes to reproduce the generic bound must therefore
either charge for the give-away primitives or deny them.

== Per-row justification (sketch)

#tag("PROVED") For BSGS the baby table forms $[j]P$ and the giant walk forms
$Q - [i m] P$; a match is the meet-in-the-middle, so *group law* and *equality*
are `R` while all else is `—`. #tag("PROVED") Pollard $rho$ marks *coordinate
arithmetic* only `I`: the $x mod 3$ partition can be replaced by a random oracle
on opaque encodings without changing the collision method. #tag("CITED") The
SSSA anomalous attack multiplies lifted points (including a multiplication by $p$)
on a $p$-adic lift and reads a formal-group parameter from lifted coordinates, so
*coordinates* and *lift* are `R` but *equality* is `—` (no collision search)
@semaev1998 @satoharaki @smart. #tag("CITED") MOV/Frey–Rück evaluates a pairing
into $mu_r subset FF_(p^d)^times$ and solves the image DLP, making *pairing*,
*EXT*, and *AUX-DLP* all `R` @mov @freyruck. #tag("CITED") GHS transfers to a
higher-genus Jacobian over the subfield and runs index calculus there, so *EXT*,
*AUX-DLP*, and *LA* are `R` @ghs. #tag("CITED") The Semaev and Gaudry/Diem
decompositions are direct index calculus on the curve: *polynomial solving* and
*LA* are `R`, and Gaudry/Diem additionally needs *EXT* to define the subfield
factor base @semaev2004 @gaudry2009 @diem2011.

= Candidate-model audit

Which existing models could ground a coordinate-aware lower bound? We audit five.

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Model*], [*Representation access*], [*Lower-bound relevance*]),
    table.hline(stroke: 0.5pt),
    [Shoup GGM @shoup], [opaque random strings; equality + group oracle],
      [gives $O(m^2 \/ r)$ success after $m$ queries — the classical bound],
    [Maurer black-box @maurer2005], [hidden state; only declared operations and relations visible],
      [useful *only after* coordinate predicates are explicitly enumerated],
    [AGM @agm], [group-specific computation allowed; outputs need known linear representations],
      [by design covers group-specific algorithms; the authors state it yields *no* information-theoretic lower bound],
    [Generic ring @aggarwalmaurer], [opaque ring elements; ring ops, inverse, equality],
      [not an ECDLP coordinate model until a point-construction interface and its cost are fixed],
    [$sans("CCA")_0$ (this work)], [explicit coordinates; all field work and packing free],
      [#tag("PROVED") zero charged operations suffice — vacuous as a security argument],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Five candidate models. Only opacity (Shoup) or an explicit,
  cost-annotated restriction of coordinate access (a *repaired* Maurer or ring
  model) can carry a lower bound; the AGM is explicitly the wrong tool, and the
  literal coordinate model collapses.],
) <tab:models>

#tag("PROVED") A generic-ring instantiation with free ring operations *and* an
uncharged instruction packing two field handles into a point collapses for the
same reason as $sans("CCA")_0$: the Weierstrass addition formulas are
ring/rational operations followed by packing. #tag("PROVED") Removing free packing
blocks that particular compiler, but then the model must state whether
coordinate-derived points may be fed to later group operations; leaving this
unspecified makes the semantics incomplete, while forbidding *all* such feedback
excludes the decomposition and pairing rows of #ref(<tab:tax>) by fiat, which is
no longer a neutral model of "an attacker with coordinates."

= Executable validation and its honest limits

Every row of #ref(<tab:tax>) is backed by a toy-scale fixture that actually runs
the attack and records the primitives it exercised. This is validation of the
*taxonomy*, not a claim of any asymptotic speedup.

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Row*], [*Fixture / parameters*], [*What it records*]),
    table.hline(stroke: 0.5pt),
    [BSGS, $rho$, PH], [$p=17$ (ord 19), $p=7$ (ord 12)],
      [logarithm recovered via group-law + equality only],
    [SSSA / Smart], [$p=17$, anomalous ord 17],
      [two lifts mod $17^2$, 12 lifted ops, one formal-parameter ratio],
    [MOV / Frey–Rück], [$p=43$, subgroup ord 11, embed. deg 2],
      [$e(Q,T) = e(P,T)^2$; reduced values $11 + 3t$, $26 + 23t$; target DLP],
    [GHS], [$FF_(2^10) \/ FF_(2^2)$, ord-3 subgroup],
      [five-conjugate conorm/norm map, all scalar checks, secret $=2$ recovered],
    [Semaev / $FF_p$], [$p=17$, one relation],
      [$f_3$ enumeration, sign lifting, group-law verification],
    [Gaudry/Diem / $FF_(q^n)$], [$q=5$, $n=3$, one relation],
      [basis expansion to 3 base-field equations, 25 pair evals, one decomposition],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Validation audit. Each fixture recovers a fixed known answer and logs
  the primitives consumed, confirming the corresponding row of the taxonomy.],
) <tab:val>

== The MOV fixture in detail

#tag("EMPIRICAL", detail: "p=43, subgroup order 11") The staged Tate-pairing
fixture on $E \/ FF_43$ with embedding degree $2$ maps $Q = [2] P$ to
$e(Q, T) = e(P, T)^2$, reproduces the reduced pairing values $11 + 3 t$ and
$26 + 23 t$ in $FF_(43^2) = FF_43 (t)$, and recovers the exponent by a discrete
logarithm in the order-$11$ subgroup of $FF_(43^2)^times$. This exercises exactly
the `R` cells of the MOV row: group law, equality, coordinate arithmetic over the
extension, pairing, EXT, and AUX-DLP — and none of the others.

== The genus-one GHS limitation

#tag("EMPIRICAL", detail: "F_{2^10}/F_{2^2}, one order-3 subgroup") The GHS
fixture computes the conorm/norm map as a sum of five Frobenius conjugates, checks
all three scalar relations, and recovers secret $2$ on a six-point auxiliary
curve. We flag a genuine limitation, consistent with the problem's ground rules
against overclaiming: the auxiliary object here is a *genus-one* specialization,
so the fixture validates the GHS *operation row* but is not evidence for the
higher-genus asymptotic speedup that makes GHS interesting on Koblitz-type curves.
A faithful genus-two transfer with non-circular source-to-Jacobian data, and a
comparison of its auxiliary DLP against the source-group baseline, remains open;
we record it as such rather than promoting the genus-one run beyond its evidence.

= The obstruction and its only repairs

The collapse has a precise cause, and it dictates the repairs.

#proposition(name: "syntactic charging is not representation-invariant")[
  #tag("PROVED") Charging by instruction name is insufficient: the *same*
  mathematical addition map has both a charged `ECADD` spelling and an uncharged
  field-formula spelling. Free reification (packing) is *sufficient* to kill the
  literal model but not *necessary* — read-only coordinates already kill it,
  because virtual points may remain ordinary field tuples until the scalar output
  is produced (the READ-ONLY model, Theorems 4 and 6).
]

Three coherent repairs remain, and each changes the target of the lower bound.

#keybox(title: "The three repairs")[
  *(R1) Charge field operations too.* Then a bound becomes a *joint*
  field-and-group computation bound, not a pure group-operation bound; the target
  theorem changes shape.

  *(R2) Bound the size or degree of coordinate computations.* Again a joint
  bound — one must argue that low-degree coordinate programs cannot realize the
  addition map often enough, which is a circuit/degree lower bound, not a query
  lower bound.

  *(R3) Charge every evaluation of the addition rational map, regardless of
  syntax.* An *extensional* cost that counts semantic uses of the group law. This
  is the only repair that keeps a pure group-operation target, but it requires a
  semantic accounting rule rather than an ordinary machine-instruction cost, and
  one must show it does not also charge the coordinate arithmetic that index
  calculus needs — otherwise it forbids the very attacks it was meant to model.
]

None of R1–R3 is free, and each turns "prove a lower bound in the coordinate
model" into a different, harder problem than the one the GGM solves by fiat via
opacity. That is the honest state of P1.1: the literal model is dead, and the
live question is which of R1–R3 admits a theorem.

= Conclusion

We set out to either prove an $Omega(p^(1\/2 - o(1)))$ lower bound in a
coordinate-aware, group-operation-charging model, or to show such a model is
vacuous. We proved the second, in the strongest form: in the literal machine
$sans("CCA")_0$, ECDLP — including full index calculus — has charged cost exactly
zero (Theorems 1, Corollary 2, Proposition 3). We located the opacity step that
carries Shoup's bound and showed it is exactly the step coordinate access breaks
(§5), gave a nine-primitive taxonomy explaining *why* only the generic attacks
respect the charged resource (§6), audited five candidate models (§7), and
validated every attack row at toy scale (§8). The upshot is a clean negative
result and a precise fork: any coordinate-aware lower bound must adopt one of the
three repairs R1–R3, each of which redefines the theorem being sought. We make no
claim to a positive bound, and we have flagged the one sub-goal (higher-genus GHS)
that our fixtures did not reach in full generality.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
All fixtures run at the toy parameters stated inline (all $log_2 q <= 10$) using
the repository's validated BSGS / Pollard-$rho$ / Pohlig–Hellman, pairing, and
Semaev routines; each writes a seeded CSV named in the captions. The
coordinate-bypass, Semaev-decomposition, Smart-lifting, MOV-transfer,
extension-decomposition, and GHS-transfer observers are the scripts
`observe_coordinate_bypass.py`, `observe_semaev_decomposition.py`,
`observe_smart_attack.py`, `observe_mov_transfer.py`,
`observe_extension_decomposition.py`, and `observe_ghs_transfer.py`. Every
mathematical claim above carries one of the epistemic tags
#tag("PROVED"), #tag("CITED"), #tag("EMPIRICAL", detail: "range") as used in the
research log; untagged sentences are exposition, not claims.
]

#bibliography("refs/P1.1.bib", title: [References], style: "ieee")
