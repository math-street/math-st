# Frozen length-3 conditions and search space - P4.2 SG-05

This file was written before the length-3 search was run.

## Algebraic conditions

[PROVED] For a directed 3-cycle
\[
 E_1/\mathbb F_{p_1}\longrightarrow
 E_2/\mathbb F_{p_2}\longrightarrow
 E_3/\mathbb F_{p_3}\longrightarrow E_1,
\]
the necessary and sufficient order/trace equations are
\[
 \#E_i(\mathbb F_{p_i})=p_{i+1},\qquad
 t_i=p_i+1-p_{i+1},
\]
with indices modulo 3. Summation gives \(t_1+t_2+t_3=3\).

[PROVED] With prime group orders, the exact embedding degrees are
\[
 k_1=\operatorname{ord}_{p_2}(p_1),\quad
 k_2=\operatorname{ord}_{p_3}(p_2),\quad
 k_3=\operatorname{ord}_{p_1}(p_3).
\]
Each claimed \(k_i\) is checked at every positive exponent through \(k_i\).

[PROVED] Unlike a 2-cycle, a 3-cycle does not force the three Frobenius
discriminants \(t_i^2-4p_i\) to agree. The search therefore records the
fundamental discriminant and conductor separately for every position.

## Frozen finite space

[PROVED] The search covers directed cycles on three distinct primes
\(5\leq p_i<2^{16}\). A directed edge \(p_i\to p_{i+1}\) is retained exactly
when \((p_i+1-p_{i+1})^2\leq4p_i\). Cyclic rotations are identified, while
the reverse orientation remains distinct unless it yields the same directed
edge sequence.

[PROVED] A full pairing-friendly hit requires all three exact embedding
degrees to belong to \(K=\{3,4,\ldots,12\}\). The candidate ledger records
every directed 3-cycle for which at least two positions satisfy this condition;
one-position and zero-position cases remain counted in the summary but are not
expanded into rows.

[CITED] Every retained trace is realized by an elliptic curve over its prime
field (Deuring's theorem as stated in Belles-Munoz--Jimenez Urroz--Silva 2022,
Section 2.1). Distinct primes and the Hasse bound make every curve ordinary.

[PROVED] No CM discriminant or \(\rho\) value is filtered. Per-curve rho is
\(\rho_i=\log(p_i)/\log(p_{i+1})\), cycle rho is
\(\rho_{\max}=\max_i\rho_i\), and the product of the three per-curve values is
1.

## Predeclared outcome criteria

[CONJECTURE] The 16-bit search will find no full length-3 hit. This is refuted
by any directed triple with all three exact degrees in 3 through 12. Any hit
must be converted to three explicit equations and independently point-counted
before it is reported as an exhibited cycle.

