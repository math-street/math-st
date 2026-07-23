# Notes

## Stable facts

- [PROVED] A nonzero homomorphism out of a group of prime order is injective,
  because its kernel is a proper subgroup of a prime-order group and is
  therefore trivial.
- [CITED] Semaev (1998), Satoh--Araki (1998), and Smart (1999) give
  polynomial-time discrete-logarithm algorithms for the characteristic-$p$
  torsion case, including prime-field anomalous curves.
- [CITED] Menezes--Okamoto--Vanstone (1993) and Frey--Ruck (1994) reduce
  suitable prime-to-characteristic torsion logarithms to finite-field
  multiplicative logarithms by pairings.
- [CITED] Belding (2007, arXiv:math/0703906) constructs a nondegenerate
  pairing on $p$-torsion over dual numbers and interprets the Semaev--Ruck
  attacks as pairing attacks analogous to MOV.

## SG-01 - operational definition

**Definition (transfer package).** For an infinite family of instances
$I=(q,E,P,r)$, put $n=\lceil\log_2 r\rceil$ and let $L$ be the full encoded
input length. Require $L=n^{O(1)}$. A transfer package consists of a uniformly
and effectively presented finite group $G_I$, setup data of size polynomial in
$L$, and a uniform evaluator

$$
\phi_I:\langle P\rangle\longrightarrow G_I
$$

subject to all of the following requirements.

1. The encoding length and group-operation cost in $G_I$ are polynomial in
   $L$.
2. The evaluator computes $\phi_I(Q)$ from the ordinary representation of
   $Q\in\langle P\rangle$ in expected polynomial time in $L$.
3. The evaluator is a group homomorphism and is injective on $\langle P\rangle$.
4. Given $\phi_I(P)$ and $\phi_I(Q)$, a uniform target algorithm recovers the
   logarithm in expected time $\exp(o(n))$, including precomputation and
   setup attributable to the instance.

The evaluator need not compute $\phi_I^{-1}$. Randomized evaluators and target
algorithms are allowed when their expected costs meet the same bounds.

- [PROVED] The definition excludes a lookup table of all $r$ source points,
  because its setup and representation cost are exponential in $n$.
- [PROVED] The abstract isomorphism $[n]P\mapsto n\bmod r$ is not a transfer
  unless its evaluator is supplied independently, because evaluating it is the
  source DLP itself.
- [PROVED] A constant map, an $x$-coordinate map, and a hash-to-group map fail
  respectively injectivity, the homomorphism requirement, and the homomorphism
  requirement.
- [PROVED] An efficiently computable isogeny to another generic elliptic curve
  does not qualify merely from being injective: the definition also requires a
  subexponential target DLP algorithm.

### Weil descent decision

Weil descent counts; it is not excluded by terminology. A particular descent
instance qualifies only after both injectivity on $\langle P\rangle$ and the
end-to-end $\exp(o(n))$ target bound have been established.

- [CITED] Gaudry--Hess--Smart (2002) construct explicit homomorphisms from
  selected characteristic-two elliptic-curve groups to Jacobians over a
  smaller field.
- [PROVED] If a constructed homomorphism has kernel order coprime to $r$, then
  its restriction to $\langle P\rangle$ is injective, because the intersection
  of the kernel with the order-$r$ subgroup is trivial.
- [CONDITIONAL: the curve-family and smoothness hypotheses in Enge--Gaudry--Thome 2009]
  A descent into their high-genus low-degree Jacobian families has a
  subexponential target DLP algorithm.
- [PROVED] Merely rewriting $E(\mathbb F_{q^n})$ as rational points of a Weil
  restriction does not meet requirement 4, because this group isomorphism
  alone supplies no target DLP algorithm.

- [CITED] Thus Weil descent is a third *geometric target family* under this
  definition, but it is known prior art rather than a newly discovered
  transfer.

## SG-04 - one framework for the two elementary transfers

- [CITED] Both elementary cases compute a nonzero character of a prime-order
  cyclic source into an easy order-$r$ target; their auxiliary constructions
  differ, but nondegeneracy is the common injectivity certificate (Belding
  2007 for the characteristic-$p$ pairing interpretation).

| Case | Tag | Auxiliary structure | Fixed functional | Easy target | Nondegeneracy test |
|---|---|---|---|---|---|
| Characteristic $p$ | [CITED] | lift to a first-order $p$-adic or dual-number thickening | connecting/formal-log map on $p$-torsion | $(\mathbb F_q,+)$ or a one-dimensional additive quotient | image of $P$ is nonzero |
| Prime-to-$p$ | [CITED] | Weil or Tate pairing on $E[r]$ | $T\mapsto e_r(T,Q)$ for a fixed independent $Q$ | $\mu_r\subset\mathbb F_{q^k}^{*}$ | $e_r(P,Q)\ne1$ |

- [PROVED] Each fixed functional in the table is injective on $\langle P\rangle$
  once it is a nonzero homomorphism, by the prime-order kernel argument in the
  stable facts.
- [CITED] Belding (2007) makes this parallel literal for $p$-torsion by
  constructing the missing nondegenerate Weil-pairing analogue over dual
  numbers.
- [CONJECTURE] A genuinely new elementary transfer requires a computable
  nonzero character not induced by a local connecting map, a bilinear torsion
  pairing, or a geometric descent; a counterexample is any explicit family
  meeting SG-01 whose construction provably lies outside all three mechanisms.

## SG-05/SG-06 - candidate target enumeration

| Candidate | Verdict | Reason |
|---|---|---|
| Other local formal groups | Excluded for $r\ne p$; known mechanism for $r=p$ | [PROVED] If $r$ is a unit in the coefficient ring, the formal multiplication series $[r](T)=rT+O(T^2)$ has a compositional inverse, so the formal group has no nonzero $r$-torsion. [CITED] Semaev (1998) handles rational characteristic-$p$ torsion beyond only the prime-field trace-one wording. |
| Jacobians of covers | Included conditionally | [PROVED] For a finite separable cover $\pi:C\to E$ of degree $d$, norm after pullback is multiplication by $d$, so pullback is injective on $r$-torsion when $r\nmid d$. [CONDITIONAL: applicable high-genus DLP hypotheses] It is a transfer only when the Jacobian algorithm is subexponential in the source security parameter. |
| Weil-restriction abelian varieties | Neutral until composed | [PROVED] The defining rational-point identification preserves the original DLP exactly; any improvement comes from a subsequent quotient, isogeny, or Jacobian realization. |
| Class and ray-class groups | Included, but every explicit quadratic ordinary target factors through a finite/local residue character | [PROVED] A003--A024 exclude or bound the natural direct, generic, rational, ray-principal-unit, and low-observation variants. [PROVED] A025 maps the established degree-two pairing target into $\operatorname{Pic}(\mathbb Z+p\mathbb Z[i])$. [PROVED, GRH only for uniform maximal short-prime setup] A028 factors every order-$r$ image through a conductor residue group or a maximal Kummer power-residue character. |
| Drinfeld modules | Excluded as a new additive target for $r\ne p$ | [CITED] A Drinfeld module has underlying algebraic group $\mathbb G_a$ (Poonen, 2021 notes, Definition 3.2). [PROVED] Its finite-field additive points have exponent $p$, so they contain no order-$r$ element for $r\ne p$; for $r=p$ an algebraic map from $E$ is excluded by SG-07 and a nonalgebraic map falls back to the characteristic-$p$ linearizer question. |
| Tori | Excluded for global algebraic maps; pairing case included | [PROVED] Every algebraic-group homomorphism $E\to T$ is trivial by SG-07 because a torus is affine. [CITED] Maps defined only on $E[r]$ arise from the established Weil/Tate pairing route. |
| Additive groups of larger characteristic-$p$ rings | Excluded for $r\ne p$ | [PROVED] The underlying additive group is killed by $p$, so it cannot contain an order-$r$ subgroup for a different prime; the $r=p$ case is the additive/local family rather than a third target type. |
| Other elliptic curves or abelian varieties | Structurally classified, not automatically useful | [PROVED] SG-07 shows that a nonconstant algebraic-group map has elliptic image isogenous to $E$; requirement 4 still needs an independently easier ambient DLP. |

