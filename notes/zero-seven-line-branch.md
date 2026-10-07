# Exact encoding of the all-fifteen seven-line pattern

The [forcing theorem](forced-seven-line-color.md) restricts every normalized
seventeen-coloring to mask0: all seven special lines have color fifteen.
Fixing the fifteen T-subspaces and the eight independent lines [z+t],
t in T, leaves 554 vertices, 16,730 edges and the palettes proved there.
Color sixteen remains available at every residual vertex; color fifteen
is excluded by fixed neighbors.

The standard-library [builder](../develop/encode_zero_seven_line_branch.py)
emits exactly-one-color clauses and edge-conflict clauses. Its
[report](../results/dimension-7-zero-seven-line-branch-encoding.json) records
7,744 variables and 241,782 clauses: 51,494 vertex clauses and 190,288
edge clauses. The CNF SHA256 is
`e173aaef8a8c42e9d874f137fc06f60f8df86765834dfad57a4eb28df00ca49c`.

The independent [auditor](../develop/check_zero_seven_line_encoding.py)
derives lists from K_U=T intersect U-perp and adjacency from dot products
on every vector pair. It shares only RREF/span enumeration helpers with
the builder. The [audit report](../results/dimension-7-zero-seven-line-branch-encoding-check.json)
checks every expected clause exactly once, rejecting missing, duplicate,
wrong-branch, illegal-variable, incomplete-choice and interior-zero
mutations. Clause and literal permutations are accepted semantically;
the report separately preserves raw byte identity. Optimized Python is
rejected, including direct low-level auditor calls.

```sh
python3 develop/encode_zero_seven_line_branch.py --output-dir /tmp/mask0
python3 develop/check_zero_seven_line_encoding.py /tmp/mask0/dimension-7-zero-seven-line-branch.cnf --controls --report /tmp/mask0-audit.json
```

The encoding was emitted and audited before the new
[omitted-color proof](dimension-seven-eighteen-obstruction.md) excluded
seventeen-colorability. It remains a reproducible encoding of the
conditional mask0 problem, but no solver run was made on it and no
SAT/DRAT result is claimed. The new full-graph lower bound is eighteen;
its exact chromatic number remains open.
