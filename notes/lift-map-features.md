# Lift rank, image and kernel: partial refinement and a coloring obstruction

Let T=span(3,12,48) and S=span(1,4,16), using the existing binary integer
coordinates. For a vertex U outside the clique, put K=U intersect T,
P=pi_S(U), and f:P -> T/K as in the
[projection argument](complement-projection.md).

## Requested diagnostic and corrections

The script added in `409f379d5a9a45d824f560167784d13c34985490`
initially failed when serializing quotient-image cosets as frozensets.
It also skipped the zero vector: for K=0 this omitted f(0) and zero from P,
so the cardinalities used for dimension and rank were not powers of two.
The corrected script includes zero and exports each coset as a sorted vector
list. Its intended feature tuple is retained. Run:

```sh
python3 develop/lift_map_matrix.py
python3 develop/check_lift_map_features.py
```

The [requested output](../results/lift-map-matrix.json) gives 878 profiles,
578 single-color and 300 multi-color. This partition uses dim K, dim P,
rank f, image cosets and the exact kernel; it does not retain the exact P.
Indeed 294 of its groups contain vertices from more than one original group.
An image represented by its full quotient cosets implicitly retains K,
as its zero coset. The requested partition is not a refinement of (K,P).

For a valid refinement comparison, retain K and P and then add the features:

| Partition | Groups | Single-color | Multi-color | Vertices in multi-color groups | Minimum disagreements with fixed witness |
| --- | ---: | ---: | ---: | ---: | ---: |
| Exact (K,P), equivalent to (dim U,H,K) | 240 | 101 | 139 | 2288 | 1133 |
| Requested feature tuple | 878 | 578 | 300 | 1967 | 993 |
| Exact (K,P) plus rank, image and kernel | 1662 | 1502 | 160 | 1122 | 492 |

Here a disagreement count is the sum, over groups, of group size minus the
largest color multiplicity. It measures the best group-constant approximation
to this fixed witness, not the validity of a new coloring. Of the original
139 multi-color groups, 87 split entirely into single-color groups and 52
retain at least one multi-color subgroup. Multi-color group counts alone
are not monotone under refinement: one mixed group can split into several.
The independent checker reproduces the entire requested JSON, checks feature
tuples, linearity and rank--nullity on all 2809 non-clique vertices, and verifies
that retaining the full lift map with K and P gives 2809 distinct vertices.
That last fact is a full representation, not a structural 15-color rule.

## Written obstruction, independent of certificate colors

**Proposition.** No proper coloring of O_6* depends solely on K, P,
rank f, image f and kernel f for this T and S.

**Proof.** Take U=span(13,6) and W=span(9,14). Their vector sets are
{0,6,11,13} and {0,7,9,14}, so they are distinct planes outside the clique.
All four cross dot products of their displayed bases are zero; thus U and W
are adjacent. Both have K={0}, P=span(1,4), rank f=2,
image f=span(3,12), and kernel f={0}. Their maps differ on the same P basis:

| Argument in P | f_U | f_W |
| --- | ---: | ---: |
| 1=e1 | 12 | 15 |
| 4=e3 | 15 | 3 |

Both maps are isomorphisms from P onto the same image. A rule using only
the stated common data assigns the adjacent planes equal colors, a
contradiction. This is Proposition 5.5 in the joint paper. The checker
replays the spans, both maps and the zero cross-Gram matrix.

## An orthogonality test in lift coordinates

For U described by (K,P,f) and W by (L,Q,g), choose representatives in T
of each value of f and g. Then U is orthogonal to W exactly when

1. K is orthogonal to Q and L is orthogonal to P;
2. for every s in P and r in Q,
   dot(s,r) + dot(f(s),r) + dot(s,g(r)) = 0 in F_2.

To prove this, pair k+f(s)+s with l+g(r)+r. The T--T term vanishes.
The first condition removes the terms dot(k,r) and dot(s,l), leaving
the displayed expression. Conversely, orthogonality applied to k and
g(r)+r, and to f(s)+s and l, gives the first condition, then pairing lifts
gives the second. Changing a representative of f(s) by K or g(r) by L
does not change the expression once the first condition holds.

This supplies a concrete criterion for evaluating a future rule based on
selected lift-map values. Such a rule must separate the displayed planes
and all other orthogonal pairs. The full maps always reconstruct the vertices;
a compression into 15 colors remains open. No new solver or Lean run was
performed. The existing final six-dimensional Lean theorem retains its four
native-evaluation axioms. The subsequent [line certificate](line-coloring.md)
settles chi(Gamma_6)=12; structural15-coloring and n7 remain open. The
[lift-relations replay](lift-relations.md) subsequently validates this criterion
against all original graph pairs.
