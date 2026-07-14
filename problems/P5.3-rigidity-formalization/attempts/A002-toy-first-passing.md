---
attempt: A002
status: complete
---
# A002 — Toy forced first-passing generator

## Idea

Instantiate the conditional construction in `DEFINITIONS.md` over a fixed
toy prime. Derive exact-uniform coefficient candidates from domain-separated
SHAKE256 blocks, force the first candidate passing a public safety profile,
and choose the base point by a deterministic shared-library rule.

## Prior art

[CITED] RFC 5639 and RFC 7748 both use forced first-passing ideas for portions
of their parameter derivations. This attempt uses a new toy profile and does
not claim wire compatibility with either standard.

## Plan

1. Fix the field from the bit size and publish every safety threshold.
2. Use rejection sampling rather than modular reduction for field elements.
3. Check the curve and twist subgroup/cofactor sizes, trace, embedding degree,
   and Frobenius discriminant.
4. Return the first passing candidate and a deterministic subgroup generator.
5. Regression-test determinism and every recorded safety invariant.

## Prediction before running

A 7-bit smoke profile with eight beacon labels should find a passing candidate
for every label within 10,000 counters. A positive result requires identical
outputs on repeated runs and independent recomputation of every recorded
safety field in the test. A negative result is any exhausted label, mismatch,
or safety invariant that cannot be recomputed from the output.

## Execution log

The script `code/sample_rigid_curve.py` implements the version-one profile
over the largest prime below \(2^m\) congruent to 3 modulo 4. It records the
curve and twist subgroup orders/cofactors, trace, raw Frobenius discriminant,
forced counter, and deterministic base point.

[EMPIRICAL: bits=7, p=127, 8 beacon labels] All labels found a passing curve;
the largest selected counter was 13. The raw output is
`data/sample_rigid_curve_b7_n8_20260625.csv`. Runtime was below one second.

[EMPIRICAL: bits=7, p=127] The regression suite recomputed the selected curve
order by independent \((x,y)\) enumeration, checked every recorded safety
field, verified the subgroup generator, verified that every earlier counter
failed, and confirmed determinism. Three tests passed.

## Outcome

**Exact-uniform field lemma. [CONDITIONAL: ideal-XOF outputs are independent
uniform byte strings]** Let \(L\) be the largest multiple of \(p\) below the
byte-string range. Conditional on an XOF integer being below \(L\), each
residue modulo \(p\) has exactly \(L/p\) preimages. Repeating with fresh
domain-separated blocks therefore returns a uniform field element.

**First-passing lemma. [CONDITIONAL: ideal-XOF outputs are independent uniform
byte strings]** Let \(S\subseteq\mathbb F_p^2\) be the coefficient encodings
passing the fixed safety predicate and let \(\alpha=|S|/p^2>0\). For any
\(x\in S\), the probability that \(x\) is the first passing candidate is
\[
  \sum_{j\geq0}(1-\alpha)^j/p^2
  =1/(p^2\alpha)=1/|S|.
\]
Thus the script's declared reference distribution is uniform over safe
coefficient encodings, not over isomorphism classes.

**Selection-capacity conclusion. [PROVED]** If the public beacon is unique
and cannot be selected, restarted, or suppressed by the designer, the forced
first-passing rule has one publishable execution and hence \(b=0\). The
cryptographic sampling statement remains conditional on the ideal-XOF model.

**Projection caveat. [PROVED]** Uniformity over coefficient encodings need not
remain uniform after quotienting by \(\mathbb F_p\)-isomorphism because orbit
sizes can differ. A004 measures this exactly at \(p=127\) and supplies the
class-uniform alternative.
