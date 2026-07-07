# Elliptic-curve-backed generic oracle separation

**Status:** `[PROVED]` in the scoped random-representation/type-safe generic bilinear model.

## Theorem

[PROVED] There exists an oracle relative to which ECDLP in \(\mathbb G_2\) is solvable with one query, while every probabilistic polynomial-time algorithm for FAPI-1 has negligible success. At prime order \(r\), an algorithm creating at most \(t\) target handles has success at most
\[
\frac{\binom t2+1}{r}+O(q/2^L),
\]
where \(q\) is its total query count and \(L\ge3\lceil\log_2r\rceil\) is the typed-label length. Constant success therefore requires \(t=\Omega(\sqrt r)\).

[PROVED] This is an elliptic-curve-backed *generic bilinear oracle separation*. It is not a lower bound for algorithms given ordinary curve coordinates, a coordinate-to-label map, or full \(\mathbb F_{p^2}\) arithmetic on target elements.

## Model audit

[CITED] Shoup's random-representation model exposes group elements through a random injective bit-string encoding and charges oracle group operations. Maurer's hidden-state model expresses generic DLP values as affine forms and obtains information through collisions. Zhandry distinguishes the random-representation and type-safe models and proves their security notions coincide for single-stage games that exist in both models (Shoup 1997; Maurer 2005; Zhandry 2022, Theorems 1.5–1.6).

[PROVED] FAPI-1 is a single-stage search game. A typed extension with three element sorts, a bilinear gate \(G_1\times G_2\to G_T\), and a DLP gate only from \(G_2\) to scalar bits exists in both models. The proof below is written directly for Shoup-style random representations and remains valid in the corresponding type-safe game.

## Elliptic-curve realization and oracle ensemble

[PROVED] For each security parameter \(\lambda\ge2\), choose a prime \(2^\lambda<r_\lambda<2^{\lambda+1}\), a prime \(p_\lambda\equiv-1\pmod{4r_\lambda}\), and
\[
E_\lambda/\mathbb F_{p_\lambda}:y^2=x^3+x.
\]
Bertrand's postulate supplies \(r_\lambda\). The congruence gives \(p_\lambda\equiv3\pmod4\). Pairing the quadratic-character contributions at \(x\) and \(-x\) proves \(\#E_\lambda(\mathbb F_{p_\lambda})=p_\lambda+1\), so an order-\(r_\lambda\) point \(P\) exists. Since \(p_\lambda\equiv-1\pmod{r_\lambda}\), its embedding degree is two.

[CITED] Dirichlet's theorem supplies primes in the class \(-1\bmod 4r_\lambda\), and Linnik's theorem bounds the least one by a fixed power of \(r_\lambda\). Hence \(p_\lambda\) has \(O(\lambda)\) bits. Oracle setup may store the selected prime and torsion data non-uniformly.

[PROVED] In \(\mathbb F_{p_\lambda^2}\), choose \(i^2=-1\) and \(\psi(x,y)=(-x,iy)\). For an order-\(r_\lambda\) base-field point \(P\), the point \(Q=\psi(P)\) lies in the opposite Frobenius eigenspace. Thus \((P,Q)\) is a basis of \(E[r_\lambda]\), and its Weil pairing value generates an order-\(r_\lambda\) target. The three cyclic groups below are random encodings of these actual elliptic-curve groups.

[PROVED] Independently random injections \(\sigma_1,\sigma_2,\sigma_T\) map the three copies of \(\mathbb Z_{r_\lambda}\) into disjoint typed \(L_\lambda\)-bit label spaces, with \(L_\lambda\ge3\lceil\log_2r_\lambda\rceil\). Public data may include \(p_\lambda,r_\lambda\), and the curve equation, but no coordinate-to-label map. The oracle exposes typed group laws, equality, generators, the pairing
\[
e(\sigma_1(a),\sigma_2(b))=\sigma_T(ab),
\]
and \(\operatorname{DLOG}_2(\sigma_2(b))=b\). Invalid or cross-typed strings return \(\bot\). It exposes no target-to-source operation.

[PROVED] The infinite oracle is the disjoint union of independently sampled components indexed by \(\lambda\). Cross-parameter queries cannot create a current-parameter handle and are independent of the current challenge; conditioning on their complete transcript leaves the per-parameter proof unchanged.

## Easy side and exact problem equivalence

[PROVED] ECDLP in \(\mathbb G_2\) takes one \(\operatorname{DLOG}_2\) query.

[PROVED] Let \(g_T=e(P,Q)\). A \(\mathbb G_T\)-DLP oracle solves FAPI-1 by computing \(c=\log_{g_T}Z\) and returning \([c]Q\). Conversely, FAPI-1 followed by \(\operatorname{DLOG}_2\) returns the discrete log of \(Z\). Therefore, relative to \(\operatorname{DLOG}_2\), FAPI-1 and target-group DLP are polynomial-time equivalent. Source DLP alone lacks exactly the target-to-source step.

## Per-parameter lower bound

