# Clique and chromatic numbers of binary subspace orthogonality graphs

**Haobo Ma · Reza Nikandish · Wenlin Zhang**

This is the public paper and reproducibility workspace for our work on
orthogonality graphs over the binary field. For the standard dot product on
`F_2^n`, the full graph has all nonzero subspaces as vertices; two distinct
subspaces are adjacent if every vector of one is orthogonal to every vector
of the other. Its line subgraph has only the one-dimensional subspaces.

## Start here

| What you want | Where to go |
| --- | --- |
| Read the complete paper | [Paper PDF](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/paper.pdf) |
| Review the extended working draft, including the dimension-seven lower bound 19 | [Extended PDF](manuscript/extended/paper.pdf) · [draft source and evidence guide](manuscript/extended/README.md); publication and submission remain joint decisions |
| Cite the public preprint | [Zenodo record: 10.5281/zenodo.23210092](https://doi.org/10.5281/zenodo.23210092) |
| Read or edit the manuscript source | [LaTeX source](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/paper.tex) · [current collaboration PR](https://github.com/the-omega-institute/binary-subspace-orthogonality/pull/1) |
| Understand the main results and their evidence | The results table below |
| Reproduce the finite checks | [Reproduction guide](docs/REPRODUCING.md) |
| Explore the geometric arguments | [Geometry section](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/sections/geometry.tex) |
| Follow our next collaboration | [Ideal-intersection Laplacian project](https://github.com/the-omega-institute/ideal-intersection-laplacian) |

The repository paper links identify manuscript snapshot `28e27a8`.
PR #1 remains open for collaboration; the default branch provides this navigation
page and retains its earlier research snapshot. Use the linked revision for the
complete paper and current certificates.

## Results and verification

Write `N(r)` for the number of nonzero subspaces of `F_2^r`.

| Result | Evidence |
| --- | --- |
| For every `n >= 1`, `omega(O_n*) = max(n, N(floor(n/2)) + (n mod 2))` | [Radical/quotient proof](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/sections/clique.tex) · [attributed Lean source](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/formal/NikandishClique.lean) |
| The full dimension-six graph has chromatic number **15** | A 15-clique and an explicit coloring of all 2,824 vertices; [independent check](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/results/full-15-check.json) covers all 3,986,076 pairs and 44,968 edges |
| The dimension-six line graph has chromatic number **12** | [Written weighted lower bound](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/notes/line-coloring.md) and [checked 12-color certificate](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/results/line-coloring-12-check.json) |
| The dimension-seven line graph and full-subspace graph require **at least 19 colors** | [Quadratic parity and partial-spread completion proof](notes/dimension-seven-nineteen-obstruction.md) and [exact finite checks](results/dimension-7-nineteen-obstruction.json); exact chromatic numbers remain open |
| The earlier full dimension-seven lower bound was **18 colors**, exceeding its clique number 16 | [Anchor forcing and omitted-color proof](notes/dimension-seven-eighteen-obstruction.md) and [82-vertex certificate](results/dimension-7-eighteen-obstruction.json), retained as history |
| Specified geometric profiles and stabilizer-equivariant rules cannot explain a proper coloring with the prescribed clique labels | [Precise statements and proofs](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/sections/geometry.tex) |

The six-dimensional [chromatic Lean development](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/formal/Chromatic/Verify.lean)
has a successful historical build. Its final theorem uses the three standard
axioms (`propext`, `Classical.choice`, `Quot.sound`) **and four native-evaluation
axioms**. See the [verification audit](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/notes/formal-verification-audit.md)
for the exact dependencies. A completed pure-kernel replacement is not claimed.
The independent finite checks and the written mathematical proofs have their
own stated scopes.

**The dimension-seven chromatic number remains open, with lower bound 19.** A complete structural
15-color rule also remains open. Failed exploratory candidates are retained as
research history; they are not proofs of upper bounds.

The earlier [29-vertex obstruction](notes/dimension-seven-obstruction.md) proves
that sixteen colors are impossible in dimension seven. Its lower bound is
a written argument checked by exact integer computation, with no Lean or
UNSAT-solver dependence. The obstruction itself has chromatic number 17;
no seventeen-coloring of the full graph is claimed.

The [dimension-seven forced-color reduction](notes/dimension-seven-propagation.md)
now gives an equivalent list instance with 14,540 vertices and 928,571 edges.
Its geometric color-list formula and exact counts are checked. The new
obstruction now proves that this sixteen-color list instance is uncolorable.

The subsequent [subspace retraction](notes/subspace-retraction.md) preserves
the chromatic number and reduces the full dimension-seven graph to 913
vertices. Fixing the clique and forced lines leaves an equivalent list
instance with **890 vertices, 33,978 edges and 426,406 pairwise clauses**.
The dimension-seven chromatic number remains open.

The [retracted SAT encoding](notes/retracted-sat-encoding.md) now has an
independent audit of every generated clause and a positive control using
the existing six-dimensional certificate. One 120-second Glucose4 attempt
returned unknown; no seven-dimensional coloring or UNSAT result was obtained.
The subsequent written obstruction settles sixteen-color nonexistence
independently of that solver attempt.

The stronger [nonradical-line retraction](notes/nonradical-line-retraction.md)
now retains only lines and totally isotropic subspaces: 577 vertices in
dimension seven. Its checker covers every original vertex and all
1,160,206 original edges. The correct seventeen-color list problem has
561 uncolored vertices and 18,056 edges. Its former forced lines now
have two allowed colors; the old sixteen-color propagation is not reused.

The [seventeen-color encoding](notes/seventeen-color-encoding.md) is now
emitted and audited clause by clause. One 120-second search returns
unknown on the original normalization. The equivalent characteristic-vector
clique encoding has 7,814 variables and 244,442 clauses, now independently
audited clause by clause. Its separate 120-second attempt also returns
unknown. Neither attempt supplies a coloring or a new chromatic bound.

The [seven-line symmetry proof](notes/seven-line-symmetry.md) further
restricts the 128 two-color patterns to ten representatives using
orthogonal lifts and clique-color renormalization. Its 118 additional
CNF clauses are checked. Its bounded search returns unknown, with no
coloring or chromatic conclusion. Within the full seven-line pattern
only, a [further saturation proof](notes/full-seven-line-branch.md)
leaves 490 uncolored vertices. Its deterministic CNF has 6,286 variables
and 196,350 clauses, each independently audited from geometric lists and
full-span orthogonality.

The [clique-triangle forcing proof](notes/forced-seven-line-color.md)
now shows that all seven special lines must receive color fifteen in
every normalized seventeen-coloring. Thus mask0 is the only possible
pattern; the other nine, including the previously audited mask127 branch,
are excluded by a written graph argument. Seven 42-vertex certificates
check the forcing mechanism. The equivalent residual problem has
554 vertices, 16,730 edges, 7,744 variables and 241,782 clauses.
Color sixteen remains available at every residual vertex, so this is
a seventeen-color problem. Its [CNF is now emitted and independently
audited](notes/zero-seven-line-branch.md); no solver was run on it.

The new [omitted-color argument](notes/dimension-seven-eighteen-obstruction.md)
excludes this final pattern and proves **chi(O_7*) >= 18**. Two forced
color-fifteen anchors forbid that color at three odd lines. Each of two
fifteen-cliques avoids fifteen and omits a unique color from the other
sixteen colors; their shared odd neighbor forces two adjacent lines to
receive the same omitted color. The combined certificate checks all 3,321
pairs on 82 vertices, including 1,066 edges. This is a written graph proof
with exact finite geometry verification, without SAT/DRAT or Lean. The
submitted manuscript remains at its linked revision for coauthor review
of this extension; no full-graph eighteen-coloring or chromatic equality
is claimed.

The [eighteen-color extension criterion](notes/eighteen-color-palettes.md)
now determines every odd-line list from the intersection of the omitted
color pairs of its fifteen incident Lagrangian cliques. Any extendible
even coloring has at most seven nonzero points with empty intersections,
and its intersections satisfy explicit odd-clique color constraints.
The finite check covers all 32,832 even/odd neighbor memberships. A
separate sufficient construction sought seventeen colors on the 442
lines and isotropic planes, reserving the eighteenth for all 135
independent triples. The line-capacity theorem below excludes that
construction; the general eighteen-color extension criterion remains valid.

The [442-vertex construction encoding](notes/lines-planes-seventeen-encoding.md)
is now emitted and audited: 427 residual vertices, 14,994 edges, 5,789
variables and 197,344 clauses. Its seven special lines retain three
color choices. One 120-second Glucose4 attempt returns unknown, with no
coloring or UNSAT proof. The subsequent written line obstruction excludes
this sufficient route. The later nineteen-color lower bound also excludes
eighteen colors on the full graph.

The [ternary special-line symmetry proof](notes/ternary-line-symmetry.md)
reduces all 2,187 three-color assignments to 32 representatives under
orthogonal lifts and the interchange of the two extra colors. Every
orbit is retained and every added clause audited, giving 199,499 clauses.
The reduction preserves auxiliary seventeen-colorability. A dedicated
[runner](develop/search_ternary_line_symmetry.py) now audits the entire
restricted formula before solving. One new 120-second Glucose4 attempt
returns [unknown](results/dimension-7-ternary-line-symmetry-search.json),
with no coloring, UNSAT proof or full-graph upper bound.

The [all14 branch reduction](notes/all14-special-line-branch.md) identifies
an independent dominating class of eight lines. That single orbit is
equivalent to sixteen-colorability of a 434-vertex induced graph, with
an exact omitted-pair list criterion on its 56 odd lines. Its 193900-clause
formula is checked against direct substitution in the base encoding.
The subsequent line-capacity obstruction excludes this branch and all
other 31 ternary orbits of the auxiliary seventeen-color construction.

The [odd-extension proof](notes/all14-odd-extension.md) determines the
56-vertex odd graph exactly: independence number seven and chromatic
number eight, with an explicit trace-field spread certificate. For a
fixed proper even coloring, its exact omitted-pair lists give a 2-SAT
extension test with at most 56 variables. These conditional statements
remain valid; the line obstruction excludes the full branch.

The [dimension-seven line-capacity proof](notes/dimension-seven-line-capacity.md)
first gave the lower bound eighteen already on the line graph. Every
independent line set avoiding the characteristic vector has at most
seven vertices, so the 126 lines with that vector deleted need at least
eighteen colors. A coordinate-only exhaustive check verifies the capacity
over all 26896 even color classes and 135 Lagrangians. This closes the
entire auxiliary seventeen-color route without a SAT/UNSAT or Lean run.
The [nineteen-color obstruction](notes/dimension-seven-nineteen-obstruction.md)
now rules out both saturated eighteen-color line structures. Nine even
heptads fail quadratic parity. The mixed structure leaves seven holes in
an eight-member partial Lagrangian spread; those holes form the ninth
Lagrangian, whose seven even points need seven labels but have only three.
This gives lower bound 19 for the line and full-subspace graphs, with
exact quadratic/heptad and incidence checks. Their exact values remain
open; no nineteen-color witness, native SAT or Lean result is claimed.

The [nineteen-color deficit analysis](notes/dimension-seven-nineteen-deficits.md)
now proves that deleting the characteristic line still leaves a graph
requiring at least nineteen colors. Any hypothetical nineteen-coloring
must put that line in a class of size three through eight; the other
eighteen classes have total size deficit exactly one less than that
class's size. The three two-point-class profiles retained in the earlier
analysis are now all excluded by a
[projected-sum and recoloring proof](notes/dimension-seven-characteristic-three.md).
The exact color-class count and pairing checks cover all 60,417 independent
six-point classes and 2,439 independent seven-point classes avoiding the
characteristic line; see the [certificate](results/dimension-7-characteristic-three.json).
A nineteen-color witness and the full graph's exact value remain open.

For a characteristic class of size three, the
[quadratic defect analysis](notes/dimension-seven-three-point-defects.md)
restricts the one-five-point-defect branch to three necessary count
profiles. Six of ten candidates fail quadratic parity and one fails
Lagrangian completion. The two-six-point-defect branch has a prescribed
pairing between its projected class sums and remains open. The
[finite certificate](results/dimension-7-three-point-defects.json) checks
the class identity on all independent five-point and six-point classes;
none of the surviving profiles is a constructed coloring.

The [completed-hole exclusion](notes/dimension-seven-hole-cover.md) now
rules out the profile (D even,odd; A,B,C)=(2,3;7,2,8). A written
symplectic normalization reduces it to 384 even-point exact-cover
instances, all excluded by an [independently audited finite certificate](results/dimension-7-hole-cover-check.json)
with 1,784 failed states. Only (0,5;3,7,7) and (1,4;2,8,7) remain in
the one-five-point-defect branch. The two-six-point-defect branch,
larger characteristic classes, and exact dimension-seven values remain
open; the numerical lower bound stays nineteen.

The [seven-Lagrangian completion lemma](notes/dimension-seven-seven-holes.md)
further excludes (0,5;3,7,7). All 1,792 seven-member partial spreads
containing a fixed Lagrangian match the deletion set of 64 independently
enumerated complete spreads, proving that their fourteen holes split
uniquely into two Lagrangians. The five odd defect points must lie in
one hole Lagrangian; the other then needs seven distinct even labels
but has only three. This left (1,4;2,8,7) in the one-five-defect
branch, with two necessary local forms recorded in the
[finite report](results/dimension-7-seven-holes.json).

The [seven-clique color budget](notes/dimension-seven-one-five-exclusion.md)
now excludes that final profile and closes the entire one-five-defect
branch for a three-point characteristic class. The four odd defect
projections occupy one hole Lagrangian; the other seven-point even
clique has at most two pure even, three mixed, and one defect label:
six labels for seven vertices. The two normalized local forms have
only six and four labels respectively, checked in the
[coordinate report](results/dimension-7-one-five-exclusion.json).
A nineteen-coloring with characteristic class size three must therefore
have two six-point defects and sixteen saturated outside classes.
That coupled branch, larger characteristic classes, and exact n=7
values remain open with numerical lower bound nineteen.

The [coupled two-six analysis](notes/dimension-seven-two-six-profiles.md)
reduces its 21 count profiles to three necessary candidates. All eleven
profiles with seven pure odd heptads are excluded by the two-hole point
capacity, charge membership, or clique label budget. With eight pure odd
heptads, only defect even counts (4,4) and saturated counts (7,1,8)
remain. The other candidates have six pure odd heptads: defect even
counts (0,0) with saturated counts (3,7,6), or (0,2) with (1,9,6).
The [coordinate report](results/dimension-7-two-six-profiles.json)
checks the count formulas and local charge/conditional-transfer controls.
Their joint realizability, larger characteristic classes, and exact n=7
values remain open; the lower bound is still nineteen.

The subsequent [four-four completed-hole exclusion](notes/dimension-seven-four-four-hole-cover.md)
rules out the final eight-pure-odd-heptad profile by a written symplectic
normalization and an independently audited finite exact-cover certificate.
All six normalized odd-projection configurations and 17,408 disjoint
partial triples are covered; 85,720 failed states and 70,672 outgoing
branches are checked from independently reconstructed class catalogs.
The [certificate](results/dimension-7-four-four-hole-cover-certificate.json)
and [audit report](results/dimension-7-four-four-hole-cover.json) leave
only the two six-pure-odd-heptad count candidates above. Their common
coloring realizability remains open. No six-Lagrangian completion,
entire size-three branch exclusion or numerical-bound improvement is claimed.

The subsequent [six-Lagrangian completion and recoloring theorem](notes/dimension-seven-six-holes.md)
excludes the last two candidates and the entire characteristic-size-three
branch. Independent original-vector/RREF Lagrangian catalogs and
bitmask/array enumerations check all 3,584 six-member partial spreads
containing a fixed member. Each leaves exactly three disjoint hole
Lagrangians, uniquely. A pure odd six-point defect lies in one of them;
moving its missing odd point into the defect yields a previously excluded
characteristic-size-two, C=7 two-six, or one-five configuration.
The [finite report](results/dimension-7-six-holes.json) binds the proof
and dependencies. Any nineteen-coloring must now give the characteristic
vector a class of size **four through eight**. Those sizes and the exact
dimension-seven chromatic numbers remain open; the numerical lower bound
stays nineteen. The preceding entries record the earlier intermediate bounds.

The [size-four deficit and charge analysis](notes/dimension-seven-size-four.md)
derives the outside defect-size patterns 4, 5+6 and 6+6+6, together
with their common-partition projection and quadratic charge equations.
For the single-four-point-defect branch, eight of nine count profiles
are excluded; only defect type (2 even,2 odd) with saturated counts
(7,2,8) remains necessary and unrealized. Its characteristic projections
must form a basis of the completed hole Lagrangian. The
[report](results/dimension-7-size-four.json) checks the counts and
1,008 local charge configurations. The 5+6 and 6+6+6 branches have
46 and 48 raw count profiles before their charge/common-coloring
feasibility is examined. The full size-four branch, larger sizes,
and exact n=7 values remain open with numerical lower bound nineteen.

## Paper status

The manuscript has been submitted to the **Journal of Algebraic Combinatorics**.
Reza also submitted it to arXiv, which declined it at moderation; no permanent
arXiv identifier or announcement was issued. Posting the current submitted
version on Zenodo was completed by Reza on October 7, 2026:
[10.5281/zenodo.23210092](https://doi.org/10.5281/zenodo.23210092).
The public record lists Haobo Ma, Reza Nikandish and Wenlin Zhang.
Its PDF has a revised abstract and additional declarations relative to
repository snapshot `28e27a8`; the matching submission source is awaiting
synchronization. The extracted text of Sections 1–7 agrees after accounting
for whitespace, page breaks and PDF glyph extraction differences.
This preprint does not include the subsequent dimension-seven research notes.
Any arXiv appeal
must follow the rejection letter's journal-acceptance condition. Submission
is not acceptance. Reza is the corresponding author.

The originating problem is Reza Nikandish, *Annihilating-Ideal Graphs and
Orthogonality Graphs over F_2*,
[arXiv:2609.22769v1](https://arxiv.org/abs/2609.22769v1).
The joint paper distinguishes those prior constructions from its new proofs
and certificates.

The [single-four-defect exclusion](notes/dimension-seven-single-four-exclusion.md)
now closes that entire outside-defect pattern for characteristic size four.
A universal symplectic normalization of the covering data, checked on all
1,008 fixed-hole local configurations, reduces the last profile to the
existing 384-root finite certificate. Its 1,784 failed states and 1,400
branches are reaudited in the [report](results/dimension-7-single-four-exclusion.json).
The size-four patterns 5+6 and 6+6+6 remain open with 46 and 48 raw
count profiles; characteristic sizes four through eight and exact n=7
remain open, with lower bound nineteen and no nineteen-color witness.

The [four-odd affine-plane argument](notes/dimension-seven-five-six-affine.md)
now excludes two size-four 5+6 profiles, (k5,k6;A,B,C)=(5,2;8,0,8)
and (1,6;8,0,8). Their characteristic charge must be zero, contradicting
the required quadratic charge product one. The [report](results/dimension-7-five-six-affine.json)
checks 168 local partial classes. The other 44 raw 5+6 profiles and
all 48 raw 6+6+6 profiles remain untested for joint feasibility.
Characteristic sizes four through eight and exact n=7 remain open,
with numerical lower bound nineteen.

The [three-plus-one odd-split exclusion](notes/dimension-seven-five-six-split31.md)
now also rules out (k5,k6;A,B,C)=(2,5;8,0,8). Its five-point defect
charge lies in the completed hole Lagrangian; the common partition
would force the six-point charge there too, contradicting its pairing
with its odd member. The [report](results/dimension-7-five-six-split31.json)
checks the local defect catalogs and all 1,792 conditional charge joins.
At that stage three of the 46 raw 5+6 profiles were excluded.

The [uniform hole-capacity theorem](notes/dimension-seven-hole-capacity.md)
now excludes twelve further 5+6 and nine 6+6+6 profiles in one argument.
If P counts pure even defects and R counts mixed defects, seven hole points
require A+P>=7 when C=8, while fourteen require 2A+B+2P+R>=14 when C=7.
The C=8 exclusions use written eight-spread completion; the C=7 exclusions
retain the existing finite seven-spread completion dependency.
The [report](results/dimension-7-hole-capacity.json) preserves all remaining
rows: at that stage fifteen of 46 raw 5+6 profiles and nine of 48 raw 6+6+6
profiles were excluded. This is a written capacity theorem with small coordinate and count
controls, without a new spread enumeration or covering search.
Characteristic sizes four through eight and exact n7 remain open >=19.

The [common-even-sum analysis](notes/dimension-seven-five-six-cover.md)
now excludes (2,6;7,1,8) by reducing it to the existing checked 384-root
hole-cover certificate. Its pure even six-point defect has completion
charge r+b in M, so it contains no even hole points; seven anchored heptads
and the two forced six-clique sums normalize to the certificate's data.
Both six-class role assignments and zero/nonzero characteristic charge
are retained. The same note gives a uniform written parity test closing
all four C=8,B=0 raw rows, newly excluding (3,4;8,0,8).
The [report](results/dimension-7-five-six-cover.json) rechecks the existing
cover without a new search and records both proof scopes. At that stage
seventeen of 46 raw 5+6 and nine of 48 raw 6+6+6 profiles were excluded. Characteristic
sizes four through eight and exact n7 remain open >=19, with no new Lean claim.

The [three-plus-five even-cover theorem](notes/dimension-seven-three-five-cover.md)
now excludes (3,5;7,1,8). Charge parity forces the four remaining odd
projections into an affine plane, so h=0 follows. A written symplectic basis
normalizes their class roles and the two even sums to 95 and 96. The necessary
cover has 400 roots, each requiring seven heptads anchored in the hole space.
A new bounded search produces a [failed-state certificate](results/dimension-7-three-five-cover-proof.json),
and its [independent audit](results/dimension-7-three-five-cover-check.json)
checks every root and branch of all 2,004 states. This is a written reduction
plus a checked finite cover proof, with no Lean claim. At that stage eighteen of 46 raw 5+6
and nine of 48 raw 6+6+6 profiles are excluded; the other 28 and 39 remain
unexcluded with joint feasibility untested. Sizes four through eight and
exact n7 remain open, with lower bound nineteen.
Characteristic sizes four through eight and exact n=7 remain open,
with numerical lower bound nineteen.

The [four-even-pairs theorem](notes/dimension-seven-four-even-pairs.md)
newly excludes (4,4;7,1,8). Written charge forces both four-even sums
into the hole Lagrangian, and a nondegenerate-span argument makes one
six-defect odd projection equal its even sum. Valid odd-point transfers
reduce all cases to the earlier audited size-three two-six theorem or
one universal size-four normal form with nonzero characteristic charge.
Its new [bounded builder](develop/build_dimension_seven_four_even_pairs.py)
and [independent auditor](develop/check_dimension_seven_four_even_pairs.py)
check a [certificate](results/dimension-7-four-even-pairs-proof.json)
with 18,752 ordered roots, 18,656 distinct root states and 72,384 failed
states. The [report](results/dimension-7-four-even-pairs-check.json)
retains the separately reaudited earlier certificate as an explicit
recoloring dependency. Nineteen of 46 raw 5+6 and nine of 48 raw
6+6+6 profiles are excluded; 27 and 39 remain unexcluded with joint
feasibility untested. Sizes four through eight and exact n7 remain
open >=19, with no new Lean or numerical bound claim.

The [pure-five/four-even charge reduction](notes/dimension-seven-five-four-charge.md)
now reduces the still-open (5,4;6,2,8) profile to four necessary marked
normal forms. Applying the existing charge-member lemma forces both
even sums into the hole Lagrangian, including the apparent dependent-span
exception. The pure-five sum may be zero; its hole point and the six
pure even heptads occupy the seven holes once each. The
[independent checker](develop/check_dimension_seven_five_four_charge.py)
and [report](results/dimension-7-five-four-charge.json) verify all 420
fixed-hole role normalizations and exact local defect catalogs. These
are necessary partial classes; no six-heptad cover search, coloring or
new profile exclusion is claimed. The totals remain 19/46 five-plus-six
and 9/48 three-six profiles excluded, with 27/39 unexcluded and exact
n7 open >=19.

The subsequent [D-form covering theorem](notes/dimension-seven-five-four-D-cover.md)
excludes the nonzero six-defect characteristic-charge normal form of
(5,4;6,2,8). Adding both mixed sextets gives 62,976 ordered roots,
with 54,448 distinct 42-point sets, retaining the actual pure-five
hole in every root. The [bounded builder](develop/build_dimension_seven_five_four_D_cover.py)
and [independent auditor](develop/check_dimension_seven_five_four_D_cover.py)
produce and check a new [six-heptad certificate](results/dimension-7-five-four-D-cover-proof.json).
Its [report](results/dimension-7-five-four-D-cover-check.json) verifies
72,576 reachable failed states and every branch. The earlier seven-heptad
certificates are not inputs. At that stage D was excluded and Z,H,G
remained open, with unchanged raw-profile totals of 27/39 unexcluded.
Exact n7 stays open >=19, with no new Lean or numerical bound claim.

The new [H-form covering theorem](notes/dimension-seven-five-four-H-cover.md)
excludes zero characteristic charge for this same (5,4;6,2,8) profile.
Retaining both mixed classes and every actual pure-five hole gives
127,680 ordered roots and 126,336 distinct 42-point sets. Its
[bounded builder](develop/build_dimension_seven_five_four_H_cover.py)
and [independent auditor](develop/check_dimension_seven_five_four_H_cover.py)
produce and check a new [six-heptad certificate](results/dimension-7-five-four-H-cover-proof.json).
The [report](results/dimension-7-five-four-H-cover-check.json) verifies
186,584 reachable failed states, 60,904 branches and 128,880 leaves.
Neither the D certificate nor earlier seven-heptad certificates are
proof inputs to H. D and H are excluded; Z and G remain open, so
the raw profile and totals of 27/39 unexcluded profiles remain unchanged.
Exact n7 remains open >=19; no new Lean or numerical bound is claimed.

The [G-form root and stabilizer reduction](notes/dimension-seven-five-four-G-roots.md)
retains the actual pure-five hole and both mixed classes. Two independent
catalog constructions give 129,280 ordered roots and 127,984 distinct
42-point remaining sets. A written pointwise-hole symplectic group of
order 64 reduces the latter to 2,306 orbit representatives. The
[checker](develop/check_dimension_seven_five_four_G_roots.py) and
[report](results/dimension-7-five-four-G-roots.json) verify all maps,
catalog invariance and the complete orbit partition. That preparatory
report supplies no covering exclusion; the subsequent proof is below.

The subsequent [G-form covering theorem](notes/dimension-seven-five-four-G-cover.md)
excludes all 2,306 representatives with a new independently audited
[certificate](results/dimension-7-five-four-G-cover-proof.json).
The [auditor](develop/check_dimension_seven_five_four_G_cover.py) checks
3,351 reachable failed states, all 1,045 branches and 2,401 leaves;
three invalid controls are rejected. Thus D/H/G are excluded and only
the zero-five-even-sum form Z remains for this raw profile. The profile
and 27/39 count totals remain open. This new finite proof is integrated
into the extended working draft; exact n7 remains open >=19.

The [Z-form root and marked stabilizer reduction](notes/dimension-seven-five-four-Z-roots.md)
now constructs 1,284,736 ordered roots and 1,271,424 distinct remaining
sets. Its written 128-element symplectic stabilizer includes exchange of
the two mixed classes and transports the actual pure-five hole, reducing
the family to 10,837 representatives. The
[checker](develop/check_dimension_seven_five_four_Z_roots.py) and
[complete report](results/dimension-7-five-four-Z-roots.json) independently
reconstruct the catalogs and root multiset and verify the full orbit
partition. No representative is solved in this step; Z, the raw profile
and exact n7 remain open >=19. Both manuscript PDFs are preserved.

The subsequent [Z covering theorem](notes/dimension-seven-five-four-Z-cover.md)
excludes all 10,837 representatives with a new independently audited
[certificate](results/dimension-7-five-four-Z-cover-proof.json). The
[auditor](develop/check_dimension_seven_five_four_Z_cover.py) verifies
14,337 reachable failed states, all 3,517 branches and 10,995 leaves;
three invalid controls are rejected. Together with the exhaustive
four-form reduction and separate D/H/G exclusions, this closes the raw
profile `(5,4;6,2,8)`. The [report](results/dimension-7-five-four-Z-cover-check.json)
reconstructs the parity-count catalogs and removes exactly this row,
leaving 26 five-plus-six and 39 three-six count candidates. The extended
working draft includes the result; exact n7 remains open >=19.

The [three-even/pure-six charge reduction](notes/dimension-seven-three-six-charge.md)
derives three exhaustive marked forms for `(3,6;6,2,8)`, the only
remaining five-plus-six count row with eight pure odd heptads. The
five-defect even sum lies outside the hole Lagrangian; the pure-six
defect contains exactly one actual hole. The full marked stabilizers
have orders 32,32,16 and retain two distinct hole orbits in each form.
The [checker](develop/check_dimension_seven_three_six_charge.py) and
[local audit report](results/dimension-7-three-six-charge.json) verify
1,344 explicit normalizations and all catalog/group actions. Each
form has four even triples, 24 pure-six blocks and 32 mixed sextets
per role; disjoint defect-pair counts are 96,96,72. No complete root
family or cover search is performed: this row, 26/39 count totals and
exact n7 remain open >=19. Both manuscript PDFs are preserved.

The subsequent [three-form root reduction](notes/dimension-seven-three-six-roots.md)
constructs every necessary remaining set with both mixed roles and
the actual pure-six hole retained. Forms I/II/III have 7,424/12,688/8,160
ordered roots and 7,408/12,688/8,112 distinct sets, reduced under their
proved full marked groups to 248/474/557 representatives. Each form
retains both actual-hole orbits; the actions are not free and no
cross-form identification is assumed. The
[checker](develop/check_dimension_seven_three_six_roots.py) and
[complete representative report](results/dimension-7-three-six-roots.json)
verify two independent catalog/root constructions, all group actions
and every orbit. No cover search or exclusion is performed; the
26/39 count totals and exact n7 remain open >=19. Both PDFs are preserved.

The [three-even/pure-six covering theorem](notes/dimension-seven-three-six-cover.md)
excludes all three marked forms of `(3,6;6,2,8)` with a new
[certificate](results/dimension-7-three-six-cover-proof.json).
The [auditor](develop/check_dimension_seven_three_six_cover.py) reconstructs
the complete roots and orbit partitions, then verifies all 248/474/557
representatives, 1,949 reachable failed states, 676 branches and 1,332
leaves. Three invalid controls are rejected. The
[report](results/dimension-7-three-six-cover-check.json) removes exactly
this raw row from the preceding lists, leaving 25 five-plus-six and
39 three-six candidates. No five-plus-six C=8 row remains; five
three-six C=8 rows remain. The extended draft incorporates this
partial result; exact n7 remains open >=19.

The earlier [profile-scope analysis](notes/dimension-seven-profile-scope.md)
gives common deficit, count, charge and hole-capacity formulas across
characteristic sizes. Its [accounting auditor](develop/check_dimension_seven_profile_scope.py)
and [report](results/dimension-7-profile-scope.json) verify that the
27/39 remaining count candidates all have characteristic size four.
All 64 candidates with six through eight pure odd heptads already
satisfy the applicable uniform hole-capacity bound; two have five.
Sizes five through eight require additional branches. No uniform
exclusion of the remaining family or completion-time estimate is
established; the completed lower bound 19 is independent of this work.
Its archived 27/39 totals predate the Z exclusion; the new Z covering
report retains its updated complete lists with totals 26/39; the new
three-even/pure-six covering report records the subsequent 25/39 lists.

## Repository map

- [Manuscript](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/paper.tex): the complete joint paper.
- [Proof notes](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/notes/dimension-six.md): readable arguments and dated exploration.
- [Certificates](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/results/full-15-coloring.json): explicit witnesses and check records.
- [Checkers](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/develop/check_full_coloring.py): independent Python verification.
- [Formal sources](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/formal/Chromatic/Verify.lean): attributed clique source and chromatic development.
- [Rights and provenance](RIGHTS.md): source attribution and applicable license information.

For follow-up discussion, use [PR #1](https://github.com/the-omega-institute/binary-subspace-orthogonality/pull/1)
for this paper and the [new repository](https://github.com/the-omega-institute/ideal-intersection-laplacian)
for the Laplacian project.
