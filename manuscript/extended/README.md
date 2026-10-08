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
Exactly one further three-six row is removed at that step: the totals
are 25/37, with three three-six C=8 rows, 60 candidates with C=6..8
and two with C=5. Exact n7 remains open >=19. Reproduce from the root:

```sh
python3 develop/check_dimension_seven_four_four_six_charge.py --report /tmp/n7-four-four-six-charge.json
```

The [two-charge recoloring reduction](../../notes/dimension-seven-four-five-five-charge.md)
shows that every hypothetical `(4,5,5;7,0,8)` coloring can be moved
to the `(4,6,6;5,2,8)` subbranch with two distinct actual defect
holes and both pure-six sums outside M. The unique even completions
of the two `(5,1)` six-defects must come from distinct pure even
heptads: other defect sources and a common heptad source yield
three precisely matched earlier exclusions. Their historical finite
premises are retained, including all D/H/G/Z marked forms.
New finite controls check 1,344 unique completions, 5,376 markings,
1,214,976 disjoint defect triples and separate source-heptad transfers.
These controls construct no complete covering roots or new cover proof.
This reduction alone excludes neither raw row; the new covering
proof below closes the source row using its transferred subbranch.
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
The [joint-family construction](../../notes/dimension-seven-four-six-six-roots.md)
now completes the necessary five-component families: 1,708,1,648,304
distinct 35-point remaining sets, with unique component decompositions
within each marked form. The complete group orbits number 224,112,21,
with stabilizers of order one or two. All 44,896 root actions retain
paired roles and actual holes. Each root has five residual holes,
so the five residual pure even heptads must come from the 224
anchored heptads. The bitmask builder and independent array auditor
agree on all roots and orbits; four invalid-artifact controls are
rejected. The subsequent
[five-heptad covering proof](../../notes/dimension-seven-four-six-six-cover.md)
now excludes all 357 representatives. Its independent auditor
reconstructs all complete roots and orbits, verifies 359 reachable
failed states, both branches and 357 leaves, and rejects four
invalid-certificate controls. This excludes the transferred
two-hole subbranch and the original raw `(4,5,5;7,0,8)` row.
The exact source transfer retains its three earlier exclusions
and their historical finite premises; those covering audits and
the older normalization/recoloring audits are not rerun.
That certificate removes one raw row, giving the intermediate totals
25/36. The two three-six C8 rows at that stage were
`(4,6,6;5,2,8)` and `(4,5,6;6,1,8)`; the latter is excluded below.
Exact n7 remains open >=19; no new Lean result is claimed.

```sh
python3 develop/check_dimension_seven_four_six_six_two_hole.py --report /tmp/n7-four-six-six-two-hole.json
python3 develop/build_dimension_seven_four_six_six_roots.py --roots /tmp/n7-four-six-six-roots.json
python3 develop/check_dimension_seven_four_six_six_roots.py --roots /tmp/n7-four-six-six-roots.json --report /tmp/n7-four-six-six-roots-check.json
python3 develop/build_dimension_seven_four_six_six_cover.py --certificate /tmp/n7-four-six-six-cover-proof.json --max-states 20000 --max-visits 80000 --seconds 20
python3 develop/check_dimension_seven_four_six_six_cover.py --certificate /tmp/n7-four-six-six-cover-proof.json --report /tmp/n7-four-six-six-cover-check.json
```

The [completion-source theorem](../../notes/dimension-seven-four-five-six-charge.md)
for `(4,5,6;6,1,8)` forces q into an anchored pure even heptad
avoiding t. The common functional has ell(c)=1 and
ell(a)=ell(d)=eta, with both eta=0 and eta=1 retained. The mixed
completion t has a distinct pure source, or for eta=1 a source in
the existing mixed heptad giving a reversible role exchange.
The pure-source transfer gives a `(4,6,6;5,2,8)` branch with
mixed/pure completion locations, outside the earlier paired
mixed/mixed certificate. Its 10,752 markings, 224 completion pairs,
1,344 mixed and 2,016 pure unique completions, source-removal and
actual-hole controls are finite modular checks, not complete joint
roots. All nine inherited theorem source/certificate/dependency
bindings are checked without rerunning historical covering audits.
That source audit excludes no raw row and retains the prior 25/36 lists.
The exhaustive ordered forms and complete joint families follow below.

