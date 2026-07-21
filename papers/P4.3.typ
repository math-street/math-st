#import "lib/paper.typ": *

#show: paper.with(
  title: "The exTNFS Complexity Is Still Heuristic: A Complete Smoothness-Dependency Audit, a Boundary Relation-Supply Theorem, and the Degree-Uniformity Barrier",
  subtitle: "What is and is not proved about the extended tower number field sieve in medium characteristic — a negative report with retained partial theorems",
  pid: "P4.3",
  keywords: ("discrete logarithm", "exTNFS", "number field sieve", "smooth numbers", "rigorous analysis", "medium characteristic", "L-notation"),
  abstract: [
    Problem P4.3 asked for an unconditional $L_(p^n)(1\/3, c)$ complexity
    theorem for the extended tower number field sieve (exTNFS) of
    Kim–Barbulescu in medium characteristic with composite extension degree —
    possibly for a modified algorithm, possibly with a worse constant. *This
    target was not achieved, and the task record closes it as failed.* This
    paper reports, with the record's own epistemic tags, exactly what stands
    between the community and such a theorem. We decompose the exTNFS pipeline
    into ten numbered analytic inputs S-01–S-10, each stated as a precise
    uniform density claim about the actual iterated-resultant norm forms; two
    are theorems (rigorous smooth-candidate factorization, and the
    Canfield–Erdős–Pomerance random-integer benchmark), and eight are open —
    joined by two adjacent non-smoothness gaps, polynomial-selection
    irreducibility and relation-matrix rank. We prove that the minimal missing
    relation statement is a *joint* two-sided smoothness lower bound (RC) that
    marginal densities do not imply; that the minimal missing rank statement is
    a hyperplane-escape bound (R2) that smoothness counts do not imply; and a
    *degree-uniformity barrier*: keeping relation norms on the optimized
    $L_Q (2\/3)$ scale in the strict medium-characteristic interior forces the
    tower degree $eta -> infinity$, outside the quantifiers of every fixed-form
    smooth-value theorem in the audited literature. On the boundary
    $ell_p = 2\/3$ we retain a genuine partial positive: an unconditional,
    explicitly randomized $L_Q (1\/3, O(1))$ *relation-supply* theorem for the
    restricted family $p equiv 3 mod 4$, $eta = 2$, $R = ZZ[i]$, with an
    explicit nonoptimized constant — which provably does not extend to the
    interior by the same proof, and which is *not* a DLP theorem: target
    splitting, special-$q$ descent, and rank remain open, and we prove
    structural barriers (a subspace-counting bound and a resultant-bidegree
    identity) explaining why the boundary construction does not linearize
    either remaining stage. An exact toy experiment ($p = 5$, $eta = 2$,
    $kappa = 3$, all 5,856 primitive coefficient vectors factored completely)
    falsifies the literal random-integer model at finite scale: joint
    smoothness exceeds the matched dyadic baseline by factors 8.50–3.05. The
    honest bottom line: today's fully rigorous alternative remains
    Bender–Pomerance at $L_Q (1\/2, sqrt(2))$-type costs, and every path to
    $1\/3$ runs through the specific open statements catalogued here.
  ],
)

= Introduction

The extended tower number field sieve computes discrete logarithms in
$FF_(p^n)^*$ for composite $n = eta kappa$ by working in a tower
$R = ZZ[t] \/ (h)$ of degree $eta$ over which two polynomials $f, g$ share an
irreducible factor of degree $kappa$ modulo $p$; its announced complexities,
down to $L_Q (1\/3, (48\/9)^(1\/3))$ and $L_Q (1\/3, (32\/9)^(1\/3))$ for the
best constructions, made every medium-characteristic pairing field
re-evaluated after 2016 @kimbarbulescu2016. Those complexities are theorems
*under classical NFS heuristics*: each structured norm value is modelled as a
uniformly random integer of the same size, two correlated norms are modelled
as independent, and the descent tree is modelled by Dickman probabilities.
Problem P4.3 asked whether this can be made unconditional — for exTNFS
itself, or for an identified modification, possibly with a worse constant.

