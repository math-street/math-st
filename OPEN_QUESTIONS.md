# Open questions

Question identifiers are namespaced by owning problem. A repeated numeric
suffix therefore denotes separate questions only when the problem prefix is
different.

## Question index

| Identifier | State |
|---|---|
| P1.2/Q001 | Resolved in the translate-probe model |
| P1.2/Q002 | Open, optional Candidate-D continuation |
| P1.2/Q003 | Needs a specification choice |
| P1.2/Q004 | Open only for corrected Variant S |
| P1.3/Q022, P1.3/Q023 | Open |
| P1.4/Q002, P1.4/Q003 | Open |
| P1.5/Q004 | Open |
| P1.6/Q008, P1.6/Q018 | Open |
| P2.1/Q005 | Open and blocking the full reduction |
| P2.2/Q003 | Open residual branch |
| P3.2/Q012, P3.2/Q013 | Open beyond the scoped results |
| P3.3/Q099 | Open end-to-end comparison |
| P3.4/Q011 | Open beyond published templates |
| P4.1/Q009, P4.1/Q010 | Resolved |
| P4.1/Q027 | Open archival question |
| P4.2/Q010 | Needs a specification choice |
| P4.3/Q016, P4.3/Q017 | Open and blocking rigor |
| P5.1/Q026 | Open for the unconditional asymptotic |
| P5.2/Q020, P5.2/Q024 | Resolved in their stated models |
| P5.2/Q025 | Open |
| P5.3/Q014 | Reopen only on new archival evidence |
| P5.3/Q015 | Resolved at toy scale |
| P5.4/Q012 | Needs external RFC confirmation |
| P5.4/Q021 | Open beyond the compile-time family |

## P5.1/Q026 - What input can break the prime-order sieve barrier for a fixed curve?

[CITED] David--Wu's theta-zero-free hypothesis supplies effective Chebotarev remainders strong enough for an eight-almost-prime lower bound and a prime-order upper bound, but not a prime-order lower bound. (David and Wu 2012, Theorems 1.1 and 1.3, arXiv:0812.2860.)

[CITED] Dey--Saha--Sivaraman--Vatwani determine the refined fixed-curve constant only after assuming an elliptic Elliott--Halberstam conjecture and a separate conjecture on the average growth of $N_p=\#E(\mathbb F_p)$. (Dey et al. 2025, DOI 10.1016/j.jmaa.2024.129212.)

[CITED] The fixed-curve Koblitz asymptotic remains open even under the numerical agreement reproduced through $x=10^9$ here. (Lee, Mayle, and Wang 2025, arXiv:2408.16641; Zywina 2011, Section 9.)

[PROVED] For the audited CM curve, `problems/P5.1-koblitz-conjecture/THEORY_CLOSURE.md` reduces the event, apart from $p=17$, to simultaneous primality of $N(a+bi)$ and $N(a+bi+1)/8$; this isolates a prime-pair value problem rather than an uncomputed local constant.

> **Gap.** I do not know an unconditional replacement for both conjectural inputs that yields an asymptotic lower bound for prime values of $\#E(\mathbb F_p)$. Resolving it requires uniform remainder control at the needed moduli and a parity-breaking mechanism that distinguishes primes from integers with a bounded number of prime factors. Blocking: yes for the formal unconditional Koblitz asymptotic; no for P5.1's completed algebraic and computational deliverables. Logged as P5.1/Q026.

## P5.4/Q021 - Can P5.4 be extended beyond the compile-time prime-field family?

[PROVED] P5.4/A002--A003 covers all three requested presentations and both exceptional invariants through a compile-time prime-field family, adds one cubic-extension SvdW fixture, and adds bounded ordinary-curve routes in characteristics two and three. The core formulas remain distinct, a valid SvdW $Z$ does not exist on at least the tiny fixture $p=7$, $y^2=x^3+x+1$, and the small-characteristic routes cover only stated subfamilies.

[CITED] RFC 9380 deliberately excludes characteristics two and three and uses suite-specific mappings rather than one formula (Faz-Hernandez et al. 2023, Sections 2.1, 6.1, and 8).

> **Gap.** I do not know a single branch-free bounded-operation construction covering every finite field and presentation, nor an impossibility theorem for such a construction. One toy $p=11$ suite now has compiled complete-group, assembly, subgroup, and timing evidence, but resolving the formal problem still requires all-curves/all-degrees characteristic-two/three proofs and a portable compiled backend for every route, or a lower bound for a precisely defined arithmetic model. Blocking: yes for calling P5.4 solved; no for the completed compile-time-family partial result. Logged as P5.4/Q021.

## P1.6/Q018 - What exact sampler and dependence test produced the p=17 xedni count?

[CITED] Jacobson, Koblitz, Silverman, Stein, and Teske (2000) describe the
finite input and broad projective-lattice procedure for Experiment A and
report 317 dependent cases in 100,000 runs, but the available account does not
fix the probability distribution or tie-breaking rules for lattice candidates
and identifies 2-descent as the dependence test.

> **Gap.** I do not have the original LiDIA/SIMATH implementation, a complete
> specification of its projective-vector and coefficient-vector sampler, or
> an equivalent locally validated 2-descent pipeline. Resolving this requires
> obtaining that code/specification and matching at least one published
> intermediate distribution before comparing dependency rates. Blocking: yes
> for P1.6/SG-09; no for the completed SG-08 bounded-relation audit. Logged as
> P1.6/Q018 and dead attempt A002.

## P4.3/Q016 - Can coefficient randomization make tower relation supply provable?

[PROVED] P4.3 reduces exTNFS relation supply to the uniform joint lower bound (RC) for two iterated-resultant norm forms and reduces special-$q$ descent to the adaptive lattice-conditioned bound (SQ).

[CITED] Lee--Venkatesan's rigorous ordinary NFS makes a polynomial evaluation vary in an integer arithmetic progression, but the exTNFS outer field norm is nonlinear when the tower degree $\eta>1$.

> **Gap.** I do not know a coefficient distribution or candidate-rich slice that preserves the common residue-field factor and exTNFS norm bounds while putting the outer integer norm under a uniform smooth-values theorem. Resolving this requires constructing such a distribution and proving (RC), then extending it to (SQ), or proving that a specified class of randomizations cannot meet the candidate-count/norm-size constraints. Blocking: yes for a rigorous exTNFS smoothness analysis. Logged as P4.3/Q016.

[PROVED] P4.3/A003 narrows this gap: for fixed $\eta=2$, the $(p,K)$ kernel family is algebraically surjective onto the tower order for ideal-coprime candidates, but bounded preimage multiplicities and irreducibility remain open.  In the interior range $\ell_p<2/3$, retaining the standard $L_Q(2/3)$ norm scale forces $\eta\to\infty$, beyond every fixed-form theorem audited.

