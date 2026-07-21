#import "lib/paper.typ": *

#show: paper.with(
  title: "The Dimension Barrier: Separating q-SDH from Constant-Size Assumptions up to Bounded Native Freshness",
  subtitle: "A typed catalogue and audited implication graph, the generic-representation boundary, and a fixed-representation meta-reduction",
  pid: "P2.2",
  keywords: ("q-SDH", "q-type assumptions", "meta-reductions", "black-box separations", "generic group model", "pairing-based cryptography"),
  abstract: [
    A $q$-type assumption such as $q$-SDH hands the adversary a power ladder
    $g, g^x, dots, g^(x^q)$ whose length grows with a scheme's usage
    parameter. Problem P2.2 asks for one of two outcomes: a black-box
    reduction from $q$-SDH to a *constant-size* assumption, or a
    meta-reduction proving that no such reduction exists. We deliver the four
    required artifacts and locate the honest boundary between them. First, a
    uniform typed catalogue of the inversion, exponent, and gap families,
    together with an audited implication graph in which every edge carries its
    breaker transformation, call count, and loss. Second, an exact account of
    where a direct $q$-SDH-to-SXDH reduction dies: a constant-size decisional
    challenge exposes only a fixed-dimensional exponent span, and already the
    prefix $([1]_1, [x]_1, [x^2]_1)$ cannot be embedded. Third, an audit of
    the Lu–Zhandry separation: no fully black-box generic-representation
    reduction bases prime-order $q$-SDH on a true fixed-size assumption once
    $n < q - 1$ (one group) or $binom(n+2, 2) < q$ (bilinear), and we prove
    that any standard-oracle reduction whose guarantee is uniform over all
    group representations is already inside that class. Fourth, our sharpest
    new theorem: for one named concrete representation, a fully black-box
    reduction that introduces at most $s_1$ unexplained ("fresh") labels in
    the $q$-SDH source group is impossible under hardness of the fixed
    assumption whenever $n_1 + s_1 < q - 1$; a safe overcounted threshold for
    broader target-valued bilinear $q$-type games is $binom(n+s+2, 2) + t < q$.
    Three attempted extensions fail for identifiable reasons, and we record
    their post-mortems: random relabeling breaks at a representation
    quantifier, efficiently seeded sparse encodings are information-theoretically
    distinguishable from random injections, and structured-label density does
    not bound execution-wise freshness. The unrestricted problem — reductions
    with native-label rank linear in $q$, and reductions that read the
    adversary's code — remains open, and we state it as such.
  ],
)

// Long audit tables must be allowed to break across pages.
#show figure.where(kind: table): set block(breakable: true)

= Introduction

Pairing-based cryptography leans, in large parts of its deployed and
standardized corpus, on assumption *families* parametrized by an integer $q$
that grows with usage. The prototype is the strong Diffie–Hellman assumption
of Boneh and Boyen @bb2008: in a group of prime order $r$, given the power
ladder $g, g^x, g^(x^2), dots, g^(x^q)$, it must be infeasible to output any
pair $(c, g^(1\/(x+c)))$. The parameter is not cosmetic. In the Boneh–Boyen
short-signature proof, $q$ equals the adversary's signing-query budget
@bb2008; in the BBS family it tracks the number of issued signatures, and
recent concrete-security work shows the dependence is real in both directions
@cat2025 @caht2026; and Cheon's algorithms show that the assumption
*quantitatively degrades* as the ladder lengthens, by roughly $sqrt(d)$ bits
of security for favorable divisors $d$ of $r plus.minus 1$ @cheon2006. A
$q$-type assumption is therefore an awkward foundation: a family whose
strength deteriorates in exactly the parameter that deployments increase.

Problem P2.2 poses the natural structural question. *Either* exhibit a
black-box reduction from $q$-SDH to a constant-size assumption — one whose
instance size does not grow with $q$ — *or* prove via meta-reduction that no
such reduction exists. The required deliverables are a uniform-notation
catalogue, an implication graph with cited edges and loss factors, a written
account of where an attempted constant-size reduction breaks, and a precisely
scoped meta-reduction statement, proved or stated as a target.

This paper is the record of three research sessions on that problem, and its
finding is a *scoped impossibility* — strictly more than the published
boundary, strictly less than an unrestricted separation.

#keybox(title: "Main finding (scoped)")[
  The strongest justified deliverable is a scoped impossibility, not a
  reduction and not an all-black-box impossibility.
  #tag("CITED") On the published side, no fully black-box
  generic-representation reduction bases prime-order $q$-SDH on a true
  fixed-size assumption whose challenger emits $n$ group elements, once
  $n < q - 1$ in a single group or $binom(n+2, 2) < q$ with a bilinear map
  @luzhandry2024.
  #tag("PROVED") Our sharpest new theorem (Theorem 16, from attempt A006)
  extends the separation to *one named concrete representation*: a fully
  black-box reduction that introduces at most $s_1$ unexplained native labels
  in the $q$-SDH source group is impossible under hardness of the fixed
  assumption whenever $n_1 + s_1 < q - 1$; for broader target-valued bilinear
  $q$-type games a safe overcounted threshold is $binom(n+s+2, 2) + t < q$.
  #tag("PROVED") What remains open is exactly the residual class: reductions
  whose native-label rank grows linearly with $q$, and reductions that use the
  $q$-SDH adversary's code non-black-box.
]

== Contributions and honest scope

