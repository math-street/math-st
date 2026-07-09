# Notes — P2.2

## Stable facts — result in one paragraph

[EMPIRICAL: primary-title, author, and ePrint-oriented literature searches run
on 2026-07-09] I found no later primary paper giving either an unrestricted
prime-order reduction of $q$-SDH to a fixed-size assumption or an impossibility
theorem for every representation-specific black-box reduction.

[CITED] The scoped meta-reduction alternative is known: Lu and Zhandry prove that no fully
black-box, representation-independent generic-group reduction can base a
prime-order $q$-type assumption, including $q$-SDH, on a true fixed-size
assumption.  In one generic group their threshold is $n<q-1$, where $n$ is the
number of challenge group elements; with one bilinear map it is
$\binom{n+2}{2}<q$.  Their conclusion is conditional in exactly the right way:
if such a reduction exists, then the proposed fixed-size assumption has a
generic attack.  [Lu–Zhandry 2024, Theorems 5.2 and 5.10, Corollary 6.1]

[CITED] This does not exclude a representation-dependent reduction, a reduction
that uses the code of the $q$-SDH adversary, or an otherwise non-fully-black-box
standard-model reduction.  [Lu–Zhandry 2024, §§1.3–1.4]

[PROVED] A003 sharpens the first boundary: a single fully-black-box
standard-oracle machine whose guarantee holds pointwise for every group
representation is already a GR-BB reduction and is therefore ruled out.  The
case not reached by A003 is a guarantee over a representation class that omits
the possibly inefficient random sparse implementations--most notably one
concrete family, or only efficient/standardized families--not merely a machine
that is allowed to inspect encoding bits.

[PROVED] A006 now resolves part of that fixed-representation case: if native
code introduces at most $s$ unexplained source labels, the same root-list
simulation works in dimension $n+s+1$ and rules out the reduction when
$n+s<q-1$.  The unresolved representation-dependent branch must supply enough
native-label rank to cross this threshold.

## 1. Uniform typed notation

[CITED] Let $r$ be prime, let
$e:\mathbb G_1\times\mathbb G_2\to\mathbb G_T$ be a non-degenerate bilinear
map, and fix generators $g_1,g_2$.  Write
$[z]_1=g_1^z$, $[z]_2=g_2^z$, and
$[z]_T=e(g_1,g_2)^z$ for $z\in\mathbb Z_r$.  [Boneh–Boyen 2008, §2]

[PROVED] For $I\subseteq\mathbb Z_{\ge 0}$, define the typed power ladder
$P_i(x;I)=([x^j]_i)_{j\in I}$; in particular $[x^0]_i=[1]_i$ is the named
base.

[PROVED] “Search” below means output the named value, while “decision” means
distinguish the named value from an independent uniform element in the same
typed group; the two tasks are not silently interchanged.

### Inversion and strong-DH family

| Repository name | Exact instance and target |
|---|---|
| [CITED] $q$-SDH (source core) | Input $P_1(x;\{0,\ldots,q\})$; output any $(c,[1/(x+c)]_1)$ with $c\in\mathbb Z_r$ and $x+c\ne0$.  [Boneh–Boyen 2008, §3.1; Lu–Zhandry 2024, Cor. 6.1] |
| [CITED] $q$-SDH (typed Boneh–Boyen instance) | The source core plus $[1]_2,[x]_2$; the extra $\mathbb G_2$ terms permit public verification but do not alter the search relation.  [Boneh–Boyen 2008, §3.1] |
| [CITED] $q$-DHI | Input $P_1(x;\{0,\ldots,q\})$; output $[1/x]_1$.  This is the prescribed choice $c=0$ of the $q$-SDH relation.  [Boneh–Boyen 2008, §3.3] |
| [PROVED] $q$-DDHI | Input $P_1(x;\{0,\ldots,q\})$ and $T\in\mathbb G_1$; decide whether $T=[1/x]_1$ or $T\leftarrow\mathbb G_1$. |
| [CITED] $q$-BDHI | In the original symmetric definition, input $(g,g^x,\ldots,g^{x^q})$ and output $e(g,g)^{1/x}$.  Its typed lift inputs $P_1(x;\{0,\ldots,q\})$ and $[1]_2$ and outputs $[1/x]_T$.  [Boneh–Boyen 2004, §3.2; Boneh–Boyen–Goh 2005, §2.3] |
| [PROVED] $q$-DBDHI | The decision version of the preceding typed target: distinguish $T=[1/x]_T$ from uniform $T\leftarrow\mathbb G_T$. |
| [CITED] $q$-wBDHI | Input independent generators $g_1,h_2$ and $P_1(x;\{1,\ldots,q\})$; output $e(g_1,h_2)^{1/x}$.  [Boneh–Boyen–Goh 2005, eq. (2)] |
| [CITED] $q$-wBDHI$^*$ | The same input as $q$-wBDHI; output $e(g_1,h_2)^{x^{q+1}}$.  [Boneh–Boyen–Goh 2005, eq. (3)] |

