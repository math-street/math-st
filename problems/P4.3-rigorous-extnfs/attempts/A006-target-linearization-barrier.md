---
attempt: A006
status: promising
---
# A006 - Why the quadratic relation randomization does not split generic targets

## Idea

[PROVED] Quantify the probability that exponent randomization puts a generic target into the low-degree subspace where the A005 linear-resultant argument applies.

## Low-degree subspace count

[PROVED] Write
\[
 \mathbb F_Q=\mathbb F_{p^\eta}[\theta]/(k(\theta)),
 \qquad \deg k=\kappa,\qquad n=\eta\kappa.
\]
The set
\[
 W_m=\left\{\sum_{j=0}^m c_j\theta^j:
 c_j\in\mathbb F_{p^\eta}\right\}
\]
has exactly $p^{\eta(m+1)}$ elements.

[PROVED] Let $s$ generate a subgroup of order $\ell$ and choose $e$ uniformly modulo $\ell$.  Since $s^e$ is uniform in that subgroup,
\[
 \Pr[s^e\in W_m]
 =\frac{|\langle s\rangle\cap W_m|}{\ell}
 \le\frac{p^{\eta(m+1)}}{\ell}.                               \tag{T1}
\]
For a full-size DLP subgroup satisfying $\ell=Q^{1-o(1)}$, this is at most
\[
 p^{-\eta(\kappa-m-1)+o(n)}.                                 \tag{T2}
\]

[PROVED] In particular, the linear relation space $W_1=\{a-b\theta\}$ has only $p^{2\eta}$ elements.  For a target uniform in the full multiplicative group and $\eta=2$, its density is at most
\[
 p^{4-n}=Q^{-1+2/\kappa},
\]
so reaching it by target exponent randomization takes exponential, not subexponential, expected time.

## One missing degree already costs too much

[PROVED] In the optimized interior exTNFS scale,
\[
 p=L_Q(\ell_p,c_p),\qquad
 \eta=\Theta((\log Q/\log\log Q)^{2/3-\ell_p}).
\]
and for a target uniform in $\mathbb F_Q^\ast$, dropping even one coefficient over $\mathbb F_{p^\eta}$ from a full degree-$(\kappa-1)$ representative incurs the probability factor $p^{-\eta}$.  The same conclusion holds for a subgroup with $\ell\ge Q/p^{o(\eta)}$.  Its inverse has logarithm
\[
 \eta\log p
 =\Theta((\log Q)^{2/3}(\log\log Q)^{1/3}),                   \tag{T3}
\]
which is on the $L_Q(2/3,O(1))$ scale and is already much larger than an $L_Q(1/3,O(1))$ budget.

[PROVED] Therefore, for full-size target distributions, an $L_Q(1/3)$ target-splitting argument cannot wait for a random target power to land in a proper fixed-codimension $\mathbb F_{p^\eta}$-linear subspace.  It must use a nonlinear representation such as a quotient/product parameterization, a subfield action, or a theorem about norms of essentially full-degree lifts.

[PROVED] For smaller DLP subgroups, including pairing subgroups whose order may be much smaller than $Q$, the cardinality bound (T1) can be trivial.  Ruling out concentration in $W_m$ would then require a subgroup--additive-subspace intersection theorem; A006 makes no such claim.

## Consequence for A005

[PROVED] A005 works because a relation candidate is *already* linear in $\theta$ and polynomial coefficients are randomized around it.  A generic full-group target is not linear, and (T1)--(T3) show that exponent randomization cannot make it linear within the desired complexity.

[PROVED] Choosing a fresh randomized polynomial field for each target or descent node does not remove this issue.  To transfer the current finite-field element to the new field one must first find a suitably small preimage there, which is exactly the initial-splitting problem quantified above.

[PROVED] Prime ideals from one number field also do not become factor-base columns in another: virtual logarithms are field-specific.  Rebuilding a relation matrix in a new field cannot express the old special-$q$ virtual logarithm without an additional cross-field relation.

## Outcome

[PROVED] For full-size target distributions, the boundary relation-supply theorem in A005 cannot be promoted to a full DLP algorithm merely by reselecting randomized polynomials during initial splitting or descent.

[PROVED] S-04--S-05 remain genuinely different analytic problems from S-01--S-03.  For full-size targets, the precise barrier is the $p^\eta=L_Q(2/3,O(1))$ cost of losing even one full tower coefficient in a target lift; for smaller subgroups, the corresponding intersection problem remains open.
