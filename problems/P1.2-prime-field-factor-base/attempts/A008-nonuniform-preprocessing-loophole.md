---
attempt: A008
status: promising
---
# A008 — Nonuniform preprocessing loophole in the square-root variant

## Idea

[PROVED] If only the online running time of $\mathcal D$ is bounded, an
input-specific table can hide a complete discrete-logarithm table. A radix
factor base covers every target with constant $m$ and size
$O(mr^{1/m})$, while online decomposition is a table lookup.

## Prior art

[PROVED] This attempt uses only the elementary positional representation of an
integer and cyclicity of a prime-order group. It is not an elliptic-curve index
calculus algorithm and does not rely on the candidate predicates A–D.

## Plan

1. Choose a generator $G$ of the prime-order group and
   $B=\lceil r^{1/m}\rceil$.
2. Let the factor base be the union of
   $\{dB^jG:0\le d<B\}$ for $0\le j<m$.
3. Precompute, for every $0\le k<r$, the base-$B$ digits of $k$ and store the
   corresponding $m$ summands under the key $kG$.
4. Exhaustively validate coverage and returned sums on the recorded 16-bit
   curve, while recording base size, table size, preprocessing work, and
   online lookup work separately.

## Execution log

- [EMPIRICAL: first local launch] The initial unit and driver runs stopped
  before construction because the new code called a nonexistent
  `Curve.is_on_curve` method. The shared API names the predicate
  `Curve.contains`; the call was corrected without changing the construction.
- [EMPIRICAL: p=65519,262139,1048571] After correction, exhaustive walks of
  all 65,537, 261,431, and 1,046,897 group elements found complete coverage,
  zero nonmember summands, and zero invalid sums.
- [EMPIRICAL: same curves, m=3] The radix/base-size pairs were $(41,120)$,
  $(64,190)$, and $(102,304)$, versus square-root diagnostic sizes 255, 511,
  and 1,023.
- [EMPIRICAL: same curves] The decoder tables contained exactly $r$ entries
  and stored $4r$ point references (key plus three output points): 262,148,
  1,045,724, and 4,187,588 references.

## Outcome

[PROVED] Let $G$ generate a cyclic group of order $r$, fix $m\ge1$, and set
$B=\lceil r^{1/m}\rceil$. Define
$$
\mathcal F=\bigcup_{j=0}^{m-1}\{[dB^j]G:0\le d<B\}.
$$
Then $|\mathcal F|\le mB$. Every $0\le k<r$ has $m$ base-$B$ digits because
$B^m\ge r$, so $[k]G$ is a sum of exactly $m$ elements of $\mathcal F$.
Thus the construction matches the full-coverage counting lower bound
$|\mathcal F|\ge r^{1/m}$ within a factor approaching $m$.

[CONDITIONAL: nonuniform indexed tables are allowed and their construction,
description, and storage are not charged] Store the finite factor base in a
balanced search structure and store the decomposition above under every point
$[k]G$. Membership and decomposition then take polynomial time in $\log p$
online, and success is one.

[PROVED] This speed is purchased with $r$ target entries,
$\Theta(rm\log p)$ bits of input-specific description, and
$\Omega(r)$ preprocessing steps. It is exponential in the input length
$\Theta(\log p)$ and embeds a complete discrete-logarithm table. It is not an
efficient ECDLP algorithm.

[PROVED] For $m=3$ and $r=\#E(\mathbb F_p)=p^{1+o(1)}$, the factor-base size
is $O(p^{1/3})=o(p^{1/2})$. Therefore merely replacing the original standard-L
bound by a square-root bound, without adding uniformity and offline-resource
bounds, makes the literal online conditions trivial in a nonuniform model.

## Post-mortem

**Why it is not the intended solution:** [PROVED] All hard work is hidden in
linear-size preprocessing and advice rather than performed by a uniform
polylogarithmic algorithm.

**What transfers:** [PROVED] Any corrected statement must charge construction,
description/advice, preprocessing time, and storage, not only online lookup.

**Would it work under different assumptions?** [CONDITIONAL: preprocessing
and advice are bounded by $p^{o(1)}$] This construction is excluded because its
target table has $p^{1+o(1)}$ entries. The resulting uniform corrected problem
is not resolved by A008.
