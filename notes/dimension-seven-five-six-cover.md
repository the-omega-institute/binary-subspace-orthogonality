# Two five-plus-six exclusions from the common even sum

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic class
size four cannot have outside defects of sizes five and six with
even counts (k5,k6)=(2,6) and saturated counts (A,B,C)=(7,1,8).
The same common-even-sum framework also excludes
(k5,k6;A,B,C)=(3,4;8,0,8) by a written charge-parity argument.

The proof derives the covering data without fixing the characteristic
markings or assuming zero characteristic charge. A written symplectic
normalization then reduces every candidate to the same 384 roots of
the existing checked [hole-cover certificate](../results/dimension-7-hole-cover-proof.json).
No new covering search or spread enumeration is required.

Together with the [uniform hole-capacity exclusions](dimension-seven-hole-capacity.md)
and earlier charge arguments, seventeen of the original forty-six 5+6
raw profiles are excluded; twenty-nine remain unexcluded. Nine of the
forty-eight 6+6+6 profiles are excluded; thirty-nine remain unexcluded.
The unexcluded rows have no joint-feasibility claim. Characteristic
sizes four through eight and exact dimension-seven chromatic numbers
remain open, with lower bound nineteen and no nineteen-color witness.

## Partition charge forces the pure even defect to avoid the holes

Put E=z-perp and C_z={z,z+e,z+f,z+g}, with h=e+f+g.
The eight pure odd heptads give eight disjoint Lagrangians. The
[written eight-spread completion theorem](dimension-seven-nineteen-obstruction.md)
identifies their seven holes as M minus {0}, for a Lagrangian M.
These seven points partition into the characteristic projections
e,f,g, three odd projections a1,a2,a3 in D5, and the odd projection
b of the single saturated mixed class. Write

```text
D5={u,v,z+a1,z+a2,z+a3},
D6={s1,s2,s3,s4,s5,s6},
t=a1+a2+a3,  r=u+v,  c=s1+s2+s3+s4+s5+s6.
```

Both restrictions u dot(-)|M and v dot(-)|M take value one at
three distinct points. Distinct nonzero functionals on a binary
three-space have only two simultaneous value-one points, so these
restrictions agree. Thus r lies in M=M-perp. For the common
functional ell, independence of u,v gives ell(r)=u dot v=1.

The seven nonzero points of M sum to zero, giving h=t+b. The
global projected-sum identity for the two defects now gives

```text
(r+t)+c=h=t+b,  hence c=r+b in M.
```

An even six-clique has nonzero vector sum c, distinct from its
members, and c pairs to one with each member. Indeed its
off-diagonal-one Gram matrix is nonsingular in even size six,
so its vectors are independent; pairing their sum with a member
gives five mod two, or one. Appending c gives its unique even
heptad completion. Hence b=r, which would give c=0, is impossible.
Since c belongs to isotropic M and pairs to one with every s_i,
none of the six defect members belongs to M.

The saturated mixed class also has six even members summing to
b, by its zero projected charge; its odd member excludes every
even point of M. The two even members u,v of D5 avoid M because
ell is nonzero, while the characteristic and pure odd classes
contain no even vectors. Thus the seven pure even heptads must
partition the seven even points of M, each meeting M exactly once.

The general capacity bound allowed the pure even defect one hole
point, giving A+P=8. The charge identity sharpens its contribution
to zero and forces all seven heptads to be anchored in M.

## Normalize the two distinct six-class roles

The mixed even six-clique has sum b; the pure even defect has sum
c=r+b. These are distinct nonzero points of M. Because ell(r)=1,
exactly one of b,c has ell-value zero. Call it x and put y=x+r,
the other point. Choose a0 in ker(ell) minus {0,x} and b0=a0+x.
Then (a0,b0,r) is a basis of M, and u pairs with it as (0,0,1).

The plane spanned by r,u is nondegenerate. Its perpendicular
complement contains a0,b0 as a Lagrangian, so choose a symplectic
dual pair d1,d2 there. An isometry of E sends

```text
(a0,b0,r,d1,d2,u) -> (3,12,48,65,71,95).
```

Extend it to the original dot space by fixing z. It normalizes

