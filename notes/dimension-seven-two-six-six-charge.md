# One marked charge form for the (2,6,6;7,0,8) profile

**Theorem.** In a nineteen-coloring of Gamma_7 with characteristic
class size four and profile (m6,1,m6,2,m6,3;A,B,C)=(2,6,6;7,0,8),
write D0 for the six-class with two even and four odd members and
D1,D2 for the two pure even six-classes. The characteristic charge
is zero. Writing r for the even sum of D0 and q1,q2 for the sums
of D1,D2, necessarily

```text
r in M minus {0},  q1+q2=r,  q1 dot r=q2 dot r=q1 dot q2=0,
q1,q2 outside M.
```

There is one necessary marked form, with full marked stabilizer of
order eight. The pure-six roles become intrinsically distinguished
by their pairing with either even member of D0. This is a reduction,
not an exclusion or a nineteen-color witness. The remaining raw
profile totals stay 25 five-plus-six and 39 three-six; exact n7 stays
open with lower bound nineteen.

## The affine plane and the charge identities

Put z=127, E=z-perp and write

```text
D0={u,v,z+a1,z+a2,z+a3,z+a4}.
```

The eight pure odd heptads leave M minus {0}, for a Lagrangian M,
by the [written eight-spread completion](dimension-seven-nineteen-obstruction.md).
All four a_i and the three characteristic projections lie in these
seven holes. The restrictions of u and v to M take value one at
four distinct points. Two distinct nonzero functionals on a binary
three-space have just two common value-one points, so these restrictions
agree. Call their common nonzero functional ell. The a_i exhaust
the affine plane G={x in M:ell(x)=1}.

Consequently r=u+v lies in M=M-perp, and
ell(r)=u dot(u+v)=u dot v=1. In particular r is one of the four
odd projections. The three characteristic projections are exactly
ker(ell) minus {0}, and their sum h is zero. The four points of G
also sum to zero, so the projected charge of D0 is r. The partition
charge identity gives q1+q2=r.

The [quadratic partition identity](dimension-seven-size-four.md)
has tau=1 for each six-class (the odd counts are 4,0,0) and
A+B=7. Thus the three pair products sum to zero. Substituting
q2=q1+r in the alternating form gives

```text
r dot q1+r dot q2+q1 dot q2=q1 dot r=0.
```

This yields the three asserted vanishing products. Neither pure-six
sum is zero: its off-diagonal-one Gram matrix is nonsingular, its
sum is absent from the class and pairs to one with all six members.

## Recoloring excludes sums inside M

Since q1+q2=r lies in M, either both sums lie in M or neither does.
In the first case ell(q1)+ell(q2)=ell(r)=1, so exactly one sum,
say q2, belongs to G. The odd vector z+q2 belongs to D0 and pairs
to one with every member of D2. Move it from D0 to D2.

The resulting coloring still has nineteen classes and the same
characteristic class. D0 now has size five with two even/three odd
members, D1 is a pure even six-defect, and D2 is a saturated mixed
(6,1) class. Its five-plus-six profile is (2,6;7,1,8), which the
[existing common-even-sum theorem](dimension-seven-five-six-cover.md)
excludes. Hence q1,q2 must lie outside M.

This step inherits the earlier checked 384-root finite hole-cover
certificate through that theorem. It is not a purely written
exclusion. The current audit checks its source/dependency hash bindings
and the new local recoloring, without rerunning the historical cover
or spread audit. No different profile's certificate is used for the
remaining outside-M case.

## Normalize the marked pair and the two sums

Choose a basis of ker(ell), then append r. The plane spanned by r,u
is nondegenerate; choose a symplectic dual basis to ker(ell) in its
perpendicular complement. An isometry of E, extended by fixing z,
normalizes

```text
symplectic basis=(3,12,48;65,71,95),
M minus {0}={3,12,15,48,51,60,63},
r=48,  {u,v}={95,111},
G={48,51,60,63},  characteristic projections={3,12,15}.
```

In coordinates (x,y) relative to this symplectic basis, q dot r=0
forces y3=0. Since q is outside M, (y1,y2) is nonzero. The GL2
action on ker(ell) normalizes this functional to (1,0).
Symmetric shears (x,y)->(x+Sy,y) preserving the unordered even
pair have S13=S23=0, with an arbitrary symmetric upper 2-by-2
block and arbitrary S33. The first column of that upper block
can erase x1,x2 of q.

Finally q dot u=q dot v=x3. Because q2=q1+r and r dot u=1,
the two sums have opposite pairings with u. Name the zero-pairing
sum q1 and the one-pairing sum q2. This normalizes them to

```text
q1=65,  q2=113=65+48.
```

The roles are fixed individually by every marked isometry: their
pairings with the unordered pair {u,v} are invariants.

## The full marked stabilizer and actual hole allocation

An isometry preserving M and the marked even pair fixes r and
preserves ell. Its restriction to M therefore has block form
GL2 times the identity on r. Fixing q1's functional on ker(ell)
leaves two restrictions (3 maps to 3 or 15, 12 and 48 are fixed).
Both lift by (x,y)->(Ax,A-inverse-transpose y). For the remaining
pointwise-M shears, preserving the even pair gives S13=S23=0;
fixing q1 gives S11=S12=0. Only S22 and S33 remain free, giving
four shears. The full marked stabilizer therefore has order 2*4=8.
It may exchange u,v and preserves both pure-six roles individually.

The pure defects need not avoid M. Each contains at most one hole,
because M is isotropic and its even members pair to one. Before
excluding u,v, each sum 65 and 113 has 32 six-clique choices.
After excluding u,v, the catalogs have 32 and 22 choices. Their
384 ordered disjoint pairs have the following actual hole counts:

| Holes in D1 | Holes in D2 | Disjoint pairs |
| --- | --- | --- |
| 0 | 0 | 16 |
| 0 | 1 | 88 |
| 1 | 0 | 64 |
| 1 | 1 | 216 |

The even pair itself avoids M. A pair of pure defects leaves 49
even points, including 7,6 or 5 holes respectively. These must be
covered by seven pure even heptads. Exactly that many heptads meet
M once; the others avoid M. A later covering problem must therefore
retain actual defect holes and allow all 288 even heptads, rather
than prematurely restricting every row to the 224 anchored heptads.
No complete remaining-set family, orbit partition or cover search
is performed here.

## Finite controls

The [checker](../develop/check_dimension_seven_two_six_six_charge.py)
compares independent array and bitmask six-clique/heptad catalogs.
It verifies all 1,152 compatible inside-M recolorings (384 for each
of the three normalized charge pairs) against the original dot product.
All 112 fixed-M first classes and twelve canonical
outside charge pairs each are covered explicitly by all 10,752
M-preserving isometries (168 restrictions and 64 shears): 1,344
normalization controls, each with eight maps. All 526,848 basis Gram
entries and 73,920 original color-class images are checked. The full order-eight
marked group is checked on all point pairs, compositions, catalogs
and disjoint defect pairs.

The [local report](../results/dimension-7-two-six-six-charge.json)
binds the proof, checker, imports and historical dependencies. The
finite audit establishes these local counts and normalization controls;
it does not decide joint coloring feasibility. Both manuscript PDFs
are preserved. No new covering certificate, Lean or independent Pro
review is claimed. The original six-dimensional formal theorem retains
three standard plus four native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_two_six_six_charge.py --report /tmp/dimension-7-two-six-six-charge.json
```
