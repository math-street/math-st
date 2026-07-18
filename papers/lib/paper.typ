// paper.typ — shared academic template for the ECC-research paper series.
//
// Usage (from papers/<PID>.typ):
//   #import "lib/paper.typ": *
//   #show: paper.with(
//     title: "...", subtitle: "...", pid: "P1.1",
//     abstract: [ ... ], keywords: ("a", "b"),
//   )
//   = Introduction
//   ...
//
// Theorem-like environments: #theorem[...], #lemma[...], #proposition[...],
// #corollary[...], #definition[...], #remark[...], each optionally with a name:
//   #theorem(name: "Addition compiler")[ statement ]
// Proofs: #proof[ ... ].  Tags: #tag("PROVED"), #tag("EMPIRICAL", "p<2^20").

#let accent = rgb("#1c5cab")
#let accent-soft = rgb("#e8eef8")
#let ink = rgb("#111111")
#let muted = rgb("#5a5a55")
#let rule-col = rgb("#d8d7cf")

// ---- epistemic tag chip -------------------------------------------------
#let tag(kind, detail: none) = {
  let col = (
    "PROVED": rgb("#0b6b3a"),
    "CITED": rgb("#1c5cab"),
    "CONDITIONAL": rgb("#8a5a00"),
    "HEURISTIC": rgb("#8a5a00"),
    "EMPIRICAL": rgb("#6a3aa0"),
    "CONJECTURE": rgb("#a03a3a"),
    "UNVERIFIED": rgb("#a03a3a"),
  ).at(kind, default: muted)
  let label = if detail == none { kind } else { kind + ": " + detail }
  box(inset: (x: 0.4em, y: 0.15em), outset: (y: 0.1em), radius: 2pt,
      fill: col.lighten(85%), text(size: 0.72em, fill: col.darken(8%),
      weight: "semibold", tracking: 0.02em, label))
}

// ---- theorem environments ----------------------------------------------
#let thmcounter = counter("thm")

#let _thmbox(kind, col, name, body) = {
  thmcounter.step()
  block(width: 100%, above: 1.1em, below: 1.1em, breakable: true,
    stroke: (left: 2.2pt + col), inset: (left: 0.9em, y: 0.2em),
  )[
    #text(weight: "bold", fill: col.darken(10%))[#kind #context thmcounter.display()]#{
      if name != none [ #text(fill: muted, weight: "regular")[ (#name)]]
    }.
    #h(0.3em)
    #body
  ]
}

#let theorem(name: none, body) = _thmbox("Theorem", rgb("#1c5cab"), name, body)
#let lemma(name: none, body) = _thmbox("Lemma", rgb("#1c5cab"), name, body)
#let proposition(name: none, body) = _thmbox("Proposition", rgb("#1c5cab"), name, body)
#let corollary(name: none, body) = _thmbox("Corollary", rgb("#1c5cab"), name, body)
#let definition(name: none, body) = _thmbox("Definition", rgb("#0b6b3a"), name, body)
#let remark(name: none, body) = _thmbox("Remark", rgb("#5a5a55"), name, body)

#let proof(body) = block(width: 100%, above: 0.8em, below: 1.1em)[
  #text(style: "italic", fill: muted)[Proof.] #h(0.2em) #body
  #h(1fr) $square$
]

// A boxed "result" / takeaway callout.
#let keybox(title: "Result", body) = block(width: 100%, above: 1.1em, below: 1.1em,
  fill: accent-soft, radius: 4pt, inset: 1em, stroke: 0.6pt + accent.lighten(40%))[
  #text(weight: "bold", fill: accent.darken(5%), size: 0.95em)[#title.]
  #h(0.3em) #body
]

// ---- figure helper ------------------------------------------------------
#let fig(path, caption: none, width: 100%) = figure(
  image(path, width: width),
  caption: caption,
)

