# Forced colors and a smaller dimension-seven instance

**Subsequent result:** the [written obstruction](dimension-seven-obstruction.md)
rules out sixteen colors. These reductions and forced assignments
remain valid for that target. The [seventeen-color problem](nonradical-line-retraction.md)
has different lists and does not reuse these singleton assignments.

Let O_7* have all nonzero subspaces of F_2^7 as vertices, with distinct
vertices adjacent when they are orthogonal for the standard dot product.
Put T=span(3,12,48) and e=64 in binary coordinates. Fix distinct colors
0 through 14 on the fifteen nonzero subspaces of T, and color 15 on
the line span(e). These sixteen vertices form the known maximum clique.

**Proposition.** Every sixteen-coloring with this fixed clique assigns
color 15 to every nonzero subspace U of T-perp that is not contained in T.
For a vertex U outside T-perp and outside the fixed clique, propagating
these forced colors leaves precisely the following list:

```text
{colors of W<=T, W nonzero, W not<=U-perp}
  union {15 if e belongs to U+T}.
```

The resulting instance on dimensions one through three has 14,540
uncolored vertices and 928,571 edges. Coloring this list instance is
equivalent to coloring O_7* with sixteen colors. The reduction supplies
neither a coloring nor a proof that sixteen colors are impossible.

## The forced class

The restriction of the dot form to T is zero, and e is orthogonal to T
with e dot e=1. Thus T-perp=T+span(e), a direct sum. A subspace
U<=T-perp is adjacent to every nonzero subspace of T unless it is one
of those fixed vertices itself. If U is not contained in T, all fifteen
colors of T are forbidden. Its only remaining color is 15. Such a U
contains a vector e+t with t in T, so it is not orthogonal to span(e).

These forced vertices are mutually nonadjacent: any two contain vectors
e+t and e+t', whose dot product is 1. Therefore the common forced color
creates no monochromatic edge within the class.

For a forced subspace of dimension d, its intersection with T has
dimension d-1. After choosing that intersection, there are 2^(4-d)
ways to lift e modulo it. The counts in dimensions one through four
are respectively 8,28,14,1. The fixed line span(e) accounts for one of
the eight lines. Hence the low-dimensional uncolored instance has
exactly 7+28+14=49 singleton lists, all with color 15. Propagation
introduces no further singleton lists. Indeed, if U is not contained
in T-perp, then dim(T intersect U-perp)<=2. At most N(2)=4 of the
fifteen T-colors are forbidden, leaving at least eleven. Propagating
color 15 removes none of those colors, so no other singleton can arise.

## The remaining color 15 condition

Every vector of T-perp outside T has the form e+t. The lines they span
already have forced color 15, so they impose all restrictions that the
higher-dimensional forced vertices could impose. A remaining vertex U
can retain color 15 exactly when

```text
U-perp intersect T-perp <= e-perp.
```

Indeed, a failure of this containment supplies an odd vector e+t
orthogonal to U and hence an adjacent forced line. Conversely, an
adjacent forced subspace supplies such a line inside it. By
nondegeneracy and the orthogonal-complement identities, the containment
is equivalent to

```text
e belongs to (U-perp intersect T-perp)-perp = U+T.
```

The other fifteen color restrictions are exactly adjacency to the fixed
nonzero subspaces of T. This proves the stated list formula.

## Equivalence and measured size

The earlier [degree reduction](dimension-seven.md) deletes every vertex
of dimension at least four: its degree is at most N(7-d)<=N(3)=15,
below the sixteen available colors. With fixed clique neighbors
removed, each lost color is accompanied by the corresponding removed
neighbor, so the strict degree-versus-list inequality still holds.
These vertices can be restored greedily after coloring the
low-dimensional instance.

Next assign and remove the 49 singleton vertices, deleting their color
from their remaining neighbors' lists. This is an equivalence: every
extension must use their forced colors, and the reduced lists exclude
all conflicts when the vertices are restored. None of the remaining
vertices satisfies the reversible degree deletion condition. The
remaining graph is connected.

| Quantity | Before propagation | After propagation |
| --- | ---: | ---: |
| Uncolored vertices | 14,589 | 14,540 |
| Edges among uncolored vertices | 953,057 | 928,571 |
| Variables in the pairwise encoding | 214,355 | 206,676 |
| Clauses in the pairwise encoding | 12,984,679 | 12,306,141 |

Propagation removes 7,630 color choices from neighbors, in addition to
the 49 assigned singleton variables. The remaining dimension counts
are 112 lines, 2,632 planes and 11,796 three-dimensional subspaces.
Their lists have size 11,12,14 or 15. The six-dimensional control
reproduces the established core of 2,080 vertices, 39,400 edges,
28,600 variables and 627,510 clauses.

The [checker](../develop/propagate_dimension_seven.py) constructs the
original low-dimensional graph by exact orthogonal-complement
enumeration. It verifies the forced class and the geometric list
formula for every remaining vertex, and prints the JSON result archived in
[the exact report](../results/dimension-7-propagation.json).

```sh
python3 develop/propagate_dimension_seven.py --dimension 6
python3 develop/propagate_dimension_seven.py --dimension 7
```

To save a regenerated seven-dimensional report rather than printing it:

```sh
python3 develop/propagate_dimension_seven.py --dimension 7 > results/dimension-7-propagation.json
```

The reduction supplies an explicit description of the remaining lists.
The subsequent written obstruction now settles their uncolorability
for sixteen colors. No SAT or Lean run is part of this reduction, and
the exact dimension-seven chromatic number remains open.
