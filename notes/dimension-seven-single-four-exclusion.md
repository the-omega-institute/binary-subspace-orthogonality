# The single-four-point-defect branch is impossible

**Theorem.** A nineteen-coloring of Gamma_7 with a characteristic
class of size four cannot have just one outside defective class of
size four. The [size-four analysis](dimension-seven-size-four.md)
already excludes eight of its nine count profiles. This note excludes
the remaining profile (D even,odd; A,B,C)=(2,2;7,2,8).

The proof uses a written normalization of the even covering data and
the existing [failed-state certificate](../results/dimension-7-hole-cover-proof.json).
It does not require a new covering search or an orbit classification
of the full marked characteristic and defective classes. Characteristic
size four still has the outside patterns 5+6 and 6+6+6 open, with
46 and 48 raw count profiles respectively. Sizes four through eight
and the exact dimension-seven chromatic numbers remain open; the
numerical lower bound remains nineteen.

## The necessary covering data

Put E=z-perp and write the characteristic class as
C_z={z,z+e,z+f,z+g}, with h=e+f+g. The eight pure odd heptads
give eight disjoint Lagrangians. By the written eight-spread completion
lemma, the remaining seven odd projections form M minus {0}, for a
Lagrangian M. These seven points are partitioned into the characteristic
projections {e,f,g}, the defective odd projections {a,b}, and the
mixed odd projections {x,y}. Write

```text
D={u,v,z+a,z+b}.
```

The global projected-sum equation gives u+v+a+b=h. The sum of
all seven nonzero points of M is zero, so

```text
r=u+v=h+a+b=x+y in M.
```

Consequently u and v restrict to the same linear functional ell on M.
Independence of D gives ell(a)=ell(b)=1 and u dot v=1; hence
ell(r)=u dot(u+v)=1. Since r=x+y, exactly one of x,y has ell-value
zero. Order them so ell(x)=0 and ell(y)=1. These deductions apply
to both previously recorded locations of h, in D or in a mixed class.

All seven even points of M must receive the seven pure even labels.
Each characteristic, mixed, or defective label is forbidden there by
an odd member whose projection lies in M. Each pure odd label is
also forbidden: on its Lagrangian L, any m in M has a nonzero point
in the kernel of m dot(-), giving an orthogonal odd neighbor.
The seven points of M are pairwise orthogonal, so each pure even
heptad must meet M in exactly one point.

## A universal normalization of the covering problem

Choose a nonzero a0 in ker(ell) different from x, and put b0=a0+x.
Then a0,b0 form a basis of ker(ell), and (a0,b0,r) is a basis of M.
The vector u pairs with this basis as (0,0,1). Choose a symplectic
dual completion (d1,d2,u), with d1,d2 orthogonal to u and to each
other. Such a completion exists: the plane spanned by r,u is
nondegenerate, its perpendicular complement contains a0,b0 as a
Lagrangian, and a symplectic dual basis in that complement supplies
d1,d2. An isometry of E sends

```text
(a0,b0,r,d1,d2,u) -> (3,12,48,65,71,95).
```

It fixes the following covering data, regardless of the positions of
the characteristic or defective odd markings:

```text
M -> {0,3,12,15,48,51,60,63},
u -> 95,  v=u+r -> 111,
x=a0+b0 -> 15,  y=x+r -> 63.
```

Every isometry of E extends to the original dot space by fixing z.
The six even members of each mixed class have vector sum equal to
its odd projection, by the forced-completion identity for even
six-cliques. Thus their normalized sums are 15 and 63. Each has
32 possible six-cliques. Excluding 95,111 and requiring the two
six-cliques to be disjoint leaves precisely the same 384 ordered
roots as the earlier completed-hole certificate. Each root leaves
49 even points to partition into seven heptads meeting M once.
The existing certificate excludes every such root, proving the theorem.

## Finite verification and scope

The [checker](../develop/check_dimension_seven_single_four_exclusion.py)
reconstructs all 1,008 fixed-M local configurations, preserving the
charge equation and disjoint characteristic/defective markings.
There are 672 with h in the defect and 336 with h in a mixed class.
For each it builds the source basis, checks the seven-dimensional
Gram matrix and induced bijection, and verifies the four normalized
covering data above. This is a local control of the universal written
argument, not an enumeration of all complete colorings.

The checker independently reconstructs all 2,016 even six-cliques,
288 heptads, and 224 heptads meeting M once. It compares all 384
roots with the existing certificate and rechecks its entire acyclic
failed-state graph: 1,784 reachable states, 1,400 branches, and
968 leaves. No builder or new exact-cover search is run. The
[report](../results/dimension-7-single-four-exclusion.json) binds the
prior certificate, audit and size-four analysis to their exact bytes.

This closes the single-four-defect branch only. The submitted
manuscript at 28e27a8 is unchanged; no Lean or independent Pro
review is claimed. The dimension-six formal theorem still depends
on three standard and four native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_single_four_exclusion.py --report /tmp/dimension-7-single-four-exclusion.json
```
