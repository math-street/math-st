---
attempt: A021
status: folded-into-A001
---
# A021 - Audit uniform succinct exact-order class constructions

## Question

- [PROVED] The ordinary-class-group target subproblem asks for a uniform
  algorithm which, on prime \(r\), outputs a polynomial-bit discriminant and
  an ideal class certified to have exact order \(r\), preferably inside the
  SG-25 target window.
- [PROVED] This target-only task is distinct from the point evaluator and is
  not necessary for the already succinct modulus-\(r^2\) ray target in A004.

## Checked constructions

- [PROVED] A019 gives the class explicitly for
  \(\Delta=1-4\cdot2^r\), but the discriminant has \(\Theta(r)\) bits.
- [CITED] Lim (2016) proves exact order \(n\) in infinitely many imaginary
  quadratic class groups using congruence choices and equations containing
  an \(n\)-th power such as \(a^2-4b^n=c^2d\).
- [CITED] Ouyang--Song (2024) proves \(n\)-divisibility for squarefree parts
  of \(x^2-y^n\) once \(y\) exceeds a constant depending on fixed \((x,n)\);
  the threshold used in the proof is ineffective.
- [CITED] Chakraborty--Hoque (2020) likewise gives infinitely many fields of
  shape \(\mathbb Q(\sqrt{x^2-2y^n})\) with an element of order \(n\).
- [EMPIRICAL: bounded primary-source search on 2026-07-10] Searches for least
  discriminants, effective bounds, and explicit imaginary-quadratic classes
  of prescribed order found existence and fixed-\(n\) families, but no
  theorem giving a discriminant of \((\log n)^{O(1)}\) bits with a uniform
  polynomial-time exact-order certificate.

## Separation exposed by the toy census

- [EMPIRICAL: exhaustive $|\Delta|\le200000$, primes $3\le r\le43$] A020
  found least qualifying discriminants with \(h(\Delta)=r\) and
  \(0.684711\le|\Delta|/r^2\le2.555556\) over the tested range.
- [PROVED] Those discriminants have only \(2\log_2r+O(1)\) bits, so they fit
  the lower edge of SG-25 at toy scale.
- [PROVED] The method that found them exhausts discriminants and class
  numbers; it is not a polynomial-time uniform construction in \(\log r\).

## Outcome

- [EMPIRICAL: bounded primary-source search on 2026-07-10] No checked result
  closes the uniform succinct ordinary-class target construction.
- [PROVED] This is not a lower bound or a nonexistence theorem.  It narrows the
  target task to an effective prescribed-order problem and prevents the
  finite A020 census from being mistaken for an infinite transfer family.
- [PROVED] Even a positive solution would not close A001: A015 still requires
  the independent cross-characteristic point-to-class evaluator.
