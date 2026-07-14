# Standards audit under an explicit accounting

## 1. Audit profile A256

This audit does not claim to recover undocumented historical intent.

**Definition.** Profile A256 fixes the named approximately 128-bit security
level, a prime subgroup of at most 256 bits, and the published generator
document. It uses two target projections:

- **core:** field plus curve equation, modulo only conversions explicitly
  fixed by the source;
- **package:** the core plus subgroup, cofactor, base point, and representation
  parameters.

**Definition.** The category rules are:

1. A value obtained by a fully specified derivation and forced first-passing
   rule costs zero bits.
2. An unexplained \(L\)-bit seed receives the *full-seed sensitivity cap*
   \(b\leq L\): all \(2^L\) inputs are conservatively treated as screenable.
   This is a cap, not a historical claim that every seed was tried.
3. An explicit random choice, a “choose one solution” step, or an unresolved
   finite solution set with \(m\) distinguishable outputs costs
   \(\log_2m\) bits.
4. A published literal with no finite source menu or exhaustive selection
   rule is marked \(\bot\) (*not identifiable from the source*). Its encoding
   length is not substituted for menu size.
5. A parameter designated as a profile input is reported conditionally, such
   as \(b_{\mid p}\). Unresolved upstream freedom remains visible in the
   boundary-debt column.
6. The curve-core count quotients out base-point-only choices. The package
   count does not.

The audited value is a selection-capacity upper bound. It is exact only when
the cited source gives the complete menu and distinctness is established.

### Category vector

The following vector prevents apparently default choices from disappearing:

| Curve | profile / size | field | equation form | primitive / encoding | seed | counter / stop | safety / cofactor | base point |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P-256 | 0 | \(\bot\) upstream; 0 given \(p\) | \(\leq1\) for the two \(b\)-roots after \(a=-3\) | SHA-1/big-endian: 0 | \(\leq160\) | forced hash expansion; arbitrary reseed on failure | 0 | \(\leq256\) package-only |
| Curve25519 | 0 | \(\bot\) upstream; 0 given \(p\) | 0 | no hash; canonical integers: 0 | 0 | 0 | 0 | \(\leq1\) for affine \(v\)-sign; 0 for X25519's \(u\)-only package |
| brainpoolP256r1 | 0 | 0 from \(\pi\) seed | 0 | SHA-1/big-endian: 0 | 0 from \(e\) | 0 | 0 | 1 package-only |
| secp256k1 | 0 | \(\bot\) | \(\bot\) | fixed representation: 0 | none | repeated selection stated, domain/order absent | fixed published \(h\): 0 | \(\bot\) |
| BLS12-381 | 0 | derived from \(u\), but \(u:\bot\) | coefficient/family choice: \(\bot\) | fixed formulas: 0 | none | optimization claim, incomplete domain/order | stated criteria, no exhaustive rule | 0 given the surviving canonical-generator rule |

## 2. Results

| Curve / source boundary | Field | Curve source | Counter / stop | Base point | A256 core \(b\) | A256 package \(b\) | Boundary debt |
|---|---:|---:|---:|---:|---:|---:|---|
| NIST P-256, fixed \(p\), \(a=-3\), SHA-1 rule | input | arbitrary 160-bit seed plus at most two \(b\)-roots | forced hash expansion; arbitrary reseed on failure | any order-\(n\) point; sample supplied | \(\leq161\) | \(\leq417\) | selection of \(p\), model, seed provenance |
| Curve25519 / RFC 7748, fixed \(p\) | input | minimal acceptable \(A\) | forced first | minimal positive \(u\); affine sign unresolved | \(0\) | \(\leq1\) affine; 0 u-only | exhaustive field-selection rule |
| brainpoolP256r1 / RFC 5639 | \(\pi\)-derived | \(e\)-derived | forced increment / first pass | random choice of \(Q\) or \(-Q\) | \(0\) | \(1\) | target-size and policy choice only |
| secp256k1 / SEC 2 v1 and v2 | literal | literals \(a=0,b=7\) | repeated endomorphism-compatible selection until prime order; no domain/order | literal | \(\bot\) | \(\bot\) | finite menus/order for \(p,a,b,G\) |
| BLS12-381 / construction note plus earliest surviving linked commit | derived from literal \(u\) | literal \(u\), coefficient 4 | optimization criteria stated; domain and tie order incomplete | canonical rule in surviving repository | \(\bot\) | \(\bot\) | finite menu/order for \(u\); pre-publication transcript |

**[PROVED]** With \(a=-3\), every nonzero square relation
\(cb^2=-27\pmod p\) has at most two roots. The P-256 package cap therefore
uses at most \(2^{160}\) seeds, two coefficient roots per seed, and fewer than
\(2^{256}\) nonidentity base-point choices, so it is at most 417 bits. This is
not an exact joint count because seeds or roots may fail safety or collide.