> **Control result.** [PROVED] A025 supplies an explicit evaluator into the
> ordinary ring class group of $\mathbb Z+p\mathbb Z[i]$. It respects
> addition and is injective because it is the composition of a nondegenerate
> pairing with the conductor exact-sequence map. It satisfies the former
> literal checklist but does not close novelty-grade Q004 because it is a
> representation of the known bilinear mechanism.

## SG-07 - restricted classification theorem

### Theorem

- [PROVED] Let $k$ be a finite field, let $E/k$ be an elliptic curve, let $H/k$
  be a smooth finite-type algebraic group, and let $f:E\to H$ be an
  algebraic-group homomorphism. The reduced image of $f$ is either trivial or
  an elliptic abelian subvariety of $H$; in the latter case
  $f:E\to f(E)$ is an isogeny.
- [PROVED] In particular, if $H$ is affine then $f$ is trivial.

### Proof

- [PROVED] The curve $E$ is proper and connected, so the image of $f$ is a
  proper connected closed algebraic subgroup of $H$.
- [CITED] A complete connected group variety is an abelian variety, and a
  complete algebraic group is anti-affine (Milne 2022, Sections 2 and 8e).
- [PROVED] The image has dimension at most one; if it has dimension zero,
  connectedness makes it the identity subgroup, and if it has dimension one,
  it is an elliptic curve.
- [PROVED] In the nonconstant case the kernel has dimension zero and is finite,
  so the induced surjection from $E$ to its elliptic image is an isogeny.
- [PROVED] If $H$ is affine, the image is both proper connected and affine;
  equivalently, every coordinate function pulls back to a global regular
  function on the complete curve $E$, hence to a constant, so the homomorphism
  is trivial.

### Boundary of the theorem

- [PROVED] The theorem does not classify the operational definition in SG-01,
  because a transfer evaluator need only be defined on $\langle P\rangle$ and
  need not extend to a morphism on $E$.
- [PROVED] MOV evades the theorem because fixing the second pairing argument
  gives a character only on the finite subgroup $E[r]$, not a global morphism
  $E\to\mathbb G_m$.
- [PROVED] The anomalous transfer evades the theorem because it uses a lift or
  infinitesimal thickening and a connecting map, not a global morphism
  $E/\mathbb F_p\to\mathbb G_a$.

## SG-02/SG-03 - computational validation

- [EMPIRICAL: seven anomalous curves, p in {101,211,401,809,1601,3203,6421}]
  Exact point counting verified $\#E(\mathbb F_p)=p$, the additive evaluator
  passed five scalar homomorphism checks per curve, and every seeded logarithm
  was recovered; see `data/run_transfers_full_20260626_raw.csv`.
- [EMPIRICAL: seven k=2 subgroups, (p,r) from (43,11) through (8011,2003)]
  Exact point counting, subgroup-order checks, four bilinearity checks per
  curve, and independent scalar multiplication validated every recovered
  logarithm; see `data/run_transfers_full_20260626_raw.csv`.
- [EMPIRICAL: Windows 11, Python 3.13.4, seven sizes per transfer, 50 timing repeats]
  The median additive map time fit work exponent $1.050508$ with log-residuals
  in $[-0.047656,0.056971]$, and the affine Tate map fit exponent $1.052569$
  against Miller-line count times field bit length with residuals in
  $[-0.271154,0.225140]$; every residual is stored in
  `data/run_transfers_full_20260626_scaling.csv`.
- [PROVED] The implemented additive map uses double-and-add for a scalar $p$
  and therefore $O(\log p)$ lifted group operations; the recorded counts rise
  from 10 to 18 over the tested range.
- [PROVED] The implemented Tate map uses a left-to-right Miller loop with
  $O(\log r)$ line evaluations; the recorded counts rise from 5 to 17, while
  retained affine denominators add field-inversion cost.
- [PROVED] The multiplicative target logs in the toy validation are solved by
  BSGS with width $\lceil\sqrt r\rceil$ rather than by index calculus, so their
  wall timings validate the map and recovered answer but do not establish the
  cited finite-field subexponential asymptotic.

## SG-08/SG-09 - CM class-group obstructions

### Orientation-loss lemma

- [PROVED] If $P$ has prime order $r$, then every $nP$ with
  $1\le n<r$ generates the same subgroup as $P$.
- [PROVED] For any endomorphism subring $R$, one also has
  $\operatorname{Ann}_R(nP)=\operatorname{Ann}_R(P)$: multiplication by $n$
  is an automorphism of the order-$r$ subgroup, so
  $n\alpha(P)=0$ if and only if $\alpha(P)=0$.
- [PROVED] Hence every label determined only by the annihilator, cyclic
  kernel, or kernel-isogeny quotient is constant on the nonzero source points
  and cannot be an injective homomorphism for odd $r$.
- [EMPIRICAL: 8 ordinary j=1728 curves, 13 <= p <= 421, 368 nonzero points]
  Complete enumeration found one annihilator label, kernel, and canonical
  Velu quotient per subgroup; see
  `data/probe_cm_class_targets_full_20260702.csv`.
- [CITED] The standard CM class-group construction indeed runs in the other
  direction: an ideal $\mathfrak a$ defines a kernel $E[\mathfrak a]$ and an
  oriented quotient curve (Castryck--Houben--Vercauteren--Wesolowski 2022,
  Section 2.2).

### Size of the curve's own endomorphism class group

- [CITED] The ring class-number formula expresses $h(f^2d_K)$ as
  $h(d_K)f$ times local factors and divided by a unit index (Cox 2013,
  Theorem 7.24).
- [CITED] The imaginary-quadratic analytic class-number formula expresses
  $h(d_K)$ through $\sqrt{|d_K|}L(1,\chi_{d_K})$ (Milne 1997,
  Chapter VI, Section 2).
- [PROVED] Splitting the series for $L(1,\chi)$ into blocks of length
  $|d_K|$ and using the zero character sum gives
  $|L(1,\chi)|\le\log|d_K|+2$; A003 contains the complete error bound.
- [PROVED] Consequently every imaginary quadratic order of discriminant
  $\Delta$ satisfies
  $$h(\Delta)\le\frac{3}{\pi}\sqrt{|\Delta|}
  (\log|\Delta|+2)^2.$$
