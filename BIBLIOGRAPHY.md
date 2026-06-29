# Bibliography

## P4.3 - rigorous exTNFS smoothness

- [CITED] Taechan Kim and Razvan Barbulescu, “Extended Tower Number Field Sieve: A New Complexity for the Medium Prime Case,” CRYPTO 2016, LNCS 9814, 543--571, DOI 10.1007/978-3-662-53018-4_20; IACR ePrint 2015/1027. Relevance: audited exTNFS algorithm, norm forms, heuristic relation yield, initial splitting, descent, and constants. <https://eprint.iacr.org/2015/1027>
- [CITED] E. R. Canfield, Paul Erdos, and Carl Pomerance, “On a Problem of Oppenheim Concerning ‘Factorisatio Numerorum’,” *Journal of Number Theory* 17(1), 1--28, 1983, DOI 10.1016/0022-314X(83)90002-1. Relevance: uniform random-integer smoothness benchmark. <https://doi.org/10.1016/0022-314X(83)90002-1>
- [CITED] Razvan Barbulescu and Sylvain Lachand, “Some Mathematical Remarks on Polynomial Selection in NFS,” *Mathematics of Computation* 86, 397--418, 2017, DOI 10.1090/mcom/3112; arXiv:1403.0184. Relevance: fixed binary-form products, fixed-number-field smooth ideals, and fixed quadratic-form partial results. <https://arxiv.org/abs/1403.0184>
- [CITED] Antal Balog, Valentin Blomer, Cecile Dartyge, and Gerald Tenenbaum, “Friable Values of Binary Forms,” *Commentarii Mathematici Helvetici* 87, 639--667, 2012, DOI 10.4171/CMH/264. Relevance: unconditional fixed-binary-form smooth-value lower bounds outside the exTNFS range. <https://doi.org/10.4171/CMH/264>
- [CITED] E. Lee and Ramarathnam Venkatesan, “Rigorous Analysis of a Randomised Number Field Sieve,” *Journal of Number Theory* 187, 92--159, 2018, DOI 10.1016/j.jnt.2017.10.019; arXiv:1805.08873. Relevance: rigorous ordinary-NFS relation generation by coefficient randomization and its limits. <https://arxiv.org/abs/1805.08873>
- [CITED] Carl Pomerance, “Fast, Rigorous Factorization and Discrete Logarithm Algorithms,” in *Discrete Algorithms and Complexity*, 119--143, 1987. Relevance: rigorous randomization precedent for prime fields and fields of characteristic two. <https://math.dartmouth.edu/~carlp/disclog.pdf>
- [CITED] Renet Lovorn Bender and Carl Pomerance, “Rigorous Discrete Logarithm Computations in Finite Fields via Smooth Polynomials,” *AMS/IP Studies in Advanced Mathematics* 7, 221--232, 1998. Relevance: rigorous same-DLP fallback with worse medium-characteristic complexity. <https://math.dartmouth.edu/~carlp/PDF/paper115.pdf>
- [CITED] Hendrik W. Lenstra Jr., Jonathan Pila, and Carl Pomerance, “A Hyperelliptic Smoothness Test, I,” *Philosophical Transactions of the Royal Society A* 345, 397--408, 1993, DOI 10.1098/rsta.1993.0138; and Part II, *Proceedings of the London Mathematical Society* 84, 105--146, 2002, DOI 10.1112/plms/84.1.105. Relevance: rigorous accepted-candidate factorization in subpolynomial-in-the-bound expected time. <https://math.dartmouth.edu/~carlp/hyperI.pdf>
- [CITED] Oliver Schirokauer, “The Number Field Sieve and the Discrete Logarithm Problem,” in *Surveys in Algorithmic Number Theory*, MSRI Publications 44, 397--420, 2008. Relevance: valuation/Schirokauer relation matrix, explicit expected-rank step, and sparse linear-algebra cost conditional on solvability. <https://library.slmath.org/books/Book44/files/12oliver.pdf>
- [CONDITIONAL: GRH] Johannes A. Buchmann and Christine S. Hollinger, “On Smooth Ideals in Number Fields,” *Journal of Number Theory* 59(1), 82--87, 1996, DOI 10.1006/jnth.1996.0088. Relevance: degree-dependent smooth-ideal lower bounds under GRH; still not a count of short paired principal generators. <https://doi.org/10.1006/jnth.1996.0088>

## P5.3 — curve-generation rigidity

- [CITED] National Institute of Standards and Technology, *Digital Signature
  Standard (DSS)*, FIPS PUB 186-4, July 2013,
  doi:10.6028/NIST.FIPS.186-4. Relevance: publishes the P-256 SHA-1 seed,
  parameters, and base-point policy.
  <https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf>
- [CITED] Adam Langley, Mike Hamburg, and Sean Turner, *Elliptic Curves for
  Security*, RFC 7748, January 2016, doi:10.17487/RFC7748. Relevance: gives
  deterministic coefficient and base-point derivations for Curve25519 after
  the field prime is fixed. <https://www.rfc-editor.org/rfc/rfc7748.html>
- [CITED] Daniel J. Bernstein, “Curve25519: New Diffie-Hellman Speed Records,”
  *PKC 2006*, LNCS 3958, 207–228. Relevance: records the field and coefficient
  shortlists and selection rationale.
  <https://cr.yp.to/ecdh/curve25519-20060209.pdf>
- [CITED] Manfred Lochter and Johannes Merkle, *Elliptic Curve Cryptography
  (ECC) Brainpool Standard Curves and Curve Generation*, RFC 5639, March
  2010, doi:10.17487/RFC5639. Relevance: fixes SHA-1, seeds derived from
  \(\pi\) and \(e\), counters, stopping rules, and an explicit base-point sign
  choice. <https://www.rfc-editor.org/rfc/rfc5639.html>
- [CITED] Standards for Efficient Cryptography Group, *SEC 2: Recommended
  Elliptic Curve Domain Parameters*, version 2.0, January 27, 2010. Relevance:
  publishes secp256k1 constants without a generation menu.
  <https://www.secg.org/sec2-v2.pdf>
- [CITED] Standards for Efficient Cryptography Group, *SEC 2: Recommended
  Elliptic Curve Domain Parameters*, version 1.0, September 20, 2000.
  Relevance: states the repeated-selection/prime-order criterion for
  prime-field Koblitz curves but does not give the candidate domain or order.
  <https://www.secg.org/SEC2-Ver-1.0.pdf>
- [CITED] Sean Bowe, “BLS12-381: New zk-SNARK Elliptic Curve Construction,”
  Electric Coin Company technical blog, March 11, 2017. Relevance: publishes
  the BLS family parameter and design goals but not an exhaustive search
  order. <https://electriccoin.co/blog/new-snark-curve/>
- [CITED] Sean Bowe, `pairing` repository, root commit `a06216f`, July 8,
  2017. Relevance: records BLS12-381's optimization claim, partial candidate
  constraints, and canonical generator rule; the reachable history contains
  no earlier selection transcript.
  <https://github.com/zkcrypto/pairing/commit/a06216f24b488fa2a25b42366cb3d3614218a7b5>
- [CITED] crates.io and docs.rs, `pairing` 0.9.0 version records, July 8,
  2017. Relevance: 0.9.0 is the earliest registry version, so no pre-0.9
  package snapshot predates the surviving Git root.
  <https://crates.io/crates/pairing/0.9.0>

## P3.3 verified references

- [CITED] David Kohel, Kristin Lauter, Christophe Petit, and Jean-Pierre
  Tignol, "On the quaternion $\ell$-isogeny path problem," *LMS Journal of
  Computation and Mathematics* 17(A), 418--432, 2014,
  doi:10.1112/S1461157014000151. Relevance: supplies the explicit maximal
  order for $p\equiv3\pmod4$, the normalized ideal norm, the
  equivalent-ideal construction, and the heuristic $p^{7/2}$ norm estimate
  for the complete basic algorithm.
  <https://doi.org/10.1112/S1461157014000151>
- [CITED] Laia Amoros, James Clements, and Chloe Martindale,
  "Parametrizing Maximal Orders Along Supersingular $\ell$-Isogeny Paths,"
  IACR Cryptology ePrint Archive, Report 2025/033, 2025. Relevance: gives
  current explicit ideal/order parametrizations and identifies optimal
  short-path finding as future work rather than a settled subroutine.
  <https://eprint.iacr.org/2025/033>

## P5.4 - universal constant-time hash-to-curve

- [CITED] A. Faz-Hernandez, S. Scott, N. Sullivan, R. S. Wahby, and C. A. Wood, *Hashing to Elliptic Curves*, RFC 9380, August 2023. Relevance: standardized SSWU, Elligator 2, isogeny workarounds, cofactor clearing, straight-line procedures, security conditions, and suite test vectors. <https://www.rfc-editor.org/rfc/rfc9380.html>
- [CITED] Eric Brier, Jean-Sebastien Coron, Thomas Icart, David Madore, Hugues Randriam, and Mehdi Tibouchi, "Efficient Indifferentiable Hashing into Ordinary Elliptic Curves," *CRYPTO 2010*, LNCS 6223, 237--254; full version IACR ePrint 2009/340. Relevance: characteristic-three encodings and the odd-degree binary Shallue--van de Woestijne construction used in session 3. <https://eprint.iacr.org/2009/340.pdf>

## P1.6 verified references

- [CITED] Michael J. Jacobson, Neal Koblitz, Joseph H. Silverman, Andreas
  Stein, and Edlyn Teske, "Analysis of the Xedni Calculus Attack," *Designs,
  Codes and Cryptography* 20, 41--64, 2000. Relevance: gives the conditional
  constant-relation-coefficient argument and practical xedni experiments.
  <https://pages.cpsc.ucalgary.ca/~jacobs/PDF/xedni.pdf>
