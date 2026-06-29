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
