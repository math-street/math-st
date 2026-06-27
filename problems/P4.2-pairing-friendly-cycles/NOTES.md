# Notes - P4.2

## Stable facts

### Algebraic cycle conditions (SG-01)

[PROVED] Let \(E_i/\mathbb F_{p_i}\) have trace \(t_i\), with indices modulo
\(m\). The cycle condition is equivalent to
\[
  p_{i+1}=p_i+1-t_i
  \quad\text{or, equivalently,}\quad
  t_i=p_i+1-p_{i+1}.
\]
This is the defining identity
\(\#E_i(\mathbb F_{p_i})=p_i+1-t_i\) followed by substitution of
\(\#E_i(\mathbb F_{p_i})=p_{i+1}\).

[PROVED] Every \(m\)-cycle satisfies
\[
  \sum_{i=1}^{m}t_i=m.
\]
Indeed, summing \(t_i=p_i+1-p_{i+1}\) makes the field-size terms telescope.
For a 2-cycle this specializes to \(t_1+t_2=2\).

[PROVED] In a 2-cycle, writing \(p_1=p\), \(p_2=q=p+1-t\),
\(t_1=t\), and \(t_2=2-t\), the two CM radicands are identical:
\[
  4q-t_2^2=4(p+1-t)-(2-t)^2=4p-t^2.
\]
Consequently, the unique decomposition
\(t_i^2-4p_i=D_K f_i^2\), with \(D_K\) a fundamental quadratic
discriminant, gives the same \(D_K\) and conductor \(f_i\) for both ordinary
isogeny classes.

[PROVED] If every curve has prime order, the exact embedding degree of
\(E_i/\mathbb F_{p_i}\) is the multiplicative order of \(p_i\) modulo
\(p_{i+1}\). Thus a claimed degree \(k_i\) requires
\(p_i^{k_i}\equiv1\pmod {p_{i+1}}\) and
\(p_i^j\not\equiv1\pmod {p_{i+1}}\) for every \(1\leq j<k_i\).

### Published MNT regression target (SG-02)

[CITED] Chiesa, Chua, and Weidner give the MNT6/MNT4 cycle polynomials
\[
\begin{array}{c|ccc}
 & p(x) & n(x) & t(x)\\
\text{MNT6} & 4x^2+1 & 4x^2+2x+1 & 1-2x\\
\text{MNT4} & 4x^2+2x+1 & 4x^2+1 & 2x+1
\end{array}
\]
and an explicit \(x=3\) example (SIAM Journal on Applied Algebra and Geometry
3(2), 2019, Table 4.1 and Example 4.9; `refs/chiesa-chua-weidner2019.md`).

[CITED] The published first two curves of that example are
\(y^2=x^3+24x+16\) over \(\mathbb F_{37}\) and
\(y^2=x^3+36x+5\) over \(\mathbb F_{43}\) (Chiesa--Chua--Weidner 2019,
Example 4.9; `refs/chiesa-chua-weidner2019.md`).

## Working conventions

[PROVED] For a prime-order cycle, the per-curve value used here is
\(\rho_i=\log(p_i)/\log(p_{i+1})\), and the cycle threshold statistic is
\(\rho_{\max}=\max_i\rho_i\). The geometric mean of the per-curve values is
always 1 because their product telescopes, so it is not used as a quality
statistic.

[PROVED] Under this convention, every distinct prime-order 2-cycle with
smaller field prime \(p\geq5\) automatically has \(\rho_{\max}<2\). Hasse's
bound gives \(q\leq p+1+2\sqrt p<p^2\), so
\(\log q/\log p<2\); the reciprocal per-curve value is below 1.

> **Gap.** The supplied question asks whether a cycle can achieve \(\rho<2\),
> but the standard per-curve definition makes this automatic for every
> distinct prime-order 2-cycle with field primes at least 5, and the published
> \(x=3\) MNT cycle has \(\rho_{\max}=1.041618836729\). Resolving the intended
> question requires a different explicit definition, if one was intended.
> Blocking: no for SG-03/SG-04. Logged as Q010.

## Tool substitution

[EMPIRICAL: shared suite on Python 3.13.4, 2026-06-27] SageMath is unavailable,
so SG-02 uses direct equation enumeration and the shared Hasse/BSGS point-count
routine as two independent checks (`env/check_env.py`, `lib/curves.py`).

[EMPIRICAL: initial P4.2 session 1 inventory] The advertised
`lib/tnfs_cost.py` was absent when the searches were designed and run. It
appeared in the shared workspace before the final test pass. No SG-01 through
SG-06 computation imports it, so this timing does not narrow the recorded
search spaces.

## Stable computational results

[EMPIRICAL: distinct primes below 2^16, exact degrees 3 through 12] The primary
2-cycle census has 26 fully verified hits and 219 one-sided near-misses; the
primary directed 3-cycle census has five fully verified hits and 37
two-of-three near-misses (`RESULTS.md`).

[EMPIRICAL: distinct primes below 2^16, exact degrees 3 through 18] The
one-axis relaxation has 36 fully verified 2-cycle hits and 12 fully verified
directed 3-cycle hits (`RESULTS.md`).

[EMPIRICAL: distinct primes below 2^22, exact degrees 3 through 12] The
candidate-complete primary census has 76 verified 2-cycle hits and five
verified directed 3-cycle hits. The only non-{(6,4),(4,6)} 2-cycles have
larger field at most 31; every directed 3-cycle hit has all fields at most 43
(`RESULTS.md`).

[EMPIRICAL: all primary 2-cycle hits below 2^22] Every one of the 76
arithmetic hits has explicit curve equations whose orders agree under BSGS and
direct enumeration. The 29 hits newly appearing between 20 and 22 bits
required at most 43,462 coefficient trials per curve
(`data/construct_hit_cycles_n29_s7207_20260708.csv`).

### MNT classification

[PROVED] If \(p<q\) form a prime-order 2-cycle with exact degree pair (6,4),
then for an integer \(x\ge1\),
\[
  p=4x^2+1,\qquad q=4x^2+2x+1.
\]
If the exact degree pair is (4,6), then
\[
  p=4x^2-2x+1,\qquad q=4x^2+1.
\]
The elementary converse proof is in `MNT_CLASSIFICATION.md`.

[PROVED] No all-prime consecutive MNT triple
\[
 (4x^2-2x+1,\,4x^2+1,\,4x^2+2x+1)
\]
closes in either orientation with every exact embedding degree in 3 through
12. A remainder bound covers \(x\ge1026\), and the deterministic certificate
covers \(1\le x\le1025\) (`MNT_THREE_CHAIN_OBSTRUCTION.md`).

### Session-3 extensions

[EMPIRICAL: distinct primes below \(2^{28}\), exact degrees 3 through 12] The
candidate-complete primary census has 333 2-cycle hits and five directed
3-cycle hits. Exactly five 2-cycle hits are outside {(6,4),(4,6)}, all with
larger field at most 31; every directed hit has fields at most 43
(`RESULTS.md`).

[PROVED] Exact-order cyclotomic residues generate every target-degree Hasse
edge. This retains the complete reportable 2-cycle and 3-cycle candidate
ledgers without scanning all Hasse-near prime pairs
(`CYCLOTOMIC_ROOT_ENUMERATION.md`).

[EMPIRICAL: complete 24-bit ledgers] The root-generated candidate CSVs are
byte-identical to the Hasse-scanned CSVs. At 28 bits the root method processed
14,630,841 primes in 301.0 seconds for 2-cycles and 427.7 seconds for
3-cycles.

[EMPIRICAL: all 61 directed near-misses below \(2^{28}\)] Twenty-six rows are
orientations of the globally excluded consecutive MNT chain. The 35 residual
rows include only two above \(2^{16}\): target-degree pairs (5,11) and (8,9),
with exact closing degrees 483,882 and 12,053,055
(`data/classify_three_cycle_near_misses_n61_20260718.csv`).

[PROVED] If both exact degrees of a prime-order 2-cycle lie in {3,4,6}, its
ordered pair is (6,4) or (4,6), and the cycle is MNT. The remaining seven
ordered pairs are excluded by the bounded 11-row multiplier certificate
(`QUADRATIC_DEGREE_CLASSIFICATION.md`).

[PROVED] A nonidentity point annihilated by a prime \(q\), together with
uniqueness of \(q\) as a multiple in the Hasse interval, independently
certifies the exact curve order. All 108 new 24-bit curve equations carry this
certificate (`PRIME_ORDER_CERTIFICATE.md`).

### Completed low-cyclotomic-degree classification

[PROVED] Mixed exact degrees, one in {3,4,6} and one in {5,8,10,12}, have the
unique cycle \((7,11;10,3)\) (`MIXED_DEGREE_CLASSIFICATION.md`).

[PROVED] Quartic/quartic exact degrees have the unique cycle
\((11,13;12,10)\). The complete proof pipeline is: quotient-difference bound,
small-gap and degenerate audits, 750 genus-one reductions, local and real
sieves, higher-power Hensel lifting, and exact global genus-one computations
(`QUARTIC_DEGREE_REDUCTION.md`).

[EMPIRICAL: exact Magma V2.29-8 computations] Of the 29 final normalized
quartics, 22 have complete small integral-point lists, five have empty fake
two-Selmer sets despite being everywhere locally soluble, and the remaining
symmetric curve has rank zero and torsion \(\mathbb Z/2\). Its only rational
points occur at \(c=-1\), with the reflection at \(c=1\).

[PROVED] The remaining global 2-cycle degree frontier below exact degree 13 is
precisely the pairs involving 7, 9, or 11. The global length-3 question also
remains open outside the consecutive-MNT-chain obstruction.
