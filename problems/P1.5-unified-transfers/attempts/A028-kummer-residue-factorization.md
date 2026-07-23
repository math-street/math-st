---
attempt: A028
status: theorem-proved-under-standing-erh
---
# A028 - Every explicit imaginary-quadratic target exposes a residue character

## 1. Result

- [PROVED] This attempt closes the two residual target branches left by A027.
  It does not construct a source evaluator and it does not solve SG-30.
- [PROVED] Let \(r\ge5\) be prime and let
  \(h\in\operatorname{Pic}(\mathcal O_f)\) have exact order \(r\), where
  \[
  \mathcal O_f=\mathbb Z+f\mathcal O_K
  \]
  is an order in an imaginary quadratic field. Assume the target package
  publicly supplies the fundamental discriminant \(D_K\), the conductor
  \(f\), and the factorization of \(f\); checking
  \(\operatorname{disc}(\mathcal O_f)=f^2D_K\) is polynomial time.
- [PROVED] Exactly one of the following target-side reductions applies.

  1. If \(h\) dies in \(\operatorname{Cl}(\mathcal O_K)\), the effective
     conductor inverse maps \(\langle h\rangle\) injectively to one tame
     finite-field torus or one wild additive \(\mathbb F_r\)-line.
  2. If the maximal projection \(\bar h\) is nonzero, a classical Kummer
     virtual unit for \(\bar h\), evaluated at a suitable split prime
     \(q\equiv1\pmod r\), maps \(\langle h\rangle\) injectively to
     \(\mu_r(\mathbb F_q)\).

- [PROVED] The existence and injectivity statements are unconditional. Once
  a separating \(q\) is supplied, each character evaluation is deterministic
  polynomial time in
  \[
  \log r+\log|D_K|+\log f+\log q. \tag{A028.1}
  \]
- [CONDITIONAL: GRH for the Dedekind zeta function of the normal Kummer
  closure] A separating \(q\) can be found by a Las Vegas algorithm in
  expected polynomial time and satisfies
  \[
  \log q=O(\log r+\log(\log|D_K|+2)). \tag{A028.2}
  \]
  This is the same ERH/GRH convention under which the repository invokes the
  rigorous subexponential imaginary-quadratic target algorithm.

The theorem is independent of how a source evaluator reads coordinates or
constructs its output form. It therefore covers `MAKEFORM`, arbitrary
branching, lifts, valuations, external conductor primes, and unrelated or
varying maximal quadratic fields.

## 2. The order-change dichotomy

The conductor exact sequence is
\[
\mathcal O_K^\times/\mathcal O_f^\times
\longrightarrow
(\mathcal O_K/f\mathcal O_K)^\times/
(\mathbb Z/f\mathbb Z)^\times
\longrightarrow
\operatorname{Pic}(\mathcal O_f)
\mathop{\longrightarrow}^{\pi_f}
\operatorname{Cl}(\mathcal O_K)
\longrightarrow1. \tag{A028.3}
\]
The unit groups of imaginary quadratic orders have order dividing six.
Hence, for \(r\ge5\), the unit term has no \(r\)-torsion.

Because \(\langle h\rangle\) has prime order, either
\(\pi_f(h)=1\), or \(\pi_f\) is injective on \(\langle h\rangle\). There is
no third case.

### 2.1 The conductor branch

Suppose \(\pi_f(h)=1\). The effective inverse in
Castagnos--Laguillaumie converts any reduced-form representative of \(h\) to
its conductor residue in polynomial time. CRT decomposes the middle term of
(A028.3) over primes \(\ell\mid f\). Since \(h\ne1\), at least one local
projection has order \(r\).

For \(\ell\ne r\), the local quotient has tame order
\[
\ell-\chi_K(\ell), \tag{A028.4}
\]
up to the known \(\ell\)-power factor. Its order-\(r\) subgroup is a subgroup
of \(\mathbb F_\ell^\times\) in the split case or of the norm-one torus in
\(\mathbb F_{\ell^2}^\times\) in the inert case. For \(\ell=r\), the
order-\(r\) part of the principal-unit filtration has an explicit additive
\(\mathbb F_r\) quotient. Raising away known prime-to-\(r\) cofactors and
projecting to a nonzero local component gives the claimed injective
character.

This is classical conductor-kernel arithmetic. Hühnlein--Takagi already
gave the class-number-one tame DLP reduction, and
Castagnos--Laguillaumie gave the general effective kernel isomorphism. The
conductor half of A028 is not claimed as new.