### Exponent and gap family

| Repository name | Exact instance and target |
|---|---|
| [CITED] $q$-DHE | Input $P_1(x;\{0,\ldots,q\})$; output $[x^{q+1}]_1$.  [Lu–Zhandry 2024, §1] |
| [CITED] $q$-DDHE | Input $P_1(x;\{0,\ldots,q\})$ and $T\in\mathbb G_1$; decide whether $T=[x^{q+1}]_1$ or uniform.  This is also called $q$-strong DDH in some sources.  [Lu–Zhandry 2024, §1] |
| [CITED] $q$-BDHE (gap form) | Input independent $g_1,h_2$ and $[x^j]_1$ for $j\in\{0,\ldots,q-1,q+1,\ldots,2q\}$; output $e(g_1,h_2)^{x^q}$.  [Boneh–Boyen–Goh 2005; Cheon 2006, §2] |
| [PROVED] $q$-DBDHE | The decision version of the preceding gap target in $\mathbb G_T$. |
| [CITED] $q$-aBDH | Input $P_1(x;\{0,\ldots,q\})$, $[1]_2,[x]_2$, an independent $h_2$, and $h_2^{x^{q+2}}$; output $e(g_1,h_2)^{x^{q+1}}$.  [Boneh–Boyen 2008, §3.3] |

[CITED] The names DHE, strong DH, BDHE, and their index shifts are not
canonical across the literature; every edge below therefore refers to the
displayed tuple rather than to a bare acronym.  [Cheon 2006, §2; Lu–Zhandry
2024, §6]

## 2. Implication graph and loss convention

[PROVED] An arrow $A\longrightarrow B$ means “hardness of $A$ implies hardness
of $B$”; operationally, a breaker for $B$ is transformed into a breaker for
$A$.  Here $H(\cdot)$ denotes the corresponding hardness statement.

```text
                                      one pairing
 H(q-BDHI) ─────────────────────────────────────────▶ H(q-DHI)
     │
     │ one call, tight
     ▼
 H(q-wBDHI*) ◀════════ one call, tight ════════▶ H(q-wBDHI)
     │
     │ one DHE-breaker call, then pair with h₂
     ▼
 H(q-DHE) ───────── reverse ladder, one tight call ──▶ H(q-DHI)
     ▲
     │ one q-DHE-breaker call, then pair with h₂
 H((q+1)-BDHE)

 H(q-aBDH) ───── one call, tight, O(q) work ───────▶ H(q-SDH)
                                                               │
                                                               │ c := 0
                                                               ▼
                                                          H(q-DHI)

 H(q-DDHI) ───────── pair challenge with [1]₂ ───────────▶ H(q-DBDHI)

 For k ≤ q and X ∈ {SDH,DHI,DDHI,BDHI,DBDHI,wBDHI}:
 H(q-X) ───────────── discard powers k+1,...,q ──────────▶ H(k-X)
```

### Audited edge table

