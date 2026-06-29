---
attempt: A001
status: promising
---
# A001 — Test whether coordinate formulas bypass the charged group oracle

## Idea

Give the proposed model a literal syntax with zero-cost field arithmetic and a
charged group-addition instruction. Check whether the affine addition formulas
can be expressed entirely with the zero-cost instructions.

## Prior art

The generic group model avoids this issue by exposing opaque encodings rather
than coordinates. The present attempt is a model audit, not a claimed ECDLP
lower bound.

## Plan

1. Write syntax and semantics for a straight-line coordinate machine.
2. Express elliptic-curve addition using only field instructions.
3. Compile BSGS into the zero-cost fragment.
4. Distinguish syntactic charging from an extensional rule that charges any
   computation equal to the group law.

## Execution log

- Defined the literal machine in `MODEL.md`.
- Replaced every charged point addition by the affine chord-and-tangent
  formulas in the free field fragment.
- Compiled BSGS through that replacement and checked a known order-19 ECDLP.
- Expressed the Semaev/Gaudry/Diem decomposition loop in the same syntax and
  checked an $f_3$ relation at toy scale.

## Outcome

[PROVED] The literal candidate is vacuous: every group addition, hence every
group algorithm, compiles to zero charged operations. The same compiler makes
the index-calculus relation loop a zero-charged-operation program.

[EMPIRICAL: p=17, two known-answer fixtures] `observe_coordinate_bypass.py`
recovers the logarithm with zero charged group operations, and
`observe_semaev_decomposition.py` recovers and verifies an $f_3$
factor-base decomposition.

## Post-mortem

**Why it failed:** The cost is attached to the spelling `ECADD`, while the
explicit coordinate representation exposes an uncharged spelling of the same
rational map.

**What transfers:** Free repacking is a sufficient bypass, but A002 shows it is
not necessary. Any repaired model must constrain composition of coordinate
formulas themselves, not only their flow back into point registers.

**Would it work under different assumptions?** Charging or bounding field
computation avoids the compiler but changes the resource being bounded.
