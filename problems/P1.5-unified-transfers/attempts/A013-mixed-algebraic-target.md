---
attempt: A013
status: dead
---
# A013 - A low-defect rational transfer into a mixed algebraic group

## Idea

- [CONJECTURE] An algebraic group with both affine and proper parts might
  admit a rational subgroup homomorphism that is neither an affine character
  nor a global elliptic embedding.

## Structural reduction

Let $k$ be perfect, let $H/k$ be a smooth algebraic group, and let
$F:E\dashrightarrow H$ be defined on $C=\langle P\rangle$, with $F|_C$ a
homomorphism.  The rational image lies in $H^0$ because its regular domain is
irreducible and contains $0_E$, which maps to $1_H$.

- [CITED] Chevalley's theorem gives an exact sequence
  $$1\longrightarrow L\longrightarrow H^0
  \mathop{\longrightarrow}^{\pi} A\longrightarrow1,$$
  where $L$ is connected affine and $A$ is an abelian variety (Milne 2022).
- [PROVED] By SG-18, $\pi\circ F:E\dashrightarrow A$ extends to a global
  homomorphism $\alpha:E\to A$.
- [PROVED] Form the pullback algebraic group
  $$H_\alpha=E\times_{A}H^0.$$
  The map $s(X)=(X,F(X))$ is a rational section of
  $H_\alpha\to E$ and is a homomorphism on $C$.
- [PROVED] Its homomorphism defect
  $$c(X,Y)=s(X+Y)(s(X)s(Y))^{-1}$$
  is a rational map $E\times E\dashrightarrow L$ and equals the identity on
  $C\times C$.

## Low-defect theorem

Fix a faithful representation $\rho:L\hookrightarrow GL_m$ and base change
to $\bar k$.  For every entry
$u_{ij}(X,Y)=(\rho(c(X,Y))-I)_{ij}$, assume:

1. for every $Q\in C$, the restricted rational function $u_{ij}(X,Q)$ on
   $E_X$ has intrinsic pole degree at most $D$; and
2. as a rational function of $Y$ on $E_{\bar k(E_X)}$, $u_{ij}(X,Y)$ has
   pole degree at most $D$.

These are exactly the two bounds used below.  The specialization clause
excludes a vertical denominator whose displayed generic degree would not
control a special fibre.  A common pole divisor on $E\times E$ can certify the
conditions through fibre-intersection degrees and the absence of vertical
pole components over $C$.

**Theorem.**  [PROVED] If $D<r$, then $F$ extends to a global algebraic-group
homomorphism $E\to H^0$.  Its image is trivial or elliptic and isogenous to
$E$.

## Proof

- [PROVED] For fixed $Q\in C$, every entry of $\rho(c(X,Q))-I$ has the $r$
  points of $C$ as zeros and pole degree at most $D<r$, so it is identically
  zero in $X$.
- [PROVED] The resulting identities for all $Q\in C$, followed by the same
  zero count in $Y$ over $\bar k(E_X)$, give $c(X,Y)=1$ as a rational-map
  identity.
- [PROVED] Hence $s$ is a rational group homomorphism.  The translation
  identity $s(X)=s(X+y)s(y)^{-1}$ removes every apparent pole exactly as in
  A008, after choosing $y$ in the dense set where the rational identity
  specializes.  Thus $s$ and therefore $F$ extend globally over $\bar k$.
  Uniqueness of extension gives Galois descent to $k$.
- [PROVED] SG-07 classifies the global image as trivial or an elliptic abelian
  subvariety isogenous to $E$.

## Outcome

- [PROVED] A mixed algebraic target supplies no new low-defect rational
  transfer.  Its proper quotient is always global, and any non-global behavior
  is measured entirely by an affine-kernel defect.  Precisely, for the fixed
  faithful representation, either a specialized $X$-fibre in item 1 or the
  generic $Y$-fibre in item 2 has pole degree at least $r$.  There is no
  representation-free degree conclusion.

## Post-mortem

**Why it failed:** [PROVED] Chevalley projection removes the proper part, and
the remaining affine cocycle has too many subgroup zeros for its pole degree.

**What transfers:** [PROVED] The residual object is explicit: an
$L$-valued rational two-cocycle on $E\times E$ that vanishes on $C^2$ but
violates at least one of the stated fibrewise degree bounds.

**Would it work under different assumptions?** [PROVED] A high-degree affine
defect, a non-rational operation, or a target without a polynomial-size
algebraic presentation remains possible; the pairing defect uses the first
exit.
