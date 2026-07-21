---
attempt: A009
status: completed
---
# A009 - From a Weil polynomial to an explicit auxiliary surface

## Idea

[CONJECTURE] The ordinary Weil polynomial produced by the prescribed-order
argument may admit a direct algebraic realization whose complexity is hidden
by the existential statement of Honda--Tate.

## Prediction and decision rule

[CONJECTURE] Checked inverse-Honda--Tate and genus-two algorithms will either
require CM class invariants or start from an explicit member of the desired
isogeny class.  The prediction is refuted by a uniform algorithm that takes
$(r,f)$, outputs explicit bounded-degree equations and group law for a surface
with Frobenius polynomial $f$, and runs in time polynomial in $\log r$ for all
ordinary degree-four $f$ used in A007.

## Plan

1. [PROVED] Separate construction of the Weil polynomial, certification that
   an isogeny class exists, certification that the class contains a Jacobian,
   and construction of an explicit equation.
2. [PROVED] Audit CM, gluing, isogeny-walk, and invariant-reconstruction
   routes against the stated input/output contract.
3. [PROVED] Test whether a non-geometric representation of the rational-point
   group still supports Maurer--Wolf's recoverable algebraic embedding.

## Four distinct output levels

[CITED] Van Bommel--Costa--Poonen--Smith--Li construct an integral Weil
polynomial $f$ with $f(1)=N$ and then invoke Honda--Tate to conclude that
$f=f_A$ for some abelian variety.  The separation is explicit in their proof:
for example, Construction 9.1, Step 6 says to take such an $A$ "if one
exists," and Proposition 9.3 uses Theorem 2.1 to supply existence.

[PROVED] The following four outputs are logically distinct:

1. [PROVED] an integral degree-four polynomial $f$ with $f(1)=N$;
2. [CITED] a Honda--Tate certificate that an abelian-surface isogeny class
   with polynomial $f$ exists;
3. [CITED] a Howe--Nart--Ritzenthaler certificate that the isogeny class
   contains a genus-two Jacobian;
4. [PROVED] an explicit curve equation, group law, and recoverable
   Maurer--Wolf `EMBED/EXTRACT` implementation.

[PROVED] Outputs 1--3 do not contain output 4.  They specify coefficients,
an isogeny class, and an existence predicate, respectively, but no projective
model or coordinate algorithms.

## Jacobian existence is checkable but not constructive

[CITED] Howe--Nart--Ritzenthaler 2009, Theorem 1.2, gives a complete
coefficient criterion for whether a degree-four Weil polynomial occurs as
the Frobenius polynomial of a genus-two curve.  Its positive conclusion is
that a Jacobian exists in the isogeny class; it is not an algorithm returning
the curve equation.

[PROVED] The exact ordinary-prime-field cases of that criterion can be
applied using only integer arithmetic and factorization.  Script
`code/surface_jacobian_scan.py` enumerates

$$
 f(x)=x^4+ax^3+bx^2+arx+r^2
$$

through the exact root-interval inequalities, groups the resulting values
$f(1)$, and marks whether at least one polynomial for each order passes the
Jacobian criterion.

[EMPIRICAL: r=251,1019,4091,16363] Every integer in

$$
 [r^2-\lfloor r^{3/2}\rfloor,
   r^2+\lfloor r^{3/2}\rfloor]
$$

was both an ordinary abelian-surface order and the order of some
Jacobian-containing isogeny class.  For the four fields the interval sizes
were respectively $7{,}953$, $65{,}057$, $523{,}329$, and $4{,}186{,}243$.

[EMPIRICAL: same four fields, B=floor((log_2 r)^3)] The numbers of smooth
integers in those intervals were respectively $3{,}038$, $17{,}379$,
$97{,}059$, and $528{,}541$; every one also had a Jacobian-admissible Weil
polynomial.  The HNR exception families were validated separately in four
unit tests before the scan.

[PROVED] This computation strengthens only the finite existence picture.
The HNR criterion does not output any of the millions of asserted curve
equations, so the experimental equality of the order sets does not validate
a realization algorithm.

## Why the checked construction routes do not supply a seed

[CITED] Bröker--Howe--Lauter--Stevenhagen 2015, Theorem 1.1 and Corollary
4.8, give exponential worst cases for CM constructions that prescribe a
genus-two Jacobian order.

[CITED] The heuristic polynomial-time algorithm in that paper solves the
different problem of prescribing $|C(\mathbb F_p)|$.  Its constructed
Jacobian is isogenous to a product $E_1\times E_2$ and does not have the
prescribed order in general.

[PROVED] An isogeny walk cannot repair the missing initial model.  Isogenous
abelian varieties have the same Frobenius polynomial, so an isogeny algorithm
can move among explicit members of the target class only after at least one
explicit member of that class has already been supplied.

[PROVED] Reconstructing a curve from supplied moduli invariants is likewise
downstream of the missing step: a Weil polynomial does not specify Igusa
invariants of one isomorphism class inside the isogeny class.

## Abstract rational-point groups are insufficient

[PROVED] From the known smooth integer $N$ one can write down an abstract
finite abelian group of order $N$.  Even if additional ideal-module data
describing a rational-point group in the desired isogeny class were supplied,
such data would not by itself instantiate Maurer--Wolf Definition 4: it gives
neither an algebraic map from an implicitly represented $x\in\mathbb F_r$
into group coordinates nor an extraction algorithm recovering $x$.

[PROVED] Even explicit equations and a group law would not alone discharge
this interface.  A007 proves the interface for a genus-two Jacobian because
the embedded curve point has the recoverable Mumford coordinate
$u(z)=z-(x+e)$.  An arbitrary explicit abelian surface would still need a
comparable bounded-cost recoverable encoding.

## Outcome

[PROVED] The prediction was confirmed.  The checked theory can construct and
classify the Weil polynomial and can decide Jacobian existence, but no checked
uniform algorithm converts the A007 polynomial into an explicit strongly
algebraically defined surface in polynomial time.

[PROVED] The realization gap is now narrowed to a seed problem: output one
explicit genus-two Jacobian in the desired isogeny class, or output another
bounded-degree surface together with a recoverable algebraic embedding.  CM
has exponential worst cases, isogeny walks require such a seed, and abstract
group representations omit the embedding interface.
