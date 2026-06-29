# Bollauf--Parisella--Siim 2025

[CITED] Maiara F. Bollauf, Roberto Parisella, and Janno Siim, "Revisiting
Discrete Logarithm Reductions," *IACR Communications in Cryptology* 2(2),
2025. DOI: 10.62056/a0c3c3c2h; IACR ePrint 2025/1079.

Primary text checked at:
<https://eprint.iacr.org/2025/1079>

## Result relevant to P2.1

[CITED] The paper gives a concretely efficient den Boer reduction for a
prime-order source group of order $r$ using the auxiliary multiplicative
group $\mathbb F_r^*$ when the prime factors of $r-1$ are sufficiently small.
Its Pohlig--Hellman-style cost contains square-root terms in the distinct
prime factors of $r-1$.

[PROVED] In asymptotic P2.1 notation this route is polynomial in $\log r$
when $P^+(r-1)=(\log r)^{O(1)}$.  The paper's concrete "somewhat smooth"
regime is useful for selected standardized parameters, but its result is not
an every-prime smoothness theorem.

## Verification performed

[EMPIRICAL: primary ePrint metadata and published full text inspected
2026-06-29] The abstract, main reduction, Pohlig--Hellman subroutine, and its
factor-dependent complexity table were checked directly.
