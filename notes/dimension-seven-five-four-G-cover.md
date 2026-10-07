# The mixed characteristic-charge normal form G has no cover

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic class
size four and profile (m5,m6;A,B,C)=(5,4;6,2,8) cannot have
normal form G. Equivalently, when the pure-five even sum is nonzero,
the characteristic charge cannot be a mixed class's odd projection.

The theorem uses the written marked normalization and pointwise-hole
stabilizer reduction, together with a new independently audited finite
covering proof. G is excluded, alongside the separate existing D and H
exclusions. Z remains open; the raw profile remains unexcluded, and
the overall remaining count candidates stay 27 five-plus-six and
39 three-six. Exact dimension-seven chromatic numbers remain open
with lower bound 19.

## Written reduction to the checked representatives

The [four-form charge argument](dimension-seven-five-four-charge.md)
normalizes G in E=z-perp, z=127, with

~~~text
M={0,3,12,15,48,51,60,63}, p=12, q=3,
D6 odd projections={3,48}, mixed projections={51,60},
characteristic projections={12,15,63}, h=60.
~~~

The pure-five block contains exactly one actual hole t, different
from p=12. D6 and both mixed-even sextets avoid M. Their four
even blocks have 21 distinct points, so six pure even heptads must
partition the remaining 42 points, one through each remaining hole.
The [complete root and stabilizer argument](dimension-seven-five-four-G-roots.md)
retains both mixed classes and every possible t. Its two independent
constructions give 129,280 ordered roots and 127,984 distinct sets.

For symmetric binary matrices S, the written symplectic maps
(x,y)->(x+Sy,y) fix M pointwise. Their extension fixing z preserves
the original dot form, all named odd projections and actual t.
They preserve both the root family and the complete anchored-heptad
catalog. Cover existence is constant on an orbit. Thus excluding
the 2,306 recorded representatives excludes every necessary root.
No assumption of transitivity on t or of free group action is used.

## Finite proof by decreasing failed states

The [bounded builder](../develop/build_dimension_seven_five_four_G_cover.py)
generates the anchored heptads with array clique recursion and searches
only the 2,306 representatives. Its explicit limits are 25,000
failed states, 100,000 visits and 30 seconds. An exhausted budget
raises an error and writes no exclusion certificate. A found even
cover is recorded separately as a necessary cover requiring extension
checking, never as a failed-state exclusion.

The [independent auditor](../develop/check_dimension_seven_five_four_G_cover.py)
reconstructs the entire root family and full orbit partition with
the preceding two-algorithm checker, matching the archived report.
It constructs all 288 even heptads by bitmask recursion and retains
all 224 rows meeting M once, checking their original dot products.
It does not import the covering builder or rely on its search result.

Every recorded failed state has a present uncovered pivot. The
auditor checks every anchored heptad contained in the state through
that pivot; each such choice must lead to a recorded failed state
with exactly seven fewer points. Leaves have no admissible row,
and the empty set is never marked failed. Every required representative
is failed, and all recorded states are reachable from these roots.
Induction on the number of points therefore proves that no root
has a six-heptad cover. Missing-root, absent-pivot and falsely
failed-empty-set controls are rejected.

The [certificate](../results/dimension-7-five-four-G-cover-proof.json)
and [audited report](../results/dimension-7-five-four-G-cover-check.json)
bind the necessary-root report, all representatives, the reachable
failed-state graph, the builder, checker and this note by SHA-256.
There are 3,351 reachable failed states, 1,045 checked branches
and 2,401 leaves. The state-size counts are 2,306 at 42 points,
984 at 35, 59 at 28 and two at 21. The finite proof includes all
2,306 representatives and terminates at leaves with no admissible row.
This G proof uses neither the D/H covering certificates nor earlier
seven-heptad certificates as proof inputs.

## Remaining question and evidence scope

The earlier [D](dimension-seven-five-four-D-cover.md) and
[H](dimension-seven-five-four-H-cover.md) theorems, combined with
this G exclusion and the exhaustive four-form reduction, leave
only Z for this specified raw profile. In Z the pure-five even sum
is zero; its five members span a nondegenerate four-space. The
characteristic charge remains nonzero, so the zero-sum class must
not be conflated with the excluded zero-characteristic-charge form H.

The current theorem is a written geometric reduction plus a finite
covering proof. No new Lean or independent Pro review is claimed.
The original six-dimensional formal theorem retains three standard
and four native-evaluation axioms. The submitted manuscript and
Zenodo record are unchanged. The extended working draft records
the three excluded marked forms and the remaining Z case. This
result does not change publication or submission decisions.

~~~sh
python3 develop/build_dimension_seven_five_four_G_cover.py --certificate /tmp/dimension-7-five-four-G-cover-proof.json
python3 develop/check_dimension_seven_five_four_G_cover.py --certificate /tmp/dimension-7-five-four-G-cover-proof.json --report /tmp/dimension-7-five-four-G-cover-check.json
~~~
