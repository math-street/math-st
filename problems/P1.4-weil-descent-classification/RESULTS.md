# Results — Session 1

**Outcome: FAILED.** The session produced only the permitted span/genus fallback; it did not construct the GHS curve or cover map and did not validate an end-to-end toy attack.

## Validation

[EMPIRICAL: `code/verify_published_example.py`, 2026-06-23] The Magma V2.19.8 function-field example over $\mathbb F_{2^{155}}/\mathbb F_{2^5}$ was independently reconstructed using the documented Frobenius polynomial $(t^{31}+1)/(t^5+t^2+1)$. The implementation found annihilator $t^5+t^2+1$, conjugate rank $5$, magic number $6$, and genus $31$, matching the documented genus exactly.

[EMPIRICAL: 23 shared tests and 7 P1.4 tests, 2026-06-23] The binary-field implementation passed exhaustive inverse, square-root, trace, and selected distributivity checks at degrees $4$, $6$, and $8$; the GHS tests passed rank, annihilator, Frobenius-invariance, and published-example checks.

## Exhaustive genus census

[EMPIRICAL: all $333$ nonzero $b$ at $n\in\{4,6,8\}$] The exact genus counts are:

| $n$ | genus: count |
|---:|---|
| 4 | $1:1,\ 2:2,\ 4:4,\ 8:8$ |
| 6 | $1:1,\ 2:2,\ 3:3,\ 4:3,\ 8:6,\ 15:12,\ 16:12,\ 32:24$ |
| 8 | $1:1,\ 2:2,\ 4:4,\ 8:8,\ 16:16,\ 32:32,\ 64:64,\ 128:128$ |

[EMPIRICAL: `data/ghs_genus_distribution_n4-6-8_20260623.csv`] Degree $6$ is the first tested degree with the lower $2^{m-1}-1$ branch: $3$ parameters give genus $3$ and $12$ give genus $15$. Every degree-$4$ and degree-$8$ parameter takes the $2^{m-1}$ branch.

## Low-genus locus

For a uniform experimental slice, define $B_n=2^{n/2}$.

[EMPIRICAL: exhaustive sweep, $n\in\{4,6,8\}$] The locus $\{b\ne0:g(b)\le B_n\}$ is exactly the nonzero kernel of the displayed linearized polynomial, with the following image under $j=1/b$:

| $n$ | $B_n$ | count / density | equation in $b$ | equation in nonzero $j$ |
|---:|---:|---:|---|---|
| 4 | 4 | $7$, $7/15$ | $b^8+b^4+b^2+b=0$ | $j^7+j^6+j^4+1=0$ |
| 6 | 8 | $15$, $5/21$ | $b^{16}+b^8+b^2+b=0$ | $j^{15}+j^{14}+j^8+1=0$ |
| 8 | 16 | $31$, $31/255$ | $b^{32}+b^{16}+b^2+b=0$ | $j^{31}+j^{30}+j^{16}+1=0$ |

[PROVED] If $f(t)=\sum_{i=0}^d f_i t^i$ annihilates $b$ under Frobenius, then $L_f(b)=\sum_i f_i b^{2^i}=0$. Substituting $b=j^{-1}$ and multiplying by the nonzero quantity $j^{2^d}$ gives the displayed $j$-equation $\sum_i f_i j^{2^d-2^i}=0$; each step is reversible for $j\ne0$.

[PROVED] Each displayed $b$-locus with zero adjoined is an $\mathbb F_2$-vector space because it is the kernel of an $\mathbb F_2$-linear map.

[PROVED] Both the $b$- and $j$-loci are Frobenius-stable: $L_f(b)^2=L_f(b^2)$ for binary coefficients, and squaring commutes with inversion on nonzero field elements.

[EMPIRICAL: exhaustive sweep, $n\in\{4,6,8\}$] None of the three displayed $j$-loci becomes an additive subgroup after adjoining zero.

[EMPIRICAL: all full-degree parameters at $n\in\{4,6,8\}$] The minimum genus among parameters outside every proper subfield is respectively $4$, $8$, and $16$; the counts attaining those minima are respectively $4$, $6$, and $16$.

## Security interpretation

[PROVED] This census classifies low-genus outputs of the basic binary GHS invariant, not vulnerable elliptic curves: the data contains neither elliptic-curve subgroup orders nor Jacobian-DLP timings, so it cannot establish an advantage over Pollard rho.

[CITED] Maurer, Menezes, and Teske (2002, *LMS Journal of Computation and Mathematics*, doi:10.1112/S1461157000000723) compare GHS only after imposing subgroup-size and hyperelliptic-DLP feasibility conditions; genus alone is insufficient.

The explicit descended curve, cover map, and end-to-end toy DLP remain future work.