#keybox(title: "Outcome, stated plainly")[
  #tag("PROVED") The formal objective *failed*: no unconditional
  $L_Q (1\/3, c)$ complexity theorem was proved for exTNFS or any complete
  modified DLP algorithm, and the research record closes the task as
  abandoned at the operator's direction. What the record retains — and what
  this paper reports — is (i) a complete ten-input dependency audit with
  every smoothness assertion stated precisely against the actual tower norm
  forms (§3); (ii) proofs that the minimal missing statements are a joint
  smoothness bound (RC), an adaptive descent bound (SQ), and a rank-escape
  bound (R2), none implied by the others (§3–4); (iii) a degree-uniformity
  barrier showing fixed-degree smooth-form theorems cannot reach the
  optimized interior parameter range (§5); (iv) an unconditional boundary
  relation-supply theorem at $ell_p = 2\/3$, $eta = 2$ with an explicit
  constant (§6); (v) proved structural barriers for target splitting and
  special-$q$ descent (§7); and (vi) an exact toy falsification of the
  literal random-integer model (§8).
]

We use the record's epistemic tags throughout: #tag("PROVED"),
#tag("CITED"), #tag("CONJECTURE") for precisely stated open inputs,
#tag("CONDITIONAL", detail: "GRH") where relevant, and
#tag("EMPIRICAL", detail: "scope") for finite computations. A negative
report has one job — to make the obstruction exact — and we have tried to
write every open statement so that a future proof (or refutation) of it is
well-posed.

= The algorithm being audited

== Notation

Write
$
  L_Q (alpha, c) = exp lr(( (c + o(1)) (log Q)^alpha (log log Q)^(1 - alpha) )),
  quad Q = p^n, quad n = eta kappa, quad gcd(eta, kappa) = 1,
$
and parameterize medium characteristic by $p = L_Q (ell_p, c_p)$ with
$1\/3 < ell_p < 2\/3$. exTNFS chooses $h in ZZ[t]$ of degree $eta$
irreducible modulo $p$, works in $R = ZZ[t] \/ (h)$, and chooses
$f, g in R[x]$ whose reductions modulo $p$ share an irreducible degree-$kappa$
factor $k(x)$ over $R \/ p R tilde.equiv FF_(p^eta)$, so both tower number
fields map onto $FF_Q$ @kimbarbulescu2016.

A relation candidate is $r = a(iota) - b(iota) x$ with
$a(t) = sum_(i < eta) a_i t^i$, $b(t) = sum_(i < eta) b_i t^i$,
$abs(a_i), abs(b_i) <= A$, and its two integer norms are the iterated
resultant forms in the $2 eta$ variables
$bold(z) = (a_0, ..., a_(eta - 1), b_0, ..., b_(eta - 1))$:
$
  F_f (bold(z)) = abs("Res"_t ("Res"_x (a(t) - b(t) x, f(x)), h(t))), quad
  F_g (bold(z)) = abs("Res"_t ("Res"_x (a(t) - b(t) x, g(x)), h(t))) .
$
A row is kept when both $F_f (bold(z))$ and $F_g (bold(z))$ are $B$-smooth
with $B = L_Q (1\/3, beta)$; accepted rows are factored over prime-ideal
factor bases, extended by Schirokauer coordinates, and the sparse system is
solved modulo the large prime $ell | Q - 1$ @kimbarbulescu2016
@schirokauer2008.

== The heuristic cost calculation

#tag("CITED") With optimized selection the two norms obey
$F_f <= L_Q (2\/3, gamma_f + o(1))$, $F_g <= L_Q (2\/3, gamma_g + o(1))$, and
Kim–Barbulescu write relation collection plus linear algebra as
$
  L_Q lr(( 1\/3, thick beta + (gamma_f + gamma_g) / (3 beta) + o(1) ))
  + L_Q (1\/3, thick 2 beta + o(1)),
$
modelling each norm as an arbitrary integer of its size and multiplying the
two probabilities @kimbarbulescu2016.

#lemma(name: "balancing")[
  #tag("PROVED") Equating the two displayed exponents gives
  $beta^2 = (gamma_f + gamma_g) \/ 3$ and total constant
  $2 sqrt((gamma_f + gamma_g) \/ 3)$.
]

Every appearance of "the probability of an arbitrary integer" above is an
unproved transfer; making that exact is the audit of the next section.

= The ten smoothness inputs

Let $cal(S)_Q (A)$ be the nonzero coefficient vectors with both norms
nonzero and $P^+ (m)$ the largest prime factor of $abs(m)$. We state the
inputs S-01–S-10 of the record's dependency audit; the full formal versions
are in the research file `SMOOTHNESS_ASSUMPTIONS.md`.

*S-01/S-02 (marginal relation densities).* #tag("CONJECTURE") Uniformly along
every admissible parameter sequence actually output by the selection
algorithm,
$
  (hash{bold(z) in cal(S)_Q (A) : P^+ (F_s (bold(z))) <= B})
  / (hash cal(S)_Q (A))
  = L_Q lr(( 1\/3, thick -gamma_s / (3 beta) + o(1) )), quad s in {f, g}.