We contribute (i) the typed catalogue and audited implication graph with
per-edge losses (§3–4, #ref(<fig:graph>)); (ii) the catalogue of constant-size
prime-order candidates and what each does *not* supply (§5); (iii) Cheon's
quantitative obstruction restated in typed notation (§6); (iv) the exact break
point of the direct SXDH embedding — an exponent-span argument that kills the
attempt already at $x^2$ (§7); (v) an audit of the Lu–Zhandry
generic-representation separation and a new boundary corollary: every
*representation-uniform* fully black-box standard-oracle reduction is already
a generic-representation reduction and inherits the published thresholds (§8);
(vi) the bounded-native-freshness meta-reduction, our main new theorem, with
its bilinear sharpening and safe overcount (§9, #ref(<fig:meta>),
#ref(<fig:region>)); (vii) post-mortems of three dead extensions — random
relabeling, efficient sparse encodings, and density-to-freshness transfer —
each with its exact failure point (§10); and (viii) a final scope
classification separating what is ruled out from what is open (§11–12).

We state the scope plainly, as the problem's ground rules demand. Nothing
here reduces $q$-SDH to a constant-size prime-order assumption, and nothing
here is an unrestricted black-box impossibility. The status of P2.2 is
*partial*: complete for the catalogue, the published generic boundary, and
the bounded-freshness representation-dependent class; open for linear native
rank and for non-black-box use of the adversary.

= Setting and typed notation

#tag("CITED") Throughout, $r$ is prime,
$e : bb(G)_1 times bb(G)_2 -> bb(G)_T$ is a non-degenerate bilinear map on
groups of order $r$, and $g_1, g_2$ are fixed generators. We write
$[z]_1 = g_1^z$, $[z]_2 = g_2^z$, and $[z]_T = e(g_1, g_2)^z$ for
$z in ZZ_r$ @bb2008.

#definition(name: "typed power ladder")[
  #tag("PROVED") For $I subset ZZ_(>=0)$, the typed power ladder is
  $ P_i (x; I) = ([x^j]_i)_(j in I), $
  where $[x^0]_i = [1]_i$ is the named base. "Search" means output the named
  value; "decision" means distinguish the named value from an independent
  uniform element of the same typed group. The two tasks are never silently
  interchanged.
]

The typing discipline matters more than it may appear: the names DHE, strong
DH, BDHE, and their index shifts are not canonical across the literature, so
every claim below refers to a displayed tuple, never to a bare acronym
@cheon2006 @luzhandry2024. Near-name variants are not identified without
tuple equality.

= The assumption catalogue

The first deliverable is a uniform-notation catalogue (sub-goal SG-01,
complete). #ref(<tab:inv>) lists the inversion and strong-DH family;
#ref(<tab:exp>) lists the exponent and gap family. Each row records the exact
instance and target in typed notation, with the epistemic tag under which the
research log holds it.

#figure(
  table(
    columns: (auto, 1fr),
    align: (left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Name*], [*Exact instance and target*]),
    table.hline(stroke: 0.5pt),
    [#tag("CITED") $q$-SDH (source core)],
      [Input $P_1 (x; {0, dots, q})$; output any $(c, [1\/(x+c)]_1)$ with
       $c in ZZ_r$, $x + c eq.not 0$ @bb2008 @luzhandry2024.],
    [#tag("CITED") $q$-SDH (typed Boneh–Boyen)],
      [The source core plus $[1]_2, [x]_2$; the extra $bb(G)_2$ terms permit
       public verification but do not alter the search relation @bb2008.],
    [#tag("CITED") $q$-DHI],
      [Input $P_1 (x; {0, dots, q})$; output $[1\/x]_1$ — the prescribed
       choice $c = 0$ of the $q$-SDH relation @bb2008.],
    [#tag("PROVED") $q$-DDHI],
      [Input $P_1 (x; {0, dots, q})$ and $T in bb(G)_1$; decide whether
       $T = [1\/x]_1$ or $T arrow.l bb(G)_1$ uniform.],
    [#tag("CITED") $q$-BDHI],
      [Symmetric original: input $(g, g^x, dots, g^(x^q))$, output
       $e(g,g)^(1\/x)$. Typed lift: input $P_1 (x; {0, dots, q})$ and
       $[1]_2$; output $[1\/x]_T$ @bbibe2004 @bbg2005.],
    [#tag("PROVED") $q$-DBDHI],
      [Decision version of the typed target: distinguish $T = [1\/x]_T$ from
       uniform $T arrow.l bb(G)_T$.],
    [#tag("CITED") $q$-wBDHI],
      [Input independent generators $g_1, h_2$ and $P_1 (x; {1, dots, q})$;
       output $e(g_1, h_2)^(1\/x)$ @bbg2005.],
    [#tag("CITED") $q$-wBDHI$zws^*$],
      [Same input as $q$-wBDHI; output $e(g_1, h_2)^(x^(q+1))$ @bbg2005.],
    table.hline(stroke: 0.7pt),
  ),
  caption: [The inversion and strong-DH family in typed notation (SG-01).],
) <tab:inv>

#figure(
  table(
    columns: (auto, 1fr),
    align: (left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Name*], [*Exact instance and target*]),
    table.hline(stroke: 0.5pt),
    [#tag("CITED") $q$-DHE],
      [Input $P_1 (x; {0, dots, q})$; output $[x^(q+1)]_1$ @luzhandry2024.],
    [#tag("CITED") $q$-DDHE],
      [Input $P_1 (x; {0, dots, q})$ and $T in bb(G)_1$; decide whether
       $T = [x^(q+1)]_1$ or uniform. Also called $q$-strong DDH in some
       sources @luzhandry2024.],
    [#tag("CITED") $q$-BDHE (gap form)],
      [Input independent $g_1, h_2$ and $[x^j]_1$ for
       $j in {0, dots, q-1, q+1, dots, 2q}$; output $e(g_1, h_2)^(x^q)$
       @bbg2005 @cheon2006.],
    [#tag("PROVED") $q$-DBDHE],
      [Decision version of the preceding gap target in $bb(G)_T$.],
    [#tag("CITED") $q$-aBDH],
      [Input $P_1 (x; {0, dots, q})$, $[1]_2, [x]_2$, an independent $h_2$,
       and $h_2^(x^(q+2))$; output $e(g_1, h_2)^(x^(q+1))$ @bb2008.],
    table.hline(stroke: 0.7pt),
  ),
  caption: [The exponent and gap family in typed notation (SG-01). The gap
  tuple omits the power $x^q$ that its target exponentiates.],
) <tab:exp>

= The implication graph and its loss audit

#tag("PROVED") An arrow $H(A) -> H(B)$ means "hardness of $A$ implies
hardness of $B$": operationally, a breaker for $B$ is transformed into a
breaker for $A$. Every edge in #ref(<fig:graph>) was audited against the
primary reduction text — not a survey summary — and carries its
transformation, call count, and loss in #ref(<tab:edges>).

#fig("/figures/P2.2/implication_graph.svg", width: 96%, caption: [
  The audited implication graph (SG-02), drawn from the edge table below;
  schematic rendering of proved/cited reductions, not data. Solid computational
  family in blue; the decisional pair at lower right; $q$-SDH highlighted as
  the problem's anchor. Every edge is one oracle call and success-preserving.
  The truncation family $H(q"-"X) -> H(k"-"X)$, $k <= q$, applies to
  $X in {"SDH", "DHI", "DDHI", "BDHI", "DBDHI", "wBDHI"}$ but not to targets
  whose exponent depends on $q$ (DHE, wBDHI$zws^*$, gap-BDHE).
]) <fig:graph>

#figure(
  table(
    columns: (28%, 49%, 23%),
    align: (left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Edge*], [*Breaker transformation*], [*Loss*]),
    table.hline(stroke: 0.5pt),
    [#tag("CITED") $H(q"-aBDH") -> H(q"-SDH")$],
      [Run the $q$-SDH breaker to get $(c, [1\/(x+c)]_1)$. Divide
       $X^(q+2) - (-c)^(q+2)$ by $X + c$ to get $X^(q+1) + w(X)$ with
       $deg w <= q$; pairing and the supplied $h_2^(x^(q+2))$ isolate the
       wanted $x^(q+1)$ term @bb2008.],
      [1 call; $epsilon$ preserved; $O(q)$ ops],
    [#tag("PROVED") $H(q"-SDH") -> H(q"-DHI")$],
      [Feed the same ladder to the DHI breaker; return its output as the SDH
       answer with $c = 0$ @bb2008.],
      [1 call; $epsilon$; $O(1)$],
    [#tag("PROVED") $H(q"-BDHI") -> H(q"-DHI")$],
      [Pair the DHI output $[1\/x]_1$ with $[1]_2$ @bbibe2004 @bb2008.],
      [1 call; $epsilon$; 1 pairing],
    [#tag("CITED") $H(q"-BDHI") -> H(q"-wBDHI"zws^*)$],
      [From $(w, w^beta, dots, w^(beta^q))$, give the wBDHI$zws^*$ breaker
       base $w^(beta^q)$, the reversed ladder, and $h = w^s$; raise its answer
       to $1\/s$ @bbg2005.],
      [1 call; $epsilon$; $O(q)$ ops],
    [#tag("CITED") $H(q"-wBDHI"zws^*) <-> H(q"-wBDHI")$],
      [Reverse the ladder with new base $g_1^(x^q)$ and hidden exponent
       $1\/x$; the two targets transform into one another @bbg2005.],
      [1 call each way; $epsilon$; $O(q)$],
    [#tag("PROVED") $H(q"-wBDHI"zws^*) -> H(q"-DHE")$],
      [Run the DHE breaker on $(g_1, g_1^x, dots, g_1^(x^q))$ and pair its
       output $g_1^(x^(q+1))$ with $h_2$ @bbg2005 @cheon2006.],
      [1 call; $epsilon$; 1 pairing],
    [#tag("PROVED") $H(q"-DHE") -> H(q"-DHI")$],
      [To use a DHI breaker, set base $g_1^(x^q)$, hidden exponent $1\/x$, and
       reverse the ladder; its output is $g_1^(x^(q+1))$ @cheon2006.],
      [1 call; $epsilon$; $O(q)$ reversal],
    [#tag("PROVED") $H((q+1)"-BDHE") -> H(q"-DHE")$],
      [On the gap tuple, run the $q$-DHE breaker on the prefix through $x^q$
       and pair $g_1^(x^(q+1))$ with $h_2$; ignore higher powers @cheon2006.],
      [1 call; $epsilon$; 1 pairing],
    [#tag("PROVED") $H(q"-DDHI") -> H(q"-DBDHI")$],
      [Pair every source challenge with $[1]_2$ and invoke the DBDHI
       distinguisher @bbibe2004.],
      [1 call; advantage preserved; 1 pairing],
    [#tag("PROVED") $H(q"-"X) -> H(k"-"X)$, $k <= q$],
      [Delete the unused suffix of the ladder before calling the $k$-breaker;
       valid for $X in {"SDH", "DHI", "DDHI", "BDHI", "DBDHI", "wBDHI"}$
       @bb2008.],
      [1 call; preserved; $O(q)$ handling],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Audited edge table (SG-02). $epsilon$ denotes the invoked
  breaker's success probability or advantage.],
) <tab:edges>

#tag("PROVED") The truncation edge formalizes why the assumptions strengthen
as $q$ grows: hardness at the larger parameter implies hardness at the
smaller, while the converse is not supplied by tuple truncation.
#tag("CITED") Boneh and Boyen further prove $q$-SDH random self-reducible by
rescaling the hidden exponent and bases — one solver call, success preserved,
$O(q)$ exponentiations @bb2008.

= Constant-size prime-order candidates

Which fixed-size assumptions could serve as a target? #ref(<tab:static>)
catalogues the standard candidates (SG-03), separating source-group,
cross-source, and target-group consequences.

#figure(
  table(
    columns: (auto, 1fr, 1fr),
    align: (left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Assumption*], [*Fixed-size typed experiment*],
      [*What it supplies — and does not*]),
    table.hline(stroke: 0.5pt),
    [#tag("CITED") DDH in $bb(G)_i$],
      [Distinguish $([1]_i, [a]_i, [b]_i, [a b]_i)$ from
       $([1]_i, [a]_i, [b]_i, [z]_i)$.],
      [A decisional degree-two correlation in one source group; no source
       power ladder @luzhandry2024.],
    [#tag("CITED") XDH / SXDH],
      [XDH: DDH holds in the designated source group despite the pairing;
       SXDH: DDH in both $bb(G)_1$ and $bb(G)_2$.],
      [Constant-size decisional assumptions for asymmetric pairings; no map
       from $bb(G)_T$ back to a source group @yuen2024 @gps2008.],
    [#tag("CITED") DLIN in $bb(G)_i$],
      [For independent $u, v, h$: distinguish
       $(u, v, h, u^a, v^b, h^(a+b))$ from the tuple with random last
       element.],
      [A constant-size linear-relation challenge; still a fixed-dimensional
       source exponent span @bbs2004.],
    [#tag("CITED") co-CDH],
      [Given $([1]_1, [a]_1, [1]_2)$, output $[a]_2$.],
      [A constant-size cross-source search problem; pairing reveals $[a]_T$
       but not $[a]_2$ in the typed interface @bgls2003 @gps2008.],
    [#tag("CITED") DBDH],
      [Given $([1]_1, [a]_1, [b]_1, [1]_2, [c]_2, T)$, distinguish
       $T = [a b c]_T$ from uniform.],
      [A constant-size target-group decision problem; it does not manufacture
       $[x^j]_1$ for unboundedly many $j$ @bbibe2004.],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Constant-size prime-order candidates (SG-03). For every true
  fixed-size candidate here, the generic separation of §8 rules out the fully
  black-box generic reduction from $q$-SDH once $q$ crosses the dimension
  threshold; this is *not* a claim that any of these assumptions is false
  @luzhandry2024.],
) <tab:static>

= The quantitative obstruction: Cheon's exponent recovery

Even before any separation, the ladder itself leaks. The following two
statements are Cheon's, restated in typed notation.

#proposition(name: [Cheon, $d | r - 1$])[
  #tag("CITED") If a divisor $d <= q$ of $r - 1$ is available, the ladder
  contains $g^x$ and $g^(x^d)$, and $x$ is recoverable in
  $O(log r (sqrt((r-1)\/d) + sqrt(d)))$ group operations @cheon2006.
]

#proposition(name: [Cheon, $d | r + 1$])[
  #tag("CITED") If $d | r + 1$ and the ladder reaches degree $2d$, then $x$
  is recoverable in $O(log r (sqrt((r+1)\/d) + d))$ group operations
  @cheon2006.
]

#corollary[
  #tag("PROVED") Recovering $x$ immediately solves $q$-SDH: choose any
  $c eq.not -x$ and compute $[1\/(x+c)]_1$ by known-scalar exponentiation.
]

#tag("CITED") These attacks reduce generic square-root security by roughly a
factor $sqrt(d)$ for favorable divisors, so concrete group sizes must account
for both $q$ and the factorization of $r plus.minus 1$ @cheon2006. This is
the quantitative face of the same phenomenon the rest of the paper treats
structurally: the ladder is a high-dimensional correlated object, and nothing
constant-size manufactures it.

= Where a direct reduction dies: the exponent-span barrier

The problem asks for a written account of where an attempted
constant-size-assumption reduction breaks. Attempt A001 tried the most
natural route: use one source-group DDH challenge — hence one component of an
SXDH challenge — to synthesize the ladder a $q$-SDH adversary expects, and
convert its answer into a DDH decision. The reduction class tested is
straight-line, type-preserving, and algebraic: it combines challenge elements
by group operations and known-scalar exponentiation, invokes one $q$-SDH
adversary, and has no source-group encoding of a target-group pairing value.

#proposition(name: "exponent-span barrier")[
  #tag("PROVED") Write the source DDH challenge exponents as $(1, a, b, z)$,
  with $z = a b$ in the real branch and independent $z$ in the random branch.
  Every $bb(G)_1$ element such a reduction creates before its oracle call has
  exponent in $L = op("span")_(ZZ_r) {1, a, b, z}$. In the random branch, no
  nonconstant $x$ satisfies both $x in L$ and $x^2 in L$; hence even the
  prefix $([1]_1, [x]_1, [x^2]_1)$ of a nontrivial $q$-SDH instance cannot be
  embedded.
]

#proof[
  In the random branch, treat $a, b, z$ as algebraically independent. Put
  $x = A + B a + C b + D z in L$. If $x^2 in L$, comparing the coefficients
  of $a^2, b^2, z^2, a b, a z, b z$ — which do not occur in $L$ — forces,
  over an odd prime field, $B = C = D = 0$. So $x$ is a known constant,
  statistically independent of the challenge bit, and an oracle query built
  from it cannot transfer any distinguishing advantage. Pairing does not
  repair the embedding: it produces degree-two exponents in $bb(G)_T$ only,
  while $q$-SDH needs the missing powers in $bb(G)_1$, and the typed
  interface has no operation $bb(G)_T -> bb(G)_1$.
]

#remark[
  #tag("PROVED") This kills the stated straight-line algebraic class *at*
  $x^2$ — before the first oracle call — but is not by itself a proof against
  rewinding, adaptive multiple calls, or representation-dependent and
  non-algebraic reductions. Those classes are the subject of the next two
  sections.
]

The failure is dimensional, and it is the germ of everything that follows: a
constant-size challenge exposes a fixed-dimensional algebraic span, while the
$q$-SDH ladder demands $q + 1$ correlated powers.

= The generic-representation boundary

== The Lu–Zhandry separation, audited

The fixed-dimensional-span failure of A001 was turned, by Lu and Zhandry,
into a separation for a substantially broader class @luzhandry2024. Attempt
A002 audited the primary proof bodies; we restate the result in the
repository's terms. Methodologically the result descends from Coron's
meta-reduction technique for signature-scheme optimality bounds @coron2002,
which is ancestry, not itself a $q$-SDH separation.

#definition(name: "GR-BB reduction")[
  #tag("CITED") A generic-representation black-box (GR-BB) reduction is
  polynomial-time, fully black-box in a possibly *inefficient* adversary
  whose generic group-operation queries it may observe and answer, and
  representation-independent: it receives concrete bit-string labels and may
  apply arbitrary bit gates to them, but its advantage is defined as the
  infimum over all — possibly inefficient — implementations of the group.
  The formulation permits interactive assumptions and adaptive oracle calls
  @luzhandry2024.
]

#definition(name: "fixed-size and q-type assumptions")[
  #tag("CITED") A *fixed-size* assumption may be interactive and may contain
  non-group auxiliary data, but across the experiment its challenger outputs
  at most $n$ group elements. A *$q$-type* assumption requires that a
  transcript expose at least $q$ linearly independent bounded-degree
  polynomial functions tied to a hidden $x_0$, such that knowing $x_0$ lets
  an efficient algorithm break the assumption with noticeable probability
  @luzhandry2024.
]

#theorem(name: "Lu–Zhandry")[
  #tag("CITED") In a prime-order generic group, if a GR-BB reduction maps
  such a $q$-type assumption to a fixed-size assumption of size $n < q - 1$,
  then a generic polynomial-time algorithm breaks the fixed-size assumption.
  In the generic bilinear extension the same conclusion holds when
  $binom(n+2, 2) < q$ @luzhandry2024.
]

#proof[
  (Audited skeleton; the proof is Lu–Zhandry's.) The meta-reduction selects
  an inefficient perfect $q$-adversary that brute-forces the hidden
  exponents. It traces every reduction-created source element as a known
  linear combination of the $n$ fixed challenge elements, so the exponent
  vectors submitted to the adversary lie in a subspace of dimension at most
  $n + 1$. A Vandermonde rank argument and finite-field root finding leave
  only polynomially many candidates for $x_0$; generic equality tests
  identify the valid ones, so the otherwise inefficient adversary is
  simulated efficiently, and the reduction with its oracle replaced by this
  simulation is a generic attack on the fixed-size assumption. With a
  pairing, recorded exponents may be quadratic in the $n$ input exponents;
  linearizing in all degree-at-most-two monomials gives dimension
  $binom(n+2, 2)$ and the bilinear threshold @luzhandry2024.
]

#corollary(name: [$q$-SDH instantiation])[
  #tag("CITED") $q$-SDH meets the $q$-type definition: its ladder supplies
  the required independent polynomials, and knowledge of $x$ yields a valid
  answer by selecting any $c eq.not -x$ after a consistency check. Hence no
  generic reduction from $q$-SDH to a true fixed-size assumption exists at
  the stated thresholds @luzhandry2024.
]

#remark(name: "why composite order escapes")[
  #tag("CITED") The prime-order proof step fails in unknown-composite-order
  groups: finding the required polynomial roots can be as hard as factoring,
  and independently rerandomizable hidden subgroups supply the "shadow"
  dimensions that the positive Déjà Q reductions exploit — computational
  $q$-SDH and broad polynomial $q$-type classes *do* reduce to constant-size
  subgroup hiding in composite-order pairing groups, with $Theta(q)$ hybrid
  loss in the original framework and logarithmic loss in the follow-up
  @chasemeiklejohn2014 @cmm2016 @luzhandry2024. The positive and negative
  results are consistent; the barrier is specifically prime-order.
]

#tag("CITED") The theorem's tracing argument also covers algebraic reductions
whose outputs carry algebraic explanations, but it does not rule out every
black-box reduction in every formalization: representation-specific
standard-model reductions, and reductions non-black-box in the $q$-adversary,
are outside its stated class @luzhandry2024. Section 3.5 of the paper
likewise leaves open derived groups whose law depends on auxiliary bit
strings, equality branches, or concrete encodings @luzhandry2024. These gaps
are exactly where the remainder of this paper operates.

== Representation-uniform reductions are already generic (A003)

One might hope that a *standard-oracle* reduction — a single machine that may
inspect encodings as bit strings — escapes the GR-BB class. It does not, as
long as its guarantee is uniform over representations.

#definition(name: "UR-FBB reduction")[
  #tag("PROVED") For single-stage prime-order group games $F$ and $Q$, a
  reduction is *universally representation-uniform fully black-box* (UR-FBB)
  if a single PPT oracle machine $R$ (i) treats the $Q$-adversary as an
  oracle, though it may run multiple copies and rewind; (ii) uses the group
  through labeling, group-operation, equality, and optional pairing
  interfaces, and otherwise performs arbitrary bit computation on labels; and
  (iii) satisfies pointwise representation uniformity: for *every* admissible
  implementation $G$ of the group, including possibly inefficient ones, and
  every possibly inefficient adversary $A$, if
  $op("Adv")_(Q^G)(A) >= epsilon$ for non-negligible $epsilon$, then
  $op("Adv")_(F^G)(R^(A,G)) >= delta$ for some non-negligible $delta$
  independent of $G$ and $A$. Conditions (i)–(ii) match the classical
  fully-black-box interface @rtv2004.
]

#theorem(name: "boundary theorem")[
  #tag("PROVED") Every UR-FBB reduction is a GR-BB reduction. Consequently no
  UR-FBB reduction bases prime-order $q$-SDH on a true fixed-size assumption
  of size $n$ when $n < q - 1$, nor, with a generic bilinear map, when
  $binom(n+2, 2) < q$.
]

#proof[
  A GR adversary with non-negligible infimum advantage breaks $Q^G$ for every
  implementation $G$ with a common non-negligible lower bound $epsilon$.
  Applying uniformity pointwise gives one non-negligible $delta$ with
  $ inf_G op("Adv")_(F^G)(R^(A,G)) >= delta . $
  Conditions (i)–(ii) make $R$ a GR oracle circuit, so this is a GR-BB
  reduction — indeed stronger than required, since the source definition may
  assign a reduction per adversary. The thresholds then follow from Theorem
  9 and its $q$-SDH instantiation. For single-stage games the statement
  transfers to the type-safe model, since TS-BB and GR-BB reductions exist if
  and only if one another @luzhandry2024. Label inspection does not
  invalidate the wrapper: for label length $ell > log_2 r + omega(log lambda)$,
  a polynomially bounded interaction guesses a valid unseen label only with
  negligible probability @luzhandry2024.
]

#remark[
  #tag("PROVED") The qualifier *universal* is load-bearing: it includes
  possibly inefficient random sparse implementations. A guarantee promised
  only over efficiently computable or standardized representations need not
  include them and is *not* promoted to GR-BB by this argument. That weaker
  quantifier is precisely the residual case attacked next.
]

= Main theorem: bounded native freshness

The remaining gap after §8 is the reduction promised for *one named concrete
representation* $G_*$ — an elliptic-curve group with its standardized
encoding, say — where the machine may exploit native operations: validation,
decompression, hash-to-group, table lookups, arbitrary encoding-bit branches.
Random relabeling cannot reach this class (§10.1). Attempt A006 reaches part
of it directly, without relabeling, by charging a new resource.

#definition(name: [$s$-fresh reduction])[
  #tag("PROVED") Fix a concrete prime-order group implementation $G_*$ with
  efficient validity, equality, group operations, and known-scalar
  exponentiation, and a fixed-size assumption $F^(G_*)$ whose challenger
  returns at most $n$ source-group elements per execution. A PPT oracle
  reduction $R$ is *$s$-fresh* if it is fully black-box in every, possibly
  inefficient, $q$-SDH adversary and, on every execution, at most $s$
  distinct valid source-group labels first appear without one of these
  explanations: challenger output, the public generator, known-scalar
  labeling, or a previously observed group operation. "First appear" is
  tested when a bit string is first used as a typed group element, including
  when it is supplied directly inside a $q$-SDH oracle query. Each such
  unexplained label consumes one *freshness unit*.
]

#tag("PROVED") The budget is semantic and execution-wise; it need not be
derivable from the source code of $R$. Native validation, decompression,
hash-to-group, and arbitrary bit-dependent code are all permitted — the
meta-reduction merely maintains a counter and invokes the theorem under the
promise that the counter never exceeds $s$.

#theorem(name: "bounded-fresh-label separation")[
  #tag("PROVED") For polynomially bounded $q, n, s$ with $n + s < q - 1$, an
  $s$-fresh PPT fully-black-box reduction from $q$-SDH to $F^(G_*)$ yields a
  PPT attack on $F^(G_*)$ with the reduction's success probability against a
  perfect $q$-SDH adversary. Consequently, if $F^(G_*)$ is hard, no such
  reduction exists at that threshold.
]

#proof[
  *Enlarged coefficient trace.* The meta-reduction runs $R$ on the real
  $F^(G_*)$ challenge and keeps a dictionary mapping every typed source label
  seen so far to a vector $D(P) in ZZ_r^(n+s+1)$, with coordinates for the at
  most $n$ challenger labels, the at most $s$ native fresh labels, and the
  public generator. A newly returned challenger label and a newly
  encountered fresh label each receive the next unused unit vector;
  known-scalar labeling receives the corresponding multiple of the generator
  vector; a group-operation output receives the sum or difference of its
  operands' vectors. If an output label already occurs in the dictionary,
  its *old* vector is retained.

  *Evaluation invariant.* Let $b in ZZ_r^(n+s+1)$ hold the actual discrete
  logarithms of the basis labels relative to the public generator.
  Inductively every dictionary vector satisfies
  $ log_g P = ⟨D(P), b⟩ . $
  Retaining the old vector after an actual-label collision preserves this:
  both candidate vectors evaluate to the same group element, so both evaluate
  to the same logarithm — the meta-reduction never needs to *discover* the
  hidden linear relation among the entries of $b$ that the collision
  witnesses. Adaptivity and representation-bit branches do not disturb the
  invariant: the same concrete code runs on the same labels, coefficients may
  depend on all previously observed bits and equalities, and every
  unexplained valid label created along the chosen branch is charged to the
  freshness budget instead.

  *Simulating the inefficient adversary.* In each oracle call, the labels of
  the proposed $q$-SDH ladder form the rows of a known matrix $M$ with at
  most $n + s + 1$ columns. Let $w$ be the actual discrete logarithm of the
  queried generator. For a valid nonidentity tuple with hidden exponent $x$,
  the invariant gives
  $ M (b \/ w)^top = (s_1 (x), dots, s_q (x))^top , $
  so the actual $x$ lies on the root list produced by the low-dimensional
  subspace root-list argument of Lu–Zhandry with $n + s$ replacing $n$
  @luzhandry2024 — only the *dimension of the column space* is used, never
  the logarithms of the fresh basis elements. When $n + s < q - 1$ the list
  is polynomial. Fix the perfect adversary to reject invalid or
  identity-generator tuples and use deterministic tie-breaking. For each
  candidate $x$ the simulator checks the ladder equations by ordinary scalar
  exponentiation and equality in the real group; the nonidentity first ladder
  element makes a consistent $x$ unique; the simulator picks a public
  $c eq.not -x$ and returns the queried generator raised to $(x+c)^(-1)$.
  Rewinding and multiple adaptive calls are covered because the dictionary
  and freshness counter persist across the whole execution. The simulation
  is transcript-exact for the selected perfect adversary and adds only
  polynomial field arithmetic, root finding, and group operations, so it
  introduces no success-probability loss.
]

#ref(<fig:meta>) shows the architecture. The only imported mathematical
ingredient is the root-list simulation and its bilinear quadratic lift; the
theorem changes the column count, not the proof @luzhandry2024.

#fig("/figures/P2.2/metareduction.svg", width: 90%, caption: [
  Architecture of the bounded-fresh-label meta-reduction (A006); structural
  schematic of the proof, not data. Native code may inject up to $s$
  unexplained source labels; each receives one formal coordinate, so every
  ladder row sent to the simulated adversary lies in a known
  $(n+s+1)$-dimensional span and the root-list simulation applies whenever
  $n + s < q - 1$.
]) <fig:meta>