| Edge | Breaker transformation | Success / time loss | Audit |
|---|---|---|---|
| [CITED] $H(q\text{-aBDH})\to H(q\text{-SDH})$ | Run the $q$-SDH breaker to obtain $(c,[1/(x+c)]_1)$.  Divide $X^{q+2}-(-c)^{q+2}$ by $X+c$ to get $X^{q+1}+w(X)$ with $\deg w\le q$; pairing and the supplied $h_2^{x^{q+2}}$ isolate the wanted $x^{q+1}$ term. | One oracle call; success $\varepsilon$ is preserved; $O(q)$ source operations plus a constant number of pairings. | Actual reduction read: Boneh–Boyen 2008, §3.3. |
| [PROVED] $H(q\text{-SDH})\to H(q\text{-DHI})$ | Feed the same ladder to the DHI breaker and return its output as the SDH answer with $c=0$. | One call; success $\varepsilon$; $O(1)$ overhead. | Direct from the two displayed relations; Boneh–Boyen 2008, §3.3, calls DHI weaker. |
| [PROVED] $H(q\text{-BDHI})\to H(q\text{-DHI})$ | Pair the DHI output $[1/x]_1$ with $[1]_2$. | One call; success $\varepsilon$; one pairing. | Direct typed calculation from Boneh–Boyen 2004, §3.2, and Boneh–Boyen 2008, §3.3. |
| [CITED] $H(q\text{-BDHI})\to H(q\text{-wBDHI}^*)$ | From $(w,w^\beta,\ldots,w^{\beta^q})$, give the wBDHI$^*$ breaker base $w^{\beta^q}$, reversed ladder, and $h=w^s$; raise its answer to $1/s$. | One call; success $\varepsilon$; $O(q)$ tuple work and one target exponentiation. | Actual reduction read: Boneh–Boyen–Goh 2005, §2.3. |
| [CITED] $H(q\text{-wBDHI}^*)\leftrightarrow H(q\text{-wBDHI})$ | Reverse the ladder with new base $g_1^{x^q}$ and hidden exponent $1/x$; the two targets transform into one another. | One call each way; success $\varepsilon$; $O(q)$ tuple work. | Actual reduction read: Boneh–Boyen–Goh 2005, eqs. (2)–(3). |
| [PROVED] $H(q\text{-wBDHI}^*)\to H(q\text{-DHE})$ | Run the DHE breaker on $(g_1,g_1^x,\ldots,g_1^{x^q})$ and pair its output $g_1^{x^{q+1}}$ with $h_2$. | One call; success $\varepsilon$; one pairing. | Direct from Boneh–Boyen–Goh 2005, eq. (3), and the DHE tuple; consistent with Cheon 2006, §2. |
| [PROVED] $H(q\text{-DHE})\to H(q\text{-DHI})$ | To use a DHI breaker, set the new base to $g_1^{x^q}$, the hidden exponent to $1/x$, and reverse the supplied ladder; its output is $g_1^{x^{q+1}}$. | One call; success $\varepsilon$; $O(q)$ tuple reversal. | Direct reduction; Cheon 2006, §2, records the same problem-ordering edge under its exponent-form “strong DH” name. |
| [PROVED] $H((q+1)\text{-BDHE})\to H(q\text{-DHE})$ | On the $(q+1)$-BDHE gap tuple, run the $q$-DHE breaker on the available prefix through $x^q$ and pair $g_1^{x^{q+1}}$ with $h_2$; ignore the higher supplied powers. | One call; success $\varepsilon$; one pairing. | Direct index-checked reduction; Cheon 2006, §2, records the same shifted edge. |
| [PROVED] $H(q\text{-DDHI})\to H(q\text{-DBDHI})$ | Pair every source challenge $T$ with $[1]_2$ and invoke the DBDHI distinguisher. | One call; identical distinguishing advantage; one pairing. | Direct typed calculation from the decisional BDHI experiment in Boneh–Boyen 2004, §3.2. |
| [PROVED] $H(q\text{-}X)\to H(k\text{-}X)$ for $k\le q$ and $X\in\{\mathrm{SDH,DHI,DDHI,BDHI,DBDHI,wBDHI}\}$ | Delete the unused suffix of the power ladder before calling the $k$-breaker. | One call; success/advantage preserved; no group operations and at most $O(q)$ tuple handling. | Direct projection; Boneh–Boyen 2008, §4.3, explicitly uses it for SDH.  It does not apply when the target exponent itself depends on $q$, as in DHE, wBDHI$^*$, or gap-BDHE. |

[PROVED] The last edge formalizes why the assumptions become stronger as $q$
grows: hardness at the larger parameter implies hardness at the smaller one,
while the converse is not supplied by tuple truncation.

[CITED] Boneh and Boyen also prove that $q$-SDH is random self-reducible by
rescaling the hidden exponent and bases; their transformation uses one solver
call, preserves success probability, and costs $O(q)$ exponentiations.
[Boneh–Boyen 2008, §3.3]

## 3. Static prime-order candidates

