# Handoff - P1.5 - after session 10

## State in five lines

SG-01--SG-36 are complete at their stated scopes.
Novelty-grade Q004 is complete for explicit imaginary-quadratic ordinary
class targets under the repository's standing ERH/GRH target-algorithm
convention. A028 is the closing theorem: every prime-order target image is
exposed either in a conductor residue group or by a maximal Kummer
power-residue character. The algebraic dichotomy and existence of separating
primes are unconditional; GRH is used only for uniform expected-polynomial
short-prime setup. A029 independently closes SG-30 unconditionally with the
exact order-\(r\) form \([r^2,2r,r^2+1]\) of discriminant \(-4r^4\).

## The new theorem

Let \(r\ge5\) be prime and let
\[
h\in\operatorname{Pic}(\mathcal O_f),\qquad
\mathcal O_f=\mathbb Z+f\mathcal O_K,
\]
have exact order \(r\). The explicit target interface supplies the
fundamental discriminant \(D_K\), conductor \(f\), and factorization of \(f\).

The conductor exact sequence gives exactly two cases.

1. If \(h\) maps to the identity in
   \(\operatorname{Cl}(\mathcal O_K)\), the known effective conductor inverse
   maps it to a nonzero local component: a split finite-field subgroup, an
   inert norm-one torus, or a wild additive \(\mathbb F_r\)-line.
2. If its maximal projection \(\bar h\) is nonzero, write
   \(\mathfrak a^r=(\alpha)\). Because the imaginary-quadratic unit group has
   order dividing six, \(\alpha K^{\times r}\) is the canonical virtual unit
   attached to \(\bar h\). For infinitely many split
   \(q\equiv1\pmod r\),
   \[
   \lambda_{\mathfrak q}(\bar h)
   =\alpha^{(q-1)/r}\bmod\mathfrak q
   \]
   is nontrivial and hence injective on \(\langle\bar h\rangle\).

Binary ideal powering with relative-generator tracking retains \(\alpha\) as
an \(O(\log r)\)-node compact power product. It can be evaluated
\(\mathfrak q\)-adically in polynomial time even when individual compact
factors have \(q\)-divisible denominators.

Under GRH for the normal Kummer closure, effective Chebotarev gives a Las
Vegas expected-polynomial search and
\[
\log q=O(\log r+\log(\log|D_K|+2)).
\]

## Q004 consequence

For any nonzero source evaluator
\[
\phi:\langle P\rangle\to\operatorname{Pic}(\mathcal O_f),
\qquad h=\phi(P),
\]
the target-side character \(\Lambda_h\) from A028 satisfies
\[
\Lambda_h(\phi(xP))=\Lambda_h(h)^x
\]
in a multiplicative branch, or
\(x\Lambda_h(h)\) in the additive branch.

Thus an ordinary imaginary-quadratic class presentation is never an
independent third transfer endpoint. If the composite source character is
not anomalous or MOV/Frey--Rück, its novelty already lies in a direct
source-to-finite-field character; the class layer is removable.

This is a factorization theorem, not a proof that \(\phi\) cannot exist and
not a claim that every resulting finite-field character is pairing-derived.
It is strictly broader than A024 and A027 because it permits arbitrary
coordinate access, lifts, valuations, branches, direct `MAKEFORM`, external
conductor primes, and varying or unrelated maximal quadratic fields.

## Prior-art boundary

- The conductor exact sequence and effective kernel inverse are classical:
  Hühnlein--Takagi and Castagnos--Laguillaumie.
- Virtual units and the Kummer pairing are classical class field theory.
- Compact ideal power products and relative generators are supported by
  Vollmer and Jacobson--Sawilla--Williams.
- Effective Frobenius-prime bounds are due to Lagarias--Odlyzko and
  Bach--Sorenson.
- The repository-original contribution is the complete effective
  conductor/maximal synthesis in A028.4 and its evaluator-independent Q004
  consequence. Do not claim any ingredient separately as new.
- A bounded primary-source search through 2026-07-23 found no checked source
  stating this full prime-order computational dichotomy for
  imaginary-quadratic Picard targets. This remains an audited novelty claim,
  not a universal bibliographic proof.

## Infinite-family checks

- A025 supplies an infinite succinct conductor-branch control family. It is
  pairing-derived and remains labeled as such.
- A029 supplies the uniform target-only family required by SG-30, for every
  odd prime \(r\), without an auxiliary prime or analytic hypothesis.
