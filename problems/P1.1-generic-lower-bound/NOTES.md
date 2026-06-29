# Notes

## Stable facts

- [PROVED] In the literal model where field operations, coordinate tests, and
  packing coordinates into a point are free while only an `ECADD` instruction
  is charged, every `ECADD` can be compiled into free field instructions.
  See [`MODEL.md`](MODEL.md), Theorem 1.
- [PROVED] BSGS therefore solves every instance in that model with zero charged
  group operations; this is stronger than merely admitting a non-generic
  attack. See [`MODEL.md`](MODEL.md), Corollary 2.
- [PROVED] Semaev/Gaudry/Diem relation collection is also syntactically
  expressible with zero charged group operations: scalar multiplications and
  relation verification compile to coordinate formulas, while polynomial
  systems can be exhaustively solved using the free field fragment. See
  [`MODEL.md`](MODEL.md), Proposition 3.
- [PROVED] Removing `PACK` does not repair the model: virtual points can remain
  ordinary field tuples until the algorithm outputs the logarithm. See
  [`READ_ONLY_MODEL.md`](READ_ONLY_MODEL.md), Theorem 4.
- [PROVED] More generally, an explicit group representation with a free
  representation-level group law has zero charged group-oracle query
  complexity for DLP. See [`READ_ONLY_MODEL.md`](READ_ONLY_MODEL.md), Theorem 6.
- [CITED] Shoup's generic lower bound depends on opaque random encodings:
  after $m$ oracle queries a simulator needs to track only $m+2$ affine-linear
  polynomials in the hidden logarithm, and it can return a fresh random string
  for every new formal polynomial (Shoup 1997, Theorem 1).
- [EMPIRICAL: p=17, one known-answer instance] The executable fixture recovers
  $[7](5,1)=(0,6)$ on $y^2=x^3+2x+2$ over $\mathbb F_{17}$ with 17 charged
  additions through the group interface and zero charged additions through the
  coordinate-compiled interface; both runs execute the same 15 affine-addition
  events (`data/observe_coordinate_bypass_p17_20260624.csv`).
- [EMPIRICAL: p=17, one known-answer decomposition] Exhaustive $f_3$ evaluation
  over the factor-base coordinates $x<8$, followed by sign lifting and group-law
  verification, recovers a decomposition of $[7](5,1)$; see
  `data/observe_semaev_decomposition_p17_20260626.csv`.
- [EMPIRICAL: p=17, all 16 nonzero logarithms tested in the library and one
  recorded trace] The Smart lifting implementation recovers the fixed secret
  after two lifts modulo $17^2$, 12 lifted group operations, and one
  formal-parameter ratio; see `code/observe_smart_attack.py` and
  `data/observe_smart_attack_p17_20260626.csv`.
- [EMPIRICAL: p=43, subgroup order 11] The staged Tate-pairing fixture maps
  $Q=[2]P$ to $e(Q,T)=e(P,T)^2$, reproduces the reduced values $11+3t$ and
  $26+23t$, and recovers the exponent in the target subgroup; see
  `code/observe_mov_transfer.py` and
  `data/observe_mov_transfer_p43_r11_20260626.csv`.
- [EMPIRICAL: q=5, extension degree 3, one fixed relation] Expanding $f_3$ in
  the polynomial basis of $\mathbb F_{5^3}$ gives three base-field coefficient
  equations; 25 factor-base pair evaluations leave one zero pair and one
  directly verified ordered decomposition; see
  `code/observe_extension_decomposition.py` and
  `data/observe_extension_decomposition_q5_n3_20260626.csv`.
- [EMPIRICAL: $K/k=\mathbb F_{2^{10}}/\mathbb F_{2^2}$, one order-three
  subgroup] The odd-degree genus-one GHS fixture computes the conorm/norm map
  as the sum of five Frobenius conjugates, checks all three scalar relations,
  and recovers secret 2 on the six-point auxiliary curve; see
  `code/observe_ghs_transfer.py` and
  `data/observe_ghs_transfer_q4_n5_r3_20260629.csv`.

## SG-01 — operation-requirement taxonomy

### Legend

