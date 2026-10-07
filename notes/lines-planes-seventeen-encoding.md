# Audited seventeen-color encoding of the lines-and-planes construction

The [sufficient eighteen-color route](eighteen-color-palettes.md) asks for
a seventeen-coloring of the induced graph on all 127 lines and 315
totally isotropic planes in F_2^7. Its 442 vertices have 16,569 edges.
A successful coloring could be extended with one fresh color on the
135 independent isotropic three-spaces, then lifted through the
nonradical retraction. Failure here would exclude this construction
alone, leaving general eighteen-colorability open.

Current status: the later [line-capacity proof](dimension-seven-line-capacity.md)
excludes this entire seventeen-color construction already on its
line vertices. The encoding and earlier unknown solver reports are
retained as history; no UNSAT solver or checked DRAT proof is claimed.
The subsequent [nineteen-color lower bound](dimension-seven-nineteen-obstruction.md)
also excludes eighteen colors on the full graph; its exact value remains open.

## Normalization and exact palettes

Put T=span(3,12,48), z=127. The fourteen nonzero proper subspaces of T
form a clique, and [z] is adjacent to all of them. Normalize this
fifteen-clique to colors 0,...,14, with [z] assigned 14. The deterministic
basis enumeration specifies the first fourteen labels in the
[construction report](../results/dimension-7-lines-planes-17-encoding.json).
Every seventeen-coloring of this graph can be relabeled to agree with
these assignments. No isotropic three-space is a vertex of this graph;
the old sixteen-clique and full-graph seventeen-color forcing arguments
are therefore not imposed here.

For each residual U let K_U=T intersect U-perp. Its list is

```text
{i in 0,...,13: the proper T-subspace of color i is not contained in K_U}
union {14 if U is an odd line}
union {15,16}.
```

The first fourteen exclusions come from the fixed T-subspaces. Color
14 is excluded precisely at even vertices, which are adjacent to [z].
The two extra labels are unrestricted by the fixed clique. Each of the
seven special lines [z+t], nonzero t in T, retains all three choices
{14,15,16}. No special line is preassigned.

The equivalent residual list problem has

```text
427 vertices = 119 lines + 308 planes,
14,994 edges, 5,789 variables and 197,344 clauses,
list-size histogram {3:7, 12:140, 13:56, 15:224}.
```

A residual list coloring extends by the fifteen fixed vertices because
its lists exclude exactly the fixed-neighbor colors. Conversely, every
normalized coloring restricts to these lists. The pairwise CNF requires
exactly one allowed color per vertex and forbids a shared color at every
residual edge. It has 37,576 vertex clauses and 159,768 edge clauses.

## Clause audit and bounded attempt

The standard-library [builder](../develop/encode_lines_planes_seventeen.py)
constructs adjacency from basis dot products and lists from fixed
neighbors. The independent [auditor](../develop/check_lines_planes_encoding.py)
uses the geometric formula above and tests orthogonality on every vector
pair in the two spans. They share only the canonical RREF/span helpers.
The [audit](../results/dimension-7-lines-planes-17-encoding-check.json)
matches each expected clause exactly once. Missing, duplicate,
wrong-construction, illegal-variable, incomplete-choice and interior-zero
mutations are rejected. A permutation of clauses and literals is
accepted semantically while changing the recorded byte hash. Direct
auditor calls under optimized Python are rejected.

The deterministic CNF SHA256 is
`f3c9d0d2df5217baad87c93ca6a3e8dcd33d53182c5aa5249962f2187a89d116`.

One 120-second Glucose4 attempt on this audited instance returned
**unknown**, with no coloring or UNSAT proof. The
[search report](../results/dimension-7-lines-planes-17-search.json)
records its actual elapsed time, statistics, solver version and source
hashes. Unknown supplies neither an upper bound nor evidence against
this construction. Further work should establish structural or symmetry
restrictions before repeating the unchanged search.

```sh
python3 develop/encode_lines_planes_seventeen.py --output-dir /tmp/lines-planes
python3 develop/check_lines_planes_encoding.py /tmp/lines-planes/dimension-7-lines-planes-17.cnf --controls --report /tmp/lines-planes-audit.json
python develop/search_lines_planes_seventeen.py /tmp/lines-planes/dimension-7-lines-planes-17.cnf --seconds 120 --output-dir /tmp/lines-planes
```

The first two commands need the standard library; the search additionally
needs python-sat. A SAT candidate must be independently checked, extended
to the 577 retained vertices and lifted and checked on the original
29,211-vertex graph before a full upper bound is claimed. A reported UNSAT
result needs a checked proof and justified encoding; even then it would
exclude only this sufficient route. Exact full n=7 chromatic number
remains open with lower bound eighteen. No Lean run is part of this step;
the original dimension-six formal theorem retains three standard and
four native-evaluation axioms. The submitted manuscript remains at 28e27a8.

The [ternary symmetry reduction](ternary-line-symmetry.md) now preserves
all auxiliary seventeen-color solutions while retaining one of 32
special-line patterns. It audits 2155 added clauses, giving 199499 total;
no additional solve has been run. The same continuation repairs the
search wrapper to use one immutable CNF snapshot and a supported timer
range. Historical encoding and search reports retain their original
source hashes; the new symmetry report binds the current clause auditor.
