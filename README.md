# math.st

**Open problems in elliptic-curve cryptography, worked by machine intelligence.**

One paper per problem. Every claim carries an epistemic tag. Negative results are
kept, not hidden.

This repository is the working record of the program: for each problem, its formal
statement, everything established so far, the attempts that failed, and the code and
data behind every empirical claim.

## What's here

```
problems/     21 open problems, grouped by category (see below)
papers/       one write-up per problem (.typ source + compiled .pdf)
lib/          shared library — curves, pairings, isogenies, dlog, finite fields
env/          toolchain notes and environment checks
BIBLIOGRAPHY.md · GLOSSARY.md · OPEN_QUESTIONS.md · 00_SCAFFOLD.md
```

Each problem folder holds:

| file | what it is |
|---|---|
| `PROBLEM.md` | the formal statement |
| `STATE.md` | current status, one-line state, last/next action |
| `LOG.md` | session-by-session record (predictions written before running) |
| `HANDOFF.md` | findings and state of play for the next session |
| `attempts/` | individual attempts, including dead ends, with post-mortems |
| `code/` · `data/` · `refs/` | scripts, their outputs, and checked sources |

## Categories

1. **Hardness of the discrete logarithm** — lower bounds, factor bases, descent and transfers
2. **Assumptions & reductions** — what the standard assumptions actually buy, and their limits
3. **Isogenies & quantum** — endomorphism rings, class-group actions, torsion leakage
4. **Pairings & exTNFS** — pairing-friendly families and cycles, extended NFS cost
5. **Curve generation & practice** — Koblitz-type conjectures, CM security, hash-to-curve

## Status

21 problems: **3 resolved**, **1 complete** (within its stated scope), **12 partial**
(still open), **1 failed**, **4 abandoned**. A problem is only marked resolved when the
result survives a second, adversarial self-verification; work that stalls or gets ruled
out is recorded as such.

## Epistemic tags

Claims are tagged inline so the strength of each statement is explicit:

`[PROVED]` · `[REFUTED]` · `[CITED]` · `[EMPIRICAL]` · `[CONDITIONAL]` ·
`[HEURISTIC]` · `[CONJECTURE]` · `[UNVERIFIED]`

A theorem and a toy-scale observation should never read the same, so they don't.

## Reproducing

Empirical claims name the script and dataset that produced them
(`code/<script>.py` → `data/<name>_<date>.csv`). The shared library runs on
CPython with no heavyweight CAS dependency; where SageMath/PARI/Magma were
unavailable, exact arithmetic fallbacks were used and are noted in `env/SETUP.md`.
