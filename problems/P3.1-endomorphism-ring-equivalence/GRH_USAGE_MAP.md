# GRH usage map - P3.1

## Scope and conclusion

- [CITED] The audited proof is Benjamin Wesolowski, *The supersingular isogeny path and endomorphism ring problems are equivalent*, FOCS 2021 proceedings (published 2022), arXiv:2111.01481v1; theorem numbers below refer to that version.
- [CITED] The proof establishes expected-polynomial-time equivalence of $\ell$-`IsogenyPath`, `MaxOrder`, and `EndRing` under GRH (Wesolowski 2022, Theorems 7.2, 7.4, 8.1, and 8.3).
- [CITED] The later unconditional equivalence of unrestricted `Isogeny`, `EndRing`, and `MaxOrder` does **not** settle the smooth/prescribed-degree problem: its authors explicitly retain GRH for the reduction from $\ell$-`IsogenyPath` to `EndRing` (Herlédan Le Merdy--Wesolowski 2026, Theorem 1 and Section 1.1).
- [CITED] The latest checked source is arXiv:2502.17010v2, dated 2026-02-02; a literature search through 2026-06-29 found no later primary source claiming a corrected unconditional classical reduction for $\ell$-`IsogenyPath`.

[PROVED] The old proof as written has four direct GRH leaves:

1. [CONDITIONAL: GRH] **D1 - a small auxiliary Frobenius prime:** construct $q_p=O((\log p)^2)$ defining a small special quaternion model.
2. [CONDITIONAL: GRH] **D2 - primes represented by one fixed quadratic-form class:** obtain a uniform main term with square-root error at radius polynomial in the discriminant.
3. [CONDITIONAL: GRH] **D3 - a uniform Titchmarsh estimate in a polynomial-size modulus range:** allow moduli as large as a fixed power of the sampled integer.
4. [CONDITIONAL: GRH] **D4 - expansion from polylogarithmic prime-ideal generators:** randomize a quadratic form within its class group in polynomial time.

- [PROVED] Every GRH-qualified result in the audited paper is a direct instance of D1--D4 or inherits its assumption from them; the exhaustive table below gives the dependency closure.
- [PROVED] The additional appeal to the Riemann hypothesis in Theorem 6.4 is unnecessary: the unconditional prime number theorem supplies the required lower bound.
- [PROVED] Session 2 removes D2 as a necessary assumption: `attempts/A003-direct-quaternary-prime-sampler.md` gives an unconditional rank-four replacement for Proposition 3.8. D1, D3, and D4 remain unresolved in the smooth-degree reduction.

## Dependency summary

```text
D1 -> Lemmas 2.2, 2.3, 2.5, 2.6 -> Lemmas 7.1, 7.3
D2 -> Theorem 3.1 -> Propositions 3.4--3.8 -> Theorems 6.3 and 8.3
D3 -> Theorem 4.4 -> Theorem 4.2 -> Corollary 4.3 -> Theorem 5.1
D4 -> Lemmas 5.3 and 5.4 ---------------------------> Theorem 5.1
D1 + D3 + D4 -> Corollary 5.8 ---------------------> Theorem 6.3
D1 + D2 + D3 + D4 -> Theorem 6.3 -> Theorem 6.4
Theorem 6.4 -> Theorems 7.2 and 8.1
Theorems 6.3 and 6.4 -> Theorem 7.4
D1 + D2 -> Theorem 8.3
```

- [PROVED] `Deuring correspondence`, lattice reduction, Brandt/$\ell$-isogeny graph mixing, quaternion ideal arithmetic, and the formal correctness arguments do not themselves invoke GRH in this proof; GRH enters when the algorithms require small or statistically plentiful arithmetic representatives.

## Direct GRH leaf D1 - the small special quaternion model

### Exact use

- [CONDITIONAL: GRH] Lemma 2.2 chooses, for $p\equiv1\pmod 8$, the least prime $q_p\equiv3\pmod4$ with $(p/q_p)=-1$ and uses $q_p=O((\log p)^2)$.
- [CONDITIONAL: GRH] Eisenträger--Hallgren--Lauter--Morrison--Petit (2018), Proposition 1, derives this from effective Chebotarev in $\mathbb Q(\sqrt p,i)$, whose absolute discriminant is $4^2p^2$ in their normalization.
- [CONDITIONAL: GRH] Lemma 2.3 uses the same bound to make both $[\mathcal O_0:R+Rj]$ and $|\operatorname{disc}(R)|$ of order $O((\log p)^2)$.
- [CONDITIONAL: GRH] Lemmas 2.5 and 2.6 inherit D1 for $p\equiv1\pmod8$: the special curve and its quaternion/endomorphism dictionary are computed by enumerating degree-$q_p$ isogenies, so polynomial time requires $q_p=\operatorname{poly}(\log p)$ (Eisenträger et al. 2018, Proposition 3).

