# Zhandry -- random-representation versus type-safe generic groups

Mark Zhandry, “To Label, or Not To Label (in Generic Groups),” CRYPTO 2022;
IACR ePrint 2022/226.

Primary text: <https://eprint.iacr.org/2022/226.pdf>

## Relevant results

[CITED] The paper separates random-representation/Shoup and type-safe/Maurer
models at the construction level while proving equivalence of security for
single-stage games whose constructions exist in both models.  [Thms. 1.1,
1.5--1.7]

[CITED] In its query-complexity convention, labeling and group operations have
unit cost while bit computation and equality tests are free.  Thus an efficient
generic algorithm may use unbounded ordinary computation while making only
polynomially many group queries.  [§3.3]

[CITED] No efficient keyed permutation pair internal to the type-safe model is
a secure PRP under that convention.  The proof uses exponential computation
with bounded or zero generic-group queries.  [§4.2, Thm. 4.10 and Lem. 4.11]

## Audit note

[PROVED] The model definitions, cost convention, and Theorem 4.10 proof setup
were checked in the primary PDF.
