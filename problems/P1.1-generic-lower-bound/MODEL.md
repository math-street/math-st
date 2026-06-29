# Formal model and case-(b) result

## 1. The literal coordinate-cost machine $\mathsf{CCA}_0$

Fix $p>3$ and a nonsingular short-Weierstrass curve

$$
E: y^2=x^3+Ax+B
$$

over $\mathbb F_p$. An ECDLP instance consists of explicit coordinates for
$P,Q\in E(\mathbb F_p)$ and a prime $r=\#E(\mathbb F_p)$, with $Q=[k]P$.

The machine has integer registers, field registers, and point registers. The
following instructions and all ordinary control flow are uncharged:

- integer arithmetic, storage, loops, branching, and random sampling;
- field constants, addition, subtraction, multiplication, inversion of a
  nonzero value, and equality in $\mathbb F_p$;
- projection of a point to its coordinates;
- construction, evaluation, resultants, and exhaustive root search for
  polynomials over $\mathbb F_p$;
- `PACK(x,y)`, which returns the point $(x,y)$ after checking the curve
  equation, together with a distinguished representation of $O$.

The instruction `ECADD(R,S)` returns $R+S$ and has cost one. The cost of a run
is the number of executed `ECADD` instructions. No bound is placed on the
number of uncharged instructions because the proposed resource measure counts
only group operations.

## 2. The addition compiler

### Theorem 1

[PROVED] Every $\mathsf{CCA}_0$ program has an extensionally equivalent
program that executes no `ECADD` instruction.

### Proof

[PROVED] It is enough to replace one call `ECADD(R,S)`. If either input is
$O$, return the other. Write $R=(x_1,y_1)$ and $S=(x_2,y_2)$. If
$x_1=x_2$ and $y_1=-y_2$, return $O$. Otherwise compute

$$
\lambda=
\begin{cases}
(y_2-y_1)(x_2-x_1)^{-1},&R\ne S,\\
(3x_1^2+A)(2y_1)^{-1},&R=S,
\end{cases}
$$

and then

$$
x_3=\lambda^2-x_1-x_2,\qquad
y_3=\lambda(x_1-x_3)-y_1.
$$

All operations are in $\mathbb F_p$ and are uncharged. The exceptional
branches ensure that every displayed denominator is nonzero. The standard
chord-and-tangent derivation gives $(x_3,y_3)=R+S$, and `PACK(x_3,y_3)` is
uncharged. Replacing each `ECADD` call proves the theorem. $\square$

### Corollary 2

[PROVED] ECDLP in $\mathsf{CCA}_0$ has charged cost zero.

### Proof

[PROVED] Run BSGS and compile every group addition using Theorem 1. The result
uses $O(\sqrt r)$ uncharged field/point operations and equality tests, returns
$k$, and executes zero charged instructions. A slower exhaustive search would
also have charged cost zero. $\square$

## 3. Explicit index-calculus expression

[CITED] For $E:y^2=x^3+Ax+B$, Semaev's third summation polynomial is

$$
\begin{aligned}
S_3(X_1,X_2,X_3)={}&(X_1-X_2)^2X_3^2\\
&-2\big((X_1+X_2)(X_1X_2+A)+2B\big)X_3\\
&+(X_1X_2-A)^2-4B(X_1+X_2),
\end{aligned}
$$

and higher summation polynomials are obtained recursively by resultants
(Semaev 2004).

### Proposition 3

[PROVED] The Semaev/Gaudry/Diem decomposition template is expressible in
$\mathsf{CCA}_0$ with zero charged group operations.

### Expression

1. [CITED] Choose a factor base $\mathcal F$ by restricting point
   $x$-coordinates, or over $\mathbb F_{q^n}$ by requiring a covering
   coordinate to lie in $\mathbb F_q$ (Semaev 2004; Diem 2011).
2. [PROVED] Choose $a,b$ and compute $R=[a]P+[b]Q$ using the addition compiler;
   this executes no charged instruction.
3. [CITED] Form
   $S_{m+1}(X_1,\ldots,X_m,x(R))$ and seek a zero whose $X_i$ correspond to
   factor-base points (Semaev 2004).
4. [PROVED] Even if no polynomial-system solver is primitive, nested
   enumeration of the finite candidate sets plus polynomial evaluation is an
   exact uncharged solver in $\mathsf{CCA}_0$.
5. [PROVED] Lift each $X_i$ to its possible $y$-coordinates and use the
   addition compiler to select signs and verify
   $R=P_1+\cdots+P_m$; this also executes no charged instruction.
6. [CITED] Record the resulting linear relation, repeat, and solve the relation
   matrix over $\mathbb Z/r\mathbb Z$ to recover $k$ (Semaev 2004; Diem 2011).

[PROVED] Every group-law occurrence in this expression is compiled away and
every remaining operation is in the uncharged fragment, so the charged cost is
zero. This proves case (b) for the literal model. $\square$

## 4. Why an oracle-only lower bound cannot survive explicit input coordinates

[PROVED] The collapse is information-theoretic rather than a claim that ECDLP
is fast in ordinary time: the complete finite instance is already present in
the input coordinates, so unbounded local computation can determine $k$
without consulting a separately charged group oracle.

[PROVED] Any meaningful lower bound must therefore bound local computation,
remove or restrict explicit coordinate access, or charge coordinate programs
according to the group maps they realize. Merely naming `ECADD` as the charged
instruction does not define a representation-invariant resource measure.

