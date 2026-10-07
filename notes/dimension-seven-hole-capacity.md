# A uniform hole-capacity obstruction excludes twenty-one further profiles

**Theorem.** Suppose a nineteen-coloring of Gamma_7 has a characteristic
class of size four. Let A,B,C count saturated pure even, mixed (6,1),
and pure odd classes. Let P count pure even defective classes and R
count defective classes containing both parities. If C=8 or C=7, then

```text
C=8:  A+P >= 7,
C=7:  2A+B+2P+R >= 14.
```

These necessary inequalities exclude twelve further raw 5+6 profiles
and nine raw 6+6+6 profiles in one argument. Together with the three
previous charge exclusions, fifteen of the original forty-six 5+6
profiles are excluded; thirty-one remain unexcluded. Nine of the
forty-eight 6+6+6 profiles are excluded; thirty-nine remain unexcluded.
The remaining rows are necessary count possibilities, with joint
coloring feasibility untested. Characteristic sizes four through eight
and exact dimension-seven chromatic numbers remain open, with lower
bound nineteen and no nineteen-color witness.

## A capacity bound on a union of hole Lagrangians

Put z=127 and E=z-perp. Every pure odd heptad consists of z+L*,
where L* is the nonzero part of a Lagrangian in E. Distinct such
classes give disjoint Lagrangians. The projections of all odd vectors
in other classes, except z itself, lie in their complement.

For C=8, the [written eight-spread completion theorem](dimension-seven-nineteen-obstruction.md)
identifies the complement as M*, with seven points. For C=7, the
[existing finite seven-spread completion lemma](dimension-seven-seven-holes.md)
identifies it as M* disjoint-union N*, with fourteen points. The
second assertion retains its finite-enumeration proof dependency;
no new spread enumeration is needed here.

More generally, suppose the hole set H is a disjoint union of t
nonzero Lagrangians. Even members of an independent color class
pair to one, whereas two points in the same hole Lagrangian pair
to zero. Thus a pure even class meets H in at most t points.

If a class also has an odd vector z+a, its nonzero projection a
belongs to one hole Lagrangian M_j. Every even point m in M_j
satisfies m dot(z+a)=m dot a=0, so none can lie in that class.
Such a mixed class meets H in at most t-1 points, regardless of
the number or positions of its other odd members. A pure odd
class meets the even set H in no points. The characteristic class
is pure odd because its members must pair to one with z.

All 7t even points of H must be partitioned among the remaining
classes. Applying these bounds to saturated and defective classes
gives the single inequality

```text
7t <= t(A+P)+(t-1)(B+R).
```

Taking t=1 and t=2 proves the theorem. This is a written capacity
argument, independent of the positions of characteristic or defect
markings, the characteristic charge h, and any marked-orbit claim.
It supplements the uniform partition-charge identities; charge
alone is not claimed to exclude these rows.

## All newly excluded raw rows

Here k5,k6 are the even counts of the distinguished five- and
six-point defects. For three six-point defects, their even counts
are unordered. The last column is the maximum hole capacity from
the theorem; it is strictly less than seven for C=8 or fourteen
for C=7.

| Pattern | Defect even counts | (A,B,C) | Hole capacity |
| --- | --- | --- | --- |
| 5+6 | (2,5) | (2,7,7) | 13 |
| 5+6 | (2,6) | (1,8,7) | 13 |
| 5+6 | (3,4) | (2,7,7) | 13 |
| 5+6 | (3,5) | (1,8,7) | 12 |
| 5+6 | (3,6) | (0,9,7) | 12 |
| 5+6 | (4,4) | (1,8,7) | 12 |
| 5+6 | (4,5) | (0,9,7) | 11 |
| 5+6 | (4,5) | (6,2,8) | 6 |
| 5+6 | (4,6) | (5,3,8) | 6 |
| 5+6 | (5,4) | (0,9,7) | 12 |
| 5+6 | (5,5) | (5,3,8) | 6 |
| 5+6 | (5,6) | (4,4,8) | 6 |
| 6+6+6 | (4,4,5) | (2,6,7) | 13 |
| 6+6+6 | (4,4,6) | (1,7,7) | 13 |
| 6+6+6 | (4,5,5) | (1,7,7) | 12 |
| 6+6+6 | (4,5,6) | (0,8,7) | 12 |
| 6+6+6 | (5,5,5) | (0,8,7) | 11 |
| 6+6+6 | (5,5,5) | (6,1,8) | 6 |
| 6+6+6 | (5,5,6) | (5,2,8) | 6 |
| 6+6+6 | (5,6,6) | (4,3,8) | 6 |
| 6+6+6 | (6,6,6) | (3,4,8) | 6 |

The twelve 5+6 rows are distinct from the three previously excluded
charge profiles (1,6;8,0,8), (5,2;8,0,8), and (2,5;8,0,8).
The same capacity rule also rejects six raw single-four rows;
these are redundant controls because that branch is already closed.

The next recorded profile (2,6;7,1,8) satisfies A+P=8,
so this theorem leaves it open. Sharper partition-charge constraints
may reduce the pure even six-point defect's allowed hole contribution
below this general bound. They must be derived before reducing that
profile to an anchored heptad cover; the capacity inequality alone
does not exclude it.

## Exact controls and evidence

The [checker](../develop/check_dimension_seven_hole_capacity.py)
independently regenerates all raw size-four profiles by direct
parity counts and by the integer-parameter formulas. It compares
the resulting 9,46,48 sets with the prior report, computes the
capacity bounds in two ways, and preserves every remaining row
without a feasibility assertion. It binds the prior completion,
count, and charge artifacts and their source hashes.

In fixed symplectic coordinates it checks both hole Lagrangians,
all even hole pairs and triples, and all single-odd-member
exclusions. These small local controls test the capacity mechanism,
not all defect classes or common colorings. The universal statement
follows from isotropy, odd-hole membership and counting.

The [report](../results/dimension-7-hole-capacity.json) separates
the eight new C=8 exclusions using written completion from the
thirteen C=7 exclusions retaining the prior finite completion
input. No prior spread enumeration, covering search, SAT, DRAT,
Lean or independent Pro review is run. The submitted manuscript
and public Zenodo PDF are unchanged. The original dimension-six
formal theorem retains three standard and four native-evaluation
axioms. The completed lower bound nineteen does not depend on
finishing the remaining nineteen-color feasibility research.

```sh
python3 develop/check_dimension_seven_hole_capacity.py --report /tmp/dimension-7-hole-capacity.json
```
