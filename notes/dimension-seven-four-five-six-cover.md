# Complete twelve-branch covering exclusion of the four-five-six row

**Theorem.** No nineteen-color line coloring with characteristic
size four has profile `(4,5,6;6,1,8)`. The independent finite covering
audit checks all twelve completion-source branches. This removes
exactly one three-six count row, leaving **25 five-plus-six and 35
three-six** candidates. Exact n=7 remains open with lower bound 19.

## Written reduction and finite induction

The [completion-source theorem](dimension-seven-four-five-six-charge.md)
forces q into an anchored pure heptad Hq avoiding t, while t has
a distinct pure source Ht or, for eta=1, the existing mixed source J.
The [ordered normalization theorem](dimension-seven-four-five-six-symmetry.md)
retains all eight forms and all twelve source branches. These written
reductions retain their exact historical covering premises; none is
replaced by the earlier paired mixed/mixed certificate.

The [complete joint-root reduction](dimension-seven-four-five-six-roots.md)
constructs every necessary disjoint tuple and retains every ordered
component decomposition and actual hole. Its full marked groups
transport every tuple and every eligible heptad, so one representative
per complete remaining-set orbit is sufficient. There are 2,604
pure-source representatives with 28 points/four holes and 654
mixed-source representatives with 35 points/five holes. The actions
need not be free; decomposition need not be unique.

Hole capacity forces every residual pure even heptad to contain
exactly one remaining M-hole. Thus the full eligible catalog is
the 224 anchored even heptads, restricted by containment. A cover
must include an eligible heptad through any chosen point p of a
nonempty remainder R. Removing it gives R minus H with seven fewer
points and one fewer hole.

The certificate records a pivot in each failed state. The auditor
enumerates **every** anchored heptad contained in that state and
containing its pivot, requiring every resulting remainder to be
another recorded failure. The empty set is never recorded as failed.
Induction on the number of remaining points proves that every
recorded state has no cover: a leaf has no admissible pivot heptad;
at a nonleaf every possible pivot heptad leads to a smaller failed
state. Every orbit representative is a recorded failure, so no
necessary remainder admits its four- or five-heptad cover. Therefore
no coloring in the entire source row exists.

## Evidence scope

The certificate has **3,262 reachable failed states**, **four required
successor branches** and **3,258 leaves** with no admissible pivot
heptad. State sizes 28 and 35 occur 2,608 and 654 times respectively.
All 3,258 orbit representatives are checked. The bounded construction
visits 3,262 states within limits of 30,000 stored failures, 120,000
visits and 20 seconds; the certificate is complete rather than a
timeout report.

The [bounded bitmask builder](../develop/build_dimension_seven_four_five_six_cover.py)
produces a [finite failed-state certificate](../results/dimension-7-four-five-six-cover-proof.json).
The [independent array/set auditor](../develop/check_dimension_seven_four_five_six_cover.py)
first reconstructs all twelve joint-root families and full group orbits,
agreeing exactly with their archived report. It enumerates all 288 even
heptads and selects the 224 anchored rows. It checks every pivot,
admissible successor, root and reachable state. Missing representatives,
absent pivots, false empty failures and omitted required successors
are rejected. Exact raw count equations are reconstructed independently,
and only `(4,5,6;6,1,8)` is removed from the prior 25/36 lists.

The [audit report](../results/dimension-7-four-five-six-cover-check.json)
binds the new source, note and certificate, the complete roots and
the previous source/normalization evidence. Nine inherited theorem
report/source/certificate/dependency bindings remain checked, retaining
the finite premises used by the source restrictions. Historical
covering audits and previous normalization/source controls are not rerun.
No old certificate is used as a failed-state premise of this new
twelve-branch covering proof.

The whole `(4,6,6;5,2,8)` raw row remains open: its previously excluded
paired mixed/mixed subbranch does not exhaust it. It is now the sole
remaining three-six row with C=8. Of the 60 current candidates, 58
have C=6,7,8 and two have C=5. Characteristic sizes four through eight
remain open, so this partial exclusion does not decide the nineteen-color
problem. No dimension-seven Lean or new independent Pro review is
claimed. The original n=6 theorem retains three standard plus four
native-evaluation axioms. The submitted snapshot is preserved.

```sh
python3 develop/build_dimension_seven_four_five_six_cover.py --certificate /tmp/dimension-7-four-five-six-cover-proof.json --max-states 30000 --max-visits 120000 --seconds 20
python3 develop/check_dimension_seven_four_five_six_cover.py --certificate /tmp/dimension-7-four-five-six-cover-proof.json --report /tmp/dimension-7-four-five-six-cover-check.json
```
