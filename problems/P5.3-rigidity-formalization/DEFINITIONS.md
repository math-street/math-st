# Rigidity game and bound

## 1. Objects and the accounting contract

**Definition.** A *domain-parameter package* is a canonical encoding of every
public object that may affect security: the base field, curve model and
coefficients, subgroup order and cofactor, base point, and any representation
data. The finite set of packages in the target profile is denoted
\(\Omega\), and the public safety predicate is
\(\mathsf{Safe}:\Omega\to\{0,1\}\).

**Definition.** An *accounting contract* \(\mathcal A\) fixes, before curve
generation:

1. the target profile and canonical encoding of \(\Omega\);
2. \(\mathsf{Safe}\), including its version and all thresholds;
3. a finite index set \(I\) of designer-screenable candidate executions;
4. a joint random experiment \((X_i)_{i\in I}\), where each
   \(X_i\in\Omega\);
5. a reference distribution \(\nu\) on \(\Omega\); and
6. the projection used by the hidden weakness predicate, for example the
   curve core or the entire domain-parameter package.

An incrementing counter inside one execution does not add an index when the
contract forces publication of the first passing candidate. Skipping a
passing candidate is a new screenable choice and must add an index.

**Definition.** Let \(M=|I|\) after identifying executions whose projected
outputs are equal for every random tape. The *selection capacity* is

\[
  b(\mathcal A)=\log_2 M.
\]

This is a support-size or max-entropy measure, not Shannon entropy. It can be
non-integral when \(M\) is not a power of two.

**Definition.** A category accounting is a decision tree whose branches are
choices such as security profile, field, curve model, hash/XOF, seed source,
encoding, counter and stopping rule, safety/cofactor policy, and base-point
rule. The authoritative value of \(b\) is the logarithm of the number of
distinct screenable leaves. If category \(j\) has at most \(m_j\) branches
after every history, then the convenient compositional cap is
\(b\leq\sum_j\log_2m_j\). Equality requires the branches to form a full
Cartesian product of distinct projected outputs.

## 2. Selective-generation game

**Definition (game \(\mathsf{RigSel}_{\mathcal A,\epsilon}\)).** The order of
play is:

1. The auditor fixes \(\mathcal A\).
2. A weakness source commits to \(\mathcal B\subseteq\Omega\). The set may
   depend on \(\mathcal A\), and the designer knows it, but it may not depend
   on the fresh random tape used in Step 3.
3. The challenger samples the joint experiment \((X_i)_{i\in I}\).
4. The designer sees or computes the candidates, tests membership in its
   hidden \(\mathcal B\), and publishes one index \(i^*\), or fails.
5. The designer wins exactly when
   \(X_{i^*}\in\mathcal B\) and
   \(\mathsf{Safe}(X_{i^*})=1\).

The accounting contract is the meta-specification. A designer may choose a
residual final specification after learning \(\mathcal B\), but every such
choice must already be represented in \(I\). This models a designer who
knows a weakness before screening parameters without allowing the designer to
invent an uncharged generator tailored to that weakness.

**Definition.** Write \(\mu_i\) for the marginal distribution of \(X_i\).
The source-bounded weak mass is

\[
  \epsilon_{\mathcal A}(\mathcal B)
  =\max_{i\in I}\mu_i(\mathcal B\cap\mathsf{Safe}^{-1}(1)).
\]

When \(\nu\) is uniform and all \(\mu_i=\nu\), this is the usual safe weak-set
density. More generally define the domination factor

\[
  \kappa=\max_{i\in I,\,x:\nu(x)>0}\frac{\mu_i(x)}{\nu(x)},
\]

with \(\kappa=\infty\) if some \(\mu_i\) charges a point outside the support
of \(\nu\).

## 3. Main bound

**Theorem (selective-generation union bound). [PROVED]** If
\(\nu(\mathcal B\cap\mathsf{Safe}^{-1}(1))\leq\epsilon\) and
\(\mu_i(x)\leq\kappa\nu(x)\) for every \(i,x\), then

