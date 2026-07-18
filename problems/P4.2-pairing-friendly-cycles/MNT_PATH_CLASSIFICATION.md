# Classification of equal-gap degree-(4,6) paths

## Theorem

[PROVED] Let \(p,q,r\ge5\) be distinct primes such that the two directed
Hasse edges \(p\to q\) and \(q\to r\) have exact embedding degrees 4 and 6.
If their signed field gaps agree,
\[
 q-p=r-q,
\]
then for an integer \(x\ge1\), either
\[
 (p,q,r)=
 (4x^2-2x+1,\;4x^2+1,\;4x^2+2x+1)
\]
or
\[
 (p,q,r)=
 (4x^2+2x+1,\;4x^2+1,\;4x^2-2x+1).
\]
Thus every such path is one orientation of the consecutive MNT chain.

## Increasing orientation

[PROVED] Put \(d=q-p=r-q>0\). Exact degree 4 gives
\[
 q\mid\Phi_4(p)=p^2+1,
\]
and \(p\equiv-d\pmod q\), so \(q\mid d^2+1\). Write
\[
 d^2+1=mq
\]
with \(m\ge1\). The Hasse inequality for the edge \(p\to q\) is
\((d-1)^2\le4p\). Hence
\[
 d^2+1\le4p+2d=4q-2d<4q,
\]
so \(1\le m<4\).

[PROVED] Exact degree 6 on \(q\to r\) gives
\[
 r\mid\Phi_6(q)=q^2-q+1.
\]
Reducing \(q=r-d\) modulo \(r\) yields \(r\mid d^2+d+1\). But
\[
 d^2+d+1=mq+d=m(r-d)+d=mr-(m-1)d.
\]
Therefore \(r\mid(m-1)d\). Since \(0<d<r\) and \(m<4<r\), primality of
\(r\) forces \(m=1\). Consequently
\[
 q=d^2+1,\qquad p=d^2-d+1,\qquad r=d^2+d+1.
\]
The odd primes have even difference \(d=2x\), giving the first formula.

## Decreasing orientation

[PROVED] Put \(e=p-q=q-r>0\). Degree 4 gives \(q\mid e^2+1\), so write
\(e^2+1=mq\). The Hasse inequality for \(q\to r\) is
\((e+1)^2\le4q\), and therefore
\[
 e^2+1\le4q-2e<4q,
\]
so again \(1\le m<4\).

[PROVED] Degree 6 gives \(r\mid e^2-e+1\). Using \(q=r+e\),
\[
 e^2-e+1=mq-e=m(r+e)-e=mr+(m-1)e,
\]
so \(r\mid(m-1)e\). Hasse also gives
\((e-1)^2\le4r\), which implies \(e<r\) for prime \(r\ge5\).
Because \(m<4<r\), it follows that \(m=1\). Thus
\[
 q=e^2+1,\qquad p=e^2+e+1,\qquad r=e^2-e+1,
\]
and \(e=2x\) gives the reverse formula.

## Consequence for the 22-bit ledger

[EMPIRICAL: all 42 two-target-edge near-misses below \(2^{22}\)] Eight rows
have equal signed gaps and target-degree pair (4,6). The classifier identifies
them as the two orientations at each of \(x=3,45,480,987\), exactly as the
theorem requires
(`data/classify_three_cycle_near_misses_n42_20260718.csv`).

[PROVED] The closing edge of every row in this class has exact degree above 12
by `MNT_THREE_CHAIN_OBSTRUCTION.md`. It can therefore never supply a primary
directed 3-cycle, regardless of parameter size.