- [PROVED] Since the endomorphism-order discriminant of an ordinary curve over
  $\mathbb F_q$ divides the Frobenius discriminant $t^2-4q$, its class number
  is at most
  $$\frac{6}{\pi}\sqrt q(\log(4q)+2)^2.$$
- [PROVED] This bound is below $q/2$ for every $q\ge2^{21}$; therefore it
  excludes an order-$r$ image in the curve's own endomorphism class group when
  $r\ge q/2$.
- [PROVED] This does not exclude a separately constructed order with much
  larger discriminant or the regime $r\ll q$.

## SG-10 - ray classes and arithmetic class pairings

- [CITED] Milne's ray-class exact sequence and order formula
  (Milne 1997, Theorem V.1.5) give, for odd $r$,
  $$|\operatorname{Cl}_{r}(\mathbb Q(i))|=
  \begin{cases}(r-1)^2/4&r\equiv1\pmod4,\\(r^2-1)/4&r\equiv3\pmod4,
  \end{cases}$$
  so the modulus-$r$ group cannot receive an injective order-$r$ image.
- [PROVED] At modulus $r^2$, the ray class number has $r$-adic valuation 2,
  and the congruence subgroup
  $(1+r\mathbb Z[i])/(1+r^2\mathbb Z[i])$ is additively isomorphic to
  $\mathbb Z[i]/r\mathbb Z[i]$ via $1+rz\mapsto z$.
- [PROVED] The order-$r$ real line therefore has an immediate target DLP, but
  the formula $nP\mapsto1+rn$ is only an abstract homomorphism: evaluating it
  from $nP$ is the source DLP.
- [PROVED] Principal units $1+ra$ act on a cyclic $r^2$-level lift by
  multiplication and preserve its image under multiplication by $r$; they
  parameterize $r$ lifts of one source point, not the $r$ source points.
- [PROVED] Full level rescaling reaches the nonzero multiples $nP$ through
  $(\mathbb Z/r\mathbb Z)^\times$, a multiplicative group of order $r-1$;
  it omits the identity and does not respect the additive source law.
- [CITED] Genuine point-to-ideal-class homomorphisms exist over number fields
  (Buell--Call 2016), correcting an overbroad negative intuition about class
  groups; with a torsion argument fixed, their construction is explicitly
  related to the Weil-descent pairing.
- [PROVED] Direct specialization of the arithmetic ideal-class pairing to
  $\operatorname{Spec}\mathbb F_q$ or to a local discrete valuation ring has
  trivial target because the Picard group of a field or local PID is zero.
- [CONJECTURE] A global lift with polynomial total encoding length cannot turn
  this arithmetic pairing into a finite-field transfer; a concrete lift and
  evaluator meeting SG-01 would refute the conjecture.
- [CITED] Parent's explicit torsion bound gives
  $r\le65(3d-1)(2d)^6$ for an order-$r\ge5$ point rational over a degree-$d$
  number field (Parent 1999, Theorem 1.2).
- [PROVED] Thus $d>(r/12480)^{1/7}=\exp(\Omega(\log r))$, so a standard dense
  number-field encoding and its arithmetic have exponential size in the
  source security parameter and fail SG-01 before the pairing is evaluated.
- [CONJECTURE] Parent's degree bound does not by itself exclude a hypothetical
  succinct implicit representation that also performs every required global
  valuation and ideal operation in polynomial time; constructing one is a
  concrete falsifier.

## SG-14 - generic-source impossibility

### Prior-art reconciliation

- [CITED] Koblitz--Menezes (2007) explains the generic-group model as a model
  that excludes algorithms exploiting special features of a concrete group
  representation, and separately warns that coordinates and implementation
  details can expose behavior absent from the generic abstraction.
- [PROVED] SG-14's conceptual generic-versus-coordinate boundary therefore
  overlaps Koblitz--Menezes. The P1.5-specific contribution is the exact
  counted setup/evaluator/target-DLP composition, the exclusion of
  encoding-dependent advice, and the expected-query truncation below.

### Theorem

- [PROVED] In the classical random-encoding generic-group model, no transfer
  satisfying SG-01 can use only generic source addition, inversion, identity,
  and equality together with $r^{o(1)}$ expected source-oracle calls.

### Proof and accounting

- [PROVED] Given a generic challenge $(P,Q=xP)$, run the counted transfer setup
  and compute $h=\phi(P)$ and $y=\phi(Q)$.  Homomorphism gives $y=xh$, while
  injectivity makes $h$ have order $r$, so the target DLP algorithm returns the
  source logarithm $x$.
- [PROVED] If the composition has expected source-query count
  $q(r)=r^{o(1)}$ and fixed success $\delta>0$, truncation after
  $4q(r)/\delta$ queries retains success at least $3\delta/4$ by Markov's
  inequality.
- [CITED] Shoup's random-encoding theorem bounds the success of a classical
  prime-order generic DLP algorithm making $m$ queries by $O(m^2/r)$.
  Substituting $m=r^{o(1)}$ makes this $r^{-1+o(1)}$, a contradiction.
- [PROVED] Arbitrary target computation and preprocessing are harmless in this
  proof because they become local computation after composition.  What is not
  allowed is encoding-dependent advice or an uncounted oracle that turns a
  random source handle into coordinates, a lift, a divisor, or a pairing
  value.

### Exact boundary

- [CITED] Anomalous transfer crosses the boundary through coordinates and a
  $p$-adic or dual-number lift; MOV/Frey--Ruck crosses it through line
  functions, an auxiliary torsion point, and extension-field arithmetic; Weil
  descent crosses it through equations, Frobenius, a field basis, and divisor
  maps.
- [PROVED] Thus every qualifying transfer must exploit a
  representation-specific source operation.  This is a complete black-box
  classification, not an unrestricted classification of coordinate formulas.
- [PROVED] Generic class, ideal, or ray arithmetic on the target cannot by
  itself evade the theorem.  A surviving point-to-class candidate must expose
  the concrete source operation that extracts scalar-sensitive information.

## SG-15 - low-degree rational-map obstruction

### Theorem

- [PROVED] Let $C=\langle P\rangle\subset E(k)$ have prime order $r$, let
  $H/k$ be affine, fix a faithful representation $H\hookrightarrow GL_s$, and
  let $F:E\dashrightarrow H$ be defined on $C$.  Suppose a common effective
  pole divisor of all matrix entries has degree $D$.  If $F|_C$ is a
  homomorphism and $r>2D$, then $F$ extends to a global algebraic-group
  homomorphism and is trivial.  Thus every injective rational transfer into an
  affine target has $D\ge r/2$.

### Proof mechanism

- [PROVED] For the generator $P$, each entry of
  $F(X+P)-F(X)F(P)$ has pole degree at most $2D$ and has the $r$ points of $C$
  as zeros.  If $r>2D$, the defect vanishes identically in $X$.
- [PROVED] Right multiplication by the invertible constant $F(P)$ preserves
  the largest local pole order among the entries.  The least common pole
  divisor is therefore invariant under translation by $P$.
- [PROVED] Every translation orbit has $r$ geometric points, while the pole
  divisor has degree $D<r$; it is empty.  The resulting morphism $E\to H$ is
  constant because $E$ is proper and geometrically connected and $H$ is
  affine.  Its value at zero is the identity.

