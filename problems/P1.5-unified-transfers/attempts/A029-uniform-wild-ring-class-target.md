---
attempt: A029
status: theorem-proved
---
# A029 - A uniform succinct exact-order ring-class target

## 1. Result

- [PROVED] SG-30 has an unconditional positive solution. On input any odd
  prime \(r\), put
  \[
  K=\mathbb Q(i),\qquad
  f=r^2,\qquad
  \mathcal O_r=\mathbb Z+r^2\mathbb Z[i].
  \]
  The order has discriminant
  \[
  \Delta_r=-4r^4. \tag{A029.1}
  \]
- [PROVED] The primitive reduced positive form
  \[
  F_r=[\,r^2,\ 2r,\ r^2+1\,] \tag{A029.2}
  \]
  represents a class of exact order \(r\) in
  \(\operatorname{Pic}(\mathcal O_r)\).
- [PROVED] If \(n=\lceil\log_2r\rceil\), then
  \[
  \log_2|\Delta_r|=2+4\log_2r=\Theta(n), \tag{A029.3}
  \]
  so the target lies strictly inside the SG-25 window
  \[
  2n-O(\log n)\le\log_2|\Delta_r|
  =o(n^2/\log n). \tag{A029.4}
  \]
- [PROVED] Computing \((\Delta_r,F_r)\), checking the certificate below, and
  performing target operations all take deterministic time polynomial in
  \(\log r\). No auxiliary-prime search, ERH/GRH assumption, class-number
  computation, or integer factorization is required.

This closes the target-only prescribed-order problem. It does not construct a
source point-to-class evaluator.

## 2. Conductor quotient

Let
\[
\mathcal O_K=\mathbb Z[i],\qquad
\mathcal O_r=\mathbb Z+r^2\mathbb Z[i].
\]
The conductor exact sequence gives
\[
1\longrightarrow
\mathcal O_K^\times/\mathcal O_r^\times
\longrightarrow
(\mathcal O_K/r^2\mathcal O_K)^\times/
(\mathbb Z/r^2\mathbb Z)^\times
\longrightarrow
\operatorname{Pic}(\mathcal O_r)
\longrightarrow1, \tag{A029.5}
\]
because \(\operatorname{Cl}(\mathbb Z[i])=1\). The residue-to-class map is
\[
z\longmapsto
[\,z\mathcal O_K\cap\mathcal O_r\,]. \tag{A029.6}
\]
The first term of (A029.5) is represented by the Gaussian units
\(\{\pm1,\pm i\}\), modulo the units already in \(\mathcal O_r\).

Put
\[
z_r=1+ri\pmod {r^2}. \tag{A029.7}
\]
It is a unit because
\[
N(z_r)=1+r^2\equiv1\pmod {r^2}.
\]

## 3. Exact-order proof

### Theorem A029.1

- [PROVED] The image of \(z_r\) under (A029.6) has exact order \(r\).

**Proof.** The binomial theorem gives
\[
(1+ri)^r\equiv1\pmod {r^2}: \tag{A029.8}
\]
the linear term is \(r^2i\), and every higher term contains \(r^2\).
Therefore the image order divides \(r\).

It is not the identity. A residue in the kernel of the map to
\(\operatorname{Pic}(\mathcal O_r)\) is a rational unit modulo \(r^2\)
times one of \(\{\pm1,\pm i\}\). Such a residue has either zero imaginary
coordinate or zero real coordinate. The residue \(1+ri\) has neither
coordinate zero modulo \(r^2\), since \(0<r<r^2\). Thus its class is
nontrivial. Because \(r\) is prime, its order is exactly \(r\).
\(\square\)

The same calculation gives a complete subgroup:
\[
(1+rai)(1+rbi)\equiv1+r(a+b)i\pmod {r^2}, \tag{A029.9}
\]
so
\[
\mathbb F_r^+\longrightarrow\operatorname{Pic}(\mathcal O_r),
\qquad
a\longmapsto[\,1+rai\,] \tag{A029.10}
\]
is an injective homomorphism.

## 4. Closed form and reduction certificate

For \(z_r=1+ri\), solve the contraction explicitly:
\[
z_r\mathcal O_K\cap\mathcal O_r
=
[\,1+r^2,\ -r^3+r^2i\,]. \tag{A029.11}
\]
Indeed,
\[
(1+ri)(x+yi)
=(x-ry)+(rx+y)i,
\]
and the imaginary coordinate is divisible by \(r^2\) exactly when
\(y=-rx+r^2k\). Taking \((x,k)=(1,0)\) and \((0,1)\) gives the displayed
basis.

Under the standard correspondence
\[
[A,B,C]\longleftrightarrow
[\,A,\ (-B+\sqrt{\Delta})/2\,],
\]
(A029.11) is the primitive form
\[
\widetilde F_r
=
[\,1+r^2,\ 2r^3,\ r^4\,],\qquad
\operatorname{disc}(\widetilde F_r)=-4r^4. \tag{A029.12}
\]
Primitivity follows from \(1+r^2\equiv1\pmod r\).

