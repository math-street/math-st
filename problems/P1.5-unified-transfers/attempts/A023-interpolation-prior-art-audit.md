---
attempt: A023
status: folded-into-A001
---
# A023 - Reconcile cryptographic interpolation and homomorphism prior art

## Question and checked boundary

- [PROVED] This audit asks whether the five items called the
  repository-original synthesis in `RATIONAL_TRANSFER_REVIEW.md` follow from
  the cryptographic polynomial-interpolation literature omitted by its first
  search, and whether the character-sum machinery improves the adversarial
  piecewise exponent from $B^2$ toward $B$.
- [EMPIRICAL: bounded primary-source reconciliation on 2026-07-20] The checked
  line is Coppersmith--Shparlinski (2000), Winterhof (2002),
  Lange--Winterhof (2002), Kiltz--Winterhof (2006), Verheul (2001/2004),
  Moody (2008/2009), and Koblitz--Menezes (2007).
- [CITED] The requested "Meidl--Winterhof, Polynomial Interpolation of the
  Discrete Logarithm" citation conflates two papers. The paper with that title
  is sole-authored by Arne Winterhof; the separate Meidl--Winterhof paper is
  "A Polynomial Representation of the Diffie--Hellman Mapping." The local
  reference record preserves both facts.

## Closest interpolation theorems

- [CITED] Coppersmith--Shparlinski Theorem 1 is the closest quantitative
  predecessor. If $f\in\mathbb F_p[X]$ agrees with the discrete-logarithm
  function on arbitrary $S\subseteq\mathbb F_p^\times$, then

  \[
  \deg f\ge \frac{|S|(|S|-1)}{2(p-2)}. \tag{A023.1}
  \]

  The proof chooses a nonidentity quotient represented by many ordered pairs
  of $S$, forms a translated defect, and zero-counts it. This is the
  multiplicative finite-field predecessor of the same-branch difference
  proof in Theorem 4.1.
- [CITED] Coppersmith--Shparlinski Theorem 3 also treats algebraic relations
  $F(x,\operatorname{ind}x)=0$, but its total-degree lower bound is of order
  $|S|/\sqrt p$. Winterhof extends most of this prime-field line to
  arbitrary finite fields.
- [CITED] Lange--Winterhof's elliptic result concerns a polynomial in the
  $x$-coordinate that returns a digit encoding of the scalar $n$ on a set
  of exponents dense in an interval. Its linear-in-interval-length conclusion
  loses terms for missing samples and digit carries. Their arbitrary-subset
  XTR and multiplicative-subgroup results return to a
  $|S|(|S|-1)/(\text{ambient size})$ bound, with additional trace or carry
  factors.
- [CITED] Kiltz--Winterhof gives reductions and interpolation lower bounds for
  polynomially transformed Diffie--Hellman and discrete-logarithm functions.
  It remains a finite-field scalar-function model.

## Verdicts on the five synthesis items

The verdict labels are the ones requested in the review: (a) derivable from
the checked interpolation results, (b) strictly stronger or incomparable
after stating the missing scope, and (c) open.

| Repository item | Verdict | Proof or exact scope comparison |
|---|---|---|
| Theorem 3.1, affine $D\ge r/2$ | **(b) Incomparable, with a prior-art scalar specialization.** | Applying (A023.1) on the full multiplicative group already gives the same half-ambient degree scale for a polynomial computing the scalar logarithm. Lange--Winterhof gives elliptic-coordinate scalar bounds under different sampling hypotheses. Neither result treats a rational map $E\dashrightarrow H$, homomorphic only on $C$, into an arbitrary affine algebraic group $H$ through a fixed faithful representation; neither proves that a vanished translation defect makes the common pole divisor invariant and hence empty. Thus Theorem 3.1 is not derivable as stated, while its scalar degree scale is not new. |
| Theorem 4.1, exact overlap and $D_+B^2\ge r/4$ | **(b) Strictly broader in source/target scope, but quantitatively anticipated.** | Equation (A023.1) already proves the quadratic subset-over-ambient-size obstruction for one polynomial branch of the finite-field discrete-log function, using essentially the same ordered-pair averaging. It therefore recovers a $D_+B^2=\Omega(r)$ consequence in that scalar specialization after choosing a largest branch. It does not reprove Theorem 4.1 for rational maps on an elliptic curve, common pole divisors, arbitrary affine targets, or faithful matrix representations. The exact inequality $m(m-1)\le2D(r-1)$ in that general setting remains the repository synthesis, not a literature-novel combinatorial mechanism. |
| Corollary 7.2, $d+2b$ depth bound | **(b) Incomparable.** | Coppersmith--Shparlinski explicitly derive parallel arithmetic/Boolean consequences from interpolation degree, so degree-to-depth reasoning is prior art. The checked papers do not define P1.5's rational decision-tree evaluator, charge arbitrary branch predicates through $B\le2^b$, bound a faithful matrix representation by $M2^dD_0$, or conclude $d+2b\ge\log_2r-O(\log\log r)$. The corollary is a synthesis of a standard degree-to-depth step with the broader Theorem 4.1. |
| Theorem 5.2, proper $B<r$ branch collapse | **(b) Strictly outside the checked interpolation scope.** | The interpolation papers study affine polynomial encodings of scalar cryptographic functions. They do not use properness to extend rational maps, the rigidity lemma for pointed maps of abelian varieties, conjugation in a disconnected/noncommutative proper group, or the fact that one branch containing two points determines the homomorphism on a prime-order subgroup. No checked result derives the proper-branch collapse. |
| Theorem 6.1, mixed fibrewise criterion | **(b) Strictly outside the checked interpolation scope.** | The checked results have no Chevalley decomposition, affine-kernel cocycle, faithful representation of that kernel, or two-stage specialized/generic fibre pole hypothesis. Their polynomial scalar graphs do not imply that an $L$-valued defect vanishes and extends $E\dashrightarrow H$ globally. No checked result derives the mixed criterion. |

