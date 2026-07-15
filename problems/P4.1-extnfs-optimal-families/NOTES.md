# P4.1 notes

## Stable facts

[CITED] Kim–Barbulescu 2016 supplies the exTNFS asymptotic framework, while Barbulescu–Duquesne 2019 supplies the finite-size cost decomposition and the 99.69-bit BN worked example.

[EMPIRICAL: published fixtures] The Dickman implementation reproduces both BN smoothness probabilities within 0.02 bits and total cost within 0.2 bits; the BLS12 polynomial at the BLS12-381 seed matches both published moduli exactly.

[EMPIRICAL: every integer seed $-10{,}000\le u\le10{,}000$, $p<2^{60}$] The bounded search contains 302 accepted candidates: 273 BN, 24 BLS12, 5 BLS24, and no KSS16.

[PROVED] In the implemented leading-term four-family optimization, BN minimizes estimated $\rho$ for 128, 192, and 256 bits under all three cost scenarios; this does not imply minimum pairing time.

## Modelling conventions under investigation

- The extension-field cost must identify its $L$-notation constant, finite-size calibration, special-form adjustment, tower adjustment, and conversion from operations to security bits.
- The searched seed space and the extrapolation beyond the toy experiment ceiling must be separated in every output table.
- The default extrapolation uses $L_Q[32]$ with a −10.425-bit prefactor calibrated to the single BN anchor.
- `pairing_proxy` is an ordering heuristic, not an operation count or runtime estimate.
