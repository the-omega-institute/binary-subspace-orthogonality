# The dimension-seven line graph already requires eighteen colors

**Theorem.** Let Gamma_7 have the 127 nonzero vectors of F_2^7 as
vertices, adjacent when distinct vectors have dot product zero.
Every independent set avoiding z=(1,...,1)=127 has at most seven
vertices. Therefore chi(Gamma_7)>=18, already on the induced graph
with z deleted.

This closes the auxiliary seventeen-color route on all 127 lines
and 315 totally isotropic planes, including all 32 ternary orbits.
In particular the all14 branch is impossible. The full-subspace
n=7 chromatic number remains open with the same lower bound eighteen;
no full-graph eighteen-color witness or stronger lower bound is claimed.

## A color-class capacity proof

An independent line set has dot product one between every pair of
distinct vectors. Let m of its vectors have even weight, and o odd
weight. Write E=z-perp, a nondegenerate alternating six-space.

If o=0, the Gram matrix on the even vectors is J_m+I_m. Its rank is
m for even m and m-1 for odd m: a kernel vector must have all entries
equal to their sum. Its rank cannot exceed six, so m<=7.

Suppose o>0, and fix one selected odd vector a. For each selected
even vector u, put b_u=u+a. Then

```text
a dot b_u = 0,       b_u dot b_u = 1,
b_u dot b_v = 0 for u != v.
```

Since a dot a=1, the space a-perp is nondegenerate of dimension six.
The m vectors b_u are orthonormal and span a nondegenerate subspace B
of dimension m. Thus m<=6. The space

```text
V = B-perp intersect a-perp
```

is nondegenerate of dimension 6-m. Let D be the span of w+a over
all selected odd vectors w. Pairwise products one imply that D is
totally isotropic and lies in V: each generator is orthogonal to a
and every b_u, and all generators are mutually orthogonal, including
themselves. Hence 2 dim(D)<=6-m. The selected odd vectors lie in
a+D, so

```text
o <= 2^floor((6-m)/2).
```

For m>=1 the resulting capacities are:

| Even lines m | Maximum odd lines o | Maximum total m+o |
| --- | --- | --- |
| 1 | 4 | 5 |
| 2 | 4 | 6 |
| 3 | 2 | 5 |
| 4 | 2 | 6 |
| 5 | 1 | 6 |
| 6 | 1 | 7 |

These give at most seven vertices whenever an even vector is selected.
This is the dimension-seven specialization of the orthonormal/affine
argument used for the [dimension-six line bound](line-coloring.md).

It remains to consider m=0. Write each selected odd vector as z+e,
with e in E. Pairwise products one are equivalent to pairwise
orthogonality of the e. Their span W is totally isotropic in E,
so dim(W)<=3. If there were eight selected odd vectors, their eight
distinct e would fill W, necessarily including zero. The selected
set would therefore contain z. An independent set avoiding z has
at most seven odd vertices as well. This proves the theorem.

Deleting z leaves 126 vertices, each color class of size at most
seven. Thus chi(Gamma_7-z)>=ceil(126/7)=18, and the same lower bound
holds for Gamma_7 and for the full-subspace graph.

## Consequences for the recorded auxiliary route

The auxiliary graph G on 127 lines and 315 totally isotropic planes
contains Gamma_7 as an induced subgraph. It therefore cannot have
seventeen colors, regardless of the normalized special-line pattern.
The original 197344-clause encoding, the 199499-clause ternary symmetry
encoding, and all 32 retained orbits describe an impossible sufficient
construction. This conclusion is a written graph obstruction; no SAT
solver reported UNSAT and no DRAT proof was obtained or checked.
Historical unknown solver reports retain their input identities and
remain accurate accounts of those earlier bounded runs.

There is also a direct all14 obstruction. Its class S consists of eight
odd lines and contains z. The remaining induced graph H contains 119
lines, all avoiding z, so those lines alone need ceil(119/7)=17 colors.
The [all14 reduction](all14-special-line-branch.md) requires all of H
to have sixteen colors. It is therefore impossible, without assuming
an even coloring or assigning hypothetical omitted pairs. The earlier
[eight-color odd graph and 2-SAT analysis](all14-odd-extension.md) remains
valid as conditional mathematics, but cannot produce a compatible
sixteen-coloring of H. Consequently, for every proper sixteen-coloring
of its even vertices, either an exact odd list is empty or the associated
2-SAT implication graph has a variable mutually reachable with its
negation. This is a universal conditional obstruction; it does not assert
existence of an even coloring or supply a concrete implication cycle.

