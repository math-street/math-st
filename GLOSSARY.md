# Glossary

## P4.3 - rigorous exTNFS

- [CITED] **Tower norm form:** For $r=a(\iota)-b(\iota)x$ and a tower polynomial $f\in(\mathbb Z[t]/h)[x]$, the integer $|\operatorname{Res}_t(\operatorname{Res}_x(a(t)-b(t)x,f(x)),h(t))|$; exTNFS uses one such form on each side (Kim--Barbulescu 2016).
- [PROVED] **Joint relation-supply statement (RC):** The uniform lower bound on the density of coefficient vectors for which the product of the two tower norms is $B$-smooth; it is the minimal smoothness-density input for the relation-collection upper bound.
- [PROVED] **Special-$q$ statement (SQ):** The joint smooth-cofactor lower bound after coefficient vectors are restricted to the short-vector enumeration box of a prime-ideal lattice; a rigorous descent needs it uniformly through the adaptive descent tree.
- [CITED] **Random-integer smoothness benchmark:** The Canfield--Erdos--Pomerance asymptotic for $\Psi(x,y)/x$; it does not itself count values of a polynomial or norm form.

- **Selection capacity \(b\):** [PROVED] In P5.3, \(b=\log_2M\), where
  \(M\) is the number of distinct candidate executions a designer may screen
  under a precommitted accounting contract. It is a support-size measure,
  not Shannon entropy.
- **Replay rigidity:** [PROVED] The property that a fixed published document
  reproduces one parameter package. It does not by itself determine the
  designer's pre-publication menu.
- **Provenance rigidity:** [PROVED] The smallness of the externally defined,
  pre-publication candidate menu after all unforced specification choices are
  charged.
- **Provenance identifiability:** [PROVED] Historical \(b\) is identifiable
  from a public record when every admissible design history producing that
  record has the same quotient menu size.
- **Unidentifiable audit value \(\bot\):** [PROVED] The cited source does not
  determine one historical selection capacity across its admissible histories.
  It denotes neither zero nor infinity and makes no claim about motive.
- **Coefficient-uniform versus class-uniform:** [PROVED] In P5.3, the former
  gives equal mass to passing short-Weierstrass coefficient pairs, while the
  latter gives equal mass to their \(\mathbb F_p\)-isomorphism classes. They
  coincide only when every retained class has the same number of encodings.
- **Class-uniform minimax kernel:** [PROVED] Uniform sampling on a fixed finite
  class universe uniquely minimizes its maximum singleton probability. P5.3
  A004 implements exact toy rejection/unranking into canonical safe classes.

- [CITED] **Reduced norm of an element:** For
  $x=a+bi+cj+dk\in(-1,-p)$,
  $\operatorname{nrd}(x)=x\bar x=a^2+b^2+p(c^2+d^2)$.
  [Kohel--Lauter--Petit--Tignol 2014, Section 2.2]
- [CITED] **Reduced norm of a left ideal:**
  $N(I)=\sqrt{|\mathcal O/I|}=\gcd\{\operatorname{nrd}(x):x\in I\}$ for an
  integral left $\mathcal O$-ideal. [Kohel--Lauter--Petit--Tignol 2014,
  Section 2.4]
- [CITED] **Normalized ideal norm form:**
  $q_I(x)=\operatorname{nrd}(x)/N(I)$. It is integral and invariant under
  right-multiplication equivalences of left ideals.
  [Kohel--Lauter--Petit--Tignol 2014, Section 2.4]
- [CITED] **Equivalent left ideals:** $I$ and $J$ are equivalent when
  $J=I\gamma$ for some nonzero quaternion $\gamma$; the left order is
  preserved. [Kohel--Lauter--Petit--Tignol 2014, Section 2.4]

- [CITED] **SSWU:** The simplified Shallue-van de Woestijne-Ulas deterministic map used by RFC 9380 directly on short-Weierstrass curves with $A B\ne0$, and through a suite-fixed isogeny when $AB=0$ (RFC 9380, Sections 6.6.2-6.6.3).
- [CITED] **Elligator 2:** The deterministic map used by RFC 9380 on eligible Montgomery curves and, through rational transport, twisted Edwards curves (RFC 9380, Sections 6.7-6.8).
- [CITED] **SvdW:** The Shallue-van de Woestijne deterministic map used as RFC 9380's generic short-Weierstrass fallback when suite parameters satisfy the Section 6.6.1 predicates.
- [CITED] **Uniform `hash_to_curve` encoding:** The RFC 9380 composition of `hash_to_field(msg, 2)`, two deterministic map calls, point addition, and cofactor clearing; its random-oracle conclusion requires the Section 10.1 assumptions.
- [PROVED] **P5.4 compile-time family:** The suite-fixed choice among SSWU, SvdW, and Elligator 2, optionally followed by fixed isogeny or model transport; it is one external interface but not one algebraic map formula.
- [PROVED] **Schedule-constant in P5.4:** Every input for one fixed public curve and field executes the same recorded sequence of high-level field-operation labels. This term does not assert constant-time behavior of the Python backend.

