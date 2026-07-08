# Archived log - Sessions 1--10

## Session 1 - 2026-06-23

**Goal:** Complete SG-01 and build a validated first baseline for SG-02/SG-03.

**Prediction (written before running anything):** [HEURISTIC] For uniformly
sampled nonsingular short-Weierstrass curves, the measured probability that
$\#E(\mathbb F_r)$ is $B$-smooth will have the same order of magnitude as the
probability for a random integer near $r$; this prediction is falsified in the
tested range if the observed binomial confidence interval excludes the stated
integer baseline by a practically significant factor fixed in A001 before the
run.

**Did:**
- Initialized the P2.1 persistent folder and inspected the shared curve and DLP
  helpers.
- Ran the environment check and all shared tests before new mathematics.
- Verified the exact auxiliary-group condition and curve embedding directly in
  Maurer--Wolf 1999.
- Added an exact BSGS/twist point counter to `lib/curves.py`, tests, a seeded
  measurement script, exact interval baselines, Dickman estimates, and Wilson
  intervals.
- Ran 512 curves at each of 12, 16, ..., 40 bits for smoothness exponents 2
  and 3.

**Found:**
- [CITED] The auxiliary curve may be noncyclic, but its exact order must be
  known and $(\log r)^{O(1)}$-smooth; the rank-at-most-two curve group is
  handled by generalized Pohlig--Hellman (Maurer--Wolf 1999, Theorem 2 and
  Section 4.1.1).
- [PROVED] The DH oracle performs multiplication on implicit
  $\mathbb F_r$ elements, enabling the randomized curve embedding and final
  extraction of the target logarithm.
- [EMPIRICAL: 36 curves over 101 <= r <= 65519] The new point counter matched
  exhaustive enumeration in every validation.
- [EMPIRICAL: one prime at each of 12,16,...,40 bits; 512 curves per prime]
  At 40 bits, $B=1600$ succeeded 4/512 times (first hit 65) and $B=64000$
  succeeded 52/512 times (first hit 6); full details are in the summary CSV.
- [CITED] Jain's 2026 all-interval theorem remains outside the needed regime:
  its smoothness lower bound is super-polylogarithmic and its required
  interval is longer than the Hasse interval (Jain 2026, Theorem 1.2).

**Prediction vs. outcome:** [EMPIRICAL: same 4,096-curve run] Matched the
pre-registered factor-two criterion: all curve-to-integer rate ratios were in
$[0.867,1.859]$. Some small-size integer rates were outside the Wilson
interval, so the stronger claim of identical finite distributions was not
supported.

**Did not work:** [HEURISTIC] Blind random search does not plausibly become a
polylogarithmic construction: with $B=(\log r)^C$, the Dickman model predicts
$r^{1/C+o(1)}$ candidates. A proved polylogarithmic candidate bound would
falsify this assessment.

**Changed my mind about:** [HEURISTIC] The obstruction is sharper than "point counting is
expensive": even granting polynomial-time SEA per candidate, the candidate
count predicted for a polylogarithmic smoothness bound is super-polynomial in
$\log r$. A proved polylogarithmic candidate bound would refute this view.

**Next:** Enumerate the explicit CM order families from Maurer--Wolf Section
4.1.3 and measure what fraction of the smooth Hasse orders they can realize.

## Session 2 - 2026-06-25

**Goal:** Complete SG-04, then use its output to start SG-05 and isolate the
constructive obstruction in SG-06.

**Prediction (written before running the Session 2 experiments):** [HEURISTIC]
The constant-size $j=0$/$j=1728$ order lists will show decreasing smooth-order
success as the field size grows, while a bounded-discriminant CM search with
$|D|\le(\log_2 r)^3$ will fail for at least one tested prime through 40 bits.
The explicit-family part is falsified by a stable nondecreasing Wilson trend
over the largest three sizes; the bounded-CM part is falsified if every tested
prime has a qualifying smooth order.

**Did:**
- Reopened the completed SG-01--03 handoff and initialized A002.
- Wrote validation tests first, then implemented the explicit $j=0$/$j=1728$
  order lists and bounded fundamental-discriminant CM scanner.
- Added process parallelism after the serial 44--60-bit commands exceeded the
  interactive wait window; the serial jobs ultimately completed and their
  189.47-second and 747.32-second files were retained.
- Extended the run to 4,096 descending 60-bit primes at discriminant bounds
  $60^2$ and $60^3$, then added a tested residue-class aggregator.
- Checked the CM construction and complexity qualifiers in
  Muzereau--Smart--Vercauteren 2004, Enge 2009, and May--Schneider 2023.

**Found:**
- [EMPIRICAL: p in {7,13,17,19,31,37}] The explicit twist formulas matched
  exhaustive point counts for every tested coefficient.
