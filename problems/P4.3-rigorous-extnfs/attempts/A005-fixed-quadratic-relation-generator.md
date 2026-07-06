---
attempt: A005
status: promising
---
# A005 - A rigorous fixed-quadratic relation-supply modification

## Scope

[PROVED] This attempt addresses **relation supply only** for the restricted case $\eta=2$ with a fixed imaginary quadratic tower order of fundamental discriminant.  It does not prove special-$q$ descent, target splitting, or relation-matrix rank, and it does not cover the optimized interior range where $\eta\to\infty$.

## Lemma 1: bounded fibers of a primitive two-generator map

[PROVED] Fix an imaginary quadratic order $R$ and a Euclidean norm $\|\cdot\|$ on $R\otimes_\mathbb Z\mathbb R\simeq\mathbb C$.  There are constants depending only on $R$ with the following property.  Let $A,B\in R$ satisfy $(A,B)=R$, put
\[
 \Phi:R^2\longrightarrow R,\qquad \Phi(u,v)=Au+Bv,
\]
and set $M=\max(1,\|A\|,\|B\|)$.  If $H\ge C_RM$ and
\[
 \|w\|\le c_RMH,
\]
then
\[
 \#\{(u,v)\in R^2:\|u\|,\|v\|\le H,\ Au+Bv=w\}
 \ge c_R(H/M)^2.                                               \tag{BF}
\]

[PROVED] Since $(A,B)=R$, choose $C,D\in R$ with $AC+BD=1$.  Every solution is
\[
 (u,v)=(Cw-Bt,Dw+At),\qquad t\in R.                            \tag{12}
\]
Indeed the displayed pair maps to $w$, and the matrix
\[
 \begin{pmatrix}C&-B\\D&A\end{pmatrix}
\]
has determinant $1$, so it is an automorphism of $R^2$.

[PROVED] Over the real vector space, the affine plane $\Phi^{-1}(w)$ has a point of norm $O_R(\|w\|/M)$.  The kernel lattice is
\[
 \{(-Bt,At):t\in R\}
\]
and has a fundamental parallelogram of diameter $O_R(M)$.  Reducing any integral solution relative to the real minimum-norm point therefore gives an integral solution with coordinates
\[
 O_R(\|w\|/M+M).
\]
For $\|w\|\le c_RMH$ and $H\ge C_RM$, this solution lies in the half-sized coefficient box.  Adding every kernel vector with $\|t\|\le c_RH/M$ remains in the full box.  A fixed rank-two lattice has $\gg_R(H/M)^2$ such $t$, proving (BF).

[PROVED] The same proof applies to an affine map $z_0+Au+Bv$ after replacing $w$ by $w-z_0$, provided $\|z_0\|\le c_RMH$ or the target disk is translated accordingly.

## Lemma 2: smooth targets retain constant-order preimage density

[CITED] For a fixed primitive positive-definite quadratic norm form of negative fundamental discriminant, Barbulescu--Lachand Theorem 4.2 gives the random-integer-order density of $Y$-smooth primitive values in a norm disk, uniformly when
\[
 \exp((\log\log X)^{5/3+\epsilon})\le Y\le X(\log X)^{-\kappa}.
\]

[PROVED] Take $X=(c_RMH)^2$.  The number of primitive $w\in R$ with $\|w\|\le c_RMH$ and $Y$-smooth norm is
\[
 \gg_R X\,\frac{\Psi(Xe^{\alpha_R},Y)}{Xe^{\alpha_R}}.         \tag{13}
\]
Multiplying (13) by the fiber lower bound (BF) gives
\[
 \#\{(u,v)\text{ in the }H\text{-box}:N(Au+Bv)\text{ is }Y\text{-smooth}\}
 \gg_R H^4\,\frac{\Psi(Xe^{\alpha_R},Y)}{Xe^{\alpha_R}}.       \tag{14}
\]
The factors $M^2$ cancel between the target count and the fiber size.  Thus a large kernel step does not by itself create an additional $M^{-O(1)}$ density loss.

## Lemma 3: irreducibility with a prescribed nonzero evaluation

