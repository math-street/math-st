# P1.5 rational-transfer theorem package and proof audit

**Audit date:** 2026-07-23

**Scope:** attempts A008--A013 and their circuit consequences

**Verdict:** the affine, proper, and mixed-target arguments form a
repository-original synthesis of restricted classification statements. The
original affine \(B^3\) branch bound is
correct but not sharp; the proof below improves it to \(B^2\). This is not an
unrestricted classification of polynomial-time transfers, and the literature
audit below is not a certified novelty claim.

## 1. Conventions and complexity parameter

Let \(k\) be a perfect field, let \(E/k\) be an elliptic curve with identity
\(0\), and let

\[
C=\langle P\rangle\subset E(k)
\]

have prime order \(r\). The intended application has \(k=\mathbb F_q\), so
perfectness imposes no additional restriction. An algebraic group is a
separated group scheme of finite type over \(k\). Smoothness is stated where
it is used.

For an affine algebraic group \(H\), fix a faithful closed immersion

\[
\rho:H\hookrightarrow \operatorname{GL}_s.
\]

If \(F:E\dashrightarrow H\) is a \(k\)-rational map, write
\(\rho F=(f_{ij})\). On \(E_{\bar k}\), define its **common pole degree** by

\[
\delta_\rho(F)=\deg \mathcal P(F),\qquad
\mathcal P(F)=\sum_{x\in E(\bar k)}
  \max_{i,j}\{0,-\operatorname{ord}_x(f_{ij})\}[x].
\]

Equivalently, \(\mathcal P(F)\) is the least effective divisor \(A\) for which
every \(f_{ij}\) lies in \(L(A)\). Defining the degree after base change is
essential: all zero counts below take place on the geometric curve. The
quantity is representation-dependent, so every quantitative statement fixes
\(\rho\); a non-faithful representation would make the conclusions false.

A piecewise rational evaluator consists of a partition into nonempty sets

\[
C=S_1\sqcup\cdots\sqcup S_B
\]

and \(k\)-rational maps \(F_a:E\dashrightarrow H\), with \(F_a\) defined at
every point of \(S_a\). No geometric or algorithmic regularity is assumed of
the sets \(S_a\). In particular, the branch partition may be adversarial.

## 2. Elementary pole lemmas

### Lemma 2.1 -- zeros versus poles

If \(u\in\bar k(E)\) is nonzero, then the degree of its zero divisor equals the
degree of its pole divisor. Hence a rational function with more distinct
regular zeros than its pole degree is identically zero.

This is the usual degree-zero property of a principal divisor. It is valid in
every characteristic.

### Lemma 2.2 -- invariant vector poles

Let \(V:E\dashrightarrow \operatorname{Mat}_{m,n}\) be rational and let
\(M\in\operatorname{GL}_m(\bar k)\), \(N\in\operatorname{GL}_n(\bar k)\).
Multiplication by \(M\) or \(N\) does not change the common pole divisor of the
entries of \(V\).

**Proof.** At a geometric point \(x\), multiplication by a constant matrix
cannot increase the largest pole order among the entries. Applying the inverse
constant matrix gives the reverse inequality. Thus the largest pole order is
unchanged at every \(x\). \(\square\)

Consequently, if \(T\in E(k)\) has order \(r\) and
\(V(X+T)=M V(X)N\), then \(\mathcal P(V)\) is invariant under translation by
\(T\). Every geometric translation orbit has exactly \(r\) points, so a
nonzero invariant effective divisor has degree at least \(r\).

## 3. Affine rational rigidity

### Theorem 3.1 -- one rational branch

Let \(H/k\) be affine, let \(F:E\dashrightarrow H\) be defined at every point
of \(C\), and suppose \(F|_C:C\to H(k)\) is a group homomorphism. Put
\(D=\delta_\rho(F)\). If \(r>2D\), then \(F\) is the constant identity map.
Therefore every nontrivial rational subgroup homomorphism, and hence every
injective one, satisfies

