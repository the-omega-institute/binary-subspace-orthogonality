# Capacity equality for the C=7 four-four-four profile

This note records the equality-case reduction for the necessary profile
`(4,4,4;3,5,7)`. No raw profile is excluded; the count lists stay 25/34
and exact n=7 remains open with lower bound 19.

**Theorem.** Up to exchanging the two hole Lagrangians, every hypothetical
coloring in this profile has one of two odd-projection distributions:

| Case | Defects with odd projections in M/N | Mixed odd projections in M/N | Characteristic projections in M/N | Characteristic charge |
| --- | --- | --- | --- | --- |
| 0 | 0/3 | 4/1 | 3/0 | zero |
| 1 | 1/2 | 3/2 | 2/1 | nonzero |

Each of the three pure even heptads meets both hole sides once. Every
mixed heptad and every defect meets exactly one even hole, on the side
opposite its odd projections. For each defect the projected charge is
one odd projection and its even sum is the other.

## Why capacity equality fixes the side counts

The [finite seven-spread completion theorem](dimension-seven-seven-holes.md)
leaves the disjoint nonzero parts of two transverse Lagrangians M,N,
with E=M direct-sum N. All odd projections outside the seven pure odd
heptads lie in these fourteen points. This retains the existing finite
completion premise, whose audit is not rerun here.

The [hole-capacity bound](dimension-seven-hole-capacity.md) is an equality:

```text
14 = 2A+B+R = 2*3+5+3.
```

The fourteen even holes must be covered, and the individual upper bounds
sum to fourteen. Every class therefore attains its bound: each pure
even heptad has one hole on each side, while each mixed class and each
(4,2) defect has one hole. If a defect's two odd projections occupied
different sides, both sides would be forbidden to its even members,
contradicting its required hole. Thus its odd projections are on one
side and its actual even hole is on the other.

Let y be the number of defects on the M side, x the number of mixed
odd projections there, and k the number of characteristic projections
there. The three pure even heptads use three holes of N. The classes
whose odd projections are in M must use its four remaining holes:

```text
x+y=4.
```

Odd projections partition M's seven points, so x+2y+k=7. Consequently
x=4-y and k=3-y. Exchanging M,N replaces y by 3-y. Hence we may take
y=0 or 1, giving the two rows above. This exchange orders the two hole
sides; it does not assume transitivity on partial spreads or markings.

## Defect charges and characteristic geometry

For a six-point (4,2) class, the existing
[charge-member lemma](dimension-seven-two-six-profiles.md) says that
its projected charge is one of its odd projections. Write the two as
g_i,s_i, with charge g_i. The charge is also the ordinary class sum,
since there are two odd members. Thus the sum of the four even members
is s_i. The roles (g_i,s_i) are distinguished by the actual charge,
although the three defect classes themselves may be permuted.

The [partition and quadratic identities](dimension-seven-size-four.md)
give, with characteristic projections e,f,t and h=e+f+t,

```text
g_1+g_2+g_3=h,
sum_{i<j} g_i dot g_j=0.
```

Here each defect has tau=binom(6,2)+binom(2,2)=0 modulo two, and
A+B=8 is even. All characteristic projections pair to zero.

In case 0 all three g_i lie in N and all characteristic projections
lie in M. The direct sum forces both sums to vanish. Each triple is
therefore the three nonzero points of a two-space on its own side.
In particular the characteristic triple has rank two and h=0.

In case 1 write the characteristic projections as e,f in M and t in N,
and the charges as g_1 in M and g_2,g_3 in N. Direct-sum uniqueness gives

```text
g_1=e+f,  g_2+g_3=t,  e dot t=f dot t=0.
```

The characteristic triple has rank three and h is nonzero. Its
orthogonality also gives the quadratic charge identity, because
g_1 dot(g_2+g_3)=(e+f) dot t=0. These equations must hold in a common
coloring; they do not assert that independent local classes can be
assembled into one.

## Complete odd markings and local actual-hole choices

Normalize the ordered transverse pair to M with basis (3,12,48) and N
with dual basis (65,71,95). Any ordered transverse pair admits this
normalization by sending a basis and its dual to the displayed basis;
the isometry of E extends to the original dot space by fixing z=127.

The [checker](../develop/check_dimension_seven_C7_equality.py) enumerates
the necessary odd markings in two different ways. One chooses
characteristic triples, disjoint same-side odd pairs and their charge
orientations, then filters both charge identities and side counts. The
other directly constructs the two derived charge splits. The exact sets
agree: **1,176 case-0 markings and 3,024 case-1 markings**, or **4,200**
for the fixed ordered hole pair with y<=1. Characteristic triples and
the three charged defects are unordered; each defect's charge and
partner remain distinguished. The five remaining hole points are the
mixed odd projections. These counts are not orbit counts and do not
assume a free action or unique component decomposition.

Independent array and bitmask catalogs agree on all 10,080 even
four-cliques. For each of the 84 ordered same-side (charge,partner)
pairs, precisely eight compatible even blocks have their required
one actual hole. There are **two possible holes on the opposite side**,
the points pairing to one with both odd projections, and four blocks
for each hole. The resulting 672 local defects satisfy the original
graph's independence condition. Among case-0 odd markings, the numbers
of distinct three-defect hole allocations are 2,6,8 for respectively
196,588,392 markings; among case-1 markings they are 6,8 for respectively
1,008,2,016 markings. Thus every necessary odd marking has a local
distinct-hole allocation. Hole choices alone do not exclude either case.

The [report](../results/dimension-7-C7-equality.json) binds the checker,
this proof note, the exact marking-set digest, five inherited reports
and their recorded source/dependency identities. Historical completion
and covering audits are not rerun. No complete jointly disjoint family,
covering search, cover certificate, new Lean or independent Pro review
is claimed. The original n=6 theorem retains three standard plus four
native-evaluation axioms. The next necessary step is joint compatibility
of the three defect blocks with the five mixed components and all
fourteen actual-hole placements, before a complete covering problem.

```sh
python3 develop/check_dimension_seven_C7_equality.py --report /tmp/n7-C7-equality.json
```