```text
M minus {0} -> {3,12,15,48,51,60,63},
u -> 95,  v=u+r -> 111,
x=a0+b0 -> 15,  y=x+r -> 63.
```

Therefore the two six-cliques have sums 15 and 63 in some order.
Their roles remain distinct: one is the even part of a saturated
mixed class, the other the pure even six-point defect. The certificate
orders them by their sums, and therefore covers both role assignments.
There is no assertion that all characteristic and odd-defect markings
form one orbit.

Each forced sum has 32 six-clique choices. Requiring disjointness
and excluding 95,111 gives precisely the same 384 ordered roots
as the existing certificate. Each leaves 49 even points to partition
into seven heptads meeting M once. The certificate excludes every
such root. Dropping the remaining odd markings only relaxes this
necessary covering problem, so its failure excludes the target profile.

## With no saturated mixed classes, one parity test excludes all four raw rows

Suppose C=8 and B=0, with two outside defects D5 and D6. Write
U_i for the sum of a defect's even members and S_i for the sum of
its odd projections, all of which lie in M. The characteristic
projections and defect odd projections partition M minus {0}, so
h=S5+S6. The partition identity then gives

```text
w5=U5+S5,  w6=U6+S6,  w5+w6=h,
U5=U6=U.
```

Consequently isotropy of M gives

```text
w5 dot w6=U dot(S5+S6)=k5*o5+k6*o6 mod 2.
```

Here each even member pairs to one with each odd projection in
its own independent class, and the same U is the even sum in
both classes. The [general quadratic partition identity](dimension-seven-size-four.md)
requires this product to equal A+B+tau5+tau6. Thus every such
profile necessarily satisfies

```text
k5*o5+k6*o6 = A+B+tau5+tau6 mod 2.
```

All four raw C=8,B=0 rows fail this test:

| (k5,k6;A,B,C) | Computed product | Required product | Status before this note |
| --- | --- | --- | --- |
| (1,6;8,0,8) | 0 | 1 | Previously excluded |
| (2,5;8,0,8) | 1 | 0 | Previously excluded |
| (3,4;8,0,8) | 0 | 1 | New exclusion |
| (5,2;8,0,8) | 0 | 1 | Previously excluded |

This uniformly recovers the three prior C=8,B=0 exclusions and
closes the fourth row. No finite cover input or assumption h=0
is needed for this corollary.

## Exact controls and retained proof dependencies

The [checker](../develop/check_dimension_seven_five_six_cover.py)
reconstructs the 448 fixed-M local D5 classes, checking the prior
catalog identity. All four unused hole points are considered as b.
Of the 1,792 placements, 112 force c=0 and fail the six-clique
condition. For the other 1,680, it verifies c=r+b, both class roles,
the symplectic basis Gram matrix and the induced bijective map.
There are 336 with h=0 and 1,344 with h nonzero; 1,344 put b at
normalized 15 and 336 put it at 63. These are conditional local
data, not complete colorings or assertions of joint feasibility.

For the normalized cover, independent bitmask six-clique and array
heptad constructions agree on all 2,016 even six-cliques and 288
heptads. The 224 heptads meeting M once and all 384 roots are
reconstructed from the original dot product. The existing acyclic
failed-state graph is checked in full: 1,784 reachable states,
1,400 branches and 968 leaves. No builder or new covering search
is run. Its exact bytes and previous audit/source identities are
bound in the [new report](../results/dimension-7-five-six-cover.json).

The checker also verifies 4,096 common-even-sum product identities
in fixed coordinates and reconstructs the parity mismatch in each
of the four raw C=8,B=0 rows. Only the (3,4;8,0,8) row is newly
excluded by this uniform written test.

The (2,6;7,1,8) exclusion combines written charge/normalization proofs
with the existing finite cover certificate. The (3,4;8,0,8) exclusion
has a written common-even-sum parity proof. Both use written eight-spread
completion; the unrelated prior finite seven-spread enumeration is
not rerun. No SAT, DRAT, Lean or independent Pro review is claimed.
The submitted manuscript and Zenodo PDF are unchanged. The original
dimension-six formal theorem retains three standard and four
native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_five_six_cover.py --report /tmp/dimension-7-five-six-cover.json
```