\[
D\ge \frac r2.
\]

**Proof.** Put \(M=\rho(F(P))\). For each matrix entry, consider

\[
g_{ij}(X)=f_{ij}(X+P)-\sum_{\ell=1}^s f_{i\ell}(X)M_{\ell j}.
\]

The first term has pole divisor bounded by a translate of
\(\mathcal P(F)\), and the second by \(\mathcal P(F)\). Thus \(g_{ij}\) has
pole degree at most \(2D\). For every \(X\in C\), both sides are defined and
the subgroup law gives \(g_{ij}(X)=0\). Since \(r>2D\), Lemma 2.1 gives the
rational identity

\[
\rho(F(X+P))=\rho(F(X))M. \tag{3.1}
\]

By faithfulness, this is an identity in \(H\). Lemma 2.2 makes
\(\mathcal P(F)\) invariant under translation by \(P\). Its degree is at most
\(D<r\), whereas every nonempty orbit has size \(r\); hence
\(\mathcal P(F)=0\). All entries of \(\rho F\) are global regular functions
on the proper geometrically connected curve \(E\), hence constants. Thus
\(F\) is constant. Since \(0\in C\) and \(F|_C\) is a homomorphism, the
constant is the identity. \(\square\)

This proof audits the translation issue in A008. Translation introduces a
translated pole divisor, so the defect bound is \(2D\), not \(D\). Once the
defect vanishes, translation invariance removes the poles; no unproved
specialization of a two-variable denominator is needed.

Faithfulness cannot be dropped. Composing any nontrivial map with the trivial
representation gives displayed pole degree zero. Likewise, an abstract map
defined only on \(C\), with no rational extension \(E\dashrightarrow H\), is
outside the theorem.

## 4. Piecewise affine rigidity

### Theorem 4.1 -- exact overlap obstruction

Let \(\phi:C\to H(k)\) be an injective homomorphism. Suppose that on each of
\(B\) nonempty branch sets \(S_a\), it agrees with a rational map \(F_a\) of
common pole degree at most \(D\). Put \(m=\lceil r/B\rceil\). Then

\[
m(m-1)\le 2D(r-1). \tag{4.1}
\]

In particular, with \(D_+=\max(1,D)\),

\[
D_+B^2\ge \frac r4. \tag{4.2}
\]

**Proof.** Choose a largest branch \(S\), so \(|S|=n\ge m\), and let \(F\)
be its rational map. For \(t\in C\), put

\[
R(t)=|S\cap(S-t)|
     =|\{x\in S:x+t\in S\}|.
\]

Counting ordered pairs in \(S^2\) by their difference gives

\[
\sum_{t\in C}R(t)=n^2,\qquad R(0)=n,
\]

and therefore some nonzero \(t\in C\) satisfies

\[
R(t)\ge \frac{n(n-1)}{r-1}. \tag{4.3}
\]

Suppose \(R(t)>2D\). For every \(x\) counted by \(R(t)\), homomorphy and the
fact that both \(x,x+t\) lie in \(S\) give

\[
F(x+t)=\phi(x+t)=\phi(t)F(x).
\]

Every entry of

\[
\rho(F(X+t))-\rho(\phi(t))\rho(F(X)) \tag{4.4}
\]

has pole degree at most \(2D\) and more than \(2D\) regular zeros. Lemma 2.1
makes (4.4) a rational identity. Because \(t\ne0\) and \(r\) is prime, \(t\)
has order \(r\). Lemma 2.2 makes \(\mathcal P(F)\) translation-invariant.
Moreover \(R(t)>2D\) implies \(D<r\), so \(\mathcal P(F)=0\). The map \(F\)
is constant, and (4.4), multiplied by its invertible constant value, gives
\(\rho(\phi(t))=I\). Faithfulness contradicts injectivity of \(\phi\).

