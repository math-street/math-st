---
attempt: A003
status: promising
---
# A003 - Extension fields and small characteristics

## Idea

Port the generic SvdW arithmetic to a fixed polynomial-basis extension field, test whether the same algebra survives characteristic three, and isolate characteristic two behind an independently validated map or a sharp complexity obstruction.

## Prior art

- [CITED] RFC 9380 defines extension-field `sgn0`, `hash_to_field`, and the generic SvdW straight-line structure, but explicitly limits its elliptic-curve treatment to characteristic greater than three (Faz-Hernandez et al. 2023, Sections 2.1, 4.1, 5, and F.1).
- [CITED] Brier et al. give a characteristic-three encoding for the ordinary model $y^2=x^3+a x^2+b$ and a three-candidate binary SvdW encoding for $y^2+xy=x^3+a x^2+b$ over odd-degree binary extensions (CRYPTO 2010 full version, Sections 8.1 and E; IACR ePrint 2009/340).

## Plan

1. Add a shared fixed-degree polynomial-basis finite field and exhaustive irreducibility validation.
2. Implement generic-field SvdW with a branch-using oracle and exhaust one $\mathbb F_{7^3}$ fixture.
3. Exhaust characteristic-three short-Weierstrass fixtures.
4. Search primary literature for a bounded-operation characteristic-two encoding; implement it if its prerequisites can be reconstructed and independently checked.
5. Record the exact residual obstruction before starting the compiled backend.

## Execution log

- Predictions and falsifiers are recorded in `LOG.md` before new experiments.
- [EMPIRICAL: $\mathbb F_{7^3}$, 343 inputs] Generic SvdW passed its direct candidate/root oracle and curve-membership test with one schedule.
- [EMPIRICAL: same cubic suite] All 102,400 ordered group pairs and 117,649 two-map/cofactor input pairs passed complete-law, pipeline-oracle, order-five subgroup, support, and schedule checks.
- [EMPIRICAL: $\mathbb F_3$, 3 inputs] The Section-8.1 square-discriminant map passed its direct oracle with one schedule.
- [EMPIRICAL: $\mathbb F_{2^n}$, $n=3,5,7$, 168 inputs] The binary map passed exhaustive ordinate oracles with one schedule; its largest observed fiber had size six.
- [EMPIRICAL: $\mathbb F_3$ and $\mathbb F_{2^n}$ for $n=3,5,7$] All 20,853 ordered group-law pairs and 17,481 two-map/cofactor input pairs passed complete-law, pipeline-oracle, subgroup, support, and schedule checks.
- [PROVED] A masked $x=0$ correction is necessary because the published rational expression for $g(x)$ has denominator $x^2$ while the curve has the unique point $(0,\sqrt b)$ above zero.

## Outcome

[EMPIRICAL: registered toy fields] The three field regimes now each have at least one bounded-operation map with exhaustive on-curve/oracle/schedule evidence. [PROVED] They remain distinct compile-time formulas, and no compiled complete group pipeline or universal theorem follows from these experiments.
