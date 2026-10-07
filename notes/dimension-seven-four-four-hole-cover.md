# Eight odd heptads are impossible in the two-six branch

**Theorem.** A nineteen-coloring of Gamma_7 with a three-point
characteristic class cannot have two defects of type (4 even,2 odd),
seven pure even heptads, one mixed (6,1) class and eight pure odd
heptads. Together with the [preceding two-six analysis](dimension-seven-two-six-profiles.md),
this excludes every C=7 and C=8 count profile in this branch.
Only (m_1,m_2; A,B,C)=(0,0;3,7,6) and (0,2;1,9,6) remain
necessary candidates, with common-coloring realizability open.

The proof combines written normalization with a checked finite
exact-cover certificate. The exact line and full-subspace chromatic
numbers remain open with lower bound nineteen. Neither the entire
three-point characteristic branch nor larger characteristic classes
are excluded. No nineteen-color witness or new numerical bound is claimed.

## The seven holes determine six projection configurations

Put z=127 and E=z-perp in the standard binary coordinates. The
restriction of the dot form to E is nondegenerate alternating.
Write C_z={z,z+e,z+f}, with e,f distinct nonzero orthogonal points.
The eight pure odd heptads leave exactly the seven nonzero points
of a Lagrangian M, by the written eight-spread completion theorem.
All remaining odd projections belong to M and partition its seven points.

By the charge-member lemma, the first defect's odd projections are
{w_1,r_1}, where w_1 is its charge, and the second's are {w_2,r_2}.
The mixed class has odd projection g. The global charge equation is

```text
e+f=w_1+w_2.
```

The four points e,f,w_1,w_2 are distinct. Thus (w_1,w_2,e) is a
basis of M: e cannot be 0,w_1,w_2, or w_1+w_2, since the last
choice would make f=0. A symplectic isometry sends this basis to
(3,12,48), fixes z on extending to the original dot space, and gives

```text
w_1=3, w_2=12, e=48, f=63,
M={0,3,12,15,48,51,60,63}.
```

The ordered triple (r_1,r_2,g) is therefore one of the six permutations
of (15,51,60). The seven nonzero points of M sum to zero; accordingly
r_1+r_2+g=0. Keeping all six configurations avoids any further orbit
or defect-exchange assumption. Every symplectic basis of M extends
to a symplectic basis of E, so this reduction covers arbitrary M
and arbitrary eight-heptad partial spreads, without re-enumerating spreads.

## Every even class is retained in the covering problem

Let U_i be the four even members of defect i. Its ordinary vector
sum is its charge, because its odd count is even. Hence

```text
sum U_i=r_i,
u dot w_i=u dot r_i=1 for every u in U_i,
u dot v=1 for distinct u,v in U_i.
```

For each fixed (w_i,r_i), there are exactly sixteen such four-point
classes, reconstructed independently in the certificate audit.
The mixed class's six even points form a six-clique whose vector
sum is g. Indeed, its Gram matrix has zero diagonal and ones off
the diagonal and is invertible over F_2. Its six points span E;
both their sum and g pair to one with every member, and are equal
by nondegeneracy. There are exactly thirty-two choices for each g.

The seven even points of M form a clique. Defect and mixed labels
are forbidden there by their odd members; the characteristic and
pure odd labels are unavailable. Its seven vertices consequently
use the seven pure even labels, once each. Every pure even heptad
meets M in exactly one point, since its members pair to one while
M is isotropic. There are 288 even heptads in E, with 224 meeting
M in exactly one point.

For each of the six configurations, enumerate all disjoint triples
(U_1,U_2,V), where V is the mixed six-clique. The triples remove
fourteen even points, leaving forty-nine points including all of
M minus {0}. These remaining points would have to partition into
seven of the 224 eligible heptads. Thus the reduction preserves
the defect charges, disjointness and a common coloring; checking
the classes individually would not suffice.

## A finite certificate excludes every remaining cover

The [builder](../develop/build_four_four_hole_cover.py) records every
eligible ordered triple and a directed acyclic graph of failed
remaining-point sets. At each state it stores an uncovered pivot.
Every eligible heptad containing that pivot and contained in the
state leads to a child formed by deleting its seven points. A
state with no such row is a leaf. The empty state is never marked
failed. The bounded builder writes a certificate only after all
roots are exhausted; a timeout or a found cover is not an exclusion.

The six configurations have respectively 3,456, 3,456, 3,456,
1,792, 3,456 and 1,792 disjoint partial triples, totaling 17,408
distinct roots. The certificate contains 85,720 failed states,
70,672 checked outgoing branches and 45,480 leaves. States have
49, 42, 35 or 28 points; no successful seven-heptad cover is reached.

The separate [auditor](../develop/check_four_four_hole_cover.py)
uses bitmask clique construction rather than the builder's array
recursion. It reconstructs all row catalogs and all roots, then
checks every pivot, every possible successor and reachability of
every recorded state. Each successor has seven fewer points.
Induction from the leaves proves that every recorded state has no
cover, including every root. No solver status is trusted.

The [certificate](../results/dimension-7-four-four-hole-cover-certificate.json)
and [audit report](../results/dimension-7-four-four-hole-cover.json)
give exact counts and bind the builder, auditor, this note and the
preceding two-six report. The normalization controls check all
168 ordered bases of a fixed M and all 1,008 associated ordered
projection assignments, using 6,048 basis dot-pair comparisons.
These controls accompany the universal written symplectic argument;
they do not enumerate all complete colorings or all partial spreads.

## What remains open

Nineteen of the original twenty-one two-six count profiles are now
excluded. The two remaining C=6 profiles leave twenty-one odd-projection
holes. No theorem completing six Lagrangians, no splitting of these
holes into three Lagrangians, and no joint realization of either
candidate is claimed. The next task is their hole geometry and
the constraints imposed by six-point pure odd defects.

This is a written reduction plus an independently checked finite
cover exclusion, with the existing written eight-spread completion
and preceding charge/count results as explicit dependencies.
It is not a Lean proof or an independent Pro review. The submitted
manuscript at 28e27a8 is unchanged; the original six-dimensional
theorem retains three standard and four native-evaluation axioms.

```sh
python3 develop/build_four_four_hole_cover.py --certificate /tmp/four-four-certificate.json
python3 develop/check_four_four_hole_cover.py --certificate /tmp/four-four-certificate.json --report /tmp/four-four-report.json
```