Thus \(R(t)\le2D\) for every nonzero \(t\). Summing gives

\[
n(n-1)=\sum_{t\ne0}R(t)\le2D(r-1),
\]

and monotonicity in \(n\ge m\) proves (4.1).

For (4.2), first suppose \(r<2B\). Then
\(D_+B^2\ge B^2>r^2/4\ge r/4\). If \(r\ge2B\) and (4.2) were false, then
\(m\ge r/B\), \(m-1\ge r/(2B)\), and

\[
m(m-1)\ge\frac{r^2}{2B^2}>2D_+r>2D(r-1),
\]

contradicting (4.1). \(\square\)

### Audit of the old \(B^3\) proof

The A010 triple-color proof is valid: coloring \((X,Y)\) by the branches of
\(X,Y,X+Y\) gives a cell of size at least \(r^2/B^3\), and its two zero counts
give \(D_+B^3\ge r/4\). It is nevertheless weaker than Theorem 4.1.
Same-branch differences use only one branch color and improve the exponent
from \(3\) to \(2\). No regularity of the branch sets is used.

The exact inequality (4.1) is retained because it is stronger than the coarse
constant in (4.2). Whether the exponent can improve from \(2\) to \(1\) under
no assumptions on the partition remains open here. Standard Riemann--Roch
interpolation gives branchwise upper constructions of degree on the order of
the branch size, but it does not prove a matching lower bound for the
structured values of a subgroup homomorphism.

## 5. Proper targets

### Theorem 5.1 -- one rational proper-target map

Let \(H/k\) be a smooth proper algebraic group and let
\(F:E\dashrightarrow H\) be defined at \(0\). If \(F(0)=1_H\), then \(F\)
extends uniquely to a global algebraic-group homomorphism \(E\to H^0\). In
particular, the conclusion holds if \(F\) is homomorphic on \(C\). Its image
is either trivial or an elliptic abelian subvariety, and in the latter case
\(E\to F(E)\) is an isogeny.

**Proof.** A rational map from the normal curve \(E\) to the proper variety
\(H\) extends uniquely to a morphism. The image of the connected curve lies
in one connected component; because it contains \(1_H\), it lies in \(H^0\).
Over the perfect field \(k\), the smooth connected proper group \(H^0\) is an
abelian variety. A morphism of abelian varieties sending zero to zero is a
homomorphism by the rigidity lemma. The image of a nonconstant homomorphism
from \(E\) is a one-dimensional abelian subvariety, and the
zero-dimensional kernel makes the induced map an isogeny. \(\square\)

The subgroup law away from \(0\) is not needed. This observation rules out
constant translations: a morphism \(t\alpha\) is pointed only when \(t=1\).

### Theorem 5.2 -- fewer than \(r\) proper-target branches

Let \(\phi:C\to H(k)\) be any homomorphism. Suppose a partition of \(C\) into
\(B<r\) nonempty sets has rational branch maps \(F_b:E\dashrightarrow H\)
that agree with \(\phi\) on their branch sets. Then there is one global
algebraic-group homomorphism \(\beta:E\to H^0\) with
\(\beta|_C=\phi\). If \(\phi\) is injective, the image of \(\beta\) is
elliptic and isogenous to \(E\).

**Proof.** Some branch contains distinct \(X,Y\). Properness extends its map
\(F\) to a morphism. Put \(t=F(0)\). Its connected image is contained in
\(tH^0\), and

\[
\alpha(Z)=t^{-1}F(Z):E\longrightarrow H^0
\]

is pointed, hence a homomorphism by rigidity. Since \(H^0\) is normal,
\(\beta=\operatorname{Int}(t)\circ\alpha:E\to H^0\) is also a homomorphism.
Using the order of factors, which matters when \(H\) is noncommutative,

\[
\begin{aligned}
\phi(X-Y)
 &=F(X)F(Y)^{-1}\\
 &=t\alpha(X)\alpha(Y)^{-1}t^{-1}\\
 &=\beta(X-Y).
\end{aligned}
\]

