---
attempt: A005
status: successful
---
# A005 — Adversarial self-verification after resolution

## Method

[PROVED] This audit treated A004 as untrusted and rechecked four independent failure surfaces: arbitrary unregistered typed labels, adaptive target-label branching, ensemble-to-fixed-oracle quantifiers, and the claimed elliptic-curve realization.

## Proof attacks

- [PROVED] Arbitrary unregistered strings can be submitted through group, equality, pairing, or DLP interfaces, not only through `DLOG2`. Independent typed encodings make a hit on a particular challenge-dependent value cost at most \(2^{-L}\) per probe; hits on other values reveal transcript-fixed constants and preserve affinity. `CLAIM.md` was broadened accordingly.
- [PROVED] Adaptive branching on challenge-label bits is handled only in the coupled experiment where each challenge is completed to a fresh uniform encoding. The later Markov–Borel–Cantelli step, not that coupling, selects one fixed oracle.
- [PROVED] The uniform-challenge bound refutes the standard worst-case search solver because a solver succeeding with probability at least \(2/3\) on every valid target must also do so on their uniform distribution.
- [PROVED] Cross-parameter queries are independent auxiliary information after conditioning on every other oracle component, so they do not change the current-parameter lazy simulation.

## Reproduction checks

- [EMPIRICAL: deterministic rerun] A separately generated affine CSV had SHA-256 `8A69F4ACE2D21F1AA34105603A295121A4DE8A6F7746FD54779BD3682EE2A042`, exactly matching the recorded dataset byte-for-byte. The temporary file was removed after its workspace path was verified.
- [EMPIRICAL: six curve realizations] For \((p,r)=(43,11),(59,5),(83,7),(103,13),(131,11),(163,41)\), direct recomputation verified \(p\equiv-1\bmod4r\), \(\#E(\mathbb F_p)=p+1\), \(rP=\mathcal O\), a nonidentity pairing value, and target order dividing \(r\).
- [EMPIRICAL: negative control] The exhaustive affine rows attain \(\min(p,\binom t2)\), so the verifier would not pass merely because its sampled collision sets were atypically sparse.

## Tooling note

[EMPIRICAL] One initial ad-hoc curve-check invocation stopped before any arithmetic because of a nonexistent placeholder import. It created no output. The corrected self-contained invocation then completed all six curve checks.

## Verdict

[PROVED] The resolved status survives adversarial self-verification. The only defect found was the too-narrow wording of the blind-label term; broadening it to all typed oracle inputs leaves the theorem and asymptotic bound unchanged. No open P2.4 claim remains.
