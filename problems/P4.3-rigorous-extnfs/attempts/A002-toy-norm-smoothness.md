---
attempt: A002
status: promising
---
# A002 - Exact toy tower-norm smoothness comparison

## Idea

[PROVED] Use $p=5$, $h(t)=t^2+2$, $f(x)=x^3+x+1$, and $g(x)=x^3+x-4$, so $f$ and $g$ have the same irreducible cubic reduction modulo $5$ and $h$ is irreducible modulo $5$.

## Prior art

[CITED] Kim--Barbulescu 2016 define each exTNFS norm as an iterated resultant and replace its smoothness density by the random-integer density in their complexity analysis.

## Plan

[PROVED] Enumerate every primitive coefficient tuple $(a_0,a_1,b_0,b_1)\in[-4,4]^4$, compute and fully factor both iterated resultants, then compare them with two independent uniform random integers from the corresponding dyadic intervals.

## Prediction

[CONJECTURE] The actual sides have positive smoothness dependence because they share $a^3+ab^2$.  This is refuted if the exact joint-dependence ratio is at most $1$ at three of the four tested bounds.

## Execution log

[PROVED] `code/measure_norm_smoothness.py` exhaustively processed 5,856 primitive vectors, using seed 4304 for the matched dyadic baseline.  Deterministic trial division completely factored all actual and baseline values.

[PROVED] Independent validation with SymPy reproduced all 23,424 recorded factorizations and 128 nested resultants from 64 stratified candidates.  The three unit tests also pass.

[EMPIRICAL: p=5, eta=2, kappa=3, A=4, 5,856 primitive vectors] At $B=7,13,31,61$, the actual joint-smooth rates were respectively 8.50, 7.76, 3.66, and 3.05 times the matched dyadic random-integer rates.  The actual joint/product-of-marginals ratios were 7.73, 5.14, 3.81, and 2.82.

## Outcome

[PROVED] The preregistered positive-dependence prediction was not refuted, and the preregistered divergence criterion was met at every tested bound.

[PROVED] The experiment demonstrates finite-parameter arithmetic structure but cannot establish or refute an asymptotic $L$-exponent.  The baseline samples are side-independent conditional on the observed norm magnitudes; their aggregate indicators remain correlated through those shared candidate-dependent magnitudes.
