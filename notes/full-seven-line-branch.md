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
independent. Every other uncolored retained vertex already forbids
sixteen, so recoloring all of A sixteen introduces no monochromatic
edge. Restricting this coloring gives a proper residual list coloring.
Conversely, extend any proper residual list coloring by the fixed
sixteen-clique and the independent 71-vertex color-sixteen class.
The lists exclude every conflict with a fixed neighbor, and residual
properness handles all remaining edges. This proves equivalence within
this branch only. A full-graph coloring is obtained afterward by the
separate nonradical retraction; the recoloring argument concerns retained
vertices.

There are 64 members of A. Take F=span(65,71,95), with generators
(f1,f2,f3)=(65,71,95) and (t1,t2,t3)=(3,12,48). Direct dot products
give ti dot fj=delta_ij and fi dot fj=0; thus E=T direct-sum F.
Each transverse three-space is uniquely the graph of a map F to T,
with generators uj=fj+sum_i Mij ti. Their pairings are
uj dot uk=Mjk+Mkj, so isotropy is equivalent to symmetry of M.
Its diagonal is unrestricted in characteristic two. The three diagonal
and three off-diagonal binary entries give 2^6=64 spaces.
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
counts, all 64 symmetric-matrix graphs, and source hashes.

The deterministic [builder](../develop/encode_full_seven_line_branch.py)
emits the 6,286-variable, 196,350-clause DIMACS instance. Variables are
ordered by canonical RREF vertex index and then increasing color. Each
vertex receives one positive choice clause and all pairwise exclusion
clauses; each residual edge receives an exclusion clause per shared color.
The independent [encoding auditor](../develop/check_full_seven_line_encoding.py)
reconstructs residual membership and lists geometrically and tests adjacency
on full spans. It checks every clause exactly once without importing the
builder. Missing clauses, duplicates, a wrong branch marker, and out-of-range
variables are rejected by negative controls. The
[encoding report](../results/dimension-7-full-seven-line-branch-encoding.json)
and [audit report](../results/dimension-7-full-seven-line-branch-encoding-check.json)
bind the emitted bytes and sources. The
[bounded search](../develop/search_full_seven_line_branch.py) binds the
same audited CNF and records its outcome in a
[separate report](../results/dimension-7-full-seven-line-branch-search.json).
SAT candidates require an independent original-graph coloring check after
extension and retraction. An UNSAT report requires a checked proof and can
exclude only this branch. The other nine patterns remain required.
The full n=7 chromatic number remains open with lower bound seventeen.

```sh
python3 develop/check_full_seven_line_branch.py --report /tmp/dimension-7-full-seven-line-branch.json
python3 develop/encode_full_seven_line_branch.py --output-dir /tmp/full-seven-line-branch
python3 develop/check_full_seven_line_encoding.py /tmp/full-seven-line-branch/dimension-7-full-seven-line-branch.cnf --controls --report /tmp/full-seven-line-branch/audit.json
# Use an interpreter with python-sat for the bounded search:
python3 develop/search_full_seven_line_branch.py /tmp/full-seven-line-branch/dimension-7-full-seven-line-branch.cnf --seconds 120 --output-dir /tmp/full-seven-line-branch
```
