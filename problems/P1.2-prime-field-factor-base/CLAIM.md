# CLAIM — P1.2 is impossible as written under standard L-notation

> **Status: [PROVED].** The initially quarantined claim survived the attacks
> listed below. The conclusion is conditional only on reading
> $L_p(1/2)$ in its standard subexponential sense and reading “constant $m$”
> as independent of $p$.

## Theorem

[PROVED] Let $G_p=E(\mathbb F_p)$ have order $r_p$, let
$\mathcal F_p\subseteq G_p$ have size
$$
s_p\le L_p[1/2,c]
=\exp\!\left((c+o(1))\sqrt{\log p\log\log p}\right)
$$
for a fixed $c>0$, and fix an integer $m$ independent of $p$. For a uniform
$R\in G_p$, every algorithm that outputs
$R=P_1+\cdots+P_m$ with $P_i\in\mathcal F_p$ has success probability at most
$p^{-1+o(1)}$. In particular, that probability is eventually smaller than
$1/q(\log p)$ for every fixed positive polynomial $q$.

[PROVED] Therefore conditions (1) and (3) in the supplied formal statement
cannot hold simultaneously under this interpretation. Membership cost,
oracle access to uniform random points, and the internal running time of the
decoder cannot repair this support-size obstruction.

## Proof

1. [PROVED] Define the ordered sum map
   $$
   \sigma_m:\mathcal F_p^m\longrightarrow G_p,
   \qquad (P_1,\ldots,P_m)\longmapsto\sum_{i=1}^mP_i.
   $$
   Its image $S_m$ is exactly the set of targets with an allowed length-$m$
   decomposition, so $|S_m|\le |\mathcal F_p^m|=s_p^m$.

2. [PROVED] A correct output on target $R$ implies $R\in S_m$, independently
   of the algorithm's randomness, advice, preprocessing, or oracle queries.
   Hence, conditioning on any fixed factor base,
   $$
   \Pr[\text{success}]\le \Pr[R\in S_m]
   =\frac{|S_m|}{r_p}\le\frac{s_p^m}{r_p}.
   $$
   If construction of $\mathcal F_p$ is randomized before the independent
   target is drawn, averaging this conditional inequality gives the same
   bound.

3. [CITED] Standard generalized L-notation is
   $L_x[r,\psi]=\exp((\psi+o(1))(\log x)^r
   (\log\log x)^{1-r})$ for fixed parameters (Lenstra 2017, Section 5.2.2).
   [PROVED] Consequently
   $$
   \log(s_p^m)\le m(c+o(1))\sqrt{\log p\log\log p}=o(\log p),
   $$
   and therefore $s_p^m=p^{o(1)}$.

4. [CITED] Hasse's bound gives
   $p+1-2\sqrt p\le r_p\le p+1+2\sqrt p$ (Sutherland 2025, Lecture 7).
   [PROVED] Thus $r_p=p^{1+o(1)}$, and Steps 2–3 give
   $$
   \Pr[\text{success}]\le p^{-1+o(1)}.
   $$

5. [PROVED] To make the last asymptotic comparison explicit, for all
   sufficiently large $p$ the upper bound is at most $2p^{-1/2}$. For every
   fixed polynomial $q$ that is eventually positive,
   $2q(\log p)<p^{1/2}$ eventually. Hence
   $2p^{-1/2}<1/q(\log p)$ eventually, contradicting condition (3).

[PROVED] The assumptions that the group order is prime and that the curve is
ordinary are not needed for this contradiction; Hasse's bound and the
cardinality of the group are sufficient.

## Adversarial checks

| Possible escape | Result |
|---|---|
| Exactly $m$ versus at most $m$ terms | [PROVED] At most $m$ reaches no more than $1+s_p+\cdots+s_p^m\le(m+1)\max(1,s_p^m)=p^{o(1)}$. |
| Repeated versus distinct terms | [PROVED] Allowing repetitions gives the larger domain $\mathcal F_p^m$ and was already used in the upper bound. |
| Ordered versus unordered terms | [PROVED] Ordered tuples give the larger representation space and were already used. |
| Signed summands | [PROVED] Replacing the base by $\mathcal F_p\cup(-\mathcal F_p)$ changes $s_p$ by at most a factor two, still $p^{o(1)}$ for fixed $m$. |
| Randomized or nonuniform decoder | [PROVED] These can select a representation only after the target lies in the fixed support $S_m$; they cannot enlarge $S_m$. |
| Randomized factor-base construction | [PROVED] Condition on the realized base and average the pointwise upper bound. |
| Uniform-point oracle | [PROVED] Oracle samples do not change whether the fixed target belongs to $S_m$. |
| Let $\mathcal F$ depend on $R$ | [PROVED] This no longer supplies the fixed pair $(\mathcal F,\mathcal D)$ required before a uniform target is tested. |
| Toy counterexample search | [EMPIRICAL: cyclic group of order 19] Exhaustive tests for $1\le s\le5$ and $0\le m\le4$ found no violation; collisions often made the support strictly smaller than $s^m$. |

## Necessary repairs to the statement

[PROVED] If the desired success is at least
$\delta_p\ge1/q(\log p)$, then the same counting argument forces
$$
s_p^m\ge \delta_p r_p.
$$
For fixed $m$, Hasse's bound therefore requires
$$
s_p\ge\left(\frac{p}{2q(\log p)}\right)^{1/m}
=p^{1/m-o(1)}.
$$
Thus a non-vacuous fixed-$m$ version needs at least a
$p^{1/m-o(1)}$ factor base; a genuinely subexponential base is too small.

[PROVED] Conversely, retaining
$s_p\le L_p[1/2,c]$ while asking for inverse-polylogarithmic success forces
$$
m\ge
\frac{\log r_p-\log q(\log p)}
     {(c+o(1))\sqrt{\log p\log\log p}}
=\left(\frac1c+o(1)\right)
  \sqrt{\frac{\log p}{\log\log p}}.
$$
This is only a necessary support-size condition, not a construction or an
efficient decomposition algorithm.

## Scope and notation caveat

[PROVED] The prompt's warning that a base of size approximately $p^{1/2}$ has
abundant three-term decompositions is correct, but it does not answer this
theorem: for every fixed $c$,
$L_p[1/2,c]=p^{o(1)}=o(p^\varepsilon)$ for every fixed $\varepsilon>0$.
In particular, a genuinely $p^{1/2}$-scale base violates formal condition (1)
under standard L-notation. The warning and the formal bound describe different
size regimes.

[CONDITIONAL: $L_p(1/2)$ was intended to mean $p^{1/2}$] The theorem above
does not refute that nonstandard square-root-size version. In that corrected
regime, the Candidate-A experiments remain relevant and the existence of a
polylogarithmic finder remains open.

[PROVED] Under standard L-notation, however, P1.2 is resolved negatively as
written. This is a specification-level impossibility proof, not an elliptic-
curve discrete-logarithm algorithm and not a break of prime-field ECC.

[PROVED] A008 does not weaken this theorem: its fixed-$m$ radix factor base has
size $\Theta(p^{1/m})$, which is necessarily larger than every fixed-constant
$L_p[1/2,c]$. A008 only shows that a separate square-root correction must also
charge nonuniform description, preprocessing, and storage.
