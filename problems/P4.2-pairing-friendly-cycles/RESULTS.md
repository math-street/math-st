# Results - P4.2 sessions 1-3

## Outcome in one paragraph

[EMPIRICAL: distinct primes 5 <= p_i < 2^28, exact 3 <= k_i <= 12]
Pairing-friendly prime-order cycles exist at toy scale outside the MNT degree
pattern: five verified 2-cycles have degree pairs other than (6,4) or (4,6),
and five verified directed 3-cycles occur. All remain tiny: the largest field
is 31 for the exceptional 2-cycles and 43 for the 3-cycles. The complete
2-cycle ledger has 333 hits, and all 328 degree-{4,6} hits lie on the standard
MNT polynomials. No scalable family or cryptographically sized cycle was
found.

## Algebraic conditions

[PROVED] An \(m\)-cycle satisfies
\[
 t_i=p_i+1-p_{i+1},\qquad \sum_i t_i=m.
\]
For a 2-cycle, \(t_1+t_2=2\) and the two Frobenius discriminants are equal.
For a 3-cycle the trace sum remains 3, but the three discriminants need not
agree. Full derivations are in `NOTES.md` and `THREE_CYCLE_CONDITIONS.md`.

[PROVED] For prime-order cycles, the exact embedding degree at position \(i\)
is \(\operatorname{ord}_{p_{i+1}}(p_i)\). Every stored hit checks residue 1 at
the claimed degree and no smaller positive exponent.

## Published MNT regression

[CITED] Chiesa--Chua--Weidner 2019, Example 4.9, gives an MNT6 curve over
\(\mathbb F_{37}\) and an MNT4 curve over \(\mathbb F_{43}\) that form a
2-cycle (`refs/chiesa-chua-weidner2019.md`).

[EMPIRICAL: published x=3 curves over fields 37 and 43] Direct equation
enumeration and the independent Hasse/BSGS-twist counter both returned orders
43 and 37. The traces are -5 and 7, the common CM radicand is 123, and the exact
embedding degrees are 6 and 4
(`data/reproduce_mnt_cycle_x3_s4202_20260627.csv`).

## Primary 2-cycle census: degrees 3 through 12

[EMPIRICAL: 5 <= p < q < 65536, exact 3 <= k_i <= 12] The deterministic
search covered 6,540 primes, 21,382,530 unordered prime pairs, and 204,074
Hasse-valid pairs. It stored 245 pairs with at least one target degree: 26 full
hits and 219 one-sided near-misses
(`data/search_two_cycles_p5-65535_k3-12_20260708_summary.json`).

[EMPIRICAL: same range] The full-hit degree-pair counts are 13 copies of
(6,4), eight copies of (4,6), and one each of (10,3), (12,10), (9,8), (7,11),
and (10,11). The five exceptional field pairs are (7,11), (11,13), (17,19),
(23,29), and (23,31)
(`data/search_two_cycles_p5-65535_k3-12_20260708_candidates.csv`).

[EMPIRICAL: all 26 full hits in the primary 2-cycle census] All 52 curve
equations were explicitly constructed. BSGS and direct equation enumeration
both matched every target order, and exact embedding degrees were rechecked
(`data/construct_hit_cycles_n26_s4203_20260708.csv`).

[EMPIRICAL: 5 <= p < q < 65536, exact 3 <= k_i <= 12] There is no full hit
whose degree pair lies outside {(6,4),(4,6)} and whose larger field prime is at
least 32. This is the precisely scoped negative 2-cycle result.

[CITED] The (10,3) pair over fields 7 and 11 is independently present as the
exceptional MNT3 parameter-1 case in Belles-Munoz--Jimenez Urroz--Silva 2022,
Table 2 (`refs/belles-munoz-jimenez-urroz-silva2022.md`). No novelty claim is
made for any of the toy instances.

## Primary directed 3-cycle census: degrees 3 through 12

[EMPIRICAL: three distinct primes 5 <= p_i < 65536, exact 3 <= k_i <= 12]
The directed Hasse graph has 408,148 edges and 6,922,890 directed triangles up
to cyclic rotation. The search found five full hits, 37 two-of-three
near-misses, 6,902 one-of-three cases, and 6,915,946 zero-of-three cases
(`data/search_three_cycles_p5-65535_k3-12_20260708_summary.json`).

[EMPIRICAL: same range] The five directed field triples and degree triples are:

