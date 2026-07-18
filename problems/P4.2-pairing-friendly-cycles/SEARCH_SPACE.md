# Frozen first search space - P4.2 SG-03

This file was written before the SG-04 search was run.

## Objects enumerated

[PROVED] The search enumerates every unordered pair of distinct primes
\(5\leq p<q<2^{16}\). It retains a pair as a prime-order 2-cycle isogeny-class
candidate exactly when
\[
  t_1=p+1-q,\qquad t_2=q+1-p
\]
satisfy \(t_1^2\leq4p\) and \(t_2^2\leq4q\).

[CITED] Every retained trace is ordinary and is realized by an elliptic curve
over the corresponding prime field (Waterhouse 1969). Here ordinarity follows
because the distinct-prime condition excludes \(t_i=0\), while Hasse's bound
for \(p_i\geq5\) gives \(|t_i|<p_i\).

## Pairing condition

[PROVED] For each retained pair, the search computes the exact multiplicative
orders
\[
  k_1=\operatorname{ord}_q(p),\qquad
  k_2=\operatorname{ord}_p(q)
\]
when they are at most 12. A hit requires both exact degrees to lie in
\(K=\{3,4,\ldots,12\}\). Degrees 1 and 2 are excluded as the deliberately
fixed non-pairing-friendly baseline; a degree above 12 is recorded as
`>12` rather than guessed.

## CM discriminants

[PROVED] No CM discriminant is pre-excluded. For every retained pair the
search decomposes the common negative Frobenius discriminant as
\[
  t_1^2-4p=t_2^2-4q=D_K f^2,
\]
where \(D_K\) is fundamental. Therefore the covered discriminants are exactly
all fundamental \(D_K\) induced by the enumerated prime pairs; necessarily
\(|D_K|<2^{18}\). The output records both \(D_K\) and \(f\).

## Rho convention and range

[PROVED] The search records
\(\rho_{\max}=\max\{\log p/\log q,\log q/\log p\}\) and does not filter on it.
Every retained pair has \(\rho_{\max}<2\) by the Hasse-bound proof in
`NOTES.md`.

## Near-misses and ordering

[PROVED] Enumeration order is increasing \(p\), then increasing \(q\).
The candidate CSV includes every Hasse-valid prime pair for which at least one
of \(k_1,k_2\) belongs to \(K\), labeled `hit`, `e1_only`, or `e2_only`.
The summary separately counts all prime pairs and all Hasse-valid pairs, so a
cold reader can audit exactly where rows were filtered.

## Positive and negative criteria

[CONJECTURE] A positive arithmetic result is any `hit` whose degree pair is
not \((6,4)\); it becomes an exhibited curve cycle only after explicit curves
are constructed and independently point-counted. A negative result is zero
such arithmetic hits, and is claimed only for the prime, trace, and embedding
degree bounds above.