- [CITED] Joseph H. Silverman, "The Xedni Calculus and the Elliptic Curve
  Discrete Logarithm Problem," *Designs, Codes and Cryptography* 20, 5--40,
  2000. Relevance: primary algorithm referenced by the failure analysis; the
  proposal was announced and circulated in 1998 before journal publication.
- [CITED] LMFDB Collaboration, "Canonical height on an elliptic curve" and
  rational elliptic-curve data for 11.a2 and 389.a1. Relevance: fixes the
  height normalization and supplies independent validation values.
  <https://www.lmfdb.org/knowledge/show/ec.canonical_height>

## P4.2 - pairing-friendly curve cycles

- [CITED] Alessandro Chiesa, Lynn Chua, and Matthew Weidner, "On Cycles of
  Pairing-Friendly Elliptic Curves," *SIAM Journal on Applied Algebra and
  Geometry* 3(2), 175-192, 2019, doi:10.1137/18M1173708;
  arXiv:1803.02067. Relevance: MNT cycle classification, explicit MNT6/MNT4
  toy curves, and non-existence for the degree pairs (5,10), (8,8), and
  (12,12). <https://arxiv.org/abs/1803.02067>
- [CITED] Marta Belles-Munoz, Jorge Jimenez Urroz, and Javier Silva,
  "Revisiting Cycles of Pairing-Friendly Elliptic Curves," IACR ePrint
  2022/1662, 2022. Relevance: family-based 2-cycle exclusions and the
  exceptional MNT3/degree-10 pair over fields 11 and 7.
  <https://eprint.iacr.org/2022/1662>
- [CITED] Computational Algebra Group, *Magma Handbook*, V2.29, 2026,
  "Integral and S-integral Points" and "Two-Selmer Set of a Curve."
  Relevance: exact integral quartic points and the empty fake two-Selmer-set
  criterion used to close the final P4.2 quartic curves.
  <https://magma.maths.usyd.edu.au/magma/handbook/text/1566>
  <https://magma.maths.usyd.edu.au/magma/handbook/text/1618>


## P2.1 verified references

- [CITED] Ueli M. Maurer and Stefan Wolf, "The Relationship Between Breaking
  the Diffie--Hellman Protocol and Computing Discrete Logarithms," *SIAM
  Journal on Computing* 28(5), 1689--1721, 1999,
  doi:10.1137/S0097539796302749. Relevance: gives the auxiliary-group
  reduction, exact smoothness condition, elliptic-curve embedding, and
  non-uniform Hasse-interval result used in P2.1.
  <https://crypto.ethz.ch/publications/files/MauWol99b.pdf>
- [CITED] Sarvagya Jain, "Existence of Smooth Numbers in Short Intervals,"
  *The Quarterly Journal of Mathematics* 77(2), 397--422, 2026,
  doi:10.1093/qmath/haag010. Relevance: current all-interval smooth-number
  theorem and its parameter gap from the polylogarithmic Hasse-interval regime
  required in P2.1.
  <https://academic.oup.com/qjmath/article/77/2/397/8677316>
- [CITED] Antoine Muzereau, Nigel P. Smart, and Frederik Vercauteren, "The
  Equivalence Between the DHP and DLP for Elliptic Curves Used in Practical
  Applications," *LMS Journal of Computation and Mathematics* 7, 50--72,
  2004, doi:10.1112/S1461157000001042. Relevance: identifies the small-CM-
  discriminant plus smooth-order search problem and supplies finite standard-
  curve witnesses.
  <https://doi.org/10.1112/S1461157000001042>
- [CITED] Alexander May and Carl Richard Theodor Schneider, "Dlog is
  Practically as Hard (or Easy) as DH -- Solving Dlogs via DH Oracles on EC
  Standards," *IACR Transactions on Cryptographic Hardware and Embedded
  Systems* 2023(4), 146--166, doi:10.46586/tches.v2023.i4.146-166; IACR
  ePrint 2023/539. Relevance: current practical random auxiliary-curve search
  and explicit statement of the reduction's non-uniformity.
  <https://eprint.iacr.org/2023/539>
- [CITED] Andreas Enge, "The Complexity of Class Polynomial Computation via
  Floating Point Approximations," *Mathematics of Computation* 78(266),
  1089--1107, 2009, arXiv:cs/0601104. Relevance: CM splitting and class-
  polynomial complexity, including the floating-point correctness qualifier.
  <https://arxiv.org/abs/cs/0601104>
- [CITED] Maiara F. Bollauf, Roberto Parisella, and Janno Siim, "Revisiting
  Discrete Logarithm Reductions," *IACR Communications in Cryptology* 2(2),
  2025, doi:10.62056/a0c3c3c2h; IACR ePrint 2025/1079. Relevance: concretely
  efficient den Boer reduction when $r-1$ is sufficiently smooth.
  <https://eprint.iacr.org/2025/1079>
- [CITED] Runbo Li, "An Average Brun--Titchmarsh Theorem and Shifted Primes
  with a Large Prime Factor," arXiv:2508.18285, 2025. Relevance: infinitely
  many primes with $P^+(r-1)>r^{0.679}$, obstructing the full multiplicative
  auxiliary group uniformly. <https://arxiv.org/abs/2508.18285>
- [CITED] Khalid Younis, "Asymptotics for Smooth Numbers in Short Intervals,"
  arXiv:2409.05761, 2024. Relevance: even under RH, its polylogarithmic
  smoothness range requires fixed interval exponent strictly above the Hasse
  endpoint $1/2$. <https://arxiv.org/abs/2409.05761>
- [CITED] Triantafyllos Xylouris, "On Linnik's Constant," arXiv:0906.2749,
  2009. Relevance: the effective $L=5.2$ least-prime bound used in the
  simultaneous CRT obstruction for full norm-one tori.
  <https://arxiv.org/abs/0906.2749>
- [CITED] Ivan Soprounov, "A Short Proof of the Prime Number Theorem for
  Arithmetic Progressions," preprint, 1998. Relevance: fixed-progression
  prime density used to choose comparable forced factors for every bounded
  norm-one extension degree.
  <https://academic.csuohio.edu/soprunov-ivan/wp-content/uploads/sites/93/2023/02/primes.pdf>
- [CITED] Victor V. Batyrev and Yuri Tschinkel, "Rational Points of Bounded
  Height on Compactifications of Anisotropic Tori," *International
  Mathematics Research Notices* 1995(12), 591--635,
  doi:10.1155/S1073792895000365; arXiv:alg-geom/9411009. Relevance: the
  determinant point-count formula and finite-order Frobenius lattice used to
  obstruct all full bounded-dimensional tori.
  <https://arxiv.org/abs/alg-geom/9411009>
- [CITED] Brian Conrad, "A Modern Proof of Chevalley's Theorem on Algebraic
  Groups," *Journal of the Ramanujan Mathematical Society* 17(1), 1--18,
  2002. Relevance: unique affine-kernel/abelian-variety decomposition over a
  perfect field used in A006. <https://math.stanford.edu/~conrad/papers/chev.pdf>
- [CITED] Brian Conrad, "Finiteness Theorems for Algebraic Groups over
  Function Fields," *Compositio Mathematica* 148(2), 555--639, 2012.
  Relevance: split unipotent radical and reductive quotient over perfect
  fields used in A006. <https://math.stanford.edu/~conrad/papers/cosetfinite.pdf>
- [CITED] Serge Lang, "Algebraic Groups over Finite Fields," *American
  Journal of Mathematics* 78(3), 555--563, 1956, DOI 10.2307/2372673.
  Relevance: vanishing of finite-field torsors for connected groups and the
  rational-point order factorizations used in A006.
  <https://doi.org/10.2307/2372673>
- [CITED] Raymond van Bommel, Edgar Costa, Bjorn Poonen, Alexander Smith, and
  Wanlin Li, "Abelian Varieties of Prescribed Order over Finite Fields,"
  *Mathematische Annalen* 392, 1167--1202, 2025, DOI
  10.1007/s00208-024-03084-4. Relevance: the fixed-dimension central interval
  of universally realizable abelian-surface orders used in A007.
  <https://arxiv.org/abs/2106.13651>
- [CITED] Reinier Broeker, Everett W. Howe, Kristin E. Lauter, and Peter
  Stevenhagen, "Genus-2 Curves and Jacobians with a Given Number of Points,"
  *LMS Journal of Computation and Mathematics* 18, 170--197, 2015, DOI
  10.1112/S1461157014000461. Relevance: exponential worst-case genus-two CM
  construction for prescribed Jacobian order, and the distinct heuristic
  algorithm for prescribed curve cardinality, audited in A007 and A009.
  <https://arxiv.org/abs/1403.6911>
- [CITED] David G. Cantor, "Computing in the Jacobian of a Hyperelliptic
  Curve," *Mathematics of Computation* 48(177), 95--101, 1987, DOI
  10.1090/S0025-5718-1987-0866101-0. Relevance: fixed-genus Mumford
  representation and Jacobian arithmetic used for A007's strong embedding.
- [CITED] Dan Boneh, "Finding Smooth Integers in Short Intervals Using CRT
  Decoding," *Journal of Computer and System Sciences* 64(4), 768--784,
  2002, DOI 10.1006/jcss.2002.1827. Relevance: the exact CRT list-decoding
  radius and strong-smoothness promise ruled out as a bridge from A007's RH
  existence theorem to a polynomial-time finder.
  <https://crypto.stanford.edu/~dabo/abstracts/CRTdecode.html>
