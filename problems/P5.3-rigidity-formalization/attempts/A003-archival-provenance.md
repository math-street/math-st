---
attempt: A003
status: complete
---
# A003 — Archival provenance and non-identifiability

## Status

Completed as a source-bounded negative result.

## Question

Can a dated primary source recover a finite, precommitted candidate menu for
secp256k1 or BLS12-381, rather than merely explain the final constants or list
desirable properties?

## Search success criterion

A positive archival hit must specify enough information to reconstruct the
historical menu relevant to an audit projection: the candidate domain (or a
finite cap), enumeration order, stopping or selection rule, equivalence
convention, and evidence that these were fixed before the final choice.  A
source that merely publishes the chosen constant, derives dependent constants,
or gives post-hoc design goals is not sufficient.

## Prediction

The available primary record will support replay of the published parameters
but will not meet the success criterion for either curve.  If so, the attempt
will replace an unsupported numerical estimate by a theorem showing that the
historical selection capacity is not identifiable from the final output alone,
and by an explicit certificate format stating what additional evidence would
make it identifiable.

## Evidence log

- **[CITED]** SEC 2 version 1.0 (September 20, 2000), Section 2.1 says
  prime-field Koblitz parameters were repeatedly selected from parameters with
  efficient endomorphisms until a prime-order curve was found. Section 2.7.1
  publishes secp256k1 but supplies no domain, ordering, random-source
  transcript, rejected candidates, or generator derivation.
- **[CITED]** SEC 2 version 2.0 preserves the tuple but adds no provenance
  menu.
- **[CITED]** Bowe's March 11, 2017 construction note gives the BLS12-381
  parameter and objectives and says a future paper would explain selection
  more thoroughly.
- **[CITED]** The repository linked by that note now resolves to
  `zkcrypto/pairing`. Its reachable history begins with zero-parent commit
  `a06216f` dated July 8, 2017. The initial README states field-size bounds,
  \(u\bmod72\in\{16,64\}\), a low-Hamming-weight goal, and an optimization
  claim; it also gives a canonical G1/G2 generator rule.
- **[EMPIRICAL: all reachable refs in a 2026-07-01 clone of
  `zkcrypto/pairing`]** No earlier reachable commit, selection program, finite
  \(u\)-domain, objective priority, or rejected-candidate transcript occurs in
  that repository history.
- **[EMPIRICAL: one `web.archive.org` CDX query on 2026-07-01]** The public
  archive-index request timed out and supplied no additional artifact.

## Outcome

**[PROVED]** Neither surviving primary record meets the search success
criterion. SEC 2 v1 is stronger than a literal-only record, and the initial
BLS12-381 README is stronger than the announcement, but both remain compatible
with pre-publication histories having different menu sizes.

**[PROVED]** `DEFINITIONS.md` now proves final-output non-identifiability and
gives a sufficient provenance-certificate checklist. The A256 audit therefore
retains \(\bot\) for both unconditional capacities, while giving BLS12-381
zero residual generator freedom conditional on the surviving canonical
generator rule.

## Reopening condition

A dated pre-publication source that fixes the missing finite domain,
enumeration/objective order, and transcript would reopen the numerical audit.
Later explanations that cannot constrain the admissible historical fiber do
not change the result.