- **Xedni calculus:** A global lifting strategy that seeks a rational
  dependence among lifts of random finite-field linear combinations; the name
  reverses "index."
- **Canonical height convention in P1.6:** The LMFDB/Sage non-normalized value
  $\widehat h(P)=\lim n^{-2}h_x([n]P)$ over $\mathbb Q$.

## P4.2 - Pairing-friendly cycles

- **Per-curve rho:** [PROVED] For a curve over \(\mathbb F_p\) with largest
  prime subgroup order \(r\), \(\rho=\log p/\log r\). For a prime-order cycle,
  \(r_i=p_{i+1}\).
- **Cycle rho:** [PROVED] P4.2 uses
  \(\rho_{\max}=\max_i\log(p_i)/\log(p_{i+1})\). This states the per-curve
  threshold directly. The geometric mean is not used: its value is identically
  1 for every prime-order cycle because the product telescopes.

- [CITED] **$q$-type assumption:** An assumption whose challenge exposes a
  number of group encodings that grows with parameter $q$; P2.2 uses the more
  precise Lu–Zhandry polynomial-independence condition when invoking their
  separation theorem.  [Lu–Zhandry 2024, Def. 4.2]
- [CITED] **Static / fixed-size assumption:** An assumption whose challenger
  emits at most a constant number of group elements, independent of $q$ and of
  the adversary's query bound.  [Lu–Zhandry 2024, Def. 4.1]
- [CITED] **$q$-SDH:** From a source-group power ladder through $x^q$, output
  $(c,g^{1/(x+c)})$ for an allowed scalar $c$.  [Boneh–Boyen 2008, §3.1]
- [CITED] **GR-BB reduction:** Lu–Zhandry's representation-independent generic
  reduction that is fully black-box in every possibly inefficient adversary.
  [Lu–Zhandry 2024, §3]
- [PROVED] **UR-FBB reduction:** P2.2's universally representation-uniform
  fully-black-box class: one standard-oracle reduction machine may inspect
  encoding bits but has a pointwise security guarantee over every group
  implementation.  Every UR-FBB reduction is a GR-BB reduction.
- [PROVED] **Representation-specific reduction:** A reduction whose security
  guarantee is asserted only for a named concrete group representation.  Its
  machine may or may not have generic syntax; the localized guarantee alone
  does not survive random relabeling.
- [PROVED] **$s$-fresh reduction:** P2.2/A006's representation-specific,
  fully-black-box class in which at most $s$ distinct valid source-group labels
  per execution first enter typed use without being challenger outputs, the
  public generator, known-scalar labelings, or recorded group-operation
  outputs.
- [CITED] **Structured generic-group model:** A labeled-group model with free
  access to a partial operation $\star$ that agrees with the group law wherever
  defined; its general discrete-log lower bound depends on the fraction of
  labels constrained by $\star$.  [Corrigan-Gibbs--Henzinger--Wu 2026,
  Defs. 2.2--3.1 and Thm. 3.2]
- [CITED] **SXDH:** The assumption that DDH is hard in each of the two source
  groups of an asymmetric pairing.  [Yuen et al. 2024, §2]
- [CITED] **Déjà Q:** The composite-order subgroup/parameter-hiding framework
  for generically reducing broad $q$-type assumption classes to static
  subgroup hiding.  [Chase–Meiklejohn 2014]

- **ECDLP:** Given $P,Q\in E(\mathbb F_p)$ with $Q=[k]P$, recover $k$.
- **GGM:** Generic group model.
- **First fall degree $d_{\mathrm{ff}}$:** First degree of a nontrivial
  homogeneous syzygy among the top parts in the truncated associated-graded
  ring; P1.3 fixes the exact quotient and trivial-syzygy convention.
- **Degree of regularity $d_{\mathrm{reg}}$:** First degree in which the
  homogeneous ideal generated by the top parts fills the entire homogeneous
  component, when this degree exists.
