# Nineteen-color line partitions: characteristic-class deficits

**Theorem.** The induced line graph Gamma_7 minus the characteristic
line z=127 requires at least nineteen colors. Consequently, in any
nineteen-coloring of Gamma_7, the class containing z has at least two
vertices. Its exact chromatic number and that of the full-subspace graph
remain open; no nineteen-color witness is supplied.

The argument strengthens the [previous lower bound](dimension-seven-nineteen-obstruction.md)
by locating it on the 126 lines avoiding z. It also restricts the
smallest possible class containing z to three necessary count profiles.
These are restrictions on a hypothetical coloring, not realized partitions.

## Deleting z still leaves a nineteen-color obstruction

Write E=z-perp. There are 63 nonzero even points u in E and 63 odd
lines z+e with e in E minus {0}. By the
[line-capacity lemma](dimension-seven-line-capacity.md), every independent
class in this deleted graph has at most seven vertices. An
eighteen-coloring would therefore consist of eighteen classes of size
seven. Such a class is either seven even points, six even points and
one odd line, or seven odd lines. Denote their counts by A,B,C. Then

```text
7A+6B=63,       B+7C=63,       A+B+C=18.
```

The only possibilities are (A,B,C)=(9,0,9) and (3,7,8).

The first would partition all even points into nine heptads. Each
heptad has odd sum under q(x,y)=x dot y, while q is one on 28 of the
63 even points. The quadratic parity obstruction excludes it.

In the second, the eight pure odd classes correspond to eight
pairwise zero-intersecting Lagrangian three-spaces in E. The universal
completion lemma from the previous proof makes the seven uncovered
nonzero points exactly M minus {0}, for a ninth Lagrangian M. These
are the seven e of the mixed odd lines. The seven even points of M
are adjacent to every mixed odd line and cannot use a pure odd label.
Only three pure even labels remain for this seven-clique, a
contradiction. This excludes eighteen colors after deleting z.

## The exact deficit identity

Suppose Gamma_7 has a proper nineteen-coloring. All nineteen labels
are nonempty by the preceding lower bound. Let C_z be the class
containing z and put s=|C_z|. Every even line is adjacent to z, so
C_z is purely odd and 1<=s<=8. The other eighteen classes avoid z
and have sizes at most seven. For them put delta_i=7-|C_i|. Counting
the 127 lines gives

```text
sum_i delta_i = 18*7-(127-s) = s-1.
```

If s=1, all other classes have size seven and give an impossible
eighteen-coloring of Gamma_7 minus z. Thus 2<=s<=8. If k is the
number of classes outside C_z of size less than seven, then

```text
1 <= k <= s-1 <= 7.
```

At least eleven classes outside C_z therefore have size seven.
Equivalently, the total deficit relative to capacity eight for C_z
and seven for the other classes is seven. This identity does not
assume that C_z fills an affine Lagrangian.

## A two-point characteristic class leaves only three count profiles

If s=2, exactly one other class D has size six; all seventeen
remaining classes have size seven. Write D's even and odd counts
as m and 6-m. The capacity table permits precisely

```text
m in {0,2,4,5,6}.
```

For the seventeen saturated classes, count A pure even heptads,
B mixed classes of type (6,1), and C pure odd heptads. The equations are

```text
7A+6B+m=63,       B+7C+(6-m)+2=64,
A+B+C=17.
```

Solving gives B=m+7t, A=9-m-6t, C=8-t. Nonnegativity gives seven
count profiles before further obstructions. Four are impossible:

| D type (even,odd) | (A,B,C) | Obstruction |
| --- | --- | --- |
| (0,6) | (9,0,8) | Nine even heptads fail quadratic parity |
| (4,2) | (5,4,8) | Seven-clique M has only five pure even labels |
| (5,1) | (4,5,8) | Seven-clique M has only four pure even labels |
| (6,0) | (3,6,8) | Seven-clique M has only four pure even labels, including D |

For the last three rows, C=8 again supplies eight disjoint
Lagrangians and their complementary M. All odd lines outside those
eight classes have their nonzero e in M: the one accompanying z,
the B mixed odd lines, and the odd part of D. Every mixed label is
therefore forbidden at each even point of M. C_z is forbidden because
it contains z; the eight saturated pure odd labels contain no even
points. Only pure even labels remain, including D exactly when m=6.
The displayed counts are strictly less than seven.

The three necessary surviving profiles are consequently

| D type (even,odd) | A pure even | B mixed (6,1) | C pure odd |
| --- | --- | --- | --- |
| (0,6) | 3 | 7 | 7 |
| (2,4) | 7 | 2 | 8 |
| (2,4) | 1 | 9 | 7 |

In the middle row, completion also forces each of the seven pure
even heptads to contain exactly one point of M. Each heptad meets
M in at most one point, since its pairwise products are one while
products within M are zero; all seven points of M must be covered.
Both even points of D and all even points of the mixed classes lie
outside M. None of these three profiles is asserted realizable.

## Verification and next step

The [standard-library checker](../develop/check_dimension_seven_nineteen_deficits.py)
enumerates the two deleted-graph saturation profiles and all seven
two-point-characteristic count profiles, checking the exclusions and
the three surviving necessary profiles. It checks the deficit identity
and allowable defective-class counts for every s from one through eight.
As coordinate controls, it constructs all 135 Lagrangians and 288 even
heptads, checks all 6,615 even-hole/odd-hole adjacencies, and all 38,880
heptad/Lagrangian intersections. The
[certificate](../results/dimension-7-nineteen-deficits.json) records source
identities and the precise scope.

The universal partial-spread completion and quadratic obstruction are
written proofs from the preceding note, not inferences from sampled
colorings. No coloring, checked UNSAT proof or Lean result is obtained.
The next structural targets are the three surviving s=2 profiles and
the larger-characteristic-class deficit cases. A line coloring alone
would still need compatible colors for the isotropic planes and
three-spaces to settle the full graph.

```sh
python3 develop/check_dimension_seven_nineteen_deficits.py --report /tmp/dimension-7-nineteen-deficits.json
```

The submitted manuscript at 28e27a8 is unchanged. The original
dimension-six Lean theorem retains three standard and four
native-evaluation axioms. The full n=7 problem remains open with
lower bound nineteen.
