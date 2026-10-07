# Retaining only lines and totally isotropic subspaces

For the standard dot product on F_2^n, let O_n* have every nonzero
subspace as a vertex, with distinct vertices adjacent exactly when they
are orthogonal. Let S_n be the induced graph retaining every line and
every totally isotropic subspace. Here total isotropy means that the
bilinear form vanishes on every pair of vectors in the subspace.

**Theorem.** There is a graph retraction O_n* -> S_n, and hence

```text
chi(O_n*) = chi(S_n).
```

This strengthens the [earlier retraction](subspace-retraction.md), which
also retained every plane in the even-parity hyperplane. In dimension
seven it reduces the graph from 29,211 vertices to 577 vertices. The
known lower bound chi(O_7*) >= 17 remains valid; the exact chromatic
number remains open.

The subsequent [seventeen-color encoding audit](seventeen-color-encoding.md)
records one bounded unknown solver attempt and an equally complete
characteristic-clique normalization with fewer encoding variables.
The counts in this reduction note describe its original fixed-line choice.

## The nonradical-line choice

Put rad(U)=U intersect U-perp. Keep every vertex of S_n fixed. For any
other vertex U, choose a vector v in U outside rad(U) and set
q(U)=span(v). Such a vector exists because U is not totally isotropic.
The image is a retained line, is contained in U, and satisfies

```text
U is not perpendicular to q(U).
```

For a deterministic implementation, inspect the basis Gram matrix and
choose the least basis vector whose row is nonzero. This basis vector
is not orthogonal to U. A nonzero Gram matrix always has such a row.

If distinct U and V are orthogonal, containment gives q(U) perpendicular
to q(V). Their images cannot coincide. If U moved and their common image
were W, then W=q(U) would be contained in V, which is contained in
U-perp. This contradicts the displayed nonorthogonality condition. The
same argument applies if V moved. If neither moved, equal images would
give U=V. Thus every edge maps to an edge and every target vertex is
fixed. Restricting a coloring and composing it with q prove the stated
chromatic equality.

The image line may be isotropic. The crucial condition is that it is
not in the radical of its source. An arbitrary contained line is
insufficient: span(3) and span(3,4) are distinct adjacent vertices, and
mapping the latter to span(3) would collapse their edge. Its radical
contains 3, whereas 4 is nonradical; the implemented choice is span(4).

## Seven-dimensional counts and complete edge checks

The even-parity hyperplane in F_2^7 is a nondegenerate six-dimensional
alternating space. Its totally isotropic subspaces have dimension at
most three. There are 315 totally isotropic planes and 135 totally
isotropic three-spaces, counted by ordered bases:

```text
315 = (63*30)/(3*2),
135 = (63*30*12)/(7*6*4).
```

Together with all 127 lines, this gives 577 retained vertices. The
induced graph has 19,539 edges. All 166,176 retained vertex pairs are
tested directly by basis dot products.

The [checker](../develop/check_nonradical_retraction.py) checks every
image of the 29,211 original vertices, including containment, fixed
target vertices and the nonradical condition for every moved vertex.
For each original vertex U it constructs U-perp from ambient vectors,
enumerates every nonzero subspace of that complement, and checks every
original edge once. It verifies that its two images are distinct and
adjacent in the directly constructed retained graph. Thus it checks
**all 1,160,206 original edges**, including 187,960 edges incident to
dimensions at least four; it does not scan every original vertex pair.

Completeness is also checked by the independent degree formula

```text
degree(U) = N(n-dim(U)) - 1 if U is totally isotropic,
            N(n-dim(U))     otherwise,
```

where N(r) counts the nonzero subspaces of F_2^r. The subtraction removes
the possible self-loop. Gaussian coefficients are computed by their
product formula, separately from the shared basis enumerator. The
degree sum is 2,320,412, twice the enumerated edge count. The checker
shares the canonical RREF basis enumeration and span helper with the
previous construction; its original-edge and retained-adjacency loops
are new. The [exact report](../results/dimension-7-nonradical-retraction.json)
binds both sources by SHA256.

## The seventeen-color problem uses different lists

Fix colors zero through fourteen on the nonzero subspaces of
T=span(3,12,48), and color fifteen on span(64). This is a sixteen-clique.
Any coloring with at most seventeen colors can be relabeled to use
these labels on the clique, leaving color sixteen as the extra label.
Remove only these sixteen fixed vertices. There remain **561 vertices**:
119 lines, 308 totally isotropic planes and 134 totally isotropic
three-spaces, with 18,056 edges between them.

For an uncolored U, its list contains precisely:

```text
the labels of nonzero W<=T that are not perpendicular to U;
color15 if span(64) is not perpendicular to U;
color16 in every case.
```

Each list is checked both by fixed-neighbor exclusion and by this
geometric formula. The palette-size counts are

| List size | Vertices |
| ---: | ---: |
| 2 | 7 |
| 12 | 98 |
| 13 | 112 |
| 15 | 40 |
| 16 | 240 |
| 17 | 64 |

The seven lines that were forced to color fifteen in the sixteen-color
problem have the two-color list {15,16} in this original seventeen-color
encoding. The old propagation alone does not justify preassigning them.
The subsequent [clique-triangle proof](forced-seven-line-color.md)
separately forces color fifteen in the characteristic-vector normalization,
while preserving the extra color sixteen in every residual list.
No singleton assignment is made in the original instance recorded here.
Its pairwise encoding would
have 8,174 variables and 257,402 clauses. These are exact counts for
the described encoding; no DIMACS file or solver run is claimed here.

For comparison, the old sixteen-color restrictions on S_7 give 554
uncolored vertices, 16,730 edges, 7,190 variables and 217,862 clauses.
That instance is uncolorable by the [written obstruction](dimension-seven-obstruction.md).
Its 554-vertex count does not describe the seventeen-color task.

## Six-dimensional control and reproduction

The retained graph in dimension six has 153 vertices: 63 lines, 75
totally isotropic planes and 15 totally isotropic three-spaces. To count
the planes, the even-parity hyperplane has one-dimensional radical and
a four-dimensional symplectic quotient. Fifteen planes contain the
radical, and each of the quotient's fifteen isotropic planes has four
complements to the radical in its preimage, giving 15+15*4=75. Its
maximal totally isotropic three-spaces are the fifteen such preimages.

Every image and all 44,968 original edges are checked, including 2,667
edges incident to higher dimensions. The existing fifteen-color
certificate restricts to a proper coloring on the retained graph's
2,611 edges. This checks a retained-graph positive control, without
rerunning or replacing the historical full-graph coloring certificate.
See the [six-dimensional report](../results/dimension-6-nonradical-retraction.json).

```sh
python3 develop/check_nonradical_retraction.py --dimension 6 --report /tmp/nonradical-n6.json
python3 develop/check_nonradical_retraction.py --dimension 7 --report /tmp/nonradical-n7.json
```

The written theorem holds in every dimension; these finite checks cover
dimensions six and seven. They do not supply a seventeen-coloring of
the full seven-dimensional graph or its exact chromatic number. No SAT,
UNSAT solver or Lean run is part of this step. The original dimension-six
formal theorem retains three standard and four native-evaluation axioms.