`R` means required by the cited algorithm as written, `I` means an
implementation choice rather than an essential requirement, and `—` means the
row has an expression not using the primitive. `EXT` includes construction of
an extension field, a distinguished base field or subspace, or Weil
restriction. `AUX-DLP` means that the attack transfers the logarithm to a
different group. `LA` is relation-matrix linear algebra.

### Matrix

| Attack | Group law | Equality / collision | Coordinate field arithmetic | $p$-adic lift | Pairing | Polynomial-system solving | EXT / subfield structure | AUX-DLP | LA |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [PROVED] BSGS, as implemented in `lib/dlog.py` | R | R | — | — | — | — | — | — | — |
| [PROVED] Pollard rho, as implemented in `lib/dlog.py` | R | R | I | — | — | — | — | — | — |
| [PROVED] Pohlig–Hellman, as implemented in `lib/dlog.py` | R | R | — | — | — | — | — | — | — |
| [CITED] Semaev–Smart–Satoh–Araki anomalous-curve attack (Semaev 1998; Satoh–Araki 1998; Smart 1999) | R | — | R | R | — | — | — | — | — |
| [CITED] MOV / Frey–Rück transfer (Menezes–Okamoto–Vanstone 1993; Frey–Rück 1994) | R | R | R | — | R | — | R | R | — |
| [CITED] GHS Weil descent (Gaudry–Hess–Smart 2002) | R | R | R | — | — | — | R | R | R |
| [CITED] Semaev prime-field decomposition (Semaev 2004) | R | R | R | — | — | R | — | — | R |
| [CITED] Gaudry/Diem extension-field decomposition (Gaudry 2009; Diem 2011) | R | R | R | — | — | R | R | — | R |

### Per-cell justifications

#### BSGS

- [PROVED] `Group law = R`: the baby table forms $[j]P$ and the giant walk
  forms $Q-[im]P$.
- [PROVED] `Equality = R`: a match between a baby point and a giant point is
  the meet in the middle; replacing hashing by a scan still needs equality.
- [PROVED] `Coordinates, lift, pairing, polynomial solving, EXT, AUX-DLP, LA = —`:
  the algorithm in `lib/dlog.py:bsgs` uses only the abstract group interface,
  equality, integer arithmetic, and a dictionary.

#### Pollard rho

- [PROVED] `Group law = R`: every walk transition adds $P$, adds $Q$, or
  doubles the current point.
- [PROVED] `Equality = R`: the method extracts a logarithm only after two walk
  states collide in their group element.
- [PROVED] `Coordinate arithmetic = I`: `lib/dlog.py:pollard_rho` partitions by
  $x\bmod 3$, but a random oracle or a function of an opaque encoding can
  replace that partition without changing the collision method.
- [PROVED] `Lift, pairing, polynomial solving, EXT, AUX-DLP, LA = —`: none of
  these appears in the state transition or collision equation implemented in
  `lib/dlog.py`.

#### Pohlig–Hellman

- [PROVED] `Group law = R`: cofactor multiplications project the instance into
  prime-power subgroups and digit corrections subtract known multiples of $P$.
- [PROVED] `Equality = R`: the implementation solves each order-$\ell$ digit
  with BSGS, whose meet step needs equality.
- [PROVED] `LA = —`: CRT combines independent scalar congruences, but no
  relation matrix is used.
- [PROVED] `Coordinates, lift, pairing, polynomial solving, EXT, AUX-DLP = —`:
  `lib/dlog.py:pohlig_hellman` is expressed using group operations, equality,
  integer factorization, small subgroup DLP, and CRT only.

#### Semaev–Smart–Satoh–Araki anomalous-curve attack

- [CITED] `Group law = R`: the algorithms multiply lifted points, including a
  multiplication by $p$, on a lift of the curve (Semaev 1998; Smart 1999).
- [CITED] `Coordinate arithmetic = R` and `$p$-adic lift = R`: the attack lifts
  the curve and input points from characteristic $p$ to a $p$-adic/local
  setting and reads a formal-group parameter from the lifted coordinates
  (Semaev 1998; Satoh–Araki 1998; Smart 1999).