// ---- main template ------------------------------------------------------
#let paper(
  title: "",
  subtitle: none,
  pid: "",
  series: "ECC Research Program",
  authors: (
    [*math.st* #super[1]],
    [*\@math\_\_street* #super[1]],
  ),
  contributors: "with GPT 5.6 Sol · Claude Fable 5",
  affiliation: [#super[1]Independent research collective, math.st],
  date: "July 2026",
  abstract: [],
  keywords: (),
  body,
) = {
  set document(title: title, author: ("math.st", "@math__street"))
  set page(
    paper: "us-letter",
    margin: (x: 1.35in, top: 1.25in, bottom: 1.1in),
    numbering: "1",
    number-align: center,
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 8.5pt, fill: muted)
        grid(columns: (1fr, 1fr),
          align(left)[#pid],
          align(right)[#title],
        )
        v(-0.4em)
        line(length: 100%, stroke: 0.4pt + rule-col)
      }
    },
  )
  set text(font: ("Libertinus Serif", "New Computer Modern", "Times New Roman"),
    size: 10.5pt, fill: ink, lang: "en")
  set par(justify: true, leading: 0.62em, first-line-indent: (amount: 1.2em, all: true))
  show par: set block(spacing: 0.9em)

  // Math
  set math.equation(numbering: "(1)")
  show math.equation.where(block: true): set block(spacing: 1.0em)

  // Headings
  set heading(numbering: "1.1")
  show heading: set text(fill: ink)
  show heading.where(level: 1): it => block(above: 1.5em, below: 0.8em)[
    #set text(size: 12.5pt, weight: "bold")
    #if it.numbering != none [#counter(heading).display() #h(0.5em)]
    #it.body
  ]
  show heading.where(level: 2): it => block(above: 1.15em, below: 0.6em)[
    #set text(size: 11pt, weight: "bold", fill: rgb("#33332f"))
    #if it.numbering != none [#counter(heading).display() #h(0.5em)]
    #it.body
  ]
  show heading.where(level: 3): it => block(above: 1.0em, below: 0.5em)[
    #set text(size: 10.5pt, weight: "bold", style: "italic", fill: rgb("#33332f"))
    #it.body
  ]

  // Links & refs
  show link: set text(fill: accent)
  show ref: set text(fill: accent)

  // Tables: clean booktabs-ish default
  set table(stroke: none, inset: (x: 0.7em, y: 0.45em))
  show table: set text(size: 9.5pt)
  show figure.where(kind: table): set figure.caption(position: top)
  set figure(gap: 0.9em)
  show figure.caption: set text(size: 9pt, fill: muted)

  // ---------- title block ----------
  block(width: 100%)[
    #set align(left)
    #text(size: 8.5pt, fill: accent, weight: "bold", tracking: 0.08em)[
      #upper(series) · #pid
    ]
    #v(0.55em)
    #text(size: 19pt, weight: "bold")[#title]
    #if subtitle != none {
      v(0.25em)
      text(size: 12.5pt, fill: muted, style: "italic")[#subtitle]
    }
    #v(0.9em)
    #text(size: 10.5pt)[#authors.join(h(1.2em))]
    #v(0.2em)
    #text(size: 9.5pt, fill: muted, style: "italic")[#contributors]
    #v(0.35em)
    #text(size: 9pt, fill: muted)[#affiliation #h(1em) · #h(1em) #date]
  ]
  v(0.4em)
  line(length: 100%, stroke: 0.6pt + rule-col)
  v(0.6em)

  // ---------- abstract ----------
  block(width: 100%, inset: (left: 0.2em))[
    #set text(size: 9.7pt)
    #set par(first-line-indent: 0em, leading: 0.58em)
    #text(weight: "bold", fill: muted, size: 8.5pt, tracking: 0.1em)[ABSTRACT]
    #v(0.3em)
    #abstract
    #if keywords.len() > 0 {
      v(0.5em)
      text(size: 9pt)[#text(weight: "bold")[Keywords.] #keywords.join(" · ")]
    }
  ]
  v(0.6em)
  line(length: 100%, stroke: 0.6pt + rule-col)
  v(0.9em)

  // ---------- body ----------
  body
}

// ---- references block ---------------------------------------------------
#let bibline(key, body) = {
  block(above: 0.55em, below: 0.55em)[
    #grid(columns: (2.4em, 1fr), gutter: 0.3em,
      text(fill: muted, size: 9pt)[[#key]],
      text(size: 9.3pt)[#body],
    )
  ]
}