```sh
python3 develop/check_dimension_seven_four_five_six_charge.py --report /tmp/n7-four-five-six-charge.json
```

The [ordered normalization theorem](../../notes/dimension-seven-four-five-six-symmetry.md)
gives eight exhaustive forms, eta=0,1 and b=a+c,a+d,c+d,a+c+d.
Every full ordered marked group has order eight and fixes every M
point. The mixed-role transfer is a recoloring, not a symmetry
exchanging the original D1 and J roles. All 10,752 ordered markings
are covered by 86,016 normalization images, eight per marking.
All local catalog actions and actual holes are checked. Each form
has 144 disjoint local P/Hq pairs, 48 orbits and twelve ordered
hole allocations; the actions are not free. The pure-source case
requires a 28-point/four-hole remainder and four anchored heptads,
the mixed-source case a 35-point/five-hole remainder and five.
Complete jointly disjoint roots for these twelve source branches
are constructed below; this normalization audit retains the prior counts.

```sh
python3 develop/check_dimension_seven_four_five_six_symmetry.py --report /tmp/n7-four-five-six-symmetry.json
```

The [complete joint-root theorem](../../notes/dimension-seven-four-five-six-roots.md)
and independent audit retain all 51,616 ordered disjoint component
families and 25,364 form-labelled remainders in 3,258 full-group
orbits. Pure sources give 2,604 necessary four-heptad problems;
mixed sources give 654 five-heptad problems. Every remainder has
two, four or eight ordered decompositions, all saved with actual
holes. The full marked groups preserve the original roles and
transport every saved decomposition; unique decomposition and
free action are not assumed. Four invalid-root controls are rejected.
The eligible later-cover catalog is the 224 anchored even heptads,
filtered by containment. The root audit retains the prior 25/36 lists;
its complete necessary covering problem is settled below.

```sh
python3 develop/build_dimension_seven_four_five_six_roots.py --roots /tmp/n7-four-five-six-roots.json
python3 develop/check_dimension_seven_four_five_six_roots.py --roots /tmp/n7-four-five-six-roots.json --report /tmp/n7-four-five-six-roots-check.json
```

The [complete twelve-branch covering theorem](../../notes/dimension-seven-four-five-six-cover.md)
excludes the entire `(4,5,6;6,1,8)` row. All 3,258 representatives
have independently checked failed-state proofs: 3,262 reachable
states, four required branches and 3,258 leaves. Every pivot and
admissible anchored-heptad successor is checked after reconstructing
the complete roots, all decompositions and group orbits. Four invalid
certificate controls are rejected. Exact raw count reconstruction
removes only this row, giving current totals **25/35**, with 58
candidates having C=6..8 and two C=5. The entire `(4,6,6;5,2,8)` row
remains open and is the sole remaining three-six C8 row.
Historical finite premises of the source restrictions remain bound;
no old certificate is used as a new failed-state premise.
Exact n7 remains open with lower bound 19; no new Lean is claimed.

```sh
python3 develop/build_dimension_seven_four_five_six_cover.py --certificate /tmp/n7-four-five-six-cover-proof.json --max-states 30000 --max-visits 120000 --seconds 20
python3 develop/check_dimension_seven_four_five_six_cover.py --certificate /tmp/n7-four-five-six-cover-proof.json --report /tmp/n7-four-five-six-cover-check.json
```

The [remaining-row source theorem](../../notes/dimension-seven-four-six-six-pure-sources.md)
forces both completions in `(4,6,6;5,2,8)` into distinct pure heptads,
each avoiding the other completion. Transfers from either mixed class
would give the newly excluded entire `(4,5,6;6,1,8)` row; transfers
from D0, the other pure sextet or a shared pure source give the other
specified excluded profiles. Four functional patterns 100,010,001,111
remain. The four pure defect/source holes exhaust the functional-one
points, leaving the three nonzero kernel points as holes. Complete
necessary roots would leave 21 points for three heptads selected from
96 kernel-anchored rows. Reversible swaps are recolorings, not assumed
isometries. All 21,504 markings and local source/actual-hole controls
are audited, with ten inherited finite theorem bindings. No complete
joint roots or cover search for this branch is claimed. Counts stay
25/35 and exact n7 remains open with lower bound 19.

```sh
python3 develop/check_dimension_seven_four_six_six_pure_sources.py --report /tmp/n7-four-six-six-pure-sources.json
```
