# Decision checklist for torsion-point leakage

> **Project disposition -- failure / abandoned (2026-07-03).** [PROVED] This
> artifact solves only the realistic finite-template audit. It does not prove
> the unrestricted necessary-and-sufficient criterion in the formal statement;
> the missing completeness theorem remains Q011.

## 0. Result and scope

[PROVED] The procedure in Section 4 is sound and complete for the attack
templates explicitly encoded here: Robert's dimension-8 recovery theorem,
Castryck--Decru's surface decision route, and Maino--Martindale's surface direct
route, after any preprocessing witness has been supplied. "Complete" means
that it returns a positive verdict exactly when the recorded profile supplies
all invocation hypotheses of at least one of those templates. It does **not**
mean that every future Kani-style or higher-dimensional attack is captured.

**Proof.** Each positive leaf is a conjunction of the hypotheses in the cited
theorem or algorithm: R8 is Robert's Theorem 1.1 plus the Section 6.4 recovery
condition; K2 is Castryck--Decru Sections 4--6 or Maino--Martindale Algorithm 1
plus an explicit auxiliary witness. Conversely, the implementation checks
every conjunct before returning that leaf. All other leaves say only which
conjunct is absent, unknown, or too costly. Therefore the equivalence is with
template applicability, not with vulnerability in an unrestricted attack
model. Q011 records the remaining broad necessity question.

[CITED] A full-rank restriction of a secret isogeny to sufficiently large,
smooth torsion can be converted into evaluation and then kernel recovery by a
higher-dimensional isogeny computation; Robert's dimension-8 theorem removes
the need for a special starting curve (Robert 2023, Theorem 1.1, Remark 1.2,
and Section 6.4; current revision dated 2024-10-07).

[CITED] The convenient headline boundary for direct recovery is
$N^2>d$, where $d=\deg\phi$ and the transcript determines
$\phi|_{E_0[N]}$; the conclusion of Robert's paper states the non-strict form
$N^2\ge d$, while the direct-reconstruction discussion uses $N^2>d$ (Robert
2023, Remark 1.2 and Section 7). Under the usual coprimality condition and
$N>1$, equality cannot occur, so this checklist uses the strict form.

[CITED] The earlier surface attacks require a protocol-specific auxiliary
isogeny or smooth-cofactor witness; knowledge of a small non-scalar
endomorphism and the availability of Richelot formulas make this practical but
are not universal logical requirements (Castryck--Decru 2023, Sections 4--5;
Maino--Martindale 2023, Theorem 1 and Algorithm 1).

## 1. SG-01 -- what the published attacks actually need

### 1.1 Common transcript inputs

| ID | Requirement | Status in the published attacks | Trace |
|---|---|---|---|
| C0 | Public domain $E_0$, codomain $E_1$, and a candidate secret isogeny $\phi:E_0\to E_1$ | [CITED] Required to formulate SSI-T and to construct the product containing both curves. | Maino--Martindale 2023, SSI-T definition; Robert 2023, Theorem 1.1. |
| C1 | The degree $d=\deg\phi$, or only polynomially many degree candidates | [CITED] The cited algorithms take the degree as an input and use it in an integer decomposition. Enumerating a polynomial-size candidate set is a direct wrapper around them. | Castryck--Decru 2023, Section 2; Maino--Martindale 2023, Algorithm 1; Robert 2023, first paragraph of Section 1.1. |
| C2 | A generating set for $E_0[N]$ and enough leaked images to derive $\phi|_{E_0[N]}$ as a rank-two map | [CITED] Required to write generators of the higher-dimensional kernel. The literal encoding may be two points, compressed coordinates, or several leaks whose closure gives the same map. | Castryck--Decru 2023, Eq. (2); Maino--Martindale 2023, Algorithm 1 input; Robert 2023, Theorem 1.1 and Lemma 2.2. |
| C3 | Accessible $N$-torsion on the relevant curves over the base field or a polynomial-degree extension | [CITED] Robert states rational-basis hypotheses over $\mathbb F_q$; his parameter-tweak analysis accounts explicitly for extension-field cost. | Robert 2023, Theorem 1.1 and Section 6.1. |
| C4 | Known factorization and sufficiently small largest prime factors for the intended polynomial-time claim | [CITED] The dimension-8 cost contains a factor polynomial in the largest prime divisor of $N$, so smooth $N$ gives polynomial time in $\log N$ while a cryptographic-size prime factor does not. | Robert 2023, Theorem 1.1 and Remark 1.2. |
| C5 | A way to turn evaluation into the protocol's recovery objective | [CITED] Robert's `ComputeKernel` additionally uses accessible target-degree torsion and a smooth-order DLP; Section 6.4 gives a direct reconstruction route when $N^2>d$. | Robert 2023, Theorem 1.1 and Section 6.4. |

