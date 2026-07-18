# Global classification for 2-cycle degrees in {3,4,6}

## Theorem

[PROVED] Let \(5\le p<q\) be primes forming a prime-order 2-cycle. If both
exact embedding degrees lie in {3,4,6}, then their ordered pair is (6,4) or
(4,6), and the fields have the corresponding MNT parameterization from
`MNT_CLASSIFICATION.md`. No ordered pair among
\[
 \{3,4,6\}^2\setminus\{(6,4),(4,6)\}
\]
occurs.

## Bounded multiplier equation

[PROVED] Put \(c=q-p>0\). The two Hasse inequalities are
\[
 (c-1)^2\le4p,\qquad(c+1)^2\le4q.
\]
For \(p\ge7\), the first gives \(c\le1+2\sqrt p<p\). The case \(p=5\)
forces \(q=7\) and has exact degree pair (6,4), so it is already MNT.

[PROVED] For \(k_1=\operatorname{ord}_q(p)\) and
\(k_2=\operatorname{ord}_p(q)\), cyclotomic divisibility gives
\[
 \Phi_{k_1}(-c)=mq,\qquad \Phi_{k_2}(c)=np
\]
for positive integers \(m,n\). For degrees 3, 4, and 6, write
\[
 \Phi_{k_1}(-c)=c^2+a c+1,\qquad
 \Phi_{k_2}(c)=c^2+b c+1,
\]
where
\[
 a=(-1,0,1),\qquad b=(1,0,-1)
\]
in degree order (3,4,6).

[PROVED] Since either quadratic is at most \(c^2+c+1\), Hasse gives
\[
 c^2+c+1\le4p+3c=4q-c<4q,
\]
so \(1\le m\le3\). Also \(c<p\) gives
\[
 c^2+c+1<7p,
\]
so \(1\le n\le6\).

[PROVED] Eliminating \(p,q\) using \(q-p=c\) gives the exact integer equation
\[
 (n-m)c^2+(na-mb-mn)c+(n-m)=0. \tag{1}
\]
Thus every case lies in the finite box
\[
 k_1,k_2\in\{3,4,6\},\quad1\le m\le3,\quad1\le n\le6,
\]
unless all three coefficients in (1) vanish.

## Identity cases

[PROVED] If \(n=m=s\), equation (1) is identically zero exactly when
\(s=a-b\). The positive possibilities are
\[
 (k_1,k_2,s)=(6,4,1),\ (4,6,1),\ (6,6,2).
\]
The first two give the two MNT parameterizations. In the last case,
\(\Phi_6(-c)=c^2+c+1\) is odd because \(c\) is even, while \(2q\) is even.
Hence the (6,6,2) identity cannot represent odd primes.

## Finite cases

[PROVED] For \(n\ne m\), equation (1) is quadratic. Exhausting the bounded
multiplier box yields only the following positive integral roots:

| Degrees | \(m,n\) | \(c\) | Rejection |
|---|---:|---:|---|
| (3,4) | (1,5) | 2 | fields \(1,3\) |
| (3,6) | (1,3) | 2 | fields \(1,3\) |
| (4,3) | (1,3) | 1 | odd gap |
| (4,4) | (1,2) | 1 | odd gap |
| (4,4) | (2,5) | 3 | odd gap |
| (4,6) | (2,6) | 2 | nonintegral quotient |
| (6,3) | (2,6) | 1 | odd gap |
| (6,4) | (2,4) | 1 | odd gap |

The three identity rows above complete the 11-row certificate. The
deterministic enumeration, including equation coefficients and rejection
reasons, is in
`data/classify_quadratic_degree_pairs_k3-4-6_20260718.csv`.

[PROVED] Every bounded multiplier case is therefore either an MNT identity,
the parity-impossible (6,6) identity, or one of the rejected finite rows.
This proves the theorem.
