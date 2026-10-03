# Third candidate: inventory repair and a zero-lift obstruction

Reza's third candidate at `eed4b180f583d3510b9260e581f7b10adb3de094` is
committed as `develop/color_function_candidate_v3`, without a .py extension.
It encodes all canonical basis lift values in base64 and uses the resulting
integer modulo the number of available label entries. This is a numeric
index into the existing ordered list, rather than a lexicographic sorting
of the labels.

## Literal output and the inventory

The unmodified script reports 2809 vertices, thirteen distinct labels,
zero availability violations and 3507 same-label orthogonality violations.
The independent checker tests all 411508 same-label pairs directly using
the original coordinate dot product and reproduces this result.

The list still has the two duplicate planes identified in v2:

    span(3,15) = span(3,12),
    span(12,60) = span(12,48).

Thus its fifteen entries are thirteen distinct subspaces. A complete
inventory can be obtained by replacing those entries, in their current
positions, with span(3,60) and span(15,51). This particular repair preserves
the other entries and the line order. The checker independently enumerates
all subspaces of T and verifies the repaired inventory is exactly that set.

For this precisely specified repaired ordering, the same numeric-index
rule reaches all fifteen labels and has 2967 violations on 351950 same-label
pairs, with zero availability violations. This diagnostic uses a separate
inventory in the checker and leaves Reza's source unchanged. The counts
apply to this ordering; they are not a result about every possible ordering.

| Rule | Distinct labels | Same-label pairs checked | Monochromatic edges |
| --- | ---: | ---: | ---: |
| Literal v3 | 13 | 411508 | 3507 |
| V3 with the specified inventory repair | 15 | 351950 | 2967 |

## A counterexample surviving the inventory repair

Take U=span(5), W=span(21), where 5=e1+e3 and 21=e1+e3+e5. These are
distinct vertices in the complement S=span(1,4,16), with

    K=L=0, P=span(5), Q=span(21), f=g=0.

They are orthogonal because dot(5,21)=1+1=0 over F2. All their lift values
are zero, so both numeric keys are zero. The first available label is
span(3) for both, since dot(3,5)=dot(3,21)=1. This remains the first label
under the specified inventory repair. Both rules give a monochromatic edge.
The cross-kernel matrices are empty and Z=[dot(5,21)]=[0].

This written example explains why increasing the amount of lift information
alone is insufficient for this rule: the example has zero lift maps, and
the choice within the palette collapses to the first entry. The geometry
of P and Q must affect the label selection beyond availability, so that
these two vertices receive different labels. The example rejects the
displayed rule and repair, not every construction from full (K,P,f).

## Cheap checks for a future proposal

The fourteen-clique from T'=span(5,18,40), proved in the preceding note,
gives a small regression fixture. A proper rule must assign fourteen
distinct labels to its fourteen vertices outside T. The literal v3 assigns
eight distinct labels there, creating eight monochromatic edges; the
specified repair assigns seven labels, creating nine monochromatic edges.
Using fifteen labels somewhere in the full graph does not imply separation
on this clique.

Before replaying all 2809 vertices, a future candidate can check the inventory
has fifteen distinct subspaces, this fourteen-clique has no repeated labels,
and span(5),span(21) receive different labels. These are necessary screens;
passing them would not prove the complete coloring. Full availability and
same-label separation still need verification and a readable proof.

## Evidence and scope

```sh
python3 develop/color_function_candidate_v3
python3 develop/check_color_candidate_v3.py
```

The [independent checker](../develop/check_color_candidate_v3.py) verifies
all author lift tuples against coordinate projection and quotient cosets,
all author labels against the numeric-index rule, and direct coordinate
adjacency in both specified variants. The
[JSON report](../results/color-candidate-v3-check.json) records the ordered
repair, per-label counts, counterexample, fixture counts and source hashes.
The author's zero omission in 1016 projections changes no chosen labels.

The author source, manuscript TeX, ten-page PDF and existing certificates
are unchanged. Exact chi(O_6*)=15 and chi(Gamma_6)=12 remain established.
Structural coloring and n=7 remain open. No solver or Lean run is involved;
the historical full-subspace six-dimensional Lean theorem retains three
standard plus four native-evaluation axioms. The previous fourteen-clique
proves only an induced-graph lower bound, not its exact chromatic number.
