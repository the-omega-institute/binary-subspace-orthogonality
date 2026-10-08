# Complete seven-component roots for the pure-source row

The sixteen ordered pure-source normal forms now have complete
necessary jointly disjoint seven-component families, retaining
every component decomposition and all four actual positive holes.

**Finite theorem.** The complete necessary family has **42,496 ordered
joint configurations**, **10,032 form-labelled even remainders** and
**1,276 full ordered marked-group remainder orbits**. Each remainder
has 21 points, exactly the three nonzero kernel holes, and zero even
sum. It requires three pure heptads from the complete 96-row
kernel-anchored catalog. This specifies a complete necessary covering
problem; the raw row remains open and the candidate lists stay 25/35.

## Why every hypothetical coloring supplies a root

The [source theorem](dimension-seven-four-six-six-pure-sources.md)
forces both completions into distinct pure heptads, each avoiding the
other completion. The [normalization](dimension-seven-pure-source-normalization.md)
provides sixteen exhaustive ordered forms, all four functional
patterns and four b positions, with full eight-element ordered groups.
Every group fixes M pointwise and preserves each actual-hole allocation.

For each form, construct the complete original-dot-product catalogs
for D0,J1,J2,P1,P2,H1,H2. Their even sizes are 4,6,6,6,6,7,7.
D0 has sum a and pairs to one with its odd projections a,b;
the mixed even sextets have sums c,d. These three blocks avoid u,v.
Each pure sextet has one actual M-hole, sum equal to its associated
completion and avoids the other completion. Each source heptad
contains its associated completion and avoids the other completion.
The even catalogs plus their specified odd members are checked as
independent sets in the original graph.

Choose one block in each catalog, requiring all seven to be mutually
disjoint. Exhaustive recursion tests every choice in a finite catalog;
a rejection occurs precisely when a chosen block meets an earlier
block. Thus no jointly disjoint tuple is pruned. Retain its four actual
holes in the order P1,P2,H1,H2. They exhaust the four positive points.
Its 42-point even union has complement of size 21, with exactly the
three kernel holes and sum a+c+d+u+v=0. Every hypothetical coloring,
after normalization, occurs among these complete necessary tuples.

The eight pure odd heptads have not been enumerated here. The family
retains the written necessary charge/projection constraints and may
contain configurations that fail additional coloring conditions.
Completeness means it includes every hypothetical coloring's even
tuple; it does not assert that each tuple extends to a coloring.

## All sixteen branches and every decomposition

The counts are form-labelled; identical coordinate remainders in
different forms remain separately represented.

| Pattern | b | Joint configurations | Distinct remainders | Remainder orbits |
| --- | --- | --- | --- | --- |
| 100 | 15 | 1536 | 336 | 44 |
| 100 | 51 | 1536 | 336 | 44 |
| 100 | 60 | 5888 | 1376 | 184 |
| 100 | 63 | 896 | 160 | 20 |
| 010 | 15 | 3456 | 768 | 96 |
| 010 | 51 | 2816 | 672 | 84 |
| 010 | 60 | 2752 | 664 | 86 |
| 010 | 63 | 960 | 224 | 28 |
| 001 | 15 | 2816 | 672 | 84 |
| 001 | 51 | 3456 | 768 | 96 |
| 001 | 60 | 2752 | 664 | 86 |
| 001 | 63 | 960 | 224 | 28 |
| 111 | 15 | 4352 | 1088 | 136 |
| 111 | 51 | 4352 | 1088 | 136 |
| 111 | 60 | 3200 | 800 | 100 |
| 111 | 63 | 768 | 192 | 24 |
| Total | | **42496** | **10032** | **1276** |

Every form retains all 24 possible ordered positive-hole allocations,
including any empty joint fiber. For pattern100 and b=15 or51, eight
allocations have no compatible seven-component tuple and sixteen are
nonempty. All 24 are nonempty in the other fourteen forms. The local
48-quartet count from normalization is not a joint-family count.

Every remainder has **four or eight ordered decompositions** into the
seven original roles. The artifact stores them all, including their
actual holes. The auditor reconstructs each decomposition independently
and transports it under every full marked-group map. Each transported
tuple has exactly the mapped remainder and retains its actual holes.

The joint tuple action is free and gives 5,312 tuple orbits. The
remainder action is not always free: its orbits have sizes four or
eight, with remainder stabilizers of order two or one. The size-four
orbit counts are 4,4,24 for pattern100 and b=15,51,60, and six each
for patterns010,001 with b=60. All other remainder orbits have size
eight. These actions and stabilizers are checked directly; neither
local-quartet freeness nor a unique-decomposition assumption is used
to divide remainder counts.

## Independent audit and evidence scope

The [builder](../develop/build_dimension_seven_pure_source_roots.py)
uses bitmask clique catalogs, disjointness and a catalog-size traversal
order. The [auditor](../develop/check_dimension_seven_pure_source_roots.py)
independently enumerates array cliques and uses set unions with a
different traversal order. It reconstructs the complete catalogs,
tuples, all decompositions, remainders and orbit partitions, then
compares the entire artifact exactly.

The auditor reconstructs each full ordered group from all symplectic
dual-basis images rather than the builder's symmetric shears. It
checks full original-dot-product preservation, group closure,
recipient completions, all original graph component conditions,
42,496 family partitions and 339,968 family actions with roles and
actual holes. Four invalid controls reject a missing form, a missing
decomposition, an incorrect actual hole and a missing orbit member.
The preceding normalization report and ten inherited finite theorem
report/source/certificate/dependency bindings are checked without
rerunning their audits.

The [roots artifact](../results/dimension-7-pure-source-roots.json)
and [independent report](../results/dimension-7-pure-source-roots-check.json)
give the complete necessary inputs for the next bounded problem:
three-heptad covers of all 1,276 representative 21-point remainders,
using the complete 96 kernel-anchored heptads filtered by containment.
Cover existence is invariant under each proved marked group, which
preserves the kernel-hole catalog; checking representatives will
therefore suffice once a complete covering proof is supplied.

No cover search or covering certificate is run here, and no raw row
is excluded. All sixteen branches and exact n=7 remain open, with
lower bound 19. The current lists stay 25/35, including one three-six
C8 row. No new Lean or independent Pro review is claimed. The original
n=6 theorem retains three standard plus four native-evaluation axioms;
the submitted snapshot and historical evidence are preserved.

```sh
python3 develop/build_dimension_seven_pure_source_roots.py --roots /tmp/n7-pure-source-roots.json --max-visits 1000000 --seconds 20
python3 develop/check_dimension_seven_pure_source_roots.py --roots /tmp/n7-pure-source-roots.json --report /tmp/n7-pure-source-roots-check.json
```
