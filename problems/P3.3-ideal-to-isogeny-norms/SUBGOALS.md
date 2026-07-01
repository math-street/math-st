# Sub-goals

- **SG-01 (done, Session 1):** Implement and validate the maximal order
  $\mathbb Z[1,i,(1+j)/2,(i+ij)/2]\subset(-1,-p)$ for primes
  $p\equiv3\pmod4$, including reduced norms and left-ideal closure.
- **SG-02 (corrected, Session 2):** Generate at least 100 seeded near-$p$ prime-norm left ideals and record the
  shortest equivalent-ideal norm and $\log_p N(J)$ against $\sqrt p$.
- **SG-03 (done, Session 1):** Certify exact shortest vectors by exhaustive finite enumeration at
  small $p$, with the coefficient bounds recorded.
- **SG-04 (done at toy scale, Session 2):** Group results by bit band, $p\bmod8$, input norm, and input-norm
  congruence; report effect sizes without treating the sampler as uniform in
  the ideal class group.
- **SG-05 (done at toy scale, Session 2):** Apply exact norm-aware LLL and measure its approximation factor,
  then exactly measure power-of-2, power-of-3, and 5-smooth shape penalties.
- **SG-06 (done for 12/20/28 bits, Session 2):** Measure runtime over at least three separated bit-size bands before
  making any scaling claim.
- **SG-07 (done for Session 2 ranges):** Give a structural-versus-algorithmic verdict restricted to the
  experiment and separate it from any claim about KLPT.
- **SG-08 (done for 12/20/28 bits, Session 2 continuation):** Implement a target-specific solver for
  $q_I(x)=2^e$ and $q_I(x)=3^e$ that avoids enumerating all norms below the
  target, then extend the exact shape comparison beyond eight-bit $p$.
- **SG-09 (next):** Implement a validated basic KLPT path on the same seeded
  ideals and compare its output norm and runtime with the exact A004 shaped
  optima, without promoting the toy sampler to a class-group distribution.
