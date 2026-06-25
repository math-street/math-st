# Muzereau--Smart--Vercauteren 2004

[CITED] Antoine Muzereau, Nigel P. Smart, and Frederik Vercauteren, "The
Equivalence Between the DHP and DLP for Elliptic Curves Used in Practical
Applications," *LMS Journal of Computation and Mathematics* 7, 50--72,
2004, DOI 10.1112/S1461157000001042.

Primary text checked at:
<https://doi.org/10.1112/S1461157000001042>

## Result in P2.1 notation

[CITED] Theorem 2 bounds Maurer's reduction in terms of the largest factors of
the auxiliary order and makes the reduction polynomial when that smoothness
bound is polynomial in the input bit length.

[CITED] Section 5 compares random curve sampling with CM construction and
uses the norm equation

$$
  4r=t^2-Dv^2,
$$

where the paper writes the positive absolute discriminant in the equivalent
form $4r=t^2+Dv^2$.

[CITED] The same section identifies the practical CM search target precisely:
find a sufficiently small discriminant for which one of $r+1\pm t$ is smooth;
large discriminants make the class polynomial expensive.

## Assumptions and limits

[CITED] The paper treats polylogarithmic smoothness in every Hasse interval as
an assumption and obtains a non-uniform reduction from supplied curve data,
not a uniform construction for every prime.

[EMPIRICAL: standardized curves studied in the paper] Its appendix supplies
individual CM witnesses for particular standardized parameters; this is
finite-instance evidence and not an asymptotic coverage theorem.

## Verification performed

[EMPIRICAL: primary PDF pp. 50--72 inspected 2026-06-25] Theorem 2, Sections
5--6, and the CM witness tables were checked in the publisher PDF.
