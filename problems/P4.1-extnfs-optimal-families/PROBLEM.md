# P4.1 — Optimal pairing-friendly families under exTNFS

## Formal statement

**Setting.** A pairing-friendly curve $E/\mathbb{F}_p$ has subgroup order $r$, embedding degree $k$, and $\rho = \log p / \log r$.

**Objective.** For a target security level $\lambda$, minimize $\rho$ subject to a selected exTNFS cost model assigning at least $\lambda$ bits to the extension-field discrete logarithm problem and Pollard rho assigning at least $\lambda$ bits to the subgroup discrete logarithm problem.

**Deliverable.** Produce a reproducible, explicitly parameterized search tool and optimization tables for $\lambda \in \{128,192,256\}$.

## Required scope

- SG-01: implement and calibrate a transparent exTNFS cost model against a published BN254 estimate.
- SG-02: implement BN, BLS12, BLS24, and KSS16 family generators and verify their embedding degrees.
- SG-03: sweep valid seeds and record exTNFS security, Pollard security, and $\rho$.
- SG-04/05: optimize for 128, 192, and 256 bits in an explicitly stated search space.
- SG-06: vary cost-model assumptions and report movement of the optimum.
- SG-07: expose operation costs as a secondary objective.

## Validation targets

- Reproduce a published revised-security estimate for BN254 within a stated tolerance.
- Match the published BLS12-381 parameters exactly from its family seed.
- Independently verify pairing-friendliness for every generated candidate.

## Scope note

[PROVED] Large published parameter constants are used only as deterministic regression fixtures for polynomial evaluation; no attack or real-world cryptanalytic run is performed. The experimental search remains bounded by the toy-size ceiling from `00_SCAFFOLD.md` unless a later session records a separate justification.
