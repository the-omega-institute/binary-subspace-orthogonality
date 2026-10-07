# Size-four characteristic classes: deficits, charges and one remaining four-point profile

**Theorem.** Suppose a nineteen-coloring of Gamma_7 has a four-point
characteristic class. If its outside deficit is concentrated in one
four-point class, that class must have two even and two odd members,
with saturated counts (A,B,C)=(7,2,8). Eight of the nine count profiles
in this branch are impossible. The remaining profile is necessary,
not asserted realizable. The alternative defect-size patterns 5+6
and 6+6+6 remain open.

The [preceding theorem](dimension-seven-six-holes.md) excludes
characteristic classes of size less than four. Sizes four through
eight and the exact line/full-subspace chromatic numbers remain open.
The numerical lower bound stays nineteen, and no nineteen-color
witness or exclusion of the entire size-four branch is claimed.

## Deficit and count equations

Write C_z={z,z+e,z+f,z+g}. The projections e,f,g are distinct
nonzero, pairwise orthogonal points of E=z-perp. Put h=e+f+g.
Here h may be zero: a dependent triple is the three nonzero points
of a two-space. An independent triple has nonzero h. The size-three
assumption that its charge is always nonzero is not reused.

The eighteen outside classes have capacity seven and total deficit
three. Thus their undersized class patterns are exactly 4, 5+6,
or 6+6+6. Let there be r defects of sizes k_i, with even counts
m_i and odd counts o_i=k_i-m_i; put m=sum m_i. The remaining
18-r saturated classes have pure even, mixed (6,1), and pure odd
counts A,B,C. Counting both parities gives

```text
7A+6B+m=63,
B+7C+sum o_i+4=64,
A+B+C=18-r.
```

Since sum k_i=7r-3, every solution has the form

```text
B=m+7t, A=9-m-6t, C=9-r-t,
```

for an integer t, with all counts nonnegative. Four-point classes
allow even counts 0..4; five-point classes allow 0..5; six-point
classes allow 0,2,4,5,6 by the existing capacity bound. Independent
direct A,B,C loops and these formulas give respectively 9, 46,
and 48 raw count profiles. Equal-size six-point defects are treated
as unordered; five- and six-point defects remain distinguished.
The 46 and 48 profiles are not feasibility results.

## The general charge and quadratic constraint

Let pi(v)=v+(v dot z)z and w_i=sum_{v in D_i}pi(v). All saturated
classes have zero projected sum, so the global partition identity gives

```text
sum w_i=h.
```

Let q be a quadratic refinement of the alternating form on E.
For any independent class of size k and odd count o, polarization gives

```text
sum q(pi(v))=q(sum pi(v))+binom(k,2)+binom(o,2).
```

The quadratic sum of C_z is q(h), because its three nonzero
projections pair to zero. Saturated pure even and mixed classes
contribute one each; pure odd classes contribute zero. The quadratic
sum over all line vectors is zero. With
tau_i=binom(k_i,2)+binom(o_i,2) modulo two, this yields

```text
sum_{i<j} w_i dot w_j = A+B+sum tau_i modulo two.
```

This formula applies to one, two, or three defects. It does not
assume h is nonzero, nor that individually valid defect classes can
be assembled into a common coloring. The report records the required
charge-product parity for every raw count profile.

## One four-point defect: nine profiles reduce to one

With one defect D, its charge equals h and the charge-product sum
is empty. Thus A+B=binom(4-m,2) modulo two. Five profiles fail:

| D (even,odd) | (A,B,C) | A+B mod 2 | binom(odd,2) mod 2 |
| --- | --- | --- | --- |
| (0,4) | (9,0,8) | 1 | 0 |
| (1,3) | (2,8,7) | 0 | 1 |
| (2,2) | (1,9,7) | 0 | 1 |
| (3,1) | (6,3,8) | 1 | 0 |
| (4,0) | (5,4,8) | 1 | 0 |

For the two remaining C=7 profiles, the existing finite seven-spread
completion lemma leaves two transverse hole Lagrangians M,N. All
remaining odd projections lie in their union. Their fourteen even
points need colors. A pure even heptad contributes at most two,
a mixed class at most one, and a defect with any odd members at
most one if it has even members, otherwise zero. Its odd member
forbids the entire hole side containing that projection; on the
other side its pairwise-one even members contribute at most one.
Therefore (0,4;3,7,7) has capacity at most 2*3+7=13, while
(3,1;0,10,7) has capacity at most 10+1=11. Both fail capacity fourteen.

For (1,3;8,1,8), the written eight-spread completion leaves one
hole Lagrangian M. Its three characteristic projections and three
odd defect projections lie in M. The defect charge is h in M;
h=u+g_1+g_2+g_3 for its sole even member u. Hence u is in M.
But it must pair to one with each g_i, contradicting isotropy.

Only (D even,odd; A,B,C)=(2,2;7,2,8) remains.

## Additional necessary geometry of the surviving single-four profile

Again all remaining odd projections lie in the seven holes M minus {0}.
Let u,v be the even defect members, a,b its two odd projections,
and x,y the mixed odd projections. The seven hole points partition as

```text
{e,f,g}, {a,b}, {x,y}.
```

Their full sum is zero. Since the defect charge is h,

```text
r=u+v=h+a+b=x+y in M.
```

The restrictions of u and v to M coincide, defining ell; ell(a)=ell(b)=1
and ell(r)=u dot(u+v)=1. Thus exactly one of x,y has ell-value one.
There are four value-one points of ell on M, so exactly one of e,f,g
has ell-value one as well. In particular ell(h)=1, h is nonzero,
and the characteristic projections e,f,g form a basis of M.

Their sum cannot equal any one of e,f,g, so h belongs either to
{a,b} or to {x,y}. Both locations survive these necessary conditions.
The seven pure even heptads must each meet M once, since its
seven even clique points can use only those seven labels.
No seven-heptad cover or complete nineteen-coloring is established.

## Verification and retained dependencies

The [checker](../develop/check_dimension_seven_size_four.py) verifies
16,384 projection-pair identities, 4,096 quadratic-pair identities,
and 262,144 three-charge polarizations. It independently enumerates
the raw counts by direct loops and the t formulas, checks all five
single-defect parity exclusions and the three geometric exclusions,
and records every required multi-defect charge parity.

For the surviving branch, array and bitmask constructions agree on
the local even-pair catalogs. In a fixed hole Lagrangian, 1,008
local configurations satisfy the characteristic/defect disjointness
and charge equation. Every one has the written functional and
radical constraints; 672 have h in the defect and 336 in a mixed
projection. These controls are partial classes and odd projections,
not jointly realized colorings. No universal orbit claim follows
from these counts.

The [report](../results/dimension-7-size-four.json) binds the note,
checker and previous results. The C=7 exclusions retain the finite
seven-spread completion input; the C=8 exclusion uses the written
eight-spread theorem. Previous proof dependencies remain in force.
No spread enumeration, all-small-class enumeration, SAT, exact-cover
search, DRAT, Lean or new independent Pro review is run.
The submitted manuscript at 28e27a8 is unchanged, and the original
six-dimensional theorem retains three standard and four native-evaluation axioms.

The next bounded target is the surviving single-four profile's
common-coloring cover, retaining its two charge locations, or one
specified 5+6/6+6+6 charge profile. Sizes four through eight remain open.

```sh
python3 develop/check_dimension_seven_size_four.py --report /tmp/dimension-7-size-four.json
```
