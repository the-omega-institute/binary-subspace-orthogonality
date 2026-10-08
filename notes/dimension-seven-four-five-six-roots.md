# Complete joint roots for all twelve completion-source branches

**Theorem.** Every hypothetical nineteen-color line coloring with
characteristic size four and profile `(4,5,6;6,1,8)` determines a
necessary remaining set in one of twelve completely constructed
ordered marked families. All component decompositions, full marked
group orbits and actual holes are retained. The necessary remainder
requires four anchored even heptads in a pure t-source branch or
five in a mixed t-source branch. No covering test is run here, and
the row remains open with count lists **25/36**.

## Written completeness reduction

The [source theorem](dimension-seven-four-five-six-charge.md)
forces q into a pure heptad Hq avoiding t, and t into a different
pure heptad Ht or, for eta=1, the existing mixed heptad J.
The [ordered normalization theorem](dimension-seven-four-five-six-symmetry.md)
gives eight exhaustive forms with full marked groups of order eight,
fixing M pointwise. There are eight pure-source and four mixed-source
branches. The reversible mixed-role recoloring is not used as an
exchange symmetry of the original roles.

For a pure source, take the ordered even components
D0,D1,P,J,Hq,Ht. For a mixed source, take D0,D1,P,J,Hq.
The complete local catalogs are exactly those specified by the
source and normalization theorems: D0 has sum a and pairs to one
with a,b while avoiding t,q; D1 has sum t+c, pairs to one with c
and avoids q; P has sum q, contains one actual M-hole and avoids t;
J has sum d, avoids q and contains t precisely for a mixed source;
Hq is an anchored heptad containing q and avoiding t; Ht, when
present, is anchored, contains t and avoids q.

A coloring selects one block from each catalog. Its original
partition makes the selected blocks mutually disjoint, so it is
included when **all** such jointly disjoint tuples are constructed.
No orbit selection, preferred hole allocation or inferred unique
decomposition is made during this construction. Conversely these
tuples are necessary partial partitions; a tuple need not extend
to all odd classes or to a complete coloring.

The fixed even component sizes are 4,5,6,6,7,7 for a pure source
and 4,5,6,6,7 for a mixed source. Their complement in the 63 nonzero
even points therefore has 28 or 35 points. The components use three
or two distinct actual holes, leaving four or five M-holes. Their
even sums add to a+(t+c)+q+d=0, so the remainder also has sum zero.
The remaining pure even heptads must each meet a remaining hole,
because a heptad meets M at most once. Thus the complete eligible
catalog for the necessary cover consists of all 224 anchored even
heptads, filtered by containment in the particular remainder.

## All decompositions and legal group orbits

Different joint tuples can have the same remaining point set.
The artifact groups them by remainder and retains **every ordered
component decomposition and its actual holes**. The group acts
on the whole tuple, preserving D0/D1/P/J/Hq/Ht roles and mapping
each actual hole to itself. Every tuple image must occur among
the retained decompositions of the image remainder.

The independent auditor reconstructs the full group using all
symplectic dual-basis choices to the fixed M basis; it does not
use the builder's symmetric-matrix formula. The group transports
anchored heptads and covers, so one representative of each complete
remaining-set orbit suffices for a later necessary cover test.
Forgetting the component decomposition for that test is justified
by the complete tuple construction and the checked equivariance,
not by an assumed unique decomposition or free group action.

## Independent finite audit

The complete counts are form-labelled: remainders in different forms
are not asserted to be globally distinct.

| eta | b | t-source | Joint families | Distinct remainders | Full-group orbits |
|---|---:|---|---:|---:|---:|
| 0 | 15 | pure | 6,560 | 3,020 | 381 |
| 0 | 51 | pure | 6,208 | 3,072 | 384 |
| 0 | 60 | pure | 7,136 | 3,528 | 441 |
| 0 | 63 | pure | 2,784 | 1,360 | 170 |
| 1 | 15 | pure | 5,392 | 2,680 | 354 |
| 1 | 15 | mixed | 3,192 | 1,596 | 210 |
| 1 | 51 | pure | 7,200 | 3,568 | 468 |
| 1 | 51 | mixed | 3,192 | 1,596 | 210 |
| 1 | 60 | pure | 5,568 | 2,752 | 344 |
| 1 | 60 | mixed | 2,816 | 1,408 | 194 |
| 1 | 63 | pure | 992 | 496 | 62 |
| 1 | 63 | mixed | 576 | 288 | 40 |
| **Total** | | | **51,616** | **25,364** | **3,258** |

The pure-source totals are 41,840 families, 20,476 remainders and
2,604 orbits; mixed-source totals are 9,776, 4,888 and 654.
Every remainder has two, four or eight ordered decompositions.
Every mixed-source remainder has two. Remainder orbits have size
four or eight, so neither unique decomposition nor a free action
can be assumed. All decompositions and all orbit members are saved.

The [bounded bitmask builder](../develop/build_dimension_seven_four_five_six_roots.py)
uses size-ordered clique catalogs and disjointness masks. The
[independent array auditor](../develop/check_dimension_seven_four_five_six_roots.py)
reconstructs all size-4/5/6/7 even cliques, then visits the component
choices in a different order using set unions and cardinalities.
It checks every component in the original binary dot-product graph,
recipient completions, every full tuple's partition, zero remainder
sum and actual holes. It matches all catalogs, decompositions,
remaining sets, basis maps and complete orbit partitions exactly.
All tuple images retain their roles and actual holes, and both
tuple and remainder orbit--stabilizer identities are checked.
Missing branches, dropped decompositions, incorrect actual holes
and omitted orbit members must all be rejected.

The [complete root artifact](../results/dimension-7-four-five-six-roots.json)
and [audit report](../results/dimension-7-four-five-six-roots-check.json)
bind the construction, audit and written argument. The previous
source/normalization reports and nine inherited covering reports
retain their exact source, certificate and dependency identities;
those old audits are not rerun. No new covering search, failed-state
certificate, Lean or independent Pro review is run. Exact n7 remains
open with lower bound 19, and the original n6 theorem retains three
standard and four native-evaluation axioms. The submitted snapshot
and historical records are preserved.

The next bounded problem is to test all complete remaining-set
orbit representatives against their justified four- or five-heptad
cover problem, recording every admissible successor in an independently
auditable finite proof if all covers fail. A timeout or root that
admits a cover would not exclude the row; a cover of a necessary
remainder would still not be a full nineteen-color witness.

```sh
python3 develop/build_dimension_seven_four_five_six_roots.py --roots /tmp/dimension-7-four-five-six-roots.json
python3 develop/check_dimension_seven_four_five_six_roots.py --roots /tmp/dimension-7-four-five-six-roots.json --report /tmp/dimension-7-four-five-six-roots-check.json
```