== Bilinear sharpening and safe overcount

#proposition(name: "source-valued pairing case")[
  #tag("PROVED") For typed $q$-SDH whose oracle instance lies in one source
  group, pairing outputs do not enlarge that source-group trace. If $n_1$
  counts the fixed-assumption challenge labels that can reach that source
  through recorded source-to-source maps and $s_1$ counts unexplained labels
  in that source, the proof of Theorem 16 gives the sharper threshold
  $ n_1 + s_1 < q - 1 , $
  provided no unrecorded target-to-source conversion is available — if one
  is, each of its outputs is fresh.
]

#proposition(name: "broader bilinear games")[
  #tag("PROVED") For a bilinear $q$-type game whose independent polynomial
  family may occur in the target group, or as a conservative common-space
  bound, at most $s$ unexplained source labels and $t$ unexplained target
  labels give trace dimension at most
  $ binom(n+s+2, 2) + t , $
  the quadratic term containing all degree-at-most-two monomials in the
  $n + s + 1$ source coordinates and each unexplained target label one
  additional coordinate. Replaying the bilinear root-list theorem yields the
  separation whenever $binom(n+s+2, 2) + t < q$. The bound deliberately
  overcounts monomials that typing may forbid: it is a safe sufficient
  threshold, not a claimed tight one.
]