## P4.3/Q017 - Do structured exTNFS relation rows have adequate rank?

[PROVED] A lower bound on the number of simultaneously smooth candidates does not imply that their ideal-valuation and Schirokauer-map rows span the required space modulo the DLP prime $\ell$.

> **Gap.** I do not know an unconditional rank theorem for the exTNFS relation matrix, even assuming the smoothness supply (RC). Resolving this requires either a distributional rank theorem for the actual structured rows, a deterministic row-construction modification, or a different rigorous linear-relation mechanism. Blocking: yes for a complete unconditional DLP complexity proof, independently of P4.3/Q016. Logged as P4.3/Q017.

[PROVED] P4.3/A004 reduces the needed distributional statement to the escape bound $\inf_{\varphi\ne0}\Pr[\varphi(R)\ne0]\ge L_Q(1/3,-o(1))$ for rows conditioned on simultaneous smoothness.  This is weaker than uniform random rows but is not supplied by a smoothness count.

## P5.3/Q014 — Can finite historical menus be recovered for secp256k1 and BLS12-381?

### Status and exact question

**[PROVED]** P5.3 resolves the source-bounded audit but not the counterfactual
historical menu. The numerical curve-core and full-package capacities remain
\(\bot\) for both curves because the inspected record does not identify one
finite pre-publication menu size. This is nonblocking for the formalization and
blocking only for replacing either \(\bot\) with a historical number.

The residual question is deliberately narrower: does a dated artifact exist
that was fixed before publication and determines the finite candidate domain,
equivalence projection, enumeration or objective priority, stopping and
tie-breaking rules, and the candidates actually screened?

### Evidence required for a positive answer

**[PROVED]** Under P5.3's accounting contract, a reproducible numerical
historical \(b=\log_2 M\) follows from a provenance certificate that fixes:

1. the complete finite candidate domain or a proved finite cap;
2. the curve-core or full-package equivalence projection used to count
   distinct outputs;
3. the enumeration order, objective priority, stopping rule, and all ties;
4. every randomness source and whether it could be selected, restarted, or
   suppressed;
5. a dated commitment showing those rules predated the chosen constants; and
6. a replay transcript, rejection list, or equivalent evidence constraining
   which branches were screenable.

**[PROVED]** A final constant, a list of desirable properties, or code that
only regenerates dependent constants is insufficient: each can be compatible
with multiple pre-publication menus.

### Primary-source ledger

- **[CITED]** SEC 2 version 1.0 (SECG, 2000, Sections 2.1 and 2.7.1) says that
  prime-field Koblitz parameters were repeatedly selected among parameters
  admitting efficient endomorphisms until a prime-order curve was found. It
  publishes secp256k1 but gives no finite domain, enumeration order, rejected
  candidates, random-source record, or generator derivation. See
  `problems/P5.3-rigidity-formalization/refs/secg2000.md`.
- **[CITED]** SEC 2 version 2.0 (SECG, 2010) preserves the published
  secp256k1 tuple without adding the missing finite historical menu or
  transcript. See `problems/P5.3-rigidity-formalization/refs/secg2010.md`.
- **[CITED]** Bowe's BLS12-381 construction note (2017-03-11) publishes the
  family parameter and design objectives and says that later work would
  explain the selection more fully. It does not commit to a complete finite
  \(u\)-domain, priority order, or rejection transcript. See
  `problems/P5.3-rigidity-formalization/refs/bowe2017.md`.
- **[CITED]** The zero-parent `zkcrypto/pairing` commit `a06216f`
  (2017-07-08) records field-size bounds,
  \(u\bmod72\in\{16,64\}\), a low-Hamming-weight objective, an optimization
  claim, and a canonical G1/G2 generator rule. It postdates the announcement
  and still omits a finite \(u\)-menu, objective priority, and rejected
  candidates. See
  `problems/P5.3-rigidity-formalization/refs/bowe-pairing2017.md`.
- **[CITED]** crates.io and docs.rs both begin the public `pairing` package
  history at version 0.9.0 on 2017-07-08. There is no indexed 0.8.x or earlier
  registry snapshot that predates the announcement. See
  `problems/P5.3-rigidity-formalization/refs/crates-pairing2017.md`.
- **[EMPIRICAL: all reachable refs in a 2026-07-01 clone of
  `zkcrypto/pairing`]** The reachable history contains no earlier commit,
  selection program, finite \(u\)-domain, objective ordering, or rejection
  transcript.
- **[EMPIRICAL: one public Web Archive CDX request on 2026-07-01]** The
  archive-index request timed out and supplied no additional artifact. This is
  a failed retrieval channel, not evidence that no private or unindexed
  artifact exists.

### Why the published output cannot determine \(b\)

**[PROVED]** Let the published package be \(y\). One admissible history may
have the singleton quotient menu \(\{y\}\), giving \(M=1\) and \(b=0\).
Another may permit the designer to screen the quotient menu
\(\{y,z_2,\ldots,z_m\}\) and publish any member, after which the observed
history publishes \(y\), giving \(M=m\) and \(b=\log_2m\). Both histories
expose the same final package.
Therefore no function of that package alone recovers historical selection
capacity.

**[PROVED]** The theorem remains true after publishing deterministic
derivations of the field, coefficients, subgroup, or generator: derivations
constrain downstream freedom but do not identify an omitted upstream candidate
fiber.

### Audit consequence

- **[PROVED]** secp256k1 retains A256 curve-core \(b=\bot\) and package
  \(b=\bot\); the repeated-selection sentence narrows admissible histories but
  does not determine their quotient-menu cardinality.
- **[PROVED]** BLS12-381 retains A256 curve-core \(b=\bot\) and package
  \(b=\bot\) because the upstream \(u\)-menu and objective order remain
  unidentified.
- **[PROVED]** Conditional on the surviving canonical G1/G2 rule and a fixed
  \(u\), BLS12-381's residual generator-only freedom is zero. This conditional
  downstream value does not replace the unconditional \(\bot\).
- **[PROVED]** Here \(\bot\) means “not identifiable from the cited public
  record.” It means neither zero nor infinity and makes no assertion about
  intent or motive.

### Reopening and falsification condition

> **Residual archival question.** Reopen P5.3/Q014 only for a dated
> pre-publication artifact that constrains the admissible historical fiber by
> fixing the finite domain or cap, equivalence projection, ordering/objective
> priority, stopping/tie rules, and screenable transcript. A later narrative,
> literal bit length, or performance rationale alone does not falsify the
> \(\bot\) result. Logged as P5.3/A003–A004. Blocking: no for P5.3; yes only
> for a numerical historical audit value.

## P5.3/Q015 — Resolved at toy scale: which fixed kernel minimizes singleton mass?

