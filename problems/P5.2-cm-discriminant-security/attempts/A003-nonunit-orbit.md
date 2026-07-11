---
attempt: A003
status: promising
---
# A003 - Non-unit $D=-7$ orbit

## Idea

Use GLV's norm-two CM endomorphism for discriminant $-7$. On a prime-order
invariant subgroup, measure the multiplicative order of its scalar eigenvalue
and compare the ideal quotient benefit with the cost of canonicalizing by
explicit orbit enumeration.

## Prior art

- [CITED] Gallant, Lambert, and Vanstone (CRYPTO 2001, LNCS 2139) give an explicit discriminant-$-7$ endomorphism whose computation is slightly more expensive than point doubling.
- [CITED] The same paper proves that an endomorphism acts as a quadratic-polynomial root modulo an invariant prime subgroup order.

## Plan

1. Reconstruct and test the rational map on the published model.
2. Transform the model to the shared short-Weierstrass representation or add a narrowly scoped compatible representation.
3. Independently count each curve and validate $\phi^2-\phi+[2]=0$ on seeded points.
4. Recover the subgroup scalar and compute its exact multiplicative order.
5. Prove the enumeration cost in a stated oracle/comparison model.

## Execution log

- Recorded before implementation and measurement.
- [PROVED] The first test command failed before test discovery because `unittest` interpreted the `P5.2` directory component as Python dotted-module syntax and raised `ModuleNotFoundError: No module named 'problems.P5'`. No mathematical test executed in that failed invocation.
- [CITED] The implemented map is GLV Example 5 with $\omega=(1+\sqrt{-7})/2$, translated from $y^2=x^3-3x^2/4-2x-1$ by $x_{\rm old}=x+1/4$ to $y^2=x^3-35x/16-49/32$.
- [EMPIRICAL: five curves, p=977..262007] Exhaustive and independent Hasse-interval/BSGS point counts agreed, and 32 seeded characteristic-equation checks passed on every curve.
- [EMPIRICAL: known DLP k=17 in the r=29 fixture] Collision-table orbit rho recovered the exact logarithm using the non-unit map.
- [PROVED] A diagnostic using secret 37 on the order-29 fixture returned 8 because $37\equiv8\pmod {29}$; treating that canonical residue as a wrong answer was a test-design failure, not an algorithm failure.

## Outcome

- [EMPIRICAL: r=233,991,4057,16139,32831] The exact eigenvalue orders were $116,495,1352,8069,16415$; the corresponding nonzero orbit quotients contained only $2,2,3,2,2$ orbits.
- [EMPIRICAL: 80 normalizations] Exhaustive least-coordinate normalization used exactly $m-1$ endomorphism evaluations in every sample; the ratio $(m-1)/\sqrt m$ grew from $10.68$ to $128.11$ over the measured range.
- [PROVED] In the sequential-successor/comparison model, any always-correct algorithm for the least label of an opaque length-$m$ cycle needs at least $m-1$ successor queries in the worst case; exhaustive enumeration is therefore optimal in that model.
- [PROVED] An exponent-returning canonicalizer for the $\langle\lambda\rangle$ action reduces ECDLP to one query plus one precomputed query for each of the $(r-1)/m$ nonzero orbits. Thus a polylogarithmic canonicalizer with a polylogarithmic quotient would itself be an ECDLP algorithm, not free preprocessing for rho.
- [PROVED] These results close SG-07b only in the explicitly stated evaluator model and for exponent-returning normalization; they do not prove an asymptotic order theorem or settle the formal P5.2 reduction/algorithm problem.
