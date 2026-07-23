---
attempt: A027
status: theorem-proved-residual-open
---
# A027 - Intrinsic-conductor support forces a known source regime

## 1. Statement

Let \(E/\mathbb F_p\) be ordinary, with Frobenius trace \(t\), and put
\[
K=\operatorname{End}(E)\otimes\mathbb Q.
\]
Let \(P\in E(\mathbb F_p)\) have odd prime order \(r\ne p\), and assume
\[
r>h(\mathcal O_K),\qquad r>2\sqrt p+2. \tag{A027.1}
\]
For \(f\ge1\), put \(\mathcal O_f=\mathbb Z+f\mathcal O_K\).
Call the target **intrinsic-conductor supported** when every prime dividing
\(f\) belongs to \(\{p,r\}\).

### Theorem A027.1 - intrinsic-support trichotomy

- [PROVED] Let
  \[
  \phi:\langle P\rangle\longrightarrow\operatorname{Pic}(\mathcal O_f)
  \]
  be a nonzero homomorphism into an intrinsic-conductor-supported target.
  Then at least one of the following holds.

  1. The \(r\)-conductor projection is nonzero. The effective conductor
     inverse followed by the local logarithm turns \(\phi\) into an
     \(\mathbb F_r\)-valued linearizer. Thus one evaluation on \(Q=xP\),
     together with the fixed value on \(P\), recovers \(x\) in polynomial
     time.
  2. The \(p\)-conductor projection is nonzero. Necessarily \(r\mid p-1\)
     and \(t=2\). Hence the source already has embedding degree one and lies
     in the Frey--Rück multiplicative-transfer regime.

In particular, an ordinary large-prime CM subgroup outside the anomalous and
small-embedding-degree regimes cannot acquire a genuinely class-specific
transfer by passing to an order in its own CM field whose conductor is built
only from the two intrinsic primes \(p\) and \(r\).

## 2. Projection to the maximal order vanishes

The conductor exact sequence contains
\[
\operatorname{Pic}(\mathcal O_f)
\mathop{\longrightarrow}^{\pi_f}
\operatorname{Pic}(\mathcal O_K)\longrightarrow1. \tag{A027.2}
\]
The composite \(\pi_f\phi\) is a homomorphism from a group of prime order
\(r\). If it were nonzero it would be injective, forcing
\(r\mid h(\mathcal O_K)\), contrary to (A027.1). Therefore
\[
\phi(\langle P\rangle)\subseteq\ker\pi_f. \tag{A027.3}
\]

This step is automatic in the standard cryptographic large-prime range.
A003 proves, for \(p\ge2^{21}\), that
\[
h(\operatorname{End}(E))
\le {6\over\pi}\sqrt p\,(\log(4p)+2)^2.
\]
Since \(h(\mathcal O_K)\le h(\operatorname{End}(E))\), the first condition in
(A027.1) follows whenever the displayed bound is smaller than \(r\).

## 3. Local decomposition

After quotienting the bounded global-unit image, the conductor kernel is a
quotient of
\[
T_f=(\mathcal O_K/f\mathcal O_K)^\times/
(\mathbb Z/f\mathbb Z)^\times. \tag{A027.4}
\]
For \(r\ge5\), the unit quotient has no \(r\)-torsion. CRT and the local order
formula give
\[
|T_{\ell^e}|=\ell^{e-1}
  \bigl(\ell-\chi_K(\ell)\bigr). \tag{A027.5}
\]
Because \(E\) is ordinary, \(p\) splits in \(K\), so
\(\chi_K(p)=1\): otherwise \(p\mid t\), and Hasse would force \(t=0\),
the supersingular case. Consequently
\[
|T_{p^a}|=p^{a-1}(p-1). \tag{A027.6}
\]
At least one local projection of the order-\(r\) image is nonzero.

## 4. The source-characteristic branch collapses to trace two

