# Magma V2.19.8 Weil-descent example

Computational Algebra Group, Magma V2.19.8 online handbook, “Weil Descent,” example H42E45.

## Example used here

[CITED] The handbook constructs $b=((t^{31}+1)/(t^5+t^2+1))(\sigma)(w)$ in $\mathbb F_{2^{155}}$, where $\sigma(x)=x^{2^5}$, and reports that the descended characteristic-two function field has genus $31$ over $\mathbb F_{2^5}$.

## Verification status

[EMPIRICAL: `code/verify_published_example.py`, 2026-06-23] The Frobenius-span implementation reproduced annihilator $t^5+t^2+1$ and genus $31$ using an independently selected irreducible degree-155 modulus.
