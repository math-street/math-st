---
attempt: A003
status: promising
---
# A003 - Quadratic outer norms under coefficient randomization

## Idea

[PROVED] When $\eta=2$, the outer field norm is a binary quadratic form in the two coordinates of the relative resultant.  Expand its pullback under one- and two-parameter polynomial randomizations and compare the resulting form, discriminant, lattice index, and sampling region with the precise hypotheses of the fixed quadratic-form smoothness theorem.

## Prior art

[CITED] Lee--Venkatesan 2018 make ordinary-NFS evaluations vary in arithmetic progressions by randomizing the defining polynomial within the kernel of reduction modulo the composite.

[CITED] Barbulescu--Lachand 2017, Theorem 4.2, gives an asymptotic for smooth values of a fixed primitive irreducible quadratic binary form in a specified two-dimensional region; the theorem is not stated uniformly over growing form discriminants.

## Plan

1. Derive the exact norm and discriminant identities for $h(t)=t^2+h_1t+h_0$.
2. Classify affine one-parameter, affine two-parameter, and homogeneous two-parameter slices.
3. Determine which slices are genuinely sampled by a valid exTNFS polynomial family.
4. Audit fixed-form, fixed-field, and congruence-coset theorem hypotheses.
5. Calculate candidate-count and norm-size losses for any viable restriction.

## Execution log

### Exact quadratic identities

[PROVED] Let $h(T)=T^2+h_1T+h_0$, let $\iota$ be its residue class, and put $\Delta_h=h_1^2-4h_0$.  Direct multiplication by the conjugate gives
\[
 N(x+y\iota)=x^2-h_1xy+h_0y^2.                                  \tag{1}
\]

[PROVED] For $z_i=x_i+y_i\iota$ and
\[
 Q(U,V)=N(Uz_0+Vz_1)=AU^2+BUV+CV^2,
\]
one has
\[
 B^2-4AC=\Delta_h(x_0y_1-x_1y_0)^2.                            \tag{2}
\]
Expanding (1) gives
\[
 B=2x_0x_1-h_1(x_0y_1+x_1y_0)+2h_0y_0y_1,
\]
and substitution followed by cancellation proves (2).  An independent SymPy expansion reduced the difference between the two sides of (2) to zero.

[PROVED] More generally $N(z_0+Uz_1+Vz_2)$ is an inhomogeneous quadratic polynomial in $(U,V)$ whose homogeneous quadratic part has discriminant $\Delta_h(x_1y_2-x_2y_1)^2$.  Its constant term is $N(z_0)$ and its two linear coefficients are the trace pairings $\operatorname{Tr}(z_0\overline{z_1})$ and $\operatorname{Tr}(z_0\overline{z_2})$.

### Comparison with the fixed quadratic-form theorem

[CITED] Barbulescu--Lachand's Theorem 4.2 assumes one fixed primitive irreducible homogeneous quadratic form of negative fundamental discriminant and averages over a two-dimensional norm-shaped region.  Its smoothness range includes the exTNFS choice $B=L_Q(1/3,\beta)$ once the form itself is fixed.

[PROVED] A one-parameter affine slice $N(z_0+Uz_1)$ is the restriction at $V=1$ of the binary form $N(Vz_0+Uz_1)$.  The theorem averages both $U$ and $V$ and therefore gives no lower bound on this single row.

[PROVED] A two-parameter affine slice $N(z_0+Uz_1+Vz_2)$ counts norms in a lattice coset $z_0+\mathbb Zz_1+\mathbb Zz_2$, not values of the homogeneous binary form in Theorem 4.2.  Removing the translation changes congruence conditions and is not covered by that theorem.

[PROVED] The homogeneous slice $N(Uz_1+Vz_2)$ is the only direct match.  If its coefficient content is $c$, its primitive part has discriminant
\[
 \Delta_h\left(\frac{x_1y_2-x_2y_1}{c}\right)^2.              \tag{3}
\]
Thus Theorem 4.2 applies only when the primitive discriminant in (3) is itself negative and fundamental; away from possible $2$-adic normalization, this requires the displayed square factor to disappear.  An ideal basis has this property after division by the ideal norm, but the removed fixed divisor must itself be $B$-smooth before the original norm can be $B$-smooth.

### Kernel-preserving polynomial randomization

[PROVED] Let $K(x)$ be an integral lift of the common residue factor $k(x)$ and let $d=\deg_x f$.  Every polynomial
\[
 f_{U,V}(x)=f_0(x)+pU(x)+K(x)V(x)                               \tag{4}
\]
has the same required factor $k(x)$ after reduction modulo $p$.  Write $P^{[e]}(a,b)=b^eP(a/b)$ for degree-$e$ homogenization.  For a fixed relation candidate, the relative resultant is
\[
 Z_{U,V}=Z_0+p\,U^{[d]}(a,b)
   +K^{[\kappa]}(a,b)V^{[d-\kappa]}(a,b)\in R.                \tag{5}
\]