- [EMPIRICAL: p in {101,211}, |D| <= 200] Cornacchia enumeration matched a
  direct ordinary-trace scan, and four known class numbers matched.
- [EMPIRICAL: 128 descending primes at each of 44,48,52,56,60 bits]
  $B=|D|=L^3$ succeeded for all 640 prime/size instances, while explicit
  success declined from 52/128 to 15/128.
- [EMPIRICAL: 4,096 descending 60-bit primes, B=60^3] The explicit families,
  $|D|\le60^2$ CM scan, and $|D|\le60^3$ CM scan covered respectively
  445, 3,635, and 4,096 primes.
- [EMPIRICAL: same 4,096 primes, B=60^3 and |D|<=60^2] Coverage ranged from
  97.07% for $r\equiv1\pmod{12}$ to 76.48% for
  $r\equiv11\pmod{12}$; the explicit list has respectively 10 and 1
  candidate orders in those classes.
- [CITED] Muzereau--Smart--Vercauteren 2004 already isolates the need for a
  small CM discriminant whose associated order is smooth; May--Schneider 2023
  instead uses finite random curve searches and calls the auxiliary curve the
  non-uniform part of the reduction.
- [CONDITIONAL: Enge's floating-point precision heuristic] A
  polylogarithmic-discriminant witness can be converted through a class
  polynomial within a polynomial bit complexity; Enge's height bound is
  rigorous but its combined sharp rounding conclusion is explicitly
  heuristic.
- [EMPIRICAL: all 7,731 successful rows in the two 4,096-prime files] A final
  audit rechecked $t^2-Dv^2=4r$, $N=r+1-t$, and the recorded smoothness bound
  for every hit.
- [EMPIRICAL: 63 shared tests and 8 P2.1 tests] The final environment and full
  regression suite passed on Python 3.13.4.

**Prediction vs. outcome:** [EMPIRICAL: the recorded ensembles] The explicit
decay prediction matched qualitatively.  The bounded-CM prediction was
falsified already through 40 bits and more strongly by all-success $L^3$
coverage on the 44--60-bit and 4,096-prime runs.

**Did not work:** [HEURISTIC] Neither explicit families nor bounded-CM search
became a proof for every prime.  A fixed $L^K$ discriminant range exposes only
polynomially many candidate orders, for which the supported random-integer
model predicts $L^K r^{-1/C+o(1)}\to0$ coverage.  A proved arithmetic
correlation would falsify this assessment.

**Changed my mind about:** [EMPIRICAL: all 4,096 tested 60-bit primes] Cubic
discriminant coverage is much stronger at the permitted toy scale than the
pre-registered expectation.  It is worth retaining as a practical finite-size
strategy, but the same result does not support a worst-case asymptotic claim.

**Next:** Q005 is now the only blocking thread: prove or refute a uniform
small-CM/smooth-order correlation, or replace CM by a structured family with
proved coverage.  Do not extend the same finite scan past the 60-bit scaffold
ceiling.

## Session 3 - 2026-06-29

**Goal:** Attack Q005 directly by exhausting current smooth-interval/auxiliary-
group routes and replacing the informal blind-search obstruction by the
strongest rigorous oracle-model lower bound available from the same data.

**Prediction (written before the Session 3 audit):** [CONJECTURE] No checked
primary source will give an every-prime, polylogarithmic-smooth auxiliary group
that is uniformly constructible in $\operatorname{poly}(\log r)$ time; the
alternative-group papers will remain parameter-specific or conditional.  This
is refuted by a source with an explicit algorithm, worst-case coverage theorem,
and polynomial bit-complexity.  [PROVED] Independently of that literature
outcome, an idealized random-order oracle should admit an exact adaptive query
lower bound in terms of the smooth-order fraction of the Hasse interval.

**Did:**
- Initialized A003 and reopened Q005 after the completed finite experiments.
- Checked the current multiplicative-group reduction of
  Bollauf--Parisella--Siim 2025, Li's 2025 shifted-prime theorem, and Younis's
  2024 smooth-short-interval theorems in primary sources.
- Proved the exact optimal adaptive success probability in an explicitly iid
  Hasse-order oracle.
- Wrote failing tests first, implemented `random_order_lower_bound.py`, and
  generated exact $L^2$ and $L^3$ query-budget tables through 40 bits.
- Updated the source notes, stable notes, attempt record, sub-goals, code
  instructions, state, and handoff.

**Found:**
- [CITED] The den Boer multiplicative route is polynomial when
  $P^+(r-1)=(\log r)^{O(1)}$ (Bollauf--Parisella--Siim 2025).
- [CITED] Infinitely many primes satisfy $P^+(r-1)>r^{0.679}$ (Li 2025).
- [PROVED] Hence no fixed polylogarithmic bound makes the full
  $\mathbb F_r^*$ auxiliary group work for every prime; full
  $\mathbb F_{r^n}^*$ remains obstructed because $r-1\mid r^n-1$.
- [CITED] Under RH, Younis 2024 reaches polylogarithmic smoothness only for
  fixed short-interval exponent $\theta>1/2$, not the Hasse endpoint.
- [PROVED] In the iid Hasse-order oracle, any adaptive $q$-query algorithm has
  success at most $1-(1-\alpha)^q$, and querying fresh labels attains it.
- [EMPIRICAL: exact 40-bit Hasse interval] The 50%/95% budgets were 91/391 for
  $B=L^2$ and 6/25 for $B=L^3$.
- [EMPIRICAL: 65 shared tests and 9 P2.1 tests] The final full regression suite
  passed on Python 3.13.4.

**Prediction vs. outcome:** [EMPIRICAL: primary-source audit through
2026-06-29] The literature prediction was not falsified: no checked result
simultaneously gave every-prime coverage, polylogarithmic smoothness, and
polynomial construction.  The oracle formula matched exhaustive finite answer
spaces exactly, as its proof predicted.

**Did not work:** [PROVED] The multiplicative route fails on an infinite prime
family, and current short-interval theorems miss the required endpoint.
[PROVED] The iid lower bound cannot be transferred to structured curve-order
maps without an additional theorem controlling those maps and adaptive
coefficient choice.

**Changed my mind about:** [PROVED] There is now a genuine unconditional
infinite-family obstruction, but only for the full multiplicative auxiliary
group and full extension multiplicative groups.  It would be incorrect to
report an obstruction for selected subgroups, tori, elliptic curves, or all
strongly algebraically defined groups.

**Next:** Q005 remains: establish or refute uniform $\mathsf{SCM}_{C,K}$, or
find a selected subgroup/tori/other constant-rank family with an every-prime
smooth-order and efficient-embedding theorem.  Further iid sampling or scans
at the 60-bit ceiling will not close this proof gap.

## Session 4 - 2026-07-01

**Goal:** Test the simplest selected-torus replacement: choose between the
split torus of order $r-1$ and the quadratic norm-one torus of order $r+1$.

**Prediction (written before validation):** [CONJECTURE] CRT plus Linnik's
least-prime theorem yields infinitely many primes for which both orders have
a factor $r^{\Omega(1)}$, so this finite menu is not a uniform solution.  A
gap in simultaneously forcing the two large factors falsifies the proposed
argument.

**Did:**
- Initialized A004 and stated the algebraic/formula falsifiers before adding
  the torus validation code.
- Wrote failing tests first, then implemented and exhaustively validated the
  quadratic norm-one torus parametrization, extraction, and group law.
- Checked Xylouris's effective Linnik theorem in the primary text.
- Combined Bertrand, CRT, and Linnik into a simultaneous $r-1$/$r+1$
  large-factor theorem, then analyzed smooth subgroups in the standard
  shift-and-test model.

**Found:**
- [PROVED] The torus $x^2-dy^2=1$ is cyclic of order $r+1$ and has a
  constant-degree bijection from $\mathbb F_r$ onto all but one point, with
  efficient extraction.  It is a valid related auxiliary whenever $r+1$ is
  polylogarithmically smooth.
- [EMPIRICAL: four complete toy fields] All points, parameters, extractions,
  and group products matched the derived formulas.
- [CITED] Linnik's least-prime theorem admits an effective absolute exponent
  $L_0=5.2$ (Xylouris 2009).
- [PROVED] Infinitely many primes satisfy both
  $P^+(r-1),P^+(r+1)\ge c r^{1/10.4}$ for an absolute $c>0$.
- [PROVED] Thus neither choosing between the two full one-dimensional tori nor
  using uniform random shifts to hit their smooth subgroups is polynomial on
  this prime family.
- [PROVED] A fixed-modulus PNT/CRT extension simultaneously forces a
  polynomially large factor in every full norm-one torus of degree
  $1\le n\le D$, for each globally fixed $D$.
- [EMPIRICAL: 69 shared tests and 11 P2.1 tests] The final full regression
  suite passed on Python 3.13.4.

**Prediction vs. outcome:** [PROVED] Confirmed.  The CRT conditions are
coprime, their modulus is $O(X^2)$, and Linnik keeps the resulting prime below
$O(X^{2L_0})$, preserving both forced factors as fixed powers of $r$.

**Did not work:** [PROVED] The new obstruction does not classify general
bounded-dimensional tori and does not extend to non-shift subgroup embeddings
or elliptic curves merely from their order formulas.  It does cover all full
norm-one extension degrees under any fixed global degree bound.

**Changed my mind about:** [PROVED] The nonsplit torus is algebraically much
simpler than a CM curve and gives a clean positive reduction on smooth-$r+1$
inputs, but it does not complement smooth-$r-1$ inputs in the worst case.

**Next:** The residual alternative-structure direction starts with general
bounded-dimensional tori or selected subgroups equipped with a genuinely new
efficient embedding; Q005 for elliptic CM remains unchanged.

## Session 5 - 2026-07-06

**Goal:** Decide whether A004 extends from full norm-one tori to every full
algebraic torus of uniformly bounded dimension, then perform the mandatory
fifth-session self-audit.

**Prediction (written before constructing the proof):** [CONJECTURE] The
finite-order Frobenius action makes every bounded-dimensional torus order a
product from a finite cyclotomic menu, so a single CRT--Linnik construction
will force a polynomially large factor in every menu entry simultaneously.
The explicit falsifiers are recorded in A005.

**Did:**
- Opened A005 and checked the finite-field torus point-count formula in
  Batyrev--Tschinkel 1995.

**Found:**
- [CITED] Every $d$-dimensional finite-field torus order is
  $\det(rI-\Phi)$ for a finite-order integral $d\times d$ Frobenius matrix
  (Batyrev--Tschinkel 1995, Theorem 1.3.11).
- [PROVED] Its order polynomial is a product of $\Phi_n(r)$ with
  $\varphi(n)\le d$; only finitely many $n$ occur below a fixed $D$.
- [PROVED] One CRT--Linnik prime family simultaneously forces a factor
  $c_Dr^{1/(|\mathcal N_D|L_0)}$ in every possible full torus order of
  dimension at most $D$.

**Prediction vs. outcome:** [PROVED] Confirmed.  All three falsifiers failed:
the Frobenius polynomial is cyclotomic, the index menu is finite, and the
simultaneous exact-order congruences retain a fixed-power factor after
Linnik's bound.

**Did not work:** [PROVED] A large factor in the full rational-point group does
not automatically exclude a selected smooth subgroup.  A005 also says
nothing about abelian varieties, including elliptic curves.

**Changed my mind about:** [PROVED] The norm-one calculation was not a special
accident: finite-order Frobenius makes the entire bounded-dimensional full-
torus class a finite cyclotomic problem.

**Next:** Run the fifth-session audit, then analyze affine commutative groups
and selected subgroups under Maurer--Wolf's strong algebraic-definition model.

## Session 6 - 2026-07-08

**Goal:** Eliminate full connected commutative groups with affine structure
and determine how far the selected-subgroup escape survives a general
recoverable encoding.

**Prediction (written before formalizing the proof):** [CONJECTURE] Chevalley
decomposition and the unipotent radical will reduce full groups to abelian
varieties, while a fixed-public-coin injectivity count will close selected
subgroups in dimension one.  Dimension at least two is expected to survive
the cardinality argument.

**Did:**
- Opened A006 and checked Chevalley's theorem, the perfect-field unipotent-
  radical structure, and Lang's theorem in primary sources.
- Proved the rational-point factorization and the public-coin target-size
  lemma.

**Found:**
- [CITED] A full smooth connected commutative group has an affine kernel and
  abelian-variety quotient; its affine kernel has split unipotent radical and
  torus quotient.
- [PROVED] A positive-dimensional unipotent part forces the input prime $r$
  into the group order, while a nontrivial torus part is covered by A005.
- [PROVED] Hence the only unobstructed full connected commutative class is
  pure abelian varieties.
- [PROVED] Any correct public-coin recoverable encoding with target $H$ has
  average success at most $|H|/r$ on $\mathbb F_r$.
- [PROVED] On A005's prime family, every polylog-smooth subgroup of a one-
  dimensional torus has size $O(r^{1-\eta})$, so its recoverable-encoding
  success is negligible even beyond the shift-and-test model.

**Prediction vs. outcome:** [PROVED] Confirmed.  The higher-dimensional
selected-subgroup branch remains because the ambient $r^d$ cardinality can
absorb the forced factor and still leave at least $r$ elements.

**Did not work:** [PROVED] The argument does not eliminate pure abelian
varieties, selected subgroups in dimension at least two, uncontrolled
disconnected families, or encodings carrying recovery information outside
the auxiliary group.

**Changed my mind about:** [PROVED] The affine-group branch is not an
independent construction frontier: for full connected commutative groups it
collapses completely to the already solved unipotent and torus cases.

**Next:** Audit prescribed-order theorems for fixed-dimensional abelian
varieties and determine whether Honda--Tate can turn a smooth target integer
near $r^g$ into a uniform constructive auxiliary group.