[PROVED] Two images are not intrinsically necessary: what is necessary for the
encoded templates is the *derivable rank-two homomorphism*. If several
same-secret leaks generate $E_0[N]$, linearity determines the restriction on a
basis; if they do not generate it, the kernel generators used by the cited
templates remain undetermined.

**Proof.** A homomorphism on a finite abelian group is determined by its values
on a generating set. The kernels in Castryck--Decru Eq. (2) and Robert Lemma
2.2 are explicit functions of those values. Thus any equivalent generating
encoding suffices, while values confined to a proper cyclic subgroup do not
determine the missing basis image.

### 1.2 Castryck--Decru surface route (K2-CD)

[CITED] In their basic notation the leaked order is $N=2^a$, the target degree
is $d=3^b$, and the initial surface construction asks for $N>d$ and an
evaluable auxiliary isogeny $\gamma:E_0\to C$ of degree $c=N-d$
(Castryck--Decru 2023, Section 4).

[CITED] The public images and $\gamma(P_0),\gamma(Q_0)$ define a maximally
isotropic kernel on $C\times E_1$; Kani's reducibility criterion forces the
quotient to split when the guessed secret data are correct (Castryck--Decru
2023, Sections 4.1--4.3, using Kani 1997, Theorem 2.6).

[CITED] Efficient construction/evaluation of $\gamma$, rather than the abstract
existence of the product quotient, is the main extra witness (Castryck--Decru
2023, Sections 4.3--5).

[CITED] A known endomorphism ring, SIKE's explicit small endomorphism, the
choice $N=2^a$, and fast Richelot formulas are conveniences that improve
construction or implementation; the paper also discusses arbitrary small
torsion primes, unknown endomorphism rings when a suitable degree is smooth,
and non-prime-power torsion (Castryck--Decru 2023, Introduction and Section 11).

### 1.3 Maino--Martindale surface route (K2-MM)

[CITED] Their SSI-T input is an unknown degree-$A$ isogeny together with its
restriction to coprime $B$-torsion; their starting curve need not have a known
endomorphism ring (Maino--Martindale 2023, SSI-T definition).

[CITED] Algorithm 1 additionally searches for integers and guesses producing a
positive smooth cofactor $f$ and a small smooth multiplier $e$, satisfying a
relation of the form $eB'=f+A'$ after optionally removing a few secret steps
and leaked torsion levels (Maino--Martindale 2023, Algorithm 1, Steps 1--4).

[CITED] The resulting product isogeny is computed from a Kani diamond and its
action reveals the remaining secret isogeny; smooth-cofactor search and
surface-isogeny arithmetic are therefore required for that concrete algorithm,
not mere conveniences (Maino--Martindale 2023, Theorem 1 and Algorithm 1).

### 1.4 Robert dimension-8 route (R8)

[CITED] For coprime, factored $N>d$, a four-square decomposition of $N-d$, a
rational basis of $E_0[N]$, and its two images under the degree-$d$ secret map,
Robert constructs an $N$-isogeny in dimension 8 that evaluates the secret map
(Robert 2023, Theorem 1.1 and Lemmas 2.1--2.2).

