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
certificate its precise role, and initially formulated the stabilizer question
with simultaneous permutation of color labels. Corollary 5.3 below settles
that question negatively for the full stabilizer. The current fixed coloring does not
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
written obstruction independent of this witness. Corollary 5.3 also rules out
full-stabilizer equivariance: swapping coordinates 1 and 2 fixes every clique
label while exchanging two adjacent lines. A structural rule must break that
symmetry. The profile proof and finite statistics have their
[validation record](../results/geometry-profile-review-20260930.json);
the corollary and final PDF have a separate
[follow-up validation record](../results/stabilizer-obstruction-review-20260930.json).

Reza's October 1 subsection on auxiliary choices from `785e778` is retained.
It uses S=span(e1,e3,e5) to distinguish the adjacent coordinate lines by
intersection dimension. The integrated text states the precise obstruction
scope and separates this example from an explanation of the full archived
coloring. The actual diagnostic path is `develop/file_separator.py`.
The [auxiliary-subsection review record](../results/auxiliary-choice-review-20261001.json)
records the coordinate checks and rebuilt PDF.

Reza's next projection diagnostic from `b913143` is preserved at its actual
path `develop/Complement_projection.py`. Its output remains 240 groups,
101 single-color and 139 multicolored. Proposition 5.4 proves that these are
the identical exact-profile groups: the projection image and H are mutual
annihilators under the perfect T--S pairing. The new
[readable argument and missing lift datum](../notes/complement-projection.md)
and [independent check](../results/complement-projection-check.json) explain
why projection alone adds no information, while intersection with S can.
The current nine-page PDF builds in two passes without warnings and all pages
are visually reviewed; see the
[projection review record](../results/complement-projection-review-20261001.json).

The [lift-feature review](../notes/lift-map-features.md) runs Reza's script
from `409f379`, with zero-vector inclusion and JSON serialization corrected.
Its requested tuple produces 878 groups, 300 multicolored; adding the features
to the exact (K,P) baseline gives 1662 groups, 160 multicolored and completely
resolves 87 of the original 139 multicolored groups. Proposition 5.5 gives
adjacent planes with identical K,P,rank,image,kernel, proving those features
insufficient for any proper coloring. The note gives a written orthogonality
criterion in lift coordinates. See the
[independent record](../results/lift-map-matrix-check.json) and
[current build review](../results/lift-map-matrix-review-20261001.json).

Reza's next script from `d150bb5` is actually `develop/lift_map_value.py`
(singular). Its zero-vector skip is corrected. The requested value list gives
836 groups, 196 multicolored, omitting the exact K and domain basis. Retaining
exact K,P and all basis values gives 2809 singleton vertices, with an explicit
reconstruction proof now in section 5. The
[value-pattern note](../notes/lift-map-values.md) explains why singleton
encodings are a complete vertex representation, not a 15-color rule. The
[independent check](../results/lift-map-values-check.json) reproduces every
pattern and reconstructs every vertex; the
[current build review](../results/lift-map-values-review-20261001.json) records
the final PDF and precise scope.

Next integration: Reza develops the structural questions in section 5; Wenlin and Haobo maintain the
chromatic proof and reconcile formal verification in sections 3, 4 and 7. Jointly
agree the introduction, author order, affiliations and AI disclosure before
submission. The current draft does not attribute AI use to Reza. The
six-dimensional coloring theorem's historical report omitted four native
axioms, as confirmed by the recovered original log; see
`notes/formal-verification-audit.md`. The finite coloring certificates have
been independently rechecked. No author-order or AI-disclosure agreement is
implied by this integration.