### Status and fixed interpretation of “best”

**[PROVED]** P5.3/Q015 is resolved for the fixed toy universe and the minimax
maximum-singleton criterion. “Best” is not projection-independent: uniformity
over coefficient encodings and uniformity over curve isomorphism classes are
different requirements when classes have unequal encoding multiplicities.

**[PROVED]** For a fixed finite class universe of size \(N\), the evaluation
criterion is
\[
  \min_{\mu}\max_{C}\mu(C).
\]
It measures the largest probability available to a hidden weakness
concentrated on one class. It does not claim optimality for every possible
performance, safety, or operational objective.

### Exact toy profile

**[PROVED]** The implemented profile fixes:

1. `bits=7` and the largest prime below \(2^7\) congruent to \(3\bmod4\),
   namely \(p=127\);
2. nonsingular short-Weierstrass encodings
   \(E_{a,b}:y^2=x^3+ax+b\) with \(0\leq a,b<127\);
3. \(\mathbb F_{127}\)-isomorphism by the scaling action
   \((a,b)\mapsto(u^4a,u^6b)\) for \(u\in\mathbb F_{127}^{*}\);
4. the lexicographically least coefficient pair as the canonical class key;
5. curve and twist prime-subgroup bit lengths at least 5, curve and twist
   cofactors at most 8, embedding degree at least 4, absolute Frobenius
   discriminant at least 16, and exclusion of traces 0 and 1; and
6. a deterministic subgroup base-point rule after the class is selected.

**[PROVED]** In characteristic greater than three, two short-Weierstrass
models are \(\mathbb F_p\)-isomorphic while preserving infinity exactly when
their coefficients lie in one such scaling orbit. The toy safety predicate is
constant on every orbit because it uses curve and twist orders and quantities
derived from them.

### Coefficient kernel versus class kernel

**[PROVED]** Let \(\mathcal C\) be the set of safe coefficient encodings and
let \(O\subseteq\mathcal C\) be one isomorphism orbit. Conditional on A002's
coefficient-level rejection sampler passing safety,
\[
  \Pr_{\mathrm{coeff}}[O]=\frac{|O|}{|\mathcal C|}.
\]
Thus coefficient-uniform sampling is class-uniform exactly when every safe
orbit has the same size.

**[PROVED]** A004 instead sorts the canonical safe representatives and
unranks directly into that list. Its target distribution is
\[
  \Pr_{\mathrm{class}}[O]=\frac1{|\mathcal C/{\cong}|}.
\]

### Exhaustive census and exact probabilities

- **[EMPIRICAL: every \(0\leq a,b<127\) and every
  \(1\leq u<127\)]** Of the \(127^2=16,129\) coefficient pairs, 16,002 are
  nonsingular. They form 258 isomorphism classes with orbit histogram
  \(\{21:6,63:252\}\).
- **[EMPIRICAL: the fixed A002 safety profile at \(p=127\)]** The
  predicate accepts 4,179 coefficient encodings in 67 classes. Exactly one
  safe class has orbit size 21 and the other 66 have orbit size 63.
- **[EMPIRICAL: canonical safe-class table]** The first class key is
  \((0,13)\), the last is \((3,123)\), and the checked-in CSV contains one
  row for each of the 67 ranks.

**[PROVED]** Given the exhaustive census, the exceptional class receives
\[
  \frac{21}{4179}=\frac1{199}
\]
under coefficient-uniform sampling, while every generic safe class receives
\[
  \frac{63}{4179}=\frac3{199}.
\]
Class-uniform sampling assigns every class \(1/67\).

**[PROVED]** Given the same counts, the exact total-variation distance is
\[
\begin{aligned}
 d_{\mathrm{TV}}
 &=\frac12\left(
   \left|\frac1{199}-\frac1{67}\right|
   +66\left|\frac3{199}-\frac1{67}\right|
 \right)\\
 &=\frac{132}{13333}.
\end{aligned}
\]

### Exact rejection/unranking kernel

**[CONDITIONAL: SHAKE256 blocks are independent uniform strings]** For
\(N=67\), A004 chooses a byte width \(w\), sets
\(L=2^{8w}-(2^{8w}\bmod N)\), hashes the domain-separated tuple
(beacon, sample index, component, retry), rejects values at least \(L\), and
returns the accepted value modulo \(N\). Accepted values are uniform on a set
whose size is a multiple of \(N\), so every rank is output with probability
\(1/67\).

**[PROVED]** The sorted canonical table makes unranking total and
deterministic for ranks \(0,\ldots,66\). No first-passing counter or
coefficient-orbit multiplicity remains after the rank is fixed.

**[PROVED]** If the future beacon, sample index, profile, code version, and
publication rule are fixed and the beacon cannot be selected, restarted, or
suppressed, the designer has one screenable execution: \(M=1\) and \(b=0\).
Allowing any of those branches must instead be charged in the accounting
contract.

### Minimax proof

**[PROVED]** For any probability distribution \(\mu\) on \(N\) classes,
\[
  1=\sum_C\mu(C)\leq N\max_C\mu(C),
\]
so \(\max_C\mu(C)\geq1/N\). Equality forces every summand to equal \(1/N\).
Therefore the uniform distribution is the unique minimizer. At \(N=67\), the
A004 class kernel attains the unique optimum \(1/67\).

### Reproducible artifacts and validation

- **[EMPIRICAL: exhaustive A004 run, Python 3.13.4]**
  `problems/P5.3-rigidity-formalization/code/class_uniform_kernel.py` writes
  the exact JSON summary and the 67-row canonical-class CSV.
- **[EMPIRICAL: six A004 regression tests]**
  `problems/P5.3-rigidity-formalization/code/tests/test_class_uniform_kernel.py`
  checks the exact counts and rational masses, every explicit scaling orbit,
  first/last ranks, subgroup points, deterministic domain separation, and the
  fixed \(p=31\) smoke CLI.
- **[EMPIRICAL: deterministic replay on 2026-07-08]** The checked-in files are
  `problems/P5.3-rigidity-formalization/data/class_kernel_b7_20260708.json`
  with SHA-256
  `1BA019A7DA47C2FB64764B3D9A79680C7CB2904D6AD9062899069689AEB03F15`
  and
  `problems/P5.3-rigidity-formalization/data/class_kernel_b7_20260708.csv`
  with SHA-256
  `EDC4C7875E2CE7A0AB0F44529BD65A99D35ADF5A57C8E485070B983DBFD382A9`.

### Resolution boundary

> **Resolution.** P5.3/Q015 is closed for this explicitly fixed toy field, safety
> profile, equivalence projection, weakness criterion, and beacon model.
> Changing any of them defines a new accounting contract and requires a new
> proof or census. No production-size parameters were computed, and this is
> not a production curve recommendation. A production profile would be new,
> separately authorized work under the scaffold's scope limit. Logged as
> P5.3/A002–A004. Blocking: no.

