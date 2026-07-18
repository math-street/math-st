# Handoff -- P2.2 -- after session 3

## State in eight lines

[PROVED] The typed catalogue, cited implication graph, and loss audit are complete.
[PROVED] A001 kills the direct straight-line SXDH/DDH embedding at $x^2$.
[CITED] A002 audits the Lu--Zhandry GR-BB separation. [Lu--Zhandry 2024]
[PROVED] A003 shows universally representation-uniform FBB implies GR-BB.
[PROVED] A004 shows why random relabeling does not cover one fixed representation.
[PROVED] A005 shows finite-seed efficient encodings fail for possibly inefficient adversaries.
[PROVED] A006 separates fixed-representation reductions with bounded native freshness.
[PROVED] A007 shows structured-label density does not automatically bound freshness.

## Main scoped impossibilities

[CITED] No GR-BB or TS-BB reduction can base prime-order $q$-SDH on a true
fixed-size assumption when $n<q-1$ in one group or
$\binom{n+2}{2}<q$ with a generic bilinear map.  Algebraic reductions with
explanations are covered. [Lu--Zhandry 2024, Lem. 3.2, Thms. 5.2, 5.10,
Claim 6.2, Cor. 6.1]

[PROVED] UR-FBB is one fixed PPT oracle transformer with a pointwise success
guarantee over every group implementation, including inefficient ones.  It is
a GR-BB reduction and inherits the published impossibility thresholds.

[PROVED] A006 fixes one concrete efficiently operated representation $G_*$ and
allows arbitrary encoding-bit branches and native group code.  It charges one
freshness unit whenever a distinct valid source label first enters typed use
without a challenger, generator, known-scalar, or recorded-operation
explanation.

[PROVED] With at most $n_1$ fixed-assumption labels able to reach the $q$-SDH
source and $s_1$ fresh labels there, the dictionary dimension is at most
$n_1+s_1+1$.
The Lu--Zhandry root-list simulation therefore gives a PPT attack on the fixed
assumption when $n_1+s_1<q-1$, with no added success loss.

[PROVED] Pairings do not enlarge this source trace.  For broader target-valued
bilinear $q$-type games with $t$ unexplained target labels, the safe overcounted
dimension is $\binom{n+s+2}{2}+t$; separation follows when it is below $q$.

## Failed extensions and exact reasons

[PROVED] Random relabeling changes the representation, so a premise promised
only for $G_*$ cannot be applied to the relabeled implementation.

[PROVED] A polynomial-seed encoding family has at most $2^m$ tables.  A
possibly inefficient adversary can enumerate all seeds and distinguish it
from the information-theoretic injection with overwhelming advantage.

[CITED] In the structured GGM, $\star$ evaluations and label computation are
free, while Theorem 3.2 controls a random-hybrid probability using density
$\delta$.  It does not bound adaptively chosen native labels. [Corrigan-Gibbs--
Henzinger--Wu 2026, Defs. 2.2--3.1 and Thm. 3.2]

## Residual gap

[PROVED] No result here rules out a representation-dependent reduction that
injects native-label rank linear in $q$, or a reduction that reads the code of
the $q$-SDH adversary.  These are the two remaining branches of Q003.

[PROVED] A future representation-specific meta-reduction must either compress
the native labels by rank/relations or exploit their concrete structure.  A
density statement without a transcript rank bound is insufficient.

## Current scheme evidence

[CITED] Composite-order Déjà Q gives positive reductions to static subgroup
hiding, but does not transfer to prime-order pairing groups. [Chase--Meiklejohn
2014; Chase--Maller--Meiklejohn 2016]

[CITED] Current BBS/BBS+ results retain $q$-dependent premises: scheme
security implies $\Theta(q)$-SDH for audited variants, and a later tight proof
still assumes $q$-SDH. [Chairattana-Apirom et al. 2025--2026]

## Validation

[PROVED] Primary proof bodies checked include four implication reductions,
Lu--Zhandry Lemmas 3.1--3.2 and Theorems 5.2/5.10, the RTV fully-black-box
definition, Zhandry's labeling model, and structured-GGM Theorem 3.2.

[EMPIRICAL: Python 3.13.4 on Windows 11, 2026-07-18] The final full repository
suite passed 274 tests and 3 subtests; one unrelated pre-existing P1.1 display-
format assertion failed.  P2.2 contains no computational code.

## Next action

Start A008 only with a new invariant for native-label rank linear in $q$, or an
explicit non-black-box construction.  Do not repeat random relabeling,
finite-seed substitution, or density-to-count transfer.

## Invariants

- Do not identify inverse $q$-SDH with exponent/DHE variants.
- Do not reverse hardness arrows without reversing the breaker transformation.
- Do not call the scoped separation an unrestricted black-box impossibility.
- Do not equate efficient representations with the universal GR quantifier.
- Do not transport composite-order Déjà Q to prime order.
- In A006, count every unexplained valid label at first typed use.

## Files that matter

`NOTES.md`, `attempts/A002-lu-zhandry-meta-reduction.md`,
`attempts/A006-bounded-fresh-label-meta-reduction.md`,
`attempts/A007-structured-ggm-density-transfer.md`, `refs/lu-zhandry-2024.md`,
and `refs/corrigan-gibbs-henzinger-wu-2026.md`.
