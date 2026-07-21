---
attempt: A007
status: completed
---
# A007 - Abelian-surface existence versus construction

## Idea

[CONJECTURE] The wider point-count interval in dimension two should move the
smooth-number problem away from the excluded square-root endpoint and yield a
conditional every-prime existence theorem.  The result may still fail to be
a Maurer reduction because an explicit smooth integer, an explicit surface,
and a strong embedding algorithm are separate requirements.

## Prediction and decision rule

[CONJECTURE] Under the Riemann Hypothesis, a polylog-smooth order exists in a
central universally realizable abelian-surface interval for every sufficiently
large prime $r$.  The prediction is refuted if the fixed-dimension
prescribed-order interval has exponent at most $1/2$ when measured around
$X=r^2$, or if the RH smooth-number theorem does not reach polylogarithmic
smoothness at that interval exponent.  Even if confirmed, it is not promoted
to an algorithm unless both the smooth order and an explicit strongly
algebraically defined surface are constructible in $\operatorname{poly}(\log
r)$ time.

## A conditional existence theorem

[CITED] Van Bommel--Costa--Poonen--Smith--Li 2025, Theorem 1.7 and Remark
1.11, imply the following fixed-dimension statement for prime fields: for any
fixed $0<\lambda<4-2\sqrt2$, every integer in

$$
  [r^2-\lambda r^{3/2},\ r^2+\lambda r^{3/2}]
$$

is the order of an ordinary abelian surface over $\mathbb F_r$ once $r$ is
sufficiently large.

[CITED] Assuming the Riemann Hypothesis, Younis 2024, Theorem 1.3, gives the
expected smooth-number asymptotic in every interval
$[X,X+X^\theta]$ for each fixed $\theta>1/2$, provided
$y\ge(\log X)^{K(\theta)}$ for a sufficiently large constant $K(\theta)$.

[CONDITIONAL: Riemann Hypothesis] Choose a fixed $\lambda$ with
$1/2<\lambda<4-2\sqrt2$ and a subinterval of the displayed realizable interval
having length $X^{3/4}$, where $X=r^2+O(r^{3/2})$.  Such a subinterval exists
because $X^{3/4}=r^{3/2}(1+o(1))$.  Apply Younis with $\theta=3/4$ and
$y=(\log X)^{K(3/4)}$.  Its positive asymptotic count supplies a $y$-smooth
integer $N$ in that subinterval for every sufficiently large prime $r$.
Because $\log X=(2+o(1))\log r$, this is

$$
  P^+(N)\le(\log r)^{O(1)}.
$$

[CONDITIONAL: Riemann Hypothesis] The prescribed-order theorem then supplies
an ordinary abelian surface $A/\mathbb F_r$ with
$|A(\mathbb F_r)|=N$.  Thus a polylog-smooth full abelian-surface order exists
for every sufficiently large prime.  This is an existence theorem only.

[PROVED] The same synthesis is unavailable unconditionally from the checked
sources.  Younis's unconditional theorem at $\theta=3/4$ requires
$y\ge\exp((\log X)^{2/3+\varepsilon})$, which is super-polylogarithmic.

## When an explicit genus-two Jacobian would suffice

[CITED] Cantor 1987 gives fixed-genus arithmetic in the Jacobian of a
hyperelliptic curve using reduced divisor (Mumford) representations.

[PROVED] Let $C:y^2=f(x)$ be an explicitly supplied nonsingular genus-two
curve over an odd prime field, with $f$ squarefree of degree five.  Its
Jacobian elements have constant-size Mumford representations, and Cantor
arithmetic uses a constant number of polynomial operations of bounded degree.
Hence its group law uses only $O(1)$ explicit or implicit field operations
outside the usual inversion cost.

[CITED] The Weil character-sum bound gives
$|\sum_{X\in\mathbb F_r}\chi(f(X))|\le4\sqrt r$.

[PROVED] Given an implicit input $x$ and a public random
$e\in\mathbb F_r$, set $X=x+e$, test whether $f(X)$ is a square, and, on
success, compute an implicit square root $Y$.  The divisor class
$[(X,Y)-\infty]$ has Mumford representation

$$
  u(z)=z-X,\qquad v(z)=Y.
$$

The character bound and at most five roots of $f$ show that a trial succeeds
with probability $1/2+O(r^{-1/2})$, so the expected number of trials is
bounded.  Extraction reads $X$ from $u$ and returns $X-e=x$.

[PROVED] For every prime $\ell\ne r$, the $\ell$-torsion of a dimension-two
abelian variety embeds in $(\mathbb Z/\ell\mathbb Z)^4$; its $r$-rank is no
larger.  Hence $J(C)(\mathbb F_r)$ has group rank at most four.  Together with
the preceding embedding and Cantor arithmetic, an explicit genus-two
Jacobian is a constant-rank strongly algebraically defined Maurer--Wolf
auxiliary group.

## Why conditional existence is not a construction

[PROVED] Younis's asymptotic count does not output a smooth $N$ in
$\operatorname{poly}(\log r)$ time.  Enumerating the $r^{3/2+o(1)}$-length
interval is exponential in the input length.

[PROVED] The prescribed-order theorem produces a realizable Weil polynomial
and an isogeny-class existence statement; it does not by itself output an
explicit genus-two curve, a Mumford representation, or the Maurer--Wolf
`EMBED` and `EXTRACT` algorithms.

[CITED] Bröker--Howe--Lauter--Stevenhagen 2015 prove that genus-two CM
constructions for prescribed Jacobian order have exponential worst-case
running time.  Their heuristic polynomial-time construction solves a
different inverse problem--prescribing $|C(\mathbb F_p)|$, not
$|J(C)(\mathbb F_p)|$--so it does not provide an alternative bridge here.

[PROVED] Therefore the RH synthesis proves every-prime smooth-order
**existence** for abelian surfaces but not a uniform CDH-to-DLP reduction.
The two missing algorithms are now explicit:

1. [PROVED] Given $r$, find a polylog-smooth $N$ in the central
   $r^{3/2}$-length interval in time polynomial in $\log r$.
2. [PROVED] Given $(r,N)$, construct an explicit strongly algebraically
   defined abelian surface of order $N$ in time polynomial in $\log r$;
   an explicit genus-two Jacobian would suffice.

## Outcome

[PROVED] The prediction was confirmed exactly at the existence level and
refuted as a complete algorithmic route.  Dimension two removes the
short-interval endpoint obstruction under RH, but it exposes a smooth-number
search problem and a prescribed-order realization problem that the cited
theorems do not solve uniformly.