## P3.3/Q099 - Can validated KLPT reproduce the exact pure-power gap on matched ideals?

[EMPIRICAL: 108 near-$p$ ideals in 12/20/28-bit bands] Norm-aware LLL found
the certified exact shortest vector on every P3.3 instance, with at most 80
nonzero coefficient tuples in any exact certificate.

[EMPIRICAL: 70 near-$p$ ideals, $7\le p\le223$] Exact powers of 2 and 3 and
5-smooth representatives all occurred by normalized norm $p$.

[PROVED] P3.3/A004 resolves the former target-solver gap with inverse-Gram
boxes and exact quadratic coordinate elimination.

[EMPIRICAL: 108 near-$p$ ideals in 12/20/28-bit bands, targets through $4p$]
All least $2^e$ and $3^e$ norms were found without censoring. Overall median
penalties over unconstrained SVP were 222.64 and 168.23; the 28-bit medians
were 2476.82 and 2622.49. Every optimum was below $p^{1.013}$.

> **Gap.** No KLPT implementation has been run on these instances. Resolving
> the remaining gap requires a separately validated basic-KLPT implementation
> and a matched comparison of its output with A004's exact shaped optimum.
> Blocking: no for the completed toy structural verdict; yes for a measured
> end-to-end KLPT-gap verdict. Logged as P3.3/Q099.

## P5.4/Q012 - Does RFC 9380 F.2.1.1 need a zero-numerator correction?

[PROVED] On the admissible toy fixture $p=11$, $E:y^2=x^3+x+1$, and $Z=6$, the generic `sqrt_ratio` procedure in RFC 9380 Appendix F.2.1.1 returns `isQR = False` for numerator zero even though RFC Section 4 defines zero as square. This makes the unmodified Appendix F.2 SSWU path return the off-curve pair $(0,0)$ for $u\in\{0,3,8\}$. The derivation and regression are in P5.4 `NOTES.md` and `code/tests/test_rfc_maps.py`.

> **Gap.** I do not know whether the RFC authors intended an unstated nonzero condition on the SSWU numerator or whether Appendix F.2.1.1 needs `isQR = (tv5 == 1) OR (u == 0)`. Resolving this requires confirmation against the derivation or authors and, if confirmed, submission of a technical erratum. Blocking: no for the toy implementation, which applies the arithmetic OR correction. Logged as P5.4/Q012.

## P1.6/Q008 - Which recent local-field lifting paper was intended in P1.6?

**Status:** open, nonblocking bibliographic identification.

[EMPIRICAL: supplied P1.6 prompt and checked local bibliography] The prompt
mentions recent local-field and hyperelliptic lifting work without a title,
author list, or identifier, and the recorded audit did not identify one unique
source.

> **Gap.** Resolving this requires a
> targeted literature search from an additional keyword, title fragment, or
> cited survey; no claim in the current P1.6 analysis depends on it.
> Blocking: no. Logged as P1.6/Q008.

## P4.2/Q010 - Which cycle-level rho did P4.2 intend?

[PROVED] With the standard per-curve value
\(\rho_i=\log(p_i)/\log(r_i)\), a prime-order 2-cycle has
\(r_i=p_{i+1}\), and Hasse's bound makes \(\rho_{\max}<2\) automatic for
distinct field primes at least 5. The independently verified MNT example over
fields 37 and 43 has \(\rho_{\max}=1.041618836729\).

> **Gap.** The prompt treats \(\rho<2\) as an open target, so it may intend a
> security-normalized or polynomial-family metric. Resolving this requires an
> explicit alternate definition. Blocking: no; P4.2 records both per-curve
> values and uses their maximum until clarified. Logged as P4.2/Q010.

## P1.2/Q001 — Resolved for translate-probe search

**Status:** resolved in the explicitly stated translate-probe model.

[PROVED] The implemented lexicographic scan has a worst case of $s^2$ pair
tests and is not polylogarithmic at square-root-scale $s$; this does not exclude
a different algorithm that exploits the interval condition.

[PROVED] P1.2/A009 defines the translate-probe model containing the implemented
pair scan and proves success at most $T|\mathcal F|/r$ after $T$ probes, for
fixed, failure-adaptive, and randomized schedules. Candidate A therefore needs
$T\ge p^{1/2-o(1)}$ probes for inverse-polylogarithmic success in this model.

[PROVED] The proof covers algorithms whose only target interaction is a
sequence of tests $R-a\in\mathcal F$, even when the shifts are randomized or
chosen adaptively from earlier failures. It does not cover algorithms that
read field coordinates and solve algebraic relations.

> **Resolution.** P1.2/Q001 is closed; no further pair-scan scaling experiment
> can reopen it. A counterexample must violate the translate-probe model, in
> which case it belongs to P1.2/Q004.

## P1.2/Q002 — What is the exact canonical-height membership predicate?

**Status:** open, but only as an optional Candidate-D continuation for a
corrected resource-bounded variant.

[PROVED] A005's tested predicate chooses the centered integral lift of $x$ and
requires an integral point on one fixed lift $\widetilde E/\mathbb Q$. This is
a decidable denominator-one subset, not the full set of rational preimages of
bounded canonical height.

[EMPIRICAL: the recorded 16-, 18-, and 20-bit curves] The denominator-one
proxy produced factor-base sizes 0, 0, and 2, so it was too sparse to provide
non-negligible three-term decomposition success in that range.

> **Gap.** A full proposal must specify a uniform lift constructor
> `Lift(p,E)`, a height threshold $H(p)$, which rational points above a residue
> class are admissible, and whether membership means existence of any
> admissible lift or selection of one canonical lift. It must then prove the
> bit complexity of deciding that predicate and charge all lift construction,
> search, advice, and storage resources. Blocking: no for literal P1.2; yes
> only for claiming Candidate D satisfies corrected Variant S. Logged as
> P1.2/Q002.

> **Closure criterion.** Close this question with either (i) an exact uniform
> predicate plus a polynomial-in-$\log p$ membership proof, followed by the
> required size and decoder analysis, or (ii) an impossibility theorem for a
> precisely named class of lift-and-height predicates. Repeating the
> denominator-one proxy does not address the gap.

## P1.2/Q003 — Did P1.2 intend square-root size rather than standard L-notation?

**Status:** needs a specification choice; it does not block the negative
resolution of the literal statement.

[PROVED] Under standard generalized L-notation, fixed-$m$ conditions (1) and
(3) are mutually inconsistent by the support-size proof in P1.2 `CLAIM.md`.

