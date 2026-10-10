# Focused orthogonality working draft

[Read the PDF](paper.pdf) · [LaTeX source](paper.tex) ·
[Collaboration PR1](https://github.com/the-omega-institute/binary-subspace-orthogonality/pull/1)

This 14-page draft implements the agreed October 9 consolidation direction. Its
main argument foregrounds the clique formula in every dimension,
`chi(Gamma_6)=12`, `chi(O_6*)=15`, and the dimension-seven lower bound
19 with clique number 16. The exact dimension-seven chromatic numbers
remain open. The geometric interpretation of the six-dimensional
coloring and the established structural obstructions are retained in
Appendix A.

The submitted manuscript at `28e27a82068a2f9129fdb5d168bd0fc179cf3e48` and
the separate 25-page [extended draft](../extended/README.md), including
the partial nineteen-color count, orbit and covering analyses, are
preserved. No case-by-case exclusion is resumed. Preparation of this
working draft does not decide its publication, submission or eventual
use after the JAC outcome. The author, affiliation and disclosure wording
is retained for coauthor review.

## Proof and evidence map

| Focused result | Source retained | Verification scope |
| --- | --- | --- |
| All-dimensional clique formula, Theorem 2.1 | `../sections/clique.tex` directly imported | Written radical/quotient proof; attributed Lean snapshot with its pinned upstream dependencies |
| Six-dimensional line equality, Theorem 3.2 | `../sections/lines.tex` directly imported | Written weighted lower bound and explicit twelve-color partition; standard-library certificate/encoding checker |
| Six-dimensional full equality, Theorem 4.1 | `../sections/chromatic-six.tex` directly imported | Fifteen-clique and complete 2,824-vertex coloring; all 3,986,076 pairs and 44,968 edges checked |
| Seven-dimensional lower bound 19, Theorem 5.3 | `sections/dimension-seven.tex`; statement/proof bodies preserved from the extended draft | Written capacity, parity and universal eight-Lagrangian completion proof; bounded exact coordinate checks |
| Six-dimensional geometry, Appendix A | `../sections/geometry.tex` directly imported | Existing mathematical obstructions and finite profile diagnostics; a conceptual fifteen-color construction remains open |

The dimension-seven lower bound is independent of the subsequent profile
exclusions. Its coordinate checker covers 4,096 polarization pairs,
288 even heptads, 2,016 six-point cliques, and 8,505 incidence counts,
plus nine explicit partial-spread controls. The universal completion
statement is proved by hyperplane counting, rather than inferred from
the nine examples. No nineteen-color witness is supplied.

The original six-dimensional Lean theorem retains the three standard
axioms and four native-evaluation axioms. Section 7 lists all four names;
the [formal audit](../../notes/formal-verification-audit.md) explains
their origin. The line equality, geometric profile calculations and
dimension-seven proof are outside that Lean theorem's scope. This
consolidation includes no new Lean build or formalization claim.

## Reproduction

From the repository root, run the existing checks:

```sh
python3 develop/check_full_coloring.py results/full-15-coloring.json --report /tmp/orth-full.json
python3 develop/check_line_chromatic_exact.py
python3 develop/check_dimension_seven_nineteen_obstruction.py --report /tmp/orth-n7.json
```

These three checks were rerun for the focused draft and their reports
match the saved records. They do not rerun the paused nineteen-color
covering searches or the historical Lean build. The lower-bound and
finite-certificate scopes remain separate.

Build from this directory with TeX Live, repeating until references stabilize:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

The final PDF builds without LaTeX warnings or overfull/underfull boxes.
All fourteen pages were rendered and visually reviewed, with the verification,
appendix transitions and intact disclosure block checked after the final edits.
The focused sources contain thirteen preserved proof bodies. The
introduction's result statements and the dimension-seven statement/proof
bodies match the extended draft; the four directly imported section
files retain their original contents. References and citations close.
The only new mathematical exposition is the scope and open-question
summary, not a new theorem. Journal, final title and eventual manuscript
use remain joint decisions.