**[PROVED]** Base-point freedom is irrelevant to a weakness set that depends
only on the curve core, which is why the core and package columns differ.

## 3. Source trace and judgement calls

### NIST P-256

- **[CITED]** FIPS 186-4 says the recommended curves were generated using
  SHA-1 and the ANSI X9.62 / IEEE 1363-2000 method; it lists P-256's 160-bit
  seed, derived coefficient, order, and base point (NIST 2013, FIPS 186-4,
  Appendix D.1.2.3).
- **[CITED]** The same appendix says any point of order \(n\) can serve as the
  base point and calls the supplied point a sample (NIST 2013, FIPS 186-4,
  Appendix D.1.1.5).
- **[CITED]** The prime-case generation procedure says to choose an arbitrary
  160-bit seed, deterministically expands it with SHA-1 and incremented
  internal blocks, and returns to the arbitrary seed choice when the
  candidate is unsuitable. It then says to choose \(a,b\) satisfying
  \(cb^2=a^3\) (NIST 2013, FIPS 186-4, Appendices D.5--D.6).
- **Judgement. [PROVED]** The seed is charged under the full-seed sensitivity
  rule, and fixing P-256's \(a=-3\) leaves at most two coefficient roots, for
  one additional bit. The field is held at the boundary rather than assigned
  an encoding-length surrogate. The core cap is therefore 161 bits; including
  all possible subgroup generators gives the conservative 417-bit package
  cap.

### Curve25519

- **[CITED]** Given \(p\), RFC 7748 selects the minimal positive compatible
  Montgomery coefficient \(A\) with the required curve/twist cofactors and
  prime quotients, and selects the base point with minimal positive
  \(u\)-coordinate in the correct subgroup (Langley, Hamburg, and Turner
  2016, RFC 7748, Appendix A).
- **[CITED]** The appendix's base-point code takes a square root after fixing
  \(u\), but its mathematical prose minimizes only \(u\), not the sign of
  \(v\) (Langley, Hamburg, and Turner 2016, RFC 7748, Appendix A.3).
- **[CITED]** RFC 7748 also says the precise field prime depends on
  implementation concerns that the document does not fully articulate
  (Langley, Hamburg, and Turner 2016, RFC 7748, Appendix A).
- **[CITED]** The original Curve25519 paper records six field-prime candidates
  and chooses \(2^{255}-19\) by the smallest reduction constant; it also
  records the successive acceptable \(A\) values and the reasons the first
  two were rejected (Bernstein 2006, PKC 2006).
- **Judgement. [PROVED]** The RFC derivation has zero curve-core selection
  capacity after \(p\) is fixed. A full affine base-point package has at most
  one sign bit, while the X25519 \(u\)-only package quotients it out. The
  documented field rationale is valuable evidence, but neither source defines
  an exhaustive precommitted universe of field shapes, so the unconditional
  provenance count is not inferred to be zero.

### brainpoolP256r1

- **[CITED]** RFC 5639 fixes big-endian conversion, SHA-1, seed increments,
  prime search, curve tests, and first-passing rules (Lochter and Merkle 2010,
  RFC 5639, Appendix A).
- **[CITED]** Its field seeds are consecutive 160-bit substrings derived from
  \(\pi\), and its curve seeds are consecutive 160-bit substrings derived
  from \(e\) (Lochter and Merkle 2010, RFC 5639, Appendix A.1--A.2).
- **[CITED]** Step 12 explicitly chooses at random between the two points
  \(Q\) and \(-Q\) having the smallest x-coordinate before multiplying by a
  derived scalar (Lochter and Merkle 2010, RFC 5639, Appendix A.2).
- **Judgement. [PROVED]** The sign choice does not change the curve core but yields two
  distinguishable base-point packages, so the audit assigns zero core bits
  and one package bit. Forced seed increments do not add capacity because
  the source does not permit skipping a passing candidate.

### secp256k1

- **[CITED]** SEC 2 v1 states that the prime-field Koblitz parameters were
  obtained by repeatedly selecting parameters admitting an efficiently
  computable endomorphism until a prime-order curve was found (SECG 2000,
  SEC 2 v1, Section 2.1).
- **[CITED]** The same edition publishes the full secp256k1 tuple but does not
  define the candidate domain, enumeration or sampling distribution, rejected
  candidates, or base-point selection rule (SECG 2000, Section 2.7.1).
- **[CITED]** SEC 2 v2 Section 2.4.1 specifies the tuple
  \((p,a,b,G,n,h)\), including \(a=0\) and \(b=7\), and classifies it as a
  Koblitz curve; that section gives constants but no seed, candidate
  enumeration, or stopping rule (SECG 2010, SEC 2 v2).
