# Non-vacuous corrected variants of P1.2

The supplied statement has two independent specification issues: standard
$L_p(1/2)$ is too small for constant-length support, while an online-only time
bound permits input-specific lookup tables. The variants below separate those
issues.

## Resource convention

**Proposed resource convention.** A uniform constructor `Build(p,E)` should output descriptions of
the factor-base predicate and decoder. Its running time, output length,
input-specific advice, preprocessing time, and persistent storage should all
be bounded explicitly. `Member` and `Decompose` should be fixed uniform
algorithms operating on those descriptions; preprocessing must finish before
the independent target is drawn.

[PROVED] Bounding only online operations does not enforce this convention:
A008 uses a description with one decomposition per group element and answers
online by table lookup.

## Variant S — square-root size and fixed length

**Proposed Variant S.** Replace condition (1) by
$|\mathcal F|\le p^{1/2+o(1)}$, fix $m=3$, and impose all of the following:

1. `Build`, its output description, all input-specific advice, preprocessing,
   and persistent storage use $p^{o(1)}$ time or bits/words as appropriate.
2. Membership is decided by a fixed uniform algorithm in
   $\operatorname{poly}(\log p)$ time from the description.
3. After preprocessing and on an independent uniform target, a fixed uniform
   decoder runs in $\operatorname{poly}(\log p)$ time and succeeds with
   inverse-polylogarithmic probability.

[PROVED] The support count does not rule out Variant S because
$|\mathcal F|^3/p$ can be large. [PROVED] A008 is excluded because its
preprocessing and storage are $p^{1+o(1)}$, and an explicit listing of a
square-root-size factor base is also excluded; the predicate must be succinct.

[CONJECTURE] Candidate A has no uniform coordinate-aware polylogarithmic
decomposition algorithm under Variant S. A009 proves this only for
translate-probe search; P1.2/Q004 is the remaining finder question. An
explicit succinct coordinate-aware construction with a total resource proof
would refute the conjecture.

[CITED] Petit–Kosters–Messeng 2016 supply a concrete coordinate-aware
smooth-subgroup predicate but leave its polynomial-system solving complexity
open. [EMPIRICAL: $p=17,257,65537$] A010's tested Gröbner implementation
completed only at $p=17$ within five seconds; this is a solver observation,
not a lower bound. Thus low-degree membership alone does not discharge the
decoder requirement.

## Variant L — standard L-size and growing length

**Proposed Variant L.** Retain
$|\mathcal F|\le L_p[1/2,c]$, but permit
$$
m(p)=\Theta\!\left(\sqrt{\frac{\log p}{\log\log p}}\right),
$$
and bound construction, description/advice, preprocessing, and storage by
$L_p[1/2,C]$ for a fixed $C$. Keep membership and online decomposition
polynomial in $\log p$, including the cost of writing all $m(p)$ outputs.

[PROVED] `CLAIM.md` shows that the stated order of growth for $m$ is necessary
up to its constant. [PROVED] A008's full target table is again excluded because
$p^{1+o(1)}$ is larger than every fixed-constant $L_p[1/2,C]$.

[CONJECTURE] Variant L is closer to a genuine subexponential index-calculus
target, but no construction satisfying it is supplied here.

## Required wording choice

**Required wording choice.** A future problem statement should select Variant S or Variant L
explicitly. Mixing the standard-L size bound, constant $m$, square-root
baseline, and uncharged online lookup produces incompatible or vacuous
requirements rather than a single asymptotic research target.
