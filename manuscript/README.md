# Joint manuscript

This is the editable joint paper, following the seven-section structure
proposed by Reza. The dated two-author note in `notes/` remains historical.
The current author display is alphabetical by surname as a temporary editing
convention; the collaborators have not settled publication author order.

| File | Contribution and handoff |
| --- | --- |
| `sections/introduction.tex` | Reza's expanded introduction from `f34e58f`, integrated with source problem numbers and the zero-vertex convention. |
| `sections/clique.tex` | Reza's full radical/quotient proof from `f34e58f`, including the endpoint argument and six-dimensional corollary. |
| `sections/lines.tex` | Written weighted lower-bound proof and checked 13-color upper bound. |
| `sections/chromatic-six.tex` | Complete certificate argument for chi(O_6*) = 15 and the precoloring reduction. |
| `sections/geometry.tex` | Starting invariants and data for Reza's planned geometric analysis. |
| `sections/higher-dimensions.tex` | Dimension-deletion proposition, n=7 measured instance, and remaining questions. |
| `sections/verification.tex` | Exact executed checks and current formalization scope. |

From this directory, run `pdflatex -interaction=nonstopmode -halt-on-error paper.tex`
twice. The checked convenience PDF is `paper.pdf`. A draft compilation is not
coauthor approval or a submission. Coordinate substantive edits through GitHub
commits or pull requests; no new branch-protection or CI policy is imposed.

The September 30 integration moves Reza's inline sections from `paper.tex`
into the two section files and includes each exactly once. Edit those section
files for subsequent revisions. The geometry section still contains the
original handoff; no later geometry contribution was present at the reviewed
remote revision `f34e58f46d4065e88cdfd209cbb17cff99aa89d8`.

Next integration: Reza develops section 5; Wenlin and Haobo maintain the
chromatic proof and reconcile formal verification in sections 3, 4 and 7. Jointly
agree the introduction, author order, affiliations and AI disclosure before
submission. The current draft does not attribute AI use to Reza. The
six-dimensional coloring theorem's historical report omitted four native
axioms, as confirmed by the recovered original log; see
`notes/formal-verification-audit.md`. The finite coloring certificates have
been independently rechecked. No author-order or AI-disclosure agreement is
implied by this integration.
