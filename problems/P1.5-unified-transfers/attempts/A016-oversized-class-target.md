---
attempt: A016
status: dead
---
# A016 - Use an arbitrarily large discriminant to force order-$r$ class torsion

## Idea

- [CONJECTURE] A separately constructed imaginary-quadratic order can make
  $r$ divide its class number by taking an extremely large discriminant, with
  no cost to the transfer definition beyond polynomial encoded setup.

## Size lower bound

Put $n=\lceil\log_2r\rceil$ and
$B=\log_2|\Delta|$.  If the class group contains an order-$r$ element, then
$h(\Delta)\ge r$.

- [PROVED] A003 gives
  $$h(\Delta)\le\frac3\pi\sqrt{|\Delta|}
  (\log|\Delta|+2)^2.$$
- [PROVED] Taking binary logarithms and using
  $2^{n-1}\le r$ yields
  $$n-1\le \frac B2+2\log_2(B\ln2+2)+\log_2(3/\pi),$$
  and therefore
  $$B\ge2n-O(\log n).$$
  Thus the natural target discriminant already needs about twice as many bits
  as the source subgroup order, but this is still polynomial setup size.

## Target-algorithm upper bound

- [CONDITIONAL: Extended Riemann Hypothesis and factor-base decomposition of
  represented target inputs] The Hafner--McCurley route has cost
  $$\exp\!\left(O\!\left(\sqrt{\log|\Delta|\,
  \log\log|\Delta|}\right)\right).$$
- [PROVED] This particular route meets SG-01's
  $\exp(o(n))$ target requirement exactly when
  $$B\log B=o(n^2).$$
  SG-01 also has $B=n^{O(1)}$, and the preceding size bound has $B=\Omega(n)$;
  hence $\log B=\Theta(\log n)$ and this is equivalent to
  $B=o(n^2/\log n)$ in the admissible range.
- [PROVED] Combining the source-image size and target-cost constraints leaves
  the discriminant-bit window
  $$2n-O(\log n)\le B=o(n^2/\log n).$$

## Outcome

- [PROVED] Arbitrarily inflating the discriminant is not free.  For the checked
  Hafner--McCurley target route, discriminants at or above the
  $n^2/\log n$ scale lose the required subexponential-in-$n$ target bound.
- [CONJECTURE] The surviving construction problem is sharper: uniformly build
  an order inside the displayed window, provide a known exact order-$r$ class,
  and evaluate its power from a source point in polynomial time.  One family
  doing all three revives A001.

## Post-mortem

**Why it failed:** [PROVED] The class group must be large enough to contain the
image but small enough, as measured by discriminant bits, for its checked DLP
algorithm to remain subexponential in the source parameter.

**What transfers:** [PROVED] Any future class-target proposal must report
$B=\log_2|\Delta|$ and verify the window above, rather than only stating that
the discriminant has polynomial bit length.

**Would it work under different assumptions?** [CONDITIONAL: a faster target
DLP algorithm] A different rigorously analyzed target algorithm could enlarge
the upper end of the window; the lower bound from class-group size remains.
