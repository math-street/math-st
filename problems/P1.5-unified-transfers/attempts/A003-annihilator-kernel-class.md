---
attempt: A003
status: dead
---
# A003 - Map a CM point through its annihilator or kernel isogeny

## Idea

- [CONJECTURE] The annihilator ideal of $Q$, the kernel $\langle Q\rangle$, or
  the corresponding quotient curve might provide a computable class-group
  label that varies homomorphically with $Q$; one varying label would refute
  this conjectural construction's negative assessment.

## Prior art

- [CITED] For an $\mathcal O$-oriented elliptic curve, an invertible ideal
  $\mathfrak a$ defines $E[\mathfrak a]=\bigcap_{\alpha\in\mathfrak a}
  \ker\iota(\alpha)$ and hence a horizontal isogeny; the output depends on the
  ideal class and gives a free action on oriented curves
  (Castryck--Houben--Vercauteren--Wesolowski 2022, Section 2.2).
- [PROVED] This standard construction has direction
  $[\mathfrak a]\mapsto(E',\iota')$ and does not by itself assign an ideal
  class to a point.

## Plan

- [PROVED] Use ordinary $j=1728$ curves where the automorphism
  $[i](x,y)=(-x,iy)$ is explicit, choose a cyclic prime factor that occurs once
  in $\#E(\mathbb F_p)$, and exhaust every nonzero multiple of a generator.
- [PROVED] Compare CM eigenvalues, annihilator relations, kernel point sets,
  and canonicalized Velu quotients.

## Execution log

- [EMPIRICAL: 8 curves, 13 <= p <= 421, 5 <= r <= 113, 368 nonzero points]
  `code/probe_cm_class_targets.py` found exactly one CM eigenvalue, one
  annihilator label, one cyclic kernel, and one canonical Velu quotient per
  source subgroup; see `data/probe_cm_class_targets_full_20260702.csv`.
- [EMPIRICAL: the same 8 curves] Exhaustive reduced-form enumeration gave
  Frobenius-order class numbers from 1 through 12, while the actual
  $j=1728$ endomorphism order $\mathbb Z[i]$ had class number 1 in every case.

## Outcome

- [PROVED] Let $R\subseteq\operatorname{End}(E)$ and let $P$ have prime order
  $r$.  For $1\le n<r$, multiplication by $n$ is an automorphism of
  $\langle P\rangle$, so
  $\alpha(nP)=0\Leftrightarrow n\alpha(P)=0\Leftrightarrow\alpha(P)=0$.
  Therefore $\operatorname{Ann}_R(nP)=\operatorname{Ann}_R(P)$.
- [PROVED] The same scalar range gives $\langle nP\rangle=\langle P\rangle$,
  so every construction determined only by the cyclic kernel, including its
  quotient isogeny up to isomorphism, is constant on all nonzero source points.
- [PROVED] If a homomorphism from a group of odd prime order is constant with
  value $c$ on nonzero points, then $c=\phi(2P)=2\phi(P)=2c$, hence $c=0$;
  such a map is not injective.

### Endomorphism-order size obstruction

- [CITED] If $\mathcal O$ has conductor $f$ in an imaginary quadratic field
  of fundamental discriminant $d_K$, its class number is
  $$h(\mathcal O)=\frac{h(d_K)f}{[\mathcal O_K^\times:\mathcal O^\times]}
    \prod_{\ell\mid f}\left(1-\frac{\chi_{d_K}(\ell)}{\ell}\right)$$
  (Cox 2013, Theorem 7.24; independently restated by Booher 2014,
  Proposition 3).
- [CITED] The imaginary-quadratic analytic class-number formula is
  $h(d_K)=w_K\sqrt{|d_K|}L(1,\chi_{d_K})/(2\pi)$ (Milne 1997,
  Chapter VI, Section 2).
- [PROVED] For a nontrivial character modulo $d=|d_K|$,
  $|L(1,\chi)|\le\log d+2$: the first $d$ terms are bounded by
  $H_d\le\log d+1$; in each later block, subtracting $1/(kd)$ uses
  $\sum_{a=1}^d\chi(a)=0$, and the absolute errors sum to less than
  $\sum_{k\ge1}1/(2k^2)<1$.
- [PROVED] Since $w_K\le6$ and
  $\prod_{\ell\mid f}(1+1/\ell)\le H_f\le\log f+1$, an order of
  discriminant $\Delta=f^2d_K$ satisfies
  $$h(\Delta)\le\frac{3}{\pi}\sqrt{|\Delta|}
    (\log|\Delta|+2)^2.$$
- [PROVED] For an ordinary elliptic curve over $\mathbb F_q$ with trace $t$,
  $t^2-4q=f_\pi^2\Delta_{\operatorname{End}(E)}$, so
  $|\Delta_{\operatorname{End}(E)}|\le4q$ and
  $$h(\operatorname{End}(E))\le\frac{6}{\pi}\sqrt q
    (\log(4q)+2)^2.$$
- [PROVED] The ratio of the last bound to $q/2$ decreases for $q\ge2$ and is
  below 1 at $q=2^{21}$; therefore, for $q\ge2^{21}$ and $r\ge q/2$, the
  endomorphism-order class group has order less than $r$ and cannot contain an
  injective image of $\langle P\rangle$.

## Post-mortem

**Why it failed:** [PROVED] Annihilators and kernel isogenies depend on the
unoriented cyclic subgroup, not on the choice of generator; additionally, the
curve's own endomorphism class group is asymptotically too small in the stated
large-prime regime.

**What transfers:** [PROVED] A target derived from a point must preserve
generator orientation; any invariant that factors through
$Q\mapsto\langle Q\rangle$ is automatically useless on a prime-order source.

**Would it work under different assumptions?** [PROVED] The size obstruction
does not cover $r\ll q$ or a separately constructed order of much larger
discriminant, but the annihilator/kernel constancy proof is independent of
sizes and still applies.
