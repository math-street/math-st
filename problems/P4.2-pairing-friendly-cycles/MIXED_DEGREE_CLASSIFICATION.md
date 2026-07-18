# Global classification for mixed quadratic/quartic 2-cycle degrees

## Theorem

[PROVED] Let \(5\le p<q\) form a prime-order 2-cycle. Suppose one exact
embedding degree lies in
\[
 Q_2=\{3,4,6\}
\]
and the other lies in
\[
 Q_4=\{5,8,10,12\}.
\]
Then the only possibility is
\[
 (p,q)=(7,11),\qquad(k_1,k_2)=(10,3).
\]

## Quadratic side second

[PROVED] Put \(c=q-p\). If \(k_2\in Q_2\), write
\[
 \Phi_{k_2}(c)=np.
\]
The Hasse bounds from `QUADRATIC_DEGREE_CLASSIFICATION.md` give
\(1\le n\le6\). Hence
\[
 n q=\Phi_{k_2}(c)+nc=:D_n(c),
\]
where \(D_n(c)=c^2+d_nc+1\) is monic quadratic.

[PROVED] If \(k_1\in Q_4\), the remaining cyclotomic condition is equivalent
to
\[
 D_n(c)\mid n\Phi_{k_1}(-c).
\]
Polynomial division by the monic \(D_n\) has an integral linear remainder
\[
 R_n(c)=u_nc+v_n.
\]
Thus the divisibility implies \(D_n(c)\mid R_n(c)\).

## Quadratic side first

[PROVED] If \(k_1\in Q_2\), write
\[
 \Phi_{k_1}(-c)=mq,\qquad1\le m\le3.
\]
Then
\[
 mp=\Phi_{k_1}(-c)-mc=:D_m(c),
\]
again a monic quadratic, and the quartic condition becomes
\[
 D_m(c)\mid m\Phi_{k_2}(c).
\]
Its polynomial remainder modulo \(D_m\) is again integral and linear.

## Finite bound

[PROVED] For either orientation, write \(D(c)=c^2+dc+1\) and
\(R(c)=uc+v\). If
\[
 c>|d|+|u|+|v|+2,
\]
then
\[
 D(c)\ge c^2-|d|c+1>|u|c+|v|\ge|R(c)|.
\]
No nonzero \(R(c)\) can then be divisible by \(D(c)\). If \(R\) is the zero
polynomial, the case must be treated as an identity family.

[EMPIRICAL: all 108 bounded multiplier cases] None of the mixed cases has
zero polynomial remainder. The largest exhaustive even-gap bound is 2,649.
The complete certificate contains 73 empty cases and 43 cases with at least
one divisibility candidate, producing 116 rows in total
(`data/classify_mixed_degree_pairs_20260718.csv`).

[EMPIRICAL: every retained even gap through its proved case bound] Exactly one
row has prime Hasse fields and the prescribed exact degrees:
\[
 k_1=10,\quad k_2=3,\quad n=3,\quad c=4,\quad(p,q)=(7,11).
\]
The other candidates fail quadratic quotient integrality, quartic
divisibility, primality, Hasse, or exact-degree checks.

[PROVED] The multiplier bounds, linear-remainder bound, absence of identity
cases, and complete finite certificate cover every mixed ordered pair. This
proves the theorem.
