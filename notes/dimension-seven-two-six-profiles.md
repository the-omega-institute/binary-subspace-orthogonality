# Two six-point defects: three necessary profiles remain

**Theorem.** A nineteen-coloring of Gamma_7 with a three-point
characteristic class must have two six-point defects and sixteen
saturated outside classes. Of their 21 nonnegative count profiles,
eighteen are impossible by the arguments below. Three remain necessary
candidates, with realizability open. In particular, if there are
eight pure odd heptads, only (m_1,m_2; A,B,C)=(4,4;7,1,8) remains.

Here m_i counts even members of defect D_i, m_1<=m_2; A,B,C count
pure even heptads, mixed (6,1) classes, and pure odd heptads.
The [one-five branch](dimension-seven-one-five-exclusion.md) is
already excluded. The exact line and full-subspace chromatic numbers
remain open with lower bound nineteen. No nineteen-color witness,
new numerical bound, or exclusion of the entire three-point branch
is claimed.

## The count equations and defect charges

Six-point classes allow m_i in {0,2,4,5,6}. Set m=m_1+m_2.
The necessary counts are

```text
7A+6B+m=63,
B+7C+12-m+3=64,
A+B+C=16.
```

Equivalently, B=m+7t, A=9-m-6t and C=7-t. Nonnegativity permits
only C=6,7,8 and yields 21 profiles. With C_z={z,z+e,z+f}, put
h=e+f. The existing projected-sum and quadratic identities give

```text
w_1+w_2=h,
w_1 dot w_2=A+B+tau_1+tau_2,
tau_i=1+binom(6-m_i,2) modulo 2.
```

All identities concern classes in one common coloring.

**Charge-member lemma.** For a six-point class with m=2 or m=4,
its charge w is the projection of an odd member of that same class.
Its odd count is even, so w is also its ordinary vector sum.
An even member pairs to one with w, so w is nonzero.
For every v in the class,

```text
v dot(z+w)=v dot z+v dot v+5=1.
```

If z+w were a new member, adjoining it would produce an independent
seven-point class of type (2,5) or (4,3). The saturated-class capacity
lemma excludes both types. Hence z+w already belongs to the class.
For a pure even six-point class, z+w is instead a proper seventh
member, giving a mixed (6,1) class.

## Eight odd heptads leave only one profile

The eight pure odd heptads leave the seven nonzero points of a
Lagrangian M by the written eight-spread completion theorem. All
remaining odd projections, including e,f and defect projections,
lie in M.

The seven even points of M form a clique. Mixed labels and every
defect label with an odd member are forbidden on it. The characteristic
and pure odd labels are forbidden as well. A pure even defect provides
at most one additional label. Thus A plus the number of pure even
defects must be at least seven. This excludes five profiles:

| (m_1,m_2) | (A,B,C) | Available label upper bound on M |
| --- | --- | --- |
| (4,5) | (6,2,8) | 6 |
| (4,6) | (5,3,8) | 6 |
| (5,5) | (5,3,8) | 5 |
| (5,6) | (4,4,8) | 5 |
| (6,6) | (3,5,8) | 5 |

For (2,5;8,0,8), the charge-member lemma gives w_1 in M. Since
h is in M, w_2=h+w_1 is in M too. But the odd projection g of
the (5,1) defect satisfies w_2 dot g=5 modulo2=1. Its five even
members each pair to one with g. This contradicts isotropy of M.

For (2,6;7,1,8), write the first defect as
D_1={u,v,z+g_1,...,z+g_4}. The four g_i are exactly the affine
plane {x in M: ell(x)=1}, where ell(x)=u dot x. They sum to zero.
The characteristic projections e,f are outside that plane, so
ell(h)=0. The charge-member lemma gives w_1 in the plane; hence
w_2=w_1+h also lies in it. Therefore the odd vector z+w_2 belongs
to D_1. Move it to the pure even six-point class D_2, whose sum
is w_2. It pairs to one with all six members of D_2, so the move
preserves proper coloring. D_1 now has size five, D_2 size seven,
and C_z still size three, contradicting the already excluded one-five
branch. This is a conditional recoloring argument, not a constructed
coloring or a new exact-cover search.

Only (4,4;7,1,8) survives among the eight C=8 count profiles.

## Seven odd heptads are impossible in this branch

For C=7, the preceding finitely proved completion lemma gives two
transverse hole Lagrangians M,N. Their fourteen even points must
all be colored. Every pure even heptad meets each hole Lagrangian
in at most one point, contributing at most two. A mixed class has
its odd projection on one side, forbidding that side, and contributes
at most one point on the other. A pure odd six-point defect has no
even members; a defect with both parities contributes at most one
hole point, since its odd members forbid at least one side; a pure
even defect contributes at most two. Therefore

