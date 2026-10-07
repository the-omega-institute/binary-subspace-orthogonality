# The three-plus-one odd split excludes another five-plus-six profile

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic
class size four cannot have outside defects of sizes five and six,
with even counts (k5,k6)=(2,5) and saturated counts (A,B,C)=(8,0,8).

Together with the [two affine-plane exclusions](dimension-seven-five-six-affine.md),
this excludes three of the 46 raw 5+6 count profiles. The other
43 profiles are unexcluded here and their joint feasibility remains
untested. All 48 raw 6+6+6 profiles remain untested. Characteristic
sizes four through eight and exact dimension-seven chromatic numbers
remain open, with lower bound nineteen and no nineteen-color witness.

## The five-point charge lies in the completed hole space

Put E=z-perp. Eight pure odd heptads give eight disjoint
Lagrangians. By the written eight-spread completion theorem, the
seven remaining odd projections are M minus {0}, for a Lagrangian M.
With no mixed classes, they partition into the three characteristic
projections e,f,g, the three odd projections a1,a2,a3 in D5, and
the single odd projection b in D6. Write

```text
D5={u,v,z+a1,z+a2,z+a3},
D6={s1,s2,s3,s4,s5,z+b},
h=e+f+g,  t=a1+a2+a3,  r=u+v.
```

The functionals u dot(-)|M and v dot(-)|M both take value one
at three distinct points a1,a2,a3. Distinct nonzero functionals on
a binary three-space have exactly two simultaneous value-one points:
their joint rank-two map has a one-dimensional fiber. Hence the
two functionals agree. Their sum vanishes on M, giving

```text
r in M-perp=M,
w5=r+t in M.
```

The partition charge identity w5+w6=h, with h in M, now forces
w6 in M as well. But independence of D6 requires si dot b=1
for each of its five even members, so

```text
w6 dot b=(s1+s2+s3+s4+s5+b) dot b=5 mod 2=1.
```

This contradicts w6,b in the isotropic space M, and proves the theorem.
No assumption that h=0 is made; both zero and nonzero characteristic
charges occur among the local controls below. This argument uses the
linear partition identity rather than a quadratic parity exclusion.

More explicitly, the seven-point sum of M is zero, so h=t+b.
The six-point defect would need charge w6=h+w5=r+b in M.
Every locally valid five-even/one-odd class has charge pairing to
one with b, and therefore none has this required charge.

## Coordinate verification and scope

The [checker](../develop/check_dimension_seven_five_six_split31.py)
works with a fixed M. It checks all pairs of distinct nonzero
functionals, verifies that their common value-one set has two points,
and reconstructs the five-point defects using independent array
and bitmask even-pair catalogs. There are 448 local D5 classes.
For each, all four placements of b among the unused hole points
are retained, preserving disjoint odd markings and the original
dot-product independence of the characteristic class. These give
1,792 conditional partition constraints, including 448 with h=0
and 1,344 with h nonzero. Every required w6 lies in M and pairs
to zero with b.

For each of the seven possible b, the checker independently
enumerates five-cliques inside the 32 even vectors pairing to one
with b, using direct combinations and a bitmask recursion. The
catalogs agree: 192 per b, or 1,344 local D6 classes. Each has
w6 dot b=1 and w6 outside M. Their charge catalogs have no
intersection with any required charge from the conditional partition
constraints. These are local partial classes and charge joins;
no complete coloring or even-heptad cover is enumerated.

The [report](../results/dimension-7-five-six-split31.json) binds the
prior count analysis, the two previous exclusions, the written
eight-spread source, this note and the checker. All 43 other raw
5+6 rows are retained without feasibility claims. No spread
enumeration, all-small-class enumeration, SAT, exact-cover search,
DRAT, Lean or independent Pro review is run. This new exclusion
has a universal written proof with coordinate controls, without a
finite cover or spread-enumeration dependency.

The repository manuscript snapshot and the public Zenodo PDF are
unchanged by this research extension. Exact submission-source
synchronization and declarations review remain pending jointly.
The original dimension-six formal theorem retains three standard
and four native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_five_six_split31.py --report /tmp/dimension-7-five-six-split31.json
```
