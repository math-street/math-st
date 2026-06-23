# Log

## Session 1 — 2026-06-23

**Goal:** Complete SG-01's linear-algebra fallback, validate one published genus, and exhaustively tabulate degrees 4, 6, and 8.

**Prediction (written before running anything):** [HEURISTIC] Every nonzero parameter will have a magic number between 1 and $n$, and the lower genera will occur on a visibly thin union of Frobenius-stable orbits. This is falsified if the sweep finds an out-of-range magic number, violates Frobenius invariance, or puts most degree-8 parameters in the two smallest genera.

**Positive result criterion:** The published example returns genus 31, all field and rank unit tests pass, and independently recomputed Frobenius-orbit rows agree.

**Negative result criterion:** A mismatch with the cited genus or any failure of the rank/genus invariants invalidates the implementation and is recorded before interpretation.

**Did:**
- Ran `env/check_env.py`; Python 3.13.4 is present and SageMath, Singular, and msolve are absent.
- Ran all 13 pre-existing shared-library tests; all passed.
- Checked the GHS magic-number statement against Gaudry–Hess–Smart (2002) and the exact genus specialization against Hess (2003).

**Found:**
- [CITED] The GHS magic number uses the span of pairs $(1,\sigma^i(\sqrt b))$, not merely the span of the conjugates (Gaudry–Hess–Smart, 2002).
- [CITED] The exact choice between $2^{m-1}$ and $2^{m-1}-1$ is determined by whether $1$ lies in the conjugate span (Hess, 2003).

**Prediction vs. outcome:** pending computation.
**Did not work:** nothing yet.
**Changed my mind about:** The two possible genera are not an unavoidable ambiguity; the conjugate-span containment test resolves the branch.
**Next:** Implement and test the binary-field and GHS routines.

### Session 1 completion

**Did:**
- Implemented and tested polynomial-basis binary fields, Frobenius spans and annihilators, the magic number, and the exact genus branch.
- Reconstructed the Magma V2.19.8 genus-31 example over $\mathbb F_{2^{155}}/\mathbb F_{2^5}$.
- Exhausted all 333 nonzero parameters at degrees 4, 6, and 8; generated the full CSV, aggregate CSV, locus CSV, and SVG plot.

**Found:**
- [EMPIRICAL: `code/verify_published_example.py`] The published example has annihilator $t^5+t^2+1$, conjugate rank $5$, magic number $6$, and genus $31$.
- [EMPIRICAL: all $b\ne0$, $n\in\{4,6,8\}$] The minimum genus on full-degree parameters is $4$, $8$, and $16$.
- [EMPIRICAL: all $b\ne0$, $n\in\{4,6,8\}$] For the threshold $B_n=2^{n/2}$, the low-genus counts are $7$, $15$, and $31$, with exact densities $7/15$, $5/21$, and $31/255$.
- [EMPIRICAL: same range] Each low-genus $b$-locus with zero adjoined is one linearized-polynomial kernel; its inverse $j$-locus is Frobenius-stable but is not additive after adjoining zero.

**Prediction vs. outcome:** matched in Frobenius stability and thinning density; the data was more structured than predicted because each selected low-genus union collapsed to one linearized-polynomial kernel.
**Did not work:** Direct function-field construction was unavailable because SageMath and Magma are absent; the scaffold-authorized span/genus fallback succeeded instead.
**Changed my mind about:** For these degrees, the low-genus locus has a compact exact equation, not merely a list of exceptional parameters.
**Next:** Prove the observed counts from the published type formula, then hand-implement one explicit low-genus cover and toy DLP map.

### Correction to Session 1 — outcome classification

**Outcome:** FAILED.

The earlier completion notes describe valid partial computations, but they do not satisfy the requested GHS construction or the end-to-end toy-attack validation target. A001 is therefore closed as dead; its data is retained only as transferable partial work.