[CITED] The four-square witness depends only on $(N,d)$ and can be found in
randomized polynomial time, so it is not a protocol-specific endomorphism-ring
assumption (Robert 2023, Remark 1.2).

[CITED] Section 6.4 recovers an $N^2$-isogeny from its action on $N$-torsion;
combined with the dimension-8 construction this yields direct recovery when
$N^2>d$ and is the applicable boundary for an individual target map (Robert
2023, Remark 1.2, Section 6.4, and Section 7).

[CITED] The dimension is a constant in the asymptotic theorem but has large
practical constants; polynomial-time applicability is not the same assertion
as an off-the-shelf practical implementation (Robert 2023, Remarks 2.3--2.4).

## 2. SG-02 -- leakage-parameter vocabulary

| Field | Meaning |
|---|---|
| `target_endpoints_public` | Whether one can name the same target map $\phi:E_0\to E_1$ across all used leakage. |
| `degree_visibility` | `exact`, `polynomial_candidates`, `hidden`, or `unknown`. |
| `degree` / `degree_factorization_known` | $d=\deg\phi$ and whether the arithmetic decomposition can use its factors. |
| `torsion_order` / `torsion_factorization_known` | The effective $N$ after combining only compatible same-secret leakage. |
| `torsion_rank` | Rank of the subgroup on which the full target action is derivable; R8/K2 need rank two. |
| `target_action_derivable` | Whether the disclosed encoding determines $\phi|_{E_0[N]}$, not merely unrelated torsion points; `code/leakage_closure.py` derives this field from coordinate-level records. |
| `torsion_access` | Base-field, polynomial-extension, infeasible-extension, or unknown access. |
| `smooth_arithmetic` | Whether the largest prime factors and field costs make the selected fixed-dimension isogeny algorithm polynomial in the security parameter. |
| `kernel_recovery` | Whether the evaluation output can be converted to the secret kernel or an equivalent protocol secret. |
| `surface_certificate` | A mechanically checked K2-CD degree-difference certificate or K2-MM smooth-cofactor certificate. |
| `surface_construction` | Whether the certificate's auxiliary isogeny and surface computation have separately been constructed/evaluated; a numerical identity alone is insufficient. |
| `endomorphism_ring_known` | Diagnostic field: important to low-dimensional witness construction, but not an R8 prerequisite. |
| `same_secret_across_samples` | Prevents invalid CRT aggregation of leakage produced by different ephemeral maps. |
| `basis_family_id` | Identifies source and target torsion bases declared compatible across orders; both this identifier and the target-map identifier must agree before CRT aggregation. |
| `structure` | Supersingular/ordinary and group-action metadata; commutativity alone is neither an attack trigger nor a defense. |

[PROVED] The vocabulary separates *what is public* from *what is constructible*:
the first seven fields describe the transcript closure, while
`surface_certificate`, `surface_construction`, smoothness, and kernel recovery describe an attack
implementation. This prevents a known endomorphism ring or a favorable size
inequality from being mistaken for leaked map evaluations.

**Proof.** The transcript fields can be computed without running a Kani
construction. The implementation fields are existential or cost witnesses used
only after the transcript fields pass. No field appears in both groups.

## 3. SG-03 -- protocol matrix

