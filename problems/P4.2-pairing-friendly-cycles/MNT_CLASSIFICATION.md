# Elementary classification of degree-(4,6) 2-cycles

## Theorem

[PROVED] Let \(5\le p<q\) be primes and suppose elliptic curves
\(E_1/\mathbb F_p\), \(E_2/\mathbb F_q\) form a prime-order 2-cycle. If their
exact embedding-degree pair is \((6,4)\), then for an integer \(x\ge1\),
\[
 p=4x^2+1,\qquad q=4x^2+2x+1.
\]
If the exact degree pair is \((4,6)\), then
\[
 p=4x^2-2x+1,\qquad q=4x^2+1.
\]
Thus every such cycle is a specialization of the known MNT6/MNT4 cycle
polynomials.

## Proof

[PROVED] Put \(c=q-p\). Both primes are odd, so \(c\) is a positive even
integer. The traces are \(1-c\) and \(1+c\). Hasse's bound gives
\((c-1)^2\le4p\), hence
\[
 \frac{c^2+1}{p}\le4+\frac4{\sqrt p}+\frac2p.
\]
For \(p\ge7\), any positive integer equal to this ratio is at most 5 and is
therefore smaller than both \(p\) and \(q\). The only case with \(p=5\) is
handled directly below.

[PROVED] First assume the degree pair is \((6,4)\). Exact degree 4 on the
second curve implies
\[
 p\mid\Phi_4(q)=q^2+1.
\]
Since \(q\equiv c\pmod p\), write \(c^2+1=mp\) for a positive integer \(m\).
Exact degree 6 on the first curve similarly gives
\[
 q\mid\Phi_6(p)=p^2-p+1.
\]
Since \(p\equiv-c\pmod q\), this says \(q\mid c^2+c+1\). But
\[
 c^2+c+1=mp+c=m(p+c)-(m-1)c=mq-(m-1)c.
\]
Therefore \(q\mid(m-1)c\). As \(0<c<q\), primality gives \(q\nmid c\), so
\(q\mid m-1\). For \(p\ge7\), the bound above gives \(0<m<q\), forcing
\(m=1\). When \(p=5\), Hasse and primality force \(q=7\), and direct
substitution again gives \(m=1\). Hence \(p=c^2+1\) and
\(q=c^2+c+1\). Writing \(c=2x\) proves the first parametrization.

[PROVED] Now assume the degree pair is \((4,6)\). Degree 4 on the first curve
gives \(q\mid c^2+1\); write \(c^2+1=mq\). Degree 6 on the second gives
\(p\mid c^2-c+1\). Since
\[
 c^2-c+1=mq-c=m(p+c)-c=mp+(m-1)c,
\]
we get \(p\mid(m-1)c\). Here \(p=5\) would force \(q=7\), whose degree pair
is \((6,4)\), so \(p\ge7\). Hasse gives \(c<p\), hence \(p\nmid c\), and the
same ratio bound gives \(0<m<p\). Thus \(p\mid m-1\) forces \(m=1\). It
follows that \(q=c^2+1\), \(p=c^2-c+1\), and \(c=2x\) gives the second
parametrization.

## Scope and relation to prior work

[CITED] Chiesa--Chua--Weidner 2019 classify all MNT cycles as degree patterns
\((6,4)\) and \((6,4,6,4)\) (Proposition 4.1). The proof above is a
self-contained converse at the parameter level for any prime-order 2-cycle
whose exact degrees are \((6,4)\) or \((4,6)\); no novelty claim is made.

