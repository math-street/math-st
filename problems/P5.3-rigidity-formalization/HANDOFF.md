# Handoff — P5.3 after session 4

## State in five lines

The fixed-menu game, accounting contract, and main theorem are in
`DEFINITIONS.md`.
The five-curve A256 audit and its source boundaries are in `AUDIT.md`.
A002 supplies the coefficient-uniform toy sampler; A004 supplies the
class-uniform refinement and exact \(p=127\) census.
Q014 and Q015 in `OPEN_QUESTIONS.md` are self-contained evidence and
resolution ledgers for the archival and sampling-kernel questions.
All requested deliverables and SG-01 through SG-11 are complete.

## Established results

- **[PROVED]** For \(M=2^b\) screenable candidates,
  \(\Pr[\mathrm{win}]\leq\min(1,2^b\kappa\epsilon)\); candidate independence
  is unnecessary.
- **[PROVED]** Uniform marginals give the requested
  \(\min(1,2^b\epsilon)\) bound, and translated disjoint hit events attain it.
- **[PROVED]** Final constants do not identify historical \(b\): the same
  public output can arise from menus of different sizes.
- **[PROVED]** A sufficient provenance certificate fixes the complete finite
  domain, equivalence projection, generator, enumeration/ties/stopping,
  randomness origin, replay transcript, and residual branches.
- **[PROVED]** The ideal canonical-beacon generator has minimal designer
  capacity \(b=0\).
- **[CITED]** A256 core results are P-256 \(\leq161\) conditional on its
  field/model boundary, Curve25519 given \(p\) equal to 0, and
  brainpoolP256r1 equal to 0.
- **[CITED]** SEC 2 v1 gives a broad repeated-selection criterion for the
  Koblitz family, while the earliest surviving linked BLS12-381 commit gives
  partial constraints and a canonical generator rule. Neither record fixes a
  complete finite historical menu and transcript.
- **[CITED]** crates.io and docs.rs both begin the public `pairing` history at
  0.9.0 on 2017-07-08; there is no earlier registry snapshot in that channel.
- **[CONDITIONAL: SHAKE256 blocks are independent uniform strings]** A002 is
  uniform over passing coefficient encodings, and A004 is uniform over the 67
  canonical safe isomorphism classes under the fixed toy profile.
- **[EMPIRICAL: exhaustive enumeration at \(p=127\)]** There are 258
  nonsingular classes from 16,002 coefficient encodings. The safety predicate
  retains 67 classes and 4,179 encodings with orbit histogram
  \(\{21:1,63:66\}\).
- **[PROVED]** Conditional on the census, coefficient-uniform class masses are
  \(1/199\) and \(3/199\), versus \(1/67\) under class-uniform sampling; the
  total-variation distance is \(132/13333\).
- **[PROVED]** Uniform is the unique minimizer of maximum singleton
  probability on a fixed finite universe, so the forced class-uniform
  generator is the toy minimax answer and has \(b=0\).

## Audit result

| Curve | A256 core \(b\) | A256 package \(b\) | Boundary |
|---|---:|---:|---|
| P-256 | \(\leq161\) | \(\leq417\) | fixed field/model; full-seed sensitivity |
| Curve25519 | \(0\) given \(p\) | \(\leq1\) affine; 0 u-only | field-selection universe |
| brainpoolP256r1 | \(0\) | \(1\) | explicit point-sign choice |
| secp256k1 | \(\bot\) | \(\bot\) | no finite historical menu/order |
| BLS12-381 | \(\bot\) | \(\bot\) | incomplete \(u\)-domain/objective order |

## Interpretation invariant

**[PROVED]** \(\bot\) means “not identifiable from the cited public record.”
It means neither zero nor infinity and carries no claim about motive. Encoded
literal length must not be substituted for menu size.

## Reopening condition

Reopen Q014 only for a dated pre-publication artifact that constrains the
admissible historical fiber by fixing the missing finite domain, selection
order/objective priority, and transcript. Later folklore alone is
insufficient. Q015 is closed for the fixed toy universe; a production-scale
profile would be a separately authorized problem.

## Files that matter

`DEFINITIONS.md`, `AUDIT.md`,
`OPEN_QUESTIONS.md`,
`attempts/A001-fixed-menu-game.md`,
`attempts/A002-toy-first-passing.md`,
`attempts/A003-archival-provenance.md`,
`attempts/A004-registry-and-class-kernel.md`,
`code/sample_rigid_curve.py`,
`code/class_uniform_kernel.py`,
`code/tests/test_class_uniform_kernel.py`,
`data/class_kernel_b7_20260708.json`,
`data/class_kernel_b7_20260708.csv`, and
`refs/crates-pairing2017.md`.

## Final validation

`env/check_env.py` passed under Python 3.13.4. The combined shared and P5.3
suite passed 79 tests, `compileall` succeeded, no unresolved-status tag
remains, and the Markdown control-character scan was clean. Deterministic
replay produced SHA-256
`1BA019A7DA47C2FB64764B3D9A79680C7CB2904D6AD9062899069689AEB03F15`
for the JSON and
`EDC4C7875E2CE7A0AB0F44529BD65A99D35ADF5A57C8E485070B983DBFD382A9`
for the CSV.