- **Judgement. [PROVED]** The v1 sentence establishes a broad prime-order
  stopping condition, but it leaves multiple histories with different menu
  sizes compatible with the published tuple. Fixed literals make document
  replay deterministic, but replay is not provenance. Profile A256 therefore
  reports \(\bot\), not zero and not the sum of the literals' bit lengths.

### BLS12-381

- **[CITED]** The original construction note gives
  \(u=-\mathtt{0xd201000000010000}\), the formulas/values for the base and
  scalar fields, and the curves; it states goals including a 255-bit scalar
  field, a large power-of-two root of unity, efficient extension towers, and
  low Hamming weight (Bowe 2017, Electric Coin Company technical note).
- **[CITED]** That note says a future paper would give a more thorough account
  of how the construction was selected, but it does not give an exhaustive
  candidate order or first-passing rule (Bowe 2017).
- **[CITED]** The earliest surviving commit of the construction repository
  linked from the note is dated July 8, 2017. Its README gives explicit bounds
  \(q<2^{383}\), \(r<2^{255}\), the residue condition
  \(u\bmod72\in\{16,64\}\), a low-Hamming-weight objective, and says the chosen
  \(u\) gives the largest \(q\) and smallest Hamming weight meeting the stated
  requirements (Bowe, `pairing` commit `a06216f`).
- **[CITED]** That README also derives the G1 and G2 generators from the
  lexicographically smallest valid coordinates followed by cofactor scaling
  (Bowe, `pairing` commit `a06216f`).
- **[CITED]** The crates.io and docs.rs version histories begin with
  `pairing` 0.9.0 on July 8, 2017; there is no earlier published registry
  version that could preserve a pre-announcement source snapshot.
- **Judgement. [PROVED]** The surviving repository strengthens replay and
  reduces generator-only residual freedom to zero once its conventions are
  fixed. It still does not state a finite domain for signed \(u\), a numeric
  threshold for “large” \(2^n\), an unambiguous priority between the two
  optimization objectives, or a rejected-candidate transcript; moreover its
  root commit postdates the March announcement. These omissions leave
  histories with different \(u\)-menu sizes compatible with the record, so
  both unconditional counts remain \(\bot\).

## 4. Reproducibility versus provenance

**[PROVED]** Treating every literal in a published document as forced gives a
replay count of zero for almost any named curve, making the metric unable to
distinguish a documented first-passing construction from an unexplained
constant. Profile A256 avoids that collapse by reporting unidentifiable
menus rather than silently assigning zero.

**[PROVED]** Conversely, charging each literal by its encoded bit length is
not a valid reconstruction of designer freedom: a 256-bit constant may be the
forced output of a zero-choice algorithm or one item from a much larger
cross-category search. Only a precommitted menu, decision tree, or explicit
sensitivity convention supports a defensible \(b\).

**[PROVED]** The non-identifiability theorem in `DEFINITIONS.md` shows this is
not merely missing arithmetic. For a fixed published tuple, singleton and
multi-candidate histories can produce the same record, so further computation
on the tuple cannot select the historical value of \(b\). A dated menu
commitment or equivalent provenance certificate is additional evidence, not a
quantity derivable from the constants.

## 5. Comparison with the minimal generator

- **[PROVED]** The ideal canonical-beacon generator in `DEFINITIONS.md` has
  no designer-controlled residual index and therefore \(b=0\), while still
  retaining fresh randomness independent of the hidden weak set.
- **[CITED]** RFC 5639 comes closest among these sources to an end-to-end
  forced construction because it derives both field and curve seeds from
  named constants and fixes the increment rules; its explicit random point
  sign leaves one package bit (Lochter and Merkle 2010).
- **[CITED]** RFC 7748 deterministically derives the coefficient and base
  point from its field but leaves the full field-selection considerations
  outside the derivation (Langley, Hamburg, and Turner 2016).
- **[CITED]** FIPS 186-4 makes the coefficient relation verifiable from a
  published 160-bit seed but leaves the arbitrary seed and coefficient-root
  choices outside a canonical provenance rule (NIST 2013).
- **[CITED]** SEC 2's secp256k1 record and the surviving BLS12-381 design
  record do not publish finite selection menus sufficient for a source-only
  provenance number (SECG 2000, 2010; Bowe 2017; Bowe `pairing` commit
  `a06216f`; crates.io `pairing` 0.9.0).

## 6. What the audit does not say

**[PROVED]** A large, small, or unidentifiable \(b\) is not evidence about a
designer's motive. It measures only selection capacity under a stated
contract. It also does not replace conventional curve, twist, subgroup,
implementation, or protocol security analysis.