[PROVED] Let $\mathbb F_s$ be a finite field, $d\ge2$, $r\in\mathbb F_s$, and $c\in\mathbb F_s^\ast$.  The number $I_d(r,c)$ of monic irreducible polynomials $F\in\mathbb F_s[x]$ of degree $d$ satisfying $F(r)=c$ obeys
\[
 I_d(r,c)\ge
 \frac1d\left(\frac{s^d-1}{s-1}-d\,s^{d/2}\right).             \tag{15}
\]
In particular,
\[
 I_d(r,c)=\frac{s^d}{d(s-1)}
 \left(1+O(d\,s^{1-d/2})\right)
 =\Theta_s(s^{d-1}/d).                                        \tag{16}
\]

[PROVED] Translation reduces to $r=0$.  A monic irreducible polynomial with constant term $c$ has a root $\theta\in\mathbb F_{s^d}$ of degree exactly $d$ and norm $(-1)^dc$.  Every nonzero norm fiber has $(s^d-1)/(s-1)$ elements.  Elements of degree less than $d$ lie in the union of proper subfields, which has at most
\[
 \sum_{e\mid d,\ e<d}s^e\le d\,s^{d/2}
\]
elements.  Dividing the remaining roots by their $d$ conjugates proves (15).

[PROVED] Choose a rational auxiliary prime $q>Y$ and a prime ideal $\mathfrak q\mid q$ of $R$, with residue field size $s=N\mathfrak q$.  A nonzero $Y$-smooth norm cannot be divisible by $q$, so every accepted target $w$ has nonzero image in $R/\mathfrak q$.  Because $p$ is invertible modulo $\mathfrak q$, varying the coefficients of $U$ in
\[
 f=f_0+pU+KV
\]
makes $f\bmod\mathfrak q$ range over all degree-$d$ coefficient vectors.  Conditional on the prescribed nonzero evaluation $f(r)=c$, (15) therefore leaves a proportion $d^{-1+o(1)}$ whose reduction is irreducible.

[PROVED] Irreducibility modulo $\mathfrak q$ implies irreducibility over $\operatorname{Frac}(R)$ by the valuation/Gauss argument.  For
\[
 d=\Theta((\log Q/\log\log Q)^{1/3}),
\]
the factor $d^{1+o(1)}$ is $L_Q(1/3,o(1))$ and changes no leading complexity constant.  Taking the integer coefficient box much larger than $s$ makes reduction modulo $\mathfrak q$ equidistributed; for fixed $\eta=2$ and $q\asymp Y=L_Q(1/3,\beta)$, this enlargement remains below the $L_Q(2/3)$ coefficient scale.

## Lemma 4: residue restrictions preserve the fiber lower bound

[PROVED] Let $\mathfrak q$ be fixed for one input and let $s=N\mathfrak q$.  In the proof of (BF), restricting $t$ to one residue class modulo $\mathfrak q$ leaves
\[
 \gg_R \frac{H^2}{M^2s}
\]
kernel points, uniformly in the class, once $H/(M\sqrt s)\to\infty$.  This follows by counting a translate of the rank-two lattice $\mathfrak q$ in the disk $\|t\|\le c_RH/M$; its covolume is $s$ and its boundary error is lower order under the displayed growth condition.

[PROVED] Apply this simultaneously to the coefficient reductions of $U,V$.  For each fixed target evaluation $w\bmod\mathfrak q$, all compatible coefficient residue classes have asymptotically equal numbers of lifts in a sufficiently enlarged box.  Summing the classes whose polynomial reduction is irreducible and using (15) therefore loses only the factor $\Theta_s(1/d)$, rather than selecting an uncontrolled exceptional congruence class.

[PROVED] At fixed $\eta=2$, one may enlarge the coefficient radius by the factor $s^{1/2+o(1)}=L_Q(1/3,O(1))$ needed for this residue equidistribution.  When the underlying coefficient/norm scale is $L_Q(2/3,O(1))$, this changes constants but not the exponent $2/3$.

## Assembly for two relation sides

