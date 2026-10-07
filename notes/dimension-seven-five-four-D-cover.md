# The nonzero six-defect characteristic-charge normal form has no cover

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic
class size four and profile (k5,k6;A,B,C)=(5,4;6,2,8) cannot have
the D normal form from the
[four-form charge reduction](dimension-seven-five-four-charge.md):
its nonzero characteristic charge cannot be an odd projection of
the six-point defect when the five-even sum is nonzero.

The written marked reduction and a new independently audited
finite covering certificate exclude this one normal form. The
three other forms Z,H,G remain open. The raw (5,4;6,2,8) profile
therefore remains unexcluded, and the totals stay nineteen of
forty-six 5+6 and nine of forty-eight 6+6+6 profiles excluded,
leaving twenty-seven and thirty-nine unexcluded. Exact dimension-seven
chromatic numbers remain open with lower bound nineteen.

## Retaining both mixed classes and the actual pure-five hole

Use z=127 and M={0,3,12,15,48,51,60,63}. In D the prior written
basis construction gives

```text
five-even sum p=63,       four-even sum q=48,
D6 odd projections={48,15},       mixed projections={3,12},
characteristic projections={51,60,63},       h=48.
```

The pure-five defect has exactly one even point t in M minus {0}.
The remaining six pure even heptads each meet M once and avoid t.
The D6 and both mixed classes contain no even M point because
each has an odd projection in M. Since p is the radical of the
five-even span, t cannot equal p=63.

There are 96 pure-five blocks with sum 63, sixteen D6 four-even
blocks with sum 48 pairing to one with both 48 and 15, and
thirty-two even sextets for each mixed projection. Each mixed
sextet has sum equal to its odd projection: its six-even Gram
matrix is nonsingular and its members span E, while both the sum
and that odd projection pair to one with every member.

All four blocks must be pairwise disjoint in one coloring. The
784 disjoint defect pairs from the preceding report are only
the first step. Choosing both mixed sextets disjoint from both
defects and each other gives 62,976 ordered roots, leaving
54,448 distinct remaining-point sets. Different partial partitions
can give the same remaining set, so both counts are retained.

| Pure-five hole t | Disjoint defect pairs | Ordered four-block roots |
| --- | --- | --- |
| 3 | 128 | 8,960 |
| 12 | 128 | 8,960 |
| 15 | 144 | 14,080 |
| 48 | 128 | 13,056 |
| 51 | 128 | 8,960 |
| 60 | 128 | 8,960 |

Every root contains 42 remaining even points and exactly the six
holes M minus {0,t}. A necessary completion partitions it into
six even heptads, each containing one hole. There are 288 even
heptads in E and 224 meeting M once. Using that whole 224-row
catalog is valid: rows containing t cannot be contained in the
root or any of its subsets. Thus the covering problem retains
the actual t without assuming an orbit on its six possible values.

## A new bounded search and an independent finite proof

The [builder](../develop/build_dimension_seven_five_four_D_cover.py)
constructs catalogs by array recursion and searches only these
necessary roots. Its limits are 150,000 failed states, 1,000,000
visits and 30 seconds. It writes an exclusion certificate only
after all roots fail; an exhausted budget or found cover writes
no such certificate.

The [independent auditor](../develop/check_dimension_seven_five_four_D_cover.py)
uses bitmask clique recursion to reconstruct the four catalogs,
every disjoint four-block root, both root multiplicities, the
hole table and all possible heptad successors. It checks the
original dot product for every partial class. Each state has a
recorded uncovered pivot; all contained anchored heptads through
that pivot lead to recorded failed states with seven fewer points.
Leaves have no admissible row, and the empty set is never marked
failed. Every state is reachable from a required root. Induction
from the leaves therefore proves all roots impossible.

The [certificate](../results/dimension-7-five-four-D-cover-proof.json)
and [report](../results/dimension-7-five-four-D-cover-check.json)
record 72,576 reachable failed states, 20,072 branches and 52,792
leaves. States have 42,35,28 or 21 points; their hole count equals
their point count divided by seven. This is a new
six-heptad covering proof. The earlier seven-heptad certificates
are not inputs to this exclusion.

The universal written D normalization uses (b,c,a) as a basis of
M, where a=q=h and d=b+c. Fixed-M controls retain all 84 D role
assignments and extend those bases symplectically. The induced
isometries, 4,116 Gram entries and 14,784 inverse-mapped partial
classes are checked against the original dot product. These
controls support the written reduction, without enumerating
complete colorings or partial spreads.

This conclusion has separate written and finite-proof dependencies:
the existing eight-spread completion and charge-member lemma give
the marked D form; the independently audited new certificate
excludes its necessary covers. No SAT, DRAT, Lean or new independent
Pro review is claimed. The submitted manuscript and Zenodo PDF are
unchanged; the original six-dimensional formal theorem retains
three standard and four native-evaluation axioms.

```sh
python3 develop/build_dimension_seven_five_four_D_cover.py --certificate /tmp/dimension-7-five-four-D-cover-proof.json
python3 develop/check_dimension_seven_five_four_D_cover.py --certificate /tmp/dimension-7-five-four-D-cover-proof.json --report /tmp/dimension-7-five-four-D-cover-check.json
```
