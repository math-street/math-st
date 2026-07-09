# Salizzoni (2023) - solving degree from degree of regularity

**Source:** Flavio Salizzoni, "An upper bound for the solving degree in terms
of the degree of regularity," arXiv:2304.13485v1, 2023.

**Checked:** 2026-07-09 against the arXiv HTML and TeX source.

[CITED] Definition 2.5 uses the same closed spaces $V_{F,d}$ and the same
Groebner-basis containment definition of mutant solving degree used by the
local exact implementation.

[CITED] Theorem 1.1 proves
$\operatorname{sd}_\sigma(F)\le d_{\mathrm{reg}}(F)+1$ when the maximum
input degree is at most $d_{\mathrm{reg}}(F)$ and the order is
degree-compatible.

[CITED] Proposition 3.10 gives the unconditional form

\[
\operatorname{sd}_\sigma(F)\le
\max\{d_{\mathrm{reg}}(F)+1,\max_{f\in F}\deg f\}.
\]

[CITED] This proposition is the final input to the quadratic mutant-family
upper bound: that family has degree of regularity at most 4 and maximum input
degree at most 4, hence solving degree at most 5.

**URL:** <https://arxiv.org/abs/2304.13485>
