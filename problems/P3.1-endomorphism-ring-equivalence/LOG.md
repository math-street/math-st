# Log - P3.1

## Session 1 - 2026-06-29

**Goal:** Complete SG-01 as far as accessible primary sources allow: produce a lemma-level GRH usage map, trace the analytic inputs, and distinguish direct uses from inherited dependencies.

**Prediction (written before literature retrieval):** The proof will use GRH only through effective production or generation of small split-prime ideal classes and short representatives in quadratic orders; Deuring correspondence and the formal reductions themselves will be unconditional. A bound exponential in $\log |D|$ will not preserve polynomial time, while a fixed power of $\log |D|$ will.

**Did:**

- Initialized the P3.1 persistent artifact set.
- Ran `env/check_env.py` and all shared-library tests: Python 3.13.4; 34 tests passed initially and 53 passed in the final workspace check; Sage, Singular, and msolve are unavailable but irrelevant to SG-01.
- Read Wesolowski arXiv:2111.01481v1 in full and expanded every GRH-qualified result to its direct analytic inputs.
- Checked the principal dependencies and unconditional substitutes in six additional full-text primary sources.
- Checked the present problem boundary against Herlédan Le Merdy--Wesolowski arXiv:2502.17010v2 and a literature search through 2026-06-29.
- Published `GRH_USAGE_MAP.md` and seven source notes.

**Found:**

- [PROVED] Four genuine GRH leaves account for the proof: D1 small auxiliary Frobenius primes, D2 fixed-form prime density, D3 the large-modulus Titchmarsh range, and D4 polylogarithmic class-group expansion.
- [PROVED] The appeal to ordinary RH in Wesolowski's Theorem 6.4 is unnecessary; the unconditional prime number theorem gives the needed product lower bound.
- [CITED] Assing--Blomer--Li's unconditional theorem allows only polylogarithmic auxiliary moduli; with the quaternion parameter $b=p$, it forces output bit length exponential in $\log p$.
- [CITED] Thorner--Zaman give a fixed-form least prime $\ll|D|^{694}$ unconditionally, but this is an existence bound rather than the inverse-polylogarithmic sampling density required by the reduction.
- [CITED] The 2026 unconditional equivalence covers unrestricted `Isogeny`; it explicitly leaves $\ell$-`IsogenyPath` to `EndRing` GRH-conditional.

**Prediction vs. outcome:** partially matched. Small split/Frobenius primes and small ideal-class generators are two direct leaves, but the prediction missed the independent large-modulus Titchmarsh input D3 and understated the fixed-form density requirement D2. Deuring correspondence itself is unconditional as predicted.

**Did not work:** Replacing GRH by the checked unconditional least-prime bounds fails to give expected polynomial time; replacing the GRH range of Assing--Blomer--Li forces exponentially long outputs; Minkowski-size class-group generators lack the needed polylogarithmic cutoff and expansion.

**Changed my mind about:** The obstruction is not a single Chebotarev lemma. Even a polylogarithmic auxiliary quaternion model would leave D2--D4. Conversely, modern unrestricted ideal-to-isogeny algorithms bypass the entire KLPT route but do not satisfy the smooth-degree output condition.

**Next:** Test SG-02b by combining the existing Brandt randomization with unconditional average-over-form-class prime results, and identify the exact probability loss for an adversarial starting ideal.

## Session 2 - 2026-07-11

**Goal:** Decide SG-02b and SG-02c: test whether the unconditional Brandt randomization already present in `EquivIdeal` can turn average-over-class prime results into a replacement for D2, then test whether the unconditional Assing--Blomer--Li range can be retained by removing the parameter $b=p$ from the norm equation.

**Prediction (written before the new source audit):** SG-02b will fail at the map from a random quaternion ideal class to the deterministic binary subform selected in Proposition 3.5; neither Sardari's binary class average nor Brandt mixing should control that pushforward. SG-02c will fail because the coefficient $p$ is forced by the ramification/discriminant of $B_{p,\infty}$ rather than by the chosen basis, but an alternative higher-dimensional parameterization may isolate a weaker, precisely stated target theorem.

**A003 pre-experiment prediction (written before implementation):** For maximal-order and small prime-ideal norm lattices with $p<64$ and $\ell\le7$, every prime value in the residue sublattice will satisfy the required quadratic-nonresidue condition, but the global coverage of admissible progression primes will be visibly incomplete below the asymptotic Rouse crossover. The prime-vector fraction should nevertheless be on the scale $1/\log X$ once the ellipsoid contains more than a few hundred vectors.

**A006 pre-audit prediction (written before source reinspection):** The flexible-model and local-dictionary machinery of Herledan Le Merdy--Wesolowski will remove the need to find the special polylogarithmic Frobenius prime D1 at the level of model translation, but its arbitrary-ideal conversion will not preserve prescribed smooth degree. A hybrid with the old smooth conversion will still need either the special dictionary or a new oriented smooth conversion theorem.

