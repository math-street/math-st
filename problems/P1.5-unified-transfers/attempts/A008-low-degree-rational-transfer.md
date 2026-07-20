---
attempt: A008
status: dead
---
# A008 - A low-degree rational transfer into an affine algebraic group

## Idea

- [CONJECTURE] A rational map on the curve, computable from ordinary point
  coordinates and homomorphic only on $\langle P\rangle$, might avoid both the
  global algebraic-group theorem and the generic-source lower bound.

## Plan

- [PROVED] Measure the map's geometric degree by a common pole divisor for the
  entries of a faithful linear representation of the affine target.
- [PROVED] Apply the homomorphism identity along translation by one generator;
  a nonzero rational function on a curve cannot have more zeros than the
  degree of its pole divisor.
- [PROVED] Determine the degree required for a nontrivial subgroup character.

## Setup

Let $k$ be a field, let $E/k$ be an elliptic curve, and let
$C=\langle P\rangle\subset E(k)$ have prime order $r$.  Let $H/k$ be an
affine algebraic group with a faithful representation
$\iota:H\hookrightarrow\operatorname{GL}_s$.  Suppose
$F:E\dashrightarrow H$ is rational and defined at every point of $C$.

Over $\bar k$, let $A$ be the least effective divisor such that every matrix
entry of $\iota\circ F$ lies in $L(A)$, and put $D=\deg A$.  Equivalently, the
coefficient of a geometric point in $A$ is the largest pole order of any
matrix entry there.  Defining this divisor after base change is essential for
the geometric zero count.  The parameter depends on the fixed faithful
representation.

## Theorem

**Theorem.**  [PROVED] If $r>2D$ and

$$F(X+Y)=F(X)F(Y)\qquad(X,Y\in C),$$

then $F$ extends to a global algebraic-group homomorphism $E\to H$.  It is
therefore trivial.  Consequently every nontrivial, and hence every injective,
rational transfer of this form satisfies $D\ge r/2$.

## Proof

Write $f_{ij}$ for the entries of $\iota\circ F$, put
$M=\iota(F(P))$, and consider the entrywise defect

$$g_{ij}(X)=f_{ij}(X+P)-\sum_{\ell=1}^s f_{i\ell}(X)M_{\ell j}.$$

It has poles bounded by the sum of a translate of $A$ and $A$, hence total
pole degree at most $2D$.  The map is defined on $C$, and the subgroup law
makes $g_{ij}$ vanish at all $r$ distinct points of $C$.  A nonzero rational
function on a smooth projective curve has equally many zeros and poles,
counted with multiplicity.  Since $r>2D$, every $g_{ij}$ is identically zero,
so

$$\iota(F(X+P))=\iota(F(X))M. \tag{1}$$

Multiplication by the invertible constant matrix $M$ preserves, at each
geometric point, the largest pole order among the matrix entries (apply both
$M$ and $M^{-1}$).  Equation (1) therefore makes the least common pole
divisor $A$ invariant under translation by $P$.  Every such translation orbit
has exactly $r$ points.  Since $D<r$, the divisor $A$ is empty.  Thus
$F:E\to H$ is a morphism.  A morphism from the proper geometrically connected
curve $E$ to the affine group $H$ is constant, and the subgroup law at $0$
makes the constant the identity.  It is therefore a global algebraic-group
homomorphism.

## Boundary audit

- [CITED] A Miller function used by a pairing has a divisor with a coefficient
  $r$, so its pole degree is of order $r$; the theorem deliberately does not
  exclude the multiplicative transfer.
- [PROVED] Any attempt to flatten the anomalous transfer into one rational
  coordinate formula on $E$ must likewise have common pole degree at least
  $r/2$, unless it retains the lift/infinitesimal operation that lies outside
  this setup.
- [PROVED] Weil descent targets a proper abelian variety rather than an affine
  group, so a nontrivial global morphism is possible and SG-07 already
  describes that branch.
- [PROVED] The theorem applies to a class-group proposal only after the target
  is supplied with a polynomial-size faithful algebraic representation and
  the evaluator is the restriction of a rational map of the stated degree.
  Compact abstract ideal encodings need not supply either property.
- [PROVED] The proof works in every characteristic, including
  $r=\operatorname{char}k$.  Faithfulness is indispensable: a trivial
  representation would assign displayed degree zero to every map.

## Outcome

- [PROVED] No affine algebraic target admits an injective subgroup transfer
  represented by rational functions with common pole degree
  $\operatorname{poly}(\log r)$ for all sufficiently large $r$.

## Post-mortem

**Why it failed:** [PROVED] The subgroup contains more zeros of the
homomorphism defect than any nonzero defect of degree below $r/2$ can have;
the resulting global homomorphism from a proper curve to an affine group is
trivial.

**What transfers:** [PROVED] The quantitative obstruction is the lower bound
$D\ge r/2$, not merely the qualitative requirement that the map be global.

**Would it work under different assumptions?** [PROVED] The theorem leaves
three exits: geometric degree at least $r/2$, a non-rational
representation-specific operation such as a lift, or a non-affine target such
as a Jacobian.
