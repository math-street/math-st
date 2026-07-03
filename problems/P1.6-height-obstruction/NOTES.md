# Notes

## Stable facts

- [PROVED] The literal lower bound cannot hold for one prescribed affine
  point: every short-Weierstrass input has a lift with canonical height
  $O(\log p)$.
- [PROVED] For $1\leq k\leq4$, every point tuple whose five-column lift matrix
  has row rank $k$ over $\mathbb F_p$ has a simultaneous generalized
  Weierstrass lift in which every selected point has canonical height
  $O_k(\log p)$.
- [PROVED] Neither construction controls the Mordell-Weil rank or forces the
  selected rational points to be dependent, so neither construction is a
  xedni attack.
- [CITED] Jacobson, Koblitz, Silverman, Stein, and Teske (2000) derive the
  asymptotic xedni failure from a constant bound on relation coefficients,
  conditional on Lang's height conjecture and a discriminant-to-point-height
  comparison; they do not prove a $p^c$ lower bound for the selected lifts.
- [EMPIRICAL: p in {31,127,503,2039,8191,32719}; 18 random inputs per k] The
  least-norm simultaneous-lift experiment is better described on the observed
  height scale by an affine function of $\log p$ than by the fitted power law
  for $k=2,3,4$.
- [EMPIRICAL: 144 curve variants at bits 5,7,9,11 and coefficient bound 8]
  Exact arithmetic found 99 finite-field relations but only two rational
  relations; both rational witnesses came from one $p=31$, $k=1$ two-torsion
  input, and none of the 108 $k=2,3,4$ variants had a rational relation through
  the search bound.

## Height convention and validation

[CITED] LMFDB uses the non-normalized convention
$$
\widehat h(P)=\lim_{n\to\infty}n^{-2}h_x([n]P),
\qquad
h_x(a/b)=\log\max(|a|,|b|),
$$
and Sage's rational-point height uses the same numerical convention.

[EMPIRICAL: three LMFDB generator values, nine exact doublings] The exact
rational implementation in `lib/heights.py` reproduced the LMFDB heights for
the generator of 37.a1 and two generators of 389.a1 within $2\cdot10^{-6}$;
`lib/tests/test_heights.py` records the values and tolerance.

[EMPIRICAL: default experiment, five exact doublings] Across the 216 random
general-Weierstrass curve variants, the last-iteration change was at most
$0.4723$ and at most $0.362\%$ of the reported positive group maximum; the
median relative change was $0.317\%$.

[PROVED] A convention with a prefactor $1/2$ gives exactly half of every height
reported here, so it changes constants but not any growth conclusion.

## The single-point upper bound

[PROVED] Let
$E:y^2=x^3+\bar a x+\bar b$ over $\mathbb F_p$ and let
$P=(\bar x,\bar y)$. Choose balanced integer representatives $A,x,y$ and set
$$
B=y^2-x^3-Ax.
$$
Then $\widetilde E:y^2=x^3+Ax+B$ reduces to $E$, the integer point
$\widetilde P=(x,y)$ reduces to $P$, and the reduction is good because the
discriminant reduces to the nonzero discriminant of $E$.

[PROVED] The construction satisfies $|x|,|y|,|A|\leq p/2$ and
$|B|=O(p^3)$. The duplication map on the fixed lifted curve is
$$
x([2]Q)=
\frac{x(Q)^4-2Ax(Q)^2-8Bx(Q)+A^2}
     {4(x(Q)^3+Ax(Q)+B)}.
$$
Homogenizing numerator and denominator to degree four bounds
$h_x([2]Q)\leq4h_x(Q)+C\log p$ for an absolute $C$, because their coefficient
heights are $O(\log p)$. Iteration and division by $4^n$ give
$\widehat h(\widetilde P)\leq h_x(\widetilde P)+(C/3)\log p=O(\log p)$;
if an iterate is the identity, the height is zero and the same conclusion
holds.

[PROVED] Since $\log p=o(p^c)$ for every fixed $c>0$, no positive
$\Omega(p^c)$ lower bound can be uniform over all single-point lifts.

## Simultaneous lifts for k at most four