### Consequences and limits

- [PROVED] Coordinate access alone is insufficient at low geometric degree:
  any nontrivial affine transfer formula has degree exponential in the input
  length $\log r$.
- [CITED] Pairing functions have divisors of size $\Theta(r)$, so Miller's
  multiplicative transfer sits beyond the degree threshold even though an
  addition chain evaluates it in polynomial time.
- [PROVED] The result does not cover proper targets, non-rational lift
  operations, rational circuits whose degree grows at least linearly in $r$,
  or abstract class groups lacking a polynomial-size algebraic embedding.

## SG-16 - rational-circuit depth obstruction

- [PROVED] For rational functions of pole degree at most $a$ and $b$, every
  binary $+,-,\times,/$ result has pole degree at most $a+b$; for a quotient,
  zeros of the denominator have the same total degree as its poles.
- [PROVED] A depth-$d$ branch-free rational circuit whose base functions have
  pole degree at most $D_0$ therefore gives each output pole degree at most
  $2^dD_0$.  With $M$ matrix-entry outputs, their summed pole divisor has
  degree at most $M2^dD_0$.
- [PROVED] Combining this with SG-15 yields
  $$d\ge\log_2 r-\log_2(2MD_0).$$
  If $MD_0=(\log r)^{O(1)}$ and $n=\lceil\log_2r\rceil$, then
  $d\ge n-O(\log n)$.
- [CITED] Miller's straight-line-program construction was designed precisely
  to keep the program short while the expanded rational function is
  exponentially large (Miller 1986/2024).
- [CITED] The $\Theta(\log r)$ dependent Miller chain and its
  $\Theta(r)$-degree function sit at the scale forced by the theorem.
- [PROVED] The validated anomalous evaluator leaves the rational base-curve
  model through its lift, but its multiplication-by-$p$ step also uses a
  $\Theta(\log p)$ dependent double-and-add chain.

## SG-17 - piecewise-rational tradeoff

- [PROVED] Suppose an affine-target evaluator partitions the order-$r$ source
  into $B$ branches and agrees on every branch with a rational map whose matrix
  entries have common pole degree at most $D$.  Then injectivity forces
  $$\left\lceil\frac rB\right\rceil
  \left(\left\lceil\frac rB\right\rceil-1\right)\le2D(r-1),$$
  and consequently
  $$\max(1,D)B^2\ge r/4.$$
- [PROVED] For a largest branch $S$, put
  $R(t)=|\{x\in S:x+t\in S\}|$.  The exact identity
  $\sum_{t\ne0}R(t)=|S|(|S|-1)$ supplies a repeated nonzero difference.
- [PROVED] If $R(t)>2D$, the zero bound forces
  $F_S(X+t)=\phi(t)F_S(X)$ globally.  Translation invariance then removes all
  poles, makes $F_S$ constant, and contradicts injectivity.  Hence every
  $R(t)\le2D$, giving the displayed exact inequality.
- [PROVED] The earlier triple-color proof genuinely gives
  $\max(1,D)B^3\ge r/4$, but the same-branch argument is stronger and works
  for arbitrary adversarial partitions.
- [PROVED] If $b$ binary tests give $B\le2^b$ branches and every branch has a
  depth-$d$ rational circuit with $M$ outputs and base pole degree $D_0$, then
  $$d+2b\ge\log_2r-\log_2(4MD_0).$$
- [PROVED] Thus even branching cannot make the representation-specific affine
  work sublinear in $\log r$ unless it creates exponentially many pieces or
  leaves the rational model.
- [PROVED] This is an algebraic-depth statement in an explicit rational
  decision-tree model, not a lower bound against arbitrary polynomial-time
  bit programs.  Linear depth remains polynomial time.

## SG-18 - proper rational targets

### Theorem

- [PROVED] Let $k$ be perfect, let $H/k$ be a smooth proper algebraic group,
  and let $F:E\dashrightarrow H$ be rational and defined at zero.  If
  $F(0)=1_H$, then $F$ extends to a global algebraic-group homomorphism.
  Thus the conclusion holds in particular when $F$ is homomorphic on
  $C=\langle P\rangle$.  Its image is trivial or an elliptic abelian
  subvariety isogenous to $E$.

### Proof and interpretation

- [CITED] A rational map from a normal curve to a proper variety extends
  uniquely to a morphism (Stacks Project, Lemma 53.2.2).
- [PROVED] Since $F|_C$ preserves the identity and $E$ is connected, the
  extended image lies in the identity component $H^0$ and sends $0_E$ to
  $0_{H^0}$.
- [CITED] The component $H^0$ is an abelian variety, and every morphism of
  abelian varieties preserving zero is a homomorphism (Milne, *Abelian
  Varieties*, Corollary 1.2).
- [PROVED] SG-07 then gives the trivial-or-elliptic-isogenous image
  classification.
- [PROVED] Therefore a rational Jacobian transfer is structurally a global
  elliptic embedding/isogeny into the ambient Jacobian.  It can still qualify
  when the ambient representation has a subexponential DLP algorithm; the
  algorithmic advantage comes from the ambient target, not a new point-map
  type.

## SG-19 - synthesized restricted classification

### Theorem

- [PROVED] Let $C=\langle P\rangle$ have prime order $r$, and consider a
  classical SG-01 transfer family.  The following restricted classification
  holds.
  1. If the source is available only through a random generic encoding and
     setup/evaluation use $r^{o(1)}$ source queries, no transfer exists.
  2. If the target is a smooth proper algebraic group and the evaluator uses
     fewer than $r$ rational branches, it is the restriction of one global
     homomorphism with trivial or elliptic-isogenous image.
  3. If the evaluator is piecewise rational into an affine algebraic group,
     using $B$ branches of common pole degree at most $D$, injectivity requires
     $\max(1,D)B^2\ge r/4$, and in fact satisfies the exact overlap inequality
     recorded in SG-17.
  4. In the third case, a rational circuit with arithmetic depth $d$, at most
     $b$ binary branch decisions, $M$ output coordinates, and base pole degree
     $D_0$ satisfies
     $$d+2b\ge\log_2r-\log_2(4MD_0).$$
  5. For one rational map into any smooth algebraic group, the abelian
     Chevalley quotient is global; if the remaining affine-kernel defect has
     pole degree below $r$ in each controlled fibre, the whole map is global
     with trivial or elliptic-isogenous image.

### Placement of the known transfers

- [CITED] The anomalous transfer is representation-specific and non-rational
  on the base curve: it uses a $p$-adic or dual-number lift and a connecting or
  formal-log map.  Its validated multiplication-by-$p$ computation has
  $\Theta(\log p)$ dependent group steps.
- [CITED] The pairing transfer is representation-specific and affine-rational
  of geometric degree $\Theta(r)$, compressed by a
  $\Theta(\log r)$ Miller chain.  It occupies the high-degree/depth exit left
  by items 3 and 4.
- [CITED] Qualifying Weil descent lies on the proper/geometric side.  A single
  rational map into a Jacobian has elliptic-isogenous image, while the ambient
  Jacobian or restriction-of-scalars representation supplies the different
  DLP algorithm.

### Residual class

