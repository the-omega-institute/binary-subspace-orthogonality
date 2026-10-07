# The completed-hole five-point-defect profile is impossible

**Theorem.** A nineteen-coloring of Gamma_7 cannot have a
three-point characteristic class, a five-point class of type
(2 even,3 odd), seven pure even heptads, two mixed (6,1) classes,
and eight pure odd heptads. This excludes the completed-hole
profile left by the [quadratic defect analysis](dimension-seven-three-point-defects.md).

The proof combines a written symplectic normalization with a
checked finite exact-cover exclusion. The other two one-five-defect
profiles, (0,5;3,7,7) and (1,4;2,8,7), remain open. The two-six-defect
branch and larger characteristic classes also remain open. The line
and full-subspace chromatic numbers still have lower bound nineteen;
no numerical improvement or nineteen-color witness is claimed.

## The local geometry is forced

Put E=z-perp and write C_z={z,z+e,z+f}, where e,f are distinct
nonzero points with e dot f=0. Set h=e+f. The eight pure odd
heptads correspond to eight disjoint Lagrangians. Their seven holes
complete to M minus {0}, so e,f and all remaining odd projections
belong to this Lagrangian M.

Write the defective class as

```text
D={u,v,z+g_1,z+g_2,z+g_3}.
```

The two even vectors satisfy u dot v=1. Their restrictions to M
are the same nonzero linear functional ell: both take value one on
the three distinct g_i, while two distinct nonzero functionals on
a three-space have at most two simultaneous value-one points.
Thus r=u+v lies in M=M-perp and ell(r)=u dot(u+v)=1.

The affine plane P={x in M: ell(x)=1} has four points. The g_i
are three of them; let t be the missing point. Its four-point sum
is zero, so g_1+g_2+g_3=t. The global projected-sum identity gives

```text
h=r+t.
```

Since h is nonzero, r is one of the three g_i. Also ell(e)=ell(f):
their sum h has value zero. They cannot both have value one,
because only t is unoccupied in P. Therefore e,f span ker(ell),
and its third nonzero point is h. The two mixed odd projections
must be precisely h and t, the remaining two holes.

## A symplectic normalization fixes all defective data

Choose the ordered basis (e,f,r) of M and a symplectic dual basis
of E. An isometry sends these three vectors to (3,12,48). Then

```text
h=15,       t=63,       M={0,3,12,15,48,51,60,63}.
```

The fixed dual basis is (65,71,95), whose third vector restricts
to ell. Hence u=95+x for some x in M. In coordinates (x,y) with
M={y=0}, a symmetric shear (x,y)->(x+S y,y), taking the third
column of S to be this x, removes it. This shear preserves the
symplectic form and fixes M pointwise. We obtain u=95 and v=111.
Every isometry of E extends to the original dot space by fixing z.
Thus every coloring in this profile can be normalized to

```text
C_z={127,124,115},       D={95,111,79,76,67},
mixed odd lines={112,64}.
```

The seven even points of M form a clique. Every mixed label and
the label of D is forbidden there by its odd members in z+M.
The pure odd labels and the characteristic label are unavailable
as well. Consequently each of the seven pure even heptads must
meet M in exactly one point.

## The finite covering problem

An even six-clique has a unique seventh completion: its vector
sum. Therefore the six even vectors of the two mixed classes have
forced sums 15 and 63 respectively. Direct coordinate construction
gives 32 choices for each. After excluding 95,111 and requiring
the two choices to be disjoint, there are 384 ordered pairs.

Each pair leaves 49 of the 63 even points. These must be partitioned
into seven even heptads. There are 288 even heptads in E, of which
224 meet M in exactly one point. The resulting 384 exact-cover
instances have no solution.

The [builder](../develop/build_three_point_hole_cover.py) records a
finite failed-state certificate, using a single common universe
of 224 heptads. A state is a remaining point set and a chosen
point in it. Every possible heptad containing that point and
contained in the state leads to another recorded failed state.
Leaves have no possible heptad. Removing a heptad strictly lowers
the number of points by seven, so these implications are acyclic.
Every one of the 384 required root states is covered.

The [independent auditor](../develop/check_three_point_hole_cover.py)
reconstructs all six-cliques by a separate bitmask enumeration,
obtains all heptads from their forced completions, and independently
reconstructs every eligible root. It verifies every branch of the
[certificate](../results/dimension-7-hole-cover-proof.json), without
trusting the builder's search result. All 1,784 states are reachable
from the roots and satisfy the closure conditions. This is a
checked finite exclusion of this specific normalized profile.

## Validation and scope

Coordinate normalization controls cover all 48 local defective
classes compatible with e=3,f=12 and a hole Lagrangian. For each,
the auditor constructs a symplectic basis with u as the third dual
vector and checks the induced isometry on all 16,384 ordered pairs
of original vectors. These are local controls; the universal
normalization is the written basis/shear argument above.

The [audit report](../results/dimension-7-hole-cover-check.json) binds
the certificate, builder, auditor, note and preceding certificate.
Rebuilding reproduces the proof bytes. Removing a required root or
failed state, replacing a pivot by an absent point, or corrupting a
forced-sum class must be rejected by the auditor. No native SAT,
DRAT or Lean is involved. The submitted manuscript at 28e27a8 is
unchanged; the original dimension-six Lean theorem retains three
standard and four native-evaluation axioms.

```sh
python3 develop/build_three_point_hole_cover.py --certificate /tmp/dimension-7-hole-cover-proof.json
python3 develop/check_three_point_hole_cover.py --certificate /tmp/dimension-7-hole-cover-proof.json --report /tmp/dimension-7-hole-cover-check.json
```
