# Exact odd-line lists for an eighteen-color construction

The full dimension-seven graph has lower bound eighteen; its exact
chromatic number remains open. The [nonradical retraction](nonradical-line-retraction.md)
reduces the upper-bound problem to 577 vertices: 513 nonzero totally
isotropic subspaces in the symplectic space E=127-perp and 64 odd lines.
This note gives an exact conditional extension criterion and necessary
constraints on a prospective eighteen-color construction.

Put z=127 and write the odd lines as [z+e], e in E. Normalize [z] to color
15, and use the other seventeen labels P={0,...,14,16,17} on the even
vertices. Every even vertex is adjacent to [z], so any full eighteen-color
coloring has this form. Conversely, start with any proper coloring c of
the 513 even vertices into P. For each Lagrangian three-space L in E,
let S(L) be its fifteen nonzero subspaces and define its omitted pair

```text
M(L) = P minus {c(U): U in S(L)}.
```

Since S(L) is a fifteen-clique, M(L) has exactly two elements. For e in E
define

```text
I(e) = intersection of M(L) over all Lagrangians L containing e.
```

There are fifteen such L for each nonzero e, and all 135 for e=0.

**Extension criterion.** The colors allowed at [z+e] by all even neighbors
are exactly {15} union I(e). The given even coloring extends to an
eighteen-coloring of the retained graph if and only if the graph on the
63 nonzero vectors e in E, with adjacency e dot f=1, has a proper list
coloring from these lists. Assign [z] color 15. Any resulting retained
coloring then lifts through the retraction to the original full graph.

**Proof.** An even totally isotropic U is adjacent to [z+e] precisely when
U is contained in e-perp, because z is orthogonal to E. If e belongs to
a Lagrangian L, every U in S(L) satisfies this condition. Conversely,
if U is contained in e-perp, then U+span(e) is totally isotropic: both
summands are isotropic and perpendicular. Extend it to a Lagrangian L
in the nondegenerate six-dimensional symplectic space E. Thus the even
neighbors of [z+e] are exactly the union of S(L) over L containing e.
Taking the complement of the union of their color sets in P gives I(e).
Color 15 is always allowed by even neighbors.

For distinct e,f in E,

```text
(z+e) dot (z+f) = 1 + e dot f.
```

Therefore odd-line adjacency is exactly e dot f=1. The characteristic
line [z] corresponds to e=0 and has no odd neighbors. These observations
account for all even-even, even-odd and odd-odd edges, proving both
directions of the criterion.

## Constraints on the omitted pairs

Let Z={e in E minus {0}: I(e) is empty}. In any extension all these odd
lines must have color 15. Their vectors must therefore be pairwise
symplectically orthogonal. Their span is totally isotropic and has
dimension at most three. Consequently

```text
|Z| <= 7,
at least 56 of the 63 nonzero e have a nonempty I(e).
```

For every nonempty clique C in the odd nonorthogonality graph, its
vertices need |C| distinct colors. Their union of lists is {15} union
the union of I(e), e in C. Hence another necessary condition is

```text
|union of I(e), e in C| >= |C|-1.
```

Applying this to every subclique gives the Hall conditions for coloring
each clique. These local conditions are necessary; the extension
criterion still requires a proper list coloring on the entire odd graph.

In the 63-vertex graph on E minus {0}, the maximal cliques have sizes
3,5,7 and vector sum zero. To see this,
the Gram matrix of a k-clique has zero diagonal and ones off the diagonal.
For even k it is nonsingular; for odd k its kernel is the span of the
all-ones vector. A linearly dependent clique must therefore have odd size and sum
zero; such a clique cannot be extended, since a common neighbor would
pair to one with that zero sum. A linearly independent clique of size below six
has a common neighbor by nondegeneracy and independent linear constraints.
A linearly independent six-clique extends by the sum of its six vectors. The
Gram rank bounds every clique by seven. Thus the maximal cliques are
exactly the linearly dependent odd cliques described above. The isolated
characteristic line is outside this 63-vertex domain; among all 64 odd
lines it contributes an additional maximal singleton.

The exact enumeration gives 336 maximal triangles, 2,016 maximal
five-cliques and 288 maximal seven-cliques. In particular, for every one
of the latter, the omitted-pair intersections must collectively supply
at least six non-15 colors. There are 26,895 nonempty subcliques in total.

If S(T), T=span(3,12,48), is normalized to colors 0,...,14, then
M(T)={16,17}. For each nonzero t in T, I(t) is contained in this pair,
so the corresponding special line has a list contained in {15,16,17}.
It is not justified to preassign these lines color 15: the previous
forcing theorem was for seventeen colors.

## A separate sufficient construction

A separate sufficient construction is to color only
lines and totally isotropic planes with seventeen colors, then give
every isotropic three-space the eighteenth color. Distinct Lagrangians
are nonadjacent: U perpendicular to V implies V is contained in
U-perp within E, which equals U. Thus the 135 three-spaces are independent.
The remaining graph has 442 vertices and 16,569 edges. A proper
seventeen-coloring of it would suffice for a full eighteen-coloring
after the retraction. This is a sufficient construction, not a restriction
that every eighteen-coloring must satisfy. No such witness is supplied.

The later [line-capacity theorem](dimension-seven-line-capacity.md)
rules out this separate construction: its line graph alone needs
eighteen colors. The general conditional extension theorem above,
which allows the three-spaces to share colors with other vertices,
is unaffected by that obstruction.

## Verification and reproduction

The standard-library [checker](../develop/check_eighteen_color_palettes.py)
constructs all 513 even vertices and 135 Lagrangians from vector sets.
Its [report](../results/dimension-7-eighteen-color-palettes.json) checks
all 8,640 vector/Lagrangian memberships and all 32,832 even/odd neighbor
memberships. For every nonzero e, its fifteen incident Lagrangian cliques
cover exactly its 121 even neighbors. The odd graph has 63 vertices,
1,008 edges and degree 32; all its cliques are enumerated. The checker
also verifies all 9,045 pairs of distinct three-spaces and all 97,461
pairs of the proposed 442-vertex construction. Removing an incident
Lagrangian and reversing the odd-adjacency parity are rejected controls.

```sh
python3 develop/check_eighteen_color_palettes.py --report /tmp/dimension-7-eighteen-color-palettes.json
```

This is a written extension theorem with exact finite geometry checks,
without a supplied even coloring or odd list coloring. It adds necessary
constraints and a concrete sufficient upper-bound route; the full
chromatic number remains open with lower bound eighteen. No solver or
Lean run is part of this step. The submitted manuscript remains at
28e27a8, and the original dimension-six formal theorem retains its three
standard and four native-evaluation axioms.