## 3. The maximal Kummer class

Now suppose
\[
\bar h=\pi_f(h)\ne1.
\]
Then \(\bar h\) has exact order \(r\) in
\(\operatorname{Cl}(\mathcal O_K)\). Choose a fractional ideal
\(\mathfrak a\) representing \(\bar h\). There is an
\(\alpha\in K^\times\) such that
\[
\mathfrak a^r=(\alpha). \tag{A028.5}
\]
Put
\[
V_r(K)=
\{\,uK^{\times r}:v_{\mathfrak p}(u)\equiv0\pmod r
\text{ for every finite }\mathfrak p\,\}. \tag{A028.6}
\]
The standard virtual-unit exact sequence is
\[
1\longrightarrow
\mathcal O_K^\times/\mathcal O_K^{\times r}
\longrightarrow V_r(K)
\longrightarrow\operatorname{Cl}(\mathcal O_K)[r]
\longrightarrow1. \tag{A028.7}
\]
Since the \(r\)-power map is an automorphism of the unit group,
(A028.7) gives a canonical isomorphism
\[
\kappa_r:
\operatorname{Cl}(\mathcal O_K)[r]
\mathop{\longrightarrow}^{\sim}V_r(K),
\qquad
[\mathfrak a]\longmapsto\alpha K^{\times r}. \tag{A028.8}
\]

This also proves well-definedness directly. Replacing
\(\mathfrak a\) by \((\beta)\mathfrak a\) replaces \(\alpha\) by
\(\epsilon\beta^r\alpha\), where
\(\epsilon\in\mathcal O_K^\times\); but \(\epsilon\) is itself an
\(r\)-th power. Products of ideals multiply the corresponding virtual
units, so \(\kappa_r\) is a homomorphism.

Finally, \(\alpha\notin K^{\times r}\). Otherwise
\(\alpha=\beta^r\), and unique factorization of fractional
\(\mathcal O_K\)-ideals in (A028.5) would give
\(\mathfrak a=(\beta)\), contrary to \(\bar h\ne1\).

## 4. A separating power-residue character

Let \(q\nmid rD_K\) be a rational prime satisfying
\[
q\equiv1\pmod r,\qquad
\left(\frac{D_K}{q}\right)=1. \tag{A028.9}
\]
Choose one prime \(\mathfrak q\mid q\), equivalently one square root of
\(D_K\) modulo \(q\). For every class \(c\in
\operatorname{Cl}(\mathcal O_K)[r]\), choose
\(\kappa_r(c)=\alpha_cK^{\times r}\), with
\(\alpha_c\) a \(\mathfrak q\)-unit, and define
\[
\lambda_{\mathfrak q}(c)
=
\alpha_c^{(q-1)/r}\bmod\mathfrak q
\in\mu_r(\mathbb F_q). \tag{A028.10}
\]
Changing \(\alpha_c\) by an \(r\)-th power does not change (A028.10).
Equation (A028.8) and multiplicativity in the residue field show that
\(\lambda_{\mathfrak q}\) is a homomorphism.

### Theorem A028.1 - unconditional separation

- [PROVED] Infinitely many pairs \((q,\mathfrak q)\) satisfying (A028.9)
  have
  \[
  \lambda_{\mathfrak q}(\bar h)\ne1. \tag{A028.11}
  \]
  Consequently \(\lambda_{\mathfrak q}\) is injective on
  \(\langle\bar h\rangle\).

**Proof.** Put \(M=K(\zeta_r)\). Since
\([M:K]\mid r-1\), restriction
\[
K^\times/K^{\times r}\longrightarrow M^\times/M^{\times r}
\]
is injective: corestriction after restriction is multiplication by
\([M:K]\), which is invertible modulo \(r\). Thus \(\alpha\) remains a
non-\(r\)-th power in \(M\), and
\[
L=M(\sqrt[r]{\alpha})/M \tag{A028.12}
\]
is a nontrivial cyclic Kummer extension.

Take the normal closure over \(\mathbb Q\); adjoining also
\(\sqrt[r]{\bar\alpha}\) suffices because \(M/\mathbb Q\) is abelian.
Choose an element of its Galois group which is trivial on \(M\) but
nontrivial on \(\sqrt[r]{\alpha}\). Chebotarev gives infinitely many
degree-one primes with this Frobenius conjugacy class. Their underlying
rational primes split completely in \(M\), so they satisfy (A028.9), and
the Kummer Frobenius formula is exactly (A028.10). If conjugation exchanges
\(\alpha\) and \(\bar\alpha\), trying the two primes over \(q\) detects the
nontrivial component. This proves (A028.11). A nonzero homomorphism from a
group of prime order is injective. \(\square\)

