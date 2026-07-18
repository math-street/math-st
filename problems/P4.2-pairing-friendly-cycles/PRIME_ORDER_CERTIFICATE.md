# Independent prime-order Hasse certificate

## Certificate

[PROVED] Let \(E/\mathbb F_p\) be an elliptic curve and let \(q\) be prime.
Suppose an affine point \(P\in E(\mathbb F_p)\) satisfies
\[
 [q]P=\mathcal O.
\]
Because \(P\ne\mathcal O\) and \(q\) is prime, \(P\) has exact order \(q\).
Lagrange's theorem therefore gives
\[
 q\mid\#E(\mathbb F_p).
\]

[PROVED] Hasse's theorem places the group order in the integer interval
\[
 I_p=
 [p+1-\lfloor2\sqrt p\rfloor,\;p+1+\lfloor2\sqrt p\rfloor].
\]
If \(q\) is the unique positive multiple of \(q\) in \(I_p\), the divisibility
above forces \(\#E(\mathbb F_p)=q\). The certificate consists of the curve,
the affine witness \(P\), its scalar-product check, and the checked interval
endpoints.

## Use in the 24-bit extension

[PROVED] This verification does not assume the order returned by the BSGS
search that selected the curve. It independently certifies the exact group
order from the displayed curve equation, one group-law witness, primality of
\(q\), and Hasse's theorem.

[EMPIRICAL: published fields 37 and 43] The implementation in
`code/construct_hit_cycles.py` certifies both published MNT curves and agrees
with direct equation enumeration. The regression is in
`code/tests/test_construct_hit_cycles.py`.

[EMPIRICAL: field primes at most \(2^{22}-1\)] Earlier construction ledgers
continue to use direct equation enumeration. The certificate path is selected
only above the configurable `--exhaustive-limit` and records its witness
coordinates and verification method in every output row.
