# Reduction of quartic/quartic 2-cycle degrees

## Scope

[PROVED] Let \(5\le p<q\) be a prime-order 2-cycle, put \(c=q-p\), and
suppose both exact embedding degrees lie in

\[
Q_4=\{5,8,10,12\}.
\]

Then the cycle is exactly

\[
(p,q;k_1,k_2)=(11,13;12,10).
\]

No other ordered pair in \(Q_4^2\) occurs.

## Quotient-difference reduction

[PROVED] The exact-degree divisibilities give positive integers \(m,n\) with

\[
F(c):=\Phi_{k_1}(-c)=mq,
\qquad
H(c):=\Phi_{k_2}(c)=np.
\]

All cyclotomic polynomials in \(Q_4\) have constant term one. Therefore
\(F(c)\equiv H(c)\equiv1\pmod c\). Since \(p\equiv q\pmod c\) and
\(\gcd(p,c)=1\), one has \(m\equiv n\pmod c\). Write

\[
n=m+hc,
\qquad h\in\mathbb Z.
\]

The polynomial

\[
G(c)=\frac{F(c)-H(c)}c
\]

has degree at most two. Subtracting the two quotient identities gives
\(G=m-hp\), hence \(m=hp+G\). Substitution into \(H=np\) yields

\[
h p^2+(hc+G(c))p-H(c)=0. \tag{1}
\]

For \(h\ne0\), an integral solution of (1) requires

\[
y^2=D_{k_1,k_2,h}(c)
 :=(hc+G(c))^2+4hH(c). \tag{2}
\]

For \(h=0\), equation (1) becomes the finite divisibility condition
\(G(c)p=H(c)\), except that \(G=0\) is immediately impossible.

## Uniform bound for \(h\)

[PROVED] The two Hasse inequalities imply the coarse estimate

\[
|h|\le
B(c):=
\frac{16(c^4+c^3+c^2+c+1)}{(c-1)^4}
+\frac{8(c^2+c+1)}{(c-1)^2}.
\]

Each factor in

\[
\frac{c^4+c^3+c^2+c+1}{(c-1)^4}
=\left(1+c^{-1}+c^{-2}+c^{-3}+c^{-4}\right)
 \left(\frac c{c-1}\right)^4
\]

is positive and decreasing for \(c>1\); the analogous factorization proves
the same for the second summand. Thus \(B\) is decreasing. Direct integer
comparison gives \(B(108)<25\). Consequently

\[
c\ge108\quad\Longrightarrow\quad |h|\le24.
\]

[PROVED] Because odd primes have even difference, the complementary gaps are
exactly \(c=2,4,\ldots,106\). For each of the 16 ordered degree pairs and all
53 such gaps, `audit_quartic_small_gaps.py` enumerates every prime divisor
\(p\mid\Phi_{k_2}(c)\), sets \(q=p+c\), and checks the other divisibility,
primality, both Hasse inequalities, and the exact multiplicative orders. This
is a complete finite audit of 848 cases.

[EMPIRICAL: complete divisor enumeration for all 848 small-gap cases] The
only exact cycle is \((11,13;12,10)\) at \(c=2\).

## Discriminant audit for large gaps

[EMPIRICAL: exact symbolic reduction of all 16 pairs and all 49 integers
\(-24\le h\le24\)] The 784 rows split as follows:

- 750 genus-one equations after removal of square factors;
- 10 nonsquare constants times polynomial squares;
- 8 genus-zero equations after removal of square factors;
- 12 finite \(h=0\) divisibility cases; and
- 4 impossible \(h=0,G=0\) cases.

No discriminant is a square polynomial. Thus the predeclared prediction in
A016 survives.

[PROVED] `audit_quartic_degenerate_cases.py` treats all 34 non-genus-one
rows. Constant-nonsquare cases can only vanish at an integral root of their
square factor. The genus-zero cases have negative leading coefficient and
are checked through an explicit Cauchy root bound. The \(h=0\) cases reduce
to polynomial remainder divisibility and are likewise bounded by Cauchy
bounds.

[EMPIRICAL: exhaustive evaluation through every proved degenerate-case
bound] No degenerate row yields a relevant large-gap cycle. Across all gaps,
the only exact row recovered is the already audited \((11,13;12,10)\) cycle.

## Resolution of the genus-one remainder

[PROVED] Necessary congruence conditions modulo powers of two and odd primes
through 251 eliminate 630 of the 750 genus-one rows. Exact sign analysis on
\(c\ge108\) eliminates another 69. Higher-power Hensel lifting eliminates four
more rows that have singular solutions modulo 3 and 13 but no lift modulo 9
or 169. The 47 surviving rows represent 29 normalized curves after square
content and squarefree twists are handled exactly.

[EMPIRICAL: every even gap \(108\le c\le10^7\) on all 51 pre-Hensel
survivors] An exact CRT-wheel search tested 11,333,558 curve/gap candidates and
found no integral point (`search_quartic_integral_points.py`).

[EMPIRICAL: exact Magma V2.29-8 computations on all 29 final curves] Twenty-two
curves have complete integral-point lists containing only \(c=0\), except one
which also has \(c=\pm1\). Five everywhere-locally-soluble curves have empty
fake two-Selmer set and hence no rational point. The last symmetric pair is
one curve under \(c\mapsto-c\); its elliptic model has rank bounds \([0,0]\)
and torsion \(\mathbb Z/2\), so its only rational points have \(c=-1\), and
the reflected curve has only \(c=1\).

[PROVED] The finite small-gap audit, the complete large-gap reduction, the
local/archimedean eliminations, and the exact global genus-one computations
leave only \((11,13;12,10)\). This proves the theorem stated above.
