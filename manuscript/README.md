# Joint manuscript

This is the editable joint paper, following the seven-section structure
proposed by Reza. The dated two-author note in `notes/` remains historical.
The current author display is alphabetical by surname as a temporary editing
convention; the collaborators have not settled publication author order.

| File | Contribution and handoff |
| --- | --- |
| `sections/introduction.tex` | Reza's planned introduction; current text supplies verified definitions and results to expand. |
| `sections/clique.tex` | Reza's planned clique section; contains the theorem and radical/quotient synopsis, with the complete archived Lean proof in `formal/`. |
| `sections/lines.tex` | Written weighted lower-bound proof and checked 13-color upper bound. |
| `sections/chromatic-six.tex` | Complete certificate argument for chi(O_6*) = 15 and the precoloring reduction. |
| `sections/geometry.tex` | Starting invariants and data for Reza's planned geometric analysis. |
| `sections/higher-dimensions.tex` | Dimension-deletion proposition, n=7 measured instance, and remaining questions. |
| `sections/verification.tex` | Exact executed checks and current formalization scope. |

From this directory, run `pdflatex -interaction=nonstopmode -halt-on-error paper.tex`
twice. The checked convenience PDF is `paper.pdf`. A draft compilation is not
coauthor approval or a submission. Coordinate substantive edits through GitHub
commits or pull requests; no new branch-protection or CI policy is imposed.

Next integration: Reza expands sections 1, 2 and 5; Wenlin and Haobo develop
the chromatic proof and formal verification in sections 3, 4 and 7. Jointly
agree the introduction, author order, affiliations and AI disclosure before
submission. The current draft does not attribute AI use to Reza.