Its reduction is completely explicit. Apply the integral shift
\(s=-r\):
\[
[1+r^2,2r^3,r^4]
\sim
[1+r^2,-2r,r^2],
\]
then swap the outer coefficients and reverse the middle sign:
\[
[1+r^2,-2r,r^2]
\sim
[r^2,2r,r^2+1]=F_r. \tag{A029.13}
\]
The last form is reduced because
\[
|2r|\le r^2\le r^2+1
\]
for every odd \(r\). It is primitive and has discriminant \(-4r^4\).
Equations (A029.8), (A029.11), and (A029.13) are therefore a
polynomial-size exact-order certificate for the canonical output form.

## 5. Uniformity, target size, and target logarithm

Binary multiplication computes \(r^2,r^3,r^4\) in
\((\log r)^{O(1)}\) bit operations. The largest output has \(O(\log r)\)
bits, and the reduction certificate consists of two elementary
\(\mathrm{SL}_2(\mathbb Z)\) steps. This proves uniform deterministic
polynomial-time construction.

The class-number formula independently gives
\[
h(-4r^4)
=
\frac{r^2}{2}
\left(1-\frac{\chi_{-4}(r)}r\right)
=
\frac{r(r-\chi_{-4}(r))}{2}, \tag{A029.14}
\]
which is divisible by \(r\). This count is a consistency check; the explicit
class proof does not rely on computing it.

The target logarithm on the constructed subgroup is transparent. For a
residue projectively normalized as \(1+rai\pmod {r^2}\), return
\[
\log_{\rm wild}(1+rai)=a\pmod r. \tag{A029.15}
\]
The effective conductor inverse of Castagnos--Laguillaumie converts any
reduced form in this subgroup back to such a residue in polynomial time.
Thus the order-\(r\) target DLP is polynomial, which is stronger than SG-25's
subexponential requirement.

## 6. Why earlier constructions missed it

- A019 forced exact order through
  \(\mathfrak a^r=(\alpha)\), placing an \(r\)-th power in the
  discriminant and producing \(\Theta(r)\) bits.
- A020 showed empirically that small targets exist but found them by class
  number census.
- A021 searched mainly for maximal-order prescribed torsion and
  \(n\)-th-power discriminant families.
- A025 used conductor \(p\) and an auxiliary prime
  \(p\equiv-1\pmod r\), because it needed compatibility with a
  degree-two pairing source.
- A026 already isolated the wild principal-unit line at conductor \(r^2\)
  and even wrote (A029.12) with a general parameter. It was correctly
  rejected as a new Q004 mechanism, but its target-only consequence for
  SG-30 was not extracted.

SG-30 does not require maximality or source compatibility. Once those
extraneous requirements are removed, the wild conductor line gives the
uniform family immediately.

## 7. Prior-art and novelty verdict

- [CITED] The conductor exact sequence, contraction map, and class-number
  formula are classical; Conrad gives (A029.5)--(A029.6) explicitly.
- [CITED] Castagnos--Laguillaumie give the effective conductor-kernel
  isomorphism and its inverse for general imaginary-quadratic conductors.
- [CITED] The local principal-unit filtration and its additive
  characteristic-\(r\) quotient are standard.
- [PROVED] Therefore the algebraic ingredients and the existence of wild
  \(r\)-torsion at conductor \(r^2\) are not claimed as new.
- [EMPIRICAL: bounded primary-source search through 2026-07-23] No checked
  source was found stating the exact closed reduced family (A029.2) as a
  uniform prescribed-order constructor with the SG-25 bit audit. The
  repository contribution is this extraction and complete certification,
  not the conductor theory itself.

## 8. Relation to A028 and Q004

A029 is fully consistent with A028. Its target lies in A028's conductor
branch, and (A029.15) is precisely the exposed additive
\(\mathbb F_r\)-character. Consequently:

- [PROVED] A029 closes SG-30 positively.
- [PROVED] It does not reopen Q004 or create a new transfer mechanism.
- [PROVED] Any nonzero source evaluator into this subgroup would recover the
  source scalar in polynomial time after one conductor inversion.

The result is nevertheless important as a target theorem: it removes the
uniform prescribed-order construction gap completely.

## 9. Infinite-family validation

`code/construct_sg30_ring_class_target.py` implements the constructor and
certificate. Its permanent full output is
`data/construct_sg30_ring_class_target_full_20260723.csv`.

- [EMPIRICAL: 15 primes \(3\le r\le10007\), target discriminants at most
  56 bits] Every output has the claimed raw and canonical forms, exact
  conductor-residue order, class-number multiple, and SG-25 size.
- [EMPIRICAL: \(r=3,5,7\)] Complete reduced-form enumeration independently
  matches (A029.14).
- [EMPIRICAL: \(r=3,5,7,11\), every parameter pair] Direct Gaussian
  multiplication verifies the additive law (A029.9), and the \(r\)
  parameters reduce to \(r\) distinct canonical forms.

## 10. Falsifiers and scope

- The theorem assumes \(r\) is an odd prime. Composite prescribed orders
  require a separate exact-order analysis.
- Requiring a maximal order would invalidate this construction and restore
  the difficult prescribed-torsion problem studied in A021.
- Requiring the target to avoid an explicit additive logarithm would also
  invalidate it, but that is not part of SG-30.
- A source evaluator is outside this target-only theorem.