$

*S-03 (joint density — the minimal relation statement).* #tag("CONJECTURE")
The single statement sufficient for the upper bound is the uniform *lower*
bound
$
  (hash{bold(z) in cal(S)_Q (A) : P^+ (F_f (bold(z)) F_g (bold(z))) <= B})
  / (hash cal(S)_Q (A))
  >= L_Q lr(( 1\/3, thick -(gamma_f + gamma_g) / (3 beta) + o(1) )),
$
paired with the deterministic count
$hash cal(S)_Q (A) = L_Q (1\/3, beta + (gamma_f + gamma_g) \/ (3 beta) + o(1))$.
We call this (RC).

#proposition(name: "marginals do not imply (RC)")[
  #tag("PROVED") S-01 and S-02 do not imply S-03: both events are functions
  of the *same* coefficient vector and may be correlated at the full
  $L$-exponent scale. Multiplying marginal densities is an additional
  assumption, not algebra. (§8 exhibits positive dependence exactly at toy
  scale.)
]

*S-04/S-05 (initial target splitting).* #tag("CONJECTURE") For a target $s$
and randomizing exponents $e <= E$, the JLSV2 lift norm $M_e <= X_0$ (or the
Waterloo numerator/denominator pair $U_e V_e$, $abs(U_e V_e) <= Q^(1 + o(1))$)
must contain squarefree $Y_0$-smooth values at random-integer frequency:
$
  hash{e <= E : P^+ (M_e) <= Y_0, thick mu^2 (M_e) = 1}
  >= E dot.c (Psi(X_0, Y_0)) / X_0 dot.c L_Q (1\/3, o(1)),
$
uniformly over all allowed targets — a smooth-value claim about
subgroup-indexed structured lifts, not about random integers.

*S-06 (squarefreeness).* #tag("CONJECTURE") The squarefree co-condition needs
a positive uniform proportion *after conditioning on smoothness*; a smooth-values
theorem alone does not discharge it.

*S-07 (one special-$q$ step).* #tag("CONJECTURE") For a prime ideal
$frak(q)$ of norm $nu$ with enumeration set $cal(C)_frak(q) (D)$ (bounded
combinations of an LLL basis of its lattice) and child bound $y = nu^c$, with
cofactor sizes $u_f = log X_(f, frak(q)) \/ log y$,
$u_g = log X_(g, frak(q)) \/ log y$:
$
  (hash{bold(z) in cal(C)_frak(q) (D) :
    P^+ (G_(f, frak(q))(bold(z)) thick F_g (bold(z))) <= y})
  / (hash cal(C)_frak(q) (D))
  >= rho_D (u_f) thick rho_D (u_g) thick L_Q (1\/3, o(1)),
$
where $G_(f, frak(q)) = F_f \/ nu$ and $rho_D$ is Dickman's function. We call
this (SQ).

*S-08 (adaptive uniformity).* #tag("CONJECTURE") (SQ) must hold — or fail
with summable probability — simultaneously over every $frak(q)$, every LLL
basis, and every child selected by the random descent history, with the
accumulated trial count inside the $L_Q (1\/3, c + o(1))$ budget. A pointwise
statement for one fixed lattice is insufficient.

*S-09 (smoothness testing — known).* #tag("CITED") Hyperelliptic smoothness
testing factors a $y$-smooth $m <= x$ in expected $y^(o(1))$ time when
$y = (log x)^(omega(1))$ @lenstrapilapomerance1993 @leevenkatesan2018.
#tag("PROVED") The exTNFS regime satisfies the hypothesis ($x <= L_Q (2\/3, O(1))$,
$y = B = L_Q (1\/3, beta)$), so *testing cost is not the obstruction* —
supply is.

*S-10 (the benchmark — known).* #tag("CITED") Canfield–Erdős–Pomerance give,
uniformly in their range, the density
$Psi(L_Q (b, d), L_Q (a, c)) \/ L_Q (b, d) = L_Q (b - a, -d (b - a) \/ c + o(1))$
@canfielderdospomerance1983. #tag("PROVED") This counts *integers*; invoking
it after calling a norm "random" is precisely the unproved transfer isolated
in S-01–S-08.