| Protocol | Degree data | Target torsion action | Other relevant structure | Checklist verdict |
|---|---|---|---|---|
| SIDH (p434-shaped Bob key) | [CITED] $d=3^{137}$ is a factored public system parameter. | [CITED] The public key encodes the images of a basis of $E_0[2^{216}]$ under the same secret map. | [CITED] The torsion is smooth and rational over $\mathbb F_{p^2}$; $2^{432}>3^{137}$. | [PROVED] **R8 positive: polynomial-time key recovery.** |
| SIKEp434 | [CITED] The KEM retains SIDH's known secret-isogeny degree. | [CITED] An uncompressed public key stores the three $x$-coordinates of the images of $P,Q,P-Q$; compression preserves equivalent torsion-map information. | [CITED] The NIST postscript records the 2022 key-recovery break. | [PROVED] **R8 positive: polynomial-time key recovery.** |
| CSIDH | [CITED] The public group-action output does not publish a canonical secret-isogeny degree. | [CITED] The public key is a curve-class representative and sends no auxiliary points. | [CITED] Commutativity enables the key exchange but does not synthesize a restriction of one secret map. | [PROVED] **No published K2/R8 route from the transcript.** This is not a statement about separate quantum group-action attacks. |
| SQIsign 2.0.1 | [CITED] The secret-isogeny degree is parameterized. | [CITED] The public key is $(E_{pk},\mathrm{hint}_{pk})$; the change-of-basis matrix containing $\phi_{sk}(P_0),\phi_{sk}(Q_0)$ information stays in the secret key. | [CITED] Signatures describe a response isogeny, not the long-term secret map; the specification explicitly distinguishes SQIsign from SIDH's easier problem. | [PROVED] **No published K2/R8 key-recovery route from the transcript.** |
| SQIsign2D-West / current 2D response method | [CITED] The long-term secret degree is fixed by parameters. | [CITED] The public key publishes $E_{pk}$, while secret torsion evaluations remain internal; response torsion evaluations intentionally represent the public response map. | [CITED] Higher-dimensional SIDH machinery is used constructively to interpolate response isogenies. | [PROVED] **No published K2/R8 route to the long-term key.** Constructive use is not itself leakage of $\phi_{sk}|_{E_0[N]}$. |

[CITED] The SIDH and SIKE rows follow Robert 2023, Remark 1.2;
Castryck--Decru 2023, Section 2; and the SIKE specification dated 2022-09-15,
Sections 1.3 and 1.5.

[CITED] The CSIDH row follows Castryck et al. 2018, which emphasizes that no
extra points are sent, and Castryck--Decru 2023, Section 2, which says the
attack does not obviously adjust to CRS/CSIDH.

[CITED] The SQIsign rows follow the SQIsign 2.0.1 specification dated
2025-07-07, Sections 1.2, 4.3--4.6, and the SQIsign2D-West paper (Basso et al.
2024, Sections 2 and 4).

## 4. SG-04 -- ordered decision procedure

The executable form is `code/leakage_checklist.py`.

1. **Can one name public endpoints for one target map?**
   - No: `NO_PUBLISHED_ROUTE`.
   - Unknown: `INSUFFICIENT_PROFILE`.
   - Yes: continue.
2. **Is $d=\deg\phi$ exact or polynomially enumerable?**
   - Hidden in a super-polynomial family: `NO_PUBLISHED_ROUTE`.
   - Unknown: `INSUFFICIENT_PROFILE`.
   - Yes: continue for every candidate.
3. **Does the closure of public data determine $\phi$ on rank-two $E_0[N]$ for one $N>1$?**
   - No: `NO_PUBLISHED_ROUTE`.
   - Unknown: `INSUFFICIENT_PROFILE`.
   - Yes: continue.
4. **Are the torsion and factorizations accessible at polynomial cost?**
   - Algebra exists but current arithmetic is not polynomial: `ALGEBRAIC_ONLY`.
   - Unknown: `INSUFFICIENT_PROFILE`.
   - Yes: continue.
5. **After any justified common-factor peeling, is $\gcd(N,d)=1$?**
   - No or peeling not supplied: `WITNESS_DEPENDENT`.
   - Yes: continue.
6. **Does $N^2>d$ and can evaluation be converted to the target secret?**
   - Yes: `KEY_RECOVERY_POLYNOMIAL` via R8.
   - No: continue.
7. **Has a valid K2-CD or K2-MM auxiliary witness been constructed?**
   - Yes with polynomial arithmetic: `KEY_RECOVERY_WITH_SURFACE_WITNESS`.
   - Yes without polynomial arithmetic: `ALGEBRAIC_ONLY`.
   - No/unknown: `WITNESS_DEPENDENT`.

[PROVED] `NO_PUBLISHED_ROUTE` is a scoped negative verdict: it means at least
one input common to all three encoded templates is absent. It does not imply
that the protocol is secure or that another attack family cannot apply.