#corollary(name: "what a surviving reduction must do")[
  #tag("PROVED") Contrapositively, any fully-black-box fixed-representation
  reduction that coexists with hardness of $F^(G_*)$ must, in some execution,
  introduce at least $q - 1 - n_1$ unexplained labels in the $q$-SDH source
  group, or use an unrecorded conversion into that source, or leave the
  fully-black-box class altogether. Linear-in-$q$ native freshness and
  non-black-box access to the adversary remain outside the theorem.
]

#fig("/figures/P2.2/freshness.svg", width: 100%, caption: [
  Parameter regions of the A006 thresholds; direct plots of the theorem's
  inequalities, not data. Left: the source-valued separation region
  $n_1 + s_1 < q - 1$ for $q in {8, 16, 32, 64}$ — deeper shading marks
  parameter pairs already separated at shorter ladders; above each line the
  residual class is open. Right: the minimal ladder length at which the
  separation bites, for the source-valued case ($q = n_1 + s_1 + 2$) versus
  the conservative bilinear overcount with $t = 0$
  ($q = (n+s+2)(n+s+1)\/2 + 1$): the safe bilinear bound demands
  quadratically longer ladders.
]) <fig:region>

#tag("PROVED") This closes a genuine part of the representation-dependent
gap left by Lu–Zhandry: bounded native operations are now covered, and the
remaining resource is precisely *source-label rank growing with $q$* — or an
unrecorded conversion supplying it.

