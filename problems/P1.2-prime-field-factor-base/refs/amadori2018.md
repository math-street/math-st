# Amadori–Pintore–Sala 2018 — Prime-field one-system variant

## Source

[CITED] Alessandro Amadori, Federico Pintore, and Massimiliano Sala, “On the
Discrete Logarithm Problem for Prime-Field Elliptic Curves,” *Finite Fields
and Their Applications* 51, 168–182, 2018,
doi:10.1016/j.ffa.2018.01.009; IACR ePrint 2017/609.
<https://eprint.iacr.org/2017/609.pdf>

## Results used here

[CITED] The paper summarizes the prime-field obstruction as the lack of an
algebraically useful factor base and the inability to use Weil descent. It
proposes building the factor base from sampled relation points and replacing
many relation systems plus linear algebra by one multivariate system.

[CITED] Its conclusion states that the complexity of that single system is not
well understood and that further work is needed before obtaining an
improvement over Pollard rho.

## Repository consequence

[PROVED] This is evidence that reducing the number of Gröbner computations
does not supply the polylogarithmic per-target decomposition algorithm demanded
by Variant S. It does not constitute a lower bound against a different
coordinate-aware method.

No published computation was reproduced.
