# Peikert 2020

- [CITED] Chris Peikert, “He Gives C-Sieves on the CSIDH,” EUROCRYPT 2020, Part II, 463–492, DOI 10.1007/978-3-030-45724-2_16; IACR ePrint 2019/725.
- [CITED] The paper simulates a generalized collimation sieve through the actual CSIDH-512 group order and reports tradeoffs including about (2^{16}) oracle queries with (2^{40}) QRACM bits.
- [CITED] Under an optimistic oracle assumption, the paper gives a CSIDH-512 logical T-gate range roughly (2^{56}) to (2^{60}) and labels the oracle cost a principal open concrete question.
- [EMPIRICAL: `code/tests/test_cost_model.py` on 2026-06-30] The optimistic rounded fixture recomputes (16+40=56) exactly in base-two log cost.
- [PROVED] The repository's low-bit-pair simulator is not Peikert's simulator and does not claim to reproduce Peikert's sieve data.
