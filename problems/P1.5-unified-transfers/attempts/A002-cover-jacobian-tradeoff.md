---
attempt: A002
status: promising
---
# A002 - Cover pullback versus high-genus DLP cost

## Idea

Use pullback along a cover $C\to E$ of degree coprime to $r$ to inject the
source subgroup into $J_C$, then choose a curve family with a subexponential
Jacobian DLP algorithm.

## Prior art

- [CITED] Gaudry--Hess--Smart (2002) implements the related Weil-descent route.
- [CONDITIONAL: the family hypotheses and smoothness assumptions]
  Enge--Gaudry--Thome (2009) gives an $L(1/3)$ target algorithm for selected
  high-genus low-degree curves.

## Plan

1. Parameterize cover degree, genus, field size, and kernel intersection.
2. Prove the source subgroup remains injective by norm after pullback.
3. Check the exact target-family hypotheses rather than assuming that high
   genus alone makes the DLP subexponential.

## Execution log

- [PROVED] Norm composed with pullback is multiplication by the cover degree,
  so degrees coprime to $r$ certify subgroup injectivity.
- [PROVED] Indeed, for every divisor $D$ on $E$, pushforward of the pulled-back
  divisor satisfies $\pi_*\pi^*D=dD$ and hence the same identity holds on
  degree-zero divisor classes. If an order-$r$ class $x$ lies in the pullback
  kernel, then $dx=0$; Bezout applied to $\gcd(d,r)=1$ gives $x=0$.

## Outcome

- [CITED] This is promising as a geometric transfer framework, but the checked
  construction belongs to known descent/correspondence methods rather than a
  new independent target family.