- [PROVED] A structurally new transfer must escape the generic theorem and
  therefore identify a concrete source operation unavailable from random
  handles.
- [PROVED] If its target is affine and its evaluator is piecewise rational, it
  must pay exponential geometric degree, exponentially many pieces, or a
  linear-in-$\log r$ arithmetic/branch-depth budget.
- [PROVED] If its target is a smooth proper algebraic group and its evaluator
  has fewer than $r$ rational branches, its image is not a new algebraic-group
  type: it is elliptic and isogenous to the source.
- [CONJECTURE] The remaining unclassified cases are non-rational operations
  such as lifts or valuations, high-depth/high-degree affine formulas or
  mixed-target defects other than pairings, succinct abstract targets without
  a polynomial-size algebraic presentation, and target DLP algorithms
  exploiting such representations.  One explicit family satisfying SG-01 and
  falling outside the three known mechanisms refutes the negative search
  assessment.

## Current answer

- [PROVED] The unrestricted classification requested in the problem is not
  proved here; the deliverable is partial rather than a claimed solution.
- [CITED] Under the adopted broad definition, Weil descent supplies a known
  third geometric target family in those instances where its homomorphism and
  target complexity satisfy SG-01.
- [PROVED] Within global algebraic-group homomorphisms, SG-07 is a complete
  structural classification: affine targets give nothing, and every
  nontrivial image remains elliptic and isogenous to the source.
- [PROVED] Within the natural CM-order branch, annihilator/kernel constructions
  are excluded, large prime subgroups outgrow the endomorphism class group,
  and the standard ray-level action moves the wrong objects. A025 nevertheless
  gives a valid ordinary ring-class target by transporting the existing
  pairing character through a conductor quotient.
- [PROVED] Every purely generic-source construction is excluded by Shoup's
  lower bound. A025 exposes exactly the required representation-specific
  operation: the nondegenerate degree-two pairing.
- [PROVED] Every affine piecewise-rational construction satisfies the explicit
  degree/branch/depth bounds in SG-15--SG-17, while every single rational
  proper-target construction is a global homomorphism with elliptic-isogenous
  image by SG-18.
- [PROVED] These results give a rigorous restricted classification and explain
  how the three established mechanisms cross its boundaries, but they do not
  classify arbitrary non-rational polynomial-time evaluators or all groups
  with subexponential DLP algorithms.

## SG-20 - piecewise rational proper targets

- [PROVED] Let $H/k$ be a smooth proper algebraic group and let a homomorphism
  $\phi:C\to H(k)$ agree on each of $B<r$ branch sets with a rational map
  $F_b:E\dashrightarrow H$.  Then $\phi$ is the restriction of one global
  algebraic-group homomorphism $E\to H^0$.
- [PROVED] Some branch contains distinct $X,Y$.  Properness extends its map;
  after translating its connected image component to $H^0$, rigidity writes
  it as $F_b(Z)=t\alpha(Z)$.  Therefore
  $$\phi(X-Y)=F_b(X)F_b(Y)^{-1}
  =t\alpha(X-Y)t^{-1}.$$
  The conjugate $\beta=\operatorname{Int}(t)\circ\alpha$ is a global
  homomorphism, and since $X-Y$ generates the prime-order group,
  $\phi=\beta|_C$ everywhere.
- [PROVED] An injective evaluator therefore has elliptic-isogenous image by
  SG-07.  Fewer than $r$ rational formulas cannot produce a structurally new
  proper-target map; explicitly storing $r$ formulas would violate SG-01's
  polynomial setup budget.

## SG-21 - mixed algebraic targets

- [CITED] For the identity component of a smooth algebraic group, Chevalley's
  theorem gives
  $$1\to L\to H^0\mathop{\longrightarrow}^{\pi}A\to1$$
  with $L$ connected affine and $A$ an abelian variety (Milne 2022).
- [PROVED] For a single rational evaluator $F:E\dashrightarrow H^0$ that is a
  homomorphism on $C$, the proper projection $\pi F$ is a global homomorphism
  $\alpha:E\to A$ by SG-18.
- [PROVED] In the pullback group $H_\alpha=E\times_AH^0$, the rational section
  $s(X)=(X,F(X))$ has an affine-kernel defect
  $$c(X,Y)=s(X+Y)(s(X)s(Y))^{-1}\in L$$
  that equals the identity on $C^2$.
- [PROVED] It is sufficient that the entries of a faithful linear
  representation of $c-I$ have pole degree $D<r$ after restriction to every
  fibre $E_X\times\{Q\}$ for $Q\in C$, and have generic pole degree $D<r$ in
  $Y$ over $\bar k(E_X)$.  These are the exact special and generic bounds used
  by the two zero counts; a generic displayed bidegree alone does not control
  vertical denominators.
- [PROVED] The resulting rational group homomorphism extends across its poles
  by translation, uniqueness gives descent to $k$, and SG-07 gives trivial or
  elliptic-isogenous image.
- [PROVED] Precisely, every non-global rational mixed-target transfer violates
  at least one stated fibrewise degree bound for the fixed faithful
  representation.  There is no representation-free degree conclusion.

## SG-22 - class-target base taxonomy

- [PROVED] Every invertible module over a local ring is free of rank one.
  Since a finite commutative ring is a finite product of Artinian local rings,
  every finite or local base has trivial Picard group.
- [PROVED] For a smooth projective curve $C/\mathbb F_q$ with rational point
  $\infty$ and $A=\Gamma(C\setminus\{\infty\},\mathcal O_C)$,
  $$\operatorname{Cl}(A)\simeq
  \operatorname{Pic}(C)/\mathbb Z[\infty]
  \simeq\operatorname{Pic}^0(C).$$
- [CITED] Milne's Jacobian Theorem 1.1 identifies
  $\operatorname{Pic}^0(C)$ with $J_C(\mathbb F_q)$ in this pointed case, and
  Section 9 identifies modulus class groups with generalized Jacobians.
- [PROVED] Thus global function-field ideal-class targets are ordinary or
  generalized Jacobian targets already covered by the proper/mixed geometric
  branches.
- [PROVED] A genuinely distinct class target must be a global number-field
  order.  A005--A006 exclude finite/local specialization and standard dense
  global torsion lifts.
- [PROVED] A025 realizes the number-field branch without a dense global lift:
  a pairing value in $\mathbb F_{p^2}^{\times}$ maps through the conductor
  exact sequence to an ideal class of $\mathbb Z+p\mathbb Z[i]$. This is the
  conductor-local control branch.
- [PROVED] A028 handles both the conductor and maximal components for every
  explicit imaginary-quadratic order. The maximal component is exposed by a
  Kummer power-residue character, with uniform short-prime setup under the
  standing GRH convention.

## SG-23 - evaluator sandwich

- [CITED] Verheul (2001/2004) proves that an efficient reverse homomorphism
  from an XTR subgroup to a paired supersingular elliptic subgroup makes
  Diffie--Hellman efficient in both groups; Moody (2008/2009) generalizes the
  consequence using computable pairings and distortion maps.
- [PROVED] The hard-problem-consequence strategy in SG-23 therefore overlaps
  the Verheul/Moody line. The inequalities below apply to any represented
  target with a target-DLP algorithm and do not require the special
  pairing/distortion structure of those papers.

