# Notes — P3.4

## Stable facts

[CITED] Castryck--Decru's surface route needs a computable auxiliary isogeny in
addition to known degree and a full leaked torsion action; the special SIKE
endomorphism and 2-power/Richelot setting make that witness practical
(Castryck--Decru 2023, Sections 4--5).

[CITED] Maino--Martindale replace the special-starting-curve assumption by a
smooth-cofactor search and bounded parameter guesses, but still consume the
full SSI-T restriction (Maino--Martindale 2023, SSI-T definition and
Algorithm 1).

[CITED] Robert's dimension-8 route evaluates a degree-$d$ secret map from its
full rank-two $N$-torsion action without a known starting endomorphism ring;
direct recovery covers $N^2>d$ when the remaining torsion, factorization,
smoothness, and kernel-recovery hypotheses hold (Robert 2023, Theorem 1.1,
Remark 1.2, and Section 6.4).

[PROVED] The broad formal problem remains open here: `CHECKLIST.md` proves an
invocation criterion only for R8, K2-CD, and K2-MM, not a universal
necessary-and-sufficient characterization of all future higher-dimensional
attacks.

**Proof.** The scope theorem in `CHECKLIST.md` quantifies over exactly those
three templates, and Q011 records the missing completeness theorem.

[CITED] SIDH/SIKE provide known smooth degrees and a full opposite-torsion
restriction, so they pass R8; CSIDH sends no auxiliary points, while SQIsign
keeps the long-term secret torsion images in the secret key (SIKE specification
2022; Castryck et al. 2018; SQIsign specification 2.0.1, 2025).

[CITED] SQIsign2D-West is a constructive negative control: it publishes an
efficient representation of a response isogeny using higher-dimensional
machinery, but not the restriction of the distinct long-term secret map
(Basso et al. 2024, Sections 2 and 4).

## Working analysis

[PROVED] The executable classifier uses six verdicts so that algebraic
embeddability, polynomial key recovery, a missing auxiliary witness, and absence
of a route in the encoded literature cannot be conflated.

**Proof.** The `Verdict` enumeration and the mutually exclusive branches in
`code/leakage_checklist.py` represent these cases separately; the regression
fixtures exercise all verdicts except `INSUFFICIENT_PROFILE` and the positive
surface-witness leaf.

[PROVED] The optional toy attack was declined because the available local
arithmetic stops at one-dimensional Vélu maps and would not validate the
higher-dimensional step on which the criterion depends.

**Proof.** `lib/isogeny.py` exposes reduced forms, Vélu maps, rational isogeny
steps, and orbit utilities; it exposes no product-polarization or
abelian-surface quotient routine.
