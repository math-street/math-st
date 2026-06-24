# Log

## Session 1 — 2026-06-22

**Goal:** Complete SG-01 and the opacity audit in SG-02; if possible, give a formal case-(b) expressibility result for the literal free-coordinate model.

**Prediction (written before implementation or toy experiments):** The operation matrix will show that coordinate access is not a single primitive, and the literal model with uncharged field arithmetic will fail even before index calculus because affine addition formulas emulate the charged group oracle.

**Did:**

- Initialized the problem state and attempt structure.
- Read Shoup's original paper by rendering the PDF and reconstructed Theorem 1
  in repository notation.
- Built the SG-01 operation matrix with per-cell justifications from primary
  sources.
- Added shared known-answer implementations of BSGS, Pollard rho, and
  Pohlig–Hellman, retaining concurrent shared-library additions.
- Defined $\mathsf{CCA}_0$, compiled affine addition into its free fragment,
  and expressed Semaev/Gaudry/Diem relation collection in the model.
- Ran the complete shared library test suite and two P1.1 smoke experiments.

**Found:**

- [PROVED] Free field arithmetic plus free packing of valid coordinates
  implements the charged curve addition instruction, so BSGS has zero charged
  cost in the literal model (`MODEL.md`).
- [PROVED] Shoup's opacity assumption enters when the simulator assigns an
  independent random label to each new affine-linear formal expression; visible
  coordinates invalidate that simulation before any group-element collision.
- [PROVED] The Semaev/Gaudry/Diem relation loop is expressible with zero charged
  group operations in $\mathsf{CCA}_0$.
- [EMPIRICAL: p=17, one known-answer ECDLP] Charged and coordinate-compiled
  BSGS both recovered $k=7$; their recorded charged group counts were 17 and 0.
- [EMPIRICAL: p=17, one known-answer decomposition] An exhaustive $f_3$ search
  over five factor-base $x$-values recovered two ordered decompositions of
  $[7](5,1)$ after direct sign lifting and group-law verification.

**Prediction vs. outcome:** Matched. The literal model fails at the addition
formula, earlier than any sophisticated non-generic attack.

**Did not work:** Treating “group operation” as an instruction name does not
survive an equivalent coordinate-formula spelling.

**Changed my mind about:** The first model boundary to study is not which
coordinate predicate an attack reads, but whether derived coordinates may flow
back into point registers.

**Next:** Define a read-only-coordinate model with an explicit information-flow
rule and rerun every SG-01 row against it.

## Session 2 — 2026-06-24

**Goal:** Exhaust SG-04/05 by formalizing read-only coordinate access, deciding
which known attacks it admits, and completing the remaining toy primitive
traces before writing `REVIEW.md`.

**Prediction (written before new experiments):** Preventing field-to-point
repacking will restore a syntactic group-operation charge, but the restriction
will exclude every attack whose coordinate computation constructs an auxiliary
point, lifted point, or target-group element. If read-only access still permits
arbitrary predicates of input coordinates, Shoup's random-label coupling will
remain unavailable even though no known attack survives intact.

**Did:**

- Defined the typed read-only machine $\mathsf{ROCCA}_0$ and proved the
  virtual-point compiler and canonical-representation no-go theorem.
- Closed A002 with a post-mortem identifying unrestricted composition, rather
  than `PACK`, as the killer primitive.
- Implemented and recorded fixed Smart, MOV, prime-field $f_3$, and
  extension-field $f_3$ traces, with one known-answer test per observation
  script.
- Replaced the Pohlig–Hellman smoke test on a prime-order group by a cyclic
  order-12 fixture that exercises the $2^2$ and $3$ components.
- Audited the independent GHS genus-profile implementation and recorded A003
  when it proved insufficient for an end-to-end source-to-Jacobian transfer.
- Ran the complete shared library suite and the P1.1 observation suite.

**Found:**

- [PROVED] Removing field-to-point packing does not restore a nonzero query
  bound: virtual point tuples can be iterated and compared with the target
  without ever creating a point handle.
- [PROVED] Any explicit group representation whose law and equality lie in the
  free local language has zero charged-oracle DLP complexity, by exhaustive
  virtual iteration.
- [EMPIRICAL: p=17, anomalous order 17] The Smart fixture recovered secret 7
  using two lifts modulo $p^2$, 12 lifted group steps, and one formal ratio.
- [EMPIRICAL: p=43, subgroup order 11] The MOV fixture reproduced reduced Tate
  values $11+3t$ and $26+23t$, then recovered secret 2 in the multiplicative
  target subgroup.
- [EMPIRICAL: q=5, extension degree 3] The extension-field fixture expanded
  $f_3$ into three base-field coefficients and found one verified relation
  after 25 base-coordinate pair evaluations.
- [PROVED] The current GHS structural fixture does not validate the transfer
  map, target divisor arithmetic, or target DLP because none of those objects
  is constructed.

**Prediction vs. outcome:** Diverged. The prediction expected removal of
`PACK` to restore at least a syntactic charge, but a DLP solver needs only a
scalar output and can keep every derived point virtual.

**Did not work:** A read-only taint boundary failed because it constrained
point handles without constraining the free coordinate program. The proposed
end-to-end GHS validation also stopped at the missing descended-function-field
and Jacobian machinery; an exhaustive transfer table would have been circular.

**Changed my mind about:** The decisive boundary is closure of the free
coordinate language under iterated group-law formulas, not feedback from field
registers into a charged group oracle.

**Next:** Treat the pure group-operation-only model question as exhausted. Any
new lower-bound attempt must explicitly charge or bound coordinate circuits;
an independent validation project may close Q002/Q003 with a genuine GHS
Jacobian transfer.
