# A checked SAT encoding of the retracted graph

The [retraction theorem](subspace-retraction.md) turns sixteen-colorability
of the full dimension-seven graph into a list-coloring problem on 890
vertices. This note records a reproducible encoding and one bounded search,
not a new chromatic-number result.

The search script constructs adjacency directly from basis dot products,
independently of the orthogonal-complement enumeration used in the earlier
retraction report. It reproduces all 38,355 edges on the 913 retained
vertices and all 33,978 edges on the uncolored core. It fixes distinct
colors on the sixteen-clique and color fifteen on the seven extra forced
lines. Each remaining palette is also checked against the geometric
formula using T intersect U-perp and the condition e in U+T. In particular,
color fifteen is absent from every remaining palette.

Variables are ordered by canonical vertex index, then increasing color.
For each vertex, one positive clause requires a color and every pair of
choices contributes a negative clause to prevent two colors. For every
edge and each color in both endpoint lists, one negative clause prevents
equal colors. The instance has 11,558 variables and 426,406 clauses:
71,184 vertex clauses and 355,222 edge clauses. A satisfying assignment
is exactly a list coloring; adding the fixed vertices and composing with
the retraction gives a sixteen-coloring of the original graph. Conversely,
any sixteen-coloring can be relabeled on the fixed clique and restricts
to a satisfying assignment.

The standard-library checker reconstructs the retained vertices, forced
lines and lists from their geometric descriptions. It constructs the
expected clause set independently of the search script, using direct
dot products for adjacency. It reads the generated DIMACS file and
requires each expected clause exactly once, with no additional clauses.
The two scripts share the canonical basis enumerator; they do not share
adjacency, palette, propagation or CNF construction code. All 426,406
clauses pass this audit. Separate damaged-input controls reject a missing
clause and an out-of-range positive literal. A fresh encoding has
byte-identical DIMACS output, with SHA256

```text
0867f899c5d1f737ba44e1e473f59c188f71d390c274d47f487e1505f534745f
```

As a positive control, the existing dimension-six certificate is relabeled
on the fifteen-clique and satisfies every clause of the corresponding
218-vertex retracted instance. Its 47,414 clauses also pass the independent
DIMACS audit. This checks the encoding against an existing witness; the
historical full-graph certificate is not rerun or replaced.

## Bounded solver attempt

On October 7, 2026 (Singapore), Glucose4 via python-sat 1.8.dev24 was run
with a 120-second interrupt limit. The limited solve returned unknown
after 123.135 seconds, including interrupt latency. It recorded 1,189,701
conflicts and 1,483,359 decisions. No satisfying witness or UNSAT result
was obtained. These statistics are diagnostics and imply no upper or
lower bound beyond the already known sixteen-clique.

The run used an isolated Python 3.12 environment on a 16 GiB Mac, after
checking available memory and active Lean/Lake processes. No Lean ran.
No shared CI or submitted manuscript was changed. Reports bind the source
files, the earlier retraction report and the generated CNF by SHA256;
the CNF can be regenerated and is not added to the repository.

## Reproduction

Use the existing pinned requirements in a task-specific environment:

```sh
python3.12 -m venv /tmp/nikandish-sat-env
/tmp/nikandish-sat-env/bin/python -m pip install -r requirements-search.txt
/tmp/nikandish-sat-env/bin/python develop/search_retracted_coloring.py --dimension 6 --encode-only --output-dir /tmp/nikandish-sat-output
/tmp/nikandish-sat-env/bin/python develop/search_retracted_coloring.py --dimension 7 --seconds 120 --output-dir /tmp/nikandish-sat-output
python3 develop/check_retracted_encoding.py /tmp/nikandish-sat-output/dimension-6-retracted.cnf --dimension 6
python3 develop/check_retracted_encoding.py /tmp/nikandish-sat-output/dimension-7-retracted.cnf --dimension 7
```

Use `--encode-only` for dimension seven to regenerate without another search.
See the [seven-dimensional search report](../results/dimension-7-retracted-search.json)
and [clause audit](../results/dimension-7-encoding-check.json), and the
[six-dimensional witness control](../results/dimension-6-retracted-search.json)
and [clause audit](../results/dimension-6-encoding-check.json).

Dimension seven remains open. Any future SAT candidate must be independently
checked against the original graph, and any UNSAT report needs a checked
proof and justified encoding. The original six-dimensional formal theorem
continues to depend on three standard and four native-evaluation axioms.
