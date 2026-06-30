# Bonnetain–Schrottenloher 2020

- [CITED] Xavier Bonnetain and André Schrottenloher, “Quantum Security Analysis of CSIDH,” EUROCRYPT 2020, Part II, 493–522, DOI 10.1007/978-3-030-45724-2_17; IACR ePrint 2018/537.
- [CITED] Table 4 reports for CSIDH-512 Section 3.3 a query exponent 19, oracle T-gate exponent 52.6, total T-gate exponent 71.6, classical-time exponent 86, and quantum memory below exponent 15.3.
- [EMPIRICAL: `code/tests/test_cost_model.py` on 2026-06-30] The logical-endpoint fixture recomputes (19+52.6=71.6) to ten decimal places in base-two log cost.
- [PROVED] The fixture does not reproduce the paper's entire circuit or classical computation; it reproduces the cited Table 4 multiplication only.
