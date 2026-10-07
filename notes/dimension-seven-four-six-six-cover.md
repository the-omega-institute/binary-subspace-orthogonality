# The transferred two-hole branch has no five-heptad cover

**Theorem.** No nineteen-color line coloring has the size-four
profile `(4,5,5;7,0,8)`. The two-hole `(4,6,6;5,2,8)` subbranch
reached by its forced two-completion transfer is excluded by a
new independently checked finite covering certificate. The
entire raw `(4,6,6;5,2,8)` profile is not excluded here.

## Written reduction to the finite problem

The [forced two-completion transfer](dimension-seven-four-five-five-charge.md)
shows that every coloring with `(4,5,5;7,0,8)` transfers its two
unique completions from distinct pure even heptads. This uses
the earlier exact exclusions `(3,5;7,1,8)`, `(4,4;7,1,8)` and
`(5,4;6,2,8)`, with their stated historical finite premises.
Its target has two pure sextets with outside-M sums, distinct
actual holes, and each completion in its paired mixed class.

The [written normalization](dimension-seven-four-six-six-two-hole.md)
gives three exhaustive marked forms b=3,15,63 and full groups
of orders 8,16,16. The [complete joint roots](dimension-seven-four-six-six-roots.md)
retain all five even components, their paired roles and actual
holes. Their 1,708,1,648,304 distinct remaining sets give
224,112,21 complete group orbits. Every target coloring therefore
has a necessary 35-point remainder in one of these 357 orbits.

Each remainder contains five holes. Its five residual pure even
heptads must each meet one hole: a heptad meets the totally
isotropic M at most once. Consequently the complete covering
catalog consists of the 224 anchored even heptads. Symplectic
isometries preserve the catalog and transport covers, so failure
for every representative excludes every root. This step uses
the proved group action, including actual-hole transport, without
assuming that the action is free.

## A checked failed-state certificate

The bounded builder searches only these representatives and this
catalog. For a nonempty remaining set R it selects a pivot p in R
and tries every anchored heptad H contained in R and containing p.
If all children R minus H fail, it records R and p. A successful
cover would reach the empty set, which is never recorded as failed.

The independent auditor reconstructs the complete five-component
roots and orbit partition using the independent array method,
then independently enumerates all 288 even heptads and selects
the 224 anchored ones. It checks the exact representative list,
every pivot and every admissible successor. All successors must
be certified failures with seven fewer points. All stored states
must be reachable from the required representatives. These
strict size decreases give a finite induction: a leaf has no
heptad covering its pivot, and every other state has all possible
first-step covers excluded by its children. Hence none of the
357 representatives has a five-heptad cover. The certificate
has 359 reachable failed states: 357 of size 35 and two of size
28. It has two checked branches and 357 leaves without an
admissible anchored heptad covering the chosen pivot.

| b | Complete roots | Checked representatives | Cover conclusion |
| --- | --- | --- | --- |
| 3 | 1,708 | 224 | All excluded |
| 15 | 1,648 | 112 | All excluded |
| 63 | 304 | 21 | All excluded |

The [certificate](../results/dimension-7-four-six-six-cover-proof.json)
and [audit report](../results/dimension-7-four-six-six-cover-check.json)
bind the complete root artifact and all proof inputs.
Invalid controls remove a representative, choose a pivot absent
from its state, falsely mark the empty set as failed or omit a
required successor; each is rejected.

The new covering proof for the transferred subbranch does not
invoke earlier covering certificates as failed-state premises.
The conclusion about the original `(4,5,5)` row does retain the
three prior exact exclusions in its written transfer. Their
historical source, certificate and dependency identities remain
checked, including the four-even-pair theorem's inherited
size-three two-six premise. Those old covering audits and the
earlier normalization/recoloring audits are not rerun here.

## Exact scope

The count audit reconstructs the original 46 five-plus-six and
48 three-six raw rows. It removes exactly `(4,5,5;7,0,8)` from
the preceding 37-row three-six list and preserves the 25-row
five-plus-six list. The current totals are **25/36**, with two
three-six C8 rows: `(4,5,6;6,1,8)` and `(4,6,6;5,2,8)`.
There are 61 candidates, 59 with six through eight pure odd
heptads and two with five. These are necessary count profiles,
not realized colorings. The other `(4,6,6)` branches remain open.

Characteristic sizes four through eight and exact n=7 remain
open with lower bound 19. No new Lean or independent Pro review
is claimed; the original n=6 theorem retains three standard plus
four native-evaluation axioms. The submitted snapshot is preserved.
The authorized extended draft integrates this partial exclusion.

The next bounded academic question is the remaining
`(4,5,6;6,1,8)` row: derive the unique five-even completion,
its possible source class and the pure-six charge/hole relations
before proposing another transfer or finite catalog. No different
profile exclusion can be imported without an exact written reduction.

```sh
python3 develop/build_dimension_seven_four_six_six_cover.py --certificate /tmp/n7-four-six-six-cover-proof.json --max-states 20000 --max-visits 80000 --seconds 20
python3 develop/check_dimension_seven_four_six_six_cover.py --certificate /tmp/n7-four-six-six-cover-proof.json --report /tmp/n7-four-six-six-cover-check.json
```
