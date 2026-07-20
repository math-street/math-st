---
attempt: A022
status: folded-into-A001
---
# A022 - Principal-unit evaluation is polynomially equivalent to source DLP

## Setup

- [PROVED] Let \(r\) be an odd prime, let \(C=\langle P\rangle\) have order
  \(r\), and put
  $$
  U_r=(1+r\mathbb Z[i])/(1+r^2\mathbb Z[i]).
  $$
- [PROVED] The map
  $$
  \theta:U_r\longrightarrow(\mathbb Z[i]/r\mathbb Z[i],+),
  \qquad 1+rz\longmapsto z\bmod r
  $$
  is an efficiently computable group isomorphism, because the cross term in
  \((1+rx)(1+ry)\) vanishes modulo \(r^2\).

## Reduction from an evaluator to ECDLP

- [PROVED] Suppose \(\psi:C\to U_r\) is a nonzero homomorphism and its
  evaluator is available.  Write
  \(u=\theta(\psi(P))=(u_1,u_2)\in\mathbb F_r^2\).  Nonzeroness gives a
  coordinate \(j\) with \(u_j\ne0\).
- [PROVED] For an input \(Q=xP\), homomorphism and linearization give
  $$
  \theta(\psi(Q))=x u.
  $$
  Hence
  $$
  x=\theta(\psi(Q))_j/u_j\pmod r.
  $$
  One evaluator call, coefficient extraction, and one field inversion recover
  the source discrete logarithm.
- [PROVED] Conversely, a source-DLP oracle evaluates every fixed
  \(\psi\): recover \(x\) and exponentiate \(\psi(P)^x\) in \(U_r\).
- [PROVED] Therefore evaluation and source DLP are polynomial-time Turing
  equivalent; more explicitly, each cost is at most the other plus
  \((\log r)^{O(1)}\).

## Outcome

- [PROVED] The modulus-\(r^2\) Gaussian principal-unit target is not merely a
  class group with an easy target DLP.  Any nonzero point evaluator itself is
  already a polynomial-time source-DLP algorithm because the target logarithm
  is transparent in the ordinary encoding.
- [PROVED] This closes the ray target as a distinct intermediate-complexity
  route: it remains logically possible only together with a polynomial-time
  solution of the source ECDLP.
- [PROVED] The result does not exclude ordinary class-group targets whose DLP
  is subexponential rather than polynomial, and it is not an unconditional
  lower bound on concrete-coordinate ECDLP.

## What transfers

- [PROVED] A proposed easy-DLP target should be audited for an explicit
  logarithm before evaluator engineering.  If the target log is polynomial,
  a polynomial evaluator is already a polynomial source-DLP solution, not a
  partial reduction.
