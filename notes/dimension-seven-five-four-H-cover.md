# The zero characteristic-charge pure-five/four-even normal form has no cover

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic
class size four and profile (k5,k6;A,B,C)=(5,4;6,2,8) cannot have
normal form H from the [four-form charge reduction](dimension-seven-five-four-charge.md).
Thus this profile cannot have zero characteristic charge.

The written marked reduction and a new independently audited finite
covering certificate exclude H. The [earlier D exclusion](dimension-seven-five-four-D-cover.md)
is separate; Z and G remain open. The raw profile remains unexcluded,
and the totals stay nineteen of forty-six 5+6 and nine of forty-eight
6+6+6 profiles excluded, leaving twenty-seven and thirty-nine
unexcluded. Exact dimension-seven chromatic numbers remain open
with lower bound nineteen.

## The actual pure-five hole and both mixed classes

The existing written eight-spread and charge-member arguments give
q=a, p=a+b+c and h=p+d. In H, h=0 gives p=d. The distinct
points a,d,b are independent: dependence would force b=a+d,
then c=0. Send the ordered basis (a,d,b) of the hole Lagrangian M
to (3,12,48), extend to a symplectic basis of E=z-perp, and fix z.
This proves the universal H normalization in the original dot space:

```text
z=127,  M={0,3,12,15,48,51,60,63},
five-even sum p=12,       four-even sum q=3,
D6 odd projections={3,12},       mixed projections={48,63},
characteristic projections={15,51,60},       h=0.
```

The pure-five class contains exactly one nonzero M point t, with
t different from p=12. Its even sum pairs to zero with every
member, whereas its member t pairs to one with the other four
members. D6 and the two mixed classes avoid M because each has
an odd projection in M. The remaining six pure even heptads must
each contain exactly one of the six holes M minus {0,t}.

There are 96 pure-five blocks, sixteen D6 four-even blocks and
thirty-two even sextets for each mixed projection. For a mixed
class, its six even members span E and their sum pairs to one
with each member, so their sum is its odd projection. Retaining
all four blocks disjointly gives 127,680 ordered roots and 126,336
distinct remaining 42-point sets. No orbit on the possible t values
is assumed.

| Pure-five hole t | Disjoint defect pairs | Ordered four-block roots |
| --- | --- | --- |
| 3 | 256 | 23,872 |
| 15 | 256 | 23,808 |
| 48 | 256 | 20,544 |
| 51 | 256 | 19,456 |
| 60 | 256 | 19,456 |
| 63 | 256 | 20,544 |

Every remaining set contains exactly the six holes other than t
and requires six even heptads. Among the 288 even heptads, 224
meet M once. The whole 224-row catalog is valid for each root:
rows containing the removed t cannot be contained in that root
or any successor. Exactly 192 catalog rows avoid each particular t.

## A new covering certificate and independent audit

The [builder](../develop/build_dimension_seven_five_four_H_cover.py)
uses array clique recursion and a bounded exact-cover search on
these roots only. Its limits are 250,000 failed states, 1,000,000
visits and 30 seconds. It writes an exclusion certificate only
when every root fails; budget exhaustion or a found cover writes
no certificate. The initial 150,000-state diagnostic exhausted
its state limit and supplied no exclusion. The revised state cap
allows the 126,336 distinct roots and their smaller successors
to be checked within the same visit and time limits.

The [independent auditor](../develop/check_dimension_seven_five_four_H_cover.py)
uses bitmask clique recursion to reconstruct every catalog and
disjoint four-block root, including its actual t. It checks each
partial class against the original dot product. Every recorded
failed state has an uncovered pivot. All contained anchored
heptads through that pivot must lead to recorded failed states
with seven fewer points. Leaves have no admissible row; the empty
set is never marked failed. All states must be reachable from a
required root, and the hole count equals the point count divided
by seven at every state. Induction from leaves proves every root
impossible.

The [new certificate](../results/dimension-7-five-four-H-cover-proof.json)
and [report](../results/dimension-7-five-four-H-cover-check.json)
record 186,584 reachable failed states, 60,904 branches and
128,880 leaves. State sizes are 42 points (126,336 states),
35 points (58,552 states) and 28 points (1,696 states).
Fixed-M controls check all 84 H marked
role assignments, 4,116 Gram entries and 14,784 inverse-mapped
partial classes. These controls support the written universal
normalization without enumerating complete colorings or spreads.

The H exclusion depends on the written marked reduction and its
own new six-heptad certificate. Neither the D certificate nor
the earlier seven-heptad certificates are proof inputs. No SAT,
DRAT, Lean or new independent Pro review is claimed. The submitted
manuscript and Zenodo PDF are unchanged; the original six-dimensional
formal theorem retains three standard and four native-evaluation axioms.

```sh
python3 develop/build_dimension_seven_five_four_H_cover.py --certificate /tmp/dimension-7-five-four-H-cover-proof.json
python3 develop/check_dimension_seven_five_four_H_cover.py --certificate /tmp/dimension-7-five-four-H-cover-proof.json --report /tmp/dimension-7-five-four-H-cover-check.json
```
