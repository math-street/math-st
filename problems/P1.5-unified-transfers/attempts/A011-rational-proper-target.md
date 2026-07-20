---
attempt: A011
status: folded-into-A002
---
# A011 - A rational transfer into a proper algebraic group

## Idea

- [CONJECTURE] A rational map into a Jacobian or another proper algebraic
  group might be homomorphic only on $\langle P\rangle$ and thereby form a
  proper-target mechanism outside global algebraic-group homomorphisms.

## Prior art

- [CITED] A rational map from a normal curve to a proper variety extends
  uniquely to a morphism (Stacks Project, Lemma 53.2.2).
- [CITED] Every morphism of abelian varieties that sends the identity to the
  identity is a homomorphism (Milne, *Abelian Varieties*, Corollary 1.2, via the
  rigidity lemma).

## Theorem

**Theorem.**  [PROVED] Let $k$ be perfect, let $H/k$ be a smooth proper
algebraic group, and let $F:E\dashrightarrow H$ be a rational map defined at
$0_E$.  If $F(0_E)=1_H$, then $F$ extends uniquely to a global
algebraic-group homomorphism $E\to H^0$.  In particular, the conclusion holds
when $F$ is defined on $C=\langle P\rangle$ and $F|_C$ is a homomorphism.  Its
image is trivial or an elliptic abelian subvariety isogenous to $E$.

## Proof

- [CITED] Since $E$ is a smooth, hence normal, complete curve and $H$ is
  proper, Stacks Project Lemma 53.2.2 extends $F$ uniquely to a morphism on all
  of $E$.
- [PROVED] The image of connected $E$ lies in one component; because
  $F(0_E)=1_H$, that component is $H^0$.
- [CITED] A smooth connected proper algebraic group is an abelian variety, and
  a morphism of abelian varieties preserving the identity is a homomorphism
  (Milne 2022; Milne, *Abelian Varieties*, Corollary 1.2).
- [PROVED] SG-07 then applies: a nonconstant image has dimension one, its
  kernel is finite, and $E$ maps isogenously onto an elliptic abelian
  subvariety of $H$.
- [PROVED] No separability hypothesis is needed.  In positive characteristic,
  a purely inseparable nonzero homomorphism is still an isogeny onto its
  elliptic image.

## Outcome

- [PROVED] A single rational proper-target formula is never merely a
  subgroup-level accident; it belongs to the global algebraic/isogeny branch.
- [PROVED] This folds into A002 for Jacobian targets.  An ambient Jacobian may
  still have an easier DLP algorithm even though the source subgroup lies in
  an elliptic image; that is a target-algorithm property, not a new kind of
  homomorphism.

## Boundary

- [PROVED] The theorem does not exclude Weil descent.  It classifies the map's
  image, while descent can exploit the ambient Jacobian representation or a
  restriction-of-scalars construction to obtain a different DLP algorithm.
- [PROVED] Piecewise rational maps with different formulas on different source
  points are not a single rational map and require separate branch accounting.
