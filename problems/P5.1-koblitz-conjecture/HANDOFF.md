# Handoff -- P5.1 -- after session 5

## State in five lines

- [PROVED] SG-01--SG-12 are complete for the repository's algebraic, computational, source-audit, and self-verification scope.
- [EMPIRICAL: 85 tests] Shared and P5.1 tests pass.
- [EMPIRICAL: all 50 published checkpoints] The exact CM run has zero actual-count and zero rounded-integral mismatches against Zywina's Table 3.
- [PROVED] The CM event is an explicit simultaneous norm-prime pattern, apart from the exceptional event $p=17$.
- [CITED] The unconditional fixed-curve asymptotic remains open; Q026 is the only theoretical boundary. (Dey et al. 2025; Lee, Mayle, and Wang 2025.)

## What is established

- [CITED] Zywina's universal product is $0.505166168239435774\ldots$; the 1728.w1 correction is $10/9$. (Zywina 2011.)
- [EMPIRICAL: all good primes $5\le p\le2^{17}$] The Serre prime-order ratio is 1.04293 and the 540.f2 quotient-order ratio is 1.01600.
- [CONDITIONAL: LMFDB's 540.f2 adelic data are correct] Exact level-90 enumeration gives $\delta_{E,3}(90)=91/648$ and correction $5824/5913$.
- [CITED] For $y^2=x^3-x$, the CM formulation uses $E_{\mathbb Q(i)}$, $t=8$, split primes $p\equiv1\pmod4$, and constant $1.067350894\ldots$. (Zywina 2011, Section 7.)
- [PROVED] If $p=a^2+b^2$ and $a\equiv1\pmod4$, then the order is $N(a+bi-1)$ for $p\equiv1\pmod8$ and $N(a+bi+1)$ for $p\equiv5\pmod8$; the first class gives a prime quotient only at $p=17$.
- [EMPIRICAL: $x=10^9$] The run counts 1,548,766 events among 25,423,491 split primes versus 1,549,656.621 predicted, ratio $0.9994253$.

## Self-verification

- [EMPIRICAL: 15 primes through $9\mathbin{\cdot}10^8$] Specialized CM and generic BSGS orders agree.
- [EMPIRICAL: split primes through $5\mathbin{\cdot}10^6$] Independent odd-only, full, and segmented sieves return the same 174,193-element sequence.
- [EMPIRICAL: 500 quotient samples] Eratosthenes, Miller--Rabin, and SymPy primality decisions have zero mismatches.
- [EMPIRICAL: all 74,416 split primes through $2\mathbin{\cdot}10^6$] The new norm identity, divisibility by $8$, and unique one-mod-eight event $(17,2)$ agree.
- [PROVED] Published fixtures are comparison-only; mutation changes no computed event count.

## Latest literature boundary

- [CITED] Dey et al. determine the refined fixed-curve constant under an elliptic Elliott--Halberstam conjecture and a separate average-growth conjecture. (Dey et al. 2025.)
- [CITED] Lee--Mayle--Wang's unconditional results concern moments of constants over families and explicitly leave the fixed-curve conjecture open. (Lee, Mayle, and Wang 2025.)
- [CITED] Xie's unconditional CM result proves bounded-almost-prime statements over prime-power fields, not the Koblitz prime-order asymptotic. (Xie 2025.)
- [CITED] David--Wu's GRH-strength input gives an eight-almost-prime lower bound and prime-order upper bound, not a prime-order lower bound. (David and Wu 2012.)

## What is ruled out

- [EMPIRICAL: $p\le2^{17}$] The raw $C_Ex/(\log x)^2$ expression is too biased for toy-range comparison; use the refined predictor.
- [EMPIRICAL: all good rational primes $5\le p\le2^{17}$] Pooling CM split and inert strata into the inapplicable full-$\mathrm{GL}_2$ model gives ratio $4.0508$.
- [PROVED] A larger finite cutoff cannot by itself turn the recorded evidence into an asymptotic proof.

## Active thread and next action

- [PROVED] A001 is complete for every scoped deliverable; Q026 is an external theorem, not an unfinished computation.
- [CONJECTURE] The only route to a full unconditional solution is a theorem that supplies both uniform distribution at the required moduli and a parity-breaking prime-value input; failure of the predicted asymptotic would refute that route.

## Invariants -- do not violate

- [PROVED] Never apply the universal product to a new curve without certifying its adelic correction.
- [CITED] Keep CM split-prime data separate from non-CM rational-prime data. (Zywina 2011, Section 7.)
- [PROVED] The factor $5824/5913$ belongs to 540.f2, not Zywina's Section 6 curve, whose factor is $6160/5913$.
- [HEURISTIC] Numerical agreement through $10^9$ is not an asymptotic proof; any future sustained departure can falsify the heuristic prediction.

## Files that matter

- `THEORY_CLOSURE.md` -- exact CM reduction and honest closure classification.
- `code/reproduce_cm_table.py` -- exact CM trace, segmented sieve, integral, and 50-row regression.
- `data/reproduce_cm_table_x1000000000_s51012026_20260720.csv` -- complete table reproduction.
- `audits/SELF-CHECK-20260713.md` and `audits/AUDIT-20260720.md` -- adversarial and fifth-session audits.
- `refs/dey-et-al2025.md`, `refs/lee-mayle-wang2025.md`, `refs/xie2025.md` -- current literature boundary.

## What I would tell my replacement

- [PROVED] The remaining issue is exactly Q026; do not rerun the finite computations or relabel the open fixed-curve asymptotic as solved.