[PROVED] Merely changing the bound to $p^{1/2+o(1)}$ while charging only
online time creates the opposite problem: A008's $O(p^{1/3})$ radix base and
$p^{1+o(1)}$ target table give success one with polylogarithmic nonuniform
lookup.

> **Decision required.** Select Variant S (square-root size, fixed $m=3$, and
> $p^{o(1)}$ total input-specific resources) or Variant L (standard
> $L_p[1/2,c]$, growing $m$, and fixed-constant $L_p[1/2,C]$ offline
> resources) from P1.2 `CORRECTED_VARIANTS.md`. Mixing the original size
> bound, fixed length, and uncharged preprocessing is not a third coherent
> interpretation. Blocking: no for the statement as written; yes for naming
> the intended corrected research problem. Logged as P1.2/Q003.

> **Closure criterion.** This is closed only by an explicit human choice of
> Variant S, Variant L, or another fully resource-accounted statement.

## P1.2/Q004 — Can coordinates beat the translate-probe lower bound?

**Status:** open only if corrected Variant S is selected.

[PROVED] A009 does not cover a decoder that uses $x(R)$ or other coordinate
relations to choose target-dependent shifts or solve the summation equation.
A008's target-indexed table is also outside the probe model but is excluded
from Variant S by its linear-size advice and preprocessing.

[CITED] Petit–Kosters–Messeng 2016 give a smooth-subgroup coordinate
predicate with a low-degree composition chain, but leave the resulting
Gröbner complexity open. [EMPIRICAL: $p=17,257,65537$] P1.2/A010 validated
that predicate and found that both tested encodings completed only at $p=17$
within a five-second SymPy limit. This does not establish a lower bound.

> **Gap.** I do not know whether the integer-$x$ base or the smooth-subgroup
> base admits a succinct, uniform, coordinate-aware polylogarithmic
> decomposition algorithm under Variant S, or whether such algorithms obey a
> stronger lower bound. Resolve this with an explicit algorithm and total
> resource proof, or a lower bound in a model that exposes field coordinates
> without permitting target-indexed advice. Blocking: no for the literal
> P1.2 audits; yes for Variant S. Logged as P1.2/Q004.

> **Closure criterion.** Close P1.2/Q004 with either (i) a fixed uniform
> coordinate-aware decoder, a proof of all Variant-S resource bounds, and a
> growing-family success analysis, or (ii) a lower bound in a coordinate-aware
> model that still excludes target-indexed advice. Generic pair scans, a
> complete target table, or a Gröbner timeout do not meet either criterion.

## P1.5/Q004 - Can a CM point subgroup map computably into a class group?

[CONDITIONAL: ERH and factor-base decomposition of represented inputs]
Imaginary-quadratic class-group relations give a subexponential target route.

[PROVED] P1.5/A003 excludes annihilator ideals, cyclic-kernel labels, and
kernel-isogeny quotients because they are constant on every nonzero generator
of the same prime-order subgroup. For $q\ge2^{21}$ and $r\ge q/2$, an explicit
class-number bound also makes the curve's own endomorphism class group too
small.

[PROVED] P1.5/A004 excludes the standard $\mathbb Q(i)$ ray-level route:
modulus $r$ has no $r$-torsion, while the modulus-$r^2$ principal units move
the $r$ lifts above one source point rather than the $r$ source points.

[PROVED] P1.5/A007 excludes every point-to-class construction that accesses
the source only through generic group operations. P1.5/A008--A010 further show
that an affine piecewise-rational evaluator with $B$ branches and common pole
degree $D$ satisfies the exact overlap obstruction
$\lceil r/B\rceil(\lceil r/B\rceil-1)\le2D(r-1)$, hence
$\max(1,D)B^2\ge r/4$.

[PROVED] P1.5/A014 classifies the base of the target. Finite and local rings
have trivial Picard groups; global function-field class groups are Jacobians
or generalized Jacobians; only a global number-field order gives a genuinely
distinct class-group target.

[PROVED] P1.5/A015 gives the exact evaluator sandwich. For a nonzero
homomorphism $\phi$ and a target DLP algorithm,
$$
T_{\rm src}\le T_{\rm eval}+T_{\rm tgt}+(\log r)^{O(1)},
$$
while source DLP followed by exponentiation evaluates $\phi$. Thus target
construction and target size do not supply the missing coordinate evaluator.

[PROVED] P1.5/A016 restricts the checked Hafner--McCurley route, writing
$n=\lceil\log_2r\rceil$ and $B=\log_2|\Delta|$, to
$$
2n-O(\log n)\le B=o(n^2/\log n).
$$

[CITED] Buell (1977), Soleng (1994), Buell--Call (2016), Gillibert (2018),
and Blum--Choi--Hoey--Iskander--Lakein--Martinez (2022) give genuine
point-to-class homomorphisms or specializations for rational or algebraic
points over number fields.

[EMPIRICAL: bounded primary-source search on 2026-07-10] P1.5/A018 found no
direct homomorphism from $E(\mathbb F_q)[r]$ to one fixed number-field class
group. The checked finite-field CM results instead use ideal classes acting on
oriented curves, the reverse direction. This is a search result, not a
nonexistence theorem.

[PROVED] P1.5/A017 rules out the direct residue-coordinate substitution into
the Buell form. Canonical integer representatives produce discriminant
$\mathcal D+k_Qp$, varying with $Q$, so the outputs do not lie in one class
group.

[PROVED] P1.5/A019 constructs an ideal class of exact prime order $r$ in
discriminant $1-4\cdot2^r$, but that target description has $\Theta(r)$ bits
and violates the polynomial input budget.

[EMPIRICAL: every negative order discriminant with $|\Delta|\le200000$,
13 primes $3\le r\le43$] P1.5/A020 found much smaller toy targets: every
least qualifying discriminant had class number exactly $r$, with
$0.684711\le|\Delta|/r^2\le2.555556$. Exhaustive class-number search does not
give a uniform growing-family constructor.

[EMPIRICAL: bounded prescribed-order literature search on 2026-07-10]
P1.5/A021 found exact-order existence theorems based on $n$-th-power
discriminant families, but no checked uniform polynomial-bit construction.
P1.5/A004 supplies a succinct ray target without solving this ordinary-class
construction gap, but the next result shows that the ray alternative has a
different, stronger obstruction.

[PROVED] P1.5/A022 sharpens the ray alternative. The explicit logarithm
$1+rz\mapsto z\bmod r$ makes any nonzero ray principal-unit evaluator itself
polynomial-time equivalent to source ECDLP: from $Q=xP$, one nonzero output
coordinate divided by the corresponding coordinate for $P$ is $x$. Thus the
ray branch has no intermediate subexponential regime; a positive evaluator
would already be a polynomial-time ECDLP algorithm.

