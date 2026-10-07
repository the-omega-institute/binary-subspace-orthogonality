# Six Lagrangians complete uniquely; characteristic size three is impossible

**Completion lemma.** Six pairwise disjoint Lagrangian three-spaces
in the six-dimensional binary symplectic space leave twenty-one
nonzero points. These are the disjoint union of the nonzero points
of three Lagrangians, uniquely determined by the holes.

This is a finite theorem with a written symplectic transitivity
reduction and two complete, independent enumerations below. It was
not assumed in the preceding two-six analysis and is not claimed
as a purely incidence-theoretic proof or a Lean theorem.

**Coloring theorem.** In any nineteen-coloring of Gamma_7, the color
class containing the characteristic vector z has size at least four.
The [previous lower bound](dimension-seven-characteristic-three.md)
was three. The remaining profiles (m_1,m_2; A,B,C)=(0,0;3,7,6)
and (0,2;1,9,6) are now excluded by the completion lemma and
conditional recoloring. Together with the preceding one-five,
C=7, and [C=8 exclusions](dimension-seven-four-four-hole-cover.md),
this closes the entire characteristic-size-three branch.

The line and full-subspace chromatic numbers still have lower bound
nineteen and remain open. Characteristic sizes four through eight
are not excluded, and no nineteen-color witness or numerical-bound
improvement is claimed.

## Finite completion with a universal normalization

Put z=127 and E=z-perp in the original seven-dimensional dot space.
The restriction of the form to E is nondegenerate alternating.
Any Lagrangian admits a symplectic dual basis, so an isometry of E
sends one chosen member of a six-member partial spread to

```text
L_0 minus {0}={3,12,15,48,51,60,63}.
```

The isometry extends to the original dot space by fixing z.
It is enough to exhaust all six-member partial spreads containing
L_0; no transitivity on partial spreads is assumed.

The [checker](../develop/check_dimension_seven_six_holes.py) constructs
the 135 Lagrangians from mutually orthogonal independent triples of
original even vectors. Independently it constructs all 1,395
three-dimensional subspaces in reduced row echelon form using
the symplectic basis (3,12,48,65,71,95), and retains the same 135
isotropic subspaces.

A bitmask clique enumeration and a separate array/set recursion
both enumerate exactly the same 3,584 six-member partial spreads
containing L_0. Neither search prunes using a completion assumption.
For every input, the twenty-one holes contain exactly three of the
135 Lagrangians. They are pairwise disjoint and their union is the
entire hole set. This proves existence and uniqueness of completion.
Seven- and nine-member spread enumerations are not rerun.

For an additional incidence control, the checker verifies every
hole set against the perpendicular hyperplane of each nonzero even
point. The intersection size is thirteen at hole points and nine
at covered points: 225,792 exact checks. Each existing Lagrangian
contributes seven points to the hyperplane when it contains the
point, and otherwise contributes three; subtracting from thirty-one
also gives these counts directly.

## Six orthogonal hole points lie in one completion member

Let the three hole Lagrangians be M_1,M_2,M_3. If G consists of six
distinct pairwise orthogonal hole points, its span Q is isotropic.
It has dimension three: a two-space has only three nonzero points,
and E has maximal isotropic dimension three.

If Q differs from every M_i, let d_i=dim(Q intersect M_i). Each
d_i is at most two, and d_i+d_j<=3 because the M_i are disjoint.
If some d_i=2, the total number of nonzero points in the three
intersections is at most 3+1+1=5. Otherwise it is at most three.
Both contradict six points of G lying in their union. Therefore
Q equals one M_i. The unique missing point q of that M_i is also
a hole, and q=sum G because the seven nonzero points sum to zero.

For a pure odd six-point color class D={z+g:g in G}, the vector
z+q can be added to D. It is new and pairs to one with every
member, so this gives a proper pure odd seven-point class.

## Moving the missing odd point excludes both final profiles

Assume a nineteen-coloring has |C_z|=3. The previous results leave
only the two profiles displayed above, both with six pure odd
heptads and at least one pure odd six-point defect. Choose such a
defect D. Its six projections are holes for the six existing pure
odd heptads, so the preceding argument supplies a missing hole q.

The odd vector z+q already has a color. It is outside D and cannot
belong to one of the six pure odd heptads, since q is a hole. A
pure even class has no odd members. Move z+q from its existing
class to D, preserving proper coloring. There are only these cases:

| Source of z+q | Result after moving it | Previously excluded condition |
| --- | --- | --- |
| Characteristic class | Its size falls from three to two | Characteristic size at least three |
| Mixed (6,1) class, starting from (0,0;3,7,6) | Two-six profile (0,6;3,6,7) | C=7 two-six exclusion |
| Mixed (6,1) class, starting from (0,2;1,9,6) | Two-six profile (2,6;1,8,7) | C=7 two-six exclusion |
| Other six-point defect in (0,2;1,9,6) | One five-point defect of type (2,3), with (A,B,C)=(1,9,7) | Entire one-five branch exclusion |

In (0,0;3,7,6), the other defect is also pure odd. It spans a
different hole Lagrangian: two disjoint six-point subsets cannot
occupy the same seven-point set. Hence it cannot contain q.
Alternatively, moving a point from any other six-point defect
would again produce the already excluded one-five branch.
The list exhausts every possible source color. Every case is
impossible, so neither remaining profile can occur.

This is a conditional recoloring of a hypothetical common coloring.
No individual partial classes are asserted to form a coloring,
and no full-coloring search is used. The old C=7 and one-five
exclusions apply to the recolored classes with their original
proof and finite dependencies intact.

## Evidence and next scope

The [report](../results/dimension-7-six-holes.json) binds the checker,
this note and the preceding four reports. It records identical
hashes for both Lagrangian catalogs and both six-spread enumerations,
completion uniqueness, hole incidence counts and the exact transfer
targets. Twenty-one local pure-odd six-class controls in one fixed
hole triple independently check their sums, new companions and
all pairings; they support the written argument rather than enumerate
all full colorings.

In that same fixed hole triple, 126 characteristic-source controls,
672 mixed-source controls and 288 other-defect-source controls verify
the three possible transfers against the original dot form. Each
control checks the proper source class, the completed pure odd class,
the reduced source and disjointness. These are local partial classes,
not asserted complete colorings; the written source-color case split
is the universal recoloring argument.

The characteristic class now has necessary size four through eight.
A concrete next problem is size four: the outside classes have total
deficit three from capacity seven, with defect-size patterns 4,
5+6, or 6+6+6. Their projection sums and counts must be derived
while retaining one common coloring. No exclusion or realizability
claim for those patterns is made here.

The earlier finite C=8 exact-cover proof remains a dependency of
the full size-three exclusion. This new completion/recoloring result
does not use a new SAT, exact-cover search, DRAT or Lean run.
The submitted manuscript at 28e27a8 and original six-dimensional
theorem with three standard and four native-evaluation axioms are
unchanged. Independent Pro review remains pending.

```sh
python3 develop/check_dimension_seven_six_holes.py --report /tmp/dimension-7-six-holes.json
```
