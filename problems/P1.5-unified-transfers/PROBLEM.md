# P1.5 - A unified theory of transfers

## Setting

Let $E/\mathbb F_q$ be an elliptic curve and let $P\in E(\mathbb F_q)$ have
prime order $r$.

## Task

Classify the curves for which there is a polynomial-time computable injective
homomorphism from $\langle P\rangle$ to a group with a subexponential discrete
logarithm algorithm.

- [CITED] Trace-one elliptic curves over prime fields admit the anomalous-curve
  reduction of Semaev (1998), Satoh--Araki (1998), and Smart (1999).
- [CITED] Prime-order subgroups with small embedding degree admit pairing
  reductions to finite-field multiplicative groups (Menezes--Okamoto--Vanstone
  1993; Frey--Ruck 1994).

The research question is whether a structurally different third transfer
exists, or whether a classification can rule one out in a stated class.

## Deliverables

1. A precise definition, including an explicit decision about Weil descent.
2. End-to-end validated additive and multiplicative transfer demonstrations.
3. A common structural description of the two known cases.
4. A candidate-target table with a reason for every inclusion or exclusion.
5. A restricted classification statement, with its proof or precise gaps.

## Scope

All computations use toy parameters under the repository-wide 60-bit ceiling.

## Q004 control results and novelty-grade resolution

- [PROVED] A025 satisfies the former literal class-group existence checklist.
  On an
  infinite trace-zero $j=1728$ family, the degree-two pairing character maps
  through the conductor exact sequence into the ordinary ring class group
  $\operatorname{Pic}(\mathbb Z+p\mathbb Z[i])$.
- [PROVED] A projective pairing value $1+ti$ maps to the reduced class of
  $(1+t^2,2pt,p^2)$, and Gaussian ideal extension converts the target DLP
  back to the same finite-field torus.
- [PROVED] This is a valid class-group transfer but not a structurally new
  mechanism: it is the known bilinear transfer in an ordinary ring-class
  presentation.
- [CITED] A026's proposed effective conductor-kernel inverse is not new:
  Hühnlein--Takagi (1999) reduce the class-number-one case to finite-field
  DLP, and Castagnos--Laguillaumie (2009) give the effective kernel
  isomorphism for general conductor.
- [PROVED] A027 nevertheless proves a source-side theorem for every
  evaluator, including direct form synthesis. In the source CM field, a
  target whose conductor is supported on \(\{p,r\}\) either exposes an
  explicit \(\mathbb F_r\) linearizer or forces trace \(2\) and embedding
  degree one.
- [PROVED] A028 closes both residuals at once for every explicit
  imaginary-quadratic order target. The conductor exact sequence gives an
  exhaustive dichotomy for the order-\(r\) image:

  1. a kernel image is exposed by the classical effective conductor inverse
     in a tame finite-field torus or a wild additive \(\mathbb F_r\)-line;
  2. a nonzero maximal projection has a canonical virtual unit
     \(\mathfrak a^r=(\alpha)\), and a suitable split
     \(q\equiv1\pmod r\) gives the injective character
     \[
     [\mathfrak a]\longmapsto
     \alpha^{(q-1)/r}\bmod\mathfrak q\in\mu_r(\mathbb F_q).
     \]
- [PROVED] Compact relative-generator tracking evaluates the maximal
  character in polynomial time without expanding the
  \(\Theta(r\log|D_K|)\)-bit generator.
- [CONDITIONAL: the standing ERH/GRH convention] Effective Chebotarev finds a
  separating \(q\) in expected polynomial time with
  \(\log q=O(\log r+\log(\log|D_K|+2))\).
- [PROVED] Hence the ordinary quadratic class presentation never supplies an
  independent third endpoint: every nonzero evaluator, including arbitrary
  direct form synthesis, post-composes to a finite/local residue character.
  This does not assert that the source evaluator cannot exist or that its
  resulting finite-field character is pairing-derived.
- [PROVED] SG-30 is unchanged and separate. A028 starts from a supplied
  explicit target and does not construct a succinct prescribed-order
  maximal class group from arbitrary \(r\).
- [PROVED] A029 subsequently closes the target-only SG-30 problem
  unconditionally. For every odd prime \(r\),
  \[
  \mathcal O_r=\mathbb Z+r^2\mathbb Z[i],\qquad
  \Delta_r=-4r^4,
  \]
  and the canonical reduced form
  \[
  [r^2,2r,r^2+1]
  \]
  has exact class order \(r\). Its discriminant has
  \(2+4\log_2r=\Theta(\log r)\) bits and lies inside the SG-25 window.
  This target theorem remains separate from the source evaluator and is the
  wild additive conductor branch predicted by A028.
