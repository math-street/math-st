# Log — P3.4

## Session 1 — 2026-06-30

**Goal:** Build a source-traced, mechanically applicable decision procedure for
known Kani-embedding attacks, classify the validation protocols, and document
the boundary where the procedure can no longer decide.

**Prediction (written before literature extraction or experiments):** The
deliverable will be a sound sufficient-condition checklist for published attack
routes, not a necessary-and-sufficient characterization of every possible
higher-dimensional attack. I expect SIDH/SIKE to reach a positive leaf because
their transcript exposes a full basis of a large coprime torsion subgroup and
its images under a known-degree secret isogeny; I expect CSIDH and SQIsign to
reach negative leaves because their public transcripts do not expose that
evaluation oracle. The degree/torsion inequality alone will probably be
insufficient without an efficiently constructible auxiliary endomorphism or
product-isogeny witness.

**Did:**

- Initialized the required problem files and attempt record.
- Verified the three 2022 attack preprints, the SIKE and SQIsign
  specifications, the CSIDH paper, Kani's source, and SQIsign2D-West.
- Wrote `CHECKLIST.md`, including requirements, vocabulary, protocol table,
  ordered procedure, boundary cases, and a necessity audit.
- Implemented `code/leakage_checklist.py` with five protocol fixtures, eight
  boundary fixtures, and regression tests.
- Added eight paper notes under `refs/`, the global bibliography entries, the
  glossary entries, and Q011.
- Ran the new tests and the full shared `unittest` suite.

**Found:**

- [CITED] Robert's dimension-8 route gives direct recovery in the
  $N^2>d$ regime from a full rank-two smooth $N$-torsion restriction, without
  assuming a known starting endomorphism ring (Robert 2023, Theorem 1.1,
  Remark 1.2, and Section 6.4).
- [CITED] Castryck--Decru and Maino--Martindale surface routes need an explicit
  auxiliary-isogeny/smooth-cofactor witness; the SIKE starting endomorphism and
  Richelot formulas are practical conveniences for one route, not universal
  prerequisites (Castryck--Decru 2023; Maino--Martindale 2023).
- [CITED] SIDH/SIKE disclose the needed target-map restriction, whereas CSIDH
  sends no auxiliary points and current SQIsign keeps the long-term secret
  torsion action secret (SIKE specification 2022; Castryck et al. 2018;
  SQIsign specification 2.0.1, 2025).
- [CITED] SQIsign2D-West uses the same higher-dimensional machinery
  constructively to represent response isogenies, showing that use of the
  machinery is not itself a leakage criterion (Basso et al. 2024).
- [PROVED] The repository now has a sound and complete invocation test for the
  R8, K2-CD, and K2-MM templates, relative to a supplied auxiliary witness; it
  does not have a completeness theorem for every possible future attack.
- [EMPIRICAL: 13 deterministic fixtures] The classifier returns positive R8
  verdicts for SIDH/SIKE, `NO_PUBLISHED_ROUTE` for CSIDH/SQIsign, and the
  documented outcomes for eight boundary cases
  (`code/tests/test_leakage_checklist.py`, generated JSON in `data/`).

**Prediction vs. outcome:** Mostly matched. The predicted protocol separation
held. The missing witness matters to the surface attacks, but Robert's
dimension-8 construction makes the four-square auxiliary witness automatic in
the generic $N^2>d$ regime, so a known starting endomorphism ring is less
central than predicted.

**Did not work:** `pytest` was unavailable. The standard-library `unittest`
runner was a complete substitute. The first dynamic test import failed because
Python 3.13 requires the module to be registered before dataclass evaluation;
registering it in `sys.modules` fixed the harness. A toy Kani attack was not
attempted because the installed local code has no abelian-surface quotient
machinery and such an implementation would not settle the broad necessity gap.

**Changed my mind about:** The sharpest generally useful first-pass inequality
is $N^2>d$, not the original surface exposition's $N>d$. Endomorphism-ring
knowledge is a low-dimensional construction accelerator, not a condition for
the dimension-8 theorem.

**Next:** Formalize the derived-leakage closure and common-factor peeling, then
implement a toy product/Kani quotient only if it can validate a condition not
already guaranteed by the cited theorems.
