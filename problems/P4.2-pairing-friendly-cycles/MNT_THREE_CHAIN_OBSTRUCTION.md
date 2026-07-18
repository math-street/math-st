# Obstruction to closing the consecutive MNT 3-chain

## Stated class

[PROVED] For an integer \(x\ge1\), define
\[
 A=4x^2-2x+1,\qquad B=4x^2+1,\qquad C=4x^2+2x+1.
\]
Whenever \(A,B,C\) are primes at least 5, the directed edges
\(A\to B\) and \(B\to C\) have exact embedding degrees 4 and 6, while the
reverse-chain edges \(C\to B\) and \(B\to A\) have exact degrees 4 and 6.
This file asks whether either orientation closes to a directed 3-cycle whose
remaining exact embedding degree is at most 12.

## Linear recurrence for the closing edge

[PROVED] Modulo \(A\), put \(y=4x\). Modulo \(C\), put \(y=-4x\). In both
cases
\[
 y^2\equiv2y-4.
\]
Write \(y^k\equiv a_k y+b_k\). Starting from
\((a_1,b_1)=(1,0)\), multiplication by \(y\) gives the recurrence
\[
 a_{k+1}=2a_k+b_k,\qquad b_{k+1}=-4a_k.
\]

[PROVED] For \(1\le k\le12\), the pairs are
\[
\begin{array}{c|rrrrrrrrrrrr}
k&1&2&3&4&5&6&7&8&9&10&11&12\\
a_k&1&2&0&-8&-16&0&64&128&0&-512&-1024&0\\
b_k&0&-4&-8&0&32&64&0&-256&-512&0&2048&4096.
\end{array}
\]
Thus \(|a_k|\le1024\), \(|b_k-1|\le4095\), and none of
\(4a_kx+b_k-1\) or \(-4a_kx+b_k-1\) is zero for an integer \(x\ge1\).

## Large-parameter exclusion

[PROVED] If the forward closing edge \(C\to A\) had degree at most 12, then
for some \(1\le k\le12\),
\[
 A\mid (4x)^k-1=4a_kx+b_k-1.
\]
If the reverse closing edge \(A\to C\) had degree at most 12, then similarly
\[
 C\mid (-4x)^k-1=-4a_kx+b_k-1.
\]
For either sign, the absolute value of the right-hand side is at most
\(4096x+4095\). For \(x\ge1026\),
\[
 A-(4096x+4095)=4x^2-4098x-4094>0,
\]
because the expression is positive at 1026 and strictly increasing thereafter.
Since \(A<C\) and the linear remainders are nonzero, neither divisibility can
hold. Both closing degrees therefore exceed 12 for every \(x\ge1026\).

## Finite remainder

[EMPIRICAL: 1 <= x <= 1025, deterministic exhaustive enumeration] The script
`code/analyze_mnt_three_chains.py` tests primality of all three polynomials,
verifies the four fixed MNT edge degrees, and computes both exact closing
degrees. Exactly four all-prime triples occur, at \(x=3,45,480,987\), and no
prime triple closes in either orientation with degree at most 12
(`data/analyze_mnt_three_chains_x1-1025_20260627.csv`).

## Conclusion

[PROVED] Combining the finite exhaustive result for \(x\le1025\) with the
linear-remainder proof for \(x\ge1026\), no consecutive MNT prime 3-chain in
the stated class closes to a pairing-friendly directed 3-cycle with all exact
embedding degrees in \(\{3,\ldots,12\}\), in either orientation.
