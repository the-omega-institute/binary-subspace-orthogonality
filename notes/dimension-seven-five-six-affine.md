# Four concentrated odd projections exclude two five-plus-six profiles

**Theorem.** For a nineteen-coloring of Gamma_7 with a characteristic
class of size four and outside defects of sizes five and six, the
following count profiles are impossible:

| Even counts (k5,k6) | Odd counts | Saturated counts (A,B,C) |
| --- | --- | --- |
| (5,2) | (0,4) | (8,0,8) |
| (1,6) | (4,0) | (8,0,8) |

The first is the specified next target after the
[single-four-defect exclusion](dimension-seven-single-four-exclusion.md).
The same short argument excludes the second. Of the 46 raw 5+6
count profiles, 44 remain unexcluded here and their joint feasibility
is untested. The 48 raw 6+6+6 profiles remain untested. This does
not exclude characteristic size four or improve the numerical bound:
the exact line and full-subspace chromatic numbers remain open,
with lower bound nineteen and no nineteen-color witness.

## Four odd members force zero characteristic charge

Write E=z-perp and C_z={z,z+e,z+f,z+g}, with h=e+f+g.
Both profiles have eight pure odd heptads and no mixed classes.
By the written eight-Lagrangian completion theorem, their seven
remaining odd projections form M minus {0}, for a Lagrangian M.
Those seven points partition into the three characteristic projections
and four odd projections a1,a2,a3,a4 belonging to one defect D.
That defect has at least one even member u.

Independence of D gives u dot ai=1 for all four i. Thus the
restriction ell=u dot(-)|M is nonzero, and its affine value-one
plane has exactly these four distinct points. The remaining three
nonzero points of M are ker(ell) minus {0}; these are precisely
e,f,g. The three nonzero points of a two-dimensional binary space
sum to zero, so

```text
h=e+f+g=0.
```

This is a universal linear-algebra argument. It does not assume
that all possible local defect classes fit in a common coloring.

## The quadratic charge equation gives a contradiction

Let w5,w6 be the projected sums of the two defects. The
[general size-four partition identities](dimension-seven-size-four.md)
give

```text
w5+w6=h,
w5 dot w6=A+B+tau5+tau6 mod 2,
tau_i=binom(size_i,2)+binom(odd_i,2) mod 2.
```

For either profile, tau5=0 and tau6=1. Since (A,B)=(8,0),
the second equation requires w5 dot w6=1. But the first equation
and h=0 imply w5=w6, whose self-pairing in the alternating space
E is zero. This contradiction excludes both profiles.

Equivalently, any size-four characteristic class with h=0 and two
outside defects requires A+B+tau5+tau6=0. The concentrated
four-odd geometry forces h=0 in these two profiles, and their
required parity is one. The other raw count profiles are not
classified by this note.

## Coordinate controls and evidence

The [checker](../develop/check_dimension_seven_five_six_affine.py)
works in a fixed Lagrangian M. It reconstructs affine planes in
two ways: from the seven nonzero functionals on a binary three-space,
and from all four-point subsets paired to one by an even vector.
The catalogs agree, with eight even vectors inducing each functional.
It checks every local defect with these four odd members: 56
five-point defects with one even member, and 112 six-point defects
with two even members. Independent array and bitmask even-pair
catalogs agree. For every one, the complementary characteristic
class is independent, disjoint from the defect, and has zero charge.
The checker also verifies the individual quadratic class identities.
These are 168 partial-class controls, not complete colorings.

Both targeted count/parity rows are independently derived and bound
to the prior report; all 44 other 5+6 rows are preserved without
feasibility claims. The [new report](../results/dimension-7-five-six-affine.json)
binds the checker, this note, the general charge analysis, and the
written eight-spread source. The new proof does not depend on
exact-cover search or a finite spread-completion enumeration.
No SAT, DRAT, Lean or independent Pro review is run. The submitted
manuscript at 28e27a8 is unchanged; the dimension-six formal theorem
retains three standard and four native-evaluation axioms.

```sh
python3 develop/check_dimension_seven_five_six_affine.py --report /tmp/dimension-7-five-six-affine.json
```
