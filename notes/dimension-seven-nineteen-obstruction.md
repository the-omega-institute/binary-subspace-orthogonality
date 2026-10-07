# The dimension-seven graph requires at least nineteen colors

**Theorem.** The line graph Gamma_7, and hence the orthogonality graph
on all nonzero subspaces of F_2^7, has chromatic number at least nineteen.
Their exact chromatic numbers remain open here. No nineteen-color
witness is supplied.

The proof rules out both necessary forms of an eighteen-color line
coloring derived in the [line-capacity analysis](dimension-seven-line-capacity.md).
One form fails a quadratic parity identity; the other fails a
Lagrangian completion and clique-capacity argument. These are written
obstructions supported by exact finite checks, without SAT or Lean.

## The two possible eighteen-color structures

Put z=127 and E=z-perp, a nondegenerate alternating six-space. Distinct
line generators are adjacent precisely when their dot product is zero.
The preceding capacity lemma gives at most seven vectors in an independent
line set avoiding z. If m even and o odd vectors are selected with o>0,
then o<=2^floor((6-m)/2). An all-even class has at most seven vectors;
an all-odd class of size eight is z+L for a Lagrangian L in E.

Thus an eighteen-coloring of all 127 lines would have one eight-odd-line
class z+T, after a symplectic normalization fixing z, and seventeen
seven-line classes. Every remaining class is either seven even lines,
six even and one odd line, or seven odd lines. If their numbers are
A,B,C, counting the 63 even and 56 remaining odd lines gives

```text
7A+6B=63,       B+7C=56,       A+B+C=17.
```

The only nonnegative integer solutions are (A,B,C)=(9,0,8) and (3,7,7).
Each seven-odd-line class has form {z+e: e in L minus {0}} for a
Lagrangian L: its seven nonzero e are pairwise orthogonal, span an
isotropic space of dimension at most three, and fill its nonzero points.
These Lagrangians are disjoint outside zero, including T, because the
line color classes are disjoint.

## Nine even heptads fail quadratic parity

Let q be any quadratic refinement of the symplectic form on E. In
coordinates with Gram matrix [0 I; I 0], take

```text
q(x,y)=x dot y,       x,y in F_2^3.
```

Its polarization is q(u+v)=q(u)+q(v)+u dot v. The number of vectors
with q=1 is 7*4=28: x=0 contributes none, and for each of the seven
nonzero x, exactly four y satisfy x dot y=1. In particular the sum
of q over all 63 nonzero points of E is zero in F_2.

An even heptad H={u_1,...,u_7} has pairwise products one. Its Gram
matrix J_7+I_7 has rank six and kernel spanned by the all-ones vector.
Since E has dimension six, the seven vectors have a nonzero linear
relation; pairing it with all u_i forces all coefficients equal.
Therefore their sum is zero. Polarization then gives

```text
0 = q(sum u_i) = sum q(u_i) + sum_{i<j} u_i dot u_j
              = sum q(u_i) + 21,
```

so each heptad has odd q-sum. Nine disjoint heptads partitioning the
63 even points would have total q-sum nine, or one in F_2, contradicting
the even count 28. This excludes (9,0,8).

## Eight disjoint Lagrangians complete uniquely

Suppose L_1,...,L_8 are Lagrangian three-spaces in E with pairwise
intersection {0}. Their nonzero points cover 56 points, leaving seven
holes R. For any nonzero e, the hyperplane e-perp has 31 nonzero points.
Its intersection with a Lagrangian has seven nonzero points if e is
in that Lagrangian, and three otherwise: L=L-perp, and a nonzero
functional on L has a two-dimensional kernel.

If e is covered, it is in exactly one L_i. The hyperplane contains
7+7*3=28 covered points and therefore three holes. If e is a hole,
the hyperplane contains 8*3=24 covered points and all seven holes.
In particular every hole is orthogonal to every hole. Their span is
isotropic of dimension at most three; seven distinct nonzero points
force dimension three. Hence

```text
R = M minus {0}
```

for one Lagrangian M, uniquely determined by its nonzero points.
It is disjoint from each L_i outside zero and completes them to a
nine-member symplectic spread. This argument applies to every such
eight-member partial spread, not only an explicit example.

## The mixed type has too few labels for the holes

In type (3,7,7), the eight-odd-line class gives T, and the seven
seven-odd-line classes give seven further disjoint Lagrangians.
The completion theorem makes the remaining seven even points
M minus {0}. They are exactly the e of the seven odd lines z+e
in the mixed classes, because those are the only odd lines not
covered by the eight pure odd classes.

Every even point u in M minus {0} is orthogonal to every such odd
line z+e: u dot z=0 and u dot e=0. It cannot use any of the seven
mixed labels. The eight pure odd labels have no even vertices by
the saturated class structure. Only the three all-even labels remain.
But M minus {0} consists of seven pairwise adjacent even lines,
requiring seven distinct labels. Three cannot suffice. This excludes
(3,7,7).

Both possible eighteen-color structures are impossible. The prior
line lower bound eighteen therefore improves to

```text
chi(Gamma_7) >= 19,       chi(O_7*) >= 19.
```

This also excludes eighteen colors on the 442-vertex auxiliary graph.
Assigning all 135 isotropic three-spaces a fresh nineteenth color
after coloring that graph with eighteen colors cannot work. If a
nineteen-coloring of the full graph exists, all nineteen labels must
already be used on the lines, and three-spaces must share those labels.
No upper bound or exact value follows from this obstruction.

## Verification and scope

The [coordinate checker](../develop/check_dimension_seven_nineteen_obstruction.py)
verifies the quadratic polarization on all 4096 pairs of points in E,
the 28/36 quadratic counts, every one of the 288 even heptads and
their zero sums/odd quadratic sums, and all 2016 even six-cliques
with their unique heptad completions. It independently constructs
all 135 Lagrangians and checks all 8505 point/hyperplane/Lagrangian
intersection counts used in the universal completion proof.

As concrete completion controls, an explicit trace-field spread is
verified and each of its nine members is omitted in turn. All nine
resulting eight-member partial spreads recover the missing member
from the seven holes, including every hyperplane's 24/28 covered
and 7/3 hole counts and all 49 even-hole/odd-hole adjacency tests.
These nine examples do not enumerate every partial spread; the
universal conclusion rests on the written counting proof above.
The [finite certificate](../results/dimension-7-nineteen-obstruction.json)
records exactly this scope and binds the checker and note.

```sh
python3 develop/check_dimension_seven_nineteen_obstruction.py --report /tmp/dimension-7-nineteen-obstruction.json
```

No native SAT solve, DRAT check, Lean run or nineteen-color witness
is involved. Historical eighteen-bound and unknown-search records
remain snapshots at their original revisions. The submitted manuscript
at 28e27a8 is unchanged; manuscript integration is a separate coauthor
decision. The historical dimension-six Lean theorem retains three
standard and four native-evaluation axioms.
