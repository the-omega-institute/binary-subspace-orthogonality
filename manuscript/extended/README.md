# Extended working draft — October 8, 2026

[Read the extended PDF](paper.pdf) · [LaTeX source](paper.tex) ·
[Collaboration PR #1](https://github.com/the-omega-institute/binary-subspace-orthogonality/pull/1)

This is a working draft for coauthor review. The manuscript snapshot
`28e27a82068a2f9129fdb5d168bd0fc179cf3e48` submitted to JAC, its PDF,
and the existing Zenodo record are preserved. Preparation of this draft
does not decide publication, submission, revision, or a separate paper.
The author and disclosure blocks retain the existing wording for joint review.

The new Section 6 gives a complete written proof that the dimension-seven
line and full-subspace graphs need at least 19 colors, while the full graph
has clique number 16. It combines independent-class capacity, quadratic
parity, and a universal eight-Lagrangian completion lemma. The exact
dimension-seven chromatic numbers remain open.

Section 7 derives common deficit, parity-count, projected-charge and hole
capacity constraints for nineteen colors, and states the precise scope of
the partial case analysis. Its six/seven-Lagrangian completion premises and
four marked-form covering exclusions close the specified profile
`(5,4;6,2,8)` and retain their separate finite dependencies;
they are not needed for the written lower bound 19. The original
six-dimensional Lean theorem still uses three standard axioms and four
native-evaluation axioms. No dimension-seven Lean formalization is claimed.

Build from this directory, using TeX Live:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

The unchanged clique, line, dimension-six and geometry sections are imported
from `../sections/`. Reproduce the two bounded checks from the repository root:

```sh
python3 develop/check_dimension_seven_nineteen_obstruction.py --report /tmp/n7-lower19.json
python3 develop/check_dimension_seven_profile_scope.py --report /tmp/n7-scope.json
```

The resulting reports should match `results/dimension-7-nineteen-obstruction.json`
and `results/dimension-7-profile-scope.json`. These commands do not rerun the
separate spread-completion or covering enumerations. See
`notes/dimension-seven-six-holes.md`, `notes/dimension-seven-seven-holes.md`,
`notes/dimension-seven-five-four-D-cover.md`,
`notes/dimension-seven-five-four-H-cover.md`, and
`notes/dimension-seven-profile-scope.md` for their written arguments,
reproduction commands, and precise dependencies.

The [Z exclusion](../../notes/dimension-seven-five-four-Z-cover.md)
uses the proved 128-element marked stabilizer and a newly audited finite
covering certificate. Together with the separate D/H/G exclusions, it
closes exactly the specified raw profile, leaving 26 five-plus-six and
39 three-six count candidates. Reproduce its bounded builder and auditor
with the commands in the Z proof note. The scope auditor above retains
its earlier snapshot of 27/39 candidates; the Z covering auditor
independently reconstructs the count catalogs and records the one-row
update. The exact dimension-seven chromatic numbers remain open >=19.

The subsequent [three-even/pure-six exclusion](../../notes/dimension-seven-three-six-cover.md)
closes `(3,6;6,2,8)` using its own three-form geometry, full marked
groups and complete necessary roots. The new auditor checks all
248/474/557 representatives and 1,949 reachable failed states,
including every one of 676 branches and 1,332 leaves. This leaves
25 five-plus-six and 39 three-six candidates, of which 62 have six
through eight pure odd heptads and two have five. Reproduce the
new builder and auditor using the commands in its proof note;
earlier covering certificates are not proof inputs. The extended
draft includes this result, with exact n7 still open >=19.

The [two-even/four-odd three-six exclusion](../../notes/dimension-seven-two-six-six-cover.md)
closes `(2,6,6;7,0,8)`. Recoloring excludes inside-M sums using
the earlier `(2,6;7,1,8)` theorem and its historical finite cover input.
For outside-M sums, the full order-eight marked group reduces all 384
distinct necessary 49-point sets to 75 representatives. The new finite
proof uses all 288 even heptads, including the 64 avoiding M, and retains
both actual defect holes. Its independent auditor checks 368 reachable
failed states, 293 branches and 225 leaves; four invalid controls fail.
This removes exactly one three-six row, leaving 25/38 candidates,
including four three-six C=8 rows. Reproduce the new builder and auditor
with the commands in its proof note. The extended draft includes this
result; exact n7 remains open >=19. The submitted snapshot is preserved.

The [transferable pure-six sum](../../notes/dimension-seven-four-four-six-charge.md)
also excludes `(4,4,6;7,0,8)`. Charge forces the pure sextet's sum
q=a+c into the hole Lagrangian M. Moving z+q into that sextet
produces either the previously excluded size-three two-six branch
or the size-four five-plus-six profile `(4,4;7,1,8)`.
The written reduction inherits both theorems' historical finite
cover premises. Its new local auditor checks 840 odd-role assignments,
672 mixed-six classes, 224 completions and 2,429,952 compatible
disjoint local triples, plus source and certificate hash bindings.
It runs no new cover search and does not rerun historical audits.
Exactly one further three-six row is removed: the current totals
are 25/37, with three three-six C=8 rows, 60 candidates with C=6..8
and two with C=5. Exact n7 remains open >=19. Reproduce from the root:

```sh
python3 develop/check_dimension_seven_four_four_six_charge.py --report /tmp/n7-four-four-six-charge.json
```

The [two-charge recoloring reduction](../../notes/dimension-seven-four-five-five-charge.md)
shows that every hypothetical `(4,5,5;7,0,8)` coloring can be moved
to the open `(4,6,6;5,2,8)` branch with two distinct actual defect
holes and both pure-six sums outside M. The unique even completions
of the two `(5,1)` six-defects must come from distinct pure even
heptads: other defect sources and a common heptad source yield
three precisely matched earlier exclusions. Their historical finite
premises are retained, including all D/H/G/Z marked forms.
New finite controls check 1,344 unique completions, 5,376 markings,
1,214,976 disjoint defect triples and separate source-heptad transfers.
These controls construct no complete covering roots or new cover proof.
The original and resulting raw rows remain open; totals stay 25/37.
Reproduce from the root:

```sh
python3 develop/check_dimension_seven_four_five_five_charge.py --report /tmp/n7-four-five-five-charge.json
```

The [transferred two-hole geometry](../../notes/dimension-seven-four-six-six-two-hole.md)
now has three exhaustive marked forms, with full stabilizer orders
8,16,16. The actual ordered hole pairs have 12,7,7 orbits. Each form
has 16 four-even blocks, 18 pure sextets in each role and 6 mixed
even sextets in each role; the 216 disjoint pure-defect pairs have
72,38,38 local orbits. Those actions are not free. All 5,376 ordered
markings have eight explicit normalization controls, and catalog
actions, group closure and actual-hole transport are checked.
Joint compatibility of all five even blocks and a complete necessary
remaining-set family are the next step. No cover search or new raw
exclusion is claimed; this normalization covers the transferred
two-hole subbranch, with 25/37 candidates and exact n7 still open >=19.

```sh
python3 develop/check_dimension_seven_four_six_six_two_hole.py --report /tmp/n7-four-six-six-two-hole.json
```
