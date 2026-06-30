# P3.4 — A decision criterion for torsion-point leakage

## Formal statement

**Setting.** An isogeny-based protocol reveals, alongside its curves, auxiliary
information $\mathcal I$, typically including images of torsion points under a
secret isogeny.

**Find.** Necessary and sufficient conditions on $\mathcal I$ for a
Kani-embedding or higher-dimensional isogeny attack to apply.

**Realistic target.** Produce a mechanically applicable checklist whose inputs
are protocol-level leakage parameters and whose outputs distinguish:

- a published attack theorem that applies;
- a published attack strategy whose remaining hypotheses require a
  protocol-specific witness;
- no known Kani-embedding route from the public transcript.

The checklist must classify SIDH and SIKE as vulnerable and CSIDH as not
vulnerable by this attack family. It must trace each condition to a published
attack requirement, stress-test boundary cases, and avoid presenting a merely
sufficient condition as necessary.

## Requested deliverables

1. A precise requirement analysis separating required inputs from conveniences.
2. A leakage-parameter vocabulary.
3. A protocol comparison table covering SIDH, SIKE, CSIDH, and SQIsign, plus any
   relevant newer protocol whose sources can be verified.
4. An ordered decision procedure with a verdict at every leaf.
5. Boundary stress-tests with verdicts and justifications.
6. An explicit decision whether to implement a toy attack.

