---
attempt: A002
status: promising
---
# A002 — Cubic-extension control experiment

## Idea

Implement the SG-02 positive control over a tiny $\mathbb F_{q^3}$, use the
subfield-coordinate factor base, and recover a known discrete logarithm end to
end.

## Prior art

[CITED] Diem (2011, Compositio 147, Sections 2–3) defines the extension-field
factor base through a degree-two covering whose value lies in
$\mathbb P^1(\mathbb F_q)$ and proves a decomposition algorithm in the stated
extension-field regime.

## Plan

1. Add validated arithmetic for one tiny cubic extension.
2. Enumerate the subfield-coordinate factor base and verify membership by the
   Frobenius equation.
3. Generate relations with the existing summation-polynomial machinery.
4. Recover a planted discrete logarithm and compare relation success with the
   prime-field baseline.

## Execution log

`code/run_extension_control.py` implements cubic polynomial-basis fields,
prime-order extension-field curve search, the Frobenius factor-base predicate,
three-term decomposition, relation collection, and modular linear solving.
Runs were made at $q=5,7,11$ with independent seeds and planted secrets.

## Outcome

[EMPIRICAL: q=5,7,11 and extension degree 3] All three planted discrete
logarithms were recovered exactly: 37 in the order-139 group, 83 in the
order-347 group, and 123 in the order-1367 group.

[EMPIRICAL: same three controls] The factor-base sizes were 8, 8, and 8; full
rank required 9 relations in each case and 15, 34, and 149 sampled targets,
respectively.

[PROVED] Relation rows contain only factor-base multiplicities, sampled
coefficients, and the unknown target-log coefficient. Exhaustive scalar labels
are constructed only after solving and are used solely to validate every
recovered factor-base logarithm.

[EMPIRICAL: exhaustive field tests at q=5] Every nonzero field element passed
the inverse check, and $x^q=x$ selected exactly the embedded prime subfield.

## Post-mortem

**Why it worked:** [PROVED] The subfield predicate is an algebraic Frobenius
equation and supplies a small explicitly enumerable base. At the tested scale,
exhaustive three-term decomposition produced enough independent relations for
linear algebra.

**What transfers:** [EMPIRICAL: q=5,7,11] The arithmetic, relation signs, and
linear solve are validated end to end; failures of prime-field candidates can
no longer be attributed to a broken decomposition or relation pipeline.

**Would it scale as implemented?** [PROVED] No. The control enumerates the
whole extension-field curve and uses an explicit pair table, so its
implementation is intentionally exponential in the input bit length. It
validates correctness, not the asymptotic algorithm of the cited papers.