The nonzero element \(X-Y\) generates the prime-order group \(C\), so the two
homomorphisms agree on all of \(C\). The final image statement follows from
Theorem 5.1. \(\square\)

This proof explicitly handles disconnected and noncommutative \(H\). The
branch translation \(t\) need not lie in \(H^0\); conjugation by it preserves
the normal subgroup \(H^0\).

## 6. Mixed algebraic groups

### Theorem 6.1 -- fibrewise low-defect criterion

Let \(H/k\) be a smooth algebraic group and let
\(F:E\dashrightarrow H\) be defined on \(C\), with \(F|_C\) a homomorphism.
The rational image lies in \(H^0\). By Chevalley's theorem there is an exact
sequence

\[
1\longrightarrow L\longrightarrow H^0
  \mathop{\longrightarrow}^{\pi}A\longrightarrow1, \tag{6.1}
\]

where \(L\) is connected affine and \(A\) is an abelian variety. Fix a
faithful representation \(\rho:L\hookrightarrow\operatorname{GL}_m\).

The pointed rational map \(\pi F\) extends to a homomorphism
\(\alpha:E\to A\). Define the \(L\)-valued rational defect

\[
c(X,Y)=F(X+Y)(F(X)F(Y))^{-1}. \tag{6.2}
\]

For every entry

\[
u_{ij}(X,Y)=(\rho(c(X,Y))-I)_{ij},
\]

assume the following intrinsic pole bounds after base change to \(\bar k\):

1. for every \(Q\in C\), the rational function \(u_{ij}(X,Q)\) on \(E_X\)
   has pole degree at most \(D\); and
2. as a rational function of \(Y\) on \(E_{\bar k(E_X)}\),
   \(u_{ij}(X,Y)\) has pole degree at most \(D\).

If \(D<r\), then \(F\) extends to a global algebraic-group homomorphism
\(E\to H^0\). Its image is trivial or elliptic and isogenous to \(E\).

**Proof.** The regular domain of \(F\) is irreducible and contains \(0\), so
its image lies in the identity component. Proper-target rigidity applied to
\(\pi F\) gives \(\alpha\). Therefore applying \(\pi\) to (6.2) gives the
identity, so \(c\) indeed takes values in \(L\). On \(C^2\), homomorphy gives
\(c=1\).

Fix \(Q\in C\). Each \(u_{ij}(X,Q)\) has the \(r\) points of \(C\) as regular
zeros and pole degree at most \(D<r\); Lemma 2.1 makes it zero identically in
\(X\). Thus, over the coefficient field \(\bar k(E_X)\), every
\(u_{ij}(X,Y)\) vanishes at the \(r\) distinct constant points \(Y=Q\).
The second pole bound and Lemma 2.1 make it identically zero. Faithfulness of
\(\rho\) gives \(c=1\), so \(F\) is a rational group homomorphism.

To remove an apparent pole at a geometric point \(a\), choose \(y\) in the
dense regular locus with \(a+y\) also in that locus. The rational identity

\[
F(X)=F(X+y)F(y)^{-1}
\]

is regular near \(a\) and extends \(F\) there. Uniqueness of these local
extensions gives a global homomorphism over \(\bar k\), and uniqueness also
gives Galois descent to \(k\). The image classification is the standard one
for a homomorphism from an elliptic curve. \(\square\)

### Why the specialization hypotheses are explicit

A generic bidegree quoted from a displayed quotient does not by itself certify
the degree of a specialized fibre: a denominator can vanish vertically, and
an unsimplified presentation can introduce fake vertical factors. The theorem
therefore measures the intrinsic pole divisor after restriction and requires
a uniform bound at every \(Q\in C\), as well as the generic bound in the
second zero count. Under a geometric presentation by a common effective pole
divisor on \(E\times E\), these conditions can instead be certified by
fibre-intersection degrees and the absence of vertical pole components over
\(C\).