- [PROVED] For a nonzero homomorphism $\phi:C\to G$ with
  $h=\phi(P)$, one has $\phi(xP)=h^x$ and $h$ has order $r$.
- [PROVED] Source DLP followed by target exponentiation gives
  $$T_{\rm eval}\le T_{\rm src}+O(\log r)T_G,$$
  while evaluation followed by target DLP gives
  $$T_{\rm src}\le T_{\rm eval}+T_{\rm tgt}+(\log r)^{O(1)}.$$
- [PROVED] Hence, with a target-DLP oracle, point-to-class evaluation and
  source DLP are polynomial-time Turing equivalent.  A polynomial evaluator
  plus an $\exp(o(\log r))$ target DLP is precisely a subexponential source
  ECDLP reduction.
- [PROVED] This does not contradict a proved concrete ECDLP lower bound - no
  such bound is available in the unrestricted coordinate model.  It shows why
  target class-number arguments alone could not finish Q004: the missing
  ingredient was a concrete cross-representation computation. A025 later
  supplies it from the pairing residue through the conductor exact sequence.

## SG-25 - class-target discriminant budget

- [PROVED] If an imaginary-quadratic order of discriminant $\Delta$ contains
  an order-$r$ ideal class, A003's class-number bound forces, with
  $n=\lceil\log_2r\rceil$ and $B=\log_2|\Delta|$,
  $$B\ge2n-O(\log n).$$
- [CONDITIONAL: Extended Riemann Hypothesis and factor-base decomposition of
  represented target inputs] The Hafner--McCurley target route costs
  $\exp(O(\sqrt{B\log B}))$ after changing only constant log bases.
- [PROVED] That cost is $\exp(o(n))$ exactly when $B\log B=o(n^2)$, so the
  checked target route requires
  $$2n-O(\log n)\le B=o(n^2/\log n).$$
- [PROVED] Polynomial discriminant bit length alone is insufficient: the
  actual growth exponent must stay inside this window.  A valid A001 family
  must also construct a known exact order-$r$ class and a polynomial-time
  evaluator, neither of which follows from the size window.

## SG-26 - direct reduction of the Buell formula

- [CITED] On an actual integral point
  $(a,b)$ of $y^2=4x(x^2+Bx+C)+\mathcal D$, the Buell point-to-form formula
  produces
  $$[aX^2+bXY+(a^2+Ba+C)Y^2]$$
  of fixed discriminant $\mathcal D$ (Buell--Call 2016, Equation (1) and the
  cited Buell construction).
- [PROVED] Canonical integer representatives of a finite-field point satisfy
  only
  $$b^2-4a(a^2+Ba+C)=\mathcal D+k_Qp.$$
  Unless $k_Q=0$, the form belongs to a different quadratic order, so the
  outputs do not share a target group.
- [EMPIRICAL: 10 nonsingular reductions, 23 <= p <= 59, 13 <= r <= 37,
  218 nonzero points] Complete enumeration produced 218 distinct lifted
  discriminants and only two equal to the model discriminant; 195 were
  negative and 199 coefficient triples were primitive.  See
  `code/probe_buell_reduction.py` and
  `data/probe_buell_reduction_full_20260710.csv`.
- [PROVED] Altering the representatives to restore the exact discriminant
  requires an actual integral/number-field point lift coherent with addition,
  returning to A006 rather than giving a direct residue-coordinate evaluator.

## SG-24 - checked literature boundary

- [CITED] Buell (1977), Soleng (1994), Buell--Call (2016), Gillibert (2018),
  and Blum--Choi--Hoey--Iskander--Lakein--Martinez (2022) give
  point-to-class homomorphisms or specializations whose source points are
  rational or algebraic over number fields.
- [CITED] Gillibert identifies the Buell--Soleng morphisms with
  line-bundle specialization and the Mazur--Tate class group pairing.
- [CITED] The standard finite-field CM construction has the reverse direction:
  an ideal class acts on an oriented elliptic curve.
- [EMPIRICAL: bounded literature search on 2026-07-10] No checked arXiv, AMS,
  journal-metadata, Buell--Call-reference, or Gillibert-reference result gave
  a direct map from $E(\mathbb F_q)[r]$ to one fixed number-field class group.
- [PROVED] The last sentence is a documented search result, not a proof of
  nonexistence.  The exact residual remains the cross-characteristic evaluator
  specified in A001 and A018.

## SG-27 - exact order versus succinct target construction

- [PROVED] For every prime $r\ge3$, the order
  $\mathcal O_r=\mathbb Z[(1+\sqrt{1-4\cdot2^r})/2]$ contains the invertible
  ideal $\mathfrak a=(2,(1+\sqrt{1-4\cdot2^r})/2)$ of exact class order $r$;
  A019 gives the complete ideal-power and nonprincipality proof.
- [PROVED] Its discriminant has $\Theta(r)$ bits, exponential in
  $n=\lceil\log_2r\rceil$, so the construction fails SG-01 before evaluation.
- [PROVED] Before A025, Q004 contained two logically separate residual tasks:
  a certified succinct order-$r$ class and a nonzero point evaluator. A025
  solves them together for a compatible pairing family; solving only the
  target-only SG-30 problem would still not supply an evaluator by itself.

## SG-29 - succinct target census

- [EMPIRICAL: every negative order discriminant with $|\Delta|\le200000$]
  Batch reduced-form enumeration reproduced seven known class numbers and the
  shared enumerator; see `code/probe_exact_order_targets.py`.
- [EMPIRICAL: 13 primes $3\le r\le43$] The least discriminant whose class
  number is divisible by $r$ always had $h(\Delta)=r$, and
  $0.684711\le|\Delta|/r^2\le2.555556$.  A nonprincipal reduced form in each
  row therefore has exact order $r$.
- [PROVED] The finite census demonstrates small-target existence only.  Its
  exhaustive search does not provide a uniform polynomial-time construction
  as $r$ grows, so it does not solve the target-only SG-30 problem. At that
  stage the evaluator was also open; A025 later supplies a compatible
  pairing-derived control without converting this census into a uniform
  constructor or closing novelty-grade Q004.

## SG-28 - prescribed-order construction audit

- [CITED] Lim (2016) gives infinitely many imaginary quadratic class groups
  with an element of exact squarefree odd order $n$, using congruence choices
  and $n$-th-power discriminant equations.
- [CITED] Ouyang--Song (2024) and Chakraborty--Hoque (2020) give further
  families based on $x^2-cy^n$; the Ouyang--Song threshold depends
  ineffectively on fixed $(x,n)$.
- [EMPIRICAL: bounded primary-source search on 2026-07-10] No checked theorem
  supplied a uniform polynomial-bit discriminant and exact-order certificate
  as $n$ varies.
- [PROVED] This does not prove such a constructor impossible.  It leaves
  SG-30 for ordinary class groups, while A004 already supplies a succinct ray
  target and shows that target construction alone does not solve Q004.

## SG-30 - uniform succinct exact-order ring-class target