[PROVED] Give the algorithm \(P=\sigma_1(1)\), \(Q=\sigma_2(1)\), and \(Z=\sigma_T(c)\) for uniform \(c\in\mathbb Z_r\); it must output \(\sigma_2(c)\). Use Shoup's coupling: first run a collision-free lazy simulator with fixed algorithm coins and fixed lazily sampled distinct labels, then choose \(c\), and finally complete a uniformly random encoding consistent with the simulated labels whenever its formal values are distinct at \(c\). For every fixed \(c\), this completion has exactly the distribution of a fresh uniform random encoding. Hence the coupled experiment has the same marginal distribution as independent uniform \((c,\sigma_1,\sigma_2,\sigma_T)\), except on the collision event that is charged below.

[PROVED] Every target handle in the simulator has a formal value \(\alpha X+\beta\). Target operations preserve affinity. Source exponents may depend on earlier opaque label bits, but along this fixed simulated transcript they are constants; no typed operation substitutes \(X\) into a source exponent. Pairing queries therefore add only constant target forms.

[PROVED] Let \(F\) be the final set of at most \(t\) distinct formal target forms on that simulated path. For each pair of distinct forms, equality at \(X=c\) has at most one solution, so the bad set
\[
R_F=\{c:\text{two forms in }F\text{ evaluate equally at }c\}
\]
has size at most \(B=\binom t2\). For every \(c\notin R_F\), the completed encoding gives a real execution using exactly the simulator's path and labels, even when the algorithm branches arbitrarily on their bit patterns. The encodings completed for different \(c\) need not be the same; the argument bounds the joint random-encoding experiment, not success over challenges for one already fixed encoding.

[PROVED] On the collision-free path, every registered \(G_2\) output handle has one transcript-fixed exponent \(b\). Among \(c\notin R_F\), it succeeds only when \(c=b\), accounting for at most one further challenge. Thus, for every fixed simulator randomness, at most \(B+1\) of the \(r\) challenges succeed through registered handles. Averaging preserves the bound \((B+1)/r\).

[PROVED] Any unregistered typed string supplied to a group, pairing, equality, or \(\operatorname{DLOG}_2\) oracle is independent of the hidden encoding for its type. Hitting a particular challenge-dependent value such as \(\sigma_1(c)\), \(\sigma_2(c)\), or an affine target value has probability at most \(2^{-L}\). Hitting some other valid label reveals only a transcript-fixed exponent and preserves the affine simulation. At most \(q\) blind typed inputs plus one unregistered output therefore add \(O(q/2^L)\). Consequently
\[
\Pr[\mathrm{FAPI\mbox{-}1\ success}]
\le \frac{\binom t2+1}{r}+O(q/2^L).
\]

[PROVED] A bounded-error worst-case FAPI-1 solver would succeed with probability at least \(2/3\) on every valid target and therefore also on a uniform target. The uniform-challenge bound is thus sufficient to exclude FAPI-1 from probabilistic polynomial time relative to the selected oracle; no average-case definition is being substituted for the search problem.

## Extraction of one fixed oracle

[PROVED] Fix a probabilistic polynomial-time oracle machine \(M\), and let \(S_{M,O}(\lambda)\) be its success averaged over its coins and uniform challenge for a fixed infinite oracle \(O\). The per-parameter bound gives
\[
\mathbb E_O[S_{M,O}(\lambda)]\le\varepsilon_M(\lambda),
\]
where \(\varepsilon_M(\lambda)=\operatorname{poly}(\lambda)/2^\lambda\).

[PROVED] Put \(\delta_M(\lambda)=\sqrt{\varepsilon_M(\lambda)}\). Markov's inequality gives
\[
\Pr_O[S_{M,O}(\lambda)>\delta_M(\lambda)]\le\delta_M(\lambda).
\]
The series \(\sum_\lambda\delta_M(\lambda)\) converges. The first Borel–Cantelli lemma therefore says that, with probability one over \(O\), only finitely many parameters violate \(S_{M,O}(\lambda)\le\delta_M(\lambda)\). Since \(\delta_M\) is negligible, \(M\)'s success is negligible for almost every fixed oracle.

[PROVED] Probabilistic polynomial-time oracle machines form a countable set. The intersection of their probability-one good-oracle sets still has probability one. Selecting any oracle in this intersection gives one fixed oracle relative to which \(\mathbb G_2\)-ECDLP is in polynomial time and FAPI-1 is not in probabilistic polynomial time.

## Self-attacks and scope boundary

- [PROVED] Target-label bit branching is covered because the collision-free simulator fixes the sampled strings before coupling each \(c\) to a uniformly distributed consistent encoding; the subsequent fixed-oracle extraction is a separate argument.
- [PROVED] Pairing known source multiples creates only transcript-fixed target constants.
- [PROVED] All adaptive equality information is contained in the roots of pairwise affine differences; exhaustive small-order validation found no violation among 530,000-plus exact affine sets and 10,000 additional seeded sets.
- [PROVED] Typed rejection prevents feeding a target handle to \(\operatorname{DLOG}_2\); arbitrary blind strings across all three types contribute only the explicit negligible term.
- [PROVED] Cross-parameter oracle access is independent auxiliary information and is included before the current component's lazy simulation.
- [PROVED] Non-uniform hidden curve setup is legitimate for an oracle separation, while Linnik's theorem keeps public parameter length polynomial.
- [PROVED] Concrete target-field addition, coordinates, or a coordinate-to-label map can destroy the affine invariant. No lower bound is claimed in that stronger model.
