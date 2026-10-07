# The three-even/pure-six eight-odd profile is excluded

**Theorem.** There is no nineteen-coloring of Gamma_7 with
characteristic class size four and profile
(m5,m6;A,B,C)=(3,6;6,2,8).

The [charge reduction](dimension-seven-three-six-charge.md) proves
that this profile admits exactly three necessary marked forms I/II/III.
The [complete root reduction](dimension-seven-three-six-roots.md)
constructs their necessary remaining sets and proves the full marked
group actions, including transport of the actual pure-six hole and
exchange of mixed roles where allowed. The new finite proof excludes
all their six-heptad covers. This closes one further raw five-plus-six
count row; the remaining totals are 25 five-plus-six and 39 three-six.
Exact dimension-seven chromatic numbers remain open with lower bound 19.

## Reduction to a finite covering proof

A coloring in form I/II/III determines one of respectively
7,408/12,688/8,112 distinct necessary 42-point remaining sets.
Their full marked groups of orders 32/32/16 reduce them to
248/474/557 representatives. Every remaining set has exactly the
six M-holes other than the actual pure-six hole t. Its six even
heptads must each meet M exactly once. Thus the complete eligible
row catalog is the 224 anchored even heptads; containment in the
remaining set excludes every row meeting t. The written group
maps carry these rows and remaining sets bijectively, so exclusion
of every representative excludes every necessary root in each form.
Both mixed roles and both actual-hole orbits remain included.

The bounded builder records a failed state by its nonempty even
remaining set U and an uncovered pivot p. The independent auditor
reconstructs every even heptad by bitmask clique recursion and checks
its original coordinate dot products. For every recorded state it
enumerates **every** anchored heptad H contained in U and containing p.
For each such row it requires U minus H to be another recorded
failed state, with seven fewer points. If no such row exists, no
partition of U into eligible heptads can cover p. The empty set is
never declared failed. Induction on |U| therefore proves that every
recorded state has no cover. The auditor requires every one of the
1,279 form-labelled representatives to occur in this proof and
requires every recorded state to be reachable from one of them.
Shared descendants may be reused; no cross-form equivalence is assumed.

The certificate has 1,949 reachable failed states, 676 checked
branches and 1,332 leaves with no admissible row. The state-size
histogram is 42 points:1,279; 35 points:647; 28 points:23.
All three deliberately invalid controls are rejected. The initial
bounded builder takes 0.20 seconds locally and produces the same
certificate bytes on reproduction; the full independent audit takes
about two seconds with less than 40 MB maximum RSS and zero swaps.

The auditor independently reconstructs the complete root catalogs
and orbit partitions, requiring equality with the archived report,
then binds this new certificate to its hash. It also rejects altered
certificates that omit a required representative, use an absent pivot
or falsely declare the empty set failed. No search-program judgment
or elapsed-time limit is used as a proof premise.

## Count scope and reproducibility

The counting audit reconstructs all 46 five-plus-six and 48 three-six
raw parity-count rows. It checks that (3,6;6,2,8) occurs exactly once
in the previous complete 26-row remaining five-plus-six list and
removes only this row. The 39-row three-six list is unchanged.
There are now 64 size-four count candidates: 62 have six through
eight pure odd heptads and two have five. No five-plus-six C=8
row remains, while five three-six C=8 rows remain. Other profiles
and characteristic sizes four through eight are still open.

The earlier (5,4) covering certificates are not inputs to this new
finite proof. The preceding accounting report supplies the already
established remaining lists; its covering audit is not rerun.
The new [builder](../develop/build_dimension_seven_three_six_cover.py),
[independent auditor](../develop/check_dimension_seven_three_six_cover.py),
[certificate](../results/dimension-7-three-six-cover-proof.json) and
[audit report](../results/dimension-7-three-six-cover-check.json)
record exact inputs, limits and SHA-256 bindings.

No new Lean or independent Pro review is claimed. The original
six-dimensional formal theorem retains three standard and four
native-evaluation axioms. The submitted manuscript is preserved;
the extended working draft incorporates this further partial result.
Publication and submission remain separate joint decisions.

~~~sh
python3 develop/build_dimension_seven_three_six_cover.py --certificate /tmp/three-six-proof.json
python3 develop/check_dimension_seven_three_six_cover.py --certificate /tmp/three-six-proof.json --report /tmp/three-six-check.json
~~~