- [PROVED] A029 closes SG-30 unconditionally. For every odd prime \(r\), set
  \[
  \mathcal O_r=\mathbb Z+r^2\mathbb Z[i],
  \qquad \Delta_r=-4r^4.
  \]
  The conductor residue \(1+ri\bmod r^2\) has exact order \(r\) modulo
  rational and Gaussian units: its \(r\)-th power is \(1\bmod r^2\), while
  it is nontrivial because both coordinates are nonzero.
- [PROVED] Contraction gives the primitive form
  \[
  [1+r^2,2r^3,r^4].
  \]
  One shift by \(-r\) and one proper swap reduce it to the closed canonical
  form
  \[
  [r^2,2r,r^2+1].
  \]
- [PROVED] The target has
  \[
  \log_2|\Delta_r|=2+4\log_2r=\Theta(\log r),
  \]
  hence lies inside the SG-25 window. Construction and certification are
  deterministic polynomial time and unconditional.
- [PROVED] The complete subgroup is
  \(a\mapsto[1+rai]\), with additive target logarithm
  \(1+rai\mapsto a\bmod r\). Thus this is a target-only theorem, not a new
  source transfer mechanism.
- [CITED] The conductor exact sequence and effective inverse are classical.
  A026 already contained the general wild form; A029's contribution is
  recognizing that no maximality or source-compatibility condition belongs
  to SG-30, and extracting the uniform closed reduced family.
- [EMPIRICAL: 15 primes \(3\le r\le10007\), discriminants at most 56 bits]
  `code/construct_sg30_ring_class_target.py` validates the exact-order
  certificate, closed reduction, class-number formula, and SG-25 bit bound.

## SG-31 - ray principal-unit evaluator equivalence

- [PROVED] The explicit logarithm
  $\theta(1+rz)=z\bmod r$ identifies the modulus-$r^2$ Gaussian principal
  units with the two-dimensional additive group over $\mathbb F_r$.
- [PROVED] For any nonzero homomorphism $\psi:\langle P\rangle\to U_r$, choose
  a nonzero coordinate of $u=\theta(\psi(P))$.  On $Q=xP$, the same coordinate
  of $\theta(\psi(Q))$ is $xu_j$, so division by $u_j$ returns $x$.
- [PROVED] Thus a ray principal-unit evaluator and source DLP are
  polynomial-time Turing equivalent.  The ray branch can qualify only by
  yielding a polynomial-time source ECDLP, not merely a subexponential one.
- [PROVED] The ray branch itself remains transparent. A025 supplies a
  different conductor quotient whose order-$r$ DLP is equivalent to the
  established finite-field pairing target, not the additive ray
  principal-unit logarithm; it is a control, not novelty-grade closure.

## SG-32 - finite valuation/factor-base evaluator model

- [PROVED] A024 fixes one ordinary-class output encoding: the unique canonical
  reduced primitive positive-definite binary quadratic form of a supplied
  negative discriminant $\Delta$, with proper Gauss composition.
- [PROVED] Its valuation-mediated factor-base (VFB) model permits canonical
  integer coordinate lifts, exact integer arithmetic, finitely many
  valuations and binary comparisons, and target operations on fixed setup
  forms. Raw lifted coordinates may affect the target only through the
  valuation/comparison transcript; direct raw-coordinate form synthesis and
  raw-indexed target tables are explicitly outside the model.
- [PROVED] If a VFB evaluator of a nonzero homomorphism makes at most $C$
  binary comparisons and valuation operands have bit-length bounds $h_j$,
  then injectivity and transcript counting give
  $$
  C+\sum_j\log_2(h_j+1)\ge\log_2r.
  $$
  In particular, polynomial-height operands and $C=o(\log r)$ require
  $\Omega(\log r/\log\log r)$ valuation observations.
- [CITED] The Verheul/Moody consequence template would turn such an evaluator
  into a Diffie--Hellman algorithm if the target also supplied an efficient
  nondegenerate pairing, distortion map, and tractable paired-target
  logarithm. No such package is available for the fixed ordinary reduced-form
  target; odd-order classes are invisible to exponent-two genus characters.
- [PROVED] SG-32 is complete at the requested one-model scope, but A024 is
  only a low-observation lower bound. A025 later supplies an explicit
  MAKEFORM-style evaluator outside VFB through the known pairing mechanism.
  Polynomial-length VFB programs remain outside A024. A029 later closes the
  independent target-only SG-30 problem.

## SG-33 - pairing-to-ordinary-ring-class control

- [CITED] For every odd prime $r$, CRT plus Linnik--Xylouris supplies a prime
  $p\equiv3\pmod4$, $p\equiv-1\pmod r$ with $\log p=O(\log r)$.
- [CITED] On $E_p:y^2=x^3+x$, the distortion map
  $\psi(x,y)=(-x,iy)$ makes the degree-two pairing
  $Q\mapsto e_r(Q,\psi(P))$ a nonzero character into
  $\mu_r\subset\mathbb F_{p^2}^{\times}$.
- [CITED] The conductor exact sequence gives
  $$
  \operatorname{Pic}(\mathbb Z+p\mathbb Z[i])
  \cong
  \mathbb F_{p^2}^{\times}/
  \bigl(\mathbb F_p^\times\langle i\rangle\bigr),
  \qquad h(-4p^2)=\frac{p+1}{2}.
  $$
- [PROVED] The quotient is injective on $\mu_r$. For projective pairing
  residue $1+ti$, the image is the ordinary ideal class represented by
  $$
  (1+t^2,\ 2pt,\ p^2),
  $$
  followed by canonical Gauss reduction. This is a polynomial-time
  fixed-discriminant evaluator.
- [PROVED] From a reduced form $(A,B,C)$, a Gaussian gcd of
  $A$ and $-B/2+pi$, followed by exponentiation by $2(p-1)$ modulo $p$,
  returns an injective finite-field torus encoding on the order-$r$ image.
  The target DLP is therefore the same accepted subexponential DLP as the
  original pairing target.
- [EMPIRICAL: complete $p=43,211,331$ class groups and source
  $r=11,53,83$] A025's validation enumerates all $(p+1)/2$ reduced classes,
  checks the two-to-one conductor quotient, obtains $r$ distinct transfer
  images, and recovers every seeded logarithm.
- [PROVED] The construction is not structurally new: it is the pairing
  transfer followed by an ordinary ring-class presentation. It is retained as
  the exact control case and does not close novelty-grade Q004.

## SG-34 - novelty-grade Q004 reopening

- [PROVED] A026 fixes the new closure contract: either construct a direct
  ordinary class transfer outside local, pairing, and geometric mechanisms,
  or prove a substantially broader literature-audited factorization/
  impossibility theorem.
- [PROVED] For
  $\mathcal O_f=\mathbb Z+f\mathcal O_K$, the conductor exact sequence gives a
  first dichotomy for every prime-order transfer: its projection to
  $\operatorname{Pic}(\mathcal O_K)$ is injective, or its entire image lies
  in the conductor kernel.
- [PROVED] The conductor kernel decomposes by CRT into local factors of order
  $\ell^{e-1}(\ell-\chi_K(\ell))$. Its prime-order pieces are additive
  principal-unit lines when $r=\ell$ and split or inert multiplicative tori
  when $r\ne\ell$.