- [CITED] Everett W. Howe, Enric Nart, and Christophe Ritzenthaler,
  "Jacobians in Isogeny Classes of Abelian Surfaces over Finite Fields,"
  *Annales de l'Institut Fourier* 59(1), 239--289, 2009, DOI
  10.5802/aif.2430. Relevance: complete coefficient criterion for Jacobian
  existence inside a surface isogeny class, implemented at toy scale in A009.
  <https://www.numdam.org/item/10.5802/aif.2430.pdf>
- [CITED] Jeffrey C. Lagarias and Andrew M. Odlyzko, "Solving Low-Density
  Subset Sum Problems," *Journal of the ACM* 32(1), 229--246, 1985, DOI
  10.1145/2455.2461. Relevance: the distributional low-density LLL theorem
  whose regime excludes A010's high-density structured logarithmic instance.
  <https://doi.org/10.1145/2455.2461>
- [CITED] Karl Bringmann, "A Near-Linear Pseudopolynomial Time Algorithm for
  Subset Sum," *SODA 2017*, 1073--1084, DOI
  10.1137/1.9781611974782.69; arXiv:1610.04712. Relevance: the
  $\widetilde O(n+t)$ bound whose numerical-target dependence is exponential
  after A010's required logarithmic rounding.
  <https://arxiv.org/abs/1610.04712>
- [CITED] Markus Hittmeir, "Smooth Subsum Search: A Heuristic for Practical
  Integer Factorization," arXiv:2301.10529, 2023. Relevance: a practical
  smooth-value method whose explicitly heuristic, factoring-specific scope
  does not give a worst-case short-interval finder.
  <https://arxiv.org/abs/2301.10529>

Entries are added only after their bibliographic metadata or text has been
checked against a primary source.

- [CITED] Arjen K. Lenstra, “General purpose integer factoring,” Chapter 5 in
  *Topics in Computational Number Theory Inspired by Peter L. Montgomery*,
  Cambridge University Press; IACR ePrint 2017/1087. Relevance: Section 5.2.2
  gives the generalized L-notation definition used to interpret P1.2's formal
  factor-base bound. <https://eprint.iacr.org/2017/1087.pdf>
- [CITED] Andrew V. Sutherland, “Point Counting,” MIT 18.783 Elliptic Curves,
  Lecture 7 slides, Fall 2025. Relevance: states the Frobenius trace formula
  and Hasse bound used to show $\#E(\mathbb F_p)=p^{1+o(1)}$ in P1.2.
  <https://ocw.mit.edu/courses/18-783-elliptic-curves-fall-2025/mit18_783_f25_lec_s_07.pdf>
- [CITED] Christophe Petit, Michiel Kosters, and Ange Messeng, “Algebraic
  Approaches for the Elliptic Curve Discrete Logarithm Problem over Prime
  Fields,” PKC 2016, LNCS 9615, 3–18,
  doi:10.1007/978-3-662-49387-8_1. Relevance: smooth-subgroup and isogeny
  factor bases whose high-degree root conditions decompose into low-degree
  maps. <https://people.maths.ox.ac.uk/petit/files/16PKC_primeECDLP.pdf>
- [CITED] Alessandro Amadori, Federico Pintore, and Massimiliano Sala, “On the
  Discrete Logarithm Problem for Prime-Field Elliptic Curves,” *Finite Fields
  and Their Applications* 51, 168–182, 2018,
  doi:10.1016/j.ffa.2018.01.009; IACR ePrint 2017/609. Relevance: a one-system
  prime-field summation-polynomial variant and an explicit statement that its
  system-solving complexity remains open. <https://eprint.iacr.org/2017/609.pdf>
- [CITED] Igor Semaev, “Summation polynomials and the discrete logarithm problem on
  elliptic curves,” IACR Cryptology ePrint Archive, Report 2004/031, 2004.
  Relevance: introduces the summation-polynomial construction used to validate
  P1.2 decompositions. <https://eprint.iacr.org/2004/031>
- [CITED] Pierrick Gaudry, “Index calculus for abelian varieties of small dimension
  and the elliptic curve discrete logarithm problem,” *Journal of Symbolic
  Computation* 44(12), 1690–1702, 2009,
  doi:10.1016/j.jsc.2008.08.005. Relevance: applies an algebraic factor base and
  Weil restriction to small-degree extension fields.
  <https://doi.org/10.1016/j.jsc.2008.08.005>
- [CITED] Claus Diem, “On the discrete logarithm problem in elliptic curves,”
  *Compositio Mathematica* 147, 75–104, 2011,
  doi:10.1112/S0010437X10005075. Relevance: gives a proved extension-field
  decomposition algorithm and explains the algebraic factor base.
  <https://doi.org/10.1112/S0010437X10005075>
- [CITED] William C. Waterhouse, “Abelian varieties over finite fields,”
  *Annales scientifiques de l'École Normale Supérieure*, Series 4, 2(4),
  521–560, 1969, doi:10.24033/asens.1183. Relevance: classification used to
  check the ordinary/supersingular trace condition for the sampled curves.
  <https://doi.org/10.24033/asens.1183>
- [CITED] The Stacks Project Authors, *The Stacks Project*, Chapter 53,
  “Algebraic Curves,” Lemma 53.2.2, Proposition 53.13.7, and Lemma 53.12.2.
  Relevance: rational-map extension, inseparable/separable factorization, and
  Riemann–Hurwitz for the Candidate C obstruction.
  <https://stacks.math.columbia.edu/chapter/curves>
- [CITED] Massachusetts Institute of Technology, *Notes for a Course in
  Algebraic Geometry*, 18.721 preliminary draft, 11 December 2021, Sections
  1.10 and 7.8. Relevance: Bézout bound for Candidate C auxiliary curves.
  <https://math.mit.edu/classes/18.721/notes/ag-dec11-2021.pdf>

- Alessio Caminata and Elisa Gorla, “Solving degree, last fall degree, and
  related invariants,” *Journal of Symbolic Computation* 114 (2023), 322–335.
  DOI: 10.1016/j.jsc.2022.05.001; arXiv:2112.05579v2. Rigorous definitions and
  separations among first fall degree, solving degree, and regularity notions.
- [CITED] Alessio Caminata, Michela Ceria, and Elisa Gorla, “The complexity of
  solving Weil restriction systems,” *Journal of Algebra* 621 (2023), 116–133.
  DOI: 10.1016/j.jalgebra.2023.01.008; arXiv:2112.10506. Gives general
  solving-degree bounds for homogeneous and nonhomogeneous Weil restrictions,
  including systems with field equations.
- [CITED] Alessio Caminata and Elisa Gorla, "Solving multivariate polynomial
  systems and an invariant from commutative algebra," *PQCrypto 2021*, LNCS
  12542, 3--36; arXiv:1706.06319v7. Relevance: bounds DRL solving degree by
  homogenized regularity under explicit hypotheses and warns that raw input
  homogenization need not be saturated. <https://arxiv.org/abs/1706.06319>
- [CITED] Flavio Salizzoni, "An upper bound for the solving degree in terms of
  the degree of regularity," arXiv:2304.13485v1, 2023. Relevance: Proposition
  3.10 bounds the closed/mutant solving degree by the maximum of regularity
  plus one and the maximum input degree; this closes the quadratic mutant
  family upper bound. <https://arxiv.org/abs/2304.13485>
- Timothy J. Hodges, Christophe Petit, and Jacob Schlather, “First fall degree
  and Weil descent,” *Finite Fields and Their Applications* 30 (2014),
  155–177. DOI: 10.1016/j.ffa.2014.07.001. Defines first fall degree for
  filtered finite-field function algebras and bounds it after Weil descent.
- Stavros Kousidis and Andreas Wiemers, “On the first fall degree of summation
  polynomials,” *Journal of Mathematical Cryptology* 13(3–4) (2019), 229–237.
  DOI: 10.1515/jmc-2017-0022; arXiv:1906.05594. Proves a first-fall bound for
  binary Weil descents of Semaev polynomials and reports Magma step degrees.
- Christophe Petit and Jean-Jacques Quisquater, “On polynomial systems arising
  from a Weil descent,” *ASIACRYPT 2012*, LNCS 7658, 451–466. DOI:
  10.1007/978-3-642-34961-4_28; IACR ePrint 2012/146. Source of the
  first-fall-based heuristic complexity estimate for the binary ECDLP setting.

- Victor Shoup, "Lower Bounds for Discrete Logarithms and Related Problems,"
  EUROCRYPT 1997, LNCS 1233, pp. 256–266. Defines the random-encoding GGM and
  proves the $O(m^2/r)$ success bound.
- V. I. Nechaev, "Complexity of a Determinate Algorithm for the Discrete
  Logarithm," Mathematical Notes 55(2), 1994, pp. 165–172. Earlier
  group-operation lower bound with free equality.
- Ueli Maurer, "Abstract Models of Computation in Cryptography," Cryptography
  and Coding 2005, LNCS 3796, pp. 1–12. Hidden-state operations-and-relations
  framework.
- Georg Fuchsbauer, Eike Kiltz, and Julian Loss, "The Algebraic Group Model and
  its Applications," CRYPTO 2018, LNCS 10993. Defines the AGM and distinguishes
  it from an information-theoretic lower-bound model.
- Divesh Aggarwal and Ueli Maurer, "Breaking RSA Generically is Equivalent to
  Factoring," EUROCRYPT 2009; full version IACR ePrint 2008/260. Defines the
  generic ring interface used in the model comparison.
- Igor Semaev, "Evaluation of Discrete Logarithms in a Group of $p$-Torsion
  Points of an Elliptic Curve in Characteristic $p$," Mathematics of
  Computation 67(221), 1998, pp. 353–356. One anomalous-curve DLP algorithm.
- Takakazu Satoh and Kiyomichi Araki, "Fermat Quotients and the Polynomial Time
  Discrete Log Algorithm for Anomalous Elliptic Curves," Commentarii
  Mathematici Universitatis Sancti Pauli 47(1), 1998, pp. 81–92. Local-lifting
  anomalous-curve attack.