The pairing implicit in (A028.10) is classical: it is the Kummer pairing
between a virtual unit representing class-group \(r\)-torsion and a prime
class modulo \(r\). The new claim below is the uniform computational
factorization obtained when it is combined with compact ideal arithmetic and
the conductor dichotomy.

## 5. Compact evaluation is polynomial time

Expanding \(\alpha\) in (A028.5) is not acceptable: its ordinary coefficient
height can have \(\Theta(r\log|D_K|)\) bits. The following representation
removes that false exponential.

### Lemma A028.2 - compact principal-power generator

- [PROVED] Given a reduced imaginary-quadratic ideal \(\mathfrak a\) and an
  integer \(r\) for which \(\mathfrak a^r\) is principal, one can compute in
  time polynomial in \(\log|D_K|+\log r\) a straight-line power product for
  a generator \(\alpha\) of \(\mathfrak a^r\). The representation has
  \(O(\log r)\) multiplication/reduction nodes; every stored quadratic
  number has \(O(\log|D_K|)\)-bit numerator and denominator.

**Proof.** Binary exponentiation performs \(O(\log r)\) ideal
multiplications. Reduce after each multiplication. The inputs to each step
are reduced, so their norms are \(O(\sqrt{|D_K|})\); standard quadratic ideal
composition and reduction return both the next reduced ideal and a relative
generator of polynomial height. Record the identity
\[
\mathfrak c=\gamma\mathfrak a\mathfrak b
\]
at each reduction rather than multiplying the \(\gamma\)'s out. Squaring is
represented by a doubling edge in the straight-line graph. At the final
step the reduced representative of the principal class is the normalized
unit ideal, and the recorded graph is a generator of
\(\mathfrak a^r\), up to a bounded unit. The unit ambiguity is an \(r\)-th
power and is irrelevant to (A028.10).

Vollmer's Algorithms 4.1--4.2 give precisely this binary
power-product/relative-generator bookkeeping, and
Jacobson--Sawilla--Williams give relative-generator reduction uniformly for
quadratic discriminants. The argument above is the imaginary,
principal-output specialization. \(\square\)

### Lemma A028.3 - modular evaluation

- [PROVED] The compact \(\alpha\) from Lemma A028.2 can be evaluated in
  \(K_{\mathfrak q}\cong\mathbb Q_q\), and then in \(\mathbb F_q\), in time
  polynomial in (A028.1), even if individual compact factors have
  \(q\)-divisible denominators.

**Proof.** First shear the input form so that its leading coefficient is
prime to \(q\). The quadratic polynomial giving the leading coefficient
after a unimodular shear has at most two roots modulo \(q\), so one of the
first three residues works.

Lift the chosen square root of \(D_K\bmod q\) by Hensel lifting. For every
compact factor, compute its \(\mathfrak q\)-adic valuation and its leading
unit residue. Individual valuations have polynomial bit size because the
stored factors have polynomial height. Add valuations with their
straight-line exponents, and exponentiate the unit residues modulo \(q\).
The total valuation is zero because the sheared ideal, and hence its
\(r\)-th power, is prime to \(\mathfrak q\). Thus all apparent numerator and
denominator powers of \(q\) cancel before the final reduction, without ever
expanding \(\alpha\). Repeated squaring evaluates the graph in polynomial
time. \(\square\)

The same procedure applies to every output class \(h^x\), not only to the
fixed generator \(h\). Therefore (A028.10) is an actual target-side
postprocessor, not a one-point certificate.

## 6. Finding a short separating prime under GRH

Let
\[
N=M(\sqrt[r]{\alpha},\sqrt[r]{\bar\alpha}). \tag{A028.13}
\]
It is Galois over \(\mathbb Q\). We have
\[
[N:\mathbb Q]=O(r^3). \tag{A028.14}
\]
The virtual-unit condition says every valuation of \(\alpha\) is divisible
by \(r\). Local Kummer theory therefore makes (A028.13) unramified outside
primes above \(rD_K\), and the compositum discriminant formula gives
\[
\log|\operatorname{Disc}N|
=O\!\left(r^3(\log|D_K|+\log r)\right). \tag{A028.15}
\]
The constant is absolute; only polynomial dependence is needed here.

