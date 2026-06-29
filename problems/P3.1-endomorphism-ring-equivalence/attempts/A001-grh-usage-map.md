---
attempt: A001
status: promising
---
# A001 — Lemma-level GRH dependency audit

## Idea

Read the equivalence proof at source level, enumerate every direct and inherited GRH dependency, and compare each required effective bound with checked unconditional results.

## Prior art

- [CITED] The target is Wesolowski, FOCS 2021 proceedings (published 2022), arXiv:2111.01481v1; its final equivalence results are Theorems 7.2, 7.4, 8.1, and 8.3.
- [CITED] Herlédan Le Merdy--Wesolowski, arXiv:2502.17010v2 (2026), unconditionally prove the unrestricted `Isogeny` equivalence but explicitly leave $\ell$-`IsogenyPath` conditional.

## Plan

1. Locate the primary equivalence proof and stable version metadata.
2. Search the full text for every occurrence of GRH and expand the dependency closure of the affected results.
3. Restate each analytic input with field/order, norm or prime bound, and probability/complexity role.
4. Check primary sources for unconditional alternatives.
5. Determine whether each alternative is polynomial in $\log p$.

## Execution log

- 2026-06-29: initialized before literature retrieval.
- 2026-06-29: checked all 31 pages of Wesolowski's proof and enumerated every occurrence of GRH or RH.
- 2026-06-29: expanded the dependency closure through Eisenträger et al. 2018, Assing--Blomer--Li 2020, and Jao--Miller--Venkatesan 2009.
- 2026-06-29: checked unconditional substitutes in Thorner--Zaman 2017 and Sardari 2019.
- 2026-06-29: checked the current frontier against Herlédan Le Merdy--Wesolowski arXiv:2502.17010v2 and a literature search through 2026-06-29.
- 2026-06-29: wrote the exhaustive map in `../GRH_USAGE_MAP.md`.

## Outcome

- [PROVED] Four genuine GRH leaves account for the complete conditional dependency graph: small auxiliary Frobenius primes, fixed-class prime representation, the large-modulus Titchmarsh range, and polylogarithmic class-group expansion.
- [PROVED] One appeal to ordinary RH in Theorem 6.4 is removable with the unconditional prime number theorem.
- [CITED] The smooth/prescribed-degree direction remains conditional in the latest checked primary source.
