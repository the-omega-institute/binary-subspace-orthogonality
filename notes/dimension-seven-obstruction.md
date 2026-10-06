# A 29-vertex obstruction to sixteen colors

**Theorem.** The full binary subspace orthogonality graph in dimension
seven satisfies

```text
chi(O_7*) >= 17 > omega(O_7*) = 16.
```

Its exact chromatic number remains open. This lower bound concerns the
full subspace graph, not only the line graph. It follows from the following
explicit 29-vertex induced subgraph, whose chromatic number is exactly 17.

Write vectors as binary integers, with coordinate vectors 1, 2, 4, ..., 64.
Set

```text
L_1 = span(66,12,48),    L_2 = span(65,12,48),
z = 127,               a = 1,               b = 2.
```

Each L_i is totally isotropic of dimension three: its displayed generators
have even weight and pairwise disjoint supports. Thus its fifteen nonzero
subspaces form a clique C_i. The two spaces intersect in span(12,48), which
has four nonzero subspaces. Hence C_1 union C_2 has 15+15-4=26 vertices.
Add the three distinct lines span(z), span(a), span(b) to obtain 29 vertices.

Every vector in either L_i has even weight. Since z is the all-ones vector,
span(z) is adjacent to every vertex of both C_i. Also a is perpendicular
to L_1, since its first coordinate vanishes, and b is perpendicular to L_2,
since its second coordinate vanishes. Finally a dot b=0, so their two lines
are adjacent. Neither odd line belongs to either C_i.

Suppose this graph had a proper coloring with at most sixteen colors.
The clique C_1 together with span(z) has sixteen vertices, so it uses all
sixteen colors. Since span(a) is adjacent to every vertex of C_1, it must
have the color of span(z). The same argument with C_2 forces span(b) to
have that color too. This contradicts the edge between span(a) and span(b).
Thus the induced graph, and consequently O_7*, require at least seventeen
colors. This is a written proof; it does not depend on an UNSAT solver.

## An explicit seventeen-coloring of the obstruction

Assign distinct colors zero through fourteen to the fifteen vertices of
C_1. The coordinate permutation swapping the first and second coordinates
maps L_1 to L_2 and fixes span(12,48) pointwise. Give the corresponding
subspace of L_2 the same color. This is well-defined on the four shared
vertices. A matched pair of distinct subspaces is not orthogonal: it has
vectors 66+t and 65+t for the same t in span(12,48), whose dot product is
one. Thus no edge receives equal colors in C_1 union C_2.

Give span(z) and span(b) color fifteen, and span(a) color sixteen.
The two lines with color fifteen are not adjacent, since z dot b=1.
These seventeen colors properly color the 29-vertex induced graph.
Together with the forcing argument, this proves its chromatic number is 17.

The independent standard-library [checker](../develop/check_dimension_seven_obstruction.py)
enumerates the subspaces of these two eight-element spaces without using
the earlier graph builder or retraction code. It checks all 406 vertex
pairs, including 261 edges, the two clique/forced-line configurations,
their four-vertex overlap, and the explicit seventeen-color witness.
The [certificate and report](../results/dimension-7-obstruction.json)
contains all 29 bases, their colors, the clique indices and the complete
edge list, bound to the checker by SHA256.

```sh
python3 develop/check_dimension_seven_obstruction.py --report /tmp/dimension-7-obstruction.json
```

## Consequence for the retracted SAT instance

The earlier fixed clique uses T=span(3,12,48), with color fifteen on
span(64). Its forced lines include span(z), since z=64+63 and 63 belongs
to T. The four nonzero subspaces of A=span(12,48) are fixed vertices of
both the T clique and C_1.

The eleven vertices of C_1 outside T, together with span(a), form a
twelve-clique in the uncolored retracted core. Each is perpendicular to
A, so none can use the four colors assigned to its nonzero subspaces.
Color fifteen is also absent from their lists, by the previous geometric
list formula. Thus twelve mutually adjacent vertices have lists drawn
from only eleven colors. The checker verifies this twelve-clique and
eleven-color palette union exactly.

This is an explicit pigeonhole obstruction to the checked sixteen-color
encoding. The [bounded solver run](retracted-sat-encoding.md) returned
unknown before this obstruction was identified; its timeout supplied no
part of the lower-bound proof. No DRAT or Lean proof is claimed. The
original six-dimensional equality and its three standard plus four
native-evaluation axioms are unchanged. Determining chi(O_7*) and deciding
how this extension relates to the submitted manuscript remain subsequent
research and joint manuscript decisions.