== Status against the strongest known partial results

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Input*], [*Closest unconditional result*], [*What is missing*]),
    table.hline(stroke: 0.5pt),
    [S-01–S-02], [fixed binary forms: positive-proportion friable values
      @balogblomerdartygetenenbaum2012; fixed quadratic form and fixed-field
      smooth ideals @barbulesculachand2017],
      [parameter-dependent $2 eta$-variable iterated-resultant forms; the far
      sparser $L (1\/3)$ range; uniformity as fields, degrees, discriminants
      vary],
    [S-03], [products of finitely many *fixed* forms in dense ranges
      @barbulesculachand2017],
      [joint $L$-scale lower bound for two *varying* tower forms],
    [S-04–S-06], [rigorous index calculus randomizes integers/polynomials with
      countable distributions @pomerance1987 @benderpomerance1998],
      [control of subgroup-indexed tower lift norms, jointly smooth and
      squarefree, uniformly over targets],
    [S-07–S-08], [Dickman-type smooth-ideal counts in one *fixed* field
      @barbulesculachand2017],
      [short principal generators in varying special-$q$ lattices, paired
      second side, adaptive uniformity],
    [S-09], [hyperelliptic smoothness test @lenstrapilapomerance1993], [nothing — this input is closed],
    [S-10], [CEP density @canfielderdospomerance1983], [nothing — but it is only the benchmark],
    table.hline(stroke: 0.7pt),
  ),
  caption: [The audit table. #tag("CONDITIONAL", detail: "GRH")
  Buchmann–Hollinger's smooth-ideal lower bound @buchmannhollinger1996 does
  not change the picture: even under GRH it counts ideals, not short
  principal generators satisfying a second-side condition or a special-$q$
  constraint.],
) <tab:audit>

#fig("/figures/P4.3/audit.svg", width: 90%, caption: [
  The dependency audit at a glance: of the ten smoothness inputs plus the two
  adjacent gaps of §4, exactly two are theorems — the cost of factoring
  accepted candidates (S-09) and the random-integer benchmark (S-10). Every
  supply statement is open.
]) <fig:audit>

= The two adjacent non-smoothness gaps

Even a full proof of (RC), (IS), and (SQ) would not prove the DLP
complexity. Two further inputs are unproved and are *not* smoothness
statements.

== Polynomial-selection irreducibility

#tag("CITED") The Conjugation selection expects suitable irreducible
polynomials after a small number of trials; the source labels this step
heuristic @kimbarbulescu2016. An unconditional proof must construct the
sequence uniformly or account for the search rigorously.

== Relation-matrix rank: the minimal escape condition

#tag("PROVED") Counting accepted relations is not enough: all
$L_Q (1\/3, beta)$ rows could lie in a proper subspace of the admissible row
space $H_Q$ (the annihilator of the true virtual-logarithm functionals
@schirokauer2008). The record's attempt A004 isolates the *minimal*
sufficient rank input.

#theorem(name: "rank escape suffices and preserves the constant")[
  #tag("PROVED") Let $mu_Q$ be the distribution of the valuation/Schirokauer
  row $R$ of an accepted relation, and define
  $
    delta_Q = inf_(phi in H_Q^* without {0}) thick
    Pr_(R tilde.op mu_Q) [phi(R) eq.not 0] .
  $
  If $delta_Q >= L_Q (1\/3, -o(1))$, then adaptively retaining independent
  rows spans $H_Q$ after at most $dim (H_Q) \/ delta_Q$ accepted rows in
  expectation; since $dim H_Q = L_Q (1\/3, beta + o(1))$, the leading
  $L (1\/3)$ constant is unchanged.
]

#proof[
  If the current span $W subset.neq H_Q$ is proper, pick $phi eq.not 0$
  vanishing on $W$; the event $phi(R) eq.not 0$ forces $R in.not W$, so the
  expected number of accepted rows per dimension increase is at most
  $1 \/ delta_Q$; sum over at most $dim H_Q$ increases.
]

#tag("PROVED") For *uniform* rows in an $r$-dimensional space, $r + s$ rows
fail to span with probability below $ell^(-s) \/ (ell - 1)$ — but exTNFS rows
are sparse, share $(a, b)$ across their two sides, and are conditioned on
simultaneous smoothness, so the uniform benchmark is exactly that: a
benchmark. The usable analytic form of the escape condition is a
character-cancellation bound over the *smooth-conditioned* candidate set —
i.e., it is logically downstream of the open (RC), and no audited fixed-form
theorem supplies the required equidistribution. The record labels this
condition (R2); it is open. The deterministic prerequisites (no empty
factor-base column, connected support hypergraph, symmetries quotiented into
$H_Q$, duplicate rows discarded) are catalogued as proved checklist items.

= The degree-uniformity barrier

Could one instead *prove* smoothness for a restricted tower — say quadratic
$eta = 2$, where the outer norm is a binary quadratic form covered by
Barbulescu–Lachand's fixed-form theorem @barbulesculachand2017? The record's
attempt A003 answers with exact identities and a scaling obstruction.