[CITED] P1.5/A023 reconciles the rational package with discrete-logarithm
interpolation. Coppersmith--Shparlinski's arbitrary-subset bound already
contains the quadratic overlap mechanism, so the $B^2$ scale is not a new
mechanism. The checked interpolation results do not cover rational maps from
an elliptic subgroup into arbitrary faithfully represented affine targets,
and their character-sum refinements do not improve the exponent for an
adversarial branch partition.

[PROVED] P1.5/A024 fixes one finite valuation-mediated factor-base model for
ordinary reduced-form outputs. A nonzero evaluator in that model satisfies
$$
C+\sum_j\log_2(h_j+1)\ge\log_2r,
$$
where $C$ counts binary comparisons and $h_j$ bounds the bit length of the
$j$-th valuation operand. This rules out low-observation polynomial-height
recipes, but remains compatible with polynomial-length valuation programs and
does not cover direct raw-coordinate form construction.

> **Gap.** [CONJECTURE] I do not know a uniform polynomial-time nonzero
> evaluator from a prime-order elliptic point subgroup into a succinct
> ordinary number-field class target that avoids first solving the
> source DLP. Outside A024's VFB lower bound, it may still use a
> polynomial-length valuation transcript, direct raw-coordinate form
> synthesis, or another non-generic operation and cross the proved
> degree/branch bounds. For an ordinary class group it must additionally
> provide a uniform certified order-$r$ target inside the size window. The
> ray option is isolated separately by A022 as polynomially equivalent to
> source DLP. Blocking:
> no. Logged as P1.5/Q004 and P1.5/A001.

> **Closure criterion.** Close P1.5/Q004 positively only with one infinite
> uniform family, polynomial-size setup, a polynomial-time evaluator on
> ordinary finite-field point encodings, a complete homomorphism and
> nonzero-image proof, and an end-to-end $\exp(o(\log r))$ target DLP bound.
> Close it negatively only with a lower bound covering the remaining
> coordinate/lift/valuation programs, not merely generic groups or rational
> maps of bounded degree. The present record does not meet either criterion.

## P1.4/Q002 — How can the explicit basic-GHS cover be built without SageMath or Magma?

> **Gap.** P1.4 computes the exact Frobenius-span genus invariant but does not construct the descended function field, curve, or divisor map. Resolving it requires implementing the fixed field of the Artin–Schreier compositum, starting with a genus-2 or genus-3 case.
> Blocking: no. Logged as P1.4/Q002.

[PROVED] P1.1/A004 resolves the odd-degree magic-number-one boundary case in
pure Python: the fixed field has genus one and the conorm/norm map is an
explicit Frobenius trace on a binary elliptic curve. P1.4/Q002 remains open only
for the genuinely higher-genus construction stated above.

## P1.4/Q003 — When does the measured low genus produce an actual DLP speedup?

> **Gap.** The P1.4 census has no elliptic-curve subgroup orders, explicit Jacobians, or measured DLP costs. Resolving it requires an end-to-end toy descent and a direct comparison with Pollard rho on the same subgroup.
> Blocking: no. Logged as P1.4/Q003.

[EMPIRICAL: one $\mathbb F_{2^{10}}/\mathbb F_{2^2}$ fixture] P1.1/A004 now
provides an explicit genus-one auxiliary Jacobian and transferred order-three
DLP, but this degenerate case supplies no meaningful speedup comparison. The
higher-genus performance question remains open.

## P2.2/Q003 — Can the prime-order $q$-SDH separation be extended beyond GR-BB?

[CITED] Lu and Zhandry rule out fully black-box generic-representation/type-safe
reductions, including the algebraic-reduction setting, from $q$-SDH to true
fixed-size prime-order assumptions at explicit dimension thresholds.
[Lu–Zhandry 2024, §§1.4, 5–6]

[PROVED] P2.2/A003 resolves the representation-uniform subcase: one
fully-black-box standard-oracle machine whose guarantee holds pointwise over
every group implementation is already a GR-BB reduction.  P2.2/A004 shows why
random relabeling cannot transfer a guarantee asserted only for one concrete
representation.

[PROVED] P2.2/A005 closes the simplest efficient-representation workaround.
A polynomial-seed sparse encoding has only exponentially many possible tables,
so a possibly inefficient adversary can enumerate every seed and distinguish
it from the information-theoretic random injection.  Finite-wise independence
requires a query bound, while a PRP adds a computational restriction.

[PROVED] P2.2/A006 resolves a further fixed-representation subcase without
random relabeling.  If a reduction introduces at most $s_1$ unexplained valid
labels in the $q$-SDH source, the enlarged trace has dimension $n_1+s_1+1$
and gives an impossibility under fixed-assumption hardness when
$n_1+s_1<q-1$.  Pairing outputs do not enlarge this source trace; the safe
quadratic condition $\binom{n+s+2}{2}+t<q$ applies to broader target-valued
bilinear $q$-type games.

[PROVED] P2.2/A007 rules out one tempting shortcut: a small constrained-label
density $\delta$ in the structured generic-group model does not imply a small
freshness budget.  Its density term controls a random-hybrid probability, and
its group-query count does not charge free structured-label computation.

> [PROVED] **Residual gap.** No impossibility or positive reduction is established for
> a representation-dependent reduction capable of introducing linearly many
> unexplained source labels as $q$ grows, nor for a reduction that uses the code
> of the $q$-SDH adversary.  Resolving the first branch requires controlling or
> exploiting that high-dimensional native-label supply; density alone is
> insufficient.  Resolving the second requires a non-fully-black-box
> construction or a stronger meta-reduction.
> Blocking: no. Logged as P2.2/Q003.

[PROVED] **Closure criterion.** The representation-dependent branch closes if
one proves that every reduction in a precisely named concrete-operation class
has source-label trace rank below $q-n_1-1$, or instead supplies a positive
constant-size reduction whose native rank reaches the required dimension.  The
code-using branch closes only through an explicitly non-black-box construction
or a meta-reduction whose scope includes code access.

[PROVED] **Do not repeat.** Random relabeling (A004), finite-seed substitution
(A005), and density-to-count transfer (A007) have distinct recorded
counterarguments and are not open approaches without an additional invariant.

## P2.1/Q005 - Can a polylog-smooth auxiliary curve be constructed uniformly?

[CITED] Maurer--Wolf's general prime-order reduction assumes an auxiliary
curve over $\mathbb F_r$ whose known order has largest prime factor
$(\log r)^{O(1)}$; their Hasse-interval result supplies non-uniform side
information, not a construction (Maurer--Wolf 1999).

[PROVED] A concrete sufficient CM statement is: for some fixed $C,K$, every
prime $r$ admits a negative fundamental discriminant $D$ and integers $t,v$
with

