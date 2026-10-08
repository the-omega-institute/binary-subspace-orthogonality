# Sixteen ordered pure-source normal forms

**Theorem.** The pure-source geometry of the remaining
`(4,6,6;5,2,8)` row has sixteen exhaustive ordered marked normal
forms. Each full ordered marked stabilizer has order eight and
fixes M pointwise, including all four actual positive holes.

The roles are D0, the ordered mixed heptads J1,J2, the ordered
pure sextets P1,P2 and their associated pure source heptads H1,H2.
This order is retained throughout the normalization.

## A basis and a shear give every ordered form

The [pure-source theorem](dimension-seven-four-six-six-pure-sources.md)
gives a basis (a,c,d) of M, a distinct point b in M, and
outside-M completions satisfying

```text
u+v=a+c+d,    u dot v=1,
ell=u dot(-)|M=v dot(-)|M,
(ell(a),ell(c),ell(d)) in {100,010,001,111}.
```

Choose a symplectic dual basis to (a,c,d). In the resulting
coordinates write u=(x,y). Its nonzero dual coordinate y is the
ordered functional pattern. Send the basis and its dual to

```text
(a,c,d,f1,f2,f3)=(3,12,48,65,71,95).
```

An M-pointwise symplectic shear (x,y)->(x+B y,y), with B a
symmetric three-by-three binary matrix, removes x. For any nonzero
y, the map B->B y is onto: in coordinates making y a unit vector,
its image is an unrestricted column of a symmetric matrix.
Changing coordinates here proves surjectivity; it does not exchange
the coloring's ordered roles. Hence take u=sum y_i f_i and v=u+63.

Since b differs from a,c,d, its only possible positions are
a+c,a+d,c+d,a+c+d. This gives the sixteen forms:

| Functional pattern | a,c,d | u | v | b |
| --- | --- | --- | --- | --- |
| 100 | 3,12,48 | 65 | 126 | 15,51,60,63 |
| 010 | 3,12,48 | 71 | 120 | 15,51,60,63 |
| 001 | 3,12,48 | 95 | 96 | 15,51,60,63 |
| 111 | 3,12,48 | 89 | 102 | 15,51,60,63 |

In each row the characteristic projections are
M minus {0,3,b,12,48}, and their sum is b+63. All maps of E
extend to the original binary dot space by fixing z=127.
They transport the original graph conditions, associated sources
and actual holes.

The forms are inequivalent under isometries of these ordered
markings. The functional values on the ordered basis are invariants;
once a,c,d are fixed, every point of M, including b, is fixed.
Thus neither two patterns nor two b positions can be identified.
Assigning an order to each pair of equal-sized roles is always
possible, so retaining all ordered forms loses no hypothetical
coloring. This theorem does not claim a minimal list for unordered
roles and does not use role exchanges for compression.

## The full ordered marked groups

Every M-preserving symplectic map has coordinate form

```text
(x,y)->(Lx+B L^(-transpose)y, L^(-transpose)y),
L in GL(3,2), B symmetric.
```

Fixing the ordered basis a,c,d forces L=I. Fixing normalized
u=(0,y) requires B y=0, which also fixes v=u+a+c+d.
Surjectivity of B->B y gives three independent conditions in the
six-dimensional space of symmetric matrices. There are exactly
eight solutions. Every one fixes all markings, and the preceding
argument excludes every other ordered marked isometry. The full
ordered stabilizer therefore has order eight for every form.

It fixes M pointwise. In particular all 24 ordered allocations
of the four distinct positive holes to P1,P2,H1,H2 must be retained;
each has the same full marked group of order eight. The stabilizer
of actual component blocks may be smaller. A reversible completion
swap between a sextet and its source changes which class has six
or seven members. It is a proper recoloring, not an isometry of
the original ordered marked classes, and supplies no extra group
element.

The full M-preserving group has 168 choices of L and 64 choices
of B, hence order 10,752. Each ordered normal form has 1,344
marked images, eight maps giving each image. Independently
enumerating all charge markings gives 21,504; the sixteen image
sets are disjoint and exhaust that set. This control verifies the
written normalization rather than inferring completeness from
group orders alone.

## Complete local catalogs and four-hole allocations

Each hypothetical coloring supplies the following local components.
D0 is a four-even block with sum a and pairings one with a,b.
J1,J2 are even sextets with sums c,d. All three avoid u,v.
P1,P2 are one-hole sextets of sums u,v, respectively, each avoiding
the other completion. H1,H2 are anchored heptads containing u,v,
respectively, each avoiding the other completion. All original odd
members are included when checking their graph independence.

| Pattern | D0 for b=15,51,60,63 | J1 | J2 | Each P1,P2,H1,H2 |
| --- | --- | --- | --- | --- |
| 100 | 10,10,16,8 | 32 | 32 | 18 |
| 010 | 16,16,16,16 | 22 | 32 | 18 |
| 001 | 16,16,16,16 | 32 | 22 | 18 |
| 111 | 16,16,16,8 | 22 | 22 | 18 |

The source avoidance restrictions explain why the sixteen-component
D0 catalog of the unrestricted geometry can shrink; these catalog
sizes are not profile exclusions.

For every form there are exactly **1,152 pairwise disjoint ordered
local quartets (P1,P2,H1,H2)**. Each of the 24 ordered positive-hole
allocations has 48 quartets. Their full eight-element ordered group
has 144 quartet orbits, all of size eight, with trivial component
stabilizers. These orbit and stabilizer counts are checked on the
actual block tuples; freeness is not inferred from a division.
Each actual-hole allocation contains six such orbits.

These quartets occupy 26 even points. They have not yet been
required to avoid compatible choices of D0,J1,J2, so they are not
complete necessary joint roots. A joint family must retain all
seven mutually disjoint components of even sizes 4,6,6,6,6,7,7.
The [source theorem](dimension-seven-four-six-six-pure-sources.md)
then gives the necessary 21-point/three-kernel-hole remainder,
requiring three residual pure heptads from the complete 96-row
kernel-anchored catalog. Every catalog and quartet action transports
the actual holes, which the ordered groups fix pointwise.

## Verification and next bounded problem

The [auditor](../develop/check_dimension_seven_pure_source_normalization.py)
constructs all 10,752 parabolic maps, checks their basis Gram
entries against the original dot product, and independently compares
the sixteen image sets with every ordered charge marking. For all
four stabilizers it checks full dot-product preservation and closure.
Independent array and bitmask clique catalogs agree for sizes four,
six and seven. Independent set-union and bitmask tests give exactly
the same complete local quartets. Component actions, quartet actions,
actual-hole transport and orbit--stabilizer identities are checked.

The [report](../results/dimension-7-pure-source-normalization.json)
binds the preceding source theorem and its ten inherited finite
report/source/certificate/dependency identities. Previous source and
historical covering audits are not rerun. No complete seven-component
roots, covering search, new certificate, Lean or independent Pro
review is produced. No raw row is excluded: the lists remain 25/35,
and exact n=7 remains open with lower bound 19. The original n=6
theorem retains three standard plus four native-evaluation axioms;
the submitted snapshot and all historical evidence are preserved.

Next construct complete mutually disjoint seven-component families
for all sixteen ordered forms and all 24 actual-hole allocations,
using the full eight-element groups. Retain complete ordered tuples
when forming remainder orbits; do not assume a unique decomposition
or transfer the local-quartet freeness to remainders. Only then is
a complete three-heptad covering question ready for proof search.

```sh
python3 develop/check_dimension_seven_pure_source_normalization.py --report /tmp/dimension-7-pure-source-normalization.json
```
