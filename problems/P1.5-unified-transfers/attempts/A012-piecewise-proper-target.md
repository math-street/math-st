---
attempt: A012
status: folded-into-A002
---
# A012 - A piecewise rational transfer into a proper algebraic group

## Idea

- [CONJECTURE] Several rational formulas into a Jacobian might splice into a
  subgroup homomorphism that does not equal the restriction of any one global
  algebraic homomorphism.

## Theorem

**Theorem.**  [PROVED] Let $k$ be perfect, let $H/k$ be a smooth proper algebraic group, let
$C=\langle P\rangle\subset E(k)$ have prime order $r$, and let
$\phi:C\to H(k)$ be a group homomorphism.  Partition $C$ into $B<r$ sets and
suppose that on each set $S_b$, the evaluator $\phi$ agrees with a rational map
$F_b:E\dashrightarrow H$.  Then $\phi$ is the restriction to $C$ of one
global algebraic-group homomorphism $E\to H^0\subset H$.

## Proof

- [PROVED] Since $B<r$, one branch $S_b$ contains distinct points $X$ and
  $Y$.
- [CITED] Properness extends $F_b$ to a morphism on $E$.  Put
  $t=F_b(0)$.  Its connected image lies in the component $tH^0$; after left translation,
  $\alpha(Z)=t^{-1}F_b(Z)$ is a zero-preserving morphism into the abelian
  variety $H^0$ and hence a homomorphism by Milne's rigidity corollary.
- [PROVED] On the two branch points,
  $$\phi(X-Y)=F_b(X)F_b(Y)^{-1}
  =t\alpha(X-Y)t^{-1}=\beta(X-Y),$$
  where $\beta=\operatorname{Int}(t)\circ\alpha:E\to H^0$ is a global
  homomorphism.
  The nonzero point $X-Y$ generates the prime-order group $C$, so the two
  homomorphisms $\phi$ and $\beta|_C$ agree on a generator and hence on all of
  $C$.
- [PROVED] This factor order is valid even when $H$ is disconnected or
  noncommutative.  The identity component is normal, and conjugation by
  $t$ restricts to an algebraic-group automorphism of $H^0$.
- [PROVED] If $\phi$ is injective, $\beta$ is nonzero and SG-07 makes its
  image an elliptic abelian subvariety isogenous to $E$.

## Outcome

- [PROVED] Fewer than $r$ rational proper-target branches do not create a new
  subgroup map; they collapse to one global homomorphism.  Polynomially many
  branches are therefore harmless for an infinite family with input length
  $\log r$.
- [PROVED] This branch remains folded into the cover/Jacobian framework A002.
  A piecewise construction outside it needs at least $r$ formulas, which
  violates polynomial setup size if the formulas are explicitly stored.
