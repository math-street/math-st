# Boneh 2002

[CITED] Dan Boneh, "Finding Smooth Integers in Short Intervals Using CRT
Decoding," *Journal of Computer and System Sciences* 64(4), 768--784, 2002,
DOI 10.1006/jcss.2002.1827.

Primary text checked at:
<https://crypto.stanford.edu/~dabo/papers/CRTdecode.ps>

## Results relevant to P2.1

[CITED] Definition 3.1 distinguishes ordinary $s$-smooth integers from
strongly $s$-smooth integers, for which every dividing prime power is at most
$s$.

[CITED] Theorem 3.1 uses CRT list decoding to find every integer in an
interval having a sufficiently large greatest common divisor with the product
of the maximal prime powers below $s$.  Its threshold is

$$
 T>S^{\sqrt{\log(4H)/\log S}+5/(4d)}.
$$

[CITED] When the interval lies below $2T$, the same theorem lists every
strongly $s$-smooth integer in it.  Boneh explicitly notes that the guarantee
is a finder under a promise and that a random admissible interval is unlikely
to contain such a value.

## Verification performed

[EMPIRICAL: primary-source audit 2026-07-14] The author-hosted PostScript,
Definition 3.1, Theorem 3.1, its proof, and its interval example were checked.
