# The seven special lines are forced to color fifteen

Fix T=span(3,12,48), z=127, and E=z-perp in F_2^7. Normalize a
proper seventeen-coloring by assigning colors zero through fourteen
to the fifteen nonzero subspaces of T, and color fifteen to span(z).
The seven special lines ell_t=span(z+t), for nonzero t in T, initially
have the list {15,16}. Retain all lines and totally isotropic subspaces,
as in the [nonradical retraction](nonradical-line-retraction.md).

**Theorem.** Every such normalized seventeen-coloring assigns color
fifteen to all seven special lines. Consequently mask0 is the only
possible [seven-line pattern](seven-line-symmetry.md).

**Proof.** Suppose ell_t has color sixteen for some nonzero t in T.
Choose d in T outside span(t). The restricted form on E is nondegenerate
alternating, and T is Lagrangian. Thus there is e in E with

```text
e dot t=0,    e dot d=1.
```

For example, the explicit symplectic complement F=span(65,71,95)
pairs perfectly with T, so these two independent linear conditions can
be solved in F. Put f=e+d. The nonzero functional x maps to e dot x
on T has a two-dimensional kernel containing t. Choose h in that
kernel outside span(t), and put

```text
A=span(t,h,e),    B=span(t,h,f).
```

Since e and f are outside T and both annihilate t and h, A and B are
totally isotropic three-spaces in E. Each has fifteen nonzero subspaces,
forming a fifteen-clique. Every vertex of either clique is adjacent to
span(z), colored fifteen, and ell_t, assumed colored sixteen. Thus each
clique must use all fifteen colors zero through fourteen.

The odd lines

```text
v=span(z+e),    w=span(z+f),    r=span(z+d)
```

are pairwise distinct. The first is orthogonal to every subspace of A,
the second to every subspace of B, and the third to every subspace of T.
Therefore each has color in {15,16}. But they form a triangle:

```text
(z+e) dot (z+f) = 1 + e dot d = 0,
(z+e) dot (z+d) = 1 + e dot d = 0,
(z+f) dot (z+d) = 1 + f dot d = 0.
```

A triangle cannot use two colors. This contradiction excludes color
sixteen at ell_t, proving the theorem for every nonzero t in T.

The proof concerns the retained graph directly and needs neither an
assumption about the other six special-line colors nor an orbit symmetry.
It excludes every nonzero seven-bit pattern, including mask127. The
earlier mask127 saturation and encoding audits remain valid conditional
reductions, and its recorded solver outcome remains unknown; the branch
is now excluded by this written graph argument, not a solver or DRAT proof.

## Explicit certificate and residual lists

For t=12, take d=3, e=65, f=66 and h=48. Then

```text
assumed color16 line: span(115),
A=span(12,48,65),    B=span(12,48,66),
triangle: span(62), span(61), span(124).
```

The three fifteen-cliques from T, A and B have common intersection
span(12,48), which has four nonzero subspaces. Their union has 37
vertices. Adding span(z), span(z+t), and the three triangle lines gives
a 42-vertex certificate for the conditional contradiction. The
standard-library [checker](../develop/check_forced_seven_lines.py)
constructs and verifies such a certificate for each of the seven t.
For each it checks all 861 pairs, including 425 edges, the three cliques,
their required fixed-neighbor adjacencies, and the triangle. Its clique
families are generated directly from vector sets, without the SAT builder.
Repeated triangle vertices and a nonisotropic alleged Lagrangian are
rejected by negative controls.

The fixed assignments now consist of the fifteen T-subspaces and the
independent eight-line color-fifteen class {span(z+t): t in T}.
No other vertex receives a fixed color. For any residual U, put
K_U=T intersect U-perp. The colors not excluded by the fixed assignments
are exactly

```text
{i in 0,...,14: the fixed T-subspace of color i is not contained in K_U}
union {16}.
```

Indeed an even retained U is already adjacent to span(z). For an odd
line span(z+e) outside the eight fixed lines, e is outside T, so its
functional on T is nonzero. Choosing t with e dot t=1 supplies a
color-fifteen neighbor span(z+t). Thus color fifteen is forbidden
everywhere in the residual graph, while color sixteen remains available.

The [exact report](../results/dimension-7-forced-seven-line-color.json)
checks every residual list both by fixed-neighbor exclusion and by
this formula. The equivalent seventeen-color list problem has

```text
554 vertices = 112 lines + 308 isotropic planes + 134 isotropic triples,
16,730 edges, 7,744 variables and 241,782 pairwise-encoding clauses,
list-size histogram {12:210, 15:280, 16:64}.
```

Any proper residual list coloring extends by the 23 fixed vertices;
the lists exclude every conflict with a fixed neighbor. It then lifts
to the original graph by the nonradical retraction. Conversely, any
normalized full-graph seventeen-coloring restricts to this list instance
by the theorem. Although the retained vertex count agrees with the old
sixteen-color problem, the lists differ: the extra color sixteen remains
available at every residual vertex. The known sixteen-color obstruction
therefore does not settle this new instance.

These are a written forcing proof, seven finite certificates and exact
list/count checks. No CNF, SAT solver or Lean run was part of this
forcing step. Subsequently the [mask0 CNF](zero-seven-line-branch.md)
was emitted and audited, and the [omitted-color proof](dimension-seven-eighteen-obstruction.md)
excluded seventeen-colorability without a solver. The current lower bound
is eighteen; the exact full n=7 chromatic number remains open. The original
n=6 formal theorem retains its three standard and four native-evaluation axioms.

```sh
python3 develop/check_forced_seven_lines.py --report /tmp/dimension-7-forced-seven-line-color.json
```
