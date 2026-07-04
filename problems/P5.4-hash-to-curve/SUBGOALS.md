# Sub-goals - P5.4

- [x] **SG-01a:** Implement RFC 9380 simplified SWU over toy prime fields with $A B\ne0$, validate every input on at least two curves, and test the exceptional input $u=0$.
- [x] **SG-01b:** Implement RFC 9380 Elligator 2 for toy Montgomery curves, validate every input on at least two curves, and exercise the $Z u^2=-1$ exceptional case when it exists.
- [x] **SG-01c:** Add seeded smoke/full scripts, independent formula oracles, deterministic CSV output, tests, and a recorded runtime.
- [x] **SG-02a:** Enumerate exact applicability predicates for SSWU, SSWU-through-isogeny, Elligator 2, and rational Montgomery-to-Edwards transport.
- [x] **SG-03a:** Construct and validate a toy $j=0$ isogeny workaround without using production parameters.
- [x] **SG-04a:** Construct and validate a toy $j=1728$ isogeny workaround without using production parameters.
- [x] **SG-05a:** Determine whether the compile-time cases share one parameterized straight-line interface or require genuinely distinct maps.
- [x] **SG-06a:** Audit the implementation schedule and run preregistered timing-distribution comparisons on the Python toy backend; a compiled production backend remains outside this session.
- [x] **SG-07a:** State the exact admissibility hypotheses needed by the two-map indifferentiability theorem and check each compile-time case against them.
- [x] **SG-08a:** Implement the RFC SvdW straight-line fallback and exhaustively validate it first on toy $j=0$ and $j=1728$ curves.
- [x] **SG-09a:** Implement and exhaust toy rational transports for Montgomery and twisted-Edwards forms, including subgroup-cleared two-map sums.
- [x] **SG-10a:** Extend the construction and its independent oracle to extension fields and determine separate characteristic-two and characteristic-three routes.
- [x] **SG-11a:** Reimplement one selected toy suite on a compiled fixed-width field and exception-complete group backend, inspect generated code, and rerun leakage tests.
- [ ] **SG-11b:** Generalize the compiled backend across the full registered compile-time family and replace target-specific code-generation evidence with a portable constant-time argument or certificate.
- [ ] **SG-12a:** Run production RFC curve-suite vectors only if the shared $\log_2q\le60$ ceiling is explicitly lifted; until then retain the Appendix K XMD anchors and exhaustive toy ground truth.
