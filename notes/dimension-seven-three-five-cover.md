# An affine odd plane forces an impossible three-plus-five even cover

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic class
size four cannot have outside defects of sizes five and six with
even counts (k5,k6)=(3,5) and saturated counts (A,B,C)=(7,1,8).

A written charge argument forces zero characteristic charge and a
four-point affine plane of odd projections. A written symplectic
normalization then reduces every candidate to one of 400 necessary
even covering roots. A new independently audited finite failed-state
certificate excludes all of them. It applies only to this specified
profile and does not use the previous 384-root certificate.

Eighteen of the original forty-six 5+6 raw profiles are now excluded;
twenty-eight remain unexcluded. Nine of forty-eight 6+6+6 raw profiles
are excluded; thirty-nine remain unexcluded. The other rows have no
joint-feasibility claim. Characteristic sizes four through eight and
exact dimension-seven chromatic numbers remain open, with lower bound
nineteen and no nineteen-color witness.

## Charge parity forces the affine plane and h=0

Put E=z-perp and C_z={z,z+e,z+f,z+g}, with h=e+f+g.
The eight pure odd heptads leave seven odd projections, the nonzero
points of a Lagrangian M, by the
[written eight-spread completion theorem](dimension-seven-nineteen-obstruction.md).
Partition these points into the characteristic projections e,f,g,
the two odd projections a1,a2 in D5, the odd projection c in D6,
and the odd projection b of the single saturated mixed class.

Let U be the sum of the three even members of D5, and V the sum
of the five even members of D6. All other saturated classes have
zero projected charge, so the seven-point sum of M and the
partition-charge identity give

```text
h=a1+a2+c+b,
(U+a1+a2)+(V+c)=h,
U+V=b.
```

The [quadratic partition identity](dimension-seven-size-four.md)
requires w5 dot w6=A+B+tau5+tau6=0: both defect taus are one
and A+B=8. On the other hand, using V=U+b and isotropy of M,

```text
w5 dot w6=U dot b + U dot c + V dot(a1+a2)
            =U dot b + 1.
```

Indeed V dot c=5 mod two=1, and U dot a1=U dot a2=3 mod two=1.
Thus U dot b=1. The restriction ell=U dot(-)|M consequently takes
value one at all four distinct points a1,a2,c,b. They are exactly
its value-one affine plane. The characteristic projections are
ker(ell) minus {0}, whose three points sum to zero. Therefore h=0
is a conclusion, not a normalization assumption.

Write R=U and S=V=R+b. Each even member of D5 pairs to zero
with R, because it pairs to one with the other two; each even
member of D6 pairs to zero with S, because there are four others.
These are their odd-cardinality Gram radicals. Both R and S restrict
to ell on M, and R dot b=1.

Every non-pure-odd class except the seven pure even heptads has an
odd member projected into M. Such a member forbids all even points
of M from its class. The characteristic class contains no even
points. Hence each of the seven pure even heptads must meet M once.

## A basis normalizes every marked covering problem

Choose an order of a1,a2 and set

```text
e1=a1+a2,  e2=a1+c,  e3=a1.
```

The first two form a basis of ker(ell), and (e1,e2,e3) is a basis
of M. The fourth affine point is b=e1+e2+e3. The vector R pairs
with this basis as (0,0,1), so the plane spanned by e3,R is
nondegenerate. Its perpendicular complement contains e1,e2 as
a Lagrangian; choose a symplectic dual pair d1,d2 there. Sending

```text
(e1,e2,e3,d1,d2,R) -> (3,12,48,65,71,95)
```

defines an isometry of E, extended to the original dot space by
fixing z. It normalizes all the following data:

```text
characteristic projections -> {3,12,15},
(a1,a2,c,b) -> (48,51,60,63),
(R,S) -> (95,96).
```

This is a written basis construction for arbitrary admissible
markings and R; transitivity on full marked colorings is not assumed.

In these coordinates, D5 has two odd members 79,76. Its three
even members pair to one with 48,51, pair to zero with R=95,
and sum to 95. Of the eight candidate even points, exactly four
three-cliques meet these conditions. D6 has odd member 67; its
five even members pair to one with 60, pair to zero with S=96,
and sum to 96. Of sixteen candidate even points, exactly six
five-cliques qualify. The mixed class has odd member 64; its
even sextet has forced sum 63, with exactly 32 choices.

Disjoint choices of these three even blocks give 400 ordered roots,
each leaving 49 even points, including all seven points of M.
These must be partitioned into seven pure even heptads meeting M
once. There are 224 eligible heptads among the 288 even heptads
in E. The finite certificate excludes every root of this necessary
covering problem, proving the theorem.

## A bounded search followed by an independent proof audit

The [builder](../develop/build_dimension_seven_three_five_cover.py)
searches only this normalized profile, with explicit state, visit
and time limits. It writes a certificate only after every root
fails. Exhausting a limit or finding a cover writes no exclusion
certificate. The completed certificate records 2,004 failed states,
1,604 branches and 1,056 leaves.

The [independent auditor](../develop/check_dimension_seven_three_five_cover.py)
regenerates the local defect catalogs by direct combinations and
bitmask clique enumeration. Array heptad and bitmask six-clique
catalogs agree on all 288 and 2,016 blocks, respectively. It checks
every required root and, at every failed state, every eligible
heptad containing the recorded pivot and contained in that state.
Every successor is another recorded failed state with seven fewer
points; leaves have no admissible heptad. All states are reachable
from the required roots. These decreasing implications give an
acyclic finite proof, independent of the builder's search result.

Normalization controls range over seven fixed-M affine planes,
twelve odd-role markings per plane and eight lifts of R, giving
672 conditional configurations. The auditor checks 32,928 basis
Gram entries, each induced bijection and candidate-set identity,
and 6,720 inverse-mapped defective classes against the original
dot product. These are local controls of the universal written
reduction, not an enumeration of complete colorings.

The [report](../results/dimension-7-three-five-cover-check.json) binds
the new [certificate](../results/dimension-7-three-five-cover-proof.json),
builder, auditor, proof note and preceding artifacts to their exact
bytes. No prior spread enumeration or unrelated coloring search is
rerun. The written reduction and finite covering proof have separate
roles; no SAT, DRAT, Lean or independent Pro review is claimed.
The submitted manuscript and Zenodo PDF are unchanged. The original
dimension-six formal theorem retains three standard and four
native-evaluation axioms.

```sh
python3 develop/build_dimension_seven_three_five_cover.py --certificate /tmp/dimension-7-three-five-cover-proof.json
python3 develop/check_dimension_seven_three_five_cover.py --certificate /tmp/dimension-7-three-five-cover-proof.json --report /tmp/dimension-7-three-five-cover-check.json
```