#proposition(name: "exact quadratic norm identities")[
  #tag("PROVED") For $h(T) = T^2 + h_1 T + h_0$ with root $iota$ and
  $Delta_h = h_1^2 - 4 h_0$:
  $N(x + y iota) = x^2 - h_1 x y + h_0 y^2$; for $z_i = x_i + y_i iota$ the
  pullback $Q(U, V) = N(U z_0 + V z_1) = A U^2 + B U V + C V^2$ has
  $
    B^2 - 4 A C = Delta_h (x_0 y_1 - x_1 y_0)^2 ,
  $
  and the inhomogeneous slice $N(z_0 + U z_1 + V z_2)$ has homogeneous part
  of discriminant $Delta_h (x_1 y_2 - x_2 y_1)^2$, constant term $N(z_0)$,
  and linear coefficients $"Tr"(z_0 overline(z_1))$, $"Tr"(z_0 overline(z_2))$.
]

#tag("PROVED") Auditing Theorem 4.2 of @barbulesculachand2017 against these
slices: the one-parameter affine slice is a single row of the averaged form
(no lower bound follows); the two-parameter affine slice is a lattice
*coset*, outside the theorem; only the homogeneous slice matches, and then
only when the square lattice-index factor in the discriminant disappears —
after which the removed fixed divisor must itself be $B$-smooth. A genuine
algebraic opening survives:

#proposition(name: "kernel randomization is surjective")[
  #tag("PROVED") Randomizing the selected polynomial inside the kernel of
  reduction, $f_(U, V) = f_0 + p U + K V$ with $K$ a lift of the common
  factor $k$, shifts the relative resultant by the ideal
  $(p b^kappa, K^([kappa]) (a, b))$, which equals the whole ring $R$ whenever
  $d = kappa$, $K$ is monic, and $(a, b) = R$ with $(a, b)$ nonzero modulo
  $p$. The natural coefficient randomization is thus *algebraically*
  surjective onto the quadratic tower order for ideal-coprime candidates.
]

But surjectivity is not a distribution theorem, and the decisive obstruction
is quantitative:

#theorem(name: "degree-uniformity barrier")[
  #tag("PROVED") Let $p = L_Q (ell_p, c_p)$ with $1\/3 < ell_p < 2\/3$ and
  let the relation search have $L_Q (1\/3, tau)$ candidates. The iterated
  resultant is homogeneous of degree $eta d >= n$ in the coefficients of
  $(a, b)$, so the standard box-wide norm bound carries an $A^n$ term with
  $
    log (A^n) = (tau + o(1)) / (2 c_p eta) thick
    (log Q)^(4\/3 - ell_p) (log log Q)^(ell_p - 1\/3) .
  $
  For *fixed* $eta$ this is an $L_Q (4\/3 - ell_p, O(1))$ scale — strictly
  above $L_Q (2\/3)$ throughout the interior — and keeping the norm on the
  $L_Q (2\/3)$ scale forces
  $
    eta = Theta lr(( (log Q \/ log log Q)^(2\/3 - ell_p) )) -> infinity,
    quad
    kappa = Theta lr(( (log Q \/ log log Q)^(1\/3) )) .
  $
  Hence every fixed-degree, fixed-form smooth-value theorem misses the
  optimized interior regime: the theorem's quantifiers and the algorithm's
  parameter range are incompatible.
]

#fig("/figures/P4.3/barrier.svg", width: 84%, caption: [
  #tag("PROVED") The barrier of Theorem 6, drawn as pure scaling (constants
  suppressed): the tower degree $eta$ required to keep relation norms on the
  optimized $L_Q (2\/3)$ scale grows without bound for every fixed interior
  $ell_p$, while every audited smooth-form theorem lives on the dashed
  fixed-$eta$ line. Only the boundary $ell_p = 2\/3$ (exponent $0$) escapes.
]) <fig:barrier>

= What can be proved on the boundary: a relation-supply theorem

At the boundary $ell_p = 2\/3$ the barrier exponent vanishes, and the record's
attempt A005 converts the algebraic opening into an unconditional — but
sharply restricted — theorem. Its ingredients, each proved in the record:
a bounded-fiber lemma for the primitive map $(u, v) |-> A u + B v$ on a fixed
imaginary quadratic order (Bézout solution plus kernel-lattice reduction); a
count of monic irreducibles with prescribed nonzero evaluation over a residue
field,
$
  I_d (r, c) >= 1/d lr(( (s^d - 1)/(s - 1) - d s^(d\/2) )) = Theta_s (s^(d-1) \/ d),
