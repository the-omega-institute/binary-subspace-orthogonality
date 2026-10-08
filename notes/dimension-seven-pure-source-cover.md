# The entire four-six-six raw row is excluded

**Theorem.** No nineteen-color line coloring with characteristic
size four has profile `(4,6,6;5,2,8)`. The current count lists
become **25/34**. Exact n=7 remains open with lower bound 19.

## Exhaustive reduction and obstruction

The [source theorem](dimension-seven-four-six-six-pure-sources.md)
applies to the entire raw row, including all four functional patterns
100,010,001,111. It forces the two pure-six completions into distinct
pure even source heptads, each avoiding the other completion. Its
transfers use ten inherited finite theorem bindings, including the
complete four-five-six exclusion. The two pure sextets and their two
sources occupy the four actual positive holes; the residual holes
are exactly the three nonzero points of the functional kernel.

The [ordered normalization](dimension-seven-pure-source-normalization.md)
gives sixteen exhaustive forms, with four b positions for each pattern.
The [complete root construction](dimension-seven-pure-source-roots.md)
retains every jointly disjoint choice of D0,J1,J2,P1,P2,H1,H2, all
ordered decompositions and actual-hole allocations. Its 42,496 ordered
configurations give 10,032 form-labelled 21-point remainders and 1,276
full ordered marked-group remainder orbits. Every hypothetical coloring
therefore supplies one root and a partition of its remainder into three
pure even heptads.

Each residual heptad contains exactly one remaining kernel hole.
There are 288 even heptads, of which 224 meet M in exactly one nonzero
point. For each normalized kernel, 96 of these rows meet a kernel hole.
Filtering the 224-row catalog by containment in a remainder is equivalent
to filtering those 96 rows: the remainder has no positive hole. The full
proved marked group fixes M pointwise and preserves the original dot
product, so it transports remainders and eligible heptads. Cover existence
is constant on every recorded remainder orbit, including size-four
orbits with nontrivial stabilizers.

For each of the 1,276 representative remainders R, the
[certificate](../results/dimension-7-pure-source-cover-proof.json)
records a point p in R. Exhaustive independent catalog containment
shows that **no eligible heptad H contained in R contains p**. In any
partition of R into eligible heptads, p would belong to one such H,
a contradiction. Thus every representative is uncoverable. Group
transport excludes all 10,032 remainders and all 42,496 necessary
configurations. The exhaustive source and normalization reductions
then exclude the entire raw row.

## Independent finite audit

The [bounded builder](../develop/build_dimension_seven_pure_source_cover.py)
uses bitmask clique catalogs and selects a pivot with the fewest contained
heptads. Its limits are 15,000 failed states, 60,000 visits and 20 seconds.
It completes in 1,276 visits. Every pivot already has zero options; no
recursive successor is needed. A resource-limit exception gives no
exclusion certificate.

The [array/set auditor](../develop/check_dimension_seven_pure_source_cover.py)
first independently reconstructs the complete root families, decompositions,
actual holes, full marked groups and orbit partitions, and matches the
historical roots report exactly. It independently enumerates all 288 even
heptads, selects the 224 anchored rows and checks the 96-row equivalence
for all four normalized kernels. It checks every state and pivot, every
admissible successor and exact reachability from the representative list.
The [report](../results/dimension-7-pure-source-cover-check.json) has
**1,276 reachable failed states, zero required successors and 1,276
leaves**, all of size 21. This is a finite covering proof, with the
zero-option pivot argument supplying its written inference.

Four invalid controls are rejected: a missing representative, an absent
pivot, a false empty failure and a false leaf on a coverable state.
For the last control the auditor constructs the 14-point union of two
disjoint anchored heptads and falsely records failure without its valid
successor. This tests successor completeness even though the actual proof
has no successors.

The ten inherited theorem report/source/certificate/dependency bindings
remain checked. Source and normalization audits and historical covering
audits are not rerun; no historical certificate is used as a failed-state
premise of this new proof. Root reconstruction is rerun. No new Lean or
independent Pro review is claimed. The original n=6 theorem retains three
standard plus four native-evaluation axioms.

## Exact count consequences

Independent reconstruction recovers the original 46 five-plus-six and 48
three-six raw count rows. From the previous 25/35 lists it removes exactly
`[4,6,6,5,2,8]`, leaving **25/34**, or **59** size-four count candidates.
Of these, 57 have C=6 or 7 and two have C=5; **no C=8 count candidate
remains in either list**. There are now 21 excluded five-plus-six rows
and 14 excluded three-six rows. The remaining candidates are necessary
profiles, not realized colorings. Characteristic sizes four through eight
and exact n=7 remain open, with lower bound 19.

```sh
python3 develop/build_dimension_seven_pure_source_cover.py --certificate /tmp/n7-pure-source-cover-proof.json --max-states 15000 --max-visits 60000 --seconds 20
python3 develop/check_dimension_seven_pure_source_cover.py --certificate /tmp/n7-pure-source-cover-proof.json --report /tmp/n7-pure-source-cover-check.json
```
