# Dimension seven: an exact reduction before search

**Current lower bound:** [chi(O_7*) >= 17](dimension-seven-obstruction.md),
proved by a two-clique forcing obstruction on 29 vertices. The exact
chromatic number remains open. The sixteen-color reductions below are
historical steps; their nonexistence question is now settled by written proof.

The subsequent [subspace retraction](subspace-retraction.md) now reduces
the full graph to 913 vertices with the same chromatic number. Its
fixed-clique list instance has 890 vertices and 33,978 edges. The
larger instances below remain the earlier reduction baselines.

The [forced-color reduction](dimension-seven-propagation.md) now propagates
the 49 singleton lists and gives an exact geometric condition for retaining
color 15. Its remaining connected instance has 14,540 vertices and 928,571
edges; sixteen-colorability is still open. The original counts below are
retained as the baseline before propagation.

The known clique lower bound is 16. Let T = span(3,12,48) inside F_2^7.
Its 15 nonzero subspaces, together with the line span(64), form a 16-clique.
Fix its colors. This note gives an equivalent search reduction, not a new
16-coloring or a proof that 16 colors are impossible.

## Delete all dimensions at least four

Write N(r) for the number of nonzero subspaces of F_2^r. A d-dimensional
vertex U has at most N(n-d) neighbors, since every neighbor is a nonzero
subspace of U-perp. If f fixed clique vertices are adjacent to U, then its
residual degree is at most N(n-d)-f and its color list has k-f elements.
Therefore N(n-d)<k implies the residual degree is strictly smaller than the
list size. Such a vertex can be deleted and restored greedily in reverse order.

For n=7 and k=16, N(3)=15. Every vertex of dimension at least four can be
deleted immediately. This removes 14,606 of the 29,211 vertices. After also
removing the 16 fixed clique vertices, the exact low-dimensional instance is:

| Quantity | Value |
| --- | ---: |
| Uncolored core vertices | 14,589 |
| Core edges | 953,057 |
| Dimension 1 / 2 / 3 vertices | 119 / 2,660 / 11,810 |
| Variables in the pairwise encoding | 214,355 |
| Clauses in the pairwise encoding | 12,984,679 |

The preprocessing constructs adjacency by enumerating the subspaces of each
orthogonal complement. It avoids testing all 426 million full-graph pairs.
There are 49 singleton-list vertices in the low-dimensional instance; their
forced colors provide a starting point for further propagation before SAT.

## Reproduce and interpret

```sh
python3 develop/dimension_seven_feasibility.py --dimension 6
python3 develop/dimension_seven_feasibility.py --dimension 7
```

The dimension-six control reproduces the independently checked original core:
2,080 vertices, 39,400 edges, 28,600 variables and 627,510 clauses.
The dimension-seven report records exact counts and the script hash. Elapsed
time is machine dependent. No dimension-seven solver result is claimed.

Next, propagate singleton lists and investigate which geometric types force
their neighbors' choices. A bounded search may then be useful. The first
priority remains the complete formal verification of the dimension-six result.