$
via norm fibers and subfield exclusion; residue-class equidistribution of the
kernel fibers; and the fixed-form smoothness input for the Gaussian norm
form of discriminant $-4$ @barbulesculachand2017 with CEP density
@canfielderdospomerance1983.

#theorem(name: "boundary relation supply, unconditional")[
  #tag("PROVED") Consider inputs $Q = p^n$ with $p = L_Q (2\/3, c_p)$,
  $p equiv 3 mod 4$, $n = 2 kappa$, tower $R = ZZ[i]$ (so $h = T^2 + 1$ stays
  irreducible modulo $p$). Lift a random irreducible degree-$kappa$ factor to
  $K in R[x]$ and randomize both sides by the kernel families
  $
    f = K (1 + v_f) + p U_f, quad g = K (1 + v_g) + p U_g .
  $
  Put $A = L_Q (1\/3, a)$, $B = L_Q (1\/3, beta)$, and
  $m = c_p + a \/ (2 c_p)$. For any $beta$ with $beta c_p > 1\/3$ and any
  $
    a > (beta + (8 c_p) / (3 beta)) / (4 - 4 / (3 beta c_p)),
  $
  the randomized collector finds an irreducible pair $(f, g)$ together with at
  least $L_Q (1\/3, beta)$ jointly $B$-smooth relation candidates in expected
  time
  $
    L_Q lr(( 1\/3, thick 4 a + (8 m) / (3 beta) + o(1) )) .
  $
]

The constant is explicit and *nonoptimized*; the theorem's value is
existence, not efficiency. Its proof multiplies the counts of admissible
$f$- and $g$-coefficients for each *fixed* candidate — so it never assumes
independence of the two norm values — and finishes with a Markov/averaging
argument over polynomial pairs.

#tag("EMPIRICAL", detail: "161 finite-field cases; 121 quadratic-order targets")
The two computational lemmas were validated exactly: Möbius/norm-fiber counts
satisfied the irreducible-count lower bound in all 161 tested instances
(fields $s in {2, 3, 5, 7, 11}$, degrees $2 <= d <= 8$, minimum slack 1.5),
and the toy Bézout identity $5(-1) + (1 - iota)(2 + 2 iota) = 1$ in
$ZZ[iota] \/ (iota^2 + 2)$ represented all 121 targets in $[-5, 5]^2$ with
coefficients bounded by 30.

#keybox(title: "Exact scope — read before citing")[
  #tag("PROVED") Theorem 7 is a *relation-supply* theorem for one boundary
  subfamily. It does not prove: (1) that accepted rows span the relation
  lattice (the (R2) gap of §4); (2) that arbitrary targets split into
  covered objects (S-04–S-06); (3) that special-$q$ descent succeeds with
  uniform probability and cost (S-07–S-08); (4) anything for fixed interior
  $ell_p < 2\/3$, where Theorem 6 forces $eta -> infinity$ and the only
  smooth-value input used — one fixed quadratic form — is unavailable. Do
  not promote it to an exTNFS or DLP complexity theorem.
]

= Why the remaining stages do not linearize

Two proved barriers explain why the boundary construction stalls exactly at
target splitting and descent.

#proposition(name: "targets do not land in low-degree subspaces")[
  #tag("PROVED") Write $FF_Q = FF_(p^eta)[theta] \/ (k(theta))$ and let
  $W_m = {sum_(j <= m) c_j theta^j}$, so $hash W_m = p^(eta (m + 1))$. If $s$
  generates a subgroup of order $ell$ and $e$ is uniform modulo $ell$, then
  $
    Pr[s^e in W_m] <= p^(eta (m + 1)) / ell ,
  $
  which for a full-size subgroup ($ell = Q^(1 - o(1))$) is
  $p^(-eta (kappa - m - 1) + o(n))$. Dropping even *one* tower coefficient
  from a full-degree representative costs a factor $p^(-eta)$, whose inverse
  has logarithm $Theta((log Q)^(2\/3) (log log Q)^(1\/3))$ — an
  $L_Q (2\/3, O(1))$ wait, far beyond any $L_Q (1\/3)$ budget. Exponent
  randomization therefore cannot make a generic full-group target linear in
  $theta$; a nonlinear representation or a genuinely new theorem about
  full-degree lift norms is required. (For much smaller subgroups the bound
  is vacuous, and the needed subgroup–subspace intersection statement is
  open.)
]

