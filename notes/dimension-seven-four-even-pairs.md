# Two four-even defect sums force an impossible normalized cover

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic class
size four cannot have outside defects of sizes five and six with
even counts (k5,k6)=(4,4) and saturated counts (A,B,C)=(7,1,8).

The proof uses written charge and nondegenerate-span arguments, a
recoloring reduction to an earlier excluded size-three branch, and
a new independently audited finite covering certificate for the
remaining normalized case. The defect sizes five and six are
distinguished throughout; the earlier two-six theorem alone does
not exclude this profile.

Nineteen of the original forty-six 5+6 raw profiles are now excluded;
twenty-seven remain unexcluded. Nine of forty-eight 6+6+6 raw profiles
are excluded; thirty-nine remain unexcluded. The remaining rows have
no joint-feasibility claim. Characteristic sizes four through eight
and exact dimension-seven chromatic numbers remain open, with lower
bound nineteen and no nineteen-color witness.

## Both even sums lie in the hole Lagrangian

Put E=z-perp and C_z={z,z+e,z+f,z+g}, with h=e+f+g. The eight
pure odd heptads leave the nonzero points of a Lagrangian M by the
[written eight-spread completion theorem](dimension-seven-nineteen-obstruction.md).
These seven odd projections partition into e,f,g, the D5 projection
a, the D6 projections c,d, and the mixed projection b.

Let p and q be the sums of the four even members of D5 and D6,
respectively. Partition charge gives

```text
h=a+c+d+b,       (p+a)+(q+c+d)=h,       p+q=b.
```

The [quadratic partition identity](dimension-seven-size-four.md)
requires w5 dot w6=0: A+B=8, while both defect taus are zero.
Using isotropy of M and the four-even pairings gives

```text
p dot a=0,       q dot c=q dot d=0,
p dot c=p dot d=q dot a=0,
w5 dot w6=p dot b=0.
```

The four distinct nonzero points a,c,d,b span M, since a two-space
has only three nonzero points. Thus p annihilates M, so p belongs
to M-perp=M inside E. Then q=p+b also belongs to M.

The four-even Gram matrix has zero diagonal and ones off diagonal.
Over F_2 it is nonsingular: it is I+J and (I+J)^2=I in order four.
Each four-even span W consequently has dimension four and is
nondegenerate. Its even sum is nonzero and pairs to one with each
of its four members. In particular p,q are nonzero and distinct,
because p+q=b is nonzero. These sums are not Gram radicals.

## One six-defect odd projection equals its even sum

Let W be the four-even span of D6. Every even member pairs to one
with q,c,d, so c+q and d+q belong to W-perp. They also belong to M.
The two-dimensional space W-perp is nondegenerate alternating;
its isotropic subspaces have dimension at most one. If q differed
from both c and d, then c+q,d+q would be two distinct nonzero
points in the isotropic intersection W-perp intersect M, a
contradiction. Relabel c,d so that c=q.

The point p is distinct from q=c and b. There are three possibilities:

1. If p is a characteristic projection, move z+p from the
   characteristic class to D5. It pairs to one with every D5 even
   member and with its odd member z+a. This produces a valid
   nineteen-coloring with a size-three characteristic class and
   two defects of type (4 even,2 odd), retaining (A,B,C)=(7,1,8).
   The [earlier audited two-six theorem](dimension-seven-four-four-hole-cover.md)
   excludes it.
2. If p=a, retain the current classes.
3. If p=d, move z+p from D6 to D5. The new D5 has size six;
   the old D6 now has size five. Relabel them by their sizes.
   The new five-defect even sum is q, equal to its sole odd
   projection q; the new six-defect even sum is p, equal to one
   of its odd projections p. Thus this becomes case 2, with
   the even sums exchanged. No characteristic point moves.

All possibilities are covered without a marked-orbit assumption.
In the remaining case a=p and c=q, the four outside odd projections
are p,q,d,b=p+q. Hence d lies outside span(p,q), h=d is nonzero,
and the characteristic projections are

```text
{d+p, d+q, d+p+q}.
```

Every pure even heptad must meet M once: all other even-containing
classes have an odd projection in M and therefore contain no even
point of M; seven even hole points have exactly seven pure even labels.

## A universal normalization and one further recoloring reduction

The ordered basis (p,q,d) of M extends to a symplectic basis of E.
An isometry sends it to (3,12,48) and extends to the original dot
space by fixing z=127. Thus every remaining case normalizes to

```text
(p,q,d,b)=(3,12,48,15),
characteristic projections={51,60,63},
D5 odd member=124,       D6 odd members={115,79},
mixed odd member=112.
```

If any characteristic projection x pairs to one with all four D5
even members, move z+x into D5. Its pairing with z+p is one by
isotropy of M. This again gives the previously excluded size-three
two-six profile. Therefore each remaining D5 block has sum 3 and
has no such compatible characteristic projection among 51,60,63.

There are 160 four-even cliques with sum 3. Forty-eight allow this
last recoloring, leaving 112. The D6 block has sum 12 and pairs
to one with 12,48; there are sixteen choices. The mixed even
sextet has sum 15; there are thirty-two choices. All these blocks
avoid M. Disjoint triples give 18,752 ordered roots but only
18,656 distinct remaining sets: distinct defect partitions can
leave the same set. Each remaining set has 49 points, including
all seven holes, and must partition into seven anchored heptads.

## The new finite covering proof and its dependencies

The [bounded builder](../develop/build_dimension_seven_four_even_pairs.py)
writes a certificate only after every required root fails. Its
default limits are 150,000 failed states, 1,000,000 visits and
30 seconds. An exhausted budget or a found cover produces no
exclusion certificate.

The [independent auditor](../develop/check_dimension_seven_four_even_pairs.py)
reconstructs catalogs with bitmask clique enumeration, independently
of the builder's array recursion. It reconstructs every ordered
root, checks every possible eligible pivot-heptad successor, and
checks reachability of all recorded failed states. There are 224
anchored heptads among the 288 even heptads. Each successor has
seven fewer points; the empty set is never marked failed. Induction
from leaves therefore excludes every root. The certificate has 72,384
reachable failed states, 54,432 branches and 40,304 leaves. Exact
counts appear in the [report](../results/dimension-7-four-even-pairs-check.json).

The earlier size-three covering certificate remains an explicit
dependency of the two recoloring steps; it is separately reaudited.
The new [certificate](../results/dimension-7-four-even-pairs-proof.json)
handles the remaining size-four normal form and is not substituted
for that earlier proof. Fixed-M local controls check the charge-member
lemma on all qualifying four-even blocks and the normalization on
all 168 ordered bases of M against the original dot product. They
support the universal written arguments without enumerating complete
colorings or partial spreads.

No SAT, DRAT, Lean or new independent Pro review is claimed. The
submitted manuscript and Zenodo PDF are unchanged. The original
dimension-six formal theorem retains three standard and four
native-evaluation axioms.

```sh
python3 develop/build_dimension_seven_four_even_pairs.py --certificate /tmp/dimension-7-four-even-pairs-proof.json
python3 develop/check_dimension_seven_four_even_pairs.py --certificate /tmp/dimension-7-four-even-pairs-proof.json --report /tmp/dimension-7-four-even-pairs-check.json
```
