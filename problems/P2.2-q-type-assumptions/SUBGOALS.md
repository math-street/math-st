# Sub-goals — P2.2

- [PROVED] **SG-01 (complete):** Fixed typed notation for $q$-SDH, DHI/DDHI,
  BDHI/DBDHI, weak BDHI variants, DHE/DDHE, gap-BDHE, and $q$-aBDH; near-name
  variants are not identified without tuple equality.
- [PROVED] **SG-02 (complete):** Drew a hardness-implication graph and recorded the
  breaker transformation, oracle-call count, success/advantage preservation,
  and overhead for every edge.
- [PROVED] **SG-03 (complete):** Catalogued DDH, XDH/SXDH, DLIN, co-CDH, and DBDH and
  separated source-group, cross-source, and target-group consequences.
- [PROVED] **SG-04 (complete):** A001 proves that a direct straight-line algebraic SXDH
  embedding fails already at the $x^2$ ladder element.
- [CITED] **SG-05 (complete):** A002 instantiates the Lu–Zhandry GR-BB meta-reduction
  for $q$-SDH, with thresholds $n<q-1$ in one group and
  $\binom{n+2}{2}<q$ in a bilinear group.  [Lu–Zhandry 2024]
- [PROVED] **SG-06 (complete):** Isolated the fixed-dimensional prime-order exponent
  span as the common obstruction and recorded the unrestricted
  representation-dependent/non-black-box gap as Q003.
- [PROVED] **SG-07 (complete):** A003 formalizes UR-FBB and proves that it
  implies GR-BB; therefore the published $q$-SDH separation rules it out at the
  same thresholds.
- [PROVED] **SG-08 (complete):** A004 attempts random relabeling for one fixed
  representation and fails at the representation quantifier; native encoding
  operations also destroy the fixed-span trace invariant.
- [PROVED] **SG-09 (complete):** A005 proves that a finitely seeded,
  efficiently computable sparse encoding cannot replace the information-
  theoretic random injection for the full possibly inefficient adversary
  class; doing so requires a computational or query-bounded restriction.
- [PROVED] **SG-10 (complete):** A005 separates the finite-seed distinguisher
  obstruction from the independent fact that breaking an artificial encoding
  does not refute hardness asserted only for a named group family.
- [PROVED] **SG-11 (complete):** A006 extends the trace meta-reduction to a
  named concrete representation when the reduction introduces at most $s$
  unexplained source labels: typed $q$-SDH has threshold $n_1+s_1<q-1$ even
  with pairings, while broader target-valued bilinear $q$-type games safely use
  $\binom{n+s+2}{2}+t<q$.
- [PROVED] **SG-12 (complete):** A007 proves that structured-GGM density
  $\delta$ does not automatically bound A006 freshness: the former controls a
  random-hybrid probability while the latter counts adaptively selected native
  labels.  A transfer needs an additional label budget or rank invariant.
