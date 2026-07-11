---
id: P3.1
updated: 2026-07-11
sessions_worked: 2
---
**Status:** partial
**One-line state:** [PROVED] A003 unconditionally removes D2 from the audited smooth-path proof, but D1, D3, and D4 remain; [EMPIRICAL: p<=71] the local Deuring round trip and a five-size toy cost fit are validated without yielding a security-bit loss.
**Last action:** Completed SG-03e: 30 independent norm-3 ideals satisfied $I\bar I=3O$, their two-step degree-9 paths used the computed dual kernels, and every terminal curve returned the source `deuring_key`.
**Next action:** Implement SG-03f by representing a non-dual norm-3 ideal in the first embedded right order, propagate its action to the intermediate curve, and identify the terminal right order without an exhaustive curve-key lookup.
**Blocked on:** nothing
**Active attempts:** A003 (promising); A001 (completed audit); A002, A004, A005, and A006 (dead with post-mortems)
**Traction assessment:** high - [PROVED] one genuine GRH leaf was removed by a written candidate proof and four tempting shortcuts now have exact obstructions; [EMPIRICAL: p<=71] the right-order-aware algebraic fixture and its cost residuals are reproducible.
