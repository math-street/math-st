---
attempt: A004
status: promising
---
# A004 — Close the GHS executable gap in the genus-one specialization

## Idea

Specialize the odd-degree basic GHS construction to magic number $m=1$.
The fixed curve then has genus one, so its Jacobian is the curve itself and
the conorm/norm map can be evaluated with an ordinary binary elliptic-curve
group law rather than a new higher-genus divisor package.

## Prior art

[CITED] Gaudry, Hess, and Smart define the class-group homomorphism as conorm
to the compositum followed by norm to the fixed field. For odd extension
degree and $m=1$, their fixed-field equation for

$$E_a:y^2+xy=x^3+a x^2+b$$

has coefficient $A=\operatorname{Tr}_{K/k}(a)$ and the same $b$ when $b\in k$.
The original KASH implementation independently checks this equation and maps
places by the same conorm/norm construction.

## Construction

Let $[K:k]=n$ be odd and choose $s\in K$ with $s^2+s=a+A$. Then

$$\psi(x,y)=(x,y+s x)$$

is a $K$-isomorphism from $E_a$ to
$E_A:y^2+xy=x^3+A x^2+b$. If $\sigma(z)=z^{|k|}$, define

$$\Phi(P)=\sum_{i=0}^{n-1}\sigma^i(\psi(P)).$$

[PROVED] The coordinate substitution verifies the curve isomorphism directly.
Each summand is a homomorphism, so $\Phi$ is a homomorphism. Frobenius cyclically
permutes the summands, hence $\Phi(P)\in E_A(k)$. On degree-zero divisor
classes this is the genus-one form of the published conorm/norm map.

## Fixed fixture

- $K=\mathbb F_{2^{10}}$ with modulus $x^{10}+x^3+1$.
- $k=\mathbb F_{2^2}$, so $n=5$.
- Source coefficients $a=234\notin k$ and $b=236\in k$.
- $A=\operatorname{Tr}_{K/k}(a)=236$ and $s=3$.
- Source generator $P=(237,311)$ has order $3$ and is not $k$-rational.
- $\Phi(P)=(237,237)$ has order $3$ on the six-point curve $E_A(k)$.

## Outcome

[EMPIRICAL: one fixed $\mathbb F_{2^{10}}/\mathbb F_{2^2}$ fixture] The
implementation checks $\Phi([d]P)=[d]\Phi(P)$ for every $d\in\{0,1,2\}$ and
recovers secret $2$ by exhaustive DLP in the image subgroup. The source point,
target point, transfer, and DLP are all computed independently of a
source-logarithm lookup table.

[PROVED] This closes the categorical gap identified in A003 for the genus-one
specialization: the auxiliary Jacobian, homomorphism, and target DLP are all
explicit.

## Limitations

The example is intentionally degenerate from an attack-complexity viewpoint.
It implements neither a higher-genus Jacobian nor class-group index calculus,
and the auxiliary group is not asymptotically easier for a reason relevant to
cryptographic GHS attacks. No claim is made beyond the stated fixture and the
general genus-one algebraic identity.
