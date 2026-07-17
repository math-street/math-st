---
attempt: A009
status: promising
---
# A009 — Translate-probe lower bound for generic three-sum search

## Idea

[PROVED] In a model where online decomposition can only test whether
$R-a\in\mathcal F$ for preprocessed shifts $a=P+Q$ with $P,Q\in\mathcal F$,
the success set after $T$ probes is a union of at most $T$ translates of
$\mathcal F$. Its density is therefore at most $T|\mathcal F|/r$.

## Prior art

[PROVED] No external lower-bound theorem is needed for this restricted model;
the proposed argument is finite-set union counting. It does not claim a lower
bound for arbitrary elliptic-curve coordinate algorithms.

## Plan

1. Define fixed, failure-adaptive, and randomized translate-probe schedules.
2. Prove the union bound and the resulting query lower bound.
3. Exhaustively check all shift subsets of sizes one through four on the
   order-19 fixture.
4. State precisely why a target-indexed table and a coordinate-aware Candidate
   A solver fall outside the model.

## Execution log

- [EMPIRICAL: cyclic group of order 19] Every subset of one through four
  shifts was checked against the four-point fixture base. The 5,035 schedules
  produced zero violations.
- [EMPIRICAL: same exhaustive audit] For $T=2,3,4$, respectively 95, 950, and
  3,876 schedules had support strictly below $T|\mathcal F|$ because
  translates overlapped.

## Outcome

### Model

[PROVED] Fix the factor base $\mathcal F\subseteq G$ before drawing the uniform
target $R$. Preprocessing may choose shifts $a=P+Q$ and store one witnessing
pair $(P,Q)\in\mathcal F^2$ for each shift. An online translate probe selects
one stored shift $a$, tests whether $R-a\in\mathcal F$, and, on a positive
answer, returns $(P,Q,R-a)$.

[PROVED] A failure-adaptive schedule may choose its next stored shift from the
previous membership bits, but it receives no other target-dependent
information. A randomized schedule is a distribution over such schedules.

### Lower bound

[PROVED] For a fixed shift $a$, the successful targets are exactly the
translate $a+\mathcal F$, which has $s=|\mathcal F|$ elements. For a fixed
sequence of at most $T$ probes, the total success set is contained in
$$
\bigcup_{j=1}^T(a_j+\mathcal F),
$$
so it has size at most $Ts$ and uniform-target success is at most $Ts/r$.

[PROVED] The same result holds for failure-adaptive schedules. Before the
first positive answer, every observed bit is zero, so, after fixing
preprocessing, the shifts encountered are exactly the single all-failure
path. Every successful target lies in one of the at most $T$ translates on
that path.

[PROVED] The same result holds for randomized schedules by conditioning on
the random coins, applying the deterministic bound, and averaging. Arbitrary
target-independent preprocessing of $\mathcal F$ does not change the result.

[PROVED] To obtain success at least $\delta$, any translate-probe decomposer
therefore needs
$$
T\ge\frac{\delta r}{s}.
$$
Candidate A always has $s\le2\lfloor\sqrt p\rfloor$, while Hasse gives
$r=p^{1+o(1)}$. Thus inverse-polylogarithmic success needs
$T\ge p^{1/2-o(1)}$ probes, ruling out a polylogarithmic translate-probe
decoder.

### Boundary of the result

[PROVED] The implemented lexicographic pair scan is in this model: each probe
uses the stored shift $P+Q$ and tests the required third point. Duplicate pair
sums can only reduce its success support.

[PROVED] A008 is outside the model because its target-indexed table uses the
full encoding of $R$ to select a representation without walking the
all-failure shift path. A hypothetical Candidate-A algorithm that uses
$x(R)$, solves a coordinate equation, or otherwise chooses shifts from target
coordinates is also outside the model.

[PROVED] P1.2/Q001 is therefore resolved negatively for the stated translate-probe
model, not for all uniform coordinate-aware algorithms. The latter residual
question is recorded separately as P1.2/Q004.

## Post-mortem

**Why generic pair probing fails:** [PROVED] Each online shift exposes at most
one translate of a square-root-size set, so polylogarithmically many probes
cover only a negligible fraction of a group of size approximately $p$.

**What transfers:** [PROVED] The theorem applies to any finite group and any
factor base; no elliptic-curve or randomness assumption on the base is used.

**Would it work under different assumptions?** [CONDITIONAL: target
coordinates or target-indexed advice are available] The translate-union proof
does not apply because the chosen shift need not follow the target-oblivious
all-failure path.