- Nigel P. Smart, "The Discrete Logarithm Problem on Elliptic Curves of Trace
  One," Journal of Cryptology 12(3), 1999, pp. 193–196. Elementary presentation
  of the anomalous-curve attack.
- Alfred Menezes, Tatsuaki Okamoto, and Scott Vanstone, "Reducing Elliptic Curve
  Logarithms to Logarithms in a Finite Field," IEEE Transactions on Information
  Theory 39(5), 1993, pp. 1639–1646. Pairing transfer underlying MOV.
- Gerhard Frey and Hans-Georg Rück, "A Remark Concerning $m$-Divisibility and
  the Discrete Logarithm in the Divisor Class Group of Curves," Mathematics of
  Computation 62, 1994, pp. 865–874. Tate-pairing transfer.
- [CITED] Pierrick Gaudry, Florian Hess, and Nigel P. Smart, “Constructive and
  Destructive Facets of Weil Descent on Elliptic Curves,” *Journal of
  Cryptology* 15(1), 2002, pp. 19–46,
  doi:10.1007/s00145-001-0011-x. Relevance: defines the GHS fixed field and the
  conorm/norm class-group homomorphism; the verified HPL-2000-10 report and
  original KASH code supply the odd-degree genus-one trace equation used by
  the P1.1 regression. <https://nigelsmart.github.io/weil_descent.html>
- Igor Semaev, "Summation Polynomials and the Discrete Logarithm Problem on
  Elliptic Curves," IACR ePrint 2004/031. Introduces summation-polynomial
  relation generation.
- Pierrick Gaudry, "Index Calculus for Abelian Varieties of Small Dimension and
  the Elliptic Curve Discrete Logarithm Problem," Journal of Symbolic
  Computation 44(12), 2009, pp. 1690–1702. Extension-field decomposition index
  calculus.
- Claus Diem, "On the Discrete Logarithm Problem in Elliptic Curves,"
  Compositio Mathematica 147(1), 2011, pp. 75–104. Rigorous decomposition and
  index-calculus analysis over extension fields.
- [CITED] Marcus Stögbauer, *Efficient Algorithms for Pairing-Based
  Cryptosystems*, diploma thesis, Darmstadt University of Technology,
  Department of Mathematics, 2004, Appendix B, pp. 67–69. Relevance: fixed
  $\mathbb F_{43^2}$ reduced Tate-pairing vector and Miller operation sequence
  used by the P1.1 pairing regression.

- [CITED] Juliana V. Belding, "A Weil pairing on the $p$-torsion of ordinary
  elliptic curves over the dual numbers of $K$," arXiv:math/0703906, 2007.
  Relevance: unifies characteristic-$p$ additive attacks with the pairing
  viewpoint used by MOV. <https://arxiv.org/abs/math/0703906>
- [CITED] James S. Milne, *Algebraic Groups: The Theory of Group Schemes of
  Finite Type over a Field*, version 2.00, 2022. Relevance: anti-affine versus
  affine homomorphisms and the algebraic-group structure theorem used in P1.5.
  <https://www.jmilne.org/math/Books/iAG2022.pdf>
- [CITED] Andreas Enge, Pierrick Gaudry, and Emmanuel Thome, "An $L(1/3)$
  Discrete Logarithm Algorithm for Low Degree Curves," arXiv:0905.2177, 2009.
  Relevance: conditional subexponential target algorithms for selected
  high-genus Jacobian families. <https://arxiv.org/abs/0905.2177>
- [CITED] James L. Hafner and Kevin S. McCurley, "A Rigorous Subexponential
  Algorithm for Computation of Class Groups," *Journal of the American
  Mathematical Society* 2(4), 837--850, 1989,
  doi:10.1090/S0894-0347-1989-1002631-0. Relevance: target-side motivation for
  the P1.5 class-group candidate.
- [CITED] Wouter Castryck, Marc Houben, Frederik Vercauteren, and Benjamin
  Wesolowski, "On the decisional Diffie--Hellman problem for class group
  actions on oriented elliptic curves," *Research in Number Theory* 8,
  article 99, 2022, doi:10.1007/s40993-022-00399-6. Relevance: fixes the
  ideal-to-kernel direction of the CM action used to reject point-annihilator
  labels in P1.5. <https://link.springer.com/article/10.1007/s40993-022-00399-6>
- [CITED] James S. Milne, *Class Field Theory*, version 3.1 course notes,
  1997. Relevance: ray-class exact sequence and order formula plus the
  imaginary-quadratic analytic class-number formula used in P1.5.
  <https://www.jmilne.org/math/CourseNotes/CFT310.pdf>
- [CITED] David A. Cox, *Primes of the Form $x^2+ny^2$: Fermat, Class Field
  Theory, and Complex Multiplication*, second edition, Wiley, 2013.
  Relevance: Theorem 7.24 supplies the ring class-number formula used for the
  P1.5 endomorphism-order bound.
- [CITED] Duncan A. Buell and Gregory S. Call, "Class pairings and isogenies
  on elliptic curves," *Journal of Number Theory* 167, 31--73, 2016,
  doi:10.1016/j.jnt.2016.02.030. Relevance: actual point-to-class
  homomorphisms over number fields and their relation to Weil descent delimit
  the arithmetic specialization branch of P1.5.
  <https://www.sciencedirect.com/science/article/pii/S0022314X16300464>
- [CITED] Duncan A. Buell, "Elliptic Curves and Class Groups of Quadratic
  Fields," *Journal of the London Mathematical Society* s2-15(1), 19--25,
  1977, doi:10.1112/jlms/s2-15.1.19. Relevance: original rational
  point-to-quadratic-class construction audited in P1.5.
  <https://academic.oup.com/jlms/article-abstract/s2-15/1/19/810895>
- [CITED] Ragnar Soleng, "Homomorphisms from the Group of Rational Points on
  Elliptic Curves to Class Groups of Quadratic Number Fields," *Journal of
  Number Theory* 46(2), 214--229, 1994,
  doi:10.1006/jnth.1994.1013. Relevance: characteristic-zero point-to-class
  morphisms compared with specialization pairings in P1.5.
- [CITED] Jean Gillibert, "From Picard groups of hyperelliptic curves to class
  groups of quadratic fields," arXiv:1807.02823, 2018. Relevance: identifies
  Buell--Soleng maps with line-bundle specialization and makes the global
  number-field source explicit. <https://arxiv.org/abs/1807.02823>
- [CITED] Talia Blum, Caroline Choi, Alexandra Hoey, Jonas Iskander, Kaya
  Lakein, and Thomas C. Martinez, "On Class Numbers, Torsion Subgroups, and
  Quadratic Twists of Elliptic Curves," *Transactions of the American
  Mathematical Society* 375, 351--368, 2022, doi:10.1090/tran/8457;
  arXiv:2007.08756. Relevance: explicit
  $E(\mathbb Q)\to\operatorname{Cl}(-D)$ maps checked against the finite-field
  residual in P1.5. <https://arxiv.org/abs/2007.08756>
- [CITED] Meng Fai Lim, "On the Divisibility of Class Numbers and
  Discriminants of Imaginary Quadratic Fields," arXiv:1601.05180, 2016.
  Relevance: exact prescribed-order existence theorem audited against P1.5's
  succinct target requirement. <https://arxiv.org/abs/1601.05180>
- [CITED] Yi Ouyang and Qimin Song, "Divisibility of Class Numbers of
  Quadratic Fields and a Conjecture of Iizuka," arXiv:2406.05975, 2024.
  Relevance: $x^2-y^n$ class-number divisibility family whose fixed-parameter
  ineffective threshold does not give a uniform P1.5 target constructor.
  <https://arxiv.org/abs/2406.05975>
- [CITED] Kalyan Chakraborty and Azizul Hoque, "Exponent of Class Group of
  Certain Imaginary Quadratic Fields," *Czechoslovak Mathematical Journal*
  70(4), 1167--1178, 2020, doi:10.21136/CMJ.2020.0289-19;
  arXiv:1801.00392. Relevance: prescribed exact-order
  families of shape $\mathbb Q(\sqrt{x^2-2y^n})$ checked in the P1.5 target
  audit. <https://arxiv.org/abs/1801.00392>
- [CITED] Pierre Parent, "Bornes effectives pour la torsion des courbes
  elliptiques sur les corps de nombres," *Journal fuer die reine und
  angewandte Mathematik* 506, 85--116, 1999,
  doi:10.1515/crll.1999.506.85. Relevance: explicit polynomial-in-degree
  prime-power torsion bound used to exclude standard global lift packages in
  P1.5. <https://www.degruyter.com/document/doi/10.1515/crll.1999.506.85/html>
- [CITED] Bjorn Poonen, *Introduction to Drinfeld Modules*, notes dated
  December 29, 2021. Relevance: defines a Drinfeld module on the underlying
  additive group scheme $\mathbb G_a$.
  <https://math.mit.edu/~poonen/papers/drinfeld.pdf>
- [CITED] Victor Shoup, "Lower Bounds for Discrete Logarithms and Related
  Problems," EUROCRYPT 1997, LNCS 1233, 256--266,
  doi:10.1007/3-540-69053-0_18. Relevance: random-injective-encoding generic
  group bound used to exclude every P1.5 transfer with only generic source
  access. <https://www.shoup.net/papers/dlbounds1.pdf>
- [CITED] Victor S. Miller, "Short Programs for Functions on Curves: A STOC
  Rejection," *12th International Conference on Fun with Algorithms*, LIPIcs
  291, 34:1--34:4, 2024, doi:10.4230/LIPIcs.FUN.2024.34. Relevance: makes the
  compact-straight-line-program versus exponential expanded-degree distinction
  used in P1.5's rational-circuit depth bound.
  <https://doi.org/10.4230/LIPIcs.FUN.2024.34>
