---
attempt: A003
status: successful-partial
---
# A003 — Transfer Satoh MI to the fixed-base FAPI-1 Miller orientation

## Normalization identity

[PROVED] On \(E:y^2=x^3+x\), let \(\psi(x,y)=(-x,iy)\) with \(i^2=-1\), and use the local parameter \(\tau=x/y\) at infinity. Then \(\tau\circ\psi=i\tau\). The affine Miller implementation normalizes every line quotient to leading coefficient one in \(\tau\); for an order-\(r\) point its final function has leading term \(\tau^{-r}\).

[PROVED] The functions \(f_{r,P}\circ\psi\) and \(f_{r,\psi^{-1}P}\) have the same divisor. Comparing leading terms at infinity gives
\[
f_{r,P}(\psi(R))=i^{-r}f_{r,\psi^{-1}P}(R).
\]
Thus a raw FAPI-1 Miller target \(v\) transfers to Satoh's orientation as \(i^rv\).

## Algorithm and scope

[PROVED] Satoh's degree-two algorithm computes
\[
u=\left(v^{(q+1)/d}\right)^{(q+1)/2},
\]
rejects unless \(u\in\mathbb F_q\), and tests the at most four base-field points above \(x(A)\pm u\). The repository implementation supports \(\ell\mid d\mid q+1\), including a Miller chain that passes through the identity.

[PROVED] Combining the normalization identity with Satoh's cited theorem yields polynomial-time raw Miller inversion for the fixed-base FAPI-1 orientation on this supersingular degree-two family.

[PROVED] This does not solve reduced FAPI-1: from \(z=v^{(q^2-1)/r}\), the algorithm still needs the unique raw representative \(v\) compatible with the cyclic Miller image.

## Validation

[EMPIRICAL: Satoh Example 4.4] The implementation reproduces \(u=131\), x-candidates \(59,75\), and solution \((59,-54)\) for \(p=139,\ell=35,d=140\), including the published raw target \(25\theta+109\).

[EMPIRICAL: six curves, all 82 nonidentity raw targets] The pullback identity and inverse both passed exhaustively for \(p\in\{43,59,83,103,131,163\}\); at most four candidate points were tested per inverse.

[EMPIRICAL: same 82 reduced targets] The canonical final-exponentiation root lying in \(\mu_r\) was compatible with the Miller image in 0 cases, so the new MI algorithm does not remove the recorded final-fibre selection obstruction.