| Assumption | Fixed-size typed experiment | What it supplies—and what it does not |
|---|---|---|
| [CITED] DDH in $\mathbb G_i$ | Distinguish $([1]_i,[a]_i,[b]_i,[ab]_i)$ from $([1]_i,[a]_i,[b]_i,[z]_i$. | A decisional degree-two correlation in one source group; no source-group power ladder.  [Lu–Zhandry 2024, §1] |
| [CITED] XDH / SXDH | XDH assumes DDH in the designated source group not made easy by the pairing; SXDH assumes DDH in both $\mathbb G_1$ and $\mathbb G_2$. | Constant-size decisional assumptions for asymmetric pairings; they do not provide a map from $\mathbb G_T$ back to either source group.  [Yuen et al. 2024, §2; Galbraith–Paterson–Smart 2008] |
| [CITED] DLIN in $\mathbb G_i$ | For independent generators $u,v,h$, distinguish $(u,v,h,u^a,v^b,h^{a+b})$ from the same tuple with a random final element. | A constant-size linear-relation challenge; it still exposes only a fixed-dimensional source exponent span.  [Boneh–Boyen–Shacham 2004, §3.2] |
| [CITED] co-CDH | Given $([1]_1,[a]_1,[1]_2)$, output $[a]_2$; this is the standard co-CDH experiment with the two source roles swapped. | A constant-size cross-source search problem; pairing reveals $[a]_T$ but not $[a]_2$ in the typed black-box interface.  [Boneh–Gentry–Lynn–Shacham 2003, §2; Galbraith–Paterson–Smart 2008] |
| [CITED] DBDH | Given $([1]_1,[a]_1,[b]_1,[1]_2,[c]_2,T)$, distinguish $T=[abc]_T$ from uniform $T\leftarrow\mathbb G_T$. | A constant-size target-group decision problem; it does not manufacture $[x^j]_1$ for unboundedly many $j$.  [Boneh–Boyen 2004, §3.1] |

[CITED] For every true fixed-size prime-order candidate in this table, the
Lu–Zhandry theorem rules out the fully black-box generic reduction to $q$-SDH
once $q$ exceeds the appropriate dimension threshold; the theorem is not a
claim that DDH, SXDH, DLIN, co-CDH, or DBDH is false.  [Lu–Zhandry 2024,
Theorems 5.2 and 5.10]

## 4. Direct $q$-SDH-to-SXDH attempt: exact break point

[PROVED] Consider a straight-line, type-preserving algebraic reduction given a
source DDH challenge with formal exponents $1,a,b,z$.  Every $\mathbb G_1$
element it can create before calling its $q$-SDH adversary has exponent in
$L=\operatorname{span}_{\mathbb Z_r}\{1,a,b,z\}$, even after multiplying by
fresh known scalars and combining group elements.

[PROVED] In the random DDH branch, treat $a,b,z$ as algebraically independent.
If $x=A+Ba+Cb+Dz\in L$ and $x^2\in L$, comparison of the coefficients of
$a^2,b^2,z^2,ab,az,bz$ over an odd prime field forces $B=C=D=0$; hence $x$ is a
known constant.

[PROVED] Therefore even the prefix $([1]_1,[x]_1,[x^2]_1)$ of a nontrivial
$q$-SDH instance cannot be perfectly embedded from a DDH/SXDH source challenge
by this reduction class.  Pairing challenge elements creates quadratic
exponents only in $\mathbb G_T$, and the typed interface has no operation
$\mathbb G_T\to\mathbb G_1$.

[PROVED] This polynomial-span proof by itself does not cover rewinding, adaptive
multiple calls, or representation-dependent/non-algebraic reductions; it is
the local failure of A001, not an unrestricted black-box separation.

## 5. The scoped meta-reduction

[CITED] Coron introduced a meta-reduction technique for proving optimality
limits on reductions for PSS and other signatures; that 2002 result is useful
methodological ancestry but is not a separation for $q$-SDH.  [Coron 2002,
EUROCRYPT, 272–287]

### Reduction class

[CITED] A Lu–Zhandry GR-BB reduction is polynomial time, independent of the
concrete group representation, and fully black-box in a possibly inefficient
adversary: it observes and answers that adversary's generic group-operation
queries but may use only its input/output behavior.  The formulation permits
interactive assumptions and adaptive oracle calls.  [Lu–Zhandry 2024, §3.2]

[CITED] Their fixed-size assumption may be interactive and may contain
non-group auxiliary data, but across the experiment its challenger outputs at
most $n$ group elements.  [Lu–Zhandry 2024, Def. 4.1]

[CITED] Their $q$-type class requires that a transcript expose at least $q$
linearly independent bounded-degree polynomial functions tied to a hidden
$x_0$, and that knowing the correct $x_0$ lets an efficient algorithm break the
assumption with noticeable probability.  [Lu–Zhandry 2024, Def. 4.2]

### Theorem and proof skeleton

[CITED] In a prime-order generic group, if a GR-BB reduction maps such a
$q$-type assumption to a fixed-size assumption of size $n<q-1$, then a generic
polynomial-time algorithm breaks the fixed-size assumption.  [Lu–Zhandry 2024,
Thm. 5.2]

[CITED] In the generic bilinear extension, the same conclusion holds when
$\binom{n+2}{2}<q$.  [Lu–Zhandry 2024, Thm. 5.10]

[CITED] The meta-reduction selects an inefficient perfect $q$-adversary that
brute-forces the hidden exponents.  It traces every reduction-created source
element as a known linear combination of the $n$ fixed challenge elements, so
the exponent vectors submitted to the adversary lie in a subspace of dimension
at most $n+1$.  A Vandermonde/rank argument and finite-field root finding leave
only polynomially many candidate values for $x_0$; generic equality tests
identify valid candidates, allowing an efficient simulation of the otherwise
inefficient adversary.  The simulated reduction therefore becomes a generic
attack on the fixed-size assumption.  [Lu–Zhandry 2024, Thm. 5.2 proof]

[CITED] With a pairing, recorded exponents may be quadratic in the $n$ input
exponents; linearizing in all degree-at-most-two monomials gives dimension
$\binom{n+2}{2}$ and the bilinear threshold above.  [Lu–Zhandry 2024, §5.2 and
App. A]

[CITED] $q$-SDH meets the $q$-type definition because its ladder supplies the
required independent polynomials and knowledge of $x$ yields a valid answer by
selecting any $c\ne-x$ after a consistency check.  Thus Corollary 6.1 explicitly
states that no generic reduction from $q$-SDH to a fixed-size assumption exists.
[Lu–Zhandry 2024, Claim 6.2 and Cor. 6.1]

[CITED] The prime-order proof step fails in unknown-composite-order groups
because finding the required polynomial roots can be as hard as factoring;
independently rerandomizable hidden subgroups also provide the “shadow”
dimensions used by positive Déjà Q reductions.  [Lu–Zhandry 2024, §1.2]

### Exact scope

[CITED] The theorem rules out fully black-box generic-representation and
type-safe reductions, and its tracing argument also covers algebraic reductions
whose outputs include algebraic explanations.  [Lu–Zhandry 2024, §§1.3–1.4]

[CITED] The theorem does not rule out every black-box reduction in every possible
formalization: in particular it leaves representation-specific standard-model
reductions and reductions non-black-box in the $q$-adversary outside its stated
class.  [Lu–Zhandry 2024, §§1.3–1.4]

[CITED] The paper also does not completely classify exotic groups built from a
base group when the derived group law depends on auxiliary bit strings,
equality branches, or concrete encodings; its positive structural argument in
that direction covers natural affine/algebraic constructions.  [Lu–Zhandry
2024, §3.5]

## 6. Positive results and scheme taxonomy

| Setting | What the result establishes | Static-assumption consequence |
|---|---|---|
| [CITED] Composite-order pairings (Déjà Q, 2014) | Computational $q$-SDH and broad polynomial $q$-type classes are based generically on constant-size subgroup hiding/parameter hiding.  The $q$-SDH proof uses $q+2$ shadow copies and has $\Theta(q)$ hybrid loss up to negligible statistical terms.  [Chase–Meiklejohn 2014, Thm. 4.8 and Ex. 4.10] | The construction is not in prime-order groups; the original framework is asymmetric and computational-source only. |
| [CITED] Composite-order pairings (Déjà Q follow-up, 2016) | The framework covers broader classes, both symmetric and asymmetric composite-order groups, and achieves logarithmic rather than linear tightness loss.  [Chase–Maller–Meiklejohn 2016, abstract and main theorems] | It does not cross the prime-order barrier. |
| [CITED] Original Boneh–Boyen signature | Its standard-model proof uses $q$-SDH with $q$ tied to the signing-query bound; the main reduction loses approximately a factor two in advantage.  [Boneh–Boyen 2008, Thm. 8] | This is not a reduction of $q$-SDH to a static assumption. |
| [CITED] Dual-form exponent-inversion signatures and IBE variants | Modified Boneh–Boyen-like signatures and Gentry-IBE variants have prime-order proofs under SXDH.  [Yuen–Chow–Wu–Zhang–Yiu 2024] | These are altered dual-form schemes, not a reduction for the original $q$-SDH assumption or an unchanged original scheme. |
| [CITED] BBS+ and deterministic BBS concrete security (2025) | After $q$ signatures, attacks recover the secret with the complexity of $\Theta(q)$-DL; the authors also reduce $\Theta(q)$-SDH to the security of those schemes. [Chairattana-Apirom--Tessaro 2025, abstract] | This is a reverse, scheme-to-$q$-SDH comparison and reinforces usage-dependent security; it is not a static basis. |
| [CITED] BBS tightness (EUROCRYPT 2026) | BBS has a tight $q$-SDH proof when each message is signed at most once; with repeated messages, no algebraic reduction to the considered $q$-SDH variants can be tight. [Chairattana-Apirom--Hofheinz--Tessaro 2026, abstract] | The result tightens a $q$-type proof and a scheme-specific lower bound; it neither reduces $q$-SDH to a static assumption nor removes $q$. |

## 7. Quantitative obstruction: Cheon's attack

[CITED] If a divisor $d\le q$ of $r-1$ is available in a prime-order group,
the ladder contains $g^x$ and $g^{x^d}$, and Cheon's algorithm recovers $x$ in
$O(\log r(\sqrt{(r-1)/d}+\sqrt d))$ group operations.  [Cheon 2006, Thm. 1]

[CITED] If $d\mid r+1$ and the ladder reaches degree $2d$, Cheon's second
algorithm recovers $x$ in
$O(\log r(\sqrt{(r+1)/d}+d))$ group operations.  [Cheon 2006, Thm. 2]

[PROVED] Recovering $x$ immediately solves $q$-SDH by choosing any
$c\ne -x$ and computing $[1/(x+c)]_1$.

[CITED] These attacks can reduce the generic square-root security by roughly a
factor $\sqrt d$ for favorable divisors, so concrete group sizes must account
for both $q$ and the factorization of $r\pm1$.  [Cheon 2006, abstract and §5]

## 8. Structural conclusion

[PROVED] The common obstruction is dimensional: $q$-SDH requires an
unbounded family of correlated source encodings, while a fixed-size
prime-order challenge supplies a fixed-dimensional algebraic span; bilinearity
raises the available degree but still leaves a fixed $O(n^2)$ monomial space.

[CITED] Composite-order hidden subgroups evade this simulation argument through
unknown-factor root finding and independent hidden-subgroup randomization,
whereas prime-order generic representations do not.  [Chase–Meiklejohn 2014;
Lu–Zhandry 2024, §1.2]

> [PROVED] **Gap.** The remaining class permits representation-native label
> rank large enough to reach the $q$-SDH ladder dimension, or non-black-box
> access to the adversary's code.  Resolving either branch requires a reduction
> or a meta-reduction with a new invariant.  Blocking: no.  Logged as Q003.

## 9. Representation-uniform boundary corollary

[PROVED] Define a **UR-FBB reduction** from a single-stage group game $Q$ to a
single-stage group game $F$ to be one PPT oracle machine $R$ that may run
arbitrary bit computations on group encodings and may rewind or multiply invoke
its $Q$-adversary, but accesses the group itself only by labeling,
group-operation, equality, and optional pairing interfaces.

[PROVED] Require pointwise representation uniformity: for every implementation
$G$ of the prime-order group, including possibly inefficient implementations,
and every possibly inefficient $A$ breaking $Q^G$, the same $R^{A,G}$ breaks
$F^G$ with a common non-negligible lower bound whenever $A$ has a common
non-negligible lower bound; both bounds and $R$ are independent of $G$.

[CITED] Lu--Zhandry's GR syntax also permits arbitrary bit computation on the
actual labels; its representation-independence is imposed by taking advantage
over every possibly inefficient group implementation.  [Lu--Zhandry 2024,
§3.2]

[PROVED] **Boundary theorem.** Every UR-FBB reduction is a GR-BB reduction.
Indeed, a GR adversary with non-negligible infimum advantage breaks $Q^G$ for
every $G$; the UR-FBB guarantee gives the same reduction non-negligible
advantage against $F^G$ for every $G$, and therefore against the GR game under
the same infimum.  The machine already has GR syntax by definition.  In
particular, if the input infimum is at least $\epsilon$, uniformity supplies a
$\delta$ such that
$\inf_G\operatorname{Adv}_{F^G}(R^{A,G})\ge\delta$.

[CITED] For single-stage games, Lemma 3.2 gives the equivalent type-safe
statement.  Its proof composes representation wrappers while preserving the
reduction's interception of the adversary's messages and group queries.
[Lu--Zhandry 2024, Lem. 3.2]

[CITED] Lemma 3.1 supplies the random sparse-label mechanism behind the model
equivalence: for $\ell>\log_2 r+\omega(\log\lambda)$, the simulation fails only
if a polynomially bounded computation guesses a valid label that has never been
returned by its labeling or group-operation interfaces, an event of negligible
probability.  [Lu--Zhandry 2024, Lem. 3.1]

[CITED] Consequently, no UR-FBB reduction bases prime-order $q$-SDH on a true
fixed-size assumption of size $n$ when $n<q-1$; with a generic bilinear map the
same conclusion holds when $\binom{n+2}{2}<q$.  [Lu--Zhandry 2024, Thms. 5.2,
5.10, Claim 6.2, Cor. 6.1]

[PROVED] This theorem rules out a strictly phrased standard-oracle class but is
not a new unrestricted separation: its universal representation quantifier is
exactly what makes the GR-BB theorem applicable.

[PROVED] “Universal” cannot be weakened here to “every efficient or
standardized implementation” without another argument.  The sparse injection
used in the information-theoretic wrapper may be an inefficient group
implementation, and full black-box security quantifies over possibly
inefficient breaking adversaries.

## 10. Why random relabeling does not settle a fixed representation

[PROVED] A reduction guaranteed only for one family $G_*$ has quantifier form
$$
  \exists G_*\,\exists R_*\,\forall A_*:\quad
  \operatorname{Break}_{Q^{G_*}}(A_*)
  \Longrightarrow
  \operatorname{Break}_{F^{G_*}}(R_*^{A_*}).
$$
The random-representation simulation needs the implication for a newly sampled
$G_L$, which is not entailed by this premise.

[PROVED] The missing implication cannot be repaired by abstract group
isomorphism alone.  A machine may check the canonical generator encoding or a
public representation identifier, behave like $R_*$ on $G_*$, and abort on all
other encodings without changing its promised behavior.

[PROVED] Concrete encodings also break the fixed-dimensional trace invariant at
the syntax level: native validation, decompression, or hash-to-curve code may
produce a valid point without an observed group-operation query, so the
meta-reduction receives no algebraic explanation of that point in the span of
the fixed-size challenge.

[CITED] Lu--Zhandry explicitly leave open derived constructions whose group law
uses auxiliary strings, equality branches, or the concrete representation;
their structural argument reduces natural affine algebraic constructions to a
product group but does not classify all bit-dependent constructions.
[Lu--Zhandry 2024, §3.5]

[HEURISTIC] Such native operations do not visibly generate the correlated
$q$-SDH power ladder, so failure of the trace proof is not positive evidence for
a reduction.

## 11. Final scope classification

| Reduction class | Result |
|---|---|
| [CITED] TS-BB / GR-BB, fully black-box in possibly inefficient adversaries | Ruled out at the published single-group and bilinear dimension thresholds. [Lu--Zhandry 2024, Lem. 3.2, Thms. 5.2 and 5.10] |
| [CITED] Algebraic reduction with explanations | The same tracing separation applies. [Lu--Zhandry 2024, §1.4] |
| [PROVED] UR-FBB standard-oracle reduction, universal over representations | Implies GR-BB by A003, hence is ruled out at the same thresholds. |
| [PROVED] One fixed concrete representation with at most $s_1$ unexplained labels in the $q$-SDH source | A006 gives a direct trace separation at $n_1+s_1<q-1$, without random relabeling. |
| [PROVED] A representation class not closed under random sparse relabeling, with native-label rank large enough to cross A006's threshold | A004 blocks relabeling and A006 no longer applies; existence or impossibility remains open. |
| [CITED] Non-black-box use of the adversary's code | Outside the fully-black-box taxonomy and outside the Lu--Zhandry theorem. [Reingold--Trevisan--Vadhan 2004, §1; Lu--Zhandry 2024, §§1.1, 2] |

[PROVED] Thus the strongest justified deliverable is a scoped impossibility,
not a reduction and not an all-black-box impossibility.  After A006, the
structural residual is narrower: enough representation-native labels to make
the trace dimension reach $q$, or access to the adversary's code.

## 12. Efficient-encoding substitution fails

[PROVED] Let an efficient sparse encoding family use an $m(\lambda)$-bit seed,
with $m$ polynomial, to choose injections from an $r$-element group into an
$N$-element label space.  Its support contains at most $2^m$ tables, while a
uniform random injection has $(N)_r$ possible tables.

[PROVED] A possibly inefficient adversary queries all $r$ exponents, enumerates
all seeds, and distinguishes the two distributions with advantage at least
$1-2^m/(N)_r$, which is overwhelming because
$\log (N)_r\ge\log(r!)=\Omega(r\log r)$ and $r$ is exponential in $\lambda$.

[PROVED] Therefore neither finite-wise independence nor a computational PRP
replaces the random injection for the fully-black-box adversary class.  The
former fails beyond its query bound; the latter protects only against
computationally bounded distinguishers.

[CITED] This boundary accords with Zhandry's generic-query convention, where
bit computation can be unbounded, and with the later sparse-GGM separations for
admissibly encoded, dense, elliptic-curve, and bilinear settings.  [Zhandry
2022, §3.3 and Thm. 4.10; Wang et al. 2025, abstract]

[PROVED] A second, independent obstruction remains: breaking a static
assumption in an artificial efficient encoding does not contradict hardness
asserted only for the named representation used by the scheme.

## 13. A fixed-representation separation with bounded native freshness

[PROVED] A006 recovers a representation-specific trace without relabeling the
group.  It permits arbitrary inspection of concrete encodings and arbitrary
native validation, decompression, hashing, and table code, but charges one
**freshness unit** whenever a distinct valid source label is first used without
being a challenger output, the public generator, known-scalar labeling, or the
result of a recorded group operation.

[PROVED] For an assumption challenge with at most $n$ source elements and a
reduction with at most $s$ such fresh labels, assign formal coordinates to the
$n$ challenge elements, the $s$ fresh labels, and the generator.  Every label
sent to the $q$-SDH adversary then has a known coefficient vector in dimension
at most $n+s+1$, even if the concrete encodings satisfy hidden algebraic
relations.

[PROVED] Actual-label collisions do not require solving those relations: keep
the first coefficient vector for a repeated label.  Both the retained vector
and the newly derived vector evaluate to the same actual discrete logarithm,
so the required evaluation invariant remains true.

[PROVED] Lu--Zhandry's low-dimensional root-list simulator therefore applies
with $n+s$ replacing $n$.  It yields a PPT attack on the fixed assumption when
$n+s<q-1$, with no additional success loss beyond the purported reduction.

[PROVED] For typed $q$-SDH in a source group, pairings do not enlarge the
source trace: the sharper threshold is $n_1+s_1<q-1$ unless an unrecorded
target-to-source conversion is available, in which case each output is fresh.
For a broader bilinear $q$-type game with target polynomials, a safe overcounted
trace dimension is $\binom{n+s+2}{2}+t$.

[PROVED] This closes a genuine part of the representation-dependent gap: a
reduction compatible with hardness of the fixed assumption must create at
least $q-1-n_1$ unexplained labels in the $q$-SDH source group in some
execution, use an unrecorded conversion into that source, or leave the fully-
black-box class.  Linear-in-$q$ native freshness and non-black-box access to the
adversary remain outside the result.

[CITED] The root-list and quadratic-lift ingredients are those of the original
generic separation.  [Lu--Zhandry 2024, Lem. 5.1 and Thms. 5.2, 5.10]

## 14. Structured-label density is not a freshness bound

[CITED] The structured generic-group model gives algorithms free access to a
partial label operation $\star$ and charges only generic group-oracle queries.
For a prime-order-$r$ group and constrained-label fraction $\delta$, its hard
labeling distribution bounds $T$-query discrete-log advantage by
$\delta(3T+2)+(3T+1)^2/r+1/r$.  [Corrigan-Gibbs--Henzinger--Wu 2026,
Defs. 2.2--3.1 and Thm. 3.2]

[PROVED] A007 shows that this theorem does not automatically strengthen A006.
The $\delta T$ term bounds a random-hybrid event, whereas freshness counts
distinct labels selected along an actual reduction execution.  A publicly
recognizable structured subset may be negligibly dense yet contain at least
$q$ labels that the reduction deliberately addresses.

[PROVED] The theorem's query parameter $T$ also cannot substitute for
freshness because $\star$ evaluations and other label computation are free in
that model.  Moreover, its hard labeling is an existential distribution, so a
reduction promised only for one named labeling need not work under that
distribution.

[PROVED] The valid conditional transfer is explicit: if at most $u$ distinct
valid labels enter through raw code and free structure, then set $s=u$ in A006.
Density alone supplies no such $u$; a future extension must bound native-label
rank or exploit the relations supplied by $\star$ directly.
