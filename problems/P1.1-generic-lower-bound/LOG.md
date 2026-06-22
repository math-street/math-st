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