### Strength actually needed

- [PROVED] A fixed bound $q_p\le(\log p)^C$ and a polynomial-time method to find it would suffice; the exponent $2$ is convenient but not essential.
- [PROVED] A bound $q_p\le p^C$ does not by itself give a polynomial-time construction by enumeration, since enumerating primes up to $p^C$ is exponential in the input length $\log p$.

### Unconditional status

- [CITED] Unconditional effective Chebotarev gives a least prime in a prescribed Frobenius class bounded by a fixed power of the relevant field invariants; for example, Thorner--Zaman (2017), Theorem 1.1, gives an explicit fixed-power bound.
- [PROVED] Applied to $\mathbb Q(\sqrt p,i)$, such a theorem gives $q_p\le p^{O(1)}$, not the polylogarithmic cutoff or polynomial-time search needed by the old reduction.
- [CITED] Herledan Le Merdy--Wesolowski (2026), Proposition 13, constructs a flexible quaternion model and dictionary directly from an endomorphism-ring basis, so the special-curve dictionary manifestation of D1 can be bypassed.
- [PROVED] This does not remove D1 from Wesolowski's smooth-equivalent-ideal route: Corollary 5.8 and Algorithm 2 still use a binary suborder whose discriminant is polylogarithmic only through D1, and Theorem 5.1 contains work polynomial in that discriminant's numerical value; see A006.
- [CITED] Herlédan Le Merdy--Wesolowski (2026), Section 3, avoids the issue for unrestricted `MaxOrder` by allowing the solver to choose a quaternion model and then translating between models; it does not produce a smooth $\ell$-path.

## Direct GRH leaf D2 - primes represented by a fixed form

### Exact use

- [CONDITIONAL: GRH] Theorem 3.1 states that for a primitive positive-definite binary quadratic form $f$ of discriminant $D$,
  $$
  \pi_f(\rho)=\frac{\delta\rho}{h(D)\log\rho}
  +O\!\left(\rho^{1/2}\log(|D|\rho)\right),
  $$
  where $\delta\in\{1/2,1\}$ depends on inversion symmetry; Wesolowski attributes this to effective Chebotarev of Lagarias--Odlyzko.
- [CONDITIONAL: GRH] Proposition 3.4 takes $\rho=O_\epsilon(|D|^{1+\epsilon})$ so the main term dominates the error and uniform lattice sampling hits a prime with inverse-polylogarithmic probability.
- [CONDITIONAL: GRH] Propositions 3.5 and 3.6 reduce higher-rank prime representation to Proposition 3.4.
- [CONDITIONAL: GRH] Theorem 3.7 applies Proposition 3.5 to the norm form $q_I$ of discriminant $p^2$, producing an equivalent prime-norm ideal with norm $O_\epsilon(p^{2+\epsilon})$.
- [CONDITIONAL: GRH] Proposition 3.8 adds a norm interval and the condition that $\ell$ be a quadratic nonresidue modulo that prime; it still derives its success probability from the same prime-representation input.

### Strength actually needed

- [PROVED] The reduction needs an efficiently samplable range of bit length $\operatorname{poly}(\log|D|)$ in which a random represented value is prime with probability at least $1/\operatorname{poly}(\log|D|)$.
- [PROVED] Existence of one prime below $|D|^C$ is insufficient without a density or search theorem, because exhaustive enumeration of the $\Theta(\rho/\sqrt{|D|})$ lattice points is exponential in $\log|D|$.

### Unconditional status