| Fields | Exact embedding degrees |
|---|---|
| (7,13,11) | (12,10,3) |
| (11,13,17) | (12,4,10) |
| (13,17,19) | (4,9,12) |
| (23,29,31) | (7,10,11) |
| (37,41,43) | (5,7,4) |

[EMPIRICAL: all five full primary 3-cycle hits] All 15 equations were
explicitly constructed, and both point counters matched every target order
(`data/construct_three_cycle_hits_n5_s4303_20260708.csv`).

[EMPIRICAL: three distinct primes 5 <= p_i < 65536, exact 3 <= k_i <= 12]
There is no full directed 3-cycle hit containing a field prime greater than
43. This is the precisely scoped negative length-3 result.

## Prime-bound extensions through 28 bits

[EMPIRICAL: primes below 2^18, exact degrees 3 through 12] Exhaustive search
found 34 2-cycle hits and the same five directed 3-cycle hits. The 2-cycle
extension added eight MNT-pattern hits; the 3-cycle candidate ledger stayed
exactly at five hits and 37 two-of-three near-misses. All 68 curves in the
extended 2-cycle ledger passed both point counters
(`data/search_two_cycles_p5-262143_k3-12_20260708_summary.json`,
`data/search_three_cycles_p5-262143_k3-12_20260708_summary.json`,
`data/construct_hit_cycles_n34_s5205_20260708.csv`).

[PROVED] The target-edge 3-cycle algorithm retains every full hit and every
two-of-three near-miss: either kind contains two consecutive target-degree
edges, which the join enumerates before testing closure. Its candidate rows
are identical to the exhaustive ledgers at 16 and 18 bits. The analogous
targeted 2-cycle algorithm remains candidate-complete while postponing
discriminant factorization; it matches the exhaustive rows at 16, 18, and 20
bits (`EXTENSION_20BIT.md`, `EXTENSION_22BIT.md`).

[EMPIRICAL: primes below 2^20, exact degrees 3 through 12] There are 47
2-cycle hits, adding 13 MNT-pattern hits. There remain five directed 3-cycle
hits, while the near-miss count rises to 40. The three new missing exact
degrees are 483,882, 2,055, and 115,320. All 26 curves in the 13 new 2-cycles
passed both point counters after twist-complement recovery
(`data/search_two_cycles_p5-1048575_k3-12_20260708_summary.json`,
`data/search_three_cycles_targeted_p5-1048575_k3-12_20260708_summary.json`,
`data/construct_hit_cycles_n13_s6207_20260708.csv`).

[EMPIRICAL: primes below 2^22, exact degrees 3 through 12] The targeted
2-cycle census covers 295,945 primes, 43,791,573,540 unordered pairs, and
54,092,289 Hasse-valid pairs. It retains 895 candidate rows: 76 hits and 819
one-sided near-misses. The hits consist of 40 degree-(6,4), 31 degree-(4,6),
and the same five tiny exceptional degree pairs
(`data/search_two_cycles_targeted_p5-4194303_k3-12_20260708_summary.json`).

[EMPIRICAL: all 29 2-cycle hits newly appearing from 20 to 22 bits] All 58
explicit curves passed BSGS and direct equation enumeration with zero order
mismatches. The largest field is 4,137,157 and the largest successful model
search took 43,462 coefficient trials
(`data/construct_hit_cycles_n29_s7207_20260708.csv`).

[EMPIRICAL: three distinct primes below 2^22, exact degrees 3 through 12] The
targeted directed search covers 108,184,578 Hasse edges and 971 target-degree
edges. It retains 47 rows: the same five full hits and 42 two-of-three
near-misses. The two new near-misses share the fields 3,894,703, 3,896,677,
and 3,898,651; their missing exact degrees are 556,386 and 1,949,325
(`data/search_three_cycles_targeted_p5-4194303_k3-12_20260708_summary.json`,
`data/analyze_three_cycle_near_misses_min1048576_n2_20260718.csv`).

[EMPIRICAL: distinct primes below 2^22, exact degrees 3 through 12] No
2-cycle outside degree pairs {(6,4),(4,6)} has larger field at least 32, and
no directed 3-cycle hit contains a field greater than 43. These are finite
negative results, not claims beyond the stated bound.

[EMPIRICAL: primes below 2^24, exact degrees 3 through 12] The Hasse-scanned
ledgers have 130 2-cycle hits, 1,364 one-sided near-misses, five directed
3-cycle hits, and 48 two-of-three near-misses. The 54 new 2-cycles are all
MNT-pattern. All 108 new explicit equations have matching BSGS orders and
independent prime-point Hasse certificates
(`data/search_two_cycles_targeted_p5-16777215_k3-12_20260708_summary.json`,
`data/search_three_cycles_targeted_p5-16777215_k3-12_20260708_summary.json`,
`data/construct_hit_cycles_n54_s8207_20260708.csv`).