[PROVED] Write balanced lifts of the target points as $(x_i,y_i)$ and balanced
curve coefficients as $a,b$. For
$$
\widetilde E:
y^2+a_1xy+a_3y=x^3+a_2x^2+a_4x+a_6,
$$
put $(a_1,a_2,a_3,a_4,a_6)=(0,0,0,a,b)+p(z_1,z_2,z_3,z_4,z_6)$. The condition
that $(x_i,y_i)$ lie on $\widetilde E$ is the linear equation
$$
(x_iy_i,-x_i^2,y_i,-x_i,-1)z
=\frac{x_i^3+ax_i+b-y_i^2}{p}.
$$

[PROVED] If the $k\times5$ matrix on the left has row rank $k$ modulo $p$,
choose a nonsingular $k\times k$ minor modulo $p$, set the other variables to
zero, and solve. Cramer's rule gives rational $z_j$ whose denominators are
prime to $p$ and whose numerator and denominator sizes are polynomial in $p$
for fixed $k$. Consequently the lifted coefficients are $p$-integral, reduce
to $(0,0,0,a,b)$, have logarithmic height $O_k(\log p)$, and define a
nonsingular rational curve with good reduction at $p$.

[PROVED] Completing the square and removing the quadratic term sends the
general model to
$$
Y^2=X^3-27c_4X-54c_6,
\quad X=36x+3b_2.
$$
The transformed coefficients and selected points still have logarithmic
height $O_k(\log p)$. Applying the duplication-map argument proves
$\widehat h(\widetilde P_i)=O_k(\log p)$ for every $i$.

[PROVED] The affine $x$-coordinate change alters naive heights by at most a
curve-dependent constant, which vanishes after division by $4^n$ in the
canonical-height limit; hence the conclusion transfers back to the original
generalized model.

[PROVED] This theorem covers a row-rank condition on the coordinate constraint
matrix, not a Mordell-Weil rank condition. An attack still needs the lifted
points to be rationally dependent while their finite-field reductions have no
useful small relation; the construction above supplies no such dependence
guarantee.

## Fixed-rank controls

[CITED] The curve 37.a1,
$y^2+y=x^3-x$, has Mordell-Weil rank one, generator $P=(0,0)$, and
$\widehat h(P)=0.0511114082399688$ in the LMFDB/Sage convention.

[PROVED] For every good prime and $1\leq i\leq4$, the same rational points
$[i]P$ simultaneously lift their reductions and satisfy
$\widehat h([i]P)=i^2\widehat h(P)$, so their maximum height is independent of
$p$ even though the rational curve has rank one.

[CITED] The curve 11.a2 has rank zero and torsion group of order five with
generator $(5,5)$.

[PROVED] Its first four nonzero torsion multiples have canonical height zero
at every good prime, providing a still simpler counterexample to any literal
uniform statement that does not exclude torsion and bounded finite-field
subgroups.

[PROVED] Both fixed controls have small rational relations known before the
finite-field problem is posed, so they violate the no-small-relation condition
needed for a meaningful ECDLP attack.

## Random-lift measurement

[EMPIRICAL: p in {31,127,503,2039,8191,32719}; three random curves and point
tuples per p; seed 16062026] The least-Euclidean-norm coefficient correction
was the smallest-height choice among itself and two sampled nullspace offsets
in all 72 comparisons ($18$ for each $k$).

[EMPIRICAL: same range and sampling] Regressing the maximum point height as
$\alpha_k\log p+\beta_k$ gave the following ordinary-least-squares results;
the intervals are unadjusted 95% Student intervals over the 18 rows.

| $k$ | $\alpha_k$ | 95% CI | height-scale RMSE | power-fit RMSE |
|---:|---:|---:|---:|---:|
| 1 | 4.543 | [3.752, 5.334] | 3.548 | 3.687 on 17 positive rows |
| 2 | 6.983 | [6.033, 7.933] | 4.259 | 5.849 |
| 3 | 8.643 | [7.346, 9.940] | 5.818 | 8.275 |
| 4 | 10.308 | [9.144, 11.472] | 5.219 | 8.828 |

[EMPIRICAL: same range and sampling] For the direct short-Weierstrass
single-point lift, the fitted logarithmic slope was $1.018$ with 95% interval
$[0.803,1.233]$ and height-scale RMSE $0.966$.