- [CITED] Thorner--Zaman (2017), Theorem 1.2, proves that every primitive positive-definite binary quadratic form of discriminant $D$ represents a prime $\ll|D|^{694}$.
- [PROVED] That theorem controls the magnitude of a least prime but does not provide the inverse-polylogarithmic sampling density required by Proposition 3.4; naive use therefore remains exponential in $\log|D|$.
- [CITED] Sardari (2019), Theorem 1.1 and Corollary 1.3, give unconditional coverage results for a positive proportion of form/ideal classes.
- [PROVED] An average-over-classes theorem does not certify the fixed adversarial form $q_I$ supplied to Theorem 3.7, so it does not prove the worst-case reduction.
- [PROVED] Brandt mixing does not repair that mismatch because Proposition 3.5's deterministic LLL-and-gcd binary restriction has no checked pushforward anti-concentration bound; see A002.
- [PROVED] A003 bypasses the binary restriction. Rouse's effective strong-local quaternary coefficient bounds, fixed-rank CVP, and explicit primes-in-progressions estimates yield an inverse-polynomial direct sampler on a residue sublattice of $q_I$.
- [PROVED] This supplies the prime-norm interval and quadratic-nonresidue condition required by Proposition 3.8 in expected time polynomial in $\log p$ and the numerical value of $\ell$.

## Direct GRH leaf D3 - uniform Titchmarsh range

### Exact use

- [CONDITIONAL: GRH] Theorem 4.4 adapts Assing--Blomer--Li (2020), Theorem 2.1, in the range $b,c,d\le x^\delta$ and obtains a power-saving error $O(x^{1-\delta})$.
- [CONDITIONAL: GRH] Theorem 4.2 and Corollary 4.3 use this to count, uniformly over a genus, representations of $n$ as a prime term plus a binary quadratic-form value when the parameters are fixed powers of $n$.
- [CONDITIONAL: GRH] Theorem 5.1 turns that count into an expected-polynomial-time solver for
  $$
  \det(\gamma)^2 f(s,t)+b f_\gamma(x,y)=n
  $$
  with only $\log n\ge c\log b$ in the $b$ parameter.

### Checked unconditional substitute and failure point