**Proof.** By inspection, every encoded template consumes public endpoints,
degree data, and a derivable target-map restriction. The negative leaf is
reachable only on failure of one of these shared inputs; no claim about other
templates is made.

## 5. SG-05 -- boundary stress tests

| Case | Profile change | Verdict | Justification |
|---|---|---|---|
| B1: rank-one leak | [PROVED] Known smooth $N,d$ with $N^2>d$, but only one cyclic subgroup image. | `NO_PUBLISHED_ROUTE` | The second basis image needed to determine the displayed kernels is absent. |
| B2: one unit inside the R8 boundary | [PROVED] $N=64$, $d=4095=N^2-1$, full action, smooth arithmetic. | `KEY_RECOVERY_POLYNOMIAL` | The strict inequality passes; no known endomorphism ring is needed. |
| B3: hidden degree | [PROVED] Full smooth rank-two action but $d$ lies in a super-polynomial candidate family. | `NO_PUBLISHED_ROUTE` | All encoded decompositions depend on $d$; exhaustive degree enumeration is not polynomial. |
| B4: below the generic boundary | [PROVED] Full action with $N^2\le d$ and no explicit surface witness. | `WITNESS_DEPENDENT` | Failure of the R8 sufficient inequality is not a safety proof; a CD/MM-style witness or parameter tweak must be exhibited. |
| B5: large-prime torsion | [PROVED] $N^2>d$ and full action, but $N$ has a cryptographic-size prime factor. | `ALGEBRAIC_ONLY` | Robert's cost is polynomial in that prime factor, not in its bit length. |
| B6: aggregating samples | [PROVED] Compatible rank-two restrictions at coprime orders for the same $\phi$ combine; identical-looking leaks for independent ephemeral maps do not. | Positive for the same map; negative for distinct maps | CRT/linearity applies only to one homomorphism. |
| B7: known endomorphism ring only | [PROVED] End$(E_0)$ is public but the transcript contains no target-map images. | `NO_PUBLISHED_ROUTE` | Auxiliary endomorphisms cannot substitute for the missing off-diagonal secret-map action in the encoded kernels. |

**Proof of B6.** For the same homomorphism and coprime $N_1,N_2$, the group
$E[N_1N_2]$ decomposes into its $N_1$- and $N_2$-primary components, so the two
restrictions determine the product-order restriction. For distinct
homomorphisms there is no single map whose restrictions are being combined.

## 6. SG-06 -- necessity and false-positive audit

[PROVED] The broad necessary-and-sufficient criterion requested in the formal
problem is **not** established here. The result is a necessary-and-sufficient
invocation test for a finite set of published templates, plus a conservative
`WITNESS_DEPENDENT` leaf.

**Proof.** The procedure quantifies only over R8, K2-CD, and K2-MM witnesses.
An unrestricted statement would have to quantify over unknown dimensions,
polarizations, parameter transformations, derived leakage, and future recovery
algorithms; no completeness theorem for that space is proved in the cited
sources or this repository.

[CITED] The condition $N^2>d$ is sufficient for Robert's direct route but is
not presented as necessary for every torsion-point attack; the same paper
develops parameter tweaks and lower-dimensional decompositions, and earlier
work attacks specially structured parameter sets (Robert 2023, Sections 3--6;
Castryck--Decru 2023; Maino--Martindale 2023).

[PROVED] The checklist avoids the main false positive "known degree + large
torsion implies break" by additionally requiring a rank-two target-map
restriction, accessible arithmetic, and a recovery route.

**Proof.** These are separate mandatory branches in Section 4 and separate
fields in the executable profile; omitting any one prevents a positive verdict.

[PROVED] The checklist avoids the main false negative "higher-dimensional use
implies leakage" by attaching the torsion restriction to a named target map.
Public evaluation data for an intentionally public response map do not
automatically become evaluations of a different long-term secret map.