- [CITED] A026's proposed computational strengthening is also prior art.
  Hühnlein--Takagi (1999) reduce DLP in totally nonmaximal class-number-one
  orders to finite-field DLP. Castagnos--Laguillaumie (2009), Lemma 1, give
  the effective conductor-kernel isomorphism for general conductor, including
  the inverse from a reduced kernel ideal by coprime replacement, extension,
  principalization, and reduction modulo the conductor. Kopp--Lagarias (2024)
  place the exact sequence in a general order/ray-class framework.
- [PROVED] The all-odd-conductor Gaussian shear/gcd inverse and the explicit
  conductor-\(p^2\) wild forms are correct executable specializations. They
  are controls, not the required discovery.
- [PROVED] The remaining question is source-side. A027 treats all evaluators,
  including arbitrary direct `MAKEFORM`, when target and source share the CM
  field and the conductor is supported on the intrinsic primes \(p,r\).

## SG-35 - intrinsic-conductor source theorem

- [PROVED] Let \(E/\mathbb F_p\) be ordinary with trace \(t\), let \(P\) have
  odd prime order \(r\ne p\), put
  \(K=\operatorname{End}(E)\otimes\mathbb Q\), and assume
  \(r>h(\mathcal O_K)\) and \(r>2\sqrt p+2\).
- [PROVED] For a target
  \(\mathcal O_f=\mathbb Z+f\mathcal O_K\), the maximal-order projection of
  any order-\(r\) image is zero. If \(f\) is supported on \(\{p,r\}\), a
  nonzero local projection must occur at one of those two primes.
- [PROVED] The \(r\)-local principal-unit quotient has a one-dimensional
  explicit logarithm over \(\mathbb F_r\), in both unramified and ramified
  cases. Thus a nonzero evaluator in this branch recovers the source scalar
  in polynomial time.
- [PROVED] Since ordinary \(p\) splits in \(K\), the \(p\)-local torus has
  order \(p^{a-1}(p-1)\). A nonzero order-\(r\) projection forces
  \(r\mid p-1\). Together with \(r\mid p+1-t\) and Hasse,
  \(r>2\sqrt p+2\) forces \(t=2\). Also \(r^2>\#E(\mathbb F_p)\), so the
  nondegenerate Tate--Lichtenbaum/Frey--Rück pairing places the source in the
  embedding-degree-one regime.
- [PROVED] Any residual same-field counterexample must contain an external
  conductor prime \(\ell\notin\{p,r\}\) satisfying
  \(r\mid\ell-\chi_K(\ell)\). Hence \(\ell\ge2r+1\) when split and
  \(\ell\ge2r-1\) when inert; a ramified \(\ell\ne r\) cannot carry the
  image.
- [EMPIRICAL: complete \(p=101,211,401\) wild images, all conductor-43 tame
  residues, and three trace-two arithmetic fixtures] The A026/A027 probe and
  five regression tests pass. These checks guard the formulas but do not
  replace their proofs.
- [PROVED] A027 is broader than A024 in evaluator access but narrower in
  target scope. A028 subsequently closes its external-prime and
  varying/unrelated maximal-order residuals by a target-side factorization.
  At this stage SG-30 remained untouched; A029 later closes it through the
  wild conductor-\(r^2\) family.

## SG-36 - Kummer/conductor target factorization

- [PROVED] For an explicit imaginary-quadratic order
  \(\mathcal O_f=\mathbb Z+f\mathcal O_K\), publicly certified by
  \((D_K,f,\operatorname{factor}(f))\), the conductor exact sequence
  exhausts every exact order-\(r\) class \(h\), \(r\ge5\): either
  \(\pi_f(h)=1\), or \(\pi_f(h)\) has exact order \(r\) in
  \(\operatorname{Cl}(\mathcal O_K)\).
- [CITED] In the first branch, Hühnlein--Takagi and
  Castagnos--Laguillaumie expose the class in a local conductor quotient.
  Its order-\(r\) component is a tame subgroup of
  \(\mathbb F_\ell^\times\) or the norm-one torus over
  \(\mathbb F_{\ell^2}\), or a wild additive \(\mathbb F_r\)-line.
- [PROVED] In the maximal branch, the virtual-unit sequence
  \[
  1\to\mathcal O_K^\times/\mathcal O_K^{\times r}
  \to V_r(K)\to\operatorname{Cl}(\mathcal O_K)[r]\to1
  \]
  is an isomorphism on the right because the imaginary-quadratic unit group
  has order dividing six. Thus
  \(\mathfrak a^r=(\alpha)\) defines a canonical non-\(r\)-th-power class
  \(\alpha K^{\times r}\).
- [PROVED] For infinitely many split \(q\equiv1\pmod r\),
  \[
  \lambda_{\mathfrak q}([\mathfrak a])
  =\alpha^{(q-1)/r}\bmod\mathfrak q
  \]
  is nontrivial and hence injective on \(\langle[\mathfrak a]\rangle\).
  Restriction/corestriction keeps \(\alpha\) nontrivial in
  \(K(\zeta_r)^\times/K(\zeta_r)^{\times r}\), and Chebotarev supplies the
  separating Kummer Frobenius.
- [CITED] Vollmer's binary power-product bookkeeping and
  Jacobson--Sawilla--Williams relative-generator reduction support the
  compact implementation. Recording \(O(\log r)\) reductions evaluates
  \(\alpha\bmod\mathfrak q\) in polynomial time without expanding it.
- [CONDITIONAL: GRH for the normal Kummer closure] Its degree is
  \(r^{O(1)}\), its logarithmic discriminant is
  \(r^{O(1)}(\log|D_K|+\log r)\), and
  Lagarias--Odlyzko/Bach--Sorenson yield an expected-polynomial Las Vegas
  search with
  \(\log q=O(\log r+\log(\log|D_K|+2))\).
- [PROVED] Therefore every nonzero source evaluator into an explicit
  imaginary-quadratic Picard group, irrespective of coordinate access,
  lifts, valuations, branches, or direct `MAKEFORM`, post-composes to a
  finite-field multiplicative character or an additive \(\mathbb F_r\)
  character. The class presentation is removable on its prime-order image.
- [PROVED] The virtual-unit/Kummer pairing is classical. The
  repository-original result is the complete effective conductor/maximal
  synthesis and its Q004 consequence, not any individual ingredient.
- [EMPIRICAL: ten exact-order targets with certified nonzero maximal
  projection, all source scalars] The A028
  probe validates the family
  \(D_r=1-4\cdot2^r\), \(\mathfrak a=(2,\omega)\),
  \(\mathfrak a^r=(\omega)\) for
  \(r=3,5,7,11,13,17,19,23,29,31\), finds a nontrivial split-prime
  character in every case, and recovers all \(r\) logarithms.
- [CITED] Lim's prescribed-order theorem, not A019, supplies maximal-branch
  infinitude: for each fixed odd prime \(r\), infinitely many imaginary
  quadratic fields have a class of exact order \(r\). A028 gives infinitely
  many separators for each such class.
- [PROVED] A019 is intentionally oversized, and its order discriminant is
  not proved fundamental for every \(r\); it is therefore only the explicit
  regression family. A025 supplies the independent infinite succinct
  conductor branch. A029 subsequently closes SG-30 with the deterministic
  conductor-\(r^2\) Gaussian family; SG-30 did not require a maximal order.
