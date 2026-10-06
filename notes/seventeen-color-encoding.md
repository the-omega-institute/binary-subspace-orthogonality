# A checked seventeen-color encoding and a smaller clique choice

The [nonradical-line retraction](nonradical-line-retraction.md) reduces
the full seven-dimensional graph to 577 vertices without changing its
chromatic number. The [written obstruction](dimension-seven-obstruction.md)
proves a lower bound of seventeen. This step emits and audits the
seventeen-color instance, records one bounded unknown solver outcome,
and checks a smaller alternative precoloring. The exact full-graph
chromatic number remains open.

## The emitted instance

Fix colors zero through fourteen on the fifteen nonzero subspaces of
T=span(3,12,48), and color fifteen on span(64). Only these sixteen clique
vertices are preassigned. The remaining 561 vertices have the geometric
lists described in the retraction note, with color sixteen available
at every vertex. The seven formerly forced odd lines keep both colors
fifteen and sixteen. No previous singleton assignment or propagation
of color fifteen is reused.

The [search builder](../develop/search_nonradical_coloring.py) orders
variables by canonical vertex index, then increasing color. For every
vertex it requires exactly one listed color using one positive clause
and all pairwise negative clauses. Every edge gets one negative clause
for each common color. The emitted DIMACS instance has

```text
561 vertices, 18,056 edges, 8,174 variables,
257,402 clauses = 57,476 vertex clauses + 199,926 edge clauses.
```

The [standard-library auditor](../develop/check_nonradical_encoding.py)
constructs all expected clauses from the geometric lists and direct
dot products, independently of the search builder's graph and CNF
loops. It shares only the canonical RREF basis enumeration and span
helper. It requires every expected clause exactly once and rejects
additional or duplicate clauses. All 257,402 clauses pass; separate
controls reject a deleted clause and a repeated clause. A fresh
encoding is byte-identical, with SHA256

```text
f346ce031264a3c9e089745a71cf2e576cea2556b7193d82aecc82ec44ccfa18
```

The corresponding six-dimensional positive control has 138 uncolored
vertices, 2,074 edges, 1,638 variables and 29,014 clauses. The existing
fifteen-color certificate, relabeled on its clique, satisfies every
clause, and all clauses pass the independent DIMACS audit. This checks
the new encoding against a known witness; the historical full-graph
coloring certificate is preserved and not rerun in this step.

## One bounded search

On October 7, 2026 (Singapore), Glucose4 via python-sat 1.8.dev24 ran
with a 120-second interrupt limit on the audited seventeen-color
instance. It returned unknown after 120.018 seconds, recording
1,367,021 conflicts and 2,910,199 decisions. No satisfying assignment
or UNSAT result was obtained. These statistics are diagnostics;
the timeout adds no chromatic bound.

The historical run used the existing task-specific Python 3.12 environment on a
16 GiB Mac after a current resource and Lean/Lake process check. No
Lean or shared CI change occurred. The [solver report](../results/dimension-7-17-nonradical-search.json)
and [clause audit](../results/dimension-7-17-encoding-check.json) bind
the emitted CNF, the builder, the auditor and the preceding retraction
source/report by SHA256. The CNF is reproducible and is not committed.

## Choosing the characteristic-vector line instead

Put z=127, the all-ones vector. For every binary vector v,

```text
z dot v = v dot v = coordinate parity of v.
```

Thus span(z) is adjacent to every retained even vertex and to no odd
line. It has 513 retained neighbors: 63 even lines, 315 totally
isotropic planes and 135 totally isotropic three-spaces. The old
span(64) has only 153 retained neighbors.

The fifteen nonzero subspaces of T together with span(z) are again
a sixteen-clique. Fixing their colors is an equally complete
normalization for seventeen-colorability: restrict any coloring to
this clique and permute its sixteen distinct labels to zero through
fifteen, leaving the seventeenth label free. No assumption that the
two odd lines span(64) and span(z) have the same color is made.

With span(z) fixed to color fifteen, that color is forbidden at every
uncolored even vertex and allowed at every uncolored odd line. Color
sixteen remains available everywhere. The seven other odd lines of
T-perp still have the two-color list {15,16}; none is preassigned.

The [exact comparison](../develop/compare_clique_precolorings.py) checks
every alternative list both by fixed-neighbor exclusion and by this
parity formula. It yields

| Quantity | Fixed line 64 | Fixed line 127 |
| --- | ---: | ---: |
| Uncolored vertices | 561 | 561 |
| Edges among uncolored vertices | 18,056 | 17,696 |
| Encoding variables | 8,174 | 7,814 |
| Pairwise clauses | 257,402 | 244,442 |

