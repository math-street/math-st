---
attempt: A015
status: folded-into-A001
---
# A015 - Relate point-to-class evaluation to the two DLPs

## Idea

- [CONJECTURE] The last Q004 evaluator might be excluded by target class-group
  structure alone, without a source-coordinate lower bound.

## Setup

Let $C=\langle P\rangle$ have prime order $r$, let $G$ be a represented class
group, and let $\phi:C\to G$ be a fixed nonzero homomorphism with all public
setup supplied.  Put $h=\phi(P)$.  Then $h$ has order $r$ and

$$\phi(xP)=h^x.$$

Write $T_{\rm src}$ for source ECDLP cost, $T_{\rm eval}$ for evaluating
$\phi$, $T_{\rm tgt}$ for DLP cost in $\langle h\rangle$, and $T_G$ for one
target group operation, with the same success convention in all randomized
costs.

## Evaluator sandwich

- [PROVED] Source DLP evaluates the map: recover $x=\log_PQ$ and compute $h^x$
  by double-and-add.  Thus
  $$T_{\rm eval}\le T_{\rm src}+O(\log r)T_G.$$
- [PROVED] Evaluation followed by target DLP solves source DLP: compute
  $Y=\phi(Q)$ and recover $x=\log_hY$.  Thus
  $$T_{\rm src}\le T_{\rm eval}+T_{\rm tgt}+(\log r)^{O(1)}.$$
- [PROVED] With a target-DLP oracle, source DLP and evaluation are
  polynomial-time Turing equivalent.  Without that oracle, evaluation is no
  harder than source DLP, while a cheap evaluator is exactly a reduction of
  source DLP to target DLP.
- [PROVED] If $T_{\rm eval}=(\log r)^{O(1)}$ and
  $T_{\rm tgt}=\exp(o(\log r))$, then
  $T_{\rm src}=\exp(o(\log r))$.  This is a consequence, not a contradiction:
  the research question asks precisely whether concrete curve structure can
  supply such a reduction.

## Outcome

- [PROVED] Target ideal arithmetic alone cannot yield an unconditional
  negative answer to Q004.  Once a known order-$r$ target element exists, the
  unresolved content is exactly the complexity of converting a concrete
  source point encoding into the corresponding power of that element.
- [PROVED] A universal impossibility theorem for the residual evaluator must
  use restrictions on its coordinate/bit/lift interface or prove a new lower
  bound for the concrete source family; generic group size and class-number
  estimates are insufficient.

## Boundary

- [PROVED] The sandwich does not assert that source ECDLP is hard, and it does
  not exclude special curves with known transfers.  It prevents the open
  evaluator question from being mislabeled as a purely algebraic class-number
  problem.