\[
 \Pr[\mathsf{RigSel}_{\mathcal A,\epsilon}=1]
 \leq \min(1,M\kappa\epsilon)
 =\min(1,2^b\kappa\epsilon).
\]

In particular, for uniform candidate marginals, \(\kappa=1\) and the requested
bound is \(\min(1,2^b\epsilon)\).

**Distribution-free form. [PROVED]** With the source-bounded mass defined
above, the same argument gives
\[
  \Pr[\mathsf{RigSel}=1]
  \leq\min(1,2^b\epsilon_{\mathcal A}(\mathcal B)).
\]
This is the correct statement when “fraction of curves” is not tied to a
uniform or dominated sampling kernel.

**Proof. [PROVED]** For each \(i\), let
\(E_i=\{X_i\in\mathcal B\cap\mathsf{Safe}^{-1}(1)\}\). A win implies
\(\bigcup_iE_i\), regardless of how the designer selects \(i^*\). Domination
gives

\[
 \Pr[E_i]=\mu_i(\mathcal B\cap\mathsf{Safe}^{-1}(1))
 \leq\kappa\nu(\mathcal B\cap\mathsf{Safe}^{-1}(1))
 \leq\kappa\epsilon.
\]

The union bound gives \(\Pr[\bigcup_iE_i]\leq M\kappa\epsilon\), and every
probability is at most one. No independence between candidates is used.
\(\square\)

**Tightness. [PROVED]** Let \(\Omega=\mathbb Z/N\mathbb Z\), let \(R\) be
uniform, let \(\mathcal B\) be a block of \(k\) elements, and set
\(X_i=R+t_i\) for translations whose inverse images of \(\mathcal B\) are
disjoint. When \(Mk\leq N\), every \(X_i\) is uniform and the win
probability is exactly \(Mk/N=M\epsilon\). When translated blocks cover
\(\Omega\), the saturation value one is attained. For independent uniform
candidates the exact probability is \(1-(1-\epsilon)^M\), so the union bound
is asymptotically tight when \(M\epsilon\) is small.

## 4. Quantifier failures

- **Post-output weakness. [PROVED]** If \(\mathcal B\) may be chosen after a
  candidate is observed, it can be the singleton containing that candidate.
  The designer then wins with probability one even when
  \(\epsilon=1/|\Omega|\) and \(b=0\).
- **Uncharged meta-specification. [PROVED]** If the generator itself may be
  chosen after \(\mathcal B\) without that choice appearing in \(I\), a
  constant generator can target an element of \(\mathcal B\); no bound in
  terms of the reported \(b\) follows.
- **Biased source. [PROVED]** Cardinal density alone is insufficient when a
  candidate distribution concentrates on \(\mathcal B\). The factor
  \(\kappa\), or the direct marginal bound
  \(\epsilon_{\mathcal A}(\mathcal B)\), is necessary.
- **No fresh experiment. [PROVED]** A deterministic fixed curve has no
  nontrivial probability statement against a fixed \(\mathcal B\): it is
  either weak or not. Reproducibility can make \(b=0\), but probabilistic
  assurance additionally needs a source of randomness independent of
  \(\mathcal B\), or a distributional model for \(\mathcal B\).

## 5. Provenance identifiability

**Definition.** Let \(\ell\) map a complete design history \(H\) to the
surviving public record \(O=\ell(H)\). Historical selection capacity is
*identifiable from \(O\)* on a class of admissible histories when \(b(H)\) is
constant on every fiber \(\ell^{-1}(O)\).

**Theorem (final-output non-identifiability). [PROVED]** Fix a published
projected output \(x\in\Omega\). If the public record contains \(x\) but
places no further restriction on the pre-publication history, then for every
integer \(M\) with \(1\leq M\leq|\Omega|\) there is a history with that same
record and selection capacity \(\log_2 M\). Consequently, no function of the
final output alone can recover historical \(b\) on this class.

