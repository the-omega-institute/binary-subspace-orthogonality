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
| `sections/geometry.tex` | Reza's geometric color-list lemma and profile table, exact-profile statistics, and the adjacent-line obstruction to a coloring based solely on the exact profile and quotient isometry type. |
| `sections/higher-dimensions.tex` | Dimension-deletion proposition, n=7 measured instance, and remaining questions. |
| `sections/verification.tex` | Exact executed checks and current formalization scope. |

From this directory, run `pdflatex -interaction=nonstopmode -halt-on-error paper.tex`
twice. The checked convenience PDF is `paper.pdf`. A draft compilation is not
coauthor approval or a submission. Coordinate substantive edits through GitHub
commits or pull requests; no new branch-protection or CI policy is imposed.

The September 30 integration moves Reza's inline sections from `paper.tex`
into the two section files and includes each exactly once. Edit those section
files for subsequent revisions. Reza's geometry contribution from `ad269bf`
and open problems from `144ce04` are now integrated. The follow-up distinguishes
the 12 dimension profiles from the 240 exact profiles, gives the full-edge
certificate its precise role, and formulates the stabilizer question with
simultaneous permutation of color labels. The current fixed coloring does not
determine a color from an exact profile alone.

The [geometry-integration check record](../results/manuscript-geometry-review-20260930.json)
records the reproduced profiles, table and coordinate checks, and the
eight-page PDF build and visual review. The final build has no unresolved
references or layout warnings. This review reruns the geometry profiler;
the unchanged full and line certificates retain their existing check records.

The subsequent [profile audit](../notes/geometry-profile-audit.md) corrects
the comparison of 139 exact multicolored groups with 29 numerical multicolored
groups: the scripts omit the actual H and K, so these are different partitions.
A genuine refinement gives 263 groups, 160 multicolored, and resolves none of
the original 139 multicolored groups completely. Proposition 5.2 supplies a
written obstruction independent of this witness. Its proof and the finite
statistics are distinguished in the [new validation record](../results/geometry-profile-review-20260930.json).

Next integration: Reza develops the structural questions in section 5; Wenlin and Haobo maintain the
chromatic proof and reconcile formal verification in sections 3, 4 and 7. Jointly
agree the introduction, author order, affiliations and AI disclosure before
submission. The current draft does not attribute AI use to Reza. The
six-dimensional coloring theorem's historical report omitted four native
axioms, as confirmed by the recovered original log; see
`notes/formal-verification-audit.md`. The finite coloring certificates have
been independently rechecked. No author-order or AI-disclosure agreement is
implied by this integration.
