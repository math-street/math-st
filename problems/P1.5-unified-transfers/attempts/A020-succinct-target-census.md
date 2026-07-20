---
attempt: A020
status: folded-into-A001
---
# A020 - Census small discriminants whose class number is divisible by r

## Idea

- [CONJECTURE] Although the self-certifying A019 family has
  \(\Theta(r)\)-bit discriminants, toy primes will already divide class
  numbers of discriminants of magnitude roughly polynomial in \(r\).
- [PROVED] Such examples would separate existential target size from a
  uniform construction of a certified class: \(r\mid h(\Delta)\) guarantees
  an order-\(r\) element by Cauchy's theorem, but a census does not provide a
  polynomial-time growing-family generator or the A001 evaluator.

## Prediction and criteria

- [CONJECTURE] For every tested prime \(3\le r\le43\), a discriminant below
  \(2\cdot10^5\) will have class number divisible by \(r\), and the first such
  magnitude will be far below \(2^r\).
- [PROVED] A positive experiment enumerates every primitive reduced positive
  form for \(|\Delta|\le X\), validates known class numbers, and records the
  least \(|\Delta|\) with \(r\mid h(\Delta)\).
- [PROVED] A negative experiment is a missing prime within the declared
  bound; it says nothing beyond that finite range.

## Plan

1. Batch-enumerate reduced primitive positive forms and aggregate their
   discriminants.
2. Validate the counts at \(-3,-4,-15,-20,-23,-47,-71\).
3. Record the least qualifying discriminant for each toy prime and compare
   its bit length with A019 and SG-25.

## Execution log

- [EMPIRICAL: every negative order discriminant with $|\Delta|\le200000$]
  `code/probe_exact_order_targets.py` batch-enumerated primitive reduced
  positive forms and aggregated exact class numbers in 2.72 seconds on Python
  3.13.4.
- [EMPIRICAL: known discriminants $-3,-4,-15,-20,-23,-47,-71$] The batch
  counts matched the recorded class numbers and the independent shared
  per-discriminant enumerator; three dedicated tests passed.
- [EMPIRICAL: 13 primes $3\le r\le43$] Every prime had a qualifying
  discriminant, and in every row the least qualifying discriminant had class
  number exactly $r$.  The recorded $|\Delta|/r^2$ range was
  $[0.684711,2.555556]$ and the discriminant bit lengths were 5--11.
- [EMPIRICAL: same 13 primes] A nonprincipal reduced form was recorded for
  every target.  Since the class-group order in each row is the prime $r$,
  each recorded form represents a class of exact order $r$.

## Outcome

- [EMPIRICAL: exhaustive through $|\Delta|\le200000$, $3\le r\le43$] Toy
  exact-order targets can be dramatically smaller than the A019
  $1-4\cdot2^r$ family; the full table is
  `data/probe_exact_order_targets_full_20260710.csv`.
- [PROVED] This does not give a uniform growing-family construction.  The
  experiment locates each discriminant by exhaustive class-number census,
  whose cost is not polynomial in $\log r$, and makes no claim beyond the
  finite search range.
- [PROVED] The result refines SG-28: the obstacle is not small-target
  existence at toy sizes but uniform certified construction without a
  class-group search, followed independently by the cross-characteristic
  evaluator.
