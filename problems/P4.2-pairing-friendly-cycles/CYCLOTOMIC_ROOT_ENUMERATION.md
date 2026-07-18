# Candidate-complete cyclotomic-root enumeration

## Exact-order residues

[PROVED] For a prime \(q\), the group \(\mathbb F_q^\ast\) is cyclic. If
\(k\mid q-1\), it has a unique subgroup of order \(k\), and that subgroup has
exactly \(\varphi(k)\) generators. Raising field elements to
\((q-1)/k\) finds a generator \(z\) of this subgroup after testing
\[
 z^{k/\ell}\ne1
\]
for every prime \(\ell\mid k\). The residues \(z^j\) with
\(\gcd(j,k)=1\) are then precisely all residues of exact order \(k\).
If \(k\nmid q-1\), no such residue exists.

[PROVED] For completeness, cyclicity follows by letting \(e\) be the exponent
of the finite abelian group \(\mathbb F_q^\ast\). Its primary decomposition
contains an element of order \(e\). Every nonzero field element is a root of
\(X^e-1\), so the field root bound gives \(q-1\le e\). Lagrange's theorem
gives \(e\le q-1\); hence \(e=q-1\), and the element of order \(e\) generates
the group.

## Recovering every Hasse edge

[PROVED] Let distinct primes \(p,q\ge5\) be a directed Hasse edge, so
\[
 (p+1-q)^2\le4p.
\]
Then \(p<2q\). Otherwise \(p\ge2q\) implies \(p\ge11\) and
\[
 p+1-q\ge p/2+1>2\sqrt p,
\]
contradicting the displayed inequality.

[PROVED] Put \(z=p\bmod q\). The inequality \(p<2q\) leaves exactly two
possibilities:
\[
 p=z\quad\text{or}\quad p=q+z.
\]
If the edge has exact embedding degree \(k\), then \(z\) is one of the exact
order-\(k\) residues generated above. Conversely, the implementation retains
only prime \(p\) satisfying the Hasse inequality and rechecks its exact order.
It therefore generates every and only target-degree Hasse edges for the fixed
prime and degree ranges.

## Consequences for cycle searches

[PROVED] Every reportable 2-cycle row has at least one target-degree directed
edge, so taking the unordered endpoint pair of every generated edge retains
every full hit and every one-sided near-miss.

[PROVED] Every reportable directed 3-cycle row has two consecutive
target-degree edges after rotation. Joining the generated target graph with
itself therefore retains every full hit and every two-of-three near-miss.

[EMPIRICAL: all overlapping bounds through \(2^{24}\)] Root-generated and
Hasse-scanned candidate ledgers agree at every tested bound. At 24 bits the
2-cycle CSVs have the identical SHA-256
`E8F7A009B6E2D390A3E97AF9895401458DD2D2A7FF92CE10598C4D52DF745DFC`,
and the 3-cycle CSVs have the identical SHA-256
`75F37BF179D1C4B535F2DCA290F861803C8ED6B7B3A97A4CA6356CCAD51366B8`.
The root runs took 20.4 and 28.4 seconds, compared with 404.6 and 405.3
seconds for the Hasse scans.