The contrapositive is precise: if \(F\) is not global, then for the fixed
faithful representation either a specialized \(X\)-fibre in item 1 or the
generic \(Y\)-fibre in item 2 has pole degree at least \(r\). There is no
representation-free degree conclusion.

## 7. Rational decision-tree corollary

The mathematical theorem does not turn an arbitrary polynomial-time program
into a low-degree map. The following explicit model is required.

For each instance, a **rational decision-tree evaluator** has:

1. base rational functions on \(E\), each of pole degree at most \(D_0\ge1\);
2. binary arithmetic gates \(+,-,\times,/\) over \(k\), with every division
   valid on the inputs routed through that computation path;
3. at most \(b\) binary decisions on any root-to-leaf path, so there are at
   most \(B\le2^b\) branch transcripts;
4. on each transcript, arithmetic depth at most \(d\); and
5. \(M\) output entries giving a fixed faithful matrix representation of the
   affine target.

Branch predicates may be arbitrary. The theorem charges them only through the
number of binary decisions; after a transcript is fixed, the output must be
the stated rational circuit. Loops must be unrolled into the charged depth. A
uniform bit-complexity interpretation additionally requires the field,
constants, circuit descriptions, target representation, and field operations
to have polynomial encoding and cost.

### Lemma 7.1 -- circuit pole growth

If rational functions have pole degrees at most \(a,b\), then each of their
sum, difference, product, and quotient has pole degree at most \(a+b\). For a
quotient, poles of \(u/v\) are bounded by poles of \(u\) plus zeros of \(v\),
and a nonzero rational function has equally many zeros and poles. Induction on
binary arithmetic depth gives pole degree at most \(2^dD_0\) for each output.
The sum of the \(M\) output pole divisors is a common pole divisor of degree

\[
D\le M2^dD_0. \tag{7.1}
\]

### Corollary 7.2 -- arithmetic/branch depth

If the evaluator is an injective subgroup homomorphism into an affine target,
then Theorem 4.1 and (7.1) give

\[
d+2b\ge\log_2 r-\log_2(4MD_0). \tag{7.2}
\]

For \(MD_0=(\log r)^{O(1)}\) and
\(n=\lceil\log_2r\rceil\), this is

\[
d+2b\ge n-O(\log n).
\]

With no branching, Theorem 3.1 gives the sharper

\[
d\ge\log_2r-\log_2(2MD_0).
\]

These are depth lower bounds in a restricted algebraic model, not
superpolynomial time lower bounds. Depth \(\Theta(n)\), polynomial circuit
size, and polynomial bit complexity are compatible. Miller evaluation is the
standard example: a linear-length/depth straight-line program represents a
function whose expanded degree is exponential in the input bit length.

## 8. Self-attack and boundary table

| Attack | Result |
|---|---|
| Constant map | The identity map satisfies every homomorphism identity but is not injective. The affine lower bounds are stated for nontrivial/injective maps. |
| Translation \(t\alpha\) | Proper-target rigidity permits a translation for an arbitrary morphism, but subgroup homomorphy forces the value at zero to be \(1\), hence removes it. In the piecewise proof, the branch translation is handled by conjugation. |
| Disconnected target | A connected single-map image containing the identity lies in \(H^0\). A proper branch may lie in \(tH^0\); Theorem 5.2 does not assume \(t\in H^0\). |
| Noncommutative target | Matrix defects use the stated order of factors. The proper branch proof produces \(\operatorname{Int}(t)\circ\alpha\), and the mixed defect is \(L\)-valued without assuming \(L\) commutative. |
| Non-faithful representation | This is a genuine counterexample to any degree claim stated without faithfulness; all quantitative theorems fix a faithful closed immersion. |
| Exceptional characteristic or \(r=\operatorname{char}k\) | The zero counts and translation-orbit arguments remain valid. Perfectness is used only for the smooth Chevalley decomposition and the standard abelian-variety description. |
| Purely inseparable homomorphism | It is still an isogeny onto its elliptic image. No separability of the global homomorphism is assumed. |
| Formula defined only on \(C\) | Outside scope. The theorem requires one rational map per branch on \(E\), not merely a table or an abstract subgroup map. |
| \(r\) singleton proper branches | The \(B<r\) collapse theorem no longer applies, and arbitrary values can be represented by constant branches. Explicitly storing them is exponential in \(\log r\), but that is an SG-01 setup argument, not an algebraic-geometric theorem. |
| Adversarial affine partition | Covered: Theorem 4.1 uses only the largest branch and the exact difference identity \(\sum_tR(t)=|S|^2\). |
| Vertical denominators | Covered only under the explicit fibrewise assumptions of Theorem 6.1. A generic displayed degree without these assumptions is insufficient. |
| Polynomial-time evaluator | Not automatically covered. One must first supply the faithful algebraic representation and rational decision-tree realization with controlled \(D_0,M,d,b\). |

