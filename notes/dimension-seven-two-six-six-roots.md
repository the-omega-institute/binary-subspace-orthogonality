# Complete necessary roots for (2,6,6;7,0,8)

**Theorem.** After the [charge and recoloring reduction](dimension-seven-two-six-six-charge.md),
every nineteen-coloring with characteristic class size four and profile
(2,6,6;7,0,8) gives one of the complete 49-point necessary even remaining
sets constructed below, up to the proved order-eight marked group.
The actual hole of each pure six-class is retained, including absence
of a hole. Cover existence is invariant under this group.

This completes the root and orbit preparation for the outside-M case.
It does not decide any seven-heptad cover or exclude the profile.
The 25 five-plus-six and 39 three-six raw candidates remain unchanged;
exact n7 remains open with lower bound nineteen.

## Reconstruct the entire necessary family

Use the normalized data

```text
z=127,  M minus {0}={3,12,15,48,51,60,63},
D0={95,111,z+48,z+51,z+60,z+63},
q1=65,  q2=113,  characteristic projections={3,12,15}.
```

Here the two pure six-class roles are intrinsic: their sums pair to
zero and one respectively with either even member of D0. Construct
all even six-cliques with those sums and remove any containing 95
or 111. There are 32 choices for D1 and 22 for D2. Retain every
ordered disjoint pair. For each pair define

```text
R=(E minus {0}) minus ({95,111} union D1 union D2).
```

Every such R has 49 points and zero vector sum: the total sum over
E minus {0} is zero, and the removed sum is
(95+111)+(65+113)=48+48=0. The even pair avoids M. Each pure
defect contains at most one hole, because its members pair to one
while M is isotropic. The actual missing holes are therefore
(D1 intersect M) union (D2 intersect M).

The complete 384 ordered pairs yield 384 distinct remaining sets.
Thus every R has a unique ordered defect pair within these complete
catalogs. This finite injectivity check is useful: preserving R
under a marked isometry necessarily preserves and transports both
defects and their individual holes. No interchange of the two
pure-six roles or loss of hole assignment is used.

The four ordered hole allocations have 16,88,64,216 roots for
(0,0),(0,1),(1,0),(1,1), respectively. The remaining holes number
seven, six, six and five. These partial local configurations are
necessary data, not complete nineteen-colorings: the eight odd
heptads and the global coloring still require compatibility.

## Reduce only under the full marked group

The preceding written proof gives the full order-eight stabilizer.
Relative to the basis (3,12,48;65,71,95), its restrictions to M are
the two maps fixing 12,48 and sending 3 to 3 or 15. Lift each
restriction A by (x,y)->(Ax,A-inverse-transpose y). The four
pointwise-M shears have only S22,S33 possibly nonzero.
These eight isometries fix z, the characteristic projections as
a set, and q1,q2 individually; they preserve {95,111} and both
pure-six catalogs.

For every root R the checker transports its unique pair (D1,D2)
and its ordered actual holes (t1,t2), where zero denotes absence.
It computes the entire orbit, chooses the smallest bitmask as
representative, and checks orbit-size times stabilizer-order equals
eight. Roots with different ordered hole-count allocations are
never identified. Each representative records its two actual
sextets, ordered holes, marked hole orbit and remaining holes.
The complete family has 75 orbits: 12 of size two, 36 of size four
and 27 of size eight. The actions are not free; their corresponding
remaining-set stabilizers have orders four, two and one. The report
records the full orbit partition rather than dividing 384 by eight.

| Ordered defect hole counts | Complete roots | Marked orbits |
| --- | --- | --- |
| (0,0) | 16 | 2 |
| (0,1) | 88 | 11 |
| (1,0) | 64 | 8 |
| (1,1) | 216 | 54 |

## The later cover must allow every even heptad

A nineteen-coloring necessarily partitions R into seven pure even
heptads. There are 288 such heptads in E, of which 224 meet M
once and 64 avoid M. Retain every row contained in R, including
rows avoiding M. Since a heptad hits M at most once, a cover of
a root with H remaining holes has exactly H anchored rows and
7-H rows avoiding M. In particular the two-hole defect branch
requires two rows avoiding M.

Every marked isometry permutes all 288 rows and sends rows
contained in R bijectively to rows contained in its image. Thus
a root has a seven-heptad cover if and only if its representative
does. A later finite exclusion must account for every representative
and every admissible pivot row from this full catalog. An even
cover alone is not a full nineteen-color witness: it must be
extended and checked in the original graph.

No cover search or failed-state certificate is run here. The
inside-M exclusion remains inherited from the prior recoloring
theorem and its historical finite cover input; no certificate for
a different profile settles any outside-M root.

## Reproducible finite audit

The [checker](../develop/check_dimension_seven_two_six_six_roots.py)
uses independent array and bitmask clique constructions and two
independent root constructions, comparing complete multisets and
their witnesses. It checks original classes, zero sums, actual
holes, all group actions on roots and catalogs, orbit partitions
and stabilizer identities. It reconstructs every eligible heptad
per representative without attempting a cover. There are 3,072
checked root-group actions; the eligible heptad counts per
representative range from 46 to 63. Every representative remains
untested for cover existence.

The [complete representative report](../results/dimension-7-two-six-six-roots.json)
binds the checker, note, imports and preceding charge proof/report.
Both PDFs and historical formal/certificate files are preserved.
No Lean or independent Pro review is claimed. The original
six-dimensional theorem retains three standard plus four
native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_two_six_six_roots.py --report /tmp/dimension-7-two-six-six-roots.json
```