[PROVED] For $d=\kappa$ and ideal-coprime relation candidates, A003 proves that the constant-coefficient kernel increments
\[
 (p b^\kappa,K^{[\kappa]}(a,b))
\]
generate $R$.  Lemmas 1--2 therefore give a random-integer-order smoothness lower bound, averaged over the coefficient-randomized polynomial family, for each fixed candidate on one side.  Lemmas 3--4 remove reducible polynomials at only a $\Theta_s(1/d)$ density loss and a lower-exponent coefficient enlargement.

[PROVED] Randomize the two sides independently.  For each fixed candidate, the counts of admissible $f$- and $g$-coefficients multiply, so summing over candidates gives a joint count without assuming independence of the two **norm values for a fixed polynomial pair**.  Averaging over polynomial pairs then yields at least one irreducible pair with at least the average number of jointly smooth candidates.

[PROVED] If $X_f,X_g=L_Q(2/3,O(1))$ and $Y=B=L_Q(1/3,\beta)$, the resulting averaged joint density is
\[
 L_Q\!\left(1/3,-\frac{\gamma_f+\gamma_g}{3\beta}+o(1)\right),
\]
with worsened $\gamma_f,\gamma_g$ coming from the enlarged coefficient boxes.  Sampling polynomial pairs until one supplies enough relations can add another inverse-density factor, but it remains on the $L_Q(1/3,O(1))$ scale.

## Exact scope of the partial theorem

[CONDITIONAL: fixed imaginary quadratic $R$ of negative fundamental discriminant, $\eta=2$, $d=\kappa$, ideal-coprime dense candidates, and box/norm constants chosen as above] The modified polynomial-ensemble relation collector has a provable $L_Q(1/3,O(1))$ **relation-supply exponent** whenever its enlarged polynomial coefficients and relation norms remain $L_Q(2/3,O(1))$.

[PROVED] At the boundary $\ell_p=2/3$, $p$, $A^\kappa$, the auxiliary modulus, and the required coefficient bounds all remain products of $L_Q(2/3,O(1))$ or smaller quantities, so the norm exponent remains $2/3$ although the constant worsens.

[PROVED] For every fixed interior $\ell_p<2/3$, A003 shows that fixed $\eta=2$ already makes the standard dense-box norm exponent exceed $2/3$.  The modification therefore does not prove the requested interior exTNFS complexity.

[PROVED] A fixed tower such as $R=\mathbb Z[i]$ also requires $h=T^2+1$ to remain irreducible modulo the input characteristic, which restricts inputs to $p\equiv3\pmod4$.  Covering all $p$ would make the quadratic form vary and would again require uniformity absent from Theorem 4.2.

## Explicit boundary-family relation theorem

[PROVED] Consider an input sequence
\[
 Q=p^n,\qquad p=L_Q(2/3,c_p),\qquad p\equiv3\pmod4,\qquad
 n=2\kappa.
\]
Use $R=\mathbb Z[i]$, so $h=T^2+1$ is irreducible modulo $p$ and its norm form has fundamental discriminant $-4$.  Generate a random monic irreducible degree-$\kappa$ polynomial $k$ over $\mathbb F_{p^2}$ by sampling and deterministic irreducibility testing, and lift it coefficientwise to $K\in R[x]$ with coefficients of size $O(p)$.

[PROVED] Use independent polynomial families
\[
 f=K(1+v_f)+pU_f,\qquad g=K(1+v_g)+pU_g,                      \tag{17}
\]
where $v_f,v_g\in R$, $U_f,U_g\in R[x]$ have degree at most $\kappa$, and $1+v_f,1+v_g$ are nonzero modulo $p$.  Both reductions are nonzero scalar multiples of $k$, so both number fields retain the required map to $\mathbb F_Q$.  Lemma 3 with an auxiliary prime $q>B$ restricts to irreducible $f,g$ at a subleading density cost.

[PROVED] Put
\[
 A=L_Q(1/3,a),\qquad B=L_Q(1/3,\beta),\qquad
 m=c_p+\frac{a}{2c_p}.                                        \tag{18}
\]
The relation box has
\[
 A^4=L_Q(1/3,4a)
\]
candidates, while
\[
 \kappa\log A
 =\left(\frac{a}{2c_p}+o(1)\right)
 (\log Q)^{2/3}(\log\log Q)^{1/3}.
\]
Consequently the kernel generators $p b^\kappa$ and $K^{[\kappa]}(a,b)$ have coordinate size at most $L_Q(2/3,m+o(1))$ uniformly in the box.

