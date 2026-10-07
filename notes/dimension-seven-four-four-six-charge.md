# A transferable pure-six sum excludes (4,4,6;7,0,8)

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic
class size four cannot have profile (4,4,6;7,0,8).

The pure even six-class has sum in the hole Lagrangian M. Its
corresponding odd vector can therefore be transferred from either
the characteristic class or a mixed six-defect. These two moves
give exactly two profiles already excluded by earlier theorems.
This is a new written reduction with inherited finite covering
premises; it needs no new normal form, stabilizer or cover search.

Exactly this three-six row is removed, leaving 25 five-plus-six
and 37 three-six count candidates. Three three-six C=8 rows remain.
Characteristic sizes four through eight and exact n7 remain open,
with lower bound nineteen.

## The charge-member lemma determines the pure sum

Put E=z-perp. The [written eight-spread theorem](dimension-seven-nineteen-obstruction.md)
leaves the seven nonzero points of a Lagrangian M as the remaining
odd projections. Write D1,D2 for the two six-defects with four
even and two odd members, and P for the pure even six-defect.

The [charge-member lemma](dimension-seven-two-six-profiles.md)
says that the projected charge of a (4,2) six-class is the
projection of one of its odd members. Name the odd projections
of D1 as a,b, with charge b, and those of D2 as c,d, with charge d.
The sums of their four even members are then a,c, respectively:
for example, U1+a+b=b gives U1=a. All four projections are distinct.

The characteristic projections are the three unused nonzero points
of M. Since all seven points sum to zero, their charge is
h=a+b+c+d. Writing q for the even sum of P, the partition charge
identity gives

```text
b+d+q=h=a+b+c+d,  hence q=a+c in M minus {0}.
```

The pure six-class Gram matrix is nonsingular; q is nonzero,
absent from P and pairs to one with every member of P. Its
members therefore avoid M. Both mixed defects also avoid even
M points because they have odd projections in isotropic M.
Thus all seven even holes would be assigned to the seven pure
even heptads. This geometry is necessary, but a new cover
obstruction is unnecessary because q itself permits a transfer.

## Every location of z+q gives an excluded coloring

The vector z+q is odd and belongs to the current coloring. Its
projection q lies in M, so it is outside the eight pure odd heptads.
It cannot lie in P, which is pure even. It must therefore lie in
the characteristic class or one of D1,D2. Moreover q=a+c differs
from a and c, so if it lies in a mixed defect its projection is
that defect's charge b or d.

Move z+q into P. For every p in P,
p dot(z+q)=p dot q=1, so the enlarged class is independent and
has type (6 even,1 odd). Removing the vector from its original
class preserves independence. No class becomes empty and the
number of labels stays nineteen. There are two cases:

1. If z+q came from the characteristic class, that class now has
   size three. The two remaining defects have type (4,2), and
   the saturated counts become (A,B,C)=(7,1,8). The
   [earlier size-three two-six theorem](dimension-seven-four-four-hole-cover.md)
   excludes precisely this coloring.
2. If it came from D1 or D2, the characteristic class stays size
   four. One defect now has size five with four even/one odd
   members, and the other is still a six-defect with four even/two
   odd members. The saturated counts are again (7,1,8). The
   [earlier four-even-pair theorem](dimension-seven-four-even-pairs.md)
   excludes the five-plus-six profile (4,4;7,1,8).

Every possible location of z+q is covered. Hence the original
(4,4,6;7,0,8) profile is impossible.

Both cited exclusions combine written reductions with historical
independently audited finite covering certificates. This theorem
inherits those premises. It is not a computation-free exclusion,
and it does not use a different profile's certificate as an
unjustified cover proof: the transfer produces the exact profiles
to which the earlier theorems apply.

## Local controls and exact accounting

The [checker](../develop/check_dimension_seven_four_four_six_charge.py)
compares independent array and bitmask four-clique and six-clique
catalogs. In fixed M it considers all 840 ordered assignments of
a,b,c,d. There are 504 with q a characteristic projection and
336 with q a mixed-defect charge. For every ordered distinct
sum/charge pair, it checks all sixteen original (4,2) classes,
including their ordinary charge and absence of even holes.
For every q in M minus {0}, it checks all 32 pure sextets and
their mixed-heptad completions. Source reductions, original
class disjointness and union preservation are checked for every
compatible disjoint local triple. These controls are partial
classes, not complete nineteen-colorings.

There are 672 original mixed-six controls and 224 pure-six
completions. The two branches contain respectively 1,462,272
and 967,680 compatible disjoint local triples; each transfer
preserves the exact union and all class independence conditions.

The audit checks source, report, certificate and recorded dependency
hash bindings for both inherited theorems without rerunning their
historical covering audits or any spread enumeration. It also
reconstructs all 46/48 raw count rows, finds the target once in
the preceding 38-row three-six list, removes exactly it and leaves
the 25-row five-plus-six list unchanged. The
[report](../results/dimension-7-four-four-six-charge.json)
records the full current lists and both transfer branches.

No new covering certificate, Lean or independent Pro review is
claimed. The original six-dimensional formal theorem retains
three standard plus four native-evaluation axioms. The submitted
snapshot is preserved; the result is included in the authorized
extended working draft, with publication and submission undecided.

```sh
python3 develop/check_dimension_seven_four_four_six_charge.py --report /tmp/dimension-7-four-four-six-charge.json
```