**SG-03d pre-experiment prediction (written before implementation):** For the $p=11$, $\ell=3$ fixture, every computed right order will have trace discriminant $p^2$ and multiplicative closure, and each exact embedded right-order key will map to one quotient `deuring_key`. Distinct embedded right orders may map to the same curve class because the local graph has parallel ideal/isogeny representatives. A collision sending one exact right-order key to two curve keys, or any discriminant/closure failure, refutes the implementation.

**SG-03e pre-experiment prediction (written before implementation):** For each norm-3 ideal $I$, the exact product lattice $I\bar I$ will equal $3O$. On the curve side, the images of the nonkernel 3-torsion under the first Velu map will form the nonzero dual kernel, and quotienting by it will return the source `deuring_key`; the recorded degree product will be 9. Any lattice-identity or endpoint failure refutes the two-step fixture.

**Did:**

- Began a fresh dependency-level audit from Algorithm 2, Proposition 3.5, and the relevant average representation literature.
- Read and source-checked Rouse 2018, Rouse--Thompson 2022, Ditchen 2018, Goren--Love 2025, Bennett--Martin--O'Bryant--Rechnitzer 2018, Kannan 1987, and the relevant algorithms in Wesolowski 2022 and Herledan Le Merdy--Wesolowski 2026.
- Closed A002, A004, A005, and A006 with mathematical post-mortems.
- Wrote A003's direct quaternary sampler proof and ran its 22-case grid plus five cutoff experiments.
- Added canonical quadratic-extension curves, Frobenius-orbit keys, extension-field Velu routines, and their shared-library tests.
- Implemented the local ideal--kernel--ideal and embedded-right-order round trip, recorded a separate 30-independent-seed validation, and timed five values of $p$.
- Added a tested log--log power-law fit and stored all five residuals.
- Ran the final repository suite after a compact legacy-serialization compatibility fix and the right-order additions: 299 tests and 3 subtests passed.

**Found:**

- [PROVED] Brandt mixing makes quaternion ideal classes nearly uniform but supplies no domination bound for the deterministic LLL-and-gcd binary-subform pushforward; the checked average-form theorems therefore do not replace D2.
- [PROVED] Ramification at $p$ forces the large parameter into a coefficient, binary discriminant, or lattice index of every integral orthogonal $2+2$ norm decomposition, so a basis change does not reach the unconditional Assing--Blomer--Li range.
- [PROVED] A003 gives an unconditional replacement for Proposition 3.8 with expected time polynomial in $\log p$ and the numerical value of $\ell$, thereby removing D2 from the old smooth-path proof.
- [PROVED] Quaternary representability alone does not construct a representation of Algorithm 2's one fixed target: uniform ellipsoid rejection loses a factor $n^{1-o(1)}$.
- [PROVED] The 2026 flexible model removes the special-curve dictionary use of D1 but not the D1-small binary discriminant required inside the old norm-equation algorithm.
- [EMPIRICAL: p<=31, ell in {3,5}, q<=3000] The A003 grid had zero reciprocity violations; $\Pr[Q(v)\text{ prime}]\log X$ ranged from 0.832 to 1.815 with mean 1.276 over 22 cases.
- [EMPIRICAL: p=11, ell=3, 30 independent seeds] The local Deuring fixture recovered the ideal and quotient curve key, visited all four embedded neighbor right orders of trace discriminant $11^2$, verified $I\bar I=3O$, and returned through the dual kernel to the source key in 30/30 trials.
- [EMPIRICAL: p in {11,23,47,59,71}, ell=3, n=5] The exhaustive right-order-aware two-step timing exponent is 1.6796, with classical 95% interval $[1.2366,2.1226]$ and $R^2=0.9798$.
- [PROVED] These timing rows have no oracle query and therefore do not identify the security-bit-loss proxy $\Delta(p)$.

**Prediction vs. outcome:** The SG-02b and SG-02c predictions matched. The A003 prediction matched on the residue invariant and prime-density scale; small-cutoff admissible-prime coverage was incomplete as expected. The A006 prediction partially matched: the dictionary layer became unconditional, but the older smooth core failed earlier than arbitrary ideal conversion, at its small-discriminant norm equation. The SG-03d and SG-03e predictions matched: every right order was closed with discriminant $p^2$, no exact-key collision occurred, every dual product was $\ell O$, and every dual quotient returned the source curve class.

**Did not work:** [PROVED] A002's probability spaces do not match. [PROVED] A004 cannot move ramification out of every analytic parameter. [PROVED] A005's exact shell is too sparse for ellipsoid rejection. [PROVED] A006 leaves the numerical-discriminant loop in Theorem 5.1. The first symbolic enumeration loop also exceeded the 120-second timebox; integer arithmetic reduced the recorded grid to 27.84 seconds.

**Changed my mind about:** [PROVED] D2 is not intrinsically a binary-form obstruction; the rank-four lattice has enough represented prime values unconditionally. [PROVED] The remaining core is constructive fixed-target representation, not another least-prime or average-density theorem. [PROVED] A modern flexible dictionary is algebraically useful but does not itself supply smooth degree.

**Next:** Complete SG-03d by attaching canonical right orders of toy neighbor ideals to quotient-curve `deuring_key` values and validating a full curve--right-order--curve class lookup on at least 20 independently seeded cases.
