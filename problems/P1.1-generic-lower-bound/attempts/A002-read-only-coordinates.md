---
attempt: A002
status: dead
---
# A002 — Read coordinates without reifying derived points

## Idea

Separate point handles from field values. A point handle may be created only by
the input interface or the charged group oracle. Coordinates may be projected
from a handle and processed freely, but no instruction converts a derived pair
of field values back into a point handle.

## Prior art

Maurer's hidden-state operations-and-relations framework permits this interface
to be stated precisely. It is stronger than the equality-only generic group
model because arbitrary coordinate predicates are visible, but weaker than the
literal coordinate machine because coordinate-derived values cannot feed the
group oracle as new points.

## Plan

1. Give typed syntax, semantics, and a noninterference invariant.
2. Classify every SG-01 algorithm by whether it creates a point outside the
   charged closure of the inputs.
3. Test the classification with primitive-trace toy implementations.
4. Attempt a lower-bound coupling or isolate the exact predicate obstruction.

## Execution log

- Proved the linear-combination invariant for point handles.
- Removed `PACK` and attempted to preserve a charged point-handle boundary.
- Constructed a zero-query algorithm that stores virtual points as ordinary
  field tuples and iterates the addition formulas without point handles.
- Generalized the counterexample to any canonical group representation whose
  group law is available in the free local language.

## Outcome

[PROVED] The read-only model is still vacuous. ECDLP needs a scalar output, so
the algorithm never has to reify a derived tuple as a point handle: it can
iterate virtual coordinates, compare with $Q$, and output the matching index.

## Post-mortem

**Why it failed:** Removing field-to-point feedback constrains only oracle data
flow. It does not constrain the free field computation that already implements
the group law and the final scalar test.

**What transfers:** The killer primitive is unrestricted composition of free
coordinate arithmetic, not `PACK` specifically.

**Would it work under different assumptions?** Only after bounding or charging
coordinate circuits, restricting their degree, or forbidding the addition
formulas; each option changes the requested model.