The [comparison report](../results/dimension-7-characteristic-clique.json)
records the palette distribution and source hashes at the preceding
comparison step. The smaller count alone does not establish better solver
performance.

## Auditing the characteristic-clique instance

The builder now accepts `--last-line 127`, while its default remains the
original line 64. The auditor separately constructs the alternative lists
using coordinate parity for color fifteen. All 244,442 emitted clauses
match exactly once: 52,180 vertex clauses and 192,262 edge clauses.
Deleted-clause, repeated-clause and wrong-clique controls are rejected.
A fresh characteristic-clique CNF is byte-identical, with SHA256

```text
e22cc8925d3450f064626fdf5ed33b7d61d021351fbf7d9bf85644c5a888512f
```

The [current audit](../results/dimension-7-characteristic-encoding-check.json)
binds the CNF and current auditor source. Replaying the default line-64
builder yields the same CNF bytes as the historical run. The historical
search and clause reports retain their original source hashes and can be
reproduced at revision `fe35c9d`; they are not current-source audits.

The six-dimensional retraction control now explicitly checks that its
retained witness uses at most fifteen labels, in addition to checking
every retained edge. It uses exactly fifteen. Both retraction reports
were regenerated against the repaired source, rechecking every original
edge in dimensions six and seven. This is an audit repair, with no change
to the historical witness or theorem. The current six-dimensional
[encoding control](../results/dimension-6-palette-bound-encoding.json)
and [clause audit](../results/dimension-6-palette-bound-encoding-check.json)
also pass; the historical full-graph coloring is not rerun.

One Glucose4 attempt on the audited characteristic-clique CNF returned
unknown after 120.047 seconds under a 120-second interrupt limit. It
recorded 1,298,217 conflicts and 3,035,516 decisions. No SAT candidate or
UNSAT result was obtained. The [characteristic-clique search report](../results/dimension-7-characteristic-search.json)
binds this separate attempt to its CNF and current source hashes.
This was the only solver attempt in this continuation; the earlier
line-64 attempt remains historical. Neither timeout gives a chromatic
bound or a reliable comparison of solver performance.

The subsequent [seven-line symmetry proof](seven-line-symmetry.md)
reduces the 128 two-color patterns to ten GL(3,2) representatives
without losing seventeen-colorability. Its 118 added clauses have
been emitted and checked, with no further solver run.

The geometric auditor now refuses `python -O` and `PYTHONOPTIMIZE`,
since its acceptance checks require assertions. A header-only file
is rejected in normal execution, and optimized execution is refused
for both malformed and valid inputs. The current clause reports
were refreshed against this guarded source; their CNF bytes remain
unchanged. Historical source-hash reports retain their pinned revisions.
In the characteristic search report the legacy `nonradical_report_sha256`
field hashes `results/dimension-7-characteristic-clique.json`; the
`retraction_sha256` field separately identifies the retraction source.

## Reproduction

Use the task-specific environment with the repository's pinned search
requirements. Generate and audit before attempting a solve:

```sh
python3.12 -m venv /tmp/nikandish17-env
/tmp/nikandish17-env/bin/python -m pip install -r requirements-search.txt
/tmp/nikandish17-env/bin/python develop/search_nonradical_coloring.py --dimension 6 --encode-only --output-dir /tmp/nikandish17-output
/tmp/nikandish17-env/bin/python develop/search_nonradical_coloring.py --dimension 7 --encode-only --output-dir /tmp/nikandish17-output
python3 develop/check_nonradical_encoding.py /tmp/nikandish17-output/dimension-6-15-nonradical.cnf --dimension 6
python3 develop/check_nonradical_encoding.py /tmp/nikandish17-output/dimension-7-17-nonradical.cnf --dimension 7
/tmp/nikandish17-env/bin/python develop/search_nonradical_coloring.py --dimension 7 --seconds 120 --output-dir /tmp/nikandish17-output
/tmp/nikandish17-env/bin/python develop/compare_clique_precolorings.py
/tmp/nikandish17-env/bin/python develop/search_nonradical_coloring.py --dimension 7 --last-line 127 --encode-only --output-dir /tmp/nikandish17-output
python3 develop/check_nonradical_encoding.py /tmp/nikandish17-output/dimension-7-17-nonradical-characteristic.cnf --dimension 7 --last-line 127
/tmp/nikandish17-env/bin/python develop/search_nonradical_coloring.py --dimension 7 --last-line 127 --seconds 120 --output-dir /tmp/nikandish17-output
```

A future satisfying witness must be lifted and independently checked
against the original graph. An UNSAT solver report requires a checked
proof and justified encoding. No seventeen-color upper bound is
claimed. The submitted manuscript is unchanged, and the original
six-dimensional formal theorem retains three standard and four
native-evaluation axioms.
