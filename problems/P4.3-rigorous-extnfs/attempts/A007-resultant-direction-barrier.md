---
attempt: A007
status: promising
---
# A007 - Resultant-direction barrier for target splitting and special-q

## Bidegree identity

[PROVED] Let $P,f\in R[x]$ have degrees $m,d$.  The resultant
\[
 \operatorname{Res}_x(P,f)
\]
is homogeneous of degree $d$ in the coefficients of $P$ and homogeneous of degree $m$ in the coefficients of $f$.

[PROVED] This follows immediately from the root formulas
\[
 \operatorname{Res}(P,f)
 =p_m^d\prod_{P(\alpha)=0}f(\alpha)
 =(-1)^{md}f_d^m\prod_{f(\beta)=0}P(\beta):
\]
scaling $P$ by $u$ multiplies the resultant by $u^d$, while scaling $f$ by $v$ multiplies it by $v^m$.

## Why A005 works for relations

[PROVED] A relation polynomial $P=a-bx$ has $m=1$.  Therefore its resultant with $f$ is **linear in the coefficients of $f$**:
\[
 \operatorname{Res}_x(a-bx,f)=b^d f(a/b).
\]
This is the only reason the kernel-preserving polynomial randomization in A005 turns the relative resultant into an affine lattice in the tower order.

## Why the same direction fails for a full target lift

[PROVED] A generic target lift has degree $m=\kappa-1$ (or comparable degree).  Randomizing the selected polynomial $f$ then makes the relative resultant a degree-$m$ polynomial in the randomized coefficients, not an affine map.  Randomizing the lift $P$ while keeping $f$ fixed makes it degree $d\ge\kappa$ in the lift coefficients.

[PROVED] Applying the outer tower norm multiplies these degrees by $\eta$.  Thus a full-degree target lift produces a randomized integer form of degree
\[
 \eta\kappa=n+O(\eta),
\]
precisely the growing-degree regime absent from every smooth-value theorem in the audit.

[PROVED] Restricting to a factorized lift $P=L\cdot S$ with only a linear factor $L$ randomized gives
\[
 \operatorname{Res}(P,f)=\operatorname{Res}(L,f)\operatorname{Res}(S,f).
\]
The randomized factor is accessible to A005, but the fixed factor must already be smooth because a product is $B$-smooth only if both factors are.  This merely moves the target-smoothing problem into $S$.

## Why changing fields does not solve special-q descent

[PROVED] A special-$q$ descent candidate is again linear, so its resultant would be affine in randomized polynomial coefficients.  However the current prime ideal $\mathfrak q$, its lattice, its virtual logarithm, and all factor-base columns are defined in the already selected number field $K_f$.

[PROVED] Replacing $f$ by a new randomized polynomial changes the number field and destroys that identification.  The new field's relation cannot contain the old prime-ideal column without a cross-field relation, whose construction is another target-lifting problem.

[PROVED] Keeping $f$ fixed preserves $\mathfrak q$ but removes the A005 source of randomness; the remaining variables are the short vectors in the special-$q$ lattice, returning exactly to (SQ).

## Outcome

[PROVED] SG-11 has a negative answer for direct coefficient-block linearization: the resultant is affine in polynomial coefficients only because ordinary relation polynomials have degree one.  Full target lifts restore degree $\Theta(n)$.

[PROVED] SG-12 has a negative answer for direct reuse of A005: polynomial randomization is incompatible with keeping the current special-$q$ and its virtual logarithm fixed.

[PROVED] These are barriers to this specific modification, not impossibility theorems for every target-splitting or descent algorithm.