#proposition(name: "resultant bidegree barrier")[
  #tag("PROVED") $"Res"_x (P, f)$ is homogeneous of degree $deg f$ in the
  coefficients of $P$ and of degree $deg P$ in the coefficients of $f$. The
  A005 mechanism works *only* because a relation polynomial $a - b x$ has
  degree one, making the resultant *affine* in the randomized coefficients of
  $f$ — indeed $"Res"_x (a - b x, f) = b^(deg f) f(a \/ b)$. A generic target
  lift of degree $kappa - 1$ makes the randomized outer form have total
  degree $eta kappa = n + O(eta)$: exactly the growing-degree regime with no
  known smooth-value theorem. Factoring the lift as $L dot.c S$ with only a
  linear factor randomized just relocates the problem into the fixed factor
  $S$, whose norm must *also* be smooth.
]

#tag("PROVED") Special-$q$ descent inherits both horns of the dilemma:
re-randomizing the polynomial changes the number field and destroys the
identification of $frak(q)$, its lattice, and every factor-base virtual
logarithm (cross-field relations are themselves target-lifting problems);
keeping the field fixed removes the A005 randomness and returns exactly to
the open (SQ). These are barriers to *this* modification family, not
impossibility theorems — the record states them as such.

= The exact toy experiment

The record's SG-04 experiment instantiates a genuine exTNFS tower — not a
proxy form — at the smallest interesting size:
$
  p = 5, quad h = t^2 + 2, quad f = x^3 + x + 1, quad g = x^3 + x - 4,
  quad Q = 5^6 ,
$
where $h$ is irreducible modulo 5 and $f equiv g mod 5$ is an irreducible
cubic ($eta = 2$, $kappa = 3$). #tag("PROVED") For $a = a_0 + a_1 iota$,
$b = b_0 + b_1 iota$ with $iota^2 = -2$, the inner resultant for
$x^3 + x + c$ is $a^3 + a b^2 + c b^3$ and the outer norm of $u_0 + u_1 iota$
is $u_0^2 + 2 u_1^2$. The program exhausts all 5,856 primitive vectors in
$[-4, 4]^4$, *fully factors* both norms of every vector by deterministic
trial division, and draws one independent uniform integer from each norm's
dyadic interval as a size-matched baseline (seed 4304). Every stored
factorization (23,424 of them) and 128 nested resultants were reproduced by
independent SymPy checks.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (right, right, left, right, right),
    table.hline(stroke: 0.7pt),
    table.header([*$B$*], [*actual joint rate*], [*baseline rate (95% Wilson)*],
      [*ratio*], [*joint / marginals*]),
    table.hline(stroke: 0.5pt),
    [7], [0.023224], [0.002732 (0.001683–0.004434)], [8.50], [7.73],
    [13], [0.043716], [0.005635 (0.004016–0.007903)], [7.76], [5.14],
    [31], [0.073087], [0.019980 (0.016698–0.023891)], [3.66], [3.81],
    [61], [0.114071], [0.037398 (0.032833–0.042568)], [3.05], [2.82],
    table.hline(stroke: 0.7pt),
  ),
  caption: [#tag("EMPIRICAL", detail: "p=5, eta=2, kappa=3, A=4, exhaustive")
  Joint $B$-smoothness of the two tower norms versus the matched
  random-integer baseline. The preregistered divergence criterion (outside
  the baseline's 95% interval by a factor $>= 1.5$ at two adjacent bounds)
  is met at all four bounds, and the preregistered positive-dependence
  prediction is not refuted at any of them.],
) <tab:toy>

#fig("/figures/P4.3/toyrates.svg", width: 86%, caption: [
  #tag("EMPIRICAL", detail: "5,856 primitive vectors, seed 4304") Actual
  joint smooth rates (exact population values) against the dyadic baseline
  with Wilson intervals, log scale. Annotations give the actual/baseline
  ratio. Data:
  `measure_norm_smoothness_p5_A4_B7-13-31-61_all_s4304_20260702_summary.csv`.
]) <fig:toyrates>

#fig("/figures/P4.3/dependence.svg", width: 82%, caption: [
  #tag("EMPIRICAL", detail: "same run") Two dependence diagnostics versus
  $B$: the actual/baseline joint-rate ratio and the actual joint rate divided
  by the product of the actual marginals. Both decrease toward — but stay
  well above — the independence line at these parameters.
]) <fig:dependence>

#tag("PROVED") The honest reading: this finite example *falsifies literal
equality* with the chosen random-integer model at these parameters and shows
the two sides are positively dependent (they share the term $a^3 + a b^2$),
but it neither supports nor refutes the asymptotic $L$-exponent. It is
evidence about model structure, not about complexity.

= Rigorous alternatives, and their price