**Proof.** `target_action_derivable` is evaluated for the candidate long-term
map, not for any map appearing in the transcript. The SQIsign2D fixture therefore
records response interpolation separately and does not pass C2 for $\phi_{sk}$.

## 7. SG-07 -- implementation decision

[PROVED] A scaled-down Kani attack was not implemented in this session. The
decision is recorded rather than silently omitted: SageMath, Singular, and
msolve are unavailable, while the current shared `lib/isogeny.py` supplies toy
one-dimensional Vélu/orbit routines but no Kani product, Richelot, theta, or
abelian-surface machinery. The deliverable's main uncertainty is template scope
rather than one quotient computation.

[PROVED] An executable decision procedure and thirteen regression fixtures were
implemented instead. This validates the logical branching and protocol
classification but provides no empirical evidence for the algebraic attack
formulas.

## 8. SG-08 -- mechanically derived leakage closure

[PROVED] Let $v_1,\ldots,v_k$ be the source-coordinate columns of disclosed
points in $R^2$, where $R=\mathbb Z/N\mathbb Z$, and let
$\Delta_{ij}=\det[v_i\ v_j]$. The columns generate all of $R^2$ if and only if

$$
\gcd\bigl(N,\{\Delta_{ij}:1\le i<j\le k\}\bigr)=1.
$$

**Proof.** Write $V$ for the $2\times k$ matrix of source columns. If the gcd
is one, Bezout coefficients $c_{ij}$ satisfy
$\sum c_{ij}\Delta_{ij}=1\pmod N$. Embed
$\operatorname{adj}([v_i\ v_j])$ in rows $i,j$ of a $k\times2$ matrix
$S_{ij}$. Then $VS_{ij}=\Delta_{ij}I_2$, so
$R_0=\sum c_{ij}S_{ij}$ is a right inverse of $V$ and the columns span. In the
other direction, if the columns span, $V$ has a right inverse $R_0$.
The two-dimensional Cauchy--Binet identity expresses
$\det(VR_0)=1$ as an $R$-linear combination of the minors, so no prime divisor
of $N$ divides all of them and the displayed gcd is one.

[PROVED] Suppose the corresponding image columns form a $2\times k$ matrix
$W$ in a fixed target basis. When the span condition holds, the unique action
matrix is $A=WR_0$ if and only if every disclosed equation $Av_i=w_i$ verifies;
otherwise the records cannot all belong to one homomorphism in the declared
coordinate systems.

**Proof.** The right-inverse identity gives $AV=WR_0V$ only after the record
equations are checked, so the check is necessary. If it passes, $A$ realizes
all records. Any other realizing matrix agrees with $A$ on a generating set
and hence on all of $R^2$, proving uniqueness.

[PROVED] No individual pair of records has to be a basis at composite order.
For example, the columns $(1,0),(0,2),(0,3)$ modulo $6$ have minors
$2,3,0$; none is a unit modulo $6$, but their collective gcd with $6$ is one.

[PROVED] Full-action certificates at orders $N_1,N_2$ combine to order
$\operatorname{lcm}(N_1,N_2)$ precisely when their four matrix entries agree
modulo $\gcd(N_1,N_2)$, provided both certificates name the same target map
and a compatible source/target basis family.

**Proof.** Apply the generalized Chinese remainder theorem independently to
the four entries. Agreement on the overlap is necessary and sufficient for
each entry, while the shared map and compatible-basis declarations ensure the
resulting matrix represents restrictions of one homomorphism rather than a
coordinate accident.

[EMPIRICAL: 6 deterministic record sets] `code/leakage_closure.py` constructs
the Bezout right inverse, verifies every image equation, and emits a full-action
certificate only after these checks. The fixtures cover collective composite
span, rank one, inconsistent images, same-secret CRT to order $36$, mixed
secrets, and incompatible basis families; all tests pass in
`code/tests/test_leakage_closure.py`.

[PROVED] The implementation deliberately combines only groups that already
determine a full action at their own order. It does not claim completeness for
partial records stated at different, non-nested orders, because relating such
coordinates requires explicit projection or lift data absent from the current
record schema.