$$
 |D|\le(\log_2r)^K,\quad 4r=t^2-Dv^2,\quad
 P^+(r+1-t)\le(\log_2r)^C.
$$

[PROVED] Given such an integer witness, discriminant enumeration, Cornacchia,
and smoothness testing take randomized expected polynomial time in $\log r$.

[CONDITIONAL: a certified class-polynomial implementation polynomial in
$|D|$ and $\log r$] The witness yields the needed auxiliary curve; Enge 2009
gives the appropriate sharp class-polynomial complexity with an explicit
floating-point precision heuristic.

[EMPIRICAL: 4,096 descending 60-bit primes] Every tested prime met the cubic
toy condition $C=K=3$, but only 3,635 met $C=3,K=2$; this is finite evidence,
not a universal theorem.

[CITED] Li 2025 proves an infinite prime family with
$P^+(r-1)>r^{0.679}$, so the full multiplicative auxiliary group is not a
uniform replacement.

[PROVED] Batyrev--Tschinkel's Frobenius determinant formula, fixed-progression
prime density, CRT, and Linnik strengthen this obstruction: for every fixed
$D$, an infinite prime family has a polynomially large factor simultaneously
in every full algebraic torus of dimension at most $D$.  This does not
classify selected subgroups or abelian varieties.

[PROVED] Chevalley decomposition, split unipotent radicals, and Lang's theorem
further show that every full bounded-dimensional smooth connected
commutative group with a nonzero affine part is obstructed; the only remaining
full connected class is pure abelian varieties.  A public-coin injectivity
lemma also rules out every polylog-smooth selected subgroup of a one-
dimensional torus when recoverable encoding must succeed nonnegligibly on
every input.  Higher-dimensional selected subgroups remain open.

[CONDITIONAL: Riemann Hypothesis] The dimension-two prescribed-order interval
and Younis's $\theta=3/4$ theorem imply that a polylog-smooth full abelian-
surface order exists for every sufficiently large prime.  This does not close
Q005: no checked theorem finds such an order and constructs an explicit
strongly algebraically defined surface in polynomial time.  Standard genus-
two CM has exponential worst-case complexity.  The heuristic construction in
the same paper prescribes the curve's point count rather than its Jacobian
order and therefore does not address this gap.  Finding the smooth order and
realizing its Weil polynomial are the two explicit remaining algorithms in
the abelian-surface branch.

[PROVED] Boneh's CRT-decoding finder does not close the first gap.  At interval
width $X^{3/4}$ and smoothness threshold $s=(\log X)^K$ with fixed $K>1$,
its irreducible decoding condition would require
$\log(X^{3/4})=O((\log X)^{2-K})$, which is false.  The decoder reaches the
full-order interval only near strongly $c\log X$-smooth values with
$1\le c\le4/3$; those values number only $X^{o(1)}$ globally and are not
supplied by Younis's theorem.

[PROVED] Bounded-support exponent-vector enumeration also cannot close the
finder gap.  For every fixed support bound and polylogarithmic factor base,
the polynomially many possible products cover only
$X^{1/4}(\log X)^{O(1)}$ prime centers at the surface interval scale, versus
$\Theta(\sqrt X/\log X)$ available prime centers in a dyadic range.
Unrestricted support gives polynomially many logarithmic items, but a direct
safe rounding must resolve width $X^{-1/4}$ and therefore creates an
exponentially large numerical subset-sum target.  Checked pseudopolynomial
and low-density lattice theorems supply no polynomial-time guarantee there;
this is not a lower bound against every specialized logarithmic algorithm.

[EMPIRICAL: r=251,1019,4091,16363] Every integer in the central interval of
half-width $\lfloor r^{3/2}\rfloor$ had an ordinary Weil polynomial whose
isogeny class contains a genus-two Jacobian under the exact HNR criterion.
This includes every tested cubic-log-smooth order.

[PROVED] HNR supplies existence, not an equation.  No checked algorithm takes
the resulting general degree-four Weil polynomial to one explicit Jacobian
in polynomial time: CM has exponential worst cases, isogeny walks require a
seed already in the target class, and abstract rational-point group data does
not instantiate Maurer--Wolf's recoverable algebraic embedding.

[PROVED] In an explicitly iid Hasse-order oracle, the exact optimal adaptive
$q$-query success probability is $1-(1-\alpha)^q$.  Actual curve-order maps
are structured, so this is not a lower bound for every algebraic construction.

> **Gap.** I do not know how to prove this sufficient condition for every
> prime for any fixed $C,K$, how to replace it with another uniform curve
> construction, or how to prove an infinite family obstructing all admissible
> auxiliary curves or constant-rank algebraic groups.  The known infinite
> families rule out full bounded-dimensional connected groups with an affine
> part and polylog-smooth selected subgroups of one-dimensional tori in the
> public-coin recoverable-encoding model, but not pure abelian varieties or
> higher-dimensional selected subgroups.
> Resolving it requires a theorem on correlated smooth values of the principal
> CM norm-equation orders, a specialized polynomial-time finder for the
> structured logarithmic interval problem, a different family with proved
> coverage, or a lower bound in a specified construction model. Blocking: yes
> for P2.1's full reduction. Logged as P2.1/Q005.

## P3.4/Q011 — Is there a complete criterion for all higher-dimensional leakage attacks?

[PROVED] P3.4 supplies a necessary-and-sufficient invocation test only for
Robert's dimension-8 template and the Castryck--Decru/Maino--Martindale surface
templates, relative to a supplied auxiliary-witness record.

> **Gap.** I do not know a theorem proving that every Kani-embedding or
> higher-dimensional key-recovery attack must consume the same rank-two
> torsion restriction, known-degree data, or one of the encoded auxiliary
> decompositions. Resolving this requires a formal attack model covering
> derived leakage, arbitrary fixed dimension and polarization, followed by
> either a completeness theorem or a counterexample attack outside the model.
> Blocking: yes for the original broad necessary-and-sufficient statement; no
> for the scoped published-template checklist. Logged as P3.4/Q011 and P3.4/A001.

## P3.2/Q012 — Does the logarithmic phase-state lower bound extend to a structured action oracle?

[PROVED] P3.2 proves an `Omega(log N)` lower bound when each query returns one independent standard hidden-shift phase qubit.

> **Gap.** The proof does not cover an arbitrary coherent call to a structured CSIDH action circuit. Resolving this requires fixing that oracle's input/output registers and either reducing every such query to the phase-state interface or constructing a counter-algorithm that uses the extra structure. Blocking: yes for unrestricted Task 2; no for the conditional theorem. Logged as P3.2/Q012.

## P3.2/Q013 — What finite-size constant does the full collimation sieve have under one physical model?

[EMPIRICAL: P3.2 fixed-batch schedule, (24\le n\le96)] The current fit gives (c=2.68677), but its bootstrap interval omits block-rounding and schedule-model error.

