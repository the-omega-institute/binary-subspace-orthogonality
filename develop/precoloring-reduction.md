# Dimension-six precoloring reduction

28 September 2026. This note prepares the search proposed by Reza Nikandish.
It does not assert a 15-coloring or a noncolorability result.

Let T = span(3,12,48) in the integer vector encoding of the supplied
coloring-certificate.json. T is a totally isotropic 3-space and T-perp = T.
Its 15 nonzero subspaces form a clique C. Give each W in C its own color c_W.
Every 15-coloring can be relabeled this way, so fixing these colors loses no
solution.

For a vertex U outside C, put H(U) = U-perp intersect T. Then U is adjacent to
W in C exactly when W is contained in H(U). Its allowed color list is therefore

    L(U) = {c_W : 0 != W <= T and W is not contained in H(U)}.

If H(U) = T, then U <= T-perp = T, contrary to U being outside C. Thus
dim H(U) is 0, 1 or 2, and |L(U)| = 15 - N(dim H(U)) is respectively 15,
14 or 11. N(2)=4 includes the three lines and the 2-space itself.

The exact enumeration gives:

| dim H(U) | Allowed colors | Vertices outside C |
| --- | --- | --- |
| 0 | 15 | 1,017 |
| 1 | 14 | 1,435 |
| 2 | 11 | 357 |

These sum to 2,809, the 2,824 graph vertices minus the fixed clique.
The full graph has 44,968 edges. The remaining task is list coloring the
induced graph outside C with the displayed lists.

## Reversible deletion

Repeatedly delete a vertex U whose current uncolored degree is strictly less
than |L(U)|, recording the deletion order. Every coloring of the remaining
instance extends in reverse order: at reinsertion, fewer than |L(U)| colored
neighbors can forbid colors from L(U). Conversely any original coloring
restricts to a coloring of the remaining instance. This is an equivalence,
not a heuristic claim that the original instance is colorable.

The supplied deletion certificate removes 729 vertices and leaves 2,080
vertices and 39,400 edges. The core has 56 lines, 644 planes and 1,380
3-spaces; all spaces of dimensions at least four have been removed.
The script replays each deletion by recomputing its degree from the original
adjacency lists. No vertex in the resulting core meets the deletion rule.

## Reproduce

Keep precoloring_reduction.py beside coloring-certificate.json and run:

    python3 precoloring_reduction.py

This regenerates precoloring-reduction.json with the fixed clique indices,
remaining indices, deletion order, counts and source hashes. Indices are into
the unchanged subspace_colors array in the original certificate. The reduction
uses the supplied complete subspace enumeration and checks distinctness and
the Gaussian dimension counts. The earlier independent check_certificate.py
validates the original 14- and 16-color witnesses separately.

No SAT solver, exhaustive 15-color search or Lean process was run here.

## Next experiment

Encode one color choice from L(U) for each core vertex and forbid equal colors
on every core edge. A satisfying assignment can be extended through the
recorded deletion order and checked against every original graph edge.
For nonexistence, retain a solver proof and check both its validity and the
faithfulness of the encoding before asserting chi(O_6*)=16. A timeout is not
nonexistence. If a small obstruction is found, analyze it through the subspaces
H(U) and their incidences with T to look for a geometric proof.

For the separate paper, the exact all-dimensional clique theorem and the
dimension-six coloring problem are the core. Broader graph parameters can be
added where they yield substantive results. Nikandish has offered to draft the
introduction and clique section; manuscript/source exchange by email suffices.