= Dead ends and their exact failure points

Three attempted extensions failed. Each post-mortem narrows the open
residual class, so we record them as results, not anecdotes.

== Random relabeling cannot settle a fixed representation (A004)

#proposition(name: "the representation quantifier")[
  #tag("PROVED") A reduction guaranteed only for one family $G_*$ has
  quantifier form
  $ exists G_* thick exists R_* thick forall A_* : quad
    "Break"_(Q^(G_*))(A_*) ==> "Break"_(F^(G_*))(R_*^(A_*)) . $
  The random-relabeling simulation needs this implication for a freshly
  sampled random sparse implementation $G_L$, which the premise does not
  entail — and cannot be made to entail. Given any $R_*$ working for a
  publicly specified $G_*$, modify it to check the canonical encoding of the
  public generator (or a public representation identifier), abort on
  mismatch, and otherwise run $R_*$: the modified machine behaves identically
  on $G_*$ and can fail on every random relabeling. Abstract group
  isomorphism does not transfer the behavior of a machine that reads
  encodings.
]

#proposition(name: "the trace invariant fails syntactically")[
  #tag("PROVED") Independently, concrete encodings break the
  fixed-dimensional trace at the syntax level: native validation,
  decompression, or hash-to-curve code may produce a valid point without an
  observed group-operation query, so the simulator receives no algebraic
  explanation of that point in the span of the fixed-size challenge.
]

