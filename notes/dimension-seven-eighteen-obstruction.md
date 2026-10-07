# The full dimension-seven graph requires at least eighteen colors

**Theorem.** For the standard dot product on F_2^7, the orthogonality graph
on all nonzero subspaces satisfies chi(O_7*) >= 18. Its clique number is 16.
The exact chromatic number remains open.

We encode a vector by its binary integer, with vector addition given by XOR.
Write [a] for the line span(a), and S(L) for the fifteen nonzero subspaces
of a totally isotropic three-space L. These subspaces form a fifteen-clique.
All vertices used below are lines or totally isotropic subspaces, so the
proof applies directly both to the full graph and to the
[retained graph](nonradical-line-retraction.md).

Suppose there is a coloring with at most seventeen colors. Put

```text
T = span(3,12,48),    z = 127,    E = z-perp.
```

The fifteen-clique S(T), together with [z], is a sixteen-clique. After
relabeling, S(T) uses colors 0,...,14 and [z] uses color 15. Use the palette
0,...,16, even if the coloring uses fewer colors. The lines [124]=[z+3]
and [115]=[z+12] are adjacent to every vertex of S(T), so their colors
belong to {15,16}.

## Two anchors must have color fifteen

The [general forcing theorem](forced-seven-line-color.md) already proves
this for all seven lines [z+t], nonzero t in T. Here are the two instances
needed in this proof, including their conditional contradictions:

| Assumed color-16 line | First isotropic three-space | Second isotropic three-space | Triangle of lines |
| --- | --- | --- | --- |
| [124] | span(3,48,71) | span(3,48,75) | [56], [52], [115] |
| [115] | span(12,48,65) | span(12,48,66) | [62], [61], [124] |

For either row, both fifteen-cliques are adjacent to [z] and to the
assumed color-16 line. They therefore each use all colors 0,...,14.
The first triangle line is adjacent to every vertex of the first clique;
the second to every vertex of the second clique; the third to every vertex
of S(T). Thus all three triangle lines have colors in {15,16}.
Their pairwise orthogonality makes this impossible. Each row independently
excludes color 16 at its anchor; neither assumes the other anchor's color.
Consequently both [124] and [115] have color 15.

## The omitted-color contradiction

Set

```text
A = span(48,65,71),    B = span(48,66,71),
v = [62]=[z+65],    u = [56]=[z+71],    w = [61]=[z+66].
```

Both A and B are totally isotropic three-spaces in E. Every vertex of
S(A) and S(B) is adjacent to [z], so both fifteen-cliques avoid color 15.
From the remaining sixteen-color palette P={0,...,14,16}, each uses
fifteen distinct colors and omits exactly one. Call these omitted colors
m(A) and m(B).

The lines v and u are orthogonal to A; w and u are orthogonal to B.
Moreover v and w are adjacent to [124], and u is adjacent to [115].
Since the two anchors have color 15, v,u,w all avoid that color.
Thus adjacency to the fifteen-cliques forces

```text
c(v) = c(u) = m(A),    c(w) = c(u) = m(B).
```

In particular c(v)=c(w). But v and w are distinct adjacent lines:
62 AND 61 = 60 has even binary weight four. This contradiction proves
the theorem.

The proof uses only explicit dot products and the pigeonhole principle.
No retraction, list-encoding equivalence or solver result is needed for
the lower bound on the original graph.

## Finite certificate and reproduction

The standard-library [checker](../develop/check_dimension_seven_eighteen_obstruction.py)
constructs S(T) and the six additional displayed fifteen-cliques, the two
anchor certificates and the omitted-color configuration. The combined
[certificate](../results/dimension-7-eighteen-obstruction.json) has 82
distinct vertices. It records the entire induced orthogonality graph on these vertices,
checking all 3,321 pairs and finding 1,066 edges. Each conditional anchor
certificate has 42 vertices, 861 checked pairs and 425 edges. Removing
fixed T-subspaces from the final omitted-color configuration gives 28
residual vertices, with 378 checked pairs and 233 edges. A wrong middle
line and a repeated endpoint are rejected by negative controls.

```sh
python3 develop/check_dimension_seven_eighteen_obstruction.py --report /tmp/dimension-7-eighteen-obstruction.json
```

The certificate checks the finite geometry supporting the written proof;
it is not a SAT/DRAT proof or a Lean formalization. No new SAT solver or
Lean run establishes this result. The separately
[audited mask0 encoding](zero-seven-line-branch.md) is now excluded by
this written argument, so no search on that seventeen-color instance
is needed. Earlier sixteen-color and nonzero-mask obstructions remain
valid historical stages. No eighteen-coloring of the full graph is
claimed. The submitted manuscript at revision 28e27a8 is preserved;
this extension is available for coauthor review. The original dimension-six
formal theorem retains its three standard and four native-evaluation axioms.
