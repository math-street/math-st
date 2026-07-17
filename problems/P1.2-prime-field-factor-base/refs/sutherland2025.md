# Sutherland 2025 — Point counting

## Source

[CITED] Andrew V. Sutherland, “Point Counting,” MIT 18.783 Elliptic Curves,
Lecture 7 slides, Fall 2025.
<https://ocw.mit.edu/courses/18-783-elliptic-curves-fall-2025/mit18_783_f25_lec_s_07.pdf>

## Result used here

[CITED] The slides state
$$
\#E(\mathbb F_q)=q+1-\operatorname{tr}(\pi_E),
\qquad |\operatorname{tr}(\pi_E)|\le 2\sqrt q.
$$

## Consequence in repository notation

[PROVED] For $q=p$ and $r=\#E(\mathbb F_p)$,
$p+1-2\sqrt p\le r\le p+1+2\sqrt p$, hence $r/p\to1$ and
$r=p^{1+o(1)}$.

## What it rules out and leaves open

[PROVED] The bound makes the denominator in the uniform-target success
probability asymptotically linear in $p$. It says nothing about how to find a
decomposition once a target is reachable.

No computation from the slides was reproduced; only the displayed point-count
identity and Hasse bound were checked.