#tag("CITED") The published structural discussion likewise leaves open
derived group laws using auxiliary strings, equality branches, or concrete
representations; the classification covers natural affine algebraic
constructions only @luzhandry2024. #tag("HEURISTIC") Fresh
representation-derived points do not visibly generate the correlated ladder
$g^x, dots, g^(x^q)$, so this trace failure is not positive evidence that a
useful reduction exists; it only prevents the relabeling route from
certifying impossibility. A006 is exactly the repair: charge the unexplained
points instead of trying to relabel them away.

== Efficient sparse encodings cannot replace random injections (A005)

Could the GR wrapper's information-theoretic random injection be replaced by
an *efficiently computable* sparse encoding, extending the separation to
reductions promised over all efficient representations? No:

#theorem(name: "finite-seed counting obstruction")[
  #tag("PROVED") Let an efficient encoding family use an $m(lambda)$-bit
  seed, $m$ polynomial, to choose injections from an $r$-element group into
  an $N$-element label space, $N >= r$. A possibly inefficient adversary
  distinguishes the family from a uniform random injection with advantage at
  least $1 - 2^m \/ (N)_r$, where $(N)_r = N(N-1) dots.c (N-r+1)$ — an
  overwhelming bound, since $log (N)_r >= log(r!) = Omega(r log r)$ while $m$
  is polynomial and $r$ is exponential in $lambda$.
]