- **Solving degree $\operatorname{sd}_\sigma$:** Least closed Macaulay cutoff
  whose row space contains a Gröbner basis for the named monomial order.
- **Algorithm maximum degree $D_{\mathcal A}$:** Largest degree label processed
  in one fully specified algorithm run; not an algebraic invariant.
- **SSSA:** The anomalous-curve attacks independently associated with Semaev,
  Smart, and Satoh–Araki.
- **$\mathsf{CCA}_0$:** The literal coordinate-cost machine defined in P1.1,
  with free field arithmetic and packing but a charged `ECADD` instruction.
- **$P^+(N)$ / $B$-smooth:** The largest prime factor of $N$ (with
  $P^+(1)=1$); $N$ is $B$-smooth when $P^+(N)\le B$.
- **Auxiliary group (Maurer reduction):** A constant-rank group algebraically
  defined over the field attached to a prime divisor of the input group order,
  used to turn a CDH oracle into arithmetic on implicit field elements.
- [PROVED] **$\mathsf{SCM}_{C,K}(r)$ (P2.1):** With
  $L=\lceil\log_2r\rceil$, the existence of a negative fundamental
  discriminant $D$ and integers $t,v$ such that $|D|\le L^K$,
  $4r=t^2-Dv^2$, and $P^+(r+1-t)\le L^C$.
- [CITED] **FAPI-1:** Given nonzero \(P\in\mathbb G_1\) and \(z\in\mathbb G_T\), recover the unique \(Q\in\mathbb G_2\) with \(e(P,Q)=z\) (Galbraith–Hess–Vercauteren 2008).
- [CITED] **Miller inversion (MI):** Given a fixed Miller-function argument and a raw field target, recover an allowed divisor or point evaluating to that target, or report that none exists (Galbraith–Hess–Vercauteren 2008).
- [CITED] **Final-exponentiation inversion (FEI):** Given a reduced pairing target, find a raw field element mapping to it under the final power map, with any domain-compatibility condition stated separately (Galbraith–Hess–Vercauteren 2008; Satoh 2025 revision).
- [CITED] **SSI-T:** Given public endpoints of an unknown degree-$A$
  supersingular isogeny and its restriction to coprime $B$-torsion, recover a
  matching isogeny (Maino--Martindale 2023).
- [CITED] **R8 route:** Robert's dimension-8 construction that turns a full
  rank-two smooth torsion restriction into secret-isogeny evaluation and, with
  the recovery hypotheses, key recovery (Robert 2023).
- [CITED] **K2 witness:** A protocol-specific auxiliary isogeny and numerical
  decomposition that instantiate a Castryck--Decru or Maino--Martindale
  abelian-surface attack (Castryck--Decru 2023; Maino--Martindale 2023).
- [PROVED] **`NO_PUBLISHED_ROUTE` (P3.4):** At least one common input to the
  encoded R8/K2 templates is absent; this is not a general security verdict.

## P3.2 — class-group quantum cost

- [PROVED] **Phase-state query:** The P3.2 interface returning a shift-independent classical label (a) and the qubit ((|0\rangle+e^{2\pi ias/N}|1\rangle)/\sqrt2).
- [PROVED] **Abstract query count:** The number of initial phase states consumed by the specified sieve schedule; it is not a gate count or elapsed time.
- [CITED] **QRACM:** Classical memory that a quantum computation can address coherently; its cost is treated separately from quantum-memory bits in Kuperberg-style tradeoffs (Kuperberg 2013; Peikert 2020).
- [PROVED] **Regular action:** An action that is both free and transitive; in a finite transitive permutation action this is equivalent to a trivial point stabilizer.

## P5.1 — Koblitz density

- [CITED] **Corrected Koblitz constant $C_{E,t}$:** The divisibility-ordered limit of the density of adelic Galois-image elements for which $\#E(\mathbb F_p)/t$ is integral and avoids all tested prime divisors, normalized by the corresponding random-integer density. (Zywina 2011, Definition 2.1.)
- [CITED] **Universal Koblitz product $C$:** The full-$\mathrm{GL}_2$ product $\prod_\ell(1-(\ell^2-\ell-1)/((\ell-1)^3(\ell+1)))\approx0.5051661682$. (Zywina 2011, equation (2.3).)
- [HEURISTIC] **Refined prime-sum predictor:** $C_{E,t}\sum_{p\le x}(\log(p+1)-\log t)^{-1}$; it can be falsified as a useful finite-range approximation by a validated sustained discrepancy larger than the stated sampling uncertainty. (Zywina 2011, Section 2.4.)