**Proof. [PROVED]** For \(M=1\), use the forced singleton menu \(\{x\}\). For
general \(M\), choose \(M-1\) other distinct projected packages and make those
packages together with \(x\) the designer-screenable menu; the designer
publishes \(x\). Both histories have the same surviving output, while their
capacities are \(0\) and \(\log_2 M\). Hence \(b\) is not constant on the
observation fiber. \(\square\)

**Seeded replay corollary. [PROVED]** A published seed and a deterministic
seed-to-curve derivation do not by themselves identify provenance capacity.
If the origin of the seed is absent, the same record is compatible both with
an externally forced singleton seed and with designer screening over any
finite collection of seeds containing it, up to the number of distinct
projected outputs of the derivation.

**Certificate criterion. [PROVED]** A record identifies \(b\) once it fixes a
finite accounting contract and supplies evidence that every admissible
history consistent with the record has the same quotient menu size. One
sufficient certificate contains:

1. a digest and externally dated commitment to the meta-specification,
   including the safety predicate and audit projection;
2. the complete finite candidate domain and canonical equivalence relation;
3. the exact generator, dependency versions, enumeration order, tie breakers,
   and forced stopping rule;
4. the origin and transcript of any fresh randomness, with restart,
   suppression, and substitution rules;
5. a replay transcript or succinct proof covering rejected candidates and the
   published candidate; and
6. a statement of every residual designer-selectable branch.

**Justification. [PROVED]** These items determine the screenable index set
\(I\), its quotient by projected-output equality, and therefore
\(b=\log_2|I|\). Omitting an item need not make identification impossible,
but then uniqueness of the quotient menu size requires a separate proof.

**Audit consequence. [PROVED]** A literal-only record can establish exact
replay while leaving provenance non-identifiable. The symbol \(\bot\) in the
audit means precisely that the cited record does not determine a common value
of \(b\) across its admissible history fiber; it does not assert malicious
selection or assign an infinite capacity.

## 6. Minimal-designer-freedom generator

**Definition (ideal canonical-beacon generator).** Fix a security profile
\(\lambda\), a finite canonically ordered safe package set
\(\Omega_\lambda\), and an exact uniform-unranking routine. After the
accounting contract and \(\mathcal B\) are fixed, the challenger supplies an
infinite unbiased public bit stream \(R\) that the designer cannot predict,
select, restart, or suppress. For
\(k=\lceil\log_2|\Omega_\lambda|\rceil\), read successive \(k\)-bit blocks;
publish the package with that index for the first block smaller than
\(|\Omega_\lambda|\), rejecting larger blocks by a forced rule.

**Proposition. [PROVED]** The ideal canonical-beacon generator has designer
selection capacity \(b=0\), outputs the uniform distribution on
\(\Omega_\lambda\), and is minimal because \(b=\log_2M\geq0\) for every
nonempty menu. The theorem therefore gives win probability at most
\(\epsilon\).

**Proof. [PROVED]** The forced stopping rule exposes exactly one publishable
candidate, so \(M=1\). Rejection of indices outside a final incomplete
power-of-two range leaves every accepted index with the same probability.
The lower bound \(b\geq0\) follows from \(M\geq1\). \(\square\)

**Concrete refinement. [CONDITIONAL: an ideal XOF and an unbiasable public
beacon]** A practical specification can replace \(R\) by domain-separated XOF
blocks from a future public beacon, use exact rejection sampling for field
elements, and force the first curve passing a versioned safety predicate and
the first canonically encoded subgroup generator. The resulting reference
distribution is the distribution induced by that fixed rejection sampler;
it need not be cardinal-uniform over a differently defined curve universe.
The condition would be falsified by a demonstrable beacon-biasing strategy or
a distinguishable bias in the XOF-derived candidate stream.

