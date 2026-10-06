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
| Read or edit the manuscript source | [LaTeX source](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/paper.tex) · [current collaboration PR](https://github.com/the-omega-institute/binary-subspace-orthogonality/pull/1) |
| Understand the main results and their evidence | The results table below |
| Reproduce the finite checks | [Reproduction guide](docs/REPRODUCING.md) |
| Explore the geometric arguments | [Geometry section](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/sections/geometry.tex) |
| Follow our next collaboration | [Ideal-intersection Laplacian project](https://github.com/the-omega-institute/ideal-intersection-laplacian) |

The paper links identify the submitted source revision, `28e27a8`.
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
| The full dimension-seven graph requires **at least 17 colors**, exceeding its clique number 16 | [Two-clique forcing proof](notes/dimension-seven-obstruction.md) and [29-vertex certificate](results/dimension-7-obstruction.json); exact full-graph chromatic number remains open |
| Specified geometric profiles and stabilizer-equivariant rules cannot explain a proper coloring with the prescribed clique labels | [Precise statements and proofs](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/manuscript/sections/geometry.tex) |

The six-dimensional [chromatic Lean development](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/formal/Chromatic/Verify.lean)
has a successful historical build. Its final theorem uses the three standard
axioms (`propext`, `Classical.choice`, `Quot.sound`) **and four native-evaluation
axioms**. See the [verification audit](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/28e27a82068a2f9129fdb5d168bd0fc179cf3e48/notes/formal-verification-audit.md)
for the exact dependencies. A completed pure-kernel replacement is not claimed.
The independent finite checks and the written mathematical proofs have their
own stated scopes.

**The dimension-seven chromatic number remains open.** A complete structural
15-color rule also remains open. Failed exploratory candidates are retained as
research history; they are not proofs of upper bounds.

The [new 29-vertex obstruction](notes/dimension-seven-obstruction.md) proves
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
full-span orthogonality. The other nine patterns remain required.

## Paper status

The manuscript has been submitted to the **Journal of Algebraic Combinatorics**.
Reza also submitted it to arXiv, which declined it at moderation; no permanent
arXiv identifier or announcement was issued. Posting the current submitted
version on Zenodo is authorized, with Reza handling the upload; its DOI is
awaiting confirmation. Any arXiv appeal
must follow the rejection letter's journal-acceptance condition. Submission
is not acceptance. Reza is the corresponding author.

The originating problem is Reza Nikandish, *Annihilating-Ideal Graphs and
Orthogonality Graphs over F_2*,
[arXiv:2609.22769v1](https://arxiv.org/abs/2609.22769v1).
The joint paper distinguishes those prior constructions from its new proofs
and certificates.

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
