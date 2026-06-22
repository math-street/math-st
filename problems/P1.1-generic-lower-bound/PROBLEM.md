# P1.1 — Lower bounds for ECDLP beyond the generic group model

## Formal statement

The setting is the elliptic-curve discrete logarithm problem on an ordinary
elliptic curve $E/\mathbb F_p$ for which $\#E(\mathbb F_p)$ is prime.

Define a computational model $\mathcal M$ that gives algorithms access to
coordinate arithmetic, including field operations and polynomial manipulation
in $x$ and $y$, while charging only for elliptic-curve group operations. Then
either:

1. prove an $\Omega(p^{1/2-o(1)})$ lower bound for ECDLP in $\mathcal M$; or
2. give an explicit expressibility argument showing that a known attack, such
   as an index-calculus-style attack, is available in $\mathcal M$ and hence
   that the model is vacuous as a security argument.

The first sub-goal is an operation-requirement taxonomy covering BSGS, Pollard
rho, Pohlig–Hellman, anomalous-curve lifting, MOV/Frey–Rück, GHS/Weil descent,
and Gaudry/Diem decomposition attacks.