[PROVED] Exact-order cyclotomic residues generate every target-degree Hasse
edge. Consequently, their unordered endpoints retain every reportable
2-cycle row, and joining the generated directed graph retains every reportable
3-cycle row (`CYCLOTOMIC_ROOT_ENUMERATION.md`).

[EMPIRICAL: complete 24-bit candidate ledgers] Root-generated and
Hasse-scanned CSVs are byte-identical. Root generation reduced the 2-cycle
runtime from 404.6 to 20.4 seconds and the 3-cycle runtime from 405.3 to 28.4
seconds.

[EMPIRICAL: primes below 2^26, exact degrees 3 through 12] There are 206
2-cycle hits, still only the original five exceptional hits, and the same five
directed 3-cycle hits. The near-miss count is 57. Eight new near-misses are
MNT-chain orientations; one isolated path has fields
\((24106111,24103481,24100957)\), target degrees (8,9), and closing degree
12,053,055
(`data/search_two_cycles_roots_p5-67108863_k3-12_20260708_summary.json`,
`data/search_three_cycles_roots_p5-67108863_k3-12_20260708_summary.json`).

[EMPIRICAL: primes below 2^28, exact degrees 3 through 12] The census covers
14,630,841 primes. It has 333 2-cycle hits and 3,714 one-sided near-misses;
the hits are 164 degree-(6,4), 164 degree-(4,6), and the same five tiny
exceptions. The directed ledger has five hits and 61 near-misses. All four
near-misses newly appearing above 26 bits are MNT-chain orientations
(`data/search_two_cycles_roots_p5-268435455_k3-12_20260708_summary.json`,
`data/search_three_cycles_roots_p5-268435455_k3-12_20260708_summary.json`).

[EMPIRICAL: distinct primes below 2^28, exact degrees 3 through 12] No
2-cycle outside degree pairs {(6,4),(4,6)} has larger field at least 32, and
no directed 3-cycle hit contains a field greater than 43. These are the final
finite negative statements of session 3.

## MNT classification and 3-chain obstruction

[PROVED] Let \(p<q\) be the field primes of a prime-order 2-cycle. Exact
degrees (6,4) force

\[
p=4x^2+1,\qquad q=4x^2+2x+1,
\]

while exact degrees (4,6) force

\[
p=4x^2-2x+1,\qquad q=4x^2+1.
\]

The proof reduces the two cyclotomic divisibilities using the gap \(q-p\),
then uses Hasse's bound to force the remaining integer multiplier to one
(`MNT_CLASSIFICATION.md`).

[EMPIRICAL: all 328 degree-{4,6} hits below 2^28] Every ledger row matches the
corresponding integer parameter formula: 164 in each orientation
(`data/verify_mnt_parameterization_n328_20260627.csv`).

[PROVED] The consecutive MNT triple

\[
(4x^2-2x+1,\;4x^2+1,\;4x^2+2x+1)
\]

never closes in either orientation with all exact embedding degrees in 3
through 12. A quadratic remainder recurrence excludes every \(x\ge1026\);
deterministic enumeration of \(1\le x\le1025\) finds four all-prime triples
and no closing hit (`MNT_THREE_CHAIN_OBSTRUCTION.md`,
`data/analyze_mnt_three_chains_x1-1025_20260627.csv`).

[PROVED] More generally, any two consecutive target edges with degree pair
(4,6) and equal signed field gaps are necessarily one orientation of that
consecutive MNT chain (`MNT_PATH_CLASSIFICATION.md`). Of the 61 directed
near-misses below \(2^{28}\), 26 are in this globally excluded class and 35
are residual isolated rows
(`data/classify_three_cycle_near_misses_n61_20260718.csv`).

[PROVED] If both exact degrees of a prime-order 2-cycle lie in {3,4,6}, then
the ordered degree pair is (6,4) or (4,6), hence the cycle is MNT. Hasse bounds
reduce all nine ordered pairs to an 11-row quadratic multiplier certificate;
the apparent (6,6) identity fails parity and every nonidentity root is invalid
(`QUADRATIC_DEGREE_CLASSIFICATION.md`).

## Global mixed and quartic degree classifications

[PROVED] If one exact 2-cycle degree lies in {3,4,6} and the other in
{5,8,10,12}, the only cycle is

