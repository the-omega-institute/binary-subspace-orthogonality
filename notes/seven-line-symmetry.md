# Ten symmetry classes for the seven two-color lines

The characteristic-clique seventeen-color instance admits a complete
restriction to ten patterns on its seven two-color lines. This restriction
preserves seventeen-colorability; it does not give a coloring or determine
the full seven-dimensional chromatic number.

The subsequent [clique-triangle forcing theorem](forced-seven-line-color.md)
excludes every nonzero pattern: all seven special lines must receive
color fifteen. The ten-orbit classification below remains correct, but
mask0 is now the only candidate for a normalized seventeen-coloring.

Let T=span(3,12,48) and z=127. The fixed sixteen-clique consists of the
fifteen nonzero subspaces of T, assigned colors zero through fourteen,
and span(z), assigned color fifteen. Every other color list contains
color sixteen. The seven lines

```text
ell_t = span(z+t),   t in T minus {0},
```

have exactly the list {15,16}. Their generators, indexed by the nonzero
coordinates 1,...,7 in the ordered basis (3,12,48), are

```text
124, 115, 112, 79, 76, 67, 64.
```

These seven lines are pairwise nonadjacent: (z+t) dot (z+u)=1 for all
t,u in T. Constraints on their colors come from the rest of the graph.

## Extending every linear action on T

The even-parity hyperplane E=z-perp is nondegenerate alternating of
dimension six, since z dot z=1. An explicit symplectic basis is

```text
t_1=3,  t_2=12, t_3=48,
s_1=65, s_2=71, s_3=95.
```

All t_i dot t_j and s_i dot s_j vanish, and t_i dot s_j is one exactly
when i=j. Together with z these vectors form a basis of the full space.

For any A in GL(3,2), define g_A to act by A on the t coordinates, by
the inverse transpose of A on the s coordinates, and to fix z. The
pairing between the two triples is preserved because

```text
(A x) transpose (A inverse transpose y) = x transpose y.
```

All other pairings are preserved as well. Thus g_A is an orthogonal
linear automorphism. It preserves T and sends ell_t to ell_(A t).
It consequently preserves the full subspace graph and its retained
line/totally-isotropic graph.

The clique is preserved as a set, rather than pointwise. This is enough:
if f is a normalized coloring, choose the color permutation p_A defined
by p_A(f(W))=f(g_A W) on its sixteen clique vertices, and p_A(16)=16.
Then define f'(g_A U)=p_A(f(U)). This is a proper normalized coloring
again. In particular p_A fixes colors fifteen and sixteen, so it sends
the set of two-color lines using color sixteen to its A-image.
No interchange of colors fifteen and sixteen is assumed.

Therefore any subset of these seven lines can be replaced by a
representative of its GL(3,2) orbit without losing a coloring of the
whole retained graph. The existence of these lifts is essential;
an arbitrary permutation of the seven lines is not a justified symmetry.

## The ten patterns

Identify nonzero T-vectors with the seven points of the Fano plane.
The group is transitive on single points and pairs. A three-point set
is either a line, where its three vectors sum to zero, or a basis;
these give two orbits. Taking complements gives the four-, five-
and six-point cases. Empty and full subsets each give one orbit.

Encode the set using color sixteen by a seven-bit mask, with bit
index-1 corresponding to coordinate index in {1,...,7}. The minimum
mask in each orbit gives the following exact representatives.

| Size | Representative mask | Orbit size | Type |
| --- | ---: | ---: | --- |
| 0 | 0 | 1 | Empty |
| 1 | 1 | 7 | Point |
| 2 | 3 | 21 | Pair |
| 3 | 7 | 7 | Fano line |
| 3 | 11 | 28 | Basis triple |
| 4 | 15 | 28 | Complement of a basis triple |
| 4 | 30 | 7 | Complement of a Fano line |
| 5 | 31 | 21 | Complement of a pair |
| 6 | 63 | 7 | Complement of a point |
| 7 | 127 | 1 | Full |

The orbit sizes sum to 128. In particular, choosing only a pattern
by its number of color-sixteen lines would discard one of the two
three-point or four-point types and is unjustified.

## A checked CNF restriction

Let b_i mean that the line with coordinate index i receives color
sixteen. For each of the 118 nonrepresentative masks m, append the
seven-literal clause that is false only at m: use literal not b_i
when bit i-1 of m is one, and literal b_i otherwise.

The resulting CNF keeps all 7,814 variables and has

```text
244,442 original clauses + 118 symmetry clauses = 244,560 clauses.
```

All ten representative patterns remain available. The preceding group
and color-renormalization argument proves that this CNF is satisfiable
exactly when the original normalized seventeen-color instance is.
The extra clauses restrict seven existing Boolean variables; they do
not claim that every coloring already has a representative pattern.

The standard-library [checker](../develop/check_seven_line_symmetry.py)
enumerates all 168 invertible three-dimensional binary matrices and
their orthogonal lifts. It tests 2,752,512 vector-pair identities,
96,936 retained vertex images, 3,282,552 retained edge images, and
94,248 normalized palette images. It partitions all 128 masks,
checks every added clause on the entire seven-bit truth table, and
checks that each nonrepresentative violates exactly one added clause.
It also audits every base clause with the separate geometric auditor
and recovers the original base body byte for byte after reading back
the emitted symmetry CNF. The shared dependency is the canonical
RREF basis enumerator and span helper.

The [report](../results/dimension-7-seven-line-symmetry.json) records
every orbit and binds the checker, helper, base CNF and symmetry CNF
by SHA256. No solver or Lean was run in this step. The two previous
120-second unknown outcomes give no chromatic bound. The full n=7
chromatic number remains open with the written lower bound seventeen.

```sh
python3 develop/check_seven_line_symmetry.py --cnf /tmp/nikandish17-output/dimension-7-17-nonradical-characteristic.cnf --output-cnf /tmp/nikandish17-output/dimension-7-symmetry.cnf --report /tmp/dimension-7-seven-line-symmetry.json
```

## Review and bounded continuation

An independent review approved the orthogonal lift, normalized-color
action, ten orbits and satisfiability-preserving clause restriction.
It found a reporting defect in the initial replay check: text-mode
reading could normalize CRLF input while still reporting byte identity.
The current emitter and replay use raw bytes, preserve every original
clause record, restore the exact original header, and compare against
the original source bytes. Full-size LF, CRLF, CR and unterminated-final-line
fixtures pass independent raw-byte replay checks. The actual historical
LF symmetry CNF remains byte-identical; the defect concerned the claim
for other accepted input encodings.

One Glucose4 attempt on the audited 244,560-clause symmetry CNF used a
120-second interrupt setting and returned unknown after 122.068 seconds
of measured solve time. It recorded 1,707,571 conflicts and 2,793,953
decisions, without a SAT candidate or UNSAT result. The
[search report](../results/dimension-7-seven-line-symmetry-search.json)
binds the CNF, current symmetry checker/report, search runner and base
construction. This is the only solver attempt in this continuation;
the timeout gives no new chromatic bound.

```sh
/tmp/nikandish17-env/bin/python develop/search_seven_line_symmetry.py /tmp/nikandish17-output/dimension-7-symmetry.cnf --seconds 120 --output-dir /tmp/nikandish17-output
```

The [full-pattern branch proof](full-seven-line-branch.md) gives a further
conditional reduction only for mask 127. Its seven fixed odd lines and
64 transverse isotropic triples can all receive color sixteen, leaving
490 uncolored vertices. The other nine pattern branches remain required.