Bach--Sorenson's GRH bound for a prescribed Artin conjugacy class, applied
with (A028.14)--(A028.15), gives a separating rational prime
\[
q\le\bigl(r(\log|D_K|+\log r)\bigr)^{O(1)}. \tag{A028.16}
\]
This proves (A028.2).

For uniform search rather than bare existence, use the
Lagarias--Odlyzko effective Chebotarev count for the union of Frobenius
classes which is trivial on \(M\) and nontrivial on at least one Kummer
radical. At a sufficiently large explicit polynomial bound \(X\) from
(A028.14)--(A028.15), there are
\[
\Omega\!\left(\frac{X}{r\log X}\right) \tag{A028.17}
\]
accepted rational primes \(q\le X\). Sampling integers \(k\) and testing
\(q=kr+1\), primality, splitting in \(K\), and the two character values
therefore succeeds with probability \(\Omega(1/\log X)\) per trial.
Doubling \(X\) until the effective range is reached gives a Las Vegas
expected-polynomial algorithm. Every acceptance test is exact.

Unconditionally, ordinary Chebotarev proves infinitely many separating
primes, but the checked effective bounds do not make this search polynomial
in \(\log r+\log|D_K|\). This is a genuine analytic boundary, not suppressed
in the verdict.

## 7. Universal target factorization

### Theorem A028.4 - explicit quadratic-target factorization

- [PROVED, with GRH only for uniform maximal-branch setup] Let \(G\) be any
  group, let \(g\in G\) have prime order \(r\ge5\), and let
  \[
  \phi:\langle g\rangle\longrightarrow
  \operatorname{Pic}(\mathcal O_f)
  \]
  be a nonzero polynomial-time homomorphism into an explicit
  imaginary-quadratic order target. Put \(h=\phi(g)\). There is a target-side
  homomorphism \(\Lambda_h\), with polynomial-time evaluation, such that
  \[
  \Lambda_h(h)\ne1 \quad\text{or}\quad \Lambda_h(h)\ne0, \tag{A028.18}
  \]
  and its codomain is one of:

  - an order-\(r\) subgroup of \(\mathbb F_\ell^\times\);
  - an order-\(r\) subgroup of
    \(\mathbb F_{\ell^2}^\times/\mathbb F_\ell^\times\);
  - the additive group \(\mathbb F_r\);
  - \(\mu_r(\mathbb F_q)\) for a split \(q\equiv1\pmod r\).

**Proof.** Apply (A028.3). If \(\pi_f(h)=1\), Section 2 gives a nonzero local
conductor character. If \(\pi_f(h)\ne1\), it has order \(r\), and Sections
3--6 give a nonzero Kummer residue character. These cases are exhaustive.
\(\square\)

For \(Q=xg\),
\[
\Lambda_h(\phi(Q))=\Lambda_h(h)^x \tag{A028.19}
\]
in a multiplicative branch, and equals
\(x\Lambda_h(h)\) in the additive branch. Thus source DLP reduces to a
finite-field DLP, or directly to division in \(\mathbb F_r\). Conversely, the
class-group layer contributes no independent logarithmic obstruction on the
order-\(r\) image.

This theorem is strictly broader than A024 and A027:

- it makes no restriction on source coordinates or evaluator instructions;
- it permits external conductor primes;
- it permits a nonzero maximal-order component;
- \(K\) may vary with the source instance and need not be the source CM
  field.

## 8. Consequence for Q004

Let \(E/\mathbb F_p\), \(P\), and \(r\) be as in Q004, and suppose an
ordinary class evaluator
\[
\phi:\langle P\rangle\to\operatorname{Pic}(\mathcal O_f)
\]
exists. Theorem A028.4 turns it, without inspecting its implementation, into
one of the residue characters in (A028.18).

- [PROVED] Therefore an ordinary imaginary-quadratic class presentation
  cannot be a third transfer mechanism independent of finite/local residue
  characters. If \(\Lambda_h\phi\) is not an anomalous or an
  MOV/Frey--Rück character, then the genuinely new object is already the
  direct source-to-finite-field character \(\Lambda_h\phi\); the class-group
  layer is removable.
- [PROVED] This is a factorization theorem, not a proof that the original
  \(\phi\) cannot exist and not a claim that every resulting finite-field
  character is pairing-derived.
- [CONDITIONAL: the standing ERH/GRH target-algorithm convention] This closes
  novelty-grade Q004 for explicit imaginary-quadratic ordinary-class
  targets. No coordinate/lift/valuation/`MAKEFORM` evaluator can evade the
  target dichotomy.
