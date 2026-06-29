# Read-only coordinates and the no-query theorem

## 1. Typed read-only coordinate machine $\mathsf{ROCCA}_0$

The machine has three disjoint register types:

- point handles, created only for $O$, the input points $P,Q$, and outputs of a
  charged `ECADD`/`ECNEG` oracle;
- field values in $\mathbb F_p$;
- ordinary integers and finite data structures.

For a point handle $H$, `COORD(H)` returns its affine coordinates, or an
infinity flag, at zero cost. All integer and field arithmetic, equality tests,
polynomial manipulation, storage, branching, loops, exhaustive finite search,
and linear algebra are free. Explicit extension fields and finite quotient
rings are represented by finite tuples of base-field or integer values, so
their arithmetic is also a free tuple program. There is no `PACK` instruction,
and field values can never become point handles. The charged cost is the number
of group-oracle calls.

### Handle invariant

[PROVED] Every point handle created during a run represents
$[a+b k]P$ for coefficients $a,b\in\mathbb F_r$ known to the algorithm, where
$Q=[k]P$ and $r=\#E(\mathbb F_p)$.

### Proof

[PROVED] The input handles have coefficient pairs $(0,0)$ for $O$, $(1,0)$
for $P$, and $(0,1)$ for $Q$. A charged sum, difference, or negation applies
the same linear operation to the coefficient pairs. Induction on the number of
oracle calls proves the invariant. $\square$

## 2. Read-only access still collapses

### Theorem 4 — zero-query ECDLP

[PROVED] Every ECDLP instance in $\mathsf{ROCCA}_0$ can be solved with zero
group-oracle calls.

### Proof

[PROVED] Project the coordinates of $P$ and $Q$. In field registers maintain a
tuple $V$ consisting of an infinity flag and two field values. Initialize
$V=O$. For $j=0,1,\ldots,r-1$, compare the tuple $V$ with the projected tuple
for $Q$; if they agree, output $j$. Otherwise replace $V$ by the affine
chord-and-tangent formula for $V+P$, including its exceptional branches.

[PROVED] These tuples are ordinary field data, not point handles, so the type
rule forbidding `PACK` is never invoked. Induction gives $V=[j]P$ after $j$
iterations. Since $P$ generates the prime-order group, exactly one
$j\in\{0,\ldots,r-1\}$ satisfies $V=Q$. The program uses only free field
instructions and executes no group-oracle call. $\square$

### Corollary 5 — virtual-point compiler

[PROVED] Any classical algorithm whose point operations have explicit
coordinate formulas can be simulated without point handles by representing
every internal point as a tuple of field values and applying those formulas
directly.

### Proof

[PROVED] Replace each internal point type by its coordinate tuple, each group
operation by its rational coordinate formula with exceptional branches, and
each point equality by coordinate equality. The simulation preserves every
branch and final scalar output while making no group-oracle call. $\square$

## 3. General no-go statement

### Theorem 6 — canonical-representation no-go

[PROVED] Let a finite group family have an explicit representation in which
the group law and equality are computable by operations declared free. Any
model that receives those representations as ordinary input and charges only a
separate group oracle has zero oracle-query complexity for discrete logarithm.

### Proof

[PROVED] Enumerate successive powers or multiples of the generator using the
free representation-level group law and compare each representation with the
target. The procedure terminates after at most the group order and never calls
the charged oracle. $\square$

[PROVED] The theorem is a query-complexity statement, not a polynomial-time
algorithm: it shows that a lower bound on one named oracle is impossible when
the same operation is available in the free local language.

## 4. Consequences for the attack taxonomy

### Generic algorithms

[PROVED] For BSGS, Pollard rho, and Pohlig–Hellman, replace every internal
point by an infinity flag and two field values, every addition by the complete
branched affine formula, and every point comparison by tuple comparison.
Scalar multiplications are loops around the same virtual addition program.
The resulting programs preserve their tables, walks, projections, and final
scalar outputs and make zero group-oracle calls.

### SSSA / Smart lifting

1. [CITED] Lift the curve and input points to a ring modulo $p^2$, compute
   lifted $p$-multiples, and recover the logarithm from a ratio of formal-group
   parameters (Semaev 1998; Satoh–Araki 1998; Smart 1999).
