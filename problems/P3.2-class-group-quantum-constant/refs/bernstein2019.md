# Bernstein–Lange–Martindale–Panny 2019

- [CITED] Daniel J. Bernstein, Tanja Lange, Chloe Martindale, and Lorenz Panny, “Quantum Circuits for the CSIDH: Optimizing Quantum Evaluation of Isogenies,” EUROCRYPT 2019, 409–441, DOI 10.1007/978-3-030-17656-3_15; IACR ePrint 2018/1059.
- [CITED] The paper reports (1{,}118{,}827{,}416{,}420\approx2^{40}) nonlinear bit operations for one CSIDH-512 action schedule with stated failure below (2^{-32}), and a (0.7\cdot2^{40}) alternative.
- [CITED] The authors separate nonlinear bit operations from reversible Toffoli and quantum T-gate conversions and discuss potentially very large intermediate memory.
- [PROVED] The Peikert fixture uses the rounded (2^{40}) optimistic T-gate endpoint, not the paper's exact nonlinear-operation integer, because those metrics are not identical.
