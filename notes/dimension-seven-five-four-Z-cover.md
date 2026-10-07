# The zero-sum form Z is excluded, closing the specified five-plus-six profile

**Theorem.** A nineteen-coloring of Gamma_7 with characteristic class
size four cannot have profile (m5,m6;A,B,C)=(5,4;6,2,8).

The new step excludes its zero-five-even-sum normal form Z. The
exhaustive [four-form reduction](dimension-seven-five-four-charge.md)
and the separate existing [D](dimension-seven-five-four-D-cover.md),
[H](dimension-seven-five-four-H-cover.md) and
[G](dimension-seven-five-four-G-cover.md) exclusions then exclude
the entire specified raw profile. The remaining count candidates
decrease from 27 to 26 five-plus-six profiles; all 39 three-six
profiles remain. The exact dimension-seven chromatic numbers
remain open with lower bound 19.

## Written reduction and independent finite proof

Use Z with z=127, M={0,3,12,15,48,51,60,63}, pure-five sum p=0,
D6 sum q=15, D6 odd projections {15,48}, mixed projections {3,12},
characteristic projections {51,60,63} and charge h=48. The zero
pure-five sum is distinct from H's zero characteristic charge.
Every coloring supplies disjoint pure-five, D6-four-even and two
mixed-even sextets. Their complement consists of 42 even points
and the six holes other than the actual pure-five hole t.

The [complete Z roots and written stabilizer](dimension-seven-five-four-Z-roots.md)
give 1,284,736 ordered partial partitions and 1,271,424 distinct
necessary remaining sets. The full 128-element marked symplectic
group includes the 64 pointwise-M shears and the exchange of mixed
classes. It transports the actual hole and preserves cover existence,
reducing every necessary set to one of 10,837 representatives.
No cross-hole transitivity or free group action is assumed.

The [bounded builder](../develop/build_dimension_seven_five_four_Z_cover.py)
searches only these representatives with all 224 even heptads meeting
M once. Its bounds are 75,000 failed states, 300,000 visits and
30 seconds. Exhausting a bound writes no exclusion certificate.
A found even cover would be recorded separately for an original
coloring extension check. Every required representative instead fails.

The [independent auditor](../develop/check_dimension_seven_five_four_Z_cover.py)
reconstructs the complete necessary-root multiset and orbit partition
with the preceding two-algorithm checker, matching its archived report.
It constructs all 288 even heptads by bitmask clique recursion,
checks their original dot products, and retains all 224 anchored rows.
It imports neither the builder nor its search procedure.

Each failed state records a pivot that is still uncovered. The auditor
checks every anchored row through that pivot contained in the state;
each successor must be a recorded failed state with exactly seven
fewer points. Leaves admit no such row, and the empty set is never
declared failed. Every representative is recorded, and every state is
reachable from a representative. Induction on the number of remaining
points proves that every root has no six-heptad cover. Missing-root,
absent-pivot and falsely failed-empty-set controls are rejected.

The [finite certificate](../results/dimension-7-five-four-Z-cover-proof.json)
and [audit report](../results/dimension-7-five-four-Z-cover-check.json)
bind the complete root report, builder, auditor and this note by SHA-256.
The Z covering proof uses none of the D/H/G or previous seven-heptad
covering certificates as proof inputs.

The certificate has 14,337 reachable failed states, 3,517 checked
branches and 10,995 leaves. The state-size counts are 10,837 at
42 points, 3,385 at 35, 98 at 28 and 17 at 21. Every one of the
10,837 required representatives is excluded by this finite proof.

## Closing exactly one raw profile

The four-form argument is exhaustive for the stated profile, so the
new Z exclusion together with the separately proved D/H/G exclusions
closes that profile. The accounting portion reconstructs all 46
five-plus-six and 48 three-six parity-count rows from the two point
balance equations. It matches the archived catalogs and verifies
that (5,4;6,2,8) occurs exactly once among the previous 27 remaining
five-plus-six rows. Removing that row leaves 26; the previous 39
three-six rows are retained exactly. The total exclusions are now
20 of 46 and nine of 48, respectively.

The auditor verifies the hashes and scope metadata of the separate
D/H/G reports for this combined conclusion; it does not rerun their
covering audits. The Z finite proof itself is independent of them.
The report retains the complete updated remaining lists. Of these
65 candidates, 63 have six through eight pure odd heptads and two
have five. Characteristic sizes four through eight still require
other branches; no uniform nineteen-color exclusion is claimed.

This is a written geometric reduction and independently audited finite
proof. No new Lean or independent Pro review is claimed. The original
six-dimensional formal theorem retains three standard and four
native-evaluation axioms. The submitted manuscript and Zenodo record
are preserved; the extended working draft is updated for coauthor review.
Publication, submission, author and disclosure decisions remain joint.

~~~sh
python3 develop/build_dimension_seven_five_four_Z_cover.py --certificate /tmp/dimension-7-five-four-Z-cover-proof.json
python3 develop/check_dimension_seven_five_four_Z_cover.py --certificate /tmp/dimension-7-five-four-Z-cover-proof.json --report /tmp/dimension-7-five-four-Z-cover-check.json
~~~
