---
attempt: A003
status: dead
---
# A003 — Bounded rational reconstruction

## Idea

Define $x\in\mathbb F_p$ to be small when
$x\equiv a/b\pmod p$ for integers $|a|,|b|<B$ with $b\ne0$, using
$B=\lfloor\sqrt p\rfloor$.

## Plan

Enumerate the exact image of the bounded ratio map, count the corresponding
curve points on the three A001 curves, and stop before decomposition search if
the factor base itself is already too large.

## Execution log

`code/measure_structured_candidates.py` enumerated every ratio for the strict
bounds and counted curve points by exact square-root multiplicities. The full
three-size run completed in 0.5 seconds including Candidate D-proxy work.

## Outcome

[EMPIRICAL: p=65519,262139,1048571] The ratio condition selected 99.9695%,
99.9893%, and 99.9989% of all field elements, respectively.

[EMPIRICAL: the same three prime-order curves] The resulting factor bases had
65,522, 261,406, and 1,046,880 points, equal to 99.9771%, 99.9904%, and
99.9984% of the whole groups.

[EMPIRICAL: tested range only] A uniform target itself is therefore a one-term
decomposition with the preceding probabilities, but this succeeds only because
the candidate is essentially the whole group.

[PROVED] The implementation's explicit ratio-image table gives constant-time
lookup only after $\Theta(p)$-scale preprocessing and does not certify formal
condition (2). This issue is secondary here because the measured base already
fails the intended size regime by factors of 256, 511, and 1,022 relative to
$\sqrt p$.

## Post-mortem

**Why it failed:** [EMPIRICAL: tested range] Allowing both numerator and
denominator to approach $\sqrt p$ makes the rational representation condition
almost universal, so its extra arithmetic structure buys density by discarding
the small-base requirement.

**What transfers:** [CONJECTURE] A useful rational-height candidate must keep
the product of numerator and denominator bounds substantially below $p$.
Testing asymmetric bounds $AB=p^\theta$ for $\theta<1$ would refute this
guidance if it produced both a small base and a faster finder.

**Would it work under different assumptions?** [CONJECTURE] Smaller or
asymmetric bounds may avoid saturation, but they also reduce the
three-decomposition count; an explicit polylogarithmic solver would be needed
to make the tradeoff useful.
