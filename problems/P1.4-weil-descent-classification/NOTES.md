# Notes

## Stable facts

[CITED] Let $K=\mathbb F_{2^N}$, let the descent base be $k=\mathbb F_{2^d}$ with $n=N/d$, and put $\sigma(x)=x^{2^d}$. For the ordinary binary model $y^2+xy=x^3+ax^2+b$, the GHS magic number is
$$
m=\dim_{\mathbb F_2}\operatorname{span}\{(1,\sigma^i(\sqrt b)):0\le i<n\}.
$$
Under the stated GHS regularity condition, the descended curve is hyperelliptic and has genus $2^{m-1}$ or $2^{m-1}-1$ (Gaudry–Hess–Smart, 2002, Theorem as restated by Maurer–Menezes–Teske, 2001/2002).

[CITED] Write $r$ for the dimension of the span of the conjugates of $\sqrt b$. Hess's genus formula specializes to
$$
g=2^{m-1}-2^{m-r}+1.
$$
Thus $g=2^{m-1}$ when $1$ lies in the conjugate span and $g=2^{m-1}-1$ otherwise (Hess, 2003, EUROCRYPT, doi:10.1007/3-540-39200-9_23).

[PROVED] The square root in $\mathbb F_{2^N}$ is unique and equals $b^{2^{N-1}}$: squaring is an automorphism of a finite field, and squaring this expression gives $b^{2^N}=b$.

[PROVED] For the displayed ordinary binary model, $j(E)=1/b$: the characteristic-two Weierstrass invariants give $c_4=1$ and $\Delta=b$, hence $j=c_4^3/\Delta=1/b$.

[EMPIRICAL: all $b\ne0$ in $\mathbb F_{2^n}$, $n\in\{4,6,8\}$] The exact genus distribution and low-genus equations are recorded in `RESULTS.md` and the CSV files under `data/`.

[PROVED] The Frobenius annihilator of $b$ equals that of $\sqrt b$: squaring commutes with Frobenius and is an invertible $\mathbb F_2$-linear map on the field.

[EMPIRICAL: all full-degree parameters, $n\in\{4,6,8\}$] The minimum basic-GHS genus is $4$, $8$, and $16$, respectively.

## Tool substitution

[EMPIRICAL: environment check 2026-06-23] SageMath, Singular, and msolve are unavailable; Python 3.13.4 is available (`env/check_env.py`). The session therefore uses direct polynomial-basis arithmetic over $\mathbb F_2$.

## Boundaries

> **Gap.** The span/genus computation does not construct the descended curve or the cover map. Resolving this requires a function-field implementation of the GHS fixed field or an equivalent explicit special-case construction.
> Blocking: no. Logged as Q002.

> **Gap.** Genus alone does not determine whether the descended Jacobian DLP beats Pollard rho on the original subgroup. Resolving this at toy scale requires curve orders, an explicit descent map, Jacobian arithmetic, and measured DLP costs.
> Blocking: no. Logged as Q003.
