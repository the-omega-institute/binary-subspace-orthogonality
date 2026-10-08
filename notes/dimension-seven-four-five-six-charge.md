# Completion sources in (4,5,6;6,1,8)

**Theorem.** In any nineteen-color line coloring with characteristic
size four and profile `(4,5,6;6,1,8)`, the pure-six completion q lies
in a pure even heptad Hq. The five-even mixed completion t lies either
in the existing mixed heptad or in a different pure even heptad Ht.
In either case Hq avoids t. The common functional on the hole
Lagrangian has two possible value patterns; one forces the pure source
for t. The profile remains open, with current count totals **25/36**.

## Charge, functional and actual holes

The [written eight-spread theorem](dimension-seven-nineteen-obstruction.md)
leaves the seven nonzero points of M as the remaining odd projections.
Let D0 be the four-even/two-odd six-defect. By the
[charge-member lemma](dimension-seven-two-six-profiles.md), name its
odd projections a,b so that its even sum is a and its charge is b.
Let D1 be the five-even/one-odd six-defect, with odd projection c and
even sum r. Let P be the pure even sextet, with sum q, and J the
existing mixed heptad, whose odd projection and even sum are d.
The points a,b,c,d are distinct nonzero points of M.

The [unique mixed completion lemma](dimension-seven-four-five-five-charge.md)
gives t=r+c outside M. A pure even sextet has nonsingular Gram
matrix I+J, so its six vectors form a basis of E. Their sum q pairs
to one with every member and is its unique even completion.
Neither completion belongs to its recipient class.

The characteristic projections are the other three points of M,
with sum h=a+b+c+d. The partition-charge and quadratic identities
from the [size-four argument](dimension-seven-size-four.md) give

```text
b+t+q=h,       t+q=v=a+c+d in M,
b dot(t+q)+t dot q=1,       t dot q=1.
```

For the quadratic calculation, A+B=7 and the three defect tau
values are 0,1,1. Thus q is outside M, and t,q restrict to a common
nonzero functional ell on M. Since ell(c)=1 and ell(v)=t dot q=1,

```text
ell(a)=ell(d)=eta,       eta in {0,1}.
```

In particular v is nonzero and a,c,d form a basis of M. Both eta
patterns must be retained; importing ell(a)=ell(c)=ell(d)=1 from
the earlier `(4,5,5)` transfer would lose the eta=0 branch.

Any class with an odd projection in M has no even member in M.
Each pure even class meets M at most once. The seven even holes
can therefore occur only in the six pure even heptads and P.
All seven classes meet M exactly once. In particular P has one
actual hole kP, which satisfies ell(kP)=kP dot q=1.

## Exhaustive source transfers

Both t and q are existing even vertices outside M. Neither can
come from the characteristic class or a pure odd class. The exact
partition therefore leaves the following source alternatives.

| Completion | Source | Profile after transfer | Earlier exclusion |
| --- | --- | --- | --- |
| q into P | D0 | `(3,5;7,1,8)` | [Three-plus-five](dimension-seven-three-five-cover.md) |
| q into P | D1 | `(4,4;7,1,8)` | [Four-even pair](dimension-seven-four-even-pairs.md) |
| q into P | J | `(4,5,5;7,0,8)` | [Transferred two-hole cover](dimension-seven-four-six-six-cover.md) |
| t into D1 | D0 | `(3,6;6,2,8)` | [Three-even/pure-six cover](dimension-seven-three-six-cover.md) |
| t into D1 | P | `(5,4;6,2,8)` | [Complete D/H/G/Z theorem](dimension-seven-five-four-Z-cover.md) |

For example, moving q out of J turns J into a five-even/one-odd
six-defect, completes P to a pure heptad and leaves D0,D1 unchanged.
Its saturated counts become (7,0,8), precisely the recently excluded
four-five-five row. Each transfer removes and adds the same existing
vertex, preserving all original-dot-product class conditions and
the full partition. The exclusions in the table therefore force
q into a pure even heptad Hq, and t into J or a pure even heptad Ht.
The pure-source hole of q is distinct from kP. Transferring q alone
exchanges the pure defect with Hq minus {q}; its sum remains q and
its actual hole is retained.

If t lies in J, then t dot d=1, forcing eta=1. Moving t into D1
exchanges the mixed roles c,d: J minus {t} has even sum d+t and
the same unique completion t. This move is reversible, and preserves
the raw profile. Thus eta=0 forces t into a pure heptad.

If both completions came from the same pure heptad, move t into
D1 and q into P simultaneously. Their distinctness follows from
t dot q=1. The source loses two vertices and becomes a pure
five-defect; D0 remains a four-even/two-odd six-defect, while the
saturated counts become (6,2,8). This is exactly the excluded
`(5,4;6,2,8)` row, using **all four D/H/G/Z forms**. Hence Ht,
when present, differs from Hq, and Hq always avoids t.

## The pure-source transfer retains a different branch

If t comes from Ht, moving it into D1 produces `(4,6,6;5,2,8)`.
Its two pure sextets are the original P, with sum q, and
Ht minus {t}, with sum t. They retain distinct actual holes.
One completion is now in its paired mixed class, while q remains
in the distinct pure even heptad Hq. This location differs from
the **paired mixed/mixed** branch excluded by the earlier
[two-hole certificate](dimension-seven-four-six-six-cover.md).
That certificate cannot exclude the present target. Both eta
values remain necessary here. The mixed-source eta=1 alternative
also remains open.

## Local verification and next problem

The [auditor](../develop/check_dimension_seven_four_five_six_charge.py)
compares independent array and bitmask clique catalogs for sizes
4,5,6,7 against the original binary dot product. It checks every
unique fixed-M five-even mixed completion and every pure-six
completion, all ordered charge markings and modular source-removal
controls. It checks the exact profile arithmetic of every transfer,
the reversible mixed-role exchange, retained actual holes and the
common-pure-source two-removal obstruction. These are modular
local controls, not compatible joint roots or full colorings.

There are 1,344 unique five-even mixed completion controls and 2,016
unique pure-six completion controls. The 10,752 ordered markings split
equally between eta=0 and eta=1 and give 224 distinct ordered completion
pairs. Each pair has 24 one-hole pure sextets of sum q and 24 anchored
heptads containing q; in each catalog exactly 18 avoid t. Removing q
from those 4,032 heptads retains their actual holes. The 1,344 shared
pure-source two-removal controls produce the pure-five obstruction.
The distinct modular source controls number 2,688 each for q or t
from D0, and 1,344 each for q from D1, q from J, t from P and t from J.
These counts deduplicate source blocks and removed vertices, rather
than counting each repeated role marking as a new source control.

The [report](../results/dimension-7-four-five-six-charge.json) binds
the sources and all nine inherited covering reports, their certificates
and dependencies, including the inherited size-three two-six premise.
Historical covering audits are not rerun. The written exclusions
retain those finite premises; the new local checks do not replace them.
There is no new covering search, cover certificate, Lean or independent
Pro review. Exact n7 stays open with lower bound 19. The original
n6 theorem retains three standard and four native-evaluation axioms.
The submitted snapshot and historical reports are preserved.

The next bounded problem is to normalize the eta=0 and eta=1
markings together with the pure-source and mixed-source alternatives,
prove their full marked symmetry groups and retain the actual holes
before constructing any complete jointly compatible root catalog.
The count lists remain 25 five-plus-six and 36 three-six rows.

```sh
python3 develop/check_dimension_seven_four_five_six_charge.py --report /tmp/dimension-7-four-five-six-charge.json
```