> **Gap.** The repository has not implemented Peikert's full phase-vector collimation simulator or calibrated a fault-tolerant oracle circuit. Resolving this requires reproducing one published sieve table from the authors' algorithm, adding the oracle circuit and error-correction compilation, then fitting a range where discretization residuals are controlled. Blocking: yes for a universal or physically calibrated (c); no for the parameterized calculator. Logged as P3.2/Q013.

## P4.1/Q009 — Resolved: can the finite SexTNFS model be independently validated across families?

[EMPIRICAL: 1,024 exact BLS12 samples, RNG seed 20260722] P4.1 reproduces the Barbulescu–Duquesne BLS12 norm inputs and obtains 131.789 bits versus 131.8 published without refitting the BN-calibrated prefactor. The exact nested-resultant records and uncertainty intervals are checked in. Resolved in P4.1/A001.

## P4.1/Q010 — Resolved: does KSS16 admit a prime toy fixture below the 60-bit field ceiling?

[PROVED] An analytic magnitude bound reduces every seed with $p<2^{60}$ to `[-255,255]`. Exhaustive evaluation leaves eight integral positive rows, and exact factorizations show that no row has both $p$ and $r$ prime. Resolved in P4.1/A001.

## P4.1/Q027 - Which integer coefficient bound produced the published BLS24 norm row?

[CITED] Barbulescu--Duquesne Section 7.2.2 prints `A=9` and norms 1295/1460, while Section 4.2 describes coefficients uniform on `[-A,A]`. The authors' surviving Python sampler instead calls inclusive `randint(-A,A+1)` and therefore draws on `[-A,A+1]`.

[EMPIRICAL: P4.1 exact samplers] With printed `A=9`, 512-sample runs under those two conventions produce mean norm bits 1241.572/1455.863 and 1262.322/1457.418, neither reproducing the printed row. A preregistered 128-sample public-code run with sampling bound 10 gives 1295.867/1461.000, placing both printed values inside the 95% intervals.

> **Gap.** The surviving public artifacts do not record whether the historical optimization rounded an internal real bound to 10 before sampling. Recovering the original execution record or an author confirmation would resolve this. Blocking: no for P4.1's transparent four-family comparison, which reports the literal runs and the sensitivity separately. Logged as P4.1/Q027.

## P5.2/Q020 - Resolved in the sequential evaluator model: can a non-unit small-CM endomorphism yield a growing cheap orbit?

**Status:** resolved in the sequential successor/comparison model.

[CITED] Efficient CM endomorphisms act as scalar multiplication by a quadratic-polynomial root on an invariant prime-order subgroup (Gallant-Lambert-Vanstone 2001).

[PROVED] P5.2/A003 proves that least-label canonicalization on an opaque length-$m$ cycle needs exactly $m-1$ successor evaluations in the sequential successor/comparison model. It also proves that an exponent-returning canonicalizer reduces ECDLP to $q+1$ canonicalizer calls where $q=(r-1)/m$. The explicit model requested here is therefore resolved, while richer access is separated into P5.2/Q024.

> **Resolution.** P5.2/Q020 is closed in its named model. Richer batched or
> exponent-free access is not a counterexample to that theorem and was routed
> to P5.2/Q024. Blocking: no.

## P5.2/Q024 - Resolved for standard coefficient-tracking rho: can exponent-free or batched non-unit orbit access support rho?

**Status:** resolved for standard formal coefficient-tracking rho.

[PROVED] A correct quotient-rho collision equation ordinarily needs the exponent that transforms each point's linear coefficients, and P5.2/A003 shows that a cheap exponent-returning normalizer with a small orbit quotient already yields an ECDLP algorithm.

[PROVED] P5.2/A004 proves that nontrivial scalar-orbit equivalence is not an additive congruence, so addition does not descend to the orbit set. In the standard formal coefficient model, canonicalization must return the orbit multiplier or equivalent orientation information; the A003 reduction then solves ECDLP in $q+1$ calls without needing the multiplier's discrete logarithm. A multiplier-returning batch gives the same reduction in one batch. Nonlinear use of unoriented collision constraints is separated into P5.2/Q025.

> **Resolution.** P5.2/Q024 is closed for the standard rho model. A nonlinear
> algorithm using unoriented subgroup-membership constraints lies outside the
> model and belongs to P5.2/Q025. Blocking: no.

## P5.2/Q025 - Can nonlinear unoriented orbit collisions beat square-root ECDLP?

[PROVED] An unoriented collision between states with coefficients $(a,b)$ and $(c,d)$ gives the constraint $(a+bs)/(c+ds)\in H=\langle\lambda\rangle$, or equivalently one of up to $|H|$ linear equations indexed by the unknown orientation multiplier.

> **Gap.** I do not know whether several such subgroup-membership constraints can be combined in sub-$\sqrt r$ time when $H$ has index two or three, as in the measured $D=-7$ cases, without reconstructing each orientation. Resolving this requires a solver with known-log tests and full group/field cost accounting, or a lower bound in a model with multiplicative-character tests. Blocking: yes for excluding nonlinear orbit-collision algorithms. Logged as P5.2/Q025.

## P1.3/Q022 - Are quadratic Semaev field equations automatically nonredundant?

[PROVED] P1.3 proves $\operatorname{sd}_{\mathrm{grevlex}}\le q$ for every
odd-prime-power quadratic non-base-target system and proves equality whenever
$(G_0,G_1,x^q-x,y^q-y)$ strictly contains the core ideal $(G_0,G_1)$.

[EMPIRICAL: 397 verified-root variants over $q=5,7,11$ and exhaustive actual
$q=5$] Every checked system has nonredundant field equations.

> **Gap.** I do not know whether nonsingularity and a non-base target force at
> least one of $x^q-x,y^q-y$ outside the core ideal for every odd prime power.
> Resolving this requires a geometric proof that the core scheme has a
> non-$\mathbb F_q$ point or an exact counterexample where both field equations
> reduce to zero. Blocking: yes for removing the final hypothesis from the
> quadratic equality theorem; no for the unconditional upper bound. Logged as
> P1.3/Q022.

## P1.3/Q023 - Does the constant-degree mutant family extend beyond $n=m=2$?

[PROVED] P1.3's quadratic proof uses a four-element degree-at-most-4 core
basis and cubic field-equation remainders.

> **Gap.** No analogous constant-degree replacement family is proved for
> $n=3,m=2$ or $m>2$. Resolving this requires an exact core-basis/remainder
> analysis in the next dimension, followed by either a parameter-uniform
> symbolic certificate or the smallest counterexample. Blocking: yes for
> extending the new upper-bound method toward the full $q,n,m$ problem.
> Logged as P1.3/Q023.
