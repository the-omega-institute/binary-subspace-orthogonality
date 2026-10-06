# A smaller induced graph with the same chromatic number

For the standard dot product on F_2^n, let O_n* have all nonzero
subspaces as vertices, with distinct vertices adjacent when they are
orthogonal. A subspace is totally isotropic when the dot product
vanishes on every pair of its vectors. Put

```text
H = {x : x dot x=0}.
```

Over F_2 this is the even-parity hyperplane.

**Theorem.** Let R_n be the induced subgraph whose vertices are all
lines, all two-dimensional subspaces contained in H, and all totally
isotropic subspaces of dimension at least three. There is a graph
retraction O_n* -> R_n. In particular,

```text
chi(O_n*) = chi(R_n).
```

For n=7, R_7 has 913 vertices: 127 lines, 651 planes and 135
three-dimensional totally isotropic subspaces. After fixing the known
sixteen-clique and assigning the seven remaining forced lines, the
equivalent uncolored list instance has 890 vertices. This is a
structural reduction; sixteen-colorability remains open.

## The retraction

Keep every vertex of R_n fixed. For any other vertex U, choose an
image r(U) contained in U as follows.

If U contains a vector v with v dot v=1, let r(U)=span(v). This is
a line with nonzero restricted dot form.

Otherwise U is contained in H. Since U is not retained, it is not
totally isotropic and has dimension at least three. There are
vectors v,w in U with v dot w=1. Both have self-product zero, so
they are independent and span a plane with Gram matrix

```text
[[0,1],[1,0]].
```

Let that plane be r(U). It lies in H and belongs to R_n. Thus every
moved vertex has a non-totally-isotropic image contained in itself.
This construction also explains why the retained planes are exactly
the planes in H: a plane outside H can be sent to one of its
nonisotropic lines, while a plane in H is either totally isotropic
or has the displayed nondegenerate alternating form.

Suppose U and V are adjacent. Containment gives r(U) perpendicular
to r(V). Their images are distinct. Indeed, if the common image
were W, it would satisfy W perpendicular to W. If either vertex
was moved, its image has nonzero restricted form, a contradiction.
If neither was moved, equality of images would give U=V, also a
contradiction. Hence r sends every edge to an edge, fixes R_n,
and is a graph retraction.

Restriction of a coloring gives chi(R_n)<=chi(O_n*). Conversely,
composing any proper coloring of R_n with r colors O_n* with
the same number of colors. This proves equality. No enumeration
or solver is needed for this argument.

## The seven-dimensional counts

For n=7, H is a six-dimensional nondegenerate alternating space:
its radical is H intersect span(127), which is zero because 127
has odd parity. A totally isotropic subspace has dimension at most
three. There are 127 lines in F_2^7 and

```text
[6 choose 2]_2 = (63*62)/(3*2) = 651
```

planes in H. The number of three-dimensional totally isotropic
subspaces of H is

```text
(63*30*12)/(7*6*4) = 135.
```

Here the numerator counts ordered independent orthogonal triples:
after choosing v, choose w from v-perp outside span(v), then choose
the third vector from span(v,w)-perp outside span(v,w). The
denominator is the number of ordered bases of a three-dimensional
binary space. Thus R_7 has 127+651+135=913 vertices.

Use the previous clique with T=span(3,12,48), e=64, colors zero
through fourteen on the nonzero subspaces of T, and color fifteen
on span(e). The [forced-color theorem](dimension-seven-propagation.md)
fixes color fifteen on every subspace of T-perp not contained in T.
Among the retained vertices, these are precisely the eight lines
span(e+t), t in T; one is already in the clique. The other forced
planes and three-dimensional subspaces contain odd vectors and
are mapped to these lines by the retraction.

After removing the sixteen fixed clique vertices and seven extra
forced lines, there remain 913-16-7=890 vertices: 112 lines,
644 planes and 134 totally isotropic three-dimensional subspaces.

## The sixteenth color disappears from the remaining lists

The previous list formula allows color fifteen at U exactly when
e belongs to U+T. Every retained plane or higher-dimensional
vertex is contained in H, as is T, whereas e is odd. Such a
vertex therefore cannot retain that color. For a remaining odd
line span(v), the same condition would imply v=e+t for some t in T,
which is one of the eight forced lines already removed. Even
lines also cannot satisfy the condition.

Consequently every remaining vertex has a list using only the
fifteen colors assigned to subspaces of T. Finding a coloring
of this 890-vertex list instance suffices for a sixteen-coloring
of the full graph. The original sixteen-clique then gives equality.
It does not follow that the list instance is colorable.

## Exact checks and the next question

The [checker](../develop/check_subspace_retraction.py) verifies every
vertex image in dimensions six and seven by exact containment and
tests the retraction against every edge between vertices of
dimensions one through three. It checks distinct images and their
orthogonality directly from basis-vector dot products. The written
containment argument covers edges incident to higher-dimensional
vertices; those edges are not enumerated in this check.

The retained six-dimensional graph has 233 vertices, and its
fixed-fifteen-clique list instance has 218 vertices. This is a
control of the new reduction, not a new proof or rerun of the
historical six-dimensional coloring certificate.

The [seven-dimensional report](../results/dimension-7-retraction.json)
and [six-dimensional control](../results/dimension-6-retraction.json)
bind the exact counts to the checker and construction source hashes.

```sh
python3 develop/check_subspace_retraction.py --dimension 6
python3 develop/check_subspace_retraction.py --dimension 7
```

The next concrete problem is this 890-vertex list instance. A
successful coloring must be lifted through the stated retraction
and verified on the original graph. No SAT or Lean result is
claimed here. The dimension-seven chromatic number remains open;
the original dimension-six formal theorem retains its four
native-evaluation axioms.