[PROVED] For constant $R$-valued $U,V$, the increment ideal in (5) is
\[
 (p b^d,b^{d-\kappa}K^{[\kappa]}(a,b)).
\]
If $d=\kappa$, $K$ is monic, $(a,b)=R$, and $(a,b)$ is nonzero modulo $p$, then
\[
 (p\,b^\kappa,K^{[\kappa]}(a,b))=R.                           \tag{6}
\]
Indeed, a prime ideal dividing $b$ and $K^{[\kappa]}(a,b)$ would divide the leading term $a^\kappa$ modulo $b$, contradicting $(a,b)=R$; the prime $pR$ cannot divide $K^{[\kappa]}(a,b)$ because the irreducible degree-$\kappa>1$ polynomial $k$ has no root in $R/pR$, including the homogeneous $b=0$ case.  Thus constant $R$-valued choices of $U,V$ make (5) surjective onto an affine copy of $R$ if coefficient bounds are ignored.

[PROVED] Surjectivity is not yet a distribution theorem.  A bounded solution of
\[
 p b^\kappa u+K^{[\kappa]}(a,b)v=w
\]
can be obtained by choosing $v$ in a fundamental domain modulo $p b^\kappa$ and setting $u=(w-K^{[\kappa]}v)/(p b^\kappa)$, but its coordinates can be as large as
\[
 O_h\!\left(p|b|^\kappa+|K^{[\kappa]}(a,b)|
       +\frac{|w|}{p|b|^\kappa}\right).                       \tag{7}
\]
The fixed-form theorem counts target elements $w$; a rigorous averaging argument still needs uniform lower and upper bounds for their preimage multiplicities inside the allowed polynomial-coefficient box, together with irreducibility of enough polynomials (4).

### Degree-uniformity barrier

[PROVED] Suppose $p=L_Q(\ell_p,c_p)$ with $1/3<\ell_p<2/3$.  Then
\[
 n=\frac{\log Q}{\log p}
 =c_p^{-1}(\log Q)^{1-\ell_p}(\log\log Q)^{\ell_p-1}(1+o(1)). \tag{8}
\]

[PROVED] A dense relation box with coefficient radius $A$ has $A^{2\eta+o(1)}$ candidates.  If the entire claimed relation search is on the $T=L_Q(1/3,\tau)$ scale, then
\[
 \log A=\frac{\tau+o(1)}{2\eta}
 (\log Q)^{1/3}(\log\log Q)^{2/3}.                             \tag{9}
\]

[PROVED] The iterated resultant associated with an $x$-degree-$d$ polynomial is homogeneous of degree $\eta d$ in the coefficients of $(a,b)$: scaling $(a,b)$ by $s$ scales the inner resultant by $s^d$ and its outer norm by $s^{\eta d}$.  Since $d\ge\kappa$ and $n=\eta\kappa$, the standard box-wide worst-case norm bound contains an $A^n$ contribution.  Combining (8) and (9) gives
\[
 \log(A^n)=\frac{\tau+o(1)}{2c_p\eta}
 (\log Q)^{4/3-\ell_p}(\log\log Q)^{\ell_p-1/3}.              \tag{10}
\]

[PROVED] If $\eta$ is fixed, (10) is an $L_Q(4/3-\ell_p,O(1))$ worst-case box norm scale, whose exponent is strictly larger than $2/3$ throughout the interior medium-characteristic range.  Applying the same worst-case random-integer substitution as the standard exTNFS analysis with $B=L_Q(1/3,\beta)$ gives inverse smoothness probability on the larger $L_Q(1-\ell_p,O(1))$ scale, not on the claimed $L_Q(1/3,O(1))$ scale.

[PROVED] Keeping (10) on the $L_Q(2/3,O(1))$ scale forces
\[
 \eta=\Theta\!\left(
   (\log Q/\log\log Q)^{\,2/3-\ell_p}
 \right),\qquad
 \kappa=\Theta\!\left((\log Q/\log\log Q)^{1/3}\right).       \tag{11}
\]
Thus $\eta\to\infty$ for every fixed $\ell_p<2/3$, exactly where all presently cited polynomial/norm-form smoothness theorems require a fixed form and fixed degree.

## Outcome

[PROVED] SG-07 yields a negative compatibility result for the standard $L(1/3)$ scaling: fixing $\eta=2$ makes the outer norm accessible to a quadratic-form theorem but pushes the standard worst-case relation norm above the $L_Q(2/3)$ scale; retaining that scale forces unbounded $\eta$, outside the theorem's quantifiers.

[PROVED] A genuine positive sub-result is (6): the natural $(p,K)$ coefficient randomization is algebraically surjective onto the quadratic tower order for degree $d=\kappa$ and ideal-coprime candidates.  Turning it into a rigorous relation generator still requires the bounded-preimage and irreducibility estimates in (7), and even success would directly address only fixed-$\eta$ or boundary-$\ell_p=2/3$ families.

[PROVED] The preregistered prediction matched for the fixed-form mismatch but was too pessimistic about the affine lattice index: the full $(p,K)$ kernel randomization can have unit image ideal.  The obstruction moved from algebraic surjectivity to bounded distribution, irreducibility, and the asymptotic growth of $\eta$.