```text
14 <= 2A+B+b(m_1)+b(m_2),
b(0)=0, b(2)=b(4)=b(5)=1, b(6)=2.
```

The four profiles (2,5;2,7,7), (2,6;1,8,7), (4,4;1,8,7), and
(4,5;0,9,7) have upper bounds 13,13,12,11 and are excluded.

For (0,0;9,0,7), the nine pure even heptads would partition all
63 even points. Each has odd quadratic sum, while the full even
point set has even quadratic sum. This is the existing quadratic
partition obstruction and needs no new enumeration.

For a pure odd six-point defect, its projections lie entirely in
one hole Lagrangian M: a mutually orthogonal set meeting both sides
has at most four points. It occupies six of M's seven nonzero
points, leaving at most one mixed odd projection there. This gives
the following bounds on the seven-clique in N:

| Profile | Reason | Label upper bound on N |
| --- | --- | --- |
| (0,4;5,4,7) | The other defect has an odd point in N and is forbidden there | 5+1=6 |
| (0,5;4,5,7) | Its odd point either forbids N or occupies the sole remaining M point; at most one mixed/defect label is available in addition to pure even labels | 4+1=5 |
| (0,6;3,6,7) | At most one mixed label and one pure even defect label supplement pure even labels | 3+1+1=5 |

For (0,2;7,2,7), write the missing point of the pure odd defect's
M as a. Its charge is a. The four odd projections of the other
defect lie in one hole Lagrangian: a split of three-plus-one would
contradict pairing to one with an even member. They cannot lie in M,
which has only one free point, so they lie in N. By the charge-member
lemma its charge w_2 is one of them. The equation e+f=a+w_2 then
forces {e,f}={a,w_2}, violating disjointness from the second defect.

Finally consider (2,2;5,4,7) and (2,4;3,6,7). The first defect's
four odd projections form an affine plane G in one hole Lagrangian
M, and its charge w_1 belongs to G. The second charge w_2 is also
an odd member of its defect. If w_2 lay in N, e+f=w_1+w_2 would
force a characteristic projection to equal a defect projection.
Thus w_2 lies in M, and the nonzero sum h forces e,f into M too.
Both e,f are outside G, hence lie in the kernel of its affine
functional ell. But ell(w_1)=1, so ell(w_2)=ell(w_1+h)=1.
This puts w_2 in G, making the two defect classes overlap. Both
profiles are impossible. All eleven C=7 profiles are now excluded.

## The three remaining necessary profiles

| (m_1,m_2) | (A,B,C) |
| --- | --- |
| (0,0) | (3,7,6) |
| (0,2) | (1,9,6) |
| (4,4) | (7,1,8) |

These are count candidates, not jointly realized class partitions.
The C=8 survivor and the two C=6 profiles give concrete next targets;
no feasibility assertion follows from the table. The C=6 cases leave
21 odd-projection holes; no completion claim for six Lagrangians is made.

## Verification and dependencies

The [checker](../develop/check_dimension_seven_two_six_profiles.py)
independently enumerates the counts by direct A,B,C loops and by
the t formulas. It records all eighteen written exclusions and three
survivors. For the charge-member lemma it checks 16 (2,4) local
classes over a specified affine odd plane and 32 (4,2) local
classes over a specified orthogonal odd pair. These are local controls,
not a new enumeration of all six-point classes.

It checks the conditional (2,6) transfer on every compatible pure
even six-class for those 16 local first defects, reconstructing the
forced-sum six-classes directly. Each valid partial pair transfers
to independent classes of sizes five and seven. It also verifies
all 84 distinct characteristic/charge quadruples in a fixed pair
of hole Lagrangians that satisfy the sum and orthogonality conditions;
all have charge pairing zero. It verifies that no characteristic
pair avoids the forced charge collisions for 49 local pure-odd/mixed
charge configurations or 40 local affine-plane/member-charge
configurations. These are local controls of the written arguments.
It also checks all fourteen local six-odd hole subsets and the fourteen
mixed four-odd subsets; the former stay on one side, and the latter
have no even vector pairing to one with every member.
No complete coloring is enumerated.

The [report](../results/dimension-7-two-six-profiles.json) binds this
note, the checker and earlier proof reports. The eight-spread theorem,
the finite seven-spread lemma, and the one-five exclusion remain
explicit dependencies. Their existing inputs are preserved; no spread
enumeration, SAT, DRAT or Lean is rerun. The submitted manuscript at
28e27a8 is unchanged; the original dimension-six theorem retains three
standard and four native-evaluation axioms. Independent Pro review
of this new deduction is pending.

```sh
python3 develop/check_dimension_seven_two_six_profiles.py --report /tmp/dimension-7-two-six-profiles.json
```
