---
attempt: A005
status: dead
---
# A005 - Use quaternary representability directly for Algorithm 2, Step 9

## Idea

- [CONJECTURE] Apply Rouse's unconditional quaternary representability theorem to the fixed target equation in Algorithm 2, Step 9, thereby bypassing both the large-modulus Titchmarsh estimate D3 and the binary class randomization D4.
- [CONJECTURE] The proposed algorithm was uniform ellipsoid sampling followed by rejection unless the norm equals the prescribed powersmooth integer \(n\).

## Prior art

- [CITED] Wesolowski 2022, Algorithm 2, Step 9, must solve
  \[
  N^2f(s,t)+p f_\Gamma(x,y)=n_2\ell^e
  \]
  for a fixed right-hand side, not merely find some represented integer.
- [CITED] Rouse 2018 gives effective existence and representation-count bounds for sufficiently large strongly locally soluble targets of an arbitrary quaternary form.

## Execution

- [PROVED] The left side is a primitive positive-definite quaternary form after the same content and coprimality normalizations used in Theorem 5.1.
- [PROVED] If its target satisfies the strong local conditions and exceeds Rouse's fixed-power crossover, Rouse can certify that at least one representation exists without D3 or D4.
- [PROVED] This existence result does not locate a representing vector.
- [PROVED] A rank-four ellipsoid \(Q(v)\le n\) contains on the scale of \(n^2/\sqrt{D(Q)}\) vectors, whereas one level set \(Q(v)=n\) has on the scale of \(n^{1+o(1)}/\sqrt{D(Q)}\) vectors in the theta-series regime.
- [PROVED] Uniform ellipsoid rejection therefore has success probability at most \(n^{-1+o(1)}\), which is exponential in the input length \(\log n\).
- [PROVED] The prime-valued sampler A003 avoids this loss because it accepts \(\asymp X/\log X\) different target values; Step 9 permits only one target value.

## Outcome

- [PROVED] Rouse's representability theorem does not by itself give an expected-polynomial-time implementation of Step 9.
- [PROVED] The exact remaining target is a constructive polynomial-time solver, with sufficient output entropy, for the structured fixed-target quaternary equation above.
- [PROVED] A theorem giving only existence above a polynomial-magnitude threshold is insufficient.

## Post-mortem

**Why it failed:**

- [PROVED] Rejection sampling loses a factor essentially equal to the target integer because a single three-dimensional shell is sparse inside a four-dimensional ellipsoid.

**What transfers:**

- [PROVED] Rouse can potentially discharge global existence after local solubility; future work must add a constructive exact-representation algorithm rather than another density estimate over many target values.

**Would it work under different assumptions?**

- [CONDITIONAL: polynomial-time exact quaternary representation oracle] Yes; such an oracle for this structured family would bypass the sampling loss, but its availability is exactly the unresolved algorithmic content.