- [OPEN outside the standing convention] An unconditional uniform
  polynomial-time construction of the separating maximal-branch prime is not
  supplied by the checked effective Chebotarev theorems.

At the A028 stage, SG-30 remained separate: A028 starts from a supplied order
and order-\(r\) target class. It neither constructs a succinct prescribed-order
target nor uses such a construction.

A029 subsequently closes that separate target-only problem by taking the
Gaussian order of conductor \(r^2\). This does not alter any A028 proof.

## 9. Infinite-family and computation check

- [CITED] Lim proves that, for every squarefree odd integer \(n>1\), there
  are infinitely many imaginary quadratic **fields** whose maximal class
  groups contain an element of exact order \(n\). Taking \(n=r\) and
  applying Sections 3--6 to any such class proves that the maximal Kummer
  branch contains infinitely many targets for every fixed odd prime \(r\);
  each target in turn has infinitely many separating split primes. This is
  an existence family, not a uniform succinct constructor, so it does not
  settle SG-30.

A019 supplies the following particularly simple exact-order test fixture in
an imaginary quadratic **order**, for every odd prime \(r\):
\[
D_r=1-4\cdot2^r,\qquad
\omega={1+\sqrt{D_r}\over2},\qquad
\mathfrak a=(2,\omega),\qquad
\mathfrak a^r=(\omega), \tag{A028.20}
\]
with \([\mathfrak a]\) of exact order \(r\). It is an oversized target and
does not solve SG-30. Moreover, \(D_r\) is not known to be a fundamental
discriminant for every prime \(r\), so A019 alone must not be called an
infinite maximal-order family. At any split
\(q\equiv1\pmod r\),
\[
\lambda_{\mathfrak q}([\mathfrak a])
=\omega^{(q-1)/r}\bmod\mathfrak q. \tag{A028.21}
\]

`code/probe_kummer_class_character.py` checks (A028.20)--(A028.21) for
\[
r=3,5,7,11,13,17,19,23,29,31.
\]
For every case it finds a nontrivial character, verifies exact order \(r\),
and recovers all \(r\) scalar logarithms. Nontriviality also certifies in
these ten cases that the extended ideal has nonzero maximal projection. The
full CSV is
`data/probe_kummer_class_character_full_20260723.csv`.

A025 independently supplies an infinite succinct conductor-branch family.
Lim supplies the maximal-branch infinitude theorem, while A019 supplies the
explicit regression fixtures. Together they exercise both sides of the
dichotomy. A029 later gives a uniform succinct conductor-branch target for
every odd prime \(r\); the harder maximal-order constructor is not part of
SG-30 as stated.

## 10. Prior-art and novelty verdict

- [CITED] The order-change exact sequence and effective conductor inverse are
  classical and appear in Cox, Hühnlein--Takagi, and
  Castagnos--Laguillaumie.
- [CITED] The virtual-unit exact sequence and Kummer pairing are classical
  class field theory; Breen--Varma--Voight give a modern explicit
  Selmer/pairing presentation in the \(2\)-primary setting.
- [CITED] Vollmer and Jacobson--Sawilla--Williams supply the compact
  ideal-power and relative-generator machinery.
- [CITED] Lagarias--Odlyzko and Bach--Sorenson supply the GRH-effective
  Frobenius-prime bounds.
- [EMPIRICAL: bounded primary-source search through 2026-07-23] Searches for
  `class group discrete logarithm` together with `Kummer pairing`,
  `power-residue symbol`, `virtual unit`, and `finite-field reduction` found
  the classical pairing literature and the totally nonmaximal
  Hühnlein--Takagi reduction, but no checked source stating Theorem A028.4's
  full conductor/maximal computational dichotomy for prime-order subgroups
  of imaginary-quadratic Picard groups.
- [PROVED] The repository-original contribution is the synthesis in Theorem
  A028.4 and its Q004 consequence. None of its classical ingredients is
  relabeled as new.

## 11. Falsifiers and scope

- A source evaluator into a number field of degree greater than two is
  outside this theorem.
- A target supplied only as a bare discriminant, without a certified
  maximal discriminant, conductor, and conductor factorization, is outside
  the stated polynomial-time interface.
- Removing GRH from the uniform maximal-branch auxiliary-prime search would
  strengthen the theorem.
- Finding a checked paper which already gives the complete effective
  dichotomy would downgrade the repository-original synthesis claim.
- A genuinely new positive Q004 mechanism must now avoid ordinary explicit
  imaginary-quadratic class targets altogether, or explain why factoring
  through the finite/local residue character is itself the intended new
  source mechanism.