- [CITED] Assing--Blomer--Li (2020), Theorem 2.1, is unconditional when its auxiliary moduli are bounded by $(\log x)^C$, with an error saving arbitrary powers of $\log x$; GRH is used to enlarge them to $x^{\delta'}$ and obtain a power saving.
- [PROVED] In the quaternion application $b=p$. Replacing $b\le x^\delta$ by $b\le(\log x)^C$ forces $\log x\ge p^{1/C}$.
- [PROVED] Since $x$ is on the scale of the represented integer $n$, the unconditional range makes the output bit length $\log n$ exponential in the input length $\log p$; this does not preserve a polynomial-time reduction.

## Direct GRH leaf D4 - small-prime class-group expansion

### Exact use

- [CONDITIONAL: GRH] Lemma 5.3 invokes Jao--Miller--Venkatesan (2009), Theorem 1.1 and Corollary 1.3, to use prime ideals of norm
  $$
  C=O_\epsilon\!\left((\log|d|)^{2+\epsilon}+\omega(m)^{1+\epsilon}\right)
  $$
  as an expanding Cayley multiset and to mix in $O(\log|d|)$ steps.
- [CONDITIONAL: GRH] This yields a common integer $B$, coprime to $md$, whose divisors are represented across all form classes and whose bit length is
  $$
  O_\epsilon\!\left(\log|d|\left((\log|d|)^{2+\epsilon}+\omega(m)^{1+\epsilon}\right)\right).
  $$
- [CONDITIONAL: GRH] Lemma 5.4 uses the same small-prime generation input but performs explicit class-group computation, costing polynomial time in $|d|$ rather than $\log|d|$.
- [CONDITIONAL: GRH] Theorem 5.1 uses Lemmas 5.3/5.4 to randomize the form $f_\gamma$ within its class/genus before applying the average count of Theorem 4.2.

### Unconditional status

- [CITED] Jao--Miller--Venkatesan (2009), Section 1 and Section 7.2, state that their polylogarithmic-prime spectral gap uses GRH and that even cancellation for quadratic characters meets the least-prime-quadratic-nonresidue obstruction; they record only typical-modulus unconditional substitutes.
- [CITED] Minkowski's ideal-class bound implies that an imaginary-quadratic class group is generated by prime ideals of norm $O(\sqrt{|d|})$.
- [PROVED] Indeed, choose in each class an integral ideal of norm $O(\sqrt{|d|})$ and factor it; every prime-ideal factor has no larger norm.
- [PROVED] This unconditional cutoff is exponential in the input length $\log|d|$, and generation alone supplies no rapid-mixing bound. Substituting it in Lemma 5.3 makes $\log B$ exponential and does not preserve polynomial time.

## Removable use D5 - RH in the powersmooth product

- [CONDITIONAL: RH] The proof of Theorem 6.4 cites the prime number theorem with the Riemann hypothesis to estimate the product of primes in
  $$
  (\log p)^{c_0}<\ell<(\log p)^{c_0+\delta}.
  $$
- [PROVED] This appeal to RH can be removed. With $X=(\log p)^{c_0}$ and $Y=(\log p)^{c_0+\delta}$, the unconditional prime number theorem gives $\vartheta(Y)-\vartheta(X)=Y-X+o(Y)\sim Y$; for any fixed $\delta>0$, this eventually exceeds $(\log p)^{c_0}$, which is the only lower bound used in Theorem 6.4.
- [PROVED] Removing D5 does not make Theorem 6.4 unconditional because it still calls Theorem 6.3, which inherits D1--D4.

## Exhaustive lemma/theorem table

| Result in Wesolowski 2022 | Role | Dependency | Unconditional assessment |
|---|---|---|---|
| Lemma 2.2 | Small $q_p$ and model $B_{p,\infty}=(-q_p,-p)$ | [CONDITIONAL: GRH] Direct D1 | [CITED] Fixed-power Chebotarev bounds exist; no required polylog search bound. |
| Lemma 2.3 | Small special order and small quadratic discriminant | [CONDITIONAL: GRH] D1 | [PROVED] Its polynomial-size guarantee fails with only $q_p\le p^{O(1)}$. |
| Lemma 2.5 | Special curve and explicit dictionary | [CONDITIONAL: GRH] D1 when $p\equiv1\pmod8$ | [CITED] The 2026 unrestricted reduction avoids needing this global dictionary. |
| Lemma 2.6 | Powersmooth ideal-to-isogeny translation | [CONDITIONAL: GRH] Inherits D1 through Lemma 2.5 | [CITED] Modern arbitrary-ideal translation removes this need for unrestricted `Isogeny`, not for prescribed smooth degree. |
| Theorem 3.1 | Prime count for a fixed binary form | [CONDITIONAL: GRH] Direct D2 | [CITED] Unconditional least-prime and average-class results lack the required worst-case sampling density. |
| Propositions 3.4--3.6 | Prime sampling for binary/higher-rank forms | [CONDITIONAL: GRH] D2 in the original proof | [PROVED] A003 bypasses these propositions for rank-four quaternion norm lattices; it does not give a general binary sampler. |
| Theorem 3.7 | Equivalent ideal of prime norm | [CONDITIONAL: GRH] D2 in the original proof | [PROVED] A003 supplies the needed special-case sampler directly. |
| Proposition 3.8 | Prime norm in an interval with a residue constraint | [CONDITIONAL: GRH] D2 in the original proof | [PROVED] A003 gives an unconditional replacement with the same complexity convention, polynomial in numerical $\ell$. |
| Theorem 4.2 | Uniform representation count over form classes | [CONDITIONAL: GRH] D3 | [CITED] ABL's unconditional modulus range is only polylogarithmic in the sampled value. |
| Corollary 4.3 | Lower bound extracted from Theorem 4.2 | [CONDITIONAL: GRH] D3 | [PROVED] Inherits the same exponential-output loss unconditionally. |
| Theorem 4.4 | Uniform primes-in-progressions/Titchmarsh estimate | [CONDITIONAL: GRH] Direct D3 | [CITED] ABL gives the precise weaker unconditional range. |
| Lemma 5.3 | Polylog-time class randomization | [CONDITIONAL: GRH] Direct D4 | [CITED] No all-discriminant polylog-prime expansion is provided unconditionally by JMV. |
| Lemma 5.4 | Small-discriminant class enumeration | [CONDITIONAL: GRH] D4 for its small generators | [PROVED] Its stated runtime is already polynomial in $|d|$, not $\log|d|$. |
| Theorem 5.1 | Quaternion norm-equation solver | [CONDITIONAL: GRH] D3 + D4 | [PROVED] Both the uniform count and class randomization are essential in its proof. |
| Corollary 5.8 | Represent prescribed norms in $\mathcal O_0$ | [CONDITIONAL: GRH] D1 + D3 + D4 | [PROVED] Uses the small special form and Theorem 5.1. |
| Theorem 6.3 | `EquivIdeal` / quaternion path core | [CONDITIONAL: GRH] D1 + D2 + D3 + D4 | [PROVED] Calls Proposition 3.8, Corollary 5.8, and Theorem 5.1. |
| Theorem 6.4 | Powersmooth equivalent ideal | [CONDITIONAL: GRH] Inherits D1--D4 from Theorem 6.3; D5 is removable | [PROVED] Unconditional PNT replaces D5 only. |
| Lemma 7.1 | Isogeny-to-ideal translation | [CONDITIONAL: GRH] D1 when $p\equiv1\pmod8$ | [PROVED] Its enumeration calls Lemma 2.6. |
| Theorem 7.2 | `MaxOrder` reduces to $\ell$-`IsogenyPath` | [CONDITIONAL: GRH] D1--D4 via Theorem 6.4 | [PROVED] No additional analytic input occurs. |
| Lemma 7.3 | Prime-power ideal-to-isogeny translation | [CONDITIONAL: GRH] D1--D4 via Theorem 6.4 and Lemma 2.6 | [PROVED] No additional analytic input occurs. |
| Theorem 7.4 | $\ell$-`IsogenyPath` reduces to `MaxOrder` | [CONDITIONAL: GRH] D1--D4 via Theorems 6.3/6.4 | [CITED] This is the direction the 2026 paper still leaves conditional. |
| Theorem 8.1 | `EndRing` reduces to `MaxOrder` | [CONDITIONAL: GRH] D1--D4 via Theorem 6.4 | [PROVED] No additional analytic input occurs. |
| Theorem 8.3 | `MaxOrder` reduces to `EndRing` | [CONDITIONAL: GRH] D1 + D2 | [PROVED] Step 3 calls Proposition 3.5, and the output model uses small $q_p$. |

## Current frontier and falsifier

- [CITED] Herlédan Le Merdy--Wesolowski (2026) bypass D1--D4 for unrestricted `Isogeny` by combining a flexible quaternion model, a local quaternion/endomorphism dictionary, arbitrary-ideal-to-isogeny translation, and a factorization-free `MOER` route.
- [CITED] The same paper explicitly says known unconditional results remain insufficient for isogenies of prescribed degree, because that requirement returns to integers represented by quadratic forms.
- [CITED] Mamah (2024) claims a factoring-oracle replacement, but Herlédan Le Merdy--Wesolowski (2026, footnote in Section 1.1) report a mistake in its proof; the checked source does not identify a published correction.
- [PROVED] Therefore Task 1, as stated with smooth degree, remains open in the checked literature; the audit does not claim an unconditional equivalence.
- [PROVED] A003 replaces D2, so the current analytic target is the D3+D4 prescribed-norm combination; merely improving a least-prime exponent does not address it.
- [PROVED] The broader constructive target is an exact fixed-target solver on an arbitrary maximal-order quaternary norm lattice: such a solver would bypass the special-order D1 dependency together with the D3+D4 sampling architecture, whereas Rouse's existence theorem alone does not locate a representation.

## Source verification record

- [CITED] Full text checked: Wesolowski, arXiv:2111.01481v1, 31 pages.
- [CITED] Full text checked: Herlédan Le Merdy--Wesolowski, arXiv:2502.17010v2, 33 pages.
- [CITED] Full text checked: Eisenträger--Hallgren--Lauter--Morrison--Petit, EUROCRYPT 2018, 40-page author/conference PDF.
- [CITED] Full text checked: Assing--Blomer--Li, arXiv:2005.13915v1, 35 pages.
- [CITED] Full text checked: Jao--Miller--Venkatesan, arXiv:0811.0647v2, 24 pages.
- [CITED] Full text checked: Thorner--Zaman, arXiv:1604.01750v2, 45 pages.
- [CITED] Full text checked: Sardari, arXiv:1803.03218v2, 53 pages.
- [CITED] Full text checked: Rouse, arXiv:1802.03437v1, 18 pages.
- [CITED] Full text checked: Ditchen, arXiv:1312.1502v1, 33 pages.
- [CITED] Full text checked: Goren--Love, arXiv:2307.16828v1, 26 pages.
- [CITED] Full text checked: Bennett--Martin--O'Bryant--Rechnitzer, arXiv:1802.00085v3, 103 pages.
- [CITED] Full scanned text checked: Kannan, *Mathematics of Operations Research* 12(3), 1987, 26 pages.
