---
attempt: A008
status: dead
---
# A008 - CRT decoding as a short-interval smooth-number finder

## Idea

[CONJECTURE] Boneh's CRT list-decoding method might enumerate the
polylog-smooth order whose existence follows under RH in A007, avoiding an
exponential scan of the abelian-surface interval.

## Prediction and decision rule

[CONJECTURE] The algorithm will require a stronger promise than ordinary
$y$-smoothness, such as a sufficiently large strongly $s$-smooth divisor.
The prediction is refuted if the checked theorem provably lists every
$y$-smooth integer in an interval of length $X^{3/4}$ in time polynomial in
$\log X$ and $y$, or if Younis's stated asymptotic uniformly guarantees the
exact promise required by the decoder.

## Exact decoder guarantee

[CITED] Boneh 2002, Definition 3.1, calls $N$ strongly $s$-smooth when every
prime power dividing $N$ is at most $s$.  With

$$
 S=\prod_{p<s}p^{\lfloor\log s/\log p\rfloor},
$$

the strongly $s$-smooth integers are exactly the divisors of $S$.

[CITED] Boneh 2002, Theorem 3.1, gives the following algorithmic guarantee.
For $I=[U,V]$, $H=V-U$, and

$$
 d\ge1+\sqrt{\frac{\log S}{\log H}},\qquad
 \varepsilon=\sqrt{\frac{\log(4H)}{\log S}}+\frac5{4d},
$$

CRT list decoding finds every $N\in I$ with
$\gcd(N,S)>T$ when $T>S^\varepsilon$, in time polynomial in $d$ and the bit
sizes of $(U,V,S,T)$.  If $V<2T$, every strongly $s$-smooth $N\in I$ meets
the promise and is output.

[PROVED] Let $L=\log X$ and take the A007 interval scale
$U\asymp X$, $H=X^{3/4+o(1)}$.  Listing all strongly smooth values requires
$T>V/2$, hence $\log T=(1+o(1))L$.  Letting $d$ grow can remove the
$5/(4d)$ term but cannot remove the square-root term, so a necessary limit
of Boneh's sufficient condition is

$$
 \log(4H)<\frac{(\log T)^2}{\log S}.
$$

[CITED] The prime number theorem in Chebyshev-function form gives
$\log S=(1+o(1))s$.

[PROVED] Put $s=L^K$ for any fixed $K>1$, as in the polylogarithmic range
available from Younis after increasing the fixed exponent if necessary.
Boneh's limiting right-hand side is then

$$
 \frac{(\log T)^2}{\log S}=L^{2-K+o(1)}=o(L),
$$

whereas $\log H=(3/4+o(1))L$.  Thus the decoder inequality fails for every
choice of $d$, even if the desired integer is promised to be strongly
$s$-smooth.

## The only asymptotic parameter window the decoder reaches

[PROVED] If $s=c\log X$ with fixed $c>0$, then
$\log S=(c+o(1))\log X$ and the limiting decoder width is

$$
 H\le X^{1/c+o(1)}.
$$

For a divisor of $S$ to lie near $X$, one needs $S\ge X$, which asymptotically
requires $c\ge1$.  Reaching $H=X^{3/4}$ additionally requires $c\le4/3$.
Hence the full-order application is confined to the narrow scale
$s=c\log X$ with $1\le c\le4/3$, not $s=(\log X)^K$ for $K>1$.

[PROVED] Strongly $c\log X$-smooth integers are globally sparse.  Every one
divides $S$, and

$$
 \log\tau(S)
 \le \pi(s)\log\!\left(1+\frac{\log s}{\log2}\right)
 =o(\log X).
$$

Thus there are at most $X^{o(1)}$ such integers in total.  Among the
$X^{1/4+o(1)}$ disjoint intervals of length $X^{3/4}$ in $[X,2X]$, the
proportion containing one is at most $X^{-1/4+o(1)}$.

[PROVED] This average-scarcity statement does not prove that the special
intervals centered near $r^2$ are empty.  It does prove that an every-prime
existence theorem at this stronger smoothness scale would require new
arithmetic structure and cannot be read off from Younis's ordinary
polylog-smooth asymptotic.

## Outcome

[PROVED] The prediction understated the obstruction.  Younis counts ordinary
smooth integers whereas Boneh lists values with large strongly smooth
divisors, but even granting strong smoothness does not help: the decoder's
parameter inequality misses the $X^{3/4}$ interval whenever
$s=(\log X)^K$ with fixed $K>1$.

## Post-mortem

**Why it failed:** [PROVED] The CRT modulus has
$\log S\asymp s$.  Making the smoothness threshold a high fixed power of
$\log X$ enlarges $S$ so much that the list-decoding radius corresponds only
to intervals with logarithmic width $o(\log X)$, not $X^{3/4}$.

**What transfers:** [PROVED] The exact missing finder is now sharper: it must
exploit the distribution or representation of ordinary polylog-smooth
integers, rather than treating them as divisors or large divisors of one CRT
modulus.

**Would it work under different assumptions?** [PROVED] Yes, if one were
given the much stronger promise that the target interval contains a strongly
$c\log X$-smooth integer for some fixed $1\le c<4/3$.  No checked existence
theorem supplies that promise, and such values are sparse on average.
