# Lenstra 2017 — General purpose integer factoring

## Source

[CITED] Arjen K. Lenstra, “General purpose integer factoring,” Chapter 5 in
*Topics in Computational Number Theory Inspired by Peter L. Montgomery*,
Cambridge University Press; IACR ePrint 2017/1087.
<https://eprint.iacr.org/2017/1087.pdf>

## Result used here

[CITED] Section 5.2.2 defines
$$
L_x[r,\psi]
=\exp\!\left((\psi+o(1))(\log x)^r(\log\log x)^{1-r}\right)
$$
for fixed parameters, with natural logarithms, and calls the range
$0<r<1$ subexponential in $\log x$.

## Consequence in repository notation

[PROVED] For fixed $c>0$,
$L_p[1/2,c]=\exp((c+o(1))\sqrt{\log p\log\log p})=p^{o(1)}$ because
$\sqrt{\log p\log\log p}/\log p\to0$.

## What it rules out and leaves open

[PROVED] Together with the elementary support bound in `CLAIM.md`, this
standard interpretation rules out a fixed number of summands from a factor
base of the stated size. It does not rule out a factor base of size
$p^{1/m-o(1)}$, a growing summand count, or a nonstandard use of
“$L_p(1/2)$” to mean $\sqrt p$.

No computation from the source was reproduced; only the displayed definition
was checked against the accessible text.
