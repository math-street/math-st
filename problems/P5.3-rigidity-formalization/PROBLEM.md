# P5.3 — Formalizing curve-generation rigidity

## 1. Formal statement

**Setting.** A curve-generation procedure
\(\mathsf{Gen}:\{0,1\}^s\to\mathsf{Curves}\), together with a public
safety predicate \(\mathsf{Safe}\).

**Define.** A game for a curve designer who knows a weak set
\(\mathcal B\), unknown to other participants, and wants the published curve
to lie in \(\mathcal B\) while passing all public checks.

**Bound.** Bound \(\Pr[\mathsf{Gen}(\mathsf{seed})\in\mathcal B]\) as a
function of the designer's degrees of freedom \(b\), measured in bits.

**Construct.** Give a generator minimizing \(b\) subject to the safety
conditions, and audit existing standard curves under an explicit accounting.

## 2. Required deliverables

1. A game-based definition with the order of quantifiers explicit.
2. Reproducible degrees-of-freedom accounting rules.
3. An audit of at least P-256, Curve25519, Brainpool, secp256k1, and
   BLS12-381, with every judgement call documented.
4. A proof of the \(\min(1,2^b\epsilon)\) bound and tightness conditions.
5. A minimal-\(b\) generator proposal and comparison with the audit.
6. A discussion of tradeoffs between rigidity, safety, and performance.

## 3. Scope and cautions

- This is an accounting method, not a claim about any designer's intent.
- Public safety is a separate requirement from rigidity.
- Choices that look like defaults—hash, encoding, endianness, field,
  equation form, cofactor, counter rule, base point—must be included.
- The audit must use published specifications rather than secondary
  summaries.