#proof[
  The family's support contains at most $2^m$ injective tables; the uniform
  distribution has support $(N)_r$. The distinguisher queries the encoding on
  all $r$ inputs, reconstructs the full table, enumerates all $2^m$ seeds,
  and accepts exactly when the table belongs to the family: it accepts a
  family member with probability one and a random injection with probability
  at most $2^m \/ (N)_r$.
]

#tag("PROVED") Neither proposed weakening survives. A $t$-wise independent
encoding matches only a bounded-query view, and the fully-black-box
adversary quantifier supplies no query bound — the distinguisher above uses
$r > t$ queries. A PRP protects only computationally bounded distinguishers,
so it buys a computational premise, not the needed information-theoretic
wrapper. #tag("CITED") This boundary accords with Zhandry's generic-query
convention, in which bit computation is unbounded and no efficient keyed
permutation internal to the type-safe model is a secure PRP @zhandry2022, and
with the later sparse-GGM separations for admissibly encoded, dense,
elliptic-curve, and bilinear settings @wang2025.

#tag("PROVED") A second, independent obstruction: breaking a static
assumption in an artificial efficient encoding would refute hardness only
*for that encoding*. If the assumption is asserted for a named curve family
$G_*$, an attack on a different artificial family does not contradict its
premise. #tag("PROVED") What does transfer is the query-bounded version: if
the reduction class quantifies only over adversaries making at most $t$
encoding or group queries, a $t$-wise or lazy-table simulation becomes
plausible — a strictly narrower class that must state its query bound
explicitly.

== Structured-label density does not bound freshness (A007)

The structured generic-group model gives algorithms free access to a partial
label operation $star.op$ agreeing with the hidden group law, and charges
only generic group-oracle queries. #tag("CITED") For a prime-order-$r$ group
whose constrained-label fraction is $delta$, its hard labeling distribution
bounds $T$-query discrete-log advantage by
$ delta(3T+2) + (3T+1)^2\/r + 1\/r $
@cghw2026. Could density $delta$ substitute for A006's freshness budget?

#proposition(name: "density is not a label count")[
  #tag("PROVED") The $delta T$ term bounds a *random-hybrid probability* —
  the chance a random challenge interaction touches the structured region —
  whereas freshness counts distinct labels *adaptively selected* along an
  actual execution. A publicly recognizable structured subset of size
  $delta r >= q$ lets a reduction deliberately address $q$ distinct labels
  even when $delta$ is negligible. The query parameter $T$ cannot substitute
  either: $star.op$ evaluations and all other label computation are free in
  the model's cost measure, so $T$ does not bound the labels enumerated,
  parsed, or produced through $star.op$ and then used as group elements.
]

#tag("PROVED") Instantiating the model's hard labeling distribution instead
repeats A004's quantifier error: the theorem is existential in a labeling
distribution, and a reduction promised for one named labeling need not
retain its guarantee there @cghw2026. #tag("PROVED") The valid conditional
transfer is explicit and modest: if a separate premise bounds by $u$ the
total distinct valid labels first-used through raw code and free
$star.op$ evaluation, then A006 applies verbatim with $s = u$, and
$n_1 + u < q - 1$ suffices for the source-valued separation. Density alone
supplies no such $u$; a future extension must bound native-label *rank* or
exploit the algebraic relations revealed by $star.op$ directly.

= Scope classification and scheme evidence

#ref(<tab:scope>) is the final classification: which reduction classes are
ruled out, by what, and what survives.

