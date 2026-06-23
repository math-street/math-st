# P1.4 — Classifying Weil Descent Vulnerability

## Formal statement

Given an elliptic curve $E/\mathbb{F}_{q^n}$ and a genus bound $B$, decide whether a curve $C/\mathbb{F}_q$ of genus at most $B$ admits a cover to $E$ defined over $\mathbb{F}_q$, and construct the cover when it exists.

The initial experimental regime is characteristic two with $q=2$ and $n\in\{4,6,8\}$.

## First target

[CITED] For an ordinary binary curve
$$
E: y^2+xy=x^3+ax^2+b,
$$
the classical GHS construction is controlled by the $\mathbb F_2$-span of the Frobenius conjugates of $\sqrt b$ together with the constant $1$ (Gaudry–Hess–Smart, 2002, *Journal of Cryptology*, doi:10.1007/s00145-001-0011-x).

The first target is to compute that span exactly, reproduce a published genus, and exhaustively tabulate the resulting GHS genus for every nonzero $b\in\mathbb F_{2^n}$ for $n\in\{4,6,8\}$.

## Scope

This session studies only the classical characteristic-two GHS locus. It does not decide the existence of arbitrary covers, analyze odd characteristic, or include isogeny walks.