- Lim (2016) supplies the rigorous infinitude statement: for every fixed odd
  prime \(r\), infinitely many imaginary quadratic fields have a maximal
  ideal class of exact order \(r\). A028 gives infinitely many separating
  primes for every such target. This existence theorem is not a uniform
  succinct SG-30 constructor.
- A019 supplies the explicit maximal-branch regression fixture:
  \[
  D_r=1-4\cdot2^r,\quad
  \mathfrak a=(2,\omega),\quad
  \mathfrak a^r=(\omega).
  \]
  Its order discriminant is not proved fundamental for every prime \(r\), so
  it is not itself claimed as an infinite maximal-order family. The ten
  probed cases have nonzero maximal projection, certified by their
  nontrivial residue character. It is deliberately oversized and does not
  solve SG-30.
- `code/probe_kummer_class_character.py` checks ten primes
  \(3\le r\le31\), finds a nontrivial character in every case, and recovers
  every scalar. The permanent output is
  `data/probe_kummer_class_character_full_20260723.csv`.
- Final verification: all 104 library/P1.5 tests pass; Python bytecode
  compilation succeeds; the 15-row A029 CSV regenerates deterministically;
  and the final 21-page paper compiles and passes full rendered-page
  inspection.

## Other established boundaries

- A023 reconciles the rational package with the closest discrete-logarithm
  interpolation literature. The \(B^2\) overlap scale has direct prior art;
  call the full package a repository-original synthesis.
- A024 proves
  \(C+\sum_j\log_2(h_j+1)\ge\log_2r\) only in its fixed VFB model.
- A025 is a correct ordinary ring-class transfer but only a presentation of
  the known degree-two pairing target.
- A026's hoped-for effective-kernel novelty was rejected as 1999/2009 prior
  art.
- A027 proves the sharper source-CM intrinsic-support consequence:
  \(r\)-local support gives an \(\mathbb F_r\) linearizer, while \(p\)-local
  support forces trace two and embedding degree one.

## Unconditional boundary

Ordinary Chebotarev proves infinitely many separating maximal-branch primes,
and evaluation is polynomial once one is supplied. The checked unconditional
effective bounds do not prove a uniform polynomial-time short-prime search in
\(\log r+\log|D_K|\). Do not erase this caveat.

This is compatible with marking Q004 complete under the standing convention:
the rigorous Hafner--McCurley class-group target route used by Q004 is itself
recorded under ERH.

## SG-30 - solved by A029

For every odd prime \(r\), take
\[
\mathcal O_r=\mathbb Z+r^2\mathbb Z[i],
\qquad \Delta_r=-4r^4.
\]
The conductor residue \(1+ri\bmod r^2\) has exact order \(r\) modulo rational
and Gaussian units. Its contracted ideal has raw form
\([1+r^2,2r^3,r^4]\), which reduces in two elementary steps to
\[
[r^2,2r,r^2+1].
\]
The output has \(\Theta(\log r)\) bits, lies inside SG-25, and is constructed
and certified in deterministic polynomial time. Its subgroup logarithm is
the explicit additive map \(1+rai\mapsto a\bmod r\).

This is a target-only theorem. It does not provide a source evaluator and is
exactly the wild conductor branch exposed by A028.

## Files that matter

- `attempts/A028-kummer-residue-factorization.md`: closing theorem and proof.
- `attempts/A029-uniform-wild-ring-class-target.md`: unconditional SG-30
  constructor and certificate.
- `attempts/A027-intrinsic-conductor-support.md`: source-side refinement.
- `attempts/A026-conductor-kernel-universality.md`: prior-art control.
- `attempts/A025-pairing-to-ring-class-transfer.md`: pairing control.
- `attempts/A024-valuation-factor-base-model.md`: VFB lower bound.
- `attempts/A023-interpolation-prior-art-audit.md`: prior-art reconciliation.
- `code/probe_kummer_class_character.py`: maximal Kummer regression driver.
- `code/construct_sg30_ring_class_target.py`: uniform A029 constructor.
- `RATIONAL_TRANSFER_REVIEW.md`: authoritative rational theorem wording.
- `NOTES.md`, `STATE.md`, `LOG.md`: synchronized current status.

## What I would tell my replacement

There are now two complementary closing results. A028 is negative and
evaluator-independent: every explicit quadratic ordinary class target has a
computable residue character on its prime-order image. A029 is positive and
target-only: conductor \(r^2\) in the fixed Gaussian field gives a uniform
succinct exact order-\(r\) class. The latter uses the same wild residue line
and therefore does not reopen Q004. Preserve A028's GRH boundary; A029 is
unconditional.