- [CITED] James S. Milne, *Abelian Varieties*, course notes, version 2.00,
  2008. Relevance: Corollary 1.2 makes every zero-preserving morphism of
  abelian varieties a homomorphism, closing P1.5's single rational
  proper-target branch. <https://www.jmilne.org/math/CourseNotes/AV110.pdf>
- [CITED] The Stacks Project Authors, Section 53.2, "Curves and function
  fields," Lemma 53.2.2. Relevance: extends a rational map from the normal
  curve $E$ to a proper P1.5 target across every missing point.
  <https://stacks.math.columbia.edu/tag/0BXX>
- [CITED] James S. Milne, *Jacobian Varieties*, online notes. Relevance:
  identifies pointed-curve degree-zero Picard groups with Jacobian rational
  points and modulus class groups with generalized Jacobians, closing P1.5's
  global-function-field class-target branch.
  <https://www.jmilne.org/math/xnotes/JVs.pdf>
- [CITED] Brian Conrad, “A Modern Proof of Chevalley's Theorem on Algebraic
  Groups,” 2002. Relevance: gives the perfect-field affine-kernel/abelian
  quotient used in P1.5's audited mixed-target theorem.
  <https://math.stanford.edu/~conrad/papers/chev.pdf>
- [CITED] Stéphane Fischler and Michael Nakamaye, “Seshadri Constants and
  Interpolation on Commutative Algebraic Groups,” *Annales de l'Institut
  Fourier* 64(3), 1269--1289, 2014, doi:10.5802/aif.2880. Relevance: closest
  checked general interpolation/obstruction-subgroup prior art for P1.5's
  finite-subgroup zero-count results; it does not state the same
  homomorphism-defect or branch tradeoff theorem.
  <https://arxiv.org/abs/1205.4088>
- [CITED] The Stacks Project Authors, Section 15.119, "Picard groups of
  rings," and Lemma 10.153.10. Relevance: invertible-module definition and
  finite-product local decomposition used to prove that every finite/local
  P1.5 class target is trivial. <https://stacks.math.columbia.edu/tag/0AFW>
- [CITED] Don Coppersmith and Igor E. Shparlinski, "On Polynomial
  Approximation of the Discrete Logarithm and the Diffie--Hellman Mapping,"
  *Journal of Cryptology* 13(3), 339--360, 2000,
  doi:10.1007/s001450010002. Relevance: closest quantitative predecessor for
  P1.5's arbitrary-subset overlap bound; Theorem 1 already gives a quadratic
  subset-over-ambient-size degree obstruction for the scalar discrete-log
  function. <https://doi.org/10.1007/s001450010002>
- [CITED] Tanja Lange and Arne Winterhof, "Polynomial Interpolation of the
  Elliptic Curve and XTR Discrete Logarithm," COCOON 2002, LNCS 2387,
  137--143, doi:10.1007/3-540-45655-4_16. Relevance: elliptic-coordinate
  scalar interpolation on dense exponent intervals and arbitrary-subset XTR
  bounds reconciled in P1.5/A023.
  <https://doi.org/10.1007/3-540-45655-4_16>
- [CITED] Eike Kiltz and Arne Winterhof, "Polynomial Interpolation of
  Cryptographic Functions Related to Diffie--Hellman and Discrete Logarithm
  Problem," *Discrete Applied Mathematics* 154(2), 326--336, 2006,
  doi:10.1016/j.dam.2005.03.030. Relevance: finite-field transformed-function
  reductions and interpolation bounds checked against the P1.5 theorem
  package. <https://doi.org/10.1016/j.dam.2005.03.030>
- [CITED] Arne Winterhof, "Polynomial Interpolation of the Discrete
  Logarithm," *Designs, Codes and Cryptography* 25(1), 63--72, 2002,
  doi:10.1023/A:1012556500517. Relevance: extends the prime-field
  interpolation line to arbitrary finite fields. The requested
  Meidl--Winterhof attribution was corrected in P1.5/A023.
  <https://doi.org/10.1023/A:1012556500517>
- [CITED] Wilfried Meidl and Arne Winterhof, "A Polynomial Representation of
  the Diffie--Hellman Mapping," *Applicable Algebra in Engineering,
  Communication and Computing* 13(4), 313--318, 2002,
  doi:10.1007/s00200-002-0104-2. Relevance: the distinct Meidl--Winterhof
  paper separated from Winterhof's discrete-logarithm article during the
  P1.5 bibliographic reconciliation.
  <https://doi.org/10.1007/s00200-002-0104-2>
- [CITED] Eric R. Verheul, "Evidence that XTR Is More Secure than
  Supersingular Elliptic Curve Cryptosystems," EUROCRYPT 2001, LNCS 2045,
  195--210; full version, *Journal of Cryptology* 17(4), 277--296, 2004,
  doi:10.1007/s00145-004-0313-x. Relevance: efficient reverse homomorphisms
  imply an efficient Diffie--Hellman algorithm in the paired XTR setting, a
  predecessor of P1.5/SG-23's consequence strategy.
  <https://www.cs.ru.nl/E.Verheul/papers/Joc2004/joc2004.pdf>
- [CITED] Dustin Moody, "The Diffie--Hellman Problem and Generalization of
  Verheul's Theorem," IACR ePrint 2008/456; *Designs, Codes and Cryptography*
  52(3), 381--390, 2009. Relevance: generalizes the reverse-homomorphism
  consequence using computable pairings and distortion maps and supplies the
  template checked before P1.5/SG-32. <https://eprint.iacr.org/2008/456>
- [CITED] Neal Koblitz and Alfred Menezes, "Another Look at Generic Groups,"
  *Advances in Mathematics of Communications* 1(1), 13--28, 2007,
  doi:10.3934/amc.2007.1.13; IACR ePrint 2006/230. Relevance: conceptual
  predecessor for P1.5/SG-14's distinction between generic handles and
  concrete coordinate/implementation features.
  <https://eprint.iacr.org/2006/230>

## P2.2 — q-type assumptions

- [CITED] Jean-Sébastien Coron, “Optimal Security Proofs for PSS and Other
  Signature Schemes,” EUROCRYPT 2002, LNCS 2332, 272–287,
  doi:10.1007/3-540-46035-7_18. Relevance: early meta-reduction technique for
  proving optimality limits on signature reductions; not a $q$-SDH separation.
  <https://www.iacr.org/archive/eurocrypt2002/23320268/coron.pdf>
- [CITED] Dan Boneh, Craig Gentry, Ben Lynn, and Hovav Shacham, “Aggregate and
  Verifiably Encrypted Signatures from Bilinear Maps,” EUROCRYPT 2003,
  LNCS 2656, 416–432. Relevance: exact computational co-Diffie–Hellman
  experiment for asymmetric source groups.
  <https://crypto.stanford.edu/~dabo/pubs/papers/aggreg.pdf>
- [CITED] Dan Boneh and Xavier Boyen, “Efficient Selective-ID Secure
  Identity-Based Encryption Without Random Oracles,” EUROCRYPT 2004,
  LNCS 3027, 223–238. Relevance: original computational and decisional
  $q$-BDHI definitions and their relation to BDH.
  <https://www.iacr.org/cryptodb/archive/2004/EUROCRYPT/1950/1950.pdf>
- [CITED] Dan Boneh, Xavier Boyen, and Hovav Shacham, “Short Group
  Signatures,” CRYPTO 2004, LNCS 3152, 41–55. Relevance: introduces the
  Decision Linear assumption and gives its exact experiment.
  <https://crypto.stanford.edu/~dabo/pubs/papers/groupsigs.pdf>
- [CITED] Steven D. Galbraith, Kenneth G. Paterson, and Nigel P. Smart,
  “Pairings for Cryptographers,” *Discrete Applied Mathematics* 156(16),
  3113–3121, 2008; IACR ePrint 2006/165. Relevance: typed pairing-group
  classification and the absence of efficient cross-source maps in Type 3.
  <https://eprint.iacr.org/2006/165.pdf>
- [CITED] Dan Boneh and Xavier Boyen, “Short Signatures Without Random Oracles
  and the SDH Assumption in Bilinear Groups,” *Journal of Cryptology* 21(2),
  149–177, 2008, doi:10.1007/s00145-007-9005-7. Relevance: inverse-form
  $q$-SDH, random self-reduction, $q$-aBDH implication, and the original
  signature reduction. <https://crypto.stanford.edu/~dabo/pubs/papers/bbsigs.pdf>
- [CITED] Dan Boneh, Xavier Boyen, and Eu-Jin Goh, “Hierarchical Identity Based
  Encryption with Constant Size Ciphertext,” EUROCRYPT 2005, LNCS 3494,
  440–456. Relevance: exact $q$-BDHI, $q$-wBDHI, and $q$-wBDHI$^*$ variants and
  their tight reductions. <https://crypto.stanford.edu/~dabo/papers/shibe.pdf>
- [CITED] Jung Hee Cheon, “Security Analysis of the Strong Diffie-Hellman
  Problem,” EUROCRYPT 2006, LNCS 4004, 1–11,
  doi:10.1007/11761679_1. Relevance: divisor-dependent recovery attacks from a
  supplied power ladder.
  <https://www.math.snu.ac.kr/~jhcheon/publications/2006/Eurocrypt_Cheon_LNCS.pdf>
