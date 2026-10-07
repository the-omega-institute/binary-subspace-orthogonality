# The all14 branch: a dominating class and exact sixteen-color reduction

The ternary orbit with all seven special lines colored 14 is equivalent
to sixteen-colorability of a specific 434-vertex induced graph. Its
odd-line extension has an exact omitted-pair criterion with no fallback
color. These reductions isolate one of the 32 retained orbits; they do
not solve this branch or exclude the other 31.

Let G be the auxiliary graph on all 127 lines and 315 totally isotropic
planes in F_2^7. Put T=span(3,12,48), z=127 and

```text
S = {[z+t]: t in T}.
```

The normalized fixed clique consists of fourteen nonzero proper
T-subspaces colored 0,...,13 and [z] colored 14. The all14 branch
therefore assigns color 14 to all eight vertices of S.

## An independent dominating color class

For any s,t in T, (z+s) dot (z+t)=1. Thus S is independent.
Every even line and totally isotropic plane is adjacent to [z], since
each of its vectors is orthogonal to z. For an odd line [u] outside S,
the linear functional t -> u dot t on T is nonzero: otherwise
u belongs to T-perp=T direct-sum span(z), and oddness gives u=z+t,
contrary to [u] outside S. Its value is one on exactly four T-vectors,
and each corresponding [z+t] is adjacent to [u].

Consequently S dominates every vertex outside it. In the all14 branch
it is exactly the color-14 class, and H=G-S uses the other sixteen
labels C={0,...,13,15,16}. Conversely, any sixteen-coloring of H can
be normalized on its fourteen-clique and extended by color 14 on S.
Therefore

```text
the normalized all14 branch is colorable <=> chi(H) <= 16.
```

The full-span finite check gives 434 vertices and 15225 edges in H.
The removed characteristic line has degree 378; each of the seven
other removed lines has degree 138, removing 1344 edges in total.
H has 378 even vertices and 56 odd lines.

## Exact lists for the odd-line extension

Assume a proper coloring of the 378 even vertices with the sixteen
labels C. Each of the 135 Lagrangian three-spaces L defines a clique
of its fourteen nonzero proper subspaces, all present among these even
vertices. Write M(L) for the two labels omitted by that clique.

The space E=z-perp is nondegenerate alternating of dimension six:
z dot z=1, and every vector of E has even weight. An odd line outside S
has the unique form [z+e] with e in E outside T. Its even neighbors are exactly the union of these
fourteen-cliques over the fifteen Lagrangians containing e.

To prove coverage, an even neighbor U satisfies U subset e-perp.
Then U+span(e) is totally isotropic and has dimension at most three,
so it extends to a Lagrangian L containing both U and e. Conversely,
if e belongs to L, every vector of L is orthogonal to e, and every
proper subspace of L is adjacent to [z+e]. Therefore its exact list is

```text
I(e) = intersection of M(L) over all L containing e.
```

There is no fallback color: label 14 is already forbidden by S.
The even coloring extends precisely when the 56 odd vertices admit
a proper coloring from these lists, with adjacent e,f defined by
e dot f=1. This odd graph is regular of degree 28 and has 784 edges.
In particular every I(e) must be nonempty, and for each odd clique Q,
the union of I(e), e in Q, must have at least |Q| labels. These are
necessary conditions; nonempty lists and the clique inequalities alone
are not asserted sufficient for a global extension.

The [odd-extension analysis](all14-odd-extension.md) proves that this
56-vertex graph has independence number seven and chromatic number
eight, and gives an exact 2-SAT diagnostic for lists derived from a
fixed proper even coloring. Neither result supplies that even coloring.

The checker verifies all 135 fourteen-cliques, fifteen containing
Lagrangians at each outside point, and all 5936 even/odd neighbor
memberships, with exactly 106 even neighbors per odd line. This is
distinct from the earlier full eighteen-color criterion on 513 even
vertices, seventeen even labels, fifteen-vertex Lagrangian cliques
and a common fallback label. Those earlier hypotheses and counts
cannot be imported into this branch.

## A checked branch formula

Normalize the fourteen T-subspaces. For each of the other 420 vertices U,
put K_U=T intersect U-perp. Its list is

```text
{i in 0,...,13: the fixed T-subspace W_i is not contained in K_U}
union {15,16}.
```

The geometric formula is valid for even vertices and the remaining odd
lines. It gives 196 lists of size 12 and 224 of size 15, 5712 variables,
36876 vertex clauses and 157024 edge clauses: 193900 total. The residual
graph has 14126 edges.

The [standard-library checker](../develop/check_all14_branch.py) builds
these clauses using full-span dot products and the geometric kernel
formula. Independently, it simplifies the original base encoding by
assigning the seven special color-14 variables true and their extra
variables false, and assigning all remaining odd color-14 variables
false. These are 77 assigned variables, seven true. Renumbering the
remaining variables gives exactly the same complete set of 193900
clauses, with no empty clause or duplicate. This comparison uses the
old builder only after constructing the geometric branch formula;
the geometric construction shares the canonical RREF/span helpers.

The [finite certificate](../results/dimension-7-all14-branch.json)
binds the checker, helpers and emitted CNF. The CNF SHA256 is
`0b0c2b774da091c77f86ec80eac3f390333e9160d09ea1f4d2bf205ca0b63506`.
No solver or Lean was run on this branch. The 434-vertex sixteen-color
question remains open; the full n=7 chromatic number remains open
with written lower bound eighteen. A branch coloring would still need
the independent auxiliary check, fresh color on all 135 three-spaces,
and original full-graph lift verification before an upper bound.

```sh
python3 develop/check_all14_branch.py --report /tmp/all14-branch.json --output-cnf /tmp/all14-branch.cnf
```

The submitted manuscript remains at 28e27a8. The original dimension-six
formal theorem retains its three standard and four native-evaluation
axioms.
