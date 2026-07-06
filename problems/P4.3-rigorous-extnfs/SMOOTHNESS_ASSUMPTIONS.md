# exTNFS smoothness-dependency audit

## Result of the audit

[CITED] Kim--Barbulescu prove the advertised exTNFS running times only under the classical NFS heuristics; for their best Conjugation construction the displayed constant is $(48/9)^{1/3}$, while the JLSV2 construction gives $(64/9)^{1/3}$ in its stated parameter range.

[PROVED] The present audit does **not** turn that result into an unconditional $L_Q(1/3,c)$ theorem.  It isolates ten inputs, of which the random-integer benchmark and the cost of rigorous smoothness testing are known; the relation-supply, target-smoothing, and special-$q$ inputs remain open for the tower norm forms.  A proof of smoothness supply alone would still leave polynomial-selection and relation-matrix-rank issues described below.

## 1. Notation and the algorithm being audited

[PROVED] Write
\[
 L_Q(\alpha,c)=\exp\!\left((c+o(1))(\log Q)^\alpha
 (\log\log Q)^{1-\alpha}\right),\qquad Q=p^n,
\]
and split the composite extension degree as $n=\eta\kappa$ with $\eta,\kappa>1$ and $\gcd(\eta,\kappa)=1$.  This renames the question's extension degree $k$ to $n$, because $k(x)$ is used below for the common residue-field factor.

[CITED] exTNFS chooses $h(t)\in\mathbb Z[t]$ of degree $\eta$, irreducible modulo $p$, and works in $R=\mathbb Z[t]/(h)$.  It chooses $f,g\in R[x]$ whose reductions modulo $p$ have a common irreducible factor $k(x)$ of degree $\kappa$ over $R/pR\simeq\mathbb F_{p^\eta}$; the two tower number fields therefore map to $\mathbb F_Q$.

[CITED] A relation candidate has
\[
 r=a(\iota)-b(\iota)x,\qquad
 a(t)=\sum_{i<\eta}a_it^i,\quad b(t)=\sum_{i<\eta}b_it^i,\quad
 |a_i|,|b_i|\le A,
\]
and its two absolute norms are the integer-valued forms
\[
 F_f(\mathbf z)=\left|\operatorname {Res}_t
   (\operatorname {Res}_x(a(t)-b(t)x,f(x)),h(t))\right|,
 \quad
 F_g(\mathbf z)=\left|\operatorname {Res}_t
   (\operatorname {Res}_x(a(t)-b(t)x,g(x)),h(t))\right|,
\]
where $\mathbf z=(a_0,\ldots,a_{\eta-1},b_0,\ldots,b_{\eta-1})$.

[CITED] The relation-collection phase enumerates this $2\eta$-dimensional box, keeps a row exactly when both $F_f(\mathbf z)$ and $F_g(\mathbf z)$ are $B$-smooth, factors the two principal ideals over prime-ideal factor bases of norm at most $B$, appends the Schirokauer-map coordinates, and solves the resulting sparse linear system modulo the large prime divisor $\ell\mid Q-1$.

[CITED] With $B=L_Q(1/3,\beta)$ and optimized polynomial selection, Kim--Barbulescu bound the two norm sizes by
\[
 F_f\le L_Q(2/3,\gamma_f+o(1)),\qquad
 F_g\le L_Q(2/3,\gamma_g+o(1)).
\]
They model the two smoothness probabilities by those of arbitrary integers of the same sizes and write relation-collection plus linear-algebra cost as
\[
 L_Q\!\left(1/3,\beta+\frac{\gamma_f+\gamma_g}{3\beta}+o(1)\right)
 +L_Q(1/3,2\beta+o(1)).
\]

[PROVED] Balancing the two displayed exponents gives $\beta^2=(\gamma_f+\gamma_g)/3$ and constant $2\sqrt{(\gamma_f+\gamma_g)/3}$.  Indeed, equality of the exponents is $\beta+(\gamma_f+\gamma_g)/(3\beta)=2\beta$.