#figure(
  table(
    columns: (1fr, 1fr),
    align: (left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Reduction class*], [*Result*]),
    table.hline(stroke: 0.5pt),
    [#tag("CITED") TS-BB / GR-BB, fully black-box in possibly inefficient
     adversaries],
      [Ruled out at the published single-group ($n < q-1$) and bilinear
       ($binom(n+2, 2) < q$) thresholds @luzhandry2024.],
    [#tag("CITED") Algebraic reduction with explanations],
      [The same tracing separation applies @luzhandry2024.],
    [#tag("PROVED") UR-FBB standard-oracle reduction, universal over
     representations],
      [Implies GR-BB (Theorem 13, A003); ruled out at the same thresholds.],
    [#tag("PROVED") One fixed concrete representation, at most $s_1$
     unexplained source labels],
      [Direct trace separation at $n_1 + s_1 < q - 1$ (Theorem 16, A006),
       without random relabeling.],
    [#tag("PROVED") Representation class not closed under random sparse
     relabeling, native-label rank crossing A006's threshold],
      [A004 blocks relabeling and A006 no longer applies; existence or
       impossibility open.],
    [#tag("CITED") Non-black-box use of the adversary's code],
      [Outside the fully-black-box taxonomy and outside every theorem here
       @rtv2004 @luzhandry2024.],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Final scope classification (NOTES §11). The strongest justified
  deliverable is the scoped impossibility of rows 1–4.],
) <tab:scope>

Scheme-level evidence reinforces the same picture from the outside:
#ref(<tab:schemes>) summarizes the positive results and why none crosses the
prime-order barrier.

#figure(
  table(
    columns: (auto, 1fr, 1fr),
    align: (left, left, left),
    table.hline(stroke: 0.7pt),
    table.header([*Setting*], [*What is established*], [*Why it does not
      close P2.2*]),
    table.hline(stroke: 0.5pt),
    [#tag("CITED") Déjà Q, 2014],
      [Computational $q$-SDH and broad polynomial $q$-type classes reduce to
       constant-size subgroup hiding in composite-order pairings; the
       $q$-SDH proof uses $q + 2$ shadow copies with $Theta(q)$ hybrid loss
       @chasemeiklejohn2014.],
      [Not prime-order; asymmetric, computational-source only.],
    [#tag("CITED") Déjà Q follow-up, 2016],
      [Broader classes, symmetric and asymmetric composite order,
       logarithmic tightness loss @cmm2016.],
      [Still does not cross the prime-order barrier.],
    [#tag("CITED") Boneh–Boyen signatures],
      [Standard-model proof under $q$-SDH with $q$ the signing-query bound,
       roughly factor-two advantage loss @bb2008.],
      [A use of $q$-SDH, not a reduction of it.],
    [#tag("CITED") Dual-form exponent inversion],
      [Modified Boneh–Boyen-like signatures and Gentry-IBE variants proved
       under SXDH @yuen2024.],
      [Altered dual-form schemes — not the original assumption or scheme.],
    [#tag("CITED") BBS/BBS+ concrete security, 2025],
      [After $q$ signatures, attacks recover the key at $Theta(q)$-DL cost;
       scheme security *implies* $Theta(q)$-SDH @cat2025.],
      [A reverse, scheme-to-$q$-SDH comparison; reinforces usage-dependent
       security.],
    [#tag("CITED") BBS tightness, 2026],
      [Tight $q$-SDH proof when each message is signed once; with repeats, no
       tight algebraic reduction to the considered $q$-SDH variants
       @caht2026.],
      [Tightens a $q$-type proof; neither removes $q$ nor adds a static
       basis.],
    table.hline(stroke: 0.7pt),
  ),
  caption: [Positive results and scheme taxonomy (NOTES §6). Current
  BBS-family results retain $q$-dependent premises in both directions.],
) <tab:schemes>

#tag("EMPIRICAL", detail: "literature searches, 2026-07-09") Primary-title,
author, and ePrint-oriented searches found no later primary paper giving
either an unrestricted prime-order reduction of $q$-SDH to a fixed-size
assumption or an impossibility theorem covering every
representation-specific black-box reduction.

= Open problems

The residual gap is logged as P2.2/Q003 and has exactly two branches.

#tag("PROVED") *Branch 1 — linear native rank.* No result here rules out a
representation-dependent reduction that injects native-label rank linear in
$q$: by the corollary of §9, a surviving reduction must place at least
$q - 1 - n_1$ unexplained labels in the $q$-SDH source in some execution, and
nothing yet shows a concrete-operation class cannot do so. Closure requires
either proving that every reduction in a precisely named class has
source-label trace rank below $q - n_1 - 1$, or exhibiting a positive
constant-size reduction whose native rank reaches the required dimension.

#tag("PROVED") *Branch 2 — code access.* A reduction that reads the code of
the $q$-SDH adversary is outside the fully-black-box taxonomy @rtv2004 and
outside every theorem above. Closure requires an explicitly non-black-box
construction or a meta-reduction whose scope includes code access.

#tag("PROVED") *Do not repeat.* Random relabeling (A004), finite-seed
substitution (A005), and density-to-count transfer (A007) each fail for the
recorded, distinct reasons; the structural conclusion of the whole record is
that the common obstruction is *dimensional* — a fixed-size prime-order
challenge exposes a fixed-dimensional algebraic span, bilinearity raises the
degree but leaves an $O(n^2)$ monomial space, and only composite-order
hidden subgroups have so far manufactured the missing dimensions
@chasemeiklejohn2014 @luzhandry2024. The relevant resource for any future
attack on Branch 1 is the rank of native labels actually injected into the
adversary transcript, not their density, their efficiency, or their number
in expectation.

= Conclusion

P2.2 asked for a reduction or a separation. The answer supported by the
record is a *layered separation with an honest boundary*. The catalogue and
audited implication graph fix the objects (§3–5). Cheon's attacks quantify
the ladder's intrinsic leak (§6). The direct constant-size embedding dies at
$x^2$ for dimensional reasons (§7). The Lu–Zhandry theorem turns that
dimension count into an impossibility for all fully black-box
generic-representation reductions, and every representation-uniform
standard-oracle reduction is inside that class (§8). Our main theorem
extends the separation to a named concrete representation whenever the
reduction's unexplained native source labels are bounded, at the sharp
source-valued threshold $n_1 + s_1 < q - 1$ and the safe bilinear overcount
$binom(n+s+2, 2) + t < q$ (§9). Three natural extensions fail at identified
points, and their post-mortems narrow the residue to exactly two branches:
native-label rank linear in $q$, and non-black-box use of the adversary's
code (§10–12). Within prime-order pairing groups, no route to basing
$q$-SDH on a constant-size assumption survives except through one of those
two doors — and no one has yet opened either.

#v(1em)
#line(length: 100%, stroke: 0.6pt + rgb("#d8d7cf"))
#v(0.5em)

#heading(numbering: none, level: 1)[Reproducibility]

#text(size: 9.3pt)[
P2.2 is a theory problem: it contains no computational code and no `data/`
CSVs, and this paper reports none. The three figures are schematics generated
by `papers/figures/P2.2/make.py` directly from the recorded content — the
implication graph from the audited edge table (NOTES §2), the meta-reduction
architecture from the proof of Theorem 16 (attempt A006), and the threshold
regions from the stated inequalities $n_1 + s_1 < q - 1$ and
$binom(n+s+2, 2) + t < q$; none depicts measured data. Primary proof bodies
checked during the research include four implication reductions, the
Lu–Zhandry lemmas and main theorems, the Reingold–Trevisan–Vadhan
fully-black-box definition, Zhandry's labeling model, and the structured-GGM
lower bound. Every mathematical claim above carries one of the epistemic tags
#tag("PROVED"), #tag("CITED"), #tag("HEURISTIC"),
#tag("EMPIRICAL", detail: "scope stated") exactly as in the research log;
untagged sentences are exposition, not claims.
]

#bibliography("refs/P2.2.bib", title: [References], style: "ieee")