This rules out assigning a fresh eighteenth color to all 135 isotropic
three-spaces after seventeen-coloring G. It does not rule out an
eighteen-coloring of the full graph in which those three-spaces share
colors with other vertices. Nor does it establish an eighteen-color
line or auxiliary coloring. All three chromatic numbers have the
written lower bound eighteen; their exact values are not computed here.

## Saturation required by an eighteen-color line coloring

If an eighteen-coloring of Gamma_7 exists, one color class must have
eight vertices, because 18*7=126<127. The proof shows that it consists
of the eight odd vectors z+L for one Lagrangian L in E; it contains z.
All other seventeen classes then have exactly seven vertices. A
symplectic change of basis on E, extended by fixing z, can send L to T:
choose a basis and dual basis for each Lagrangian to construct the map.
Thus the eight-line class can be normalized to S.

The capacity table leaves only three types for the other seven-vertex
classes: seven even lines, six even and one odd line, or seven odd lines.
Let their numbers be A, B, C respectively. Counting the remaining 63
even and 56 odd lines gives

```text
7A+6B=63,       B+7C=56,       A+B+C=17.
```

There are exactly two nonnegative integer possibilities:

| Seven even A | Six even + one odd B | Seven odd C |
| --- | --- | --- |
| 9 | 0 | 8 |
| 3 | 7 | 7 |

In a mixed class with even vectors u_1,...,u_6, these vectors form a
basis of E: their Gram matrix J_6+I_6 is invertible. The common odd
vector is forced to be z+(u_1+...+u_6), since its even point must pair
to one with each u_i. The sum itself completes the six even points to
a pairwise nonorthogonal seven-point set. This is a concrete constraint
on the mixed-type partition, not a construction of one.

Every color in a hypothetical full-subspace eighteen-coloring is
therefore already used on the lines. The isotropic three-spaces must
share these labels; a fresh common label is unavailable. Determining
whether either saturated line partition exists, and whether it extends
over the other retained subspaces using the same eighteen labels,
is the next structural problem. Neither existence nor nonexistence
of those partitions is established here.

## An exhaustive finite check of the capacity lemma

The [standard-library checker](../develop/check_dimension_seven_line_capacity.py)
uses coordinate dot products, without repository geometry or SAT helpers.
It enumerates all 26896 possible even-line color classes, including
the empty class, as cliques for dot product one on the 63 nonzero
points of E. Their cardinality counts are:

```text
m             0    1     2     3      4     5     6    7
classes       1   63  1008  5376  10080  8064  2016  288
```

For an even class Q, an odd line z+e can share its color exactly when
e dot u=1 for every u in Q. The checker obtains this entire affine
availability set by direct dot products. Any independently selected
odd points lie in an isotropic subspace of E, hence in one of its 135
Lagrangians. Conversely, any subset of one Lagrangian has pairwise
orthogonal points. Thus the largest possible odd part equals

```text
max over Lagrangians L of |A(Q) intersect L intersect domain|,
```

where domain is E without zero for deleting z, or E outside T for
the all14 line graph. All these intersections are checked, not merely
sampled. The maxima by m are (7,4,4,2,2,1,1,0) in both domains, and
the maximum total class size is seven. The unrestricted pure odd
maximum is eight; every attaining Lagrangian contains zero, confirming
the exceptional role of z.

The checker independently constructs the 135 Lagrangians by all
isotropic independent triples. It also checks the complete line-edge
sets: Gamma_7 has 3969 edges, deleting z leaves 3906, and the all14
119-line graph has 3465. The [certificate](../results/dimension-7-line-capacity.json)
includes witnesses for all eight capacity rows and the exhaustive
histograms, with source/note hashes. This finite check supports the
written proof; it is not a solver or Lean certificate.

```sh
python3 develop/check_dimension_seven_line_capacity.py --report /tmp/dimension-7-line-capacity.json
```

The submitted manuscript at 28e27a8 is unchanged. The historical
dimension-six Lean theorem retains three standard and four
native-evaluation axioms. No native SAT or Lean was run for this result.
