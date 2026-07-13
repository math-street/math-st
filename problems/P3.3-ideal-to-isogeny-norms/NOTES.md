# Notes

## Stable facts

[PROVED] For $p\equiv3\pmod4$, write
$B=(-1,-p)=\mathbb Q\langle i,j\rangle$ with $i^2=-1$, $j^2=-p$, and
$ij=-ji$. On the basis

$$e_0=1,\quad e_1=i,\quad e_2=(1+j)/2,\quad e_3=(i+ij)/2,$$

the reduced norm of $x=\sum_r z_r e_r$ is

$$
\operatorname{nrd}(x)=z_0^2+z_0z_2+\frac{p+1}{4}z_2^2
 +z_1^2+z_1z_3+\frac{p+1}{4}z_3^2.
$$

This follows by substituting
$x=(z_0+z_2/2)+(z_1+z_3/2)i+(z_2/2)j+(z_3/2)ij$ into
$a^2+b^2+p(c^2+d^2)$.

## Scope decisions

[PROVED] The repository contained no quaternion, isogeny, or KLPT module when
Session 1 began; this is established by the recorded workspace file listing in
the session transcript.

[HEURISTIC] Prime-norm neighbor ideals generated from uniformly sampled
nonzero norm-zero residues are a useful toy sampler, but they are not assumed
to be uniformly distributed in the ideal class group. The heuristic would be
refuted as a protocol-representative model by a comparison showing a material
distributional difference from protocol-generated ideals.

## Session 1 findings - regression only

[CITED] The chosen order is one of the explicit maximal orders in
$B_{p,\infty}$ for $p\equiv3\pmod4$, and for $x\in I$ the ideal
$I\bar x/N(I)$ is integral, equivalent to $I$, and has norm
$\operatorname{nrd}(x)/N(I)$. [Kohel--Lauter--Petit--Tignol 2014, Lemmas 2
and 5]

[PROVED] The exact search is certified by the coordinate inequality
$c_i^2\le2R(H^{-1})_{ii}$ for all vectors with doubled norm at most $2R$.
`RESULTS.md` gives the Cauchy--Schwarz argument.

[EMPIRICAL: 140 prime-neighbor ideals, $7\le p\le223$] Norm-aware LLL and the
certified exact optimum agree on every instance. Exact equivalent-ideal norms
range from 1 through 9, and $N(J)/\sqrt p$ has median 0.35921.

[EMPIRICAL: same range] No $p\bmod8$ dependence was detected. A modest
$\ell\bmod4$ difference is visible, but the intervals overlap and the
prime-neighbor sampler confounds input norm with ideal class.

[PROVED] A finite normalized theta prefix is invariant under ideal
equivalence, so different recorded fingerprints distinguish normalized norm
lattices. Equal finite prefixes may still come from different ideal classes.

[CITED] The original KLPT paper's complete basic ideal output is estimated at
$p^{7/2}$ under its heuristics; $p^3$ is the scale of an intermediate lifted
quaternion. [Kohel--Lauter--Petit--Tignol 2014, Sections 4.4--4.5]

## Correction to Session 1

[PROVED] The Session 1 distribution is class-biased in a fatal, explicit way:
for input norm $N(I)=\ell\le31$, the central element $\ell\in I$ gives
$q_I(\ell)=\ell$. Hence $N(J)\le31$ independently of $p$. Those rows validate
arithmetic but do not establish the Minkowski target line.

## Session 2 findings

[PROVED] Large prime-norm neighbors can be sampled without $O(\ell)$ rejection
by solving the order norm's quadratic discriminant modulo $\ell$ with exact
Tonelli--Shanks. The resulting ideal still passes index $\ell^2$ and left
closure checks.

[EMPIRICAL: 108 near-$p$ ideals, 12/20/28-bit $p$] Norm-aware LLL equals exact
SVP on every row. Mean $N(J)/\sqrt p$ is 0.36186, 0.37189, and 0.35809 in the
three bands, while mean exponents rise toward $1/2$.

[PROVED] The exact normalized-norm spectrum uses the same inverse-Gram box but
evaluates its integer quadratic form in overflow-checked NumPy int64 blocks.
Every stored witness is re-evaluated with the exact Python norm form.

[EMPIRICAL: 70 near-$p$ ideals, $7\le p\le223$] All rows represent powers of 2
and 3 and a 5-smooth norm by cutoff $p$. Pure-power penalties have long tails
above 20 times the unconstrained optimum, while the 5-smooth median penalty is
1.

[EMPIRICAL: measured ranges] The evidence now favors an algorithmic or
search-structural explanation for the basic KLPT gap: short unconstrained and
pure-power representatives exist in every measured class, but KLPT's sequence
of congruence and norm-equation constraints was not implemented here.

## Session 2 continuation - sparse targets

[PROVED] A single target equality can be certified without enumerating the
full norm spectrum. After inverse-Gram bounding, fix three coefficients in the
coefficient Gram form and solve the fourth quadratic exactly by an integer
square-discriminant and divisibility test. This reduced the largest encountered
full box from 5,254,365,169 tuples to 1,241,059 tested triples before finding
its witness.

[EMPIRICAL: 108 near-$p$ ideals, 12/20/28-bit $p$, targets through $4p$] Exact
$2^e$ and $3^e$ optima were uncensored on every row. Their overall median
penalties over unconstrained SVP are 222.64 and 168.23, increasing to 2476.82
and 2622.49 in the 28-bit band.

[EMPIRICAL: same range] The earlier $p\le223$ conclusion did not extrapolate:
pure-power shape is a material structural cost by 28 bits. However, all
measured shaped optima remain below $p^{1.013}$, so they do not by themselves
explain basic KLPT's heuristic $p^{7/2}$ output scale.
