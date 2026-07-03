# Robert 2023

Damien Robert, "Breaking SIDH in Polynomial Time," EUROCRYPT 2023, Part V;
IACR ePrint 2022/1038, revision dated 2024-10-07.

## Main result in repository notation

[CITED] For factored coprime $N>d$, a basis of rational $E_0[N]$, its images
under the degree-$d$ secret isogeny, and a four-square decomposition of $N-d$,
Theorem 1.1 evaluates the secret map via an explicit dimension-8 isogeny.

[CITED] If the target kernel torsion is accessible, `ComputeKernel` recovers a
kernel generator; Section 6.4 yields direct reconstruction in the broader
$N^2>d$ range.

## Assumptions and costs

[CITED] The four-square decomposition is a randomized polynomial-time
parameter-only precomputation (Remark 1.2).

[CITED] The arithmetic cost depends polynomially on the largest prime factor of
$N$; a polynomial-time-in-input-size verdict therefore requires sufficiently
smooth $N$ (Theorem 1.1).

[CITED] The starting curve need not have a known endomorphism ring (Theorem 1.1
and Remark 1.2).

## What it rules out and leaves open

[CITED] The theorem breaks all standard SIDH parameter orientations because at
least one party exposes the needed smooth full torsion action (Remark 1.2).

[CITED] Section 7 asks how the recovery toolbox can be used constructively; it
does not prove a necessary condition for all future attacks.

## Verification status

[CITED] The theorem, complexity, Section 6.4, and Section 7 statements were
checked. No dimension-8 computation was reproduced in this repository.

