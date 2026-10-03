# Comparing geometric profiles on the same baseline

The exact `(dim U,H,K)` profile retains actual subspaces and gives 240 groups,
139 multicolored. The first numerical script retains dimensions but omits H
and K themselves, giving 30 groups, 29 multicolored. These are different
partitions; our earlier description of a reduction from 139 to 29 was incorrect.

Run `python3 develop/audit_geometry_profiles.py` to reproduce this comparison:

| Partition | Groups | Multicolored | Vertices in multicolored groups |
| --- | ---: | ---: | ---: |
| Dimensions alone | 12 | 11 | 2,808 |
| First numerical script | 30 | 29 | 2,808 |
| Numerical plus self-orthogonal-count parity | 30 | 29 | 2,808 |
| Exact `(dim U,H,K)` | 240 | 139 | 2,288 |
| Exact plus quotient dimension | 263 | 160 | 2,288 |
| Exact plus quotient dimension and alternating status | 263 | 160 | 2,288 |

Adding quotient dimension splits 22 original exact profiles. None of the
139 original multicolored groups becomes entirely single-color. Minimum
disagreements between the witness and a profile-constant map, ignoring edges,
change from 1,133 to 1,131; these are not feasible recoloring counts.
Refinement can increase the number of multicolored groups, so their raw count
alone is a misleading measure of progress.

The audit report includes all member bases and colors for the 160 remaining
exact multicolored groups. Quotient dimension was checked both by radical
enumeration and independent binary elimination on the restricted Gram matrix.
Both original scripts' counts were reproduced and compared with the audit.

## Redundant intersections and the parity calculation

Since H is contained in T and K=U intersect T, we have
`U intersect H = K intersect H`. Thus both intersection dimensions, and
`dim(U/(U intersect H))`, are already determined by the exact profile.
Derived quantities cannot split an exact group.

For the symmetric bilinear dot form B over F_2, B(x,x) is linear:
B(x+y,x+y)=B(x,x)+B(y,y). Its polarization is zero, so it does not give
a quadratic refinement with polar form B when B is nonzero. Arf invariants
require a specified quadratic form with nondegenerate alternating polar form;
the generally nonalternating quotients here have no such form supplied.
Failure of this parity test is not failure of an Arf approach on a separately
defined quadratic space.

With d=dim U and r=dim(rad U), the number of self-orthogonal vectors outside
the radical is `2^d-2^r` for an alternating restriction and
`2^(d-1)-2^r` otherwise. Indeed the self-pairing functional is respectively
zero or a nonzero linear functional, whose kernel has half the vectors.
The parity therefore follows from dimension, radical dimension and alternating
status. In this witness it makes no additional split. The historical function
name in the coauthor script is retained for compatibility.

## Written obstruction

**Proposition.** No proper coloring of the six-dimensional full orthogonality
graph depends only on `(dim U,H,K)` and the isometry type of the restricted
nondegenerate bilinear quotient `U/(U intersect U-perp)`.

**Proof.** The distinct lines U=span(e1) and V=span(e2), encoded as span(1)
and span(2), are adjacent because e1 dot e2=0. Both have dimension one,
H=span(e3+e4,e5+e6)=span(12,48), and K={0}. Their restricted forms have
Gram matrix [1]; their radicals vanish and the quotient forms are isometric.
A rule depending only on these data assigns equal colors to adjacent vertices.
This contradiction is independent of the fixed certificate and color count.
The audit also replays the coordinate witness. **QED.**

## Full-stabilizer equivariance is also impossible

Let G be the orthogonal stabilizer of T, acting on the 15 clique labels by
g.c_W=c_(gW). No proper 15-coloring with the prescribed clique colors can
satisfy c(gU)=g.c(U) for every g in G. The coordinate transposition (1,2)
preserves the dot product and fixes T pointwise, so it fixes every clique
subspace and all 15 color labels. It exchanges the adjacent lines span(e1)
and span(e2); equivariance forces equal colors, a contradiction.

This is Corollary 5.3 in the paper. It supersedes the earlier suggestion
that full-stabilizer equivariance with permuted clique labels was open.
It is specific to the 15 labels determined by the precolored clique.
The audit checks the transposition on all 4096 vector pairs and all eight
vectors in T as a coordinate replay of the written proof.

Rules using further information about U's placement, auxiliary choices, or
a smaller symmetry group remain possible directions. The statistics and
these written obstructions do not solve structural 15-coloring or n=7.
No Lean verification is claimed for the proposition or corollary.