**Implementation limitation. [PROVED]** Uniform unranking of the entire safe
set is a definitional construction, not an efficient production algorithm.
A deployable generator must replace it with a specified sampling kernel and
then state weak-set density relative to that kernel.

**Toy instantiation. [CONDITIONAL: ideal-XOF outputs are independent uniform
byte strings]** `code/sample_rigid_curve.py` fixes a toy prime and safety
profile, samples coefficient pairs with exact field-element rejection, and
forces the first passing pair. `attempts/A002-toy-first-passing.md` proves that
its induced reference distribution is uniform over passing coefficient
encodings. The batch sample index is for measurement only; allowing a designer
to select among batch rows would add the corresponding menu capacity.

### Class-uniform toy refinement

**Short-Weierstrass class criterion. [PROVED]** Over a field of characteristic
greater than three, two short-Weierstrass models
\(y^2=x^3+ax+b\) and \(y^2=x^3+a'x+b'\) are isomorphic over the field while
preserving the point at infinity exactly when there is a \(u\ne0\) with
\((a',b')=(u^4a,u^6b)\).

**Proof. [PROVED]** Substituting the general Weierstrass change of variables
into two short models forces its translation and shear terms to vanish because
2 and 3 are invertible. The remaining scaling
\((x,y)=(u^2x',u^3y')\) gives the displayed coefficient action, and every such
scaling is an isomorphism. \(\square\)

**Kernel projection formula. [PROVED]** Let \(\mathcal C\) be the safe
coefficient encodings, partitioned into scaling orbits \(O\). Conditional on
the A002 coefficient kernel passing safety, its induced class probability is
\[
  \Pr[O]=\frac{|O|}{|\mathcal C|}.
\]
Thus coefficient-uniform sampling is class-uniform exactly when all safe
orbits have equal size.

**Toy census. [EMPIRICAL: exhaustive \(0\leq a,b<127\), all nonzero
scalings]** At \(p=127\), 16,002 nonsingular encodings form 258 classes with
orbit histogram \(\{21:6,63:252\}\). The fixed A002 safety profile accepts
4,179 encodings in 67 classes, with safe histogram \(\{21:1,63:66\}\).
Consequently the exceptional safe class has coefficient-kernel mass \(1/199\)
and every other safe class has mass \(3/199\); their total variation distance
from class-uniform is \(132/13333\).

**Class-uniform generator. [CONDITIONAL: ideal-XOF outputs are independent
uniform byte strings]** `code/class_uniform_kernel.py` lexicographically orders
the 67 canonical safe representatives and uses exact rejection to unrank one
future-beacon-derived index. It therefore outputs every safe
\(\mathbb F_{127}\)-isomorphism class with probability \(1/67\).

**Designer capacity. [PROVED]** When the profile, class list, sample label, and
future beacon are externally fixed and restart/suppression is forbidden, the
class-uniform generator exposes one publishable execution and has \(b=0\).

**Minimax property. [PROVED]** Among distributions with full support on a
fixed set of \(N\) classes, the uniform distribution uniquely minimizes the
largest singleton probability, attaining \(1/N\). Indeed, probabilities sum
to one, so their maximum is at least \(1/N\), with equality only when all are
equal. Hence the toy class kernel is minimax for a hidden weakness containing
one isomorphism class under this fixed universe and projection.

## 7. Design consequences

- **[PROVED]** A low \(b\) never compensates for a weak
  \(\mathsf{Safe}\); safety and designer selection capacity are separate
  coordinates.
- **[PROVED]** Performance-motivated fields or models do not inherently add
  freedom when the architecture, cost function, tie-breaking rule, and
  stopping rule are fixed before \(\mathcal B\). An undocumented shortlist
  does add unmeasured freedom.
- **[PROVED]** Algorithm agility is compatible with low \(b\) only when the
  choice or migration rule is externally fixed. Allowing a designer to try
  several hashes, fields, encodings, or safety thresholds multiplies the
  screenable menu.