[EMPIRICAL: same range and sampling] The fitted power exponents for the general
construction were $0.205$, $0.201$, $0.212$, and $0.220$ for $k=1,2,3,4$;
their drift over a short range and their worse original-scale residuals for
$k=2,3,4$ do not constitute evidence for a positive asymptotic exponent.

## Conjecture and falsifier

[CONJECTURE] For each fixed $1\leq k\leq4$, under the script's random input
distribution and least-Euclidean-norm lift rule, the maximum canonical height
is $\Theta_k(\log p)$ in probability. Refute this operationally by running at
bits $17,19,21,23,25$ with at least 30 independent trials per size and showing
either (i) that the 95% interval for the logarithmic slope contains zero,
(ii) that the median of height$/\log p$ changes by more than a factor of two
between bits 17 and 25, or (iii) that a power fit improves height-scale AIC by
at least 10.

## What an attack-relevant proof would require

[CITED] The 2000 failure analysis samples finite-field points with deliberately
excluded small relations, asks whether their rational lifts are dependent,
and under Lang's conjecture plus
$\log|\Delta|\geq C\max_i\widehat h(P_i)$ obtains an absolute bound on the
coefficients of any rational relation.

[PROVED] A height lower bound for every selected lift is neither true nor the
logical input used in that analysis. A structural unconditional theorem needs
an explicit input distribution, a growing lower bound on finite-field relation
coefficients, and either an unconditional uniform Lang-type lower bound for
the smallest non-torsion rational height or a direct unconditional relation
bound for this lift family.

[CITED] The general unconditional Lang-type estimate required in the preceding
route was not available in Jacobson et al. (2000); their Theorem 4.1 is stated
under plausible assumptions rather than as an unconditional result.

## Sampling and rank limitations

[EMPIRICAL: recorded in the point and group CSV files] Random finite curves,
points, and nullspace offsets use seed 16062026; coordinates are balanced
representatives, and coefficient corrections minimize Euclidean norm before
two bounded nullspace perturbations are sampled.

[EMPIRICAL: local environment on 2026-07-03] Sage and PARI rank routines were
unavailable, so the total ranks of the random lifted curves were not measured;
every random row is marked `rank_status=total rank unavailable` rather than
being assigned a guessed rank.

[PROVED] The random data therefore measure this explicit coefficient-minimizing
procedure, not the minimum over all lifts and not a rank-conditioned attack
distribution.

## Exact bounded-relation audit

[EMPIRICAL: all three stored lift variants for 12 inputs at each $k=1,2,3,4$,
bits 5,7,9,11, coefficient bound 8] The meet-in-the-middle audit classified
144 curve variants: 99 had a finite-field relation through the bound, 45 did
not, 97 had no rational relation through the bound after passing the necessary
finite filter, and two had a rational relation.

[EMPIRICAL: the same 144 variants] The two rational witnesses have coefficient
$-2$, canonical height zero, and arise from the same $p=31$, $k=1$ point with
$y=0$ under the least-norm and one nullspace-offset lift. Thus they are
two-torsion controls rather than evidence of useful multi-point dependence.

[PROVED] A row labeled `no-relation-through-bound` is only a bounded exact
statement and is not a certificate of Mordell-Weil independence.

## Failed p=17 reproduction

[CITED] Table 3 of Jacobson et al. (2000) reports 317 dependent cases among
100,000 executions of Experiment A at $p=17$ using projective lattice lifts
and a 2-descent dependence test.

[PROVED] Attempt A002 did not reproduce that experiment: the available source
does not fix a probability distribution or tie-breaking rule over short
projective vectors and nearby coefficient-lattice vectors, while those choices
can change the resulting curve and discriminant distributions.

[EMPIRICAL: three smoke rows only] The local prototype generated internally
valid lifted curves, but the original LiDIA/SIMATH and 2-descent pipeline was
unavailable. No dependency rate produced by the prototype is accepted as
evidence or compared with 317/100,000.

[CONDITIONAL: original sampling code or a complete sampling specification plus
an equivalent 2-descent implementation] The validated finite parameters,
Smith-lattice construction, containment checks, and standard-model conversion
can be reused in a faithful retry.
