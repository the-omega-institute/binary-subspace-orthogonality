# Eight colors and an exact Boolean test for the all14 odd extension

Current branch status: the subsequent
[line-capacity proof](dimension-seven-line-capacity.md) excludes all14
and the entire auxiliary seventeen-color route. This note records
the preceding conditional odd-extension analysis at
[716ab70](https://github.com/the-omega-institute/binary-subspace-orthogonality/commit/716ab709f022c11ec2d4c3def79b369a07aab710).

The 56-vertex odd graph left by the all14 branch has independence number
seven and chromatic number eight. Given a proper sixteen-coloring of
the 378 even vertices, its exact odd extension can be decided by a
2-SAT formula with at most 56 variables. This supplies restrictions
and a diagnostic for the conditional extension problem. It does not
supply the even coloring or solve the 434-vertex branch.

Use the notation of the [branch reduction](all14-special-line-branch.md):
z=127, T=span(3,12,48), E=z-perp, and vertices e in E outside T representing
the odd lines [z+e]. Two such vertices are adjacent precisely when
e dot f=1. The graph has 56 vertices and 784 edges, of degree 28.

## The independence bound

An independent set consists of pairwise orthogonal vectors of E.
Since E is alternating, each vector is also orthogonal to itself.
Their span W is therefore totally isotropic. Nondegeneracy gives
dim(W-perp)=6-dim(W), and W subset W-perp implies dim(W)<=3.
Consequently an independent set has at most 2^3-1=7 points.
Every proper coloring of all 56 points needs at least eight colors.

## An explicit eight-coloring

The ordered bases

```text
T basis = (3,12,48),       D basis = (65,71,95)
```

give symplectic coordinates E=T direct-sum D with Gram matrix
[0 I; I 0]. Identify each coordinate three-space with F_8 using the
ordered field basis (1,a,a^2), where a^3+a+1=0. For b in F_8 define
the symmetric matrix

```text
M_b[i,j] = Tr(b * a^i * a^j),       i,j=0,1,2,
Tr(x) = x + x^2 + x^4.
```

For b nonzero the trace pairing (u,v) -> Tr(buv) is nondegenerate:
if u is nonzero, take v=(bu)^(-1), since Tr(1)=1. Hence M_b is
invertible. Linearity gives M_b+M_c=M_(b+c), which is invertible
whenever b differs from c.

Define L_b={(M_b y,y): y in F_2^3}. Symmetry of M_b makes L_b
totally isotropic: the pairing of (M_b y,y) and (M_b w,w) is
y^t(M_b^t+M_b)w=0. Each L_b meets T only at zero. Distinct L_b,L_c
also meet only at zero, because (M_b+M_c)y=0 forces y=0.
The eight sets L_b minus {0}, each with seven points, thus partition
E outside T and are independent color classes. Together with T these
nine Lagrangians form a symplectic spread. This proves

```text
alpha(odd graph) = 7,       chi(odd graph) = 8.
```

The [checker](../develop/check_all14_odd_extension.py) constructs the
field arithmetic without geometry helpers, verifies the dual Gram
matrix, all eight trace matrices and their differences, and checks
the resulting certificate against every one of the 1540 original
odd-line pairs. The [original report](https://github.com/the-omega-institute/binary-subspace-orthogonality/blob/716ab709f022c11ec2d4c3def79b369a07aab710/results/dimension-7-all14-odd-extension.json)
includes all 56 color assignments. This is an odd-subgraph witness.

## Capacity conditions on the exact lists

Now fix one common proper sixteen-coloring of the 378 even vertices.
Every Lagrangian proper-subspace fourteen-clique omits exactly two
labels M(L). The exact list of an outside point is

```text
I(e) = intersection of M(L) over the fifteen Lagrangians containing e.
```

These are the branch lists, without a fallback label. In particular
|I(e)|<=2. If they extend to a proper odd coloring, then for any subset
R of odd points, each label in their union covers at most seven points.
Thus

```text
|union of I(e), e in R| >= ceil(|R|/7).
```

Taking all 56 points requires at least eight labels in the global
union. This follows from the independent-set capacity rather than
clique size. No claim is made that these inequalities alone suffice.
The exhibited eight-coloring need not respect lists from an even
coloring.

## An exact 2-SAT diagnostic for a fixed even coloring

Reject an empty I(e) immediately. Use one Boolean variable X_e per
point, at most 56 in total. If I(e)={a,b} with a<b, select a when
X_e is false and b when it is true. If I(e)={a}, force X_e true and
select a. Write P_(e,c) for the signed literal expressing selection
of c at e. For every odd edge ef and every c in I(e) intersect I(f), add

```text
not P_(e,c) OR not P_(f,c).
```

Singleton points contribute a unit clause. There are at most two
clauses per edge and at most 56 unit clauses: 1624 clauses in total.
An assignment satisfying the formula selects one allowed label at
each vertex and forbids every monochromatic edge. Conversely any
proper coloring from these lists determines a satisfying assignment.
This proves exact equivalence, including singleton lists and empty
lists, with no native SAT solver assumption.

The implication graph replaces (p OR q) by -p -> q and -q -> p;
a unit (p) gives -p -> p. The formula is satisfiable precisely when
no X_e and -X_e lie in the same strongly connected component.
For necessity, paths express implications, so mutual paths between
a literal and its negation forbid both truth choices. For sufficiency,
collapse components to an acyclic graph and order them topologically.
Choose a literal true when its component comes later than that of
its negation. If p -> q and p were true but q false, the companion
edge -q -> -p and the topological ordering would give
component(-p)<component(p)<=component(q)<component(-q)<=component(-p),
a contradiction. This constructs a satisfying assignment.

The checker supplies a reusable clause encoder and SCC diagnostic.
It exhausts all 1728 three-vertex instances with singleton/two-label
lists from three labels and all eight simple graphs, comparing each
of 13824 Boolean assignments to direct proper list coloring and
checking SCC feasibility against exhaustion. Empty and oversized
list controls are separate. These synthetic instances validate the
encoding and diagnostic; they are not asserted realizable by a common
proper even coloring. No such coloring is supplied here, and no
actual 56-point branch list instance has been solved.

The next structural question is whether the simultaneous omitted
pairs coming from a proper even coloring force or prevent a
contradictory implication cycle, even after the capacity and clique
conditions pass. Arbitrary independently chosen M(L) do not answer
this question.

```sh
python3 develop/check_all14_odd_extension.py --report /tmp/all14-odd-extension.json
```

At the recorded revision, all14 and the other 31 orbits were open.
The subsequent written line obstruction now excludes all of them.
The full n=7 chromatic number remains open with lower bound eighteen.
The original finite report retains its source/note hashes at 716ab70;
checkout that revision to reproduce the exact report bytes.
No native solver or Lean was run for this result.
The submitted manuscript at 28e27a8 is unchanged; the historical
dimension-six Lean theorem retains three standard and four
native-evaluation axioms.
