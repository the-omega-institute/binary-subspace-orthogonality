# Saturating color sixteen in the full seven-line pattern

This reduction concerns only mask 127 among the ten
[seven-line symmetry representatives](seven-line-symmetry.md): all seven
lines span(z+t), with nonzero t in T, receive color sixteen.
It does not discard the other nine patterns or give a full-graph coloring.

Keep T=span(3,12,48), z=127, and the characteristic-clique normalization.
Write E=z-perp, the six-dimensional symplectic even-parity hyperplane.
Let A be the set of totally isotropic three-spaces U in E transverse
to T, meaning U intersect T={0}.

**Proposition.** In any proper normalized seventeen-coloring with the
full seven-line pattern, every uncolored retained vertex that may still receive
color sixteen is in A. The set A together with the seven fixed odd
lines is independent. Consequently all vertices of A may be recolored
sixteen, preserving a coloring, and removed from the uncolored problem.

**Proof.** A retained even vertex U is totally isotropic or an even
line. Its adjacency to span(z+t) is equivalent to t in U-perp. For
dim U at most two, the linear map from T to the dual of U has a
nonzero kernel, so U has a neighbor among the seven color-sixteen lines.
For an isotropic three-space, U is Lagrangian in E and U-perp intersect E
equals U. It has no such neighbor exactly when U intersect T={0}.

An odd line span(v) outside the seven special lines and span(z) has
a nonzero functional t maps to t dot v on T. If that functional were
zero, v would belong to T-perp=T direct-sum span(z), making it one
of the already fixed eight odd lines. A nonzero functional has four
nonzero T-vectors with t dot v=1. Since z dot v=1, the odd line is
orthogonal to all four corresponding span(z+t), so cannot use sixteen.
Thus precisely the transverse Lagrangian three-spaces remain eligible.

Distinct Lagrangians U,V in E cannot be orthogonal: V would lie in
U-perp intersect E=U, forcing equality. Each transverse U has no edge
to any special line by the first argument. The seven special lines
are themselves pairwise nonadjacent. Their union with A is therefore
independent. Every remaining vertex outside this union already forbids
sixteen, so recoloring all of A sixteen introduces no monochromatic
edge. The converse is immediate by restriction. This proves equivalence
within this branch only.

There are 64 members of A. Relative to T and its displayed symplectic
dual, each transverse Lagrangian is the graph of a linear map from
the dual to T. Its isotropy condition is that the three-by-three matrix
is symmetric. The six independent binary entries give 2^6=64 spaces.
Together with the seven odd lines, they form a 71-vertex color class.

After these assignments and the sixteen-clique normalization, the
uncolored instance has

```text
490 vertices = 112 lines + 308 isotropic planes + 70 isotropic triples,
15,386 edges, 6,286 variables and 196,350 pairwise-encoding clauses.
```

Its list-size histogram is {11:154,12:56,14:280}. Color sixteen is
absent throughout this residual problem. Colors zero through fourteen
are allowed exactly when their fixed T-subspace is not contained in
T intersect U-perp; color fifteen is allowed exactly at odd lines.

The independent standard-library [checker](../develop/check_full_seven_line_branch.py)
tests retained adjacency directly, confirms the exact eligible set and
independence, and checks every one of the 490 residual lists against
the geometric formula. It shares the canonical RREF basis enumerator
and span helper, and does not import the SAT builder.
The [report](../results/dimension-7-full-seven-line-branch.json) records
counts and source hashes. No branch DIMACS file or solver run was made.
The full n=7 chromatic number remains open with lower bound seventeen.

```sh
python3 develop/check_full_seven_line_branch.py --report /tmp/dimension-7-full-seven-line-branch.json
```
