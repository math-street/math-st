---
attempt: A002
status: promising
---
# A002 - CM and explicit-family coverage

## Idea

Measure two increasingly broad constructive families over $\mathbb F_r$:

1. the $j=0$ and $j=1728$ order formulas in Maurer--Wolf Section 4.1.3;
2. smooth Hasse orders classified by their fundamental CM discriminant.

## Prior art

[CITED] Maurer--Wolf 1999, Section 4.1.3, gives constant-size explicit order
lists obtained from the $j=0$ and $j=1728$ families.

[CITED] The CM equation for a curve with trace $t$ is
$t^2-4r=Dv^2$, where $D<0$ is a fundamental discriminant; a root of $H_D$
modulo $r$ gives a CM $j$-invariant (Muzereau--Smart--Vercauteren 2004,
Section 5; Enge 2009, Section 2).

## Plan

1. Validate both explicit order formulas against exact point counting.
2. Enumerate their smoothness success over many seeded primes through 40 bits.
3. For smooth orders, compute the associated fundamental discriminant and
   record the smallest discriminant cost found.
4. Compare explicit-family coverage, bounded-discriminant CM coverage, and
   the full smooth Hasse interval.

## Prediction and decision rule

[HEURISTIC] A constant-size explicit order list will have success probability
of the same order as a constant number of random Hasse integers, so its
success rate for $B=(\log r)^C$ should decrease with the bit length. This is
falsified on the tested prime ensemble if the Wilson intervals show a stable
nondecreasing success rate over the largest three sizes.

[HEURISTIC] The least fundamental CM discriminant among smooth orders will
grow faster than every tested fixed power of $\log r$ on a substantial
fraction of primes. This finite prediction is rejected if every tested prime
through 40 bits has a smooth order with $|D|\le(\log_2 r)^3$.

## Execution log

[PROVED] Added `code/measure_cm_coverage.py` with fundamental-discriminant
enumeration, Cornacchia norm solving, $j=0$/$j=1728$ order formulas, reduced
binary-quadratic-form class numbers, deterministic descending-prime ensembles,
Wilson intervals, CSV output, and process parallelism.

[EMPIRICAL: p in {7,13,17,19,31,37}] Exhaustive point counting over every
nonzero coefficient validated both explicit twist-order families.

[EMPIRICAL: p in {101,211}, |D| <= 200] The bounded-CM trace set matched a
direct Hasse-trace scan; four known class numbers and the extra-unit traces for
$D=-3,-4$ also matched.

[EMPIRICAL: 128 descending primes at each of 44,48,52,56,60 bits] The serial
two-bound scan took 747.32 seconds.  For $B=|D|=L^3$, all 640 prime/size
instances succeeded; explicit success counts were respectively
52, 42, 34, 24, and 15 out of 128.

[EMPIRICAL: 4,096 descending 60-bit primes] Eight-worker scans took 28.50
seconds at $(B,|D|)=(L^3,L^2)$ and 42.95 seconds at
$(B,|D|)=(L^3,L^3)$.  Coverage was respectively 3635/4096 and 4096/4096;
the explicit families covered 445/4096.

[PROVED] Added `code/summarize_cm_residues.py` after first writing a
hand-counted failing test, then generated the modulo-12 summaries from the raw
4,096-prime files.

## Outcome

[EMPIRICAL: all tested primes through 40 bits, then the stated 44--60-bit
ensembles] The pre-registered bounded-CM failure prediction was falsified:
every tested prime had an $L^3$-smooth order with $|D|\le L^3$.  The explicit
family prediction matched qualitatively, with a strict decrease over the
44--60-bit $B=L^3$ series.

[EMPIRICAL: 4,096 descending 60-bit primes, B=L^3] Reducing the discriminant
bound from $L^3$ to $L^2$ exposed failures and a strong residue effect:
coverage was 97.07% for $r\equiv1\pmod{12}$ but 76.48% for
$r\equiv11\pmod{12}$.

[PROVED] The experiment isolates the sufficient small-CM condition
$|D|\le L^K$, $4r=t^2-Dv^2$, and
$P^+(r+1-t)\le L^C$.  Enumerating and smoothness-testing such integer
witnesses is randomized expected polynomial time for fixed $C,K$.

[CONDITIONAL: Enge's floating-point class-polynomial precision heuristic, or
another certified polynomial-time CM implementation] Such a witness can be
turned into the auxiliary curve in polynomial time; this code measures the
integer reachability and discriminant cost but does not implement that final
class-polynomial step.

[HEURISTIC] The route remains asymptotically unsupported: only
$O(L^K)$ candidate orders are exposed, and the random-integer model predicts
$L^K r^{-1/C+o(1)}\to0$ coverage.  A proved small-CM/smoothness correlation
or uniform construction would falsify this assessment.

## What transfers

[PROVED] The norm-equation scanner, validation suite, residue aggregator, and
the formal $\mathsf{SCM}_{C,K}$ condition are reusable.  Further searches at
the same toy scale are unlikely to address Q005; the next useful advance must
be a theorem about correlated smooth values, a different structured family,
or a rigorous obstruction model.
