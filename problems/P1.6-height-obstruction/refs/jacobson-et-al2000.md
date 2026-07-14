# Jacobson--Koblitz--Silverman--Stein--Teske (2000)

Michael J. Jacobson, Neal Koblitz, Joseph H. Silverman, Andreas Stein, and
Edlyn Teske, "Analysis of the Xedni Calculus Attack," *Designs, Codes and
Cryptography* 20 (2000), 41--64.

Primary-source copy:
<https://pages.cpsc.ucalgary.ca/~jacobs/PDF/xedni.pdf>

## Result in repository notation

[CITED] The xedni algorithm lifts $r$ random linear combinations of an ECDLP
pair, usually with $4\leq r\leq6$, to rational points on one rational elliptic
curve and succeeds only when those rational points are dependent.

[CITED] Theorem 4.1 bounds the success probability by $C_0/p$ under the lemma's
discriminant-to-selected-height assumption and Lang's conjectural lower bound
for the least non-torsion canonical height.

[CITED] The proof bounds coefficients of a rational dependence relation by an
absolute constant and then counts the chance that the random finite-field
reductions satisfy such a small relation.

## Quantitative check

[CITED] Section 5.4.1 reports that Experiment C uses
$E/\mathbb F_{257}:y^2=x^3+88x-41$, generator $(2,20)$, and group order 263;
after excluding the identity and $\pm P_1$, the probability of a relation with
coefficients at most two is $4/(263-3)=1/65$.

[EMPIRICAL: exact enumeration at p=257] `code/reproduce_xedni_probability.py`
recounts 263 curve points, 260 eligible choices, and four favorable choices.

## What it rules out and leaves open

[CITED] The paper's asymptotic conclusion is conditional and concerns rare
dependence with bounded relation coefficients, not a $p^c$ lower bound on the
heights of all possible selected lifts.

[CITED] The paper reports 100,000-run experiments at $p=17,67,257,5167$ and
finds that dependence becomes rare as discriminants grow, while explicitly
warning that its practical estimates depend on modeling assumptions.