\[
(p,q;k_1,k_2)=(7,11;10,3).
\]

Hasse bounds leave 108 multiplier cases. Reducing the quartic cyclotomic
condition modulo the monic quadratic side gives a linear remainder and a
complete even-gap bound, at most 2,649 (`MIXED_DEGREE_CLASSIFICATION.md`).

[PROVED] If both exact degrees lie in {5,8,10,12}, the only cycle is

\[
(p,q;k_1,k_2)=(11,13;12,10).
\]

The quotient-difference identity reduces all 16 ordered pairs to 750
large-gap genus-one equations plus 34 degenerate cases; all smaller gaps are
audited directly. Local congruences, exact real signs, and higher-power Hensel
lifting reduce the 750 rows to 47 rows on 29 normalized curves. Exact Magma
V2.29-8 computations close the final curves: 22 complete integral-point
lists, five empty fake two-Selmer sets, and one symmetric rank-zero curve
(`QUARTIC_DEGREE_REDUCTION.md`).

[EMPIRICAL: every even gap \(108\le c\le10^7\) on all 51 curves surviving
the first two sieves] The independent CRT-wheel search tested 11,333,558
curve/gap candidates and found no integral point
(`data/search_quartic_integral_points_c108-10000000_p251_20260718.csv`).

[PROVED] Combining the quadratic, mixed, and quartic theorems classifies every
prime-order 2-cycle whose two exact degrees lie in
{3,4,5,6,8,10,12}. Besides the two MNT orientations, the only cycles in this
class are the tiny ordered cases (10,3) over (7,11) and (12,10) over (11,13).

## One-axis relaxation: degrees 3 through 18

[EMPIRICAL: same 16-bit prime spaces, exact 3 <= k_i <= 18] Raising only the
degree ceiling increased 2-cycle hits from 26 to 36 and directed 3-cycle hits
from 5 to 12
(`data/search_two_cycles_p5-65535_k3-18_20260708_summary.json`,
`data/search_three_cycles_p5-65535_k3-18_20260708_summary.json`).

[EMPIRICAL: all relaxed full hits] All 72 relaxed 2-cycle equations and all 36
relaxed 3-cycle equations passed both point counters and their exact degree
checks (`data/construct_hit_cycles_n36_s4502_20260708.csv`,
`data/construct_three_cycle_hits_n12_s4503_20260708.csv`).

[EMPIRICAL: same relaxed ranges] The non-{(6,4),(4,6)} 2-cycle hits have larger
field prime at most 271, and the directed 3-cycle hits have every field prime
at most 673. Thus no relaxed exceptional 2-cycle occurs from 272 through
65,535, and no relaxed 3-cycle contains a field above 673.

## Rho

[PROVED] With the standard prime-order per-curve definition
\(\rho_i=\log(p_i)/\log(p_{i+1})\), every distinct prime-order 2-cycle over
fields at least 5 automatically satisfies \(\rho_{\max}<2\) by Hasse's bound.
The published fields 37 and 43 give \(\rho_{\max}=1.041618836729\).

[PROVED] The geometric mean of the per-curve rho values is identically 1 for
every prime-order cycle, so P4.2 uses their maximum. Q010 records that the
prompt may have intended another metric (`GLOSSARY.md`, `OPEN_QUESTIONS.md`).

## Limitations

[PROVED] The primary finite negative statements above say nothing about a
prime at least \(2^{28}\), an embedding degree above 12, composite-order
variants, repeated field primes, or polynomial families that have no instance
inside the finite range. The degree-18 relaxation remains only a 16-bit
result. The global 2-cycle classifications for degrees in
{3,4,5,6,8,10,12} and the consecutive-MNT-chain obstruction are the
stated-class exceptions to this finite-bound limitation. Exact degrees 7, 9,
and 11 remain outside those global 2-cycle theorems.

[EMPIRICAL: construction ledgers through 24 bits] Every full arithmetic hit
through \(2^{24}\) was converted to explicit curves and independently
verified. Above 24 bits, all newly appearing full hits are degree-{4,6} rows
covered by the global MNT classification and exact arithmetic checks, but
individual curve equations were not redundantly model-searched. The much
larger near-miss ledgers contain isogeny-class parameters only; they are not
presented as full cycle candidates.

SageMath was unavailable, and `lib/tnfs_cost.py` was absent when the searches
ran but appeared before the final shared test pass. Neither search imports that
helper. The substitute construction is seeded random model search using exact
BSGS counts, followed by direct equation enumeration through 22 bits and the
independent prime-point Hasse certificate at 24 bits.