- [CITED] `Equality, pairing, polynomial solving, EXT, AUX-DLP, LA = —`: the
  cited local-lifting route obtains the scalar from the ratio of local/formal
  logarithmic quantities, without a collision search, pairing transfer,
  multivariate relation search, extension-field descent, foreign DLP, or
  relation matrix.

#### MOV / Frey–Rück

- [CITED] `Group law = R`: scalar multiplication locates torsion components and
  Miller-style pairing evaluation follows an addition chain (Menezes,
  Okamoto, and Vanstone 1993; Frey and Rück 1994).
- [CITED] `Equality = R`: the reduction checks that a pairing value is
  nontrivial and the target finite-field DLP uses equality in its target group.
- [CITED] `Coordinate arithmetic = R`, `Pairing = R`, and `EXT = R`: rational
  functions are evaluated on curve coordinates over a field containing the
  required torsion, and the Weil or Tate pairing maps into roots of unity in an
  extension field (Menezes, Okamoto, and Vanstone 1993).
- [CITED] `AUX-DLP = R`: bilinearity turns $Q=[k]P$ into
  $e(Q,T)=e(P,T)^k$, which is a DLP in a finite-field multiplicative subgroup
  (Menezes, Okamoto, and Vanstone 1993).
- [CITED] `$p$-adic lift, polynomial-system solving, LA = —`: these operations
  are absent from the pairing transfer itself.

#### GHS Weil descent

- [CITED] `Group law = R`, `AUX-DLP = R`, and `LA = R`: GHS transfers the ECDLP
  to the divisor-class group of a higher-genus curve over the smaller field and
  applies an index-calculus DLP there (Gaudry, Hess, and Smart 2002).
- [CITED] `Coordinate arithmetic = R` and `EXT = R`: the construction descends
  equations from a characteristic-two composite extension to its base field
  and constructs the covering/descent curve (Gaudry, Hess, and Smart 2002).
- [CITED] `Equality = R`: relation verification and the target class-group
  computation compare represented divisor classes.
- [CITED] `$p$-adic lift, pairing, polynomial-system solving = —`: the GHS
  construction is a Weil-descent transfer followed by a class-group DLP; its
  polynomial arithmetic and factorization do not require the multivariate
  system-solving primitive used by Semaev/Gaudry/Diem decomposition.

#### Semaev prime-field decomposition

- [CITED] `Group law = R` and `Equality = R`: relation collection computes
  $R=[a]P+[b]Q$ and verifies decompositions of $R$ into factor-base points
  (Semaev 2004).
- [CITED] `Coordinate arithmetic = R` and `Polynomial solving = R`: the factor
  base is defined by bounded $x$-coordinates and relations are zeros of
  summation polynomials (Semaev 2004).
- [CITED] `LA = R`: enough relations determine factor-base logarithms and the
  target logarithm by modular linear algebra (Semaev 2004).
- [CITED] `$p$-adic lift, pairing, EXT, AUX-DLP = —`: the proposal works
  directly on $E(\mathbb F_p)$ and does not transfer the DLP to a different
  group.

#### Gaudry/Diem extension-field decomposition

- [CITED] `Group law = R` and `Equality = R`: a relation starts from a random
  linear combination of the ECDLP inputs and is verified as a sum of
  factor-base points (Diem 2011, Section 2.3).
- [CITED] `Coordinate arithmetic = R`, `Polynomial solving = R`, and `EXT = R`:
  for $E/\mathbb F_{q^n}$ the factor base is cut out by a degree-two covering
  whose image lies in $\mathbb P^1(\mathbb F_q)$, and decomposition solves a
  multivariate system over $\mathbb F_q$ after expanding in an
  $\mathbb F_q$-basis of $\mathbb F_{q^n}$ (Diem 2011, Sections 2.1 and 2.3).
- [CITED] `LA = R`: relation rows are reduced over the subgroup-order ring to
  recover the target logarithm (Diem 2011, Section 2.3).
- [CITED] `$p$-adic lift, pairing, AUX-DLP = —`: the method is a direct index
  calculus on $E(\mathbb F_{q^n})$; Weil restriction is used in the analysis
  rather than to transfer the DLP to a different group (Diem 2011, Introduction).

