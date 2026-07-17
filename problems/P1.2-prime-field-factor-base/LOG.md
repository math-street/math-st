# Session log

Full entries for sessions 1–5 are in `LOG-archive/LOG-001-005.md`.

- **Session 1 — 2026-06-22:** [EMPIRICAL: $p$ near $2^{16},2^{18},2^{20}$]
  Established the random baseline and Candidate-A comparison; reproduced the
  extension-field control and measured Candidates B–D.
- **Session 2 — 2026-06-25:** [PROVED] Consolidated the natural-candidate
  obstructions and isolated existence from finder complexity.
- **Correction to Session 2 — 2026-06-25:** [PROVED] The standard
  $L_p[1/2,c]$/fixed-$m$ statement is impossible by support size; the
  square-root experiment addresses only a corrected interpretation.
- **Session 3 — 2026-06-30:** [PROVED] Audited the uncharged-preprocessing
  loophole with a radix base and a complete target-indexed table, then wrote
  the resource-bounded Variants S and L.
- **Session 4 — 2026-07-07:** [PROVED] Established the
  $T|\mathcal F|/r$ translate-probe success bound and closed P1.2/Q001 in that
  restricted model.
- **Session 5 — 2026-07-13:** [EMPIRICAL: $p=17,257,65537$] Validated the
  smooth-subgroup coordinate predicate, found no density or generic-scan
  advantage, recorded Gröbner timeouts separately from mathematical failure,
  and closed A010 without resolving corrected-Variant-S P1.2/Q004.

## Session 6 — 2026-07-17

**Goal:** Make the root question register globally unambiguous and make the
P1.2 entries independently resumable.

**Protocol note:** This follow-up began as a documentation-status correction,
so no mathematical experiment was preregistered. The administrative invariant
checked at the end is that every root heading has one unique namespaced ID and
that every live P1.2 reference uses it.

**Did:**

- Audited all root question headings against their recorded owning problems.
- Added a complete status index, namespaced every heading, and expanded all
  four P1.2 entries with status, scope, established evidence, gap, blocking
  condition, closure criterion, and non-solutions where applicable.
- Synchronized P1.2 state, notes, sub-goals, attempts, audit, and handoff.

**Found:**

- [EMPIRICAL: root heading audit] The register contains 31 question sections
  and 31 unique full identifiers after normalization.
- [PROVED] P1.2/Q001 is closed only in its stated model; P1.2/Q002 is an
  optional Candidate-D predicate gap; P1.2/Q003 requires a human specification
  choice; P1.2/Q004 remains open only under corrected Variant S.

**Next:** None for literal P1.2. Resume only the specifically selected open
question under its recorded closure criterion.

**Final validation:**

- [EMPIRICAL: root register audit] All 31 question headings have distinct
  namespaced identifiers, the index and body identifier sets are equal, every
  owner prefix names an existing problem directory, and zero bare numeric
  question references remain in `OPEN_QUESTIONS.md`.
- [EMPIRICAL: section-structure audit] Every one of the 31 question sections
  contains tagged evidence and an explicit status, gap, residual question, or
  resolution disposition.
- [EMPIRICAL: local CPython 3.13.4] All 70 currently present shared tests and
  all 17 P1.2 tests passed; `HANDOFF.md` remains below its cap at 117 lines.
