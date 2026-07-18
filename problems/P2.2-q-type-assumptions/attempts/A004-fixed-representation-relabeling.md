---
attempt: A004
status: dead
---
# A004 -- Randomly relabel a fixed-representation reduction

## Goal

[PROVED] Try to extend A003 from reductions whose guarantee is universal over
representations to a reduction guaranteed only for one concrete prime-order
group family $G_*$.

## Prediction inherited from the session log

[CONJECTURE] The attempt will fail when it replaces $G_*$ by a random sparse
encoding, because the fixed-representation reduction has no promised behavior
on that new implementation.

## Attempt

[PROVED] Start with the fixed-family premise
$$
  \exists G_*\,\exists R_*\,\forall A_*:\quad
  \operatorname{Break}_{Q^{G_*}}(A_*)
  \Longrightarrow
  \operatorname{Break}_{F^{G_*}}(R_*^{A_*}).
$$
Try to run $R_*$ under a uniformly random injection
$L:\mathbb Z_r\hookrightarrow\{0,1\}^{\ell}$, use the sparse-label wrapper to
trace all group operations, and then invoke the Lu--Zhandry root-finding
simulation.

## Exact failure 1: the representation quantifier

[PROVED] The wrapper step needs the security implication for the randomly
encoded group $G_L$, but the premise supplies it only for $G_*$.  Abstract
isomorphism of $G_L$ and $G_*$ does not transfer the behavior of a machine that
reads their encodings.

[PROVED] This is a genuine logical obstruction, not a missing hybrid.  Given
any $R_*$ that works for a publicly specified family $G_*$, modify it to check
the canonical encoding of the public generator (or a public representation
identifier), abort on a mismatch, and otherwise run $R_*$.  The modified
machine has identical behavior on $G_*$ and can fail on every random relabeling.
Consequently, existence of a fixed-representation reduction alone cannot imply
the representation-uniform premise needed by A003.

## Exact failure 2: the trace invariant

[PROVED] On a concrete representation, arbitrary bit computation can construct
and validate group encodings without issuing a traced group-operation query;
for example, public point decompression or hash-to-curve code can turn computed
bits into a valid curve point.  The Lu--Zhandry simulator then has no algebraic
explanation for that new element in the span of the fixed-size challenge.

[CITED] The published structural discussion likewise leaves open derived group
laws that use auxiliary bit strings, equality branches, or the concrete
bit-string representation; its classification covers the natural affine
algebraic construction, not all such cases.  [Lu--Zhandry 2024, §3.5]

[HEURISTIC] Fresh representation-derived points do not by themselves provide
the correlated ladder $g^{x},\ldots,g^{x^q}$ required by $q$-SDH, so this trace
failure is not evidence that a useful reduction exists; it only prevents the
current meta-reduction from certifying impossibility.

## Outcome

[PROVED] A004 is dead.  Random relabeling cannot extend the theorem to a
specific concrete representation without an additional invariance theorem
about $R_*$, and such an invariance premise collapses the attempt back to A003.

[PROVED] The same quantifier failure applies to any promised representation
class that is not closed under the possibly inefficient random sparse
relabelings used by the wrapper, even if that class contains every currently
standardized or efficiently computable group family.

## Post-mortem

[PROVED] Any future stronger separation must either constrain the allowed
representation-dependent operations enough to restore algebraic explanations,
or prove a new simulation theorem directly for a named concrete group family.
The GR-BB proof alone supplies neither step.