[CITED] For an individual logarithm, the paper first randomizes the target, lifts it to one side (JLSV2) or to a numerator/denominator pair (Conjugation/Waterloo), and waits for the lift norm or norms to be smooth and squarefree.  It then applies special-$q$ descent: a prime ideal $\mathfrak q$ is put into a coefficient lattice of determinant $N\mathfrak q$, an LLL basis is enumerated, and a candidate is accepted when the norm cofactors on both sides factor into smaller prime ideals.

## 2. The exact analytic statements

[PROVED] Let $\mathcal S_Q(A)$ be the nonzero coefficient vectors in the relation box for which both norms are nonzero, and let $P^+(m)$ denote the largest prime factor of $|m|$, with $P^+(1)=1$.  For nonzero integers $u,v$, both are $B$-smooth if and only if $P^+(uv)\le B$, because the prime divisors of $uv$ are precisely the union of their prime divisors.

### S-01 -- first-side relation density

[CONJECTURE] Uniformly along every admissible exTNFS parameter sequence and every polynomial/box choice actually output by the stated selection algorithm,
\[
 \frac{\#\{\mathbf z\in\mathcal S_Q(A):P^+(F_f(\mathbf z))\le B\}}
      {\#\mathcal S_Q(A)}
 =L_Q\!\left(1/3,-\frac{\gamma_f}{3\beta}+o(1)\right),
\]
with an $o(1)$ uniform over the optimized parameter range.  Kim--Barbulescu use this when replacing the first-side norm by an arbitrary integer of the same size.

### S-02 -- second-side relation density

[CONJECTURE] Under the same quantifiers,
\[
 \frac{\#\{\mathbf z\in\mathcal S_Q(A):P^+(F_g(\mathbf z))\le B\}}
      {\#\mathcal S_Q(A)}
 =L_Q\!\left(1/3,-\frac{\gamma_g}{3\beta}+o(1)\right).
\]
This is a separate claim because the two selected polynomials and their norm sizes differ.

### S-03 -- simultaneous relation density

[CONJECTURE] The complexity calculation additionally uses the product of the two marginal probabilities.  A weaker single statement sufficient for its upper bound is the uniform lower bound
\[
 \frac{\#\{\mathbf z\in\mathcal S_Q(A):P^+(F_f(\mathbf z)F_g(\mathbf z))\le B\}}
      {\#\mathcal S_Q(A)}
 \ge L_Q\!\left(1/3,-\frac{\gamma_f+\gamma_g}{3\beta}+o(1)\right).       \tag{RC}
\]
Equality at this scale recovers the paper's random-independent model; the lower bound alone supplies enough candidates for the claimed running-time upper bound, subject to row rank.

[CITED] The two factor bases together have $L_Q(1/3,\beta+o(1))$ columns.

[PROVED] Consequently the density form (RC) must be paired with the deterministic parameter equalities/inequalities
\[
 \#\mathcal S_Q(A)
 = L_Q\!\left(1/3,\beta+\frac{\gamma_f+\gamma_g}{3\beta}+o(1)\right)
\]
and
\[
 \#\{\mathbf z\in\mathcal S_Q(A):P^+(F_f(\mathbf z)F_g(\mathbf z))\le B\}
 \ge L_Q(1/3,\beta+o(1)).                                      \tag{RC-count}
\]
The first display times the (RC) density gives the second display at the $L$ scale.  The polynomial/box optimization is useful only when it satisfies the norm bounds and these candidate-count bounds simultaneously.

[PROVED] Statements S-01 and S-02 do not imply (RC): the events are functions of the same coefficient vector and may be correlated at the full $L$-exponent scale.  Thus multiplying the marginal densities is an additional assumption, not algebra.

### S-04 -- JLSV2 initial splitting

[CONJECTURE] Fix a target $s$ in the relevant large subgroup, let $e$ range over the randomizing exponents used by the algorithm, and write $M_e$ for the absolute norm of the prescribed lift of $s^e$ to $K_f$.  If $M_e\le X_0(Q)$ and the initial smoothness bound is $Y_0(Q)$, the needed claim is a uniform lower bound of random-integer order
\[
 \#\{e\le E:P^+(M_e)\le Y_0,\ \mu^2(M_e)=1\}
 \ge E\,\frac{\Psi(X_0,Y_0)}{X_0}\,L_Q(1/3,o(1)),                 \tag{IS-J}
\]
for the algorithm's $E,X_0,Y_0$ and for every allowed target.  The JLSV2 lift has $X_0\le Q^{2-2/(\kappa+1)+o(1)}$, but this size bound does not imply (IS-J).

### S-05 -- Conjugation/Waterloo initial splitting

[CONJECTURE] Write $U_e,V_e$ for the two numerator/denominator lift norms produced by Waterloo and use its bound $|U_eV_e|\le Q^{1+o(1)}$.  The required replacement for (IS-J) is
\[
 \#\{e\le E:P^+(U_eV_e)\le Y_0,\ \mu^2(U_eV_e)=1\}
 \ge E\,\frac{\Psi(X_0,Y_0)}{X_0}\,L_Q(1/3,o(1)),                 \tag{IS-C}
\]
with $X_0=Q^{1+o(1)}$, uniformly over targets and chosen fields.  This is a joint smooth-value assertion about two structured lifts.

### S-06 -- the squarefree co-condition

[CONJECTURE] The squarefree restrictions in (IS-J) and (IS-C) need a positive, uniform proportion after conditioning on smoothness.  A theorem giving only $Y_0$-smooth values does not discharge this use, because the descent setup in the cited analysis uses squarefree ideal factorizations.

### S-07 -- one special-$q$ descent step

[PROVED] For a current prime ideal $\mathfrak q$ of norm $\nu$, let $\mathcal C_{\mathfrak q}(D)$ be the finite set of coefficient vectors obtained by enumerating the prescribed bounded combinations of an LLL basis of its lattice.  On the side containing $\mathfrak q$, its rational norm $\nu$ divides the corresponding absolute norm, so define
\[
 G_{f,\mathfrak q}(\mathbf z)=F_f(\mathbf z)/\nu,
 \]
interchanging $f$ and $g$ when $\mathfrak q$ lies on the other side.

[PROVED] Define the worst-case cofactor sizes in the enumeration box by
\[
 X_{f,\mathfrak q}=\max_{\mathbf z\in\mathcal C_{\mathfrak q}(D)}
 |G_{f,\mathfrak q}(\mathbf z)|,
 \qquad
 X_{g,\mathfrak q}=\max_{\mathbf z\in\mathcal C_{\mathfrak q}(D)}
 F_g(\mathbf z),
\]
and put $u_f=\log X_{f,\mathfrak q}/\log y$ and $u_g=\log X_{g,\mathfrak q}/\log y$.

[CONJECTURE] At a level whose child bound is $y=\nu^c$, the local input is the uniform lower bound
\[
 \frac{\#\{\mathbf z\in\mathcal C_{\mathfrak q}(D):
       P^+(G_{f,\mathfrak q}(\mathbf z)F_g(\mathbf z))\le y\}}
      {\#\mathcal C_{\mathfrak q}(D)}
 \ge \rho(u_f)\rho(u_g)L_Q(1/3,o(1)),                            \tag{SQ}
\]
or any explicit lower bound large enough for the same descent cost, where $\rho$ is the Dickman function.  The statement must hold for both placements of $\mathfrak q$.

### S-08 -- uniformity through the adaptive descent tree

[CONJECTURE] A pointwise version of (SQ) for one fixed lattice is insufficient.  The proof needs it simultaneously, or with summable failure probability, for every $\mathfrak q$, every LLL basis, every medium/small-$\nu$ regime, and every child ideal selected by the preceding random descent history.  It must also ensure that the accumulated number of trials and children stays within the stated $L_Q(1/3,c+o(1))$ budget.

### S-09 -- detecting and factoring smooth candidates

[CITED] Lenstra--Pila--Pomerance's hyperelliptic smoothness machinery, as used explicitly by Lee--Venkatesan, factors a $y$-smooth integer $m\le x$ in expected $y^{o(1)}$ time when $y=(\log x)^{\omega(1)}$.  It therefore supplies a rigorous expected-time replacement for the ECM-style smoothness-testing subroutine.

[PROVED] The exTNFS relation regime satisfies that hypothesis: if $x\le L_Q(2/3,O(1))$ and $y=B=L_Q(1/3,\beta)$, then $\log y/\log\log x\to\infty$.  Hence accepted relations can be completely factored in $B^{o(1)}$ expected time; smoothness *testing cost* is not the density obstruction.

### S-10 -- the random-integer benchmark

[CITED] Canfield--Erdos--Pomerance prove, uniformly in their stated range, an asymptotic for $\Psi(x,x^{1/u})$.  Its standard $L$-notation consequence is
\[
 \frac{\Psi(L_Q(b,d),L_Q(a,c))}{L_Q(b,d)}
 =L_Q\!\left(b-a,-\frac{d(b-a)}c+o(1)\right),\qquad 0<a<b\le1.
\]
For $a=1/3,b=2/3$ this is the exponent used in S-01--S-03.

[PROVED] S-10 says nothing about $F_f(\mathbf z)$, $F_g(\mathbf z)$, target lifts, or lattice-conditioned norm values: those are not uniformly sampled integers.  Invoking S-10 after calling a norm "random" is precisely the unproved transfer isolated in S-01--S-08.

## 3. Unconditional status

| Input | Status | Closest unconditional result | Missing hypothesis/conclusion |
|---|---|---|---|
| S-01, S-02 | **Open** | [CITED] Balog--Blomer--Dartyge--Tenenbaum and Barbulescu--Lachand give positive-proportion or restricted smooth-value lower bounds for **fixed** binary forms. | [PROVED] exTNFS uses parameter-dependent $2\eta$-variable iterated-resultant forms, a much smaller $L(1/3)$ smoothness bound, and uniformity as fields, degrees, discriminants, and coefficient boxes vary. |
| S-03 | **Open** | [CITED] Barbulescu--Lachand treat products of finitely many fixed binary forms in restricted dense-smoothness ranges. | [PROVED] No cited theorem gives the required joint $L$-scale lower bound for the two varying tower forms. |
| S-04--S-06 | **Open** | [CITED] Rigorous index-calculus algorithms obtain smooth inputs by randomizing integers or polynomials whose distribution can be counted. | [PROVED] No cited result controls the subgroup-indexed tower lift norms, their pairwise smoothness, and squarefreeness uniformly over targets. |
| S-07, S-08 | **Open** | [CITED] Fixed-number-field ideal counts have Dickman-type asymptotics, uniformly in a broad $x,y$ range for that fixed field. | [PROVED] Such counts do not count short principal generators in a varying special-$q$ lattice, do not pair the second tower side, and are not uniform over an adaptive family of fields/lattices. |
| S-09 | **Known** | [CITED] Hyperelliptic smoothness testing/factorization gives the required expected $B^{o(1)}$ accepted-candidate cost. | [PROVED] It controls the cost **after candidates exist**, not how often they exist. |
| S-10 | **Known** | [CITED] Canfield--Erdos--Pomerance give the needed random-integer density. | [PROVED] The transfer from integers to norm-form values remains S-01--S-08. |

[CITED] Barbulescu--Lachand also prove a Dickman-type asymptotic for smooth ideals in one fixed number field and an alpha-corrected asymptotic for a fixed quadratic binary form.  These are genuine partial results, but their constants and quantifiers are not uniform in the tower fields selected as $Q\to\infty$.

[CONDITIONAL: GRH] Buchmann--Hollinger give a smooth-ideal lower bound whose non-smoothness dependence is only on the field degree.  This does not help the unconditional target and, even under GRH, does not count short principal generators satisfying the second-side relation or a special-$q$ lattice constraint.

## 4. Two rigorous modification patterns and their cost

### 4.1 Randomized NFS polynomial selection does not presently pass through the tower

[CITED] Lee--Venkatesan rigorously generate simultaneous rational/algebraic smooth relations for a randomized ordinary NFS.  They randomize
\[
 f=\widehat f+(x-my)R,
\]
so, for fixed $(a,b)$, $f(a,b)$ is genuinely distributed in an arithmetic progression; smooth-number theorems in progressions and stochastic deepening replace the usual relation-yield heuristic.  Their congruence-of-squares-to-factor conclusion still uses a separately stated character conjecture.

[PROVED] The literal tower analogue does not yield an integer arithmetic progression.  Randomizing a tower polynomial by a multiple that preserves the common factor modulo $p$ makes its relative resultant vary in $R=\mathbb Z[t]/(h)$, after which the outer norm $N_{R/\mathbb Q}$ is a nonlinear degree-$\eta$ form.  The ordinary-NFS progression theorem therefore does not prove S-01--S-03, and it gives no special-$q$ statement.

[CONJECTURE] A viable $L_Q(1/3)$ modification would need a distribution on tower polynomial coefficients for which the *outer norm of the randomized relative resultant* has a provable smooth-value lower bound, while preserving the common residue-field factor and norm-size optimization.  Establishing such a distribution is an open analytic subproblem rather than a completed algorithm modification.

### 4.2 A fully rigorous DLP fallback loses the $1/3$ exponent

[CITED] Bender--Pomerance give a rigorous index-calculus algorithm for every finite field by representing $\mathbb F_Q$ as $\mathbb F_p[x]/(f)$ and using smooth polynomials.  When the extension degree grows, their bounds include
\[
 L_Q(1/2,\sqrt2+o(1))\quad\text{if }p\le n^{o(n)},
 \qquad p^{2+o(1)}\quad\text{if }p>n^{4n/3},
\]
with an intermediate $L_Q(1/2,\sqrt{8/3}+o(1))$ range.

[PROVED] If medium characteristic is parameterized by $p=L_Q(\ell_p,c_p)$ with $1/3<\ell_p<2/3$, then their rigorous fallback is $L_Q(1/2,\sqrt2+o(1))$ for $\ell_p<1/2$ and $L_Q(\ell_p,2c_p+o(1))$ for $\ell_p>1/2$ (with boundary behavior depending on constants).  Indeed $\log n=(1+o(1))\log\log Q$, so $\log p=o(n\log n)$ below $\ell_p=1/2$ and $\log p\gg n\log n$ above it; also $p^{2+o(1)}=L_Q(\ell_p,2c_p+o(1))$.

[PROVED] This is an unconditional result for the same DLP problem, but it is not a rigorous analysis of exTNFS and it does not retain the exponent $1/3$.  It is the cleanest currently identified "modified algorithm with worse complexity" fallback.

### 4.3 Sampling arbitrary smooth ideals is only a one-side partial modification

[CITED] Barbulescu--Lachand's fixed-number-field ideal theorem suggests sampling smooth ideals first and then seeking short generators, instead of hoping a short generator has smooth norm.  Their discussion notes that enumerating the relevant ideals/generators is itself the principal algorithmic difficulty.

[PROVED] Even if that enumeration were made efficient for one fixed tower side, a relation still needs the same generator to map to a smooth norm on the other side.  Thus this idea may discharge a one-side supply problem but does not by itself discharge S-03 or special-$q$ descent.

### 4.4 Fixed quadratic outer norms do not cover the interior optimized scale

[PROVED] Attempt A003 proves that for $\eta=2$ and $h(T)=T^2+h_1T+h_0$,
\[
 N(x+y\iota)=x^2-h_1xy+h_0y^2,
\]
and a homogeneous two-parameter pullback has discriminant
\[
 (h_1^2-4h_0)(x_0y_1-x_1y_0)^2.
\]
This precisely identifies the rare slices to which a fixed quadratic-form theorem could apply.

[PROVED] The same attempt identifies a degree-uniformity barrier.  If $p=L_Q(\ell_p,c_p)$ with $1/3<\ell_p<2/3$, a relation box containing $L_Q(1/3,\tau)$ candidates has standard worst-case norm contribution
\[
 \log(A^n)=\frac{\tau+o(1)}{2c_p\eta}
 (\log Q)^{4/3-\ell_p}(\log\log Q)^{\ell_p-1/3}.
\]
Keeping this on the $L_Q(2/3)$ scale forces
\[
 \eta=\Theta((\log Q/\log\log Q)^{2/3-\ell_p})\to\infty.
\]
Thus the fixed quadratic theorem and the optimized interior exTNFS parameter range require incompatible degree quantifiers.

[PROVED] There is nevertheless an algebraic opening at fixed $\eta=2$: randomizing a degree-$\kappa$ polynomial by the kernel family $f_0+pU+KV$ maps onto the entire quadratic order for ideal-coprime candidates.  Attempt A005 supplies bounded preimage multiplicities, irreducibility, and parameter bookkeeping for a boundary subfamily; the construction still cannot reach the optimized strict interior.

### 4.5 A rigorous relation-supply result on the $\ell_p=2/3$ boundary

[PROVED] Attempt A005 closes those three relation-supply subgaps for the restricted family
\[
 p=L_Q(2/3,c_p),\qquad p\equiv3\pmod4,\qquad
 n=2\kappa,\qquad R=\mathbb Z[i].
\]
It proves a bounded-fiber lemma for the surjection $(u,v)\mapsto Au+Bv$, proves that irreducibility modulo an auxiliary prime $q>B$ retains a $\Theta(1/\kappa)$ fraction even after prescribing the evaluation, and performs the coefficient/norm bookkeeping.

[PROVED] With $A=L_Q(1/3,a)$, $B=L_Q(1/3,\beta)$, and
\[
 m=c_p+\frac{a}{2c_p},
\]
choose $\beta c_p>1/3$ and
\[
 a>
 \frac{\displaystyle\beta+\frac{8c_p}{3\beta}}
      {\displaystyle4-\frac{4}{3\beta c_p}}.
\]
The modified ensemble
\[
 f=K(1+v_f)+pU_f,\qquad g=K(1+v_g)+pU_g
\]
then finds an irreducible polynomial pair with $L_Q(1/3,\beta)$ jointly smooth relations in expected time
\[
 L_Q\!\left(1/3,\,
 4a+\frac{8m}{3\beta}+o(1)\right).
\]
This is an unconditional $L_Q(1/3,O(1))$ theorem for **relation supply**, with a worse nonoptimized constant, not for the full DLP.

[PROVED] The result does not extend by the same proof to fixed $\ell_p<2/3$, because optimized exTNFS forces $\eta\to\infty$ and the only smooth-value theorem used in A005 is for one fixed quadratic form.

## 5. Dependencies not reducible to smoothness

[CITED] The Conjugation polynomial-selection analysis expects suitable irreducible polynomials after a small number of trials; the cited paper labels this as heuristic.  A fully unconditional complexity proof must either construct the required sequence uniformly or account rigorously for this search.

[PROVED] A count of at least as many smooth relations as factor-base columns does not imply that their valuation/Schirokauer rows span the required space modulo $\ell$.  The sparse linear-algebra running time is rigorous once an adequate matrix is supplied, but the rank of the structured exTNFS relation matrix is a separate unproved supply assertion.

[PROVED] Attempt A004 gives a minimal sufficient rank theorem.  If $\mu_Q$ is the accepted-row distribution on the algebraically allowed row space $H_Q$, define
\[
 \delta_Q=\inf_{\varphi\in H_Q^\ast\setminus\{0\}}
 \Pr_{R\sim\mu_Q}[\varphi(R)\ne0].
\]
The condition $\delta_Q\ge L_Q(1/3,-o(1))$ implies that adaptive collection of independent rows spans $H_Q$ after at most $\dim(H_Q)/\delta_Q$ accepted rows in expectation, preserving the leading constant.  No cited theorem proves this hyperplane anti-concentration after conditioning on simultaneous smoothness.

[PROVED] Therefore even proofs of (RC), (IS-J)/(IS-C), and (SQ) would not alone prove unconditional DLP complexity for the stated algorithm; they would close the smoothness part of the argument and leave the two adjacent gaps above.

## 6. Exact toy check (SG-04)

[PROVED] The repository experiment uses the genuine tower instance
\[
 p=5,\quad h=t^2+2,\quad f=x^3+x+1,\quad g=x^3+x-4,\quad Q=5^6<2^{60}.
\]
Modulo $5$, $h$ is irreducible and $f\equiv g$ is an irreducible cubic, so this is an $\eta=2,\kappa=3$ exTNFS setup rather than a proxy form.

[PROVED] For $a=a_0+a_1\iota$, $b=b_0+b_1\iota$, and $\iota^2=-2$, the inner resultant is $a^3+ab^2+cb^3$ for $x^3+x+c$, and the outer norm of $u_0+u_1\iota$ is $u_0^2+2u_1^2$.  The program exhausts all 5,856 primitive vectors in $[-4,4]^4$, fully factors both norms, and independently samples one uniform integer from each norm's dyadic interval on each side.

| $B$ | actual joint rate | dyadic baseline rate (95% Wilson interval) | ratio | actual joint/product-of-marginals |
|---:|---:|---:|---:|---:|
| 7  | 0.023224 | 0.002732 (0.001683--0.004434) | 8.50 | 7.73 |
| 13 | 0.043716 | 0.005635 (0.004016--0.007903) | 7.76 | 5.14 |
| 31 | 0.073087 | 0.019980 (0.016698--0.023891) | 3.66 | 3.81 |
| 61 | 0.114071 | 0.037398 (0.032833--0.042568) | 3.05 | 2.82 |

[PROVED] The preregistered divergence criterion is met at all four bounds, and the preregistered positive-dependence prediction is not refuted.  Independent SymPy checks reproduced all 23,424 stored factorizations and 128 nested resultants from 64 stratified candidates.

[PROVED] This finite example falsifies literal equality with the chosen random-integer model at these parameters, but it neither supports nor refutes the required asymptotic $L$-exponent.  The baseline draws are independent between sides conditional on the two observed norm magnitudes; its unconditional dependence ratio can still exceed one because both magnitudes are functions of the same coefficient vector.

## 7. Bottom line

[PROVED] The smallest missing theorem for relation collection is (RC), not two marginal Dickman statements.  The strongest missing theorem is (SQ) with S-08's adaptive uniformity.  No unconditional result identified in the primary literature has those quantifiers for exTNFS tower norm forms.

[PROVED] The claimed exTNFS $L_Q(1/3,c)$ complexity consequently remains heuristic.  What is unconditional today is (i) the random-integer comparison rate, (ii) a rigorous low-overhead way to factor accepted smooth candidates, (iii) limited fixed-form/fixed-field partial density theorems, and (iv) a different rigorous finite-field DLP algorithm with a worse exponent or constant as detailed above.
