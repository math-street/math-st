# Handoff — P2.3 — after session 1

## State in five lines

The overall P2.3 target is recorded as failed.
No general invariant, non-divisor speedup, or GGM lower bound was obtained.
SG-01 and SG-02 nevertheless completed as a validated baseline.
All 328 full-run recoveries matched their seeded secrets.
The exponentiation-call slope was 0.25001, CI [0.24610, 0.25351].

## What is established (tagged)

- [CITED] Cheon 2006 Theorem 1 gives the divisor-case cost stated in
  `refs/cheon2006.md`.
- [EMPIRICAL: exhaustive n in {17,19,31}] The implementation recovered every
  tested scalar (`code/tests/test_cheon.py`).
- [EMPIRICAL: 328 trials, 70913 <= n <= 17592207015937] Every full-run
  recovery verified; fitted exponentiation-call slope 0.25001 with 95%
  bootstrap CI [0.24610, 0.25351].

## What is ruled out

The session did not produce the requested extension beyond \(d\mid n\pm1\)
or a matching generalized GGM lower bound.

## Active thread

A001 completed the known divisor-case baseline only. No attempt is active.

## Next action

If resumed, sweep all divisors for SG-03, then specify an executable SG-04
non-divisor adaptation with a nearby divisor-case live control.

## Invariants — do not violate

- Every recovered secret must be checked against ground truth.
- Exponentiation calls and primitive group operations must not be conflated;
  the latter include Cheon's published \(\log n\) factor.
- Keep all group orders within the scaffold's 60-bit ceiling.

## Files that matter

`code/cheon.py` is the validated implementation.
`code/tests/test_cheon.py` contains exhaustive known-answer tests.
`data/run_scaling_hb8-22_t41_s2303_20260713.csv` contains all full-run rows.
`data/run_scaling_summary_hb8-22_t41_s2303_20260713.csv` contains size medians.
`data/run_scaling_fit_hb8-22_t41_s2303_20260713.json` contains the fit and CI.

## What I would tell my replacement

Do not describe this session as solving P2.3. It reproduced only the known
divisor case; the user explicitly requested that the overall target be left
recorded as failed.