Suppose the \(p\)-local projection is nonzero. Since \(r\ne p\),
(A027.6) implies \(r\mid p-1\). On the other hand,
\[
r\mid\#E(\mathbb F_p)=p+1-t.
\]
Subtracting the two multiples of \(r\) gives \(r\mid2-t\). Hasse's bound and
(A027.1) yield
\[
|2-t|\le2+2\sqrt p<r,
\]
so
\[
t=2,\qquad \#E(\mathbb F_p)=p-1,\qquad
\operatorname{ord}_r(p)=1. \tag{A027.7}
\]
Moreover \(r>2\sqrt p+2\) gives \(r^2>p-1=\#E(\mathbb F_p)\), so the
order-\(r\) source is not contained in \(rE(\mathbb F_p)\). Nondegeneracy of
the Tate--Lichtenbaum/Frey--Rück pairing therefore supplies a nonzero
character into
\(\mathbb F_p^\times/\mathbb F_p^{\times r}\). Thus a \(p\)-supported tame
ring-class target can occur only on a source already exposed to the
embedding-degree-one pairing transfer. This conclusion uses no restriction
on how \(\phi\) reads coordinates or builds its output form.

## 5. The subgroup-order branch is an explicit linearizer

Suppose the \(r\)-local projection is nonzero. Castagnos--Laguillaumie's
effective kernel isomorphism converts a canonical reduced-form output to a
residue in \(T_{r^b}\) in polynomial time when the conductor is public.
For completeness, after moving the form to a conductor-coprime ideal
\(\mathfrak a\), extend it to \(\mathcal O_K\). Equation (A027.3) says the
extension is principal. In the complex embedding, a shortest nonzero vector
of a principal ideal \(\alpha\mathcal O_K\) has absolute norm
\(|N(\alpha)|\), because every nonzero multiplier in \(\mathcal O_K\) has
nonzero integral norm of magnitude at least one. Exact two-dimensional Gauss
reduction therefore finds a generator in polynomial bit complexity; reducing
that generator modulo \(f\) gives the conductor residue.

For odd \(r\), the \(r\)-primary part of \(T_{r^b}\) is a one-dimensional
local unit quotient. In the unramified case a nonzero order-\(r\) projection
requires \(b\ge2\), and the \(r\)-adic logarithm gives
\[
(1+r\mathcal O_{K,r})/(1+r^b\mathcal O_{K,r})
\big/
(1+r\mathbb Z_r)/(1+r^b\mathbb Z_r)
\;\cong\;\mathbb Z/r^{b-1}\mathbb Z. \tag{A027.8}
\]
The residue-field quotient has order \(r-\chi_K(r)\), which is prime to
\(r\) in this unramified branch. After raising by this known cofactor, every
order-\(r\) residue is represented uniquely modulo rational units by
\[
1+r^{b-1}a\tau,\qquad a\in\mathbb F_r, \tag{A027.9}
\]
for any fixed basis \(1,\tau\) of \(\mathcal O_{K,r}\).

In the ramified case choose a local basis
\(\mathcal O_{K,r}=\mathbb Z_r[\varpi]\) with
\(\varpi^2=ur\), \(u\in\mathbb Z_r^\times\). Modulo rational units, every
unit has a unique parameter \(c\) in the form \(1+c\varpi\), with group law
\[
c\oplus d={c+d\over1+urcd}. \tag{A027.10}
\]
Modulo \(r\) this is addition. More generally, the order-\(r\) subgroup
modulo \(r^b\) consists exactly of \(c=r^{b-1}a\), and (A027.10) again
reduces to addition of \(a\in\mathbb F_r\). Thus both ramified and
unramified cases have an explicit additive coordinate. The bounded global
unit quotient is removed by raising to its known order, coprime to \(r\);
this changes the coordinate by a known nonzero scalar only.

Let this coordinate be \(\lambda\). Nonzero projection means
\(\lambda(\phi(P))\ne0\). Therefore, for \(Q=xP\),
\[
x=
\lambda(\phi(Q))\lambda(\phi(P))^{-1}\pmod r. \tag{A027.11}
\]
This is not a new subexponential class-group mechanism: it is a complete
polynomial-time source linearizer if the evaluator exists.

## 6. External-prime necessity beyond the theorem

Drop the intrinsic-support condition, retain (A027.1), and suppose neither
branch of Theorem A027.1 is allowed. Any nonzero conductor projection must
then occur at a prime \(\ell\notin\{p,r\}\). Formula (A027.5) forces
\[
r\mid\ell-\chi_K(\ell). \tag{A027.12}
\]
Thus:

- if \(\ell\) splits, then \(\ell\equiv1\pmod r\); writing
  \(\ell-1=mr\), parity forces \(m\) even, so \(\ell\ge2r+1\);
- if \(\ell\) is inert, then \(\ell\equiv-1\pmod r\), and because \(r-1\)
  is an even integer greater than two, \(\ell\ge2r-1\);
- a ramified \(\ell\ne r\) cannot carry the order-\(r\) image.

Accordingly, every still-genuine same-CM-field counterexample must introduce
an external prime of size at least \(2r-1\), contributing at least
\(2\log_2(2r-1)\) bits to the target discriminant through its squared
conductor, and compute a cross-characteristic character into its split or
inert finite-field torus. This is a precise
falsifier, not a claim that the external-prime branch is impossible.

## 7. Prior-art and novelty verdict

- [CITED] Cox, Conrad, Kopp--Lagarias, and
  Castagnos--Laguillaumie supply the order-change exact sequence and its
  effective kernel description.
- [CITED] Hühnlein--Takagi already identify the tame class-number-one
  conductor kernel with finite-field DLP.
- [PROVED] Those results remove A026's proposed novelty.
- [EMPIRICAL: bounded primary-source search through 2026-07-23] No checked
  source states the source-side implication
  \[
  \text{\(p\)-local order-\(r\) ring-class image}
  \Longrightarrow r\mid p-1\Longrightarrow t=2
  \]
  together with the intrinsic/external conductor trichotomy.
- [PROVED] Theorem A027.1 is a new repository theorem and is strictly broader
  than A024 in evaluator access: it permits arbitrary polynomial-time
  coordinate, lift, valuation, branching, and direct `MAKEFORM` behavior.
  Its target scope is narrower: the order must lie in the source CM field and
  have intrinsic conductor support.
- [OPEN] The external-prime cross-characteristic character in Section 6 and
  the varying/unrelated maximal-order component remain outside the theorem.
  Therefore A027 is a real structural advance but does not honestly complete
  unrestricted novelty-grade Q004.