- [CITED] Melissa Chase and Sarah Meiklejohn, “Déjà Q: Using Dual Systems to
  Revisit q-Type Assumptions,” EUROCRYPT 2014, LNCS 8441, 622–639,
  doi:10.1007/978-3-642-55220-5_34. Relevance: positive generic reduction of
  computational $q$-SDH and related assumptions to static subgroup hiding in
  composite-order bilinear groups. <https://eprint.iacr.org/2014/570.pdf>
- [CITED] Melissa Chase, Mary Maller, and Sarah Meiklejohn, “Déjà Q All Over
  Again: Tighter and Broader Reductions of q-Type Assumptions,” ASIACRYPT 2016
  Part II, LNCS 10032, 655–681, doi:10.1007/978-3-662-53890-6_22. Relevance:
  broader composite-order framework and logarithmic-in-$q$ tightness.
  <https://eprint.iacr.org/2016/840.pdf>
- [CITED] George Lu and Mark Zhandry, “Limits on the Power of Prime-Order
  Groups: Separating Q-Type from Static Assumptions,” CRYPTO 2024 Part V,
  LNCS 14924, 46–74; IACR ePrint 2024/993. Relevance: fully black-box generic
  separation for prime-order $q$-type assumptions, explicitly including
  $q$-SDH. <https://eprint.iacr.org/2024/993.pdf>
- [CITED] Omer Reingold, Luca Trevisan, and Salil Vadhan, “Notions of
  Reducibility between Cryptographic Primitives,” TCC 2004, LNCS 2951, 1–20,
  doi:10.1007/978-3-540-24638-1_1. Relevance: formal taxonomy separating
  fully-, semi-, weakly-, and non-black-box reductions; its fully-black-box
  definition fixes an oracle security transformer for every breaking
  adversary. <https://lucatrevisan.github.io/pubs/rtv04.pdf>
- [CITED] Mark Zhandry, “To Label, or Not To Label (in Generic Groups),”
  CRYPTO 2022; IACR ePrint 2022/226. Relevance: separates random-representation
  and type-safe generic groups, fixes the query-cost convention, and rules out
  internal type-safe PRPs under unbounded bit computation.
  <https://eprint.iacr.org/2022/226.pdf>
- [CITED] Taiyu Wang, Cong Zhang, Hong-Sheng Zhou, Xin Wang, Pengfei Chen,
  Wenli Wang, Kui Ren, and Chun Chen, “Attention is still what you need:
  Another Round of Exploring Shoup's GGM,” ASIACRYPT 2025; IACR ePrint
  2025/1930. Relevance: black-box separations between sparse GGM and
  admissibly encoded, dense, EC-generic, and bilinear group settings.
  <https://eprint.iacr.org/2025/1930>
- [CITED] Henry Corrigan-Gibbs, Alexandra Henzinger, and David J. Wu, “The
  Structured Generic-Group Model,” EUROCRYPT 2026; IACR ePrint 2026/384.
  Relevance: formalizes free partial structure on labels and proves a
  density-sensitive discrete-log lower bound; A007 audits why its density
  parameter does not itself bound native-label trace dimension.
  <https://www.cs.utexas.edu/~dwu4/papers/SGGM.pdf>
- [CITED] Tsz Hon Yuen, Sherman S. M. Chow, Huangting Wu, Cong Zhang, and
  Siu-Ming Yiu, “Exponent-Inversion P-Signatures and Accountable Identity-Based
  Encryption from SXDH,” *IACR Communications in Cryptology* 1(3), article 48,
  2024, doi:10.62056/ahsdkmp-3y. Relevance: prime-order static-assumption
  security for modified dual-form exponent-inversion schemes, not for the
  $q$-SDH assumption itself. <https://cic.iacr.org/p/1/3/48>
- [CITED] Rutchathon Chairattana-Apirom and Stefano Tessaro, “On the Concrete
  Security of BBS/BBS+ Signatures,” ASIACRYPT 2025; IACR ePrint 2025/1093.
  Relevance: attacks matching the usage-dependent $\Theta(q)$-DL scale and a
  reverse reduction from scheme security to $\Theta(q)$-SDH.
  <https://eprint.iacr.org/2025/1093>
- [CITED] Rutchathon Chairattana-Apirom, Dennis Hofheinz, and Stefano Tessaro,
  “Tight Security for BBS Signatures,” EUROCRYPT 2026; IACR ePrint 2025/1973,
  revised 2026-02-20. Relevance: a tight $q$-SDH proof for one-signature-per-
  message BBS and an algebraic meta-reduction against tightness with repeated
  messages; it retains the $q$-type premise. <https://eprint.iacr.org/2025/1973>

## P2.4 verified references

- [CITED] Victor Shoup, “Lower Bounds for Discrete Logarithms and Related Problems,” EUROCRYPT 1997, LNCS 1233, 256–266. Relevance: random-encoding generic-group method and the collision bound specialized in A002. <https://link.springer.com/chapter/10.1007/3-540-69053-0_18>
- [CITED] Ueli Maurer, “Abstract Models of Computation in Cryptography,” *Cryptography and Coding 2005*, LNCS 3796, 1–12. Relevance: hidden-state affine-expression collision argument and typed-operation interpretation. <https://crypto.ethz.ch/publications/files/Maurer05.pdf>
- [CITED] Mark Zhandry, “To Label, or Not To Label (in Generic Groups),” CRYPTO 2022, LNCS 13509, 66–96, doi:10.1007/978-3-031-15982-4_3. Relevance: distinguishes RR/Shoup from TS/Maurer and proves their security equivalence for applicable single-stage games. <https://crypto.iacr.org/2022/papers/538805_1_En_3_Chapter_OnlinePDF.pdf>
- [CITED] Steven D. Galbraith, Florian Hess, and Frederik Vercauteren, “Aspects of Pairing Inversion,” *IEEE Transactions on Information Theory* 54(12), 5719–5728, 2008, doi:10.1109/TIT.2008.2006431; IACR ePrint 2007/256. Relevance: defines FAPI and MI, proves the BDH/CDH and homomorphism consequences, and analyzes the final-exponentiation/MI interface. <https://eprint.iacr.org/2007/256>
- [CITED] Takakazu Satoh, “Miller Inversion is Easy for the Reduced Tate Pairing of Embedding Degree Greater than one,” IACR ePrint 2019/385, revised January 2025. Relevance: polynomial-time MI for the fixed-extension/variable-base orientation and an explicit demonstration that FEI must supply the correct raw representative. <https://eprint.iacr.org/2019/385>
- [CITED] Marcus Stögbauer, “Efficient Algorithms for Pairing-Based Cryptosystems,” diploma thesis, Technische Universität Darmstadt, 2004. Relevance: Appendix B supplies the \(p=43,r=11\) staged validation vector used by `lib/tests/test_pairing.py`. <https://citeseerx.ist.psu.edu/document?doi=cd3be12257d063b3c444d424ec5806ffd87f1cd3&repid=rep1&type=pdf>
- [CITED] Triantafyllos Xylouris, “On the least prime in an arithmetic progression and estimates for the zeros of Dirichlet L-functions,” *Acta Arithmetica* 150(1), 65–91, 2011. Relevance: Linnik's theorem may supply polynomial-bit-size congruence primes when auditing an elliptic-curve realization of A002. <https://eudml.org/doc/279129>

## P1.4 verified references

- [CITED] Pierrick Gaudry, Florian Hess, and Nigel P. Smart, “Constructive and Destructive Facets of Weil Descent on Elliptic Curves,” *Journal of Cryptology* 15(1), 19–46, 2002, doi:10.1007/s00145-001-0011-x. Relevance: defines the basic binary GHS magic number and construction.
- [CITED] Florian Hess, “The GHS Attack Revisited,” *EUROCRYPT 2003*, LNCS 2656, 374–387, doi:10.1007/3-540-39200-9_23. Relevance: supplies the exact genus formula used to resolve the two possible GHS genera.
- [CITED] Markus Maurer, Alfred Menezes, and Edlyn Teske, “Analysis of the GHS Weil Descent Attack on the ECDLP over Characteristic Two Finite Fields of Composite Degree,” *LMS Journal of Computation and Mathematics* 5, 127–174, 2002, doi:10.1112/S1461157000000723. Relevance: analyzes Frobenius types, density, and the cost conditions beyond genus.
- [CITED] Computational Algebra Group, Magma V2.19.8 online handbook, “Weil Descent,” example H42E45. Relevance: published genus-31 regression over $\mathbb F_{2^{155}}/\mathbb F_{2^5}$. <https://www.math.uzh.ch/sepp/magma-2.19.8-cr/html/text441.htm>

## P5.1 — Koblitz's conjecture