2. [PROVED] Represent a lifted coordinate by an integer modulo $p^2$ and a
   lifted point by a projective or affine tuple. Hensel lifting, ring
   arithmetic, and the doubled-and-added $p$-multiple are free tuple programs.
3. [PROVED] Compute the formal parameter and its ratio in integer registers and
   output the residue modulo $p$; no value needs to become a point handle.

### MOV / Frey–Rück

1. [PROVED] Represent $\mathbb F_{p^k}$ as coefficient tuples modulo a chosen
   irreducible polynomial and represent torsion points by extension-coordinate
   tuples.
2. [CITED] Evaluate a Weil or Tate pairing along an addition chain, apply final
   exponentiation, and reduce $Q=[d]P$ to
   $e(Q,T)=e(P,T)^d$ in a finite-field subgroup (Menezes–Okamoto–Vanstone
   1993; Frey–Rück 1994).
3. [PROVED] Each Miller line, virtual curve transition, extension-field
   operation, exponentiation, equality test, and finite target-DLP search lies
   in the free tuple language. The expression therefore makes zero base
   group-oracle calls.

### GHS Weil descent

1. [CITED] Expand the characteristic-two curve over an extension-field basis,
   construct the descent cover and its divisor-class map, transfer the ECDLP
   to the descended Jacobian, and run class-group index calculus (Gaudry–Hess–
   Smart 2002).
2. [PROVED] Basis expansion, Frobenius, equation construction, polynomial
   arithmetic, divisor reduction, relation tests, and relation-matrix algebra
   are programs on finite tuples and polynomials; none requires a base
   elliptic-curve point handle.
3. [PROVED] Source scalar combinations can first be computed as virtual source
   coordinates, then passed as ordinary coordinate data to the explicit
   descent map. Thus an explicit GHS implementation is a zero-base-oracle
   program in the generalized finite-field version of $\mathsf{ROCCA}_0$.

### Semaev / Gaudry / Diem decomposition

1. [CITED] Form virtual random combinations of the ECDLP inputs, solve the
   summation-polynomial system over a coordinate or subfield factor base,
   verify the lifted relation, and solve the relation matrix (Semaev 2004;
   Gaudry 2009; Diem 2011).
2. [PROVED] The random combination uses the virtual addition compiler;
   polynomial construction, exhaustive system solving, sign enumeration,
   relation verification, and modular linear algebra are all in the free
   language.
3. [PROVED] This is the read-only analogue of Proposition 3 in `MODEL.md` and
   makes zero group-oracle calls.

[PROVED] The typed read-only rule therefore excludes none of the SG-01 attack
rows: every row has an explicit expression using only free data programs and a
final scalar output.

## 5. Exhaustion of natural repairs

### Free coordinate programs closed under composition

[PROVED] If the free coordinate language contains the curve law and permits
iteration or polynomial-size/unbounded composition, Theorem 4 or Corollary 5
applies.

### One-shot or predicate-only coordinates

[PROVED] If arbitrary coordinate predicates are free, a predicate may contain
the entire virtual-point computation and test whether $Q=[j]P$; bounding the
predicate's circuit size or algebraic degree is therefore necessary to avoid
the no-query theorem.

### Taint rules

[PROVED] Marking field values derived from coordinates as tainted does not
help if tainted values may still undergo the addition formulas and be compared
with target coordinates; forbidding those operations removes general free
coordinate arithmetic by definition.

### Extensional charging

[PROVED] A rule that charges every field program computing the group law can
block the compiler, but its cost is semantic rather than instruction based and
must also specify how approximate, batched, or algebraically equivalent
programs are recognized.

### Charging or bounding field computation

[PROVED] Charging field operations, bounding total circuit size, or bounding
predicate degree yields a coherent model, but the resulting lower bound is no
longer a lower bound that counts only group operations while granting free
general coordinate arithmetic.

## 6. Conclusion for case (b)

[PROVED] Both the literal and read-only natural interpretations of “coordinate
arithmetic free, only group operations counted” admit zero-query ECDLP and, in
particular, admit every index-calculus-style row in SG-01. Avoiding the collapse
requires restricting or charging coordinate computation, so the requested
intermediate model cannot simultaneously retain the stated free access and
support a nonzero group-operation lower bound.
