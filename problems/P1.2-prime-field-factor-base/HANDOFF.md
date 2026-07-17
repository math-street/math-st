# Handoff — P1.2 — after session 6

## State in five lines

[PROVED] Standard $L_p[1/2,c]$ size and fixed $m$ are incompatible with
inverse-polylogarithmic success by the support-size theorem in `CLAIM.md`.
[PROVED] Replacing the bound by $p^{1/2+o(1)}$ but charging only online time is
nonuniformly trivial by A008's positional factor base and full target table.
[EMPIRICAL: all recorded 16–20-bit groups] A008 covered all 1,373,865 targets
with zero membership or sum errors, while storing one entry per target.
[PROVED] Construction, description/advice, preprocessing, and storage must be
bounded in addition to online membership and decomposition time.
[CONJECTURE] The corrected variants remain open: P1.2/Q002 is the optional
Candidate-D predicate gap, P1.2/Q003 is the required specification choice,
and P1.2/Q004 is the coordinate-aware Variant-S finder question.

## Audit 1 — standard L-notation

[PROVED] For a fixed factor base $\mathcal F$ of size $s$, the reachable set
is the image of $\mathcal F^m$ and has size at most $s^m$. Standard
$L_p[1/2,c]=p^{o(1)}$ and fixed $m$ therefore reach $p^{o(1)}$ targets, while
Hasse gives $\#E(\mathbb F_p)=p^{1+o(1)}$. Success is at most
$p^{-1+o(1)}$, below every inverse polynomial in $\log p$.

[PROVED] Fixed $m$ needs $s\ge p^{1/m-o(1)}$. Retaining standard L-size needs
$m\ge(1/c+o(1))\sqrt{\log p/\log\log p}$.

## Audit 2 — uncharged square-root correction

[PROVED] For a cyclic group of order $r$, generator $G$, fixed $m$, and
$B=\lceil r^{1/m}\rceil$, the factor base
$$
\bigcup_{j=0}^{m-1}\{[dB^j]G:0\le d<B\}
$$
has at most $mB$ points and represents every target through the base-$B$
digits of its scalar.

[CONDITIONAL: unbounded input-specific preprocessing and nonuniform indexed
tables] Storing the representation under every point gives polylogarithmic
online membership and decomposition with success one.

| Tag | $p$ | $r$ | Base size ($m=3$) | Square-root diagnostic | Target entries | Stored point references | Errors |
|---|---:|---:|---:|---:|---:|---:|---:|
| [EMPIRICAL: exhaustive] | 65,519 | 65,537 | 120 | 255 | 65,537 | 262,148 | 0 |
| [EMPIRICAL: exhaustive] | 262,139 | 261,431 | 190 | 511 | 261,431 | 1,045,724 | 0 |
| [EMPIRICAL: exhaustive] | 1,048,571 | 1,046,897 | 304 | 1,023 | 1,046,897 | 4,187,588 | 0 |

[PROVED] The table needs $\Theta(rm\log p)$ bits and $\Omega(r)$ construction
steps, exponential in the input length. It embeds a complete DLP table and is
not an efficient ECC attack.

## Non-vacuous continuations

- Variant S: $p^{1/2+o(1)}$ base, fixed $m=3$, but every input-specific
  construction, description, advice, preprocessing, and storage resource is
  $p^{o(1)}$; online algorithms are uniform and polylogarithmic.
- Variant L: standard $L_p[1/2,c]$ base,
  $m=\Theta(\sqrt{\log p/\log\log p})$, with all offline resources bounded by
  a fixed-constant $L_p[1/2,C]$ and uniform polylogarithmic online algorithms.

[PROVED] A007 excludes the original statement; A008 excludes treating an
online-only square-root substitution as a meaningful repair. Neither excludes
the resource-bounded variants above.

[PROVED] A009 additionally excludes every fixed, failure-adaptive, or
randomized translate-probe decoder using only tests $R-a\in\mathcal F$: after
$T$ probes its success is at most $T|\mathcal F|/r$. Candidate A therefore
needs $p^{1/2-o(1)}$ probes in that model. Coordinate-aware algorithms lie
outside this result.

[PROVED] A smooth order-64 multiplicative subgroup at $p=65537$ has an exact
six-squaring membership chain and defines a succinct coordinate-aware
60-point factor base outside the A009 model.

[EMPIRICAL: 96 targets, three random controls] Its normalized decomposition
ratio to random was 1.112 (95% bootstrap interval $[0.819,1.470]$), and its
pair-check ratio was 0.969 ($[0.827,1.130]$).

[EMPIRICAL: SymPy 1.14.0, five-second limit] Direct and chain $f_4$ systems
completed at $p=17$ and timed out at $p=257$ and $p=65537$. This is not a
lower bound; the cited PKC 2016 and FFA 2018 work also leaves system-solving
complexity open.

## Supporting candidate record

- [EMPIRICAL: p=65519,262139,1048571] Candidate A is random-like in
  decomposition density and generic pair-scan work.
- [EMPIRICAL: q=5,7,11] The extension-field control recovered all planted
  secrets end to end.
- [EMPIRICAL: prime-field test curves] Candidate B is more than 99.97% of each
  group; Candidate D's proxy has sizes 0, 0, and 2, while its full predicate
  remains P1.2/Q002.
- [PROVED] Candidate C's rational-map subclass is constant, while a distinct
  degree-$d$ plane curve meets $E$ in at most $3d$ points.
- [PROVED] Candidate E has succinct smooth-subgroup membership, but
  [EMPIRICAL: tested range] no density, generic-scan, or tested Gröbner
  advantage supplied the required decoder.

## Files that matter

- `CLAIM.md`: standard-L impossibility theorem and attacks.
- `attempts/A008-nonuniform-preprocessing-loophole.md`: radix construction.
- `attempts/A009-translate-probe-lower-bound.md`: restricted generic lower
  bound.
- `attempts/A010-smooth-subgroup-factor-base.md`: coordinate-aware audit and
  post-mortem.
- `CORRECTED_VARIANTS.md`: two resource-bounded replacement statements.
- `../../OPEN_QUESTIONS.md`: unique root index and four complete P1.2 entries.
- `NOTES.md`: all formal and experimental tables.

## What I would tell my replacement

Do not search under the original statement, and do not call a giant lookup
table a square-root-version breakthrough. Resolve P1.2/Q003 first. Under
Variant S, use P1.2/Q004 and count all offline state; P1.2/Q002 applies only if
Candidate D is resumed. Do not infer a lower bound from A010's timeouts. Under
Variant L, start from `CLAIM.md`'s growing-$m$ threshold.