## 9. Standard ingredients versus repository synthesis

The following ingredients are standard.

- Degree-zero principal divisors give the curve zero count.
- Affine algebraic groups admit faithful linear representations.
- A rational map from a normal curve to a proper variety extends uniquely.
- A pointed morphism of abelian varieties is a homomorphism by rigidity.
- Over a perfect field, Chevalley's theorem decomposes a smooth connected
  algebraic group into a connected affine kernel and an abelian quotient.
- A nonzero homomorphism from an elliptic curve has elliptic image and is an
  isogeny onto that image.

The repository-original synthesis, subject to the novelty caveat below, is the
application of those ingredients to a map promised homomorphic only on one
prime-order rational subgroup, yielding:

- the representation-relative affine bound \(D\ge r/2\);
- the exact piecewise overlap obstruction (4.1) and the \(D_+B^2\) bound;
- the decision-tree depth bound \(d+2b\ge n-O(\log n)\);
- the \(B<r\) proper-branch collapse including disconnected/noncommutative
  targets; and
- the fibrewise affine-defect criterion for a mixed target.

## 10. Prior-art search and interpolation reconciliation

The initial search on 2026-07-20 covered algebraic-group interpolation, zero
estimates, rational-function values in subgroups, and algebraic computation
trees. A023 adds the closer cryptographic interpolation and efficiently
computable-homomorphism lines that the initial pass missed.

### 10.1 Cryptographic polynomial interpolation

- Coppersmith--Shparlinski, *On Polynomial Approximation of the Discrete
  Logarithm and the Diffie--Hellman Mapping*, *Journal of Cryptology* 13
  (2000), 339--360, is the closest quantitative predecessor. Their Theorem 1
  proves, for a polynomial of degree $d$ agreeing with the scalar discrete
  logarithm on arbitrary $S\subseteq\mathbb F_p^\times$,

  \[
  d\ge\frac{|S|(|S|-1)}{2(p-2)}. \tag{10.1}
  \]

  The proof chooses a quotient represented by many ordered pairs and
  zero-counts a multiplicative translate defect. Thus the quadratic
  subset-over-ambient-size mechanism behind Section 4 has direct prior art.
- Winterhof, *Polynomial Interpolation of the Discrete Logarithm*, *Designs,
  Codes and Cryptography* 25 (2002), 63--72, extends most of that line to
  arbitrary finite fields. The requested Meidl--Winterhof attribution is a
  bibliographic conflation: Meidl--Winterhof's distinct 2002 paper is *A
  Polynomial Representation of the Diffie--Hellman Mapping*.
- Lange--Winterhof, *Polynomial Interpolation of the Elliptic Curve and XTR
  Discrete Logarithm*, COCOON 2002, proves an elliptic-coordinate scalar bound
  for exponent samples dense in an interval. Its arbitrary-subset XTR and
  multiplicative-subgroup bounds again have quadratic
  $|S|(|S|-1)/(\text{ambient size})$ form, with trace or digit-carry losses.
