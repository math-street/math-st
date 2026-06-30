# P2.2 — Reducing or separating $q$-type assumptions

## Formal statement

**Setting.** [CITED] Pairing groups
$(\mathbb G_1,\mathbb G_2,\mathbb G_T)$ of prime order $r$.
[Boneh–Boyen 2008, §2]

**$q$-SDH.** [CITED] Given $g,g^x,g^{x^2},\ldots,g^{x^q}$, output
$(c,g^{1/(x+c)})$ for some $c\in\mathbb Z_r$.
[Boneh–Boyen 2008, §3.1]

**Task.** Either give a black-box reduction from $q$-SDH to a constant-size
assumption (one whose instance size does not grow with $q$), or prove via
meta-reduction that no such reduction exists.

## Deliverables

1. A uniform-notation assumption catalogue.
2. An implication graph with cited edges and loss factors.
3. A written account of where an attempted constant-size-assumption reduction
   breaks.
4. A precisely scoped meta-reduction statement, proved or stated as a target.

## Verified best-known table

| Result | Verified statement | Primary reference |
|---|---|---|
| [CITED] $q$-SDH introduction | Short standard-model signatures are proved under inverse-form $q$-SDH. | Boneh–Boyen, EUROCRYPT 2004 / *J. Cryptology* 2008 |
| [CITED] Generic hardness | The $q$-SDH family has generic-group lower bounds; this evidence is not a reduction to a static assumption. | Boneh–Boyen 2008 |
| [CITED] Concrete attack | Supplied powers enable Cheon's divisor-dependent hidden-exponent recovery algorithms. | Cheon, EUROCRYPT 2006 |
| [CITED] Historical meta-reduction | Coron's technique proves optimality/lower bounds for reductions of several signature schemes; it is not itself a $q$-SDH-to-static separation. | Coron, EUROCRYPT 2002 |
| [CITED] Positive static reduction outside the setting | Déjà Q reduces $q$-SDH and broad $q$-type classes to static subgroup hiding in composite-order pairing groups. | Chase–Meiklejohn, EUROCRYPT 2014; Chase–Maller–Meiklejohn, ASIACRYPT 2016 |
| [CITED] Prime-order meta-reduction | A fully black-box generic reduction from $q$-SDH to a true fixed-size prime-order assumption is impossible at the stated dimension thresholds. | Lu–Zhandry, CRYPTO 2024 |
| [CITED] Scheme-level concrete follow-up | BBS+ and deterministic BBS security implies $\Theta(q)$-SDH, and matching usage-dependent attacks exist; later work gives a tight $q$-SDH proof for restricted-use BBS. | Chairattana-Apirom–Tessaro, ASIACRYPT 2025; Chairattana-Apirom–Hofheinz–Tessaro, EUROCRYPT 2026 |
| [CITED] Label-model boundary | Random-representation and type-safe generic models require care when ordinary label computation is unbounded; efficient internal PRP substitutions do not preserve the full information-theoretic class. | Zhandry, CRYPTO 2022 |
| [CITED] Structured-GGM lower bound | A partial public label operation yields a density-sensitive discrete-log lower bound, but not a $q$-SDH-to-static separation or a deterministic native-label budget. | Corrigan-Gibbs–Henzinger–Wu, EUROCRYPT 2026; A007 |
| [PROVED] Representation-uniform corollary | A fully-black-box standard-oracle reduction guaranteed pointwise over every group representation implies GR-BB and is impossible at the same thresholds. | A003, using Lu–Zhandry Lemma 3.2 and Corollary 6.1 |
| [PROVED] Limited-representation boundary | Random relabeling cannot extend the result to a guarantee for a class excluding random sparse implementations, including one named family or efficient-only families; the required representation quantifier and algebraic trace are absent. | A004 |
| [PROVED] Bounded native-label separation | For one named concrete representation, a fully-black-box reduction that introduces at most $s_1$ unexplained labels in the $q$-SDH source is impossible under fixed-assumption hardness when $n_1+s_1<q-1$.  For broader target-valued bilinear $q$-type games, a safe threshold is $\binom{n+s+2}{2}+t<q$. | A006, extending the trace dimension in Lu–Zhandry Theorems 5.2 and 5.10 |
