# Sub-goals — P3.4

- [x] SG-01: Extract the exact public inputs, numerical hypotheses, and
  construction witnesses used by Castryck–Decru, Maino–Martindale, and Robert.
- [x] SG-02: Define a protocol-independent leakage-parameter record.
- [x] SG-03: Populate and source a protocol matrix for SIDH, SIKE, CSIDH,
  SQIsign, and one verified newer higher-dimensional construction if available.
- [x] SG-04: Turn the sourced requirements into an ordered, multi-valued
  decision procedure.
- [x] SG-05: Evaluate at least five synthetic boundary cases.
- [x] SG-06: Audit necessity, false positives, and false negatives; state the
  exact scope of every verdict.
- [x] SG-07: Decide whether a scaled-down attack adds enough confidence to
  justify its implementation cost in this session.
- [x] SG-08: Replace the hand-set rank/action fields by a proved module-span
  test for multiple same-secret point-image leaks at composite torsion order.
- [ ] SG-09: Replace the surface-witness boolean by mechanically checked
  Castryck--Decru and Maino--Martindale numerical certificates.
- [ ] SG-10: Specify and test the exact common-factor peeling precondition for
  cyclic separable secret isogenies.
- [ ] SG-11: Implement a toy recovery experiment that measures ambiguity under
  full-rank, rank-one, and mixed-secret leakage without claiming to reproduce
  the higher-dimensional quotient.

Work stopped on 2026-07-03 at the user's request. SG-09 is only partially
complete (numerical identities implemented; construction verification absent),
and SG-10--SG-11 remain unresolved.