- Kiltz--Winterhof, *Polynomial Interpolation of Cryptographic Functions
  Related to Diffie--Hellman and Discrete Logarithm Problem*, *Discrete
  Applied Mathematics* 154 (2006), 326--336, relates useful low-degree
  interpolants of transformed finite-field cryptographic functions to
  algorithms for the underlying hard problems and proves corresponding
  degree bounds.

Equation (10.1) recovers $D_+B^2=\Omega(r)$ after choosing a largest branch
in its scalar finite-field specialization. It does **not** state Theorem 4.1:
the repository theorem concerns rational maps on an elliptic curve into an
arbitrary affine algebraic group, with degree measured by common poles in a
fixed faithful matrix representation. Likewise, the checked interpolation
papers do not cover the proper-branch or mixed Chevalley-defect theorems.

The character-sum refinements do not improve $B^2$ toward $B$ for an
adversarial partition. Their linear degree estimates require dense intervals,
random samples, or other distribution hypotheses. For arbitrary $S\subset C$,

\[
\sum_{t\ne0}|S\cap(S-t)|=|S|(|S|-1),
\]

so the universally guaranteed overlap remains of order $|S|^2/r$, exactly
the scale producing $D=\Omega(r/B^2)$. Whether another argument can exploit
several branches jointly and improve the exponent to $1$ remains open.

### 10.2 Homomorphism consequences and generic/concrete boundaries

- Verheul, *Evidence that XTR Is More Secure than Supersingular Elliptic
  Curve Cryptosystems*, EUROCRYPT 2001 / *Journal of Cryptology* 17 (2004),
  proves that an efficient reverse homomorphism from the XTR group to the
  relevant paired supersingular elliptic subgroup makes Diffie--Hellman easy
  in both groups. Moody, ePrint 2008/456 / *Designs, Codes and Cryptography*
  52 (2009), generalizes the consequence using computable pairings and
  distortion maps. This is conceptual prior art for SG-23's strategy of
  deriving a hard-problem consequence from an efficient cross-group map.
- Koblitz--Menezes, *Another Look at Generic Groups*, *Advances in Mathematics
  of Communications* 1 (2007), stresses that a generic model excludes special
  features of concrete encodings and that coordinate or implementation
  structure must be audited separately. This is conceptual prior art for
  SG-14's generic-versus-coordinate boundary.

### 10.3 Remaining general literature and verdict

Masser, Fischler, and Fischler--Nakamaye study interpolation and obstruction
subgroups on commutative algebraic groups. Gomez-Perez--Shparlinski studies
rational-function values in finite-field subgroups. Miller records the short
program versus expanded-degree distinction, and Ben-Or supplies a different
algebraic-computation-tree precedent.

A023 assigns a verdict to each of the five synthesis items. None is derivable
as stated from the checked interpolation results, but the scalar half-degree
scale, the quadratic arbitrary-subset overlap mechanism, and the
degree-to-depth idea have clear prior art. The proper and mixed results remain
outside the checked interpolation scope. The appropriate description is
therefore **repository-original synthesis**, not a novelty or priority claim.
A broader MathSciNet/Zentralblatt search and expert review would still be
needed for any publication-level novelty statement.

Primary links:

- <https://doi.org/10.1007/s001450010002>
- <https://doi.org/10.1023/A:1012556500517>
- <https://doi.org/10.1007/3-540-45655-4_16>
- <https://doi.org/10.1016/j.dam.2005.03.030>
- <https://www.cs.ru.nl/E.Verheul/papers/Joc2004/joc2004.pdf>
- <https://eprint.iacr.org/2008/456>
- <https://eprint.iacr.org/2006/230>
- <https://arxiv.org/abs/1205.4088>

## 11. Regression certificate and remaining classes