## SG-02 — Shoup's proof and the opacity boundary

### Prime-order statement in repository notation

[CITED] Let $G=\langle P\rangle$ have prime order $r$, choose
$k\leftarrow\mathbb F_r$, and give a generic algorithm the random encodings
$\sigma(P)$ and $\sigma([k]P)$. If it makes at most $m$ group-oracle queries,
then its success probability is $O(m^2/r)$ (Shoup 1997, Theorem 1).

### Re-derivation

1. [PROVED] Associate the inputs with formal polynomials $F_1(K)=1$ and
   $F_2(K)=K$ in $\mathbb F_r[K]$; addition or subtraction of two known group
   elements produces the corresponding sum or difference of their formal
   polynomials, so every $F_i$ remains affine-linear.
2. [PROVED] A symbolic simulator gives equal labels exactly when two formal
   polynomials are identical and otherwise samples a fresh unused label; after
   $m$ queries it has at most $m+2$ formal polynomials.
3. [PROVED] For distinct affine-linear polynomials $F_i\ne F_j$, the equation
   $F_i(k)=F_j(k)$ has at most one solution in $\mathbb F_r$, hence occurs for
   uniform $k$ with probability at most $1/r$.
4. [PROVED] A union bound over at most $\binom{m+2}{2}$ pairs bounds the
   probability of any accidental collision by $\binom{m+2}{2}/r$.
5. [PROVED] Conditioned on no accidental collision, the transcript is
   independent of $k$ beyond the formal equalities, so a final scalar guess
   equals $k$ with probability at most $1/r$.
6. [PROVED] The total success probability is therefore at most
   $(\binom{m+2}{2}+1)/r=O(m^2/r)$; constant success probability requires
   $m=\Omega(\sqrt r)$.
7. [PROVED] If $\#E(\mathbb F_p)=r$ is prime, Hasse's bound
   $|r-(p+1)|\le 2\sqrt p$ implies
   $\sqrt r=p^{1/2}(1+O(p^{-1/2}))$, so the generic lower bound is
   $\Omega(p^{1/2})$ in the stated regime.

### Exact use of opacity

[PROVED] The opacity assumption is used in step 2, not in the root-counting
step: the simulator is allowed to replace a newly computed group element by an
independent fresh string because the algorithm can observe only string
equality and the group oracle's answers.

[PROVED] If the label is instead the affine coordinate pair, a fresh random
string is not a valid simulation: the pair must satisfy the curve equation,
its negation has the same $x$-coordinate, and the coordinates of a sum satisfy
the rational chord-and-tangent formulas. These are observable relations even
when no two group elements collide.

[PROVED] Extending Shoup's symbolic list from affine-linear exponent
polynomials to coordinate rational functions does not preserve his argument:
the algorithm can itself evaluate the addition rational map, and in the
literal zero-cost coordinate model that evaluation bypasses the charged oracle
entirely.

## SG-03 — candidate-model audit

| Model | Representation access | What it admits | Lower-bound relevance |
|---|---|---|---|
| [CITED] Shoup GGM (1997) | Opaque random strings; equality plus group oracle | BSGS, Pollard rho, Pohlig–Hellman | Gives $O(m^2/r)$ success after $m$ queries |
| [CITED] Maurer abstract black-box model (2005) | Hidden state; only declared operations and relations are visible | Depends on the declared relation set; equality recovers the generic case | Useful only after coordinate predicates are explicitly enumerated |
| [CITED] AGM (Fuchsbauer–Kiltz–Loss 2018) | Group-specific computation is allowed; group-element outputs require known linear representations | It is designed to cover group-specific algorithms | The paper explicitly states that the AGM does not yield information-theoretic complexity lower bounds |
| [CITED] Generic ring model (Aggarwal–Maurer 2009) | Opaque ring elements; ring operations, inverses, and equality | Ring-generic algorithms | It is not a coordinate-access ECDLP model until a point-construction interface and its cost are specified |
| [PROVED] Literal free-coordinate model $\mathsf{CCA}_0$ | Explicit coordinates; all field work and packing are free | Every row of SG-01, and compiled BSGS | Zero charged operations suffice |