No item receives verdict (a): the closest results recover important
specializations and proof patterns, but not any of the five statements with
their current hypotheses. No item is verdict (c) as a comparison question;
the remaining mathematical strengthening of the branch exponent is open.

## Does interpolation reprove or improve the $B^2$ tradeoff?

- [PROVED] **It rederives the $B^2$ scale in its own scalar finite-field
  model.** Put $m=|S|$ in (A023.1). A largest branch among $B$ branches
  has $m\ge(p-1)/B$, so the theorem gives
  $D_+B^2=\Omega(p)$. This is the same quantitative mechanism as P1.5's
  largest-branch proof, not an improvement of it.
- [PROVED] **It does not reprove P1.5 Theorem 4.1 as stated.** Computing the
  discrete-log scalar by one field polynomial is a special output encoding.
  A homomorphism into a general affine group need not expose a scalar
  coordinate, and P1.5 measures the common poles of a faithful matrix
  representation on the elliptic source curve.
- [PROVED] **The checked character-sum route does not change $B^2$ to
  $B$ for adversarial branches.** For an arbitrary branch $S\subset C$,

  \[
  \sum_{t\ne0}|S\cap(S-t)|=|S|(|S|-1). \tag{A023.2}
  \]

  Hence the only overlap guaranteed without structure is of order
  $|S|^2/r$, exactly the input producing $D=\Omega(r/B^2)$. The linear
  degree bounds in the checked interpolation literature require a dense
  interval of exponents, random sampling, or another distribution hypothesis
  that an adversarial branch partition need not satisfy. Their
  arbitrary-subset theorems revert to (A023.1)-type quadratic energy bounds,
  sometimes with extra encoding losses.
- [PROVED] The character sums therefore do not supply the missing universal
  assertion $D=\Omega(|S|)$ for every branch. They cannot, as currently
  stated, be substituted into Section 4 to obtain $D_+B=\Omega(r)$.
- [CONJECTURE] Whether a different argument using the homomorphism values
  across several branches can improve the exponent from $2$ to $1$
  remains open. A proof must exploit more than the single-branch overlap
  guaranteed by (A023.2), or a counterexample must realize a near-uniform
  adversarial partition by actual low-pole branch maps.

## Verheul/Moody and generic-group reconciliation

- [CITED] Verheul proves that an efficient reverse homomorphism from the XTR
  subgroup to the paired supersingular elliptic subgroup makes
  Diffie--Hellman easy in both groups. Moody generalizes this consequence to
  arbitrary finite fields and suitable supersingular curves using computable
  pairings and distortion maps.
- [PROVED] This overlaps the conceptual content of SG-23: an efficient
  cross-group homomorphism can transfer the source hard problem to the target
  problem. SG-23's exact evaluator/source-DLP/target-DLP inequalities are more
  general as black-box reductions, but the consequence strategy is prior art.
- [CITED] Koblitz--Menezes emphasize that generic-group conclusions exclude
  special features of concrete encodings and that coordinate or
  implementation structure must be audited separately.
- [PROVED] This overlaps SG-14's conceptual boundary. SG-14 still contributes
  the P1.5-specific counted setup/evaluator composition and truncation
  argument, but not the general warning that generic groups omit concrete
  representation features.

## Outcome

- [PROVED] Section 10's former closest-prior-art account was incomplete and
  its novelty-adjacent wording was too strong.
- [PROVED] The corrected classification is a **repository-original
  synthesis**: the general elliptic-source/affine-target statements and the
  proper/mixed extensions were not found in the checked line, while the
  scalar half-degree bound, quadratic subset-overlap mechanism,
  degree-to-depth idea, generic/concrete boundary, and hard-problem
  consequence pattern all have clear predecessors.
- [PROVED] The interpolation literature does not cover A024's ordinary-class
  reduced-form evaluator with canonical lifts and integer valuations. A024
  therefore analyzes that exact model separately.