The script [audit_rational_tradeoffs.py](code/audit_rational_tradeoffs.py)
exhausts cyclic subsets at small prime orders and checks the exact identity

\[
\sum_{t\ne0}|S\cap(S-t)|=|S|(|S|-1)
\]

and the integer constants used in Theorem 4.1. Its tests are a falsification
guard for the combinatorial reduction, not a proof of the
algebraic-geometric theorem.

The rational theorem package by itself leaves open:

- polynomial-length valuation/factor-base programs beyond A024's transcript
  lower bound, and direct raw-coordinate-to-form operations outside VFB;
- rational maps or affine defects at the permitted high degree;
- linear-depth polynomial-size circuits, including Miller-type programs;
- succinct targets with no polynomial-size faithful algebraic presentation;
- at least \(r\) proper-target formulas given implicitly rather than stored;
- mixed-target maps failing the explicit fibrewise degree bounds; and
- the connection between any such evaluator and a genuinely subexponential
  target DLP algorithm.

The formerly open target-only prescribed-order construction is no longer on
this list. A029 gives, for every odd prime \(r\), the exact order-\(r\)
reduced form \([r^2,2r,r^2+1]\) in discriminant \(-4r^4\). This does not
address any rational evaluator residual above.

## 12. Final classification status

P1.5 now contains a **repository-original synthesis of restricted
classification statements** that survived this proof audit and the A023
prior-art reconciliation. The proper-target part is mainly a standard
rigidity reformulation; the affine statements broaden known scalar
interpolation mechanisms to rational maps with faithful affine targets, and
the package also includes the explicit circuit and controlled mixed-target
consequences.

It is not a solution of the unrestricted P1.5 problem and makes no certified
claim of literature novelty, priority, or publishability.

After this rational audit, A025 supplies a control construction for the former
literal Q004 checklist by composing the known degree-two pairing with an
ordinary ring-class presentation. It does not close novelty-grade Q004. A026
then tested the conductor-kernel route, but its hoped-for effective inverse is
prior art: Hühnlein--Takagi (1999) reduce the totally nonmaximal
class-number-one case to finite-field DLP, and
Castagnos--Laguillaumie (2009) give the effective conductor-kernel isomorphism
for general conductor.

A027 contributes a source-side theorem outside the rational models above. For
an ordinary large-prime subgroup, a target order in the same CM field whose
conductor is supported on \(p,r\) either gives an explicit
\(\mathbb F_r\)-linearizer or forces \(r\mid p-1\), whence Hasse forces trace
two and embedding degree one. It permits arbitrary coordinate, lift,
valuation, branching, and direct form construction.

A028 subsequently closes A027's two target residuals under the standing
ERH/GRH convention. The conductor exact sequence puts every prime-order image
either in the known effective local residue quotient or injectively in the
maximal class group. In the latter case
\(\mathfrak a^r=(\alpha)\) gives a canonical virtual unit, and a separating
split prime gives the Kummer character
\[
[\mathfrak a]\longmapsto
\alpha^{(q-1)/r}\bmod\mathfrak q\in\mu_r(\mathbb F_q).
\]
Compact relative-generator tracking makes evaluation polynomial, while
effective Chebotarev makes short-prime setup expected-polynomial under GRH.
Thus arbitrary ordinary quadratic-class evaluators factor through
finite/local residue characters even when they lie outside every rational
model in this review. This later target theorem does not change any proof in
Sections 3--8 and does not promote their individual ingredients beyond
repository-original synthesis.

A029 then closes the independent SG-30 target-construction question
unconditionally: conductor \(r^2\) in \(\mathbb Q(i)\) gives the
\(\Theta(\log r)\)-bit discriminant \(-4r^4\) and exact order-\(r\) reduced
form \([r^2,2r,r^2+1]\). Its explicit additive conductor logarithm places it
inside A028's known residue branch; it does not supply or classify a source
evaluator.
