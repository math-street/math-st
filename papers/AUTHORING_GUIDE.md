# Paper authoring guide (read fully before writing a paper)

You are writing one polished academic PDF paper per ECC-research problem, grounded
in the **actual research content** in `problems/<PID>-<slug>/`. The exemplar
`papers/P1.1.typ` (compiled `P1.1.pdf`, 11 pages) is the reference — match its
structure, density, and honesty.

## Hard requirements
- **≥ 10 pages** in the compiled PDF (verify with `python build.py <PID>`).
- **Grounded in real content.** Read the problem's `PROBLEM.md`, `NOTES.md`,
  `STATE.md`, `HANDOFF.md`, and whatever result files exist (`RESULTS.md`,
  `CLAIM.md`, `LOG.md`, `attempts/`, `data/*.csv`, `refs/*.md`). Use the actual
  theorems, definitions, empirical numbers, parameter ranges, and obstructions.
  **Do not fabricate results.** If the research reached a negative result, an
  obstruction, or a conditional/empirical finding, write the paper that way —
  negative and partial results are legitimate and expected here.
- **Epistemic honesty.** Keep the repo's tags via `#tag("PROVED")`,
  `#tag("CITED")`, `#tag("EMPIRICAL", detail: "p<2^20")`,
  `#tag("CONDITIONAL", detail: "GRH")`, `#tag("HEURISTIC")`, `#tag("CONJECTURE")`.
  Attach them to the corresponding claims exactly as the research notes do.
- **Visuals: at least 2–3 figures** generated from the real data (`data/*.csv`)
  or reconstructed from the research (schematics, distributions, scaling fits,
  heatmaps, flow/structure diagrams). Reuse existing `problems/<PID>/figures/*.svg`
  if good, but prefer regenerating with the shared style for consistency.
- **Real mathematics.** Include the actual formulas, theorem statements, and
  derivations from the research (summation polynomials, cost models, class-group
  bounds, Dickman/smoothness integrals, isogeny/quaternion facts, etc.).
- **Authors are preset by the template**: `math.st`, `@math__street`, contributor
  line "with GPT 5.6 Sol · Claude Fable 5". Do not change them.

## File layout to produce, per paper
- `papers/<PID>.typ`            — the paper (e.g. `papers/P2.3.typ`)
- `papers/refs/<PID>.bib`       — BibTeX for its citations
- `papers/figures/<PID>/make.py`— figure generator (writes `.svg` next to it)
- compiled `papers/<PID>.pdf`   — via `python build.py <PID>`

## Template API (`#import "lib/paper.typ": *`)
```typst
#show: paper.with(
  title: "…", subtitle: "…",            // subtitle optional
  pid: "P2.3",
  keywords: ("…", "…"),
  abstract: [ … one dense paragraph … ],
)
= Section     == Subsection    === Subsubsection
```
Environments (each takes optional `name:`):
`#theorem(name: "…")[…]`, `#lemma`, `#proposition`, `#corollary`,
`#definition`, `#remark`, `#proof[…]` (auto QED □),
`#keybox(title: "Result")[…]` (highlighted callout),
`#fig("/figures/<PID>/x.svg", width: 80%, caption: […])`,
`#tag("EMPIRICAL", detail: "…")`.
Cross-reference figures/tables with `#ref(<label>)` where you attached `<label>`
after a `#fig(...)` or `#figure(...)`. Cite with `@bibkey` (renders `[n]`).
End the paper with:
```typst
#bibliography("refs/<PID>.bib", title: [References], style: "ieee")
```

## Typst gotchas (these WILL bite you — the exemplar already handles them)
- **Figure image paths must be root-absolute**: `"/figures/<PID>/x.svg"` (the
  compile root is `papers/`). Relative paths resolve against `lib/` and fail.
- **No `big(...)`/`bigl`**: use `lr(( … ))` for auto-sized delimiters.
- **No `angle.l` / `angle.r`**: use the unicode brackets `⟨` and `⟩` directly.
- **`bmod` does not exist**: use `mod` (e.g. `x mod 3`).
- **Fractions in exponents**: write `p^(1\/2)` (escape the slash as `\/`).
- **`#E` / cardinality**: use `hash E(FF_p)` in math (the `hash` symbol prints #).
- **Fields**: `FF_p`, `FF_(q^n)`, `ZZ`, `QQ`, `RR`, `CC` are built-in shorthands.
- **Citations must use the native bibliography** (above). Do NOT hand-roll a
  reference list with labels — labels on plain blocks are not referenceable
  ("cannot reference block").
- Multi-cite in a row `@a @b @c` is fine.
- Keep `#tag(...)` calls OUTSIDE math mode (in markup text).

## Matplotlib figure style
Every `figures/<PID>/make.py` starts with:
```python
import os, sys
import numpy as np, matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F
F.apply()
OUT = os.path.dirname(__file__)
# … build fig …  then:  F.finish(fig, os.path.join(OUT, "name.svg"))
```
- Palette: `F.PALETTE[0..7]` (fixed order, don't cycle past what you need),
  sequential `F.SEQ`, inks `F.INK`, `F.MUTED`, `F.GRID`, surface `F.SURFACE`.
- **Do not put `\#` in matplotlib mathtext titles** (it crashes the parser);
  write "group order r" instead of `\#E`.
- Save **SVG** (crisp in the PDF). Load real CSVs from
  `../../../problems/<PID>-<slug>/data/…` with stdlib `csv` or `numpy`.

## Suggested paper skeleton (adapt to the actual research)
1. Introduction — the problem, why it matters, the finding in one `#keybox`.
2. Setting & notation.
3. Core construction / model / definitions.
4. Main theorem(s) with proof or proof sketch (from the repo's proofs).
5. Figure-backed analysis (taxonomy / scaling / distribution / structure).
6. Empirical validation — a table of parameters and measured quantities from
   the real `data/` CSVs, with honest ranges and CIs where the notes give them.
7. Obstruction / limitations / open questions — faithfully from `STATE.md` /
   `OPEN_QUESTIONS.md`.
8. Conclusion.
9. Reproducibility note + `#bibliography(...)`.

## Compile loop
```
python build.py <PID>     # prints "ok  <PID>.pdf -- N pages"; must be ≥10
```
Iterate on Typst errors until it says `ok`. If a figure is missing, run its
`make.py` first. Never leave a paper that does not compile.
