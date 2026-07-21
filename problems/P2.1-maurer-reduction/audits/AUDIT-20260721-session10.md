# Tenth-session audit - 2026-07-21

## 1. Epistemic tags

[EMPIRICAL: `rg` scan plus manual review of all P2.1 Markdown changed in
Sessions 6--10] No live `[UNVERIFIED]`, pending claim, or in-progress attempt
remains.  The only `UNVERIFIED` search hit is the fifth-session audit's
literal report that none remained then.  Mathematical display blocks are
continuations of their immediately preceding tagged claims; distinct claims
inside numbered or bulleted lists carry their own tags.

[EMPIRICAL: manual cross-read of A007--A010, NOTES, Q005, and the new source
notes] The Session 7 surface theorem, Session 8 decoder bounds, Session 9
realization boundary, and Session 10 subset-sum obstruction retain their
stated assumptions and do not promote conditional or finite evidence to an
unconditional construction.

## 2. Script validation

[EMPIRICAL: 15 P2.1 unit tests on Python 3.13.4] Every P2.1 validation module
passes its known-answer or exhaustive toy fixture: exact point counts and
smooth masks, CM twist and trace sets, class numbers, residue aggregation,
iid query budgets, torus point/group formulas, and the published ordinary HNR
exception families.

[EMPIRICAL: six documented P2.1 entry points on Windows 11] The five scripts
with `--smoke` modes completed successfully, and the formula-only
`torus_alternative.py` completed through its exhaustive unit tests.  The
smoke runs stayed below one second each; bounded CM was the longest at 0.52
seconds.

[EMPIRICAL: repository-wide regression on Python 3.13.4] The full suite
passed with 315 tests and 3 subtests in 28.49 seconds.  SageMath, PARI/GP,
Singular, and msolve remain unavailable; all checked P2.1 routines use the
documented Python substitutes within the 60-bit experimental ceiling.

## 3. Consistency of stable notes

[EMPIRICAL: NOTES and A001--A010 cross-read] No finite table or proved
obstruction is contradicted by later work.  The corrected surface interval
uses $1/2<\lambda<4-2\sqrt2$, and the genus-two inverse-problem note now
distinguishes prescribed curve cardinality from prescribed Jacobian order.

[PROVED] A009's abstract-group paragraph now avoids asserting an uncited
ideal-module construction: it states only that even supplied group-description
data would omit Maurer--Wolf's recoverable algebraic `EMBED/EXTRACT`
interface.

[PROVED] Q005 now records the exact negative scope.  Full bounded-dimensional
connected groups with affine part and one-dimensional selected torus
subgroups are obstructed in their stated models; pure abelian varieties and
higher-dimensional selected subgroups are not.

## 4. Sub-goal quality

[EMPIRICAL: SG-01--SG-15 reviewed] The five newest sub-goals each have a
bounded deliverable: affine decomposition and a counting lemma, a conditional
surface-existence theorem plus explicit interface, one exact CRT substitution,
one exact HNR toy implementation, and one exponent-vector obstruction.  None
asks only for generic understanding or unscoped literature search.

## 5. Attempt status

[EMPIRICAL: front matter and outcomes of A001--A010] No attempt is left
in-progress.  A001, A008, and A010 are dead with post-mortems; A003--A007 and
A009 are completed within stated scopes; A002 is promising finite evidence
but explicitly paused at Q005 rather than presented as a proof.

## 6. Most important lesson

[PROVED] Dimension two removes the short-interval existence endpoint under
the Riemann Hypothesis, but existence separates into a smooth-order finder and
an explicit strongly algebraically defined realization.

[PROVED] Three generic bridges now fail for precise reasons: CRT decoding has
the wrong radius, bounded exponent support has insufficient coverage, and a
direct full-support subset-sum encoding pays exponential logarithmic
precision.

[PROVED] The requested unconditional reduction therefore remains open for
two explicit algorithmic reasons, not because the finite existence picture is
sparse; the next structural branch is recoverable encoding into selected
subgroups of dimension at least two.