- [CITED] Neal Koblitz, “Primality of the number of points on an elliptic curve over a finite field,” *Pacific Journal of Mathematics* 131(1), 157–165, 1988. Relevance: original prime-order conjecture, local product, CM distinction, and numerical tables. <https://msp.org/pjm/1988/131-1/pjm-v131-n1-p09-s.pdf>
- [CITED] David Zywina, “A refinement of Koblitz's conjecture,” *International Journal of Number Theory* 7(3), 739–769, 2011; arXiv:0909.5280. Relevance: corrected adelic constant, explicit Serre-curve value, refined finite-cutoff predictor, and survey of partial results. <https://pi.math.cornell.edu/~zywina/papers/KoblitzConj.pdf>
- [CITED] Chantal David and Jie Wu, “Almost prime values of the order of elliptic curves over finite fields,” *Forum Mathematicum* 24(1), 99–119, 2012; arXiv:0812.2860. Relevance: locates the zero-free/GRH input in effective Chebotarev and quantifies the resulting sieve level, almost-prime count, and prime-order upper bound. <https://arxiv.org/abs/0812.2860>
- [CITED] LMFDB Collaboration, elliptic-curve records 1728.w1, 112.b4, and 540.f2, accessed 2026-06-29. Relevance: independent q-expansion point-count fixtures, torsion and CM status, and the level-30 adelic-image generators used for the exact 540.f2 quotient-constant certificate. <https://www.lmfdb.org/EllipticCurve/Q/540/f/2>
- [CITED] Joseph H. Silverman, *The Arithmetic of Elliptic Curves*, second edition, Graduate Texts in Mathematics 106, Springer, 2009. Relevance: CM endomorphisms and integrality of CM $j$-invariants used to certify the hand-constructed torsion examples as non-CM.
- [CITED] P. G. Walsh, "A note on the trace of Frobenius for curves of the form $y^2=x^3+dx$," *Annales Mathematicae et Informaticae* 55, 184--188, 2022, DOI 10.33039/ami.2022.11.003. Relevance: exact $j=1728$ trace formula and quartic-residue sign convention used for the complete Zywina Table 3 reproduction. <https://doi.org/10.33039/ami.2022.11.003>
- [CITED] Sampa Dey, Arnab Saha, Jyothsnaa Sivaraman, and Akshaa Vatwani, "On the refined Koblitz conjecture," *Journal of Mathematical Analysis and Applications* 546(1), article 129212, 2025, DOI 10.1016/j.jmaa.2024.129212. Relevance: obtains the refined fixed-curve constant conditionally on an elliptic Elliott--Halberstam conjecture and a separate average-growth conjecture. <https://doi.org/10.1016/j.jmaa.2024.129212>
- [CITED] Sung Min Lee, Jacob Mayle, and Tian Wang, "Opposing average congruence class biases in the cyclicity and Koblitz conjectures for elliptic curves," *Canadian Journal of Mathematics*, published online 2025, DOI 10.4153/S0008414X25101156; arXiv:2408.16641. Relevance: current primary statement that the fixed-curve conjecture remains open and unconditional moment results over curve families. <https://arxiv.org/abs/2408.16641>
- [CITED] Likun Xie, "Almost Prime Orders of Elliptic Curves Over Prime Power Fields," arXiv:2504.18732, 2025. Relevance: unconditional CM bounded-almost-prime progress and GRH-conditional non-CM analogues, without a fixed-curve prime-order asymptotic. <https://arxiv.org/abs/2504.18732>

## P3.4 — torsion-leakage criterion

- [CITED] Wouter Castryck and Thomas Decru, "An Efficient Key Recovery Attack
  on SIDH," EUROCRYPT 2023, Part V, LNCS 14008, pp. 423--447; IACR ePrint
  2022/975. Relevance: dimension-2 Kani reducibility attack, exact auxiliary
  isogeny requirement, search-to-decision reduction, and SIKE timings.
  <https://eprint.iacr.org/2022/975.pdf>
- [CITED] Luciano Maino and Chloe Martindale, "An Attack on SIDH with Arbitrary
  Starting Curve," EUROCRYPT 2023, Part V, LNCS 14008, pp. 448--471; IACR
  ePrint 2022/1026. Relevance: direct surface attack, SSI-T definition, and
  smooth-cofactor/parameter-tweak witness without a special starting curve.
  <https://eprint.iacr.org/2022/1026.pdf>
- [CITED] Damien Robert, "Breaking SIDH in Polynomial Time," EUROCRYPT 2023,
  Part V, LNCS 14008, pp. 472--503; IACR ePrint 2022/1038, revision dated
  2024-10-07. Relevance: dimension-8 recovery theorem, four-square
  precomputation, $N^2>d$ direct-recovery boundary, and smoothness cost.
  <https://eprint.iacr.org/2022/1038.pdf>
- [CITED] Ernst Kani, "The Number of Curves of Genus Two with Elliptic
  Differentials," *Journal für die reine und angewandte Mathematik* 485
  (1997), pp. 93--122, doi:10.1515/crll.1997.485.93. Relevance: Theorem 2.6 is
  the reducibility criterion used by the surface attacks.
  <https://mast.queensu.ca/~kani/papers/numgenl.pdf>
- [CITED] Wouter Castryck, Tanja Lange, Chloe Martindale, Lorenz Panny, and
  Joost Renes, "CSIDH: An Efficient Post-Quantum Commutative Group Action,"
  ASIACRYPT 2018, LNCS 11274, pp. 395--427; IACR ePrint 2018/383. Relevance:
  CSIDH publishes a curve-class representative and explicitly sends no extra
  torsion points. <https://joostrenes.nl/publications/csidh.pdf>
- [CITED] SIKE team, *Supersingular Isogeny Key Encapsulation*, NIST Round-4
  submission specification, 2022-09-15. Relevance: exact SIDH/SIKE public-key
  encoding, torsion images, compression, and postscript recording the break.
  <https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/round-4/submissions/SIKE-spec.pdf>
- [CITED] SQIsign team, *SQIsign: Algorithm Specifications and Supporting
  Documentation*, version 2.0.1, 2025-07-07. Relevance: public/secret key split,
  response interpolation data, constructive abelian-surface use, and explicit
  separation from SIDH's hardness problem.
  <https://sqisign.org/spec/sqisign-20250707.pdf>
- [CITED] Andrea Basso, Pierrick Dartois, Luca De Feo, Antonin Leroux, Luciano
  Maino, Giacomo Pope, Damien Robert, and Benjamin Wesolowski,
  "SQIsign2D-West: The Fast, the Small, and the Safer," IACR ePrint 2024/760.
  Relevance: constructive use of SIDH attack machinery to represent response
  isogenies while retaining long-term torsion evaluations as secret data.
  <https://eprint.iacr.org/2024/760.pdf>

## P3.1 - supersingular path/endomorphism-ring equivalence

- [CITED] Benjamin Wesolowski, “The supersingular isogeny path and
  endomorphism ring problems are equivalent,” *62nd IEEE Symposium on
  Foundations of Computer Science (FOCS 2021)*, 1100--1111, published 2022;
  arXiv:2111.01481. Relevance: the audited GRH-conditional smooth-path
  equivalence. <https://arxiv.org/abs/2111.01481>
- [CITED] Arthur Herlédan Le Merdy and Benjamin Wesolowski, “Unconditional
  foundations for supersingular isogeny-based cryptography,” TCC 2025,
  266--297; arXiv:2502.17010v2, 2026. Relevance: unconditional unrestricted
  `Isogeny` equivalence and explicit exclusion of $\ell$-`IsogenyPath` from that
  result. <https://arxiv.org/abs/2502.17010>
- [CITED] Kirsten Eisenträger, Sean Hallgren, Kristin E. Lauter, Travis
  Morrison, and Christophe Petit, “Supersingular isogeny graphs and
  endomorphism rings: reductions and solutions,” EUROCRYPT 2018 Part III,
  LNCS 10822, 329--368. Relevance: special quaternion model/curve and the
  original heuristic reductions.
  <https://www.iacr.org/archive/eurocrypt2018/10822193/10822193.pdf>
- [CITED] Edgar Assing, Valentin Blomer, and Junxian Li, “Uniform Titchmarsh
  divisor problems,” arXiv:2005.13915, 2020. Relevance: exact unconditional
  polylog-modulus range and GRH-conditional power-modulus range used by
  Wesolowski's Theorem 4.4. <https://arxiv.org/abs/2005.13915>
- [CITED] David Jao, Stephen D. Miller, and Ramarathnam Venkatesan, “Expander
  graphs based on GRH with an application to elliptic curve cryptography,”
  *Journal of Number Theory* 129(6), 1491--1504, 2009; arXiv:0811.0647.
  Relevance: polylogarithmic prime-ideal Cayley expansion used in Lemmas
  5.3--5.4. <https://arxiv.org/abs/0811.0647>
- [CITED] Jesse Thorner and Asif Zaman, “An explicit bound for the least prime
  ideal in the Chebotarev density theorem,” *Algebra & Number Theory* 11(5),
  1135--1197, 2017; arXiv:1604.01750. Relevance: unconditional fixed-power
  Chebotarev and $|D|^{694}$ fixed-form least-prime bounds.
  <https://arxiv.org/abs/1604.01750>
- [CITED] Naser T. Sardari, “The least prime number represented by a binary
  quadratic form,” arXiv:1803.03218v2, 2019. Relevance: unconditional
  average-over-form-class coverage, a candidate input for SG-02b.
  <https://arxiv.org/abs/1803.03218>
- [CITED] Jakob J. Ditchen, "On the Average Distribution of Primes Represented
  by Binary Quadratic Forms," arXiv:1312.1502v1, manuscript dated 2018.
  Relevance: unconditional averages over discriminants and binary form classes;
  A002 records why their probability space does not match Brandt mixing.
  <https://arxiv.org/abs/1312.1502>
- [CITED] Jeremy Rouse, "Integers Represented by Positive-Definite Quadratic
  Forms and Petersson Inner Products," arXiv:1802.03437v1, 2018. Relevance:
  effective strong-local representation-number bounds for arbitrary quaternary
  forms, the main analytic input to A003.
  <https://arxiv.org/abs/1802.03437>
- [CITED] Jeremy Rouse and Katherine Thompson, "Quaternary Quadratic Forms
  with Prime Discriminant," arXiv:2206.00412v1, 2022. Relevance: explicit
  quaternary bounds checked but not directly applicable to discriminant-
  \(p^2\) quaternion ideal norm forms.
  <https://arxiv.org/abs/2206.00412>
- [CITED] Eyal Z. Goren and Jonathan R. Love, "On Elements of Prescribed Norm
  in Maximal Orders of a Quaternion Algebra," *Canadian Journal of
  Mathematics* 77(6), 1938--1965, 2025; arXiv:2307.16828. Relevance: level-
  \(p\) theta series and local similarity of quaternion ideal lattices.
  <https://arxiv.org/abs/2307.16828>
