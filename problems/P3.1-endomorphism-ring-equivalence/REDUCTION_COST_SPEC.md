# Concrete reduction-cost specification

## Purpose

- [PROVED] This file defines SG-04's counters and parameter grid independently of whether Task 1 is ultimately made unconditional.
- [PROVED] Conditional and unconditional candidate reductions must be reported in separate rows so that an empirical timing result never changes the logical status of a reduction.

## Unit counters

- [PROVED] `field_mul`, `field_square`, `field_inv`, and `field_frob` count arithmetic in \(\mathbb F_{p^2}\); integer and extension-field operations are not merged.
- [PROVED] `velu_steps[ell]` counts prime-degree isogeny steps by degree, and `kernel_points[ell]` counts kernel points processed.
- [PROVED] `brandt_steps[ell]` counts quaternion/curve random-walk edges by degree.
- [PROVED] `ideal_mul`, `ideal_intersection`, `ideal_hnf`, `ideal_equivalence`, and `right_order` count exact quaternion lattice operations.
- [PROVED] `lll_calls`, `lll_rank`, `lll_input_bits`, and `lll_output_bits` record lattice-reduction work and operand growth.
- [PROVED] `prime_tests`, `prime_rejections`, and `prime_output_bits` record prime-sampler work.
- [PROVED] `class_group_steps`, `class_group_generators`, and `largest_generator_norm` isolate D4 from all other costs.
- [PROVED] `norm_equation_trials`, `cornacchia_calls`, `local_rejections`, and `norm_solution_bits` isolate Theorem 5.1 and D3.
- [PROVED] `oracle_queries`, `oracle_input_bits`, and `oracle_output_bits` record the black-box part of each reduction.
- [PROVED] `wall_seconds`, `peak_bytes`, and a deterministic `seed` accompany every measured row.

## Output-quality counters

- [PROVED] `degree_bits=ceil(log2(deg(phi)+1))` records output size without expanding a smooth isogeny into its enormous rational-map degree.
- [PROVED] `chain_length=sum(e_i)` and `largest_prime_power=max(ell_i**e_i)` record the cost-relevant smooth factorization \(\deg\phi=\prod_i\ell_i^{e_i}\).
- [PROVED] `smoothness_bound=max(ell_i)` is kept separate from chain length because ideal-to-isogeny conversion is polynomial in the largest prime power, not merely in \(\log\deg\phi\), in the old dictionary-based algorithm (Wesolowski 2022, Lemma 2.6).
- [PROVED] `frobenius_ambiguity` is a Boolean recording whether the accepted endpoint matched the target only after applying `deuring_key`.

## Success and loss metrics

- [PROVED] `trial_success` is one only when all algebraic invariants and the endpoint acceptance rule pass.
- [PROVED] For repeated independent trials, report the Wilson 95% confidence interval for the success probability rather than only the sample mean.
- [PROVED] `expected_repetitions` is estimated as the reciprocal of the measured success probability only when the confidence interval excludes zero.
- [PROVED] Define the measured time expansion
  \[
  R_T(p)=\frac{T_{\mathrm{reduction}}(p)+Q(p)T_{\mathrm{oracle}}(p)}{T_{\mathrm{oracle}}(p)}.
  \]
- [PROVED] Define the concrete bit-loss proxy
  \[
  \Delta(p)=\log_2 Q(p)+\log_2(1/s(p))+\log_2\max(1,R_T(p)),
  \]
  where \(Q\) is oracle query count and \(s\) is reduction success probability.
- [PROVED] This proxy is an accounting convention, not a theorem equating runtime and advantage; reports must also show its three summands separately.

## Parameter grid

- [PROVED] Exhaustive algebraic validation uses primes in each nonempty class modulo eight with \(7\le p<2^{16}\), subject to the implementation's current model restrictions.
- [PROVED] Scaling runs use target bit lengths \(8,12,16,20,24,32,40,48,60\) only for subroutines that do not enumerate all field elements.
- [PROVED] Smooth degrees use \(\ell\in\{2,3,5,7,11\}\), chain lengths \(1,2,4,8,16\), and mixed supports \(\{2,3\}\), \(\{2,3,5\}\), and \(\{3,5,7\}\).
- [PROVED] Every randomized cell uses at least 30 seeds for an exploratory row and at least 200 seeds before a success probability is used in \(\Delta(p)\).
- [PROVED] A timing exponent is reported only after fitting at least five parameter sizes and storing residuals, as required by the shared scaffold.

## Baselines

- [PROVED] The first baseline is the existing GRH-conditional Wesolowski route with each D1--D4 call counted but not silently replaced by a heuristic.
- [PROVED] The second baseline is the unconditional unrestricted-isogeny route of Herledan Le Merdy--Wesolowski 2026; its degree quality is reported as unrestricted and is not compared as though it solved the smooth problem.
- [CONJECTURE] A third row will use A003 as an unconditional candidate replacement for D2 if its remaining proof obligations survive source audit and toy refutation; a counterexample to any obligation removes this row.
