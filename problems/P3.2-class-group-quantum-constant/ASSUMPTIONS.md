# What drives the concrete-security disagreement

## Sieve choice

- [CITED] Kuperberg's first sieve, Regev's polynomial-space variant, Kuperberg's collimation sieve, and later subset-sum hybrids occupy different query/time/memory points rather than defining one universal leading constant (Kuperberg 2005; Regev 2004; Kuperberg 2013; Remaud, Schrottenloher, and Tillich 2022).
- [CITED] Peikert reports CSIDH-512 examples near (2^{19}) queries with (2^{32}) QRACM bits and near (2^{16}) queries with (2^{40}) QRACM bits, so selecting a memory point changes the query exponent by several bits (Peikert 2020, Section 4.1).

## Oracle input distribution and failure budget

- [CITED] Bernstein, Lange, Martindale, and Panny count (1{,}118{,}827{,}416{,}420\approx2^{40}) nonlinear bit operations for one stated CSIDH-512 action algorithm at failure probability below (2^{-32}), and also report a (0.7\cdot2^{40}) variant (EUROCRYPT 2019, Sections 1 and 7–8).
- [CITED] Peikert explicitly treats the optimistic oracle cost as an assumption, notes that fewer oracle calls permit a larger per-call failure probability, and gives a logical T-gate range rather than an error-corrected physical cost (Peikert 2020, Sections 1.4 and 4.2).

## Logical metric

- [CITED] Bernstein et al. distinguish nonlinear bit operations, Toffoli gates, T gates, and stored intermediate bits; their generic conversions multiply nonlinear operations by up to two for Toffoli gates and then by up to seven for T gates (EUROCRYPT 2019, Appendix A).
- [CITED] Bonnetain and Schrottenloher's CSIDH-512 Section 3.3 row combines a (2^{19}) query count with a (2^{52.6})-T-gate oracle into (2^{71.6}) logical T gates and (2^{86}) classical work (EUROCRYPT 2020, Table 4).

## Memory technology

- [CITED] The published estimates separately use quantum memory, ordinary classical memory, and quantumly accessible classical memory; equating their bits or access costs changes the optimization problem (Kuperberg 2013; Bonnetain and Schrottenloher 2020; Peikert 2020).
- [PROVED] The bundled calculator keeps QRACM bits as a reported logical assumption and does not silently convert them into surface-code data qubits; inspect `quantum_accessible_classical_memory_bits` in each configuration.

## Physical error correction

- [PROVED] Physical error rate, threshold, suppression prefactor, failure budget, code-cycle time, distance-dependent cycle cost, data footprint, factory footprint, T-state production rate, power, parallel workers, and utilization are named JSON fields in the bundled phenomenological model.
- [PROVED] Neither published logical-endpoint fixture thereby becomes a published physical estimate; each configuration labels its surface-code output illustrative.

## Reproduced endpoints

- [EMPIRICAL: `code/tests/test_cost_model.py` on 2026-06-30] The Bonnetain–Schrottenloher fixture reproduces `log2(T gates)=71.6` from (2^{19}\cdot2^{52.6}).
- [EMPIRICAL: `code/tests/test_cost_model.py` on 2026-06-30] The Peikert optimistic rounded fixture reproduces `log2(T gates)=56` from (2^{16}\cdot2^{40}) and records (2^{40}) QRACM bits.