[PROVED] Choose the randomized coefficient radius $H=L_Q(2/3,m+o(1))$ times the lower-exponent auxiliary residue factor required in Lemma 4.  Evaluating (17) on the relation box then gives relative-resultant coordinates of size at most $L_Q(2/3,2m+o(1))$ and absolute quadratic norms of size
\[
 X_f,X_g\le L_Q(2/3,4m+o(1)).                                 \tag{19}
\]

[CITED] Applying Barbulescu--Lachand Theorem 4.2 to the fixed Gaussian norm in Lemma 2 and Canfield--Erdos--Pomerance to its density gives the averaged joint success probability
\[
 \pi_{\rm joint}\ge
 L_Q\!\left(1/3,-\frac{8m}{3\beta}+o(1)\right).               \tag{20}
\]

[PROVED] Choose any $\beta$ with $\beta c_p>1/3$, followed by any
\[
 a>
 \frac{\displaystyle\beta+\frac{8c_p}{3\beta}}
      {\displaystyle4-\frac{4}{3\beta c_p}}.                  \tag{21}
\]
Substituting $m=c_p+a/(2c_p)$ shows that
\[
 4a>\beta+\frac{8m}{3\beta}.
\]
Hence the average number of jointly smooth candidates in one polynomial pair is asymptotically larger on the $L$ scale than the $L_Q(1/3,\beta)$ factor-base size.

[PROVED] If $X(f,g)$ is the number of jointly smooth candidates for one polynomial pair and $T=A^4$, then $0\le X\le T$.  Once $\mathbb E X\ge2L_Q(1/3,\beta)$,
\[
 \Pr[X\ge L_Q(1/3,\beta)]
 \ge\frac{\mathbb EX-L_Q(1/3,\beta)}
          {T-L_Q(1/3,\beta)}
 \ge L_Q\!\left(1/3,-\frac{8m}{3\beta}+o(1)\right).            \tag{22}
\]
Thus sampling a polynomial pair, scanning its relation box, and rejecting pairs with too few relations has expected cost
\[
 L_Q\!\left(
 1/3,\ 4a+\frac{8m}{3\beta}+o(1)
 \right).                                                     \tag{23}
\]
The associated sparse linear algebra, once adequate rank is supplied, costs $L_Q(1/3,2\beta+o(1))$.

[PROVED] Equations (17)--(23) give an unconditional, explicitly randomized $L_Q(1/3,O(1))$ **relation-supply algorithm** for this boundary subfamily, with a worse and nonoptimized constant.  It proves neither rank nor individual logarithms and therefore is not an unconditional DLP complexity theorem.

## Remaining gaps

[PROVED] Equations (17)--(23) promote the relation-supply component to a formal boundary-subfamily theorem with an explicit, nonoptimized constant expression.  Extending it to the strict interior range would require a smooth-value theorem uniform in growing $\eta$.

[PROVED] Even that promotion would settle only relation supply.  Initial splitting, special-$q$ descent, and the rank escape condition (R2) remain open, so this is not an unconditional DLP algorithm.

## Outcome

[PROVED] The two obstacles “bounded preimages” and “irreducible randomized polynomials” can be handled at fixed quadratic tower degree without a leading-exponent loss: Lemma 1 supplies the first and Lemma 3 supplies the second.

[PROVED] The surviving fundamental obstruction is degree uniformity.  The proof uses one fixed quadratic norm form, whereas optimized interior exTNFS necessarily has $\eta\to\infty$.

[EMPIRICAL: prime fields $s\in\{2,3,5,7,11\}$, $2\le d\le8$, all $c\ne0$] An independent exact Möbius/norm-fiber count checked 161 instances of (15); the smallest actual-minus-lower-bound slack was $1.5$.

[EMPIRICAL: $R=\mathbb Z[\iota]/(\iota^2+2)$, $A=5$, $B=1-\iota$, targets $[-5,5]^2$] The identity $5(-1)+(1-\iota)(2+2\iota)=1$ supplied solutions for all 121 targets, with maximum coefficient magnitude 30.