- [CITED] Michael A. Bennett, Greg Martin, Kevin O'Bryant, and Andrew
  Rechnitzer, "Explicit Bounds for Primes in Arithmetic Progressions,"
  *Illinois Journal of Mathematics* 62(1--4), 427--532, 2018;
  arXiv:1802.00085v3. Relevance: effective progression-prime density at
  \(\log X=\operatorname{poly}(\ell)\) in A003.
  <https://arxiv.org/abs/1802.00085>
- [CITED] Ravi Kannan, "Minkowski's Convex Body Theorem and Integer
  Programming," *Mathematics of Operations Research* 12(3), 415--440, 1987.
  Relevance: polynomial-time closest-vector computation in fixed rank for the
  rank-four Voronoi sampler in A003.
  <https://doi.org/10.1287/moor.12.3.415>

## P3.2 — class-group quantum constant

- [CITED] Andrew M. Childs, David Jao, and Vladimir Soukharev, “Constructing Elliptic Curve Isogenies in Quantum Subexponential Time,” *Journal of Mathematical Cryptology* 8(1) (2014), 1–29, DOI 10.1515/jmc-2012-0016; arXiv:1012.4019. Relevance: hidden-shift reduction and ideal-action evaluation under GRH. <https://arxiv.org/abs/1012.4019>
- [CITED] Greg Kuperberg, “A Subexponential-Time Quantum Algorithm for the Dihedral Hidden Subgroup Problem,” *SIAM Journal on Computing* 35 (2005), 170–188; arXiv:quant-ph/0302112. Relevance: original subexponential hidden-shift sieve. <https://arxiv.org/abs/quant-ph/0302112>
- [CITED] Oded Regev, “A Subexponential Time Algorithm for the Dihedral Hidden Subgroup Problem with Polynomial Space,” *Algorithmica* 47 (2007), 29–39; arXiv:quant-ph/0406151. Relevance: polynomial-space tradeoff. <https://arxiv.org/abs/quant-ph/0406151>
- [CITED] Greg Kuperberg, “Another Subexponential-Time Quantum Algorithm for the Dihedral Hidden Subgroup Problem,” TQC 2013, LIPIcs 22, 20–34, DOI 10.4230/LIPIcs.TQC.2013.20. Relevance: collimation sieve and QRACM tradeoffs. <https://doi.org/10.4230/LIPIcs.TQC.2013.20>
- [CITED] Daniel J. Bernstein, Tanja Lange, Chloe Martindale, and Lorenz Panny, “Quantum Circuits for the CSIDH: Optimizing Quantum Evaluation of Isogenies,” EUROCRYPT 2019, 409–441, DOI 10.1007/978-3-030-17656-3_15; IACR ePrint 2018/1059. Relevance: concrete oracle-operation and memory accounting. <https://eprint.iacr.org/2018/1059.pdf>
- [CITED] Xavier Bonnetain and André Schrottenloher, “Quantum Security Analysis of CSIDH,” EUROCRYPT 2020, Part II, 493–522, DOI 10.1007/978-3-030-45724-2_17; IACR ePrint 2018/537. Relevance: hidden-shift tradeoffs and the (2^{71.6}) CSIDH-512 logical T-gate row. <https://eprint.iacr.org/2018/537.pdf>
- [CITED] Chris Peikert, “He Gives C-Sieves on the CSIDH,” EUROCRYPT 2020, Part II, 463–492, DOI 10.1007/978-3-030-45724-2_16; IACR ePrint 2019/725. Relevance: simulated collimation-sieve tradeoffs through the CSIDH-512 order. <https://eprint.iacr.org/2019/725.pdf>
- [CITED] Dave Bacon, Andrew M. Childs, and Wim van Dam, “Optimal Measurements for the Dihedral Hidden Subgroup Problem,” *Chicago Journal of Theoretical Computer Science* 2006(2), DOI 10.4086/cjtcs.2006.002. Relevance: logarithmic hidden-subgroup-state lower-bound threshold. <https://arxiv.org/abs/quant-ph/0501044>
- [CITED] Mark Ettinger, Peter Høyer, and Emanuel Knill, “The Quantum Query Complexity of the Hidden Subgroup Problem Is Polynomial,” *Information Processing Letters* 91 (2004), 43–48, DOI 10.1016/j.ipl.2004.01.024. Relevance: query/time separation. <https://arxiv.org/abs/quant-ph/0401083>
- [CITED] Maxime Remaud, André Schrottenloher, and Jean-Pierre Tillich, “Time and Query Complexity Tradeoffs for the Dihedral Coset Problem,” arXiv:2206.14408 (2022). Relevance: logarithmic-query and subexponential-time interpolation, with CSIDH examples. <https://arxiv.org/abs/2206.14408>

## P5.2 - small CM discriminant and ECDLP security

- [CITED] A. O. L. Atkin and Francois Morain, "Elliptic Curves and Primality Proving," *Mathematics of Computation* 61(203), 29-68, 1993, doi:10.1090/S0025-5718-1993-1199989-X. Relevance: CM-method construction context. <https://doi.org/10.1090/S0025-5718-1993-1199989-X>
- [CITED] Michael J. Wiener and Robert J. Zuccherato, "Faster Attacks on Elliptic Curve Cryptosystems," Selected Areas in Cryptography 1998, LNCS 1556, 190-200. Relevance: early equivalence-class rho and look-ahead cycle handling.
- [CITED] Iwan Duursma, Pierrick Gaudry, and Francois Morain, "Speeding up the Discrete Log Computation on Curves with Automorphisms," ASIACRYPT 1999, LNCS 1716, 103-121, doi:10.1007/978-3-540-48000-6_10. Relevance: automorphism-orbit collision speedups. <https://doi.org/10.1007/978-3-540-48000-6_10>
- [CITED] Robert P. Gallant, Robert J. Lambert, and Scott A. Vanstone, "Faster Point Multiplication on Elliptic Curves with Efficient Endomorphisms," CRYPTO 2001, LNCS 2139, 190-200. Relevance: explicit $j=0$, $j=1728$, $D=-7$, and $D=-8$ endomorphisms, subgroup eigenvalues, and GLV decomposition. <https://www.iacr.org/archive/crypto2001/21390189.pdf>
- [CITED] Joppe W. Bos, Thorsten Kleinjung, and Arjen K. Lenstra, "On the Use of the Negation Map in the Pollard Rho Method," ANTS 2010, LNCS 6197, 67-83, doi:10.1007/978-3-642-14518-6_9. Relevance: fruitless-cycle analysis and countermeasures. <https://doi.org/10.1007/978-3-642-14518-6_9>
- [CITED] Daniel J. Bernstein, Tanja Lange, and Peter Schwabe, "On the Correct Use of the Negation Map in the Pollard Rho Method," PKC 2011; IACR ePrint 2011/003. Relevance: practical branchless use of equivalence classes. <https://eprint.iacr.org/2011/003>
- [CITED] Ping Wang and Fangguo Zhang, "Computing Elliptic Curve Discrete Logarithms with the Negation Map," IACR ePrint 2011/008. Relevance: exact fruitless-cycle probabilities, deterministic escape strategy, and ideal orbit-factor benchmark. <https://eprint.iacr.org/2011/008.pdf>

## P4.1 verified references

- [CITED] Taechan Kim and Razvan Barbulescu, “Extended Tower Number Field Sieve: A New Complexity for the Medium Prime Case,” CRYPTO 2016 Part I, LNCS 9814, 543–571, doi:10.1007/978-3-662-53018-4_20; IACR ePrint 2015/1027. Relevance: exTNFS construction and asymptotic constants. <https://eprint.iacr.org/2015/1027>
- [CITED] Razvan Barbulescu and Sylvain Duquesne, “Updating Key Size Estimations for Pairings,” *Journal of Cryptology* 32(4), 1298–1336, 2019, doi:10.1007/s00145-018-9280-5; IACR ePrint 2017/334. Relevance: finite-size SexTNFS equation, BN worked estimate, family polynomials, and key-size tables. <https://eprint.iacr.org/2017/334>
- [CITED] Razvan Barbulescu, “Pairings: scripts and parameters,” public companion source archive. Relevance: surviving `compute_distribution.py` coefficient sampler and parameter files used in the P4.1 reproducibility audit. <https://razvanbarbulescu.pages.math.cnrs.fr/Pairings/Pairings.html>
- [CITED] David Freeman, Michael Scott, and Edlyn Teske, “A Taxonomy of Pairing-Friendly Elliptic Curves,” *Journal of Cryptology* 23, 224–280, 2010, doi:10.1007/s00145-009-9048-z; IACR ePrint 2006/372. Relevance: family taxonomy and wider search-space context. <https://eprint.iacr.org/2006/372>
- [CITED] Aurore Guillevic, “A Short-List of Pairing-Friendly Curves Resistant to Special TNFS at the 128-bit Security Level,” PKC 2020; IACR ePrint 2019/1371. Relevance: refined special-TNFS polynomial selection and current 128-bit practical recommendations. <https://eprint.iacr.org/2019/1371>
- [CITED] Diego F. Aranha, Georgios Fotiadis, and Aurore Guillevic, “A Short-List of Pairing-Friendly Curves Resistant to the Special TNFS Algorithm at the 192-bit Security Level,” *IACR Communications in Cryptology* 1(3), article 3, 2024, doi:10.62056/angyl86bm. Relevance: current 192-bit concrete seeds and implementation-aware comparison. <https://cic.iacr.org/p/1/3/3>
- [CITED] Sean Bowe, “BLS12-381: New zk-SNARK Elliptic Curve Construction,” Electric Coin Company, 2017. Relevance: published BLS12-381 seed and exact $p,r$ regression constants. <https://electriccoin.co/blog/new-snark-curve/>