[PROVED] A generic-ring instantiation with free ring operations and an
uncharged operation that packs two field handles into an elliptic-curve point
collapses for the same reason as $\mathsf{CCA}_0$: the Weierstrass addition
formulas are ring/rational operations followed by packing.

[PROVED] Removing free packing prevents that particular compiler, but then the
model must say whether coordinate-derived points can be fed to later group
operations; without such a rule the semantics are incomplete, while forbidding
all such feedback excludes the decomposition and pairing rows by definition.

## SG-04/05 — current obstruction and repair directions

[PROVED] Free reification is sufficient to kill the literal candidate but is
not necessary: read-only coordinates still kill it because virtual points may
remain field tuples until the scalar output is produced.

[PROVED] Charging by instruction name is insufficient because the same
mathematical addition map has both a charged `ECADD` spelling and an uncharged
field-formula spelling.

[PROVED] Three coherent repairs remain: charge field operations as well as
group operations; bound the size or degree of coordinate computations; or
define an extensional cost that charges every evaluation of the addition
rational map regardless of syntax.

[PROVED] The first two repairs change the target from a pure group-operation
lower bound to a joint computation bound, while the third requires a semantic
accounting rule rather than an ordinary machine instruction cost.

## Validation audit

| Attack row | Executable evidence | Coverage |
|---|---|---|
| BSGS | [EMPIRICAL: p=17, order 19] `observe_coordinate_bypass.py` and `lib/tests/test_dlog.py` recover a fixed logarithm through both oracle and coordinate-formula spellings. | Complete for the matrix primitives. |
| Pollard rho | [EMPIRICAL: p=17, order 19] `lib/tests/test_dlog.py` recovers the fixed logarithm with the group-law walk and collision test. | Complete for the matrix primitives. |
| Pohlig–Hellman | [EMPIRICAL: p=7, cyclic group order 12] `lib/tests/test_dlog.py` recovers the fixed logarithm through the $2^2$ and $3$ prime-power components, small-subgroup BSGS, and CRT. | Complete for the matrix primitives. |
| SSSA / Smart | [EMPIRICAL: p=17, anomalous order 17] `observe_smart_attack.py` records the lift, lifted group arithmetic, coordinate work, and formal ratio. | Complete for the listed primitives. |
| MOV / Frey–Rück | [EMPIRICAL: p=43, subgroup order 11, embedding degree 2] `observe_mov_transfer.py` records extension-field point arithmetic, two pairings, ten Miller line steps, and one target-group DLP. | Complete for the listed primitives. |
| GHS | [EMPIRICAL: $\mathbb F_{2^{10}}/\mathbb F_{2^2}$, order-three subgroup] `observe_ghs_transfer.py` constructs the genus-one auxiliary Jacobian, evaluates the five-conjugate conorm/norm map, checks every subgroup scalar, and solves the target DLP. The independent P1.4 tests additionally cover higher-genus invariants. | Complete for an exact genus-one transfer. Higher-genus divisor arithmetic and an attack speedup are not claimed; see `attempts/A004-genus-one-ghs-transfer.md`. |
| Semaev over $\mathbb F_p$ | [EMPIRICAL: p=17, one fixed relation] `observe_semaev_decomposition.py` records polynomial solving, sign lifting, equality, and relation verification. | Complete through relation collection; relation-matrix linear algebra is represented by the shared modular DLP tests, not a large relation matrix. |
| Gaudry/Diem over $\mathbb F_{q^n}$ | [EMPIRICAL: q=5, n=3, one fixed relation] `observe_extension_decomposition.py` records the subfield factor base, basis expansion, polynomial system, sign lifting, and group verification. | Complete through relation collection; large relation-matrix linear algebra is not benchmarked. |

[PROVED] The explicit genus-one GHS program is itself compiled from field and
coordinate operations admitted by the free local language, consistently with
Corollary 5 in `READ_ONLY_MODEL.md`. The executable result validates the
operation row; it is not evidence for a higher-genus asymptotic speedup.
