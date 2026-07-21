---
attempt: A006
status: completed
---
# A006 - Affine factors and selected subgroups

## Idea

[CONJECTURE] Structure theory should eliminate the full rational-point group
of every bounded-dimensional connected commutative algebraic group with a
nonzero affine part.  A counting argument should also eliminate every
polylog-smooth selected subgroup of a one-dimensional torus whenever the
encoder has public coins and a correct decoder.

## Prediction and decision rule

[CONJECTURE] For full groups, Chevalley decomposition will leave only abelian
varieties.  For selected subgroups, correctness alone will force a subgroup
of size at least the desired success probability times the input-space size.
The prediction is refuted if a connected affine commutative group over a
finite field has neither a positive-dimensional split-unipotent part nor a
torus quotient, if rational-point counts fail to multiply across the relevant
exact sequences, or if a correct public-coin encoding can map more inputs
successfully than the size of its target subgroup for a fixed coin value.

## Full connected commutative algebraic groups

[CITED] Let $G/\mathbb F_r$ be a smooth connected commutative algebraic group.
Chevalley's theorem gives a unique exact sequence

$$
  1\longrightarrow L\longrightarrow G\longrightarrow A\longrightarrow 1,
$$

where $L$ is smooth, connected, affine, and commutative, and $A$ is an
abelian variety (Conrad 2002, Theorem 1.1).

[CITED] Because $\mathbb F_r$ is perfect, the unipotent radical $U$ of $L$ is
defined over $\mathbb F_r$, is split, and $T=L/U$ is a torus.  A split
$u$-dimensional unipotent group is isomorphic to $\mathbb A^u$ as a variety,
so

$$
  |U(\mathbb F_r)|=r^u.
$$

[CITED] Lang's theorem says $H^1(\mathbb F_r,H)=1$ for every smooth connected
algebraic group $H/\mathbb F_r$.  Applying it to the kernels in the two exact
sequences makes the maps on rational points surjective and therefore gives

$$
  |L(\mathbb F_r)|=|U(\mathbb F_r)|\,|T(\mathbb F_r)|,
  \qquad
  |G(\mathbb F_r)|=|L(\mathbb F_r)|\,|A(\mathbb F_r)|.
$$

[PROVED] If $u>0$, then the input prime $r$ divides $|G(\mathbb F_r)|$.
Thus the full group is not $(\log r)^C$-smooth for any fixed $C$ and all
sufficiently large $r$.

[PROVED] If $u=0$ and $L$ is nontrivial, then $L=T$ is a positive-dimensional
torus.  For every fixed dimension bound $D$, A005 supplies infinitely many
primes $r$ on which every such $T$ has

$$
  P^+(|T(\mathbb F_r)|)\ge c_Dr^{\eta_D}
$$

for constants $c_D,\eta_D>0$.  Since $|T(\mathbb F_r)|$ divides
$|G(\mathbb F_r)|$, the same obstruction holds for the full group.

[PROVED] Consequently, among full rational-point groups of smooth connected
commutative algebraic groups of globally bounded dimension, every candidate
with a nonzero affine part is obstructed on an infinite prime family.  The
only full connected class not eliminated by this argument is the class of
abelian varieties, including elliptic curves.

## A public-coin counting lemma for selected subgroups

[PROVED] Let $S$ be a finite input set, let $H$ be a finite target group, and
let $e$ be public randomness independent of $x\in S$.  Suppose an encoder
$f_e$ may fail, but whenever it succeeds a decoder $d$ satisfies
$d(e,f_e(x))=x$.  For each fixed $e$, the successful restriction of $f_e$ is
injective: two successful inputs with the same image would make the decoder
return two different values on the same pair $(e,h)$.  Hence

$$
  \sum_{x\in S}\Pr_e[f_e(x)\text{ succeeds}]
  =\mathbb E_e\bigl|\{x:f_e(x)\text{ succeeds}\}\bigr|
  \le |H|.
$$

[PROVED] The average success probability is therefore at most $|H|/|S|$.
In particular, success at least $\delta$ for every input forces
$|H|\ge\delta|S|$.  This conclusion permits arbitrary computation inside the
encoder and decoder; it uses only public coins, correctness, and the finite
target size.

[PROVED] Apply the lemma with $S=\mathbb F_r$ and with $H$ a
$(\log r)^C$-smooth subgroup of a one-dimensional torus.  On the A005 prime
family the full torus order is $O(r)$ and contains a prime
$\ell\ge c r^\eta$.  For large $r$, smoothness forces $\ell\nmid|H|$, so

$$
  |H|\le \frac{|T(\mathbb F_r)|}{\ell}=O(r^{1-\eta}),
  \qquad
  \frac{|H|}{r}=O(r^{-\eta}).
$$

[PROVED] Thus no correct public-coin encoding into a polylog-smooth selected
subgroup of a one-dimensional torus can have inverse-polynomial-in-$\log r$
success on every input along that prime family.  This strictly strengthens
A004's shift-and-test lower bound.

[PROVED] The counting lemma does not by itself eliminate selected subgroups
in dimension at least two: an ambient order of size about $r^d$ can lose a
factor $r^\eta$ and still leave at least $r$ target elements.  It also does
not cover private randomness unavailable to the decoder, many-to-one
encodings with extra recovery information outside $H$, disconnected families
with uncontrolled component complexity, or abelian varieties.

## Outcome

[PROVED] The prediction was confirmed in its stated scope.  Full connected
commutative auxiliary groups reduce rigorously to pure abelian varieties, and
all selected polylog-smooth subgroups of one-dimensional tori are ruled out
in the public-coin recoverable-encoding model.  Higher-dimensional selected
subgroups and abelian varieties remain separate branches.
