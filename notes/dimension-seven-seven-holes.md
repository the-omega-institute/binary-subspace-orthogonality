# Seven odd heptads leave two complementary hole Lagrangians

**Completion lemma.** Seven pairwise disjoint Lagrangian three-spaces
in the six-dimensional binary symplectic space leave fourteen nonzero
points. These points are the disjoint union of the nonzero points of
two Lagrangians, uniquely determined by the holes.

The lemma is established by two exact coordinate enumerations and a
written symplectic transitivity reduction below. It is a finite proof,
not a purely incidence-theoretic proof or a Lean theorem.

**Coloring consequence.** A nineteen-coloring of Gamma_7 with a
three-point characteristic class and one five-point defective class
cannot have profile (D even,odd; A,B,C)=(0,5;3,7,7).
Together with the [completed-hole exclusion](dimension-seven-hole-cover.md),
this leaves only (1,4;2,8,7) in the one-five-defect branch.
The two-six-defect branch, larger characteristic classes, exact line
and full-subspace chromatic numbers, and nineteen-color witnesses remain
open. The numerical lower bound stays nineteen.

## A finite proof of the completion lemma

Fix the original binary dot space, z=127 and E=z-perp, with symplectic
basis (3,12,48,65,71,95). Put

```text
L_0 minus {0} = {3,12,15,48,51,60,63}.
```

Every Lagrangian has a symplectic dual basis. Sending this basis and
its dual to the fixed basis gives an isometry taking that Lagrangian
to L_0. Thus any seven-member partial spread can be normalized to
contain L_0; this does not require transitivity on partial spreads.
An isometry of E extends to the original dot space by fixing z.

The [checker](../develop/check_dimension_seven_seven_holes.py) constructs
all 135 Lagrangians from mutually orthogonal independent triples of
original even vectors. Its second construction enumerates all 1,395
three-dimensional subspaces in reduced row echelon form in symplectic
coordinates and retains the 135 isotropic subspaces. The two exact
sets agree.

A bitmask clique enumeration lists every seven-member partial spread
containing L_0: there are 1,792. A separate point-pivot exact-cover
enumeration lists all 64 complete nine-member spreads containing L_0.
Deleting two members other than L_0 gives exactly the same set of
1,792 partial spreads, with each occurring once. Equality of the two
sets proves existence and uniqueness of the completion for every
normalized input. Directly inspecting the fourteen holes also finds
exactly two contained Lagrangians, which are disjoint.

The exhaustive seven-member enumeration, the nine-member exact-cover
enumeration, and the deletion-set comparison are separate computations.
The argument neither assumes completion to prune the seven-member
search nor uses sampled partial spreads as universal evidence.

## Five odd defect points force a seven-clique obstruction

Write C_z={z,z+e,z+f}, with e,f distinct nonzero orthogonal vectors
of E, and put h=e+f. The seven pure odd heptads correspond to seven
disjoint Lagrangians. Their holes are M minus {0} and N minus {0},
where E=M direct-sum N and the pairing between M and N is nondegenerate.
All other odd projections belong to these holes.

In the profile (0,5;3,7,7), let G be the five projections of the
defect's odd vectors. They are pairwise orthogonal. If G met both
M and N, let a,b be the dimensions of the spans of its two parts.
Orthogonality and the perfect pairing give a+b<=3, with a,b>=1.
Their combined size is at most (2^a-1)+(2^b-1)<=4. Therefore all
five points of G lie in one hole Lagrangian, say M.

The global projected-sum identity gives sum G=h. This is nonzero.
Since h lies in M, and each of e,f lies in M or N, direct-sum
uniqueness forces both e and f into M. They are disjoint from G,
so G={nonzero points of M} minus {e,f}. The seven mixed odd
projections are consequently all the nonzero points of N.

The seven even points of N form a clique. Every mixed label is
forbidden there by its odd member in z+N. A defect label would
require an even point of N to pair to one with all five points
of G in M. A linear functional on M has at most four value-one
points, so this is impossible. Pure odd labels are unavailable
because their seven-point projections span their Lagrangians;
the characteristic label is forbidden by z. Only the three pure
even labels remain for a seven-clique, a contradiction.

## The remaining one-five profile has two local configurations

This is a necessary normalization, not a realizability claim.
For (D even,odd; A,B,C)=(1,4;2,8,7), write D={u,z+g_1,...,z+g_4}.
Its four pairwise orthogonal odd projections again lie in M union N.
If they met both sides, the preceding dimension argument forces
three points in a two-dimensional subspace on one side and one
point on the other. Those three points sum to zero; u cannot
pair to one with each of them. Hence all four g_i lie in M.

The restriction ell=u dot(-) on M is nonzero, and the four g_i
are its complete affine value-one plane. Their sum is zero, so
the global projected-sum identity forces u=e+f. The characteristic
projections e,f are not both in M. They are either both in N,
or one in M and one in N. In the second case, their orthogonality
puts the M member in ker ell.

An ordered pair of transverse Lagrangians determines a perfect
pairing. Changes of basis on one side, with the inverse dual
change on the other, act transitively on distinct nonzero pairs
in N, and on nonzero incident pairs e in M, f in N with e dot f=0.
Thus, after possibly exchanging e and f, the two local forms are:

| Case | (e,f,u) | Four odd defect projections |
| --- | --- | --- |
| Both characteristic projections in N | (65,71,6) | {3,12,51,60} |
| Characteristic projections on opposite sides | (3,71,68) | {12,15,60,63} |

Here M has basis (3,12,48), and N has dual basis (65,71,95).
Each local configuration satisfies the required characteristic and
defect independence and projected-sum constraints. Neither supplies
the eight mixed classes, the two even heptads, or the seven odd
heptads of a common coloring. Completing or excluding these two
coupled configurations is a concrete next problem.

## Verification and scope

The [report](../results/dimension-7-seven-holes.json) binds this note,
the checker, and the preceding completed-hole report. It records
exact set hashes for both Lagrangian enumerations, the seven-member
partial spreads and the independently reconstructed deletion set.
It checks hole sizes, unique completion, and the hyperplane hole
counts: ten for a hole's perpendicular hyperplane, six otherwise.
The 168 basis changes preserving a fixed ordered hole pair give two
disjoint orbits of 21 local configurations, exactly matching a direct
enumeration of all 42 allowed configurations for that pair. Their
original dot-form basis matrices and all local defect equations are
checked. These are individual local classes, not complete colorings.

No SAT, DRAT, Lean or independent Pro review is involved. The submitted
manuscript at 28e27a8 is unchanged; the original dimension-six Lean
theorem retains three standard and four native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_seven_holes.py --report /tmp/dimension-7-seven-holes.json
```