#tag("CITED") Bender–Pomerance give a rigorous index-calculus algorithm for
*every* finite field via smooth polynomials, with growing-extension costs
$L_Q (1\/2, sqrt(2) + o(1))$ for $p <= n^(o(n))$, an intermediate
$L_Q (1\/2, sqrt(8\/3) + o(1))$ range, and $p^(2 + o(1))$ for
$p > n^(4n\/3)$ @benderpomerance1998, building on the randomization
precedents of @pomerance1987. #tag("PROVED") In medium-characteristic
notation this fallback costs $L_Q (1\/2, sqrt(2) + o(1))$ for
$ell_p < 1\/2$ and $L_Q (ell_p, 2 c_p + o(1))$ for $ell_p > 1\/2$ — an
unconditional theorem for the same DLP, with exponent $1\/2$ or $ell_p$ in
place of $1\/3$. It is the cleanest currently identified "modified algorithm
with worse complexity", and it is not an analysis of exTNFS.

#tag("CITED") Lee–Venkatesan's randomized ordinary NFS is the closest
rigorous relative at exponent $1\/3$: randomizing $f = hat(f) + (x - m y) R$
makes evaluations vary in an arithmetic progression, where smooth-number
theorems apply (their factoring conclusion still cites a separate character
conjecture) @leevenkatesan2018. #tag("PROVED") The literal tower analogue
fails: a kernel-randomized relative resultant varies in $R = ZZ[t] \/ (h)$,
and the outer norm $N_(R \/ QQ)$ is a *nonlinear* degree-$eta$ form of it —
not an integer progression — so the progression theorem proves none of
S-01–S-03 and gives no special-$q$ statement. Sampling smooth *ideals* first
@barbulesculachand2017 is a one-side idea only: the same generator must still
be smooth on the other side, so (RC) and (SQ) survive intact.

= Why the formal target failed

#tag("PROVED") Assembling the audit: the smallest missing relation theorem
is (RC) — not two marginal Dickman statements — and the strongest missing
theorem is (SQ) under S-08's adaptive uniformity; even both, plus S-04–S-06,
would leave polynomial-selection accounting and the rank bound (R2). The
boundary theorem (Theorem 7) closes relation supply for one restricted
family and provably does not extend inward (Theorem 6). No statement in the
audited literature has the exTNFS quantifiers. The record therefore closes
P4.3 with its target unmet, and lists the resume conditions verbatim: a
uniform lower bound for smooth values of growing-degree tower norm forms; or
character cancellation / hyperplane escape after conditioning on simultaneous
smoothness; or a provable target-splitting distribution compatible with the
restricted generator; or a rigorous special-$q$ descent whose degrees and
coefficient sizes stay within the claimed complexity. Any one of these would
reopen the problem with a real chance of progress.

= Conclusion

The extended tower number field sieve's $L_Q (1\/3, c)$ complexity remains,
today, a heuristic statement. This report replaces the folklore version of
that sentence with an exact one: the heuristic content is precisely S-01
through S-08 plus polynomial-selection accounting and the rank escape (R2);
the two rigorous ingredients (S-09, S-10) are cost and benchmark, not
supply; fixed-form theorems are structurally blocked from the optimized
interior by the degree-uniformity barrier; the boundary family
$ell_p = 2\/3$, $eta = 2$ admits an unconditional relation-supply theorem
with explicit constants; and the toy data show the random-integer model is
already false in the small, in the direction (positive dependence) that at
least does not starve relation collection. We did not prove the theorem we
wanted. What a future proof must contain is now, we believe, stated
precisely enough to be attacked.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rule-col)
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
The full formal statements of S-01–S-10, the status table, and the modified
algorithm audits are the research file `SMOOTHNESS_ASSUMPTIONS.md`; the
partial theorems are attempts A003 (quadratic identities, kernel
surjectivity, degree barrier), A004 (rank escape), A005 (boundary
relation-supply theorem and its four lemmas), A006 (subspace counting), and
A007 (resultant bidegree), all in `attempts/`. The toy experiment is
`code/measure_norm_smoothness.py` (deterministic, seed 4304, exhaustive
$A = 4$ box; independent SymPy replay of all 23,424 factorizations and 128
nested resultants), with dated raw and summary CSVs in `data/`; the figures
here are regenerated from the summary CSV by `papers/figures/P4.3/make.py`,
and the audit map and barrier plot are drawn from the proved statements
cited in their captions. The task's terminal status (abandoned, formal
target failed) is recorded in `STATE.md` and `HANDOFF.md`. Every
mathematical claim above carries the epistemic tag of the research record;
untagged sentences are exposition, not claims.
]

#bibliography("refs/P4.3.bib", title: [References], style: "ieee")
