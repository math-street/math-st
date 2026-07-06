---
attempt: A004
status: promising
---
# A004 - Minimal rank theorem for exTNFS relation rows

## Idea

[PROVED] Replace the vague instruction to collect “enough” relations by an exact escape-from-subspaces statement for the conditional distribution of accepted exTNFS rows.

## Prior art

[CITED] Schirokauer's NFS-DLP survey constructs the valuation/Schirokauer matrix and says that, if the target vector is not in its column space, one enlarges the relation set and “expects” the rank to increase.  It proves the sparse linear-algebra cost once a solvable matrix is present, not the rank of the relation supply.

[CITED] Lee--Venkatesan 2018 prove enough character information for the congruence-of-squares stage of randomized factoring NFS, but that theorem is not a full-rank theorem for a DLP factor-base matrix.

## Exact row space

[PROVED] Let $V_Q=\mathbb F_\ell^{N_Q}$ have one coordinate for every prime-ideal factor-base element and every Schirokauer-map coordinate after deterministic symmetries and known dependencies are quotiented out.  Let
\[
 R(\mathbf z)\in V_Q
\]
be the signed valuation/Schirokauer row of an accepted two-sided smooth relation.

[PROVED] Let $\mathcal L_Q\subseteq V_Q^\ast$ be the desired virtual-log solution space determined by the actual maps to $\mathbb F_Q^\ast$, and define its annihilator
\[
 H_Q=\{r\in V_Q:\lambda(r)=0\text{ for every }\lambda\in\mathcal L_Q\}.
\]
Every algebraically valid relation row lies in $H_Q$.  Sparse linear algebra determines precisely the intended solution space exactly when the collected rows span $H_Q$.

[PROVED] Merely proving
\[
 \#\{\mathbf z:\mathbf z\text{ gives a smooth relation}\}\ge N_Q
\]
does not imply this spanning property: all those rows may lie in one proper subspace of $H_Q$.

## A sufficient anti-concentration statement

[PROVED] Let $\mu_Q$ be the distribution of $R(\mathbf z)$ when a randomized relation candidate is conditioned on simultaneous smoothness.  Define the escape parameter
\[
 \delta_Q=\inf_{\substack{\varphi\in H_Q^\ast\\\varphi\ne0}}
 \Pr_{R\sim\mu_Q}[\varphi(R)\ne0].                             \tag{R1}
\]
The precise rank input that preserves the claimed $L(1/3)$ constant is
\[
 \delta_Q\ge L_Q(1/3,-o(1))                                  \tag{R2}
\]
uniformly over the selected tower fields and factor bases.

[PROVED] Conditions (R1)--(R2) are sufficient.  If the current row span is a proper subspace $W\subsetneq H_Q$, choose a nonzero functional $\varphi$ on $H_Q$ that vanishes on $W$.  The event $\varphi(R)\ne0$ forces $R\notin W$, so the expected number of accepted rows required to raise the span dimension is at most $1/\delta_Q$.  Summing over $\dim H_Q$ dimension increases gives
\[
 \mathbb E[\text{accepted rows to span }H_Q]
 \le \frac{\dim H_Q}{\delta_Q}.                               \tag{R3}
\]
Since $\dim H_Q=L_Q(1/3,\beta+o(1))$, (R2) changes no leading $L(1/3)$ constant.

[PROVED] An equivalent hyperplane formulation is
\[
 \sup_{\varphi\ne0}\Pr_{R\sim\mu_Q}[\varphi(R)=0]\le1-\delta_Q.
\]
It is substantially weaker than assuming uniform random rows, but it is still not implied by smoothness density.

## Uniform-row benchmark

[PROVED] If rows were independent and uniform in an $r$-dimensional $H_Q$, then $r+s$ rows would fail to span with probability at most
\[
 \sum_{j=0}^{r-1}\ell^{j-(r+s)}
 <\frac{\ell^{-s}}{\ell-1}.                                  \tag{R4}
\]
Indeed, after any $j$ independent rows, a new uniform row remains in their span with probability $\ell^{j-r}$; multiplying the complementary probabilities gives the exact full-rank probability, and a union bound gives (R4).

[PROVED] The exTNFS rows are not uniform: they are sparse, their two sides share the same $(a,b)$, local splitting restricts which columns can occur, and conditioning on both norms being smooth changes the distribution.  Formula (R4) is therefore a benchmark, not a theorem about exTNFS.

## Hyperplane and character-sum form of the missing theorem

[PROVED] A functional $\varphi\in H_Q^\ast$ assigns weights to factor-base ideals and Schirokauer coordinates.  On a smooth principal relation it evaluates the corresponding weighted valuation sum.  A nonzero $\varphi$ for which every accepted row satisfies $\varphi(R)=0$ is exactly a spurious null character preventing full rank.

[CONJECTURE] A directly usable analytic form of (R2) is the hyperplane-incidence bound
\[
 \#\{\mathbf z\in\mathcal S_Q(A):
 P^+(F_f(\mathbf z)F_g(\mathbf z))\le B,\ \varphi(R(\mathbf z))=0\}
 \le (1-\delta_Q)
 \#\{\mathbf z\in\mathcal S_Q(A):P^+(F_fF_g)\le B\},           \tag{R5}
\]
for every nontrivial $\varphi$ modulo the true virtual-log dependencies, with $\delta_Q$ satisfying (R2).  This conjecture is refuted by a sequence of nontrivial functionals whose phase is $1$ on all but an $L_Q(1/3,-\Omega(1))$ fraction of accepted rows.

[PROVED] Fourier inversion rewrites the left side of (R5) as
\[
 \frac1\ell\sum_{t\in\mathbb F_\ell}
 \sum_{\mathbf z\ {\rm smooth}}
 e_\ell(t\varphi(R(\mathbf z))).
\]
Thus cancellation estimates for every $t\ne0$ would imply (R5), but the sums are over values already conditioned to satisfy the open simultaneous-smoothness statement (RC).  None of the fixed-form density theorems in the P4.3 audit supplies this extra equidistribution.

## Deterministic obstructions to check first

[PROVED] Before any probabilistic rank theorem can apply, the following deterministic failures must be removed:

1. [PROVED] A factor-base column that occurs in no accepted relation makes the span deficient.
2. [PROVED] A partition of the support hypergraph into disconnected components creates independent scaling freedoms unless known cross-relations join them.
3. [PROVED] Unit, class-group, automorphism, and subfield dependencies must be included in the definition of $H_Q$ rather than mistaken for random rank defects.
4. [PROVED] Duplicate rows from units or sign symmetries add relation count but no rank.

## Outcome

[PROVED] SG-08 is complete as a precise theorem target.  The minimal missing rank statement is the subexponential escape bound (R2), not the much stronger uniform-row heuristic.

[PROVED] The adaptive algorithmic modification is straightforward: maintain the row span online, retain only independent accepted rows, and stop when it reaches $\dim H_Q$.  Its expected overhead is rigorously bounded by (R3) **if** (R2) is proved; the modification does not itself prove (R2).

[PROVED] The rank gap is analytically coupled to, but logically stronger than, relation smoothness: it asks for character cancellation inside the simultaneously smooth subset.
